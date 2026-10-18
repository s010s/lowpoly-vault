# Candidate evidence contract, version 1

`python scripts/validate_candidate.py candidates/<asset>/<revision>/candidate.json --json`
validates a candidate record against real files. Relative paths resolve under the
repository root, or an explicit `--root`. `--require-approved` additionally requires
an independent `approved_for_brief` decision. Exit 0 without that flag can mean
**valid, pending or rejected**; read `approved_for_brief`, not merely the exit code.
The command is read-only and never publishes.

The executable contract is `scripts/validate_candidate.py`; behavioral examples
are generated only in temporary directories by `scripts/test_validate_candidate.py`.
No synthetic test record is an approval of a real asset.

## Freeze the inputs

Copy `templates/candidate.template.json`, `brief.template.json`, and
`references.template.json`. Templates are intentionally pending and non-executable:
replace paths, hashes, null ceilings, identities, sources and subject-specific
criteria before validation. `textured-brief.example.json` illustrates budgets for
one possible textured prop; its numbers are neither global ceilings nor quality
recommendations. The required style may use rich texture detail and higher budgets.

The candidate requires:

- `schema_version: 1`, stable `asset_id`, immutable `revision`, and
  `maker: {id, task_id}`.
- `artifacts.glb`, `.brief`, `.references`: `{path, sha256}` for exact file bytes.
  Additional artifact roles use the same descriptor and are also hash-checked.
- A production brief freezes `required_deliverables`: entries containing `role`,
  `path`, `sha256`, including `source`, `generator`, and `config`. They must exactly
  match candidate artifact descriptors. This binds editable source, reproducible
  build/export recipe, and configuration through the brief checksum.
- `textures`, `evidence`, all seven `stages`, `blockers`, and `approval`.
- Optional `supersedes: {path, sha256, revision}` links an immutable prior record
  for the same asset and a different revision. Preserve prior bundles. The
  optional `--previous <snapshot.json>` rejects changed artifact/texture inputs
  under the same revision. It does not require review statuses to stay frozen.

Use a new revision when GLB, source, generator, configuration, brief, or reference
inputs change. Bind review to a subject object containing exactly:

```json
{
  "revision": "v001",
  "glb_sha256": "<actual SHA-256>",
  "brief_sha256": "<actual SHA-256>",
  "references_sha256": "<actual SHA-256>"
}
```

Neither a mutable `latest` pointer nor an unchanged filename establishes identity.
Paths must be contained relative paths with no parent traversal or symlinks.
Duplicate JSON keys, nonfinite values, missing files and checksum drift fail.
The gate cannot detect a history that was never retained: use version control and
immutable bundle storage, plus `--previous`, rather than claiming JSON is a lock.

## Frozen brief and reference ledger

The brief requires `schema_version`, matching `asset_id`, `brief_version`,
`profile` (`study` or `production`), `publication_authority: "separate"`,
`required_stages`, `criteria`, `required_views`, `turntable_frames`,
`geometry_policy`, and `texture_policy`.

Each criterion has `id`, `stage`, `critical` boolean, substantive `description`,
and `required_sources` IDs. Every required stage has explicit criteria. At least
one critical factual obligation needs a nonempty required-source list. Optional
noncritical criteria may set `allow_not_applicable: true`; a critical obligation
cannot be waived. Each criterion gets an explicit outcome in its stage.

The reference ledger is `{schema_version: 1, sources: [...]}`. Every source has a
unique `id`, `title`, `url`, and `license` (which may explicitly say reference-only
or unknown). Optional `local: {path, sha256}` freezes a saved source/image as well.
A reference link does not grant permission to redistribute a texture.

Geometry policy requires positive integer `max_triangles`, `max_materials`,
`max_primitives`, `max_glb_bytes`. Texture policy requires nonnegative integer
`max_textures`, `max_dimension`, `max_total_bytes`, and optionally
`max_decoded_bytes`. All are brief-specific constraints. Zero texture limits mean
an explicitly texture-free brief, never an implicit default for all assets.

