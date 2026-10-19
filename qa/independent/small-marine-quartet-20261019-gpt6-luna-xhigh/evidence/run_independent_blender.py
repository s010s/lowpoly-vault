#!/usr/bin/env python3
"""Run exact-GLB source/export checks and fresh multi-view imports, recording real elapsed time."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path.cwd()
QA = ROOT / 'qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh/evidence'
INPUTS = json.loads((QA / 'inputs.json').read_text())
BLENDER = '/usr/bin/blender'
RENDER_VIEWS = 'hero,reversehero,front,rear,left,right,top,bottom,clay,clayalt,wire'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def run(label, cmd, log_base):
    started = datetime.now(timezone.utc).isoformat()
    monotonic = time.monotonic()
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    elapsed = time.monotonic() - monotonic
    finished = datetime.now(timezone.utc).isoformat()
    log_base.parent.mkdir(parents=True, exist_ok=True)
    log_base.with_suffix('.stdout.txt').write_text(result.stdout)
    log_base.with_suffix('.stderr.txt').write_text(result.stderr)
    record = {
        'label': label,
        'started_at_utc': started,
        'finished_at_utc': finished,
        'elapsed_wall_seconds_monotonic': round(elapsed, 6),
        'command': cmd,
        'returncode': result.returncode,
        'stdout_log': log_base.with_suffix('.stdout.txt').relative_to(ROOT).as_posix(),
        'stderr_log': log_base.with_suffix('.stderr.txt').relative_to(ROOT).as_posix(),
    }
    (log_base.with_suffix('.timing.json')).write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    if result.returncode != 0:
        raise RuntimeError(f'{label} failed ({result.returncode}); see {record["stderr_log"]}')
    return record


def run_check(label, cmd, log_base, input_paths):
    before = {name: digest(path) for name, path in input_paths.items()}
    record = run(label, cmd, log_base)
    after = {name: digest(path) for name, path in input_paths.items()}
    record['input_sha256_before'] = before
    record['input_sha256_after'] = after
    record['input_paths'] = {name: str(path.relative_to(ROOT)) for name, path in input_paths.items()}
    if before != after:
        raise RuntimeError(f'{label}: frozen input bytes changed')
    log_base.with_suffix('.timing.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    return record


def main():
    started = datetime.now(timezone.utc).isoformat()
    records = {'schema_version': 1, 'kind': 'independent_blender_checks', 'started_at_utc': started,
               'blender': subprocess.check_output([BLENDER, '--version'], text=True).splitlines()[0],
               'commands': []}
    for spec in INPUTS['assets']:
        asset, revision = spec['asset_id'], spec['revision']
        blend, glb = ROOT / spec['blend'], ROOT / spec['glb']
        source_output = QA / 'source-export' / f'{asset}.json'
        cmd = [BLENDER, '--background', '--factory-startup', '--disable-autoexec', '--threads', '2',
               '--python-exit-code', '1', '--python', 'scripts/check_source_export.py', '--',
               '--source', str(blend.relative_to(ROOT)), '--glb', str(glb.relative_to(ROOT)), '--output', str(source_output.relative_to(ROOT))]
        records['commands'].append(run_check(f'{asset}_{revision}_source_export', cmd,
            QA / 'source-export' / f'{asset}', {'blend': blend, 'glb': glb}))
    import_report = QA / 'blender-import-audit.json'
    import_cmd = [BLENDER, '--background', '--factory-startup', '--disable-autoexec', '--threads', '2',
                  '--python-exit-code', '1', '--python', str((QA / 'blender_import_audit.py').relative_to(ROOT)), '--',
                  '--pairs', str((QA / 'inputs.json').relative_to(ROOT)), '--output', str(import_report.relative_to(ROOT))]
    import_inputs = {}
    for spec in INPUTS['assets']:
        import_inputs[f"{spec['asset_id']}_blend"] = ROOT / spec['blend']
        import_inputs[f"{spec['asset_id']}_glb"] = ROOT / spec['glb']
    records['commands'].append(run_check('four_asset_clean_blender_reimport', import_cmd,
        QA / 'blender-import', import_inputs))
    for spec in INPUTS['assets']:
        asset, revision = spec['asset_id'], spec['revision']
        blend, glb = ROOT / spec['blend'], ROOT / spec['glb']
        output = QA / 'renders' / asset
        cmd = [BLENDER, '--background', '--factory-startup', '--disable-autoexec', '--threads', '2',
               '--python-exit-code', '1', '--python', 'scripts/render_candidate_views.py', '--',
               str(glb.relative_to(ROOT)), '--revision', revision,
               '--brief', str((blend.parent / 'brief.json').relative_to(ROOT)),
               '--references', str((blend.parent / 'references.json').relative_to(ROOT)),
               '--output-dir', str(output.relative_to(ROOT)), '--views', RENDER_VIEWS,
               '--turntable-frames', '0', '--resolution', '512', '--samples', '8']
        records['commands'].append(run_check(f'{asset}_{revision}_fresh_exact_glb_multiview_render', cmd,
            QA / 'renders' / f'{asset}-run', {'blend': blend, 'glb': glb}))
    records['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    report_path = QA / 'blender-execution-log.json'
    report_path.write_text(json.dumps(records, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status':'pass','commands':len(records['commands']),'report':str(report_path)},indent=2))


if __name__ == '__main__':
    main()
