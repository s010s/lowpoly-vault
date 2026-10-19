# Candidate record and software scene closure

This supplements the frozen r001 evidence rather than rewriting its history.
The `.blend`, GLB, generator, build configurations, original briefs, source
ledgers and original renders remain unchanged. Parent-requested documentation
clarifications do not invalidate their geometry/material visual verdicts.

Independent QA at `f4406976378c132e5ec50c51e839a717ed4418fa` passes all four
bounded stylized candidates for visual craft, brief compliance, file validity,
scale disclosure and source/export matching. No geometry repair is recommended.
`independent-qa-provenance.json` pins the original report and decisions and
rechecks all eight GLB/Blend hashes. It does not turn the maker into the
independent reviewer or expand the original decision to formal production.

## Real chronology evidence and its acceptance effect

`extract-concept-time.py` parses the original PNG's embedded
`c2pa.actions.v2` CBOR box. Its `c2pa.created` action declares
`2026-10-19T15:57:08.648462002Z`, with software-agent strings `ChatGPT` and
`gpt-image`. The source image hash, byte offset, CBOR hash and decoded actions
are retained in `concept-time-evidence.json`. This is genuine metadata already
inside the original delivered image, not a date inferred from filesystem mtimes.
It is a provider-embedded assertion; C2PA signature or trusted timestamp
validation has **not** been performed. It does not prove the tool's return time.

The exact **first pixel-inspection time remains unknown**. The earlier task
history and pre-model generation record attest that the concept was inspected
before the frozen brief and modeling, but neither provides a separately recorded
exact viewing time. A git commit date, image mtime, current reinspection time or
subsequent render must not fill that field. No such timestamp is invented here.
`concept-generation-current.json` and the four `*-concept-evidence-current.json`
sidecars add only the supported creation-time declaration and retain
`concept_inspected_at: null`. The original sidecars and reports are preserved.

The distinction follows the current repository Skill and checker:

- `skills/concept-guided-lowpoly/SKILL.md`, “Prove the exported result,” says
  **“Record actual stage timings, or explicitly say unrecorded/not run.”**
  Honest unknown timing is compatible with a bounded study and does not overturn
  the independent artistic/technical pass. The missing exact viewing timestamp
  is not evidence of an uninspected concept or a geometry defect.
- `references/workflow.md` and `validate_concept_evidence.py` define an additional
  **complete chronology record**. Current runs return `valid: true` and
  `evidence_complete: false`, with exactly one blocker: unknown
  `concept_inspected_at`. `--require-complete` therefore still fails. This strict
  evidence-completeness gate is genuinely open; its requirement is not waived or
  silently edited. The generation time is no longer missing.
- The same Skill says the supplemental checker cannot grant candidate approval
  or publication. Its allowance for unrecorded timings means the missing exact
  clock time alone is **not an explicit Skill instruction to reject the models**.
  It must not be promoted into a new artistic failure or an automatic formal
  rejection beyond the strict helper's actual completeness check. Formal
  `accepted_for_brief`/release readiness is still not asserted: this batch has
  provisional-study records and a scoped independent pass, rather than a formal
  production acceptance record. Physical GPU and actual deployed museum scene
  validation remain unperformed and must be considered only within the relevant
  frozen runtime profile. No acceptance criteria or checker rules are changed.

## Delivered size and factual scope

Dorypterus's delivered overall GLB length is **0.09960000217 m**, displayed as
**0.0996 m / 99.6 mm**. Current metadata and
`dorypterus-delivered-specification.json` use that measured size for downstream
placement and descriptions. The historical approximate 0.12 m brief target and
the generator's `length_m=0.12` scale input remain frozen for reproducibility;
the authored outline spans 0.83 of that scalar. Changing the generator parameter
to 0.0996 would change geometry and would not merely correct its description.
Independent QA explicitly accepted the size difference as nonblocking.

Pteraspis is an **original stylized Pteraspis-inspired scene prop**, not an exact
species/specimen reconstruction. Detailed shield layout, proportions and tail
ratios remain unverified and unclaimed. Independent QA passes the truthful
stylized scope; unknown exact scientific reconstruction anatomy is not a failed
obligation of that narrower brief. No anatomy/geometry change is made.

## Runnable population check

From repository root:

```sh
node production/concept-small-fish-20261019/closure-20261019/run-scenes.mjs /tmp/fish-scene-check-new
python production/concept-small-fish-20261019/closure-20261019/extract-concept-time.py
```

The first command starts a local read-only server, uses pinned Three.js
0.180.0/GLTFLoader and `/usr/bin/chromium`, and explicitly requests ANGLE
SwiftShader. It tests 8 and 32 copies of each asset and balanced mixed groups
(8 total = 2 per species; 32 total = 8 per species), in hero and top views.
Metre scale is retained; only translation and yaw change. It measures actual
draw calls/triangles, GL errors, foreground pixels, renderer identity and 30
warm render+`gl.finish()` wall-time samples per scenario, with hashed screenshots.
The script asserts 20 successful scenarios and software-renderer identification.

Actual run: **20/20 pass**, no page/console/request or WebGL errors. Chromium
154.0.8037.57 reports ANGLE Vulkan / SwiftShader Device (Subzero). All 20 original
1200×800 screenshots were individually inspected and their hashes verified in
`software-webgl/visual-inspection.json`.

| Composition | 8-copy calls / triangles | 32-copy calls / triangles |
|---|---:|---:|
| Metaspriggina | 240 / 18,368 | 960 / 73,472 |
| Falcatus | 184 / 13,024 | 736 / 52,096 |
| Pteraspis | 128 / 10,688 | 512 / 42,752 |
| Dorypterus | 176 / 12,256 | 704 / 49,024 |
| Balanced mixed group | 182 / 13,584 | 728 / 54,336 |

Hero/top submitted counts agree. Mixed-group hero render+finish medians were
2.5 ms (8 copies) and 10.9 ms (32), with p95 12.0 / 27.9 ms in this run.
The raw report retains all per-view measurements; these are observations with
no hardware or target-scene performance acceptance threshold.

This is a **synthetic software-WebGL functional scene test**, not a physical GPU
benchmark or the deployed museum scene. Timing samples are machine/run-specific
software rendering wall times, not a promised FPS or a target-device budget pass.
No FPS threshold was frozen. Hardware GPU and production integration remain
unverified; render-call and triangle measurements are reported without turning
their size into an artistic verdict.

The parent reported main bac6621 CI now successful; read-only API confirmation
is retained in `main-ci-success.json`. No workflow was rerun. No main merge,
production manifest change or deployment is performed by this closure.
