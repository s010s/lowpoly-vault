#!/usr/bin/env python3
"""Read frozen/rebuilt Blend-GLB pairs and independently compare geometry bounds."""
import bpy, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from asset_common import audit_source, render_previews
from check_source_export import compare_source_audit
from qa_glb import audit_glb

args = sys.argv[sys.argv.index("--") + 1:]
if len(args) != 1:
    raise SystemExit("usage: blend_glb_audit.py -- <pairs.json>")
manifest = json.loads(Path(args[0]).read_text())
digest = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
results = []
for pair in manifest["pairs"]:
    blend, glb = Path(pair["blend"]).resolve(), Path(pair["glb"]).resolve()
    blend_hash, glb_hash = digest(blend), digest(glb)
    bpy.context.preferences.filepaths.use_scripts_auto_execute = False
    bpy.ops.wm.open_mainfile(filepath=str(blend), load_ui=False, use_scripts=False)
    collections = [c for c in bpy.data.collections if c.get("asset_root")]
    if len(collections) != 1:
        raise RuntimeError(f"{pair['asset_id']}: expected one asset_root collection, got {len(collections)}")
    source = audit_source(collections[0], max_triangles=10**9)
    exported = audit_glb(glb, max_triangles=10**9, max_materials=10**6, max_primitives=10**6)
    result = compare_source_audit(source, exported, blend_hash, glb_hash)
    result.update({"asset_id": pair["asset_id"], "input_kind": pair["input_kind"],
                   "blender_version": bpy.app.version_string, "export_collection": collections[0].name,
                   "source_audit": source, "glb_audit": exported,
                   "blend_unchanged": digest(blend) == blend_hash, "glb_unchanged": digest(glb) == glb_hash,
                   "limitations": "Evaluated source triangles and axis-converted bounds are compared to exact GLB. It does not certify appeal, taxonomy, or GPU performance."})
    if pair.get("render_output_dir"):
        out = Path(pair["render_output_dir"]).resolve()
        if out.exists() and any(out.iterdir()):
            raise RuntimeError(f"Render output directory must be empty: {out}")
        out.mkdir(parents=True, exist_ok=True)
        views = ("hero", "reversehero", "front", "side", "rear", "top", "clay", "silhouette")
        paths = render_previews(collections[0], out, views=views, resolution=512, samples=16, transparent=True)
        frames = []
        for name, path in zip(views, paths):
            image = bpy.data.images.load(path, check_existing=False)
            frames.append({"view": name, "path": Path(path).name, "sha256": digest(path),
                           "bytes": Path(path).stat().st_size, "width": int(image.size[0]), "height": int(image.size[1])})
            bpy.data.images.remove(image)
        result["independent_source_renders"] = {"views": frames, "samples": 16, "engine": "Cycles CPU",
            "transparent_background": True, "visual_review": "pending", "source_saved": False}
    if digest(blend) != blend_hash or digest(glb) != glb_hash:
        result["errors"].append("Input changed during check")
        result["status"] = "fail"
    report_path = Path(pair["report"]).resolve()
    if report_path.exists():
        raise RuntimeError(f"Refusing to overwrite evidence: {report_path}")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    results.append({"asset_id": pair["asset_id"], "input_kind": pair["input_kind"],
                    "report": str(report_path), "status": result["status"],
                    "triangles_match": result["triangles_match"], "bounds_match": result["bounds_match"],
                    "source_triangles": result.get("source_triangles"), "glb_triangles": result.get("glb_triangles"),
                    "bounds_max_error_m": result.get("bounds_max_error_m"), "errors": result["errors"]})
print(json.dumps({"status": "pass" if all(r["status"] in {"pass", "pass_with_warnings"} for r in results) else "fail",
                  "pairs": results}, indent=2))
if any(r["status"] == "fail" for r in results):
    raise RuntimeError("One or more Blend/GLB pairs failed")
