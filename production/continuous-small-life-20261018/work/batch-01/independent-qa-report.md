# Independent QA — Small-Life Batch 01

**Reviewed source:** `e6391cd3d1059f39feba4dc88a18544cbeebfee6` (`candidate/small-life-batch-01-20261018`)

**Review branch:** `qa/independent-small-life-batch-01-20261018`

**Result:** Archaeopteryx, Canadaspis and Ceratomyrmex **PASS**. Hydropteris geometry and runtime **PASS**, with one mandatory metadata correction before acceptance: current taxonomic naming and uncertainty around the round appendages. No geometry change is requested.

The review is bound to the exact GLBs and editable `.blend` files below. I inspected the eight-view contact sheets, the actual GLB runtime images at 80, 160, 240 and 360 px, all seven runtime directions, and the exact-GLB three-copy scene screenshots. I also reopened each `.blend`, imported each exact GLB into a clean Blender process, and rebuilt each asset into `/tmp` for comparison. I did not use the maker's self-score as a verdict.

## Frozen artifact identities

| Asset | GLB bytes / triangles | Exact GLB SHA-256 | Exact `.blend` SHA-256 |
|---|---:|---|---|
| archaeopteryx | 141,564 / 3,776 | `2f74e3b9620ec72ae02f6e9a986a6e8593519aca7287c1ed7351f30c279d1a04` | `7ac64cd8b03b65f09b51b1b40d668f32d672b9d13bfd90352c7f623fa0b90257` |
| canadaspis | 112,708 / 4,276 | `08619d89a3ef455b9612b0c55575de2abe84ec161c06ef072f38cf7e0d9e98b1` | `a3fe0904a5f8be7d6b205f47c22a4890360fde1711ffa1f6b5f83280e6451522` |
| ceratomyrmex | 43,596 / 1,856 | `41ffc10021d27f7cf799d854076a6dd32ae657f2487dc28f601602a436761c3c` | `b1dfa3c851f188cd874f6f8ef75e3a47e4a24416d8b82b9984c8c5320be5240b` |
| hydropteris | 234,596 / 5,332 | `629e4313bd5c2102135a1809b6be8f778e510d6e928a01a60d8a58152369b125` | `df1b33c1140050cd2d04de155e00f64d22a0e7f645b7ce9bb48758189e14e032` |

These values were checked against `handoff-hashes.json`, each candidate's own file checksums, and the files on disk. Exact manifest checks are retained in [handoff-hash-check.json](independent-evidence/handoff-hash-check.json).

## Per-asset verdicts

### Archaeopteryx — PASS

The front, side, rear, top and bottom views preserve the two-wing/two-leg body plan, long feathered tail, beak with small teeth and wing-hand claws. The tail feathers and wing planes remain connected in the runtime views. At 80 px, small facial and claw detail softens as expected; the main silhouette remains distinct. No conspicuous missing face, unintended penetration, broken attachment or shading failure was visible.

