# Batch 32 independent QA — continuous-small-life round 11

- Reviewer: Leon Made This <8357465+s010s@users.noreply.github.com>.

**Conclusion: PASS for the brief-scoped independent visual and technical QA.** All four exact IDs are verified. **Must-fix model issues: none.**

- Handoff source commit: `5d2cfac309a28b05a1f213d69f79938081c8bbdc` (report branch is based directly on this commit).
- Frozen handoff inputs: `HANDOFF.md` `54a70e1f217eeb4f959b28e80d81f61021b27955add6169c3ac4f0951ebb859d`, `final-handoff.jsonl` `045703462fe390bc43200a95dd2f9fc3fae1e4b080f475d9f4c8d0cfa84280f6`, `scope.json` `f55d56fa74091305ca8d84226843c0d2f1a9d10e5bfa191d7bac43486d4e20dd`.
- Visual evidence: all fixed-view and runtime frames were inspected as pixels; the frozen manifests and every referenced frame SHA256 were checked. Exact per-item contact sheets and independent technical outputs are in `evidence/<asset-id>/`.
- Technical evidence: Blender 4.3.2 reopened the pinned Blend files, independently compared source-export bounds and triangle counts, imported exact pinned GLBs, and independently rebuilt each GLB. All eight-view source manifests contain exactly hero/reversehero/front/side/rear/top/clay/silhouette with zero turntable frames.
- Runtime pixels show the requested form at normal viewing scale. Web evidence is **Chromium ANGLE SwiftShader software WebGL** (Batch 33 uses Three.js 0.180.0); it demonstrates function and pixels only. No physical GPU performance is claimed.
- Scope: natural, polished, stylized low-poly teaching assets. The review does not certify exact taxa, measured fossil specimens, paleoflow, or universal geologic processes; those are outside the frozen briefs.
- Blend-import review prompts for smooth faces and GLB corner-split boundary-edge counts were visually reviewed against the actual geometry/wireframes. No visible cracks or export mismatch were found; these are not repair items.
- The independent static-stylized-v1 2026-10-18.1 candidate-record check passes for each item. Existing candidate records remain `approved_for_brief=false`; formal approval stages are still unresolved and were not changed by this report. The inherited `legacy-v1` gate continues to flag missing `license` text on consulted-only reference entries; no guessed license or source-media reuse was introduced. This is separate from the scoped QA verdict.

## Exact item pins and scoped observations

| Asset ID | Candidate checkpoint | Delivered GLB SHA256 | Triangles | Rebuild byte-identical | QA observation |
|---|---|---|---:|:---:|---|
| `ctenocystis` | `0a138d15e155…` | `5fa8da2d107ecd444ddbbab5f9801807b1c5a970b460713ffe2b12bed82e1ecc` | 2,270 | `True` | 低矮、双侧对称的板状体、分节边缘板与前端梳状构造在固定视图及 GLB 像素中清楚；符合简报限定的启发式教学形态。 |
| `baculites` | `cfad590fcd56…` | `89600216159c052b2c667ff55c31a18011f6ac6022738aa1ace5ed1c11742b1b` | 4,156 | `True` | 近直、逐渐收窄的压扁壳体、真实开口壁与内腔可辨；线框显示开口壁连续。 |
| `estuary-basin` | `ebdd87bff416…` | `22d8cbe94157394901e294c39f9d9a0476dd2a89282266696eefc3b6b9681d56` | 6,202 | `True` | 展宽主槽、支槽与低沙洲在俯视/斜视和运行时画面中可辨；保持为无水的陆床地块。 |
| `cross-bedded-sandstone` | `e151470dae73…` | `1a93b06b2a9a3457f0f11bff876328dc50b5d8c2f3a7a730fe411ebc200b3ac1` | 588 | `True` | 三组交错层理由真实倾斜、截切的楔形几何组成，剖面起伏在灰模和运行时像素中可读。 |

The source Blend SHA256, GLB size, decoded semantic digest, exact frame-manifest SHA256, runtime evidence and detailed audits are recorded in `results.json`. Each evidence directory includes independently generated GLB audit, Blend source-export comparison, source mesh inspection, Blender GLB roundtrip report/wireframe, fresh rebuild log and static-profile report; contact sheets and pinned runtime evidence are included alongside them.

## Remaining blockers

- **Model repair required:** none for these frozen briefs.
- **Separate release/process state:** the maker candidate records were not mutated and are not marked approved; their recorded formal stages remain pending/unknown. The unchanged legacy gate also reports consulted-only reference rows with no nonempty license field. This QA report alone does not change either state.

## Handoff files read

- `HANDOFF.md`: `54a70e1f217eeb4f959b28e80d81f61021b27955add6169c3ac4f0951ebb859d`
- `final-handoff.jsonl`: `045703462fe390bc43200a95dd2f9fc3fae1e4b080f475d9f4c8d0cfa84280f6`
- `scope.json`: `f55d56fa74091305ca8d84226843c0d2f1a9d10e5bfa191d7bac43486d4e20dd`
