# Lightweight per-model records and index generation

This isolated change adds storage and generation tools, not a new approval system.
It is based on the exact 217-model release snapshot
`da3fb30ccc4dd4e511e029c0a51a7a67265870c5`. This branch now includes that
refreshed metadata import, explicit npm commands, a read-only
build/audit consistency check and narrowly scoped registry-data append recognition.
It does not modify the existing release collectors, model/poster proof validators,
workflows, historical asset/gallery bytes, URLs or approval data. It is not merged
or deployed. The experimental admission, source-review and local-queue modules are
**not included**. Do not merge that larger experimental branch to obtain these tools.

## Responsibilities

- Keep the existing stable model ID and binary URLs. A record at
  `registry/models/<id>/revisions/<sha256>/record.json` owns the asset metadata,
  poster pair/seals, wheel framing, optional turntable/card and pack membership.
- Import one exact release into `registry/baseline.json`. Each new batch adds its
  own `registry/batches/<batch-id>.json` and model records. There is no shared
  mutable ID counter. A batch descriptor and its evidence hashes are data, not
  approval. Duplicate ownership, modified references and orphan records fail.
- `model-registry-sync.mjs` composes the selected records into the existing five
  JSON files. Independent workers do not edit these aggregate indexes by hand.
- `install-posters` installs only explicitly selected registered pairs. It never
  replaces the gallery directory or writes its index, and refuses to replace any
  existing PNG with different bytes. Identical retries/concurrent installers are
  safe. Old manual pixels, source URLs and original formal unknowns stay intact.

## Fixed migration included; refresh it before final integration

This candidate commits `registry/baseline.json` and 217 immutable model records
from the exact source above. No binary is copied. If ordinary releases advance main
before integration, replace this **not-yet-activated migration** with an import of
that then-current exact release, and compare again. Do not merge an older migration
snapshot over a newer release. After activation the baseline is frozen; future
batches append their own records instead of replacing it.

The reproducible import command requires an exact full commit, not a moving branch
name, and a new output directory:

```sh
node site/model-registry-cli.mjs import \
  --repo /path/to/repo --commit FULL_40_CHARACTER_SHA --out /tmp/records
```

The importer reads original Git objects rather than replacement refs. It requires
a lossless semantic round-trip of all five old metadata shapes. It does not execute
a release gate or authenticate approval. Copy the resulting `registry/` into the
isolated migration branch after its comparison has passed. The generator and
incremental logic do not hardcode a model count.

## Use the existing collector, then generate the indexes

The current release collector remains responsible for the release manifest's
model values, order and publication headers. Generate that manifest by the existing
release process first. The bridge requires its ID set and every complete asset
value to equal the per-model records; it preserves its exact array order and
headers. The registry cannot add an unselected model, turn `unknown` into `pass`,
or supply its own replacement publication authority.

```sh
node site/model-registry-sync.mjs sync \
  --registry-root /path/to/repo \
  --release-manifest /path/to/collector-manifest.json \
  --target-root /path/to/repo
node site/model-registry-sync.mjs check \
  --registry-root /path/to/repo \
  --release-manifest /path/to/collector-manifest.json \
  --target-root /path/to/repo
```

The repository now provides these direct entries, defaulting to its own committed
records and existing collector-generated manifest:

```sh
npm run registry:sync
npm run registry:check
npm run registry:posters -- --source-root /path/to/checked-source --model-ids model-a,model-b
```

`npm run build` first executes the unchanged publication gate, then requires a
read-only registry check before Vite. The final `audit-release.mjs` repeats the
same check, including when Pages or the full-review audit consumes a reused build.
No build/audit command silently rewrites source JSON. Missing registry records or
generated-index drift stop the build; an approval/reference flag cannot waive it.

The manifest can also be the existing `assets/manifest.json` after the collector
has generated it. This reference is **data**, not proof that checks ran. The bridge
does not issue an admission handle or approval receipt. Continue running the
unchanged `publication:check`, gallery/poster, source, independent QA and release
checks. A fabricated reference manifest does not bypass those checks.

