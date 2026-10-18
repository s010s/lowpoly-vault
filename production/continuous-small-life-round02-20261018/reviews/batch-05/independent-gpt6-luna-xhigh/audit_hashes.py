#!/usr/bin/env python3
"""Read-only evidence-integrity audit for frozen Batch 05 candidate bundles."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HANDOFF = ROOT / "production/continuous-small-life-round02-20261018/work/batch-05/HANDOFF.json"
ASSETS = ("goniophyllum", "halysites", "marrella", "proteroctopus")


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def same(path, expected):
    return path.is_file() and sha(path) == expected


def main():
    handoff = read(HANDOFF)
    by_id = {a["asset_id"]: a for a in handoff["assets"]}
    errors = []
    for name in ASSETS:
        entry = by_id[name]
        glb, blend, candidate = (ROOT / entry[key]["path"] for key in ("glb", "blend", "candidate"))
        view_manifest = ROOT / entry["view_manifest"]["path"]
        source_sheet = ROOT / entry["source_contact_sheet"]["path"]
        runtime_sheet = ROOT / entry["runtime_contact_sheet"]["path"]
        bundle = glb.parent
        cand = read(candidate)
        vm = read(view_manifest)
        validator = read(bundle / "gltf-validator.report.json")
        runtime = read(ROOT / cand["technical_evidence"]["runtime"]["path"])
        scene = read(ROOT / cand["technical_evidence"]["scene"]["path"])
        checks = {
            "glb": same(glb, entry["glb"]["sha256"]) and glb.stat().st_size == entry["glb"]["bytes"],
            "blend": same(blend, entry["blend"]["sha256"]) and blend.stat().st_size == entry["blend"]["bytes"],
            "candidate": same(candidate, entry["candidate"]["sha256"]) and candidate.stat().st_size == entry["candidate"]["bytes"],
            "view_manifest": same(view_manifest, entry["view_manifest"]["sha256"]),
            "source_contact": same(source_sheet, entry["source_contact_sheet"]["sha256"]),
            "runtime_contact": same(runtime_sheet, entry["runtime_contact_sheet"]["sha256"]),
            "manifest_glb_binding": vm.get("glb_sha256") == entry["glb"]["sha256"] and vm.get("turntable_frames") == 0,
            "validator": validator.get("issues", {}).get("numErrors") == 0 and validator.get("issues", {}).get("numWarnings") == 0,
            "runtime": runtime.get("status") == "pass" and runtime.get("glb_sha256") == entry["glb"]["sha256"] and not runtime.get("errors") and not runtime.get("failed"),
            "scene": scene.get("status") == "pass" and scene.get("glb_sha256") == entry["glb"]["sha256"] and not scene.get("errors") and not scene.get("failed"),
        }
        frame_errors = []
        for frame in vm["frames"]:
            path = ROOT / frame["path"]
            if not path.is_file() or path.stat().st_size != frame["bytes"] or sha(path) != frame["sha256"]:
                frame_errors.append(frame["path"])
        checks["20_frame_records"] = len(vm["frames"]) == 20 and not frame_errors
        runtime_counts = {len(vm["frames"]), len(vm["sheets"])}
        failed = [key for key, value in checks.items() if not value]
        failed.extend(f"frame:{p}" for p in frame_errors)
        print(f"{name}: GLB {glb.stat().st_size}B {sha(glb)}; blend {sha(blend)}; candidate {sha(candidate)}; turntable={vm['turntable_frames']}; frame/sheet records={len(vm['frames'])}/{len(vm['sheets'])}; validator=0/0; runtime={runtime['status']}; scene={scene['status']}; {'PASS' if not failed else 'FAIL '+','.join(failed)}")
        errors.extend(f"{name}:{e}" for e in failed)
    if errors:
        print("Errors:", "; ".join(errors))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
