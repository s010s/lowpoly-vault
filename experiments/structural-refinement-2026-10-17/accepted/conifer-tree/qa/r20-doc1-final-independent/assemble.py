"""Assemble a new independent review record; never write candidate/old QA files."""
import copy, datetime, hashlib, json, math, shutil, subprocess, sys
from pathlib import Path

Q=Path(__file__).resolve().parent
ROOT=Q.parent.parent
REPO=ROOT.parents[2]
C=ROOT/'candidate-r20-a-normal16-doc1'
RUNTIME=REPO.parent/'asset-refinements/qa/conifer-r20-runtime-20261017'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def copyfile(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    assert H(src)==H(dst)
def pin(p):return {'path':str(p.relative_to(ROOT)),'sha256':H(p)}

record=read(C/'candidate.json')
brief=read(C/'brief.json')
subject={'revision':record['revision'],'glb_sha256':H(C/'conifer-tree.glb'),'brief_sha256':H(C/'brief.json'),'references_sha256':H(C/'references.json')}
assert subject['glb_sha256']=='c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
reviewer={'id':'independent-sol61-conifer-QA','task_id':'conifer-independent-r15-through-doc1-review'}
runtime_copies=[]
for profile in ['metal','swiftshader']:
    p=RUNTIME/'attempt-01'/profile
    for name in ['runtime-report.json','execution.json']:
        copyfile(p/name,Q/'support/runtime'/profile/name)
    for sub in ['scene','diagnostics']:
        for image in sorted((p/sub).glob('*.png')):
            copyfile(image,Q/'support/runtime'/profile/sub/image.name)
    for name in ['report.json']:
        copyfile(p/'diagnostics'/name,Q/'support/runtime'/profile/'diagnostics'/name)
    copyfile(p/'normal16/512-42-r20.png',Q/'support/runtime'/profile/'hero.png')
for name in ['README.md','SHA256SUMS.json']:
    copyfile(RUNTIME/name,Q/'support/runtime'/name)
for src in sorted((RUNTIME/'motion-continuous-01').iterdir()):
    if src.is_file():copyfile(src,Q/'support/motion'/src.name)
sample_indices=[1,30,70,110,150,190,199,200,201,202,203,204,205,230,270,310,350,390,409]
for i in sample_indices:
    src=Path('/tmp/conifer-r20-motion-review')/f'frame-{i:04}.png'
    copyfile(src,Q/'support/decoded-samples'/src.name)
for src in sorted(Path('/tmp/conifer-r20-motion-review').glob('contact-*.jpg')):
    copyfile(src,Q/'support/decoded-contact'/src.name)
copyfile(Path('/tmp/conifer-r20-motion-review/frame-stats.json'),Q/'support/frame-stats.json')

capture=read(Q/'support/motion/capture-report.json');trace=read(Q/'support/motion/frame-trace.json')
assert H(Q/'support/motion/orbit-zoom.webm')==capture['video']['sha256']
assert H(Q/'support/motion/frame-trace.json')==capture['trace']['sha256']
assert len(trace)==821 and all(x['draw_calls']==3 and x['triangles']==19052 for x in trace)
assert all(a['elapsed_ms']<=b['elapsed_ms'] for a,b in zip(trace,trace[1:]))
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(Q/'support/motion/orbit-zoom.webm')],text=True))
pts=[float(x['best_effort_timestamp_time']) for x in probe['frames']]
assert len(pts)==409 and all(a<b for a,b in zip(pts,pts[1:]))
stats=read(Q/'support/frame-stats.json');assert len(stats)==409
motion={'status':'pass_with_disclosed_aliasing','video_sha256':capture['video']['sha256'],'decoded_frames':len(pts),'render_trace_frames':len(trace),'pts_first_s':pts[0],'pts_last_s':pts[-1],'max_encoded_pts_gap_s':max(b-a for a,b in zip(pts,pts[1:])),'capture_wall_ms':capture['elapsed_ms'],'azimuth_range_deg':[min(x['azimuth_deg']for x in trace),max(x['azimuth_deg']for x in trace)],'zoom_scale_range':[min(x['zoom_scale']for x in trace),max(x['zoom_scale']for x in trace)],'foreground_pixel_range':[min(x['nonbackground_pixels']for x in stats),max(x['nonbackground_pixels']for x in stats)],'blank_frames_by_background_check':sum(x['nonbackground_pixels']==0 for x in stats),'full_resolution_frames_opened':sample_indices,'all_decoded_frames_viewed_in_ordered_contact_sheets':True,'method':'Independent ffmpeg decode, ffprobe PTS/trace/hash checks, all 409-frame ordered contact sequence and 19 full-resolution samples including six successive near frames. Not a claim of watching real-time playback or pixel-identical frames.','observed':'No empty frame, whole-spray popping, normal inversion or broad flashing patches. Thin opaque needles have visible subpixel edge shimmer/aliasing and VP9 sampling softness. These do not erase the selected A hierarchy in the examined motion.','limits':'Fixed elevation23.3, one 360-degree orbit and zoom0.45..1.1 on M5 Pro/Metal at768px; earlier128/512 small-angle evidence remains complementary. Encoded frames409 are not821 captured frames or a benchmark; video capture has a195ms initial PTS gap. No universal no-alias claim.'}
write(Q/'motion-review.json',motion)

