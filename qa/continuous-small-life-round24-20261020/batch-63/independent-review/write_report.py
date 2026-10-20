#!/usr/bin/env python3
from pathlib import Path
import json
OUT=Path('/workspace/shared/lowpoly-round24-qa63')
REPO=Path('/tmp/lowpoly-batch63-20261020')
BATCH=REPO/'assets/candidates/continuous-small-life-round24-20261020/batch-63'
root=json.loads((OUT/'integrity-summary.json').read_text())
extra={
'siphusauctum':{
 'visual':'ACCEPT BOUNDED','factual':'ACCEPT BOUNDED','specification':'ACCEPT BOUNDED',
 'notes':'Whole external organism reads as a coherent holdfast + bilayered stem + closed ovoid calyx. Six actual basal through-ports and one terminal top opening are present; no petal/arm/tentacle reading. The ROM source supports the external fossil morphology; uncertain affinity, exact proportions and palette stay illustrative. No modern phylum or internal-anatomy claim.',
 'reference_url':'https://burgess-shale.rom.on.ca/fossils/siphusauctum-gregarium/','reference_image_sha256':'c5a8198f50b969bae0c0126b10c3ed06030420c0dadf1af910a908f8fc1b3026'},
'esker':{
 'visual':'ACCEPT BOUNDED','factual':'ACCEPT BOUNDED','specification':'ACCEPT BOUNDED',
 'notes':'A positive, sinuous S-ridge with rounded uneven crest and sloping flanks; top/oblique views do not read as a channel, riverbed or canyon. Generic full-volume landform, not named, dated, or directionally asserted. Surface is intentionally quiet/texture-free and scale remains illustrative.',
 'reference_url':'https://www.usgs.gov/media/images/a-simple-esker-iceland','reference_image_sha256':'630a6296a521b88caffe3d539fec856bd758f3a25cbdaab4d60510cf22c92adb'},
'caldera':{
 'visual':'REVISE','factual':'REVISE (frozen feature evidence incomplete)','specification':'REVISE',
 'notes':'Broad subsided basin, floor, inward scarp and outward slope are present and low relief is appropriate. However hero/reverse/front/top show a largely continuous, nearly regular terraced rim; the subdued breach is only a shallow, hard-to-read dip, so the frozen uneven remnant rim and one-breach obligations are not clearly evidenced. Minimal repair: preserve r001 scale and basin, make one small but unambiguous low saddle interrupt the rim in top + oblique views, and vary only adjacent rim/scarp heights into restrained irregular bays. Do not add a dramatic opening, starburst fluting, lava, or any new claim. r002 attempt was correctly rejected for starburst-like regularity; r001 is unchanged.',
 'reference_url':'https://home.nps.gov/articles/000/older-caldera-complexes.htm','reference_image_sha256':'521addd6146d20e9eee40e7a1ca3a5006b07ea0d8c586830e48f5053325b5508'},
'dogtooth-spar-cavity':{
 'visual':'ACCEPT BOUNDED','factual':'ACCEPT BOUNDED','specification':'ACCEPT BOUNDED',
 'notes':'Open-front, deep cavity with thick closed host/back; irregular inward-pointing acute crystals have triangular/scalenohedral planes, mixed lengths/depths and preserve a readable void. NPS supports pointed calcite dogtooth spar lining limestone pockets; the Smithsonian National Museum of Natural History source also explicitly identifies dogtooth calcite as scalenohedral. Supports a generic habit, not an assay, measured specimen, or specific cave-site claim.',
 'reference_url':'https://www.nps.gov/wica/learn/nature/cave-formations-speleothems.htm','reference_image_sha256':'dc6d532a76a34e349dfaf4c877a71c11278d712afcc6422eb2650d25cfe8a4e0'} }
