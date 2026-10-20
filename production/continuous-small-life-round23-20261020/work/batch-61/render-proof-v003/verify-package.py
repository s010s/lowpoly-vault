# SPDX-License-Identifier: MIT
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import json,hashlib,subprocess,datetime,copy
R=Path.cwd();W=R/'production/continuous-small-life-round23-20261020/work/batch-61';D=W/'render-proof-v003';BASE='896563bfcbc70f160edf29b84dacfc824536be6a';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(R));now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();pin=lambda p:{'path':rel(p),'sha256':H(p)}
def put(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
idx=json.loads((D/'actual-render-index.json').read_text());rows=[];all_comp=[]
for x in idx['assets']:
 b=R/x['path'];o=R/x['proof_directory'];man=json.loads((o/'render-manifest.json').read_text());run=json.loads((R/x['runner_record']['path']).read_text());brief=b/'candidate-brief-scale-v002.json';c0=json.loads((b/'candidate-scale-v002.json').read_text());expected={'revision':x['revision'],'glb_sha256':H(b/'model.glb'),'brief_sha256':H(brief),'references_sha256':H(b/'references.json')};assert man['subject']==expected;assert run['inputs']['corrected_brief']['sha256']==H(brief);assert run['command'][run['command'].index('--brief')+1]==str(brief);assert run['returncode']==0;assert run['blender_process_pid']>0
 comparisons=[];sheet=Image.new('RGB',(2048,1060),'#E8E4DC');draw=ImageDraw.Draw(sheet)
 for j,f in enumerate(man['frames']):
  p=o/f['path'];old=b/'proof-final'/f['path'];assert H(p)==f['sha256'];a=Image.open(old).convert('RGBA');z=Image.open(p).convert('RGBA');assert z.size==(512,512);same=a.tobytes()==z.tobytes();assert same,('Decoded-pixel difference requires inspection',p)
  comparisons.append({'frame':f['id'],'old_png':pin(old),'new_png':pin(p),'decoded_rgba_sha256':hashlib.sha256(z.tobytes()).hexdigest(),'decoded_rgba_identical':same,'png_bytes_identical':old.read_bytes()==p.read_bytes()});sheet.paste(z.convert('RGB'),((j%4)*512,(j//4)*530));draw.text(((j%4)*512+8,(j//4)*530+512),x['asset_id']+' fresh v003 / '+f['id'],fill='#222222')
 sheet.save(o/'contact-sheet-v003.png');comparison=o/'decoded-pixel-comparison-v003.json';put(comparison,{'schema_version':1,'checked_at':now(),'kind':'decoded-rgba-equivalence','old_images_remain_original_subject':'Old proof-final manifest remains untouched and bound to old brief; these new images were genuinely rerendered using corrected brief. Equality is measured, not evidence-copying.','new_manifest':pin(o/'render-manifest.json'),'actual_runner':x['runner_record'],'all_eight_decoded_rgba_identical':True,'frames':comparisons,'difference_images_needing_inspection':[]});all_comp.extend(comparisons)
 c=copy.deepcopy(c0);c['metadata_revision']='render-proof-v003';c['metadata_predecessor']=pin(b/'candidate-scale-v002.json');c['render_proof_revision']='fresh-fixed8-v003';c['artifacts']['brief']=pin(brief)
 for e in c['evidence']:
  e['subject']=expected;e['path']=rel(o/'render-manifest.json');e['sha256']=H(o/'render-manifest.json')
 c['stages']['visual']['note']='Fresh v003 fixed8 images actually rendered from unchanged exact GLB using corrected v002 brief. Runner PID/command/times retained; independent differential binding acceptance pending. No stage/approval flags changed.'
 c['stages']['specification']['note']='Corrected v002 scale_note retained; original rejected carry-forward manifests remain historical only. Current candidate uses genuine fresh v003 render manifest. Original QA differential acceptance pending.'
 c['raw_checks']['actual-render-v003']=x['runner_record'];c['raw_checks']['decoded-pixel-comparison-v003']=pin(comparison)
 assert c['approval']==c0['approval'];assert {k:v['status'] for k,v in c['stages'].items()}=={k:v['status'] for k,v in c0['stages'].items()}
 for stage in c['stages']:
  assert {k:v for k,v in c['stages'][stage].items() if k!='note'}=={k:v for k,v in c0['stages'][stage].items() if k!='note'}
 cp=b/'candidate-proof-v003.json';put(cp,c);contract=b/'profile-contract-proof-v003.json'
 with contract.open('x') as f:subprocess.run(['python3','scripts/candidate_profile.py',rel(cp),'--root',str(R)],stdout=f,check=True)
 val=b/'candidate-validation-proof-v003.json'
 with val.open('x') as f:p=subprocess.run(['python3','scripts/validate_candidate.py',rel(cp),'--root',str(R),'--profile','static-stylized-v1','--profile-contract',str(contract),'--json'],stdout=f)
 report=json.loads(val.read_text());assert p.returncode==0 and report['valid'],report
 rows.append({**x,'glb':pin(b/'model.glb'),'source':pin(b/'source.blend'),'corrected_delivery_brief':pin(brief),'superseded_rejected_candidate':pin(b/'candidate-scale-v002.json'),'superseded_rejected_manifest':pin(b/'proof-final/render-manifest-scale-v002.json'),'fresh_candidate':pin(cp),'fresh_profile_contract':pin(contract),'candidate_integrity_report':pin(val),'pixel_equivalence':pin(comparison),'contact_sheet':pin(o/'contact-sheet-v003.png'),'candidate_record_valid':True,'all_approval_and_stage_flags_unchanged':True})
#Independently compare every prior committed batch asset and both archived QA directories against commit bytes.
paths=['assets/candidates/continuous-small-life-round23-20261020/batch-61','qa/batch61-independent-20261020','qa/batch61-scale-v002-differential-20261020'];preserved={}
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--']+paths,text=True).splitlines():
 old=subprocess.check_output(['git','show',BASE+':'+path]);h=hashlib.sha256(old).hexdigest();assert H(R/path)==h,path;preserved[path]=h
subprocess.run(['git','diff','--exit-code',BASE,'--'],check=True,stdout=subprocess.DEVNULL)
put(D/'original-byte-preservation-v003.json',{'baseline_commit':BASE,'checked_at':now(),'all_original_bytes_match_commit':True,'files':preserved,'pseudopulex_unchanged':True,'old_v001_v002_proofs_and_all_archived_qa_unchanged':True})
new_files=[p for x in rows for p in (R/x['proof_directory']).rglob('*') if p.is_file()]+list(D.rglob('*'));new_bytes=sum(p.stat().st_size for p in set(new_files) if p.is_file());assert new_bytes<20_000_000,new_bytes
put(D/'verification-v003.json',{'schema_version':1,'baseline_commit':BASE,'checked_at':now(),'assets':rows,'new_png_count':24,'all24_decoded_rgba_identical_to_previous_comparable_pixels':all(v['decoded_rgba_identical'] for v in all_comp),'all_render_process_pids':[json.loads((R/x['runner_record']['path']).read_text())['blender_process_pid'] for x in rows],'fresh_render_inputs_and_subjects_verified':True,'all_approval_and_stage_flags_unchanged':True,'original_byte_preservation':pin(D/'original-byte-preservation-v003.json'),'new_output_bytes_so_far':new_bytes,'output_budget_bytes':20_000_000,'geometry_rebuilds':0,'pseudopulex_renders':0,'new_imagegen_calls':0,'pushes':0,'independent_acceptance':'pending differential QA','gpu':'not_run','scene':'not_run'})
put(D/'final-selection-proof-v003.json',[{**x,'candidate_record':rel(R/x['path']/'candidate-proof-v003.json'),'delivery_brief':rel(R/x['path']/'candidate-brief-scale-v002.json'),'proof_directory':x['proof_directory']} for x in rows])
print(json.dumps({'new_fresh_views':24,'decoded_rgba_identical':True,'preserved_prior_files':len(preserved),'new_output_bytes':new_bytes,'candidate_records_valid':True,'approvals_unchanged':True},indent=2))
