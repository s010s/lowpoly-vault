# Standardized asset production and acceptance

This contract applies to new candidates and revisions. It does not retroactively turn historical first-pack records into current approval. Use the existing build/export helpers and [QA entry points](qa-design.md); add the candidate record and independent review described here.

## Lifecycle and identities

`planned → brief_ready → building → candidate → reviewing → repair → reviewing → accepted_for_brief`

Publication is a separate authorized transition. `blocked`, `cancelled` and `superseded` are explicit states, not successful completions. The 1,000-entry research inventory is planning data; it must not populate approved counts, downloads or release manifests.

Use a stable asset ID plus immutable revision and run/attempt ID. Store every attempt in its own directory. Never let two jobs write the same candidate, preview or QA file. A successful job produces bytes; it does not set visual/factual acceptance. Preserve failed logs and completed evidence so work can resume without fabricating success.

The frozen bundle contains:

- `brief.json`: subject/variant, claim scope, intended use, scale/uncertainty, view plan, runtime profile, geometry and texture limits, required stages and feature-level criteria.
- `references.json`: claim/source mappings, source edition/date/location, provenance/license and consulted-versus-incorporated use.
- Editable source, deterministic generator/config, actual standalone GLB and any source maps/bakes needed for editing.
- `candidate.json`: exact artifact/brief/reference hashes, maker and independent reviewer identities, stage evidence, criteria, blockers and acceptance decision.
- Hashed technical reports and exact-GLB view manifest with full-resolution images. Paths must stay inside the reviewed bundle/root and be portable when the bundle is copied.

Start from the pending templates under `schemas/templates/`. Unknown checks stay unknown. Use:

```sh
python scripts/validate_candidate.py path/to/candidate.json --root path/to/bundle --json
python scripts/validate_candidate.py path/to/candidate.json --root path/to/bundle --require-approved --json
```

The first checks record integrity; an unapproved candidate can be a valid record. The second fails unless the required evidence and acceptance obligations are satisfied. This checker enforces structure and provenance, not truthfulness of a human assertion. Exact CLI/schema fields are documented with the templates.

## 1. Brief and evidence before geometry

Freeze subject, variant, jurisdiction/era or taxon/life stage, approximate versus measured scale, pose, identifying structures, style, intended viewing distances and whether close inspection is supported. Define feature-specific obligations and legitimate artistic choices. Decide the required runtime/device/scene scope rather than inventing it after seeing results.

Use [asset-factual-review](../../asset-factual-review/SKILL.md) for anatomy and other factual obligations. Link each critical obligation to primary evidence with exact section/figure/specimen and uncertainty. A reference image is not a license to copy it; a style target is not scientific authority. If evidence cannot support the requested claim, narrow the claim or leave the gate unknown.

Set independent geometry, material/primitive, image dimension/encoded byte and decoded-memory budgets. Record instances and actual runtime submissions separately. Historic first-pack bands and helper defaults are not universal limits. A named increase such as resolving shoulder/hip flow is meaningful; filling a higher triangle ceiling is not.

## 2. Build form, then portable surfaces

Build deliberate primary and secondary structure before polish. Inspect clay, silhouette or internal-relief views and relevant close-ups. Resolve attachment, weight, proportion and function-bearing features before using texture detail to increase apparent finish.