for a in root['selected_assets']:
    d=BATCH/a['asset_id']/a['revision']
    metrics=json.loads((d/'metrics.json').read_text())
    brief=json.loads((d/'brief.json').read_text())
    config=json.loads((d/'build-config.json').read_text())
    cgen=json.loads((d/'concept-generation.json').read_text())
    a['bounds_gltf_xyz_m']=metrics['glb']['bounds_m']['size']
    a['nominal_dimensions_blender_xyz_m_illustrative']=brief['nominal_dimensions_blender_xyz_m']
    a['illustrative_dimensions_note']=brief['scale_note']
    a['local_procedural_seed']=config['seed']
    a['dependency_versions']={'Blender':config['blender_version'],'Three.js':config['three_version'],'GLTF exporter':metrics['glb']['generator']}
    a['concept_generation']={'tool':cgen['tool_name'],'request_observed_at':cgen['request_observed_at'],'completion_observed_upper_bound':cgen['completion_observed_upper_bound'],'inspection_observed_at':cgen['inspection_observed_at'],'provider_generation_timestamp':'unknown','provider_model_seed':'not returned','modeling_start_timestamp':'not sampled'}
    a['eight_view_names']=['hero','reversehero','front','side','rear','top','clay','silhouette']
    a['independent_disposition']=extra[a['asset_id']]
    a['technical']='PASS'
    a['runtime_parse']='PASS (Three.js GLTFLoader.parseAsync, Three r180; CPU only)'
    a['gpu']='NOT RUN / UNKNOWN'
    a['scene']='NOT RUN / UNKNOWN'
    a['formal_user_approval']='PENDING; no approval status changed'
    a['concept_evidence_completeness']='INCOMPLETE for all: concept_generated_at and modeling_started_at unknown; evidence valid but not complete'
    a['proof_frames']='all 8 fixed views at 512x512 independently checked, manifest subject pins exact GLB + frozen brief + references'
root['disposition_note']='ACCEPT BOUNDED is the independent QA recommendation for technical/factual/visual/specification/runtime_parse only; it does not alter candidate approval or constitute formal/user approval. All GPU, populated-scene, formal and publication approvals remain unperformed/pending. Caldera is REVISE.'
root['independent_validators']={
 'candidate_and_profile':'PASS valid/no errors; profile contract pass; approved_for_brief=false and stages/approvals remain pending/unknown',
 'concept_evidence':'valid=true; evidence_complete=false; exact blockers: provider concept generation timestamp unknown and modeling start timestamp unknown; no mtimes used to infer them',
 'project_glb_qa':'PASS on a separate exact copy per selected GLB',
 'khronos':'PASS 0 errors / 0 warnings for each selected GLB on separate exact copies',
 'threejs':'PASS exact hash parse with Three.js r180 GLTFLoader.parseAsync; CPU parser only, not GPU or scene test',
 'blender':'read-only Blender 4.3.2 reopen; authored/evaluated counts and axis-converted exported bounds reconcile; per-mesh welded boundary/nonmanifold/wire/degenerate counts all zero',
 'topology':'independent custom GLB mesh weld audit; all boundary/nonmanifold/degenerate/duplicate triangle counts zero per mesh',
 'rebuilds':'two different queue-bound successful Blender builds per selected GLB: distinct request/result files, output directories, PIDs and ordered UTC run times; selected output bytes equal final GLB; independently recomputed semantic digest matches recorded digest for each run. Queue records are attestations, not cryptographic execution proof.'}
root['release_scope']='No source edits, commits, pushes, GitHub actions, approval flags, formal/user approval or publication actions.'
root['chronology_limitation']='Concept request/completion-observer/inspection records precede the frozen brief, and every successful queue generator run follows its freeze. However provider-internal exact concept-generated and modeling-start timestamps were not disclosed/sampled; concept validator therefore reports evidence_complete=false. Generator authorship start itself is not inferred from filesystem mtimes.'
root['references_conclusion']='Actual primary-reference pixels were inspected locally at /tmp/lowpoly-round24-primary-consulted/batch63, including the selected image for each cited source (and both ROM holotype/reconstruction images for Siphusauctum). Copyrighted reference pixels were not copied into QA report.'
(OUT/'machine-summary.json').write_text(json.dumps(root,indent=2,ensure_ascii=False)+'\n')

