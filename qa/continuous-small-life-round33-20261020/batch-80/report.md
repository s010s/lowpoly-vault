# Batch 80 independent static QA

Reviewed: 2026-10-20T18:15:40.881002+00:00

Pinned source: `42610ec62eeeddfb79ff24866b5840b012a9d729` (`candidate/small-life-batch80-concept-20261020`), clean worktree. SHA-256 and Git blob IDs rechecked for all 741 evidence entries (78,033,093 bytes). All six handoff hashes match for each candidate.

## Scope and integrity

This is bounded independent static QA, not formal acceptance, GPU/scene sign-off, user approval, or publication approval. The original frozen briefs were verified before recorded generator authoring and geometry build; provider internal timestamps remain unknown. Actual reference and concept pixels and source text were consulted.

All 32 final diagnostic images are genuine 512×512 PNGs bound to the exact final GLBs, candidate briefs and reference manifests; four 2048×1060 contact sheets were checked. The renderer explicitly applies a black emission material override for silhouette views on white, and the actual silhouette frames use it.

Fresh Blender 4.3.2 read-only reopen/export of each saved `.blend` reproduced its shipped GLB byte-for-byte and semantic digest. Fresh K0 static audit, Three.js r180 parse, Khronos Validator 2.0.0-dev.3.10 and independent decoded-GLB edge-incidence checks pass for all four. Every final GLB has one connected component and zero boundary/nonmanifold edges. Hash-bound maker physical reports also record zero nonadjacent triangle-intersection pairs; those intersection checks were cross-checked from evidence, not rerun by this reviewer.

Eight actual queued semantic rebuild runs were cross-checked, two per asset. Each has distinct PID/fingerprint, request/result files matching bindings, successful recorded exit and inputs with hashes matching actual current source; its rebuilt GLB is byte-identical and semantically equal to the final. Persisted records are evidence-consistent but are not cryptographic proof of execution.

## Candidate dispositions

### spriggina r003: PASS_STATIC_ONLY

Correctly treated as a shallow negative-hyporelief fossil mould informed by the actual N14-03 figure, not as a whole living animal. The thin irregular slab and central body impression are visible; the hero relief is subdued but clearer in top and reversehero views. No invented eyes, legs, antennae, mouth, or behavior.

GLB SHA-256 `c5f189656f3558c352c9413fadc7049a398e7ccf4bab1277e91722b1347cd5e2`; 12,672 triangles, 3 materials, 3 primitives, 954,412 bytes. Saved-source Blender re-export exact hash: True; Khronos 0 errors/0 warnings; fresh Three meshes/materials: 3 / edge, impression, sandstone.

### pediment r002: PASS_STATIC_ONLY

Broad, shallow near-bedrock erosional apron remains connected to the abrupt receding mountain front and occupies most of the model. It reads as a pediment rather than a radial depositional alluvial fan. Some mountain/apron transitions are deliberately sharp and stylized.

GLB SHA-256 `5acccae174dabafb01b6f253d09684821d467726d796f251f831ead2f8dad24a`; 3,180 triangles, 3 materials, 3 primitives, 233,424 bytes. Saved-source Blender re-export exact hash: True; Khronos 0 errors/0 warnings; fresh Three meshes/materials: 3 / bedrock, mountain, weathered.

### kame-mound r002: PASS_STATIC_ONLY

Irregular glaciofluvial sediment mound with a broad uneven crest, shorter offset shoulder and unequal flanks. The secondary shoulder is clearer in reverse/front/rear views than in the hero. Faceted gravel is a stylization, but the form does not read as a long streamlined drumlin, esker or volcanic cone.

GLB SHA-256 `f3877ca2efcca03a31e5b904c55c00675f64d9e58f0bc7736bcda93ac96dccf2`; 5,796 triangles, 3 materials, 3 primitives, 435,480 bytes. Saved-source Blender re-export exact hash: True; Khronos 0 errors/0 warnings; fresh Three meshes/materials: 3 / earth, gravel, sand.

### tuya r002: REVISE

Critical frozen feature “Dark jointed cap” is absent from the actual model: hero, top and front show an uninterrupted, uniform dark cap surface. The generator’s low-amplitude `joints` sine terms perturb radial ring radii on j=4..6 (z=300..349), i.e. near the rim/flank, not legible joints on the cap plane. This does not satisfy either the critical visual or factual criteria. Other broad flat-cap/steep-flank elements are present; missing cap joints alone is a clear REVISE blocker.

GLB SHA-256 `84c88e230f7fa437c8c41119ea181d0ccb3d7ddcbc2fe4f784ee95e50d44b2d3`; 1,728 triangles, 3 materials, 3 primitives, 133,380 bytes. Saved-source Blender re-export exact hash: True; Khronos 0 errors/0 warnings; fresh Three meshes/materials: 3 / basalt, breccia, tuff.

## Formal status and limits

The package candidate records remain `approved_for_brief: false`; formal visual, factual, specification, GPU and scene approvals are not granted. GPU and composed-scene rendering were not run. The independent static disposition above must not be represented as publication approval. Tuya requires a geometry/art revision to make cap jointing visibly satisfy the frozen brief.

## Primary references checked

- [Evans et al. 2026, Scientific Reports](https://www.nature.com/articles/s41598-026-53857-x), Fig. 2I and primary text on Spriggina N14-03.
- [National Park Service, Arid Landforms](https://www.nps.gov/subjects/geology/arid-landforms.htm) and [USGS, Lake Mead eroding pediment](https://www.usgs.gov/media/images/lake-mead-eroding-pediment).
- [Wisconsin DNR, Johnson Hill Kame](https://dnr.wisconsin.gov/topic/statenaturalareas/JohnsonHillKame) and [Iowa DNR, Ocheyedan Mound](https://www.iowadnr.gov/places-go/state-preserves/ocheyedan-mound-state-preserve).
- [USGS, Hoare (1978), A Tuya in Togiak Valley](https://www.usgs.gov/publications/a-tuya-togiak-valley-southwest-alaska) and [USGS, Moore et al. (1995)](https://www.usgs.gov/publications/tholeiitic-alkalic-transition-subglacial-volcanoes-tuya-region-british-columbia-canada).

Detailed machine-readable checks and owned artifact hashes are listed in the companion files in this QA directory. `owned_outputs.json` lists only QA-created files, excluding itself to avoid a recursive self-hash; it excludes source/reference copies and dependencies.
