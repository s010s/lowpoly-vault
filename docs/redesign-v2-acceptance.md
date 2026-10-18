# Asset browser v2: review handoff

This is a **review candidate**, not an asset release or a public deployment.

## Verified implementation

- Stable original asset IDs and file paths; world/theme membership is separate from curated packs and cross-world category. A model may belong to multiple worlds and packs. The shared contract is [catalog schema v2](catalog-schema-v2.md); the 1,000-item research inventory is separate planning data, never fabricated live content.
- Global searchable grid with compact controls, real suggestions and honest empty results. URL query, category, world, pack, triangle limit, sort and page survive navigation. Map mode is available only for a selected real pack with at most 30 items; sparse categories use one compact arrangement.
- Real bilingual HTML at `/models/<id>/` and `/zh-CN/models/<id>/`, including visible no-JavaScript content, title/description, canonical/hreflang, Open Graph, structured data and sitemap. Ordinary anchors work without an SPA 404 workaround. GitHub project paths, root paths and custom origins have tests.
- List clicks progressively enhance to a keyboard-contained dialog. Back/Forward, close, neighboring models and same-pack links retain the originating results, scroll and focus. Direct detail documents remain readable before optional 3D enhancement.
- Exact file sizes, GLB/Blender downloads, a real ZIP containing both originals and CREDITS.txt, and initiation-only download feedback. Release copying uses the approved manifest allowlist; QA, experiments and third-party references are excluded.
- Singleton 3D renderer, one in-flight request, bounded byte cache, canceled stale work, on-demand drawing, wireframe and disposal. The optional grid states verified meter spacing from decoded bounds; original asset geometry and authored scale are unchanged.

## Test result and measured limits

The full browser review at final code commit `7bd2ced4948a36dfb28dbb0367de0da61786f529` passed both profiles in [GitHub Actions run 38953140279](https://github.com/s010s/lowpoly-vault/actions/runs/38953140279), including the static-label contrast correction found during screenshot inspection. The following evidence-only commit does not change site code or models.

- 10 actual GLBs parsed and drawn in Chromium 141 using software WebGL/SwiftShader. Every model passed wireframe, metric-grid, orbit/zoom/reset, theme retention and scene-disposal checks.
- Independent forced-WebGL-failure profile retained the actual previews, accessible explanation and downloads.
- 26 bilingual static documents and 40 original/download/credits endpoints passed HTTP/content/byte-size checks. Missing detail routes returned 404. No page or resource errors occurred. JavaScript-disabled specification labels meet the tested 4.5:1 minimum contrast in both color-scheme settings.
- English/Chinese × light/dark × desktop/390px touch-emulated Chromium screenshot matrix passed layout and interaction checks. Selected screenshots in `qa/redesign-v2-evidence/` were visually inspected. Cloud desktop screenshots and a 390px iframe were also inspected. These are not physical Android testing or hardware-GPU performance measurements.
- Browser stress fixture: 10,000 records, 39 uneven categories, 7 worlds, 400 packs, 417 result pages, 24 visible card nodes and 1,068 total DOM nodes. Peak GLB requests: 1; byte-cache entries: 3; retained bytes: 293,288; renderer creations: 1 (0 in forced fallback). Closing the detail leaves zero live scenes and scheduled draw frames. The fixture intercepts in-memory catalog data, so these measurements are not a network-capacity benchmark.
- Separate Node catalog fixture: 17 uneven categories, 30,383-byte index, 40 summary shards totaling 2,888,068 bytes, one shard needed for a distant page. This measures catalog construction and lookup, not GPU/network performance.

## Preview-method decision

Three unchanged original assets were rendered with common camera/light/background/framing rules and 16 views: dinosaur-nest, lepidodendron and natural-arch. The source geometry and authored scale were preserved.

Clean statics total **12,228 bytes**, versus **171,688 bytes** for three sheets (14×). A decoded sheet has a **4 MiB RGBA8 pixel budget**, versus **0.25 MiB** for one static. Actual cloud Chromium fresh-image decoding from preloaded bytes measured static medians **1.00–1.20 ms**, sheet medians **9.90–13.20 ms**. These exclude network, GPU upload and Android performance. Shadow alpha was grainy/cropped and did not composite equivalently on light and dark backgrounds.

**Decision:** retain static previews and lazy real GLB; do not ship the sprite experiment. Full render settings, per-file sizes, exact samples and comparison images are in [the experiment report](../experiments/preview-turntable-v3/README.md).

## Build and preservation

- Isolated candidate build: `qa/redesign-v2-site/`, base `/lowpoly-vault/`, canonical origin `https://s010s.github.io`. This configured origin does not mean the build has been published.
- The local build has **100 files / 25,125,181 bytes / 26 static documents**. Exact build inventory and SHA-256 hashes: `qa/redesign-v2-build-verification.json`.
- Original directory and old port-5188 review build are preserved. All 20 original GLB/Blender hashes match authored metadata and the untouched original directory: `qa/redesign-source-preservation.json`.
- Branch checkpoints are on `redesign/asset-browser-wip`, authored with the owner's no-reply address. Two private 18:48 UTC Drive ZIPs preserve original assets (80,542,918 bytes) and code/renders (57,188,345 bytes); a final incremental code/evidence archive follows this verification.

## Remaining owner review and deployment gate

- Physical Android interaction and performance review; artistic/scientific approval of the candidate models. Automated green checks do not grant either approval.
- Optional separately authorized private phone-preview deployment. Sites supports a static `dist` directory, but its private URLs are still production endpoints; deployment requires explicit approval. Rebuild the isolated allowlisted review output with `/` as base and the returned deployment origin, retain noindex/review notices, then verify nested directory routes and true 404 behavior on the actual host.
- No Sites deployment, Pages publication, main merge or release-manifest approval has been performed by this redesign task.
- The on-demand Three.js viewer chunk is about 606 kB (155 kB gzip) and still triggers Vite's chunk-size warning. It is lazy-loaded; this is a disclosed build characteristic, not a claim of zero startup cost.
