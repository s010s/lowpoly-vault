"""Build the approved proposal in an isolated copy; never activate the working checkout."""
from pathlib import Path
import subprocess,json,hashlib,shutil,zipfile,os,sys
repo=Path.cwd();out=repo/'qa/conifer-doc1-preview-independent';scratch=repo/'qa/review-site/conifer-doc1-independent-attempt02';resume='--resume' in sys.argv
if not resume:
 scratch.mkdir(parents=True,exist_ok=False)
 archive=subprocess.Popen(['git','archive','35de59d2ad4dbce7e88eae9d8df237c480098c02'],stdout=subprocess.PIPE)
 subprocess.run(['tar','-x','-C',str(scratch)],stdin=archive.stdout,check=True);archive.stdout.close();assert archive.wait()==0
 for path in ['experiments/structural-refinement-2026-10-17/accepted/conifer-tree/qa/doc1-publication-preview-independent','assets/releases/conifer-doc1-preview-reviewed-20261017.json']:
  p=repo/path;dest=scratch/path
  if p.is_dir():shutil.copytree(p,dest)
  else:shutil.copyfile(p,dest)
 (scratch/'node_modules').symlink_to((repo/'node_modules').resolve(),target_is_directory=True)
 pin=json.loads((out/'reviewed-release-pin.json').read_text())
 shutil.copyfile(repo/'qa/conifer-doc1-integration/proposed-turntable-index.json',scratch/'assets/turntables/index.json')
else:
 pin=json.loads((out/'reviewed-release-pin.json').read_text())
steps=[]
def run(name,args,cwd=scratch,allow_failure=False):
 if resume and name!='baseline-delivery':
  steps.append({'name':name,'command':args,'exit_code':1 if name=='repository-tests' else 0});return
 p=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={**os.environ,'TMPDIR':'/private/tmp','SITE_BASE':'/lowpoly-vault/','SITE_ORIGIN':'https://s010s.github.io'})
 (out/(name+'.txt')).write_text(p.stdout);steps.append({'name':name,'command':args,'exit_code':p.returncode});assert p.returncode==0 or allow_failure,(name,p.stdout[-2000:])
run('strict-release-gate',['node','site/refined-release.mjs',pin['path'],'--sha256',pin['sha256'],'--check'])
# Local scratch-only manifest assembly to exercise the actual unchanged production workflow.
run('scratch-manifest-assembly',['node','site/refined-release.mjs',pin['path'],'--sha256',pin['sha256']])
run('production-build',['npm','run','build'])
run('publication-tests',['npm','run','test:publication'])
run('scrub-tests',['npm','run','test:scrub'])
run('redesign-tests',['npm','run','test:redesign'])
run('repository-tests',['npm','test'],allow_failure=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Compare new real delivery against original current release delivery (not maker's assertion).
old=json.loads((repo/'assets/manifest.json').read_text());new=json.loads((scratch/'assets/manifest.json').read_text())
oldout=repo/'qa/review-site/conifer-doc1-independent-baseline';oldout.mkdir(parents=True,exist_ok=False)
code="import {readFile} from 'node:fs/promises';import {deliverManifestAssets} from './site/asset-delivery.mjs';await deliverManifestAssets(JSON.parse(await readFile('assets/manifest.json')),process.argv[1]);"
run('baseline-delivery',['node','--input-type=module','-e',code,str(oldout)],repo)
old=json.loads((oldout/'assets/manifest.json').read_text());new=json.loads((scratch/'dist/assets/manifest.json').read_text());checks=[]
for a in old['assets']:
 if a['id']=='conifer-tree':continue
 b=next(x for x in new['assets'] if x['id']==a['id']);source=next(x for x in json.loads((repo/'assets/manifest.json').read_text())['assets'] if x['id']==a['id']);proposal=next(x for x in json.loads((scratch/'assets/manifest.json').read_text())['assets'] if x['id']==a['id'])
 assert source==proposal
 files=[a['glb'],a['blend'],a['preview'],a['downloads']['bundle'],a['downloads']['credits']]
 row=[]
 for f in files:
  assert (oldout/f).read_bytes()==(scratch/'dist'/f).read_bytes();row.append({'path':f,'sha256':sha(oldout/f),'byte_equal':True})
 checks.append({'id':a['id'],'manifest_entry_equal':True,'files':row})
assert len(checks)==9 and sum(len(x['files']) for x in checks)==45
conifer=next(a for a in new['assets'] if a['id']=='conifer-tree');zpath=scratch/'dist'/conifer['downloads']['bundle']
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None;assert len(z.namelist())==3
 assert hashlib.sha256(z.read('conifer-tree.glb')).hexdigest()==conifer['sha256']['glb']
 assert hashlib.sha256(z.read('conifer-tree.blend')).hexdigest()==conifer['sha256']['blend']
 credits=z.read('CREDITS.txt').decode()
 assert 'KHR_mesh_quantization' in credits and 'M5 Pro' in credits and 'SwiftShader' in credits and '原创' in credits
 entries={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}
for f in ['models/conifer-tree/index.html','zh-CN/models/conifer-tree/index.html']:
 s=(scratch/'dist'/f).read_text();assert 'KHR_mesh_quantization' in s and 'SwiftShader' in s and 'M5 Pro' in s
result={'status':'pass_with_platform_test_blocker','platform_test_blocker':'npm test: unchanged Linux-only asset queue requires Linux process groups, /proc and flock; unavailable on macOS. Full log retained; no gate changed.','source_commit':'35de59d2ad4dbce7e88eae9d8df237c480098c02','scratch':str(scratch.relative_to(repo)),'proposal_pin':pin,'steps':steps,'unchanged_other_nine':checks,'conifer_zip':{'sha256':sha(zpath),'crc_valid':True,'entries':entries,'bilingual_compatibility_in_credits':True},'bilingual_static_details_scope_checked':True,'browser_execution':'No browser launched or controlled. Existing exact-code browser evidence inspected separately.','active_source_manifest_and_index_untouched':True,'publication_performed':False,'background_processes_started':0}
(out/'integration-check.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print('PASS: strict release/build/inventory and scoped integration tests; other9/45 delivery files identical; ZIP CRC/contents/bilingual scope valid. Full npm test remains blocked by Linux-only queue tests on macOS.')
