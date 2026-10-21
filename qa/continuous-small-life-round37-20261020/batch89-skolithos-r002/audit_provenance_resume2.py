import json,hashlib,pathlib,datetime,subprocess
from PIL import Image
S=pathlib.Path('/workspace/shared/lowpoly-batch89-skolithos-repair-20261020'); B=S/'production/small-life-batch89'; R=B/'skolithos-pipe-field/r002'; Q=pathlib.Path('/workspace/shared/lowpoly-skolithos-r002-independent-qa-20261020'); RAW=pathlib.Path('/workspace/shared/lowpoly-batch89-skolithos-repair-raw-20261020')
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def pin(p):p=pathlib.Path(p);return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def read(p):return json.loads(pathlib.Path(p).read_text())
def time(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
checks=[]
def check(name,cond,detail=None):
 checks.append({'check':name,'pass':bool(cond),'detail':detail});assert cond,(name,detail)
def match(p,h):check('sha256 '+str(p),sha(p)==h,{'actual':sha(p),'expected':h})
def save(name,d):
 p=Q/name
 with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')
 return pin(p)
def progress(stage,p):
 f=Q/'recovery-progress.json';d=read(f);d['stages'].append({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':stage,'status':'pass','receipt':p});f.write_text(json.dumps(d,indent=2)+'\n')
# The audit does not rerun prior successful Blender jobs, nor mutate maker source.
readreceipt=read(Q/'recovery-readreceipt-resume2.json')
for p in readreceipt['predecessor_independent_qa_files']:match(p['path'],p['sha256'])
check('source HEAD',subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip()=='4264dbafd0cc3142175c890644f2990dfaa0acf6')
check('source worktree clean',not subprocess.check_output(['git','-C',str(S),'status','--short'],text=True).strip())
handoff=read(R/'maker-handoff.json'); subject=handoff['subject']
for k,v in handoff['artifacts'].items():match(S/v['path'],v['sha256'])
oldmap=read(R/'qa/original-failure-byte-map.json')
for e in oldmap['files']:
 match(e['raw_original_path'],e['sha256']);match(S/e['retained_repository_path'],e['sha256'])
# Original history must also agree with immutable Git parent, rather than maker declarations alone.
for rel in ['production/small-life-batch89/original-freeze-manifest.json',*[e['retained_repository_path'] for e in oldmap['files']]]:
 old=subprocess.check_output(['git','-C',str(S),'show',handoff['base_commit']+':'+rel]);check('Git base unchanged '+rel,hashlib.sha256(old).hexdigest()==sha(S/rel))
a=read(B/'skolithos-pipe-field/r001/original-brief.json'); b=read(R/'delivery-brief.json');differences=[k for k in a if a[k]!=b.get(k)]
check('all original brief fields unchanged except derived brief_version label',differences==['brief_version'],differences)
oldcfg=read(B/'skolithos-pipe-field/r001/config.json'); cfg=read(R/'config.json');check('original hard parameter ranges unchanged',oldcfg['parameters']==cfg['parameters']==b['parameters'])
freeze=read(R/'repair-freeze.json');initial=read(R/'qa/initial-execution.json');initial_request=read(R/'qa/initial-request.json')
check('repair freeze before initial request and actual geometry',time(freeze['frozen_at'])<time(initial_request['created_at'])<time(initial['started_at']))
for e in read(R/'dependencies.json')['files']:match(S/e['path'],e['sha256'])
refs=read(R/'references.json');check('no incorporated third party assets',refs['no_incorporated_third_party_assets'] is True)
for e in refs['sources']:
 check('rights and nonincorporation '+e['id'],bool(e['rights_note']) and e['incorporated'] is False and e['use']=='consulted-only')
 for f in e['consult_only_files']:match(f['path'],f['sha256']);check('consult-only pixels outside source tree',not pathlib.Path(f['path']).is_relative_to(S))
raw=read(R/'qa/local-raw-manifest.json')
for e in raw['files']:match(e['path'],e['sha256']);check('raw bytes '+e['path'],pathlib.Path(e['path']).stat().st_size==e['bytes'])
check('raw manifest byte sum',sum(e['bytes'] for e in raw['files'])==raw['total_bytes'])
rebuild=[]
for label in ['a','b']:
 req=read(R/f'qa/rebuild-{label}-request.json');res=read(R/f'qa/rebuild-{label}-result.json');exe=read(R/f'qa/rebuild-{label}-execution.json'); rep=read(R/f'qa/reproducibility-{label}.report.json')
 out=pathlib.Path(req['argv'][req['argv'].index('--output')+1]);attempt=out.parent
 for own,file in [(R/f'qa/rebuild-{label}-request.json',attempt/'request.json'),(R/f'qa/rebuild-{label}-result.json',attempt/'result.json'),(R/f'qa/rebuild-{label}-execution.json',out/'execution.json')]:check('raw/published queued receipt match '+label+str(file),sha(own)==sha(file))
 check('blocking flock and threads2 '+label,req['argv'][0:3]==['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender'] and req['argv'][req['argv'].index('--threads')+1]=='2')
 check('success and result/execution PID '+label,res['status']=='succeeded' and res['returncode']==0 and res['error'] is None and exe['parent_pid']==res['pid'])
 check('actual queue lifecycle '+label,time(req['created_at'])<=time(res['started_at'])<=time(exe['started_at'])<=time(exe['finished_at'])<=time(res['finished_at']))
 check('input hash bindings '+label,exe['generator_sha256']==handoff['artifacts']['generator']['sha256'] and exe['config_sha256']==handoff['artifacts']['config']['sha256'])
 for key,e in req['identity']['inputs'].items():match(e['path'],e['sha256'])
 for path,e in res['outputs'].items():match(out/path,e['sha256']);check('output bytes '+label+path,(out/path).stat().st_size==e['bytes'])
 check('rebuilt GLB exact candidate bytes '+label,sha(out/'skolithos-pipe-field/skolithos-pipe-field.glb')==subject['glb_sha256'])
 stdout=(attempt/'stdout.log').read_text();check('actual Blender export stdout '+label,'Blender quit' in stdout and 'Finished glTF' in stdout)
 check('repro report semantic and byte match '+label,rep['semantic_match'] and rep['byte_identical'] and rep['semantic_sha256']==rep['rebuilt_semantic_sha256'])
 rebuild.append({'label':label,'request':pin(attempt/'request.json'),'result':pin(attempt/'result.json'),'execution':pin(out/'execution.json'),'stdout':pin(attempt/'stdout.log'),'stderr':pin(attempt/'stderr.log'),'glb':pin(out/'skolithos-pipe-field/skolithos-pipe-field.glb'),'wrapper_pid':res['pid'],'blender_pid':exe['pid'],'created_at':req['created_at'],'started_at':exe['started_at'],'finished_at':exe['finished_at'],'semantic_sha256':rep['semantic_sha256']})
check('distinct actual rebuild Blender PIDs',rebuild[0]['blender_pid']!=rebuild[1]['blender_pid'],[e['blender_pid'] for e in rebuild])
check('distinct queue output paths',rebuild[0]['glb']['path']!=rebuild[1]['glb']['path'])
# Renderer computes full triplet before import and render, rejects nonempty output, then rechecks unchanged inputs.
manifest=read(R/'views/render-manifest.json');gate=read(R/'qa/prefinal-binding-gate.json');prov=read(R/'qa/execution-provenance.json');rc=read(R/'views/render-config.json'); renderer=B/'tools/render.py'; code=renderer.read_text(); log=(RAW/'final-render.log').read_text()
check('exact full final subject binding',manifest['subject']==gate['subject']==subject)
check('triplet fixed before recorded parse and render completion',time(b['delivery_bound_at'])==time(gate['checked_at'])<time(prov['final_render_order']['three_parse_completed_before_render_command_at'])<time(manifest['created_at']))
check('renderer binds before pixels and rechecks afterward',code.index('subject =')<code.index('bpy.ops.import_scene.gltf')<code.index('bpy.ops.render.render')<code.index("if digest(source)!=source_hash") and "if any(output.iterdir())" in code)
match(renderer,rc['renderer_sha256']);match(R/'views/render-config.json',manifest['config_sha256']);match(RAW/'final-render.log',next(e['sha256'] for e in prov['raw_logs'] if e['path'].endswith('final-render.log')))
check('eight final fixed views',len(manifest['frames'])==8 and [e['id'] for e in manifest['frames']]==b['required_views'])
frames=[];sheet=Image.open(R/'views/contact-sheet.png').convert('RGBA')
for i,e in enumerate(manifest['frames']):
 p=R/'views'/e['path'];match(p,e['sha256']);im=Image.open(p).convert('RGBA');check('exact512 '+e['id'],im.size==(512,512));check('saved exact new view log '+e['id'],("Saved: '"+str(p)+"'") in log)
 check('lossless sheet exact original pixel crop '+e['id'],sheet.crop(((i%4)*512,(i//4)*540,(i%4+1)*512,(i//4)*540+512)).tobytes()==im.tobytes())
 frames.append({'view':e['id'],**pin(p),'size':list(im.size),'old_r001_sha256':sha(B/'skolithos-pipe-field/r001/views'/e['path']),'bytes_differ_from_old_view':sha(p)!=sha(B/'skolithos-pipe-field/r001/views'/e['path'])})
 # Views can be equal if unchanged geometry is hidden. Actual new render log, not inequality alone, establishes rendering.
check('CPU is not GPU',rc['engine']=='Cycles CPU' and rc['render_threads']==2 and manifest['runtime_qa']=='not_run')
sheetprov=read(R/'qa/contact-sheet-provenance.json');match(R/'views/contact-sheet.png',sheetprov['sheet_sha256'])
source=read(Q/'own-source-reopen-reexport.json');match(Q/'source-reexport.glb',subject['glb_sha256']);check('predecessor source reexport exact identity',source['glb_sha256']==subject['glb_sha256'] and source['reexport_semantic_match'] and source['reexport_byte_match'] and source['source_unchanged'] and not source['source_saved'])
khr=read(Q/'own-khronos-validation.json');three=read(Q/'own-three-parse.json');cv=read(Q/'own-candidate-validation.json')
check('predecessor official Khronos no issues',khr['glb_sha256']==subject['glb_sha256'] and not any(khr['report']['issues'][k] for k in ['numErrors','numWarnings','numInfos','numHints']))
check('predecessor Three parse exact identity',three['glb_sha256']==subject['glb_sha256'] and three['status']=='pass' and not three['errors'])
check('predecessor candidate profile validity not approval',cv['valid'] and not cv['approved_for_brief'] and cv['validation_profile']=='static-stylized-v1' and cv['subject']==subject)
result={'schema_version':1,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'resume_skolithos_qa_recovery2','status':'pass','checks':checks,'check_count':len(checks),'raw_files_rehashed':len(raw['files']),'raw_bytes_rehashed':raw['total_bytes'],'source_commit':readreceipt['source_commit'],'subject':subject,'rebuilds':rebuild,'frames':frames,'chronology':{'original_freeze_at':a['frozen_at'],'repair_freeze_at':freeze['frozen_at'],'first_request_at':initial_request['created_at'],'first_actual_geometry_started_at':initial['started_at'],'delivery_triplet_bound_at':b['delivery_bound_at'],'renderer_manifest_completed_at':manifest['created_at'],'exact_render_start_time':'unknown, not recorded; not inferred from filesystem times','basis':'Pinned renderer binds GLB/brief/refs before import/render and rechecks unchanged after eight true saved frames; fail-closed sequential maker execution receipt places render after final binding and parse. Local chronology evidence, not cryptographic execution proof.'},'predecessor_execution_attribution':'Prior independent reviewer actually reopened/reexported source and executed Khronos/Three/candidate tests. This continuation rehashed and reconciled successful receipts rather than rerunning Blender.','source_log_note':'The predecessor Blender log reports unavailable optional Draco compression; candidate is deliberately uncompressed and export completed byte-identically. No compression dependency or failed candidate export is implied.'}
p=save('own-provenance-closure-resume2.json',result);progress('verify_raw_rebuilds_freeze_and_final_pixel_closure',p);print(json.dumps({'receipt':p,'checks':len(checks),'raw_count':len(raw['files']),'rebuild_blender_pids':[e['blender_pid'] for e in rebuild]},indent=2))
