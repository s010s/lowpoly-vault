# Museum Environment Research and Scientific Boundaries

Reviewed on 2026-10-16 against museum source snapshot [`dbdb0a3`](https://github.com/s010s/prehistoric-animal-museum/commit/dbdb0a3fc1ec82c586f8aaa45667aac76c424669), dated 2026-10-07. This document contains original summaries and source links, not third-party models, reference images, or downloaded source-code files. A [Simplified Chinese version](museum-research.zh-CN.md) is available.

## What the current project needs

- The museum primarily serves children aged 2–6 and accompanying adults. It emphasizes calm observation and already discloses artistic reconstruction. Environments should therefore be gentle and legible; nests and fallen logs do not need a danger narrative. [Museum README](https://github.com/s010s/prehistoric-animal-museum/blob/dbdb0a3fc1ec82c586f8aaa45667aac76c424669/README.zh-CN.md)
- Its production environments combine distant panoramas, physically based ground materials, and world-space terrain, banks, water, vegetation, and props. They do not form a uniformly lowpoly world. Present this pack independently first, then evaluate style, scale, occlusion, and performance before integration. This assessment comes from source inspection, not a screen-by-screen visual review of the live site. [Environment documentation](https://github.com/s010s/prehistoric-animal-museum/blob/dbdb0a3fc1ec82c586f8aaa45667aac76c424669/src/scale-encounter/environments/land-biomes/README.md)
- The legacy theme ID `gobi` means an Iren Dabasu vegetated floodplain with braided channels and temporary ponds. Do not substitute empty dunes based on the modern Gobi landscape. Dilophosaurus uses a Kayenta-inspired seasonal river valley. Carboniferous coal swamps, Ice Age steppe, ocean, and sky have separate themes. [Theme registry](https://github.com/s010s/prehistoric-animal-museum/blob/dbdb0a3fc1ec82c586f8aaa45667aac76c424669/src/scale-encounter/environment-theme-registry.ts)
- The mammoth environment already has a regional teaching-composite anchor in the Eastern Alps around 45,000 years ago: an ice-free valley, limited seasonal snow, and distant high-elevation ice. This pack has no dedicated Ice Age vegetation; Mesozoic plants should not be used to fill that gap. [Scientific anchor](https://github.com/s010s/prehistoric-animal-museum/blob/dbdb0a3fc1ec82c586f8aaa45667aac76c424669/src/scale-encounter/environments/glacier/scientific-anchor.ts)

## The first ten categories

See [asset-briefs.json](asset-briefs.json) for morphology, uses, suggested dimensions, misleading treatments to avoid, and evidence IDs.

| Asset | Identifying structure to preserve | Supported presentation |
|---|---|---|
| Layered sedimentary outcrop | Coherent bedding, differential recession of hard and soft layers, solid mass | Time-neutral sedimentary-rock concept |
| Natural stone arch | Through-opening, asymmetric supports, substantial arch thickness | Time-neutral erosional-landform concept |
| Conifer tree | Straight main axis, layered lateral branches, crown gaps | Jurassic–Cretaceous concept forest |
| Cycad-inspired plant | Stout low stem, stiff radiating pinnate crown | Mesozoic plant-form concept |
| Ground fern clump | Low curved frond axes, pinnae, limited unfurling growth | Mesozoic fern-form concept |
| Horsetail clump | Segmented stems, nodes, whorled fine branches | Mesozoic moist-margin concept |
| Uprooted log | Horizontal broken trunk, root plate, natural fractures | Mesozoic seed-plant deadwood concept |
| Dinosaur egg nest | Shallow ground nest, egg grouping, central opening | Teaching model inspired by Late Cretaceous oviraptorid nests |
| Three-toed footprint mud patch | Depressions, displaced margins, alternating steps | Mesozoic trackway teaching model without a taxonomic assignment |
| Carboniferous lycopsid tree | Columnar trunk, diamond-shaped leaf cushions, upper dichotomous branches | Late Carboniferous coal-swamp concept in its own theme |

These categories differ in structure and purpose. Recoloring or rescaling does not create another category. The outcrop is a solid bedded mass; the arch is organized around a through-opening. Conifers and arborescent lycopsids use different branching structures. A gallery may display the ten together as a **cross-period asset catalogue**, but must not imply that they coexisted in one place and time.

## Six scientific boundaries

1. **An ancient lineage is not an unchanged modern species.** Living ferns, cycads, and conifers can inform morphology. That does not justify presenting a particular modern species as an exact copy of a Mesozoic plant. [NHM dinosaur garden](https://www.nhm.ac.uk/discover/how-to-grow-a-dinosaur-garden.html), [NHM ferns](https://www.nhm.ac.uk/discover/ferns.html)
2. **Similar crowns do not identify the same plant.** Cycads are not palms, and cycad and bennettitalean reproductive structures should not be combined without evidence. Enlarging a small horsetail does not reconstruct a Carboniferous Calamites tree. [Smithsonian cycads](https://qrius.si.edu/taxonomy/term/11978), [NHM horsetails](https://www.nhm.ac.uk/discover/jurassic-scavenger-hunt.html)
3. **Lycopsid trees need their own structure.** Their diamond-shaped pattern represents leaf cushions, and dichotomous branching differs from conifer lateral branches. Do not apply the modern-style root plate of the uprooted-log asset to a lycopsid. [PRI leaf structure](https://www.digitalatlasofancientlife.org/learn/embryophytes/tracheophytes/leaves/), [PRI branching](https://www.digitalatlasofancientlife.org/learn/embryophytes/tracheophytes/branching/), [Smithsonian coal-swamp research](https://repository.si.edu/bitstreams/27b279ae-6030-4d71-93ba-1b0a713e7399/download)
4. **Rock age is not landform age.** Kayenta sediments support river and floodplain environments, not the existence of today's canyon at the time of deposition. A stone arch may form much later through jointing and erosion. The pack's arch is not assigned to a museum fossil locality. [NPS Kayenta](https://www.nps.gov/zion/learn/nature/kayenta.htm), [NPS arches](https://www.nps.gov/articles/nps-geodiversity-atlas-arches-national-park-utah.htm)
5. **Nearby fossils do not identify a nest's maker.** Do not call this asset a “Gigantoraptor nest,” or suggest that all dinosaurs shared one egg shape, arrangement, and nesting material. Its intact, peaceful presentation is an educational design choice. [AMNH dinosaur eggs](https://www.amnh.org/dinosaurs/dinosaur-eggs), [AMNH associated nest specimen](https://www.amnh.org/research/paleontology/vertebrate/fossil-preparation/follow-the-specimen)
6. **Three toes are not a genus-level signature.** The default asset represents fresh mud depressions, not raised sculpted toes. Do not identify Dilophosaurus from this schematic shape or infer speed from an artistic stride length. A fossil version must distinguish true tracks, undertracks, and natural casts. [NPS footprints](https://www.nps.gov/zion/learn/nature/fossil-footprints.htm)

## Asset disclosure and remaining checks

Suggested disclosure:

> An original stylized model informed by scientific references. Shapes are simplified; colors and some details are artistic choices. It is not an exact reconstruction of a particular species, locality, or moment.

Colors, counts, wear, exact dimensions, and layout are artistic choices. A scientific reconstruction needs a supported classification, stratum, locality, scale, and explicit reasoning for missing parts. Museum and university educational material can support a concept pack but cannot alone replace that evidence chain.

The first pack does not cover marine ecological props, dedicated sky/coastal objects, Ice Age vegetation, or complete ecological communities. Attribute original assets according to this repository's LICENSE and ATTRIBUTION files; cited institutions do not become the model authors or endorsers. Successful model export also does not establish that museum production integration has passed review.

