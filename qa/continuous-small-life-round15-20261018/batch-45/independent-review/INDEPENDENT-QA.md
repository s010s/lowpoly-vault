# Batch45 independent QA

**Scope:** only `tokummia`, `obsidian-flow-face`, `helictite`, and `protovirgularia-chevron-trail`, bound to the exact handoff and model-source commits below.

- Profile: `static-stylized-v1`, rule `2026-10-18.1`
- Candidate branch: `candidate/small-life-batch45-20261018`
- Handoff commit: `2ef6f5bca0f63b753dbfa7fa0192f925fb2785c3`
- Model-source commit: `8d486f11e0d89970a1e886589c5d3b5f993b6e53`
- Review branch: `qa/s010s/batch45-independent-qa-20261019`

## Decision

**Content review: PASS for all four exact pinned assets within their frozen, intentionally stylized scopes. No model repair is required. Formal acceptance: BLOCKED.** The frozen candidate records remain `approved_for_brief=false` with all seven formal stages `unknown` and approval `pending`. The captured browser renderer is ANGLE SwiftShader software WebGL2; this evidence does not satisfy a hardware-GPU gate or establish device performance.

**Reviewer identity caveat:** this execution context exposes no attested model/reasoning metadata, so the requested `GPT-6 Luna xhigh` identity cannot be independently confirmed. The requested identity is recorded as requested; no second review round was started.

## Hash-bound assets

| Asset | Attempt | Dimensions (m) | Triangles | Blend SHA-256 | GLB SHA-256 | Result |
|---|---|---:|---:|---|---|---|
| tokummia | `attempt-01` | `0.100000 × 0.021628 × 0.045221` | 10,668 | `1faf9e4f465af8b77674274c5ab6dae3879b3dfedead0ddf0f9d173c625ccbf4` | `be3300c4da0e245a8f30d27403bbaccaff769be5003150e7dd8601af46f26bde` | Content PASS / formal gate blocked |
| obsidian-flow-face | `attempt-02` | `0.700000 × 0.480991 × 0.241993` | 7,256 | `f9a8f0d000df15046f296fbe1c5711ab60b0226ca3faa90ba16b23e8a29f3d5a` | `af1b9ee1e7b43c0ea381363849aa20eaeb0dd0ad1390ddad7c372507df848c90` | Content PASS / formal gate blocked |
| helictite | `attempt-02` | `0.236521 × 0.193293 × 0.076768` | 8,898 | `8e149292746e5d5176a0580c5ef522f4eb3dcf7cd53c3c5b309244d43ba7ec97` | `03c833696173e8d272bb39186f6d10b9ae5687e4fad71944cd48259b22fd9260` | Content PASS / formal gate blocked |
| protovirgularia-chevron-trail | `attempt-02` | `0.164878 × 0.015180 × 0.330697` | 10,898 | `9a013cd74fe14c83604058c29507417ec7bf16c22cf6380a90833be79562852f` | `ceb9cd24d4b097cfa41e120c1f15641b878d1d3ff4b2bd0368351dc48647e511` | Content PASS / formal gate blocked |

All four GLBs have zero textures and remain below 14,000 triangles and 1 MB. Exact GLB and Blend paths, byte counts, candidate hashes, and checkpoint pins are in `independent-review.json`.

## Checks completed

- The handoff and QA scope agree on exactly these four IDs and source commit `8d486f11e0d89970a1e886589c5d3b5f993b6e53`. Each selected GLB and Blend file’s direct SHA-256 matches both the handoff and candidate record.
- Inspected all source/runtime contact sheets, the true-scale contact sheet, and original-resolution key views. Recomputed SHA-256 for all 8 source frames and 12 runtime captures per asset; all 80 image files match the frozen view manifests. Protovirgularia was reviewed at final `attempt-02`; its top and side runtime pixels show the raised chevrons above the host surface. The archived `attempt-01` occlusion is not used as current evidence.
- Persisted source-reopen/source-export evidence is bound to the exact Blend and GLB hashes; triangle counts and bounds match, with no export errors. The source-export checker emits only its pinned smooth-face review warnings; visual review found no defect.
- The two already-recorded rebuild outputs per asset were checked by direct hash against the delivered GLB and both semantic-match records. All eight outputs are byte-identical to their exact pinned GLB. No rebuild was repeated.
- Existing Khronos reports are hash-pinned with zero errors and zero warnings. Existing runtime and six-instance scene reports are hash-pinned to the same GLB, pass on WebGL2 / Three.js r180 / ANGLE SwiftShader, and their 12 capture-image hashes per asset match the report.
- No browser replay, source-export rerun, Khronos rerun, rebuild rerun, or profile rerun was performed; the immutable pinned evidence was read and compared to the actual files. No candidate record or model file was modified.

## Per-asset review

- **Tokummia — PASS.** The long segmented trunk reads beneath the paired lobate carapace; the anterior pincer pair has open gaps, and walking limbs and caudal rami remain legible across the fixed and runtime angles. Simplification and palette fit the frozen teaching-art scope. No must-fix.
- **Obsidian flow face — PASS.** The irregular dark glass face reads as a substantial exposure. Broad concave fracture scars and sinuous bands remain visible in clay and exact-GLB views; reflections do not obscure the geometry. No must-fix.
- **Helictite — PASS.** Tapered, contorted mineral tubes and subordinate curls remain distinct across views and visibly root into the declared limestone fragment. No detached branch or must-fix observed.
- **Protovirgularia chevron trail — PASS on final attempt-02.** The median trail and bilateral raised V relief remain visible above the host in the final top and side runtime pixels, with ribs connected to the axis. The earlier attempt-01 occlusion is archived history only. No must-fix.

## Evidence and limits

- Repository guidance: no `AGENTS.md` was present. The `.agents/skills` inventory is animation-focused; its `review-animations` skill/standards were read and do not apply to static prop geometry. The static candidate contract and pinned `static-stylized-v1` rules were reviewed.
- Batch overview and actual-scale images: `production/continuous-small-life-round15-20261018/work/batch-45/batch45-contact-sheet.jpg` and `batch45-true-scale-sheet.jpg` (both hashes are pinned in the JSON report).
- Detailed exact evidence paths and SHA-256 values: [`independent-review.json`](independent-review.json). The review is bound to each fixed-view manifest, source/runtime contact sheet, source-scene/export report, rebuild report, Khronos report, runtime report, scene report, candidate, Blend, and GLB.
- The source ledger is consulted-only; no third-party media is incorporated. This review stays within the frozen artistic claims and does not assert exact specimen morphology, locality, scale, behavior, or co-occurrence.
- Formal production acceptance remains blocked by the frozen unknown stages, pending approval, and missing hardware-GPU evidence. Publication authority remains separate from this review.
