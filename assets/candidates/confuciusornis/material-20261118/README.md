# Confuciusornis material repair

Status: **in progress; not release-ready**. The shared `repair/live-models-review` branch selects this candidate through the real manifest and gallery poster resolver. Main and the production deployment are unchanged.

The material-only edit improves wing and belly readability. Geometry, UVs and the GLB binary payload are unchanged. `source.blend` is an editable import of this candidate with packed images, not the original modeling session. Both posters belong to this candidate.

Independent scoped review confirmed asset pairing and material improvement. The real integration now checks source-bound posters, sizes and hashes, generated GLB/Blend ZIP/credits, and that all 938 other manifest entries are unchanged. Run `node qa/repair-integration/confuciusornis-test.mjs`. This focused test is not a full build or visual release approval.

Remaining: integrate shared transition fixes in source, retest the integrated renderer and complete full-repository CI plus final independent review. No diagnostic compiled bundle or per-model cumulative whitelist was copied. Historical source files remain intact.

All models are handled on the shared repair branch with per-model commits. Open a PR and merge/deploy only after the full requested scope and integrated verification are complete, not after a timed or model-count batch.
