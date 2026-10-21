import sys,json,pathlib,hashlib,datetime,subprocess,math,struct
from PIL import Image
import numpy as np
R=pathlib.Path('/workspace/shared/lowpoly-batch81-charnia-repair-20261020'); B=R/'production/small-life-batch81'; P=B/'assets/charnia/r006'; O=pathlib.Path(__file__).parent; OLD=pathlib.Path('/workspace/shared/lowpoly-batch81-20261020'); ORIG=OLD/'production/small-life-batch81/assets/charnia'; Q=pathlib.Path('/workspace/shared/lowpoly-batch81-independent-qa-20261020')
sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
from check_reproducibility import compare_rebuild
from qa_glb import audit_glb
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def write(n,v):(O/n).write_text(json.dumps(v,indent=2)+'\n')
def cmd(a,cwd=R):return subprocess.check_output(a,cwd=cwd,text=True).strip()
assert cmd(['git','rev-parse','HEAD'])=='47e3b51172f44176cd0bb2ad52bc01d7de32fddc'
assert cmd(['git','rev-parse','HEAD^'])=='7576247b611e1b357313e5409c18c7912197cf2b'
assert cmd(['git','status','--short'])==''
assert cmd(['git','rev-parse','HEAD'],OLD)=='51368e6e458a531b362babd3f1d8f940faaa05ec'
assert sha(Q/'independent-qa.report.json')=='dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5'
assert sha(B/'charnia-repair-records/handoff.json')=='366829bc478f849d671235c1347bb5e29ff003803254b3124abcc3ba695242d9'
manifests=[]
for n in ['lean-manifest.json','local-raw-evidence-index.json']:
 m=read(B/'charnia-repair-records'/n)
 for e in m['files']:
  f=pathlib.Path(e['local_path']);assert f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],f
 manifests.append({'path':str(B/'charnia-repair-records'/n),'sha256':sha(B/'charnia-repair-records'/n),'files_verified':len(m['files']),'bytes_verified':sum(e['bytes'] for e in m['files'])})
# Verify all changed tracked repair files against the fixed commit, not only manifest claims.
changed=cmd(['git','diff','--name-only','HEAD^','HEAD']).splitlines()
for rel in changed:
 raw=subprocess.check_output(['git','show','HEAD:'+rel],cwd=R);assert (R/rel).read_bytes()==raw,rel
# Scope-constrained original r003 and r001 tracked data remain identical to original commit.
original_files=cmd(['git','ls-files','production/small-life-batch81/assets/charnia/r001','production/small-life-batch81/assets/charnia/r003'],OLD).splitlines()
for rel in original_files:assert (OLD/rel).read_bytes()==subprocess.check_output(['git','show','HEAD:'+rel],cwd=OLD),rel
freeze=read(ORIG/'r001/modeling-freeze.json')
for n,h in freeze['files'].items():assert sha(ORIG/'r001'/n)==h,n
for n in ['brief.json','brief.md','references.json','concept-original.png','concept-prompt.txt','concept-generation.json']:assert sha(P/n)==sha(ORIG/'r001'/n),n
rf=read(P/'repair-freeze.json')
for n,h in rf['frozen_files'].items():assert sha(P/n)==h,n
oldcfg=read(ORIG/'r001/build-config.json');cfg=read(P/'build-config.json')
config_changes=[k for k in set(cfg)|set(oldcfg) if cfg.get(k)!=oldcfg.get(k)];assert set(config_changes)=={'revision','repair_parameters'},config_changes
br=read(P/'brief.json');cb=read(P/'candidate-brief.json');brief_changes=[k for k in set(br)|set(cb) if br.get(k)!=cb.get(k)];assert set(brief_changes)=={'required_deliverables','packaging_adapter'},brief_changes
cand=read(P/'candidate.json')
for role,e in cand['artifacts'].items():assert sha(R/e['path'])==e['sha256'],role
for e in cand['evidence']:assert sha(R/e['path'])==e['sha256']
subject={'revision':'r006','glb_sha256':sha(P/'model.glb'),'brief_sha256':sha(P/'candidate-brief.json'),'references_sha256':sha(P/'references.json')}
pre=read(P/'preproof-binding.json');life=[json.loads(s) for s in (P/'lifecycle.jsonl').read_text().splitlines()];render=next(e for e in life if e['stage']=='proof-final');build=next(e for e in life if e['stage']=='build');assert rf['created_at']<build['started_at'];assert pre['checked_at']<render['started_at']<render['ended_at'];assert all(e['exit_code']==0 for e in life)
frames=[];m=read(P/'proof-final/render-manifest.json');assert m['subject']==subject;assert m['source_glb_sha256']==subject['glb_sha256'];assert sha(P/'proof-final/render-config.json')==m['render_config']['sha256'];assert len(m['frames'])==8
for f in m['frames']:
 p=P/'proof-final'/f['path'];assert sha(p)==f['sha256'];assert Image.open(p).size==(512,512);assert p.stat().st_size==f['bytes'];frames.append({'view':f['view'],'sha256':sha(p),'width':512,'height':512})
