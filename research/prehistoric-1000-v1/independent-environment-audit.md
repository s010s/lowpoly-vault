> Review appendix: this preserves the domain review history. Earlier filenames/counts refer to that research subset; `inventory.json`, `sources.json` and `counts.json` in this delivery are authoritative. Resolved findings are reconciled below or in `DEDUPLICATION.md`.

# Independent environmental concept audit

Audit date: 2026-10-16. Reviewed the complete 190-row `environment/curated.tsv`, the ten records in `existing-assets.json`, and canonical `docs/catalog-schema-v2.md`. This is a concept/brief review, not mesh QA or certification of the complete 1,000-record inventory. No source inventory files were modified.

## Decision summary

Replace four current slots to make the distinct-count claim substantially stronger:

1. **Butte**: redundant with Mesa under the user's ban on scale/proportion padding.
2. **Bajada**: an aggregate of the already listed Alluvial fan; density/composition padding.
3. **Standing hollow snag**: retain only one of this and Hollow fallen log. The present pair mainly changes a hollow trunk's orientation and anchoring. My preference is to retain the two-ended Hollow fallen log because its traversable tube is clearly distinct from the existing solid, rooted `uprooted-log`.
4. **River logjam**: valuable scene assembly, but the present brief is interlocked copies of trunks. A barrier function alone does not establish a distinct original model concept. Keep it as a scene recipe outside the unique-asset count.

Also resolve the **Braided river reach / Glacial outwash plain** overlap before finalizing. The latter's present brief is another branching-channel gravel plain; source-supported glacial origin alone does not change its mesh. Either replace it or expressly design an integrated ice-front-to-outwash transition with a different terrain structure, subject to the inventory owner's composite-asset rule. Replacement is the cleaner conservative choice.

These are count-quality judgments, not claims that the scientific terms are synonyms.

## High-confidence redundancy findings

### Mesa / Butte

The NPS describes mesas as broad flat-topped mountains and buttes as smaller flat-topped mountains or hills. Both current briefs use a flat resistant cap with steep walls; the stated differentiator is explicitly compact versus broad proportions. Retain Mesa; replace Butte. Do not solve this by adding cracks or changing erosion detail.

