# Preserve interrupted bird-pair outputs

This checkpoint preserves the interrupted maker's existing output bytes. No modeling, rerender or new asset-acceptance claim is made. The source-only checkpoint was 5030e53968209412ec240d70fd25bb8747261f0c; its tree contained no assets/prehistoric/birds files. The local final build_bird_pair.py and render_candidate_views.py differed from that source checkpoint, and are preserved with these outputs to retain the actual producing recipe.

Ichthyornis: 134252-byte GLB, 2432 triangles. Confuciusornis: 116860-byte GLB, 2108 triangles. Both have editable .blend sources, six 512px views, existing render manifests/configs, metadata and technical reports. A zero-frame turntable.json is renderer metadata, not a produced turntable sequence.

Current preservation checks only established file presence, GLB header length and image/GLB/config hash binding. Existing Khronos reports record zero errors/warnings, while the source QA includes intentional-opening warnings. These checks and inherited reports do not establish aesthetic, basic-form, graphics or composed-scene acceptance. Independent review and runtime work remain open. No main ref, published gallery or museum code is changed.
