#!/usr/bin/env python3
"""Read-only evidence closure. Writes compact independent receipts only to this directory."""
import json, hashlib, subprocess, datetime, re, struct, sys
from pathlib import Path
from collections import Counter
R=Path('/workspace/shared/lowpoly-batch93-20261020')
P=R/'production/small-life-batch93'
E=Path('/workspace/shared/lowpoly-batch93-evidence')
C=Path('/workspace/shared/lowpoly-round39-coordination')
O=Path(__file__).parent
H='2cbc3cbb206d81c2383eada3a3f142c2b2c5cd82'
EXPECTED_HANDOFF='18858bee5ef966f0cdaafa741177c6a05cfc1502f0df79058759dde522e1e7bb'
EXPECTED_RECEIPT='209e146e9dee7f7a1fce73e8245b5cf32d324b43402fae9462d50908a5aa8cf5'
checks=[]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def date(s): return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
def check(name,value,detail=None):
    checks.append({'check':name,'pass':bool(value),**({'detail':detail} if detail is not None else {})})
    return bool(value)
def path(p): return Path(p) if Path(p).is_absolute() else R/p
def record(p):
    p=Path(p); return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
def pin(p,h,size=None,label='hash'):
    p=path(p); ok=p.is_file() and sha(p)==h and (size is None or p.stat().st_size==size)
    check(label,ok,{'path':str(p),'expected_sha256':h} if not ok else None); return ok
def refs(obj,prefix):
    if isinstance(obj,dict):
        if isinstance(obj.get('path'),str) and isinstance(obj.get('sha256'),str):pin(obj['path'],obj['sha256'],label=prefix+'.pin')
        for k,v in obj.items():refs(v,prefix+'.'+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj): refs(v,prefix+'.'+str(i))
def git(*a): return subprocess.check_output(['git','-C',str(R),*a])
def job(raw, tag, current_inputs=True):
    raw=Path(raw); q=load(raw/'request.json'); z=load(raw/'result.json'); i=q['identity']; spec=i['job']; outs=z['outputs']
    check(tag+'.fingerprint',digest(json.dumps(i,sort_keys=True,separators=(',',':'),allow_nan=False).encode())==q['fingerprint']==z['fingerprint']==raw.parent.name)
    check(tag+'.success',z['status']=='succeeded' and z['returncode']==0 and z['error'] is None)
    check(tag+'.identity',all(spec[k]==z[k] for k in ['asset_id','revision','job_id']))
    check(tag+'.times',date(q['created_at'])<=date(z['started_at'])<date(z['finished_at']))
    check(tag+'.flock_threads',q['argv'][:3]==['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender'] and q['argv'][q['argv'].index('--threads')+1]=='2' and i['threads']==2)
    pin(R/'scripts/run_asset_queue.py',i['runner_sha256'],label=tag+'.runner')
    pin(i['executable']['path'],i['executable']['sha256'],i['executable']['bytes'],label=tag+'.executable')
    if current_inputs:
        for key,v in i['inputs'].items():pin(v['path'],v['sha256'],v['bytes'],label=tag+'.input.'+key)
    check(tag+'.declared_outputs',set(spec['outputs']).issubset(outs))
    extra=set(outs)-set(spec['outputs'])
    check(tag+'.extra_outputs_bounded',not extra or (spec['job_id']=='final-eight-views' and extra=={'turntable.json'} and load(raw/'outputs/turntable.json')['frame_count']==0))
    for name,v in outs.items():pin(raw/'outputs'/name,v['sha256'],v['bytes'],label=tag+'.output.'+name)
    for f in ['request.json','result.json','stdout.log','stderr.log']:
        check(tag+'.raw_manifest.'+f,str((raw/f).relative_to(E)) in raw_manifest['files'])
    return q,z,{'request':record(raw/'request.json'),'result':record(raw/'result.json'),'started_at':z['started_at'],'finished_at':z['finished_at'],'wrapper_pid':z['pid'],'output_count':len(outs),'fingerprint':q['fingerprint']}

