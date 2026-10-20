# Batch 51 specification-correction v001: independent difference review

**Review result:** Pass for the supplemental nominal-scale description of Calcite raft deposit r002 and accretionary lapilli bed r002. The two corrected nominal values agree with the original concept prompts, frozen construction plans, and exact unchanged GLB geometry. This is a narrow metadata/specification difference result; it is not a formal candidate approval.

## Pins and methods

- New candidate head: `9000874083b6a6fb8e4e83dc95e4915801eecff4`.
- Previous candidate handoff: `6b5bc2793572361242544f7a19afd6bbd71243ab`, confirmed as an ancestor of the new head.
- Original artifact source commit: `ee4e37b3c1cc49ab5e41c807c6ca8e1a155bbc6b`.
- New correction index SHA-256: `e8d2c00dcee9222b95db16d4630c1aeae14753148f22bbb3615373aecb581616`.
- Original correction checker SHA-256: `9ff0634433351b3e5d36f4f7f6762a3ff2627e379d2b3138d384989659922016`.

The source `verify_correction.py` was replayed read-only. It passed, verified the index/handoff pins, checked every item in the 772-file preservation manifest against its current bytes and Git blob, checked candidate bundle checksums, compared supplemental briefs against the originals, and reran original candidate and concept validators. Its result retains `--require-approved` exit 1 and `--require-complete` exit 1 for all four items. The latter has exactly one blocker: `concept_generated_at: unknown; do not reconstruct times from file mtimes`.

I also used the independent replay script next to this report. It decodes each GLB binary `POSITION` stream directly, unions the actual vertex coordinates, verifies identity-only mesh nodes, hashes the GLBs, and checks all 772 preserved file blobs against the preceding handoff commit. It confirmed that the only changes between candidate handoff commits are the handoff/index pointers and the versioned correction directory. No candidate bundle, GLB, Blend, concept image, old r002 brief, or prior freeze changed.

## Recomputed measurements

| Asset | Registered r002 nominal | Supplemental nominal | Decoded exact GLB bounds XYZ | GLB SHA-256 | Review |
|---|---:|---:|---|---|---|
| Calcite raft deposit | 0.42 m | 0.32 m | 0.3359383047 × 0.0260695666 × 0.2542886138 m | `fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22` | Supplemental specification pass |
| Accretionary lapilli bed | 0.60 m | 0.28 m | 0.2844992578 × 0.1155999973 × 0.2050909027 m | `61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3` | Supplemental specification pass |

The new nominal fields match the original concept prompt and frozen construction plan/build configuration. The computed GLB bounds match the supplemental brief, metadata, and derived-freeze measurements. Nominal design span is an art-direction value; it is not the exact bounding box or a measured fossil/specimen dimension. Neither brief sets a numeric tolerance connecting nominal art direction to the outermost vertices, so this pass means the contradictory descriptive fields have been reconciled and truthful actual bounds are separately stated. It does not certify a tighter dimensional tolerance.

## What the addendum supports

Downstream documentation may cite the **0.32 m Calcite** and **0.28 m lapilli** nominal design values when it names `specification-correction-v001` as its source and retains the separately measured GLB bounds. A targeted specification review or descriptive inventory of these exact, hash-pinned GLBs may rely on the addendum. The source prompt and construction plan independently support those two design values, so no geometry rebuild is needed to reconcile the nominal dimensions.

The addendum was made after modeling. It cannot be described as a pre-model freeze or as the original production brief. The original registered r002 candidate brief hashes and values remain:

- Calcite: `8c44fdec8e9109219fbe9dde0e75aeeb082e77aec9e2f326b2e0493d5bb8c69d` with 0.42 m.
- Lapilli: `0f3019059ad83b67e7af323ec95045a3f08828aa5c21e2ec6cd82185c5495c5` with 0.60 m.

Those old brief bytes, candidate records, freeze records, and historic reports were not rebound to the supplemental briefs. Therefore this review does **not** retroactively change the official specification stage for either registered candidate. The production-side `--require-approved` result remains unapproved, and the handoff continues to say the targeted correction is pending until an authorized candidate-side transition is made under the immutable-revision rules. No historical PASS is carried to a new brief.

For formal acceptance against corrected values, a distinct immutable candidate revision must bind the corrected brief and its matching evidence, then receive the required candidate-side stage records and approval. The unchanged four-item complete-evidence gate still lacks the exact ImageGen provider generation time. Preserve it as unknown; this difference review supplies no timestamp. Formal approval and publication remain separate.

## Boundaries

This review did not reopen or repeat visual QA. It does not expand the prior software WebGL result, which used Chromium/Three.js with ANGLE SwiftShader. Hardware GPU behavior and the target parent/museum scene remain unverified. No runtime, source, image, Blender, or model bytes were changed.

## Replay evidence

- [Independent verification output](independent-verification.json)
- [Independent exact-GLB decoder and preservation checker](verify_spec_correction.py)
- Candidate correction index SHA-256: `e8d2c00dcee9222b95db16d4630c1aeae14753148f22bbb3615373aecb581616`
- Candidate correction checker and replay output: indexed in the candidate `specification-correction-v001/index.json` at the pinned head above.

Run the independent replay from this QA branch checkout, with a separate pinned candidate checkout available:

```sh
python3 qa/batch51-independent-20261019/evidence/differential-v001/verify_spec_correction.py --root /path/to/candidate-9000874083b6a6fb8e4e83dc95e4915801eecff4
```

Run the candidate-side mechanical checker from the pinned candidate checkout:

```sh
python3 production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/verify_correction.py
```
