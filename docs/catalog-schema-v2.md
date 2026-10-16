# Catalog schema v2: shared implementation and inventory contract

Status: canonical v2 contract, 2026-10-16. Additive extensions are permitted through review; IDs and original source paths remain stable. Research inventory is a planning artifact, never a released asset manifest.

## Independent axes

- `id`: globally unique stable kebab-case asset ID. Existing IDs remain unchanged even where a folder differs. No world/category name is required in the ID.
- `name`, `description`: localized objects with `en` and `zh` keys. Routes use locale `zh-CN`; metadata retains existing `zh` key compatibility.
- `worlds: string[]`: many-to-many broad creative worlds/themes. The current real collection has `prehistoric`. Do not create speculative world facets in the production catalog.
- `packs: string[]`: many-to-many finite curated groups. The actual ten candidates belong to `prehistoric-starter`. A pack is not a world or a category; a model may appear in several packs without duplicating its files or ID. Pack records have id, localized name/description and ordered asset IDs. Research may define proposed packs, clearly marked planning, but these must not enter the site's live facets.
- `category: string`: one cross-world functional/form class. Existing stable categories are `plants`, `geology`, `wood`, `traces`. New categories can be added when the research requires distinct useful classes, e.g. `animals`, `fungi`, `terrain`, `water`, `props`, `structures`; category names must describe asset form/use rather than an era, locality or pack.
- `subcategory: string | null`: controlled refinement within the chosen category, e.g. plants/tree, plants/fern, geology/arch, traces/nest. Do not encode taxonomy rank as a mandatory category tree. A registry may add new subcategories without changing storage paths.
- `taxon_group: string | null`: optional reference-supported organism grouping, independent of form-based subcategory; uncertainty belongs in scientific notes.
- `tags: string[]`: controlled discoverability descriptors; optional. Do not duplicate every axis as a tag. Bilingual labels live in a registry, IDs are English kebab-case.
- `eras: string[]`: optional controlled geological intervals, as specifically supported; broad or mixed intervals are allowed only with notes. Never invent precise coexistence claims for an art asset.
- `biomes: string[]`: optional supported environment descriptors, kept separate from geological time and world membership.
- `scientific_scope: {en,zh}` and `sources: [{title,url,...}]`: distinctions between reference-supported identity, reconstruction, generic composite and artistic simplification. Unknown is explicitly unknown.

## Production compatibility and specifications

Existing `collection` stays as a legacy primary-world alias, read fallback only. `worlds` falls back to `[collection]`. Category and path compatibility remain untouched; no directory migration is necessary. Assets are not copied to multiple directories when assigned to multiple packs.

Existing `preview`, `glb`, `blend`, `triangles`, `dimensions`, license and attribution fields remain. Dimensions are the existing X×Y×Z source meter bounds and require trustworthy unit/export verification before a metric viewer reference appears. `file_sizes: {glb,blend,bundle}` contains exact bytes measured at build, never hand-entered estimates. `downloads: {glb,blend,bundle}` contains actual published paths. Reliable format availability derives from real files. Materials/animation/color filters must not appear until data is actually verified; missing fields are not false claims.

## Research inventory additions (not deployment)

A planning record may additionally contain `status` (`existing-candidate` or `planned`), `priority`, `complexity`, `reference_notes`, and `production_notes`. Existing candidates retain exact current IDs. Proposed records get stable proposed IDs and at least one source supporting identity or form; source licensing is not permission to copy geometry or artwork. Existing candidate QA states remain unchanged. Planned records and packs are not exported to site manifests, counts, search suggestions or sitemaps.

Research can propose necessary taxonomy additions with rationale. The implementation owner reconciles these additions into this contract; the inventory should reference `schema_version: 2`.
