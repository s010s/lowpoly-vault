#!/usr/bin/env python3
"""Read-only verification of the pinned batch-38 handoff and source blobs."""
from __future__ import annotations
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HANDOFF_COMMIT = "70abb5ec41aadd31d56ac9f0d1890ad708afc6da"
HANDOFF_PATH = "production/continuous-small-life-round13-20261018/work/batch-38/HANDOFF.json"
SCOPE_PATH = "production/continuous-small-life-round13-20261018/work/batch-38/QA-HANDOFF-SCOPE.json"
OUT = Path(__file__).resolve().parents[1] / "evidence/source-integrity.json"

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)

handoff = json.loads((ROOT / HANDOFF_PATH).read_text())
scope = json.loads((ROOT / SCOPE_PATH).read_text())
model_commit = handoff["model_source_commit"]
expected_ids = ["diplomoceras", "nelumbo", "marine-terrace", "angular-unconformity-outcrop"]
assets = {row["asset_id"]: row for row in handoff["assets"]}
assert handoff["branch"] == "candidate/small-life-batch38-20261018"
assert handoff["assets"] and list(assets) == expected_ids
assert scope["expected_asset_ids"] == expected_ids
assert scope["expected_source_commit"] == model_commit
assert scope["expected_glb_sha256_by_asset"] == {name: assets[name]["glb"]["sha256"] for name in expected_ids}
assert scope["ready_for_qa"] is True

checked = []
def walk(value):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
            rel = Path(value["path"])
            assert not rel.is_absolute() and ".." not in rel.parts, rel
            path = ROOT / rel
            assert path.is_file() and not path.is_symlink(), rel
            raw = path.read_bytes()
            assert sha(raw) == value["sha256"], rel
            if "bytes" in value:
                assert len(raw) == value["bytes"], rel
            checked.append({"path": rel.as_posix(), "sha256": sha(raw), "bytes": len(raw)})
        for item in value.values():
            walk(item)
    elif isinstance(value, list):
        for item in value:
            walk(item)

walk(handoff)
for key, path in (("handoff", HANDOFF_PATH), ("qa_handoff_scope", SCOPE_PATH)):
    frozen = git_blob(HANDOFF_COMMIT, path)
    current = (ROOT / path).read_bytes()
    assert frozen == current

source_blobs = []
for asset_id in expected_ids:
    row = assets[asset_id]
    for kind in ("glb", "blend"):
        record = row[kind]
        raw = git_blob(model_commit, record["path"])
        digest = sha(raw)
        assert digest == record["sha256"], (asset_id, kind, digest, record["sha256"])
        assert len(raw) == record["bytes"]
        source_blobs.append({"asset_id": asset_id, "kind": kind, "path": record["path"], "sha256": digest, "bytes": len(raw)})

report = {
    "schema_version": 1,
    "check": "frozen_batch38_source_integrity",
    "status": "pass",
    "handoff_commit": HANDOFF_COMMIT,
    "handoff_path": HANDOFF_PATH,
    "handoff_sha256": sha((ROOT / HANDOFF_PATH).read_bytes()),
    "qa_handoff_scope_path": SCOPE_PATH,
    "qa_handoff_scope_sha256": sha((ROOT / SCOPE_PATH).read_bytes()),
    "model_source_commit": model_commit,
    "expected_asset_ids": expected_ids,
    "expected_glb_sha256_by_asset": scope["expected_glb_sha256_by_asset"],
    "handoff_file_references_verified": len(checked),
    "model_source_glb_blend_blobs_verified": source_blobs,
    "limitations": "Pins and bytes only; this record makes no visual, runtime, factual, profile approval, or hardware performance claim."
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"status": report["status"], "handoff_file_references_verified": len(checked), "model_source_blobs": source_blobs}, indent=2))
