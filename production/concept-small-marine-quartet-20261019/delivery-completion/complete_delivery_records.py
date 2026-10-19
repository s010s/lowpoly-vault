# SPDX-License-Identifier: MIT
"""Register existing immutable models and fill measured delivery metadata.
This is a current-time delivery supplement, never a retrospective production freeze.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
REPO=next(p for p in HERE.parents if (p/'scripts/validate_candidate.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
from qa_glb import audit_glb,read_glb
from validate_candidate import validate_candidate

def hash_file(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def descriptor(p):return {'path':p.relative_to(REPO).as_posix(),'sha256':hash_file(p)}
def write(p,value):p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
now=datetime.now(timezone.utc).isoformat()
pins=json.load(open(HERE/'baseline-model-pins.json'))['files']
qa=json.load(open(HERE/'qa-provenance.json'))
selected=json.load(open(BASE/'selected-models.json'))['selected']
summary=[]
for item in selected:
 asset=item['id'];rev=item['revision'];d=BASE/asset/rev;glb=d/(asset+'.glb');blend=d/(asset+'.blend')
 for model in (glb,blend):assert hash_file(model)==pins[model.relative_to(REPO).as_posix()]['sha256']
 audit=audit_glb(glb,max_triangles=16000,max_materials=7,max_primitives=220);doc,binary,raw=read_glb(glb)
 assert not audit['errors'];assert not doc.get('textures',[]) and not doc.get('images',[])
 source=json.load(open(HERE/'evidence'/(asset+'-source.json')));assert source['model_bytes_unchanged']
 assert source['source_export']['glb_sha256']==audit['sha256']
 source_size=source['source']['bounds_blender_m']['size'];expected=[source_size[0],source_size[2],source_size[1]]
 assert max(abs(x-y) for x,y in zip(expected,audit['bounds_m']['size']))<1e-7
 write(HERE/'evidence'/(asset+'-glb-audit.json'),audit)
 metadata=json.load(open(d/'metadata.json'))
 metadata.update(dimensions_m=audit['bounds_m']['size'],dimensions_m_order='glTF X, Y, Z; Y-up; meters',axis={'up':'+Y','forward':'+Z','handedness':'right','source_up':'+Z','source_forward':'-Y','source_to_glb':'(x, y, z) -> (x, z, -y)','verification':'Fresh axis-aware source/export bounds comparison; original explicit Blender export_yup=True contract.'},primitives=audit['scene_primitives_estimated_base_draw_calls'],textures=len(doc.get('textures',[])),texture_count=len(doc.get('textures',[])),images=len(doc.get('images',[])),texture_inventory=[],texture_bytes=0,bytes=len(raw),glb_bytes=len(raw),blend_bytes=blend.stat().st_size,file_bytes={'glb':len(raw),'blend':blend.stat().st_size},exported_position_stream_vertices=audit['unique_position_accessor_vertices'],authored_vertices=source['authored']['vertices'],authored_polygon_faces=source['authored']['polygon_faces'],material_count=audit['materials'],extensions_used=doc.get('extensionsUsed',[]),extensions_required=doc.get('extensionsRequired',[]),candidate_record=(d/'candidate.json').relative_to(REPO).as_posix(),publication_status='unapproved candidate; formal stage acceptance and release remain separate',metadata_completed_at=now,metadata_measurement=descriptor(HERE/'evidence'/(asset+'-glb-audit.json')),source_measurement=descriptor(HERE/'evidence'/(asset+'-source.json')),independent_qa='Limited independent review reported pass at '+qa['qa_commit']+'; this is not formal candidate or physical GPU acceptance.',independent_qa_record=descriptor(HERE/'qa-provenance.json'))
 write(d/'metadata.json',metadata)
 # Preserve the original pre-model design brief and reference ledger, and register
 # a separately dated acceptance-contract supplement. No historical file is changed.
 original=json.load(open(d/'brief.json'));refs=json.load(open(d/'references.json'));config=json.load(open(d/'build-config.json'))
 sources=[]
 for s in refs['sources']:
  sources.append({**s,'license':'Reference-only factual consultation; ROM source imagery/models/code not incorporated or relicensed.','use':'consulted-only; no source media, mesh or texture incorporated','incorporated':False,'rights_note':refs['rights']})
 ledger={'schema_version':1,'registered_at':now,'asset_id':asset,'sources':sources,'original_ledger':descriptor(d/'references.json'),'no_incorporated_third_party_assets':True,'scientific_scope':refs['classification'],'limits':refs['limits']}
 write(d/'candidate-references.json',ledger)
 generator=BASE/('generator-r003.py' if rev=='r003' else 'generator-r002.py')
 artifacts={'glb':descriptor(glb),'source':descriptor(blend),'generator':descriptor(generator),'config':descriptor(d/'build-config.json'),'design_brief':descriptor(d/'brief.json'),'design_references':descriptor(d/'references.json'),'references':descriptor(d/'candidate-references.json'),'metadata':descriptor(d/'metadata.json'),'source_metrics':descriptor(HERE/'evidence'/(asset+'-source.json')),'static_metrics':descriptor(HERE/'evidence'/(asset+'-glb-audit.json'))}
 stages=['technical','visual','factual','specification','runtime_parse','gpu','scene']
 descriptions={
 'technical':'Check the exact GLB format, measured dimensions/counts/bytes, source correspondence and reproducibility against the bound original model/configuration.',
 'visual':'Independent formal evidence review of silhouette, proportions, full volume and material regions against the unchanged original design brief and references.',
 'factual':'Verify only the explicitly stylized external landmarks and retained uncertainty from the ROM source; no specimen-exact, color or phylogeny claim.',
 'specification':'Verify complete source/generator/configuration, provenance, original brief and current delivery registration; no publication authority is implied.',
 'runtime_parse':'Parse the exact GLB with the pinned Three.js loader and bind a formal report; an existing Node parse is supporting evidence only.',
 'gpu':'Target physical device/browser GPU acceptance remains unverified; software SwiftShader is not a physical GPU or performance pass.',
 'scene':'Target deployed/populated gallery scene acceptance remains unverified; the separate software 2x2 QA scene does not establish deployed scene acceptance.'}
 criteria=[{'id':stage+'-acceptance','stage':stage,'critical':True,'description':descriptions[stage],'required_sources':[s['id'] for s in sources] if stage in ('visual','factual') else []} for stage in stages]
 registration={'schema_version':1,'asset_id':asset,'brief_version':rev,'profile':'production','registered_at':now,'registration_only':True,'preproduction_freeze_claim':False,'purpose':'Current-time initial candidate registration for already-built, unchanged models. Original pre-model design brief remains separately pinned. All formal stage decisions remain unknown/pending. This supplement is not a retrospectively frozen design or acceptance claim.','publication_authority':'separate','required_stages':stages,'criteria':criteria,'geometry_policy':{'max_triangles':config['max_triangles'],'max_materials':config['max_materials'],'max_primitives':config['max_primitives'],'max_glb_bytes':config['soft_glb_bytes']},'budget_note':'Copied original explicit geometry ceilings; the original byte target was advisory. This initial unapproved formal registration records that ceiling without claiming pre-production hard-budget acceptance.','texture_policy':{'max_textures':0,'max_dimension':0,'max_total_bytes':0,'max_decoded_bytes':0},'required_deliverables':[{'role':role,**artifacts[role]} for role in ('source','generator','config')],'original_design_brief':descriptor(d/'brief.json'),'original_evidence_coverage':{'required_views':original['required_views'],'turntable_frames':original['turntable_frames'],'scope':'Original frozen bounded-study scope; retained unchanged. Existing exact GLB proof comprises twelve fixed views and no turntable.'},'required_views':['hero','reversehero','front','rear','left','right','top','bottom','clay','clayalt','wire','detail'],'turntable_frames':24,'view_exemptions':{},'coverage_justification':'These are the repository legacy production-profile acceptance obligations, not a claim that new detail/turntable evidence exists. Current original twelve-view/zero-turntable proof remains valid for its bounded scope. Formal profile coverage is unknown and needs the parent formal acceptance process.','scope_limits':refs['limits']}
 write(d/'candidate-brief.json',registration);artifacts['brief']=descriptor(d/'candidate-brief.json')
 technical_evidence={name:descriptor(file) for name,file in {'measured_glb':HERE/'evidence'/(asset+'-glb-audit.json'),'measured_source':HERE/'evidence'/(asset+'-source.json'),'khronos':d/'gltf-validator.report.json','source_export':d/'source-export.report.json','reproducibility_1':d/'reproducibility-1.json','reproducibility_2':d/'reproducibility-2.json','node_parse':d/'threejs-parse.report.json','original_render_manifest':d/'proof/render-manifest.json','original_concept_evidence':d/'concept-evidence.json'}.items()}
 states={stage:{'status':'unknown','reviewer':None,'subject':None,'reviewed_at':None,'evidence':[],'inspected_references':[],'criteria':[{'id':stage+'-acceptance','status':'unknown','evidence':[],'note':'Formal candidate stage not asserted by the maker. See separately hash-pinned raw evidence and independent limited QA provenance.'}],'note':descriptions[stage]+' The limited QA predates these registration supplement hashes and is not promoted or re-signed here.'} for stage in stages}
 states['visual']['inspected_frames']=[]
 candidate={'schema_version':1,'asset_id':asset,'revision':rev,'created_at':now,'maker':{'id':'codex-small-marine-quartet-maker','task_id':'small-marine-quartet-production-20261019'},'artifacts':artifacts,'supersedes':None,'textures':[],'evidence':[],'stages':states,'blockers':[{'id':'formal-stage-acceptance-pending','status':'open','description':'Formal stage reports and independent approval for this initial registration are not asserted. Limited independent QA pass is separately pinned and scoped.'},{'id':'physical-gpu-and-deployed-scene-unknown','status':'open','description':'Physical target GPU/device/performance and deployed populated gallery remain unknown; software WebGL must not substitute.'},{'id':'formal-profile-coverage-unverified','status':'open','description':'Preserved original proof has twelve fixed views and zero turntable frames. Legacy formal production profile detail/orbit coverage has not been provided or asserted.'}],'approval':{'status':'pending'},'publication_authority':'separate','status':'registered-delivery-candidate-not-approved','technical_evidence':technical_evidence,'independent_qa_provenance':{'commit':qa['qa_commit'],'report':descriptor(HERE/'independent-review-source.md'),'provenance':descriptor(HERE/'qa-provenance.json'),'scope':qa['scope']},'measurements':{'dimensions_m':audit['bounds_m']['size'],'triangles':audit['scene_triangles'],'materials':audit['materials'],'primitives':audit['scene_primitives_estimated_base_draw_calls'],'textures':len(doc.get('textures',[])),'images':len(doc.get('images',[])),'glb_bytes':len(raw),'blend_bytes':blend.stat().st_size},'timing_provenance':{'registration_created_at':now,'previous_candidate_registration_time':'unknown; no candidate.json existed at the frozen source commit','original_build_timing':descriptor(d/'build-timing.json'),'original_concept_receipt':descriptor(BASE/'concept-generation.json'),'formal_reviewed_at':None}}
 write(d/'candidate.json',candidate)
 result=validate_candidate(d/'candidate.json',REPO);write(d/'candidate-validation.json',result)
 assert result['valid'] and not result['approved_for_brief'],(asset,result['errors'])
 # The validator independently re-reads the GLB and must agree on all recorded metrics.
 for key in ('triangles','materials','primitives','glb_bytes'):assert result['measurements'][key]==candidate['measurements'][key]
 assert result['measurements']['texture_count']==0
 assert all(candidate['stages'][s]['status']=='unknown' for s in stages)
 for model in (glb,blend):assert hash_file(model)==pins[model.relative_to(REPO).as_posix()]['sha256']
 summary.append({'asset_id':asset,'revision':rev,'candidate':descriptor(d/'candidate.json'),'metadata':descriptor(d/'metadata.json'),'validation':descriptor(d/'candidate-validation.json'),'record_valid':result['valid'],'approved_for_brief':result['approved_for_brief'],'model_hashes_unchanged':True,'glb_sha256':hash_file(glb),'blend_sha256':hash_file(blend),'primitives':audit['scene_primitives_estimated_base_draw_calls'],'textures':0,'glb_bytes':len(raw),'blend_bytes':blend.stat().st_size})
write(HERE/'completion-report.json',{'completed_at':datetime.now(timezone.utc).isoformat(),'source_model_commit':'7c3cc658c1d10fa595e3ef7d27c6f0b17a842dd1','qa_commit':qa['qa_commit'],'scope':'Delivery registration/metadata only. No model, original brief/reference/config, generator or original QA report modified. No formal/hardware or publication approval.','items':summary})
print(json.dumps(summary,indent=2))
