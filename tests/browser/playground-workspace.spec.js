import { test, expect } from "@playwright/test";
import { selectRoute } from "./routes.js";

test.beforeEach(async ({ page }) => {
  await page.goto(
    process.env.MHRN_PLAYGROUND_TEST_URL || "http://127.0.0.1:4174/",
  );
  await page.locator('[data-mhrn-language="de"]').click();
  await selectRoute(page, "playground", "builder");
  await expect(page.locator("#pg-groups")).toBeVisible();
});

test("PAN full profile is the initial default and restores its I/O payload", async ({
  page,
}) => {
  await expect(page.locator("#pg-user-preset-select")).toHaveValue(
    "pan_full_balanced",
  );
  await expect(page.locator("#pg-neurons")).toHaveValue("256");
  await expect(page.locator("#pg-ticks")).toHaveValue("2000");
  await expect(page.locator("#pg-pan-enabled")).toBeChecked();
  await expect(page.locator("#pg-neural-io-enabled")).toBeChecked();
  await expect(page.locator("#pg-input-channels")).toHaveValue("8");
  await expect(page.locator("#pg-offload-enabled")).not.toBeChecked();
  await expect(page.locator("#pg-neural-io-payload")).toHaveValue("0.5");
});

test("guided groups preserve controls and validate channel edits with undo", async ({
  page,
}) => {
  await expect(page.locator(".pg-group")).toHaveCount(6);
  await expect(page.locator("#pg-run")).toBeEnabled();
  await page.locator("#pg-group-3 > summary").click();
  const original = await page.locator("#pg-input-channels").inputValue();
  await page.locator("#pg-input-channels").fill("10");
  await page.locator("#pg-input-channels").press("Tab");
  await expect(page.locator("#pg-channel-rows tr")).toHaveCount(10);
  await page
    .getByRole("spinbutton", { name: "Kanal 0 Amplitude", exact: true })
    .fill("600");
  await expect(page.locator("#pg-run")).toBeDisabled();
  await expect(page.locator("#pg-validation")).toContainText("Amplitude");
  await page
    .getByRole("spinbutton", { name: "Kanal 0 Amplitude", exact: true })
    .fill("12");
  await page
    .getByRole("spinbutton", { name: "Kanal 0 Amplitude", exact: true })
    .press("Tab");
  await expect(page.locator("#pg-run")).toBeEnabled();
  expect(
    JSON.parse(await page.locator("#pg-input-amplitudes").inputValue())[0],
  ).toBe(12);
  await page.locator("#pg-workspace-undo").click();
  expect(
    JSON.parse(await page.locator("#pg-input-amplitudes").inputValue())[0],
  ).not.toBe(12);
  await page.locator("#pg-workspace-undo").click();
  await expect(page.locator("#pg-input-channels")).toHaveValue(original);
});

test("configuration export/import restores values and rejects malformed files", async ({
  page,
}) => {
  await page.locator("#pg-neurons").fill("96");
  await page.locator("#pg-neurons").press("Tab");
  const downloaded = page.waitForEvent("download");
  await page.locator("#pg-workspace-export").click();
  const file = await downloaded;
  const path = await file.path();
  await page.locator("#pg-neurons").fill("64");
  await page.locator("#pg-workspace-file").setInputFiles(path);
  await expect(page.locator("#pg-neurons")).toHaveValue("96");
  await page.locator("#pg-workspace-file").setInputFiles({
    name: "invalid.json",
    mimeType: "application/json",
    buffer: Buffer.from('{"bad":true}'),
  });
  await expect(page.locator("#pg-workspace-message")).toContainText(
    "Import fehlgeschlagen",
  );
  await expect(page.locator("#pg-neurons")).toHaveValue("96");
});

test("CPU run and CUDA compilation remain connected to the real server", async ({
  page,
}) => {
  await page.locator("#pg-neurons").fill("32");
  await page.locator("#pg-edges").fill("64");
  await page.locator("#pg-group-1 > summary").click();
  await page.locator("#pg-ticks").fill("16");
  await page.locator("#pg-ticks").press("Tab");
  await page.locator("#pg-run").click();
  await expect(page.locator("#pg-status")).toContainText("Lauf abgeschlossen");
  await expect(page.locator("#pg-result-summary")).toContainText("Session");
  await expect(page.locator("#pg-result-summary")).toContainText(
    "Reiz-Kontexte",
  );
  await expect(page.locator("#pg-metrics")).toContainText("Spikes");
  await selectRoute(page, "playground", "builder");
  await page.locator("#pg-group-5 > summary").click();
  await page.locator("#pg-cuda-compile").click();
  await expect(page.locator("#pg-cuda-compiler-state")).toContainText(
    "kernel_abi",
  );
});

test("presets, secondary pages and narrow layouts remain usable", async ({
  page,
}) => {
  await page.locator("#pg-workspace-preset-search").fill("minimal_closed_loop");
  const card = page
    .locator(".pg-preset-card:visible")
    .filter({ hasText: "minimal_closed_loop" })
    .first();
  await card.getByRole("button", { name: "Anwenden", exact: true }).click();
  await expect(page.locator("#pg-user-preset-select")).toHaveValue(
    "minimal_closed_loop",
  );
  await page.locator("#pg-group-5 > summary").click();
  await expect(page.locator("#pg-cuda-smoke")).toBeVisible();
  await expect(page.locator("#pg-cuda-rng")).toBeVisible();
  await selectRoute(page, "playground", "run");
  await expect(page.locator("#pg-result-summary")).toContainText(
    "Noch kein Lauf",
  );
  await selectRoute(page, "playground", "sessions");
  await expect(page.locator("#pg-workspace-session-search")).toBeVisible();
  await selectRoute(page, "playground", "catalog");
  await page
    .locator("#pg-workspace-catalog-search")
    .fill("not-a-real-component");
  await expect(page.locator("#pg-catalog-grid article:visible")).toHaveCount(0);
  await selectRoute(page, "playground", "builder");
  await page.setViewportSize({ width: 390, height: 844 });
  await expect(page.locator("#pg-workspace-export")).toBeVisible();
  expect(
    await page
      .locator("#pg-groups")
      .evaluate((e) => e.scrollWidth <= e.clientWidth + 1),
  ).toBe(true);
});

