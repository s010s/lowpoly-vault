# Static catalog and delivery build, v2

## Outputs and commands

- Review: `SITE_BASE=/lowpoly-vault/ SITE_ORIGIN=https://s010s.github.io node site/prepare-review.mjs`.
- Review output: `qa/redesign-v2-site`. The previous `qa/redesign-site` output is protected against replacement. Review generation does not create an approved source manifest or modify source QA.
- Release: `SITE_BASE=/lowpoly-vault/ SITE_ORIGIN=https://s010s.github.io npm run build`.
- Root/custom domains: set `SITE_BASE=/` or an explicit absolute prefix such as `/catalog/`; set `SITE_ORIGIN` to that deployment's actual origin. URLs are generated centrally rather than resolved relative to a model directory.
- `SITE_BASE` must be an absolute, traversal-free path prefix. All route links, resource links, canonical URLs, alternate languages, social metadata, and sitemap URLs account for it.

Every model has two actual HTML documents: `/models/<id>/` and `/zh-CN/models/<id>/`. There are localized home, about, and model listing pages, including `/models/page/2/` and subsequent pages as needed. The ten-candidate review currently generates 26 content documents plus a useful standalone `404.html`. Unknown URLs are not rewritten to the application shell.

Each detail document includes a visible article with name, description, preview, specifications available from reliable metadata, attribution, source references, and actual download links. It has a unique title/description/canonical, bilingual hreflang, Open Graph metadata, and CreativeWork JSON-LD. A visible locale-switch anchor works without JavaScript. The client may progressively enable the detail article's `data-enhance-model` button. It should only hide static listing content after its interactive replacement succeeds.

## Model delivery and attribution

`asset-delivery.mjs` validates the supplied manifest and copies only its exact `glb`, `blend`, and `preview` files. There is no recursive source-directory copy. QA, references, experiments, metadata sidecars, and unlisted source files are excluded. Paths are checked for traversal, unsafe characters, restricted directories, and symlinks escaping the asset root; supplied SHA-256 values must match.

With no approved `assets/manifest.json`, release output contains no model payloads, catalog, or downloads. It still contains informative bilingual landing/list/about pages. A review-only manifest is rejected by release delivery.

Build-time `stat` measurements produce exact `file_sizes.glb`, `file_sizes.blend`, and, after packaging, `file_sizes.bundle`. `downloads` provides actual paths. Python's standard-library ZIP implementation creates one deterministic archive per asset containing its original GLB, Blender source, and `CREDITS.txt`. An individual downloadable attribution text is also available. Review archives are explicitly marked as unapproved. Material counts are only exposed when a passing existing GLB QA report records the count and its checksum matches the manifest. Missing material evidence stays unknown. Existing dimension/source/scientific metadata is preserved.

## Independent taxonomy

Legacy IDs, collection, category, and storage paths are preserved. Worlds are multiple memberships with a legacy collection fallback. Packs are independent multiple memberships. `curation.js` explicitly assigns the ten existing candidates to `prehistoric-starter`; this does not infer a pack from every world. The pack record includes localized name/description and ordered IDs. Production facet counts only include actual manifest entries. Optional subcategory/tags/eras/biomes and complete provenance remain intact in detail metadata; planning inventories are never loaded by the site.

## Scaling and checks

`catalog.js` keeps summaries in 256-item shards, eight cached shards, four detail entries, serial/cancellable reads, and bounded rendered pages. Only a selected complete detail entry is loaded. The initial 24 summaries are embedded in the index. Shared query semantics support bilingual terms, category, world, pack, legacy collection, name/triangle sorting, and maximum triangle count. URL state additionally carries pagination and grid/map view.

Commands:

- `node site/catalog-test.mjs`: original 10,000-record compatibility/cancellation/cache tests
- `node site/catalog-v2-test.mjs`: 10,000 records across 17 deliberately uneven categories, overlapping worlds/packs, combined filtering, triangle limits, and route/query round trips
- `node site/static-routes-test.mjs`: actual bilingual documents, pagination, root/custom/project prefixes, metadata, ZIP contents, exact bytes, release allowlist, and unsafe path refusal
- `node site/manifest-test.mjs`: existing release/review and QA gates

Observed v2 synthetic run in this environment: 40 shards; 30,383-byte index; approximately 2.89 MB of complete summary shards; 38 ms in-memory catalog generation. The initial page required no additional shard request; the final page required one. These are measurements of this fixture/environment, not promised network or browser rendering latencies. The synthetic fixtures exist only inside test programs and do not enter any build, inventory, facet, or sitemap.
