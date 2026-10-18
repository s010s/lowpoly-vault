# SPDX-License-Identifier: MIT
"""Integrity checker for this batch's fixed-eight practical candidate profile."""
from pathlib import Path
import sys,json,hashlib
from PIL import Image
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').is_file());BASE=ROOT/'assets/candidates/continuous-small-life-20261018/batch-02/r001'
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for s in ['longipteryx','urasterella','alienopterus','aglaophyton']:
 p=BASE/s;c=json.loads((p/'candidate.json').read_text());q=json.loads((p/'qa.json').read_text());m=json.loads((p/'metadata.json').read_text());errors=[]
 for name,r in c['files'].items():
  f=p/name
  if not f.is_file() or f.stat().st_size!=r['bytes'] or hashfile(f)!=r['sha256']:errors.append('file integrity: '+name)
 for name in ['generator','helper','checker']:
  f=ROOT/c['generator'] if name=='generator' else (ROOT/c['generator']).parent/'lib'/('asset_common.py' if name=='helper' else 'qa_glb.py')
  if hashfile(f)!=c[name+'_sha256']:errors.append(name+' hash mismatch')
 for name,f in [('brief','brief.json'),('config','build-config.json'),('references','references.json')]:
  if hashfile(p/f)!=c[name+'_sha256']:errors.append(name+' hash mismatch')
 sha=hashfile(p/(s+'.glb'))
 if sha!=c['artifact']['sha256'] or sha!=m['sha256']['glb'] or hashfile(p/(s+'.blend'))!=m['sha256']['blend']:errors.append('artifact/metadata hash mismatch')
 if q['source']['errors'] or q['glb']['errors']:errors.append('project audit errors')
 if q['khronos_validator']['status']!='pass':errors.append('Khronos not pass')
 if q['glb']['bytes']>1000000 or q['glb']['scene_triangles']>14000:errors.append('hard budget exceeded')
 for name in ['source-roundtrip.report.json','reproducibility.report.json','runtime/report.json']:
  r=json.loads((p/name).read_text())
  if r['status']!='pass':errors.append(name+' not pass')
  bound=r.get('glb_sha256',r.get('original_sha256'))
  if bound!=sha:errors.append(name+' stale')
 for v in ['hero','reversehero','front','side','rear','top','clay','silhouette']:
  im=Image.open(p/('preview-'+v+'.png'));im.verify()
 im=Image.open(p/'preview-hero.png').convert('RGBA')
 if im.getchannel('A').getextrema()!=(0,255):errors.append('hero lacks mixed transparent and opaque pixels')
 if Path(m['glb']).is_absolute() or Path(m['blend']).is_absolute():errors.append('metadata paths are not portable')
 if '--require-approved' in sys.argv:errors.append('Independent QA pending; maker cannot approve')
 results.append({'asset_id':s,'status':'fail' if errors else 'pass','errors':errors,'glb_sha256':sha,'scope':'candidate integrity and maker technical evidence only; independent acceptance pending'})
report={'status':'fail' if any(r['errors'] for r in results) else 'pass','results':results};print(json.dumps(report,indent=2));sys.exit(report['status']=='fail')
