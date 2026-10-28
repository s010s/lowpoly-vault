/** Exact frozen source facts, not a new QA decision or publication grant. */
const deepFreeze=x=>{if(x&&typeof x==="object"){Object.values(x).forEach(deepFreeze);Object.freeze(x);}return x;};
export const SOURCE_PROFILES = deepFreeze([
  {
    "entry_id": "banded-iron-formation-far-lod",
    "stable_model_id": "banded-iron-formation",
    "configuration": "far-lod",
    "operation": "same_model_representation_entry",
    "original_documents": {
      "original_review": {
        "sha256": "7dce5d0984dae65c4f41d4867cf92a9020da55a33c37d12ab180ea16df557b42",
        "bytes": 7326
      },
      "original_qa_event": {
        "sha256": "89129feee2655290519d5ac76652bcbbdfcb4163f909043a1038598176b7f701",
        "bytes": 6594
      },
      "original_maker_evidence": {
        "sha256": "a20b528d201d574ff59a16aaed2d78a0782e998bacab92c77169a9beb69316ba",
        "bytes": 5913
      }
    },
    "original_report_pointer": "/report/sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/status",
      "value": "PASS_SCOPED_FAR_ASSET"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/candidate/sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/native/sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/banded-iron-formation-far-lod/model.glb",
        "sha256": "680b358071c0097bda7745ef66f1cde02145cf0cdf00ea5ed7462b9cb95e9d36",
        "bytes": 963992
      },
      "blend": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/banded-iron-formation-far-lod/source.blend",
        "sha256": "e5e9386027ac96b8d2e271531c1abbcd3238153f3255d21e0dc9dc32b8f5a322",
        "bytes": 1631088
      }
    },
    "maker": {
      "id": "resume_model_rolling_coordination/make_old_corrective_batch10",
      "task_id": "resume_model_rolling_coordination/make_old_corrective_batch10"
    },
    "reviewer": {
      "id": "resume_model_rolling_coordination/review_old_corrective_batch12",
      "task_id": "resume_model_rolling_coordination/review_old_corrective_batch12"
    },
    "maker_pointer": {
      "document": "original_maker_evidence",
      "pointer": "/worker"
    },
    "maker_link": {
      "kind": "DIRECT_QA_EVENT_HANDOFF_HASH",
      "pointer": "/maker_handoff/sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/task"
    },
    "identity_supplement": null,
    "original_scoped_statements": {
      "original_host_world_goal": "NOT_RUN_STILL_OPEN"
    },
    "public_semantics": {
      "id": "banded-iron-formation-far-lod",
      "name": {
        "en": "Banded iron formation form study — far-LOD variant",
        "zh": "条带状铁建造 — 远景LOD变体"
      },
      "description": {
        "en": "Separately supplied far-LOD variant of the existing banded-iron-formation model. The original teaching/near representation is retained. Bounded static-source acceptance only; no automatic runtime LOD, host/world, GPU, or user visual approval is inferred. Folded-band far representation with a fixed color/normal atlas; no geological composition, age, locality or unique genesis is inferred.",
        "zh": "既有 banded-iron-formation 模型单独提供的远景LOD变体，保留原教学/近景表示；不是新物种。仅限原已验收静态源范围，不推断自动LOD、宿主/世界、GPU或用户视觉认可。"
      },
      "dimensions": [
        0.866278737783432,
        0.671999990940094,
        0.44130145013332367
      ],
      "units": "meters",
      "triangles": 5940,
      "source_model_identity": {
        "stable_model_id": "banded-iron-formation",
        "original_catalog_id": "banded-iron-formation",
        "original_catalog_glb_sha256": "e1ce2df854e001919b7105c56c0f6a26cabc9b84a163f2a89ae1cadcbac2ba38",
        "representation_configuration": "far-lod",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": true,
    "source_limits": "PASS_SCOPED_FAR_ASSET",
    "all_originals_preserved": true
  },
  {
    "entry_id": "calamites-crown-lod0",
    "stable_model_id": "calamites",
    "configuration": "lod0",
    "operation": "same_model_representation_entry",
    "original_documents": {
      "original_review": {
        "sha256": "bcb2fc8cbc21e461e9b70231d1eab07abefff87e595e56c60eec8e1227a95d09",
        "bytes": 8471
      },
      "original_qa_event": {
        "sha256": "570b4610116d1b206aabc0c66a72a4c01de651e77d9f15a240020d2b9134c5c9",
        "bytes": 8290
      },
      "original_maker_evidence": {
        "sha256": "2bffb29fea66fc081b5b24c234cc54c0e2d3dee6f457f330821717a641e3e50a",
        "bytes": 6008
      },
      "coordinator_snapshot": {
        "sha256": "936416e6e4bebbdbb4d2f68a9bf58ca5565e36c6346703665c4df97c839fac2a",
        "bytes": 92150
      }
    },
    "original_report_pointer": "/evidence/3/sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/phase",
      "value": "PASS_SCOPED_PAIRED_CROWN_PROPORTION_STATIC_ASSET"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/outputs/0/glb_sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/outputs/0/blend_sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/calamites-crown-lod0/model.glb",
        "sha256": "2a5a35caa10878d8ed34727620da2f81c6b3e3b62c59d15cdd269e1061db9e0d",
        "bytes": 508444
      },
      "blend": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/calamites-crown-lod0/source.blend",
        "sha256": "4038a7ad501ac1f939581a642c5bbabdb134c9179190a83edc1d42c6da6a513f",
        "bytes": 1459272
      }
    },
    "maker": {
      "id": "resume_model_rolling_coordination/make_old_corrective_batch08",
      "task_id": "resume_model_rolling_coordination/make_old_corrective_batch08"
    },
    "reviewer": {
      "id": "resume_model_rolling_coordination/review_old_corrective_batch09",
      "task_id": "resume_model_rolling_coordination/review_old_corrective_batch09"
    },
    "maker_pointer": {
      "document": "coordinator_snapshot",
      "pointer": "/issues/calamites-original-ground-tip-crown-lod-20261024/proposed_crown_proportion_work/maker_worker"
    },
    "maker_link": {
      "kind": "DIRECT_QA_EVENT_HANDOFF_HASH",
      "pointer": "/maker_handoff/sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/worker"
    },
    "identity_supplement": {
      "kind": "EXACT_COORDINATOR_SNAPSHOT_NOT_ORIGINAL_MAKER_TASK_FIELD",
      "original_ledger_sha256": "95cb4afdbc8c8726525a465be3c242611352097cc5edff852f3a700cbc77a0b7",
      "original_pointer": "/issues/calamites-original-ground-tip-crown-lod-20261024/proposed_crown_proportion_work",
      "maker_handoff_sha256": "2bffb29fea66fc081b5b24c234cc54c0e2d3dee6f457f330821717a641e3e50a",
      "paired_candidate_sha256": {
        "lod0": {
          "glb_sha256": "2a5a35caa10878d8ed34727620da2f81c6b3e3b62c59d15cdd269e1061db9e0d",
          "blend_sha256": "4038a7ad501ac1f939581a642c5bbabdb134c9179190a83edc1d42c6da6a513f"
        },
        "lod1": {
          "glb_sha256": "1558c46c95af5c2a262efa3374844278962cfc9d9d52ebdc356014897a6bf061",
          "blend_sha256": "43853870c7d53ea9d70bb287e622a43803fda2a2dfc5d744fab12c232ea417af"
        }
      }
    },
    "original_scoped_statements": {
      "remaining_open": [
        "Original tip concern disposition",
        "Host burial/seating and world integration",
        "Runtime shadow/culling/LOD",
        "GPU and formal whole-world acceptance"
      ],
      "counts_and_claims": {
        "additional_static_configuration_of_existing_Calamites": true,
        "eighth_distinct_old_model": false,
        "distinct_new_qualified_model_increment": 0,
        "existing_seven_distinct_models_unchanged": true,
        "old_chain3_HOLD_preserved": true,
        "original_source_and_prior_LOD1_unchanged": true,
        "scientific_correction": false,
        "whole_original_problem_closed": false,
        "user_acceptance": "pending",
        "private_backup": "pending",
        "integrated": false,
        "published": false
      }
    },
    "public_semantics": {
      "id": "calamites-crown-lod0",
      "name": {
        "en": "Calamites form study — crown-proportion variant · LOD0",
        "zh": "芦木形态研究 — 冠幅变体 · LOD0"
      },
      "description": {
        "en": "Separately supplied crown-proportion variant · LOD0 of the existing calamites model. The original teaching/near representation is retained. Bounded static-source acceptance only; no automatic runtime LOD, host/world, GPU, or user visual approval is inferred. Fixed paired crown-proportion source-art configuration; original tip and host concerns are not declared resolved.",
        "zh": "既有 calamites 模型单独提供的冠幅变体 · LOD0，保留原教学/近景表示；不是新物种。仅限原已验收静态源范围，不推断自动LOD、宿主/世界、GPU或用户视觉认可。"
      },
      "dimensions": [
        2.5739359855651855,
        4.800000190734863,
        2.5032739639282227
      ],
      "units": "meters",
      "triangles": 9660,
      "source_model_identity": {
        "stable_model_id": "calamites",
        "original_catalog_id": "calamites",
        "original_catalog_glb_sha256": "44fec258d990ba04a28211ecd8f0c6bfc25071e2a8fdadf7fc864507c9168238",
        "representation_configuration": "lod0",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": true,
    "source_limits": "PASS_SCOPED_PAIRED_CROWN_PROPORTION_STATIC_ASSET",
    "all_originals_preserved": true
  },
  {
    "entry_id": "calamites-crown-lod1",
    "stable_model_id": "calamites",
    "configuration": "lod1",
    "operation": "same_model_representation_entry",
    "original_documents": {
      "original_review": {
        "sha256": "bcb2fc8cbc21e461e9b70231d1eab07abefff87e595e56c60eec8e1227a95d09",
        "bytes": 8471
      },
      "original_qa_event": {
        "sha256": "570b4610116d1b206aabc0c66a72a4c01de651e77d9f15a240020d2b9134c5c9",
        "bytes": 8290
      },
      "original_maker_evidence": {
        "sha256": "2bffb29fea66fc081b5b24c234cc54c0e2d3dee6f457f330821717a641e3e50a",
        "bytes": 6008
      },
      "coordinator_snapshot": {
        "sha256": "936416e6e4bebbdbb4d2f68a9bf58ca5565e36c6346703665c4df97c839fac2a",
        "bytes": 92150
      }
    },
    "original_report_pointer": "/evidence/3/sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/phase",
      "value": "PASS_SCOPED_PAIRED_CROWN_PROPORTION_STATIC_ASSET"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/outputs/1/glb_sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/outputs/1/blend_sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/calamites-crown-lod1/model.glb",
        "sha256": "1558c46c95af5c2a262efa3374844278962cfc9d9d52ebdc356014897a6bf061",
        "bytes": 453000
      },
      "blend": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/calamites-crown-lod1/source.blend",
        "sha256": "43853870c7d53ea9d70bb287e622a43803fda2a2dfc5d744fab12c232ea417af",
        "bytes": 1354812
      }
    },
    "maker": {
      "id": "resume_model_rolling_coordination/make_old_corrective_batch08",
      "task_id": "resume_model_rolling_coordination/make_old_corrective_batch08"
    },
    "reviewer": {
      "id": "resume_model_rolling_coordination/review_old_corrective_batch09",
      "task_id": "resume_model_rolling_coordination/review_old_corrective_batch09"
    },
    "maker_pointer": {
      "document": "coordinator_snapshot",
      "pointer": "/issues/calamites-original-ground-tip-crown-lod-20261024/proposed_crown_proportion_work/maker_worker"
    },
    "maker_link": {
      "kind": "DIRECT_QA_EVENT_HANDOFF_HASH",
      "pointer": "/maker_handoff/sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/worker"
    },
    "identity_supplement": {
      "kind": "EXACT_COORDINATOR_SNAPSHOT_NOT_ORIGINAL_MAKER_TASK_FIELD",
      "original_ledger_sha256": "95cb4afdbc8c8726525a465be3c242611352097cc5edff852f3a700cbc77a0b7",
      "original_pointer": "/issues/calamites-original-ground-tip-crown-lod-20261024/proposed_crown_proportion_work",
      "maker_handoff_sha256": "2bffb29fea66fc081b5b24c234cc54c0e2d3dee6f457f330821717a641e3e50a",
      "paired_candidate_sha256": {
        "lod0": {
          "glb_sha256": "2a5a35caa10878d8ed34727620da2f81c6b3e3b62c59d15cdd269e1061db9e0d",
          "blend_sha256": "4038a7ad501ac1f939581a642c5bbabdb134c9179190a83edc1d42c6da6a513f"
        },
        "lod1": {
          "glb_sha256": "1558c46c95af5c2a262efa3374844278962cfc9d9d52ebdc356014897a6bf061",
          "blend_sha256": "43853870c7d53ea9d70bb287e622a43803fda2a2dfc5d744fab12c232ea417af"
        }
      }
    },
    "original_scoped_statements": {
      "remaining_open": [
        "Original tip concern disposition",
        "Host burial/seating and world integration",
        "Runtime shadow/culling/LOD",
        "GPU and formal whole-world acceptance"
      ],
      "counts_and_claims": {
        "additional_static_configuration_of_existing_Calamites": true,
        "eighth_distinct_old_model": false,
        "distinct_new_qualified_model_increment": 0,
        "existing_seven_distinct_models_unchanged": true,
        "old_chain3_HOLD_preserved": true,
        "original_source_and_prior_LOD1_unchanged": true,
        "scientific_correction": false,
        "whole_original_problem_closed": false,
        "user_acceptance": "pending",
        "private_backup": "pending",
        "integrated": false,
        "published": false
      }
    },
    "public_semantics": {
      "id": "calamites-crown-lod1",
      "name": {
        "en": "Calamites form study — crown-proportion variant · LOD1",
        "zh": "芦木形态研究 — 冠幅变体 · LOD1"
      },
      "description": {
        "en": "Separately supplied crown-proportion variant · LOD1 of the existing calamites model. The original teaching/near representation is retained. Bounded static-source acceptance only; no automatic runtime LOD, host/world, GPU, or user visual approval is inferred. Fixed paired crown-proportion source-art configuration; original tip and host concerns are not declared resolved.",
        "zh": "既有 calamites 模型单独提供的冠幅变体 · LOD1，保留原教学/近景表示；不是新物种。仅限原已验收静态源范围，不推断自动LOD、宿主/世界、GPU或用户视觉认可。"
      },
      "dimensions": [
        2.5739359855651855,
        4.800000190734863,
        2.5032739639282227
      ],
      "units": "meters",
      "triangles": 8340,
      "source_model_identity": {
        "stable_model_id": "calamites",
        "original_catalog_id": "calamites",
        "original_catalog_glb_sha256": "44fec258d990ba04a28211ecd8f0c6bfc25071e2a8fdadf7fc864507c9168238",
        "representation_configuration": "lod1",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": true,
    "source_limits": "PASS_SCOPED_PAIRED_CROWN_PROPORTION_STATIC_ASSET",
    "all_originals_preserved": true
  },
  {
    "entry_id": "cave-popcorn-far-lod",
    "stable_model_id": "cave-popcorn",
    "configuration": "far-lod",
    "operation": "same_model_representation_entry",
    "original_documents": {
      "original_review": {
        "sha256": "59eadba1d5c1b266cc06eac208f0e35520780ea1404f6f952f8070a8730f777e",
        "bytes": 3348
      },
      "original_qa_event": {
        "sha256": "3b653b4ccaf9f8eb106e95cf3bbc32ed0b9ec92fead8731b9e8523c867057810",
        "bytes": 4846
      },
      "original_maker_evidence": {
        "sha256": "5a827a4fca576a1d6f09fd4848e6614776220b2a99f8f5afbd731d9fc1d75d3c",
        "bytes": 13618
      }
    },
    "original_report_pointer": "/report/sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/status",
      "value": "PASS_SCOPED_SAME_SOURCE_FAR_LOD_STATIC_SUPPLY"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/candidate/sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/native/sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/cave-popcorn-far-lod/model.glb",
        "sha256": "9766dc1fe8ccb2c09d2e889f33bfb0d54a462df4f666224fa1f297d2c3264b55",
        "bytes": 407364
      },
      "blend": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/cave-popcorn-far-lod/source.blend",
        "sha256": "c8d25dc3a860b56e64395a2b1b2605bb9dd2d736555f1c62d14535e7435cd92d",
        "bytes": 1113736
      }
    },
    "maker": {
      "id": "resume_model_rolling_coordination/make_old_corrective_batch08",
      "task_id": "resume_model_rolling_coordination/make_old_corrective_batch08"
    },
    "reviewer": {
      "id": "resume_model_rolling_coordination/review_old_corrective_batch10",
      "task_id": "resume_model_rolling_coordination/review_old_corrective_batch10"
    },
    "maker_pointer": {
      "document": "original_maker_evidence",
      "pointer": "/task"
    },
    "maker_link": {
      "kind": "DIRECT_QA_EVENT_HANDOFF_HASH",
      "pointer": "/maker_handoff/sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/task"
    },
    "identity_supplement": null,
    "original_scoped_statements": {
      "remaining_open": [
        "host embedding and wall normal placement",
        "receiver/collision/nav",
        "actual LOD switch and flicker",
        "physicalGPU",
        "wholeworld/formalacceptance",
        "userapproval",
        "privatebackup verification",
        "integration/publication"
      ]
    },
    "public_semantics": {
      "id": "cave-popcorn-far-lod",
      "name": {
        "en": "Cave popcorn — far-LOD variant",
        "zh": "洞穴葡萄状结核 — 远景LOD变体"
      },
      "description": {
        "en": "Separately supplied far-LOD variant of the existing cave-popcorn model. The original teaching/near representation is retained. Bounded static-source acceptance only; no automatic runtime LOD, host/world, GPU, or user visual approval is inferred. Same-source static far representation; original near geometry remains separately available.",
        "zh": "既有 cave-popcorn 模型单独提供的远景LOD变体，保留原教学/近景表示；不是新物种。仅限原已验收静态源范围，不推断自动LOD、宿主/世界、GPU或用户视觉认可。"
      },
      "dimensions": [
        0.550000011920929,
        0.2560162339359522,
        0.4000000059604645
      ],
      "units": "meters",
      "triangles": 5000,
      "source_model_identity": {
        "stable_model_id": "cave-popcorn",
        "original_catalog_id": "cave-popcorn",
        "original_catalog_glb_sha256": "36439f98c26784601b24ba4ac18c709f51c3ef9b071e0225438aaec42b7ba85b",
        "representation_configuration": "far-lod",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": true,
    "source_limits": "PASS_SCOPED_SAME_SOURCE_FAR_LOD_STATIC_SUPPLY",
    "all_originals_preserved": true
  },
  {
    "entry_id": "coal-seam-outcrop",
    "stable_model_id": "coal-seam-outcrop",
    "configuration": "candidate",
    "operation": "same_id_successor",
    "original_documents": {
      "original_review": {
        "sha256": "cc4d341df2d7b3ee6681b75bcaf1f875787f61e1b0a1d84c9e6ac30fb6c43a33",
        "bytes": 10436
      },
      "original_qa_event": {
        "sha256": "430ca3290ca5103587b5b7fb36fb7bfcb318d20a77619bffc45a692545398997",
        "bytes": 4862
      },
      "original_maker_evidence": {
        "sha256": "c8748c4f4604ba447962470d8f03e6ce68017aca7ff0b71bb158274fe6512824",
        "bytes": 8316
      },
      "maker_checksum": {
        "sha256": "e5fd1acdc453e9d30f77d74e40770c42fd3e930ec7c6de169fcf3a8ef659ee0f",
        "bytes": 9716
      }
    },
    "original_report_pointer": "/report_sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/status",
      "value": "PASS_SCOPED_LOCAL_END_NATURALIZATION"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/candidate_glb_sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/candidate_blend_sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/coal-seam-outcrop/model.glb",
        "sha256": "4f3cc2472ef5aa32cf46382d8d957c6696e8b76b7dc064835d040cf9590e3eb7",
        "bytes": 597068
      },
      "blend": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/coal-seam-outcrop/source.blend",
        "sha256": "f289a43d2065e99887cc3039f6b91ad326154826429abeadf10e8a0c02562154",
        "bytes": 1249072
      }
    },
    "maker": {
      "id": "coordinate_model_rolling_batches/make_coal_bed_controlled_ends",
      "task_id": "coordinate_model_rolling_batches/make_coal_bed_controlled_ends"
    },
    "reviewer": {
      "id": "coordinate_model_rolling_batches/review_old_repairs_batch04",
      "task_id": "coordinate_model_rolling_batches/review_old_repairs_batch04"
    },
    "maker_pointer": {
      "document": "original_maker_evidence",
      "pointer": "/worker"
    },
    "maker_link": {
      "kind": "QA_CHECKSUM_MANIFEST_HANDOFF_MEMBER",
      "pointer": "/maker_manifest_sha256",
      "member": "HANDOFF-EVENT.json"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/worker"
    },
    "identity_supplement": null,
    "original_scoped_statements": {
      "accepted_scope": [
        "actual visible nonconvex end retreat improvement at fixed512/256",
        "coal/resistant-bed identification retained",
        "source/common-C/central/material/matrix preservation within documented numeric tolerances",
        "necessary local render/geometry/cap/contact/native/CPU runtime checks"
      ],
      "not_accepted_or_not_run": [
        "complete original neighbouring-rock/world target",
        "strict unchanged old Ymax/Zmin extrema",
        "global manifold/Boolean solid certification",
        "target GPU/WebGL",
        "collision/navigation/LOD",
        "user acceptance",
        "private backup/download integrity",
        "integration/GitHub submission/merge/deployment"
      ]
    },
    "public_semantics": {
      "id": "coal-seam-outcrop",
      "name": {
        "en": "Coal seam outcrop form study",
        "zh": "煤层露头"
      },
      "description": {
        "en": "Generic human-scale coal-seam source-art correction. Non-convex end retreat reduces the straight-cut wedge appearance while retaining the coal and resistant-bed reading. Actual neighbouring-rock connection remains untested; this is not a global manifold or Boolean-solid certificate. Very small triangles and the recorded local normal differences remain disclosed numerical limitations. No named mine, age, coal rank, gas or permeability measurement is inferred.",
        "zh": "通用人尺度煤层露头源美术修正版，以非凸端部退缩弱化齐切楔体读感，保留煤层及抗蚀床层识别。尚未接入真实邻岩，不承诺全局流形或布尔实体认证；极小三角及已记录局部法线差保留为数值限制。不推断特定矿井、年代、煤阶、含气量或渗透率。"
      },
      "dimensions": [
        3.30360746383667,
        2.568094687536359,
        1.474614143371582
      ],
      "units": "meters",
      "triangles": 12855,
      "source_model_identity": {
        "stable_model_id": "coal-seam-outcrop",
        "original_catalog_id": "coal-seam-outcrop",
        "original_catalog_glb_sha256": "f86f6b501899b116915b1d6d037926617508f37d0e3f1bbb21f109f20e9118d3",
        "representation_configuration": "candidate",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": false,
    "source_limits": [
      "actual visible nonconvex end retreat improvement at fixed512/256",
      "coal/resistant-bed identification retained",
      "source/common-C/central/material/matrix preservation within documented numeric tolerances",
      "necessary local render/geometry/cap/contact/native/CPU runtime checks"
    ],
    "all_originals_preserved": true
  },
  {
    "entry_id": "flute-cast-slab",
    "stable_model_id": "flute-cast-slab",
    "configuration": "candidate",
    "operation": "same_id_successor",
    "original_documents": {
      "original_review": {
        "sha256": "8f98c87f726d2ee512bf4075edfa08f4623f06e8f834e37cc84b4553c8fb3b58",
        "bytes": 11077
      },
      "original_qa_event": {
        "sha256": "ac6c4bebff1708eb2d39d9f76202751534aa91dcf68f460e02f6a4907726dd26",
        "bytes": 7862
      },
      "original_maker_evidence": {
        "sha256": "43c22be324aa013cdb12f72ccd12742ff2916aacd78f9d8c06fe8a153a5750ff",
        "bytes": 5975
      }
    },
    "original_report_pointer": "/artifacts/0/sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/verdict",
      "value": "PASS"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/candidate_glb_sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/candidate_blend_sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/flute-cast-slab/model.glb",
        "sha256": "b962166e288aae0a1ca73f7436b7faa0310f7376cdd9b8242a9f1dd6f71378ee",
        "bytes": 267376
      },
      "blend": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/flute-cast-slab/source.blend",
        "sha256": "5fa2c24b0ab1aae20ea98d14e3e744e2728e46cb99c0ed660ce0b2ada5c6c742",
        "bytes": 1208660
      }
    },
    "maker": {
      "id": "make_old_repairs_batch02",
      "task_id": "make_old_repairs_batch02"
    },
    "reviewer": {
      "id": "review_old_repairs_batch02",
      "task_id": "review_old_repairs_batch02"
    },
    "maker_pointer": {
      "document": "original_maker_evidence",
      "pointer": "/task"
    },
    "maker_link": {
      "kind": "DIRECT_QA_EVENT_HANDOFF_HASH",
      "pointer": "/maker_handoff_sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/task"
    },
    "identity_supplement": null,
    "original_scoped_statements": {},
    "public_semantics": {
      "id": "flute-cast-slab",
      "name": {
        "en": "Flute cast exposed bed-sole teaching slab",
        "zh": "槽模岩板露出层底教学模块"
      },
      "description": {
        "en": "Generic teaching slab with six positive spoon-shaped sole casts deliberately shown sole-face-up. The irregular cropped perimeter and modest ordinary-view readability improvement preserve the raised casts; final longest span is 0.583 m, not the original uncut nominal 0.60 m. Placement, relief and color remain original art choices. Not a measured specimen, exact paleoflow reconstruction, host-integrated rock or process simulation.",
        "zh": "教学展示主动将层底朝上，保留六个同向正凸匙状模铸。不规则裁边及普通视图下的适度可读性改进不改变正凸模语义；最终最长跨距0.583米，不把原未裁件名义0.60米当作当前精确尺寸。排列、浮雕与配色仍为原创美术设定，不是实测标本、精确古流向重建、已接入宿主的岩体或过程模拟。"
      },
      "dimensions": [
        0.37599945068359375,
        0.055040955543518066,
        0.5830000042915344
      ],
      "units": "meters",
      "triangles": 10787,
      "source_model_identity": {
        "stable_model_id": "flute-cast-slab",
        "original_catalog_id": "flute-cast-slab",
        "original_catalog_glb_sha256": "4ebbbc5561e622b2ce2fa777dfc6ec4236b1c6fa736a5caf14d290142f5b2268",
        "representation_configuration": "candidate",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": false,
    "source_limits": "Irregular stone edge and modest ordinary-view readability improvement of six positive casts; host/world/GPU/user acceptance/release not covered.",
    "all_originals_preserved": true
  },
  {
    "entry_id": "mudpot",
    "stable_model_id": "mudpot",
    "configuration": "candidate",
    "operation": "same_id_successor",
    "original_documents": {
      "original_review": {
        "sha256": "d1fd8f5dd7e3b7ef1469d51af5ba036b46290180007984a878bf8a39a4a1dd05",
        "bytes": 10325
      },
      "original_qa_event": {
        "sha256": "52b73a17291ea6b17b56e5f1b7cfec4559ced8f8ac583cb12ce5accec0c9e3df",
        "bytes": 5616
      },
      "original_maker_evidence": {
        "sha256": "f4f9de0d13e667563cc37e5ca231862bd8d79616624baafc808ab50aca9c7f21",
        "bytes": 6056
      }
    },
    "original_report_pointer": "/artifacts/0/sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/verdict",
      "value": "PASS"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/candidate_glb_sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/candidate_blend_sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/mudpot/model.glb",
        "sha256": "bc4fafd0c92887edc2b4689aa09489ca05cff53db139bc6b2c43519bb0d0f7d0",
        "bytes": 504772
      },
      "blend": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/mudpot/source.blend",
        "sha256": "aa41448ff087e6a7a0cf9ec64456091cfa3152c2a46fad194f1cdfb3f703ad4b",
        "bytes": 946580
      }
    },
    "maker": {
      "id": "make_old_repairs_batch02",
      "task_id": "make_old_repairs_batch02"
    },
    "reviewer": {
      "id": "review_old_repairs_batch02",
      "task_id": "review_old_repairs_batch02"
    },
    "maker_pointer": {
      "document": "original_maker_evidence",
      "pointer": "/task"
    },
    "maker_link": {
      "kind": "DIRECT_QA_EVENT_HANDOFF_HASH",
      "pointer": "/maker_handoff_sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/task"
    },
    "identity_supplement": null,
    "original_scoped_statements": {},
    "public_semantics": {
      "id": "mudpot",
      "name": {
        "en": "Mudpot form study",
        "zh": "泥浆池"
      },
      "description": {
        "en": "Generic static mudpot source-art correction. The final approximately 5.22 × 4.18 m footprint has 0.49 m relief: two broad low shoulders, a variable apron and a non-enclosing light rim weaken the regular shallow-tray appearance. Three low domes and one collapsed cup remain. The open-root surface has not been joined to a geothermal host; broad color patches remain a style limitation. No named Yellowstone feature, eruption, chemical composition, temperature or physical simulation is claimed.",
        "zh": "通用静态泥火山源美术修正版，最终占地约5.22×4.18米、高差约0.49米。两处宽低肩、变化的外裙及不闭合浅色边弱化规则浅盘读感，保留三个低泥泡和一个塌陷杯。开放根部尚未接入实际地热宿主；较大色块仍属风格限制。不主张特定黄石地貌、喷发、化学组成、温度或物理模拟。"
      },
      "dimensions": [
        5.221174955368042,
        0.4860956631600857,
        4.176406145095825
      ],
      "units": "meters",
      "triangles": 6160,
      "source_model_identity": {
        "stable_model_id": "mudpot",
        "original_catalog_id": "mudpot",
        "original_catalog_glb_sha256": "7818b6e324a8da1f93db36fcb09c989bf0b98c3d4fa02873ae8750daf41f4bf1",
        "representation_configuration": "candidate",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": false,
    "source_limits": "Original visible tray-like enclosing rim materially weakened; coarse color-patch aesthetic limitation retained; no actual host/GPU/user acceptance/release.",
    "all_originals_preserved": true
  },
  {
    "entry_id": "oncoid-bed",
    "stable_model_id": "oncoid-bed",
    "configuration": "candidate",
    "operation": "same_id_successor",
    "original_documents": {
      "original_review": {
        "sha256": "255dac030460a81e853d695cc3553f453da567c25065f222bdede4e2baad7a83",
        "bytes": 6304
      },
      "original_qa_event": {
        "sha256": "74c126a453dbfb578757bf6339f1ebf9c2b30243a0d393a1f2b77b4b459461c8",
        "bytes": 5953
      },
      "original_maker_evidence": {
        "sha256": "c79ffafbd2c131c04b4542f769ff1dd28d2cc7a2f4bd6f7dd161a2b0bd6335a8",
        "bytes": 6043
      }
    },
    "original_report_pointer": "/qa_report_sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/verdict",
      "value": "PASS_SCOPED_SOURCE_ART_CORRECTION02_NO_ADDED_NODULE_OVERLAP"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/candidate_glb_sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/candidate_blend_sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/oncoid-bed/model.glb",
        "sha256": "e7d1d99d272800e4d43dd559233dd514efa9cc0c5668fdfc235e69979fbcfbb2",
        "bytes": 326756
      },
      "blend": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/oncoid-bed/source.blend",
        "sha256": "89645e386916747d155a1e206be81a829eba3fadd9b3ed0ef7b94d6f408bee9e",
        "bytes": 954604
      }
    },
    "maker": {
      "id": "resume_model_rolling_coordination/make_old_corrective_batch04",
      "task_id": "resume_model_rolling_coordination/make_old_corrective_batch04"
    },
    "reviewer": {
      "id": "resume_model_rolling_coordination/review_old_corrective_batch05",
      "task_id": "resume_model_rolling_coordination/review_old_corrective_batch05"
    },
    "maker_pointer": {
      "document": "original_maker_evidence",
      "pointer": "/worker"
    },
    "maker_link": {
      "kind": "DIRECT_QA_EVENT_HANDOFF_HASH",
      "pointer": "/maker_handoff_sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/worker"
    },
    "identity_supplement": null,
    "original_scoped_statements": {
      "qualification_scope": "Approved bounded source-art: two whole-shell restorations,one small off-center nucleus/uneven fracture,limited placement andthin irregular sediment edge; strict no-added-grain-overlap andactual16support for this fixed candidate.",
      "limits": [
        "128px nucleus/coating detail remains weak",
        "Broad protected source arrangement remains somewhat row-like",
        "Existing inherited inter-grain overlap remains permitted by unchanged scope",
        "No total overlapvolume/maxdepth/worldhost/GPU/nav/LOD claim"
      ]
    },
    "public_semantics": {
      "id": "oncoid-bed",
      "name": {
        "en": "Oncoid bed form study",
        "zh": "核形石层"
      },
      "description": {
        "en": "Generic pedagogical oncoid-bed source-art correction, not a measured Hydra bed or unique locality. Two conspicuous teaching discs now have whole shells and one smaller off-center fracture retains readable coatings; a thin irregular sediment edge reduces the display-podium appearance. All sixteen grains remain, with no added grain overlap in the accepted static arrangement. Residual row-like spacing and weak 128 px fine detail are limitations; actual host/world integration is not accepted. No specific organism or unique growth mechanism is asserted.",
        "zh": "通用鲕粒状核形石床教学源美术修正版，不是Hydra或唯一地点的实测重建。两个醒目展示剖盘改为完整外壳，另一个较小偏心断口保留可读包壳；薄而不规则的沉积物边缘弱化展台读感。保留16粒，已验收静态排列没有新增颗粒重叠。残留行列式间距及128像素细节较弱仍是限制，未验收真实宿主/世界整合；不指认特定生物或唯一生长机制。"
      },
      "dimensions": [
        0.2448064088821411,
        0.05260603874921799,
        0.18000000715255737
      ],
      "units": "meters",
      "triangles": 6110,
      "source_model_identity": {
        "stable_model_id": "oncoid-bed",
        "original_catalog_id": "oncoid-bed",
        "original_catalog_glb_sha256": "117b18e476249c85b4e45ebbdbdd51c1dddf392b5aef8ffe967c39742723e2fa",
        "representation_configuration": "candidate",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": false,
    "source_limits": "PASS_SCOPED_SOURCE_ART_CORRECTION02_NO_ADDED_NODULE_OVERLAP",
    "all_originals_preserved": true
  },
  {
    "entry_id": "parabolic-dune-terrain-only",
    "stable_model_id": "parabolic-dune",
    "configuration": "terrain-only",
    "operation": "same_model_representation_entry",
    "original_documents": {
      "original_review": {
        "sha256": "23d6d6272f6df3d47191630850d397ebe9a351146430cfe041010212b22a3bef",
        "bytes": 8274
      },
      "original_qa_event": {
        "sha256": "467110219b0db5b0d6d967589369395f8a79fb5ee29160ef15780f9aeab8e2bb",
        "bytes": 4024
      },
      "original_maker_evidence": {
        "sha256": "d87c46bdc2ecd3b0c3169bfabf7129622d1ad7028ba6ece1beb0fd9229f94419",
        "bytes": 5362
      }
    },
    "original_report_pointer": "/report_sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/verdict",
      "value": "PASS_TERRAIN_ONLY_SYMBOL_REMOVAL_EXACT_TERRAIN"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/candidate_glb_sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/candidate_blend_sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/parabolic-dune-terrain-only/model.glb",
        "sha256": "a055f21ad8170489fc9651be985286b9aa13664abc3ce5f75243b61ab1d24936",
        "bytes": 250132
      },
      "blend": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/parabolic-dune-terrain-only/source.blend",
        "sha256": "d14fb128b2f8980996a31389ab81e121088640eb24a6aad8aed6abe35a257a93",
        "bytes": 651068
      }
    },
    "maker": {
      "id": "resume_model_rolling_coordination/make_old_corrective_batch04",
      "task_id": "resume_model_rolling_coordination/make_old_corrective_batch04"
    },
    "reviewer": {
      "id": "resume_model_rolling_coordination/review_old_corrective_batch04_resume",
      "task_id": "resume_model_rolling_coordination/review_old_corrective_batch04_resume"
    },
    "maker_pointer": {
      "document": "original_maker_evidence",
      "pointer": "/worker"
    },
    "maker_link": {
      "kind": "DIRECT_QA_EVENT_HANDOFF_HASH",
      "pointer": "/maker_handoff_sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/worker"
    },
    "identity_supplement": null,
    "original_scoped_statements": {
      "qualification_scope": "Approved separately supplied terrain-only variant: remove36 teaching symbols, retained terrain exact; not entire original123"
    },
    "public_semantics": {
      "id": "parabolic-dune-terrain-only",
      "name": {
        "en": "Parabolic dune form study — terrain-only variant",
        "zh": "抛物线沙丘 — 纯地形变体"
      },
      "description": {
        "en": "Separately supplied terrain-only variant of the existing parabolic-dune model. The original teaching/near representation is retained. Bounded static-source acceptance only; no automatic runtime LOD, host/world, GPU, or user visual approval is inferred. Terrain geometry is retained exactly; the 36 teaching symbols are removed, not replaced by actual vegetation. Rectangular boundary and host integration are unchanged.",
        "zh": "既有 parabolic-dune 模型单独提供的纯地形变体，保留原教学/近景表示；不是新物种。仅限原已验收静态源范围，不推断自动LOD、宿主/世界、GPU或用户视觉认可。"
      },
      "dimensions": [
        30.0,
        7.355748176574707,
        46.0
      ],
      "units": "meters",
      "triangles": 3410,
      "source_model_identity": {
        "stable_model_id": "parabolic-dune",
        "original_catalog_id": "parabolic-dune",
        "original_catalog_glb_sha256": "203a4940714165708aed83799fa132eae02c633d7581806fef47f4540ff4bcf9",
        "representation_configuration": "terrain-only",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": true,
    "source_limits": "PASS_TERRAIN_ONLY_SYMBOL_REMOVAL_EXACT_TERRAIN",
    "all_originals_preserved": true
  },
  {
    "entry_id": "serac",
    "stable_model_id": "serac",
    "configuration": "local02",
    "operation": "same_id_successor",
    "original_documents": {
      "original_review": {
        "sha256": "cecb942b080668ed1387543dac9d78e54044aba83c5ce2f9b9f3918a2f69db70",
        "bytes": 6038
      },
      "original_qa_event": {
        "sha256": "30b08f788e910a91aa9450f505062a50e945fc2df6dd63988af74b6e1f3c0b79",
        "bytes": 2297
      },
      "original_maker_evidence": {
        "sha256": "7edc13bf1939e8af8c6eda413e8495f696f1b88d75a68e055bc3bcb1f47485a9",
        "bytes": 1339
      }
    },
    "original_report_pointer": "/report/sha256",
    "original_decision": {
      "document": "original_review",
      "pointer": "/verdict",
      "value": "PASS"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/candidate_glb/sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/native/sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/serac/model.glb",
        "sha256": "262f633da317773c7724fb6a56a32b2553827f97f9066443fd716cc449762342",
        "bytes": 504688
      },
      "blend": {
        "path": "assets/successors/old-corrective-ten-20261027-r001/serac/source.blend",
        "sha256": "0622757b38263ca6614c1b896c53ce425f4c1bc9fb22c4443f9548b69a0a74ca",
        "bytes": 837012
      }
    },
    "maker": {
      "id": "start_serac_fixed_chain01/maker_serac_junction01",
      "task_id": "start_serac_fixed_chain01/maker_serac_junction01"
    },
    "reviewer": {
      "id": "start_serac_fixed_chain01/maker_serac_junction01/qa_serac_junction01",
      "task_id": "start_serac_fixed_chain01/maker_serac_junction01/qa_serac_junction01"
    },
    "maker_pointer": {
      "document": "original_maker_evidence",
      "pointer": "/task"
    },
    "maker_link": {
      "kind": "EXACT_COMMON_CANDIDATE_SEAL_AND_IDENTITY",
      "pointer": "/candidate_seal/sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/task"
    },
    "identity_supplement": null,
    "original_scoped_statements": {
      "limits": [
        "PASS binds only this exact fixed candidate, not any later revision.",
        "No automatic qualification-count increase, release, GitHub upload, merge, publication or deployment.",
        "No hardware GPU, target scene, terrain seams, collision, navigation, LOD or production world-host acceptance claimed.",
        "No retry, new Research/Maker dispatch, or budget renewal."
      ],
      "summary": "独立技术及固定视觉验收通过。局部 NE/SW 交汇错位在 512/256 均清晰可见，值得保留；塔体、低槽陡壁连续性与源拓扑/材质/场景保持。仅此 sealed candidate 的合同内 PASS，不是发布或 world-host/GPU/物理批准。"
    },
    "public_semantics": {
      "id": "serac",
      "name": {
        "en": "Serac form study",
        "zh": "冰塔"
      },
      "description": {
        "en": "Generic glacier-serac source-art correction limited to the fixed northeast and southwest channel junctions. The bounded local changes weaken grid-like junction readings while preserving the remaining source geometry and nominal 30 × 30 m footprint. This is not a full-field naturalization, named glacier, age or measured hazard/ice-dynamics simulation. Host integration, collision and physical GPU performance remain separate unverified concerns.",
        "zh": "通用冰塔源美术修正版，仅修改固定东北和西南沟道交汇局部，以弱化交点网格读感，其余源几何及名义30×30米占地保留。不是整片地形自然化、特定冰川、年代或实测危险性/冰动力模拟；宿主整合、碰撞与物理GPU性能仍待各自验证。"
      },
      "dimensions": [
        30.0,
        18.040258407592773,
        30.0
      ],
      "units": "meters",
      "triangles": 6942,
      "source_model_identity": {
        "stable_model_id": "serac",
        "original_catalog_id": "serac",
        "original_catalog_glb_sha256": "ef5e2e8bfce46ba5bac00557573dacfcbe13384f1ddde27bf743c8af93be2ee5",
        "representation_configuration": "local02",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": false,
    "source_limits": "Fixed local anti-grid standalone asset only; no user visual acceptance, GPU, world host, integration or deployment claim",
    "all_originals_preserved": true
  },
  {
    "entry_id": "stromatolite-mound-full-exterior",
    "stable_model_id": "stromatolite-mound",
    "configuration": "full-exterior",
    "operation": "same_model_representation_entry",
    "original_documents": {
      "original_review": {
        "sha256": "e10ee93e5881ea30e0b7a0978fd142202c542334b7489ef0e6ae6b209b15c9bc",
        "bytes": 4922
      },
      "original_qa_event": {
        "sha256": "124f6db2db804012ed65e45dcc6a53ee70d2587e0c5b169e2d657155312045ee",
        "bytes": 10807
      },
      "original_maker_evidence": {
        "sha256": "ae517ed4d002d3df917ff181f88a70a654e443d85b6c55de1157ed274c26d2ea",
        "bytes": 18635
      }
    },
    "original_report_pointer": "/report_sha256",
    "original_decision": {
      "document": "original_qa_event",
      "pointer": "/verdict",
      "value": "PASS_SCOPED_FULL_EXTERIOR_SOURCE_ART"
    },
    "subject_pointers": {
      "glb": {
        "document": "original_qa_event",
        "pointer": "/candidate_glb_sha256"
      },
      "blend": {
        "document": "original_qa_event",
        "pointer": "/candidate_blend_sha256"
      }
    },
    "subject": {
      "glb": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/stromatolite-mound-full-exterior/model.glb",
        "sha256": "c9fd3c70b4888c4be21c9334769913471969ebc704b77c6ee00750194fde3ea2",
        "bytes": 655412
      },
      "blend": {
        "path": "assets/additions/old-corrective-ten-20261027-r001/stromatolite-mound-full-exterior/source.blend",
        "sha256": "d50d7ca280087765e5bea8a030414c87247f223f5e94b8255fa98892c2fa657b",
        "bytes": 922076
      }
    },
    "maker": {
      "id": "resume_model_rolling_coordination/make_old_corrective_batch05",
      "task_id": "resume_model_rolling_coordination/make_old_corrective_batch05"
    },
    "reviewer": {
      "id": "resume_model_rolling_coordination/review_old_corrective_batch05",
      "task_id": "resume_model_rolling_coordination/review_old_corrective_batch05"
    },
    "maker_pointer": {
      "document": "original_maker_evidence",
      "pointer": "/worker"
    },
    "maker_link": {
      "kind": "DIRECT_QA_EVENT_HANDOFF_HASH",
      "pointer": "/maker_handoff_sha256"
    },
    "reviewer_pointer": {
      "document": "original_qa_event",
      "pointer": "/worker"
    },
    "identity_supplement": null,
    "original_scoped_statements": {
      "scope": "Exact root-approved full-exterior source-art supply subgoal only"
    },
    "public_semantics": {
      "id": "stromatolite-mound-full-exterior",
      "name": {
        "en": "Stromatolite mound — full exterior variant",
        "zh": "叠层石丘 — 完整外壳变体"
      },
      "description": {
        "en": "Separately supplied full exterior variant of the existing stromatolite-mound model. The original teaching/near representation is retained. Bounded static-source acceptance only; no automatic runtime LOD, host/world, GPU, or user visual approval is inferred. Full exterior source-art representation; internal teaching layers are not exposed. It is not a measured fossil.",
        "zh": "既有 stromatolite-mound 模型单独提供的完整外壳变体，保留原教学/近景表示；不是新物种。仅限原已验收静态源范围，不推断自动LOD、宿主/世界、GPU或用户视觉认可。"
      },
      "dimensions": [
        0.6503495872020721,
        0.16115990281105042,
        0.49775637686252594
      ],
      "units": "meters",
      "triangles": 11520,
      "source_model_identity": {
        "stable_model_id": "stromatolite-mound",
        "original_catalog_id": "stromatolite-mound",
        "original_catalog_glb_sha256": "90d7583a58345dd9e673c815a4d53b2df18be70bc8a05c1c9c8a74165ff06a2b",
        "representation_configuration": "full-exterior",
        "is_new_scientific_subject": false
      }
    },
    "original_teaching_near_preserved": true,
    "source_limits": "PASS_SCOPED_FULL_EXTERIOR_SOURCE_ART",
    "all_originals_preserved": true
  }
]);
