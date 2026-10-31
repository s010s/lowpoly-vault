# 36 accepted creature revisions — 2026-10-31

Updates 36 existing IDs in one batch; the catalog remains 752 ordered IDs. Three locally modified candidates (Parasaurolophus, Inostrancevia and Quetzalcoatlus) are adopted. Nine previously held candidates retain their original geometry under the later general-display review. The remaining 24 retain their conditional source acceptance. Historical anatomy HOLD findings are preserved; this is not scientific certification or a claim that all 12 were repaired.

The stable `gastornis` URL now displays **Diatryma gigantea**, following the retained taxonomic correction; no duplicate species is added. The first five revisions released in PR86 and the loading work in PR87 remain unchanged.

## Geometry and delivery

The exact accepted source hashes and final hashes are mapped in [integration-ledger.json](integration-ledger.json). Only root transforms add uniform authored scale, Y-axis orientation and a grounded, horizontally centered origin. All binary buffers, geometry, UV, embedded image bytes and material definitions are unchanged. Existing maximum authored dimensions are retained; several assets intentionally use approximately 1 m display envelopes, so these are not life-size or specimen measurements.

Editable sources are new clean imports of the exact final GLBs. Blender 4.3.2 independently reopened each file; another fresh GLB import matched saved vertex/face/UV/material-slot/image/matrix data. Earlier authoring history, original files and review evidence remain in private recovery storage. Unchanged source reviews retain their own scope; the integration checks do not upgrade anatomical accuracy.

The 36 GLBs total **200,322,776 bytes** (200.323 decimal MB). They are requested individually. Poster images, shared application code and optional Blender/ZIP downloads are separate payloads. No new texture compression or geometry reduction was applied. Pakicetus, Beelzebufo and Deinocheirus exceed 100k triangles; a hard 80k limit is not claimed. Previously rejected reduction trials were not repeated.

## Evidence

- [Catalog overlay](evidence/catalog-overlay.json): 36 replacements, 716 untouched raw manifest rows, 72 source-bound posters; historical resource entries retained.
- [Exact capture identities](evidence/capture-identities.json): current final-GLB Chromium/SwiftShader wheel images, with frame bounds checked and all 36 whole-animal views inspected.
- [Source pair reopen](evidence/source-reopen.json), [fresh GLB versus reopened Blend](evidence/source-equality.json).
- [Khronos format validation](evidence/format-validation.json): all 36 zero errors; each retains the source tangent-generation warning. Identity orientation matrices may also produce informational notices.
- [Synthetic network and interaction checks](evidence/network-summary.json): current built-site delivery, selected-model-only requests, orbit/zoom/reset and separate network accounting.
- [Checks and limits](evidence/checks.json).

The homepage first-paint CSS fix is restored together with the reviewed five-document creature Skill update. The Skill also records pragmatic whole-animal acceptance of small digit differences, retention of historical caveats, and reverting low-value local repairs. No Meshy calls, credit purchases, user Mac access or permission/security-setting changes occur in this integration.

## Selected candidates

| Stable ID | Adopted candidate | Historical source status | Triangles |
| --- | --- | --- | ---: |
| pakicetus | pass_with_limits | PASS_WITH_LIMITS | 157,440 |
| beelzebufo | pass_with_limits | PASS_WITH_LIMITS | 102,937 |
| bothriolepis | pass_with_limits | PASS_WITH_LIMITS | 82,425 |
| diictodon | pass_with_limits | PASS_WITH_LIMITS | 83,075 |
| arctodus | pass_with_limits | PASS_WITH_LIMITS | 83,453 |
| moeritherium | pass_with_limits | PASS_WITH_LIMITS | 82,952 |
| basilosaurus | pass_with_limits | PASS_WITH_LIMITS | 81,275 |
| shonisaurus | pass_with_limits | PASS_WITH_LIMITS | 80,632 |
| zygomaturus | pass_with_limits | PASS_WITH_LIMITS | 82,829 |
| protoceratops | pass_with_limits | PASS_WITH_LIMITS | 82,767 |
| deinosuchus | pass_with_limits | PASS_WITH_LIMITS | 83,381 |
| cladoselache | pass_with_limits | PASS_WITH_LIMITS | 83,686 |
| gastornis | pass_with_limits | PASS_WITH_LIMITS | 83,369 |
| placerias | pass_with_limits | PASS_WITH_LIMITS | 83,444 |
| estemmenosuchus | pass_with_limits | PASS_WITH_LIMITS | 83,003 |
| deinocheirus | original_with_caveat | ANATOMY_HOLD | 208,274 |
| quetzalcoatlus | modified_with_limits | ANATOMY_HOLD | 82,000 |
| inostrancevia | modified_with_limits | ANATOMY_HOLD | 82,873 |
| megatherium | original_with_caveat | ANATOMY_HOLD | 83,857 |
| parasaurolophus | modified_with_limits | ANATOMY_HOLD | 82,777 |
| glyptodon | original_with_caveat | ANATOMY_HOLD | 83,319 |
| diplocaulus | original_with_caveat | ANATOMY_HOLD | 82,700 |
| deinotherium | pass_with_limits | PASS_WITH_LIMITS | 83,098 |
| chalicotherium | original_with_caveat | ANATOMY_HOLD | 83,561 |
| cynognathus | original_with_caveat | ANATOMY_HOLD | 83,008 |
| henodus | pass_with_limits | PASS_WITH_LIMITS | 82,312 |
| mosasaurus | pass_with_limits | PASS_WITH_LIMITS | 83,501 |
| mixosaurus | pass_with_limits | PASS_WITH_LIMITS | 83,954 |
| toxodon | original_with_caveat | ANATOMY_HOLD | 82,709 |
| castoroides | original_with_caveat | ANATOMY_HOLD | 82,902 |
| metoposaurus | original_with_caveat | ANATOMY_HOLD | 82,356 |
| pliosaurus | pass_with_limits | PASS_WITH_LIMITS | 83,089 |
| ichthyosaurus | pass_with_limits | PASS_WITH_LIMITS | 83,924 |
| ophthalmosaurus | pass_with_limits | PASS_WITH_LIMITS | 83,803 |
| stenopterygius | pass_with_limits | PASS_WITH_LIMITS | 83,797 |
| tylosaurus | pass_with_limits | PASS_WITH_LIMITS | 83,696 |

## Validation limits

These are static display props. No animation/deformation, all-viewpoint anatomical review, physical-device or other-browser performance certification is made. Source colours and soft tissues remain artistic. Local browser timings use Cloud loopback, CDP bandwidth/latency emulation and uncompressed HTTP; they are not real CDN predictions or GPU-memory measurements. Public-site access from this Cloud executor is denied by network policy (`CONNECT 403`); post-deployment HTTP readback is performed by the existing GitHub Actions release workflow and recorded as such, separately from the local browser test.
