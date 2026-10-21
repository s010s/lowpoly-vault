from pathlib import Path
import json,hashlib,os,subprocess,sys,datetime,difflib
from PIL import Image,ImageChops
O=Path(__file__).parent;R=Path('/workspace/shared/lowpoly-batch90-rosary-repair-20261020');P=R/'production/batch90-rosary-repair';B=P/'assets/rosary-shaped-chambered-burrow-hormosiroidea-type/r002';OLD=Path('/workspace/shared/lowpoly-batch90-20261020/production/batch90/assets/rosary-shaped-chambered-burrow-hormosiroidea-type/r001');sys.path.insert(0,str(R/'scripts'))
from qa_glb import audit_glb
from check_reproducibility import compare_rebuild
from validate_candidate import validate_candidate,STATIC_PROFILE
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();J=lambda p:json.loads(Path(p).read_text());pins=[]
def pin(p,h,label):
 p=Path(p);got=H(p);pins.append(dict(path=str(p),expected=h,actual=got,label=label));assert h==got,(p,h,got)
def git(*args):
 env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0');return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(R),*args],env=env)
assert git('rev-parse','HEAD').decode().strip()=='afa7e3514b5c346794c1a5e6dae59ebb6645d1a6';assert git('rev-parse','HEAD^').decode().strip()=='ee1eaa334f5e56a2716f30edb125e01cf193da6f';assert git('status','--porcelain')==b''
pin(P/'maker-handoff.json','db3c3cf36140688e4352544ce2070b2e003db04b6f609904091f345d0b4f2d10','parent fixed handoff');pin(P/'payload-manifest.json','db66e97e4c834bf107a5634e33e392030e974115f878aa0874f400ed1fbcfd70','parent fixed manifest')
pin('/workspace/shared/lowpoly-batch90-independent-qa-20261020/independent-review.json','da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd','old failure');pin('/workspace/shared/lowpoly-batch90-independent-qa-20261020/rosary-shaped-chambered-burrow-hormosiroidea-type/chamber-tail-exact-triangle-evidence.json','39bf61422cee95669f0cf0a3f7dbaf599aadf6df52d18c2a34414ed4f924a034','old exact failure')
manifest=J(P/'payload-manifest.json')
for f in manifest['files']:
 pin(R/f['path'],f['sha256'],'payload');assert hashlib.sha256(git('show','HEAD:'+f['path'])).hexdigest()==f['sha256']
for p,f in J(P/'local-evidence-index.json')['files'].items():pin(p,f['sha256'],'original raw evidence')
for p,h in J(P/'implementation-record-v001.json')['original_files'].items():pin(p,h,'preserved original')
freeze=J(P/'original-freeze/modeling-freeze.json')
for name,h in freeze['files'].items():
 pin(P/'original-freeze'/name,h,'freeze');pin(OLD/name,h,'original r001 freeze')
for n in ['brief.json','references.json','concept-original.png','concept-prompt.txt','concept-generation.json','LICENSES.md']:assert H(B/n)==H(OLD/n)
original=J(OLD/'brief.json');derived=J(B/'candidate-brief.json');assert all(derived[k]==v for k,v in original.items());cfg=J(B/'build-config.json');ocfg=J(OLD/'build-config.json');assert all(cfg[k]==v for k,v in ocfg.items() if k not in ['revision','modeling_decisions']);assert cfg['parameters']['chamber_radius_range_m']==[.0027,.0032]
for f in derived['required_deliverables']:pin(R/f['path'],f['sha256'],'delivery closure')
dep=J(B/'build-dependencies.json')
for p,h in dep['inputs'].items():pin(R/p,h,'dependencies')
pin(R/'package-lock.json',dep['node_lockfile_sha256'],'lockfile');mod=Path('/workspace/shared/lowpoly-landair-web-integration/node_modules');assert str(mod.resolve())=='/workspace/scratch/f9208c421601/lowpoly-modal-scrollbar-20261018/node_modules';assert J(mod/'three/package.json')['version']=='0.180.0'
for source in J(B/'references.json')['sources']:
 assert source['rights_note'] and source['incorporated']==False
 for f in source['consult_only_files']:pin(f['path'],f['sha256'],'source references')
