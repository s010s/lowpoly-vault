# Independent QA: lowpoly-vault batch 69

**Reviewer:** GPT-6 Luna xhigh  
**Review date:** 2026-10-20  
**Pinned target:** `candidate/small-life-batch69-concept-20261020` at `0a58b9eab9bd4b777a1cf73262cfee00c4ba009d`  
**Worktree:** `/workspace/shared/lowpoly-batch69-20261020` (clean before and after read-only checks)

## Disposition

**Bounded recommendation: ACCEPT all four exact r001 candidates for the reviewed local candidate scope.** This is an independent QA recommendation only, not formal, user, publication, release, merge, or hardware approval. The commit remained unchanged and clean. GPU and composed-scene stages were not run.

| Candidate / exact final GLB SHA-256 | Technical | Visual | Factual | Specification | Runtime parse | GPU | Scene | Bounded recommendation |
|---|---|---|---|---|---|---|---|---|
| wiwaxia / `d1c7e67515487fc583fd0eb903a961aec5ba855a2e95183696c031531f53c266` | PASS | PASS, bounded | PASS, uncertainty retained | PASS | PASS | NOT RUN | NOT RUN | ACCEPT |
| hanging-valley / `adb2ca389d1260ac1d2cd4f0ecd6153ed344484c95fd0667928339fa198be2b9` | PASS | PASS, bounded | PASS, generic form | PASS | PASS | NOT RUN | NOT RUN | ACCEPT |
| mudpot / `7818b6e324a8da1f93db36fcb09c989bf0b98c3d4fa02873ae8750daf41f4bf1` | PASS | PASS, bounded | PASS, generic form | PASS | PASS | NOT RUN | NOT RUN | ACCEPT |
| dike-wall / `f0c69989e84ca70dd90a039c78199e65b5448f5d85d52fa3b4b1beb856f617d7` | PASS | PASS, bounded | PASS, generic form | PASS | PASS | NOT RUN | NOT RUN | ACCEPT |

## Review performed

- Confirmed the exact source branch, pinned commit and clean status. Compared the source inventory blob at the pinned base and candidate commit: both are byte-identical, SHA-256 `b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c`; it contains 1,000 records, and each selected ID occurs once. The complete original source-inventory records for these four IDs are byte-for-byte equal to their selected-copy records. The batch claim/dedup evidence names exactly the four candidates under review.
- Read the handoff, verification, original premodel freezes, complete original briefs/configs/reference ledgers, derived delivery briefs, candidate records, project/runtime records and the production addendum. Verified original frozen-file hashes and candidate-to-handoff bindings. Reference ledgers have rights notes and explicit non-incorporation; each hash-listed consult-only image exists outside the repository and matches its ledger. Hash-scanned all 28,505 tracked worktree paths against the 11 consulted-image digests; none is present in the repository.
- Inspected all four original generated concepts and contact sheets. The available ImageGen observer records retain actual call/result/inspection times, prompts, image pixels and output receipts. Provider-internal generation timestamps/request IDs and exact authoring start times were not returned and remain **unknown**; filesystem timestamps were not substituted.
- Read primary source text and inspected actual full-resolution primary/official reference pixels. Consult-only pixel hashes and source identities are in `independent-static-checks.json`. For Wiwaxia, I viewed the actual Nature Figs. 2, 5 and 6 and ROM specimens 32570, 56950, 57707 and 57726; the local images hash-match the frozen reference ledger and remain outside the repository. The ROM's old approximately-50-row prose was not used as accepted evidence.
- Personally inspected every exact final individual 512×512 image (all 32), all four final lossless contact sheets, and the separately labelled exact-final Wiwaxia ventral diagnostic. Frame SHA-256, manifest and final-subject bindings and sheet dimensions/hashes were independently checked. No images were copied into this QA folder.
- Independently reopened all four saved Blender projects read-only in separate Blender 4.3.2 processes, each under its own blocking `/tmp/lowpoly-production-blender.lock` and `--threads 2`; source hashes remained identical. Reopened mesh-object part counts, authored/evaluated vertex/polygon counts and measured bounds match the reported source data. All four have zero linked libraries and zero external image dependencies.
- Independently parsed each exact GLB and checked limits of 14,000 triangles, 1,000,000 bytes, 6 materials and 30 primitives; all have zero textures. Ran Khronos glTF Validator 2.0.0-dev.3.10 and Node Three.js 0.180.0 `GLTFLoader.parseAsync` against the exact final files. Every Khronos run returned zero errors, zero warnings, zero infos and zero hints; all four Three.js CPU parses succeeded with matching triangle counts and bounds. These do not evidence GPU rendering or scene performance.
- Independently matched two distinct existing queued producer rebuilds per candidate to their separate request/result records, PIDs, times, exact inputs, output bytes and semantic reports. Each produced the exact final GLB hash, semantic match and byte-identical output; no redundant full producer builds were run.
- Kept historical attempts out of acceptance proof. Wiwaxia's original tooth-row occlusion and body/foot contact-gap attempts remain; the final ventral diagnostic shows a continuous naked foot and discernible two-row mouth apparatus, and the final front/side/contact views no longer show the earlier gaps. Hanging Valley's embedded-fall attempt remains. Its earlier stale comparison report (`retained-stale-comparisons/141445-repro-final-2.report.json`) remains a failure: it compared a different earlier rebuilt hash `f32f7d5bca83ba2e5a1bea9e5860765e4cef25acfc4339139786b63d5aa6fda7`; it is not used as final evidence. Dike Wall's prior overly planar/repetitive-wall attempt remains. These retained artifacts are summarized in the static JSON report.

