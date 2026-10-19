#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon Made This / s010s
"""Read-only verification of the additive Batch 51 nominal-scale correction.

This is a mechanical identity/specification-consistency check, not independent
acceptance. It leaves the registered candidate briefs and every gate unchanged.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
BASE = Path('assets/candidates/continuous-small-life-round17-20261018/batch-51')
HANDOFF = Path('production/continuous-small-life-round17-20261018/work/batch-51/QA-HANDOFF.json')
EXPECTED = {'calcite-raft-deposit': 0.32, 'accretionary-lapilli-bed': 0.28}
sys.path.insert(0, str(ROOT / 'scripts'))
from qa_glb import audit_glb
from validate_candidate import check_brief, STATIC_PROFILE


def read(path):
    return json.loads(path.read_text())


def checked(pin):
    path = ROOT / pin['path']
    assert not path.is_symlink() and path.resolve().is_relative_to(ROOT), pin['path']
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == pin['sha256'], pin['path']
    if 'bytes' in pin:
        assert len(raw) == pin['bytes'], pin['path']
    return path


def run_gate(args):
    run = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
    assert not run.stderr, run.stderr
    return {'command': [sys.executable, *args], 'exit_code': run.returncode, 'result': json.loads(run.stdout)}


def main():
    index = read(HERE / 'index.json')
    assert {item['asset_id'] for item in index['items']} == set(EXPECTED)
    preserved = read(checked(index['preservation_manifest']))
    for pin in preserved['files']:
        path = checked(pin)
        oid = hashlib.sha1(b'blob ' + str(path.stat().st_size).encode() + b'\0' + path.read_bytes()).hexdigest()
        assert oid == pin['git_blob_sha1'], pin['path']
    for pin in index['historical_handoff'].values():
        checked(pin)
    handoff = read(ROOT / HANDOFF)
    checked(handoff['specification_correction'])
    old_handoff = read(checked(index['historical_handoff']['QA-HANDOFF.json']))
    assert handoff['source_commit'] == old_handoff['source_commit']
    assert handoff['asset_ids'] == old_handoff['asset_ids']
    items = []
    for item in index['items']:
        aid = item['asset_id']; nominal = EXPECTED[aid]; bundle = ROOT / BASE / aid / 'r002'
        old = read(bundle / 'candidate-brief.json')
        corrected = read(checked(item['supplemental_brief']))
        freeze = read(checked(item['derived_freeze']))
        for pin in [*freeze['current_files'].values(), *freeze['original_evidence'].values()]:
            checked(pin)
        # Only a version label, nominal scalar, and an explicit correction note differ.
        expected_brief = copy.deepcopy(old)
        expected_brief['brief_version'] = 'batch51-concept-plan-v002-specification-correction-v001'
        expected_brief['scale']['meters'] = nominal
        expected_brief['specification_correction'] = freeze['correction']
        assert corrected == expected_brief
        assert freeze['correction']['registered_candidate_changed'] is False
        assert freeze['correction']['formal_candidate_approval'] is False
        assert freeze['correction']['independent_differential_review'] == 'pending'
        assert freeze['historical_premodel_freeze'] is False and freeze['modeling_already_completed'] is True
        candidate = read(bundle / 'candidate.json')
        refs = read(bundle / 'references.json')
        required, criteria = check_brief(corrected, candidate, {v['id'] for v in refs['sources']}, STATIC_PROFILE)
        assert required == set(old['required_stages'])
        assert corrected['criteria'] == old['criteria']
        cfg = read(bundle / 'build-config.json')
        assert corrected['scale']['meters'] == corrected['frozen_construction_plan']['nominal'] == cfg['design']['nominal']
        assert f'{nominal:.2f} m' in (bundle / 'concepts/prompt.txt').read_text()
        audit = audit_glb(bundle / f'{aid}.glb', max_triangles=14000, max_materials=6, max_primitives=30)
        assert not audit['errors']
        metadata = read(checked(item['supplemental_metadata']))
        old_meta = read(bundle / 'metadata.json')
        expected_meta = copy.deepcopy(old_meta)
        for key in ['specification_correction', 'nominal_art_direction', 'corrected_specification_brief',
                    'historical_metadata', 'registered_candidate_brief_unchanged']:
            expected_meta[key] = metadata[key]
        assert metadata == expected_meta
        assert metadata['dimensions'] == audit['bounds_m']['size'] == freeze['correction']['measured_dimensions_glb_xyz_m']
        assert metadata['nominal_art_direction']['meters'] == nominal
        checked(metadata['historical_metadata']); checked(metadata['registered_candidate_brief_unchanged'])
        checked(metadata['corrected_specification_brief'])
        assert candidate['artifacts']['brief']['path'].endswith('/r002/candidate-brief.json')
        assert candidate['artifacts']['brief']['sha256'] == freeze['original_evidence']['candidate-brief.json']['sha256']
        old_item = next(i for i in old_handoff['items'] if i['asset_id'] == aid)
        new_item = next(i for i in handoff['items'] if i['asset_id'] == aid)
        assert new_item['stages'] == old_item['stages'] and new_item['approval'] == old_item['approval']
        for role, pin in old_item['files'].items():
            assert new_item['files'][role] == pin
        items.append({'asset_id': aid, 'nominal_consistency': 'pass', 'corrected_nominal_design_m': nominal,
                      'exact_measured_dimensions_glb_xyz_m': audit['bounds_m']['size'],
                      'corrected_brief_sha256': item['supplemental_brief']['sha256'],
                      'unchanged_registered_candidate_brief_sha256': candidate['artifacts']['brief']['sha256'],
                      'independent_specification_acceptance': 'pending'})
    gates = []
    for item in handoff['items']:
        for pin in item['files'].values():
            checked(pin)
        aid = item['asset_id']; bundle = Path(item['bundle_root'])
        # Every original checksum remains exact, including concepts, renders and reports.
        for line in (ROOT / bundle / 'bundle-files.sha256').read_text().splitlines():
            if not line.strip():
                continue
            digest, rel = line.split(None, 1)
            checked({'path': str(bundle / rel.lstrip('* ')), 'sha256': digest})
        candidate = ['scripts/validate_candidate.py', str(bundle / 'candidate.json'), '--root', '.',
                     '--profile', 'static-stylized-v1', '--profile-contract', str(bundle / 'profile-contract.json'), '--json']
        integrity = run_gate(candidate)
        approved = run_gate([*candidate, '--require-approved'])
        concept = ['scripts/validate_concept_evidence.py', 'concept-evidence.json', '--root', str(bundle)]
        concept_integrity = run_gate(concept)
        complete = run_gate([*concept, '--require-complete'])
        assert integrity['exit_code'] == 0 and integrity['result']['valid'] is True
        assert approved['exit_code'] == 1 and approved['result']['approved_for_brief'] is False
        assert concept_integrity['exit_code'] == 0 and complete['exit_code'] == 1
        assert complete['result']['valid'] is True and complete['result']['evidence_complete'] is False
        assert complete['result']['blockers'] == ['concept_generated_at: unknown; do not reconstruct times from file mtimes']
        assert read(ROOT / bundle / 'concept-evidence.json')['chronology']['concept_generated_at'] is None
        gates.append({'asset_id': aid, 'candidate_integrity': integrity, 'candidate_require_approved': approved,
                      'concept_integrity': concept_integrity, 'concept_require_complete': complete})
    print(json.dumps({'status': 'pass', 'scope': 'Mechanical additive specification consistency and original-byte preservation only',
        'protected_original_file_count': len(preserved['files']), 'items': items, 'gate_replays': gates,
        'independent_differential_review': 'pending', 'formal_candidate_approval': False,
        'concept_evidence_complete': False, 'historical_gate_outcomes_not_relabelled': True}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
