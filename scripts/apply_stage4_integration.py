"""Apply the Stage-4 full-stack integration to the feature branch worktree.

This script is intentionally idempotent and is used by the one-shot Stage-4
integration workflow.  It keeps large existing files patchable without
rewriting them manually through the GitHub Contents API.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    (ROOT / path).write_text(content, encoding="utf-8")


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Stage-4 integration anchor missing: {label}")
    return text.replace(old, new, 1)


def patch_embodiment_exports() -> None:
    path = "src/embodiment/__init__.py"
    text = read(path)
    anchor = "from .pipeline import EmbodimentPipeline\n"
    block = """from .specialized_areas import (\n    LATEST_MSBA_DATA,\n    STAGE4_MIN_NEURONS,\n    STAGE4_MIN_SYNAPSES,\n    SpecializedAreaNetwork,\n    SpecializedAreaSpec,\n    default_specialized_areas,\n    reference_probe_suite,\n    specialized_area_contract,\n)\nfrom .pipeline import EmbodimentPipeline\n"""
    text = replace_once(text, anchor, block, label="embodiment specialized import")
    marker = '    "SensorFrame",\n'
    exports = """    "SensorFrame",\n    "LATEST_MSBA_DATA",\n    "STAGE4_MIN_NEURONS",\n    "STAGE4_MIN_SYNAPSES",\n    "SpecializedAreaNetwork",\n    "SpecializedAreaSpec",\n"""
    text = replace_once(text, marker, exports, label="embodiment specialized exports")
    marker = '    "default_modality_profiles",\n'
    exports = """    "default_modality_profiles",\n    "default_specialized_areas",\n    "reference_probe_suite",\n    "specialized_area_contract",\n"""
    text = replace_once(text, marker, exports, label="embodiment specialized functions")
    write(path, text)


def patch_server() -> None:
    path = "src/dashboard/server.py"
    text = read(path)
    import_anchor = "    SensorActivationService,\n)\n"
    import_replacement = (
        "    SensorActivationService,\n    specialized_area_contract,\n)\n"
    )
    text = replace_once(text, import_anchor, import_replacement, label="server import")

    start = text.index("    def _send_neural_symbiosis(self) -> None:\n")
    end = text.index("    @staticmethod\n    def _gateway_maturity", start)
    method = """    def _send_neural_symbiosis(self) -> None:\n        \"\"\"Serve catalog, Stage-4 areas and separately governed gateway runtime.\"\"\"\n        catalog = NeuralSymbiosisCatalog().to_json([])\n        gateway = self.dashboard_server.gateway_runtime.status()\n        specialized = specialized_area_contract()\n        self._send_json(\n            {\n                \"name\": \"Neural Symbiosis\",\n                \"status\": \"implemented_experimental\",\n                \"maturity_level\": self._gateway_maturity(gateway),\n                \"catalog\": catalog,\n                \"specialized_areas\": specialized,\n                \"gateway\": gateway,\n                \"productive_gateway\": {\n                    \"available\": False,\n                    \"reason\": \"experimental_validation_incomplete\",\n                },\n                \"scientific_boundary\": {\n                    \"stage4_engineering_contract\": \"implemented\",\n                    \"dynamic_100k_10m_execution_verified\": False,\n                    \"automatic_evidence_promotion\": False,\n                    \"productive_activation_enabled\": False,\n                },\n            }\n        )\n\n"""
    current = text[start:end]
    if '"specialized_areas": specialized' not in current:
        text = text[:start] + method + text[end:]
    write(path, text)


