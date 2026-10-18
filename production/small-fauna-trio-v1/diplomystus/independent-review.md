# Diplomystus independent review

Exact GLB SHA-256: `9ac31f6c6290f4150dc68b2314e4610da9f95939b98720e8ae87bc39164a6f30`.

The visual and basic stylized anatomy review passes. This is an original child-friendly, static taxon-inspired prop, reviewed at 80, 160, 240 and moderate 480 px. No geometry or cosmetic revision is requested. Publication is not accepted or authorized.

| Criterion | Verdict | Evidence |
|---|---|---|
| technical-integrity | pass | Validator: zero errors/warnings. Source/export comparison: 2064 triangles and bounds match exactly; reproducible GLB bytes and semantic digest match. 103448 bytes, 4 materials, 8 primitives, 0 textures meet budgets. Free-swimming mount explains negative minimum Y. Smooth body is intentional and visually clean. |
| normal-view-recognition | pass | All source and exact-export fixed views inspected. At 80/160/240 px, deep forebody, taper, dorsal fin and forked tail remain readable; at 480 px no conspicuous detached major component, penetration or broken shading. End-on tail/median-fin collapse is expected foreshortening. |
| identity-1 | pass | Side, hero, reversehero and silhouette show elongate herring-like body, deeper anterior half and narrow caudal peduncle; does not read as a deep oval armored fish. DIP-WY Physical Characteristics supports deep-bodied form; DIP-NPS Fish Wall identifies freshwater herring. |
| identity-2 | pass | Side and hero at 240/480 px show a small dark seam rising to a raised snout; front shows both seam halves meeting at the upper tip. Dorsal edge has a restrained small scute rhythm and no head shield. DIP-WY explicitly supports upturned mouth; exact scute count/shape is an artistic simplification, not a verified specimen claim. |
| identity-3 | pass | Source/browser side, front, top and bottom show one dorsal, one anal, paired pectoral/pelvic fins, and a deeply notched two-lobed tail. Gray view preserves secondary structure. Visible joins seat into the body with no floating major parts. Fin panels are deliberately stylized and have visible edge thickness. No exact fin-ray formula claimed. |
| deliverables-and-label | pass | Final freeze.json supplies actual source/generator/config/brief/reference/GLB hashes and byte lengths; all six were independently checked against delivered bytes. Required editable source, generator/config, GLB, views, hero and stylized/static labels are present. |
| target-loader | pass | Final browser/diplomystus.json binds exact GLB hash to Three.js r180 GLTFLoader, matching bounds, 4 materials/8 primitives/0 textures, no errors or failed requests. |
| functional-render | pass | Seven browser export views plus three projected-size views inspected. Final WebGL2 report passes with ANGLE Vulkan SwiftShader. Functional software rendering only; no physical GPU performance claim. Initial favicon-only 404 report is superseded. |
| representative-scene | pass | Scene hero/top pixels inspected: three fish copies among nine props are visible. Final scene report passes, 76 calls and 31214 submitted triangles including floor. Final scene loaded entry and isolated report both bind the exact fish hash. Neutral benchmark only, no museum/coexistence or hardware throughput claim. |

## Consolidated blockers

None. All nine brief criteria pass in the reviewed scope. No asset revision is requested.

## Advisories

At 80 px the tiny mouth seam, scutes and fin rays fade naturally; the body and forked tail remain readable. At 240/480 px the mouth rises to a raised snout, while the dorsal edge stays restrained. Fins seat into the body; no accidental major detachment, join crack, flipped broad face or broken normal pattern was visible. The smooth body and ochre planar fins read as deliberate stylization.

DIP-WY directly supports the deep body and upturned mouth; DIP-NPS identifies the fish as freshwater herring. Exact fossil proportions, fin rays, scute count, color and behavior are outside this claim. A consulted museum specimen image returned 403, limiting independent specimen comparison. The finalized brief consistently specifies 480 px moderate inspection.

Final browser evidence has zero errors and failed requests; the initial favicon-only 404 report is superseded. SwiftShader establishes functional software WebGL rendering, with no physical device-performance claim.

## Inspected evidence

All eight source images (hero/reversehero/front/side/rear/top/clay/silhouette), seven export views (including bottom), three small-size export images and both scene views were opened as actual pixels. Final text and image paths with SHA-256 values, criteria, warning dispositions and source locations are in `independent-review.json`. The scene contains three fish among nine props, with 76 draw calls and 31,214 submitted triangles including the floor.

## Tail repair recheck

The maker corrected concave sheet tessellation using polygon tessellation while preserving the silhouette. New source and export hero/reversehero/side/clay views show a clean caudal notch, and all required views plus the 80/160/240/480 px and scene evidence were re-inspected without regression. Final source/export comparison has matching 2,064 triangles and bounds; the rebuild is byte-identical. All six freeze hashes and sizes were reverified. No additional revision is requested.
