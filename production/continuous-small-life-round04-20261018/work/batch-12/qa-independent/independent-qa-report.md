# Batch 12 — independent QA

## Result

**PASS for all four assigned candidates. No asset-level must-fix was found.** This is an independent review of the frozen deliverables; it does not update the source candidate’s formal stages, approval, publication policy, or shared state.

The reviewed source is `candidate/small-life-batch12-20261018` at **`b7a0582edbaa4e6cdea0f04524c6c59166987e56`**, based on main **`0bd62cda92814af5ac781e1a706bba6310cecc35`**. I applied the current `static-stylized-v1` rules (`2026-10-18.1`) and the frozen brief’s eight fixed views / zero-turntable contract. The source tree contains `HANDOFF.md` and `HANDOFF.json`; there is no file named `handoff-hashes.json`. `HANDOFF.json` (SHA-256 `2d19aa29e906d9fbc57a56887c34c752ad270ec046fcb7c4265602bc047952a8`) supplies the per-asset pins.

## Pinned assets and findings

`checkpoint` is the per-asset frozen candidate commit. SHA-256 values below were recomputed from the exact source snapshot and match its handoff pins.

### cystiphyllum — PASS

- Checkpoint: `9238f3015850f797ae4e69a2adddbd15b6797f04`
- GLB: **149,860 bytes; 8,064 triangles**; SHA-256 `0e8239998b510334a1e6743adf82de0fabc4c3f557b3ca8b43d6fa0f9b049dbf`
- Blend SHA-256: `3dc70e1b1850d5c71248fb50e2782f59a224765525426a089a3911ea36f52ab8`
- Independent Blender reopen found one connected export component, identity root, positive transform determinant, no camera/light objects, and 8,064 evaluated triangles. The current main source/export audit matched GLB triangle count and bounds exactly. Khronos: 0 errors / 0 warnings.
- Visually, the inflated curved solitary cup, broad shallow opening, and restrained blister-like floor relief read clearly from top and hero views. The smooth shading warning from the source/export checker was reviewed in the images and is intentional; no missing face or apparent intersection found.

### limnobiophyllum — PASS

- Checkpoint: `792ed38f8cd3fc395628a79ed7506c3d5dcde972`
- GLB: **153,672 bytes; 8,166 triangles**; SHA-256 `f6d5b1ddb3653bc44550a8c064184ab1a4d07c99929cde6f03f7037af461addb`
- Blend SHA-256: `ab1dd742bc0615508c3e5076de175b17599b4d4d363fb6f02cadb5757319fd2e`
- Blender reopen found 4,177 evaluated vertices, positive transform determinants, and no camera/light objects. Source/export triangles and bounds matched exactly. Khronos: 0 / 0.
- The stolon-linked leaf rosettes and hanging roots remain distinct in hero, top, side, and 160–240 px views. The checker reports lowest glTF Y `-0.040036 m`; this matches the explicit `Z=0` waterline mount with roots below it, not a displaced ground-bottom model. No apparent break or intersection found.

### wielandiella — PASS

- Checkpoint: `12a77488eb64b9d6bf1b9cc3f84c8854400af0c9`
- GLB: **107,508 bytes; 5,196 triangles**; SHA-256 `0fc748d918fe67228621f8a02c01b4791c2a04352aed594062cd6e6df82456ae`
- Blend SHA-256: `0556028342797c223ec2e8b79ec6aa138032d56e0117f58056657366028490ff`
- Blender reopen found 3,008 evaluated vertices, positive transform determinants, and no camera/light objects. Source/export triangles matched; maximum bounds error was `4.773028194904327e-09 m`. Khronos: 0 / 0.
- The continuous trunk and open forked shrub form read from all reviewed sides. Small terminal foliage is sparse at the 80 px check but the silhouette remains legible and the leaves read at 160–240 px. This matches the brief’s branch-first, vegetative-only direction; no apparent break or intersection found.

### desiccation-crack-surface — PASS

- Checkpoint: `196f2603de1ea7a4f2fcd3fd4d734e24ba118ef6`
- GLB: **85,208 bytes; 4,476 triangles**; SHA-256 `c46336a7c5a88faadd79ed89d664968649d6a28116f821c0bae77edc0c993571`
- Blend SHA-256: `01da9a048db913b5bcb2a0d0b108b95ebd48530bb41c67e3bb3272677baa36b0`
- Blender reopen found 2,276 evaluated vertices, positive transform determinants, and no camera/light objects. Source/export triangles and bounds matched exactly. Khronos: 0 / 0.
- The top view shows interlocking polygonal plates and tapering real geometry cracks, with modest raised edges. It is below the brief’s usual 100–500 KB range by design, while remaining well under hard limits; no padding is warranted. No apparent top-face gap or intersection found.

