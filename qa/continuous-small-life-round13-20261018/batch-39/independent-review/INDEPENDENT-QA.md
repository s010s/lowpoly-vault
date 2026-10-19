# Batch39 independent QA and Aa r002 differential

This report preserves the original one-round content/artifact review of `batch-39` and adds exactly one targeted differential re-review for `aa-lava-front` r002. The differential covers Aa r002 only; the other three original content decisions are preserved without new inspection.

- **Handoff source commit:** `0eed2d38d04f4b3d2b847eff8f376934769c0102`
- **Handoff:** `production/continuous-small-life-round13-20261018/work/batch-39/HANDOFF.md` (SHA-256 `0e301a7b5888f81aa2668f3ff2c1b0f47cc094b17d79b4f7dd26b043750c6cbc`)
- **Exact final handoff JSONL:** `production/continuous-small-life-round13-20261018/work/batch-39/final-handoff.jsonl` (SHA-256 `6e863c6c7b1d0cb46b6c96b8393d7f86c48019ac818fd214f9ba8afa03f05707`); pinned by `scope.json`.
- **Review checkout:** isolated worktree based on the handoff commit; the four candidate branches were checked out separately at their exact remote tips.
- **Profile compatibility:** `static-stylized-v1`, rule `2026-10-18.1`. Compatibility is not candidate approval.
- **Reviewer model identity:** not independently verifiable from runtime metadata. The parent request reports GPT-6 Luna xhigh; the targeted Aa follow-up was requested because r002 supplied new evidence, not because of that unverified identity.
- **Updated handoff:** commit `aac9a3c9085136469f816862b0c2a4139fc4eb3c`; `HANDOFF.md` SHA-256 `65fe582bb28a4e3a8dee3d7420c5bad2b01cab0aba299f74b94c8ae59a399b9b`, `final-handoff.jsonl` SHA-256 `0ec64f17bd638638aa6552bc65df487b4c8be786c7d2c01fbaca87afd5c9a1e6`, and `scope.json` SHA-256 `e93958cbd026bf2b125d2ffedf438f71126d780c7cc2a53a76964144c715c1cb`.

## Decision

**Batch content result: PASS for all four reviewed content items after the targeted Aa r002 differential.** The one original mandatory issue, B39-AA-01 on r001, is closed for r002. The Clavagella, copper and Nereites PASS decisions are carried forward from the original review and were not re-reviewed.

The initial four-item review and its artifact pins remain documented below and in `evidence/hashes/batch39-integrity.json`. For this update, the exact Aa r002 remote tip, hashes, reported rebuilds, and targeted Blender audit were checked. The candidate profile contract passes and the record remains `approved_for_brief=false`; formal candidate/profile acceptance remains blocked because required stages remain unknown/pending and hardware-GPU evidence is absent.

| Asset | Exact candidate branch tip | Blend SHA-256 | GLB SHA-256 | Triangles / GLB bytes | Content result |
|---|---|---|---|---:|---|
| clavagella | `candidate/batch39-clavagella-20261018` @ `9965f69214d8234921836885e27d45a51ac10481` | `df7099aaf0cfb96003c3fcbafc77e6ed5fffc69f30eb757c91fbe89697fb22a2` | `ba1afe1555b5d8d755cacd4ceab594973f579d4a05327ba71b805d57d7667367` | 9,956 / 186,684 | PASS |
| aa-lava-front | `candidate/batch39-aa-lava-front-r002-20261019` @ `1a65d88bd1fe81d0df3211b61235a150d71caa8d` | `1e14854740b6cd9260ce43fdc9caa6ca5270cf038d2be0ca7f5f8366c70ffe41` | `7960936e5ee17c46db8cd3d5658705ef04643a665ebfe5305e16a2bdefeb243c` | 1,646 / 92,640 | PASS — targeted differential |
| native-copper-dendrite | `candidate/batch39-native-copper-dendrite-20261018` @ `37a66698356bb847a34ad3fb772d1d828c06a87f` | `6e08c4af5c4ac513575ea31063fa61d035fa504e503649b73f8a8ddca471179a` | `bc7e051c9a04f93f9689359142bc673f73cb4944b325565fa523c3ea7a9491ad` | 1,800 / 95,044 | PASS |
| nereites-lobed-meander | `candidate/batch39-nereites-lobed-meander-20261018` @ `85b15327910c516aea001a42d4feaf51e775d3ed` | `31b9369d5c2f5a23d50dbc9f2738e30bcd964e77811a188f0d46b3fe6c61d1b1` | `691e88fe743aaf2e04f10bfc68c9fd961211004b0fc28d969ae33c68f20be442` | 8,620 / 165,560 | PASS |

