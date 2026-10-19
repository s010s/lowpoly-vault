# SPDX-License-Identifier: MIT
"""Independent, fail-closed delivery-record audit. No source or candidate mutation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,subprocess,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'scripts/qa_glb.py').is_file())
BASE=Path('production/concept-small-land-air-20261019');B=ROOT/BASE;D=B/'delivery-completion'
FROZEN='68483aa3b8eed2d86f9e59a930128d99579b0838';REPAIR='e874e99d20b3b98c73cddb8496bcd7e89be4e28c';QACOMMIT='3d024e53c36863d1887abd726998fa0f0d7b3831'
QA=Path('qa/independent/small-land-air-quartet-20261019');ASSETS=['sapeornis','longirostravis','dunbaria','chimerarachne']
sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb,read_glb
from validate_concept_evidence import validate as validate_concept

def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(p):return sha(p.read_bytes())
def load(p):return json.loads(p.read_text())
def write(n,d):
 p=OUT/n; text=json.dumps(d,indent=2,ensure_ascii=False)+'\n'
 if p.exists():assert p.read_text()==text, 'Refusing changed evidence overwrite: '+str(p)
 else:p.write_text(text)
def git(*a):return subprocess.check_output(['git',*map(str,a)],cwd=ROOT)
def raw(c,p):return git('show',c+':'+str(p))
def tree(c,p):
 out={}
 for line in git('ls-tree','-rz',c,'--',p).split(b'\0'):
  if line:
   header,path=line.split(b'\t',1);mode,typ,oid=header.decode().split();assert typ=='blob';out[path.decode()]={'mode':mode,'git_blob':oid}
 return out
def bind(desc,base=ROOT):
 p=(base/desc['path']).resolve();assert p.is_relative_to(ROOT) and p.is_file(),desc
 assert digest(p)==desc['sha256'],desc
 if 'bytes' in desc:assert p.stat().st_size==desc['bytes'],desc
 return str(p.relative_to(ROOT))
def walk_bind(v,base=ROOT):
 result=[]
 if isinstance(v,dict):
  if isinstance(v.get('path'),str) and isinstance(v.get('sha256'),str):result.append(bind(v,base))
  for x in v.values():result+=walk_bind(x,base)
 elif isinstance(v,list):
  for x in v:result+=walk_bind(x,base)
 return result
old=tree(FROZEN,BASE);new=tree(REPAIR,BASE)
changed=sorted(p for p in old if p in new and old[p]!=new[p]);removed=sorted(set(old)-set(new));added=sorted(set(new)-set(old));unchanged=sorted(p for p in old if old[p]==new.get(p))
allowed={str(BASE/n) for n in ['HANDOFF.md','handoff.json','freeze-manifest.json']}|{str(BASE/a/'r001/output'/a/'metadata.json') for a in ASSETS}
assert set(changed)==allowed and not removed and len(unchanged)==329 and len(added)==61
all_changes=git('diff','--name-only',FROZEN,REPAIR).decode().splitlines();assert set(all_changes)==set(changed+added)
assert git('rev-parse',REPAIR+'^').decode().strip()==FROZEN
pins=load(D/'baseline-files.json');assert pins['source_commit']==FROZEN and set(pins['files'])==set(old)
entries=[]
for p in old:
 original=raw(FROZEN,p);assert pins['files'][p]=={'sha256':sha(original),'bytes':len(original)}
 current=(ROOT/p).read_bytes()
 if p in unchanged:assert current==original,p
 entries.append({'path':p,'original_git_blob':old[p]['git_blob'],'repair_git_blob':new[p]['git_blob'],'original_sha256':sha(original),'repair_sha256':sha(current),'unchanged':current==original})
for p in new:
 assert (ROOT/p).read_bytes()==raw(REPAIR,p),p
actual={str(p.relative_to(ROOT)) for p in B.rglob('*') if p.is_file()};assert actual==set(new),(actual-set(new),set(new)-actual)
for p in changed:
 name=Path(p).name if Path(p).name!='metadata.json' else Path(p).parent.name+'-metadata.json'
 assert (D/'original-records'/name).read_bytes()==raw(FROZEN,p)
assert (B/'HANDOFF.md').read_bytes().startswith(raw(FROZEN,BASE/'HANDOFF.md'))
manifest=load(B/'freeze-manifest.json');assert manifest['source_model_commit']==FROZEN
assert {str(BASE/f['path']) for f in manifest['files']}==set(new)-{str(BASE/'freeze-manifest.json')}
for f in manifest['files']:bind(f,B)
exact=load(D/'exact-diff.json');assert exact['source_commit']==FROZEN and exact['unchanged_original_files']==329
assert {f['path'] for f in exact['modified_records']}==set(changed)-{str(BASE/'freeze-manifest.json')}
assert {f['path'] for f in exact['added_files']}==set(added)-{str(BASE/'delivery-completion/exact-diff.json')}
for f in exact['modified_records']:
 assert f['before']==pins['files'][f['path']];assert f['after']=={'sha256':digest(ROOT/f['path']),'bytes':(ROOT/f['path']).stat().st_size}
for f in exact['added_files']:bind(f)
write('tree-integrity.json',{'frozen_source':FROZEN,'repair':REPAIR,'repair_parent_is_frozen_source':True,'original_bundle_files':len(old),'unchanged_original_files':len(unchanged),'changed_existing_records':changed,'added_files':added,'deleted_files':removed,'changes_outside_bundle':[],'current_worktree_matches_exact_repair':True,'original_versions_preserved_verbatim':True,'complete_current_snapshot_bindings_verified':len(manifest['files']),'entries':entries})
qa_files=tree(QACOMMIT,QA);qa_catalog=[]
for p,e in qa_files.items():
 data=raw(QACOMMIT,p);qa_catalog.append({'path':p,**e,'bytes':len(data),'sha256':sha(data)})
qa_source=tree(QACOMMIT,BASE);assert qa_source==old
provenance=load(D/'qa-provenance.json');assert provenance['qa_commit']==QACOMMIT and provenance['source_commit']==FROZEN
for f in provenance['files']:bind(f);assert (ROOT/f['path']).read_bytes()==raw(QACOMMIT,f['original_path'])
q=load(D/'independent-review-source.json');assert q['frozen_git_sha']==FROZEN and q['overall_status']=='limited_qa_pass_with_formal_and_release_blockers'
visual=json.loads(raw(QACOMMIT,QA/'visual-review.json'));assert visual['frozen_git_sha']==FROZEN
assert digest(ROOT/visual['concept_image']['path'])==visual['concept_image']['sha256']
qa_image_bindings=[]
for a in visual['assets']:
 for frame in a['frames']:
  assert sha(raw(QACOMMIT,frame['path']))==frame['sha256'];qa_image_bindings.append(frame['path'])
runtime=json.loads(raw(QACOMMIT,QA/'runtime/software-webgl-scene.report.json'))
assert [s['instances_per_asset'] for s in runtime['scenarios']]==[1,8,32]
assert not runtime['page_errors'] and not runtime['console_messages'] and not runtime['runtime']['context_lost']
assert 'SwiftShader' in runtime['runtime']['unmasked_gl_renderer']
write('original-qa-integrity.json',{'qa_commit':QACOMMIT,'source_tree_matches_frozen_source':True,'all_original_qa_files_accessible':True,'qa_file_count':len(qa_catalog),'source_reports_copied_verbatim':provenance['files'],'hash_verified_original_visual_images':qa_image_bindings,'software_instances_per_asset':[1,8,32],'software_renderer':runtime['runtime']['unmasked_gl_renderer'],'current_visual_review_rerun':False,'limitation':'Prior observed visual/software evidence retained by exact Git object identities and hashes. This audit grants no formal or hardware/target-scene approval.','files':qa_catalog})
h=load(B/'handoff.json');assert {a['asset_id']:a['revision'] for a in h['assets']}=={a:'r001' for a in ASSETS}
assert h['rejected_revision']['asset_id']=='sapeornis' and h['rejected_revision']['revision']=='r002'
all_bindings=walk_bind(h,B);items=[]
for asset in ASSETS:
 folder=BASE/asset/'r001';d=ROOT/folder;out=d/'output'/asset;glb=out/(asset+'.glb');blend=out/(asset+'.blend');m=load(out/'metadata.json');c=load(d/'candidate.json');brief=load(d/'candidate-brief.json');refs=load(d/'candidate-references.json');config=load(d/'build-config.json');item=next(i for i in h['assets'] if i['asset_id']==asset)
 measured=audit_glb(glb,max_triangles=config['max_triangles'],max_materials=config['max_materials'],max_primitives=config['max_primitives']);doc,binary,glbraw=read_glb(glb)
 assert not measured['errors'];write(asset+'-fresh-glb-audit.json',measured)
 assert m['dimensions_m']==m['dimensions']==measured['bounds_m']['size']==c['measurements']['dimensions_m']==item['dimensions_m']==item['dimensions_glb_xyz_m']
 assert m['bounds_glb_m']==measured['bounds_m']
 assert m['bytes']==m['glb_bytes']==len(glbraw)==c['measurements']['glb_bytes']==item['glb_bytes']
 assert m['blend_bytes']==blend.stat().st_size==c['measurements']['blend_bytes'];assert m['file_bytes']=={'glb':len(glbraw),'blend':blend.stat().st_size}
 assert m['triangles']==measured['scene_triangles']==c['measurements']['triangles']==item['triangles']
 assert m['primitives']==measured['scene_primitives_estimated_base_draw_calls']==c['measurements']['primitives']==item['scene_primitives']
 assert m['material_count']==len(doc['materials'])==measured['materials']==c['measurements']['materials']==item['materials']
 assert m['textures']==m['texture_count']==len(doc.get('textures',[]))==c['measurements']['textures']==0
 assert m['images']==len(doc.get('images',[]))==c['measurements']['images']==0 and m['texture_inventory']==[] and m['texture_bytes']==0
 assert m['exported_position_accessor_vertices']==measured['unique_position_accessor_vertices']==item['exported_position_accessor_vertices']
 assert m['extensions_used']==doc.get('extensionsUsed',[]) and m['extensions_required']==doc.get('extensionsRequired',[])
 assert m['sha256']=={'glb':digest(glb),'blend':digest(blend)}
 assert m['axis']['up']=='+Y' and m['axis']['forward']=='+Z' and m['axis']['source_up']=='+Z' and m['axis']['source_forward']=='-Y' and m['axis']['handedness']=='right' and m['axis']['source_to_glb']=='(x, y, z) -> (x, z, -y)'
 assert m['axis']==item['axis'] and m['origin']==config['mount_origin']
 src=load(OUT/(asset+'-fresh-blender-source.json'));stored_src=load(D/'evidence'/(asset+'-source.json'));orig_src=load(d/'source-export.report.json')
 assert src['model_bytes_unchanged'] and src['hashes_before']==src['hashes_after']=={glb.name:digest(glb),blend.name:digest(blend)}
 assert src['authored_vertices']==m['authored_vertices']==stored_src['authored']['vertices']==item['authored_vertices']
 assert src['authored_polygon_faces']==m['authored_polygon_faces']==stored_src['authored']['polygon_faces']
 assert src['evaluated_triangles']==m['triangles']==stored_src['source']['triangles']==orig_src['source_triangles']==orig_src['glb_triangles']
 assert src['blender_version']==m['blender_version']==stored_src['blender_version'] and src['unit_scale']==m['blender_unit_scale']==stored_src['blender_unit_scale']==1
 assert src['bounds_blender_m']==stored_src['source']['bounds_blender_m']==orig_src['source_bounds_blender_m']
 assert src['bounds_blender_m']['size']==m['blender_dimensions_m']
 delta=max(abs(src['expected_glb_bounds_m'][s][i]-measured['bounds_m'][s][i]) for s in ['min','max'] for i in range(3));assert delta<1e-8 and delta==orig_src['bounds_max_error_m']==stored_src['source_export']['bounds_max_error_m']
 assert src['expected_glb_bounds_m']==orig_src['expected_glb_bounds_m']==stored_src['source_export']['expected_glb_bounds_m']
 assert measured['bounds_m']==orig_src['measured_glb_bounds_m']==stored_src['source_export']['measured_glb_bounds_m']
 assert m['source_export_status']==orig_src['status']==stored_src['source_export']['status']
 assert m['source_export_warnings']==orig_src['warnings']==stored_src['source_export']['warnings']
 assert orig_src['source_sha256']==digest(blend) and orig_src['glb_sha256']==digest(glb)
 assert all(measured[k]==load(D/'evidence'/(asset+'-glb-audit.json'))[k] for k in measured if k!='file')
 palette={x['name']:x['srgb'] for x in m['materials']};actual_colors={};material_deltas=[]
 assert set(src['used_materials'])=={x['name'] for x in doc['materials']}
 for mat in doc['materials']:
  pbr=mat['pbrMetallicRoughness'];linear=pbr['baseColorFactor'];source_mat=src['used_materials'][mat['name']]
  md=max(abs(source_mat['base_color'][i]-linear[i]) for i in range(4));assert md<1e-7
  assert abs(source_mat['roughness']-pbr['roughnessFactor'])<1e-7 and abs(source_mat['metallic']-pbr.get('metallicFactor',1))<1e-7
  color='#'+''.join(f'{round((v*12.92 if v<=0.0031308 else 1.055*v**(1/2.4)-0.055)*255):02X}' for v in linear[:3]);assert color==palette[mat['name']]
  actual_colors[mat['name']]=color;material_deltas.append(md)
 assert c['revision']=='r001' and c['asset_id']==asset and c['approval']=={'status':'pending'} and c['publication_authority']=='separate'
 assert set(c['stages'])=={'technical','visual','factual','specification','runtime_parse','gpu','scene'}
 assert all(s['status']=='unknown' and s['reviewer'] is None and s['reviewed_at'] is None and s['subject'] is None and s['evidence']==[] and all(x['status']=='unknown' and x['evidence']==[] for x in s['criteria']) for s in c['stages'].values())
 assert c['evidence']==[] and len(c['blockers'])==4 and all(x['status']=='open' for x in c['blockers'])
 assert brief['registration_only'] and brief['preproduction_freeze_claim'] is False and brief['registered_at']==c['created_at']==m['metadata_completed_at']
 assert brief['original_evidence_coverage']['turntable_frames']==0 and len(brief['original_evidence_coverage']['required_views'])==11 and brief['turntable_frames']==24 and 'detail' in brief['required_views']
 all_bindings+=walk_bind(c)+walk_bind(brief)+walk_bind(refs)+walk_bind(m)
 for k in ['glb','blend','generator','preview','candidate_record']:assert (ROOT/m[k]).is_file()
 assert digest(ROOT/m['generator'])==m['generator_sha256'] and digest(ROOT/m['preview'])==m['preview_sha256']
 assert m['generator']==str(BASE/('generator-r001.py' if asset=='sapeornis' else 'generator.py'))
 proof=load(d/'proof/render-manifest.json');assert proof['source_glb_sha256']==proof['subject']['glb_sha256']==digest(glb)
 assert proof['subject']['brief_sha256']==digest(d/'brief.json') and proof['subject']['references_sha256']==digest(d/'references.json')
 assert len(proof['frames'])==11;all_bindings+=walk_bind(proof,d/'proof')
 assert m['preview']==str(folder/'proof/hero.png') and c['artifacts']['preview']==m['preview_record']
 vcmd=[sys.executable,'-B','scripts/validate_candidate.py',str(folder/'candidate.json'),'--json']
 vr=subprocess.run(vcmd,cwd=ROOT,capture_output=True,text=True);assert vr.returncode==0,vr.stdout+vr.stderr;v=json.loads(vr.stdout)
 write(asset+'-candidate-validation.json',v);assert v['valid'] and not v['approved_for_brief'] and not v['errors'] and v==load(d/'candidate-validation.json')
 gr=subprocess.run(vcmd+['--require-approved'],cwd=ROOT,capture_output=True,text=True);assert gr.returncode==1 and json.loads(gr.stdout)==v
 write(asset+'-approval-guard.json',{'command':vcmd+['--require-approved'],'exit_code':gr.returncode,'expected_exit_code':1,'meaning':'Record valid, formal approval correctly rejected','result':json.loads(gr.stdout),'stderr':gr.stderr})
 cv=validate_concept(d/'concept-evidence.json',B);assert cv['valid'] and cv['evidence_complete'];write(asset+'-concept-integrity.json',cv)
 kh=load(OUT/(asset+'-fresh-khronos.json'));assert kh['glb_sha256']==digest(glb) and kh['report']['issues']['numErrors']==kh['report']['issues']['numWarnings']==0 and not kh['report']['issues']['truncated']
 prior=next(x for x in q['assets'] if x['id']==asset);assert prior['glb_sha256']==digest(glb) and prior['blend_sha256']==digest(blend)
 assert runtime['assets'][asset]['sha256']==digest(glb)
 oldm=json.loads(raw(FROZEN,folder/'output'/asset/'metadata.json'));meta_changes={k:{'old':oldm[k],'new':m.get(k)} for k in oldm if oldm[k]!=m.get(k)}
 assert set(meta_changes)<={'preview','generator','origin'},meta_changes
 items.append({'asset_id':asset,'revision':'r001','status':'pass','glb_sha256':digest(glb),'blend_sha256':digest(blend),'candidate_sha256':digest(d/'candidate.json'),'metadata_sha256':digest(out/'metadata.json'),'candidate_record_valid':True,'approved_for_brief':False,'all_formal_stages':'unknown','require_approved_exit_code':gr.returncode,'triangles':m['triangles'],'materials':m['material_count'],'primitives':m['primitives'],'glb_bytes':m['glb_bytes'],'blend_bytes':m['blend_bytes'],'dimensions_m':m['dimensions_m'],'fresh_source_export_bounds_max_error_m':delta,'fresh_source_export_triangle_match':True,'fresh_source_export_material_names_and_pbr_match':True,'source_material_base_color_max_error':max(material_deltas),'actual_exported_srgb_colors':actual_colors,'palette_unused_names':sorted(set(palette)-set(actual_colors)),'source_export_status':m['source_export_status'],'source_export_warnings':m['source_export_warnings'],'fresh_khronos_errors':0,'fresh_khronos_warnings':0,'preview_role':m['preview_role'],'original_concept_evidence_complete':True,'existing_metadata_field_changes':meta_changes})
write('current-path-hash-bindings.json',{'status':'pass','bindings_verified':len(all_bindings),'unique_files':len(set(all_bindings)),'paths':all_bindings,'snapshot_bindings_verified_separately':len(manifest['files']),'historical_original_record_paths':'Preserved verbatim; validated against frozen Git blobs, not falsely reinterpreted as current paths.'})
result={'schema_version':1,'checked_at':datetime.now(timezone.utc).isoformat(),'status':'pass','scope':'Independent delivery-record repair integrity and current technical measurements only. No source edits, rerendering, publication or formal approval.','frozen_source_commit':FROZEN,'repair_commit':REPAIR,'prior_independent_qa_commit':QACOMMIT,'unchanged_original_files':len(unchanged),'changed_existing_records':len(changed),'added_files':len(added),'all_current_bundle_bytes_match_repair_commit':True,'all_snapshot_path_hash_bindings_valid':True,'candidate_path_hash_bindings_valid':True,'original_qa_evidence_unchanged_and_accessible':True,'sapeornis_selected_revision':'r001','sapeornis_r002':'preserved unchanged, not adopted','fresh_npm_test':{'exit_code':0,'evidence':'npm-test.txt','attempts':1},'assets':items,'blockers_for_delivery_record_repair':[],'remaining_acceptance_gates':['Seven formal stages unknown, approval pending; prior limited QA is not re-signed against new candidate/brief hashes.','Production profile requires detail plus 24 turntable frames; unchanged proof has 11 fixed views and zero turntable frames.','Physical target hardware/performance and deployed populated production-scene acceptance remain unverified.','Diagnostic previews resolve and bind exactly; official unified-gallery poster delivery remains separate.','Sapeornis outer-wing shape limitation and flight-body-center mounting warning retained.','Publication/integration authorization is separate and parent-owned.'],'not_rerun':['Visual/factual review or new renders','Browser/WebGL scenes or hardware/performance tests','Rebuild reproducibility'],'mutation_scope':'New QA evidence only in this audit directory.'}
write('report.json',result)
print(json.dumps({k:result[k] for k in ['status','unchanged_original_files','changed_existing_records','added_files','blockers_for_delivery_record_repair']},indent=2))
