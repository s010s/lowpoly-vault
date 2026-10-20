/** Exact independently reviewed land/air pins; bounded website publication only. */
export const CONCEPT_LANDAIR_RELEASE = {
  "version": 1,
  "scope": "concept-landair-20261019",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "base_descriptor": {
    "path": "assets/releases/concept-quartets-20261019.json",
    "sha256": "df4e8571463d5d8be98b53d46fd1b8492b3d43a6798caf2069e2a084f1130423"
  },
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  },
  "source_bundle": {
    "path": "qa/landair-release-20261019/source-bundle.json",
    "sha256": "1687f12839da22a81a5b05fb9e7140949fbd4836f92e0f8e423de9ee0653e740"
  },
  "integration_audit": {
    "path": "qa/landair-release-20261019/integration-audit/source-integrity.json",
    "sha256": "efc945e448f73a64d35e6dfd77e6207d8ba5e8a2d8779d3bc02f50e2be82cbef"
  },
  "excluded_ids": [
    "ctenoimbricata"
  ],
  "additions": [
    {
      "id": "sapeornis",
      "group": "land-air",
      "revision": "r001",
      "source_commit": "e874e99d20b3b98c73cddb8496bcd7e89be4e28c",
      "review_commit": "3d024e53c36863d1887abd726998fa0f0d7b3831",
      "delivery_review_commit": "b0426b7e3a696b30fea4de9e8b46c3772bab3f23",
      "original_review_freeze": "68483aa3b8eed2d86f9e59a930128d99579b0838",
      "review": {
        "path": "qa/independent/small-land-air-quartet-20261019/report.json",
        "sha256": "3551d1d471069218b78fc124b32df0df06e838c36f1cbe2a29e6be0a46ccea14"
      },
      "delivery_review": {
        "path": "qa/independent/land-air-delivery-records-20261019/report.json",
        "sha256": "f93e5a01768aa5f5fc7e03390383db2c825e9fdbb7b95e92a7575676bd9c3f1c"
      },
      "metadata": {
        "path": "assets/additions/sapeornis/concept-landair-20261019/release-metadata.json",
        "sha256": "7db3985ba4f28266a2931814042e531a336a4dcb3e718a1b568958e16647e01f"
      },
      "source_metadata": {
        "path": "production/concept-small-land-air-20261019/sapeornis/r001/output/sapeornis/metadata.json",
        "sha256": "50d58e2a7c7c2a6ff0c04525fe9827176134fd98e26fda22d69aed33bb55662d"
      },
      "candidate": {
        "path": "production/concept-small-land-air-20261019/sapeornis/r001/candidate.json",
        "sha256": "38fb0b38d4b2ef9f22d68c670e305cf9aca7ebe44bf394b7b3cf8c2d46b2c009"
      },
      "candidate_validation": {
        "path": "production/concept-small-land-air-20261019/sapeornis/r001/candidate-validation.json",
        "sha256": "e3250debb3007a913b58e5e8488e2ff30f91611a32a5bee7e4ab915091554a20"
      },
      "artifacts": {
        "glb": {
          "path": "production/concept-small-land-air-20261019/sapeornis/r001/output/sapeornis/sapeornis.glb",
          "sha256": "7b0aef80ee8327ebc06a8372fc63fce63c393a62451820b4bd183ff868b2755b"
        },
        "blend": {
          "path": "production/concept-small-land-air-20261019/sapeornis/r001/output/sapeornis/sapeornis.blend",
          "sha256": "fe598c50f50823d38e50a15aa1ce903dd1264f17d05cda20194c7b3396d7a734"
        },
        "brief": {
          "path": "production/concept-small-land-air-20261019/sapeornis/r001/brief.json",
          "sha256": "a1931a260a3ee691c7a40bb3b359b5f02fd33d7089b8f310643774845c99b558"
        },
        "references": {
          "path": "production/concept-small-land-air-20261019/sapeornis/r001/references.json",
          "sha256": "7870b82f5a84b86e29d1bbebdd38a30896dd860885f5a22f12736e603376dd1f"
        },
        "config": {
          "path": "production/concept-small-land-air-20261019/sapeornis/r001/build-config.json",
          "sha256": "39e714546e7f690136f57afa0f83b40240382a07b65eb799ecfe2e54e8ff1795"
        },
        "generator": {
          "path": "production/concept-small-land-air-20261019/generator-r001.py",
          "sha256": "f7d8e34c1b6e4a531869eba74070f7149a909eafe248d82ddb93f97946946dc7"
        }
      },
      "technical": {
        "source_export": {
          "path": "production/concept-small-land-air-20261019/sapeornis/r001/source-export.report.json",
          "sha256": "b9d29ef26d01e93d33d0440dfcc17bde917592e4c854b8a2c2c4c1c2ae9b904a"
        },
        "rebuild_1": {
          "path": "production/concept-small-land-air-20261019/sapeornis/r001/reproducibility-1.report.json",
          "sha256": "8bd4cce597b2259ff8474bc48b84450722eba626f50d46232ab602ae69da4606"
        },
        "rebuild_2": {
          "path": "production/concept-small-land-air-20261019/sapeornis/r001/reproducibility-2.report.json",
          "sha256": "9a21f756639211a4b0148f7af56e97267f917d9452f8d1462036f644164cc791"
        },
        "khronos": {
          "path": "production/concept-small-land-air-20261019/sapeornis/r001/output/sapeornis/gltf-validator.report.json",
          "sha256": "52e6f5208469c0fd2b061e9cce1abd5d5a42873ca8e1c8793e827c07e4367bdc"
        },
        "fresh_glb": {
          "path": "qa/independent/land-air-delivery-records-20261019/sapeornis-fresh-glb-audit.json",
          "sha256": "9c1a4edcb0c6b5c6c2784d5399e7e8a2ac11c077615c2756f8ec6dbcb43e6070"
        },
        "fresh_blender": {
          "path": "qa/independent/land-air-delivery-records-20261019/sapeornis-fresh-blender-source.json",
          "sha256": "864395fb622aa68dcfe03133f6b9e4d6a2eb6d047ee02068f8fc0b81e69e6a51"
        },
        "fresh_khronos": {
          "path": "qa/independent/land-air-delivery-records-20261019/sapeornis-fresh-khronos.json",
          "sha256": "763490b072281111121bb1b47f7d65ccc1063700307d8346a06793a53eb82485"
        }
      },
      "proof": {
        "path": "production/concept-small-land-air-20261019/sapeornis/r001/proof/render-manifest.json",
        "sha256": "beb935c1710cbf06722d5d27a445348babed3e69902349eb39deac01dfc7ed2d"
      },
      "runtime": {
        "path": "qa/independent/small-land-air-quartet-20261019/runtime/software-webgl-scene.report.json",
        "sha256": "f6fbf69cb4018b51989ceff91793f398f055e8114af80a9911dc33774d1f3185"
      },
      "limits": {
        "asset_id": "sapeornis",
        "revision": "r001",
        "length_m": 0.35,
        "seed": 19,
        "max_triangles": 16000,
        "max_materials": 8,
        "max_primitives": 160,
        "soft_glb_bytes": 1000000,
        "surface_profile": "palette-only",
        "mount_origin": "flight-body center",
        "role": "supporting scene life; typical128px, inspectable512px",
        "normal_visible_copies": 8,
        "stress_visible_copies": 32,
        "runtime_target": "Three.js0.180.0; parent independent parse/GPU/scene QA pending"
      },
      "sha256": {
        "glb": "7b0aef80ee8327ebc06a8372fc63fce63c393a62451820b4bd183ff868b2755b",
        "blend": "fe598c50f50823d38e50a15aa1ce903dd1264f17d05cda20194c7b3396d7a734",
        "preview": "3150996862c56bf8b5b20e4eef0cd5d3027124aba308e88a4bf2b40d916ca62c"
      },
      "capture": {
        "report": {
          "path": "qa/landair-release-20261019/card-capture/render-report.json",
          "sha256": "cd8a1d8159d89d2a0434033a3710a35c191e5f606851803266ba786a5bafcb68"
        },
        "index": {
          "path": "qa/landair-release-20261019/card-capture/assets/turntables/index.json",
          "sha256": "d5feefb37ec2d6e046b4807cd9f642fa56e032d6b9a78ccf148c17e8cba7dd8e"
        },
        "reference": {
          "path": "qa/landair-release-20261019/card-capture/references/sapeornis.png",
          "sha256": "3150996862c56bf8b5b20e4eef0cd5d3027124aba308e88a4bf2b40d916ca62c"
        }
      }
    },
    {
      "id": "longirostravis",
      "group": "land-air",
      "revision": "r001",
      "source_commit": "e874e99d20b3b98c73cddb8496bcd7e89be4e28c",
      "review_commit": "3d024e53c36863d1887abd726998fa0f0d7b3831",
      "delivery_review_commit": "b0426b7e3a696b30fea4de9e8b46c3772bab3f23",
      "original_review_freeze": "68483aa3b8eed2d86f9e59a930128d99579b0838",
      "review": {
        "path": "qa/independent/small-land-air-quartet-20261019/report.json",
        "sha256": "3551d1d471069218b78fc124b32df0df06e838c36f1cbe2a29e6be0a46ccea14"
      },
      "delivery_review": {
        "path": "qa/independent/land-air-delivery-records-20261019/report.json",
        "sha256": "f93e5a01768aa5f5fc7e03390383db2c825e9fdbb7b95e92a7575676bd9c3f1c"
      },
      "metadata": {
        "path": "assets/additions/longirostravis/concept-landair-20261019/release-metadata.json",
        "sha256": "228f9a74f992b7a1a8f16f3644c540f48acc7a7510d930113904deeb64b03747"
      },
      "source_metadata": {
        "path": "production/concept-small-land-air-20261019/longirostravis/r001/output/longirostravis/metadata.json",
        "sha256": "c7026d6f169f95f8273bb910096580b781b60eb732b453a1501e238ce0a18d89"
      },
      "candidate": {
        "path": "production/concept-small-land-air-20261019/longirostravis/r001/candidate.json",
        "sha256": "660678f4d4a160dcfcd7d97dfac342666f1b5115b32c7a5e616643e85280148c"
      },
      "candidate_validation": {
        "path": "production/concept-small-land-air-20261019/longirostravis/r001/candidate-validation.json",
        "sha256": "4270309f864cec36b2a889ecd6f4af1f7ae023dce7727f408638d80ecbb1b978"
      },
      "artifacts": {
        "glb": {
          "path": "production/concept-small-land-air-20261019/longirostravis/r001/output/longirostravis/longirostravis.glb",
          "sha256": "10668416201cf7ec57e48285019fcd0738e6bb69665fd8fb519559aabaa6bd83"
        },
        "blend": {
          "path": "production/concept-small-land-air-20261019/longirostravis/r001/output/longirostravis/longirostravis.blend",
          "sha256": "b9ccf3e817136a22c848afcb4a6f48b7791c31acb32ef86b0c7eb841d140ebe3"
        },
        "brief": {
          "path": "production/concept-small-land-air-20261019/longirostravis/r001/brief.json",
          "sha256": "e5db584733786b710b4b552c6d7754ed4ea9c97915f2aeaca8676f7561d5b139"
        },
        "references": {
          "path": "production/concept-small-land-air-20261019/longirostravis/r001/references.json",
          "sha256": "9c9ffcb2267b0698bf095ccf075f9998cd77fd46c271213d00e51493ae236a36"
        },
        "config": {
          "path": "production/concept-small-land-air-20261019/longirostravis/r001/build-config.json",
          "sha256": "d3d714afb2750ca575623062ab30a891ca2ced7faa615f42c7be9071b6e5e69e"
        },
        "generator": {
          "path": "production/concept-small-land-air-20261019/generator.py",
          "sha256": "bf434db894d09ece49928edfcbc8822d9c08a18f2b037fbc6a11884a869399a6"
        }
      },
      "technical": {
        "source_export": {
          "path": "production/concept-small-land-air-20261019/longirostravis/r001/source-export.report.json",
          "sha256": "ac9d473760efe3cb16ebbf99636f67a093582bb9e1a7825c05f826c0e4e7a964"
        },
        "rebuild_1": {
          "path": "production/concept-small-land-air-20261019/longirostravis/r001/reproducibility-1.report.json",
          "sha256": "3a7c4a6a6e485325c00df75ee1bc3db7c6da5ad53c80f7c0dd249076e02451ce"
        },
        "rebuild_2": {
          "path": "production/concept-small-land-air-20261019/longirostravis/r001/reproducibility-2.report.json",
          "sha256": "9a7202c8da051a230d3df236e9b6f8287dd23834881622f6dd08b1453ffed9c0"
        },
        "khronos": {
          "path": "production/concept-small-land-air-20261019/longirostravis/r001/output/longirostravis/gltf-validator.report.json",
          "sha256": "436bc7bf5a7f5d7fc7cdc38de3fd5e0970aa76bc993a1c0a3c496a0b22a1059b"
        },
        "fresh_glb": {
          "path": "qa/independent/land-air-delivery-records-20261019/longirostravis-fresh-glb-audit.json",
          "sha256": "08de24f42d3dae9a345da6e9a721ae4679c44db3d2cc57a5d0eacebaf2c28538"
        },
        "fresh_blender": {
          "path": "qa/independent/land-air-delivery-records-20261019/longirostravis-fresh-blender-source.json",
          "sha256": "41f433c01ae916274807b3c6c8912c3b44990c6084a86d182923cbcef4408364"
        },
        "fresh_khronos": {
          "path": "qa/independent/land-air-delivery-records-20261019/longirostravis-fresh-khronos.json",
          "sha256": "f3c7f94014458dba110a9a70b862ef39678ea5431575bcd7828126247f9d1f41"
        }
      },
      "proof": {
        "path": "production/concept-small-land-air-20261019/longirostravis/r001/proof/render-manifest.json",
        "sha256": "1a3c1868cd1530caed15d347094e6cf83195451d6b30d0cf848fb888b1c6e5a2"
      },
      "runtime": {
        "path": "qa/independent/small-land-air-quartet-20261019/runtime/software-webgl-scene.report.json",
        "sha256": "f6fbf69cb4018b51989ceff91793f398f055e8114af80a9911dc33774d1f3185"
      },
      "limits": {
        "asset_id": "longirostravis",
        "revision": "r001",
        "length_m": 0.18,
        "seed": 19,
        "max_triangles": 16000,
        "max_materials": 8,
        "max_primitives": 160,
        "soft_glb_bytes": 1000000,
        "surface_profile": "palette-only",
        "mount_origin": "floor contact center",
        "role": "supporting scene life; typical128px, inspectable512px",
        "normal_visible_copies": 8,
        "stress_visible_copies": 32,
        "runtime_target": "Three.js0.180.0; parent independent parse/GPU/scene QA pending"
      },
      "sha256": {
        "glb": "10668416201cf7ec57e48285019fcd0738e6bb69665fd8fb519559aabaa6bd83",
        "blend": "b9ccf3e817136a22c848afcb4a6f48b7791c31acb32ef86b0c7eb841d140ebe3",
        "preview": "1e6c4ee2f6b0a5e4ca1736f6daa3443ca044ea9b3f19d8eae9aad77cf623b742"
      },
      "capture": {
        "report": {
          "path": "qa/landair-release-20261019/card-capture/render-report.json",
          "sha256": "cd8a1d8159d89d2a0434033a3710a35c191e5f606851803266ba786a5bafcb68"
        },
        "index": {
          "path": "qa/landair-release-20261019/card-capture/assets/turntables/index.json",
          "sha256": "d5feefb37ec2d6e046b4807cd9f642fa56e032d6b9a78ccf148c17e8cba7dd8e"
        },
        "reference": {
          "path": "qa/landair-release-20261019/card-capture/references/longirostravis.png",
          "sha256": "1e6c4ee2f6b0a5e4ca1736f6daa3443ca044ea9b3f19d8eae9aad77cf623b742"
        }
      }
    },
    {
      "id": "dunbaria",
      "group": "land-air",
      "revision": "r001",
      "source_commit": "e874e99d20b3b98c73cddb8496bcd7e89be4e28c",
      "review_commit": "3d024e53c36863d1887abd726998fa0f0d7b3831",
      "delivery_review_commit": "b0426b7e3a696b30fea4de9e8b46c3772bab3f23",
      "original_review_freeze": "68483aa3b8eed2d86f9e59a930128d99579b0838",
      "review": {
        "path": "qa/independent/small-land-air-quartet-20261019/report.json",
        "sha256": "3551d1d471069218b78fc124b32df0df06e838c36f1cbe2a29e6be0a46ccea14"
      },
      "delivery_review": {
        "path": "qa/independent/land-air-delivery-records-20261019/report.json",
        "sha256": "f93e5a01768aa5f5fc7e03390383db2c825e9fdbb7b95e92a7575676bd9c3f1c"
      },
      "metadata": {
        "path": "assets/additions/dunbaria/concept-landair-20261019/release-metadata.json",
        "sha256": "b4f2d9a0e79f342c812c93773dbe11f4c225e3ce394d60165c10de34722d9ef0"
      },
      "source_metadata": {
        "path": "production/concept-small-land-air-20261019/dunbaria/r001/output/dunbaria/metadata.json",
        "sha256": "3058c26b470e87accf70f96bab5cd85835c1da64d887bb30dbc6c39981b027e4"
      },
      "candidate": {
        "path": "production/concept-small-land-air-20261019/dunbaria/r001/candidate.json",
        "sha256": "f319c784d3ac8398877696092791fcb41fb27020549c6cf251ee366a38646952"
      },
      "candidate_validation": {
        "path": "production/concept-small-land-air-20261019/dunbaria/r001/candidate-validation.json",
        "sha256": "ebce0a6cc68c6bd0c38468d4602363774e0ad9cfc73424fbed4bb363eb5c5a9c"
      },
      "artifacts": {
        "glb": {
          "path": "production/concept-small-land-air-20261019/dunbaria/r001/output/dunbaria/dunbaria.glb",
          "sha256": "2f584412b3318fa3969e6b008271df107f73fe9f00c8f304c04bfa47e134311e"
        },
        "blend": {
          "path": "production/concept-small-land-air-20261019/dunbaria/r001/output/dunbaria/dunbaria.blend",
          "sha256": "27a429059cbacb2f93563cf7a132a09ebe04eb6b7961e8234c85528d85ea4730"
        },
        "brief": {
          "path": "production/concept-small-land-air-20261019/dunbaria/r001/brief.json",
          "sha256": "a354aeaa8549eecf09fbe858430aca47eade271f1ecbbe1e11d11018b8f7c02b"
        },
        "references": {
          "path": "production/concept-small-land-air-20261019/dunbaria/r001/references.json",
          "sha256": "8e2bd938aa87e9d07e16c744ba85f612a8721fd897b4ddf7b776c76b7142f998"
        },
        "config": {
          "path": "production/concept-small-land-air-20261019/dunbaria/r001/build-config.json",
          "sha256": "9266fa202963600ee0efa521fb98022fb19339d31e33e49d8108c5398976bd0c"
        },
        "generator": {
          "path": "production/concept-small-land-air-20261019/generator.py",
          "sha256": "bf434db894d09ece49928edfcbc8822d9c08a18f2b037fbc6a11884a869399a6"
        }
      },
      "technical": {
        "source_export": {
          "path": "production/concept-small-land-air-20261019/dunbaria/r001/source-export.report.json",
          "sha256": "0bedeff8c8281765b019fa5544a7276875563d9765ac74b524b3473f6416bd26"
        },
        "rebuild_1": {
          "path": "production/concept-small-land-air-20261019/dunbaria/r001/reproducibility-1.report.json",
          "sha256": "d9dc9980b9774a9a2b5bd6323a2f7e7395a6cf047dba2ee706f46c5e0023b21d"
        },
        "rebuild_2": {
          "path": "production/concept-small-land-air-20261019/dunbaria/r001/reproducibility-2.report.json",
          "sha256": "372bca8b576cddc69e4b5ca92eef51c7ffa346a33bc97ec0cb89d0c213b77c14"
        },
        "khronos": {
          "path": "production/concept-small-land-air-20261019/dunbaria/r001/output/dunbaria/gltf-validator.report.json",
          "sha256": "0b2548d39f226edeacd3a243635ce39ef7aaf285aa6087723392898da4d6bd61"
        },
        "fresh_glb": {
          "path": "qa/independent/land-air-delivery-records-20261019/dunbaria-fresh-glb-audit.json",
          "sha256": "70c85b5a90d28590c53876185719dd39985f645150c075c8a21a6291bccdb12e"
        },
        "fresh_blender": {
          "path": "qa/independent/land-air-delivery-records-20261019/dunbaria-fresh-blender-source.json",
          "sha256": "908c240c9b45a5f0ff0dbca04bf11d181f5b2eadeb694bf7d0e0ebaa19d23ddd"
        },
        "fresh_khronos": {
          "path": "qa/independent/land-air-delivery-records-20261019/dunbaria-fresh-khronos.json",
          "sha256": "ccb4ba19fc8e82eb371b0ad4d4ba9e4411f716a0446785db08f74629380264fa"
        }
      },
      "proof": {
        "path": "production/concept-small-land-air-20261019/dunbaria/r001/proof/render-manifest.json",
        "sha256": "0b74743828199915046ee05b19ce84b3e73012131b20589645bfd50f867a0955"
      },
      "runtime": {
        "path": "qa/independent/small-land-air-quartet-20261019/runtime/software-webgl-scene.report.json",
        "sha256": "f6fbf69cb4018b51989ceff91793f398f055e8114af80a9911dc33774d1f3185"
      },
      "limits": {
        "asset_id": "dunbaria",
        "revision": "r001",
        "length_m": 0.035,
        "seed": 19,
        "max_triangles": 16000,
        "max_materials": 8,
        "max_primitives": 160,
        "soft_glb_bytes": 1000000,
        "surface_profile": "palette-only",
        "mount_origin": "floor contact center",
        "role": "supporting scene life; typical128px, inspectable512px",
        "normal_visible_copies": 8,
        "stress_visible_copies": 32,
        "runtime_target": "Three.js0.180.0; parent independent parse/GPU/scene QA pending"
      },
      "sha256": {
        "glb": "2f584412b3318fa3969e6b008271df107f73fe9f00c8f304c04bfa47e134311e",
        "blend": "27a429059cbacb2f93563cf7a132a09ebe04eb6b7961e8234c85528d85ea4730",
        "preview": "84a475cd3a28f5c19b3b829ac0246d8dbc66d679c628725b83c90ad8b2a96a61"
      },
      "capture": {
        "report": {
          "path": "qa/landair-release-20261019/card-capture/render-report.json",
          "sha256": "cd8a1d8159d89d2a0434033a3710a35c191e5f606851803266ba786a5bafcb68"
        },
        "index": {
          "path": "qa/landair-release-20261019/card-capture/assets/turntables/index.json",
          "sha256": "d5feefb37ec2d6e046b4807cd9f642fa56e032d6b9a78ccf148c17e8cba7dd8e"
        },
        "reference": {
          "path": "qa/landair-release-20261019/card-capture/references/dunbaria.png",
          "sha256": "84a475cd3a28f5c19b3b829ac0246d8dbc66d679c628725b83c90ad8b2a96a61"
        }
      }
    },
    {
      "id": "chimerarachne",
      "group": "land-air",
      "revision": "r001",
      "source_commit": "e874e99d20b3b98c73cddb8496bcd7e89be4e28c",
      "review_commit": "3d024e53c36863d1887abd726998fa0f0d7b3831",
      "delivery_review_commit": "b0426b7e3a696b30fea4de9e8b46c3772bab3f23",
      "original_review_freeze": "68483aa3b8eed2d86f9e59a930128d99579b0838",
      "review": {
        "path": "qa/independent/small-land-air-quartet-20261019/report.json",
        "sha256": "3551d1d471069218b78fc124b32df0df06e838c36f1cbe2a29e6be0a46ccea14"
      },
      "delivery_review": {
        "path": "qa/independent/land-air-delivery-records-20261019/report.json",
        "sha256": "f93e5a01768aa5f5fc7e03390383db2c825e9fdbb7b95e92a7575676bd9c3f1c"
      },
      "metadata": {
        "path": "assets/additions/chimerarachne/concept-landair-20261019/release-metadata.json",
        "sha256": "2186c17990619abe7f1052e94f768db5fbd7a45f3fadc0ca612dc34052fe74a2"
      },
      "source_metadata": {
        "path": "production/concept-small-land-air-20261019/chimerarachne/r001/output/chimerarachne/metadata.json",
        "sha256": "48925de79977c53889cf5ac04ed49e30bf07f44d3c3dfd5fbac8a7bfcd167528"
      },
      "candidate": {
        "path": "production/concept-small-land-air-20261019/chimerarachne/r001/candidate.json",
        "sha256": "9f1425803ab60620628f2f079be5de5f872e9af276b70ea4fc047870eb3b955e"
      },
      "candidate_validation": {
        "path": "production/concept-small-land-air-20261019/chimerarachne/r001/candidate-validation.json",
        "sha256": "8719106d5797102704bd0027b81664b957b5ae5a1e19a090e978f53b9f7b3dc3"
      },
      "artifacts": {
        "glb": {
          "path": "production/concept-small-land-air-20261019/chimerarachne/r001/output/chimerarachne/chimerarachne.glb",
          "sha256": "848328130f8874bc6c81b0636d8bfc78f76d04b46cfa0786fe7d978f28e3ad6c"
        },
        "blend": {
          "path": "production/concept-small-land-air-20261019/chimerarachne/r001/output/chimerarachne/chimerarachne.blend",
          "sha256": "02db9598d09e548f42e72cd443a87b8028dd6d76dd40a4676ef79b4070609259"
        },
        "brief": {
          "path": "production/concept-small-land-air-20261019/chimerarachne/r001/brief.json",
          "sha256": "8b453e1c3dd836b070c78c61a593b2751f21c97a848a201dc8036551ab967766"
        },
        "references": {
          "path": "production/concept-small-land-air-20261019/chimerarachne/r001/references.json",
          "sha256": "c93746e53d01952b3f26295e1e4224131ea66ce30781dbac5ad6f6301bd924f6"
        },
        "config": {
          "path": "production/concept-small-land-air-20261019/chimerarachne/r001/build-config.json",
          "sha256": "468d9933101db5867d24d46fd46c03104e26e07625d48d68e9da7676189b9da4"
        },
        "generator": {
          "path": "production/concept-small-land-air-20261019/generator.py",
          "sha256": "bf434db894d09ece49928edfcbc8822d9c08a18f2b037fbc6a11884a869399a6"
        }
      },
      "technical": {
        "source_export": {
          "path": "production/concept-small-land-air-20261019/chimerarachne/r001/source-export.report.json",
          "sha256": "b01fa016e2e59200d6ed12eb34431408d8100d22e6cf4771df15abc42d939097"
        },
        "rebuild_1": {
          "path": "production/concept-small-land-air-20261019/chimerarachne/r001/reproducibility-1.report.json",
          "sha256": "b792a79efda52a523249d5927c1647261aedaa9f2bb7f11846456d92f653d160"
        },
        "rebuild_2": {
          "path": "production/concept-small-land-air-20261019/chimerarachne/r001/reproducibility-2.report.json",
          "sha256": "cebf8349cbc5cc4d648b4f8a3605a952664cb81c678cb224c1eb775e947fa149"
        },
        "khronos": {
          "path": "production/concept-small-land-air-20261019/chimerarachne/r001/output/chimerarachne/gltf-validator.report.json",
          "sha256": "c1fe572fc0759eb64cdd4767355e5ab762a00fa0e31adce4d49da7c92ae7305d"
        },
        "fresh_glb": {
          "path": "qa/independent/land-air-delivery-records-20261019/chimerarachne-fresh-glb-audit.json",
          "sha256": "955030be0f868099ee56c887160b323ba3b182d070bcbbd80d429582ed0a4e69"
        },
        "fresh_blender": {
          "path": "qa/independent/land-air-delivery-records-20261019/chimerarachne-fresh-blender-source.json",
          "sha256": "df27fa05d2fcde560787dc6f85510f5e06da2842ac22b21bf066c9fd4dbe04a2"
        },
        "fresh_khronos": {
          "path": "qa/independent/land-air-delivery-records-20261019/chimerarachne-fresh-khronos.json",
          "sha256": "55c91bde138a66da9ad51ef4b35397e000d51aa5e5dabb87bc2cbc9e4ce17399"
        }
      },
      "proof": {
        "path": "production/concept-small-land-air-20261019/chimerarachne/r001/proof-macro-attempt02/render-manifest.json",
        "sha256": "58d90626e1508659a3461568577d8d92962935867475ee0133418f2b890f4a5f"
      },
      "runtime": {
        "path": "qa/independent/small-land-air-quartet-20261019/runtime/software-webgl-scene.report.json",
        "sha256": "f6fbf69cb4018b51989ceff91793f398f055e8114af80a9911dc33774d1f3185"
      },
      "limits": {
        "asset_id": "chimerarachne",
        "revision": "r001",
        "length_m": 0.003,
        "seed": 19,
        "max_triangles": 16000,
        "max_materials": 8,
        "max_primitives": 160,
        "soft_glb_bytes": 1000000,
        "surface_profile": "palette-only",
        "mount_origin": "floor contact center",
        "role": "supporting scene life; typical128px, inspectable512px",
        "normal_visible_copies": 8,
        "stress_visible_copies": 32,
        "runtime_target": "Three.js0.180.0; parent independent parse/GPU/scene QA pending"
      },
      "sha256": {
        "glb": "848328130f8874bc6c81b0636d8bfc78f76d04b46cfa0786fe7d978f28e3ad6c",
        "blend": "02db9598d09e548f42e72cd443a87b8028dd6d76dd40a4676ef79b4070609259",
        "preview": "507a818c24dfe50f58897d0a94a4484c4ca772a79ec3c5ec30f90d6e194b07e9"
      },
      "capture": {
        "report": {
          "path": "qa/landair-release-20261019/card-capture/render-report.json",
          "sha256": "cd8a1d8159d89d2a0434033a3710a35c191e5f606851803266ba786a5bafcb68"
        },
        "index": {
          "path": "qa/landair-release-20261019/card-capture/assets/turntables/index.json",
          "sha256": "d5feefb37ec2d6e046b4807cd9f642fa56e032d6b9a78ccf148c17e8cba7dd8e"
        },
        "reference": {
          "path": "qa/landair-release-20261019/card-capture/references/chimerarachne.png",
          "sha256": "507a818c24dfe50f58897d0a94a4484c4ca772a79ec3c5ec30f90d6e194b07e9"
        }
      }
    }
  ]
};

