# SPDX-License-Identifier: MIT
"""Bind actual maker evidence without asserting independent acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import subprocess

R=Path(__file__).resolve().parent
REPO=next(p for p in R.parents if (p/'scripts/asset_common.py').exists())
ASSETS=['sapeornis','longirostravis','dunbaria','chimerarachne']
VIEWS=['hero','reversehero','front','rear','left','right','top','bottom','clay','clayalt','wire']
def read(p):return json.loads(p.read_text())
def save(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p)}
def iso(s):return datetime.strptime(s,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=timezone.utc).isoformat()

def main():
    now=datetime.now(timezone.utc).isoformat();concept=read(R/'concept-generation.json');handoff=[]
    for slug in ASSETS:
        d=R/slug/'r001';o=d/'output'/slug;proof=d/('proof-macro-attempt02' if slug=='chimerarachne' else 'proof')
        generator=R/('generator-r001.py' if slug=='sapeornis' else 'generator.py')
        for n in [1,2]:
            attempts=list((R/'rebuild-runs/build'/slug/'r001'/f'rebuild-{n}').glob('*/*'))
            success=[p for p in attempts if (p/'result.json').exists() and read(p/'result.json')['status']=='succeeded'];assert len(success)==1,success
            p=success[0];dest=d/f'reproducibility-{n}.report.json'
            if not dest.exists():
                command=['python',str(REPO/'scripts/check_reproducibility.py'),'--glb',str(o/(slug+'.glb')),'--rebuilt-glb',str(p/'outputs'/slug/(slug+'.glb')),'--generator',str(generator),'--config',str(d/'build-config.json'),'--build-request',str(p/'request.json'),'--build-result',str(p/'result.json'),'--rebuilt-output',f'{slug}/{slug}.glb','--root',str(R),'--output',str(dest)]
                result=subprocess.run(command,capture_output=True,text=True);(d/f'reproducibility-{n}.log').write_text(result.stdout+result.stderr);assert result.returncode==0,(slug,result.stdout)
        qa=read(o/'qa.json');metric=read(o/'metadata.json');manifest=read(proof/'render-manifest.json');structure=read(d/'mesh-structure.report.json');roundtrip=read(o/'glb-roundtrip.report.json');validator=read(o/'gltf-validator.report.json')
        limitations={
         'sapeornis':'Outer wing silhouette remains narrow/pointed versus the broad-wing concept. R002 widened tips look paddle-like and do not deliver a clear craft improvement under locked camera/light conditions; R002 NOT ADOPTED. R001 remains a candidate with this explicit visual limitation; no visual/brief acceptance claimed.',
         'longirostravis':'Folded wings and paired narrow tail feathers deliberately simplified, feather counts/tooth detail are not fossil-exact. Neck/head transitions remain visibly faceted. No critical new maker-visible defect found in the eleven inspected frames; this observation is not independent acceptance.',
         'dunbaria':'Four main wings, six walking legs, two small front lobes and paired cerci are modeled. Front lobes use simplified thick leaf-like volumes rather than exact fossil cordate outlines. Wing vein network is sparse; bands/approximate dimensions are artistic. This remains a genus-inspired prop, not a species/sex-exact reconstruction.',
         'chimerarachne':'Eight walking legs, smaller paired pedipalps, segmented abdomen, whip tail and four simplified underside spinneret projections inspected. Exact spinneret homology/eye count/sex-specific palp form not claimed. Original common-renderer proof is too small for inspection; macro proof is final diagnostic evidence. Actual GLB scale is unchanged.'}
        note=f'''# Maker pixel-inspection record — {slug} r001

Record created {now}. Actual full-resolution view_image calls opened all eleven final frames individually in this session: {', '.join(VIEWS)}. This is the maker's inspection, not independent QA.

Source GLB SHA-256: {metric['sha256']['glb']}. Evidence: {proof.relative_to(R).as_posix()}/render-manifest.json. Body depth, paired appendage attachments and underside visible in reverse/top/bottom/clay/wire views. Separate closed components intentionally overlap; no assertion of a printable watertight union.

{limitations[slug]}

Technical warning review: Khronos {validator['issues']['numErrors']} errors / {validator['issues']['numWarnings']} warnings. Source audit warnings: {qa['source']['warnings']}. Sapeornis floor warning is expected for an explicitly flying center mount. Reimport status is {roundtrip['status']}, with {len(roundtrip['warnings'])} raw warnings retained: importer flags smooth faces and boundary edges after split normals/vertices. Actual saved source audit reports closed parts; additional position-weld audit at {structure["position_weld_tolerance_m"]:.12g}m (bbox maximum dimension times 1e-6) reports {sum(x['boundary_edges_after_position_weld'] for x in structure['imported_parts'])} boundary and {sum(x['nonmanifold_edges_after_position_weld'] for x in structure['imported_parts'])} nonmanifold edges across imported parts. This supports a representation-split explanation, not a general visual/material acceptance. Normals remain visibly faceted in proof; no artefact files were repaired by that audit.

No independent visual, factual or specification verdict has run. Three.js parse, actual GPU rendering, populated-scene evidence and formal gallery-renderer posters are deferred to the parent task. These diagnostic Blender frames must not be advertised as final gallery posters.

Original assets/renders/prose CC BY 4.0 — Leon Made This / s010s. Executable code MIT. Consulted scientific sources are separately owned, not incorporated.
'''
        (d/'maker-review.md').write_text(note)
        gen=read(o/'build-timing.json')
        inspections={'record_created_at':now,'inspector':'maker agent gpt-6.1-sol / medium; explicitly requested model','not_independent_qa':True,'method':'Actual view_image calls, each required PNG opened individually; timestamp is record creation after completed inspection, not reconstructed from mtimes','frames':[dict(id=f['id'],path=f['path'],sha256=f['sha256']) for f in manifest['frames']]}
        save(d/'maker-inspection.json',inspections)
        timings=[]
        for stage in ['imagegen','interpretation','modeling_export','proof_rendering','visual_review','target_browser']:
            status='unrecorded';seconds=None;record=None;why='Elapsed active work not separately measured; do not infer from mtimes.'
            if stage=='imagegen':status='measured';seconds=(datetime.fromisoformat(iso(concept['return_observed_utc']))-datetime.fromisoformat(iso(concept['invocation_start_utc']))).total_seconds();record=bind(R/'concept-generation.json');why='UTC pre-call to observed return, includes tool/orchestration latency; no throughput claim.'
            if stage=='modeling_export':status='measured';seconds=gen['wall_seconds'];record=bind(o/'build-timing.json');why='Blender geometry construction and export process only; excludes generator authoring, failed renderer retry and QA.'
            if stage=='proof_rendering':status='measured';seconds=manifest['wall_seconds'];record=bind(proof/'render-manifest.json');why='Successful final diagnostic render run only; failed copied-renderer attempt is separately retained.'
            if stage=='target_browser':status='not_run';why='Parent task owns independent runtime/GPU/populated-scene evidence.'
            timings.append(dict(stage=stage,status=status,wall_seconds=seconds,measurement_record=record,note=why))
        artifacts={key:bind(path) for key,path in {'glb':o/(slug+'.glb'),'source':o/(slug+'.blend'),'generator':generator,'config':d/'build-config.json','brief':d/'brief.json','references':d/'references.json'}.items()}
        sidecar=dict(schema_version=1,kind='concept_evidence',scope='provisional-study',asset_id=slug,revision='r001',labels={'en':metric['name']['en'],'zh-CN':metric['name']['zh']},artifacts=artifacts,concept=dict(provider='ImageGen',prompt=bind(R/'concept-prompt.txt'),generation_record=bind(R/'concept-generation.json'),images=[dict(id='original-sheet',view='four rows; paired aesthetic oblique and lateral proposals',**bind(R/'concept-original.png'))],cross_view_consistency_note=read(d/'brief.json')['concept_interpretation'],hidden_surface_decisions='Full volumetric bodies, closed thick feather/wing meshes and tapered closed limb tubes; underside and paired appendages deliberately authored. No concept image used as texture or plane.'),chronology=dict(concept_generated_at=iso(concept['return_observed_utc']),concept_inspected_at=iso(concept['pixel_inspection_observed_utc']),modeling_started_at=gen['started_at']),stage_timings=timings,coverage={'required_views':VIEWS,'turntable_frames':0},render_manifest=bind(proof/'render-manifest.json'),thumbnail=dict(**bind(proof/'hero.png'),source_frame_id='hero'),review_note=bind(d/'maker-review.md'),inspected_frames=VIEWS,khronos=dict(glb_sha256=metric['sha256']['glb'],report=bind(o/'gltf-validator.report.json'),warning_review=[]),budget=dict(target_glb_bytes=1000000,enforcement='advisory',rationale='Supporting scene-life candidate. Preserve recognizable volume and editable parts; no byte target establishes quality.'))
        save(d/'concept-evidence.json',sidecar)
        command=['python',str(REPO/'scripts/validate_concept_evidence.py'),str(d/'concept-evidence.json'),'--root',str(R),'--require-complete']
        result=subprocess.run(command,capture_output=True,text=True);(d/'concept-completeness.report.json').write_text(result.stdout);(d/'concept-completeness.stderr.log').write_text(result.stderr);assert result.returncode==0,(slug,result.stdout,result.stderr)
        handoff.append(dict(asset_id=slug,revision='r001',state='candidate_pending_independent_qa',artifacts=artifacts,metadata=bind(o/'metadata.json'),concept_evidence=bind(d/'concept-evidence.json'),proof=bind(proof/'render-manifest.json'),maker_review=bind(d/'maker-review.md'),triangles=metric['triangles'],glb_bytes=metric['glb_bytes'],dimensions_glb_xyz_m=metric['dimensions'],authored_vertices=structure['authored_vertices'],evaluated_vertices=structure['evaluated_vertices'],exported_position_accessor_vertices=qa['glb']['unique_position_accessor_vertices'],materials=qa['glb']['materials'],scene_primitives=qa['glb']['scene_primitives_estimated_base_draw_calls'],visible_instance_count=1,limits=limitations[slug],khronos_errors=validator['issues']['numErrors'],khronos_warnings=validator['issues']['numWarnings'],source_export=read(d/'source-export.report.json')['status'],roundtrip=roundtrip['status'],rebuilds=[bind(d/f'reproducibility-{n}.report.json') for n in [1,2]],mesh_structure=bind(d/'mesh-structure.report.json')))
    save(R/'handoff.json',dict(created_at=now,branch='candidate/small-land-air-quartet-main-20261019',base_main='4774ea94c864dca71dbe252fdd1c03230cc8c610',scope='Only four bounded candidates; production catalog/main and published count182 unchanged',maker={'model':'gpt-6.1-sol','reasoning_effort':'medium','source':'Parent delegated agent spawn configuration, user explicitly requested; distinct from undisclosed ImageGen model'},concept=bind(R/'concept-generation.json'),selection=bind(R/'evidence/remote-occupancy-scan.json'),assets=handoff,rejected_revision={'asset_id':'sapeornis','revision':'r002','reason':'Wider paddle-like outer tips did not show sufficient overall craft benefit; not adopted, no further iteration','path':'sapeornis/r002','matched_camera_provenance':'sapeornis/r002/matched-renderer-provenance.json'},pending=['Fresh independent visual/factual/specification review','Three.js parse, actual GPU and populated-scene validation','Final official posters from parent unified gallery renderer','Any approval/publication requires separate gate'],license={'assets_renders_prose':'CC-BY-4.0, Leon Made This / s010s','code':'MIT','references':'Consulted-only; cited third-party rights preserved'}))
    rows='\n'.join(f"| {x['asset_id']} | {x['revision']} | {x['triangles']} | {x['glb_bytes']} | {', '.join(f'{v:.6g}' for v in x['dimensions_glb_xyz_m'])} |" for x in handoff)
    (R/'HANDOFF.md').write_text(f'''# Four small land/air creature candidates

Branch `candidate/small-land-air-quartet-main-20261019`; base main `4774ea94c864dca71dbe252fdd1c03230cc8c610`. Candidate-only; no catalog or release count change. Maker gpt-6.1-sol / medium. Pin exact per-artifact hashes in handoff.json; git freeze SHA reported in the delivery message.

| ID | Revision | Triangles | GLB bytes | Actual GLB bbox X,Y,Z (m) |
|---|---|---:|---:|---|
{rows}

Dimension values are measured export bounds, including spread wings, tail or legs. `length_m` in build-config is a generator scalar, **not delivered total length or a scientific measurement**. Sapeornis uses flight body-center mount; others ground-center. Source semantic parts are closed separately and overlap intentionally; not a printable union.

298 refs / 269 unique SHAs scanned; selected inventory entries 678 sapeornis,681 longirostravis,831 dunbaria,828 chimerarachne had no occupied paths/claim/handoff. Excluded previously occupied taxa and historical evidence are in evidence/remote-occupancy-scan.json. Main published count remains182.

Real ImageGen original, exact prompt and available tool metadata retained. Generated return observed20:52:40 UTC; genuine view_image inspection completed/clock-recorded20:52:53 UTC, before frozen briefs and Blender construction. No ImageGen seed/model/call ID invented. Original generated image is aesthetic evidence, never a model poster or anatomical authority.

All four r001 files bind official Khronos0errors/0warnings, source-export reports, clean Blender import reports and **two separately executed queue rebuilds with successful semantic comparison**. Reimport warnings are retained and reviewed in maker-review.md plus actual position-weld boundary audit; do not describe all checks as warning-free. Eleven final exact-GLB diagnostic PNGs per asset were individually opened through view_image. Concept completeness validates internal evidence, not craft or scientific truth.

Sapeornis r001 remains visibly narrower/pointier in the outer wing than its concept. R002 widened ends become paddle-like under exact matched camera/light conditions, so R002 is retained **not adopted**. No visual acceptance/brief pass is claimed. Longirostravis, Dunbaria and Chimerarachne retain simplification/factual limits in their individual maker reviews.

Chimerarachne original common-renderer proof is unreviewably tiny at the0.025m minimum radius. `proof-macro-attempt02` lowers only the diagnostic minimum-radius floor; GLB bytes and real scale remain identical. Copies, source hashes, exact change notes, failed first-attempt logs and successful render configuration are retained. These are Blender diagnostics; parent must generate official posters through the unified gallery renderer. No promotional substitute images are included.

Independent QA, Three.js parse, actual GPU rendering and populated-scene acceptance remain pending parent task. This bundle does not claim independent QA, species-exact reconstruction, approval or publication.

Original assets/renders/prose CC BY4.0 — Leon Made This / s010s. Executable code MIT. Third-party sources consulted only, no imported geometry/material/image assets.
''')
    print(json.dumps({'assets':len(handoff),'status':'maker_bundle_complete_independent_qa_pending'},indent=2))

if __name__=='__main__':main()
