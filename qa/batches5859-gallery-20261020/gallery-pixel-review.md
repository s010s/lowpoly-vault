# Independent gallery detail/wheel review: batches 58/59

Outcome: PASS for exactly seven new static gallery pairs (14 actual PNGs). No new-seven blocker. This is not an all-201, formal, physical-GPU, interaction, or live-publication approval.

Reviewed source head: `ffb40574ea5ef4840d43fb4ec74879d25ec3d9af`. Baseline: `7d108d1bb8043925e3cc8efa1e4a2c53b699be6c`.
Capture run `39402013074`, head `32656650e7a0276de0787fceb4dcddf15425ff33`, artifact `12255870323`.
ZIP: 1686268 bytes, SHA-256 `781815071b94db9804c42977ef4586d31c04894094803495e8f578a5108792c6`.
Receipt SHA-256: `fdf70d9ad365351649580e6531944a44bbb98c78c8cb99ce6e06b55ed27d4462`.
Recipe v3 SHA-256: `20565eab93aa3e8d17f47665c1a2221f0cff805d7a49ab8e373d74adae07549b`; PreviewRenderer.poster, Chromium 141.0.7390.37, receipt-bound ANGLE SwiftShader.

## Independent scope and evidence

All 14 original images were directly viewed. ZIP/extraction, PNG seals, source bytes, shared recipe, input keys, dimensions, wheel framing and current source import were independently checked. Detail images are 512 x 512; wheel images are 768 x 432. All are nonblank RGBA, have transparent corners, and have opaque model bounds strictly inside the frame. Finite wheel specs use azimuth 42, aspect 16:9 and elevations 23.3 or 40.

Parent card QA SHA-256 `515434e55d62dae9d65996894bb4d438fc4650ecc1a4d33f999018e9fa25c5e2` was reused, not re-reviewed. Each exact source GLB and accepted card byte hash was checked. Visual consistency across the new pair supports material/identity continuity; this does not assert pixel equality across renderer types.

## Per-asset findings

### calamophyton r001: PASS

Slender brown trunk and sparse branching greenish twig sprays are recognizable in both views. Trunk foot and branch tips remain fully within the frame.
Limit: The fine branch silhouette is intentionally sparse; a static image does not demonstrate branch connectivity at every occluded point.
Source GLB SHA-256: `005c21c5dfa735762fcfc65387075701ba3e24a915316e6e7c1a59a096362815`.
Poster input SHA-256: `ccac7ab61c6639f3b7f972c6e2743be304b94557b2087dbdcead994dd873a3db`.
- detail: `gallery/posters/calamophyton.png`; 136251 bytes; SHA-256 `46052b29c520cd1305e631bc62c9334d2abe13ec61098c032e7277a2f9bc1ad6`; opaque >=250 bounds [143, 77, 359, 406] (exclusive right/bottom).
- wheel: `gallery/posters/calamophyton-wheel.png`; 125625 bytes; SHA-256 `b57e2548593190aaa467ee689ec6cbc9ad80ce6031778e6201b1eed0564c1f04`; opaque >=250 bounds [270, 54, 489, 380] (exclusive right/bottom).

### perspicaris r002: PASS

Tan paired oval valves, dark stalk eyes and antennae, paired swimming flaps, and forked terminal tail read as the same bounded organism in both views. The 40-degree wheel view exposes the body without cutting appendages.
Limit: Some paired limbs and the far valve overlap naturally at these viewpoints; hidden anatomy and motion are not established.
Source GLB SHA-256: `ec95315cac17288508b02d7f3901e9a6a8e8ef464e46b44f460bba049488d35c`.
Poster input SHA-256: `3af6d55202b89ae4f217cad8e4e53b499a737bc4cada544eb426593a881ace71`.
- detail: `gallery/posters/perspicaris.png`; 91655 bytes; SHA-256 `bd510fa73198416ffd1ea63cd3c24d6ba40f901590113b69fadb689d9e1f0ec6`; opaque >=250 bounds [45, 201, 401, 376] (exclusive right/bottom).
- wheel: `gallery/posters/perspicaris-wheel.png`; 137881 bytes; SHA-256 `8a761441085c5acce7ebbe11e025790f555a31ae87c4c1c3cdd4690cfec65ad6`; opaque >=250 bounds [150, 59, 554, 363] (exclusive right/bottom).

