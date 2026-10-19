# SPDX-License-Identifier: MIT
"""Pin actual maker evidence; explicit static profile, independent acceptance pending."""
import json,hashlib,sys,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());b=Path(__file__).resolve().parent;s=sys.argv[1];w=b/s/'r001';attempt=json.loads((w/'config.json').read_text()).get('selected_attempt','attempt-01');d=ROOT/f'assets/candidates/continuous-small-life-round16-20261018/batch-48/{s}/r001/{attempt}/{s}';inputs=ROOT/'production/continuous-small-life-round16-20261018/items'/s
sys.path.insert(0,str(ROOT/'scripts'));from qa_glb import audit_glb

def read(p):return json.loads(p.read_text())
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
a=audit_glb(d/(s+'.glb'),14000,6,30);assert not a['errors'] and a['bytes']<=1000000
source=read(w/'source-scene.json');cmp=read(w/'source-export.json');rebuild=read(w/'reproducibility.json');single=read(d/'runtime/single.json');scene=read(d/'runtime/scene.json');validator=read(d/'gltf-validator.report.json')
assert not validator['issues']['numErrors'] and not validator['issues']['numWarnings'];assert source['status']=='pass' and cmp['triangles_match'] and cmp['bounds_match'];assert rebuild['status']=='pass'
assert single['status']==scene['status']=='pass' and single['glb_sha256']==scene['glb_sha256']==a['sha256'];assert scene['instances']==6 and scene['views'][0]['triangles']==a['scene_triangles']*6
meta=read(d/'metadata.json');meta.update(status='candidate-awaiting-independent-QA',source_authored_vertices=source['source_authored_vertices'],source_evaluated_vertices=source['source_evaluated_vertices'],exported_position_stream_vertices=a['unique_position_accessor_vertices'],exported_materials=a['materials'],exported_primitives=a['scene_primitives_estimated_base_draw_calls'],texture_metrics={'count':0,'encoded_bytes':0,'decoded_bytes':0},reference_access_supplement=ref(b/'reference-access.json'),attribution={'en':'Leon Made This / s010s — CC-BY-4.0; generator code MIT','zh':'Leon Made This / s010s 署名；模型/渲染 CC-BY-4.0，生成代码 MIT'},independent_qa={'status':'pending','dispatcher':'parent','model':'GPT-6 Luna','reasoning':'xhigh'})
put(d/'metadata.json',meta)
views=['hero','reversehero','front','side','rear','top','clay','silhouette'];sp=[d/f'preview-{v}.png' for v in views];rp=[d/'runtime'/v['path'] for q in [single,scene] for v in q['views']]
def sheet(paths,out):
 im=Image.new('RGB',(1600,435*((len(paths)+3)//4)),'#e8e4dc');draw=ImageDraw.Draw(im)
 for k,p in enumerate(paths):
  src=Image.open(p).convert('RGBA');src.thumbnail((400,400));x=k%4*400;y=k//4*435;im.paste(src,(x+(400-src.width)//2,y+(400-src.height)//2),src);draw.text((x+10,y+410),s+' / '+p.stem,fill='#30434b')
 im.save(out,quality=93)
sheet(sp,d/'source-contact-sheet.jpg');sheet(rp,d/'runtime-contact-sheet.jpg')
for p in sp:
 im=Image.open(p);assert im.mode=='RGBA'
 if 'silhouette' not in p.name:assert im.getchannel('A').getextrema()[0]==0
manifest={'schema_version':1,'asset_id':s,'revision':'r001','glb_sha256':a['sha256'],'turntable_frames':0,'source_render':{'engine':'Blender4.3.2 Cycles CPU','threads':2,'resolution':512,'samples':16,'color':'Standard/None/exposure0/gamma1','framing':'asset_common.py per-view projected-bound fit','directions_blender':{'hero':[.574,-.819,.466],'reversehero':[-.574,.819,.466],'front':[0,-1,0],'side':[1,0,0],'rear':[0,1,0],'top':[0,0,1],'clay':[.574,-.819,.466],'silhouette':[.574,-.819,.466]}},'runtime_render':{'renderer':single['renderer'],'three':'0.180.0','extent_px':[80,160,240,480],'tone_mapping':'None','output':'sRGB','camera_and_lighting_source':ref(b/'viewer.html')},'frames':[dict(ref(p),width=Image.open(p).width,height=Image.open(p).height,origin='source' if p in sp else 'exact-glb-runtime') for p in sp+rp],'sheets':[ref(d/'source-contact-sheet.jpg'),ref(d/'runtime-contact-sheet.jpg')],'review_state':'maker pixel inspection separate; independent acceptance pending'}
put(d/'view-manifest.json',manifest)
notes={'facivermis': 'Original whole lobopodian teaching form: five pairs of restrained spine-bearing anterior arms, long bare trunk and integrated expanded posterior attachment; no full unsupported tube or feeding animation.', 'cave-pearl-pool': 'Original shallow mineral cup has genuine concavity and a few unequal rounded discrete concretions, with readable gaps/contact; not eggs, mechanical sphere array or crystal cluster.', 'lava-tree-mold-crust': 'Original continuous lava crust encloses a deep negative trunk-shaped cavity with integral chilled lining and restrained bark-like relief. No black-painted log, freestanding hollow column, additional tree asset or species/locality/age inference.', 'treptichnus-serial-probe-burrow': 'Original sectional-structure: a zigzag main route connects serial short angled J-shaped probes, with genuine exposed internal junctions. No stretched palmate relief, dense network, producer or exact behavior claim.'}

qa=read(d/'qa.json');qa.update(threejs_runtime=single,representative_scene=scene,source_reopen=ref(w/'source-scene.json'),source_export=ref(w/'source-export.json'),reproducibility=ref(w/'reproducibility.json'),previews={'status':'maker pixel inspection recorded; independent acceptance pending','views':views,'manifest':ref(d/'view-manifest.json')},visual_review={'status':'maker_self_review_only','observations':notes[s],'independent_qa':'pending parent Luna xhigh'},warning_disposition={'smooth_normals':'Intentional organic smooth surfaces; rock uses restrained mixed smooth/faceted relief. Closed semantic parts may overlap at original organic/rock connections; inspected with default backface culling.','scale':'Metric nominal art scale and identity placement root; each source has a documented floor or static-display mounting low point. No measured fossil-size claim.','habitat':meta['habitat'],'claim_scope':meta['claim_scope']})
put(d/'qa.json',qa)
# Explicit versioned execution ledger: normalize consultation usage only, never invent a license.
ledger=read(inputs/'references.json');ledger['original_frozen_ledger']=ref(inputs/'references.json');ledger['normalization_note']='Execution-only schema normalization: use=consulted-only. Original source usage text and access history retained; no media license inferred and frozen planner ledger unchanged.'
for source_entry in read(b/'reference-access.json')['sources']:
 if source_entry.get('asset_id')==s and source_entry.get('id'):
  ledger['sources'].append({'id':source_entry['id'],'title':source_entry['title'],'url':source_entry['url'],'use':'consulted-only','verification':source_entry['status'],'supports':source_entry['scope'],'rights_note':'Facts consulted only; no source media incorporated.'})
for source_entry in ledger['sources']:
 source_entry['incorporated']=False;source_entry['original_use']=source_entry.get('use');source_entry['use']='consulted-only'
put(w/'references.execution.json',ledger)
artifacts={k:ref(p) for k,p in {'glb':d/(s+'.glb'),'source':d/(s+'.blend'),'generator':w/'generator.py','config':w/'config.json','brief':inputs/'brief.json','references':w/'references.execution.json','frozen_references':inputs/'references.json','mesh_utils':b/'mesh_utils.py','helper':ROOT/'scripts/asset_common.py','audit':ROOT/'scripts/qa_glb.py','source_inspector':b/'inspect_source.py','runtime_viewer':b/'viewer.html','runtime_checker':b/'browser_qa.mjs','verification_runner':b/'verify_item.py','package_lock':ROOT/'package-lock.json','reference_access':b/'reference-access.json','claim':b/'claim.json','inventory':inputs/'inventory-record.json','review_policy':ROOT/'production/continuous-small-life-round16-20261018/review-policy.json'}.items()}
evidence={k:ref(p) for k,p in {'khronos':d/'gltf-validator.report.json','source_scene':w/'source-scene.json','source_export':w/'source-export.json','two_rebuilds':w/'reproducibility.json','runtime':d/'runtime/single.json','scene':d/'runtime/scene.json','views':d/'view-manifest.json','metadata':d/'metadata.json','qa':d/'qa.json'}.items()}
record=read(ROOT/'schemas/templates/candidate.template.json');record.update(asset_id=s,revision='r001',maker={'id':'GPT-6.1 Sol medium','task_id':'01a15056-509d-725f-bad0-871371cd7010'},artifacts={k:{field:v[field] for field in ['path','sha256']} for k,v in artifacts.items()},textures=[],technical_evidence=evidence,status='maker-candidate-awaiting-independent-QA',publication_authority='separate',blockers=[{'id':'independent-acceptance-pending','description':'Parent must dispatch fresh independent Luna xhigh acceptance. Measured maker checks are separately pinned, not promoted to independent stage approval.','status':'open'}],approval={'status':'pending'})
brief=read(inputs/'brief.json')
for stage,entry in record['stages'].items():
 entry['criteria']=[{'id':x['id'],'status':'unknown','evidence':[],'note':'Pending formal stage acceptance; actual maker measurements are separately pinned in technical_evidence.'} for x in brief['criteria'] if x['stage']==stage];entry['note']='Formal stage acceptance pending; no independent PASS asserted by maker.'
put(w/'candidate.json',record)
put(w/'freeze.json',{'schema_version':1,'asset_id':s,'revision':'r001','final_attempt':attempt,'files':artifacts,'evidence':evidence,'candidate':ref(w/'candidate.json'),'independent_acceptance':'pending','source_plan_commit':'ebc011b6fad1988ee66ac32efb8e706bf5c95c76','base_main':'de413ef720463a2999516faf92c606bcdf9ab1b7'})
cmd=['python3','scripts/candidate_profile.py',str((w/'candidate.json').relative_to(ROOT)),'--root',str(ROOT)]
with (w/'profile-contract.json').open('w') as f:subprocess.run(cmd,cwd=ROOT,stdout=f,check=True)
if (w/'profile-gate.json').exists() and not (w/'profile-raw-ledger.json').exists():
 put(w/'profile-raw-ledger.json',read(w/'profile-gate.json'))
for mode,args in [('legacy-gate',[]),('profile-gate',['--profile','static-stylized-v1','--profile-contract',str(w/'profile-contract.json')])]:
 with (w/(mode+'.json')).open('w') as f:result=subprocess.run(['python3','scripts/validate_candidate.py',str(w/'candidate.json'),'--root',str(ROOT),*args,'--json'],cwd=ROOT,stdout=f)
 q=read(w/(mode+'.json'));print(mode,result.returncode,q.get('valid'),q.get('profile_contract_status'),q.get('errors'))
print(s,a['sha256'],a['bytes'],a['scene_triangles'])
