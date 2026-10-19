# Batch 33 independent QA — continuous-small-life round 11

- Reviewer: Leon Made This <8357465+s010s@users.noreply.github.com>.

**Conclusion: PASS for the brief-scoped independent visual and technical QA.** All four exact IDs are verified. **Must-fix model issues: none.**

- Handoff source commit: `1156d5a59362fbc191f217fdacf0dd051b58f95c` (report branch is based directly on this commit).
- Maker model source commit recorded by Batch 33: `9db27f8606b0bdd37baa79ce0af748df129ae3c0`.
- Frozen handoff inputs: `HANDOFF.json` `f2d0205326be610effa38837645b2a56268543fc6e532ae48c8f3fd666240b01`, `QA-HANDOFF-SCOPE.json` `cc878e7320fe1c1f09005134541e5b89bb49f9d7da57c7638e8f610c55c0f26a`.
- Visual evidence: all fixed-view and runtime frames were inspected as pixels; the frozen manifests and every referenced frame SHA256 were checked. Exact per-item contact sheets and independent technical outputs are in `evidence/<asset-id>/`.
- Technical evidence: Blender 4.3.2 reopened the pinned Blend files, independently compared source-export bounds and triangle counts, imported exact pinned GLBs, and independently rebuilt each GLB. All eight-view source manifests contain exactly hero/reversehero/front/side/rear/top/clay/silhouette with zero turntable frames.
- Runtime pixels show the requested form at normal viewing scale. Web evidence is **Chromium ANGLE SwiftShader software WebGL** (Batch 33 uses Three.js 0.180.0); it demonstrates function and pixels only. No physical GPU performance is claimed.
- Scope: natural, polished, stylized low-poly teaching assets. The review does not certify exact taxa, measured fossil specimens, paleoflow, or universal geologic processes; those are outside the frozen briefs.
- Blend-import review prompts for smooth faces and GLB corner-split boundary-edge counts were visually reviewed against the actual geometry/wireframes. No visible cracks or export mismatch were found; these are not repair items.
- The independent static-stylized-v1 2026-10-18.1 candidate-record check passes for each item. Existing candidate records remain `approved_for_brief=false`; formal approval stages are still unresolved and were not changed by this report. The inherited `legacy-v1` gate continues to flag missing `license` text on consulted-only reference entries; no guessed license or source-media reuse was introduced. This is separate from the scoped QA verdict.

## Exact item pins and scoped observations

| Asset ID | Candidate checkpoint | Delivered GLB SHA256 | Triangles | Rebuild byte-identical | QA observation |
|---|---|---|---:|:---:|---|
| `mucrospirifer` | `b386300c0c44…` | `55b0f89e3c36912f5ac34b9300527d969ad1aa53956d373c763ce04b1737d748` | 11,296 | `True` | 长铰合翼与短凸起中央壳体的褶、肋在多方向画面中可读；作为保存壳体教学概念符合简报。 |
| `wave-cut-platform` | `b9f4292baaf6…` | `fbeffd65ef58a40e7276d5c474d0956b2e02203fe8c122f7bf0f48bacda8ecc3` | 6,816 | `True` | 低位海蚀平台与后退崖壁关系明确；风化面片有意保持风格化，尺寸/尺度与裁切边界符合简报。 |
| `flute-cast-slab` | `0097c871150d…` | `4ebbbc5561e622b2ce2fa777dfc6ec4236b1c6fa736a5caf14d290142f5b2268` | 11,192 | `True` | 板面上六枚凸起的圆匙形铸型与收尖尾部真实连入基底，顶视/斜视与 GLB 运行画面均可辨。 |
| `paleodictyon-mesh-trace` | `9db27f8606b0…` | `d0a4427dae977a5c12f7f09b541d36316b0a353ef2237ded516099f9885bef4d` | 6,660 | `True` | 薄管状正浮雕构成连续六边网格；符合教学模块范围，不暗示精确遗迹种或生物机制。 |

The source Blend SHA256, GLB size, decoded semantic digest, exact frame-manifest SHA256, runtime evidence and detailed audits are recorded in `results.json`. Each evidence directory includes independently generated GLB audit, Blend source-export comparison, source mesh inspection, Blender GLB roundtrip report/wireframe, fresh rebuild log and static-profile report; contact sheets and pinned runtime evidence are included alongside them.

## Remaining blockers

- **Model repair required:** none for these frozen briefs.
- **Separate release/process state:** the maker candidate records were not mutated and are not marked approved; their recorded formal stages remain pending/unknown. The unchanged legacy gate also reports consulted-only reference rows with no nonempty license field. This QA report alone does not change either state.

## Handoff files read

- `HANDOFF.json`: `f2d0205326be610effa38837645b2a56268543fc6e532ae48c8f3fd666240b01`
- `QA-HANDOFF-SCOPE.json`: `cc878e7320fe1c1f09005134541e5b89bb49f9d7da57c7638e8f610c55c0f26a`
