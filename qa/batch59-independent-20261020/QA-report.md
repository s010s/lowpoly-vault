# Independent full QA: batch 59 (frozen source)

**Review date:** 2026-10-20. **Reviewer:** dot, independent fresh-context review. **Scope:** one bounded, read-only review of exactly four candidate revisions. No source edits, external writes, publication, push, merge, deployment, or formal approval were performed.

## Outcome

- **glacial-erratic r002 — ACCEPT bounded stylized scope.** Coherent generic glacial-erratic decorative prop; identity, locality, age and real-world scale are not asserted. No actionable defect found in this scope.
- **gypsum-cave-flower r002 — ACCEPT bounded stylized scope.** Readable stylized gypsum-flower prop; the broad curled ribbons are an intentional simplification, not fine/crystalline fidelity. No locality, age or real-world scale asserted.
- **stalactite-group r002 — ACCEPT bounded stylized scope.** Five downward-pointed cave pendants beneath an explicit ceiling mount. The mount is the origin; the negative-Y bound is expected, not a ground-placement defect. No cave identity, locality, age or real-world scale asserted.
- **erbenochile r003 — BLOCKED.** It is a well-finished dorsal-shell teaching reconstruction only, not the whole-animal subject named in the original inventory. Primary source anatomy pixels could not be inspected with available retrieval/rendering, so eye/visor morphology is not factually signed off. The source-image gap and the scope conflict are independent blockers: obtaining Fig. 1 pixels would help review anatomy but would not cure the subject/inventory mismatch. Do not repair geometry solely to satisfy the unresolved full-organism scope without the authorized scope decision; either explicitly authorize a separately scoped dorsal-shell prop and provide/view the figure pixels, or rebuild the whole organism against primary anatomy evidence and documented uncertainty.

These are independent-review recommendations, not persisted formal acceptance. The candidate records still say `approved_for_brief=false` and leave formal approval pending. For every model, GPU and populated-scene checks are unknown/unrun, and no hardware/live/user approval is evidenced.

## Frozen source and audit inputs

Source worktree: `/tmp/lowpoly-batch59-20261020`, HEAD `330bc4aa669a1647c632a32622ce4318fd8d1b59`; clean at initial and final checks. I did not alter the worktree. Authoritative maker handoff: `production/continuous-small-life-round22-20261020/work/batch-59/handoff.json` and `HANDOFF.md`. Candidate roots are under `assets/candidates/continuous-small-life-round22-20261020/batch-59/<id>/<revision>/`.

