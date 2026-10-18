# Narrow runtime verification addendum

2026-10-18 UTC. Cloud only; no Mac access, geometry changes, merge or security-setting changes.

## Result

Three.js 0.180.0 Node GLTFLoader parsing: PASS for all four exact GLBs. Counts and bounds match the independent static audit. Zero animations, as expected. Exact hashes and measurements are in `node-parse.json`; executable reproduction is `parse.mjs` with pinned `package-lock.json`.

- Juracimbrophlebia: b6fa8ebf0995614401b27cafea2e5095f6f48bbdcb69fd99957cacd60272fa94; 2,128 triangles / 5 meshes.
- Asteroxylon: 028eca80ede2eb4fc95f87c17465aee8dd3284c43d3d5633cb8343db91abcc8e; 5,744 triangles / 5 meshes.
- Bothriolepis: 311da456d83b2bb722f654769ce4a937393d7f771e5ae71185eb7db473a14f98; 736 triangles / 8 meshes.
- Waptia: 300e2ef721c7822cc717f808941bc19cb2ff00b8ef4b147a0c634e6b6683033b; 1,452 triangles / 7 meshes.

This supersedes the original review's unknown insect/plant Node parsing status. It does not supersede its GPU/scene limitations.

## Actual browser rendering: BLOCKED BY CLOUD EXECUTION ACCESS

A narrow browser harness was prepared in `index.html`: one canvas, all four GLBs, orbit control, three four-asset switch/dispose cycles, and twelve mixed duplicated props. It was NOT executed successfully; its planned checks must not be described as passed.

Observed attempts:
1. Cloud Chromium launch through Playwright with Chromium sandbox enabled exited before a page loaded: `socket() failed: Operation not permitted (1)`; accompanying crashpad startup error reported `--database is required`.
2. Existing supported cloud browser inventory confirmed an active Chromium browser. Opening `http://localhost:8767/` through its supported CUA tab API failed with `net::ERR_CONNECTION_REFUSED`. The local server command remained running, but a separate shell localhost probe also could not reach it.
3. The permitted escalated cloud-server route failed before starting: `bwrap: Can't create file /home/agent/.codex/sessions: Read-only file system`. No access to that denied path was attempted, and no filesystem/security change was made to bypass the error.

Stopping condition: verified cloud browser/executor access blocker. Actual WebGL/GPU rendering, browser orbit, repeated switch/disposal behavior and the duplicated scene remain UNTESTED. This is not an asset failure. Use an already authorized browser-reachable cloud executor to run the supplied narrow harness later; no broader benchmark or model revision is indicated.
