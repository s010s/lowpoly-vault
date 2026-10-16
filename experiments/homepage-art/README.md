# Forms for worlds

An original editorial homepage composition for Lowpoly Vault, rendered from four existing repository models. This is a curated display of independent stylized objects, not a claim that they form a scientifically coexisting prehistoric ecosystem.

## Outputs

- `../../site/public/home/editorial-hero.webp`: optimized homepage artwork, 1600 × 1000
- `../../site/public/home/editorial-hero.png`: full-resolution PNG
- `../../site/public/home/editorial-hero.json`: model references, source hashes, display transforms, render settings, and license metadata
- `hero.blend`: editable composition, with a separate collection for each original model and for all editorial staging
- `build_hero.py`: reproducible composition and render script

Background: **#F2EFE7**. The left 36–40% is intentionally quiet for a headline. Objects and their shadows are physically rendered together. The floor is a Cycles shadow catcher composited onto the exact paper color so the artwork can meet the page background without a visible frame.

## Reproduce

Run from the repository root with Blender 4.3.2:

```sh
blender -b --threads 8 --python-exit-code 1 --python experiments/homepage-art/build_hero.py -- --preview
blender -b --threads 8 --python-exit-code 1 --python experiments/homepage-art/build_hero.py
python experiments/homepage-art/encode_webp.py
```

The preview is 1000 × 625 at 12 samples; the final is 1600 × 1000 at 64 samples. Both use Cycles CPU without denoising. Production asset files are read only and hashed before and after rendering. Rerunning replaces only the homepage composition outputs.

## Original models used

- [Natural Arch](https://github.com/s010s/lowpoly-vault/tree/main/assets/prehistoric/geology/natural-arch)
- [Conifer Tree](https://github.com/s010s/lowpoly-vault/tree/main/assets/prehistoric/plants/conifer-tree)
- [Cycad Rosette](https://github.com/s010s/lowpoly-vault/tree/main/assets/prehistoric/plants/cycad)
- [Fern Cluster](https://github.com/s010s/lowpoly-vault/tree/main/assets/prehistoric/plants/fern-cluster)

Only scene position, uniform scale, and rotation change. No production mesh, palette, metadata, or preview is overwritten. The geometric display risers are original staging for this artwork and are not additional catalog assets. No third-party model, texture, photograph, or illustration is used.

## Attribution and license

“Forms for worlds,” using models from Lowpoly Vault, by **Leon Made This / s010s**. Source: https://github.com/s010s/lowpoly-vault . Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: original editorial arrangement, display transforms, staging, lighting, and camera. Provided as-is, without warranties.

The original composition, renders, and `.blend` scene follow the repository's CC BY 4.0 content license. Scripts use MIT. See the root LICENSE and ATTRIBUTION.md for the complete scope.

Production: GPT-6 Astra, xhigh; cloud Blender 4.3.2. No access to the user's Mac was used.