`sync` writes only:

- `assets/manifest.json`
- `site/catalog-data.json`
- `assets/turntables/index.json`
- `site/public/gallery/resources.json`
- `site/gallery/wheel-framing.json`

Already semantically equal JSON is not rewritten, preserving its original bytes.
New models' actual GLB/editable source/preview, gallery, optional descriptor/frame/
card and evidence bytes are checked against their record hashes before any JSON
write. Existing checks continue protecting historical payloads and approval.
Gallery headers retain the imported capture history; the bridge never invents a
new full-gallery capture session or rewrites approval files.

The coordinator runs `sync` once after combining disjoint records. An exclusive
local lock rejects overlapping syncs; the writer checks its input file state again
before renaming. Renames are per-file, **not a five-file transaction**. If interrupted,
rerun `sync` and `check` before existing release checks; inspect any leftover lock
rather than assuming its owner is dead. There is no remote queue executor.

Do not deploy the raw catalog previews from the older `compose` command.
Production `copy-assets.mjs` is unchanged and still performs actual asset/download,
file-size, card and turntable enrichment before `writeCatalog`.

## Install only a selected poster pair

For existing reviewed source data, use the same source tree whose evidence the
current release process has already checked:

```sh
node site/model-registry-sync.mjs install-posters \
  --registry-root /path/to/repo --source-root /path/to/checked-source \
  --target-root /path/to/repo --model-ids model-a,model-b
```

The installer verifies source GLB bytes, canonical owner paths, exact PNG SHA-256,
byte counts, dimensions and transparency against the selected record. All selected
inputs and existing targets are checked before installation. It only adds missing
`site/public/gallery/posters/<id>[-wheel].png` files. It does not copy source scripts,
change records, merge a stale gallery snapshot, or write `approved-poster-inputs`.

The same installer can consume explicitly selected packages from the independent
capture writer, adding these options:

```sh
  --packages-root /path/to/captures --package-refs model-a/PACKAGE_SHA256,model-b/PACKAGE_SHA256
```

Each package must exactly match that registered model's asset metadata, poster and
seals. `--source-root` still supplies source GLB bytes. No package directory is
implicitly selected as approved. Capture packages remain `unverified-model-capture`;
installation returns `publication_authority: false`. The existing poster checks
must accept their recipe/provenance before release. The separately tested opt-in
renderer hook is not included or activated by this minimal bridge commit.

## Existing incremental pipeline, not a new cache policy

`ci-scope.mjs` recognizes only canonical published-ID record paths and new batch
JSON as model data. The subsequent existing `assessIncrementalDiff` is stricter:

- It needs the exact prior Git path inventory and actual new record bytes.
- A changed existing baseline, record or batch cannot qualify as an append.
- Every new manifest ID needs exactly one new content-addressed canonical record;
  its complete metadata must match the current generated five-file snapshot.
- New batch descriptors must claim those records exactly once. Unknown keys,
  duplicate owners, foreign IDs, unbound records and executable/unknown registry
  paths fail closed and require the existing full validation path.
- Current source/QA/publication checks still decide whether additions are accepted.
  These checks only determine eligible work scope; they issue no reusable proof.

A fixture passes two independent registry batches/four new models through the
actual existing incremental eligibility and acceptance-plan functions. With an
independently compatible synthetic baseline, the old models remain reusable and
exactly the four new IDs are fresh. This demonstrates the new record paths no
longer accidentally force full work; it is not a new real GPU acceptance result.
Missing/incompatible baseline evidence still forces full validation.

The 217-model manifest is 1,218,478 bytes, exceeding Node's default 1 MiB Git
stdout buffer. The scope CLI now sets an explicit 16 MiB bound on its Git reads
so ordinary catalog growth does not accidentally discard valid diff provenance.
Its real-CLI fixture checks a 217-model predecessor plus one owned new record stays
scoped, while missing provenance and a source over 16 MiB still fail closed to full
validation. This changes a read limit, not a proof or publication requirement.

