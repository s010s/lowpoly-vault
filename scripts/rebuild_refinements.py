#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Record new local rebuilds of the two frozen, accepted structural candidates.

Run from the repository: python3 scripts/rebuild_refinements.py --run-id NAME
Historical missing logs are never replaced. Exported build files stay separate
from immutable release files. Two executions must reproduce accepted semantics.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from qa_glb import read_glb, semantic_digest

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', default='/opt/homebrew/bin/blender')
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    if not args.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in args.run_id):
        parser.error('run-id must contain lowercase letters, numbers, hyphens or underscores')
    run = ROOT / 'qa/refinement-integration/runs' / args.run_id
    run.mkdir(parents=True, exist_ok=False)
    summary = {'kind':'new_local_rebuild', 'historical_log_replacement':False,
               'blender_version':subprocess.check_output([args.blender, '--version'], text=True).splitlines()[0],
               'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'assets':[]}
    for asset, candidate in [('natural-arch','candidate-r002.reviewed.json'), ('fern-cluster','candidate-r006.reviewed.json')]:
        root = ROOT / 'experiments/structural-refinement-2026-10-17/accepted' / asset
        record = json.loads((root / 'review' / candidate).read_text())
        artifacts = record['artifacts']
        original = root / artifacts['glb']['path']
        original_doc, original_bin, _ = read_glb(original)
        expected_semantic = semantic_digest(original_doc, original_bin)
        results = []
        for attempt in [1, 2]:
            folder = run / asset / f'attempt-{attempt}'
            folder.mkdir(parents=True)
            generator = root / artifacts['generator']['path']
            config = root / artifacts['config']['path']
            script = ROOT / 'scripts/rebuild_frozen_blender.py' if asset == 'natural-arch' else generator
            command = [args.blender, '-b', '-t', '2', '--factory-startup', '--python-exit-code', '1', '--python', str(script), '--']
            if asset == 'natural-arch':
                command += ['--generator', str(generator)]
            command += ['--config', str(config), '--output-dir', str(folder / 'outputs')]
            save(folder / 'request.json', {'kind':'new_local_rebuild', 'historical_log_replacement':False,
                 'command':command, 'generator_sha256':digest(generator), 'config_sha256':digest(config),
                 'compatibility_adapter_sha256':digest(script) if asset == 'natural-arch' else None,
                 'accepted_glb_sha256':digest(original), 'expected_semantic_sha256':expected_semantic})
            with (folder / 'stdout.txt').open('w') as stdout, (folder / 'stderr.txt').open('w') as stderr:
                try:
                    process = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr, timeout=180,
                                             env=dict(os.environ, OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2'))
                    result = {'exit_code':process.returncode}
                except subprocess.TimeoutExpired:
                    result = {'exit_code':None, 'error':'180 second timeout'}
            result['ended_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            output = folder / 'outputs' / asset / (asset + '.glb')
            if result['exit_code'] == 0 and output.exists():
                doc, binary, raw = read_glb(output)
                semantic = semantic_digest(doc, binary)
                result.update({'bytes':len(raw), 'glb_sha256':digest(output), 'semantic_sha256':semantic,
                               'matches_accepted_semantics':semantic == expected_semantic,
                               'matches_accepted_bytes':digest(output) == digest(original)})
            save(folder / 'result.json', result)
            results.append(result)
        summary['assets'].append({'id':asset, 'accepted_glb_sha256':digest(original),
                                  'attempts':results, 'new_runs_byte_identical':results[0].get('glb_sha256') == results[1].get('glb_sha256')})
    summary['status'] = 'pass' if all(a['new_runs_byte_identical'] and all(r.get('matches_accepted_semantics') for r in a['attempts']) for a in summary['assets']) else 'fail'
    save(run / 'summary.json', summary)
    print(json.dumps(summary, indent=2))
    return 0 if summary['status'] == 'pass' else 1


if __name__ == '__main__':
    sys.exit(main())
