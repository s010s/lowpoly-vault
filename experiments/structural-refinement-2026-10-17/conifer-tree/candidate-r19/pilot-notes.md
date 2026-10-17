# r19 complete tree — user-selected airy A, pilot review pending

The user explicitly chose A from the actual r18 same-camera style comparison. This means separated narrow needles, feather-like sprays and a light open crown. **No B connected opaque core surface is present.** Natural sparsity and clear sky windows are intended. User choice is a style direction, not approval of defects, performance or publication.

## Exact candidate

GLB SHA-256:`e912444734c357017d3b839c0ba009dfc994d0e57acdb8d1d1a4fe431c0357c8`.

- **19,052 exported triangles;834,840 raw GLB bytes;3 used materials/3 primitives;zero textures.**
- 25,325 authored/evaluated source vertices;29,882 exported POSITION-stream vertices.
- Original r12 main wood:1,525 vertices /2,914 triangles, exact vertex and polygon prefix preserved. `woody-source.json` is a portable immutable geometry/group snapshot captured directly from r12 without saving or changing that source.
- Frozen r17 A constructor:`b88dfe9f8f0e1538ef1c6964f1df501b4de743cb12f7b11820ff327b6dddfb40`, directly verified before construction. The source is copied exactly into the self-contained r19 generator; leaf widths, counts, curvature and terminals were not retuned.
- 149 sprays ×106 triangles =15,794 foliage triangles.106 lower sprays use paired nearby attachments with modest up/down pitch;43 upper sprays inherit the r18 arrangement, including its8 additional sprays. Natural irregular spaces and the broken lower branch are retained.
- Only43 upper sprays receive tiny fine wood supports:344 separately counted triangles. Lower sprays retain the thin green rachis. Total:2,914 +15,794 +344 =19,052.
- Relative to r12 actual:346 more triangles (+1.85%),369,056 more raw bytes (+79.23%). More separate leaf vertices explain much of the cost difference; this is not a performance pass. Original asset remains2,382 triangles /145,732 bytes.

## Exact pilot pixels

`comparisons/four-hero512.png`: azimuth35/125/215/305°, elevation20°, each original512px.

`comparisons/detail-color-clay512.png`: matched middle-crown detail and gray detail, original512px cells. `evidence/pilot512/clay.png` retains whole-tree clay. Same historical framing, camera, lights, exposure and color transform; no paint-over or beautification.

`comparisons/native128-views.png`: four hero directions, four horizontal cardinals and silhouette, each cell exactly128px without enlargement. All16 individual raw PNGs and exact-GLB manifests are retained under `evidence/`.

The maker has inspected the contact sheets and detail pixels without approving art. Sprays remain narrow and feather-like; at128px, fine strands naturally diminish into lines. The full outline, primary bough rhythm, relative foliage organization, contacts, normals and distracting crossings still need independent judgment. Do not reinstate an opaque connected-mass requirement after the user selected A; equally, do not treat that choice as a waiver for broken joins, unreadable whole-tree structure, toy-like hard blades or bad runtime behavior.

## Gate status and handoff

Current status is **pilot-first, pending independent A-style review**. Parent coordinates that review. Static/source build audits have zero errors and explicit intentional thin-surface/smoothing warnings. No independent acceptance or official full-format validation is claimed by those build checks.

After pilot review, complete the required full-angle freeze/hash checks, saved source/export comparison, official validator, independent-process rebuild, exact Three.js renderer/GPU and1/16/32-clone composed-scene gates, followed by independent final acceptance. CPU Blender previews are actual GLB reimports, not proof of target WebGL appearance or performance. `candidate.json` keeps all seven production stages unknown. No main, already released fern/arch, website or publication manifest was changed.

`pilot-handoff.json` binds subject hashes, the16 raw PNGs, known limits and next gate. `build-attempt-01/build-measurements.json` records every spray attachment, direction, cluster, support and count. Source generator requires its adjacent `woody-source.json`, `build-config.json`, and the existing repository `scripts/asset_common.py` helper. Blender5.2.0LTS local macOS, one worker/two threads,180-second per-process timeout. All invoked build/render jobs returned normally; no duplicate workers were launched.

## Reproduce a fresh build

Use the existing authorized bounded runner pattern with:

    Blender -b -t 2 --factory-startup --python-exit-code 1 --python build_airy_conifer.py -- --output-dir NEW_EMPTY_DIRECTORY --config build-config.json

Do not overwrite a frozen build or reuse a filled output directory. Record actual Blender/helper/exporter versions and hashes for the later reproducibility gate.

## Reference and license

Modern foliage analogue only: NC State Extension's Metasequoia Leaves/Quick ID sections and its consulted Francois Gulbert foliage photograph, https://plants.ces.ncsu.edu/plants/metasequoia-glyptostroboides/ ; Earle Description, https://www.conifers.org/cu/Metasequoia.php . Source ledger remains `references.json`. No external pixels, meshes or textures are incorporated; exact grouping, crown layout, palette and seven-meter scale are artistic choices, not an extinct-species reconstruction.

Original code MIT; source blend, geometry, renders and documentation CC-BY-4.0, Leon Made This /s010s.