Choose palette-only, color-only texture or [textured-PBR](production-contract.md#textured-pbr-profile) explicitly. Use the [controlled optimization checklist](controlled-optimization.md) when comparing their quality and delivery cost; a cheaper tier need not have equivalent close-detail quality. Texture-rich low-poly is valid. Preserve editable source and bake original maps for portable export. A surface A/B holds geometry, normals, camera, lighting and exposure fixed; a changed mesh is a separately labeled experiment.

After exporting, run source and GLB checks, official format validation, clean reimport and semantic rebuild. Bind each result to the current GLB and the configured budgets. Unsupported content is blocked/unknown. A warning must have an asset-specific review reason; no blanket suppression.

## 3. Quick full-angle evidence first

Use the headless renderer and queue in [parallel-queue.md](parallel-queue.md). One Blender installation can run multiple isolated processes. The GUI is not the scheduling unit.

Freeze a view plan. A 24–36-frame full-azimuth turntable is a starting profile, configurable after a visual/cost benchmark. Add front/rear/both sides/top/bottom, clay and alternate key, actual triangulated wireframe and subject-specific details. Request extra angles around uncertain joints, undersides, thin surfaces and cavities. Full angle coverage at low samples precedes final high-resolution renders.

Every image must identify source GLB hash and camera/render config. Keep frame order, azimuth/elevation, pose, resolution, background, color management, bytes and SHA-256 in a manifest. Fit the full asset using stable framing; do not allow each frame to zoom independently. Generate a navigation montage while retaining originals. A reviewer must open the actual required pixels; a montage or filename alone does not establish inspection.

The turntable export contract also supports list-card hover image scrubbing. Website posters and scrub frames must use the actual detail viewer's camera, tone mapping, background and lighting preset when appearance continuity is required; neutral Blender QA renders do not automatically match WebGL. Keep a separately identified website-render profile and verify its pixels against the actual detail view. Its consumer must lazily fetch only the active asset, bound decoded memory, support keyboard/touch and reduced motion, and retain a static fallback. The detail view automatically loads the real GLB; do not add a separate 3D activation button or replace detail 3D with the frame sequence. Images do not establish interactive WebGL correctness. Compare individual WebP/AVIF frames and sheets using encoded bytes and decoded memory before choosing; no format is automatically best. Changing the site's default preview or published files is separate work with separate release tests.

## 4. Independent review and defect loop

Open a fresh review task with the brief, source ledger and frozen evidence, without the maker's self-score or persuasive explanation. Initial findings come before repair history. Separate:

- Technical file/geometry checks
- Visual craft and surface quality
- Factual feature obligations and uncertainty
- Brief/specification compliance
- Runtime parse, actual GPU render and populated-scene performance

Use `pass`, `fail`, `unknown`, `not_applicable` and `stale`. A study can legitimately lack target GPU evidence, but cannot become a production approval through that omission. Runtime parse success is not GPU success; software/fallback and actual graphics paths are distinct.

Each defect records severity, view/location, observation, obligation/source, required repair/evidence and retest. Do not average scores to erase a failed criterion. Repair the top blockers, export a new revision, rerun affected checks and regenerate images. Inspect regressions in previously passing views. Reconcile conflicting reviews with evidence or escalate the relevant artistic choice; do not select the most favorable score.

If a change affects only packaging, state and verify that the model and images are unchanged. Geometry/material/texture changes invalidate affected visual/runtime evidence. Brief or source changes invalidate affected factual decisions. Hash-based integrity cannot determine impact by itself; the reviewer must state the scope.

## 5. Bounded parallel work and resumption

Keep a heavy build/bake/render worker pool separate from independent image QA tasks. Queue asset-ready evidence while another asset builds. Use conservative measured concurrency, explicit Blender threads, memory/timeout limits and cleanup. Inspect effective affinity/quota and other active jobs; advertised host cores are not available capacity.

Cancellation stops new work and cleans up owned child processes. Never kill another task's Blender process. Retry only recoverable attempts under the authorized scope, into a new attempt directory. Resume only after verifying current input/config/tool identity and output hashes. A stale report or existing filename is not a completed job. Start with a measured small pilot before scaling a batch; do not launch 1,000 processes from the planning list.

Do not start expensive HD refinement until structural/material direction passes quick review. Full-angle quick review is not final image-quality approval. Record actual wall time, dimensions/samples, concurrency and capacity limits; fixture tests do not establish production throughput.

## 6. Acceptance and publication

`accepted_for_brief` requires every mandatory criterion to pass with current evidence, independent visual/factual/specification review, reviewed warnings and no unresolved required unknown or blocker. This is acceptance within the documented claim scope, not a scientific guarantee. User style approval is separately recorded when required by the brief.

Formal release generation additionally checks the candidate acceptance record. A publication request does not rewrite QA, and accepted candidates do not automatically authorize publication or bulk replacement. The existing exact-ten initial release uses `assets/initial-publication.json` and `site/initial-release.mjs`: it is explicitly work in progress with sealed IDs/hashes. Preserve that narrow exception; do not use it to publish new candidates or report them as fully QA-approved.

The site's current deployment allowlist is intentionally fixed to that initial ten. Scaling publication requires a separately reviewed release pack and integration change; adding accepted candidates to a folder is insufficient. Keep source licensing, attribution and uncertainty with delivered artifacts.