rc=read(P/'proof-final/render-config.json');oldrc=read(ORIG/'r003/proof-final/render-config.json')
# Camera numeric differences from measured size have floating-point scale only.
def eql(a,b):
 if isinstance(a,(int,float)) and isinstance(b,(int,float)):return math.isclose(a,b,rel_tol=1e-6,abs_tol=1e-8)
 if isinstance(a,dict) and isinstance(b,dict):return a.keys()==b.keys() and all(eql(a[k],b[k]) for k in a)
 if isinstance(a,list) and isinstance(b,list):return len(a)==len(b) and all(eql(x,y) for x,y in zip(a,b))
 return a==b
render_diff=[k for k in set(rc)|set(oldrc) if not eql(rc.get(k),oldrc.get(k))];assert render_diff==[],render_diff
for sn in ['scripts/asset_common.py','scripts/qa_glb.py']:
 assert sha(R/sn)==sha(OLD/sn),sn
# Fresh independent runtime/static results, exact budget.
a=audit_glb(P/'model.glb',br['geometry_policy']['max_triangles'],br['geometry_policy']['max_materials'],br['geometry_policy']['max_primitives']);assert a['status']=='pass';assert a['bytes']<=br['geometry_policy']['max_glb_bytes'];write('static-fresh.json',a)
for kind,args in [('candidate-profile',['validate_candidate.py',str(P/'candidate.json'),'--root',str(R),'--profile','static-stylized-v1','--profile-contract',str(P/'profile-contract.json'),'--json']),('concept',['validate_concept_evidence.py',str(P/'concept-evidence.json'),'--root',str(P)])]:
 run=subprocess.run([sys.executable,str(R/'scripts'/args[0])]+args[1:],capture_output=True,text=True);(O/(kind+'-fresh.json')).write_text(run.stdout);(O/(kind+'-fresh.stderr.txt')).write_text(run.stderr);assert run.returncode==0,(kind,run.stdout,run.stderr)
