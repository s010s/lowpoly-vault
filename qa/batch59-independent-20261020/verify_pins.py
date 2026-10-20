from pathlib import Path
import hashlib,json,sys
R=Path('/tmp/lowpoly-batch59-20261020'); OUT=Path('/tmp/lowpoly-round22-qa59')
ids={'erbenochile':'r003','glacial-erratic':'r002','gypsum-cave-flower':'r002','stalactite-group':'r002'}
pins={'erbenochile':'ec7b7fb8e84b2298a17d5ee42f0074ce97aab38eaac98a21579edc6eee59645f','glacial-erratic':'94bdc5b0dddd8a3925d53ded4be6191d4769cc9414d8860d9664a8170010bfcd','gypsum-cave-flower':'8ddaf4c36f2fd0dbe7c3971c27c750e8c41760954a8fb25e9e40b679c24eac2b','stalactite-group':'6e2bf795d94dae162a65dd8cf0924d70e402e28dbb1c17917d622919d608fca7'}
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
res={'commit':'330bc4aa669a1647c632a32622ce4318fd8d1b59','models':{}}
for id,rev in ids.items():
 root=R/'assets/candidates/continuous-small-life-round22-20261020/batch-59'/id/rev
 m={'root':str(root),'glb_sha256':h(root/f'{id}.glb'),'glb_pin_match':h(root/f'{id}.glb')==pins[id]}
 for f in ['candidate.json','brief.json','references.json','profile-contract.json','source-export.report.json','technical.report.json','runtime-parse.report.json','gltf-validator.report.json','candidate-validation.json','concept-evidence.json','concept-validation.json','metrics.json']:
  p=root/f
  if p.exists(): m[f.replace('.json','_sha256')]=h(p)
 mf=json.loads((root/'proof-final/render-manifest-static.json').read_text())
 m['render_manifest_source_glb_sha256']=mf.get('source_glb_sha256') or mf.get('subject',{}).get('glb_sha256')
 m['render_manifest']=str(root/'proof-final/render-manifest-static.json')
 m['frames']=[]
 for fr in mf.get('frames',[]):
  img=root/'proof-final'/fr.get('path','')
  item={'id':fr.get('id'),'view':fr.get('view'),'path':str(img.relative_to(R)) if img.exists() else None,'sha256':fr.get('sha256'),'actual_sha256':h(img) if img.exists() else None,'width':fr.get('width'),'height':fr.get('height'),'status': bool(img.exists() and h(img)==fr.get('sha256') and fr.get('width')==512 and fr.get('height')==512)}
  m['frames'].append(item)
 m['render_manifest_pin_match']=m['render_manifest_source_glb_sha256']==pins[id]
 # inspect rebuilt evidence paths for queue runs separately
 res['models'][id]=m
print(json.dumps(res,indent=2))
(OUT/'pins-and-frames.json').write_text(json.dumps(res,indent=2)+'\n')
