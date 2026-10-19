# Batch 41 independent QA

**Scope:** exactly four r001 candidates pinned by the batch 41 handoff; one independent QA round.

- Handoff branch: `handoff/batch41-20261018`
- Handoff commit: `a6fabaa18df480e5f73d505162199a51282d25c1`
- `final-handoff.jsonl` SHA-256: `2fd8eee800ac6babb4e2b4f1f2ce7d8b659d274a7237243a56480fd4377aca47`
- Review profile: `static-stylized-v1` / `2026-10-18.1`
- Requested reviewer model: `gpt-6-luna xhigh`; execution identity has no metadata and is **not independently verified**.

## Decision

**Content QA: PASS for all four assets within their frozen, intentionally stylized teaching-art scopes. No model geometry or label fixes are required.** The source records remain `approved_for_brief=false`; formal profile acceptance is **BLOCKED** until a hardware-GPU capture is attached to each exact GLB hash. The available Chromium/Three.js images use ANGLE SwiftShader software WebGL and show function and pixels only, not physical GPU or production performance.

## Hash-pinned candidates

| Asset | Candidate branch commit (verified remote tip) | Blend SHA-256 | GLB SHA-256 | Triangles | Content QA | Must fix |
|---|---|---|---|---:|---|---|
| `selkirkia` | `a3557c8eb9f673e5781f028bb1d93586d050d737` | `cdf4c1faedf28ee4166f2aacbbcc56d1f3dc7f0e745ed82521ca39394fa5ad8a` | `57ce103c80d3ab21a83a76cee11a5e7ba8428768b4048a510f429c8a13ee923b` | 8060 | PASS | None |
| `dicroidium` | `350d9a3e77e4c4e61b1bd6701d68c31f44cb84fd` | `4f49c320e36ac0f9df939a79a98337ea188d25c06380d30857a87c4a375cb1de` | `916976a3511d962c2e8797557e8b52ad5035a6b902c6e8c4120efa30e9350f61` | 2352 | PASS | None |
| `waterfall-plunge-pool` | `28b53366d2f5b682128459e3562829db4d4bb650` | `5914d66910e0fa36ddb8ee42a7075887a779ea0e5dcff523a19d6aa8edc53045` | `d2028eaaedf9e941c407045389020ed94c72fb10dd6eee95bcb641cc4311c298` | 6106 | PASS | None |
| `cave-boxwork` | `631c4da356c01558b4f9fe1c737a5d4f2ce75c49` | `6bbb0bd78c448b1b2532a539003c9f766ce1e0aa63a6f0e1fffc14f5191de057` | `611bfe65b74aecbb90161e9408b6dec96c6c8233c13e2ed36f0c01363e64f10a` | 1224 | PASS | None |

## Checks and results

The handoff JSONL hash matched `scope.json`, all four remote candidate refs matched their pinned full commits, and all 138 hash entries in the four handoff artifact maps matched the fetched files. Each eight-frame fixed-view manifest is bound to the selected GLB; all fixed image hashes match. The actual fixed-view and Chromium runtime contact sheets were visually inspected, with full-size hero pixels opened for each model. All seven runtime screenshots per asset match their manifest hashes and 512×512 dimensions.

Blender 4.3.2 reopened each exact `.blend` with auto-execution disabled and imported the exact GLB. Source and imported triangle counts match; world bounds match; there are no degenerate source faces or non-finite source vertices. Source-export records also report matching triangles and bounds (maximum error 0 m).

Both saved bounded-runner rebuilds per item have `succeeded` / return code `0`. Their result-record hashes and output GLB hashes were rechecked; every rebuild GLB is byte-identical to the selected GLB, and the saved comparison reports `semantic_match=true`. The generators were not run again during this QA. Khronos GLTF reports show zero errors and warnings for all four.

## Per-asset review

### selkirkia

The shell and enclosed animal read as a single teaching subject in hero, reverse, front, side and top views. The two real openings, tube wall, exposed introvert and small posterior end remain legible; the calm color and blunt sparse spines stay child-friendly. Smooth shading is intentional and does not hide a structural defect.

