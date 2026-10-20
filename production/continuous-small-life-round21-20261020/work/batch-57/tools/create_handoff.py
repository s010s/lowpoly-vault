import pathlib,json,hashlib,datetime,shutil
from PIL import Image,ImageDraw
R=pathlib.Path.cwd();W=R/'production/continuous-small-life-round21-20261020/work/batch-57';C=R/'assets/candidates/continuous-small-life-round21-20261020/batch-57';F=json.loads((W/'final-selection.json').read_text())['assets'];h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
items=[]
for a,rev in F.items():
 d=C/a/rev;im=Image.new('RGB',(2048,1080),'white');dr=ImageDraw.Draw(im)
 for k,n in enumerate(['hero','reversehero','front','side','rear','top','clay','silhouette']):im.paste(Image.open(d/f'proof-final/{n}.png'),(k%4*512,k//4*540));dr.text((k%4*512+8,k//4*540+512),n,fill='black')
 im.save(d/'eight-views-final.png')
 identity={'asset_id':a,'revision':rev,'root':str(d.relative_to(R)),'glb_sha256':h(d/f'{a}.glb'),'candidate':str((d/'candidate.json').relative_to(R)),'metrics':json.loads((d/'metrics.json').read_text()),'stages':{s:x['status'] for s,x in json.loads((d/'candidate.json').read_text())['stages'].items()},'concept_integrity':{'valid':True,'evidence_complete':False,'limitations':['Provider exact generation time unknown','Generator authoring start unknown']},'acceptance':'pending; not approved'};items.append(identity)
 # extra integrity manifest excludes itself and checker outputs; no circular hashes
 files={str(p.relative_to(d)):h(p) for p in d.rglob('*') if p.is_file() and p.name!='hashes.sha256'}
 (d/'hashes.sha256').write_text(''.join(f'{sha}  {f}\n' for f,sha in sorted(files.items())))
claim=json.loads((W/'claim.json').read_text());claim.update(status='candidate_delivery_pending_independent_qa',blender_started=True,concepts_generated=True,final_revisions=F,completed_at=now(),not_approved=True);(W/'claim.json').write_text(json.dumps(claim,indent=2))
handoff={'batch_id':'batch-57','branch':'candidate/small-life-batch57-concept-20261020','base_main':'0cbef7c9826ddd1d83e7d0c941b7864dbaa6865c','planning_commit':'53fe7ef3bb50fea084acc7ea5f5e52c47a472156','task_id':'01a1570a-a6b4-7734-a288-c61fe31fe0c8','turn_id':'01a1570a-aff9-73b3-bcfa-060571e95b79','created_at':now(),'source_commit':None,'source_commit_note':'Parent must pin actual final pushed commit; commit cannot self-embed its SHA. Exact SHA returned in completion message. Original QA-SCOPE dispatch template preserved.','items':items,'independent_review':'Parent only; exactly one fresh-context GPT-6 Luna xhigh full batch QA, then targeted differences only. Maker launched no independent QA.','remaining_limits':['Nidula corrected holotype figure pixels unavailable; no figure-match PASS.','Quatsinoporites regular pore grid remains a visible craft concern; r002 failed geometry checks, baseline retained.','Rusophycus slab outline remains simple; attempted r002 irregular outline failed degenerate triangle check.','Physical GPU and intended populated scene not run.','Provider model/seed/request ID/start/end and generator authoring-start unknown.','Source helper metadata.json records staging paths; authoritative delivery paths are candidate.json and delivery.json.'],'ordinary_push_only':True,'publication':'No main merge, production release/site edits, PR, deploy or Drive upload.'}
(W/'handoff.json').write_text(json.dumps(handoff,indent=2,ensure_ascii=False)+'\n')
rows='\n'.join('| '+x['asset_id']+' | '+x['revision']+' | '+str(x['metrics']['triangles'])+' | '+str(x['metrics']['glb_bytes'])+' | `'+x['glb_sha256']+'` |' for x in items)
(W/'HANDOFF.md').write_text('''# Batch 57 candidate handoff

Branch: `candidate/small-life-batch57-concept-20261020`. Base main: `0cbef7c9826ddd1d83e7d0c941b7864dbaa6865c`. Planning inputs: `53fe7ef3bb50fea084acc7ea5f5e52c47a472156`. Original full-round checksums verified against original Git package (28/28); only this batch inputs imported, no planning merge. Old frozen files and original 1000 inventory unchanged.

Maker task/thread `01a1570a-a6b4-7734-a288-c61fe31fe0c8`, turn `01a1570a-aff9-73b3-bcfa-060571e95b79`, supplied by parent creation result. GPT-6.1 Sol medium. No independent reviewer spawned here.

| Asset | Fixed revision | Triangles | GLB bytes | SHA-256 |
|---|---|---:|---:|---|
'''+rows+'''

Each selected revision has editable Blend, standalone GLB, generator/config/seed, original shared four-row ImageGen concept and exact prompt/available result record, original modeling freeze, references, nominal display envelope and separately measured Blender XYZ / glTF XYZ, candidate JSON, metrics, hashes, preview and eight exact-GLB views, original and explicitly derived static-label render manifests, source reopen, two successful queue-bound semantic rebuilds, Khronos and pinned Three.js parse results. `candidate.json`/`delivery.json` contain authoritative artifact paths. Original helper `metadata.json` is retained as staging receipt.

Delivery brief `brief.delivery-v003.json` is a truthful post-build declaration with actual source/generator/config required_deliverables paths and hashes. Original `brief.json`/modeling freeze retained unchanged. No source hash or packaging declaration backdated before modeling. `delivery-freeze-v003.json` binds the new declaration. The renderer labels canonical 90-degree side as right internally; `render-manifest-static.json` and `render-config-static.json` explicitly normalize that semantic label only, retaining original manifest/config, all camera values and exact image bytes.

Technical and runtime_parse PASS from current bound raw outputs. Four static-profile candidate integrity checks valid, approval false. Khronos 0 errors / 0 warnings. Visual/factual/specification unknown pending parent QA; gpu/scene unknown and unrun. Cycles CPU renders are not GPU/device performance proof.

Concept helper valid but --require-complete fails honestly: provider exact generation timestamp and generator authoring start are unknown. Actual invocation observation, receipt, pixel inspection, process execution and wall times retained where observed. No mtime-derived chronology; provider model/seed/request ID remain unknown.

Bounded revision outcomes: cave-column r002 improves offset fused growth/attachments; Nidula r002 replaces nondeterministic sphere index order with an original deterministic lenticular loft. Quatsinoporites/Rusophycus attempted r002 refinements fail source geometry degeneracy checks and are preserved, not selected. Final Quatsinoporites r001 has genuine pore cavities and broken block edges but still visibly regular pore pattern; Rusophycus r001 has deep negative lobes and scratch fields on a simple rectangular slab. No further cosmetic loop.

Nidula access limit: primary publisher corrected figure endpoints 403, Oregon State endpoint 418 in web / 403 direct. Author manuscript text available via Academia; original figures 1–2 identified as AF-9-20B, figure 3 excluded. Corrected figure pixels not inspected; no specimen-match factual PASS. Basic form is source-informed; colors, display scales and unseen geometry are artistic choices.

Parent should pin actual pushed commit and four hashes in a NEW QA scope, then dispatch exactly one fresh-context GPT-6 Luna xhigh independent full review. Original batch-57-QA-SCOPE.json remains an unpopulated dispatch template. No merge, PR, main/site/production-release modification or deployment performed.
''')
for src,name in [('/tmp/b57-npm.log','dependency-install-initial.log'),('/tmp/b57-npm-retry.log','dependency-install-tmp-cache.log'),('/tmp/b57-progress.log','initial-lifecycle.log'),('/tmp/b57-progress-retry.log','retry-lifecycle.log'),('/tmp/b57-final-queue.log','final-queue.log'),('/tmp/b57-final-progress.log','final-validation.log'),('/tmp/b57-baseline-delivery.log','baseline-delivery.log'),('/tmp/b57-nidula-r002-build.log','nidula-r002-initial-build.log'),('/tmp/b57_package.py','tools/package_evidence.py'),('/tmp/b57_handoff.py','tools/create_handoff.py')]:
 if pathlib.Path(src).exists():shutil.copyfile(src,W/name)
print(rows)