### barchan-dune r001: PASS

A pale sand-colored crescent body and two tapering horns are legible in both views. Both tips are intact; the higher wheel viewpoint preserves the crescent silhouette.
Limit: Pale preset lighting gives low internal contrast, especially on the detail image. This is nonblocking at the supplied size; neither wind direction nor terrain-scale behavior is tested.
Source GLB SHA-256: `4b4580c6ed599b80865ebe9a4e506dc3d4a770077fa5f5be3ec099d3ab8a2543`.
Poster input SHA-256: `059bef2fcbd8b9a0334a7390d0c27f6b83b87ee8f78a58cb31beb23ecd3ff8c4`.
- detail: `gallery/posters/barchan-dune.png`; 97709 bytes; SHA-256 `1da9fe94dd2e8bebd6e885bee8e541a03e1eb7e69f8a9d8f838c66289c4d4ed4`; opaque >=250 bounds [45, 213, 384, 398] (exclusive right/bottom).
- wheel: `gallery/posters/barchan-dune-wheel.png`; 162271 bytes; SHA-256 `c2a45efb4810666ea081dda5df7abc1228e95cf249d7c0588bdee15c64f8d588`; opaque >=250 bounds [137, 92, 526, 362] (exclusive right/bottom).

### current-ripple-surface r001: PASS

A tan rectangular sediment slab carries a readable train of parallel asymmetric ridges. The end profiles and higher wheel view reveal the ripple relief; all slab corners remain in frame.
Limit: Fine relief has intentionally subdued tonal contrast. No hydrodynamic simulation, scale validation, or live scene interaction is inferred.
Source GLB SHA-256: `2bdae5b8730c661fe9817df41baa7e12ea5b0f91c78a245f4f13eedffcae640d`.
Poster input SHA-256: `9d08318b9e14e492853d9d233a425c1981ec08a58235c434d22e93f56efec8cd`.
- detail: `gallery/posters/current-ripple-surface.png`; 66175 bytes; SHA-256 `4e458f85b338528fbe5312c26f5263ab08526a28b28053463b6e389f2789a1c7`; opaque >=250 bounds [39, 184, 484, 390] (exclusive right/bottom).
- wheel: `gallery/posters/current-ripple-surface-wheel.png`; 118930 bytes; SHA-256 `54fc041ab639778a976f1c11b003b878d9c132915fe2e09c1391317c14437bdb`; opaque >=250 bounds [147, 50, 634, 387] (exclusive right/bottom).

### glacial-erratic r002: PASS

A blue-gray faceted boulder with a pale cross-cutting vein sits on an ochre support slab. Shape, vein and support colors continue coherently across detail and wheel; no face or base is clipped.
Limit: Viewpoint occludes the rear boulder surface. A static presentation does not prove geologic provenance or contact behavior.
Source GLB SHA-256: `94bdc5b0dddd8a3925d53ded4be6191d4769cc9414d8860d9664a8170010bfcd`.
Poster input SHA-256: `785185c2c02b1524c4e0e3512676fbfdfea716ac0293684cfaf33fdfdd31b2ae`.
- detail: `gallery/posters/glacial-erratic.png`; 83256 bytes; SHA-256 `0a436ec7c1224c31e70578924cf99a2f217d041e6f4e5822ba4f8d618e03a6cb`; opaque >=250 bounds [129, 131, 394, 421] (exclusive right/bottom).
- wheel: `gallery/posters/glacial-erratic-wheel.png`; 96897 bytes; SHA-256 `553f46ee8f9d560b39da9dfd4d32702b76e1588393d077840ea6164c99e46e2f`; opaque >=250 bounds [234, 43, 545, 383] (exclusive right/bottom).

### gypsum-cave-flower r002: PASS

