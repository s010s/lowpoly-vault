import sys,json,hashlib,struct,math,os
from pathlib import Path
sys.path.insert(0,'/tmp/lowpoly-batch62-20261020/scripts')
from qa_glb import read_glb,accessor_values,audit_glb
ROOT=Path('/tmp/lowpoly-batch62-20261020')
OUT=Path('/workspace/shared/lowpoly-round24-qa62')
B='assets/candidates/continuous-small-life-round24-20261020/batch-62'
finals=[('dinomischus','r002'),('star-dune','r002'),('slot-canyon','r001'),('flowstone-cascade','r002')]
handoff=json.load(open(ROOT/'production/continuous-small-life-round24-20261020/work/batch-62/handoff.json'))
assets={x['asset_id']:x for x in json.load(open(ROOT/'production/continuous-small-life-round24-20261020/work/batch-62/handoff-assets.json'))}
sel={x['asset_id']:x for x in handoff['final_selection']}
results=[]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def file_entry(root,path): return {'path':str(path.relative_to(root)),'sha256':sha(path),'bytes':path.stat().st_size}
def topo(path):
 doc,binb,raw=read_glb(path)
 ret=[]
 for mi,mesh in enumerate(doc.get('meshes',[])):
  tris=[]; xyzs=[]
  for pi,prim in enumerate(mesh.get('primitives',[])):
   if prim.get('mode',4)!=4: continue
   pos=accessor_values(doc,binb,prim['attributes']['POSITION'])
   ix=accessor_values(doc,binb,prim['indices'])[0:] if 'indices' in prim else [(i,) for i in range(len(pos))]
   inds=[int(v[0]) for v in ix]
   for i in range(0,len(inds)-2,3):
    tris.append(tuple(tuple(float(z) for z in pos[inds[j]]) for j in (i,i+1,i+2)))
  if not tris: ret.append({'mesh':mi,'name':mesh.get('name'),'triangles':0}); continue
  flat=[p for t in tris for p in t]
  mins=[min(p[k] for p in flat) for k in range(3)]; maxs=[max(p[k] for p in flat) for k in range(3)]
  extent=max(maxs[k]-mins[k] for k in range(3)); tol=max(1e-9,extent*1e-8)
  welded={};
  def wid(p):
   q=tuple(round(v/tol) for v in p)
   if q not in welded: welded[q]=len(welded)
   return welded[q]
  edges={}; deg=0; zero_area=0; dup=set(); duplicate_faces=0
  def addedge(a,b):
   key=(min(a,b),max(a,b)); edges[key]=edges.get(key,0)+1
  for tri in tris:
   ids=[wid(p) for p in tri]
   if len(set(ids))<3: deg+=1
   a,b,c=tri
   u=[b[i]-a[i] for i in range(3)]; v=[c[i]-a[i] for i in range(3)]
   cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
   area2=math.sqrt(sum(x*x for x in cross))
   if area2<=tol*tol: zero_area+=1
   face=tuple(sorted(ids))
   if face in dup: duplicate_faces+=1
   dup.add(face)
   for a,b in ((ids[0],ids[1]),(ids[1],ids[2]),(ids[2],ids[0])): addedge(a,b)
  incidence={n:edges.get(edge,0) for edge,n in []}
  boundaries=sum(1 for n in edges.values() if n==1); nonman=sum(1 for n in edges.values() if n>2)
  ret.append({'mesh_index':mi,'name':mesh.get('name'),'primitives':len(mesh.get('primitives',[])),'triangles':len(tris),'position_vertices_raw':sum(doc['accessors'][p['attributes']['POSITION']]['count'] for p in mesh['primitives']),'welded_vertices':len(welded),'weld_tolerance':tol,'boundary_edges_welded':boundaries,'nonmanifold_edges_welded':nonman,'degenerate_triangles_welded':deg,'near_zero_area_triangles':zero_area,'duplicate_triangles':duplicate_faces})
 return ret
