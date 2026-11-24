# Urasterella: retain original assets

Baseline: `d0d38f94b920a1972cbe09bb5f4d9abcf7bffd51`. Exact GLB: `174e62ce62eb2cd2b47c44e3611bf856710a800002f96cd38102deb5a73d79e3` (2,357,996 bytes, 32,999 triangles).

The original GLB, packed editable Blend and matching wheel/detail posters were checked against current Git/manifest identities. The Blend reopened with 22,667 vertices, 32,999 polygons, one UV layer and a packed 1024×1024 image. It is the existing accepted-GLB-derived editable file, not the original generation project. Existing scoped artistic acceptance is retained; this review is not a new original-input or scientific certification.

Nine views of the actual model in the current compiled renderer preserve five continuous tapered arms and readable granular margins. The brown upper surface is readable in the normal display. The underside is dark; a same-camera unlit-baseColor diagnostic remained dark, so this is not attributed solely to missing illumination. Temporarily setting metallic=0 washed the whole upper surface toward cream. Neither that colour change nor any geometry, orientation or poster replacement was adopted. No demonstrated defect currently justifies regenerating the model. Dark underside detail and authored-scale uncertainty remain limitations, not a blanket scientific pass.

## Historical evidence retained

The exact-version historical record was read rather than treating an empty new checklist as no previous review. The November 6 scoped whole-artistic acceptance used the original input contract and four hash-checked reference images; it did not recover the independent original prompt. Earlier concerns about dark underside detail and irregular arm/central-underbody shape remain historical observations, not an automatic remake decision. The November 15 record also reports an actual RAW archive integrity check with the embedded GLB matching this production hash and a four-image TRELLIS execution record; input PNG bytes were not newly verified there. This pass does not re-download or extend that provenance verification, and does not relabel the chain wholly missing. The prior one-view offscreen brown-surface check was not web or mobile acceptance; the runtime results below are new.

## Browser checks

The real unchanged Vite source and normal catalog/delivery/static-route functions built a three-model local fixture (Urasterella plus two switching anchors), not the full release. Desktop 1440×1000 and touch-emulated mobile 390×844 returned the exact model bytes with HTTP 200 and reached ready without page errors.

Handoff capture: 30 desktop and 54 mobile finite CDP samples, with 1/2 timestamp inversions. Comparing timestamps to the settled-poster interaction event leaves 18/14 sampled images with model features present. No corresponding blank-model flash was observed in those samples. Dark-feature poster/model bounding-box edges differ by at most one pixel; this is not a complete silhouette measurement. Approximate loader-excluded dark-intersection mean absolute channel differences were 6.77/10.57, so the poster and rendered model are not pixel-identical. Shadow/edge sampling differences are retained.

The existing `qa/repair-integration/integrated-browser-regression.mjs`, run with `QA_MODEL_IDS=urasterella`, passed eight cases: two viewports × rapid reselection, cancellation after switching away, visible retry after controlled failure, and drag then Reset. Retry issued two requests. Reset waited for the real animation endpoint; camera/target tolerance remained `1e-4` and quaternion `1e-7`. These cases are specific to this model, not inherited from other model runs. Cancellation is not successful stale delivery, and mouse drag in a touch-emulated viewport is not native multitouch.

No asset bytes or shared rendering code are changed. Integration CI, independent scoped review and branch readback must accompany final completion; deployment and physical-device checks remain separate. This document does not declare the entire inventory accepted or the model newly published.
