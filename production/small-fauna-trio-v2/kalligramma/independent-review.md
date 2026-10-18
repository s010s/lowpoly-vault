# Kalligramma v002 independent review

Final GLB SHA-256: `6a5a15ea887312171f5ee213a7db1774459170b9f99df3ef4e9fa81e60fcd39e`. **Mandatory brief criteria pass within the stylized-inspired scope; user style acceptance remains pending.** Publication is separate.

The final browser export is coherent, with no hard visual defects found. The quieter pigment and smoother shading follow the requested direction, but this review does not certify the user will find it beautiful.

## Aesthetic comparison and residuals

Compared matched v1/v2 hero and top: v2 removes loud cream/ochre facets and raised concentric target discs, giving soft low-contrast brown marks and smoother continuous shading. This is a visible directional improvement, not proof the user likes it.

Near bilateral symmetry, broad smooth leaf/petal wings and repeated cross-vein spacing still look designed/procedural. The quieter color makes the repeated ladder-like vein structure relatively more noticeable.

Side view still has fairly thick lens-shaped wings and a bead-chain abdomen; transitions are smoother than v1 but retain separate primitive-like segment lobes. These are aesthetic residuals, not conspicuous structural failures at normal prop size.

Pigment is subdued enough to read as diffuse brown smudges rather than a distinctive eyespot at close view. The body/wing palette is compressed and can look dull olive-gray in neutral preview. This is a taste tradeoff for the user to judge.

The 128px oblique silhouette merges wing lobes and does not permit six-leg counting; top/obliques provide clearer four-wing identity. Tiny appendages are expected to disappear near 80px.

Actual wingspan is 0.108m versus nominal artistic brief 0.12m; document as approximate or reconcile if literal size is required.

## Criteria

**technical-integrity: pass** — Reviewer reran official Khronos validator on current GLB: zero errors/warnings. Inspected exact-hash source/export and reproducibility reports: 4504 triangles, 2420 exported position vertices, 3 materials/5 primitives, 150456 bytes; bounds match, deterministic rebuild byte identical. Smooth shading is intentional and flying centerline permits negative minimum height.

**normal-view-recognition: pass** — Opened all eight current source previews plus all ten exact-hash browser images. Four broad wings/body read at 80/160/240px and close views; all six angles plus underside have coherent attachments, no conspicuous broken shading, floating major parts or star-shaped UV pigment distortion. Clay retains sparse vein structure without raised target discs.

**identity-1: pass** — Four broad rounded wings/slender body visible in top and both obliques. Exact-export browser bottom directly shows three bilateral leg pairs, two antennae and central proboscis; side shows three near-side legs. Basic-inspired anatomy only.

**identity-2: pass** — Fine forward/downward central proboscis distinct from the paired antennae in front/side and source construction. A few primary and repeated cross veins are visible without a dense microgeometry mesh. This is basic-form compliance only, not fossil feeding-apparatus/venation certification.

**identity-3: pass** — Broad four-lobed wing silhouette and top view differ clearly from a narrow leaf-outline hangingfly. Muted irregular pigment replaces v1 concentric raised targets; original color/vein arrangement is within artistic scope.

**deliverables-and-label: pass** — Editable source, deterministic generator/config, standalone GLB, original 256px pigment map, hero and complete six-angle source evidence plus clay/silhouette present. Brief now permits one texture; config labels pigment mapping. Metadata labels static inspired art. Seven freeze entries and all eighteen manifest frames verified against actual bytes; final-validation-r2 final-generator rebuild is byte-identical.

**target-loader: pass** — Exact-hash browser report matches reviewed final GLB. Three.js180, matching bounds, 3 materials/5 primitives/1 texture; no errors or failed requests.

**functional-render: pass** — Opened ten exact-hash browser PNGs: seven 480px angle/underside views and 80/160/240px top views. Declared ANGLE Vulkan SwiftShader WebGL2, 5 calls/4504 triangles. Functional software rendering only, not physical GPU/device performance.

**representative-scene: pass** — Opened exact-hash neutral benchmark hero/top. Scene report explicitly records final Kalligramma hash, three copies among nine total asset instances, 98 calls/80008 triangles. Insect silhouette remains recognizable at small relative size. No physical GPU, museum integration or scientific coexistence claim.

**scientific-species-and-venation-fidelity: unknown** — Nonblocking outside narrowed inspired-art scope. KAL-2025 primary abstract read: species/redescription depends on detailed venation. KAL-2016 full text blocked by reCAPTCHA. No inaccessible fossil figure pixels claimed inspected; reference ledger IV-LACEWINGS supports family context only, not all required feature claims.

## Evidence and boundaries

All 7 frozen file hashes and all 18 image-manifest hashes match actual bytes; manifest and individual/scene runtime identify reviewed current GLB.

- `assets/candidates/small-fauna-trio-v2/kalligramma/preview-hero.png`
- `assets/candidates/small-fauna-trio-v2/kalligramma/preview-reversehero.png`
- `assets/candidates/small-fauna-trio-v2/kalligramma/preview-front.png`
- `assets/candidates/small-fauna-trio-v2/kalligramma/preview-side.png`
- `assets/candidates/small-fauna-trio-v2/kalligramma/preview-rear.png`
- `assets/candidates/small-fauna-trio-v2/kalligramma/preview-top.png`
- `assets/candidates/small-fauna-trio-v2/kalligramma/preview-clay.png`
- `assets/candidates/small-fauna-trio-v2/kalligramma/preview-silhouette.png`
- `assets/candidates/small-fauna-trio-v1/kalligramma/preview-hero.png`
- `assets/candidates/small-fauna-trio-v1/kalligramma/preview-top.png`
- `assets/candidates/small-fauna-trio-v1/kalligramma/preview-side.png`
- `assets/candidates/small-fauna-trio-v1/kalligramma/preview-clay.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-hero.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-reversehero.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-front.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-side.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-rear.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-top.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-bottom.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-80px.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-160px.png`
- `qa/small-fauna-trio-v2/browser/kalligramma-240px.png`
- `qa/small-fauna-trio-v2/browser/scene-hero.png`
- `qa/small-fauna-trio-v2/browser/scene-top.png`

All exact input/image hashes and inspected report filenames are recorded in `independent-review.json`. Official validator was rerun by the reviewer with zero errors and zero warnings. Source/export and final-generator rebuild reports were inspected. Runtime uses SwiftShader software WebGL; no physical GPU performance claim is made.

Scientific limits: [KAL-2025 abstract](https://mapress.com/zt/article/view/zootaxa.5659.1.4) was accessible; [KAL-2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4760178/) was blocked by reCAPTCHA, so no fossil figure pixels were claimed inspected. Exact species, color and vein fidelity remain outside this brief.

No asset edits were made. No further cosmetic repair is requested; the remaining aesthetic judgment belongs to the user.
