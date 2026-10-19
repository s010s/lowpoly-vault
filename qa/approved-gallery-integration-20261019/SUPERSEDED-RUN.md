# Superseded preliminary run

Source: `598958244db0cd76a8dae137dad6448e16a73d6c`.

The cloud environment remained available. Build passed; main gallery browser suite completed 24/25 cases, with zero runtime errors. The native wheel test failed at `site/gallery-browser-test.mjs:228` because its wait condition already held at the initial nonzero scroll position. Five independent runs recorded initial scroll 19968, the same position immediately after the original wait, a moved position around 20865 after 250 ms, and settled position 20864. This distinguishes an early assertion from broken scrolling.

The scrub wrapper reproduced that same failure; shared and handoff wrappers passed. The runner was stopped during the hover wrapper when the parent supplied a new exact final SHA. Unfinished jobs are not claimed as passed. Additional screenshot capture completed 54 frames and records actual observed times in `visual/sequence.json`; individual screenshot overhead missed much of the cold reference animation, so final visual acceptance adds actual CDP compositor screencast frames.

All final-target evidence is separate under `final-1e8b5cb4/`. This preliminary evidence is not final-target acceptance.