/** Exact Batch54 bounded website release; not formal acceptance. */
export const BATCH54_RELEASE = {
  "version": 1,
  "scope": "batch54-20261020",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "provider_generation_timestamp": "unknown",
  "source_commit": "54d5380ec3c63ae3e9ab4f36cb377db65ab16c75",
  "review_commit": "d5b0956916ab21d1ef0fef44a42358b3d9c2db95",
  "base_descriptor": {
    "path": "assets/releases/concept-landair-20261019.json",
    "sha256": "bb8e0aa3846a0cca9b381e675a988b756c652546efb44405fb4b27927895136b"
  },
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  },
  "source_bundle": {
    "path": "qa/batch54-release-20261020/source-bundle.json",
    "sha256": "34ea7c701cd23ff36c6007d6cc813397ebb56a26e34d6a8e119c6e68f4a379e9"
  },
  "review": {
    "path": "qa/batch54-independent-20261020/report-data.json",
    "sha256": "9f5fa2c212810feafeaf23b6d1d7f1d267bda61fad747f5e493abdfb5d98eb7e"
  },
  "dispatch_binding": {
    "path": "qa/batch54-release-20261020/dispatch-binding.json",
    "sha256": "664b6faf71825718f6b70a913d01ac7278fd4aadc0068f30d4b6090339d6e930"
  },
  "capture": {
    "independent_review": {
      "path": "qa/batch54-release-20261020/capture-independent-verification.json",
      "sha256": "7359fd4f8e73eb3f30ff529897073c7e5e8f73095fa890c0cf56e2d252cea537"
    },
    "report": {
      "path": "qa/batch54-release-20261020/capture/render-report.json",
      "sha256": "25a892394b4bde3d14a3b5d2d597ce5bbd55fc253783fba15c15174890b0f2bf"
    },
    "index": {
      "path": "qa/batch54-release-20261020/capture/assets/turntables/index.json",
      "sha256": "874c91b833a5084ab91aee14fef650fafba5de09dd945d1924824051d5afeef9"
    },
    "provenance": {
      "path": "qa/batch54-release-20261020/capture-provenance.json",
      "sha256": "51a0680076af52a853222bc0625bef26408ff61612a01a276c38e9537abd3836"
    }
  },
  "additions": [
    {
      "id": "didymoceras",
      "revision": "r003",
      "source_commit": "54d5380ec3c63ae3e9ab4f36cb377db65ab16c75",
      "review_commit": "d5b0956916ab21d1ef0fef44a42358b3d9c2db95",
      "metadata": {
        "path": "assets/additions/didymoceras/batch54-20261020/release-metadata.json",
        "sha256": "0395e21e1d6c0d0021575794feb800930f0b3de83580d5bd1a0aa19f1e486a2f"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/metadata.json",
        "sha256": "b706254d4c20d690c4817bcb32b1c3fccbba609edab7256a7a1f8ab68ac5d8db"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/candidate.json",
        "sha256": "f98075de91c43bfd072380ae5aa3174bdee0a090072e4a04d9d4175823cbc89d"
      },
      "review": {
        "path": "qa/batch54-independent-20261020/report-data.json",
        "sha256": "9f5fa2c212810feafeaf23b6d1d7f1d267bda61fad747f5e493abdfb5d98eb7e"
      },
      "capture_reference": {
        "path": "qa/batch54-release-20261020/capture/references/didymoceras.png",
        "sha256": "87fc3176a72a9948c16919c75f6f7c6a300af46f264eab4773eddc9e8e85938e"
      }
    },
    {
      "id": "spirematospermum",
      "revision": "r003",
      "source_commit": "54d5380ec3c63ae3e9ab4f36cb377db65ab16c75",
      "review_commit": "d5b0956916ab21d1ef0fef44a42358b3d9c2db95",
      "metadata": {
        "path": "assets/additions/spirematospermum/batch54-20261020/release-metadata.json",
        "sha256": "fb4452f138350973121c8e8fa1a8a3c135063e80e9a3a4a4fad7b8d8fb37ba42"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/metadata.json",
        "sha256": "e636c43ac24e3cbb5f044deb7a158baf8e3f1e83c926314be6c6233fb4f29aac"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/candidate.json",
        "sha256": "4812625e458d703af8f9a6cd23cbc9bd31b45ea79183305710798b3392a49655"
      },
      "review": {
        "path": "qa/batch54-independent-20261020/report-data.json",
        "sha256": "9f5fa2c212810feafeaf23b6d1d7f1d267bda61fad747f5e493abdfb5d98eb7e"
      },
      "capture_reference": {
        "path": "qa/batch54-release-20261020/capture/references/spirematospermum.png",
        "sha256": "a11a1f953a1b634dc99da456aa94da3ccde7557162c42cc6e054cd9a5f8cde01"
      }
    },
    {
      "id": "cave-shield",
      "revision": "r002",
      "source_commit": "54d5380ec3c63ae3e9ab4f36cb377db65ab16c75",
      "review_commit": "d5b0956916ab21d1ef0fef44a42358b3d9c2db95",
      "metadata": {
        "path": "assets/additions/cave-shield/batch54-20261020/release-metadata.json",
        "sha256": "ddb717d76e84b5d343a5c398a0add3e9cc6adf31c48c548967938aee362e78db"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/metadata.json",
        "sha256": "ea23d0e2d56907453e5c94c96dca050ec1f7edd0d35c4d1f630ba195e6cfca7e"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/candidate.json",
        "sha256": "f8327e28883fd1de199f2ba1760fd95e5a5c27b458bc9546c04d4f20742a1793"
      },
      "review": {
        "path": "qa/batch54-independent-20261020/report-data.json",
        "sha256": "9f5fa2c212810feafeaf23b6d1d7f1d267bda61fad747f5e493abdfb5d98eb7e"
      },
      "capture_reference": {
        "path": "qa/batch54-release-20261020/capture/references/cave-shield.png",
        "sha256": "0c8cc0040d81fab701a0713b37405e2cc39a196b299fa27bd2e6e4a635edb66a"
      }
    },
    {
      "id": "psammichnites-ribbon-trace",
      "revision": "r002",
      "source_commit": "54d5380ec3c63ae3e9ab4f36cb377db65ab16c75",
      "review_commit": "d5b0956916ab21d1ef0fef44a42358b3d9c2db95",
      "metadata": {
        "path": "assets/additions/psammichnites-ribbon-trace/batch54-20261020/release-metadata.json",
        "sha256": "fda301376c2b272abb21dd21f54e081c904c16fab9c550740ae3f2057b0b6a89"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/metadata.json",
        "sha256": "a1ca2a0a88d7719eb8c252abfa078db9f89fb35e5dfc48cb5f3a1c677f33d1dd"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/candidate.json",
        "sha256": "f50307bf859549bc6eb20e4fad0d44996892aeea25e2c579ea8e76daa83a02c1"
      },
      "review": {
        "path": "qa/batch54-independent-20261020/report-data.json",
        "sha256": "9f5fa2c212810feafeaf23b6d1d7f1d267bda61fad747f5e493abdfb5d98eb7e"
      },
      "capture_reference": {
        "path": "qa/batch54-release-20261020/capture/references/psammichnites-ribbon-trace.png",
        "sha256": "f534407262a5e13690fb535ae0837c57eae47d758a94f41784f12ee2a9b5c435"
      }
    }
  ],
  "files": [
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/brief-delivery.json",
      "sha256": "9b3bf91ace2b5c1050a09a627708d52f2723a5b756aa1331a01fd9126fe1d47e",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/brief.json",
      "sha256": "2fe565b96d10d5fe23071dab8cc896e6f9caddc0179e6ce5a8199f9e4eed45c9",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/brief.md",
      "sha256": "84d42014dca04fdf278cd77c1f1df0d4dc3a08ff3ca388998fb51c4b0d1cf94b",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/build-config.json",
      "sha256": "15b1d4cd99b1c10ef44d4333689447e52703309953107cba75d203289e97bb03",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/build-qa.json",
      "sha256": "8991773344ca084af84dc574510d7cff7337ef9df1daf01d102132183dbdd85d",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/candidate-check-initial.json",
      "sha256": "76cedf4b8d83eac1451e6f7ad47af4781a490d914b83a4e231216cdf15ed81fb",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/candidate-check.json",
      "sha256": "3fb938bcf31d02a5f4ae82a523532d49f16a284f073cb92e71dcf76984294c02",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/candidate.json",
      "sha256": "f8327e28883fd1de199f2ba1760fd95e5a5c27b458bc9546c04d4f20742a1793",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/cave-shield.blend",
      "sha256": "2a19392c990e37c1f77002e0addfa2f1805ce6ef71997cdac440d1852afcc88c",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/cave-shield.glb",
      "sha256": "4c772ba8705c9921836accd4607f15dae75f34ad9bdf67d8ef9970bbea961028",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/concept-completeness.json",
      "sha256": "27048eb36c9df7f58c7893d6573b852813e2cd34a75f037260f16448a18acf76",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/concept-completeness.stderr.txt",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/concept-evidence.json",
      "sha256": "68b3a0de8c72e368af8b56365d7bb03dbf347c798a31a0b0adecee12c7feca02",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/delivery-freeze.json",
      "sha256": "961e35f008c5585a3d897b607d9aedbe882fb9fd2e815eb73559099662afb528",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/dependency-hashes.json",
      "sha256": "ccae1479c6d9c14260a7904c8fe0f57c87868acf2d7cc426b0dfee4600baf2e3",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/eight-views.png",
      "sha256": "16e3e368a362e0cb0591251c86ff250ff221dc861e481576acb7f67012936ca1",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/evidence/rebuild-1.check.log",
      "sha256": "6c52e53acaef1378222cc6267d67654f14f65f918ed62018fb84e650194d650c",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/evidence/rebuild-1.json",
      "sha256": "6c52e53acaef1378222cc6267d67654f14f65f918ed62018fb84e650194d650c",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/evidence/rebuild-2.check.log",
      "sha256": "840e11d14218eb12db1ff3775bb39544880eb1f766a3c91450dffae34dd6c2b3",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/evidence/rebuild-2.json",
      "sha256": "840e11d14218eb12db1ff3775bb39544880eb1f766a3c91450dffae34dd6c2b3",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/evidence/runtime-parse.json",
      "sha256": "8eb0b73459380195b36ea2f52ec96ab7472f34364fb03cd0534422d3fa41493b",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/evidence/source-export.json",
      "sha256": "7732af0fcfa10d6f906dd6b4d1eb0d5346a3d02d52d17a03f0cd3f8128abdb48",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/evidence/static-glb.json",
      "sha256": "2397c88aa81f0b402a70033b276e77b6b5449d06732e6b41371f973ee6198f57",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/evidence/technical.json",
      "sha256": "f1ec8f1399c2d1ae7896357822813117d1649c6c8e8a032fdd37fe091aaf1cd7",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/generator.py",
      "sha256": "a5ec704a7d7b7711d1fa575edaf4e2a8d2e4c7381583cc7e1f46b59a1e01ab21",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/gltf-validator.report.json",
      "sha256": "43140dc58e17815057bac1f33a518cd934497d3cc971688679bd4155306bb50e",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/maker-review.md",
      "sha256": "699ccb95d4d4e4ea21c78877909c5444a0bb65f60beb65fb084a6956928a53cb",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/metadata.json",
      "sha256": "ea23d0e2d56907453e5c94c96dca050ec1f7edd0d35c4d1f630ba195e6cfca7e",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/metrics.json",
      "sha256": "f636cb8a41954ab46ab0a617e4bd99c3b7a10a4608a8edd98c11343a75c59e4a",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/modeling-freeze.json",
      "sha256": "9d8a59d335a2aeec4f40beec567b47bd0071664240984f88fa9ba67327435cb4",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/preview-hero.png",
      "sha256": "4ebb5b2f738cda0b8d2a5a8e0280178b2f45cbcfc190c6212b1802d8f840fce2",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/profile-contract.json",
      "sha256": "fe4637c585127867601b49d0dbb77bd9847523f8034fb4ab7b96e8b9eb94d152",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/clay.png",
      "sha256": "c3784810559740457e9e65ced91a954c742c53ac650c7058d9ca188e0ae513df",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/front.png",
      "sha256": "5bae12b927cc811266a1af19ea7c116013bad89cf9a63266aaaf4f5cbfc58827",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/hero.png",
      "sha256": "4ebb5b2f738cda0b8d2a5a8e0280178b2f45cbcfc190c6212b1802d8f840fce2",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/rear.png",
      "sha256": "e1dbf6f458fe272108f8c59b4756173f772c4c26a20ccca1820306e30dfd0e48",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/render-config.json",
      "sha256": "4246d1dddc124c2829e0326a8d3d548122f83668d697078568a9cab09c7461da",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/render-manifest.json",
      "sha256": "eea11d3cc7077c417232e407b328b29a11d9f00fd0825e7924b470cd72828bd7",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/reversehero.png",
      "sha256": "7ae4240e51b50f61bd7b3d98e92e54b00f89366ff037605bdbafe9b1a535421b",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/side.png",
      "sha256": "1899e078cb122708fc019ccd9a2947857dd4f173cc72ce7912b060ef0d08bec3",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/silhouette.png",
      "sha256": "948c709b2f35133bcde9086af11cbc5c5f9c5c3b9ef628c7316e09751e8841a5",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/top.png",
      "sha256": "656cb6a72eda984e62aaad150b12cc12c3088c0b0fc424d3b9ea8fc0a50b5f77",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof/turntable.json",
      "sha256": "28a66f3509d75c03ed9a3f846e1f84096725cbf87826bf302c14ec2618b29cf2",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/clay.png",
      "sha256": "3301e0c8013c98227bb2e8ac59cd52d57d37ea093aee1bff999431f34578a228",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/front.png",
      "sha256": "edb70bd8bf5b0a947543207c9938f1f2a806f5db5c0d11894406e9770dd922ae",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/hero.png",
      "sha256": "9309086d1937c338949b9bc4fde68967d811e696c75618763d0f80a8c79427ae",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/rear.png",
      "sha256": "47b47823a083f0f0d593fd5d44a220def105140833a86196d8ee3dc61cbbf4c3",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/render-config.json",
      "sha256": "0f1e1add748daa450c751ef068856eb17c434aec26542e478e36dccb6cbbe525",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/render-manifest.json",
      "sha256": "4c5a1d6e0c03976a68ebfccb8c489c1990ab659a5a342f061a68bf9196cbf83d",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/reversehero.png",
      "sha256": "baca69d3b30d9779a8061c0a26876fe37805dcbce05490d197bb553bff7182da",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/side.png",
      "sha256": "7adedaec6a676921be230107deb97d814ef060ec39437fb8a51cf2c089f84aa6",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/silhouette.png",
      "sha256": "d54960fd8913fd5ef99803b98bf5538f23e902909d34ddcffb5d7dfda1a7b9c5",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/top.png",
      "sha256": "57567ea30205d98efc1ee48cbe9a0bbc759afe16f36e9292facd5f1b3ee95d2c",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/proof-initial/turntable.json",
      "sha256": "caf9fd54ab65ead1c22b3ebea037f4736e3668798f5fadc68fbafc924a42bf78",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/qa.json",
      "sha256": "3614defb1c300f84811a9110d617efdd042d8aa6b4ecca18eaf18ce903ad7499",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/reference-declaration-amendment.json",
      "sha256": "cf1bcd17d4951c07586522f97f275207d4c7bd29737a11b7b92c0c18d79c7cc8",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/references-delivery.json",
      "sha256": "d13fcf87cec258234c5a5583aa37eacce0ce146d27fb9cd6b10d2a4f969c58e3",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/references.json",
      "sha256": "cf698befe17b201df5597d39156c065ab4ff4c372367c83aefdafd88a345ce96",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/cave-shield/r002/runtime-parse.json",
      "sha256": "a0f7fe72ebbe3e1db4a18e3d271d9a23e26a902211a7cf59062a1b0a7abe3bd1",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/brief-delivery.json",
      "sha256": "237c8e61466e46b265c148e5de3aac81e4807200db39ccf6f041b18db8533afb",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/brief.json",
      "sha256": "0733eba2c4e82592b0b73c669884855b45cd3dd88e0f9a4643c5d3823c65a0d4",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/brief.md",
      "sha256": "273686438ffef9b6cd51f022fddd23f7460c1a0c86c6119d15ad0f4fc3b3cae7",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/build-config.json",
      "sha256": "1d4b3ebd91785d72254324af29c5c3be8fff69a8a7797d76ecf8e4b9df3a6fea",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/build-qa.json",
      "sha256": "6e080549b1628bb42614ad2eb5fe47b576d23a270bcfd6ae734bdba95cd1ddb9",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/candidate-check-initial.json",
      "sha256": "1670c7ca991942219ec4cd4c3a3ffe232651e7613b5c95502881e05d8831d69c",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/candidate-check.json",
      "sha256": "26568a8417ef1e3757d4500888fd11568a4b88ed77b58ef4f273aa5b42c3cfe0",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/candidate.json",
      "sha256": "f98075de91c43bfd072380ae5aa3174bdee0a090072e4a04d9d4175823cbc89d",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/concept-completeness.json",
      "sha256": "cff146e72aa9e2347ecbdaf0842a352b896a88a92be4bc438d07d7cbfef1261a",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/concept-completeness.stderr.txt",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/concept-evidence.json",
      "sha256": "06b8e8da365e674ea9614d96290201a9462682f9822f777405d7f8f1d2c75ac8",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/delivery-freeze.json",
      "sha256": "3e5635ff0ba8df22210c05e22077b85e4b2a763565dcbe1b3978fab1541ada36",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/dependency-hashes.json",
      "sha256": "59344047b6518239087c50ec878dd4bf53e213edf5aa854dd79001b431658897",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/didymoceras.blend",
      "sha256": "4a45666f0d20cab05873179c5c2e7de9fc92ded2e528b1458d0f1165b8cfec28",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/didymoceras.glb",
      "sha256": "32526e504c03f9a7ababc367cb4291d7a3286d811d270ca7c90e8e3068272d8d",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/eight-views.png",
      "sha256": "b46c7d8f9ecec8b1dde999c1620464390685033bc2d2ce03089b48a1654b0c8e",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/evidence/rebuild-1.check.log",
      "sha256": "82e45a60e9bb942c49c95d6fcc53f6c873dd4a3c88a2ca863fbc550831386b59",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/evidence/rebuild-1.json",
      "sha256": "82e45a60e9bb942c49c95d6fcc53f6c873dd4a3c88a2ca863fbc550831386b59",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/evidence/rebuild-2.check.log",
      "sha256": "9271b6f298cbea48eb652a4813af4895c5d05c91aadcd9b4c33f2e412c823f34",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/evidence/rebuild-2.json",
      "sha256": "9271b6f298cbea48eb652a4813af4895c5d05c91aadcd9b4c33f2e412c823f34",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/evidence/runtime-parse.json",
      "sha256": "42ab3a4484f2806223e60550b0b9b42205a7cf7dfefc9594580353c24d1c88bc",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/evidence/source-export.json",
      "sha256": "4fba045c001fcfcfabb692a06ce49abd06415f1a8c39b2eb0b4da80957228f34",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/evidence/static-glb.json",
      "sha256": "df29ed2188498e368ff32bd3f4fdfef2c7435bf93b628457ecb1767fd83807c1",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/evidence/technical.json",
      "sha256": "6f95ffa60606a918efbe8b74c1ddc27d07a4cbaaf9bc64ff4b974da44b25b684",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/generator.py",
      "sha256": "4a4e93cd8749e7875a3b27ae67ebd66b459a69dad794a5149c77c9b63e75e059",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/gltf-validator.report.json",
      "sha256": "ded848870539abf84ccbe706943a127986e76c882030ea7c8418f4393e3af37d",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/maker-review.md",
      "sha256": "a6105c5817acbf546d7e68455d34cb347d20429d01d299cb14eacd9e40fa8e1e",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/metadata.json",
      "sha256": "b706254d4c20d690c4817bcb32b1c3fccbba609edab7256a7a1f8ab68ac5d8db",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/metrics.json",
      "sha256": "96ab97fa8e6bcc27829c50e902a6ed3f4bf2bd0a83017b3072934929cd155c6b",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/modeling-freeze.json",
      "sha256": "1e68c0c993e7eaa0557b48292ad97b8e7243600de5f0ee9256a29c0491a45d21",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/preview-hero.png",
      "sha256": "729345e987a326a8126f0cc12681e380ac1437b4b407bf767ee48f77cb3b4a99",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/profile-contract.json",
      "sha256": "0dae4397dd67c8d1724e2d1eeb3eff354ce0d1370272f4b881aa593db096eda4",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/clay.png",
      "sha256": "fbc95661c2883bc79adc09df378e852fad29fc091e461b3002dc8e756e1d7ba2",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/front.png",
      "sha256": "568ad3fffcfb5bad2a106adef05d223e141f66f2cb60d15737fc219c87b6bc65",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/hero.png",
      "sha256": "729345e987a326a8126f0cc12681e380ac1437b4b407bf767ee48f77cb3b4a99",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/rear.png",
      "sha256": "9052521305d6c61c730fdc8f7a1b40791e8e522e894f4619b7d62f9cb5fa71b4",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/render-config.json",
      "sha256": "7bcb88e1d81ea6c7c480117ae1b2899073a4360d689fe988550aa1d9625551a6",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/render-manifest.json",
      "sha256": "cbac8a2102d2ec7c544b7d2ae90eb0844265e4150ef96a609a5b0284794cfc5b",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/reversehero.png",
      "sha256": "6fbeb4c8ed446d6770cfb967dbc859873df1c04f99fbc5dad3008efce8b7b89f",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/side.png",
      "sha256": "071af4599bba9795e31e205b2d2a9e2d1a27ed6f8430336bd11284851dbcc865",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/silhouette.png",
      "sha256": "90f8506a2f1c69fe5345b282a47fdeb0fef49e807048561ba25cd510c5da14a8",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/top.png",
      "sha256": "e32431fc17ff29a235bd92065dd8bf4bb2f1574916b6b46ec8660094b6266d5d",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/proof/turntable.json",
      "sha256": "39b8805f207407bd973144dfe5dc77da7f7eb1484289b211a62e4a169ba996a8",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/qa.json",
      "sha256": "87dc8f4235b3f6c5ad54ec68770f9b3418d064a8dd8d4f63e95b9a570bf2dd02",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/reference-declaration-amendment.json",
      "sha256": "7af8e29d138a54b9b5e18c951e877c2387f402f3f8952213cc49dc2c707147b3",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/references-delivery.json",
      "sha256": "ada14af402a1e2858191d7e9c1186471dd1c89309149ab355b7fbe8e3c94f0a1",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/references.json",
      "sha256": "6baecd88991c3fd888665fcf07d367e2209f80403b0bcdc4aab51d348fe6f54b",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/didymoceras/r003/runtime-parse.json",
      "sha256": "3cc8774a96d2a6702bb9291690253dfba45f8125d31e2df92fd7874b730a1210",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/brief-delivery.json",
      "sha256": "b78ec9d742ee99a8bcc98e7dd9d34faa4731ccdf43b947193bc015fe1f981c3a",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/brief.json",
      "sha256": "58646a39dd047d10c625922274a8ddcc51b8271055d43c602a514b0028b70610",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/brief.md",
      "sha256": "27f6a68830847b522a726330f0b933940a14b515df38a36e8718efbce0165cc7",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/build-config.json",
      "sha256": "30a30241dce575f114e778db095f8f39e3086f65168ee5f94cc63d8689f3c91a",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/build-qa.json",
      "sha256": "d0b605c986583de655a4fd15c8bd4db3b623997af2ab73bc5c921ae2637773ad",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/candidate-check-initial.json",
      "sha256": "b6b383d3749099f4a57b7bfc5c99d5f9d78ebf11c4474edb86c63af882158c4d",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/candidate-check.json",
      "sha256": "9a7970d28050f1ad40df72f61f6f7e4381b012599234ee507b730d47ee733300",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/candidate.json",
      "sha256": "f50307bf859549bc6eb20e4fad0d44996892aeea25e2c579ea8e76daa83a02c1",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/concept-completeness.json",
      "sha256": "6748935aee0ac2af65666b76b434d908e749e9889e72979188e07c3e29d9fb61",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/concept-completeness.stderr.txt",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/concept-evidence.json",
      "sha256": "a8a5a3b5c0fb31bdf52a1f2e430a11b51680772f53160b99615fbade08701250",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/delivery-freeze.json",
      "sha256": "cb957473df30e2803706ce0d1e0344c1f1226006a13dc195fe958105f8dcece7",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/dependency-hashes.json",
      "sha256": "87dfea3dc0b7a78005dc22738809823676991c2373b0b62ac2b343dc2131581d",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/eight-views.png",
      "sha256": "b7a53f878d20a25a49e6dc5a8a92905c0a921b51767afa47da4e141ff6df38b4",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/evidence/rebuild-1.check.log",
      "sha256": "87b9597a14f88b4bfeec41ee2df30e4df2fd8c0577925b9ba2341e981c6f59b4",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/evidence/rebuild-1.json",
      "sha256": "87b9597a14f88b4bfeec41ee2df30e4df2fd8c0577925b9ba2341e981c6f59b4",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/evidence/rebuild-2.check.log",
      "sha256": "d7e7bd33dbb11783f4464c8047ed3901c6609c4f1b677f96734cacc627cb5392",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/evidence/rebuild-2.json",
      "sha256": "d7e7bd33dbb11783f4464c8047ed3901c6609c4f1b677f96734cacc627cb5392",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/evidence/runtime-parse.json",
      "sha256": "67733f9fa6a0761b364e090ef5655a971e7fa20b142c3b8bd6ba6728963d91e7",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/evidence/source-export.json",
      "sha256": "4e3f8b7abd88d1a9dcdb0aa5d7788253e052cebac23d41de8f395e4915ef2825",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/evidence/static-glb.json",
      "sha256": "04da294e9ada14da607a15fc283be9aa4d9b8dcad4c65e5fa527b1b9b944f09e",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/evidence/technical.json",
      "sha256": "2c644da81a0ca47053a47fe8fe23ccede0003fde361b8106aeac49a100a0eca7",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/generator.py",
      "sha256": "a5ec704a7d7b7711d1fa575edaf4e2a8d2e4c7381583cc7e1f46b59a1e01ab21",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/gltf-validator.report.json",
      "sha256": "6c9db0f45beecb295309aefb611a38e13507e467bc69839bd5129b2fd32e67e6",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/maker-review.md",
      "sha256": "09c509acb94c62b28a11f5ad1b09dbf8aa0860dbde64e4ef1ce00df22419bbca",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/metadata.json",
      "sha256": "a1ca2a0a88d7719eb8c252abfa078db9f89fb35e5dfc48cb5f3a1c677f33d1dd",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/metrics.json",
      "sha256": "22fc5e2ce9fd852093300827d5f75d8fcaee58a78367c9bd6866ae94d1039f91",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/modeling-freeze.json",
      "sha256": "5a0ba845e4b0aa8da6dcbde14f5332a645b48eef75411c54231cbaae6eaa1784",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/preview-hero.png",
      "sha256": "2d53d3536cbb1ba2191df5fc70db48be70545cbae5e7d1bd0810555a38b18517",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/profile-contract.json",
      "sha256": "b22cfd5cd46fb324a5faef6ad68ec042a55bfaf1eb4696b26ab7d698d7bc946a",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/clay.png",
      "sha256": "039e7cfcb7f17ba925f09b9eeeda1812f64c563b4cfaa90c9698d4fd8e285ed5",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/front.png",
      "sha256": "f233c808584ed9bfea06487c8e7372d547efcfc9f3785a80bb5a2ba9482feae1",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/hero.png",
      "sha256": "2d53d3536cbb1ba2191df5fc70db48be70545cbae5e7d1bd0810555a38b18517",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/rear.png",
      "sha256": "223e0ce96902441c5663b8488d1f19bfd820fff0afc5ccfb2425de3ebf5661a8",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/render-config.json",
      "sha256": "5d046d93c65297dd49041b8a9acaad5d8658a9e26bfaf5dc4b6dfe9fde3deb13",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/render-manifest.json",
      "sha256": "ea4cafcc5f47d3e80f10ae514846cbd89404078c560656b273edbdcf42ae928b",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/reversehero.png",
      "sha256": "1bcd977ede0980de51042530baac08a7bb6068b40fa742a841a8673a8394f15c",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/side.png",
      "sha256": "2eafd38c47316ac91ef17cd9fb34517ec720d88d424302ceb4ee8273c22c09ea",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/silhouette.png",
      "sha256": "92a7e6b7def63ac3151c6c27cc3bc2f7922fd1951b2bde967233b044941438ac",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/top.png",
      "sha256": "df4401efed9a978028e01737acdaccc8ba940e8082d55068f0151e7d6f826b61",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof/turntable.json",
      "sha256": "346e1b6d6fd57dab123c46df9589147be38dcc22688ae8063bb40dc20ee9ca6a",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/clay.png",
      "sha256": "1672d7e7665a7d766d88a1bc386aaf024c9926fae3ef21fe721e02bd1f64ddce",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/front.png",
      "sha256": "f2a6bf6931e632594a887cba97c8ebd5d21f70369e3b76cb9b5cefa225380b87",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/hero.png",
      "sha256": "b2ff2e12440836ce2b4b8e401d956c8301e91853c30c71e62afcdffafdb4bca3",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/rear.png",
      "sha256": "1cc137f6a577c22736dac180610919870fe8bd8297f4dcd31cb2331f78744c24",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/render-config.json",
      "sha256": "c0f38d6ef18f7a31b7dc7cccf1104275596a7d823695447506f6cb6f2fd23079",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/render-manifest.json",
      "sha256": "f671af43229759c010ceba7c767842990c60a179ef8826aa9ee1ba9f21317430",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/reversehero.png",
      "sha256": "fcc1dcf5a13e9d9672cc89d88ec9b30f422d302ec8bc805c41deb074bdbdf231",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/side.png",
      "sha256": "5ba0b2829c7151b1113ed58d649550ca4b8cb379c52418517a4e75f891335eb9",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/silhouette.png",
      "sha256": "ba3cba9d44e8b3a936db4271f8a6a5b0dbe6df81ea61f95fd873cbe02b67ffa1",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/top.png",
      "sha256": "61a38f0bbecc46757fc16910faffd8d04de2544b1c0b7e8b832adc518ac9cc9a",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/proof-initial/turntable.json",
      "sha256": "240f01d4974c31cfd057f1c4ab562714efb06b9c227876403dfa2261e2476d41",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/psammichnites-ribbon-trace.blend",
      "sha256": "cdc84db78f44065fb6ec02828d2bc4ff629b7f189eacd82647a4e34d41d42caa",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/psammichnites-ribbon-trace.glb",
      "sha256": "d6e23b814e3aa68fa1f47cf23755e3fd15d895748fe4720ba5a49b7a6744ec87",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/qa.json",
      "sha256": "181281246bedd302b13b24d2f023ce28be7c196248ca2a8978272179a022e2e7",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/reference-declaration-amendment.json",
      "sha256": "a2195543957c1711439f6d44540ed03db1e22fcff055c6a0244fed5aec6f0017",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/references-delivery.json",
      "sha256": "065f64fe60e6bad21a306d999aaf1c52961aaa1f28e4de372aea7bfc37c4b92c",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/references.json",
      "sha256": "8b614811ce9fe0a54b298ae546f163a0be58659de203e829e9d92935b79b240b",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/psammichnites-ribbon-trace/r002/runtime-parse.json",
      "sha256": "d0af50b684d50687a05e92d6c8bdf6a0f52a3d82ea7da5356f1579cab3c83324",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/brief-delivery.json",
      "sha256": "75b50ce8311d89a345bbcfe086ca9a1f08d218bcc43c5453395d72dce248cc22",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/brief.json",
      "sha256": "7bebba0a627c6546660732987ae54dba5e0b37ccdb343da2479529693661b700",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/brief.md",
      "sha256": "1930a479f9405174132c2723e1f201a02550a5635d39397eb5928a3b1f15b6ee",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/build-config.json",
      "sha256": "50657cf6c3d1e8d612469148f95fb389cf0a42bacba11766ba78585946cc96fa",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/build-qa.json",
      "sha256": "871167359cecca2e6dc86a67a127819966f5abbf26653183c634b3d618b8c47d",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/candidate-check-initial.json",
      "sha256": "463659cb4604ecb97120d1f31dfa203d00c035c714f9df7759034d37088339d0",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/candidate-check.json",
      "sha256": "9508e420e8adb02a4834a06f49264a50970282a7c8a0ef2860cc03aa980daa15",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/candidate.json",
      "sha256": "4812625e458d703af8f9a6cd23cbc9bd31b45ea79183305710798b3392a49655",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/concept-completeness.json",
      "sha256": "d60cc4a98696e9791d3128374db43b7d9458e0b0bf2e5781be95fb6686a6a7dc",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/concept-completeness.stderr.txt",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/concept-evidence.json",
      "sha256": "ffbd824e5bd7aa95535e6bfb7efd575412268f8dca5b7d7fa1800a0f625c8fdc",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/delivery-freeze.json",
      "sha256": "5648d2ce3194cb9303a40e2d57f6c594a2afd951b68094eef7de6a2629ca6a9f",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/dependency-hashes.json",
      "sha256": "58b2ab59052f5ce5dc1c6e64de166e889b35fdb7ed85acb6f6b71fec7f9ee8b6",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/eight-views.png",
      "sha256": "ed850c337a6d727a69b77484cc0265260015746669eef926898333dfca6d7bdc",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/evidence/rebuild-1.check.log",
      "sha256": "12400b4049b01b77bd6cab6bf57e7607ff99e7139ec232193b124e3e03f9410f",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/evidence/rebuild-1.json",
      "sha256": "12400b4049b01b77bd6cab6bf57e7607ff99e7139ec232193b124e3e03f9410f",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/evidence/rebuild-2.check.log",
      "sha256": "e76c5398033bd465bd10fef242c3c4f110dda6cd5cb504de2e6946dcb000ae9a",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/evidence/rebuild-2.json",
      "sha256": "e76c5398033bd465bd10fef242c3c4f110dda6cd5cb504de2e6946dcb000ae9a",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/evidence/runtime-parse.json",
      "sha256": "964954cad0fb4df481df6e76427b7b923673f5d2223986e8252eaf9f799f925e",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/evidence/source-export.json",
      "sha256": "1b14a4c44930b66502e0869e6ca6dee02c7ec6d7ed7f3af807c6afe180e3bdeb",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/evidence/static-glb.json",
      "sha256": "ec586746c962ed4fd9b7560b8728f5226daabeac423c9df3a17111fcb94cfe83",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/evidence/technical.json",
      "sha256": "b25e64d98c20275a02ea8379f3090eac5f017985af3c1d3a3fcfe49dd1df9174",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/generator.py",
      "sha256": "4a4e93cd8749e7875a3b27ae67ebd66b459a69dad794a5149c77c9b63e75e059",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/gltf-validator.report.json",
      "sha256": "7be7af16dc9f3fc63730811d15d056eb90f9ba02b48898ca0182a63ec3abd81f",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/maker-review.md",
      "sha256": "94cf8cb4236b110099ecc1bdb8cdec9a4046f668c4692944add96c79cd6ae27a",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/metadata.json",
      "sha256": "e636c43ac24e3cbb5f044deb7a158baf8e3f1e83c926314be6c6233fb4f29aac",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/metrics.json",
      "sha256": "d8f53f4c897243bc219086ad813b7b9933023b1c7bd36ddbb0a3e477deb6a4cd",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/modeling-freeze.json",
      "sha256": "41c4fad58f5ac16b7e3ae054c56be2ed5eeedafabdab29a0d3f21071eb257498",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/preview-hero.png",
      "sha256": "480e61b74b3478c703136508d65d32cbf00522df0ada493f86326ab6c55f0766",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/profile-contract.json",
      "sha256": "bde9df80ecededb8785c5520542e33c308b8af0f3724f2e2255049933a16a229",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/clay.png",
      "sha256": "3df6f4afeb88505e0a517aa05f5a078669be72b01f8e13719bd6a44b7d189407",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/front.png",
      "sha256": "647707f53a40614730b877f062204992abc01c0c3c2848011c177c6d055241c4",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/hero.png",
      "sha256": "480e61b74b3478c703136508d65d32cbf00522df0ada493f86326ab6c55f0766",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/rear.png",
      "sha256": "0c935b01e69711f07568f3cffb59c8da96d9a7767c822f0c4840283871be76e9",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/render-config.json",
      "sha256": "aa0e42f2316686ef1b498157fe62dceb03f72b2172a28b3e9a9e2fa28c5d2fc6",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/render-manifest.json",
      "sha256": "35451e430898a84a883f857b0506fba474cdbe7676840289efc2e69be011e537",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/reversehero.png",
      "sha256": "b195e085627e81776e33fe94b7186193831733b5a766e6f2df4c328941df570f",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/side.png",
      "sha256": "1d55b8c77a246f15e6b5ceb897311a9804ab54ad3e9c69a3be0215fdf9605d1d",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/silhouette.png",
      "sha256": "ca4926c2af3d6daf578a3db310453c52ee55a22b05fd991839b2eec741780511",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/top.png",
      "sha256": "d201547b3d907e7b30f44cbf9cb126772eb967cf6187bc3e2be3c3c83c5da814",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/proof/turntable.json",
      "sha256": "e1d197643e57e3042960fcf93673c9e8a68d74a5b717e019fd16f1e5a82f6b91",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/qa.json",
      "sha256": "14dd8038912f37e547280a97f320f21c0cec5b84fba109ccc90b00d7f5ba3bbd",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/reference-declaration-amendment.json",
      "sha256": "b73cd0ea698299b2d4cc98e887eac6d9f2bc5ee1b5ec2c7b3567bae070058021",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/references-delivery.json",
      "sha256": "f92914141ae7a15df62483d694ea180e5a3fe6879e1f951dcac272a0327f0690",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/references.json",
      "sha256": "f60fbfad08303f559f0570482d8f0fd31e035ac7b77b4a5487449574a84fdbcc",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/runtime-parse.json",
      "sha256": "ce94958e8641df90c496745408d8c7b1a6b736d5c73c55113f77662f9df1cf34",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/spirematospermum.blend",
      "sha256": "ef1300be85201b1b2cf62a1bf9d267d74bbcedd97d8dc351ddfd2104dffd14ee",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "assets/candidates/continuous-small-life-round19-20261020/batch-54/spirematospermum/r003/spirematospermum.glb",
      "sha256": "816fac9a751596664f39da97257acdc70a60efe39e83042b31e8d84d72f648f1",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/concepts/generation-record.json",
      "sha256": "e1d91fae6c27b70c3bfd147dd26bbf813b1401b22b026e18db0f10bb396023e6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/concepts/invocation.json",
      "sha256": "c2d4f576a874637077ec68b41c6415685ff845dd4a4d58a2179342cd4926d69e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/concepts/original.png",
      "sha256": "bb7fb4d66a28075770d03ffbc55d145542d35d683ab5efde2d985a2d8fc8db46",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/concepts/prompt.txt",
      "sha256": "0bc4d5c78c714ae18aeb2d9c8506ff836fec41ac419e944d5683f2b7a42a54cc",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/concepts/tool-result.json",
      "sha256": "4d3141cbfebf5075b247a16e51099aed03d9de06b2363c04333ab8bd5899b44a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/cave-shield/r002/rebuild-1/f12ce3ab0e95b8fed12537562b7b162545ef4278f235985b036da4531911468c/20261020T003321-5663e37393274e1b9fdedff60ac7dcd1/request.json",
      "sha256": "31e62368b9346a93da6cb61d8519467b189b7566ef731218357cc4bbfee3e7bb",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/cave-shield/r002/rebuild-1/f12ce3ab0e95b8fed12537562b7b162545ef4278f235985b036da4531911468c/20261020T003321-5663e37393274e1b9fdedff60ac7dcd1/result.json",
      "sha256": "b9dc4a2106b0ddea52460db3bdf06d29ea597d45c704e0ff9b29a9c2356db196",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/cave-shield/r002/rebuild-2/53454bc80edb443867ee87babe8d1507f6d298770d00d6a3b082e046f5760b9b/20261020T003325-5c367ac9f7c74102a98be9ea11dfe7c3/request.json",
      "sha256": "a627ef6434672bed13faa9d521e0f924cd4006decb5097c6094e29f7ac3a74ec",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/cave-shield/r002/rebuild-2/53454bc80edb443867ee87babe8d1507f6d298770d00d6a3b082e046f5760b9b/20261020T003325-5c367ac9f7c74102a98be9ea11dfe7c3/result.json",
      "sha256": "797597d501fef0f21e8666ee00e269ffff517a169d9961ee4883710f645305f1",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/didymoceras/r003/rebuild-1/a8367be2fefd785ba9a53a62ae8687cec375f1cb41fb86b6c57f5ecad6832a9d/20261020T003452-ed4ba4761e5245edac353f2bc1826107/request.json",
      "sha256": "8303f5643f87fde95f826091a85391e34b1320449b7350b0be22fe2cb269e3c8",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/didymoceras/r003/rebuild-1/a8367be2fefd785ba9a53a62ae8687cec375f1cb41fb86b6c57f5ecad6832a9d/20261020T003452-ed4ba4761e5245edac353f2bc1826107/result.json",
      "sha256": "c54072667b99170857a599ff4d81da86790990604d90dcd0f8a03236ce9d3bac",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/didymoceras/r003/rebuild-2/382194a91e714f401b5981ea991b5c3350cdf97c8c21412c9b4052170ca0ab2b/20261020T003456-4421ae615e3d4db2aed9f894eddeff44/request.json",
      "sha256": "08b0162e058ecab3b038b0e4eb2fa02d8a394af606d037b540c853df3a433cef",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/didymoceras/r003/rebuild-2/382194a91e714f401b5981ea991b5c3350cdf97c8c21412c9b4052170ca0ab2b/20261020T003456-4421ae615e3d4db2aed9f894eddeff44/result.json",
      "sha256": "4283521197ad932f0d48809bc540fd7beec26f4b50bab921eacb4bca80aad9e6",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/psammichnites-ribbon-trace/r002/rebuild-1/280316d32fb7c31b5ddb394ee2e6d9492bf357bed9a65498f741598243474bff/20261020T003334-be8df99f0ff44a18b421f8e96c204b77/request.json",
      "sha256": "eb6aecfe89a6f392acc20da9d90440f5e30de3f4252c217403695e5f12f8a2de",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/psammichnites-ribbon-trace/r002/rebuild-1/280316d32fb7c31b5ddb394ee2e6d9492bf357bed9a65498f741598243474bff/20261020T003334-be8df99f0ff44a18b421f8e96c204b77/result.json",
      "sha256": "a460406b3d6a5887073615be5cf81ae3cd94540fdcc090762ad22b12bca05597",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/psammichnites-ribbon-trace/r002/rebuild-2/120d368ca89f72d1a937cf56af0d04e90e52c3988f91c2c77fae47204c628a3b/20261020T003337-93f97e0c55df44ed92e4ec185f986c5d/request.json",
      "sha256": "c299b35cc617b709d271aa033b74ba1f61769e9d39a8523880e8676c5f1ca5e2",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/psammichnites-ribbon-trace/r002/rebuild-2/120d368ca89f72d1a937cf56af0d04e90e52c3988f91c2c77fae47204c628a3b/20261020T003337-93f97e0c55df44ed92e4ec185f986c5d/result.json",
      "sha256": "d2bfdcab6e1c837ea8258e9872ba0a99fc0d16c3631421ef6b561e7b005e8ec4",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/spirematospermum/r003/rebuild-1/df7c5f592568f74a89ee34658a6da2d9a5e9befbadfaa86ba259851704676f6f/20261020T003500-9a5c6925a3764ab3825580b4f0cd9ba6/request.json",
      "sha256": "ee887d2374b7fc917c5e72eca4293202098c181d40201979543f3bda3b76a75e",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/spirematospermum/r003/rebuild-1/df7c5f592568f74a89ee34658a6da2d9a5e9befbadfaa86ba259851704676f6f/20261020T003500-9a5c6925a3764ab3825580b4f0cd9ba6/result.json",
      "sha256": "610bc78b0efd63af3220f1c66a144c43ea4aee42bead69f930bcef8d63b59c7b",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/spirematospermum/r003/rebuild-2/90c2a22628f8aca05e61ee8b00dce8fcd51181051412fef50304cb14c99fe5e9/20261020T003503-f8f756447caf40be86059826fe17111b/request.json",
      "sha256": "d2b30726db4aca270aef4f2b2f755066af0430b45daecdc4ec299df6b06d0f92",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/rebuild-runs/build/spirematospermum/r003/rebuild-2/90c2a22628f8aca05e61ee8b00dce8fcd51181051412fef50304cb14c99fe5e9/20261020T003503-f8f756447caf40be86059826fe17111b/result.json",
      "sha256": "d0e68bbbd189e72e3c0757455933de4af783f90e4cabc429d833a12efbae1521",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/render_exact_glb.py",
      "sha256": "1354910a72831a66c8bc2ffb9ddc41f59a20f0094a7a8262cdf8e667c4d975f2",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/runs/build/cave-shield/r002/build-r002/c9f51d8d5027ed11e2e81831a6d22a32b74676e0d39bd27b708b7e2ddcfaa168/20261020T003203-5a4cdf41a46d4aa88fa2475e5c511391/result.json",
      "sha256": "70dd2ce9c570bc6e8c895b4d5ebafd353479e1d1c1f11d4a5141755c486e6e48",
      "origin": "source",
      "owner": "cave-shield"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/runs/build/didymoceras/r003/build-r003/57afc3ae39de4a7a11e9e8f3e69fdeb65f4a07ed56462339eaa64c1e00c6907f/20261020T003413-e482da98c456426a875a16377128e412/result.json",
      "sha256": "e6e3976a47c0ba503871ee84ebc951c0ad8241727eb2579f456ccea2c071235a",
      "origin": "source",
      "owner": "didymoceras"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/runs/build/psammichnites-ribbon-trace/r002/build-r002/d574dddcbf9e5fd6b9b67f536ed28fdcdf728b55143d75ff696ae8fd3a9c8d77/20261020T003209-fc6ea7fceef940dbbf21e03b0631c13d/result.json",
      "sha256": "444643605bcd929297247ccd3d1359b151270814fbb28031737f3503049c044a",
      "origin": "source",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "production/continuous-small-life-round19-20261020/work/batch-54/runs/build/spirematospermum/r003/build-r003/cbd0910ebf84e931f97cd404e94c3cd5cc2ec65c3b34abad69b6bdd08b16ce96/20261020T003420-6604bfe65111463ab8e03c31cd95805f/result.json",
      "sha256": "86c2e927fbf639d5ed825d7fa2b97a3ca3ec283aca2fd02347420938e05e7479",
      "origin": "source",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/concept/generation-record.json",
      "sha256": "e1d91fae6c27b70c3bfd147dd26bbf813b1401b22b026e18db0f10bb396023e6",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/concept/original.png",
      "sha256": "bb7fb4d66a28075770d03ffbc55d145542d35d683ab5efde2d985a2d8fc8db46",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/concept/prompt.txt",
      "sha256": "0bc4d5c78c714ae18aeb2d9c8506ff836fec41ac419e944d5683f2b7a42a54cc",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/cave-shield/clay.png",
      "sha256": "c3784810559740457e9e65ced91a954c742c53ac650c7058d9ca188e0ae513df",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/cave-shield/eight-views.png",
      "sha256": "16e3e368a362e0cb0591251c86ff250ff221dc861e481576acb7f67012936ca1",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/cave-shield/front.png",
      "sha256": "5bae12b927cc811266a1af19ea7c116013bad89cf9a63266aaaf4f5cbfc58827",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/cave-shield/hero.png",
      "sha256": "4ebb5b2f738cda0b8d2a5a8e0280178b2f45cbcfc190c6212b1802d8f840fce2",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/cave-shield/rear.png",
      "sha256": "e1dbf6f458fe272108f8c59b4756173f772c4c26a20ccca1820306e30dfd0e48",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/cave-shield/reversehero.png",
      "sha256": "7ae4240e51b50f61bd7b3d98e92e54b00f89366ff037605bdbafe9b1a535421b",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/cave-shield/side.png",
      "sha256": "1899e078cb122708fc019ccd9a2947857dd4f173cc72ce7912b060ef0d08bec3",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/cave-shield/silhouette.png",
      "sha256": "948c709b2f35133bcde9086af11cbc5c5f9c5c3b9ef628c7316e09751e8841a5",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/cave-shield/top.png",
      "sha256": "656cb6a72eda984e62aaad150b12cc12c3088c0b0fc424d3b9ea8fc0a50b5f77",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/didymoceras/clay.png",
      "sha256": "fbc95661c2883bc79adc09df378e852fad29fc091e461b3002dc8e756e1d7ba2",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/didymoceras/eight-views.png",
      "sha256": "b46c7d8f9ecec8b1dde999c1620464390685033bc2d2ce03089b48a1654b0c8e",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/didymoceras/front.png",
      "sha256": "568ad3fffcfb5bad2a106adef05d223e141f66f2cb60d15737fc219c87b6bc65",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/didymoceras/hero.png",
      "sha256": "729345e987a326a8126f0cc12681e380ac1437b4b407bf767ee48f77cb3b4a99",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/didymoceras/rear.png",
      "sha256": "9052521305d6c61c730fdc8f7a1b40791e8e522e894f4619b7d62f9cb5fa71b4",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/didymoceras/reversehero.png",
      "sha256": "6fbeb4c8ed446d6770cfb967dbc859873df1c04f99fbc5dad3008efce8b7b89f",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/didymoceras/side.png",
      "sha256": "071af4599bba9795e31e205b2d2a9e2d1a27ed6f8430336bd11284851dbcc865",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/didymoceras/silhouette.png",
      "sha256": "90f8506a2f1c69fe5345b282a47fdeb0fef49e807048561ba25cd510c5da14a8",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/didymoceras/top.png",
      "sha256": "e32431fc17ff29a235bd92065dd8bf4bb2f1574916b6b46ec8660094b6266d5d",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/psammichnites-ribbon-trace/clay.png",
      "sha256": "039e7cfcb7f17ba925f09b9eeeda1812f64c563b4cfaa90c9698d4fd8e285ed5",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/psammichnites-ribbon-trace/eight-views.png",
      "sha256": "b7a53f878d20a25a49e6dc5a8a92905c0a921b51767afa47da4e141ff6df38b4",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/psammichnites-ribbon-trace/front.png",
      "sha256": "f233c808584ed9bfea06487c8e7372d547efcfc9f3785a80bb5a2ba9482feae1",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/psammichnites-ribbon-trace/hero.png",
      "sha256": "2d53d3536cbb1ba2191df5fc70db48be70545cbae5e7d1bd0810555a38b18517",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/psammichnites-ribbon-trace/rear.png",
      "sha256": "223e0ce96902441c5663b8488d1f19bfd820fff0afc5ccfb2425de3ebf5661a8",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/psammichnites-ribbon-trace/reversehero.png",
      "sha256": "1bcd977ede0980de51042530baac08a7bb6068b40fa742a841a8673a8394f15c",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/psammichnites-ribbon-trace/side.png",
      "sha256": "2eafd38c47316ac91ef17cd9fb34517ec720d88d424302ceb4ee8273c22c09ea",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/psammichnites-ribbon-trace/silhouette.png",
      "sha256": "92a7e6b7def63ac3151c6c27cc3bc2f7922fd1951b2bde967233b044941438ac",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/psammichnites-ribbon-trace/top.png",
      "sha256": "df4401efed9a978028e01737acdaccc8ba940e8082d55068f0151e7d6f826b61",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/spirematospermum/clay.png",
      "sha256": "3df6f4afeb88505e0a517aa05f5a078669be72b01f8e13719bd6a44b7d189407",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/spirematospermum/eight-views.png",
      "sha256": "ed850c337a6d727a69b77484cc0265260015746669eef926898333dfca6d7bdc",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/spirematospermum/front.png",
      "sha256": "647707f53a40614730b877f062204992abc01c0c3c2848011c177c6d055241c4",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/spirematospermum/hero.png",
      "sha256": "480e61b74b3478c703136508d65d32cbf00522df0ada493f86326ab6c55f0766",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/spirematospermum/rear.png",
      "sha256": "0c935b01e69711f07568f3cffb59c8da96d9a7767c822f0c4840283871be76e9",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/spirematospermum/reversehero.png",
      "sha256": "b195e085627e81776e33fe94b7186193831733b5a766e6f2df4c328941df570f",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/spirematospermum/side.png",
      "sha256": "1d55b8c77a246f15e6b5ceb897311a9804ab54ad3e9c69a3be0215fdf9605d1d",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/spirematospermum/silhouette.png",
      "sha256": "ca4926c2af3d6daf578a3db310453c52ee55a22b05fd991839b2eec741780511",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/frozen-views/spirematospermum/top.png",
      "sha256": "d201547b3d907e7b30f44cbf9cb126772eb967cf6187bc3e2be3c3c83c5da814",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/cave-shield/glb-roundtrip.report.json",
      "sha256": "6a49324ce5299717a3fb8ead135d8d57e5684530d09e1fe4d682966db1d01dee",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/cave-shield/preview-glb-roundtrip.png",
      "sha256": "b56edc703857a1b6750e2c11a2f094566625cbb48901aea31499dbe9a0821869",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/cave-shield/preview-glb-wireframe.png",
      "sha256": "90f7d9c8f328e2ab771e9d931fff217b74059668be576d5aa641e0b0b657f689",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/didymoceras/glb-roundtrip.report.json",
      "sha256": "2e169c9399be66d1456f363418ef6360d59d00d2fc1547625bbefbf262f9cb25",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/didymoceras/preview-glb-roundtrip.png",
      "sha256": "c48f7b9f97cc649e5b6fd0e1da3a72505732006086df20b30978b36d12a1ba71",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/didymoceras/preview-glb-wireframe.png",
      "sha256": "613c3f41000d5c5d29445811f7b8bcce409be09bba38f7d8d74b291bc321cb05",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/psammichnites-ribbon-trace/glb-roundtrip.report.json",
      "sha256": "5fcacf18dfc0b273739a17ccaaa84bd8ae42c88ff407f75c82613e2a9b73252a",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/psammichnites-ribbon-trace/preview-glb-roundtrip.png",
      "sha256": "c6f6c0483b4108abf9308e1c93e6c11b7f237aa55905670d2aea7efad49b6168",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/psammichnites-ribbon-trace/preview-glb-wireframe.png",
      "sha256": "7667f16d72a77b242edb6cc0f9dabb92951d50fa5d7f579b92605e43e31c076d",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/spirematospermum/glb-roundtrip.report.json",
      "sha256": "ee711ecf4619a7580cb2f4cfa04b9434f75c44b069b2422e40e63336cae951a8",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/spirematospermum/preview-glb-roundtrip.png",
      "sha256": "62754bf0ea781a15579c614fec5d7c93b7512abea5a455328d50038fda5d5c4c",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/glb-roundtrip/spirematospermum/preview-glb-wireframe.png",
      "sha256": "c22d5dc9427af2d73be27a069e3a14b838ad89bae447c80a9a51d28fbb2aa3a5",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/khronos/cave-shield/gltf-validator.report.json",
      "sha256": "d8ad5c90f4e646d087174bc81419fe150a63d820c896b51a8687331eb05b0fd1",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/khronos/cave-shield/qa.json",
      "sha256": "d5e46e530265d76c5373c8eebad20c5bf4b8f8d18c809e716262f27229058b8b",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/khronos/didymoceras/gltf-validator.report.json",
      "sha256": "dd366844430ec014be7edc757d71b1c70cb1ad90d481928f120a674cb35056dc",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/khronos/didymoceras/qa.json",
      "sha256": "6a9b0d410e5e022e610548f7b8a6e753aaef973b1af236dff35001a59dfd3c49",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/khronos/psammichnites-ribbon-trace/gltf-validator.report.json",
      "sha256": "8eaa80083c1c84b66fcee4f17406c733927c6f48610064ccf92021a97995fd5f",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/khronos/psammichnites-ribbon-trace/qa.json",
      "sha256": "3b04cb0e25669fb1521f2722af399439d0d5eeef09547467359afc63ed358f28",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/khronos/spirematospermum/gltf-validator.report.json",
      "sha256": "ab534ee8d3684cebc525ca04c075ba0f2e484bdee0ba12431ce3f4270baf7d4e",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/khronos/spirematospermum/qa.json",
      "sha256": "4314e3ddd70e11afd23205b9a15e054c0ace72e3556cc92dec00914ea8374c15",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/source-export/cave-shield/source-export.report.json",
      "sha256": "8e737f6d6c84b9b7d1458bd2579bf14c95f5f8bfaf74ecababa59d6b52b1b68a",
      "origin": "review",
      "owner": "cave-shield"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/source-export/didymoceras/source-export.report.json",
      "sha256": "b81b725fa07227e771d5fb401c14c7e108e91f6945c92ea5f092cf04e02bcf15",
      "origin": "review",
      "owner": "didymoceras"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/source-export/psammichnites-ribbon-trace/source-export.report.json",
      "sha256": "687ec2bbb07ded76a4123b439cfaf00470e576c22ed83914fd9b1c741dbd2d37",
      "origin": "review",
      "owner": "psammichnites-ribbon-trace"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/independent/source-export/spirematospermum/source-export.report.json",
      "sha256": "19a878e9e4b85d0ce340de97e6785344dc495dc0f81b0154b8898b63533725f8",
      "origin": "review",
      "owner": "spirematospermum"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/software-webgl/index.html",
      "sha256": "2f953b69d79e70c8a6b4d8a0d989930835fe6f6e244133c1c68ad2412c493386",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/software-webgl/main.js",
      "sha256": "b6f7ab62ac3082566eb20ece1a40a62ec380a69025eb30382a4a8b303d99cca8",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/software-webgl/run-browser.cjs",
      "sha256": "93ed12c6894ee3bc895878b10dd297a4385cf280d3897d8bced9d0d6628d6efb",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/software-webgl/runtime-report.json",
      "sha256": "5707ea6c0384909454718617c46bd28a6be5fa739e30394986f4a35ff924a0df",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/software-webgl/vite.config.js",
      "sha256": "030987a13e3361a426ac22fd8b87fd18a05c8ce069ba24110658d31542e385be",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/evidence/software-webgl/webgl-review.png",
      "sha256": "9980533feb93cb8f4fafbaa7d662811d5f9969a6593981ec248f1856113243b2",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/report-data.json",
      "sha256": "9f5fa2c212810feafeaf23b6d1d7f1d267bda61fad747f5e493abdfb5d98eb7e",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-independent-20261020/report.md",
      "sha256": "70c9023a49ee6c67b556871c3484722ceda1050dcd0071e444b5792b1b8178d1",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/capture/assets/turntables/index.json",
      "sha256": "874c91b833a5084ab91aee14fef650fafba5de09dd945d1924824051d5afeef9",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/capture/references/cave-shield.png",
      "sha256": "0c8cc0040d81fab701a0713b37405e2cc39a196b299fa27bd2e6e4a635edb66a",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/capture/references/didymoceras.png",
      "sha256": "87fc3176a72a9948c16919c75f6f7c6a300af46f264eab4773eddc9e8e85938e",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/capture/references/psammichnites-ribbon-trace.png",
      "sha256": "f534407262a5e13690fb535ae0837c57eae47d758a94f41784f12ee2a9b5c435",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/capture/references/spirematospermum.png",
      "sha256": "a11a1f953a1b634dc99da456aa94da3ccde7557162c42cc6e054cd9a5f8cde01",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/capture/render-report.json",
      "sha256": "25a892394b4bde3d14a3b5d2d597ce5bbd55fc253783fba15c15174890b0f2bf",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/capture-independent-verification.json",
      "sha256": "7359fd4f8e73eb3f30ff529897073c7e5e8f73095fa890c0cf56e2d252cea537",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/capture-inputs.json",
      "sha256": "73c930bdf687687ff9ff66a3b9312406c6f5dbacfe9bcc423fdadcb1d732ed24",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/capture-provenance.json",
      "sha256": "51a0680076af52a853222bc0625bef26408ff61612a01a276c38e9537abd3836",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/dispatch-binding.json",
      "sha256": "664b6faf71825718f6b70a913d01ac7278fd4aadc0068f30d4b6090339d6e930",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch54-release-20261020/source-integrity.json",
      "sha256": "30fe78e7dccbe9790a3ec4bac5e0ece818f063fe50def166398417dd9fa169e7",
      "origin": "release",
      "owner": "$batch"
    }
  ]
};

