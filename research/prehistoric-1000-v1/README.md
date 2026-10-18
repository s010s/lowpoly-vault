# Lowpoly Vault: 1,000 prehistoric asset concepts
## 史前资源概念清单：共 1,000 项

Research snapshot: **2026-10-16** · Catalog schema **v2** · English-first, with Chinese core fields.

**Exactly 1,000 total records = the 10 existing candidates + 990 new planning concepts.** This is a curated research inventory, not 1,000 completed or scientifically approved models. Existing IDs and names are preserved. No new model, mesh, render, polygon budget, export or measured asset dimension was produced.

**Evidence coverage:** 585 direct-form-supported records, 396 group-supported records, and 19 explicitly held candidates. There are 541 cited source records / 541 distinct URLs. 235 sources were opened; 306 were verified through actual indexed results, abstracts or excerpts. Indexed access is not a complete reading of the paper or its figures. **Do not advertise this as “1,000 verified assets.”**

中文要点：总数包含现有 10 项，新增 990 项。已逐项记录中英文名称、辨识结构、制作方向、来源及审核门槛。部分来源只支持类群背景，部分形态或分类仍待核实；这些条目不能直接进入制作。清单不是同一时代、同一地点共存的生态系统，也不是已完成的模型库。

## Contents

- `inventory.json`: authoritative 1,000-record envelope and complete fields.
- `inventory.csv`: the same ordered records, flattened into 40 columns; UTF-8 with BOM.
- `sources.json` / `sources.csv`: cited URL registry with bounded support and access level.
- `registry.json`: schema-v2-compatible worlds, categories, subcategories, packs, eras, biomes and tags.
- `counts.json`: machine-readable totals.
- `DEDUPLICATION.md`: count rule, alias/organ/variant decisions and unresolved form gates.
- `PRODUCTION.md`: ordered production and research queues with IDs.
- `independent-taxonomy-audit.md` / `independent-environment-audit.md`: independent challenge records, including historical findings and revision reconciliation.
- `flora-review.md`, `vertebrate-review.md`, `invertebrate-review.md`: domain-specific evidence and scope notes, when supplied.
- `integrity-audit.json`: mechanical collision checks. A common-name homonym is explained in the deduplication report.
- `validate.py`: standalone validation of delivered JSON, CSV, source references and registry.
- `checksums.sha256`: SHA-256 checksums for delivery files.

## Overview

| Practical category | Count |
|---|---:|
| Animals / 动物 | 700 |
| Fungi / 真菌 | 4 |
| Geological bodies / 地质体 | 65 |
| Plants and algal forms / 植物与藻类形态 | 101 |
| Landforms / 地形 | 89 |
| Traces and ecological structures / 遗迹与生态构造 | 40 |
| Deadwood / 枯木 | 1 |
| **Total / 合计** | **1,000** |

Animals include 110 non-avian dinosaurs, with substantial fish, mammal, amphibian, reptile, bird and invertebrate coverage. The inventory has 7 practical categories, 56 category/subcategory combinations and 34 overlapping pack concepts. Pack membership never increases the record count.

## Shared information architecture

All records use `worlds: ["prehistoric"]`. Worlds, packs, categories, tags, eras and biomes are independent axes, following the shared catalog v2 contract. Category/subcategory describe a practical asset form or use; `taxon_group` holds biological grouping separately. Neither is an assertion of a complete phylogeny. Examples: “synapsid” is a practical non-mammalian grouping; “plants/alga” accommodates fossil algal/cyanobacterial forms without claiming cyanobacteria are plants.

`prehistoric-starter` is the existing candidate pack. Other pack definitions and registry extensions are **planning-only**. This research must not be merged into the live asset manifest, download counts, released filters or sitemap as though the assets exist.

## Scientific scope

