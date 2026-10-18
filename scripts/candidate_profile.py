#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Emit an explicit static-profile sidecar to stdout; never edits frozen inputs."""
import argparse
import hashlib
import json
from pathlib import Path
from validate_candidate import STATIC_PROFILE, PROFILE_RULE_VERSION, relative_file


def create_contract(root, candidate, policy):
    root = Path(root).resolve()
    def pin(name, label):
        path = relative_file(root, name, label)
        return {'path': path.relative_to(root).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    return {'schema_version': 1, 'validation_profile': STATIC_PROFILE, 'rule_version': PROFILE_RULE_VERSION,
            'candidate': pin(candidate, 'candidate'), 'publication_authority': 'separate',
            'publication_policy': pin(policy, 'publication policy'),
            'rationale': 'Interpret this exact frozen production brief under its explicit zero-turntable/eight-fixed-view contract. Artifact pins supply required source/generator/config roles when the historical brief omits the list. Preserve original authority wording and record candidate/publication separation through the pinned policy. No stage outcome or approval is changed.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--policy', default='production/policies/qa-passed-batch-publication-20261018.json')
    args = parser.parse_args()
    print(json.dumps(create_contract(args.root, args.candidate, args.policy), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
