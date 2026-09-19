import { test, expect } from '@playwright/test';
import { selectRoute } from './routes.js';

test.use({ baseURL: 'http://127.0.0.1:4174' });

for (const port of [4174, 4175]) {
 for (const popup of [true, false]) {
  test(`publication ${port} ${popup ? "popup" : "inline"}: current v1.8 and frozen v1.5 remain separately reachable`, async ({ page }) => {
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`http://127.0.0.1:${port}/`);
    await selectRoute(page, 'files', 'browse');
    await page.locator('#fm-popup-toggle').setChecked(popup);
    await page.getByRole('button', { name: 'Abhandlung lesen', exact: true }).click();
    const viewer = page.locator(popup ? '#fm-dialog-viewer' : '#fm-viewer');
    await expect(viewer).toBeVisible();
    await expect(viewer).toHaveAttribute('data-render-state', 'ready');
    await expect(viewer).toContainText('Edition 1.8');

    const currentApiResponse = await page.request.get(`http://127.0.0.1:${port}/api/publication/current`);
    const currentApiText = await currentApiResponse.text();
    expect(currentApiResponse.ok(), currentApiText).toBeTruthy();
    const currentApi = JSON.parse(currentApiText);
    expect(currentApi.edition).toBe('1.8');
    expect(currentApi.entrypoint_path).toContain('v1.8/MANUSCRIPT.md');
    expect(currentApi.document_title).toContain('Rekursive Epistemik');
    expect(currentApi.content).toContain('## Inhaltsverzeichnis');
    expect(currentApi.content).toContain('Teil XI');
    expect(currentApi.content).toContain('# Anhang — Quellen und Vorarbeiten');
    expect(currentApi.chapters).toHaveLength(11);
    expect(currentApi.attachments.map(item => item.path)).toEqual(expect.arrayContaining([
      expect.stringContaining('CONTENT_INTEGRATION.md'),
      expect.stringContaining('RESEARCH_REGISTER.md'),
      expect.stringContaining('SOURCE_INDEX.md'),
      expect.stringContaining('REFERENCES.md'),
      expect.stringContaining('manifest.json'),
    ]));
    expect(currentApi.history.map(item => item.label)).toEqual(expect.arrayContaining([
      'Aktuelle Arbeitsfassung',
      'Frozen empirical baseline',
      'Vorgänger 1.7',
    ]));

    await page.evaluate(() => window.MHRNWorkspaceArchitecture?.selectRoute?.('publication', 'overview'));
    await expect(page.locator('body')).toHaveAttribute('data-current-area', 'publication');
    const publicationPanel = page.locator('#publication-panel');
    await expect(publicationPanel).toBeVisible();
    const readerLink = publicationPanel.locator('a[data-pub-reader-link]').first();
    await expect(readerLink).toBeVisible();
    const readerHref = await readerLink.getAttribute('href');
    expect(readerHref).toBeTruthy();
    expect(readerHref).not.toBe('#');
    expect(readerHref).toContain('/api/files/raw/');

    const prefix = `http://127.0.0.1:${port}/api/files/preview/`;
    const catalogue = JSON.parse((await (await page.request.get(prefix + encodeURIComponent('publications/catalog.json') + '?source=research')).json()).content);
    const current = catalogue.publications.filter(item => item.current);
    expect(current).toHaveLength(1);
    expect(current[0].version).toBe('1.8');
    expect(current[0].edition_status).toBe('current_wip');
    expect(current[0].authority).toBe('interpretation_only_work_in_progress');
    expect(current[0].automatic_evidence_promotion).toBe(false);
    expect(current[0].entrypoint).toContain('v1.8/MANUSCRIPT.md');
    expect(current[0].predecessor).toBe('PUB-RECURSIVE-EPISTEMICS-20260915-V1.7');
    expect(current[0].inherits_empirical_edition).toBe('PUB-RECURSIVE-EPISTEMICS-20260913-V1.5');

    const currentManuscript = await page.request.get(prefix + encodeURIComponent(current[0].entrypoint) + '?source=research');
    expect(currentManuscript.ok()).toBeTruthy();
    const currentDescriptor = await currentManuscript.json();
    expect(typeof currentDescriptor.truncated).toBe('boolean');
    expect(currentDescriptor.read_only).toBe(true);
    expect(currentDescriptor.editable).toBe(false);

    const currentRaw = await page.request.get(
      `http://127.0.0.1:${port}/api/files/raw/${encodeURIComponent(current[0].entrypoint)}?source=research`,
    );
    expect(currentRaw.ok()).toBeTruthy();
    const currentRawText = await currentRaw.text();
    expect(currentRawText).toContain('Edition 1.8');
    expect(currentRawText).toContain('Frozen 1.5');
    expect(currentRawText).toContain('Stage 6');

    const currentManifest = JSON.parse((await (await page.request.get(prefix + encodeURIComponent(current[0].manifest) + '?source=research')).json()).content);
    expect(currentManifest.version).toBe('1.8');
    expect(currentManifest.edition_status).toBe('current_wip');
    expect(currentManifest.viewer_entrypoint).toBe('MANUSCRIPT.md');
    expect(currentManifest.historical_data_modified).toBe(false);
    expect(currentManifest.accepted_evidence).toBe(false);
    expect(currentManifest.automatic_evidence_promotion).toBe(false);
    expect(currentManifest.semantic_completeness_certified).toBe(false);

    const frozen = catalogue.publications.find(item => item.id === catalogue.frozen_empirical_baseline);
    expect(frozen.version).toBe('1.5');
    expect(frozen.edition_status).toBe('frozen_empirical_baseline');
    const base = frozen.snapshot + '/';
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

    const frozenPointer = await page.request.get(prefix + encodeURIComponent('publications/FROZEN_V1.5.md') + '?source=research');
    expect(frozenPointer.ok()).toBeTruthy();
    expect((await frozenPointer.json()).content).toContain('Frozen empirical baseline');

    const historical = JSON.parse((await (await page.request.get(prefix + encodeURIComponent('publications/reader/manifest.json') + '?source=research')).json()).content);
    expect(historical.section_count).toBe(46);
    for (const section of historical.sections) {
      const response = await page.request.get(prefix + encodeURIComponent(`publications/reader/${section.path}`) + '?source=research');
      const descriptor = await response.json();
      expect(descriptor.truncated, section.path).toBe(false);
      expect(descriptor.read_only, section.path).toBe(true);
      expect(descriptor.content, section.path).toContain('Inhaltsuebersicht');
    }

    const write = await page.request.put(`http://127.0.0.1:${port}/api/files/document/` + encodeURIComponent(current[0].entrypoint) + '?source=research', {
      data: { action: 'write', content: 'unauthorized change', expected_sha256: 'invalid' },
    });
    expect(write.status()).toBe(403);
    expect(errors).toEqual([]);
  });
 }
}


