# SPDX-License-Identifier: MIT
"""Run copied generator in an isolated tree with Python-level shared-path reads audited."""
import json,os,runpy,sys
from pathlib import Path
source=Path(__file__).resolve().parents[1];base=source.parent;out=base/'out';out.mkdir(exist_ok=True)
allowed=[base]+[Path(os.environ[v]).resolve() for v in ('BLENDER_USER_CONFIG','BLENDER_USER_EXTENSIONS','XDG_CONFIG_HOME','TMPDIR') if os.environ.get(v)]
reads=[];denied=[]
def hook(event,args):
 if event!='open' or not args or not isinstance(args[0],(str,bytes,os.PathLike)):return
 p=Path(os.fsdecode(args[0])).absolute()
 if str(p).startswith('/workspace/'):
  is_allowed=any(p==root or root in p.parents for root in allowed)
  reads.append({'path':str(p.relative_to(base)) if base in p.parents else '<isolated runtime config>','allowed':is_allowed})
  if not is_allowed:
   denied.append(str(p));raise RuntimeError('Undeclared workspace read blocked: '+str(p))
sys.addaudithook(hook)
sys.argv=[str(source/'generate.py'),'--','--output',str(out)]
runpy.run_path(str(source/'generate.py'),run_name='__main__')
report={'status':'PASS' if not denied else 'FAIL','workspace_reads':reads,'denied':denied,
 'scope':'Two copied source-only trees run from different working directories. Python open audit forbids workspace access outside this tree and declared isolated Blender runtime configuration. This is not an OS-level syscall sandbox.'}
(out/'dependency-audit.json').write_text(json.dumps(report,indent=2)+'\n')