/** Exact bounded Batch58 release; unchanged formal gates. */
export const BATCH58_RELEASE = {
  "version": 1,
  "scope": "batch58-20261020",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "provider_generation_timestamp": "unknown",
  "source_commit": "9bb7eb242a2c7ee35868ca57789c93c06c4bcbb8",
  "review_commit": "48f08fa3e2d6bb9a06526efd7142c4fc35184d86",
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  },
  "base_descriptor": {
    "path": "assets/releases/batch54-20261020.json",
    "sha256": "18848be2e9bffb004c8301ff7f05816ab0d691afbee6b569459f28e3099f3f4b"
  },
  "source_bundle": {
    "path": "qa/batch58-release-20261020/source-bundle.json",
    "sha256": "0d76609ebde90f4979bdc85c681d59a184c4fc0e6ba6c00dda9e05a523379eee"
  },
  "protected_source_inputs": [
    {
      "path": "ATTRIBUTION.md",
      "sha256": "31cfae805768d2857f9cd3b86d328ba1ec83f3c28ccc728b0cac8edddfd29412"
    },
    {
      "path": "LICENSE",
      "sha256": "9dc06b87ac2f86cc6c7b3afdd8b02c5887c9a29bf5a4924a611937d4195f996c"
    },
    {
      "path": "LICENSES/CC-BY-4.0.txt",
      "sha256": "9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411"
    },
    {
      "path": "LICENSES/MIT.txt",
      "sha256": "f4cd278b3853ba4c6b36d85975839c2b51d09bb841d6eecced516c482e826ce0"
    },
    {
      "path": "package-lock.json",
      "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
    },
    {
      "path": "package.json",
      "sha256": "1bddf73367b09c1c72034cca826c1dfcebc1ae35e1480d9da99b8fd202a34b1b"
    },
    {
      "path": "production/policies/qa-passed-batch-publication-20261018.json",
      "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
    },
    {
      "path": "schemas/README.md",
      "sha256": "cdecb3681106b07e1414d18a4861162525da67d7061e7f7539f40c0fc817d615"
    },
    {
      "path": "schemas/templates/brief.template.json",
      "sha256": "cb1f2ff179d3363f0adec9717be204e2a355056686fadf792eea232c82b9278d"
    },
    {
      "path": "schemas/templates/candidate.template.json",
      "sha256": "3148c62284480a8118bc89135a3fa1371cb0c86f2726369338c499fc32dc2a91"
    },
    {
      "path": "schemas/templates/references.template.json",
      "sha256": "9c43e161399f377d2e943f36ddcecf84330618495689f461fb1b8beba80d288b"
    },
    {
      "path": "schemas/templates/static-profile-contract.template.json",
      "sha256": "538e12417c3d77e84746e8a4814c3c18701c18d327707b8ac4043fdea32c8ce4"
    },
    {
      "path": "schemas/templates/textured-brief.example.json",
      "sha256": "51a3b254d288bdc5f2716f6272a57539529cb17ac8939cc1c2787d7416ab5ab9"
    },
    {
      "path": "scripts/asset_common.py",
      "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
    },
    {
      "path": "scripts/candidate_profile.py",
      "sha256": "0489ec5378ec5d073ac4e84994b796ac529b122fd1c9c51be7b55623a413ac7d"
    },
    {
      "path": "scripts/check_reproducibility.py",
      "sha256": "62ab7b959ad8e73128d1d1f2300fd4bd19ecc92244bccf6cc88fdc7b0b3a57d2"
    },
    {
      "path": "scripts/check_source_export.py",
      "sha256": "1b4aafd9d1963e103ba469aff7e1f3917592e839f9372883b88c7db51834b34a"
    },
    {
      "path": "scripts/qa_glb.py",
      "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
    },
    {
      "path": "scripts/render_candidate_views.py",
      "sha256": "22a4bd8aab71dc76696f01f2bd768ad371ebf9b4230e170c921063b5f842f041"
    },
    {
      "path": "scripts/run_asset_queue.py",
      "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
    },
    {
      "path": "scripts/validate_candidate.py",
      "sha256": "fe679a8be19d16b9d9b86ee3419a73d2dd16b77dfa371bf1186ce0120d120ff9"
    },
    {
      "path": "scripts/validate_concept_evidence.py",
      "sha256": "745938a9b1624e8b744e9c03f597fd8d967ef1b4c145209805c6b6357578c723"
    },
    {
      "path": "scripts/validate_gltf.cjs",
      "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
    }
  ],
  "review": {
    "path": "qa/batch58-independent-20261020/independent-qa.md",
    "sha256": "ded5ef8f1fc70e1c71c0f730f194135e93e3c22f0505f016465a78f58343a6dc"
  },
  "review_custody": {
    "path": "qa/batch58-independent-20261020/evidence-custody.json",
    "sha256": "41df5be052aa4cbcf83ea73dedfd211379fa54814b47b4022d07e512db30877e"
  },
  "capture": {
    "report": {
      "path": "qa/batch58-release-20261020/capture/render-report.json",
      "sha256": "17fe72174a4c459ec7ba5bb602ec48bab23cf46113d6cc33213eb1930c37967b"
    },
    "index": {
      "path": "qa/batch58-release-20261020/capture/assets/turntables/index.json",
      "sha256": "e5bd58e972a3bfb450d21e8dc43dd5d19b68211d4a5fc2e0572dae03e0a35e70"
    },
    "zip_verification": {
      "path": "qa/batch58-release-20261020/capture-verification.json",
      "sha256": "420b42aa48a8e24456780cd1418f73154b6bf80baff54d34c4434dad48d04581"
    },
    "independent_review": {
      "path": "qa/batch58-release-20261020/independent-card-review.json",
      "sha256": "515434e55d62dae9d65996894bb4d438fc4650ecc1a4d33f999018e9fa25c5e2"
    }
  },
  "excluded_ids": [],
  "additions": [
    {
      "id": "calamophyton",
      "revision": "r001",
      "source_commit": "9bb7eb242a2c7ee35868ca57789c93c06c4bcbb8",
      "review_commit": "48f08fa3e2d6bb9a06526efd7142c4fc35184d86",
      "metadata": {
        "path": "assets/additions/calamophyton/batch58-20261020/release-metadata.json",
        "sha256": "b7be0c1dec716382a7eb811672c27852b69c9439cb9a941605625017e99c91c2"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/candidate.json",
        "sha256": "765c947ae1c33bbee590f3574c34c4a61a7a6aaf2e21123838964b4ff625b3a8"
      },
      "review": {
        "path": "qa/batch58-independent-20261020/independent-qa.md",
        "sha256": "ded5ef8f1fc70e1c71c0f730f194135e93e3c22f0505f016465a78f58343a6dc"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/metrics.json",
        "sha256": "b42413a8ed7ffdc854a48c3de458beb66d5f182894232a027e5b1b8a1013997e"
      },
      "original_metadata": null,
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/brief.json",
        "sha256": "abf73275f4e7d4fdc8f3176e93e7795acddbb0ef4a5301cb27b522ef1b8fad3c"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/render-manifest.json",
        "sha256": "42150cba486a47f5806785d0f345fef3ebfb9a197bf55246677c61f4abff70b0"
      },
      "rebuilds": [
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/repro-final-1.report.json",
          "sha256": "729d8be56e7ca25741d0274479d064fda51001f689ac546db953e918fa335a00"
        },
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/repro-final-2.report.json",
          "sha256": "412e34ca83f431a4fc2d533f08a006936c4cfdbeddddf29b329194c1603e36fe"
        }
      ],
      "capture_reference": {
        "path": "qa/batch58-release-20261020/capture/references/calamophyton.png",
        "sha256": "c71aa4e6ec4730101634f982b569f729eb30bff5bc2ebed95efbe0d7f3e5e365"
      }
    },
    {
      "id": "perspicaris",
      "revision": "r002",
      "source_commit": "9bb7eb242a2c7ee35868ca57789c93c06c4bcbb8",
      "review_commit": "48f08fa3e2d6bb9a06526efd7142c4fc35184d86",
      "metadata": {
        "path": "assets/additions/perspicaris/batch58-20261020/release-metadata.json",
        "sha256": "7a2fdcb075ceec62a4ccf6439965ff84e75c24519621585e4f6767f51c01098b"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/candidate.json",
        "sha256": "3e14024b74f08d4f5a459de54e7b25eb43dc482310abeadf780fd0c821d39d1e"
      },
      "review": {
        "path": "qa/batch58-independent-20261020/independent-qa.md",
        "sha256": "ded5ef8f1fc70e1c71c0f730f194135e93e3c22f0505f016465a78f58343a6dc"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/metrics.json",
        "sha256": "eadd5ed3c6636308be2ecb54ece5a0480442c59b8eda41b6948403f3bf20076a"
      },
      "original_metadata": null,
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/brief.json",
        "sha256": "7ad2fe63a0a6e3c0a97149c338b27b2aea81f0a024a40ba088a52ba71782984e"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/render-manifest.json",
        "sha256": "8de34dfdb60f99dfe273072476ca00b6d41991fa5ef53a4e314db3dfbb845f7a"
      },
      "rebuilds": [
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/repro-final-1.report.json",
          "sha256": "2eb0b047cc6fcfcfa371e0012d7caff6fa75090e2a764e56bbbc4671f8b6937d"
        },
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/repro-final-2.report.json",
          "sha256": "1fdb28613118e295ac92164effbec9ae756cae9c94fb261564bad1595b46b0cc"
        }
      ],
      "capture_reference": {
        "path": "qa/batch58-release-20261020/capture/references/perspicaris.png",
        "sha256": "ea53e321ac1ddca04afc15ecc8d1de64f7adf9001e067b38404e5b22046a8c89"
      }
    },
    {
      "id": "barchan-dune",
      "revision": "r001",
      "source_commit": "9bb7eb242a2c7ee35868ca57789c93c06c4bcbb8",
      "review_commit": "48f08fa3e2d6bb9a06526efd7142c4fc35184d86",
      "metadata": {
        "path": "assets/additions/barchan-dune/batch58-20261020/release-metadata.json",
        "sha256": "7f1f4a65e9841d17de8547d98fec6c01837782926c629c1f5d5f0b61b92242b2"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/candidate.json",
        "sha256": "cd3a51719b4b5ab7dc5256f037e8e0858b84b2b7eed558395f5cdf40701531ae"
      },
      "review": {
        "path": "qa/batch58-independent-20261020/independent-qa.md",
        "sha256": "ded5ef8f1fc70e1c71c0f730f194135e93e3c22f0505f016465a78f58343a6dc"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/metrics.json",
        "sha256": "d19d9bb2b9c19073aa2b60d30e43a2f988c054c31ef5cf588cb6da0adca2f963"
      },
      "original_metadata": null,
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/brief.json",
        "sha256": "55f728ba03957d5914f9487bb81c33aac3362441672fe85a9b1ce61f4b212ee4"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/render-manifest.json",
        "sha256": "0dd987aa3ca33777f719037321757dc18308af8f30ce8e77da060f0c6b083db9"
      },
      "rebuilds": [
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/repro-final-1.report.json",
          "sha256": "5e383dfdf6b6f34ee4fbba64a487ddcf5206e5b3a70d1b8abf80392940ca37c9"
        },
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/repro-final-2.report.json",
          "sha256": "091126cce5eb0f6307b38c423f50b658f6bc0de4406d665ff933d928d0966f8a"
        }
      ],
      "capture_reference": {
        "path": "qa/batch58-release-20261020/capture/references/barchan-dune.png",
        "sha256": "28d1a601a2e10784d7124e20aff1233ed9ce42802d560f1d0e64ec08f8824f35"
      }
    },
    {
      "id": "current-ripple-surface",
      "revision": "r001",
      "source_commit": "9bb7eb242a2c7ee35868ca57789c93c06c4bcbb8",
      "review_commit": "48f08fa3e2d6bb9a06526efd7142c4fc35184d86",
      "metadata": {
        "path": "assets/additions/current-ripple-surface/batch58-20261020/release-metadata.json",
        "sha256": "35df12cf8fd35c43750c2d50560f9545191afa267f000aca145b94e805bda925"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/candidate.json",
        "sha256": "d54f5c4dc2bd9cd26f91af500df540e8eab51df663c1fe176237ac9e8da45101"
      },
      "review": {
        "path": "qa/batch58-independent-20261020/independent-qa.md",
        "sha256": "ded5ef8f1fc70e1c71c0f730f194135e93e3c22f0505f016465a78f58343a6dc"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/metrics.json",
        "sha256": "05bce4fd0cb5ad499be332612c66a9807c6635b6332285451256230a317c96f7"
      },
      "original_metadata": null,
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/brief.json",
        "sha256": "86c9eff8908d6cf275f9b656c1bc79165e3962932bf55dcc22844db18028d00e"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/render-manifest.json",
        "sha256": "f855477019d11b7f0bf2586d5dd45fab583ac2fe3a6f4cb0b2f2f25352d80b09"
      },
      "rebuilds": [
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/repro-final-1.report.json",
          "sha256": "3eecf3518bbcbdbc3146659fbe222efe00077c2439059255f8c22ac5d592dc5d"
        },
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/repro-final-2.report.json",
          "sha256": "901fb26395b8a7b99ad4b54e7a5830e2d428c5b78d95d03701936e4c50b84e22"
        }
      ],
      "capture_reference": {
        "path": "qa/batch58-release-20261020/capture/references/current-ripple-surface.png",
        "sha256": "a58d48299f645b87be65051185a832d06cef35cf1cb28569ccdc74e69c5d6ce0"
      }
    }
  ],
  "files": [
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/LICENSES.md",
      "sha256": "1eecd39e2bd19f7a6d5eca8128529dab222080c81d0f6aa0cb48e19a1ea9d2b5",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/brief.json",
      "sha256": "55f728ba03957d5914f9487bb81c33aac3362441672fe85a9b1ce61f4b212ee4",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/brief.md",
      "sha256": "00faea6200c1148f02bf714321bd81dd35b22e586698f61ebe297556d7cd12d0",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/build-config.json",
      "sha256": "2425810ec855d4ce6d60dc346a81eb77331a70dc5f07eb3bd4d9f716e722647b",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/candidate-brief.json",
      "sha256": "4895dc7d110691fd356ee31f8bf23f7b178743043731ac119728290f3755232f",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/candidate-validation-prerights-failed.json",
      "sha256": "639b9e7cc433b686b7422f19a79f3f0abc7b77e7e4a5450bb869bed317096b36",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/candidate-validation.json",
      "sha256": "50434f8a8c1a2ce58feff2780f94ebdd34b942a10e1f26755d783bec29c56985",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/candidate.json",
      "sha256": "cd3a51719b4b5ab7dc5256f037e8e0858b84b2b7eed558395f5cdf40701531ae",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/concept-evidence.json",
      "sha256": "0462e7c5f4c609d520d7995fb5329cc97b9808eda6d21a3d886e84c9151a7f7f",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/concept-generation.json",
      "sha256": "cd8ee9a2c64c6f8c40effef8d4d37042c29e9be157d3fdbac791d9a04b8382dc",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/concept-original.png",
      "sha256": "f9a9a825f359eced65a04ef33a7500b7361e82bfc75928fc830cb1543eb9bfa3",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/concept-prompt.txt",
      "sha256": "deefebedd36cc161fe5e41787bf21a77500f46143952336752be4dc7e791858a",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/concept-validation.json",
      "sha256": "600a90b5c10385b01259fbc930afeaf23de35bb504b1086ce82089c44c9a6cbb",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/contact-sheet.png",
      "sha256": "653c88b48e39e544fa698ec58621ab32576d635247bb8e30c16c81c2bda2e6e6",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/dependency-hashes.json",
      "sha256": "323bc3aafd1e8766d81793a433522a0d92beb78bdd26aa7ddf81beb0f1e52840",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/freeze-path-map.json",
      "sha256": "c74bc7ba076166d889e25b1b3df8089d4feaa54eafaaeb2382d6d6f8580e293a",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/generator.py",
      "sha256": "bcf6fe8f693b83f6e5614d2b0362556f7bde569957c104d1592df03de401b667",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/gltf-validator.report.json",
      "sha256": "0e966d33cde9384cd728d01dab82e50c52da907a5313061200aeec31d1aa457d",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/lifecycle.jsonl",
      "sha256": "28f145049ec09404b6cb6dce6d1233f7bdfa706c1580ee1e91cf54c0c0503c0a",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/maker-review.md",
      "sha256": "033ec7b87a739fa5b3efdcf326c5f624172acee3235648abd797fd5ace026802",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/metrics.json",
      "sha256": "d19d9bb2b9c19073aa2b60d30e43a2f988c054c31ef5cf588cb6da0adca2f963",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/model-start.json",
      "sha256": "2b2839715913521593d11d05c1fc75f29e58760f304f649e1a84cf64d458325b",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/model.glb",
      "sha256": "4b4580c6ed599b80865ebe9a4e506dc3d4a770077fa5f5be3ec099d3ab8a2543",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/modeling-freeze.json",
      "sha256": "a75746bee1a694968a327148103d0fb3a5b21440422ad99cfc20b0940f0c4abd",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/pixel-identity-rights-adapter.json",
      "sha256": "baa56cab878d05bb9212baeb16f601fa023c4c7741d9e6d5e13a89415bc2727f",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/preview.png",
      "sha256": "494fe522c97f1b6ccd30e2fbd1243090b67cccea3b31e769919b24b4d452b78d",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/profile-contract.json",
      "sha256": "c6c7148f5f12bc066e3ab09e2a792ed8531e7e537f2aec8e7bb43d7c5d0daa1a",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/clay.png",
      "sha256": "22bc21d1f79a2a163996f450c4d3337ed86fd35f201ae7d0b4a45b575528a6ae",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/front.png",
      "sha256": "7dae5849ec3ebcee94ce78ef13080a9ca3f4c2e651056fc626fd24fdb17505d8",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/hero.png",
      "sha256": "494fe522c97f1b6ccd30e2fbd1243090b67cccea3b31e769919b24b4d452b78d",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/rear.png",
      "sha256": "5953c32cc403286f2e6494b5be1ca981a57adbe74b93b3841d8e75a5a3532c8f",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/render-config.json",
      "sha256": "9307387d3fa9adb865763d94f28e03ff76c4aa84c183700b4210948a17b72d7d",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/render-manifest.json",
      "sha256": "0dd987aa3ca33777f719037321757dc18308af8f30ce8e77da060f0c6b083db9",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/reversehero.png",
      "sha256": "1b2e4d5cf9dec16fa4abe2f3c70806196c14881f132fb8d1b3fb69468e53f0a0",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/side.png",
      "sha256": "31eb5197579fa325727516141d508c2498142c9675a191cc64eebfd75d259656",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/silhouette.png",
      "sha256": "4f39a4280a354d31962c8b3086932ff850fbd3ec98745db406cfae84b7752910",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/top.png",
      "sha256": "13af7082fb0b6bf515ef8a6a120a42750e496643bc1f2726487be5bc50a1fee5",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-final/turntable.json",
      "sha256": "806de143a0d8f3d073d11e2d11cbe45d9d56d23dadacd8fdda7f488527c5fada",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/clay.png",
      "sha256": "95449a5e5b34101bf4bafb47c4f560d306eb2cc5cc21595e2e6054406f8f9e01",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/front.png",
      "sha256": "dcc2ee2121481834e04becaff332e39e22fda215ab202f5864c7b56521b903b6",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/hero.png",
      "sha256": "8fe63a9a6f2cc4fcee5e965e8b90ea9a391cc479928fabf3b7d76dad4ebe0648",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/rear.png",
      "sha256": "2cd51c2da8ee8ce102e692d48a02b5a51d0932fc7741a742e3bc6007518465bc",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/render-config.json",
      "sha256": "9307387d3fa9adb865763d94f28e03ff76c4aa84c183700b4210948a17b72d7d",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/render-manifest.json",
      "sha256": "5f29d89010af7d2c4638ea240fd0f8e2065702cbf97004b0e870226e975a6b86",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/reversehero.png",
      "sha256": "790f6a02ed85cd25c22de067143bede5450bf86865281c6decaec810870130db",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/side.png",
      "sha256": "1f7e8ce8d5cd31d5e26b6224a5800a6e478bdefa46b1043c0d65f81a8fa097dd",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/silhouette.png",
      "sha256": "69ddce9f8cdd28d80119bbe8a630b82315e22ee7af68b58653385c9a2a86152b",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/top.png",
      "sha256": "3f32b5a6322e1bab69b53c5a5e2e784be11326a1f36798f873cb6eab1b313da0",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof-prerights/turntable.json",
      "sha256": "806de143a0d8f3d073d11e2d11cbe45d9d56d23dadacd8fdda7f488527c5fada",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/clay.png",
      "sha256": "896aac363a8874de956954db050655d7a63e602291a8943e50654b4e39f39b39",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/front.png",
      "sha256": "0eb7fee8e2117fb80c66a9323820af213533cdc0816579ed277447a2c2a61598",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/hero.png",
      "sha256": "7b8de0d5f4b06a5fc193783fdb278d86e0ab6f69953b453849391a459cd8342e",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/rear.png",
      "sha256": "e199eb8064cd103fa0fb80e520c19a0d19c797a94f1a51502b36f3c4c0af88a0",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/render-config.json",
      "sha256": "9307387d3fa9adb865763d94f28e03ff76c4aa84c183700b4210948a17b72d7d",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/render-manifest.json",
      "sha256": "0c36de17715eea124fae257c740d51d23059179234a3dce96aaeea29aa813afc",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/reversehero.png",
      "sha256": "f0f538a16640250f7b2785acbba58acb4408b9e337896e7c72f764208b97e030",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/side.png",
      "sha256": "30b860c485229081bb1c3cf8b8e4b59066f78dfa22ea01402f11eddc39e754e7",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/silhouette.png",
      "sha256": "0a527879d8f62502f6c27fbe985c46ab003e3803dea0c823cb9fb26928ee2a9c",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/top.png",
      "sha256": "9043763a23e2f2b6899f37bf30e18f407a75b7bca26f115b68bf28afa8bf642e",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/proof/turntable.json",
      "sha256": "806de143a0d8f3d073d11e2d11cbe45d9d56d23dadacd8fdda7f488527c5fada",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/qa.json",
      "sha256": "461b90b6c89ba7289449835d7f8fdec4d9cb0bff9b75648b0fa3f7ec827b45e7",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/references-premodel.json",
      "sha256": "9882a20e0de98e490a77aca0ab39bf702e56ce8554b8973bab1a78b9a26f65ca",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/references.json",
      "sha256": "2711d6863316a86f41658a1a5b6160e572c80d173b2ba873e234e310d5d0b7a4",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/repro-bound-1.report.json",
      "sha256": "807fbd1ad8769929692a5b65b5bbd832fad720e2a142b9b81466327c9a41ee0e",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/repro-bound-2.report.json",
      "sha256": "4187eb7a412d788c30427e7ea00bb0ee4b791bd186a8a91186b8fffe5cccf44e",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/repro-final-1.report.json",
      "sha256": "5e383dfdf6b6f34ee4fbba64a487ddcf5206e5b3a70d1b8abf80392940ca37c9",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/repro-final-2.report.json",
      "sha256": "091126cce5eb0f6307b38c423f50b658f6bc0de4406d665ff933d928d0966f8a",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/runtime-parse.report.json",
      "sha256": "0ccda02595480467af69fa1d56f04469c85de63d93d7a517abd1d3f5aa23e01e",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/source-final.report.json",
      "sha256": "b8b7f53a33547911ee1e4ce0129f3071b1f248d712bf365b63cecca0397c895b",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/source-metrics.json",
      "sha256": "4688752d9750b88bcdbeac7ab83a9f959f4856ce397bf2c174bb9395e64ff05a",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/source-vertex-counts.json",
      "sha256": "ec0ae22b47c427026a3fd2b41ca702d216de5cf26bd832504a374416c12ed3c8",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/barchan-dune/r001/source.blend",
      "sha256": "c36cffccdb973aeb20cdab8da46e8991e2734fb4264988a60098820475cf9e9c",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/LICENSES.md",
      "sha256": "1eecd39e2bd19f7a6d5eca8128529dab222080c81d0f6aa0cb48e19a1ea9d2b5",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/brief.json",
      "sha256": "abf73275f4e7d4fdc8f3176e93e7795acddbb0ef4a5301cb27b522ef1b8fad3c",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/brief.md",
      "sha256": "cc1d9a09a90df53e51a24ebb5276606a7ca9e005d138a505a47599fe4bd6520b",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/build-config.json",
      "sha256": "122cdad002098cf19cbce77843a23e03691fdab7b51d3f9ee29de64d862ab8fc",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/candidate-brief.json",
      "sha256": "0d2ee0cd978526b243f687a02f25aa717e38839a407a4e0396ba38497aeb0c8c",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/candidate-validation-prerights-failed.json",
      "sha256": "6322854905facfde2e1568e24ed0644dead9a394e6be18a4481613f56bc42835",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/candidate-validation.json",
      "sha256": "a79d7b560dec1bedb6aa82cc5476f0805c52cd159a3ad2d6f31eb7afc8a0403f",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/candidate.json",
      "sha256": "765c947ae1c33bbee590f3574c34c4a61a7a6aaf2e21123838964b4ff625b3a8",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/concept-evidence.json",
      "sha256": "22f8a04383dc79b6c9b1a033c5433799f49a68390bd6479596a973719077b015",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/concept-generation.json",
      "sha256": "cd8ee9a2c64c6f8c40effef8d4d37042c29e9be157d3fdbac791d9a04b8382dc",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/concept-original.png",
      "sha256": "f9a9a825f359eced65a04ef33a7500b7361e82bfc75928fc830cb1543eb9bfa3",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/concept-prompt.txt",
      "sha256": "deefebedd36cc161fe5e41787bf21a77500f46143952336752be4dc7e791858a",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/concept-validation.json",
      "sha256": "7efbd8309f583e40c6d0e51c35eda74a4ec30f72548aa7932de47b2e1bfc8a42",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/contact-sheet.png",
      "sha256": "1bab3f459791ead76463b9127a38c0988880058233403ffcfc01f90d6dc433ca",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/dependency-hashes.json",
      "sha256": "323bc3aafd1e8766d81793a433522a0d92beb78bdd26aa7ddf81beb0f1e52840",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/freeze-path-map.json",
      "sha256": "d29350a8c3ead91e430ef4b623edc8a2080eb7fc97f4404426692e65f80b9a27",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/generator.py",
      "sha256": "bcf6fe8f693b83f6e5614d2b0362556f7bde569957c104d1592df03de401b667",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/gltf-validator.report.json",
      "sha256": "4a0f63254a618c533f415c54522ec6786a9f6625ddbe5a26005aa6655ca6ce9d",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/lifecycle.jsonl",
      "sha256": "b2b46ad93b744bf2a904c73aafa2b426e7c23cc75203030e61f58b98c08aa9cb",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/maker-review.md",
      "sha256": "8a79c061abba1b77706fea9a2246a109dd16badaa24442abf025c65f58872bbe",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/metrics.json",
      "sha256": "b42413a8ed7ffdc854a48c3de458beb66d5f182894232a027e5b1b8a1013997e",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/model-start.json",
      "sha256": "eea22b7d5b7609388c7f15e4b506269b2fa181881b1d57c3f833167cadab3cc9",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/model.glb",
      "sha256": "005c21c5dfa735762fcfc65387075701ba3e24a915316e6e7c1a59a096362815",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/modeling-freeze.json",
      "sha256": "2735ffbe28af1b16bbef7d294aabf3da31ffe4a7b9412e327b9e970e5b172cb9",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/pixel-identity-rights-adapter.json",
      "sha256": "bcbfc828dfb0d2b07a4edca4e74d2d9eea8133736bdaf0225c35e6ce308fc1f4",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/preview.png",
      "sha256": "7e75660b7127abb53cfaf2f124fe58dfa2736e31942c6df508660052992874d0",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/profile-contract.json",
      "sha256": "8187aee0da9fa84a69ad64e562e8ae4f645dc4e3425d6b1467ab81f98f819f27",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/clay.png",
      "sha256": "f14bc1d569ead6aa9c71fffa50a50055f675e8870af2b7164cd9d1f419fcf651",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/front.png",
      "sha256": "7f68cc06ca68448644a97808d62a3d0a2b8c7040132182942a3919df51a1e6da",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/hero.png",
      "sha256": "7e75660b7127abb53cfaf2f124fe58dfa2736e31942c6df508660052992874d0",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/rear.png",
      "sha256": "7b318ee6bb16ab8b6364ef2366a581b71088b67928196a982078ed8e702ae35f",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/render-config.json",
      "sha256": "99a60462d13f0c8ca52a8dc6d3c66dc0005f89e12ccce4a1321b78bc060a415a",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/render-manifest.json",
      "sha256": "42150cba486a47f5806785d0f345fef3ebfb9a197bf55246677c61f4abff70b0",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/reversehero.png",
      "sha256": "e6ab17b32053ee1da7fc650bd0e346d20cd6a6bf923778422a750ed52cf9f7c5",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/side.png",
      "sha256": "3cc5243ad6f87a69148c1d45cbd0ab2f4fa27f76ae39805c99a215890a0e4e6a",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/silhouette.png",
      "sha256": "a8f7170cee506ef3019a80b377f8513c4f6d31beef83a45985fc223827af19f4",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/top.png",
      "sha256": "2a79dd761897dd26daf9515c3ff813c939c9ddf903fe61c270749f4007dba9d0",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-final/turntable.json",
      "sha256": "6a27670551bad3b3c6d1ca6d19c4f3b7cee4546000dfde888b44b472af525de9",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/clay.png",
      "sha256": "c719382e68761396d7ec77907315afdff26017224644a9ffd150c3a9f8b65447",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/front.png",
      "sha256": "21efc8f409f43be291434bcbb248c2d0cb6fe788fec37052f86a7700a7556d2b",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/hero.png",
      "sha256": "3786387049a31781615066eeff79716bc74eefea7469e8a54570ffd034cac615",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/rear.png",
      "sha256": "b1e62c648ec9ba18eadf8dfc0a37ecf8d8b00f58fc3c3beebc2453a5ddefea98",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/render-config.json",
      "sha256": "99a60462d13f0c8ca52a8dc6d3c66dc0005f89e12ccce4a1321b78bc060a415a",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/render-manifest.json",
      "sha256": "1821ab00a27d749ba7774468512a97f6b4f14e0f9c7aee64d840e9aa2bd1389c",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/reversehero.png",
      "sha256": "bbba7822415fa886c7f4ef048a6439cede9d8835f249e376a0f68b1060ed1d4e",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/side.png",
      "sha256": "4cbfe761694f7ed81ad0091e0e562a2c27ee2b5aebaf69d0be4d4879b2c35226",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/silhouette.png",
      "sha256": "65879cfa3da31e48bac1666552e4c62ab2ecaa2eac07bd26a61a0d23d7057591",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/top.png",
      "sha256": "fab7e26be24ddf353fbd029ad5398ddccc3fa35aa15a6eec4e9384d5fd0d25ee",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof-prerights/turntable.json",
      "sha256": "6a27670551bad3b3c6d1ca6d19c4f3b7cee4546000dfde888b44b472af525de9",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/clay.png",
      "sha256": "eb3f4c0801b1ac31c5be234dd13e1c1f71ded99c9479050ae4a9bb39c997f4bd",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/front.png",
      "sha256": "003a0d820051882fe041ab8cd4d9e974061887d76058e4bf0f5bbb5b17309ef5",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/hero.png",
      "sha256": "252b890617bf6d49538fa5b6fe0b67effe9b8fee5ce5285a1ce112e691c0d49f",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/rear.png",
      "sha256": "6ed1183855f73b197ff9c5f475c7f315dfe430040628afd06f6a6d2a1d6070dc",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/render-config.json",
      "sha256": "99a60462d13f0c8ca52a8dc6d3c66dc0005f89e12ccce4a1321b78bc060a415a",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/render-manifest.json",
      "sha256": "6728fab542b52c487980d219922b582e0f652ea468ecdec1815d15b041cb985e",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/reversehero.png",
      "sha256": "ead78bb806e0b8615e58abfbc136fa6271873e150b8d5c9f313c5fb4e40e3ea0",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/side.png",
      "sha256": "c3f1df5159d8304a38bf7cddb18efbec22cb183a7cf9418313fdec1d24505dc1",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/silhouette.png",
      "sha256": "78c5afbd7eee9daaf536b60a078bb32575f5d433f73486094e2d63655225eb3b",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/top.png",
      "sha256": "b40c5a7da83d2ea3f3c4c8003110e86d0e220f762e583cf925d6844c6d6913e3",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/proof/turntable.json",
      "sha256": "6a27670551bad3b3c6d1ca6d19c4f3b7cee4546000dfde888b44b472af525de9",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/qa.json",
      "sha256": "865820c99fb981ac5233d94129473feed2d94b6f5d7aa6d94160357472b12268",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/references-premodel.json",
      "sha256": "b54438a87dd5d370aa72baa13a0287c99cee0799eb2f6283c0cde5485f7e26bb",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/references.json",
      "sha256": "366bd4f247b7aac8c94073813ab467b8f4924b86fdaf71b0ad4f6421fda073ad",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/repro-bound-1.report.json",
      "sha256": "bbd631ec141656aacc225cb27ed000e22acd276833300c909f9e072c6ec826e4",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/repro-bound-2.report.json",
      "sha256": "d9b332ce78558469753c279513bf970b06d1a6fec8062d2e840794617f6c6c71",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/repro-final-1.report.json",
      "sha256": "729d8be56e7ca25741d0274479d064fda51001f689ac546db953e918fa335a00",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/repro-final-2.report.json",
      "sha256": "412e34ca83f431a4fc2d533f08a006936c4cfdbeddddf29b329194c1603e36fe",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/runtime-parse.report.json",
      "sha256": "985d55425eb89d5c7915c99057581d695e8a5bf61dbd588f6fb7a2497efba0b2",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/source-final.report.json",
      "sha256": "a91cfd528df7f61bd3b837f41a4646cbfbc549fb40bbd873fc42f483f8e5cb50",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/source-metrics.json",
      "sha256": "54d070d8b12b1cee05d4ca688a1f868a55bb9b9b0ce7bb1c8fd0a53fbeeafdf2",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/source-vertex-counts.json",
      "sha256": "3433fbca386cb46aad0c5043b6f04e9e6d050b3610265319847f8b655e306f49",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/calamophyton/r001/source.blend",
      "sha256": "01730a05cce3e638e1fe0305a99f93c25efbbbffb6fc16cb523cc05e08fbc4f9",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/LICENSES.md",
      "sha256": "1eecd39e2bd19f7a6d5eca8128529dab222080c81d0f6aa0cb48e19a1ea9d2b5",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/brief.json",
      "sha256": "86c9eff8908d6cf275f9b656c1bc79165e3962932bf55dcc22844db18028d00e",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/brief.md",
      "sha256": "9bdbe1b6d501dfb9042c95daa8806a2d17f5e4028c6154e738f2b4a09865ea0b",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/build-config.json",
      "sha256": "402866fb029f5fb5c05ad67a8b3098de8c86e6f5fe7e4b80f9c9409649b75d02",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/candidate-brief.json",
      "sha256": "eff771e6df13518527323cbdea9a721f36c575729d85d9ee84b30d66543bc7ba",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/candidate-validation-prerights-failed.json",
      "sha256": "c053eac2d972e47829c7acec866c7e199cfa129c12ad66bc537c79b16c545d8e",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/candidate-validation.json",
      "sha256": "b2c91bae40d461d3e80db671d14060a099b6a5b89715f872528569d68421c98a",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/candidate.json",
      "sha256": "d54f5c4dc2bd9cd26f91af500df540e8eab51df663c1fe176237ac9e8da45101",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/concept-evidence.json",
      "sha256": "8ad30b3d9886148555eca57a1b9c18cf90a2422d5406b854f0d472a426801e61",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/concept-generation.json",
      "sha256": "cd8ee9a2c64c6f8c40effef8d4d37042c29e9be157d3fdbac791d9a04b8382dc",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/concept-original.png",
      "sha256": "f9a9a825f359eced65a04ef33a7500b7361e82bfc75928fc830cb1543eb9bfa3",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/concept-prompt.txt",
      "sha256": "deefebedd36cc161fe5e41787bf21a77500f46143952336752be4dc7e791858a",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/concept-validation.json",
      "sha256": "d209fd1cea6a39c204c48a059134f34774e4ae7d938107bfc2b6794325e1b33b",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/contact-sheet.png",
      "sha256": "fc40e19df173d9d16aefa0af05d392949a0e3be32730573465c3b7688990cd2b",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/dependency-hashes.json",
      "sha256": "323bc3aafd1e8766d81793a433522a0d92beb78bdd26aa7ddf81beb0f1e52840",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/freeze-path-map.json",
      "sha256": "70ab35faab3b34ea6777bfa75de00c9aab37dfbe658ecb47e6ff04734ad8c833",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/generator.py",
      "sha256": "bcf6fe8f693b83f6e5614d2b0362556f7bde569957c104d1592df03de401b667",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/gltf-validator.report.json",
      "sha256": "eee6c0461d375cb9e514f9a24adbd0ccb217626f2a228c742a6352cc1fa73af3",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/lifecycle.jsonl",
      "sha256": "e1e180b49932b0aaaa70acd038f2533fa21a5e46a13977c2a0b5940e93f2b5b3",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/maker-review.md",
      "sha256": "2b3e08f747734121bda91a310f2f6cc1236b18b4b4bf3a0a0de67a4a83481766",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/metrics.json",
      "sha256": "05bce4fd0cb5ad499be332612c66a9807c6635b6332285451256230a317c96f7",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/model-start.json",
      "sha256": "d98238a87d16c00298aee59b8136978f1c7bc11e959657af38f5ec504f481f72",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/model.glb",
      "sha256": "2bdae5b8730c661fe9817df41baa7e12ea5b0f91c78a245f4f13eedffcae640d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/modeling-freeze.json",
      "sha256": "565ab2f106c30a524c37ec884fbbd20d00e0a15170bf08f0beef5b8493d5aa4d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/pixel-identity-rights-adapter.json",
      "sha256": "79e775be7d02810c35880f2d34687f9d37a2de145bf8b6f3f23d41ddba71f15d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/preview.png",
      "sha256": "7baf1703168b07f8928e7c44f29587863f246c343c5b16f20a9ce24c87a715b6",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/profile-contract.json",
      "sha256": "d9b1ffe8181a7cc5f7bcd51cbe817e199767dd03c76e289e25b764cea223d909",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/clay.png",
      "sha256": "1708d2905727e29c87b38a7ac07d428fcfcd954071fe0e92b608800e851f6d25",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/front.png",
      "sha256": "c83125a1c7f1a00aa5905045459966591cd62a59c45e2477b5576fedaaa6519b",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/hero.png",
      "sha256": "7baf1703168b07f8928e7c44f29587863f246c343c5b16f20a9ce24c87a715b6",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/rear.png",
      "sha256": "4cc38174271563b28bc4e0e6ff75d655c8fe7171d0bd6f3ef8a9e70e48e8537e",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/render-config.json",
      "sha256": "d1a2868ba86b7fb431721461c7cb547889eff64a49d08faf42186a20638e57c6",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/render-manifest.json",
      "sha256": "f855477019d11b7f0bf2586d5dd45fab583ac2fe3a6f4cb0b2f2f25352d80b09",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/reversehero.png",
      "sha256": "7654e58f4687a6dd1c01103db3a15971cc2dc0899cd4ea144c9d539ffbb619ab",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/side.png",
      "sha256": "8743cda5458613afc22e24613f4240b91fd74a7f54510807b591d6b273b75f08",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/silhouette.png",
      "sha256": "dabd227510cff787ef5cebd26119e2a564288193efa7be2da959c971e306246c",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/top.png",
      "sha256": "f5b1a75e8ba5c54646224179b0739cd31b21b308e68c8120c24469766ae55fba",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-final/turntable.json",
      "sha256": "77235cfd215e265b2630c4b8d3a186ebe072111705717131f7c5db95167ffa6f",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/clay.png",
      "sha256": "b179906e09c3c6fb5f030c660abc255ba40aa213fc8c1d8efa32be02e0de629d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/front.png",
      "sha256": "f89c5c4adcd26963b733b21eb55fe7884c3fa2872dbd5f6bb0fd599008a47fbd",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/hero.png",
      "sha256": "00ce4e34cd57f8dfcbf2254433f6c40dadb1b6f1dade2f763d1a56d6a9211770",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/rear.png",
      "sha256": "0ccafe4113c29bfa246d386fa74b5b4823470eeed68e54181b755cd307556e81",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/render-config.json",
      "sha256": "d1a2868ba86b7fb431721461c7cb547889eff64a49d08faf42186a20638e57c6",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/render-manifest.json",
      "sha256": "231087f276bf93b4e7f6eb6c121bb82e27f3d2740497faf946328e0a3846287e",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/reversehero.png",
      "sha256": "aeac376a59a547cc94b3a7b827a2af9c18e1af3c2dc7db734a9f643274a20bd1",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/side.png",
      "sha256": "091d09376a1b9ce9e370b7b0837aa12a9949adebb7199efaee8ff439aabd89aa",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/silhouette.png",
      "sha256": "dded08d43b3d21e11314e188e377cd666a8b9933d463cfa56772150602e6c984",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/top.png",
      "sha256": "14528a49ac59f159ab34f4a662d3f4d513bad6b468c5d4d0a7312256c929ba4d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof-prerights/turntable.json",
      "sha256": "77235cfd215e265b2630c4b8d3a186ebe072111705717131f7c5db95167ffa6f",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/clay.png",
      "sha256": "e1e29a9e3049c3b36e919df0b01d7af6a2ac51d6c48273079877edf2a586a7d5",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/front.png",
      "sha256": "6595a86b71058e963974edc716e11898af2d2e58a18f682f51c2e12a908315af",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/hero.png",
      "sha256": "6dc5468303786ba1f1fd8cc2bd8d801c63ed090e7f69f90e8ff3647cb5057ea1",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/rear.png",
      "sha256": "b91b4abfa0b2d741a757b1f653a281a89259d54540452fae8591b48c340ed9a8",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/render-config.json",
      "sha256": "d1a2868ba86b7fb431721461c7cb547889eff64a49d08faf42186a20638e57c6",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/render-manifest.json",
      "sha256": "b36f92dfa65bc05243efee0d729539694ed6623b180ac2c6dc215daf1c61db69",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/reversehero.png",
      "sha256": "cc1faf7d234ddfd470f620545f3c6aa0418bf98e4899d2629bf04d9fa52dadee",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/side.png",
      "sha256": "45c3e236caba852a241d2c59fa38068181d877a6ee4f695b0a9533d3d9fe8410",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/silhouette.png",
      "sha256": "1338235833ab9743e2df4973f8599096bfebe871036e1b64be3b601b3631df04",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/top.png",
      "sha256": "d375807f6f4234bf6409d0e06de5110629e03a1b7a720fedc493fa3d73a8929c",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/proof/turntable.json",
      "sha256": "77235cfd215e265b2630c4b8d3a186ebe072111705717131f7c5db95167ffa6f",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/qa.json",
      "sha256": "1b532e56011b8be60cc089623db5ae40023f349474e57cbf620e267941cf1893",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/references-premodel.json",
      "sha256": "8667c21cf1127cbd93719cf9ea1fcd49bd5e59dde412abb682d705904389774d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/references.json",
      "sha256": "b5008bb387b011678c61fa23fd51ee1f51e1a1c55e1827dac038872c16bf91e2",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/repro-bound-1.report.json",
      "sha256": "aeeb53b5d86e0efdad0d0855583d8c7dcb733d6486630ad33a3c2d6d87d519cf",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/repro-bound-2.report.json",
      "sha256": "73b930a68bedddb7c071ca88a3e9ed76f029b4998fe82913b0acbda7cf9aa432",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/repro-final-1.report.json",
      "sha256": "3eecf3518bbcbdbc3146659fbe222efe00077c2439059255f8c22ac5d592dc5d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/repro-final-2.report.json",
      "sha256": "901fb26395b8a7b99ad4b54e7a5830e2d428c5b78d95d03701936e4c50b84e22",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/runtime-parse.report.json",
      "sha256": "a3dd5e485e341a650467ffa35a0c370b38f8077e5c351f084dede7360d266abf",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/source-final.report.json",
      "sha256": "4dbb205b73ee31f44489bbdfcd338a8f04c7fad2d50107048d0f903dc570e9e2",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/source-metrics.json",
      "sha256": "c7dbba53835156cab725069646f266549712c550276dc6c001d241fde8075ebc",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/source-vertex-counts.json",
      "sha256": "56a444b132e49d33387df3e4eec5b0afbe35363a10bc07120aef59a46f632316",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/current-ripple-surface/r001/source.blend",
      "sha256": "873e86fcba5a02e53395bf963cd863e67d49dc221c93d3beb93a718878b8758f",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/LICENSES.md",
      "sha256": "1eecd39e2bd19f7a6d5eca8128529dab222080c81d0f6aa0cb48e19a1ea9d2b5",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/brief.json",
      "sha256": "7ad2fe63a0a6e3c0a97149c338b27b2aea81f0a024a40ba088a52ba71782984e",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/brief.md",
      "sha256": "eae6821d5d702c05df6a89f09e7e32236603609a8211358fafce21387dbf9d39",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/build-config.json",
      "sha256": "e31ea080a957d10f099c3dcb8f9f05d59c1d9e34fcdc7ed753cbbfd62ccda107",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/candidate-brief.json",
      "sha256": "562f7435555aa51844db611e61923008bdf5572f8fb0420385be2992fa64655c",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/candidate-validation-prerights-failed.json",
      "sha256": "dedc564aebd189c42ea0b51ae52f1db026f81083ae47a8710289450fe4336962",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/candidate-validation.json",
      "sha256": "e3c78ee23466ac362ee9f46aa6bd8a50c3dbea5ab7e99666e0257533c2339f59",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/candidate.json",
      "sha256": "3e14024b74f08d4f5a459de54e7b25eb43dc482310abeadf780fd0c821d39d1e",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/concept-evidence.json",
      "sha256": "23f509547ab2327f652450a7a0f803597d094b2965aa50fb48ebd0f012d9d883",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/concept-generation.json",
      "sha256": "e1f59d2b28030f76d793d5af3ec0af5224fe33d7adc60791abc806e52111b02a",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/concept-original.png",
      "sha256": "2404e7259c082d931d34cbc1e61b0ba18291e6b69006b92dd52c99742cafbda9",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/concept-prompt.txt",
      "sha256": "ae5d759951985ecff66b1b6d038067441de2302076b871fb0cbcc0e8ed7ea508",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/concept-validation.json",
      "sha256": "b42c759c41b1da09dc9430364c7150e93a71c230bd84a41d36d640d137cd2e8d",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/contact-sheet.png",
      "sha256": "9342efd6265d89d660fd0c677e0b2bab552e471a4fb4d4e693478c3903c12e72",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/dependency-hashes.json",
      "sha256": "323bc3aafd1e8766d81793a433522a0d92beb78bdd26aa7ddf81beb0f1e52840",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/freeze-path-map.json",
      "sha256": "a2ab2c8015c5673fea46318679512b2d129eb953adcf2475c726565fee344f51",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/generator.py",
      "sha256": "1036fb570efd95df8f779014f629951d1bc7aae124571d279fbd370a51ed69d8",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/gltf-validator.report.json",
      "sha256": "19d15b0ec50c7e5e3d7f813295155502e8cf957fe2e2ba96b58757eec4e94e83",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/lifecycle.jsonl",
      "sha256": "5d26535759e9ac307ae4c42a957b941f2bd85d53fc1694dbfce0e0e099243d8a",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/maker-review.md",
      "sha256": "e0c10c2d9ad9edec13ecc950a903e81db38d1624fb633d072fa62dbe00673b10",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/metrics.json",
      "sha256": "eadd5ed3c6636308be2ecb54ece5a0480442c59b8eda41b6948403f3bf20076a",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/model.glb",
      "sha256": "ec95315cac17288508b02d7f3901e9a6a8e8ef464e46b44f460bba049488d35c",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/modeling-freeze.json",
      "sha256": "b4b65833327550dc9615f2e8a81144bf06277db52537aec49cabc38042db7ec4",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/pixel-identity-rights-adapter.json",
      "sha256": "db29fd8d5f7291ff79e22cb4167963819bf05f9a8721d3c3038cc4d962f255a0",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/preview.png",
      "sha256": "bf45865550853c3e9173e03ee608b40293f9ad34eb1e85fd2be170d6869b1389",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/profile-contract.json",
      "sha256": "310c57088b49c598738c44718e5cb956f358eecd462162a4ea051eb240bf557f",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/clay.png",
      "sha256": "bf6a5338f0f7fb8e08bc46b7b85a9b65e6caebc5d7c68b7ea85ae54814fb482f",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/front.png",
      "sha256": "bfdb2513824b7befe3277c6dd44f28c1d5a5f8a34943e00c39a46933c6ab9ed7",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/hero.png",
      "sha256": "bf45865550853c3e9173e03ee608b40293f9ad34eb1e85fd2be170d6869b1389",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/rear.png",
      "sha256": "51f2f1ebbad0553be5992eac59247e577a9871e2c40f06c57093f955be9b0626",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/render-config.json",
      "sha256": "54488017e65fbe3a1c1faeb2eabf62880ca66f7ed862f5f8fef928c290ddf664",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/render-manifest.json",
      "sha256": "8de34dfdb60f99dfe273072476ca00b6d41991fa5ef53a4e314db3dfbb845f7a",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/reversehero.png",
      "sha256": "d51c72ab62f54e9bd50ce41605b980bef7677bcd16d7a8fb47f22478cf720393",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/side.png",
      "sha256": "78e3aa7a1c2167fb8a277d91c332af45c39ec0cbfeeba9ea2e4af9c1a20182ea",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/silhouette.png",
      "sha256": "f368f71c2bda0d692ed141cf0e1dc64f504efacd949c3f64af3b89dcd052c0fd",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/top.png",
      "sha256": "5e6ad969543f75135322c300c528bfdcde79d06cf6f1acc4bf6502b06d272cf1",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-final/turntable.json",
      "sha256": "feb46ef3e94b264c33f16fcde3517611302e9ea1508d42f357a43d2b7b0d56e4",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/clay.png",
      "sha256": "2fea659d764e3aec71529b0302d325561b13dc2861554f77b75c8e653358b496",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/front.png",
      "sha256": "e32be118437401777f4772f9d7f32e8750e5804a3c3f864345616e9200c0c27e",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/hero.png",
      "sha256": "009d2856c78e6b67800ef9092e53f05d07fbf0c62c3de286042599e47c98a752",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/rear.png",
      "sha256": "8c341c5780bcad24fcb7898e0dace147ed3964e9aea81ffd1cb983cc38110e77",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/render-config.json",
      "sha256": "54488017e65fbe3a1c1faeb2eabf62880ca66f7ed862f5f8fef928c290ddf664",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/render-manifest.json",
      "sha256": "95e38301fb8fafaa55e37233e248a47457d30c391b7321402d4bd5696a9c80b7",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/reversehero.png",
      "sha256": "4b1d4a37a2b8c815d691e3291ce4a6fe9863b06441cd013ad1b5a2221ddfa3a9",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/side.png",
      "sha256": "56f38a7eeeeaddb1f9cde0569c46fed665c69b845e69a550004162648ef18926",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/silhouette.png",
      "sha256": "3a5e964d5b5cc2ebc8d07fcd5d5c7b100a9f4242f939414ba3797e1494546236",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/top.png",
      "sha256": "d905d56c26d967057272142f2cd8d0d94deca19ba6100b423398feab3242ccad",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof-prerights/turntable.json",
      "sha256": "feb46ef3e94b264c33f16fcde3517611302e9ea1508d42f357a43d2b7b0d56e4",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/clay.png",
      "sha256": "cddff110fa4b78de756bf9010241d2d4db6d9874890812df6695c066ba910873",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/front.png",
      "sha256": "92b649d6f68cd67b8e08dcb896ec01c127b7bdae94d140e6e8eeb9fe2adac63a",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/hero.png",
      "sha256": "6d693919bdc18c9a666feffe66406dca27630103ec6757876ca3f9eba6a1f7d5",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/rear.png",
      "sha256": "8428cba8bd11b13fee6e7c1efef19217b0af39164e937228820e51ee591c3a74",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/render-config.json",
      "sha256": "54488017e65fbe3a1c1faeb2eabf62880ca66f7ed862f5f8fef928c290ddf664",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/render-manifest.json",
      "sha256": "ca69682685c7b4178cfbf7253a0f9a4208905ab938a8c515bd5c634de22b5050",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/reversehero.png",
      "sha256": "689e3c1148b2c39473bf97da49e5af787d80a2ac38cc439d5b80d70f877a11c2",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/side.png",
      "sha256": "81eb5c53701c01780160380bba5121f62fa79bb1ed950a4f08ca9bf7d86168a5",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/silhouette.png",
      "sha256": "76c418bc7a7c2799796a9d2057f05c463a11d308f8f5c66ddd6b095f9ff96112",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/top.png",
      "sha256": "174c7620c0196d2b25ba1df850e518a3004713a0b625879541e013dc987721b8",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/proof/turntable.json",
      "sha256": "feb46ef3e94b264c33f16fcde3517611302e9ea1508d42f357a43d2b7b0d56e4",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/qa.json",
      "sha256": "35ae7390483a4802deb5216d0cd6343dcacd6e2e44792d69424c3ac15c3bcffd",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/references-premodel.json",
      "sha256": "d7cef507ef0fa46654a3f871f3b2e37ee6f639f08be7832857990a76d277624f",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/references.json",
      "sha256": "0371d0379eeec1cbd63987a002f134d509d9722253045c8e341d3e5bc756ab45",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/repro-final-1.report.json",
      "sha256": "2eb0b047cc6fcfcfa371e0012d7caff6fa75090e2a764e56bbbc4671f8b6937d",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/repro-final-2.report.json",
      "sha256": "1fdb28613118e295ac92164effbec9ae756cae9c94fb261564bad1595b46b0cc",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/runtime-parse.report.json",
      "sha256": "10011e7a025b712ceb95d1d74d566130c8ae74a00fedd9b122f25287ef884352",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/source-final.report.json",
      "sha256": "fea6bc7a2f01079e798761392319538fc22d44c03ccbe09bb89a689b57585f7b",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/source-metrics.json",
      "sha256": "cf559d5badf0709a52eb9cab0a540724a1af755da87b28d4639026dfebb10a45",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/source-vertex-counts.json",
      "sha256": "22334a3d32ebcefc39aad222a69663c98df4da17b972de3fe21ae1973320d4dd",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-58/perspicaris/r002/source.blend",
      "sha256": "d9fdfe3fcef95cd75649c3908cb685ce547dd0b2d36f2093805d12d2afeb0804",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/HANDOFF.md",
      "sha256": "6f23a3cbee94bb2f3d2dd23ce84936c98379b0bbb918354f5320138667a841e5",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/KNOWN-LIMITS.md",
      "sha256": "3d40157d7da584b166dc4544d53d620c4f8435fd36738a2943f26f728b50194c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/claim.json",
      "sha256": "fb89089e99147609009c2697d8f34534d7597f448d189a60a946b16e2156a2e2",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-1/4848b9fece4b46164f9e8f9e79c8de4f90a0e204bad69b72a4d8a34561707204/20261020T072427-a7e3ed1dcc1c4cdb816674e548f7e95a/outputs/metrics.json",
      "sha256": "6a599f8dad1ff721482853e3f43680d9d1c0f63d72a6924f8a2cdb5427a60916",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-1/4848b9fece4b46164f9e8f9e79c8de4f90a0e204bad69b72a4d8a34561707204/20261020T072427-a7e3ed1dcc1c4cdb816674e548f7e95a/outputs/model.glb",
      "sha256": "4b4580c6ed599b80865ebe9a4e506dc3d4a770077fa5f5be3ec099d3ab8a2543",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-1/4848b9fece4b46164f9e8f9e79c8de4f90a0e204bad69b72a4d8a34561707204/20261020T072427-a7e3ed1dcc1c4cdb816674e548f7e95a/outputs/source-metrics.json",
      "sha256": "4688752d9750b88bcdbeac7ab83a9f959f4856ce397bf2c174bb9395e64ff05a",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-1/4848b9fece4b46164f9e8f9e79c8de4f90a0e204bad69b72a4d8a34561707204/20261020T072427-a7e3ed1dcc1c4cdb816674e548f7e95a/outputs/source.blend",
      "sha256": "49dc2e3a436fc30bf54bf30f1f7f84f5809f9b99168a3c3e95bebdee5ef6ff35",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-1/4848b9fece4b46164f9e8f9e79c8de4f90a0e204bad69b72a4d8a34561707204/20261020T072427-a7e3ed1dcc1c4cdb816674e548f7e95a/request.json",
      "sha256": "b4815c9b2b439c0f78d06f04b262904e9e13ec74164c1118e012e59e0ade5997",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-1/4848b9fece4b46164f9e8f9e79c8de4f90a0e204bad69b72a4d8a34561707204/20261020T072427-a7e3ed1dcc1c4cdb816674e548f7e95a/result.json",
      "sha256": "4231a66224b0fda0759cde70bfd1ba5fcc142f9a8c6639a3ed34899710065548",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-2/adb0297019c426932ebeee4077c60b08dd723a798ecc53c81d209e973b0411bc/20261020T072430-09528ededbf6411a81878b307400f904/outputs/metrics.json",
      "sha256": "d9a1ca6d66e3068d4c8bc3c7f949fd09baa3ad3fd852e414bd9937444b5d01aa",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-2/adb0297019c426932ebeee4077c60b08dd723a798ecc53c81d209e973b0411bc/20261020T072430-09528ededbf6411a81878b307400f904/outputs/model.glb",
      "sha256": "4b4580c6ed599b80865ebe9a4e506dc3d4a770077fa5f5be3ec099d3ab8a2543",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-2/adb0297019c426932ebeee4077c60b08dd723a798ecc53c81d209e973b0411bc/20261020T072430-09528ededbf6411a81878b307400f904/outputs/source-metrics.json",
      "sha256": "4688752d9750b88bcdbeac7ab83a9f959f4856ce397bf2c174bb9395e64ff05a",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-2/adb0297019c426932ebeee4077c60b08dd723a798ecc53c81d209e973b0411bc/20261020T072430-09528ededbf6411a81878b307400f904/outputs/source.blend",
      "sha256": "3577bf8964967756d3ad73fc90c0d352a865703e3cf477802c99fd6ac205962b",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-2/adb0297019c426932ebeee4077c60b08dd723a798ecc53c81d209e973b0411bc/20261020T072430-09528ededbf6411a81878b307400f904/request.json",
      "sha256": "83dedd204bc79b790985cfa45e73ba7197660d3b14abdc5e3510ce88468d8979",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/barchan-dune/r001/semantic-rebuild-2/adb0297019c426932ebeee4077c60b08dd723a798ecc53c81d209e973b0411bc/20261020T072430-09528ededbf6411a81878b307400f904/result.json",
      "sha256": "ee82c56daa47bc8e6714e2c8ae4a107375680aff883bdd738fc66424d76182fc",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-1/49c4cfe7e2721861644ebb7525bda5fcb1beb6c816703122849b0884792cd5ca/20261020T072408-80e39771311d4a089d655b8689421330/outputs/metrics.json",
      "sha256": "012916de780a680a8c553097ec063203d8855063b64f46a458b60742ae73da0f",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-1/49c4cfe7e2721861644ebb7525bda5fcb1beb6c816703122849b0884792cd5ca/20261020T072408-80e39771311d4a089d655b8689421330/outputs/model.glb",
      "sha256": "005c21c5dfa735762fcfc65387075701ba3e24a915316e6e7c1a59a096362815",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-1/49c4cfe7e2721861644ebb7525bda5fcb1beb6c816703122849b0884792cd5ca/20261020T072408-80e39771311d4a089d655b8689421330/outputs/source-metrics.json",
      "sha256": "54d070d8b12b1cee05d4ca688a1f868a55bb9b9b0ce7bb1c8fd0a53fbeeafdf2",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-1/49c4cfe7e2721861644ebb7525bda5fcb1beb6c816703122849b0884792cd5ca/20261020T072408-80e39771311d4a089d655b8689421330/outputs/source.blend",
      "sha256": "7320890a02dfd52d0f5076074f4dbe776f360bd7cda7bb0d2fe0616fdea8461a",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-1/49c4cfe7e2721861644ebb7525bda5fcb1beb6c816703122849b0884792cd5ca/20261020T072408-80e39771311d4a089d655b8689421330/request.json",
      "sha256": "b9c1094685bf360cdeed731eb1c5d73e17555485946224ad1b753efd5eb05b71",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-1/49c4cfe7e2721861644ebb7525bda5fcb1beb6c816703122849b0884792cd5ca/20261020T072408-80e39771311d4a089d655b8689421330/result.json",
      "sha256": "afb8517f1710105cd457f70e3fa6f8907fa53206269d364d2b617c64780af491",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-2/8483c29e462ba443106a768490caeb7906f20ae267aa81ae895d11e72f8f7582/20261020T072415-4dbe6ae12da342ff97967889e2c549c7/outputs/metrics.json",
      "sha256": "82de974009d5a38b9c2fcc2601edad8978ac76ad9c73468227afe2932c45afa0",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-2/8483c29e462ba443106a768490caeb7906f20ae267aa81ae895d11e72f8f7582/20261020T072415-4dbe6ae12da342ff97967889e2c549c7/outputs/model.glb",
      "sha256": "005c21c5dfa735762fcfc65387075701ba3e24a915316e6e7c1a59a096362815",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-2/8483c29e462ba443106a768490caeb7906f20ae267aa81ae895d11e72f8f7582/20261020T072415-4dbe6ae12da342ff97967889e2c549c7/outputs/source-metrics.json",
      "sha256": "54d070d8b12b1cee05d4ca688a1f868a55bb9b9b0ce7bb1c8fd0a53fbeeafdf2",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-2/8483c29e462ba443106a768490caeb7906f20ae267aa81ae895d11e72f8f7582/20261020T072415-4dbe6ae12da342ff97967889e2c549c7/outputs/source.blend",
      "sha256": "2a4de4315c2e928d6723a9f1afbabf9398c2f82ad2dcca220ec2bd9867578b1a",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-2/8483c29e462ba443106a768490caeb7906f20ae267aa81ae895d11e72f8f7582/20261020T072415-4dbe6ae12da342ff97967889e2c549c7/request.json",
      "sha256": "2656be1504a99f85477109a2e4f72830cf8a3f56df86cda195995a3b822a3a44",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/calamophyton/r001/semantic-rebuild-2/8483c29e462ba443106a768490caeb7906f20ae267aa81ae895d11e72f8f7582/20261020T072415-4dbe6ae12da342ff97967889e2c549c7/result.json",
      "sha256": "4e96b78b7e71b2c1bf3f31963a81a9268942e8315528bec3f771276667c1a497",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-1/0b2684055a9e009164d49d8c4f9dda669b90d76e6fba2f7fa9098520dea50856/20261020T072432-53ebe546fc7d49f69d94571843aaebd4/outputs/metrics.json",
      "sha256": "4ae3b8a18e74ffe59bb60f52f498ac04a2416fcd8123d98450374e4e3638dcfa",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-1/0b2684055a9e009164d49d8c4f9dda669b90d76e6fba2f7fa9098520dea50856/20261020T072432-53ebe546fc7d49f69d94571843aaebd4/outputs/model.glb",
      "sha256": "2bdae5b8730c661fe9817df41baa7e12ea5b0f91c78a245f4f13eedffcae640d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-1/0b2684055a9e009164d49d8c4f9dda669b90d76e6fba2f7fa9098520dea50856/20261020T072432-53ebe546fc7d49f69d94571843aaebd4/outputs/source-metrics.json",
      "sha256": "c7dbba53835156cab725069646f266549712c550276dc6c001d241fde8075ebc",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-1/0b2684055a9e009164d49d8c4f9dda669b90d76e6fba2f7fa9098520dea50856/20261020T072432-53ebe546fc7d49f69d94571843aaebd4/outputs/source.blend",
      "sha256": "6017f37e393c0357e8b23f776fa2cc3b72edcbf269241fbd07a49201c1f4637c",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-1/0b2684055a9e009164d49d8c4f9dda669b90d76e6fba2f7fa9098520dea50856/20261020T072432-53ebe546fc7d49f69d94571843aaebd4/request.json",
      "sha256": "7ad9d554bb1a68a07007a38cdc4e9105fc6f6778adbf8f6ada1a73c7cc1e3185",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-1/0b2684055a9e009164d49d8c4f9dda669b90d76e6fba2f7fa9098520dea50856/20261020T072432-53ebe546fc7d49f69d94571843aaebd4/result.json",
      "sha256": "e1d1c873d891286be676b69776ae946368d874a230187e927a2223c0c8b69930",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-2/1747c1a6e68d0ff38e7a36c99f03ef09f6e82d6aaea8d7a60052dae363effef5/20261020T072436-bce0c2ae0ae340dda3cbf123f35b9b89/outputs/metrics.json",
      "sha256": "656dfc5a3752f9c02365db4ec97d45aee7bbab4a933886ce05bbed73fa6d3552",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-2/1747c1a6e68d0ff38e7a36c99f03ef09f6e82d6aaea8d7a60052dae363effef5/20261020T072436-bce0c2ae0ae340dda3cbf123f35b9b89/outputs/model.glb",
      "sha256": "2bdae5b8730c661fe9817df41baa7e12ea5b0f91c78a245f4f13eedffcae640d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-2/1747c1a6e68d0ff38e7a36c99f03ef09f6e82d6aaea8d7a60052dae363effef5/20261020T072436-bce0c2ae0ae340dda3cbf123f35b9b89/outputs/source-metrics.json",
      "sha256": "c7dbba53835156cab725069646f266549712c550276dc6c001d241fde8075ebc",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-2/1747c1a6e68d0ff38e7a36c99f03ef09f6e82d6aaea8d7a60052dae363effef5/20261020T072436-bce0c2ae0ae340dda3cbf123f35b9b89/outputs/source.blend",
      "sha256": "930c64977baf6f81342989913087d57c08dd2891e087b0f3a609180dedfc69bd",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-2/1747c1a6e68d0ff38e7a36c99f03ef09f6e82d6aaea8d7a60052dae363effef5/20261020T072436-bce0c2ae0ae340dda3cbf123f35b9b89/request.json",
      "sha256": "41bd4df6979446e47d4923c78a95050595e1392fe0fcaaa68032a97393f5b639",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-2/1747c1a6e68d0ff38e7a36c99f03ef09f6e82d6aaea8d7a60052dae363effef5/20261020T072436-bce0c2ae0ae340dda3cbf123f35b9b89/result.json",
      "sha256": "2594945e270d78491b4452e6c264cca7882aab6214aefff26e233db9a48a14cc",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-1/e44e0399be29f0c972ff787ff3bce238d9bcaf9fec0fd01cbc12fd1022f4c501/20261020T072418-1e16c5e09a484d74b38dacd4d9ae60a9/outputs/metrics.json",
      "sha256": "39d544dde7e4ab54eea0c6067a514e227a0c49caae9d97a40c6bb14bf7320eb9",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-1/e44e0399be29f0c972ff787ff3bce238d9bcaf9fec0fd01cbc12fd1022f4c501/20261020T072418-1e16c5e09a484d74b38dacd4d9ae60a9/outputs/model.glb",
      "sha256": "ec95315cac17288508b02d7f3901e9a6a8e8ef464e46b44f460bba049488d35c",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-1/e44e0399be29f0c972ff787ff3bce238d9bcaf9fec0fd01cbc12fd1022f4c501/20261020T072418-1e16c5e09a484d74b38dacd4d9ae60a9/outputs/source-metrics.json",
      "sha256": "cf559d5badf0709a52eb9cab0a540724a1af755da87b28d4639026dfebb10a45",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-1/e44e0399be29f0c972ff787ff3bce238d9bcaf9fec0fd01cbc12fd1022f4c501/20261020T072418-1e16c5e09a484d74b38dacd4d9ae60a9/outputs/source.blend",
      "sha256": "6f7ea514ebf7857e5de80e9691fb080402c004846dbb4ba12eef1ea34b8a0c85",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-1/e44e0399be29f0c972ff787ff3bce238d9bcaf9fec0fd01cbc12fd1022f4c501/20261020T072418-1e16c5e09a484d74b38dacd4d9ae60a9/request.json",
      "sha256": "5031c8b33a83241f1688c46264e213adaf27a330d8113c9015527fa73910c327",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-1/e44e0399be29f0c972ff787ff3bce238d9bcaf9fec0fd01cbc12fd1022f4c501/20261020T072418-1e16c5e09a484d74b38dacd4d9ae60a9/result.json",
      "sha256": "b9fbf768c68a28e17bae7205b5b705b0ae00fd2268b8f4772972123a5309ae97",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-2/3d6be71be4656132f22cfec16856ebfd34e9ec8f68f71a0c5a5e08c864d262f9/20261020T072423-331fa819fbaa441581f6839d50f2478d/outputs/metrics.json",
      "sha256": "9360fbdd47e0eaaf1b5e65671548923a979f4ea93e603315c9fc75c3399ff7d1",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-2/3d6be71be4656132f22cfec16856ebfd34e9ec8f68f71a0c5a5e08c864d262f9/20261020T072423-331fa819fbaa441581f6839d50f2478d/outputs/model.glb",
      "sha256": "ec95315cac17288508b02d7f3901e9a6a8e8ef464e46b44f460bba049488d35c",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-2/3d6be71be4656132f22cfec16856ebfd34e9ec8f68f71a0c5a5e08c864d262f9/20261020T072423-331fa819fbaa441581f6839d50f2478d/outputs/source-metrics.json",
      "sha256": "cf559d5badf0709a52eb9cab0a540724a1af755da87b28d4639026dfebb10a45",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-2/3d6be71be4656132f22cfec16856ebfd34e9ec8f68f71a0c5a5e08c864d262f9/20261020T072423-331fa819fbaa441581f6839d50f2478d/outputs/source.blend",
      "sha256": "8612db2f208253639b60ede05a92972954b362a1305f1d614b0163cc0ebb3ab7",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-2/3d6be71be4656132f22cfec16856ebfd34e9ec8f68f71a0c5a5e08c864d262f9/20261020T072423-331fa819fbaa441581f6839d50f2478d/request.json",
      "sha256": "15a9415a40bf7d7216dd255804845eb0e14d7cbb59417fdd154905ac7ca7a04f",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/build/perspicaris/r002/semantic-rebuild-2/3d6be71be4656132f22cfec16856ebfd34e9ec8f68f71a0c5a5e08c864d262f9/20261020T072423-331fa819fbaa441581f6839d50f2478d/result.json",
      "sha256": "e03cd48f6b84e14b884319dbea620d26abeb1e053347bb55cc66de99a642dde6",
      "origin": "source",
      "owner": "perspicaris"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/runs/20261020T072406-3951f394886547eeb506fdd99ee61799/manifest.json",
      "sha256": "6ffc74e6edb33156e3b7cc7e7ee07e5dc2411720e2e300e32c61f96cf743c084",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-rebuild-runs/runs/20261020T072406-3951f394886547eeb506fdd99ee61799/summary.json",
      "sha256": "0088163543cfdc2d19092da9d50281ae006bb47da32dfbd4df8127ac8959d19a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/final-selection.json",
      "sha256": "2dfb0c9958af3d5c4ab9e207bd259785601eedcfcf4e9b4a942ed86504deb77c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/handoff.json",
      "sha256": "001fe0258696cc0bf3faef640173d62bd261b9609e56ca2fc492e24c687df393",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-jobs.json",
      "sha256": "a85c96036d1567251590aed5d4fbd2a97ff89773fabe98ca6ab2c37875a19036",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/barchan-dune/r001/semantic-rebuild-1/4848b9fece4b46164f9e8f9e79c8de4f90a0e204bad69b72a4d8a34561707204/20261020T072250-1a4b51cdad6941b8bc616b5b7d014763/outputs/model.glb",
      "sha256": "4b4580c6ed599b80865ebe9a4e506dc3d4a770077fa5f5be3ec099d3ab8a2543",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/barchan-dune/r001/semantic-rebuild-1/4848b9fece4b46164f9e8f9e79c8de4f90a0e204bad69b72a4d8a34561707204/20261020T072250-1a4b51cdad6941b8bc616b5b7d014763/request.json",
      "sha256": "62b65b09b713a8d8bdb038f23b5c43beb31fbb919261b964856b7f3070fbc319",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/barchan-dune/r001/semantic-rebuild-1/4848b9fece4b46164f9e8f9e79c8de4f90a0e204bad69b72a4d8a34561707204/20261020T072250-1a4b51cdad6941b8bc616b5b7d014763/result.json",
      "sha256": "f3ca0a5437317d7d88330bd75edb4900c6b721cdd1f244e8bef61a1939ebc63a",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/barchan-dune/r001/semantic-rebuild-2/adb0297019c426932ebeee4077c60b08dd723a798ecc53c81d209e973b0411bc/20261020T072254-4dbfc846cd73461da527e84cad96b72a/outputs/model.glb",
      "sha256": "4b4580c6ed599b80865ebe9a4e506dc3d4a770077fa5f5be3ec099d3ab8a2543",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/barchan-dune/r001/semantic-rebuild-2/adb0297019c426932ebeee4077c60b08dd723a798ecc53c81d209e973b0411bc/20261020T072254-4dbfc846cd73461da527e84cad96b72a/request.json",
      "sha256": "9fcaea6062fd3e4d6afcfac66f94a41f534acb4d84097e7615de42aa7aebf637",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/barchan-dune/r001/semantic-rebuild-2/adb0297019c426932ebeee4077c60b08dd723a798ecc53c81d209e973b0411bc/20261020T072254-4dbfc846cd73461da527e84cad96b72a/result.json",
      "sha256": "90d142e424701e9f9358958d0ca34e580db51b881be4a7bfdc27682d52779b05",
      "origin": "source",
      "owner": "barchan-dune"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/calamophyton/r001/semantic-rebuild-1/49c4cfe7e2721861644ebb7525bda5fcb1beb6c816703122849b0884792cd5ca/20261020T072236-94ce262d0292490ba02c26e110385249/outputs/model.glb",
      "sha256": "005c21c5dfa735762fcfc65387075701ba3e24a915316e6e7c1a59a096362815",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/calamophyton/r001/semantic-rebuild-1/49c4cfe7e2721861644ebb7525bda5fcb1beb6c816703122849b0884792cd5ca/20261020T072236-94ce262d0292490ba02c26e110385249/request.json",
      "sha256": "dbf5baf944cadd03bfb3a60ecf74efc7c3b8d6bc320b97038dec06e98e0cd052",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/calamophyton/r001/semantic-rebuild-1/49c4cfe7e2721861644ebb7525bda5fcb1beb6c816703122849b0884792cd5ca/20261020T072236-94ce262d0292490ba02c26e110385249/result.json",
      "sha256": "3bf033c4fbb4e028fcb97bafffebfc00955d94d3d6af1031c3ff3b6ddfc32c6f",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/calamophyton/r001/semantic-rebuild-2/8483c29e462ba443106a768490caeb7906f20ae267aa81ae895d11e72f8f7582/20261020T072239-21f0272365d94d1e91bab7763b02ce7e/outputs/model.glb",
      "sha256": "005c21c5dfa735762fcfc65387075701ba3e24a915316e6e7c1a59a096362815",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/calamophyton/r001/semantic-rebuild-2/8483c29e462ba443106a768490caeb7906f20ae267aa81ae895d11e72f8f7582/20261020T072239-21f0272365d94d1e91bab7763b02ce7e/request.json",
      "sha256": "e3c32cdefa2bc70c6b22feba075a5a45fe17b5ddccf0c065936bd888b4c8e34c",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/calamophyton/r001/semantic-rebuild-2/8483c29e462ba443106a768490caeb7906f20ae267aa81ae895d11e72f8f7582/20261020T072239-21f0272365d94d1e91bab7763b02ce7e/result.json",
      "sha256": "32193a7252d404ce5cf40ed91129b7aec99da3dec3db5caacb95bc7e89080ddd",
      "origin": "source",
      "owner": "calamophyton"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-1/0b2684055a9e009164d49d8c4f9dda669b90d76e6fba2f7fa9098520dea50856/20261020T072258-f67a481024ca442da6e045ce15f26e71/outputs/model.glb",
      "sha256": "2bdae5b8730c661fe9817df41baa7e12ea5b0f91c78a245f4f13eedffcae640d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-1/0b2684055a9e009164d49d8c4f9dda669b90d76e6fba2f7fa9098520dea50856/20261020T072258-f67a481024ca442da6e045ce15f26e71/request.json",
      "sha256": "1224797538a7dfbe870125441d6aa4271020506382af71b2c7f0600b2bbe90f4",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-1/0b2684055a9e009164d49d8c4f9dda669b90d76e6fba2f7fa9098520dea50856/20261020T072258-f67a481024ca442da6e045ce15f26e71/result.json",
      "sha256": "caf14624a55fb87aacc484d9cfeddf50123ce06cc3c6ce8a2e6e3d8f041dbc51",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-2/1747c1a6e68d0ff38e7a36c99f03ef09f6e82d6aaea8d7a60052dae363effef5/20261020T072305-bd35e062891046fbaaa92f291987db27/outputs/model.glb",
      "sha256": "2bdae5b8730c661fe9817df41baa7e12ea5b0f91c78a245f4f13eedffcae640d",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-2/1747c1a6e68d0ff38e7a36c99f03ef09f6e82d6aaea8d7a60052dae363effef5/20261020T072305-bd35e062891046fbaaa92f291987db27/request.json",
      "sha256": "5f7752eb30972389d97528af80330bcd60f1926d114886fff8fe7dbf39d1303c",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-58/rebuild-runs/build/current-ripple-surface/r001/semantic-rebuild-2/1747c1a6e68d0ff38e7a36c99f03ef09f6e82d6aaea8d7a60052dae363effef5/20261020T072305-bd35e062891046fbaaa92f291987db27/result.json",
      "sha256": "79ac29fb9939c770193e32594a3eb572361430b83ce9ffec04ee99db1e169fe5",
      "origin": "source",
      "owner": "current-ripple-surface"
    },
    {
      "path": "qa/batch58-independent-20261020/barchan-dune-views.png",
      "sha256": "fcd9c68d79a6646e677faa1cd314a1ed0f7143e125b391b56af1439320c9c618",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/calamophyton-views.png",
      "sha256": "bc497d8b6b8bf01bf38c8f08c88d94dbfd657cdecb288eb30ad9549ab7feb732",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/candidate-validation.log",
      "sha256": "059cb16ef0e5298d7e8cc1a7aa7e2b098f418480d01368ecc3bc98d9420c722a",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/current-ripple-surface-views.png",
      "sha256": "146042bf1985c28d26df6d2aaf174aeb8802f21a41609e792b206d954f9d86e1",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/evidence-custody.json",
      "sha256": "41df5be052aa4cbcf83ea73dedfd211379fa54814b47b4022d07e512db30877e",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/freeze-provenance-audit.json",
      "sha256": "2b8cb58b8a63a869c476f3094086bee80ea963a38fc6fd23fe7c5dcc98578a64",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/glb-topology-audit.json",
      "sha256": "8e0cab3d6c149ef4652167b2164c1b13456bc694c23c66d8de6879f73bf1ecd9",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/glb-topology-audit.log",
      "sha256": "8e0cab3d6c149ef4652167b2164c1b13456bc694c23c66d8de6879f73bf1ecd9",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/gltf-copies/barchan-dune-r001.glb",
      "sha256": "4b4580c6ed599b80865ebe9a4e506dc3d4a770077fa5f5be3ec099d3ab8a2543",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/gltf-copies/calamophyton-r001.glb",
      "sha256": "005c21c5dfa735762fcfc65387075701ba3e24a915316e6e7c1a59a096362815",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/gltf-copies/current-ripple-surface-r001.glb",
      "sha256": "2bdae5b8730c661fe9817df41baa7e12ea5b0f91c78a245f4f13eedffcae640d",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/gltf-copies/gltf-validator.report.json",
      "sha256": "2f8fba2ec8637ceb3247c5c095568c4867bff76b801b50bcc89899e1d416b1e1",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/gltf-copies/perspicaris-r002.glb",
      "sha256": "ec95315cac17288508b02d7f3901e9a6a8e8ef464e46b44f460bba049488d35c",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/gltf-copies/qa.json",
      "sha256": "35ae7390483a4802deb5216d0cd6343dcacd6e2e44792d69424c3ac15c3bcffd",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/independent-qa.md",
      "sha256": "ded5ef8f1fc70e1c71c0f730f194135e93e3c22f0505f016465a78f58343a6dc",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/official-validator.log",
      "sha256": "505c791c8c1cbde1bb53a6f2af25f369207f81a187e318774b7a3912cd918390",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/perspicaris-views.png",
      "sha256": "5120bb927d843e90fafb8b3208199fce545e3a4ac008c7d3ac635ea01f50e9c5",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/pin-and-views.json",
      "sha256": "fa6becd6e350196a64a73803be93fd0eb40825ee9a893f24d7699ac404df8691",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/queue-rebuild-audit.json",
      "sha256": "183de526079ad69326904abe0b99f547155a667df4d8befc804e6be96ada379c",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/reopen-audit.py",
      "sha256": "9cb3fb8711373fef108fec4159666d851321f87c94f6048422e896d0f022e24d",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/runtime-audit.mjs",
      "sha256": "5819ae2f41acec1f234c9fa696ceb95e5e2ba02ef7046a3b109d036f6c5a2490",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/source-reopen-audit.json",
      "sha256": "835b33c2e740d32744699064b829d6fba35b21b0a19e77e51d4e813d6e6a8676",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/source-reopen-audit.log",
      "sha256": "f842be942cff1b99c04cf0928f12ed27f3138a4850bb767045956b480bbe82d5",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/three-parse-audit.json",
      "sha256": "d94ac08b9811cf55a564d79167befb0422b8b1dbf494ee2488d1f99ed9e4f5af",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/three-parse-audit.log",
      "sha256": "d94ac08b9811cf55a564d79167befb0422b8b1dbf494ee2488d1f99ed9e4f5af",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-independent-20261020/topology-audit.mjs",
      "sha256": "8da28be671cd09ecc7d5262e7e1bff96a280b3f7a93e3e5adb6f4500bb8a2a43",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/assets/card-previews/barchan-dune-v2-768-q90.webp",
      "sha256": "da1a41300e2992226be1a648378c485a0d1ed75b74e2ba792c632d804024584c",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/assets/card-previews/calamophyton-v2-768-q90.webp",
      "sha256": "7c24d47bf4589eedf695085ecb232ca02ba61c2176e2fea97c322719321a9d54",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/assets/card-previews/current-ripple-surface-v2-768-q90.webp",
      "sha256": "17b0e52797111465dea342474fcb75be060fb910d340fdf1b6212bb2b0e8e9d7",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/assets/card-previews/perspicaris-v2-768-q90.webp",
      "sha256": "e3ef7456c613b3a65a4017ca9fe45051eca918b35190b04fd8b17bb2d1d95397",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/assets/turntables/index.json",
      "sha256": "e5bd58e972a3bfb450d21e8dc43dd5d19b68211d4a5fc2e0572dae03e0a35e70",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/references/barchan-dune.png",
      "sha256": "28d1a601a2e10784d7124e20aff1233ed9ce42802d560f1d0e64ec08f8824f35",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/references/calamophyton.png",
      "sha256": "c71aa4e6ec4730101634f982b569f729eb30bff5bc2ebed95efbe0d7f3e5e365",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/references/current-ripple-surface.png",
      "sha256": "a58d48299f645b87be65051185a832d06cef35cf1cb28569ccdc74e69c5d6ce0",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/references/perspicaris.png",
      "sha256": "ea53e321ac1ddca04afc15ecc8d1de64f7adf9001e067b38404e5b22046a8c89",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture/render-report.json",
      "sha256": "17fe72174a4c459ec7ba5bb602ec48bab23cf46113d6cc33213eb1930c37967b",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/capture-verification.json",
      "sha256": "420b42aa48a8e24456780cd1418f73154b6bf80baff54d34c4434dad48d04581",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/independent-card-review.json",
      "sha256": "515434e55d62dae9d65996894bb4d438fc4650ecc1a4d33f999018e9fa25c5e2",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch58-release-20261020/source-capture-review.md",
      "sha256": "14cbe9f91b6aa7c72a3ff87b72d51c398d3640f66142f3f84c11c63c94e10e83",
      "origin": "release",
      "owner": "$batch"
    }
  ]
};

