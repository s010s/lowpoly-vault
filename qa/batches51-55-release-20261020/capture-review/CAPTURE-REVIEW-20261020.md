# Independent capture addendum: batches 51 and 55

Reviewed 2026-10-20T04:18:30.094078+00:00. Additive extension to `REVIEW.md`; the source/declaration findings and all their conditions remain unchanged.

## Verdict

PASS for all eight exact ModelStage card/reference pairs. This closes only the selected-source actual-renderer capture and image-review gate. It does not complete bounded publication, formal candidate acceptance, generator reproducibility, physical-GPU testing, intended target-scene testing, approved gallery detail/wheel review, final CI, merge or deployment.

## Immutable provenance and byte binding

- Repository: `s010s/lowpoly-vault`. Capture run [39368175380](https://github.com/s010s/lowpoly-vault/actions/runs/39368175380), job `118449690500`. Independently fetched API job and all step results are completed/success.
- Exact capture head: `acdfbc66541b007dddb5f5438a307d76c822b239`; inherited baseline: `62c00f18f6ca79db18ceab9bc2b44d37bdc2573e`.
- Artifact `12239989007`, `pinned-publication-capture`, 415,874 bytes. Independently fetched GitHub digest and job upload receipt agree with the locally recomputed ZIP SHA-256: `d8fdb18666b14898505242e90c723267314f84447c661703a4f1fa4d58babe6a`.
- All 18 archive file entries match extracted bytes exactly, without extra files: eight WebP cards, eight PNG references, render report and capture-time index.
- Every capture descriptor GLB/metadata/QA pin matches the exact original source or QA commit and capture head. All eight GLB hashes match the source-scope accepted subjects. Batch 55 original production-output paths and candidate paths contain the same accepted GLB bytes; paths were not mistaken for new model revisions.
- The capture descriptor is identical to the exact descriptor embedded in the workflow. It says `capture_only=true` and `publication_authority=false`.
- Source files for the real ModelStage viewer, capture script, preset, image-path recipe and package/lockfile are unchanged from the inherited baseline. Exact hashes are recorded in `capture-review.json`.
- Viewer SHA-256: `3d3e6dd1335c21b0836ebcf32689a4bfc558a8803ac2cc666e407f79ced509d0`. Preset SHA-256: `2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff`.
- Runtime: Three.js `0.180.0`; Playwright/playwright-core `1.56.1`; Chromium `141.0.7390.37`, matching the captured pin and installation log. The capture launches ANGLE/SwiftShader, so no hardware-GPU claim is made.
- Capture telemetry records eight model requests and eight parses, peak one request, totaling 1,587,776 GLB bytes, equal to the eight selected payloads. The script requires successful real ModelStage first paint for each asset. It does not preserve a separate browser console-error inventory, so this review does not claim a verified zero-console-error audit.

## Image inspection

All eight original PNG references and eight corresponding WebP images were inspected. Each is 768 × 768 RGBA, nonblank and fully inside its image bounds. Every WebP hash/byte count agrees with its index and report. PNG/WebP alpha masks match exactly. Visible RGB mean absolute differences are 0.51–1.54 out of 255, consistent with the declared quality-0.9 lossy card encoding; no critical visible encoding defect was found.

Transparent WebP hidden RGB can look blocky in alpha-ignoring previews. For an accurate visual check, I decoded the exact WebPs and inspected separately labeled alpha composites on the declared `#e8e4dc` background. Their alpha boundaries are identical to the references. These are inspection copies only; original capture bytes were not changed. No model or capture was rerendered.

### dicranurus r001: PASS
Both curved horns remain distinct with open negative space; lateral spines and segmented body are readable; no tip or body crop.
- Reference PNG SHA-256: `204f235e3b2f09e9dca5ceb12c913c313fa139ba4c1f79056d5f3705dbd0cc82`.
- Card WebP SHA-256: `7c77acdba4580d92598699ab1d5cd12eb84041dd8288ad0e52bfcbcdc2d03e0e`.

### calcite-raft-deposit r002: PASS
Pale thin overlapping plates remain distinct over the tan substrate; complete slab silhouette and edges are visible.
- Reference PNG SHA-256: `2e58eb4d64aaf6813d4b38795493f8972ebf3d9d347d571311152e1ed8879144`.
- Card WebP SHA-256: `22bd23cdb081f540a0ba6b0a4defcdad729fc649510cd7f887ce911c304f0916`.

### accretionary-lapilli-bed r002: PASS
Layered block, upper nodules and three exposed concentric sections remain readable; entire block is in frame.
- Reference PNG SHA-256: `80e40df6891a4da13ba1c5972bd0df010cc0af1520b1e4ffee3695f4de9c678e`.
- Card WebP SHA-256: `0183bde24a5c2e507358e0bf2007e34508a66e1bfda6bd4fb63cfaf4add4b744`.

### conichnus-conical-burrow r001: PASS
Circular opening and sediment-block silhouette are visible without crop. This single pale oblique hero does not by itself prove cavity depth or taper; those remain supported by the preserved original multi-view/ray-probe QA, not newly inferred here.
- Reference PNG SHA-256: `f7ccc38bbc4429f91de72a35ee6e6fd2936840a4ad2b8bf603c4efa918149d03`.
- Card WebP SHA-256: `5a96178925499b5ad1c937bafdf49c352d5e62efa18706a4511a08f97d35dec2`.

### vermicularia r001: PASS
Continuous juvenile coil, long adult tube and open aperture/lumen remain readable, with clear separation and no cropped extremity.
- Reference PNG SHA-256: `0f1210f16065ea22bc0ff3aa9fff3a59f7c538cfc54afd171939bf192150451a`.
- Card WebP SHA-256: `a5738d45964606eb3d5034ef63817afb7395c709028b7b12fef59ebc371cd823`.

### weichselia r001: PASS
Stem, attachment relief and cut end remain readable; complete top and base are visible.
- Reference PNG SHA-256: `037f7be551d3a979e7fa90adddf9ace911f2eed7ae5182d8747c037ad9f0315e`.
- Card WebP SHA-256: `d6fbc2500edc3f4a703553af3c7403ce5647ef04ac7ebc4131f5c190edddfd91`.

### ventifact r001: PASS
Broad planar faces and sharp meeting ridges remain readable; no missing surface or crop is visible.
- Reference PNG SHA-256: `69c228408dc80cfac34b9c6a0f07acede1b6e6db62ae5ef212d6240188000750`.
- Card WebP SHA-256: `8969b6a9ce883a64b69b017f36e5eff57bfc9c28bf9e75fa7d4fa3f882d381ff`.

### pentichnus-deep-dwelling-trace r002: PASS
Sectional negative cavity visibly narrows downwards; rim, long walls and bottom region remain in frame. This remains an illustrative section, not an uncut specimen claim.
- Reference PNG SHA-256: `bfa5ccdce52a8d3f41f5d05839810ca80f3970457d9c8e52d3b2b3f654ac7f99`.
- Card WebP SHA-256: `5e0c94274e67bb1f4bcf8aa84779c2ec1361d9d01071622cb12472eaefd9fcdb`.

## Integration boundaries

- There is exactly one captured view per selected asset, not 24 newly captured turntable frames. The preset contains the shared 24-frame default, but this run is explicitly posters-only and the per-asset report records `frames=1`.
- The index preserves 190 inherited posters and adds eight. It is a capture-time snapshot, not evidence of the final trusted main baseline. Merge only the eight independently reviewed new entries into the then-current release index; do not overwrite later approved additions with this snapshot.
- Final integration must retain these exact sources, viewer/preset/recipe bindings, WebP bytes and reference PNGs, or obtain the narrowly affected updated capture evidence. This review does not authorize changing renderer semantics.
- Batch 51 corrected nominal spans must still explicitly cite specification-correction-v001, with actual bounds separately reported. Original 0.42/0.60 m frozen-brief failures stay historical failures. The capture does not modify or approve any descriptive release metadata.
- Batch 55 remains subject to the precise 20-gap historical-maker-log disclosure and `certified_generator_rebuild=false`. Post-modeling packaging declarations remain labeled as such.
- Formal profile approval stays BLOCKED; physical GPU and intended target scene remain unverified, and unknown generation/authoring timestamps remain unknown. No historical PASS is rebound to a new candidate.
- Separate approved gallery detail/wheel output, bounded collector and tamper tests, complete payload verification, trusted-baseline incremental CI, coordinated merge, Pages deployment and live-site readback remain required.

## Evidence files

- `capture-review.json`: exact per-asset source/image pins, ZIP checks, runtime bindings, dimensions and alpha/encoding comparison.
- `capture-api-receipts.json`: independently retrieved artifact and successful job/step records.
- `capture-job.log`: independently retrieved original CI job log.
- `decoded-webp/`: labeled inspection-only decoded/composited copies, not replacement release payloads.

The earlier coordinator `capture-status.json` is a pre-completion snapshot and was left untouched. Terminal success here comes from the fresh API job response and immutable upload receipt. The initial local audit stopped because this sparse checkout lacks package.json; the successful audit read package files from exact Git commits instead. No source, evidence, policy, code, remote or deployed site was altered.