def patch_timeline() -> None:
    path = "src/dashboard/development_timeline.py"
    text = read(path)
    start = text.index(
        '        StageSpec(\n            4,\n            "specialized_neural_areas",'
    )
    end = text.index(
        '        StageSpec(\n            5,\n            "integrated_artificial_nervous_system",',
        start,
    )
    block = """        StageSpec(
            4,
            "specialized_neural_areas",
            "Spezialisierte neuronale Areale",
            "Areale",
            (
                "Auditive, visuelle und digitale Pfade",
                "modality-specific pathways",
                "unterschiedliche Adapter- und Plastizitätsregeln",
            ),
            {"neurons": "10^5-10^6", "synapses": "10^7-10^8"},
            (
                CriterionSpec(
                    "modality_pathways",
                    "Typed modality pathways",
                    paths=(
                        "src/signal_processing",
                        "src/embodiment/msba.py",
                        "src/embodiment/specialized_areas.py",
                    ),
                    tests=("tests/test_stage4_specialized_neural_areas.py",),
                    verification=(
                        "research/generated/verification/specialized_neural_areas_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "neural_symbiosis_gateway",
                    "Neural Symbiosis gateway",
                    paths=(
                        "src/embodiment/neural_symbiosis.py",
                        "src/embodiment/peripheral_adapters.py",
                        "src/experiments/msba_lab.py",
                    ),
                    tests=(
                        "tests/test_gateway_runtime.py",
                        "tests/test_msba_experiment_runner.py",
                    ),
                    verification=(
                        "research/generated/verification/specialized_neural_areas_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "provenance_bound_treatments",
                    "Provenance-bound treatments and matched controls",
                    paths=(
                        "src/embodiment/msba.py",
                        "src/embodiment/peripheral_adapters.py",
                        "src/research/experiment_recorder.py",
                    ),
                    tests=("tests/test_msba_experiment_runner.py",),
                    verification=(
                        "research/generated/verification/specialized_neural_areas_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "scaled_area_network",
                    "Aggregated Stage-4 area scale contract",
                    paths=("src/embodiment/specialized_areas.py",),
                    tests=("tests/test_stage4_specialized_neural_areas.py",),
                    verification=(
                        "research/generated/verification/specialized_neural_areas_reference_alpha3.json",
                    ),
                ),
            ),
            (
                "src/signal_processing",
                "src/embodiment/msba.py",
                "src/embodiment/neural_symbiosis.py",
                "src/embodiment/peripheral_adapters.py",
                "src/embodiment/specialized_areas.py",
            ),
            (
                "tests/test_msba.py",
                "tests/test_signal_processing_contracts.py",
                "tests/test_gateway_runtime.py",
                "tests/test_msba_experiment_runner.py",
                "tests/test_stage4_specialized_neural_areas.py",
                "tests/test_dashboard_embodiment_routes.py",
            ),
            (
                "src/experiments/msba_lab.py",
                "scripts/run_stage4_reference.py",
                "research/experiments/EXP-BATCH-20260914074039-90",
                "research/experiments/EXP-BATCH-20260914074039-91",
                "research/experiments/EXP-BATCH-20260914074039-92",
                "research/experiments/EXP-BATCH-20260914074039-93",
                "research/experiments/EXP-BATCH-20260914074039-94",
            ),
            (
                "RQ9",
                "RQ11",
                "RQ-MSBA-E01",
                "RQ-MSBA-E02",
                "RQ-MSBA-E03",
                "RQ-MSBA-E04",
                "RQ-MSBA-E05",
            ),
            (
                "The Stage-4 lower-bound scale is an aggregated topology budget; a dynamically executed 100k-neuron/10M-edge multimodal SNN is not claimed.",
                "Peripheral adapters and plasticity remain experiment-only; productive activation stays locked.",
                "Recorded E01-E05 runs are DATA and are not automatically promoted to EVID.",
            ),
            (
                "R4 scientific evidence promotion and independent review remain separate from scoped engineering completion.",
                "Large dynamic multimodal scaling remains a performance/scaling study rather than a Stage-4 contract prerequisite.",
            ),
            (
                "Run independent confirmatory review of E01-E05 before any EVID promotion.",
                "Benchmark dynamically materialized multimodal networks separately at increasing scale.",
            ),
        ),
"""
    text = text[:start] + block + text[end:]
    write(path, text)


