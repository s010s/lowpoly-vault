# Content first, one release build

`pages.yml` runs `node site/ci-build-release.mjs`: source acceptance once,
standard GLB checks, registry consistency, Vite once, package once, final `dist`
audit once. Successful source results travel directly between these calls;
there is no new persisted cache, skip receipt, signature or cross-run bridge.
The existing exact-build stamp, Pages artifact and post-deployment queue remain.

## Checks by change

- Model-only append: unique IDs, safe paths, immutable old records/assets and
  registry projections; new content acceptance and standard GLB checks; a shared
  loader contract; build and final output audit. Historical regression suites are
  not applicable, not reported as newly passed.
- Website change: website/controller regressions and the same build/output gates.
  Full-catalog geometry matrices run only for renderer/geometry/shared-dependency
  changes, not for unrelated release/CI changes.
  Code-test scope is separate from model scope: unchanged accepted model bytes do
  not need a fresh content review because a website or validator file changed.
- Validator/CI change: small safety fixtures and historical publication
  compatibility suites. The standardized asset workflow owns Python pipeline
  self-tests and no longer repeats publication validation or publication suites.
- Invalid/missing provenance or unavailable successful-main baseline: full source
  validation. Existing authenticated-main proof remains the only reuse authority,
  now for an exact main push as well as a PR. No unavailable check becomes PASS.

A file pinned as actual model source remains a content dependency even if also
used as a tool. Changed model content is checked; old records cannot masquerade
as additions. Website changes cannot be routed into the model-only test lane.

## Independent acceptance

New `content-production-release-v1` descriptors retain exact GLB/Blend, source,
factual scope, measurements, independent review, poster and license/credits pins.
They cannot contain `implementation` pins. Review binds content, not validator
code hashes, and cannot grant publication or promote an unknown/failed runtime
result. This change creates no production descriptor or real review receipt.

Old evidence is untouched. Exactly the five already reviewed PR60 bridge/review
byte pairs have a frozen compatibility boundary: their current-implementation
pins describe the historical code, not future code. Original descriptor, review,
implementation snapshots, subjects and record pins remain mandatory. Other
bridges or changed bytes are rejected. Do not create more bridges
for routine code changes.

## Output and rollback

The final audit enforces the deployment file allowlist, exact IDs and source-bound
metadata, asset hashes, license/credits bytes, gallery seals and ZIP members/hashes.
Private QA files, unexpected files, symlinks and bad archives fail. Stamping adds
only the existing build marker and verifies that audited bytes did not change.
Deploy the uploaded artifact, not another build. Keep the previous known-good
source/artifact for the existing GitHub Pages rollback procedure. This change
does not grant or automate a rollback or deployment.

## Focused verification

- `node site/ci-lean-release-test.mjs`: execution order, all fail-stop phases,
  real invalid GLB, per-descriptor turntable collection and scope selection.
- `node site/content-production-acceptance-test.mjs`: actual small legacy/v2
  fixtures, hashes, source/media/license changes, independent review and history.
- `node site/audit-release-test.mjs`: real final audit, bad ZIPs, altered bytes,
  extra/missing files, private QA and symlinks.
- Existing append, registry and provenance fixtures cover duplicate IDs, old-file
  changes, wrong events, dirty Git state and missing/failed baseline proof.

Local focused tests are not a full 448-model build, hosted CI, browser/GPU review,
independent code acceptance or deployment. Historical diagnostic commands remain
available; the production workflow no longer runs them redundantly.
