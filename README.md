<div align="center">

# Lowpoly Vault

**Original low-poly assets. Worlds of possibility.**

Made with Blender · Built to edit, reuse, and remix

[Browse assets](https://s010s.github.io/lowpoly-vault/) · [Formats & workflow](#formats--workflow) · [License](#license--credit) · [简体中文](README.zh-CN.md)

</div>

Lowpoly Vault is a growing library of original, stylized 3D assets by **Leon Made This / [s010s](https://github.com/s010s)**. From everyday objects and natural landscapes to futuristic, fantasy, and alien worlds, the vault leaves room for many different themes.

> **Initial collection.** Ten original models with GLB, editable Blender source and attribution downloads. The models remain a work in progress; artistic and scientific refinement is ongoing.

## Formats & workflow

| Edit | Use | Explore |
| :--- | :--- | :--- |
| Editable **Blender** sources | Portable **GLB** exports | **PNG** previews and a categorized **Web 3D** gallery |
| Change geometry, materials, and composition | Bring assets into real-time scenes | Find assets by theme and category |

Reproducible scripts and reusable Skills will document the path from modeling to export. The gallery is hosted on [GitHub Pages](https://s010s.github.io/lowpoly-vault/) with English and Simplified Chinese model pages.

**Choose a theme → find an asset → edit or import → credit the creator.**

## Browse assets

Each theme keeps its asset notes beside its files. Themes can grow independently without changing the library's overall structure.

| Theme | Scope | Status |
| :--- | :--- | :--- |
| [Prehistoric environments](assets/prehistoric/) | Terrain, plants, and environmental details | In progress |

Additional themes will appear here as they are developed.

## Inside the vault

Existing source folders retain the legacy **theme → broad category → asset slug** layout below. Catalog identity and membership are independent: changing a world, pack, or category does not move files or duplicate an asset. Final-quality releases require full QA approval; this initial collection uses a separate owner-authorized, checksum-pinned publication manifest:

```text
assets/
├── manifest.json                 # Shared catalog for all themes
└── <theme>/
    ├── README.md                 # Theme notes and scope
    ├── README.zh-CN.md
    └── <category>/
        └── <slug>/
            ├── <slug>.blend      # Editable Blender source
            ├── <slug>.glb        # Real-time model
            └── preview-hero.png       # Preview image
```

The published shared catalog lives at `assets/manifest.json`; review builds generate a separate review-only manifest. New metadata can use `worlds` and `packs` without `collection`; legacy `collection` remains a primary-world fallback. See [schema v2](docs/catalog-schema-v2.md).

## License & credit

Different content uses different licenses:

- **[CC BY 4.0](LICENSES/CC-BY-4.0.txt)** — original models, renders, images, asset metadata, documentation, and Skills prose
- **[MIT](LICENSES/MIT.txt)** — original modeling/export scripts, website code, workflows, configuration code, executable Skill scripts, and documentation code examples
- **Third-party materials** — their respective licenses apply

When sharing CC BY 4.0 content, credit **Leon Made This / s010s**, link to the source and license, and describe changes. When distributing MIT code, retain its copyright and permission notices. See [LICENSE](LICENSE) for the scope and [ATTRIBUTION.md](ATTRIBUTION.md) for asset credit examples.

## Gallery and publication

The first published collection contains exactly ten original models. The owner authorized this initial release while further visual refinement remains ongoing; publication does not promote the historical per-asset QA records to final artistic or scientific approval. The gallery now has independent worlds, multi-membership curated packs and cross-world categories. Existing IDs and file paths are unchanged. Global browsing defaults to a compact searchable grid; a map is available only for a selected real pack of at most 30 models. Planned inventory never appears in live counts or search suggestions.

Build-time English and Simplified Chinese model pages are real HTML documents: `/models/<id>/` and `/zh-CN/models/<id>/`. They retain descriptions, images, attribution and downloads without JavaScript. Ordinary list clicks enhance to a modal while preserving filter/sort/query/page state and Back navigation. ZIP downloads contain the GLB, editable source and CREDITS.txt; sizes are measured from the actual files.

Review commands: `npm test` (structural review checks; no approval), `npm run test:redesign`; `SITE_BASE=/lowpoly-vault/ node site/prepare-review.mjs`; `node site/redesign-browser-test.mjs`. See [build and release safety](docs/static-catalog-build-v2.md), [schema v2](docs/catalog-schema-v2.md), and the [implementation checklist](docs/redesign-v2-checklist.md). The release copier uses an explicit file allowlist. `npm run publication:check` validates the initial release against `assets/initial-publication.json` and all original bytes; `npm run manifest:check` retains the separate strict formal-QA gate. Every deployment passes a full output audit and real-model browser tests. See [initial publication](docs/initial-publication.md).

A three-model [preview experiment](experiments/preview-turntable-v3/README.md) preserves original scale and geometry. Measurements favor static cards plus lazy real GLB inspection over 16-frame sprite sheets for this small collection. CPU proxies and cloud UI fallback screenshots are clearly separated from actual browser/WebGL and touch-device acceptance.
