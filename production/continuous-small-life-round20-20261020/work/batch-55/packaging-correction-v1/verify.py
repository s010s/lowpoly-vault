#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only batch 55 packaging audit. Does not alter the candidate/release gate."""
import argparse
import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
from candidate_profile import create_contract
from validate_candidate import (STATIC_PROFILE, checked_file, json_bytes,
                                need, relative_file, timestamp, validate_candidate)
from validate_concept_evidence import validate as validate_concept

BASELINE = '89f6086b5d6411b70a7d42c8f5d7aff69b68f7d5'
MODEL_SOURCE = '1e43f9e2c79b6d2465d8eadf2169355cba3690c7'
ROUND = 'continuous-small-life-round20-20261020'
ASSETS = f'assets/candidates/{ROUND}/batch-55'
WORK = f'production/{ROUND}/work/batch-55/packaging-correction-v1'
POLICY = 'production/policies/qa-passed-batch-publication-20261018.json'
SUBJECTS = {'vermicularia': 'r001', 'weichselia': 'r001', 'ventifact': 'r001',
            'pentichnus-deep-dwelling-trace': 'r002'}
MISSING = {'evidence/khronos.log', 'evidence/reproducibility-1.log',
           'evidence/reproducibility-2.log', 'evidence/source-export.log',
           'evidence/source-metrics.log'}
SCOPE = [f'assets/candidates/{ROUND}', f'production/{ROUND}',
         'scripts', 'schemas', POLICY, 'docs/candidate-profile-compatibility.zh-CN.md']
