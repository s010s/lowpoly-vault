# Animation review

Reviewed implementation commit `ebce4e7` against the pinned official `review-animations/SKILL.md` and `STANDARDS.md`. User instructions take priority for instant reduced motion and preserving the existing model-continuity subsystem.

## Findings table

| Before | After | Why |
| --- | --- | --- |
| `site/motion.js` list entry 460ms + up to 240ms delay, 100ms awaited exit, 280ms FLIP | `site/main.js:121`–129 replaces results as soon as the current search resolves; no list animation owner/observer or busy dimming | Repeated search and reading surfaces fail the frequency/function gates; deleting choreography is preferable to retuning it. |
| Generic 180ms post-click scale ran for keyboard and pointer | `site/motion.js:12`–18 distinguishes actual primary pointer presses; `site/style.css:106`–108 uses interruptible scale(.97), 160ms press / 100ms release, and removes CSS keyboard :active movement | One feedback response, no duplicate bounce after click, no generic keyboard motion. Pointercancel, blur and page visibility clean up ownership. |
| Hover selectors were unconditional | All existing :hover selectors in style.css and atlas.css now sit in `(hover:hover) and (pointer:fine)` at their original cascade position | Prevents touch from activating hover motion; preserves focus-visible and selected states, plus the intentional static mobile affordance. |
| Refine native details snapped visibly | `site/style.css:115`–126: 160ms opacity + translateY(-4px)/scale(.97), top-right origin aligned with trigger; content-visibility is a discrete lifecycle switch | Spatial connection with bounded compositor properties; native keyboard/focus semantics remain immediate. Mutation observer makes closed controls inert immediately. Unsupported browsers use native instant fallback. Rapid close/reopen retargets current CSS values. |
| Clipboard success only replaced button text | `site/motion.js:46`–61 and `site/main.js:186`: check appears only after confirmed clipboard write; 160ms transition, stable minimum width, immediate localized text/live announcement | Confirms success without a toast, delay, or repeated remount; failure removes the success indication and exposes selectable source text. |
| Old shell and provenance entrances replayed decoration | Removed, along with dead GalleryMotion methods and legacy card-ready fade | Content should be readable and focusable immediately. Shared model reveal owns model coverage already. |

## Verdict

**Accessibility:** scoped keyboard feedback and new details/copy transitions are instant; reduced motion is instant by explicit user requirement, overriding the reference default of retained fades. Native focus, Tab, Escape and immediate inert semantics passed actual Chromium tests. Coarse-pointer static affordances are retained.

**Interruptibility & timing:** new motion uses CSS transitions, 160ms strong ease-out from the existing `--ease` token updated to the official `(0.23,1,0.32,1)` value. No new RAF loop, dependency or library. A one-time layout/style read for clipboard confirmation is not an animated layout property. Refine uses a discrete content-visibility switch to retain native exit painting. No animated height/width, scale(0), ease-in or transition:all was added.

**Origin & cohesion:** Refine grows from the actual trigger side. Clipboard check is intentionally small. Screenshot inspection of light/desktop, dark/Chinese and mobile surfaces found no overlap or overflow. Related-model links remain stable; no new related animation was justified. Existing 140ms hover reveal, modal/return flights and all real GLB/poster ownership are unchanged. No second renderer or sequence assets were introduced.

**Approve the scoped animation diff.** This is a self-review, not independent or physical-device acceptance. The original shared-model native-touch zoom test remains a documented failure on both base and changed builds; a separate 400ms gesture-settling diagnostic passes without changing product code or weakening the original assertion. Overall test status is therefore not an unconditional all-pass.
