import json, hashlib, pathlib, os, time
from PIL import Image
W=pathlib.Path('/workspace/shared/lowpoly-batch75-20261020'); P=W/'production/continuous-small-life-round30-20261020/work/batch-75'; O=pathlib.Path('/workspace/shared/lowpoly-round30-qa75')
cases=[('parvancorina','r001','6d121aa830daae492b81ff6a4fd99dd491f74105c0273ecb034a907de2b4fd35'),('glacial-horn','r002','dc476400091e3a9375de913d3684cceb8a8400ea9a4af18228516899bb5ed92b'),('eruptive-fissure','r003','5c01f576cfdb26179b4002bebc0c27997f41e805cf2fb9d9075b022291f83caf'),('banded-gneiss-outcrop','r003','ead8a0740aae860dce43f982ebb9a0ba72800b976a322c37ea18cef17630e638')]
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def parse_time(s): return time.strptime(s[:19],'%Y-%m-%dT%H:%M:%S')
allref=[]; assets=[]
for id,rev,glb_expected in cases:
 d=P/'assets'/id/rev; brief=json.load(open(d/'brief.json')); candidate=json.load(open(d/'candidate-brief.json')); refs=json.load(open(d/'references.json')); freeze=json.load(open(d/'modeling-freeze.json')); render=json.load(open(d/'proof-final/render-manifest.json')); config=json.load(open(d/'proof-final/render-config.json'))
 hashes={'glb_sha256':sha(d/'model.glb'),'frozen_brief_sha256':sha(d/'brief.json'),'candidate_brief_sha256':sha(d/'candidate-brief.json'),'references_sha256':sha(d/'references.json'),'source_sha256':sha(d/'source.blend'),'generator_sha256':sha(d/'generator.py'),'config_sha256':sha(d/'build-config.json')}
 assert hashes['glb_sha256']==glb_expected
 assert candidate['required_deliverables'] and {r['role']:r['sha256'] for r in candidate['required_deliverables']}=={'source':hashes['source_sha256'],'generator':hashes['generator_sha256'],'config':hashes['config_sha256']}
 assert freeze['files']['brief.json']==hashes['frozen_brief_sha256']
 assert freeze['files']['references.json']==hashes['references_sha256']
 assert freeze['files']['build-config.json']==hashes['config_sha256']
 assert freeze['files']['concept-original.png']==sha(d/'concept-original.png')
 for fname,h in freeze['files'].items():
  p=d/fname
  assert p.is_file() and sha(p)==h,(id,fname,sha(p),h)
 assert render['source_glb_sha256']==glb_expected and render['subject']['glb_sha256']==glb_expected
 assert render['subject']['brief_sha256']==hashes['candidate_brief_sha256']
 assert render['subject']['references_sha256']==hashes['references_sha256']
 assert render['render_config']['sha256']==sha(d/'proof-final/render-config.json')
 assert render['frame_count']==8 and render['width']==512 and render['height']==512
 assert render['target_renderer']=='blender-cycles-cpu'
 assert render['source_unchanged'] is True and render['runtime_qa']=='not_run'
 assert len(render['frames'])==8
 frames=[]
 for f in render['frames']:
  p=d/'proof-final'/f['path']; im=Image.open(p)
  assert im.size==(512,512) and sha(p)==f['sha256'] and os.path.getsize(p)==f['bytes']
  frames.append({'id':f['id'],'sha256':f['sha256'],'width':im.width,'height':im.height,'bytes':f['bytes']})
 for key in ['brief.json','build-config.json','references.json','concept-original.png','concept-prompt.txt','concept-generation.json']:
  assert key in freeze['files']
 adapter=candidate.get('packaging_adapter')
 assert adapter and parse_time(adapter['created_at']) < parse_time(render['created_at']),(id,adapter,render['created_at'])
 # References ledger rights and actual consult-only pixels, verified against stored SHA and kept outside repo.
 refs_rows=[]
 for source in refs['sources']:
  assert source.get('rights_note')
  assert source.get('incorporated') is False
  for im in source.get('consulted_images',[]):
   p=pathlib.Path('/workspace/shared/batch75-consult-only')/im['filename']
   assert p.is_file() and sha(p)==im['sha256'],(id,im['filename'])
   assert not str(p).startswith(str(W))
   row={'asset_id':id,'source_id':source['id'],'filename':im['filename'],'sha256':im['sha256'],'path':str(p),'outside_git_worktree':True}
   refs_rows.append(row); allref.append(row)
 sheet=d/'contact-sheet.png'; sim=Image.open(sheet)
 assert sim.format=='PNG'
 assets.append({'asset_id':id,'revision':rev,'scope':brief['claim_scope'],'freeze_at':freeze['frozen_at'],'freeze_status':freeze['status'],'render_manifest_created_at':render['created_at'],'candidate_packaging_adapter_created_at':adapter['created_at'],'candidate_adapter_precedes_render_manifest':True,'render_subject_bound_exact_glb_candidate_brief_references':True,'candidate_required_source_generator_config_bound':True,'frozen_artifacts_and_hashes_match_freeze_record':True,'source_references_with_rights_and_pixels':refs_rows,'final_views':frames,'contact_sheet':{'path':str(sheet),'sha256':sha(sheet),'bytes':sheet.stat().st_size,'dimensions':[sim.width,sim.height]},'render_target':'Blender Cycles CPU; not hardware/GPU or composed-scene evidence'})
chron=json.load(open(P/'design-freeze-chronology.json'))
result={'checked_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'chronology':chron,'notes':['Provider-internal concept generation timestamps are null and remain unknown; only recorded observed invocation/result times are used.','The render script captures exact GLB/active brief/reference hashes before rendering and aborts if these inputs change during rendering. Render manifests bind the exact final hashes and all 8 PNG hashes. Candidate packaging adapters predate the render manifests.','Consult-only pixels remain outside the Git worktree. Every source ledger entry has an explicit rights_note and declares non-incorporation.'],'assets':assets,'consult_only_images':allref,'all_bindings_verified':True}
json.dump(result,open(O/'binding-evidence.json','w'),indent=2,sort_keys=True)
print('all final GLB/brief/reference identities bound to render manifests; 32 PNG frame hashes and dimensions, four lossless sheets, all frozen artifacts, rights notes, and local consulted pixel hashes verified')
for a in assets: print(a['asset_id'],a['revision'],a['candidate_packaging_adapter_created_at'],'<',a['render_manifest_created_at'],len(a['source_references_with_rights_and_pixels']),'consulted pixels')