NEW_BLOCKERS = [
    {'id': 'historical-packaging-logs-missing', 'severity': 'required', 'status': 'open',
     'description': 'Five log files named by the original artifact-hashes.json were absent from the original model-source commit. They remain absent; no historical logs were synthesized. See packaging-contract.json.'},
    {'id': 'packaging-revision-review-pending', 'severity': 'required', 'status': 'open',
     'description': 'This later packaging-only revision changes the brief hash and review subject. Historical evidence and independent QA are not rebound or treated as approval of this new subject.'},
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(root, pin, label):
    return json_bytes(checked_file(root, pin, label)[1], label)


def digest_pin(root, path):
    return {'path': path, 'sha256': sha((root / path).read_bytes())}


def audit_original_manifest(root, folder):
    original = json_bytes((root / folder / 'artifact-hashes.json').read_bytes(), 'original hash manifest')
    present, missing = [], []
    for relative, expected in sorted(original.items()):
        pin = {'path': f'{folder}/{relative}', 'sha256': expected}
        if (root / pin['path']).exists():
            checked_file(root, pin, 'original checksum entry')
            present.append(pin)
        else:
            missing.append(pin)
    return {'present_entries_verified': len(present), 'missing_entries': missing}


def derive_brief(original, artifacts, created_at):
    result = copy.deepcopy(original)
    result['brief_version'] += '-packaging-v1'
    result['frozen_at'] = created_at
    result['required_deliverables'] = [{'role': role, **artifacts[role]}
                                       for role in ('source', 'generator', 'config')]
    return result


def derive_candidate(original, original_pin, new_brief):
    result = copy.deepcopy(original)
    result['revision'] += '-packaging-v1'
    result['artifacts']['brief'] = new_brief
    result['supersedes'] = {**original_pin, 'revision': original['revision']}
    result['blockers'] += copy.deepcopy(NEW_BLOCKERS)
    return result


def verify_package(root, contract):
    """Check one additive record and invoke unchanged official validators."""
    need(contract['schema_version'] == 1 and contract['kind'] == 'additive-packaging-correction', 'packaging contract version')
    need(contract['baseline_commit'] == BASELINE and contract['model_source_commit'] == MODEL_SOURCE, 'packaging baseline changed')
    created = contract['declared_at']
    timestamp(created, 'packaging declared_at')
    old = read(root, contract['original_candidate'], 'original candidate')
    need(SUBJECTS.get(old['asset_id']) == old['revision'], 'unexpected original subject')
    need(old['approval'] == {'status': 'pending'} and old['evidence'] == [] and
         all(stage['status'] == 'unknown' for stage in old['stages'].values()),
         'only pending original records may use this packaging-only correction')
    old_brief = read(root, old['artifacts']['brief'], 'original brief')
    need(old_brief['required_deliverables'] == [], 'original declaration was not explicitly empty')
    need(datetime.fromisoformat(created) > datetime.fromisoformat(old_brief['frozen_at']),
         'packaging declaration must be later than original freeze')
    new = read(root, contract['corrected_candidate'], 'corrected candidate')
    new_brief = read(root, new['artifacts']['brief'], 'corrected brief')
    need(new_brief == derive_brief(old_brief, old['artifacts'], created),
         'corrected brief changed beyond declaration/version/current freeze timestamp')
    need(new == derive_candidate(old, contract['original_candidate'], new['artifacts']['brief']),
         'corrected candidate changed beyond additive packaging revision')
    expected_folder = f"{ASSETS}/{old['asset_id']}/{old['revision']}-packaging-v1"
    need(contract['corrected_candidate']['path'] == expected_folder + '/candidate.json' and
         new['artifacts']['brief']['path'] == expected_folder + '/brief.json',
         'corrected records must use their own versioned directory')
    sidecar = read(root, contract['profile_contract'], 'profile contract')
    need(sidecar == create_contract(root, contract['corrected_candidate']['path'], POLICY),
         'profile sidecar must match unchanged official generator')
    for role, pin in old['artifacts'].items():
        checked_file(root, pin, f'original artifact {role}')
        if role != 'brief':
            need(new['artifacts'][role] == pin, 'non-brief artifact pin changed')
    old_folder = str(Path(contract['original_candidate']['path']).parent)
    audit = audit_original_manifest(root, old_folder)
    need(audit == contract['historical_checksum_audit'], 'historical missing/present inventory changed')
    need({str(Path(p['path']).relative_to(old_folder)) for p in audit['missing_entries']} == MISSING,
         'missing historical log set changed; do not reconstruct it')
    need(contract['chronology'] == {
        'original_brief_frozen_at': old_brief['frozen_at'],
        'packaging_declaration_at': created,
        'declaration_is_post_modeling': True,
        'establishes_concept_first_chronology': False,
    }, 'packaging chronology claim changed')
    need(contract['approval_effect'] == 'none; all seven stages remain unknown and approval remains pending',
         'packaging approval effect changed')
    need(contract['historical_evidence_policy'] == 'Retained at original paths and hashes; not rebound to the new revision or brief hash. Missing logs are not recreated.',
         'historical evidence policy changed')
    for key, name in [('original_brief', 'brief.json'), ('original_modeling_freeze', 'modeling-freeze.json'),
                      ('original_concept_evidence', 'concept-evidence.json'),
                      ('original_render_manifest', 'proof/render-manifest.json'),
                      ('original_hash_manifest', 'artifact-hashes.json')]:
        need(contract[key] == digest_pin(root, f'{old_folder}/{name}'), f'{key} binding changed')
    original_result = validate_candidate(contract['original_candidate']['path'], root,
        validation_profile=STATIC_PROFILE, profile_contract=f'{old_folder}/profile-contract.json')
    need(not original_result['valid'] and original_result['errors'] ==
         ['production: frozen source/generator/config required_deliverables missing'],
         'original candidate failure must remain visible')
    corrected_result = validate_candidate(contract['corrected_candidate']['path'], root,
        previous=contract['original_candidate']['path'], validation_profile=STATIC_PROFILE,
        profile_contract=contract['profile_contract']['path'])
    need(corrected_result['valid'] and not corrected_result['approved_for_brief'],
         'corrected candidate must be structurally valid but not approved')
    need(corrected_result['legacy_result']['errors'] == ['brief.turntable_frames: integer >= 2 required'],
         'legacy zero-turntable rejection changed')
    # Original concept records deliberately use bundle-relative paths.
    concept = validate_concept('concept-evidence.json', root / old_folder)
    need(concept['valid'] and not concept['evidence_complete'], 'historical concept integrity/completeness changed')
    return {'asset_id': old['asset_id'], 'revision': new['revision'],
            'original_candidate': original_result, 'corrected_candidate': corrected_result,
            'original_concept_integrity_recheck': concept, 'historical_checksum_audit': audit}


def verify(root, index):
    root = Path(root).resolve()
    need(index['schema_version'] == 1 and index['kind'] == 'batch-packaging-correction-index', 'index version changed')
    need(index['baseline_commit'] == BASELINE and index['model_source_commit'] == MODEL_SOURCE, 'index baseline changed')
    snapshot = read(root, index['preserved_files'], 'preserved files')
    tree = subprocess.check_output(['git', 'ls-tree', '-r', '-z', BASELINE, '--', *SCOPE], cwd=root)
    original_tree = {entry.split(b'\t', 1)[1].decode(): entry.split()[2].decode()
                     for entry in tree.split(b'\0') if entry}
    need(len(original_tree) == len(snapshot) and set(original_tree) == {item['path'] for item in snapshot},
         'preservation snapshot coverage mismatch')
    for pin in snapshot:
        # A baseline may include an empty __init__ or log. This is byte
        # preservation, not acceptance of an empty evidence/artifact file.
        raw = relative_file(root, pin['path'], 'preserved original file').read_bytes()
        need(sha(raw) == pin['sha256'], 'preserved original file checksum mismatch')
        git_sha = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
        need(git_sha == original_tree[pin['path']], 'original bytes differ from baseline Git object')
    contracts = [read(root, pin, 'packaging contract') for pin in index['packages']]
    need(all(contract['declared_at'] == index['declared_at'] for contract in contracts), 'index declaration time mismatch')
    results = [verify_package(root, contract) for contract in contracts]
    need(len(results) == 4 and {item['asset_id'] for item in results} == set(SUBJECTS), 'four exact subjects required')
    return {'schema_version': 1, 'kind': 'current-packaging-verification',
            'packaging_checks_pass': True, 'approved_for_brief': False,
            'baseline_commit': BASELINE, 'model_source_commit': MODEL_SOURCE,
            'preserved_baseline_file_count': len(snapshot),
            'all_original_bytes_git_blob_identical': True,
            'historical_missing_log_count': sum(len(r['historical_checksum_audit']['missing_entries']) for r in results),
            'current_checks': 'New read-only file/hash/GLB/candidate/concept integrity checks only. No modeling, rebuild, image rendering, visual review, GPU/scene run, or acceptance is claimed.',
            'candidates': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--checked-at', required=True, help='Actual current UTC time from the coordinator clock, not a historical modeling time')
    args = parser.parse_args()
    timestamp(args.checked_at, 'checked_at')
    index = json_bytes((args.root / WORK / 'index.json').read_bytes(), 'packaging index')
    result = verify(args.root, index)
    result['checked_at'] = args.checked_at
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
