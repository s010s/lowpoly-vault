# Batch 03 — independent review handoff

Dispatch a fresh **GPT-6 Luna xhigh** review. This maker task has not run or claimed independent QA, accepted any candidate, merged main, or published assets. Use this branch's final commit and `result.json` to lock exact artifact identities. Historical checkpoint records and Onoclea r001 are not the current review candidate.

## Exact review inputs

All paths below are repository relative. Prefix is `production/continuous-small-life-20261018/`.

| Inventory ID | Frozen execution bundle | Actual editable/source bundle |
|---|---|---|
| cephalaspis | `work/batch-03/cephalaspis/r001/` | `assets/candidates/continuous-small-life-20261018/batch-03/cephalaspis/r001/cephalaspis/` |
| saccocoma | `work/batch-03/saccocoma/r001/` | `assets/candidates/continuous-small-life-20261018/batch-03/saccocoma/r001/saccocoma/` |
| archaeocidaris | `work/batch-03/archaeocidaris/r001/` | `assets/candidates/continuous-small-life-20261018/batch-03/archaeocidaris/r001/archaeocidaris/` |
| onoclea | `work/batch-03/onoclea/r002/` | `assets/candidates/continuous-small-life-20261018/batch-03/onoclea/r002/onoclea/` |

Start with `items/<id>/brief.json`, its original `build-config.json`, `work/batch-03/<id>/<revision>/references-execution.json`, `execution-config.json`, `freeze.json`, `candidate.json`, and the exact GLB. The expanded reference ledger distinguishes new web access from inherited notes and from original image bytes that could not be downloaded in the shell (HTTP403). No external image/scan/model/texture is bundled or incorporated. Sources support basic inspired form, not a strict reconstruction, microscopic anatomy or exact fossil measurements. Onoclea uses a modern botanical analogue; historical chapter details were not newly reverified.

## Image evidence

Prefix: `qa/continuous-small-life-20261018/batch-03/`.

- `<id>-exact-contact.png`: navigation sheet of eight actual imported-GLB Cycles views.
- `<id>/exact-glb/preview-{hero,reversehero,front,side,rear,top,clay,silhouette}.png`: actual pixels; open required originals as needed. All except 128px silhouette are 512px at 8 samples; hero and other color views retain alpha. Rendering preset and per-frame hashes/dimensions are in the manifest.
- `<id>-runtime-contact.png`: seven 360px-envelope exact-GLB browser angles, normal 80/160/240px envelopes and two nine-copy scenes.
- `browser/<id>-*.png`: original 640px browser screenshots. `browser/<id>.json` and `<id>-scene.json` identify exact GLB, pinned Three.js, device, bounds, materials, calls, triangles, instances, console/network outcomes.
- `<id>-view-manifest.json`: current exact GLB and all image hashes.

Functional graphics evidence uses **SwiftShader software WebGL2**, never physical-device FPS. Each benchmark has nine copies of one asset at the authored meter scale, plus one simple floor (2 triangles); no museum integration or historical coexistence is claimed. Tiny subjects need close placement. Fine detail disappearance at 80px is not itself a strict reconstruction failure; judge required basic shape and the stated envelope.

## Review scope

Return criterion-level findings tied to the brief, a specific view and the exact GLB SHA256. Independently judge visual craft, basic form, honest labels and specification. Keep technical/runtime evidence separate. Do not treat the maker's integrity PASS or file counts as an aesthetic/factual verdict. The maker supplies no numerical beauty score or expected independent decision.

Read `REFERENCE-GATES.md`: rounded test and organized long spines; tiny stemless cup and open branched arms; broad swept-corner shield and high-set eyes; broad sterile and beaded fertile fronds on one rhizome. Color, pose, nominal dimensions, exact plate/spine counts, lateral flange cross-sections and uncertain fine reconstruction remain artistic/advisory. Use one consolidated review and at most one planned cosmetic repair; return persistent required defects to the coordinator for scope decisions.

## Actual technical commands/results

- `node scripts/validate_gltf.cjs <exact asset directory>`: all four GLBs, zero errors and warnings.
- `python production/continuous-small-life-20261018/work/batch-03/verify_builds.py`: already executed. Source reopened with autoexec disabled, bounds/triangles matched; two distinct Blender builds per asset matched semantic digests and exact GLB bytes. Immutable command/log/hash records are under `<id>/verification/`.
- `blender -b -t 2 --disable-autoexec --python-exit-code 1 --python production/continuous-small-life-20261018/work/batch-03/source_metrics.py`: editable/evaluated counts, identity root, meter units, zero preview objects/cameras/lights.
- `python scripts/test_qa_glb.py -v`: 14 tests, OK; retained regression output.
- `python production/continuous-small-life-20261018/work/batch-03/validate_bundle.py`: current practical-profile integrity PASS, **independent QA remains pending**.

The historical `validate_candidate.py` approval schema does not implement this authorized zero-turntable profile. It is not reported as passed, and no fake turntable or independent verdict was generated. `validate_bundle.py` is a current integrity check, not a replacement independent reviewer.

To reproduce browser evidence, serve the repository on port8765 (`python -m http.server 8765 --bind 127.0.0.1`) and run `node production/continuous-small-life-20261018/work/batch-03/browser_qa.mjs cephalaspis saccocoma archaeocidaris onoclea` with installed locked dependencies and `/usr/bin/chromium`. Run in a disposable checkout/evidence directory if preserving the original screenshots.

Parent owns atomic queue state, independent QA dispatch, serialized merge/release and any publication. This branch changes no CI, global site logic, release manifests or other batches' assets.
