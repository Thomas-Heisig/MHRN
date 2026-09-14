import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

// Import the dependency-free contract by source, independent of package type.
const source = await readFile(new URL("../../src/dashboard/static/frontend/modules/cognition-contract.js", import.meta.url), "utf8");
const { memorySummary, predictionRows, displayValue } = await import(`data:text/javascript;base64,${Buffer.from(source).toString("base64")}`);

test("episode count comes from the summary, not a non-existent episode list", () => {
  assert.equal(memorySummary({ episode_count: 17, controls: { read_enabled: true, write_enabled: false } }).episodeCount, 17);
  assert.equal(memorySummary({ memory: { episode_count: 0 } }).episodeCount, 0);
  assert.equal(memorySummary({}).episodeCount, null);
  assert.equal(memorySummary({ available: false }), null);
});

test("unknown flags do not become false and actual false remains false", () => {
  assert.equal(memorySummary({}).readEnabled, null);
  assert.equal(memorySummary({ controls: { read_enabled: false } }).readEnabled, false);
});

test("canonical prediction field names, bool and zero are preserved", () => {
  const [item] = predictionRows({ predictions: [{ tick: 0, target_tick: 1, predicted_state: { matched: false }, actual_state: { matched: false }, error: 0 }] });
  assert.deepEqual(item.predicted, { matched: false });
  assert.deepEqual(item.actual, { matched: false });
  assert.equal(item.error, 0);
  assert.equal(item.tick, 0);
});

test("unavailable is distinct from an empty list", () => {
  assert.equal(predictionRows({ model: {} }), null);
  assert.deepEqual(predictionRows({ predictions: [] }), []);
  assert.equal(predictionRows({ predictions: [{ error: NaN }] })[0].error, null);
});

test("object state displays as JSON and does not become object Object", () => {
  assert.equal(displayValue({ matched: false }), '{"matched":false}');
  assert.equal(displayValue(0), "0");
  assert.equal(displayValue(false), "false");
  assert.equal(displayValue(null), "\u2014");
});

test("read-disabled and unavailable payloads cannot look like empty successful observations", () => {
  assert.equal(predictionRows({ available: false, predictions: [] }), null);
  assert.equal(predictionRows({ available: true, read_enabled: false, predictions: [] }), null);
  assert.deepEqual(predictionRows({ available: true, read_enabled: true, predictions: [] }), []);
});

test("fieldwise error values and zero coverage remain distinguishable from unavailable", () => {
  const errors = { numeric_absolute: { x: 0 }, categorical_mismatch: { matched: 0 }, coverage: 0 };
  assert.deepEqual(predictionRows({ predictions: [{ error_components: errors }] })[0].errorComponents, errors);
  assert.equal(predictionRows({ predictions: [{}] })[0].errorComponents, null);
});
