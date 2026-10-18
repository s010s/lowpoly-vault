# CI timing investigation and bounded optimization

Baseline: 79 published assets at eb9153eab06f7e95235eac30611b731c8178ffb7. The baseline GitHub Pages build job 117794889580 (run 39167985593) took 305 seconds: publication gate plus all rejection regressions 198 s; other static tests 6 s; build 33 s; Chromium installation 20 s; parsing/static-download/interaction/handoff probes 23 s; remaining time checkout/upload/setup. github-baseline.json records exact timestamps. The original 102-second measurement was for the much smaller initial collection; it is not a 79-asset measurement.

## Actual local breakdown

`profile.py` runs the same mandatory commands in sequence and instruments Python process counts. The baseline was an isolated clean worktree at the above SHA; the optimized worktree used the same 79-model manifest and implementation fingerprints in optimized-inputs.json. Wall-clock results depend on host load; exact process counts and byte comparisons complement timings. Each command's actual output and counter log is retained.

| Phase | Before seconds / Python calls | After seconds / Python calls |
|---|---:|---:|
| All publication rejection suites | 238.696 / 1,166 | 123.139 / 668 |
| Round03 suite alone | 100.292 / 574 | 29.394 / 208 |
| Successful full publication check | 18.108 / 135 | 21.095 / 135 |

The optimized test set includes two additional old-generation corruption/missing-file refusals (303 total release checks instead of 301). Successful validation still invokes every original checker and reads every pinned input; it is not a cache hit. All 344 original assertion expressions across the five modified gates are exactly unchanged, verified by parsing both revisions (assertions-preserved.json).

A separate read-only profile uses the real delivery module and extracts its existing ZIP packer rather than reimplementing it. For 79 assets / 237 payload files: all payload hashes/stat/enrichment 0.297 s; payload copying 0.290 s; all ZIP packaging 2.503 s. All 79 generated ZIPs match baseline bytes. These are measured subphases, not an extrapolated 1,000-asset benchmark. A full optimized build through the actual npm entry point took 19.292 s preflight gate + 2.253 s Vite + 3.421 s copy/package/routes + 18.752 s final audit on this host. This makes repeated Python validation the first target, rather than adding ZIP-cache trust machinery for a currently small cost.

## Minimal changes and invariants

Five historical addition gates previously validated the entire predecessor release before rejecting malformed new additions. Their dependency/byte/policy/candidate assertions are preserved, with predecessor validation moved to after all new additions pass. Every successful result still performs the complete predecessor validation, count/duplicate checks and identical manifest composition. A failure stops the publication; it cannot emit a partial accepted collection. The new tests mutate and remove an older published GLB after an earlier successful collection call, proving unchanged-generation inputs are freshly checked and not trusted from memory.

Pages and parallel review jobs previously ran a standalone publication check and then npm build, which repeats that same check before Vite and again inside the final output audit. The redundant workflow call is removed. **The build's mandatory preflight gate and post-build full inventory/ZIP audit remain.** The pipeline job has no build and retains its standalone publication check. A failing preflight stops before compilation; a failing final audit makes the build fail. No artifact can advance to deployment through these ordinary success dependencies when a gate fails.

A small CI-only command runner preserves the original nine-suite and four-build-command order and exit statuses while emitting per-phase JSON timings. Tests prove all mandatory suites run, the first nonzero exit is preserved, subsequent commands do not run, a missing suite fails, preflight failure prevents compilation, and final-audit failure prevents a successful build. Future release suites must be appended to this same explicit list. Pages/full-review artifacts retain qa/ci-timings/. All manual full-review entry points remain unchanged.

No persistent cache, cache receipt, validator skip flag, threshold change, permission/protection change, asset change or 16–18 publication is introduced. Unchanged assets remain protected by full physical-byte checks against the checksum-pinned release chain on every successful build. This removes the measured repeated-rejection work; it does not claim constant-time validation or a tested 1,000-asset result. Required successful hashing/auditing remains linear in data size, and adding more complete historical suites still has a cost. Further incremental/cached validation should be based on a measured, version-bound complete dependency closure, not an unversioned cache.

## Proof and reproduction

- before-timings.json / after-timings.json: all command results and Python invocation counts; associated actual logs are retained.
- delivery-before.json: real hash/copy/ZIP measurements and byte matches.
- actual-timed-build.json: real npm build phases, all successful.
- delivery-equality.json: all 988 baseline and optimized deployment files have exactly the same path and SHA-256; no added, removed or modified public file.
- assertions-preserved.json: all original gate assertions unchanged; two new negative regressions added.

From a clean checkout: `python qa/ci-optimization-20261018/profile.py <checkout-root> <absolute-output-directory>` runs the full measured sequence without approving/publishing assets. Build variables are fixed to the real Pages base/origin. `node qa/ci-optimization-20261018/profile-delivery.mjs <checkout-root> <report.json>` requires an already-built dist and compares all newly generated ZIPs with that real delivery. The scratch outputs are removed after verification; source inputs are read-only. Final authoritative optimized CI and deployed-browser timings belong to the exact PR/main Actions runs linked in the final report.
