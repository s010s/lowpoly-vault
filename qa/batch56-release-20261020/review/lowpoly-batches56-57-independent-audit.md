# Independent candidate audit: small-life batches 56–57

Date: 2026-10-20 (UTC)  
Scope: read-only audit of the pinned candidate commits and their exact selected outputs. This report is local only. No candidate source, frozen brief, old revision, approval field, publication state, remote branch, PR, merge, or deployment was changed.

## Scope and disposition

- Batch 56: `candidate/small-life-batch56-concept-20261020`, commit `5485316a065c2e63e64f7b9f7087b49eb9f1afda`.
- Batch 57: `candidate/small-life-batch57-concept-20261020`, commit `c49dded6cbfc89429800933d39f8a0b1c2b3db81`.
- Both handoffs and `handoff.json` were read. The commit refs matched the requested SHAs. The eight selected GLBs were independently hashed; byte lengths and SHA-256 values matched the handoffs.
- Recommendation: hold both batches from formal independent acceptance pending two narrow, maker-side visual corrections: Cycadeoidea’s four pockets vs the frozen brief’s three, and Quatsinoporites’ overly regular pore grid. This is not a blanket technical failure. The remaining six candidates are provisionally acceptable on the limited visual/spec scope inspected, subject to all formal gates remaining pending. Do not amend frozen briefs or overwrite old revisions to resolve the issues.

## Fresh checks I executed

All checks below were run against the exact selected candidate files materialized from the pinned commits under `/tmp/lowpoly-round21-independent-20261020/`.

1. Current `scripts/validate_candidate.py`, profile `static-stylized-v1`: all 8 returned `valid: true`, no errors, profile contract pass. Candidate records still correctly show `approved_for_brief: false`; no approval was inferred. The legacy profile still reports its unrelated turntable-frame requirement; that is not a failure of this explicitly static eight-view profile.
2. Current `scripts/qa_glb.py`, budget caps 14,000 triangles / 6 materials / 30 primitives: all 8 `status=pass`, zero errors and warnings. Results are in `/tmp/round21-qa-glb/`.
3. Current Blender 4.3.2 source-vs-export check (`scripts/check_source_export.py`, factory startup, autoexec disabled, two threads): all 8 passed with no errors or warnings. Results are in `/tmp/round21-source-export/`.
4. Independently hashed each selected GLB and inspected the exact eight-view images (`proof-final` / `eight-view-sheet`); reviewed the brief, candidate metadata, measured metrics, render manifests, and handoff limitations.

The following were not rerun by this audit: Khronos validation, Node runtime parser, deterministic semantic rebuilds, GPU test, or formal production-scene test. Handoff/maker records report Khronos/parser/rebuild successes; those are pre-existing evidence, not tests executed in this audit. GPU/formal scene remain unrun. Exact provider generation/modeling-authoring timestamps remain unknown where the handoffs say so. Static-profile eight-view proof must not be presented as a GPU or turntable result.

## Selected asset integrity

| Batch | Asset / revision | GLB bytes | SHA-256 |
|---|---|---:|---|
| 56 | Cycadeoidea r002 | 302,400 | `9388a918314ca5426c992d9f1702e881d369bc5a15ad43d5dce18afcf80c0fd0` |
| 56 | Gondwanagaricites r002 | 36,864 | `8133ad81f4f3d18b4d0ebd5d29ca2fe540039254b6efc8522fe20d2ec4b4036a` |
| 56 | Deflation hollow r001 | 108,392 | `c679676d46d8e51789a690db2f1590baa89c766cd50eb29700347150b43fd7be` |
| 56 | Arthrophycus annulated burrow r002 | 297,892 | `a32b30732582580884b7f6de257a22c701df20f2359e9183585a10a8f959834c` |
| 57 | Quatsinoporites r001 | 109,672 | `8d1dbd00dab4303b667d48048d5a8df737f07cb54d53a8173bb72fc025d622c2` |
| 57 | Nidula baltica r002 | 98,192 | `2de9c6a6ef69e3aab055add63797055bcd9174da0c7d92554b76ed697c3d2997` |
| 57 | Cave column r002 | 103,728 | `2659a158b5c3bf2a50b32057e58e6a28c42ed36827ed27f968918274fc48679a` |
| 57 | Rusophycus resting excavation r001 | 544,188 | `7493f6df58164496ae64161395138520787fa2be9a9eb0f2363c56ef4f276751` |

## Visual, specification, and factual review

### Batch 56

