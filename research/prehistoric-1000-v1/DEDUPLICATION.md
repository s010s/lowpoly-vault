# Distinctness and deduplication audit / 去重审核

Snapshot: 2026-10-16. **Counted inventory: 1,000 = 10 existing + 990 new.** These are distinct proposed subjects/use concepts under the stated rules, with unresolved anatomy/form gates retained. No claim is made that 1,000 finished meshes have passed visual QA.

## Passes established mechanically

- Exactly 1,000 unique kebab-case IDs.
- Exactly 10 existing candidates, retaining original IDs, names and categories; 990 planned records.
- No repeated normalized English display names, exact taxon strings or first genus tokens in the delivered inventory.
- Every counted row has a resolved source ID and the five required bilingual text objects.
- CSV IDs, ordering, localized names, core fields and source links match JSON.
- Packs are many-to-many references to the same IDs, never repeated counted rows.

The genus-token test cannot detect all synonyms, homonyms, organ associations or uncertain taxonomic assignments. Sparse alias lists must not be advertised as exhaustive nomenclatural validation.

## Count rule

A separate record needs a meaningful independently identifiable taxon, geological type, form, function or specimen use **and** a defensible visual construction. A name alone is insufficient for production. Recolouring, scaling, changing pose/crown density, adding damage, or splitting detachable parts does not create a new counted asset. Juvenile/adult and male/female variations are not quota fillers. Generic current plants retain their generic identities rather than being retroactively assigned species.

One genus-level biological subject is the default. A specimen is counted instead of its unknown whole organism, not automatically alongside it. No same-genus living organism + isolated fossil is counted twice. Distinct specimen uses across different subjects still require a readable anatomical difference.

## Known alias collision: resolved as a naming collision

`otodus` has the familiar shark common name “Megalodon.” `megalodon-bivalve` refers to the historically named bivalve genus, not the shark. Their organism groups and construction differ completely. They must not be merged by string matching. The bivalve row remains taxonomy-held because traditional Triassic megalodontid identifications need a species/specimen treatment; the existence of this homonym does not validate every old assignment to that genus.

## Replacements and corrections made during review

| Earlier proposal | Final counted treatment | Reason |
|---|---|---|
| Butte | Eruptive fissure | Avoided mesa/butte proportion-only differentiation. |
| Bajada | Reticulite clast | Avoided a mere repetition/assembly of alluvial fans. |
| Glacial outwash plain | Fulgurite tube | Avoided overlap with a braided-river reach. |
| Standing hollow snag | Boudinaged rock layer | Avoided damage/pose variations of generic deadwood. |
| River logjam | Treptichnus serial-probe burrow | Avoided counting an assembly of repeated logs. |
| Nunatak | Staurolite cross-twin | Avoided a summit distinguished mainly by surrounding ice. |
| Malachite botryoid | Stylolite seam section | Avoided near-duplicate rounded mineral clusters. |
| Hollow fallen log | Lava tree-mold crust | Removed another damage-state log; new record is a negative cavity in continuous rock, not wood. |
| Miragaia | Gigantspinosaurus | Removed disputed Miragaia/Dacentrurus two-slot dependence; retained supported conspicuous shoulder-spine architecture. |
| Pohlsepia | Paleocadmus | Updated the 2026 nautiloid reinterpretation; no obsolete octopus body is retained. |
| Alienoptera | Alienopterus | Corrected an order-level label to the supported genus/species concept. |
| Orthoceras | Yochelcionella | Removed duplicate simple straight-shell risk beside Baculites and commercial-name ambiguity. |
| Hamites | Capinatator | Removed duplicate paperclip-shell construction beside Diplomoceras. |
| Lichenoides | Sollasina | Selected a more distinct, supported echinoderm construction. |
| Voronocladus | Marchantites | Replaced contested upper-body topology with documented thallus/gemma-cup architecture. |

These earlier proposals are review history, not additional counted alternatives. Other nomenclatural updates include Biceratocarpum → Iodes, Heterocladus → Jimaodanus, and spelling reconciliation for Joffrea. Associated organ names are recorded as associations, not mislabeled synonyms.

## Parent/part and generic/specific tests

- Calamites/Annularia/Calamostachys, Lyginopteris/Lagenostoma, Dicroidium/Umkomasia/Pteruchus, Caytonia/Sagenopteris, Archaeopteris/Callixylon, and Macginitiea-associated reproductive organs are not additional counted parent/part sets.
- Araucaria mirabilis is one documented cone/branch specimen, with no same-taxon whole tree or detached-cone second slot. Williamsonia bockii is a supported cone specimen, not an assumed organ of the separate Wielandiella angustifolia concept.
- Existing fern, horsetail, cycad, conifer and lycopsid concepts were compared against the proposed architecture. New specimens/whole plants need branch topology, leaf construction, attachment, root/stem architecture or a specific specimen use, not denser or larger versions of the same silhouette.
- Fossil marks, shells, carapaces and cutaways stay explicit about preserved evidence. A convenient hypothetical complete animal is not inferred from a fragment.

## Taxonomic/specimen safeguards

- Shonisaurus/Shastasaurus require different species/specimen anchors; do not use the same sikanniensis skeleton under two genera.
- Carcharodontosaurus must not use the Egyptian material reassigned to Tameryraptor as if it were the Moroccan C. saharicus specimen.
- Oviraptor must use its own skull evidence, not a borrowed Citipati crest.
- Tapejara and Tupandactylus must not duplicate historical “Tapejara imperator” material.
- Nectocaris uses the 2025 stem-chaetognath discussion and does not retain an unqualified squid funnel/tentacle reconstruction.
- Nidula baltica uses the validating corrigendum and corrected figure identities; unseen peridioles are not invented.
- Disputed affinities and candidate microscopic forms remain held. A changed catalog bucket does not settle a scientific phylogeny.

## Remaining visual-review conditions

The independent review contains 150 numbered close-pair/cohort challenges. Many identify legitimate named subjects whose short briefs are not yet sufficient to approve distinct production meshes. In particular: similar theropods; Brachiosaurus/Giraffatitan; Apatosaurus/Brontosaurus; very-long-necked plesiosaurs; some shells and coral colonies; early algal forms; and superficially similar fossil organs require specimen-based comparisons.

For terrain and geology, explicit guards include linear/transverse dune slope topology; rimstone versus terraced pools versus non-pooling flowstone; crystal pockets in continuous host rock versus a free geode; distinct volcanic cone construction; and geometry-bearing rock fabrics rather than recolouring the existing stratified cliff. Planolites and Skolithos must show their sediment context, not simply the same tube rotated.

**Production acceptance test:** compare neutral-grey blockouts at normalized scale and common pose/view; identify a source-backed geometric criterion that remains readable at intended viewing distance. If no criterion survives, merge or replace a slot and re-run the exact-count audit. Holds are work to resolve, not evidence that this test already passed.

中文概要：本次已排查名称别名、同属重复、器官与母体、通用形态与具体分类单元，以及缩放／换色／密度／姿态／损伤变体。已移除明确的凑数风险。仍有形态、标本或分类审核项；后续模型必须通过同尺度灰模对比，不能把审核状态当作已验证的独特性。
