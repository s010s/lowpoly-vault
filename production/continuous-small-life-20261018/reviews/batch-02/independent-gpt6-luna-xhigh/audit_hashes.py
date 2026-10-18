#!/usr/bin/env python3
"""Read-only integrity audit for the frozen Batch 02 candidate bundles."""
import argparse
import hashlib
import json
from pathlib import Path

ASSETS = ("longipteryx", "urasterella", "alienopterus", "aglaophyton")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    args = ap.parse_args()
    repo = args.repo.resolve()
    result_path = repo / "production/continuous-small-life-20261018/work/batch-02/batch-02-result.json"
    root = repo / "assets/candidates/continuous-small-life-20261018/batch-02/r001"
    result = json.loads(result_path.read_text())
    expected = {a["asset_id"]: a for a in result["assets"]}
    failures = []
    for name in ASSETS:
        p = root / name
        manifest = json.loads((p / "evidence-manifest.json").read_text())
        runtime = json.loads((p / "runtime/report.json").read_text())
        validator = json.loads((p / "gltf-validator.report.json").read_text())
        sums = {}
        for line in (p / "checksums.sha256").read_text().splitlines():
            digest, rel = line.split("  ", 1)
            sums[rel] = digest
        bad = []
        for rel, want in sums.items():
            path = p / rel
            if not path.is_file() or sha(path) != want:
                bad.append(f"checksum:{rel}")
        glb = p / f"{name}.glb"
        blend = p / f"{name}.blend"
        candidate = json.loads((p / "candidate.json").read_text())
        checks = {
            "glb_sha": sha(glb) == manifest["glb_sha256"] == runtime["glb_sha256"] == expected[name]["glb_sha256"],
            "blend_sha": sha(blend) == manifest["source_blend_sha256"],
            "candidate_sha": sha(p / "candidate.json") == expected[name]["candidate_sha256"],
            "glb_size": glb.stat().st_size == expected[name]["glb_bytes"],
            "runtime_status": runtime.get("status") == "pass" and not runtime.get("errors"),
            "validator": validator.get("issues", {}).get("numErrors") == 0 and validator.get("issues", {}).get("numWarnings") == 0,
        }
        for key, ok in checks.items():
            if not ok:
                bad.append(key)
        image_count = 0
        for rel, spec in manifest["images"].items():
            path = p / rel
            if not path.is_file() or sha(path) != spec["sha256"] or path.stat().st_size != spec["bytes"]:
                bad.append(f"manifest-image:{rel}")
            else:
                image_count += 1
        print(f"{name}: glb={glb.stat().st_size}B sha={sha(glb)}; blend_sha={sha(blend)}; candidate_sha={sha(p/'candidate.json')}; files={len(sums)} checksums; images={image_count}/{len(manifest['images'])}; validator={validator.get('issues',{}).get('numErrors')} errors/{validator.get('issues',{}).get('numWarnings')} warnings; result={'PASS' if not bad else 'FAIL'}")
        failures.extend(f"{name}:{item}" for item in bad)
    if failures:
        print("FAILURES:", "; ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
