# Combined bounded release: 194 → 217

This release composes 23 independently accepted stylized models in one additive publication candidate. It does not introduce a new acceptance policy, change model bytes, replace previous QA, or promote formal profile acceptance.

## Composition and immutable inputs

- Existing 194 published records, including Batch54, remain unchanged.
- Batches52/53: 8 models from `c8714ec3eba2925d1669663556445f8c43e40030`. The original Batch52 three-model review and Aturia differential repair review remain distinct descriptors.
- Batches56/57: 7 models from `a4891ceac7d01e29710d3b5d92b29db203e1a0c0`. Nidula baltica remains excluded.
- Batches51/55: 8 models from `cc63e87a94ae77c6563709d4947fed398cfe7b8d`. Batch55's 20 missing historical maker logs remain missing and disclosed; certified generator rebuild remains unestablished.
- No Batch58 or later model is included.

The bounded registry retains the existing Batch54 entry and appends all seven new descriptor entries. Original source bundles, reviews, capture evidence, metadata, and descriptor hash pins are preserved byte-for-byte. Catalog and gallery composition appends new records instead of replacing snapshots from older branches. The collector chain checks the full previous release before appending each independently bounded scope.

## Acceptance limits and validation

Acceptance remains `independent_qa_accepted_stylized_prop`. Formal profile acceptance is `BLOCKED`; physical hardware GPU and intended-scene verification are not claimed. Historical evidence retains its original, narrower scope.

Selected negative-test entry points are `--batches52-53-only`, `--batches5657-only`, and `--batches5155-only` on `site/concept-landair-release-test.mjs`. The default test invocation also includes all three scopes. Mutation tests operate on isolated copies; accepted source inputs are not modified.

Publication still requires the complete combined release CI and Pages checks for the exact final commit after integrating the verified transport-fix main baseline. Earlier per-batch CI or local source checks do not substitute for that gate. No shared render/proof policy or classifier is modified by this release.
