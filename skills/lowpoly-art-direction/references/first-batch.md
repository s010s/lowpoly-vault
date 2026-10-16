# First-Batch Art Standards

This is an independent stylized asset pack, reviewed in a shared gallery. The existing museum's realistic distant scenery, PBR terrain, and real-world-coordinate vegetation are outside the modification scope. This pack does not claim to replace those assets directly.

The project selected ten categories: rock cliff (岩崖), stone arch (石拱), conifer (针叶树), cycad (苏铁), fern cluster (蕨丛), horsetail stand (木贼群落), uprooted fallen log (连根倒木), egg nest (卵窝), three-toed footprint slab (三趾足迹泥板), and Lepidodendron form (鳞木). These are library categories, not a claim that all coexisted in one ecosystem, place, or period. Verify scientific labels through dedicated research.

## Fixed original palette

Create the materials or palette texture yourself; do not download tutorial resources. Typically use 2–5 structurally meaningful color groups per asset, without treating that number as a hard limit. Assign colors by part, layer, or material, never randomly per face.

| ID | sRGB HEX | Structural use |
|---|---|---|
| fern_deep | #294C43 | Inner leaf groups and limited dark areas |
| fern_mid | #47745C | Main foliage |
| fern_light | #719366 | Outer or young leaf groups |
| dry_olive | #A1A276 | Limited dry leaves or transitions |
| bark_deep | #4F443D | Small internal cracks |
| bark_mid | #79624B | Main trunks and roots |
| cut_wood | #B59B72 | Broken ends and exposed wood |
| earth | #8A715B | Soil, nests, and mud slabs |
| warm_stone | #A89578 | Main rock strata |
| stone_light | #C7B798 | Light strata and initial eggshell color |
| cool_stone | #6B7774 | Cooler stone |
| water_deep | #386B73 | Reserved for future water assets |
| water_shallow | #679A97 | Reserved for future shallow water |
| ochre | #BD8B4D | Very limited ochre accents |

If a color needs adjustment during development, update that named color across the batch rather than allowing per-file drift. Scientifically unknown colors must be labeled as stylized choices, not reconstruction findings.

HEX values represent sRGB. When writing to Blender API color properties whose contract is linear, convert correctly: check the actual property contract first, then compare the result with UI entry. Also inspect colors after glTF export. Do not apply a remembered conversion function when the property's color-space contract is unclear.

## Historical first-pass triangle bands and category signatures

The first modeling pass used T1: 250–700 exported triangles; T2: 700–1,400; T3: 1,400–2,600, excluding preview platforms, lights, cameras, and collision geometry. These are preserved historical starting bands for this pack, not current universal limits, target amounts to fill, or vertex budgets. Their small/medium/large labels were local shorthand, not a physical-size classification for the whole library. A useful asset may fall below or above them.

For new assets and revisions, use [asset budgeting](asset-budgeting.md) to set separate vertex, triangle, material/primitive, and population limits from actual screen coverage, viewing distance, and runtime tests. Natural, geological, modern, futuristic, fantasy, and alien assets must not inherit city-object size tiers or the first pack's triangle bands automatically. Extra geometry needs a specific visible benefit; reducing geometry must preserve the identity-bearing structure.

| Category | Historical first-pass tier | Dominant form and structural features | Avoid |
|---|---|---|---|
| Rock cliff (岩崖) | T3 | Off-center wedge, inclined strata, stepped breaks, broad quiet planes | Potato-shaped rock piles; uniformly small triangular fragments |
| Stone arch (石拱) | T2 | One heavy side and one tapering side; a large noncircular opening; a believable load-bearing crown | A torus; two posts joined by a straight bar; weightless construction |
| Conifer (针叶树) | T3 | Progressively tapered trunk, offset crown tiers, one clear crown gap | Perfect stacked cones; equal-width branches; no crown negative space |
| Cycad (苏铁) | T2 | Short thick stem, two radial crown layers at different heights, drooping outer leaves | Equal-angle fan blades; identical leaf lengths; a miniature palm |
| Fern cluster (蕨丛) | T2 | Three frond groups at different heights, clear frond curves, progressively changing leaflets | A flat comb; identical angles and spacing; a solid green sphere |
| Horsetail stand (木贼群落) | T1 | Tall, medium, and short jointed stems; hierarchical internodes and branches; dense and sparse areas | An array of equal-width straws; a uniform fence; identical spikes at every joint |
| Uprooted fallen log (连根倒木) | T2 | Curved tapering trunk, large/medium/small roots, asymmetric break, horizontal reach | Constant-width pipe; equal-length starburst roots; regular sawtooth breaks |
| Egg nest (卵窝) | T1 | Shallow earthen depression, two lowered rim areas, separate eggs in an intentional arrangement; inspect from above in gray | Assuming every prehistoric nest is a twig ring; eggs in an evenly spaced circle |
| Three-toed footprint slab (三趾足迹泥板) | T2 | Uneven slab thickness and genuine shallow depressions; verify toe shape and stride; inspect gray top-view relief | Floating black decals; cartoon arrows; unsupported species identification |
| Lepidodendron form (鳞木) | T3 | Tall trunk and crown clearly distinct from the conifer; ordered but restrained leaf scars | A retextured conifer; uniform trunk noise; leaf scars overwhelming the main form |

