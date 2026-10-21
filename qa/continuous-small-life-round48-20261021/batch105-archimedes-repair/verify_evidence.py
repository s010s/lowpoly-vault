import json,hashlib,pathlib,os,subprocess,sys,datetime
from PIL import Image
R=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-repair-20261021');Q=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-independent-qa-20261021');D=R/'production/small-life-batch105-archimedes-repair/r002';A=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-repair-evidence');P=pathlib.Path('/workspace/shared/lowpoly-batch105-independent-qa-20261021')
sha=lambda b:hashlib.sha256(b).hexdigest();pin=lambda p:{'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size};load=lambda p:json.loads(p.read_text())
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0');git=lambda *a:subprocess.check_output(['git','-c','protocol.allow=never','-C',str(R),*a],env=env)
assert git('rev-parse','HEAD').decode().strip()=='3b470a4aca963df9ceae39affcc96602707a1180';assert git('status','--porcelain')==b''
base='cc7568aae69c84100837b056ea82314aafcaf525';changed=git('diff','--name-status',base,'HEAD').decode().splitlines();assert len(changed)==93;assert all(x.startswith('A\tproduction/small-life-batch105-archimedes-repair/') for x in changed)
hand=R/'production/small-life-batch105-archimedes-repair/maker-handoff.json';manifest=hand.parent/'submission-manifest.json';freeze=R/'production/small-life-batch105/original-freeze-manifest.json';prior=P/'independent-report.json'
for p,h in [(hand,'23e373e424450beba574ca33e00c5a0a64b20094e7c5c97ea95dd332568d6d54'),(manifest,'1ce33666a24feeeffabb7c3e502d5f73fb3daf1f5a1f4f8f898ba0ee168dd724'),(freeze,'4513b45ecbf59f49a046d176025a1a998cdab1b3cc9d4d9a6fa67454853549e3'),(prior,'5dcd2cd93424713c0895ec0ffc79eff3a0c884fefe3042ada6a0169ca50235bb'),(A/'endpoint-interior-contact.report.json','90c7521025376581fa1c3445c25a1660a5e60d7b1e626d180a412554705cfe89')]:assert pin(p)['sha256']==h
verified=[]
for f in load(manifest)['files']+load(freeze)['files']:
 p=R/f['path'];blob=git('show','HEAD:'+f['path']);assert sha(blob)==f['sha256'] and len(blob)==f['bytes'];assert not p.exists() or blob==p.read_bytes();verified.append(dict(f,verified_from='offline committed blob',worktree_materialized=p.exists()))
for f in load(freeze)['files']:assert git('show',base+':'+f['path'])==git('show','HEAD:'+f['path'])
inherited=[]
for aid,rev in [('penniretepora','r001'),('constellaria','r002'),('cystodictya','r003')]:
 prefix=f'production/small-life-batch105/{aid}/{rev}';a=git('ls-tree','-r',base,'--',prefix);b=git('ls-tree','-r','HEAD','--',prefix);assert a==b;files=[]
 for line in a.decode().splitlines():
  meta,p=line.split('\t');mode,kind,oid=meta.split();blob=git('cat-file','blob',oid);assert not (R/p).exists() or blob==(R/p).read_bytes();files.append({'path':p,'sha256':sha(blob),'bytes':len(blob),'git_blob_oid':oid})
 priorasset=next(a for a in load(prior)['assets'] if a['asset_id']==aid); assert priorasset['bounded_static_result']=='pass'
 for role,f in priorasset['pins'].items():
  if isinstance(f,dict) and 'path' in f:assert sha(git('show','HEAD:'+f['path']))==f['sha256']
 inherited.append({'asset_id':aid,'revision':rev,'preserved_prior_verdict':'bounded static PASS, not newly re-reviewed','prior_pins':priorasset['pins'],'files':files})
assert sum(len(a['files']) for a in inherited)==212
# The complete original Archimedes r001 tree is inherited unmodified, preserving failure subject.
op='production/small-life-batch105/archimedes/r001';assert git('ls-tree','-r',base,'--',op)==git('ls-tree','-r','HEAD','--',op)
cand=load(D/'candidate.json');triplet=load(D/'candidate-binding.json')['subject']
for f in cand['artifacts'].values():assert sha((R/f['path']).read_bytes())==f['sha256']
orig=load(D/'original-brief.json');brief=load(D/'delivery-brief.json');assert (D/'original-brief.json').read_bytes()==(R/op/'original-brief.json').read_bytes();assert (D/'references.json').read_bytes()==(R/op/'references.json').read_bytes();assert all(brief[k]==v for k,v in orig.items() if k!='brief_version')
# Check every manifest subject and the exact lossless sheet pixels.
visual=[];bind=load(D/'candidate-binding.json')['bound_at'];sheet=Image.open(D/'views/lossless-contact-sheet.png').convert('RGBA');proof=load(D/'views/contact-sheet-proof.json')
for sub in ['views','views/views-1','views/views-2','views/views-3','views/views-4','lower-end','upper-end']:
 p=D/sub/'render-manifest.json';m=load(p);assert m['subject']==triplet;assert m['source_glb_sha256']==triplet['glb_sha256'];assert m['created_at']>=bind
 for f in m['frames']:
  fp=p.parent/f['path'];assert sha(fp.read_bytes())==f['sha256'];im=Image.open(fp);assert im.size==(512,512);visual.append(pin(fp))
for cell in proof['cells']:
 im=Image.open(D/'views'/cell['source']).convert('RGBA');assert sheet.crop(cell['pixel_rect']).tobytes()==im.tobytes()
rebuilds=[]
for label in ['a','b']:
 ex=load(D/f'qa/rebuild-{label}/execution.json');res=load(D/f'qa/rebuild-{label}/result.json');output=pathlib.Path(ex['argv'][ex['argv'].index('--output')+1]);assert res['status']=='succeeded' and res['returncode']==0;checks=[]
 for rel,meta in res['outputs'].items():
  p=output/rel;assert pin(p)['sha256']==meta['sha256'] and p.stat().st_size==meta['bytes'];checks.append(pin(p))
 assert (output/'archimedes/archimedes.glb').read_bytes()==(D/'artifacts/archimedes.glb').read_bytes();assert load(output/'execution.json')==ex
 rebuilds.append({'label':label,'execution':ex,'result':res,'verified_retained_outputs':checks})
assert rebuilds[0]['execution']['pid']!=rebuilds[1]['execution']['pid'];assert rebuilds[0]['execution']['finished_at_executor_clock']<rebuilds[1]['execution']['started_at_executor_clock']
r={'status':'pass','source_commit':git('rev-parse','HEAD').decode().strip(),'base_commit':base,'branch':git('branch','--show-current').decode().strip(),'git_status':'','changed_paths':changed,'verified_manifest_and_freeze_files':verified,'manifest':pin(manifest),'maker_handoff':pin(hand),'original_freeze':pin(freeze),'prior_qa':pin(prior),'inherited_assets':inherited,'all_212_inherited_files_byte_identical':True,'original_archimedes_tree_unchanged':True,'original_failure':'QA105-ARCH-TERMINAL-TAPER remains r001 FAIL/REVISE','all_original_criteria_unchanged':True,'render_bindings_and_sheet_pixels_verified':True,'visual_files':visual,'two_distinct_actual_process_rebuilds':rebuilds,'rebuild_limitations':'Retained execution records and all output bytes reverified, not two fresh rebuilds performed by this reviewer. PIDs and timestamps are executor attestations, not provider-independent cryptographic attestations.','postcommit_contact_supplement':pin(A/'endpoint-interior-contact.report.json')}
(Q/'evidence-integrity.json').write_text(json.dumps(r,indent=2)+'\n');(Q/'RECOVERY.txt').write_text('Stage 1 complete: candidate commit, all93 additions, all23 frozen files and all212 inherited accepted files verified. Exact render binding, sheet pixels and both retained rebuild outputs verified. Original r001 failure preserved. Fresh source geometry and runtime checks next.\n');print('PASS:93 additions,',len(verified),'manifest/freeze files;212 inherited;8 sheet cells;2 distinct retained builds')
