#!/usr/bin/env python3
"""Read-only integrity audit of batch39 source handoff and pinned candidate branches."""
from __future__ import annotations

import hashlib
import json
import subprocess
import struct
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
WORKSPACE = REPO.parent
SOURCE_COMMIT = "0eed2d38d04f4b3d2b847eff8f376934769c0102"
SOURCE_DIR = REPO / "production/continuous-small-life-round13-20261018/work/batch-39"
IDS = ["clavagella", "aa-lava-front", "native-copper-dendrite", "nereites-lobed-meander"]
EXPECTED_VIEWS = ["hero", "reversehero", "front", "side", "rear", "top", "clay", "silhouette"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_size(path: Path) -> list[int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
        raise ValueError(f"not a PNG: {path}")
    return list(struct.unpack(">II", data[16:24]))


def json_file(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    path = path.resolve()
    for asset_id in IDS:
        candidate_root = WORKSPACE / f"lowpoly-vault-b39-review-{asset_id}"
        if path.is_relative_to(candidate_root):
            return path.relative_to(candidate_root).as_posix()
    return path.relative_to(REPO).as_posix()


handoff_path = SOURCE_DIR / "HANDOFF.md"
final_path = SOURCE_DIR / "final-handoff.jsonl"
scope_path = SOURCE_DIR / "scope.json"
final_rows = [json.loads(line) for line in final_path.read_text(encoding="utf-8").splitlines() if line.strip()]
scope = json_file(scope_path)
assert len(final_rows) == 4 and [row["asset_id"] for row in final_rows] == IDS
final_digest = sha(final_path)
assert final_digest == scope["final_handoff_jsonl_sha256"]
assert SOURCE_COMMIT == subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()

report = {
    "schema_version": 1,
    "kind": "batch39-independent-integrity-audit",
    "source": {
        "handoff_commit": SOURCE_COMMIT,
        "handoff_path": rel(handoff_path),
        "handoff_sha256": sha(handoff_path),
        "final_handoff_path": rel(final_path),
        "final_handoff_sha256": final_digest,
        "scope_path": rel(scope_path),
        "scope_sha256": sha(scope_path),
        "scope_pins_final_handoff": True,
        "base_commit": scope["base_commit"],
        "planning_commit": scope["planning_commit"],
    },
    "assets": [],
}

for row in final_rows:
    asset_id = row["asset_id"]
    candidate_root = WORKSPACE / f"lowpoly-vault-b39-review-{asset_id}"
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=candidate_root, text=True).strip()
    remote_tip = subprocess.check_output(
        ["git", "rev-parse", f"origin/{row['branch']}"], cwd=REPO, text=True
    ).strip()
    assert head == row["remote_tip"] == remote_tip == row["commit"]
    item_root = candidate_root / row["candidate_dir"]

    pin_checks = []
    for name, entry in row["artifacts"].items():
        artifact_path = candidate_root / entry["path"]
        actual = sha(artifact_path)
        pin_checks.append({
            "name": name,
            "path": entry["path"],
            "expected_sha256": entry["sha256"],
            "actual_sha256": actual,
            "match": actual == entry["sha256"],
        })
    assert all(check["match"] for check in pin_checks), f"artifact pin mismatch: {asset_id}"

    blend_path = item_root / f"{asset_id}.blend"
    glb_path = item_root / f"{asset_id}.glb"
    blend_sha, glb_sha = sha(blend_path), sha(glb_path)
    assert glb_sha == row["glb_sha256"] and glb_path.stat().st_size == row["glb_bytes"]
    assert blend_sha == row["artifacts"]["blend"]["sha256"]

    view_manifest_path = item_root / "views/render-manifest.json"
    view_manifest = json_file(view_manifest_path)
    frames = view_manifest["frames"]
    assert view_manifest["turntable_frames"] == 0
    assert [frame["id"] for frame in frames] == EXPECTED_VIEWS
    fixed_views = []
    for frame in frames:
        image_path = item_root / "views" / frame["path"]
        size = png_size(image_path)
        actual = sha(image_path)
        fixed_views.append({
            "id": frame["id"],
            "path": rel(image_path),
            "sha256": actual,
            "manifest_sha256": frame["sha256"],
            "bytes": image_path.stat().st_size,
            "dimensions_px": size,
            "match": actual == frame["sha256"],
        })
        assert actual == frame["sha256"] and image_path.stat().st_size == frame["byte_length"]
        assert size == [frame["width"], frame["height"]]

    runtime_manifest_path = item_root / "runtime/evidence-manifest.json"
    runtime_manifest = json_file(runtime_manifest_path)
    assert runtime_manifest["subject"]["glb_sha256"] == glb_sha
    runtime_report_path = item_root / "runtime/runtime-report.json"
    runtime_report = json_file(runtime_report_path)
    assert runtime_report["source_glb_sha256"] == glb_sha
    assert runtime_report["status"] == "pass" and runtime_report["errors"] == []
    assert all(view["gl_error"] == 0 for view in runtime_report["views"])
    runtime_images = []
    for image in runtime_manifest["images"]:
        image_path = item_root / "runtime" / image["path"]
        actual = sha(image_path)
        size = png_size(image_path)
        assert actual == image["sha256"] and image_path.stat().st_size == image["bytes"]
        runtime_images.append({
            "path": rel(image_path),
            "sha256": actual,
            "bytes": image_path.stat().st_size,
            "dimensions_px": size,
        })

    export_path = item_root / "source-export.report.json"
    export = json_file(export_path)
    assert export["source_sha256"] == blend_sha and export["glb_sha256"] == glb_sha
    assert export["triangles_match"] and export["bounds_match"] and export["errors"] == []

    validator_path = item_root / "gltf-validator.report.json"
    validator = json_file(validator_path)
    assert validator["issues"]["numErrors"] == 0 and validator["issues"]["numWarnings"] == 0

    rebuilds = []
    for n in (1, 2):
        rebuild_path = item_root / f"reproducibility-{n}.report.json"
        rebuild = json_file(rebuild_path)
        out = candidate_root / "production" / rebuild["rebuilt_glb_path"].split("/production/", 1)[1]
        run_dir = out.parent.parent
        run_result = json_file(run_dir / "result.json")
        out_sha = sha(out)
        recorded_output = run_result["outputs"][f"{asset_id}.glb"]
        assert rebuild["status"] == "pass" and rebuild["errors"] == []
        assert rebuild["semantic_match"] is True
        assert rebuild["semantic_sha256"] == rebuild["rebuilt_semantic_sha256"]
        assert out_sha == rebuild["rebuilt_glb_sha256"] == recorded_output["sha256"] == glb_sha
        assert run_result["status"] == "succeeded" and run_result["returncode"] == 0
        rebuilds.append({
            "report_path": rel(rebuild_path),
            "report_sha256": sha(rebuild_path),
            "result_path": rel(run_dir / "result.json"),
            "result_sha256": sha(run_dir / "result.json"),
            "rebuilt_glb_path": rel(out),
            "rebuilt_glb_sha256": out_sha,
            "semantic_sha256": rebuild["semantic_sha256"],
            "semantic_match": True,
            "run_status": run_result["status"],
            "returncode": run_result["returncode"],
        })

    profile_contract_path = item_root / "profile-contract.json"
    profile = json_file(item_root / "profile-checker.report.json")
    assert profile["validation_profile"] == "static-stylized-v1"
    assert profile["rule_version"] == "2026-10-18.1"
    assert profile["profile_contract_status"] == "pass"
    profile_cmd = [
        "python3", "scripts/validate_candidate.py", f"{row['candidate_dir']}/candidate.json",
        "--root", ".", "--profile", "static-stylized-v1", "--profile-contract",
        f"{row['candidate_dir']}/profile-contract.json", "--json",
    ]
    profile_run = subprocess.run(profile_cmd, cwd=candidate_root, text=True, capture_output=True, check=False)
    current_profile = json.loads(profile_run.stdout)
    assert profile_run.returncode == 0
    assert current_profile["profile_contract_status"] == "pass"
    assert current_profile["valid"] is True and current_profile["approved_for_brief"] is False
    candidate = json_file(item_root / "candidate.json")

    independent_blender_path = REPO / f"qa/continuous-small-life-round13-20261018/batch-39/independent-review/evidence/blender/{asset_id}.json"
    blender_audit = json_file(independent_blender_path)
    assert blender_audit["blend_sha256"] == blend_sha and blender_audit["glb_sha256"] == glb_sha
    assert blender_audit["triangles_match"] and blender_audit["bounds_match_within_1e-4_m"]
    assert blender_audit["root_identity"] and blender_audit["source_cameras_lights"] == 0
    assert blender_audit["source_parts_all_closed_no_degenerate_finite_normals"]

    report["assets"].append({
        "asset_id": asset_id,
        "remote_ref": f"refs/heads/{row['branch']}",
        "remote_commit_sha": head,
        "candidate_dir": row["candidate_dir"],
        "blend": {"path": row["artifacts"]["blend"]["path"], "bytes": blend_path.stat().st_size, "sha256": blend_sha},
        "glb": {"path": rel(glb_path), "bytes": glb_path.stat().st_size, "triangles": row["triangles"], "sha256": glb_sha},
        "all_handoff_artifact_pins": {"count": len(pin_checks), "all_match": True, "checks": pin_checks},
        "fixed_views": {"manifest_path": rel(view_manifest_path), "exact_ids": EXPECTED_VIEWS, "turntable_frames": 0, "images": fixed_views},
        "runtime": {
            "report_path": rel(runtime_report_path),
            "evidence_manifest_path": rel(runtime_manifest_path),
            "browser_version": runtime_report["browser_version"],
            "three_version": runtime_report["three_version"],
            "renderer": runtime_report["unmasked_renderer"],
            "functional_status": runtime_report["status"],
            "hardware_performance_claim": False,
            "images": runtime_images,
        },
        "source_export": {
            "report_path": rel(export_path),
            "report_sha256": sha(export_path),
            "status": export["status"],
            "source_sha256_matches_blend": True,
            "glb_sha256_matches": True,
            "triangles_match": export["triangles_match"],
            "bounds_match": export["bounds_match"],
            "bounds_max_error_m": export["bounds_max_error_m"],
            "warnings": export["warnings"],
        },
        "khronos": {"report_path": rel(validator_path), "report_sha256": sha(validator_path), "num_errors": validator["issues"]["numErrors"], "num_warnings": validator["issues"]["numWarnings"]},
        "rebuilds": rebuilds,
        "independent_blender_audit": {"path": rel(independent_blender_path), "sha256": sha(independent_blender_path), "triangles_match": True, "bounds_match_within_1e-4_m": True, "source_closed_finite": True},
        "candidate_record": {"valid": row["candidate_record_valid"], "approved_for_brief": row["approved_for_brief"], "approval_status": candidate.get("approval", {}).get("status")},
        "static_profile": {"name": "static-stylized-v1", "rule_version": "2026-10-18.1", "contract_status": current_profile["profile_contract_status"], "validator_exit_code": profile_run.returncode, "candidate_record_valid": current_profile["valid"], "approved_for_brief": current_profile["approved_for_brief"], "approval_blockers": current_profile["approval_blockers"], "legacy_errors_preserved": current_profile["legacy_result"]["errors"], "contract_path": row["artifacts"]["profile_contract"]["path"], "contract_sha256": sha(profile_contract_path)},
    })

out_path = REPO / "qa/continuous-small-life-round13-20261018/batch-39/independent-review/evidence/hashes/batch39-integrity.json"
out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"status": "pass", "source_commit": SOURCE_COMMIT, "final_handoff_sha256": final_digest, "assets": [{"id": a["asset_id"], "remote_commit_sha": a["remote_commit_sha"], "artifact_pin_count": a["all_handoff_artifact_pins"]["count"], "fixed_views": len(a["fixed_views"]["images"]), "runtime_images": len(a["runtime"]["images"]), "rebuilds": len(a["rebuilds"])} for a in report["assets"]], "output": rel(out_path)}, ensure_ascii=False))
