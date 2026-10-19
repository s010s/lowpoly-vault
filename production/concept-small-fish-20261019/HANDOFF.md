# Four small fish — independent QA handoff

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
0.180.0 Node GLTFLoader parsing, triangles and dimensions match. This establishes
parsing only, not browser GPU rendering or populated-scene performance.

`concept-integrity.report.json` is **valid=true, evidence_complete=false** for
each asset. The exact concept-generation and first-inspection timestamps were not
separately recorded and stay null; they are not reconstructed from file mtimes.
The genuine image, prompt and available tool identity are present. `--require-complete`
is expected to fail for those chronology gaps. These supplemental study records
are not formal production candidate approval records.

Metaspriggina's first shallow-gill attempt is retained under
`attempt-01-gill-cues-too-shallow/`, including original GLB/Blend/proofs/generator.
Only the external landmark visibility was repaired. Two concept-angle wrapper
preflights failed while resolving helper paths; their logs are preserved, and the
separate final `concept-angle-proof/` runs succeeded. No failed run is counted as
passing evidence.

Remaining gates and limits:

- Parent assigns fresh independent artistic/factual/specification QA. Begin with
  the frozen brief, references and exact GLB/proofs; maker self-check notes are
  separate and must not supply the independent verdict. No acceptance is claimed.
- Pteraspis full primary anatomy access remains limited. Original UCL page fetch:
  web 502; shell `curl: (56) CONNECT tunnel failed, response 403`. Later opened
  Kermack 1943 abstract supports the hypocercal tail; that consulted-only source
  is in `references-supplement.json`, without modifying frozen source bindings.
  Precise plate patterns, proportions and oral anatomy remain unverified.
- Browser GPU, hardware GPU and populated-scene tests are **not run**. Repeat-copy
  performance is not inferred from file size, materials or triangle count.
- Main CI runs for bac6621 were queued on observation during the reported
  [GitHub Actions/Pages incident](https://www.githubstatus.com/incidents/8tzbpcnl75jp).
  No workflow was rerun. CI must be confirmed by the parent before any later release.
- No main merge, manifest/catalog/inventory update, PR20 modification, deployment,
  force push, remote deletion, permission change, user-computer work or Drive upload.

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
