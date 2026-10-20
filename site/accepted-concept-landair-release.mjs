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

export const BATCHES5155_RELEASES = [
  {
    "descriptor": {
      "path": "assets/releases/batch51-20261020.json",
      "sha256": "416e953c2c9dab4fe710fe0c9e3cbe39800041f1ecc16f416b401c3a19986367"
    },
    "release": {
      "version": 1,
      "scope": "batch51-20261020",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "user_visual_acceptance": "not_established",
      "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4",
      "review_commit": "2b61ba2f70110f3bd01df45972558bc94f134566",
      "source_bundle": {
        "path": "qa/batch51-release-20261020/source-bundle.json",
        "sha256": "57e18b16919d0063cfebffd6bd359b0b2335e30fb06cb0896c910ede9ba65bd4"
      },
      "source_scope_review": {
        "path": "qa/batches51-55-release-20261020/source-scope-review/review-summary.json",
        "sha256": "a7763a1603657d4d3cacb3030853a6f684a88489b606499d6669e041a2e0df54"
      },
      "capture": {
        "report": {
          "path": "qa/batches51-55-release-20261020/capture/render-report.json",
          "sha256": "ecd07698cef1dab39855e806e8e4e6bbfefb09de2eff16d3104152797fb7edb3"
        },
        "index": {
          "path": "qa/batches51-55-release-20261020/capture/assets/turntables/index.json",
          "sha256": "ae819d5845ed6ddd55e084ca0bec92ea11f9d6f799b626dd5a688f3c482e2d2c"
        },
        "provenance": {
          "path": "qa/batches51-55-release-20261020/capture-provenance.json",
          "sha256": "307baa1e131983ca335e3c44b0df8dbe408d80fa4ebc382134fc00476b1c1e03"
        },
        "independent_review": {
          "path": "qa/batches51-55-release-20261020/capture-review/capture-review.json",
          "sha256": "b1262c2f209724149fbf98799cf502cc186db973fd5269d32ca36e8af9503c09"
        }
      },
      "additions": [
        {
          "id": "dicranurus",
          "revision": "r001",
          "metadata": {
            "path": "assets/additions/dicranurus/batch51-20261020/release-metadata.json",
            "sha256": "1fa4454acc5338a89a31642ecdae50682203664c64c024fcdac734311e9af5de"
          },
          "source_metadata": {
            "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/metadata.json",
            "sha256": "300d2bf2fd13679e872589c45fbc4f3141a11d2179f2e75a3ea15b0cf2712c0c"
          },
          "candidate": {
            "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate.json",
            "sha256": "b7721823ba4b4f5f62bae8582449d2b4bf1333edc14fbfaf37a3efe85c8a533b"
          },
          "artifacts": {
            "glb": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/dicranurus.glb",
              "sha256": "ffe61e0340399eb1bd41cb198ba5abc20edae439db44e3c21d4cf6d9e032bd65",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "source": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/dicranurus.blend",
              "sha256": "a38846c7822b375f763f5ec71a2483261553845d03ade6355e84335929a7b3ab",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "generator": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/generator.py",
              "sha256": "d844d9c6ad4870d31e49821f387b6f266e5559b00669287734c3ad8d4c3811bc",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "config": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/build-config.json",
              "sha256": "fa5c836f1e391a0269c1504a77e25acc80daada4f76a2e16b4553828caccf4a8",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "references": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/references.json",
              "sha256": "c6b75ad597c5228bbaa49d34f6ca5bdf61f89667db7f50b468454c6308df4e69",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "brief": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-brief.json",
              "sha256": "08212f4648bcd1dee2fcfaf484d313810d5f06cc08305205d1a84c3de0f6f5a0",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            }
          },
          "packaging_candidate": null,
          "packaging_brief": null,
          "poster": {
            "id": "dicranurus",
            "path": "assets/card-previews/dicranurus-v2-768-q90.webp",
            "sha256": "7c77acdba4580d92598699ab1d5cd12eb84041dd8288ad0e52bfcbcdc2d03e0e",
            "bytes": 14298,
            "width": 768,
            "height": 768,
            "source_glb_sha256": "ffe61e0340399eb1bd41cb198ba5abc20edae439db44e3c21d4cf6d9e032bd65",
            "render_preset_sha256": "2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff"
          },
          "capture_reference": {
            "path": "qa/batches51-55-release-20261020/capture/references/dicranurus.png",
            "sha256": "204f235e3b2f09e9dca5ceb12c913c313fa139ba4c1f79056d5f3705dbd0cc82"
          },
          "review": {
            "path": "qa/batch51-independent-20261019/report.md",
            "sha256": "6a6c00bbb209702694cb8a0153c6b4b13def0ca5f7d566916cdd4ef7123997d9"
          }
        },
        {
          "id": "calcite-raft-deposit",
          "revision": "r002",
          "metadata": {
            "path": "assets/additions/calcite-raft-deposit/batch51-20261020/release-metadata.json",
            "sha256": "824c2cb046afcfff85be0c23b8344db4fdf9142d3d6f12ef57aab79eb9b51659"
          },
          "source_metadata": {
            "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/metadata.json",
            "sha256": "0c20fe5c58c8f679eb54db1fa6aad50b1c4620d3e01b53f5bed9bf43c4b3214c"
          },
          "candidate": {
            "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate.json",
            "sha256": "2e107717536a26a84f262a7be3f9884bd57c8c5b291115b66b8b2442c72f5e9e"
          },
          "artifacts": {
            "glb": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/calcite-raft-deposit.glb",
              "sha256": "fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "source": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/calcite-raft-deposit.blend",
              "sha256": "2a3226cbe8048b49554a40e87d0ac13a8bc7804be0f009d27824a979e42f4392",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "generator": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/generator.py",
              "sha256": "4e194758dfa704516a56ca9ff615c7d4d752a0ed435937375ae60d766bb455e8",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "config": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/build-config.json",
              "sha256": "754964fd808f8a29326bfb5e9f8aa0f68d536396dc464ca91236602fcca2e858",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "references": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/references.json",
              "sha256": "5213a445fa920c25af8cea7a065e0f9f80195adaf6ee93bda455d490582bca19",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "brief": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-brief.json",
              "sha256": "8c44fdec8e9109219fbe9dde0e75aeeb082e77aec9e2f326b2e0493d5bb8c69d",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            }
          },
          "packaging_candidate": null,
          "packaging_brief": null,
          "poster": {
            "id": "calcite-raft-deposit",
            "path": "assets/card-previews/calcite-raft-deposit-v2-768-q90.webp",
            "sha256": "22bd23cdb081f540a0ba6b0a4defcdad729fc649510cd7f887ce911c304f0916",
            "bytes": 8694,
            "width": 768,
            "height": 768,
            "source_glb_sha256": "fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22",
            "render_preset_sha256": "2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff"
          },
          "capture_reference": {
            "path": "qa/batches51-55-release-20261020/capture/references/calcite-raft-deposit.png",
            "sha256": "2e58eb4d64aaf6813d4b38795493f8972ebf3d9d347d571311152e1ed8879144"
          },
          "review": {
            "path": "qa/batch51-independent-20261019/report.md",
            "sha256": "6a6c00bbb209702694cb8a0153c6b4b13def0ca5f7d566916cdd4ef7123997d9"
          }
        },
        {
          "id": "accretionary-lapilli-bed",
          "revision": "r002",
          "metadata": {
            "path": "assets/additions/accretionary-lapilli-bed/batch51-20261020/release-metadata.json",
            "sha256": "c83c45869417e6c4741cbd092e3363824ffc63d60f03114d9c3fae9ee596e00e"
          },
          "source_metadata": {
            "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/metadata.json",
            "sha256": "294dce68de44b5a05aa3ed45fd69ee8d493d8f3eba311f48e8d9e4e9f90d6217"
          },
          "candidate": {
            "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate.json",
            "sha256": "0aed6702dde95c169d0692e606b0212b4f8b0b2fdf5831ce39bf9dcab445a71d"
          },
          "artifacts": {
            "glb": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/accretionary-lapilli-bed.glb",
              "sha256": "61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "source": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/accretionary-lapilli-bed.blend",
              "sha256": "83b58908c86c908b28330bfbf5e8ff034020e186812a41a4f9682e151d387125",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "generator": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/generator.py",
              "sha256": "7128a119466d57120bf2f5635618a510dbecc4b36693d95f113e4709d22bd418",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "config": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/build-config.json",
              "sha256": "03cfc2dfbc7960342a3426d0085f93c32dbb71af5c1cf7e7fd7219b63b39a611",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "references": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/references.json",
              "sha256": "5245b6fb370a20b8622e83f29a289fcf263b8caa60e81ec2a5d1a70aad884465",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "brief": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-brief.json",
              "sha256": "0f3019059ad83b67e7af323ec950437a3f08828aa5c21e2ec6cd82185c5495c5",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            }
          },
          "packaging_candidate": null,
          "packaging_brief": null,
          "poster": {
            "id": "accretionary-lapilli-bed",
            "path": "assets/card-previews/accretionary-lapilli-bed-v2-768-q90.webp",
            "sha256": "0183bde24a5c2e507358e0bf2007e34508a66e1bfda6bd4fb63cfaf4add4b744",
            "bytes": 9218,
            "width": 768,
            "height": 768,
            "source_glb_sha256": "61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3",
            "render_preset_sha256": "2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff"
          },
          "capture_reference": {
            "path": "qa/batches51-55-release-20261020/capture/references/accretionary-lapilli-bed.png",
            "sha256": "80e40df6891a4da13ba1c5972bd0df010cc0af1520b1e4ffee3695f4de9c678e"
          },
          "review": {
            "path": "qa/batch51-independent-20261019/report.md",
            "sha256": "6a6c00bbb209702694cb8a0153c6b4b13def0ca5f7d566916cdd4ef7123997d9"
          }
        },
        {
          "id": "conichnus-conical-burrow",
          "revision": "r001",
          "metadata": {
            "path": "assets/additions/conichnus-conical-burrow/batch51-20261020/release-metadata.json",
            "sha256": "479207cc7b53866bae5f5495e03bc57cea15c8b9e689446843a28262207d88f9"
          },
          "source_metadata": {
            "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/metadata.json",
            "sha256": "99fadb070a377f891fc1265bfd6902082e35a8f9e8c0e355da0ac555ef2f10ce"
          },
          "candidate": {
            "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate.json",
            "sha256": "fb7c9aa45fc7a0ae9fabb3eb45463935a890d8d64efca787aca1a27eef72fa37"
          },
          "artifacts": {
            "glb": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/conichnus-conical-burrow.glb",
              "sha256": "34948b0738264195544dd24ff377a1b0f3b92a93a1e34ab07d66647235388042",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "source": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/conichnus-conical-burrow.blend",
              "sha256": "4bb156af41158e9c2c899e0b55efdb0cb0e005ddf83cb7af46841e876388d121",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "generator": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/generator.py",
              "sha256": "7128a119466d57120bf2f5635618a510dbecc4b36693d95f113e4709d22bd418",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "config": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/build-config.json",
              "sha256": "ac67eb8c2ad7b7b406bd155250d071115084b5a693a2efb95c24bb1580a34ce1",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "references": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/references.json",
              "sha256": "730d3eb206ee0033122a50a8beae6a7289463e82b013f6fa914610608f69f160",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            },
            "brief": {
              "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-brief.json",
              "sha256": "df27fbe9dc29d10c09d1a763737b81353a0b98c00cd0a6ba1075dc0580f89fa2",
              "source_commit": "9000874083b6a6fb8e4e83dc95e4915801eecff4"
            }
          },
          "packaging_candidate": null,
          "packaging_brief": null,
          "poster": {
            "id": "conichnus-conical-burrow",
            "path": "assets/card-previews/conichnus-conical-burrow-v2-768-q90.webp",
            "sha256": "5a96178925499b5ad1c937bafdf49c352d5e62efa18706a4511a08f97d35dec2",
            "bytes": 9432,
            "width": 768,
            "height": 768,
            "source_glb_sha256": "34948b0738264195544dd24ff377a1b0f3b92a93a1e34ab07d66647235388042",
            "render_preset_sha256": "2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff"
          },
          "capture_reference": {
            "path": "qa/batches51-55-release-20261020/capture/references/conichnus-conical-burrow.png",
            "sha256": "f7ccc38bbc4429f91de72a35ee6e6fd2936840a4ad2b8bf603c4efa918149d03"
          },
          "review": {
            "path": "qa/batch51-independent-20261019/report.md",
            "sha256": "6a6c00bbb209702694cb8a0153c6b4b13def0ca5f7d566916cdd4ef7123997d9"
          }
        }
      ],
      "supplemental_review_commit": "2b61ba2f70110f3bd01df45972558bc94f134566",
      "original_model_review_commit": "925ff855ad0fcc3635cfc44a457101344ffddbde",
      "files": [
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/accretionary-lapilli-bed.blend",
          "sha256": "6b20b7718d321eba2c61f241cdda0acd10c3bcbd17a91b01e121380967ca0be5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/accretionary-lapilli-bed.glb",
          "sha256": "b25ee4fd368d42ce142bd05659d4b3d7b6eb75b3f54d899f8506e5e726d43f36",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/brief.json",
          "sha256": "17d6c03fb129ec692a85dbbbb89777c3df1eacfeeca0de95799d817d622c979e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/build-config.json",
          "sha256": "18cc89fc9064efffb0dc8f32717cf71afeb980636948856583220d4831b973ff",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/concept-brief.md",
          "sha256": "a0484379323f6acadb76be4358ef708d67643863c37bb2f3330478508448a79c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/concepts/generation-record.json",
          "sha256": "0d8ddb7ddf2b0487a5fa69af935d20ca15277f14c7962df495e217b3df749fc8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/concepts/inspection.json",
          "sha256": "3aabea9ef6bd81709fdc9ab2399ee207875ea75180dda31715bef078ea972a45",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/concepts/original.png",
          "sha256": "0a71d024dd5550445c94a54204b3cdcce3e8ef8d9ce2d541ff7c4c325b2ad5e7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/concepts/prompt.txt",
          "sha256": "bf17fc74b41b04dfe0a51670f4efed0bcbf1543418039e7d5b614de4fa3cc801",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/derived-freeze.json",
          "sha256": "772f3d43eecb5d08ba34029da846fc74710d86623496469b201af7d20d9332ed",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/export-qa.json",
          "sha256": "7c9ad90f4b67576b79d0f32c149527ef9200f2264b82bccb3bf6d9e6a2291e68",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/generator.py",
          "sha256": "4e194758dfa704516a56ca9ff615c7d4d752a0ed435937375ae60d766bb455e8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/gltf-validator.report.json",
          "sha256": "90b446ea6c1a277de85e1e3ff8bcfc04e8e9d8d992268c2eb6436861f4f0433b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/khronos.stdout.txt",
          "sha256": "1ac003aa8e9a423cfade67b3a8a98404c11f576916b80952af294f7d64f0af5e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/metadata.json",
          "sha256": "2d809b017c6e168a3b507cc526a189961521cce9841ba330e2c06afa05513533",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/model-start.json",
          "sha256": "9561d4f8c483a26fce989ded646340859510007a7a7e0f31c16f0d5964dd933c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof-render.stdout.txt",
          "sha256": "f887ecc909cb77fc2315e819df5107311eb2abf338fb152e0d4778bac1e2504a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/clay.png",
          "sha256": "b6f5ae360db9ce256882748adb9536ecf4f0cdd7f4c4b9074bee1710793ac0b8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/front.png",
          "sha256": "11aed196bfe6bbd3773eb3499849bd29691d7380fc1ef166d1b3c0f0cab70d32",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/hero.png",
          "sha256": "f1e273cf02de791ee7c8adc1e1efd1ab3db97617201a8f16f0e93b6538356c08",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/rear.png",
          "sha256": "1e7b105e12bb8943ea14d2164e9305c87db7a75cda1fd6aef811be44c96c63aa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/render-config.json",
          "sha256": "31a1f61df6784dd89e4461942c121fe145810c7beef95321acfdbd0fc68df8d4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/render-manifest.json",
          "sha256": "27e830e02d43f9d447f430d42c6978e1214934c190361eb815738ec8dc271d5c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/reversehero.png",
          "sha256": "9ec7619d48a2baa4b814e16872fc99228e942a5feb76c0879061b4b36eb9d4d4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/side.png",
          "sha256": "1aed42791e688e1c5c411090354f8442de80454a67493c8972f02d7c9b99aec0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/silhouette.png",
          "sha256": "3db3bbb9e9b943547b133fc52504eafcca631726efe1ec1dbffc664166a4d44f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/top.png",
          "sha256": "084c120bb1b817c84a205a4fadaede960bcd61ffd6e79a9dfc60f8c2e7e52cfc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/proof/turntable.json",
          "sha256": "6550fd74bd997802bb2dfcead435d64fb5096a1b9af2613377d03dd62096f621",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/qa.json",
          "sha256": "20f2b9fd509923adf6c5a6a6d6c28f307c60d278bded52757576e534f501e0a8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/rebuild-1.report.json",
          "sha256": "9a73f1f8b9f68a36bf26bd9e076c3c6db7e571b3de679e0762beef7143bb52e6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/rebuild-1.stdout.txt",
          "sha256": "9a73f1f8b9f68a36bf26bd9e076c3c6db7e571b3de679e0762beef7143bb52e6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/rebuild-2.report.json",
          "sha256": "857e1de83801d9e4d71bb63ea0a353813c39283da78c811b2507a38085760ba2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/rebuild-2.stdout.txt",
          "sha256": "857e1de83801d9e4d71bb63ea0a353813c39283da78c811b2507a38085760ba2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/rebuilds.stdout.txt",
          "sha256": "dcdcca7cb92f9995178806bbb753e6656376417262fe69575183feb57a36e566",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/references.json",
          "sha256": "5245b6fb370a20b8622e83f29a289fcf263b8caa60e81ec2a5d1a70aad884465",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/runtime/front.png",
          "sha256": "600ffcfcb049fd0b81835d82366922b442f18e327b0256ee492bfb9debabe47f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/runtime/hero.png",
          "sha256": "c6bbfbc821e7b841354cff3edf98b9fea340ea8006cd0dacc029da805eead58f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/runtime/near.png",
          "sha256": "8264e14fe1989f2f95281d9bd55427166ae2b24ecd1e8cbaf60b43483b04815f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/runtime/reversehero.png",
          "sha256": "4135abfe4764f2d771291b67d7e4ccd313541f658731800e27f5e3d4a8975ad0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/runtime/runtime-report.json",
          "sha256": "81c287ac86028f8841096057c7ab2374b69e894ee97cce9bd91e0ce712f051e1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/runtime/scene-9-copies.png",
          "sha256": "2481b31d1d5e3395b4cb9a53149a9ac089607454c664151094e79ba52f53f394",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/runtime/side.png",
          "sha256": "88829c5b8c535d060f73f1dc650646c5108b3b28fbd168ee081c71647ee6abb9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/runtime/top.png",
          "sha256": "3219d34f45403eff20f9a18d0ee0916ce0b4da800cdeb2aa02b34bea8daff074",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/source-export.report.json",
          "sha256": "00da6144a38fc05b0728b235cb994a80cf2d556feb73daf5656bdfd61b463f74",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r001/source-reopen.stdout.txt",
          "sha256": "aa0f3343472031de83cff1770e6f58abf1f04a32ae8480fdbcb2a9d677868617",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/accretionary-lapilli-bed.blend",
          "sha256": "83b58908c86c908b28330bfbf5e8ff034020e186812a41a4f9682e151d387125",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/accretionary-lapilli-bed.glb",
          "sha256": "61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/brief.json",
          "sha256": "1997290d983b25b1938575ca69791078148cc2743324a1e9885ad643ff67ec7d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/build-config.json",
          "sha256": "03cfc2dfbc7960342a3426d0085f93c32dbb71af5c1cf7e7fd7219b63b39a611",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/bundle-files.sha256",
          "sha256": "589f93008492d55b97236d6ba105acad14674b6f29e9fc57f703f3fb23b3930a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-brief.json",
          "sha256": "0f3019059ad83b67e7af323ec950437a3f08828aa5c21e2ec6cd82185c5495c5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-freeze.json",
          "sha256": "77fb11831e8adf3994487a62de4d580f41ac5330f6b66c3aa2746d1c8f5fc000",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-integrity.json",
          "sha256": "86552351278aae2771ebfc8c06b0a4adfed6e74952adfa80f81ba04b95a935c7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-integrity.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/clay.png",
          "sha256": "e596f455fbf4986b5cd7175205e8f50356e418949379f4902e23ba9c16639a7e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/front.png",
          "sha256": "02289900c4b919b7e57f2966a6e7f33da34cb8e87a4f090baf7fc87c6114820c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/hero.png",
          "sha256": "d8d3931769a2c9da98d0c46531d7d53f1904f45f6f1ffbf8cd82d44caa288062",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/rear.png",
          "sha256": "1d8cce4576fccc3127f74611db685f9a58371379661b8c2c1a21e8337079edb7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/render-config.json",
          "sha256": "d5783d7600a026b6e08e562e7cf67553a997e46176a2408480f573f4d4f92b3b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/render-manifest.json",
          "sha256": "94e474d4e0a2d93056c17284d2c7fc3ada08e1317d7f9c797165f640ced71a4e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/reversehero.png",
          "sha256": "5d514f4e12492e711a51c464ec986bc908553137ebef0f6d57fe9e0bb7ab25dd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/side.png",
          "sha256": "f101f30800bef6acd165667fcab318b831153f85deb51ecd34bc096cdd0a8260",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/silhouette.png",
          "sha256": "6d7c5977a82c25c8b3ffb3035479b60089f0e19a3455b5deed7a5ba129d46b85",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/top.png",
          "sha256": "81dfd05cd85294c11a31b0ccc191ace5dcb872faeef5856f1dd1643a266859e3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-proof/turntable.json",
          "sha256": "2d5d672ec1b03f3e7dfc646fb32ee9fb9faa7cd8aefee9cb5ffd51f9b59df691",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate-render.stdout.txt",
          "sha256": "7194a771ab34bd77a3f41307b490754e9c91de7920ecd4ab91ee020d1401ab99",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/candidate.json",
          "sha256": "0aed6702dde95c169d0692e606b0212b4f8b0b2fdf5831ce39bf9dcab445a71d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/checker-exits.json",
          "sha256": "e8efe55b90b8ae143931eca13f6d961b455bb4bc06d937339afa306d3ea046c0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/concept-brief.md",
          "sha256": "c6805fa20c4229cd5a872e5558bcce2f7c35f0779bbe45b6d794dfb92722de06",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/concept-completeness.json",
          "sha256": "dd10cfc0ed5147ed7db06de7c4dafb43d23c6f0ef07921e2849ab4fa86ffaca5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/concept-completeness.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/concept-evidence.json",
          "sha256": "a64fb310c4ec35b92133b8670c1a87dca24273c089ce56644016c4f1ef42e63d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/concepts/generation-record.json",
          "sha256": "0d8ddb7ddf2b0487a5fa69af935d20ca15277f14c7962df495e217b3df749fc8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/concepts/inspection.json",
          "sha256": "3aabea9ef6bd81709fdc9ab2399ee207875ea75180dda31715bef078ea972a45",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/concepts/original.png",
          "sha256": "0a71d024dd5550445c94a54204b3cdcce3e8ef8d9ce2d541ff7c4c325b2ad5e7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/concepts/prompt.txt",
          "sha256": "bf17fc74b41b04dfe0a51670f4efed0bcbf1543418039e7d5b614de4fa3cc801",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/dependency-pins.json",
          "sha256": "350ba7f010997a62d4f449f75b911ca3e488e2ee030cb5ca0f61db1cf55e8f7b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/derived-freeze.json",
          "sha256": "b8ecd73e403b75d335057d5eb9379452b2b60d3039b65834cda2bc8c129e8c35",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/export-qa.json",
          "sha256": "6a4a7d7c7cc0ddf837b74d24ad322b062cc2f405460e3bc22fa0fdcee22d351a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/factual.report.json",
          "sha256": "c8b877942e22e7da799428bce2bd30f5d0401ac772e5e72664c52b899b2fa51a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/final-inspection.json",
          "sha256": "d6505ffd3da7dba611ab9b5c5d3b29635b2b5191487b5826891978cb5aa11c8e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/generator.py",
          "sha256": "7128a119466d57120bf2f5635618a510dbecc4b36693d95f113e4709d22bd418",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/gltf-validator.report.json",
          "sha256": "72659b35238deb698a991585f2846c82ff5936a9b861522666053bcd99bafe4b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/gpu.report.json",
          "sha256": "5a6c7a660e13b632fc2f8021380c76c28269e8d350a444413fa4ffb5d702d73c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/khronos.stdout.txt",
          "sha256": "514def9c8642d98dd4c9da3911e930a21aa06c64666fafce29ddfd3872199226",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/maker-review.md",
          "sha256": "93cb0fcfe02da9f1d496ba9e2becc92c6b0506d5a33ec81a358139d5b983c10d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/metadata.json",
          "sha256": "294dce68de44b5a05aa3ed45fd69ee8d493d8f3eba311f48e8d9e4e9f90d6217",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/model-start.json",
          "sha256": "40186e29b310809f66dc826f8d0417ae2ed80ed0f7ea726e63226c13ca1623b3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/profile-contract.json",
          "sha256": "03b8c1cce94cd65f77c7c2815ec20a549ff8d0a2b6d33eb6e8537367818997be",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof-inspection-identity.json",
          "sha256": "5b1b45a0b00498744d7c88ea5b28eb10c799ac30db7e5b0a4bd0a25d92198a2e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof-render.stdout.txt",
          "sha256": "4ef5f8239722dc1a90b379727c92a0b8d7cec54654fe07843aa5412f3a438e62",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/clay.png",
          "sha256": "aab2c8a0f2509cb26bc06dd87ee515183116be0d3cbf554c400157bccbb1ccbe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/front.png",
          "sha256": "d10e0d0a40efed893b50c2feb3b3497df3746e2b2319c53d7ff0d6a3106da553",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/hero.png",
          "sha256": "515c15649c96d832a9e6a4e250d5b5d3beac4859fa764fa7cd0348f02ecc355e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/rear.png",
          "sha256": "52ef8270e0efec5df884ff23e69fcdc48185a95076f8aced0ff9777fb6d444a0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/render-config.json",
          "sha256": "e49351dc32369f4dd493d31eb31a61b1fd4193ac3bdfcb1f05b44574d337b700",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/render-manifest.json",
          "sha256": "cee9d6eb77650427bd82ea37fbc9cca203b33b56d5cc0225561ae34d472e351d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/reversehero.png",
          "sha256": "5971ba56cff8389ee7abf14053a0c167e5b7305273c9669acc7e22439cd733b8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/side.png",
          "sha256": "197fea9fa2ff8910335c066fd972ad1ce9c5187d7485dec0b5ff8ab0fbe330a8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/silhouette.png",
          "sha256": "2bd96116870326cff47b237901788396123dd074632f5989058726c24040611a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/top.png",
          "sha256": "9bc31d4ea93994bbdd11e806ccf339d41027b078109395c71d6f34a7a3ea9336",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/proof/turntable.json",
          "sha256": "3bf2f145acb3743a59d5fc09fbfc92c3e27e8a77129e6d8f8a151e726d75d8c0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/qa.json",
          "sha256": "cff73b18a7e146a5dd263c52bcc2a6c105996a2e11dff281bebb7208dc208e02",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/rebuild-1.report.json",
          "sha256": "3816c93a8820f97657469e6b98b5f8c3ceec14635f5dfdb42e1e1c135057f5eb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/rebuild-1.stdout.txt",
          "sha256": "3816c93a8820f97657469e6b98b5f8c3ceec14635f5dfdb42e1e1c135057f5eb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/rebuild-2.report.json",
          "sha256": "b397271b73b25d0cba69ae80cdd47efa07e831ad09d66c394eb56fd7b7951330",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/rebuild-2.stdout.txt",
          "sha256": "b397271b73b25d0cba69ae80cdd47efa07e831ad09d66c394eb56fd7b7951330",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/rebuilds.stdout.txt",
          "sha256": "e9ad5afca93a28e884dfc120d805fcb78264fea4e4f4ebb35dbbe54228a9a56f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/references.json",
          "sha256": "5245b6fb370a20b8622e83f29a289fcf263b8caa60e81ec2a5d1a70aad884465",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime/front.png",
          "sha256": "abbe8a2c0603e291651b3aae31479bc1a5d4201ea1769ced6ddb2b56622bc5a8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime/hero.png",
          "sha256": "be33f0366e3ff62883db76c5751e87e13f826b63bd69e02fac54f27d062d4a4e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime/maker-inspection.json",
          "sha256": "6004fe73b6e432811a151c3589186221c53ce4bb503685e1c31b227194ca8919",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime/near.png",
          "sha256": "011ebdc311bb30607894caf1368a407c5789d59ea8e2419d937d88f113397fa8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime/reversehero.png",
          "sha256": "1e4e0f6684f93b475819b62eab6e8d7cdd837388ae20cefb9d2f70db48d0e7e1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime/runtime-report.json",
          "sha256": "bd69f0dee28d0dfef3e867a72f8288d05d8eb6500e415cc5bda8e37c7f3d3d2c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime/scene-9-copies.png",
          "sha256": "c75da5459b4f9e04f4127d6adf06ad7a71148de1cd50b5872593f540a70c99fe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime/side.png",
          "sha256": "d836c32135fa835604c94b733b13dd53bf4601f9eb62139991275099d5166262",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime/top.png",
          "sha256": "9b2f2e82028c7f09d932128948f83d69b8c0312cc18ccc361125d20164ecde29",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/runtime_parse.report.json",
          "sha256": "9c12a6dc0d559d6f08e8f92f507393494aa43b33a036db88de0fffaee98049d3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/scene.report.json",
          "sha256": "fdce6f83e08ec62bb0c4eca5c34955d9b670030955cf0d6672a9f81ad9d62923",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/source-export.report.json",
          "sha256": "b86015291bbf846273d218f1c514d83f57680f85aaf097cc56fb43244bab6b76",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/source-metrics.json",
          "sha256": "e93c3748d2d61ea055569da9c349aabec19ca03be2bcee76e4f041cb468b3ed0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/source-reopen.stdout.txt",
          "sha256": "14ce56967a5fb11c3cab13e9187b6ddb8c8a6c3faf63a55b9c0dd2d88e79794a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/specification.report.json",
          "sha256": "f94a177118db0456c6ece19e800b82b78e36d5d696c912467a10ba92c021567f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/static-glb.report.json",
          "sha256": "84f3bafdf4efbd4b9b095a7b26cc31ef323c471956ac4ea21a573a5afeade437",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/technical.report.json",
          "sha256": "9f6cf39248e6f055449942b992e0c39ff04c137103798fe8c4f22f7f5a4b7920",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/accretionary-lapilli-bed/r002/visual.report.json",
          "sha256": "e0e97991a18c1bf791ab7bfd17438c79780d6e736a56af54585c4cb9d5dff479",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/brief.json",
          "sha256": "44dbf2ec31d49eb2fcd21cbf9719b0de4d8534df7a7d405f9a5f72e33727c1e9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/build-config.json",
          "sha256": "860f993f301a3cb073525bda3159d833ab7748f8db49b35095a83953b607ce26",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/calcite-raft-deposit.blend",
          "sha256": "95c0634588527ab71722c29837a3e823efccbfde7b28e93decc8ea93833ce736",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/calcite-raft-deposit.glb",
          "sha256": "5620215ee6b745c7fff7a393ce2d48f164f6914ed48027cbf3bddc54aa5ab336",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/concept-brief.md",
          "sha256": "471074359c19ee5412c8b9f0218d82107836f34250a55533df9b5dfce19ceaea",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/concepts/generation-record.json",
          "sha256": "701885e9a932cc4c113d85c810f3ce5b96532447bdbd4012cd2b93b828226e5f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/concepts/inspection.json",
          "sha256": "149c5dc6b494ae2f5ab89879e284a5590416caee5f109db91b760deb296f38c6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/concepts/original.png",
          "sha256": "07140bd478b0f36c4e97281d70559f392010bbb6e9f50830da31e07e41368cfa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/concepts/prompt.txt",
          "sha256": "3785718352897fe890639ee618899b68a20be934e1fd9f4354529f3a0583dc68",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/derived-freeze.json",
          "sha256": "c7ca6f6f277456667ec746b37a192e3ff578bdb4da5ad75242bea4958703b10a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/export-qa.json",
          "sha256": "4b025ab6d506ccd47eb1277afb60332622371c7f17a9704df1251c3d6b89063f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/generator.py",
          "sha256": "d844d9c6ad4870d31e49821f387b6f266e5559b00669287734c3ad8d4c3811bc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/gltf-validator.report.json",
          "sha256": "23ce4c2357e2adee761ea35fb7bca0c833441f69c12b84898f6c1ada55ba893b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/khronos.stdout.txt",
          "sha256": "12eaa789bfb156a75a985995c449a8e205b4a06e108861785922065de18ac433",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/metadata.json",
          "sha256": "95ffe63de58172b4a94e5fae7484ca36e781f993038a564619b0a109bfd4c97f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/model-start.json",
          "sha256": "9f8bbf2008e959faf3dbfdfaf357133e70549e27ddf528cacd0d939d728969ff",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof-render.stdout.txt",
          "sha256": "f3137f608ffb5e9b4ec4e8fa45824777d36ed7d1f2b7a5d6a08795dba1157280",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/clay.png",
          "sha256": "fdbd0807b6804814421f094722e3bd574eca0a5ccfd251a8dcbbcff1a8c501fa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/front.png",
          "sha256": "135b8f1ee704017ba5e69e0bf5d606b618738b42ba75f2d4ef04e3247ec36ebb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/hero.png",
          "sha256": "3c24503e12cc3ea8d7aa86bf54f86db2cb0ffd09aa1775d566f58cd47ec91934",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/rear.png",
          "sha256": "90985bd61f7becdedb93481e2dac0aab798ef1fe0b2e6bd5624ad110e0c9eef0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/render-config.json",
          "sha256": "4aa31c2fafa5a45ac4a94584f683fe6ecda649e0d188def575760a4d4af0db06",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/render-manifest.json",
          "sha256": "91d692cb4eeb3364bd4c861f158a8869c8df9c11edd791e15313d5efd83640e5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/reversehero.png",
          "sha256": "083c6321e0999238886ab03bf18a32f7a36f2e70b24e98eb485ebedfad9f209c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/side.png",
          "sha256": "3eeb36489ceb42ee63e263873b2091360d37bb22be193f3b8d729ce090ecaf3b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/silhouette.png",
          "sha256": "979362e0ead27576cd5f040494aed9447cc3549d68e66a99e9ff6ebdbc5c429e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/top.png",
          "sha256": "1a3b2e816aba96f03663af91bf47b06a48fe653dbcaf0a5cd3739b9d8295af40",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/proof/turntable.json",
          "sha256": "c6d1a35d55852f36bb24a5e1efdd127a05f4bc6f14701e5d392edb0d928fb4dc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/qa.json",
          "sha256": "9d1acf851953c18f23f85f0dcce999f6b70d4fb4517f92321e33e68607fadca6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/rebuild-1.report.json",
          "sha256": "8621229144fadc7c82c1daa5eb3c8ca4670051ea150fd8d96a5dcc0a8bf88e69",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/rebuild-1.stdout.txt",
          "sha256": "8621229144fadc7c82c1daa5eb3c8ca4670051ea150fd8d96a5dcc0a8bf88e69",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/rebuild-2.report.json",
          "sha256": "1a2d580bed99f5cf88c369d981fcd6b3ca98e99f3450f8d07cf3ac6f982b5e8c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/rebuild-2.stdout.txt",
          "sha256": "1a2d580bed99f5cf88c369d981fcd6b3ca98e99f3450f8d07cf3ac6f982b5e8c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/rebuilds.stdout.txt",
          "sha256": "a27a87a30bb9f82e46927af1113b4aea031edad2ffdab2e7ac24333158bdd9a2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/references.json",
          "sha256": "5213a445fa920c25af8cea7a065e0f9f80195adaf6ee93bda455d490582bca19",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/runtime/front.png",
          "sha256": "6ef32f18337f4e26ee2a83fe5f9fa7df0bfc3658f6496ddf11a0ed458834e1dd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/runtime/hero.png",
          "sha256": "29d133a11342c92545c8c407d1af37b4217f1ae6b6a00c0c4b6034e14f129e2f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/runtime/near.png",
          "sha256": "503c6f2b4acd0cd2223a5e19810a72f311c1a3164951d6acec94be8fa401fcc7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/runtime/reversehero.png",
          "sha256": "c7ef786c350d5ad406c3871cc27c8627750dfc77aed361c9bc41046f3d6dd3fe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/runtime/runtime-report.json",
          "sha256": "67adb2df6580d67ee8a5ba1a29e24d8caa7a1df6fd498b90babec8b9a4e740fe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/runtime/scene-9-copies.png",
          "sha256": "5987c300c44a3a9d5fdeba8cea6c9718c15eb8afb8bfa967e0962df56d148c99",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/runtime/side.png",
          "sha256": "d1d94f56e6391398346d5146bbd0504ae418fbd3c7b78b0b45ac42a8335954f4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/runtime/top.png",
          "sha256": "70cd4256166837c4a9384ec04b673ef34c7d654e86d3e2ea51980b91bc3eee0c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/source-export.report.json",
          "sha256": "667441c943a6be5cbb8248a798531169fc817170885ec6531db4a8032e16f0b8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r001/source-reopen.stdout.txt",
          "sha256": "447255aed777d9b76f098c5715729e14b6de1303d7235e8ca0881fcf669b37a3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/brief.json",
          "sha256": "6473983ac984d9aff316bba880fbf36741a7a9741e5a556e0e96ad5c70324c82",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/build-config.json",
          "sha256": "754964fd808f8a29326bfb5e9f8aa0f68d536396dc464ca91236602fcca2e858",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/bundle-files.sha256",
          "sha256": "5b8c8b7a7a164df5489a2b10ce9f6a92b30e24455cc56d594ed6baa15457549e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/calcite-raft-deposit.blend",
          "sha256": "2a3226cbe8048b49554a40e87d0ac13a8bc7804be0f009d27824a979e42f4392",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/calcite-raft-deposit.glb",
          "sha256": "fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-brief.json",
          "sha256": "8c44fdec8e9109219fbe9dde0e75aeeb082e77aec9e2f326b2e0493d5bb8c69d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-freeze.json",
          "sha256": "7c8baba8dfecea3bb6dbb9eef72584853c5d36db7d68e341e7dbf466255f56c3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-integrity.json",
          "sha256": "042fd00f4faa9b4887fe5ec28f8473e9ad28546298a439f9639fbd7b4529a0be",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-integrity.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/clay.png",
          "sha256": "ffb57ab3a7565e4d1664fba848de56ede527b6587ccb91caccc0f62d9fdcbffc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/front.png",
          "sha256": "dda5dc744e489108eae7130a094a4289f659e1ad5f744f7c7805de34453d4759",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/hero.png",
          "sha256": "792b196b0423b8ff5b27fd33509ad73b58281048270b7e903212270ac1d3d5ae",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/rear.png",
          "sha256": "7a42f7f9646eb33e2207ab8b715a90bfa3aebc06f3b5dbe5c03888ec868f7635",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/render-config.json",
          "sha256": "45165ba09442ca9b93b542e5355b92ee624283f1729f98e06f6817b9cf57396e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/render-manifest.json",
          "sha256": "b02efe2d2a52d018aaa01571fc81e78e35132f501da8e597297ceada1534cf16",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/reversehero.png",
          "sha256": "d95cb59158c4f73044111f00a3b311e93cff277124877a9f18f7690ed00ad1a1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/side.png",
          "sha256": "9655f44f1a999ed485efb0489ec3233f3b2df2435411b32363428a960626ad02",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/silhouette.png",
          "sha256": "f519d7e875008a8933dcc758efdd8c65441249210da133368224887ae895a34c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/top.png",
          "sha256": "78ce012f934e7ff315930bc7d0487b4d8b3a675cef37e8cc10625275925ccf1d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-proof/turntable.json",
          "sha256": "2002e8104cd0181778570c7a7ca1c5e0bffa554c70fadb7613e9cce3235d1c07",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate-render.stdout.txt",
          "sha256": "8500ab463d6ff2dd031cd7330e03ab4d9a1b2eeaf22078eef4b93402cc93e361",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/candidate.json",
          "sha256": "2e107717536a26a84f262a7be3f9884bd57c8c5b291115b66b8b2442c72f5e9e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/checker-exits.json",
          "sha256": "e8efe55b90b8ae143931eca13f6d961b455bb4bc06d937339afa306d3ea046c0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/concept-brief.md",
          "sha256": "32002cbe68490f2ba0acfddfac722364856b655b7c2978e9cbd87e9547883ed2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/concept-completeness.json",
          "sha256": "2e46ed77b38e1c50962fc12734a933e52fbb8cb48c1ea4b5b1da1db03902796f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/concept-completeness.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/concept-evidence.json",
          "sha256": "7fa82963de4b8cdea80cb2e77add133efaa493567f7e3569775698cc53747435",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/concepts/generation-record.json",
          "sha256": "701885e9a932cc4c113d85c810f3ce5b96532447bdbd4012cd2b93b828226e5f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/concepts/inspection.json",
          "sha256": "149c5dc6b494ae2f5ab89879e284a5590416caee5f109db91b760deb296f38c6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/concepts/original.png",
          "sha256": "07140bd478b0f36c4e97281d70559f392010bbb6e9f50830da31e07e41368cfa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/concepts/prompt.txt",
          "sha256": "3785718352897fe890639ee618899b68a20be934e1fd9f4354529f3a0583dc68",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/dependency-pins.json",
          "sha256": "da736d6cabdad8a56cddbb9e788d274d3aaa1b7127b0c3f4edaf37b2f710c04b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/derived-freeze.json",
          "sha256": "1f482f73c81ef19f12a51989f23ee54eaf0314c2c02d67a897c3f84b26e41371",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/export-qa.json",
          "sha256": "89c16cd03dc9e1e0692883f882fde62567faa96e8956654089d39258df266faf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/factual.report.json",
          "sha256": "2f10034764bb61d62aca7734f20c272ca1f62690d9b3a47932450ac7983a7f73",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/final-inspection.json",
          "sha256": "530cd769da4f099bf2e01f11201d9c102d275bd0dcbfeea95beebf6f86c448d1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/generator.py",
          "sha256": "4e194758dfa704516a56ca9ff615c7d4d752a0ed435937375ae60d766bb455e8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/gltf-validator.report.json",
          "sha256": "303a25636a97c32fa94f9955cacce04edfa9f042a2d5e00024ba1d2046dc032f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/gpu.report.json",
          "sha256": "ba7ffc9de348a02c700cd0f4918f65b5bf2a07f16a8b7b19c4c05889e4dc5923",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/khronos.stdout.txt",
          "sha256": "85b69fe5816301a7feb19f221b4ffd4835a21dc4c8cc517f9aa50cf59678d85e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/maker-review.md",
          "sha256": "e69641c6d5cfab0f7274ac68388db85f3f2ce817c059339a39617e74ff768393",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/metadata.json",
          "sha256": "0c20fe5c58c8f679eb54db1fa6aad50b1c4620d3e01b53f5bed9bf43c4b3214c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/model-start.json",
          "sha256": "4b2afbf23331dd30cd0e6585101bea0ec83fedb0a9c4eb5af800b198b49084b4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/profile-contract.json",
          "sha256": "e178fb85318c1b82901582062a6e58e9e4b0662cbd1e9fa53ce54cd136714f3a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof-inspection-identity.json",
          "sha256": "923871d672df51cba322f28318308e07549bc22c3364a5a459b5a02efb48c989",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof-render.stdout.txt",
          "sha256": "10134b93697956ebe9ab1b533c40519f0cbc94b388bc22e1bc76eab7ab1b03a0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/clay.png",
          "sha256": "d7c6707df8707518082b094889b665511cde94dcc483a0daf6c059a525cf7e39",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/front.png",
          "sha256": "ce9027ad21896936a37fbc2507d9716c08823bdd0b2c96f149aaa2bb44dadd8e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/hero.png",
          "sha256": "af57975c765f52aa8efc4d73acc6abcc2b9d3eff825e477e5c5d3aafdf13a077",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/rear.png",
          "sha256": "47aaee84928213cd5c291dba5e5668e42167a9b1b81f4833e7fa7e0531b15447",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/render-config.json",
          "sha256": "42db3a1dca17c84c7cff9e953166d04e27bde34d64c2dc495b19b5b9ca3d365a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/render-manifest.json",
          "sha256": "cfbf05139f174cba644a866929d28d51193563d857c46c4e5f8b6e842faf5839",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/reversehero.png",
          "sha256": "cec8fbfc3720209c7331b08085a23a0b7e493603bbd5bdc8dc6168ae2f9faf2a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/side.png",
          "sha256": "8a00135c94ebfb914790256c5f3ad17b10575cbbad79500aa9aec6620e59514a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/silhouette.png",
          "sha256": "291d1f8187420c1d8fd01a89955d69d1071000be9a60c47307501de62d592111",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/top.png",
          "sha256": "8c5ad2ad9c66c72298f23c7aa38dae03eeed957ffeeae2f60135469fa571f458",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/proof/turntable.json",
          "sha256": "b70196b528d609e5312fa7e9740ab451a9fa02cb7d1aa508940b301d0c84a760",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/qa.json",
          "sha256": "538ecf4a2077efaf207bf97f809f46f48e4836a905bda68e1d66905b2d638400",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/rebuild-1.report.json",
          "sha256": "d01319eab512ba494a6aa3aa2a86cc61f15ef35717daca821d129aa4770d87ab",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/rebuild-1.stdout.txt",
          "sha256": "d01319eab512ba494a6aa3aa2a86cc61f15ef35717daca821d129aa4770d87ab",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/rebuild-2.report.json",
          "sha256": "d2e7cd6d6df4d0cb2d77601a4454eb039699e6f08f25cc25941b87a4a5f44335",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/rebuild-2.stdout.txt",
          "sha256": "d2e7cd6d6df4d0cb2d77601a4454eb039699e6f08f25cc25941b87a4a5f44335",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/rebuilds.stdout.txt",
          "sha256": "407b5ecc691a2c6068659f4383dd38c126c567207d5c9b0e198b1c7aba2e54c8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/references.json",
          "sha256": "5213a445fa920c25af8cea7a065e0f9f80195adaf6ee93bda455d490582bca19",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime/front.png",
          "sha256": "43027fb62f36c0e852bad351f85b26ac7fb2de663bd70063af630104fe03a492",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime/hero.png",
          "sha256": "9ec5cbdedecc095beaa060d9ea8d3fe0095d75f33f5e6f28d9f87729e00ce725",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime/maker-inspection.json",
          "sha256": "f99af4b389c627f8ec864164be80bbfdb83321a2b626076eaaef047db4166283",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime/near.png",
          "sha256": "0bc69491eee23ee6d5bac621ef30bc43f7c4228380ac79788d0e36de74e77d60",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime/reversehero.png",
          "sha256": "5b79c6b434ddf661cad9c7cd90b31103448e79576fefefb8d42716e5de1ea6b3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime/runtime-report.json",
          "sha256": "cfbc794c612866fbe283d910536ba2e72d778e77e9366c3c1774f14f1e893087",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime/scene-9-copies.png",
          "sha256": "0c7bb63aef1ee6fbcfc7fcb1b1f5dc5545423ce7d5e3a34f2db778c1a54f6459",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime/side.png",
          "sha256": "3b612c9c6b2fa84bb819519aac61a0d1747e5df312b245b8e96b528ed792318c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime/top.png",
          "sha256": "d9c0df4feca174234d615e96c192b7f842ddf5f113606ee0c7d3bb580a0414bd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/runtime_parse.report.json",
          "sha256": "6461ec5440848ef353442a5607106d225046670420e7a6f159ed313921a3dcec",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/scene.report.json",
          "sha256": "676c6cf085978b5f324928bd30b310874401cd0bbd018597aaa84eaa39b212f9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/source-export.report.json",
          "sha256": "6a6a564ae4ae25ed8bf8a3adb70781fe4c5ed85fa474d897e194cbc035d6852d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/source-metrics.json",
          "sha256": "06eb25e5cda0f503f5285e5043e24aceda8111cf1b2eadc4fb3fa0bca23efa9b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/source-reopen.stdout.txt",
          "sha256": "1fd336da1b037391c3e396e3fe780f1cb4024f9eafc5eee27ca4d18c7aa7d605",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/specification.report.json",
          "sha256": "a3436ebd135170f741c55ed9fd0661f824be3b721049d7220fc7ce38ff5e2fbc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/static-glb.report.json",
          "sha256": "37ced9ff035fbe9d972c66353687bc8e01585ca92de896fa19a960785ca56d53",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/technical.report.json",
          "sha256": "ec6ce2fe302c96239c5de423b1ded698029aedc61e46a83315b0a65fb04ae873",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/calcite-raft-deposit/r002/visual.report.json",
          "sha256": "d8154f87dbae0a1a866c579fa3e6df7f3c72c0468615f1c1a0ffd44bbaf38940",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/brief.json",
          "sha256": "de200ddd48b79454f39b265b20fc7cdd4f4cef1030e0445bec0590dd1045ed4a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/build-config.json",
          "sha256": "ac67eb8c2ad7b7b406bd155250d071115084b5a693a2efb95c24bb1580a34ce1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/bundle-files.sha256",
          "sha256": "a696031e92b74643ec7d8f820f291bf172cad0800de3bc90a2701f3ae87225db",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-brief.json",
          "sha256": "df27fbe9dc29d10c09d1a763737b81353a0b98c00cd0a6ba1075dc0580f89fa2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-freeze.json",
          "sha256": "a3ee59039b5ec5a699e0f72d94f94e8820335c31f727fa45a90f7b353a44f52b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-integrity.json",
          "sha256": "6bd1caecd4f680033740e8bf9cb356ac911e970eee08400725eba252bd70b501",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-integrity.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/clay.png",
          "sha256": "e66597ad7c854e684ecb7da8d84c7ed0da67ba0869e10220c9027f4b2e6f06d1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/front.png",
          "sha256": "e011089884275e6211d5af81bf1dafa8a352b7f4c4240b1b66274b9a06e1c753",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/hero.png",
          "sha256": "60cab922f9474ac079b98fbc6a95734cd93af69ff5c780df4f81b4f49e40c667",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/rear.png",
          "sha256": "15fb92ca9d995a28e3f5669a621baba1935d7c9e7638dbea4bc611ccf6fd56ed",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/render-config.json",
          "sha256": "40f83cd3e5c82390a4ef0c6e2469917a964bae081c4bbc84062414461b06f166",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/render-manifest.json",
          "sha256": "b53f50e1800ea81fac9ed81f6f9a0c9a0ae93d2993cb82fe0c56c648e91f2a67",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/reversehero.png",
          "sha256": "c7f3858cacecb63dc03ca3818d80041375e375b4ce3a7eee7d139efb015642a0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/side.png",
          "sha256": "d7aa8ccfe008b9426b48a276fa34b3561bd60e2db6e4eb8defa63d8a4b7e2502",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/silhouette.png",
          "sha256": "f70a0c73369842177ff2cfcefbfe1a18c6cc3e63e03e13d2a60cd6456ab808fb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/top.png",
          "sha256": "e8dbb8e02df790c7939be5ce8afc834c04783c9686b4bab938b1ae2718a6217e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-proof/turntable.json",
          "sha256": "9e8dacc3e4eb297a08132dd3bdd035c44283b9f57cc0b92af09fcdf86d7d9f7a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate-render.stdout.txt",
          "sha256": "2e01dbf83742b82dd723292a06a2ec3ec1dfbb65455c0e232b51cdeb89383923",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/candidate.json",
          "sha256": "fb7c9aa45fc7a0ae9fabb3eb45463935a890d8d64efca787aca1a27eef72fa37",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/checker-exits.json",
          "sha256": "e8efe55b90b8ae143931eca13f6d961b455bb4bc06d937339afa306d3ea046c0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/concept-brief.md",
          "sha256": "f7bb38bf08fa65063d934c09e598abbe04b7da1a590c48e70d636f60b1c8b13d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/concept-completeness.json",
          "sha256": "cb64eb7412eede623cc2a7232ff61b164ae752ccd955e411490dcdd11d3baac1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/concept-completeness.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/concept-evidence.json",
          "sha256": "cb385f88dcea3336c1f11f7cf17d5a589a66166bc55a115caee5845e4e08d8b3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/concepts/generation-record.json",
          "sha256": "cc4f61f51da06042f807fe3b35dc42bad7e3aa98bc4f26879edfaf082936cb35",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/concepts/inspection.json",
          "sha256": "dbbf2f629930fd4cbb30785401a81e7137eca5000c7f238d302cb2157ff41a9b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/concepts/original.png",
          "sha256": "7c2cb8dd3ba7578ffe702e2818b2cc33abb6ec6a297b31c08895dd9654a80585",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/concepts/prompt.txt",
          "sha256": "042d1697a08baa8659c3a5b0eda1f8b45f55d2b44050d17a0bb097abbfacf2c9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/conichnus-conical-burrow.blend",
          "sha256": "4bb156af41158e9c2c899e0b55efdb0cb0e005ddf83cb7af46841e876388d121",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/conichnus-conical-burrow.glb",
          "sha256": "34948b0738264195544dd24ff377a1b0f3b92a93a1e34ab07d66647235388042",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/dependency-pins.json",
          "sha256": "0b8d79c088bfad8bfc2eea1d776f9dbcfd2233d46e741f64edf82836f46c700d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/derived-freeze.json",
          "sha256": "b6024b20d35e58c3296f8e8f1d1cdb559aefcd531d50efad6cf7c2e51c71a9a0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/diagnostics.stdout.txt",
          "sha256": "85fb930828980cb440aac3e0f845736a4527ee0989225998fb6cbc4e08cb369a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/diagnostics/diagnostic-manifest.json",
          "sha256": "69d373194dfc80a8a0f28caf27ffb8ab2de5214e1548281fc7ddcffe0136775e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/diagnostics/gray-oblique.png",
          "sha256": "944abb4429eb3e90f5014464a4e7905819484608a6b27bedbb88f081e452ba4d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/diagnostics/gray-section.png",
          "sha256": "dfdcafbb8a32367f1a95b838ba1b988882fbd7d8131cb6c7fe0668e3f20cb290",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/diagnostics/gray-top.png",
          "sha256": "c1acee054826ffd870da357488299a3925b54da658fb9219637752ecc347d4c3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/export-qa.json",
          "sha256": "5b5e07c2f2b36381c4393accb69f11e9d8f9b96f4bf340b98273929aa693f45b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/factual.report.json",
          "sha256": "adaa317c359214987e0d8ca1c3a1b03bcf023f6e147f98d4484d3c146623a1e3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/final-inspection.json",
          "sha256": "00f958b53691dcfe6f628843c809a45fe4941a2da7d0089523321d72f1808ea5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/generator.py",
          "sha256": "7128a119466d57120bf2f5635618a510dbecc4b36693d95f113e4709d22bd418",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/gltf-validator.report.json",
          "sha256": "55baf79bb794961b5e0e15e214104d4a92940bae08ee63fcbc2e1a8766f27096",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/gpu.report.json",
          "sha256": "5910c78182f72ad10ddd644d4fc6edf69bf0def770e4a3115320f321201ebbbe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/khronos.stdout.txt",
          "sha256": "874877703180212a15591a25baa15fd087eb4f9e219c3322e6977da004835afc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/maker-review.md",
          "sha256": "160144d559becbd6ebb48ed7b674a333d2bed0ffce74dbc8d905ada2574f9e61",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/metadata.json",
          "sha256": "99fadb070a377f891fc1265bfd6902082e35a8f9e8c0e355da0ac555ef2f10ce",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/model-start.json",
          "sha256": "32ff01a353b97a0b0a6c543797217987e7ca4c178dc114d346c62a7fedf75f50",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/negative-cavity-probe.json",
          "sha256": "8dac9e6240bb4017693d6dd3bc21de9d478d0113e665bf5aa39ecde51d87d15c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/profile-contract.json",
          "sha256": "4b6a63856b7751e78b8f8ca3ae28758c2d3611164388887798a214b8d23368f1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof-inspection-identity.json",
          "sha256": "50f9269fee63f9a074022e0f7ced4c821ededc4948d2868f7aba94b340cd79f6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof-render.stdout.txt",
          "sha256": "a2ab4cb3769e4b205c06d16896b258637135a5f18feb393adb5f0cdd85a4a27c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/clay.png",
          "sha256": "15029fa41a519e4ac749e1c0e95ded197ddd5d6e72020b7b31c28f28f4248c6d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/front.png",
          "sha256": "5e0c49955e33619a31d5f1d2ea3665c0576d3abcd3120e706402f3eaba97dfae",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/hero.png",
          "sha256": "5018eef72bfdeb9cdd3df493cc334db0cfad36b4b04ef69507495a8aaec226a2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/rear.png",
          "sha256": "cade77c0ecf795e0b3154babb6ef9979c54bd1c361f85e83e5ad96235ced8665",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/render-config.json",
          "sha256": "40f83cd3e5c82390a4ef0c6e2469917a964bae081c4bbc84062414461b06f166",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/render-manifest.json",
          "sha256": "98e18740c212dc5c275d42c23dd975165b3036a3a7346ccfb02bf8a7968f6e5e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/reversehero.png",
          "sha256": "1656139638a9508e30ee28c5767381c99710e39c0d06515f95b95fb7734dd016",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/side.png",
          "sha256": "1b2806d46809ea0b232f84c4d071b020882aaa12f3041aadd21132457290ed5c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/silhouette.png",
          "sha256": "fa085eb4a470e0d3aaeb588195322b527e1d9d10bb43692e32985471848d3bc5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/top.png",
          "sha256": "9555b0fe25193548b6eac38631c2a7d92591c84213dbfabfa9603c4721f5e6ac",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/proof/turntable.json",
          "sha256": "9e8dacc3e4eb297a08132dd3bdd035c44283b9f57cc0b92af09fcdf86d7d9f7a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/qa.json",
          "sha256": "01e6d26807be42fa6764bb106358f7065500c9362bbb079bf7d27c73a73281f8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/rebuild-1.report.json",
          "sha256": "11fca938b893c7c91971a87e4070c7cc8f7d6396f5d79dab6431fbafa9b18fc1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/rebuild-1.stdout.txt",
          "sha256": "11fca938b893c7c91971a87e4070c7cc8f7d6396f5d79dab6431fbafa9b18fc1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/rebuild-2.report.json",
          "sha256": "85f8156921ffe6618e529575a556ad3ae1291cad524e7950d99350eaf30a6802",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/rebuild-2.stdout.txt",
          "sha256": "85f8156921ffe6618e529575a556ad3ae1291cad524e7950d99350eaf30a6802",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/rebuilds.stdout.txt",
          "sha256": "939928b77277b7d33d547a9a9d580a941b0da1ad5ae7f5f66eb8e5f6dcf426ee",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/references.json",
          "sha256": "730d3eb206ee0033122a50a8beae6a7289463e82b013f6fa914610608f69f160",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime/front.png",
          "sha256": "aa3913f2901a91849bc8b175cd1b9cb90c4210596a0425e6feda9331bd2ed271",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime/hero.png",
          "sha256": "a6a63ff79bc6db0c14e865405f13a5df924427fb3c589f713dbb5234a14158c4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime/maker-inspection.json",
          "sha256": "2709453b39c77712c83732cf1c296f42c0ab47f97cb0f8bd5cd281f47d554ca9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime/near.png",
          "sha256": "7e2bd188cb2621a37a1a2ce4a4a9c1dc3b6c35cf9b3898ae824d970c53943d13",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime/reversehero.png",
          "sha256": "f57dfcb6d90f195d24e05fbaae8bc209a0e4437a21af2398239ffad71fd84ca7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime/runtime-report.json",
          "sha256": "8730b9ca6fbdd8a26249fa67a92b5d3b035139723817f0680f358b08abb45127",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime/scene-9-copies.png",
          "sha256": "8fa85b0721be4a24cf512f9a7d14d687be395e84efab1a588f97ff0ee224dbf1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime/side.png",
          "sha256": "09ed6cad03ec3220503effbe5caf0f0f095c8a18af8925a5b04ba565da5233fc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime/top.png",
          "sha256": "6a58c8bf92c45790dd76526fdb536a2536cca10b2c5aed398ec3007b08d49c14",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/runtime_parse.report.json",
          "sha256": "859d3830fdcc9b2284a6978ee789d50deca367a8093ff0ae992827240199166c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/scene.report.json",
          "sha256": "b3edcdbeb55697f6a9453ce2ee90b44ac8b5db3660491a7386e6676525d21b98",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/source-export.report.json",
          "sha256": "d51ea69cc9eb7149493d1d09ef027b9eed7dddeb824b4dde1e3ab08e16cdcb3b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/source-metrics.json",
          "sha256": "1ef5af4c17b0b167cbc8bf5ba288a32704b8da186b6bd3b453b7a06cf73d0c52",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/source-reopen.stdout.txt",
          "sha256": "1a0e06e82e6d33f147d2217c95a6455709bcfd8e403cdfeb765f6e40bfd425be",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/specification.report.json",
          "sha256": "0029f30076e2d4817386e091fc4e6bd51918fffe0135ddffebbca35a83fc7dec",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/static-glb.report.json",
          "sha256": "74f969a63950504409f93cccc7a61aa5be319818d5262b1c1145d94900a78ffe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/technical.report.json",
          "sha256": "8369bd63309d00d827bc186b3467562215e2cd700f90d333ec0019c62304e628",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/conichnus-conical-burrow/r001/visual.report.json",
          "sha256": "d7d7c537a012866ee1b287a5b726e3b57835b0d592e7900766557d0539663e82",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/brief.json",
          "sha256": "ac8a307da9938c7f52eb72a88e2922c83a93ced204edc024e341075b27dc3f97",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/build-config.json",
          "sha256": "fa5c836f1e391a0269c1504a77e25acc80daada4f76a2e16b4553828caccf4a8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/bundle-files.sha256",
          "sha256": "0486d44dd52f408a8f2132011fb28dfaaab545e1a2d7df2f8bc448dbd0e84681",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-brief.json",
          "sha256": "08212f4648bcd1dee2fcfaf484d313810d5f06cc08305205d1a84c3de0f6f5a0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-freeze.json",
          "sha256": "d6f5be37daa4ec7c28bbb2b223365a5820a6af2f9dbdb56975003b92577f0c6d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-integrity.json",
          "sha256": "3137134329dda0f8d00dd4ce5eb11ee5d106df66e91162c2df2de16b7511221e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-integrity.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/clay.png",
          "sha256": "0b8a9fbf8755d4474cdf716437308b5a0614dd2b28195de92f93a55273f2ef6b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/front.png",
          "sha256": "8fece4795421c639ecade6041909d6acd3fbc5fe28659226e27e1ec37ecb2ac9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/hero.png",
          "sha256": "b855e9a473445f61a8220e430072aba754a865007386b2360071137cf04dbadf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/rear.png",
          "sha256": "717d890c9518509ddc6577b1e25c7280c5e20fc163c9e25c4054a6fc5bf45209",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/render-config.json",
          "sha256": "5bd62b31f8f31c385a03b1cebb9a57ae039312a13d014ba48e96c66e7ba52d65",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/render-manifest.json",
          "sha256": "6b22102a41f63ca47bfb071ecf58a418db6f66281ce368c100154dc91dc682de",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/reversehero.png",
          "sha256": "24048915096fbecc50b6c6a8eea398f97c75c9d7f9951d5ca3567dac6d975523",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/side.png",
          "sha256": "57574905cf398b9a3814c60f444432525b6153241cb07a4751741926de8e7a0f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/silhouette.png",
          "sha256": "ffd1b2b87f65e6f8d0daf29af99588dcdff5ed235cf8ea27a387296cc9bfca2f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/top.png",
          "sha256": "b629f2532330a091f029a74513cf59ab22b86226403655ecf5446d04e126ac46",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-proof/turntable.json",
          "sha256": "f5914f0a75c914fa7c7acf905e5f27b2b00e8408662036f8761f4442fdc6cae3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate-render.stdout.txt",
          "sha256": "bd2bf5fbca0438d3f6a6ee73af730ca49e98a31140eba17afd19bdeec83a4302",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/candidate.json",
          "sha256": "b7721823ba4b4f5f62bae8582449d2b4bf1333edc14fbfaf37a3efe85c8a533b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/checker-exits.json",
          "sha256": "e8efe55b90b8ae143931eca13f6d961b455bb4bc06d937339afa306d3ea046c0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/concept-brief.md",
          "sha256": "9cfb046e45f724c80d2cd779f95d7ae6315655cb13b8e1af9829bef7cd339f39",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/concept-completeness.json",
          "sha256": "52b2c5eeff598016e97dd7b9dd18a99ba2a4a1ffb1602adfd697b64f5a2e1529",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/concept-completeness.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/concept-evidence.json",
          "sha256": "df8287d3d24a4886673b6837efc07fe90dbe334a5f81a557398a31f8ac10931e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/concepts/generation-record.json",
          "sha256": "f02b82839b4e75d5e75ccb15a2abec65e10087c09892a73626905f0eb38b33f6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/concepts/inspection.json",
          "sha256": "29bb8bfbb83b4e7c95d883fee65e00c9e296076b0f613748977dc70184d2e509",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/concepts/original.png",
          "sha256": "a8c8eaf0df9efe39148dc92ac980a5f2d64fd34c529cf4e94166be83f3055932",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/concepts/prompt.txt",
          "sha256": "fc60cd3f52ac7d9ce946fd4d8be0e940874aac511fe19781f154315165999705",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/dependency-pins.json",
          "sha256": "dd9f2f9ae3138a853f352ed81c59b1fd65a85c4764e611feb89bd147352d9586",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/derived-freeze.json",
          "sha256": "afaa7c065723f8a45af3d3b568409e7d03339c57057b0c1e5e82dd8108e9ca50",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/dicranurus.blend",
          "sha256": "a38846c7822b375f763f5ec71a2483261553845d03ade6355e84335929a7b3ab",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/dicranurus.glb",
          "sha256": "ffe61e0340399eb1bd41cb198ba5abc20edae439db44e3c21d4cf6d9e032bd65",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/export-qa.json",
          "sha256": "40fd8d72fa132c42368ea5872868f4d03676162856bd18ddbaf53e028bc874a6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/factual.report.json",
          "sha256": "b219eeeeaeac006d12e5a38e31137f2f4a797e9c6120080bba7c579a1c1884f5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/final-inspection.json",
          "sha256": "84c15ffb7367706b17f1dec4c520afad58f99106d6ef2226f00be429a7971a8b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/generator.py",
          "sha256": "d844d9c6ad4870d31e49821f387b6f266e5559b00669287734c3ad8d4c3811bc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/gltf-validator.report.json",
          "sha256": "69217988a1a048f3cd615be15cabf96dff65d7cd8b8c3005de78421f3cf6af36",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/gpu.report.json",
          "sha256": "285bb43c2ca0de163f76407fcd069d77b50fcdd399bad2d96d87a1dc016f7e5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/khronos.stdout.txt",
          "sha256": "fe2ba3f1347b4cb8286112242a938a4e14c993225e5d030891dab4d7cf6fda0a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/maker-review.md",
          "sha256": "dc486442c5079f5a75abe58f5fd347d36fcbba3f3716fc577e30345a14612ace",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/metadata.json",
          "sha256": "300d2bf2fd13679e872589c45fbc4f3141a11d2179f2e75a3ea15b0cf2712c0c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/model-start.json",
          "sha256": "518bd524263c476e89cf5fbe12ccd7414f58c20f266967bfec7d8ac5b8a71fc2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/profile-contract.json",
          "sha256": "c15133fe0d9331375ab5c6d2b21c45d018aed7c4f55fd248ba7ba0baf884e41d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof-inspection-identity.json",
          "sha256": "4a8d6f3fa9e57abecf09a0426deeefc1e7d7e928f94f3743468b7474a21e0f6e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof-render.stdout.txt",
          "sha256": "74cd08148cf6f9e07b37fde6af1993e403c781333ce184768850c1d32225c372",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/clay.png",
          "sha256": "aa42ef80a405c6e7d6ca4f4dd76862e25722b3943fb1bac20d112f6672f5eac7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/front.png",
          "sha256": "01cd3bc29085172bcbc9727d9d55f3b91084384f938c4f9b052f695cc0407e71",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/hero.png",
          "sha256": "cde4cf8039fbe69163c5e5f07b14535f77d057ddedb59faa09cb907027f2d5b7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/rear.png",
          "sha256": "8d88b5f08acff79af57fcb9fbadf04ab1f51d88f0b1184845f9d963e0776d68c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/render-config.json",
          "sha256": "9a248be310db2d3cc1e20a61c89fe2958e55377e8217b70fc60716bc3664629e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/render-manifest.json",
          "sha256": "2c369a68965402e8197d313fcd5a0ef398e7b6f41993cd793fde8d9c8fce9bf6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/reversehero.png",
          "sha256": "4155575d2e1121805160047792a3b70566830a3d7e916a25942ed6c8afef6f0f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/side.png",
          "sha256": "b08aa9d7725b5b63487919d08e702ee11a5b0539b5da747e203eb2a891702407",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/silhouette.png",
          "sha256": "a2ed525e0ad4ba7b26bd828670c00866a1cd0c6b61496cedb6b74336d0edb1e4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/top.png",
          "sha256": "25d1bb3c6edc81cba4e63975d0191fce993620647610ca0ab291c85acae1e5e9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/proof/turntable.json",
          "sha256": "1a802de53f9c8504328609976021be3ced86fdd02c8364a0abfa558bf49133c9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/qa.json",
          "sha256": "bfbf53f4e63868d4a80317a1c75f428a388c39966a906b1f7f0e92b6cd73a4f7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/rebuild-1.report.json",
          "sha256": "b86d3ecba8be25a407e1d0d9209cf042dea3c841937db6c462a16ba712ada9fe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/rebuild-1.stdout.txt",
          "sha256": "b86d3ecba8be25a407e1d0d9209cf042dea3c841937db6c462a16ba712ada9fe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/rebuild-2.report.json",
          "sha256": "a6f35ba3da53d0817888d3af7dcbd6a6809c31db848051074e55821381e78dc3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/rebuild-2.stdout.txt",
          "sha256": "a6f35ba3da53d0817888d3af7dcbd6a6809c31db848051074e55821381e78dc3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/rebuilds.stdout.txt",
          "sha256": "5c97c76e2f6b26b9561442209b0af9a11577dde90299085074ab1b4326ce66d0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/references.json",
          "sha256": "c6b75ad597c5228bbaa49d34f6ca5bdf61f89667db7f50b468454c6308df4e69",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime/front.png",
          "sha256": "ff31f0a61859bbcde6bbf2785db020d205650bc29289750a0cda4cf68f509b3b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime/hero.png",
          "sha256": "75d632fc4e2aa6637e36b37415f1778f652e586e038fc068947f0dc9871e2dc8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime/maker-inspection.json",
          "sha256": "4792e729036bfcf17412f59305f9665915a6f7f864407b2a50ebcc2c203ce25b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime/near.png",
          "sha256": "dfd748ac3d66f1ac9c92d90bf69b28cebfdd778db418b7106bc2ea2c259b34e5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime/reversehero.png",
          "sha256": "24e7e7dd6a68d3018184af29f8a3ce5b6a27b1bef02ebeb1a09995e830a19298",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime/runtime-report.json",
          "sha256": "625794a00fdf00b994f55d5639d41eb2e8143c747c932bbdbc452c60160d7bcf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime/scene-9-copies.png",
          "sha256": "4f6549606160dfa10cea52761418be6ea32f72bad95b39379cc85ed136f3cb83",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime/side.png",
          "sha256": "6fc435362f13b0476136e1cc12bacad60bd4e5cc88f12840588eeee45590ee0f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime/top.png",
          "sha256": "df34e1e43a4faad6f9f1020efaef4f4fdcbcf70f10476b8685f3be17e886d6ae",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/runtime_parse.report.json",
          "sha256": "a043faf2c47a213a5248e3db87f696f53350597146c0cf18d53b8b48945e4659",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/scene.report.json",
          "sha256": "aee3ab24f13dc9282cc8cdb41c0d4fa8f67f37eb1be350b9b2064874780e48a6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/source-export.report.json",
          "sha256": "227b1559b85b835fb76804e90ca023dca6fa07d6a973d67383d10f9eb3a05854",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/source-metrics.json",
          "sha256": "35b4834709edc8d13e54ccb6d3cd75de08f0a774369497cd803e1fb6cf90f629",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/source-reopen.stdout.txt",
          "sha256": "28c58cf08420c37c3ab3e7de3a01d9eb1001982a5025b0556167b7043de780d2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/specification.report.json",
          "sha256": "0dc181b8bdbb7400b6939aea016660170732a301ae2b60ffcbf48afddafa3913",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/static-glb.report.json",
          "sha256": "1123a12cef2921c3a411ef203cd0fdcf1993f1a841b84ff88de58cc295f29037",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/technical.report.json",
          "sha256": "f1b47ef42dd4cc464acaf29dbd7e4ac0d5762c8a47ef441ddcbdedd4c45b9486",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round17-20261018/batch-51/dicranurus/r001/visual.report.json",
          "sha256": "ff13febb99ce617bd172d7549352cc3ce1452a17e2a9b2c6ea084a984908db16",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/HANDOFF.md",
          "sha256": "6d97f1552d7122a3584557bb4ca64b23308f3073aadf7a55936a1cada8c6218f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/QA-HANDOFF.json",
          "sha256": "c8cf11f8bd1128c480f25ba359668d5a6ab3dfdc073754eded72a6f2e8a84efa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/brief.json",
          "sha256": "17d6c03fb129ec692a85dbbbb89777c3df1eacfeeca0de95799d817d622c979e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/build-config.json",
          "sha256": "18cc89fc9064efffb0dc8f32717cf71afeb980636948856583220d4831b973ff",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/build-jobs.json",
          "sha256": "a4cc0317cb02552ea499d81a4fe4624a12da3563a04c1daa58e1bfb668fca58a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/concept-brief.md",
          "sha256": "a0484379323f6acadb76be4358ef708d67643863c37bb2f3330478508448a79c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/concepts/generation-record.json",
          "sha256": "0d8ddb7ddf2b0487a5fa69af935d20ca15277f14c7962df495e217b3df749fc8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/concepts/inspection.json",
          "sha256": "3aabea9ef6bd81709fdc9ab2399ee207875ea75180dda31715bef078ea972a45",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/concepts/original.png",
          "sha256": "0a71d024dd5550445c94a54204b3cdcce3e8ef8d9ce2d541ff7c4c325b2ad5e7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/concepts/prompt.txt",
          "sha256": "bf17fc74b41b04dfe0a51670f4efed0bcbf1543418039e7d5b614de4fa3cc801",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/derived-freeze.json",
          "sha256": "772f3d43eecb5d08ba34029da846fc74710d86623496469b201af7d20d9332ed",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/generator.py",
          "sha256": "4e194758dfa704516a56ca9ff615c7d4d752a0ed435937375ae60d766bb455e8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/model-start.json",
          "sha256": "9561d4f8c483a26fce989ded646340859510007a7a7e0f31c16f0d5964dd933c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-jobs.json",
          "sha256": "9854a3cdf8b3ab8def5308d18a34c001e92a66a926b2280006313601f936f786",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-1/9f5ce286905410ccbb0fe80b1d42a30c8c11400c39500b54cf4e5ebc7faff7a6/20261019T225521-d1b42d2b15524b5f81f904f274648a40/outputs/accretionary-lapilli-bed.blend",
          "sha256": "c34fc08436727aab8abc4154b039f89e7bbadd2333f7ba896d228bbc6c9fc3f7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-1/9f5ce286905410ccbb0fe80b1d42a30c8c11400c39500b54cf4e5ebc7faff7a6/20261019T225521-d1b42d2b15524b5f81f904f274648a40/outputs/accretionary-lapilli-bed.glb",
          "sha256": "b25ee4fd368d42ce142bd05659d4b3d7b6eb75b3f54d899f8506e5e726d43f36",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-1/9f5ce286905410ccbb0fe80b1d42a30c8c11400c39500b54cf4e5ebc7faff7a6/20261019T225521-d1b42d2b15524b5f81f904f274648a40/outputs/metadata.json",
          "sha256": "f6278e45365e6eedafe1ff7f0075f7f55af083281698e2c18390e242ead7838b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-1/9f5ce286905410ccbb0fe80b1d42a30c8c11400c39500b54cf4e5ebc7faff7a6/20261019T225521-d1b42d2b15524b5f81f904f274648a40/outputs/qa.json",
          "sha256": "ac3deb4b394bdabb1b117cdf81de77bc73cccc9e6014792243ad4e4062caf169",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-1/9f5ce286905410ccbb0fe80b1d42a30c8c11400c39500b54cf4e5ebc7faff7a6/20261019T225521-d1b42d2b15524b5f81f904f274648a40/request.json",
          "sha256": "c8f0d3290d367a99d88adb330481768043e88bbc124d1d9eb7c6f53d6fbed5a5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-1/9f5ce286905410ccbb0fe80b1d42a30c8c11400c39500b54cf4e5ebc7faff7a6/20261019T225521-d1b42d2b15524b5f81f904f274648a40/result.json",
          "sha256": "434b0bcbd74d4e2058caa982791d9a17ea6d9091dc4811970ffe94ac2fe5658f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-1/9f5ce286905410ccbb0fe80b1d42a30c8c11400c39500b54cf4e5ebc7faff7a6/20261019T225521-d1b42d2b15524b5f81f904f274648a40/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-1/9f5ce286905410ccbb0fe80b1d42a30c8c11400c39500b54cf4e5ebc7faff7a6/20261019T225521-d1b42d2b15524b5f81f904f274648a40/stdout.log",
          "sha256": "e12a84afbffb2ec00aef7f594205ac24f4e3959d77254d603a5683ebf6b47026",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-2/30fbf078bea19fd5fa47d5de933160319df2b624351c6d942a2fc1c38cdd94b1/20261019T225527-d377c38234c042ff80d24a2de24a6990/outputs/accretionary-lapilli-bed.blend",
          "sha256": "c94f7202c01a69015bb8e8cd5c3a7365157e5d40772268bf43a59dd57168419c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-2/30fbf078bea19fd5fa47d5de933160319df2b624351c6d942a2fc1c38cdd94b1/20261019T225527-d377c38234c042ff80d24a2de24a6990/outputs/accretionary-lapilli-bed.glb",
          "sha256": "b25ee4fd368d42ce142bd05659d4b3d7b6eb75b3f54d899f8506e5e726d43f36",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-2/30fbf078bea19fd5fa47d5de933160319df2b624351c6d942a2fc1c38cdd94b1/20261019T225527-d377c38234c042ff80d24a2de24a6990/outputs/metadata.json",
          "sha256": "ad59d663ce9259938160afa7e70685b76870267973da07a1892cf35a7c0e8ff6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-2/30fbf078bea19fd5fa47d5de933160319df2b624351c6d942a2fc1c38cdd94b1/20261019T225527-d377c38234c042ff80d24a2de24a6990/outputs/qa.json",
          "sha256": "d15bd996c449786b3b98829f9a04ccddef7ccda0f2e538598f1516859aae5232",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-2/30fbf078bea19fd5fa47d5de933160319df2b624351c6d942a2fc1c38cdd94b1/20261019T225527-d377c38234c042ff80d24a2de24a6990/request.json",
          "sha256": "bb1ed417faa8a8328f6b41d88d5ffe676c14f91cc39c267e10c471917feed62e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-2/30fbf078bea19fd5fa47d5de933160319df2b624351c6d942a2fc1c38cdd94b1/20261019T225527-d377c38234c042ff80d24a2de24a6990/result.json",
          "sha256": "8c4730ef26fb309159cb33e90e0b77864bb43867daaf60af2c1465b7591b1fb2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-2/30fbf078bea19fd5fa47d5de933160319df2b624351c6d942a2fc1c38cdd94b1/20261019T225527-d377c38234c042ff80d24a2de24a6990/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/build/accretionary-lapilli-bed/r001/rebuild-2/30fbf078bea19fd5fa47d5de933160319df2b624351c6d942a2fc1c38cdd94b1/20261019T225527-d377c38234c042ff80d24a2de24a6990/stdout.log",
          "sha256": "c0352e3d063bbd2abb82e588de7e220b20393522a048de6a2ab76f570a84f4c3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/runs/20261019T225520-7953331dfb7a46eeac63a4bcff1a5ede/manifest.json",
          "sha256": "04023f59a61a2524171df215662b0132c60fa4fdd98b0037d543602eeaf946b1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/rebuild-runs/runs/20261019T225520-7953331dfb7a46eeac63a4bcff1a5ede/summary.json",
          "sha256": "a371666acf810d65f72f72bcabdc6b2d6015ebadf4cc322c64bffa33285da626",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/references.json",
          "sha256": "5245b6fb370a20b8622e83f29a289fcf263b8caa60e81ec2a5d1a70aad884465",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/build/accretionary-lapilli-bed/r001/build-original/5e9ca01c87243962c5f9771a6543b4d638d13da17c94e084728f3c8999a4b898/20261019T225409-dd31a52f4a5044fb84c45f9e47cec8fd/outputs/accretionary-lapilli-bed.blend",
          "sha256": "6b20b7718d321eba2c61f241cdda0acd10c3bcbd17a91b01e121380967ca0be5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/build/accretionary-lapilli-bed/r001/build-original/5e9ca01c87243962c5f9771a6543b4d638d13da17c94e084728f3c8999a4b898/20261019T225409-dd31a52f4a5044fb84c45f9e47cec8fd/outputs/accretionary-lapilli-bed.glb",
          "sha256": "b25ee4fd368d42ce142bd05659d4b3d7b6eb75b3f54d899f8506e5e726d43f36",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/build/accretionary-lapilli-bed/r001/build-original/5e9ca01c87243962c5f9771a6543b4d638d13da17c94e084728f3c8999a4b898/20261019T225409-dd31a52f4a5044fb84c45f9e47cec8fd/outputs/metadata.json",
          "sha256": "5338adbc4980e25ea0e0485c323b3d96c3847ad9ae8c83aeb0a9fb2547ccafb6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/build/accretionary-lapilli-bed/r001/build-original/5e9ca01c87243962c5f9771a6543b4d638d13da17c94e084728f3c8999a4b898/20261019T225409-dd31a52f4a5044fb84c45f9e47cec8fd/outputs/qa.json",
          "sha256": "7c9ad90f4b67576b79d0f32c149527ef9200f2264b82bccb3bf6d9e6a2291e68",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/build/accretionary-lapilli-bed/r001/build-original/5e9ca01c87243962c5f9771a6543b4d638d13da17c94e084728f3c8999a4b898/20261019T225409-dd31a52f4a5044fb84c45f9e47cec8fd/request.json",
          "sha256": "d17ab3583aaa78b93f95eb25c00323d8ec7f89ad827d881cddfce11d3e1e8356",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/build/accretionary-lapilli-bed/r001/build-original/5e9ca01c87243962c5f9771a6543b4d638d13da17c94e084728f3c8999a4b898/20261019T225409-dd31a52f4a5044fb84c45f9e47cec8fd/result.json",
          "sha256": "014dbf6310181148cdac61099a3c537762d86510c85c8d33270c0da60864e39c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/build/accretionary-lapilli-bed/r001/build-original/5e9ca01c87243962c5f9771a6543b4d638d13da17c94e084728f3c8999a4b898/20261019T225409-dd31a52f4a5044fb84c45f9e47cec8fd/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/build/accretionary-lapilli-bed/r001/build-original/5e9ca01c87243962c5f9771a6543b4d638d13da17c94e084728f3c8999a4b898/20261019T225409-dd31a52f4a5044fb84c45f9e47cec8fd/stdout.log",
          "sha256": "ff7ae282507bd24cbb9e1b56d02ecac1dff16b77c9e62ba9a5e5b1b63284bff0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/runs/20261019T225408-ba93988e7a6f4d44a55c42960828310c/manifest.json",
          "sha256": "f2bec5c5109312576d5d34a5ef397c90b94c551c121a125ccb85cb39be127194",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r001/runs/runs/20261019T225408-ba93988e7a6f4d44a55c42960828310c/summary.json",
          "sha256": "b30a0b8cef25728e496250862a833f8b7613131b896ab1ae9035158b984f8f5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/brief.json",
          "sha256": "1997290d983b25b1938575ca69791078148cc2743324a1e9885ad643ff67ec7d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/build-config.json",
          "sha256": "03cfc2dfbc7960342a3426d0085f93c32dbb71af5c1cf7e7fd7219b63b39a611",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/build-jobs.json",
          "sha256": "f5b920866e15ad54d603718cec71db38ece67359948cff772f30c5e73beebe0f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/concept-brief.md",
          "sha256": "c6805fa20c4229cd5a872e5558bcce2f7c35f0779bbe45b6d794dfb92722de06",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/concepts/generation-record.json",
          "sha256": "0d8ddb7ddf2b0487a5fa69af935d20ca15277f14c7962df495e217b3df749fc8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/concepts/inspection.json",
          "sha256": "3aabea9ef6bd81709fdc9ab2399ee207875ea75180dda31715bef078ea972a45",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/concepts/original.png",
          "sha256": "0a71d024dd5550445c94a54204b3cdcce3e8ef8d9ce2d541ff7c4c325b2ad5e7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/concepts/prompt.txt",
          "sha256": "bf17fc74b41b04dfe0a51670f4efed0bcbf1543418039e7d5b614de4fa3cc801",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/derived-freeze.json",
          "sha256": "b8ecd73e403b75d335057d5eb9379452b2b60d3039b65834cda2bc8c129e8c35",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/generator.py",
          "sha256": "7128a119466d57120bf2f5635618a510dbecc4b36693d95f113e4709d22bd418",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/model-start.json",
          "sha256": "40186e29b310809f66dc826f8d0417ae2ed80ed0f7ea726e63226c13ca1623b3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-jobs.json",
          "sha256": "80a2cb50b16c2d85eab8008cb09578f8702861d404d6e17e5b0c8004e591f83e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-1/ae5423f72cc810549784a77b5185c5aa824a6540418a9b948c39439da6d870db/20261019T225659-68b7ddbf06e94bdcb224a4e9ecd3ed1d/outputs/accretionary-lapilli-bed.blend",
          "sha256": "8dfb176c00f762fe3a41426170db3cc52fcd71f3e07923b84be1abcd87b82d8d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-1/ae5423f72cc810549784a77b5185c5aa824a6540418a9b948c39439da6d870db/20261019T225659-68b7ddbf06e94bdcb224a4e9ecd3ed1d/outputs/accretionary-lapilli-bed.glb",
          "sha256": "61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-1/ae5423f72cc810549784a77b5185c5aa824a6540418a9b948c39439da6d870db/20261019T225659-68b7ddbf06e94bdcb224a4e9ecd3ed1d/outputs/metadata.json",
          "sha256": "9d6dba602ce18956a6cdcad50fc036f4e4b77cc50afa7a5c7365bde7267eaf53",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-1/ae5423f72cc810549784a77b5185c5aa824a6540418a9b948c39439da6d870db/20261019T225659-68b7ddbf06e94bdcb224a4e9ecd3ed1d/outputs/qa.json",
          "sha256": "43851ac7bfdb30588f854d43fc8df68bb3f5a7c39230535b5d52752220e54f51",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-1/ae5423f72cc810549784a77b5185c5aa824a6540418a9b948c39439da6d870db/20261019T225659-68b7ddbf06e94bdcb224a4e9ecd3ed1d/request.json",
          "sha256": "c5a0d2ec8fb197c4624dcb0275009576a36419213b47e666ba4265ad8419c973",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-1/ae5423f72cc810549784a77b5185c5aa824a6540418a9b948c39439da6d870db/20261019T225659-68b7ddbf06e94bdcb224a4e9ecd3ed1d/result.json",
          "sha256": "372745479a45bf5eb240cb3f4aff438eb339d116777f8ebd6e3c7bf50d312e9e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-1/ae5423f72cc810549784a77b5185c5aa824a6540418a9b948c39439da6d870db/20261019T225659-68b7ddbf06e94bdcb224a4e9ecd3ed1d/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-1/ae5423f72cc810549784a77b5185c5aa824a6540418a9b948c39439da6d870db/20261019T225659-68b7ddbf06e94bdcb224a4e9ecd3ed1d/stdout.log",
          "sha256": "e58172e358f99967c276e8084e237939cd2b5d9bb93fabaf692d824528dca2ff",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-2/1bade824e8719e0496e3825613bbb5874a0626d381dbd9ebf9d8ae4dce74abaf/20261019T225705-19eb13258e7a4e9caf060e813598fb25/outputs/accretionary-lapilli-bed.blend",
          "sha256": "9ab5f01df41cecefb306826e1b5b706a41761be19720af1eb5a536c3b75a0442",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-2/1bade824e8719e0496e3825613bbb5874a0626d381dbd9ebf9d8ae4dce74abaf/20261019T225705-19eb13258e7a4e9caf060e813598fb25/outputs/accretionary-lapilli-bed.glb",
          "sha256": "61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-2/1bade824e8719e0496e3825613bbb5874a0626d381dbd9ebf9d8ae4dce74abaf/20261019T225705-19eb13258e7a4e9caf060e813598fb25/outputs/metadata.json",
          "sha256": "ebf92779f231c286b6e41427643de81004f731d3060625e1e89955e6612af6a3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-2/1bade824e8719e0496e3825613bbb5874a0626d381dbd9ebf9d8ae4dce74abaf/20261019T225705-19eb13258e7a4e9caf060e813598fb25/outputs/qa.json",
          "sha256": "1ff4386d7954fa1de60826c786827128fa98370b4faa17307f1a1a0a384080b7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-2/1bade824e8719e0496e3825613bbb5874a0626d381dbd9ebf9d8ae4dce74abaf/20261019T225705-19eb13258e7a4e9caf060e813598fb25/request.json",
          "sha256": "d787f03fb3431e797b03897d23115a227d0015d27ff0054ef440c5d3c9fd7231",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-2/1bade824e8719e0496e3825613bbb5874a0626d381dbd9ebf9d8ae4dce74abaf/20261019T225705-19eb13258e7a4e9caf060e813598fb25/result.json",
          "sha256": "5616b36745fa13083e7d97e44d671118e5d3c29f55f22cba62ed9258c0122613",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-2/1bade824e8719e0496e3825613bbb5874a0626d381dbd9ebf9d8ae4dce74abaf/20261019T225705-19eb13258e7a4e9caf060e813598fb25/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/build/accretionary-lapilli-bed/r002/rebuild-2/1bade824e8719e0496e3825613bbb5874a0626d381dbd9ebf9d8ae4dce74abaf/20261019T225705-19eb13258e7a4e9caf060e813598fb25/stdout.log",
          "sha256": "71e0992fda65272ab13dd5d1c297f307a3772163a6727b643a5aeeac44aae342",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/runs/20261019T225658-3148f0cdbd1d4b1490a31f6ee29dfe6a/manifest.json",
          "sha256": "1ef39eaaae4487ee51991b9bf9c51b5ba5138a53e83add01dcfd75756fe600bd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/rebuild-runs/runs/20261019T225658-3148f0cdbd1d4b1490a31f6ee29dfe6a/summary.json",
          "sha256": "bf3b91a7abc9d11d16b08685de4b45ea1fcfe1dd255ab9674edb9ea8ea2b4e91",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/references.json",
          "sha256": "5245b6fb370a20b8622e83f29a289fcf263b8caa60e81ec2a5d1a70aad884465",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/build/accretionary-lapilli-bed/r002/build-original/95637d3237227f8d083410ea9eab3008d8d52f0b87c2ae722c3d1b1f5324f97f/20261019T225557-01db125273724d86940eff2ec428206e/outputs/accretionary-lapilli-bed.blend",
          "sha256": "83b58908c86c908b28330bfbf5e8ff034020e186812a41a4f9682e151d387125",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/build/accretionary-lapilli-bed/r002/build-original/95637d3237227f8d083410ea9eab3008d8d52f0b87c2ae722c3d1b1f5324f97f/20261019T225557-01db125273724d86940eff2ec428206e/outputs/accretionary-lapilli-bed.glb",
          "sha256": "61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/build/accretionary-lapilli-bed/r002/build-original/95637d3237227f8d083410ea9eab3008d8d52f0b87c2ae722c3d1b1f5324f97f/20261019T225557-01db125273724d86940eff2ec428206e/outputs/metadata.json",
          "sha256": "377222af5079ef8d2b1a63712b8734714a8f7ab7a2cd60b07f52f55c2d5975b1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/build/accretionary-lapilli-bed/r002/build-original/95637d3237227f8d083410ea9eab3008d8d52f0b87c2ae722c3d1b1f5324f97f/20261019T225557-01db125273724d86940eff2ec428206e/outputs/qa.json",
          "sha256": "6a4a7d7c7cc0ddf837b74d24ad322b062cc2f405460e3bc22fa0fdcee22d351a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/build/accretionary-lapilli-bed/r002/build-original/95637d3237227f8d083410ea9eab3008d8d52f0b87c2ae722c3d1b1f5324f97f/20261019T225557-01db125273724d86940eff2ec428206e/request.json",
          "sha256": "86a1b31128484d91a1e29086a04620690ef23cb5f63154ef4dcba66522da5513",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/build/accretionary-lapilli-bed/r002/build-original/95637d3237227f8d083410ea9eab3008d8d52f0b87c2ae722c3d1b1f5324f97f/20261019T225557-01db125273724d86940eff2ec428206e/result.json",
          "sha256": "19e2831b4f677a14e621138390dd24ca7be68ee80cc2688b679984250690d98d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/build/accretionary-lapilli-bed/r002/build-original/95637d3237227f8d083410ea9eab3008d8d52f0b87c2ae722c3d1b1f5324f97f/20261019T225557-01db125273724d86940eff2ec428206e/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/build/accretionary-lapilli-bed/r002/build-original/95637d3237227f8d083410ea9eab3008d8d52f0b87c2ae722c3d1b1f5324f97f/20261019T225557-01db125273724d86940eff2ec428206e/stdout.log",
          "sha256": "061b86796b9f846c017e9a004229c07afd81203324d083a5cb112768cf917f6e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/runs/20261019T225557-35820ac4061a44dc84498c0971cd1ccc/manifest.json",
          "sha256": "ac725460836242ca37445984fdd694bf5e68d33d61e804a016d5db7df5afc661",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/accretionary-lapilli-bed/r002/runs/runs/20261019T225557-35820ac4061a44dc84498c0971cd1ccc/summary.json",
          "sha256": "4e83485d367bb7960c61649cf2b7e412a2241850b54dfe4cec9fde8ea2020259",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/brief.json",
          "sha256": "44dbf2ec31d49eb2fcd21cbf9719b0de4d8534df7a7d405f9a5f72e33727c1e9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/build-config.json",
          "sha256": "860f993f301a3cb073525bda3159d833ab7748f8db49b35095a83953b607ce26",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/build-jobs.json",
          "sha256": "554a06c6f373e50f4fc0244d67d9183bb661678714bba6295dc45f0a919636d0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/concept-brief.md",
          "sha256": "471074359c19ee5412c8b9f0218d82107836f34250a55533df9b5dfce19ceaea",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/concepts/generation-record.json",
          "sha256": "701885e9a932cc4c113d85c810f3ce5b96532447bdbd4012cd2b93b828226e5f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/concepts/inspection.json",
          "sha256": "149c5dc6b494ae2f5ab89879e284a5590416caee5f109db91b760deb296f38c6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/concepts/original.png",
          "sha256": "07140bd478b0f36c4e97281d70559f392010bbb6e9f50830da31e07e41368cfa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/concepts/prompt.txt",
          "sha256": "3785718352897fe890639ee618899b68a20be934e1fd9f4354529f3a0583dc68",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/derived-freeze.json",
          "sha256": "c7ca6f6f277456667ec746b37a192e3ff578bdb4da5ad75242bea4958703b10a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/generator.py",
          "sha256": "d844d9c6ad4870d31e49821f387b6f266e5559b00669287734c3ad8d4c3811bc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/model-start.json",
          "sha256": "9f8bbf2008e959faf3dbfdfaf357133e70549e27ddf528cacd0d939d728969ff",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-jobs.json",
          "sha256": "3d56853646170b7175942029d0a2cb4f1cb7cb7a905c1463389cd32d59a3e342",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-1/de0a60b36c1bd05179fbae9acb36762f2702f3657984e280b40da9bbb274ec2d/20261019T225137-a5724a5c78cc41a29b88cdcc14240a8e/outputs/calcite-raft-deposit.blend",
          "sha256": "cebc6d8783adf61e80e003cd03861c2afb6af08c292e968e4d126e3aad16e936",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-1/de0a60b36c1bd05179fbae9acb36762f2702f3657984e280b40da9bbb274ec2d/20261019T225137-a5724a5c78cc41a29b88cdcc14240a8e/outputs/calcite-raft-deposit.glb",
          "sha256": "5620215ee6b745c7fff7a393ce2d48f164f6914ed48027cbf3bddc54aa5ab336",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-1/de0a60b36c1bd05179fbae9acb36762f2702f3657984e280b40da9bbb274ec2d/20261019T225137-a5724a5c78cc41a29b88cdcc14240a8e/outputs/metadata.json",
          "sha256": "e1f60d7c8957dc11fed6417debe279469fe6f5a49bf1cacaf8c30ff5a6f76b23",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-1/de0a60b36c1bd05179fbae9acb36762f2702f3657984e280b40da9bbb274ec2d/20261019T225137-a5724a5c78cc41a29b88cdcc14240a8e/outputs/qa.json",
          "sha256": "c634136bc1dde6e041c7af2c2f6b05c4b59c939558f4a0aa3c40fe04d51f43c6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-1/de0a60b36c1bd05179fbae9acb36762f2702f3657984e280b40da9bbb274ec2d/20261019T225137-a5724a5c78cc41a29b88cdcc14240a8e/request.json",
          "sha256": "5418e11cf5f4b44def675b9369d11e5956db0db83a7cfca5246ca1817fd19440",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-1/de0a60b36c1bd05179fbae9acb36762f2702f3657984e280b40da9bbb274ec2d/20261019T225137-a5724a5c78cc41a29b88cdcc14240a8e/result.json",
          "sha256": "fb462f401587191e08140471adda1623aa460573a558dfb760fab2b58288cdaf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-1/de0a60b36c1bd05179fbae9acb36762f2702f3657984e280b40da9bbb274ec2d/20261019T225137-a5724a5c78cc41a29b88cdcc14240a8e/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-1/de0a60b36c1bd05179fbae9acb36762f2702f3657984e280b40da9bbb274ec2d/20261019T225137-a5724a5c78cc41a29b88cdcc14240a8e/stdout.log",
          "sha256": "d47175014bfc78dfcee537d30c4f92f6cfa313a65ae4c30ea4588159eb23f3ab",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-2/c1db012046b2b3d983f7f3e95a96a89f26df8fe7c4c1a3f6d426db901fe1367f/20261019T225146-e6b03daac0e34e11aaeba3f75102e7dc/outputs/calcite-raft-deposit.blend",
          "sha256": "fe89823751ea918c242b68458a14dfd0213250055e369f7c3f5ed0b6bd8aa04b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-2/c1db012046b2b3d983f7f3e95a96a89f26df8fe7c4c1a3f6d426db901fe1367f/20261019T225146-e6b03daac0e34e11aaeba3f75102e7dc/outputs/calcite-raft-deposit.glb",
          "sha256": "5620215ee6b745c7fff7a393ce2d48f164f6914ed48027cbf3bddc54aa5ab336",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-2/c1db012046b2b3d983f7f3e95a96a89f26df8fe7c4c1a3f6d426db901fe1367f/20261019T225146-e6b03daac0e34e11aaeba3f75102e7dc/outputs/metadata.json",
          "sha256": "b48e387c485ba60a6c0bc9ddb18b4624f9dc42585a846c5b033d782ae6ac8446",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-2/c1db012046b2b3d983f7f3e95a96a89f26df8fe7c4c1a3f6d426db901fe1367f/20261019T225146-e6b03daac0e34e11aaeba3f75102e7dc/outputs/qa.json",
          "sha256": "3900650ab569c13c4ae5532f1a565d56b6748a88c7c4509b076a9e77167c405e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-2/c1db012046b2b3d983f7f3e95a96a89f26df8fe7c4c1a3f6d426db901fe1367f/20261019T225146-e6b03daac0e34e11aaeba3f75102e7dc/request.json",
          "sha256": "ae649ace16d7f9d216b724cba4059c9ee63a6314efa2259ac7fc5e143178b52b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-2/c1db012046b2b3d983f7f3e95a96a89f26df8fe7c4c1a3f6d426db901fe1367f/20261019T225146-e6b03daac0e34e11aaeba3f75102e7dc/result.json",
          "sha256": "828e602f218b45b521850df6ec598bc632f462d684b0e0e923f2c77f64ec5969",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-2/c1db012046b2b3d983f7f3e95a96a89f26df8fe7c4c1a3f6d426db901fe1367f/20261019T225146-e6b03daac0e34e11aaeba3f75102e7dc/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/build/calcite-raft-deposit/r001/rebuild-2/c1db012046b2b3d983f7f3e95a96a89f26df8fe7c4c1a3f6d426db901fe1367f/20261019T225146-e6b03daac0e34e11aaeba3f75102e7dc/stdout.log",
          "sha256": "6ba148d96982f82bb16f3fee8ca319c3dba877653636107339cca8e406a7430b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/runs/20261019T225137-60d4e23a6db249b0af7ed5491ae29f2b/manifest.json",
          "sha256": "8e7068a7f2bf68d85f4185b746961e0a09f05b97d914634eafbe02aae04d47c2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/rebuild-runs/runs/20261019T225137-60d4e23a6db249b0af7ed5491ae29f2b/summary.json",
          "sha256": "a09610a6c2bee1f474a85f7052e63d547189db8ecebf9cc3ab938ae712535662",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/references.json",
          "sha256": "5213a445fa920c25af8cea7a065e0f9f80195adaf6ee93bda455d490582bca19",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/build/calcite-raft-deposit/r001/build-original/4bf834fcd58a6c41ecbcc7294952650e8d7ec1d9039c32997e445a141fe8224f/20261019T225057-cae5eab219f647408f1c8dad9cb6b4e6/outputs/calcite-raft-deposit.blend",
          "sha256": "95c0634588527ab71722c29837a3e823efccbfde7b28e93decc8ea93833ce736",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/build/calcite-raft-deposit/r001/build-original/4bf834fcd58a6c41ecbcc7294952650e8d7ec1d9039c32997e445a141fe8224f/20261019T225057-cae5eab219f647408f1c8dad9cb6b4e6/outputs/calcite-raft-deposit.glb",
          "sha256": "5620215ee6b745c7fff7a393ce2d48f164f6914ed48027cbf3bddc54aa5ab336",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/build/calcite-raft-deposit/r001/build-original/4bf834fcd58a6c41ecbcc7294952650e8d7ec1d9039c32997e445a141fe8224f/20261019T225057-cae5eab219f647408f1c8dad9cb6b4e6/outputs/metadata.json",
          "sha256": "7e57464f6790f268c1d780dd8908904f7ba0b701c1550d5b31cb56998afb1d17",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/build/calcite-raft-deposit/r001/build-original/4bf834fcd58a6c41ecbcc7294952650e8d7ec1d9039c32997e445a141fe8224f/20261019T225057-cae5eab219f647408f1c8dad9cb6b4e6/outputs/qa.json",
          "sha256": "4b025ab6d506ccd47eb1277afb60332622371c7f17a9704df1251c3d6b89063f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/build/calcite-raft-deposit/r001/build-original/4bf834fcd58a6c41ecbcc7294952650e8d7ec1d9039c32997e445a141fe8224f/20261019T225057-cae5eab219f647408f1c8dad9cb6b4e6/request.json",
          "sha256": "17398bd1aa2931a9fbf694b3964b33e8aa1bc87bc42385fb31fb4a8d490a1194",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/build/calcite-raft-deposit/r001/build-original/4bf834fcd58a6c41ecbcc7294952650e8d7ec1d9039c32997e445a141fe8224f/20261019T225057-cae5eab219f647408f1c8dad9cb6b4e6/result.json",
          "sha256": "21b113778b3bd1a39e6b45dd182205787badc3c433dafb69b38e4050e16e5fc8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/build/calcite-raft-deposit/r001/build-original/4bf834fcd58a6c41ecbcc7294952650e8d7ec1d9039c32997e445a141fe8224f/20261019T225057-cae5eab219f647408f1c8dad9cb6b4e6/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/build/calcite-raft-deposit/r001/build-original/4bf834fcd58a6c41ecbcc7294952650e8d7ec1d9039c32997e445a141fe8224f/20261019T225057-cae5eab219f647408f1c8dad9cb6b4e6/stdout.log",
          "sha256": "8e4f3beeac1d27434397328f479c6b337c156b4edfc3bf2e5c4189a7e9dec17f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/runs/20261019T225057-8a87b4ab510644d8b6542c7eea9054ff/manifest.json",
          "sha256": "753ac7321251ac49570976436a7577a7ac4b63dc1f663a4f90383c4a43820915",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r001/runs/runs/20261019T225057-8a87b4ab510644d8b6542c7eea9054ff/summary.json",
          "sha256": "0f05bcb2ef293ddb0b779f3bbf9bb9197de498d44993b6c4bcf2a0e826e15eca",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/brief.json",
          "sha256": "6473983ac984d9aff316bba880fbf36741a7a9741e5a556e0e96ad5c70324c82",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/build-config.json",
          "sha256": "754964fd808f8a29326bfb5e9f8aa0f68d536396dc464ca91236602fcca2e858",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/build-jobs.json",
          "sha256": "d677fe087c2744a5a60c5f00017b276a96aafafc7d76f288e7f3e7c09acc4857",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/concept-brief.md",
          "sha256": "32002cbe68490f2ba0acfddfac722364856b655b7c2978e9cbd87e9547883ed2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/concepts/generation-record.json",
          "sha256": "701885e9a932cc4c113d85c810f3ce5b96532447bdbd4012cd2b93b828226e5f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/concepts/inspection.json",
          "sha256": "149c5dc6b494ae2f5ab89879e284a5590416caee5f109db91b760deb296f38c6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/concepts/original.png",
          "sha256": "07140bd478b0f36c4e97281d70559f392010bbb6e9f50830da31e07e41368cfa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/concepts/prompt.txt",
          "sha256": "3785718352897fe890639ee618899b68a20be934e1fd9f4354529f3a0583dc68",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/derived-freeze.json",
          "sha256": "1f482f73c81ef19f12a51989f23ee54eaf0314c2c02d67a897c3f84b26e41371",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/generator.py",
          "sha256": "4e194758dfa704516a56ca9ff615c7d4d752a0ed435937375ae60d766bb455e8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/model-start.json",
          "sha256": "4b2afbf23331dd30cd0e6585101bea0ec83fedb0a9c4eb5af800b198b49084b4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-jobs.json",
          "sha256": "516e7853f4ce1cdba0f3d2cd94f6477e2bc9fb5d35ff436694b285a43cdda743",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-1/3139ad41d138353151cd398f5d000ad6bf29c1657418485f8ad5e870ca9e4857/20261019T225332-04f9508f19634e91bfffdea3c7d4fd06/outputs/calcite-raft-deposit.blend",
          "sha256": "fa644154a1d671b85be1f43e4dc3937e6054f743d4d8f67815218c24390a583b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-1/3139ad41d138353151cd398f5d000ad6bf29c1657418485f8ad5e870ca9e4857/20261019T225332-04f9508f19634e91bfffdea3c7d4fd06/outputs/calcite-raft-deposit.glb",
          "sha256": "fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-1/3139ad41d138353151cd398f5d000ad6bf29c1657418485f8ad5e870ca9e4857/20261019T225332-04f9508f19634e91bfffdea3c7d4fd06/outputs/metadata.json",
          "sha256": "5f4594b763bf660f07b44a147e6b2c3873297015ce5ab37eccad54896d88b3ac",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-1/3139ad41d138353151cd398f5d000ad6bf29c1657418485f8ad5e870ca9e4857/20261019T225332-04f9508f19634e91bfffdea3c7d4fd06/outputs/qa.json",
          "sha256": "8808b23eb3b4dbee0cad0ee092f6112685642102f6f1f5a3cf7ebd4055789f58",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-1/3139ad41d138353151cd398f5d000ad6bf29c1657418485f8ad5e870ca9e4857/20261019T225332-04f9508f19634e91bfffdea3c7d4fd06/request.json",
          "sha256": "692544677bb428c8736c9f53e27eec63651eb17244a6e35bf09f07119ee6764a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-1/3139ad41d138353151cd398f5d000ad6bf29c1657418485f8ad5e870ca9e4857/20261019T225332-04f9508f19634e91bfffdea3c7d4fd06/result.json",
          "sha256": "8b788097054b728397f76d52c2bebdc7f00f4eabebaa4665a13a8905af57941c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-1/3139ad41d138353151cd398f5d000ad6bf29c1657418485f8ad5e870ca9e4857/20261019T225332-04f9508f19634e91bfffdea3c7d4fd06/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-1/3139ad41d138353151cd398f5d000ad6bf29c1657418485f8ad5e870ca9e4857/20261019T225332-04f9508f19634e91bfffdea3c7d4fd06/stdout.log",
          "sha256": "2dc2e496a944cd1b762d65c6e20ee78f282cd2df7655aebe132416aaf1910aae",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-2/ea938f68d2c40ad475b43f7c5650e9aef8683878795633c8a8a169af3cdbdf32/20261019T225340-22e3b923aae342f4ac174ebf0d4069ec/outputs/calcite-raft-deposit.blend",
          "sha256": "87857dd15ff0f1aced65b0b7a16e710d59ac4f786db1c7caabb5ebc66ae4e367",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-2/ea938f68d2c40ad475b43f7c5650e9aef8683878795633c8a8a169af3cdbdf32/20261019T225340-22e3b923aae342f4ac174ebf0d4069ec/outputs/calcite-raft-deposit.glb",
          "sha256": "fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-2/ea938f68d2c40ad475b43f7c5650e9aef8683878795633c8a8a169af3cdbdf32/20261019T225340-22e3b923aae342f4ac174ebf0d4069ec/outputs/metadata.json",
          "sha256": "92fe3976c4ac4b8472577601e4e6df25400ff1a33d912995a14123cfed461d70",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-2/ea938f68d2c40ad475b43f7c5650e9aef8683878795633c8a8a169af3cdbdf32/20261019T225340-22e3b923aae342f4ac174ebf0d4069ec/outputs/qa.json",
          "sha256": "c3b56d47cd715415943fb163eb940e88e881ed24c55e02464818e6372a691ad9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-2/ea938f68d2c40ad475b43f7c5650e9aef8683878795633c8a8a169af3cdbdf32/20261019T225340-22e3b923aae342f4ac174ebf0d4069ec/request.json",
          "sha256": "4260efec8a117e677f626d03c0697bbcb30c86892b42d3eda08f631b4a847946",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-2/ea938f68d2c40ad475b43f7c5650e9aef8683878795633c8a8a169af3cdbdf32/20261019T225340-22e3b923aae342f4ac174ebf0d4069ec/result.json",
          "sha256": "a1b506ba9083e48c1aaa6f87c48f645f75e4f0f0b7cd4914931f3838906a79f6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-2/ea938f68d2c40ad475b43f7c5650e9aef8683878795633c8a8a169af3cdbdf32/20261019T225340-22e3b923aae342f4ac174ebf0d4069ec/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/build/calcite-raft-deposit/r002/rebuild-2/ea938f68d2c40ad475b43f7c5650e9aef8683878795633c8a8a169af3cdbdf32/20261019T225340-22e3b923aae342f4ac174ebf0d4069ec/stdout.log",
          "sha256": "f14607682f1dc9176de9d3d475b8b949782ca17e121e7b6c91ca9db0e409aa36",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/runs/20261019T225331-6790cd4081804ec9a7f94194f38d5c27/manifest.json",
          "sha256": "603d6ea65afe8d1b309c90e5d9e6eb8ca4019340c5d01cd197be37afbdb5ed3c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/rebuild-runs/runs/20261019T225331-6790cd4081804ec9a7f94194f38d5c27/summary.json",
          "sha256": "ee2fbaa5ce241ed414e9ec43453945b666966feea2cadcc3c8534d92bbdfeb64",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/references.json",
          "sha256": "5213a445fa920c25af8cea7a065e0f9f80195adaf6ee93bda455d490582bca19",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/build/calcite-raft-deposit/r002/build-original/754251ee5ccde57c321d2a8cdb2066d6d617a90b1809273326e558c32b2403ee/20261019T225223-18fd8be5fd4b4028ac6d4fc85f7a4bbd/outputs/calcite-raft-deposit.blend",
          "sha256": "2a3226cbe8048b49554a40e87d0ac13a8bc7804be0f009d27824a979e42f4392",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/build/calcite-raft-deposit/r002/build-original/754251ee5ccde57c321d2a8cdb2066d6d617a90b1809273326e558c32b2403ee/20261019T225223-18fd8be5fd4b4028ac6d4fc85f7a4bbd/outputs/calcite-raft-deposit.glb",
          "sha256": "fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/build/calcite-raft-deposit/r002/build-original/754251ee5ccde57c321d2a8cdb2066d6d617a90b1809273326e558c32b2403ee/20261019T225223-18fd8be5fd4b4028ac6d4fc85f7a4bbd/outputs/metadata.json",
          "sha256": "52ec3eab4f7490fc28a86d2b892da06792c30ef9e89c91b7aad1269c594e2773",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/build/calcite-raft-deposit/r002/build-original/754251ee5ccde57c321d2a8cdb2066d6d617a90b1809273326e558c32b2403ee/20261019T225223-18fd8be5fd4b4028ac6d4fc85f7a4bbd/outputs/qa.json",
          "sha256": "89c16cd03dc9e1e0692883f882fde62567faa96e8956654089d39258df266faf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/build/calcite-raft-deposit/r002/build-original/754251ee5ccde57c321d2a8cdb2066d6d617a90b1809273326e558c32b2403ee/20261019T225223-18fd8be5fd4b4028ac6d4fc85f7a4bbd/request.json",
          "sha256": "1bf001b3ff94a0f8e3f42aab85a12e73a1ac51c3e5bd8285d377b4f6e80e8de3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/build/calcite-raft-deposit/r002/build-original/754251ee5ccde57c321d2a8cdb2066d6d617a90b1809273326e558c32b2403ee/20261019T225223-18fd8be5fd4b4028ac6d4fc85f7a4bbd/result.json",
          "sha256": "c7570f888353ecdef4f05f5f82888fc8ea60f697f9bc315ee79a82df1542a16c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/build/calcite-raft-deposit/r002/build-original/754251ee5ccde57c321d2a8cdb2066d6d617a90b1809273326e558c32b2403ee/20261019T225223-18fd8be5fd4b4028ac6d4fc85f7a4bbd/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/build/calcite-raft-deposit/r002/build-original/754251ee5ccde57c321d2a8cdb2066d6d617a90b1809273326e558c32b2403ee/20261019T225223-18fd8be5fd4b4028ac6d4fc85f7a4bbd/stdout.log",
          "sha256": "c0e52a87ec715cb913f96bff7143718cf49df7d576003707e70d7b765bd1fac2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/runs/20261019T225223-8944529d2bf341e097255432f38d4633/manifest.json",
          "sha256": "c33291aac9c2b4ff2387c040acd19635305c834fafbcd1b618f2041be0f797d6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/calcite-raft-deposit/r002/runs/runs/20261019T225223-8944529d2bf341e097255432f38d4633/summary.json",
          "sha256": "41e3d7ec7d4047892f8c963cd1aeec96a3fe20e7b2e44ed3dd6b26b98d1c0a1c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/claim.json",
          "sha256": "b04981571a1f89687779edb80cfcd1d34b790cf2645abb2153736aac5c45fa2b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/concept-plan-requirements.json",
          "sha256": "3391897e1d6b5d2dcd4fb37dff19344e181e7dc9863d860d4ab4776bae4db7cf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/brief.json",
          "sha256": "de200ddd48b79454f39b265b20fc7cdd4f4cef1030e0445bec0590dd1045ed4a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/build-config.json",
          "sha256": "ac67eb8c2ad7b7b406bd155250d071115084b5a693a2efb95c24bb1580a34ce1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/build-jobs.json",
          "sha256": "ea5d06a90263f05582cc235109c6d5e9fe8cb6c38e5b22389d5ee5dd8b50d400",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/concept-brief.md",
          "sha256": "f7bb38bf08fa65063d934c09e598abbe04b7da1a590c48e70d636f60b1c8b13d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/concepts/generation-record.json",
          "sha256": "cc4f61f51da06042f807fe3b35dc42bad7e3aa98bc4f26879edfaf082936cb35",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/concepts/inspection.json",
          "sha256": "dbbf2f629930fd4cbb30785401a81e7137eca5000c7f238d302cb2157ff41a9b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/concepts/original.png",
          "sha256": "7c2cb8dd3ba7578ffe702e2818b2cc33abb6ec6a297b31c08895dd9654a80585",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/concepts/prompt.txt",
          "sha256": "042d1697a08baa8659c3a5b0eda1f8b45f55d2b44050d17a0bb097abbfacf2c9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/derived-freeze.json",
          "sha256": "b6024b20d35e58c3296f8e8f1d1cdb559aefcd531d50efad6cf7c2e51c71a9a0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/generator.py",
          "sha256": "7128a119466d57120bf2f5635618a510dbecc4b36693d95f113e4709d22bd418",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/model-start.json",
          "sha256": "32ff01a353b97a0b0a6c543797217987e7ca4c178dc114d346c62a7fedf75f50",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-jobs.json",
          "sha256": "aac8b7833d78b702789c23ed9bd7c311952a845ae14ef5ad60e7f49fdd25b008",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-1/106acbae40d752ea9accb499609dceec6bee289379c5ae153e30943d8bb748a9/20261019T225936-ea8142698d8d4fcf91a96057e669263d/outputs/conichnus-conical-burrow.blend",
          "sha256": "32cb10c0a15e2e811ac721208a7093030bf515a883e97f900a6142fa9210f6ea",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-1/106acbae40d752ea9accb499609dceec6bee289379c5ae153e30943d8bb748a9/20261019T225936-ea8142698d8d4fcf91a96057e669263d/outputs/conichnus-conical-burrow.glb",
          "sha256": "34948b0738264195544dd24ff377a1b0f3b92a93a1e34ab07d66647235388042",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-1/106acbae40d752ea9accb499609dceec6bee289379c5ae153e30943d8bb748a9/20261019T225936-ea8142698d8d4fcf91a96057e669263d/outputs/metadata.json",
          "sha256": "c5729dca8c61a18b6cafd0460462b98522fa338fa816a0ea50b5ac5f26a5d0ff",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-1/106acbae40d752ea9accb499609dceec6bee289379c5ae153e30943d8bb748a9/20261019T225936-ea8142698d8d4fcf91a96057e669263d/outputs/qa.json",
          "sha256": "f9a8890166d1daa9a42d7814dd349710cbffe9ec6c07ff2f832247970efe6bb2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-1/106acbae40d752ea9accb499609dceec6bee289379c5ae153e30943d8bb748a9/20261019T225936-ea8142698d8d4fcf91a96057e669263d/request.json",
          "sha256": "529bd5fef3814cd4a229fbc09da19a18abd8d5212a46254827417f871ef64c91",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-1/106acbae40d752ea9accb499609dceec6bee289379c5ae153e30943d8bb748a9/20261019T225936-ea8142698d8d4fcf91a96057e669263d/result.json",
          "sha256": "cd28c8fd278f488b65dfc8579ec12d2e7ade07e4aca96ac0028c28d07fbfeaac",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-1/106acbae40d752ea9accb499609dceec6bee289379c5ae153e30943d8bb748a9/20261019T225936-ea8142698d8d4fcf91a96057e669263d/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-1/106acbae40d752ea9accb499609dceec6bee289379c5ae153e30943d8bb748a9/20261019T225936-ea8142698d8d4fcf91a96057e669263d/stdout.log",
          "sha256": "5ff29b1ecd40a9f4f849ed9f5b053d0caebece7698d5458639a21ebe8534a294",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-2/43ea0ed0085859efca00ffe91889864ab10f8dd07768e99da209d2649f8ea08f/20261019T225945-71e25d2fb66b4172abd009c15ea828e4/outputs/conichnus-conical-burrow.blend",
          "sha256": "9c12a50359320178e37809e894d433a5c44eefb9117e21123f4541685536f59c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-2/43ea0ed0085859efca00ffe91889864ab10f8dd07768e99da209d2649f8ea08f/20261019T225945-71e25d2fb66b4172abd009c15ea828e4/outputs/conichnus-conical-burrow.glb",
          "sha256": "34948b0738264195544dd24ff377a1b0f3b92a93a1e34ab07d66647235388042",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-2/43ea0ed0085859efca00ffe91889864ab10f8dd07768e99da209d2649f8ea08f/20261019T225945-71e25d2fb66b4172abd009c15ea828e4/outputs/metadata.json",
          "sha256": "61a3ecd91c3603c9628ce3bb0c65f60c1f7e1d9ce3eab9f352100b02c964ce80",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-2/43ea0ed0085859efca00ffe91889864ab10f8dd07768e99da209d2649f8ea08f/20261019T225945-71e25d2fb66b4172abd009c15ea828e4/outputs/qa.json",
          "sha256": "dc7e32589bf49f7caa782020488c729caa0aab9e709fd7efcbd4146a99b48b76",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-2/43ea0ed0085859efca00ffe91889864ab10f8dd07768e99da209d2649f8ea08f/20261019T225945-71e25d2fb66b4172abd009c15ea828e4/request.json",
          "sha256": "da7db9b95ba54d741be50a33949cd2c34fbbbfcb211756b323a870b45aaf50f2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-2/43ea0ed0085859efca00ffe91889864ab10f8dd07768e99da209d2649f8ea08f/20261019T225945-71e25d2fb66b4172abd009c15ea828e4/result.json",
          "sha256": "95ae78b9569ef4ce133ffec9f9a0a62255f5ce75eb6ade838d842206e4ff172f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-2/43ea0ed0085859efca00ffe91889864ab10f8dd07768e99da209d2649f8ea08f/20261019T225945-71e25d2fb66b4172abd009c15ea828e4/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/build/conichnus-conical-burrow/r001/rebuild-2/43ea0ed0085859efca00ffe91889864ab10f8dd07768e99da209d2649f8ea08f/20261019T225945-71e25d2fb66b4172abd009c15ea828e4/stdout.log",
          "sha256": "0f861088e27657c8b7708c1896ad73767ff1a5f6b78b3b211783ee1735ef9901",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/runs/20261019T225935-dde309738c794662b22990523402c096/manifest.json",
          "sha256": "96bbbbe238b708e113c9795fafaeb715f074e8c03cf7d631f9a1e3eb898d17fe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/rebuild-runs/runs/20261019T225935-dde309738c794662b22990523402c096/summary.json",
          "sha256": "4b3bdec97c17c5bb8588b2dc05611672de7995fffe612555ae646626c3c318cb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/references.json",
          "sha256": "730d3eb206ee0033122a50a8beae6a7289463e82b013f6fa914610608f69f160",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/build/conichnus-conical-burrow/r001/build-original/aad9aa0fe1996101e7b595c75aab3dd9c3b508c85c6345aaae104b6c978f6e27/20261019T225833-3ab992ac800c4a5c9a23db602a850045/outputs/conichnus-conical-burrow.blend",
          "sha256": "4bb156af41158e9c2c899e0b55efdb0cb0e005ddf83cb7af46841e876388d121",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/build/conichnus-conical-burrow/r001/build-original/aad9aa0fe1996101e7b595c75aab3dd9c3b508c85c6345aaae104b6c978f6e27/20261019T225833-3ab992ac800c4a5c9a23db602a850045/outputs/conichnus-conical-burrow.glb",
          "sha256": "34948b0738264195544dd24ff377a1b0f3b92a93a1e34ab07d66647235388042",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/build/conichnus-conical-burrow/r001/build-original/aad9aa0fe1996101e7b595c75aab3dd9c3b508c85c6345aaae104b6c978f6e27/20261019T225833-3ab992ac800c4a5c9a23db602a850045/outputs/metadata.json",
          "sha256": "fdce4944a45fb5e44dd5d05a42afe0eaca59e65a4ff60e0db038f64715629630",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/build/conichnus-conical-burrow/r001/build-original/aad9aa0fe1996101e7b595c75aab3dd9c3b508c85c6345aaae104b6c978f6e27/20261019T225833-3ab992ac800c4a5c9a23db602a850045/outputs/qa.json",
          "sha256": "5b5e07c2f2b36381c4393accb69f11e9d8f9b96f4bf340b98273929aa693f45b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/build/conichnus-conical-burrow/r001/build-original/aad9aa0fe1996101e7b595c75aab3dd9c3b508c85c6345aaae104b6c978f6e27/20261019T225833-3ab992ac800c4a5c9a23db602a850045/request.json",
          "sha256": "8a5a4a2ba45101be8082fc7d1c7f7d0ff90c79f09d15e412aa560fcec9cca2da",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/build/conichnus-conical-burrow/r001/build-original/aad9aa0fe1996101e7b595c75aab3dd9c3b508c85c6345aaae104b6c978f6e27/20261019T225833-3ab992ac800c4a5c9a23db602a850045/result.json",
          "sha256": "1972a7c35af67b0346311af768cfc18ad8c09d07f436ee7dbda7c4c164aab0f6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/build/conichnus-conical-burrow/r001/build-original/aad9aa0fe1996101e7b595c75aab3dd9c3b508c85c6345aaae104b6c978f6e27/20261019T225833-3ab992ac800c4a5c9a23db602a850045/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/build/conichnus-conical-burrow/r001/build-original/aad9aa0fe1996101e7b595c75aab3dd9c3b508c85c6345aaae104b6c978f6e27/20261019T225833-3ab992ac800c4a5c9a23db602a850045/stdout.log",
          "sha256": "00382811c474ba93fd571a89337c1228425e9088b7df64185f0d5bf4473790f3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/runs/20261019T225832-f47c33df98674be2bf7a92a405a880c0/manifest.json",
          "sha256": "88a74b1861d224bfd6f09d03131ef4c74baae5ea668041f659bdb45f7e3258c7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/conichnus-conical-burrow/r001/runs/runs/20261019T225832-f47c33df98674be2bf7a92a405a880c0/summary.json",
          "sha256": "ee6078c9f7406bc2e56a79b23bbad46d06585ddcef0d8ac5512d85f3a8991708",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/brief.json",
          "sha256": "ac8a307da9938c7f52eb72a88e2922c83a93ced204edc024e341075b27dc3f97",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/build-config.json",
          "sha256": "fa5c836f1e391a0269c1504a77e25acc80daada4f76a2e16b4553828caccf4a8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/build-jobs.json",
          "sha256": "01d70c8bf7446b4c045d5aa42678e71957f8ebd0d1574ed40c52cf40f92fba15",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/concept-brief.md",
          "sha256": "9cfb046e45f724c80d2cd779f95d7ae6315655cb13b8e1af9829bef7cd339f39",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/concepts/generation-record.json",
          "sha256": "f02b82839b4e75d5e75ccb15a2abec65e10087c09892a73626905f0eb38b33f6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/concepts/inspection.json",
          "sha256": "29bb8bfbb83b4e7c95d883fee65e00c9e296076b0f613748977dc70184d2e509",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/concepts/original.png",
          "sha256": "a8c8eaf0df9efe39148dc92ac980a5f2d64fd34c529cf4e94166be83f3055932",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/concepts/prompt.txt",
          "sha256": "fc60cd3f52ac7d9ce946fd4d8be0e940874aac511fe19781f154315165999705",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/derived-freeze.json",
          "sha256": "afaa7c065723f8a45af3d3b568409e7d03339c57057b0c1e5e82dd8108e9ca50",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/generator.py",
          "sha256": "d844d9c6ad4870d31e49821f387b6f266e5559b00669287734c3ad8d4c3811bc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/model-start.json",
          "sha256": "518bd524263c476e89cf5fbe12ccd7414f58c20f266967bfec7d8ac5b8a71fc2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-jobs.json",
          "sha256": "cf61694f6cdf39a91e20ab0056dee09044ba98189c5168cc2a8394d7101f822e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-1/146f710969326e28cb9946f8d35f648560df6c9ff990fb2509a4643e459e8cb1/20261019T225028-51c3220611334d4c817ad43301e336ee/outputs/dicranurus.blend",
          "sha256": "953a071293d77bca2c08ce280ab0627a6a6b685f79149d7e47215d539e4702b6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-1/146f710969326e28cb9946f8d35f648560df6c9ff990fb2509a4643e459e8cb1/20261019T225028-51c3220611334d4c817ad43301e336ee/outputs/dicranurus.glb",
          "sha256": "ffe61e0340399eb1bd41cb198ba5abc20edae439db44e3c21d4cf6d9e032bd65",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-1/146f710969326e28cb9946f8d35f648560df6c9ff990fb2509a4643e459e8cb1/20261019T225028-51c3220611334d4c817ad43301e336ee/outputs/metadata.json",
          "sha256": "6d77fcae2aab522adf98c33026cad063ee9b230ea18df271e56c9e80ce3839da",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-1/146f710969326e28cb9946f8d35f648560df6c9ff990fb2509a4643e459e8cb1/20261019T225028-51c3220611334d4c817ad43301e336ee/outputs/qa.json",
          "sha256": "184bc092ccd7abed934a64717d2c14ab5c55a8214b947a2c949d830f46d65f64",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-1/146f710969326e28cb9946f8d35f648560df6c9ff990fb2509a4643e459e8cb1/20261019T225028-51c3220611334d4c817ad43301e336ee/request.json",
          "sha256": "5ab9ff29d4d5bde270eced5667213f8ea49ddb26bd3af7cdcb4d2ee8728253b9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-1/146f710969326e28cb9946f8d35f648560df6c9ff990fb2509a4643e459e8cb1/20261019T225028-51c3220611334d4c817ad43301e336ee/result.json",
          "sha256": "df004eb6eebc50278bf8d81041f951a920b91ad79670d659c7b699281a14d015",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-1/146f710969326e28cb9946f8d35f648560df6c9ff990fb2509a4643e459e8cb1/20261019T225028-51c3220611334d4c817ad43301e336ee/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-1/146f710969326e28cb9946f8d35f648560df6c9ff990fb2509a4643e459e8cb1/20261019T225028-51c3220611334d4c817ad43301e336ee/stdout.log",
          "sha256": "4734952ceece6eddf0fcfffb34ed4bc93ef1d4dbc965d56e4798517d91282635",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-2/34d350ea6eee4b1796804807cb95ee89a776bebac7f59ed4afc3617f36d8eae7/20261019T225036-dacc700773874c6aa99e737303c8d423/outputs/dicranurus.blend",
          "sha256": "bac246cd4d7b2d5a01ba78b3178352fd8e9e69a3c2b99882851e613321c89870",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-2/34d350ea6eee4b1796804807cb95ee89a776bebac7f59ed4afc3617f36d8eae7/20261019T225036-dacc700773874c6aa99e737303c8d423/outputs/dicranurus.glb",
          "sha256": "ffe61e0340399eb1bd41cb198ba5abc20edae439db44e3c21d4cf6d9e032bd65",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-2/34d350ea6eee4b1796804807cb95ee89a776bebac7f59ed4afc3617f36d8eae7/20261019T225036-dacc700773874c6aa99e737303c8d423/outputs/metadata.json",
          "sha256": "b5702dd3ab3276abe43b7fce705c34cc0736566adcf49df6fd1269702d436b5e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-2/34d350ea6eee4b1796804807cb95ee89a776bebac7f59ed4afc3617f36d8eae7/20261019T225036-dacc700773874c6aa99e737303c8d423/outputs/qa.json",
          "sha256": "ac6585cd79a6a4ea0cf992d8723cfc39f98d376d782f0a5ff63a448a456e1ab9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-2/34d350ea6eee4b1796804807cb95ee89a776bebac7f59ed4afc3617f36d8eae7/20261019T225036-dacc700773874c6aa99e737303c8d423/request.json",
          "sha256": "0f97245626e8124c224436126036f5916e54dc4758e5db70b458f378820b78d8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-2/34d350ea6eee4b1796804807cb95ee89a776bebac7f59ed4afc3617f36d8eae7/20261019T225036-dacc700773874c6aa99e737303c8d423/result.json",
          "sha256": "8d613e83dc741229e6b03ecb291f5ad1554e0cbc492b2383907d129dfd88059c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-2/34d350ea6eee4b1796804807cb95ee89a776bebac7f59ed4afc3617f36d8eae7/20261019T225036-dacc700773874c6aa99e737303c8d423/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/build/dicranurus/r001/rebuild-2/34d350ea6eee4b1796804807cb95ee89a776bebac7f59ed4afc3617f36d8eae7/20261019T225036-dacc700773874c6aa99e737303c8d423/stdout.log",
          "sha256": "3d2626f0fc6626460274e3514a584017024194a4b33ffd00f9cec6df8cdbb034",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/runs/20261019T225027-57460528828a4c8bb8fa8d797c6dd845/manifest.json",
          "sha256": "43a94f04275b14b3b6a2025c26104330f9079a6bb2d712650c093c65880637b1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/rebuild-runs/runs/20261019T225027-57460528828a4c8bb8fa8d797c6dd845/summary.json",
          "sha256": "adc3027d29d648abb5410e010d51037f72e60a742bc42b1c2c5ae0e8e6813828",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/references.json",
          "sha256": "c6b75ad597c5228bbaa49d34f6ca5bdf61f89667db7f50b468454c6308df4e69",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/build/dicranurus/r001/build-original/78bf6b9e53e0d38e42aaf3f1e428cfcad671ea75876bf1097f2304eeecf7b5d2/20261019T224901-7d4a1e06b3ec4cb0ab95b25afd888754/outputs/dicranurus.blend",
          "sha256": "a38846c7822b375f763f5ec71a2483261553845d03ade6355e84335929a7b3ab",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/build/dicranurus/r001/build-original/78bf6b9e53e0d38e42aaf3f1e428cfcad671ea75876bf1097f2304eeecf7b5d2/20261019T224901-7d4a1e06b3ec4cb0ab95b25afd888754/outputs/dicranurus.glb",
          "sha256": "ffe61e0340399eb1bd41cb198ba5abc20edae439db44e3c21d4cf6d9e032bd65",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/build/dicranurus/r001/build-original/78bf6b9e53e0d38e42aaf3f1e428cfcad671ea75876bf1097f2304eeecf7b5d2/20261019T224901-7d4a1e06b3ec4cb0ab95b25afd888754/outputs/metadata.json",
          "sha256": "b14402c555a193706029fbe38b3036cf472c8380fafd64bbf9bcf495b5e42f6d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/build/dicranurus/r001/build-original/78bf6b9e53e0d38e42aaf3f1e428cfcad671ea75876bf1097f2304eeecf7b5d2/20261019T224901-7d4a1e06b3ec4cb0ab95b25afd888754/outputs/qa.json",
          "sha256": "40fd8d72fa132c42368ea5872868f4d03676162856bd18ddbaf53e028bc874a6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/build/dicranurus/r001/build-original/78bf6b9e53e0d38e42aaf3f1e428cfcad671ea75876bf1097f2304eeecf7b5d2/20261019T224901-7d4a1e06b3ec4cb0ab95b25afd888754/request.json",
          "sha256": "5f4f108cfe674d41efb2aeb6bda40d3d168bfa6c11ea5e848072d02dda83b3ed",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/build/dicranurus/r001/build-original/78bf6b9e53e0d38e42aaf3f1e428cfcad671ea75876bf1097f2304eeecf7b5d2/20261019T224901-7d4a1e06b3ec4cb0ab95b25afd888754/result.json",
          "sha256": "a1a2850d7e5a66221d1e8b5d021aa023536c9cb8425c776a5d9038be9062a9d4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/build/dicranurus/r001/build-original/78bf6b9e53e0d38e42aaf3f1e428cfcad671ea75876bf1097f2304eeecf7b5d2/20261019T224901-7d4a1e06b3ec4cb0ab95b25afd888754/stderr.log",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/build/dicranurus/r001/build-original/78bf6b9e53e0d38e42aaf3f1e428cfcad671ea75876bf1097f2304eeecf7b5d2/20261019T224901-7d4a1e06b3ec4cb0ab95b25afd888754/stdout.log",
          "sha256": "1e414e27a45645ab9ae1b7f45bc2a7057d63c5aa531eddb0739ace29747c036a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/runs/20261019T224900-d349fdde402749ddac4ba351be7acfce/manifest.json",
          "sha256": "888f4c3a5a0fa4be1165c1baf97e48d4608dd11a25aec7f560882bd1c6fec9c1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/dicranurus/r001/runs/runs/20261019T224900-d349fdde402749ddac4ba351be7acfce/summary.json",
          "sha256": "6d5129810a683b45dcc8e91fd16c2b722dbf89688ee7588f9190f0e5afd320ee",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/environment-status.json",
          "sha256": "5a846ca7c58c0d55a006c7bd3d7965790971cf94c55cdda4658347805b1b170e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/original-input-integrity.json",
          "sha256": "4aaafa2007c4bd61cbf3a1efefe2da540e442f5dfcae5552a7fbcb4db41bdbc7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/preclaim-dedup.json",
          "sha256": "7396bbc3fa31e42288b76c998e58172b2ceea614c84c2e08c60a7d0807461f14",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/README.md",
          "sha256": "021f24128623ce612abfae703ebb102adea883ac58294fbc1527f79915dd3b08",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/accretionary-lapilli-bed/brief.json",
          "sha256": "2afd0c8533c79dd19fae2e28f189ffb800dd14f517dcc5a8eacc707ea9a794df",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/accretionary-lapilli-bed/derived-freeze.json",
          "sha256": "8fdc51883d45a70c1f6d7405f7ba464901f81d6f089fc7b13dfbadd9f1160d5e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/accretionary-lapilli-bed/fresh-static-glb-report.json",
          "sha256": "1be153d079a8238483847bc649dc90776bce5680d93b508d70b148f755be7930",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/accretionary-lapilli-bed/metadata.json",
          "sha256": "3664df66f4ec3ef9d451fbe6dc25045d04b5dcd83bd9439c78e3ec5909053dd0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/baseline-original-verification.json",
          "sha256": "87a79b6217ff475d3459ae1a25cb11803c0e55f3e2667c3bbc86ff16a7f37876",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/calcite-raft-deposit/brief.json",
          "sha256": "6c7f519dfc5357bf489969f2d4e1a031559d7b92ac5b313baa71c0b72a45f303",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/calcite-raft-deposit/derived-freeze.json",
          "sha256": "5175cf3c192bae32d4e87df08043cd04c138ddf35e01122a7d52036608b48388",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/calcite-raft-deposit/fresh-static-glb-report.json",
          "sha256": "99c044832d33ff3adb484110e11e6efea8e324a9c38ff9874d536df3d0f6942c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/calcite-raft-deposit/metadata.json",
          "sha256": "b64118b161f0cf373613e53fc8cc3f5068587f606e5a4d39f5475b930b345eaa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/historical-handoff/HANDOFF.md",
          "sha256": "2cae7159754160ce3b8b59c288d769d1733341947a1be68b100b8842dd13d13c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/historical-handoff/QA-HANDOFF.json",
          "sha256": "3001dbd918be6cd05ce2cf82a7e94a99cf92f3892e1b9b88e643dc7bfd1308a9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/index.json",
          "sha256": "e8d2c00dcee9222b95db16d4630c1aeae14753148f22bbb3615373aecb581616",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/preserved-original-files.json",
          "sha256": "354f59ca7664e11ce62d4fcac174533919546556e2d6a6cd7bd7fce99f7f5c3e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/regression-tests.log",
          "sha256": "8523ede0172a1a08e0e8e5a023dbd553ed6870c2a3a7706fac7b813249c4119d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/verification.json",
          "sha256": "fc362bb8d9d31c1b5aea2ccd7284528635c97dae832c13ed84ccbf3391f84fdf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/specification-correction-v001/verify_correction.py",
          "sha256": "9ff0634433351b3e5d36f4f7f6762a3ff2627e379d2b3138d384989659922016",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/build_lifecycle.py",
          "sha256": "9b1173993534cdf54065653873864383a83cec2389c7c1f8673c3c4426428076",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/conichnus_diagnostics.py",
          "sha256": "3817b87023a5d69110b236e4e0028a00220a3e3ae58c306725a71ca6a8384b1b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/finalize_candidate.py",
          "sha256": "4534487ffb06a775100aa1e282242660ae29a540444e0523e2f3466e1e18688e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/generator.py",
          "sha256": "7128a119466d57120bf2f5635618a510dbecc4b36693d95f113e4709d22bd418",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/measure_sources.py",
          "sha256": "03890b5c7e205a742386c753be32f4cbb05d3ea9f3336861a7f1b7058134fb9d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/prepare_candidate.py",
          "sha256": "8d01c1c3b81a0a4b3ab56f55fce7381f088b2fea918ef7f4fd16c2d72e29cf3d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/render_views-v001.py",
          "sha256": "678b0c222409e7bb8b5688436cee21134fe3e55868b7dc1d3306dc9db9ff92a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/render_views-v002.py",
          "sha256": "2e47bdcfc2fb1e928f3db32fd2e8baf7fcb76c24014286d554af3fe410f17009",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/render_views.py",
          "sha256": "411f6e4a51a16329ca33730fbdbfdf86232fadb573f611563ad72b94b7e6fc0c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/runtime.mjs",
          "sha256": "466a7bc48cf9f062c75bbe25da5f0ef1f9280cb6ef872983e2723b2ccdbdbd2b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round17-20261018/work/batch-51/tools/technical_lifecycle.py",
          "sha256": "3668a75a808e8c69e520482da76de9dc15be3cb240dd59eda845f72ebf1d57d4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/build_results.py",
          "sha256": "b96b48ef9a3f64e5b131b65c7fcfa6405d7fb36df28686840478e732a7f8a2e4",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/README.md",
          "sha256": "b9b17fba41a5e4d1ac85bd00fa3fb7e8f418815c4cc03c82f07c16026940fe71",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/blender-source-export/accretionary-lapilli-bed.json",
          "sha256": "3a45a24e40edc3b35e7a769f05cb62e2b8fc1efe737eb1c917f9e5c8ee1f6fac",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/blender-source-export/accretionary-lapilli-bed.stdout.txt",
          "sha256": "8fcfc73293ed8d458fdd23ef4f15c0e8f1b5d61878e11be9bc06f5b43135886a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/blender-source-export/calcite-raft-deposit.json",
          "sha256": "26567da370f9b923ca454cbbbb2957e4b44d7060805afe5ec135a40e0a507d2c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/blender-source-export/calcite-raft-deposit.stdout.txt",
          "sha256": "48041fe31c7d2a6ba1641ec6d3d604f5ec16c1ac80d2be9865bd6e3f729d66b8",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/blender-source-export/conichnus-conical-burrow.json",
          "sha256": "2298198974ce06630c1475893bfb9173c0dc8040dc75e25d0d60b5e963b8b2b5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/blender-source-export/conichnus-conical-burrow.stdout.txt",
          "sha256": "abee70af2e72b99f347ca2c1e8400fcde5dc7d4bb89a6e0c91f93de286e6ef7a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/blender-source-export/dicranurus.json",
          "sha256": "7be79370a0a756aba3904d59ec86f08a610c6f71134dd8626690cca7dd733228",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/blender-source-export/dicranurus.stdout.txt",
          "sha256": "7bc56a822699875ea98cd4c476a95e1fb46f32be314d31bb00b0d8432c9559ac",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/accretionary-lapilli-bed-candidate-integrity.json",
          "sha256": "86552351278aae2771ebfc8c06b0a4adfed6e74952adfa80f81ba04b95a935c7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/accretionary-lapilli-bed-candidate-integrity.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/accretionary-lapilli-bed-concept-require-complete.json",
          "sha256": "dd10cfc0ed5147ed7db06de7c4dafb43d23c6f0ef07921e2849ab4fa86ffaca5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/accretionary-lapilli-bed-concept-require-complete.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/accretionary-lapilli-bed-require-approved.json",
          "sha256": "86552351278aae2771ebfc8c06b0a4adfed6e74952adfa80f81ba04b95a935c7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/accretionary-lapilli-bed-require-approved.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/calcite-raft-deposit-candidate-integrity.json",
          "sha256": "042fd00f4faa9b4887fe5ec28f8473e9ad28546298a439f9639fbd7b4529a0be",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/calcite-raft-deposit-candidate-integrity.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/calcite-raft-deposit-concept-require-complete.json",
          "sha256": "2e46ed77b38e1c50962fc12734a933e52fbb8cb48c1ea4b5b1da1db03902796f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/calcite-raft-deposit-concept-require-complete.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/calcite-raft-deposit-require-approved.json",
          "sha256": "042fd00f4faa9b4887fe5ec28f8473e9ad28546298a439f9639fbd7b4529a0be",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/calcite-raft-deposit-require-approved.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/conichnus-conical-burrow-candidate-integrity.json",
          "sha256": "6bd1caecd4f680033740e8bf9cb356ac911e970eee08400725eba252bd70b501",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/conichnus-conical-burrow-candidate-integrity.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/conichnus-conical-burrow-concept-require-complete.json",
          "sha256": "cb64eb7412eede623cc2a7232ff61b164ae752ccd955e411490dcdd11d3baac1",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/conichnus-conical-burrow-concept-require-complete.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/conichnus-conical-burrow-require-approved.json",
          "sha256": "6bd1caecd4f680033740e8bf9cb356ac911e970eee08400725eba252bd70b501",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/conichnus-conical-burrow-require-approved.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/dicranurus-candidate-integrity.json",
          "sha256": "3137134329dda0f8d00dd4ce5eb11ee5d106df66e91162c2df2de16b7511221e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/dicranurus-candidate-integrity.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/dicranurus-concept-require-complete.json",
          "sha256": "52b2c5eeff598016e97dd7b9dd18a99ba2a4a1ffb1602adfd697b64f5a2e1529",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/dicranurus-concept-require-complete.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/dicranurus-require-approved.json",
          "sha256": "3137134329dda0f8d00dd4ce5eb11ee5d106df66e91162c2df2de16b7511221e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/dicranurus-require-approved.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/candidate-checks/exit-codes.json",
          "sha256": "af8e7c77e014acdac82fa50d2085060c0ff7237f23b9ef0f74ce3d6c1c1778b9",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/conichnus/independent-raycast.stdout.txt",
          "sha256": "7354b82d4b71abeabb8265eca025b7a5a3729ca25e2fa46c7ec2260290159fbd",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/conichnus/maker-diagnostic-manifest.json",
          "sha256": "69d373194dfc80a8a0f28caf27ffb8ab2de5214e1548281fc7ddcffe0136775e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/conichnus/maker-negative-cavity-probe.json",
          "sha256": "8dac9e6240bb4017693d6dd3bc21de9d478d0113e665bf5aa39ecde51d87d15c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/accretionary-lapilli-bed/gltf-validator.report.json",
          "sha256": "44f459ab4d0d4a0b02e5c0d7ee630c0b811a0334d81334935f8d4e8b20a88e92",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/accretionary-lapilli-bed/qa.json",
          "sha256": "c9df6079418af235273ef6884c5ddd27f6d5f1be911bbcda1d7a3aa63863e51b",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/accretionary-lapilli-bed/stdout.txt",
          "sha256": "87d33d1f123c9416101420c09c228572de580cfbb7bafa871ee6dab5660423e7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/calcite-raft-deposit/gltf-validator.report.json",
          "sha256": "ae3b512757ef07ac1cdf9bcf638dc56b69c9791d37178f67bc00655b5c3ed4df",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/calcite-raft-deposit/qa.json",
          "sha256": "36181a9b41497e1ff5ff73b19f1d61e3eb270151e5e3245793e5eb24a911b044",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/calcite-raft-deposit/stdout.txt",
          "sha256": "5247b5d2f1547db4337b8bbdc6a2e791041464f3b870112fd498266713d05016",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/conichnus-conical-burrow/gltf-validator.report.json",
          "sha256": "efcac7057a9e24b5e256c4b0ffbdd7f7d6079083c6d8dfa23fe0074961b9e4ea",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/conichnus-conical-burrow/qa.json",
          "sha256": "d9d706b9a4a3a37d4adb7d7733f4653346eb6fb95a042d0f4b4ab73ff7d42c77",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/conichnus-conical-burrow/stdout.txt",
          "sha256": "de0954193101323dd8939531224ca7e61e6a025842978c4e104247168a3ab839",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/dicranurus/gltf-validator.report.json",
          "sha256": "ad8c97f7a583fcb473ac3dfd4cb909fb135d9c218af87dcba10ffd83d18a9396",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/dicranurus/qa.json",
          "sha256": "bacd062c6bdca46f6034b3f3488961fe051c1cdc43d4a31eec459743c6f525cf",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/khronos/dicranurus/stdout.txt",
          "sha256": "05f414c2a72dec82ce5b24330da3657e2531976988ab0ee87f2a7d911f6d8cf7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/probe_negative_cavity.py",
          "sha256": "4bcfcd16de69de0ae7eb7e0be43438952b2dd1d8b6bf34a9aa461e64ee7b9d10",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/accretionary-lapilli-bed/independent-runtime-report.json",
          "sha256": "e6b936f511bcf873697d94ab3e50d66360634b2c4a5d9abc276c3088c28436aa",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/accretionary-lapilli-bed/independent-runtime.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/accretionary-lapilli-bed/independent-runtime.stdout.txt",
          "sha256": "9d9731c8ba193b203201aa2c5a01b186461f0db23d60dda9acac164bd89f9fc3",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/calcite-raft-deposit/independent-runtime-report.json",
          "sha256": "4214d4e1377ca84166b0309cf75227ed3dfe1499b047b6728a9358102376ca29",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/calcite-raft-deposit/independent-runtime.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/calcite-raft-deposit/independent-runtime.stdout.txt",
          "sha256": "1262eaaf8a1d64ac9d143ec7cbaa66174c3f5421f7fb39eb51ac8557b3e2bfad",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/conichnus-conical-burrow/independent-runtime-report.json",
          "sha256": "946a2bb9dbbf50140c010c02810e707895b2a0bdff8ad5d4f3c491df112e08e3",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/conichnus-conical-burrow/independent-runtime.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/conichnus-conical-burrow/independent-runtime.stdout.txt",
          "sha256": "92ec907392bbd8ae1140bac1cc2ae386b0683cbcbac4a6b8ee85732f7e5695dc",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/dicranurus/independent-runtime-report.json",
          "sha256": "d69bb0f83bd4b484790add40ec7498ff95d2fd645a34aa35b83159e98b489be0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/dicranurus/independent-runtime.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/dicranurus/independent-runtime.stdout.txt",
          "sha256": "4e0e5e007a1375568a4cb4fdab1a15477c06dee40144468b828cbbc692a113dc",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/replay/runtime/runtime-replay-summary.json",
          "sha256": "afbd4a5620f2dcf77f591ea81a9255058cf8302eae40a3b4ce7f61de3e06a1da",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/results.json",
          "sha256": "b373db93aae4373d761fbfe916999e96def533768fe491deaecf99af93f532f0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/toolchain.json",
          "sha256": "c0bda7b838c0c65770eb48db769324b6cb1803858f617a8b51fb0bc73bd3652b",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/verified-inputs.json",
          "sha256": "87a79b6217ff475d3459ae1a25cb11803c0e55f3e2667c3bbc86ff16a7f37876",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/verify_inputs.py",
          "sha256": "b57dac5ffd4de171af23d47ecc7af6a1755112b1caf6023a00358f764866e6a2",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/report.md",
          "sha256": "6a6c00bbb209702694cb8a0153c6b4b13def0ca5f7d566916cdd4ef7123997d9",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/differential-v001/independent-verification.json",
          "sha256": "1e884e08a25295317846110ae98cdba3f1440667ab7aa57083320a38d48ba197",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/differential-v001/report.md",
          "sha256": "ac8a0dbd4085bf101e9bfb4fd44ff6f06dbdf7be2495a97ad9236a8a336c6f5e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-independent-20261019/evidence/differential-v001/verify_spec_correction.py",
          "sha256": "fd2cde0564dd8c21528ca39d11c44bc078b76a766ae3303c77a402531090c8b1",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/batch51-release-20261020/original-review-925ff855.md",
          "sha256": "f9d3d6bf2499c68f0fae515632eae751b1be30084effad9d3e62f778abb9e18b",
          "origin": "release",
          "owner": "$batch"
        }
      ],
      "original_review_archive": {
        "original_commit": "925ff855ad0fcc3635cfc44a457101344ffddbde",
        "original_path": "qa/batch51-independent-20261019/report.md",
        "original_sha256": "f9d3d6bf2499c68f0fae515632eae751b1be30084effad9d3e62f778abb9e18b",
        "archive_path": "qa/batch51-release-20261020/original-review-925ff855.md"
      }
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/batch55-20261020.json",
      "sha256": "51d31c778ff54f21d00c79a280799d511be4b0de9c64ec11656bb7a382c30ae6"
    },
    "release": {
      "version": 1,
      "scope": "batch55-20261020",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "user_visual_acceptance": "not_established",
      "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1",
      "review_commit": "1cdfab1b0351c61854b5480c8eac012440232fa1",
      "source_bundle": {
        "path": "qa/batch55-release-20261020/source-bundle.json",
        "sha256": "fee960e8aa6e75da56587f6a6e0e1e87c33c54f8ae4940482dd755e2a7d041f4"
      },
      "source_scope_review": {
        "path": "qa/batches51-55-release-20261020/source-scope-review/review-summary.json",
        "sha256": "a7763a1603657d4d3cacb3030853a6f684a88489b606499d6669e041a2e0df54"
      },
      "capture": {
        "report": {
          "path": "qa/batches51-55-release-20261020/capture/render-report.json",
          "sha256": "ecd07698cef1dab39855e806e8e4e6bbfefb09de2eff16d3104152797fb7edb3"
        },
        "index": {
          "path": "qa/batches51-55-release-20261020/capture/assets/turntables/index.json",
          "sha256": "ae819d5845ed6ddd55e084ca0bec92ea11f9d6f799b626dd5a688f3c482e2d2c"
        },
        "provenance": {
          "path": "qa/batches51-55-release-20261020/capture-provenance.json",
          "sha256": "307baa1e131983ca335e3c44b0df8dbe408d80fa4ebc382134fc00476b1c1e03"
        },
        "independent_review": {
          "path": "qa/batches51-55-release-20261020/capture-review/capture-review.json",
          "sha256": "b1262c2f209724149fbf98799cf502cc186db973fd5269d32ca36e8af9503c09"
        }
      },
      "additions": [
        {
          "id": "vermicularia",
          "revision": "r001",
          "metadata": {
            "path": "assets/additions/vermicularia/batch55-20261020/release-metadata.json",
            "sha256": "696752dc29d2960e361168296d432e7c50745e118fa0cb7813ec9923cba84bf1"
          },
          "source_metadata": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/metadata.json",
            "sha256": "499435f6614d4547cab34e47c4c88cd2755c0e30c6fafd0ecb6ac86e01fc1702"
          },
          "candidate": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/candidate.json",
            "sha256": "616b24ff699261111d8ad89feae12f5fb22bdb0117a5234d3aa0c1f93dd9ddd6"
          },
          "artifacts": {
            "glb": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/vermicularia.glb",
              "sha256": "5bb8a455b222496fbe8568184eb2aff11b717aab29bbf42d3138707781b27f7f",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "brief": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/brief.json",
              "sha256": "772239b047fa49aec3129b38853c244e39c6ebd05c43c2e02749a9677e2d9455",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "references": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/references.json",
              "sha256": "85c3ffaf8b67e46ba15a0e8b845d913b473be6f14a3af617af246788ed6514b5",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "source": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/vermicularia.blend",
              "sha256": "328513c8cb5600645ba0f4e2d2a378acea89235039f313021b981698561cb7af",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "generator": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/generator.py",
              "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "config": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/build-config.json",
              "sha256": "32b0cc39c4f82b7b489f013963b0b02f61b45039e3fdcaa0bf7b3823b13eb8fc",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            }
          },
          "packaging_candidate": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001-packaging-v1/candidate.json",
            "sha256": "4a3856d4e81323d77040d8109f098a2656d9aa4233fa0dc4bec30dc984cac481"
          },
          "packaging_brief": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001-packaging-v1/brief.json",
            "sha256": "eb3bd83020e990e3cfffe3ad4510a907d5958f68c47499044a24417d6bf49eaf"
          },
          "poster": {
            "id": "vermicularia",
            "path": "assets/card-previews/vermicularia-v2-768-q90.webp",
            "sha256": "a5738d45964606eb3d5034ef63817afb7395c709028b7b12fef59ebc371cd823",
            "bytes": 9348,
            "width": 768,
            "height": 768,
            "source_glb_sha256": "5bb8a455b222496fbe8568184eb2aff11b717aab29bbf42d3138707781b27f7f",
            "render_preset_sha256": "2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff"
          },
          "capture_reference": {
            "path": "qa/batches51-55-release-20261020/capture/references/vermicularia.png",
            "sha256": "0f1210f16065ea22bc0ff3aa9fff3a59f7c538cfc54afd171939bf192150451a"
          },
          "review": {
            "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/INDEPENDENT-QA.md",
            "sha256": "7321a9c25b1372ee9615e485f441b5ab029bf6a081d76486babca49574e2f66b"
          }
        },
        {
          "id": "weichselia",
          "revision": "r001",
          "metadata": {
            "path": "assets/additions/weichselia/batch55-20261020/release-metadata.json",
            "sha256": "3c063dd9bf99a869d9cfe9f7ae405428de6a911b2c62bd245bf5c11c7a8574fe"
          },
          "source_metadata": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/metadata.json",
            "sha256": "8466cc47b61284d0a1a6f2ef076ca2a6ae6528a05f56562a814fa77994f31043"
          },
          "candidate": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/candidate.json",
            "sha256": "82c0bca150da913fceeccbfb582744d941d70646e89e476d232475b79c3817c9"
          },
          "artifacts": {
            "glb": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/weichselia.glb",
              "sha256": "4ece730443de73b6c2dca2fe2bc7a50517628e344b5e6edd37486901c997676a",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "brief": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/brief.json",
              "sha256": "b48f62878a56e0cc5869d44f660316875b85f7e9b1fb8285b57442ed9cbfe05c",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "references": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/references.json",
              "sha256": "5df07b75b5aec7d47d24a0f72cdfe60b9638e44ef44cd4476cf99f79d982bfac",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "source": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/weichselia.blend",
              "sha256": "a196ad872025a7d25f998798bde442c6654d06ed55564f9bc76f95f9e1e905fd",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "generator": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/generator.py",
              "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "config": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/build-config.json",
              "sha256": "ba83b050bbfa90d02b5843d9ee15ab1070a58813bb55d2f15a253ba99f69dab3",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            }
          },
          "packaging_candidate": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001-packaging-v1/candidate.json",
            "sha256": "05c7513b88c91b04db11f97b55dcddde800da0254c990ff3a20ac31310a8552e"
          },
          "packaging_brief": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001-packaging-v1/brief.json",
            "sha256": "ca06a95a81305d0cb561662e051c52536d0426dcc57783667c4b7f415e96b5b9"
          },
          "poster": {
            "id": "weichselia",
            "path": "assets/card-previews/weichselia-v2-768-q90.webp",
            "sha256": "d6fbc2500edc3f4a703553af3c7403ce5647ef04ac7ebc4131f5c190edddfd91",
            "bytes": 8622,
            "width": 768,
            "height": 768,
            "source_glb_sha256": "4ece730443de73b6c2dca2fe2bc7a50517628e344b5e6edd37486901c997676a",
            "render_preset_sha256": "2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff"
          },
          "capture_reference": {
            "path": "qa/batches51-55-release-20261020/capture/references/weichselia.png",
            "sha256": "037f7be551d3a979e7fa90adddf9ace911f2eed7ae5182d8747c037ad9f0315e"
          },
          "review": {
            "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/INDEPENDENT-QA.md",
            "sha256": "7321a9c25b1372ee9615e485f441b5ab029bf6a081d76486babca49574e2f66b"
          }
        },
        {
          "id": "ventifact",
          "revision": "r001",
          "metadata": {
            "path": "assets/additions/ventifact/batch55-20261020/release-metadata.json",
            "sha256": "a0abb780a9450ec14c80a4072ba156d8dd7e38094ee9da76e0bd65c25765253e"
          },
          "source_metadata": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/metadata.json",
            "sha256": "0033eec290e58bd7756d51d1ce6fa4fd0b990b891dcc328b4b907916d0810fdd"
          },
          "candidate": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/candidate.json",
            "sha256": "14adee0e803e6cb7234190ad3c964cb36337871baf72bb09b71f5ea9c827b192"
          },
          "artifacts": {
            "glb": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/ventifact.glb",
              "sha256": "291ad1bbff024594c61ad218ea4fc33add08425d2998fbec20051de8abad64fa",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "brief": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/brief.json",
              "sha256": "80d933ba49132009c2b8801c358fefb40b0c123666d84ce7a2b37baf943c0628",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "references": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/references.json",
              "sha256": "2d318b9cd1aba064a7c753092fda99f6147df49ea99d2a05384ddec775918b27",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "source": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/ventifact.blend",
              "sha256": "4e58fea6b2c19ac70d39c87d93bf6ebd2683a7eb60c8250128b0fc465e3d6b92",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "generator": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/generator.py",
              "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "config": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/build-config.json",
              "sha256": "8048ab06a3b10dd45189a64795a2b92de51311655955e6dd7843dac0a8fb4abc",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            }
          },
          "packaging_candidate": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001-packaging-v1/candidate.json",
            "sha256": "7e5f2fba1b83d8622d193eb09335a044f7a95535fb61c19a4db54c7d2123f60c"
          },
          "packaging_brief": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001-packaging-v1/brief.json",
            "sha256": "66e28588e8171bd2c4658acb9a1d51aed22d0bb830aff774ff5025618323f03e"
          },
          "poster": {
            "id": "ventifact",
            "path": "assets/card-previews/ventifact-v2-768-q90.webp",
            "sha256": "8969b6a9ce883a64b69b017f36e5eff57bfc9c28bf9e75fa7d4fa3f882d381ff",
            "bytes": 6296,
            "width": 768,
            "height": 768,
            "source_glb_sha256": "291ad1bbff024594c61ad218ea4fc33add08425d2998fbec20051de8abad64fa",
            "render_preset_sha256": "2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff"
          },
          "capture_reference": {
            "path": "qa/batches51-55-release-20261020/capture/references/ventifact.png",
            "sha256": "69c228408dc80cfac34b9c6a0f07acede1b6e6db62ae5ef212d6240188000750"
          },
          "review": {
            "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/INDEPENDENT-QA.md",
            "sha256": "7321a9c25b1372ee9615e485f441b5ab029bf6a081d76486babca49574e2f66b"
          }
        },
        {
          "id": "pentichnus-deep-dwelling-trace",
          "revision": "r002",
          "metadata": {
            "path": "assets/additions/pentichnus-deep-dwelling-trace/batch55-20261020/release-metadata.json",
            "sha256": "86b3a71ce63e7845c1810a425e0f216bed540877752b97cc7a50228f9020d951"
          },
          "source_metadata": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/metadata.json",
            "sha256": "da84e300aabcd7a64cd25fcfc68314fa8d01df96d9d2c4e930aff8caed0e224e"
          },
          "candidate": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/candidate.json",
            "sha256": "136439a975d0464daa5abe5229a2ae73718213a3027977258c528271a7cb8bd9"
          },
          "artifacts": {
            "glb": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/pentichnus-deep-dwelling-trace.glb",
              "sha256": "aefb89b47511df9534a02af61e0d96c77bafc34c2646eb295891bc2104cc59f9",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "brief": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/brief.json",
              "sha256": "f6ba0d57331cd96eab2454b3ea29ba9dd487dc9f506a9a030da915c79a4269e7",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "references": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/references.json",
              "sha256": "abb9d2c688c19f51666a637e02ebd603822d9f14e57c6253f95a9dcdf4768192",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "source": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/pentichnus-deep-dwelling-trace.blend",
              "sha256": "2c043946f5054c1722e72b62bb74826a619d94e63ee94c9ee83729e184d2cb3a",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "generator": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/generator.py",
              "sha256": "f1f2574869ff4e170c08f374e1c69a6599aa9ff9995e3cf413348b45af08af40",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            },
            "config": {
              "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/build-config.json",
              "sha256": "4b3d51521130c3767fea2a8b4ee5c16a28349cb6f8fd7e5a35ad1770edf2fa75",
              "source_commit": "54ca033757bce0d282358e60473e81b8ca4778e1"
            }
          },
          "packaging_candidate": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002-packaging-v1/candidate.json",
            "sha256": "64d8f0bbaa2cd23afe2d48f12cb8300559729f84349dbb5a5c5130f6f0cd2753"
          },
          "packaging_brief": {
            "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002-packaging-v1/brief.json",
            "sha256": "0077e3d7efd6a2c240ae3a0035b0e9c371208745c2774aea068991f1d4724264"
          },
          "poster": {
            "id": "pentichnus-deep-dwelling-trace",
            "path": "assets/card-previews/pentichnus-deep-dwelling-trace-v2-768-q90.webp",
            "sha256": "5e0c94274e67bb1f4bcf8aa84779c2ec1361d9d01071622cb12472eaefd9fcdb",
            "bytes": 7414,
            "width": 768,
            "height": 768,
            "source_glb_sha256": "aefb89b47511df9534a02af61e0d96c77bafc34c2646eb295891bc2104cc59f9",
            "render_preset_sha256": "2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff"
          },
          "capture_reference": {
            "path": "qa/batches51-55-release-20261020/capture/references/pentichnus-deep-dwelling-trace.png",
            "sha256": "bfa5ccdce52a8d3f41f5d05839810ca80f3970457d9c8e52d3b2b3f654ac7f99"
          },
          "review": {
            "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/INDEPENDENT-QA.md",
            "sha256": "7321a9c25b1372ee9615e485f441b5ab029bf6a081d76486babca49574e2f66b"
          }
        }
      ],
      "historical_evidence_disclosure": {
        "path": "qa/batch55-release-20261020/historical-evidence-disclosure.json",
        "sha256": "319f9959f5471728175fa3504ef616386120fc0d1a783afff4eb01e594cf2d84"
      },
      "files": [
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/brief.json",
          "sha256": "12fa2c003cd5c638220723fa9c830ab5629e2abcbff7975788dc45c889c0ca44",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/brief.md",
          "sha256": "5d7ec95d0d7774a91875be495c87f9951de10b85ecae3c4d42a1a2b8557a05e6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/build-config.json",
          "sha256": "9a912433db99c8aa2dfc490bb54a298f34234d83d41f0ab8412c55fcbb41b9f1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/build-run-binding.json",
          "sha256": "ec02ef765c7c06f82c64faf14f9bb399a4a796aed9ff116522a08b85022091cd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/generator.py",
          "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/gltf-validator.report.json",
          "sha256": "a4475a9af6eb229a442e22f4cdc41ae2985f513633c69c635675c3cb80fe97c5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/metadata.json",
          "sha256": "f20acc1a3f2133627d57e2692bb832af388b81f6b19394bd264ccdee887a96bf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/modeling-freeze.json",
          "sha256": "372db00f831b7a26730771045a8c516b874651c829fedecc52a9bb2ad7b39639",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/modeling-start.json",
          "sha256": "3470975d5bc5dd370c7dbb07fd1b4459f8b2c54c4987203968b952f618d79a98",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/pentichnus-deep-dwelling-trace.blend",
          "sha256": "03eb861822aa8c6bc9801704532ad9b41a43eefbe12b0dff903aef29ea2bdef0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/pentichnus-deep-dwelling-trace.glb",
          "sha256": "71dd737b105ed36eec1021147c73db2e0d0abb6c7aafdcb836a4e63d580584cd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/qa.json",
          "sha256": "a550ba7a15b19dce527dc0bb6531fc5bf9d9e3a6907615e9623304ded78ac9f3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r001/references.json",
          "sha256": "abb9d2c688c19f51666a637e02ebd603822d9f14e57c6253f95a9dcdf4768192",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002-packaging-v1/brief.json",
          "sha256": "0077e3d7efd6a2c240ae3a0035b0e9c371208745c2774aea068991f1d4724264",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002-packaging-v1/candidate.json",
          "sha256": "64d8f0bbaa2cd23afe2d48f12cb8300559729f84349dbb5a5c5130f6f0cd2753",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002-packaging-v1/packaging-contract.json",
          "sha256": "5af8bf6afa9c5d964658edd0342dd50ae25c2c1163587bbd0cda5c981af0d3be",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002-packaging-v1/profile-contract.json",
          "sha256": "aeb1c5345165c8b4f9e552457937f86549fe94ee43c2bbda07422448d346620a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/artifact-hashes.json",
          "sha256": "9ced40f21a16314a8199a8f8fe51a198eb8145444c96ad62e8a9595afb7aa682",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/brief.json",
          "sha256": "f6ba0d57331cd96eab2454b3ea29ba9dd487dc9f506a9a030da915c79a4269e7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/brief.md",
          "sha256": "5d7ec95d0d7774a91875be495c87f9951de10b85ecae3c4d42a1a2b8557a05e6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/build-config.json",
          "sha256": "4b3d51521130c3767fea2a8b4ee5c16a28349cb6f8fd7e5a35ad1770edf2fa75",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/build-run-binding.json",
          "sha256": "c212b93b666d469d967ff0e1b6f330424402e21bee92a8b042ba84aa0fc68fb4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/candidate.json",
          "sha256": "136439a975d0464daa5abe5229a2ae73718213a3027977258c528271a7cb8bd9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/concept-evidence.json",
          "sha256": "f5b8cadde1129124c74b99d17c6ab354bf29cf63faa0a71ec359d69d229e4bbe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/contact-sheet.png",
          "sha256": "9932d11824a2aeb2c55fbca6a81c5f559f2fee80de44a6c851699ae1756f498b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/dependency-hashes.json",
          "sha256": "39db4a4a0e919a7dc1b53512633a69b10b2846e2d9deae86abc378e9ff88d28e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/candidate-legacy.json",
          "sha256": "bf004cc25d4df0a5389b9f9dd18c4f2c90a264ca2ad539499cb86fe312a0cecc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/candidate-profile.json",
          "sha256": "8128c81248e374d157a1a1ee78c31cc4425bfb1cb0b1e7b694b1ed502a35ca1f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/concept-completeness-draft-authoring-time.json",
          "sha256": "1a8d85a768c53dbf0990b9ea1de0d6cabf0991302b0b34235ce592cae31fa070",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/concept-completeness-initial-scope-error.json",
          "sha256": "441e171f34c666ba670da8a761e63164532ccc37e8e0af422b6b3f2ceb5c2edb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/concept-completeness-relative-invocation-error.json",
          "sha256": "0bd660fbba82253f8c6020a85d66e99f359d1f33a0fae0e541f78db1ce58f60e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/concept-completeness.json",
          "sha256": "38ce7e4f46d9af7a498bea80840fbc38cc4cc2af36c6610514d61720d6684c41",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/concept-integrity-draft-authoring-time.json",
          "sha256": "1a8d85a768c53dbf0990b9ea1de0d6cabf0991302b0b34235ce592cae31fa070",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/concept-integrity-initial-scope-error.json",
          "sha256": "441e171f34c666ba670da8a761e63164532ccc37e8e0af422b6b3f2ceb5c2edb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/concept-integrity-relative-invocation-error.json",
          "sha256": "0bd660fbba82253f8c6020a85d66e99f359d1f33a0fae0e541f78db1ce58f60e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/concept-integrity.json",
          "sha256": "38ce7e4f46d9af7a498bea80840fbc38cc4cc2af36c6610514d61720d6684c41",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/reproducibility-1.json",
          "sha256": "f985a2ac74e2b72a54227fe53b940f5c73776d0fe05c6d5021d73cf632152c14",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/reproducibility-2.json",
          "sha256": "13a801e7d9ff2efafa356f8890baadd54fc422f30672a67436976d3a3bc88675",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/runtime-parse.json",
          "sha256": "e43ccdf967130d4d37f5c01132d8b281fc5f10023c15f858f9cce588d4255161",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/source-export.json",
          "sha256": "998b8f581f507417aa9b4e6549fbdea4a9d8845bbf62016b13cecab9db07937c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/evidence/source-metrics.json",
          "sha256": "e8f5f6670252d7dd8fe00f7c922094270d964709061d68383e9da541cc991bc9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/generator.py",
          "sha256": "f1f2574869ff4e170c08f374e1c69a6599aa9ff9995e3cf413348b45af08af40",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/gltf-validator.report.json",
          "sha256": "e5fe7fa694ae75338788efb7a7ad17de98010cbc03628c314eaacd769de8c6a9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/maker-review.md",
          "sha256": "3dcbd43dc1c6654f4eefcb0726cec399fee47747fdb6781cd69cffbf7d03de77",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/measurements.json",
          "sha256": "6e957c3b9e3fc5863cd9204318d0f32a407122a6346b19c55a3c66b789d53131",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/metadata.json",
          "sha256": "da84e300aabcd7a64cd25fcfc68314fa8d01df96d9d2c4e930aff8caed0e224e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/modeling-freeze.json",
          "sha256": "182062a4566afd2f8a69902d939ae82ed63404c93b8e9af6bd73c41cb46c4c43",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/modeling-start.json",
          "sha256": "2d14c47d3d17ec7309a5fbee7cbde5cb99a07002b2d4fb86b8028aecf08b1025",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/pentichnus-deep-dwelling-trace.blend",
          "sha256": "2c043946f5054c1722e72b62bb74826a619d94e63ee94c9ee83729e184d2cb3a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/pentichnus-deep-dwelling-trace.glb",
          "sha256": "aefb89b47511df9534a02af61e0d96c77bafc34c2646eb295891bc2104cc59f9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/profile-contract.json",
          "sha256": "3682af633d6128f2efe2ef396f96a262841fd0258e2550833d5b9b3db9f69c31",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/clay.png",
          "sha256": "5fa07a0973b056bf1a2cae2d97bb2dfb3ccaf855f053cbd6b93d576f81fae29d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/front.png",
          "sha256": "2616556afefbf052a461f646fe709707e73e6ea9374d8835b5b53c3a53a590c4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/hero.png",
          "sha256": "91d5c371ece5a7a5848d4dd9dbefa06113addabbda79560080827fa4da287e3e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/rear.png",
          "sha256": "ac7367d761ad1c5bcf536d87045fc4d8a27f0c97ebc2904262eefff3b070cd67",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/render-config.json",
          "sha256": "d3e2187687607f1c183b2e8b05f1e20b805ac8d9bd0dc08d7c2f40e865c3ca6d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/render-manifest.json",
          "sha256": "755b3e96c1c533dc7baf7943b268389f1817f67654b46698f47268e19b46ccd5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/reversehero.png",
          "sha256": "a08c377942f4899658b755e51c6576c6953bc0ce296d72a050c989c3c24c6291",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/side.png",
          "sha256": "ac239382b3961df8ee075f2f59d52a5daec1e3782e2cf3c975a45abbfc902a10",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/silhouette.png",
          "sha256": "2dda20579ee26a9787a4229ec9df5c03b2aea1c577e7a6ee5253e8540820cca5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/top.png",
          "sha256": "677fc17428e96c835923d27639615f75d11bcb1ae244d0b74561410eeb3a45ba",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/proof/turntable.json",
          "sha256": "78c597ff1ebe22566316ea8385123dc1b79ba1ee3cb89934785693d262f6864c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/qa.json",
          "sha256": "6fd86ccc0af5632dd6b2c4f06b7c4ee015253c7055733fb7807fe6a1add3cdfe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/references-profile.json",
          "sha256": "8151bbe3429c69ff6ce6e13d19ea7e5fc2391812d2f92bb76a86eabd8a290ad4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/references.json",
          "sha256": "abb9d2c688c19f51666a637e02ebd603822d9f14e57c6253f95a9dcdf4768192",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/pentichnus-deep-dwelling-trace/r002/repair-note.md",
          "sha256": "6c39f632c6bc84ad884fa89a16d49ba3f96f7816172b8f29195898133cde2351",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001-packaging-v1/brief.json",
          "sha256": "66e28588e8171bd2c4658acb9a1d51aed22d0bb830aff774ff5025618323f03e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001-packaging-v1/candidate.json",
          "sha256": "7e5f2fba1b83d8622d193eb09335a044f7a95535fb61c19a4db54c7d2123f60c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001-packaging-v1/packaging-contract.json",
          "sha256": "6bc91704ba78fb94ff0a0cb8ac2074079482cff1b70a5e80f00be44f41dd93a7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001-packaging-v1/profile-contract.json",
          "sha256": "5c3c42224dcf13820c7d11fa9784cad327ed68f04cb7e7e17b36d220144e481c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/artifact-hashes.json",
          "sha256": "85de1d36fce69b036d5f6f22387b442fe1212d744c95838179f73170fd54a5e8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/brief.json",
          "sha256": "80d933ba49132009c2b8801c358fefb40b0c123666d84ce7a2b37baf943c0628",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/brief.md",
          "sha256": "30bfad3e97682a3734e6fde80eb65584a9d049d6d020ff2d759f16ef96936ea0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/build-config.json",
          "sha256": "8048ab06a3b10dd45189a64795a2b92de51311655955e6dd7843dac0a8fb4abc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/build-run-binding.json",
          "sha256": "dcb7a29e83b1e2c7bf3751ea9a2cb28dfba620130c16ef970a6fb27960a483b5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/candidate.json",
          "sha256": "14adee0e803e6cb7234190ad3c964cb36337871baf72bb09b71f5ea9c827b192",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/concept-evidence.json",
          "sha256": "ca38a6ebe1e11a665ec24df8e127fcb64d5635f81e67f24481d8964e1393ff1d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/contact-sheet.png",
          "sha256": "d7971ce008428d89c87ea515d3f3b689c17c785e99b439c43c7c6c9432afb76e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/dependency-hashes.json",
          "sha256": "39db4a4a0e919a7dc1b53512633a69b10b2846e2d9deae86abc378e9ff88d28e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/candidate-legacy.json",
          "sha256": "bf004cc25d4df0a5389b9f9dd18c4f2c90a264ca2ad539499cb86fe312a0cecc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/candidate-profile.json",
          "sha256": "8128c81248e374d157a1a1ee78c31cc4425bfb1cb0b1e7b694b1ed502a35ca1f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/concept-completeness-draft-authoring-time.json",
          "sha256": "c9e09599337ad4df8b4114e0fe14441381768f2237800f81c2b9676ed196d83f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/concept-completeness-initial-scope-error.json",
          "sha256": "441e171f34c666ba670da8a761e63164532ccc37e8e0af422b6b3f2ceb5c2edb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/concept-completeness-relative-invocation-error.json",
          "sha256": "555082aab4f6461e4b76bd4cda711f8d2d0204414fea96328a3901f54cb0cd2d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/concept-completeness.json",
          "sha256": "4bcb34d4d16c6f607cec6ee518a7db286fff6b40cea39744d3deb86d4d5f2612",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/concept-integrity-draft-authoring-time.json",
          "sha256": "c9e09599337ad4df8b4114e0fe14441381768f2237800f81c2b9676ed196d83f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/concept-integrity-initial-scope-error.json",
          "sha256": "441e171f34c666ba670da8a761e63164532ccc37e8e0af422b6b3f2ceb5c2edb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/concept-integrity-relative-invocation-error.json",
          "sha256": "555082aab4f6461e4b76bd4cda711f8d2d0204414fea96328a3901f54cb0cd2d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/concept-integrity.json",
          "sha256": "4bcb34d4d16c6f607cec6ee518a7db286fff6b40cea39744d3deb86d4d5f2612",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/reproducibility-1.json",
          "sha256": "67e8e738e57f688255e87dba77a31d22613f4fa5ca49507a09262fcdc1519aba",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/reproducibility-2.json",
          "sha256": "931ff80c072b7a556d5cdf6817262ada1f6fc4efacf1f48520dada04335f0f95",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/runtime-parse.json",
          "sha256": "4342bccaacd19cd920b8aa9d20e89bdd99511211721da9ab9d386f7b0ec5b2dd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/source-export.json",
          "sha256": "8f2f116808bdb0bf4cc4078cb7bca2c8090b71bd8f3976efc21115255dd16730",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/evidence/source-metrics.json",
          "sha256": "97ec51f9e5f62a21db74213a96720b30519a77f67299a2fe80733ffd60f7713c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/generator.py",
          "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/gltf-validator.report.json",
          "sha256": "962bcb1ce81526ea18cfb138a6b1ec6acfeb409b944dc764c955962ddfca8045",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/maker-review.md",
          "sha256": "46bd439fd6a29898c82cfe622bc6a579d7b3e1102ce864bee3d67cf6d9276d0b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/measurements.json",
          "sha256": "c90f2fe862799d84e49678bfa8a1ba3de9cbbe0947c450b31bfa17f07dc93a51",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/metadata.json",
          "sha256": "0033eec290e58bd7756d51d1ce6fa4fd0b990b891dcc328b4b907916d0810fdd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/modeling-freeze.json",
          "sha256": "0c466d1abea3c0f4bdbfc2a7fa9c808d2261b6dd207783dfc3b486041b3a0856",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/modeling-start.json",
          "sha256": "b0537b2a22dfd45bbf4695ead10f20d190df3a2f899d0190c3e59a374c488dbb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/profile-contract.json",
          "sha256": "898f1becea9f74e9516eaee36b7e6665258827bf72081b858e34fb8c7ab868cf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/clay.png",
          "sha256": "1912e301af5b2163cb64aa7b80c3612ee31beb2249d05e64eaa956d49ac3eeed",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/front.png",
          "sha256": "c6235cfaeb4eea8b0ab91021552c8062e5f6ba0098aed32dadde07cc68129209",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/hero.png",
          "sha256": "f84679423ac48c77c432a501a080f9b3ad3a0698886a83b06618348aa75fee4e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/rear.png",
          "sha256": "563df1c0e1188060bf288ed84ab7040d43c6dbabf87b06a467eb0ece5d7bd4a8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/render-config.json",
          "sha256": "c8292540e8fb8f2383f11c85f6cbcc10cf8e2acb3b48803feeec4fa2993a4bbe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/render-manifest.json",
          "sha256": "e8196587eb4018c00b4c9e8401d18d0edc7989ac8c5f78ba5a33581a54bbd8ef",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/reversehero.png",
          "sha256": "90610c2b7e6f4d395ed73d1645f94c37faa78aaeaf1ff3d111803bbc8cafa397",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/side.png",
          "sha256": "30931acb4cf57c3cd9394f675e50481850eceadf01cd0fc81bd2b9f3e62865a6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/silhouette.png",
          "sha256": "40c613b9d5018036e25f757a201afdcbe72eee0b0068c08d51e589a90000d633",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/top.png",
          "sha256": "71c26abe1ec60ca672c9987857f0d96c5eb5796e8655027aa354de335437fbad",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/proof/turntable.json",
          "sha256": "f9a41efd0cf267fb9d2c6feac8d53a3bc8f246c79a2dcd217f1ee7d3e02dddfa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/qa.json",
          "sha256": "5fd1dbf586ee937c14947189ee4fd079ff379d08f25ef829c92e710e3caef4c7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/references-profile.json",
          "sha256": "9bdfd50511b06be68aeb05359a9553d66a77a25e2d11d227f1d96ab722237171",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/references.json",
          "sha256": "2d318b9cd1aba064a7c753092fda99f6147df49ea99d2a05384ddec775918b27",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/ventifact.blend",
          "sha256": "4e58fea6b2c19ac70d39c87d93bf6ebd2683a7eb60c8250128b0fc465e3d6b92",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/ventifact/r001/ventifact.glb",
          "sha256": "291ad1bbff024594c61ad218ea4fc33add08425d2998fbec20051de8abad64fa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001-packaging-v1/brief.json",
          "sha256": "eb3bd83020e990e3cfffe3ad4510a907d5958f68c47499044a24417d6bf49eaf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001-packaging-v1/candidate.json",
          "sha256": "4a3856d4e81323d77040d8109f098a2656d9aa4233fa0dc4bec30dc984cac481",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001-packaging-v1/packaging-contract.json",
          "sha256": "0190bf7b65ca6ad0c0e2d26a45deda8f321890f7e7d5f19ffdd8186910b1abb4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001-packaging-v1/profile-contract.json",
          "sha256": "867e39bac7dfe1273c81f65988b47a8731a28be41e79e18bb8826e6f4fcb12cc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/artifact-hashes.json",
          "sha256": "c6a4d00282f608073d7b3a29893b28d5c54797796df943de25c21d239a87bbec",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/brief.json",
          "sha256": "772239b047fa49aec3129b38853c244e39c6ebd05c43c2e02749a9677e2d9455",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/brief.md",
          "sha256": "3175cef2fd595d8609c2b196c2309cda72ff08746202a68644a7dec342a822ff",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/build-config.json",
          "sha256": "32b0cc39c4f82b7b489f013963b0b02f61b45039e3fdcaa0bf7b3823b13eb8fc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/build-run-binding.json",
          "sha256": "5ddd988b9042bffbfcfecc1085b01579587c5114de048d1884838941125daf3d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/candidate.json",
          "sha256": "616b24ff699261111d8ad89feae12f5fb22bdb0117a5234d3aa0c1f93dd9ddd6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/concept-evidence.json",
          "sha256": "0b9af2586368a12132182ccaf94cda50f78dfaa29929ca86ab79c0c506e16167",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/contact-sheet.png",
          "sha256": "5278eb0a2a974c7cdccdc357f053408304d95c660eef0fee92d2d79136088c68",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/dependency-hashes.json",
          "sha256": "39db4a4a0e919a7dc1b53512633a69b10b2846e2d9deae86abc378e9ff88d28e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/candidate-legacy.json",
          "sha256": "bf004cc25d4df0a5389b9f9dd18c4f2c90a264ca2ad539499cb86fe312a0cecc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/candidate-profile.json",
          "sha256": "8128c81248e374d157a1a1ee78c31cc4425bfb1cb0b1e7b694b1ed502a35ca1f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/concept-completeness-draft-authoring-time.json",
          "sha256": "b5968983526efd4eb07de7d01f48df4c2ec17e0333aa22aca2d9e7dd31026f35",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/concept-completeness-initial-scope-error.json",
          "sha256": "441e171f34c666ba670da8a761e63164532ccc37e8e0af422b6b3f2ceb5c2edb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/concept-completeness-relative-invocation-error.json",
          "sha256": "c7fdb974539730133055fd84975f34a299b923e350c567d46473219895379780",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/concept-completeness.json",
          "sha256": "3d010f84398b481bb99590b47c1a37ad6c9163f2549cfcd15d142853eba51edc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/concept-integrity-draft-authoring-time.json",
          "sha256": "b5968983526efd4eb07de7d01f48df4c2ec17e0333aa22aca2d9e7dd31026f35",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/concept-integrity-initial-scope-error.json",
          "sha256": "441e171f34c666ba670da8a761e63164532ccc37e8e0af422b6b3f2ceb5c2edb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/concept-integrity-relative-invocation-error.json",
          "sha256": "c7fdb974539730133055fd84975f34a299b923e350c567d46473219895379780",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/concept-integrity.json",
          "sha256": "3d010f84398b481bb99590b47c1a37ad6c9163f2549cfcd15d142853eba51edc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/reproducibility-1.json",
          "sha256": "7b823549fad445b232055ecb482530acd17c26d48661ff63e2911980e7091212",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/reproducibility-2.json",
          "sha256": "0a97f02f9806dbbbaf1aaa980f063a73b7fd0e6d2b2b14fffb14d17d4f02acbe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/runtime-parse.json",
          "sha256": "69e28872e70b3366f25593a8417125ae75019d362b67d6cf46ac1c72c6c8ca09",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/source-export.json",
          "sha256": "795602b29353da8a612731495430ac5f3198e02c422a9fadd76fb906a20a87b2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/evidence/source-metrics.json",
          "sha256": "09c13a32f8ea4463785a6fe9e0fc69c208972f00bb9fe2da4047be9cca2c941a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/generator.py",
          "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/gltf-validator.report.json",
          "sha256": "afc6ab50b366102ba43ea5548701b22ddc833d1d1b23cebdd251e1c9772a37d6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/maker-review.md",
          "sha256": "d419bb37ce7a22acd7949a24431a92ed61ddfae017ad9e545157a2d03ac4d244",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/measurements.json",
          "sha256": "2edd255652cb1bbf90df6ffca68128a642a95bdf3cde6ef4046a0bfb6ab18ef4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/metadata.json",
          "sha256": "499435f6614d4547cab34e47c4c88cd2755c0e30c6fafd0ecb6ac86e01fc1702",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/modeling-freeze.json",
          "sha256": "ba2439c97d0a3690197a0afbaa6afbfd4d08d181eba47ba02d5d3071c7872a9c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/modeling-start.json",
          "sha256": "a7701bcea969114912c6fec8cf0d9fa3c1a3ffbf4a6f51ed9cc5179122506073",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/profile-contract.json",
          "sha256": "b3a91a34ade32c8b8dd64283a7ed358893021a4c54ce0c3495a1e9e174eeccb4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/clay.png",
          "sha256": "af1c6bb31345e37aee9b086ac68b6d6108d36a3c32a5d063c62e5d2951e2867d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/front.png",
          "sha256": "7492ac431cfbd4643b38ff56f6bc60a051c7f1835319f20d08505fcf9defa737",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/hero.png",
          "sha256": "33b73fff663b469a63629ad33fc86f91cace7cd44e3ab9d3a8d54d83a568f3c8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/rear.png",
          "sha256": "f18c4aaa992782e8b9d41ace52d98625aafe3ac714f7059c0315805c98fa02af",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/render-config.json",
          "sha256": "cf5c70d161ff62d9bcad021b278c0db14d027e9b9595356a6bbbf8d49e9dd1c9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/render-manifest.json",
          "sha256": "a0374f174ef932cede7ba38f510e212506b0ff87245a679b5bb251c4afe7e6ad",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/reversehero.png",
          "sha256": "f517aabb1c4699d64540ee6577247fa458454f561bda2aea6147b12374b680b5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/side.png",
          "sha256": "55d73f79d64749bf30d47e5624fc918780000916a89066e3702307f8cd2e23cd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/silhouette.png",
          "sha256": "024b683c0308e5afb3b326a60d883c0d0bf2c20983eb61ff11d148fb482b813c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/top.png",
          "sha256": "5ff8eb57adb046fd706d25016e7c21737f183fe8cf35c90af8bfb8d659390923",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/proof/turntable.json",
          "sha256": "15e3086a4dd21ba87f65f43178796bdf21d9318cce9c59ec5d016a82e8180fa4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/qa.json",
          "sha256": "17df464db17e5f3e0294ec930d6ee5dadf1ad5f89316ead55cfb0ffda350557e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/references-profile.json",
          "sha256": "99ad5db27781b7bb9cad99db0e50a0dc5dbbc9d5f4f0c499b8f923fc1ca81573",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/references.json",
          "sha256": "85c3ffaf8b67e46ba15a0e8b845d913b473be6f14a3af617af246788ed6514b5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/vermicularia.blend",
          "sha256": "328513c8cb5600645ba0f4e2d2a378acea89235039f313021b981698561cb7af",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/vermicularia/r001/vermicularia.glb",
          "sha256": "5bb8a455b222496fbe8568184eb2aff11b717aab29bbf42d3138707781b27f7f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001-packaging-v1/brief.json",
          "sha256": "ca06a95a81305d0cb561662e051c52536d0426dcc57783667c4b7f415e96b5b9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001-packaging-v1/candidate.json",
          "sha256": "05c7513b88c91b04db11f97b55dcddde800da0254c990ff3a20ac31310a8552e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001-packaging-v1/packaging-contract.json",
          "sha256": "6eb2ebe3eda232d6ffb59015cadf00163fb0759e94be87715e611358e0683dc1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001-packaging-v1/profile-contract.json",
          "sha256": "ac0e06d839e12e9d3b082cdefd360531393822fb68dfc2e74f66c48ff6864b6b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/artifact-hashes.json",
          "sha256": "c5eb56800369aaf2025c2ab241622a3984273bbfcb844e9b84de1c71acf4199f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/brief.json",
          "sha256": "b48f62878a56e0cc5869d44f660316875b85f7e9b1fb8285b57442ed9cbfe05c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/brief.md",
          "sha256": "2ca6a26f55dcdadbe82e530af1bf64532cd71183d7ea8d557eadb1c080317b53",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/build-config.json",
          "sha256": "ba83b050bbfa90d02b5843d9ee15ab1070a58813bb55d2f15a253ba99f69dab3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/build-run-binding.json",
          "sha256": "a23249055600e89ea0a6ef65a53db8474c8672ae179253788777dc3dcbe44045",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/candidate.json",
          "sha256": "82c0bca150da913fceeccbfb582744d941d70646e89e476d232475b79c3817c9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/concept-evidence.json",
          "sha256": "58a8c95b17d416dd112d67b6ad28491f9ba23d9e2b2f5f932403d17cbfbb6aed",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/contact-sheet.png",
          "sha256": "dc9bce9de60c1daaf7fa4fe41562b3d722a4963b6f7a1aacc48d9af7088379b9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/dependency-hashes.json",
          "sha256": "39db4a4a0e919a7dc1b53512633a69b10b2846e2d9deae86abc378e9ff88d28e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/candidate-legacy.json",
          "sha256": "bf004cc25d4df0a5389b9f9dd18c4f2c90a264ca2ad539499cb86fe312a0cecc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/candidate-profile.json",
          "sha256": "8128c81248e374d157a1a1ee78c31cc4425bfb1cb0b1e7b694b1ed502a35ca1f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/concept-completeness-draft-authoring-time.json",
          "sha256": "53395430c104bb23fe3e68014a205867f5620558f7cc2d269be9c310220d09ed",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/concept-completeness-initial-scope-error.json",
          "sha256": "441e171f34c666ba670da8a761e63164532ccc37e8e0af422b6b3f2ceb5c2edb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/concept-completeness-relative-invocation-error.json",
          "sha256": "998cc2bfc3d6502e6ffe2a02e18555f31ee96bab5ff5e306f3addca78c22dd90",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/concept-completeness.json",
          "sha256": "d9928fbf34f951bc94f0a16b075ec0a2f73d623d16d502c7bd95b608d32c114d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/concept-integrity-draft-authoring-time.json",
          "sha256": "53395430c104bb23fe3e68014a205867f5620558f7cc2d269be9c310220d09ed",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/concept-integrity-initial-scope-error.json",
          "sha256": "441e171f34c666ba670da8a761e63164532ccc37e8e0af422b6b3f2ceb5c2edb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/concept-integrity-relative-invocation-error.json",
          "sha256": "998cc2bfc3d6502e6ffe2a02e18555f31ee96bab5ff5e306f3addca78c22dd90",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/concept-integrity.json",
          "sha256": "d9928fbf34f951bc94f0a16b075ec0a2f73d623d16d502c7bd95b608d32c114d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/reproducibility-1.json",
          "sha256": "c50c20f802f7ccbb5249da0ab5f68ae4ba09abec423642c8a576fedf592ad791",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/reproducibility-2.json",
          "sha256": "e17bf810ba38b98c19d075ef8b20b86e4821789ad64690dc65a9f152e1d7af7d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/runtime-parse.json",
          "sha256": "7917af61d838e59ba68de3b50b5f678fa69a0a43867917de9902f85b88161f7d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/source-export.json",
          "sha256": "57657abe1012e253dae4fb3f50fba7d684181f67aee6cd1ab6c1aeb9b806851d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/evidence/source-metrics.json",
          "sha256": "e24c0e6ee62edae2d8d2799055507ee0c7f1b9aba3d170c14627026da493e60c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/generator.py",
          "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/gltf-validator.report.json",
          "sha256": "4d8ca80ac6cc38d7bb3d9ab8ffadaac6933248f591e7542d6735b98572ed51ac",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/maker-review.md",
          "sha256": "eff1a98791dc99e66630f01a8783783d8d52ba283701e31e3d25885fab27480e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/measurements.json",
          "sha256": "0195ab09e3d33de21de4380266f09724eb6bdedd555faee0459f2e4738749408",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/metadata.json",
          "sha256": "8466cc47b61284d0a1a6f2ef076ca2a6ae6528a05f56562a814fa77994f31043",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/modeling-freeze.json",
          "sha256": "366634e21cfe5be2d4ab3825b5bcdecb24e8377e1d7f7f4c375bd861d1adc80b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/modeling-start.json",
          "sha256": "9378e4dbdef6901df791408248b39e0449b1a8ce761b58a7b75e9c5fc54ccbf6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/profile-contract.json",
          "sha256": "77b22d76ff0a4da8df272f74ca4271a4de0049908a14db744751629a3c536991",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/clay.png",
          "sha256": "952b2ff19fb09bb34ee5f4ee81c95cc30dc488fe142d89fa487fcb2c8b0fdb7f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/front.png",
          "sha256": "9d956d96eab573541dd7ac27eedd3cb55016959a97d7654b322791a8788699b1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/hero.png",
          "sha256": "53e400515c7587929db892a49ef37076bf430a673b3b431c113c194cfa513e6e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/rear.png",
          "sha256": "ad881835d1129d77a1cb8368b5a63c0879e0d0754758b08b60afc49e9941d2b0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/render-config.json",
          "sha256": "bc455cbd4358fd5a4512bddbbb30747df7b52d8602246b300696e6c980ad0806",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/render-manifest.json",
          "sha256": "254b6235e8bafe09aae002dcff2675054e4306dda58b77c2d93a3b5855cdb53c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/reversehero.png",
          "sha256": "23c32f2616fca33311eec43ff524f975838400b26b09c191a0d6d0b0f0acaa4d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/side.png",
          "sha256": "0c83c3e48a3c4388271888c653c7764bd76507696837a97a0308f8dbeeb23e18",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/silhouette.png",
          "sha256": "7c3bde8bb694d313cc4be921fcb5077f98a0e9edca9c3f3b73aa6b9ae4ad58de",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/top.png",
          "sha256": "dabf0bf40d716e10a92826fda948316b865635c738e73ecfca82b50ea6364fb4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/proof/turntable.json",
          "sha256": "5d68db4654d691a956073931a6a2323559f87c5f7f816618194325a04207c5eb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/qa.json",
          "sha256": "f26fe1cedc29765760a9dabc586f6a5e0f34dd9c4e4a1bceb67f8ddae20df760",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/references-profile.json",
          "sha256": "b18398e1709fbcf304ccd598dd87863dd9110c598037ee57adb436191f38d032",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/references.json",
          "sha256": "5df07b75b5aec7d47d24a0f72cdfe60b9638e44ef44cd4476cf99f79d982bfac",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/weichselia.blend",
          "sha256": "a196ad872025a7d25f998798bde442c6654d06ed55564f9bc76f95f9e1e905fd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "assets/candidates/continuous-small-life-round20-20261020/batch-55/weichselia/r001/weichselia.glb",
          "sha256": "4ece730443de73b6c2dca2fe2bc7a50517628e344b5e6edd37486901c997676a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/HANDOFF.md",
          "sha256": "7dff876d5b3109a3165dea9b0b1d2c717076e59fcfaad90fb955f08ce33a8c02",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/build-jobs.json",
          "sha256": "9c09615c86e1156ea5dc72c61d5036172d160076209234c7865d44754e6f94ef",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/claim.json",
          "sha256": "bd92c453c4f690cab7a67de925cc27fa16c5903610abc2f6027181d18b5df41a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/dispatch-execution.json",
          "sha256": "337db86c6417f382a6ae01eeb877d75bb756910f548e3800f47d4d6d5e500c3f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/frozen-subjects.json",
          "sha256": "1e17dbc6f4ed8b5a4f800611f6633fdf195196241066c1635d0bd472b9b44a2d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/generator.py",
          "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/maker-identity-provenance.json",
          "sha256": "9d4b1ca338b813c61658dfac0f4aa107132c6785c5a6c6ab8ca4681326111ab5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/maker-identity-validation.json",
          "sha256": "316ddb977c1b4ce9fa96b3e4192c75cdef40b4adc117c504d7770faa213bb4d5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/HANDOFF.md",
          "sha256": "c2fffcb1008f27ff15b0069a8b190599152e4f3bb1dcdbc3cb9b8b8c5a807071",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/correction-files.json",
          "sha256": "dc1c115576fd420fd5459ed03879f9277a2a502b6b0448007e3f5a5eae58078f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/create.py",
          "sha256": "e8f75fd1b5928967bc7478265573b226b516ed335e760ab6c4ac995e8f3f8ee5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/index.json",
          "sha256": "3367afe25b3c57bef322ded5288f16254bdb988f2900e75e164379f536a31a32",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/pipeline-pilot-baseline-retry.json",
          "sha256": "0dd9368ac5f1b70f118c6bbf597b8b4bf5c12803c33900b562e26d4aa221426b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/preserved-files.json",
          "sha256": "45765e9f32c99bf96025ee3512716edd8e7f8cfad33a5d87fc6d76a6149eb38a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/regression-results.json",
          "sha256": "e9daf03b636b4b9ec95415624469e29cdee9b038c6c5b683081b6469b2206d56",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/review-summary.json",
          "sha256": "8df93ee65f0d4b042d26cbcf8e1cc5a562f34c939a3e4a9b70fc9fa3d9644200",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/test_verify.py",
          "sha256": "acfaed0d90f11f8b0de1cf56fb54fce15de34b77bceb5cbc860e9373d5255327",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/validation-current.json",
          "sha256": "b5a47fbd4834b4c17f3b65fdb0b219dc4416408170fc94689551aca33463b57c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/packaging-correction-v1/verify.py",
          "sha256": "6279aa7b6152f1641b8c4e52d0ef753ec197f82e1a9d032ad899a626ac496d21",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/brief.json",
          "sha256": "12fa2c003cd5c638220723fa9c830ab5629e2abcbff7975788dc45c889c0ca44",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/brief.md",
          "sha256": "5d7ec95d0d7774a91875be495c87f9951de10b85ecae3c4d42a1a2b8557a05e6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/build-config.json",
          "sha256": "9a912433db99c8aa2dfc490bb54a298f34234d83d41f0ab8412c55fcbb41b9f1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/generator.py",
          "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/modeling-freeze.json",
          "sha256": "372db00f831b7a26730771045a8c516b874651c829fedecc52a9bb2ad7b39639",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/modeling-start.json",
          "sha256": "3470975d5bc5dd370c7dbb07fd1b4459f8b2c54c4987203968b952f618d79a98",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r001/references.json",
          "sha256": "abb9d2c688c19f51666a637e02ebd603822d9f14e57c6253f95a9dcdf4768192",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/brief.json",
          "sha256": "f6ba0d57331cd96eab2454b3ea29ba9dd487dc9f506a9a030da915c79a4269e7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/brief.md",
          "sha256": "5d7ec95d0d7774a91875be495c87f9951de10b85ecae3c4d42a1a2b8557a05e6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/build-config.json",
          "sha256": "4b3d51521130c3767fea2a8b4ee5c16a28349cb6f8fd7e5a35ad1770edf2fa75",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/generator.py",
          "sha256": "f1f2574869ff4e170c08f374e1c69a6599aa9ff9995e3cf413348b45af08af40",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/modeling-freeze.json",
          "sha256": "182062a4566afd2f8a69902d939ae82ed63404c93b8e9af6bd73c41cb46c4c43",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/modeling-start.json",
          "sha256": "2d14c47d3d17ec7309a5fbee7cbde5cb99a07002b2d4fb86b8028aecf08b1025",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/references.json",
          "sha256": "abb9d2c688c19f51666a637e02ebd603822d9f14e57c6253f95a9dcdf4768192",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/pentichnus-deep-dwelling-trace/r002/repair-note.md",
          "sha256": "6c39f632c6bc84ad884fa89a16d49ba3f96f7816172b8f29195898133cde2351",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-fixed8-jobs.json",
          "sha256": "e2b204c2c2dbb79a62e2158e114bad048d8d3b5118f5815672e8e21af5ebc7ac",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-jobs.json",
          "sha256": "f6959ec47ffe29d2d7605ca5c63d17a0378467b3a3701c918be8a0cbc8a0c085",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r001/exact-eight-views/755ebe91136e0eb36380222c951a210637414ce3e25ca4db39e6ca1c35ba7a6d/20261020T012831-7df4984a5bfa454baec527d78b5495de/request.json",
          "sha256": "398e4e443e3faf59aaf2e070487e4cc9005fac0c1f923c9afe92b2d1117ba9a6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r001/exact-eight-views/755ebe91136e0eb36380222c951a210637414ce3e25ca4db39e6ca1c35ba7a6d/20261020T012831-7df4984a5bfa454baec527d78b5495de/result.json",
          "sha256": "cc047d896d202a540ffdbbcc0bfdcefed639ef6b57fed5698c4206f2b83d5ff7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/clay.png",
          "sha256": "5fa07a0973b056bf1a2cae2d97bb2dfb3ccaf855f053cbd6b93d576f81fae29d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/front.png",
          "sha256": "2616556afefbf052a461f646fe709707e73e6ea9374d8835b5b53c3a53a590c4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/hero.png",
          "sha256": "91d5c371ece5a7a5848d4dd9dbefa06113addabbda79560080827fa4da287e3e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/rear.png",
          "sha256": "ac7367d761ad1c5bcf536d87045fc4d8a27f0c97ebc2904262eefff3b070cd67",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/render-config.json",
          "sha256": "d3e2187687607f1c183b2e8b05f1e20b805ac8d9bd0dc08d7c2f40e865c3ca6d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/render-manifest.json",
          "sha256": "755b3e96c1c533dc7baf7943b268389f1817f67654b46698f47268e19b46ccd5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/reversehero.png",
          "sha256": "a08c377942f4899658b755e51c6576c6953bc0ce296d72a050c989c3c24c6291",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/side.png",
          "sha256": "ac239382b3961df8ee075f2f59d52a5daec1e3782e2cf3c975a45abbfc902a10",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/silhouette.png",
          "sha256": "2dda20579ee26a9787a4229ec9df5c03b2aea1c577e7a6ee5253e8540820cca5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/top.png",
          "sha256": "677fc17428e96c835923d27639615f75d11bcb1ae244d0b74561410eeb3a45ba",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/outputs/turntable.json",
          "sha256": "78c597ff1ebe22566316ea8385123dc1b79ba1ee3cb89934785693d262f6864c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/request.json",
          "sha256": "71878054c726a5b0ca5913c9e775549ea62cda368776dadb9b1e6649437c0ca2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/pentichnus-deep-dwelling-trace/r002/exact-eight-views/c44331a061afd2ef08cfbf1e92889eddbfc02540d3696b6f6a11a9a19ecf75d5/20261020T012948-bb32a7a3a0ca4d6ab36152ff2617e86d/result.json",
          "sha256": "5292e54fd10b1c8c6477c161fa02d73b5a105366c647c0e2b92f2cf02df097d0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/clay.png",
          "sha256": "1912e301af5b2163cb64aa7b80c3612ee31beb2249d05e64eaa956d49ac3eeed",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/front.png",
          "sha256": "c6235cfaeb4eea8b0ab91021552c8062e5f6ba0098aed32dadde07cc68129209",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/hero.png",
          "sha256": "f84679423ac48c77c432a501a080f9b3ad3a0698886a83b06618348aa75fee4e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/rear.png",
          "sha256": "563df1c0e1188060bf288ed84ab7040d43c6dbabf87b06a467eb0ece5d7bd4a8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/render-config.json",
          "sha256": "c8292540e8fb8f2383f11c85f6cbcc10cf8e2acb3b48803feeec4fa2993a4bbe",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/render-manifest.json",
          "sha256": "e8196587eb4018c00b4c9e8401d18d0edc7989ac8c5f78ba5a33581a54bbd8ef",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/reversehero.png",
          "sha256": "90610c2b7e6f4d395ed73d1645f94c37faa78aaeaf1ff3d111803bbc8cafa397",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/side.png",
          "sha256": "30931acb4cf57c3cd9394f675e50481850eceadf01cd0fc81bd2b9f3e62865a6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/silhouette.png",
          "sha256": "40c613b9d5018036e25f757a201afdcbe72eee0b0068c08d51e589a90000d633",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/top.png",
          "sha256": "71c26abe1ec60ca672c9987857f0d96c5eb5796e8655027aa354de335437fbad",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/outputs/turntable.json",
          "sha256": "f9a41efd0cf267fb9d2c6feac8d53a3bc8f246c79a2dcd217f1ee7d3e02dddfa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/request.json",
          "sha256": "378487ebd0e3be5fd1d63f502c693110af55c9656102a5079c7ecbf488e3701b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/144ff4290d3b5878ee03a9f7bb592ca638fa1299ab6334043d3c977cfcd6558f/20261020T012939-2e01fed02cd8428d8b1180bfca2ba809/result.json",
          "sha256": "9c04ad3afb9e81b52ba09a40da2d494e36d0ceca1e357eb0c819fa8e78a15d7b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/bacd050bd1ebc2b425fb759690cd97b57d201e0cbd679c6a1ee0d16e43d80b43/20261020T012830-d650ed3370f64cb2a23de83fe4287c8e/request.json",
          "sha256": "625aa38a829e56d4ae6f74b531a6a8db93d72ea081092be95973ae6161c37a40",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/ventifact/r001/exact-eight-views/bacd050bd1ebc2b425fb759690cd97b57d201e0cbd679c6a1ee0d16e43d80b43/20261020T012830-d650ed3370f64cb2a23de83fe4287c8e/result.json",
          "sha256": "ea3dffe51ae0797ba025bd5b3c3091aa9fe6537248669dfe91889c0cd1f63992",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/clay.png",
          "sha256": "af1c6bb31345e37aee9b086ac68b6d6108d36a3c32a5d063c62e5d2951e2867d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/front.png",
          "sha256": "7492ac431cfbd4643b38ff56f6bc60a051c7f1835319f20d08505fcf9defa737",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/hero.png",
          "sha256": "33b73fff663b469a63629ad33fc86f91cace7cd44e3ab9d3a8d54d83a568f3c8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/rear.png",
          "sha256": "f18c4aaa992782e8b9d41ace52d98625aafe3ac714f7059c0315805c98fa02af",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/render-config.json",
          "sha256": "cf5c70d161ff62d9bcad021b278c0db14d027e9b9595356a6bbbf8d49e9dd1c9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/render-manifest.json",
          "sha256": "a0374f174ef932cede7ba38f510e212506b0ff87245a679b5bb251c4afe7e6ad",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/reversehero.png",
          "sha256": "f517aabb1c4699d64540ee6577247fa458454f561bda2aea6147b12374b680b5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/side.png",
          "sha256": "55d73f79d64749bf30d47e5624fc918780000916a89066e3702307f8cd2e23cd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/silhouette.png",
          "sha256": "024b683c0308e5afb3b326a60d883c0d0bf2c20983eb61ff11d148fb482b813c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/top.png",
          "sha256": "5ff8eb57adb046fd706d25016e7c21737f183fe8cf35c90af8bfb8d659390923",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/outputs/turntable.json",
          "sha256": "15e3086a4dd21ba87f65f43178796bdf21d9318cce9c59ec5d016a82e8180fa4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/request.json",
          "sha256": "e2e7a6e94cb9def6b787867ed4c95a7cd24913bfb9d5e48bb104da037c0fa93f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/4625c7ba761e2de712ff94eaded466fe0bb99e5c34421aa3212c52a72c4a76a7/20261020T013007-4988600de084410aae940a5b60f24e69/result.json",
          "sha256": "3c595e4b86170a0cab474b03702ca624e8e5614490b9586004a2b9f011c6f87a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/6e4814dcf66917efc593e8565c130509efbd0f4c48fcd41e113c621f31f91b62/20261020T012834-2eacae15aba74220ad8a5c920231b522/request.json",
          "sha256": "8f184dfe430d0bb5107036d11d6d5eca422cf1c100e45e427ee5c2df7d809a16",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/vermicularia/r001/exact-eight-views/6e4814dcf66917efc593e8565c130509efbd0f4c48fcd41e113c621f31f91b62/20261020T012834-2eacae15aba74220ad8a5c920231b522/result.json",
          "sha256": "bfaef6a8119286d7c8144ea87a3aefc0616c4da495b1ac0e65d7a21ce9aba01c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/clay.png",
          "sha256": "952b2ff19fb09bb34ee5f4ee81c95cc30dc488fe142d89fa487fcb2c8b0fdb7f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/front.png",
          "sha256": "9d956d96eab573541dd7ac27eedd3cb55016959a97d7654b322791a8788699b1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/hero.png",
          "sha256": "53e400515c7587929db892a49ef37076bf430a673b3b431c113c194cfa513e6e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/rear.png",
          "sha256": "ad881835d1129d77a1cb8368b5a63c0879e0d0754758b08b60afc49e9941d2b0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/render-config.json",
          "sha256": "bc455cbd4358fd5a4512bddbbb30747df7b52d8602246b300696e6c980ad0806",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/render-manifest.json",
          "sha256": "254b6235e8bafe09aae002dcff2675054e4306dda58b77c2d93a3b5855cdb53c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/reversehero.png",
          "sha256": "23c32f2616fca33311eec43ff524f975838400b26b09c191a0d6d0b0f0acaa4d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/side.png",
          "sha256": "0c83c3e48a3c4388271888c653c7764bd76507696837a97a0308f8dbeeb23e18",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/silhouette.png",
          "sha256": "7c3bde8bb694d313cc4be921fcb5077f98a0e9edca9c3f3b73aa6b9ae4ad58de",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/top.png",
          "sha256": "dabf0bf40d716e10a92826fda948316b865635c738e73ecfca82b50ea6364fb4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/outputs/turntable.json",
          "sha256": "5d68db4654d691a956073931a6a2323559f87c5f7f816618194325a04207c5eb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/request.json",
          "sha256": "98ff3984e3270f1d0f962b053cfc4154c44be37670885026bf48cbc571ac77ae",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/81210e5e0f712291190d82f8f169a9bab635762c125116860121caff0c44ec26/20261020T012959-339e2390ce0741848b57f43558a5807f/result.json",
          "sha256": "9847c3c0cfb59dc158e8ae2909db0e75ee3db056a14cd8cc331399d9e3024ec9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/861726ae8ee563977a26ed2f4b9ad42de1a91c6997a850429529d0d7f85ade4c/20261020T012833-4473dec03eaf4c97ad5d0e37c36fd675/request.json",
          "sha256": "4fd6f566c45b222a6211a44bcc1f5e8c707522b11f4eb71c203a6ee732c0c02a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/render/weichselia/r001/exact-eight-views/861726ae8ee563977a26ed2f4b9ad42de1a91c6997a850429529d0d7f85ade4c/20261020T012833-4473dec03eaf4c97ad5d0e37c36fd675/result.json",
          "sha256": "484a059e3f1b512e7425351a73f26232926bfe01a70fd1b9f49f506a4e900106",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/runs/20261020T012830-4d956608237c402a84aabe5cd28f6612/manifest.json",
          "sha256": "8c583a641a8e17044dd35f1067e0a61803138973e4b538a59c63d1f7062f19a9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/runs/20261020T012830-4d956608237c402a84aabe5cd28f6612/summary.json",
          "sha256": "24b913d126053cb5be962c2c2676335fa5d62550af8890b9356cf317fef21240",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/runs/20261020T012938-197e373ac65d4d3cbbf0542d35130017/manifest.json",
          "sha256": "acd2e7176833bc7519e7bfc1b85470d24814a9a560ef44796266042c22483efd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-runs/runs/20261020T012938-197e373ac65d4d3cbbf0542d35130017/summary.json",
          "sha256": "17258e9280361d08313de9c3f70f69da8918eaf9f40578f63bcdcdaa1a4e8205",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-tools/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-tools/qa_glb.py",
          "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/render-tools/render_candidate_views.py",
          "sha256": "ccf495a88f88480de609b9cf91ddeeb2a1e0d79c345e66ce1a97baa5bedee83a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/repair-build-jobs.json",
          "sha256": "1a888378083aec5f089a84ea98817ee4e31be111bd5d2be8aeab4a70868bd18b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/research/access.json",
          "sha256": "82cf6f3e83f07245b9f033ec3d4b727f89bf117c45a73d16e6f2918ba22d697d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/.queue.lock",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/initial/8d45330aa4edb4f9125c75db7a2236003d005ebebb9f6131152f38560ef9cb8b/20261020T012801-7c11e4e450b3437891608b8299b75cc6/outputs/pentichnus-deep-dwelling-trace/metadata.json",
          "sha256": "f20acc1a3f2133627d57e2692bb832af388b81f6b19394bd264ccdee887a96bf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/initial/8d45330aa4edb4f9125c75db7a2236003d005ebebb9f6131152f38560ef9cb8b/20261020T012801-7c11e4e450b3437891608b8299b75cc6/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.blend",
          "sha256": "03eb861822aa8c6bc9801704532ad9b41a43eefbe12b0dff903aef29ea2bdef0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/initial/8d45330aa4edb4f9125c75db7a2236003d005ebebb9f6131152f38560ef9cb8b/20261020T012801-7c11e4e450b3437891608b8299b75cc6/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.glb",
          "sha256": "71dd737b105ed36eec1021147c73db2e0d0abb6c7aafdcb836a4e63d580584cd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/initial/8d45330aa4edb4f9125c75db7a2236003d005ebebb9f6131152f38560ef9cb8b/20261020T012801-7c11e4e450b3437891608b8299b75cc6/outputs/pentichnus-deep-dwelling-trace/qa.json",
          "sha256": "686a3d5da42c9573a8e2a81628c38d0e825bd31ac27ee57cdcb28c6353d072cc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/initial/8d45330aa4edb4f9125c75db7a2236003d005ebebb9f6131152f38560ef9cb8b/20261020T012801-7c11e4e450b3437891608b8299b75cc6/request.json",
          "sha256": "9db0b9bb42136d42a8bd0a309ad824c991da9668cbf1e0e9045a83d2c0b616ca",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/initial/8d45330aa4edb4f9125c75db7a2236003d005ebebb9f6131152f38560ef9cb8b/20261020T012801-7c11e4e450b3437891608b8299b75cc6/result.json",
          "sha256": "991ed66e1f9df0da5e7a655db14508edaf9aef4122efb4a2d88db82bb2d243f6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-1/95c357f7efbc66fa88b2c7c2fe000c9dc65bf69aa5f1c79c5252e29c1117b64e/20261020T012803-eb964cf0b693411fb37035194c8e1e28/outputs/pentichnus-deep-dwelling-trace/metadata.json",
          "sha256": "35c57641e013b406c1364bbbaf485a6a1bf6c39d2cebbf854d7de52ae8901868",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-1/95c357f7efbc66fa88b2c7c2fe000c9dc65bf69aa5f1c79c5252e29c1117b64e/20261020T012803-eb964cf0b693411fb37035194c8e1e28/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.blend",
          "sha256": "5cdef0aa0bd3604808b1adeee7a0f869459e3860395afd4da83043faf23a2835",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-1/95c357f7efbc66fa88b2c7c2fe000c9dc65bf69aa5f1c79c5252e29c1117b64e/20261020T012803-eb964cf0b693411fb37035194c8e1e28/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.glb",
          "sha256": "71dd737b105ed36eec1021147c73db2e0d0abb6c7aafdcb836a4e63d580584cd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-1/95c357f7efbc66fa88b2c7c2fe000c9dc65bf69aa5f1c79c5252e29c1117b64e/20261020T012803-eb964cf0b693411fb37035194c8e1e28/outputs/pentichnus-deep-dwelling-trace/qa.json",
          "sha256": "903ffb21dd4b533d59cb6de83655d59d3fb4dbd95a02ed50be65f0baf6d10194",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-1/95c357f7efbc66fa88b2c7c2fe000c9dc65bf69aa5f1c79c5252e29c1117b64e/20261020T012803-eb964cf0b693411fb37035194c8e1e28/request.json",
          "sha256": "019598710781967e8e85261c616f0c66ec6575087a376544c13be44d0c103f4c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-1/95c357f7efbc66fa88b2c7c2fe000c9dc65bf69aa5f1c79c5252e29c1117b64e/20261020T012803-eb964cf0b693411fb37035194c8e1e28/result.json",
          "sha256": "fc428973cc0061805aa5e7c1d165a5964c0cfdedf583e76c2f984695ba2283cf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-2/f2f878bd26b5a02ddedc74ada132b788acbd7a38071056592f79d2baf06452f5/20261020T012805-0191368903e84f559cb16a86039a5110/outputs/pentichnus-deep-dwelling-trace/metadata.json",
          "sha256": "5c436a21b5ee5aec81cd708752db08cf19acda58c05d4bc3d568ce0d7cc64449",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-2/f2f878bd26b5a02ddedc74ada132b788acbd7a38071056592f79d2baf06452f5/20261020T012805-0191368903e84f559cb16a86039a5110/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.blend",
          "sha256": "d723eee634beae0d6c789cb79ff204f971a7a9bf5faa2a8e8517f7ec2cd03e1e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-2/f2f878bd26b5a02ddedc74ada132b788acbd7a38071056592f79d2baf06452f5/20261020T012805-0191368903e84f559cb16a86039a5110/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.glb",
          "sha256": "71dd737b105ed36eec1021147c73db2e0d0abb6c7aafdcb836a4e63d580584cd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-2/f2f878bd26b5a02ddedc74ada132b788acbd7a38071056592f79d2baf06452f5/20261020T012805-0191368903e84f559cb16a86039a5110/outputs/pentichnus-deep-dwelling-trace/qa.json",
          "sha256": "8d114f05369947c093ae7927b0a7f89937f389ca57f35981dff1111c945e4618",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-2/f2f878bd26b5a02ddedc74ada132b788acbd7a38071056592f79d2baf06452f5/20261020T012805-0191368903e84f559cb16a86039a5110/request.json",
          "sha256": "128cb0cbc6228700b177cf5bee9b730da2121e794709c85a22ce870eb2bd3190",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r001/rebuild-2/f2f878bd26b5a02ddedc74ada132b788acbd7a38071056592f79d2baf06452f5/20261020T012805-0191368903e84f559cb16a86039a5110/result.json",
          "sha256": "f50fba5a373b62b4a6535a59a9d6879f20e59b28150829fe76b72f96f6a8bf92",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/initial/91de28c949a1c703e228d34d7add3f06c13e7623fd403658ed00a342d96b0c39/20261020T012908-00e71f859eb34a4687549d4baa089310/outputs/pentichnus-deep-dwelling-trace/metadata.json",
          "sha256": "da84e300aabcd7a64cd25fcfc68314fa8d01df96d9d2c4e930aff8caed0e224e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/initial/91de28c949a1c703e228d34d7add3f06c13e7623fd403658ed00a342d96b0c39/20261020T012908-00e71f859eb34a4687549d4baa089310/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.blend",
          "sha256": "2c043946f5054c1722e72b62bb74826a619d94e63ee94c9ee83729e184d2cb3a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/initial/91de28c949a1c703e228d34d7add3f06c13e7623fd403658ed00a342d96b0c39/20261020T012908-00e71f859eb34a4687549d4baa089310/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.glb",
          "sha256": "aefb89b47511df9534a02af61e0d96c77bafc34c2646eb295891bc2104cc59f9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/initial/91de28c949a1c703e228d34d7add3f06c13e7623fd403658ed00a342d96b0c39/20261020T012908-00e71f859eb34a4687549d4baa089310/outputs/pentichnus-deep-dwelling-trace/qa.json",
          "sha256": "f07b9d79b11a11907ea6bed2befe658155cc7262abc46fe0ab1f964e66a277c1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/initial/91de28c949a1c703e228d34d7add3f06c13e7623fd403658ed00a342d96b0c39/20261020T012908-00e71f859eb34a4687549d4baa089310/request.json",
          "sha256": "962ab3deb95f9b2cf83b817649ebd6d361635069eb7219b08dc9a3e442f1755c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/initial/91de28c949a1c703e228d34d7add3f06c13e7623fd403658ed00a342d96b0c39/20261020T012908-00e71f859eb34a4687549d4baa089310/result.json",
          "sha256": "1ae4d2852a50d9ffea71ac9d1f07c75ad3e34e899abe2abdfd7981d145d44ead",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-1/b2c6c32b4612ca6f810f1d02cbbe1302db90676290dd208740f0b961dfb03100/20261020T012910-ad3e8eece5564aeda63380076570ebdc/outputs/pentichnus-deep-dwelling-trace/metadata.json",
          "sha256": "4e1634720995f4a840fbe71309bfc30933f316f604f1e69f537fde27ec95b0a3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-1/b2c6c32b4612ca6f810f1d02cbbe1302db90676290dd208740f0b961dfb03100/20261020T012910-ad3e8eece5564aeda63380076570ebdc/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.blend",
          "sha256": "27e3be345daaad6d3e8588cec4f3d5f124bd0430768e576403657026a71ca1d1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-1/b2c6c32b4612ca6f810f1d02cbbe1302db90676290dd208740f0b961dfb03100/20261020T012910-ad3e8eece5564aeda63380076570ebdc/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.glb",
          "sha256": "aefb89b47511df9534a02af61e0d96c77bafc34c2646eb295891bc2104cc59f9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-1/b2c6c32b4612ca6f810f1d02cbbe1302db90676290dd208740f0b961dfb03100/20261020T012910-ad3e8eece5564aeda63380076570ebdc/outputs/pentichnus-deep-dwelling-trace/qa.json",
          "sha256": "bccc50c31008719915ca31a3f7996ed2c9ecccc7a256aa6ee2a462ba92fea11c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-1/b2c6c32b4612ca6f810f1d02cbbe1302db90676290dd208740f0b961dfb03100/20261020T012910-ad3e8eece5564aeda63380076570ebdc/request.json",
          "sha256": "e55a9fcead95796b1fda931451420a8176f18590bce132e7961e52605674146f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-1/b2c6c32b4612ca6f810f1d02cbbe1302db90676290dd208740f0b961dfb03100/20261020T012910-ad3e8eece5564aeda63380076570ebdc/result.json",
          "sha256": "9a5eefa45498441551b4042add07e68987e7d6d300a8034665637e9e758ec1e9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-2/49a25f4797c2bb164bb7efa8e961a19c9902c3dda008a8bedd80e8ae40fda039/20261020T012911-ee420ff7706a4eea986546a6bb3de058/outputs/pentichnus-deep-dwelling-trace/metadata.json",
          "sha256": "092b3b1430a0ea053b2316cf2d251bb2b594ebf5ff074d2e02b39c90cdfd7541",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-2/49a25f4797c2bb164bb7efa8e961a19c9902c3dda008a8bedd80e8ae40fda039/20261020T012911-ee420ff7706a4eea986546a6bb3de058/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.blend",
          "sha256": "9ae845c331a292462c058edad769edccacdaef6c69625414cec1ba7d0160ea60",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-2/49a25f4797c2bb164bb7efa8e961a19c9902c3dda008a8bedd80e8ae40fda039/20261020T012911-ee420ff7706a4eea986546a6bb3de058/outputs/pentichnus-deep-dwelling-trace/pentichnus-deep-dwelling-trace.glb",
          "sha256": "aefb89b47511df9534a02af61e0d96c77bafc34c2646eb295891bc2104cc59f9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-2/49a25f4797c2bb164bb7efa8e961a19c9902c3dda008a8bedd80e8ae40fda039/20261020T012911-ee420ff7706a4eea986546a6bb3de058/outputs/pentichnus-deep-dwelling-trace/qa.json",
          "sha256": "75184a46786cdfe2b6a3a2b124fad5d4389ed290eaae8033bf84a2fa2ed8df1f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-2/49a25f4797c2bb164bb7efa8e961a19c9902c3dda008a8bedd80e8ae40fda039/20261020T012911-ee420ff7706a4eea986546a6bb3de058/request.json",
          "sha256": "e3a9f133f069896dd2ca2a576d77e413970fddf25bead0408446ff7a86c092b6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/pentichnus-deep-dwelling-trace/r002/rebuild-2/49a25f4797c2bb164bb7efa8e961a19c9902c3dda008a8bedd80e8ae40fda039/20261020T012911-ee420ff7706a4eea986546a6bb3de058/result.json",
          "sha256": "777d96185e248f5f3af48c1373a7deb1b8d5aebdccb764ca02f3b8b8275d38ef",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/initial/d93d9121129e8c3fd0a0ddba24ab0eb2861836e6b3236aec22c88b9f7000ddf0/20261020T012756-c17d8a3eb55b4a7d8c8dc310513652e8/outputs/ventifact/metadata.json",
          "sha256": "0033eec290e58bd7756d51d1ce6fa4fd0b990b891dcc328b4b907916d0810fdd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/initial/d93d9121129e8c3fd0a0ddba24ab0eb2861836e6b3236aec22c88b9f7000ddf0/20261020T012756-c17d8a3eb55b4a7d8c8dc310513652e8/outputs/ventifact/qa.json",
          "sha256": "c20f711db6aa6e3c4b6963f02aa4e0f2652a1e85237bdf343bef93d9e67c8f46",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/initial/d93d9121129e8c3fd0a0ddba24ab0eb2861836e6b3236aec22c88b9f7000ddf0/20261020T012756-c17d8a3eb55b4a7d8c8dc310513652e8/outputs/ventifact/ventifact.blend",
          "sha256": "4e58fea6b2c19ac70d39c87d93bf6ebd2683a7eb60c8250128b0fc465e3d6b92",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/initial/d93d9121129e8c3fd0a0ddba24ab0eb2861836e6b3236aec22c88b9f7000ddf0/20261020T012756-c17d8a3eb55b4a7d8c8dc310513652e8/outputs/ventifact/ventifact.glb",
          "sha256": "291ad1bbff024594c61ad218ea4fc33add08425d2998fbec20051de8abad64fa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/initial/d93d9121129e8c3fd0a0ddba24ab0eb2861836e6b3236aec22c88b9f7000ddf0/20261020T012756-c17d8a3eb55b4a7d8c8dc310513652e8/request.json",
          "sha256": "99c2a608ff55a55a0260f07b3c957ef62784764e5b2dffded112f414b3848a76",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/initial/d93d9121129e8c3fd0a0ddba24ab0eb2861836e6b3236aec22c88b9f7000ddf0/20261020T012756-c17d8a3eb55b4a7d8c8dc310513652e8/result.json",
          "sha256": "60de259e94aa94898481088e411cf0f8c97afb98ba2546d204da75a49ca86842",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-1/cb87f2ea173c76b3d01c32f1c95c0c0e6d488124d9e85e20797bc457b47bf639/20261020T012758-ff2cedb7a0f740c1bd189c0f971ffc31/outputs/ventifact/metadata.json",
          "sha256": "212d8e10dc00fc9ea94e982cd075456981e88f5956690a46ebe3d5230e256178",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-1/cb87f2ea173c76b3d01c32f1c95c0c0e6d488124d9e85e20797bc457b47bf639/20261020T012758-ff2cedb7a0f740c1bd189c0f971ffc31/outputs/ventifact/qa.json",
          "sha256": "d0dbec9e5eade85f567a5bd4621a44eb3fece40a857baf98c3ca51d5feda7224",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-1/cb87f2ea173c76b3d01c32f1c95c0c0e6d488124d9e85e20797bc457b47bf639/20261020T012758-ff2cedb7a0f740c1bd189c0f971ffc31/outputs/ventifact/ventifact.blend",
          "sha256": "68058e55e833e9a04c238a5ce53dface5560a85fc35a41d94902ea667a612cd0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-1/cb87f2ea173c76b3d01c32f1c95c0c0e6d488124d9e85e20797bc457b47bf639/20261020T012758-ff2cedb7a0f740c1bd189c0f971ffc31/outputs/ventifact/ventifact.glb",
          "sha256": "291ad1bbff024594c61ad218ea4fc33add08425d2998fbec20051de8abad64fa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-1/cb87f2ea173c76b3d01c32f1c95c0c0e6d488124d9e85e20797bc457b47bf639/20261020T012758-ff2cedb7a0f740c1bd189c0f971ffc31/request.json",
          "sha256": "b4be8c6ae9b2d3a5a92cd5a54950fb5c1693fa85a77ad5a37f9eaebf957c1eb1",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-1/cb87f2ea173c76b3d01c32f1c95c0c0e6d488124d9e85e20797bc457b47bf639/20261020T012758-ff2cedb7a0f740c1bd189c0f971ffc31/result.json",
          "sha256": "49bf41eaa535cb420fafe71c857e1d7162065d14ffba34633bd02feb077c865d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-2/d83105f533ff317c420013eacd794312ff3d75a61ed63517153de55a9633509b/20261020T012759-5f48f0af076e403e812544f6f6edbe48/outputs/ventifact/metadata.json",
          "sha256": "a0fd48e08df18c5902006982e8601f2d66785cc8775db7377cdceaf18da7c880",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-2/d83105f533ff317c420013eacd794312ff3d75a61ed63517153de55a9633509b/20261020T012759-5f48f0af076e403e812544f6f6edbe48/outputs/ventifact/qa.json",
          "sha256": "7ff50c06e4a93fcb4f5ed228cb7ea09d81f4e6205c349a0b6e9e8fab0a9a48c4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-2/d83105f533ff317c420013eacd794312ff3d75a61ed63517153de55a9633509b/20261020T012759-5f48f0af076e403e812544f6f6edbe48/outputs/ventifact/ventifact.blend",
          "sha256": "cc39f0c16aa4e435d26506d66af208e78267d196a1662eedd617775456ad652a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-2/d83105f533ff317c420013eacd794312ff3d75a61ed63517153de55a9633509b/20261020T012759-5f48f0af076e403e812544f6f6edbe48/outputs/ventifact/ventifact.glb",
          "sha256": "291ad1bbff024594c61ad218ea4fc33add08425d2998fbec20051de8abad64fa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-2/d83105f533ff317c420013eacd794312ff3d75a61ed63517153de55a9633509b/20261020T012759-5f48f0af076e403e812544f6f6edbe48/request.json",
          "sha256": "f9c1b5fad4404363c38f8465dcb8eb96e3f230a49c9a503af82c36fb508245b3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/ventifact/r001/rebuild-2/d83105f533ff317c420013eacd794312ff3d75a61ed63517153de55a9633509b/20261020T012759-5f48f0af076e403e812544f6f6edbe48/result.json",
          "sha256": "7a7a1313bf10560d1cdc6d1a208bc29f8ce32855d13fe5b17c953cb82a576655",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/initial/d7b9fc38de2015c80d1d7f59be21cdeabe09dc533b18b156a82dacb55f4d2631/20261020T012812-0e1d83ff4cbb40309f851ba7f769a94f/outputs/vermicularia/metadata.json",
          "sha256": "499435f6614d4547cab34e47c4c88cd2755c0e30c6fafd0ecb6ac86e01fc1702",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/initial/d7b9fc38de2015c80d1d7f59be21cdeabe09dc533b18b156a82dacb55f4d2631/20261020T012812-0e1d83ff4cbb40309f851ba7f769a94f/outputs/vermicularia/qa.json",
          "sha256": "df210b72c317784ed72a472bc910563d4259cd4dd05fe2b5c19906ff7adb3b1f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/initial/d7b9fc38de2015c80d1d7f59be21cdeabe09dc533b18b156a82dacb55f4d2631/20261020T012812-0e1d83ff4cbb40309f851ba7f769a94f/outputs/vermicularia/vermicularia.blend",
          "sha256": "328513c8cb5600645ba0f4e2d2a378acea89235039f313021b981698561cb7af",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/initial/d7b9fc38de2015c80d1d7f59be21cdeabe09dc533b18b156a82dacb55f4d2631/20261020T012812-0e1d83ff4cbb40309f851ba7f769a94f/outputs/vermicularia/vermicularia.glb",
          "sha256": "5bb8a455b222496fbe8568184eb2aff11b717aab29bbf42d3138707781b27f7f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/initial/d7b9fc38de2015c80d1d7f59be21cdeabe09dc533b18b156a82dacb55f4d2631/20261020T012812-0e1d83ff4cbb40309f851ba7f769a94f/request.json",
          "sha256": "71a6cdd120ed2f48b91647fc4ebd600dc2920077d666d4525a32f9f475f7c59c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/initial/d7b9fc38de2015c80d1d7f59be21cdeabe09dc533b18b156a82dacb55f4d2631/20261020T012812-0e1d83ff4cbb40309f851ba7f769a94f/result.json",
          "sha256": "1e73922bcf14f4a98bc21bb6648422a1e6647d4a2ab647327d22fa9330bbf6aa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-1/d145992dc835362427bb87833153c5e44700d356ead82ba022a00c06432f9451/20261020T012814-79bb3b8cc2d248c3994d74d46a631bd3/outputs/vermicularia/metadata.json",
          "sha256": "2be93b5683dd9cec9939b3f2b341dcf8bbb56d36ee6a9305e2ba370aa7f2890d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-1/d145992dc835362427bb87833153c5e44700d356ead82ba022a00c06432f9451/20261020T012814-79bb3b8cc2d248c3994d74d46a631bd3/outputs/vermicularia/qa.json",
          "sha256": "9b446660a149f274d20ed031833b9aa0b3f6ced83e6bc6811ee4823d9df2d5ef",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-1/d145992dc835362427bb87833153c5e44700d356ead82ba022a00c06432f9451/20261020T012814-79bb3b8cc2d248c3994d74d46a631bd3/outputs/vermicularia/vermicularia.blend",
          "sha256": "bb93709376a977140ac0388d50fcb65bcfbbb023c8335bd702a1286720e23605",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-1/d145992dc835362427bb87833153c5e44700d356ead82ba022a00c06432f9451/20261020T012814-79bb3b8cc2d248c3994d74d46a631bd3/outputs/vermicularia/vermicularia.glb",
          "sha256": "5bb8a455b222496fbe8568184eb2aff11b717aab29bbf42d3138707781b27f7f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-1/d145992dc835362427bb87833153c5e44700d356ead82ba022a00c06432f9451/20261020T012814-79bb3b8cc2d248c3994d74d46a631bd3/request.json",
          "sha256": "4d09627abc68c826a08dbcb085d41be8689d38dbd9736eaeb3354ca8696bb0c8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-1/d145992dc835362427bb87833153c5e44700d356ead82ba022a00c06432f9451/20261020T012814-79bb3b8cc2d248c3994d74d46a631bd3/result.json",
          "sha256": "121395dbf9b43582891942efff568db48ffb8987fd046bb6cabc0b2e3e7f3576",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-2/bc189af1cac1eeec6c8d6a12197066c3eefeb97846bf34d8afb395f0f7b32b53/20261020T012816-4b14fa624ffd4bf8bf41a5e1d2abdf17/outputs/vermicularia/metadata.json",
          "sha256": "6c6a1a8b54ead0c17949e90a55a5cba5a621548212a89d840b1b76fc7a395a4d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-2/bc189af1cac1eeec6c8d6a12197066c3eefeb97846bf34d8afb395f0f7b32b53/20261020T012816-4b14fa624ffd4bf8bf41a5e1d2abdf17/outputs/vermicularia/qa.json",
          "sha256": "e6527346d61b3397b684bc34ee6a5fd1a841d054163c25ffd80c0c1b81fc48ba",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-2/bc189af1cac1eeec6c8d6a12197066c3eefeb97846bf34d8afb395f0f7b32b53/20261020T012816-4b14fa624ffd4bf8bf41a5e1d2abdf17/outputs/vermicularia/vermicularia.blend",
          "sha256": "17662696a06b1f9af30fd910264963945115ad6e73008f8a3a2e49217227f3c8",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-2/bc189af1cac1eeec6c8d6a12197066c3eefeb97846bf34d8afb395f0f7b32b53/20261020T012816-4b14fa624ffd4bf8bf41a5e1d2abdf17/outputs/vermicularia/vermicularia.glb",
          "sha256": "5bb8a455b222496fbe8568184eb2aff11b717aab29bbf42d3138707781b27f7f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-2/bc189af1cac1eeec6c8d6a12197066c3eefeb97846bf34d8afb395f0f7b32b53/20261020T012816-4b14fa624ffd4bf8bf41a5e1d2abdf17/request.json",
          "sha256": "f57b0f553fda372a6a52929b35570935716edabc88e1306f7bb97107d12ca2fc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/vermicularia/r001/rebuild-2/bc189af1cac1eeec6c8d6a12197066c3eefeb97846bf34d8afb395f0f7b32b53/20261020T012816-4b14fa624ffd4bf8bf41a5e1d2abdf17/result.json",
          "sha256": "f695ac00d24bf36bdb16ed7c49d8e94d41555079b756743d702aa1f2a866b776",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/initial/e5b2824e783f41ff2763c079180136da29ad5689349acaaf7ea775f8f92f36cd/20261020T012806-20a5230bf8164369a8ff0caedc1abdf0/outputs/weichselia/metadata.json",
          "sha256": "8466cc47b61284d0a1a6f2ef076ca2a6ae6528a05f56562a814fa77994f31043",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/initial/e5b2824e783f41ff2763c079180136da29ad5689349acaaf7ea775f8f92f36cd/20261020T012806-20a5230bf8164369a8ff0caedc1abdf0/outputs/weichselia/qa.json",
          "sha256": "808f262697999b58b586a9389c2c4c6254d403b4f5d8e9ff86a7c849963ea58a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/initial/e5b2824e783f41ff2763c079180136da29ad5689349acaaf7ea775f8f92f36cd/20261020T012806-20a5230bf8164369a8ff0caedc1abdf0/outputs/weichselia/weichselia.blend",
          "sha256": "a196ad872025a7d25f998798bde442c6654d06ed55564f9bc76f95f9e1e905fd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/initial/e5b2824e783f41ff2763c079180136da29ad5689349acaaf7ea775f8f92f36cd/20261020T012806-20a5230bf8164369a8ff0caedc1abdf0/outputs/weichselia/weichselia.glb",
          "sha256": "4ece730443de73b6c2dca2fe2bc7a50517628e344b5e6edd37486901c997676a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/initial/e5b2824e783f41ff2763c079180136da29ad5689349acaaf7ea775f8f92f36cd/20261020T012806-20a5230bf8164369a8ff0caedc1abdf0/request.json",
          "sha256": "83912c2237548bf661b942475f552e7930a390e140f9e5c94df6001cde770e6b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/initial/e5b2824e783f41ff2763c079180136da29ad5689349acaaf7ea775f8f92f36cd/20261020T012806-20a5230bf8164369a8ff0caedc1abdf0/result.json",
          "sha256": "e8c30353829ad1db7e5a205b031e1732cb57e23b8a071d26b59a1bfab859aa12",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-1/dbd0fbc429b3f51a1f419ab70c0f621c53bb0805b9791a6123e706b6d6f00f4c/20261020T012808-4dc7bd2357a24b13a067a593bc1665e8/outputs/weichselia/metadata.json",
          "sha256": "bfd3406294212f50b14b2c5b383804c570e9959e43d1951e23d60cfe1918a110",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-1/dbd0fbc429b3f51a1f419ab70c0f621c53bb0805b9791a6123e706b6d6f00f4c/20261020T012808-4dc7bd2357a24b13a067a593bc1665e8/outputs/weichselia/qa.json",
          "sha256": "beeca8088438d24178b57544bac96d4f4371e3b3b419c1f8893ef41c5e91508a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-1/dbd0fbc429b3f51a1f419ab70c0f621c53bb0805b9791a6123e706b6d6f00f4c/20261020T012808-4dc7bd2357a24b13a067a593bc1665e8/outputs/weichselia/weichselia.blend",
          "sha256": "dc684a85e95c9beb9bbcba74f115d4cf0008aa35524444e80d6da481335dfaca",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-1/dbd0fbc429b3f51a1f419ab70c0f621c53bb0805b9791a6123e706b6d6f00f4c/20261020T012808-4dc7bd2357a24b13a067a593bc1665e8/outputs/weichselia/weichselia.glb",
          "sha256": "4ece730443de73b6c2dca2fe2bc7a50517628e344b5e6edd37486901c997676a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-1/dbd0fbc429b3f51a1f419ab70c0f621c53bb0805b9791a6123e706b6d6f00f4c/20261020T012808-4dc7bd2357a24b13a067a593bc1665e8/request.json",
          "sha256": "84128ee5e918cf4f32337bffab004c109074109c63c9932b1c31e6fcc14cc8cd",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-1/dbd0fbc429b3f51a1f419ab70c0f621c53bb0805b9791a6123e706b6d6f00f4c/20261020T012808-4dc7bd2357a24b13a067a593bc1665e8/result.json",
          "sha256": "d81aea2d975259e8f38442bdab3ea635f8c38a6b75a4743b33765d72ed6e4a6e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-2/cc0c29a8287be9a40ea729d14a06128468a126599f73de96e19f7472ff0e593b/20261020T012810-295d070aab7f4f0e99def1f74039e4b0/outputs/weichselia/metadata.json",
          "sha256": "9ead5be49e9a19c7372868c65595233beeb9ed848a6c5f41d016a811f5731b84",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-2/cc0c29a8287be9a40ea729d14a06128468a126599f73de96e19f7472ff0e593b/20261020T012810-295d070aab7f4f0e99def1f74039e4b0/outputs/weichselia/qa.json",
          "sha256": "852521992d9577cdf4b88c11c0ab8007b72a88cc6c64372185417dc3d0f496d7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-2/cc0c29a8287be9a40ea729d14a06128468a126599f73de96e19f7472ff0e593b/20261020T012810-295d070aab7f4f0e99def1f74039e4b0/outputs/weichselia/weichselia.blend",
          "sha256": "12ca15768df7f32c503c84291c42eb66ea51a82e41c1080ec389eec4550c60bf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-2/cc0c29a8287be9a40ea729d14a06128468a126599f73de96e19f7472ff0e593b/20261020T012810-295d070aab7f4f0e99def1f74039e4b0/outputs/weichselia/weichselia.glb",
          "sha256": "4ece730443de73b6c2dca2fe2bc7a50517628e344b5e6edd37486901c997676a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-2/cc0c29a8287be9a40ea729d14a06128468a126599f73de96e19f7472ff0e593b/20261020T012810-295d070aab7f4f0e99def1f74039e4b0/request.json",
          "sha256": "254946b2c61b480053d0d7c0b87acb088137717fcaaf6660bcf4b6466c721e9c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/build/weichselia/r001/rebuild-2/cc0c29a8287be9a40ea729d14a06128468a126599f73de96e19f7472ff0e593b/20261020T012810-295d070aab7f4f0e99def1f74039e4b0/result.json",
          "sha256": "759f3b5e80546c1ed5240cb35dfcd9d0463d0a9030198f6e2685b7ce39ea2dfc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/runs/20261020T012755-fc9993e22e9a406d891ee5a71ec26622/manifest.json",
          "sha256": "300bda074dc0b45085be562c3c8d6b985c488e4f7e1523d96ed96c0450382eac",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/runs/20261020T012755-fc9993e22e9a406d891ee5a71ec26622/summary.json",
          "sha256": "498494e2dfb894776d2985f6ead4ae669ad695aced4aa537daf0c72ac902b917",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/runs/20261020T012908-f5df1d651afc42a2937761f4fbdec55c/manifest.json",
          "sha256": "8411931469e4a06d4a5fb9e9aa6be9624e2f5cd018b55cd5d6fd430ac7a9d262",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runs/runs/20261020T012908-f5df1d651afc42a2937761f4fbdec55c/summary.json",
          "sha256": "8119f91b055bef22919c66d47b6dc65e5450c257c3e77ba77e1f6ca81a8d23bf",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/runtime-parse.mjs",
          "sha256": "d303b43010c5622a9d89f5a4b46d8e0cd3da0cf9a0cd83bd692446b396718581",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/source-metrics.py",
          "sha256": "c90a10d0ef8a0043d2a5057b9f8e2a658ac34d1e633ffd6313e660b849b84837",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/brief.json",
          "sha256": "80d933ba49132009c2b8801c358fefb40b0c123666d84ce7a2b37baf943c0628",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/brief.md",
          "sha256": "30bfad3e97682a3734e6fde80eb65584a9d049d6d020ff2d759f16ef96936ea0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/build-config.json",
          "sha256": "8048ab06a3b10dd45189a64795a2b92de51311655955e6dd7843dac0a8fb4abc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/generator.py",
          "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/modeling-freeze.json",
          "sha256": "0c466d1abea3c0f4bdbfc2a7fa9c808d2261b6dd207783dfc3b486041b3a0856",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/modeling-start.json",
          "sha256": "b0537b2a22dfd45bbf4695ead10f20d190df3a2f899d0190c3e59a374c488dbb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/ventifact/r001/references.json",
          "sha256": "2d318b9cd1aba064a7c753092fda99f6147df49ea99d2a05384ddec775918b27",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/brief.json",
          "sha256": "772239b047fa49aec3129b38853c244e39c6ebd05c43c2e02749a9677e2d9455",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/brief.md",
          "sha256": "3175cef2fd595d8609c2b196c2309cda72ff08746202a68644a7dec342a822ff",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/build-config.json",
          "sha256": "32b0cc39c4f82b7b489f013963b0b02f61b45039e3fdcaa0bf7b3823b13eb8fc",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/generator.py",
          "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/modeling-freeze.json",
          "sha256": "ba2439c97d0a3690197a0afbaa6afbfd4d08d181eba47ba02d5d3071c7872a9c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/modeling-start.json",
          "sha256": "a7701bcea969114912c6fec8cf0d9fa3c1a3ffbf4a6f51ed9cc5179122506073",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/vermicularia/r001/references.json",
          "sha256": "85c3ffaf8b67e46ba15a0e8b845d913b473be6f14a3af617af246788ed6514b5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/brief.json",
          "sha256": "b48f62878a56e0cc5869d44f660316875b85f7e9b1fb8285b57442ed9cbfe05c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/brief.md",
          "sha256": "2ca6a26f55dcdadbe82e530af1bf64532cd71183d7ea8d557eadb1c080317b53",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/build-config.json",
          "sha256": "ba83b050bbfa90d02b5843d9ee15ab1070a58813bb55d2f15a253ba99f69dab3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/concept-generation.json",
          "sha256": "4e3edff9e108d848579125ff424d474ff0e8a435ea7536f5d53bcb4b4a9414a4",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/concept-inspection.md",
          "sha256": "f972e67f8690cc704d00e5c08bd7c489b060d99c8c679b60ddaf468cd202808b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/concept-original.png",
          "sha256": "3924d0a7857f59fc5e95a158e486b6a4b67a903311c1bf265038430ce1404d5d",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/concept-prompt.txt",
          "sha256": "7995634e6ad51ce26545af2a7bd7592947e24fb859ee48885e54f54a55c4f563",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/generator.py",
          "sha256": "7cee4c6e6aced0bd8db3cd271797a4b8b50b94ec0ff3d4f499d6cf0bc4333daa",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/modeling-freeze.json",
          "sha256": "366634e21cfe5be2d4ab3825b5bcdecb24e8377e1d7f7f4c375bd861d1adc80b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/modeling-start.json",
          "sha256": "9378e4dbdef6901df791408248b39e0449b1a8ce761b58a7b75e9c5fc54ccbf6",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/work/batch-55/weichselia/r001/references.json",
          "sha256": "5df07b75b5aec7d47d24a0f72cdfe60b9638e44ef44cd4476cf99f79d982bfac",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/INDEPENDENT-QA.md",
          "sha256": "7321a9c25b1372ee9615e485f441b5ab029bf6a081d76486babca49574e2f66b",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/README.md",
          "sha256": "9dba699acfaf8e40b9e700980a1bb2ccab60464f87840fed0f58c7427bd64881",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/SHA256SUMS.txt",
          "sha256": "33e4c50573d6c512f911d6efd79c99f612ad69ba783192fc8518e30335e336c5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/asset-binding.json",
          "sha256": "d486cf67cb242549eee8413864f7ea0a1fb8ad0004b483fbdfaff2df1d9cdc24",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/blender-import-glb.py",
          "sha256": "35c406fe3371a8fa410b3e686c808b50fce629d759f685b467bdd2e28d8eb69f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/build-binding.py",
          "sha256": "70f82b743ffe0380a18e9db7aa5375ab8e29f337e7edc48fa8560842cde39210",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/candidate-pentichnus.json",
          "sha256": "8128c81248e374d157a1a1ee78c31cc4425bfb1cb0b1e7b694b1ed502a35ca1f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/candidate-ventifact.json",
          "sha256": "8128c81248e374d157a1a1ee78c31cc4425bfb1cb0b1e7b694b1ed502a35ca1f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/candidate-vermicularia.json",
          "sha256": "8128c81248e374d157a1a1ee78c31cc4425bfb1cb0b1e7b694b1ed502a35ca1f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/candidate-weichselia.json",
          "sha256": "8128c81248e374d157a1a1ee78c31cc4425bfb1cb0b1e7b694b1ed502a35ca1f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/concept-evidence-pentichnus.json",
          "sha256": "38ce7e4f46d9af7a498bea80840fbc38cc4cc2af36c6610514d61720d6684c41",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/concept-evidence-pentichnus.txt",
          "sha256": "38ce7e4f46d9af7a498bea80840fbc38cc4cc2af36c6610514d61720d6684c41",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/concept-evidence-ventifact.json",
          "sha256": "4bcb34d4d16c6f607cec6ee518a7db286fff6b40cea39744d3deb86d4d5f2612",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/concept-evidence-ventifact.txt",
          "sha256": "4bcb34d4d16c6f607cec6ee518a7db286fff6b40cea39744d3deb86d4d5f2612",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/concept-evidence-vermicularia.json",
          "sha256": "3d010f84398b481bb99590b47c1a37ad6c9163f2549cfcd15d142853eba51edc",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/concept-evidence-vermicularia.txt",
          "sha256": "3d010f84398b481bb99590b47c1a37ad6c9163f2549cfcd15d142853eba51edc",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/concept-evidence-weichselia.json",
          "sha256": "d9928fbf34f951bc94f0a16b075ec0a2f73d623d16d502c7bd95b608d32c114d",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/formal-checks/concept-evidence-weichselia.txt",
          "sha256": "d9928fbf34f951bc94f0a16b075ec0a2f73d623d16d502c7bd95b608d32c114d",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/glb-reopen/pentichnus-deep-dwelling-trace-r002.json",
          "sha256": "11df266178f2d7c9f8c05f8b53b936fe4a83af6fc74f2f05fdc37f00f6542426",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/glb-reopen/pentichnus-deep-dwelling-trace-r002.log",
          "sha256": "79a954d82682b1428f6d1a072a6bd47492d7f98c550d34c51c04ba7ec37c3a31",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/glb-reopen/ventifact-r001.json",
          "sha256": "0632f711df4f65821c33952f0c9797e45c1e5564eeade936e5ae30fa7f14b185",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/glb-reopen/ventifact-r001.log",
          "sha256": "3e325d1136628e2f00fda4a1959dff7f4b1f9b5dd58dd692571c6426164eb8d7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/glb-reopen/vermicularia-r001.json",
          "sha256": "a4dc2e57501bfa6f141972d94eb084fd72a735d76dc3430436b494f438857fd8",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/glb-reopen/vermicularia-r001.log",
          "sha256": "feb37eb0ee3e967ad787bf8ea7d488ae3c75fe4de89be039388834a18581d561",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/glb-reopen/weichselia-r001.json",
          "sha256": "9e7e6c80fca1997bdfe70565a677d932e728be974fd2f281d0bb89b3f414de2a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/glb-reopen/weichselia-r001.log",
          "sha256": "4f4867805eb02768d5cd2a2c68ef23f76f083dbaf2018e29127d33b8bc0dd95f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/pentichnus-generator-r001-r002.diff",
          "sha256": "b6180f661bda834fffaf94ffae2d9f5e4b7c559de62be665a3d15d45aca8cabc",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/pentichnus-r002-repair-note.md",
          "sha256": "6c39f632c6bc84ad884fa89a16d49ba3f96f7816172b8f29195898133cde2351",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/reproduce-static-audit.py",
          "sha256": "696f3f7c326115fbeff316f78b029feccfa5861bc1f24995e7ad5936efed9b68",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/reproduce-webgl.cjs",
          "sha256": "360bba40f3a1603a4e13a09f5cc1bd7a58d6ab21d1ee98237ea6d90ffbd9fcf2",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-pentichnus-deep-dwelling-trace-r001.json",
          "sha256": "9dd849e7c65c363779a273005273d5bb555948cbb634cf2f72494eadc68fd5f7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-pentichnus-deep-dwelling-trace-r001.log",
          "sha256": "a9a2e1fab13211fedb5f3f9f04a00009073706c2e2572e2442a558161b393908",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-pentichnus-deep-dwelling-trace-r002.json",
          "sha256": "c572d8b08ff9f36550f64c6625d33e9c28d6556bcd9b4f83be77f15ad77a50b9",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-pentichnus-deep-dwelling-trace-r002.log",
          "sha256": "96fce425c2125d8e46be553ca82a0eed4314c6971034d7a9e72591cf81c11680",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-ventifact-r001.json",
          "sha256": "11952bcbd4ef59ca8d3b5d8da6863f8148c8d5276c8b2bddf54bcc18b51d1e99",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-ventifact-r001.log",
          "sha256": "206e54d01e1c98668f9154f46e66465a50edd7718c1280062f891f82b77232e5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-vermicularia-r001.json",
          "sha256": "d2dfd98d0c1aea2b150583bcc0e2a2dc87823d709fb84f241ef44ec70fc6c862",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-vermicularia-r001.log",
          "sha256": "b2711001cd65b4190b649e04b3bb4f352491e1353ced92d37b0408f3c510e7a7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-weichselia-r001.json",
          "sha256": "1fe9b200f7ad3343f802ca71c36f5028fbcab5840b24a5c50ae5d67ef09900d3",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-export-weichselia-r001.log",
          "sha256": "4a3d25883305f12a960a9a44dd6f63019aa33e05950921820e9c32dd3a970446",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-pentichnus-deep-dwelling-trace-r001.json",
          "sha256": "53b2110700ff99b059d3a8ecf325a4ae12393f824ac19ab7f9441ce6a82cd17d",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-pentichnus-deep-dwelling-trace-r001.log",
          "sha256": "245276ec7bbc27bf802eb32052c844d0beec254cc8f58c2520382e4d1d77ed8e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-pentichnus-deep-dwelling-trace-r002.json",
          "sha256": "e8f5f6670252d7dd8fe00f7c922094270d964709061d68383e9da541cc991bc9",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-pentichnus-deep-dwelling-trace-r002.log",
          "sha256": "3f92d4c99bfad2c63b249a7b169d7d06e3f8605177bb29c041ad0ad2a0ab9486",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-ventifact-r001.json",
          "sha256": "97ec51f9e5f62a21db74213a96720b30519a77f67299a2fe80733ffd60f7713c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-ventifact-r001.log",
          "sha256": "3878227607970e0b59c23db1268b11fd1e1d11a97e0ba3dc64734a665100d0bf",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-vermicularia-r001.json",
          "sha256": "09c13a32f8ea4463785a6fe9e0fc69c208972f00bb9fe2da4047be9cca2c941a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-vermicularia-r001.log",
          "sha256": "b92994784d5bb0868181a55da4daf2dbcae8dee910a53fd57b08376c92d52e41",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-weichselia-r001.json",
          "sha256": "e24c0e6ee62edae2d8d2799055507ee0c7f1b9aba3d170c14627026da493e60c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/source/source-metrics-weichselia-r001.log",
          "sha256": "2aa7471e65764d7bc6b9bc23f1bbdf313b163647f09dd4f36a5aa4febfbd60d0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/static-audit.json",
          "sha256": "43fa69f7c18421eda4147081675951766290fa39e79039e674e57c0edc846688",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/pentichnus/gltf-validator.report.json",
          "sha256": "7ae05648cd09f40113b5fc4f8db185c956ef91833131526524e78fb1319af0c7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/pentichnus/qa.json",
          "sha256": "c4850b48d9ab7cb6dc9005ac7e6327ce03ae7c7d9c84968da459f7fb5d1ba54b",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/pentichnus/validator.log",
          "sha256": "7ba7603d631358123a1dcaf4e1b76a6371803e59d831cd06d0ad9af4402de208",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/ventifact/gltf-validator.report.json",
          "sha256": "3e0e6286c0c1d10b035c3f74260c9af10d811385de0ae06906d7716b23b4188a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/ventifact/qa.json",
          "sha256": "af8bd31a1c689839749868f885bdaa9d8dc4056cc6c0d06fd61903ccb09f61f3",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/ventifact/validator.log",
          "sha256": "af10ac4bd98cf4e64767a1e7c5faa838f57032621fd9b0e82b80605bf0210ee5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/vermicularia/gltf-validator.report.json",
          "sha256": "edc2b9463cb9f978e60d23a9321ab84540c598faa5ec6009092eaf109f6ffd3f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/vermicularia/qa.json",
          "sha256": "9636cd2698cfaa067bac4a7f42341e0fc226a55f0e1168fd36eb43addd5624fd",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/vermicularia/validator.log",
          "sha256": "f961da0313d07d16bd4d5f224fa8acd110656399dfd9963fe538cb37d9c381b0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/weichselia/gltf-validator.report.json",
          "sha256": "811e1dfcb262599b03bb53215b47c8c020290b280b96a03f472f69ec715b7501",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/weichselia/qa.json",
          "sha256": "9dc99dcfd8600313aff3cc79e04bcf3581b2919376362260fa4f8f8782d1cdb1",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/validator/weichselia/validator.log",
          "sha256": "2518e33a4c127c2dfb73b8fe882d899e350413865ed3ec9b12dd32c075c2d560",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/webgl/four-asset-smoke-scene.png",
          "sha256": "116914057c51eeaa5ad6405d8daf61de652f7741cc94d44ae547506db945b967",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/webgl/pentichnus-deep-dwelling-trace.png",
          "sha256": "27179006fef9d304db25c1c1de65b98afe6ebe700fa39910830ae13b5a5ab69a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/webgl/software-webgl-report.json",
          "sha256": "ee06ef8e6179088ccf2695b1c9bf804d725330304651f4307444812163e0ddd2",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/webgl/ventifact.png",
          "sha256": "9d1680860169900ecd6aa32593a7976a580e9d4ac71afdc179564afbf86e8cd2",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/webgl/vermicularia.png",
          "sha256": "d42d360ebd5b19542bd00cb42f46282557d4eef5cd6fd669e234e24efa7ed5b0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/evidence/webgl/weichselia.png",
          "sha256": "4c1c4d27871d77444aa418727eed83fd3f6750a6acd210f15b4b0994c92b3f33",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020/independent-qa.json",
          "sha256": "a34bb0ab2f412ec9a19708d3a74b8131679f04f40c1867f9dd33e8e6b38a0f97",
          "origin": "review",
          "owner": "$batch"
        }
      ]
    }
  }
];
