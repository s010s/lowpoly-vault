# Asset-budget research for lowpoly-vault

Research date: 2026-10-17. Baseline: main `e4019e28354f058cd11efaf5e4529af1e957855a`, Three.js `0.180.0`.

## Main result

Budget by role, projected screen size, visible repetition and target device. Start with convincing proportions/silhouette and lightweight color, then add surface detail only when matched A/B demonstrates value. The accepted 471,784-byte Triceratops is a useful concrete trade-off, not a universal 500 KB ceiling.

**All numeric profiles here are project proposals awaiting real-device calibration. They are not industry standards, engine limits, adopted defaults or measured FPS guarantees.** No production files/defaults are changed by this research folder.

## Read first

- [中文完整报告与预算表](REPORT.zh-CN.md)
- [English Skill-ready policy proposal](proposals/BUDGET_POLICY.md)
- [Machine-readable planning profiles](proposals/budget-profiles.proposed.json)
- [Device/scene measurement protocol](MEASUREMENT_PLAN.md)
- [37 primary sources with evidence classes and dates](SOURCES.md)

## Reproducible evidence and implementation proposal

- [19 exact local GLB inventories](data/local-sample-inventory.json): hashes, bytes, declarations, embedded-image costs and explicitly estimated mip allocations.
- [Official sample metadata](data/official-sample-metadata.json): Fox, DamagedHelmet and FlightHelmet at a pinned Khronos commit; not FPS benchmarks.
- [Source ledger JSON](data/source-ledger.json).
- [Record schema](proposals/asset-budget-record.schema.json) and [held Triceratops example](proposals/triceratops-light.example.json).
- [Research-only schema/cross-field checker](scripts/check_budget_record.py) and [15 tests](tests/test_budget_record.py).
- [Read-only supported-subset GLB inventory](scripts/inspect_glb_samples.py).

The inventory is not a glTF validator. The evidence-record checker cannot verify that referenced reviews are truthful or replace human/device QA. The synthetic approval test fixture is not a real asset approval.

## Validation status and commands

The GLB inventory was run against the actual research artifacts before the environment interruption. Reports retain exact hashes and clearly separate declared counts from measured bytes and estimated memory. The new record schema/checker/test suite is delivered for validation; **test execution is pending in this snapshot**. No actual-device GPU/frame/decode benchmark was run.

From this folder, with Python and jsonschema available:

```sh
python -m unittest discover -s tests -v
python scripts/check_budget_record.py proposals/asset-budget-record.schema.json proposals/triceratops-light.example.json
```

The first command should run 15 unit tests. The second should accept the record structure while its release_status remains hold. A valid held record is not a release approval.

To regenerate supported GLB inventories, provide an input JSON array of objects containing id, path and optional visual_status, then run:

```sh
python scripts/inspect_glb_samples.py inputs.local.json output.json
```

The inventory requires Pillow and actual source assets. Local machine paths are intentionally not committed. Compare SHA-256 with the archived inventory before interpreting differences. It does not decode compressed geometry or validate arbitrary glTF features.

## Open requirements

1. Run the delivered schema tests in a stable environment and archive the result.
2. Nominate minimum devices and calibrate representative assets in a real populated museum scene.
3. Review/adopt specific profile limits and reconcile this proposal with the existing frozen-brief pipeline.
4. Preserve independent shape/factual/runtime holds despite bounded user style/size acceptance.
5. Archive this committed research folder with the project's backup process.

Source assets and third-party model binaries are not duplicated here. See per-asset source/experiment records and licenses. Original helper scripts in this folder carry MIT SPDX notices.
