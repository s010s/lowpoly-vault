# SPDX-License-Identifier: MIT
"""Independent supplemental-delivery audit. Writes only this audit directory."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,math,subprocess,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[2]
BASE=Path('production/concept-small-marine-quartet-20261019')
QA=Path('qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh')
FROZEN='7c3cc658c1d10fa595e3ef7d27c6f0b17a842dd1'; SOURCE='1c1b5fd0f466feb95457a8c96ed58ed8f219201f'; QACOMMIT='45b1411119a624461f84452adfcd0cd83838a074'
SELECTED={'emeraldella':'r002','burgessia':'r002','tuzoia':'r003','sanctacaris':'r002'}
sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb,read_glb
from validate_concept_evidence import validate as validate_concept

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
 p=OUT/name
 assert not p.exists(),p
 p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def frozen(commit,path):return git('show',commit+':'+str(path))
def tree(commit,prefix):
 entries={}
 for row in git('ls-tree','-rz',commit,'--',str(prefix)).split(b'\0'):
  if row:
   header,path=row.split(b'\t',1);mode,typ,oid=header.decode().split()
   assert typ=='blob'
   entries[path.decode()]={'oid':oid,'mode':mode}
 return entries
def bloboid(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def verify_worktree(commit,prefix):
 entries=tree(commit,prefix);failed=[]
 for path,entry in entries.items():
  p=ROOT/path
  if not p.is_file() or bloboid(p.read_bytes())!=entry['oid']:failed.append(path)
 actual={str(p.relative_to(ROOT)) for p in (ROOT/prefix).rglob('*') if p.is_file()}
 extra=sorted(actual-set(entries))
 return {'commit':commit,'prefix':str(prefix),'tracked_files':len(entries),'mismatches':failed,'uncommitted_extra_files':extra,'matches_exact_commit':not failed and not extra}
old=tree(FROZEN,BASE);new=tree(SOURCE,BASE)
changed=[p for p in old if p in new and old[p]!=new[p]];removed=sorted(set(old)-set(new));added=sorted(set(new)-set(old))
allowed={str(BASE/n) for n in ['HANDOFF.md','bundle-hashes.json','events.jsonl','handoff.json','selected-models.json']}
for a,r in SELECTED.items():allowed|={str(BASE/a/r/n) for n in ['metadata.json','integration-metadata.json']}
unexpected=sorted(set(changed)-allowed)
assert not removed and not unexpected,(removed,unexpected)
assert (ROOT/BASE/'events.jsonl').read_bytes().startswith(frozen(FROZEN,BASE/'events.jsonl'))
assert (ROOT/BASE/'HANDOFF.md').read_bytes().startswith(frozen(FROZEN,BASE/'HANDOFF.md'))
assert (ROOT/BASE/'delivery-completion/original-bundle-hashes-at-7c3cc658.json').read_bytes()==frozen(FROZEN,BASE/'bundle-hashes.json')
source_match=verify_worktree(SOURCE,BASE);qa_match=verify_worktree(QACOMMIT,QA)
assert source_match['matches_exact_commit'] and qa_match['matches_exact_commit'],(source_match,qa_match)
unchanged_count=sum(1 for p in old if p in new and old[p]==new[p])
write('marine-frozen-tree-comparison.json',{'original_commit':FROZEN,'supplemented_commit':SOURCE,'original_files':len(old),'unchanged_original_files':unchanged_count,'changed_existing_files':changed,'added_files':added,'removed_files':removed,'unexpected_existing_changes':unexpected,'source_worktree':source_match,'independent_qa_worktree':qa_match,'original_handoff_and_event_records_preserved_as_prefix':True,'original_hash_manifest_preserved_verbatim':True})
items=[];selections=json.loads((ROOT/BASE/'selected-models.json').read_text())['selected']
assert {i['id']:i['revision'] for i in selections}==SELECTED
for asset,revision in SELECTED.items():
 folder=BASE/asset/revision;d=ROOT/folder;glb=d/(asset+'.glb');blend=d/(asset+'.blend')
 m=json.loads((d/'metadata.json').read_text());im=json.loads((d/'integration-metadata.json').read_text());c=json.loads((d/'candidate.json').read_text());brief=json.loads((d/'candidate-brief.json').read_text());selection=next(i for i in selections if i['id']==asset)
 report=audit_glb(glb,max_triangles=16000,max_materials=7,max_primitives=220);doc,binary,raw=read_glb(glb)
 assert report['status']=='pass',report
 write(asset+'-fresh-glb-audit.json',report)
 assert m['dimensions_m']==m['dimensions']==report['bounds_m']['size'];assert m['bounds_glb_m']==report['bounds_m'];assert m['bytes']==m['glb_bytes']==len(raw);assert m['blend_bytes']==blend.stat().st_size
 assert m['file_bytes']=={'glb':len(raw),'blend':blend.stat().st_size};assert m['triangles']==report['scene_triangles'];assert m['primitives']==report['scene_primitives_estimated_base_draw_calls']
 assert m['material_count']==len(doc.get('materials',[]))==report['materials'];assert m['textures']==m['texture_count']==len(doc.get('textures',[]))==0
 assert m['images']==len(doc.get('images',[]))==0;assert m['texture_inventory']==[] and m['texture_bytes']==0
 assert m['exported_position_stream_vertices']==report['unique_position_accessor_vertices'];assert m['extensions_used']==doc.get('extensionsUsed',[]) and m['extensions_required']==doc.get('extensionsRequired',[])
 assert m['sha256']=={'glb':digest(glb),'blend':digest(blend)}
 assert m['axis']['up']=='+Y' and m['axis']['forward']=='+Z' and m['axis']['source_up']=='+Z' and m['axis']['source_forward']=='-Y' and m['axis']['handedness']=='right' and m['axis']['source_to_glb']=='(x, y, z) -> (x, z, -y)'
 for k in ['dimensions_m','axis','primitives','textures','bytes']:assert m[k]==im[k]==selection[k],(asset,k)
 src=json.loads((OUT/(asset+'-fresh-blender-source.json')).read_text())
 assert src['model_bytes_unchanged'] and src['authored_vertices']==m['authored_vertices'] and src['authored_polygon_faces']==m['authored_polygon_faces'] and src['evaluated_triangles']==m['triangles']
 assert src['unit_scale']==m['blender_unit_scale']==1 and src['blender_version']==m['blender_version']
 assert max(abs(src['bounds_blender_m']['size'][i]-m['blender_dimensions_m'][i]) for i in range(3))<1e-8
 delta=max(abs(src['expected_glb_bounds_m'][side][i]-report['bounds_m'][side][i]) for side in ['min','max'] for i in range(3));assert delta<1e-8
 expected_materials={x['name']:x['srgb'] for x in m['materials']};actual_materials={}
 for mat in doc['materials']:
  linear=mat['pbrMetallicRoughness']['baseColorFactor'][:3]
  srgb=[v*12.92 if v<=0.0031308 else 1.055*(v**(1/2.4))-0.055 for v in linear]
  actual_materials[mat['name']]='#'+''.join(f'{round(v*255):02X}' for v in srgb)
 assert actual_materials==expected_materials,(actual_materials,expected_materials)
 assert c['approval']['status']=='pending' and c['publication_authority']=='separate'
 assert set(c['stages'])=={'technical','visual','factual','specification','runtime_parse','gpu','scene'}
 assert all(s['status']=='unknown' and s['reviewer'] is None and s['reviewed_at'] is None and s['subject'] is None for s in c['stages'].values())
 assert all(k['status']=='unknown' for s in c['stages'].values() for k in s['criteria'])
 assert brief['registration_only'] is True and brief['preproduction_freeze_claim'] is False and brief['registered_at']==c['created_at']==m['metadata_completed_at']
 assert brief['original_evidence_coverage']['turntable_frames']==0 and brief['turntable_frames']==24 and 'detail' in brief['required_views']
 assert len(brief['original_evidence_coverage']['required_views'])==12
 for descriptor in [*c['artifacts'].values(),*c['technical_evidence'].values()]:assert digest(ROOT/descriptor['path'])==descriptor['sha256']
 vcmd=[sys.executable,'-B','scripts/validate_candidate.py',str(folder/'candidate.json'),'--json']
 vrun=subprocess.run(vcmd,cwd=ROOT,capture_output=True,text=True);assert vrun.returncode==0,vrun.stdout+vrun.stderr;v=json.loads(vrun.stdout)
 write(asset+'-current-candidate-validation.json',v)
 assert v['valid'] and not v['approved_for_brief'] and v['approval_status']=='pending' and not v['errors']
 expected=json.loads((d/'candidate-validation.json').read_text());assert v==expected
 guard=subprocess.run(vcmd+['--require-approved'],cwd=ROOT,capture_output=True,text=True);assert guard.returncode==1 and json.loads(guard.stdout)==v
 concept=validate_concept(d/'concept-evidence.json',ROOT/BASE);assert concept['valid'] and concept['evidence_complete'];write(asset+'-concept-evidence-validation.json',concept)
 oldmeta=json.loads(frozen(FROZEN,folder/'metadata.json'));meta_changes={k:{'old':oldmeta.get(k),'new':m.get(k)} for k in oldmeta if oldmeta[k]!=m.get(k)}
 assert set(meta_changes)<= {'dimensions_m','axis','primitives','textures','independent_qa','blender_unit_scale'},meta_changes
 items.append({'asset_id':asset,'revision':revision,'status':'pass','glb_sha256':digest(glb),'blend_sha256':digest(blend),'fresh_candidate_structure_valid':True,'require_approved_exit_code':guard.returncode,'approved_for_brief':False,'formal_stages':'all unknown','approval':'pending','fresh_static_glb_status':report['status'],'fresh_blender_source_matches':True,'source_to_glb_bounds_max_error_m':delta,'populated_metadata_matches_measured_artifacts':True,'original_concept_evidence_complete':True,'triangles':m['triangles'],'primitives':m['primitives'],'glb_bytes':m['bytes'],'blend_bytes':m['blend_bytes'],'materials':m['material_count'],'textures':m['textures'],'dimensions_m':m['dimensions_m'],'authored_vertices':m['authored_vertices'],'authored_polygon_faces':m['authored_polygon_faces'],'exported_position_stream_vertices':m['exported_position_stream_vertices'],'existing_metadata_field_changes':meta_changes})
prov=json.loads((ROOT/BASE/'delivery-completion/qa-provenance.json').read_text()); retained=ROOT/BASE/'delivery-completion/independent-review-source.md'
assert prov['qa_commit']==QACOMMIT and prov['sha256']==digest(retained)==hashlib.sha256(frozen(QACOMMIT,QA/'REVIEW.md')).hexdigest()
review=json.loads((ROOT/QA/'review.json').read_text());assert review['scoped_review']=='pass' and review['release_acceptance']=='not_granted' and review['frozen_source_commit']==FROZEN
for a in review['assets']:
 measured=next(i for i in items if i['asset_id']==a['asset_id']);assert measured['glb_sha256']==a['glb_sha256'] and measured['blend_sha256']==a['blend_sha256']
checks=[]
for script in ['scripts/test_validate_candidate.py','scripts/test_candidate_profile.py']:
 p=subprocess.run([sys.executable,'-B',script,'-v'],cwd=ROOT,capture_output=True,text=True)
 name=Path(script).stem+'.txt';(OUT/('marine-'+name)).write_text(p.stdout+p.stderr);checks.append({'script':script,'exit_code':p.returncode,'evidence':'marine-'+name});assert p.returncode==0,p.stdout+p.stderr
result={'schema_version':1,'checked_at':datetime.now(timezone.utc).isoformat(),'status':'pass','scope':'Independent metadata/candidate delivery-completion integrity verification only. No original model, frozen design evidence, or formal approval edited.','source_commit':SOURCE,'original_qa_freeze':FROZEN,'independent_qa_commit':QACOMMIT,'source_matches_exact_commit':True,'qa_matches_exact_commit':True,'original_files_unchanged_except_allowed_delivery_metadata':True,'unchanged_original_files':unchanged_count,'changed_existing_delivery_record_count':len(changed),'new_completion_files':len(added),'candidate_validator_regression_tests':checks,'assets':items,'blockers_for_metadata_completion':[],'remaining_acceptance_gates':['All seven formal candidate stages remain unknown and approval pending.','Current production registration requires detail and 24-orbit coverage; original limited proof is twelve fixed views and zero turntable frames. Coverage is unverified, not waived or passed.','Independent limited QA pass applies to unchanged original model artifacts and the original bounded study only; it does not approve the added candidate/brief hashes.','Physical target hardware/device/performance and deployed populated scene acceptance remain unverified.','Publication authority remains separate.'],'not_rerun':['Independent visual or scientific/factual review','Khronos validator (original and independent reports hash-pinned unchanged)','Browser/WebGL runtime or physical device tests','Rebuild reproducibility','Formal profile acceptance'],'source_mutation':'none; audit output only'}
write('marine-delivery-integrity.json',result)
print(json.dumps({k:result[k] for k in ['status','unchanged_original_files','changed_existing_delivery_record_count','new_completion_files','blockers_for_metadata_completion']},indent=2))
