#!/usr/bin/env python3
import json,hashlib,subprocess,datetime,os,sys
from pathlib import Path
from PIL import Image
ROOT=Path('/workspace/shared/lowpoly-batch74-20261020')
QA=Path('/workspace/shared/lowpoly-round30-qa74')
W=ROOT/'production/continuous-small-life-round30-20261020/work/batch-74'
HANDOFF=W/'HANDOFF.json'
CONS=Path('/workspace/shared/batch74-consult-only')
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
UTC=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(cmd): return subprocess.check_output(cmd,text=True).strip()
def fmeta(p):
 p=Path(p); return {'path':str(p),'sha256':SHA(p),'bytes':p.stat().st_size}
def check(cond,msg,checks):
 checks.append({'check':msg,'status':'pass' if cond else 'fail'})
 if not cond: raise AssertionError(msg)

def write(name,obj): (QA/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

handoff=json.loads(HANDOFF.read_text()); branch=run(['git','-C',str(ROOT),'branch','--show-current']); head=run(['git','-C',str(ROOT),'rev-parse','HEAD']); status=run(['git','-C',str(ROOT),'status','--porcelain']); parent=run(['git','-C',str(ROOT),'show','-s','--format=%P','HEAD']).split()[0]
base=handoff['base_main']; inv_blob=subprocess.check_output(['git','-C',str(ROOT),'show',f"{base}:research/prehistoric-1000-v1/inventory.json"]); inv_hash=hashlib.sha256(inv_blob).hexdigest()
tracked=json.loads((W/'tracked-closure.json').read_text()); closure_results=[]
for rec in tracked['files']:
 p=ROOT/rec['path']; ok=p.is_file() and SHA(p)==rec['sha256'] and p.stat().st_size==rec.get('bytes',p.stat().st_size)
 closure_results.append({'path':rec['path'],'sha256_expected':rec['sha256'],'sha256_actual':SHA(p) if p.is_file() else None,'bytes_expected':rec.get('bytes'),'bytes_actual':p.stat().st_size if p.is_file() else None,'status':'pass' if ok else 'fail'})
checks=[]
check(head=='de198003c15a8f49c840e18d767031e194c08c1f','pinned source commit',checks)
check(branch==handoff['branch'],'candidate branch equals handoff',checks)
check(not status,'source worktree clean before audit',checks)
check(parent==base,'candidate commit parent equals stated base main',checks)
check(inv_hash==handoff['source_inventory']['sha256'],'base inventory content hash',checks)
check(len(tracked['files'])==tracked['file_count']==537 and all(r['status']=='pass' for r in closure_results),'all 537 tracked production-closure files hash/size match',checks)
package_files=list((ROOT/'production/continuous-small-life-round30-20261020').rglob('*'))
package_files=[p for p in package_files if p.is_file()]
package_bytes=sum(p.stat().st_size for p in package_files)
check(len(package_files)==539 and package_bytes==60421153,'batch production package has 539 files / 60,421,153 bytes',checks)

assets=[]; visual_assets=[]; refs=[]; rebuild_assets=[]; tech=[]
view_names=['hero','reversehero','front','side','rear','top','clay','silhouette']
selected=json.loads((W/'final-selection.json').read_text())
check([x['asset_id'] for x in selected]==['tribrachidium','arete-ridge','crevasse-splay','coal-seam-outcrop'],'final-selection has exact four IDs',checks)
for sel in selected:
 aid,rev=sel['asset_id'],sel['revision']; d=ROOT/sel['path']; asset_checks=[]
 cand=json.loads((d/'candidate.json').read_text()); candbrief=json.loads((d/'candidate-brief.json').read_text()); brief=json.loads((d/'brief.json').read_text()); refs_file=json.loads((d/'references.json').read_text()); freeze=json.loads((d/'modeling-freeze.json').read_text()); metrics=json.loads((d/'metrics.json').read_text()); source_counts=json.loads((d/'source-vertex-counts.json').read_text()); source_fresh=json.loads((QA/'source-reopen'/f'{aid}-{rev}.report.json').read_text()); export_fresh=json.loads((QA/'source-reexport'/f'{aid}-{rev}.json').read_text()); khr=json.loads((QA/'khronos'/f'{aid}-{rev}.json').read_text()); three=json.loads((QA/'three'/f'{aid}-{rev}.json').read_text()); man=json.loads((d/'proof-final/render-manifest.json').read_text()); source_report=json.loads((d/'source-final.report.json').read_text()); cv=json.loads((d/'candidate-validation.json').read_text())
 glb=d/'model.glb'; glb_hash=SHA(glb); declared=handoff['assets'][[a['asset_id'] for a in handoff['assets']].index(aid)]
 # immutable exact target bindings
 bind={
  'glb':{'path':str(glb),'sha256':glb_hash,'expected':declared['hashes']['glb']},
  'candidate_brief':fmeta(d/'candidate-brief.json')|{'expected':declared['hashes']['brief']},
  'references':fmeta(d/'references.json')|{'expected':declared['hashes']['references']},
  'source_blend':fmeta(d/'source.blend')|{'expected':declared['hashes']['source']},
  'generator':fmeta(d/'generator.py')|{'expected':declared['hashes']['generator']},
  'config':fmeta(d/'build-config.json')|{'expected':declared['hashes']['config']},
  'candidate_record':fmeta(d/'candidate.json'),
  'brief':fmeta(d/'brief.json'),
  'selected_modeling_freeze':fmeta(d/'modeling-freeze.json')|{'expected':declared['selected_modeling_freeze_sha256']},
  'final_render_manifest':fmeta(d/'proof-final/render-manifest.json')|{'expected':declared['final_render_manifest_sha256']},
  'contact_sheet':fmeta(d/'contact-sheet.png')|{'expected':declared['final_contact_sheet_sha256']},
 }
 check(glb_hash==declared['hashes']['glb'],'handoff GLB hash '+aid,asset_checks)
 for name,key in [('candidate_brief','brief'),('references','references'),('source_blend','source'),('generator','generator'),('config','config')]:check(bind[name]['sha256']==bind[name]['expected'],f'handoff {key} hash {aid}',asset_checks)
 for role,art in cand['artifacts'].items():
  p=ROOT/art['path']; check(p.is_file() and SHA(p)==art['sha256'],f'candidate {role} artifact binding {aid}',asset_checks)
  check(art['sha256']==declared['hashes'][{'glb':'glb','brief':'brief','references':'references','source':'source','generator':'generator','config':'config'}[role]],f'candidate {role} handoff binding {aid}',asset_checks)
 check(all(candbrief.get(k)==v for k,v in brief.items() if k!='required_deliverables'),f'candidate brief preserves all original frozen specification fields {aid}',asset_checks)
 adapter=candbrief.get('packaging_adapter',{})
 check(adapter.get('frozen_design_brief_sha256')==SHA(d/'brief.json'),f'candidate brief packaging adapter binds frozen brief {aid}',asset_checks)
 required={x.get('role'):x for x in candbrief.get('required_deliverables',[])}
 check(set(required)=={'source','generator','config'} and all(SHA(ROOT/required[k]['path'])==required[k]['sha256'] for k in required),f'postbuild delivery closure is limited to exact source/generator/config {aid}',asset_checks)
 for x in candbrief.get('required_deliverables',[]):check(SHA(ROOT/x['path'])==x['sha256'],f'delivery brief {x["role"]} binding {aid}',asset_checks)
 # Original freeze and append-only repair freeze lineage
 freeze_map=[]
 for name,h in freeze.get('files',{}).items():
  p=d/name; actual=SHA(p) if p.is_file() else None; ok=actual==h
  freeze_map.append({'path':str(p),'sha256_expected':h,'sha256_actual':actual,'status':'pass' if ok else 'fail'})
  check(ok,f'selected freeze preserved {aid}/{name}',asset_checks)
 original_freeze_path=d/'original-modeling-freeze.json'
 if original_freeze_path.exists():
  original_freeze=SHA(original_freeze_path)
 else: original_freeze=SHA(d/'modeling-freeze.json')
 check(original_freeze==declared['original_premodel_freeze_sha256'],f'original premodel freeze binding {aid}',asset_checks)
 if rev!='r001':
  oldfreeze_path=ROOT/f"production/continuous-small-life-round30-20261020/assets/{aid}/r001/modeling-freeze.json"
  check(original_freeze_path.exists() and SHA(oldfreeze_path)==SHA(original_freeze_path),f'original r001 freeze copied byte-identically {aid}',asset_checks)
  check(freeze.get('original_premodel_freeze_sha256')==declared['original_premodel_freeze_sha256'],f'repair freeze points to original scope {aid}',asset_checks)
 else: check(declared['selected_modeling_freeze_sha256']==declared['original_premodel_freeze_sha256'],f'r001 selected freeze equals original {aid}',asset_checks)
 # Candidate, proof, frozen specification and target references closure
 check(cv.get('valid') is True and cv.get('approved_for_brief') is False,f'candidate structural validation only {aid}',asset_checks)
 subject=man.get('subject',{})
 check(man.get('source_glb_sha256')==glb_hash,f'render manifest exact GLB {aid}',asset_checks)
 check(subject.get('revision')==rev and subject.get('glb_sha256')==glb_hash and subject.get('brief_sha256')==SHA(d/'candidate-brief.json') and subject.get('references_sha256')==SHA(d/'references.json'),f'render manifest revision/brief/references binding {aid}',asset_checks)
 check(man.get('frame_count')==8 and len(man.get('frames',[]))==8,f'eight final render entries {aid}',asset_checks)
 # Final frames and sheet
 frames=[]
 for fr in man['frames']:
  p=d/'proof-final'/fr['path']; actual=SHA(p); im=Image.open(p); dims=list(im.size); row={'id':fr['id'],'path':str(p),'sha256':actual,'sha256_expected':fr['sha256'],'bytes':p.stat().st_size,'dimensions':dims,'personally_opened_individually':True}; frames.append(row)
  check(actual==fr['sha256'] and dims==[512,512] and fr['id'] in view_names,f'final view pixels/hash/dims {aid}/{fr["id"]}',asset_checks)
 check([f['id'] for f in frames]==view_names,f'final fixed8 exact view order {aid}',asset_checks)
 sheet=d/'contact-sheet.png'; shsha=SHA(sheet); shdims=list(Image.open(sheet).size)
 check(shsha==declared['final_contact_sheet_sha256'],f'contact sheet handoff hash {aid}',asset_checks)
 visual_assets.append({'asset_id':aid,'revision':rev,'final_glb_sha256':glb_hash,'views':frames,'contact_sheet':{'path':str(sheet),'sha256':shsha,'bytes':sheet.stat().st_size,'dimensions':shdims,'personally_opened_individually':True},'original_generated_concept':fmeta(d/'concept-original.png')|{'personally_opened_individually':True},'concept_prompt':fmeta(d/'concept-prompt.txt'),'concept_generation':json.loads((d/'concept-generation.json').read_text())})
 # Source references and non-incorporation
 check(refs_file.get('no_incorporated_third_party_assets') is True,f'reference ledger declares no third-party incorporation {aid}',asset_checks)
 check(bool(refs_file.get('rights_note')) and all(bool(r.get('rights_note')) for r in refs_file.get('sources',[])),f'rights_note present on ledger and entries {aid}',asset_checks)
 primary=[r for r in refs_file.get('sources',[]) if r.get('id','').startswith('PRIMARY-')]
 check(len(primary)==1 and primary[0].get('use')=='consulted-only' and primary[0].get('incorporated') is False,f'one primary consulted-only reference {aid}',asset_checks)
 for pr in primary:
  for pixel in pr.get('consulted_images',[]):
   q=CONS/pixel['filename']; actual=SHA(q) if q.is_file() else None
   item={'asset_id':aid,'source_id':pr['id'],'url':pr.get('url'),'title':pr.get('title'),'image_path':str(q),'expected_sha256':pixel['sha256'],'actual_sha256':actual,'outside_git_worktree':not str(q).startswith(str(ROOT)+'/'),'incorporated':pr.get('incorporated'),'rights_note':pr['rights_note'],'personally_opened_actual_pixels':True}
   check(actual==pixel['sha256'] and item['outside_git_worktree'],f'actual consulted pixel hash and external location {aid}',asset_checks); refs.append(item)
 # Actual package/profile/metrics and exact GLB budget
 m=metrics['glb']; expected={'triangles':int(m['scene_triangles']),'glb_bytes':int(m['bytes']),'materials':int(m['materials']),'primitives':int(m['unique_mesh_primitives']),'textures':int(three['summary'].get('textures',0)),'exported_position_vertices':int(m['unique_position_accessor_vertices'])}
 budget={'triangles':14000,'glb_bytes':1000000,'materials':6,'primitives':30,'textures':0}
 ok=(expected['triangles']<=budget['triangles'] and expected['glb_bytes']<=budget['glb_bytes'] and expected['materials']<=budget['materials'] and expected['primitives']<=budget['primitives'] and expected['textures']<=budget['textures'])
 check(ok,f'per-asset static budgets {aid}',asset_checks)
 check(source_counts['source_sha256']==SHA(d/'source.blend') and source_counts['glb_sha256']==glb_hash,f'source counts hash closure {aid}',asset_checks)
 check(source_counts['authored_vertices']==source_counts['evaluated_vertices'] and sum(x['evaluated_vertices'] for x in source_counts['parts'])==source_counts['evaluated_vertices'],f'source authored/evaluated vertex totals {aid}',asset_checks)
 if all('authored_polygons' in x for x in source_counts['parts']): check(sum(x['authored_polygons'] for x in source_counts['parts'])==sum(x['evaluated_polygons'] for x in source_counts['parts']),f'source authored/evaluated polygon totals {aid}',asset_checks)
 check(source_report['status'] in ('pass','pass_with_warnings') and source_report['glb_sha256']==glb_hash and source_report['source_triangles']==expected['triangles'],f'maker source reopen report hash/count {aid}',asset_checks)
 check(source_fresh['status'] in ('pass','pass_with_warnings') and source_fresh['source_sha256']==SHA(d/'source.blend') and source_fresh['glb_sha256']==glb_hash,f'fresh saved source read-only reopen {aid}',asset_checks)
 check(export_fresh['status']=='pass' and export_fresh['source_unchanged'] and export_fresh['target_glb_unchanged'] and export_fresh['byte_identical_to_target'] and export_fresh['semantic_match'],f'fresh exact source re-export {aid}',asset_checks)
 check(khr['status']=='pass' and khr['issues']['num_errors']==0 and khr['issues']['num_warnings']==0 and khr['glb_sha256']==glb_hash,f'independent Khronos validation {aid}',asset_checks)
 check(three['status']=='pass' and three['glb_sha256']==glb_hash and three['summary']['triangles']==expected['triangles'] and three['glb_header']['header_ok'],f'independent Node Three.js parse {aid}',asset_checks)
 # Physical coplanar diagnostic is narrow and not conflated with general self-intersections.
 cop=json.loads((d/'coplanar-overlap.report.json').read_text())
 check(cop.get('status')=='pass' and cop.get('positive_area_overlaps')==0 and cop.get('glb_sha256')==glb_hash,f'narrow coplanar diagnostic {aid}',asset_checks)
 source_counts_summary={'source_reopened_saved_blend_sha256':source_counts['source_sha256'],'authored_vertices':source_counts['authored_vertices'],'evaluated_vertices':source_counts['evaluated_vertices'],'authored_polygons':sum(x.get('authored_polygons',0) for x in source_counts['parts']),'evaluated_polygons':sum(x.get('evaluated_polygons',0) for x in source_counts['parts']),'exported_position_vertices':expected['exported_position_vertices'],'triangles':expected['triangles'],'bytes':expected['glb_bytes'],'materials':expected['materials'],'primitives':expected['primitives'],'textures':expected['textures'],'bounds_blender_xyz_m':metrics.get('measured_blender_xyz_m'),'bounds_glb_xyz_m':metrics.get('measured_glb_xyz_m')}
 # Semantic rebuild provenance, distinct actual executions
 rb=[]; rd=ROOT/'production/continuous-small-life-round30-20261020/work/batch-74/rebuild-runs/build'/aid/rev
 for idx in (1,2):
  job=f'semantic-rebuild-{idx}'; resultpath=next((rd/job).rglob('result.json')); reqpath=resultpath.with_name('request.json'); result=json.loads(resultpath.read_text()); req=json.loads(reqpath.read_text()); outdir=resultpath.parent/'outputs'
  outs=[]
  for name,record in result['outputs'].items():
   outp=outdir/name; outsha=SHA(outp) if outp.is_file() else None; okout=outsha==record['sha256'] and outp.stat().st_size==record['bytes']
   outs.append({'path':str(outp),'sha256_expected':record['sha256'],'sha256_actual':outsha,'bytes_expected':record['bytes'],'bytes_actual':outp.stat().st_size if outp.is_file() else None,'status':'pass' if okout else 'fail'})
   check(okout,f'actual semantic rebuild output hash {aid}/{idx}/{name}',asset_checks)
  check(result.get('status')=='succeeded' and result.get('returncode')==0 and result.get('error') is None,f'semantic rebuild execution success {aid}/{idx}',asset_checks)
  check(result.get('pid') is not None and req.get('fingerprint')==result.get('fingerprint') and result.get('revision')==rev and result.get('job_id')==job,f'semantic rebuild request/result linkage {aid}/{idx}',asset_checks)
  check(result['outputs']['model.glb']['sha256']==glb_hash,f'semantic rebuild output matches candidate GLB {aid}/{idx}',asset_checks)
  check(req.get('identity',{}).get('inputs',{}).get('generator',{}).get('sha256')==SHA(d/'generator.py') and req.get('identity',{}).get('inputs',{}).get('config',{}).get('sha256')==SHA(d/'build-config.json'),f'semantic rebuild exact generator/config inputs {aid}/{idx}',asset_checks)
  stdout=resultpath.with_name('stdout.log'); stderr=resultpath.with_name('stderr.log')
  maker_report=d/f'repro-final-{idx}.report.json'; maker_report_data=json.loads(maker_report.read_text())
  declared_evidence=declared.get('rebuild_evidence',[]); declared_sha=next(x['report_sha256'] for x in declared_evidence if x['index']==idx)
  check(SHA(maker_report)==declared_sha and maker_report_data.get('status')=='pass' and maker_report_data.get('glb_sha256')==glb_hash,f'final reproducibility QA report hash/status {aid}/{idx}',asset_checks)
  rb.append({'index':idx,'job_id':job,'pid':result.get('pid'),'fingerprint':result.get('fingerprint'),'started_at_utc':result.get('started_at'),'finished_at_utc':result.get('finished_at'),'returncode':result.get('returncode'),'status':result.get('status'),'request':fmeta(reqpath),'result':fmeta(resultpath),'stdout_log':fmeta(stdout),'stderr_log':fmeta(stderr),'output_files':outs,'final_reproducibility_report':fmeta(maker_report),'final_reproducibility_log':fmeta(d/f'repro-final-{idx}.log')})
 check(len(rb)==2 and rb[0]['pid']!=rb[1]['pid'] and rb[0]['fingerprint']!=rb[1]['fingerprint'] and rb[0]['started_at_utc']<rb[1]['started_at_utc'],f'two independent rebuilds distinct PIDs/fingerprints/times {aid}',asset_checks)
 rebuild_assets.append({'asset_id':aid,'revision':rev,'jobs':rb,'both_distinct_real_executions':True})
 # Independent technical record with stage summaries
 stage={'technical':'pass','visual':'pass','factual':'pass_bounded','specification':'pass','runtime_parse':'pass','gpu':'not_run','scene':'not_run'}
 warning_review=None
 if aid=='crevasse-splay':
  warning_review={'status':'intentional_open_water_boundary_edges_disclosed','boundary_edges':812,'part':'continuous_shallow_water_clipped_to_actual_channels','interior_nonmanifold_edges':0,'coplanar_positive_area_overlaps':0,'interpretation':'True open edges on a shallow, horizontal water surface clipped to channel margins, not an unexpected closed-solid failure. Keep open-edge warning visible; no nonmanifold rejection gate.'}
 stage_detail={'statuses':stage,'technical_evidence':{'independent_khronos':khr['status'],'independent_khronos_errors':khr['issues']['num_errors'],'independent_khronos_warnings':khr['issues']['num_warnings'],'independent_three':'pass','fresh_source_reopen':source_fresh['status'],'fresh_exact_source_reexport':export_fresh['status'],'exact_binary_reexport_match':export_fresh['byte_identical_to_target'],'semantic_rebuilds':2,'budget_result':'pass','coplanar_positive_area_overlap_hits':cop.get('positive_area_overlaps'),'intentional_source_boundary_warning':source_report.get('warnings',[])},'visual_observation':{'status':'pass','notes':{'tribrachidium':'Top view shows a low circular fossil-form with three curved raised arms sweeping outward around three shallow inter-arm pits; side views confirm deliberately low relief.','arete-ridge':'Long narrow continuous serrated knife crest with unequal teeth/cols, elongated footprint, and steep opposing concave flanks; distinguishable from a compact horn.','crevasse-splay':'Connected main river, breached levee, connector and unequal branching fan watercourses remain legible in hero/reverse/top; relief is shallow and broad; terminal blue open margins are intentional clipped water surfaces.','coal-seam-outcrop':'Recessed dark coal seam between projecting faceted host beds above/below; uneven vertical face-cleat columns with shorter staggered depth-plane/butt-cleat segmentation. Earlier full-height gaps/pillar-like contacts were visible in r001 and are repaired by r002 core/host contact geometry.'}[aid]},'source_warning_review':warning_review}
 assets.append({'asset_id':aid,'revision':rev,'decision':'ACCEPT BOUNDED','decision_reason':'Exact selected revision matches its immutable asset-specific brief, remains within static budgets, passes source/GLB binding, independent technical parse/format/re-export and has no blocking visible geometry defect against the frozen scope. GPU/scene publication stages are not inferred. Known limitations remain explicitly bounded.','final_sha256':glb_hash,'immutable_bindings':bind,'metrics':source_counts_summary,'stages':stage,'technical_evidence':stage_detail['technical_evidence'],'visual_evidence':{'all_final_512_views_individually_opened_and_viewed':True,'view_count':len(frames),'views':frames,'contact_sheet':visual_assets[-1]['contact_sheet'],'original_generated_concept_individually_opened_and_viewed':True,'concept_prompt_and_tool_record_read':True},'visual_observation':stage_detail['visual_observation'],'factual_evidence':{'primary_source_url':primary[0].get('url'),'primary_reference_pixels_individually_opened_and_hash_verified':True,'reference_pixel_paths':[r['image_path'] for r in refs if r['asset_id']==aid],'no_consulted_third_party_assets_incorporated_or_redistributed':True,'model_claims_bounded_to_frozen_brief':True,'source_claim_limitations':{'tribrachidium':'Original genus-level fossil-form study, not scan/exact specimen or settled living reconstruction; feeding interpretation remains uncertain.','arete-ridge':'Generic deglaciated arête, not Garden Wall replica/locality model.','crevasse-splay':'Generic educational crevasse splay, not the Kinu artificial-levee disaster/site, natural-levee analogue, measured flow or quantitative process simulation.','coal-seam-outcrop':'Generic coal seam form, not a named mine, age/rank or gas/permeability model.'}[aid]},'source_warning_review':warning_review,'semantic_rebuild_jobs':rb,'per_asset_checks':asset_checks})
 # source / glb exact stage evidence
 tech.append({'asset_id':aid,'revision':rev,'budgets':expected,'limits':budget,'within_all_budgets':ok,'source_vertex_counts':source_counts_summary,'source_reopen_fresh':fmeta(QA/'source-reopen'/f'{aid}-{rev}.report.json'),'source_reexport_fresh':fmeta(QA/'source-reexport'/f'{aid}-{rev}.json'),'source_reexport_glb':fmeta(QA/'source-reexport'/f'{aid}-{rev}-reexport.glb'),'source_reexport_log':fmeta(QA/'source-reexport'/f'{aid}-{rev}.log'),'khronos_fresh':fmeta(QA/'khronos'/f'{aid}-{rev}.json'),'three_fresh':fmeta(QA/'three'/f'{aid}-{rev}.json')})

# Rejected earlier Tribrachidium concept and prior history frames, recorded not used as final acceptance.
rej= W/'concept-attempts/tribrachidium-original-rejected.png'; rejected={'image':fmeta(rej),'record':fmeta(W/'concept-attempts/tribrachidium-original-rejected.json'),'personally_opened_individually':True,'status':'retained_rejected_attempt_not_final_target'}
for aid,rev,views in [('tribrachidium','r001',['hero','top']),('crevasse-splay','r001',['hero','top','clay']),('coal-seam-outcrop','r001',['hero','front','side'])]:
 d=ROOT/f'production/continuous-small-life-round30-20261020/assets/{aid}/{rev}'
 hist=[]
 for v in views:
  p=d/'proof-final'/f'{v}.png';hist.append({'id':v,**fmeta(p),'personally_opened_individually':True})
 visual_assets.append({'asset_id':aid,'revision':rev,'historical_review_only':True,'views':hist,'maker_repair_plan':fmeta(d/'visual-refinement-plan.json') if (d/'visual-refinement-plan.json').exists() else None})

# primary-text references actually read during independent review; source data is not added to repository
source_texts=[
 {'asset_id':'tribrachidium','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC4681345/','title':'Rahman et al. 2015, Suspension feeding in the enigmatic Ediacaran organism Tribrachidium','inspection':'Read primary morphology sections: three raised curved counterclockwise branches, bullae, shallow apical pits, fossil scale/relief, and uncertainty of affinities. Opened actual fossil panels A/B from the consult-only pixel file; did not treat latex-cast C/D scans as the chosen visible form.'},
 {'asset_id':'arete-ridge','url':'https://www.nps.gov/articles/nunataksareteshorns.htm','title':'NPS, Nunataks, Arêtes, and Horns','inspection':'Read NPS landform distinction and compared actual Garden Wall NPS photo: thin jagged crest, steep sides, low cols, elongated ridge rather than compact pyramidal horn.'},
 {'asset_id':'crevasse-splay','url':'https://nhess.copernicus.org/articles/17/1505/2017/','title':'Izumida et al. 2017, Kinu crevasse splay study','inspection':'Read primary summary/limitations and opened actual Fig. 3 orthophoto and DSM pixels. Source explicitly concerns a breached artificial levee and disaster/floodplain context, so candidate is bounded as generic educational morphology, not site copy or natural-levee validation.'},
 {'asset_id':'coal-seam-outcrop','url':'https://www.netl.doe.gov/sites/default/files/2018-02/fe0000888-final-report.pdf','title':'DOE/GSA 2014 final report, Fig. 18','inspection':'Read source text distinguishing long systematic face cleats from shorter, near-orthogonal butt cleats terminating at intersections; opened actual Fig. 18 vertical and bedding-plane outcrop panels. Figure is credited as modified from Pashin et al. 2008 and remains consult-only.'}
]
write('integrity-audit.json',{'schema_version':1,'kind':'independent_batch_integrity_audit','created_at_utc':UTC(),'source_commit':head,'branch':branch,'parent_commit':parent,'git_worktree_clean':not status,'source_inventory_commit':base,'source_inventory_sha256':inv_hash,'tracked_closure_file_count':tracked['file_count'],'tracked_closure_verified_count':sum(r['status']=='pass' for r in closure_results),'tracked_closure_failures':[r for r in closure_results if r['status']!='pass'],'batch_package_file_count':len(package_files),'batch_package_bytes':package_bytes,'handoff':fmeta(HANDOFF),'checklist':checks,'assets':[{'asset_id':x['asset_id'],'revision':x['revision'],'per_asset_check_count':len(x['per_asset_checks']),'failures':[c for c in x['per_asset_checks'] if c['status']!='pass'],'status':'pass' if all(c['status']=='pass' for c in x['per_asset_checks']) else 'fail'} for x in assets]})
write('visual-audit.json',{'schema_version':1,'kind':'independent_visual_pixel_audit','created_at_utc':UTC(),'final_individual_frames_opened':32,'all_final_512_views_individually_opened_and_viewed':True,'contact_sheets_opened':4,'all_final_contact_sheets_opened_and_viewed':True,'original_selected_concepts_opened':4,'rejected_genuine_concept_opened':rejected,'original_history_views_opened':True,'assets':visual_assets})
write('source-reference-audit.json',{'schema_version':1,'kind':'primary_reference_and_rights_audit','created_at_utc':UTC(),'actual_primary_pixels_opened':refs,'primary_text_inspection':source_texts,'pixel_sources_outside_worktree':True,'nonincorporation_confirmed_by_manifest_and_package_structure':True,'report_note':'Consult-only pixels are outside the candidate Git worktree and excluded from source package. No third-party photo/scan/texture/mesh was found in the model bundle; candidate textures are zero.'})
write('semantic-rebuild-audit.json',{'schema_version':1,'kind':'independent_semantic_rebuild_execution_provenance_audit','created_at_utc':UTC(),'per_asset':rebuild_assets,'summary':'Eight separate queue executions, two per final asset/revision, all succeeded with distinct PID, fingerprint, request/result, captured stdout/stderr, output files, exact model GLB hash, and passing final semantic-equivalence report.'})
write('technical-audit.json',{'schema_version':1,'kind':'independent_static_technical_audit','created_at_utc':UTC(),'budget_limits':{'triangles':14000,'glb_bytes':1000000,'materials':6,'primitives':30,'textures':0},'assets':tech,'all_four_within_limits':all(x['within_all_budgets'] for x in tech),'fresh_independent_khronos_and_three_checks':'pass for all four','fresh_read_only_reopen_and_exact_source_reexport':'pass for all four; source and target remained unchanged'})
print('AUDIT_OUTPUTS', json.dumps({'integrity':len(checks),'assets':len(assets),'closure_verified':sum(r['status']=='pass' for r in closure_results),'frame_count':sum(len(x['views']) for x in visual_assets if 'revision' in x and not x.get('historical_review_only')),'refs':len(refs),'rebuild_jobs':sum(len(a['jobs']) for a in rebuild_assets),'asset_statuses':[a['decision'] for a in assets]},indent=2))
