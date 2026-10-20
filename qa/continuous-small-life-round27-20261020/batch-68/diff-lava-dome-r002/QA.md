# Independent focused differential QA: lava-dome r002

**Disposition:** targeted r002 differential accepted for the specified generic lava-dome brief. This is not a publication/release approval and does not replace the repository's required platform approvals. No source, candidate, approval, CI, or release state was changed by this review.

## Target and immutable pins

- Branch `candidate/small-life-batch68-concept-20261020`, clean worktree, commit `f78e8081cf4d8336351547e57e217ae95b94ae22`.
- Active GLB: `assets/candidates/continuous-small-life-round27-20261020/batch-68/lava-dome/r002/model.glb`, SHA-256 `5e791acedfe0a8bfa24c4eac3817c70557b3b027e46e095833b976f5baae94c0` (154,772 bytes).
- Reopenable Blender source: `.../r002/source.blend`, SHA-256 `3ec5a122fbac32e2e30d2f6475699b695887c97b5a03521fbaa68e21a84122a2`.
- Bound brief SHA-256 `aa648adb6ea7426538b1a45639bc6b1f98496994ba657be63a5323558ae5474f`; reference ledger `1cd99cf0e05282e5b85c404ddb40e098a9050eb84b4d0ee0330d95f5e5a18a5b`; generator `aa665f1c1b52c9db31b9b6317174fd8eb56d924a045c98c2b2075a6e0f71845a`; config `2a8bba8089c7ae8ac1fd39e793768737e68791ce08eb3713b2bfc9bbef6b1877`.
- r002 supersedes r001 candidate record SHA-256 `56709a6f4e5d24f922488fadf4d3d8133c75d3da4f1fda0c673db8b6dc82ee38`. The original r001 asset/QA and the other three accepted assets are unchanged.

## Independent review and disposition

**Visual: pass.** I compared original concept and inspected the prior r001 hero/top views, actual consulted dome and rubble reference pixels (kept outside the repository), both preserved repair attempts, every one of the eight final 512×512 views individually, and the final contact sheet. r001 had a prominent circumferential block annulus around a broad smooth, uncovered summit. In final r002, unequal fracture plates continue across the summit and steep flanks; there is no exposed summit disc, horizontal mechanical belt, or tiled decorative ring. The overall silhouette reads as a broad, steep-sided, craterless dome rather than a cone or heap. Small fractured basal contact fragments are rooted/low and do not form a belt. Surface plates remain visibly stylized and somewhat polygonal, but the final variation is substantially less repetitive than the retained first diagnostic attempt and meets the brief's coarse irregular blocky rind. This is a generic teaching illustration, not a site-specific replica.

**Specification: pass.** Full frozen brief, concept, and unchanged source-reference ledger are bound to the final candidate. The immutable repair freeze was recorded before the render chronology and explicitly addressed summit/flank fracture coverage. The pre-proof binding names the final GLB before its eight-view manifest; the subsequent recorded pixel review names those exact images. Render settings preserve the r001 profile after normalizing expected bounding-box-adaptive camera/light scaling. No chronology conclusion depends on filesystem mtimes.

**Factual: bounded pass for a generic volcanic dome.** The form is consistent with the cited generic source on steep-sided, rough/blocky lava domes ([NPS: Volcanic Domes](https://www.nps.gov/articles/000/domes.htm)) and the consulted primary dome/rubble imagery. No named site, exact geology, hazard, or diagnostic field-identification claim is made. The references were consulted-only and are not embedded in the candidate/repository.

**Technical: pass.** Blender 4.3.2 independently reopened the exact source. A separate fresh export from its `EXPORT` collection was byte-identical to the pinned GLB; source SHA-256 was unchanged before/after. The source/GLB geometry and bounds agree within floating-point export tolerance. GLB is 2,632 triangles, 4 materials, 6 primitives, zero textures, and 154,772 bytes, within the stated <14,000-triangle, <1 MB, <6-material, <30-primitive limits. The two existing distinct final rebuild job receipts were independently checked for unique request/result identities, process/time evidence, and matching byte/semantic outputs; I did not repeat producer builds. Khronos validator 2.0.0-dev.3.10 reports zero errors and warnings. Three.js 0.180.0 `GLTFLoader.parseAsync` independently parses 2,632 triangles and six meshes/primitives.

**Runtime parse: pass. GPU: not run. Scene/browser composition: not run.** CPU parser and validator evidence does not demonstrate GPU rendering or composed-scene behavior.

## Evidence, completeness, and limits

- Candidate validation reports valid, but `approved_for_brief=false` and approval remains pending. This focused visual/specification disposition is a reviewer finding, not an approval-state change.
- Concept is valid and matches the original concept/tool-output hash, but `evidence_complete=false`: provider generation time and actual geometry-authoring start are unknown and remain unknown. Tool call/result observation times are recorded; they are not substituted for provider-internal timestamps.
- The committed-closure verification passed at the pinned HEAD: 67 active pins, 178 new tracked files including 32 tracked raw logs, and 351 protected prior full-tree files. Existing original r001 and other accepted asset histories remain preserved, including the failed/diagnostic dome attempts.
- This is only a focused lava-dome r002 differential; the other three batch assets were not re-reviewed here. No GPU/scene, user, formal release, upload, or publication approval is claimed.

## Evidence files

Machine-readable differential and exact frame/artifact pins: `independent-differential.json`.
CPU runtime checks: `independent-runtime.json` and `runtime-check.mjs`.
Committed-closure result: `committed-closure-verification.json`.
Fresh source reopen/export result and log: `source-export.json`, `source-export.log`, `source-reopened-export.json`, `reopen-export.log`; the fresh export is `source-reopened-export.glb`.
