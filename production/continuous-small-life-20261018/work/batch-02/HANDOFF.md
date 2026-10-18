# Batch 02 / 首轮四项候选交付

Branch: `candidate/small-life-batch-02-20261018`; base main `643534830397824dfd46990485bd16ad66ecf9ce`.

All four are **candidates awaiting parent-dispatched independent GPT-6 Luna xhigh review**. No independent QA PASS, merge, publication or deployment is claimed. The original planning state is retained unchanged; use `batch-02-result.json` as this maker's owned result for parent reconciliation.

| Asset | GLB bytes | Exported triangles | Source vertices | Export POSITION vertices | Materials / primitives |
|---|---:|---:|---:|---:|---:|
| longipteryx | 47,420 | 2,228 | 1,180 | 1,180 | 5 / 8 |
| urasterella | 135,700 | 6,240 | 3,122 | 3,962 | 3 / 3 |
| alienopterus | 32,340 | 1,428 | 746 | 746 | 5 / 6 |
| aglaophyton | 66,016 | 3,412 | 1,760 | 1,760 | 3 / 3 |

No modifiers: authored/evaluated source vertex counts coincide. All use original geometry and palette materials, zero textures and zero decoded texture bytes. Below-100KB delivery is intentional. Dimensions, source archive bytes and exact digests are in `batch-02-result.json` and each model's metadata/candidate record.

Bundles: `assets/candidates/continuous-small-life-20261018/batch-02/r001/<ID>/`. Each contains editable blend, standalone GLB, frozen brief/config/references, bilingual metadata, transparent hero, eight fixed source QA views, source contact sheet, exact-GLB normal/near/five other angle images and nine-copy benchmark under `runtime/`, official validator report, source reopen/roundtrip and deterministic semantic rebuild reports, exact commands/logs, evidence manifest and checksums. Rebuild sources and private helper/checker copies are in `frozen/<ID>/` here.

Exact GLB SHA-256:

```text
787b7859332aebf4c8135bd2c1af4723d90ef86b5f9f9e00f2b2f8fdff4f8953  longipteryx
c15c786fbf9cb626385b10ea2a806a6203219ad8a2b1786475d625cfd2ac2d50  urasterella
1463670dda905a4c3107b5216d7e57736789da2b6548d8b5cbda49b991946a98  alienopterus
428d646967dcb99ef11dc093f6df7c58ed1d288d318f607ba91f139df0a35ef1  aglaophyton
```

All four: project private audit, source reopen and exact GLB roundtrip, separately executed semantic rebuild, Khronos **zero errors / zero warnings**, Three.js r180 parser/bounds and SwiftShader functional render passed. Nine copies were measured separately per asset; this is a neutral prop benchmark, not museum integration or physical-device performance. `local-checker-regression.txt` records 14 passing fixture tests for the batch-local checker.

The shared repository helper/checker are untouched. Frozen private copies use source-area `<1e-14 m²` / GLB cross-product-squared `<1e-28 m⁴` thresholds for millimeter-scale subjects, and the insect preview removes the historical 5cm minimum framing. The original absolute thresholds produced false failures on valid small features. The actual five collinear cap triangles in an intermediate sea-star mesh were fixed with explicit central triangle fans. The plant's intermediate section-frame twist was fixed before freeze. Helper root discovery was subsequently made portable; all exact GLB hashes stayed unchanged during final packaging/rechecks. Editable blend hashes changed on saves as expected.

`actual-reference-access.json` records what was actually opened. Reliable source text supports the basic forms, and the accepted v002 fish contact pixels were viewed locally. Several external reference images/Sketchfab views could not be downloaded because of 403 responses; do not infer fossil-image pixel inspection, a source-mesh measurement, or exhaustive anatomical verification. No external image/mesh/texture is redistributed. Color, nominal scale, soft tissue, counts and posture remain artistic within the stylized-inspired scope.

Independent reviewer entry: frozen `brief.json`, `references.json`, `candidate.json`, `evidence-manifest.json`, `contact-sheet.jpg`, and `runtime/contact-sheet.jpg` per bundle; inspect original images/GLB as needed. Maker notes are separate and must not be substituted for the reviewer's first verdict. Old turntable-schema approval is not fabricated: this brief explicitly requests eight fixed views and zero turntable frames.

Recheck from repository root:

```sh
python production/continuous-small-life-20261018/work/batch-02/verify_batch02.py
node scripts/validate_gltf.cjs assets/candidates/continuous-small-life-20261018/batch-02/r001
```

The validator rewrites reports; rerun packaging if intentionally regenerating evidence. The read-only integrity checker above verifies the frozen delivery. `--require-approved` deliberately fails while independent review is pending.

No other-batch assets, CI, global site logic, release manifests or permissions were changed. Normal pushes use `Leon Made This <8357465+s010s@users.noreply.github.com>`; parent owns serial integration and publication.