Source: [NPS, About Arches, Buttes & Rock Formations](https://www.nps.gov/subjects/rockformations/about.htm).

### Alluvial fan / Bajada

USGS explicitly defines a bajada as several fans that meet and overlap. The current brief accurately describes this geology but adds no independent constituent form. Retain Alluvial fan and treat bajada arrangement as a future scene recipe.

Sources: [USGS, Geology of Joshua Tree](https://www.usgs.gov/geology-and-ecology-of-national-parks/geology-joshua-tree-national-park); [USGS, Alluvial fans and bajadas](https://pubs.usgs.gov/of/2004/1007/fans.html).

### Braided river reach / Glacial outwash plain

NPS identifies actively forming outwash plains as expansive flat areas dominated by braided rivers. A generic branching gravel plain cannot uniquely establish its glacial origin. Grain-size grading represented only by colors or clast density also fails the user's rule. The paired briefs currently need a replacement or substantive geometry revision.

Source: [NPS, Outwash Plains and Eskers](https://www.nps.gov/articles/outwashplainsandeskers.htm).

### Hollow deadwood and logjam

The existing `uprooted-log` has a solid tapering trunk, torn branches, a root plate and soil. One genuinely hollow trunk is an addition because an open internal cavity changes topology and scene use. Counting both an upright hollow snag and the same basic hollow trunk lying down is much weaker. Root/no-root distinction should not rescue a rotated hollow trunk when an existing root-plate log already covers that feature.

A logjam can make a good authored diorama, but the current brief adds only arrangement and multiplicity. If composites are exempted, the same exemption would also rescue Bajada and undermine the no-density rule. Recommend consistency: keep both logjam and bajada outside the distinct-model count.

## Source-backed replacement candidates

Choose four for the four recommended removals, or five if replacing outwash as well. These descriptions are original modeling directions derived from geological/ichnological identities; references do not grant permission to copy meshes or illustrations.

### 1. Eruptive fissure terrain / 裂隙喷发地形

- Proposed form: terrain/volcanic-fissure.
- Geometry: a long, irregular open eruptive crack with locally welded lips and lateral lava breakouts into the surrounding ground; no central cone and no row of repeated cones.
- Distinction: a surface source fissure differs from the positive-standing Dike wall, rounded Fumarole vent, and open downhill Lava channel.
- Scope: generic process analogue; no named volcano, eruption date or asserted prehistoric locality.
- Evidence: NPS distinguishes elongated fissure vents from central-vent edifices and describes dikes reaching the surface.
- Source: [NPS, Fissure Volcanoes](https://www.nps.gov/articles/000/fissure-volcanoes.htm).

### 2. Reticulite clast / 网状玻质火山渣块

- Proposed form: geology/pyroclast.
- Geometry: one irregular fragile clast formed from intersecting glass struts enclosing open, connected polyhedral cells. Model real holes, not a solid rock with dark dimples.
- Distinction: skeletal open-cell foam is unlike Volcanic bomb, Accretionary lapilli bed, angular Breccia, or continuous Pahoehoe surface. Do not separately add generic pumice solely to obtain another porosity/density variant.
- Scope: an illustrative volcanic material; modern reference supports its form, not a precise geological age or locality.
- Source: [USGS, Reticulite and Kīlauea's caldera](https://www.usgs.gov/observatories/hvo/news/volcano-watch-almost-nothing-enough-reticulite-helps-measure-depth-kilaueas).

### 3. Boudinaged rock layer / 石香肠构造岩层

- Proposed form: geology/deformed-layer.
- Geometry: a competent layer stretched into separated sausage/lozenge-shaped lenses, with surrounding softer material pinching into the intervening necks. Expose the topology on a broken outcrop face.
- Distinction: interrupted, pinched segmentation differs from the continuous bending sheets in Folded strata and Slump-folded bed. Merely recoloring bands would not suffice.
- Scope: generic deformation structure, not a specific metamorphic event.
- Source: [Connecticut Geological Survey, The Bedrock Geology of the Collinsville Quadrangle, fig. 10 and Boudinage section](https://portal.ct.gov/-/media/DEEP/geology/QuadReports/QR16pamphletpdf.pdf).

### 4. Treptichnus serial-probe burrow / Treptichnus 连续探穴

- Proposed form: traces/feeding-burrow.
- Geometry: an angular zigzag of successively connected short J/U-shaped probes, each extending just beyond its joining point to make a short terminal projection; include shallow three-dimensional downbows.
- Distinction: serial angular probes are neither Chondrites' branching tree, Phycodes' terminal broom, nor a featureless Planolites tube. Avoid using a generic curved tube or beaded trail: those would overlap existing concepts.
- Scope: ichnogenus-inspired trace geometry, no identified animal producer; broad range only when directly supported.
- Source: [University of Kansas Ichnology, Treptichnus](https://ichnology.ku.edu/invertebrate_traces/tfimages/treptichnus.html).

### 5. Lava tree-mold terrain / 熔岩树模地面

- Proposed form: geology/tree-mold.
- Geometry: a continuous lava-crust patch enclosing a deep blind cylindrical trunk void, with an exposed side section showing a thin chilled lining and bark-impression relief; no surviving wooden trunk.
- Distinction: a negative biological mold embedded within a flow differs from a free hollow wooden log or open conduit. The integrated crust and preserved negative bark structure must be modeled, rather than substituting a generic hole.
- Scope: generic forest/lava interaction analogue; use only in a world with trees, and do not claim the modern Hawaiian reference identifies an ancient species or formation.
- Sources: [NPS, Lava Trees and Tree Molds](https://www.nps.gov/havo/learn/nature/lava-trees.htm); [NPS, Volcanoes and Fossils](https://www.nps.gov/subjects/fossils/volcanoes-and-fossils.htm).

## Conditional near-duplicates: retain only with geometry guardrails

These are not automatic removals. Different process or geological type can support separate concepts when the stated mesh actually expresses it.

- **Linear dune / Transverse dune ridge**: orientation to an invisible wind is not a mesh distinction. Give the linear dune an elongated two-flank ridge architecture and the transverse dune an explicitly asymmetric, laterally continuous slipface. Transverse must not simply be repeated Barchans. NPS describes crescentic, linear, star and parabolic morphological groups and the coalescence of barchans into ridges: [NPS, Monitoring Aeolian Features](https://home.nps.gov/articles/aeolian.htm).
- **Nunatak / Glacial horn / Inselberg**: Nunatak is a rock island surrounded by flowing ice, not an exclusive summit shape. A lone peak recolored at the base fails. If retained, require bifurcating/rejoining ice margins and a rock island with an original planform; otherwise it is a scene assembly. [NPS, Nunataks, Arêtes, and Horns](https://www.nps.gov/articles/nunataksareteshorns.htm).
- **Dogtooth spar cavity / Geode cavity**: preserve an irregular pocket in continuous host bedrock versus a free rounded hollow nodule with an enclosing rind. Pointed crystals alone must not be both entries' entire distinction. NPS supports the pocket/vug setting and pointed calcite morphology: [Wind Cave formations](https://www.nps.gov/wica/learn/nature/cave-formations-speleothems.htm).
- **Rimstone dam / Travertine terrace pools / Flowstone cascade**: one enclosing thin dam, linked stepped shelves, and continuous non-pooling lobes are distinct structures; don't implement all three as resized copies of the same scalloped pool mesh. Their current descriptions can support distinct geometry if followed.
- **Cave popcorn / Malachite botryoid**: both are connected rounded nodules. Different mineral names and green coloring are insufficient. Malachite needs a substantive broken cross-section exposing radial/concentric growth relief, while cave popcorn remains attached growth on host rock. If that distinction cannot survive low-poly simplification, replace one. NPS confirms popcorn encompasses knobby and botryoidal forms: [NPS, Speleothems](https://www.nps.gov/subjects/caves/speleothems.htm).
- **Stratified Cliff / Coal seam / Banded iron formation / Banded gneiss / Schist**: do not recolor the existing cliff mesh. Coal needs recess/cleat structure; BIF needs fine persistent laminated erosion relief; gneiss needs folded coarse segregated bands; schist needs platy foliation controlling fracture. The existing cliff is broad inclined sedimentary bedding. Rock names alone do not establish a unique mesh.
- **Stratovolcano / Cinder cone / Spatter cone**: retain composite flank ridge/flow architecture, loose fragment cone around a broad crater, and irregular welded spatter walls, respectively. A scaled generic crater cone fails. [NPS, Anatomy of a Volcano](https://home.nps.gov/subjects/volcanoes/anatomy-of-a-volcano.htm).
- **Planolites / Skolithos**: do not rely just on rotating a smooth tube. Keep a winding bedding-parallel tunnel versus straight shafts penetrating a visibly sectional block. The contextual sediment geometry is doing important work; if identical free tubes are delivered, the distinctness claim fails.

## Scientific wording and period controls

1. **Ignimbrite outcrop** should read **Welded ignimbrite outcrop** to match Chinese 熔结凝灰岩 and its flattened inclusions. USGS discusses variable usage of ignimbrite/ash-flow tuff and confirms that welding is not universal: [USGS, Ignimbrite or tuff?](https://www.usgs.gov/observatories/calvo/news/ignimbrite-or-tuff).
2. **Hormosiroidea bead-chain trace**: avoid implying settled genus-level taxonomy. Suggested label: **Rosary-shaped chambered burrow (Hormosiroidea-type)** / **珠链状腔室潜迹（Hormosiroidea 型）**. Some revisions merge it with Halimedides; a recent primary paper discusses continued disagreement and the spherical-versus-heart-shaped chamber distinction. It can remain one morphological concept; never count the competing names separately. [Geological Magazine, 2026 systematic discussion](https://www.cambridge.org/core/journals/geological-magazine/article/ediacaran-or-late-paleozoic-integrating-trace-fossils-and-upb-geochronology-to-resolve-paleoenvironmental-and-stratigraphic-ambiguities/40E949AB3F78F67B9F978F556B9C08AD).
3. **Pentichnus / Asteriacites** can remain separate. Preserve a deep pentameral plug versus a shallow star with widely spreading tapered arms; not merely a deeper copy of the same star. KGS explicitly distinguishes the deep dwelling architecture and notes Carboniferous records, which should not silently become all-era availability. [Kansas Geological Survey systematic ichnology](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno2.html).
4. **Daemonelix** should not enter a dinosaur-era preset merely because it is a trace. The cited Agate forms are dry-land-beaver burrow casts; use an appropriately sourced Cenozoic context. The current corkscrew and terminal chamber geometry is distinct from the sheet-like Zoophycos. [NPS, Molds, Casts, and Steinkerns](https://home.nps.gov/articles/000/mold-casts-and-steinkerns.htm).
5. **Banded iron formation** needs formation-age versus exposed-rock-age wording. The major deposits are characteristically ancient; a later exposed outcrop is possible but does not mean active BIF deposition in a generic dinosaur scene. Do not infer a single precise interval from a modern outcrop reference. [USGS mineral-resource overview](https://pubs.usgs.gov/of/2005/1294/a/of2005-1294a.pdf).
6. Generic glaciers, dunes, caves, volcanic surfaces and modern analogue sites do not imply coexistence with every organism in the catalog. Their era arrays should be empty/appropriately broad with explicit generic-process notes unless a source supports a particular reconstruction. Snow or an active glacier should not automatically mean Pleistocene.
7. For burrows, distinguish void reconstruction, sediment fill/cast, and exposed fossil relief in the record. Do not silently switch all of them into positive free-standing pipes; that both misleads scientifically and collapses useful mesh distinctions.

## Findings against the existing ten

- No newly listed generic natural arch duplicates `natural-arch`.
- No newly listed tridactyl theropod print duplicates `three-toed-track`; sauropod manus/pes and pterosaur hand/foot patterns require genuinely different impression geometry.
- No additional dinosaur nest currently duplicates `dinosaur-nest`.
- The main existing-asset collision risks are the deadwood variants against `uprooted-log` and visually generic banded-rock specimens against `stratified-cliff`.
- Keep all existing IDs unchanged. Any replacement is a new planned record, not a relabeling of an existing asset.

## Final acceptance check

After replacements, recount records globally, confirm exactly 10 existing plus 990 planned, and verify that no proposed replacement already appears in another research domain's inventory. This audit does not establish that global count. Before production, compare normalized grey silhouettes, topology and sectional structure with materials disabled; reject concepts whose only distinction disappears with color, scale, orientation, or multiplicity removed.

## Inventory-owner resolution received after audit

The owner accepted Butte → Eruptive fissure, Bajada → Reticulite, Standing hollow snag → Boudinaged layer, and River logjam → Treptichnus. The owner also chose to replace Glacial outwash plain, retain Hollow fallen log for its through-cavity, and add a Hormosiroidea-type naming caveat. These are accepted revision decisions, not independent verification that the working inventory has already been changed.

For the fifth replacement the owner proposed **Fulgurite tube / 闪电熔结管**. This is defensible as a different origin and materially different thin-walled glass structure. Require an irregular exposed hollow with a fused inner wall and adherent granular exterior, rather than a recolored burrow cast. [NPS, Fulgurites: The Power of Lightning](https://www.nps.gov/articles/grsa-fulgurites.htm) supports lightning-fused sand/glass tubes; [Environment and Climate Change Canada, Fulgurites](https://www.canada.ca/en/environment-climate-change/services/lightning/learn-more/fulgurites.html) explicitly supports thin, hollow tubes. These two retrieved texts do not explicitly establish a branching pattern; source that detail separately if it is included. The Lava tree-mold option above remains an alternate, not an additional required row.
