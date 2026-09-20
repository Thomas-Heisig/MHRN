import { test, expect } from '@playwright/test';

for (const width of [390, 1280]) {
  test(`MHRN bilingual identity at ${width}px`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('http://127.0.0.1:4174/');
    await expect(page).toHaveTitle(/MHRN/);
    await expect(page.locator('.project-title')).toHaveText('Multi-Scale Homeostatic Recurrence Network');
    await expect(page.locator('.project-subtitle')).toHaveText('Mehrskaliges homöostatisches Rekurrenznetzwerk');
    await expect(page.locator('body')).toHaveAttribute('data-ui-language', 'en');
    await expect(page.locator('.project-title')).toBeVisible();
    await expect(page.locator('.project-subtitle')).toBeHidden();
    const title = await page.locator('.project-title').boundingBox();
    expect(title).not.toBeNull();
    expect(title.x).toBeGreaterThanOrEqual(0);
    expect(title.x + title.width).toBeLessThanOrEqual(width);

    await page.locator('[data-mhrn-language="de"]').click();
    await expect(page.locator('body')).toHaveAttribute('data-ui-language', 'de');
    await expect(page.locator('.project-title')).toBeHidden();
    await expect(page.locator('.project-subtitle')).toBeVisible();
    const subtitle = await page.locator('.project-subtitle').boundingBox();
    expect(subtitle).not.toBeNull();
    expect(subtitle.x).toBeGreaterThanOrEqual(0);
    expect(subtitle.x + subtitle.width).toBeLessThanOrEqual(width);
    await page.screenshot({ path: testInfo.outputPath(`mhrn-${width}.png`), fullPage: true });
  });
}