def patch_wesen_frontend() -> None:
    path = "src/dashboard/static/wesen-neural-symbiosis.js"
    text = read(path)
    article_anchor = '      <article><header><strong>MSBA pathways</strong><span>3 MODALITIES</span></header><div id="wesen-msba-pathways" class="wesen-symbiosis-list"></div></article>\n'
    article = (
        article_anchor
        + '      <article><header><strong>Stage 4 · Specialized areas</strong><span id="wesen-stage4-scale">ENGINEERING CONTRACT</span></header><div id="wesen-stage4-areas" class="wesen-symbiosis-list"></div></article>\n'
    )
    text = replace_once(text, article_anchor, article, label="Wesen Stage-4 article")
    variable_anchor = '  const topologyCount = document.getElementById("wesen-symbiosis-topology-count");\n'
    variable = (
        variable_anchor
        + '  const stage4Areas = document.getElementById("wesen-stage4-areas");\n  const stage4Scale = document.getElementById("wesen-stage4-scale");\n'
    )
    text = replace_once(
        text, variable_anchor, variable, label="Wesen Stage-4 variables"
    )
    render_anchor = '  msba.innerHTML = MSBA.map(([name, path, coords, plasticity, throttle]) => `<div class="wesen-symbiosis-item"><span class="wesen-symbiosis-dot"></span><div><strong>${escapeHtml(name)} · ${escapeHtml(path)}</strong><small>${escapeHtml(coords)} · ${escapeHtml(plasticity)} · throttle: ${escapeHtml(throttle)}</small></div></div>`).join("");\n'
    render = (
        render_anchor + """  const specialized = lastSymbiosis?.specialized_areas || {};
  const specializedRows = Array.isArray(specialized.areas) ? specialized.areas : [];
  const scale = specialized.topology || {};
  if (stage4Scale) stage4Scale.textContent = `${Number(scale.total_neuron_budget || 0).toLocaleString("de-DE")} N · ${Number(scale.total_synapse_budget || 0).toLocaleString("de-DE")} S · ${scale.dynamic_scale_execution_verified ? "DYNAMIC VERIFIED" : "AGGREGATED"}`;
  if (stage4Areas) stage4Areas.innerHTML = specializedRows.length ? specializedRows.map((area) => `<div class="wesen-symbiosis-item"><span class="wesen-symbiosis-dot"></span><div><strong>${escapeHtml(area.name)} · ${escapeHtml(area.modality)}</strong><small>${Number(area.neuron_budget || 0).toLocaleString("de-DE")} neurons · ${Number(area.synapse_budget || 0).toLocaleString("de-DE")} synapses · ${escapeHtml(area.pathway)} · ${escapeHtml(area.plasticity_rule)}</small></div></div>`).join("") : '<div class="wesen-symbiosis-item"><div><strong>Stage-4 contract unavailable</strong><small>Backend has not published specialized area data.</small></div></div>';
"""
    )
    text = replace_once(text, render_anchor, render, label="Wesen Stage-4 render")
    write(path, text)


