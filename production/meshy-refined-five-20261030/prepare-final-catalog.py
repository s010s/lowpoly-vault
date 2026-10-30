#!/usr/bin/env python3
"""Prepare JSON-only five-revision catalog overlay; never modify the repository.

Requires the exact baseline, portable candidate inventory, and materialized Cloud
capture outputs. Inventory file records use safe repo_path values, not producer
absolute paths. The output COPY-PLAN is operational and must not be committed.
No model/image generation, copying, QA approval, Git or network action occurs.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import struct

RELEASE = "meshy-refined-five-20261030"
BASE_COMMIT = "bd07cc709dd7ce4cfa1d87043fcf8a6ed7b8aca6"
BASE_PINS = {
    "assets/manifest.json": "08120ac330a58b81ce5f2c22fa9410a89e05e4a14a402b2f9a3a599d8f22c630",
    "site/public/gallery/resources.json": "82299aeaeaeef3801b711b9413149ff726b509fdc1eec63ad4127b7741acfa9c",
}
EXPECTED = {
    "gomphotherium": "98adc0276da06ca3883eb13d8274974609d30779c8cb5d13225a4467eb8e8616",
    "paraceratherium": "9febf81df9730fda570a60f7ac7b5c293b818bee0b6bae7591b5db530ff669c2",
    "uintatherium": "3a26fdaadc463c2053457df0d1a00cac8231e339e32602e1610b591b8a35ea94",
    "thylacosmilus": "759b44b25a20d6e46c5dad067e4d6d8ecb58dfcd20cd78663d2ba6495c3fcc86",
    "smilodon": "22fa65c2b4a37f8602794746d51e790ab1c74396c91f01a97dccd86e00411b26",
}
DETAIL_POLICY = {"revision": 2, "minimum_margin": 0.025, "screen_shift": 0.06, "raster_size": 1536}
DESCRIPTIONS = {
    "gomphotherium": {
        "en": "Gomphotherium aff. steinheimense-inspired living animal prop, developed from an external Meshy base with Blender refinement. The retained reference brief informs the taxonomic qualification; trunk surface, ears, soft tissues, pose and colour are artistic. Nominal display height is about 1.2 m; measured file dimensions are not real-animal or specimen measurements.",
        "zh": "Gomphotherium aff. steinheimense 启发的完整活体道具，由外部 Meshy 底模经 Blender 精修。沿用原参考简报的分类限定；象鼻表面、耳部、软组织、姿态和配色属于艺术处理。名义展示高度约 1.2 米；文件中的精确尺寸不是动物或标本实测值。",
    },
    "paraceratherium": {
        "en": "Paraceratherium-inspired hornless living-animal prop, retaining the P. grangeri reference convention. An external Meshy base was refined in Blender. Soft tissues, ears, lips, feet, pose and colour are artistic. Nominal display length is about 1.2 m; no exact specimen, maximum mass or species-exclusive measurement is claimed.",
        "zh": "巨犀 Paraceratherium 启发的无角完整活体道具，保留 P. grangeri 参考约定；由外部 Meshy 底模经 Blender 精修。软组织、耳唇、足部、姿态和配色属于艺术处理。名义展示长度约 1.2 米，不主张精确标本、最大体重或物种独占的尺寸数据。",
    },
    "uintatherium": {
        "en": "Uintatherium anceps-inspired living-animal prop, developed from an external Meshy base with Blender refinement. The retained reference brief guides the identity; skin, colour, soft tissues, pose and fine anatomy remain artistic interpretations. Nominal display length is about 1 m. No sex assignment or exact specimen reconstruction is claimed.",
        "zh": "Uintatherium anceps 启发的完整活体道具，由外部 Meshy 底模经 Blender 精修。沿用参考简报的识别目标；皮肤、颜色、软组织、姿态和细部解剖属于艺术解释。名义展示长度约 1 米，不作性别判断或精确标本复原声明。",
    },
    "thylacosmilus": {
        "en": "Thylacosmilus atrox-inspired living-animal prop, developed from an external Meshy base with Blender refinement. The retained reference brief guides the identity; tail, feet, ears, coat, pose and colour include bounded artistic completion. Nominal display length is about 1 m. No exact complete specimen, feeding interpretation or animation claim is made.",
        "zh": "Thylacosmilus atrox 启发的完整活体道具，由外部 Meshy 底模经 Blender 精修。沿用参考简报的识别目标；尾、足、耳、毛色与姿态包含有限的艺术补全。名义展示长度约 1 米，不主张精确完整标本、摄食行为解释或动画适用性。",
    },
    "smilodon": {
        "en": "Smilodon populator-inspired living-animal prop, retaining the selected refined KEEP revision from the Meshy-to-Blender batch. Tawny coat, soft anatomy, expression, paws, pose and precise saber exposure include artistic interpretation. Nominal display length is about 0.8 m. It is not an exact skeleton, scan or whole-specimen reconstruction.",
        "zh": "Smilodon populator 启发的完整活体道具，保留本轮 Meshy→Blender 制作中选定的精修 KEEP 版本。黄褐毛色、软组织、表情、爪足、姿态与犬齿显露程度包含艺术解释。名义展示长度约 0.8 米，不是精确骨架、扫描体或完整标本复原。",
    },
}

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def check(condition, message):
    if not condition:
        raise ValueError(message)

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def safe_relative(path):
    return isinstance(path, str) and bool(path) and not path.startswith("/") and not re.search(r"[\\\x00-\x1f?#%:]", path) and all(p not in ("", ".", "..") for p in path.split("/"))

def under(root: Path, relative: str) -> Path:
    check(safe_relative(relative), "Unsafe relative path")
    p = root / relative
    check(p.resolve().is_relative_to(root.resolve()), "Path escaped selected root")
    check(p.resolve() == p.absolute(), "Symlink in selected file path")
    return p

def verified_record_file(record, repo):
    check("absolute_path" not in record, "Producer absolute_path is not a portable handoff")
    p = under(repo, record["repo_path"])
    data = p.read_bytes()
    check(len(data) == record["bytes"] and digest(data) == record["sha256"], "Candidate inventory bytes/hash mismatch: " + p.name)
    return p, data

DECODER = json.JSONDecoder()
def ws(text, i):
    while i < len(text) and text[i].isspace():
        i += 1
    return i

def members(text, start=0):
    """Object member value spans, preserving every untouched character."""
    i = ws(text, start)
    check(text[i] == "{", "Expected object")
    i = ws(text, i + 1)
    result = {}
    while text[i] != "}":
        key, i = DECODER.raw_decode(text, i)
        check(isinstance(key, str) and key not in result, "Duplicate/non-string object key")
        i = ws(text, i)
        check(text[i] == ":", "Expected colon")
        a = ws(text, i + 1)
        value, b = DECODER.raw_decode(text, a)
        result[key] = (a, b, value)
        i = ws(text, b)
        if text[i] == "}":
            break
        check(text[i] == ",", "Expected member comma")
        i = ws(text, i + 1)
    return result

def items(text, start):
    i = ws(text, start)
    check(text[i] == "[", "Expected array")
    i = ws(text, i + 1)
    result = []
    while text[i] != "]":
        a = i
        value, b = DECODER.raw_decode(text, a)
        result.append((a, b, value))
        i = ws(text, b)
        if text[i] == "]":
            break
        check(text[i] == ",", "Expected array comma")
        i = ws(text, i + 1)
    return result, i

def rendered(value, text, position):
    indent = len(text[text.rfind("\n", 0, position) + 1:position])
    return json.dumps(value, ensure_ascii=False, indent=2).replace("\n", "\n" + " " * indent)

def edits(text, changes):
    last = len(text) + 1
    for a, b, replacement in sorted(changes, reverse=True):
        check(0 <= a <= b < last, "Overlapping edits")
        text = text[:a] + replacement + text[b:]
        last = a
    return text

def preserve_asset_rows(text, replacements):
    spans, _ = items(text, members(text)["assets"][0])
    ids = [row[2]["id"] for row in spans]
    check(len(ids) == 752 and len(set(ids)) == 752, "Baseline must contain exactly 752 unique rows")
    check(set(replacements) <= set(ids), "Replacement ID missing from baseline")
    changes = [(a, b, rendered(replacements[v["id"]], text, a)) for a, b, v in spans if v["id"] in replacements]
    result = edits(text, changes)
    new_spans, _ = items(result, members(result)["assets"][0])
    check([r[2]["id"] for r in new_spans] == ids, "Catalog membership/order changed")
    unchanged = 0
    for old, new in zip(spans, new_spans):
        if old[2]["id"] not in replacements:
            check(text[old[0]:old[1]] == result[new[0]:new[1]], "Untargeted row bytes changed")
            unchanged += 1
    check(unchanged == 747, "Expected 747 untouched row byte ranges")
    return result

def preserve_resources(text, replacements, new_files):
    root = members(text)
    posters = members(text, root["posters"][0])
    check(set(replacements) <= set(posters), "Target poster missing")
    file_spans, _ = items(text, root["files"][0])
    check(file_spans, "Expected existing resource file inventory")
    paths = [x[2]["path"] for x in file_spans]
    check(len(paths) == len(set(paths)), "Duplicate existing file inventory")
    check(not (set(paths) & {x["path"] for x in new_files}), "Versioned image path already exists; do not overwrite history")
    changes = [(posters[k][0], posters[k][1], rendered(v, text, posters[k][0])) for k, v in replacements.items()]
    insertion = "".join(",\n    " + json.dumps(v, ensure_ascii=False, indent=2).replace("\n", "\n    ") for v in new_files)
    changes.append((file_spans[-1][1], file_spans[-1][1], insertion))
    result = edits(text, changes)
    old, new = json.loads(text), json.loads(result)
    for k, v in old.items():
        if k not in ("files", "posters"):
            check(v == new[k], "Historical resource header changed")
    check(new["files"][:len(old["files"])] == old["files"], "Historical file inventory changed")
    for k, v in old["posters"].items():
        if k not in replacements:
            check(v == new["posters"][k], "Untargeted poster changed")
    new_posters = members(result, members(result)["posters"][0])
    for k, (a, b, _) in posters.items():
        if k not in replacements:
            c, d, _ = new_posters[k]
            check(text[a:b] == result[c:d], "Untargeted poster bytes changed")
    return result

def png_metadata(data):
    check(data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24, "Capture is not a PNG")
    return struct.unpack(">II", data[16:24])

def prepare(repo, inventory_path, capture_dir, output):
    repo, capture_dir, output = repo.resolve(), capture_dir.resolve(), output.resolve()
    check(output != repo and not output.is_relative_to(repo), "Output must be outside the checkout")
    check(not output.exists(), "Output directory already exists; no overwrite")
    base_text = {}
    for relative, pin in BASE_PINS.items():
        data = under(repo, relative).read_bytes()
        check(digest(data) == pin, "Baseline changed; reconcile latest main before regenerating: " + relative)
        base_text[relative] = data.decode("utf-8")
    baseline = json.loads(base_text["assets/manifest.json"])
    resources = json.loads(base_text["site/public/gallery/resources.json"])
    original = {a["id"]: a for a in baseline["assets"]}
    inventory = read_json(inventory_path)
    models = inventory["models"]
    check(len(models) == 5 and {m["id"] for m in models} == set(EXPECTED), "Wrong candidate set")
    capture_bytes = under(capture_dir, "capture-identity.json").read_bytes()
    capture = json.loads(capture_bytes)
    renderer_bytes = under(capture_dir, "renderer-report.json").read_bytes()
    renderer = json.loads(renderer_bytes)
    check(capture["status"] == "CAPTURED_NOT_REVIEWED" and not capture.get("errors"), "Capture did not succeed")
    check(renderer["status"] == "CAPTURED_NOT_REVIEWED" and not renderer.get("errors"), "Renderer capture did not succeed")
    check(len(renderer.get("models", [])) == 5 and {x["id"] for x in renderer["models"]} == set(EXPECTED), "Renderer model set differs")
    check(re.fullmatch(r"[a-f0-9]{40}", capture.get("source_commit", "")), "Capture source commit absent")
    check(len(capture["inputs"]) == 5 and {r["id"] for r in capture["inputs"]} == set(EXPECTED), "Capture input set differs")
    check(len(capture["outputs"]) == 10, "Exactly ten captured PNGs required")
    image_map = {(r["id"], r["role"]): r for r in capture["outputs"]}
    check(len(image_map) == 10, "Duplicate capture output role")
    capture_inputs = {r["id"]: r for r in capture["inputs"]}
    rows, poster_rows, image_files, copy_plan, payloads = {}, {}, [], [], []
    for m in models:
        id_ = m["id"]
        check(m["selected_glb"]["sha256"] == EXPECTED[id_], "Wrong frozen GLB pin")
        glb_source, glb_bytes = verified_record_file(m["selected_glb"], repo)
        blend_source, blend_bytes = verified_record_file(m["selected_editable_source"], repo)
        audit = m["glb_readonly_audit"]
        check(not audit["external_resource_uris"], "Unexpected external model resource URI")
        bounds = audit["bounds_world"]
        check(all(len(bounds[k]) == 3 and all(isinstance(v, (int,float)) and math.isfinite(v) for v in bounds[k]) for k in ("min", "max", "dimensions")), "Invalid measured bounds")
        check(all(v > 0 for v in bounds["dimensions"]), "Nonpositive dimension")
        check(capture_inputs[id_]["sha256"] == EXPECTED[id_] and capture_inputs[id_]["bytes"] == len(glb_bytes), "Capture source bytes mismatch")
        check(capture_inputs[id_]["dimensions"] == bounds["dimensions"], "Capture used stale dimensions")
        directory = f"assets/revisions/{RELEASE}/{id_}"
        paths = {"glb": directory + "/model.glb", "blend": directory + "/source.blend", "preview": directory + "/preview.png"}
        check(capture_inputs[id_]["glb"] == paths["glb"], "Capture path mismatch")
        check(m["selected_glb"]["repo_path"] == paths["glb"] and m["selected_editable_source"]["repo_path"] == paths["blend"], "Portable source paths differ from the frozen revision layout")
        check(next(x for x in renderer["models"] if x["id"] == id_)["glb"] == paths["glb"], "Renderer source path differs")
        for role, source, data in (("glb", glb_source, glb_bytes), ("blend", blend_source, blend_bytes)):
            dest = under(repo, paths[role])
            if dest.exists():
                check(digest(dest.read_bytes()) == digest(data), "Existing revision file differs; no replacement allowed")
            copy_plan.append({"id":id_, "role":role, "source_root":"repo", "source_path":paths[role], "destination":paths[role], "copy_required":False, "bytes":len(data), "sha256":digest(data)})
        for role in ("wheel", "detail"):
            entry = image_map[(id_, role)]
            check(entry["source_glb_sha256"] == EXPECTED[id_], "PNG bound to different GLB")
            source = under(capture_dir, entry["path"])
            data = source.read_bytes()
            check(digest(data) == entry["sha256"] and len(data) == entry["bytes"], "Captured PNG bytes mismatch")
            check(png_metadata(data) == ((768,432) if role == "wheel" else (1536,1536)), "Unexpected captured PNG size")
            rel = f"gallery/revisions/{RELEASE}/{id_}/{role}.png"
            image_files.append({"path":rel, "sha256":digest(data), "bytes":len(data)})
            copy_plan.append({"id":id_, "role":"gallery_"+role, "source_root":"capture", "source_path":entry["path"], "destination":"site/public/"+rel, "copy_required":True, "bytes":len(data), "sha256":digest(data)})
            if role == "detail":
                preview_hash = digest(data)
                copy_plan.append({"id":id_, "role":"asset_preview", "source_root":"capture", "source_path":entry["path"], "destination":paths["preview"], "copy_required":True, "bytes":len(data), "sha256":preview_hash})
        evidence = {}
        for name in ("qa-summary.json", "gltf-validator.json", "production-provenance.json"):
            relative = f"production/{RELEASE}/models/{id_}/{name}"
            content = under(repo, relative).read_bytes()
            evidence[name] = {"record":json.loads(content), "pin":{"path":relative,"sha256":digest(content)}}
        summary = evidence["qa-summary.json"]["record"]
        provenance = evidence["production-provenance.json"]["record"]
        check(summary["asset_id"] == id_ and summary["subject"]["glb"]["sha256"] == EXPECTED[id_], "QA summary is for a different candidate")
        check(summary["subject"]["editable_source"]["sha256"] == digest(blend_bytes), "QA summary editable-source binding differs")
        check(summary["new_readonly_format_audit"]["validator_report"] == evidence["gltf-validator.json"]["pin"], "Validator evidence pin differs")
        check(provenance["asset_id"] == id_ and provenance["subject"] == {"revision":RELEASE,"glb_sha256":EXPECTED[id_]}, "Provenance subject differs")
        check(provenance["stages"]["external_generation"]["base_glb_sha256"] == m["original_external_base"]["sha256"], "External base provenance differs")
        old = original[id_]
        check(resources["posters"][id_]["source_glb_sha256"] == old["sha256"]["glb"], "Baseline source/poster mismatch")
        row = copy.deepcopy(old)
        # No old geometry, QA, turntable, original-generator or poster claims may
        # be inherited by a new hash. Current baseline five rows are much smaller.
        for key in ("approval_provenance","production_release","production_posters","production_acceptance_adapter","production_provenance","qa","card_preview","turntable","wheelSpec","generator","generator_config","generator_sha256","generator_dependencies","config_sha256","revision_provenance","successor_provenance"):
            row.pop(key, None)
        row.update(paths)
        row["description"] = DESCRIPTIONS[id_]
        row["scientific_scope"] = {
            "scope":old.get("scientific_scope",{}).get("scope","whole living animal-inspired prop"),
            "artistic_interpretation":"External generated base and Blender refinement; retained reference brief, artistic soft tissues, pose, colour and fine detail. Not an exact specimen or photorealistic reconstruction.",
            "measurement_scope":"Nominal authored display scale. Exact GLB-coordinate bounds are file measurements, not real-animal/specimen metrology.",
            "limits":"Historical handmade component/intersection assertions and old QA conclusions do not certify this changed geometry. Animation, physical-device performance and composed-scene acceptance are not claimed.",
        }
        row["dimensions"] = bounds["dimensions"]
        row["bounds_glb_m"] = {"min":bounds["min"], "max":bounds["max"]}
        row["triangles"] = audit["triangles"]
        row["primitives"] = len(audit["primitives"])
        row["material_count"] = len(audit["materials"])
        row["sha256"] = {"glb":EXPECTED[id_], "blend":digest(blend_bytes), "preview":preview_hash}
        row["file_sizes"] = {"glb":len(glb_bytes), "blend":len(blend_bytes)}
        row["glb_bytes"], row["blend_bytes"] = len(glb_bytes), len(blend_bytes)
        row["revision"] = RELEASE
        row["quality_status"] = "user_accepted_visual_revision"
        row["acceptance_scope"] = "User accepted this exact current visual revision for integration on 2026-10-30. Current exact-GLB Chromium/SwiftShader static captures are generated, not independent model approval. Earlier local reviews retain their own scope and advisories; no blanket natural-reference, animation, physical-device, interactive-scene or formal production acceptance is asserted. Merge/deployment requires separate authorization."
        row["scale_scope"] = "Nominal authored display scale; measured dimensions match the exact current GLB. Not specimen metrology."
        row["revision_provenance"] = {
            "author":row.get("author", "Leon Made This / s010s"),
            "source_url":"https://github.com/s010s/lowpoly-vault",
            "changes":"Replace the selected same-ID native geometry with the user-selected Meshy-base/Blender-refined revision and exact new static captures; retain all prior source and QA files unchanged as history.",
            "original_author":old.get("author", "Leon Made This / s010s"),
            "original_source_url":old.get("source_url", "https://github.com/s010s/lowpoly-vault"),
            "original_glb_sha256":old["sha256"]["glb"],
            "previous_glb_path":old["glb"],
            "previous_blend_path":old["blend"],
            "previous_preview_path":old["preview"],
            "external_provider":"Meshy",
            "retained_external_base_sha256":m["original_external_base"]["sha256"],
        }
        # Copy the already-reviewed exact-candidate stage record, without changing
        # its conservative pending QA state or touching the source evidence files.
        row["production_provenance"] = copy.deepcopy(provenance)
        row["production_provenance_record"] = evidence["production-provenance.json"]["pin"]
        row["bounded_qa_summary"] = evidence["qa-summary.json"]["pin"]
        row["format_validation_record"] = evidence["gltf-validator.json"]["pin"]
        row["integration_ledger"] = f"production/{RELEASE}/integration-ledger.json"
        row["model_network_payload"] = {
            "glb_bytes":len(glb_bytes), "external_texture_bytes":0, "total_model_bytes":len(glb_bytes),
            "embedded_images":len(audit["images"]),
            "scope":"Downloaded model file plus external model resources only. All current texture resources are embedded. Excludes separately requested editable Blend/ZIP downloads, poster images and shared application code; not a VRAM or GPU-memory estimate.",
        }
        rows[id_] = row
        poster_rows[id_] = {"source_glb_sha256":EXPECTED[id_], "render_route":"webgl-manual-v1", "detailPresentation":DETAIL_POLICY, "wheel":f"gallery/revisions/{RELEASE}/{id_}/wheel.png", "detail":f"gallery/revisions/{RELEASE}/{id_}/detail.png"}
        payloads.append({"id":id_, "glb_bytes":len(glb_bytes), "external_texture_bytes":0, "model_payload_bytes":len(glb_bytes), "blend_download_bytes":len(blend_bytes)})
    check(sum(r["model_payload_bytes"] for r in payloads) == 17300760, "Frozen total model network bytes changed")
    result_manifest = preserve_asset_rows(base_text["assets/manifest.json"], rows)
    result_resources = preserve_resources(base_text["site/public/gallery/resources.json"], poster_rows, image_files)
    # Safety: only the intended root JSON values change; old historical headers stay.
    final_manifest = json.loads(result_manifest)
    check({k:v for k,v in baseline.items() if k != "assets"} == {k:v for k,v in final_manifest.items() if k != "assets"}, "Manifest headers changed")
    for id_, row in rows.items():
        public = json.dumps(row,ensure_ascii=False)
        check("/workspace/" not in public and "drive.google" not in public and "task_id" not in public, "Private field leaked")
        check(row["quality_status"] != original[id_]["quality_status"], "Historical QA status copied")
    output.mkdir(parents=True, exist_ok=False)
    outputs = {"assets/manifest.json":result_manifest, "site/public/gallery/resources.json":result_resources}
    receipts = []
    for relative, text in outputs.items():
        dest = output / relative
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(text,encoding="utf-8")
        receipts.append({"path":relative,"bytes":len(text.encode()),"sha256":digest(text.encode())})
    private_plan = {"visibility":"PRIVATE_DO_NOT_UPLOAD_VERBATIM", "performed_file_copies":False,"operations":copy_plan}
    (output/"COPY-PLAN-PRIVATE.json").write_text(json.dumps(private_plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report = {
        "status":"JSON_OVERLAY_PREPARED_NOT_INSTALLED", "baseline_commit":BASE_COMMIT,"baseline_sha256":BASE_PINS,
        "total_assets":752,"changed_asset_rows":5,"unchanged_asset_row_byte_ranges":747,"historical_resource_entries_preserved":True,
        "new_resource_files":10,"capture_source_commit":capture["source_commit"],"capture_identity_sha256":digest(capture_bytes),"renderer_report_sha256":digest(renderer_bytes),
        "capture_visual_review":"NOT_REVIEWED_BY_THIS_SCRIPT","outputs":receipts,"model_network_payloads":payloads,"total_model_network_bytes":17300760,
        "blend_downloads_not_page_model_payload":True,"external_texture_bytes":0,"copies_performed":False,"repo_modified":False,"git_actions":False,
        "limits":["This script verifies file identity and prepares data; it does not independently review pixels or models.","Independent QA/public-safe stage records are coordinated separately and are not manufactured here.","No old scientific/component-based geometry statements or old independent QA status are transferred to new hashes.","Inherited project license declarations require the separately reviewed generation/output rights evidence; this script is not a license audit."],
    }
    (output/"PREPARE-FINAL-CATALOG-PRIVATE.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report

def self_test():
    fixture={"assets":[{"id":f"m{i}","n":i,"text":"中文"} for i in range(752)],"header":{"keep":True}}
    text=json.dumps(fixture,ensure_ascii=False,indent=2)+"\n"
    replacements={f"m{i}":{"id":f"m{i}","n":i+1} for i in range(5)}
    result=preserve_asset_rows(text,replacements)
    check(json.loads(result)["assets"][5:] == fixture["assets"][5:],"Unchanged fixture rows mismatch")
    r={"head":{"historical":True},"files":[{"path":"old.png","sha256":"a"}],"posters":{f"m{i}":{"x":i} for i in range(7)}}
    t=json.dumps(r,indent=2)+"\n"
    rr=preserve_resources(t,{"m0":{"x":20}},[{"path":"new.png","sha256":"b"}])
    check(json.loads(rr)["posters"]["m0"]["x"]==20,"Poster replacement failed")
    check(json.loads(rr)["files"]==r["files"]+[{"path":"new.png","sha256":"b"}],"File append failed")
    try:
        preserve_resources(t,{},[{"path":"old.png","sha256":"b"}])
    except ValueError:
        pass
    else:
        raise AssertionError("Historical path replacement was not refused")
    print("PASS: lexical replacement, 747 raw rows preserved, resource append, historical path refusal; no repository changed")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path)
    parser.add_argument("--inventory",type=Path,help="Portable JSON: models[].selected_glb/selected_editable_source require repo_path, bytes, sha256; never producer absolute_path")
    parser.add_argument("--capture-dir",type=Path,help="Materialized capture-identity.json, renderer-report.json and images/ from the exact-five wrapper")
    parser.add_argument("--out",type=Path,help="New output directory outside repo; writes JSON only and never installs the overlay")
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:
        self_test()
    else:
        parser.error("--repo --inventory --capture-dir --out are required") if any(x is None for x in (args.repo,args.inventory,args.capture_dir,args.out)) else None
        print(json.dumps(prepare(args.repo,args.inventory,args.capture_dir,args.out),ensure_ascii=False,indent=2))
