# Per-model registry and staged release integration

Status: opt-in phase A compatibility scaffold plus a phase B per-model capture-package writer and checked existing-release admission adapter. None is connected to the production publication/CI path. Future-batch admission, the renderer's opt-in package-output mode, an automatic integration queue and production cutover are not implemented. No historical record set is committed by this change; import the exact current release commit when its turn in the integration queue arrives.

## Why IDs alone did not remove the collisions

The repository already separates most payloads by ID: `assets/additions/<id>/<release>/...`, `assets/revisions/<id>/<revision>/...` and `site/public/gallery/posters/<id>[-wheel].png`. These URLs must remain stable. Different model IDs are necessary, but the current authoring path still has several shared writers:

- `site/generate-manifest.mjs` and the accepted-release collectors produce `assets/manifest.json`; `site/initial-release.mjs` selects the legacy authority chain.
- `site/catalog-build.mjs` correctly derives browsing data, but it consumes shared manifest and `site/catalog-data.json` inputs. The catalog output directory is replaced as a whole.
- `site/capture-gallery-posters.mjs:persistSourceGallery` replaces the entire source gallery after complete-snapshot validation. The images have unique names, but their metadata and ownership are still a shared snapshot.
- `assets/turntables/index.json`, `site/public/gallery/resources.json` and `site/gallery/wheel-framing.json` mix independent per-model entries.
- `site/accepted-bounded-batches.mjs` and batch-specific collectors are shared release-policy/edit points.

Git normally reports overlapping changes rather than silently overwriting them. The risk is conflict resolution or importing a stale full snapshot, not a claim that every Git merge loses images. Per-model ownership removes the competing authoritative writers; deterministic projection removes manual aggregate merges. The last branch-head/deployment decision must still have one order.

## Ownership and identity

Use the existing stable descriptive `asset.id` as the model code. Do not add a global incrementing number or a mutable ID-allocation file. A batch is a workflow grouping, not the identity of a model or its public storage address.

The phase-A on-disk contract is:

- `registry/baseline.json`: one exact-commit historical import, including original shared headers, editorial definitions, unknown fields, source-file hashes and historical ordering. Frozen after import.
- `registry/models/<id>/revisions/<record-sha256>/record.json`: canonical JSON, immutable content-addressed record. It owns the model metadata, its detail/wheel poster record and file pins, manual wheel framing, optional turntable/card metadata and its catalog memberships.
- `registry/batches/<batch-id>.json`: one immutable descriptor per independently submitted batch. It references exact model record digests, new editorial definitions, and pinned external evidence. It is data, not an approval token.
- Existing binaries stay at their existing paths. New models may use `assets/models/<id>/...` or the already supported `assets/additions/<id>/...`. No duplicate GLBs, Blend files or images are needed for migration.

Each selected ID has exactly one owner and one selected immutable revision. Duplicate IDs, duplicate batch or pack definitions, reused model/optional-resource paths, cross-model gallery paths and unselected records fail closed. The loader inventories all files under `registry/models`; canonical but unreferenced record files, unexpected files and symlinks are rejected rather than ignored. Phase A stores only selected records there; future retained inactive revisions will require a separately specified archival inventory. Existing revisions cannot be replaced by appending a second record. A future revision switch needs a separate explicitly reviewed transition, retaining old revisions and their URLs. This scaffold intentionally does not implement automatic switches.

Historical undefined editorial labels, unknown formal results, work-in-progress statuses, scientific limits and manually approved pixels are retained. Import is not an opportunity to fill gaps, rename paths, recapture pictures, or promote approval.

## Deterministic composition

`site/model-registry.mjs` separates import, composition, append eligibility, input binding and final integration-plan checks.

Import reads the five exact legacy metadata files from an immutable Git commit. It splits their per-model ownership and immediately requires a lossless semantic round-trip. No production files are rewritten. Canonical record files use their actual SHA-256 in their path; the loader rejects noncanonical or changed record bytes.

Composition preserves historical array ordering and metadata. Independent new records/definitions are sorted by ASCII ID after the historical prefix. The result depends on the selected set, not batch arrival order. All five old metadata shapes remain available. The CLI also calls the existing `createCatalog` implementation with the raw projected source manifest and curation data to generate the browsing index, shards and details. This verifies raw-source catalog parity only. Production `copy-assets.mjs` first enriches the manifest through `deliverManifestAssets` and `deliverTurntables`, adding downloads, file sizes, card previews and turntable delivery fields. The separate phase B delivery-parity command below exercises those actual production functions; it does not turn raw `compose` output into a deployed catalog.

