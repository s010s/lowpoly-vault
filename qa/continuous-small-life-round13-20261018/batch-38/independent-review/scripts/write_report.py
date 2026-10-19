#!/usr/bin/env python3
"""Assemble the final machine-readable independent QA record from evidence."""
from datetime import datetime, timezone
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
QA = Path(__file__).resolve().parents[1]
E = QA / "evidence"
batch = ROOT / "production/continuous-small-life-round13-20261018/work/batch-38"
handoff = json.loads((batch / "HANDOFF.json").read_text())
scope = json.loads((batch / "QA-HANDOFF-SCOPE.json").read_text())
integrity = json.loads((E / "source-integrity.json").read_text())
profile = json.loads((E / "profile-checks/summary.json").read_text())
rebuild = json.loads((E / "rebuilds/rebuild-summary.json").read_text())
visual = json.loads((E / "visual-inspection.json").read_text())
visual_by_id = {a["asset_id"]: a for a in visual["assets"]}
profile_by_id = {a["asset_id"]: a for a in profile["assets"]}
rebuild_by_id = {a["asset_id"]: a for a in rebuild["assets"]}
fixed_views = ["hero", "reversehero", "front", "side", "rear", "top", "clay", "silhouette"]
runtime_views = ["single-hero", "single-reversehero", "single-front", "single-side", "single-rear", "single-top", "single-bottom",
                 "single-80px", "single-160px", "single-240px", "scene-hero", "scene-top"]
digest = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

notes = {
    "diplomoceras": {
        "content_verdict": "PASS within preserved-shell concept scope",
        "observation": "A single continuous, ribbed shell sweep with two broad open hairpin turns and parallel growing shafts reads consistently in the fixed views and exact-GLB browser views. The terminal aperture is visibly recessed. It remains clearly a simplified shell-only teaching prop; no soft body, chamber reconstruction, species dimensions, or swimming behavior is inferred.",
        "must_fix": [], "reviewed_nonblocking_warnings": ["Smooth-shaded source faces on the round shell were flagged by the mechanical audit and visually reviewed as intentional."]
    },
    "nelumbo": {
        "content_verdict": "PASS within detached fossil-leaf scope",
        "observation": "The broad, lightly uneven peltate disk, near-central attachment scar, and radial venation remain readable in top, clay, silhouette, and runtime views. Side views show shallow relief. The mesh retains only a detached leaf form; no flower, pod, root, whole plant, or exact modern species claim is made.",
        "must_fix": [], "reviewed_nonblocking_warnings": ["Smooth-shaded leaf and venation faces were flagged by the mechanical audit and visually reviewed as intentional for shallow organic relief."]
    },
    "marine-terrace": {
        "content_verdict": "PASS within original stylized landscape-crop scope",
        "observation": "The stepped bench, rear abandoned cliff, and lower seaward margin read as a coherent teaching section from hero, side, and top views. The 16 m span is retained as an illustrative crop. The supplied context plane is presentation-only; no water simulation, surveyed locality, dated site, or uplift rate is claimed.",
        "must_fix": [], "reviewed_nonblocking_warnings": []
    },
    "angular-unconformity-outcrop": {
        "content_verdict": "PASS within original teaching-section scope",
        "observation": "Older inclined lower beds visibly terminate at a real contact under three near-horizontal upper beds. The contact remains legible in neutral clay and opposing runtime views. This is an original 0.85 m teaching section, not a named locality or dated sequence.",
        "must_fix": [], "reviewed_nonblocking_warnings": []
    }
}

