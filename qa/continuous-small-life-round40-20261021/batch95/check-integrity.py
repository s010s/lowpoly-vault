import pathlib,json,hashlib,subprocess,os,datetime,sys
from PIL import Image
S=pathlib.Path('/workspace/shared/lowpoly-batch95-20261020');P=S/'production/small-life-batch95';E=pathlib.Path('/workspace/shared/lowpoly-batch95-evidence');O=pathlib.Path('/workspace/shared/lowpoly-batch95-independent-qa-20261021');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();j=lambda p:json.loads(p.read_text());errors=[];checks=[]
def pin(p,h,label=None):
 p=pathlib.Path(p);p=p if p.is_absolute() else S/p;actual=H(p)if p.is_file()else None;ok=actual==h;checks.append({'path':str(p),'expected_sha256':h,'sha256':actual,'pass':ok,'scope':label});
 if not ok:errors.append(str(p))
 return ok
def tree(d,label):
 if isinstance(d,dict):
  if isinstance(d.get('path'),str)and isinstance(d.get('sha256'),str):pin(d['path'],d['sha256'],label)
  for v in d.values():tree(v,label)
 elif isinstance(d,list):
  for v in d:tree(v,label)
h=j(P/'maker-handoff.json');pin(P/'maker-handoff.json','bf39518270dd1e58b6fa6caa9b9228e1a36c7ce0b5fe7eb9672444c59fcd9991','entry');tree(h,'handoff');freeze=j(P/'original-freeze-manifest.json')
for p,hh in freeze['files'].items():pin(p,hh,'original-freeze')
tree(j(P/'dependencies.json'),'dependency-closure');pin('/workspace/shared/lowpoly-round40-coordination/batch-95-selected-inventory.json',H(P/'batch-95-selected-inventory.json'),'original-inventory')
raw=j(E/'raw-evidence-manifest-v002.json');rawbad=[]
for p,r in raw['files'].items():
 f=E/p
 if not f.exists()or H(f)!=r['sha256']or f.stat().st_size!=r['bytes']:rawbad.append(p)
