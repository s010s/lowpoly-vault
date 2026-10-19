# Commands and environment

Reviewed from the cloud workspace `/workspace/lowpoly-vault`. No user computer was used. The repository was checked out at the frozen candidate and work was kept on `qa/independent-concept-small-fish-20261019`.

## Baseline and policies

```sh
git fetch --no-tags origin main 3196c36c51d5a14487dcd4ebbebcafc00aa933d7
git merge-base --is-ancestor origin/main 3196c36c51d5a14487dcd4ebbebcafc00aa933d7
git show -s --format='%H%n%P%n%an <%ae>%n%s' 3196c36c51d5a14487dcd4ebbebcafc00aa933d7
rg --files -g 'AGENTS.md' .
```

The candidate is a descendant of main `bac6621fc39144b3759c53b1b27231ac1b6e21c6`. The `AGENTS.md` search returned no files. Relevant checked-in guidance reviewed: `skills/concept-guided-lowpoly/SKILL.md` and `references/workflow.md`; `skills/lowpoly-art-direction/SKILL.md` and `references/visual-acceptance.md`; `skills/asset-factual-review/SKILL.md`; `skills/blender-lowpoly-pipeline/SKILL.md`, `references/standardized-pipeline.md`, `references/production-contract.md`, and `references/qa-design.md`.

## Independent checks run

- Opened original concept and every exact-GLB proof frame in the viewer, not just the overview sheet.
- Ran `evidence/verify_artifact_bindings.py`: checked candidate-sidecar source hashes and both render manifests per asset, then independently checked all frame hashes, byte lengths, and PNG dimensions.
- Ran `evidence/blender_reimport.py` with Blender 4.3.2: opened each `.blend`, independently imported each `.glb` into a clean scene, and compared evaluated triangle counts, dimensions, used material names, linear base colors, roughness, and metallic factors. Output: `evidence/blender-reimport.json`.
- Ran `evidence/threejs_node_load.mjs` with locked Three.js 0.180.0 `GLTFLoader`. Output: `evidence/threejs-node-loader.json`.
- Ran `evidence/validate_gltf.mjs` with locked Khronos glTF Validator 2.0.0-dev.3.10. Full reports: `evidence/khronos/`.
- Ran `evidence/measure_pteraspis_tail.py` on a clean GLB import to measure the stated lower-lobe-led tail cue. Output: `evidence/pteraspis-tail-measurement.json`.
- Served the repository locally using `python3 -m http.server 8765 --bind 127.0.0.1`, then ran `evidence/run_runtime.mjs`. Its page loads the four exact GLBs through Three.js 0.180.0 in Chromium WebGL2 and renders one copy of each in a single lighted scene. Output and image: `evidence/threejs-webgl-result.json` and `evidence/threejs-webgl-scene.png`.

The browser backend was ANGLE SwiftShader software WebGL. No hardware GPU or 8/32-copy population test was run. Node was v24.19.0. `npm ci --ignore-scripts --no-audit --no-fund` installed dependencies from the existing lockfile into ignored `node_modules`; no tracked package files were changed. GitHub CI was not rerun.
