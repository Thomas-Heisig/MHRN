"""Exercise the export package under a project subpath with no collector."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread

from playwright.sync_api import expect, sync_playwright

from review_portal.build_static import build


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    with TemporaryDirectory(prefix="review-static-") as directory:
        root = Path(directory)
        build(root / "MHRN")
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(QuietHandler, directory=directory)
        )
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(
                    channel=os.environ.get("MHRN_TEST_BROWSER_CHANNEL")
                )
                page = browser.new_page(accept_downloads=True)
                errors, requests = [], []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on("request", lambda request: requests.append(request))
                url = f"http://127.0.0.1:{server.server_port}/MHRN/index.html"
                page.goto(url, wait_until="networkidle")
                expect(page.locator("#mode")).to_contain_text("kein Versand")
                expect(page.locator("a[href='./privacy.html']")).to_be_visible()
                expect(page.locator(".withdrawal")).not_to_be_visible()
                page.locator("#adult").check()
                page.locator("#consent").check()
                page.locator("#start").click()
                page.locator('.question:has(.qid:text-is("A4")) textarea').first.fill(
                    "SYNTHETIC EXPORT TEST"
                )
                assert page.evaluate("localStorage.length") == 0
                with page.expect_download() as download:
                    page.locator("#save").click()
                assert "SYNTHETIC EXPORT TEST" in Path(download.value.path()).read_text(
                    encoding="utf-8"
                )
                page.set_viewport_size({"width": 390, "height": 844})
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                expect(page.locator("#online")).not_to_be_visible()
                assert not errors, errors
                assert all("/api/" not in r.url and r.method == "GET" for r in requests)
                page.goto(url.replace("index.html", "privacy.html"))
                expect(page.locator("h1")).to_have_text("Datenschutz und lokaler Export")
                browser.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
    print("PASS: project subpath, offline export, privacy page, mobile; zero API requests")


if __name__ == "__main__":
    main()
