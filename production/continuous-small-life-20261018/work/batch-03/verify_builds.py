# SPDX-License-Identifier: MIT
"""Actual bounded source reopen plus two isolated deterministic Blender rebuilds."""
import subprocess,json,hashlib,sys,time
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
BASE=ROOT/'production/continuous-small-life-20261018';WORK=BASE/'work/batch-03';QA=ROOT/'qa/continuous-small-life-20261018/batch-03'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd,log):
 t=time.monotonic()
 with log.open('x') as f:r=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError(str(cmd)+' failed; see '+str(log))
 return {'command':cmd,'returncode':r.returncode,'wall_seconds':time.monotonic()-t,'log':str(log.relative_to(ROOT)),'log_sha256':digest(log)}
for slug in sys.argv[1:] or ['cephalaspis','saccocoma','archaeocidaris','onoclea']:
 rev='r002' if slug=='onoclea' else 'r001';a=ROOT/'assets/candidates/continuous-small-life-20261018/batch-03'/slug/rev/slug;out=QA/slug/'verification';out.mkdir(parents=True,exist_ok=False)
 generator=WORK/'build_batch03.py';config=BASE/'items'/slug/'build-config.json';g_hash=digest(generator);c_hash=digest(config);original=audit_glb(a/(slug+'.glb'),14000,6,30);assert not original['errors']
 cmd=['blender','-b','-t','2','--disable-autoexec','--python-exit-code','1','--python','scripts/check_source_export.py','--','--source',str(a/(slug+'.blend')),'--glb',str(a/(slug+'.glb')),'--output',str(out/'source-export.json')]
 reopen=run(cmd,out/'source-export.txt');records=[]
 for n in [1,2]:
  target=Path('/tmp/batch03-semantic-rebuild')/('run'+str(n));cmd=['blender','-b','-t','2','--python-exit-code','1','--python',str(generator),'--','--asset',slug,'--output',str(target),'--no-preview'];execution=run(cmd,out/('rebuild-'+str(n)+'.txt'))
  b=target/slug/rev/slug/(slug+'.glb');rebuilt=audit_glb(b,14000,6,30);match=original['semantic_sha256']==rebuilt['semantic_sha256'];assert not rebuilt['errors'] and match
  records.append({**execution,'rebuilt_sha256':rebuilt['sha256'],'semantic_sha256':rebuilt['semantic_sha256'],'semantic_match':match,'bytes_identical':original['sha256']==rebuilt['sha256'],'rebuilt_glb_bytes':b.stat().st_size})
 assert digest(generator)==g_hash and digest(config)==c_hash
 report={'status':'pass','asset_id':slug,'revision':rev,'glb_sha256':original['sha256'],'source_sha256':digest(a/(slug+'.blend')),'generator_sha256':g_hash,'config_sha256':c_hash,'helper_sha256':digest(ROOT/'scripts/asset_common.py'),'blender':'4.3.2','threads_per_process':2,'rebuild_count':2,'source_reopen_execution':reopen,'rebuilds':records,'semantic_sha256':original['semantic_sha256'],'scope':'Actual source reopen, axis-converted bounds/triangles, and two executed isolated rebuilds. Not independent aesthetic or factual review.'}
 (out/'reproducibility.json').write_text(json.dumps(report,indent=2)+'\n');print(slug,'two actual rebuilds and source reopen passed',flush=True)
