# Bounded cloud Blender queue and frame evidence

`run_asset_queue.py` schedules trusted local manifests. It does not publish, modify makers' source folders, or approve an asset. It is not a sandbox for untrusted Python/Blender code. Use an isolated cloud workspace; a job script still has the caller's filesystem/network privileges. Scripts must honor `--output-dir`, declare all file dependencies, and avoid writes outside their attempt.

## Resource policy

- Defaults: **1 worker × 2 Blender threads**. Concurrency is opt-in, hard-capped at 8 workers. A request for 1,000 workers is rejected.
- Each invocation has exactly one lane: `preview`, `build`, or `render`. Keep fast visual/QA work in a preview queue, separate from expensive model generation and HD renders.
- `--cpu-budget N` declares this queue's share of a shared cloud host. `workers × threads` cannot exceed this share or the detected affinity/visible cgroup quota. Coordinate other queues and makers: separate roots do **not** provide a global resource governor. A hidden quota is reported unknown.
- Blender commands receive `--background -t N --python-exit-code 1`; the manifest must not supply those flags. BLAS/OpenMP environment thread counts are also bounded. A script can still explicitly change its own thread settings; this is a trusted-code contract, not an OS CPU quota.
- `--memory-mb N` optionally applies Linux `RLIMIT_AS` to each process and its descendants. It limits virtual address space per process, **not total tree RSS**. Default 0 disables it. Blender libraries can reserve much more address space than their resident footprint; calibrate it before using it in production. No job-specific memory support is implied beyond the CLI setting.
- A timeout applies to each attempt. SIGINT/SIGTERM stop new dispatches. Default `--on-cancel terminate` terminates active process groups; `drain` waits for active jobs (still subject to timeouts), and a second signal forces termination. Cleanup sends TERM then KILL after the grace period, including descendants left behind by a successful direct child. A child that deliberately escapes its process group is outside this trusted scheduler's containment guarantee.
- `finally` cleans active process groups on ordinary runner errors. SIGKILL, host failure, or power loss cannot run cleanup; use a container/cgroup supervisor for hard-failure guarantees. Such interrupted attempts have no completed result and cannot resume as success.

## Declarative job template

Save this JSON outside maker/source folders. Input paths are relative to the manifest location unless absolute. All scripts, helper modules, asset files, brief/reference manifests, and other semantic file dependencies belong in `inputs`. `config` records additional frozen intent and participates in identity. Metadata such as a label cannot replace an actual declared file dependency.

```json
{
  "schema_version": 1,
  "lane": "preview",
  "jobs": [
    {
      "asset_id": "natural-arch",
      "revision": "r3",
      "job_id": "full-visual-plan",
      "inputs": {
        "glb": "/cloud/candidate/natural-arch.glb",
        "brief": "/cloud/candidate/brief.json",
        "references": "/cloud/candidate/references.json",
        "renderer": "/cloud/repo/scripts/render_candidate_views.py",
        "helper": "/cloud/repo/scripts/asset_common.py",
        "audit": "/cloud/repo/scripts/qa_glb.py"
      },
      "argv": [
        "{blender}", "--factory-startup", "--python", "{input:renderer}", "--",
        "{input:glb}", "--output-dir", "{output_dir}", "--revision", "r3",
        "--brief", "{input:brief}", "--references", "{input:references}",
        "--resolution", "256", "--samples", "8", "--turntable-frames", "24",
        "--views", "front,rear,left,right,top,bottom,clay,clayalt,wire,detail",
        "--detail-target", "0.5,0.5,0.6"
      ],
      "outputs": [
        "render-manifest.json", "render-config.json", "turntable.json",
        "turntable-000.png", "turntable-001.png", "turntable-002.png",
        "turntable-003.png", "turntable-004.png", "turntable-005.png",
        "turntable-006.png", "turntable-007.png", "turntable-008.png",
        "turntable-009.png", "turntable-010.png", "turntable-011.png",
        "turntable-012.png", "turntable-013.png", "turntable-014.png",
        "turntable-015.png", "turntable-016.png", "turntable-017.png",
        "turntable-018.png", "turntable-019.png", "turntable-020.png",
        "turntable-021.png", "turntable-022.png", "turntable-023.png",
        "front.png", "rear.png", "left.png", "right.png", "top.png", "bottom.png",
        "clay.png", "clayalt.png", "wire.png", "detail.png"
      ],
      "config": {"purpose": "quick exact-GLB visual plan before HD", "coverage_baseline": 24},
      "timeout_seconds": 600
    }
  ]
}
```

