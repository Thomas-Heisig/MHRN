import { test, expect } from '@playwright/test';
import { selectRoute } from './routes.js';

test.use({ baseURL: 'http://127.0.0.1:4174' });

for (const port of [4174, 4175]) {
  test(`publication ${port}: complete current reader and immutable historical sources`, async ({ page }) => {
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`http://127.0.0.1:${port}/`);
    await selectRoute(page, 'files', 'browse');
    await page.getByRole('button', { name: 'Abhandlung lesen', exact: true }).click();
    const viewer = page.locator('#fm-viewer');
    await expect(viewer).toHaveAttribute('data-render-state', 'ready');
    await expect(viewer).toContainText('Fassung 1.5');
    await viewer.getByRole('button', { name: 'Dissertationsmanuskript und Forschungsarbeit', exact: true }).click();
    await expect(viewer).toContainText('Menschliches wissenschaftliches Review');
    const prefix = `http://127.0.0.1:${port}/api/files/preview/`;
    const catalogue = JSON.parse((await (await page.request.get(prefix + encodeURIComponent('publications/catalog.json') + '?source=research')).json()).content);
    const current = catalogue.publications.filter(item => item.current);
    expect(current).toHaveLength(1);
    expect(current[0].version).toBe('1.5');
    expect(current[0].authority).toBe('interpretation_only');
    expect(current[0].automatic_evidence_promotion).toBe(false);
    const base = current[0].snapshot + '/';
    const manifest = JSON.parse((await (await page.request.get(prefix + encodeURIComponent(base + 'manifest.json') + '?source=research')).json()).content);
    expect(manifest.section_count).toBe(69);
    expect(manifest.accepted_evidence).toBe(false);
    for (const name of manifest.section_order) {
      const response = await page.request.get(prefix + encodeURIComponent(base + name) + '?source=research');
      expect(response.ok(), name).toBeTruthy();
      const descriptor = await response.json();
      expect(descriptor.truncated, name).toBe(false);
      expect(descriptor.read_only, name).toBe(true);
      expect(descriptor.editable, name).toBe(false);
    }
    await viewer.getByRole('button', { name: 'Quellenbindung und Zusammenfassung', exact: true }).click();
    await expect(viewer).toContainText('EXP-EMP-20260913-A3');
    await expect(viewer.getByRole('button', { name: 'Bearbeiten', exact: true })).toHaveCount(0);
    const historical = JSON.parse((await (await page.request.get(prefix + encodeURIComponent('publications/reader/manifest.json') + '?source=research')).json()).content);
    expect(historical.section_count).toBe(46);
    for (const section of historical.sections) {
      const response = await page.request.get(prefix + encodeURIComponent(`publications/reader/${section.path}`) + '?source=research');
      const descriptor = await response.json();
      expect(descriptor.truncated, section.path).toBe(false);
      expect(descriptor.read_only, section.path).toBe(true);
      expect(descriptor.content, section.path).toContain('Inhaltsuebersicht');
    }
    const write = await page.request.put(`http://127.0.0.1:${port}/api/files/document/` + encodeURIComponent(base + 'README.md') + '?source=research', {
      data: { action: 'write', content: 'unauthorized change', expected_sha256: 'invalid' },
    });
    expect(write.status()).toBe(403);
    expect(errors).toEqual([]);
  });
}