/** Exact bounded Batch59 release; unchanged formal gates. */
export const BATCH59_RELEASE = {
  "version": 1,
  "scope": "batch59-20261020",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "provider_generation_timestamp": "unknown",
  "source_commit": "330bc4aa669a1647c632a32622ce4318fd8d1b59",
  "review_commit": "289cca9359cdd3595f7015f894a00675a004c422",
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  },
  "base_descriptor": {
    "path": "assets/releases/batch54-20261020.json",
    "sha256": "18848be2e9bffb004c8301ff7f05816ab0d691afbee6b569459f28e3099f3f4b"
  },
  "source_bundle": {
    "path": "qa/batch59-release-20261020/source-bundle.json",
    "sha256": "90ccc901e1058520274c65fef37b66c67267e2c1a08a177307c72dbd8cbcfe64"
  },
  "protected_source_inputs": [
    {
      "path": "ATTRIBUTION.md",
      "sha256": "31cfae805768d2857f9cd3b86d328ba1ec83f3c28ccc728b0cac8edddfd29412"
    },
    {
      "path": "LICENSE",
      "sha256": "9dc06b87ac2f86cc6c7b3afdd8b02c5887c9a29bf5a4924a611937d4195f996c"
    },
    {
      "path": "LICENSES/CC-BY-4.0.txt",
      "sha256": "9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411"
    },
    {
      "path": "LICENSES/MIT.txt",
      "sha256": "f4cd278b3853ba4c6b36d85975839c2b51d09bb841d6eecced516c482e826ce0"
    },
    {
      "path": "package-lock.json",
      "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
    },
    {
      "path": "package.json",
      "sha256": "1bddf73367b09c1c72034cca826c1dfcebc1ae35e1480d9da99b8fd202a34b1b"
    },
    {
      "path": "production/policies/qa-passed-batch-publication-20261018.json",
      "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
    },
    {
      "path": "schemas/README.md",
      "sha256": "cdecb3681106b07e1414d18a4861162525da67d7061e7f7539f40c0fc817d615"
    },
    {
      "path": "schemas/templates/brief.template.json",
      "sha256": "cb1f2ff179d3363f0adec9717be204e2a355056686fadf792eea232c82b9278d"
    },
    {
      "path": "schemas/templates/candidate.template.json",
      "sha256": "3148c62284480a8118bc89135a3fa1371cb0c86f2726369338c499fc32dc2a91"
    },
    {
      "path": "schemas/templates/references.template.json",
      "sha256": "9c43e161399f377d2e943f36ddcecf84330618495689f461fb1b8beba80d288b"
    },
    {
      "path": "schemas/templates/static-profile-contract.template.json",
      "sha256": "538e12417c3d77e84746e8a4814c3c18701c18d327707b8ac4043fdea32c8ce4"
    },
    {
      "path": "schemas/templates/textured-brief.example.json",
      "sha256": "51a3b254d288bdc5f2716f6272a57539529cb17ac8939cc1c2787d7416ab5ab9"
    },
    {
      "path": "scripts/asset_common.py",
      "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
    },
    {
      "path": "scripts/candidate_profile.py",
      "sha256": "0489ec5378ec5d073ac4e84994b796ac529b122fd1c9c51be7b55623a413ac7d"
    },
    {
      "path": "scripts/check_reproducibility.py",
      "sha256": "62ab7b959ad8e73128d1d1f2300fd4bd19ecc92244bccf6cc88fdc7b0b3a57d2"
    },
    {
      "path": "scripts/check_source_export.py",
      "sha256": "1b4aafd9d1963e103ba469aff7e1f3917592e839f9372883b88c7db51834b34a"
    },
    {
      "path": "scripts/qa_glb.py",
      "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
    },
    {
      "path": "scripts/render_candidate_views.py",
      "sha256": "22a4bd8aab71dc76696f01f2bd768ad371ebf9b4230e170c921063b5f842f041"
    },
    {
      "path": "scripts/run_asset_queue.py",
      "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
    },
    {
      "path": "scripts/validate_candidate.py",
      "sha256": "fe679a8be19d16b9d9b86ee3419a73d2dd16b77dfa371bf1186ce0120d120ff9"
    },
    {
      "path": "scripts/validate_concept_evidence.py",
      "sha256": "745938a9b1624e8b744e9c03f597fd8d967ef1b4c145209805c6b6357578c723"
    },
    {
      "path": "scripts/validate_gltf.cjs",
      "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
    }
  ],
  "review": {
    "path": "qa/batch59-independent-20261020/QA-report.md",
    "sha256": "de1608a0e8fa90d519b6bd7aed1002c7bdb853631d57dbd1f7c5fb6d4680ae1e"
  },
  "review_custody": {
    "path": "qa/batch59-independent-20261020/evidence-custody.json",
    "sha256": "3fe9ea28e306273b9c3ed4e727576f702d6deaeec7fd15c35a12c3e7067d7c54"
  },
  "capture": {
    "report": {
      "path": "qa/batch59-release-20261020/capture/render-report.json",
      "sha256": "17fe72174a4c459ec7ba5bb602ec48bab23cf46113d6cc33213eb1930c37967b"
    },
    "index": {
      "path": "qa/batch59-release-20261020/capture/assets/turntables/index.json",
      "sha256": "e5bd58e972a3bfb450d21e8dc43dd5d19b68211d4a5fc2e0572dae03e0a35e70"
    },
    "zip_verification": {
      "path": "qa/batch59-release-20261020/capture-verification.json",
      "sha256": "420b42aa48a8e24456780cd1418f73154b6bf80baff54d34c4434dad48d04581"
    },
    "independent_review": {
      "path": "qa/batch59-release-20261020/independent-card-review.json",
      "sha256": "515434e55d62dae9d65996894bb4d438fc4650ecc1a4d33f999018e9fa25c5e2"
    }
  },
  "excluded_ids": [
    "erbenochile"
  ],
  "additions": [
    {
      "id": "glacial-erratic",
      "revision": "r002",
      "source_commit": "330bc4aa669a1647c632a32622ce4318fd8d1b59",
      "review_commit": "289cca9359cdd3595f7015f894a00675a004c422",
      "metadata": {
        "path": "assets/additions/glacial-erratic/batch59-20261020/release-metadata.json",
        "sha256": "0aa94971593bfc31fe1da221bbba7f83fde2c70d622f303a4cceeafd45395744"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/candidate.json",
        "sha256": "2d8e3d573930296ca990e3c754afb1135c5b94334938d252fe5a12364ea62c81"
      },
      "review": {
        "path": "qa/batch59-independent-20261020/QA-report.md",
        "sha256": "de1608a0e8fa90d519b6bd7aed1002c7bdb853631d57dbd1f7c5fb6d4680ae1e"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/metrics.json",
        "sha256": "d2f147c47f158a0c1c1f98d586206880f8f011f757910363bf277876ae5a0999"
      },
      "original_metadata": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/metadata.json",
        "sha256": "efc317adb1c3e8fdaa649749b438a1c0567995414012f5417806fd4e5c2a65cc"
      },
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/brief.json",
        "sha256": "f205a3faa10a068c52d202cdd0a22ce1020d2cbea58e62ff7a856a68c788a98b"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/render-manifest.json",
        "sha256": "5dc58f10cfa299dc367861c1c0400dd88247a9e71f3d0a08a53f5f216e74aefd"
      },
      "rebuilds": [
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/rebuild-1.report.json",
          "sha256": "30f77345522cc9bc566ad26a7ac86c970aae964caf1ea0189f3417f3e2a7402c"
        },
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/rebuild-2.report.json",
          "sha256": "8c3b854374ca783c0227b69c31e70096dbbdda153002c3f41f443fdaf2386ea9"
        }
      ],
      "capture_reference": {
        "path": "qa/batch59-release-20261020/capture/references/glacial-erratic.png",
        "sha256": "06cf6c4bffaae4506fa3e62b5c33fe399a7351811d98b612dfd178511613a695"
      }
    },
    {
      "id": "gypsum-cave-flower",
      "revision": "r002",
      "source_commit": "330bc4aa669a1647c632a32622ce4318fd8d1b59",
      "review_commit": "289cca9359cdd3595f7015f894a00675a004c422",
      "metadata": {
        "path": "assets/additions/gypsum-cave-flower/batch59-20261020/release-metadata.json",
        "sha256": "c20d29152f569888c8be31b3b0b6cd9353fd8a950eacaa4cb1cc9e60c80c4a20"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/candidate.json",
        "sha256": "c6e95e08c99e53e69295e5684839be7c91fea0bb849120d53484a3f4d99aa1a6"
      },
      "review": {
        "path": "qa/batch59-independent-20261020/QA-report.md",
        "sha256": "de1608a0e8fa90d519b6bd7aed1002c7bdb853631d57dbd1f7c5fb6d4680ae1e"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/metrics.json",
        "sha256": "57d042f10fe05e02947aca98fb9cf4fee01eb90ef6541543050c1c10c98caf62"
      },
      "original_metadata": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/metadata.json",
        "sha256": "26926652a133f47fa3dbc18f56a29533cf0daaff5a1d2ec2016a800cf777bcc8"
      },
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/brief.json",
        "sha256": "b22c9eb1acff38a7d67d06fedd78a8475f0597addf59965a663496b75badcdfe"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/render-manifest.json",
        "sha256": "0cb96385202363d9a1a1e92977f1c57642bc1065b6cb3192d56ac81725337e1b"
      },
      "rebuilds": [
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/rebuild-1.report.json",
          "sha256": "08e7349a2b23d803f586c466d9daa8df03d94c93d08bb2e9ecbccba0457b00a9"
        },
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/rebuild-2.report.json",
          "sha256": "32d93777da741a0ea247daee61e0c16b93c31eea4ebae2c7777696994b6266c4"
        }
      ],
      "capture_reference": {
        "path": "qa/batch59-release-20261020/capture/references/gypsum-cave-flower.png",
        "sha256": "5a16d53abeea289548fe6e7232520bb7223ce77b71e3f97b55ad093521d41c4d"
      }
    },
    {
      "id": "stalactite-group",
      "revision": "r002",
      "source_commit": "330bc4aa669a1647c632a32622ce4318fd8d1b59",
      "review_commit": "289cca9359cdd3595f7015f894a00675a004c422",
      "metadata": {
        "path": "assets/additions/stalactite-group/batch59-20261020/release-metadata.json",
        "sha256": "522be7878e29dbc1d2ee87409974fa65937639aeaa86665171c5649e3b04af66"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/candidate.json",
        "sha256": "dbab752080622f3adb04432f576179114150cad3a0cd14eb47954261f6350806"
      },
      "review": {
        "path": "qa/batch59-independent-20261020/QA-report.md",
        "sha256": "de1608a0e8fa90d519b6bd7aed1002c7bdb853631d57dbd1f7c5fb6d4680ae1e"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/metrics.json",
        "sha256": "99c55fe895b084befa1f519c3d98ee8e8dd0e2b579ca731076de8b911edfb9a0"
      },
      "original_metadata": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/metadata.json",
        "sha256": "c1d421c64196efa46ea0e619e985387be0fae424238cc4ccfdcd2f27a8e0765d"
      },
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/brief.json",
        "sha256": "e9f99ec92d3a562b18f4cff44394531d08cd99e22d9a91411aa8e7842534ef4c"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/render-manifest.json",
        "sha256": "80fcccbf3d3c199815f76a8f1edf3caca7b0fbfaa45e6e27a604ea7b419b1028"
      },
      "rebuilds": [
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/rebuild-1.report.json",
          "sha256": "71ff99c01c67c4bd70ead6b2028759745bf6f810f0b7298fde969da99833264d"
        },
        {
          "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/rebuild-2.report.json",
          "sha256": "e3b0355cb25ba6e93f2d63bd4035dd45236fbc119540272ce2bd502492e15e8d"
        }
      ],
      "capture_reference": {
        "path": "qa/batch59-release-20261020/capture/references/stalactite-group.png",
        "sha256": "18e04e45636d923193b3a9558649d64f8031fa59257eaa5b490c65bd0cebc586"
      }
    }
  ],
  "files": [
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/authoring-start.json",
      "sha256": "4e22b7f0651149374956f8b00e8a193aae136f5287a9c94bb7d8854d77e17dd7",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/brief.delivery-v001.json",
      "sha256": "84d96a4439937d436007a3c8e390466381e1c74533b086979c1eabdef20b4e18",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/brief.json",
      "sha256": "f205a3faa10a068c52d202cdd0a22ce1020d2cbea58e62ff7a856a68c788a98b",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/brief.md",
      "sha256": "d9b8a1741da8c9795334676bd987d83b6675cd4b19a2a6e6e0fffb32f3d3317f",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/build-config.json",
      "sha256": "28fed7227c3620a169a0782abe0e85e5563cdef66dd1a6d134ad8e0213964866",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/candidate-validation.json",
      "sha256": "fad037718b23379060cb2ce658da01ab413df8209e167fc980daee05ee664fa3",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/candidate.json",
      "sha256": "2d8e3d573930296ca990e3c754afb1135c5b94334938d252fe5a12364ea62c81",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/concept-evidence.json",
      "sha256": "1a894781144d0a37fee49ebe706bf39fd20a26eed684e33dae1dc589b93c79df",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/concept-validation.json",
      "sha256": "c4d9e4d18fbb8b0436ef2ef590a9f09262cf44b9f2e3c6e9d38377dd538826ca",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/concepts/generation-record.json",
      "sha256": "f3f7b4703f18d122442dec16fddde9582ae1be1f9ba6f4baa964d940c5221088",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/concepts/inspection.json",
      "sha256": "f74e7558aca29f22c4f9095ae6b8f677cc43e4540330ef3bccd0a7e350b94502",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/concepts/original.png",
      "sha256": "ab336656469263436be00788818db00a2d119872623e0d7e9c43e5d01086780a",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/concepts/prompt.txt",
      "sha256": "6c7fa0f06398703ed9ae6a52dae1f058d0e9be14f14cefcb4c20b218dfb2b853",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/delivery.json",
      "sha256": "32ed4f31e85010ed0d1d06b5295dfd7ec22b45811653a7a1e4fa8d3820c87711",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/eight-views.png",
      "sha256": "2b8cd71cd76cd992ab1e0316185dacfd932cb4ea871dffcbadd29d490d9ae2ee",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/generator.py",
      "sha256": "cc5ed645c7c04b6080bfd8e024a77599b64716774bc9a3dcdbe86111cd0eada5",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/glacial-erratic.blend",
      "sha256": "e4381e4138c48006a922e387d7437ea8425b7e2d23d4137bf99e786ce1f57f02",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/glacial-erratic.glb",
      "sha256": "94bdc5b0dddd8a3925d53ded4be6191d4769cc9414d8860d9664a8170010bfcd",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/gltf-validator.report.json",
      "sha256": "52e62ee2f0164ded069c580f43fce8675a762c9bb8ef8aa4fab34cda1c8cefbf",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/hashes.sha256",
      "sha256": "386d3ff5b32288b39eef06e412ee36071514c5344809d368d4349f5a4c7bcad1",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/maker-review.md",
      "sha256": "77b25a0eef07b38c892f16e009e6bc1e2dd51501053cf9a0cfa8e63c6613dcc0",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/metadata.json",
      "sha256": "efc317adb1c3e8fdaa649749b438a1c0567995414012f5417806fd4e5c2a65cc",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/metrics.json",
      "sha256": "d2f147c47f158a0c1c1f98d586206880f8f011f757910363bf277876ae5a0999",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/modeling-freeze.json",
      "sha256": "8b2c7e4fc811cab10f8352f25109ff424dcfc1054a4aed59ce4dbcd4380925f9",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/profile-contract.json",
      "sha256": "b34cffa1a60eb08267d00b04cbc351fc3b57478d6ddde9258c8dea566766a089",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/clay.png",
      "sha256": "36e19ba9b96a3afd40aa7da87fa1adefc406230e606bf5fc4c0514c7ef22c06c",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/front.png",
      "sha256": "3af45d787cdce987ce568a13b0bae7b57062184e4d4b3dbaa57d36f022a6da54",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/hero.png",
      "sha256": "4efe0149abdbf8d189bd63df731c36c010ed533e511acfe68d02a3722203681e",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/rear.png",
      "sha256": "db56ae88a8434a331442b2a5dc74c75a9f3281aeb11740fb2e901a770b43707e",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/render-config-static.json",
      "sha256": "0d0675c10f3d046871ba794df8ee489cbb590ba49819744564fbb1edeb690e49",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/render-config.json",
      "sha256": "f9f46260a01842277fd9de15a5cb65b07484bd145284880d7d7c2fc80f615d27",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/render-manifest-static.json",
      "sha256": "a374f0c103b281576faae0d420ce6fe134bd61e071c4eac94e00c9aa7f4236c7",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/render-manifest.json",
      "sha256": "5dc58f10cfa299dc367861c1c0400dd88247a9e71f3d0a08a53f5f216e74aefd",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/reversehero.png",
      "sha256": "71d0431fce920b3f0da7b50619466dbd8be0b91bacee04cd4222b062a504bd8c",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/side.png",
      "sha256": "553c2e400606a03d5cf301e1040b12acb0279858667979191a35651e5435e07f",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/silhouette.png",
      "sha256": "3a9b3d9b63c123a9063509196f0547a6b9405ef01abb72682b8ededc3dd1f3fd",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/top.png",
      "sha256": "4130a459a08f8d1b42308a557f94760428b59b0b39f2e9b96dca63e8105d1d6c",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/proof-final/turntable.json",
      "sha256": "84dc77abca99915bc2f516c620a3ad5086b905a5903b922c60f456865426ec3d",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/qa.json",
      "sha256": "9a2e49459f8d0ee98e41c45a8be08648814c942c334bfbb5ff667600001f65bc",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/rebuild-1.report.json",
      "sha256": "30f77345522cc9bc566ad26a7ac86c970aae964caf1ea0189f3417f3e2a7402c",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/rebuild-2.report.json",
      "sha256": "8c3b854374ca783c0227b69c31e70096dbbdda153002c3f41f443fdaf2386ea9",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/references.json",
      "sha256": "55fce1ff9558cc7d07a0912fa402e2682f83cc8030b8a1ccbedcb8c430da420c",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/repair-freeze.json",
      "sha256": "f007367a5f1cc464d7d0b784bbd3e92d10907718585a182117a11f8464854c4d",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/runtime-parse.report.json",
      "sha256": "a321682501630043162677969ad794385e0ec7c262758a1e507e797c5c677c2b",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/runtime.report.json",
      "sha256": "8b05e601dc86bee930b37b335af2a8eff3eea38e5c8c606ff42cc55342a5e359",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/source-export.report.json",
      "sha256": "28ddbde0232bef3bd4c771b9919280462af4e9726d177c8c696a8a3672dfad69",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/static-glb.report.json",
      "sha256": "3544574c8e267a16a7418c9a5d25223fad54dd078f216f2f46d271396bd75164",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/glacial-erratic/r002/technical.report.json",
      "sha256": "80130a8abdc20af3a3f2014048a1fd2252ff442a00e985b2955e90c486c9a648",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/authoring-start.json",
      "sha256": "a9316903fb691e8d809e9f281126b4cd7c1f431b57c20d4d6f0200a2808609b1",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/brief.delivery-v001.json",
      "sha256": "4bee0a60bb107ec5f999ab58464f8b8175df379bd8574b2868f5c3a42fc4599a",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/brief.json",
      "sha256": "b22c9eb1acff38a7d67d06fedd78a8475f0597addf59965a663496b75badcdfe",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/brief.md",
      "sha256": "0f05eb84a7461d808277e3bb1eb99aa02faadd461d5424500d2db447a9950208",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/build-config.json",
      "sha256": "d4ae566acb2a57d6c3faefcd0de4c8bf769aa458b1b5497dbbf710ddbe06c941",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/candidate-validation.json",
      "sha256": "d6a995a64ac2a9b66800680be4f2fb120f7ab3048ab184d9075c2cc564eb87a9",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/candidate.json",
      "sha256": "c6e95e08c99e53e69295e5684839be7c91fea0bb849120d53484a3f4d99aa1a6",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/concept-evidence.json",
      "sha256": "85e768508f574984359b35cd94b22aeb61dd144d39ea4e57987bc24a4573edee",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/concept-validation.json",
      "sha256": "e3a64c9c5f8efcf66404d5f093a1f53c58c0ff549df0b4424c3f0e15c43f06bc",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/concepts/generation-record.json",
      "sha256": "b4da1da75c30780bbe18614c425f6c323fbcb765200deeef7618769059be70c7",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/concepts/inspection.json",
      "sha256": "5157f00f1b5ab112ad9bd558578bb79f5127507e99f9dd9244f38701cb384707",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/concepts/original.png",
      "sha256": "4f0e5e478813fe50e09be25967bd46d3f4cf2348d6000e8d24e287ec0a2fb7d0",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/concepts/prompt.txt",
      "sha256": "2a960403e40e63fe277b0ff39533b1500b14c016a489e2faf8d3de4b5bc2198a",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/delivery.json",
      "sha256": "b0ff706923209a7806c53ec5f84f0d6d37fbd48c78ae44c7707cbead3148651e",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/eight-views.png",
      "sha256": "883c0fbc3e9bcfa4ab4ddbe80eb34173a98a3ef3a9a5185cd5b903498e5a5011",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/generator.py",
      "sha256": "cc5ed645c7c04b6080bfd8e024a77599b64716774bc9a3dcdbe86111cd0eada5",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/gltf-validator.report.json",
      "sha256": "57a08a2c34030fcdd4d4c2730227cdd7d25abb474f2e7dcda01a920516c93211",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/gypsum-cave-flower.blend",
      "sha256": "90a8c4f5a71a5cf9a90519559f312ef4da744daeed48295911460cbe3d593b9b",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/gypsum-cave-flower.glb",
      "sha256": "8ddaf4c36f2fd0dbe7c3971c27c750e8c41760954a8fb25e9e40b679c24eac2b",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/hashes.sha256",
      "sha256": "0dd516b8e2478814560d69746cbed18b18b1f4a711a550eae53a0f4670b79072",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/maker-review.md",
      "sha256": "425f598296830799cd30ab25f853561306cc840d9d976118542e77e8b08111ec",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/metadata.json",
      "sha256": "26926652a133f47fa3dbc18f56a29533cf0daaff5a1d2ec2016a800cf777bcc8",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/metrics.json",
      "sha256": "57d042f10fe05e02947aca98fb9cf4fee01eb90ef6541543050c1c10c98caf62",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/modeling-freeze.json",
      "sha256": "5455a627702922cf612779f0b0b75212958942f8e0418ec023e4b53e1530f9dd",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/profile-contract.json",
      "sha256": "b4f2213c41d23c6ca552b1eb59f01d50ab5769495e429391f0c75a04795bd756",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/clay.png",
      "sha256": "b93c9b58790a0b416f7c2e0bd26d342bc1b15e783d1250e217438e24636efe19",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/front.png",
      "sha256": "971badf78be5e0a7d3ce4a237b53bd1727c554fd9c5a66d7aee7789488a1faa9",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/hero.png",
      "sha256": "9296a21bdc5e294917f0eb0aa097dd5a7227e670b4d8801b4de3763feb7e79b4",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/rear.png",
      "sha256": "f35071ff210d98f613bd17febf83d46fd70589516db0563c2f8a9051ff86d488",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/render-config-static.json",
      "sha256": "479edcd89191633d11d4550d9b37993dfccb13189877ee1f9eaf12fab9221847",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/render-config.json",
      "sha256": "1459df1569036ba3c1e46c648feee121989eea987e4350329a4cec7dd77b7e03",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/render-manifest-static.json",
      "sha256": "06f2c3047ea93772556dc1097cc5321cf552b11a2716610685ab384d3d47574d",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/render-manifest.json",
      "sha256": "0cb96385202363d9a1a1e92977f1c57642bc1065b6cb3192d56ac81725337e1b",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/reversehero.png",
      "sha256": "ac1645dd5559d1a6a36906322d84c1b13f44c73789d36dde6e7f6b43a22e8689",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/side.png",
      "sha256": "cfc38745acfc34944b2ce89f74bc527ac4add22daddc36636117fb05c10917b1",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/silhouette.png",
      "sha256": "f28db54d53e02b547a750294dcf07dc9f18af836f00533e29bbf751f54928679",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/top.png",
      "sha256": "e39dbed527c3833e133cfecb0d3bd7ff02994bbbe0937b8128ea33a91a86c7f0",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/proof-final/turntable.json",
      "sha256": "8ca64ae980ba20d6b692c108576d40933987f5e699e7229294bafb8dc22b999e",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/qa.json",
      "sha256": "94c4f1bfbc7fab4edcf4d059d6e6e555f7705c4fc1ad18351ec270ceede66d12",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/rebuild-1.report.json",
      "sha256": "08e7349a2b23d803f586c466d9daa8df03d94c93d08bb2e9ecbccba0457b00a9",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/rebuild-2.report.json",
      "sha256": "32d93777da741a0ea247daee61e0c16b93c31eea4ebae2c7777696994b6266c4",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/references.json",
      "sha256": "ac94eddc9f19b063322e88b0f9c8a88335ebcf64acb6aec98f3a2322113ae29f",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/repair-freeze.json",
      "sha256": "2490d149ac8cc8c87513b29062809e26288e5b9a7c45f0a32af021fb4beb1395",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/runtime-parse.report.json",
      "sha256": "a7939010e20b4cb324ff99d147187a89ae18bb573a3f871faab21d7f9653de11",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/runtime.report.json",
      "sha256": "84052c0f64e82b3986abe6b4081b55b55f67e7639781163ee060e6601b8c3b5a",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/source-export.report.json",
      "sha256": "d6812de80cb952d61abe6288c895ffc42d4f69cfad4b5f0551d42dca90cf01b6",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/static-glb.report.json",
      "sha256": "09e9dc94f405119622336d2392d6975c936c45baa5f0fec8820d49480cb36901",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/gypsum-cave-flower/r002/technical.report.json",
      "sha256": "56dc2bc6fdca7199e0dfeedcc0427662b2f6dd193cceb53eaa6912da2e949561",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/authoring-start.json",
      "sha256": "ccbb0f19d8dc8a4ae5484a06c759936abae2765844fabd77064c0667f358dfe7",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/brief.delivery-v001.json",
      "sha256": "13f329fce348f36e674b1630d788d8cf5cbe764ad4ee9426fec983f257114234",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/brief.json",
      "sha256": "e9f99ec92d3a562b18f4cff44394531d08cd99e22d9a91411aa8e7842534ef4c",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/brief.md",
      "sha256": "084e3d46d6189e3c2b853e6e7e8f4125d5542810028847d48ef88b37b1de5296",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/build-config.json",
      "sha256": "afc5c6600f0e24daf64151c6cd6b905c3bb6b5255318ca2458420acc53248c8e",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/candidate-validation.json",
      "sha256": "5d15cba6b05166a8261412351c2ea1e847f071da415a1ddbf41cb022ee9de455",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/candidate.json",
      "sha256": "dbab752080622f3adb04432f576179114150cad3a0cd14eb47954261f6350806",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/concept-evidence.json",
      "sha256": "d59508dd6d1400a15916d623e62c9d79a1b3c3e84ea57a307973be9bb547d8f8",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/concept-validation.json",
      "sha256": "12df1d387dd8c011f731928dbfe61f847909e195261e882a83e6b2700d54711c",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/concepts/generation-record.json",
      "sha256": "898e69b0e525b9e2735438ec66f845b948040f77d1f249063ebd54cfe8e963e6",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/concepts/inspection.json",
      "sha256": "157199b73769c27de9b2f4e55bd8f4e115f2ae80e688180ef8235efc69704b92",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/concepts/original.png",
      "sha256": "ab336656469263436be00788818db00a2d119872623e0d7e9c43e5d01086780a",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/concepts/prompt.txt",
      "sha256": "6c7fa0f06398703ed9ae6a52dae1f058d0e9be14f14cefcb4c20b218dfb2b853",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/delivery.json",
      "sha256": "25c16c246b18906bf9c6ea78b409d14225184c86e9167542ab83da521172aebf",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/eight-views.png",
      "sha256": "c982f125116d6296e5b48d8886d17e3680d6b0effac13615a49534c123928908",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/generator.py",
      "sha256": "cc5ed645c7c04b6080bfd8e024a77599b64716774bc9a3dcdbe86111cd0eada5",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/gltf-validator.report.json",
      "sha256": "1732ab5fd4a025d171f510ee054cb712052c7339e4b7a73fffe6778ebeb17c3b",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/hashes.sha256",
      "sha256": "6d05fc792dfb3f450a5ab1da8fa0aba6a5230b3d6e63e8234545e495882e0b75",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/maker-review.md",
      "sha256": "e56279d4e853e0546555f55f814c1871d86979b5818bfac40ad2a0fd67a91501",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/metadata.json",
      "sha256": "c1d421c64196efa46ea0e619e985387be0fae424238cc4ccfdcd2f27a8e0765d",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/metrics.json",
      "sha256": "99c55fe895b084befa1f519c3d98ee8e8dd0e2b579ca731076de8b911edfb9a0",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/modeling-freeze.json",
      "sha256": "88dc595044e9addd01af06753720033a55e271f07836e980bb281282b418f02f",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/profile-contract.json",
      "sha256": "c63b35f9ea943bd5efa0f7c9e83e36f0b4a14a14ff1776a8afa7bc5086c448d9",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/clay.png",
      "sha256": "194961f0e914df6c8a14c9584383eac7138c51a4c82c1a8d8ba2091b17ba826c",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/front.png",
      "sha256": "9e6edaa88957fbbbec6710dde003281e2030387ad94772340439d130c4aa7304",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/hero.png",
      "sha256": "98cbe7066c1c32d9e31c4ad159d82fe166866d09e93beaeda17a370fce3e0659",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/rear.png",
      "sha256": "e41c94fc3b4b6a502f29565a241bcaeec117be29e1144e606fd7db6a5e35f937",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/render-config-static.json",
      "sha256": "c4e73f14f1ec4eac446d2d9d95f4c19f832c2a877e8d5cdb1aa748db628f1fdd",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/render-config.json",
      "sha256": "c4b0d69b3db2f80ed0aa79e495ba4875592bac377ca9f60636245ac041a28df8",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/render-manifest-static.json",
      "sha256": "93b6507972189b9b95d3798262ebdad9c0f6d49e026ad525ed60c895d25ce526",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/render-manifest.json",
      "sha256": "80fcccbf3d3c199815f76a8f1edf3caca7b0fbfaa45e6e27a604ea7b419b1028",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/reversehero.png",
      "sha256": "999083fee53609984d411b59a7c1c02303a704541a770d90aeb4141da2b3222c",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/side.png",
      "sha256": "e07814ce5f4a688dff89361685e1b6242db55a25a639936470a71a70082f13c2",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/silhouette.png",
      "sha256": "87b95a15a26bb5768e9867de678097a2db3322b4106cbfce522b3ac7e13e0dbc",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/top.png",
      "sha256": "396200f216dbe7b3e8c2e445be265f44961deb022e28f58c508f03d0877dd245",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/proof-final/turntable.json",
      "sha256": "bb87f7bfca6a06eb7018878ed30a06b4c4b0a47eb4a11139d4550295d398516b",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/qa.json",
      "sha256": "28c1a7832ab3f8b2a4da281c42922a640b678cc817b229ce9dba917dae2c5368",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/rebuild-1.report.json",
      "sha256": "71ff99c01c67c4bd70ead6b2028759745bf6f810f0b7298fde969da99833264d",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/rebuild-2.report.json",
      "sha256": "e3b0355cb25ba6e93f2d63bd4035dd45236fbc119540272ce2bd502492e15e8d",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/references.json",
      "sha256": "0aa4604481bea2e8e093d581f13aa7d7176610b28696ed5618d565932ed4e58a",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/repair-freeze.json",
      "sha256": "595703592a019981c55deae1caaa5612804c2f1ec54f273660365a4e7648ac74",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/runtime-parse.report.json",
      "sha256": "89188d1f6cae1d11e77550c61e2b0995209f54ed81bddf49afe9cb99c3c36b79",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/runtime.report.json",
      "sha256": "4cae1b2c198de23fd5ac8c5e86097e7dd5dffde25409994e00b068ea2d57bf78",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/source-export.report.json",
      "sha256": "6f1a2b757b2a5dac399d2ae371a91f72f094d5ac0821fc714326c805d62f14b1",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/stalactite-group.blend",
      "sha256": "1a56a769490486027c70f5afc4d953cfec9309efdd4232c4ef5ab17d31cc29b4",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/stalactite-group.glb",
      "sha256": "6e2bf795d94dae162a65dd8cf0924d70e402e28dbb1c17917d622919d608fca7",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/static-glb.report.json",
      "sha256": "2a8b21e5ed451f67abbb723858eadfee75a83a0d088c6c0d60dff10277e7fe7d",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "assets/candidates/continuous-small-life-round22-20261020/batch-59/stalactite-group/r002/technical.report.json",
      "sha256": "4150510e40d08e5b96484758c9b9ff6610570c1de8ebea68e2ac9eb50cc308f2",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/HANDOFF.md",
      "sha256": "6b8d302ee2659a238f397f5453341ac3475765b7b0ca92c2138e2736156c361c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/build-dependencies.json",
      "sha256": "2bde36af86085b0909c4e735c78de2e65a4eb12b8fb49ade95ae7e476de3d6b8",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/claim.json",
      "sha256": "0fb138563e44353d67dd79bb1e16509b72ca45d0d270b1f976d0f68296ab4666",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/final-selection.json",
      "sha256": "66963b8cfcab0670ac70788248fc9f7862544b80cd5d1a75cf4f219084fbb9e6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/handoff.json",
      "sha256": "47aea5ff37efd0a6d39d71b8d3dfb9f61b42105e3e005b9c431da968b76e33a6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-queue.json",
      "sha256": "eaf65a5ffb6e9c85b25b38e37fcf717cf2244738d7ccef4ab460987108629abe",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-1/871024eecb4c07c0828eab82f26d4e24ad770813261ff6002ebfd552ad42c945/20261020T072306-95c515fb7ed34063a0442b1e5824392c/outputs/glacial-erratic.blend",
      "sha256": "a3fa662aead9e4df366bbec34b2e6612cbc96c854142e7e4f22d55f0756b6304",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-1/871024eecb4c07c0828eab82f26d4e24ad770813261ff6002ebfd552ad42c945/20261020T072306-95c515fb7ed34063a0442b1e5824392c/outputs/glacial-erratic.glb",
      "sha256": "94bdc5b0dddd8a3925d53ded4be6191d4769cc9414d8860d9664a8170010bfcd",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-1/871024eecb4c07c0828eab82f26d4e24ad770813261ff6002ebfd552ad42c945/20261020T072306-95c515fb7ed34063a0442b1e5824392c/outputs/metadata.json",
      "sha256": "48c8cf411e4d9158958b0d1134a43bc3af0068db80f301ea4e06d8eb03201db2",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-1/871024eecb4c07c0828eab82f26d4e24ad770813261ff6002ebfd552ad42c945/20261020T072306-95c515fb7ed34063a0442b1e5824392c/outputs/qa.json",
      "sha256": "56387045ec61f5b3bfcec62634fc4de518362583b84b541eee7bf84f4ee9051a",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-1/871024eecb4c07c0828eab82f26d4e24ad770813261ff6002ebfd552ad42c945/20261020T072306-95c515fb7ed34063a0442b1e5824392c/request.json",
      "sha256": "f563155d6882c8c845da0cde143e97b4ab4933f9095af609d4c2328a8d77630a",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-1/871024eecb4c07c0828eab82f26d4e24ad770813261ff6002ebfd552ad42c945/20261020T072306-95c515fb7ed34063a0442b1e5824392c/result.json",
      "sha256": "497286a00e6724a9a99a4f23d863229ea284a8b4375d2db566a9763013968463",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-2/10e39bac18a4fb1addb55798a8d8751401668fabeb3e4e11dec8516d92a04e7b/20261020T072308-0e52d0677f4f412ebdda2f5caca4ea5e/outputs/glacial-erratic.blend",
      "sha256": "cab9111a18fc2e9d3dca3d7294ca337d01f55ff9cba6c7c83b55e697d88051e5",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-2/10e39bac18a4fb1addb55798a8d8751401668fabeb3e4e11dec8516d92a04e7b/20261020T072308-0e52d0677f4f412ebdda2f5caca4ea5e/outputs/glacial-erratic.glb",
      "sha256": "94bdc5b0dddd8a3925d53ded4be6191d4769cc9414d8860d9664a8170010bfcd",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-2/10e39bac18a4fb1addb55798a8d8751401668fabeb3e4e11dec8516d92a04e7b/20261020T072308-0e52d0677f4f412ebdda2f5caca4ea5e/outputs/metadata.json",
      "sha256": "bbc478d9d1bff0c495e7d63210536bbcda33b97f348319d66517a90d8fc705ed",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-2/10e39bac18a4fb1addb55798a8d8751401668fabeb3e4e11dec8516d92a04e7b/20261020T072308-0e52d0677f4f412ebdda2f5caca4ea5e/outputs/qa.json",
      "sha256": "2f51405600c0f127aa1344048d805d18c2af5d128ee59371cc165b3454400cdd",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-2/10e39bac18a4fb1addb55798a8d8751401668fabeb3e4e11dec8516d92a04e7b/20261020T072308-0e52d0677f4f412ebdda2f5caca4ea5e/request.json",
      "sha256": "9bb7de7d6342dcd963126de38ff52bac952f3e17209544d3384192efdaede836",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/glacial-erratic/r002/rebuild-2/10e39bac18a4fb1addb55798a8d8751401668fabeb3e4e11dec8516d92a04e7b/20261020T072308-0e52d0677f4f412ebdda2f5caca4ea5e/result.json",
      "sha256": "f0fbaef380776541b83000a2e46c92d7d9b41519b9f024d9616b56b7380b0699",
      "origin": "source",
      "owner": "glacial-erratic"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-1/c189f987268df41f36e3dc9d5ad8468c44d7891eb52b3c8bff26ce8ac2ce3ac8/20261020T072317-616a68d97fff4afdb7eba7e3bd943656/outputs/gypsum-cave-flower.blend",
      "sha256": "ec9497059a5139bbaf5e165e0fc138aa8ea1cdbe65f68e47276b5328702570a1",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-1/c189f987268df41f36e3dc9d5ad8468c44d7891eb52b3c8bff26ce8ac2ce3ac8/20261020T072317-616a68d97fff4afdb7eba7e3bd943656/outputs/gypsum-cave-flower.glb",
      "sha256": "8ddaf4c36f2fd0dbe7c3971c27c750e8c41760954a8fb25e9e40b679c24eac2b",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-1/c189f987268df41f36e3dc9d5ad8468c44d7891eb52b3c8bff26ce8ac2ce3ac8/20261020T072317-616a68d97fff4afdb7eba7e3bd943656/outputs/metadata.json",
      "sha256": "47ca05e5b3c2a44196da3bbea259cc13a4f0aaa106db0118d32ea068c15a82cd",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-1/c189f987268df41f36e3dc9d5ad8468c44d7891eb52b3c8bff26ce8ac2ce3ac8/20261020T072317-616a68d97fff4afdb7eba7e3bd943656/outputs/qa.json",
      "sha256": "6ade3d28cee772116f151eaf88f96ab6f070c35acfa3e701aa9b5f5656f72274",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-1/c189f987268df41f36e3dc9d5ad8468c44d7891eb52b3c8bff26ce8ac2ce3ac8/20261020T072317-616a68d97fff4afdb7eba7e3bd943656/request.json",
      "sha256": "473a90cb79b569ebd11df313f7697265079927fea44cba49f608c51aff4d145f",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-1/c189f987268df41f36e3dc9d5ad8468c44d7891eb52b3c8bff26ce8ac2ce3ac8/20261020T072317-616a68d97fff4afdb7eba7e3bd943656/result.json",
      "sha256": "3846312f935a054e5e7eaab0232e3a7e780c906440de1ae9ac0d1bc5ba67ba45",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-2/2f1c7203979177b16d6bcf2b13b3c581e5af7af5cdb95b592f7e199a98f6c529/20261020T072321-d2e7ebe992ce425ab8766faf2fbeae02/outputs/gypsum-cave-flower.blend",
      "sha256": "ec9c4181dc132b57811651f7eba13abb7cda7362a37696b24a600667cc3a3679",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-2/2f1c7203979177b16d6bcf2b13b3c581e5af7af5cdb95b592f7e199a98f6c529/20261020T072321-d2e7ebe992ce425ab8766faf2fbeae02/outputs/gypsum-cave-flower.glb",
      "sha256": "8ddaf4c36f2fd0dbe7c3971c27c750e8c41760954a8fb25e9e40b679c24eac2b",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-2/2f1c7203979177b16d6bcf2b13b3c581e5af7af5cdb95b592f7e199a98f6c529/20261020T072321-d2e7ebe992ce425ab8766faf2fbeae02/outputs/metadata.json",
      "sha256": "4d0899c5ff3b0411eebeaa4ac08b744600293ccd6839428ca04f88b1892f1eeb",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-2/2f1c7203979177b16d6bcf2b13b3c581e5af7af5cdb95b592f7e199a98f6c529/20261020T072321-d2e7ebe992ce425ab8766faf2fbeae02/outputs/qa.json",
      "sha256": "00e16e5a67561f4fd6b4852de953ddf7abe44aaf933ca82ccbe5e8f478d820c1",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-2/2f1c7203979177b16d6bcf2b13b3c581e5af7af5cdb95b592f7e199a98f6c529/20261020T072321-d2e7ebe992ce425ab8766faf2fbeae02/request.json",
      "sha256": "6f076362c73d68d1811f319d4b5452bf8df498a0cff6126ea855d52d90684928",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/gypsum-cave-flower/r002/rebuild-2/2f1c7203979177b16d6bcf2b13b3c581e5af7af5cdb95b592f7e199a98f6c529/20261020T072321-d2e7ebe992ce425ab8766faf2fbeae02/result.json",
      "sha256": "c0c8a280f424118978883447266b8d352792d5045a018936c52813094beb8296",
      "origin": "source",
      "owner": "gypsum-cave-flower"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-1/210b2250f4f86099f7125619324b6450932e530e8b5a1e27e8a53ac585234521/20261020T072312-9967b1d9fb214947bec97271a26efa4b/outputs/metadata.json",
      "sha256": "53f93ede323e49083eed98711f4a211522094abcca76c555ae252f8a33acfc36",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-1/210b2250f4f86099f7125619324b6450932e530e8b5a1e27e8a53ac585234521/20261020T072312-9967b1d9fb214947bec97271a26efa4b/outputs/qa.json",
      "sha256": "b74bb5bc8e81111e36f343bbe0542fa60b32bb8a81f82160079b9d61eb5f905e",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-1/210b2250f4f86099f7125619324b6450932e530e8b5a1e27e8a53ac585234521/20261020T072312-9967b1d9fb214947bec97271a26efa4b/outputs/stalactite-group.blend",
      "sha256": "50810d5394f97e1475163b7a40652637c0802c944cad7d72fd5835b5b0d1c7ae",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-1/210b2250f4f86099f7125619324b6450932e530e8b5a1e27e8a53ac585234521/20261020T072312-9967b1d9fb214947bec97271a26efa4b/outputs/stalactite-group.glb",
      "sha256": "6e2bf795d94dae162a65dd8cf0924d70e402e28dbb1c17917d622919d608fca7",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-1/210b2250f4f86099f7125619324b6450932e530e8b5a1e27e8a53ac585234521/20261020T072312-9967b1d9fb214947bec97271a26efa4b/request.json",
      "sha256": "a56b1f386543b2257b034d18eedfcba72089801a6887d9100220362b1a21fa24",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-1/210b2250f4f86099f7125619324b6450932e530e8b5a1e27e8a53ac585234521/20261020T072312-9967b1d9fb214947bec97271a26efa4b/result.json",
      "sha256": "c07bce5c9985438db8c8d480dc57280d64c910c4316d9c6e4fb6acbd58800767",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-2/47c3cdf8fe9a9c86d23a6de02c4145cf4e004fdf4f4f482730424aefd2450fef/20261020T072315-438dfff693df47c08bb691ebbe055fe6/outputs/metadata.json",
      "sha256": "8f475d60aaba483d10f0cf9d55c87043c8e9d3e77a592feb8b4fc9ca99778e05",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-2/47c3cdf8fe9a9c86d23a6de02c4145cf4e004fdf4f4f482730424aefd2450fef/20261020T072315-438dfff693df47c08bb691ebbe055fe6/outputs/qa.json",
      "sha256": "e469676d5c0ecf1616a245c77762af8dbe5003a1b7024a804fb511bb7d96ab37",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-2/47c3cdf8fe9a9c86d23a6de02c4145cf4e004fdf4f4f482730424aefd2450fef/20261020T072315-438dfff693df47c08bb691ebbe055fe6/outputs/stalactite-group.blend",
      "sha256": "f8a4c3e5f5ddbd808886bfbee0a0cc3ca0df42b23c385fc0b0fe4e3d59662781",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-2/47c3cdf8fe9a9c86d23a6de02c4145cf4e004fdf4f4f482730424aefd2450fef/20261020T072315-438dfff693df47c08bb691ebbe055fe6/outputs/stalactite-group.glb",
      "sha256": "6e2bf795d94dae162a65dd8cf0924d70e402e28dbb1c17917d622919d608fca7",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-2/47c3cdf8fe9a9c86d23a6de02c4145cf4e004fdf4f4f482730424aefd2450fef/20261020T072315-438dfff693df47c08bb691ebbe055fe6/request.json",
      "sha256": "f48cc1ac254852088df6aa233ce2254423cbc807da21a8e185558ca888b0e5f8",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/build/stalactite-group/r002/rebuild-2/47c3cdf8fe9a9c86d23a6de02c4145cf4e004fdf4f4f482730424aefd2450fef/20261020T072315-438dfff693df47c08bb691ebbe055fe6/result.json",
      "sha256": "b23015158e170d5a70ce040a1335ca31a1c7b71fc90c32e1cae140459358f501",
      "origin": "source",
      "owner": "stalactite-group"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/runs/20261020T072304-d918434e6e1047b083b0c748cfb1b07d/manifest.json",
      "sha256": "bff9a5cfd80d12e7965d9252cc06f3a7e4cb62650a93ce8fd4321c7c4179bc6f",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round22-20261020/work/batch-59/rebuild-r002-runs/runs/20261020T072304-d918434e6e1047b083b0c748cfb1b07d/summary.json",
      "sha256": "c0a440c4c95fec5ab07ab9e58bb956bdee678d6dd1aca43f836cb2656bc2bcc4",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/QA-report.md",
      "sha256": "de1608a0e8fa90d519b6bd7aed1002c7bdb853631d57dbd1f7c5fb6d4680ae1e",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/erbenochile-candidate.json",
      "sha256": "fd0407a4a932a4d6909458c090564891bffcf3835da2430c2648774a4b0e8503",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/erbenochile-rebuild-1-independent.json",
      "sha256": "b938b15821c8dcf01536416bc3bec9d6ef865348f3abf093f8fd492590e245ca",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/erbenochile-rebuild-2-independent.json",
      "sha256": "24eb502df7137837ef85b8adea377c13c3ebdd97dc0c24eaa172296ef0d9b771",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/erbenochile-static.json",
      "sha256": "a1ab94d07c6345894f6533b997b12fd63de38b7952babc7b7e8c41118a227486",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/glacial-erratic-candidate.json",
      "sha256": "fad037718b23379060cb2ce658da01ab413df8209e167fc980daee05ee664fa3",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/glacial-erratic-rebuild-1-independent.json",
      "sha256": "7c8dfbc24965c9ad25706815a25e6612134debbc765cc76a9cf0c8382b43d8f5",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/glacial-erratic-rebuild-2-independent.json",
      "sha256": "59b0b0b190a68bb748889cb6a8547fd33698ea3e262bf45abdda963e1344e162",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/glacial-erratic-static.json",
      "sha256": "c93da88fc2668a0f147b3df2914c1aaa8e8c3e28a73ce3efeafb823f35b69364",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/gypsum-cave-flower-candidate.json",
      "sha256": "d6a995a64ac2a9b66800680be4f2fb120f7ab3048ab184d9075c2cc564eb87a9",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/gypsum-cave-flower-rebuild-1-independent.json",
      "sha256": "ffc30b8990f505e20ff8e17bf9aafeabc1088bae917c3ac0c0ebc36410045cdf",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/gypsum-cave-flower-rebuild-2-independent.json",
      "sha256": "94fe4daa5da85de8b592e9b74a821929f51d5f456ea767e090eca7d9b122ef35",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/gypsum-cave-flower-static.json",
      "sha256": "47b62eb3c97f8ce74813778047b5ef45a830743a04bb6ff6306701a396464869",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/khronos-validator.json",
      "sha256": "b0c76cd92f7d7e2350f38fc364ea51bdd0ab74e07063f00c710877a33087e8a9",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/parse.mjs",
      "sha256": "e6ff513682da71ea7c1385702e7548bdad49ecb27470f350f335422c08b2236c",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/rebuild-audit.json",
      "sha256": "e7fbfc6d2b50cbfafc7dbbb91ce8b131dc39c0c80b1f10356088015a69ea8f11",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/reopen_sources.py",
      "sha256": "6dd87bd3e0623e37d13373f5c4c6a3abe8e0439203c40d43fc8e923933688159",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/runtime-parse.jsonl",
      "sha256": "53e085f686a0769d944076eab0292ee86367b3dc5de15642d02cc8e31359ed9b",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/source-reopening.json",
      "sha256": "b3cf2032b6a6c8632096b14a1e69d5fecd1779be9efa2defa8b141cafc4a077d",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/source-reopening.log",
      "sha256": "30baf0690f418ed9c146d896735ee80207df3f392a7ba6a40a68982b50f9ab59",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/stalactite-group-candidate.json",
      "sha256": "5d15cba6b05166a8261412351c2ea1e847f071da415a1ddbf41cb022ee9de455",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/stalactite-group-rebuild-1-independent.json",
      "sha256": "ff4d1006448f4c7500c2c716edc91245ae396ebd08ba1a71cbd64d240f66ba03",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/stalactite-group-rebuild-2-independent.json",
      "sha256": "5b184a39cd2dd7102b8c4d1f1c8312f6574da6c1b2b0ebebaddaa03bfd035e6b",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/audits/stalactite-group-static.json",
      "sha256": "14dccb848787630b98eab60fbb65b30a0f0e74c035bc4b18ee0e065483d0054f",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/erbenochile-eight-views-contact.png",
      "sha256": "5ddb728003c7437f2cb0ab365f6a9ef4ed831d4c20588f64ed1925241d04552e",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/evidence-custody.json",
      "sha256": "3fe9ea28e306273b9c3ed4e727576f702d6deaeec7fd15c35a12c3e7067d7c54",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/glacial-erratic-eight-views-contact.png",
      "sha256": "b196c265ad53753bf41f58f9534fe529ef5296486573a7c49fa8111abcf299d7",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/gypsum-cave-flower-eight-views-contact.png",
      "sha256": "e764f64687de280e38f342a89cb10e0175c3348150489b10d703cfa59ded5241",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/independent-results.json",
      "sha256": "e962262db85cb26557a3c5723cd92012bce10e9d3899f90feee3c7d92f89c29e",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/pins-and-frames.json",
      "sha256": "df9f970e83ea4ae985986cb290568144ee67d0350be8523b23bc015fe8485bc6",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/pins-and-frames.stdout.json",
      "sha256": "df9f970e83ea4ae985986cb290568144ee67d0350be8523b23bc015fe8485bc6",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/stalactite-group-eight-views-contact.png",
      "sha256": "289ec8eff63f5722a9fd6cb2e8c72ef33abb8b0525cb862e2abb03b44cea754c",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-independent-20261020/verify_pins.py",
      "sha256": "dcee1423e6da55d9d8ec145a073b07da40d2fc9fe990315f83acff4d789f3ff0",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/capture/assets/card-previews/glacial-erratic-v2-768-q90.webp",
      "sha256": "e15860a7fbedadba147d9cbc9b3d5450149452571a2602a4954e873056d12218",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/capture/assets/card-previews/gypsum-cave-flower-v2-768-q90.webp",
      "sha256": "fbd93ded6a769d150575c20c406ab8afe6c6643290c97be9abf21a51b9c511a3",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/capture/assets/card-previews/stalactite-group-v2-768-q90.webp",
      "sha256": "f0b7af4113f9bf6162701be859ab8a47a9e8584211b2bf9cff012b74599346bb",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/capture/assets/turntables/index.json",
      "sha256": "e5bd58e972a3bfb450d21e8dc43dd5d19b68211d4a5fc2e0572dae03e0a35e70",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/capture/references/glacial-erratic.png",
      "sha256": "06cf6c4bffaae4506fa3e62b5c33fe399a7351811d98b612dfd178511613a695",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/capture/references/gypsum-cave-flower.png",
      "sha256": "5a16d53abeea289548fe6e7232520bb7223ce77b71e3f97b55ad093521d41c4d",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/capture/references/stalactite-group.png",
      "sha256": "18e04e45636d923193b3a9558649d64f8031fa59257eaa5b490c65bd0cebc586",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/capture/render-report.json",
      "sha256": "17fe72174a4c459ec7ba5bb602ec48bab23cf46113d6cc33213eb1930c37967b",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/capture-verification.json",
      "sha256": "420b42aa48a8e24456780cd1418f73154b6bf80baff54d34c4434dad48d04581",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/independent-card-review.json",
      "sha256": "515434e55d62dae9d65996894bb4d438fc4650ecc1a4d33f999018e9fa25c5e2",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch59-release-20261020/source-capture-review.md",
      "sha256": "14cbe9f91b6aa7c72a3ff87b72d51c398d3640f66142f3f84c11c63c94e10e83",
      "origin": "release",
      "owner": "$batch"
    }
  ]
};
