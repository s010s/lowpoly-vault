# Five accepted creature revisions — 2026-10-30

Integrates the exact accepted gomphotherium, paraceratherium, uintatherium, thylacosmilus and Smilodon KEEP models, paired editable Blender sources and actual browser captures. These are Meshy external bases refined in Blender. No new generation or artwork changes were made.

The catalog retains 752 ordered IDs. Exactly five asset/poster records switch to versioned files; the other 747 raw asset rows and poster records and every previous resource entry remain unchanged. Old models, sources, posters and historical QA remain available.

The three reviewed creature Skill files add reference-led colour gates, structure versus surface-detail choices, UV/tangent/embedded-resource checks, and bounded experiment/return-on-effort records. Their exact bytes are in [the frozen-input receipt](evidence/frozen-input-receipt.json).

## Evidence

- [Frozen inputs, bounds, sources and hashes](input-inventory.json); [integration ledger](integration-ledger.json).
- [Exact capture identities and ten screenshot hashes](evidence/capture-identity.json), [renderer report](evidence/renderer-report.json), [scoped visual review](evidence/visual-review.json).
- [Checks and limitations](evidence/checks.json); [new read-only format validation](evidence/format-validation.json).
- [Network requests, separate payload accounting and five website screenshot hashes](evidence/network-report.json); [website screenshots](evidence/website/).

## Synthetic cold loading

Cloud loopback HTTP with CDP bandwidth/latency emulation, fresh contexts, disabled cache and blocked service workers. The static server sends uncompressed bytes. This is not real-world CDN or physical-device timing. Whole-page loading includes shared JS, manifests and competing poster requests; it is not interchangeable with model-only transfer.

| Model | GLB body bytes | 5 Mbps / 80 ms model transfer | 20 Mbps / 40 ms model transfer |
| --- | ---: | ---: | ---: |
| gomphotherium | 885,980 | 3.51 s | 0.74 s |
| paraceratherium | 4,626,896 | 9.78 s | 2.53 s |
| uintatherium | 4,472,888 | 9.42 s | 2.44 s |
| thylacosmilus | 2,382,948 | 5.26 s | 1.39 s |
| smilodon | 4,932,048 | 10.09 s | 2.61 s |

All five models total **17,300,760 bytes (17.301 decimal MB, 16.499 MiB)** if each is requested. All texture images are embedded: external texture bytes = 0. Optional Blender source downloads are separate and were not requested by normal page loading. Per-run JS and poster transfer bytes and page-ready times are recorded separately. Mbps is megabits per second; these are not MB/s.

## Validation and limits

`npm test`, capture helper tests, exact-five GLB/source/poster hashes, provenance schema/subject binding, 752 delivery checks, the full 752-model build and whitespace checks passed. The new validator run has zero errors and zero warnings for all five. Each model loaded once in both network profiles; mouse orbit, zoom and reset were exercised in the built website.

The required browser installer could not install root dependencies; the preinstalled system Chromium 154.0.8037.57 with SwiftShader was used. Downloading Playwright Chromium 141 was denied by destination policy, with no bypass. Raw transparent captures show ground-fringe stripes also present in the existing published baseline poster and a fresh old-model capture. The actual website composites are readable; renderer code is unchanged.

An extra historical migration test, `site/detail-capture-scope-test.mjs`, already failed before catalog integration because its oncoid-bed GLB pin predates the current baseline; this batch does not change that test or model. See the check record for exact hashes.

Historical per-model QA summaries are retained verbatim. Gomphotherium naturalness/reference-level HOLD and later visual acceptance are distinct. Formal independent QA remains pending. No physical-device, animation, all-viewpoint, real CDN or live deployment acceptance is claimed. Exact-head CI and final release review belong to the release coordinator.