The old snapshot's publication/capture headers remain historical data. Appending a record does **not** manufacture updated publication authority or claim that a new capture session occurred. Generated append previews therefore are not deployable simply because they compose successfully. The publication adapter in phase C must supply independently verified authority and capture provenance before a deployment can consume them.

Deterministic ordering of the new suffix may change after another independent batch is added. Existing append-only legacy checks that currently require an identical aggregate-array prefix must not be disabled to make this pass. The cutover needs reviewed ID/content-based immutable-history checks, while preserving the old exact-byte/prefix checks on the historical adapter. Until then, use the existing release pipeline.

## Phase-A commands and guarantees

Run on an isolated branch. All output directories must be new; the CLI refuses to overwrite an existing tree. Use a full 40-character commit, not `main` or another moving ref.

```
node --test site/model-registry-test.mjs
node site/model-registry-cli.mjs import --repo /path/to/repo --commit FULL_SHA --out /tmp/registry-import
node site/model-registry-cli.mjs compose --registry-root /tmp/registry-import --out /tmp/registry-projection
node site/model-registry-cli.mjs plan --previous /tmp/registry-import --next /tmp/registry-next --head FULL_CURRENT_HEAD --out /tmp/registry-plan
```

These commands never change Git refs, source aggregates, assets, workflows or active release branches. They never run archived generator code or infer authority from a filename. Their staged outputs are not a replacement for `publication:check` or the existing build/release gates.

`modelInputBinding` verifies the record's GLB, editable source, preview, gallery images, optional turntable descriptor and frames, optional card image and caller-supplied evidence pins against actual bytes. Optional descriptor/card paths must be canonical and owned by that exact model/revision. Descriptor source GLB hashes and any explicit identity fields must match the model; legacy descriptors without an ID remain identified by their owned path. Frame inventories must be nonempty, match declared frame count/total bytes, contain a valid poster index and resolve to exact sequential owned frame paths. Frame and card byte counts are checked against actual bytes. Its digest also binds the complete record and a caller-supplied shared context hash. Changing one model's bytes/metadata or the shared context invalidates its binding; adding an unrelated model does not. This is an input-binding primitive, **not** a GitHub artifact verifier or proof of source quality. It does not replace source reconstruction, candidate approval, strict GPU execution, poster review, trusted producer identity or the existing dependency-closure/provenance checks.

## Phase B implemented boundary

### Per-model capture-package writer

`site/model-capture-package.mjs` exposes `createModelCaptureDraft`, `assertModelCaptureDraft` and `writeModelCaptureDraft`. Given one renderer-produced detail/wheel PNG pair, it verifies the actual GLB hash, existing poster input recipe and browser binding, canonical owner paths, dimensions/transparency and byte seals. It appends:

```
registry/captures/<id>/<capture-record-sha256>/capture.json
registry/captures/<id>/<capture-record-sha256>/detail.png
registry/captures/<id>/<capture-record-sha256>/wheel.png
```

Independent IDs do not share a mutable index. Installation uses staging and atomic rename. Identical concurrent submissions are idempotent; altered existing bytes, extra files and symlinks fail. Public image URLs remain the existing `gallery/posters/<id>[-wheel].png` in metadata. The package always declares `unverified-model-capture` and `publication_authority: false`. It is storage and consistency validation, not proof of render quality or source approval.

The existing capture renderer and `persistSourceGallery` are deliberately unchanged in this checkpoint. Calling the new writer from a separately reviewed opt-in renderer mode and consuming its packages at integration are still required. Tests use synthetic PNG headers and do not claim fresh browser/GPU rendering.

### Independently checked existing-release admission

`site/model-registry-admission.mjs:admitExistingRegistryRelease` has a deliberately narrow contract: the registry must project to the **exact already released source scope** in a clean fixed-commit checkout. New IDs or altered source metadata cannot inherit that release's authority. There are no hardcoded batch numbers or model counts.

The factory:

