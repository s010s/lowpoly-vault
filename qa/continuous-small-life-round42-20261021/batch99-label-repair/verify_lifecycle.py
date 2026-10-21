import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,datetime,difflib,subprocess
from PIL import Image
W=Path('/workspace/shared/lowpoly-batch99-label-repair-20261021');O=Path('/workspace/shared/lowpoly-batch99-20261021');Q=Path(__file__).parent;B=W/'production/small-life-batch99';sys.path.insert(0,str(W/'scripts'));from check_reproducibility import compare_rebuild
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=lambda p:json.loads(Path(p).read_text())
def write(name,data): (Q/name).write_text(json.dumps(data,indent=2)+'\n')
def stage(s):
 with (Q/'recovery-progress.jsonl').open('a') as f:f.write(json.dumps({'stage':s,'status':'pass','at':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
rows=[]
for a,old,new in [('monetianthus','r001','r002'),('proterocladus','r002','r003')]:
 p=B/a/new;op=O/'production/small-life-batch99'/a/old;glb=p/'artifacts'/(a+'.glb');subject={'revision':new,'glb_sha256':h(glb),'brief_sha256':h(p/'delivery-brief.json'),'references_sha256':h(p/'references.json')};assert j(p/'candidate-binding.json')['subject']==subject
 orig=j(p/'original-brief.json');delivery=j(p/'delivery-brief.json');dd=[k for k in set(orig)|set(delivery) if orig.get(k)!=delivery.get(k)]; assert set(dd)<={'delivery_note','delivery_bound_at','original_frozen_brief','brief_version','required_deliverables','revision'},dd
 for k,v in j(p/'candidate-binding.json').items():
  if isinstance(v,dict) and 'path' in v and k!='original_freeze_manifest':assert h(W/v['path'])==v['sha256']
 prov=j(p/'qa/execution-provenance.json');builds=[]
 for run in prov['queue_runs']:
  receipts={k:W/run[k]['path'] for k in ['request','result','execution']}
  for k,fp in receipts.items():assert h(fp)==run[k]['sha256']
  req,res,ex=[j(receipts[k]) for k in ['request','result','execution']];raw_glb=Path(run['raw_output_glb']['path']);rawroot=raw_glb.parents[2];outputs=rawroot/'outputs'
  for k in ['request','result']:assert (rawroot/(k+'.json')).read_bytes()==receipts[k].read_bytes()
  assert (outputs/'execution.json').read_bytes()==receipts['execution'].read_bytes()
  for stream in ['stdout.log','stderr.log']:assert (rawroot/stream).read_bytes()==(p/'qa'/('rebuild-'+run['run'])/stream).read_bytes()
  for k,v in req['identity']['inputs'].items():assert h(v['path'])==v['sha256'] and Path(v['path']).stat().st_size==v['bytes'],k
  assert h(req['identity']['executable']['path'])==req['identity']['executable']['sha256']
  for k,v in res['outputs'].items():assert h(outputs/k)==v['sha256'] and (outputs/k).stat().st_size==v['bytes']
  assert ex['pid']==run['pid'] and ex['parent_pid']==res['pid'] and ex['argv']==req['argv'][2:]
  assert req['argv'][:3]==['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender'] and req['argv'][req['argv'].index('--threads')+1]=='2'
  assert req['created_at']<=res['started_at']<=ex['started_at_executor_clock']<=ex['finished_at_executor_clock']<=res['finished_at']
  assert ex['generator_sha256']==h(B/'tools/generate-label-repair-r001.py') and ex['config_sha256']==h(p/'config.json')
  report=compare_rebuild(glb,raw_glb,B/'tools/generate-label-repair-r001.py',p/'config.json',receipts['request'],receipts['result'],a+'/'+a+'.glb',W)
  assert report['status']=='pass' and report['byte_identical'];write(a+'-rebuild-'+run['run']+'-independent.json',report)
  builds.append({'pid':ex['pid'],'parent_pid':ex['parent_pid'],'all_input_output_hashes_reverified':True,'raw_log_receipts_match':True,'glb_sha256':h(raw_glb),'blend_sha256':h(Path(run['raw_output_blend']['path'])),'semantic_sha256':report['semantic_sha256'],'raw_root':str(rawroot),'request_sha256':h(receipts['request']),'result_sha256':h(receipts['result']),'execution_sha256':h(receipts['execution'])})
 assert len(set(x['pid'] for x in builds))==2
 stage(a+'_separate_pid_rebuild_records')
 req=j(p/'qa/final-render/request.json');res=j(p/'qa/final-render/result.json');fp=hashlib.sha256(json.dumps(req['identity'],sort_keys=True,separators=(',',':')).encode()).hexdigest();assert fp==req['fingerprint']==res['fingerprint'];assert res['status']=='succeeded' and res['returncode']==0
 for k,v in req['identity']['inputs'].items():assert h(v['path'])==v['sha256'] and Path(v['path']).stat().st_size==v['bytes']
 rawviews=Path(req['argv'][req['argv'].index('--output-dir')+1]);rawroot=rawviews.parents[1]
 for s in ['request.json','result.json','stdout.log','stderr.log']:assert (rawroot/s).read_bytes()==(p/'qa/final-render'/s).read_bytes()
 for k,v in res['outputs'].items():assert h(rawroot/'outputs'/k)==v['sha256'] and (rawroot/'outputs'/k).stat().st_size==v['bytes'];assert h(p/k)==v['sha256']
 manifest=j(p/'views/render-manifest.json');assert manifest['subject']==subject and manifest['source_glb_sha256']==h(glb);assert h(p/'views/render-config.json')==manifest['config_sha256'];assert (p/'views/render-config.json').read_bytes()==(op/'views/render-config.json').read_bytes()
 sheet=Image.open(p/'views/contact-sheet.png').convert('RGBA');oldsheet=Image.open(op/'views/contact-sheet.png').convert('RGBA');assert sheet.size==(2048,1088) and sheet.tobytes()==oldsheet.tobytes();frames=[]
 assert [x['id'] for x in manifest['frames']]==orig['required_views']
 for i,f in enumerate(manifest['frames']):
  imgp=p/'views'/f['path'];oldp=op/'views'/f['path'];im=Image.open(imgp).convert('RGBA');oim=Image.open(oldp).convert('RGBA');assert im.size==oim.size==(512,512);assert h(imgp)==f['sha256'];assert im.tobytes()==oim.tobytes(),(a,f['id'],'changed_pixels')
  tile=sheet.crop((i%4*512,i//4*544,i%4*512+512,i//4*544+512));assert tile.tobytes()==im.tobytes()
  frames.append({'view':f['id'],'new_path':str(imgp),'new_sha256':h(imgp),'old_path':str(oldp),'old_sha256':h(oldp),'rgba_pixels_exact':True,'changed_pixels':0,'maximum_channel_delta':0,'sheet_tile_exact':True,'personally_viewed':True})
 geo=j(Q/(a+'-geometry.json'));oldgeo=j('/workspace/shared/lowpoly-batch99-independent-qa-20261021/'+a+'-geometry.json');assert geo['contacts']==oldgeo['contacts'];assert not any(not c['actual_base_contact'] for c in geo['contacts']);assert all(c['raw_boundary_edges']==0 and c['raw_nonmanifold_edges']==0 for c in geo['components'])
 comps={c['tag']:c for c in oldgeo['components']};assert all(c==comps[c['tag']] for c in geo['components'] if c['tag']!='enlarged_label')
 runtime=j(Q/(a+'-runtime.json'));khr=j(Q/(a+'-khronos.json'));assert runtime['glb_sha256']==h(glb) and runtime['status']=='pass' and khr['source_sha256']==h(glb) and khr['issues']['numErrors']==khr['issues']['numWarnings']==0
 stage(a+'_runtime_contacts_pixels_cameras')
 rows.append({'asset_id':a,'subject':subject,'source_sha256':h(p/'artifacts'/(a+'.blend')),'delivery_brief_changes':dd,'builds':builds,'frames':frames,'sheet_sha256':h(p/'views/contact-sheet.png'),'sheet_pixels_match_original':True,'personally_viewed_sheet':True,'render_config_byte_identical':True,'render_config_sha256':h(p/'views/render-config.json'),'raw_render_inputs_outputs_rehashed':True,'fresh_contacts_count':len(geo['contacts']),'all_contact_details_exact_to_original':True,'nonlabel_geometry_measurements_and_exposure_exact_to_original':True,'fresh_runtime_khronos_pass':True})
write('lifecycle-pixel-camera-verification.json',{'status':'pass','assets':rows,'independence':'Actual bytes, raw execution records and live parse checked; no maker verdict is accepted as proof. Build execution receipts are recorded attestations, not a cryptographic execution proof. Review did not rerun generators or render views.','pixel_method':'Decode RGBA, compare complete byte buffers including RGB and alpha. No alpha-only getbbox shortcut.','source_unchanged':True})
# Re-run original independent GLB label decoder with routing only changed. Exact classification body retained.
original=Path('/workspace/shared/lowpoly-batch99-independent-qa-20261021/glb_label_orientation.py').read_text()
for name,isnew in [('old',False),('new',True)]:
 out=Q/('original-method-'+name);out.mkdir(exist_ok=True)
 s=original.replace("W=pathlib.Path('/workspace/shared/lowpoly-batch99-20261021');Q=pathlib.Path('/workspace/shared/lowpoly-batch99-independent-qa-20261021')", "W=pathlib.Path('"+str(W if isnew else O)+"');Q=pathlib.Path('"+str(out)+"')")
 s=s.replace("geo=json.loads((Q/(a+'-geometry.json')).read_text())", "geo=json.loads((pathlib.Path('/workspace/shared/lowpoly-batch99-independent-qa-20261021')/(a+'-geometry.json')).read_text())")
 if isnew:s=s.replace("[('monetianthus','r001'),('proterocladus','r002')]", "[('monetianthus','r002'),('proterocladus','r003')]")
 script=Q/('original-method-'+name+'.py');script.write_text('import sys;sys.dont_write_bytecode=True\n'+s);result=subprocess.run([sys.executable,str(script)],capture_output=True,text=True);(Q/('original-method-'+name+'.log')).write_text(result.stdout+result.stderr);assert result.returncode==0
 for a in ['monetianthus','proterocladus']:
  d=j(out/(a+'-glb-label-orientation.json'));assert len(d['same_direction_shared_coordinate_edges'])==(0 if isnew else 92);assert d['original_cap_winding']==({'front_outward':82,'back_outward':82} if isnew else {'front_outward':82,'back_inward':82})
write('classification-history.json',{'original_decoder_sha256':h('/workspace/shared/lowpoly-batch99-independent-qa-20261021/glb_label_orientation.py'),'original_failure_preserved':True,'original_thresholds':{'plane_spread_lt':1e-9,'front_proximity_lt':1e-8},'retained_maker_first_diagnostic':{'plane_spread_lt':1e-10,'front_proximity_lt':1e-10,'reason_for_correction':'Incorrect cap classification at float32 coordinate precision, not relaxation of original QA acceptance. Original QA criteria are reproduced without change.'},'original_decoder_rerun_old':{'each_back_inward':82,'each_same_direction_coordinate_edges':92},'original_decoder_rerun_new':{'each_back_inward':0,'each_same_direction_coordinate_edges':0},'raw_index_splits_alone_not_failure_rule':True,'no_virtual_mesh_repair_in_qa':True})
stage('original_classification_regression');print('PASS both rebuild pairs, raw render receipts, sixteen RGBA pixel comparisons, two sheets, exact cameras, strict contacts and unchanged original label decoder')
