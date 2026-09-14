"""
Integrationstest: Simuliere den kompletten AIRR-Pipeline-Durchlauf
mit normalize_output -> _validateOutput -> AIAnalysisRecord.create
"""
from src.research_assistant.models import AIAnalysisRecord, ResearchPacket

# 1. ResearchPacket erstellen (minimal)
packet = ResearchPacket(
    experiment_id='EXP-TEST-NORMALIZE-0001',
    research_question={},
    hypotheses=[],
    claims=[],
    manifest={},
    data={},
    evidence=[],
    literature_sources=[],
    protocol={},
    known_limitations=[],
    previous_analyses=[],
    provenance={
        'git_commit': 'test',
        'git_dirty': 'False',
        'source_freeze_sha': 'test',
        'configuration_path': '/dev/null',
        'configuration_sha256': 'test',
        'experiment_manifest_digest': 'test',
        'data_ids': 'TEST',
        'evid_ids': 'TEST',
        'protocol_id': 'TEST',
        'protocol_digest': 'test',
        'data_digest': 'test',
        'evid_digests': '[]',
    },
)

model_info = {
    'provider': 'integration-test',
    'model': 'test-model',
    'model_digest': 'test',
    'quantization': 'unknown',
    'context_length': 'unknown',
    'temperature': 0.0,
    'top_p': 1.0,
    'seed': 'test',
    'backend_version': 'test',
}

# 2. Simuliere Modell-Ausgaben, die Felder auslassen
test_cases = [
    ('nur assessment', {'assessment': 'Das Experiment zeigt klare Ergebnisse.'}),
    ('nur observations', {'observations': ['Spike rate: 10 Hz']}),
    ('leeres Dict', {}),
    ('assessment + confidence aber keine observations', {'assessment': 'Test', 'confidence': 0.85}),
    ('assessment als None', {'assessment': None, 'observations': None, 'confidence': '0.85'}),
]

all_ok = True
for name, output in test_cases:
    try:
        record = AIAnalysisRecord.create(
            role='scientific_writer',
            model=model_info,
            packet=packet,
            output=output,
            prompt='Test prompt',
        )
        print(f'PASS {name}: AIAR={record.analysis_id}')
        print(f'   assessment={str(record.output["assessment"])[:60]}...')
        print(f'   observations={record.output["observations"]}')
        print(f'   confidence={record.output["confidence"]}')
    except Exception as e:
        print(f'FAIL {name}: {e}')
        all_ok = False

print()
print('--- Test: scientific_analyst mit effect_direction ---')
try:
    record = AIAnalysisRecord.create(
        role='scientific_analyst',
        model=model_info,
        packet=packet,
        output={'assessment': 'Analyse'},
        prompt='Test',
    )
    print(f'PASS analyst: effect_direction={record.output["effect_direction"]}')
except Exception as e:
    print(f'FAIL analyst: {e}')
    all_ok = False

print()
print('--- Test: critical_reviewer mit fehlenden Feldern ---')
try:
    record = AIAnalysisRecord.create(
        role='critical_reviewer',
        model=model_info,
        packet=packet,
        output={'assessment': 'Review', 'observations': 'keine liste'},
        prompt='Test',
    )
    print(f'PASS reviewer: observations={record.output["observations"]}')
except Exception as e:
    print(f'FAIL reviewer: {e}')
    all_ok = False

print()
if all_ok:
    print('ALLE INTEGRATIONSTESTS BESTANDEN')
else:
    print('EINIGE TESTS FEHLGESCHLAGEN')
    exit(1)
