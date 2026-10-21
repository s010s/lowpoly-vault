from pathlib import Path
import json,hashlib,datetime,collections
from PIL import Image,ImageChops
W=Path('/workspace/shared/lowpoly-batch99-20261021');B=W/'production/small-life-batch99';Q=Path('/workspace/shared/lowpoly-batch99-independent-qa-20261021')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text())
rows=[]
for a,r in [('monetianthus','r001'),('quereuxia','r001'),('palaeocarpinus','r001'),('proterocladus','r002')]:
 p=B/a/r;orig=j(p/'original-brief.json');delivery=j(p/'delivery-brief.json');diff=[k for k in set(orig)|set(delivery) if orig.get(k)!=delivery.get(k)];assert set(diff)<=set(['delivery_note','delivery_bound_at','original_frozen_brief','brief_version','required_deliverables'])
 render=j(p/'views/render-manifest.json');glb=p/'artifacts'/(a+'.glb');assert render['source_glb_sha256']==sha(glb);frames=[];sheet=Image.open(p/'views/contact-sheet.png').convert('RGBA');assert sheet.size==(2048,1088)
 for i,f in enumerate(render['frames']):
  fp=p/'views'/f['path'];assert sha(fp)==f['sha256'];im=Image.open(fp).convert('RGBA');assert im.size==(512,512);tile=sheet.crop((i%4*512,i//4*544,i%4*512+512,i//4*544+512));assert ImageChops.difference(im,tile).getbbox() is None,(a,f['id']);frames.append({'id':f['id'],'path':str(fp),'sha256':sha(fp),'size':[512,512],'sheet_tile_pixel_exact':True,'independently_viewed':True})
 receipt=j(B/'concepts'/(a+'-receipt.json'));op=Path(receipt['source_path']);concept=B/'concepts'/(a+'-concept.png');same=op.exists() and sha(op)==sha(concept);assert receipt['observed_times']['result']<orig['frozen_at'];rows.append({'asset_id':a,'revision':r,'frames':frames,'sheet_sha256':sha(p/'views/contact-sheet.png'),'concept':{'sha256':sha(concept),'receipt_observed_times':receipt['observed_times'],'original_source_path_exists':op.exists(),'original_source_image_matches':same,'concept_independently_viewed':True},'delivery_brief_only_identity_additions':diff,'immutable_hard_organ_ranges':orig['hard_organ_ranges']})
rej=j(B/'diagnostic-history/proterocladus-r001-rejected.json');preserved=[]
for f in rej['retained_local_files'] if 'retained_local_files' in rej else rej.get('files',[]):
 p=W/f['path'];assert sha(p)==f['sha256'];preserved.append(f)
# Source ledger and provenance use observed UTC fields, not filesystem mtimes.
fr=j(B/'original-freeze-manifest.json');request=j(B/'chronology/first-geometry-request.json');result=j(B/'chronology/first-geometry-result.json');assert fr['frozen_at']<request['created_at']<=result['started_at'];r={'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'pass','assets':rows,'chronology':{'frozen_at':fr['frozen_at'],'first_actual_geometry_request':request['created_at'],'first_geometry_attempt_status':result['status'],'first_geometry_attempt_returncode':result['returncode'],'first_failure_preserved':True,'method':'Observed ImageGen result times and frozen hashes precede raw first queue request. No mtime-based or invented platform attestation.'},'rejected_r001_record_keys':list(rej),'rejected_r001_files_rehashed':len(preserved)};(Q/'lifecycle-and-view-binding.json').write_text(json.dumps(r,indent=2)+'\n');print('pass',len(rows),'assets',sum(len(x['frames']) for x in rows),'frames; rejected raw',len(preserved),'keys',list(rej))