rec=J(B/'concept-generation.json');assert rec['tool']=='image_gen.imagegen';pin(rec['original_returned_path'],H(B/'concept-original.png'),'genuine concept original');assert rec['observed_returned_at']<freeze['frozen_at'] and rec['actual_pixel_inspection_at']<freeze['frozen_at']
# Exact generator diff kept for review; only constrained support path is changed, all other functions intact.
diff=''.join(difflib.unified_diff((OLD/'generator.py').read_text().splitlines(True),(B/'generator.py').read_text().splitlines(True),fromfile='r001/generator.py',tofile='r002/generator.py'));(O/'generator-difference.patch').write_text(diff)
for function in ['poly_outline','inside','rosary']:
 def fn(text,name):
  a=text.index('def '+name+'(');b=text.find('\ndef ',a+1);return text[a:b] if b>=0 else text[a:]
 a=fn((OLD/'generator.py').read_text(),function);b=fn((B/'generator.py').read_text(),function)
 if function=='rosary':b=b.replace(";semantic['support_repair']={'kind':'constrained inscribed32-gon with neck-only boundary heights','inward_construction_guard_m':2e-8,'support_polygon_sides':32,'not_an_acceptance_tolerance':True}",'')
 assert a==b,function
val=validate_candidate(str(B/'candidate.json'),R,None,STATIC_PROFILE,str(B/'profile-contract.json'));(O/'own-candidate-validation.json').write_text(json.dumps(val,indent=2)+'\n');assert val['valid'] and not val['approved_for_brief'];ga=audit_glb(B/'model.glb',14000,6,30);assert not ga['errors'] and ga['bytes']<=1000000;(O/'own-project-audit.json').write_text(json.dumps(ga,indent=2)+'\n')
life=[json.loads(x) for x in (B/'lifecycle.jsonl').read_text().splitlines()];runs=[]
for run in J(B/'final-rebuild-binding.json')['runs']:
 raw=Path(run['original_run_dir']);q=J(raw/'request.json');res=J(raw/'result.json');ex=J(raw/'outputs/execution.json');i=run['job']
 for n,snapshot in [('request.json',P/f'rebuild-evidence/semantic-rebuild-{i}/request.json'),('result.json',P/f'rebuild-evidence/semantic-rebuild-{i}/result.json'),('outputs/execution.json',P/f'rebuild-evidence/semantic-rebuild-{i}/execution.json'),('stdout.log',P/f'rebuild-evidence/semantic-rebuild-{i}/stdout.log'),('stderr.log',P/f'rebuild-evidence/semantic-rebuild-{i}/stderr.log')]:assert H(raw/n)==H(snapshot)
 assert res['pid']==ex['pid'] and res['returncode']==0 and res['status']=='succeeded';assert q['created_at']<=res['started_at']<=ex['started_at']<=ex['finished_at']<=res['finished_at'];assert q['identity']['threads']==2 and q['argv'][q['argv'].index('-t')+1]=='2';assert q['argv']==ex['argv'];assert Path(q['argv'][q['argv'].index('--output')+1])==raw/'outputs'
 for f in q['identity']['inputs'].values():pin(f['path'],f['sha256'],'rebuild exact input')
 pin(q['identity']['executable']['path'],q['identity']['executable']['sha256'],'actual Blender binary')
 for n,f in res['outputs'].items():pin(raw/'outputs'/n,f['sha256'],'rebuild actual output')
 l=next(x for x in life if x['stage']=='queue-'+str(i) and x['exit_code']==0);assert l['command'][:2]==['flock','/tmp/lowpoly-production-blender.lock'];assert l['started_at_host']<=res['started_at']<res['finished_at']<=l['ended_at_host'];pin(l['log'],l['log_sha256'],'queue lock log')
 rr=compare_rebuild(B/'model.glb',raw/'outputs/model.glb',B/'generator.py',B/'build-config.json',P/f'rebuild-evidence/semantic-rebuild-{i}/request.json',P/f'rebuild-evidence/semantic-rebuild-{i}/result.json','model.glb',root=R);assert rr['semantic_match'] and rr['byte_identical'] and not rr['errors'];(O/f'own-rebuild-{i}-comparison.json').write_text(json.dumps(rr,indent=2)+'\n');runs.append(dict(pid=ex['pid'],started_at=ex['started_at'],finished_at=ex['finished_at'],raw_directory=str(raw),raw_output_glb_sha256=H(raw/'outputs/model.glb'),request_sha256=H(raw/'request.json'),result_sha256=H(raw/'result.json'),execution_sha256=H(raw/'outputs/execution.json'),semantic_match=True,byte_identical=True))
