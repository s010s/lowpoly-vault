> Review appendix: this preserves the domain review history. Earlier filenames/counts refer to that research subset; `inventory.json`, `sources.json` and `counts.json` in this delivery are authoritative. Resolved findings are reconciled below or in `DEDUPLICATION.md`.

# Prehistoric flora, fungi and algae research

Research date: 2026-10-16. Schema version: 2. Planning only.

## Delivery

- `assets.json`: exactly **100** counted concepts; all `status: planned`.
- `sources.json`: **104** bounded source records, including the source retained for the explicitly excluded Voronocladus concept.
- `alternates.json`: empty. The one strong alternate, Marchantites, was promoted into the counted inventory. No spare quota was padded with weak variants.
- 96 plant-form records and 4 fungal records. Plant form facets also accommodate algal and cyanobacterial fossils; these display conventions do not imply that cyanobacteria are plants.
- 47 whole-organism reconstruction concepts and 53 specimen concepts. Isolated fossil organs are intentional specimen/close-up assets, never silently complete plants.
- Evidence: 84 direct, 14 group-supported, 2 candidate.
- Production gates: 49 reference-ready, 25 needs-specific-reference, 17 needs-form-review, 9 needs-taxonomy-review.
- Priority: 10 P1, 36 P2, 52 P3, 2 hold. These are planning judgments, not measured production cost or completed QA.

## Scope and evidence

This collection spans separate geological intervals and regions. It is not a single coexisting ecosystem. Era arrays represent supported planning intervals, not an exhaustive first/last occurrence range. `neoproterozoic` is used only for Proterocladus (near the Tonian boundary) and Flabellophyton (Ediacaran), with explicit notes. Fossil occurrence does not establish a modern species' prehistoric identity. Biomes remain empty when the consulted evidence does not safely support a controlled environment label.

The source registry distinguishes 11 opened sources from 93 search-result sources. The latter were verified through actual indexed abstracts, descriptions or excerpts, but should not be mistaken for a complete read of every paper or every figure. A direct label means the accessed text names the taxon and supports the proposed visible form. It does not claim complete reconstruction, current resolution of every systematic debate, or permission to reproduce an image. Broad teaching sources and historical reconstructions are bounded and flagged. Relevant modern revisions are paired with older specimen descriptions where necessary.

All proposed geometry briefs are original interpretations. Fossil colours, tissue inflation, missing branches, precise crown outlines, substrate arrangement and exact dimensional scale are not presented as observed facts. Relative complexity and scale classes are planning labels. No model files, polygon counts, asset dimensions, export tests or production rights have been invented. Reference-ready means the concept has useful named form evidence, not that a released mesh or complete dimensional/rights audit exists.

## Existing-asset comparisons

The existing generic fern, cycad, conifer, Lepidodendron and horsetail do not exclude every member of their clades. A retained named concept must instead offer a concrete, visible architectural difference:

- Existing fern-cluster is an arching pinnate rosette. New fern concepts use tree/root-mantle architecture, climbing axes, floating linked leaves, palmate rays, broad fused fans, fertile/sterile dimorphism, or specifically preserved trunk anatomy. Ordinary additional pinnate rosettes were not added.
- Existing cycad is a short caudex with stiff pinnate leaves. Cycadeoidea is limited to a trunk specimen with embedded reproductive structures, Bjuvia to an entire strap-leaf specimen, and Wielandiella to a documented branching bennettitalean shrub.
- Existing conifer-tree uses narrow sprays on a tapered branched trunk. Agathis uses documented broad leaves; Pseudofrenelopsis uses jointed near-leafless shoots; Sciadopitys uses a whorled cladode branch specimen. Metasequoia is a fertile, opposite-leaved close-up specimen, not a second generic redwood tree.
- Existing Lepidodendron has diamond leaf cushions and a high dichotomous crown. Sigillaria's vertical scar rows, Paralycopodites' repeated deciduous lateral systems, and smaller isoetalean rooting/cone architectures provide different structural plans. Specific reconstructions remain gated where the genus varies.
- Existing horsetail-cluster uses slender jointed stems and thin radial branch whorls. Calamites is a woody branching tree, Pseudobornia has conspicuously divided leaves, Schizoneura is a broad paired-sheath shoot specimen, and Sphenophyllum has wedge-leaf whorls on climbing axes.

Each asset includes its own bilingual distinctness and modeling brief. A named difference is not enough by itself; the indicated structure must survive a production silhouette/readability review.

## Organ associations and anti-duplication

Default: one counted concept per genus-level biological subject. No asset is counted again for a recolour, size, density, pose, age, sexual state, damage state or different name.

Detached organ associations are recorded in `reference_notes`, not mislabeled as taxonomic synonyms in `aliases`. In particular, the counted concepts already cover these related names for deduplication:

- Calamites: Annularia foliage and Calamostachys reproductive organs.
- Lyginopteris: Lagenostoma lomaxii ovules; Lyginodendron oldhamium is retained as an alternate name.
- Dicroidium: associated Umkomasia and Pteruchus organs.
- Caytonia: associated Sagenopteris foliage.
- Cordaites and other associated organ genera are not extra counts.
- Archaeopteris: Callixylon wood is not a separate asset.
- Nordenskioldia: associated Zizyphoides flabella foliage.
- Macginitiea: associated Macginicarpa glabra and Platananthus synandrus reproductive organs.
- Joffrea: leaves, reproductive shoots, seeds and seedlings belong to the same concept; original spelling J. speirsii and later J. speirsiae are not two taxa.

