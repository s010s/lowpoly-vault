#!/usr/bin/env python3
"""Independently hash the frozen fish artifacts and verify exact-GLB render manifests."""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

ROOT = Path.cwd().resolve()
PACKAGE = ROOT / "production/concept-small-fish-20261019"
OUTPUT = ROOT / "qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence"
CANDIDATE_COMMIT = "3196c36c51d5a14487dcd4ebbebcafc00aa933d7"
ASSETS = ("metaspriggina", "falcatus", "pteraspis", "dorypterus")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        header = stream.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"Not a PNG with an IHDR chunk: {path}")
    return struct.unpack(">II", header[16:24])


def add_record(records: list[dict], rel: str, role: str) -> Path:
    path = ROOT / rel
    if not path.is_file():
        raise FileNotFoundError(path)
    records.append({"path": rel, "role": role, "bytes": path.stat().st_size, "sha256": digest(path)})
    return path


def verify_render_manifest(manifest_path: Path, glb_sha: str) -> dict:
    manifest = json.loads(manifest_path.read_text())
    checks = {"source_glb_sha256_matches": manifest.get("source_glb_sha256") == glb_sha, "frames": []}
    for frame in manifest["frames"]:
        image_path = manifest_path.parent / frame["path"]
        actual_hash = digest(image_path)
        actual_bytes = image_path.stat().st_size
        actual_width, actual_height = png_size(image_path)
        checks["frames"].append({
            "id": frame["id"],
            "path": str(image_path.relative_to(ROOT)),
            "sha256_matches": actual_hash == frame["sha256"],
            "bytes_match": actual_bytes == frame["byte_length"],
            "dimensions_match": [actual_width, actual_height] == [frame["width"], frame["height"]],
            "dimensions": [actual_width, actual_height],
        })
    checks["all_frames_match"] = all(
        f["sha256_matches"] and f["bytes_match"] and f["dimensions_match"] for f in checks["frames"]
    )
    return checks


