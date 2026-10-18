# Current-release preview payload audit

Baseline: `01c60dd85322932a967c4f2aa50045f2da1a25bd`. Exact measured files come from the selected ten-asset manifest, not historical frames. This is payload and baseline-source evidence, not browser/hardware performance certification.

| Asset | GLB bytes | Poster bytes | 24-frame bytes | GLB saving vs full sequence |
|---|---:|---:|---:|---:|
| natural-arch | 51,388 | 9,650 | 204,010 | 74.81% |
| stratified-cliff | 82,896 | 11,460 | 263,632 | 68.56% |
| conifer-tree | 715,500 | 34,692 | 824,778 | 13.25% |
| cycad | 154,316 | 20,748 | 501,954 | 69.26% |
| fern-cluster | 420,508 | 23,692 | 545,260 | 22.88% |
| horsetail-cluster | 107,256 | 26,082 | 607,156 | 82.33% |
| lepidodendron | 158,864 | 23,126 | 499,398 | 68.19% |
| dinosaur-nest | 85,872 | 8,554 | 207,948 | 58.71% |
| three-toed-track | 48,552 | 8,074 | 197,584 | 75.43% |
| uprooted-log | 55,460 | 11,518 | 280,974 | 80.26% |
| **Total** | **1,880,612** | **177,596** | **4,132,694** | **54.49%** |

The model payload saves **2,252,082 bytes** against fully visiting every sequence angle. Static poster plus GLB totals **2,058,208 bytes**; poster plus all frames totals **4,310,290 bytes**, excluding sequence manifests. HTTP compression, headers, Three.js/code delivery, decode time, GPU allocations and runtime draw cost are not measured here.

## Important interpretation

- Existing scrubbing requests only the active frame plus two neighbors. Every GLB is larger than its first three scrub frames; the full-sequence comparison does not establish a cold-hover latency or short-hover bandwidth win.
- Every poster equals its frame 0 byte-for-byte but has a separate URL. The report counts actual file/URL payloads and does not assume cross-URL cache deduplication.
- All 10 GLBs, 10 source previews, 10 selected sequence manifests, 10 posters and 240 frames match their recorded SHA-256 identities. All selected posters/frames decode to 768 × 768 with transparent pixels. No assets were changed.
- The older image-scrub checkpoint totals in the existing docs are historical; this report follows the current mixed-release replacements.

## Baseline scaling safeguards

- Catalog: 256-item summary shards, eight cached shards, four detail entries, first 24 summaries embedded. Grid: 24 mounted cards. The global map is disabled; the optional pack map is offered only for explicit packs of at most 30 assets. Its geometry helper additionally caps visible candidates at 80.
- Ordinary name pagination skips earlier shards using descriptor counts. Search and combined filters scan relevant shards. Deep numeric sorting can retain up to the full catalog outside the eight-shard LRU, so it is not constant-memory search.
- Source-inspected ModelStage: one shared renderer/live model, serialized model request/parse work, three-file/24 MiB original-byte LRU, on-demand drawing, visibility suspension, DPR cap 2, retained poster on WebGL failure. These are baseline safeguards, not final-new-controller acceptance.
- The selected conifer retains documented SwiftShader frame-budget failures and narrowly scoped hardware acceptance; byte savings do not remove rendering cost.

## Checks actually run

- `node site/catalog-test.mjs`: pass; 10,000 records / 40 shards, 0 first-page shard requests, 1 distant-page shard request, caches ≤8 shards/4 details, peak requests 1 per metadata lane, cancellation/path/filter checks.
- `node site/catalog-v2-test.mjs`: pass; 10,000 records across 17 uneven categories, 30,383-byte index and 2,888,068-byte serialized synthetic summary fixture, overlapping worlds/packs, bounded cache and distant-page checks.
- `node site/turntable-delivery-test.mjs`: pass; 15 base checks plus 55 revision-route checks.
- Isolated atlas geometry sampling: pass for 10 and 10,000 synthetic records, 1,176 sampled viewports each, observed maximum 10/80 visible candidates. No production fixture data was written.

Full file hashes, per-frame measurements, startup-neighbor costs and limitations are in [payload-audit.json](payload-audit.json). Command output is retained in [catalog-and-delivery-tests.json](catalog-and-delivery-tests.json) and [atlas-geometry-check.json](atlas-geometry-check.json).
