# Marine quartet release evidence

## Result

PR [#27](https://github.com/s010s/lowpoly-vault/pull/27) merged normally on 2026-10-19 at 22:06:17 UTC. Final PR checks: **32 successful, 2 intentionally skipped, 0 failed**. This archive preserves technical publication evidence for Emeraldella r002, Burgessia r002, Tuzoia r003, and Sanctacaris r002 as limited, evidence-informed stylized scene props.

**Production deployment and live verification: pending.** Final production results will be recorded only after those runs and live checks complete.

Formal candidate approval remains false. Physical-device and target-scene acceptance are unverified. The CI profile named `strict-gpu` uses actual WebGL/GLTFLoader rendering in software Chromium; its name does not establish hardware acceptance. Mobile results use emulated viewports.

## Release identity

- Source head: `66e813c233d2f01f4aefb91f3db8a63913441bf6`
- Previous main: `4774ea94c864dca71dbe252fdd1c03230cc8c610`
- PR test-merge commit: `6ff29de5285ac08bf2b524924d15c9c2625b40a4`
- Released merge: `456a53e3cb257032f210da50e005854b4485abca`
- Released tree: `1686268aeda83b5f94263fecbb45ab6f5a338dde`
- Immutable model source: `1c1b5fd0f466feb95457a8c96ed58ed8f219201f`

The catalog contains 186 assets. A read-only manifest and Git-object comparison confirms all 182 preceding asset entries and 612 files referenced by them are unchanged. See [source-preservation.json](source-preservation.json) for the scope and per-file identities.

## Final PR verification

- [Pages validation, run 39328320495](https://github.com/s010s/lowpoly-vault/actions/runs/39328320495): success. All 12 generated JSON reports are preserved under [pr/pages](pr/pages): parser, publication/build timing, static review, brand, existing seven-model regression, new quartet, full gallery, interaction, and handoff smoke.
- [New quartet browser report](pr/pages/quartets-release-20261019/browser/report.json): 8 passing desktop-English/mobile-Chinese cases, 0 errors. All 16 browser PNGs, including source panels, are preserved beside it.
- [Full release review, run 39328320501](https://github.com/s010s/lowpoly-vault/actions/runs/39328320501): success. The [all-model report](pr/full-review/release-strict-gpu/report.json) records actual previews for all 186 models, no fallback models, and no page/resource errors. Four new-model detail screenshots are preserved beside it.
- [Pinned capture, run 39328320528](https://github.com/s010s/lowpoly-vault/actions/runs/39328320528): success. [Render report](pr/capture/render-report.json) retained.
- [Asset pipeline, run 39328320502](https://github.com/s010s/lowpoly-vault/actions/runs/39328320502): success.
- [Check-run record](pr/check-runs.json) and each workflow-run JSON retain exact source SHA, outcome, public run URL, and artifact identities. Workflow metadata names the source head; artifact reports identify the PR test-merge commit.

The parser reports 189 original/auxiliary parses; that number is not the published model count. The full model browser report establishes the 186-model render count. Static review remains explicitly static-only.

## Capture reproducibility

[Image-byte comparisons](pr/image-byte-comparisons.json) record SHA-256 for 384 gallery files and four PNG/WebP card pairs. Every compared file is byte-identical to its version in the release merge. Those website images are already committed, so this archive keeps the comparison records rather than duplicate copies. No local renderer was run to assemble this archive.

## Production verification

Awaiting final results for [Pages 39332548948](https://github.com/s010s/lowpoly-vault/actions/runs/39332548948), [full review 39332549257](https://github.com/s010s/lowpoly-vault/actions/runs/39332549257), and [asset pipeline 39332548943](https://github.com/s010s/lowpoly-vault/actions/runs/39332548943), followed by checks of the [live gallery](https://s010s.github.io/lowpoly-vault/).

## Reading and integrity

[release-evidence.json](release-evidence.json) is the machine-readable summary. [file-hashes.json](file-hashes.json) indexes all archived files except itself with SHA-256 and byte size; its own integrity is tied to the Git commit containing this archive.

Raw CI reports are retained byte-for-byte. Their original runner paths and localhost URLs are contextual evidence, not currently accessible download links. Reports may refer to older-model screenshots that are deliberately omitted from this focused archive. The original artifact IDs and public workflow URLs remain in the workflow-run records.

This QA-only branch adds evidence under this directory. It does not change application code, model sources, main, the marine source branch, or the separate land/air PR #28.