1. Runs the existing `assertBuiltRenderInputs` and computes actual built-input model bindings. A source-only proof cannot substitute.
2. Independently retrieves a successful exact-source main workflow's model proof through the existing GitHub provenance verifier. Compatible-ancestor evidence alone is insufficient to admit a changed release scope. Every model and the actual delivered payload must match.
3. Independently retrieves the separate poster artifact from the same successful run and attempt, rechecking repository/workflow/run/check-suite identity, immutable artifact metadata/digest, safe archive inventory, exact renderer recipe/runtime, every model input and the complete PNG pair coverage.
4. Runs the exact checkout's original `node site/initial-release.mjs --check` source/candidate/publication chain. Independent render evidence does not replace publication checks.
5. Rechecks source, registry and built-input digests after validation.

Only this factory creates an opaque, process-local admission handle. `collectAdmittedRegistry` and `writeAdmittedRegistryProjection` reject serialized receipts, `accepted: true` flags and arbitrary proof JSON, and recheck unchanged source/build inputs before use. The write adapter produces a fresh staged legacy projection only; it does not publish, create a Git merge, enrich a deployed catalog or modify current production aggregates. Transport injection exists only for protected-code tests, never as a repository-data acceptance field.

The original publication chain is still the authority for prospective batches. Generic admission of new source/review bundles is **not yet implemented**. The current adapter proves a safe handoff for existing admitted scope, not a shortcut that lets new records approve themselves. Automated tests use API/artifact fixtures and the real validators; no live GitHub admission or new full-release QA result is claimed.

### Actual production delivery parity

`site/model-registry-delivery-parity.mjs` is an offline, read-only-source check:

```
node site/model-registry-delivery-parity.mjs /path/to/clean/source /tmp/registry-import
```

It requires an exact semantic source projection, loads the fixed checkout's actual `deliverManifestAssets`, `deliverTurntables` and `writeCatalog`, and executes both legacy and registry inputs into separate temporary outputs. It compares the complete enriched manifests, every generated JSON field and output path, and exact bytes of assets/downloads. It cleans only its own temporary directory and checks that the source commit/tracked files did not change.

Canonical registry JSON may serialize object properties in a different order. The report lists these serialization-only JSON differences explicitly; semantic equality is not a byte-for-byte deployed-site claim. Full site HTML/bundles, routes, browser/GPU QA and deployment remain separate gates. Repeat delivery parity against the then-current cumulative source at cutover, not a fixed model count.

## Rollout sequence

### A. Compatibility scaffold, this change

- Add importer, per-model immutable record format, deterministic composer and integration-plan checks, with adversarial tests.
- Dry-run an exact historical release snapshot and compare all five metadata outputs and derived catalog data.
- Leave current publication, full/page workflows, accepted-batch registry and cache policies unchanged.
- Do not commit a snapshot from a release train that is still moving. Regenerate the import from the exact admitted head later.

### B. Independent authoring and capture, partly implemented above

- Author each new model's assets and record under its own ID. Emit a batch-specific submission descriptor rather than editing five aggregate files.
- Add a per-model poster-output mode that emits only that model's sealed pair and metadata. Keep the complete-gallery audit as an integration gate; do not make `persistSourceGallery` silently merge unchecked snapshots.
- Keep draft submissions separate from admitted release descriptors. The present compatibility `batches` directory is not by itself the admission mechanism.
- Preserve the source/review archive owner rules and exact pinned source bundles. No arbitrary executable file becomes exempt merely because it lives under a model directory.

### C. Authority adapter and proof cutover, existing-scope adapter only above

- Freeze the legacy publication chain as a checked historical adapter; add a generic data-driven validator for future exact per-batch descriptors instead of another executable collector per batch.
- Admission must run existing candidate/source/review/publication checks, bind each ID to approved source and review artifacts, and independently verify trusted CI evidence. Repository-authored JSON and matching hashes alone must never skip GPU/image QA.
- Generate old aggregate URLs from the admitted registry only. Do not deploy arbitrary `compose` output. Hard cutover gate: compare the complete production-enriched manifest and deployed catalog/index/shards/details after `deliverManifestAssets` and `deliverTurntables`, including downloads, file sizes, card-preview and turntable fields; raw-source `createCatalog` equality is insufficient.
- Keep global build, route, schema, coverage, gallery-completeness and publication invariants. Tests do not all disappear: unchanged model-specific rendering may reuse verified compatible-ancestor evidence; changed models and shared renderer/policy changes remain invalidating.
- Adding these new `site/*.mjs` files is itself a protected-policy change under `ci-model-proof.mjs:protectedModelPath`. Even unused scaffolding changes that hash if merged. Coordinate one fresh full baseline for the reviewed cutover; do not add a hash exemption just to preserve a current cache hit.
- Leave full/page per-ref cancellation unchanged until separately reviewed. An older canceled run is not proof for a newer head.