lines=['# Independent QA report: batch 63 fixed candidates','',
'## Executive disposition','',
'| Candidate | Technical | Visual | Factual | Specification | Runtime parse | Independent disposition |',
'|---|---|---|---|---|---|---|',
'| Siphusauctum r001 | PASS | PASS | PASS, bounded | PASS | PASS | ACCEPT BOUNDED |',
'| Esker r001 | PASS | PASS | PASS, bounded | PASS | PASS | ACCEPT BOUNDED |',
'| Caldera r001 | PASS | REVISE | REVISE, feature evidence incomplete | REVISE | PASS | REVISE |',
'| Dogtooth spar cavity r002 | PASS | PASS | PASS, generic habit bounded | PASS | PASS | ACCEPT BOUNDED |','',
'“Accept bounded” is an independent QA recommendation for technical, visual, factual, specification and CPU parser criteria only. The project candidate/profile validator still says valid/pending with approved_for_brief=false. GPU rendering, populated-scene rendering, formal approval, user approval and publication are not established. No approval flag was changed.','',
'## Exact source, selections and integrity','',
'- Source: `/tmp/lowpoly-batch63-20261020`, branch `candidate/small-life-batch63-concept-20261020`, clean HEAD `d840b363277c9f0727ffb93fdf9ca7dd27ca6f4b`.',
'- Exact selected GLBs:',
'  - Siphusauctum r001: `cc0b3d56057bba735d422feaae49485572e669cda131eb2b8d21830e892c31dc`.',
'  - Esker r001: `4415be20721b7002b0db1319287626915af648a2086c3ba50a54a8c4ca48b3ed`.',
'  - Caldera r001: `5d84c7b706351559d6217e558fc8ef5458a9374043a8d001a91708c788b51258`.',
'  - Dogtooth-spar-cavity r002: `3db7f65435d8117dd71285b3fc7afb9d3e73f4ba68b3f2c99e219303dbb2b80c`.',
'- Independently matched handoff, candidate artifact records, brief/reference/source/generator/config pins, and each selected inventory row against the original inventory. Original inventory unchanged; source worktree remains clean.',
'- Maker revision chronology is documented: dogtooth r002 targeted visual refinement pins the original freeze and says no scope changes; caldera r002 starburst-like attempt rejected; r001 retained without alteration. No post-hoc scope narrowing is relied on.','',
'## Per-candidate findings','']
for a in root['selected_assets']:
    ident=a['asset_id']; q=extra[ident]
    lines += [f"### {ident} {a['revision']} — {q['visual']}", '',
              f"- **Visual / factual / specification:** {q['notes']}",
              f"- **Primary source page:** [{q['reference_url']}]({q['reference_url']}). Actual locally consulted reference-image SHA256: `{q['reference_image_sha256']}`.",
              ("- **Supplementary morphology check:** [Smithsonian NMNH calcite record](https://naturalhistory.si.edu/explore/collections/geogallery/10026196) supports the generic dogtooth/scalenohedral label; this does not narrow or alter the frozen claim scope.\n" if ident=='dogtooth-spar-cavity' else ''),
              f"- **Hashes:** GLB `{a['hashes']['glb']}`; frozen brief `{a['hashes']['brief']}`; references `{a['hashes']['references']}`; Blender source `{a['hashes']['source']}`.",
              f"- **Geometry:** {a['triangles']:,} triangles; {a['glb_bytes']:,} bytes; {a['materials']} materials; {a['primitives']} primitives; {a['textures']} textures. Measured GLB envelope X×Y×Z: `{a['bounds_gltf_xyz_m']}` m. Nominal plan only, not a measurement: `{a['nominal_dimensions_blender_xyz_m_illustrative']}` Blender XYZ m; `{a['illustrative_dimensions_note']}",
              f"- **Build provenance:** local procedural seed `{a['local_procedural_seed']}`; generator/config/source SHA256s as above; pinned dependencies `{a['dependency_versions']}`. Provider image-generation seed/version was not returned; it is not fabricated.",
              f"- **Blender source reopen:** {a['blender']['objects']} mesh object(s), {a['blender']['evaluated_triangle_equiv']:,} evaluated triangles reconcile with exported GLB; Blender XYZ bounds `{a['blender']['bounds_xyz_m']}` m (axis-converted bounds reconcile). Every mesh: zero welded boundary/nonmanifold/wire edges and zero degenerate triangulated faces.",
              f"- **Exact proof render:** {a['final_render_at']} by pinned CPU runner SHA256 `{a['render_runner_sha256']}`; `{', '.join(a['eight_view_names'])}` frames, each actual 512×512, individually inspected and hash-checked. Manifest subject binds selected GLB, brief and references. This is CPU-render evidence only, not GPU proof.",
              f"- **Two queue rebuilds:** {', '.join(f"run{b['index']} PID {b['pid']} {b['started_at']}→{b['finished_at']} SHA {b['output_sha256']} semantic {b['semantic_sha256']}" for b in a['rebuilds'])}. Distinct successful queue-bound requests/PIDs/output dirs; semantic digest independently recomputed on each output. Runner records remain attestations, not cryptographic execution proof.",
              '']
