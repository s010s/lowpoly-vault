# r18 — one bounded upper-crown arrangement

State: **direction review pending; maker observes that the horizontal128 crown remains too skeletal**. No art approval, whole-tree integration or full QA. This is the only arrangement trial in this checkpoint. Original r17 A/B and all earlier candidates remain unchanged.

## Fixed and permitted changes

The original r17 `ribbon_fan` constructor is imported unchanged. A leaf count, width/length ratio, camber, terminal shape, topology, smoothing and palette were not retuned. Constructor hash: `b88dfe9f8f0e1538ef1c6964f1df501b4de743cb12f7b11820ff327b6dddfb40`.

The same r12 main wood excerpt retains its exact 386 vertex coordinates and original face prefix, 732 triangles. Only subordinate spray attachment points, axis lengths, pitch and path change. New fine support twigs are appended separately within the combined wood mesh; main branches are neither moved nor shortened.

Thirty-five existing sprays were reorganized as paired local clusters. Lower bough clusters pair oblique-upward and drooping carriers to bridge vertical tier gaps. The three shorter upper boughs receive six extra sprays; two extra leader sprays reinforce the tip. Total **43 sprays, exactly8 added**. No new full-tree model exists.

## Measured bounded-trial cost

- Existing A foliage: 35 ×106 =3,710 triangles.
- Eight added A sprays: **848 triangles**, exact authorized leaf increment.
- Total foliage:4,558 triangles.
- Original main wood:732 triangles.
- Fine support:43 ×8 =344 triangles, separately accounted.
- Total: **5,634 triangles;252,428 GLB bytes;3 used materials /3 primitives;zero textures**.
- Exact GLB SHA-256:`4c2ce23957beb0811f2dd54e6902597e0267687ebf261b94e0052fc8e337fd0a`.

`build-attempt-01/layout-measurements.json` records every attachment, direction, length, cluster and added-spray flag. `layout-config.json` freezes this layout; no random-search or second seed was used.

## Exact requested evidence

Only seven current-trial raw images were produced:

- `evidence/horizontal128/{front,rear,left,right}.png`: original128px horizontal cardinal images.
- `evidence/hero-detail512/{hero,reversehero,detailclay}.png`: two opposite hero images and local gray detail,512px.
- `comparisons/r17-r18-horizontal128-native.png`: original-size128px before/after cells, no enlargement.
- `comparisons/hero-and-reverse512.png`: navigation sheet.

Camera, light, exposure and framing are the same as the r17 upper-section comparison. Hash-bound manifests retain actual source GLB and camera details. Per-job two Blender threads and180-second timeout; sequential workers, all jobs exited normally. Build-time source/static checks only. No official validator, full turntable, GPU or scene work was run.

## Observed limit and conditional style choices

The new arrangement makes oblique sprays and inter-tier continuity more visible, especially in512px, and avoids the old thin-horizontal-layer pattern in several spots. **At horizontal128px the upper crown still reads predominantly as fine linework around exposed wood.** The maker does not claim the requested clustered-crown result. No further parameter or needle-detail iteration was performed.

As requested for that outcome, two clear same-camera style choices are prepared in `comparisons/user-style-options-{512,128}.png`:

**A — separated, airy feather needles.** The actual frozen r18 QA model,5,634 triangles. It prioritizes visible individual-like narrow strands and open sky; it currently lacks the desired thumbnail crown mass.

**B — connected feather-group core with the same fine A fringe.** A separately saved **unapproved style proposal**, not a second arrangement trial and not a substitute for passing QA. It adds one shallow, flat, opaque core band beneath each existing A spray, retaining all original A vertices, main wood and all43 placements. The core trades separate internal gaps for a continuous mid-scale feather silhouette. It adds602 triangles: **6,236 total;272,556 bytes;3 materials/primitives;zero textures**. This additional core cost is outside the bounded r18 leaf increment and is disclosed as a future style proposal, not silently charged to the authorized848-triangle addition. This abstraction may read more broadly as fronds; conifer identity and preferred style still need user judgment.

Only a same-camera hero and native128 front preview were rendered for B. Source and measured cost are under `style-proposal-b/`. It has not received independent direction approval, validation or production acceptance. No imagegen, texture paint-over or image beautification was used; both choices are original Blender geometry renders.

The next action is a representation-style decision and the parent's independent direction review. Do not tune another whole-crown width/tip/roll/seed, and do not spread either style over the whole tree until a direction is explicitly chosen and passes the required review.

## Reference and claim boundary

Modern linear, opposed, feather-like needle ranks remain the consulted analogy: NC State Extension, Leaves/Quick ID and Francois Gulbert foliage photograph, https://plants.ces.ncsu.edu/plants/metasequoia-glyptostroboides/ ; Earle Description, https://www.conifers.org/cu/Metasequoia.php . No third-party imagery or geometry is included. Exact grouping, cluster layout, density, scale and the connected B core are artistic choices, not claims of measured botanical anatomy or extinct-species reconstruction. The inherited source ledger is `references.json`.

Code MIT. Original geometry, blend, renders and documentation CC-BY-4.0, Leon Made This /s010s.