assert [x['pid'] for x in runs]==[46,71]
pre=J(B/'preproof-binding.json');man=J(B/'proof-final/render-manifest.json');render=next(x for x in life if x['stage']=='proof-final');assert pre['checked_at_host']<render['started_at_host']<man['created_at']<=render['ended_at_host'];assert render['exit_code']==0;assert render['command'][:2]==['flock','/tmp/lowpoly-production-blender.lock'];assert render['command'][render['command'].index('--threads')+1]=='2';pin(render['log'],render['log_sha256'],'actual final render log')
for role,name in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json')]:assert pre[role+'_sha256']==man['subject'][role+'_sha256']==H(B/name)
assert man['subject']['revision']=='r002' and man['source_unchanged'];pin(B/'proof-final/render-config.json',man['config_sha256'],'render config');oldconf=J(OLD/'proof-final/render-config.json');newconf=J(B/'proof-final/render-config.json');assert oldconf==newconf
assert H(P/'render-fixed8.py')==H(OLD.parents[2]/'render-fixed8.py')
sheet=Image.open(B/'contact-sheet.png').convert('RGB');assert sheet.size==(2048,1080);frames=[]
for i,f in enumerate(man['frames']):
 p=B/'proof-final'/f['path'];pin(p,f['sha256'],'actual final frame');im=Image.open(p).convert('RGB');assert im.size==(512,512);tile=sheet.crop((i%4*512,i//4*540+28,i%4*512+512,i//4*540+540));assert ImageChops.difference(tile,im).getbbox() is None;assert f['wall_seconds']>0;frames.append(dict(view=f['view'],path=str(p),sha256=H(p),lossless_sheet_tile_equal=True))
assert [x['view'] for x in frames]==['hero','reversehero','front','side','rear','top','clay','silhouette'];assert len({x['sha256'] for x in frames})==8
report=dict(status='pass',checked_at_host=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_commit=git('rev-parse','HEAD').decode().strip(),parent=git('rev-parse','HEAD^').decode().strip(),source_clean=git('status','--porcelain')==b'',committed_payload_files=len(manifest['files']),pin_count=len(pins),all_pins_match=True,original_freeze_preserved=True,original_source_failure_unchanged=True,original_config_parameters_palette_seed_unchanged=True,original_renderer_and_render_config_unchanged=True,derived_brief_original_fields_unchanged=True,original_concept_preserved=True,concept_receipt=rec,closure_dependency_root=str(mod.resolve()),two_executed_rebuilds=runs,preproof_binding=pre,render_started_at=render['started_at_host'],render_finished_at=render['ended_at_host'],final_subject=man['subject'],all_frames_after_final_binding=True,frames=frames,sheet_sha256=H(B/'contact-sheet.png'),limits='Maker execution records were corroborated against raw outputs/logs, not cryptographic history. Provider timestamp/request ID and exact original authoring start unknown; no mtime chronology. Unrelated3batch90 assets not rerun. No publication.')
(O/'own-integrity-provenance.json').write_text(json.dumps(report,indent=2)+'\n');(O/'source-pin-checks.json').write_text(json.dumps(pins,indent=2)+'\n');print('PASS',report['committed_payload_files'],report['pin_count'])