## Technical and specification evidence

| Asset | Triangles | GLB bytes | Materials | Primitives | Textures | Source authored/evaluated vertices | Exported POSITION vertices | Measured Blender XYZ bounds (m) | Nominal Blender XYZ (m) |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| wiwaxia | 11,292 | 605,696 | 6 | 12 | 0 | 7,000 / 7,000 | 21,948 | 0.03138 × 0.05140 × 0.03384 | 0.038 × 0.050 × 0.036 |
| hanging-valley | 13,310 | 840,860 | 4 | 6 | 0 | 6,663 / 6,663 | 31,487 | 80.019 × 70.022 × 24.430 | 80 × 70 × 24 |
| mudpot | 6,494 | 497,148 | 3 | 3 | 0 | 3,249 / 3,249 | 18,965 | 5.106 × 4.045 × 0.609 | 5 × 4 × 0.7 |
| dike-wall | 2,084 | 88,896 | 4 | 7 | 0 | 1,056 / 1,056 | 3,090 | 16 × 24 × 8.608 | 16 × 24 × 9 |

All remain within stated geometry/file budgets. Nominal geology dimensions are explanatory/artistic; none of these bounds asserts a measured named site. The frozen design brief is intact, the candidate record is pending rather than approved, and no approval authority is inferred.

Final render manifests bind the exact current GLB, derived delivery brief and source-reference ledger hashes; these identities match every delivered frame and the pinned final artifacts. The renderer computes the per-render subject hashes before its frame loop. A chronology nuance is retained: standalone `preproof-binding.json` checks for Wiwaxia, Hanging Valley and Mudpot have check times later than their final render-manifest timestamps. I do **not** rely on those later check timestamps to claim a pre-render gate; the direct render-time subject capture and exact matching frame manifest are the evidence for final pixel binding. Dike Wall's checked binding precedes its final rerender.

## Per-asset observations

### Wiwaxia

The evidence-informed target is the **whole adult *Wiwaxia corrugata***, not a loose armour shell or isolated scleritome. The inspected final views show an oval soft body with differentiated overlapping sclerite zones and unequal, flattened blade-like dorsal/lateral spine ranks. The separate ventral diagnostic shows a broad continuous naked foot and an anterior mouth-support with two visible tooth rows; the teeth are very small at 512 px but no longer occluded. Canonical top/front and the ventral diagnostic complement each other; I do not claim the tooth form or count is equally legible in every hero angle. Body ends remain deliberately faceted and scale/posture/color are reconstruction choices, not a specimen replica.

The row accounting is transparently reconciled rather than silently treating two conventions as identical: Smith (2014) supports eight posterior/trunk rows plus anterior organization; Zhang, Smith & Shu (2015) discuss *Wiwaxia papilio* (not “papillosa”) but also interpret the anterior organization in adult *W. corrugata* ROM 57707 as a ninth serial organization. The maker's freeze specifies eight posterior/trunk rows plus the paired anterior fan and separately states that this is nine under the 2015 convention. It does not transfer juvenile *W. papilio* morphology into adult *W. corrugata*. The 2023 correction adds omitted data and does not retract that morphology. Affinity, soft tissue/color, posture and fine ridging remain uncertain; no internal gut, scan, copied mesh, or exact measured fossil is claimed.

