import { test, expect } from '@playwright/test';
import { selectRoute } from './routes.js';

test.use({ baseURL: 'http://127.0.0.1:4174' });

test('real server keeps stages 8-10 planned from backend through rendered frontend', async ({ page }) => {
  const response = await page.request.get('/api/release/development-timeline');
  expect(response.ok()).toBeTruthy();
  const timeline = await response.json();
  expect(timeline.consciousness_claim).toBe('unsupported');

  for (const number of [8, 9, 10]) {
    const stage = timeline.stages.find(item => item.stage === number);
    expect(stage, `stage ${number} missing`).toBeTruthy();
    expect(stage.status).toBe('planned');
    expect(stage.implementation_score).toBe(0);
    expect(stage.criteria.every(item => item.status === 'planned')).toBeTruthy();
  }

  const placeholderResponse = await page.request.get('/development-frontier-placeholders.json');
  expect(placeholderResponse.ok()).toBeTruthy();
  const placeholders = await placeholderResponse.json();
  expect(placeholders.status).toBe('PLANNED_RESEARCH_ONLY');
  expect(placeholders.stages['8'].solution_placeholders).toContain('SynapticConsolidationContract');
  expect(placeholders.stages['9'].solution_placeholders).toContain('AttentionGainContract');
  expect(placeholders.stages['10'].observer_module).toBe('src/research/self_monitor.py');
  expect(placeholders.stages['10'].claim_boundary).toContain('read-only');

  await page.goto('/');
  await selectRoute(page, 'release', 'development');

  for (const number of [8, 9, 10]) {
    const card = page.locator(`#development-stage-list [data-development-stage="${number}"]`);
    await expect(card).toBeVisible();
    await expect(card).toContainText('planned');
  }

  await page.locator('#development-stage-list [data-development-stage="10"]').click();
  const detail = page.locator('#development-detail');
  await expect(detail).toBeVisible();
  await expect(detail).toContainText('Bewusstseinsforschung');
  await expect(detail).toContainText('never automatically establishes consciousness');
  await expect(detail).toContainText('E10-A through E10-H');
});
