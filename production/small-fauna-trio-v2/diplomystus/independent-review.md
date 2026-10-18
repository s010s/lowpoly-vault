# Independent review — Diplomystus v002

Decision: **passes required brief gates with aesthetic advisories**. Remaining hard blockers: **none**. User acceptance: **pending**.

Final reviewed GLB SHA-256: `36f382a00d8f93c0970d5cc9fef34a0ac4099cf9eec7edd0ce9f3f4a5f54cbe8`. Exact inspected filenames and hashes are recorded in the JSON companion.

The new fish visibly responds to “更自然精致：比例可信，低多边形但衔接柔和”: continuous rounded head/body volume and a tapered caudal mass replace v001's sharper segmented construction. The smaller dark eye, muted silver-blue fins and gradual dorsal color reduce toy-like contrast. This visible improvement does not establish user acceptance or benchmark beauty. V001 comparison used actual hero/side pixels only.

## Hard-defect recheck

The initial export `6d92c040…` had a background wedge under the rear dorsal-fin base in source and browser side views. The maker inset dorsal and anal root endpoints. All eight repaired source diagnostics and ten refreshed browser views were reopened against the final hash above: the rear dorsal base now meets the back, and no conspicuous new attachment or export-shading defect was observed. **FISH-H1 resolved.**

The zero-texture/palette-only record mismatch was corrected: the current brief allows one original pigment map and the config names the pigment-mapped profile. The final freeze's source/generator/config/brief/reference/helper hashes were independently compared with actual files. **FISH-S1 resolved.**

## Residual aesthetic advisories

- The broad rounded chin and drawn V-shaped mouth remain schematic from the front. The small upturned profile is present, but the mouth has limited anatomical volume.
- Paired fins end as short, blunt polygonal paddles. Dorsal and tail membranes retain rigid fan outlines, slight puckering and embossed-looking rays.
- The calmer pigment has a uniform repeated scale rhythm. Most small detail disappears at 80px, where fish/tail silhouette carries recognition.
- The mostly straight, symmetric body has limited natural liveliness. These are advisory simplifications under the hard-defects-only scope, not claims that the user's aesthetic concerns are settled.

## Criterion verdicts

| Criterion | Status | Evidence |
|---|---|---|
| technical-integrity | pass | Existing source/export and Khronos reports match exact hash: 3424 triangles, 1834 POSITION vertices, 6 materials, 7 primitives, 93752 bytes; zero validator errors/warnings. Source bounds round trip exactly; negative minimum height is intentional free-swimming mount. Numeric QA does not certify intersections. |
| normal-view-recognition | pass | Refreshed source and exact-export browser side/reversehero show dorsal basal edge seated continuously in back; original background wedge resolved. Fish silhouette, fins and forked tail read; no conspicuous detached major parts, accidental penetration or broken export shading observed across refreshed views. Residual style advisories retained. |
| identity-1 | pass | Deeper forebody and continuous taper to narrow caudal peduncle visibly satisfy the broad stylized herring-like obligation; exact fossil proportions are not certified. |
| identity-2 | pass | Small lip rises to the snout apex; dorsal scutes are restrained, mostly near the front of the dorsal ridge. Mouth remains a schematic drawn V in front view; advisory for naturalism. |
| identity-3 | pass | Dorsal, anal, paired fins and forked caudal fin are organized and distinguishable in side/clay/top/bottom views. Attachment defect is tracked separately; no duplicated deep oval Dapedium body. |
| deliverables-and-label | pass | Source, deterministic generator/config, standalone embedded-map GLB and eight source diagnostics exist. Current brief permits one original pigment map; current config matches. Final freeze source/generator/config/brief/reference/helper hashes independently matched actual files. Labels state stylized-inspired and static; user acceptance remains pending. |
| target-loader | pass | Three.js r180 metadata loads exact hash; bounds/counts match; no errors recorded. |
| functional-render | pass | Actual full-angle browser pixels inspected; SwiftShader WebGL2 functional software rendering, not physical-device performance. |
| representative-scene | pass | Actual neutral scene hero/top inspected, 3 visible fish among 9 subject copies; scene metadata includes exact fish hash, 98 calls and 80008 scene triangles. Functional simple benchmark only, no museum/ecological or physical-device claim. |

The museum source's Physical Characteristics section supports a deep body and upturned mouth ([DIP-WY](https://nhmofwyoming.org/blog/diplomystus-a-fossil-fish-of-the-green-river-formation), independently reopened 2026-10-18). This review checks a named-taxon-inspired stylized prop, not exact fossil proportions, fin/scute measurements or scientific reconstruction.

Khronos reports zero errors/warnings. The exact export has 3,424 triangles, 1,834 POSITION vertices, six materials, seven primitives and 93,752 bytes. Final source/export bounds match; final generator rebuild is byte-identical. Browser evidence uses Three.js r180 on SwiftShader WebGL2. Neutral nine-subject scene hero/top visibly contain three fish, with 98 calls/80,008 scene triangles. This establishes functional software rendering only; technical success does not establish beauty or user acceptance.

All eight source diagnostic images, original pigment map, ten fish browser views (including 80/160/240px), two neutral scene images and v001 actual hero/side images were inspected. Full paths and hashes are in the JSON companion. No alternate-key/wireframe images were supplied, so direct inspection of those views remains unavailable. No physical GPU or museum performance claim is made. Re-export requires hash-bound recheck.
