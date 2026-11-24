# Mobile gallery detail: independent document flow

At the existing mobile breakpoint (760px), place navigation, title, media and tools/downloads in distinct regions. The model retains the same canonical fit-square size and its poster and GPU host share a fixed rectangle for each viewport. The desktop keeps its original layout. No model, poster, material, orientation or asset binding is modified here.

The WebGL canvas is viewport-fixed while the host is now in the document. A single passive scroll listener requests one draw per animation frame during mobile detail. In inspection mode, the media center still captures rotation; two 24px edges allow a vertical swipe to continue reading. Outside inspection, the whole media area can scroll. The responsive shell matches the startup markup structure.

## Verification

* `mobile-flow-browser.mjs` compares two loopback builds containing identical model assets. Set `QA_ORIGINAL`, `QA_CANDIDATE` and `QA_OUTPUT_DIR`. Its default cases cover a long Chinese title, wide and ordinary phones, landscape and a 1440px desktop. Use `QA_GROUP=extra` for former threshold edges, additional landscape, and simulated safe-area insets. Use `QA_GROUP=samples` for the candidate fixture matrix (Cambroraster, Cooksonia, Flint nodule, Spinolestes). Run from the repository whose manifest matches the served builds.
* The browser check gates real GLB completion, verifies downloaded assets by SHA, checks no stage movement or model scale change between poster and ready, and requires controls to be unobstructed, keyboard-ordered and reachable even when below the initial fold. Both asset downloads, keyboard attribution and entering/exiting inspection are exercised.
* `mobile-flow-swipe.mjs` uses `QA_CANDIDATE` and `QA_OUTPUT_DIR` on a loopback build containing Paratingia. It exercises real touch events, frame/hash changes on document scroll, the hidden-to-visible return, resize and reduced motion. These are Chromium simulations, not native-device/Safari results or the complete release CI.
* Trade-off: on a short screen, first view can crop the model at the viewport edge, and tools/downloads can be below the fold. Scrolling reveals the rest without changing the media fit or covering any of it with controls.
