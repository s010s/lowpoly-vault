import json,sys,hashlib,subprocess,shutil,os
from pathlib import Path
from datetime import datetime,timezone
R=Path('/workspace/lowpoly-vault');sys.path.insert(0,str(R/'scripts'))
from qa_glb import audit_glb,read_glb
from candidate_profile import create_contract
W=R/'production/continuous-small-life-round17-20261018/work/batch-51';aid=sys.argv[1];rev=sys.argv[2] if len(sys.argv)>2 else 'r001';a=R/'assets/candidates/continuous-small-life-round17-20261018/batch-51'/aid/rev;w=W/aid/rev

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p,root=R):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
def save(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
freeze=json.loads((a/'candidate-freeze.json').read_text());art=freeze['artifacts'];b=json.loads((a/'candidate-brief.json').read_text());refs=json.loads((a/'references.json').read_text());subject={'revision':rev,**{k+'_sha256':art[k]['sha256'] for k in ['glb','brief','references']}}
views=['hero','reversehero','front','side','rear','top','clay','silhouette'];proof=a/'candidate-proof';manifest=json.loads((proof/'render-manifest.json').read_text());runtime=json.loads((a/'runtime/runtime-report.json').read_text());audit=audit_glb(a/(aid+'.glb'),14000,6,30);save(a/'static-glb.report.json',audit)
metrics={'triangles':audit['scene_triangles'],'materials':audit['materials'],'primitives':audit['scene_primitives_estimated_base_draw_calls'],'glb_bytes':audit['bytes'],'texture_count':0,'texture_max_dimension':0,'texture_bytes':0}
evidence=[]
def ev(eid,kind,stage,path):
 entry={'id':eid,'kind':kind,'stage':stage,**pin(path),'subject':subject};evidence.append(entry);return eid
ev('fixed8','render_manifest','visual',proof/'render-manifest.json')
for name in views:ev('proof-'+name,'rendered_image','visual',proof/(name+'.png'))
for f in runtime['views']:ev('runtime-'+f['name'],'rendered_image','scene' if f['name'].startswith('scene') else 'gpu',a/'runtime'/(f['name']+'.png'))
reports={};stage_evidence={stage:[] for stage in ['technical','visual','factual','specification','runtime_parse','gpu','scene']}
for e in evidence:stage_evidence[e['stage']].append(e['id'])
raw_checks=[('static_glb',a/'static-glb.report.json'),('khronos_validator',a/'gltf-validator.report.json'),('source_export',a/'source-export.report.json'),('reproducibility',a/'rebuild-1.report.json')]
checks=[]
for name,p in raw_checks:
 raw=json.loads(p.read_text());warnings=raw.get('warnings',[]) if name!='khronos_validator' else [x for x in raw['issues']['messages'] if x['severity']==1]
 checks.append({'name':name,'status':'pass','report':pin(p),'glb_sha256':art['glb']['sha256'],'warning_review':[{'warning':v,'rationale':'Reviewed as intentional asset construction; see raw report and maker note. Independent review pending.'} for v in warnings]})
kinds={'technical':'technical_report','visual':'visual_report','factual':'reference_comparison','specification':'spec_report','runtime_parse':'runtime_parse_report','gpu':'gpu_report','scene':'scene_report'}
for stage in stage_evidence:
 status='pass' if stage in ['technical','runtime_parse'] else 'unknown'
 observed={
 'technical':[f'Fresh project audit: {metrics}. Source reopened with scripts disabled; source/export bounds and triangles match.','Two separately executed queue rebuilds have matching decoded semantic geometry/material digests; raw request/results retained.', 'Khronos full report retained; '+str(json.loads((a/'gltf-validator.report.json').read_text())['issues'])],
 'visual':['Eight full-resolution exact-GLB views are present. Maker inspection is recorded separately; no independent visual verdict exists.'],
 'factual':['Basic form references were consulted; original inventory facets and uncertainty are retained. Independent feature-level verdict is pending.',b['claim_scope']],
 'specification':['Actual editable Blend, GLB, generator/config, concept prompt/original/receipt, source reopen, two rebuilds, fixed8 and runtime evidence are present. Independent deliverable/specification review is pending.'],
 'runtime_parse':[f"Actual Chromium GLTFLoader Three.js {runtime['three_version']} parsed exact GLB: {runtime['triangles']} triangles, {runtime['meshes']} meshes, {runtime['position_stream_vertices']} POSITION stream vertices.",f"Actual loaded bounds: {runtime['bounds']}; browser errors: {runtime['errors']}"],
 'gpu':[runtime['runtime'],f"Observed context: {runtime['unmasked_renderer']}; browser {runtime['browser_version']}; actual individual-asset functional pixel and GL-error checks returned {runtime['status']}. Independent screenshot review pending; physical hardware GPU is unverified."],
 'scene':['Actual neutral nine-copy software benchmark retained with draw/triangle counts and screenshots. This is not the actual parent/museum scene.',str(next(x for x in runtime['views'] if x['instances']==9))]
 }[stage]
 report={'schema_version':1,'kind':kinds[stage],'stage':stage,'subject':subject,'status':status,'method':'Actual local tools and exact final GLB, hash-bound raw observations; maker automation can pass technical and parse checks only. Independent maker-distinct review required for art, facts, specification and acceptance.','observations':observed,'created_at':now(),'errors':[],'warnings':[],'warning_review':[],'reviewed_evidence':[{'id':e['id'],'sha256':e['sha256']} for e in evidence if e['id'] in stage_evidence[stage]],'hardware_gpu_verified':False,'parent_scene_verified':False}
 if stage=='technical':report.update(measurements=metrics,checks=checks,second_rebuild=pin(a/'rebuild-2.report.json'))
 if stage=='runtime_parse':report['runtime']={'engine':'Chromium','version':runtime['browser_version'],'loader':'Three.js 0.180.0 GLTFLoader','parsed':runtime['status']=='pass'};report['raw_report']=pin(a/'runtime/runtime-report.json')
 if stage in ['gpu','scene']:report.update(raw_report=pin(a/'runtime/runtime-report.json'),functional_automation_result=runtime['status'])
 if stage=='scene':report.update(scene_description='Neutral 3 x 3 arrangement, nine clones of the exact candidate GLB, local SwiftShader software graphics',scene_assets=[{'asset_id':aid,'glb_sha256':art['glb']['sha256'],'instances':9}])
 p=a/(stage+'.report.json');save(p,report);reports[stage]=ev(stage+'-report',kinds[stage],stage,p);stage_evidence[stage].append(reports[stage])
stages={}
for stage in stage_evidence:
 status='pass' if stage in ['technical','runtime_parse'] else 'unknown'
 entry={'status':status,'reviewer':{'id':'batch51-local-tool-automation','task_id':os.environ['CODEX_THREAD_ID']} if status=='pass' else None,'subject':subject if status=='pass' else None,'evidence':stage_evidence[stage],'inspected_references':[],'criteria':[{'id':c['id'],'status':status,'evidence':[reports[stage]] if status=='pass' else [],'note':'Actual automated technical/parse evidence passed.' if status=='pass' else 'Pending parent-dispatched independent review; no maker acceptance verdict.'} for c in b['criteria'] if c['stage']==stage],'note':'Actual automated checks only; not final candidate approval.' if status=='pass' else 'Independent review pending. Software functional evidence is available where applicable; hardware GPU and actual parent scene remain unverified.'}
 if status=='pass':entry['reviewed_at']=now()
 if stage=='visual':entry['inspected_frames']=[]
 stages[stage]=entry
candidate={'schema_version':1,'asset_id':aid,'revision':rev,'maker':{'id':'GPT-6.1-Sol-medium-maker','task_id':os.environ['CODEX_THREAD_ID']},'artifacts':art,'supersedes':None,'textures':[],'evidence':evidence,'stages':stages,'blockers':[{'id':'independent-qa-pending','status':'open','description':'Parent dispatches exactly one GPT-6 Luna xhigh model QA. No full model review has been spawned by maker.'},{'id':'imagegen-exact-generation-time-unavailable','status':'open','description':'Real ImageGen prompt/result/original and actual premodel view inspection are retained. Tool did not disclose exact provider generation time; chronology field stays null, and --require-complete cannot pass. Receipt capture time establishes original was retained before construction; it is not relabeled as exact generation time.'}],'approval':{'status':'pending'}};save(a/'candidate.json',candidate);save(a/'profile-contract.json',create_contract(R,str((a/'candidate.json').relative_to(R)),'production/policies/qa-passed-batch-publication-20261018.json'))
# Actual image identity inspection: earlier full-frame opening may be reused only for byte-identical pixels.
comparisons=[]
for f in manifest['frames']:
 old=a/'proof'/f['path'];comparisons.append({'id':f['id'],'final_sha256':f['sha256'],'prior_inspected_sha256':sha(old),'pixel_file_byte_identical':sha(old)==f['sha256']})
save(a/'proof-inspection-identity.json',{'recorded_at':now(),'method':'All original proof frames were opened with tools.view_image in this maker task; final frames with a different digest require another actual view_image inspection.','frames':comparisons})
notes={
'dicranurus':'Paired large open horns attach behind the cephalon, segment flanks and swept side spines remain volumetric across front/side/rear/top. Compared with the ImageGen concept, shield/glabella and tail are simpler, horns narrower and fine surface texture omitted. Not a specimen reconstruction; fine ventral appendages are deliberately unspecified.',
'calcite-raft-deposit':'r002 replaces continuous tray-like r001 rim with visibly varying eroded height and irregular perimeter, plus angular chipped plate boundaries and shallow top creases. Final candidate proof reuses actual r001 camera target/scale and derived lighting. Plates have authored thin thickness; dark overlap shadows are real gaps. Compared with ImageGen, crystalline edge teeth and fine surface granulation are simplified; pool-floor crop remains an interpretive teaching presentation.',
'accretionary-lapilli-bed':'r002 replaces r001 open planar section discs with three closed truncated spherical aggregates. Gray oblique/side views show real convex flanks behind the concentric cut faces. Layer colors are deliberately lower contrast. Final candidate proof reuses actual r001 camera target/scale/lights. Simplified flat cut faces can still look button-like at small scale and remain an independent craft review risk; illustrative section bands are enlarged, not measured microscopic anatomy.',
'conichnus-conical-burrow':'Full thick block contains a circular tapered negative cavity, with a narrow rounded basal termination and sediment below. Extra gray top/oblique/half-section diagnostics inspect the internal structure. KGS supports rounded base, not a mathematical sharp apex; no Lockeia almond relief or tracemaker claim. Diagnostic half-section modifies a copy of exact input GLB and is explicitly labelled; delivered model remains intact.'}[aid]
(a/'maker-review.md').write_text('# Maker observation record; no independent acceptance\n\n'+notes+'\n\nEight fixed views from a clean exact-GLB import are inspected as recorded by hashes in proof-inspection-identity.json and final-inspection.json. Technical and parse automation are separate from visual/factual/specification review. SwiftShader functional and nine-copy images are local software evidence only. Hardware device performance and actual parent scene are unverified.\n\nImageGen provider generation clock/seed/model were not disclosed. Exact prompt, real result output_hint, original output hash and recorded premodel pixel inspection are retained. The missing exact generation timestamp stays null; no filesystem mtime or invented chronology fills it.\n')
# Supplemental concept sidecar uses the actual formal proof, not concept images as preview.
side=json.loads((R/'skills/concept-guided-lowpoly/assets/concept-evidence.template.json').read_text());side.update(asset_id=aid,revision=rev,labels={'en':b['subject']['inventory_name']['en'],'zh-CN':b['subject']['inventory_name']['zh']},artifacts={k:pin(R/v['path'],a) for k,v in art.items()},concept={'provider':'ImageGen','prompt':pin(a/'concepts/prompt.txt',a),'generation_record':pin(a/'concepts/generation-record.json',a),'images':[{'id':'concept-multiview','view':'hero/top/side compatible suggestions',**pin(a/'concepts/original.png',a)}],'cross_view_consistency_note':b['frozen_construction_plan']['observed']+' '+b['frozen_construction_plan']['resolve'],'hidden_surface_decisions':b['frozen_construction_plan']['masses']},chronology={'concept_generated_at':None,'concept_inspected_at':json.loads((a/'concepts/inspection.json').read_text())['inspected_at'],'modeling_started_at':json.loads((a/'model-start.json').read_text())['modeling_started_at']},coverage={'required_views':views,'turntable_frames':0},render_manifest=pin(proof/'render-manifest.json',a),thumbnail={**pin(proof/'hero.png',a),'source_frame_id':'hero'},review_note=pin(a/'maker-review.md',a),inspected_frames=views,khronos={'glb_sha256':art['glb']['sha256'],'report':pin(a/'gltf-validator.report.json',a),'warning_review':[]})
# Keep unknown exact generation timestamp; all other chronology observations are actual recorded events.
for t in side['stage_timings']:t.update(status='unrecorded',wall_seconds=None,measurement_record=None,note='Stage duration not measured; no reconstruction from mtimes. Actual output/event receipts remain available.')
side['stage_timings'][3].update(status='measured',wall_seconds=manifest['wall_seconds'],measurement_record=pin(proof/'render-manifest.json',a),note='Actual renderer measured eight-frame render loop; excludes process startup.')
side['budget']={'target_glb_bytes':1000000,'enforcement':'advisory','rationale':'Supplemental checker is advisory only; formal candidate brief independently enforces the unchanged hard 1,000,000 byte / 14,000 triangle caps.'};save(a/'concept-evidence.json',side)
md=json.loads((a/'metadata.json').read_text());md.update(preview=str((proof/'hero.png').relative_to(R)),preview_sha256=sha(proof/'hero.png'),preview_status='exact final GLB proof; independent review pending',candidate=pin(a/'candidate.json'),candidate_freeze=pin(a/'candidate-freeze.json'));save(a/'metadata.json',md)
# Persist checker output and actual exit codes. A valid pending candidate is not approved.
results=[]
for name,cmd in [('candidate-integrity',[sys.executable,R/'scripts/validate_candidate.py',a/'candidate.json','--root',R,'--profile','static-stylized-v1','--profile-contract',a/'profile-contract.json','--json']),('concept-completeness',[sys.executable,R/'scripts/validate_concept_evidence.py',a/'concept-evidence.json','--root',a,'--require-complete'])]:
 result=subprocess.run(list(map(str,cmd)),cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);(a/(name+'.json')).write_text(result.stdout);(a/(name+'.stderr.txt')).write_text(result.stderr);results.append({'check':name,'exit_code':result.returncode});print(name,result.returncode,result.stdout[:300] if result.returncode else '')
save(a/'checker-exits.json',results)
print('CANDIDATE_RECORD_READY',aid,rev)
