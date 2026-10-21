import json,pathlib,hashlib,sys,subprocess,datetime
from PIL import Image,ImageChops
R=pathlib.Path('/workspace/shared/lowpoly-batch90-20261020');B=R/'production/batch90';E=pathlib.Path('/workspace/shared/lowpoly-batch90-evidence');O=pathlib.Path('/workspace/shared/lowpoly-batch90-independent-qa-20261020');sys.path.insert(0,str(R/'scripts'))
from check_reproducibility import compare_rebuild
from validate_candidate import validate_candidate,STATIC_PROFILE
from qa_glb import audit_glb
j=lambda p:json.loads(pathlib.Path(p).read_text());h=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();pins=[];errors=[]
def pin(p,sha,label):
 p=pathlib.Path(p);got=h(p) if p.is_file() else None;r=dict(path=str(p),sha256=sha,match=sha==got,label=label);pins.append(r)
 if sha!=got:errors.append(dict(path=str(p),expected=sha,actual=got,label=label))
hand=j(B/'maker-handoff.json');checked=j('/workspace/shared/lowpoly-round37-coordination/batch90-maker-handoff-readback.json')
for f in [checked['handoff'],checked['assets_handoff']]+checked['core_artifacts']:pin(f['path'],f['sha256'],'coordinator_fixed')
for name in ['local-evidence-index.json','payload-manifest.json']:
 for f in j(B/name)['files']:pin(pathlib.Path(f['path']) if f['path'].startswith('/') else R/f['path'],f['sha256'],name)
