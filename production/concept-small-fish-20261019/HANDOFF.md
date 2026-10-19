# Four small fish — independent QA and scene closure

Branch: `candidate/small-fish-birds-20261019`. Source baseline includes
`bac6621fc39144b3759c53b1b27231ac1b6e21c6`. Cloud-only Blender 4.3.2;
maker requested GPT-6.1 Sol Medium. Git author: Leon Made This
<8357465+s010s@users.noreply.github.com>.

| Inventory ID | Entry (1-based) | Triangles | GLB bytes | Materials | Primitives |
|---|---:|---:|---:|---:|---:|
| metaspriggina | 543 | 2,296 | 143,812 | 6 | 30 |
| falcatus | 569 | 1,628 | 108,568 | 5 | 23 |
| pteraspis | 548 | 1,336 | 91,952 | 6 | 16 |
| dorypterus | 585 | 1,532 | 107,160 | 6 | 22 |

Selection is from `research/prehistoric-1000-v1/inventory.json`.
`selection-evidence.json` and `evidence/remote-heads.txt` record 145 inspected
candidate/handoff/production refs, no matching ID paths, no published/current
production exact IDs, and open PR20/PR21 scope. The unrelated invertebrate
Cambroraster falcatus is not the Falcatus taxon. The original inventory and all
published files are unchanged. These are four structural designs, not palette or
scale variants. No invertebrate, coral, rock, plant or large dinosaur is included.

`concept-original.png` is genuine retained ImageGen output; exact prompt and
available tool output identity are preserved. It was generated and inspected
before modeling, with each brief frozen before geometry. Concept contradictions
and unseen surfaces are explicitly resolved in each `brief.md`. All are labeled
original inspired scene props; none claims a scientifically exact reconstruction.
The original R1 preference is respected; no historical R2 is promoted or replaced.

Current closure: [acceptance notes](closure-20261019/ACCEPTANCE-NOTES.md), [independent-QA provenance](closure-20261019/independent-qa-provenance.json), and [8/32-copy software-WebGL report](closure-20261019/software-webgl/report.json). Independent QA at `f4406976` passes all four bounded visual/technical/brief checks with no model repair. Model binaries and frozen build inputs remain unchanged. Dorypterus current delivered length is **0.0996 m (99.6 mm)**; Pteraspis remains an inspired stylized prop rather than an exact scientific reconstruction.

For each `<id>/r001/`, review:

- `brief.json`, `brief.md`, `references.json`, `build-config.json`.
- `output/<id>.blend` and `output/<id>.glb`; the shared `generator.py` retains
  editable profile-based, closed volumetric construction in semantic parts.
- `proof/`: 11 original 512px PNGs, clean-imported from the exact delivered GLB,
  with hash-bound render/camera/lighting manifests. Includes both three-quarter
  views, front/rear/both sides/top/bottom, clay, alternate-key clay and triangulated
  wire. Every original frame was individually opened for maker self-check.
- `concept-angle-proof/`: clean-imported GLB at approximate concept azimuth 70°,
  elevation 12°. The illustration has no calibrated camera, so exact camera
  equality is not claimed. The same palette/primary landmarks are retained with
  simpler, more angular fins and tails. `candidate-overview.png` is navigation
  only; use the original proofs for review.
- Actual raw `qa.json`, official `gltf-validator.report.json`,
  `source-export.report.json`, both `rebuild-*.report.json`, and
  `threejs-parse.report.json`. `handoff.json` pins exact artifact/report hashes.

All four source/static checks have zero errors; the mounting-height advisory is
intentional for the declared swimming-midline origin. Official Khronos Validator
2.0.0-dev.3.10: zero errors and warnings for each exact GLB. Source/export evaluated
triangles and axis-converted bounds match. Two separately executed bounded-queue
rebuilds per asset match both normalized semantics and actual GLB bytes. Queue
request/result identities and raw logs remain in `rebuild-runs/`. Three.js
0.180.0 Node GLTFLoader parsing, triangles and dimensions match. That earlier Node result establishes parsing only. The new closure separately renders all four models in Chromium 154 / ANGLE SwiftShader software WebGL2, with 8/32 copies per species and balanced mixed groups in hero/top views: all 20 functional scenarios pass. These synthetic scenes retain actual metre scale and are not hardware-GPU or deployed museum validation.

The original `concept-integrity.report.json` files remain historical. Current
`closure-20261019/*-concept-integrity-current.report.json` files are
**valid=true, evidence_complete=false**, with one remaining blocker: exact first
pixel-inspection time is unknown. A real embedded C2PA created-action timestamp
was recovered from the original PNG: **2026-10-19T15:57:08.648462002Z**. This is
an unverified provider declaration, not a cryptographically validated trusted
clock. No mtime or later viewing time is substituted for the missing first-view
time. `--require-complete` still fails; the Skill permits honestly unrecorded
study timings, so this does not invalidate the independent bounded visual pass.
It does prevent claiming strict chronology completeness. Formal production
acceptance remains separate and is not granted by this update.

Metaspriggina's first shallow-gill attempt is retained under
`attempt-01-gill-cues-too-shallow/`, including original GLB/Blend/proofs/generator.
Only the external landmark visibility was repaired. Two concept-angle wrapper
preflights failed while resolving helper paths; their logs are preserved, and the
separate final `concept-angle-proof/` runs succeeded. No failed run is counted as
passing evidence.

Current decisions and limits:

- Fresh independent QA is complete at `f4406976378c132e5ec50c51e839a717ed4418fa`:
  all four bounded stylized candidates pass visual, technical, brief and honest
  claim-scope review; no geometry repair is recommended. Its GLB/Blend bindings
  still match all eight delivered model files.
- The exact first concept-inspection timestamp remains unknown. Current strict
  concept completeness checks remain intentionally incomplete, as explained above.
- Pteraspis exact armor layout/proportions/tail ratios are unknown and unclaimed;
  this is nonblocking for the independently accepted stylized inspired scope.
- Software WebGL scenes are checked for each species and mixed groups at 8/32
  copies in hero/top views, with exact counts, GL errors, foreground pixels,
  renderer identity, timing samples and inspected screenshots. All 20 pass.
  Physical GPU and the actual deployed museum scene remain unverified. Timings
  are run-specific software render+finish wall times, not a hardware FPS promise.
- Main bac6621's three CI runs are now all completed/success, confirmed read-only
  in `closure-20261019/main-ci-success.json`. No workflow was rerun.
- No main merge, production manifest/catalog/inventory update, PR20 modification,
  deployment, force push, remote deletion, permission change, user-computer work
  or Drive upload. Formal production approval and release remain with parent.

Reproduce from repository root using a **new** output directory:

```sh
blender --background --factory-startup --disable-autoexec --threads 2 \
  --python-exit-code 1 --python production/concept-small-fish-20261019/generator.py -- \
  --config production/concept-small-fish-20261019/falcatus/r001/build-config.json \
  --output-dir /tmp/new-falcatus-build
node production/concept-small-fish-20261019/parse-exact-models.mjs
python scripts/validate_concept_evidence.py \
  falcatus/r001/concept-evidence.json \
  --root production/concept-small-fish-20261019
```

The renderer and source/rebuild checker invocations are retained in raw logs and
queue request files. Reuse the pinned scripts, generator/config and package lock;
choose new evidence paths because the checkers preserve existing outputs.

Original art, renders and prose: CC BY 4.0, Leon Made This / s010s. Executable code:
MIT. No third-party geometry, textures or reference images are incorporated.
