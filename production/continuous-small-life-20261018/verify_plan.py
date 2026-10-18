#!/usr/bin/env python3
"""Read-only planning integrity checks; never imports bpy or dispatches work."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
repo = root.parents[1]
queue = json.loads((root / 'queue.json').read_text())
state = json.loads((root / 'state.json').read_text())
assert queue['kind'] == 'planning-only-production-backlog-not-executable-runner-manifest'
inventory_path = repo / queue['inventory']['path']
assert hashlib.sha256(inventory_path.read_bytes()).hexdigest() == queue['inventory']['sha256']
inventory = {a['id']: a for a in json.loads(inventory_path.read_text())['assets']}
assert len(inventory) == 1000
jobs = queue['jobs']
ids = [j['inventory_id'] for j in jobs]
assert len(ids) == len(set(ids)) == 12
assert len(queue['batches']) == 3
flat = []
for batch in queue['batches']:
    assert len(batch['asset_ids']) == 4
    flat.extend(batch['asset_ids'])
assert flat == ids
assert set(state['jobs']) == set(ids)
excluded = {x['id'] for x in json.loads((root / 'dedup-snapshot.json').read_text())['excluded']}
assert not set(ids) & excluded
for job in jobs:
    asset = job['inventory_id']
    assert inventory[asset]['name'] == job['name']
    assert job['maker'] == {'model': 'GPT-6.1 Sol', 'reasoning': 'medium'}
    bundle = repo / job['plan_dir']
    freeze = json.loads((bundle / 'freeze.json').read_text())
    assert hashlib.sha256((root / 'reference-gate-policy.json').read_bytes()).hexdigest() == freeze['shared_policy_sha256']
    assert job['budget_intent']['usual_glb_bytes_range'] == [100000, 500000]
    for name, digest in freeze['files'].items():
        assert hashlib.sha256((bundle / name).read_bytes()).hexdigest() == digest, (asset, name)
    for name, digest in freeze['upstream_hashes'].items():
        assert hashlib.sha256((bundle / 'upstream' / name).read_bytes()).hexdigest() == digest
    brief = json.loads((bundle / 'brief.json').read_text())
    assert brief['geometry_policy'] == job['geometry_policy']
    assert brief['texture_policy'] == job['texture_policy']
    assert brief['turntable_frames'] == 0 and len(brief['required_views']) == 8
    for field in ['candidate_dir', 'production_dir', 'release_dir_after_acceptance']:
        assert not Path(job[field]).is_absolute() and '..' not in Path(job[field]).parts
for line in (root / 'checksums.sha256').read_text().splitlines():
    digest, name = line.split('  ', 1)
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
print('PASS: 1000 real inventory entries; 12 unique planned IDs; 3 x 4 batches; exclusions, frozen inputs and static checksums verified. No Blender/QA/release executed.')
