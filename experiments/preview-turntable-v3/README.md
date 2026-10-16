# Preview method experiment v3

## Decision

**Keep optimized static images for catalog cards and the existing on-demand GLB viewer for actual rotation. Do not integrate the 16-frame sprite into the catalog yet.**

A clean cutout sheet is smaller than the *uncompressed* nest and lycopsid GLBs, but its 4 MiB RGBA8 pixel budget is 16 times that of one 256 px image. For the arch, even the clean sheet is larger than the actual GLB. These GLBs also compress well over HTTP if the host supports it. A sheet does not provide arbitrary orbit/elevation, zoom detail, relighting, or geometry inspection.

The transparent shadow-catcher version fails this prototype's visual/weight tradeoff: grain reaches the tile edges, its alpha data compresses poorly, and dark-theme compositing is not physically equivalent to a dark floor. The clean variant avoids the background/shadow grain, but appears ungrounded. It is a useful comparison, not a production-art approval.

**Possible later niche:** an explicitly activated, GPU-free turntable on a detail page. It would need a real browser/mobile decode and memory test, a restrained cache, keyboard/touch QA, and a higher-quality shadow decision. No runtime files were changed here.

## Exact encoded sizes

All numbers below are actual on-disk bytes, not estimates. Static and sprite images use identical source render frames, WebP quality 82, method 6, alpha quality 100. Sheets are 4×4 / 1024×1024; frames are 256×256.

| Asset | Clean static | Clean 16-view sheet | 16 separate clean frames | Original GLB | GLB gzip-9 estimate |
|---|---:|---:|---:|---:|---:|
| dinosaur-nest | 3,156 | 45,358 | 48,870 | 85,872 | 27,390 |
| lepidodendron | 5,656 | 78,440 | 83,342 | 158,864 | 54,241 |
| natural-arch | 3,416 | 47,890 | 51,748 | 40,656 | 13,598 |

All three clean statics total **12,228 bytes**; their sheets total **171,688 bytes**, about **14.0×** more. Sheet packaging saves only about 6–8% versus the encoded separate frames here. Its main packaging advantage is one request; it also forces the whole sheet to be decoded. Separate frames allow demand loading, but 16 eager image elements can still retain 4 MiB of decoded pixels plus overhead.

The gzip column is an optional transport-compression calculation, **not a verified hosting response**. Actual renderer/loader JavaScript transfer, cache behavior, shader compilation, GPU upload, and WebGL framebuffer cost were not measured. Raw GLB file size alone is not complete 3D startup cost.

| Asset | Shadow RGBA static | Shadow RGBA sheet | Opaque-light static | Opaque-light sheet | Opaque-dark sheet |
|---|---:|---:|---:|---:|---:|
| dinosaur-nest | 12,434 | 196,348 | 2,272 | 34,090 | 27,262 |
| lepidodendron | 27,326 | 423,612 | 6,178 | 92,038 | 24,160 |
| natural-arch | 27,240 | 438,040 | 6,518 | 102,886 | 27,662 |

The very small opaque-dark files partly reflect compressed low-contrast dark areas; they are not evidence of equal visual quality or theme interchangeability. Opaque light/dark variants are composites of the same shadow RGBA, while the separate `hero-physical-*` checks actually rerender the floor.

## Decoded pixel budgets and measured CPU proxies

- One 256×256 RGBA8 static: **262,144 bytes / 0.25 MiB**.
- One 1024×1024 RGBA8 sheet: **4,194,304 bytes / 4 MiB**.
- Sixteen separately decoded RGBA8 frames: **4 MiB total**; one resident frame is 0.25 MiB.
- Three visible statics: **0.75 MiB**, versus **12 MiB** if all three sheets are decoded.
- Formula-only scale illustration: 100 resident card statics = **25 MiB**; 100 sheets = **400 MiB**. This is a pixel budget, not observed browser residency.

The actual GLB packed attribute/index buffers are 76,836 / 151,164 / 35,520 bytes for nest / lycopsid / arch. Those are **geometry-only lower bounds**, not complete GPU or JavaScript memory. There are no textures in these GLBs.

| Asset | Clean static decode, median / p95 ms | Clean sheet decode, median / p95 ms | All 16 clean frames, median / p95 ms | GLB Node parse, median / p95 ms |
|---|---:|---:|---:|---:|
| dinosaur-nest | 0.647 / 0.821 | 12.311 / 17.895 | 12.065 / 16.813 | 1.322 / 7.616 |
| lepidodendron | 0.671 / 0.814 | 11.203 / 14.295 | 11.244 / 11.950 | 0.763 / 7.878 |
| natural-arch | 0.706 / 0.982 | 10.779 / 14.061 | 12.179 / 18.648 | 0.302 / 2.431 |

**These are CPU proxies, not browser timings and not an apples-to-apples browser race.** Image timing uses Pillow 12.3.0 / libwebp 1.6.0 on Python 3.12.14: encoded bytes preloaded, open + decode + RGBA conversion + byte allocation included. GLB timing uses Three.js 0.180.0 GLTFLoader in Node 24.19.0: parse plus object/material/buffer allocation, without rendering or GPU upload. Both use five warmups and 40 measured iterations, in a shared AMD EPYC 9V74 cloud environment with no CPU affinity or exclusive-load guarantee. Exact samples are in the JSON reports.

Browser measurement could not be obtained: the bundled Playwright browser is absent; installed Chromium failed with a sandbox socket restriction, and the supported elevated retry failed during sandbox setup. No security restriction was bypassed. Browser decode, mobile behavior, GPU upload, frame rate, and actual residency remain **unmeasured**. The isolated `index.html` includes an optional `createImageBitmap` probe to collect real browser decode samples when a supported browser can run it; this page itself has not had browser interaction QA.