The detail target is a normalized bounding-box point chosen per asset; the example is not a universal good angle. Declare every required frame in `outputs`, not just the manifest, so missing frames fail the initial job. The runner also recursively hashes every regular file under `outputs`, including undeclared images; modifying, adding, or deleting one prevents resume even if the manifest stays unchanged. Output symlinks are rejected. File outputs must be normalized relative paths, cannot collide as file/directory names, and cannot resolve outside the attempt's output folder.

```sh
python3 scripts/run_asset_queue.py jobs.json --runs-root /cloud/runs/preview --resume
# Only after allocating a four-thread host share:
python3 scripts/run_asset_queue.py jobs.json --runs-root /cloud/runs/preview --workers 2 --threads 2 --cpu-budget 4 --resume
```

Additional executables require explicit `--allow-executable /absolute/path`; subprocess calls always use argument lists and `shell=False`. There is no inline shell command field. Python fixtures use this option only to test scheduler mechanics.

## Identity, immutable attempts, and resume

Layout:

```text
<runs-root>/<lane>/<asset>/<revision>/<job>/<fingerprint>/<timestamp-uuid>/
  request.json
  stdout.log
  stderr.log
  result.json
  outputs/
  work/
  tmp/
<runs-root>/runs/<queue-run-id>/manifest.json
<runs-root>/runs/<queue-run-id>/summary.json
```

A root lock rejects concurrent invocations in the same store. Asset/revision/job identifiers must be unique in a manifest. Each retry has a new UUID directory; the runner never rewrites completed records. This is append-only behavior, not cryptographic write protection against another process.

Identity hashes the declaration (including argv/config/outputs), actual declared input bytes, resolved executable bytes, runner version/bytes, lane, threads, timeout, and memory setting. Input and executable hashes are checked before dispatch and after completion; mutation is failure. Resume is opt-in and reuses only a successful matching identity whose request and **the whole output tree's current file list, sizes, and hashes** still match. Failure, cancellation, interrupted attempts, missing files, changed inputs/config/scripts, and changed output bytes never count as old success. `--retries 0..3` can retry failures/timeouts with unchanged inputs; it does not reuse failed outputs. Dependency completeness remains the author's responsibility, including external software/environment versions that can affect a result.

Exit codes: 0 all final jobs succeeded/reused; 1 job failure; 2 invalid configuration/launch setup; 130/143 cancellation. Summaries retain every attempt, including failed retries. Sampled process-group RSS/process counts are **observations at 50ms intervals**, not kernel maximums or throughput guarantees; startup/cleanup and hash checking are included in queue wall time.

## Renderer and web-preview contract

`render_candidate_views.py` imports the exact GLB into a fresh scene, adds an isolated fixed studio/camera, and never saves over the GLB or source `.blend`. Use an empty separate output directory. It reuses source import, scene, material, color, bounds, and camera helpers. It emits:

- `render-config.json`: renderer/helper hashes, Blender version, CPU settings, color management, lighting, fixed enclosing-sphere orthographic framing, dimensions, frame plan, base pose, elevation, and detail target.
- `render-manifest.json`: `schema_version:1`, `kind:"render_manifest"`, `stage:"visual"`, source-bound `subject`, render-config path/hash, frame IDs/view tags/angles/dimensions/byte counts/SHA-256, total encoded bytes, decoded RGBA estimate, and pending visual/runtime review states.
- `turntable.json`: website `version:1`, `source_glb_sha256`, `config_sha256`, orbit-only `frame_count`, `width`, `height`, `frames`, `poster_index`, `background`, elevation/base pose, total bytes, decoded estimate. Frames include `path`, `bytes`, `sha256`, `azimuth_deg`, and `elevation_deg`. All file paths are relative to their manifest directory. This supports image mouse/touch scrubbing without WebGL; it does not implement a website or replace real-GLB detail-view checks.

The normal turntable baseline is 24–36 frames, configurable for asset complexity and an approved brief. Default is 24. Top/bottom, clay/wire, and targeted detail views are separate diagnostic frames; orbit coverage is not a substitute. Fixed framing prevents zoom pumping between orbit angles. Default diagnostics omit targeted detail until a per-asset `--detail-target` is provided. A full QA reviewer must inspect the declared full frame set (with montage as an aid); a few beauty views cannot pass full coverage.

