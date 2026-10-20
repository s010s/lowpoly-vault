#!/usr/bin/env python3
"""Independent read-only replay of Batch 51 specification correction v001.

Run from the QA branch checkout, with a separate candidate checkout available:
  python3 qa/batch51-independent-20261019/evidence/differential-v001/verify_spec_correction.py --root /path/to/candidate-checkout

The script verifies original-byte preservation and independently decodes GLB
POSITION streams to compute bounds. It does not change any candidate status.
"""
from __future__ import annotations

import copy
import argparse
import hashlib
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OLD_HANDOFF = "6b5bc2793572361242544f7a19afd6bbd71243ab"
NEW_HANDOFF = "9000874083b6a6fb8e4e83dc95e4915801eecff4"
BASE = Path("assets/candidates/continuous-small-life-round17-20261018/batch-51")
CORRECTION = Path("production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001")
HANDOFF_PATH = Path("production/continuous-small-life-round17-20261018/work/batch-51/QA-HANDOFF.json")
EXPECTED = {
    "calcite-raft-deposit": {
        "nominal": 0.32,
        "old_nominal": 0.42,
        "sha256": "fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22",
    },
    "accretionary-lapilli-bed": {
        "nominal": 0.28,
        "old_nominal": 0.60,
        "sha256": "61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3",
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def checked(pin: dict) -> Path:
    path = ROOT / pin["path"]
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
        raise AssertionError(f"unsafe or escaping path: {pin['path']}")
    raw = path.read_bytes()
    if sha256(raw) != pin["sha256"]:
        raise AssertionError(f"sha256 mismatch: {pin['path']}")
    if "bytes" in pin and len(raw) != pin["bytes"]:
        raise AssertionError(f"byte-count mismatch: {pin['path']}")
    return path


def glb_position_bounds(path: Path):
    raw = path.read_bytes()
    magic, version, total_length = struct.unpack_from("<III", raw, 0)
    assert (magic, version, total_length) == (0x46546C67, 2, len(raw))
    offset = 12
    document = None
    binary = None
    while offset < len(raw):
        size, kind = struct.unpack_from("<II", raw, offset)
        payload = raw[offset + 8:offset + 8 + size]
        if kind == 0x4E4F534A:
            document = json.loads(payload.decode("utf-8"))
        elif kind == 0x004E4942:
            binary = payload
        offset += 8 + size
    assert document is not None and binary is not None
    # These files contain only identity mesh nodes; there is no hidden node transform.
    assert all(not any(k in node for k in ("matrix", "translation", "rotation", "scale"))
               for node in document.get("nodes", []))
    positions = []
    for mesh in document["meshes"]:
        for primitive in mesh["primitives"]:
            accessor = document["accessors"][primitive["attributes"]["POSITION"]]
            assert accessor["componentType"] == 5126 and accessor["type"] == "VEC3"
            view = document["bufferViews"][accessor["bufferView"]]
            stride = view.get("byteStride", 12)
            start = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
            assert stride >= 12
            for i in range(accessor["count"]):
                positions.append(struct.unpack_from("<3f", binary, start + i * stride))
    assert positions
    mins = [min(p[i] for p in positions) for i in range(3)]
    maxs = [max(p[i] for p in positions) for i in range(3)]
    return mins, maxs, [maxs[i] - mins[i] for i in range(3)], len(positions)


def main():
    global ROOT
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT,
                        help="candidate 9000874 checkout (defaults to this checkout)")
    ROOT = parser.parse_args().root.resolve()
    assert git("rev-parse", "HEAD") == NEW_HANDOFF, "run in the pinned candidate checkout"
    assert git("merge-base", "--is-ancestor", OLD_HANDOFF, NEW_HANDOFF) == ""
    assert git("rev-parse", "--show-toplevel") == str(ROOT)
    index_path = ROOT / CORRECTION / "index.json"
    index = read_json(index_path)
    assert index["source_handoff_commit"] == OLD_HANDOFF
    assert index["source_artifact_commit"] == "ee4e37b3c1cc49ab5e41c807c6ca8e1a155bbc6b"
    assert index["independent_review_commit"] == "925ff855ad0fcc3635cfc44a457101344ffddbde"
    assert set(item["asset_id"] for item in index["items"]) == set(EXPECTED)

    handoff = read_json(ROOT / HANDOFF_PATH)
    correction_pin = handoff["specification_correction"]
    assert correction_pin["path"] == str(CORRECTION / "index.json")
    assert sha256(index_path.read_bytes()) == correction_pin["sha256"]
    assert len(index_path.read_bytes()) == correction_pin["bytes"]

    # No production candidate artifact files changed: only handoff pointers and
    # the separately versioned specification-correction directory differ.
    changed = git("diff", "--name-status", OLD_HANDOFF, NEW_HANDOFF).splitlines()
    expected_status = {
        "M\tproduction/continuous-small-life-round17-20261018/work/batch-51/HANDOFF.md",
        "M\tproduction/continuous-small-life-round17-20261018/work/batch-51/QA-HANDOFF.json",
    }
    assert expected_status.issubset(set(changed))
    for row in changed:
        path = row.split("\t", 1)[1]
        if path not in {line.split("\t", 1)[1] for line in expected_status}:
            assert path.startswith(str(CORRECTION) + "/"), row
        assert not path.startswith(str(BASE) + "/"), row

    # Verify all 772 original files by SHA-256 and Git blob ID, both in the
    # current candidate tree and in the immediately preceding pinned handoff.
    preserved = read_json(checked(index["preservation_manifest"]))
    assert preserved["source_commit"] == OLD_HANDOFF
    preserved_count = 0
    for pin in preserved["files"]:
        path = checked(pin)
        raw = path.read_bytes()
        oid = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        assert oid == pin["git_blob_sha1"], pin["path"]
        assert git("rev-parse", f"{OLD_HANDOFF}:{pin['path']}") == pin["git_blob_sha1"], pin["path"]
        preserved_count += 1
    assert preserved_count == 772

    for pin in index["validation_evidence"].values():
        checked(pin)
    for pin in index["historical_handoff"].values():
        checked(pin)

    item_results = []
    for pin in index["items"]:
        asset = pin["asset_id"]
        spec = EXPECTED[asset]
        bundle = ROOT / BASE / asset / "r002"
        old_brief_path = bundle / "candidate-brief.json"
        old_brief = read_json(old_brief_path)
        assert old_brief["scale"]["meters"] == spec["old_nominal"]
        assert old_brief["frozen_construction_plan"]["nominal"] == spec["nominal"]
        config = read_json(bundle / "build-config.json")
        assert config["design"]["nominal"] == spec["nominal"]
        prompt = (bundle / "concepts" / "prompt.txt").read_text(encoding="utf-8")
        assert f"{spec['nominal']:.2f} m" in prompt

        corrected = read_json(checked(pin["supplemental_brief"]))
        freeze = read_json(checked(pin["derived_freeze"]))
        for freeze_pin in [*freeze["current_files"].values(), *freeze["original_evidence"].values()]:
            checked(freeze_pin)
        expected_brief = copy.deepcopy(old_brief)
        expected_brief["brief_version"] = "batch51-concept-plan-v002-specification-correction-v001"
        expected_brief["scale"]["meters"] = spec["nominal"]
        expected_brief["specification_correction"] = freeze["correction"]
        assert corrected == expected_brief
        assert corrected["criteria"] == old_brief["criteria"]
        assert corrected["required_stages"] == old_brief["required_stages"]
        assert freeze["historical_premodel_freeze"] is False
        assert freeze["modeling_already_completed"] is True
        assert freeze["correction"]["registered_candidate_changed"] is False
        assert freeze["correction"]["formal_candidate_approval"] is False

        glb_path = bundle / f"{asset}.glb"
        glb_sha = sha256(glb_path.read_bytes())
        assert glb_sha == pin["glb_sha256"] == spec["sha256"]
        mins, maxs, size, vertex_count = glb_position_bounds(glb_path)
        assert size == freeze["correction"]["measured_dimensions_glb_xyz_m"]
        metadata = read_json(checked(pin["supplemental_metadata"]))
        assert metadata["dimensions"] == size
        assert metadata["nominal_art_direction"]["meters"] == spec["nominal"]
        assert metadata["registered_candidate_brief_unchanged"]["sha256"] == sha256(old_brief_path.read_bytes())
        assert metadata["corrected_specification_brief"]["sha256"] == sha256((ROOT / pin["supplemental_brief"]["path"]).read_bytes())

        item_results.append({
            "asset_id": asset,
            "revision": "r002",
            "old_registered_nominal_m": spec["old_nominal"],
            "corrected_supplemental_nominal_m": spec["nominal"],
            "glb_sha256": glb_sha,
            "glb_bounds_min_xyz_m": mins,
            "glb_bounds_max_xyz_m": maxs,
            "glb_measured_dimensions_xyz_m": size,
            "decoded_position_vertices": vertex_count,
            "registered_candidate_brief_sha256": sha256(old_brief_path.read_bytes()),
            "supplemental_brief_sha256": sha256((ROOT / pin["supplemental_brief"]["path"]).read_bytes()),
            "supplemental_metadata_sha256": sha256((ROOT / pin["supplemental_metadata"]["path"]).read_bytes()),
            "derived_freeze_sha256": sha256((ROOT / pin["derived_freeze"]["path"]).read_bytes()),
            "specification_difference": "pass for additive nominal-scale description; unchanged original candidate contract remains pending",
        })

    output = {
        "status": "pass",
        "candidate_commit": NEW_HANDOFF,
        "prior_candidate_commit": OLD_HANDOFF,
        "prior_candidate_is_ancestor": True,
        "changed_path_count": len(changed),
        "all_changed_paths_confined_to_handoff_and_addendum": True,
        "protected_original_file_count": preserved_count,
        "protected_original_files_match_prior_git_blobs": True,
        "supplemental_index_matches_current_handoff_pin": True,
        "geometry_rebuilt_or_changed": False,
        "items": item_results,
        "formal_candidate_approval": False,
        "concept_exact_generation_time": "unknown; original --require-complete remains failed",
        "hardware_gpu_and_parent_scene": "not verified by this differential review",
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