The full frozen `static-stylized-v1` contract was reviewed. It uses exactly eight required fixed views (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`) and zero turntable frames. This is a view-plan allowance only: it does not waive source deliverables, budgets, provenance, independent stages, or approval checks. I followed the contract's key boundary that profile compatibility/record validity do not equal approval or publication authority.

### Exact artifact pins and digests

All SHA-256 values below were checked against actual local bytes; GLB pins match the supplied final pins. `source` is the candidate's `.blend` source artifact. The machine-readable record also contains per-view render hashes, dimensions, bounds, and rebuild details.

| Candidate | Frozen artifact directory | GLB SHA-256 | `.blend` SHA-256 | `candidate.json` SHA-256 | `profile-contract.json` SHA-256 | `generator.py` SHA-256 | `build-config.json` SHA-256 | `brief.json` SHA-256 | `references.json` SHA-256 |
|---|---|---|---|---|---|---|---|---|---|
| `erbenochile r003` | `assets/candidates/continuous-small-life-round22-20261020/batch-59/erbenochile/r003/` | `ec7b7fb8e84b2298a17d5ee42f0074ce97aab38eaac98a21579edc6eee59645f` | `a52027e64c87ef13109e6bb19b1d35a4f1fa024d17dbdefe31d6f8a3edab1b54` | `aafa9d7aa8240695a5431e738f9da54f9379a1e475f8edb1c4449de35612c2df` | `5d26aececea65cdce29128139854faec48ce995a7dd99b0d4e17f7449b752b8f` | `177fffe401549bc26c35585e5ac3e418eff2e6dae36d09ec592e652c397ad4ec` | `d5ff1edf529abb24b6417bc7fc12ef011ff9014dd9cbf7fa99bc87d09693fc08` | `11b11420612223f22be9ada7f7fae5fb90ebf0d01e926a039a85d7a738022136` | `270ce5acd81d12c5f171c7f00e050c56356273e17bbaef45814dd83440f2dd97` |
| `glacial-erratic r002` | `assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/` | `94bdc5b0dddd8a3925d53ded4be6191d4769cc9414d8860d9664a8170010bfcd` | `e4381e4138c48006a922e387d7437ea8425b7e2d23d4137bf99e786ce1f57f02` | `2d8e3d573930296ca990e3c754afb1135c5b94334938d252fe5a12364ea62c81` | `b34cffa1a60eb08267d00b04cbc351fc3b57478d6ddde9258c8dea566766a089` | `cc5ed645c7c04b6080bfd8e024a77599b64716774bc9a3dcdbe86111cd0eada5` | `28fed7227c3620a169a0782abe0e85e5563cdef66dd1a6d134ad8e0213964866` | `84d96a4439937d436007a3c8e390466381e1c74533b086979c1eabdef20b4e18` | `55fce1ff9558cc7d07a0912fa402e2682f83cc8030b8a1ccbedcb8c430da420c` |
| `gypsum-cave-flower r002` | `assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/` | `8ddaf4c36f2fd0dbe7c3971c27c750e8c41760954a8fb25e9e40b679c24eac2b` | `90a8c4f5a71a5cf9a90519559f312ef4da744daeed48295911460cbe3d593b9b` | `c6e95e08c99e53e69295e5684839be7c91fea0bb849120d53484a3f4d99aa1a6` | `b4f2213c41d23c6ca552b1eb59f01d50ab5769495e429391f0c75a04795bd756` | `cc5ed645c7c04b6080bfd8e024a77599b64716774bc9a3dcdbe86111cd0eada5` | `d4ae566acb2a57d6c3faefcd0de4c8bf769aa458b1b5497dbbf710ddbe06c941` | `4bee0a60bb107ec5f999ab58464f8b8175df379bd8574b2868f5c3a42fc4599a` | `ac94eddc9f19b063322e88b0f9c8a88335ebcf64acb6aec98f3a2322113ae29f` |
| `stalactite-group r002` | `assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/` | `6e2bf795d94dae162a65dd8cf0924d70e402e28dbb1c17917d622919d608fca7` | `1a56a769490486027c70f5afc4d953cfec9309efdd4232c4ef5ab17d31cc29b4` | `dbab752080622f3adb04432f576179114150cad3a0cd14eb47954261f6350806` | `c63b35f9ea943bd5efa0f7c9e83e36f0b4a14a14ff1776a8afa7bc5086c448d9` | `cc5ed645c7c04b6080bfd8e024a77599b64716774bc9a3dcdbe86111cd0eada5` | `afc5c6600f0e24daf64151c6cd6b905c3bb6b5255318ca2458420acc53248c8e` | `13f329fce348f36e674b1630d788d8cf5cbe764ad4ee9426fec983f257114234` | `0aa4604481bea2e8e093d581f13aa7d7176610b28696ed5618d565932ed4e58a` |

## Checks executed independently

- **Pins, provenance and candidate/profile integrity:** Verified exact GLB, source `.blend`, generator, config, brief, references, candidate descriptor and profile sidecar bytes against the candidate/hash records. Re-ran `scripts/validate_candidate.py --profile static-stylized-v1 --profile-contract ... --json` on all four: all records valid, profile contract pass, integrity errors none. Stored `approved_for_brief` remains false, with formal review/approval blockers intact.
- **Required visual proof:** For each pinned GLB, checked the exact eight final 512×512 images against `proof-final/render-manifest-static.json` and their per-frame SHA-256 entries; all eight actual images match the frozen manifest. Inspected actual pixel contact sheets at original tile resolution. Sheets: `/tmp/lowpoly-round22-qa59/erbenochile-eight-views-contact.png`, `/tmp/lowpoly-round22-qa59/glacial-erratic-eight-views-contact.png`, `/tmp/lowpoly-round22-qa59/gypsum-cave-flower-eight-views-contact.png`, `/tmp/lowpoly-round22-qa59/stalactite-group-eight-views-contact.png`. The per-frame hashes are retained in `independent-results.json` / `pins-and-frames.json`.
- **Technical budget and GLB audit:** Independently ran `scripts/qa_glb.py`. All four are below the limits of 14,000 triangles, 1 MB GLB, 6 materials and 30 primitives. No textures. GLB file-space dimensions (metres per exported coordinates; not claims about real object scale): Erbenochile 0.0478 × 0.0194988 × 0.0730; glacial erratic 3.5593 × 2.7287 × 2.9638; gypsum flower 0.1201 × 0.06038 × 0.1071; stalactites 2.8646 × 2.2894 × 1.6029.
- **Source reopening, counts, topology and bounds:** Opened all four `.blend` files in Blender 4.3.2 with auto-execution disabled in one process (two threads), did not save. Source triangles/materials agree with GLB. No boundary or non-manifold edges in audited mesh objects. Blender-source vs GLB bounds agree within 1e-4 m; max coordinate-size deltas were Erbenochile 1.20e-6 m, erratic 8.20e-8 m, flower 1.86e-9 m, stalactite 8.94e-8 m. Source audit has no errors. The sole warning is the stalactite low-Y check described below.
- **Official validator:** Khronos `gltf-validator` 2.0.0-dev.3.10 run on the exact four pins: 0 errors, 0 warnings, 0 infos/hints, none truncated for every GLB.
- **Runtime parse:** Independently parsed all four pins with Three.js `GLTFLoader` 0.180.0. Parse succeeds for each; mesh/triangle counts and bounds agree. This is software parsing only, not GPU proof.
- **Two queue-bound semantic rebuild reports:** Audited both actual queue-bound reports for each candidate using the independent `scripts/check_reproducibility.py` checks and cross-checked queue request/result hashes, fingerprints, success return status, generator/config argv, output record and semantic hash. All eight rebuilds match the candidate's semantic hash and byte-identical GLB. The only warning is both stalactite rebuilds' expected negative-Y extent because its frozen mount is at the ceiling. Rebuild and source/validator evidence is in `/tmp/lowpoly-round22-qa59/audits/` and summarized in `independent-results.json`.

## Visual, factual and specification findings

### erbenochile r003 — BLOCKED

The eight pixels show a clean, symmetric, low-poly dorsal shield with a broad cephalon, paired short cylindrical capped eye turrets, central axial ridge, eleven illustrative bilateral rib pairs, tapering pygidium and two swept genal spines. Mesh organization is deliberate and polished; the maker has explicitly limited this to a dorsal-shell teaching reconstruction, not a complete living animal. The turrets read as short capped posts, rather than the documented prominent, strongly curved tower eyes with an overhanging eyeshade. Without primary image pixels, I cannot validate that anatomical simplification. More importantly, the original inventory still names a whole organism. Current narrowed r003 brief cannot be counted as fulfilling it.

**Stage review:** technical pass; visual pass only as stylized dorsal-shell art; factual blocked/unknown for taxon-specific anatomical fidelity; specification pass only against the narrowed r003 brief and fail against the original whole-organism inventory; runtime_parse pass; GPU unknown/unrun; scene unknown/unrun. Formal record and approval remain pending. This is a block, not a geometric repair request: a different scope/reconstruction decision must come first.

### glacial-erratic r002 — ACCEPT bounded stylized scope

Across all views, the candidate reads as one irregular, asymmetric, faceted blue-gray boulder seated on low, uneven ochre bedrock with a pale mineral-colored stripe integrated across the boulder. Negative spaces, fracture plane and changed views preserve its single-boulder read. Stripe/rock colors are artistic; they do not establish a real boulder's proven transport or source. NPS describes erratics generically as rocks transported by glaciers over distance and dropped away from origin, often far from that origin. This supports the category-level stylization, not a specimen identity.

**Stage review:** technical pass; visual pass; factual pass only for generic erratic concept/scope; specification pass against frozen narrowed generic-prop brief; runtime_parse pass; GPU unknown/unrun; scene unknown/unrun. Formal acceptance pending.

### gypsum-cave-flower r002 — ACCEPT bounded stylized scope

All views show a small dark attachment base and six pale radial, thickened, flattened curled ribbons. The open negative spaces and asymmetrical curl/length pattern preserve a mineral-flower silhouette. The smooth broad bands are visibly stylized ribbons, not fibrous crystals or fine specimen morphology; this is a meaningful abstraction, not a factual specimen reconstruction. NPS describes cave flowers as commonly gypsum, crystal petals radiating from a common center/base and curved/flowerlike. No site, locality, age, exact specimen or physical scale is asserted.

**Stage review:** technical pass; visual pass; factual pass limited to a generic stylized gypsum cave-flower prop; specification pass against frozen narrowed prop brief; runtime_parse pass; GPU unknown/unrun; scene unknown/unrun. Formal acceptance pending.

### stalactite-group r002 — ACCEPT bounded stylized scope

The object reads consistently as five rooted, downward-tapered pendants attached to a shallow, irregular ceiling slab. Hero, reverse, front, side and rear views preserve the hierarchy of one longer, slightly offset central pendant and four shorter ones; no stalagmite or ground base is present. File-space low-Y is −2.289444 m because the explicit ceiling mount is at the origin and pendants extend down. That is the intended mounting convention, not a defect to flip. NPS describes stalactites as ceiling-hanging, icicle/carrot-like forms and notes they can be calcite or other minerals. No cave identity/site/age/scale is asserted.

**Stage review:** technical pass with expected ceiling-mount warning; visual pass; factual pass limited to generic stylized stalactite group; specification pass against frozen ceiling-mount brief; runtime_parse pass; GPU unknown/unrun; scene unknown/unrun. Formal acceptance pending.

## Erbenochile evidence gap: exact reference and access attempts

The missing primary figure is **Fig. 1(A–E)** in Richard A. Fortey & Brian D. E. Chatterton, “A Devonian Trilobite with an Eyeshade,” *Science* 301(5640), 1689 (2003), DOI [10.1126/science.1088713](https://doi.org/10.1126/science.1088713). Caption: (A) posterior view showing overhanging eyeshades, (B) lateral view, (C) dorsal view, (D) right-eye detail, and (E) eyeshade blocking overhead light. The reference is specifically needed to review tall/tower-like and curved eyes and visor extent, not to identify the existing shell as a full living organism.

Attempts and outcomes:

1. Official Science article endpoint [`https://www.science.org/doi/10.1126/science.1088713`](https://www.science.org/doi/10.1126/science.1088713): page fetch returned **403 Forbidden**; no image pixels.
2. Article PDF mirror [`https://ftp.soest.hawaii.edu/engels/Stanley/Textbook_update/Science_301/Fortey-03.pdf`](https://ftp.soest.hawaii.edu/engels/Stanley/Textbook_update/Science_301/Fortey-03.pdf): text opened; it exposes the article and Fig. 1 caption, including headshield width, but screenshot/render tool returned no image payload, so primary figure pixels were **not** visually available to this review.
3. AMNH *Trilobite Hall of Fame*, PDF page 38 Erbenochile entry: [`https://www.amnh.org/content/download/432038/6245021/file/trilobites-hall-of-fame.pdf`](https://www.amnh.org/content/download/432038/6245021/file/trilobites-hall-of-fame.pdf). PDF text opened and identifies the entry/photo, but the screenshot response supplied no pixels. It is a supplemental specimen photo source, not a substitute for Fig. 1(A–E).

Even if those pixels are supplied, the whole-organism inventory mismatch remains. To accept current geometry, the owner/coordinator must explicitly authorize a separate limited dorsal-shell educational/museum-prop scope; then review visible figure pixels for the eye/visor claims and keep the shell-only disclosure. If the work must satisfy the original whole-organism inventory, it needs a new complete-animal build and anatomy evidence for the missing body/appendage and ventral regions, with uncertain reconstruction portions explicitly labeled. Figure access alone cannot change the contractual subject scope.

## Scope boundaries, unknowns and evidence custody

The maker's supplemental concept evidence is valid but incomplete: `provider_created_at` (actual image-provider generation time) and `modeling_started_at` remain null for every asset. The observed time and pre-generator/pre-geometry freeze are recorded, but neither file modification times nor other chronology were inferred to fill the gaps; this remains a supplemental completeness limitation, not silently upgraded evidence.

For all candidates, this QA keeps the seven stages separate: **technical**, **visual**, **factual**, **specification**, **runtime_parse**, **GPU**, and **scene**. Passing static geometry/GLB checks does not prove a live hardware GPU or a populated integration scene. No formal-profile acceptance, hardware/live/user approval, or deployment evidence was found or created. Three recommendations are bounded to generic stylized props only; no named specimen, locality, geological age or real-world scale is invented.

Evidence files under `/tmp/lowpoly-round22-qa59/`:
- `independent-results.json`: exact pins, per-view frame hashes, dimensions, source-vs-GLB comparisons, profile results, runtime-parse status and rebuild checks.
- `pins-and-frames.json`: extracted hash-pinned frame records.
- `audits/`: four independent static GLB audits, four candidate/profile validations, official validator output, runtime-parse logs, source reopen report/log and eight rebuild rechecks.
- Four eight-view original-pixel contact sheets named above.

## Verified factual sources

- Fortey & Chatterton's original 2003 Science article and Fig. 1 caption (PDF mirror of the primary article): [full article PDF](https://ftp.soest.hawaii.edu/engels/Stanley/Textbook_update/Science_301/Fortey-03.pdf); official DOI landing page [returns 403 in this review](https://www.science.org/doi/10.1126/science.1088713).
- U.S. Geological Survey, *Glossary of Glacier Terminology*, erratic entry: [USGS text glossary](https://pubs.usgs.gov/of/2004/1216/text.html). It defines an erratic by glacier/iceberg transport and deposition away from origin. USGS HTML was blocked to direct fetch in this review, but search-indexed official text returned the definition; corroborating official NPS article is directly readable.
- U.S. National Park Service, [Glacial Erratics](https://www.nps.gov/articles/erratics.htm), glacier transport and deposition away from origin.
- U.S. National Park Service, [Speleothems](https://www.nps.gov/subjects/caves/speleothems.htm), stalactite orientation/composition and gypsum cave-flower radial, base-grown morphology.
