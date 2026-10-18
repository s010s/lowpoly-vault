# Batch27 independent QA

**This report applies only to `batch27`: Sollasina, Ottoia, Eocladus, and limestone-pavement.** It was prepared from the exact handoff commit and model-source commit below. No batch01, batch18, or batch23 QA conclusion was used.

- Profile: `static-stylized-v1`, rule `2026-10-18.1`
- Candidate branch: `candidate/small-life-batch27-20261018`
- Handoff commit: `8c16ab8777d98d30674dda79dae90031e11e90bc`
- Model source commit: `bd4a80f1b9595480bf73b2d2369e28aae5770cef`
- Review branch: `qa/s010s/batch27-independent-qa-20261018` (based on `origin/main` `da272109c96e3c38a7f2421dc2340c192a0153bb`)

## Decision

**Content review: PASS for all four pinned assets within their frozen, intentionally stylized claim scopes. No model geometry repair is requested. Formal profile acceptance: BLOCKED.** The candidate records remain unapproved (`approved_for_brief=false`). The independent Blender, fixed-view, and Chromium/Three checks pass, but their WebGL2 renderer is ANGLE SwiftShader software rendering. It does not satisfy the required hardware-GPU stage, so this report does not mark the profile accepted.

The exact remaining action for each model is: run the required WebGL2 runtime/GPU capture on a supported hardware GPU (not SwiftShader), record the device/renderer and screenshot hash, and bind the report to that model’s exact GLB SHA below. This is evidence work; no source/model change or threshold/CI change is indicated.

## Hash-bound assets

| Asset | Attempt | GLB triangles | GLB dimensions (m) | Blend SHA-256 | GLB SHA-256 | Result |
|---|---:|---:|---|---|---|---|
| sollasina | `attempt-01` | 8,050 | `0.061310 × 0.012020 × 0.060219` | `6bc87e49512e84f3abb5b8c46c971a5e71f54d0fb52b90bf5100701a8632e452` | `f6d12978189266bfd5fbad4504f3beef6d355c4dcb2683a7ba9c9c6d3a633170` | Content PASS / GPU gate open |
| ottoia | `attempt-01` | 8,816 | `0.067135 × 0.013342 × 0.070035` | `62ae0ec332bda35ddeb01cfe5ee3393bb329ae45b2fbebc65112bd70d0cf0c6b` | `1a384d0f920016b04faf7e848e821156a60f57ddebfc4e6f14aa935db64ff7c2` | Content PASS / GPU gate open |
| eocladus | `attempt-02` | 9,812 | `0.053378 × 0.001305 × 0.147076` | `69bf10e1a602a12436d9745504a9936d1a485e0cba2ac3defb7e687b8f212a9f` | `6861da609c64f7433e31d0214541938f8552baa6532c0ea7a10666cd0148fb9a` | Content PASS / GPU gate open |
| limestone-pavement | `attempt-02` | 11,812 | `3.000000 × 0.505366 × 2.289977` | `2e124144a128f6fdc3d71b510cd72f7b3ff4127319cd374f344cbcca80082f66` | `b4a061d66caa7023c5f20f004e8f8ec241f3a580b2e14d6798ececb20a5eaccd` | Content PASS / GPU gate open |

The selected checkpoint commits are `sollasina 505a4c0706a85d05464e97f0d9ad60ff35767575`, `ottoia 0372f2b6cdc802b39779d55fb4a7c658ea83d993`, `eocladus 2886489b9bd180e448afee9de77b8dc448fd4203`, and `limestone-pavement bd4a80f1b9595480bf73b2d2369e28aae5770cef`. The Blend and GLB SHA-256 values above match the handoff pins.

## Checks completed

- The handoff names exactly the four assets above; its selected candidate records report profile-contract `pass` and record validity `true`, while all remain `approved_for_brief=false`. All pinned source dependency hashes were checked against the model-source commit.
- Blender 4.3.2 read each exact `.blend`, evaluated the `EXPORT` geometry, imported the exact `.glb`, and compared geometry. Triangle counts match at 8,050 / 8,816 / 9,812 / 11,812. Bounds match within `1e-4 m`; export parts are closed, with no degenerate faces or nonfinite normals. Per-asset details are in `evidence/blender/*.json`.
- The eight fixed 512×512 views (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`) are present, hash-bound to each GLB, and have zero turntable frames. The independent contact sheets were visually inspected.
- Fresh browser execution loaded each exact GLB using Chromium `154.0.8037.57`, Three.js r180, and WebGL2. Each asset passed 10 single-item views and two six-copy scenes with zero WebGL errors. This confirms parse/function/render on the available software renderer only.
- The four-asset scene uses original units without per-asset resizing and includes a 100 mm reference bar. It renders four assets with zero WebGL errors. The 3 m-wide pavement dominates the 6–15 cm biological props in this world-scale view; that is the real-size relationship, not a geometry defect. Evidence: `evidence/runtime/batch27-relative-scale-scene.png`.

## Per-asset review

- **Sollasina — content PASS.** The plated central form and surrounding podia read across the fixed views. The metadata’s scope is named-taxon-inspired teaching art, not a strict species reconstruction. Keep the generic fallback label anywhere the presentation might imply an exact fossil specimen. No missing faces or detached podia were observed.
- **Ottoia — content PASS.** The curved annulated trunk, short anterior introvert, and posterior hook accents remain a connected form. The small repeated structures are simplified; no exact hook count, body length, ecology, or fossil pose claim is made. The ROM description notes a commonly U-shaped trunk, annulation, and posterior hook rings; see [ROM Ottoia description](https://burgess-shale.rom.on.ca/fossils/ottoia-prolifica/), Description section.
- **Eocladus — content PASS within a specimen-fragment scope.** Axis and lateral branching read in silhouette and clay views. Keep the existing `needs-specific-reference` tag; do not describe this as a complete parent thallus or exact specimen. LoDuca et al.’s primary paper abstract describes Eocladus laterals branching to fifth order and a central axis with laterals ([paper, p. 1](https://www.vliz.be/imisdocs/publications/226999.pdf)).
- **Limestone-pavement — content PASS as an original stylized terrain prop.** Clints and grikes read as a coherent patch and the actual 3 m span is preserved. Keep the no-locality/no-coastal-origin scope. The small biological assets appear much smaller beside it in the actual-scale scene, as their source dimensions require.

The Sollasina source remains the primary paper named in the frozen ledger, but its full text was not directly accessible in the review browser. The narrow inspired-art label therefore remains essential; this review does not certify specimen-level morphology. No third-party geometry, texture, or source image was incorporated.

## Evidence files

- `independent-review.json` — machine-readable hash and stage record
- `evidence/blender/` — source/re-import geometry measurements
- `evidence/fixed-views/` — eight independent views, manifests, contact sheets
- `evidence/runtime/` — per-asset screenshots/reports, mixed-scale scene, aggregate runtime report
- `scripts/` — audit and rendering scripts used to create this independent evidence

No candidate, model, threshold, CI, publication, or Drive file was changed. No merge was performed.
