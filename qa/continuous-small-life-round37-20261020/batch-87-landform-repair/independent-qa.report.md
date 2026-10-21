# Batch87 landform repair: fresh independent difference QA

## Decision

Both new repairs pass technical, visual, factual, specification and runtime_parse within the declared static scope. GPU and composed-scene remain BLOCKED / not run. This is not full, formal, user, live-site or release approval, and no counter is incremented.

Fixed source commit: `178664a29c9bf5a751ccb3833e749e539d1b3745`.

- Spatter-cone r006: GLB `51b4daefbebba036ba57c76b932f2d18b265349c84d047261dbfbd1c223936a7`.
- Travertine-terrace-pools r003: GLB `f0b8e2558e44250555c7205858f602e1bcab8ba33f2b2f1a8fb0934b3227c432`.

## What changed and what was measured

Spatter now measures 7.80000019 × 7.40000010 × 2.79999995 m. Actual crest mean is 2.5 m, maximum 2.79999995 m, mean opening radius 0.649999999 m, and planar floor 0.180000007 m. The crest is independently recovered from final GLB ray maxima, not only source labels. Original construction has 64 rays, 14 intervals / 15 stations and 9 staggered two-layer relief groups; 8 exterior midpoint refinements make 23 final rings. The nominal 3.7 m construction foot radius is not claimed as final maximum: that is 4.439519 m. This distinction was prospectively clarified, not silently rewritten.

The r005 smooth-funnel/radial-banding diagnostic failure remains. In r006, clay and opposite views show broad asymmetric cohesive welts and a clear narrow opening. Some radial faceting and coarse palette flecks remain as stylization; no new universal no-repetition criterion was invented.

Travertine now measures 10 × 18 × 4.69999981 m. Five actual floors retain four 0.7 m rises. The declared primary lip contribution is 0.18 m after separately accounting for overflow saddles and side-edge relief; actual total sampled rim relief spans 0.030289–0.414496 m, not uniformly 0.18 m. An independent old/new source comparison confirms all 754 top vertices shift approximately +0.635504 m while all 106 bottom vertices stay at zero. XY is separately corrected. This is not global Z normalization. All views were newly judged for the thicker substrate; rear and side artificial module-cut faces remain disclosed.

## Evidence

- Fresh source opening and byte-identical reexport for both assets; zero source-to-transformed-GLB coordinate error, matching authored/evaluated bounds and counts.
- Independent project checks, Khronos 0 errors / 0 warnings, and Three.js GLTFLoader revision180 parsing.
- 700 lifecycle/binding checks, 23 local dependency import edges, 218 repair raw files and 448 prior raw files rehashed with no mismatch.
- Both distinct-PID rebuilds per asset verified against request/result/execution/output bytes. Final GLB + brief + references bound before both real eight-frame512px render jobs and separate bottom jobs.
- Personally inspected all 16 mandatory individual images, 2 supplemental bottoms, 2 sheets, 2 primary photographs, 2 concepts and all retained landform diagnostic pixels. All16 sheet cells are byte-identical RGB copies of native512px frames.
- Source facts were checked against [NPS Spatter Cones](https://www.nps.gov/places/spatter-cones.htm) and the [NPS Travertine Terraces section](https://www.nps.gov/yell/learn/nature/hydrothermal-features.htm). These support generic form and process, not the authored art dimensions.

## Preserved boundaries

Original spatter r004 and travertine r002 specification BLOCKED decisions stay unchanged. Pleuromeia and glacier-crevasse-field remain REVISE and untouched. New measurement definitions were appended before recorded new builds; old definitions are not retrospectively recast. No original source, freeze, failure or QA outcome was edited.

Historical timestamps are preserved. The present host clock is about two hours ahead of the tool clock; no chronology was fabricated from file times. Historical maker records remain attestations, not independently signed inspection timestamps.

No new authored geometry, source save, external upload, push, PR, merge, deployment or formal candidate approval was performed. GPU and composed-scene need their own genuine evidence.