This integration changes shared executable code and therefore **must get a fresh
normal shared baseline** before later data additions can reuse it. It adds no
policy hash exemption. Explicit full-review/main-push behavior remains unchanged.
Existing batch-specific collectors and frozen descriptors still constrain new
publication. Some future batches still require those code/data updates; a new or
shared collector outside the existing recognized roles can require full review.
This change does not solve that by introducing a generic approval producer.

## Validation and actual scope

Run the bounded storage/projection tests:

```sh
node --test site/model-registry-test.mjs \
  site/model-capture-package-test.mjs site/model-registry-sync-test.mjs
```

The original 66 storage/projection tests passed, including actual two-worker disjoint record files combined on
disk, deterministic union without manually editing aggregate indexes, real CLI
sync/check, collector order/value constraints, failed input preflight, symlink/
lock rejection, immutable source and optional-resource checks, package-to-poster
installation, seven-model installation, and simultaneous independent installers.
Synthetic PNG fixtures test storage/contracts, not rendering or artistic quality.

The original storage comparison and the refreshed migration comparison are recorded in
`docs/model-registry-lite-validation.json`:

- Exact `db94a64d04a578a7a2e8feaa46b9b4480354b33d`: 194 models imported, stored,
  read back and composed; all five source JSON values equal and original JSON
  bytes unchanged after `sync`/`check`.
- Seven existing IDs installed as 14 PNGs from that exact source, every byte read
  back equal to the old source seal; a second install writes zero files. Shared
  JSON files remain unchanged. This is not a new render or approval operation.
- No full production delivery comparison was rerun in this small step. The existing
  delivery/build code is unchanged; source-projection equality is not a claim that
  a new deployed site or a newly approved release was produced.

The isolated candidate now contains the migration and hooks rather than only CLI
files. The refreshed exact `da3fb30ccc4dd4e511e029c0a51a7a67265870c5` comparison
imports 217 records and confirms all five existing JSON byte sequences remain
unchanged after `registry:sync`/`registry:check`; sync writes zero files. No source
payload, poster PNG, production evidence, publication collector or workflow is
changed. This conclusion uses exact Git metadata/object equality, not a second
copy or full rescan of the binary corpus. The older seven-model poster install
above remains evidence for its original 194-model snapshot, not a new 217-model
render or installer run.

The same local candidate includes the desktop thumbnail-axis patch from
`70f94fecefe9ab1aa52f76eb427c32177d1aa871`. Its four files apply without conflicts
and exactly match that source commit: `site/gallery/main.js`,
`site/gallery/startup.js`, `site/gallery-startup-test.mjs` and
`site/gallery-thumbnail-axis-browser.mjs`. Only the two desktop paint expressions
change runtime behavior, keeping horizontal displacement at zero while preserving
scale/opacity and the existing mobile CSS offset. The two existing test files
assert that common axis; no additional UI policy or rendering layer is introduced.

The combined targeted run passed 73/73 tests. It includes the six registry/scope/
incremental/build test files plus gallery startup, thumbnail queue, focus centering
and navigation contracts. It retains mandatory publication/audit failures and
registry-check failure propagation. The actual candidate diff classifies as full
shared model/preview work (`runtime: true`, empty scoped IDs), not an append-only
shortcut. Existing registry-baseline and shared code changes are intentionally not
exempted. After the bounded-buffer correction, the scope CLI test passed again and the actual
combined diff selected full work without a missing-provenance fallback. Syntax and
diff checks pass. No browser run or complete production
build/renderer/QA run was repeated for this combined candidate; the desktop patch's
separate browser evidence used the earlier 194-model release.

Actual activation remains an ordinary reviewed integration after the current
release, using its updated source snapshot and the normal CI checks. No main merge,
deployment, remote queue or future-batch producer has occurred. Rollback can revert
the migration/hooks while keeping existing aggregate files and binary URLs.
