"""
Echter E2E-Test: Ollama -> _parse_json_object -> normalize_output -> _validate_output
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.research_assistant.ollama_backend import OllamaBackend, _parse_json_object
from src.research_assistant.models import normalize_output, _validate_output

# Ollama direkt ansprechen
backend = OllamaBackend(
    model="qwen2.5-coder:7b",
    endpoint="http://127.0.0.1:11434/api/generate",
    temperature=0.0,
    top_p=1.0,
    max_tokens=2048,
    timeout=120.0,
)

prompt = """Role: scientific_writer
Interpret only the supplied ResearchPacket. Separate direct observation, derived quantity, statistical inference and interpretation.
Never call an effect significant, statistically robust, causal, confirmed or disproven unless the packet contains an explicit statistical test or a design that supports that exact claim.
Before interpretation, verify semantic consistency between research question, hypothesis, protocol, conditions and measured metrics. If they do not match, state this as the primary methodological finding and do not pretend the experiment answers the registered question.
Do not infer biological meaning from engineering metrics unless their operational definition is supplied. Distinguish deterministic replication from statistically independent samples.
Report exact numerical results whenever available, including n, seeds, ticks, condition-wise values, absolute differences, ratios and timing. Include equations in plain LaTeX strings for every derived metric and define each symbol.
State missing definitions, missing controls, missing variance/statistics, provenance limitations and alternative explanations explicitly.
Do not issue commands, decide evidence, approve claims, or answer a research question with scientific authority.
 For role scientific_writer, produce a detailed publication-style synthesis rather than a short abstract. The assessment must cover: objective; registered RQ and hypothesis; design; data basis; operational definitions; formulas; exact quantitative results; seed-by-seed reproducibility; effect sizes or descriptive ratios only when mathematically justified; spike timing/ISI where present; state-digest interpretation limits; methodological critique; competing explanations; what the run does and does not show; and concrete follow-up experiments.
Use cautious language. A repeated identical deterministic sequence across seeds is reproducibility of the observed output, not evidence of independent replication. If RQ/H and protocol mismatch, label the report as semantically mismatched and explain the correct scope of the experiment.
Return JSON only with assessment (string), observations (array), methodological_concerns (array), alternative_explanations (array), recommended_experiments (array), requested_evidence (array), effect_direction (string), confidence (number 0..1).
ALL fields are required. Observations should contain exact values and formulas where possible.
Packet: {"experiment_id": "EXP-TEST-E2E-0001", "data": {"spike_count": 42, "isi_mean": 3.2}, "provenance": {"git_commit": "test"}}"""

print("🚀 Sende Prompt an Ollama (qwen2.5-coder:1.5b)...")
print(f"   Prompt-Länge: {len(prompt)} Zeichen")
print()

try:
    output, metadata = backend(prompt)
    print(f"✅ Ollama antwortete. Provider: {metadata.get('provider', '?')}")
    print(f"   Model: {metadata.get('model', '?')}")
    print(f"   structured_output_valid: {metadata.get('structured_output_valid', '?')}")
    print(f"   structured_output_repaired: {metadata.get('structured_output_repaired', '?')}")
    print()

    # Normalisieren
    normalized = normalize_output(output)
    print(f"📋 Normalisierte Ausgabe:")
    print(f"   assessment: {str(normalized.get('assessment', 'MISSING'))[:80]}...")
    print(f"   observations: {normalized.get('observations', 'MISSING')}")
    print(f"   methodological_concerns: {normalized.get('methodological_concerns', 'MISSING')}")
    print(f"   alternative_explanations: {normalized.get('alternative_explanations', 'MISSING')}")
    print(f"   recommended_experiments: {normalized.get('recommended_experiments', 'MISSING')}")
    print(f"   requested_evidence: {normalized.get('requested_evidence', 'MISSING')}")
    print(f"   effect_direction: {normalized.get('effect_direction', 'MISSING')}")
    print(f"   confidence: {normalized.get('confidence', 'MISSING')}")
    print()

    # Validieren
    try:
        _validate_output(normalized, 'scientific_writer')
        print("✅ _validateOutput() BESTANDEN")
    except ValueError as e:
        print(f"❌ _validateOutput() FEHLGESCHLAGEN: {e}")

except Exception as e:
    print(f"❌ FEHLER: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
