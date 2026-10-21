import json,hashlib,pathlib,subprocess,os,sys,datetime
from PIL import Image
W=pathlib.Path('/workspace/shared/lowpoly-batch98-20261020');B=W/'production/small-life-batch98';O=pathlib.Path(__file__).parent
sys.path.insert(0,str(W/'scripts'));from qa_glb import audit_glb
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'}
def git(*x):return subprocess.check_output(['git','-c','protocol.allow=never',*x],cwd=W,env=env)
r={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':git('rev-parse','HEAD').decode().strip(),'branch':git('branch','--show-current').decode().strip(),'status':git('status','--porcelain').decode(),'checks':[],'assets':{}}
for f,expected in [('/workspace/shared/lowpoly-batch98-evidence/final-handoff.json','d92b48173912e32d58b18c93943b763ccffb036b42ba0ed5b5d3a99054b5e945'),(B/'maker-handoff.json','ce9e0114b9f577db9d41987cf0ad73a4e3043ae2958155c4cb53aeeb926b1cc4'),(B/'submission-manifest.json','850a7fcc00643bc2d000eeba2dbfbc2b3ee44ad58255daf8b5ec64d88ff4aece')]:
 r['checks'].append({'path':str(f),'sha256':H(f),'expected':expected,'pass':H(f)==expected})
for label in ['submission-manifest.json','original-freeze-manifest.json','dependencies.json']:
 results=[]
 for f in json.loads((B/label).read_text())['files']:
  p=W/f['path'];blob=git('show',r['commit']+':'+f['path']);results.append({'path':f['path'],'pass':H(p)==f['sha256']==hashlib.sha256(blob).hexdigest()})
 r[label]={'count':len(results),'all_pass':all(x['pass'] for x in results),'files':results}
for aid in ['voltzia','sciadopitys','agathis','archaefructus']:
 d=B/aid/'r001';out=O/aid;out.mkdir(exist_ok=True);c=json.loads((d/'candidate.json').read_text());x={'candidate_sha256':H(d/'candidate.json'),'artifacts':{},'render_sets':[],'rebuilds':[]}
 for k,v in c['artifacts'].items():x['artifacts'][k]={**v,'actual_sha256':H(W/v['path']),'pass':H(W/v['path'])==v['sha256']}
 subject={'revision':'r001',**{k+'_sha256':c['artifacts'][k]['sha256'] for k in ['glb','brief','references']}}
 for mp in sorted(d.rglob('render-manifest.json')):
  m=json.loads(mp.read_text());cfg=json.loads((mp.parent/'render-config.json').read_text());checks=[]
  for f in m['frames']:
   fp=mp.parent/f['path'];im=Image.open(fp);checks.append({'path':str(fp),'sha256':H(fp),'pass':H(fp)==f['sha256'] and im.size==(512,512)})
  x['render_sets'].append({'path':str(mp),'subject_match':m['subject']==subject,'config_hash_match':H(mp.parent/'render-config.json')==m['config_sha256'],'frames':checks,'camera':cfg['camera'],'engine':cfg['engine'],'render_threads':cfg['render_threads'],'samples':cfg['samples']})
 sheet=Image.open(d/'views/contact-sheet.png').convert('RGBA');receipt=json.loads((d/'views/contact-sheet-receipt.json').read_text());x['sheet_receipt']=receipt
 x['sheet_png_size']=sheet.size
 # Known lossless 4x2 sheet: 512px frames, 32px label strip per row.
 x['sheet_pixel_identity']={v:list(sheet.crop((i%4*512,i//4*544,i%4*512+512,i//4*544+512)).getdata())==list(Image.open(d/'views'/f'{v}.png').convert('RGBA').getdata()) for i,v in enumerate(['hero','reversehero','front','side','rear','top','clay','silhouette'])}
 for name in ['rebuild-a','rebuild-b']:
  q=d/'qa'/name;req=json.loads((q/'request.json').read_text());res=json.loads((q/'result.json').read_text());exe=json.loads((q/'execution.json').read_text());identity=req['identity'];fp=hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
  x['rebuilds'].append({'name':name,'request_sha256':H(q/'request.json'),'result_sha256':H(q/'result.json'),'execution_sha256':H(q/'execution.json'),'fingerprint_valid':fp==req['fingerprint']==res['fingerprint'],'pid':exe['pid'],'generator_sha256':exe['generator_sha256'],'config_sha256':exe['config_sha256'],'status':res['status'],'returncode':res['returncode'],'outputs':res['outputs'],'started':exe['started_at_executor_clock'],'finished':exe['finished_at_executor_clock']})
 x['distinct_rebuild_pids']=len({z['pid'] for z in x['rebuilds']})==2
 glb=W/c['artifacts']['glb']['path'];audit=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30);audit['glb_sha256']=H(glb);audit['size_hard_limit_pass']=glb.stat().st_size<=1000000
 (out/'project-glb.json').write_text(json.dumps(audit,indent=2)+'\n');x['project_audit_errors']=audit['errors'];r['assets'][aid]=x
(O/'integrity.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:{'artifacts':all(v['pass'] for v in x['artifacts'].values()),'sheets':all(x['sheet_pixel_identity'].values()),'project_errors':x['project_audit_errors'],'pids':[z['pid'] for z in x['rebuilds']]} for k,x in r['assets'].items()},indent=2))
