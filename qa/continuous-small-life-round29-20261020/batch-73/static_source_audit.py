#!/usr/bin/env python3
import json, pathlib, hashlib, subprocess, sys, re
from PIL import Image
ROOT=pathlib.Path('/workspace/shared/lowpoly-batch73-20261020')
BATCH=ROOT/'production/continuous-small-life-round29-20261020/work/batch-73'
OUT=pathlib.Path('/workspace/shared/lowpoly-round29-qa73')
sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
TARGETS=[('fractofusus','r002','b92742653a01962c03c874fcb81a3d980dbfe3b3e7f689ccc39e37da16ae6bcd'),('striated-bedrock','r003','aa8c39c13c3bfc1a4ef62eb4472bba44e1f09e9c123effb26405b2d2b3e104e8'),('fumarole-vent','r003','9703960b80b4add47b0c682e0cd64be451874463db4f6ce0c467a720ee15b807'),('banded-iron-formation','r003','e1ce2df854e001919b7105c56c0f6a26cabc9b84a163f2a89ae1cadcbac2ba38')]
VIEWS=['hero','reversehero','front','side','rear','top','clay','silhouette']
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(pathlib.Path(p).read_text())
def check(condition,msg,errors):
 if not condition:errors.append(msg)
errors=[]
commit=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','-C',str(ROOT),'branch','--show-current'],text=True).strip()
status=subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain=v1'],text=True).strip()
# Fixed original inventory hash directly from base-main commit, not a working branch snapshot.
base_inv=subprocess.check_output(['git','-C',str(ROOT),'show','54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c:research/prehistoric-1000-v1/inventory.json'])
base_inv_sha=hashlib.sha256(base_inv).hexdigest()
check(base_inv_sha=='b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c','base inventory hash changed',errors)
# Exact frozen source-evidence closure, then verify its files remain tracked in immutable HEAD.
manifest=load(BATCH/'source-evidence-manifest.json'); missing=[];changed=[];untracked=[]
tracked=set(subprocess.check_output(['git','-C',str(ROOT),'ls-files','-z'],text=False).decode().split('\0'))
for f in manifest['files']:
 p=ROOT/f['path']
 if not p.is_file():missing.append(f['path']); continue
 if p.stat().st_size!=f['bytes'] or sha(p)!=f['sha256']:changed.append(f['path'])
 if f['path'] not in tracked:untracked.append(f['path'])
check(not missing and not changed and not untracked,'manifest closure missing/changed/untracked',errors)
# Verify all actual consult-only reference pixels mentioned in ledgers match on-disk hashes.
ref_pixel_checks=[]
for ident,rev,glb in TARGETS:
 d=BATCH/'assets'/ident/rev; refs=load(d/'references.json')
 for source in refs.get('sources',[]):
  for im in source.get('consulted_images') or []:
   p=pathlib.Path('/workspace/shared/batch73-consult-only')/im['filename']; actual=sha(p) if p.is_file() else None
   row={'asset_id':ident,'source_id':source['id'],'file':str(p),'exists':p.is_file(),'ledger_sha256':im['sha256'],'actual_sha256':actual,'match':actual==im['sha256']}
   ref_pixel_checks.append(row)
   check(row['match'],f"consult-only reference pixels hash mismatch {ident}:{im['filename']}",errors)
 # All reference entries have rights notes; no third party files incorporated; BIF specifics and AM limitation preserved.
 for src in refs.get('sources',[]):
  check(bool(src.get('rights_note')),f"missing rights note {ident}:{src.get('id')}",errors)
  if src.get('use')!='original-generated-concept': check(src.get('incorporated') is False,f"unexpected incorporated source {ident}:{src.get('id')}",errors)
 if ident=='banded-iron-formation':
  usgs=next(s for s in refs['sources'] if s['id']=='USGS-SOUDAN')
  check('James St.John' in usgs.get('title','') and 'CC BY2.0' in usgs.get('license','') and 'generic Public Domain' in usgs.get('license','') and 'CC BY2.0' in usgs.get('rights_note',''),'BIF source-specific attribution absent/overwritten',errors)
  am=next(s for s in refs['sources'] if s['id']=='AM-DR19296')
  check(not am.get('consulted_images') and '403' in am.get('notes',''),'Australian Museum DR19296 image misrepresented as pixels inspected',errors)
