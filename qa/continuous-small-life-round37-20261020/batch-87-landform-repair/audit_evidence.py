import pathlib,json,hashlib,datetime,subprocess,sys
from PIL import Image
R=pathlib.Path('/workspace/shared/lowpoly-batch87-landform-repair-20261020');P=R/'production/batch87-landform-repair';O=pathlib.Path('/workspace/shared/lowpoly-batch87-landform-repair-independent-qa-20261020');L=pathlib.Path('/workspace/shared/lowpoly-batch87-landform-repair-raw');h=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();j=lambda p:json.loads(pathlib.Path(p).read_text());checks=[];errors=[]
def ck(ok,label):
 checks.append({'check':label,'pass':bool(ok)})
 if not ok:errors.append(label)
def walk(x,base=R):
 if isinstance(x,dict):
  if 'path'in x and 'sha256'in x:
   p=pathlib.Path(x['path']);p=p if p.is_absolute()else base/p;ck(p.is_file()and h(p)==x['sha256'],'bound '+str(p))
  for v in x.values():walk(v,base)
 elif isinstance(x,list):
  for v in x:walk(v,base)
H=j(P/'maker-handoff.json');walk(H);walk(j(P/'original-byte-identity.json'));walk(j(P/'premodel-freeze-v002.json'));walk(j(P/'dependencies.json'));raw=j(L/'raw-evidence-manifest.json')
for f in raw['files']:ck((L/f['path']).is_file()and h(L/f['path'])==f['sha256']and (L/f['path']).stat().st_size==f['bytes'],'raw '+f['path'])
freeze=j(R/'production/small-life-batch87/original-freeze-manifest.json')
for f,d in freeze['files'].items():ck(h(R/f)==d,'original freeze '+f)
changed=subprocess.check_output(['git','-C',str(R),'diff','14f14a9e0ab6c5bacab7c746d27186a8ea4de2f0','HEAD','--','production/small-life-batch87'],text=True);ck(not changed,'all tracked original production untouched versus original commit')
# Track complete local module dependency closure from entry points by AST imports.
import ast
files={x['path']:x['sha256']for x in j(P/'dependencies.json')['files']};unclosed=[];closure=[]
for rel in files:
 if not rel.endswith('.py'):continue
 for n in ast.walk(ast.parse((R/rel).read_text())):
  names=[n.module.split('.')[0]]if isinstance(n,ast.ImportFrom)and n.module else [a.name.split('.')[0]for a in n.names]if isinstance(n,ast.Import)else []
  for name in names:
   possible=[R/'scripts'/(name+'.py'),(R/rel).parent/(name+'.py')]
   for local in possible:
    if local.exists():
     lr=str(local.relative_to(R));closure.append({'importer':rel,'dependency':lr,'sha256':h(local)});ck(lr in files and files.get(lr)==h(local),'dependency closure '+rel+' -> '+lr)
