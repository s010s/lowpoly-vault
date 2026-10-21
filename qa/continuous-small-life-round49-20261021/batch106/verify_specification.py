import json,pathlib,hashlib,datetime,os
from PIL import Image
R=pathlib.Path('/workspace/shared/lowpoly-batch106-20261021');B=R/'production/small-life-batch106';O=pathlib.Path(__file__).parent;RAW=pathlib.Path('/workspace/shared/lowpoly-batch106-evidence');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();errors=[];result={}
def check(p,sha=None,size=None):
 p=pathlib.Path(p);ok=p.is_file() and (sha is None or h(p)==sha) and (size is None or p.stat().st_size==size)
 if not ok:errors.append(str(p))
 return ok
files=json.loads((B/'delivery-manifest.json').read_text())['files'];result['payload']={'files':len(files),'manifest_self_additional':1,'bytes':sum(f['bytes'] for f in files),'checks':[check(R/f['path'],f['sha256'],f['bytes']) for f in files]}
result['original_dispatch']=[]
for p in (B/'original-dispatch').iterdir():
 q=pathlib.Path('/workspace/shared/lowpoly-round36-coordination/PRODUCTION-ADDENDUM.md') if p.name=='PRODUCTION-ADDENDUM.md' else pathlib.Path('/workspace/shared/lowpoly-round49-coordination')/p.name
 result['original_dispatch'].append({'name':p.name,'original_sha256':h(q),'copied_sha256':h(p),'same':check(p,h(q))})
result['assets']={}
for aid,rev in [('didymograptus','r004'),('monograptus','r004'),('diplograptus','r009'),('dictyonema','r005')]:
 d=B/aid/rev;c=json.loads((d/'candidate.json').read_text());sub={'revision':rev,'glb_sha256':c['artifacts']['glb']['sha256'],'brief_sha256':c['artifacts']['brief']['sha256'],'references_sha256':c['artifacts']['references']['sha256']};im=[];man=[]
 for mf in d.glob('*/render-manifest.json'):
  m=json.loads(mf.read_text());ok=m['subject']==sub and m['source_glb_sha256']==sub['glb_sha256'] and m['source_unchanged'];man.append({'path':str(mf),'subject_matches':ok,'created_at':m['created_at']})
  if not ok:errors.append(str(mf)+' subject')
  for f in m['frames']:
   p=mf.parent/f['path'];ok=check(p,f['sha256'],f['bytes']) and Image.open(p).size==(512,512);im.append({'path':str(p),'sha256':h(p),'dimensions':[512,512],'pass':ok})
  rc=m['render_config'];check(mf.parent/rc['path'],rc['sha256'])
 sheet=Image.open(d/'views/contact-sheet.png').convert('RGBA');sm=json.loads((d/'views/contact-sheet-manifest.json').read_text());check(d/'views/contact-sheet.png',sm['sheet_sha256']);tiles=[]
 for j,f in enumerate(sm['frames']):
  x=(j%4)*512;y=(j//4)*532+20;p=d/'views'/(f['id']+'.png');same=sheet.crop((x,y,x+512,y+512)).tobytes()==Image.open(p).convert('RGBA').tobytes();tiles.append({'view':f['id'],'same_pixels':same})
  if not same:errors.append(str(p)+' sheet pixels')
 receipt=json.loads((B/'concepts'/f'{aid}-prompt-receipt.json').read_text());request=json.loads(pathlib.Path(receipt['request_receipt']).read_text());cp=B/'concepts'/f'{aid}-concept.png';orig=pathlib.Path(receipt['original_output_path']);concept={'retained_sha256':h(cp),'original_exists':orig.exists(),'original_pixels_match':check(orig,h(cp)),'prompt_matches_request':receipt['prompt']==request['prompt'],'observed_request':request['requested_at'],'result_observed_by':receipt['result_observed_by'],'provider_time_unknown':receipt['provider_timestamps'] is None}
 old=json.loads((B/aid/'r001/original-brief.json').read_text());new=json.loads((d/'delivery-brief.json').read_text());diff={k:[old.get(k),new.get(k)] for k in set(old)|set(new) if old.get(k)!=new.get(k)}
 allowed={'brief_version','refinement_note'}
 if not set(diff)<=allowed:errors.append(aid+' original brief substantive changed')
 first=RAW/'first-builds'/aid/'execution.json';chron={'freeze':old['frozen_at'],'first_execution':json.loads(first.read_text())['started_at'] if first.exists() else None,'first_failed_attempt_log':str(RAW/'first-builds'/f'{aid}.log') if not first.exists() else None,'limitation':'Authorship/readback chronology uses retained observed records, not fabricated provider times or file mtimes.'}
 result['assets'][aid]={'revision':rev,'subject':sub,'render_manifests':man,'inspected_images':im,'sheet_pixels':tiles,'concept_provenance':concept,'brief_differences':diff,'original_hard_organ_ranges':old['hard_organ_ranges'],'chronology':chron}
raw=json.loads((RAW/'raw-retention-manifest-before-commit.json').read_text());print('rawkeys',raw.keys());hist=json.loads((RAW/'retained-worktree-history-map.json').read_text());hr=[]
for f in hist['files']:hr.append(check(f['retained_path'],f['sha256'],f['bytes']))
result['retained_revisions']={'history_files':len(hr),'all_match':all(hr),'history_manifest_sha256':h(RAW/'retained-worktree-history-map.json'),'raw_manifest_sha256':h(RAW/'raw-retention-manifest-before-commit.json'),'revision_history_sha256':h(B/'revision-history.json'),'scientific_correction_sha256':h(B/'diplograptus-transmitted-light-correction.json')}
result['errors']=errors;result['status']='PASS' if not errors else 'FAIL';result['created_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();(O/'specification.json').write_text(json.dumps(result,indent=2));print('SPECIFICATION',result['status'],errors)
(O/'recovery-stage-specification.json').write_text(json.dumps({'stage':'specification','status':'complete','result':result['status'],'artifact':'specification.json','at':result['created_at']},indent=2))
