import pathlib,json,hashlib,datetime,subprocess,zipfile
O=pathlib.Path('/workspace/shared/lowpoly-batch92-independent-qa-20261020');R=pathlib.Path('/workspace/shared/lowpoly-batch92-20261020');P=R/'production/batch92'
J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
chain=J(O/'chain-audit.json');assert chain['all_checks_pass']; im=J(O/'input-manifest.json')
for p in [P/'source-and-concept-observations.json',P/'generator-authoring-record.json',P/'local-preservation-policy.json']:
 im[str(p)]={'bytes':p.stat().st_size,'sha256':H(p)}
(O/'input-manifest.json').write_text(json.dumps(im,indent=2)+'\n')
observations={
'eophyllophyton':{
'concept':'Concept has comparatively broad, ginkgo-like leaf fans and a heavy tree axis. The original frozen brief explicitly rejects those features. The final geometry is not accepted on concept resemblance alone.',
'source':'Hao et al. 2003 primary article text, on its publisher abstract and author-uploaded full-text page, supports tiny strongly divided blades on axes, occasional paired leaves, and uncertainty in their three-dimensional form. The inspected seven-panel fossil plate is a secondary-hosted reproduction attributed to Hao and Xue 2013, not an accessed original publisher plate.',
'views':{
'hero':'Slender open axes, attached terminal paired leaf clusters, no broad continuous ginkgo blades; grounded basal stem.',
'reversehero':'Opposite side shows branching depth and terminal leaf attachments without a planar billboard.',
'front':'Small leaf units remain subordinate to the three-axis framework; incised margins read as thin divided lobes.',
'side':'Nonzero depth with projected branch overlap; no visibly floating lateral or detached leaf fan.',
'rear':'Reverse branching and foliage are consistent with hero; no hidden-sheet substitution.',
 'top':'Radially spaced shoots and three-dimensional leaf poses; pair overlaps do not become a continuous canopy.',
'clay':'Volumetric axis caps and thin solid leaves remain coherent without palette cues.',
'silhouette':'Open branching structure and divided terminal margins; no visible framing clipping or detached patches.'},
'judgment':'Pass within selected-axis artistic reconstruction scope. Whole habit, exact 12 pairs, palette and scale remain artistic. Fine unequal laminar divisions are small at 512px, not evidence of anatomical venation or a literal fossil replica.',
'component_summary':'24 nonempty single-connected leaf groups on 12 terminal shoots. Actual projected longitudinal spans 3.288803–4.000001 mm and transverse spans 2.934385–3.305769 mm satisfy the original 2.2–5 and 1.7–4.8 mm hard intervals. Paired material thickness is approximately 0.120 mm; folded normal extent was separately measured and is not misused as the thickness requirement.'},
'thrombolite-mound':{
'concept':'The generated image contains photoreal surface speckling and relief-like cut clots. Frozen choices instead call for a texture-free faceted mound and diagrammatically enlarged, integrated clotted cut.',
'source':'UGS Special Study 168 text and actual PDF pages 22–23 were inspected, including Figure 10 mound, Figure 11 core and clotted micrograph, and oncoid contrasts. The source distinguishes clotted internal fabric from lamination; a cut face at model scale is illustrative rather than a literal micrograph extruded into rock. UGS was an explicitly frozen replacement for unavailable inventory USGS sources.',
'views':{
'hero':'One squat solid mound with front cut; irregular branching dark/light fabric remains on the cut rather than stacked horizontal laminae.',
'reversehero':'Continuous domed rear; visible regular facet rows are exterior low-poly shading, not painted diagnostic stromatolite bands.',
'front':'Connected irregular clot patches in a continuous matrix; no parallel internal lamination, detached pebble overlays or apparent doubled faces.',
'side':'Cut wall closes into the rounded rear with a grounded bottom; silhouette is coherent.',
'rear':'Single closed faceted arch volume; no separate plane or open shell exposed.',
 'top':'Continuous mound footprint and mildly irregular faceted contour; no floating cut component.',
'clay':'Solid integrated cut confirms full-volume surface; internal color fabric deliberately disappears in clay, as a planar geological section should.',
'silhouette':'One intact squat volume with no detached fragments or framing clipping.'},
'judgment':'Pass as a stylized pedagogical cutaway, not a naturalistic locality specimen. Exterior is deliberately simplified and its facet grid remains noticeable. No new universal prohibition on regular meshing is imposed; diagnostic internal clots, not the external facet grid, govern this frozen scope.',
'component_summary':'One mesh and one connected closed component. Actual whole XYZ bounds 0.604465 × 0.400000 × 0.283130 m are inside 0.5–0.7 × 0.28–0.5 × 0.22–0.36 m.'},
'oncoid-bed':{
'concept':'Concept supports separate rounded grains and three visible cuts, but its numerous photoreal small pebbles and uniform onion-like rings are not factual requirements. Original freeze chooses 16 grains, three uneven internal coating exposures and a quiet shallow base.',
'source':'UGS Figure 12 polished slab and Figure 13 core show separate coated grains and nuclei. The primary Hydra article oncoid subsection describes irregular, roughly concentric, partially overlapping coatings and asymmetric forms. Its 1.8–4.1 mm locality grain sizes are not applied to this explicitly generic artistic centimetre-scale teaching bed.',
'views':{
'hero':'Three front cuts have distinct nuclei and uneven interrupted coatings; intact grains remain separate rounded volumes.',
'reversehero':'Rear grains have faceted rough exteriors rather than exposed cortical rings painted around every sphere.',
'front':'All three cut faces are readable with separated nuclei; bed remains subordinate.',
'side':'Shallow support slab and rounded grain depth are clear; no floating cut planes.',
'rear':'Rounded closed backs show facet lighting, not internal cortical band material; grain-base contact is visually coherent.',
 'top':'Sixteen identifiable grain locations, with some normal contact/overlap; no continuous fused mound.',
'clay':'Three geometric cuts remain flat within otherwise full-volume grains; contacts show no visible coplanar flicker pattern.',
'silhouette':'Subordinate shallow bed supports solid grain profiles with no detached floating outlines.'},
'judgment':'Pass for generic geological teaching asset. Coating rings are section-only; the exterior facet palette and repeated rounded modules are stylized, not a claim of exact natural surface texture. Normal intersecting contact volumes are not rejected absent a visible defect.',
'component_summary':'Actual connectivity yields 17 closed source shells: sediment plus 16 grains. Three cut-grain groups correspond to actual grain shells. Actual whole bounds 0.244806 × 0.180000 × 0.052606 m are inside the original hard ranges.'},
'caytonia':{
'concept':'Concept incorrectly suggests distal longitudinal slits and a heavier woody axis. The original freeze rejects this and requires proximal mouth/lip directions on near-subopposite pairs.',
'source':'Taylor and Taylor 2009 primary review text supports a slender axis with subopposite stalked recurved cupules and a lip towards attachment. The inspected official Shi et al. 2021 Extended Data Figure 6 pixels and locally retained official caption show two ranks, compressed cupules, proximal lips and no individual subtending bracts. Elgorriaga et al. 2019 primary text retains whole-plant association and habit uncertainty.',
'views':{
'hero':'Twelve compact rounded cupules on six paired levels, attached by slender lateral stalks; no distal egg slit.',
'reversehero':'Reverse body surfaces and stalks remain coherent; cupules are solids, not paired picture planes.',
'front':'Six near-subopposite pairs and a slender central axis are readily countable; mouths are mostly edge-on at this angle.',
'side':'Compressed but nonzero volumetric depth is evident; paired cupules overlap in projection as expected for two ranks.',
'rear':'Closed rounded back faces, no speculative seeds or whole-plant foliage.',
 'top':'Shallow three-dimensional stalk/cupule pose and small proximal rim/attachment relationships can be seen; depth is not a zero-thickness sheet.',
'clay':'Rounded compressed cupules and thin real stalks persist without material cues.',
'silhouette':'Twelve separated cupule profiles on one reproductive axis, without roots, fruit slits or foliage.'},
'judgment':'Pass as isolated reproductive organ. Tiny proximal lips are not prominent in the full-asset 512px hero, so these stills are not a close-up anatomy plate. Actual rim-to-centroid direction was independently measured against actual stalk-root vertices, not trusted from a config direction. No whole-plant or angiosperm-fruit interpretation is approved.',
'component_summary':'12 cupules across six pair levels and 12 stalk groups. Every actual mouth direction points towards its actual attachment, minimum cosine >0.9999999999998. Actual Y thickness 4.767148 mm is within original 4–14 mm interval; XYZ are 21.426361 × 4.767148 × 52.028053 mm.'}}
source_review={
'observer':'fresh independent full-batch reviewer /root/resume_parallel_model_production/review_batch92_candidates',
'recorded_at':now,'actual_images_opened':[
'/workspace/shared/lowpoly-batch92-evidence/reference-pixels/eophyllophyton-secondary-fig2-2.png','/workspace/shared/lowpoly-batch92-evidence/reference-pixels/ugs-primary-022.png','/workspace/shared/lowpoly-batch92-evidence/reference-pixels/ugs-primary-023.png','/workspace/shared/lowpoly-batch92-evidence/reference-pixels/caytonia-shi2021-ed6.jpg'],
'primary_text_read':[
{'url':'https://www.journals.uchicago.edu/doi/10.1086/344557','scope':'Publisher abstract, not paywalled full PDF.'},
{'url':'https://www.researchgate.net/publication/249158474_Structure_of_the_Earliest_Leaves_Adaptations_to_High_Concentrations_of_Atmospheric_CO_2','scope':'Author-uploaded primary article text, particularly results and dimensions.'},
{'path':'/workspace/shared/lowpoly-batch92-evidence/reference-pixels/ugs-ss168.txt','scope':'UGS SS168 definitions, Figure 7 text and Figures 10–13 captions alongside actual page pixels.'},
{'url':'https://geology.utah.gov/energy-minerals/hydrocarbons/microbialites/','scope':'First-party UGS overview and explicit first-party SS168 link.'},
{'url':'https://onlinelibrary.wiley.com/doi/10.1002/dep2.117','scope':'Primary oncoid subsection and distinction from ooids.'},
{'url':'https://bsapubs.onlinelibrary.wiley.com/doi/10.3732/ajb.0800202','scope':'Primary review Caytoniales ovulate organ section; no longer treating its 2009 no-anatomy claim as a current absolute.'},
{'path':'/workspace/shared/lowpoly-batch92-evidence/reference-pixels/caytonia2019.txt','scope':'Primary introduction and limitations on whole-plant association.'},
{'url':'https://www.nature.com/articles/s41586-021-03598-w/figures/9','local_path':'/workspace/shared/lowpoly-batch92-evidence/reference-pixels/shi2021-fig9.html','scope':'Official locally preserved caption inspected after current web retrieval cache miss; actual figure JPEG also opened. No claim full Nature article read.'}],
'not_inspected':['UGS poster page pixels; poster not used for the verdict.','Original publisher Hao and Xue 2013 full article.','Nature full paywalled 2021 article.'],
'copyright':'All source images consulted in place only; no third-party source pixels copied into QA deliverables or geometry.'}
(O/'source-and-pixel-review.json').write_text(json.dumps({'source_review':source_review,'assets':observations},indent=2)+'\n')
assets=[]
for a in chain['assets']:
 d=O/a['asset_id'];src=J(d/'source-inspection.json');kh=J(d/'khronos.json')
 stages={s:{'status':'pass','scope':'static-only independent evidence'} for s in ['technical','visual','factual','specification','runtime_parse']}
 stages['gpu']={'status':'unknown','execution':'not_run','reason':'No actual target graphics-device render was executed. CPU stills and Node parse do not qualify.'}
 stages['scene']={'status':'unknown','execution':'not_run','reason':'No intended populated/composed scene or site-level inspection was executed.'}
 assets.append({**a,'verdict':'PASS_STATIC_ONLY','stages':stages,'observations':observations[a['asset_id']],'fresh_source_reopen_pid':src['pid'],'fresh_reexport_byte_identical':True,'fresh_khronos':kh['report']['issues'],'approvals':{'formal':False,'user':False,'site':False,'release':False,'live':False},'evidence':{n:{'path':str((d/n).relative_to(O)),'sha256':H(d/n)} for n in ['source-inspection.json','runtime-parse.json','khronos.json','candidate-validation.json','concept-validation.json']}})