The original benchmark suggestion was rock cliff, conifer, and fern. Following the recorded reference study, the next quality samples are conifer and natural arch, with fern as a third sample to test fine organic rhythm. This is a revised review plan, not a claim that new versions have passed.

Before propagating their approach, freeze two or three accepted samples by file version/hash. Review matched before/after framing, neutral-gray structure, color, side/reverse views, and actual target-viewer output. Confirm convincing secondary structure and proportions, not just category recognition or a count below a cap. Record the visual decision and runtime profile. Continue the wider batch only after this standard is actually met; use the same facet logic, palette, materials, and diagnostic lighting within the pack.

## Fixed preview setup

The primary preview tests asset readability; it is not a mixed-period paleoenvironment reconstruction.

- **Background:** Light warm gray #E8E4DC. A matching ground plane may show contact shadows. Save transparent thumbnails separately if useful.
- **Color management:** For this batch's Blender inspection images, use Standard, Exposure 0, Gamma 1, and no additional Look or curves. Record the actual version and enum values. If the project has chosen another transform, update the entire batch once rather than mixing transforms.
- **Lighting:** A neutral soft key approximately 45° front-left of the camera and 50° above the ground, with weak neutral fill. Start around a 3:1 key-to-fill ratio. Reuse the same rig, scaling light distance and size consistently relative to object bounds and maintaining one exposure baseline. Do not create special effects for individual assets.
- **Camera:** Orthographic three-quarter inspection view, approximately 35° azimuth and 25° elevation. The object occupies about 80% of the frame, with space for contact shadow. Avoid ultrawide distortion.
- **Outputs:** At least 1024×1024 primary and opposite-side views; also a 128×128 pure black, shadow-free silhouette, a neutral-gray material view, and final triangulated wireframe. Egg nests, footprint slabs, and fern clusters require top views.
- **Trace-asset exception:** For nests and footprint slabs, the silhouette only documents outer mass and proportions. Identify them from neutral-gray top views, cavity depth, rim shape, egg placement, and footprint relief. Do not require the outer silhouette alone to identify a nest or footprint, and do not distort the slab outline merely to pass that test.
- **Materials:** Default to opaque, nonmetallic, relatively rough surfaces; use roughness 0.85 as the shared starting point. Allow justified differences between foliage and rock. Do not use strong specular, emission, or transparency to simulate finish quality.
- **Inspection effects:** No depth of field, dense fog, colored rim lights, strong AO, outlines, or particles. These may appear in separate presentation images but cannot replace inspection views.
- **Gallery:** Use consistent neutral environmental lighting and a rotatable view. Pixel matching with Blender is unnecessary, but verify that there are no missing faces, distorted normals, missing materials, or obvious color shifts.
- **Batch comparisons:** Produce both normalized individual framing and a true-relative-scale contact sheet. Normalized thumbnails do not establish consistent physical scale.

Exact light wattage is not a universal cross-renderer constant. Direction, softness, exposure, and consistency are the comparison criteria. Record the final rig and reuse it for subsequent assets.

## Procedural assistance boundaries

Procedural creation is allowed for original geometry, but parameters must express design: bedding angle, center-of-gravity offset, crown openings, frond curvature, main-root direction, fracture placement, and arch-opening shape. Use fixed random seeds for reproducibility; reserve randomness for controlled secondary variation. Changing only the seed, color, or uniform scale is not a new shape design.

Each natural variant must change at least one major structural decision. Open and inspect every preview, and revise according to the visual acceptance checklist. A successful script or a file that opens is not evidence that the art passes.
