#!/usr/bin/env python3
"""Join the frozen coverage inventory to human visual review decisions."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews/natural-appearance-nonbiota-20261019"


def main() -> None:
    coverage = json.loads((OUT / "coverage.json").read_text())
    decisions = json.loads((OUT / "review_decisions.json").read_text())
    visual_manifest = json.loads((OUT / "evidence/visual-manifest.json").read_text())
    visual_by_id = {entry["asset_id"]: entry for entry in visual_manifest}
    if len(visual_by_id) != len(visual_manifest):
        raise ValueError("Visual manifest has duplicate asset ids")

    rows = [asset for asset in coverage["assets"] if asset["scope_disposition"] == "in_scope"]
    ids = [asset["asset_id"] for asset in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("In-scope inventory has duplicate asset ids")

    reviewed: list[dict] = []
    for source in sorted(rows, key=lambda a: (a["batch"], a["asset_id"])):
        decision = decisions["assets"].get(source["asset_id"], {})
        image = visual_by_id.get(source["asset_id"])
        available = source["availability"] == "available" and bool(source["model_path"])
        if available:
            if not image:
                raise ValueError(f"{source['asset_id']}: available model lacks rendered evidence")
            if image["source_glb_sha256"] != source["actual_glb_sha256"]:
                raise ValueError(f"{source['asset_id']}: image source hash differs from coverage pin")
            if image["source_model_path"] != source["model_path"]:
                raise ValueError(f"{source['asset_id']}: image source path differs from coverage pin")
            image_path = image["image_path"]
            visual_status = "six_views_pixel_inspected"
            verdict = decision.get("verdict", decisions["default_verdict"])
            finding = decision.get("finding", decisions["default_finding"])
            minimum = decision.get("minimum_improvement", decisions["default_minimum_improvement"])
            priority = decision.get("priority", "")
        else:
            image_path = ""
            visual_status = "not_generated_not_pixel_inspected"
            verdict = "unavailable"
            finding = source.get("display_context") or "Latest recovery handoff records this in-scope model as not generated."
            minimum = "No visual repair recommendation until an actual model exists and can be reviewed."
            priority = "blocked_by_missing_model"

        version = source["revision"]
        if source.get("selected_attempt"):
            version += f" / {source['selected_attempt']}"
        elif source.get("source_type") == "published_main":
            version += " (frozen published baseline)"

        reviewed.append({
            "asset_id": source["asset_id"],
            "scope_relationship": {
                "published_main": "frozen_baseline_responsibility",
                "candidate": "unreleased_candidate",
                "paused_batch50": "unreleased_unbuilt_candidate",
            }[source["source_type"]],
            "source_type": source["source_type"],
            "batch": source["batch"],
            "category": source["category"],
            "subcategory": source["subcategory"],
            "version": version,
            "revision": source["revision"],
            "selected_attempt": source["selected_attempt"],
            "source_ref": source["source_ref"],
            "source_commit": source["source_commit"],
            "handoff_ref": source["handoff_ref"],
            "handoff_commit": source["handoff_commit"],
            "handoff_path": source["handoff_path"],
            "model_path": source["model_path"],
            "model_record_path": source.get("model_record_path", ""),
            "brief_path": decision.get("brief_path", source.get("brief_path", "")),
            "reference_path": decision.get("reference_path", ""),
            "metadata_path": source.get("metadata_path", ""),
            "source_glb_sha256": source["actual_glb_sha256"],
            "availability": source["availability"],
            "visual_status": visual_status,
            "image_path": image_path,
            "image_sha256": image["image_sha256"] if image else "",
            "representation": decision.get("representation", "natural_form_or_display_sample") if available else "not_inspected_model_missing",
            "verdict": verdict,
            "priority": priority,
            "finding": finding,
            "minimum_improvement": minimum,
            "reference_note": decision.get("reference_note", ""),
        })

    required_ids = set(ids)
    if set(decisions["assets"]) - required_ids:
        extra = sorted(set(decisions["assets"]) - required_ids)
        raise ValueError(f"Review decisions refer to out-of-scope or missing ids: {extra}")
    if len(visual_by_id) != coverage["in_scope_models_available"]:
        raise ValueError("Rendered evidence count differs from available in-scope model count")

    count = Counter(row["verdict"] for row in reviewed)
    summary = {
        "frozen_baseline": coverage["frozen_baseline"],
        "published_baseline_assets": coverage["published_baseline_assets"],
        "published_baseline_in_scope": coverage["published_baseline_in_scope"],
        "candidate_batches_reviewed_for_coverage": [f"batch-{n}" for n in range(40, 51)],
        "discovered_assets_total": coverage["discovered_assets_total"],
        "in_scope_discovered_total": coverage["in_scope_discovered_total"],
        "available_models_pixel_inspected": sum(row["visual_status"] == "six_views_pixel_inspected" for row in reviewed),
        "not_generated_not_pixel_inspected": sum(row["visual_status"] == "not_generated_not_pixel_inspected" for row in reviewed),
        "unreleased_available_candidate_models": sum(row["scope_relationship"] == "unreleased_candidate" for row in reviewed),
        "verdict_counts": dict(sorted(count.items())),
        "review_date": decisions["review_date"],
    }
    output = {"summary": summary, "items": reviewed}
    (OUT / "review.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    fields = list(reviewed[0].keys())
    with (OUT / "review.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(reviewed)

    write_report(coverage, summary, reviewed)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def write_report(coverage: dict, summary: dict, reviewed: list[dict]) -> None:
    out = []
    out += [
        "# Non-biota natural-appearance review",
        "",
        "Review date: 2026-10-19  ",
        f"Frozen published baseline: `{coverage['frozen_baseline']}` (175 assets).  ",
        "Scope: geology, terrain and trace assets; animal, plant, fungi and wood categories excluded.",
        "",
        "## Coverage",
        "",
        "The inventory is keyed by exact `asset_id` so the same asset is never counted twice as a separate model just because a revision exists. It covers the 175-asset frozen baseline and the latest available handoffs for batches 40–50. The batch-44 source is the requested handoff commit `49b1d6cddd807c89884935974ee2de1bc27bd0fb`.",
        "",
        f"- Total discovered across baseline and handoffs: **{summary['discovered_assets_total']}** asset records.",
        f"- In-scope asset IDs: **{summary['in_scope_discovered_total']}** = **{coverage['published_baseline_in_scope']}** frozen-baseline assets + **{summary['unreleased_available_candidate_models']}** available candidate models + **{summary['not_generated_not_pixel_inspected']}** in-scope models not generated in batch 50.",
        f"- Available in-scope models visually inspected: **{summary['available_models_pixel_inspected']}**; all have a six-angle contact sheet tied to source GLB SHA-256 in `evidence/visual-manifest.json`.",
        f"- Per-asset results: **{summary['verdict_counts'].get('usable', 0)} usable**, **{summary['verdict_counts'].get('needs_change', 0)} needs change**, **{summary['verdict_counts'].get('unavailable', 0)} unavailable**.",
        "- Two batch-50 in-scope IDs (`karst-sinkhole`, `fault-scarp`) were prepared but not built; they are uninspected, not visual passes.",
        "- Batches 49 and 50 remain paused/incomplete per their handoffs. Visual inspection of available candidate GLBs here does not assert independent QA or batch completion.",
        "- The baseline `dinosaur-nest` and `three-toed-track` are included because the frozen manifest categorizes them as traces; this review covers those exact IDs as traces.",
        "",
        "The complete source paths, revision/attempt labels, source commits, hashes, scope relation, verdict, and image paths are in `review.csv` and `review.json`. `coverage.csv` and `coverage.json` retain all 219 discovered baseline/candidate records, including excluded categories and source handoff status.",
        "",
        "## How the pixels were reviewed",
        "",
        "Each available source GLB was hash-checked against the pinned inventory, imported into a controlled orthographic studio setup, rendered as six 512×512 angles (hero, reverse hero, front, side, rear, top), and assembled as a 1600×1182 contact sheet. I directly inspected all 74 contact sheets. The standardized light and background make silhouettes, proportions, relief, layering, repetition and broad material/color cues comparable; this is an asset-level visual review, not a product-scene or lighting integration check. No visual pass is inferred from QA JSON alone.",
        "",
        "Verdicts describe whether the model reads naturally enough for a stylized child-friendly 3D world. They are not claims of strict scientific reconstruction. Purposeful sections, cast surfaces, and trace slabs remain labeled as such; their flat display face is not by itself treated as a defect. Recommendations are deliberately bounded to small visible edits, not micro-detail work.",
        "",
        "## Main visual findings",
        "",
        "| Asset | Exact version | Priority | What reads unnaturally | Smallest improvement | Evidence |",
        "|---|---|---:|---|---|---|",
    ]
    for item in reviewed:
        if item["verdict"] != "needs_change":
            continue
        version = item["version"].replace("|", "\\|")
        finding = item["finding"].replace("|", "\\|")
        improve = item["minimum_improvement"].replace("|", "\\|")
        image_rel = item["image_path"].replace("reviews/natural-appearance-nonbiota-20261019/", "")
        image = f"[six views]({image_rel})" if item["image_path"] else "unavailable"
        out.append(f"| `{item['asset_id']}` | {version} | {item['priority']} | {finding} | {improve} | {image} |")
    out += [
        "",
        "The cross-bedded sandstone is a special case. Its brief describes a child-friendly teaching exposure with three cross-bed sets and physical lamina truncations; the flat teaching face and cutaway are intentional. The fresh views show those wedges reading clearly. The finding is limited to the uniform brick-like exterior and repetitive side rhythm, and the recommended tweak leaves the teaching geometry intact. The brief’s reference record says source image pixels were not viewed, so this is not a comparison against a specimen photograph.",
        "",
        "## Items visually usable as delivered",
        "",
        f"The remaining **{summary['verdict_counts'].get('usable', 0)}** available IDs are marked usable for this bounded natural-appearance check. Their specific identity, exact version, source hash and inspected contact sheet are listed in `review.csv` / `review.json`; no required natural-appearance edit was apparent at the six reviewed angles. This includes intentional teaching sections whose flat display planes support the stated use.",
        "",
        "## Not available to inspect",
        "",
        "| Asset | Handoff | State | Visual result |",
        "|---|---|---|---|",
    ]
    for item in reviewed:
        if item["verdict"] != "unavailable":
            continue
        out.append(f"| `{item['asset_id']}` | `{item['handoff_commit']}` | not generated | no pixels available; not inspected |")
    out += [
        "",
        "## Limits and disposition",
        "",
        "This is a read-only visual review. No model, gate, website, CI, or release file was changed. It does not change candidate QA state or release authority. The high-priority shape and repetition findings are suitable for the baseline-correction discussion before another publish batch; no merge or deployment was performed.",
        "",
        "## Evidence and machine-readable deliverables",
        "",
        "- `review.csv` — one row per in-scope asset ID with verdict, version, source hash and contact-sheet link.",
        "- `review.json` — same per-asset results plus aggregate counts.",
        "- `coverage.csv` / `coverage.json` — source/handoff coverage for all discovered records, with hash pins and incomplete handoff states.",
        "- `evidence/multiview/` — full 6-angle pixel evidence for all 74 available models.",
        "- `evidence/visual-manifest.json` — render settings, source hash, contact-sheet hash and dimensions.",
        "- `review_decisions.json` — authored concise dispositions and minimum suggested improvements.",
        "",
    ]
    (OUT / "report.md").write_text("\n".join(out))


if __name__ == "__main__":
    main()