test("recurrent CUDA diagnostic reports unavailability without a CPU success fallback", async ({
  page,
}) => {
  await page.route("**/api/playground/cuda/recurrent-parity", async (route) => {
    const payload = route.request().postDataJSON();
    expect(payload.n_neurons).toBe(129);
    expect(payload.ticks).toBe(100);
    await route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({ error: "CUDA driver unavailable" }),
    });
  });
  await page.locator("#pg-group-5 > summary").click();
  await page.locator("#pg-cuda-recurrent").click();
  await expect(page.locator("#pg-cuda-recurrent-state")).toContainText(
    "CUDA driver unavailable",
  );
  await page.locator("#pg-cuda-plasticity").click();
  await expect(page.locator("#pg-cuda-plasticity-state")).toContainText(
    "CUDA driver unavailable",
  );
});

test("Builder run renders the coupled PAN body and recorded frame replay", async ({
  page,
}) => {
  await page.locator("#pg-neurons").fill("32");
  await page.locator("#pg-edges").fill("64");
  await page.locator("#pg-group-1 > summary").click();
  await page.locator("#pg-ticks").fill("128");
  await page.locator("#pg-ticks").press("Tab");
  await page.locator("#pg-run").click();
  await expect(page.locator("#pg-run-sandbox-panel")).toBeVisible();
  await expect(page.locator("#pg-run-sandbox-state")).toContainText(
    "CPU_REFERENCE",
  );
  await expect(page.locator("#pg-run-sandbox-summary")).toContainText(
    "Haltung",
  );
  expect(
    await page
      .locator("#pg-run-sandbox-panel")
      .evaluate((el) => el.getBoundingClientRect().height),
  ).toBeLessThan(800);
  await expect(page.locator("#pg-run-sandbox-frame")).toHaveAttribute(
    "max",
    "127",
  );
  await page.locator("#pg-run-sandbox-frame").fill("0");
  await expect(page.locator("#pg-run-sandbox-state")).toContainText(
    '"pan_action": null',
  );
  await expect(page.locator("#pg-analysis-io")).toContainText("cue_decoding");
});

test("CUDA Builder choice and D3 control use explicit endpoints without fallback", async ({
  page,
}) => {
  await page.locator("#pg-workspace-expand").click();
  await page.locator("#pg-neuron-backend").selectOption("cuda_membrane");
  let attempts = 0;
  await page.route("**/api/playground/run", async (route) => {
    attempts++;
    expect(route.request().postDataJSON().neuron_backend).toBe("cuda_membrane");
    await route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({ error: "GPU unavailable" }),
    });
  });
  await page.locator("#pg-run").click();
  await expect(page.locator("#pg-status")).toContainText("GPU unavailable");
  expect(attempts).toBe(1);
  await page.route("**/api/playground/cuda/builder-parity", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        passed: false,
        scope: "REAL_BUILDER_CUDA_MEMBRANE_CPU_SYNAPSES_AND_ENVIRONMENT",
      }),
    }),
  );
  await page.locator("#pg-cuda-builder-parity").click();
  await expect(page.locator("#pg-cuda-builder-parity-state")).toContainText(
    "REAL_BUILDER_CUDA_MEMBRANE",
  );
});

test("randomized cue selection and paired research controls are wired", async ({
  page,
}) => {
  await page.locator("#pg-workspace-expand").click();
  await page.locator("#pg-target-cue-control").selectOption("randomized");
  await page.route("**/api/playground/research/cue-controls", async (route) => {
    expect(route.request().postDataJSON().target_cue_control).toBe(
      "randomized",
    );
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        classification: "PLAYGROUND_CUE_INTERVENTION_SUITE",
        conditions: [],
        neural_learning_claim: false,
      }),
    });
  });
  await page.locator("#pg-cue-controls").click();
  await expect(page.locator("#pg-cue-controls-state")).toContainText(
    "PLAYGROUND_CUE_INTERVENTION_SUITE",
  );
  await expect(page.locator("#pg-cue-controls-state")).toContainText(
    '"neural_learning_claim": false',
  );
});

test("synaptic transfer control displays bounded interpretation", async ({
  page,
}) => {
  await page.locator("#pg-workspace-expand").click();
  await page.route("**/api/playground/research/synaptic-transfer", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        classification: "PLAYGROUND_SYNAPTIC_TRANSFER_PROBE",
        changed_pretraining_weights: 64,
        neural_transfer_claim: false,
        conditions: [],
      }),
    }),
  );
  await page.locator("#pg-synaptic-transfer").click();
  await expect(page.locator("#pg-transfer-summary")).toContainText(
    "64 veraenderte Gewichte",
  );
  await expect(page.locator("#pg-transfer-summary")).toContainText(
    "kein automatischer Nachweis",
  );
  await expect(page.locator("#pg-transfer-state")).toContainText(
    '"neural_transfer_claim": false',
  );
});
