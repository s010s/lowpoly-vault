# Batch 04 independent QA review

**Decision:** all four exact candidates pass the current frozen, stylized low-poly brief. No model repair is required. This review is bound to candidate source commit `abc24f3289df8ccce4ef6fd29c1edb1eeec8253a`; it does not alter the candidate records, models, thresholds, CI, or release state.

**Reviewer:** Codex independent QA, task `01a1187a-1f8d-746a-8448-61f8cb38d0fc`

**Scope:** `production/continuous-small-life-round02-20261018/items/<id>/brief.json`, reference ledgers, final attempt sources and GLBs, eight-view GLB manifests, exact-GLB Three.js captures, and the 12-instance metric-scale scene.

## Per-asset verdicts

| Asset / attempt | Decision | Exact GLB SHA-256 | Editable source `.blend` SHA-256 | Bytes / triangles | Measured glTF bounds (X × Y × Z, m) |
|---|---|---|---|---:|---|
| calceola / attempt-03 | **PASS** | `13ed3091c6408621858a183b8df90fc17984c0de0f01380600faac6c9a0c56b4` | `65eb309c8bd3a1ce4aad3be3ac6b6a5a1c96bd518ba881f334f1e777c76e209a` | 37,020 / 1,438 | 0.0700 × 0.0474 × 0.0602 |
| favosites / attempt-02 | **PASS** | `364bb5b4209a2eb7076527dc87b28d4659eee233462fd7f44a3f41b21ee5327e` | `6c516f78f143e665ee777d0212463267a4ae186f31d78dc8264db8f4d98a0a65` | 139,440 / 2,602 | 0.1769 × 0.0593 × 0.1667 |
| opabinia / attempt-01 | **PASS** | `a4353db85fd14c30deab7283f3e6d71de05ed2af5d41e90f923ff94f98d55c38` | `ed8ce116558710d800714811d955b82659495a96af10bdc5e9d4214d19af5169` | 94,388 / 4,724 | 0.0500 × 0.0247 × 0.1697 |
| choia / attempt-02 | **PASS** | `30f6c8b4bcf1c73f5c0c56672eac14710fc41997e556fd6311c95dc24750fcea` | `3f363e32b160db53353ccaffadfa4f0b2fcb9475ed46263890e4cafcf9d12818` | 97,640 / 4,776 | 0.0600 × 0.0039 × 0.0525 |

### calceola — PASS

The cup has a readable slipper outline and open recess; the single lid meets the rim at a visible hinge and remains attached in the side, hero, reverse-hero and top views. The opening, thin rim and ribs remain legible at close size. I saw no missing faces, detached lid, accidental intersections, or shading artifacts in the exact runtime views. The measured 70 mm span matches the nominal cup-and-lid art-direction scale.

The frozen source ledger notes inherited/search-result access. On this review, Wiley's abstract was accessible and supports a slipper-shaped Calceola with an operculum; the full text was unavailable. Detailed hinge mechanics and soft anatomy remain unverified and are not claimed by this inspired-by asset. [Wiley abstract](https://onlinelibrary.wiley.com/doi/abs/10.1111/1475-4983.00254)

Evidence: [exact-GLB 8-view contact sheet](../../../../assets/candidates/continuous-small-life-round02-20261018/batch-04/calceola/r001/attempt-03/views/contact-sheet.png); [Three.js 480 px multi-angle and size contact sheet](runtime-attempt-02/calceola-contact-sheet.png).

### favosites — PASS

The rounded colony reads as densely packed, recessed polygonal tubes in hero, top and side views; the tube mouths continue into a continuous mound and the sealed base is intact. Repetition is regular but communicates the requested honeycomb structure rather than looking like accidental mechanical assembly. No missing surfaces or visible intersections. Its 176.9 mm measured width is consistent with the nominal 180 mm art-direction width.

