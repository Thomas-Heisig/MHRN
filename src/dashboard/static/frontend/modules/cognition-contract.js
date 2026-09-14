/** Shared normalization for the actual cognition API, without invented metrics. */
const record = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const count = (value) => Number.isInteger(value) && value >= 0 ? value : null;

export function memorySummary(payload) {
  if (!record(payload)) return null;
  const value = record(payload.memory) ? payload.memory : payload;
  if (payload.available === false || value.available === false) return null;
  return {
    episodeCount: count(value.episode_count),
    workingCount: count(value.working_count),
    predictionCount: count(value.prediction_count),
    readEnabled: typeof value.controls?.read_enabled === "boolean" ? value.controls.read_enabled : null,
    writeEnabled: typeof value.controls?.write_enabled === "boolean" ? value.controls.write_enabled : null,
    integrityDigest: typeof value.integrity_digest === "string" ? value.integrity_digest : null,
  };
}

export function predictionRows(payload) {
  if (!record(payload) || !Array.isArray(payload.predictions)) return null;
  return payload.predictions.filter(record).slice(-20).reverse().map((row) => ({
    tick: row.tick ?? null,
    targetTick: row.target_tick ?? null,
    predicted: row.predicted_state ?? null,
    actual: row.actual_state ?? null,
    error: typeof row.error === "number" && Number.isFinite(row.error) ? row.error : null,
    uncertainty: typeof row.uncertainty === "number" && Number.isFinite(row.uncertainty) ? row.uncertainty : null,
    source: typeof row.source === "string" ? row.source : null,
  }));
}

export function displayValue(value) {
  if (value === null || value === undefined) return "\u2014";
  return typeof value === "object" ? JSON.stringify(value) : String(value);
}
