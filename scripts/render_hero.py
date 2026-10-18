# SPDX-License-Identifier: MIT
"""Re-render ONLY hero from an already loaded blend, preserving asset/QA facts.

blender -b assets/.../asset.blend --python-exit-code 1 --python scripts/render_hero.py -- --samples 256
"""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import sys
import tempfile

PAUSE_FILE=Path(__file__).resolve().parents[1]/'qa'/'hero-refinement.pause.json'
if PAUSE_FILE.is_file():
    print('HERO_RENDER_PAUSED: '+PAUSE_FILE.read_text(),flush=True)
    raise SystemExit(75)

sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from asset_common import render_previews

args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--samples',type=int,default=256)
p.add_argument('--resolution',type=int,default=1024)
p.add_argument('--output-dir',help='Defaults to loaded .blend directory')
p.add_argument('--no-update-qa',action='store_true',help='For temporary research renders only')
a=p.parse_args(args)
if a.samples<1 or a.resolution<1: raise ValueError('Positive sample and resolution values are required')
if not bpy.data.filepath: raise RuntimeError('Load an existing .blend before running this script')
source=Path(bpy.data.filepath).resolve()
output=Path(a.output_dir).resolve() if a.output_dir else source.parent
output.mkdir(parents=True,exist_ok=True)
collection=bpy.data.collections.get('EXPORT')
if collection is None: raise RuntimeError('Loaded blend has no EXPORT collection')
qa_path=output/'qa.json'
# Require existing QA for an in-place production update; do not invent the other stages.
if not a.no_update_qa and not qa_path.is_file(): raise RuntimeError('Existing qa.json is required; use --no-update-qa for a separate test output')
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix='.hero-render-',dir=output) as temporary:
    render_previews(collection,temporary,views=('hero',),resolution=a.resolution,samples=a.samples)
    generated=Path(temporary)/'preview-hero.png'
    if not generated.is_file(): raise RuntimeError('Renderer produced no hero PNG')
    png_hash=hashlib.sha256(generated.read_bytes()).hexdigest()
    generated.replace(output/'preview-hero.png')
if hashlib.sha256(source.read_bytes()).hexdigest()!=source_hash: raise RuntimeError('Unexpected source blend modification')
if not a.no_update_qa:
    # Read immediately before updating so unrelated latest results are preserved.
    qa=json.loads(qa_path.read_text())
    previews=qa.setdefault('previews',{})
    previews['status']='refined_hero_pending_review'
    previews['settings_note']='Per-view settings override the original batch settings; hero was refined separately.'
    per_view=previews.setdefault('per_view',{})
    per_view['hero']={'status':'rendered_not_visually_reviewed','file':'preview-hero.png',
        'engine':'Cycles CPU','samples':a.samples,'resolution':a.resolution,'denoising':False,
        'view_transform':'Standard','look':'None','background_srgb':'#E8E4DC',
        'sha256':png_hash,'source_blend_sha256':source_hash,
        'rendered_at':datetime.now(timezone.utc).isoformat()}
    # A dedicated record also survives a separate author's later QA-file rewrite.
    (output/'hero-render.report.json').write_text(json.dumps(per_view['hero'],indent=2,ensure_ascii=False)+'\n')
    temporary_qa=qa_path.with_name('.qa-hero-update.json')
    temporary_qa.write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
    temporary_qa.replace(qa_path)
print(json.dumps({'status':'rendered','hero':str(output/'preview-hero.png'),'samples':a.samples,
                  'resolution':a.resolution,'sha256':png_hash,'source_unchanged':True}))