limitations=[
'Only technical, visual, factual, specification and runtime_parse static stages pass. GPU and scene remain unknown/not run. This is not formal, user, website, release or live approval.',
'Historical timing statements are auditable source-process attestations. Recorded freeze precedes executed geometry and observed authoring completion; exact first modeling-authoring start, provider generation time and exact original source-pixel opening time were not captured. They remain unknown. No file mtime was used to invent chronology.',
'Both recorded semantic rebuild chains per final asset were checked in full against original local request/result/stdout/stderr/execution/output bytes, with distinct PIDs. This independent review additionally executed one real source reopen and byte-identical reexport per asset; it did not claim to have rerun the maker’s two builds.',
'32 individual final 512px images, four lossless contact sheets, four concepts and four actual reference image files were personally opened. Every sheet tile was pixel-compared to its individual image. Visual acceptance is limited to these exact stills; later target-view artifacts may require geometry repair.',
'The first independent candidate-validator invocation passed dictionaries to a path-only API. Its four harness errors are retained as candidate-validation-harness-attempt1.json and chain-audit-harness-attempt1.json. Corrected path arguments pass; this was a QA harness issue, not altered candidate evidence.',
'A preliminary local HTML extraction attempted unavailable bs4, then succeeded using Python standard-library HTML stripping. No package was installed.',
'No source/frozen brief/reference/model/raw evidence was modified. No push, PR, merge, website build, full clone, install, credential or environment change. Reexport GLBs are local-only and excluded from the compact report archive.'
]
report={'schema_version':1,'kind':'independent-full-four-id-static-qa','review_id':'batch92-independent-qa-20261020-v001','reviewer':source_review['observer'],'completed_at':now,'source_commit':chain['source_commit'],'source_parent':chain['source_parent'],'source_branch':chain['source_branch'],'verdict':'PASS_STATIC_ONLY','all_four_static_pass':True,'chain_checks_passed':chain['checks_count'],'assets':assets,'source_review':source_review,'limitations':limitations,'approvals':{'formal':False,'user':False,'site':False,'release':False,'live':False},'repair_requested':False,'raw_inputs_read_only':True,'sources_unchanged':subprocess.check_output(['git','status','--porcelain'],cwd=R,text=True)==''}
assert report['sources_unchanged'];(O/'REPORT.machine.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# Batch92 independent QA v001','', '**Verdict: PASS_STATIC_ONLY for all four exact candidates.**','',f"Fixed commit: `{chain['source_commit']}`. Direct parent: `{chain['source_parent']}`. Branch: `{chain['source_branch']}`.",'','Technical, visual, factual, specification and runtime_parse pass. GPU and scene remain **unknown / not run**. No formal, user, site, release or live approval.','', '## Independently executed and measured','',f"- {chain['checks_count']} integrity, provenance, schema, final-pixel and dimensional checks pass.",'- Four .blend sources freshly reopened with autoexec disabled and actual authored/evaluated vertices measured. Four real GLB reexports are byte-identical to the fixed originals. Fresh Blender PIDs: Eophyllophyton 7, thrombolite 37, oncoid 67, Caytonia 97.','- Every heavy process used blocking global flock and Blender threads 2, releasing per process.','- Fresh project audits pass; fresh Khronos reports each have zero errors and warnings. Fresh Three.js 0.180 GLTFLoader parse passes. No rendering work is relabeled GPU evidence.','- Raw original two-build chains were independently checked, including outputs, timestamps, request/result snapshots and distinct Blender PIDs: 46/71, 165/190, 284/309, 403/428 respectively.','- Immutable round39 claim/inventory/requirements match; all original r001 freeze files match their manifest. Derived candidate briefs only add deliverable closure, with no changed original design field.','- Exact GLB/derived brief/references triplets are fixed before every final render invocation. All 32 final frame hashes and 512×512 sizes match, and all 32 sheet tiles are pixel-identical.','- I personally opened all 32 individual finals, all four lossless sheets, all four concepts, and the four reference-pixel files. The UGS poster was not inspected or used.','']
for a in assets:
 o=observations[a['asset_id']];lines += [f"## {a['asset_id']} {a['revision']}: PASS_STATIC_ONLY",'',f"{a['counts']['triangles']} triangles; {a['counts']['glb_bytes']} GLB bytes; {a['counts']['materials']} materials / {a['counts']['primitives']} primitives; zero textures.",'',o['component_summary'],'',o['judgment'],'',o['source'],'']