### D. Short final serialized integration

Parallel work can include research, construction, source checks, independent review, per-model rendering and provenance validation. The final queue does only what needs a common latest state:

1. Read the exact current protected main head and already admitted record set.
2. Verify unchanged historical record/batch digests, resolve only genuine duplicate-ID/definition conflicts, and take the deterministic union with the candidate batch.
3. Regenerate aggregate metadata/catalog/indices; verify exact retained+added coverage, file ownership, no deletion, hashes, source authority and all applicable release/global checks.
4. Independently revalidate candidate proof bindings against actual current inputs and shared policy. A new shared policy requires the required full baseline, not a fallback cache claim.
5. Recheck that main still equals the planned head immediately before an authorized merge. If it moved, recompose/recheck against the new head; never force-push or overwrite another batch's output.
6. Publish and observe the exact admitted commit. If the platform merges a group, validate the group union, not just its individual branches.

`createIntegrationPlan` records the prior/next registry digests, exact expected head, added IDs, retained count and output hashes. `assertIntegrationPlan` rejects a moved head or changed inputs. It never merges or grants approval. A trustworthy final queue runner must supply the observed head and the verified checks; its implementation is deliberately deferred to phase C/D.

## Phase A validation checkpoint, 2026-10-20

- Initial review found real optional-resource path/content and orphan-record gaps in the original 25-test checkpoint. The revised 50-test suite includes failures for foreign/traversing optional paths, cross-model card aliases, mismatched descriptor IDs/source hashes, empty/misdeclared frame inventories, incorrect frame/card byte counts, and on-disk orphans/symlinks. All 50 tests passed after the fixes.
- Existing synthetic catalog regression passed with 10,000 models and 40 shards.
- Immutable 202-model snapshot `c8714ec3eba2925d1669663556445f8c43e40030`: all five legacy metadata outputs round-trip semantically exactly; raw-source `createCatalog` index, shards and details are equal. Phase A did not verify production delivery enrichment; that additional check is reported separately below.
- Checked 1,462 existing model/image input files, 259,833,677 bytes, against existing content hashes. No binaries copied or changed.
- Not run/claimed: full release validation, source rebuilding, fresh browser/GPU QA, CI deployment or main integration. None is necessary to claim a compatible scaffold, and all applicable checks remain necessary at cutover.

## Phase B validation checkpoint, 2026-10-20

- `node --test site/model-registry-test.mjs site/model-capture-package-test.mjs site/model-registry-admission-test.mjs`: 79/79 pass (50 registry, 7 capture, 22 admission). Existing model-cache and gallery-poster-cache regression programs also pass; the existing 10,000-model/40-shard catalog regression passes.
- Capture-package tests cover immutable/idempotent storage, malformed or foreign PNG pairs, source/browser/input bindings, symlink/inventory refusal and four real concurrent producer processes spanning three independent IDs.
- Admission tests cover exact model plus separate poster artifact provenance, missing/failed/forked/expired/partial/mismatched evidence, source-only substitution, payload/recipe/source/input mismatches, serialized or self-reported acceptance, post-admission source/build tampering, and a failing original publication gate.
- Actual production delivery on fixed source `c8714ec3eba2925d1669663556445f8c43e40030`, 202 models: complete enriched manifests equal; all 205 generated JSON files semantically equal; all 1,462 asset/download files, 254,428,093 bytes, byte-identical. There are 203 serialization-only generated JSON differences (202 detail objects and the enriched manifest), disclosed rather than claimed byte-identical. Original source bytes/URLs and metadata remain unchanged.
- No current workflow, publication gate, cache policy, historical source asset, main branch or active release branch is modified. The protected-policy baseline refresh requirement above still applies if this code is later integrated.