started=datetime.datetime.now(datetime.timezone.utc).isoformat()
head=git('rev-parse','HEAD').decode().strip(); status=git('status','--porcelain').decode()
check('fixed_head',head==H);check('clean_worktree',not status)
added=git('diff-tree','--no-commit-id','--name-status','-r',H).decode().splitlines()
check('added_only_232',len(added)==232 and all(x.startswith('A\t') for x in added))
blobs=[]
for entry in added:
    _,p=entry.split('\t',1); b=git('show',H+':'+p); f=R/p
    check('committed_blob.'+p,f.is_file() and f.read_bytes()==b)
    blobs.append({'path':p,'sha256':digest(b),'bytes':len(b),'git_blob':git('rev-parse',H+':'+p).decode().strip()})
check('tracked_payload_bytes',sum(x['bytes'] for x in blobs)==23970850)
pin(P/'maker-handoff.json',EXPECTED_HANDOFF,label='fixed_handoff');pin(E/'local-commit-receipt.json',EXPECTED_RECEIPT,label='fixed_local_commit_receipt')
handoff=load(P/'maker-handoff.json');receipt=load(E/'local-commit-receipt.json')
refs(handoff,'handoff')
check('receipt_commit',receipt['commit']==H and receipt['parent']==git('rev-parse',H+'^').decode().strip())
coord=[]
for n in ['batch-93-claim.json','batch-93-selected-inventory.json','batch-93-concept-plan-requirements.json']:
    check('coordination_unchanged.'+n,(P/n).read_bytes()==(C/n).read_bytes());coord.append(record(C/n))
for n in ['PRODUCTION-ADDENDUM.md','DIAGNOSTIC-EFFICIENCY-v001.md']:coord.append(record(Path('/workspace/shared/lowpoly-round36-coordination')/n))
inventory=load(P/'batch-93-selected-inventory.json')
inventory_bytes=git('show',inventory['source_inventory_commit']+':'+inventory['source_inventory_path'])
check('source_inventory_committed_hash',digest(inventory_bytes)==inventory['source_inventory_sha256'])
inventory_original=load(P/'batch-93-selected-inventory.json')
source_inventory=json.loads(inventory_bytes)
source_asset_index={x['id']:x for x in source_inventory['assets']}
check('selected_inventory_original_assets_unchanged',all(source_asset_index[x['id']]==x for x in inventory['assets']))
freeze=load(P/'original-freeze-manifest.json')
for p,h in freeze['files'].items():pin(p,h,label='original_freeze.'+p)
raw_manifest=load(E/'raw-evidence-manifest.json'); raw_bad=[]
for p,v in raw_manifest['files'].items():
    f=E/p
    if not f.is_file() or sha(f)!=v['sha256'] or f.stat().st_size!=v['bytes']:raw_bad.append(p)
check('raw_snapshot_all_but_append_only_progress_match',raw_bad==['recovery-progress.json'])
progress=load(E/'recovery-progress.json'); prefix_matches=[]
for n in range(len(progress['entries'])+1):
    b=(json.dumps({**progress,'entries':progress['entries'][:n]},indent=2)+'\n').encode()
    if digest(b)==raw_manifest['files']['recovery-progress.json']['sha256'] and len(b)==raw_manifest['files']['recovery-progress.json']['bytes']:prefix_matches.append(n)
check('raw_snapshot_progress_exact_prefix_recovered',prefix_matches==[4])
retention=load(E/'lean-retention-receipt.json'); retained_count=0
for d in retention['moved']:
    for p,h in d['files'].items():pin(Path(d['retained'])/p,h,label='retained_prior_evidence');retained_count+=1

