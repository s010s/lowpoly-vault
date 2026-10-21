import sys,json,pathlib,hashlib,subprocess,datetime,base64
from PIL import Image,ImageChops
W=pathlib.Path('/workspace/shared/lowpoly-batch89-20261020');B=W/'production/small-life-batch89';E=pathlib.Path('/workspace/shared/lowpoly-batch89-evidence');O=pathlib.Path('/workspace/shared/lowpoly-batch89-independent-qa-20261020');sys.path.insert(0,str(W/'scripts'))
from qa_glb import audit_glb
from validate_candidate import validate_candidate,STATIC_PROFILE
from check_reproducibility import compare_rebuild
j=lambda p:json.loads(pathlib.Path(p).read_text());h=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
errors=[];pins=[]
def pin(path,sha,label):
 p=pathlib.Path(path);got=h(p) if p.is_file() else None;r={'label':label,'path':str(p),'expected':sha,'actual':got,'pass':sha==got};pins.append(r)
 if not r['pass']:errors.append(r)
 return r['pass']
def traverse(x,label='handoff'):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and 'sha256' in x:pin(W/x['path'],x['sha256'],label)
  for k,v in x.items():traverse(v,label+'.'+k)
 elif isinstance(x,list):
  for n,v in enumerate(x):traverse(v,f'{label}.{n}')
hand=j(B/'maker-handoff.json');traverse(hand);hand_count=len(pins)
raw=j(E/'raw-evidence-manifest.json')
for name,v in raw['files'].items():
 pin(E/name,v['sha256'],'raw.'+name)
 if (E/name).stat().st_size!=v['bytes']:errors.append('size mismatch '+name)