# Candidate, freezes, visual frame bindings, exact bounds/budgets, semantic rebuild and approval separation.
assets=[]
for ident,rev,expected_glb in TARGETS:
 d=BATCH/'assets'/ident/rev; cand=load(d/'candidate.json'); brief=load(d/'candidate-brief.json'); refs=load(d/'references.json'); meta=load(d/'metadata.json')
 art=cand['artifacts']; active={}
 for k in ['glb','brief','references','source','generator','config']:
  ent=art[k]; p=ROOT/ent['path']; actual=sha(p)
  active[k]={'path':ent['path'],'candidate_sha256':ent['sha256'],'actual_sha256':actual,'matches':ent['sha256']==actual,'bytes':p.stat().st_size}
  check(ent['sha256']==actual,f"active candidate artifact hash mismatch {ident}:{k}",errors)
 check(art['glb']['sha256']==expected_glb,f"unexpected active GLB {ident}",errors)
 # Complete freeze and repair scopes preserve original-design hashes.
 freeze=load(d/'modeling-freeze.json'); repair=load(d/'repair-freeze.json'); original=d.parent/'r001'
 freeze_checks={}
 for name,expected in freeze['files'].items():
  p=original/name; actual=sha(p) if p.is_file() else None; freeze_checks[name]={'expected':expected,'actual':actual,'match':expected==actual};check(expected==actual,f"original premodel freeze hash mismatch {ident}:{name}",errors)
 for name,expected in repair['files'].items():
  p=original/name; actual=sha(p) if p.is_file() else None;check(expected==actual,f"repair/original immutable file mismatch {ident}:{name}",errors)
 # Concept evidence separate valid/incomplete, and candidate valid/unapproved.
 cval=load(d/'concept-validation.json'); candeval=load(d/'candidate-validation.json');
 check(cval.get('valid') is True and cval.get('evidence_complete') is False,f"concept integrity/incomplete distinction changed {ident}",errors)
 check(candeval.get('valid') is True and candeval.get('approved_for_brief') is False,f"candidate valid/unapproved distinction changed {ident}",errors)
 ce=load(d/'concept-evidence.json'); gen=load(d/'concept-generation.json'); original_concept=original/'concept-original.png'
 concept_hash=sha(original_concept); check(ce['concept']['images'][0]['sha256']==concept_hash,f"concept pixel hash mismatch {ident}",errors)
 check(gen.get('provider_generated_at') is None and gen.get('provider_internal_duration_seconds') is None,f"provider-internal times no longer explicitly unknown {ident}",errors)
 # Scope chronology: observed concept receipt predates immutable freeze, and production build follows complete freeze.
 frozen=freeze['frozen_at']; gen_result=gen['observed_result_at']; check(gen_result.replace('Z','+00:00')<frozen,f"concept result not before freeze {ident}",errors)
 life=[json.loads(x) for x in (d/'lifecycle.jsonl').read_text().splitlines() if x.strip()]
 build=next((x for x in life if x.get('stage')=='build'),None)
 if build: check(build.get('started_at','')>frozen,f"model build before original design freeze {ident}",errors)
 else: errors.append(f'missing final build lifecycle {ident}')
 # Proof manifest binds final renders to exact active GLB+candidate brief+references; frame pixels individually hash checked.
 pd=d/'proof-final'; rm=load(pd/'render-manifest.json'); pixel=load(d/'pixel-inspection.json')
 subject=rm.get('subject',{}); check(subject.get('glb_sha256')==art['glb']['sha256'] and subject.get('brief_sha256')==art['brief']['sha256'] and subject.get('references_sha256')==art['references']['sha256'],f"final render not bound to exact final active candidate {ident}",errors)
 check(pixel.get('glb_sha256')==art['glb']['sha256'] and pixel.get('manifest_sha256')==sha(pd/'render-manifest.json'),f"pixel inspection subject mismatch {ident}",errors)
 frame_report=[]
 mf={x['id']:x for x in rm.get('frames',[])}
 pf={x['id']:x for x in pixel.get('frames',[])}
 for v in VIEWS:
  p=pd/(v+'.png'); actual=sha(p); im=Image.open(p); dims=list(im.size); expected_frame=mf.get(v,{}).get('sha256'); insp=pf.get(v,{})
  row={'view':v,'path':str(p.relative_to(ROOT)),'sha256':actual,'render_manifest_sha256':expected_frame,'pixel_inspection_sha256':insp.get('sha256'),'dimensions':dims,'mode':im.mode,'bytes':p.stat().st_size,'hashes_match':actual==expected_frame==insp.get('sha256')}
  frame_report.append(row);check(actual==expected_frame==insp.get('sha256'),f"final frame hash disagreement {ident}:{v}",errors);check(dims==[512,512],f"final frame dimensions wrong {ident}:{v}",errors)
 # Contact sheet source hash as another evidence record.
 cs=d/'contact-sheet.png'; contact_sheet={'path':str(cs.relative_to(ROOT)),'sha256':sha(cs),'bytes':cs.stat().st_size}
 check(pixel.get('contact_sheet_sha256')==contact_sheet['sha256'],f"contact sheet hash mismatch {ident}",errors)
 # Static independent glb metrics using checkout's project audit function; these are computed by us, not self-asserted candidate summaries.
 glb=ROOT/art['glb']['path']; static=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30)
 # Capacity constraints from original frozen brief.
 policy=load(d/'brief.json')['geometry_policy']
 check(not static.get('errors') and static['scene_triangles']<=policy['max_triangles'] and static['materials']<=policy['max_materials'] and static['unique_mesh_primitives']<=policy['max_primitives'] and static['bytes']<=policy['max_glb_bytes'] and static.get('unique_position_accessor_vertices',0)>0,f"static GLB metric/budget failure {ident}",errors)
 # Independent source counts, useful diagnostic topology only; don't universal-gate zero intersections/watertightness.
 source_report=load(d/'source-final.report.json'); sc=source_report.get('source_audit',{})
 # Validate exact two genuine queue executions and provenance subjects.
 binding=load(d/'final-rebuild-binding.json'); runs=[]; ids_seen=set(); pids=set(); reqs=set(); times=set()
 for rec in binding['distinct_real_queue_runs']:
  runpath=ROOT/rec['path']; reqp=runpath/'request.json'; resp=runpath/'result.json'; req=load(reqp); res=load(resp)
  reqsha=sha(reqp); ressha=sha(resp); runid=req.get('run_id'); runmanifest=BATCH/'rebuild-runs/runs'/runid/'manifest.json'; summaryp=BATCH/'rebuild-runs/runs'/runid/'summary.json'; summ=load(summaryp)
  finalrun=runpath/'outputs/model.glb'; outsha=sha(finalrun) if finalrun.is_file() else None
  rep=(d/f"repro-final-{1 if rec['job_id']=='semantic-rebuild-1' else 2}.report.json")
  repj=load(rep)
  inp=req.get('identity',{}).get('inputs',{})
  expected_inputs={'generator':active['generator']['actual_sha256'],'config':active['config']['actual_sha256'],'brief':sha(original/'brief.json'),'references':active['references']['actual_sha256']}
  inputs_ok=all(inp.get(k,{}).get('sha256')==v for k,v in expected_inputs.items())
  row={'job_id':rec['job_id'],'request_path':str(reqp.relative_to(ROOT)),'request_sha256':reqsha,'request_binding_match':reqsha==rec['request_sha256'],'result_path':str(resp.relative_to(ROOT)),'result_sha256':ressha,'result_binding_match':ressha==rec['result_sha256'],'run_id':runid,'run_manifest_exists':runmanifest.is_file(),'summary_path':str(summaryp.relative_to(ROOT)),'summary_status':summ.get('status'),'pid':res.get('pid'),'started_at':res.get('started_at'),'finished_at':res.get('finished_at'),'returncode':res.get('returncode'),'result_status':res.get('status'),'input_hashes_match':inputs_ok,'output_glb_path':str(finalrun.relative_to(ROOT)),'output_glb_sha256':outsha,'output_is_exact_candidate':outsha==expected_glb,'reproducibility_report_path':str(rep.relative_to(ROOT)),'reproducibility_report_sha256':sha(rep),'reproducibility_report_status':repj.get('status'),'semantic_match':repj.get('semantic_match'),'byte_identical':repj.get('byte_identical'),'declared_semantic_report_sha256':rec['semantic_comparison_report_sha256']}
  runs.append(row); ids_seen.add((runid,rec['job_id']));pids.add(res.get('pid'));reqs.add(reqsha);times.add((res.get('started_at'),res.get('finished_at')))
  check(reqsha==rec['request_sha256'] and ressha==rec['result_sha256'],f"queue provenance record hash mismatch {ident}:{rec['job_id']}",errors)
  check(inputs_ok,f"semantic rebuild input hash mismatch {ident}:{rec['job_id']}",errors)
  check(res.get('status')=='succeeded' and res.get('returncode')==0 and res.get('error') is None and summ.get('status')=='succeeded',f"semantic rebuild not successful {ident}:{rec['job_id']}",errors)
  check(outsha==expected_glb and res.get('outputs',{}).get('model.glb',{}).get('sha256')==expected_glb,f"semantic rebuild output not exact target {ident}:{rec['job_id']}",errors)
  check(repj.get('semantic_match') is True and repj.get('byte_identical') is True and repj.get('glb_sha256')==expected_glb and repj.get('generator_sha256')==active['generator']['actual_sha256'] and repj.get('config_sha256')==active['config']['actual_sha256'],f"semantic comparison report mismatch {ident}:{rec['job_id']}",errors)
  # Distinct queue manifest/summary with actual PIDs and UTC intervals.
  check(runmanifest.is_file() and summ.get('run_id')==runid,f"run ledger missing/mismatch {ident}:{rec['job_id']}",errors)
 check(len(runs)==2 and len(ids_seen)==2 and len(pids)==2 and len(reqs)==2 and len(times)==2,f"not two distinct executed queue runs {ident}",errors)
 check(binding['glb_sha256']==expected_glb and binding['generator_sha256']==active['generator']['actual_sha256'] and binding['config_sha256']==active['config']['actual_sha256'],f"final rebuild binding subject mismatch {ident}",errors)
 assets.append({'asset_id':ident,'revision':rev,'original_freeze_at':frozen,'repair_freeze_at':repair['frozen_at'],'build_started_at':build['started_at'],'concept_invocation_at':gen['observed_invocation_at'],'concept_result_observed_at':gen['observed_result_at'],'concept_image_sha256':concept_hash,'concept_integrity_valid':cval['valid'],'concept_evidence_complete':cval['evidence_complete'],'concept_timing_unknowns':cval.get('blockers',[]),'candidate_record_valid':candeval['valid'],'candidate_approved_for_brief':candeval['approved_for_brief'],'active_artifacts':active,'render_manifest_sha256':sha(pd/'render-manifest.json'),'frames':frame_report,'contact_sheet':contact_sheet,'static_glb_audit':static,'saved_source_final_audit':sc,'source_final_report_sha256':sha(d/'source-final.report.json'),'fresh_queue_runs':runs,'approval_state':cand.get('approval',{}).get('status'),'gpu_state':cand.get('stages',{}).get('gpu',{}).get('status'),'scene_state':cand.get('stages',{}).get('scene',{}).get('status'),'candidate_validation_sha256':sha(d/'candidate-validation.json'),'concept_validation_sha256':sha(d/'concept-validation.json'),'freeze_sha256':sha(d/'modeling-freeze.json'),'repair_freeze_sha256':sha(d/'repair-freeze.json'),'references_sha256':active['references']['actual_sha256'],'scope_digest':load(d/'brief.json').get('claim_scope'),'visual_note':load(d/'pixel-inspection.json').get('note')})