for asset,rev in finals:
 d=ROOT/B/asset/rev
 h=sel[asset]; expected=assets[asset];
 b=json.load(open(d/'brief.json')); pre=json.load(open(d/'candidate-brief-prebinding.json')); candbrief=json.load(open(d/'candidate-brief.json')); binding=json.load(open(d/'artifact-binding.json'))
 refs=json.load(open(d/'references.json')); freeze=json.load(open(d/'modeling-freeze.json')); config=json.load(open(d/'build-config.json')); deps=json.load(open(d/'build-dependencies.json'))
 concept=json.load(open(d/'concept-generation.json')); ev=json.load(open(d/'concept-evidence.json')); manifest=json.load(open(d/'proof-final/render-manifest.json'))
 proof_bound=[e for e in map(json.loads,open(d/'lifecycle.jsonl')) if e.get('stage')=='proof-bound']
 # exact selected hashes
 pins={key:sha(d/filename) for key,filename in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json'),('source','source.blend'),('generator','generator.py'),('config','build-config.json')]}
 pin_match=pins==h['hashes'] and pins==expected['hashes']
 # original pre-model brief/metadata-only add check
 pre_hash=sha(d/'candidate-brief-prebinding.json')
 orig_freeze_match=(pre==b and pre_hash==freeze.get('brief_sha256') and freeze.get('brief_sha256')==sha(d/'brief.json'))
 bind_after_build=(binding.get('glb_sha256')==pins['glb'] and binding.get('original_premodel_brief_sha256')==freeze.get('brief_sha256') and binding.get('bound_candidate_brief_sha256')==pins['brief'] and binding.get('bound_at')>=freeze.get('frozen_at'))
 only_delivery_bind_change=(candbrief.get('required_deliverables')==[{'role':role,'path':f'{B}/{asset}/{rev}/{path}','sha256':pins[key]} for role,key,path in [('generator','generator','generator.py'),('config','config','build-config.json'),('source','source','source.blend')]] and {k:v for k,v in candbrief.items() if k!='required_deliverables'}==pre)
 # closure pins
 deps_ok=all(sha(ROOT/p)==hsh for p,hsh in deps.items())
 # reference and concept image binding
 cg_img=Path(concept['local_original']); concept_hash=sha(cg_img); concept_copy_hash=sha(d/'concept-original.png')
 # render evidence
 frame_records=[]; oldframes={}
 if (d/'proof-prebinding/render-manifest.json').exists():
  old=json.load(open(d/'proof-prebinding/render-manifest.json')); oldframes={f['id']:f['sha256'] for f in old['frames']}
 for f in manifest.get('frames',[]):
  p=d/'proof-final'/f['path']; actualsha=sha(p); actualbytes=p.stat().st_size
  from PIL import Image
  im=Image.open(p); dims=list(im.size); im.verify()
  frame_records.append({'id':f['id'],'file_sha256':actualsha,'manifest_sha256':f['sha256'],'sha_match':actualsha==f['sha256'],'actual_bytes':actualbytes,'manifest_bytes':f.get('byte_length'),'bytes_match':actualbytes==f.get('byte_length'),'dimensions':dims,'prebinding_same_sha':oldframes.get(f['id'])==actualsha})
 proof_bind=proof_bound[-1] if proof_bound else {}
 render_binding_ok=(manifest.get('frame_count')==8 and {f['id'] for f in manifest.get('frames',[])}==set(b['required_views']) and manifest.get('source_glb_sha256')==pins['glb'] and manifest.get('subject',{}).get('brief_sha256')==pins['brief'] and manifest.get('subject',{}).get('references_sha256')==pins['references'] and len(proof_bound)>=1 and proof_bind.get('exit_code')==0 and proof_bind.get('started_at')<=manifest.get('created_at')<=proof_bind.get('ended_at') and ('proof-final' in proof_bind.get('command',[]) or any('proof-final' in x for x in proof_bind.get('command',[]))))
 # actual static glb audit
 audit=audit_glb(d/'model.glb',max_triangles=14000,max_materials=6,max_primitives=30)
 doc,binb,raw=read_glb(d/'model.glb')
 textures=len(doc.get('textures',[])); imgs=len(doc.get('images',[]))
 # profile and concept validator outputs
 profile=json.load(open(OUT/'profile'/f'{asset}.json')); conceptv=json.load(open(OUT/'concept'/f'{asset}.json'))
 kh=json.load(open(OUT/'khronos'/asset/'gltf-validator.report.json'))
 runtime=json.load(open(OUT/'runtime'/asset/'runtime-parse.report.json'))
 # per mesh topology
 top=topo(d/'model.glb')
 # recorded bounds scale notes
 metadata=json.load(open(d/'metadata.json')); metric=json.load(open(d/'metrics.json'))
 results.append({'asset_id':asset,'revision':rev,'path':B+'/'+asset+'/'+rev,'pins':pins,'handoff_pin_match':pin_match,'original_premodel_brief':{'hash':pre_hash,'frozen_hash':freeze.get('brief_sha256'),'equal_prebinding_and_original':orig_freeze_match,'freeze_time':freeze.get('frozen_at'),'concept_hash':freeze.get('concept_sha256'),'seed':config.get('seed'),'config_hash_at_freeze':freeze.get('config_sha256'),'freeze_config_matches_current':freeze.get('config_sha256')==pins['config']},'delivery_binding':{'bound_at':binding.get('bound_at'),'metadata_only_required_deliverables_change':only_delivery_bind_change,'artifact_binding_matches':bind_after_build,'required_deliverables':candbrief.get('required_deliverables')},'dependency_closure':{'ok':deps_ok,'pinned':deps,'config_seed':config.get('seed'),'blender_version':config.get('blender_version'),'three_version':config.get('three_version')},'concept':{'local_original_sha256':concept_hash,'concept_copy_sha256':concept_copy_hash,'record_hash':concept.get('original_sha256'),'evidence_record_artifacts':ev.get('artifacts'),'provider_receipt_limit':concept.get('provider_receipt_limit'),'validation':conceptv},'proof_render':{'created_at':manifest.get('created_at'),'actual_postbinding_runner':proof_bind,'manifest_pin_match':render_binding_ok,'frame_count':len(frame_records),'frames':frame_records,'different_from_prebinding':all(not f['prebinding_same_sha'] for f in frame_records),'config_sha256':manifest.get('config_sha256'),'render_config_sha256':sha(d/'proof-final/render-config.json'),'render_config_matches_manifest':manifest.get('config_sha256')==sha(d/'proof-final/render-config.json')},'glb':{'independent_static_audit':audit,'texture_count':textures,'image_count':imgs,'khronos_validator':kh,'node_threejs_parse':runtime,'topology_per_mesh_welded':top,'budgets':{'triangles':audit.get('scene_triangles'),'max_triangles':14000,'materials':audit.get('materials'),'max_materials':6,'primitives':audit.get('scene_primitives'),'max_primitives':30,'bytes':len(raw),'max_bytes':1000000,'textures':textures,'max_textures':0}},'scale':{'nominal':metadata.get('nominal_dimensions_blender_xyz_m'),'measured_blender':metadata.get('measured_dimensions_blender_xyz_m'),'measured_glb':metadata.get('measured_dimensions_glb_m'),'nominal_distinct_from_measured':metadata.get('nominal_dimensions_blender_xyz_m')!=metadata.get('measured_dimensions_blender_xyz_m'),'note':metadata.get('scale_note'),'handoff_nominal':h.get('nominal_dimensions_blender_xyz_m'),'handoff_measured_blender':h.get('measured_blender_xyz_m'),'handoff_measured_glb':h.get('measured_glb_xyz_m')},'metadata_status':metadata.get('acceptance')})
status=subprocess=None
r={'schema_version':1,'source_repo':{'path':str(ROOT),'head':os.popen(f'cd {ROOT} && git rev-parse HEAD').read().strip(),'branch':os.popen(f'cd {ROOT} && git branch --show-current').read().strip(),'status_porcelain':os.popen(f'cd {ROOT} && git status --porcelain').read().strip()},'handoff_batch':handoff.get('batch'),'round':handoff.get('round'),'assets':results}
(OUT/'structural-audit.json').write_text(json.dumps(r,indent=2)+'\n')
print(OUT/'structural-audit.json')
for x in results:
 print(x['asset_id'], 'pins',x['handoff_pin_match'],'freeze',x['original_premodel_brief']['equal_prebinding_and_original'],'bind',x['delivery_binding']['metadata_only_required_deliverables_change'],x['delivery_binding']['artifact_binding_matches'],'closure',x['dependency_closure']['ok'],'proof',x['proof_render']['manifest_pin_match'],x['proof_render']['different_from_prebinding'],'mesh',[(m['triangles'],m['boundary_edges_welded'],m['nonmanifold_edges_welded'],m['degenerate_triangles_welded'],m['near_zero_area_triangles']) for m in x['glb']['topology_per_mesh_welded']])
