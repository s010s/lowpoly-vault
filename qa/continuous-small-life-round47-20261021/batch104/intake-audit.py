from pathlib import Path
import json,hashlib,subprocess,os
W=Path('/workspace/shared/lowpoly-batch104-20261021');P=W/'production/small-life-batch104';Q=Path(__file__).resolve().parent
E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0');C='6d2ed0f8ebd8a37df619a2d219ba9a03bb16e008'
def git(*args):return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(W),*args],env=E)
H=lambda b:hashlib.sha256(b).hexdigest();records=[]
assert git('rev-parse','HEAD').decode().strip()==C
assert git('show','-s','--format=%P',C).decode().strip()=='43e40fc89f2b369a5f1858e72fa58a0d10318124'
assert not git('status','--porcelain','--untracked-files=no').strip()
man=json.loads((P/'delivery-manifest.json').read_text());hand=json.loads((P/'handoff.json').read_text())
assert H((P/'delivery-manifest.json').read_bytes())=='c61529881176952078877342c6715cec4a7060e5323c0f11d3adfb356760ceac'
assert H((P/'handoff.json').read_bytes())=='4c55c5f92600b54cd4faf6c95fd0ae26fb3995099b72b6d44375e20ca4c047b2'
for r in man['files']:
 p=W/r['path'];raw=p.read_bytes();committed=git('show',C+':'+r['path']);ok=H(raw)==r['sha256']and len(raw)==r['bytes']and committed==raw
 records.append({**r,'local_and_commit_match':ok});assert ok,r['path']
pins=[]
def walk(v):
 if isinstance(v,dict):
  if 'path'in v and'sha256'in v:
   p=Path(v['path']);p=p if p.is_absolute()else W/p;raw=p.read_bytes();ok=H(raw)==v['sha256']and('bytes'not in v or len(raw)==v['bytes']);pins.append({**v,'verified':ok});assert ok,str(p)
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(hand)
dep=[]
for f in ['build-dependencies.json','build-dependencies-v002.json']:
 j=json.loads((P/f).read_text());before=len(pins);walk(j);dep.append({'file':f,'sha256':H((P/f).read_bytes()),'verified_pins':len(pins)-before})
freeze=json.loads((P/'original-freeze-manifest.json').read_text());walk(freeze)
intake={'source_commit':C,'worktree':str(W),'parent':git('show','-s','--format=%P',C).decode().strip(),'branch':git('branch','--show-current').decode().strip(),'handoff_sha256':H((P/'handoff.json').read_bytes()),'delivery_manifest_sha256':H((P/'delivery-manifest.json').read_bytes()),'assets':[]}
for a in hand['items']:
 base=f"production/small-life-batch104/{a['asset_id']}/{a['revision']}";intake['assets'].append({'asset_id':a['asset_id'],'revision':a['revision'],'glb':a['glb']['path'],'glb_sha256':a['glb']['sha256'],'source':a['editableBlend']['path'],'source_sha256':a['editableBlend']['sha256'],'generator':a['generator']['path'],'config':a['config']['path'],'metadata':base+'/artifacts/metadata.json','candidate':a['candidate']['path'],'original_brief':a['original_brief']['path'],'delivery_brief':a['delivery_brief']['path'],'references':a['references']['path'],'views':base+'/views','detail':base+'/detail','qa':base+'/qa'})
 for k in ['config','delivery_brief','candidate']:
  b=json.loads((W/intake['assets'][-1][k]).read_text())
(Q/'final-intake.json').open('x').write(json.dumps(intake,indent=2)+'\n')
r={'source_commit':C,'tracked_clean':True,'manifest_files':records,'manifest_count':len(records),'manifest_bytes':sum(x['bytes']for x in records),'handoff_and_dependency_and_freeze_pins':pins,'dependency_manifests':dep,'final_manifest_committed_matches':git('show',C+':production/small-life-batch104/delivery-manifest.json')==(P/'delivery-manifest.json').read_bytes(),'original_freeze_sha256':H((P/'original-freeze-manifest.json').read_bytes())}
(Q/'final-intake-integrity.json').open('x').write(json.dumps(r,indent=2)+'\n')
print('Independent final intake verified',len(records),'manifest files',sum(x['bytes']for x in records),'bytes;',len(pins),'recursive pins incl dependencies/freeze')
