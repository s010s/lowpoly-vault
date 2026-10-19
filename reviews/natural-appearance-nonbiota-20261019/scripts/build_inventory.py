#!/usr/bin/env python3
"""Freeze the in-scope visual review inventory from main and batch handoffs.

This records source paths, commits, and SHA-256 pins only. It does not edit or
validate production assets.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews/natural-appearance-nonbiota-20261019"
BASELINE = "de413ef720463a2999516faf92c606bcdf9ab1b7"
SCOPE_CATEGORIES = {"geology", "traces", "terrain"}

HANDOFFS = [
    ("40", "refs/remotes/origin/candidate/small-life-batch40-20261018",
     "production/continuous-small-life-round14-20261018/work/batch-40/HANDOFF.json", "json"),
    ("41", "refs/remotes/origin/handoff/batch41-20261018",
     "production/continuous-small-life-round14-20261018/work/batch-41/final-handoff.jsonl", "jsonl"),
    ("42", "refs/remotes/origin/candidate/small-life-batch42-20261018",
     "production/continuous-small-life-round14-20261018/work/batch-42/HANDOFF.json", "json"),
    ("43", "refs/remotes/origin/candidate/small-life-batch43-20261018",
     "production/continuous-small-life-round15-20261018/work/batch-43/HANDOFF.json", "json"),
    ("44", "refs/remotes/origin/handoff/batch44-20261018",
     "production/continuous-small-life-round15-20261018/work/batch-44/final-handoff.jsonl", "jsonl"),
    ("45", "refs/remotes/origin/candidate/small-life-batch45-20261018",
     "production/continuous-small-life-round15-20261018/work/batch-45/HANDOFF.json", "json"),
    ("46", "refs/remotes/origin/candidate/small-life-batch46-20261018",
     "production/continuous-small-life-round16-20261018/work/batch-46/HANDOFF.json", "json"),
    ("47", "refs/remotes/origin/handoff/batch47-20261018",
     "production/continuous-small-life-round16-20261018/work/batch-47/final-handoff.jsonl", "jsonl"),
    ("48", "refs/remotes/origin/candidate/small-life-batch48-20261018",
     "production/continuous-small-life-round16-20261018/work/batch-48/HANDOFF.json", "json"),
    ("49", "refs/remotes/origin/candidate/small-life-batch49-20261018",
     "production/continuous-small-life-round17-20261018/work/batch-49/HANDOFF.json", "json"),
]
BATCH50_HANDOFF = "refs/remotes/origin/handoff/batch50-20261018"
BATCH50_STATUS = "production/continuous-small-life-round17-20261018/work/batch-50/recovery-status.json"


def git(*args: str, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary)


def read_blob(ref: str, path: str) -> bytes:
    return git("show", f"{ref}:{path}", binary=True)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def handoff_data(ref: str, path: str, kind: str):
    raw = read_blob(ref, path).decode("utf-8")
    if kind == "jsonl":
        return [json.loads(line) for line in raw.splitlines() if line.strip()]
    return json.loads(raw)


def find_model_path(ref: str, asset: dict) -> str | None:
    glb = asset.get("glb")
    if isinstance(glb, dict) and glb.get("path"):
        return glb["path"]
    candidate_dir = asset.get("candidate_dir")
    if not candidate_dir:
        return None
    paths = git("ls-tree", "-r", "--name-only", ref).splitlines()
    expected = asset.get("glb_sha256")
    matches = []
    for path in paths:
        if not path.startswith(candidate_dir + "/") or not path.lower().endswith(".glb"):
            continue
        if expected:
            if sha256(read_blob(ref, path)) == expected:
                matches.append(path)
        elif Path(path).name == f"{asset['asset_id']}.glb":
            matches.append(path)
    if len(matches) == 1:
        return matches[0]
    return None


def candidate_record(batch: str, handoff_ref: str, handoff_path: str,
                     handoff_kind: str, record: dict) -> dict:
    source_ref = handoff_ref
    source_commit = git("rev-parse", source_ref).strip()
    category = (record.get("catalog_facets") or {}).get("category", "unknown")
    if record.get("branch"):
        source_ref = "refs/remotes/origin/" + record["branch"]
        stated = record.get("commit")
        source_commit = stated or ""
        if category in SCOPE_CATEGORIES:
            source_commit_actual = git("rev-parse", source_ref).strip()
            if stated and stated != source_commit_actual:
                raise ValueError(f"{record['asset_id']}: branch tip differs from handoff commit")
            source_commit = source_commit_actual
    asset_id = record.get("asset_id", "")
    subcategory = (record.get("catalog_facets") or {}).get("subcategory", "")
    glb_path = find_model_path(source_ref, record) if category in SCOPE_CATEGORIES or not record.get("branch") else None
    expected_hash = (record.get("glb") or {}).get("sha256") or record.get("glb_sha256")
    actual_hash = sha256(read_blob(source_ref, glb_path)) if glb_path else ""
    if expected_hash and actual_hash and actual_hash != expected_hash:
        raise ValueError(f"{asset_id}: GLB SHA-256 differs from latest handoff")
    revision = record.get("revision", "r001")
    attempt = record.get("selected_attempt", "")
    if not attempt and glb_path:
        bits = glb_path.split("/")
        attempt = next((part for part in bits if part.startswith("attempt-")), "")
    metadata_path = (record.get("metadata") or {}).get("path", "")
    if not metadata_path and glb_path:
        metadata_path = str(Path(glb_path).with_name("metadata.json"))
    display_context = ""
    if metadata_path and category in SCOPE_CATEGORIES:
        try:
            metadata = json.loads(read_blob(source_ref, metadata_path))
            description = metadata.get("description", {})
            display_context = description.get("en", "") if isinstance(description, dict) else str(description)
            display_context = metadata.get("claim_scope", "") or display_context
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            pass
    return {
        "asset_id": asset_id,
        "source_type": "candidate",
        "batch": f"batch-{batch}",
        "category": category,
        "subcategory": subcategory,
        "revision": revision,
        "selected_attempt": attempt,
        "source_ref": source_ref,
        "source_commit": source_commit,
        "handoff_ref": handoff_ref,
        "handoff_commit": git("rev-parse", handoff_ref).strip(),
        "handoff_path": handoff_path,
        "model_path": glb_path or "",
        "model_record_path": "",
        "brief_path": "",
        "metadata_path": metadata_path,
        "expected_glb_sha256": expected_hash or "",
        "actual_glb_sha256": actual_hash,
        "metadata_path": metadata_path,
        "scope_disposition": "in_scope" if category in SCOPE_CATEGORIES else "excluded_category",
        "availability": "available" if glb_path else "not_generated",
        "visual_review": "pending" if glb_path and category in SCOPE_CATEGORIES else "not_applicable",
        "image_path": "",
        "display_context": display_context,
    }


def main():
    manifest = json.loads((ROOT / "assets/manifest.json").read_text())
    if len(manifest["assets"]) != 175:
        raise ValueError("Frozen main manifest must contain exactly 175 assets")
    rows = []
    for asset in manifest["assets"]:
        category = asset.get("category", "unknown")
        model_path = asset["glb"]
        data = (ROOT / model_path).read_bytes()
        actual_hash = sha256(data)
        expected = asset.get("sha256", {}).get("glb", "")
        if expected and actual_hash != expected:
            raise ValueError(f"{asset['id']}: published GLB hash mismatch")
        rows.append({
            "asset_id": asset["id"],
            "source_type": "published_main",
            "batch": "main",
            "category": category,
            "subcategory": asset.get("subcategory", ""),
            "revision": asset.get("source_revision", "main-release"),
            "selected_attempt": "",
            "source_ref": "origin/main",
            "source_commit": BASELINE,
            "handoff_ref": "",
            "handoff_commit": "",
            "handoff_path": "assets/manifest.json",
            "model_path": model_path,
            "model_record_path": asset.get("candidate_record", ""),
            "brief_path": "",
            "metadata_path": "",
            "expected_glb_sha256": expected,
            "actual_glb_sha256": actual_hash,
            "model_record_path": asset.get("candidate_record", ""),
            "scope_disposition": "in_scope" if category in SCOPE_CATEGORIES else "excluded_category",
            "availability": "available",
            "visual_review": "pending" if category in SCOPE_CATEGORIES else "not_applicable",
            "image_path": "",
            "display_context": asset.get("description", {}).get("en", ""),
        })

    all_batches = {}
    for batch, ref, path, kind in HANDOFFS:
        handoff = handoff_data(ref, path, kind)
        records = handoff.get("assets", []) if isinstance(handoff, dict) else handoff
        for record in records:
            rows.append(candidate_record(batch, ref, path, kind, record))
        all_batches[batch] = {
            "handoff_ref": ref,
            "handoff_commit": git("rev-parse", ref).strip(),
            "handoff_path": path,
            "status": handoff.get("status", "candidate handoff; see per-item records") if isinstance(handoff, dict) else "candidate handoff",
            "asset_count": len(records),
        }

    status = handoff_data(BATCH50_HANDOFF, BATCH50_STATUS, "json")
    all_batches["50"] = {
        "handoff_ref": BATCH50_HANDOFF,
        "handoff_commit": git("rev-parse", BATCH50_HANDOFF).strip(),
        "handoff_path": BATCH50_STATUS,
        "status": status["kind"],
        "asset_count": len(status["assets"]),
    }
    for record in status["assets"]:
        asset_id = record["asset_id"]
        source_ref = "refs/remotes/origin/" + record["branch"]
        source_commit = git("rev-parse", source_ref).strip()
        work_dir = record.get("work_dir", "")
        brief_path = f"{work_dir}/brief.json" if work_dir else ""
        category = "unknown"
        if brief_path:
            try:
                brief = json.loads(read_blob(source_ref, brief_path))
                category = (brief.get("subject") or {}).get("category", "unknown")
            except (subprocess.CalledProcessError, json.JSONDecodeError):
                category = "unknown"
        model_path = ""
        actual_hash = ""
        expected_hash = ""
        if record["status"] == "completed_maker_evidence_paused_before_independent_review":
            model_path = f"{record['candidate_dir']}/{asset_id}.glb"
            blob = read_blob(source_ref, model_path)
            actual_hash = sha256(blob)
            expected_hash = actual_hash
        rows.append({
            "asset_id": asset_id,
            "source_type": "paused_batch50",
            "batch": "batch-50",
            "category": category,
            "subcategory": "",
            "revision": "r001",
            "selected_attempt": "",
            "source_ref": source_ref,
            "source_commit": source_commit,
            "handoff_ref": BATCH50_HANDOFF,
            "handoff_commit": all_batches["50"]["handoff_commit"],
            "handoff_path": BATCH50_STATUS,
            "model_path": model_path,
            "model_record_path": "",
            "metadata_path": "",
            "expected_glb_sha256": expected_hash,
            "actual_glb_sha256": actual_hash,
            "brief_path": brief_path,
            "scope_disposition": "in_scope" if category in SCOPE_CATEGORIES else "excluded_category",
            "availability": "available" if model_path else "not_generated",
            "visual_review": "not_applicable" if category not in SCOPE_CATEGORIES else "not_generated_not_inspected",
            "image_path": "",
            "display_context": record.get("status", ""),
        })

    visual_manifest_path = OUT / "evidence/visual-manifest.json"
    visual_by_id = {}
    if visual_manifest_path.exists():
        visual_by_id = {item["asset_id"]: item for item in json.loads(visual_manifest_path.read_text())}
        if len(visual_by_id) != len(json.loads(visual_manifest_path.read_text())):
            raise ValueError("Visual manifest contains duplicate asset ids")
        for row in rows:
            if row["scope_disposition"] != "in_scope":
                continue
            if row["availability"] == "available":
                visual = visual_by_id.get(row["asset_id"])
                if not visual:
                    raise ValueError(f"{row['asset_id']}: available in-scope model is missing visual evidence")
                if visual["source_glb_sha256"] != row["actual_glb_sha256"]:
                    raise ValueError(f"{row['asset_id']}: visual source hash differs from inventory")
                row["visual_review"] = "six_views_pixel_inspected"
                row["image_path"] = visual["image_path"]
            else:
                row["visual_review"] = "not_generated_not_inspected"

    scope_rows = [r for r in rows if r["scope_disposition"] == "in_scope"]
    scope_rows.sort(key=lambda r: (r["batch"], r["asset_id"]))
    render_inputs = []
    temp_input_dir = Path("/tmp/lowpoly-natural-review/input-glb")
    temp_input_dir.mkdir(parents=True, exist_ok=True)
    for row in scope_rows:
        if not row["model_path"]:
            continue
        model_bytes = (ROOT / row["model_path"]).read_bytes() if row["source_type"] == "published_main" else read_blob(row["source_ref"], row["model_path"])
        actual_hash = sha256(model_bytes)
        if actual_hash != row["actual_glb_sha256"]:
            raise ValueError(f"{row['asset_id']}: source changed while preparing render inputs")
        local_path = temp_input_dir / f"{row['asset_id']}.glb"
        local_path.write_bytes(model_bytes)
        render_inputs.append({
            "asset_id": row["asset_id"],
            "batch": row["batch"],
            "category": row["category"],
            "revision": row["revision"],
            "source_commit": row["source_commit"],
            "source_ref": row["source_ref"],
            "model_path": row["model_path"],
            "sha256": actual_hash,
            "input_path": str(local_path),
        })
    all_batches = dict(sorted(all_batches.items(), key=lambda x: int(x[0])))
    inventory = {
        "frozen_baseline": BASELINE,
        "published_baseline_assets": len(manifest["assets"]),
        "published_baseline_in_scope": sum(r["source_type"] == "published_main" and r["scope_disposition"] == "in_scope" for r in rows),
        "candidate_batches": all_batches,
        "discovered_assets_total": len(rows),
        "in_scope_discovered_total": len(scope_rows),
        "in_scope_models_available": sum(bool(r["model_path"]) for r in scope_rows),
        "in_scope_models_not_generated": sum(r["availability"] == "not_generated" for r in scope_rows),
        "classification_rule": "geology, traces, and terrain are in scope; animals, plants, fungi, and wood are out of scope",
        "assets": rows,
    }
    (OUT / "coverage.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n")
    fields = list(rows[0].keys())
    with (OUT / "coverage.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    Path("/tmp/lowpoly-natural-review/render-inputs.json").write_text(json.dumps(render_inputs, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "discovered_assets_total": len(rows),
        "published_baseline_in_scope": inventory["published_baseline_in_scope"],
        "in_scope_discovered_total": len(scope_rows),
        "in_scope_models_available": inventory["in_scope_models_available"],
        "in_scope_models_not_generated": inventory["in_scope_models_not_generated"],
        "candidate_batch_counts": {k: v["asset_count"] for k, v in all_batches.items()},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
