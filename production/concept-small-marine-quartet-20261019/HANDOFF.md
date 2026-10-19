# Four small marine candidates — parent handoff

Cloud-only maker delivery. Candidate production is complete; independent acceptance and release remain with the parent. No main merge, PR edit, force push, branch deletion, permission change, Google Drive operation, or user-computer operation was performed. PR20 remains untouched and paused. Published counts and site/catalog files are unchanged.

Branch: `candidate/small-marine-quartet-concept-20261019`.
Base main: `f8d1fa6a1b58e70728aa30852f08ecb38043314f`.
Exact selected paths, hashes, dimensions, licenses and poster instructions: `selected-models.json` and each selected revision's `integration-metadata.json`.

| Inventory ID | Selected revision | Triangles | GLB bytes | glTF XYZ size, meters |
|---|---|---:|---:|---|
| emeraldella | r002 | 2,996 | 202,492 | 0.054570 × 0.021623 × 0.140179 |
| burgessia | r002 | 1,862 | 124,420 | 0.020955 × 0.005789 × 0.044137 |
| tuzoia | r003 | 2,176 | 152,604 | 0.069401 × 0.066010 × 0.153276 |
| sanctacaris | r002 | 3,604 | 250,108 | 0.052000 × 0.024020 × 0.100456 |

Every selected folder contains the editable Blend, exact GLB, frozen brief/configuration, factual ledger, source/export comparison, two bound deterministic rebuild reports, Khronos output, Three.js Node parse, authored/evaluated topology counts, actual exported-GLB proof frames/manifest/configuration, maker inspection, and concept-evidence integrity check. Code and raw queue records are retained at batch level. Original art/renders/prose: CC BY 4.0, Leon Made This / s010s. Executable code: MIT. No ROM image/model/texture/code was reused.

## Selection and concept provenance

`selection-evidence.json`, `remote-heads.txt`, `remote-pr-heads.txt`, and `claim.json` preserve the actual snapshot. All 270 branch heads and 26 PR heads were fetched; 297 remote references (including origin/HEAD) and 436 unique task-registration blobs were scanned. These four IDs had no GLB or registration occupancy. Sidneyia was considered then rejected because an old batch candidate occupied it. All seven named PR24 additions, ctenoimbricata and paused PR20 were excluded. GitHub's GraphQL PR list returned Forbidden; Git's complete advertised PR-head references provided the alternate inspection route.

`concept-original.png` is the genuine generated design sheet. `concept-prompt.txt`, `concept-generation.json` and `events.jsonl` retain actual prompt/tool identity, invocation/return/inspection times and pre-model brief chronology. No retrospective timestamps or seed/model version are invented. The generation tool did not disclose a seed or model version. Twelve original design panels were viewed before construction; concept inconsistencies were resolved in each brief.

## Adopted visible changes

R001 is retained for all four. R002 replaces hard antenna elbows with continuous tapered arcs in the first three creatures, and rectangular head tabs with swept triangular Sanctacaris wings. Comparisons visibly show these changes. Tuzoia R003 additionally adds an explicit projecting head: its R001/R002 anterior eye/antenna roots lacked a visible connection. R003 fixes that issue and is the selected Tuzoia. Do not select earlier Tuzoia revisions.

`revision-presentation-check.json` confirms exact camera targets/scales, lights, color settings, samples, background and resolution match the R001 baseline. The `concept-match` camera (55° azimuth, 32° elevation) is an authored approximation of the ImageGen illustration, which has no calibrated camera; it is not a recovered measurement. Each candidate has twelve actual clean-import GLB frames: concept-match, hero, reversehero, front, rear, left, right, top, bottom, clay, alternate-key clay and wire. Contact sheets are labeled evidence derivatives.

## Facts and limits

Sources are the named Royal Ontario Museum Burgess Shale pages linked in each `references.json`: Emeraldella brocki, Burgessia bella, Tuzoia burgessensis, Sanctacaris uncata. These are child-friendly, evidence-informed scene props, not scientific reconstructions or exact fossil specimens. Emeraldella and Burgessia have no invented eyes. Tuzoia soft anatomy is explicitly a genus-level composite; its head volume and valve depth are authored simplifications. Fine limb podomeres, setae, spine ornament and colors remain artistic. Separate individually closed meshes overlap at joints; this is not a fused print-ready model.