freeze=j(B/'original-freeze-manifest.json')
for p,sha in freeze['files'].items():pin(W/p,sha,'freeze.'+p)
selected=B/'batch-89-selected-inventory.json';pin(selected,h(pathlib.Path('/workspace/shared/lowpoly-round37-coordination/batch-89-selected-inventory.json')),'coordination_inventory_byte_identity')
sel=j(selected);source=subprocess.check_output(['git','-C',str(W),'show',sel['source_inventory_commit']+':'+sel['source_inventory_path']]);source_sha=hashlib.sha256(source).hexdigest();assert source_sha==sel['source_inventory_sha256']
# Observed freeze, source inspection and genuine concept receipts, not filesystem timestamps.
concepts=[]
for item in hand['items']:
 aid=item['asset_id'];rev=item['revision'];d=B/aid/rev;out=O/aid;out.mkdir(exist_ok=True)
 receipt=j(B/'concepts'/f'{aid}-receipt.json');assert receipt['returned_at']<=freeze['freeze_observed_at'];orig=receipt.get('output_hint','');cn={'asset_id':aid,'receipt':receipt,'concept_sha256':h(B/'concepts'/f'{aid}-concept.png'),'prompt_sha256':h(B/'concepts'/f'{aid}-prompt.txt')}
 if aid=='psilophyton':cn['original_transport_same']=hashlib.sha256(base64.b64decode((E/'psilophyton-concept.transport.b64').read_bytes())).hexdigest()==cn['concept_sha256']
 else:
  import re
  m=re.search(r'as (/[^ ]+\.png)',orig);p=pathlib.Path(m.group(1));cn['original_path']=str(p);cn['original_retained']=p.exists();cn['original_pixels_same']=h(p)==cn['concept_sha256'] if p.exists() else None
 concepts.append(cn)
 refs=j(W/item['artifacts']['references']['path']);assert refs['no_incorporated_third_party_assets']
 for src in refs['sources']:
  assert src['rights_note'] and not src['incorporated']
  for f in src['consult_only_files']:pin(f['path'],f['sha256'],'reference.'+src['id'])
 dep=j(W/item['artifacts']['dependencies']['path'])
 for f in dep['files']:pin(W/f['path'],f['sha256'],'dependency.'+aid)
 # Validate candidate integrity under declared profile, without conferring approval.
 val=validate_candidate(item['candidate']['path'],W,None,STATIC_PROFILE,item['profile_contract']['path']);(out/'own-candidate-validation.json').write_text(json.dumps(val,indent=2)+'\n')
 assert val['valid'],val['errors']
 ga=audit_glb(W/item['artifacts']['glb']['path'],max_triangles=14000,max_materials=6,max_primitives=30);assert not ga['errors'];(out/'own-static-glb.json').write_text(json.dumps(ga,indent=2)+'\n')
 prov=j(W/item['two_rebuilds']['path']);runs=[]
 for r in prov['two_distinct_real_rebuilds']:
  rawdir=pathlib.Path(r['raw_directory']);request=W/r['request']['path'];result=W/r['result']['path'];execution=W/r['execution']['path'];q=j(request);z=j(result);x=j(execution)
  assert h(rawdir/'request.json')==h(request) and h(rawdir/'result.json')==h(result)
  assert x['parent_pid']==z['pid'] and z['started_at']<=x['started_at']<=x['finished_at']<=z['finished_at']
  assert '/usr/bin/flock'==q['argv'][0] and '/tmp/lowpoly-production-blender.lock'==q['argv'][1] and q['argv'][q['argv'].index('--threads')+1]=='2'
  for key,value in q['identity']['inputs'].items():pin(value['path'],value['sha256'],aid+'.rebuild_input.'+key)
  for name,v in z['outputs'].items():pin(rawdir/'outputs'/name,v['sha256'],aid+'.rebuild_output.'+name)
  rebuilt=rawdir/'outputs'/aid/f'{aid}.glb';rr=compare_rebuild(W/item['artifacts']['glb']['path'],rebuilt,W/item['artifacts']['generator']['path'],W/item['artifacts']['config']['path'],request,result,aid+'/'+aid+'.glb',root=W);assert rr['semantic_match'] and not rr['errors'];(out/f"own-rebuild-{r['label']}-comparison.json").write_text(json.dumps(rr,indent=2)+'\n')
  runs.append({'pid':x['pid'],'flock_pid':z['pid'],'started_at':x['started_at'],'finished_at':x['finished_at'],'request_sha256':h(request),'result_sha256':h(result),'execution_sha256':h(execution),'raw_directory':str(rawdir),'semantic_match':rr['semantic_match'],'byte_identical':rr['byte_identical']})
 assert len(runs)==2 and runs[0]['pid']!=runs[1]['pid'] and runs[0]['started_at']!=runs[1]['started_at']
 sub=j(d/'subject.json');manifest=j(W/item['render_manifest']['path']);assert all(manifest['subject'][k]==sub[k] for k in ['revision','glb_sha256','brief_sha256','references_sha256'])
 cand=j(d/'candidate.json');assert all(cand['artifacts'][k]['sha256']==sub[k+'_sha256'] for k in ['glb','brief','references'])
 render_requests=list((E/'final-render-queue/render'/aid/rev).rglob('request.json'));assert len(render_requests)==1;rd=render_requests[0].parent;req=j(rd/'request.json');res=j(rd/'result.json');assert res['status']=='succeeded' and res['returncode']==0;assert sub['bound_at']<req['created_at']<=res['started_at']<manifest['created_at']<=res['finished_at']
 for role in ['glb','brief','references']:assert req['identity']['inputs'][role]['sha256']==sub[role+'_sha256']
 frames=[]
 for f in manifest['frames']:
  fp=d/'views'/f['path'];pin(fp,f['sha256'],aid+'.finalframe.'+f['id']);assert Image.open(fp).size==(512,512);assert h(rd/'outputs'/f['path'])==h(fp)==res['outputs'][f['path']]['sha256'];frames.append({'id':f['id'],'sha256':h(fp),'seconds':f['wall_seconds']})
 assert len(frames)==8 and all(f['seconds']>0 for f in frames)
 sheet=Image.open(W/item['contact_sheet']['path']).convert('RGBA');assert sheet.size==(2048,1088);tiles=[]
 for i,f in enumerate(manifest['frames']):
  tile=sheet.crop((i%4*512,i//4*544,i%4*512+512,i//4*544+512));frame=Image.open(d/'views'/f['path']).convert('RGBA');same=ImageChops.difference(tile,frame).getbbox() is None;assert same;tiles.append(same)
 old=None
 if aid=='teichichnus-spreite-wall':
  oldreq=list((E/'final-render-queue/render'/aid/'r002').rglob('request.json'))[0];oldm=j(oldreq.parent/'outputs/render-manifest.json');old={'raw_dir':str(oldreq.parent),'manifest_sha256':h(oldreq.parent/'outputs/render-manifest.json'),'all_eight_retained':all((oldreq.parent/'outputs'/f['path']).is_file() for f in oldm['frames']),'all_eight_hashes_differ_from_r003':all(x['sha256']!=y['sha256'] for x,y in zip(oldm['frames'],manifest['frames']))};assert old['all_eight_retained'] and old['all_eight_hashes_differ_from_r003']
 # Preserve immutable brief core, additions and geometry revision provenance never overwrite frozen text.
 original=j(B/aid/'r001/original-brief.json');delivery=j(W/item['artifacts']['brief']['path']);diff={k:{'original':v,'delivery':delivery.get(k)} for k,v in original.items() if k != 'brief_version' and delivery.get(k)!=v};assert not diff,diff
 (out/'own-provenance.json').write_text(json.dumps({'asset_id':aid,'revision':rev,'stage_subject':sub,'two_rebuilds':runs,'render_request_sha256':h(rd/'request.json'),'render_result_sha256':h(rd/'result.json'),'render_raw_dir':str(rd),'render_started_at':res['started_at'],'render_finished_at':res['finished_at'],'render_wall_seconds':res['wall_seconds'],'frames':frames,'sheet_lossless_512_tiles':tiles,'old_failed_r002_retention':old,'original_brief_core_unchanged':not diff},indent=2)+'\n')
initial=[j(p) for p in (E/'build-queue').rglob('request.json')];chron={'original_freeze_observed_at':freeze['freeze_observed_at'],'source_inspection_observed_at':j(B/'source-inspection-v001.json')['observed_at'],'earliest_initial_build_request':min(x['created_at'] for x in initial),'all_initial_builds_after_freeze':all(x['created_at']>freeze['freeze_observed_at'] for x in initial),'generator_authorship_evidence':'Freeze records generator_authored=false, geometry_authored=false; original manifest excludes generator and geometry, then initial queue requests pin generator and output. This is observed local chronological provenance, not cryptographic attestation; filesystem times are not used as provider/authoring timestamps.'}
assert chron['all_initial_builds_after_freeze'];assert subprocess.check_output(['git','-C',str(W),'status','--porcelain']).decode()==''
report={'schema_version':1,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fixed_commit':subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD']).decode().strip(),'parent':subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD^']).decode().strip(),'maker_handoff_sha256':h(B/'maker-handoff.json'),'handoff_pin_count':hand_count,'raw_manifest_sha256':h(E/'raw-evidence-manifest.json'),'raw_file_count':len(raw['files']),'freeze_sha256':h(B/'original-freeze-manifest.json'),'freeze_file_count':len(freeze['files']),'source_inventory_sha256':source_sha,'chronology':chron,'concept_provenance':concepts,'pin_count':len(pins),'pins':pins,'errors':errors,'clean_source_worktree':True,'status':'pass' if not errors else 'fail'}
(O/'own-integrity-provenance.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['pins','concept_provenance']},indent=2));assert not errors
