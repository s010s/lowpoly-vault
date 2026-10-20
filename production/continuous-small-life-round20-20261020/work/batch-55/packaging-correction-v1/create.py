#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Add batch-specific packaging records once; refuse to overwrite any output."""
import argparse
import json
from pathlib import Path
import subprocess
from verify import (ROOT, WORK, ASSETS, SUBJECTS, BASELINE, MODEL_SOURCE, SCOPE,
                    POLICY, digest_pin, derive_brief, derive_candidate,
                    audit_original_manifest, create_contract, timestamp, need)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--declared-at', required=True)
    args = parser.parse_args()
    timestamp(args.declared_at, 'declared_at')
    root = ROOT
    targets = [root / ASSETS / asset / (rev + '-packaging-v1') for asset, rev in SUBJECTS.items()]
    need(not any(path.exists() for path in targets), 'a corrected revision already exists; no overwrite')
    need(not (root / WORK / 'index.json').exists(), 'correction index already exists; no overwrite')
    need(not subprocess.check_output(['git', 'diff', '--name-only', BASELINE, '--', *SCOPE], cwd=root),
         'tracked baseline must be byte-identical before creating packaging correction')

    def save(path, value):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('x') as handle:
            handle.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
        return digest_pin(root, path)

    baseline_paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASELINE, '--', *SCOPE], cwd=root).decode().splitlines()
    snapshot = save(WORK + '/preserved-files.json', [digest_pin(root, path) for path in baseline_paths])
    packages = []
    for asset, revision in SUBJECTS.items():
        old_folder = f'{ASSETS}/{asset}/{revision}'
        new_folder = f'{ASSETS}/{asset}/{revision}-packaging-v1'
        old_pin = digest_pin(root, old_folder + '/candidate.json')
        old = json.loads((root / old_pin['path']).read_text())
        brief = json.loads((root / old['artifacts']['brief']['path']).read_text())
        new_brief = save(new_folder + '/brief.json', derive_brief(brief, old['artifacts'], args.declared_at))
        new_candidate = save(new_folder + '/candidate.json', derive_candidate(old, old_pin, new_brief))
        profile = save(new_folder + '/profile-contract.json', create_contract(root, new_candidate['path'], POLICY))
        contract = {
            'schema_version': 1, 'kind': 'additive-packaging-correction',
            'baseline_commit': BASELINE, 'model_source_commit': MODEL_SOURCE,
            'declared_at': args.declared_at,
            'original_candidate': old_pin, 'corrected_candidate': new_candidate,
            'profile_contract': profile,
            'chronology': {'original_brief_frozen_at': brief['frozen_at'],
                          'packaging_declaration_at': args.declared_at,
                          'declaration_is_post_modeling': True,
                          'establishes_concept_first_chronology': False},
            'approval_effect': 'none; all seven stages remain unknown and approval remains pending',
            'historical_evidence_policy': 'Retained at original paths and hashes; not rebound to the new revision or brief hash. Missing logs are not recreated.',
            'historical_checksum_audit': audit_original_manifest(root, old_folder),
        }
        for key, name in [('original_brief', 'brief.json'), ('original_modeling_freeze', 'modeling-freeze.json'),
                          ('original_concept_evidence', 'concept-evidence.json'),
                          ('original_render_manifest', 'proof/render-manifest.json'),
                          ('original_hash_manifest', 'artifact-hashes.json')]:
            contract[key] = digest_pin(root, f'{old_folder}/{name}')
        packages.append(save(new_folder + '/packaging-contract.json', contract))
    save(WORK + '/index.json', {'schema_version': 1, 'kind': 'batch-packaging-correction-index',
         'baseline_commit': BASELINE, 'model_source_commit': MODEL_SOURCE,
         'declared_at': args.declared_at, 'preserved_files': snapshot, 'packages': packages})
    print('Created four additive, pending packaging revisions. No original files were edited.')


if __name__ == '__main__':
    main()
