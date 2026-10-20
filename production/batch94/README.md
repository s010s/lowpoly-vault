# Batch 94: four bounded static prehistoric plants

This is a local maker handoff, not independent acceptance, a publication grant or proof of GPU/composed-scene behavior. The selected deliverables are indexed by `final-selection.json` and `handoff-assets.json`.

- Rhacophyton r002: an explicitly interpretive sterile historical spiral reconstruction, not settled phyllotaxy. The failed r001 had forklet bases off the curved pinnae; original source and measurements remain local. r002 changes the actual attachment geometry, not the original brief.
- Sigillaria r001: one unbranched ribbed Rhytidolepis-type genus-level habit, not a species-exact reconstruction. The first center-only/ray checker produced false negatives at a cap and two ray seams; actual closed-surface base-ring measurements are retained separately and pass without geometry alteration.
- Pseudobornia r001: a two-metre artistic juvenile, interpreted from detached primary fossils. Four-leaf whorls occur only on thin terminal axes; sterile, no new claim about fertile organ association.
- Calamites r001: genus-level woody vegetative reconstruction. The external trunk does not copy internal pith-cast ribs as asserted bark; associated Annularia-like foliage is not a separate asset or asserted exact organ species association.

## Reproduction and dependencies

The four selected folders each contain editable `source.blend`, standalone static `model.glb`, exact `generator.py`, `build-config.json`, frozen original `brief.json` and `references.json`, and a clearly derived `candidate-brief.json` that only adds postbuild source/generator/config hash closure. Original 22:54:47 freezes are unchanged.

Each generator resolves the repository's `scripts/asset_common.py` and `scripts/qa_glb.py`; those exact two support files are already tracked in the base commit and their SHA256 values are pinned in `build-dependencies.json`. No mesh, pixel or texture input is required. Use Blender4.3.2 and the pinned seed/config. An example command, from repository root:

    flock /tmp/lowpoly-production-blender.lock /usr/bin/blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 --python production/batch94/assets/rhacophyton/r002/generator.py -- --config production/batch94/assets/rhacophyton/r002/build-config.json --output /absolute/new-output-directory

Never select an existing output directory containing a model. Each selected asset has two separately executed, queue-bound rebuilds with distinct actual Blender PIDs, request/result/output provenance and byte-identical GLBs. Full run outputs stay local; compact exact request/result/execution copies are under `rebuild-evidence/`. Source reopen compares actual evaluated counts and world bounds with the selected GLB. Node Three.js0.180.0 parsing and Khronos validation are separate from device rendering.

## Evidence and limits

The final GLB, derived brief and original references were fixed and prechecked before every new final512px proof frame. All32 individual frames were personally opened. Lossless contact sheets only arrange the original pixels, without resampling. Actual world-space counts, bounds, solid topology and attachment base measurements are included. Artistic dimensions are explicitly nominal, never retroactively treated as hard equalities; hard counts and technical ceilings remain enforced.

All seven stage records are distinct. Automated checks and maker inspection do not constitute independent acceptance. GPU and composed scene were not run. Provider internal ImageGen timestamps and exact first authoring keystroke time remain unknown; observed invocations, return intervals, freezes and executions are preserved rather than inferred from mtimes.

The copied historical `publication-policy.json` is a schema reference only. Current task authorization permits no upload, PR, merge or deployment; any future action remains subject to the owner's current exact scope and platform mandatory approvals. `source_url` remains null until an authorized upload is actually verified.

Raw third-party source PDFs/photos remain consult-only outside Git. Earlier diagnostics, failed geometry and full queue outputs remain locally preserved and are indexed by the local preservation inventory. No original evidence was deleted to fit the lean payload. No duplicate ZIP is added.