assets = []
for a in handoff["assets"]:
    asset = a["asset_id"]
    src_report = json.loads((E / f"blender/{asset}-source-export.json").read_text())
    scene_report = json.loads((E / f"blender/{asset}-source-scene.json").read_text())
    profile_item = json.loads((E / f"profile-checks/{asset}.json").read_text())
    profile_result = profile_item["result"]
    browser_single = json.loads((E / f"runtime/{asset}/single.json").read_text())
    browser_scene = json.loads((E / f"runtime/{asset}/scene.json").read_text())
    khronos = json.loads((E / f"blender/{asset}-khronos.json").read_text())
    rebuilt = rebuild_by_id[asset]
    run_pairs = [json.loads((E / f"rebuilds/{asset}/run-{n}-source-export.json").read_text()) for n in (1,2)]
    v = visual_by_id[asset]
    assets.append({
        "asset_id": asset,
        "attempt": a["selected_attempt"],
        "claim_scope": handoff["subject_scope"][asset],
        "content_review": notes[asset],
        "measurements": {"dimensions_m_glTF_XYZ": a["dimensions_m"], "triangles": a["triangles"],
                         "materials": a["materials"], "primitives": a["primitives"]},
        "frozen_artifacts": {
            "blend": {"path": a["blend"]["path"], "sha256": a["blend"]["sha256"], "bytes": a["blend"]["bytes"]},
            "glb": {"path": a["glb"]["path"], "sha256": a["glb"]["sha256"], "bytes": a["glb"]["bytes"]}
        },
        "source_scene": {"status": scene_report["status"], "blender_version": scene_report["blender_version"],
                         "unit_scale": scene_report["unit_scale"], "root_identity": scene_report["root_identity"],
                         "cameras_lights": scene_report["source_scene_cameras_lights"],
                         "vertices_authored": scene_report["source_authored_vertices"],
                         "vertices_evaluated": scene_report["source_evaluated_vertices"],
                         "parts": scene_report["parts"], "evidence": f"evidence/blender/{asset}-source-scene.json"},
        "source_to_glb": {"status": src_report["status"], "triangles_match": src_report["triangles_match"],
                           "bounds_match": src_report["bounds_match"], "bounds_max_error_m": src_report["bounds_max_error_m"],
                           "tolerance_m": src_report["tolerance_m"], "warnings": src_report["warnings"],
                           "evidence": f"evidence/blender/{asset}-source-export.json"},
        "official_khronos": {"status": "pass" if khronos["issues"]["numErrors"] == 0 else "fail",
                              "validator_version": khronos["validatorVersion"], "errors": khronos["issues"]["numErrors"],
                              "warnings": khronos["issues"]["numWarnings"], "exact_glb_sha256": a["glb"]["sha256"],
                              "evidence": f"evidence/blender/{asset}-khronos.json"},
        "rebuilds": {"status": "pass" if rebuilt["rebuild_semantic_match_frozen"] and rebuilt["rebuilds_semantically_match_each_other"] else "fail",
                     "runs": [{"run": r["run"], "status": r["status"], "glb_sha256": r["glb_sha256"],
                               "blend_sha256": r["blend_sha256"], "semantic_sha256": r["semantic_sha256"],
                               "triangles": r["triangles"], "log": r["log_path"], "log_sha256": r["log_sha256"]} for r in rebuilt["runs"]],
                     "both_glbs_byte_identical_to_frozen": rebuilt["rebuild_bytes_match_frozen"],
                     "both_semantically_match_frozen": rebuilt["rebuild_semantic_match_frozen"],
                     "both_rebuilds_match_each_other": rebuilt["rebuilds_semantically_match_each_other"],
                     "source_export_pair_checks": [{"status": r["status"], "triangles_match": r["triangles_match"],
                                                     "bounds_match": r["bounds_match"], "bounds_max_error_m": r["bounds_max_error_m"],
                                                     "evidence": f"evidence/rebuilds/{asset}/run-{i}-source-export.json"}
                                                    for i,r in enumerate(run_pairs,1)],
                     "evidence": "evidence/rebuilds/rebuild-summary.json"},
        "fixed_view_review": {"profile_view_count": 8, "views": fixed_views, "fresh_independent_render": True,
                              "fresh_source_images": [x["path"] for x in v["source_fixed_views"]],
                              "contact_sheet": v["source_contact_sheet"], "evidence": f"evidence/fixed-views/{asset}/render-manifest.json"},
        "runtime_review": {"single_mode": browser_single["status"], "single_view_count": len(browser_single["views"]),
                           "six_instance_scene_mode": browser_scene["status"], "scene_view_count": len(browser_scene["views"]),
                           "three_revision": browser_single["three"], "webgl2": browser_single["webgl2"],
                           "renderer": browser_single["renderer"], "errors": browser_single["errors"],
                           "failed_requests": browser_single["failed"], "captured_views": runtime_views,
                           "pixel_contact_sheet": v["runtime_contact_sheet"], "evidence": f"evidence/runtime/{asset}/"},
        "static_profile_check": {"profile": "static-stylized-v1", "rule_version": "2026-10-18.1",
                                 "profile_contract_status": profile_result.get("profile_contract_status"),
                                 "candidate_valid": profile_result.get("valid"),
                                 "approved_for_brief": profile_result.get("approved_for_brief"),
                                 "approval_blockers": profile_result.get("approval_blockers"),
                                 "evidence": f"evidence/profile-checks/{asset}.json"}
    })