items=[]
for a in H['items']:
 aid=a['asset_id'];rev=a['revision'];p=P/aid/rev;orig=j(R/'production/small-life-batch87'/aid/'r001/original-brief.json');cfg=j(p/'config.json');brief=j(p/'delivery-brief.json');refs=j(p/'references.json');walk(refs);walk(j(p/'candidate.json'));walk(j(p/'qa/technical.report.v002.json'))
 ck(cfg['parameters']==orig['parameters']==brief['parameters'],aid+' original parameter values preserved');ck(cfg['art_target_bounds_blender_xyz_m']==orig['scale']['art_target_bounds_blender_xyz_m'],aid+' art target preserved')
 for k in orig:
  if k=='brief_version':continue
  ck(orig[k]==brief[k],aid+' derived preserves original '+k)
 subject={k+'_sha256':a['artifacts'][k]['sha256']for k in ['glb','brief','references']};subject['revision']=rev
 subj=j(p/'subject.json');ck(all(subj[k]==v for k,v in subject.items()),aid+' final subject')
 prov=j(p/'qa/execution-provenance.json');walk(prov);rebuilds=[]
 for rep in prov['two_distinct_real_rebuilds']:
  d=pathlib.Path(rep['raw_directory']);req=j(d/'request.json');res=j(d/'result.json');ex=j(d/'outputs/execution.json')
  ck(res['status']=='succeeded'and res['returncode']==0,aid+' rebuild '+rep['label']+' succeeded');ck(req['created_at']<=res['started_at']<=ex['started_at']<ex['finished_at']<=res['finished_at'],aid+' rebuild '+rep['label']+' chronological process')
  ck(req['argv'][0]=='/usr/bin/flock'and req['argv'][1]=='/tmp/lowpoly-production-blender.lock'and req['argv'][req['argv'].index('--threads')+1]=='2',aid+' rebuild resource lock '+rep['label'])
  walk(req['identity']['inputs']);
  for f,rec in res['outputs'].items():ck(h(d/'outputs'/f)==rec['sha256'],aid+' rebuild output '+rep['label']+' '+f)
  ck(h(d/'outputs'/aid/(aid+'.glb'))==a['artifacts']['glb']['sha256'],aid+' rebuild exact GLB '+rep['label']);ck(ex['generator_sha256']==a['artifacts']['generator']['sha256']and ex['config_sha256']==a['artifacts']['config']['sha256'],aid+' rebuild executed exact config/generator '+rep['label'])
  for kind,key in [('request','request'),('result','result'),('execution','outputs/execution')]:ck(h(R/rep[kind]['path'])==h(d/(key+'.json')),aid+' rebuild copied '+kind+' '+rep['label'])
  rebuilds.append({'label':rep['label'],'request':str(d/'request.json'),'pid':ex['pid'],'queue_pid':res['pid'],'started_at':ex['started_at'],'finished_at':ex['finished_at'],'byte_equal':h(d/'outputs'/aid/(aid+'.glb'))==a['artifacts']['glb']['sha256']})
 ck(len(rebuilds)==2 and rebuilds[0]['pid']!=rebuilds[1]['pid']and rebuilds[0]['request']!=rebuilds[1]['request'],aid+' two distinct process rebuilds')
 frames=[];render_records=[]
 for tag,pointer,expected,manpath in [('final',prov['final_render_raw'],orig['required_views'],p/'views/render-manifest.json'),('bottom',prov['supplemental_bottom_raw'],['bottom'],p/'qa/supplemental-bottom-raw/render-manifest.json')]:
  d=pathlib.Path(pointer).parent;req=j(d/'request.json');res=j(d/'result.json');man=j(manpath);rm=j(d/'outputs/views/render-manifest.json');walk(req['identity']['inputs']);ck(res['status']=='succeeded'and res['returncode']==0,aid+' '+tag+' render succeeded');ck(subj['bound_at']<req['created_at']<=res['started_at']<res['finished_at'],aid+' fixed final subject precedes '+tag+' render');ck(man==rm,aid+' exact raw manifest '+tag);ck(man['subject']==subject,aid+' exact final subject on '+tag+' manifest');ck([f['id']for f in man['frames']]==expected,aid+' actual frame list '+tag)
  ck(req['argv'][0]=='/usr/bin/flock'and req['argv'][1]=='/tmp/lowpoly-production-blender.lock'and req['argv'][req['argv'].index('--threads')+1]=='2',aid+' render resource lock '+tag)
  for role in ['glb','brief','references']:ck(req['identity']['inputs'][role]['sha256']==subject[role+'_sha256'],aid+' render exact '+tag+' '+role)
  for f,rec in res['outputs'].items():ck(h(d/'outputs'/f)==rec['sha256'],aid+' render output '+tag+' '+f)
  for f in man['frames']:
   v=p/'views'/f['path'];ck(h(v)==f['sha256']==h(d/'outputs/views'/f['path']),aid+' final raw image hash '+f['id']);im=Image.open(v);ck(im.size==(512,512),aid+' 512 image '+f['id']);frames.append({'view':f['id'],'path':str(v),'sha256':h(v),'dimensions':list(im.size)})
  render_records.append({'kind':tag,'request':str(d/'request.json'),'pid':res['pid'],'started_at':res['started_at'],'finished_at':res['finished_at'],'bound_at':subj['bound_at']})
 sheet=Image.open(p/'views/contact-sheet.png').convert('RGB');ck(sheet.size==(2048,1088),aid+' full native sheet size')
 for i,view in enumerate(orig['required_views']):
  frame=Image.open(p/'views'/(view+'.png')).convert('RGB');x=(i%4)*512;y=(i//4)*544;ck(sheet.crop((x,y,x+512,y+512)).tobytes()==frame.tobytes(),aid+' lossless 512 sheet cell '+view)
 init=j(p/'qa/initial-build-request.json');initres=j(p/'qa/initial-build-result.json');cf=j(P/'premodel-freeze-v002.json')if aid=='travertine-terrace-pools'else j(p/'premodel-freeze.json');ck(cf['frozen_at']<init['created_at']<=initres['started_at'],aid+' prospective clarification/config freeze precedes new initial build')
 ck(j(P/'measurement-clarification-v002.json')['frozen_at']<init['created_at'],aid+' new measurement definitions precede geometry')
 items.append({'asset_id':aid,'revision':rev,'subject':subject,'frames':frames,'renders':render_records,'rebuilds':rebuilds,'initial_build_started':initres['started_at'],'prospective_freeze':cf['frozen_at']})
r={'created_at_host':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'check_count':len(checks),'errors':errors,'raw_files_rehashed':len(raw['files']),'old_frozen_files_rehashed':len(freeze['files']),'dependency_import_closure':closure,'items':items,'time_note':'Historical maker timestamps preserved as recorded, not inferred from mtime. Independent host clock differs approximately +2 hours from tool clock. Ordering checks compare same recorded domain, not newly fabricated historical times.'};(O/'evidence-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'checks':len(checks),'errors':errors,'closure_edges':len(closure)},indent=2))