runs=[]
for rb in read(P/'final-rebuild-binding.json')['runs']:
 q=pathlib.Path(rb['full_local_run']);req=read(q/'request.json');res=read(q/'result.json')
 assert sha(q/'request.json')==rb['request']['sha256'];assert sha(q/'result.json')==rb['result']['sha256'];assert req['identity']==rb['identity'];assert res['outputs']==rb['outputs'];assert res['pid']==rb['pid'];assert res['returncode']==0 and res['status']=='succeeded';assert res['started_at']<res['finished_at'];assert req['identity']['threads']==2
 for role,fi in req['identity']['inputs'].items():assert sha(pathlib.Path(fi['path']))==fi['sha256'],role
 assert sha(pathlib.Path(req['identity']['executable']['path']))==req['identity']['executable']['sha256'];assert sha(R/'scripts/run_asset_queue.py')==req['identity']['runner_sha256']
 for file,fi in res['outputs'].items():assert sha(q/'outputs'/file)==fi['sha256'];assert (q/'outputs'/file).stat().st_size==fi['bytes']
 log=(q/'stdout.log').read_text();assert 'BUILT charnia '+subject['glb_sha256'] in log and 'Blender quit' in log
 rep=compare_rebuild(P/'model.glb',q/'outputs/model.glb',P/'generator.py',P/'build-config.json',q/'request.json',q/'result.json','model.glb',R);assert rep['status']=='pass';write(res['job_id']+'-fresh-comparison.json',rep)
 runs.append({'path':str(q),'pid':res['pid'],'job_id':res['job_id'],'started_at':res['started_at'],'finished_at':res['finished_at'],'request_sha256':sha(q/'request.json'),'result_sha256':sha(q/'result.json'),'stdout_sha256':sha(q/'stdout.log'),'outputs_verified':res['outputs'],'semantic_sha256':rep['semantic_sha256'],'semantic_match':True,'byte_identical':rep['byte_identical']})
assert len(runs)==2 and len({x['pid'] for x in runs})==2 and len({x['path'] for x in runs})==2
# Full-volume boundary shape comparison is visual evidence, not fossil feature proof.
masks={}
for rev,path in [('r003',ORIG/'r003'),('r005',P.parent/'r005'),('r006',P)]:
 im=np.asarray(Image.open(path/'proof-final/silhouette.png').convert('RGB'));masks[rev]=np.all(im<50,axis=2)
mask_comparisons={}
for rev in ['r005','r006']:
 aa=masks['r003'];bb=masks[rev];mask_comparisons['r003_vs_'+rev]={'iou':float(np.sum(aa&bb)/np.sum(aa|bb)),'different_pixels':int(np.sum(aa!=bb)),'original_foreground_pixels':int(aa.sum()),'revised_foreground_pixels':int(bb.sum())}
reference_files=[]
for e in read(P/'references.json')['sources'][0]['consulted_images']:
 f=pathlib.Path('/workspace/shared/lowpoly-batch81-reference-consult')/e['filename'];assert sha(f)==e['sha256'];reference_files.append({'path':str(f),'sha256':sha(f)})
write('input-provenance-audit.json',{'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'pass','repair_commit':cmd(['git','rev-parse','HEAD']),'repair_parent':cmd(['git','rev-parse','HEAD^']),'clean_worktree':True,'original_qa_sha256':sha(Q/'independent-qa.report.json'),'original_tracked_charnia_files_verified':len(original_files),'repair_changed_tracked_files_verified':len(changed),'manifests':manifests,'original_freeze_sha256':sha(ORIG/'r001/modeling-freeze.json'),'original_freeze_all_hashes_match':True,'reference_files':reference_files,'frozen_scope_references_concept_palette_dimensions_unchanged':True,'config_changes_only':config_changes,'derived_brief_changes_only':brief_changes,'repair_freeze_precedes_build':True,'preproof_binding_precedes_all_final_frames':True,'renderer_config_equal_with_float_tolerance':True,'renderer_sha256':rc['renderer_sha256'],'frames':frames,'triplet':subject,'rebuilds':runs,'silhouette_mask_comparisons':mask_comparisons,'limitations':['Retained PID/job/timestamp/stdout records show separate executions; not independent observation of historical process execution or cryptographic proof.','No filesystem modification-time chronology used.','Original provider internal generation time/request ID and exact generator authoring start remain unknown.','CPU images and Node parse are not GPU or populated-scene tests.']})
print(json.dumps({'status':'pass','manifests':manifests,'config_changes_only':config_changes,'renderer_diff':render_diff,'silhouette_mask_comparisons':mask_comparisons,'rebuild_pids':[x['pid'] for x in runs]},indent=2))