# Use only existing same-byte visual evidence; the separate doc1 review established documentary mapping.
visual_images=[copy.deepcopy(e) for e in record['evidence'] if e['stage']=='visual' and e['kind'] in ['render_manifest','rendered_image']]
record['evidence']=visual_images
stage_images={s:[] for s in record['stages']}
stage_images['visual']=[x['id'] for x in visual_images]
for stage,sub in [('gpu','diagnostics'),('scene','scene')]:
    for profile in ['metal','swiftshader']:
        paths=sorted((Q/'support/runtime'/profile/sub).glob('*.png'))
        if stage=='gpu':paths.append(Q/'support/runtime'/profile/'hero.png')
        for path in paths:
            eid=stage+'-'+profile+'-'+path.stem
            record['evidence'].append({'id':eid,'kind':'rendered_image','stage':stage,**pin(path),'subject':subject})
            stage_images[stage].append(eid)

warning_alias='Thin separated needles show ordinary subpixel edge aliasing during motion; no zero-shimmer promise.'
warning_swift='SwiftShader exceeds16.7ms rAF p95 for all1/16/32 cases; software performance is not accepted.'
limitations=[warning_alias,warning_swift,'Only measured M5 Pro/ANGLE Metal, Chromium141 WebGL2, Three.js0.180.0, DPR1, no shadows, declared authored-meter sparse-grove camera fits. No all-device, dense-forest, near32-copy or long-duration thermal guarantee.','Actual source/build executions were performed by the recorded producer; independent reviewer checked raw reports, hashes and rebuilt outputs without rerunning Blender.','Publication authorization, complete renderer-specific24alpha release preview approval and website integration remain separate.']
refs=['PRI-branching','HK-branchlets','repository-triage','NHM-context','NCSU-flat-needles','Earle-flat-needles']
report_kinds={'technical':'technical_report','visual':'visual_report','factual':'reference_comparison','specification':'spec_report','runtime_parse':'runtime_parse_report','gpu':'gpu_report','scene':'scene_report'}
metal=read(Q/'support/runtime/metal/runtime-report.json')
swift=read(Q/'support/runtime/swiftshader/runtime-report.json')
runtime={'engine':'Three.js','version':'0.180.0','renderer':'WebGLRenderer','device':capture['device'],'browser':'Chromium141.0.7390.37 isolated headless producer evidence; reviewer did not launch browser','context':'WebGL2RenderingContext','context_created':True,'rendered':True,'rendered_frames':409,'draw_calls':3,'triangles':19052,'output_color_space':'srgb','tone_mapping':'ACESFilmic','exposure':1.2}
def sample_summary(d):
    return [{**{k:x[k]for k in ['copies','mode','visible_copies','draw_calls','triangles','gpu_timer_disjoint']},'gpu_valid_samples':len(x['gpu_timer_ms']),'raf_samples':len(x['raf_intervals_ms']),'raf_p95_ms':sorted(x['raf_intervals_ms'])[math.ceil(.95*len(x['raf_intervals_ms']))-1]} for x in d['populations']]
