import { test, expect } from '@playwright/test';
import { selectRoute } from './routes.js';

for (const port of [4174, 4175]) {
  test(`cognition ${port}: actual reference, field errors, export and independent read control`, async ({ page }) => {
    const base = `http://127.0.0.1:${port}`;
    await page.request.post(`${base}/__test__/cognition`, { data: { available: true } });
    await page.goto(base);
    await selectRoute(page, 'wesen', 'cognition');
    const panel = page.locator('#mhrn-cognition');
    await expect(panel).toBeVisible();
    await expect(panel.locator('[data-world]')).toContainText('categorical_mismatch');
    await expect(panel.locator('[data-world]')).toContainText('false');
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      panel.locator('[data-prediction-export]').click(),
    ]);
    expect(download.suggestedFilename()).toBe('mhrn-predictions-bounded.json');
    const stream = await download.createReadStream();
    const chunks = [];
    for await (const chunk of stream) chunks.push(chunk);
    const exported = JSON.parse(Buffer.concat(chunks).toString('utf8'));
    expect(exported.scientific_evidence).toBe(false);
    expect(exported.scope).toBe('visible_bounded_prediction_records');
    expect(exported.predictions).toHaveLength(3);
    expect(exported.predictions[2].error_components.numeric_absolute.position).toBe(0);
    await panel.locator('#cognition-read-enabled').uncheck();
    await expect(panel.locator('[data-message]')).toContainText('bestätigt');
    await expect(panel.locator('[data-prediction-export]')).toHaveCount(0);
    await expect(panel.locator('[data-world]')).toContainText('nicht verfügbar');
    expect((await (await page.request.get(`${base}/api/cognition/state`)).json()).memory.latest_prediction).toBeNull();
    const world = await (await page.request.get(`${base}/api/cognition/world-model`)).json();
    expect(world.model).toBeNull();
    expect(world.learning_enabled).toBe(true);
    expect(world.prediction_enabled).toBe(true);
    await page.request.post(`${base}/__test__/cognition`, { data: { available: false } });
  });
}

test('cognition does not retain an active badge or confirmed write after a failed request', async ({ page }) => {
  const base = 'http://127.0.0.1:4174';
  await page.request.post(`${base}/__test__/cognition`, { data: { available: true } });
  await page.goto(base);
  await selectRoute(page, 'wesen', 'cognition');
  const panel = page.locator('#mhrn-cognition');
  await expect(panel.locator('#cognition-state-badge')).toHaveText('active');
  await page.route('**/api/cognition/memory/controls', route => route.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ error: 'fixture write rejected' }) }));
  await panel.locator('#cognition-read-enabled').uncheck();
  await expect(panel.locator('[data-message]')).toContainText('Nicht gespeichert');
  await expect(panel.locator('#cognition-read-enabled')).toBeChecked();
  await page.route('**/api/cognition/state', route => route.fulfill({ status: 503, contentType: 'application/json', body: '{}' }));
  await panel.locator('[data-refresh]').click();
  await expect(panel.locator('#cognition-state-badge')).toHaveText('unavailable');
  await page.request.post(`${base}/__test__/cognition`, { data: { available: false } });
});


test('a delayed pre-write poll cannot restore enabled memory reads or old exports', async ({ page }) => {
  const base = 'http://127.0.0.1:4174';
  await page.request.post(`${base}/__test__/cognition`, { data: { available: true } });
  await page.goto(base);
  await selectRoute(page, 'wesen', 'cognition');
  const panel = page.locator('#mhrn-cognition');
  await expect(panel.locator('[data-prediction-export]')).toBeVisible();
  let release;
  let announce;
  const held = new Promise(resolve => { release = resolve; });
  const received = new Promise(resolve => { announce = resolve; });
  let first = true;
  await page.route('**/api/cognition/memory', async route => {
    if (!first) { await route.continue(); return; }
    first = false;
    const response = await route.fetch();
    announce();
    await held;
    await route.fulfill({ response });
  });
  try {
    await panel.locator('[data-refresh]').click();
    await received;
    await panel.locator('#cognition-read-enabled').uncheck();
    await expect(panel.locator('[data-message]')).toContainText('best\u00e4tigt');
    release();
    await expect(panel.locator('[data-prediction-export]')).toHaveCount(0);
    await expect(panel.locator('#cognition-read-enabled')).not.toBeChecked();
    await expect(panel.locator('[data-world]')).toContainText('nicht verf\u00fcgbar');
  } finally {
    release();
    await page.unroute('**/api/cognition/memory');
    await page.request.post(`${base}/__test__/cognition`, { data: { available: false } });
  }
});
