#!/usr/bin/env python3
"""Read-only third-round planning checks, never dispatches or runs Blender."""
import hashlib
import json
from pathlib import Path
root = Path(__file__).resolve().parent
repo = root.parents[1]
q = json.loads((root / 'queue.json').read_text())
state = json.loads((root / 'state.json').read_text())
assert q['kind'] == 'planning-only-production-backlog-not-executable-runner-manifest'
assert q['round'] == 3
invpath = repo / q['inventory']['path']
assert hashlib.sha256(invpath.read_bytes()).hexdigest() == q['inventory']['sha256']
inv = {a['id']: a for a in json.loads(invpath.read_text())['assets']}
assert len(inv) == 1000
ids = [j['inventory_id'] for j in q['jobs']]
assert len(ids) == len(set(ids)) == 12
assert [b['id'] for b in q['batches']] == ['batch-07', 'batch-08', 'batch-09']
assert all(len(b['asset_ids']) == 4 for b in q['batches'])
assert [i for b in q['batches'] for i in b['asset_ids']] == ids
prior_ids = set()
for name in ['continuous-small-life-20261018', 'continuous-small-life-round02-20261018']:
    prior = json.loads((repo / 'production' / name / 'queue.json').read_text())
    prior_ids.update(j['inventory_id'] for j in prior['jobs'])
assert len(prior_ids) == 24 and not set(ids) & prior_ids
snapshot = json.loads((root / 'dedup-snapshot.json').read_text())
assert not set(ids) & {j['id'] for j in snapshot['excluded']}
assert all(not r['selected_model_or_named_generator_paths'] for r in snapshot['selected_branch_scan'])
assert set(state['jobs']) == set(ids)
assert len(q['true_coral_ids']) == 4 and len(q['sponge_ids']) == 3 and len(q['alga_ids']) == 3 and len(q['small_marine_animal_ids']) == 2
for j in q['jobs']:
    i = j['inventory_id']
    assert inv[i]['name'] == j['name']
    assert inv[i]['production_gate'] == j['inventory_gate']
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
    brief = json.loads((d / 'brief.json').read_text())
    refs = json.loads((d / 'references.json').read_text())
    assert {s['id'] for s in refs['sources']} == set(inv[i]['source_ids'])
    assert brief['subject']['representation'] == inv[i]['representation']
    assert brief['subject']['reconstruction_type'] == inv[i]['reconstruction_type']
    assert brief['turntable_frames'] == 0 and len(brief['required_views']) == 8
    assert brief['geometry_policy'] == j['geometry_policy']
    for field in ['candidate_dir', 'production_dir', 'release_dir_after_acceptance']:
        assert not Path(j[field]).is_absolute() and '..' not in Path(j[field]).parts
for i in q['specimen_only_alga_ids']:
    assert inv[i]['representation'] == 'fossil-specimen' and inv[i]['reconstruction_type'] == 'specimen'
    assert inv[i]['biomes'] == ['marine']
assert inv['halimeda']['reconstruction_type'] == 'whole-organism' and inv['halimeda']['biomes'] == ['marine']
for line in (root / 'checksums.sha256').read_text().splitlines():
    expected, name = line.split('  ', 1)
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
print('PASS: 12 real round03 IDs; batches 07–09 x4; prior 24/released/candidate exclusions; original specimen scopes, source ledgers, budgets and frozen hashes intact. No work dispatched by this check.')