- **Decision:** PASS within the metadata claim scope; no mandatory model fix.
- **Blend:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/selkirkia/r001/selkirkia.blend` — SHA-256 `cdf4c1faedf28ee4166f2aacbbcc56d1f3dc7f0e745ed82521ca39394fa5ad8a`.
- **GLB:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/selkirkia/r001/selkirkia.glb` — SHA-256 `57ce103c80d3ab21a83a76cee11a5e7ba8428768b4048a510f429c8a13ee923b`; 8,060 triangles.
- **Fixed-view pixels:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/selkirkia/r001/qa-contact-sheet.png`; eight frames in `assets/candidates/continuous-small-life-round14-20261018/batch-41/selkirkia/r001/views/render-manifest.json` (all hashes match the selected GLB).
- **Runtime pixels:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/selkirkia/r001/runtime-contact-sheet.png`; exact screenshots under `candidate/batch41-selkirkia-20261018` at `selkirkia/runtime/` (manifest paths and hashes are listed in `independent-review.json`).
- **Blend→GLB:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/selkirkia/r001/source-export.report.json`; pass_with_warnings, triangles/bounds match, max bounds error 0.0 m.
- **Rebuild evidence:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/selkirkia/r001/reproducibility-1.report.json` and `assets/candidates/continuous-small-life-round14-20261018/batch-41/selkirkia/r001/reproducibility-2.report.json`; each bound run result and output path is included in the JSON report.
- **Profile:** contract pass / `static-stylized-v1` `2026-10-18.1`; record valid, `approved_for_brief=false`. Hardware-GPU gate remains open.

### dicroidium

The basal Y rachis and two coherent pinnule-bearing arms read clearly from hero, reverse and top. The fork and one repeated entire pinnule form carry identity without claiming the whole parent plant. Front/rear views are naturally thin for a preserved foliage-organ concept; no geometry repair is needed.

- **Decision:** PASS within the metadata claim scope; no mandatory model fix.
- **Blend:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/dicroidium/r001/dicroidium.blend` — SHA-256 `4f49c320e36ac0f9df939a79a98337ea188d25c06380d30857a87c4a375cb1de`.
- **GLB:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/dicroidium/r001/dicroidium.glb` — SHA-256 `916976a3511d962c2e8797557e8b52ad5035a6b902c6e8c4120efa30e9350f61`; 2,352 triangles.
- **Fixed-view pixels:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/dicroidium/r001/qa-contact-sheet.png`; eight frames in `assets/candidates/continuous-small-life-round14-20261018/batch-41/dicroidium/r001/views/render-manifest.json` (all hashes match the selected GLB).
- **Runtime pixels:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/dicroidium/r001/runtime-contact-sheet.png`; exact screenshots under `candidate/batch41-dicroidium-20261018` at `dicroidium/runtime/` (manifest paths and hashes are listed in `independent-review.json`).
- **Blend→GLB:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/dicroidium/r001/source-export.report.json`; pass_with_warnings, triangles/bounds match, max bounds error 0.0 m.
- **Rebuild evidence:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/dicroidium/r001/reproducibility-1.report.json` and `assets/candidates/continuous-small-life-round14-20261018/batch-41/dicroidium/r001/reproducibility-2.report.json`; each bound run result and output path is included in the JSON report.
- **Profile:** contract pass / `static-stylized-v1` `2026-10-18.1`; record valid, `approved_for_brief=false`. Hardware-GPU gate remains open.

### waterfall-plunge-pool

The deep rounded basin reads directly below the recessed step and projecting lip, and the side/top views show it connected to the upstream bed and continuous banks. The current shape is a clear low-poly teaching patch, not an isolated enlarged pothole or a water-surface effect.

