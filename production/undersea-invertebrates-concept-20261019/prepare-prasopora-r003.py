from pathlib import Path
import json,shutil,hashlib
R=Path.cwd();B=R/'production/undersea-invertebrates-concept-20261019';A=R/'assets/candidates/undersea-invertebrates-concept-20261019';d=A/'prasopora/r003';old=A/'prasopora/r002';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ats=[p.parent for p in (B/'repair-runs/build/prasopora/r003/underside-repair').glob('*/*/result.json') if json.loads(p.read_text())['status']=='succeeded'];at=ats[0]
for p in (at/'outputs/prasopora').iterdir():shutil.copy2(p,d/p.name)
m=json.loads((d/'metadata.json').read_text());m.update(glb=str((d/'prasopora.glb').relative_to(R)),blend=str((d/'prasopora.blend').relative_to(R)),preview=str((d/'proof/hero.png').relative_to(R)));(d/'metadata.json').write_text(json.dumps(m,indent=2)+'\n')
b=json.loads((old/'brief.json').read_text());b['brief_version']='r003'
b['required_deliverables']=[{'role':role,'path':str((d/f).relative_to(R)),'sha256':H(d/f)} for role,f in [('source','prasopora.blend'),('generator','generator.py'),('config','build-config.json')]];b['concept_interpretation']={'path':str((d/'brief.md').relative_to(R)),'sha256':H(d/'brief.md')};(d/'brief.json').write_text(json.dumps(b,indent=2)+'\n')
for name,out in [('final-render-jobs','prasopora-final-render-jobs'),('rebuild-jobs','prasopora-rebuild-jobs'),('source-jobs','prasopora-source-jobs')]:
 j=json.loads((B/(name+'.json')).read_text());j['jobs']=[q for q in j['jobs'] if q['asset_id']=='prasopora']
 for q in j['jobs']:q['revision']='r003';q['inputs']={k:v.replace('/r002/','/r003/') for k,v in q['inputs'].items()};q['argv']=['r003' if x=='r002' else x for x in q['argv']]
 (B/(out+'.json')).write_text(json.dumps(j,indent=2)+'\n')
cur=json.loads((B/'current-revisions.json').read_text());cur['prasopora']='r003';(B/'current-revisions.json').write_text(json.dumps(cur,indent=2)+'\n')
