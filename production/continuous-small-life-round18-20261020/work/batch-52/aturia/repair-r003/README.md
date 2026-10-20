# Aturia r003 color repair

Final handoff: `handoff.json`. Candidate delivery: `assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/`.

From the repository root, run the read-only pinned-file and candidate/concept integrity verification:

```bash
python3 production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/verify_delivery.py
```

Rebuilds are reproducible with the retained `build-jobs.json` and `scripts/run_asset_queue.py`, using a NEW runs-root inside this repair folder, one worker and two Blender threads. Existing successful queue request/results and two semantic comparisons are retained. `verification-commands.json` records actual source/static/Khronos/rebuild/render commands and elapsed times; final render used `brief-production.json` and `proof-final`, logged in `logs/render-final.log`. `check_color_only.py BASELINE.glb R003.glb NEW_REPORT.json` verifies the sole permitted RGB/metadata change. `check_source_geometry.py` runs under Blender with baseline source, r003 source, and a NEW output report after `--`.

All eight exact-GLB views are in `proof-final`; `preview-hero.png` is its hero file verbatim. Both original r002 and all earlier assets/evidence remain in place. The requested change is complete, and formal independent r003 acceptance remains pending. Exact ImageGen provider time, hardware GPU, formal populated target scene and r003 browser-runtime checks remain unknown/unrun. `validate_concept_evidence.py --require-complete` is expected to fail solely for the disclosed unknown provider timestamp.

The first local color-only checker failed because its whitelist omitted the matching palette_srgb metadata update. That report is retained; corrected verification accepts exactly that metadata field and the three RGB components. No model repair retry was needed.