if rawbad:errors+=rawbad
concept=[];provenance=[]
for a in [x['asset_id']for x in h['items']]:
 b=P/a/'r002';c=j(b/'candidate.json');tree(c,'candidate');tree(j(b/'delivery-brief.json'),'delivery');tree(j(b/'profile-contract.json'),'profile');orig=j(P/a/'r001/original-brief.json');delivery=j(b/'delivery-brief.json');diff={k:{'original':v,'delivery':delivery.get(k)}for k,v in orig.items()if delivery.get(k)!=v};r=j(P/'concepts'/f'{a}-receipt.json');source=pathlib.Path(r['source_path']);concept.append({'asset_id':a,'receipt':r,'copied_original_pixels_identical':source.is_file()and H(source)==H(P/'concepts'/f'{a}-concept.png'),'observed_result_before_freeze':r['result_observed']<freeze['freeze_observed_at']})
 fr=j(b/'qa/final-render-request.json');res=j(b/'qa/final-render-result.json');rm=j(b/'views/render-manifest.json');bi=j(b/'qa/byte-identity.json');sheet=Image.open(b/'views/contact-sheet.png').convert('RGB');rawrender=pathlib.Path(bi['render_raw_directory']);rawbuild=pathlib.Path(bi['raw_build_directory']);views=[]
 for k,f in enumerate(rm['frames']):
  p=b/'views'/f['path'];im=Image.open(p).convert('RGB');x=k%4*512;y=k//4*544;v={'id':f['id'],'path':str(p),'sha256':H(p),'correct_hash':H(p)==f['sha256']==res['outputs'][f['path']]['sha256'],'size_512':im.size==(512,512),'raw_bytes_identical':p.read_bytes()==(rawrender/f['path']).read_bytes(),'sheet_tile_identical':sheet.crop((x,y,x+512,y+512)).tobytes()==im.tobytes()};views.append(v)
 pin(b/'views/render-config.json',rm['config_sha256'],'render-config')
 for role in ['glb','brief','references']:
  assert fr['identity']['inputs'][role]['sha256']==c['artifacts'][role]['sha256'];assert rm['subject'][role+'_sha256']==c['artifacts'][role]['sha256']
 assert res['status']=='succeeded'and res['returncode']==0 and delivery['delivery_bound_at']<fr['created_at']<res['finished_at'];assert len(views)==8 and all(v[k]for v in views for k in ['correct_hash','size_512','raw_bytes_identical','sheet_tile_identical'])
 rawidentity={ext:(rawbuild/f'{a}.{ext}').read_bytes()==(b/'artifacts'/f'{a}.{ext}').read_bytes()for ext in ['glb','blend']};assert all(rawidentity.values())
 rebuilds=[]
 for label in ['a','b']:
  er=j(b/f'qa/rebuild-{label}-execution.json');rr=j(b/f'qa/rebuild-{label}-request.json');rz=j(b/f'qa/rebuild-{label}-result.json');assert rz['returncode']==0 and rz['status']=='succeeded'and er['generator_sha256']==c['artifacts']['generator']['sha256']and er['config_sha256']==c['artifacts']['config']['sha256'];rebuilds.append({'label':label,'pid':er['pid'],'started_at':er['started_at'],'finished_at':er['finished_at'],'fingerprint':rr['fingerprint'],'output_sha256':rz['outputs'][a+'/'+a+'.glb']['sha256']})
 assert rebuilds[0]['pid']!=rebuilds[1]['pid']
 provenance.append({'asset_id':a,'derived_brief_diff':diff,'subject':rm['subject'],'bound_at':delivery['delivery_bound_at'],'request_at':fr['created_at'],'render_finished_at':res['finished_at'],'request_fingerprint_valid':hashlib.sha256(json.dumps(fr['identity'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()==fr['fingerprint']==res['fingerprint'],'views':views,'raw_artifacts_identical':rawidentity,'maker_rebuilds':rebuilds})
assert all(x['copied_original_pixels_identical']and x['observed_result_before_freeze']for x in concept)
initial=[]
for p in(E/'build-queue').glob('**/request.json'):
 r=j(p);initial.append({'asset_id':r['identity']['job']['asset_id'],'created_at':r['created_at'],'generator_sha256':r['identity']['inputs']['generator']['sha256']})
assert all(x['created_at']>freeze['freeze_observed_at']for x in initial)
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0');git=lambda *args:subprocess.check_output(['git','-c','protocol.allow=never','-C',str(S),*args],env=env)
head=git('rev-parse','HEAD').decode().strip();status=git('status','--porcelain=v1').decode();staged=git('diff','--cached','--name-only').decode();assert head=='5899a9f5c9e57341b42dee07ca564134bc1cbadc'and not status and not staged
entries=git('ls-tree','-r','-z','HEAD').split(b'\0');committed=[]
for e in entries:
 if not e:continue
 meta,name=e.split(b'\t');mode,typ,oid=meta.split();f=S/name.decode()
 if f.is_file()and not f.is_symlink():
  rawbytes=f.read_bytes();oh=hashlib.sha1(b'blob '+str(len(rawbytes)).encode()+b'\0'+rawbytes).hexdigest();ok=oh==oid.decode();committed.append({'path':name.decode(),'blob':oid.decode(),'local_blob':oh,'match':ok})
  if not ok:errors.append(name.decode())
report={'checked_at':now(),'head':head,'worktree_clean':not status,'index_clean':not staged,'checks':checks,'raw_local_manifest_file_count':len(raw['files']),'raw_local_manifest_mismatches':rawbad,'committed_local_files':committed,'concept_timeline':concept,'immutable_freeze_at':freeze['freeze_observed_at'],'first_geometry_queue':initial,'timeline_limit':'Observed request/result receipts and freeze records are coherent; no invented provider timestamp or external cryptographic authorship proof. Filesystem mtimes not used.','render_and_build_provenance':provenance,'errors':errors,'pass':not errors}
(O/'independent-integrity.json').write_text(json.dumps(report,indent=2)+'\n');print('checked pins',len(checks),'raw',len(raw['files']),'committed',len(committed),'errors',errors)