Off-white curled ribbon-like radial petals rise from a small brown rock base. The large upper curl, lateral curls and negative spaces are visible and fully in frame in both views.
Limit: The dense center and rear curls overlap naturally. The review does not certify every hidden ribbon junction or mineral growth accuracy.
Source GLB SHA-256: `8ddaf4c36f2fd0dbe7c3971c27c750e8c41760954a8fb25e9e40b679c24eac2b`.
Poster input SHA-256: `60880883d6b22c3be5cf843db9afea32fa12fa86b4a5718f836c1b34989b1f74`.
- detail: `gallery/posters/gypsum-cave-flower.png`; 139402 bytes; SHA-256 `76438622c94fa43e2b5c51fe3c8819a6d6a06853e7bb6af6e4d5b40ac894c34f`; opaque >=250 bounds [79, 149, 404, 354] (exclusive right/bottom).
- wheel: `gallery/posters/gypsum-cave-flower-wheel.png`; 208686 bytes; SHA-256 `b58ae00a04d4f0cac67476491a144362356b89a4f8ccccdbe1c70c3db2dbf279`; opaque >=250 bounds [109, 41, 620, 365] (exclusive right/bottom).

### stalactite-group r002: PASS

Ochre ceiling slab supports downward-pointing hanging pendants in both views. The long central tip is intact. The slab remains above the pendants, not flipped into floor-standing stalagmites.
Limit: Several pendants are viewpoint-occluded. A soft preview support/shadow plane is present, but is not a cave floor or evidence of an installed scene. Ceiling-mounted intent is preserved; no physical hanging/load or scene placement test is claimed.
Source GLB SHA-256: `6e2bf795d94dae162a65dd8cf0924d70e402e28dbb1c17917d622919d608fca7`.
Poster input SHA-256: `2fb8f10f49f43b2cb2806439b8d17bdf7d74f5c40c88533256577166a584140f`.
- detail: `gallery/posters/stalactite-group.png`; 114115 bytes; SHA-256 `276ea2aa156c790ed9dfcb60a85e2d33fc2a95f5ac6813f18a025bfa05edab05`; opaque >=250 bounds [134, 102, 423, 371] (exclusive right/bottom).
- wheel: `gallery/posters/stalactite-group-wheel.png`; 118123 bytes; SHA-256 `7af2a527018d6c930aa39f47a43dfe3c653b0d847322c793a04175865aadbd61`; opaque >=250 bounds [228, 45, 600, 390] (exclusive right/bottom).

## Preservation and inherited limitation

All 194 prior manifest asset objects and poster rows are unchanged. All 399 prior resource seals and their actual bytes are unchanged, including 388 old detail/wheel PNGs. The golden approval file is unchanged. Only seven poster rows and 14 PNGs are added.

The untouched 194-model base has 186 valid input seals and eight stale; the candidate 201-model preparation has 193 valid and the same eight stale. The seven new inputs are all valid. Inherited IDs: burgessia, chimerarachne, dunbaria, emeraldella, longirostravis, sanctacaris, sapeornis, tuzoia.

Do not claim complete gallery coverage for this 201 preparation, repair/re-sign old seals under this review, or replace the separately validated 217 baseline. Parent integration must preserve that validated baseline, append these seven, and rerun complete-gallery and final publication checks for 224.

Pale dune/ripple internal contrast and naturally occluded anatomy/branches are nonblocking within these static viewpoints. Low-alpha support-shadow RGB can look noisy in raw transparency viewers, but light gallery-background composition is clean. Soft shadows near canvas edges are not clipped model geometry. The stalactite support/shadow display is not a cave floor or scene-placement proof.

The immutable capture receipt keeps its producer-time independent review status pending; this separate report provides scoped independent pixel acceptance. Formal acceptance remains BLOCKED. No physical-GPU, target-scene, wheel interaction, final CI, main merge or live proof is asserted.

## Deliverables

Structured full report: `/tmp/batches5859-independent-review/independent-gallery-review.json`
Structured report SHA-256: `cd69da156831d50c7391f35d2f157c74ce5266ca2c5fb77a8313752ce2df4946`
Machine artifact/pixel audit: `/tmp/batches5859-independent-review/gallery-pairs-machine-audit.json`
Independent import/preservation audit: `/tmp/batches5859-independent-review/gallery-import-audit.json`

No repository edits or remote actions were performed by this reviewer.
