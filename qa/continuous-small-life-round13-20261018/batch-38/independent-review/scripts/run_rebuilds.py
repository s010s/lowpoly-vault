#!/usr/bin/env python3
"""Run two fresh pinned-generator rebuilds per asset into isolated /tmp outputs."""
import hashlib, json, os, subprocess, tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from qa_glb import audit_glb

IDS = ["diplomoceras", "nelumbo", "marine-terrace", "angular-unconformity-outcrop"]
BASE = ROOT / "production/continuous-small-life-round13-20261018/work/batch-38"
HANDOFF = json.loads((BASE / "HANDOFF.json").read_text())
ROWS = {a["asset_id"]: a for a in HANDOFF["assets"]}
QA = Path(__file__).resolve().parents[1]
EVIDENCE = QA / "evidence/rebuilds"
BLENDER = "/usr/bin/blender"
TMP = Path(tempfile.mkdtemp(prefix="lowpoly-batch38-rebuild-", dir="/tmp"))
digest = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

pairs = []
report = {"schema_version": 1, "check": "two_fresh_rebuilds_per_asset", "status": "fail",
          "model_source_commit": HANDOFF["model_source_commit"], "blender": None,
          "temporary_output_root": str(TMP), "assets": [],
          "limitations": "Fresh generator executions plus decoded GLB semantic digests; no byte-level Blend identity or visual/factual claim."}
version = subprocess.run([BLENDER, "--version"], check=True, text=True, capture_output=True).stdout.splitlines()[:2]
report["blender"] = {"version_output": version}

for asset in IDS:
    row = ROWS[asset]
    gen = BASE / asset / "r001/generator.py"
    cfg = BASE / asset / "r001/config.json"
    original_glb = ROOT / row["glb"]["path"]
    original_blend = ROOT / row["blend"]["path"]
    original_audit = audit_glb(original_glb, max_triangles=10**9, max_materials=10**6, max_primitives=10**6)
    if original_audit["errors"]:
        raise RuntimeError(f"Frozen GLB audit failed for {asset}: {original_audit['errors']}")
    item = {"asset_id": asset, "generator_sha256": digest(gen), "config_sha256": digest(cfg),
            "mesh_utils_sha256": digest(BASE / "mesh_utils.py"), "helper_sha256": digest(ROOT / "scripts/asset_common.py"),
            "frozen_glb_sha256": row["glb"]["sha256"], "frozen_blend_sha256": row["blend"]["sha256"],
            "frozen_glb_semantic_sha256": original_audit["semantic_sha256"], "frozen_triangles": original_audit["scene_triangles"],
            "runs": []}
    for run_number in (1, 2):
        output_root = TMP / asset / f"run-{run_number}"
        output_root.mkdir(parents=True, exist_ok=False)
        command = [BLENDER, "--background", "--factory-startup", "--threads", "2", "--disable-autoexec",
                   "--python-exit-code", "1", "--python", str(gen), "--", "--asset", asset,
                   "--config", str(cfg), "--output", str(output_root), "--no-preview"]
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=900)
        run_dir = output_root / asset
        rebuilt_glb, rebuilt_blend = run_dir / f"{asset}.glb", run_dir / f"{asset}.blend"
        log = EVIDENCE / asset / f"run-{run_number}.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text("COMMAND: " + json.dumps(command) + "\nEXIT: " + str(proc.returncode) +
                       "\n--- STDOUT ---\n" + proc.stdout + "\n--- STDERR ---\n" + proc.stderr)
        if proc.returncode or not rebuilt_glb.is_file() or not rebuilt_blend.is_file():
            item["runs"].append({"run": run_number, "status": "fail", "returncode": proc.returncode,
                                 "log": str(log.relative_to(ROOT))})
            continue
        audit = audit_glb(rebuilt_glb, max_triangles=10**9, max_materials=10**6, max_primitives=10**6)
        run = {"run": run_number, "status": "fail" if audit["errors"] else "pass",
               "command": command, "log_path": str(log.relative_to(ROOT)), "log_sha256": digest(log),
               "blend_sha256": digest(rebuilt_blend), "glb_sha256": audit.get("sha256"), "glb_bytes": audit.get("bytes"),
               "semantic_sha256": audit.get("semantic_sha256"), "triangles": audit.get("scene_triangles"),
               "glb_static_audit_errors": audit["errors"], "glb_static_audit_warnings": audit["warnings"],
               "temporary_blend_path": str(rebuilt_blend), "temporary_glb_path": str(rebuilt_glb)}
        item["runs"].append(run)
        pairs.append({"asset_id": asset, "input_kind": f"independent rebuild run-{run_number}",
                      "blend": str(rebuilt_blend), "glb": str(rebuilt_glb),
                      "report": str((EVIDENCE / asset / f"run-{run_number}-source-export.json").resolve())})
    if len(item["runs"]) == 2 and all(r.get("status") == "pass" for r in item["runs"]):
        item["rebuild_semantic_match_frozen"] = all(r["semantic_sha256"] == item["frozen_glb_semantic_sha256"] for r in item["runs"])
        item["rebuilds_semantically_match_each_other"] = item["runs"][0]["semantic_sha256"] == item["runs"][1]["semantic_sha256"]
        item["rebuild_bytes_match_frozen"] = all(r["glb_sha256"] == item["frozen_glb_sha256"] for r in item["runs"])
    else:
        item.update({"rebuild_semantic_match_frozen": False, "rebuilds_semantically_match_each_other": False,
                     "rebuild_bytes_match_frozen": False})
    source_report = EVIDENCE.parent / "blender" / f"{asset}-source-export.json"
    source_render = EVIDENCE.parent / "fixed-views" / asset
    pairs.append({"asset_id": asset, "input_kind": "frozen source candidate", "blend": str(original_blend), "glb": str(original_glb),
                  "report": str(source_report.resolve()), "render_output_dir": str(source_render.resolve())})
    report["assets"].append(item)

report["status"] = "pass" if all(a["rebuild_semantic_match_frozen"] and a["rebuilds_semantically_match_each_other"]
                                  and all(r.get("status") == "pass" for r in a["runs"]) for a in report["assets"]) else "fail"
manifest_path = TMP / "blend-glb-pairs.json"
manifest_path.write_text(json.dumps({"pairs": pairs}, indent=2) + "\n")
report["pair_audit_manifest"] = str(manifest_path)
out = EVIDENCE / "rebuild-summary.json"
out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"status": report["status"], "temporary_output_root": str(TMP),
                  "assets": [{"asset_id": a["asset_id"], "runs": [{k:r.get(k) for k in ("run", "status", "glb_sha256", "semantic_sha256", "triangles")} for r in a["runs"]],
                             "semantic_match_frozen": a["rebuild_semantic_match_frozen"],
                             "runs_match_each_other": a["rebuilds_semantically_match_each_other"],
                             "byte_match_frozen": a["rebuild_bytes_match_frozen"]} for a in report["assets"]]}, indent=2))
