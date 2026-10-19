#!/usr/bin/env python3
"""Read-only integrity audit for the frozen batch-40 handoff and evidence."""
from __future__ import annotations

import hashlib
import json
import struct
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[5]
HANDOFF_PATH = Path("production/continuous-small-life-round14-20261018/work/batch-40/HANDOFF.json")
SCOPE_PATH = Path("production/continuous-small-life-round14-20261018/work/batch-40/QA-HANDOFF-SCOPE.json")
SOURCE_COMMIT = "af92e43e0b191f024c72232a40f0fe0f42996fa1"
IDS = ["sidneyia", "botrychium", "barrier-island", "diplocraterion-spreite-burrow"]
FRAME_NAMES = ["hero", "reversehero", "front", "side", "rear", "top", "clay", "silhouette"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def image_stats(path: Path, relpath: str):
    with Image.open(path) as im:
        im.load()
        bbox = im.getbbox()
        return {
            "path": relpath,
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "width": im.width,
            "height": im.height,
            "mode": im.mode,
            "nonempty_bbox": list(bbox) if bbox else None,
        }


def parse_glb(path: Path):
    raw = path.read_bytes()
    if len(raw) < 20:
        raise ValueError("GLB shorter than header plus JSON chunk")
    magic, version, declared_len = struct.unpack_from("<4sII", raw, 0)
    if magic != b"glTF" or version != 2 or declared_len != len(raw):
        raise ValueError(f"bad GLB header: magic={magic!r} version={version} length={declared_len}/{len(raw)}")
    json_len, json_type = struct.unpack_from("<II", raw, 12)
    if json_type != 0x4E4F534A or 20 + json_len > len(raw):
        raise ValueError("missing/invalid GLB JSON chunk")
    doc = json.loads(raw[20 : 20 + json_len].decode("utf-8").rstrip(" \t\r\n\0"))
    primitives = [p for m in doc.get("meshes", []) for p in m.get("primitives", [])]
    triangles = 0
    vertices = 0
    mins, maxs = [float("inf")] * 3, [float("-inf")] * 3
    for p in primitives:
        if p.get("mode", 4) != 4:
            raise ValueError(f"non-triangle primitive mode {p.get('mode')}")
        if "indices" in p:
            icount = doc["accessors"][p["indices"]]["count"]
            if icount % 3:
                raise ValueError("triangle index count is not divisible by three")
            triangles += icount // 3
        else:
            acount = doc["accessors"][p["attributes"]["POSITION"]]["count"]
            if acount % 3:
                raise ValueError("unindexed triangle vertex count is not divisible by three")
            triangles += acount // 3
        pos = doc["accessors"][p["attributes"]["POSITION"]]
        vertices += pos["count"]
        for i in range(3):
            mins[i] = min(mins[i], pos["min"][i])
            maxs[i] = max(maxs[i], pos["max"][i])
    return {
        "magic": magic.decode("ascii"),
        "version": version,
        "declared_length": declared_len,
        "json_chunk_bytes": json_len,
        "buffer_bytes": doc.get("buffers", [{}])[0].get("byteLength"),
        "meshes": len(doc.get("meshes", [])),
        "primitives": len(primitives),
        "triangles": triangles,
        "position_vertices_sum": vertices,
        "materials": len(doc.get("materials", [])),
        "textures": len(doc.get("textures", [])),
        "animations": len(doc.get("animations", [])),
        "extensions_required": doc.get("extensionsRequired", []),
        "position_bounds": {"min": mins, "max": maxs, "size": [maxs[i] - mins[i] for i in range(3)]},
        "sha256": sha256(path),
        "bytes": len(raw),
    }


def walk_pins(value):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
            yield value
        for v in value.values():
            yield from walk_pins(v)
    elif isinstance(value, list):
        for v in value:
            yield from walk_pins(v)


def verify_pin(relpath: str, expected: str, expected_bytes=None):
    p = ROOT / relpath
    result = {"path": relpath, "expected_sha256": expected, "exists": p.is_file()}
    if not p.is_file():
        result["match"] = False
        return result
    actual = sha256(p)
    result.update({"actual_sha256": actual, "bytes": p.stat().st_size, "match": actual == expected})
    if expected_bytes is not None:
        result["expected_bytes"] = expected_bytes
        result["bytes_match"] = p.stat().st_size == expected_bytes
    return result


def main():
    handoff = load_json(ROOT / HANDOFF_PATH)
    scope = load_json(ROOT / SCOPE_PATH)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    is_source_or_descendant = subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE_COMMIT, head], cwd=ROOT).returncode == 0
    if not is_source_or_descendant:
        raise SystemExit(f"audit must run at the pinned source commit or one of its descendants; HEAD is {head}")
    if handoff.get("batch") != "batch-40" or handoff.get("branch") != "candidate/small-life-batch40-20261018":
        raise SystemExit("handoff identity mismatch")
    if scope.get("expected_asset_ids") != IDS or scope.get("expected_source_commit") != "cf7565ed2c4ca70c4ffed567aa32ec0aafd40a0b":
        raise SystemExit("frozen QA handoff scope mismatch")
    if [a["asset_id"] for a in handoff["assets"]] != IDS:
        raise SystemExit("handoff asset identity mismatch")

    pinned = {}
    for entry in walk_pins(handoff):
        pinned[(entry["path"], entry["sha256"])] = entry
    pins = [verify_pin(p, h, entry.get("bytes")) for (p, h), entry in sorted(pinned.items())]

    assets = []
    for item in handoff["assets"]:
        asset_id = item["asset_id"]
        candidate = load_json(ROOT / item["candidate"]["path"])
        source_scene = load_json(ROOT / item["source_scene"]["path"])
        source_export = load_json(ROOT / item["source_export"]["path"])
        reproducibility = load_json(ROOT / item["two_rebuilds"]["path"])
        profile = load_json(ROOT / item["profile_result"]["path"])
        legacy = load_json(ROOT / item["legacy_result"]["path"])
        metadata = load_json(ROOT / item["metadata"]["path"])
        base = Path(item["glb"]["path"]).parent
        view_manifest = load_json(ROOT / item["view_manifest"]["path"])
        runtime_single = load_json(ROOT / base / "runtime/single.json")
        runtime_scene = load_json(ROOT / base / "runtime/scene.json")
        glb = parse_glb(ROOT / item["glb"]["path"])
        blend_pin = verify_pin(item["blend"]["path"], item["blend"]["sha256"], item["blend"]["bytes"])
        glb_pin = verify_pin(item["glb"]["path"], item["glb"]["sha256"], item["glb"]["bytes"])

        if candidate.get("asset_id") != asset_id or candidate.get("revision") != item["revision"]:
            raise SystemExit(f"candidate identity mismatch for {asset_id}")
        if candidate["artifacts"]["glb"]["sha256"] != scope["expected_glb_sha256_by_asset"][asset_id]:
            raise SystemExit(f"candidate GLB hash disagrees with frozen scope for {asset_id}")
        if glb["sha256"] != scope["expected_glb_sha256_by_asset"][asset_id] or glb["triangles"] != item["triangles"]:
            raise SystemExit(f"actual GLB differs from handoff pin/triangle count for {asset_id}")
        if not blend_pin["match"] or not glb_pin["match"]:
            raise SystemExit(f"Blend/GLB checksum mismatch for {asset_id}")
        if source_scene.get("status") != "pass" or source_scene.get("source_sha256") != item["blend"]["sha256"]:
            raise SystemExit(f"source-scene evidence mismatch for {asset_id}")
        if source_export.get("errors") or not source_export.get("triangles_match") or not source_export.get("bounds_match"):
            raise SystemExit(f"source-export evidence mismatch for {asset_id}")
        if source_export.get("glb_sha256") != glb["sha256"] or source_export.get("source_sha256") != blend_pin["actual_sha256"]:
            raise SystemExit(f"source-export hashes mismatch for {asset_id}")
        if reproducibility.get("status") != "pass" or reproducibility.get("delivered_glb_sha256") != glb["sha256"]:
            raise SystemExit(f"rebuild evidence mismatch for {asset_id}")
        if len(reproducibility.get("runs", [])) != 2 or not all(r.get("byte_match") and r.get("semantic_match") and r.get("glb_sha256") == glb["sha256"] for r in reproducibility["runs"]):
            raise SystemExit(f"two-rebuild result mismatch for {asset_id}")
        source_frames = [f for f in view_manifest["frames"] if f.get("origin") == "source"]
        if view_manifest.get("turntable_frames") != 0 or [Path(f["path"]).stem.removeprefix("preview-") for f in source_frames] != FRAME_NAMES:
            raise SystemExit(f"fixed source-view contract mismatch for {asset_id}")
        if view_manifest.get("glb_sha256") != glb["sha256"]:
            raise SystemExit(f"view manifest is not bound to exact GLB for {asset_id}")

        fixed = []
        for frame in source_frames:
            p = ROOT / frame["path"]
            audited = image_stats(p, frame["path"])
            audited["manifest_sha256"] = frame["sha256"]
            audited["manifest_bytes"] = frame["bytes"]
            audited["matches_manifest"] = audited["sha256"] == frame["sha256"] and audited["bytes"] == frame["bytes"] and audited["width"] == frame["width"] and audited["height"] == frame["height"]
            fixed.append(audited)
        sheets = []
        for sh in item["source_contact_sheet"], item["runtime_contact_sheet"]:
            audited = image_stats(ROOT / sh["path"], sh["path"])
            audited["manifest_sha256"] = sh["sha256"]
            audited["manifest_bytes"] = sh["bytes"]
            audited["matches_manifest"] = audited["sha256"] == sh["sha256"] and audited["bytes"] == sh["bytes"]
            sheets.append(audited)

        runtime_images = []
        for mode, report in (("single", runtime_single), ("scene", runtime_scene)):
            if mode == "scene" and (report.get("status") != "pass" or report.get("errors") or report.get("failed")):
                raise SystemExit(f"runtime scene report did not pass for {asset_id}")
            if report.get("renderer", "").find("SwiftShader") < 0 or not report.get("webgl2"):
                raise SystemExit(f"runtime renderer disclosure mismatch for {asset_id}")
            for view in report["views"]:
                relpath = (base / "runtime" / view["path"]).as_posix()
                audited = image_stats(ROOT / relpath, relpath)
                audited.update({"mode": mode, "view": view["view"], "expected_sha256": view["sha256"], "expected_extent_px": view["extent"], "sha256_matches": audited["sha256"] == view["sha256"]})
                runtime_images.append(audited)

        barrier_context = None
        if asset_id == "barrier-island":
            context = load_json(ROOT / "production/continuous-small-life-round14-20261018/work/batch-40/barrier-island/r001/barrier-context.json")
            if context.get("status") != "pass" or context.get("glb_sha256") != glb["sha256"] or context.get("errors"):
                raise SystemExit("barrier context evidence mismatch")
            context_images = []
            for image in context["views"]:
                relpath = image["path"]
                audited = image_stats(ROOT / relpath, relpath)
                audited.update({"expected_sha256": image["sha256"], "expected_bytes": image["bytes"], "matches_context_report": audited["sha256"] == image["sha256"] and audited["bytes"] == image["bytes"]})
                context_images.append(audited)
            barrier_context = {
                "report_path": "production/continuous-small-life-round14-20261018/work/batch-40/barrier-island/r001/barrier-context.json",
                "sha256": sha256(ROOT / "production/continuous-small-life-round14-20261018/work/batch-40/barrier-island/r001/barrier-context.json"),
                "datum_m": context["datum"],
                "scope": context["scope"],
                "images": context_images,
            }

        assets.append({
            "asset_id": asset_id,
            "revision": item["revision"],
            "selected_attempt": item["selected_attempt"],
            "candidate_checkpoint_sha": item["candidate_checkpoint_sha"],
            "candidate_checkpoint_is_ancestor": subprocess.run(["git", "merge-base", "--is-ancestor", item["candidate_checkpoint_sha"], head], cwd=ROOT).returncode == 0,
            "candidate_path": item["candidate"]["path"],
            "candidate_sha256": item["candidate"]["sha256"],
            "candidate_valid": item["candidate_valid"],
            "approved_for_brief": item["approved_for_brief"],
            "blend": {"path": item["blend"]["path"], "sha256": blend_pin["actual_sha256"], "bytes": blend_pin["bytes"]},
            "glb": {"path": item["glb"]["path"], **glb},
            "source_scene": {"path": item["source_scene"]["path"], "sha256": item["source_scene"]["sha256"], "status": source_scene["status"], "source_authored_vertices": source_scene["source_authored_vertices"], "source_evaluated_vertices": source_scene["source_evaluated_vertices"], "parts": [{"name": p["name"], "triangles": p["triangles"], "boundary_edges": p.get("boundary_edges"), "nonmanifold_edges": p.get("nonmanifold_edges")} for p in source_scene["parts"]]},
            "source_export": {"path": item["source_export"]["path"], "sha256": item["source_export"]["sha256"], "status": source_export["status"], "errors": source_export["errors"], "warnings": source_export["warnings"], "triangles_match": source_export["triangles_match"], "bounds_match": source_export["bounds_match"], "bounds_max_error_m": source_export["bounds_max_error_m"]},
            "rebuilds": {"path": item["two_rebuilds"]["path"], "sha256": item["two_rebuilds"]["sha256"], "status": reproducibility["status"], "byte_identical": item["two_rebuilds_byte_identical"], "semantic_sha256": reproducibility["semantic_sha256"], "run_glb_sha256": [r["glb_sha256"] for r in reproducibility["runs"]]},
            "profile": {"path": item["profile_result"]["path"], "sha256": item["profile_result"]["sha256"], "valid": profile["valid"], "approved_for_brief": profile["approved_for_brief"], "gpu_blocker": any("gpu: unknown" in x for x in profile["approval_blockers"])},
            "legacy": {"path": item["legacy_result"]["path"], "sha256": item["legacy_result"]["sha256"], "valid": legacy["valid"], "errors": legacy["errors"]},
            "view_manifest": {"path": item["view_manifest"]["path"], "sha256": item["view_manifest"]["sha256"], "turntable_frames": view_manifest["turntable_frames"], "fixed_views": fixed, "contact_sheets": sheets},
            "runtime": {"single_report": (base / "runtime/single.json").as_posix(), "scene_report": (base / "runtime/scene.json").as_posix(), "renderer": runtime_scene["renderer"], "three": runtime_scene["three"], "single_views": len(runtime_single["views"]), "scene_views": len(runtime_scene["views"]), "instances": runtime_scene["instances"], "scene_draw_calls": runtime_scene["views"][0]["calls"], "scene_triangles": runtime_scene["views"][0]["triangles"], "image_evidence": runtime_images},
            "barrier_context": barrier_context,
        })

    result = {
        "schema_version": 1,
        "kind": "batch40_independent_readonly_artifact_audit",
        "source_commit": SOURCE_COMMIT,
        "source_branch": handoff["branch"],
        "source_parent": handoff["parent_thread_id"],
        "handoff": {"path": HANDOFF_PATH.as_posix(), "sha256": sha256(ROOT / HANDOFF_PATH)},
        "scope": {"path": SCOPE_PATH.as_posix(), "sha256": sha256(ROOT / SCOPE_PATH)},
        "profile": handoff["profile"],
        "pinned_artifact_count": len(pins),
        "pinned_artifacts": pins,
        "all_pinned_artifacts_match": all(p["match"] and p.get("bytes_match", True) for p in pins),
        "assets": assets,
    }
    out = ROOT / "qa/continuous-small-life-round14-20261018/batch-40/independent-review/evidence/artifact-audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not result["all_pinned_artifacts_match"]:
        raise SystemExit("one or more pinned artifacts did not match; inspect artifact-audit.json")
    print(f"wrote {out.relative_to(ROOT)}; {len(pins)} handoff pins matched")


if __name__ == "__main__":
    main()