# Original-source and concept binding, not a new historical claim of personal inspection.
concepts=[]; chronology=[]
source_ledger=load(P/'source-inspection-v001.json')
sys.path.insert(0,str(R/'scripts'))
from qa_glb import read_glb, semantic_digest
for a in ['omphalophloios','chaloneria','nathorstiana','diplopora']:
    original=load(P/a/'r001/original-brief.json'); c=load(P/'concepts'/f'{a}-receipt.json')
    end=c.get('observed_return_utc',c.get('returned_at')); start=c.get('observed_call_start_utc',c.get('started_at'))
    orig=c.get('original_pixel_path')
    if orig is None:orig=re.search(r'as (/[^\s]+\.png) by default',c.get('output_hint','')).group(1)
    cp=P/'concepts'/f'{a}-concept.png';check(a+'.concept_original_retained',Path(orig).is_file() and sha(orig)==sha(cp))
    check(a+'.concept_return_before_freeze',date(start)<date(end)<date(freeze['freeze_observed_at']))
    check(a+'.original_brief_freeze_time',original['frozen_at']==freeze['freeze_observed_at'])
    check(a+'.concept_pin',sha(cp)==original['concept_inspection']['sha256'])
    original_requests=[f for f in (E/'build-queue').rglob('request.json') if load(f)['identity']['job']['asset_id']==a]
    check(a+'.one_initial_queue',len(original_requests)==1)
    first=load(original_requests[0]); initial_raw=original_requests[0].parent
    check(a+'.first_geometry_after_freeze',date(first['created_at'])>date(freeze['freeze_observed_at']))
    check(a+'.first_queue_original_config',first['identity']['inputs']['config']['sha256']==sha(P/a/'r001/config.json'))
    check(a+'.first_generator_pin',first['identity']['inputs']['generator']['sha256']==sha(P/'tools/generate.py'))
    job(initial_raw,a+'.initial-geometry')
    src=load(P/a/'r001/references.json'); check(a+'.rights_notes',all(x.get('rights_note') for x in src['sources'])); refs(src,a+'.original_reference')
    for source in src['sources']:
        end_source=source['observed_inspection_window_utc'].split('to')[-1].strip()
        check(a+'.source_inspection_before_concept.'+source['id'],date(end_source)<date(start))
        check(a+'.source_ledger_consistent.'+source['id'],source_ledger['sources'][source['id']]['window']==source['observed_inspection_window_utc'])
    concepts.append({'asset_id':a,'concept':record(cp),'original_pixel_path':orig,'original_pixels_byte_identical':True,'receipt':record(P/'concepts'/f'{a}-receipt.json'),'prompt':record(P/'concepts'/f'{a}-prompt.txt'),'observed_call_start':start,'observed_return':end,'provider_id_time':'unknown, preserved as unknown'})
    chronology.append({'asset_id':a,'freeze_recorded':freeze['freeze_observed_at'],'initial_request':record(original_requests[0]),'first_queued_geometry_created_at':first['created_at'],'initial_result':record(initial_raw/'result.json'),'generator_authorship_time':'not independently timestamped; manifest assertion only'})

all_requests=[]
for f in E.rglob('request.json'):
    d=load(f); spec=d.get('identity',{}).get('job',{})
    if spec.get('job_id')=='final-eight-views':all_requests.append((f,d))
