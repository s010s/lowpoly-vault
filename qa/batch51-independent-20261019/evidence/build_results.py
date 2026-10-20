#!/usr/bin/env python3
"""Build the machine-readable review summary from pinned Batch 51 artifacts."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path("assets/candidates/continuous-small-life-round17-20261018/batch-51")
EVIDENCE = Path("qa/batch51-independent-20261019/evidence")
SELECTIONS = [
    ("dicranurus", "r001", "pass", "AMNH Hall of Fame, PDF p.31"),
    ("calcite-raft-deposit", "r002", "pass", "NPS Wind Cave calcite-raft section"),
    ("accretionary-lapilli-bed", "r002", "pass", "USGS Bohor & Triplehorn (1984); NPS Hawaiʻi PDF separately unavailable"),
    ("conichnus-conical-burrow", "r001", "pass", "Kansas Geological Survey, Conichnus section"),
]
NOMINAL_AXIS_SIZE = {
    "dicranurus": (0.065, "body and backward horns span", 2),
    "calcite-raft-deposit": (0.42, "former pool-floor deposit span", 0),
    "accretionary-lapilli-bed": (0.60, "layered ash teaching section width", 0),
    "conichnus-conical-burrow": (0.24, "interpretive sediment section span", 0),
}
SPEC = {
    "dicranurus": {
        "status": "pass",
        "note": "The measured longest span is 0.06083 m against a 0.065 m nominal choice (about 6.4% below); the frozen construction plan also specifies 0.065 m, and no stricter tolerance is stated.",
    },
    "calcite-raft-deposit": {
        "status": "fail",
        "note": "Candidate brief scale is 0.42 m, while the frozen plan/prompt nominal is 0.32 m and exported floor span is 0.33594 m. This is an input-spec conflict, not a visual defect.",
    },
    "accretionary-lapilli-bed": {
        "status": "fail",
        "note": "Candidate brief scale is 0.60 m, while the concept prompt and frozen plan nominal are 0.28 m and exported width is 0.28450 m. This is an input-spec conflict, not a visual defect.",
    },
    "conichnus-conical-burrow": {
        "status": "pass",
        "note": "Exported span 0.24000 m matches the 0.24 m nominal scale and frozen plan.",
    },
}
VISUAL = {
    "dicranurus": "Paired open backward-curving horn loops, compact segmented body and paired lateral spines read clearly in the exact candidate views; no model change requested.",
    "calcite-raft-deposit": "Thin, broken polygonal sheets overlap across visible former-pool substrate; low side/front views confirm thin plate form; no model change requested.",
    "accretionary-lapilli-bed": "Continuous layered ash block, sparse embedded rounded pellets and three exposed concentric sections read as the specified teaching block; no model change requested.",
    "conichnus-conical-burrow": "The top opening is a true negative cavity in a volumetric block; neutral gray top/oblique/half-section and independent rays confirm a deep wall that narrows toward a small rounded bottom. No slab outline, positive cone or footprint; no model change requested.",
}


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    handoff = read(Path("production/continuous-small-life-round17-20261018/work/batch-51/QA-HANDOFF.json"))
    integrity_exit = read(EVIDENCE / "replay/candidate-checks/exit-codes.json")
    runtime_replay = read(EVIDENCE / "replay/runtime/runtime-replay-summary.json")
    ray_stdout = (ROOT / EVIDENCE / "replay/conichnus/independent-raycast.stdout.txt").read_text()
    ray_prefix = "BATCH51_RAY_PROBE_JSON="
    ray_obj = json.loads(next(line[len(ray_prefix):] for line in ray_stdout.splitlines() if line.startswith(ray_prefix)))
    runtimes = {item["asset_id"]: item for item in runtime_replay["items"]}

    items = []
    for asset, revision, factual_status, source_summary in SELECTIONS:
        bundle = BASE / asset / revision
        candidate = read(bundle / "candidate.json")
        brief = read(bundle / "candidate-brief.json")
        metrics = read(bundle / "source-metrics.json")
        concept = read(bundle / "concept-evidence.json")
        generation = read(bundle / "concepts/generation-record.json")
        inspection = read(bundle / "concepts/inspection.json")
        model_start = read(bundle / "model-start.json")
        visuals = read(bundle / "candidate-proof/render-manifest.json")
        validator = read(EVIDENCE / f"replay/khronos/{asset}/qa.json")["khronos_validator"]
        source_export = read(EVIDENCE / f"replay/blender-source-export/{asset}.json")
        concept_check = read(EVIDENCE / f"replay/candidate-checks/{asset}-concept-require-complete.json")
        approval_check = read(EVIDENCE / f"replay/candidate-checks/{asset}-require-approved.json")
        codes = {row["check"]: row["exit_code"] for row in integrity_exit if row["asset_id"] == asset}
        target_size, axis, axis_index = NOMINAL_AXIS_SIZE[asset]
        actual_axis = metrics["dimensions_glb_xyz_m"][axis_index]
        plan = brief["frozen_construction_plan"]
        runtime_record = runtimes[asset]
        items.append(
            {
                "asset_id": asset,
                "revision": revision,
                "glb_sha256": handoff["items"][len(items)]["glb_sha256"],
                "source_blend_sha256": metrics["source_sha256"],
                "concept_image_sha256": generation["image_sha256"],
                "concept_prompt_sha256": generation["prompt_sha256"],
                "derived_freeze_sha256": sha(bundle / "derived-freeze.json"),
                "visual": {"status": "pass", "views_reviewed": sorted(frame["id"] for frame in visuals["frames"]), "note": VISUAL[asset]},
                "factual": {"status": factual_status, "reference_summary": source_summary, "claim_scope": candidate["metadata"] if "metadata" in candidate else brief["claim_scope"]},
                "specification": {
                    **SPEC[asset],
                    "nominal_scale_m": target_size,
                    "nominal_scale_axis": axis,
                    "measured_axis_extent_m": actual_axis,
                    "all_export_dimensions_gltf_xyz_m": metrics["dimensions_glb_xyz_m"],
                    "frozen_plan_dimensions_m": plan.get("dimensions"),
                    "frozen_plan_nominal_m": plan.get("nominal"),
                },
                "format_and_budget": {
                    "status": "pass",
                    "blender_version": metrics["blender_version"],
                    "source_glb_triangle_bounds_comparison": source_export["status"],
                    "source_glb_triangle_counts_match": source_export["triangles_match"],
                    "source_glb_bounds_match_within_m": source_export["tolerance_m"],
                    "khronos_status": validator["status"],
                    "khronos_errors": validator["num_errors"],
                    "khronos_warnings": validator["num_warnings"],
                    "triangles": metrics["glb_scene_triangles"],
                    "materials": metrics["glb_materials"],
                    "primitives": metrics["glb_primitives"],
                    "glb_bytes": metrics["glb_bytes"],
                    "images": 0,
                    "textures": 0,
                    "limits": {"triangles": 14000, "glb_bytes": 1000000, "materials": 6, "primitives": 30},
                },
                "runtime_parse": {"status": "pass", "independently_replayed": True, "runtime_replay_exit_code": runtime_record["exit_code"], "browser": "Chromium " + runtime_record["browser_version"], "three": runtime_record["three_version"], "parsed_glb_sha256": runtime_record["glb_sha256"], "all_7_screenshot_pixels_identical_to_candidate": all(v["pixel_identical"] for v in runtime_record["views"].values()), "gl_errors": 0, "browser_errors": runtime_record["browser_errors"]},
                "functional_software_webgl": {"status": "pass", "renderer": runtime_record["unmasked_renderer"], "hardware_gpu_verified": False},
                "representative_single_asset_scene": {"status": "pass", "instances": 9, "render_calls": next(v["render_calls"] for v in read(bundle / "runtime/runtime-report.json")["views"] if v["name"] == "scene-9-copies"), "neutral_grid": "3 x 3 clones of this exact GLB", "parent_or_museum_scene_verified": False},
                "concept_order_and_completeness": {
                    "call_and_capture_recorded": generation["tool"] == "image_gen.imagegen" and sha(bundle / "concepts/original.png") == generation["image_sha256"],
                    "captured_at": generation["captured_at"],
                    "inspected_at": inspection["inspected_at"],
                    "modeling_started_at": model_start["modeling_started_at"],
                    "capture_before_inspection_before_modeling": generation["captured_at"] < inspection["inspected_at"] < model_start["modeling_started_at"],
                    "concept_generated_at": None,
                    "require_complete_exit_code": codes["concept-require-complete"],
                    "require_complete_valid": concept_check["valid"],
                    "require_complete": concept_check["evidence_complete"],
                    "exact_blockers": concept_check["blockers"],
                    "order_evidence_assessment": "Stored ImageGen prompt/result/capture, matching original image hash, view record and later model-start receipt support call-result capture -> image view -> modeling. The provider did not disclose the exact generation instant.",
                },
                "formal_candidate_approval": {
                    "status": "not approved",
                    "candidate_integrity_exit_code": codes["candidate-integrity"],
                    "candidate_record_approval": candidate.get("approval", {}).get("status"),
                    "require_approved_exit_code": codes["require-approved"],
                    "require_approved_valid": approval_check["valid"],
                    "require_approved": approval_check["approved_for_brief"],
                    "current_open_blockers": [blocker["id"] for blocker in candidate.get("blockers", []) if blocker.get("status") == "open"],
                },
            }
        )

    result = {
        "schema_version": 1,
        "kind": "batch51-independent-qa-results",
        "reviewed_at": "2026-10-19T23:24:47Z",
        "branch": "qa/batch51-independent-20261019",
        "candidate_handoff_commit": "6b5bc2793572361242544f7a19afd6bbd71243ab",
        "artifact_source_commit": "ee4e37b3c1cc49ab5e41c807c6ca8e1a155bbc6b",
        "official_profile": "static-stylized-v1 / 2026-10-18.1",
        "overall": "Independent limited-stage QA is recorded below. It is not formal candidate approval.",
        "batch_requirement_findings": {
            "actual_scene_requirement": "Neutral multiple-copy teaching-prop benchmark with actual instance/work counts.",
            "128_8_32_count_requirement_found": False,
            "reason": "No 128/8/32 count appears in the batch task, QA scope or selected briefs. Each item has a hash-bound neutral 3x3 nine-copy single-asset benchmark; this is not a parent/museum scene.",
            "hardware_gpu": "unverified; the available browser used ANGLE SwiftShader software WebGL.",
        },
        "concept_provenance_finding": {
            "order_evidence": "Sufficient for the recorded sequence ImageGen output captured -> matching source image viewed -> first modeling start.",
            "exact_generation_time": "unknown for all four; kept null, not derived from capture time or file mtimes.",
            "formal_completeness": "Blocked for all four: --require-complete exits 1 with only 'concept_generated_at: unknown; do not reconstruct times from file mtimes'.",
        },
        "nonblocking_source_access_issue": {
            "source_id": "EN-VO3B",
            "source": "NPS Hawaiʻi Keonehelelei eruption-geology PDF",
            "status": "unverified; inherited search result only; current retrieval returned proxy 403/internal error.",
            "impact": "Does not block the generalized accretionary-lapilli claim because the accessible USGS source supports spherical volcanic-ash aggregates and accretion around nuclei.",
        },
        "conichnus_independent_ray_probe": ray_obj,
        "items": items,
        "formal_gate_current_state": {
            "all_four_require_approved": "exit 1; approved_for_brief=false",
            "all_four_require_complete": "exit 1; evidence_complete=false",
            "candidate_review_records": "Remain pending/unknown on the pinned candidate branch. This independent report does not mutate them.",
            "hard_missing_evidence": [
                "Exact ImageGen provider generation time is unavailable. Current completeness checker and open candidate blocker require it.",
                "Candidate-side independent visual/factual/specification/GPU/scene stage verdict records remain unknown and approval pending; this separate QA report does not promote the candidate record.",
                "Calcite and lapilli candidate briefs disagree with their selected construction-plan/prompt nominal size and need a versioned specification decision before formal approval.",
                "Hardware GPU and actual parent/museum scene remain unverified.",
            ],
        },
    }
    (ROOT / EVIDENCE / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