The gate measures the shipped static, uncompressed GLB with the existing project
auditor. Unsupported geometry profiles cannot be approved through this gate.
Reported triangle/material/primitive/GLB-byte counts must match those independent
measurements. Every embedded image requires a `textures` entry:

```json
{
  "image_index": 0,
  "path": "candidates/example/v001/textures/exported-image-0.png",
  "sha256": "<actual embedded-image SHA-256>",
  "width": 1024,
  "height": 1024,
  "byte_length": 123456,
  "provenance": {
    "source_id": "original-surface",
    "creator": "Identified creator",
    "license": "Actual reuse license",
    "usage": "Purpose and permitted use"
  }
}
```

The image file must equal the actual GLB embedded-image bytes. Dimensions and byte
counts are measured. `max_textures` counts embedded images. Decoded memory is an
explicit RGBA8/full-mip-chain estimate per image, not measured device allocation;
it excludes driver overhead, duplication and device-specific compression.

## Stage decisions and independence

The seven separate stages are `technical`, `visual`, `factual`, `specification`,
`runtime_parse`, `gpu`, `scene`. Core technical/visual/factual/specification/parser
stages are always mandatory. Production additionally requires GPU and composed
scene checks. A brief may add required stages; it cannot remove these core checks.
Critical criteria also make their stage mandatory. Missing hardware is `unknown`,
not `pass` or a production waiver.

Each stage contains:

- `status`: `pass`, `fail`, `unknown`, `not_applicable`, or `stale`
- `note`, `reviewer`, `subject`, `evidence` IDs, `inspected_references` source IDs,
  and `criteria: [{id, status, evidence: [...], note}]`
- For `pass`, an ISO `reviewed_at` with timezone and a nonempty structured passing
  report. Every passing criterion has evidence; its required sources must be
  included in the stage's inspected-reference list.
- Visual additionally needs `inspected_frames` covering the entire render manifest.

Visual, factual, specification and final approval reviewers must have both an
identity and task different from the maker. Technical/runtime automation may use
an identified tool and the maker's task. These are traceable attestations; the
validator cannot authenticate people or prove someone actually looked at pixels.

`approval.status` is `pending`, `rejected`, or `approved_for_brief`. Approval needs
an independent reviewer, exact subject, `reviewed_at`, note, and
`review_snapshot_sha256`. Compute the snapshot with
`validate_candidate.approval_snapshot_sha256(record)` only after actual review:
it binds artifact descriptors, maker identity, texture provenance, evidence
descriptors, stage decisions, blockers and supersedes. Changing a reviewed report,
criterion or image invalidates the prior final decision. Computing a digest is an
integrity seal; it is neither review nor authorization. Any open blocker,
missing required stage, unresolved criterion, stale hash, budget failure or missing
evidence rejects an approval claim. A structurally honest failed/pending record
remains valid. `not_applicable` is permitted only within the frozen brief's scope.

## Evidence files

An evidence descriptor has `id`, `kind`, `stage`, `path`, `sha256`, `subject`.
Allowed kinds are `rendered_image`, visual `render_manifest`, or the stage-specific
report kind:

- technical: `technical_report`
- visual: `visual_report`
- factual: `reference_comparison`
- specification: `spec_report`
- runtime_parse: `runtime_parse_report`
- gpu: `gpu_report`
- scene: `scene_report`

A report's own JSON repeats `schema_version: 1`, `kind`, `stage`, `subject`,
`status`, substantive `method`, and nonempty `observations`. A passing report has
`errors: []`. Every warning requires `warning_review: [{warning, rationale}]`.
Descriptor-only relabeling does not turn unrelated reports into evidence.
Every passing report also freezes `reviewed_evidence: [{id, sha256}]` for every
non-report item cited by its stage (render manifests/images/screenshots). An empty
list is explicit when there are no such items. Report self-hashes are excluded to
avoid cycles. A newly hashed image/manifest cannot inherit an unchanged old review.
The final approval snapshot additionally binds all report hashes and stage decisions.