def main() -> None:
    records: list[dict] = []
    checks = {"candidate_commit": CANDIDATE_COMMIT, "assets": {}}
    for rel, role in (
        ("production/concept-small-fish-20261019/HANDOFF.md", "handoff"),
        ("production/concept-small-fish-20261019/README.md", "batch-scope"),
        ("production/concept-small-fish-20261019/concept-original.png", "original-concept"),
        ("production/concept-small-fish-20261019/concept-prompt.txt", "original-prompt"),
        ("production/concept-small-fish-20261019/concept-generation.json", "generation-record"),
        ("production/concept-small-fish-20261019/generator.py", "shared-generator"),
        ("production/concept-small-fish-20261019/parse-exact-models.mjs", "threejs-parse-script"),
    ):
        add_record(records, rel, role)

    for asset_id in ASSETS:
        asset_root = f"production/concept-small-fish-20261019/{asset_id}/r001"
        artifact_paths = {
            "brief_md": f"{asset_root}/brief.md",
            "brief_json": f"{asset_root}/brief.json",
            "references": f"{asset_root}/references.json",
            "build_config": f"{asset_root}/build-config.json",
            "concept_evidence": f"{asset_root}/concept-evidence.json",
            "source_blend": f"{asset_root}/output/{asset_id}.blend",
            "glb": f"{asset_root}/output/{asset_id}.glb",
        }
        for name, rel in artifact_paths.items():
            add_record(records, rel, f"{asset_id}:{name}")
        glb_hash = next(r["sha256"] for r in records if r["path"] == artifact_paths["glb"])
        sidecar = json.loads((ROOT / artifact_paths["concept_evidence"]).read_text())
        sidecar_checks = {}
        for name in ("brief", "references", "config", "source", "glb"):
            item = sidecar["artifacts"][name]
            path = PACKAGE / item["path"]
            sidecar_checks[name] = digest(path) == item["sha256"]

        concept_checks = {}
        for item in (sidecar["concept"]["prompt"], sidecar["concept"]["generation_record"], *sidecar["concept"]["images"]):
            path = PACKAGE / item["path"]
            concept_checks[item["path"]] = digest(path) == item["sha256"]

        render_checks = {}
        for folder in ("proof", "concept-angle-proof"):
            manifest_rel = f"{asset_root}/{folder}/render-manifest.json"
            add_record(records, manifest_rel, f"{asset_id}:{folder}:manifest")
            config_rel = f"{asset_root}/{folder}/render-config.json"
            add_record(records, config_rel, f"{asset_id}:{folder}:config")
            manifest_path = ROOT / manifest_rel
            manifest = json.loads(manifest_path.read_text())
            config_path = manifest_path.parent / manifest["render_config"]["path"]
            config_hash_ok = digest(config_path) == manifest["render_config"]["sha256"]
            render_checks[folder] = verify_render_manifest(manifest_path, glb_hash)
            render_checks[folder]["render_config_hash_matches"] = config_hash_ok
            for frame in manifest["frames"]:
                image = manifest_path.parent / frame["path"]
                add_record(records, str(image.relative_to(ROOT)), f"{asset_id}:{folder}:frame:{frame['id']}")

        chronology = sidecar.get("chronology", {})
        checks["assets"][asset_id] = {
            "sidecar_artifacts_match": sidecar_checks,
            "sidecar_concept_hashes_match": concept_checks,
            "render_manifests": render_checks,
            "concept_generated_at": chronology.get("concept_generated_at"),
            "concept_inspected_at": chronology.get("concept_inspected_at"),
            "modeling_started_at": chronology.get("modeling_started_at"),
        }

    checks["all_sidecar_artifacts_match"] = all(
        all(a["sidecar_artifacts_match"].values()) and all(a["sidecar_concept_hashes_match"].values())
        for a in checks["assets"].values()
    )
    checks["all_render_evidence_matches"] = all(
        all(r["source_glb_sha256_matches"] and r["all_frames_match"] and r["render_config_hash_matches"] for r in a["render_manifests"].values())
        for a in checks["assets"].values()
    )
    for rel, role in (
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/REPORT.md", "independent-qa-report"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/review-decisions.json", "structured-review-decisions"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/commands.md", "review-method-and-commands"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/blender_reimport.py", "independent-blender-reimport-script"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/blender-reimport.json", "independent-blender-reimport-result"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/threejs_node_load.mjs", "independent-threejs-loader-script"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/threejs-node-loader.json", "independent-threejs-loader-result"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/validate_gltf.mjs", "independent-khronos-validator-script"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/khronos/summary.json", "independent-khronos-validator-summary"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/runtime-harness.html", "threejs-browser-harness"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/favicon.svg", "threejs-browser-harness-icon"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/run_runtime.mjs", "threejs-browser-runner"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/threejs-webgl-result.json", "threejs-browser-result"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/threejs-webgl-scene.png", "threejs-browser-render"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/measure_pteraspis_tail.py", "pteraspis-caudad-feature-measurement-script"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/pteraspis-tail-measurement.json", "pteraspis-caudad-feature-measurement"),
        ("qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/verify_artifact_bindings.py", "artifact-binding-verifier"),
    ):
        add_record(records, rel, role)
    for asset_id in ASSETS:
        rel = f"qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/khronos/{asset_id}.gltf-validator.json"
        add_record(records, rel, f"{asset_id}:independent-khronos-validator-report")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    binding_path = OUTPUT / "binding-verification.json"
    binding_path.write_text(json.dumps(checks, indent=2) + "\n")
    add_record(records, str(binding_path.relative_to(ROOT)), "independent-binding-verification-result")
    (OUTPUT / "artifact-hashes.json").write_text(json.dumps({"candidate_commit": CANDIDATE_COMMIT, "files": records}, indent=2) + "\n")
    print(json.dumps({"records": len(records), "all_sidecar_artifacts_match": checks["all_sidecar_artifacts_match"], "all_render_evidence_matches": checks["all_render_evidence_matches"], "chronology": {a: {"concept_generated_at": v["concept_generated_at"], "concept_inspected_at": v["concept_inspected_at"]} for a, v in checks["assets"].items()}}, indent=2))


if __name__ == "__main__":
    main()
