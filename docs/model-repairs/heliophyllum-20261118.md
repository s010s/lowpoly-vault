# Heliophyllum scoped material repair

Original live GLB `100d5c5031567a50ec72ca57353dbea5cef73a6f29c728f3fb27c900592e8abd` and Blend `36fe905f2c19b5486549c08a7953ec47d4d42fffac6edb2e0651d06c946f4e14` were downloaded from the production site and matched the repository baseline. This is a local repair, not a wholesale rebuild.

The original default metallic factor 1 obscures the default-view ribbed surface. Same-model four-angle controls compared 1, 0.65 and 0. The 0.65 candidate improves rib visibility while retaining brown colour and recessed shadows; 0 was unnecessarily pale. Independent visual review accepted 0.65 as the minimal change. Shape, texture, transforms, size and orientation stay unchanged; no new anatomy/scientific or real-world scale certification is claimed.

Candidate GLB `434125cc24153ab1349846a4a6f9c8e20f1e6123e13e1e20c4212851e3d9db0c` changes only the parsed metallicFactor to 0.65. All other GLB JSON and the complete BIN match. Both original/candidate glTF validation have zero errors/warnings. Editable Blend was freshly imported from the exact candidate, saved/reopened, and compared for geometry/UV/matrix, nonempty 1024×1024 texture pixels and packed image bytes. It is not the original authoring session. Both Blender byte-count fields match the delivered file.

Fresh wheel/detail images use the current application renderer and original framing. Their real browser response bytes and the exact GLB response are checked against the paired candidate. Original and candidate two-model scoped Vite builds use the production delivery/catalog/static-route functions and generate real downloads; neither is full-site release acceptance.

Desktop 1440 and touch-emulated mobile 390 held-poster/ready-model captures preserve subject position, scale, angle and brown surface. Original finite screencasts: 39/47 frames, with 1/0 timestamp inversions; candidate: 41/47 frames, with 1/1 inversions. These inversions and finite sampling preclude a continuous zero-blank or physical-device guarantee. Small shadow/raster differences remain. Independent review accepted the scoped four-panel transition evidence; preload text disappearing is expected.

Branch integration, exact-commit CI and eventual production release are separate. No production publication is claimed.

Eight fresh lifecycle tests pass (rapid reselect, delayed response, retry, rotate/reset × both widths). Four actual candidate GLB/Blend download clicks pass exact SHA checks; original downloads also passed. Actual bound wheel/detail response hashes match. The download harness waits for initial poster readiness before choosing a model, avoiding its early-initialization test race.
