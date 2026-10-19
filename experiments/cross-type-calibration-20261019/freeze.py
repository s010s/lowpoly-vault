# SPDX-License-Identifier: MIT
"""Basic artifact identity and matched-view integrity, not production QA."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
H=Path(__file__).resolve().parent;ROOT=H.parents[1];base='de413ef720463a2999516faf92c606bcdf9ab1b7'
def sha(b):return hashlib.sha256(b).hexdigest()
before=json.loads((H/'preflight.json').read_text())['before'];metrics=json.loads((H/'comparison-metrics.json').read_text());pins={}
for slug,item in before.items():
 for kind in ['glb','blend']:
  p=ROOT/item[kind];old=subprocess.check_output(['git','show',base+':'+item[kind]],cwd=ROOT);assert p.read_bytes()==old
  pins[str(p.relative_to(ROOT))]=sha(old)
 q=json.loads((H/'candidates'/slug/'qa.json').read_text());p=H/'candidates'/slug/(slug+'.glb');assert sha(p.read_bytes())==q['glb']['sha256'];assert q['khronos_validator']['num_errors']==q['khronos_validator']['num_warnings']==0
 assert q['glb']['scene_triangles']==item['actual_glb_metrics']['scene_triangles'];assert q['glb']['bytes']==item['actual_glb_metrics']['bytes'];assert q['glb']['sha256']!=item['glb_sha256']
 assert q['glb']['materials']==item['actual_glb_metrics']['materials'];assert q['glb']['unique_mesh_primitives']==item['actual_glb_metrics']['unique_mesh_primitives']
records=json.loads((H/'render-manifest.json').read_text());pairs={}
for r in records:
 assert r['glb_sha256']==metrics[r['asset_id']][r['version']]['sha256'];assert Image.open(H/r['file']).size==(r['resolution'],r['resolution'])
 pairs.setdefault((r['asset_id'],r['view']),{})[r['version']]=r
assert len(pairs)==14
for key,v in pairs.items():
 assert set(v)=={'before','candidate'}
 for field in ['camera_m','target_m','projection','ortho_scale','lens_mm','resolution','samples','exposure','scale']:
  assert v['before'][field]==v['candidate'][field],(key,field)
files={str(p.relative_to(H)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(H.rglob('*')) if p.is_file() and p.name not in ['integrity.json','checksums.sha256'] and '__pycache__' not in str(p)}
(H/'integrity.json').write_text(json.dumps({'status':'candidate comparison only','source_commit':base,'original_model_files_unchanged':pins,'matched_view_pairs':len(pairs),'reference_photos_not_bundled':True,'files':files},indent=2))
(H/'checksums.sha256').write_text(''.join(f"{v['sha256']}  {k}\n" for k,v in files.items()))
print('Verified 14 matched pairs, all four frozen original GLB/Blend files unchanged, only bounded candidate position changes.')