## Per-asset findings

### Clavagella — PASS within the preserved shell/tube concept

The bulbous calcareous tube, integrated shallow valve relief, long narrowing neck, open rim/lumen, and small anterior tubules read as one shell structure across the fixed views. There is no living posture or unsupported soft tissue. The visible neck opening and low-relief valve remain understandable at the intended hand-scale prop size. The frozen name and generic fallback keep the claim bounded; this is not an exact species or specimen reconstruction.

The primary abstract for Morton & Grebneff describes an adventitious tube progressively enclosing a valve and an anterior array of tubules; its full text was not available in this review, so no more specific taxon, count, or dimensions are claimed ([article abstract](https://rsnz.onlinelibrary.wiley.com/doi/abs/10.1080/00288306.2011.537611)). No correction is required.

### Aa lava front — PASS for r002; B39-AA-01 closed

The r001 baseline finding was correct for that revision: the hero/front/side views showed a clean rectangular plate with vertical sides beneath the clinker. The targeted r002 comparison used the exact revised GLB and actual source-render plus runtime hero/front/side pixels. The straight-sided plate edge is gone; an irregular sloping core is recessed below unequal clinker, and an uneven rubble toe reaches the front. At the intended small child-viewing scale the form reads as a coherent low-poly flow-front mass. Remaining shadowed gaps between rocks do not create a rectangular tray silhouette, so no further mandatory correction is needed for this blocker.

The r002 Blend and GLB are pinned to candidate branch `candidate/batch39-aa-lava-front-r002-20261019` @ `1a65d88bd1fe81d0df3211b61235a150d71caa8d`. Their SHA-256 values are `1e14854740b6cd9260ce43fdc9caa6ca5270cf038d2be0ca7f5f8366c70ffe41` (Blend, 528,040 bytes) and `7960936e5ee17c46db8cd3d5658705ef04643a665ebfe5305e16a2bdefeb243c` (GLB, 92,640 bytes, 1,646 triangles). The checked source has two closed manifold meshes: a 560-triangle irregular sloping core and a 1,086-triangle clinker mesh. Blender 4.3.2 independently reopened the Blend and imported the exact GLB; triangle counts match and bounds match within `1e-4 m`. Source export reports zero bounds error and no warnings; Khronos reports zero errors/warnings. Both supplied semantic rebuild reports pass and resolve to the exact GLB hash.

The runtime report binds to that GLB and records seven views with zero WebGL errors. It uses Chromium 154.0.8037.57, Three.js 180, and ANGLE SwiftShader software WebGL; this is functional-render evidence only, not a hardware performance result. The focused image, report and audit pins are in `evidence/differential-aa-r002.json` and `evidence/blender/aa-lava-front-r002.json`.

The factual direction remains consistent with the NPS description of ʻaʻā as rough and jagged, with clinkery rubble moving down the flow front ([NPS field guide](https://www.nps.gov/crmo/learn/education/site-tour-1.htm)). This conclusion is limited to the targeted visual blocker.

### Native copper dendrite — PASS; terminal naturalness is not a mandatory fix

Branching sheets coalesce and taper with unequal widths; the gray/clay and top views preserve a dendritic mineral read. The form stays planar at approximately 15 cm span and 4.75 mm thickness, consistent with the cited “leaf” habit of dendritic native-copper aggregates flattened in one plane ([A.E. Seaman Mineral Museum, *Mineralogy of Michigan*, “Habits”](https://museum.mtu.edu/pdfs/COPPER.pdf)).

Terminal pads repeat a somewhat squared, flared rhythm. At the intended small, child-friendly low-poly scale, their silhouette is clear and the irregular differences are sufficient; this is an observation, not a repair request. Do not reopen the tips for microscopic realism. The very thin front/side projection is consistent with the intentionally planar aggregate.

### Nereites lobed meander — PASS within interpretive raised-relief scope

The neutral-gray top and oblique views show real raised relief on one sediment host: a meandering median axis with alternating, slightly offset lateral lobes that touch or overlap. The raised-relief presentation is labeled as an interpretive teaching layout; no trace-maker or exact excavated specimen is asserted. The repeated roundness is an economical stylization, not a missing structural feature.

This matches the narrow morphological points in the Kansas Geological Survey description: meandering traces, lateral ovate-to-lanceolate lobes that touch/partially overlap, alternating or slightly offset rows, a median backfilled tunnel, and positive hyporelief ([KGS systematic ichnology](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno2.html)). No correction is required.

## Checks and limits

- Read the exact handoff, final JSONL, source skills (`asset-factual-review`, `blender-lowpoly-pipeline`, `lowpoly-art-direction`), `static-stylized-v1` / `2026-10-18.1` compatibility note, and `.agents/skills` inventory. The `.agents` skills are animation-specific and do not govern these static assets.
- The original `batch39-integrity.json` audit covers the first review pins for all four r001 candidates. It remains the historical full-batch evidence; this differential did not rerun the whole audit or re-review the other assets.
- The original Blender 4.3.2 audits reopened each r001 Blend and imported its exact GLB. For this update, the same targeted audit script was run only on Aa r002: source and imported GLB triangle counts match at 1,646; bounds match within `1e-4 m`; root identity is present; source meshes have no boundary/nonmanifold edges, zero-area faces, or nonfinite normals. GLB reimport has split-normal boundary-edge counts, a documented possible artifact of flat-normal vertex splits. The r002 report is `evidence/blender/aa-lava-front-r002.json`.
- The original review visually checked all eight source views and seven runtime views per item. This differential visually checked the actual r001 and r002 hero/front/side source images and exact-GLB runtime images. Its r002 visual pass covers those three views only, with SHA-256 pins in `evidence/differential-aa-r002.json`. Runtime reports for both reviews use Chromium `154.0.8037.57`, Three.js `180`, and ANGLE SwiftShader software WebGL. They establish functional software rendering; hardware-GPU performance remains untested.
- The original review recorded source-export and two semantic rebuild passes for each r001 item. The targeted r002 handoff supplies passing source-export and two semantic rebuild reports bound to the exact GLB SHA; the targeted differential report records their pins.
- The original review recorded `static-stylized-v1` compatibility with `valid=true`, `approved_for_brief=false`, and `profile_contract_status=pass`. The updated Aa handoff reports the same contract compatibility while `approved_for_brief=false`. The legacy checker’s missing nonempty source-license text errors remain preserved; references are consulted-only and no third-party media or meshes are incorporated. No license was guessed.
- The updated final handoff has four rows; the three non-Aa JSONL rows compare byte-for-byte equal to the original. The r001 Aa candidate subtree also compares unchanged between the old and new candidate tips. The candidate record remains `approved_for_brief=false`. Only QA report/evidence files were edited here; no candidate model, threshold, CI, permissions, candidate record, publication state, or Drive content was changed. No merge was performed.

## Evidence paths

- `independent-review.json` — machine-readable decisions, exact source/candidate bindings, per-item hashes, and blockers.
- `evidence/hashes/batch39-integrity.json` — artifact-by-artifact, fixed-view, runtime, validator, source-export, rebuild, and profile-contract integrity checks.
- `evidence/blender/` — fresh source Blend and exact-GLB reopen/import audits.
- `evidence/differential-aa-r002.json` — the single targeted r002 delta, image hashes, report pins, and closure decision.
- `scripts/audit_blend.py` and `scripts/verify_batch39_evidence.py` — review commands/scripts.
- The initial fixed-view and runtime pixels remain in the original r001 candidate branches. The targeted Aa r002 source and runtime pixels remain in its pinned candidate branch under `assets/candidates/continuous-small-life-round13-20261018/batch-39/aa-lava-front/r002/{views,runtime}/`.
