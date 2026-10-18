#!/usr/bin/env python3
"""Recompute candidate/handoff and fixed-view integrity without modifying it."""
import argparse
import hashlib
import json
from pathlib import Path

REQUIRED_SOURCE_VIEWS = {"hero", "reversehero", "front", "side", "rear", "top", "clay", "silhouette"}
REQUIRED_RUNTIME_VIEWS = {"hero", "reversehero", "front", "side", "rear", "top", "bottom"}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("candidate_root", type=Path)
    p.add_argument("output_json", type=Path)
    a = p.parse_args()
    root = a.candidate_root.resolve()
    handoff_path = root / "production/continuous-small-life-round04-20261018/work/batch-11/HANDOFF.json"
    handoff = json.loads(handoff_path.read_text())
    result = {"handoff_sha256": digest(handoff_path), "asset_results": [], "errors": []}
    for asset in handoff["assets"]:
        aid = asset["asset_id"]
        checked = []
        def check_file(label, entry):
            if not isinstance(entry, dict) or not entry.get("path") or not entry.get("sha256"):
                return
            path = root / entry["path"]
            exists = path.is_file()
            sha = digest(path) if exists else None
            nbytes = path.stat().st_size if exists else None
            ok = exists and sha == entry["sha256"] and ("bytes" not in entry or nbytes == entry["bytes"])
            checked.append({"label": label, "path": entry["path"], "exists": exists, "bytes": nbytes,
                            "sha256_expected": entry["sha256"], "sha256_actual": sha, "status": "pass" if ok else "fail"})
            if not ok:
                result["errors"].append(f"{aid}.{label}: file/hash/bytes mismatch")

        for key, value in asset.items():
            if key == "asset_id":
                continue
            if isinstance(value, dict) and value.get("path"):
                check_file(key, value)
        freeze_path = root / f"production/continuous-small-life-round04-20261018/work/batch-11/{aid}/r001/freeze.json"
        freeze = json.loads(freeze_path.read_text())
        check_file("freeze", {"path": str(freeze_path.relative_to(root)), "sha256": digest(freeze_path), "bytes": freeze_path.stat().st_size})
        for group_name in ("files", "evidence"):
            for label, entry in freeze.get(group_name, {}).items():
                check_file(f"freeze.{group_name}.{label}", entry)
        glb_sha = asset["glb"]["sha256"]
        attempt = handoff["final_attempts"][aid]
        view_path = root / f"assets/candidates/continuous-small-life-round04-20261018/batch-11/{aid}/r001/{attempt}/{aid}/view-manifest.json"
        view = json.loads(view_path.read_text())
        source_names = {Path(x["path"]).stem.removeprefix("preview-") for x in view["frames"] if x["origin"] == "source"}
        runtime = [x for x in view["frames"] if x["origin"] == "exact-glb-runtime"]
        runtime_480 = {Path(x["path"]).stem.removeprefix("single-") for x in runtime
                       if Path(x["path"]).stem in {f"single-{v}" for v in REQUIRED_RUNTIME_VIEWS}}
        pixel_views = {Path(x["path"]).stem for x in runtime if Path(x["path"]).stem in {"single-80px", "single-160px", "single-240px"}}
        source_ok = source_names == REQUIRED_SOURCE_VIEWS
        if not source_ok:
            result["errors"].append(f"{aid}: fixed source views differ from profile contract")
        runtime_ok = (view["glb_sha256"] == glb_sha and view["turntable_frames"] == 0
                      and len(runtime) == 12 and REQUIRED_RUNTIME_VIEWS.issubset(runtime_480)
                      and pixel_views == {"single-80px", "single-160px", "single-240px"})
        if not runtime_ok:
            result["errors"].append(f"{aid}: runtime image/GLB/zero-turntable pin mismatch")
        frame_check = []
        for frame in view["frames"]:
            fpath = root / frame["path"]
            exists = fpath.is_file()
            sha = digest(fpath) if exists else None
            size = fpath.stat().st_size if exists else None
            ok = exists and sha == frame["sha256"] and size == frame["bytes"]
            frame_check.append({"path": frame["path"], "origin": frame["origin"], "bytes": size,
                                "sha256": sha, "status": "pass" if ok else "fail"})
            if not ok:
                result["errors"].append(f"{aid}: frame file integrity mismatch at {frame['path']}")
        runtime_json_path = root / f"assets/candidates/continuous-small-life-round04-20261018/batch-11/{aid}/r001/{attempt}/{aid}/runtime/single.json"
        scene_json_path = runtime_json_path.with_name("scene.json")
        runtime_json = json.loads(runtime_json_path.read_text())
        scene_json = json.loads(scene_json_path.read_text())
        freeze_runtime = freeze["evidence"]["runtime"]
        freeze_scene = freeze["evidence"]["scene"]
        if digest(runtime_json_path) != freeze_runtime["sha256"] or digest(scene_json_path) != freeze_scene["sha256"]:
            result["errors"].append(f"{aid}: runtime/scene JSON differs from freeze hash")
        runtime_ok = runtime_ok and runtime_json.get("status") == "pass" and not runtime_json.get("errors") and runtime_json.get("glb_sha256") == glb_sha
        scene_ok = scene_json.get("status") == "pass" and not scene_json.get("errors") and scene_json.get("glb_sha256") == glb_sha
        runtime_ok = runtime_ok and all(x.get("triangles", 0) > 0 for x in runtime_json.get("views", []))
        scene_ok = scene_ok and scene_json.get("instances") == 6 and all(x.get("triangles", 0) > 0 for x in scene_json.get("views", []))
        if not runtime_ok or not scene_ok:
            result["errors"].append(f"{aid}: runtime single/scene result does not pass exact GLB")
        result["asset_results"].append({
            "asset_id": aid,
            "checkpoint": asset["candidate_checkpoint_sha"],
            "glb_sha256": glb_sha,
            "blend_sha256": asset["blend"]["sha256"],
            "checked_handoff_files": checked,
            "source_views": sorted(source_names),
            "source_views_status": "pass" if source_ok else "fail",
            "runtime_frames": len(runtime),
            "runtime_480_views": sorted(runtime_480),
            "runtime_80_160_240_present": sorted(pixel_views),
            "turntable_frames": view["turntable_frames"],
            "runtime_single_status": runtime_json.get("status"),
            "runtime_scene_status": scene_json.get("status"),
            "runtime_single_json_sha256": digest(runtime_json_path),
            "runtime_scene_json_sha256": digest(scene_json_path),
            "view_manifest_sha256": digest(view_path),
            "frame_results": frame_check,
            "status": "pass" if source_ok and runtime_ok and scene_ok and all(x["status"] == "pass" for x in checked + frame_check) else "fail",
        })
    result["status"] = "pass" if not result["errors"] and all(x["status"] == "pass" for x in result["asset_results"]) else "fail"
    a.output_json.parent.mkdir(parents=True, exist_ok=True)
    a.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": result["status"], "assets": len(result["asset_results"]), "errors": result["errors"]}, ensure_ascii=False))
    raise SystemExit(0 if result["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
