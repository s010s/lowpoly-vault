import pathlib,json,sys,hashlib,datetime,ast,os
from PIL import Image
S=pathlib.Path('/workspace/shared/lowpoly-batch94-20261020');P=S/'production/batch94';O=pathlib.Path('/workspace/shared/lowpoly-batch94-independent-qa-20261020');sys.path.insert(0,str(S/'scripts'));from qa_glb import audit_glb;from validate_candidate import check_brief,STATIC_PROFILE
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();R=lambda p:json.loads(p.read_text());records=[]
for a in R(P/'maker-handoff.json')['selected_assets']:
 B=S/a['path'];aid=a['asset_id'];D=O/aid;D.mkdir(exist_ok=True);errors=[];binding=R(B/'preproof-binding.json');brief=R(B/'candidate-brief.json');orig=R(B/'brief.json');ledger=R(B/'references.json');check_brief(brief,{'asset_id':aid},set(s['id']for s in ledger['sources']),STATIC_PROFILE)
 clean=dict(brief);clean.pop('packaging_adapter');deliverables=clean.pop('required_deliverables');assert clean==orig
 for f in deliverables:assert H(S/f['path'])==f['sha256']
 dependencies=R(B/'build-dependencies.json');assert all(H(S/p)==h for p,h in dependencies['inputs'].items());assert H(S/'package-lock.json')==dependencies['node_lockfile_sha256'];assert all(s['rights_note']and not s['incorporated']for s in ledger['sources'])
 refs=[]
 for ref in ledger['sources']:
  for f in ref['consult_only_files']:
   path=pathlib.Path(f['path']);refs.append({'path':str(path),'sha256':H(path),'pass':H(path)==f['sha256']and path.stat().st_size==f['bytes']});assert refs[-1]['pass']
 audit=audit_glb(B/'model.glb',14000,6,30);(D/'independent-project-audit.json').write_text(json.dumps(audit,indent=2)+'\n');assert not audit['errors']
 # All actual imports are explicit standard/Blender built-ins plus two pinned repository helpers.
 imports=[]
 for f in [B/'generator.py',S/'scripts/asset_common.py',S/'scripts/qa_glb.py']:
  tree=ast.parse(f.read_text());imports.append({'path':str(f),'sha256':H(f),'imports':sorted({n.module if isinstance(n,ast.ImportFrom)else a.name for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom)) for a in (n.names if isinstance(n,ast.Import)else [None])})})
 life=[json.loads(x)for x in (B/'lifecycle.jsonl').read_text().splitlines()];render=next(x for x in life if x['stage']=='proof-final');assert binding['checked_at']<=render['started_at'];assert render['exit_code']==0;assert H(pathlib.Path(render['log']))==render['log_sha256'];log=pathlib.Path(render['log']).read_text();manifest=R(B/'proof-final/render-manifest.json');subject={'glb_sha256':H(B/'model.glb'),'brief_sha256':H(B/'candidate-brief.json'),'references_sha256':H(B/'references.json')};assert all(binding[k]==v and manifest['subject'][k]==v for k,v in subject.items());assert H(B/'proof-final/render-config.json')==manifest['config_sha256'];frames=[];sheet=Image.open(B/'contact-sheet.png').convert('RGBA');assert sheet.size==(2048,1080)
 for i,f in enumerate(manifest['frames']):
  p=B/'proof-final'/f['path'];img=Image.open(p).convert('RGBA');crop=sheet.crop(((i%4)*512,(i//4)*540+28,(i%4+1)*512,(i//4)*540+540));lossless=crop.tobytes()==img.tobytes();assert img.size==(512,512)and H(p)==f['sha256']and lossless;assert 'Saved: ' in log and f['path']in log;frames.append({'view':f['view'],'sha256':H(p),'size':list(img.size),'lossless_sheet_tile':lossless})
 runs=[]
 for i in [1,2]:
  E=P/'rebuild-evidence'/aid/a['revision']/('semantic-rebuild-'+str(i));identity=R(E/'byte-identity.json');raw=pathlib.Path(identity['original_run_dir']);req=R(E/'request.json');res=R(E/'result.json');exc=R(E/'execution.json');assert res['returncode']==0 and res['status']=='succeeded';fp=hashlib.sha256(json.dumps(req['identity'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest();assert req['fingerprint']==res['fingerprint']==fp
  copied=[]
  for n,h in identity['files'].items():
   source=raw/('outputs/'+n if n=='execution.json'else n);assert H(E/n)==h==H(source);copied.append(n)
  inputs=[]
  for label,f in req['identity']['inputs'].items():
   p=pathlib.Path(f['path']);assert H(p)==f['sha256']and p.stat().st_size==f['bytes'];inputs.append({'label':label,**f})
  outputs=[]
  for n,f in res['outputs'].items():
   p=raw/'outputs'/n;assert H(p)==f['sha256']and p.stat().st_size==f['bytes'];outputs.append({'name':n,**f})
  assert H(raw/'outputs/model.glb')==H(B/'model.glb');rebuilt=audit_glb(raw/'outputs/model.glb',14000,6,30);assert rebuilt['semantic_sha256']==audit['semantic_sha256'];assert req['created_at']<=res['started_at']<=exc['started_at']<=exc['finished_at']<=res['finished_at'];assert '/tmp/lowpoly-production-blender.lock'in req['argv']and '--threads'in req['argv'];assert exc['generator_sha256']==H(B/'generator.py')and exc['config_sha256']==H(B/'build-config.json');assert '--output'in exc['argv']and exc['argv'][-1]==str(raw/'outputs');assert not (raw/'outputs/model.glb').samefile(B/'model.glb')
  runs.append({'job':i,'raw_run_directory':str(raw),'fingerprint':fp,'request_sha256':H(E/'request.json'),'result_sha256':H(E/'result.json'),'blender_pid':exc['pid'],'started_at':exc['started_at'],'finished_at':exc['finished_at'],'inputs':inputs,'outputs':outputs,'copied_evidence_verified':copied,'semantic_sha256':rebuilt['semantic_sha256'],'byte_identical':True,'run_stdout_bytes':(raw/'stdout.log').stat().st_size})
 assert runs[0]['blender_pid']!=runs[1]['blender_pid'];assert runs[0]['finished_at']<=runs[1]['started_at']
 rec={'asset':aid,'revision':a['revision'],'subject':subject,'original_frozen_design_unmodified_in_derived_brief':True,'dependency_closure':dependencies,'imports':imports,'source_consult_files':refs,'binding_checked_at':binding['checked_at'],'render_started_at':render['started_at'],'render_finished_at':render['ended_at'],'render_log_sha256':render['log_sha256'],'frames':frames,'rebuilds':runs,'all_checks_pass':True};records.append(rec);print(aid,'provenance pass',flush=True)
(O/'independent-provenance.json').write_text(json.dumps({'host_observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assets':records,'limit':'Queue evidence is internally consistent original execution records plus independently rehashed full closure and decoded GLBs, not retrospective cryptographic proof of process execution.'},indent=2)+'\n')