- **Decision:** PASS within the metadata claim scope; no mandatory model fix.
- **Blend:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/waterfall-plunge-pool/r001/waterfall-plunge-pool.blend` — SHA-256 `5914d66910e0fa36ddb8ee42a7075887a779ea0e5dcff523a19d6aa8edc53045`.
- **GLB:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/waterfall-plunge-pool/r001/waterfall-plunge-pool.glb` — SHA-256 `d2028eaaedf9e941c407045389020ed94c72fb10dd6eee95bcb641cc4311c298`; 6,106 triangles.
- **Fixed-view pixels:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/waterfall-plunge-pool/r001/qa-contact-sheet.png`; eight frames in `assets/candidates/continuous-small-life-round14-20261018/batch-41/waterfall-plunge-pool/r001/views/render-manifest.json` (all hashes match the selected GLB).
- **Runtime pixels:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/waterfall-plunge-pool/r001/runtime-contact-sheet.png`; exact screenshots under `candidate/batch41-waterfall-plunge-pool-20261018` at `waterfall-plunge-pool/runtime/` (manifest paths and hashes are listed in `independent-review.json`).
- **Blend→GLB:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/waterfall-plunge-pool/r001/source-export.report.json`; pass_with_warnings, triangles/bounds match, max bounds error 0.0 m.
- **Rebuild evidence:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/waterfall-plunge-pool/r001/reproducibility-1.report.json` and `assets/candidates/continuous-small-life-round14-20261018/batch-41/waterfall-plunge-pool/r001/reproducibility-2.report.json`; each bound run result and output path is included in the JSON report.
- **Profile:** contract pass / `static-stylized-v1` `2026-10-18.1`; record valid, `approved_for_brief=false`. Hardware-GPU gate remains open.

### cave-boxwork

The intersecting mineral fins form open, unequal cells attached to a finite eroded host face. Top, side and reverse views preserve varied cell geometry and fin heights; the surface reads as a stylized geological exposure rather than an equal grid or detached panels.

- **Decision:** PASS within the metadata claim scope; no mandatory model fix.
- **Blend:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/cave-boxwork/r001/cave-boxwork.blend` — SHA-256 `6bbb0bd78c448b1b2532a539003c9f766ce1e0aa63a6f0e1fffc14f5191de057`.
- **GLB:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/cave-boxwork/r001/cave-boxwork.glb` — SHA-256 `611bfe65b74aecbb90161e9408b6dec96c6c8233c13e2ed36f0c01363e64f10a`; 1,224 triangles.
- **Fixed-view pixels:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/cave-boxwork/r001/qa-contact-sheet.png`; eight frames in `assets/candidates/continuous-small-life-round14-20261018/batch-41/cave-boxwork/r001/views/render-manifest.json` (all hashes match the selected GLB).
- **Runtime pixels:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/cave-boxwork/r001/runtime-contact-sheet.png`; exact screenshots under `candidate/batch41-cave-boxwork-20261018` at `cave-boxwork/runtime/` (manifest paths and hashes are listed in `independent-review.json`).
- **Blend→GLB:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/cave-boxwork/r001/source-export.report.json`; pass, triangles/bounds match, max bounds error 0.0 m.
- **Rebuild evidence:** `assets/candidates/continuous-small-life-round14-20261018/batch-41/cave-boxwork/r001/reproducibility-1.report.json` and `assets/candidates/continuous-small-life-round14-20261018/batch-41/cave-boxwork/r001/reproducibility-2.report.json`; each bound run result and output path is included in the JSON report.
- **Profile:** contract pass / `static-stylized-v1` `2026-10-18.1`; record valid, `approved_for_brief=false`. Hardware-GPU gate remains open.

## Remaining formal gate

Capture and bind an actual hardware-GPU runtime check for each exact GLB SHA. This is required for formal profile acceptance. It is not a requested geometry change. Historical legacy license-key failures remain because the sources are consulted-only; no third-party license was invented.

## Evidence files

- Machine-readable review with all per-image SHA-256 values, full branch commits, full artifact paths, Blender results, source-export details, and rebuild request/result/output paths: [`independent-review.json`](independent-review.json).
- Independent Blender audit output: [`evidence/blender-reimport-audit.json`](evidence/blender-reimport-audit.json).
- Audit script: [`scripts/blender-source-glb-audit.py`](scripts/blender-source-glb-audit.py).
- Source per-asset `HANDOFF.md`, `final-handoff.jsonl`, each candidate’s `views/render-manifest.json`, `runtime/evidence-manifest.json`, `source-export.report.json`, `source-mesh-measurements.json`, and both `reproducibility-*.report.json` files are pinned to their respective source commits recorded in the JSON.
