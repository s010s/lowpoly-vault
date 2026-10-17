# Sharp transparent image-only previews

The initial ten original assets each have 24 derived WebP angles and a static poster. Original GLB, Blend and downloadable bundle bytes remain unchanged. This presentation work does not approve their artistic or scientific quality.

## Rendering contract

The actual Three.js ModelStage renders both the detail viewer and offline website images. The pinned shared preset fixes camera angle, centered-square perspective fitting, target, normalization, lighting, ACES tone mapping, sRGB color and exposure. Website frames are 768 × 768 WebP at quality 0.90 with transparent surrounding pixels. Their versioned paths include the preset version, size and quality to avoid an old cached opaque frame being mixed into the new presentation.

The UI paints the neutral stage background. Only model pixels travel from card to detail and back. WebGL clear alpha, copied snapshots, handoff overlays and animated flights all preserve transparency. Light and dark UI themes share model lighting. Blender diagnostic renders remain separate quality evidence.

## Interaction and resource bounds

- Only the current hovered, keyboard-selected or horizontally dragged card fetches its manifest and current/neighbor images. The catalog does not fetch GLBs or import the Three.js viewer.
- Desktop movement is relative to the entry position; there is no automatic rotation. Keyboard arrows, Home/End and Escape remain available with reduced motion.
- Horizontal touch dragging scrubs the selected card. Vertical movement keeps native scrolling and an ordinary tap opens detail.
- Three retained decoded 768px RGBA bitmaps occupy 7,077,888 bytes. The one 768px canvas adds 2,359,296 bytes, for 9 MiB of controlled objects. This excludes browser internals, transient decode copies, encoded objects and a retained return snapshot; it is not a physical-device process-memory measurement.
- The encoded LRU holds at most 12 frames or 2 MiB; the manifest LRU holds three entries. One request is active at a time. Superseded requests abort, stale decoded bitmaps close, and intermediate pointer positions coalesce.
- Leaving, hiding, scrolling away or entering detail releases active decoded frames. A failed image restores its static poster without silently loading 3D.

Opening detail copies the actually painted card image and its camera azimuth/elevation. The original GLB loads automatically at that view. Closing retains the current rendered snapshot, including free-orbit elevation and zoom, so immediate reopening preserves the inspected view. Next/previous selection retains the prior painted view until the replacement renders. Only one live GLB scene exists.

Viewer controls and hint text reserve their layout space before loading completes. Ready/error state changes visibility and disabled state without changing canvas-host height. The static poster is hidden beneath a ready transparent canvas and made available again on context loss or load failure.

## Verification

The release checks validate source hashes, all allowed paths, metadata, dimensions and immutable originals, then reproduce all 250 WebP files from the pinned actual viewer. Browser tests cover each of the ten image-only cards independently, active-only requests, bounded objects, mobile drag/scroll/tap, delayed and superseded loading, direct URLs, theme changes and reduced motion. Detail tests inspect rendered-alpha bounds and the handoff release boundary rather than treating a nonempty DOM canvas as visual correctness.

Chromium CI uses SwiftShader and emulated viewport/device-scale settings. Its screenshots, videos and measurements do not certify physical-GPU identity or real-phone performance. Final deployment requires the exact integrated candidate to pass release CI and its visual evidence to be reviewed.