## Cross-asset checks

- Independently recomputed GLB, Blend, candidate, freeze, generator, config, source-sheet, runtime-sheet, and view-manifest hashes against the handoff. Each pin matched; the GLB copies used for QA also matched the delivered bytes.
- `scripts/qa_glb.py` on all four GLBs: within the frozen 14,000-triangle / 6-material / 30-primitive ceilings. No external buffers, textures, or non-finite geometry. The only baseline warning is Limnobiophyllum’s documented waterline/root offset.
- Reopened each exact Blend with Blender 4.3.2 and ran the current-main source/export comparison. The source and GLB triangle counts match for all four; bounds match exactly except Wielandiella’s sub-nanometer floating-point delta noted above.
- Khronos glTF Validator `2.0.0-dev.3.10`: all four exact GLBs have **0 errors and 0 warnings**.
- Re-ran current-main `validate_candidate.py --profile static-stylized-v1` with each frozen profile contract: all return `valid: true` and `profile_contract_status: pass`. The original candidate still reports `approved_for_brief: false`, stage outcomes unknown, and approval pending. The legacy profile remains invalid only for absent source-license text; the consulted references are not treated as incorporated media or as proof of media rights. No candidate record or policy was edited.
- Compared overall finish to the accepted small-fauna trio v2 examples: restrained natural colors, readable silhouettes, and detail concentrated at useful viewing sizes are consistent with that direction. Nothing here needs species-level micro-detail or another subjective polish loop.

### Factual claim boundaries

The briefs expressly call these teaching art / concept props, not strict scientific reconstructions. Claims stay within the available support: the Digital Atlas describes solitary and colonial rugose-coral forms at group level, not a precise `Cystiphyllum` restoration; the Limnobiophyllum paper describes a floating aquatic angiosperm with rosettes, stolons, and roots; the Wielandiella revision supports a shrub-sized bennettite with branched axes bearing leaves; and the BGS memoir associates desiccation cracks with intermittent exposure. I found no visual label or brief claim that overstates those sources.

- [Digital Atlas of Ancient Life — Rugose corals](https://www.digitalatlasofancientlife.org/learn/cnidaria/anthozoa/rugosa/)
- [Stockey & Rothwell — *The fossil monocot Limnobiophyllum scutatum*](https://bsapubs.onlinelibrary.wiley.com/doi/pdf/10.2307/2446009)
- [Pott — *A Revision of Wielandiella angustifolia*](https://www.journals.uchicago.edu/doi/10.1086/675577)
- [British Geological Survey — Church Stretton memoir](https://webapps.bgs.ac.uk/Memoirs/docs/B01602.html)

## Non-blocking observations and remaining planning limitation

- The exact runtime sheet renders the crack slab’s underside very dark / near black. The top and hero views are clear, and Blender inspection confirms the continuous base is present. This is not a missing-face finding; if the underside is expected to be a common product view, optionally review its material or lighting.
- The round04 checksum file verifies **69 / 69** frozen planning files. The broader `verify_plan.py` cannot complete its cross-round queue check: this snapshot has only the round04 queue, and the script stops on missing `production/continuous-small-life-20261018/queue.json`. The four assigned candidate packages and their handoff-pinned deliverables are present, so this is a planning-history verification gap, not an asset-delivery failure. Parent should resolve any cross-round assignment question from the authoritative shared planning state before integrating the batch.
- Publication authority is separate from this QA result. No assets, thresholds, permissions, CI, candidate stages, or publication policy were changed.

## Evidence

The `evidence/` folder contains the recomputed pins, current-main audit reports, command/output logs, and checksum-preserved source/runtime sheets. Each runtime sheet is pinned to its selected GLB in the source handoff and includes seven fixed single-instance views, 80/160/240 px checks, and two six-instance scenes.

- [Cystiphyllum source views](evidence/images/cystiphyllum-source.jpg) · [exact GLB runtime views](evidence/images/cystiphyllum-runtime.jpg)
- [Limnobiophyllum source views](evidence/images/limnobiophyllum-source.jpg) · [exact GLB runtime views](evidence/images/limnobiophyllum-runtime.jpg)
- [Wielandiella source views](evidence/images/wielandiella-source.jpg) · [exact GLB runtime views](evidence/images/wielandiella-runtime.jpg)
- [Desiccation crack surface source views](evidence/images/desiccation-crack-surface-source.jpg) · [exact GLB runtime views](evidence/images/desiccation-crack-surface-runtime.jpg)
- [Exact commands](evidence/logs/commands.log) · [hash audit](evidence/reports/hash-audit.json) · [full Khronos reports](evidence/reports/)
