Self-contained generation and review tools

Generation: Blender 4.3.2 with bundled Khronos glTF Blender I/O 4.3.47.
From any empty working directory:
blender -b -t 2 --python-exit-code 1 --python /path/to/source/generate.py -- --output-dir /path/to/new/output
The generator reads only adjacent params.json and Python helpers vendored here. Reference images are not inputs. No network access is used.

asset_common.py, qa_glb.py, render_candidate_views.py and validate_gltf.cjs are unmodified canonical lowpoly-vault helper snapshots, individually SHA-256 pinned in dependencies.json. MIT license, Leon Made This / s010s. Other helpers are original adapters for this candidate, also MIT.

render_views.py imports the exact supplied GLB into a clean Blender scene. Four-view example:
blender -b -t 2 --python-exit-code 1 --python /path/to/source/deps/render_views.py -- /path/to/model.glb --output-dir /path/to/empty/render-output --revision r001 --resolution 768 --samples 64 --turntable-frames 0 --views front,side,top,perspective
Use the project resource limiter before all Blender invocations. Camera perspective points along (+X,-Y,+Z); no auto-turntable.

inspect_source.py: Blender read-only blend topology/identity/BVH check. Arguments after -- are model.blend and report.json.
validate_gltf.cjs: Node >=20 plus installed official gltf-validator 2.0.0-dev.3.10. Pass exact GLB path; writes reports beside it, so use an isolated test copy. No external resources fetched.
parse_glb.mjs: Node >=20 plus installed Three.js 0.180.0. Arguments: exact GLB, report output, installed three package directory. Parse-only, not GPU.

Source generation does not require Node packages, photos, another model directory, or any absolute path from the author's workspace. Review tools declare their independent runtime packages; those packages are not embedded in the model.