## Art direction and preservation

- **Original sources only:** `dinosaur-nest`, `lepidodendron`, `natural-arch` under `assets/prehistoric`; no third-party imagery, models, or textures.
- All original `.blend` and `.glb` hashes still match their original metadata. No source geometry, source material, source object transform, authored scale, or asset file was changed.
- The experimental scene loads the original source and retains its scene objects. Non-EXPORT presentation objects are hidden in the copy, rather than indiscriminately deleted. The report inventories them and their original visibility/transforms.
- Shared **orthographic** projection, nominal lens 50 mm (irrelevant to orthographic perspective), **35° elevation**, starting azimuth **−55°**, 16 equal **22.5°** steps.
- Each asset's evaluated world-space vertices are projected at every view. The maximum centered radius is fit to **82%** of the square frame. One constant orthographic scale is used for all frames of that asset. No per-frame zoom pumping, object rescaling, or shape distortion.
- Objects retain their natural silhouette: the wide nest stays wide; the tall lycopsid uses the frame height. Their frame-zero width/height occupancy is approximately 73/42%, 44/76%, and 72/59% respectively. The shared fit limit is a maximum centered extent across all views, not a promise that every frame has 82% height.
- Neutral key/fill/rim rig is camera-relative and bounds-normalized. Power scales with bounds squared and light sizes/positions with bounds; **the source object does not scale**. Key/fill/rim powers are 70/20/25 watts per bounds-span squared; world strength 0.30. Same exposure and material palette for every asset.
- Blender **4.3.2**, **Cycles CPU**, **24 samples**, **no denoising**, no adaptive sampling, seed 42, Standard / None, 256×256 RGBA8 PNG. WebP conversion happens after rendering. Operator: **GPT-6 Astra, xhigh**, cloud computer only.

An overbright first pilot was corrected before the final common-rig render. Final rendered samples preserve grain honestly; they are a 256 px decision prototype, not final production-quality images.

## Visual inspection

Inspected `quick-look.png`, `quick-clean-look.png`, the alpha/shadow comparison and the final clean turntable contact sheet.

- The clean object silhouettes are intact through all 16 frames. Alpha is zero at every outer image edge; minimum alpha>8 object margin is 22 px for nest/arch and 23 px for lycopsid.
- The shadows are **not clean enough** at 24 samples. Their nonzero alpha reaches every tile boundary. Maximum edge alpha over all views is 15/255 (nest), 41/255 (lycopsid), and 47/255 (arch); the broad ground treatment is therefore visibly cropped/grainy in some orientations.
- WebP preserves the frame-zero shadow alpha exactly for all three images. Lossy RGB changes still exist, and byte-identical alpha does not fix the source shadow noise.
- Dark compositing hides most of the shadow and reduces the lycopsid's foliage/trunk contrast. The actual dark-floor renders visibly differ from composited light-floor shadow RGBA, especially underneath the arch. This is evidence against claiming universal background correctness.
- The arch changes width naturally through the turn; its narrow side views are not artificially enlarged. The nest's shallow original relief and the tree's small leaf facets remain limited by the original model and 256 px sampling. This experiment is not approval of their scientific or modeling quality.

## Files

- `index.html`: isolated static/sheet/separate-frame comparison and optional browser decode probe.
- `measurements.json`: exact encoded bytes, RGBA budgets, image decode samples, source camera framing and alpha checks.
- `glb-parser-proxy.json`: actual GLB bytes, mesh/triangle counts and Node parser timing samples.
- `art-direction-comparison.png`: original source hero beside unified views 00/04/08.
- `alpha-shadow-comparison.png`: clean/shadow on light/dark backgrounds plus physically rerendered dark floor.
- `clean-cutout-turntable-contact.png`: clean views 00/04/08/12 for all three assets.
- `<asset>/preview-scene.blend`: editable experimental scene with original objects retained and the added camera/light/catcher setup.
- `<asset>/render-report.json`, `clean-render-report.json`: source hashes, inventory, framing, render settings and timings.
- `<asset>/png-shadow/`, `png-clean/`: 16 original 256 px PNG frames each.
- `<asset>/frames-{clean,shadow,light,dark}/`: WebP frame sets.
- `<asset>/sheet-{clean,shadow,light,dark}.{png,webp}`: 4×4 sheets.
- `<asset>/hero-*.webp`: optimized static choices; `hero-physical-{light,dark}.png` are actual floor-render checks.

## Reproduce

From the repository root:

```sh
for asset in dinosaur-nest lepidodendron natural-arch; do
  blender -b -t 8 --python-exit-code 1 \
    --python scripts/experiments/render_preview_turntable_v3.py -- --asset "$asset"
  blender -b -t 8 --python-exit-code 1 \
    --python scripts/experiments/render_preview_turntable_v3.py -- --asset "$asset" --clean-only
done
python scripts/experiments/measure_preview_turntable_v3.py
python scripts/experiments/measure_preview_turntable_v3.py --add-clean
node scripts/experiments/measure_preview_glb_v3.mjs
```

Use an authorized local HTTP server rooted at this repository to open `experiments/preview-turntable-v3/index.html`. Serving the directory is not a deployment. Do not interpret the optional probe's `createImageBitmap` timings as complete page, GPU or GLB performance.

## License and status

Original models and rendered previews: **CC-BY-4.0**, **Leon Made This / s010s**. Experiment scripts: **MIT**. No third-party images or reference assets are included. These are art-directed displays of independent stylized assets, not a single coexisting ecological reconstruction.

**Status:** source preservation verified; render outputs and encoded/decode measurements complete; visual strengths/defects documented; browser runtime performance unverified; no production integration, commit, push or deployment performed by this experiment.