lines += ['## Limits and exact evidence','','The fixed machine report contains every exact subject triplet, seven stage states, per-view observations and source scopes. `exact-triplets.json`, `chain-audit.json`, `input-manifest.json`, the four fresh source/runtime/Khronos report sets, and `source-and-pixel-review.json` provide the full audit trail.','']+['- '+s for s in limitations]
(O/'REPORT.md').write_text('\n'.join(lines)+'\n')
(O/'.gitignore').write_text('*/reexport.glb\nreport-package.zip\n')
manifest=[]
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name not in {'ownmanifest.json','HANDOFF.md','report-package.zip'}:
  manifest.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'sha256':H(p),'disposition':'local-only-reexport-not-for-git' if p.suffix=='.glb' else 'review-evidence'})
(O/'ownmanifest.json').write_text(json.dumps({'created_at':now,'files':manifest,'self_and_handoff_excluded_to_avoid_circular_hashes':True},indent=2)+'\n')
handoff=f'''# Batch92 fixed independent QA handoff

All four: PASS_STATIC_ONLY. No repair requested for the fixed static candidates.

Input commit: {chain['source_commit']}
Input direct parent: {chain['source_parent']}
Input branch: {chain['source_branch']}
Independent output root: {O}

- Machine report: REPORT.machine.json SHA256 {H(O/'REPORT.machine.json')}
- Readable report: REPORT.md SHA256 {H(O/'REPORT.md')}
- Own manifest: ownmanifest.json SHA256 {H(O/'ownmanifest.json')}
- Exact triplets: exact-triplets.json SHA256 {H(O/'exact-triplets.json')}

Technical / visual / factual / specification / runtime_parse pass. GPU / scene unknown, not run. Formal / user / site / release / live approvals false. Exact first authoring and provider timestamps remain unknown; recorded freeze and real execution chain retained. Source checkout remains clean. No external changes were made.

Report package is compact and excludes four duplicate local reexport GLBs, all maker raw outputs, and all consulted source pixels/PDFs. Original artifacts and failed attempts remain untouched in their original paths. Read the report limitations before using this verdict. Do not rebind it to changed GLBs, briefs or references.
'''
(O/'HANDOFF.md').write_text(handoff)
with zipfile.ZipFile(O/'report-package.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(O.rglob('*')):
  if p.is_file() and p.suffix!='.glb' and p.name!='report-package.zip':z.write(p,str(p.relative_to(O)))
print(json.dumps({'verdict':report['verdict'],'report_sha256':H(O/'REPORT.machine.json'),'handoff_sha256':H(O/'HANDOFF.md'),'manifest_sha256':H(O/'ownmanifest.json'),'archive_sha256':H(O/'report-package.zip'),'archive_bytes':(O/'report-package.zip').stat().st_size,'local_bytes':sum(p.stat().st_size for p in O.rglob('*') if p.is_file()),'source_clean':report['sources_unchanged']},indent=2))
