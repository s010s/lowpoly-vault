# SPDX-License-Identifier: MIT
"""Local evidence integrity and basic exports, never production approval."""
from pathlib import Path
import json,hashlib,struct,subprocess,shutil
from PIL import Image
H=Path(__file__).resolve().parent;E=H.parent;ROOT=H.parents[2];base='28e86acc6df9cbe3cd69892c5e1b862279c70788'
def sha(b):return hashlib.sha256(b).hexdigest()
old={}
for p in sorted(E.glob('*/*')):
 if p.suffix in ['.glb','.blend']:
  baseline=subprocess.check_output(['git','show',base+':'+str(p.relative_to(ROOT))],cwd=ROOT);assert p.read_bytes()==baseline;old[str(p.relative_to(E))]=sha(baseline)
p=H/'cross-bedded-sandstone/cross-bedded-sandstone.glb';b=p.read_bytes();l=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+l]);assert len(g['images'])==len(g['textures'])==len(g['materials'])==1
q=json.loads((H/'cross-bedded-sandstone/qa.json').read_text());assert q['glb']['sha256']==sha(b);assert q['khronos_validator']['num_errors']==q['khronos_validator']['num_warnings']==0
assert q['glb']['unique_mesh_primitives']==1;assert q['glb']['scene_triangles']==3840;assert len(b)<1000000
assert Image.open(H/'sandstone-original-basecolor-512.png').size==(512,512)
r=json.loads((H/'render-manifest.json').read_text());pairs={}
for entry in r:pairs.setdefault(entry['view'],{})[entry['version']]=entry
assert len(pairs)==5
metrics=json.loads((H/'three-version-metrics.json').read_text())
for view,v in pairs.items():
 assert set(v)=={'production','previous','new'}
 for version,entry in v.items():
  assert entry['source_glb_sha256']==metrics[version]['sha256']
  assert Image.open(H/entry['file']).size==(entry['resolution'],entry['resolution'])
 for key in ['camera_m','target_m','projection','ortho_scale','lens_mm','physical_scale','resolution','samples','exposure']:
  assert v['production'][key]==v['previous'][key]==v['new'][key],(view,key)
shutil.copyfile(H/'views/new-hero.png',H/'cross-bedded-sandstone/preview-hero.png')
files={str(p.relative_to(H)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(H.rglob('*')) if p.is_file() and p.name not in ['integrity.json','checksums.sha256'] and '__pycache__' not in str(p)}
(H/'integrity.json').write_text(json.dumps({'kind':'single-asset textured calibration experiment; no production approval','previous_candidate_commit':base,'old_models_unchanged':old,'reference_photo_not_bundled':True,'matched_three_version_views':5,'new_glb_sha256':sha(b),'files':files},indent=2))
(H/'checksums.sha256').write_text(''.join(f"{v['sha256']}  {k}\n" for k,v in files.items()))
print('Frozen 5 matched three-version views; old four model files unchanged; one 512px image / material / primitive.')
