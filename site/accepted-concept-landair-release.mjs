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

/** Batch52/53 exact bounded release scopes; not formal profile acceptance. */
export const BATCH52_ORIGINAL_THREE_RELEASE = {
  "version": 1,
  "scope": "batch52-original-three-20261020",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "provider_generation_timestamp": "unknown",
  "source_commit": "110ec9772e1854ab9c4ccfa23848541b8e3aa1d7",
  "review_commit": "f3f793f6f9024d43453dbd302623c98eb34af5e7",
  "source_bundle": {
    "path": "qa/batch52-original-three-20261020/source-bundle.json",
    "sha256": "8eb6f0cfac97f536f15aafa882ac73b5dbaf49daa2e0c3799245473bef4103d9"
  },
  "review": {
    "path": "qa/batch52-independent-20261020/review-evidence.json",
    "sha256": "3331497ea393fb9dce15eae7449f26f65f95172b73f79a1d6b8779d571f8afc7"
  },
  "capture": {
    "report": {
      "path": "qa/batch52-original-three-20261020/capture/render-report.json",
      "sha256": "0143db47a04a3b357d9a03e6814b51a7b897321ee8acc4813c8e3441311e6e02"
    },
    "index": {
      "path": "qa/batch52-original-three-20261020/capture/index.json",
      "sha256": "9903a35e0e68a5e0846aa36d14ff43a567ba74375260eae3d75c4d382e57e516"
    },
    "packager_integrity": {
      "path": "qa/batch52-original-three-20261020/capture-integrity-verification.json",
      "sha256": "422d2e33d762e891336adec45b3299e8cdfd3329bf5da7807f30d590ca9984f4"
    },
    "projection_audit": {
      "path": "qa/batch52-original-three-20261020/capture-projection-audit.json",
      "sha256": "c0d16a5b11635d7fcd848cfd23b8f8d6076cb3c8e5d5ef23470228c9a5feca66"
    },
    "independent_review": {
      "path": "qa/batch52-original-three-20261020/capture-independent-review.json",
      "sha256": "c406877c97a32df7da4768916b267704dcb0ef14f6b12ca0f7cbe9e0d3bc2c1d"
    }
  },
  "additions": [
    {
      "id": "phoenicopsis",
      "revision": "r001",
      "source_commit": "110ec9772e1854ab9c4ccfa23848541b8e3aa1d7",
      "review_commit": "f3f793f6f9024d43453dbd302623c98eb34af5e7",
      "metadata": {
        "path": "assets/additions/phoenicopsis/batch52-20261020/release-metadata.json",
        "sha256": "47a8c0b604a14c4ac29a4e14bc9dff6c96753c3022cce632f1b8f619d1e67bd3"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/metadata.json",
        "sha256": "21bc06dd8b83fa435afaac4401c22638b05aad00510405e092cc776a3c27e193"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/candidate.json",
        "sha256": "09e4c25e081a8d146fa0bb0368c9a94821fc7529f6516a5dac036be7c1f0836d"
      },
      "review": {
        "path": "qa/batch52-independent-20261020/review-evidence.json",
        "sha256": "3331497ea393fb9dce15eae7449f26f65f95172b73f79a1d6b8779d571f8afc7"
      },
      "capture_reference": {
        "path": "qa/batch52-original-three-20261020/capture/references/phoenicopsis.png",
        "sha256": "dd36f2eb7a1168e1684282e00db7f96a8cfed2c8eb2d456a86c66f4ea5b13351"
      }
    },
    {
      "id": "cave-popcorn",
      "revision": "r003",
      "source_commit": "110ec9772e1854ab9c4ccfa23848541b8e3aa1d7",
      "review_commit": "f3f793f6f9024d43453dbd302623c98eb34af5e7",
      "metadata": {
        "path": "assets/additions/cave-popcorn/batch52-20261020/release-metadata.json",
        "sha256": "621d4dbe46fe6bc071473ae7537770854b8e7f139f7bd21e64953a699017724c"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/metadata.json",
        "sha256": "f8af1bac3b25830c60706a1e5b8c11dbbb0e954e6ca2b0a8a871aaeb9acf56f5"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/candidate.json",
        "sha256": "a1d8eff77bb6377e878206b5a549a546a23f0a4347784077775fc71bf9fb6d44"
      },
      "review": {
        "path": "qa/batch52-independent-20261020/review-evidence.json",
        "sha256": "3331497ea393fb9dce15eae7449f26f65f95172b73f79a1d6b8779d571f8afc7"
      },
      "capture_reference": {
        "path": "qa/batch52-original-three-20261020/capture/references/cave-popcorn.png",
        "sha256": "ecf6a89e452376834ee8d3f90968f16bedce9e43ac270e0538127f54aef34608"
      }
    },
    {
      "id": "curvolithus-trilobed-trail",
      "revision": "r001",
      "source_commit": "110ec9772e1854ab9c4ccfa23848541b8e3aa1d7",
      "review_commit": "f3f793f6f9024d43453dbd302623c98eb34af5e7",
      "metadata": {
        "path": "assets/additions/curvolithus-trilobed-trail/batch52-20261020/release-metadata.json",
        "sha256": "95a40ede3067feda3db7aaf7692c8f97b76f441726015001cfbb3c9682708bd9"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/metadata.json",
        "sha256": "62b7a607b68be7954063df24f27d23569f516e3eb815f24a2bcb726955e74e60"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/candidate.json",
        "sha256": "0935957783e8ab5eb24c1e72529effa8e97ba8e389ed80a9560ea93a09f5cc82"
      },
      "review": {
        "path": "qa/batch52-independent-20261020/review-evidence.json",
        "sha256": "3331497ea393fb9dce15eae7449f26f65f95172b73f79a1d6b8779d571f8afc7"
      },
      "capture_reference": {
        "path": "qa/batch52-original-three-20261020/capture/references/curvolithus-trilobed-trail.png",
        "sha256": "b6d3cb79a9c8b91e6251fa02171b11156bfc3171376e45db0ff91222f3811043"
      }
    }
  ],
  "files": [
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/brief-delivery.json",
      "sha256": "fa0b49cc36c4b7e5c21cb212556b744801e2e1b2961e4a4a036df8700a143062",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/brief-final.json",
      "sha256": "8693c8dd420de277e874f0e57b47e109c0468e1a678b23766bf0be8642fbf66f",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/brief.json",
      "sha256": "b22352d3bd1a795b8947d0e5afa19c7bd6bbbd7a9554faf5b3710374c0b8c4a4",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/brief.md",
      "sha256": "012330c8406e8bbf2fd96ad8699bd98441e49bd2696eb65920e1a259f97290c0",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/build-config.json",
      "sha256": "33b6f26c1f2b93288142a9a077dcb1738a1e9e1ebc86e3a3462297ff44fa258f",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/candidate-validation.json",
      "sha256": "a37c2d57797f6b6e72524e8a5ca778717662e71c167db22953d2a80d0346e913",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/candidate.json",
      "sha256": "a1d8eff77bb6377e878206b5a549a546a23f0a4347784077775fc71bf9fb6d44",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/cave-popcorn.blend",
      "sha256": "1fcf06b6d7ab810b7122a15f9ec1417e47405fa70f8a7834eafcfa7398bd4f3a",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/cave-popcorn.glb",
      "sha256": "36439f98c26784601b24ba4ac18c709f51c3ef9b071e0225438aaec42b7ba85b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/concept-evidence.json",
      "sha256": "20236b368ef508dcb571b96050d79261cc900c4bfa9e6def7f8993e174a8451b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/concept-validation.json",
      "sha256": "0ad3524ab9f30f90b414adf1dff9dfb1951340a91a7ba9cb20a99ab2d10b5bcf",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/generation-record.json",
      "sha256": "576d33d3bbee224d1f3122b736d799118e5bf2c05213e03a38072b95988f0571",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/generator.py",
      "sha256": "61aa3254749cd04670cdcf4cde05f7df2d76dfeeeb5e6b4c1f1ba287a4ec5332",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/gltf-validator.report.json",
      "sha256": "779abe1e66c8d750e574f3addbdb5b6c661ba709c67d7a744a45f4c9603e4884",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/measurements.json",
      "sha256": "14fb5754d1d27cc9ce50a2018e1bb56845694ace651517715a040b5d0f6e2ca8",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/metadata.json",
      "sha256": "f8af1bac3b25830c60706a1e5b8c11dbbb0e954e6ca2b0a8a871aaeb9acf56f5",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/original.png",
      "sha256": "1e615db7d008d4755c38707d10b49d9908b1493a2fce1e023dfd346268d833eb",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/profile-contract.json",
      "sha256": "c2fdfbed4f3b2cd78d91c8166cb3e1f18b380ae7be478263ac6a45e953d68ff5",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/prompt.txt",
      "sha256": "b01a697f9469468c18785dd540956cc027e8c5dce2ac296e4c619b5ed8a149f9",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/clay.png",
      "sha256": "f69dc7217e861e8f2e63ecfed5798c681fcdaa1a8e3963e9e3e013f4ea13de3e",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/front.png",
      "sha256": "9944980810827d822dd7c073c646069ff0bbb667ccee1bc12d855bcddaff1841",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/hero.png",
      "sha256": "5acf6dced4cfa3a30810b70298c46a2448603e4e98d3ad2054a9a49b448d2115",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/rear.png",
      "sha256": "1879a9d8f558db40d0d179cb230ee4a9ff20e95372b1d89a3d56f6441168febf",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/render-config.json",
      "sha256": "c06c2784729715f26b05e8b629b4ed63dc98a93aed8d5ced2d7e67257b930f35",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/render-manifest.json",
      "sha256": "ef157676987602410c9f22fe0a462e472150c538abfd22ffa9b9e10416126a43",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/reversehero.png",
      "sha256": "ebdabc013a4643bee9bb9418f1cdf407f5686bb2d02c7c53a9f64f175506ec9d",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/side.png",
      "sha256": "c49fed8062bd8dbe4c0bce8ae4801debddf1aee575e122f053f1ff41184dcb6e",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/silhouette.png",
      "sha256": "4d92ded86aa313bb6c5d07820fc5733c2dbf127a25a2a5ce32d6084d34418199",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/top.png",
      "sha256": "a82add70aea3379656ddf9990c45acf6b7fcc95eef9a24918e5b046eb4bb7800",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-delivery/turntable.json",
      "sha256": "7ea65b0e1b8b4de97d0682e965fa249bc4a3b21dffb54d53ded9491bc4d4b8d9",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/clay.png",
      "sha256": "9a9ba96460a308396c0468d9d515ccd951fe052b3cbea24eacd08cc4bc921b6b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/front.png",
      "sha256": "7984910ff9b3601293682ee747c9670637a41046b6432c2cc90b9427d0bf64e7",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/hero.png",
      "sha256": "a75f32402e9ba205e2c4e8e84d104da71a6babb7cfceef766a7d9e0839279f22",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/rear.png",
      "sha256": "e3877a0028f27cec716e1a90baea7c665bcd32482f215201988c4aae6e4faa5a",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/render-config.json",
      "sha256": "c06c2784729715f26b05e8b629b4ed63dc98a93aed8d5ced2d7e67257b930f35",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/render-manifest.json",
      "sha256": "a05b4c4557f5724be8fb9faf712005a0433d87db2721584134507f9df931f195",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/reversehero.png",
      "sha256": "860c69035e788d8f761d6681c3483d20f85c5bf92bc141666f1dc97f7e21d92d",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/side.png",
      "sha256": "feefe27d994452beaf023ae7b494c7165c6b99ee232c5843e17038d980e51f31",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/silhouette.png",
      "sha256": "94b91ef1155b36b9bfb94b5dc6a13851398b029a57970f3ef589177f88be9407",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/top.png",
      "sha256": "b6ed519ce9f8653dda233b4a028bb555c1607bbc1495edec0d8a7848b0c776a7",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof-final/turntable.json",
      "sha256": "7ea65b0e1b8b4de97d0682e965fa249bc4a3b21dffb54d53ded9491bc4d4b8d9",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/clay.png",
      "sha256": "edd1c078b0690a783a6a65293ed82e293a6577a61cef65ff7048a7b733817568",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/front.png",
      "sha256": "3a354479a202771582bc287c0e5e50a55a5a6652f9252665bfd0fc1f350867d6",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/hero.png",
      "sha256": "b585fa3fe4670a4bc412c992e6c582be83997a2414407a1b05752e969abdb18b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/rear.png",
      "sha256": "dc93cf53b9b8cfa7039f1be1d58da2896ee1e3d73d4c0d6fc667e53967219bc1",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/render-config.json",
      "sha256": "c06c2784729715f26b05e8b629b4ed63dc98a93aed8d5ced2d7e67257b930f35",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/render-manifest.json",
      "sha256": "d6a7f0170ee9052fb6dfc9fb2ea73c9ff2cc2e9ebcc6ef535e3a01609057a838",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/reversehero.png",
      "sha256": "5e93ca2549e906011a36b7d8a90d5a399e4fa4b1e4e91400e8f342272093e881",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/side.png",
      "sha256": "6ac7f5559b86fc2cb5b087f4ca08b5963ef08e9c69809535c8b9c5782d01b870",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/silhouette.png",
      "sha256": "83bfede1144d93a5fcf022ae52e591e93c5d1b6a4527ca0dc1afd19a50d59cff",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/top.png",
      "sha256": "51b0b30a4f7cd2460312043aa218ba3e1a149a8b8e326214e9cd32363da12fb8",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/proof/turntable.json",
      "sha256": "7ea65b0e1b8b4de97d0682e965fa249bc4a3b21dffb54d53ded9491bc4d4b8d9",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/qa.json",
      "sha256": "1b579aab4db09f214844598f70e3fa4219c71260d8c9e6921f2d4c06e430e5ab",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/rebuild-1.report.json",
      "sha256": "15c62748fab96294f35001b007752d4a9207217f91d46e5b1cda7c37cd383208",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/rebuild-2.report.json",
      "sha256": "59c9de1c72dc6924fa7e3af86a7ea5c5d72ee83f8749aae4ee6b3d3bdeca2b27",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/references.json",
      "sha256": "9bb4d2c3387a3ff6667eabf38d7ddd8c7e65700a7f9cf8c95bc80e4a10c9c515",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/review.md",
      "sha256": "1d98d65f4b1c7ab7e40acfe5c3e4fcb456f7f5b2b2878ddc231d4eaef955b808",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/source-export.report.json",
      "sha256": "07f649489372ac766a396504adfcda7917b436b647d52c851caf6adccf2c650e",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/static-glb.report.json",
      "sha256": "344888eab9ecf6e9a3cfc6cb75d3b0be4806a3b6eefc2ca1d5d33b878e0c66eb",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/technical.report.json",
      "sha256": "258366e27e0ee402f46bcc14d4124aa733528950ffd14fdf6595c672cb31d8b5",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/authoring-qa.json",
      "sha256": "c38f798a1c18af9ae7c3e8d54d3484ac9c5c459fa2761e4ae24026983bc23688",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/brief.json",
      "sha256": "81e38839bea00379be0a42048491a6fcffc2cb06923c511d7de241e9b5d2cebf",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/brief.md",
      "sha256": "0c3e5b5e7cf4fe819d3a33a1038870fa12d5ef0ba2dc724001eb9cd37893f065",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/build-config.json",
      "sha256": "a3fc3f021f7976f10e8918479b9785edd5c291cc4f247216243fdedce7254b3f",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/candidate-validation.json",
      "sha256": "467db672cbc63d3c602c7eced0704cc4760b49015fee1f1634a01d901466d378",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/candidate.json",
      "sha256": "0935957783e8ab5eb24c1e72529effa8e97ba8e389ed80a9560ea93a09f5cc82",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/curvolithus-trilobed-trail.blend",
      "sha256": "855e69c6679d20f4e63f7caa8a93e804f66cc386ae3b99759dce589067f0f9bf",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/curvolithus-trilobed-trail.glb",
      "sha256": "c07529a8856b679af1a1d3e816c37046076488ee926f7e38e70241f0cbefed22",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/generator.py",
      "sha256": "550c4041cce3be23fb28e7f70bd971c71c975a6ca09faac085fb5c8b304f9cad",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/gltf-validator.report.json",
      "sha256": "9493a64682bcfaa6eac2e32cd69a0f278d7901004b954e3c26c8f51402bd2ae7",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/metadata.json",
      "sha256": "62b7a607b68be7954063df24f27d23569f516e3eb815f24a2bcb726955e74e60",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/profile-contract.json",
      "sha256": "bad0776cb44b199b700189b30e4135be6855a7112940fa2733e6aa23f09a4515",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/clay.png",
      "sha256": "9aa3052fcd5fd5bf73504e8c073bebfc1136841da96c5fbbc5edc34cdc7e5d52",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/front.png",
      "sha256": "8e1c0038ca380174866682c34ae362e88a78a44a8d762f27f1b112148087149a",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/hero.png",
      "sha256": "91edff5e5be0002681ee1c9fa769cbc4c5cc63b5ae36c6b9ecfb91f46022bbd9",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/rear.png",
      "sha256": "da74065862c65a091012ed8205aef6d586f2d66f4947c32afa5e0bbf115f7bef",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/render-config.json",
      "sha256": "7ba75dbdf81b27e06cf4df2d738ac223ed59e09ba8db86b7f696d3dfaf87c3cb",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/render-manifest.json",
      "sha256": "a07be061c5ffef57ef4077765617ca0581093a27604f24b4ccb663b7b5fb6046",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/reversehero.png",
      "sha256": "a52c6017dbc826005cd69d177b195827f12b35fbe94116463f83029f0abcac2e",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/side.png",
      "sha256": "2e571f6bcc6cebe2f5daac6ed721b0bb7678b1da1a4b3ef2ec6f5e67148b31f0",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/silhouette.png",
      "sha256": "0a919576aa115849ff50bd51642473e6fedc841b325a881e0f699c6dc47f89ab",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/top.png",
      "sha256": "cc75dfc75b4c7754c19e49bc29d3bb6cff99975236d7a39bb02113ab6ab5cc4b",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-ledger-amendment/turntable.json",
      "sha256": "a886f71d9a67caca932f6bb16967f24e1b515a36a05cc3859f71cafed1677eae",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/clay.png",
      "sha256": "ee3f92b5afd47bf039b5e60779e45e64fbf108e6dcba05b257a0c39bcf7e2c10",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/front.png",
      "sha256": "818ac49d6ca4960a2670b6c449b24126d42a4cffb1c49a1135d958781ff2b911",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/hero.png",
      "sha256": "5ac86acca908017bb932b6fd98c51eae7f21db4cae60852e621f5f5a9780934b",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/rear.png",
      "sha256": "e872e443157f931f7ec2fe3ceb306c430ba39c0966577c7f745bddf53ce33c61",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/render-config.json",
      "sha256": "7ba75dbdf81b27e06cf4df2d738ac223ed59e09ba8db86b7f696d3dfaf87c3cb",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/render-manifest.json",
      "sha256": "ce9aa387e443b7a8d9bdc4a0f205d0f8625f012e69aee9c9c57031c4100a54d9",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/reversehero.png",
      "sha256": "6b75b420cdf73132f957e0569b723f42982b9de765ad9d79a079d146befac9ff",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/side.png",
      "sha256": "8c45c177a5023175289ae2a38ea4a134c5386257013b05e77d7e8d324baff6cf",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/silhouette.png",
      "sha256": "95377ca842cf81c8a535f8b1b15c69e085bf8fa16c1c9bf5731aadb12704b277",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/top.png",
      "sha256": "a56581be3186c7c6c24f4574d6c87a87d3a548861ea37912ab958496bb1e0e66",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof-pre-profile-amendment/turntable.json",
      "sha256": "a886f71d9a67caca932f6bb16967f24e1b515a36a05cc3859f71cafed1677eae",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/clay.png",
      "sha256": "2b5aad1d1cd2a21fcfcd6fb9322f3e5d1f08ac9160230621bf4f3307790d6527",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/front.png",
      "sha256": "408e88d2f4a292862ef7b8dcae5710b0bd880db5ecc7df3a14a5f253768aa057",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/hero.png",
      "sha256": "3b5a19601e1995474dd78a3b650f7c9d63a6f86b3c025c4b0d2d0d63bf9cd80b",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/rear.png",
      "sha256": "9841527c1b0fd05c230f421ae8eda507854c91f43c105e93bf2858397400b019",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/render-config.json",
      "sha256": "7ba75dbdf81b27e06cf4df2d738ac223ed59e09ba8db86b7f696d3dfaf87c3cb",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/render-manifest.json",
      "sha256": "bc6a9817aa4d538d57c0826a668ef97b281935620d0337f8f1fab6ad3e0e3585",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/reversehero.png",
      "sha256": "4b8720238d7ea22197f9d16c75538fab7e21c1365595cce55a9be0d084452ce7",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/side.png",
      "sha256": "824b4286e8308c9c1b1f72ea03c6e5dcf44f25b00071ec1b0503d71cdabd572d",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/silhouette.png",
      "sha256": "0e986b9ac4a9ae7c0d20c767319b7de49439425344cf44d4232f8404a7a5627e",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/top.png",
      "sha256": "2bdacf1c2cd32e248ac33f4de4c0b16515e10ac247e419dc2369f66fc6cf7366",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/proof/turntable.json",
      "sha256": "a886f71d9a67caca932f6bb16967f24e1b515a36a05cc3859f71cafed1677eae",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/qa.json",
      "sha256": "07c5e1db626a4063881fe7ca13f3d5e63ba9cf29541b1fdc55b979d587ddc656",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/rebuild-1.report.json",
      "sha256": "b3a2db2b8c447d4ca9f2868a923458c3440c6b29bcc2ee57bdb0d2c156d33a02",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/rebuild-2.report.json",
      "sha256": "9912f168bddd2957c4a3f43dc136536eb8f4bbbe07818ff86bc801c30aa99d8c",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/references.json",
      "sha256": "6a992a61c2296cbed9c33c41647c55841afdc45cc92b0a06c5c21c2b56ff70b3",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/render-fixed8.py",
      "sha256": "c1a7435fa83eb433e02a8abdc7dcdd000728e5baa0e0824c2c2cb41b89efb5df",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/source-export.report.json",
      "sha256": "e855c07ba2c0abf1ea131343ddf2de2a5a2578d2997c985bc8aba5b61920a563",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/brief.json",
      "sha256": "2e89b53f477701d08fd77334cd0e6a3ad4a164ee5fb9ac79cd06974745a01724",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/brief.md",
      "sha256": "d40c8eb81c4917e652771385085d733da12029c0736f295a0c03c91c4c0d1f20",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/build-config.json",
      "sha256": "71a010d10d06a4738bbe180def9ebda96623fad18e707609c062369679f339b2",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/candidate.json",
      "sha256": "09e4c25e081a8d146fa0bb0368c9a94821fc7529f6516a5dac036be7c1f0836d",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/concept-evidence.json",
      "sha256": "df0d7cddacafded13458326540c2bc8252c734b8203310161509db6ddfe7eeb0",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/evidence/rebuild1.json",
      "sha256": "2760220ed3fa8b4433650692bd7f4a0c535b2a892ee343adc41157cab6423bdf",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/evidence/rebuild2.json",
      "sha256": "0b155035fb5ad01a8b06baf9a16e73601047f91cdb18d7fbdf44805afa728edb",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/evidence/source-export.json",
      "sha256": "8834e2949d7d8b98937988dd0f6d9d2250aac127b7ab3c1eb915fdd325fb5378",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/evidence/static-glb.json",
      "sha256": "28a3d87bab310ba43fb674e6618bfec1efd9e667043823256a5afae2325e01a4",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/evidence/technical.report.json",
      "sha256": "ef72311ad9295bb1d3e01f8c6bc3839baf6d17e3495d4675bacaa19bc10f3405",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/generator.py",
      "sha256": "852bc3d259272c82cb02d0f42b9a1864cece682222baa84fb1c43f7d27032940",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/gltf-validator.report.json",
      "sha256": "ba9b9b15d7d927b9f9389fc3033c7551b7e0b148b2da41b5ba91fb8a3657538e",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/maker-inspection.md",
      "sha256": "da1640d4f8a60f14a15346b1d5594179efd35e2efd758ce3c59d7f691f0228eb",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/metadata.json",
      "sha256": "21bc06dd8b83fa435afaac4401c22638b05aad00510405e092cc776a3c27e193",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/phoenicopsis.blend",
      "sha256": "667f919e75ef8d1b0839bb9d494197646833d5160992d88b6364d6e72f02bcdd",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/phoenicopsis.glb",
      "sha256": "7e7fa939eeca8d1d0571ae1724faa7fa2387f03441bf0794fe4b269d666182d0",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/profile-contract.json",
      "sha256": "8d32347e9b629d95ec1b1028411f2dfe5edce4ae092121f9a41fbfad8814956f",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/clay.png",
      "sha256": "4328def3d4f8eb08c44f2f9bd7783b202fcf247ba4167f39973672ef592a5451",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/front.png",
      "sha256": "df994ca351f98490a5e956f6a274ecbdc7533a81ecc424957b5949ec8eb9a8d7",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/hero.png",
      "sha256": "604d332784f716f8843e0756f4ca1f0dd10939260dd2b0e87b0b86e294bd1590",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/rear.png",
      "sha256": "37ffc1160702dec0de3cb2a817e8ad890078c98e226e06208ec8dcb8caab62a3",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/render-config.json",
      "sha256": "b144f295716630e8935f7063bb3f4c3ec1186dfafa416d7f773b2b5ee8184b41",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/render-manifest.json",
      "sha256": "4afe8f85e4ef78c6f9342285315fa888bd0e6e74d95921afac538bd6d2083f60",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/reversehero.png",
      "sha256": "e170c7a2daab1b229258152052c5cd003d05d14f234e49ee185ad38513b0c90b",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/side.png",
      "sha256": "1daa73446b5804249e9d4cee45babb8ad7514e0b444f4bdf1e16f36087c7ab90",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/silhouette.png",
      "sha256": "f982f96b36ef0dbc6b7d7e5d22fbccac916711ead4ea8679749bda7a015cdcfc",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/top.png",
      "sha256": "aa27f578f25f22775e3868e2f169dedf6862b2edcbb5cbaed9e2d1faa5fd8b47",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/proof/turntable.json",
      "sha256": "232c02434266fc6f572e79046381e90f96f10c4a9427501ecd3ee10b22d1064b",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/qa.json",
      "sha256": "7f6a0b1d0d8a5ff104cf9a9f76949dc69b3aba8b61270c0e382120e48314052f",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/references.json",
      "sha256": "e8058e4dc7ddbab90d7d348ba067bc35f75c6ab31a107021a0f40d7441668d3a",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/source-counts.json",
      "sha256": "00edffa177927624e4fbfeb9dcdca10186be6b5a8c713f17a50cecaccd43e1e8",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/ATURIA-R003-QA-RETURN.md",
      "sha256": "715b1471c7673f5c32d98c14a6ed6180de32259fadc905ea2a56ad4a06363d6d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/HANDOFF.json",
      "sha256": "f3efbadf65f524d277be98fd692775b022b4576923432f7a2d53a5e90247f29e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/README.md",
      "sha256": "3d92944eb21fa8eda0a4ddba941ddd1cb6959b16852265bf382e19bb95685754",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia-r003-coordinator-checks.json",
      "sha256": "6815fad7c021afb67010c9cf5b6fdb79a9e76ea201a405e7aa0796110883549a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia-r003-protected-files.json",
      "sha256": "45f8671579826f7b1efab16e985247a1d2b316a433e7a204f7d5ea0924fdcfc9",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia-r003-repair-claim.json",
      "sha256": "df7b4a6c2c7514f960fa86e3e14acc9cac6077e5e1b1a527b79a473e2771def7",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia-supplemental-final.json",
      "sha256": "4069dab10f8b5fccea0dadcea7df2176ce3820aac8d08c309ef851d4d88dc012",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia-supplemental-path-attempt.json",
      "sha256": "b6b232ef3f766bab020db53ac420ce1030272d21cc70fb06b32a8f880343af16",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn-supplemental-final.json",
      "sha256": "0ad3524ab9f30f90b414adf1dff9dfb1951340a91a7ba9cb20a99ab2d10b5bcf",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/HANDOFF.json",
      "sha256": "3f864c7f95bbae0fc331e868fe9d18821449b0e0430796b43f85d8d550c337b9",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/build.log",
      "sha256": "ef2db0a2b29f811ad34d5c1b9a86a1f09a50b763f8f652301d8c504c4edcd0bc",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/build/cave-popcorn/cave-popcorn.blend",
      "sha256": "1bf8efddd9c34c396e50763eab7d436fc1d165b959a80a0bde00f4879a8bc4ba",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/build/cave-popcorn/cave-popcorn.glb",
      "sha256": "632cd423e346082d424d33323955635381a20e5b19be7ec663a5afdfda8ddebb",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/build/cave-popcorn/metadata.json",
      "sha256": "1ba3005d8ee441e1c01c46210ae34d20a0eb4ca4aeb8ddf88b40da7684049f57",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/build/cave-popcorn/qa.json",
      "sha256": "8fdd6120e7e5a43a297a6cfa41df2efb62463687dd847d3a14f5cea03fd15596",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/candidate-validation.json.stderr",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/concept-validation.json.stderr",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/concepts/generation-record.json",
      "sha256": "576d33d3bbee224d1f3122b736d799118e5bf2c05213e03a38072b95988f0571",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/concepts/original.png",
      "sha256": "1e615db7d008d4755c38707d10b49d9908b1493a2fce1e023dfd346268d833eb",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/concepts/prompt.txt",
      "sha256": "b01a697f9469468c18785dd540956cc027e8c5dce2ac296e4c619b5ed8a149f9",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/handoff-hashes.json",
      "sha256": "e74570fbbc5be8ad3c8c9900410b126c166265b224f473a2469f95ded94d42a1",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/modeling-freeze.json",
      "sha256": "27a5b80e08ecd7eb30f24876f12f7f724885ae512aa54ba59525a800076fe4bf",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/package-r002.py",
      "sha256": "7982f5c202a7f3fb5417bf76603181931897c6610d8acacc6c0014ed0c0f5229",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/package-r003.py",
      "sha256": "596ce6050ddc64cd69d2152aad23684e59f8ee160395d8b57446df851b403161",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/prepare.py",
      "sha256": "aa0bca86078cb5a21235f59c9e11beffe95a23ff95f286f440bb7832e2fa2420",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/profile-contract.json.stderr",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/proof-retry.log",
      "sha256": "f988e8cdca0e0eded5fa5918451f7fa9b59ae2023bbe5240ffcefcf351663f56",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/proof.log",
      "sha256": "74cd08148cf6f9e07b37fde6af1993e403c781333ce184768850c1d32225c372",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-jobs.json",
      "sha256": "56e572e3c64052bb1b20e43c5ec7768c4d26f40557b9207fc5bc0b68dcf0cc29",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/build/cave-popcorn/r002/initial-build/dae45eff35b7f57375836e9755d59f758b8ea1ded2feaeb716f2fc9021fafcd8/20261020T001315-9d8a7deac25f478380f2ab4a78ce1af8/outputs/cave-popcorn/cave-popcorn.blend",
      "sha256": "17c95df14c9b263f6e8d46544b4bf9c5905723aa11345da33babc2ebc48397f3",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/build/cave-popcorn/r002/initial-build/dae45eff35b7f57375836e9755d59f758b8ea1ded2feaeb716f2fc9021fafcd8/20261020T001315-9d8a7deac25f478380f2ab4a78ce1af8/outputs/cave-popcorn/cave-popcorn.glb",
      "sha256": "e5eb0f51d07cf4c138a56a9f6baab309ce004e138241d6acf5a7843c9fe69efc",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/build/cave-popcorn/r002/initial-build/dae45eff35b7f57375836e9755d59f758b8ea1ded2feaeb716f2fc9021fafcd8/20261020T001315-9d8a7deac25f478380f2ab4a78ce1af8/outputs/cave-popcorn/metadata.json",
      "sha256": "bf8cc9ad8c5ccd5eb35a5281bde30c9123c8d635b7bbcda6ec59ad946abe02c4",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/build/cave-popcorn/r002/initial-build/dae45eff35b7f57375836e9755d59f758b8ea1ded2feaeb716f2fc9021fafcd8/20261020T001315-9d8a7deac25f478380f2ab4a78ce1af8/outputs/cave-popcorn/qa.json",
      "sha256": "3809cbdc9293f8bd26f6568cfe58ff8ef74c3053c812b16c7471ea22df4f3c5b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/build/cave-popcorn/r002/initial-build/dae45eff35b7f57375836e9755d59f758b8ea1ded2feaeb716f2fc9021fafcd8/20261020T001315-9d8a7deac25f478380f2ab4a78ce1af8/request.json",
      "sha256": "29ba4b238c1c217dd34668c8e4796c7f2a3397d37a26a04049b989f33549ab07",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/build/cave-popcorn/r002/initial-build/dae45eff35b7f57375836e9755d59f758b8ea1ded2feaeb716f2fc9021fafcd8/20261020T001315-9d8a7deac25f478380f2ab4a78ce1af8/result.json",
      "sha256": "042f8a353e0c6fb05f31ee5872f36d7440c65cb482c597385f87c9e82d653bff",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/build/cave-popcorn/r002/initial-build/dae45eff35b7f57375836e9755d59f758b8ea1ded2feaeb716f2fc9021fafcd8/20261020T001315-9d8a7deac25f478380f2ab4a78ce1af8/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/build/cave-popcorn/r002/initial-build/dae45eff35b7f57375836e9755d59f758b8ea1ded2feaeb716f2fc9021fafcd8/20261020T001315-9d8a7deac25f478380f2ab4a78ce1af8/stdout.log",
      "sha256": "f4f9279182e034eecf1c8564a486828a5ecce1791fca4706cf914cf50d233e15",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/runs/20261020T001315-854e1b9b2e8a4e798dff594311b67b6c/manifest.json",
      "sha256": "41fb782d18792c9e282ebc0495fc092a31156dd373ee0d42d24f03a894953bd8",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build-runs/runs/20261020T001315-854e1b9b2e8a4e798dff594311b67b6c/summary.json",
      "sha256": "d734153351787b340e04e97851de9d39f26e16638af9b7fcb66f4405332953d5",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-build.log",
      "sha256": "bccbd721ee1430a13678ba6bf11dd2660f2077916c05cd439b5b78aa8349c940",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-khronos-execution.json",
      "sha256": "280ea85d39c1d0e24035e792068f051dcf06d4a4186d8377e54bf20a69ed2c61",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-khronos.log",
      "sha256": "652217d8d2d3de871773844248b6104279078207dcab1a6f974309600195daef",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-modeling-freeze.json",
      "sha256": "1a24820653c71e43b66faac3ffd3eb16f8b9388cbca5c022dc7e75a5f9bf61eb",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-1-comparison-execution.json",
      "sha256": "2364c857531e9ff2e7326176fe31d764a90759e213305a3bf0385bbd5323a086",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-1-comparison.log",
      "sha256": "1b88f8be4868fcf0409ad71367d68b22d17b65b801902224476bb01c1c00e0dc",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-2-comparison-execution.json",
      "sha256": "b2e9e952bf22ca27d75c207aa9a6154526e6482bd248dbffcfa91735f825e5dc",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-2-comparison.log",
      "sha256": "72ad643d3f3dcba4dcf345068121d53fa17d3dc7ac74061eb3e7c86f5eccf24b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-execution.json",
      "sha256": "e7dd8dc6852bad186ea32c3d552e63f1150fb955f3d25627ae73246e5aed9669",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-jobs.json",
      "sha256": "7114f4ce88b7bf58a954f1a0693189b6fe0c686a58f021a39f5de7749ac6d54c",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-1/ada072c093890e62a366bce00d1c14e296abe4405bad50f9400e0c15a5d0e70d/20261020T001420-a1ad0f81c0fa4a3eb54fd249997823d0/outputs/cave-popcorn/cave-popcorn.blend",
      "sha256": "42ba038b2d6cfca4ae6593f69544b4ef9cae8f2f173cc8430add1e0bad80f5bd",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-1/ada072c093890e62a366bce00d1c14e296abe4405bad50f9400e0c15a5d0e70d/20261020T001420-a1ad0f81c0fa4a3eb54fd249997823d0/outputs/cave-popcorn/cave-popcorn.glb",
      "sha256": "e5eb0f51d07cf4c138a56a9f6baab309ce004e138241d6acf5a7843c9fe69efc",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-1/ada072c093890e62a366bce00d1c14e296abe4405bad50f9400e0c15a5d0e70d/20261020T001420-a1ad0f81c0fa4a3eb54fd249997823d0/outputs/cave-popcorn/metadata.json",
      "sha256": "aaf531e2f94667d22c5592d5ea5c7672b95335f6ab919b6afc2de40e7e0581f9",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-1/ada072c093890e62a366bce00d1c14e296abe4405bad50f9400e0c15a5d0e70d/20261020T001420-a1ad0f81c0fa4a3eb54fd249997823d0/outputs/cave-popcorn/qa.json",
      "sha256": "4bc0f927b121eea43f3295e9f5b41f20000971e1a1760ec71ae70246160f2def",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-1/ada072c093890e62a366bce00d1c14e296abe4405bad50f9400e0c15a5d0e70d/20261020T001420-a1ad0f81c0fa4a3eb54fd249997823d0/request.json",
      "sha256": "7167ca6d38d82f348611945bf733666d9f5504083f4e5b32059bbb4eacff6f15",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-1/ada072c093890e62a366bce00d1c14e296abe4405bad50f9400e0c15a5d0e70d/20261020T001420-a1ad0f81c0fa4a3eb54fd249997823d0/result.json",
      "sha256": "e8757071ac76dc73d623d639498ed3bf0733ed96365f40b6133c991d6881aa59",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-1/ada072c093890e62a366bce00d1c14e296abe4405bad50f9400e0c15a5d0e70d/20261020T001420-a1ad0f81c0fa4a3eb54fd249997823d0/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-1/ada072c093890e62a366bce00d1c14e296abe4405bad50f9400e0c15a5d0e70d/20261020T001420-a1ad0f81c0fa4a3eb54fd249997823d0/stdout.log",
      "sha256": "85eff692338db9d64343b7828f5ca97a5b83999d55a5c2011c7d31e360d340db",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-2/1c2f32880b6cc09ec5b3f36705b68c1df75dd712069ead03d7867e2cf1ac66e7/20261020T001422-cbe8f706ee38444ab56c0049a8240ed1/outputs/cave-popcorn/cave-popcorn.blend",
      "sha256": "dd7e9969d9b696cb8b8347a2483ac8090dd68491a8bfa46f1e32b8a0cddd095f",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-2/1c2f32880b6cc09ec5b3f36705b68c1df75dd712069ead03d7867e2cf1ac66e7/20261020T001422-cbe8f706ee38444ab56c0049a8240ed1/outputs/cave-popcorn/cave-popcorn.glb",
      "sha256": "e5eb0f51d07cf4c138a56a9f6baab309ce004e138241d6acf5a7843c9fe69efc",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-2/1c2f32880b6cc09ec5b3f36705b68c1df75dd712069ead03d7867e2cf1ac66e7/20261020T001422-cbe8f706ee38444ab56c0049a8240ed1/outputs/cave-popcorn/metadata.json",
      "sha256": "9ee601778883176e53385d57a7eb4f1727673f81abd5cd4dadce09f3fbccf7e8",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-2/1c2f32880b6cc09ec5b3f36705b68c1df75dd712069ead03d7867e2cf1ac66e7/20261020T001422-cbe8f706ee38444ab56c0049a8240ed1/outputs/cave-popcorn/qa.json",
      "sha256": "494b69a2617cf87aafee4761e5f3f1bc2c8116ce3e53b2382f72b6c8a22cdb21",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-2/1c2f32880b6cc09ec5b3f36705b68c1df75dd712069ead03d7867e2cf1ac66e7/20261020T001422-cbe8f706ee38444ab56c0049a8240ed1/request.json",
      "sha256": "4414b260395a1aabb2f95c7f3d3dad6827145616213d95f6c22cd0e838b2a193",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-2/1c2f32880b6cc09ec5b3f36705b68c1df75dd712069ead03d7867e2cf1ac66e7/20261020T001422-cbe8f706ee38444ab56c0049a8240ed1/result.json",
      "sha256": "6a1037c6c7b5eece6e01037c873309740a69020ce0c8eec4e06ff2c7b4891ac8",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-2/1c2f32880b6cc09ec5b3f36705b68c1df75dd712069ead03d7867e2cf1ac66e7/20261020T001422-cbe8f706ee38444ab56c0049a8240ed1/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/build/cave-popcorn/r002/rebuild-2/1c2f32880b6cc09ec5b3f36705b68c1df75dd712069ead03d7867e2cf1ac66e7/20261020T001422-cbe8f706ee38444ab56c0049a8240ed1/stdout.log",
      "sha256": "364f9b7c2891ab47f652e83d19fa0bbe2252b970a3386f023984e2d01bc1a210",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/runs/20261020T001420-d790df11412d4fa294c39dd732e25b28/manifest.json",
      "sha256": "e8df97fb6b44976b264d8add4ec35262860ed5612c6386d38470126e4b5180eb",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild-runs/runs/20261020T001420-d790df11412d4fa294c39dd732e25b28/summary.json",
      "sha256": "00aa3c7f6a6b534efa022c395b365ec2d473becc8d35ddb60cd84bf536bd0069",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-rebuild.log",
      "sha256": "66e26d148c43d08c92e9c0f9a5d1d6d8068949891855039c145446b8a9c49c15",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-render-execution.json",
      "sha256": "37cb1df1b977f6711d786230325e5d2cfb45df77bf2006b27d4d6236cb47af67",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-render.log",
      "sha256": "94afba567240a150ed47617bc1a2440a1602d7de933e3c20d7532ff6877b2c29",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-source-reopen-execution.json",
      "sha256": "56afccf06937e80823ae6bf7fa2d8ebe6250743f87d886fce3447ab5651cd79b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r002-source-reopen.log",
      "sha256": "c997800fe71e978b8ab8087657a603906ce184d639addec3f539c0b5225195fd",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-jobs.json",
      "sha256": "0c2186b9219aef600d41b7a35732264cd6455cf5f8dfb24205d4e1bc180f3ccc",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/build/cave-popcorn/r003/initial-build/7b1e623afddfcc9b4311bc62eb52c222678f68362a239f233a01fe640f211dfd/20261020T001517-cca83638cb074379a5fc3d1b06835fbc/outputs/cave-popcorn/cave-popcorn.blend",
      "sha256": "1fcf06b6d7ab810b7122a15f9ec1417e47405fa70f8a7834eafcfa7398bd4f3a",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/build/cave-popcorn/r003/initial-build/7b1e623afddfcc9b4311bc62eb52c222678f68362a239f233a01fe640f211dfd/20261020T001517-cca83638cb074379a5fc3d1b06835fbc/outputs/cave-popcorn/cave-popcorn.glb",
      "sha256": "36439f98c26784601b24ba4ac18c709f51c3ef9b071e0225438aaec42b7ba85b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/build/cave-popcorn/r003/initial-build/7b1e623afddfcc9b4311bc62eb52c222678f68362a239f233a01fe640f211dfd/20261020T001517-cca83638cb074379a5fc3d1b06835fbc/outputs/cave-popcorn/metadata.json",
      "sha256": "1736e04b365c4ad7ca20885aa7c51382146a092619c3089d854c84a17df54d9f",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/build/cave-popcorn/r003/initial-build/7b1e623afddfcc9b4311bc62eb52c222678f68362a239f233a01fe640f211dfd/20261020T001517-cca83638cb074379a5fc3d1b06835fbc/outputs/cave-popcorn/qa.json",
      "sha256": "ac37bb637e94cb25907cff7d2180d738b84658d8137dfd2f9fbac5a700491676",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/build/cave-popcorn/r003/initial-build/7b1e623afddfcc9b4311bc62eb52c222678f68362a239f233a01fe640f211dfd/20261020T001517-cca83638cb074379a5fc3d1b06835fbc/request.json",
      "sha256": "c00ffc4e2a56712d116d6ba218de068fee0b17785723af8fbd6ed684800ccd54",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/build/cave-popcorn/r003/initial-build/7b1e623afddfcc9b4311bc62eb52c222678f68362a239f233a01fe640f211dfd/20261020T001517-cca83638cb074379a5fc3d1b06835fbc/result.json",
      "sha256": "cb371fc11c683ce5e6ea34a3a8084266eba175f26126b6d220385ca8b93572e7",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/build/cave-popcorn/r003/initial-build/7b1e623afddfcc9b4311bc62eb52c222678f68362a239f233a01fe640f211dfd/20261020T001517-cca83638cb074379a5fc3d1b06835fbc/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/build/cave-popcorn/r003/initial-build/7b1e623afddfcc9b4311bc62eb52c222678f68362a239f233a01fe640f211dfd/20261020T001517-cca83638cb074379a5fc3d1b06835fbc/stdout.log",
      "sha256": "b95106ba1bc008230ce15dbb5d6bf384f424fa7e94fc79fa095898e9a8511559",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/runs/20261020T001517-9152cfe297264570a6b25d54a391917e/manifest.json",
      "sha256": "fd82df8cc269c814c53b139317eae2e1e5b9001225704447e210be7a6f41e5e0",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build-runs/runs/20261020T001517-9152cfe297264570a6b25d54a391917e/summary.json",
      "sha256": "a8855d22201ea09042c4d31d75cdf033493286664213909bd9ab77edd57d4a7f",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-build.log",
      "sha256": "a5a69078e121331445e2772f226f5cb68e6e1dd7416bbf2142ab8caa85802b60",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-delivery-render.log",
      "sha256": "640632e32f50cc2b265ea19d550157e50cb5cecbb76c9aaa3d2c5b2bdb124f08",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-final-render.log",
      "sha256": "007a97d529c4a7b141db1a405671de2a6dcd7cb28bd5fa4a155eb176a0910951",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-khronos-execution.json",
      "sha256": "7ab105304657848a9faf269908a90bfbf945e4b219b00355d37bacfc3cefa210",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-khronos.log",
      "sha256": "7361252631fb250b494ce4ed81fdf1280344fd7e9b44e702cb2cbc1eba8d045a",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-modeling-freeze.json",
      "sha256": "0a53bbba03e68ce38015fbd356a6f134717f895f51576acbca3c2f319b337185",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-packaging-amendment.json",
      "sha256": "61566dd00163b0698bae924db0193b1337dd82ac77f46fbb2bdd519f7c3e7591",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-1-comparison-execution.json",
      "sha256": "05a4141867760d08e61819b5da48765256ecf0237eaaa52ac16e03781cfcca5c",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-1-comparison.log",
      "sha256": "15c62748fab96294f35001b007752d4a9207217f91d46e5b1cda7c37cd383208",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-2-comparison-execution.json",
      "sha256": "e0fbfcfd68b1d5409d092350877c30be21badafd3099bd969b0b6a6fda1cbcf6",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-2-comparison.log",
      "sha256": "59c9de1c72dc6924fa7e3af86a7ea5c5d72ee83f8749aae4ee6b3d3bdeca2b27",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-execution.json",
      "sha256": "bccbfcb2cd02ace28f64fa85439dcba764c19635c15ed0a9f2ea1d194f2c3fd5",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-jobs.json",
      "sha256": "946d71705ebb86be7e0883c2180c778833f8398a5677ab27ebd6cc3f12405bba",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-1/5f83a4248cf71c137424641b27cb7ced125f782a62975a57186689b3f5d9d2a9/20261020T001537-d2f8e83922fe4fc18f444be7327c5159/outputs/cave-popcorn/cave-popcorn.blend",
      "sha256": "9520c966d07b4f15fcaa3bb52c8b69eb1e9c9f73daca4ba63d65dbe04e1a2fd8",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-1/5f83a4248cf71c137424641b27cb7ced125f782a62975a57186689b3f5d9d2a9/20261020T001537-d2f8e83922fe4fc18f444be7327c5159/outputs/cave-popcorn/cave-popcorn.glb",
      "sha256": "36439f98c26784601b24ba4ac18c709f51c3ef9b071e0225438aaec42b7ba85b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-1/5f83a4248cf71c137424641b27cb7ced125f782a62975a57186689b3f5d9d2a9/20261020T001537-d2f8e83922fe4fc18f444be7327c5159/outputs/cave-popcorn/metadata.json",
      "sha256": "6caf0d10bc344a45ad68e7aaad3474523ceeb18f03022fb9025fb7be3eeeac8c",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-1/5f83a4248cf71c137424641b27cb7ced125f782a62975a57186689b3f5d9d2a9/20261020T001537-d2f8e83922fe4fc18f444be7327c5159/outputs/cave-popcorn/qa.json",
      "sha256": "b0ca45ccf251b9b96a610f038b14a76683226f21a13c9697d4c831fb3a1820bd",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-1/5f83a4248cf71c137424641b27cb7ced125f782a62975a57186689b3f5d9d2a9/20261020T001537-d2f8e83922fe4fc18f444be7327c5159/request.json",
      "sha256": "4a643629ed1326a300370c629bc1310cd7df20d42918ea49841a39ad6a8492ee",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-1/5f83a4248cf71c137424641b27cb7ced125f782a62975a57186689b3f5d9d2a9/20261020T001537-d2f8e83922fe4fc18f444be7327c5159/result.json",
      "sha256": "eff83cdf9d467f789bb4304028c562f55a8e3e3c1e027eec7541b41047cc0bc5",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-1/5f83a4248cf71c137424641b27cb7ced125f782a62975a57186689b3f5d9d2a9/20261020T001537-d2f8e83922fe4fc18f444be7327c5159/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-1/5f83a4248cf71c137424641b27cb7ced125f782a62975a57186689b3f5d9d2a9/20261020T001537-d2f8e83922fe4fc18f444be7327c5159/stdout.log",
      "sha256": "81116b80be6675e045d1daa5dfeeb51447c1155af7c7bd0c6797d6f8bf004bbc",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-2/8935c150e6f3e08eac753695a98aa29404a97a26aa1c97eec1300f6b5ee6e65a/20261020T001541-82e967c8611b448ca3f4915d634ac1f4/outputs/cave-popcorn/cave-popcorn.blend",
      "sha256": "0ba522c6663c9745fa594b8f6a894a5d5359c5421c70cb216ac1ddb3bd9c3ee8",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-2/8935c150e6f3e08eac753695a98aa29404a97a26aa1c97eec1300f6b5ee6e65a/20261020T001541-82e967c8611b448ca3f4915d634ac1f4/outputs/cave-popcorn/cave-popcorn.glb",
      "sha256": "36439f98c26784601b24ba4ac18c709f51c3ef9b071e0225438aaec42b7ba85b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-2/8935c150e6f3e08eac753695a98aa29404a97a26aa1c97eec1300f6b5ee6e65a/20261020T001541-82e967c8611b448ca3f4915d634ac1f4/outputs/cave-popcorn/metadata.json",
      "sha256": "427b84e56afb93bf826a1cf7509b8214f667296df5deb38e85baa29b4c78780e",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-2/8935c150e6f3e08eac753695a98aa29404a97a26aa1c97eec1300f6b5ee6e65a/20261020T001541-82e967c8611b448ca3f4915d634ac1f4/outputs/cave-popcorn/qa.json",
      "sha256": "52aef2ff204b4f76e5484f03c1e780dd340155652df915d15524ab5931026a24",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-2/8935c150e6f3e08eac753695a98aa29404a97a26aa1c97eec1300f6b5ee6e65a/20261020T001541-82e967c8611b448ca3f4915d634ac1f4/request.json",
      "sha256": "46eac58dbe6fb58e403796db7a4cd298e23dc5a628331cb76fea0d4ce72a7f26",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-2/8935c150e6f3e08eac753695a98aa29404a97a26aa1c97eec1300f6b5ee6e65a/20261020T001541-82e967c8611b448ca3f4915d634ac1f4/result.json",
      "sha256": "27cd1035a8d4064c2f1e4bbd62c42bfe9574c68dfcebffad773ad3a2439c81b9",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-2/8935c150e6f3e08eac753695a98aa29404a97a26aa1c97eec1300f6b5ee6e65a/20261020T001541-82e967c8611b448ca3f4915d634ac1f4/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/build/cave-popcorn/r003/rebuild-2/8935c150e6f3e08eac753695a98aa29404a97a26aa1c97eec1300f6b5ee6e65a/20261020T001541-82e967c8611b448ca3f4915d634ac1f4/stdout.log",
      "sha256": "e15a0187d95185b317a047f1f6cb5242c8d78ac2ab8fa1fb9a64e0d90badc716",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/runs/20261020T001537-784e9469d6d1457f90fccee5ccf30937/manifest.json",
      "sha256": "c816d6977b05058f3cbe7d0125148603e641955df710f76bd1bda446228837a5",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild-runs/runs/20261020T001537-784e9469d6d1457f90fccee5ccf30937/summary.json",
      "sha256": "e2ec361b4eb11010c5388b59421321cedbdcf88bc0d02d75dc0545698193f5c8",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-rebuild.log",
      "sha256": "9ef49e819d1781c974bb2bf2a8a5fd4232e8aed2f732226dddff9a53f1f40d07",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-render-execution.json",
      "sha256": "3a7416aad4393fb170e94e1764785051092235aec53a672cb6a0d5f99738ada7",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-render.log",
      "sha256": "32dbc2f8e0b47e497552156f9225b896c11c7f534ccb23e5cad5b3d4b64e4dce",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-source-reopen-execution.json",
      "sha256": "0a49f78f0ca7e468a35a5c3ec1fe96b0ce2cac11297264829b33645a971903a2",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/r003-source-reopen.log",
      "sha256": "14bd28929c33f638396d2ee4f31b8e69fc8e450ba53b06d0ca1da69c01ffc1f6",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-1-comparison.log",
      "sha256": "0a7c227af224e3db567982a216157f0b32ecc1daa57407bc90d8b1e309f225f1",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-2-comparison.log",
      "sha256": "056da29c78f0979fd57cd881a75272d7689a6ca56c75460fd420bfb8ce6d8a92",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-jobs.json",
      "sha256": "7184f1f9724aceb80a7f2d76764209d5bad59fb49ee66f3b5514cd6c83b2050e",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-1/244ad9fa6dec2dc9373e30c7781bbd7a96cfb51cee75111aca4f548ed417b9d8/20261020T001214-e3ca50e1753c4cf9b5179aba95576ed4/outputs/cave-popcorn/cave-popcorn.blend",
      "sha256": "78bbb4d4b6c11b4389b3b309732836c83de05fe57d9eaddc54832a553b76730b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-1/244ad9fa6dec2dc9373e30c7781bbd7a96cfb51cee75111aca4f548ed417b9d8/20261020T001214-e3ca50e1753c4cf9b5179aba95576ed4/outputs/cave-popcorn/cave-popcorn.glb",
      "sha256": "632cd423e346082d424d33323955635381a20e5b19be7ec663a5afdfda8ddebb",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-1/244ad9fa6dec2dc9373e30c7781bbd7a96cfb51cee75111aca4f548ed417b9d8/20261020T001214-e3ca50e1753c4cf9b5179aba95576ed4/outputs/cave-popcorn/metadata.json",
      "sha256": "5a57cdb7e179e4705d5147ba8fa2a4c75934b9b695f6a79d96ea80415e7462c2",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-1/244ad9fa6dec2dc9373e30c7781bbd7a96cfb51cee75111aca4f548ed417b9d8/20261020T001214-e3ca50e1753c4cf9b5179aba95576ed4/outputs/cave-popcorn/qa.json",
      "sha256": "6eef285f6c77149eb1ae33b895080ab0d00576a13848f14bb55b588a8f92e10e",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-1/244ad9fa6dec2dc9373e30c7781bbd7a96cfb51cee75111aca4f548ed417b9d8/20261020T001214-e3ca50e1753c4cf9b5179aba95576ed4/request.json",
      "sha256": "c0b4ac45140872e9c0e4b83d701bd94f0e5b91fdad3a1155d5c35a558eef7a52",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-1/244ad9fa6dec2dc9373e30c7781bbd7a96cfb51cee75111aca4f548ed417b9d8/20261020T001214-e3ca50e1753c4cf9b5179aba95576ed4/result.json",
      "sha256": "9a672b451438b85277c359778a547555da68a3c92dd24389c4d03eb92f0d61e4",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-1/244ad9fa6dec2dc9373e30c7781bbd7a96cfb51cee75111aca4f548ed417b9d8/20261020T001214-e3ca50e1753c4cf9b5179aba95576ed4/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-1/244ad9fa6dec2dc9373e30c7781bbd7a96cfb51cee75111aca4f548ed417b9d8/20261020T001214-e3ca50e1753c4cf9b5179aba95576ed4/stdout.log",
      "sha256": "01d14732cbabec35f2411059d81d485085b59a444c073d19e98a1a22b10a8725",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-2/1c56f398588d70aa32386139fa1fdc508ac83785066ef5dc430400f69cacaf20/20261020T001216-54f8dbe9198943e699e9f6c49e4cd853/outputs/cave-popcorn/cave-popcorn.blend",
      "sha256": "9f1f35fac3c53e801e2b7493112ea3f5a4345ec6430fa9c3bf7e0da2b186b9b4",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-2/1c56f398588d70aa32386139fa1fdc508ac83785066ef5dc430400f69cacaf20/20261020T001216-54f8dbe9198943e699e9f6c49e4cd853/outputs/cave-popcorn/cave-popcorn.glb",
      "sha256": "632cd423e346082d424d33323955635381a20e5b19be7ec663a5afdfda8ddebb",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-2/1c56f398588d70aa32386139fa1fdc508ac83785066ef5dc430400f69cacaf20/20261020T001216-54f8dbe9198943e699e9f6c49e4cd853/outputs/cave-popcorn/metadata.json",
      "sha256": "a92e1524a3a52e62d9bc52f05f1557ed708186b30b0deea8f0e5d5f4b97fc014",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-2/1c56f398588d70aa32386139fa1fdc508ac83785066ef5dc430400f69cacaf20/20261020T001216-54f8dbe9198943e699e9f6c49e4cd853/outputs/cave-popcorn/qa.json",
      "sha256": "5ce8866fefe80f445df1929c2d3f16aa09bc7da8e4e93e70f602ce191edd9818",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-2/1c56f398588d70aa32386139fa1fdc508ac83785066ef5dc430400f69cacaf20/20261020T001216-54f8dbe9198943e699e9f6c49e4cd853/request.json",
      "sha256": "13e6aeb66001d3b2dbbd41317fad80c1a405d255c75376fe8fede39cc9d90398",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-2/1c56f398588d70aa32386139fa1fdc508ac83785066ef5dc430400f69cacaf20/20261020T001216-54f8dbe9198943e699e9f6c49e4cd853/result.json",
      "sha256": "4ea68c49d5725d830c2d15c4dbb91b568a421de04024b4df6968705b982d7250",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-2/1c56f398588d70aa32386139fa1fdc508ac83785066ef5dc430400f69cacaf20/20261020T001216-54f8dbe9198943e699e9f6c49e4cd853/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/build/cave-popcorn/r001/rebuild-2/1c56f398588d70aa32386139fa1fdc508ac83785066ef5dc430400f69cacaf20/20261020T001216-54f8dbe9198943e699e9f6c49e4cd853/stdout.log",
      "sha256": "e9a3375727a0d3d04859c61d2674c27f36b2c570acf6f15eb94564d9fbaba04b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/runs/20261020T001214-f6cac3247873419bb688ca91c320d513/manifest.json",
      "sha256": "21375cdc04b5dd6ee7bc5664f2b91a350a70d3629c35ed3b696b184ac6c4a3a3",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild-runs/runs/20261020T001214-f6cac3247873419bb688ca91c320d513/summary.json",
      "sha256": "7bd2cb60a312b884674de428bc1ddf657fbfafd8ca1e68155144537bf2159d3e",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/rebuild.log",
      "sha256": "60454301a30254832c81a866d6245f9df2f37f488db2fa780bbd5a1f95b41881",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/renderer/__pycache__/asset_common.cpython-313.pyc",
      "sha256": "7a2935b1c79e48a6b561ed27571de599013a133b6fd998422a322df95da9797b",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/renderer/__pycache__/qa_glb.cpython-313.pyc",
      "sha256": "1c93e744bf62c8712949bb7c81dbe21447db7d4f90548e7a89a7930a3d834e52",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/renderer/asset_common.py",
      "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/renderer/qa_glb.py",
      "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/renderer/render_candidate_views.py",
      "sha256": "16f85c1a8bffdaa17480b3d878120dbb3dea8d664f826b2df9d4db4d1f6c5dec",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/run-r002-verification.py",
      "sha256": "acf3019ee1daedf4487fc7d76537807c5d7c10449a7f6ea00a515f2ff9702099",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/run-r003-verification.py",
      "sha256": "1d8744a9f14c185b14855486850315333f674b963cc3328ad77366f0db9783d0",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/cave-popcorn/source-reopen.log",
      "sha256": "68e80ab56ff7cb9681300684e57c4405c59b239cf65d9eaf522384b4667deabd",
      "origin": "source",
      "owner": "cave-popcorn"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/checksums.sha256",
      "sha256": "57adfb45e2190baf469cc766d203212750ed8f2260c25d316660a013464b548c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/claim.json",
      "sha256": "e903f890b3b05662a5da9f6e0d8677bb5e75a7cafc9357a47fbd28d81ba1b73f",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail-supplemental-final.json",
      "sha256": "65f758f0dd30354ecd659a6b04c85026864e296bd07a490644d66c2f603c87fe",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/brief-design-freeze.json",
      "sha256": "811733f797a4f7ca2c926b950c474153e3c7dd194a30903e833e700d541e4bad",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-jobs.json",
      "sha256": "8bf167256f5bd27c84cb16046b3f113b43e2f056f22e6047cb03d1e1e80a136a",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/initial/30984c6e9e1bf94e7ded1869506242ebe452d40f676aa0cccbc5e5d135c76cd6/20261020T001147-ea264e39bf494b02b3ebcc88877f98cd/outputs/curvolithus-trilobed-trail/curvolithus-trilobed-trail.blend",
      "sha256": "855e69c6679d20f4e63f7caa8a93e804f66cc386ae3b99759dce589067f0f9bf",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/initial/30984c6e9e1bf94e7ded1869506242ebe452d40f676aa0cccbc5e5d135c76cd6/20261020T001147-ea264e39bf494b02b3ebcc88877f98cd/outputs/curvolithus-trilobed-trail/curvolithus-trilobed-trail.glb",
      "sha256": "c07529a8856b679af1a1d3e816c37046076488ee926f7e38e70241f0cbefed22",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/initial/30984c6e9e1bf94e7ded1869506242ebe452d40f676aa0cccbc5e5d135c76cd6/20261020T001147-ea264e39bf494b02b3ebcc88877f98cd/outputs/curvolithus-trilobed-trail/metadata.json",
      "sha256": "03460265c1098b854d2f7ab5ccc67f9e4c4dd27b446458140d2c6aadc3092e50",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/initial/30984c6e9e1bf94e7ded1869506242ebe452d40f676aa0cccbc5e5d135c76cd6/20261020T001147-ea264e39bf494b02b3ebcc88877f98cd/outputs/curvolithus-trilobed-trail/qa.json",
      "sha256": "c38f798a1c18af9ae7c3e8d54d3484ac9c5c459fa2761e4ae24026983bc23688",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/initial/30984c6e9e1bf94e7ded1869506242ebe452d40f676aa0cccbc5e5d135c76cd6/20261020T001147-ea264e39bf494b02b3ebcc88877f98cd/request.json",
      "sha256": "e70a98b5e5e5ac392236a3e31ab70e6192033ab86ee175aaf44cdfddf415368f",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/initial/30984c6e9e1bf94e7ded1869506242ebe452d40f676aa0cccbc5e5d135c76cd6/20261020T001147-ea264e39bf494b02b3ebcc88877f98cd/result.json",
      "sha256": "69eba2024f943d447a460a3829a1c2fcf434119935798f3a7c051b56e7cdc73d",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/initial/30984c6e9e1bf94e7ded1869506242ebe452d40f676aa0cccbc5e5d135c76cd6/20261020T001147-ea264e39bf494b02b3ebcc88877f98cd/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/initial/30984c6e9e1bf94e7ded1869506242ebe452d40f676aa0cccbc5e5d135c76cd6/20261020T001147-ea264e39bf494b02b3ebcc88877f98cd/stdout.log",
      "sha256": "c860df4ad314f396681e0b5b782c9d9dc7b6556779af3fa2aca46a24f309d63e",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-1/61a6cb8dae07f49b80d48dd222149dce86437937a6fc114deb6b8434e0d03755/20261020T001149-dac59c6b89b54b579383f2fc25c4f9a7/outputs/curvolithus-trilobed-trail/curvolithus-trilobed-trail.blend",
      "sha256": "2fbe3e35222c2ec3d6b4d86f6be13936b49fd2f59533874d0feb23351c1397b4",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-1/61a6cb8dae07f49b80d48dd222149dce86437937a6fc114deb6b8434e0d03755/20261020T001149-dac59c6b89b54b579383f2fc25c4f9a7/outputs/curvolithus-trilobed-trail/curvolithus-trilobed-trail.glb",
      "sha256": "c07529a8856b679af1a1d3e816c37046076488ee926f7e38e70241f0cbefed22",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-1/61a6cb8dae07f49b80d48dd222149dce86437937a6fc114deb6b8434e0d03755/20261020T001149-dac59c6b89b54b579383f2fc25c4f9a7/outputs/curvolithus-trilobed-trail/metadata.json",
      "sha256": "58cb68515f095589c78803a7ec1e024623d7294df93b284eeabe3fc4c005e663",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-1/61a6cb8dae07f49b80d48dd222149dce86437937a6fc114deb6b8434e0d03755/20261020T001149-dac59c6b89b54b579383f2fc25c4f9a7/outputs/curvolithus-trilobed-trail/qa.json",
      "sha256": "334f6571e9bda00b0109be7c36ffb05aa8c2683bdd5aa3edf0910c63c2eeb5e6",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-1/61a6cb8dae07f49b80d48dd222149dce86437937a6fc114deb6b8434e0d03755/20261020T001149-dac59c6b89b54b579383f2fc25c4f9a7/request.json",
      "sha256": "e36688a31eff7e74711287e5fea4a6dc3fccc2ae9e6f7b1c93a350e459f70c16",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-1/61a6cb8dae07f49b80d48dd222149dce86437937a6fc114deb6b8434e0d03755/20261020T001149-dac59c6b89b54b579383f2fc25c4f9a7/result.json",
      "sha256": "bff09b9952bc7b26bbb305574bdca143647641cc2469110b10c416c67ccd7d89",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-1/61a6cb8dae07f49b80d48dd222149dce86437937a6fc114deb6b8434e0d03755/20261020T001149-dac59c6b89b54b579383f2fc25c4f9a7/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-1/61a6cb8dae07f49b80d48dd222149dce86437937a6fc114deb6b8434e0d03755/20261020T001149-dac59c6b89b54b579383f2fc25c4f9a7/stdout.log",
      "sha256": "60e38db7548af0e290a559897f94f56e5b019702a645f8768321be86ddba5892",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-2/0f3fe59e2078b8d3f19b7ec2099a3f11c493b9dc2f698d0066e03ada7c4fd704/20261020T001150-93a9abab089042d0a24825e703742023/outputs/curvolithus-trilobed-trail/curvolithus-trilobed-trail.blend",
      "sha256": "a710abf90eea7a0dad4d4d5529ff6483c9f99c6f2237714b28e5b2ad82755d1c",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-2/0f3fe59e2078b8d3f19b7ec2099a3f11c493b9dc2f698d0066e03ada7c4fd704/20261020T001150-93a9abab089042d0a24825e703742023/outputs/curvolithus-trilobed-trail/curvolithus-trilobed-trail.glb",
      "sha256": "c07529a8856b679af1a1d3e816c37046076488ee926f7e38e70241f0cbefed22",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-2/0f3fe59e2078b8d3f19b7ec2099a3f11c493b9dc2f698d0066e03ada7c4fd704/20261020T001150-93a9abab089042d0a24825e703742023/outputs/curvolithus-trilobed-trail/metadata.json",
      "sha256": "25f31901c9e9632f33d00e0cc3f8ad3c49256223ec079939f8922ef167ff0c85",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-2/0f3fe59e2078b8d3f19b7ec2099a3f11c493b9dc2f698d0066e03ada7c4fd704/20261020T001150-93a9abab089042d0a24825e703742023/outputs/curvolithus-trilobed-trail/qa.json",
      "sha256": "6b7f34df063c578320a8754cdb0b6590e68235b03597580911b0b41a827ae670",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-2/0f3fe59e2078b8d3f19b7ec2099a3f11c493b9dc2f698d0066e03ada7c4fd704/20261020T001150-93a9abab089042d0a24825e703742023/request.json",
      "sha256": "00f7a4043a7f27bb88a43d49566268ade2b9c441c3cdf661579fedf8c8223c5c",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-2/0f3fe59e2078b8d3f19b7ec2099a3f11c493b9dc2f698d0066e03ada7c4fd704/20261020T001150-93a9abab089042d0a24825e703742023/result.json",
      "sha256": "20c2fc2c4cd4e759676b3f42c5446c0f3248def9254cc82519862f439b63eece",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-2/0f3fe59e2078b8d3f19b7ec2099a3f11c493b9dc2f698d0066e03ada7c4fd704/20261020T001150-93a9abab089042d0a24825e703742023/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/build/curvolithus-trilobed-trail/r001/rebuild-2/0f3fe59e2078b8d3f19b7ec2099a3f11c493b9dc2f698d0066e03ada7c4fd704/20261020T001150-93a9abab089042d0a24825e703742023/stdout.log",
      "sha256": "453dbe6b48d7189e6448289b8ad0e7f8fd2cdea5013896bf5b8f3ced8f2a6375",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/runs/20261020T001147-a698aaac82e344c4ac6a86b4f0b9a0e3/manifest.json",
      "sha256": "ecfd84804339e0d1bd4d263b012ad1fc90f8b5af95c2de53de05298202a76c33",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/build-runs/runs/20261020T001147-a698aaac82e344c4ac6a86b4f0b9a0e3/summary.json",
      "sha256": "23cee4a14c0e2c3004f71724aea0efd6f21d44dab30cca2ce25bb9bd9afa8626",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concept-evidence.json",
      "sha256": "344469bb0f50e94cde9fc03669c4621de34f8e3ce4f55332911bcdd57ab1ffc7",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concept-validation-require-complete.json",
      "sha256": "65f758f0dd30354ecd659a6b04c85026864e296bd07a490644d66c2f603c87fe",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concept-validation.json",
      "sha256": "65f758f0dd30354ecd659a6b04c85026864e296bd07a490644d66c2f603c87fe",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concepts/generation-record.json",
      "sha256": "e1380e36a0f03188475218716e2a17bd2a314932cafe6c9bb3bb2e2d0f70f046",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concepts/inspection.json",
      "sha256": "392c777d3ed7f19d2afcbb5cf91529ae8e57ad9cd8573cbe9c87e716463a3d52",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concepts/invocation-start.json",
      "sha256": "1ef0141a865fa6ba61e04ec3b48d15e1c19f9a81aaeebb59de82b3fdd6280de9",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concepts/original.png",
      "sha256": "5cec7a83688540fd880a945abd4a93d30c67824c6511eff2fe96d2a4e287f0f8",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concepts/prompt.txt",
      "sha256": "506d9b60f961349040682e29ef88e1df8e58e6355b135765a7285643daef5da5",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/delivery-metadata-amendment.json",
      "sha256": "b26d825fd130aa9ee19fa981043c7044fb8fd4b67d09746e09d7047cfbaa2174",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/final-bundle-hashes.json",
      "sha256": "4859ab1e0e12dbdaf4b582e5f4b4faadcc6118dcff67698e5af434880800ea49",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/frame-byte-equivalence.json",
      "sha256": "8bf5d3bc5aabb0970af4767d99ace2364d72645a62dd6112e96700bf705517f3",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/handoff.json",
      "sha256": "48fee8ca703cff22fef2ef5d254acb5e0142381c4da2fb88b30bb7f68232a51e",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/handoff.md",
      "sha256": "fd9c8b95be2d41c766745342ad0113d40fc03442ec76325cf08f97229003119b",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/ledger-amendment.json",
      "sha256": "e30c01a8b1942843875ffd8f5411ead25dde3570e9d07d050a4223d02b7f16aa",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/maker-inspection.json",
      "sha256": "46caedcb6a7effc7f1143baa7d18e553aae61483c3678eb40975f4605b4526a9",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/maker-review.md",
      "sha256": "d53840bfdd30e8ef226dc87623ecd33d48e9dbc586b20bf1fa18bf7f3431f9c1",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/modeling-freeze.json",
      "sha256": "52fb96fdfa367b9d775cc6a6b07855ac25744a0727520d68be2f9967b760506d",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/modeling-start.json",
      "sha256": "5a0de2afd4c7ffd4bb9ae0ed2d106c5eaac30989de1aadc9a81e1147d44c5cae",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/references-initial.json",
      "sha256": "3c0204aef7181cadb0ae42eae09c8f61b07e148653565642e1ead8b5c2923dab",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/render-amended-ledger.log",
      "sha256": "a6ed6d45ca37de8637c6d1432a3b02393079da31aa8cb6b2f85da852acb3dca8",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/render-final-delivery.log",
      "sha256": "b425a6b14e15bfc94267276e121ff8750a2dce00420aca86bb9d2e391eeabd70",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/render.log",
      "sha256": "0e610db166c56466edcf23bb46f1e2fd9cc88ab9b3735ee2b3faae4cb9c78bde",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/source-reopen.log",
      "sha256": "a8b1bfdb4b8f7ca7dc11b3a9bc67f61585d793f22b46660d79ce6f359b10cf89",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/validation-attempt-notes.md",
      "sha256": "d2cd07905574a4bf83264b795ebf15c69ef40c90f42149e44072125e125251c6",
      "origin": "source",
      "owner": "curvolithus-trilobed-trail"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/dispatch-record.json",
      "sha256": "86067b9d00f1cc3c88be52627ae664cb6c7e87b3b36f3e09e1e3e4e5d934b15f",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/environment-and-dependencies.json",
      "sha256": "e6d1f938301e449c22dbede689fd4c4595ab6c58efcd763d9e09da9f21310f0b",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/final-integrity.json",
      "sha256": "f15fe9191ca55e0fbab9e7c04261317ed744e331add4909ccfc64f03b952d310",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/npm-ci-success.log",
      "sha256": "51a578e266ed6ba20de2b38c44417a81e70cd03faa1432d6ddfe9099e2f1525b",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis-supplemental-final.json",
      "sha256": "4dc16438d38b27fa64940e054ab57510f768d290ac8904b84a6827cd71139b04",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/brief-pre-model.json",
      "sha256": "363d7254093144925e5af9dcf67859025e92a8536aaa7e5c7758eb59d1324cff",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-jobs.json",
      "sha256": "476cf5fc3a4260894dc91d6fff45b14f7f96851ad810482b6332e5dda5891322",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-queue-invalid-flags.log",
      "sha256": "2fedfe0b5b1ab2b5218e9f70e50905b773aeaac75fc1eff7f682769dfb33a2a1",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-queue.log",
      "sha256": "c30880b970d0f8ddb8699126c0dc4874fd5a804bf37de57ef986a5859d0c4c04",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/initial/b6123272259e26a449e46413c0cc2247f6ee6a1946f4cc5ed52dd0f885b22e7a/20261020T001139-b003cc0588564e8a99c5bacdc064840a/outputs/metadata.json",
      "sha256": "1a498656d62df6e3fb7a8005184f7a1d658ba8eac7adb6e98a277c7456bc9d42",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/initial/b6123272259e26a449e46413c0cc2247f6ee6a1946f4cc5ed52dd0f885b22e7a/20261020T001139-b003cc0588564e8a99c5bacdc064840a/outputs/phoenicopsis.blend",
      "sha256": "667f919e75ef8d1b0839bb9d494197646833d5160992d88b6364d6e72f02bcdd",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/initial/b6123272259e26a449e46413c0cc2247f6ee6a1946f4cc5ed52dd0f885b22e7a/20261020T001139-b003cc0588564e8a99c5bacdc064840a/outputs/phoenicopsis.glb",
      "sha256": "7e7fa939eeca8d1d0571ae1724faa7fa2387f03441bf0794fe4b269d666182d0",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/initial/b6123272259e26a449e46413c0cc2247f6ee6a1946f4cc5ed52dd0f885b22e7a/20261020T001139-b003cc0588564e8a99c5bacdc064840a/outputs/qa.json",
      "sha256": "395bb68bf4401e1b0ed5b1388964d0588c02d1a1fa680d4a9855ee8ded5f88f4",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/initial/b6123272259e26a449e46413c0cc2247f6ee6a1946f4cc5ed52dd0f885b22e7a/20261020T001139-b003cc0588564e8a99c5bacdc064840a/outputs/source-counts.json",
      "sha256": "00edffa177927624e4fbfeb9dcdca10186be6b5a8c713f17a50cecaccd43e1e8",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/initial/b6123272259e26a449e46413c0cc2247f6ee6a1946f4cc5ed52dd0f885b22e7a/20261020T001139-b003cc0588564e8a99c5bacdc064840a/request.json",
      "sha256": "51fb494d217b77d6c293a1ced9f77871513eb6cf2315a5f582796ec0bc45e7a9",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/initial/b6123272259e26a449e46413c0cc2247f6ee6a1946f4cc5ed52dd0f885b22e7a/20261020T001139-b003cc0588564e8a99c5bacdc064840a/result.json",
      "sha256": "27169c454064446ad9d0c0fb94613427601aab320e55c5535eed98114ae2ca57",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/initial/b6123272259e26a449e46413c0cc2247f6ee6a1946f4cc5ed52dd0f885b22e7a/20261020T001139-b003cc0588564e8a99c5bacdc064840a/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/initial/b6123272259e26a449e46413c0cc2247f6ee6a1946f4cc5ed52dd0f885b22e7a/20261020T001139-b003cc0588564e8a99c5bacdc064840a/stdout.log",
      "sha256": "2ddccfd5b17d74d0dcb747f0bca25db8293088fe3dd230b767d0fe0675deb30e",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild1/d995fbde7cdbcf419f3aed3548e0f046545ff8cfc7f1c8c2673d2b573983bfc9/20261020T001141-72e1747c6f0b46bb9ff4e340e9266eeb/outputs/metadata.json",
      "sha256": "91df72f770a71a2980fc609ade654bc90c61a0bff93e0b72cc974b6eeeb85b62",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild1/d995fbde7cdbcf419f3aed3548e0f046545ff8cfc7f1c8c2673d2b573983bfc9/20261020T001141-72e1747c6f0b46bb9ff4e340e9266eeb/outputs/phoenicopsis.blend",
      "sha256": "eb5e0c71692b16d9c32e2b8e5ac2e14ce441f7edd084f3c8cc2649bb9d478602",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild1/d995fbde7cdbcf419f3aed3548e0f046545ff8cfc7f1c8c2673d2b573983bfc9/20261020T001141-72e1747c6f0b46bb9ff4e340e9266eeb/outputs/phoenicopsis.glb",
      "sha256": "7e7fa939eeca8d1d0571ae1724faa7fa2387f03441bf0794fe4b269d666182d0",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild1/d995fbde7cdbcf419f3aed3548e0f046545ff8cfc7f1c8c2673d2b573983bfc9/20261020T001141-72e1747c6f0b46bb9ff4e340e9266eeb/outputs/qa.json",
      "sha256": "ce39fca8ab83ef38a4829ec845dc91ec02411d4b9028ebaa89b1be8421a19730",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild1/d995fbde7cdbcf419f3aed3548e0f046545ff8cfc7f1c8c2673d2b573983bfc9/20261020T001141-72e1747c6f0b46bb9ff4e340e9266eeb/outputs/source-counts.json",
      "sha256": "00edffa177927624e4fbfeb9dcdca10186be6b5a8c713f17a50cecaccd43e1e8",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild1/d995fbde7cdbcf419f3aed3548e0f046545ff8cfc7f1c8c2673d2b573983bfc9/20261020T001141-72e1747c6f0b46bb9ff4e340e9266eeb/request.json",
      "sha256": "469ccb6803b72e34fd7fc7035f0f33301685bed8f112e83ac075f40f4f40a0f7",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild1/d995fbde7cdbcf419f3aed3548e0f046545ff8cfc7f1c8c2673d2b573983bfc9/20261020T001141-72e1747c6f0b46bb9ff4e340e9266eeb/result.json",
      "sha256": "b390637ed6af30d0c460ceb61716d72edf8e91bd78c83f4acdb928251f4bb3a2",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild1/d995fbde7cdbcf419f3aed3548e0f046545ff8cfc7f1c8c2673d2b573983bfc9/20261020T001141-72e1747c6f0b46bb9ff4e340e9266eeb/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild1/d995fbde7cdbcf419f3aed3548e0f046545ff8cfc7f1c8c2673d2b573983bfc9/20261020T001141-72e1747c6f0b46bb9ff4e340e9266eeb/stdout.log",
      "sha256": "19230cb6261665bb4926892f111534ee4cc5431cafa5791ab9cc06b4e73b6f6a",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild2/404ef46e616baa1085516986d507b1ee844531e8ced43ad5da27042c5c5b5397/20261020T001143-da864ad20f194ee5b6b04a82ec548f95/outputs/metadata.json",
      "sha256": "52a10fa1cb616598c4da95c6686b4512f95abd3b6fec4f845b682cbab1200d6b",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild2/404ef46e616baa1085516986d507b1ee844531e8ced43ad5da27042c5c5b5397/20261020T001143-da864ad20f194ee5b6b04a82ec548f95/outputs/phoenicopsis.blend",
      "sha256": "f6c5221583b1456fa90bafa7d2a6e933544d486fae5574405ea4fb6c22dde270",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild2/404ef46e616baa1085516986d507b1ee844531e8ced43ad5da27042c5c5b5397/20261020T001143-da864ad20f194ee5b6b04a82ec548f95/outputs/phoenicopsis.glb",
      "sha256": "7e7fa939eeca8d1d0571ae1724faa7fa2387f03441bf0794fe4b269d666182d0",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild2/404ef46e616baa1085516986d507b1ee844531e8ced43ad5da27042c5c5b5397/20261020T001143-da864ad20f194ee5b6b04a82ec548f95/outputs/qa.json",
      "sha256": "c05aa7dd536681421a5d3cf01661d3735efd337cec11286f5cde86e52ea86ad5",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild2/404ef46e616baa1085516986d507b1ee844531e8ced43ad5da27042c5c5b5397/20261020T001143-da864ad20f194ee5b6b04a82ec548f95/outputs/source-counts.json",
      "sha256": "00edffa177927624e4fbfeb9dcdca10186be6b5a8c713f17a50cecaccd43e1e8",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild2/404ef46e616baa1085516986d507b1ee844531e8ced43ad5da27042c5c5b5397/20261020T001143-da864ad20f194ee5b6b04a82ec548f95/request.json",
      "sha256": "b7a109beb9e43d9b7371f9692665c2352790df55bb99913893b4bbd45417ec1b",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild2/404ef46e616baa1085516986d507b1ee844531e8ced43ad5da27042c5c5b5397/20261020T001143-da864ad20f194ee5b6b04a82ec548f95/result.json",
      "sha256": "996cd8e537c110debd3e0051050505eb3d906c8ae59403228867bddfc4ece7e9",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild2/404ef46e616baa1085516986d507b1ee844531e8ced43ad5da27042c5c5b5397/20261020T001143-da864ad20f194ee5b6b04a82ec548f95/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/build/phoenicopsis/r001/rebuild2/404ef46e616baa1085516986d507b1ee844531e8ced43ad5da27042c5c5b5397/20261020T001143-da864ad20f194ee5b6b04a82ec548f95/stdout.log",
      "sha256": "44f78c91b0a27fbda8c46c4c9c6f89ab3ece3afb4f5ecb9da5a3f2db906c43fd",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/runs/20261020T001139-06c95a49eb374cf3a2104771724d49c8/manifest.json",
      "sha256": "baf13f63bd6bc8090e42d3dccbef57404816c38dfa8781f1be4807679e0611aa",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/build-runs/runs/20261020T001139-06c95a49eb374cf3a2104771724d49c8/summary.json",
      "sha256": "855f86c1376798219fbf4d8f23e17d7083f720c85abab834d6012661052c735b",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/candidate-validation.json",
      "sha256": "c034db47249ab6bba3f752b70830fae28c6657db52f85b06509609db0807152c",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/checksums.sha256",
      "sha256": "7feeaaa89cbd3a3dd200420f95d7c107e04f084ea5581814d146d93676957204",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/concept-validation.txt",
      "sha256": "4dc16438d38b27fa64940e054ab57510f768d290ac8904b84a6827cd71139b04",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/concept/generation-record.json",
      "sha256": "8e7c9996e94fde854ebf0ce2da844b4c4ab980b551cc43664b6320ca75133eb4",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/concept/original.png",
      "sha256": "3405dea11e2776970efcf652bcdab7469e2805a15d8a7097efdddfbad251432b",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/concept/prompt.txt",
      "sha256": "4c72aa1e079498b442736261b7e73a398f27df86f2325a6e86f660860463ec4c",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/concept/tool-result.json",
      "sha256": "4c01c1d08a78f93163b1e847da15621314e162775722ad0537be08a9ae8de4a0",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/handoff.json",
      "sha256": "0b91ed1ece2fb145d41c6299aa56060ce4f7b17e4a517127b14adda3eb0a095a",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/modeling-freeze.json",
      "sha256": "3df8a9f80422511d1f5dd523bf32eee80723b7627dc61a4afa7a2ac69e01cd64",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/package_candidate.py",
      "sha256": "49f23281dc281466528333b66bd46d4835becec2ea5cea1dd37ebccaa53d4b3a",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/packaging-amendment.json",
      "sha256": "0328a72e3baecfb3cc56405f2a9d88a5d05e0990519539840fc57591c08519f7",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/clay.png",
      "sha256": "fca428cbd44b3ec562a6828789006c34991bf01bf6e348089b2be28a5fbf1b69",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/front.png",
      "sha256": "acf2395460534134c9509315f1ef705748405812ab05346c804a166ed0067e74",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/hero.png",
      "sha256": "bf768f8196bd572f5c3a82289dedd36ef7aa9c839b5d97c1562df8d1142e9382",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/rear.png",
      "sha256": "caa8fadb53e37f138334ba4d6c964edbfe88f3889200cf59eadb25b036af8c7f",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/render-config.json",
      "sha256": "b144f295716630e8935f7063bb3f4c3ec1186dfafa416d7f773b2b5ee8184b41",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/render-manifest.json",
      "sha256": "e68345434224d6f55767eb240bd0748815ade90ea61f89383874e9b1c4242a81",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/reversehero.png",
      "sha256": "aab4baeab2057912b0ac7197dfe981407b3c3a9c0e4dc371ef9e02036b456288",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/side.png",
      "sha256": "b1e137632cb8095fe553982b3e42df0f1eaf2feeb7f4d1f9e474fa4b6501d5be",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/silhouette.png",
      "sha256": "00bbd45ceb27399d51452edd115cb8de08910400f4c25a9a3c70115a7641f1ea",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/top.png",
      "sha256": "54f2932d2ff83901bfdc7d922df3994c8afee365e0e23959968e0fceb549444b",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/proof-pre-packaging-amendment/turntable.json",
      "sha256": "232c02434266fc6f572e79046381e90f96f10c4a9427501ecd3ee10b22d1064b",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/rebuild1-check.log",
      "sha256": "2760220ed3fa8b4433650692bd7f4a0c535b2a892ee343adc41157cab6423bdf",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/rebuild2-check.log",
      "sha256": "0b155035fb5ad01a8b06baf9a16e73601047f91cdb18d7fbdf44805afa728edb",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/render-amended-brief.log",
      "sha256": "f60ad9b524b4d915e18d340301219566323891b85420e920c2d48c4aa0edff6d",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/render-invalid-unsupported-silhouette.log",
      "sha256": "74cd08148cf6f9e07b37fde6af1993e403c781333ce184768850c1d32225c372",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/render-tools/__pycache__/asset_common.cpython-313.pyc",
      "sha256": "4d3cc6e7946339ed62886a73429dc9606bfa37c65e4399f16785e24d090a90d4",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/render-tools/__pycache__/qa_glb.cpython-313.pyc",
      "sha256": "989d4f7a15b329e6609e8aff2f4f99926ffb9452f0b1b99f7edb5dc7595c8e40",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/render-tools/asset_common.py",
      "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/render-tools/qa_glb.py",
      "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/render-tools/render_candidate_views.py",
      "sha256": "9f56ef4a7a0c28cd6cb7815aa8790023b1dfa674862166c9be74ce822b06d607",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/render.log",
      "sha256": "275125eff7f3b7619bbf8300b2551078416536b52697ef92ed5e617977230da5",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/phoenicopsis/source-reopen.log",
      "sha256": "ad20b943a20c7ff43fd3e4d5475d1d370d1f23cbf13c8f3e6a79929a1a3020b2",
      "origin": "source",
      "owner": "phoenicopsis"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/planning-import-manifest.json",
      "sha256": "9f26d5b03d9e34e292e6787317b10aea9db51940b10fc4c11f725a8ea384ed8a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/verify-aturia-r003-protected.py",
      "sha256": "dfe60e0656d36788c6a13d09b15f46d1b72e49a969655fd46f69c302d3907c8b",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/verify_handoff.py",
      "sha256": "ef7db90cd4e7cd56cd802e46820b5bd5cee5a1756461cc06a3661915e993c4c5",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/blender-import-audit.py",
      "sha256": "e3d3c25999bf045ba09167ab2690e92f4564ffd63b9a3f1cc8ea33259d5110b7",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/format-check.mjs",
      "sha256": "3f7de1de2a5079e72685dcb009ada448ee09831ddb26323b43b6bd50bce5291f",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/record-inputs.py",
      "sha256": "80043b51761ec44420087396daee85971b9688dc336f1353ede24cfb2fdaccf0",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/pinned-inputs.json",
      "sha256": "6f0a288ea4f4eb82933de35825f0d942897084d0b9a577a46bbfc516617004e7",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/production-checksum-verification.txt",
      "sha256": "605081d21bb0f11391d117b1fbd8292273a13c11abbd49ebaa8e1ad42668bc72",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/runtime/aturia-single.png",
      "sha256": "03012addfa9304e1fa73656779b7830d4680888502932d90f9325306c49832c8",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/runtime/cave-popcorn-single.png",
      "sha256": "19f92a8d56c46a90d89f6122152dec9c2650235de518a02d90b7193e5b13bab4",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/runtime/curvolithus-trilobed-trail-single.png",
      "sha256": "19646497658496e0662b130f51ef8c579fc3ccf1867dea7330b4e2b0675b4895",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/runtime/phoenicopsis-single.png",
      "sha256": "0952a4dc1c2c08821476ad307c416ae35f216188fdd75f90ccd76b5a735825e4",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/runtime/runtime-report.json",
      "sha256": "9a356bb34037626c8413ec698488e6220370cb3436a8426e00c71c5aedbdb92c",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/runtime/scene-hero.png",
      "sha256": "1286ce04ec8d2b33fc6a320da36083be0190a40702cb6c780ad79b39d0e0fa13",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/runtime/scene-top.png",
      "sha256": "90b2a640f09cbb3a862bc03512d0d3e326dab330f6bab5e7d098acc8b2ebc4b5",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/aturia-blender-import.json",
      "sha256": "42ac4aeb8e30d1dbff3287c6d939dcc1a80cb64d11ce23b498cd5d920de45be5",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/aturia-candidate-validation.json",
      "sha256": "48d6c0174ac19406aa0d2ada206210cb3acf1db51e5c907b8b5bb6eea02ec2d9",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/aturia-concept-evidence-require-complete.exit",
      "sha256": "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/aturia-concept-evidence-require-complete.json",
      "sha256": "4069dab10f8b5fccea0dadcea7df2176ce3820aac8d08c309ef851d4d88dc012",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/aturia-concept-evidence.json",
      "sha256": "4069dab10f8b5fccea0dadcea7df2176ce3820aac8d08c309ef851d4d88dc012",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/aturia-khronos.json",
      "sha256": "ca33f0ff5d387d400ac8fda9b8583fefe79f96596681fdd88191834c3686bfb5",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/aturia-source-export.json",
      "sha256": "92c5b5223796b544ffb74b03305fbff5b390877a920882d6e58e9c8a44a9d847",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/aturia-static.json",
      "sha256": "78244dfa1e65070cc1bf9b7d787c156da01feb6a5bc3486c2c08ec80df0967d5",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/cave-popcorn-blender-import.json",
      "sha256": "3564013f0d93f56a7c18a23876f84ee709eafefc6ac9532b60dffe4dc1085e9d",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/cave-popcorn-candidate-validation.json",
      "sha256": "a37c2d57797f6b6e72524e8a5ca778717662e71c167db22953d2a80d0346e913",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/cave-popcorn-concept-evidence-require-complete.exit",
      "sha256": "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/cave-popcorn-concept-evidence-require-complete.json",
      "sha256": "0ad3524ab9f30f90b414adf1dff9dfb1951340a91a7ba9cb20a99ab2d10b5bcf",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/cave-popcorn-concept-evidence.json",
      "sha256": "0ad3524ab9f30f90b414adf1dff9dfb1951340a91a7ba9cb20a99ab2d10b5bcf",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/cave-popcorn-khronos.json",
      "sha256": "5a905f56002e5db4a8c0722db45cc85d623461d94e98afedd6525748bf8a10e5",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/cave-popcorn-source-export.json",
      "sha256": "15ef730c8a621b5555bb8f58cca26e0099409106bce4552bd84d4dab5a6a3366",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/cave-popcorn-static.json",
      "sha256": "d31797948d2c4a43bd23836a3b3defc6268d6e9424918c3d58e56df082971c9e",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/curvolithus-trilobed-trail-blender-import.json",
      "sha256": "8f0f3a508d0094e4c8cc4607534a1495ed9b7e3bfb25760c6b2affc90ef06061",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/curvolithus-trilobed-trail-candidate-validation.json",
      "sha256": "467db672cbc63d3c602c7eced0704cc4760b49015fee1f1634a01d901466d378",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/curvolithus-trilobed-trail-concept-evidence-require-complete.exit",
      "sha256": "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/curvolithus-trilobed-trail-concept-evidence-require-complete.json",
      "sha256": "65f758f0dd30354ecd659a6b04c85026864e296bd07a490644d66c2f603c87fe",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/curvolithus-trilobed-trail-concept-evidence.json",
      "sha256": "65f758f0dd30354ecd659a6b04c85026864e296bd07a490644d66c2f603c87fe",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/curvolithus-trilobed-trail-khronos.json",
      "sha256": "27d83d55f8258a0f34399db05f3a4cf80ac2b91479c8d310134619200eba4073",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/curvolithus-trilobed-trail-source-export.json",
      "sha256": "3ed85d8c6b809c2f57d6aa36abc773d8eb6c63666a105c10405b330db7475606",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/curvolithus-trilobed-trail-static.json",
      "sha256": "1ab9a29c899f8e2c65d40b2b6b217b2ac341506200494805dfcf0c0afa1aed9e",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/khronos-summary.json",
      "sha256": "d6b1bb84113cc147fadc839e79f12052f7ae83c7c7bf4b75cca1fe2187a5a4c1",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/phoenicopsis-blender-import.json",
      "sha256": "3db13348e07cad5a3183e38f8f3931a8002b232d900f6ca92797a82ea50e5684",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/phoenicopsis-candidate-validation.json",
      "sha256": "c034db47249ab6bba3f752b70830fae28c6657db52f85b06509609db0807152c",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/phoenicopsis-concept-evidence-require-complete.exit",
      "sha256": "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/phoenicopsis-concept-evidence-require-complete.json",
      "sha256": "4dc16438d38b27fa64940e054ab57510f768d290ac8904b84a6827cd71139b04",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/phoenicopsis-concept-evidence.json",
      "sha256": "4dc16438d38b27fa64940e054ab57510f768d290ac8904b84a6827cd71139b04",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/phoenicopsis-khronos.json",
      "sha256": "e2dec3fa4c7f84aede67180b0de6535a21afe497b96f50316bbc5e33a387a62e",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/phoenicopsis-source-export.json",
      "sha256": "e5c11a4b7e775843cc6e69f858df8caf0d47e5ec8e99e18226057c36f9ff433a",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay-20261020T003048Z/technical/phoenicopsis-static.json",
      "sha256": "2262687b166468735a7d7fd45ef5880c92e934c393aeacc2a96153fdfc4f21d0",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/replay.sh",
      "sha256": "900576a715efe8c0770f204b01c95dbe31fc5b909938f69f1173bd7d4bef7aca",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/report.md",
      "sha256": "2d66bc95df2427cfbf2924fc5a9ba4438203e88fd8d529adb272fa58c283d8eb",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/review-evidence.json",
      "sha256": "3331497ea393fb9dce15eae7449f26f65f95172b73f79a1d6b8779d571f8afc7",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/run-checks.sh",
      "sha256": "ee789c95b788dac6a715ae5553a8e3fa489a340097b60667713f6760bc56b0d6",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/run-source-audits.sh",
      "sha256": "fbddd6d391977663a6284917d7409e5851617afda5c9e239ae815524d072ad7c",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-independent-20261020/runtime-scene.mjs",
      "sha256": "7212af2b51a9ac7fa89509cd42de5652aa841331c3585e8d66214a8e373147a7",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-original-three-20261020/capture/render-report.json",
      "sha256": "0143db47a04a3b357d9a03e6814b51a7b897321ee8acc4813c8e3441311e6e02",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-original-three-20261020/capture/index.json",
      "sha256": "9903a35e0e68a5e0846aa36d14ff43a567ba74375260eae3d75c4d382e57e516",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-original-three-20261020/capture-integrity-verification.json",
      "sha256": "422d2e33d762e891336adec45b3299e8cdfd3329bf5da7807f30d590ca9984f4",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-original-three-20261020/capture-projection-audit.json",
      "sha256": "c0d16a5b11635d7fcd848cfd23b8f8d6076cb3c8e5d5ef23470228c9a5feca66",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-original-three-20261020/capture-independent-review.json",
      "sha256": "c406877c97a32df7da4768916b267704dcb0ef14f6b12ca0f7cbe9e0d3bc2c1d",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-original-three-20261020/capture/references/phoenicopsis.png",
      "sha256": "dd36f2eb7a1168e1684282e00db7f96a8cfed2c8eb2d456a86c66f4ea5b13351",
      "origin": "release",
      "owner": "phoenicopsis"
    },
    {
      "path": "qa/batch52-original-three-20261020/capture/references/cave-popcorn.png",
      "sha256": "ecf6a89e452376834ee8d3f90968f16bedce9e43ac270e0538127f54aef34608",
      "origin": "release",
      "owner": "cave-popcorn"
    },
    {
      "path": "qa/batch52-original-three-20261020/capture/references/curvolithus-trilobed-trail.png",
      "sha256": "b6d3cb79a9c8b91e6251fa02171b11156bfc3171376e45db0ff91222f3811043",
      "origin": "release",
      "owner": "curvolithus-trilobed-trail"
    }
  ],
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  }
};
export const BATCH52_ATURIA_REPAIR_RELEASE = {
  "version": 1,
  "scope": "batch52-aturia-repair-20261020",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "provider_generation_timestamp": "unknown",
  "source_commit": "110ec9772e1854ab9c4ccfa23848541b8e3aa1d7",
  "review_commit": "cd53a96b93f7cd513163ade75afe9855237fcd8b",
  "source_bundle": {
    "path": "qa/batch52-aturia-repair-20261020/source-bundle.json",
    "sha256": "16dac3a4723bd789e4a2abaf82c12df18b417635c6bbf73aa34843cab9d01905"
  },
  "review": {
    "path": "qa/batch52-aturia-r003-diff-20261020/review-evidence.json",
    "sha256": "0de129c580b0dbfa7dc65128f1cbdc3c411958507e4b9148e5f42f20d34f0954"
  },
  "capture": {
    "report": {
      "path": "qa/batch52-aturia-repair-20261020/capture/render-report.json",
      "sha256": "0143db47a04a3b357d9a03e6814b51a7b897321ee8acc4813c8e3441311e6e02"
    },
    "index": {
      "path": "qa/batch52-aturia-repair-20261020/capture/index.json",
      "sha256": "9903a35e0e68a5e0846aa36d14ff43a567ba74375260eae3d75c4d382e57e516"
    },
    "packager_integrity": {
      "path": "qa/batch52-aturia-repair-20261020/capture-integrity-verification.json",
      "sha256": "422d2e33d762e891336adec45b3299e8cdfd3329bf5da7807f30d590ca9984f4"
    },
    "projection_audit": {
      "path": "qa/batch52-aturia-repair-20261020/capture-projection-audit.json",
      "sha256": "c0d16a5b11635d7fcd848cfd23b8f8d6076cb3c8e5d5ef23470228c9a5feca66"
    },
    "independent_review": {
      "path": "qa/batch52-aturia-repair-20261020/capture-independent-review.json",
      "sha256": "c406877c97a32df7da4768916b267704dcb0ef14f6b12ca0f7cbe9e0d3bc2c1d"
    }
  },
  "additions": [
    {
      "id": "aturia",
      "revision": "r003",
      "source_commit": "110ec9772e1854ab9c4ccfa23848541b8e3aa1d7",
      "review_commit": "cd53a96b93f7cd513163ade75afe9855237fcd8b",
      "metadata": {
        "path": "assets/additions/aturia/batch52-20261020/release-metadata.json",
        "sha256": "afc44f75e826c3ac40b57e283c89a3a9c0ce6980846911b939000777a8e870d2"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/metadata.json",
        "sha256": "aee6108b2f4cff5414352de619a3036f52cf85d829c9fd9f4bc460dbe51cc6b8"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/candidate.json",
        "sha256": "1e920d02db72ae1182e52e5f6185126fac26956841b7e2742c5c6f5553f20545"
      },
      "review": {
        "path": "qa/batch52-aturia-r003-diff-20261020/review-evidence.json",
        "sha256": "0de129c580b0dbfa7dc65128f1cbdc3c411958507e4b9148e5f42f20d34f0954"
      },
      "capture_reference": {
        "path": "qa/batch52-aturia-repair-20261020/capture/references/aturia.png",
        "sha256": "a2039d069363d05214fbb5564ca331c6cf78c2e197e7fb9080cb90eff31bef33"
      }
    }
  ],
  "files": [
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/aturia.blend",
      "sha256": "f2e7b514dc4adfcb9acfc268335a372d99714f2a81f4011f2b2cef2991f5f675",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/aturia.glb",
      "sha256": "74b4e090382777b9d8b358dd1dad2df57f9751d8266437e95d9d144448cf31d1",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/brief-delivery-completion.json",
      "sha256": "210237b1086c8937b002435919b6dc273b32fcbc8de1f8e9b6aa42ff6a921c6b",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/brief-production.json",
      "sha256": "d19431b328f0b55640b8145bc6fd333c93d0da435fd95c7253bd8488d3237bca",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/brief.json",
      "sha256": "22706fedd098cd247a51ae67dbf529bc256dac2b93c020a48eace16671144b0f",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/build-timing.json",
      "sha256": "d3d4c7504e781ebd878ff2e495cfc41485f2969801cfe4d11164ccb6b43c1048",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/candidate-validation.json",
      "sha256": "c65c81cf9f2c50bb57e8d0883197da379bd8238959d1e9d720022efce59fc421",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/candidate.json",
      "sha256": "1e920d02db72ae1182e52e5f6185126fac26956841b7e2742c5c6f5553f20545",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/color-only.report.json",
      "sha256": "8fb323d5877337c377ed4253b24e047bf2fef8e8d18d8649321afa89130ba0c4",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/concept-evidence-check.json",
      "sha256": "bbde1d57d2fcaf25d93b32bf3b30c5cbc415259806ee2c37ca21ed41a01f11c0",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/concept-evidence.json",
      "sha256": "f7482fb873b830835be35d3104bb70c87fb5c2fcbe1086d186c5df9fbaa6c85c",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/concept-generation.json",
      "sha256": "5ef5886b705780d43ba67dfee36bba7e0ef2cfbfe8ffb12d383f9292d04ae7af",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/concept-original.png",
      "sha256": "55722e90c04098cdc12a4d5f8df5edaefb06ab70c946bfa0e153eeae2978dce6",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/concept-prompt.txt",
      "sha256": "1602693bb882034335c0c4fa7eb816a5518acdc91cc0164b9c41efbf0e60d72d",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/config.json",
      "sha256": "6dedf042fb637d86b136c19c66968f64852e0ecc3dfa8b7cd4be10b2e8bb1954",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/freeze.json",
      "sha256": "7ea1da1b00d00a688e8b9286df94b7a111ff7d3cb30b0e723ad1de30e1824e98",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/generator.py",
      "sha256": "3ef3a3fc69a1f509510ba857a13e6a595efa91fe667a99b9531d24a61cd39058",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/gltf-validator.report.json",
      "sha256": "dae548f1eed16be5164d6d6e24e02e0c592ac3888d3e9483d390c8200c6b38ad",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/metadata.json",
      "sha256": "aee6108b2f4cff5414352de619a3036f52cf85d829c9fd9f4bc460dbe51cc6b8",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/preview-hero.png",
      "sha256": "712ad5513fbbe4a1b33aa7ef5ab485fa47c1091bde5f40562eb3c40125dd4630",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/profile-contract.json",
      "sha256": "3b76b7fe7ac855243605db789d1ab10f16b8751951e0f979b2cc5907a6ec004a",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/clay.png",
      "sha256": "20ad1953457dfc64889c43e952ac7914921be1ed4ef5c0f6b21881c5de52715a",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/front.png",
      "sha256": "b474d26c821d445f95d8e1ee00fbdf1fa49e58d07fb7bad2ac9a56069646d6dd",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/hero.png",
      "sha256": "712ad5513fbbe4a1b33aa7ef5ab485fa47c1091bde5f40562eb3c40125dd4630",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/rear.png",
      "sha256": "641d6afa64326eaceb1acaeae3bb613c58b9769afdd4ce33c297eb3add5abb72",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/render-config.json",
      "sha256": "222ddc37e787008a5683088c341d460bb7b7d86264cd84067ad9a328a54a7e74",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/render-manifest.json",
      "sha256": "7021ec700b139fe314e169665036a3e89877261093eebabd25a7d9024aa82cd3",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/reversehero.png",
      "sha256": "66e090eca277ab809914770f92223107884785f02d3bcb110a72122921c3fcc8",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/side.png",
      "sha256": "30cce1f6fd834d629151508bc058291efdc3a4cefd13b49165a7324be04af174",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/silhouette.png",
      "sha256": "385b7d35ef4b740715ede7055911d1c92c88697cc4086f573b39dcf0a8b0ac20",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/top.png",
      "sha256": "e18c3209555c0bc74c5dca4c8835597073b14533b25e72261ffd78e06ae7c8ae",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/turntable.json",
      "sha256": "15b85d167f3e30989bdbc25e73593034006ba48d3e8d12163973a132c6415d98",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/clay.png",
      "sha256": "718962e8e003893dc09faab83be0076fa2f9b29084a86b9c513e4c741c5f4e29",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/front.png",
      "sha256": "9d539374fdc9ae6e1398664cba2035b134f37553da16dc9986ad585faf9b6293",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/hero.png",
      "sha256": "6e2e77e9318c49d869818b8e6935198c7b9ad09a46d4566f50f985104c58e91c",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/rear.png",
      "sha256": "e1acb130ec7cb5af70d64a8f66fec66ee5b9566f11c8c1c09c0375a58e1c1111",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/render-config.json",
      "sha256": "222ddc37e787008a5683088c341d460bb7b7d86264cd84067ad9a328a54a7e74",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/render-manifest.json",
      "sha256": "c404c19fd6a4586fc113543c16ed0d959169adeeae164f44b54a626b30033e10",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/reversehero.png",
      "sha256": "8515197a7036b5fae91f6a7349befcf9839fb7376fe8d70f29999987d8678027",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/side.png",
      "sha256": "1c4b89a5692608d048fb0de4cd636cef3e5922627001b76de7c2ddd9e73e20c1",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/silhouette.png",
      "sha256": "f9df7cb3358db468784b08265f80c3243c31427679cb432f1e251ef92a93db11",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/top.png",
      "sha256": "1269bbc7154fc443977f145d2652c8dd602a0270bf0974a07877633938cbcaf5",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof/turntable.json",
      "sha256": "15b85d167f3e30989bdbc25e73593034006ba48d3e8d12163973a132c6415d98",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/qa.json",
      "sha256": "849c83bb1dab2b80f7d3e0732d5f9663a300223206630c164c11f41da58bfa0c",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/references.json",
      "sha256": "46c953ad0b45dea0b1a4713513f533b372eb0a80f520cc02852495cca8db24ad",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/render-comparison.report.json",
      "sha256": "405a235b703e8071f20f78d0e5923a5e5bc4c2f0220d59594e49c0fe61e51715",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/reproducibility-1.report.json",
      "sha256": "d0810aab8ae8ca4dc27e867972a63f214b4b08a29f6b53b84febf93c675bf900",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/reproducibility-2.report.json",
      "sha256": "802a5b9388743cf524b063a9c5ec2f5b494ad60e8cad1a121d2a4dd9951b8b3e",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/self-review.md",
      "sha256": "7028e8d4f29fb6b3b35a7840604ef13bf4c6d48c4087eb88ea75357bb98c3027",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/source-access.json",
      "sha256": "aa65c731a5d9f3c49530e9e8a3afc4a3b523b559768df6a39e557460cf5f0010",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/source-export.report.json",
      "sha256": "ab9d134e399fd00eb8aadecdb4545fcdc8b698e375f5244e4d96e9f6dd1a00e4",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/source-geometry-identity.report.json",
      "sha256": "bcd90472741395c7eecdc6a9db14bdb7e5d6d9e4bdf02264f1a4c4c70f1d667e",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/source-mesh-measurements.json",
      "sha256": "e3ae81b8c02a2585f2b0b676d16b488dc226604164dee6bc7a1e5b98d884815c",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/source-qa.json",
      "sha256": "6d9083542f4ec50485757acd8e984ae061a484869f7cf5433dba0f312d040c0e",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/static-glb.report.json",
      "sha256": "10c30faf70dce9089814834d22d86e28620ed514e9c01968407b2b5fbd2c9dd9",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/technical-summary.json",
      "sha256": "1398db936ba6a5f512a45b320456bd473ae88fbda0040d77b53dc7f103510f33",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/HANDOFF.md",
      "sha256": "f9e61a1c1a2353aba4df5b40b46a38fbc90658d0259d8df566a1bb330b31ba11",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/build-jobs.json",
      "sha256": "44a4af37d66fa1a92f18880c3967f5ed9640ccace3133afaa00a7494c03ee0b8",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/build-r002-jobs.json",
      "sha256": "3a0e5cd7d653135de3038a628866b3cbf5e41995adddbde49f9a3f6cfd3981c9",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/build-r002.py",
      "sha256": "3ef3a3fc69a1f509510ba857a13e6a595efa91fe667a99b9531d24a61cd39058",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/build.py",
      "sha256": "cf877f2fc4d5ee4b9efbd6d64f3911ba799b4a1ab743450827bed02f35ba5207",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/bundle-checksums.json",
      "sha256": "5c0494e1d6e152a3b44e7427230b523d71147c468d7f6fc2d40ed537780bfef6",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/finalize.py",
      "sha256": "c447b447083dbe0b8ab61ef92ae58a8bb3d94be90aa6f61f6619b40e2af9a570",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/handoff.json",
      "sha256": "4bc27927693100ea3b06c8a480fa6a91a61480b0779e74b1e1a711fa34c1faa9",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/inspect_source.py",
      "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs-r002/khronos.log",
      "sha256": "b72cf0749bbff75391b49a5a28ed72d47f393d3fbcaac16a4d6770e64f4b6463",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs-r002/rebuild-1.log",
      "sha256": "b8a6f8ee2affb5b9c0bddeaf95e14db95d3f2bbf609ec21bd20df2d1b0f8832b",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs-r002/rebuild-2.log",
      "sha256": "d4bed8fa1a691b6b482fafce308cd21399f636eedb655c5a10d878afabd5c62c",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs-r002/render-final.log",
      "sha256": "1e39ac6035a252f1b8bb37852a80d64b74a1d524d9b4f19fb2bfc2e28cac3332",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs-r002/render-retry.log",
      "sha256": "2810bb7628c60393db4f9eb4de63ed1a77770c28c6504d89115d7b9379f9e1a7",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs-r002/render.log",
      "sha256": "c5fdf97c77922b231ca43c70bbc9a7f0b767a23578ff0919bf97d3415f35aea5",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs-r002/source-export.log",
      "sha256": "d45f115e50e068aeb987a4c4abc5ec148943e78f46ee86b96ddb4bd046ddf622",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs-r002/source-measure.log",
      "sha256": "14b5f4620f55fd505f8227d11c7a25c44bc846aca80f28e1587b0743144b3db1",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs/khronos.log",
      "sha256": "139f9ead0107fa134f00baae7cbbf9f466e2b30a7473e314d3b0296f96f0dc63",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs/rebuild-1.log",
      "sha256": "f6adb8480461210699f395ac11536decc5c4366d576e6f2221f9ba2dd9d3c2e6",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs/rebuild-2.log",
      "sha256": "0a30fda1941b65ddd92fa3ff8755eaac5af20ee02d0e7c4d24668190dbce8b82",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs/render-fixed8-retry.log",
      "sha256": "6aade8264095ff9ce35235936650b61fa7c226875c325e5bd24481480ec119a2",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs/render-fixed8.log",
      "sha256": "86cf07d5a1928661894e5db3cdb95a7505fa49582d45976d90bfb22d2522f520",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs/render.log",
      "sha256": "74cd08148cf6f9e07b37fde6af1993e403c781333ce184768850c1d32225c372",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs/source-export.log",
      "sha256": "f4e2357e40870bd6f9151497c7a2720daa47a114cb14d66dfa7821bd3b41308e",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/logs/source-measure.log",
      "sha256": "b38dd677d5859eb2c9f6507cafea504928b42c2e5636e834a053f1c709d0c8bd",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/render-failed-shadow.py",
      "sha256": "0eadeaf9bd942dcdf1e39664915b31f307a6f653cc6bdeff93158125895abd83",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/render.py",
      "sha256": "82d80847c27d2b344da17750983002291f30cde8c9132814d7d52430921f1dba",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/README.md",
      "sha256": "a91b5d095308e71939965d57da990a23f41e36957e66f8eb65ca8f6f323be518",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/baseline-independent-qa.md",
      "sha256": "2d66bc95df2427cfbf2924fc5a9ba4438203e88fd8d529adb272fa58c283d8eb",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/build-jobs.json",
      "sha256": "d3dfd90a191b543e22661c4f7b2d8665224d2159ac36c4e4257c117856576b76",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/check_color_only.py",
      "sha256": "6b4e14c38833491cc0121467874cd11c04a21a8c8f0f139b01c838c1c27ba4c0",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/check_source_geometry.py",
      "sha256": "b9556fba9feb1e816469192ce2e2d896f054d3dce35e45492b962e8e2ad9fc74",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/color-only-initial-check-failed.json",
      "sha256": "28df9bb56e27654178c994efe51819d46374d54dcb7b7b4dda8ddc0d2d35c9d7",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/finalize.py",
      "sha256": "4159c564f411ad0e71393c1c29dd67880c10ea340234a4bb486da21e8181c1f2",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/handoff.json",
      "sha256": "ecf5ca1193166ada769b706fbc401c0a124dba203d7d14eb9dbfe34e666e18e3",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/initial-build/5a812f7108fcf558bdc17491523594959ce6ab0ba46e95fc46f0a4e41b3065c0/20261020T011847-d77994fe40a8462b82252e2a50f6470f/outputs/aturia.blend",
      "sha256": "f2e7b514dc4adfcb9acfc268335a372d99714f2a81f4011f2b2cef2991f5f675",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/initial-build/5a812f7108fcf558bdc17491523594959ce6ab0ba46e95fc46f0a4e41b3065c0/20261020T011847-d77994fe40a8462b82252e2a50f6470f/outputs/aturia.glb",
      "sha256": "74b4e090382777b9d8b358dd1dad2df57f9751d8266437e95d9d144448cf31d1",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/initial-build/5a812f7108fcf558bdc17491523594959ce6ab0ba46e95fc46f0a4e41b3065c0/20261020T011847-d77994fe40a8462b82252e2a50f6470f/outputs/build-timing.json",
      "sha256": "d3d4c7504e781ebd878ff2e495cfc41485f2969801cfe4d11164ccb6b43c1048",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/initial-build/5a812f7108fcf558bdc17491523594959ce6ab0ba46e95fc46f0a4e41b3065c0/20261020T011847-d77994fe40a8462b82252e2a50f6470f/outputs/metadata.json",
      "sha256": "c71d0ac652db0704964bd8035e204e9014cf127d4dcff2f86f7c4b5f6bb6b00c",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/initial-build/5a812f7108fcf558bdc17491523594959ce6ab0ba46e95fc46f0a4e41b3065c0/20261020T011847-d77994fe40a8462b82252e2a50f6470f/outputs/qa.json",
      "sha256": "6d9083542f4ec50485757acd8e984ae061a484869f7cf5433dba0f312d040c0e",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/initial-build/5a812f7108fcf558bdc17491523594959ce6ab0ba46e95fc46f0a4e41b3065c0/20261020T011847-d77994fe40a8462b82252e2a50f6470f/request.json",
      "sha256": "80fcff0b74599b5cfa57c77d1bfa128b40cac7944faa8d5233fc7f9228535979",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/initial-build/5a812f7108fcf558bdc17491523594959ce6ab0ba46e95fc46f0a4e41b3065c0/20261020T011847-d77994fe40a8462b82252e2a50f6470f/result.json",
      "sha256": "c7b298d6e0cb6a9cec7f0ce228889a47b8e269d832b98ee816d5cf86b0535e16",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-1/5ee57993883e766d7c3c85d350145694ca7d1e0d1ae58dd1055690e16ce726bc/20261020T011849-babeaac54bb4488dbd8f31207bd79bfa/outputs/aturia.blend",
      "sha256": "b50fa2047784568fb8b1f9604b6a875bbe0c2d7895fbfd4d14895d551848db71",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-1/5ee57993883e766d7c3c85d350145694ca7d1e0d1ae58dd1055690e16ce726bc/20261020T011849-babeaac54bb4488dbd8f31207bd79bfa/outputs/aturia.glb",
      "sha256": "74b4e090382777b9d8b358dd1dad2df57f9751d8266437e95d9d144448cf31d1",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-1/5ee57993883e766d7c3c85d350145694ca7d1e0d1ae58dd1055690e16ce726bc/20261020T011849-babeaac54bb4488dbd8f31207bd79bfa/outputs/build-timing.json",
      "sha256": "8b5956c29d1c15241e705f6c8b4151dc521acf5dfa8de8a0886eb6e9d4f3e241",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-1/5ee57993883e766d7c3c85d350145694ca7d1e0d1ae58dd1055690e16ce726bc/20261020T011849-babeaac54bb4488dbd8f31207bd79bfa/outputs/metadata.json",
      "sha256": "e76f6ae8f31154ecf2600bf982ba3373354f3172ab4da37308da6c383cb115dd",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-1/5ee57993883e766d7c3c85d350145694ca7d1e0d1ae58dd1055690e16ce726bc/20261020T011849-babeaac54bb4488dbd8f31207bd79bfa/outputs/qa.json",
      "sha256": "16f700df8d7d6a3ec92160621b99440faaea93cf88cab0d0d512b198fff997a9",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-1/5ee57993883e766d7c3c85d350145694ca7d1e0d1ae58dd1055690e16ce726bc/20261020T011849-babeaac54bb4488dbd8f31207bd79bfa/request.json",
      "sha256": "22cd0b74925d80b1c95af4dd825c968ab0aecc5babcc8b739a84c5a335fa507f",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-1/5ee57993883e766d7c3c85d350145694ca7d1e0d1ae58dd1055690e16ce726bc/20261020T011849-babeaac54bb4488dbd8f31207bd79bfa/result.json",
      "sha256": "f34466d29c7276798b95a87e011141f3e9bbbc7ce7aac3e9a938aad0a05babe8",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-2/78ee256a91b86f7a353159f3df21088ad38ef8babcd18d8cc183ae94750afef3/20261020T011852-6adee771f72d42c98b7a73902b8f830c/outputs/aturia.blend",
      "sha256": "34d1f1f54a514f0cad1ee9364fc88b8e2d4015dd5ef3559100ca72c1f70391e5",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-2/78ee256a91b86f7a353159f3df21088ad38ef8babcd18d8cc183ae94750afef3/20261020T011852-6adee771f72d42c98b7a73902b8f830c/outputs/aturia.glb",
      "sha256": "74b4e090382777b9d8b358dd1dad2df57f9751d8266437e95d9d144448cf31d1",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-2/78ee256a91b86f7a353159f3df21088ad38ef8babcd18d8cc183ae94750afef3/20261020T011852-6adee771f72d42c98b7a73902b8f830c/outputs/build-timing.json",
      "sha256": "6ff0189b1a4b9c4847bcd0b6b9b8ca6261f487295f215749f6079779670a9347",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-2/78ee256a91b86f7a353159f3df21088ad38ef8babcd18d8cc183ae94750afef3/20261020T011852-6adee771f72d42c98b7a73902b8f830c/outputs/metadata.json",
      "sha256": "92a6351253b0d3f1f49a3bb7823c6b671b4b782eb5dda9a1d4363b5038308be9",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-2/78ee256a91b86f7a353159f3df21088ad38ef8babcd18d8cc183ae94750afef3/20261020T011852-6adee771f72d42c98b7a73902b8f830c/outputs/qa.json",
      "sha256": "a006c638a6ab7125a49e9380b96cc89c0c7b645525f296cf3d50384e3ea0d0ee",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-2/78ee256a91b86f7a353159f3df21088ad38ef8babcd18d8cc183ae94750afef3/20261020T011852-6adee771f72d42c98b7a73902b8f830c/request.json",
      "sha256": "5277a5d53f717c893d0e5c21d1d9bdf41352479042ac440ddbecb76f842a23a8",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/build/aturia/r003/semantic-rebuild-2/78ee256a91b86f7a353159f3df21088ad38ef8babcd18d8cc183ae94750afef3/20261020T011852-6adee771f72d42c98b7a73902b8f830c/result.json",
      "sha256": "58789a395aff4c25ab3d54b638ade58bb08917ead7a42d28740d87e6adb51192",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/runs/20261020T011847-1c7b3af8e322445b8338df59834ba9fc/manifest.json",
      "sha256": "de4c7e7fb473251ed532f609d799d337ff5cd0ea26db040cdd426a18b047ce7a",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/runs/runs/20261020T011847-1c7b3af8e322445b8338df59834ba9fc/summary.json",
      "sha256": "46816f3ecef3428283b3c9c3d29b6aed7a35ddad39910711f13774fcaef2b995",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/verification-commands.json",
      "sha256": "d938c058ca66a07cfea3ad9167a41c5713e5299afe6eb915415a76e8f834420a",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/verify_and_render.py",
      "sha256": "deaafc698e0d70560354274eb043486f3b736d55f80ad60fc6e38d5608e29f2d",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/repair-r003/verify_delivery.py",
      "sha256": "7732ff40965eb12090228c5f45a562ebbd55795a637cc02a9463e5de0c17617a",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/initial-build/2bd6eca4da253261390b93ed998b91903c4dae065b6bcafedbb3acce5d34855f/20261020T001413-b353f1ce3218494cad1bfcc14a0ae730/outputs/aturia.blend",
      "sha256": "7fc1baa737bf10264ea615504e6178e4854e4a3b82ee10d344985d98da2cedf5",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/initial-build/2bd6eca4da253261390b93ed998b91903c4dae065b6bcafedbb3acce5d34855f/20261020T001413-b353f1ce3218494cad1bfcc14a0ae730/outputs/aturia.glb",
      "sha256": "65f2c625334872f5e849d3bee11ff6085cc3245c93cb2cd86ba4baf13a74287b",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/initial-build/2bd6eca4da253261390b93ed998b91903c4dae065b6bcafedbb3acce5d34855f/20261020T001413-b353f1ce3218494cad1bfcc14a0ae730/outputs/build-timing.json",
      "sha256": "69cf3e29dede7affc085780c6c14fa085ae95c92b76f97abc548b8fc4e562868",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/initial-build/2bd6eca4da253261390b93ed998b91903c4dae065b6bcafedbb3acce5d34855f/20261020T001413-b353f1ce3218494cad1bfcc14a0ae730/outputs/metadata.json",
      "sha256": "61ef7ad1492b2c9b6f3c8feaf65b9afcb298e16f2df67aa548a578329c96e350",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/initial-build/2bd6eca4da253261390b93ed998b91903c4dae065b6bcafedbb3acce5d34855f/20261020T001413-b353f1ce3218494cad1bfcc14a0ae730/outputs/qa.json",
      "sha256": "1ec42ee2f8a4313b58830b1b20bce291454baf9b42b292fae3c6c1b457f04f4d",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/initial-build/2bd6eca4da253261390b93ed998b91903c4dae065b6bcafedbb3acce5d34855f/20261020T001413-b353f1ce3218494cad1bfcc14a0ae730/request.json",
      "sha256": "e158d754ba8642eb3fe0520b8d93745c288fa23cf47159b3b6798d9a0d2c66e0",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/initial-build/2bd6eca4da253261390b93ed998b91903c4dae065b6bcafedbb3acce5d34855f/20261020T001413-b353f1ce3218494cad1bfcc14a0ae730/result.json",
      "sha256": "6df1d8246251f76849117bbeb229e5a8c369969990a3dfbfe01741c472f09a04",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/initial-build/2bd6eca4da253261390b93ed998b91903c4dae065b6bcafedbb3acce5d34855f/20261020T001413-b353f1ce3218494cad1bfcc14a0ae730/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/initial-build/2bd6eca4da253261390b93ed998b91903c4dae065b6bcafedbb3acce5d34855f/20261020T001413-b353f1ce3218494cad1bfcc14a0ae730/stdout.log",
      "sha256": "e961f0fbe03c7ab8040be8795959e16cabe9efd99bd4b5ab41fc9e26926271ac",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-1/ffd1168a2a6c22f7d6fb6ae15fada8d8daebbf3f4ad865b3a64bbc5e7e9b3ebd/20261020T001415-c782355d019b410586f01d206b5abebf/outputs/aturia.blend",
      "sha256": "9b53ca6d7d163ab3e56d1c38989d8498fe95e0b10f10c7665c9ad825ff872487",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-1/ffd1168a2a6c22f7d6fb6ae15fada8d8daebbf3f4ad865b3a64bbc5e7e9b3ebd/20261020T001415-c782355d019b410586f01d206b5abebf/outputs/aturia.glb",
      "sha256": "65f2c625334872f5e849d3bee11ff6085cc3245c93cb2cd86ba4baf13a74287b",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-1/ffd1168a2a6c22f7d6fb6ae15fada8d8daebbf3f4ad865b3a64bbc5e7e9b3ebd/20261020T001415-c782355d019b410586f01d206b5abebf/outputs/build-timing.json",
      "sha256": "bb029359800e7d4a86bd699447cf77d066e7349a10146216a741a42b1bfbf187",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-1/ffd1168a2a6c22f7d6fb6ae15fada8d8daebbf3f4ad865b3a64bbc5e7e9b3ebd/20261020T001415-c782355d019b410586f01d206b5abebf/outputs/metadata.json",
      "sha256": "eb9a9f3de58421f9777273ad1dcd81aed8d84c45c1d9051fe97ce281e63c28a0",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-1/ffd1168a2a6c22f7d6fb6ae15fada8d8daebbf3f4ad865b3a64bbc5e7e9b3ebd/20261020T001415-c782355d019b410586f01d206b5abebf/outputs/qa.json",
      "sha256": "b7789e89b91de5d8f08a8f61ae31311c7fc4d3a5e4f87fa515ea162ce1b4d69a",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-1/ffd1168a2a6c22f7d6fb6ae15fada8d8daebbf3f4ad865b3a64bbc5e7e9b3ebd/20261020T001415-c782355d019b410586f01d206b5abebf/request.json",
      "sha256": "a7bb816e4a5dae3020cb3c676f8d7f48bc650e29cfbfe882454dc8931c819c28",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-1/ffd1168a2a6c22f7d6fb6ae15fada8d8daebbf3f4ad865b3a64bbc5e7e9b3ebd/20261020T001415-c782355d019b410586f01d206b5abebf/result.json",
      "sha256": "709493e44a487930eed08d1ed0f92f7f2e4fbd11dec457fef87986a412a2ce97",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-1/ffd1168a2a6c22f7d6fb6ae15fada8d8daebbf3f4ad865b3a64bbc5e7e9b3ebd/20261020T001415-c782355d019b410586f01d206b5abebf/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-1/ffd1168a2a6c22f7d6fb6ae15fada8d8daebbf3f4ad865b3a64bbc5e7e9b3ebd/20261020T001415-c782355d019b410586f01d206b5abebf/stdout.log",
      "sha256": "7a106630538c25147812e1790febdd50b48281cf714dccc159b62960249c331e",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-2/c938e85d2c83776f91dc32971f0e48b6b44f9f6007c82f7aefcbf2473cdc6d68/20261020T001417-464b6692f57f4073a605eaa870e463fa/outputs/aturia.blend",
      "sha256": "7cfc23e97a1220bc357336527c854c98f4d754708a6afad1859b5781921703a0",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-2/c938e85d2c83776f91dc32971f0e48b6b44f9f6007c82f7aefcbf2473cdc6d68/20261020T001417-464b6692f57f4073a605eaa870e463fa/outputs/aturia.glb",
      "sha256": "65f2c625334872f5e849d3bee11ff6085cc3245c93cb2cd86ba4baf13a74287b",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-2/c938e85d2c83776f91dc32971f0e48b6b44f9f6007c82f7aefcbf2473cdc6d68/20261020T001417-464b6692f57f4073a605eaa870e463fa/outputs/build-timing.json",
      "sha256": "aea0c1983b9259f1d29200ee3cc70438e360d9cd8275733a95b122547871ccc1",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-2/c938e85d2c83776f91dc32971f0e48b6b44f9f6007c82f7aefcbf2473cdc6d68/20261020T001417-464b6692f57f4073a605eaa870e463fa/outputs/metadata.json",
      "sha256": "441e3fb4878ffaf153535e7e1bd510a06580883182b94a4be0ddb6c144b5c4ad",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-2/c938e85d2c83776f91dc32971f0e48b6b44f9f6007c82f7aefcbf2473cdc6d68/20261020T001417-464b6692f57f4073a605eaa870e463fa/outputs/qa.json",
      "sha256": "920c40af0d8a86a0f495ffce5e87035c690ab0a40d42082ed1c6468996861c65",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-2/c938e85d2c83776f91dc32971f0e48b6b44f9f6007c82f7aefcbf2473cdc6d68/20261020T001417-464b6692f57f4073a605eaa870e463fa/request.json",
      "sha256": "fb2aea7bd910bf05e5e100f5a0fcc6fed93d6259815a16445d31c2a3f3b4de42",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-2/c938e85d2c83776f91dc32971f0e48b6b44f9f6007c82f7aefcbf2473cdc6d68/20261020T001417-464b6692f57f4073a605eaa870e463fa/result.json",
      "sha256": "da94fac03bfc15c61221d3db6f585527cc7c799631de2e6d43e8aacea4ef3b11",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-2/c938e85d2c83776f91dc32971f0e48b6b44f9f6007c82f7aefcbf2473cdc6d68/20261020T001417-464b6692f57f4073a605eaa870e463fa/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/build/aturia/r002/semantic-rebuild-2/c938e85d2c83776f91dc32971f0e48b6b44f9f6007c82f7aefcbf2473cdc6d68/20261020T001417-464b6692f57f4073a605eaa870e463fa/stdout.log",
      "sha256": "422efd3f436bb5c3308dc69531c797c1b7fa62e4e17b5d8d1596ce8cd639beac",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/runs/20261020T001412-e8e098718f0e41ef984f956fcef6a7bf/manifest.json",
      "sha256": "995e9e380cc6f61efa2f9755c0ef987e3df10ae91219952a6fb87c27207fdf5c",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs-r002/runs/20261020T001412-e8e098718f0e41ef984f956fcef6a7bf/summary.json",
      "sha256": "d3a173c9d4e2518fc7eef925d5da84aa5121162e03ad2fee5bd920e3243b94ea",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/initial-build/c8bfbcef6b6dea64ab3ee5bb6eb6a5d335f06fba5ff459cea9a1dec22988fdd1/20261020T001117-0463ecdce9fb46e5bcb99777ad70a3ca/outputs/aturia.blend",
      "sha256": "fd74c0b8ed476211c54d0b4b64a6377cdb681374a3e00d6ecbed381282437882",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/initial-build/c8bfbcef6b6dea64ab3ee5bb6eb6a5d335f06fba5ff459cea9a1dec22988fdd1/20261020T001117-0463ecdce9fb46e5bcb99777ad70a3ca/outputs/aturia.glb",
      "sha256": "809131be6b98ef307fe16d8ae2c7ebf5f175d52295b44b0a5fb4fde38ba3a5f6",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/initial-build/c8bfbcef6b6dea64ab3ee5bb6eb6a5d335f06fba5ff459cea9a1dec22988fdd1/20261020T001117-0463ecdce9fb46e5bcb99777ad70a3ca/outputs/build-timing.json",
      "sha256": "2fc5a35726e1e976cb03b4d370a47b21b98e18933123f360b54df1b79c0be09b",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/initial-build/c8bfbcef6b6dea64ab3ee5bb6eb6a5d335f06fba5ff459cea9a1dec22988fdd1/20261020T001117-0463ecdce9fb46e5bcb99777ad70a3ca/outputs/metadata.json",
      "sha256": "c21e6bfb3f454065e5b77c60a2b3ab79a480381ee7113909558049257d2a18e5",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/initial-build/c8bfbcef6b6dea64ab3ee5bb6eb6a5d335f06fba5ff459cea9a1dec22988fdd1/20261020T001117-0463ecdce9fb46e5bcb99777ad70a3ca/outputs/qa.json",
      "sha256": "c79412c3fde33ccd6ecd3bd8d18fa38a45ea1023eabbaf8ec811e80eb4bdfe65",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/initial-build/c8bfbcef6b6dea64ab3ee5bb6eb6a5d335f06fba5ff459cea9a1dec22988fdd1/20261020T001117-0463ecdce9fb46e5bcb99777ad70a3ca/request.json",
      "sha256": "df282ac1a3ec2f72fb976844fb8340ed7f48dc59aa5ff21754786c053488949f",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/initial-build/c8bfbcef6b6dea64ab3ee5bb6eb6a5d335f06fba5ff459cea9a1dec22988fdd1/20261020T001117-0463ecdce9fb46e5bcb99777ad70a3ca/result.json",
      "sha256": "40d872cfc8e1c9d4fc280ff51c6f02f22a0464c46579d447aa73556b1cafa98e",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/initial-build/c8bfbcef6b6dea64ab3ee5bb6eb6a5d335f06fba5ff459cea9a1dec22988fdd1/20261020T001117-0463ecdce9fb46e5bcb99777ad70a3ca/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/initial-build/c8bfbcef6b6dea64ab3ee5bb6eb6a5d335f06fba5ff459cea9a1dec22988fdd1/20261020T001117-0463ecdce9fb46e5bcb99777ad70a3ca/stdout.log",
      "sha256": "310317c8654eb04d830746330128c6bda30fa1ceddfe2dbecf0b51cd4e049587",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-1/1f827390bb11a26237f0283fd0d77a8c0cc167b087cf07b29534e582b977cce8/20261020T001119-6cb62aed998b491ca91d126c1f4c255d/outputs/aturia.blend",
      "sha256": "23d02c062377f6a10cef7b5671dc888721b8b8e7536a0f7537255e14ef4eca2b",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-1/1f827390bb11a26237f0283fd0d77a8c0cc167b087cf07b29534e582b977cce8/20261020T001119-6cb62aed998b491ca91d126c1f4c255d/outputs/aturia.glb",
      "sha256": "809131be6b98ef307fe16d8ae2c7ebf5f175d52295b44b0a5fb4fde38ba3a5f6",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-1/1f827390bb11a26237f0283fd0d77a8c0cc167b087cf07b29534e582b977cce8/20261020T001119-6cb62aed998b491ca91d126c1f4c255d/outputs/build-timing.json",
      "sha256": "b937783bfcff60c35483e7309e9531af2228142420bccc47a4f9dfdf0c0e24b3",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-1/1f827390bb11a26237f0283fd0d77a8c0cc167b087cf07b29534e582b977cce8/20261020T001119-6cb62aed998b491ca91d126c1f4c255d/outputs/metadata.json",
      "sha256": "d9054d10c5d9f35df35b48cda4d21781cfbe9d32f1efae1dcc66af7abd1048e8",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-1/1f827390bb11a26237f0283fd0d77a8c0cc167b087cf07b29534e582b977cce8/20261020T001119-6cb62aed998b491ca91d126c1f4c255d/outputs/qa.json",
      "sha256": "83f245cd0199e36aead8a6382ccb72c5bdf6d8f25fa5775180d6a4c453d84048",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-1/1f827390bb11a26237f0283fd0d77a8c0cc167b087cf07b29534e582b977cce8/20261020T001119-6cb62aed998b491ca91d126c1f4c255d/request.json",
      "sha256": "4a2525d93c2a23f10ae5e00ee379c99313b0367982cd029a44803a9554d6cc43",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-1/1f827390bb11a26237f0283fd0d77a8c0cc167b087cf07b29534e582b977cce8/20261020T001119-6cb62aed998b491ca91d126c1f4c255d/result.json",
      "sha256": "6db8b3160202763dc3e61df857ce5a2c97f6d7b54aa81a2942b2bf004d9a1c3f",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-1/1f827390bb11a26237f0283fd0d77a8c0cc167b087cf07b29534e582b977cce8/20261020T001119-6cb62aed998b491ca91d126c1f4c255d/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-1/1f827390bb11a26237f0283fd0d77a8c0cc167b087cf07b29534e582b977cce8/20261020T001119-6cb62aed998b491ca91d126c1f4c255d/stdout.log",
      "sha256": "378a7eda2b4edfdfa91250b5cac7606d03f9d8884a8d39902653c6c504d099df",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-2/59b9635d7a48e2c3677959642998918f726c4af43d8cbfb26be8ee9faeb151ec/20261020T001121-b1fb97e6e5724b148db4fe11fa080cd3/outputs/aturia.blend",
      "sha256": "8ba567aa33ee1760e1321c38345f549e8c867fd82b0b997b9200fe19389d0e23",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-2/59b9635d7a48e2c3677959642998918f726c4af43d8cbfb26be8ee9faeb151ec/20261020T001121-b1fb97e6e5724b148db4fe11fa080cd3/outputs/aturia.glb",
      "sha256": "809131be6b98ef307fe16d8ae2c7ebf5f175d52295b44b0a5fb4fde38ba3a5f6",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-2/59b9635d7a48e2c3677959642998918f726c4af43d8cbfb26be8ee9faeb151ec/20261020T001121-b1fb97e6e5724b148db4fe11fa080cd3/outputs/build-timing.json",
      "sha256": "8c19c7658b80551e5f3874254e592b11642dbda368251a6b5a1e9632948f3317",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-2/59b9635d7a48e2c3677959642998918f726c4af43d8cbfb26be8ee9faeb151ec/20261020T001121-b1fb97e6e5724b148db4fe11fa080cd3/outputs/metadata.json",
      "sha256": "9936947c586ca3d142393b286db4905df73e6df467576784951b8de7e6d7135e",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-2/59b9635d7a48e2c3677959642998918f726c4af43d8cbfb26be8ee9faeb151ec/20261020T001121-b1fb97e6e5724b148db4fe11fa080cd3/outputs/qa.json",
      "sha256": "b162eec6b8f49fa62eb2f41b6f3d48c8a1965e2600ca0ab86a7b69c96bd0274b",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-2/59b9635d7a48e2c3677959642998918f726c4af43d8cbfb26be8ee9faeb151ec/20261020T001121-b1fb97e6e5724b148db4fe11fa080cd3/request.json",
      "sha256": "4582c028b9d9b52e18311de069d417a75e74b74f21a04259c7d2eb67140192c4",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-2/59b9635d7a48e2c3677959642998918f726c4af43d8cbfb26be8ee9faeb151ec/20261020T001121-b1fb97e6e5724b148db4fe11fa080cd3/result.json",
      "sha256": "7d69db8b0c80162fe0add8dc5cbfd6c26ceb166558288e09c9ef91980b957141",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-2/59b9635d7a48e2c3677959642998918f726c4af43d8cbfb26be8ee9faeb151ec/20261020T001121-b1fb97e6e5724b148db4fe11fa080cd3/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/build/aturia/r001/semantic-rebuild-2/59b9635d7a48e2c3677959642998918f726c4af43d8cbfb26be8ee9faeb151ec/20261020T001121-b1fb97e6e5724b148db4fe11fa080cd3/stdout.log",
      "sha256": "909af6ca669126118becc4c23ad462416574f5463b3a38ad382e2dfce6b74d7d",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/runs/20261020T001116-2f7f682ec967417a90f22b215cc5d94b/manifest.json",
      "sha256": "e065c3cff4ccdc977e3d97f1e74660fb1f69ae27e8c6a948a4704bacb2dd109a",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/runs/runs/20261020T001116-2f7f682ec967417a90f22b215cc5d94b/summary.json",
      "sha256": "dafeb3d6bf0f1a6dfc5c0d11ba767ade69dda4c37ff427f55206c5918d1cccf8",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/source-access.json",
      "sha256": "aa65c731a5d9f3c49530e9e8a3afc4a3b523b559768df6a39e557460cf5f0010",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/verify-r002.py",
      "sha256": "1d03f767059fe3561fadd8558deee7f920efcb79bfbab2b13cc822a83b1b0eab",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-52/aturia/verify.py",
      "sha256": "bf07782f465f6376b3bdd3a1a6c1cd101b5ddea89de765c366c0a0ed88be23d3",
      "origin": "source",
      "owner": "aturia"
    },
    {
      "path": "qa/batch52-aturia-r003-diff-20261020/report.md",
      "sha256": "4061c89e0fd450ed4fbaef5bf9609c516c98f29ad27cedfcb2207f6c58797c36",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-aturia-r003-diff-20261020/review-evidence.json",
      "sha256": "0de129c580b0dbfa7dc65128f1cbdc3c411958507e4b9148e5f42f20d34f0954",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-aturia-repair-20261020/capture/render-report.json",
      "sha256": "0143db47a04a3b357d9a03e6814b51a7b897321ee8acc4813c8e3441311e6e02",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-aturia-repair-20261020/capture/index.json",
      "sha256": "9903a35e0e68a5e0846aa36d14ff43a567ba74375260eae3d75c4d382e57e516",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-aturia-repair-20261020/capture-integrity-verification.json",
      "sha256": "422d2e33d762e891336adec45b3299e8cdfd3329bf5da7807f30d590ca9984f4",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-aturia-repair-20261020/capture-projection-audit.json",
      "sha256": "c0d16a5b11635d7fcd848cfd23b8f8d6076cb3c8e5d5ef23470228c9a5feca66",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-aturia-repair-20261020/capture-independent-review.json",
      "sha256": "c406877c97a32df7da4768916b267704dcb0ef14f6b12ca0f7cbe9e0d3bc2c1d",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch52-aturia-repair-20261020/capture/references/aturia.png",
      "sha256": "a2039d069363d05214fbb5564ca331c6cf78c2e197e7fb9080cb90eff31bef33",
      "origin": "release",
      "owner": "aturia"
    }
  ],
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  }
};
export const BATCH53_RELEASE = {
  "version": 1,
  "scope": "batch53-20261020",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "provider_generation_timestamp": "unknown",
  "source_commit": "0d4d6153955b2ca8809d343d63628f55b493b074",
  "review_commit": "19bf7332eb3cf5138a8b91820d495599f790d727",
  "source_bundle": {
    "path": "qa/batch53-20261020/source-bundle.json",
    "sha256": "36876c8c77236f969c378396d9e8aeacb0ec415c5f2ed59112537e36622fcb64"
  },
  "review": {
    "path": "qa/continuous-small-life-round18-20261020/batch-53/INDEPENDENT-REVIEW.md",
    "sha256": "495ac88acb3002de206a84dcd383206d7b67c5c7a7da7f4c553fa6f8d45ac2c1"
  },
  "capture": {
    "report": {
      "path": "qa/batch53-20261020/capture/render-report.json",
      "sha256": "0143db47a04a3b357d9a03e6814b51a7b897321ee8acc4813c8e3441311e6e02"
    },
    "index": {
      "path": "qa/batch53-20261020/capture/index.json",
      "sha256": "9903a35e0e68a5e0846aa36d14ff43a567ba74375260eae3d75c4d382e57e516"
    },
    "packager_integrity": {
      "path": "qa/batch53-20261020/capture-integrity-verification.json",
      "sha256": "422d2e33d762e891336adec45b3299e8cdfd3329bf5da7807f30d590ca9984f4"
    },
    "projection_audit": {
      "path": "qa/batch53-20261020/capture-projection-audit.json",
      "sha256": "c0d16a5b11635d7fcd848cfd23b8f8d6076cb3c8e5d5ef23470228c9a5feca66"
    },
    "independent_review": {
      "path": "qa/batch53-20261020/capture-independent-review.json",
      "sha256": "c406877c97a32df7da4768916b267704dcb0ef14f6b12ca0f7cbe9e0d3bc2c1d"
    }
  },
  "additions": [
    {
      "id": "hypoturrilites",
      "revision": "r001",
      "source_commit": "0d4d6153955b2ca8809d343d63628f55b493b074",
      "review_commit": "19bf7332eb3cf5138a8b91820d495599f790d727",
      "metadata": {
        "path": "assets/additions/hypoturrilites/batch53-20261020/release-metadata.json",
        "sha256": "c754b99eaa38c2cd998a75f99a836d6496d57a4c1da278258c3338d852d9a3a3"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/metadata.json",
        "sha256": "c1f79f94056ed6a401f7b1552d7847befc1adf0da58b65c7a1a35f5f5f728277"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/candidate.json",
        "sha256": "180655885a9d7ca514d95843acd7dc43b8ece67f0e34fbfc6496d6ab65bdd3b9"
      },
      "review": {
        "path": "qa/continuous-small-life-round18-20261020/batch-53/INDEPENDENT-REVIEW.md",
        "sha256": "495ac88acb3002de206a84dcd383206d7b67c5c7a7da7f4c553fa6f8d45ac2c1"
      },
      "capture_reference": {
        "path": "qa/batch53-20261020/capture/references/hypoturrilites.png",
        "sha256": "0a293440fe77c4be25567736206993d4739b32650d3fdbd39d3ad4942d1d5a7a"
      }
    },
    {
      "id": "iodes-brownii",
      "revision": "r001",
      "source_commit": "0d4d6153955b2ca8809d343d63628f55b493b074",
      "review_commit": "19bf7332eb3cf5138a8b91820d495599f790d727",
      "metadata": {
        "path": "assets/additions/iodes-brownii/batch53-20261020/release-metadata.json",
        "sha256": "f9c95baac050b3a3bee701ce45afab87fd87b52a35c7509d5329ef3a1fd38b37"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/metadata.json",
        "sha256": "66449e3ced5d9a08ea61f30e22a21b61dfcc36dd8fb9fa6a2039e034b16975bd"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/candidate.json",
        "sha256": "28e9d69f5f07fcafc438cc2bedbc8e6a80c4cc92cff5b6062e0bc9056d497370"
      },
      "review": {
        "path": "qa/continuous-small-life-round18-20261020/batch-53/INDEPENDENT-REVIEW.md",
        "sha256": "495ac88acb3002de206a84dcd383206d7b67c5c7a7da7f4c553fa6f8d45ac2c1"
      },
      "capture_reference": {
        "path": "qa/batch53-20261020/capture/references/iodes-brownii.png",
        "sha256": "2017638fead71e83e5217dad32d55d19ab721a7375ae64a4ea5171d010a98818"
      }
    },
    {
      "id": "welded-ignimbrite-outcrop",
      "revision": "r001",
      "source_commit": "0d4d6153955b2ca8809d343d63628f55b493b074",
      "review_commit": "19bf7332eb3cf5138a8b91820d495599f790d727",
      "metadata": {
        "path": "assets/additions/welded-ignimbrite-outcrop/batch53-20261020/release-metadata.json",
        "sha256": "6ce64a44ef4ef4bfd776337354566248f0f84f882987aa4d80da6594dbb490e9"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/metadata.json",
        "sha256": "481b3e82e69a7b62825ace8559cad5857dd7a83ac3cb5211d7705d7e1adb62bc"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/candidate.json",
        "sha256": "f44c35763d8c7b7142bbe3230897a927a996e977eb931802748e39bd2194ba05"
      },
      "review": {
        "path": "qa/continuous-small-life-round18-20261020/batch-53/INDEPENDENT-REVIEW.md",
        "sha256": "495ac88acb3002de206a84dcd383206d7b67c5c7a7da7f4c553fa6f8d45ac2c1"
      },
      "capture_reference": {
        "path": "qa/batch53-20261020/capture/references/welded-ignimbrite-outcrop.png",
        "sha256": "f652b5f2db5e8e1a74452cbdb96b569308d9e83c8ee022b0c4cf17a8fa80150d"
      }
    },
    {
      "id": "halopoa-furrowed-burrow",
      "revision": "r001",
      "source_commit": "0d4d6153955b2ca8809d343d63628f55b493b074",
      "review_commit": "19bf7332eb3cf5138a8b91820d495599f790d727",
      "metadata": {
        "path": "assets/additions/halopoa-furrowed-burrow/batch53-20261020/release-metadata.json",
        "sha256": "8e1d4ea49e65f657567c6fbf5aa7179c899c6366e0390b31d2d93fafb7d9ca38"
      },
      "source_metadata": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/metadata.json",
        "sha256": "01bf918df84837da1dae0bd14490d07dfacd9991aec8b2156e37179ed40adb47"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/candidate.json",
        "sha256": "68cddfb268d063f9f61fb786441446ba463e6049f839dddd02f6a346907d6c31"
      },
      "review": {
        "path": "qa/continuous-small-life-round18-20261020/batch-53/INDEPENDENT-REVIEW.md",
        "sha256": "495ac88acb3002de206a84dcd383206d7b67c5c7a7da7f4c553fa6f8d45ac2c1"
      },
      "capture_reference": {
        "path": "qa/batch53-20261020/capture/references/halopoa-furrowed-burrow.png",
        "sha256": "e13289147dfec2b491439bce5edfde7683ae1766ae0008b3dc18a75872a7fbed"
      }
    }
  ],
  "files": [
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/HANDOFF.md",
      "sha256": "1adb3a1b916c0340f0c6a3f657f034e75befdd5e4852aaf0afae8ed6995a0ce9",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/LICENSE.txt",
      "sha256": "e3d79dd430ea798cc905fac6d635fb214aaeefec982085fd9aa883291625f863",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/brief.json",
      "sha256": "5689fc5e38a0aa45183fb5d1d4e193d6d29697cadb4ce855fe7a12a636ea200b",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/brief.md",
      "sha256": "d28962b0b97f3cc3b3947068d6d58db5348304fc4fbfcb0837c27c68f8ba32cf",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/candidate.json",
      "sha256": "68cddfb268d063f9f61fb786441446ba463e6049f839dddd02f6a346907d6c31",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/checksums.sha256",
      "sha256": "4523c45a730ad5ccae92185967d57a4c6e5d4f5980e5e964f4d95e54edf1ce36",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/concept-checker.report.json",
      "sha256": "8f0660f52718428bd22258d8f9a7edf1c095de122d7e24c8a148740db356f4c9",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/concept-complete-checker.report.json",
      "sha256": "8f0660f52718428bd22258d8f9a7edf1c095de122d7e24c8a148740db356f4c9",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/concept-evidence.json",
      "sha256": "e574ff0e35c7579c1c721212a56685b509179ea952cb0cc1c672602b0f460ded",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/concept-inspection.json",
      "sha256": "3c24b8f7a0bcb464011df24be948e061a2fbccbbe665bcea76d98bd2db7b9f23",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/concepts/generation-record.json",
      "sha256": "ced46ee3afaad114ea63039078705dab63350767c4ec8b527649d9e66dfd112c",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/concepts/original.png",
      "sha256": "10d34a7be437bf9b1627a324ad628c1e604e81477cb16cc1dc9ae6221008f422",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/concepts/prompt.txt",
      "sha256": "50ef37aa95eac68014d5cacb4d02abff0f81d215021561f6db39ac695f5ad182",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/concepts/tool-result-metadata.json",
      "sha256": "28973b103d1b7bf99b797cabc43973d6aa323b9ed35223f4b772855924fd9fa0",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/config.json",
      "sha256": "cdc44924b5f7affccddd8344a6c2148d82653b844927e76defeb593043d57cab",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/contact-sheet.jpg",
      "sha256": "9022b59e2b397395acc597c3352fe40f80f8c2f5a76f02a0b23174bf5ba0ee1c",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/delivery-binding.json",
      "sha256": "7177da83b5cbb7cf5f506cda4f8f39c2ba290c0860ad6db36809f37bd93d6fcb",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/delivery-brief.json",
      "sha256": "742673d0dd23386af99844097acc53b1062a2e9509e83c33e9215751d3a2363c",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/dependency-hashes.json",
      "sha256": "c45f27827abdbc59df439060221f4ded82e585c4df9bf53e2fdc254229519436",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/generator.py",
      "sha256": "eb2d60ec78322e205d41eb2691d9133f6a7c9c0ff1eb3b3afccdba4ceeaada34",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/gltf-validator.report.json",
      "sha256": "ab9f628195e0522e040ae4dd699dc99416f5ea891a83ff91b067c0a2cb26b341",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/halopoa-furrowed-burrow.blend",
      "sha256": "6c538d87b579f9a32fe28d2a21c19f6937927108773f0c1774bb63ebd7699714",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/halopoa-furrowed-burrow.glb",
      "sha256": "42e7fd3105d689c27d3bdf7de6ea0fbfc95094d0645e840b1b66062ca8fd54f6",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/maker-inspection.json",
      "sha256": "ebde73328a4080ad0b70a564782f2f103056e276b1c40bac6e4d1d3e18e1b3fa",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/maker-review.md",
      "sha256": "c6912c08fcee88331eb19f6d9c039bac85edefee60ae25f427983fcc5c9b9a57",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/metadata.json",
      "sha256": "01bf918df84837da1dae0bd14490d07dfacd9991aec8b2156e37179ed40adb47",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/metrics.json",
      "sha256": "f659145ccd9d3d38e2572da985edf6445837ea215d73b99335b8080d3f9905cc",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/modeling-freeze.json",
      "sha256": "488fc7fcce94a6484f9b7dace48d014fe51c70f9479147f059cbc53bb5ad9ea9",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/preflight-contract.report.json",
      "sha256": "8906287e2a8cb38777f80b880f9ea63f367117f10555d2697d1c5955097242ec",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/preview-hero.png",
      "sha256": "7b2885b06c086a5781999ab201c03ac2da0e7a1b59d9dec316b0a585281c224b",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/profile-approved-checker.report.json",
      "sha256": "4d7b31ff682f104c86177de3c7976c0626a113bfea5df7db6fd7b105500cff75",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/profile-checker.report.json",
      "sha256": "4d7b31ff682f104c86177de3c7976c0626a113bfea5df7db6fd7b105500cff75",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/profile-contract.json",
      "sha256": "f2719d54792e4b1393e34cf3e403b20bbb305f43f248dd83e513cfc3b71a6b2a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/project-checker.report.json",
      "sha256": "a7ece4635dc3944fd8ff9c131cc49eddd58d9ac2d18df0a2d7940ba9a7979da1",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/proof-renderer.py",
      "sha256": "259b1cea4838a1fa37c42610800f8f75b9b5fffc8f8d7770be1c9931b173d2f3",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/qa.json",
      "sha256": "0577b75e7ae7105eb1cac074fa6e633924af4afceab1586ec23e4f8469e36e7a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/rebuild-1.report.json",
      "sha256": "4892070d9ba80f38f2a9090005f710316ecd0729b28fb021311d8d2dacd860f2",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/rebuild-2.report.json",
      "sha256": "3c100fc66967c91879d6e0ada0b090dc1c9a45730e5bce2050a84305a6fbf173",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/reference-access.json",
      "sha256": "e8e57239e8592d6a796a7a3b6470eec723dfc3bf9516ef4d60730f704144e149",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/reference-profile-mapping.json",
      "sha256": "48724e0645a1d6a03fc46c266ecf7651e8a2fadaa491908a420453a0f7ac143f",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/references-profile.json",
      "sha256": "f0f3768cb8277e9954ee277e8db460bbd01f9c50b8c03e2c36acf6efb420113b",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/references.json",
      "sha256": "38303926bba47bd021b17da151fe2aedade08f1d3cd2f0a1b40df698d8356146",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/repair-notes.md",
      "sha256": "d4449259d8a3bffd765c38d1478ee640c9f3aa6583b99e1ab15be3bf5573f021",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/runtime/front.png",
      "sha256": "ff933eb4ca1298e6adab231c8b1c09474065afcd2c8ad42d8d8ccb5a9247cb8d",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/runtime/hero.png",
      "sha256": "318f2c9b95543a46f7c4f142d44a1bd2d5c7fa82968fdd55791e4988beafb154",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/runtime/reversehero.png",
      "sha256": "c96e8842d75c086e0df13ae415d4ceb1f0469a833eb9d2940fee07bd29470ccc",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/runtime/runtime-report.json",
      "sha256": "647830aaa5c89f851c3758e4463d551559a0588ec67360d90d0211f9b640f1c1",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/runtime/scene-9.png",
      "sha256": "7b03ca1700da26862587f6759d621261a35ea8721054a10c6ec718de205d6188",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/runtime/side.png",
      "sha256": "4d4bb5388147221e89603c4542c818bad52708b9087382fc84b1865952672a35",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/runtime/top.png",
      "sha256": "be7fa83e45c15c8eb105360ea4474cd2ff6d0d6557056ae6c095677f074afb3e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/source-export.report.json",
      "sha256": "fdd30511542b56ba6e3155c86ce438feedad9ffe6ce4ef525476022f2a5b4a68",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/source-measurements.json",
      "sha256": "2bd587e00cbca3d00696dcd34f7a21e575eedcef9ecbf23a711ab18a0baddac9",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/clay.png",
      "sha256": "3d62cacef0ba85517e2eab94920e57d5a4d2ddb919952da30f0217797dc72ea2",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/derivation.json",
      "sha256": "64f03b20f8e06343cb46c51f6c1ec05508096fbffc8b6e3d4e4470d001d72064",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/front.png",
      "sha256": "ee27435d43351cf3c760bd319cedd6a8377884d2b19cc9d2e31b035890b8d08f",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/hero.png",
      "sha256": "7b2885b06c086a5781999ab201c03ac2da0e7a1b59d9dec316b0a585281c224b",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/rear.png",
      "sha256": "0f4f30a558dade12f113dffd91b62917888666395e8c0e5caca827a222e5ea35",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/render-config.json",
      "sha256": "7b85877771fad4324ee42ebef408343b0f0344b7610724f6c85098b54128ff34",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/render-manifest.json",
      "sha256": "0995779490dd60bcca9a34fb469f37f17c440b82684853100dd0904b71126154",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/reversehero.png",
      "sha256": "d846609de7f11e588a9046b9d6283c14cce971c9ebfa71e590692f740fa3610c",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/side.png",
      "sha256": "e0640bdeabc08f57502ce2d82137e93f0d32b83695bbe08422103f3ce1293402",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/silhouette.png",
      "sha256": "eb86167ca8be4ce80ad724b64b6f209cd00aa7e054d2c82265defd04d8f3c9b0",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views-static/top.png",
      "sha256": "d9e4ed2fafba4da7296ab597bb2554ef9681cc2c0818b9ebbe5ad534760eaa42",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/clay.png",
      "sha256": "3d62cacef0ba85517e2eab94920e57d5a4d2ddb919952da30f0217797dc72ea2",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/claytop.png",
      "sha256": "86fcee5bebe2dea57b404321c689623836c03706d80cc2b4c83b3c11b88dfd03",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/front.png",
      "sha256": "ee27435d43351cf3c760bd319cedd6a8377884d2b19cc9d2e31b035890b8d08f",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/hero.png",
      "sha256": "7b2885b06c086a5781999ab201c03ac2da0e7a1b59d9dec316b0a585281c224b",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/rear.png",
      "sha256": "0f4f30a558dade12f113dffd91b62917888666395e8c0e5caca827a222e5ea35",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/render-config.json",
      "sha256": "9ec0d976697560473bd86daa24aba5fe5a880a7cf086ed75ab2970b764bba15a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/render-manifest.json",
      "sha256": "8318d92b53cd60a06bbce6ff0a3a92af63f0b8271aa9bb198fa0634b3639ed1e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/reversehero.png",
      "sha256": "d846609de7f11e588a9046b9d6283c14cce971c9ebfa71e590692f740fa3610c",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/side.png",
      "sha256": "e0640bdeabc08f57502ce2d82137e93f0d32b83695bbe08422103f3ce1293402",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/silhouette.png",
      "sha256": "eb86167ca8be4ce80ad724b64b6f209cd00aa7e054d2c82265defd04d8f3c9b0",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/top.png",
      "sha256": "d9e4ed2fafba4da7296ab597bb2554ef9681cc2c0818b9ebbe5ad534760eaa42",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/views/turntable.json",
      "sha256": "b7d8516352bd124985fd276e2acfef85f917bbded8b6e34ed7f2d0910d6edcce",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/halopoa-furrowed-burrow/r001/warning-review.json",
      "sha256": "d4bb31507b9dbbb33a01c6c8f7771bb4620c91f790a483177a3c5316e94063cc",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/HANDOFF.md",
      "sha256": "a43797efa8bff28c76389c98a81113b98f374884588c9f4d2c196e513dfad69e",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/LICENSE.txt",
      "sha256": "e3d79dd430ea798cc905fac6d635fb214aaeefec982085fd9aa883291625f863",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/brief.json",
      "sha256": "3b9a0458f082072e754e2921e401209a6bf12372484ccfbc01aa62d7008cf8e8",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/brief.md",
      "sha256": "a0585fa32c5bb70888522a07f605cda9dc57beef61b9ca96832f117fe4c39980",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/candidate.json",
      "sha256": "180655885a9d7ca514d95843acd7dc43b8ece67f0e34fbfc6496d6ab65bdd3b9",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/checksums.sha256",
      "sha256": "9c80c4015d932de59612cb0cfc55a2bf3b0c0503207e8fb8059761960d138f6a",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/concept-checker.report.json",
      "sha256": "bb6aa858db12b96ae7c9f732c5fd58a7cc8bd39ed440e2380b696446b0a24476",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/concept-complete-checker.report.json",
      "sha256": "bb6aa858db12b96ae7c9f732c5fd58a7cc8bd39ed440e2380b696446b0a24476",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/concept-evidence.json",
      "sha256": "6e85f25420364a032d93fec091bd9ee0b0ab35b27def0ecc53bf7db67bb95311",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/concept-inspection.json",
      "sha256": "2e53c7bf3de91e93ab3269c5c1f614f91383dded902b8061129b575508635aa1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/concepts/generation-record.json",
      "sha256": "9f41792a81694acf71a0383150c70d02322bfeab378b6d6d9e505a510f454d39",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/concepts/original.png",
      "sha256": "26c9d2112254ac08110582054a850bd2761f1d72f9f63f8134b6cfe0f5116042",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/concepts/prompt.txt",
      "sha256": "ca350d496f5e26e43fb59c8a9ac1df55ddce77fa3a3104eb3e3c5f0ed7385eab",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/concepts/tool-result-metadata.json",
      "sha256": "70a0232a7474214f3473b2b39b894f4a9517fd73b1f7f36f081c3efdb71b6f1c",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/config.json",
      "sha256": "7d91dd7ecb73c10ceb69cb931c4423ee4ad56e84d88af11e8fb18c71428727d1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/contact-sheet.jpg",
      "sha256": "2aa88c34ff8f7daeae987bc1f57543cffbafb7afb1683429d5132daa0049c83a",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/delivery-binding.json",
      "sha256": "8d862dca61200fdbe57dbc37ce2e2910357003d35d46ec5e6b39e65bada70e04",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/delivery-brief.json",
      "sha256": "2cabe7cc13d7b1dd40932634bf606d7c063475b3200da8825004d89d4e851961",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/dependency-hashes.json",
      "sha256": "6cbb545bf8967a9da5c2d21eb24603dde75087b59d1b7d6dfe0266724b8a9229",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/generator.py",
      "sha256": "34d48adcee75422948f5b1fe18d480f50ae4d050ea9e853c92b32586496d3239",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/gltf-validator.report.json",
      "sha256": "e8f17c5a7f170bf2dd392323923b60b5b59ca8d7d261c4282743cfe4da9c2eeb",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/hypoturrilites.blend",
      "sha256": "3aaba1ae3140edd3730a3800fb271a131b3891aa8919d95a0efaff11dfb139cc",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/hypoturrilites.glb",
      "sha256": "23d62a058ebc966e287d6a70feec6c041e30a4c2314418e7504ca59258d56bc1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/maker-inspection.json",
      "sha256": "b3c36b2fb02ffff056bfc8987337052836ce350d2a6726abf4292b3b38eff3e5",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/maker-review.md",
      "sha256": "b52f73259e36cc5019314d1d29018ff716c387710c99649692314a9e154f53e4",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/metadata.json",
      "sha256": "c1f79f94056ed6a401f7b1552d7847befc1adf0da58b65c7a1a35f5f5f728277",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/metrics.json",
      "sha256": "2952755c2849d404fe4cb0afb22114c8a71eafbde40861a026780a9b550d6e23",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/modeling-freeze.json",
      "sha256": "c7013b5fbe1ee6ef379e080d81febf62e831240cbc03e57c951cb93224dfa959",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/preflight-contract.report.json",
      "sha256": "766a0657c10349327b461620e921747fc92c63b77880d8a594c6a4e9666b9975",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/preview-hero.png",
      "sha256": "a9286f41032d398346dcce709a19693ad2bcaa042924846caf8f4bf1b78b0551",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/profile-approved-checker.report.json",
      "sha256": "195f9cc87e73f2da3e1363b0018beed19f098140dee5099df7c7d57e4f1aa0f2",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/profile-checker.report.json",
      "sha256": "195f9cc87e73f2da3e1363b0018beed19f098140dee5099df7c7d57e4f1aa0f2",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/profile-contract.json",
      "sha256": "fbb5edc3e923cddcb08dd66a2c738294168203b104f7eabbf014b34be21540e1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/project-checker.report.json",
      "sha256": "b2d85229b93e934a5ccdcfdb94c8256e1b5609b8faa4cae119e073146d3a5885",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/proof-renderer.py",
      "sha256": "8cfbb47c5e9b95c27785a23e4e9f7f20f2730cff8803c12e40a6a08f7b498b0c",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/qa.json",
      "sha256": "0c2da26097d68e8f4a593b5ddb26120ebe80647d7aadc9301b082f14c53b120b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/rebuild-1.report.json",
      "sha256": "297a2365c20eabe18cecc9e4d377e0f1550d6fe4098194bc367e1e11a5b42690",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/rebuild-2.report.json",
      "sha256": "8bf5ab9f10909f65933f80456f65a9b7d919817d876c0158e180f563357ff28b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/reference-access.json",
      "sha256": "e215461056884a55457a0fae0f1bbef9ae91f5f538e2b16b861cc0fd6d54bdd4",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/reference-profile-mapping.json",
      "sha256": "2b1a3e2d50a557b1ae3595e3d30c74f1fa926964a5526b13fb6ff48be451076e",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/references-profile.json",
      "sha256": "c202c1c1a656dc05b291d5194b1c6755c42d4a6d8592f519e16b7758571e26fc",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/references.json",
      "sha256": "a9f2fb257e6acc84e1deae423a6505227f5c32d2b92799e3b7edc080137bc7fb",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/repair-notes.md",
      "sha256": "dd372bfd9458c0156d7cd97af61c3bc07287910a19d84ad4be899752ea3ebe95",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/runtime/front.png",
      "sha256": "dea4fbd620df6b15a5ebd754d1b447a1216da3d8f2019b863672c26c5bb0dfa3",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/runtime/hero.png",
      "sha256": "bcb680e270247cc25ae77e4d21d0d346b84ea312bbb3861aca40e3a91bad5361",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/runtime/reversehero.png",
      "sha256": "4f0b8e15e6e9964ba675b283fd276df0f7568f0f0038bd772cb11fb7d6434c7f",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/runtime/runtime-report.json",
      "sha256": "3cfe43914c5b9a21c44e96b486eab1141e9f29caabf7a20319faa85c8492a345",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/runtime/scene-9.png",
      "sha256": "f76a20697a86d8dbb636778a05d1bd7886acde96c279a6a3b51732f94e51f192",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/runtime/side.png",
      "sha256": "5c8eb481013cd9136445ba2f995f7605f6120c15a682a68a03539f6d5cc39f95",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/runtime/top.png",
      "sha256": "03f564875426e199b3dfd4102129c3044eeda29c6219734189eb232f11236ced",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/source-export.report.json",
      "sha256": "c3ba0437340f547769f1844926a2e90040c7f51fb5ec089f1091f4271bd2993c",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/source-measurements.json",
      "sha256": "d6e6f749f68c34389a94ee62fdbebd28b4883c5f33f34972630aa4887b1c03d5",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/clay.png",
      "sha256": "2d95c4aa924bdfbd69373b5d1d899315089445eda56d2399d817819fa44facf2",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/derivation.json",
      "sha256": "d8fb8e72a561d0ee2b1c0bd396b51d5a437c153678671c60694cb77e0a51a28b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/front.png",
      "sha256": "ab28c5a336eea1602dd0cacdfc3f08d813f69fb2576e2c44e38dae9c6c6aa919",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/hero.png",
      "sha256": "a9286f41032d398346dcce709a19693ad2bcaa042924846caf8f4bf1b78b0551",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/rear.png",
      "sha256": "21f62269379afa61a2a3624fef5a6a711e020edd584fb4fa2052ec4e8bfb2870",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/render-config.json",
      "sha256": "5241a2e54f782f35d8ae0badf813fffcf0ee0d02fcba1be5f3436cdbd218171f",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/render-manifest.json",
      "sha256": "f9b81595a09b19d710408f6cabe93866674b4542715c165ff1cbfe6784be0bbe",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/reversehero.png",
      "sha256": "6ddb63b1201b2e3470a8f2b403cd601480c03178994d7152a5e2b868c6830abb",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/side.png",
      "sha256": "f46b7d855512d2e80a87a5c64978ab271cd686b24e4ec32b7428681f43a77270",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/silhouette.png",
      "sha256": "c2526b667c50fa33cd22611cd02e30112caab588efee5bdd01cacde83aa03376",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views-static/top.png",
      "sha256": "b7e0302a343b59d7d095994e2ea9e6b6d253ce8ebf1b48dd2e5284f79ac8b3b6",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/clay.png",
      "sha256": "2d95c4aa924bdfbd69373b5d1d899315089445eda56d2399d817819fa44facf2",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/front.png",
      "sha256": "ab28c5a336eea1602dd0cacdfc3f08d813f69fb2576e2c44e38dae9c6c6aa919",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/hero.png",
      "sha256": "a9286f41032d398346dcce709a19693ad2bcaa042924846caf8f4bf1b78b0551",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/rear.png",
      "sha256": "21f62269379afa61a2a3624fef5a6a711e020edd584fb4fa2052ec4e8bfb2870",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/render-config.json",
      "sha256": "560b9e598946920926566c5942286b401d45ae5c2116cf4c379dd4086410b436",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/render-manifest.json",
      "sha256": "affee67658c99303991082e3cc3ffc4cb88f6fb3d0c6da18f6ca583eebde7705",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/reversehero.png",
      "sha256": "6ddb63b1201b2e3470a8f2b403cd601480c03178994d7152a5e2b868c6830abb",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/side.png",
      "sha256": "f46b7d855512d2e80a87a5c64978ab271cd686b24e4ec32b7428681f43a77270",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/silhouette.png",
      "sha256": "c2526b667c50fa33cd22611cd02e30112caab588efee5bdd01cacde83aa03376",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/top.png",
      "sha256": "b7e0302a343b59d7d095994e2ea9e6b6d253ce8ebf1b48dd2e5284f79ac8b3b6",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/views/turntable.json",
      "sha256": "796e3b4264c35123bf0528f163e31107485a421dd899ca0f7cb5d48b0c783f8a",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/hypoturrilites/r001/warning-review.json",
      "sha256": "6b1dc32a6e2b95560ecf6d92ccac4fcdd1f7962913adafbc28210b35540f6683",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/HANDOFF.md",
      "sha256": "982a83776ba00928b5a5421bb8e51b2d522e6dc8eb25fe668ff73b4a63b4c200",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/LICENSE.txt",
      "sha256": "e3d79dd430ea798cc905fac6d635fb214aaeefec982085fd9aa883291625f863",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/brief.json",
      "sha256": "15c04046f1e56575f6b3eba010e502149651de5fd37e06769ba7376042ae7299",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/brief.md",
      "sha256": "f5bb303e7c7c407d221e47f78e6bc35c9b5fb2f93a1d8789cdb9d8d861fa1397",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/candidate.json",
      "sha256": "28e9d69f5f07fcafc438cc2bedbc8e6a80c4cc92cff5b6062e0bc9056d497370",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/checksums.sha256",
      "sha256": "5d862e4a8f2c8ad523c13e633bf36906fb8410c76c9fe533b6f41ec3bb588309",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/concept-checker.report.json",
      "sha256": "4e614d9b0f83516a4f6c964b01ab117ba797c3113a007bc8bfffa9e4ee223fbe",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/concept-complete-checker.report.json",
      "sha256": "4e614d9b0f83516a4f6c964b01ab117ba797c3113a007bc8bfffa9e4ee223fbe",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/concept-evidence.json",
      "sha256": "03d1f5673baf073782f0f187a59dac86ae6dbbabaa8488be2a23ad49ece741b4",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/concept-inspection.json",
      "sha256": "38f2865221e037f7e115439012a22372c0211f88bf5eda7207b39249f6243b06",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/concepts/generation-record.json",
      "sha256": "aa044a72e87afe6af1a261859b144722e4a1b1163df3448ec9af9b179a12d6ff",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/concepts/original.png",
      "sha256": "81d1648c96cdc3780c1f07e13fc0afb0ce9383c9ca4626e1fc2afa1edc4ceeca",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/concepts/prompt.txt",
      "sha256": "6b5badbcb0ddba9e8dc3104c7ff8fefb53634776bcbabe1e0c7b71083ee4b1d9",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/concepts/tool-result-metadata.json",
      "sha256": "737c4d79ffd65baa585866bac9cec203da941093eaedbcec012bcf10d7a2c9ea",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/config.json",
      "sha256": "26a870b9aa75713d11adacca1379076cd88c3c5dd9087c05a2c4ae883189c133",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/contact-sheet.jpg",
      "sha256": "6300bb4841b0e53beef22e0cb4c343de9f3a6110817a8e94ead44571bcca0c40",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/delivery-binding.json",
      "sha256": "c8674ec00833c47f637ce14b7486ac5fcf49d5276a5363df30dc46884f29f4de",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/delivery-brief.json",
      "sha256": "88ed0271315334f99988190527ad7630e35d29b9b00f467c79b4fc96d22baa1a",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/dependency-hashes.json",
      "sha256": "a3fc8d55c2d85657e7378c1bd28aa77a10d339ffecba7810943c2a97e595be86",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/generator.py",
      "sha256": "fb3018d9ed4b7d4a6017d189c2e2318552378fd364bf2b445fde9d8fb6a494e8",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/gltf-validator.report.json",
      "sha256": "06e38dc06d9fb667f3bf23f3576857f54cafbd4e06e1f4d9dbe701090002ca6e",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/iodes-brownii.blend",
      "sha256": "85b7c6596cdd0c3c21ccd6ac25863569961c5686929243393a7753af46fdb55c",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/iodes-brownii.glb",
      "sha256": "f3604fbfab6eb74df9dfc6924994e642dc9722681a3329a91f21c0d42c997dff",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/maker-inspection.json",
      "sha256": "8e36acad460a83ce2cfcb1865ae6b4eae7f4102409e4217e8fe620daf79e3894",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/maker-review.md",
      "sha256": "7f7d803314355ddc694b95343666cb39263879add078d6b90fca2bfa9a67deee",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/metadata.json",
      "sha256": "66449e3ced5d9a08ea61f30e22a21b61dfcc36dd8fb9fa6a2039e034b16975bd",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/metrics.json",
      "sha256": "c30614b9da1df37b3bf95862682124f6217786656819463a93afc03dc6cf2da4",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/modeling-freeze.json",
      "sha256": "96747fe239d9dd4bb680f9cf5e5bc6074e3955e71e76f51e4649992866dc4a7d",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/preflight-contract.report.json",
      "sha256": "04f135ac85c59bfd0e5c00438c98242604d0ce47064520bc0f22a6ee467bd4b1",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/preview-hero.png",
      "sha256": "ddc4669f4133f8bbf2c3aa1a837da3a7670eb417302faa9681d9881f0dffb076",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/profile-approved-checker.report.json",
      "sha256": "3727054f983b8cee666062e2e2f53a6f394b612d78f6506d07cd17eada0bad11",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/profile-checker.report.json",
      "sha256": "3727054f983b8cee666062e2e2f53a6f394b612d78f6506d07cd17eada0bad11",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/profile-contract.json",
      "sha256": "8e556bbd74b463aa7f730cd941dd1451fb2f7fd9575530557805eaa374410e71",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/project-checker.report.json",
      "sha256": "d34540107d65bfb4836903cb7e8b02317620203703ba21f98fdfaf7c97866def",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/proof-renderer.py",
      "sha256": "fa98ab1d8f30003deb9a7379ee1a9222f4a361ebbf6a7d273f5596a662184baf",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/qa.json",
      "sha256": "62c3e58f023d5872e7dd282fc46ddca69dcde488ddb2fb175bdc3b58d4208ced",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/rebuild-1.report.json",
      "sha256": "ace7acb3f697ca60335b40397093d912c9827aaa99c4962ee2c1187644caecd3",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/rebuild-2.report.json",
      "sha256": "a26d56a79f497f6d791e651d48dc5183b7033def89d23ac673f7aaf9dbadc9be",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/reference-access.json",
      "sha256": "52807f84288aec565b7888c8bc483223d4bae7d4b5267fa5eac034e4a6d480e6",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/reference-profile-mapping.json",
      "sha256": "8a423685064355b073b0cf3890322d61700f80441d5d2e321f19cced5129ebd9",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/references-profile.json",
      "sha256": "e2e46329fc6a401eb2961d912e33de25a324e751deddb6bf4d923d545a5acb46",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/references.json",
      "sha256": "fc86e083897fdb133218dd2791651d96baac4c725d7e0d05dae0005338e578c2",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/repair-notes.md",
      "sha256": "8713a04171d6868a07d16d0e044f756e5ab38ba294b423896ac80b98778c039b",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/runtime/front.png",
      "sha256": "b7005ec530979eef3f3557338ba0d96d9475c247b2fce2f25027f5bd78221aea",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/runtime/hero.png",
      "sha256": "fcddebc1b1e0e719575dec996739d0b7b661c27dbd9c974f115a59e290e26e05",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/runtime/reversehero.png",
      "sha256": "c101041f950be5e57ba53cef9cc4f61fc9f44869a0b3114cc7218ed5c7b45e8b",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/runtime/runtime-report.json",
      "sha256": "c6abb1b6f025922ef43e393771ff23614795e404709386905c4b3ad5652a1d87",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/runtime/scene-9.png",
      "sha256": "2ca8e50e4a0cb6c2d7c63ce7657d82823a0d05424e6e04b78712402e6c9bff93",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/runtime/side.png",
      "sha256": "12e4bef2599d9b7b818e3fd0530c4f4b38dd3bbe8cf2dc1ca4bcbf71becde34b",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/runtime/top.png",
      "sha256": "a8cafaa691ce332a6f59d9ae9d3e05a4e267e4b449743a3e52db48ac8c4d44ce",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/source-export.report.json",
      "sha256": "4a18d6cce5a15a3ab6eddc7304ce0fff55f95e3b456f59e800e38149f58796ba",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/source-measurements.json",
      "sha256": "a8f68b2b0fbb4258cc6bf94704db5ac8e7903c57ec3a09f3f653b39467cc98d7",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/clay.png",
      "sha256": "1bb1999d79d5156ded47cca66d4f43333ca97d53f777c30b80b80c10b3b272d0",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/derivation.json",
      "sha256": "91b5d7ac1dcf803b1a070e196f62f8ce849b02c4aab563dac627ff67387a9f47",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/front.png",
      "sha256": "51c5c401d594dbdaf367eef1910f586c265193e83112ac1e8462bba187a049af",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/hero.png",
      "sha256": "ddc4669f4133f8bbf2c3aa1a837da3a7670eb417302faa9681d9881f0dffb076",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/rear.png",
      "sha256": "94199d4b5eb357754fda22a0f9fb8bd124e779d1a19c6831623fdc60779f4191",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/render-config.json",
      "sha256": "507be70f9b1d3413061f57a1da41a468d48ddf5bcaa90772e2448140845ef22e",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/render-manifest.json",
      "sha256": "ea48c26e839187f94a04a8e3fb19e7dbbb2886bf6b273ba764646f65dd2caea8",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/reversehero.png",
      "sha256": "3d3e2805cf7767f11d4de94134fedd912a02cbea8299fa75a2327778bec96832",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/side.png",
      "sha256": "41782e1af1c3d9420679290c3613257c9b09679f3defbfbe4fea3bb0bdd4b2e8",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/silhouette.png",
      "sha256": "e8bbe9109548093f2399fcfc4ef80349a1a1ca098fed7e0b1240c836e1bdb139",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views-static/top.png",
      "sha256": "2c9954512eb18725e20cf41c061e49b38fb3bfdba413e07e336b31fcb95e2b35",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/clay.png",
      "sha256": "1bb1999d79d5156ded47cca66d4f43333ca97d53f777c30b80b80c10b3b272d0",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/front.png",
      "sha256": "51c5c401d594dbdaf367eef1910f586c265193e83112ac1e8462bba187a049af",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/hero.png",
      "sha256": "ddc4669f4133f8bbf2c3aa1a837da3a7670eb417302faa9681d9881f0dffb076",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/rear.png",
      "sha256": "94199d4b5eb357754fda22a0f9fb8bd124e779d1a19c6831623fdc60779f4191",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/render-config.json",
      "sha256": "bcf8c797c3694e0ae1c34be92053d2d1853af2587560ec1798f5ba224110ee33",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/render-manifest.json",
      "sha256": "917c4c5ff48ace1cd4a8f7f2217a9e68485a0542d9125903b90b573cdeff8416",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/reversehero.png",
      "sha256": "3d3e2805cf7767f11d4de94134fedd912a02cbea8299fa75a2327778bec96832",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/side.png",
      "sha256": "41782e1af1c3d9420679290c3613257c9b09679f3defbfbe4fea3bb0bdd4b2e8",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/silhouette.png",
      "sha256": "e8bbe9109548093f2399fcfc4ef80349a1a1ca098fed7e0b1240c836e1bdb139",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/top.png",
      "sha256": "2c9954512eb18725e20cf41c061e49b38fb3bfdba413e07e336b31fcb95e2b35",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/views/turntable.json",
      "sha256": "4a962a028f3301fc78c9bac97564a0505ee467c74a934e2e62386a55782ca738",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/iodes-brownii/r001/warning-review.json",
      "sha256": "6b1dc32a6e2b95560ecf6d92ccac4fcdd1f7962913adafbc28210b35540f6683",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/HANDOFF.md",
      "sha256": "43a6c816550e8b556dde14b05aa7f5ebe564fbf4146e24067375eabeccc8753d",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/LICENSE.txt",
      "sha256": "e3d79dd430ea798cc905fac6d635fb214aaeefec982085fd9aa883291625f863",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/brief.json",
      "sha256": "1fac7cb2aecc9d4253607f20dc5eed6f9866c073828424f40c6d4954b8a81592",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/brief.md",
      "sha256": "3a2999989f84718b9d6987c2034476df418ab93cd76c736dea17c55d62b4d8b3",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/candidate.json",
      "sha256": "f44c35763d8c7b7142bbe3230897a927a996e977eb931802748e39bd2194ba05",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/checksums.sha256",
      "sha256": "db69809f275d3130cebf5d8a308f5dcef152123ac2b36c5993ce679cc793c28e",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/concept-checker.report.json",
      "sha256": "49fccae9c76a81d2ef376299cfc7beb0dfe9a03ebc21896343b53ef6db68ac30",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/concept-complete-checker.report.json",
      "sha256": "49fccae9c76a81d2ef376299cfc7beb0dfe9a03ebc21896343b53ef6db68ac30",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/concept-evidence.json",
      "sha256": "a5d9c0b47249ee718e52466109c33569622f7e163670785de6908eb963fa8e2a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/concept-inspection.json",
      "sha256": "dfd2444a50a768ad8172db3dcfc036d7ed2b4efb47969d1192f2de00a95ed7af",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/concepts/generation-record.json",
      "sha256": "58c84e9fa75b654a95f2a1ea7c7a665b2a80c8047b669dec0eae5a593c107cc6",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/concepts/original.png",
      "sha256": "2e675c167302a5b9c625f6c4cd43f4e5de022392c757e46f90a9fd17341de76e",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/concepts/prompt.txt",
      "sha256": "38a41d80fc2e632ff0b30bfbbc15f75893ab72c38c9960927118aaa0c8aa17f2",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/concepts/tool-result-metadata.json",
      "sha256": "701ceab8dc8abc243350e27e0a90dbf0ccb6ce09850baa10451be3e8f7b4fc9a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/config.json",
      "sha256": "6493b585ed5bc221bea77e667a504f0103af44bf13673f7be2e73aaba95bfcd3",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/contact-sheet.jpg",
      "sha256": "815e3263e674f45b4d8d051de05ecfd2ebb18c54da68fe687c849e3c3300f4ee",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/delivery-binding.json",
      "sha256": "89c6d1113047562bf8a5f68633598e190a3caf760aa193bab2bab5a61de3c586",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/delivery-brief.json",
      "sha256": "83d2a796cd7b7e704600e4302252e6e7415e5d4e706f69ac88e9e936baf8ec26",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/dependency-hashes.json",
      "sha256": "0059e7b38c1631f8282a81805cadc777ab8d9836c6ff03690c863cc4999dfbe2",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/generator.py",
      "sha256": "4e8b52198a421df76cd7f4b95553328f50808777b832068be68a43c605ba7368",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/gltf-validator.report.json",
      "sha256": "dbe35164d42e19d903b2c0f2d059a3a64611aef3a96d2686ee2f3a0a0dac68ca",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/maker-inspection.json",
      "sha256": "8ca291754a3ac6606104bfd7ffcfe0c3df7faad9ccf19f0b8f7be6738fa79b56",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/maker-review.md",
      "sha256": "f1da6dd12e900306d05e43a58a1f85993bd9c4d4603a60bb9d30aef7d74eaf65",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/metadata.json",
      "sha256": "481b3e82e69a7b62825ace8559cad5857dd7a83ac3cb5211d7705d7e1adb62bc",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/metrics.json",
      "sha256": "1cf4d790015dac3170840accbe44a455ed0cfd0431a69b830f60bdd8aee4d53e",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/modeling-freeze.json",
      "sha256": "d5aa6f5cfb729644671480349542b99649c0199495fa26255aec753ef58d69ad",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/preflight-contract.report.json",
      "sha256": "15a05f6a85c72f5ca8b4f27d535c9b7551d0a2785c1ac9fe188daf9d5e248a35",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/preview-hero.png",
      "sha256": "ca26d3b281ae59b35ef0a00989cd98e6031f83a45b0713e2ff0930d454aa2dc1",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/profile-approved-checker.report.json",
      "sha256": "aade771a89c79b5f63bc71a61ba10e88cfffbf8cadcd0b63e42b4f882ee14edd",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/profile-checker.report.json",
      "sha256": "aade771a89c79b5f63bc71a61ba10e88cfffbf8cadcd0b63e42b4f882ee14edd",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/profile-contract.json",
      "sha256": "99f1b1e22f72acace0607e1024c600df0e219c428d3ff2976e87cd43e31bb640",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/project-checker.report.json",
      "sha256": "aecbd725f3172324de10490b8089da9be2459d00df55af5d79a4420659856149",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/proof-renderer.py",
      "sha256": "fa98ab1d8f30003deb9a7379ee1a9222f4a361ebbf6a7d273f5596a662184baf",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/qa.json",
      "sha256": "ed2d0e7a1a7df651def3cdc91f266b9c4b248313ab0d93a366d02f76a15ad7e9",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/rebuild-1.report.json",
      "sha256": "dbf77f96c7322317d1891a731fbc47350918b14a2a469e96467b8ec2f0f3a32a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/rebuild-2.report.json",
      "sha256": "9ff91f500a1ae17634c86efd9acd8e21fe1591a248a87be89d9d289f04d96b63",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/reference-access.json",
      "sha256": "0e972b5c875132f2156f49de1d53033f2047843f7fc21204d0daf088fdb6f4e2",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/reference-profile-mapping.json",
      "sha256": "a208cd1b65ccdb5eec0f97b8ccfbba8e60cc5b04fd6ec0474f1167ff63bff4dc",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/references-profile.json",
      "sha256": "a00a50d829635fce808dd1c38d77ddbde70980603744419b0ec2304ffc89c68f",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/references.json",
      "sha256": "4980ddffe5755f5b1d51eeebdffd505909b2b7e1e4d221f26628abea70dfe203",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/repair-notes.md",
      "sha256": "0d9a0c9664e8da6b00f4b8d179c1fb99c52f10a1c2c5129f844bcf96d321ad7a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/runtime/front.png",
      "sha256": "7b7414e7526f99b7799660182934072220f61b1ca13dccb17096d858e8ff43a7",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/runtime/hero.png",
      "sha256": "c9c14f8439d064cacdde20a3c6653cbaee9bdb9e744085cce69271407407f9b6",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/runtime/reversehero.png",
      "sha256": "9658980422375550d7d253dc8f12f9eef06aa1f4800711b2ff48e9b70b2f5189",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/runtime/runtime-report.json",
      "sha256": "975cc059daf29562ac9f143197d6c1c1f11f68b9c44cec9a01984175c339d788",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/runtime/scene-9.png",
      "sha256": "1dbc64925743c5664fe681da92571afc23b450020c00b78d76d11c12d22d5d5a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/runtime/side.png",
      "sha256": "4429dc2ae2491542aa57f10584ad4c91f981a2594b615f327a97ec9218a7eb1e",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/runtime/top.png",
      "sha256": "403740367d951ba850878eaafaa04b8373f1550ac881ba44ec67386c26cafcd5",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/source-export.report.json",
      "sha256": "7f8d72000af7863bdf3f0bebb833cfe04ffba9afc65caa2ae8438a7d492c8590",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/source-measurements.json",
      "sha256": "88a7ab40e1b4f3759b085cb09aa3d43df6fc561a25c5e57a5c91a408987645e7",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/clay.png",
      "sha256": "3e11eebeb5bb62b4bbfdc694ce3813141bb0c511564a010dc97cb48d4b1c5f3c",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/derivation.json",
      "sha256": "7c917829c82108286550aecef58c640b888cbed71f255bb5347a217dcbf85ca7",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/front.png",
      "sha256": "56432117f834bbe3faf42df07699d7bef75b2b0b8571b8b7a2c3b55689f7b2f5",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/hero.png",
      "sha256": "ca26d3b281ae59b35ef0a00989cd98e6031f83a45b0713e2ff0930d454aa2dc1",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/rear.png",
      "sha256": "789e83094df018a1fede14a73bbcee2e94cb9adcc5850d0d0b119d48eeb84b45",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/render-config.json",
      "sha256": "6654e6972746c5a0a316496ca2ed944c07b759e45a8a9da1c0384601115865a4",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/render-manifest.json",
      "sha256": "ea66f45b4c7477735e3e99465f24d8f3129f778daf3a8fc37d87a9272beb76fa",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/reversehero.png",
      "sha256": "57ae104df180d1818cb2208a64ea99ac6adc25d9d7e500949f1914cb215828e9",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/side.png",
      "sha256": "660791bd3c3179754e8801b6b2961e2f7909c66ed7b690b34977fd8604cc2aca",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/silhouette.png",
      "sha256": "48c02005e91fee2e2250ccf81f0adafec4acb23243663fe3ebdc809123bcaa35",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views-static/top.png",
      "sha256": "21577095aa86d404215194ea881ba8461ae72ffde605b68f45baf27ef8ac5f5a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/clay.png",
      "sha256": "3e11eebeb5bb62b4bbfdc694ce3813141bb0c511564a010dc97cb48d4b1c5f3c",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/front.png",
      "sha256": "56432117f834bbe3faf42df07699d7bef75b2b0b8571b8b7a2c3b55689f7b2f5",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/hero.png",
      "sha256": "ca26d3b281ae59b35ef0a00989cd98e6031f83a45b0713e2ff0930d454aa2dc1",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/rear.png",
      "sha256": "789e83094df018a1fede14a73bbcee2e94cb9adcc5850d0d0b119d48eeb84b45",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/render-config.json",
      "sha256": "efc3915cae74a480d36e671aa812588e91d442694f8545f9e7e379b18543a0a3",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/render-manifest.json",
      "sha256": "cc0f38122b60ea9a25419dc7dcd57a2b90411cb5d6d3f27c119dbb0134665a62",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/reversehero.png",
      "sha256": "57ae104df180d1818cb2208a64ea99ac6adc25d9d7e500949f1914cb215828e9",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/side.png",
      "sha256": "660791bd3c3179754e8801b6b2961e2f7909c66ed7b690b34977fd8604cc2aca",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/silhouette.png",
      "sha256": "48c02005e91fee2e2250ccf81f0adafec4acb23243663fe3ebdc809123bcaa35",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/top.png",
      "sha256": "21577095aa86d404215194ea881ba8461ae72ffde605b68f45baf27ef8ac5f5a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/views/turntable.json",
      "sha256": "71318dd1276410f57a3ff6e848166b1eaab4f06a16586c9d71da8301eb6b5000",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/warning-review.json",
      "sha256": "6b1dc32a6e2b95560ecf6d92ccac4fcdd1f7962913adafbc28210b35540f6683",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/welded-ignimbrite-outcrop.blend",
      "sha256": "1e1cdcb3bfd64ed630455fb6b6bcda8f66b83704823a17fb7a0914a0bb3f5357",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "assets/candidates/continuous-small-life-round18-20261020/batch-53/welded-ignimbrite-outcrop/r001/welded-ignimbrite-outcrop.glb",
      "sha256": "83b7d4170c8cb51870e2ea643294306e4cc6a62a2386712457cfb887ff0c2704",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/HANDOFF.json",
      "sha256": "022ccc702db84d01e2f1005cfecad760310ff5931c299f834d57a565c6cbea48",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/HANDOFF.md",
      "sha256": "3a54378ea26734cf5dc76d7b9c8d5ea672636c0078a40a91f86983af7406a5a4",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/bind-delivery-v001-file-byte-assumption.py",
      "sha256": "21257345cb1355fd5dc7527c4b6bda21a3555f350558ed8bc33edb58410c6480",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/bind-delivery.py",
      "sha256": "c73ad791578298e846dc425bcb3e14a89dc39bd2e4864e4f462e59b2e01f0330",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/build-handoff.py",
      "sha256": "0311180520708c5cffdd86b0157dc3e0634ea909be614b6adf042cfd87fb8930",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/check-batch.py",
      "sha256": "bb07a4dd2f839f3024665e690fa1c707535dfa1e546c0a19f7d9e0d672e06935",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/checksums.sha256",
      "sha256": "6f964925c53b8db763d68cb2daed82771980877630797e27dbdb12a4a1475249",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/claim.json",
      "sha256": "0d40a63fed68ee1f13d2d34bdae13887845c50155153fb5ce6dad8625b2117ce",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/dispatch-record.json",
      "sha256": "1877c3fefa6478aa138ce3ae27b4ecb2c0b673907111efca6dba8dfc08ee4945",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/finish.py",
      "sha256": "2e971a6235db2ea6f8ba68d0235f45307f9e1d88cfe1519e803d9e09e24376ad",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/build-jobs.json",
      "sha256": "9bd3fc8588f2ed19bc6937f65629aa8a52a4bdee2ff7ba2148339164c614e031",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/delivery-render.log",
      "sha256": "8de6553b7d3a54d924107ab85edc868073fda9ea2b75e09a69e528370f06813d",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/execution.jsonl",
      "sha256": "1dd4087d792401418b8c728a62b05d6fb580eddd2cb97c528d4109f7361f239d",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/execution.jsonl",
      "sha256": "9a9867f09b7bb908c1df552e9941c29c10d55001a27050f831cb6260029184a0",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/generator.py",
      "sha256": "a6de8c2902a0b1d341cccacdee108e6f400027e222edab9ef96bb559f30d6580",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/measure-source.log",
      "sha256": "c20a80a279910fa82065a0f884b5ee5f8c89ee83386caa03172c3f4d148ef297",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/queue.log",
      "sha256": "a4190cf2ef8dd740e10f31a21046201eb640f08201e81548e7b42e0d490b67b0",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/initial/c2429def88f4165502f61f91e5aa92b37bacd3bcf2366bd4b3a770a72f48c009/20261020T002518-88ecdc2728934bdab87aec048ddaf477/outputs/halopoa-furrowed-burrow/qa.json",
      "sha256": "299731e6f76cc195c8ee394e6a1b7442d65ce587fc01273212d660d5013cb88a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/initial/c2429def88f4165502f61f91e5aa92b37bacd3bcf2366bd4b3a770a72f48c009/20261020T002518-88ecdc2728934bdab87aec048ddaf477/request.json",
      "sha256": "93f27b1266d17eb4580afde242f4c00e8706d7e8bc5fdd4920fb3b095e3f0650",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/initial/c2429def88f4165502f61f91e5aa92b37bacd3bcf2366bd4b3a770a72f48c009/20261020T002518-88ecdc2728934bdab87aec048ddaf477/result.json",
      "sha256": "f53f96a93e1023fc8b9274110e68f19dbe759ad8f950cd998534cce56339603d",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/initial/c2429def88f4165502f61f91e5aa92b37bacd3bcf2366bd4b3a770a72f48c009/20261020T002518-88ecdc2728934bdab87aec048ddaf477/stderr.log",
      "sha256": "3c24c51f79480654b5bf2a34b1841c42865044391ba9c49075d0222e0c712171",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/initial/c2429def88f4165502f61f91e5aa92b37bacd3bcf2366bd4b3a770a72f48c009/20261020T002518-88ecdc2728934bdab87aec048ddaf477/stdout.log",
      "sha256": "90b9f23d612e25562b057cb9a15b4c7e5304ebbd85d3aae0f5cabe1bfc51ebaa",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/21158468e648f6e55e3782a833b7a65ad01b85b03be1a2392297dc3463029a9b/20261020T002519-08a73aa1312d472196c0b4f619d5e2f6/outputs/halopoa-furrowed-burrow/qa.json",
      "sha256": "299731e6f76cc195c8ee394e6a1b7442d65ce587fc01273212d660d5013cb88a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/21158468e648f6e55e3782a833b7a65ad01b85b03be1a2392297dc3463029a9b/20261020T002519-08a73aa1312d472196c0b4f619d5e2f6/request.json",
      "sha256": "1e335eca36ee78203791a3e658fe4be9fce4260ccbdcb45048ed8837ee9bdb34",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/21158468e648f6e55e3782a833b7a65ad01b85b03be1a2392297dc3463029a9b/20261020T002519-08a73aa1312d472196c0b4f619d5e2f6/result.json",
      "sha256": "c980d751107549de752fa1d66cdd6da8c68eabecafdd16b8e7f4eac043756825",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/21158468e648f6e55e3782a833b7a65ad01b85b03be1a2392297dc3463029a9b/20261020T002519-08a73aa1312d472196c0b4f619d5e2f6/stderr.log",
      "sha256": "3c24c51f79480654b5bf2a34b1841c42865044391ba9c49075d0222e0c712171",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/21158468e648f6e55e3782a833b7a65ad01b85b03be1a2392297dc3463029a9b/20261020T002519-08a73aa1312d472196c0b4f619d5e2f6/stdout.log",
      "sha256": "90b9f23d612e25562b057cb9a15b4c7e5304ebbd85d3aae0f5cabe1bfc51ebaa",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/b88125a5f02427f59f5f92a23e05e53c245a9f68b222068e8b35d8f51122a2f2/20261020T002521-9da8fdb51e5644db8132999ec3c90af7/outputs/halopoa-furrowed-burrow/qa.json",
      "sha256": "299731e6f76cc195c8ee394e6a1b7442d65ce587fc01273212d660d5013cb88a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/b88125a5f02427f59f5f92a23e05e53c245a9f68b222068e8b35d8f51122a2f2/20261020T002521-9da8fdb51e5644db8132999ec3c90af7/request.json",
      "sha256": "a580225eb94bc830eaf2e72bed15f34dd4c92129bcb7ed85deff68998ebfa9c1",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/b88125a5f02427f59f5f92a23e05e53c245a9f68b222068e8b35d8f51122a2f2/20261020T002521-9da8fdb51e5644db8132999ec3c90af7/result.json",
      "sha256": "e2c9de2fcafd044e595d04b806eb3221caf90706bf4213665aa4992f73515ddb",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/b88125a5f02427f59f5f92a23e05e53c245a9f68b222068e8b35d8f51122a2f2/20261020T002521-9da8fdb51e5644db8132999ec3c90af7/stderr.log",
      "sha256": "3c24c51f79480654b5bf2a34b1841c42865044391ba9c49075d0222e0c712171",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/b88125a5f02427f59f5f92a23e05e53c245a9f68b222068e8b35d8f51122a2f2/20261020T002521-9da8fdb51e5644db8132999ec3c90af7/stdout.log",
      "sha256": "90b9f23d612e25562b057cb9a15b4c7e5304ebbd85d3aae0f5cabe1bfc51ebaa",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/runs/20261020T002518-95999996d747475a9cde022612f01b1a/manifest.json",
      "sha256": "f0782b9176da65497fbdd9dff032760c3f65ad93de242051f11d880e74533030",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runs/runs/20261020T002518-95999996d747475a9cde022612f01b1a/summary.json",
      "sha256": "f4e2e528d6f174c8beeae4b748b63467be19222f36f99b0140e7a6d24af17dda",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/failed-attempt-02-concave-end-caps/runtime.log",
      "sha256": "d5d3a52f690c9b8f5b1299cb72ed972fdc10ffd6b2b51861187a96ba31b2dd84",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/khronos.log",
      "sha256": "50b114a7ff9a8a6123cfefec88bea1c208921fd458c6fdea480de9e6cc23ce7a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/measure-source-final.log",
      "sha256": "f3d1c23af544a3de0cffabe5def3d9a92bf5e33e3a3018347f8b19342f0bf7d2",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/execution.jsonl",
      "sha256": "5fbaa098cb7010a91fc223985325cfe4ae2418318c4becf8f025ca87eb3ccb9a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/generator.py",
      "sha256": "79927f538c01ac6f8028de0dc3e2c68cc842c0131d283df05ca5a2f04ddec130",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/gltf-validator.report.json",
      "sha256": "b691c248a58d432aff76ed897ffb82012a4eb3e408bf193ae1340818815269cb",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/halopoa-furrowed-burrow.blend",
      "sha256": "d78307292c8aed8076a57ec6de57bb5ea07d8981c8d5fddd7bb6006fb52a4137",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/halopoa-furrowed-burrow.glb",
      "sha256": "0defc7e2f12f4d6fa0bd2678a6f900d38c3182acb735947157c024a9b1ef280e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/metadata.json",
      "sha256": "a1602f18f5021953dbc77e2d5450d787b916e0e60a8e26e4f5f10d3f22e9f715",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/preview-hero.png",
      "sha256": "4d393b8c0c80b85c1c26ec7ae745200f5974741bf14eaaad03621cc2c3a25723",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/qa.json",
      "sha256": "000eceb8f50a6b45c0426d48e5be7cb50ff7b0e3e2d30e0773ec082428d2f114",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/rebuild-1.report.json",
      "sha256": "ff6456544d0bd837d6534bae9383dfd7defd59736fa15ce0e227a285c5b4cff1",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/rebuild-2.report.json",
      "sha256": "0790781cb396be9e9d2dace2ad942aaf0cd0ccc6f47e7f8a8592bd46ee7c48d0",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/initial/37a4f49ee88d4938d4d1d6f78ad0f4e04744bed78d22f26ce2dad8ec72e8dd03/20261020T002352-54adaae422374406935ad51100e46fbd/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.blend",
      "sha256": "d78307292c8aed8076a57ec6de57bb5ea07d8981c8d5fddd7bb6006fb52a4137",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/initial/37a4f49ee88d4938d4d1d6f78ad0f4e04744bed78d22f26ce2dad8ec72e8dd03/20261020T002352-54adaae422374406935ad51100e46fbd/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.glb",
      "sha256": "0defc7e2f12f4d6fa0bd2678a6f900d38c3182acb735947157c024a9b1ef280e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/initial/37a4f49ee88d4938d4d1d6f78ad0f4e04744bed78d22f26ce2dad8ec72e8dd03/20261020T002352-54adaae422374406935ad51100e46fbd/outputs/halopoa-furrowed-burrow/metadata.json",
      "sha256": "a1602f18f5021953dbc77e2d5450d787b916e0e60a8e26e4f5f10d3f22e9f715",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/initial/37a4f49ee88d4938d4d1d6f78ad0f4e04744bed78d22f26ce2dad8ec72e8dd03/20261020T002352-54adaae422374406935ad51100e46fbd/outputs/halopoa-furrowed-burrow/qa.json",
      "sha256": "ae5b7e98071d4bac0478721094539327608d6688bea5af792d4da449495c9159",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/initial/37a4f49ee88d4938d4d1d6f78ad0f4e04744bed78d22f26ce2dad8ec72e8dd03/20261020T002352-54adaae422374406935ad51100e46fbd/request.json",
      "sha256": "a3b586c1e543d129bcf3a6273f5cdd3c9a4944b21beb868942468888769ed1f1",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/initial/37a4f49ee88d4938d4d1d6f78ad0f4e04744bed78d22f26ce2dad8ec72e8dd03/20261020T002352-54adaae422374406935ad51100e46fbd/result.json",
      "sha256": "8e7be52f654de93cfd6fa3e3a0057e4ead6ead01a4da24eed3e84ff02b605ae2",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/initial/37a4f49ee88d4938d4d1d6f78ad0f4e04744bed78d22f26ce2dad8ec72e8dd03/20261020T002352-54adaae422374406935ad51100e46fbd/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/initial/37a4f49ee88d4938d4d1d6f78ad0f4e04744bed78d22f26ce2dad8ec72e8dd03/20261020T002352-54adaae422374406935ad51100e46fbd/stdout.log",
      "sha256": "ca826efb60db47d3cf09eeaea1fc3378ec75d9a508f54c3cba38c9b668479d42",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/bba505036106b76ff0790d417479e67d5b67d7dc31f5d1ff48c4336c9cf9e3f7/20261020T002354-2b0d4b31a7f54195bb1ba7a474eaaea8/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.blend",
      "sha256": "ffe289597a4c388db3ea0ffafb462f412f538f57cb04f082f90c84289cfca222",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/bba505036106b76ff0790d417479e67d5b67d7dc31f5d1ff48c4336c9cf9e3f7/20261020T002354-2b0d4b31a7f54195bb1ba7a474eaaea8/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.glb",
      "sha256": "0defc7e2f12f4d6fa0bd2678a6f900d38c3182acb735947157c024a9b1ef280e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/bba505036106b76ff0790d417479e67d5b67d7dc31f5d1ff48c4336c9cf9e3f7/20261020T002354-2b0d4b31a7f54195bb1ba7a474eaaea8/outputs/halopoa-furrowed-burrow/metadata.json",
      "sha256": "b5c5c43408c33319f17d4df9962ffd35c53d82c8290e72bef07e0d5fdc9eb45d",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/bba505036106b76ff0790d417479e67d5b67d7dc31f5d1ff48c4336c9cf9e3f7/20261020T002354-2b0d4b31a7f54195bb1ba7a474eaaea8/outputs/halopoa-furrowed-burrow/qa.json",
      "sha256": "4a0a34386f027e8e3cc8c292d6b4e88896d81d2be16280dea6356df8eee690a5",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/bba505036106b76ff0790d417479e67d5b67d7dc31f5d1ff48c4336c9cf9e3f7/20261020T002354-2b0d4b31a7f54195bb1ba7a474eaaea8/request.json",
      "sha256": "7fb04e0e63beeb062ef8f71e1d2991741ca747fc874324efdeeef0e7cb1ccfe0",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/bba505036106b76ff0790d417479e67d5b67d7dc31f5d1ff48c4336c9cf9e3f7/20261020T002354-2b0d4b31a7f54195bb1ba7a474eaaea8/result.json",
      "sha256": "172c6dc2560ecd05960ead26be5be4b900eec1e9a205f2030bc574f3593be55b",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/bba505036106b76ff0790d417479e67d5b67d7dc31f5d1ff48c4336c9cf9e3f7/20261020T002354-2b0d4b31a7f54195bb1ba7a474eaaea8/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/bba505036106b76ff0790d417479e67d5b67d7dc31f5d1ff48c4336c9cf9e3f7/20261020T002354-2b0d4b31a7f54195bb1ba7a474eaaea8/stdout.log",
      "sha256": "eebbb907fb145036ba0e841e017b695b76c7f8b4e893be69f81a0dd5940b5d1d",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/32ca708d4e389c4d5616d1d5afa937f3c66ba7d3ff683bc884cf47ed21282fc4/20261020T002356-7864feaac7b94651960de1425f762e06/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.blend",
      "sha256": "0b589e3f7aa928a007242389b433c2c339dde29a5370e5c89079110a3be5c00a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/32ca708d4e389c4d5616d1d5afa937f3c66ba7d3ff683bc884cf47ed21282fc4/20261020T002356-7864feaac7b94651960de1425f762e06/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.glb",
      "sha256": "0defc7e2f12f4d6fa0bd2678a6f900d38c3182acb735947157c024a9b1ef280e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/32ca708d4e389c4d5616d1d5afa937f3c66ba7d3ff683bc884cf47ed21282fc4/20261020T002356-7864feaac7b94651960de1425f762e06/outputs/halopoa-furrowed-burrow/metadata.json",
      "sha256": "8b8baa1e11bc685ddddd047fdab18f09f4af38dbf4e0d60dec6da0130cedd3e5",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/32ca708d4e389c4d5616d1d5afa937f3c66ba7d3ff683bc884cf47ed21282fc4/20261020T002356-7864feaac7b94651960de1425f762e06/outputs/halopoa-furrowed-burrow/qa.json",
      "sha256": "8eab8124edf8b3c244ca28bf418d00608a60379bf07ecbe0c24bad71c21a0b55",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/32ca708d4e389c4d5616d1d5afa937f3c66ba7d3ff683bc884cf47ed21282fc4/20261020T002356-7864feaac7b94651960de1425f762e06/request.json",
      "sha256": "0113e78015350b8dbe31ecd15a728f3b38c7d4ec665c5b6e18671622da0c9c6a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/32ca708d4e389c4d5616d1d5afa937f3c66ba7d3ff683bc884cf47ed21282fc4/20261020T002356-7864feaac7b94651960de1425f762e06/result.json",
      "sha256": "b21eaee9c302b79897e224aa6b59ad0ce382ed374752e9f3fa70663bb9cb7909",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/32ca708d4e389c4d5616d1d5afa937f3c66ba7d3ff683bc884cf47ed21282fc4/20261020T002356-7864feaac7b94651960de1425f762e06/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/32ca708d4e389c4d5616d1d5afa937f3c66ba7d3ff683bc884cf47ed21282fc4/20261020T002356-7864feaac7b94651960de1425f762e06/stdout.log",
      "sha256": "fb130d43dc771dba88c1913fb72d5e4a2a641c73df8adbd3888a46db44503723",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/runs/20261020T002352-3c896803b1524b9fa7eecb2aa6bc36f9/manifest.json",
      "sha256": "f0782b9176da65497fbdd9dff032760c3f65ad93de242051f11d880e74533030",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runs/runs/20261020T002352-3c896803b1524b9fa7eecb2aa6bc36f9/summary.json",
      "sha256": "cce7b089fa04a90d3255c350e9ec9e65b71d10727257e74fea9ad2c69206b947",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runtime/front.png",
      "sha256": "2a1c3485550d0c63e5d4a7b7f38d8ae4a63dab72a31b71ecad62c10eb490e331",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runtime/hero.png",
      "sha256": "174960936f88b298193a31a169ae7d456920820f336b9b7b2027a04045f85482",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runtime/reversehero.png",
      "sha256": "d712e04a62c124dbd5ef461742da5db2d6f5542060f0044f20cbe9386e716f49",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runtime/runtime-report.json",
      "sha256": "53a7da83158f85a6b1cf798fe73c23fe656cce6d7ad63241b8700210ed7c94ae",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runtime/scene-9.png",
      "sha256": "55ced4e113f5eb64af76b951013e4cd378188f175a88058d5f3bfd8c944ee5a5",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runtime/side.png",
      "sha256": "df6b4b099508d85f4c7255db7b4d5ecfd87087daa664112d61cd76ac10604f40",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/runtime/top.png",
      "sha256": "182f7dd4942851f6b108deec7c47bcbeaf544ca45003621e0c656f4b3288b06d",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/source-export.report.json",
      "sha256": "aae4c68a8ff5aacc454444256f704bd9670df57117c99b63d0bc1a25583192bb",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/source-measurements.json",
      "sha256": "c705444bb2932385f4ebc59a15e9f52f52b6765c1b7d7db3eb36223e55c1ea6d",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/clay.png",
      "sha256": "2d05fe8b788f6584444da2e095d3ca6cf97a17d6489d2b3e62cbd6ebbf44abf9",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/claytop.png",
      "sha256": "059ce937398655bd88829bf3adcc972522ead5ec4146fd136cf104402175659e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/front.png",
      "sha256": "845ee18ebbd1be064ead7a740c41f74a0f60c2e1301aa01b6e7b170df1bb8f91",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/hero.png",
      "sha256": "4d393b8c0c80b85c1c26ec7ae745200f5974741bf14eaaad03621cc2c3a25723",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/rear.png",
      "sha256": "a1e843d39717e02c950b3502c45c26db450183feb817a596628f06b82011a73e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/render-config.json",
      "sha256": "00086bcc306549589b147be9248319f127fcb03277ca8dc0adeed32ee34e1c91",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/render-manifest.json",
      "sha256": "c2e2551361f427ebee17a43f0a4dac7242e178a2780ebdd354366e84311d3fd1",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/reversehero.png",
      "sha256": "c872cbda021170f88b26c4f2f556e802bfbfebfa451c2c919c2b16b2ec8025fc",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/side.png",
      "sha256": "948bd62f0a30680b3f708e46bb90e15848a711f68b1ebb92f5e22e1a43ff7e30",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/silhouette.png",
      "sha256": "2115f6cb6b3d6cf3b69b64ed6b0d32e6780beef489fb81736643e7d12546884f",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/top.png",
      "sha256": "60b594c93edcc70ecf6c6a331adbd384cc79d786f04cd755be88fbc51e44bab4",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/prototype-01-too-few-visible-furrows/views/turntable.json",
      "sha256": "591c0d0931c818e59da13f11b8924395d7572b8feaaf7ba1cb1b63b4e873f0f8",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/queue.log",
      "sha256": "840d570bd81f92209439547f5733bd93638b8474647523e832877fb1ed735a2c",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/rebuild-1.log",
      "sha256": "4892070d9ba80f38f2a9090005f710316ecd0729b28fb021311d8d2dacd860f2",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/rebuild-2.log",
      "sha256": "3c100fc66967c91879d6e0ada0b090dc1c9a45730e5bce2050a84305a6fbf173",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/render.log",
      "sha256": "b57a9ef39ddd1b9a156d701cf41ac67bd2033cb76e13f9562f760b31aa1a36a7",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/initial/7225feb80783b4346e3b2a2b28f3221117aa054c3d1c13a313004bd7f4596ee2/20261020T002625-3d95c43b07c9460fbd58cb9d305c9cc6/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.blend",
      "sha256": "6c538d87b579f9a32fe28d2a21c19f6937927108773f0c1774bb63ebd7699714",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/initial/7225feb80783b4346e3b2a2b28f3221117aa054c3d1c13a313004bd7f4596ee2/20261020T002625-3d95c43b07c9460fbd58cb9d305c9cc6/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.glb",
      "sha256": "42e7fd3105d689c27d3bdf7de6ea0fbfc95094d0645e840b1b66062ca8fd54f6",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/initial/7225feb80783b4346e3b2a2b28f3221117aa054c3d1c13a313004bd7f4596ee2/20261020T002625-3d95c43b07c9460fbd58cb9d305c9cc6/outputs/halopoa-furrowed-burrow/metadata.json",
      "sha256": "fbb650d598be498ddb98f3296e4e635c951186b799b3bf81db04b5d50c827f0f",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/initial/7225feb80783b4346e3b2a2b28f3221117aa054c3d1c13a313004bd7f4596ee2/20261020T002625-3d95c43b07c9460fbd58cb9d305c9cc6/outputs/halopoa-furrowed-burrow/qa.json",
      "sha256": "b69a37b2c17a7f49cf50029c72894f69868f74bdc9fc1244e0139c7abb93f9e7",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/initial/7225feb80783b4346e3b2a2b28f3221117aa054c3d1c13a313004bd7f4596ee2/20261020T002625-3d95c43b07c9460fbd58cb9d305c9cc6/request.json",
      "sha256": "a59988e78e92ba071b5a933ae8de3c48fe6cb265c9d3f478c25d0ded09c12056",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/initial/7225feb80783b4346e3b2a2b28f3221117aa054c3d1c13a313004bd7f4596ee2/20261020T002625-3d95c43b07c9460fbd58cb9d305c9cc6/result.json",
      "sha256": "8156ffa4f576b8ffd17978c00b8dfffef6655537c7b72fdf88984825ce8a5f06",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/initial/7225feb80783b4346e3b2a2b28f3221117aa054c3d1c13a313004bd7f4596ee2/20261020T002625-3d95c43b07c9460fbd58cb9d305c9cc6/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/initial/7225feb80783b4346e3b2a2b28f3221117aa054c3d1c13a313004bd7f4596ee2/20261020T002625-3d95c43b07c9460fbd58cb9d305c9cc6/stdout.log",
      "sha256": "0cf84d803b3251aa8580085854d293b5acfb9639ab86d023953068ada0bd7a0f",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/f0d0d07371079bba86f2e2724a48d000047faadd67c6d980b0938a91b6c747c1/20261020T002627-2aa00c05e993440583737b4c792d6ea3/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.blend",
      "sha256": "0a9a8d6605644d8fecfc52df7f7e5a773dbabf73459adfb2fc1979775dd19a00",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/f0d0d07371079bba86f2e2724a48d000047faadd67c6d980b0938a91b6c747c1/20261020T002627-2aa00c05e993440583737b4c792d6ea3/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.glb",
      "sha256": "42e7fd3105d689c27d3bdf7de6ea0fbfc95094d0645e840b1b66062ca8fd54f6",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/f0d0d07371079bba86f2e2724a48d000047faadd67c6d980b0938a91b6c747c1/20261020T002627-2aa00c05e993440583737b4c792d6ea3/outputs/halopoa-furrowed-burrow/metadata.json",
      "sha256": "648278243727a75364c74d7367ba77fdfe6cc75d6098487e8c878707af9ad985",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/f0d0d07371079bba86f2e2724a48d000047faadd67c6d980b0938a91b6c747c1/20261020T002627-2aa00c05e993440583737b4c792d6ea3/outputs/halopoa-furrowed-burrow/qa.json",
      "sha256": "25e49f682b0afd10566496b642533408a2bc2e9568692fe43b86f82333d46a5e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/f0d0d07371079bba86f2e2724a48d000047faadd67c6d980b0938a91b6c747c1/20261020T002627-2aa00c05e993440583737b4c792d6ea3/request.json",
      "sha256": "5bd23914c68f14d44c647ca34b91d8cd4ecd74f9101abe70b5ca69ee5de96d98",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/f0d0d07371079bba86f2e2724a48d000047faadd67c6d980b0938a91b6c747c1/20261020T002627-2aa00c05e993440583737b4c792d6ea3/result.json",
      "sha256": "93395e1d91bf066532e1c22da6d6603f3e354e863eb4f81021326df89b710465",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/f0d0d07371079bba86f2e2724a48d000047faadd67c6d980b0938a91b6c747c1/20261020T002627-2aa00c05e993440583737b4c792d6ea3/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-1/f0d0d07371079bba86f2e2724a48d000047faadd67c6d980b0938a91b6c747c1/20261020T002627-2aa00c05e993440583737b4c792d6ea3/stdout.log",
      "sha256": "f00a23fd73beaa7a707ace95f203838a7787734674f189d8b48fb85ea6358ad5",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/4706fe8cfe32c521ee3b8d40a800b87da9b6ba663a236d400241e38953f1bcad/20261020T002629-45da6a2af5924cf99c3bacc3fe6d9bf0/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.blend",
      "sha256": "30326abf6fec382f6674648ebe80a05e7b2debc442968b69aeb10d2bd021a06f",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/4706fe8cfe32c521ee3b8d40a800b87da9b6ba663a236d400241e38953f1bcad/20261020T002629-45da6a2af5924cf99c3bacc3fe6d9bf0/outputs/halopoa-furrowed-burrow/halopoa-furrowed-burrow.glb",
      "sha256": "42e7fd3105d689c27d3bdf7de6ea0fbfc95094d0645e840b1b66062ca8fd54f6",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/4706fe8cfe32c521ee3b8d40a800b87da9b6ba663a236d400241e38953f1bcad/20261020T002629-45da6a2af5924cf99c3bacc3fe6d9bf0/outputs/halopoa-furrowed-burrow/metadata.json",
      "sha256": "bc717fc507519e7a9bd3014b4c2b334c6ab74a853785842bd2307820b9f081fa",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/4706fe8cfe32c521ee3b8d40a800b87da9b6ba663a236d400241e38953f1bcad/20261020T002629-45da6a2af5924cf99c3bacc3fe6d9bf0/outputs/halopoa-furrowed-burrow/qa.json",
      "sha256": "d94af6d259e376d650fe564c51d81ca90cfe4c63101a8fb519f3c0657a3bf70e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/4706fe8cfe32c521ee3b8d40a800b87da9b6ba663a236d400241e38953f1bcad/20261020T002629-45da6a2af5924cf99c3bacc3fe6d9bf0/request.json",
      "sha256": "2b7d211f628014c6cf19c80bb76885dc411805c7cc4067ff7bdd2a0c231f64bf",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/4706fe8cfe32c521ee3b8d40a800b87da9b6ba663a236d400241e38953f1bcad/20261020T002629-45da6a2af5924cf99c3bacc3fe6d9bf0/result.json",
      "sha256": "0076dd4e3f759924f03ffe27d96ad266f81ad40ad4bea6c3df6aae7abf68b7c1",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/4706fe8cfe32c521ee3b8d40a800b87da9b6ba663a236d400241e38953f1bcad/20261020T002629-45da6a2af5924cf99c3bacc3fe6d9bf0/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/build/halopoa-furrowed-burrow/r001/rebuild-2/4706fe8cfe32c521ee3b8d40a800b87da9b6ba663a236d400241e38953f1bcad/20261020T002629-45da6a2af5924cf99c3bacc3fe6d9bf0/stdout.log",
      "sha256": "df8ef501aa678e84d416722f946498cee2f8205f8d84f3a3b0bbaa9ae268c5f8",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/runs/20261020T002625-0496cf9a640e4f80bd4afeb0673e7cb0/manifest.json",
      "sha256": "f0782b9176da65497fbdd9dff032760c3f65ad93de242051f11d880e74533030",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runs/runs/20261020T002625-0496cf9a640e4f80bd4afeb0673e7cb0/summary.json",
      "sha256": "6956878c0925edaa3d5280ac625a061aa7a60e9309d2c3449831aab2fda93a0e",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/runtime-final.log",
      "sha256": "1fbb3ed7bf2bfd40eff5361cecc71377f501f5d94997dc7b8cd8274bf1868ab4",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/source-reopen.log",
      "sha256": "bb67cef33535aae782ab3cb2868d672e193e01f16d3d2059a6b9a101a5dcb973",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/clay.png",
      "sha256": "8ef8ab53de91cd85483fde29016f5de3495848468468419a88fc0d4a5d71cff2",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/claytop.png",
      "sha256": "dce0a2df9ee51fb1e8209fb435819bcb2e8cc696adf2d141955a511f6148ce5a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/front.png",
      "sha256": "5baa12e0a74126215dab4d4fe0e0c51d52c8540ceb907513358398fa6ec52a59",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/hero.png",
      "sha256": "225eda22d1957a39688f289f4072a7a828f838f3c6510e57511ab6bb77e7efb8",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/rear.png",
      "sha256": "baaebfcee226ece618b09f40db23c68dfd61fe2cde066d2f512886a986e088f4",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/render-config.json",
      "sha256": "9ec0d976697560473bd86daa24aba5fe5a880a7cf086ed75ab2970b764bba15a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/render-manifest.json",
      "sha256": "5e76e70b31a7746d481fca0a4b4d8a1d495860dcd31740adff2fc4fcbd87a482",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/reversehero.png",
      "sha256": "ac20e28b20d498899f625266b935fd74cae24a41c46c481d0d271562682c314d",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/side.png",
      "sha256": "a4b2f570da8a2149545ebe62bc12e868a0cbc5d984f3ce2618465c7a0c7e1ed9",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/silhouette.png",
      "sha256": "82abc034cd824bd66beda2940b6abdbdbfe20fe35cb621aec59fa53358f1cdf3",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/top.png",
      "sha256": "096175d0b0653989ea5cf762d300800ec1c2a4300c022c702367d4844c12a09a",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/halopoa-furrowed-burrow/r001/views-pre-delivery-binding/turntable.json",
      "sha256": "b7d8516352bd124985fd276e2acfef85f917bbded8b6e34ed7f2d0910d6edcce",
      "origin": "source",
      "owner": "halopoa-furrowed-burrow"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/build-jobs.json",
      "sha256": "cbe0132f31a456caa352da0ebc18aef14c426faa9d61b73f6c489ca921f1b499",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/concepts/prompt.txt",
      "sha256": "ca350d496f5e26e43fb59c8a9ac1df55ddce77fa3a3104eb3e3c5f0ed7385eab",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/delivery-render.log",
      "sha256": "177dbf69bac90c9451b7f0020aeeabfb2f71049b15390de36b04d251609d5800",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/execution.jsonl",
      "sha256": "8c341dfd03d7eb19364a0b588b0592127e028d38111224baa11f187c19a1d120",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/failed-attempt-01/build.log",
      "sha256": "0e22bd62dd67d33e50fb342695ad940654ac052f4268ae86669998e09a99652f",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/failed-attempt-01/generator.py",
      "sha256": "5038e3d308a62204bd36d1ab26059b3cfdabc6e1717c48b9d48bec2402c3feb1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/failed-attempt-01/raw-output/hypoturrilites/qa.json",
      "sha256": "5e24b04b130755f76e3f7a857835a37cb6afca01d6ff80c10074c0a693bf51e0",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/failed-attempt-01/source-qa.json",
      "sha256": "5e24b04b130755f76e3f7a857835a37cb6afca01d6ff80c10074c0a693bf51e0",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/khronos.log",
      "sha256": "c861d7e61d4e3da6e810a79c7adbdea8ecff7a58488b1dbead9bf9a532906835",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/measure-source.log",
      "sha256": "d8057d7143cd109dc64d347c85c38f2f6b75b1c9434ed647e28fe331a8c49910",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/execution.jsonl",
      "sha256": "f993bac57b9e376467a0868a1cf17f952ddf9efa8cab76199e89faf89a4ba7ee",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/generator.py",
      "sha256": "898b16c09ca0c4d5f1fd9a39f8afc31e3980dccf6cf25b99824d0286421d8cc5",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/gltf-validator.report.json",
      "sha256": "1afa498a2c2899d53e0361d96e028170174b9363074c7dd93f1cd265079b7a8a",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/hypoturrilites.blend",
      "sha256": "b9764d225b3e1c807956de77e7f3c2e065bb512b16062d31319968832a045ace",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/hypoturrilites.glb",
      "sha256": "2163646a03163834881bbfd391dd3d7995811dd75cfe95dc8e2ce19afacd288b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/metadata.json",
      "sha256": "0de5e088611c644bf2d8e761fdb4d6bf08f72ddf93802f26760c7572de86c2ad",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/preview-hero.png",
      "sha256": "e5feda30d321070ccf94870730a4190daf4c2d2a4312fae36a080a30fa505108",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/qa.json",
      "sha256": "4c88198a5baea790c61df693c97af3d4c05e3acaea1540731f68c1e18fe41782",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/rebuild-1.report.json",
      "sha256": "8dbd589b4ead08dbb8f5744ac447623b916d7e7c72344f8a6e635f1dcf8256ec",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/rebuild-2.report.json",
      "sha256": "16d47b5191537b076265dde07fb72db9e27a603d514eda07630bc3877c77f5bf",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/initial/13abf47882eb95841cb21cb3faacbdb1f1074a3e1c1061d7c344d40d39afdee1/20261020T001202-1d3afc72e47a4449a836b8c9a04dda21/outputs/hypoturrilites/hypoturrilites.blend",
      "sha256": "b9764d225b3e1c807956de77e7f3c2e065bb512b16062d31319968832a045ace",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/initial/13abf47882eb95841cb21cb3faacbdb1f1074a3e1c1061d7c344d40d39afdee1/20261020T001202-1d3afc72e47a4449a836b8c9a04dda21/outputs/hypoturrilites/hypoturrilites.glb",
      "sha256": "2163646a03163834881bbfd391dd3d7995811dd75cfe95dc8e2ce19afacd288b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/initial/13abf47882eb95841cb21cb3faacbdb1f1074a3e1c1061d7c344d40d39afdee1/20261020T001202-1d3afc72e47a4449a836b8c9a04dda21/outputs/hypoturrilites/metadata.json",
      "sha256": "0de5e088611c644bf2d8e761fdb4d6bf08f72ddf93802f26760c7572de86c2ad",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/initial/13abf47882eb95841cb21cb3faacbdb1f1074a3e1c1061d7c344d40d39afdee1/20261020T001202-1d3afc72e47a4449a836b8c9a04dda21/outputs/hypoturrilites/qa.json",
      "sha256": "4f08bb9f9c490b5484b41f239f70f43a0a003b509e3f6783c19bb7a5e36b592c",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/initial/13abf47882eb95841cb21cb3faacbdb1f1074a3e1c1061d7c344d40d39afdee1/20261020T001202-1d3afc72e47a4449a836b8c9a04dda21/request.json",
      "sha256": "2f05fb2e8a19dd254cf148ff18e3ec5e0a7925fe1dc14ab75cb199dbba356246",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/initial/13abf47882eb95841cb21cb3faacbdb1f1074a3e1c1061d7c344d40d39afdee1/20261020T001202-1d3afc72e47a4449a836b8c9a04dda21/result.json",
      "sha256": "cc79209977fbc73b92ba762d5697e9d3208f07a8748357140963ad29ef6e742f",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/initial/13abf47882eb95841cb21cb3faacbdb1f1074a3e1c1061d7c344d40d39afdee1/20261020T001202-1d3afc72e47a4449a836b8c9a04dda21/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/initial/13abf47882eb95841cb21cb3faacbdb1f1074a3e1c1061d7c344d40d39afdee1/20261020T001202-1d3afc72e47a4449a836b8c9a04dda21/stdout.log",
      "sha256": "237628c46e9e43a4e7bddae773c00694408b3563c728340ce9602d7e546af4e4",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-1/bf3cec898401d0e0d68dabf26b5ca9a95ecc25da049467cf56ae4455919c1ea8/20261020T001205-b3126e2693f946a8b7cfc4a08407be6e/outputs/hypoturrilites/hypoturrilites.blend",
      "sha256": "a9443ad61d1df89c96ea00112606fd7d32fa9a802ccfe0e6136b570ef07f35da",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-1/bf3cec898401d0e0d68dabf26b5ca9a95ecc25da049467cf56ae4455919c1ea8/20261020T001205-b3126e2693f946a8b7cfc4a08407be6e/outputs/hypoturrilites/hypoturrilites.glb",
      "sha256": "2163646a03163834881bbfd391dd3d7995811dd75cfe95dc8e2ce19afacd288b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-1/bf3cec898401d0e0d68dabf26b5ca9a95ecc25da049467cf56ae4455919c1ea8/20261020T001205-b3126e2693f946a8b7cfc4a08407be6e/outputs/hypoturrilites/metadata.json",
      "sha256": "1cbd9aae9ed9bf8f5baec8975d89b5795bc21c4077804be52036c6e71d5dcadb",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-1/bf3cec898401d0e0d68dabf26b5ca9a95ecc25da049467cf56ae4455919c1ea8/20261020T001205-b3126e2693f946a8b7cfc4a08407be6e/outputs/hypoturrilites/qa.json",
      "sha256": "7642e6c3f61e17f3d8205a078029e7b5811ff61f0edfed05d2eac0c9ba51a849",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-1/bf3cec898401d0e0d68dabf26b5ca9a95ecc25da049467cf56ae4455919c1ea8/20261020T001205-b3126e2693f946a8b7cfc4a08407be6e/request.json",
      "sha256": "dcfc4201f33e93d37e452b714c593d7a322c0d2901d0354648b7a73cff364e31",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-1/bf3cec898401d0e0d68dabf26b5ca9a95ecc25da049467cf56ae4455919c1ea8/20261020T001205-b3126e2693f946a8b7cfc4a08407be6e/result.json",
      "sha256": "e0fcc1b1292c85b63cd41106068bce67cd18b16798f67d9bb16731018c92049d",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-1/bf3cec898401d0e0d68dabf26b5ca9a95ecc25da049467cf56ae4455919c1ea8/20261020T001205-b3126e2693f946a8b7cfc4a08407be6e/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-1/bf3cec898401d0e0d68dabf26b5ca9a95ecc25da049467cf56ae4455919c1ea8/20261020T001205-b3126e2693f946a8b7cfc4a08407be6e/stdout.log",
      "sha256": "dc6c459178852f938f259878a5319a8b9bee8ac1507032a9d79e730c3115ee59",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-2/01aa0d071f6a2c70c0a6df13274c70fef091996eb939dc1ac570d822956f811d/20261020T001207-797e6753029b493da86badf4219d2317/outputs/hypoturrilites/hypoturrilites.blend",
      "sha256": "e5dde3a8289125e901af5e15b0780283d8e176da8cb2a5c814e3fa81386df86d",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-2/01aa0d071f6a2c70c0a6df13274c70fef091996eb939dc1ac570d822956f811d/20261020T001207-797e6753029b493da86badf4219d2317/outputs/hypoturrilites/hypoturrilites.glb",
      "sha256": "2163646a03163834881bbfd391dd3d7995811dd75cfe95dc8e2ce19afacd288b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-2/01aa0d071f6a2c70c0a6df13274c70fef091996eb939dc1ac570d822956f811d/20261020T001207-797e6753029b493da86badf4219d2317/outputs/hypoturrilites/metadata.json",
      "sha256": "0b6d0eaad8e2929ce71a4d8e0de8be95412c9d088e714d1abb3b73b207f69385",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-2/01aa0d071f6a2c70c0a6df13274c70fef091996eb939dc1ac570d822956f811d/20261020T001207-797e6753029b493da86badf4219d2317/outputs/hypoturrilites/qa.json",
      "sha256": "c5c48079b42974138b13967490aadae8816be6a4d4129cafc26adf32cf2df0a8",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-2/01aa0d071f6a2c70c0a6df13274c70fef091996eb939dc1ac570d822956f811d/20261020T001207-797e6753029b493da86badf4219d2317/request.json",
      "sha256": "8cac1d621a175ecf26657c1b71d5231f65d175ae9ad2143f70ca01dd8a92235a",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-2/01aa0d071f6a2c70c0a6df13274c70fef091996eb939dc1ac570d822956f811d/20261020T001207-797e6753029b493da86badf4219d2317/result.json",
      "sha256": "fda056a1e1a7e6c22e3cf1674f37dde1c99768516c0401fbc790130a508d17ad",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-2/01aa0d071f6a2c70c0a6df13274c70fef091996eb939dc1ac570d822956f811d/20261020T001207-797e6753029b493da86badf4219d2317/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/build/hypoturrilites/r001/rebuild-2/01aa0d071f6a2c70c0a6df13274c70fef091996eb939dc1ac570d822956f811d/20261020T001207-797e6753029b493da86badf4219d2317/stdout.log",
      "sha256": "ff7c8ec53159b436696f4fb7426390d24f913714a5013be0930b943d91271a40",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/runs/20261020T001202-40bd84464e484a04a29faefa1d9e644e/manifest.json",
      "sha256": "29ab82ca7a398cbf636f94be15f56aaee177eff9b4a2ce91e12c7f310b5ff665",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/runs/runs/20261020T001202-40bd84464e484a04a29faefa1d9e644e/summary.json",
      "sha256": "2d7278ad0100fcc086a7a2a3700d8bbfe80dabcd1f28f88492493093bc34fa75",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/source-export.report.json",
      "sha256": "a9b51a7253c63d3a288c07d81f0fd853dac9a6ec0f3a0b25d20b27a7968a40f1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/clay.png",
      "sha256": "7917c1eb02cb0be477f09ccab54369c8d2d3bcc086e7b9521520a8c36718e4b2",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/front.png",
      "sha256": "56de67cb71b5078963015600e565e7a6d0763e80f7eba078388739e0ca084254",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/hero.png",
      "sha256": "e5feda30d321070ccf94870730a4190daf4c2d2a4312fae36a080a30fa505108",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/rear.png",
      "sha256": "4cefe7109ec787c18b05002e3779a9fd7bb2c2e12d4986cb47a6b796880bf676",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/render-config.json",
      "sha256": "a6bc518c87d44f6265605638e3237fe1696a13babf80d7a01ed8a01f879893c2",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/render-manifest.json",
      "sha256": "6a2b7c0d7b6fd9c2656f5ac8b1baa0b620edcc41344778f08d420a08f8c371e8",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/reversehero.png",
      "sha256": "e59c914a0c2f52bf721f639a8458ef7805ef2ee529301dc338be8d71879b69c8",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/side.png",
      "sha256": "e6f027f4ba07c9abc68a5917b250b7dcd8fe3e95e43ee234e73f6553794304e9",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/silhouette.png",
      "sha256": "cbceb7f617f79420ebb58410103e62aaad3236abbb299d028e8c9fa27e6d23b9",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/top.png",
      "sha256": "8055449e93fed357ce7503a60ea605f834bd8ca8a1e144a1c0655b611a000317",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/prototype-02-hollow-axis/views/turntable.json",
      "sha256": "a600d11fdcdce2c3c4a86db75c4cab38c3ab54a01c65a214938423d278f9364e",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/queue.log",
      "sha256": "8f9a95fe2b5e71ac61e67d2c03ffcc57bd003348b163877235c0e0c72302d7e2",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/rebuild-1.log",
      "sha256": "297a2365c20eabe18cecc9e4d377e0f1550d6fe4098194bc367e1e11a5b42690",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/rebuild-2.log",
      "sha256": "8bf5ab9f10909f65933f80456f65a9b7d919817d876c0158e180f563357ff28b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/render.log",
      "sha256": "22054b20c055479476e262e6190b7fcb37b038b52d652724c9d87baa0f03e19f",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/initial/85b45f33c5c0a5ed33efffe65d63be2949d1117e597b890ca5333fd86c04a1fe/20261020T001308-c7c3842668b04eb6aec5930138f60a75/outputs/hypoturrilites/hypoturrilites.blend",
      "sha256": "3aaba1ae3140edd3730a3800fb271a131b3891aa8919d95a0efaff11dfb139cc",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/initial/85b45f33c5c0a5ed33efffe65d63be2949d1117e597b890ca5333fd86c04a1fe/20261020T001308-c7c3842668b04eb6aec5930138f60a75/outputs/hypoturrilites/hypoturrilites.glb",
      "sha256": "23d62a058ebc966e287d6a70feec6c041e30a4c2314418e7504ca59258d56bc1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/initial/85b45f33c5c0a5ed33efffe65d63be2949d1117e597b890ca5333fd86c04a1fe/20261020T001308-c7c3842668b04eb6aec5930138f60a75/outputs/hypoturrilites/metadata.json",
      "sha256": "7a87881a20c7175977a175330813e226131e0dbe5303df749273e3697ecd0664",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/initial/85b45f33c5c0a5ed33efffe65d63be2949d1117e597b890ca5333fd86c04a1fe/20261020T001308-c7c3842668b04eb6aec5930138f60a75/outputs/hypoturrilites/qa.json",
      "sha256": "81632fba3caf2ecf0f7c9e364abeedd739befb5822638ac6a124c0d1e8a2b073",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/initial/85b45f33c5c0a5ed33efffe65d63be2949d1117e597b890ca5333fd86c04a1fe/20261020T001308-c7c3842668b04eb6aec5930138f60a75/request.json",
      "sha256": "4153c1bf1faa7e5ecb2c7132aa40ad37126b12784d543a46c6dbe7c2701801d3",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/initial/85b45f33c5c0a5ed33efffe65d63be2949d1117e597b890ca5333fd86c04a1fe/20261020T001308-c7c3842668b04eb6aec5930138f60a75/result.json",
      "sha256": "6c12cd5e02c227a695a6784c99897d8a004d340d7eddd6059c69acb316c7841b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/initial/85b45f33c5c0a5ed33efffe65d63be2949d1117e597b890ca5333fd86c04a1fe/20261020T001308-c7c3842668b04eb6aec5930138f60a75/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/initial/85b45f33c5c0a5ed33efffe65d63be2949d1117e597b890ca5333fd86c04a1fe/20261020T001308-c7c3842668b04eb6aec5930138f60a75/stdout.log",
      "sha256": "cba9bbd4595da2ea3c9eb29b6d8850f3d882d5c11a5d95dd1c9bd1951f3c32a9",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-1/4cd119d2bb150f6fe00e43314f4339bbf05082fb58614ab5b8e27eac8adf71a0/20261020T001311-c3a9b447c5484f80b08890a452e273d9/outputs/hypoturrilites/hypoturrilites.blend",
      "sha256": "3cc8e3b583357e16b1eafc5e81947ec95dc7745c4469d5379cb85e83e4eed74c",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-1/4cd119d2bb150f6fe00e43314f4339bbf05082fb58614ab5b8e27eac8adf71a0/20261020T001311-c3a9b447c5484f80b08890a452e273d9/outputs/hypoturrilites/hypoturrilites.glb",
      "sha256": "23d62a058ebc966e287d6a70feec6c041e30a4c2314418e7504ca59258d56bc1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-1/4cd119d2bb150f6fe00e43314f4339bbf05082fb58614ab5b8e27eac8adf71a0/20261020T001311-c3a9b447c5484f80b08890a452e273d9/outputs/hypoturrilites/metadata.json",
      "sha256": "80888414595b4779bc7c3b7f88e75c7a554ea9bcc4bf01d6847b5b714faf78f1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-1/4cd119d2bb150f6fe00e43314f4339bbf05082fb58614ab5b8e27eac8adf71a0/20261020T001311-c3a9b447c5484f80b08890a452e273d9/outputs/hypoturrilites/qa.json",
      "sha256": "7fc0626dfc4cff9630ea223bd783da2e589baee6f52702153831890263ddc8a3",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-1/4cd119d2bb150f6fe00e43314f4339bbf05082fb58614ab5b8e27eac8adf71a0/20261020T001311-c3a9b447c5484f80b08890a452e273d9/request.json",
      "sha256": "23b83d7ffc9d26b380eff6f772994edca71f36b1eea1a540fed0df8c2cbba489",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-1/4cd119d2bb150f6fe00e43314f4339bbf05082fb58614ab5b8e27eac8adf71a0/20261020T001311-c3a9b447c5484f80b08890a452e273d9/result.json",
      "sha256": "f169afa999840d4afe68d54ab95a5d72208d41bf1b86f91ef14c38134e2fcf2f",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-1/4cd119d2bb150f6fe00e43314f4339bbf05082fb58614ab5b8e27eac8adf71a0/20261020T001311-c3a9b447c5484f80b08890a452e273d9/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-1/4cd119d2bb150f6fe00e43314f4339bbf05082fb58614ab5b8e27eac8adf71a0/20261020T001311-c3a9b447c5484f80b08890a452e273d9/stdout.log",
      "sha256": "d1293eb49b2fda4d9e69685d4527e49b0d9b7957947fccb083aa4a2293a1d455",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-2/47566f881bba8b699b9bb48860e6327f82da49ea22a58da76bdf756a1c6b9451/20261020T001313-b3df0dbe4c8847d99c10c0d0dea4c1f3/outputs/hypoturrilites/hypoturrilites.blend",
      "sha256": "83696d443d827af6a737d34403e70f36370fc74ead3b58865c4761aa7877078a",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-2/47566f881bba8b699b9bb48860e6327f82da49ea22a58da76bdf756a1c6b9451/20261020T001313-b3df0dbe4c8847d99c10c0d0dea4c1f3/outputs/hypoturrilites/hypoturrilites.glb",
      "sha256": "23d62a058ebc966e287d6a70feec6c041e30a4c2314418e7504ca59258d56bc1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-2/47566f881bba8b699b9bb48860e6327f82da49ea22a58da76bdf756a1c6b9451/20261020T001313-b3df0dbe4c8847d99c10c0d0dea4c1f3/outputs/hypoturrilites/metadata.json",
      "sha256": "239b6e3e45f91f264ea81b16b6dde7c69b32e1910f74156ebd31f5e3d7d157da",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-2/47566f881bba8b699b9bb48860e6327f82da49ea22a58da76bdf756a1c6b9451/20261020T001313-b3df0dbe4c8847d99c10c0d0dea4c1f3/outputs/hypoturrilites/qa.json",
      "sha256": "222435a2300ad86c324eb55db10ed250a2746231f7acf0ee08e94e482f3f2e70",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-2/47566f881bba8b699b9bb48860e6327f82da49ea22a58da76bdf756a1c6b9451/20261020T001313-b3df0dbe4c8847d99c10c0d0dea4c1f3/request.json",
      "sha256": "e37d9cefb85b4595b60eb88d592272ae187391a60572ba8f41258833f85f88c3",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-2/47566f881bba8b699b9bb48860e6327f82da49ea22a58da76bdf756a1c6b9451/20261020T001313-b3df0dbe4c8847d99c10c0d0dea4c1f3/result.json",
      "sha256": "770db787e64dc46fce325d6aa1a98cd22a0a89a23d4a3d93f74365eeb6d9002b",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-2/47566f881bba8b699b9bb48860e6327f82da49ea22a58da76bdf756a1c6b9451/20261020T001313-b3df0dbe4c8847d99c10c0d0dea4c1f3/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/build/hypoturrilites/r001/rebuild-2/47566f881bba8b699b9bb48860e6327f82da49ea22a58da76bdf756a1c6b9451/20261020T001313-b3df0dbe4c8847d99c10c0d0dea4c1f3/stdout.log",
      "sha256": "0c8744888b1794b2fd59af1336148c572102182acadce1af83bbd2a23ec10350",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/runs/20261020T001308-b36efc29903c43629cdf500f405323d5/manifest.json",
      "sha256": "29ab82ca7a398cbf636f94be15f56aaee177eff9b4a2ce91e12c7f310b5ff665",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runs/runs/20261020T001308-b36efc29903c43629cdf500f405323d5/summary.json",
      "sha256": "388470dba3b6462c140bcaaf137c318baa0b3e067bbf1ace24b3b4460cd0734f",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/runtime.log",
      "sha256": "fb457ab1936a463fa29ff41cb588f1c208d56c4c656480a1c4277bd3d53f93c5",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/source-reopen.log",
      "sha256": "a7806e987751844cc2ecc8332ea6e8ec701edd0cf7bfaf3be56455fb94e7631f",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/clay.png",
      "sha256": "ad89765aaade19b4744bbfb999910d1d55ed2827fb32cadfe01627afa429c723",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/front.png",
      "sha256": "7b6a3652f5bfbaf7770354501862ea09ece1acd5141a91bac411f38cd19d23d5",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/hero.png",
      "sha256": "d7995872e45b2f49c2270a2b52b8a0a54d2fa177c3d95883ee6b3ae0926c9ffe",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/rear.png",
      "sha256": "b6c0f2847c1ca6a8138a8819360567288057ee78739be34e661f3db6c2aee106",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/render-config.json",
      "sha256": "560b9e598946920926566c5942286b401d45ae5c2116cf4c379dd4086410b436",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/render-manifest.json",
      "sha256": "189192cb226617d6edaa4f1934ccdfd8374c268f699fda6696a94f2e122a1be4",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/reversehero.png",
      "sha256": "b6e6df83cebad50014c695a829e57fe27975d898b2759993ee0fed68681197dc",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/side.png",
      "sha256": "c78109287b64d6eb30f06a1c45956280bd5c98255f767599ae82bceb0fbe2be9",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/silhouette.png",
      "sha256": "f4c3c31d5283ea7c9764b2ff06e523e4d076650faee0f52bf2e64ee23862a1e1",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/top.png",
      "sha256": "7960900b55770d828abff6bffa870a303a9c5424c235fbcfc8d2d53d6379e4b4",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/hypoturrilites/r001/views-pre-delivery-binding/turntable.json",
      "sha256": "796e3b4264c35123bf0528f163e31107485a421dd899ca0f7cb5d48b0c783f8a",
      "origin": "source",
      "owner": "hypoturrilites"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/identity-provenance.json",
      "sha256": "c7f25011ab60b6b51aafb1ac48b8dec553a60b3682536c1b75aaffc632d42ad1",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/build-jobs.json",
      "sha256": "12693734eaf4fe06858f64ea808a2645df815ae26f02576c0db3da16815e5353",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/delivery-render.log",
      "sha256": "6723227e6ab52d17f2ce134276474c8072544de00873d279c0895ddfa11a192a",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/execution.jsonl",
      "sha256": "50e747906752d175af26ba8bb15dc01a8e5ad22d77124072787d77e96d983e77",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/clay.png",
      "sha256": "5b1ce10ce6710e99303ec6a64843d070f8ea36eb767750dc6c87bd9698fe7f02",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/front.png",
      "sha256": "20ecb089a5df246671c7dec01145bbffc132b2fb072315f1da42a4eba9628e43",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/hero.png",
      "sha256": "8f381c3b296b4d176e1304e229ad7e21bbcbcb16eab15e41c964d1c710e268b6",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/rear.png",
      "sha256": "d9b145156d72560869671f9f7f9c6e782a6b906583d5644d3681f077d7de8e50",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/render-config.json",
      "sha256": "f01d43d5a5d61a377a02e5ae28eee69568f277137f19cd2433b217aa3cb7d1cd",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/render-manifest.json",
      "sha256": "ef0a9f18a809529e0c5ae68034862e36e289462d3c2b1d341f2137d96414dffc",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/reversehero.png",
      "sha256": "7bd647d3615a7df1087d81ab4abb88aa7aeff8abf21febc5df309eea5fd7c2e7",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/side.png",
      "sha256": "7c030f127952c14c52718776c2748be1dbb0c97b7f701c98bb12b59cb63ea440",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/silhouette.png",
      "sha256": "276cfd045bbd23e2b924c7db6f462d57212363a005f89bafad0bff0ef8452ade",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/top.png",
      "sha256": "0c6b273bfbaa558b07db61a5b15f51616a11372f398bd88394381f2bf1367664",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/initial-too-small-framing-views/turntable.json",
      "sha256": "7dc1811ad9e1a905f368b8ce074314f5ae17f8462b6bfb33c2446bd32801dbd3",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/khronos.log",
      "sha256": "aa3857d3ab02e40566d4671bcbaa743e2b86f43cb2cb2a749763deaac529f2a3",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/measure-source.log",
      "sha256": "c31cfb1dee8587edd7092d3034c493f706187d7343299c3de72d709cd08dfb93",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/execution.jsonl",
      "sha256": "a5a2a3e404a1e4d66cab9c747bb26c56dd3d9997f7cdd41231b6dc6dcb1b1aef",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/generator.py",
      "sha256": "b801f24388663e7f65746242db451bdadd0ee2471db734bccfa118f5d4091dc2",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/gltf-validator.report.json",
      "sha256": "52d7a80a9a74eaa5ce7ebf2fbfda2e3c14ff09321f1f6d39173d67da54d6cae4",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/iodes-brownii.blend",
      "sha256": "9a4399facff056c72368e8ebadb9bc88a4e68490ba58b4ee0c59ea9065a48eb4",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/iodes-brownii.glb",
      "sha256": "fad72de8d3a5214e402f1dbd77b07ccea0a6ccef3d4250e54767edfbb3cb300e",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/metadata.json",
      "sha256": "b99c35eb5c240387e16a164884530d14a8c1664e370f19b7fb08c3d942d556c4",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/preview-hero.png",
      "sha256": "8f381c3b296b4d176e1304e229ad7e21bbcbcb16eab15e41c964d1c710e268b6",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/qa.json",
      "sha256": "ae0dabe946ca388031ca2aa77a291e2e3fe886702cf0aed4578be975c9ee36d1",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/rebuild-1.report.json",
      "sha256": "fd9b64fc04f606a8c329b94573f0a6612bf429117dc1d3d7eaf198538f76e104",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/rebuild-2.report.json",
      "sha256": "0b16a4578b402f7e993c7d551f126c2c755c35a3add463ab6caf6c36a6b7132a",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/initial/d68ff6af846c9809299b2478dc230a609bd1e0314780fce7bcaaf1b25d46da62/20261020T001615-4324a565ab564c82ab21ec16c8a0298a/outputs/iodes-brownii/iodes-brownii.blend",
      "sha256": "9a4399facff056c72368e8ebadb9bc88a4e68490ba58b4ee0c59ea9065a48eb4",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/initial/d68ff6af846c9809299b2478dc230a609bd1e0314780fce7bcaaf1b25d46da62/20261020T001615-4324a565ab564c82ab21ec16c8a0298a/outputs/iodes-brownii/iodes-brownii.glb",
      "sha256": "fad72de8d3a5214e402f1dbd77b07ccea0a6ccef3d4250e54767edfbb3cb300e",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/initial/d68ff6af846c9809299b2478dc230a609bd1e0314780fce7bcaaf1b25d46da62/20261020T001615-4324a565ab564c82ab21ec16c8a0298a/outputs/iodes-brownii/metadata.json",
      "sha256": "b99c35eb5c240387e16a164884530d14a8c1664e370f19b7fb08c3d942d556c4",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/initial/d68ff6af846c9809299b2478dc230a609bd1e0314780fce7bcaaf1b25d46da62/20261020T001615-4324a565ab564c82ab21ec16c8a0298a/outputs/iodes-brownii/qa.json",
      "sha256": "542355cdef610e68e39df0fb48379def6f58f35113dbb43515f7c97464983188",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/initial/d68ff6af846c9809299b2478dc230a609bd1e0314780fce7bcaaf1b25d46da62/20261020T001615-4324a565ab564c82ab21ec16c8a0298a/request.json",
      "sha256": "362e64daa93b1f2aff0887a833c1deee1c98f818da87e81fbc835bbe69738d1d",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/initial/d68ff6af846c9809299b2478dc230a609bd1e0314780fce7bcaaf1b25d46da62/20261020T001615-4324a565ab564c82ab21ec16c8a0298a/result.json",
      "sha256": "43116923b5b23cf1a524df106a80cb833d5f212b293f0143f74eff1f2a3d0fb6",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/initial/d68ff6af846c9809299b2478dc230a609bd1e0314780fce7bcaaf1b25d46da62/20261020T001615-4324a565ab564c82ab21ec16c8a0298a/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/initial/d68ff6af846c9809299b2478dc230a609bd1e0314780fce7bcaaf1b25d46da62/20261020T001615-4324a565ab564c82ab21ec16c8a0298a/stdout.log",
      "sha256": "44cf9a805f696f7440acfbc36677b0508026162b99c5619452f4a922c3e489c0",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-1/9b4b902898a8b3d8f8c441d1afe7d7c130e08652397c375345381c4bef876c61/20261020T001618-acaad5dadab64dd7af79fc2cf7e5bcca/outputs/iodes-brownii/iodes-brownii.blend",
      "sha256": "8cf5ee2813275fe1885f9842068bf70f5194833864450ce14fa02d60d080ac5d",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-1/9b4b902898a8b3d8f8c441d1afe7d7c130e08652397c375345381c4bef876c61/20261020T001618-acaad5dadab64dd7af79fc2cf7e5bcca/outputs/iodes-brownii/iodes-brownii.glb",
      "sha256": "fad72de8d3a5214e402f1dbd77b07ccea0a6ccef3d4250e54767edfbb3cb300e",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-1/9b4b902898a8b3d8f8c441d1afe7d7c130e08652397c375345381c4bef876c61/20261020T001618-acaad5dadab64dd7af79fc2cf7e5bcca/outputs/iodes-brownii/metadata.json",
      "sha256": "b3556d0d99c47511518b1dfbc84dfc83dc61f36f1d23aa02d4fca1a81cab1296",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-1/9b4b902898a8b3d8f8c441d1afe7d7c130e08652397c375345381c4bef876c61/20261020T001618-acaad5dadab64dd7af79fc2cf7e5bcca/outputs/iodes-brownii/qa.json",
      "sha256": "3d9b8495d38c1ff4311d8e6e997769ae3bab7b4299298e635993e550e7a57d6d",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-1/9b4b902898a8b3d8f8c441d1afe7d7c130e08652397c375345381c4bef876c61/20261020T001618-acaad5dadab64dd7af79fc2cf7e5bcca/request.json",
      "sha256": "0623643d1afc42c360f244492b0895f962e333848d8ebf27ecd85d576eef7dd4",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-1/9b4b902898a8b3d8f8c441d1afe7d7c130e08652397c375345381c4bef876c61/20261020T001618-acaad5dadab64dd7af79fc2cf7e5bcca/result.json",
      "sha256": "2834570e6d7bc70e0604da75c210c8e9d2a3263f6477a86f1aeef3ec5beb2b29",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-1/9b4b902898a8b3d8f8c441d1afe7d7c130e08652397c375345381c4bef876c61/20261020T001618-acaad5dadab64dd7af79fc2cf7e5bcca/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-1/9b4b902898a8b3d8f8c441d1afe7d7c130e08652397c375345381c4bef876c61/20261020T001618-acaad5dadab64dd7af79fc2cf7e5bcca/stdout.log",
      "sha256": "0072af7f6604e878fe9a04bd25fc6762a50926b5d8e772544efb754706587111",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-2/8c0e3d1b8741baca25f6cf74d1783c5e211f6a74b09529abccac7284fa8389b7/20261020T001620-b5e287cd592c48a4aa7ca20cb5421a4c/outputs/iodes-brownii/iodes-brownii.blend",
      "sha256": "0f24859f9aee7b99e2fea8906fe7674371293ac5dfc76b3ab496f10d33d0a159",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-2/8c0e3d1b8741baca25f6cf74d1783c5e211f6a74b09529abccac7284fa8389b7/20261020T001620-b5e287cd592c48a4aa7ca20cb5421a4c/outputs/iodes-brownii/iodes-brownii.glb",
      "sha256": "fad72de8d3a5214e402f1dbd77b07ccea0a6ccef3d4250e54767edfbb3cb300e",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-2/8c0e3d1b8741baca25f6cf74d1783c5e211f6a74b09529abccac7284fa8389b7/20261020T001620-b5e287cd592c48a4aa7ca20cb5421a4c/outputs/iodes-brownii/metadata.json",
      "sha256": "a028b311e8a762e47442d8d743345cab18c2e413b359b712e1787eb7f7dbbc31",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-2/8c0e3d1b8741baca25f6cf74d1783c5e211f6a74b09529abccac7284fa8389b7/20261020T001620-b5e287cd592c48a4aa7ca20cb5421a4c/outputs/iodes-brownii/qa.json",
      "sha256": "b3c7144a48341bb5598b7ede697966f483a628a70b7780a57d1950b14fb951c0",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-2/8c0e3d1b8741baca25f6cf74d1783c5e211f6a74b09529abccac7284fa8389b7/20261020T001620-b5e287cd592c48a4aa7ca20cb5421a4c/request.json",
      "sha256": "70fc302033d5aa2afb604891a69ccc2a2f86ed8812e2c2793f16b63f75c22675",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-2/8c0e3d1b8741baca25f6cf74d1783c5e211f6a74b09529abccac7284fa8389b7/20261020T001620-b5e287cd592c48a4aa7ca20cb5421a4c/result.json",
      "sha256": "029bcb89e9fe3a5ab2e68130b9a34e1563b1f44ca8ea9766d8bbae2e64d53753",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-2/8c0e3d1b8741baca25f6cf74d1783c5e211f6a74b09529abccac7284fa8389b7/20261020T001620-b5e287cd592c48a4aa7ca20cb5421a4c/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/build/iodes-brownii/r001/rebuild-2/8c0e3d1b8741baca25f6cf74d1783c5e211f6a74b09529abccac7284fa8389b7/20261020T001620-b5e287cd592c48a4aa7ca20cb5421a4c/stdout.log",
      "sha256": "7a22124b23543a057e067e559c40c934300585df591ae52a5601449daab83a34",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/runs/20261020T001615-835e03b6897147439edcd062d434c06b/manifest.json",
      "sha256": "aaa02fb9ecb9e309529bee75b9a90a60027aebaf60b47b51546b5ac523b6e24c",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runs/runs/20261020T001615-835e03b6897147439edcd062d434c06b/summary.json",
      "sha256": "ee1b50321a30de9fc321539428467ba7fa2a9c0996ae41965b3fb1c830b51dff",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runtime/front.png",
      "sha256": "d73e60dc0f02f1a0983e2367310043d08299219ea85bb962d3b4024d85da1d33",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runtime/hero.png",
      "sha256": "dd32e52962d9736e191a8450581be5abf8529cb1c02357a69a8f9d665821016d",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runtime/reversehero.png",
      "sha256": "fbee9b72a6ff548bed95cff994ff5033621f99a3e990b7ad4ecc2a96498f52a4",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runtime/runtime-report.json",
      "sha256": "6034e1bd4e29206a9e7d0c60a58e0e7819d42006a9fa2778a5950ca322d3acd7",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runtime/scene-9.png",
      "sha256": "69d8c9b5ba8cdae076f2ec2f21474034d99b44a3f4418fdb65d5fd496203e2c0",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runtime/side.png",
      "sha256": "0204201568ecee06fe76743b839ac6c8a671e29d1332fb4b34af02f2805e5283",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/runtime/top.png",
      "sha256": "cd2fb3029c12eefd2c82d06dc8863999faf8d2a5701cd5de1d9fe966c2480fd1",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/source-export.report.json",
      "sha256": "6bf74f3057849bb2ac7419fdd342f1c50089afd81f7749a2b192598d8c5d7b8b",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/source-measurements.json",
      "sha256": "2951495f818c046015f916f9c56e8352841c4395ceb3cfe414a9b6bc10c0bad8",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/clay.png",
      "sha256": "aaba48ddc9ee4840495a8f1c3a0ace1dfb7e865b82cca80effc001fcc071310e",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/front.png",
      "sha256": "499dfacaa687adae6a919c03d03c05f38326b4360dca78ee60cf2060fcac8fd8",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/hero.png",
      "sha256": "4e90853db27f1bc8e49347addeb811cf177aaa140e4ecac626b794c2045e4fd9",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/rear.png",
      "sha256": "e196ade227b073fce9056f2f99bca4467db3d2058686815ea5450eb6e784d222",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/render-config.json",
      "sha256": "bcf8c797c3694e0ae1c34be92053d2d1853af2587560ec1798f5ba224110ee33",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/render-manifest.json",
      "sha256": "4c2acd0a6f28cba4eac1ba11455ff6a6bafdace90c865982eb762645855467d1",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/reversehero.png",
      "sha256": "061183b0a2d49d22fd24bfa95267318a3631bf42d61f0f92ef7604c916398eac",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/side.png",
      "sha256": "23a13598e463aaba20874d795d6b4ac6361d39f9f37b96959afdca7e0acda58f",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/silhouette.png",
      "sha256": "70a251f5368a87ae09d80a37f5f9fbbd6ac0c0c06b5aa5bbf207e8df9030f29d",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/top.png",
      "sha256": "881383c4be6dfd391aab7f3a33b25852bd88e22d85cec21bf183b9d12acbc567",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/prototype-01-grid-reticulum/views/turntable.json",
      "sha256": "69804e57b009d66bc0083d60dfb80e7e42ff615c8c849c49950773c16bfe8338",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/queue.log",
      "sha256": "018dc7aa9193df61b31be0a96ac3d943bec3f795059f4a41769dca31d68e1b34",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/rebuild-1.log",
      "sha256": "ace7acb3f697ca60335b40397093d912c9827aaa99c4962ee2c1187644caecd3",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/rebuild-2.log",
      "sha256": "a26d56a79f497f6d791e651d48dc5183b7033def89d23ac673f7aaf9dbadc9be",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/render-millimeter-fit.log",
      "sha256": "254301c58a792e91386a2afa22d98ff8e438dddb8b496d54d1e560523052a9c3",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/render.log",
      "sha256": "ff9121f0d10892a631cc1449fd7cf2091ece1129395becae33e119763670baaa",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/initial/f4ce3f121375f3c6fdcbffa31115d751739053aad7bd8692a99aae25b7dd35e8/20261020T001746-f90df3f4a452486083ccfe508c9b5026/outputs/iodes-brownii/iodes-brownii.blend",
      "sha256": "85b7c6596cdd0c3c21ccd6ac25863569961c5686929243393a7753af46fdb55c",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/initial/f4ce3f121375f3c6fdcbffa31115d751739053aad7bd8692a99aae25b7dd35e8/20261020T001746-f90df3f4a452486083ccfe508c9b5026/outputs/iodes-brownii/iodes-brownii.glb",
      "sha256": "f3604fbfab6eb74df9dfc6924994e642dc9722681a3329a91f21c0d42c997dff",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/initial/f4ce3f121375f3c6fdcbffa31115d751739053aad7bd8692a99aae25b7dd35e8/20261020T001746-f90df3f4a452486083ccfe508c9b5026/outputs/iodes-brownii/metadata.json",
      "sha256": "250fa7997484f1fccd906761f7433808f56e72fc064c929b0f6eb1dae95ed345",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/initial/f4ce3f121375f3c6fdcbffa31115d751739053aad7bd8692a99aae25b7dd35e8/20261020T001746-f90df3f4a452486083ccfe508c9b5026/outputs/iodes-brownii/qa.json",
      "sha256": "53ca0fb66001207657d4f89d80a25a567561446f7bbe3336bdecc166928a75e8",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/initial/f4ce3f121375f3c6fdcbffa31115d751739053aad7bd8692a99aae25b7dd35e8/20261020T001746-f90df3f4a452486083ccfe508c9b5026/request.json",
      "sha256": "2b9bcc004d5ffbb226915566d6c70cd7b1d57b800a81484ce7791aebf54c11ba",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/initial/f4ce3f121375f3c6fdcbffa31115d751739053aad7bd8692a99aae25b7dd35e8/20261020T001746-f90df3f4a452486083ccfe508c9b5026/result.json",
      "sha256": "a841a4d041ee3d1b91b525799f8b53247d582e9e320ab8f071485402f49bccda",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/initial/f4ce3f121375f3c6fdcbffa31115d751739053aad7bd8692a99aae25b7dd35e8/20261020T001746-f90df3f4a452486083ccfe508c9b5026/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/initial/f4ce3f121375f3c6fdcbffa31115d751739053aad7bd8692a99aae25b7dd35e8/20261020T001746-f90df3f4a452486083ccfe508c9b5026/stdout.log",
      "sha256": "0940d83390c3284ca04af4b43848b665b2dcea5df111f2dcf8ceebf7a8f4a6fe",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-1/5dee763c2a7297b846bf71e6cc804759ba882172868e8ec52ad132e598a638cf/20261020T001748-4c642afd5bd740d3a6bde6754c1084db/outputs/iodes-brownii/iodes-brownii.blend",
      "sha256": "e132b686e7b8de6a442323b96b411813ff5316e094b9bebbcb087c380493b293",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-1/5dee763c2a7297b846bf71e6cc804759ba882172868e8ec52ad132e598a638cf/20261020T001748-4c642afd5bd740d3a6bde6754c1084db/outputs/iodes-brownii/iodes-brownii.glb",
      "sha256": "f3604fbfab6eb74df9dfc6924994e642dc9722681a3329a91f21c0d42c997dff",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-1/5dee763c2a7297b846bf71e6cc804759ba882172868e8ec52ad132e598a638cf/20261020T001748-4c642afd5bd740d3a6bde6754c1084db/outputs/iodes-brownii/metadata.json",
      "sha256": "37464bfc7f7474874ef0234ad9db000f24ae9b28990ea55d1d15b0166ed521df",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-1/5dee763c2a7297b846bf71e6cc804759ba882172868e8ec52ad132e598a638cf/20261020T001748-4c642afd5bd740d3a6bde6754c1084db/outputs/iodes-brownii/qa.json",
      "sha256": "0bcc410d5d79a01a0b20da602f0e7486b2380b387e03959e95d06f44b1c3e4c5",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-1/5dee763c2a7297b846bf71e6cc804759ba882172868e8ec52ad132e598a638cf/20261020T001748-4c642afd5bd740d3a6bde6754c1084db/request.json",
      "sha256": "0be6d43eb8eac7fab47ed807c9b6ec96193f74c3070e553fa61dc7420760e99d",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-1/5dee763c2a7297b846bf71e6cc804759ba882172868e8ec52ad132e598a638cf/20261020T001748-4c642afd5bd740d3a6bde6754c1084db/result.json",
      "sha256": "c20fb1d0533b8d19942fe5b5c41cf9d28eebccda5c4a1cb7fc46c5a1a93656f0",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-1/5dee763c2a7297b846bf71e6cc804759ba882172868e8ec52ad132e598a638cf/20261020T001748-4c642afd5bd740d3a6bde6754c1084db/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-1/5dee763c2a7297b846bf71e6cc804759ba882172868e8ec52ad132e598a638cf/20261020T001748-4c642afd5bd740d3a6bde6754c1084db/stdout.log",
      "sha256": "c25c97522e4f083305a0ad7c86e2254ee7e1be6f064c900436737191664eb007",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-2/7e3a437979eeb0685613db62bd875e4a85d240957a6abdc63608c241a70c0403/20261020T001751-e3d9a8c8702d4ab582497b64e54c66be/outputs/iodes-brownii/iodes-brownii.blend",
      "sha256": "8d3094f9bb85fb07790c8d7001797dae909dcda090e53d2d9df4fac3ebbc8664",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-2/7e3a437979eeb0685613db62bd875e4a85d240957a6abdc63608c241a70c0403/20261020T001751-e3d9a8c8702d4ab582497b64e54c66be/outputs/iodes-brownii/iodes-brownii.glb",
      "sha256": "f3604fbfab6eb74df9dfc6924994e642dc9722681a3329a91f21c0d42c997dff",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-2/7e3a437979eeb0685613db62bd875e4a85d240957a6abdc63608c241a70c0403/20261020T001751-e3d9a8c8702d4ab582497b64e54c66be/outputs/iodes-brownii/metadata.json",
      "sha256": "50b8583e79a8438a544fea87734c6e5308a60cd859387ab030f90b4ecd1202b1",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-2/7e3a437979eeb0685613db62bd875e4a85d240957a6abdc63608c241a70c0403/20261020T001751-e3d9a8c8702d4ab582497b64e54c66be/outputs/iodes-brownii/qa.json",
      "sha256": "9e2eb3bd45b788488d1f9293532c5185dd00f67eac90668e7c073f929d53c8be",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-2/7e3a437979eeb0685613db62bd875e4a85d240957a6abdc63608c241a70c0403/20261020T001751-e3d9a8c8702d4ab582497b64e54c66be/request.json",
      "sha256": "b3e3360f94a3c22f45765e955c1096ee3c1491d27e7665963b7efb73d5933b89",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-2/7e3a437979eeb0685613db62bd875e4a85d240957a6abdc63608c241a70c0403/20261020T001751-e3d9a8c8702d4ab582497b64e54c66be/result.json",
      "sha256": "50bdedefb1b2d97a97fae4a6552a31ad493980f79f10ccff174a2cc4aec3e229",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-2/7e3a437979eeb0685613db62bd875e4a85d240957a6abdc63608c241a70c0403/20261020T001751-e3d9a8c8702d4ab582497b64e54c66be/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/build/iodes-brownii/r001/rebuild-2/7e3a437979eeb0685613db62bd875e4a85d240957a6abdc63608c241a70c0403/20261020T001751-e3d9a8c8702d4ab582497b64e54c66be/stdout.log",
      "sha256": "58a77507b5c55c7918150f1b556f4454e63cbba23d28c29248c03be5fd23c9d6",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/runs/20261020T001746-73d6ac8ed68444479cd2bdb4fcf79a01/manifest.json",
      "sha256": "aaa02fb9ecb9e309529bee75b9a90a60027aebaf60b47b51546b5ac523b6e24c",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runs/runs/20261020T001746-73d6ac8ed68444479cd2bdb4fcf79a01/summary.json",
      "sha256": "fea2b7883665c0ba40bbf578b74a3f8554bac7a25d330abfb531d98ba84acf18",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/runtime.log",
      "sha256": "96e6c5480ba5cb2ec6bc4550c31258ceedaa2ae28cae5cbcbf3e63de072345c1",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/source-reopen.log",
      "sha256": "fc9db596a42c691ccacc6b20db5bf8c17141011905b68cb1ea07f488d306d690",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/clay.png",
      "sha256": "36ff32c3f3aae455f12dffa60a70a794780609d673db3ed2bbed075a9ab43147",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/front.png",
      "sha256": "1458c968a613653f65f934c63e5fe8f78f08b020fb86be4773f87177cf7d3a37",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/hero.png",
      "sha256": "0fe65881ad52398d2a8fbd75f265f4963579348ceb6b01a35388ee3d58d8ccce",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/rear.png",
      "sha256": "74b47af29388ba0d34960b8855201f53832fff4a27b882f8ebae28f3412da58c",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/render-config.json",
      "sha256": "bcf8c797c3694e0ae1c34be92053d2d1853af2587560ec1798f5ba224110ee33",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/render-manifest.json",
      "sha256": "3ad11d9e362a233d9d3d05f62ffeee66741921289460844f48ec39a76e558a82",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/reversehero.png",
      "sha256": "44ee9c722eedfddd6bbf86a60a34cba7dc3c4c0249b6361239c3690425d29f54",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/side.png",
      "sha256": "2e8c5cbbc4974038f896490c0c49726057e078306b2c3ff3abf78776d025a824",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/silhouette.png",
      "sha256": "b453ca25e65528eb9ec1cc0e3ead01eaec0ff250965ee1295dbe7ab8bf0494c7",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/top.png",
      "sha256": "57dc099095e2699364d217656700c2f5184a8fa18dbd6601f6c0033baeac00d3",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/iodes-brownii/r001/views-pre-delivery-binding/turntable.json",
      "sha256": "4a962a028f3301fc78c9bac97564a0505ee467c74a934e2e62386a55782ca738",
      "origin": "source",
      "owner": "iodes-brownii"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/measure-source.py",
      "sha256": "f7ef644693e391149297dcec676e5103b31ecbf356c181cf7a37538380f630c7",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/prepare.py",
      "sha256": "0662bc56957daa66c135318234e689a8d8ae89aaf8a6ea81ef56528df669df20",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/render.py",
      "sha256": "259b1cea4838a1fa37c42610800f8f75b9b5fffc8f8d7770be1c9931b173d2f3",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/run.py",
      "sha256": "c1106e2026e5e14284591f99cc845427837ac787001b33727cf00a09ea73637e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/runtime.mjs",
      "sha256": "18347c470e3822fb419d8402b5a3462cedb150f270d81e3416a681f3f9706699",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/static-view-binding.py",
      "sha256": "612372f0d744d7ee365eec57ef4fafdb4b8305cb83a779ef83bb2e6019f6c8b0",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/verify-identity-update.py",
      "sha256": "e7a37b7c9010150ede6f8f41ec764ca9f17f9737ed6c54bdc52aa949a2d236be",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/build-jobs.json",
      "sha256": "cb17485da76f2084b2bb96ee4ff453e134339d55a61d7db8c0b70b0683f58f56",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/delivery-render.log",
      "sha256": "bf7aa274e62d0263fa46ab5a67bb91000fb0544cfd2f0355eb4a120aa21eb534",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/execution.jsonl",
      "sha256": "ddd77dbd5c55868cef607010a5d26d39869ea08a8ede8a619f8f9ae4be5f3c2e",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/khronos.log",
      "sha256": "81dabd81c4f85aa64566f25b8a46234bf1a82083bd8016c9145b3ea15a48a4c2",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/measure-source.log",
      "sha256": "5e8c0e6a91047741ec8388e9acad9e6514a8b885b5222c88d0fac96211e25518",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/execution.jsonl",
      "sha256": "7cced7484dc800e7419503f86b6edb7499bab4bc958ffa52cd1b80a632388664",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/generator.py",
      "sha256": "89615507e5a48bdd8f199b30c36dfb1edfd2039900a6e1b6c9bd25825cdca09f",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/gltf-validator.report.json",
      "sha256": "d2ef56790321c8f8579c73698b05328e31c4e39259c6ac0f265ed201306574f6",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/metadata.json",
      "sha256": "95422a8c2e6d640c843b75422474c8505dede3574bdd1ea1f8b578978266af42",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/preview-hero.png",
      "sha256": "b279df19dee2d3dd840ad258c67434ad3fef780e084474d54e5cae32fed11047",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/qa.json",
      "sha256": "ebbf5a0bad3b07ee695f26dced396fd752bc9d4779295cfe4e12e99ed586cdc5",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/rebuild-1.report.json",
      "sha256": "2bda584f01f9ab7c91f11d8adf464c5b154028c545e92ed0fa1edc2f0c2de1e1",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/rebuild-2.report.json",
      "sha256": "0bd59eadcd8afe9de360d189a7af6274424aaaff492b266bc2ad88b7d2d94bb9",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/initial/9389c70bd6e7e5742b2061bbc518ac7085e7ca34e866b7cb511e733d93aa6107/20261020T002015-86347e943d4c43d698b3ecd87f7665fb/outputs/welded-ignimbrite-outcrop/metadata.json",
      "sha256": "95422a8c2e6d640c843b75422474c8505dede3574bdd1ea1f8b578978266af42",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/initial/9389c70bd6e7e5742b2061bbc518ac7085e7ca34e866b7cb511e733d93aa6107/20261020T002015-86347e943d4c43d698b3ecd87f7665fb/outputs/welded-ignimbrite-outcrop/qa.json",
      "sha256": "393467d51772060a2c4d7fb3ec48047a77dd32a532595a97eb9f2ab9748384bc",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/initial/9389c70bd6e7e5742b2061bbc518ac7085e7ca34e866b7cb511e733d93aa6107/20261020T002015-86347e943d4c43d698b3ecd87f7665fb/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.blend",
      "sha256": "9cae0bc0bb6001055496bd57bdc1c0c51cf56c8737a184ed916c3152b9431362",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/initial/9389c70bd6e7e5742b2061bbc518ac7085e7ca34e866b7cb511e733d93aa6107/20261020T002015-86347e943d4c43d698b3ecd87f7665fb/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.glb",
      "sha256": "25955dc3240d9efa93eade8d3d345b8f7dfb8f3a6038ae4dea223d8b5c4a471b",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/initial/9389c70bd6e7e5742b2061bbc518ac7085e7ca34e866b7cb511e733d93aa6107/20261020T002015-86347e943d4c43d698b3ecd87f7665fb/request.json",
      "sha256": "f5f8ca81f45f21bb906f3d2eab28200c00b4aaf5fdf7600edd8032df867f9ca6",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/initial/9389c70bd6e7e5742b2061bbc518ac7085e7ca34e866b7cb511e733d93aa6107/20261020T002015-86347e943d4c43d698b3ecd87f7665fb/result.json",
      "sha256": "cc3ab2a308d17ee2d2af6d9e7e23214ec313306990eec5410e84860abee836a5",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/initial/9389c70bd6e7e5742b2061bbc518ac7085e7ca34e866b7cb511e733d93aa6107/20261020T002015-86347e943d4c43d698b3ecd87f7665fb/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/initial/9389c70bd6e7e5742b2061bbc518ac7085e7ca34e866b7cb511e733d93aa6107/20261020T002015-86347e943d4c43d698b3ecd87f7665fb/stdout.log",
      "sha256": "946c7050fb2d19f5a13cab629b74010f54b1d2e998ecc7fb226417a1a499f03a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/546c22e7bcfb9e5fd41f48bc3b1e5443bc97808340d63e8a5be973eedc5e270a/20261020T002017-eb7a32ae9ce14c2a909d3f00ac2bb0a3/outputs/welded-ignimbrite-outcrop/metadata.json",
      "sha256": "2c839ed95040db71334ee824e8f0d982433d7deb38b8741c5eae5b6a14f98ec4",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/546c22e7bcfb9e5fd41f48bc3b1e5443bc97808340d63e8a5be973eedc5e270a/20261020T002017-eb7a32ae9ce14c2a909d3f00ac2bb0a3/outputs/welded-ignimbrite-outcrop/qa.json",
      "sha256": "8c6f66937c60415b8e9ecab0340aa65be0e34260d560fa261823904ff87d99de",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/546c22e7bcfb9e5fd41f48bc3b1e5443bc97808340d63e8a5be973eedc5e270a/20261020T002017-eb7a32ae9ce14c2a909d3f00ac2bb0a3/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.blend",
      "sha256": "f929a78fd9de33d2a65d8177288ac5b6749dd7aedcb73314254373347b98daf0",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/546c22e7bcfb9e5fd41f48bc3b1e5443bc97808340d63e8a5be973eedc5e270a/20261020T002017-eb7a32ae9ce14c2a909d3f00ac2bb0a3/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.glb",
      "sha256": "25955dc3240d9efa93eade8d3d345b8f7dfb8f3a6038ae4dea223d8b5c4a471b",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/546c22e7bcfb9e5fd41f48bc3b1e5443bc97808340d63e8a5be973eedc5e270a/20261020T002017-eb7a32ae9ce14c2a909d3f00ac2bb0a3/request.json",
      "sha256": "91afbb549fbe07ac1d0463b9afff5193ee76762dd472fb3549381270d969e731",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/546c22e7bcfb9e5fd41f48bc3b1e5443bc97808340d63e8a5be973eedc5e270a/20261020T002017-eb7a32ae9ce14c2a909d3f00ac2bb0a3/result.json",
      "sha256": "0c9a4f4ae6af9c72e82ec48ff3a5178cdef5637e796d1d545dc4e2af8cb1f1a2",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/546c22e7bcfb9e5fd41f48bc3b1e5443bc97808340d63e8a5be973eedc5e270a/20261020T002017-eb7a32ae9ce14c2a909d3f00ac2bb0a3/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/546c22e7bcfb9e5fd41f48bc3b1e5443bc97808340d63e8a5be973eedc5e270a/20261020T002017-eb7a32ae9ce14c2a909d3f00ac2bb0a3/stdout.log",
      "sha256": "5a5b75afe9b5f12ecbdf1e6fdf2f3fb665a47b12eded99d018d225d4a509d560",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/46ecdf0453d966f0957b78c121a7d3de138497875a83b0f2fc3b95aa91a85b4b/20261020T002019-a5ce8cf3c6f44deeb149d3eebd561afa/outputs/welded-ignimbrite-outcrop/metadata.json",
      "sha256": "6dab71fa6941e622f8c86a5480f9d4a530da475c98a5c540f976859a7db02f00",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/46ecdf0453d966f0957b78c121a7d3de138497875a83b0f2fc3b95aa91a85b4b/20261020T002019-a5ce8cf3c6f44deeb149d3eebd561afa/outputs/welded-ignimbrite-outcrop/qa.json",
      "sha256": "706ac9d60daacc51d626856c3107bb07cab5fd019b3dd5b137d10f9a4c9abff1",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/46ecdf0453d966f0957b78c121a7d3de138497875a83b0f2fc3b95aa91a85b4b/20261020T002019-a5ce8cf3c6f44deeb149d3eebd561afa/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.blend",
      "sha256": "798f22caf58cddc7f7f1d0a48ad40183ec820df7b9e591fa6f7943f64d32b6ad",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/46ecdf0453d966f0957b78c121a7d3de138497875a83b0f2fc3b95aa91a85b4b/20261020T002019-a5ce8cf3c6f44deeb149d3eebd561afa/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.glb",
      "sha256": "25955dc3240d9efa93eade8d3d345b8f7dfb8f3a6038ae4dea223d8b5c4a471b",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/46ecdf0453d966f0957b78c121a7d3de138497875a83b0f2fc3b95aa91a85b4b/20261020T002019-a5ce8cf3c6f44deeb149d3eebd561afa/request.json",
      "sha256": "c7fb212dc02156394094046e40eb3232007de6751c4cf74866f5839b5b69c7cb",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/46ecdf0453d966f0957b78c121a7d3de138497875a83b0f2fc3b95aa91a85b4b/20261020T002019-a5ce8cf3c6f44deeb149d3eebd561afa/result.json",
      "sha256": "b80d89628621d807408377a84511ea05c7b7f08dc342635ad7625ae89b4f6419",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/46ecdf0453d966f0957b78c121a7d3de138497875a83b0f2fc3b95aa91a85b4b/20261020T002019-a5ce8cf3c6f44deeb149d3eebd561afa/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/46ecdf0453d966f0957b78c121a7d3de138497875a83b0f2fc3b95aa91a85b4b/20261020T002019-a5ce8cf3c6f44deeb149d3eebd561afa/stdout.log",
      "sha256": "52204cbc708b61fbabd96e5b49831d51b478cf86e9c1da53e77a8857ac476ff8",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/runs/20261020T002014-db63f157a213430780e536b46df75916/manifest.json",
      "sha256": "3090afb3c15c5061a29ef6cfc3391a8fea64c57cb0f245f369e1e8fc83d62b6b",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runs/runs/20261020T002014-db63f157a213430780e536b46df75916/summary.json",
      "sha256": "de9980df171bfe486f13ee668218860b2f97315959bf98fa34503d57f18193a1",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runtime/front.png",
      "sha256": "1325dd58c855a892014d275bd647e473a00713fa5863775df111326043e37c1b",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runtime/hero.png",
      "sha256": "c3a282e77b1ef3c8291a9d6cb8bd1c750d0f5967355a22ff051b649b9648d9a1",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runtime/reversehero.png",
      "sha256": "1d7d5608d32ffb2f8fb37cfe5e513fa05c35445de1493b5db06d56739770bb0c",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runtime/runtime-report.json",
      "sha256": "dd4497a116e79161491444ad86f7daafedcda4276b6453924adf52f80e9cc33a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runtime/scene-9.png",
      "sha256": "5b0b0a22564b4ad183040504652bb40aa9dc700faf58cad23d9e03011b574295",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runtime/side.png",
      "sha256": "d841fe1203b860e9d734dc741540cffcd688e0ca4703356fbc8bbccb4f658651",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/runtime/top.png",
      "sha256": "2ddffff33108fcfd324402d414a3db4503eadba6c9b400e89f9e004d7d61f0df",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/source-export.report.json",
      "sha256": "fb0c033ee7fd650624d502a26581df3aeeef8c1c64b5a3264b99485b59d6933c",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/source-measurements.json",
      "sha256": "9a64171328180be42ca977038cb987435033216634646016595972c059b7455a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/clay.png",
      "sha256": "e845be4ac6ef5b8001b82ec1e0834071f43b3ccb3a35b13947d4719217b2f873",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/front.png",
      "sha256": "82481dce428d1e2ab6e360764c06790965ee33581c6251c2502d6fdf2ef3a528",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/hero.png",
      "sha256": "b279df19dee2d3dd840ad258c67434ad3fef780e084474d54e5cae32fed11047",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/rear.png",
      "sha256": "c9098ddede2944d8ef736236d624da784332a38c5e9ba3b10c91c83c185098a9",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/render-config.json",
      "sha256": "9262afbe7719cf7342c85d9beb20694848962e0c7540294c17c3b0a7131e61a9",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/render-manifest.json",
      "sha256": "1ef942525e79ab6d85ef23ec8d4080bb7f1b4ed2a133df31e5c74bd70f689871",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/reversehero.png",
      "sha256": "45613d9ccf490da2978679fbbc0f07ee2825651ded4ae6294eaeaad3e12af202",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/side.png",
      "sha256": "f6d2c2bef3dfcb4ced17afe98f5902b33c3e8e9a7bae05826c91d41e0b4a3e34",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/silhouette.png",
      "sha256": "28748e289e2e9a3162c8224b1991cf3d2973799b817e51446cb2e155ff164163",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/top.png",
      "sha256": "061bc2a5b222770a6eb07be99a63679a4f80dbfb649a9faf19c31443dbb24fdc",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/views/turntable.json",
      "sha256": "33a94c43e8fd0bc79844d6c9d3d69f2db542bf64daf03b2020e048bfca0258dc",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/welded-ignimbrite-outcrop.blend",
      "sha256": "9cae0bc0bb6001055496bd57bdc1c0c51cf56c8737a184ed916c3152b9431362",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/prototype-01-overregular-mass/welded-ignimbrite-outcrop.glb",
      "sha256": "25955dc3240d9efa93eade8d3d345b8f7dfb8f3a6038ae4dea223d8b5c4a471b",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/queue.log",
      "sha256": "0446e199c4d9466533343ed0b9f706f654d013b583da9fe08e24cfaec244b919",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/rebuild-1.log",
      "sha256": "dbf77f96c7322317d1891a731fbc47350918b14a2a469e96467b8ec2f0f3a32a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/rebuild-2.log",
      "sha256": "9ff91f500a1ae17634c86efd9acd8e21fe1591a248a87be89d9d289f04d96b63",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/render.log",
      "sha256": "26f3e8828cf91325138b0706720e3da025540f2f10446df51c9445a64e54b908",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/initial/f9f75c0f6e466a5bf558dd3fe1e014dc502e6521f5c5f4099535e92ad1356079/20261020T002119-c9fe04aa491d4880bcea287bf7f066e0/outputs/welded-ignimbrite-outcrop/metadata.json",
      "sha256": "e6e5cbdc59abaf1e4f38e1f605ebda5c8dfdf71daf2912afba005b2757b0a4de",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/initial/f9f75c0f6e466a5bf558dd3fe1e014dc502e6521f5c5f4099535e92ad1356079/20261020T002119-c9fe04aa491d4880bcea287bf7f066e0/outputs/welded-ignimbrite-outcrop/qa.json",
      "sha256": "ddad63b246f8b634c5a3d5a68a1fdb53cec067a444d63ac0f869808258f66192",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/initial/f9f75c0f6e466a5bf558dd3fe1e014dc502e6521f5c5f4099535e92ad1356079/20261020T002119-c9fe04aa491d4880bcea287bf7f066e0/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.blend",
      "sha256": "1e1cdcb3bfd64ed630455fb6b6bcda8f66b83704823a17fb7a0914a0bb3f5357",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/initial/f9f75c0f6e466a5bf558dd3fe1e014dc502e6521f5c5f4099535e92ad1356079/20261020T002119-c9fe04aa491d4880bcea287bf7f066e0/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.glb",
      "sha256": "83b7d4170c8cb51870e2ea643294306e4cc6a62a2386712457cfb887ff0c2704",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/initial/f9f75c0f6e466a5bf558dd3fe1e014dc502e6521f5c5f4099535e92ad1356079/20261020T002119-c9fe04aa491d4880bcea287bf7f066e0/request.json",
      "sha256": "aed3ffa15f3cdeead4657e901172d193f3af2556c1e18a887fa9f8c1acd31efd",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/initial/f9f75c0f6e466a5bf558dd3fe1e014dc502e6521f5c5f4099535e92ad1356079/20261020T002119-c9fe04aa491d4880bcea287bf7f066e0/result.json",
      "sha256": "128f34c36205f8a72ce55f262331361ba4423e78306e4b4578fc12f8a454e209",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/initial/f9f75c0f6e466a5bf558dd3fe1e014dc502e6521f5c5f4099535e92ad1356079/20261020T002119-c9fe04aa491d4880bcea287bf7f066e0/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/initial/f9f75c0f6e466a5bf558dd3fe1e014dc502e6521f5c5f4099535e92ad1356079/20261020T002119-c9fe04aa491d4880bcea287bf7f066e0/stdout.log",
      "sha256": "c331805fc139966cdaef9ea1552dbb4ca6ae35ae0a4efbece44133c5c29b306d",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/da050b0bf7e77cbbfa3cc2ab732179ca40d91473053e012e083ce0299b1b85a3/20261020T002121-80302919269e4fb59c5f91cfdd5d4e9a/outputs/welded-ignimbrite-outcrop/metadata.json",
      "sha256": "0cde9cbfc8a539135163690c5c209eff4d7ac2ec2b44cc8e8ec90744cf11555a",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/da050b0bf7e77cbbfa3cc2ab732179ca40d91473053e012e083ce0299b1b85a3/20261020T002121-80302919269e4fb59c5f91cfdd5d4e9a/outputs/welded-ignimbrite-outcrop/qa.json",
      "sha256": "fe5f15e57be827c0265e852998904562bd70f403f9b332131d4104faed86f195",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/da050b0bf7e77cbbfa3cc2ab732179ca40d91473053e012e083ce0299b1b85a3/20261020T002121-80302919269e4fb59c5f91cfdd5d4e9a/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.blend",
      "sha256": "01c44bc034f4ca1f04161b4f24afe64f46c8b8e217dc490f3d08adcf73de67b6",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/da050b0bf7e77cbbfa3cc2ab732179ca40d91473053e012e083ce0299b1b85a3/20261020T002121-80302919269e4fb59c5f91cfdd5d4e9a/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.glb",
      "sha256": "83b7d4170c8cb51870e2ea643294306e4cc6a62a2386712457cfb887ff0c2704",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/da050b0bf7e77cbbfa3cc2ab732179ca40d91473053e012e083ce0299b1b85a3/20261020T002121-80302919269e4fb59c5f91cfdd5d4e9a/request.json",
      "sha256": "c6456f9232928e22a193048547b13029f34f231077950f9dc0010150e9475fab",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/da050b0bf7e77cbbfa3cc2ab732179ca40d91473053e012e083ce0299b1b85a3/20261020T002121-80302919269e4fb59c5f91cfdd5d4e9a/result.json",
      "sha256": "06f9db26b9b3abbc3e6a17e0308661c895cf904b9314910c1c0b8681e9926fb7",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/da050b0bf7e77cbbfa3cc2ab732179ca40d91473053e012e083ce0299b1b85a3/20261020T002121-80302919269e4fb59c5f91cfdd5d4e9a/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-1/da050b0bf7e77cbbfa3cc2ab732179ca40d91473053e012e083ce0299b1b85a3/20261020T002121-80302919269e4fb59c5f91cfdd5d4e9a/stdout.log",
      "sha256": "47d466bfedeb9e579a39505cc6d365ab18c369199de8dcc890eedc5256b2283f",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/6b4d0de6bb332ebe7dfd206e2373b5ba1758b057323150ad6502ce56c84e2f0a/20261020T002123-45853b1f7db14dedafb6bb4a83b275ae/outputs/welded-ignimbrite-outcrop/metadata.json",
      "sha256": "1545b9df488479cd452a87d6439b8df63dfd31ef7379b6752f09fec164fcc57b",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/6b4d0de6bb332ebe7dfd206e2373b5ba1758b057323150ad6502ce56c84e2f0a/20261020T002123-45853b1f7db14dedafb6bb4a83b275ae/outputs/welded-ignimbrite-outcrop/qa.json",
      "sha256": "fb365e54db4748133d5a10948d7b1f9f55c11259f12f29fc6e4fa40e4f3e8b1c",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/6b4d0de6bb332ebe7dfd206e2373b5ba1758b057323150ad6502ce56c84e2f0a/20261020T002123-45853b1f7db14dedafb6bb4a83b275ae/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.blend",
      "sha256": "155a90169fc11870a12e0700fc51357ce9f78d1e6cf1df9b8ef7180d74aa9fa6",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/6b4d0de6bb332ebe7dfd206e2373b5ba1758b057323150ad6502ce56c84e2f0a/20261020T002123-45853b1f7db14dedafb6bb4a83b275ae/outputs/welded-ignimbrite-outcrop/welded-ignimbrite-outcrop.glb",
      "sha256": "83b7d4170c8cb51870e2ea643294306e4cc6a62a2386712457cfb887ff0c2704",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/6b4d0de6bb332ebe7dfd206e2373b5ba1758b057323150ad6502ce56c84e2f0a/20261020T002123-45853b1f7db14dedafb6bb4a83b275ae/request.json",
      "sha256": "3e943e4c83026d6fa7a1326ebb44aef276fb3f27a125f58af0ba31f9c7daa4e7",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/6b4d0de6bb332ebe7dfd206e2373b5ba1758b057323150ad6502ce56c84e2f0a/20261020T002123-45853b1f7db14dedafb6bb4a83b275ae/result.json",
      "sha256": "7c269eafb9c5e5d86e4983a53b315e8772f4310f6d6fff05e3e936e826e090a7",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/6b4d0de6bb332ebe7dfd206e2373b5ba1758b057323150ad6502ce56c84e2f0a/20261020T002123-45853b1f7db14dedafb6bb4a83b275ae/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/build/welded-ignimbrite-outcrop/r001/rebuild-2/6b4d0de6bb332ebe7dfd206e2373b5ba1758b057323150ad6502ce56c84e2f0a/20261020T002123-45853b1f7db14dedafb6bb4a83b275ae/stdout.log",
      "sha256": "bb0e810fc759877cbb07272b83821bbb1986b6a657f00cec3a3bd41a62aea805",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/runs/20261020T002119-a778812b637546229d4c36cb1d9524cd/manifest.json",
      "sha256": "3090afb3c15c5061a29ef6cfc3391a8fea64c57cb0f245f369e1e8fc83d62b6b",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runs/runs/20261020T002119-a778812b637546229d4c36cb1d9524cd/summary.json",
      "sha256": "78e7b83ee36cf1466c68cbc132b96409bb65ee1224daf9a6554fe926c451d7f4",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/runtime.log",
      "sha256": "914dd3e597207a14c88083912b457599b24fcc60801c007c959662c3693bf7cc",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/source-reopen.log",
      "sha256": "69f093e96e149463a58fd91825d63d6d0f80b2d0ab4fdf133f9a0c4b4e507f20",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/clay.png",
      "sha256": "02ecadc87811e1301d79acec394ffad49c1eb36bc26412011657818834717f86",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/front.png",
      "sha256": "614fef42bcb5f0d587847ba649b46ed1cf454ccb60dc6ce02ab77694fb62f915",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/hero.png",
      "sha256": "14eea102e110ca0ffa65deb5e5ee84a6ce1fe14d54091b1bf901fff2d412b38f",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/rear.png",
      "sha256": "ff28e0b5e99c3bca1a599ebe0e3216f7468bdf3562c14f27314f4655651e1f14",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/render-config.json",
      "sha256": "efc3915cae74a480d36e671aa812588e91d442694f8545f9e7e379b18543a0a3",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/render-manifest.json",
      "sha256": "c78acc4c7ec14f88c10f0c488a2cc82b5ced793a841b483fd279019e5ba48c70",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/reversehero.png",
      "sha256": "8bc6c27cc6b9b75e7a35264fcdd282c983cf16d4b1c873d4c28201fcb81ccde0",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/side.png",
      "sha256": "7277817b63a9cecb118b5b4c9a5487b65db6cc621993e09e97ce0fda2833ad7c",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/silhouette.png",
      "sha256": "79218d83614815b3e49626a49ec9004036aacb8cd894e8ab16a49755a162595b",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/top.png",
      "sha256": "8ebdab5a9d5814e0a2da9c54cdea67e3ee5acc2dc4cb457e1be0aee37c981dc8",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "production/continuous-small-life-round18-20261020/work/batch-53/welded-ignimbrite-outcrop/r001/views-pre-delivery-binding/turntable.json",
      "sha256": "71318dd1276410f57a3ff6e848166b1eaab4f06a16586c9d71da8301eb6b5000",
      "origin": "source",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "qa/continuous-small-life-round18-20261020/batch-53/INDEPENDENT-REVIEW.md",
      "sha256": "495ac88acb3002de206a84dcd383206d7b67c5c7a7da7f4c553fa6f8d45ac2c1",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch53-20261020/capture/render-report.json",
      "sha256": "0143db47a04a3b357d9a03e6814b51a7b897321ee8acc4813c8e3441311e6e02",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch53-20261020/capture/index.json",
      "sha256": "9903a35e0e68a5e0846aa36d14ff43a567ba74375260eae3d75c4d382e57e516",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch53-20261020/capture-integrity-verification.json",
      "sha256": "422d2e33d762e891336adec45b3299e8cdfd3329bf5da7807f30d590ca9984f4",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch53-20261020/capture-projection-audit.json",
      "sha256": "c0d16a5b11635d7fcd848cfd23b8f8d6076cb3c8e5d5ef23470228c9a5feca66",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch53-20261020/capture-independent-review.json",
      "sha256": "c406877c97a32df7da4768916b267704dcb0ef14f6b12ca0f7cbe9e0d3bc2c1d",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch53-20261020/capture/references/hypoturrilites.png",
      "sha256": "0a293440fe77c4be25567736206993d4739b32650d3fdbd39d3ad4942d1d5a7a",
      "origin": "release",
      "owner": "hypoturrilites"
    },
    {
      "path": "qa/batch53-20261020/capture/references/iodes-brownii.png",
      "sha256": "2017638fead71e83e5217dad32d55d19ab721a7375ae64a4ea5171d010a98818",
      "origin": "release",
      "owner": "iodes-brownii"
    },
    {
      "path": "qa/batch53-20261020/capture/references/welded-ignimbrite-outcrop.png",
      "sha256": "f652b5f2db5e8e1a74452cbdb96b569308d9e83c8ee022b0c4cf17a8fa80150d",
      "origin": "release",
      "owner": "welded-ignimbrite-outcrop"
    },
    {
      "path": "qa/batch53-20261020/capture/references/halopoa-furrowed-burrow.png",
      "sha256": "e13289147dfec2b491439bce5edfde7683ae1766ae0008b3dc18a75872a7fbed",
      "origin": "release",
      "owner": "halopoa-furrowed-burrow"
    }
  ],
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  }
};
