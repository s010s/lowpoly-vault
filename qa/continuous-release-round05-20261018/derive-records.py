import json,subprocess,hashlib,posixpath,copy,sys,tempfile,shutil
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
from candidate_profile import create_contract
from validate_candidate import validate_candidate,STATIC_PROFILE,image_size
from qa_glb import read_glb
x=json.loads(Path('/tmp/lpv-round05-audit.json').read_text());out=Path('qa/continuous-release-round05-20261018');out.mkdir(parents=True,exist_ok=True);allpins={};root=Path.cwd()
def sha(b):return hashlib.sha256(b).hexdigest()
def get(ref,p):return subprocess.check_output(['git','show',ref+':'+p])
def save(p,v):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p.read_bytes())}
def put(ref,p,dest=None):
 b=get(ref,p);t=Path(dest or p)
 if t.exists():assert t.read_bytes()==b,('conflict',str(t))
 else:t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(b)
 allpins[str(t)]={'path':str(t),'sha256':sha(b),'bytes':len(b),'git_commit':ref};return {'path':str(t),'sha256':sha(b)}
for a in x['assets']:
 for pin in a['evidence']:
  p=pin['path'];dest=p if p.startswith(('assets/','production/','qa/'))else f"production/continuous-release-round05-20261018/source-snapshots/{a['id']}/"+p
  put(a['source_commit'],p,dest)
  if dest!=p:pin['original_path']=p;pin['path']=dest
for b in x['batches']:
 if b.get('handoff'):put(b['handoff_commit'],b['handoff']['path'])
 qa=b['review_commit'];report=b['review']['path'];prefix=posixpath.dirname(report)+'/'
 for p in subprocess.check_output(['git','ls-tree','-r','--name-only',qa],text=True).splitlines():
  include=(p.startswith(prefix)if True else p==report or p.startswith(prefix+'independent-evidence/'))
  if include:put(qa,p)
for a in x['assets']:
 id=a['id'];folder=Path('production/continuous-release-round05-20261018/records')/id;raw=json.loads(Path(a['candidate']['path']).read_text());refs_pin=raw['artifacts']['references'];refs=json.loads(get(a['source_commit'],refs_pin['path']));normalized=copy.deepcopy(refs)
 assert all(ref['use']=='consulted-only' and ref['url'] and ref['rights_note'] for ref in refs['sources'])
 assert refs['no_incorporated_third_party_assets'] is True
 derived=copy.deepcopy(raw)
 if raw.get('textures'):
  doc,binary,_=read_glb(raw['artifacts']['glb']['path']);texture_rows=[]
  for index,image in enumerate(doc.get('images',[])):
   assert 'uri'not in image and 'bufferView'in image
   view=doc['bufferViews'][image['bufferView']];start=view.get('byteOffset',0);image_bytes=binary[start:start+view['byteLength']];match=next(t for t in raw['textures']if t['sha256']==sha(image_bytes));assert Path(match['path']).read_bytes()==image_bytes;width,height=image_size(image_bytes)
   sid='original-'+id+'-pigment';author=a['metadata']['author'];license=a['metadata']['license'];generator=raw['artifacts']['generator'];url=f"https://github.com/s010s/lowpoly-vault/blob/{a['source_commit']}/{generator['path']}"
   normalized['sources'].append({'id':sid,'title':'Original procedural valley pigment authored by the asset maker','url':url,'license':license,'creator':author,'use':'original-authored incorporated texture','rights_note':'Applies only to the owner-authored image generated and packed by this frozen generator; no license is asserted for consulted third-party references.'})
   texture_rows.append({**match,'image_index':index,'width':width,'height':height,'byte_length':len(image_bytes),'provenance':{'source_id':sid,'creator':author,'license':license,'usage':'Original procedural image embedded in the same owner-authored asset; not consulted-source media.'}})
  assert len(texture_rows)==len(raw['textures']);derived['textures']=texture_rows;a['texture_provenance']=texture_rows
 new_refs=put(a['source_commit'],refs_pin['path'],str(folder/'references.json'));derived['artifacts']['references']=new_refs
 redirects={}
 for role,pin in derived['artifacts'].items():
  path=pin['path']
  if not path.startswith(('assets/','production/','qa/')):
   snapshot=f'production/continuous-release-round05-20261018/source-snapshots/{id}/'+path;assert Path(snapshot).exists();redirects[role]={'source_path':path,'snapshot_path':snapshot};pin['path']=snapshot
 derived['derivation_provenance']={'source_candidate':{k:a['candidate'][k]for k in ['path','sha256']},'source_commit':a['source_commit'],'scope':'Reference-use spelling, archival dependency paths and measured owner-authored embedded-image provenance only. Stages, blockers, evidence and approval are unchanged.','dependency_redirects':redirects}
 for k in ['stages','blockers','evidence','approval']:assert derived[k]==raw[k]
 a['profile_candidate']=save(folder/'candidate.json',derived);contract=create_contract(root,a['profile_candidate']['path'],'production/policies/qa-passed-batch-publication-20261018.json');a['profile_contract']=save(out/f'profile-checks/{id}-contract.json',contract);result=validate_candidate(a['profile_candidate']['path'],root,validation_profile=STATIC_PROFILE,profile_contract=a['profile_contract']['path']);assert result['profile_contract_status']=='pass',(id,result);assert not result['approved_for_brief'];a['profile_result']=save(out/f'profile-checks/{id}-result.json',result);a['profile_outcome']={k:result[k]for k in ['valid','approved_for_brief','errors','approval_blockers','profile_contract_status']}
 # Preserve the original legacy outcome in an exact source-byte root, without replacing shared code.
 with tempfile.TemporaryDirectory(prefix='lpv-original-profile-')as tmp:
  tr=Path(tmp);p=tr/a['candidate']['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(get(a['source_commit'],a['candidate']['path']))
  for pin in raw['artifacts'].values():
   p=tr/pin['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(get(a['source_commit'],pin['path']))
  old=validate_candidate(a['candidate']['path'],tr);assert not old['valid']and not old['approved_for_brief'];a['original_legacy_result']=save(out/f'profile-checks/{id}-original-legacy.json',old)
 print(id,'profile',result['profile_contract_status'],'valid',result['valid'],'approved',result['approved_for_brief'],'errors',result['errors'],flush=True)
save(out/'source-audit.json',x);save(out/'import-scope.json',{'policy':'Frozen final bundles and independent QA evidence only; shared inputs archived under source-snapshots, no planning queue/state or shared implementation replacement.','selected_files':len(allpins),'pins':list(allpins.values())});print('Selected files',len(allpins))
