from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('/workspace/lowpoly-vault'); W=R/'production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn'; A=R/'assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r001'
def save(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
config={'asset_id':'cave-popcorn','seed':5203,'nominal_art_dimensions_blender_xyz_m':[0.55,0.40,0.26],'radial_steps':34,'angular_steps':96,'palette':['#AA9471','#DCC59D','#EFE0BC'],'texture_free':True}
save(A/'build-config.json',config)
refs={'schema_version':1,'no_incorporated_third_party_assets':True,'sources':[{'id':'EN-SP2','title':'Wind Cave formations — Cave Popcorn','url':'https://www.nps.gov/wica/learn/nature/cave-formations-speleothems.htm','supports':'Small knobby calcite growths on cave walls, floor or ledges; generic form only.','verification':'opened','access_observed_at':'2026-10-20T00:09:00Z','access_time_note':'Minute precision observation; exact tool start time unrecorded.','license':'Consulted-only; no media incorporated and no redistribution rights asserted.','use':'consulted-only','rights_note':'Original geometry and palette; no named locality, period, precise dimensions or age asserted.'}]}
# Source page tool-access exact time was not provided; do not fabricate it.
refs['sources'][0]['access_observed_at']=None
save(A/'references.json',refs)
brief=json.loads((R/'schemas/templates/brief.template.json').read_text()); brief.update(asset_id='cave-popcorn',brief_version='r001',purpose='Original concept-first generic cave popcorn mineral prop; independent review pending.',required_views=['hero','reversehero','front','side','rear','top','clay','silhouette'],turntable_frames=0,geometry_policy={'max_triangles':14000,'max_materials':6,'max_primitives':30,'max_glb_bytes':1000000},texture_policy={'max_textures':0,'max_dimension':0,'max_total_bytes':0,'max_decoded_bytes':0},required_deliverables=[],coverage_justification='Fixed8 static-stylized-v1 dispatch, rule 2026-10-18.1; exact front -Y, side +X, rear +Y and top +Z plus hero/reversehero/clay/silhouette.',nominal_art_dimensions_blender_xyz_m=[0.55,0.40,0.26],nominal_art_dimensions_gltf_xyz_m=[0.55,0.26,0.40],dimension_claim='Invented nominal art scale, not measured specimen dimensions.')
for c in brief['criteria']:c['required_sources']=['EN-SP2'] if c['stage'] in ['visual','factual'] else []
save(A/'brief.json',brief)
(A/'brief.md').write_text('''# Cave popcorn — r001 frozen concept interpretation

English: Cave popcorn. 中文：洞穴葡萄状结核。 Generic geological form; static supporting museum prop viewed around 1–3 m. Not a specimen reconstruction.

Nominal art dimensions: Blender X width 0.55 m, Y depth 0.40 m, Z height 0.26 m; glTF XYZ 0.55 × 0.26 × 0.40 m. These are invented display dimensions. Actual measured bounds will be reported separately. Origin at floor contact center; Blender Z up / -Y front; glTF Y up / +Z front. Target runtime is the repository viewer; runtime/GPU/populated scene are separate unrun stages.

Genuine ImageGen original was generated before geometry and actually inspected at the recorded tool-observation time. The three panels show a broad irregular slab, a pale knobby crust and a taller rear-right mound, with a quiet exposed front-left corner. Panel nodule counts and small creases differ; these are suggestions, not orthographic measurements. Retain the shared mass hierarchy rather than copy inconsistent individual balls. The concept is more spherical than the dispatch requires: explicitly fuse all nodules and their necks into one closed continuous mineral surface. No discrete loose sphere meshes. Model underside as a plain closed resting plane, sides as coarse limestone facets, and rear as continuous lower mineral shoulders. No hidden anatomy is claimed.

Construction: deterministic polar triangulated closed height surface, with smooth unions of original elliptical nodule caps and low mineral mounds. One manifold mesh with editable vertices and material regions; continuous base and mineral necks are geometric. Seed 5203. Ivory crust, warm calcite shadow and ochre limestone, flat facets, opaque Principled materials, no textures. No coral branches, crystals, negative relief or loose pebbles.

Budgets: 14,000 triangles / 1,000,000 GLB bytes / 6 materials / 30 primitives, texture-free. Spend triangles on rounded nodule profile and fused saddles, not microtexture. Blender 4.3.2; shared asset_common export flags. Preserve source, generator/config, exact exported GLB, eight fixed views including clay and silhouette. Thumbnail uses exact hero frame. Check source reopen, two semantic rebuilds, static audit, Khronos, candidate and supplemental integrity. Formal visual/factual/specification approval is independent and pending. No browser/GPU/scene result inferred from CPU proof renders.

Reference: NPS Wind Cave page opened through web tool, text supports small knobby calcite growths. Facts consulted only. No source media incorporated. Precise age, locality, scale, individual nodule counts and palette are not factual claims. Concept original is separately retained and never used as a final thumbnail.

Remaining concept differences: authored continuous height surface reduces isolated spherical lobes and omits tiny granular texture. Frozen eight proof views use repository camera/light/color management; hero and alternate views must be inspected after exact GLB import. Stage wall timings not explicitly measured stay unrecorded. Provider-generated timestamp unknown; tool receipt and actual inspection observation remain distinct.

Original assets/renders/prose: CC BY 4.0, Leon Made This / s010s. Code: MIT.
''')
freeze={'kind':'derived-modeling-freeze','asset_id':'cave-popcorn','revision':'r001','task_id':'/root/cave_popcorn','thread_id':None,'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'provider_generated_at':None,'tool_result_received_observed_at':'2026-10-20T00:10:09Z','concept_inspected_observed_at':'2026-10-20T00:10:09Z','modeling_started_at':None,'files':{str(p.relative_to(R)):h(p) for p in [W/'concepts/original.png',W/'concepts/prompt.txt',W/'concepts/generation-record.json',A/'brief.json',A/'brief.md',A/'references.json',A/'build-config.json']}}
save(W/'modeling-freeze.json',freeze)
for p in (W/'concepts').iterdir():shutil.copy2(p,A/p.name)