## Technical evidence and parent next steps

All selected artifacts passed source mesh/static GLB checks, source/export count-and-bounds comparison, Khronos (0 errors/0 warnings), two separately executed bound rebuild comparisons, pinned Three.js 0.180.0 Node GLTFLoader geometry parse, and concept-evidence completeness. The source, exported position-stream, triangle, material, primitive and bytes metrics are separated in `technical-summary.json`; no single ambiguous “poly” count is used. Blend 4.3.2 and helper hashes are retained in `environment.json`.

These are maker checks only. A fresh independent Luna XHigh reviewer is to be assigned by the parent. Give that reviewer frozen briefs, source ledgers, exact selected models and full-angle proof; withhold maker expectations/self-verdict until their independent assessment. Independent visual/factual/specification review, target browser/GPU/populated-scene acceptance and formal candidate/release acceptance remain pending. Node parsing and evidence integrity do not establish those gates.

Generate the eventual poster with the merged unified gallery renderer. `preview` and `poster` are deliberately null in integration metadata. Blender proof frames and concept art must not become gallery posters. Parent owns integration and PR creation/update/merge.

## Rebuild and read-only verification

Generators: `generator.py` (R001), `generator-r002.py` (R002), `generator-r003.py` (Tuzoia R003). Configuration is local to each revision. A fresh direct execution is:

```sh
blender -b --factory-startup --disable-autoexec -t 2 --python-exit-code 1 \
  --python production/concept-small-marine-quartet-20261019/generator-r003.py -- \
  --config production/concept-small-marine-quartet-20261019/tuzoia/r003/build-config.json \
  --output-dir /tmp/tuzoia-fresh/output
```

Use a fresh output directory. Queue manifests and append-only request/result/stdout/stderr records preserve actual isolated executions, output hashes and resource settings. Their absolute input paths describe this cloud workspace; adapt a *new* manifest if relocating, leaving historical evidence untouched. Do not run the validator over frozen output folders because it writes reports beside the GLB; validate a fresh copy/rebuild.

For a read-only evidence audit, run from repository root (repeat for the other selected revisions):

```sh
python3 scripts/validate_concept_evidence.py \
  production/concept-small-marine-quartet-20261019/tuzoia/r003/concept-evidence.json \
  --root production/concept-small-marine-quartet-20261019 --require-complete
```

No remaining production blocker. Remaining approval/runtime/publication gates belong to the parent scope above.


## Delivery completion after independent QA

The initial handoff omitted schema candidate records and the revision-local aliases `dimensions_m`, `axis`, `primitives`, `textures`, `bytes`. This gap is now repaired in all four selected directories. The original GLB/Blend, generators, design briefs, references and original raw QA artifacts remain byte-identical to `7c3cc658c1d10fa595e3ef7d27c6f0b17a842dd1`. New read-only measurements and before/after hashes are under `delivery-completion/evidence/`. `delivery-completion/completion-report.json` binds the four complete candidate/metadata records.

Independent limited QA at commit `45b1411119a624461f84452adfcd0cd83838a074` reported visual/factual/specification, format/source correspondence and software WebGL checks passed, without model rework. The exact review text and commit/path/hash provenance are retained under `delivery-completion/`. This is not formal candidate, physical GPU/device/performance or deployed populated-scene acceptance.

Each new `candidate.json` is an initial, current-time registration: `candidate-brief.json` is a separately dated acceptance-contract supplement, and `candidate-references.json` adds explicit rights/scope fields while pinning the unchanged originals. No post-production document is represented as a pre-model freeze. All seven formal stages remain unknown and approval remains pending. Unknown original candidate registration/review times stay unknown.

The executable legacy production contract records its usual 24-orbit/detail acceptance obligations as **unverified**, while explicitly retaining the original bounded study's twelve fixed views and zero turntable frames. No missing frames are fabricated; neither the old limited QA nor original render manifests are relabeled to approve the newly registered contract. Parent owns any subsequent formal profile/approval handling, gallery posters, integration and publication.

The four CLI `validate_candidate.py candidate.json --json` runs return `valid: true`, `approved_for_brief: false`; this validates pending record structure and measurable artifact bindings, not acceptance. Historical `bundle-hashes.json` was retained verbatim as `delivery-completion/original-bundle-hashes-at-7c3cc658.json`; the root checksum inventory now describes the supplemented delivery.