The consulted Digital Atlas collection identifies named Favosites specimens and describes them as honeycomb tabulate corals. This supports only the broad stylized form; no species-level or locality reconstruction is claimed. No Atlas model or image is incorporated. [Digital Atlas of Ancient Life](https://www.digitalatlasofancientlife.org/vc/cnidaria/anthozoa/tabulata/)

Evidence: [exact-GLB 8-view contact sheet](../../../../assets/candidates/continuous-small-life-round02-20261018/batch-04/favosites/r001/attempt-02/views/contact-sheet.png); [Three.js 480 px multi-angle and size contact sheet](runtime-attempt-02/favosites-contact-sheet.png).

### opabinia — PASS

Five eye tips are visible in the top and front views; the single long proboscis reaches a bifid terminal grasper; the tapered low body, paired side lobes and tail fan read as one connected animal across front, rear, side and hero views. The soft parts join the body cleanly, with no visible floating pieces, holes, or conspicuous intersections. Eye grouping is compact but all five remain discernible at the intended near view.

The GLB's overall long-axis bound is 169.7 mm. This is not a scale mismatch: the exact generator defines the nominal 100 mm as body length excluding the proboscis and tail fan; appendages account for the longer overall bound. The documented free-swimming mount places the lowest surface at glTF Y = 5 mm, rather than on the floor. The ROM page supports the five-eye, nozzle and lateral-lobe features used for this broad inspired-by claim. [Royal Ontario Museum, Opabinia regalis](https://burgess-shale.rom.on.ca/fossils/opabinia-regalis/)

Evidence: [exact-GLB 8-view contact sheet](../../../../assets/candidates/continuous-small-life-round02-20261018/batch-04/opabinia/r001/attempt-01/views/contact-sheet.png); [Three.js 480 px multi-angle and size contact sheet](runtime-attempt-02/opabinia-contact-sheet.png).

### choia — PASS

The low elliptical disc and long radial spicules form a readable, connected silhouette in hero, top, front, rear and bottom views. Its very thin profile is intentional and matches the frozen brief; the disc appears continuous from top and underside, with no visible hole or detached rays. The model remains recognizable at close size without requiring individual spicule counting. Its 60 mm nominal span matches the measured X bound.

The ROM page describes Choia as a discoidal sponge with long radial spicules and captions complete specimens showing a central disc and radiating spicules. This supports the basic morphology, not a strict reconstruction. No ROM source media is incorporated. [Royal Ontario Museum, Choia carteri](https://burgess-shale.rom.on.ca/fossils/choia-carteri/)

Evidence: [exact-GLB 8-view contact sheet](../../../../assets/candidates/continuous-small-life-round02-20261018/batch-04/choia/r001/attempt-02/views/contact-sheet.png); [Three.js 480 px multi-angle and size contact sheet](runtime-attempt-02/choia-contact-sheet.png).

## Independent integrity and runtime evidence

- Recomputed SHA-256 values for all four `.blend` and `.glb` files match the delivery index, candidate artifact entries, source-export reports, view manifests and runtime loader reports. Exact GLB byte counts match the handoff. Candidate generator, attempt config, brief and reference-ledger hashes also match their referenced files.
- Independently reopened each `.blend` with Blender 4.3.2 and counted evaluated mesh triangles and world-space bounds in `EXPORT`. After converting Blender coordinates `(x, y, z)` to glTF `(x, z, -y)`, triangle counts match exactly and maximum source-to-GLB bound errors are: calceola `1.28e-9 m`, favosites `0 m`, opabinia `0 m`, choia `7.28e-12 m`.
- Independently parsed each exact GLB with `scripts/qa_glb.py` using the frozen limits (14,000 triangles, 6 materials, 30 primitives). All four have no audit errors; counts, bytes, bounds and semantic digests match their QA and two-rebuild records. The only parser warning is Opabinia's 5 mm lowest-Y mount, which is intentional and documented. The hash-bound Khronos reports show 0 errors and 0 warnings for each exact GLB.
- Checked every candidate artifact hash, all 8 fixed-view manifest frame hashes, each model's 7 480 px runtime views, 3 size captures and contact-sheet hashes: 30 integrity checks per model, no mismatches. Three.js 0.180.0 loaded and rendered the exact GLBs with no runtime errors. The renderer is Google SwiftShader software WebGL; this does not establish physical-GPU performance.
- The 12-instance scene loaded each of the four exact GLB hashes three times at scale 1; `viewer.html` only offsets clones by position. Its capture reports 70 draw calls and 40,622 triangles, including the floor, and has no load/render failures. The scene preserves each asset's metre-scale proportions; it is not a cross-period coexistence or museum-performance claim.
- Existing rebuild-A/rebuild-B outputs are byte-identical to each candidate GLB and their semantic digests match. Their reports state that successful build-queue records attest execution; this review does not claim a cryptographic proof of generator execution.

## Legacy checker / acceptance-record compatibility

I ran `python scripts/validate_candidate.py <candidate.json> --root . --json` for each item. All four returned `valid: false` at the first reference-ledger error: the source entry lacks the checker's required `license` text field. The frozen ledgers already say `consulted-only` and state that no source media, mesh, or texture is incorporated, so this is a machine-readable record-format gap, not an identified rights breach. The reference schema's allowed `reference-only` value would express the current rights boundary, but changing a frozen ledger would change its hash.

The current checker also hard-requires at least two turntable frames and, for production profiles, front/rear/left/right/top/bottom/clay/wire/detail views. The frozen task instead explicitly sets `turntable_frames: 0` and requires the eight fixed views `hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`. Those exact eight views are present and hash-bound. Thus the checker cannot certify these candidate records under this task's contract. Its failure must not be reported as a clean validator PASS, but it does not reveal a model defect. No thresholds or CI rules were relaxed or edited here; parent release coordination should resolve the record/checker contract separately.

**Release boundary:** these are independent PASS verdicts for the exact assets and frozen brief, not a change to `candidate.json` approval fields or publication state. The review branch is separate and is not merged by this task.
