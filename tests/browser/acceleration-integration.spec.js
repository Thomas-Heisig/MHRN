import { test, expect } from '@playwright/test';
import { selectRoute } from './routes.js';

test('CUDA FE3 integration status is visible in the correct workspaces', async ({ page }) => {
  await page.goto('/');

  await selectRoute(page, 'playground', 'builder');
  await expect(page.locator('#mhrn-acceleration-playground')).toBeVisible();
  await expect(page.locator('#mhrn-acceleration-playground')).toContainText('FE-3 Live Backend Bridge');

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