- Eras span multiple geological intervals. A row's interval may be a supported example or a provisional planning interval, **not** a complete first/last occurrence range. Read its evidence and caveats together. Empty arrays mean unassigned, not universally compatible.
- Biomes are broad planning labels, not a fossil locality or a claim of regional coexistence. Many remain empty rather than inventing ecology.
- Geological forms can use modern, well-described process analogs. That verifies a form/process, not its presence at a selected prehistoric site. A rock's formation age and its later exposed landform age differ.
- `reconstruction_type` distinguishes **whole-organism**, **specimen**, and **artistic-concept**. Preserved leaves, cones, flowers, shells or incomplete skeletons do not silently become complete living organisms. There is no automatic second count for “living + fossil.”
- Trace fossils are named for trace morphology, not necessarily their makers. Cutaways and relief conventions are illustrative. Trackways do not identify a producer species by themselves.
- Colour, unpreserved skin, soft tissue, missing limbs, crown density and reconstructed inflation are not asserted as observed facts. No fantasy creature or modern human prop was added.
- Chinese names are established common names where checked; otherwise Latin names plus Chinese descriptive labels avoid inventing authoritative vernacular taxonomy.

## Evidence and production gates

| Field | Meaning |
|---|---|
| `direct` | Accessed named reference supports the proposed form or diagnostic structure. Not a complete anatomy or mesh certification. |
| `group-supported` | Reference establishes only the broader group/context; specific identity, interval or distinguishing anatomy needs a dedicated source. |
| `candidate` | Identity, interpretable form or low-poly readability is materially unresolved; priority is `hold`. |
| `reference-ready` | Sufficient named form evidence to begin a careful blockout review. No released-model QA, dimensional validation or image licensing is implied. |
| `needs-specific-reference` | Obtain and read an appropriate named specimen/taxon/process reference before modeling. |
| `needs-taxonomy-review` | Resolve naming, affinity, species or specimen treatment before modeling. |
| `needs-form-review` | Demonstrate a distinctive, supported construction at intended low-poly viewing distance. |

Confidence is a qualitative planning judgment, not a probability. `priority`, `complexity` and `scale_class` are art-direction estimates, not measured cost, exact dimensions or polygon counts. `specifications` is null for all 990 planned concepts. Existing measurements are inherited metadata snapshots and were not remeasured here.

There are 343 reference-ready concepts; 657 records still have an explicit review gate. Production queues also respect `priority: hold`, which may conservatively defer a record even when its source is direct. See `PRODUCTION.md`; evidence and priority are intentionally not the same thing.

## Research method and limits

1. Read the ten existing asset descriptions and preserve their generic status, IDs and names.
2. Allocate non-overlapping research domains and coordinate practical facets with the site schema owner.
3. Search museum, university, geological-survey, botanical-institution and primary-paper references. Record actual URLs and the exact bounded claim supported; one source can support multiple concepts.
4. Write original bilingual visual criteria and low-poly briefs. Separate taxonomic facts from reconstruction choices and unknowns.
5. Challenge close pairs, historic synonyms, detached-organ associations, whole-versus-specimen choices and the existing generic silhouettes. Replace weak padding candidates, rather than filling quotas with recolours or damage states.
6. Run independent domain/global reviews plus automated count, bilingual-field, alias, genus-token, source-resolution and CSV round-trip checks.

This pass is substantial but not exhaustive taxonomy: alias lists are selective, many group-supported records need primary specimen work, and no 3D silhouette comparison has been performed because modeling has not begun. Taxonomy can change after the snapshot date. The review files document unresolved conditions rather than disguising them as passes.

## Machine-readable conventions

JSON is authoritative and includes extra scoped notes where available. CSV fields ending `_json` contain valid JSON arrays, objects, strings or null; do not split those cells on commas or semicolons. `source_ids_json` joins to the source registry; `source_urls_json` is supplied for convenience. Stable IDs, not English or Chinese display names, are keys. Preserve all caveats and production gates when importing.

Core localized objects are `name`, `description`, `distinctness`, `modeling_brief` and `scientific_scope`. Some technical review notes remain English-only. The JSON `trace_display` and inherited existing-asset provenance remain available even when not separate CSV columns.

Run `python validate.py` in this folder to validate the delivered bundle. It uses only Python's standard library.

## Use of references

References support research; they do **not** grant rights to copy photographs, museum scans, diagrams or third-party meshes. Build original geometry. Obtain permissions or use appropriately licensed visual material for later production. Source availability and search indexing can change. The independent appendices preserve earlier review snapshots; their final reconciliation and the consolidated inventory supersede resolved historical findings.

中文制作原则：先核实分类与标本，再以同尺度、同姿势、灰色材质比较结构；颜色、尺寸、姿态、密度、年龄或损伤变化不另计。若关键差异在低多边形简化后消失，应合并或替换条目，而不是硬凑数量。
