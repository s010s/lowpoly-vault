#!/usr/bin/env python3
"""Read-only second-round plan validation; no production or network actions."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
repo = root.parents[1]
q = json.loads((root / 'queue.json').read_text())
state = json.loads((root / 'state.json').read_text())
first = json.loads((repo / 'production/continuous-small-life-20261018/queue.json').read_text())
assert q['kind'] == 'planning-only-production-backlog-not-executable-runner-manifest'
assert q['round'] == 2 and q['start_gate']['ci_simplification_confirmed'] is True
# queue.start_gate is historical planning intent, never a live dispatch lock.
# Explicit parent dispatch and current state override stale empty claims.
invpath = repo / q['inventory']['path']
assert hashlib.sha256(invpath.read_bytes()).hexdigest() == q['inventory']['sha256']
inv = {a['id']: a for a in json.loads(invpath.read_text())['assets']}
assert len(inv) == 1000
ids = [j['inventory_id'] for j in q['jobs']]
assert len(ids) == len(set(ids)) == 12
assert set(q['true_coral_ids']) == {'calceola', 'goniophyllum', 'favosites', 'halysites', 'aulopora', 'thamnopora'}
assert not set(q['deferred_asset_ids']) & set(ids)
assert len(q['batches']) == 3
assert [b['id'] for b in q['batches']] == ['batch-04', 'batch-05', 'batch-06']
assert all(len(b['asset_ids']) == 4 for b in q['batches'])
assert [i for b in q['batches'] for i in b['asset_ids']] == ids
assert not set(ids) & {j['inventory_id'] for j in first['jobs']}
snapshot = json.loads((root / 'dedup-snapshot.json').read_text())
assert not set(ids) & {j['id'] for j in snapshot['excluded']}
assert all(not x['selected_model_or_named_generator_paths'] for x in snapshot['selected_branch_scan'])
assert set(state['jobs']) == set(ids)
for j in q['jobs']:
    i = j['inventory_id']
    assert inv[i]['name'] == j['name']
    assert inv[i]['production_gate'] == j['inventory_gate']
    assert j['inventory_gate'] == 'reference-ready' or (i == 'thamnopora' and j['inventory_gate'] == 'needs-specific-reference')
    assert j['maker'] == {'model': 'GPT-6.1 Sol', 'reasoning': 'medium'}
    assert j['reviewer']['model'] == 'GPT-6 Luna' and j['reviewer']['reasoning'] == 'xhigh'
    assert j['budget_intent']['usual_glb_bytes_range'] == [100000, 500000]
    d = repo / j['plan_dir']
    f = json.loads((d / 'freeze.json').read_text())
    for name, expected in f['files'].items():
        assert hashlib.sha256((d / name).read_bytes()).hexdigest() == expected, (i, name)
    assert hashlib.sha256((root / 'reference-policy.json').read_bytes()).hexdigest() == f['shared_policy_sha256']
    brief = json.loads((d / 'brief.json').read_text())
    refs = json.loads((d / 'references.json').read_text())
    assert {s['id'] for s in refs['sources']} == set(inv[i]['source_ids'])
    assert brief['turntable_frames'] == 0 and len(brief['required_views']) == 8
    assert brief['geometry_policy'] == j['geometry_policy']
    for field in ['candidate_dir', 'production_dir', 'release_dir_after_acceptance']:
        assert not Path(j[field]).is_absolute() and '..' not in Path(j[field]).parts
stats = json.loads((root / 'INVENTORY-STATS.json').read_text())
assert stats['total'] == sum(stats['category_counts'].values()) == 1000
assert stats['coral_count'] == len(stats['corals']) == 17
assert len(q['true_coral_ids']) == 6 and set(q['true_coral_ids']) <= {x['id'] for x in stats['corals']}
assert stats['cnidarian_total'] == 22
for line in (root / 'checksums.sha256').read_text().splitlines():
    expected, name = line.split('  ', 1)
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
print('PASS: 12 round-02 real inventory IDs; batches 04–06 x4; no first-round/released/candidate overlap; frozen source scopes, budgets and checksums intact. This check starts no production.')
