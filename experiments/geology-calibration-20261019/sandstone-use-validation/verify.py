# SPDX-License-Identifier: MIT
"""Placement evidence integrity only. No asset rebuild or full QA."""
from pathlib import Path
import json,hashlib,subprocess
H=Path(__file__).resolve().parent;E=H.parent;ROOT=E.parents[1]
def digest(b):return hashlib.sha256(b).hexdigest()
base='34d8d3f3b46503a0f5d734cc200ebb2c4f2136e0';unchanged={}
# Exact GLB and Blend bytes for both frozen candidates must stay unchanged.
for p in sorted(E.glob('*/*')):
 if p.suffix in ['.glb','.blend']:
  old=subprocess.check_output(['git','show',base+':'+str(p.relative_to(ROOT))],cwd=ROOT)
  assert old==p.read_bytes(),p
  unchanged[str(p.relative_to(E))]=digest(old)
records=json.loads((H/'render-manifest.json').read_text());pairs={}
for r in records:
 # Camera Z is measured from the asset origin, not an inferred point on a slope.
 if 'eye_height_above_ground_m' in r:r['camera_height_above_asset_ground_origin_m']=r.pop('eye_height_above_ground_m')
 p=ROOT/r['source_glb'];assert digest(p.read_bytes())==r['source_glb_sha256']
 pairs.setdefault(r['scenario'],{})[r['version']]=r
assert len(pairs)==2
for pair in pairs.values():
 assert set(pair)=={'before','after'}
 for key in ['camera_m','target_m','lens_mm','projection','asset_translation_m','asset_rotation','asset_scale','resolution','samples','exposure']:
  assert pair['before'][key]==pair['after'][key],key
(H/'render-manifest.json').write_text(json.dumps(records,indent=2))
files={str(p.relative_to(H)):{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(H.iterdir()) if p.is_file() and p.name not in ['integrity.json','checksums.sha256']}
(H/'integrity.json').write_text(json.dumps({'kind':'placement evidence only; no full QA','base_commit':base,'models_unchanged':unchanged,'matched_placement_pairs':len(pairs),'reference_access':'unchanged; maker real-reference pixels unavailable','files':files},indent=2))
(H/'checksums.sha256').write_text(''.join(f"{v['sha256']}  {k}\n" for k,v in files.items()))
print('Verified 2 placement pairs; all 4 candidate GLB/Blend files unchanged.')
