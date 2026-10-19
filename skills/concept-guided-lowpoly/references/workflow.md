# Production and evidence recipe

## A small, preserved bundle

Keep each revision in an isolated directory. Start with
`assets/concept-brief.template.md` and `assets/concept-evidence.template.json` from
this skill. The JSON is deliberately incomplete: fill real paths, hashes and
observations; null timestamps mean unknown, not permission to invent history.
This sidecar supplements the existing [candidate contract](../../../schemas/README.md).
It is not a new production profile and does not relax either existing profile.

Suggested files: original concept image and exact prompt; generation record;
frozen brief and reference ledger; generator and configuration; `.blend` and
`.glb`; source/build logs; exact-GLB proof manifest/config/frames; raw QA reports;
review note; concept evidence sidecar. Optional bilingual labels do not change IDs.
For a retrospective bundle, set an unavailable `concept.generation_record`,
`render_manifest`, `thumbnail` or `review_note` to JSON `null`. These remain explicit
completeness blockers, not structural errors or inferred passes. Never write a
retrospective narrative as though it were the missing original tool receipt.
Existing timestamp gaps likewise remain null. A later render is a new run with its
own provenance; it cannot be backdated to fill a historical render manifest.

The generation record should retain the actual ImageGen invocation/result identity,
available timestamps and saved output identity. Do not claim a seed or model
version that the tool did not disclose. Filesystem mtimes are not chronology proof.

