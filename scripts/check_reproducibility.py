#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compare exact original/rebuilt static GLBs; never execute a generator.

A separately supplied rebuilt file is required. Semantic equality is measured;
this command cannot prove that the supplied generator/config produced either file.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

from qa_glb import audit_glb


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_new_report(path, report):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')


def validate_build_run(request, result, generator_sha256, config_sha256, rebuilt_sha256, output):
    """Check a bounded-queue build request/result binding; records are attestations."""
    if not isinstance(request, dict) or not isinstance(result, dict):
        raise ValueError('Build request/result must be JSON objects')
    identity = request.get('identity')
    if not isinstance(identity, dict) or identity.get('lane') != 'build' or identity.get('runner_schema') != 1:
        raise ValueError('Reproducibility requires a build-lane queue run')
    fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
    if request.get('fingerprint') != fingerprint or result.get('fingerprint') != fingerprint:
        raise ValueError('Build request/result fingerprint mismatch')
    if result.get('schema_version') != 1 or result.get('status') != 'succeeded' or type(result.get('returncode')) is not int or result['returncode'] != 0 or result.get('error') is not None:
        raise ValueError('Build run must have succeeded with returncode 0 and no error')
    inputs = identity.get('inputs', {})
    for key, expected in (('generator', generator_sha256), ('config', config_sha256)):
        value = inputs.get(key)
        if not isinstance(value, dict) or value.get('sha256') != expected or not isinstance(value.get('path'), str):
            raise ValueError(f'Build run does not bind the exact {key} input')
        argv = request.get('argv')
        if not isinstance(argv, list) or not all(isinstance(arg, str) for arg in argv) or not any(arg == value['path'] or arg.endswith('=' + value['path']) for arg in argv):
            raise ValueError(f'Build run argv does not explicitly use its {key} input')
    job = identity.get('job', {})
    if any(not job.get(key) or result.get(key) != job[key] for key in ('asset_id', 'revision', 'job_id')):
        raise ValueError('Build result asset/revision/job differs from request')
    if not isinstance(output, str) or not output or Path(output).is_absolute() or '..' in Path(output).parts:
        raise ValueError('Build output must be a safe relative output name')
    exported = result.get('outputs', {}).get(output)
    if not isinstance(exported, dict) or exported.get('sha256') != rebuilt_sha256 or type(exported.get('bytes')) is not int or exported['bytes'] <= 0:
        raise ValueError('Build result does not bind the rebuilt GLB output')
    return fingerprint


def compare_rebuild(glb, rebuilt_glb, generator, config, build_request=None, build_result=None, rebuilt_output=None, root=None):
    paths = {key: Path(value).resolve() for key, value in
             (('glb', glb), ('rebuilt_glb', rebuilt_glb), ('generator', generator), ('config', config))}
    report = {'schema_version': 1, 'check': 'reproducibility', 'status': 'fail', 'errors': [], 'warnings': [],
              'created_at': datetime.now(timezone.utc).isoformat(), 'generator_executed': False,
              'limitations': 'Measures semantic equality. Successful queue records bind declared build execution and output, but are attestations rather than cryptographic proof of correct execution. This checker never executes generators or establishes artistic/factual quality.'}
    try:
        for key, path in paths.items():
            if not path.is_file() or path.stat().st_size == 0:
                raise ValueError(f'{key}: nonempty input file required')
            report[key + '_path'] = str(path)
            report[key + '_sha256'] = file_hash(path)
        if paths['glb'].samefile(paths['rebuilt_glb']):
            raise ValueError('A distinct separately rebuilt GLB is required; same file/hardlink is not a rebuild comparison')
        audits = {}
        for name in ('glb', 'rebuilt_glb'):
            audit = audit_glb(paths[name], max_triangles=10**9, max_materials=10**6, max_primitives=10**6)
            audits[name] = audit
            report['errors'].extend(f'{name}: {error}' for error in audit['errors'])
            report['warnings'].extend(f'{name}: {warning}' for warning in audit['warnings'])
        report['semantic_sha256'] = audits['glb'].get('semantic_sha256')
        report['rebuilt_semantic_sha256'] = audits['rebuilt_glb'].get('semantic_sha256')
        report['byte_identical'] = report['glb_sha256'] == report['rebuilt_glb_sha256']
        report['semantic_match'] = bool(report['semantic_sha256'] and
                                        report['semantic_sha256'] == report['rebuilt_semantic_sha256'])
        if not report['semantic_match']:
            report['errors'].append('Original and rebuilt decoded geometry/material/scene semantic digests differ or cannot be established')
        for key, path in paths.items():
            if file_hash(path) != report[key + '_sha256']:
                report['errors'].append(f'{key}: input changed during comparison')
        if not report['errors']:
            if build_request is None or build_result is None or rebuilt_output is None:
                report['status'] = 'unknown'
                report['provenance_status'] = 'missing_successful_build_run'
                report['warnings'].append('Semantic equality only: a separately hashed successful build request/result is required for reproducibility pass.')
            else:
                from validate_candidate import json_bytes
                base = Path(root or Path.cwd()).resolve()
                request_path, result_path = Path(build_request).resolve(), Path(build_result).resolve()
                request, result = json_bytes(request_path.read_bytes(), 'build request'), json_bytes(result_path.read_bytes(), 'build result')
                fingerprint = validate_build_run(request, result, report['generator_sha256'], report['config_sha256'],
                                                 report['rebuilt_glb_sha256'], rebuilt_output)
                report['build_run'] = {'request': {'path': request_path.relative_to(base).as_posix(), 'sha256': file_hash(request_path)},
                                       'result': {'path': result_path.relative_to(base).as_posix(), 'sha256': file_hash(result_path)},
                                       'output': rebuilt_output}
                report['build_fingerprint'] = fingerprint
                report['provenance_status'] = 'bound_successful_build_run'
                report['status'] = 'pass_with_warnings' if report['warnings'] else 'pass'
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report['errors'].append(str(exc))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--glb', required=True, type=Path)
    parser.add_argument('--rebuilt-glb', required=True, type=Path)
    parser.add_argument('--generator', required=True, type=Path)
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--build-request', type=Path, help='successful bounded-queue request.json')
    parser.add_argument('--build-result', type=Path, help='matching bounded-queue result.json')
    parser.add_argument('--rebuilt-output', help='rebuilt GLB name under queue outputs, e.g. model.glb')
    parser.add_argument('--root', type=Path, default=Path.cwd(), help='root for recorded build evidence paths')
    parser.add_argument('--output', required=True, type=Path, help='new report path; existing evidence is never overwritten')
    args = parser.parse_args()
    result = compare_rebuild(args.glb, args.rebuilt_glb, args.generator, args.config, args.build_request, args.build_result, args.rebuilt_output, args.root)
    try:
        write_new_report(args.output, result)
    except OSError as exc:
        parser.exit(1, f'Report not written: {exc}\n')
    print(json.dumps(result, indent=2, allow_nan=False))
    return 1 if result['errors'] else 2 if result['status'] == 'unknown' else 0


if __name__ == '__main__':
    sys.exit(main())