lines += ['## Independent validation and approval boundaries','',
'- Candidate/profile validator: `valid=true`, no errors, profile contract pass, but `approved_for_brief=false`; all formal candidate stages remain pending/unknown. Concept evidence validators are structurally valid but incomplete for all four because `concept_generated_at` and `modeling_started_at` are unknown. These exact provider/modeling timestamps were not disclosed/sampled; no file mtimes were used to invent them.',
'- Independent project GLB checks passed on separate exact copies. Khronos validator: zero errors and zero warnings on each. Independent Node Three.js r180 `GLTFLoader.parseAsync` parsed each exact hash and reconciled triangle counts/bounds. This is CPU parser evidence, not a browser GPU render or populated-scene result.',
'- Read-only Blender 4.3.2 reopen on all four exact `.blend` files; authored/evaluated vertices/polygons/triangle-equivalents match. Per-mesh welded topology audits show zero boundary, nonmanifold, wire, zero-area/degenerate, or duplicate triangles. Axis-converted source/export bounds reconcile within tolerance.',
'- Two actual successful queue-bound rebuilds per selected final GLB were verified independently: separate requests, results, PIDs, timestamps and output paths; Blender, queue runner, generator, config, helper and audit identities pinned; output GLB byte hashes match the selected GLB; semantic digests independently recomputed and match. Repro logs themselves are not cryptographic proof.',
'- Concept chronology: request/completion-observer/inspection records precede each freeze; actual successful queue generator executions follow freeze. Exact provider concept-generation and modeling-start timestamps are absent, as is an ImageGen provider seed; the concept evidence gate correctly remains incomplete. The selected local deterministic build seeds are recorded above and are distinct from an ImageGen provider seed.',
'- GPU stage: **not run**. Intended composed scene: **not run**. Formal/user approval: **not granted**. Publication authority: separate. No approval, upload, commit, push, merge or publish action was taken.',
'- External reference pixels are consult-only; no source image was copied into this report.','',
'## QA artifacts','',
'- Machine-readable summary: `machine-summary.json`.',
'- Independent integrity/rebuild/render-binding script: `audit_batch63_integrity.py`.',
'- Blender read-only source inspector: `work/read_blend_readonly.py`.',
'- Independent GLB topology auditor: `work/audit_glb_topology.py`.',
'- Independent Three.js parser: `work/runtime_parse_exact.mjs`.',
'- Khronos, Project QA, runtime parse, Blender per-mesh and two-run semantic-rebuild outputs are under `work/` (private exact GLB copies only).',
'- This report is a QA recommendation; it is not formal or user approval.']
(OUT/'report.md').write_text('\n'.join(lines)+'\n')
