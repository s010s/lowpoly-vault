# r20 A delivery candidate — NORMAL16, independent/GPU gates pending

Exact GLB: `conifer-tree.glb`, SHA-256 **c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40**.

**19,052 triangles /29,882 POSITION vertices /715,500 B /3 materials and primitives /zero textures.** No A shape, fine needle, attachment, main wood, texture, material or scene-transform redesign. Only NORMAL storage uses normalized signed SHORT,8-byte stride, with required KHR_mesh_quantization. This saves119,340 B /14.29% compared with r19. The default pinned Three.js0.180.0 loader handles the extension/normalized attributes with no external decoder.

## Preserve r19 and distinguish precision from mathematical losslessness

The original r19 candidate, sources,16 pilot images and its freeze remain unchanged. Parent communicated that independent r19 A art direction passed. That result covers the user's separated, narrow, feathery, airy style; it does not silently approve r20's new normal storage or the final full-angle/runtime gates.

r20 positions, indices and triangle order, material dictionaries and all node/scene transforms compare **exactly** against r19. Source `.blend` retains the full-precision editable geometry. `geometry-equivalence.report.json` records actual comparisons. Rebuilding the frozen geometry constructor produces a canonical float GLB **byte-identical to r19** before storage conversion. That canonical file remains in the independent rebuild evidence.

Normal precision is explicitly lossy: max angular error0.001443°, mean0.000661°, p990.001227°; max decoded unit-length error0.00002421. Shader normalization remains expected. No16-bit position quantization,8-bit normal conversion, vertex welding, decimation, normal removal, material merging, Draco or Meshopt was used. It is not correct to call the complete file mathematically lossless.

## Actual pixel comparisons

`comparisons/r19-r20-hero035.png` and `r19-r20-detailclay.png` show unmodified original512px side-by-side cells; no paint-over. `pixel-comparison.report.json` measures all16 original r19 matched pilot images against the new exact GLB, preserving both PNG hashes per row.

- Native128px black silhouette: **exactly identical pixels**, zero difference.
- Four512px hero views:162–206 changed pixels each /262,144 (0.0618–0.0786%), maximum isolated8-bit channel difference3.
- Color detail:1,125 changed pixels (0.4292%); mean channel difference0.003512/255, max6.
- Gray detail:1,177 changed pixels (0.4490%); mean channel difference0.005535/255, RMSE0.09514/255, max9.
- Other128px color views:5–12 changed pixels per16,384, max channel error2–5.

The maker inspected the comparison pixels and sees the same A form; this does **not** substitute for independent perceptual approval. The images are not all pixel-identical. Differences and precision limits are disclosed rather than rounded away. These are CPU Cycles actual GLB reimports, not GPU timing results.

## Full-angle and technical evidence

`evidence/full-angle256/` contains37 current raw images:24 azimuths at15° intervals, hero/opposite, all six orthogonal directions, clay/alternate key, wire, detail and gray detail. `comparisons/full-angle256-contact-sheet.png` is navigation only. Required directions and24-angle coverage are inside this single manifest; raw frames remain individually hash-bound.

`evidence/detail512/` adds seven four-hero/color/clay detail images. `evidence/native128/` adds nine four-hero/cardinal/silhouette images. **53 current frozen raw images total**, plus the earlier four-frame precision probe retained separately. All use the historical fixed framing, light/color setup and meter-space geometry. No full-tree shape iteration was done after A direction acceptance.

- Official Khronos validator: **0 errors /0 warnings**.
- Static audit: pass with original intentional double-sided-leaf warnings.
- Saved source/export counts and bounds: pass with documented thin-leaf/smoothing warnings.
- Independent bounded local geometry+NORMAL16 rebuild: **byte-identical final GLB**, semantic digest identical. Its canonical float GLB is byte-identical to r19.
- Three.js0.180.0 actual Node GLTFLoader parse: pass; all three NORMAL streams are normalized Int16Array, position/bounds/counts match. **This is not an actual WebGL render.**
- Candidate record integrity: valid; **approved_for_brief=false**. Technical and parser stages pass; current independent visual/factual/specification and actual GPU/scene stages remain open.

All Blender jobs use one local worker, two threads and180-second timeout, with normal exit. Bounded macOS request/result records are preserved; no Linux affinity/cgroup or GPU capability is invented. No headless Chrome, user Chrome/Safari, software install or system-setting change was used.

## Cost analysis

The full read-only breakdown is in sibling `cost-analysis-r19/README.md` and its raw JSON. r19's byte growth is mostly separate leaf endpoints: r12 foliage9,024 vertices /15,792 triangles versus r19 foliage23,542 vertices /15,794 triangles. There is **zero exact redundant full vertex, zero unused vertex and zero unused BIN bytes** to remove. Export normal-split growth explains only3.4% of the byte increase; authored vertex attributes explain96.1%. All files already have only POSITION/NORMAL and UINT16 indices.

Raw r19 storage: POSITION358,584 B, NORMAL358,584 B, indices114,312 B, JSON/container3,360 B. r20 retains the same POSITION/index bytes and reduces NORMAL to239,056 B; schema/alignment overhead yields715,500 B total. Names and license extras were retained; their total removal would save only752 B.

Measured transfer/archive sizes: r19 gzip9=521,340 B /Brotli11=429,349 B; r20 gzip9=455,213 B /Brotli11=376,956 B, each byte-identical after decompression. Those are **not raw GLB bytes, GPU memory or measured frame times**. Hosting compression is an integration concern and was not modified here.

Format/alignment primary source: https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_mesh_quantization . Required extension support and exact attribute types were also observed in the pinned local loader/parser. No new external decoder dependency is introduced, but target GPU behavior still must be tested.

## Next gates and exact handoff

Use `gpu-scene-handoff.json` for the exact file/hash,1/16/32 **independent clone** scene profile and required actual evidence. It intentionally contains no measured GPU/scene values. Capture actual renderer/device, visible population, resolution/DPR, camera/lights/shadows, errors, calls/triangles and warmup/sample frame timings. Report real GPU versus software fallback explicitly. Any GPU-instanced variant is a separate measured profile and cannot replace the declared clone baseline.

Parent must coordinate fresh independent current-r20 full-angle, normal-precision, factual/specification review. Full production approval remains blocked until that review and actual target GPU/composed-scene gates are satisfied. The accepted r19 A style is the judging direction; do not reject solely for natural sparsity or redesign toward the rejected B core mass.

Only after acceptance should integration use latest main and verify the same accepted GLB/source blend and24alpha previews. Existing diagnostic opaque renders are not claimed as24alpha release previews. No main, published asset, website or release manifest was changed.

## Rebuild

The bounded run is `run_local_build.py` with `rebuild-jobs.json`. The generator is `build_delivery.py`, which runs the copied frozen `build_airy_conifer.py`, then `pack_normal16.py`. Adjacent `woody-source.json` and `build-config.json` are required inputs, as are repository `scripts/asset_common.py` and `qa_glb.py`. The job records hash all of these. Each fresh run must use an empty output directory; never overwrite a frozen candidate.

Code MIT; original geometry, blend, renders and documentation CC-BY-4.0, Leon Made This /s010s. References remain consulted-only; no external image, model or texture is incorporated.