for (const port of [4174, 4175]) {
  test(`publication ${port}: imprint/legal subtab exposes identity and incomplete-publication warning`, async ({ page }) => {
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`http://127.0.0.1:${port}/`);

    const response = await page.request.get(`http://127.0.0.1:${port}/api/publication/imprint`);
    expect(response.ok()).toBeTruthy();
    const imprint = await response.json();
    expect(imprint.provider.name).toBe('Thomas Heisig');
    expect(imprint.project.short_name).toBe('MHRN');
    expect(imprint.project.orcid).toContain('0009-0002-9589-1872');
    expect(imprint.read_only).toBe(true);
    expect(imprint.public_internet_ready).toBe(false);
    expect(imprint.missing_required_fields).toEqual(expect.arrayContaining(['postal_address', 'email']));
    expect(JSON.stringify(imprint)).not.toContain('t_heisig@gmx.de');
    expect(JSON.stringify(imprint)).not.toContain('news@thomas-heisig.de');

    await page.evaluate(() => window.MHRNWorkspaceArchitecture?.selectRoute?.('publication', 'imprint'));
    await expect(page.locator('body')).toHaveAttribute('data-current-area', 'publication');
    await expect(page.locator('#publication-imprint-panel')).toBeVisible();
    await expect(page.locator('#publication-imprint-panel')).toContainText('Impressum & Rechtliche Hinweise');
    await expect(page.locator('#publication-imprint-panel')).toContainText('Thomas Heisig');
    await expect(page.locator('#publication-imprint-panel')).toContainText('Wolffsheide 10');
    await expect(page.locator('#publication-imprint-panel')).toContainText('t_heisig@gmx.de');
    await expect(page.locator('#publication-imprint-panel')).toContainText('Hosting-Datenschutz offen');

    await page.evaluate(() => window.MHRNWorkspaceArchitecture?.selectRoute?.('publication', 'simple'));
    await expect(page.locator('#publication-simple-panel')).toBeVisible();
    await expect(page.locator('#publication-simple-panel')).toContainText('MHRN · EINFACH ERKLÄRT');
    await expect(page.locator('#publication-simple-panel')).toContainText('methodischen Forschungsgegenstands');
    await expect(page.locator('#publication-simple-panel')).toContainText('unabhängige externe Replikation');
    await expect(page.locator('#publication-imprint-panel')).toContainText('0009-0002-9589-1872');

    await page.evaluate(() => window.MHRNWorkspaceArchitecture?.selectRoute?.('publication', 'overview'));
    await expect(page.locator('#publication-panel')).toBeVisible();
    await expect(page.locator('#publication-imprint-panel')).toBeHidden();
    expect(errors).toEqual([]);
  });
}
