import pathlib,json,hashlib,datetime,subprocess,sys,os,struct
from PIL import Image,ImageChops
sys.dont_write_bytecode=True
R=pathlib.Path('/workspace/shared/lowpoly-batch92-20261020');P=R/'production/batch92';O=pathlib.Path('/workspace/shared/lowpoly-batch92-independent-qa-20261020');C=pathlib.Path('/workspace/shared/lowpoly-round39-coordination')
sys.path.insert(0,str(R/'scripts'))
from validate_candidate import validate_candidate
from validate_concept_evidence import validate as validate_concept
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
J=lambda p:json.loads(pathlib.Path(p).read_text())
T=lambda x:datetime.datetime.fromisoformat(x.replace('Z','+00:00'))
checks=[];input_manifest={}
def record(p):
 p=pathlib.Path(p);input_manifest[str(p)]={'bytes':p.stat().st_size,'sha256':H(p)};return H(p)
def check(name,ok,detail=None):checks.append(dict(name=name,pass_=bool(ok),detail=detail));checks[-1]['pass']=checks[-1].pop('pass_')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();parent=subprocess.check_output(['git','rev-parse','HEAD^'],cwd=R,text=True).strip();branch=subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip();status=subprocess.check_output(['git','status','--porcelain'],cwd=R,text=True)
check('fixed commit',commit=='37ddf403430e4859d077163855ecdf6e1aa2b0ba');check('fixed direct parent',parent=='43e40fc89f2b369a5f1858e72fa58a0d10318124');check('clean input tree',status=='')
check('handoff sha',record(P/'HANDOFF.md')=='9ba01fc13dab168591a4bc870bd79995498e379c65f81c8c2ccd56fae7d0237f');check('assets sha',record(P/'handoff-assets.json')=='df25a0e4f2303c65d32fcf5dff025a89c39bfceaa3cd0138b6280a1ed3e8da62')
for name in ['batch-92-claim.json','batch-92-selected-inventory.json','batch-92-concept-plan-requirements.json']:
 check('unchanged original dispatch '+name,record(P/name)==record(C/name))
