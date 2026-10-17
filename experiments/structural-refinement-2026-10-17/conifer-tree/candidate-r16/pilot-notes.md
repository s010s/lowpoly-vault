# r16 bounded intermediate review

Status: **awaiting independent direction review**. No art approval, full QA run, publication or remote push.

## What changed

Only the foliage constructor changes from r15. Same 26 woody boughs and 141 inherited spray axes. Exact wood coordinate/face/matrix equality against immutable r12 is recorded in `wood-preservation.report.json`.

Inspected NC State's actual Francois Gulbert Metasequoia foliage photograph, linked in `references.json`: https://plants.ces.ncsu.edu/plants/metasequoia-glyptostroboides/ . Its needles have long nearly parallel sides, narrow short terminals, bowed axes and local differences in inclination. The photograph remains only in temporary research storage and is not incorporated in this candidate. It does not support a species reconstruction, the enlarged grouped width, the exact fan count or seven-meter scale.

r16 replaces the double-apex diamond with a six-edge linear perimeter: broad attachment edge, nearly stable width to 60% of length, then narrowing to a short end edge instead of a mathematical point. Each group has centerline camber and a drooping terminal. Four paired ranks replace five pairs plus terminal; each rank and side receives a distinct bounded pitch, so the fan is not one rigid rolled plane. Existing surface area is redistributed into fewer longer groups; positions and woody support do not change. This is a representation change toward grouped needle surfaces, not new fine needle density.

## Budget

- r15: 16,450 triangles; 479,320 B; 11,677 source vertices; 15,718 export POSITION vertices.
- r16: **16,450 triangles; 452,244 B; 10,549 source vertices; 14,590 export POSITION vertices.**
- Difference: 0 triangles, -27,076 B (-5.65%); 3 materials / 3 primitives / 0 textures unchanged.
- Per branchlet: 11 visible groups plus keel in r15 become 8 groups, with 12 triangles each allocated to curved stable-width silhouettes rather than 8-triangle diamonds. No increase in overall foliage triangles. New triangle guard is 16,450 rather than inherited 19,000. Physical shallow section is 7% of group width, not thick round volume.

## Only these intermediate views

- `evidence/four-hero512/hero035.png`, `hero125.png`, `hero215.png`, `hero305.png`: azimuth 35/125/215/305 degrees, elevation20, 512px.
- `evidence/detailclay512/detailclay.png`: identical previous detail framing, 512px neutral gray.
- `evidence/directions128/{hero,reversehero,front,rear,left,right}.png`: six original128px images.
- `four-hero512-sheet.png` and `directions128-sheet.png` are navigation aids; original PNGs stay separate. The128 sheet does not enlarge its cells.

`pilot-handoff.json` binds exact GLB/source/config and the 11 PNG hashes. Matching r15 reference pixels already exist under `candidate-r15/evidence/`; they have not been overwritten. No full24-angle turntable or119-file acceptance freeze was run. Build-time source/static checks pass with the existing intentional-smoothing warning, but that is not official full validation or art approval.

## Issues to judge before further work

Maker inspected four-hero sheet, the detail gray pixels and native128 front, without making an acceptance decision. Several grouped surfaces can still look broad, hard or pointed; upper crown remains open. Determine whether the local curvature, silhouette and cardinal coverage now establish the requested needle-spray reading. If the direction still fails, discuss representation scale with the parent instead of authorizing another blind parameter loop.

Original code MIT; geometry, blend, renders and documentation CC-BY-4.0, Leon Made This / s010s. All earlier candidates and the independent r15 report remain unchanged.
