#!/usr/bin/env python3
"""Read-only eleventh-round planning checks, never dispatches or runs Blender."""
import hashlib
import json
from pathlib import Path
root = Path(__file__).resolve().parent
repo = root.parents[1]
q = json.loads((root / 'queue.json').read_text())
state = json.loads((root / 'state.json').read_text())
assert q['kind'] == 'planning-only-production-backlog-not-executable-runner-manifest'
assert q['round'] == 11
invpath = repo / q['inventory']['path']
assert hashlib.sha256(invpath.read_bytes()).hexdigest() == q['inventory']['sha256']
inv = {a['id']: a for a in json.loads(invpath.read_text())['assets']}
assert len(inv) == 1000
ids = [j['inventory_id'] for j in q['jobs']]
assert len(ids) == len(set(ids)) == 12
assert [b['id'] for b in q['batches']] == ['batch-31', 'batch-32', 'batch-33']
assert all(len(b['asset_ids']) == 4 for b in q['batches'])
assert [i for b in q['batches'] for i in b['asset_ids']] == ids
prior_ids = set()
for name in ['continuous-small-life-20261018', 'continuous-small-life-round02-20261018', 'continuous-small-life-round03-20261018', 'continuous-small-life-round04-20261018', 'continuous-small-life-round05-20261018', 'continuous-small-life-round06-20261018', 'continuous-small-life-round07-20261018', 'continuous-small-life-round08-20261018', 'continuous-small-life-round09-20261018', 'continuous-small-life-round10-20261018']:
    prior = json.loads((repo / 'production' / name / 'queue.json').read_text())
    prior_ids.update(j['inventory_id'] for j in prior['jobs'])
assert len(prior_ids) == 120 and not set(ids) & prior_ids
snapshot = json.loads((root / 'dedup-snapshot.json').read_text())
assert not set(ids) & {j['id'] for j in snapshot['excluded']}
assert all(not r['selected_model_or_named_generator_paths'] for r in snapshot['selected_branch_scan'])
assert set(state['jobs']) == set(ids)
assert len(q['marine_organism_ids']) == 5 and len(q['landform_and_rock_ids']) == 5 and len(q['trace_concept_ids']) == 2
assert len(q['shell_specimen_ids']) == 2 and len(q['whole_organism_ids']) == 3
assert not set(ids) & set(snapshot['current_main_catalog_or_addition_ids'])
for j in q['jobs']:
    i = j['inventory_id']
    assert inv[i]['name'] == j['name']
    assert inv[i]['production_gate'] == j['inventory_gate']
    assert j['catalog_facets'] == {k: inv[i].get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type']}
    assert inv[i]['representation'] == j['representation']
    assert inv[i]['reconstruction_type'] == j['reconstruction_type']
    assert j['maker'] == {'model': 'GPT-6.1 Sol', 'reasoning': 'medium'}
    assert j['reviewer']['model'] == 'GPT-6 Luna' and j['reviewer']['reasoning'] == 'xhigh'
    assert j['budget_intent']['usual_glb_bytes_range'] == [100000, 500000]
    d = repo / j['plan_dir']
    freeze = json.loads((d / 'freeze.json').read_text())
    for name, expected in freeze['files'].items():
        assert hashlib.sha256((d / name).read_bytes()).hexdigest() == expected, (i, name)
    assert hashlib.sha256((root / 'reference-policy.json').read_bytes()).hexdigest() == freeze['shared_policy_sha256']
    assert hashlib.sha256((root / 'profile-policy.json').read_bytes()).hexdigest() == freeze['profile_policy_sha256']
    scope_file = root / (j['batch_id'] + '-QA-SCOPE.json')
    assert hashlib.sha256(scope_file.read_bytes()).hexdigest() == freeze['qa_scope_sha256']
    scope = json.loads(scope_file.read_text())
    assert scope['batch_id'] == j['batch_id'] and scope['expected_source_commit'] is None and scope['ready_for_qa'] is False
    assert set(scope['expected_asset_ids']) == {x['inventory_id'] for x in q['jobs'] if x['batch_id'] == j['batch_id']}
    assert all(x is None for x in scope['expected_glb_sha256_by_asset'].values())
    brief = json.loads((d / 'brief.json').read_text())
    assert brief['review_identity_policy']['prefer_new_context'] is True
    assert brief['publication_authority'] == 'separate' and brief['candidate_validation_profile'] == 'static-stylized-v1'
    refs = json.loads((d / 'references.json').read_text())
    assert {s['id'] for s in refs['sources']} == set(inv[i]['source_ids'])
    assert refs['no_incorporated_third_party_assets'] is True
    assert all(s['use'] == 'consulted-only' and s['incorporated'] is False and s['rights_note'] for s in refs['sources'])
    assert brief['subject']['representation'] == inv[i]['representation']
    assert brief['subject']['reconstruction_type'] == inv[i]['reconstruction_type']
    assert brief['turntable_frames'] == 0 and len(brief['required_views']) == 8
    assert brief['geometry_policy'] == j['geometry_policy']
    for field in ['candidate_dir', 'production_dir', 'release_dir_after_acceptance']:
        assert not Path(j[field]).is_absolute() and '..' not in Path(j[field]).parts
assert all(inv[i]['representation'] == 'fossil-specimen' and inv[i]['reconstruction_type'] == 'specimen' for i in q['shell_specimen_ids'])
assert all(inv[i]['reconstruction_type'] == 'artistic-concept' for i in q['natural_object_ids'])
assert all(inv[i]['reconstruction_type'] == 'whole-organism' for i in q['whole_organism_ids'])
assert all(inv[i]['representation'] == 'trace-concept' for i in q['trace_concept_ids'])
assert all(inv[i]['scale_class'] == 'landscape' for i in ['sea-cave','estuary-basin','wave-cut-platform'])
profile = json.loads((root / 'profile-policy.json').read_text())
assert profile['kind'] == 'planning-profile-policy-not-validator-sidecar'
assert profile['validation_profile'] == 'static-stylized-v1' and profile['rule_version'] == '2026-10-18.1'
for line in (root / 'checksums.sha256').read_text().splitlines():
    expected, name = line.split('  ', 1)
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
print('PASS: 12 real round11 IDs; batches 31–33 x4; prior 120/released/candidate exclusions; original form/habitat scopes, source ledgers, budgets and frozen hashes intact. No work dispatched by this check.')
