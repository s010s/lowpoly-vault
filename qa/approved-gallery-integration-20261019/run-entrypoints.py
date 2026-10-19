"""Run requested unmodified browser entrypoints against the exact local build."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import shutil
import time

root = Path(os.environ.get('QA_RUN_ROOT', 'qa/approved-gallery-integration-20261019'))
sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
common = dict(os.environ, CHROMIUM_PATH='/usr/bin/chromium', SITE_BASE='/lowpoly-vault/',
              GALLERY_DIR='dist', GITHUB_SHA=sha)
jobs = [
    ('gallery', ['npm', 'run', 'test:gallery:browser'], {}),
    ('browser', ['npm', 'run', 'test:browser'], {}),
    ('scrub', ['npm', 'run', 'test:scrub:browser'], {}),
    ('shared', ['npm', 'run', 'test:preview:browser'], {}),
    ('handoff', ['npm', 'run', 'test:handoff:browser'], {}),
    ('hover', ['npm', 'run', 'test:hover:browser'], {}),
    ('modal', ['npm', 'run', 'test:modal:browser'], {}),
    ('interaction', ['npm', 'run', 'test:interaction:browser'], {}),
    ('scroll', ['npm', 'run', 'test:scroll:browser'], {}),
    ('redesign-models', ['node', 'site/redesign-browser-test.mjs'], {'QA_REVIEW_SCOPE': 'models'}),
    ('small-life', ['node', 'site/small-life-browser-test.mjs'], {}),
    ('round13', ['node', 'site/small-life-browser-test.mjs'],
     {'QA_ADDITION_PACK': 'prehistoric-small-life-round13-20261018'}),
    ('live-local-adapter', ['node', 'qa/approved-gallery-integration-20261019/live-entrypoint-local-adapter.mjs'], {}),
]
results = {'source_sha': sha, 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'environment': {k: common[k] for k in ['CHROMIUM_PATH', 'SITE_BASE', 'GALLERY_DIR', 'GITHUB_SHA']},
           'entrypoints': [], 'not_run': [{'entrypoint': 'site/live-release-browser-test.mjs',
               'reason': 'Hard-coded public Pages origin; this exact integration SHA is not published. Local runtime/browser acceptance is separate from post-deployment acceptance.'}]}
for name, command, extra in jobs:
    output = root / name
    output.mkdir(parents=True, exist_ok=True)
    env = dict(common, QA_OUTPUT_DIR=str(output), **extra)
    print(f'START {name}', flush=True)
    started = time.monotonic()
    with (output / 'entrypoint.txt').open('w') as log:
        try:
            code = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT,
                                  timeout=1200).returncode
        except subprocess.TimeoutExpired:
            code = 124
    row = {'name': name, 'command': command, 'extra_env': extra,
           'seconds': round(time.monotonic() - started, 2), 'exit_code': code,
           'output': str(output)}
    if name == 'browser' and Path('qa/browser-report.json').exists():
        shutil.copyfile('qa/browser-report.json', output / 'browser-report.json')
    results['entrypoints'].append(row)
    (root / 'entrypoints.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'END {name}: {code}', flush=True)
print('All requested local entrypoints attempted.', flush=True)