assert all(x['raf_p95_ms']<=16.7 for x in sample_summary(metal))
assert all(x['raf_p95_ms']>16.7 for x in sample_summary(swift))
methods={
'technical':'Independent exact GLB/accessor/normal/pixel audit, Khronos validator rerun and actual Three.js parser; reviewed original frozen static/source-export and hash-bound rebuild reports and outputs. Doc1 same-binary reuse independently checked; no new Blender execution claimed.',
'visual':'Independently opened all53 exact raw diagnostic PNGs and three comparisons in original r20, checked every new-doc1 image byte unchanged, applied user-selected airy A criteria; additionally inspected actual GPU diagnostics and decoded continuous orbit/zoom frames.',
'factual':'Read public feature-specific PRI branching, HK2018 p17, NCSU Leaves, Earle Description, NHM context plus repository triage; compared actual frozen pixels and honest labels; independently checked doc1 corrections only clarify current A versus historical B.',
'specification':'Independent S1-S4 document and lowercase identity review, six deliverable hashes, original118/new138 freeze checks, same model/inputs/images and current subject mapping, measured dimensions/storage/budgets and all planned image coverage; actual GPU/scene evidence now reviewed in its explicit M5 scope.',
'runtime_parse':'Independent execution of pinned Three.js0.180.0 GLTFLoader on same GLB; observed normalized Int16Array streams and exact bounds/counts, without external decoder. Doc1 metadata does not change runtime input.',
'gpu':'Independent review of actual browser-consumed hashes, raw Metal/software reports, under/high and branch screenshots, normal precision pairs, shader/console logs; independently decoded409-frame real orbit/zoom recording, PTS/821-frame trace and sampled actual pixels. No new GPU run by reviewer.',
'scene':'Independent actual1/16/32 clone and instanced screenshot inspection, recomputed raw sampling p95/counts/disjoint flags and exact candidate identity; accepted only frozen16.7ms target on reported M5 Pro/Metal under recorded no-shadow/DPR1/camera conditions. SwiftShader failures explicitly retained.'}
observations={
'technical':['19052 triangles,29882 POSITION vertices,715500 bytes,3 materials/primitives,0 textures; normal max angle0.001443162deg within0.001444deg.','POSITION/index order/materials/transforms exact to r19; only SHORT normalized NORMAL storage changed.','Independent validator0errors/0warnings; existing canonical/rebuilt output bytes match r19/r20 respectively; raw execution records preserve original identity.'],
'visual':['All24 azimuths plus canonical directions, clay/alternate key/wire/detail and native128 retain selected A silhouette and primary/secondary hierarchy.','No coarse green cylinders, broad hard blade groups, obvious floating components or new large normal seams.','Natural sky windows and fine needle diminution at128 are permitted by explicit A choice. Current motion preserves structure with disclosed edge aliasing.'],
'factual':['Pass only evidence-informed generic stylized conifer architecture; modern branching and narrow feather-needle analogues support broad features.','7m scale,26 boughs,149 sprays,12 pairs,spacing,palette and gaps are artistic abstractions, not measured fossil anatomy.','No named extinct/current species, exact geological age/locality or scientifically exact reconstruction accepted. PRI fossil example is Eocene, not Mesozoic proof.'],
'specification':['All six required deliverables hash-match; dimensions4.661952x7.042110x5.167211m and origin minY0.','S1 existing diagnostic preview,S2 equivalence path,S3 actual versus ceiling arithmetic,S4 historical B scope corrected; lowercase new identity has explicit old/new evidence lineage.','Numerical caps19500tri/3materials/3primitives/1000000B and zero textures remain unchanged; normal delivery profile and mandatory views satisfied.','Exact rendering/scene evidence is accepted at recorded M5 device scope;16.7ms unchanged. Publishing/preview integration is separate.'],
'runtime_parse':['Pinned loader parsed3 meshes/3 primitives with normalized interleaved Int16Array NORMAL and finite decoded values.','No external decoder, bounds and counts match source; runtime render separately checked.'],
'gpu':['Metal hardware-reported actual WebGL2 output and software output preserve current A form with no logged shader/page errors.','Continuous recording decoded409 actual VP9 frames; all821 draw-trace submissions3calls/19052tri; no empty decoded image or large visible normal/backface pop.','Video encoding/PTS variability is not a frame-time benchmark; original GPU/scene arrays remain authoritative.'],
'scene':['1/16/32 clones physically grounded at authored-meter scale; visible counts match; clone calls5/50/98 include floor/grid, triangles19054/304834/609666.','All six Metal rAF p95 values8.9..9.7ms meet frozen16.7ms; query60valid percase, no disjoint.','SwiftShader all cases fail strict rAF target;16/32 query arrays have10 completed samples, not60. Instancing5calls is supplementary, not substitute for clone baseline.']}
for stage in record['stages']:
    eid='independent-'+stage
    report={'schema_version':1,'kind':report_kinds[stage],'stage':stage,'subject':subject,'status':'pass','reviewer':reviewer,'reviewed_at':now,'method':methods[stage],'observations':observations[stage],'errors':[],'warnings':[],'warning_review':[],'reviewed_evidence':sorted([{'id':x['id'],'sha256':x['sha256']}for x in record['evidence']if x['id']in stage_images[stage]],key=lambda x:x['id']),'limits':limitations,'documentary_reuse':pin(C/'evidence-reuse.json')}
    if stage=='technical':
        source=read(C/'technical.report.json');report['measurements']=source['measurements'];report['checks']=source['checks'];report['warnings']=source['warnings'];report['warning_review']=source['warning_review']
        report['independent_extra_audits']=[pin(ROOT/'qa/r20-independent-sol61'/x)for x in ['audit-results.json','validator-independent.json','parse-independent.json','cost-independent.json']]
    if stage=='runtime_parse':report['runtime']={'engine':'Three.js','version':'0.180.0','loader':'GLTFLoader','parsed':True}
    if stage in ['gpu','scene']:
        report.update(runtime=copy.deepcopy(runtime),screenshots=stage_images[stage],warnings=[warning_alias,warning_swift],warning_review=[{'warning':warning_alias,'rationale':'Observed edge/subpixel variation is bounded to fine needle outlines; no sampled structural dropout or broad flashing; user explicitly selected separated airy A, not a zero-alias guarantee.'},{'warning':warning_swift,'rationale':'Failure remains recorded as a nonaccepted software profile. Pass applies only to measured M5 Pro/Metal scenes against unchanged16.7ms target.'}],accepted_profile={'device':capture['device'],'scene_config':metal['scene_config'],'samples':sample_summary(metal)},nonaccepted_software_profile={'device':swift['device']['device'],'samples':sample_summary(swift)},motion_review=pin(Q/'motion-review.json'),source_runtime_reports=[pin(Q/'support/runtime'/p/'runtime-report.json')for p in ['metal','swiftshader']],source_motion_records=[pin(Q/'support/motion'/x)for x in ['orbit-zoom.webm','capture-report.json','frame-trace.json','supplement-report.json']])
        if stage=='scene':
            report['runtime'].update(rendered_frames=6,draw_calls=98,triangles=609666)
            report['scene_description']='Authored-meter sparse grove on common floor/grid; tested1/16/32 independent clones, same-geometry instanced comparison, fixed light preset,no shadows,DPR1,1200x900,fit each whole grove; scope excludes dense mixed biome/near32 trees.'
            report['scene_assets']=[{'asset_id':'conifer-tree','glb_sha256':subject['glb_sha256'],'instances':32,'population_cases':[1,16,32],'mode':'independent clones; instanced results supplemental'}]
    path=Q/(stage+'.report.json');write(path,report)
    record['evidence'].append({'id':eid,'kind':report_kinds[stage],'stage':stage,**pin(path),'subject':subject})
    stage_entry=record['stages'][stage]
    stage_entry.update(status='pass',reviewer=reviewer,reviewed_at=now,subject=subject,evidence=stage_images[stage]+[eid],inspected_references=refs if stage in ['visual','factual']else [],note=methods[stage]+' Scope/limits retained in structured report.')
    for criterion in stage_entry['criteria']:
        criterion.update(status='pass',evidence=[eid],note='Independently reviewed for exact doc1 subject; see report feature-level observations and explicit scope, not maker self-approval.')
    if stage=='visual':stage_entry['inspected_frames']=[x['id']for x in read(C/'evidence/full-angle256/render-manifest.json')['frames']]
