# Generation, refinement and QA provenance

This optional [schema](../schemas/production-provenance.schema.json) and
[anonymous template](../schemas/templates/production-provenance.template.json)
record workflow facts. They do not change catalog identity, production acceptance,
publication authority or site behavior. The template is unknown data, not a task
request, approved budget or completed model.

## Keep stages separate

- `external_generation`: whether an external 3D service produced a base. Optional
  `provider` and `tool_route` identify a public-safe service/route, not account or
  request identity. `completed` requires the retained base GLB SHA-256; generation
  alone does not mean Blender refinement or QA happened.
- `refinement`: work on the exact candidate in `subject`. `completed` requires its
  immutable revision and final GLB SHA-256; an optional `tool` names the editor.
  A deliberate low-poly finish can be complete without photorealistic details.
  This is a maker-work state, not independent approval.
- `independent_qa`: outcome for that exact `subject`, with explicitly inspected
  `scope` and relative-path/SHA-256 evidence. `pass` needs actual independent
  review, nonempty scope and evidence; schema validity cannot authenticate review
  or certify visual quality. Unrun checks remain unknown outside the stated scope.

Generation/refinement statuses are `unknown`, `not_started`, `in_progress`,
`completed`, `failed` or `not_applicable`. Use `not_started`/`not_applicable` only
when known; absence of records is not evidence of either. QA uses `unknown`,
`pending`, `pass`, `fail` or `stale`. Missing provenance on a historical asset is
interpreted as **unknown**, never silently backfilled as generated, refined or not
made. Preserve previous failures and their evidence.

The `subject` binds refinement and QA to one revision and exact final GLB bytes.
Changing geometry, materials or export bytes creates a new subject and requires
review of affected checks. Keep the old record and evidence; do not copy `pass`
to new bytes. Mark copied old QA stale or pending until reviewed. A base's hash is
separate: retain it even when refinement produces different bytes. Evidence paths
must be repository-relative in public records, with no parent traversal or links
to private storage. Check their actual bytes separately from schema validation.

## Compatible storage, not a migration

Use a candidate sidecar or private per-model ledger first. If a new public asset
record needs these facts, `asset.production_provenance` may carry this object.
Existing registry top-level keys remain unchanged. Its `asset_id` must equal
`record.id`, its subject GLB hash must equal `asset.sha256.glb`, and its revision
must match the recorded candidate revision. These cross-record/file checks remain
necessary; this standalone schema does not execute them. Current registry code
preserves extra asset metadata but does not validate this optional schema.

Changing a content-addressed record creates a new record hash and requires the
normal collector/registry consistency process. Do not rewrite historical records,
hand-edit generated aggregate manifests, or insert unsupported fields into a
frozen candidate profile. This addition does not change existing validators,
publication checks, release manifests, binary files, or historical QA.

A newer private candidate is not the old published asset: only the authorized
release's exact GLB and source hashes establish what is live. Generation complete,
refinement complete and QA pass are all independent from release permission.
The actual release manifest remains the source for publication state.

## Public and private records

Public optional metadata can state a provider/tool route, stage, immutable version,
artifact hash and publishable evidence. Keep real service/task IDs, billing and
credit usage, retry reservations, user budgets, account identifiers, credentials
and private backup locations in the private ledger. Unknown charges stay unknown,
not zero; recording them here never increases authorization or resets spent budget.
No public field is required to expose those private values.

For offline schema checks use a Draft 2020-12 validator. Also inspect the actual
artifact/evidence hashes and current authorization; no schema result is a release
or spending approval. Repository task handoffs follow [AGENTS.md](../AGENTS.md).