report = {
    "schema_version": 1,
    "report_type": "independent_visual_technical_qa",
    "created_at_utc": datetime.now(timezone.utc).isoformat(),
    "scope": {"candidate_branch": handoff["branch"], "handoff_commit": integrity["handoff_commit"],
              "handoff_path": integrity["handoff_path"], "handoff_sha256": integrity["handoff_sha256"],
              "model_source_commit": integrity["model_source_commit"], "qa_handoff_scope_path": integrity["qa_handoff_scope_path"],
              "qa_handoff_scope_sha256": integrity["qa_handoff_scope_sha256"], "batch_id": "batch-38",
              "expected_asset_ids": scope["expected_asset_ids"], "expected_glb_sha256_by_asset": scope["expected_glb_sha256_by_asset"],
              "profile": "static-stylized-v1", "rule_version": "2026-10-18.1"},
    "reviewer_identity": {"requested_model": "GPT-6 Luna", "requested_reasoning": "xhigh",
                          "backend_identity_status": "not independently verified",
                          "reason": "The execution context exposes no backend model or reasoning metadata. This review does not infer the requested model from a generic assistant identity and no duplicate QA was initiated on that basis."},
    "overall": {"content_verdict": "PASS within the frozen, user-authorized stylized claim scopes",
                "technical_verdict": "PASS for the exact frozen Blend/GLB artifacts and two independent rebuilds per asset",
                "formal_profile_acceptance": "BLOCKED; this review does not mutate candidate approval/stage records",
                "model_repairs_required": [],
                "formal_blockers": ["The candidate records remain approved_for_brief=false and retain unknown/pending production stage values.",
                                    "No hardware-GPU evidence was produced; browser evidence uses ANGLE SwiftShader software WebGL2.",
                                    "The requested reviewer model/reasoning identity cannot be independently attested from the available backend metadata."],
                "hardware_performance_claim": False},
    "integrity": {"status": integrity["status"], "handoff_reference_occurrences_verified": integrity["handoff_file_references_verified"],
                   "frozen_source_glb_and_blend_blobs_verified": len(integrity["model_source_glb_blend_blobs_verified"]),
                   "evidence": "evidence/source-integrity.json"},
    "profile_check_summary": profile,
    "runtime_environment": {"blender": "4.3.2", "chromium": "154.0.8037.57", "three_revision": "180",
                             "renderer": "ANGLE SwiftShader software WebGL2", "runtime_scope": "load/draw/pixel evidence only; no physical-device or GPU performance claim"},
    "browser_summary_evidence": "evidence/runtime/batch38-browser-summary.json",
    "assets": assets,
    "visual_review_policy": "Reviewed frozen claim scopes, exact frozen fixed-view/source/runtime evidence, fresh fixed source renders, and fresh exact-GLB browser pixels. Style accepted as refined low-poly teaching props; strict scientific reconstruction was not required.",
    "applicable_instructions_reviewed": ["skills/blender-lowpoly-pipeline/SKILL.md and references/qa-design.md, production-contract.md",
                                        "skills/lowpoly-art-direction/SKILL.md and references/visual-acceptance.md",
                                        "skills/asset-factual-review/SKILL.md",
                                        "skills/prehistoric-environment-art/SKILL.md",
                                        ".agents/skills/emil-animation/* reviewed; not applicable to static asset QA",
                                        "docs/candidate-profile-compatibility.zh-CN.md and schemas/README.md (static-stylized-v1 2026-10-18.1)"],
    "limitations": ["This is one independent QA round; no unbounded microdetail iteration was performed.",
                    "Content decisions apply only to the frozen artistic/specimen scopes, not species-level scientific validation.",
                    "SwiftShader WebGL2 is software rendering; it is not evidence of hardware GPU behavior or representative museum-scene performance.",
                    "Candidate assets, stage thresholds, CI, permissions, publication records, and main were not changed."]
}
out = QA / "review.json"
out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"report": str(out.relative_to(ROOT)), "assets": len(assets), "content": report["overall"]["content_verdict"],
                  "formal": report["overall"]["formal_profile_acceptance"], "model_identity": report["reviewer_identity"]["backend_identity_status"]}, indent=2))