record['supersedes']={**pin(ROOT/'candidate-r20/candidate.json'),'revision':'structure-r20-A-normal16'}
record['blockers']=[{'id':'documentary-identity-recheck-pending','status':'resolved','description':'S1-S4/lowercase identity and exact old/new mapping required.','resolution':'Independent062be906 doc1 review established unchanged models/source/config/pixels, corrected docs and exact runtime pins; report inqa/r20-doc1-independent-sol61.'},{'id':'continuous-motion-review-pending','status':'resolved','description':'Need real orbit/zoom to assess fine leaf temporal quality.','resolution':'Independent b3107dc video decode/trace and sampled actual pixels show no new blocking defect; subpixel aliasing retained as explicit limit.'},{'id':'final-stage-assembly-pending','status':'resolved','description':'Independent seven-stage exact-subject assembly required.','resolution':'This independent record binds all seven current structured reports and frozen evidence; final integrity/require-approved results saved alongside.'}]
record['acceptance_scope']={'classification':brief['claim_scope'],'device_scope':'M5 Pro/ANGLE Metal recorded profile only','frame_time_target_ms':16.7,'software_performance':'SwiftShader failed all strict rAFp95 cases; retained, not accepted','limitations':limitations,'frozen_doc_commit':'062be906210f34f206748a313e288934a52a2c4f','base_gpu_evidence_commit':'c92f41539448758817635d0e8b5a4701e12fdfe2','continuous_motion_commit':'b3107dc7a5e04c2fd1cb0031ebb1bdb4f8cdfc17','old_QA_modified':False,'publication_authority':'separate; no publication performed'}
sys.path.insert(0,str(REPO/'scripts'))
from validate_candidate import approval_snapshot_sha256
record['approval']={'status':'approved_for_brief','reviewer':reviewer,'reviewed_at':now,'subject':subject,'note':'Independent acceptance for generic user-selected airy A within explicit M5 Pro/Metal measured use scope only. No all-device/software/dense-forest/scientific-reconstruction guarantee; publication remains separate.','review_snapshot_sha256':approval_snapshot_sha256(record)}
write(Q/'candidate.independent.json',record)
print('Assembled independent doc1 seven-stage record; original candidate/QA unchanged.')
