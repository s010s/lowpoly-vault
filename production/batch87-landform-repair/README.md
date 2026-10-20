# Batch87 two-landform local repair handoff

Selected: spatter-cone r006 and travertine-terrace-pools r003. See maker-handoff.json for exact hashes, actual geometry measurements, provenance and remaining stages.

Original batch87 inventory, concepts, frozen briefs/configs and independent QA remain unchanged in the base commit. The original r004/r002 specification BLOCKED decisions are not retroactively accepted. Measurement-clarification-v002 was fixed prospectively before new geometry, with no art tolerance. Independent clarification is retained byte-for-byte. Pleuromeia and glacier-crevasse-field were not modified.

Spatter r005 smooth-funnel diagnostic is preserved locally and in its disposition record. The selected r006 uses real staggered fused surface welts, 64 construction rays and 14 intervals / 15 original stations, with 8 exterior midpoint tessellations. The actual 64 crest vertices average 2.5 m, maximum 2.8 m, average horizontal opening radius 0.65 m; actual central floor is 0.18 m. Final complete envelope is 7.8 x 7.4 x 2.8 m within float32 serialization only.

Travertine r003 retains five planar floors and four 0.7 m rises, with nominal primary lip contribution 0.18 m. Actual outer envelope is 10 x 18 x 4.7 m. Top surfaces were translated upward before solid sidewall/bottom construction, with bottom at zero; Z was not scaled. Actual complete source and final GLB local measurements, including 290 lip samples, are retained.

Editable Blend and standalone GLB, exact generator/config/helper dependencies, actual source reopen and final binary measurements, two real queued separate-PID rebuilds per asset, official Khronos and Three.js parsing, eight exact final512px views plus a separate supplemental bottom and lossless sheet are complete. Both selected candidates pass integrity validation, not independent artistic acceptance. All18 individual final images were inspected. A failed metadata-only check was preserved and corrected with an explicit schema adapter; final subjects and pixels were not changed.

Rebuild with Blender4.3.2 using a blocking shared flock and --threads2. Invoke tools/generate-spatter-r006.py for spatter r006, or tools/generate.py for travertine r003, with --config pointing to its exact config and --output pointing to a new empty directory. Original generator is also retained for rejected r005. Dependencies are pinned in dependencies.json; no installation or full site build is needed. Proofs are rendered from final GLBs, not from an unsaved authoring scene.

Fresh independent visual/factual/specification review is pending. GPU and composed-scene stages are unknown/unrun. Nothing was uploaded, pushed, published or released. Raw failed/incomplete/successful process records and consulted reference pixels remain local; no consulted copyrighted pixels are added to Git.

Code MIT; original geometry, concepts, renders and writing CC BY4.0, Leon Made This / s010s. External references consulted only, not incorporated.