The following specimen exceptions are deliberate:

- **Araucaria mirabilis** is a Jurassic attached cone/branch specimen with documented rounded cone architecture. Its independent educational/reproductive use is absent from the existing generic conifer tree. No same-taxon living tree or separate detached cone is counted.
- **Williamsonia bockii** is an anatomically studied Cretaceous ovulate cone. It is not asserted to belong to the counted Wielandiella angustifolia shrub, whose older Williamsonia angustifolia name is an alias. Cycadeoidea's embedded reproductive structures remain within its single trunk-specimen concept. This distinction requires taxon-specific reference retention rather than using “bennettitalean cone” as a generic duplicate.
- Glossopteris, Dicroidium, Hausmannia, Baiera, Sabalites and comparable detached foliage concepts do not invent the architecture of an unknown parent tree. Leaf-only evidence is not a license to create a complete plant.
- Quatsinoporites is only the preserved poroid fungal fragment. A complete shelf-shaped bracket is not reconstructed from that fragment.
- Botrychium's fertile and vegetative remains are not organically connected; the brief does not join them into an invented complete plant.

## Paired leaf-specimen form gate (audit #129)

Glossopteris and Bjuvia both use broad, entire, elongate leaf specimens. Both now require `needs-form-review`; direct fossil evidence remains unchanged. Their distinctness is unresolved at the proposed lowpoly viewing scale. A neutral-material, comparable-display-size comparison must demonstrate source-supported blade and modeled vein-relief differences. Colour, texture-only detail, scale, pose, damage or an invisible diagnostic character cannot satisfy this gate. The central rib is shared and is not sufficient. If the netted relief does not read without unsupported exaggeration, consolidate or replace one concept before production. Neither row claims this test has been performed. These are direct-evidence concepts with a production-blocking form comparison, separate from the two low-confidence candidate holds below.

## Current holds and exclusions

**Counted but production-held:**

1. `monetianthus`: direct fossil flower evidence exists, but the specimen is tiny and perianth phyllotaxis is uncertain. It is a low-confidence candidate for an enlarged educational close-up only. Do not produce an environment-scale flower or whole water lily from this row.
2. `proterocladus`: published branching multicellular thalli support the identity, but much of the diagnostic evidence is microscopic. This remains a low-confidence candidate for an explicitly enlarged educational specimen, pending readability and form review. Do not treat its cellular traits as visible environmental geometry.

**Excluded after review:**

- `voronocladus` / Voronocladus dryganti: removed from the counted array because competing interpretations of the upper structures change the proposed body topology. Its source FL-voronocladus is retained only as the exclusion trail: https://commons.emich.edu/fac_sch2024/85/ . It is not a ready alternate.
- Replacement ID: `marchantites` / Marchantites huolinhensis. A primary study describes attached gemma cups on dichotomous, midribbed thalli from 27 specimens. Source FL-marchantites: https://www.sciencedirect.com/science/article/pii/S0195667114000470 . Gemma contents are not asserted to be preserved; small cup readability remains a form-review gate.
- Stromatolites, thrombolites, oncoids, deadwood and ecological structures are outside this domain's scope and were not added.
- No microscopic fungal spore, pollen or cellular-only taxon has been added to reach the quota.

Other cautions are row-specific rather than silently resolved: debated Archaeopteris crowns; variable medullosan habit; Rhacophyton's affinities; historical Sciadopitys cf. material; uncertain Protosalvinia affinity; possible non-natural fossil foliage genera; Marpolia's cyanobacterial status; Winfrenatia's disputed lichen interpretation; and algal thallus thickness lost by compression.

## Taxonomic housekeeping

- Aglaophyton majus retains Rhynia major and Aglaophyton major as historical alternate names.
- Iodes brownii uses the later combination and records Biceratocarpum brownii / Carpolithus browni for deduplication.
- Jimaodanus replaces the preoccupied Heterocladus name; the original morphology paper and replacement-name paper are both cited.
- Bosworthia is scoped to B. simulans; former B. gyges is not silently included after its transfer to Walcottophycus.
- Clypeina is scoped to the Eocene type-species concept C. marginoporella; removed Jurassic C. sulcata material is not conflated with it.
- Gondwanagaricites uses the publication's nomenclatural correction together with the fossil description.
- Joffrea uses J. speirsiae as in later literature and records the original J. speirsii spelling.
- Nidula baltica is paired with its 2021/2022 validating corrigendum (FL-nidula-corrigendum); the model brief uses the corrected holotype images and does not infer additional peridioles.

## Validation

The JSON arrays were checked for exact count, unique kebab-case IDs, mandatory bilingual text, source cross-references, allowed evidence/gate/representation values, explicit reconstruction type, candidate hold priority, and no ID collision with the existing 10 assets. Source records are descriptive research citations, not asset license grants. Final integration should preserve the holds, row-level caveats and specimen/whole-organism distinction.

中文概要：本组包含100项规划概念，其中47项为整株或整体重建，53项为标本概念；另有两项因微小尺度与形态可读性问题暂停制作。年代跨多个地质时期，并非同一生态群落。所列来源不构成复制图片、模型或几何数据的许可。
