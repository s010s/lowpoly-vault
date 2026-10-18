# Animation opportunities — 2026-10-18

Base: `77720858d73fcb8f6b8845576851762dcba078ef`, cloud Linux only.
Official workflow: emilkowalski/skills at `2d228630ba1446365f614a108cb8252f1feda202`.
Read find-animation-opportunities/SKILL.md → animate/SKILL.md + RECIPES.md → review-animations/SKILL.md + STANDARDS.md. Retained verbatim under `.agents/skills/emil-animation/` with the original MIT license. No global skill installer or added motion dependency.

## Opportunities table

| # | Location | Today | Purpose | Frequency | Suggested motion |
| --- | --- | --- | --- | --- | --- |
| 1 | site/main.js:78, site/style.css:33 | Native Refine details appears/disappears instantly | Spatial consistency / state indication | Occasional pointer action | Native details-content transition, opacity 0→1 and scale(.97)→1 from top right at trigger; 160ms strong ease-out cubic-bezier(.23,1,.32,1), symmetric path. Keyboard and reduced motion instant. Native fallback instant where unsupported. |
| 2 | site/main.js:187 | Clipboard success only replaces text | Feedback | Occasional, only after confirmed write | Stable-size inline check, opacity 0→1 and scale(.97)→1, 160ms same curve; repeat success stays settled. Text and live announcement update immediately; keyboard/reduced motion instant. |

All candidates pass frequency (occasional), purpose (above), speed (160ms), and function (no input delay, moving data, layout animation or new focus primitive). User explicitly requires instant reduced motion, overriding the reference preference for retained fades.

## Rejected candidates

- Existing 140ms hover reveal, 300ms modal open, 180ms return and interrupted-history ownership: already implemented; no missing-feature claim. Preserve one Three.js renderer and real GLBs/posters. No sequence restoration.
- Repeated listing entrance (460ms + up to 240ms stagger), 100ms awaited exits, 280ms FLIP: frequency/function fail. Remove, including offscreen and shell reveal; results should be immediately inspectable when data arrives.
- Generic 180ms click rebound: frequency/keyboard fail. Remove; one pointer-only CSS press (.97, 160ms press / 100ms release), no post-click rebound or keyboard motion.
- Related models: no new transition unless actual browser inspection shows a jarring discontinuity; preserve immediate navigation.
- Provenance disclosure: informational native details; remove decorative entrance rather than replay it for keyboard.
- Search, sorting, counters, empty state, routes and reading surfaces: frequency/function fail. No decorative entrances.

## Verdict

The gallery already spends its motion budget on model continuity. The largest improvement is removing repeated list choreography. Only Refine and confirmed clipboard feedback warrant new small transitions. This report is the read-only find-animation-opportunities output; implementation proceeds under the separately requested animate stage.
