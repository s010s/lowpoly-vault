# Bosworthia scoped live-model repair

Baseline `95ddc59e2a0aa728cf4618ca97b7880eeb0ee173`. Freshly downloaded public production GLB, Blend and both posters matched the Git checkout byte-for-byte. Original GLB: `248774e29348d0081f28167883857bdd9f719457c63c18ebc67134d65312bab1`.

## Evidence-led repair, not reconstruction

The asset is a stylized Bosworthia-inspired preserved-thallus slab fragment, not a living three-dimensional organism reconstruction. Original-lit / temporary metallic-0 / baseColor-unlit four-angle comparison showed two original angles obscuring even the orange educational thallus motif. Independent coordinator review confirmed that metallic 0 restores readable slab facets and motif boundaries while retaining shadows. Original slab geometry, painted motif, topology, UV, texture, authored scale and pose are unchanged. Original artistic colour is the preservation target; no independent new colour reference or specimen/biological-scale certification.

Candidate GLB `aa048a068274f93e1a6fa5b2a29b11ca049782edd937fdced04f7964450f55d3` changes only metallicFactor from default 1 to 0. The rest of JSON and entire BIN payload match exactly. Blender delivery is newly derived from this precise candidate, packed/saved/reopened and compared against GLB for geometry/UV/matrix and nonempty decoded/packed image fingerprints; not the original generation session. Texture: 1024×1024, 4,194,304 channel values, 820,852 packed bytes. Original and candidate validators: zero errors and warnings.

Wheel/detail PNGs come from the actual candidate under the current PreviewRenderer policy, with explicit source binding and public-file hashes. No global viewer edits. Initial diagnostic overrides were memory-only and are distinct from this actual candidate and its fresh tests.

## Acceptance scope

Original and repaired versions each receive real scoped Vite builds using production delivery/catalog/routes, official sandbox-enabled Chromium, desktop 1440×1000 and emulated touch/mobile 390×844. Tests include delayed GLB response poster→3D evidence, rapid-reselect, late-response, retry, rotation/reset, actual GLB/Blend download button bytes and real poster HTTP body hashes. Focused test verifies source/poster identity, generated ZIP/attribution, and isolation of all other 938 entries.

Final frame counts/inversions and independent review are recorded in SUMMARY.json. Finite samples and emulated touch are not all-frame/real-device certification. Full integrated build, exact remote-commit CI and release remain coordinator-owned and pending. No PR, push, merge or deployment by this task.

Final independent review passed desktop/mobile endpoint outline, placement, scale, default pose and orange-brown motif continuity, limited to 1440/390 samples. Final handoff: desktop 36 and mobile 47 frames, no timestamp inversions. Eight interaction cases and four actual downloads passed. First candidate download process stalled without completion output and was interrupted; a bounded diagnostic rerun passed unchanged bytes. Cause of the first stall is unknown, not silently classified as a product fix.