Primary sources: [Smith 2014, DOI 10.1111/pala.12063](https://doi.org/10.1111/pala.12063); [Zhang, Smith & Shu 2015, DOI 10.1038/srep14810](https://doi.org/10.1038/srep14810); [2023 correction, DOI 10.1038/s41598-023-48303-1](https://doi.org/10.1038/s41598-023-48303-1); [Royal Ontario Museum specimen/source page](https://burgess-shale.rom.on.ca/fossils/wiwaxia-corrugata/).

### Hanging Valley

The final model reads as a broad lower main trough and a smaller elevated tributary that ends at a real drop/lip above the main floor. Hero, reverse and top views show the higher junction; the actual blue fall is thin and low contrast, but it is a visible free vertical descent rather than water simply running through the wall. The main trough is U-shaped, though the 512px front section is a simplified low-poly U/V-to-flat profile. Terrain surfaces are quiet and much plainer than the original concept, but the diagnostic landform survives. This is generic nominal-scale glacial terrain, not Bridalveil or another measured site.

Source: [National Park Service, U-shaped valleys, fjords and hanging valleys](https://www.nps.gov/articles/ushapedvalleysfjordshangingvalleys.htm).

### Mudpot

The final is a low irregular shallow basin with a finite slumped rim, opaque pale muddy interior, several low domes and one collapsed-cup/crater structure. It does not read as a geyser cone or erupting simulation. The muddy surface and bubble relief are intentionally static; coloration and gas state are illustrative, not a chemical/temperature assay or a named Yellowstone replica. At 512 px the pale palette makes the mud/bubble relief restrained, but top and hero remain diagnostic.

Sources: [NPS, Yellowstone hydrothermal features](https://www.nps.gov/yell/learn/nature/hydrothermal-features.htm); [NPS Fountain Paint Pot](https://www.nps.gov/features/yell/tours/fountainpaint/fountainpaintpot.htm).

### Dike Wall

Hero/front/rear show the dark, narrow, finite-thickness tabular intrusion cutting across each horizontal host bed. Top and side views preserve the cross-cutting orientation and the resistant irregular crest; it does not read as a parallel sill or a generic stack of blocks. The host beds are a teaching cutaway, not measured stratigraphy; locality, age and exact lithology are not asserted.

Sources: [NPS, Intrusive igneous landforms](https://www.nps.gov/subjects/geology/intrusive-igneous-landforms.htm); [FHWA reference photograph](https://fhwaapps.fhwa.dot.gov/bywaysp/photos/82356).

## Queued rebuild receipt summary

Each row denotes two separate successful queued runs. The full, independently matched request/result SHA-256 values, output/semantic bindings and fingerprints are in `independent-static-checks.json`.

| Asset | Rebuild 1 PID / UTC interval | Rebuild 2 PID / UTC interval | Both output and semantic matches |
|---|---|---|---|
| wiwaxia | 349 / 14:10:28.925–14:10:32.333 | 373 / 14:10:32.684–14:10:35.697 | PASS, exact final bytes |
| hanging-valley | 187 / 14:12:49.922–14:12:53.409 | 211 / 14:12:53.816–14:13:00.586 | PASS, exact final bytes |
| mudpot | 445 / 14:10:43.272–14:10:46.394 | 469 / 14:10:46.753–14:10:50.844 | PASS, exact final bytes |
| dike-wall | 239 / 14:13:05.480–14:13:08.283 | 263 / 14:13:08.968–14:13:16.406 | PASS, exact final bytes |

## Exact supporting artifacts

All QA files are new and separate from the producer worktree under `/workspace/shared/lowpoly-round27-qa69/`:

- `independent-static-checks.json`: independent source, concept/reference rights, render/image, count/bounds/budget, and rebuild checks.
- `independent-runtime-checks.json`: independent Khronos and Three.js CPU parse results; GPU and scene explicitly not run.
- `source-reopen-<asset>.json` and `.log`: four direct Blender 4.3.2 read-only source reopen measurements and process logs.
- `independent_static.py`, `independent_runtime.mjs`: small reproducible QA scripts.

**No producer files, approvals, remote refs, site, CI, permissions, credentials or security settings were changed.**
