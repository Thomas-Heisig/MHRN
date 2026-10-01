import { test, expect } from '@playwright/test';
import { selectRoute } from './routes.js';

test('CUDA FE3 integration status is visible in the correct workspaces', async ({ page }) => {
  await page.goto(process.env.MHRN_ACCELERATION_TEST_URL || 'http://127.0.0.1:4174/');

  await selectRoute(page, 'playground', 'builder');
  await expect(page.locator('#mhrn-acceleration-playground')).toBeVisible();
  await expect(page.locator('#mhrn-acceleration-playground')).toContainText('FE-3 Live Backend Bridge');
  await expect(page.locator('#mhrn-acceleration-playground')).toContainText('PAN Wave 5B');
  await expect(page.locator('#mhrn-acceleration-playground')).toContainText('PAN_CONTRACT_NOT_FROZEN');

  const acceleration = await page.evaluate(async () => {
    const response = await fetch('/api/integration/status', { cache: 'no-store' });
    return (await response.json()).acceleration;
  });
  expect(acceleration.pan_wave5b_preflight.preflight_ready).toBe(true);
  expect(acceleration.pan_wave5b_preflight.ready_for_execution).toBe(false);

  await selectRoute(page, 'release', 'development');
  await expect(page.locator('#mhrn-acceleration-release')).toBeVisible();
  await expect(page.locator('#mhrn-acceleration-release')).toContainText('Engineering Acceptance');

  await selectRoute(page, 'science', 'observatory');
  await expect(page.locator('#mhrn-acceleration-science')).toBeVisible();
  await expect(page.locator('#mhrn-acceleration-science')).toContainText('keine DATA / keine EVID');

  await selectRoute(page, 'old', 'overview');
  await expect(page.locator('#mhrn-acceleration-old')).toBeVisible();
  await expect(page.locator('#mhrn-acceleration-old')).toContainText('OLD-Regel');
});