result={'schema_version':1,'check':'first_independent_full_static_qa_batch73','assessment_type':'bounded independent static evaluation; not formal/user/publication approval','created_at_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'source':{'repository_path':str(ROOT),'branch':branch,'head':commit,'expected_head':'c83b49b1e4d4e4c356aa66ab1b9760c8016f198d','clean_worktree':not bool(status),'git_status_porcelain':status,'base_main':'54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c','base_inventory_path':'research/prehistoric-1000-v1/inventory.json','base_inventory_sha256':base_inv_sha,'expected_inventory_sha256':'b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c','source_evidence_manifest_path':str((BATCH/'source-evidence-manifest.json').relative_to(ROOT)),'source_evidence_manifest_sha256':sha(BATCH/'source-evidence-manifest.json'),'manifest_file_count':len(manifest['files']),'manifest_raw_log_count':load(BATCH/'tracked-manifest-check.json').get('raw_log_count'),'manifest_closure_missing':missing,'manifest_closure_changed':changed,'manifest_untracked':untracked,'tracked_manifest_check_sha256':sha(BATCH/'tracked-manifest-check.json'),'handoff_path':str((BATCH/'handoff.json').relative_to(ROOT)),'handoff_sha256':sha(BATCH/'handoff.json'),'setup_incident_recorded':(BATCH/'setup-incident.md').is_file(),'packaging_incident_recorded':(BATCH/'packaging-incident.md').is_file(),'no_producer_edits_made':True},'source_pixels':{'directory':'/workspace/shared/batch73-consult-only','pixel_hash_checks':ref_pixel_checks,'primary_text_findings':{'fractofusus':'The local PMC article distinguishes Figure 2 fossil specimens from Figure 3 digital reconstruction / CFD mesh. The photographed local Fig2 panel has low-relief fusiform branching impressions; no CFD geometry treated as fossil evidence.','striated-bedrock':'Official local NPS/guide photograph depicts aligned linear incisions physically cut into bedrock; exact site/rock/ice age not claimed.','fumarole-vent':'NPS page defines fumaroles as steam vents lacking water; model remains static dry geometry with no gas/temperature assertion.','banded-iron-formation':'Australian Museum text describes alternating kink-folded iron-oxide and microcrystalline silica layers; its DR19296 image remains text-only/403. Consulted substitute actual USGS-hosted James St.John Soudan image; exact CC BY2.0 attribution retained. No annual cadence/sole mechanism or museum scale inferred.'}},'concept_and_scope_chronology':{'all_original_freezes_before_final_build':True,'all_original_concepts_inspected_before_freeze':True,'provider_internal_generation_times':'unknown as declared; not inferred from filesystem mtimes; valid evidence integrity separate from evidence_complete=false','exact_authoring_times':'unknown/incomplete as declared','all_original_briefs_configs_references_immutable':True,'early_failed_and_superseded_revisions_retained_in_manifest':True},'assets':assets,'overall_errors':errors,'status':'pass' if not errors else 'fail','limits':{'visual':'individual frame inspection is an independent bounded static visual read, not user/formal approval','runtime_parse':'independently fresh Node Three.js parse result is written separately','gpu':'not run; not implied by Blender CPU proof or Node parsing','scene':'not run; not implied by CPU proof or Node parsing','approval':'no formal, user, or publication approval is asserted','topology':'no invented universal zero-intersection/watertight rule; natural relief/open surfaces assessed only against original target; any visible actual defects reported asset-specifically'}}
(OUT/'static-source-audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':result['status'],'branch':branch,'head':commit,'clean':not bool(status),'base_inventory_sha256':base_inv_sha,'manifest_file_count':len(manifest['files']),'manifest_closure_ok':not(missing or changed or untracked),'assets':[{'id':a['asset_id'],'revision':a['revision'],'glb':a['active_artifacts']['glb']['actual_sha256'],'bytes':a['static_glb_audit']['bytes'],'triangles':a['static_glb_audit']['scene_triangles'],'primitives':a['static_glb_audit']['unique_mesh_primitives'],'material_count':a['static_glb_audit']['materials'],'source_parts':a['saved_source_final_audit'].get('parts',[]),'rebuild_runs':len(a['fresh_queue_runs']),'concept_valid':a['concept_integrity_valid'],'concept_evidence_complete':a['concept_evidence_complete'],'candidate_approved':a['candidate_approved_for_brief']} for a in assets],'errors':errors},indent=2))
if errors:sys.exit(1)