def patch_public_msba_frontend() -> None:
    path = "src/dashboard/static/msba/msba.js"
    text = read(path)
    insert_anchor = "function renderGateway(gateway, productiveGateway) {\n"
    function = """function renderSpecializedAreas(specialized) {
  let root = byId("stage4-area-list");
  if (!root) {
    const areaList = byId("area-list");
    const parent = areaList?.parentElement;
    if (parent) {
      root = document.createElement("div");
      root.id = "stage4-area-list";
      root.className = "area-grid";
      const title = document.createElement("h3");
      title.textContent = "Stage 4 · Spezialisierte Areale";
      parent.insertAdjacentElement("afterend", title);
      title.insertAdjacentElement("afterend", root);
    }
  }
  if (!root) return;
  const rows = Array.isArray(specialized?.areas) ? specialized.areas : [];
  const topology = specialized?.topology || {};
  root.innerHTML = rows.map((area) => `<article class="area-card"><header><h3>${escapeHtml(area.name)}</h3><span class="kind">${escapeHtml(area.modality)}</span></header><p>${escapeHtml(area.pathway)} · ${escapeHtml(area.plasticity_rule)}</p><p>${Number(area.neuron_budget || 0).toLocaleString("de-DE")} Neuronen · ${Number(area.synapse_budget || 0).toLocaleString("de-DE")} Synapsen</p></article>`).join("") + `<article class="area-card"><header><h3>Scale boundary</h3><span class="kind">${topology.lower_bound_satisfied ? "LOWER BOUND" : "INCOMPLETE"}</span></header><p>${Number(topology.total_neuron_budget || 0).toLocaleString("de-DE")} Neuronen · ${Number(topology.total_synapse_budget || 0).toLocaleString("de-DE")} Synapsen</p><p>${topology.dynamic_scale_execution_verified ? "dynamic execution verified" : "aggregated topology contract; dynamic scale execution not claimed"}</p></article>`;
}

function renderGateway(gateway, productiveGateway) {
"""
    text = replace_once(
        text, insert_anchor, function, label="public MSBA Stage-4 renderer"
    )
    refresh_anchor = "    renderAreas(symbiosis.catalog || {});\n    renderGateway(symbiosis.gateway || {}, symbiosis.productive_gateway || {});\n"
    refresh = "    renderAreas(symbiosis.catalog || {});\n    renderSpecializedAreas(symbiosis.specialized_areas || {});\n    renderGateway(symbiosis.gateway || {}, symbiosis.productive_gateway || {});\n"
    text = replace_once(text, refresh_anchor, refresh, label="public MSBA refresh")
    write(path, text)


def patch_research_docs() -> None:
    path = "research/README.md"
    text = read(path)
    marker = "<!-- stage4-specialized-areas -->"
    if marker not in text:
        preface = f"""{marker}
## Stage 4 — Spezialisierte neuronale Areale

Der technische Stage-4-Vertrag ist auf `feature/stage4-specialized-neural-areas`
als durchgängiger Audio-/Vision-/Digitalpfad ergänzt. Die E01–E05-Serie vom
14.09.2026 wird als DATA-Grundlage referenziert; eine automatische EVID-Promotion
findet nicht statt. Der 100k-Neuronen-/10M-Synapsen-Wert ist ein aggregierter
Topologievertrag und ausdrücklich kein behaupteter dynamischer Großskalierungslauf.

Details: `research/stage4_specialized_neural_areas.md` und
`research/generated/verification/specialized_neural_areas_reference_alpha3.json`.

"""
        text = preface + text
        write(path, text)

    path = "docs/08-roadmap/TODO.md"
    text = read(path)
    marker = "## 2026-09-14 Stage 4 specialized neural areas"
    if marker not in text:
        section = """## 2026-09-14 Stage 4 specialized neural areas

- [x] Add explicit audio, vision and digital specialized-area contracts with distinct adapter and plasticity rules.
- [x] Add an aggregated 100k-neuron / 10M-synapse lower-bound topology contract without pretending full dynamic execution.
- [x] Connect the existing E01-E05 MSBA runner/data programme to the Stage-4 engineering verification.
- [x] Publish Stage-4 area state through the Neural Symbiosis API and both integrated/public frontend surfaces.
- [x] Add deterministic Stage-4 tests and generated engineering verification.
- [ ] Scientific EVID promotion, independent review and dynamically materialized large-scale multimodal benchmarks remain separate research work.

"""
        anchor = "# MHRN Current TODO\n"
        if anchor not in text:
            raise RuntimeError("TODO anchor missing")
        text = text.replace(anchor, anchor + "\n" + section, 1)
        write(path, text)


def main() -> int:
    patch_embodiment_exports()
    patch_server()
    patch_timeline()
    patch_wesen_frontend()
    patch_public_msba_frontend()
    patch_research_docs()
    print("Stage-4 full-stack integration patch applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
