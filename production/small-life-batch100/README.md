# Batch 100 original low-poly candidates

Final revisions: lygodium r003, flabellophyton r001, protosalvinia r003, chaetocladus r001. These are candidates, not independently accepted or published assets.

Read handoff.json for exact artifact hashes, actual authored/evaluated/exported counts, transformed dimensions and two distinct queued rebuild PIDs per asset. The immutable original pre-model freeze and unmodified inventory remain present. Scope clarifications precede geometry. Lygodium is an isolated foliage organ; Chaetocladus is Ordovician C. plumula rather than the inventory's generic Silurian planning label.

Each final folder contains editable Blender source, standalone GLB, deterministic config/seed, eight real 512px single views and a lossless contact sheet. Repository helpers and external read-only package versions are pinned. CPU stills and Three.js parsing do not establish GPU or composed-scene performance.

Revision history preserves genuine failed geometry and pixels locally. Lygodium's non-parent lamina burial was corrected in geometry and verified with all-other-component exposure plus actual individual images. Protosalvinia's radial mesh artifact and notch fold were removed in geometry. No frozen limits were loosened and no material or camera was used to hide those defects. The common renderer's absolute size floor was removed transparently so millimeter-scale specimens are properly framed.

Primary reference photographs, articles and historical drawings are consultation only and remain outside this Git payload. No consulted raster or existing mesh is incorporated as a final texture or geometry. Concepts are genuine ImageGen planning, not scientific evidence.

## Rebuild

Use Blender 4.3.2 and the pinned repository helpers listed in each candidate's dependency manifest. Run the generator with --config and a fresh --output after the Blender -- separator. Every Blender process must use blocking /usr/bin/flock /tmp/lowpoly-production-blender.lock /usr/bin/blender --background --threads 2 --factory-startup --python-exit-code 1 --python ... . No installation, full checkout or website build is required.

Seven stages remain separate. Technical and runtime_parse pass; visual, factual and specification await fresh independent review; gpu and scene are unknown, not run. No release authority is implied.