freeze=j(B/'original-freeze-manifest.json')
for p,sha in freeze['files'].items():pin(R/p,sha,'original_freeze')
sel=j(B/'batch-90-selected-inventory.json');srcbytes=subprocess.check_output(['git','-C',str(R),'show',sel['source_inventory_commit']+':'+sel['source_inventory_path']]);assert hashlib.sha256(srcbytes).hexdigest()==sel['source_inventory_sha256'];src=json.loads(srcbytes);src=src if isinstance(src,list) else src['assets'];lookup={a['id']:a for a in src};assert all(lookup[a['id']]==a for a in sel['assets'])
concepts=[];details=[]
for x in hand['assets']:
 aid=x['asset_id'];rev=x['revision'];b=R/x['path'];o=O/aid;orig=b.parent/'r001';assert h(orig/'brief.json')==h(b/'brief.json');assert h(orig/'references.json')==h(b/'references.json');ori=j(orig/'brief.json');deliv=j(b/'candidate-brief.json');assert all(deliv[k]==v for k,v in ori.items());assert j(orig/'build-config.json')['parameters']==j(b/'build-config.json')['parameters']
 for f in deliv['required_deliverables']:pin(R/f['path'],f['sha256'],'delivery_closure')
 for p,sha in j(b/'build-dependencies.json')['inputs'].items():pin(R/p,sha,'dependency')
 pin(R/'package-lock.json',j(b/'build-dependencies.json')['node_lockfile_sha256'],'node_lock')
 for src in j(b/'references.json')['sources']:
  assert src['rights_note'] and src['incorporated']==False
  for f in src['consult_only_files']:pin(f['path'],f['sha256'],'reference')
 rec=j(b/'concept-generation.json');p=pathlib.Path(rec['original_returned_path']);assert p.is_file();assert h(p)==h(b/'concept-original.png');assert rec['tool']=='image_gen.imagegen';assert rec['observed_returned_at']<freeze['freeze_observed_at'];assert rec['actual_pixel_inspection_at']<freeze['freeze_observed_at'];assert j(b/'execution.json')['started_at']>freeze['freeze_observed_at'];concepts.append(dict(asset_id=aid,original_path=str(p),original_sha256=h(p),receipt_sha256=h(b/'concept-generation.json'),prompt_sha256=h(b/'concept-prompt.txt'),observed_started_at=rec['observed_started_at'],observed_returned_at=rec['observed_returned_at'],observed_inspected_at=rec['actual_pixel_inspection_at'],provider_timestamp=rec['provider_timestamp'],provider_request_id=rec['provider_request_id'],exact_authoring_start='unknown'))
 val=validate_candidate(str(b/'candidate.json'),R,None,STATIC_PROFILE,str(b/'profile-contract.json'));(o/'own-candidate-validation.json').write_text(json.dumps(val,indent=2)+'\n');assert val['valid'],val['errors'];ga=audit_glb(b/'model.glb',14000,6,30);assert not ga['errors'] and ga['bytes']<=1000000;(o/'own-project-audit.json').write_text(json.dumps(ga,indent=2)+'\n')
 life=[json.loads(l) for l in (b/'lifecycle.jsonl').read_text().splitlines()];runs=[]
 for z in j(b/'final-rebuild-binding.json')['runs']:
  raw=pathlib.Path(z['original_run_dir']);request=R/z['request']['path'];result=R/z['result']['path'];execution=R/z['execution']['path'];q=j(request);res=j(result);ex=j(execution)
  for name,f in [('request.json',request),('result.json',result),('outputs/execution.json',execution)]:assert h(raw/name)==h(f)
  assert res['status']=='succeeded' and res['returncode']==0;assert res['pid']==ex['pid'];assert q['created_at']<=res['started_at']<=ex['started_at']<=ex['finished_at']<=res['finished_at'];assert q['identity']['threads']==2;assert q['argv'][q['argv'].index('-t')+1]=='2'
  for name,f in q['identity']['inputs'].items():pin(f['path'],f['sha256'],'rebuild_input')
  for name,f in res['outputs'].items():pin(raw/'outputs'/name,f['sha256'],'rebuild_output')
  # Queue wrapper itself carries the blocking process lock for this single job.
  l=next(l for l in life if l['stage']=='queue-'+str(z['job']) and l['exit_code']==0);assert l['command'][:2]==['flock','/tmp/lowpoly-production-blender.lock'];assert l['started_at']<=res['started_at']<res['finished_at']<=l['ended_at'];pin(l['log'],l['log_sha256'],'queue_log')
  rr=compare_rebuild(b/'model.glb',raw/'outputs/model.glb',b/'generator.py',b/'build-config.json',request,result,'model.glb',root=R);assert rr['semantic_match'] and rr['byte_identical'] and not rr['errors'];(o/('own-rebuild-'+str(z['job'])+'-comparison.json')).write_text(json.dumps(rr,indent=2)+'\n');runs.append(dict(pid=ex['pid'],started_at=ex['started_at'],finished_at=ex['finished_at'],raw_directory=str(raw),request_sha256=h(request),result_sha256=h(result),execution_sha256=h(execution),output_glb_sha256=h(raw/'outputs/model.glb'),semantic_sha256=ga['semantic_sha256'],semantic_match=True,byte_identical=True))
 assert len(runs)==2 and runs[0]['pid']!=runs[1]['pid'] and runs[0]['started_at']!=runs[1]['started_at']
 pre=j(b/'preproof-binding.json');man=j(b/'proof-final/render-manifest.json');render=next(l for l in life if l['stage']=='proof-final' and l['exit_code']==0);assert pre['checked_at']<render['started_at']<man['created_at']<=render['ended_at'];assert render['command'][:2]==['flock','/tmp/lowpoly-production-blender.lock'];assert render['command'][render['command'].index('--threads')+1]=='2';pin(render['log'],render['log_sha256'],'final_render_log')
 for role,file in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json')]:assert man['subject'][role+'_sha256']==pre[role+'_sha256']==h(b/file)
 assert man['subject']['revision']==rev and man['source_unchanged'];sheet=Image.open(b/'contact-sheet.png').convert('RGB');assert sheet.size==(2048,1080),sheet.size;tiles=[];frames=[]
 for i,f in enumerate(man['frames']):
  p=b/'proof-final'/f['path'];pin(p,f['sha256'],'frame');im=Image.open(p).convert('RGB');assert im.size==(512,512) and f['wall_seconds']>0;tile=sheet.crop((i%4*512,i//4*540+28,i%4*512+512,i//4*540+540));same=ImageChops.difference(tile,im).getbbox() is None;tiles.append(same);assert same,(aid,i);frames.append(dict(id=f['id'],sha256=h(p),wall_seconds=f['wall_seconds']))
 assert len(frames)==8
 row=dict(asset_id=aid,revision=rev,original_brief_unchanged=True,original_parameters_unchanged=True,original_references_unchanged=True,two_executed_rebuilds=runs,final_subject=man['subject'],binding_at=pre['checked_at'],render_started_at=render['started_at'],render_finished_at=render['ended_at'],render_log_sha256=h(render['log']),all_frames_after_final_binding=True,frames=frames,sheet_sha256=h(b/'contact-sheet.png'),sheet_lossless_tiles=tiles)
 (o/'own-provenance.json').write_text(json.dumps(row,indent=2)+'\n');details.append(row)
assert not errors,errors
report=dict(checked_at=now(),source_commit=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD']).decode().strip(),parent=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD^']).decode().strip(),source_clean=subprocess.check_output(['git','-C',str(R),'status','--porcelain']).decode()=='',maker_handoff_sha256=h(B/'maker-handoff.json'),original_inventory_sha256=sel['source_inventory_sha256'],selected_inventory_original_entries_identical=True,freeze_sha256=h(B/'original-freeze-manifest.json'),freeze_observed_at=freeze['freeze_observed_at'],source_inspection_observed_at=j(B/'source-inspection-v001.json')['observed_at'],pin_count=len(pins),all_pins_match=not errors,checked_index_sha256=h(B/'local-evidence-index.json'),checked_payload_sha256=h(B/'payload-manifest.json'),concepts=concepts,errors=errors,limitations='Chronology is observed process records, not cryptographic attestation; provider/internal authoring times remain unknown and no filesystem times are substituted.')
(O/'own-integrity-provenance.json').write_text(json.dumps(report,indent=2)+'\n');(O/'source-pin-checks.json').write_text(json.dumps(pins,indent=2)+'\n');print(json.dumps(report,indent=2))
