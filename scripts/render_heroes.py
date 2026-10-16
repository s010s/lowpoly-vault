#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Sequential high-sample hero refresh after model authors have finished writing."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--assets-root',type=Path,default=ROOT/'assets'/'prehistoric')
p.add_argument('--blender',default='/usr/bin/blender')
p.add_argument('--samples',type=int,default=256)
p.add_argument('--resolution',type=int,default=1024)
p.add_argument('--expected-count',type=int)
p.add_argument('--slug',action='append',help='Optional explicit slug selection; repeatable')
a=p.parse_args()
files=sorted(a.assets_root.rglob('*.blend'))
if a.slug: files=[f for f in files if f.stem in set(a.slug)]
if not files: p.error('No blend files found')
if a.expected_count is not None and len(files)!=a.expected_count:
    p.error(f'Expected {a.expected_count} blend files, found {len(files)}; wait for model completion')
failed=[]
for index,blend in enumerate(files,1):
    pause_file=ROOT/'qa'/'hero-refinement.pause.json'
    if pause_file.is_file():
        print('Hero refinement paused; unfinished images remain pending.',flush=True)
        raise SystemExit(75)
    print(f'[{index}/{len(files)}] Refining hero: {blend.stem}',flush=True)
    command=[a.blender,'--background',str(blend),'--python-exit-code','1','--python',str(ROOT/'scripts'/'render_hero.py'),
        '--','--samples',str(a.samples),'--resolution',str(a.resolution)]
    result=subprocess.run(command,check=False)
    if result.returncode==75:
        print('Hero refinement paused by request; unfinished images remain pending.',flush=True)
        raise SystemExit(75)
    if result.returncode: failed.append((str(blend),result.returncode))
if failed:
    print('Hero renders failed: '+repr(failed),file=sys.stderr)
    raise SystemExit(1)
print(f'All {len(files)} hero renders finished; inspect the images before marking visual review complete.')