freeze=J(P/'original-freeze-manifest.json');record(P/'original-freeze-manifest.json');ft=T(freeze['frozen_at']);author=J(P/'generator-authoring-record.json');record(P/'generator-authoring-record.json')
check('recorded freeze before observed generator completion',ft<T(author['observed_completed_at']))
check('selected inventory frozen hash',record(P/'batch-92-selected-inventory.json')==freeze['original_inventory_sha256'])
assets=[];triplets=[]
for h in J(P/'handoff-assets.json'):
 a=h['asset_id'];d=R/h['path'];out=O/a;before=len(checks)
 paths={'glb':'model.glb','brief':'candidate-brief.json','references':'references.json','source':'source.blend','generator':'generator.py','config':'build-config.json'}
 for k,n in paths.items():check(a+' exact '+k,record(d/n)==h['hashes'][k])
 triplet={k+'_sha256':h['hashes'][k] for k in ['glb','brief','references']};triplet['revision']=h['revision'];triplets.append({'asset_id':a,'commit':commit,**triplet})
 for n,m in freeze['assets'][a].items():check(a+' frozen '+n,record(R/m['path'])==m['sha256'])
 orig=J(d.parent/'r001/brief.json');brief=J(d/'candidate-brief.json');refs=J(d/'references.json');pre=J(d/'preproof-binding.json');man=J(d/'proof-final/render-manifest.json');ce=J(d/'concept-evidence.json');record(d/'preproof-binding.json');record(d/'proof-final/render-manifest.json');record(d/'proof-final/render-config.json');record(d/'geometry-semantics.json');record(d/'execution.json')
 check(a+' all original frozen design fields unchanged',all(brief[k]==v for k,v in orig.items()))
 check(a+' final local brief equals original freeze',record(d/'brief.json')==freeze['assets'][a]['brief.json']['sha256'])
 check(a+' final references equals original freeze',h['hashes']['references']==freeze['assets'][a]['references.json']['sha256'])
 check(a+' packaging only added closure',set(brief)-set(orig)=={'required_deliverables','packaging_adapter'})
 for dep,hh in J(d/'build-dependencies.json')['inputs'].items():check(a+' dependency '+dep,record(R/dep)==hh)
 check(a+' pinned npm lock',record(R/'package-lock.json')==J(d/'build-dependencies.json')['node_lockfile_sha256'])
 for ref in refs['sources']:
  check(a+' rights '+ref['id'],bool(ref.get('rights_note')) and ref.get('incorporated') is False)
  for f in ref['consult_only_files']:check(a+' source file '+f['path'],record(f['path'])==f['sha256'])
 concept=J(d/'concept-generation.json');record(d/'concept-generation.json');record(d/'concept-prompt.txt');record(d/'concept-original.png')
 check(a+' original concept bytes retained',H(d/'concept-original.png')==record(P/'concepts'/f'{a}-concept.png'))
 check(a+' observed concept before freeze',T(concept['observed_returned_at'])<=T(concept['actual_pixel_inspection_at'])<=ft)
 check(a+' executed geometry after freeze',ft<T(J(d/'execution.json')['started_at']))
 life=[json.loads(t) for t in (d/'lifecycle.jsonl').read_text().splitlines()];record(d/'lifecycle.jsonl')
 proof=next(x for x in life if x['stage']=='proof-final')
 check(a+' adapter and preproof before proof invocation',T(brief['packaging_adapter']['created_at'])<=T(pre['checked_at'])<T(proof['started_at']))
 check(a+' preproof exact subject',all(pre[k]==v for k,v in triplet.items() if k!='revision'))
 check(a+' all final pixels exact subject',man['subject']==triplet)
 check(a+' final proof execution success',proof['exit_code']==0 and T(proof['started_at'])<T(man['created_at'])<=T(proof['ended_at']))
 for event in life:check(a+' lifecycle log '+event['stage'],record(event['log'])==event['log_sha256'])
 check(a+' required distinct frames',set(f['id'] for f in man['frames'])=={'hero','reversehero','front','side','rear','top','clay','silhouette'} and len(man['frames'])==8)
 sheet=Image.open(d/'contact-sheet.png').convert('RGB');record(d/'contact-sheet.png');frames=[]
 for i,f in enumerate(man['frames']):
  pix=d/'proof-final'/f['path'];im=Image.open(pix).convert('RGB');check(a+' frame '+f['id'],record(pix)==f['sha256'] and im.size==(512,512))
  crop=sheet.crop((i%4*512,i//4*540+28,i%4*512+512,i//4*540+540));same=ImageChops.difference(crop,im).getbbox() is None;check(a+' lossless sheet tile '+f['id'],same)
  frames.append({'id':f['id'],'path':str(pix),'sha256':H(pix),'pixels':[512,512],'lossless_sheet_tile_exact':same})
 rebuild=[]
 for i in [1,2]:
  q=P/'rebuild-evidence'/a/h['revision']/f'semantic-rebuild-{i}';ident=J(q/'byte-identity.json');raw=pathlib.Path(ident['original_run_dir']);req=J(q/'request.json');res=J(q/'result.json');ex=J(q/'execution.json');record(q/'byte-identity.json')
  for n,hh in ident['files'].items():
   rp=raw/('outputs/'+n if n=='execution.json' else n)
   check(a+f' rebuild{i} snapshot '+n,record(q/n)==hh and record(rp)==hh)
  for n,f in res['outputs'].items():check(a+f' rebuild{i} actual output '+n,record(raw/'outputs'/n)==f['sha256'] and (raw/'outputs'/n).stat().st_size==f['bytes'])
  for name,f in req['identity']['inputs'].items():check(a+f' rebuild{i} input '+name,record(f['path'])==f['sha256'])
  check(a+f' rebuild{i} binary',H(req['identity']['executable']['path'])==req['identity']['executable']['sha256'])
  check(a+f' rebuild{i} raw successful process',res['status']=='succeeded' and res['returncode']==0 and res['pid']==ex['pid'] and req['argv']==ex['argv'] and req['fingerprint']==res['fingerprint'])
  check(a+f' rebuild{i} ordered execution',ft<T(req['created_at'])<=T(res['started_at'])<=T(ex['started_at'])<T(ex['finished_at'])<=T(res['finished_at'])<T(pre['checked_at']))
  check(a+f' rebuild{i} exact final GLB',H(raw/'outputs/model.glb')==h['hashes']['glb'])
  check(a+f' rebuild{i} generator/config executed',ex['generator_sha256']==h['hashes']['generator'] and ex['config_sha256']==h['hashes']['config'])
  check(a+f' rebuild{i} stdout actual built hash',h['hashes']['glb'] in (q/'stdout.log').read_text() and 'BUILT '+a in (q/'stdout.log').read_text())
  rebuild.append({'job':i,'pid':ex['pid'],'original_run_dir':str(raw),'started_at':ex['started_at'],'finished_at':ex['finished_at'],'request_sha256':H(q/'request.json'),'result_sha256':H(q/'result.json'),'execution_sha256':H(q/'execution.json'),'output_glb_sha256':H(raw/'outputs/model.glb')})
 check(a+' genuinely distinct rebuild run identities',rebuild[0]['pid']!=rebuild[1]['pid'] and rebuild[0]['original_run_dir']!=rebuild[1]['original_run_dir'])
 candidate=J(d/'candidate.json');cv=validate_candidate(d/'candidate.json',root=R,validation_profile='static-stylized-v1',profile_contract=d/'profile-contract.json');(out/'candidate-validation.json').write_text(json.dumps(cv,indent=2)+'\n')
 ev=validate_concept(d/'concept-evidence.json',d);(out/'concept-validation.json').write_text(json.dumps(ev,indent=2)+'\n')
 check(a+' fresh candidate schema valid unapproved',cv['valid'] and not cv['approved_for_brief']);check(a+' fresh concept valid with disclosed incomplete times',ev['valid'] and not ev['evidence_complete'])
 si=J(out/'source-inspection.json');rt=J(out/'runtime-parse.json');kh=J(out/'khronos.json');pa=si['project_audit']
 check(a+' fresh source reopen reexport and actual numeric checks',si['status']=='pass')
 check(a+' fresh runtime and Khronos',rt['status']=='pass' and kh['report']['issues']['numErrors']==0 and kh['report']['issues']['numWarnings']==0)
 check(a+' actual runtime/source/GLB counts agree',rt['triangles']==pa['scene_triangles']==sum(x['evaluated_triangles'] for x in si['parts']) and rt['exported_position_vertices']==pa['unique_position_accessor_vertices'])
 check(a+' budget',pa['scene_triangles']<=14000 and pa['bytes']<=1000000 and pa['materials']<=6 and pa['scene_primitives_estimated_base_draw_calls']<=30)
 glb=(d/'model.glb').read_bytes();js=json.loads(glb[20:20+struct.unpack_from('<I',glb,12)[0]])
 check(a+' no textures animations skins or image planes',not js.get('textures') and not js.get('images') and not js.get('animations') and not js.get('skins'))
 check(a+' materials opaque single sided',all(m.get('alphaMode','OPAQUE')=='OPAQUE' and not m.get('doubleSided',False) for m in js['materials']))
 assets.append({'asset_id':a,'revision':h['revision'],'subject':triplet,'source_hashes':h['hashes'],'frames':frames,'rebuilds':rebuild,'fresh_checks_pass':all(x['pass'] for x in checks[before:]),'check_count':len(checks)-before,'counts':{'authored_vertices':sum(x['authored_vertices'] for x in si['parts']),'evaluated_vertices':sum(x['evaluated_vertices'] for x in si['parts']),'triangles':rt['triangles'],'exported_position_vertices':rt['exported_position_vertices'],'glb_bytes':pa['bytes'],'materials':pa['materials'],'primitives':pa['scene_primitives_estimated_base_draw_calls']},'world_blender_xyz_m':si['authored_world_bounds'],'world_glb_xyz_m':rt['world_bounds'],'chronology':{'freeze':freeze['frozen_at'],'concept_observed_return':concept['observed_returned_at'],'concept_inspection':concept['actual_pixel_inspection_at'],'generator_first_authoring_start':'unknown','provider_internal_generation_timestamp':'unknown','observed_generator_completed_at':author['observed_completed_at'],'final_geometry_execution':J(d/'execution.json')['started_at'],'derived_brief_closed_at':brief['packaging_adapter']['created_at'],'preproof_bound_at':pre['checked_at'],'proof_invocation_at':proof['started_at'],'proof_manifest_complete_at':man['created_at']}})
result={'kind':'fresh-independent-full-batch-chain-audit','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':commit,'source_parent':parent,'source_branch':branch,'source_status':status,'all_checks_pass':all(c['pass'] for c in checks),'checks_count':len(checks),'checks':checks,'assets':assets,'limitations':['Recorded process and historical timing evidence is an auditable attestation, not cryptographic proof of chronology. Exact modeling-authoring start and provider internal image timestamp remain unknown. No times inferred from filesystem metadata.','Rebuild raw outputs were independently hashed and checked, not rebuilt a third and fourth time. Each source was freshly reopened and actually reexported in this QA.']}
(O/'chain-audit.json').write_text(json.dumps(result,indent=2)+'\n');(O/'input-manifest.json').write_text(json.dumps(input_manifest,indent=2)+'\n');(O/'exact-triplets.json').write_text(json.dumps(triplets,indent=2)+'\n');print(json.dumps({'passed':result['all_checks_pass'],'count':len(checks),'failed':[c for c in checks if not c['pass']]}))
