import { test, expect } from '@playwright/test';
import { selectRoute } from './routes.js';

test('nested focus restores ancestor paths without leaking siblings or duplicate review panels', async ({ page }) => {
  await page.goto('http://127.0.0.1:4174/');
  await selectRoute(page, 'wesen', 'live');
  await expect(page.locator('.wesen-layout')).toBeVisible();
  await selectRoute(page, 'wesen', 'symbiosis');
  const target = page.locator('#wesen-neural-symbiosis');
  await expect(target).toBeVisible();
  expect(await target.evaluate(node => {
    for (let parent = node; parent; parent = parent.parentElement) {
      if (parent.hidden || parent.inert || getComputedStyle(parent).display === 'none') return false;
    }
    return true;
  })).toBe(true);
  await expect(page.locator('.wesen-layout > [data-mhrn-focus-sibling]:visible')).toHaveCount(0);
  await selectRoute(page, 'wesen', 'live');
  await expect(page.locator('.wesen-layout [data-mhrn-focus-sibling]')).toHaveCount(0);
  await expect(target).toBeVisible();
  await selectRoute(page, 'review', 'external');
  await expect(page.locator('#review-external-mount #external-review-status')).toBeVisible();
  await expect(page.locator('#external-review-status')).toHaveCount(1);
  await expect(page.locator('#tab-research #external-review-status')).toHaveCount(0);
});
