#!/usr/bin/env python3
"""Bind the independent review to the frozen commit and each delivered byte file."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path.cwd()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    inputs = json.loads(args.inputs.read_text())
    source = inputs['frozen_source_commit']
    observed = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    if observed != source:
        raise SystemExit(f'Input audit requires source HEAD {source}; current HEAD is {observed}')
    bundle = Path('production/concept-small-marine-quartet-20261019')
    pins = json.loads((bundle / 'bundle-hashes.json').read_text())['files']
    concept_hash = sha(bundle / 'concept-original.png')
    result = {
        'schema_version': 1,
        'kind': 'frozen_input_hash_audit',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'frozen_source_branch': inputs['frozen_source_branch'],
        'frozen_source_commit': source,
        'source_head_verified': observed == source,
        'concept_original': {'path': str(bundle / 'concept-original.png'), 'sha256': concept_hash},
        'producer_chronology_records': {},
        'assets': [],
    }
    for name in ['concept-generation.json', 'events.jsonl', 'environment.json']:
        path = bundle / name
        actual = {'path': path.as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}
        pin = pins.get(name)
        actual['bundle_pin_matches'] = bool(pin and pin['sha256'] == actual['sha256'] and pin['bytes'] == actual['bytes'])
        if not actual['bundle_pin_matches']:
            raise SystemExit(f'Producer chronology/environment pin mismatch: {name}')
        result['producer_chronology_records'][name] = actual
    for spec in inputs['assets']:
        asset_dir = Path('production/concept-small-marine-quartet-20261019') / spec['asset_id'] / spec['revision']
        integration = json.loads((asset_dir / 'integration-metadata.json').read_text())
        concept = json.loads((asset_dir / 'concept-evidence.json').read_text())
        evidence_check = json.loads((asset_dir / 'concept-evidence-check.json').read_text())
        files = {
            'blend': Path(spec['blend']),
            'glb': Path(spec['glb']),
            'brief': asset_dir / 'brief.json',
            'references': asset_dir / 'references.json',
            'generator': bundle / ('generator-r003.py' if spec['asset_id'] == 'tuzoia' and spec['revision'] == 'r003' else 'generator-r002.py'),
            'config': asset_dir / 'build-config.json',
            'build_timing': asset_dir / 'build-timing.json',
            'integration_metadata': asset_dir / 'integration-metadata.json',
            'proof_manifest': asset_dir / 'proof/render-manifest.json',
            'concept_match_frame': asset_dir / 'proof/concept-match.png',
            'concept_evidence': asset_dir / 'concept-evidence.json',
        }
        records = {}
        for role, path in files.items():
            if not path.is_file():
                raise SystemExit(f'Missing required file: {path}')
            rel = path.relative_to(bundle).as_posix() if path.is_relative_to(bundle) else path.as_posix()
            record = {'path': path.as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}
            pin = pins.get(rel)
            if pin:
                record['bundle_pin_sha256'] = pin['sha256']
                record['bundle_pin_bytes'] = pin['bytes']
                record['bundle_pin_matches'] = pin['sha256'] == record['sha256'] and pin['bytes'] == record['bytes']
                if not record['bundle_pin_matches']:
                    raise SystemExit(f'Bundle pin mismatch: {rel}')
            records[role] = record
        glb_hash, blend_hash = records['glb']['sha256'], records['blend']['sha256']
        matches_metadata = (integration['sha256']['glb'] == glb_hash and integration['sha256']['blend'] == blend_hash)
        subject = evidence_check.get('subject', {})
        brief_hash, refs_hash = records['brief']['sha256'], records['references']['sha256']
        subject_matches = (subject.get('glb_sha256') == glb_hash and subject.get('brief_sha256') == brief_hash and subject.get('references_sha256') == refs_hash)
        concept_record = concept['concept']['images'][0]
        concept_matches = concept_record['sha256'] == concept_hash
        manifest_record = concept['render_manifest']
        proof_hash_matches = manifest_record['sha256'] == records['proof_manifest']['sha256']
        selected_run = None
        for run_dir in (bundle / 'build-runs' / 'runs').iterdir():
            summary_path = run_dir / 'summary.json'
            if not summary_path.is_file():
                continue
            run_summary = json.loads(summary_path.read_text())
            for run_result in run_summary.get('results', []):
                if run_result.get('asset_id') == spec['asset_id'] and run_result.get('revision') == spec['revision']:
                    output = run_result.get('outputs', {}).get(f"{spec['asset_id']}.glb", {})
                    if output.get('sha256') == glb_hash:
                        attempt = Path(run_result['attempt_dir'])
                        if not attempt.is_absolute():
                            attempt = ROOT / attempt
                        attempt = attempt.resolve()
                        attempt_rel = attempt.relative_to(ROOT)
                        selected_run = {
                            'run_summary_path': summary_path,
                            'queue_wall_seconds': run_result.get('wall_seconds'),
                            'queue_started_at': run_result.get('started_at'),
                            'queue_finished_at': run_result.get('finished_at'),
                            'attempt_request': attempt_rel / 'request.json',
                            'attempt_result': attempt_rel / 'result.json',
                        }
                        break
            if selected_run:
                break
        if not selected_run:
            raise SystemExit(f'No successful build queue record binds {spec["asset_id"]}/{spec["revision"]} GLB')
        for key in ['run_summary_path', 'attempt_request', 'attempt_result']:
            path = selected_run[key]
            if not path.is_file():
                raise SystemExit(f'Missing selected build record: {path}')
            rel = path.relative_to(bundle).as_posix()
            pin = pins.get(rel)
            rec = {'path': path.as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}
            rec['bundle_pin_matches'] = bool(pin and pin['sha256'] == rec['sha256'] and pin['bytes'] == rec['bytes'])
            if not rec['bundle_pin_matches']:
                raise SystemExit(f'Selected build record pin mismatch: {rel}')
            selected_run[key + '_record'] = rec
            selected_run[key] = path.as_posix()
        timing = json.loads((ROOT / records['build_timing']['path']).read_text())
        selected_run['direct_build_timing'] = {
            'started_at': timing.get('started_at'),
            'finished_at': timing.get('finished_at'),
            'wall_seconds': timing.get('wall_seconds'),
            'stage': timing.get('stage'),
        }
        result['assets'].append({
            'asset_id': spec['asset_id'], 'revision': spec['revision'], 'files': records,
            'integration_metadata_hashes_match': matches_metadata,
            'evidence_sidecar_subject_matches_glb_brief_references': subject_matches,
            'shared_concept_hash_matches_concept_sidecar': concept_matches,
            'proof_manifest_hash_matches_concept_sidecar': proof_hash_matches,
            'selected_build_run': selected_run,
            'maker_concept_evidence_checker_status': evidence_check.get('valid'),
            'maker_concept_evidence_checker_complete': evidence_check.get('evidence_complete'),
            'maker_checker_interpreted_only_as_integrity_not_visual_acceptance': True,
        })
        if not all((matches_metadata, subject_matches, concept_matches, proof_hash_matches)):
            raise SystemExit(f'Frozen subject/hash binding mismatch for {spec["asset_id"]}')
    result['status'] = 'pass'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FileExistsError(args.output)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n')
    print(json.dumps({'status': result['status'], 'assets': len(result['assets']), 'output': str(args.output)}, indent=2))


if __name__ == '__main__':
    main()
