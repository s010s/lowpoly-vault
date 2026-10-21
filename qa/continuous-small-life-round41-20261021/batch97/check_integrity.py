import json,hashlib,pathlib,subprocess,os,sys,datetime
from PIL import Image
import numpy as np
W=pathlib.Path('/workspace/shared/lowpoly-batch97-20261020');B=W/'production/small-life-batch97';O=pathlib.Path(__file__).parent
sys.path.insert(0,str(W/'scripts'));from qa_glb import audit_glb
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'}
def git(*x):return subprocess.check_output(['git','-c','protocol.allow=never',*x],cwd=W,env=env)
commit=git('rev-parse','HEAD').decode().strip();assert commit=='280ef4dcae42c368727b22a666b2e6a455c9e9d7'
r={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':commit,'branch':git('branch','--show-current').decode().strip(),'status':git('status','--porcelain').decode(),'handoff_sha256':H(B/'handoff.json'),'prior_output':'No existing output directory at first check. Fresh reviewer, no uncertain prior results.','manifests':{},'assets':{}}
assert r['handoff_sha256']=='b2280ef3390203eb59c984e2cf3ba121569639238ffde1b485a8dfc4a7aaf726'
for label in ['delivery-manifest.json','original-freeze-manifest.json','dependencies.json','dependencies-v002.json']:
 m=json.loads((B/label).read_text());results=[]
 for f in ([{'path':p,'sha256':s} for p,s in m['files'].items()] if isinstance(m['files'],dict) else m['files']):
  p=W/f['path'];blob=git('show',commit+':'+f['path']);results.append({'path':f['path'],'sha256':H(p),'pass':H(p)==f['sha256']==hashlib.sha256(blob).hexdigest()})
 r['manifests'][label]={'sha256':H(B/label),'count':len(results),'all_pass':all(x['pass'] for x in results),'files':results}
for aid,rev in [('ginkgo','r002'),('dicranophyllum','r003'),('noeggerathia','r002'),('bjuvia','r001')]:
 d=B/aid/rev;out=O/aid;out.mkdir(exist_ok=True);c=json.loads((d/'candidate.json').read_text());x={'revision':rev,'candidate_sha256':H(d/'candidate.json'),'artifacts':{},'render_sets':[],'rebuilds':[],'references':[]}
 for k,v in c['artifacts'].items():x['artifacts'][k]={**v,'actual_sha256':H(W/v['path']),'pass':H(W/v['path'])==v['sha256']}
 subject={'revision':rev,**{k+'_sha256':c['artifacts'][k]['sha256'] for k in ['glb','brief','references']}}
 for mp in sorted(d.rglob('render-manifest.json')):
  m=json.loads(mp.read_text());cfg=json.loads((mp.parent/'render-config.json').read_text());checks=[]
  for f in m['frames']:
   fp=mp.parent/f['path'];im=Image.open(fp);checks.append({'path':str(fp),'sha256':H(fp),'pass':H(fp)==f['sha256'] and im.size==(512,512),'mode':im.mode,'dimensions':im.size})
  x['render_sets'].append({'path':str(mp),'subject_match':m['subject']==subject,'config_hash_match':H(mp.parent/'render-config.json')==m['config_sha256'],'frames':checks,'camera':cfg['camera'],'engine':cfg['engine'],'render_threads':cfg['render_threads'],'samples':cfg['samples']})
 sheet=Image.open(d/'views/contact-sheet.png').convert('RGBA');x['sheet_png_size']=sheet.size;x['sheet_sha256']=H(d/'views/contact-sheet.png')
 x['sheet_pixel_identity']={v:np.array_equal(np.array(sheet.crop((i%4*512,i//4*544,i%4*512+512,i//4*544+512))),np.array(Image.open(d/'views'/f'{v}.png').convert('RGBA'))) for i,v in enumerate(['hero','reversehero','front','side','rear','top','clay','silhouette'])}
 for name in ['rebuild-a','rebuild-b']:
  q=d/'qa';req=json.loads((q/f'{name}-request.json').read_text());res=json.loads((q/f'{name}-result.json').read_text());exe=json.loads((q/f'{name}-execution.json').read_text());fp=hashlib.sha256(json.dumps(req['identity'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest();raw=pathlib.Path(req['argv'][req['argv'].index('--output')+1]);checks=[]
  for f,v in res['outputs'].items():
   p=raw/f;checks.append({'path':str(p),'sha256':H(p),'pass':H(p)==v['sha256']})
  rawglb=raw/aid/f'{aid}.glb';audit=audit_glb(rawglb,14000,6,30)
  x['rebuilds'].append({'name':name,'request_sha256':H(q/f'{name}-request.json'),'result_sha256':H(q/f'{name}-result.json'),'execution_sha256':H(q/f'{name}-execution.json'),'fingerprint_valid':fp==req['fingerprint']==res['fingerprint'],'blender_pid':exe['pid'],'wrapper_pid':res['pid'],'parent_pid':exe['parent_pid'],'generator_sha256':exe['generator_sha256'],'config_sha256':exe['config_sha256'],'status':res['status'],'returncode':res['returncode'],'raw_output_checks':checks,'started':exe['started_at'],'finished':exe['finished_at'],'semantic_sha256':audit['semantic_sha256']})
 x['distinct_rebuild_pids']=len({z['blender_pid'] for z in x['rebuilds']})==2
 for ref in json.loads((B/aid/'r001/references.json').read_text())['sources']:
  x['references'].append({'id':ref['id'],'url':ref['url'],'files':[{'path':f['path'],'sha256':H(f['path']),'pass':H(f['path'])==f['sha256']} for f in ref['consult_only_files']]})
 glb=W/c['artifacts']['glb']['path'];audit=audit_glb(glb,14000,6,30);audit['glb_sha256']=H(glb);audit['size_hard_limit_pass']=glb.stat().st_size<=1000000
 (out/'project-independent.json').write_text(json.dumps(audit,indent=2)+'\n');x['project_audit_errors']=audit['errors'];x['semantic_sha256']=audit['semantic_sha256'];x['rebuild_semantic_equal']=all(z['semantic_sha256']==audit['semantic_sha256'] for z in x['rebuilds']);r['assets'][aid]=x
(O/'integrity.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'commit':commit,'status':r['status'],'manifests':{k:[v['count'],v['all_pass']] for k,v in r['manifests'].items()},'assets':{k:{'artifacts':all(v['pass'] for v in x['artifacts'].values()),'sheets':all(x['sheet_pixel_identity'].values()),'project_errors':x['project_audit_errors'],'pids':[z['blender_pid'] for z in x['rebuilds']],'rebuild_semantic_equal':x['rebuild_semantic_equal']} for k,x in r['assets'].items()}},indent=2))
