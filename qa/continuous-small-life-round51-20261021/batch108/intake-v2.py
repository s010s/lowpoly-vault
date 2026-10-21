import json,pathlib,hashlib,subprocess,sys,datetime
from PIL import Image,ImageChops
R=pathlib.Path('/workspace/shared/lowpoly-batch108-20261021');O=pathlib.Path(__file__).parent;B=R/'production/batch-108'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
jload=lambda p:json.loads(p.read_text())
sys.path.insert(0,str(R/'scripts'));from qa_glb import audit_glb
from check_reproducibility import compare_rebuild
errs=[];records=[]
def check(name,ok,data=None):
 records.append(dict(check=name,pass_result=bool(ok),observed=data))
 if not ok:errs.append(name)
def git(*args):return subprocess.check_output(['git','-c','protocol.allow=never',*args],cwd=R,env={**__import__('os').environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'})
check('fixed_HEAD',git('rev-parse','HEAD').decode().strip()=='052a965e17a31c42b121bf79d004ac0eed11546b')
check('freeze_pin',sha(B/'original-freeze-manifest.json')=='6606c757270f008ad591a3ec560beceac8dc7624dae10222bd33eb0fe9ff76d8')
for x in jload(B/'original-freeze-manifest.json')['immutable_originals']:
 p=R/x['path'];check('freeze:'+x['path'],sha(p)==x['sha256'] and p.stat().st_size==x['bytes'])
baseline=[]
for p in B.rglob('*'):
 if p.is_file() and '__pycache__' not in str(p):baseline.append(dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size))
(O/'source-baseline.json').write_text(json.dumps(baseline,indent=2)+'\n')
for rec in jload(B/'maker-handoff.json')['assets']:
 a=rec['asset_id'];rev=rec['revision'];d=B/a/rev;c=jload(d/'candidate.json');od=O/a;od.mkdir(exist_ok=True)
 for name,x in c['artifacts'].items():check(a+':artifact:'+name,sha(R/x['path'])==x['sha256'])
 for x in c['evidence']:check(a+':evidence:'+x['id'],sha(R/x['path'])==x['sha256'])
 for group in ['views','details']:
  m=jload(d/group/'render-manifest.json');check(a+':'+group+':subject',m.get('source_glb_sha256')==rec['triplet']['glb_sha256'],{k:v for k,v in m.items() if k not in ['frames']})
  for f in m['frames']:
   p=d/group/f['path'];check(a+':'+group+':'+f['id'],sha(p)==f['sha256'] and Image.open(p).size==(f['width'],f['height']))
 # Pixel exact sheet tiles retain labels in margins; find positions from original renderer.
 sheet=Image.open(d/'views/contact-sheet.png').convert('RGBA');tiles=[]
 for i,v in enumerate(['hero','reversehero','front','side','rear','top','clay','silhouette']):
  f=Image.open(d/'views'/f'{v}.png').convert('RGBA');x=i%4*512;y=i//4*(sheet.height//2);ok=ImageChops.difference(f,sheet.crop((x,y,x+512,y+512))).getbbox() is None;tiles.append(ok)
 check(a+':lossless_sheet_tiles',all(tiles),{'size':sheet.size,'tiles':tiles})
 glb=d/'artifacts'/f'{a}.glb';audit=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30);(od/'fresh-project-audit.json').write_text(json.dumps(audit,indent=2)+'\n');check(a+':project',not audit['errors'],audit['errors'])
 rebuilds=[]
 for letter in ['a','b']:
  q=d/'qa'/f'rebuild-{letter}';e=jload(q/'execution.json');req=jload(q/'request.json');res=jload(q/'result.json');outpath=pathlib.Path(e['argv'][e['argv'].index('--output')+1]);files=list(outpath.rglob(f'{a}.glb'));check(a+':rebuild_'+letter+':actual_binary_exists',len(files)==1)
  if not files:continue
  output=next(k for k in res['outputs'] if k.endswith(f'{a}.glb'))
  report=compare_rebuild(glb,files[0],R/c['artifacts']['generator']['path'],R/c['artifacts']['config']['path'],q/'request.json',q/'result.json',output,R)
  (od/f'rehashed-rebuild-{letter}.json').write_text(json.dumps(report,indent=2)+'\n');check(a+':rebuild_'+letter,report['status'] in ['pass','pass_with_warnings'],report['errors']);rebuilds.append(e)
 check(a+':distinct_rebuild_processes',len(rebuilds)==2 and rebuilds[0]['pid']!=rebuilds[1]['pid'],rebuilds)
 gen=jload(B/'concepts'/f'{a}-generation-record.json');orig=pathlib.Path(gen['originalRuntimePath']);check(a+':genuine_concept_original_bytes',orig.is_file() and sha(orig)==gen['imageSha256'])
(O/'intake-v2.json').write_text(json.dumps(dict(status='pass' if not errs else 'fail',created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),records=records,errors=errs),indent=2)+'\n');print('INTAKE',len(records),'checks; errors',errs)