world=load(P/'final-world-measurements.json')
assets=[]; all_pids=[]; all_raw_rebuilds=[]
for item in handoff['items']:
    a=item['asset_id'];v=item['revision']; d=P/a/v; tag=a+'.'+v
    original=load(P/a/'r001/original-brief.json');brief=load(d/'delivery-brief.json'); subject=load(d/'subject.json');deps=load(path(item['artifacts']['dependencies']['path']))
    refs(brief,tag+'.delivery');refs(deps,tag+'.dependencies')
    check(tag+'.original_alias',sha(d/'original-brief.json')==sha(P/a/'r001/original-brief.json'))
    check(tag+'.scope_preserved',all(original[k]==brief[k] for k in ['criteria','scale','axes','origin','identifying_features','factual_scope','intended_use','geometry_policy','texture_policy']))
    expected={'revision':v,**{k+'_sha256':item['artifacts'][k]['sha256'] for k in ['glb','brief','references']}}
    check(tag+'.subject_hashes',all(subject[k]==val for k,val in expected.items()))
    check(tag+'.delivery_before_subject',date(brief['delivery_bound_at'])<=date(subject['bound_at']))
    prov=load(d/'qa/execution-provenance.json');refs(prov,tag+'.execution')
    rebuilds=[]
    for build in prov['two_distinct_real_rebuilds']:
        label=build['label'];raw=Path(build['raw_directory']);q,z,j=job(raw,tag+'.rebuild-'+label)
        for filename,cp in [('request.json',build['request']['path']),('result.json',build['result']['path']),('outputs/execution.json',build['execution']['path'])]:check(tag+'.raw_copy.'+label+'.'+filename,sha(raw/filename)==sha(path(cp)))
        ex=load(path(build['execution']['path'])); rp=load(d/'qa'/f'reproducibility-{label}.report.json')
        check(tag+'.rebuild_time.'+label,date(q['created_at'])<=date(z['started_at'])<date(ex['started_at'])<date(ex['finished_at'])<=date(z['finished_at']))
        check(tag+'.rebuild_parent_pid.'+label,ex['parent_pid']==z['pid'] and ex['pid']!=z['pid'])
        check(tag+'.rebuild_execution_pins.'+label,ex['generator_sha256']==item['artifacts']['generator']['sha256'] and ex['config_sha256']==item['artifacts']['config']['sha256'])
        check(tag+'.rebuild_config_generator_inputs.'+label,q['identity']['inputs']['generator']['sha256']==item['artifacts']['generator']['sha256'] and q['identity']['inputs']['config']['sha256']==item['artifacts']['config']['sha256'])
        glb=raw/'outputs'/a/f'{a}.glb'
        check(tag+'.rebuild_bytes_identical.'+label,sha(glb)==item['artifacts']['glb']['sha256']==build['rebuilt_glb_sha256'])
        gd,gb,_=read_glb(glb)
        check(tag+'.semantic_digest_recomputed.'+label,semantic_digest(gd,gb)==build['semantic_sha256'])
        check(tag+'.semantic_report.'+label,rp['status']=='pass' and rp['byte_identical'] and rp['semantic_match'] and rp['semantic_sha256']==rp['rebuilt_semantic_sha256']==build['semantic_sha256'])
        j.update({'blender_pid':ex['pid'],'blender_started_at':ex['started_at'],'blender_finished_at':ex['finished_at'],'execution':record(path(build['execution']['path'])),'glb_sha256':sha(glb),'semantic_sha256':build['semantic_sha256'],'output_glb_matches_final_bytes':True})
        rebuilds.append(j);all_pids.append(ex['pid']);all_raw_rebuilds.append(str(raw))
    check(tag+'.two_actual_distinct_rebuilds',len(rebuilds)==2 and rebuilds[0]['blender_pid']!=rebuilds[1]['blender_pid'] and len({b['fingerprint'] for b in rebuilds})==2)
    check(tag+'.handoff_pids',item['actual_rebuild_pids']==prov['actual_rebuild_pids']==[x['blender_pid'] for x in rebuilds])
    source_raw=Path(prov['source_reopen_raw']).parent.parent;sq,sz,sj=job(source_raw,tag+'.source-reopen')
    for name in ['request','result']:check(tag+'.source_copy.'+name,sha(source_raw/(name+'.json'))==sha(d/'qa'/('source-'+name+'.json')))
    for name,val in sz['outputs'].items():check(tag+'.source_measurement_copy.'+name,sha(d/'qa'/name)==val['sha256'])
    source=load(d/'qa/source-export.report.json');counts=load(d/'qa/authored-evaluated-counts.json');features=load(d/'qa/frozen-feature-measurements.json')
    for obj in [source,counts,features]:check(tag+'.source_measurement_hash',obj['source_sha256']==item['artifacts']['source']['sha256'])
    check(tag+'.counts_handoff',counts['totals']==item['metrics']['authored_evaluated'])
    check(tag+'.counts_sum',all(sum(p[k] for p in counts['parts'])==val for k,val in counts['totals'].items()))
    check(tag+'.source_count_consistency',counts['totals']['evaluated_triangles']==source['source_triangles']==source['glb_triangles']==item['metrics']['triangles'])
    check(tag+'.source_bounds_consistency',source['measured_glb_bounds_m']==item['metrics']['bounds_glb_m'] and source['bounds_match'] and source['triangles_match'])
    check(tag+'.feature_component_sums',sum(x['vertices'] for x in features['components'])==counts['totals']['authored_vertices'] and sum(x['polygons'] for x in features['components'])==counts['totals']['authored_polygons'])
    wi=next(x for x in world['items'] if x['asset_id']==a)
    check(tag+'.world_bound_summary',wi['source_measurements_sha256']==sha(d/'qa/frozen-feature-measurements.json') and wi['world_bounds_glb_m']==item['metrics']['bounds_glb_m'] and wi['actual_connected_components']==len(features['components']) and wi['glb_sha256']==item['artifacts']['glb']['sha256'])
    matched=[(f,q) for f,q in all_requests if q['identity']['job']['asset_id']==a and q['identity']['job']['revision']==v]
    check(tag+'.one_final_render_job',len(matched)==1)
    rf,rq=matched[0];q,z,rj=job(rf.parent,tag+'.final-render');manifest=load(d/'views/render-manifest.json')
    check(tag+'.bound_before_final_job',date(subject['bound_at'])<date(q['created_at'])<=date(z['started_at']))
    check(tag+'.exact_render_inputs',all(q['identity']['inputs'][k]['sha256']==item['artifacts'][k]['sha256'] for k in ['glb','brief','references']))
    check(tag+'.render_manifest_subject',manifest['subject']==expected and manifest['source_glb_sha256']==expected['glb_sha256'])
    check(tag+'.render_manifest_time',date(z['started_at'])<date(manifest['created_at'])<date(z['finished_at']))
    for name,info in z['outputs'].items():check(tag+'.render_copy.'+name,sha(d/'views'/name)==info['sha256'])
    check(tag+'.eight_exact_views',len(manifest['frames'])==8 and {x['id'] for x in manifest['frames']}=={'hero','reversehero','front','side','rear','top','clay','silhouette'})
    for frame in manifest['frames']:
        f=d/'views'/frame['path']; b=f.read_bytes();check(tag+'.png_dimensions.'+frame['id'],b[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',b[16:24])==(512,512));pin(f,frame['sha256'],frame['bytes'],label=tag+'.frame_hash')
    check(tag+'.source_reopen_before_final_job',date(sz['finished_at'])<date(q['created_at']))
    stage=item['stage_status'];check(tag+'.seven_stages_distinct',set(stage)==set(['technical','visual','factual','specification','runtime_parse','gpu','scene']) and stage['gpu']=='unknown' and stage['scene']=='unknown')
    rj.update({'bound_at':subject['bound_at'],'delivery_bound_at':brief['delivery_bound_at'],'render_manifest_created_at':manifest['created_at'],'subject':expected,'subject_hashes_bound_before_job':True,'frame_hashes_and_dimensions_verified':8})
    assets.append({'asset_id':a,'revision':v,'subject':expected,'source_reopen':sj,'counts':counts['totals'],'bounds':source['measured_glb_bounds_m'],'source_components':len(features['components']),'rebuilds':rebuilds,'final_render':rj,'stage_status_is_maker_claim':stage,'final_delivery_brief_parameter_changes':{k:{'original':original['parameters'].get(k),'effective':val} for k,val in brief['parameters'].items() if original['parameters'].get(k)!=val}})
check('all_eight_rebuild_processes_distinct',len(all_pids)==8 and len(set(all_pids))==8 and len(set(all_raw_rebuilds))==8)
check('worktree_still_clean',git('status','--porcelain').decode()=='')

warnings=[{'id':'append_only_recovery_progress','severity':'informational','finding':'The historical raw snapshot lists recovery-progress.json at 4,435 bytes. Its current bytes differ after two appended bookkeeping entries. Reconstructing the first four entries in memory reproduces the exact snapshotted SHA-256 and length. All other 616 snapshotted files match current bytes. No raw artifact or execution mismatch was found.','snapshot_expected':raw_manifest['files']['recovery-progress.json'],'current':record(E/'recovery-progress.json'),'exact_historical_prefix_entry_count':prefix_matches,'later_entry_times':[x['observed_at'] for x in progress['entries'][4:]]}]
limitations=[
'Historical execution, inspection and authoring chronology is evidence-record verification, not independent observation at production time. Queue requests/results, generated execution receipts, exact inputs and outputs are preserved and internally consistent, but are not cryptographically signed runtime attestation.',
'Original freeze records 2026-10-20T22:41:47.170277+00:00. All four initial geometry queue requests follow it and pin original configs and the generator. Exact generator-authoring time is not independently timestamped; generator_authored=false in the freeze remains a maker assertion. Filesystem metadata was not used to invent chronology.',
'Concept original pixels, prompt files and available receipts are preserved. Provider request IDs and provider generation times remain unknown. Recorded tool observation windows are not converted into provider timestamps.',
'Primary-source/ref/concept personal-inspection claims are maker assertions, with preserved local source evidence; this provenance audit did not independently watch historic inspection or re-decide scientific adequacy.',
'No Blender was run by this provenance reviewer. Source counts and bounds were cross-checked against bound raw reopened-source records and summaries, not independently remeasured here. The parent review owns actual reopen/reexport, geometry, visual and factual acceptance.',
'The provenance audit does not establish publication, GPU hardware or composed-scene approval. Those stages remain unknown/unrun as recorded.'
]
failed=[x for x in checks if not x['pass']]
report={'schema_version':1,'scope':'Independent read-only provenance closure, batch93; no external action','started_at':started,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':H,'source':str(R),'status':'pass_with_disclosed_snapshot_bookkeeping_note' if not failed else 'fail','checks_total':len(checks),'checks_passed':len(checks)-len(failed),'failures':failed,'commit_evidence':{'added_blobs':len(blobs),'payload_bytes':sum(x['bytes'] for x in blobs),'clean':not status,'handoff':record(P/'maker-handoff.json'),'local_commit_receipt':record(E/'local-commit-receipt.json')},'requirements':coord,'freeze':{'manifest':record(P/'original-freeze-manifest.json'),'files_verified':len(freeze['files']),'chronology':chronology},'concept_receipts':concepts,'raw_evidence':{'manifest':record(E/'raw-evidence-manifest.json'),'snapshotted_files':len(raw_manifest['files']),'current_files_matching':len(raw_manifest['files'])-len(raw_bad),'current_mismatches':raw_bad,'historical_prefix_recovered':prefix_matches==[4],'retained_earlier_files_verified':retained_count},'assets':assets,'warnings':warnings,'limitations':limitations}
(O/'provenance-report.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'verification-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(O/'committed-blob-receipt.json').write_text(json.dumps({'commit':H,'files':blobs},indent=2)+'\n')
print(json.dumps({'status':report['status'],'checks':len(checks),'failures':failed,'all_rebuild_pids':all_pids,'output_report':str(O/'provenance-report.json')},indent=2))