```sh
blender -b -t 2 --python-exit-code 1 --python scripts/render_candidate_views.py -- \
  /cloud/candidate/model.glb --output-dir /cloud/preview/new-run --revision r3 \
  --resolution 256 --samples 8 --turntable-frames 24 \
  --views front,rear,left,right,top,bottom,clay,clayalt,wire,detail --detail-target 0.5,0.5,0.6
# A lightweight website set, kept distinct from full-resolution QA evidence:
blender -b -t 2 --python-exit-code 1 --python scripts/render_candidate_views.py -- \
  /cloud/original/model.glb --output-dir /cloud/preview/web-run --revision original \
  --resolution 512 --samples 8 --turntable-frames 24 --views '' --format WEBP
```

WEBP conversion uses an explicitly selected/available Python with Pillow/WebP support, performs no installation, and uses argument-list subprocesses. PNG is the default. Individual image frames are the baseline; sprite-sheet versus image-frame transfer, decode memory, loading, and device performance must be benchmarked before choosing a different packaging format. `--turntable-frames 0 --views hero,side` is an explicitly incomplete quick smoke test, never full visual evidence. Missing brief/reference hashes remain null and cannot pass formal candidate evidence gates. No browser GPU/runtime test is performed by this renderer.

## Verified capacity, October 17, 2026

- Scheduler fixture suite: final 13 tests passed in 13.46 seconds; the initial 11-test suite took 10.76 seconds, before adding whole-output-tree tamper and shared-root lock regressions. Tested two simultaneous tiny Python jobs, five total, bounded peak of two; failure/retry, output collisions/path escape, missing outputs, timeout, SIGTERM termination/drain, successful-child orphan cleanup, optional memory limit, resume/config/script/input invalidation. These are scheduler tests, not Blender throughput measurements.
- Real Blender 4.3.2 pilot: frozen copies of V4 `triceratops-horridus.glb` (SHA-256 `d2a6abc238eb890504acbb83692fb3eca7b3a3550e09cf3cab3dd15b10f379e9`) and refined arch B (SHA-256 `9427a1b0e38790c562bb30f04559c825ecb0b59600d4dce221ee805ccc01cc81`). Source originals remained unchanged.
- Actual run was **serial: 1 worker × 2 threads**, two PNG views per asset at 256px, 4 samples. Total queue wall 8.6829 seconds; dinosaur 6.1665 seconds; arch 1.8011 seconds. Sampled peak process-group RSS 272,039,936 bytes (~259.4 MiB), peak one active job/process. RSS limit was disabled. Nine affinity CPUs were visible, but cgroup quota was hidden; other cloud makers were running and capacity was coordinated.
- Pixels were checked for nonblank correct-asset output. Four views total are incomplete. No 24-frame/full-diagnostic coverage, visual acceptance, real-GLB browser/GPU pass, two-Blender concurrency, production throughput, or 1,000-asset capacity has been established by this initial pilot. Keep the default at one worker until representative combined-resource measurements justify raising it.

Run scheduler tests with `python3 scripts/test_asset_queue.py`.

### Full-coverage quick renderer exercise

A second, separately frozen textured triceratops study used GLB SHA-256 `e24b10555eab61d0a3001f1dba9713477a80a3099c77a33ec6a8196a7ec70930`, revision `v4-texture-2k`, with its actual brief/reference hashes. The queue ran one 2-thread Blender job producing **24 orbit frames + 10 diagnostic frames** (front/rear/left/right/top/bottom/clay/clayalt/wire/head-frill detail), all original 256px PNGs, 4 samples. Full original frames and a labeled contact sheet were retained separately.

Measured queue wall: **31.1497 seconds**; renderer loop: **26.42 seconds**; sampled peak process-group RSS: **348,184,576 bytes (~332.1 MiB)**; peak one active job/process. Encoded frame bytes: **1,870,928**; decoded RGBA estimate: **8,912,896 bytes** for all 34 frames. The standard render-manifest checker verified exact source/brief/reference/config binding, image hashes/dimensions/bytes, required diagnostics, and 24 distinct angles around the complete orbit with no coverage problems.

This is actual full-plan generation and structural evidence checking, **not artistic acceptance**. Contact-sheet inspection showed the intended angles, stable orbit scale, alternate clay lighting, wire view, and head/frill crop. Low 4-sample noise limits fine texture judgment; the study retains its visual/factual/runtime blockers. The run still establishes only serial Blender operation, not a two-Blender throughput result. WebP conversion was separately exercised with two 128px orbit frames and clayalt on the frozen arch; it does not establish 512px website capacity. The validator supports PNG, JPEG and WebP dimensions; unsupported formats such as AVIF remain blocked until an explicit decoder and tests are added. Website sequences must use a separately frozen target-renderer profile matching the actual detail viewer; neutral Blender QA lighting is not assumed to match Three.js.