- **Cycadeoidea r002 — targeted correction required.** The selected model and the maker’s own delivery note show four recessed reproductive pockets, but the frozen brief’s recognition feature calls for exactly three. Its barrel/trunk and repeated armor/leaf-base rhythm read clearly, but are very regular and the pockets are not immediately countable in the hero view. Do not reinterpret the fourth as a scientific specimen claim: the count is a design requirement of the frozen brief. On a new revision, retain r002 unchanged and make three unambiguous recessed sites. Brief pointer: `assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/brief.json`; selected source/model: same directory’s `source.blend` and `model.glb`; exact views: `proof-final/`. Maker evidence: `production/continuous-small-life-round21-20261020/work/batch-56/cycadeoidea/r002/`.
- **Gondwanagaricites r002 — provisionally acceptable with disclosed legibility limitation.** It reads as the small, slender-stiped fossil fungus on a slab, without an unsupported ring or color assertion. The gills are very shallow/small and hard to read at this scale, matching the maker caveat; no material contradiction found. The primary paper describes a roughly 10-mm cap, 34-mm stipe, 4.5-mm gills, no ring, and unknown original color: [PLOS One paper](https://journals.plos.org/plosone/article/file?id=10.1371%2Fjournal.pone.0178327&type=printable); nomenclature correction: [PLOS corrigendum](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199660).
- **Deflation hollow r001 — provisionally acceptable.** A shallow concavity with an asymmetric raised rim reads as a stylized deflation hollow across top/side/clay views. No unsupported named place, age, or scale is added. NPS describes wind scooping loose surface material as the general blowout/deflation process: [NPS aeolian landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm). The particular rim shape is artistic, not independently claimed as a diagnostic specimen form.
- **Arthrophycus annulated burrow r002 — provisionally acceptable.** Three separate curved, raised, cross-annulated trace tubes read clearly. Slab and scale are stylized; there is no maker-producer attribution. This is appropriate for a trace fossil; compare [Digital Atlas of Ancient Life, feeding traces](https://www.digitalatlasofancientlife.org/vc/trace-fossils/feeding-traces/).

### Batch 57

- **Quatsinoporites r001 — targeted correction required.** It has true recessed cavities and reads as a fragment, but its pores appear close to a regular round grid with highly similar size and spacing. That conflicts with the frozen “irregular fragment” / varied blind openings direction and the primary description of round-to-elliptical pores distributed irregularly. Maker notes independently acknowledge the visible grid regularity. New revision should vary pore shape, size, and spacing while preserving blind recessed cavities and fractured fragment character; do not replace or edit r001. Brief and selected files: `assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/{brief.json,candidate.json,quatsinoporites.glb,source.blend}` and `proof-final/`. Maker evidence: `production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/`. Factual reference: Smith et al. (2004), [Mycologia paper record and author-uploaded paper](https://www.researchgate.net/publication/315907142_Cretaceous_and_Eocene_poroid_hymenophores_from_Vancouver_Island_British_Columbia).
- **Nidula baltica r002 — generic form supported; specimen-image match unknown.** The cup and internal lenticular peridiole are legible in the images, consistent with the accessible text-level evidence for the genus/species’ basic structure. However, the corrected holotype plate pixels were not accessible, so I cannot certify that this exact silhouette/detail matches the figure. For this limited stylized model, treat specimen-level visual match as unknown rather than requiring an unavailable plate or fabricating a pass; color and display scale are artistic choices. This matches the handoff disclosure.
- **Cave column r002 — provisionally acceptable.** A connected, subtly fluted pillar with irregular floor/top attachments reads as a cave column rather than the earlier separated/symmetric form. NPS defines a column as a connected stalagmite and stalactite: [NPS speleothems](https://www.nps.gov/subjects/caves/speleothems.htm). Fine growth history is not claimed.
- **Rusophycus resting excavation r001 — provisionally acceptable.** Two deep bilobed negative impressions and scratch fields read as a resting trace in the top/clay views. The slab outline is deliberately simple and there is no animal/behavior-specific claim. This stays within the published trace category: [Digital Atlas of Ancient Life, resting traces](https://www.digitalatlasofancientlife.org/vc/trace-fossils/resting-traces/).

## Minimal maker follow-up

Use a new, bounded revision while preserving both selected revisions and all frozen briefs:

1. Cycadeoidea: make exactly three clearly distinct recessed reproductive sites in the selected hero/top/clay views.
2. Quatsinoporites: break the near-grid regularity via controlled variation in pore size, round-to-elliptical shape, and spacing, without losing blind cavity depth or the irregular broken fragment silhouette.

After those repairs, rerun the candidate, GLB, source/export, Khronos, runtime parser, semantic rebuild and proof binding checks; then conduct fresh independent visual/spec review. Keep Nidula’s specimen-plate comparison explicitly unknown unless corrected source pixels become available. Keep approval/publication gates pending until formally completed.