The Natural History Museum overview supports the broad feathered, toothed, long-tailed, clawed-hand identity and explicitly notes uncertainty around the bird boundary and flight. The candidate is labeled as stylized-inspired static art and makes no flight claim, so this scope passes. See the [NHM overview](https://www.nhm.ac.uk/discover/what-were-the-first-birds-like.html).

Evidence: [contact sheet](../../../../assets/candidates/continuous-small-life-20261018/batch-01/archaeopteryx/r001/contact-sheet.jpg), [GLB 240 px](../../../../assets/candidates/continuous-small-life-20261018/batch-01/archaeopteryx/r001/evidence/runtime/hero-240px.png), [runtime front](../../../../assets/candidates/continuous-small-life-20261018/batch-01/archaeopteryx/r001/evidence/runtime/front-360px.png), [runtime rear](../../../../assets/candidates/continuous-small-life-20261018/batch-01/archaeopteryx/r001/evidence/runtime/rear-360px.png), [runtime top](../../../../assets/candidates/continuous-small-life-20261018/batch-01/archaeopteryx/r001/evidence/runtime/top-360px.png), [three-copy scene](../../../../assets/candidates/continuous-small-life-20261018/batch-01/archaeopteryx/r001/evidence/runtime/scene-hero-480px.png).

### Canadaspis — PASS

The dorsal and front views show a paired, suboval shell with a clear dorsal seam, a small exposed head and anterior sensory parts. Side and rear views show the exposed segmented abdomen, marginal spines, terminal processes and repeated limb rhythm. The shell-to-body relationship is readable at the target sizes and does not collapse into a generic oval crawler. No conspicuous unintended penetration, missing face or broken connection was visible.

The Royal Ontario Museum morphology summary describes a bivalved carapace covering about half the body, a rounded protruding head, eyes and frontal appendages, thoracic limbs, and a legless segmented abdomen with spines. The model covers those broad identity cues; it does not assert a disputed crustacean classification or precise anatomy. See the [ROM morphology description](https://burgess-shale.rom.on.ca/fossils/canadaspis-perfecta/).

Evidence: [contact sheet](../../../../assets/candidates/continuous-small-life-20261018/batch-01/canadaspis/r001/contact-sheet.jpg), [GLB 240 px](../../../../assets/candidates/continuous-small-life-20261018/batch-01/canadaspis/r001/evidence/runtime/hero-240px.png), [runtime front](../../../../assets/candidates/continuous-small-life-20261018/batch-01/canadaspis/r001/evidence/runtime/front-360px.png), [runtime side](../../../../assets/candidates/continuous-small-life-20261018/batch-01/canadaspis/r001/evidence/runtime/side-360px.png), [runtime rear](../../../../assets/candidates/continuous-small-life-20261018/batch-01/canadaspis/r001/evidence/runtime/rear-360px.png), [runtime bottom](../../../../assets/candidates/continuous-small-life-20261018/batch-01/canadaspis/r001/evidence/runtime/bottom-360px.png), [three-copy scene](../../../../assets/candidates/continuous-small-life-20261018/batch-01/canadaspis/r001/evidence/runtime/scene-hero-480px.png).

### Ceratomyrmex — PASS within the stated inspired-by scope

The standard hero, front and top views make the tall forehead horn and opposing upturned mandibles distinct. The ant-like body remains segmented, with six attached legs, antennae and a narrow waist. The key head gap is visible at 240–360 px; the 80 px image appropriately prioritizes the overall ant silhouette. No prey, attack pose or behavior claim is present. No conspicuous unintended penetration or broken attachment was visible.

The frozen claim is basic recognizable anatomy, not strict reconstruction. The original 2016 paper is identifiable as Perrichot, Wang and Engel, “Extreme Morphogenesis and Ecological Specialization among Cretaceous Basal Ants” ([Current Biology / DOI](https://doi.org/10.1016/j.cub.2016.03.075)); full text was not accessible in this review. I therefore pass only the broad horn/jaw inspiration visible in the exact GLB, not exact ratios, setae, microanatomy or behavior.

Evidence: [contact sheet](../../../../assets/candidates/continuous-small-life-20261018/batch-01/ceratomyrmex/r001/contact-sheet.jpg), [GLB 240 px](../../../../assets/candidates/continuous-small-life-20261018/batch-01/ceratomyrmex/r001/evidence/runtime/hero-240px.png), [runtime front](../../../../assets/candidates/continuous-small-life-20261018/batch-01/ceratomyrmex/r001/evidence/runtime/front-360px.png), [runtime top](../../../../assets/candidates/continuous-small-life-20261018/batch-01/ceratomyrmex/r001/evidence/runtime/top-360px.png), [runtime reverse hero](../../../../assets/candidates/continuous-small-life-20261018/batch-01/ceratomyrmex/r001/evidence/runtime/reversehero-360px.png), [three-copy scene](../../../../assets/candidates/continuous-small-life-20261018/batch-01/ceratomyrmex/r001/evidence/runtime/scene-hero-480px.png).

### Hydropteris — MUST FIX: taxon and structure wording only

**Visual and geometry: PASS.** The top, side and reverse views show a branching rhizome, roots below, six pinnate fronds with a useful alternating/subopposite rhythm, and three round appendages at rhizome/frond junctions. The rooted patch reads clearly at 80–240 px. No conspicuous missing leaf face, unintended penetration or broken connection was visible; the near view retains the same connected structure.

**Required metadata correction before acceptance:** the user-facing `Hydropteris` name and the unqualified “sporocarps” criterion overstate the current literature. A 2025 nomenclatural paper identifies `Hydropteris` as an illegitimate homonym and treats the Canadian `Hydropteris pinnata` material as a synonym of `Dorfiella knowltonii`. It also describes the simple appendages as having competing interpretations, including floats, sporocarps or reduced fronds. Update the display/taxon metadata to `Dorfiella knowltonii` (optionally noting `Hydropteris pinnata` as the historical 1994 name), add this source, and describe the round structures as uncertain “sporocarp-like appendages” or an explicit artistic interpretation. Keep the internal `hydropteris` asset ID if useful. **No mesh change is requested.** See [Hermsen 2025, Phytotaxa](https://doi.org/10.11646/phytotaxa.733.1.8) and the earlier [Rothwell & Stockey 1994 morphology paper](https://doi.org/10.1002/j.1537-2197.1994.tb15473.x). The 1994 abstract supports branching rhizomes, elongated roots, pinnate fronds, subopposite-to-alternate pinnae and appendages interpreted as sporocarps; the 2025 paper narrows how confidently that last interpretation can be stated.

Evidence: [contact sheet](../../../../assets/candidates/continuous-small-life-20261018/batch-01/hydropteris/r001/contact-sheet.jpg), [GLB 240 px](../../../../assets/candidates/continuous-small-life-20261018/batch-01/hydropteris/r001/evidence/runtime/hero-240px.png), [runtime side](../../../../assets/candidates/continuous-small-life-20261018/batch-01/hydropteris/r001/evidence/runtime/side-360px.png), [runtime top](../../../../assets/candidates/continuous-small-life-20261018/batch-01/hydropteris/r001/evidence/runtime/top-360px.png), [runtime bottom](../../../../assets/candidates/continuous-small-life-20261018/batch-01/hydropteris/r001/evidence/runtime/bottom-360px.png), [three-copy scene](../../../../assets/candidates/continuous-small-life-20261018/batch-01/hydropteris/r001/evidence/runtime/scene-hero-480px.png).

## Technical evidence and warning disposition

Independent static GLB audits passed for all four files with no errors or warnings at the frozen limits (14,000 triangles, 6 materials, 30 primitives). The exact hashes, bounds, triangles, primitive counts and file sizes are in [glb-audit.json](independent-evidence/glb-audit.json). The repository's practical bundle validator also passed; its report is retained at [bundle-validation.json](independent-evidence/bundle-validation.json). The bundled Khronos validator reports are hash-bound to the same GLBs and record zero errors and zero warnings.

I opened each exact `.blend` using Blender 4.3.2 with auto-execution disabled and compared its export collection to the corresponding GLB. All four source/export comparisons matched triangle counts and axis-converted bounds with **0.0 m** maximum error. The only warnings were the pipeline's smooth-face review notices; the reviewed views confirm the smooth organic treatment is intentional, with faceted feather and leaf surfaces retained.

I then imported each exact GLB in a fresh Blender process. All four imports had zero errors, exact triangle counts and **0.0 m** bounds error. The importer reported open boundary edges on thin feather, exopod and pinna sheet meshes, plus smooth-face notices. Those boundaries correspond to intended thin/open surface elements and remain visually coherent in the front/rear/top/bottom images; they do not appear as missing body surfaces. The [source-export reports](independent-evidence/source-export/) and [clean-import reports](independent-evidence/roundtrip/) retain the warnings and exact hashes.

Fresh Blender 4.3.2 rebuilds into `/tmp/small-life-qa-rebuild` were byte-identical to the frozen GLBs for all four assets; semantic digests also matched. See [semantic-rebuild.json](independent-evidence/semantic-rebuild.json). Blender emitted non-blocking startup notices that its extension cache was read-only and the optional Draco library was unavailable. The artifacts are uncompressed standalone GLBs, so neither notice changed the output or blocked validation.

## Style, runtime and non-blocking notes

- Compared with the accepted `small-fauna-trio-v2` examples inspected at commit `c8514b8c348777c9a2d81c6c0bbd9cf02cdb5184` (Diplomystus and Kalligramma hero pixels), this batch uses simpler palette-only surfaces and less surface texture. The four candidates still share the target's restrained natural palettes, clear primary forms, deliberate low-poly rhythm and soft organic transitions. This is a style difference, not a repair requirement for the frozen palette-only brief.
- At 80 px, the smallest facial, jaw and leaflet details naturally soften; the silhouettes and large identity cues remain readable. The 160/240/360 px runtime images retain the expected detail without requiring micro-detail work.
- Runtime evidence uses Three.js r180 through ANGLE/Vulkan SwiftShader. It confirms functional exact-GLB loading and rendering, not physical GPU/device performance. The three-copy screenshots are a neutral prop benchmark, not museum integration.
- The two supported minor operational notes are to frame the very small animal props at a close enough display scale, and to avoid calling SwiftShader results device-performance evidence.

## Commands and retained evidence

```sh
python3 production/continuous-small-life-20261018/work/batch-01/validate_bundle.py
```

This passed all four frozen bundles and verified their integrity and the existing exact-GLB view/runtime evidence. A separate `qa_glb.audit_glb` invocation used budgets of 14,000 triangles, 6 materials and 30 primitives; per-file output is retained in `independent-evidence/glb-audit.json`.

For each asset, the `.blend` reopen command was:

```sh
blender -b -t 2 --factory-startup --disable-autoexec --python-exit-code 1 \
  --python scripts/check_source_export.py -- \
  --source assets/candidates/continuous-small-life-20261018/batch-01/<asset>/r001/<asset>.blend \
  --glb assets/candidates/continuous-small-life-20261018/batch-01/<asset>/r001/<asset>.glb \
  --output /tmp/small-life-qa-reopen/<asset>-source-export.json
```

The clean import command was:

```sh
blender -b --factory-startup --disable-autoexec -t 2 --python-exit-code 1 \
  --python scripts/check_glb_roundtrip.py -- \
  assets/candidates/continuous-small-life-20261018/batch-01/<asset>/r001/<asset>.glb \
  --output-dir /tmp/small-life-qa-roundtrip/<asset> --no-render
```

Fresh rebuilds used `build_batch01.py` for archaeopteryx, ceratomyrmex and hydropteris, and `build_canadaspis.py` for canadaspis, with the frozen per-asset `build-config.json` and output directory `/tmp/small-life-qa-rebuild`. Runtime screenshots inspected are the linked exact files under each bundle's `evidence/runtime/`; their GLB and image hashes are checked by the retained manifest and bundle-validation report.

No candidate model, original GLB, `.blend`, build file, CI, publication allowlist or permissions were changed by this review. This branch contains the review report and independent QA evidence only; it is not a merge or publication branch.