Passing technical reports contain `measurements` with `triangles`, `materials`,
`primitives`, `glb_bytes`, `texture_count`, `texture_max_dimension`, `texture_bytes`.
They must also contain these named `checks`, each with a distinct hashed raw
`report: {path, sha256}`, `status: "pass"`, exact `glb_sha256`, and warning reviews:

1. `static_glb`: actual project audit output, exact GLB `sha256`, no errors. Its
   status, errors and warning multiset must match the gate's newly computed audit;
   suppressing a current warning cannot bypass explicit warning review.
2. `khronos_validator`: official validator output with `validatorVersion`,
   `issues.numErrors: 0`, full `messages`, matching warning count and
   `truncated: false`. The check wrapper binds its raw report to the GLB.
3. `source_export`: `status: "pass"`, `glb_sha256`, `source_sha256`, `errors: []`,
   `triangles_match: true`, `bounds_match: true` from the actual axis-aware check.
4. `reproducibility`: `status: "pass"`, `glb_sha256`, `generator_sha256`,
   `config_sha256`, `errors: []`, `semantic_sha256`, `rebuilt_semantic_sha256`.
   Both semantic digests must match the independently decoded current GLB.
   Also requires `rebuilt_glb_sha256` and
   `build_run: {request: {path, sha256}, result: {path, sha256}, output}`.
   The raw request/result must bind a successful build-lane queue run, matching
   identity fingerprint, exact generator/config inputs explicitly used by argv,
   and the rebuilt output digest. Merely supplying a copied second GLB establishes
   equality, not a rebuild, and cannot satisfy this provenance requirement.

Store real observations/reports; never generate a passing wrapper from this list
without running the checks. The checker enforces their structure and integrity,
not the truth of an unsupported assertion.

Parser reports require `runtime: {engine, version, loader, parsed: true}`. GPU and
scene reports instead require runtime `engine`, `version`, `renderer`, `device`,
`browser`, `context`, `output_color_space`, `tone_mapping`, numeric `exposure`,
`context_created: true`, `rendered: true`, positive `rendered_frames`, `draw_calls`,
`triangles`, and `screenshots` naming same-stage hashed rendered-image evidence.
A parse-only report cannot pass by changing its kind. Scene reports also need
`scene_description` and `scene_assets` including the exact candidate `glb_sha256`
with positive `instances`. A browser render does not establish anatomy.

## Executable raw-report producers

Source/export comparison reads the exact editable source with script autoexecution
disabled, identifies its unique asset-root-marked export collection (or an explicit
`--collection`), evaluates actual geometry, and compares triangles and axis-mapped
bounds within 0.0001 m. It never saves the source, re-exports the GLB or reads old QA
metadata as proof:

```sh
blender --background --factory-startup --disable-autoexec --python-exit-code 1 \
  --python scripts/check_source_export.py -- \
  --source candidates/example/v001/source.blend \
  --glb candidates/example/v001/model.glb \
  --output candidates/example/v001/evidence/source-export.report.json
```

Rebuild comparison never executes the generator. Supply a separately produced GLB
and the successful bounded-queue build request/result that created it. The queue
job must declare `generator` and `config` file inputs and explicitly pass their
paths in its resolved argv. Report descriptors are relative to `--root`:

```sh
python3 scripts/check_reproducibility.py \
  --glb candidates/example/v001/model.glb \
  --rebuilt-glb runs/build/example/v001/rebuild/attempt/outputs/model.glb \
  --generator candidates/example/v001/generator.py \
  --config candidates/example/v001/build-config.json \
  --build-request runs/build/example/v001/rebuild/attempt/request.json \
  --build-result runs/build/example/v001/rebuild/attempt/result.json \
  --rebuilt-output model.glb --root . \
  --output candidates/example/v001/evidence/reproducibility.report.json
```

