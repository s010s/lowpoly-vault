<div align="center">

# Lowpoly Vault

**Original low-poly assets. Worlds of possibility.**

Made with Blender · Built to edit, reuse, and remix

[Browse assets](#browse-assets) · [Formats & workflow](#formats--workflow) · [License](#license--credit) · [简体中文](README.zh-CN.md)

</div>

Lowpoly Vault is a growing library of original, stylized 3D assets by **Leon Made This / [s010s](https://github.com/s010s)**. From everyday objects and natural landscapes to futuristic, fantasy, and alien worlds, the vault leaves room for many different themes.

> **Work in progress.** The library, exports, and browsing experience are being built. Entries below describe the intended structure; a complete asset release and hosted gallery are not yet available.

## Formats & workflow

| Edit | Use | Explore |
| :--- | :--- | :--- |
| Editable **Blender** sources | Portable **GLB** exports | **PNG** previews and a categorized **Web 3D** gallery |
| Change geometry, materials, and composition | Bring assets into real-time scenes | Find assets by theme and category |

Reproducible scripts and reusable Skills will document the path from modeling to export. The gallery is planned for GitHub Pages; its link will be added after deployment is verified.

**Choose a theme → find an asset → edit or import → credit the creator.**

## Browse assets

Each theme keeps its asset notes beside its files. Themes can grow independently without changing the library's overall structure.

| Theme | Scope | Status |
| :--- | :--- | :--- |
| [Prehistoric environments](assets/prehistoric/) | Terrain, plants, and environmental details | In progress |

Additional themes will appear here as they are developed.

## Inside the vault

Assets are organized by **theme → broad category → asset slug**. The following is the target layout, not a list of files already released:

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

The shared catalog lives at `assets/manifest.json`. Broad categories keep related assets together; theme-specific context and limitations belong in each theme's README.

## License & credit

Different content uses different licenses:

- **[CC BY 4.0](LICENSES/CC-BY-4.0.txt)** — original models, renders, images, asset metadata, documentation, and Skills prose
- **[MIT](LICENSES/MIT.txt)** — original modeling/export scripts, website code, workflows, configuration code, executable Skill scripts, and documentation code examples
- **Third-party materials** — their respective licenses apply

When sharing CC BY 4.0 content, credit **Leon Made This / s010s**, link to the source and license, and describe changes. When distributing MIT code, retain its copyright and permission notices. See [LICENSE](LICENSE) for the scope and [ATTRIBUTION.md](ATTRIBUTION.md) for asset credit examples.
