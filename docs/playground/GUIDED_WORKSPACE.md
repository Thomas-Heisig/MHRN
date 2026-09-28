# Guided Playground workspace

The Builder groups its existing controls into six collapsible areas: model and
network, run and stimulus, PAN core, learning and closed loop, application, and
operations. Section labels use A1–F4 instead of a discontinuous global sequence.
All existing API routes and the exploratory evidence boundary remain in place.

## Configuration workflow

- Explore/search the preset cards, inspect their descriptions and compare their
  resolved settings with the current configuration. Expected success is labelled
  as a hypothesis, never a measured result.
- Edit channel amplitude, frequency, phase and optional neuron IDs in a table.
  Changing the channel count resizes the table. Short value lists repeat cyclically,
  exactly as in the runtime; empty vectors use 0 amplitude, 20 Hz and 0 phase.
  Automatic neuron assignment stays in the backend. Once an explicit map is edited,
  empty rows contain no neurons; the automatic button clears that explicit map.
- Correct highlighted fields before starting. Dependency warnings explain shared
  target/action/reward channels, missing sandbox coupling and ineffective inhibition.
  Warnings do not silently rewrite the experiment.
- Undo up to 29 prior form states. Section reset restores the values from the
  initial page profile, not values from the most recently selected preset.
- Export/import the versioned JSON configuration, including the editable form
  values. Browser presets live in localStorage; persisted sessions live on the server.
  YAML parsing and URL-based configuration sharing are not implemented.

CPU execution and CUDA gate diagnostics are distinct actions. CUDA results have
readable status summaries with expandable raw data. Availability never substitutes
for a hardware smoke test. No full-SNN CUDA execution or unsupported logging/seed
modes are implied by the UI. Runtime duration is explicitly unmeasured rather than
estimated without calibration.

The run page identifies the loaded session and exports its result. Sessions and
the component catalogue have search controls and descriptive introductions. The
layout collapses to a single column on small screens; channel tables scroll within
their own container. Existing live-monitor and night-run controls remain reachable
under Operations.

## Verification

`tests/browser/playground-workspace.spec.js` covers channel editing, invalid input,
undo, export/import, preset application, secondary navigation, narrow layouts,
CPU execution and CUDA compilation using the real browser fixture server. It is
picked up by the existing browser CI job.
