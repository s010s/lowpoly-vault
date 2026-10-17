# r17 local representation study — direction review pending

This is a bounded local study, not a whole-tree r17 candidate and not a visual approval. No foliage was spread back over the full tree. r12–r16 remain unchanged. Current candidate branch checkpoint d26c525 was already pushed before this study.

## Sources and representation

NC State Extension, *Metasequoia glyptostroboides*, Leaves/Quick ID sections, describes linear, soft, feathery needle foliage with opposed ranks: https://plants.ces.ncsu.edu/plants/metasequoia-glyptostroboides/ . The actual linked Francois Gulbert Leaves photograph was inspected from a temporary consulted-only file. It shows many narrow leaves following a curved shoot, distinct longitudinal leaf curvature and a feather-like outline, rather than eight broad ridged pieces. Photo license CC BY-NC-ND 2.0; no photo pixels, textures or geometry are included. Earle's Description supports flattened linear foliage as a modern analogue: https://www.conifers.org/cu/Metasequoia.php .

Neither source supports our enlarged dimensions, exact group counts, two-feather simplification, prehistoric species or resulting art quality. Geometry and grouping remain artistic low-poly representation choices. Source ledger: `references.json`.

## Two alternatives, same unchanged wood

A `a-ribbon`: one axis carries 12 pairs of narrow bowed strips plus a short terminal. Each side leaf uses two longitudinal panels / 4 triangles. A small flat green connecting axis uses 6 triangles. **106 foliage triangles per inherited spray**. No cap, center ridge, thick shell or eight large solid leaf groups.

B `b-feather`: one inherited spray becomes two shorter secondary feather outlines, each with eight pairs of simple straight tapered strips. Each side strip uses one quad / 2 triangles; two curved connecting axes plus inherited axis use 18 triangles. **82 foliage triangles per inherited spray**. It spends fewer faces on surface bend and more on two feather axes; the individual strip pieces visibly meet the axis but are not a watertight or connected solid shell.

Both use opaque double-sided open leaf surfaces, zero textures, no shell thickness and no per-face palette noise. Deliberately open surfaces and smooth shared leaf normals produce source warnings; these are representation limitations, not suppressed errors. Double-sided rendering has runtime costs which were not measured here.

Wood comes directly from immutable r12 blend, not a newly generated trunk. The unit is the existing tier5-bough1 and its four inherited spray axes. The upper section includes the existing tier5/tier6 boughs, the original trunk rings from approximately z=5 m upward, and seven existing leader sprays: 35 inherited spray axes total. Original wood coordinates and face-index mappings are retained in `build-attempt-01/study-measurements.json`. Source vertices are checked exactly against the loaded excerpt. No ground normalization, new woody axes, trunk cap, or displaced wood is used.

## Measured costs

| Local sample | Foliage triangles | Wood triangles | Total triangles | GLB bytes | Used materials/primitives |
| --- | ---: | ---: | ---: | ---: | --- |
| A one bough unit | 424 | 92 | 516 | 24,916 | 2 / 2 |
| B one bough unit | 328 | 92 | 420 | 23,764 | 2 / 2 |
| A upper section | 3,710 | 732 | 4,442 | 196,296 | 3 / 3 |
| B upper section | 2,870 | 732 | 3,602 | 186,216 | 3 / 3 |

r16 used 96 foliage triangles per inherited spray. A uses 10 more per spray (+10.4%); B uses 14 fewer (-14.6%). These are measured local costs; no whole-tree export, performance extrapolation or acceptance claim is made.

## Review actual pixels

- `comparisons/unit-detailclay512.png`: same gray closeup, A and B at original512 cells. Also inspect `unit-clay512.png` for unclipped local context.
- `comparisons/unit-top512.png`: same top view; helps distinguish the feather silhouette from a solid blade.
- `comparisons/upper-horizontal128-native.png`: A/B rows, front/rear/left/right, each cell exactly128px without enlargement.
- `comparisons/upper-clay512.png`: upper-section gray context.

A and B use identical shared camera/light/color settings and union-bounds framing for each sample scope. All raw PNGs and exact-GLB manifests are under `evidence/`. Twenty-two raw PNGs total; no full turntable or whole-tree QA.

## Maker observations and stop point

The A top view shows a recognizably feather-like sequence rather than broad diamond groups. The close gray view is still directional, and several edge-on leaf strips disappear. B looks more skeletal; two thin feather arrays do not create an opaque mid-scale crown mass. **Both upper-section horizontal128 sets remain overly sparse, with dominant woody crossbars and weak leafy crown volume.** The upper-leader strips are also too fine to establish the desired upper crown in those images.

These are observed shortcomings, not independent verdicts. Neither alternative is being promoted to the full tree. Independent direction review should judge whether A's local needle outline is a useful building block, and whether an explicitly aggregated continuous feather mass is needed for128px. Do not tune the full tree's widths, tips, roll angles or random seed based on these images. Await the parent's representation-scale decision or independent direction pass before further geometry work.

Build-time source/static checks only. No official full validator, independent art/factual acceptance, browser/GPU or scene/performance work was run. All locally started Blender jobs returned normally and logs end in Blender quit; no duplicate worker was launched.

Original code MIT; geometry, blend, renders and documentation CC-BY-4.0, Leon Made This / s010s.
