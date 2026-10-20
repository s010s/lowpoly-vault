#!/usr/bin/env python3
"""Verify the pinned Batch 51 handoff and all selected candidate evidence hashes.

Run from any directory with Python 3 and Git available:
  python3 qa/batch51-independent-20261019/evidence/verify_inputs.py

This reads the repository only. It does not edit model or production files.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HANDOFF = Path(
    "production/continuous-small-life-round17-20261018/work/batch-51/QA-HANDOFF.json"
)
BASE = Path("assets/candidates/continuous-small-life-round17-20261018/batch-51")
SOURCE = "ee4e37b3c1cc49ab5e41c807c6ca8e1a155bbc6b"
HANDOFF_COMMIT = "6b5bc2793572361242544f7a19afd6bbd71243ab"
EXPECTED = {
    "dicranurus": ("r001", "ffe61e0340399eb1bd41cb198ba5abc20edae439db44e3c21d4cf6d9e032bd65"),
    "calcite-raft-deposit": ("r002", "fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22"),
    "accretionary-lapilli-bed": ("r002", "61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3"),
    "conichnus-conical-burrow": ("r001", "34948b0738264195544dd24ff377a1b0f3b92a93a1e34ab07d66647235388042"),
}
VIEWS = {"hero", "reversehero", "front", "side", "rear", "top", "clay", "silhouette"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def verify_bundle_checksums(bundle: Path) -> int:
    manifest = bundle / "bundle-files.sha256"
    if not manifest.is_file():
        fail(f"missing {manifest.relative_to(ROOT)}")
    checked = 0
    for line_no, line in enumerate(manifest.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            expected_hash, relpath = line.split(None, 1)
        except ValueError:
            fail(f"malformed bundle checksum line {manifest}:{line_no}")
        relpath = relpath.lstrip("* ")
        path = bundle / relpath
        if not path.is_file():
            fail(f"bundle file missing: {path.relative_to(ROOT)}")
        if sha256(path) != expected_hash:
            fail(f"bundle hash mismatch: {path.relative_to(ROOT)}")
        checked += 1
    return checked


def main() -> None:
    if not (ROOT / ".git").exists():
        fail("repository root not found")
    if git("rev-parse", f"{SOURCE}^{{commit}}") != SOURCE:
        fail("source commit object mismatch")
    if git("rev-parse", f"{HANDOFF_COMMIT}^{{commit}}") != HANDOFF_COMMIT:
        fail("candidate handoff commit object mismatch")
    if git("rev-parse", f"{HANDOFF_COMMIT}^") != SOURCE:
        fail("handoff commit is not directly based on the pinned artifact commit")
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", HANDOFF_COMMIT, "HEAD"],
        cwd=ROOT,
        check=True,
    )

    handoff = json.loads((ROOT / HANDOFF).read_text())
    expected_ids = list(EXPECTED)
    if handoff.get("source_commit") != SOURCE:
        fail("handoff source commit mismatch")
    if handoff.get("branch") != "candidate/small-life-batch51-concept-20261019":
        fail("handoff branch mismatch")
    if [item.get("asset_id") for item in handoff.get("items", [])] != expected_ids:
        fail("handoff asset order/identity mismatch")

    report_items = []
    for item in handoff["items"]:
        asset = item["asset_id"]
        revision, expected_glb = EXPECTED[asset]
        if item.get("revision") != revision or item.get("glb_sha256") != expected_glb:
            fail(f"handoff selection/hash mismatch for {asset}")
        bundle = ROOT / BASE / asset / revision
        checked_roles = 0
        for role, record in item.get("files", {}).items():
            path = ROOT / record["path"]
            if not path.is_file():
                fail(f"handoff {asset}.{role} missing: {record['path']}")
            if sha256(path) != record["sha256"]:
                fail(f"handoff hash mismatch: {record['path']}")
            if "bytes" in record and path.stat().st_size != record["bytes"]:
                fail(f"handoff byte length mismatch: {record['path']}")
            checked_roles += 1

        glb = bundle / f"{asset}.glb"
        if sha256(glb) != expected_glb:
            fail(f"selected GLB changed: {asset}")
        checksum_count = verify_bundle_checksums(bundle)

        candidate_manifest = bundle / "candidate-proof/render-manifest.json"
        manifest = json.loads(candidate_manifest.read_text())
        if manifest.get("source_glb_sha256") != expected_glb:
            fail(f"candidate view manifest is not bound to selected GLB: {asset}")
        frames = manifest.get("frames", [])
        if {frame.get("id") for frame in frames} != VIEWS or len(frames) != 8:
            fail(f"candidate fixed-eight coverage mismatch: {asset}")
        view_hashes = {}
        for frame in frames:
            image = candidate_manifest.parent / frame["path"]
            if not image.is_file() or sha256(image) != frame["sha256"]:
                fail(f"candidate view hash mismatch: {asset}/{frame.get('id')}")
            view_hashes[frame["id"]] = frame["sha256"]

        concept = json.loads((bundle / "concept-evidence.json").read_text())
        generation = json.loads((bundle / "concepts/generation-record.json").read_text())
        inspection = json.loads((bundle / "concepts/inspection.json").read_text())
        model_start = json.loads((bundle / "model-start.json").read_text())
        original = bundle / "concepts/original.png"
        prompt = bundle / "concepts/prompt.txt"
        if sha256(original) != generation.get("image_sha256"):
            fail(f"original concept hash mismatch: {asset}")
        if sha256(prompt) != generation.get("prompt_sha256"):
            fail(f"concept prompt hash mismatch: {asset}")
        if inspection.get("sha256") != sha256(original):
            fail(f"concept inspection points at a different image: {asset}")
        if concept.get("chronology", {}).get("concept_generated_at") is not None:
            fail(f"unknown generation time was replaced: {asset}")
        if generation.get("generated_at") != "not separately disclosed by tool; invocation/result occurred in this task before capture":
            fail(f"generation time attestation changed: {asset}")
        captured = generation.get("captured_at")
        inspected = inspection.get("inspected_at")
        modeled = model_start.get("modeling_started_at")
        if not (captured and inspected and modeled and captured < inspected < modeled):
            fail(f"capture/view/model order not established by records: {asset}")

        runtime = json.loads((bundle / "runtime/runtime-report.json").read_text())
        if runtime.get("source_glb_sha256") != expected_glb:
            fail(f"runtime is not bound to selected GLB: {asset}")
        runtime_images = {}
        for image_name in ["hero", "reversehero", "front", "side", "top", "near", "scene-9-copies"]:
            image = bundle / f"runtime/{image_name}.png"
            if not image.is_file():
                fail(f"runtime image missing: {asset}/{image_name}")
            runtime_images[image_name] = sha256(image)

        conichnus_diagnostics = None
        if asset == "conichnus-conical-burrow":
            diagnostic_root = bundle / "diagnostics"
            diagnostic_manifest = json.loads(
                (diagnostic_root / "diagnostic-manifest.json").read_text()
            )
            if diagnostic_manifest.get("source_glb_sha256") != expected_glb:
                fail("gray diagnostic views are not bound to the selected Conichnus GLB")
            diagnostic_hashes = {}
            for frame in diagnostic_manifest.get("frames", []):
                image = diagnostic_root / frame["path"]
                if not image.is_file() or sha256(image) != frame["sha256"]:
                    fail(f"Conichnus diagnostic image hash mismatch: {frame.get('id')}")
                if frame.get("geometry_modified") != (frame.get("id") == "gray-section"):
                    fail("Conichnus section diagnostic geometry disclosure mismatch")
                diagnostic_hashes[frame["id"]] = frame["sha256"]
            if set(diagnostic_hashes) != {"gray-top", "gray-oblique", "gray-section"}:
                fail("Conichnus gray diagnostics must include top, oblique and section")
            probe_path = bundle / "negative-cavity-probe.json"
            probe = json.loads(probe_path.read_text())
            if probe.get("glb_sha256") != expected_glb or not probe.get("negative_cavity_confirmed"):
                fail("Conichnus stored ray probe is not bound to the selected GLB or did not confirm a cavity")
            conichnus_diagnostics = {
                "source_unchanged": diagnostic_manifest.get("source_unchanged"),
                "sha256_by_view": diagnostic_hashes,
                "maker_probe_sha256": sha256(probe_path),
            }

        report_items.append(
            {
                "asset_id": asset,
                "revision": revision,
                "glb_sha256": expected_glb,
                "handoff_roles_verified": checked_roles,
                "bundle_files_verified": checksum_count,
                "candidate_proof_sha256_by_view": view_hashes,
                "concept_sha256": sha256(original),
                "prompt_sha256": sha256(prompt),
                "concept_capture_at": captured,
                "concept_inspected_at": inspected,
                "modeling_started_at": modeled,
                "concept_generated_at": None,
                "runtime_report_glb_sha256": runtime["source_glb_sha256"],
                "runtime_image_sha256": runtime_images,
                "targeted_diagnostics": conichnus_diagnostics,
            }
        )

    protected = subprocess.check_output(
        [
            "git",
            "diff",
            "--name-only",
            HANDOFF_COMMIT,
            "--",
            "assets/candidates/continuous-small-life-round17-20261018/batch-51",
            "production/continuous-small-life-round17-20261018",
        ],
        cwd=ROOT,
        text=True,
    ).strip()
    if protected:
        fail("candidate/model or production tree changed relative to pinned handoff commit")

    print(
        json.dumps(
            {
                "status": "pass",
                "source_commit": SOURCE,
                "candidate_handoff_commit": HANDOFF_COMMIT,
                "selected_asset_count": len(report_items),
                "candidate_or_production_changes_since_handoff": [],
                "items": report_items,
                "limitations": [
                    "Hash verification does not establish visual, scientific, GPU hardware, or parent-scene acceptance.",
                    "Exact ImageGen generation times remain unknown and are not reconstructed.",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
