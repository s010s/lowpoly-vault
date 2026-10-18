# SPDX-License-Identifier: MIT
"""Run isolated headless rebuilds, reopen Blend, and compare actual semantic digests."""
import subprocess,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
out=ROOT/'qa/small-fauna-trio-v2/final-validation-r2';out.mkdir(parents=True,exist_ok=True);base=ROOT/'assets/candidates/small-fauna-trio-v2';scratch=Path('/workspace/small-fauna-runtime/rebuild')
for s in ['diplomystus','burgessomedusa','kalligramma']:
 d=base/s
 cmd=['blender','-b','-t','3','--python-exit-code','1','--python',str(ROOT/'production/small-fauna-trio-v2/build_trio.py'),'--','--asset',s,'--output',str(scratch),'--no-preview']
 with (out/(s+'-rebuild.txt')).open('w') as f:subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
 a=audit_glb(d/(s+'.glb'));b=audit_glb(scratch/s/(s+'.glb'))
 report={'status':'pass' if a['semantic_sha256']==b['semantic_sha256'] else 'fail','generator_sha256':hashlib.sha256((ROOT/'production/small-fauna-trio-v2/build_trio.py').read_bytes()).hexdigest(),'delivered_sha256':a['sha256'],'rebuilt_sha256':b['sha256'],'semantic_sha256':a['semantic_sha256'],'rebuilt_semantic_sha256':b['semantic_sha256'],'command':cmd,'execution_returncode':0,'bytes_identical':a['sha256']==b['sha256'],'semantic_match':a['semantic_sha256']==b['semantic_sha256'],'limitation':'Blend byte identity is not required; geometry/material/scene digest compared.'}
 (out/(s+'-reproducibility.json')).write_text(json.dumps(report,indent=2)+'\n');assert report['status']=='pass'
 cmd=['blender','-b','-t','3','--disable-autoexec','--python-exit-code','1','--python','scripts/check_source_export.py','--','--source',str(d/(s+'.blend')),'--glb',str(d/(s+'.glb')),'--output',str(out/(s+'-source-export.json'))]
 with (out/(s+'-source-export.txt')).open('w') as f:subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
 print(s,'rebuild and Blend reopen passed',flush=True)