Use `asset_common.py` for new modeling/export code where applicable. Keep asset
geometry separate from presentation geometry. The existing
[source/export and reproducibility tools](../../../schemas/README.md#executable-raw-report-producers)
check the saved source against the GLB and a separately executed deterministic
rebuild. A retained generator alone does not prove reproducibility.

## Reuse the actual GLB renderer

From the repository root, with Blender available, choose a new empty output folder:

```sh
blender --background --factory-startup --disable-autoexec --threads 2 \
  --python-exit-code 1 --python scripts/render_candidate_views.py -- \
  studies/example/r001/model.glb --revision r001 \
  --brief studies/example/r001/brief.md \
  --references studies/example/r001/references.json \
  --output-dir studies/example/r001/proof \
  --views hero,reversehero,right,top --turntable-frames 0 \
  --resolution 512 --samples 32
```

This study command imports the exact GLB, freezes hashes/configuration and creates
four proof frames. It does not meet all required views of a formal candidate by
itself: select that profile's complete frozen coverage when preparing one. The
renderer accepts any brief file for hash binding; formal candidate validation
requires the established JSON brief schema. Retain a prose concept brief as an
additional artifact when a formal JSON brief is used.

Map canonical front/right/top to the asset’s actual forward axis before choosing
views. A geometric +X camera can be an end view for an X-aligned fish; naming it
“side” does not establish lateral anatomy coverage. The existing renderer expects
the project’s Blender -Y-forward convention.

For the historical pilot, `rear` and `top` are oblique poses. In a retrospective
record use descriptive view labels `rear-oblique` and `top-oblique`, preserving
actual transforms and original filenames/hashes. These are evidence labels, not
aliases accepted by the existing renderer CLI. Do not invent canonical angles to
make the manifest validate. R2 matches the same R1 cameras, so it inherits the
same caveat. Missing historical manifests and receipts stay null/incomplete.

Inspect the images. The static checker cannot establish actual volume, clean
intersections or likeness. Inspect rear/top/side thickness and connections; use
clay/wire views and mesh checks when needed. Intentional separate closed fish
parts can overlap without becoming a printable single solid. Declare such limits.
Keep final thumbnails as a rendered frame or a documented resize of one. The
supplemental checker deliberately supports only an exact proof-frame thumbnail:
render at the required size or retain the original frame for that check; any
separate derivative needs its own source-hash/transformation record and review.

The existing renderer uses fixed orbit framing within a run but refits bounds for
a new model. Reusing CLI flags alone does **not** guarantee revision-matched
framing: compare render configs, lock the baseline camera/target/scale and light
transforms in the study renderer if bounds change, and retain the actual settings.
Match exposure, transform, lights, background and samples. Document intentional
presentation changes separately from geometry improvements.

## Format and evidence checks

Official Khronos validation requires the repository's declared `gltf-validator`
devDependency to be installed and resolvable. A sparse checkout without installed
dependencies can exit 2 for missing tooling; that is not an asset validation
failure. Use the project's normal lockfile-based setup, or point `NODE_PATH` to
an already installed compatible official package; record its version. Then run:

```sh
node scripts/validate_gltf.cjs studies/example/r001/model.glb
python3 scripts/validate_concept_evidence.py concept-evidence.json \
  --root studies/example/r001 --require-complete
python3 scripts/test_concept_evidence.py -v
```

The Khronos command writes `gltf-validator.report.json` and `qa.json` beside the
GLB. Run it before freezing the bundle and use a separate folder per asset; it
can replace those files, so never run it over an immutable historical bundle.
Copy the validator's exact GLB SHA-256 from `qa.json` into the sidecar binding.
Record and review every warning. Run the repository's existing source/export,
rebuild, candidate and runtime checks separately when their acceptance is needed.

The supplemental helper is read-only and needs only Python's standard library
plus the repository's existing helper modules. All sidecar paths resolve under
`--root`, with no absolute paths, parent traversal or symlinks. Render config and
frame paths retain the existing rule: relative to the render manifest directory.
Hashes are SHA-256 of exact file bytes (for example `sha256sum FILE`).

It checks:
- Required source/generator/configuration/brief/reference and original-concept files
- Original concept image headers, prompt and generation-record hashes
- Recorded concept generation → inspection → model-start ordering
- Existing render-manifest subject hashes, configuration, planned views, image
  dimensions/bytes and actual image hashes, plus distinct proof angles
- A thumbnail identical to a declared exported-GLB frame; concept substitution fails
- The full recorded frame-inspection list and hashed review note
- Fresh static GLB metrics and bound full Khronos output with warning reviews
- Explicit measured/unrecorded/not-run stage timings; measured times need a source file
- A study-specific advisory byte target without enforcing a universal quality cap

`valid: true` means the sidecar is internally consistent. `evidence_complete: true`
means these study evidence obligations are present, including recorded chronology
and inspection coverage. Neither result is artistic acceptance, demonstrated tool
authenticity, source/rebuild parity, browser acceptance or a release decision.
The first pilot lacks a separately persisted ImageGen invocation/result receipt
and the new renderer-format hash-bound manifest. Its genuine prompt and image are
retained, but these historical gaps must stay incomplete in retrospective records.
Prospectively, capture the real tool receipt and use the manifest-producing renderer.

A complete sidecar can correctly say target-browser timing `not_run`; the output
always says runtime QA was not checked by this tool. The existing candidate gate
remains the only repository approval route. A false recorded inspection cannot
be made true by hashing it. Inspect actual pixels and primary source records.

Exit 0 by default accepts an honest valid-but-incomplete record; `--require-complete`
returns nonzero if chronology/coverage/static validity is incomplete. Invalid
hashes, unsafe paths or contradictory claims always return nonzero. Over-target
bytes produce an advisory. Unknown historical timings remain null and do not
become speed claims. Synthetic test fixtures exercise rejection behavior only.

## Review before expansion

Review silhouette, proportions, material grouping, secondary structure and
alternate-view completeness against the brief. Record the location and severity
of each gap, then choose a bounded structural revision. Compare under matched
presentation and retain both versions. For this pilot the specific gaps were
straight coral branches, angular fish face/fins and a regular rock band.

User review of the representative set comes before a larger production batch.
Record factual-source limits, license/provenance, and every unrun target-browser,
GPU, populated-scene or rebuild check. Do not manufacture passing reports to fit
a schema. Do not treat smaller files or higher triangle counts as proof of art quality.
