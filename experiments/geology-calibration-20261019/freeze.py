# SPDX-License-Identifier: MIT
"""Check comparison framing and bind source files and evidence to exact hashes."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
subprocess.run(['python',str(H/'compose.py')],check=True)
records=json.loads((H/'render-manifest.json').read_text())+json.loads((H/'scene-render-manifest.json').read_text())
metrics=json.loads((H/'comparison-metrics.json').read_text())
pairs={}
for r in records:
 assert sha(H/r['file'])
 assert r['source_glb_sha256']==metrics[r['slug']][r['version']]['sha256']
 assert r['samples']==32
 assert Image.open(H/r['file']).size==(r['resolution'],r['resolution'])
 pairs.setdefault((r['slug'],r['view']),{})[r['version']]=r
for key,v in pairs.items():
 assert set(v)=={'before','after'},key
 for field in ['camera_location','target','ortho_scale','resolution','samples','view_transform','exposure']:
  assert v['before'][field]==v['after'][field],(key,field)
assert len(pairs)==18
files={str(p.relative_to(H)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(H.rglob('*')) if p.is_file() and p.suffix not in ['.pyc'] and p.name not in ['evidence-integrity.json','checksums.sha256'] and '__pycache__' not in str(p)}
(H/'evidence-integrity.json').write_text(json.dumps({'scope':'candidate only','production_commit':'de413ef720463a2999516faf92c606bcdf9ab1b7','matched_pairs':len(pairs),'files':files},indent=2))
(H/'checksums.sha256').write_text(''.join(f"{v['sha256']}  {k}\n" for k,v in files.items()))
deps={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'scripts/asset_common.py',ROOT/'scripts/qa_glb.py',ROOT/'scripts/validate_gltf.cjs',ROOT/'package-lock.json']}
(H/'dependency-hashes.json').write_text(json.dumps(deps,indent=2))
print('Frozen',len(pairs),'matched before/after pairs;',len(files),'files')