Without build provenance, matching separately supplied geometry yields `unknown`
and exit 2. A mismatch or failed/mismatched run record fails. Same-file and hardlink
self-comparisons fail. A bound successful run plus semantic equality may pass this
technical subcheck; queue records are still auditable attestations, not proof
against forged records or a malicious generator. Both producers create new report
paths exclusively and refuse to overwrite existing evidence. Hash those raw reports
into the technical report; review every actual warning. No candidate review status
is changed automatically.

`python3 scripts/test_technical_reports.py -v` exercises actual temporary GLB files,
axis/count mismatches, semantic/material changes, unchanged inputs, missing/failed
run provenance, output/input hash binding and no-clobber behavior. Blender loading
is a separate integration check; the pure test suite does not claim to run Blender.

## Complete visual coverage

The frozen brief lists named `required_views` plus `turntable_frames`. Production
requires front/rear/left/right/top/bottom/clay/wire/detail. A subject with no
applicable detail may use `view_exemptions: {detail: "Specific explanation"}` and
omit `detail` from required views. Other canonical diagnostic views cannot be
waived. The default template plans 24 turntable views, but fewer may be justified
with `coverage_justification`; the frozen count and full angular coverage remain
mandatory. A full orbit needs at least two distinct positions. Sample count is
never an automatic quality score.

The visual `render_manifest` file contains `schema_version: 1`, `kind`, `stage`,
exact `subject`, `render_config: {path, sha256}` and `frames`. Each frame includes
`id`, `path`, `sha256`, `view`, `angle_degrees: [azimuth, elevation]`, `width`,
`height`, `byte_length`. **Config/frame paths resolve relative to the manifest's
own directory**, while candidate evidence paths resolve from the selected root.
PNG, JPEG and WebP (VP8, VP8L, VP8X) dimension headers are supported. Header checks
are not full image decoding or pixel inspection. Unsupported formats fail clearly.

The hashed render config records `renderer`, `version`, `color_management`,
`lighting`, `camera`, and the complete planned `frames` (`id`, `view`, angles).
Every manifest frame must match that plan. Canonical camera angles match the
renderer: front `[0,0]`, right `[90,0]`, rear `[180,0]`, left `[270,0]`, top `[0,90]`,
bottom `[0,-90]`. Orbit frames cannot collapse to a pole or cluster on one side.
A partial manifest can be stored on a pending/failed candidate. A visual pass
requires every declared frame, every required view, enough distinct orbit angles
without oversized gaps, verified dimensions/bytes/hashes, and an explicit
`inspected_frames` list containing all frames. It still requires a separate visual
report and independent judgment against the references.

## Release boundary and regression checks

`site/generate-manifest.mjs` invokes this gate with `--require-approved` for formal
releases via `metadata.candidate_record`, then verifies the production profile,
asset ID, exact shipped GLB/source digests, measured triangle count, and a published
preview included in approved visual evidence. Candidate approval grants no publication
authority. Preview-only manifests are review artifacts. The separately authorized
initial-ten path remains byte-locked and explicitly `work_in_progress`; this
change does not promote or re-approve those original models.

```sh
python scripts/test_validate_candidate.py -v
python scripts/test_technical_reports.py -v
node site/manifest-test.mjs
node site/initial-release-test.mjs
node site/initial-release.mjs --check
```

Tests intentionally include fabricated/mutated fixtures so the gate's rejection
behavior is observable. Passing synthetic tests are evidence about the gate,
not evidence that any production model looks good or is factually correct.

## Explicit environment-prop tier

A production brief with quality_tier environment-prop retains all seven stages but permits turntable_frames zero with a coverage reason. It requires hero/front/right/rear/top/clay; extra detail views are need-driven. Old briefs without this opt-in keep their full-view/orbit requirements. The practical Skill defines stylized-inspired claim scope, advisory uncertainty and bounded review.
