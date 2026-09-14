import { expect } from '@playwright/test';

// Exercise visible public navigation rather than clicking hidden legacy buttons.
export async function selectRoute(page, area, route = 'overview') {
  await page.locator(`[data-mhrn-area="${area}"]`).click();
  if (route !== 'overview') {
    await page.locator(`[data-area-overview="${area}"] [data-route-card="${route}"]`).click();
  }
  await expect(page.locator('body')).toHaveAttribute('data-current-area', area);
  await expect(page.locator('body')).toHaveAttribute('data-current-route', route);
}

export async function selectLabStage(page, stage) {
  await selectRoute(page, 'science', 'experiments');
  await page.locator(`[data-lab-stage-button="${stage}"]`).click();
  await expect(page.locator(`[data-lab-stage="${stage}"]`)).toBeVisible();
}

export async function selectResearchView(page, view) {
  if (view === 'files') return selectRoute(page, 'files', 'browse');
  if (view === 'external') return selectRoute(page, 'review', 'external');
  const stage = { plan: 'run', runs: 'series', review: 'evidence', question: 'question', results: 'results' }[view];
  if (!stage) throw new Error(`Unknown research view: ${view}`);
  await selectLabStage(page, stage);
}
