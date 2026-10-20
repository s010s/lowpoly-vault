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

/** Exact bounded Batch56 release; unchanged formal gates. */
export const BATCH56_RELEASE = {
  "version": 1,
  "scope": "batch56-20261020",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "provider_generation_timestamp": "unknown",
  "source_commit": "1e90635f5d3bc9940f23fb17d3d581cd8f409170",
  "review_commit": "adace4d7fd4cd091ab63f60ee4737f77096ba666",
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  },
  "base_descriptor": {
    "path": "assets/releases/concept-landair-20261019.json",
    "sha256": "bb8e0aa3846a0cca9b381e675a988b756c652546efb44405fb4b27927895136b"
  },
  "source_bundle": {
    "path": "qa/batch56-release-20261020/source-bundle.json",
    "sha256": "5ae1d1fedfc49669efb09529c4e9e6c0f6e7896c237ac27cd6f5473f1ac2a435"
  },
  "review": {
    "path": "qa/batch56-independent-20261020/disposition.md",
    "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c"
  },
  "capture": {
    "report": {
      "path": "qa/batch56-release-20261020/capture/render-report.json",
      "sha256": "c1ed101baab8a80cfef0e2b4c479b411374f23b46bdee79769fad7d279badf44"
    },
    "index": {
      "path": "qa/batch56-release-20261020/capture/assets/turntables/index.json",
      "sha256": "9e680d380178684ed2ee52fb035bc32d0169bfa7c71b754931e468b9f281d90f"
    },
    "zip_verification": {
      "path": "qa/batch56-release-20261020/capture-zip-verification.json",
      "sha256": "3079fcf81466fd1aa05a460e4a98eb1ceb9156c43406beb16e379cabc827000c"
    }
  },
  "excluded_ids": [],
  "additions": [
    {
      "id": "cycadeoidea",
      "revision": "r003",
      "source_commit": "1e90635f5d3bc9940f23fb17d3d581cd8f409170",
      "review_commit": "adace4d7fd4cd091ab63f60ee4737f77096ba666",
      "metadata": {
        "path": "assets/additions/cycadeoidea/batch56-20261020/release-metadata.json",
        "sha256": "1fd6281b3afbf7d067d2eab28755e4b171a08ec91252922a90ea006953505104"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/candidate.json",
        "sha256": "3cdd60e83969011b064852e05e8ba81053716f77ffcf9f0fb372f58bbcf7afe6"
      },
      "review": {
        "path": "qa/batch56-independent-20261020/disposition.md",
        "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/metrics.json",
        "sha256": "d0b686086b4d2cdb1ae6e37178b757b238ad4e84f0b2cc1bcb8e0b1ee7fcb5f6"
      },
      "original_metadata": null,
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/brief.json",
        "sha256": "565e599fe3326edcfe53774d1da297c7c44623cbc83db884c068bb0154aa91e4"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/render-manifest.json",
        "sha256": "c4169c245e0b3c95ae8587f48aa8a352da8d06d4e05ccea982943e882e9e5755"
      },
      "capture_reference": {
        "path": "qa/batch56-release-20261020/capture/references/cycadeoidea.png",
        "sha256": "11de5a9d35f3f1084666f37ad577398687888fa39e8efd6ce4ac1b44fb6f18d8"
      }
    },
    {
      "id": "gondwanagaricites",
      "revision": "r002",
      "source_commit": "1e90635f5d3bc9940f23fb17d3d581cd8f409170",
      "review_commit": "adace4d7fd4cd091ab63f60ee4737f77096ba666",
      "metadata": {
        "path": "assets/additions/gondwanagaricites/batch56-20261020/release-metadata.json",
        "sha256": "df11c2dbb5bb022f98b1f6eb0e5aa1d8f9ce4821ce8966675667036b79d71fe9"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/candidate.json",
        "sha256": "4972be24873fcd14501c7e39b02cbe1b6e7b9922dcba10cd3bdf7f527f893341"
      },
      "review": {
        "path": "qa/batch56-independent-20261020/disposition.md",
        "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/metrics.json",
        "sha256": "a9814f8f19ce2c5b5662e9ed63ca8a1e3544dd7eb895c54f30cec116d19f02c0"
      },
      "original_metadata": null,
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/brief.json",
        "sha256": "ca5dcb8fe58a9034b4a7c5ace7d4a04202d05e390b15d71f10f318c58dc88fc3"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/render-manifest.json",
        "sha256": "5368ccec266d2fc43942eae6062622bda1642a86037e0a0b38d20cb271a08f84"
      },
      "capture_reference": {
        "path": "qa/batch56-release-20261020/capture/references/gondwanagaricites.png",
        "sha256": "2853d0b7d6909d5aa12bbf25ea0495fa275b6263d01cb2809d35761376f98935"
      }
    },
    {
      "id": "deflation-hollow",
      "revision": "r001",
      "source_commit": "1e90635f5d3bc9940f23fb17d3d581cd8f409170",
      "review_commit": "adace4d7fd4cd091ab63f60ee4737f77096ba666",
      "metadata": {
        "path": "assets/additions/deflation-hollow/batch56-20261020/release-metadata.json",
        "sha256": "3079e2c699bcf406ad4fff2825d271953610f984775c7de0ee45a680f4c53b98"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/candidate.json",
        "sha256": "701168809517d06280bbc7b5b6c12a24d801a32bb2679c00e0d96e32d5ff879c"
      },
      "review": {
        "path": "qa/batch56-independent-20261020/disposition.md",
        "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/metrics.json",
        "sha256": "9155120f576fd19b6b27590c424a06a84026c52f7a614721a6199abc8fa4cf8d"
      },
      "original_metadata": null,
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/brief.json",
        "sha256": "b5dca761406ec90f845ab283f9efc55b305acf66a316052439ad54c655da26ac"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/render-manifest.json",
        "sha256": "ca6ad46122b610219f4a8b91572e013120c61296f39ec88411b417263bea3ddb"
      },
      "capture_reference": {
        "path": "qa/batch56-release-20261020/capture/references/deflation-hollow.png",
        "sha256": "2f01afbfb29c8564d5ad353c5bc1c195d4eeea3991c088b5756a4e97efc5e6b2"
      }
    },
    {
      "id": "arthrophycus-annulated-burrow",
      "revision": "r002",
      "source_commit": "1e90635f5d3bc9940f23fb17d3d581cd8f409170",
      "review_commit": "adace4d7fd4cd091ab63f60ee4737f77096ba666",
      "metadata": {
        "path": "assets/additions/arthrophycus-annulated-burrow/batch56-20261020/release-metadata.json",
        "sha256": "15356dd4a6781c0d3c94fb0b019f85d939fa805c10af49875ec3759365b06dd7"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/candidate.json",
        "sha256": "18c115bc07d4b339d5467b1f30ae481f6e59c2430374fb77cf2d87ffcdd1f040"
      },
      "review": {
        "path": "qa/batch56-independent-20261020/disposition.md",
        "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/metrics.json",
        "sha256": "12747b6231261f7f3685baddbf76be63d3062d5e92561e493d4570f7ce50234c"
      },
      "original_metadata": null,
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/brief.json",
        "sha256": "ba3a9d13f09d0a7da99b4f39f23907e7fdc6b1d085e868cc808516392c0d32d3"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/render-manifest.json",
        "sha256": "dd8b9722e97e023169a855f986684a958fa40bbebb858b7c56da3763eb65e53d"
      },
      "capture_reference": {
        "path": "qa/batch56-release-20261020/capture/references/arthrophycus-annulated-burrow.png",
        "sha256": "1c00c7b171083753aba0a485da5806ab7ff5fec574d7813f39698266d591204f"
      }
    }
  ],
  "files": [
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/brief.json",
      "sha256": "8968592cc06b16d97beb45d21bf68661053d62934165d239146e80c841721d00",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/build-config.json",
      "sha256": "321596ccb5b05f49ab759277a7d275e3879d5fb2c7985c9f6fa6384c1341b852",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/build.log",
      "sha256": "1c0119d62800ff50ef8d7bda62084504925c4d97bd69bebcce25f0984e1f0b45",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/concept-generation.json",
      "sha256": "03662507be4e1c578f28294891d85cf582533fdb8de8579ac392c0a202099950",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/concept-original.png",
      "sha256": "7285ce56f8ede05348925a4480669500f32dc7ee9f2c7f53f1cd0f8fa19fb246",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/concept-prompt.txt",
      "sha256": "6c9914d0db89a006731268e03ce94b65cd2873657604b2aed5a220e98d24a31c",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/dependency-hashes.json",
      "sha256": "f440e920943401d0f28112fdf1da0da2f15357b997200d9b208dc35d2968a543",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/format.log",
      "sha256": "4306e85be5a73d12426cff3b05583ffea4f2a18e8649b977cd813c3279745926",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/generator.py",
      "sha256": "d496960e7ba16268b8b7e0575d96032726dc3630c53bb0b469af54d20f6ba3e8",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/gltf-validator.report.json",
      "sha256": "67582c945c1307b1f8385e1df49baeae760f29bc0e6a7a36e9bdc710a76198ee",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/lifecycle.jsonl",
      "sha256": "f37948c1886ae2f5690c5bbd8617b23434daababf2af7aa8801b61408e35d690",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/metrics.json",
      "sha256": "9fa196e5d7e83ecb36899e8ac136b7ef9ad9dcc26b4e51770b843b14f6e2f7ed",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/model-start.json",
      "sha256": "85751d7e21dd3e8ee84d79501c5a996bac651efeadb7986371d5a83538545769",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/model.glb",
      "sha256": "ce68d66fa8c50817f7eb69b067a340d12fcf875ed5a1e4d0357f0fac33fb2a43",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/modeling-freeze.json",
      "sha256": "3e5e000ab0469db5769010aed9b66650b11562bbe254eb266e9997044b1f4539",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof.log",
      "sha256": "5e3ee3fdcf8708d07dbed16e07b88de7c883b04f89a2b19f573ffac8107431fc",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/clay.png",
      "sha256": "251341b0d5ab9ace3599237d565380eb4258109bc31595deb536f80e14a8eaa1",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/front.png",
      "sha256": "4b3bccad72780843a338bf557b3e4cf16cfd0e12f14b8b6632651f55ee091efb",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/hero.png",
      "sha256": "0d656cb7dbcff3826fb0072828ea9dfcc65bcc134d17cbb94adea1ea4386ce8b",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/rear.png",
      "sha256": "7fc4d29822e12e7ac07cc41295f77cff9f3e888cde02f8781f00e24fe612c0f3",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/render-config.json",
      "sha256": "5abd484a18f293332cc997e6f60a9fe32fa59f78037b0a21907d1dca968f5352",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/render-manifest.json",
      "sha256": "e445e772dbb76e63e115cc917b6bf388c1ae10a39ec14483c7c6fcce985f0c56",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/reversehero.png",
      "sha256": "9080470fa8291018cd717185d1535afe766b4d9539a19b8cd7fd361ada1efeb7",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/side.png",
      "sha256": "e390391f54629a1a48d41f14b742708aa4f913750d2ca07d4c461d68f9ecd930",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/top.png",
      "sha256": "8b94b391bf0082628e6e1101c7293b7aac8be91a58b1f2107655df572a70eab0",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/proof/turntable.json",
      "sha256": "c7253a1a2ee5dc74fe0b37c07948d94ecb1868475169d83fa1d3d4528d470632",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/qa.json",
      "sha256": "2f0eab612ead34cdda4f474e43800d7d5f40ab66beb7ee9f2fc2841b637fc6bb",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/rebuild-1.log",
      "sha256": "b0799a3a2076d692092aed9ec6beb6566f619c995616b8ae1a6244e716644cf4",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/rebuild-2.log",
      "sha256": "eaff2625b4787f2525aea49021948914f578c0e2bec7feb222424f95bc431dff",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/references.json",
      "sha256": "7ef651ed04c394a5f3cddd60763dfbf6f6cdc224c091fb6e69f854f79c419aa1",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/repro-1.log",
      "sha256": "9615d94dfe4314508d7c7e57b424d87c618c684a9dbb4815ea675f493026c177",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/repro-1.report.json",
      "sha256": "9615d94dfe4314508d7c7e57b424d87c618c684a9dbb4815ea675f493026c177",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/repro-2.log",
      "sha256": "45fed6b0fdc49c25ac9b855c795cc7393a208061924101c6ecd76fbbd84d53ec",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/repro-2.report.json",
      "sha256": "45fed6b0fdc49c25ac9b855c795cc7393a208061924101c6ecd76fbbd84d53ec",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/runtime-parse.report.json",
      "sha256": "8e18d9e592cdb795717e9a9ff19bf3317783ad50c89f6b13e966d4fc5dbd612b",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/source-export.report.json",
      "sha256": "5a9e3c21bc760fd8299dbebc768111175f87891f8bf71ba3ad3fea68e4aee3ac",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/source-metrics.json",
      "sha256": "ab8f397570b60753f9793830babb900a41dafc6679a49ef6e7a3f042d78b3337",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/source-reopen.log",
      "sha256": "ba2a669f6034bfed07aa3102a8c4b6dba18b1f6751da746aa8e3ce08ebee18a1",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r001/source.blend",
      "sha256": "b69f17c244352a701c718b37a1477a7ccee0f73147c73bc0f57d0f8a6a48a71c",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/brief.json",
      "sha256": "ba3a9d13f09d0a7da99b4f39f23907e7fdc6b1d085e868cc808516392c0d32d3",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/build-config.json",
      "sha256": "fe161902d34604cc622a39ad25c12c04069d5a2873f2e264c8a117007beb6a39",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/build.log",
      "sha256": "88aefb5e479a9fcc250fe00aa0691b3eea85b5f7fd021fb4a04bd8f0bd0fb86e",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/candidate-brief-adapter-v001.json",
      "sha256": "32a4ff407390b40364ee3e65e2c9bc3be4edcaa3f37a483d1de8bf84be1391a8",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/candidate-brief.json",
      "sha256": "c7f94914c51dc43bf748c852abbbbb48da8e35f52b96a746cdb08b48b2ff155e",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/candidate-validation.json",
      "sha256": "7c94e216462a5a0b58f6d6595303baac71d001b5a181687297b6cf69c6fdb542",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/candidate.json",
      "sha256": "18c115bc07d4b339d5467b1f30ae481f6e59c2430374fb77cf2d87ffcdd1f040",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/concept-evidence.json",
      "sha256": "edbb64f99231bea061e6a1fb50b7c1481a311d9cf1ee30f4bc8cc84144390052",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/concept-generation.json",
      "sha256": "03662507be4e1c578f28294891d85cf582533fdb8de8579ac392c0a202099950",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/concept-original.png",
      "sha256": "7285ce56f8ede05348925a4480669500f32dc7ee9f2c7f53f1cd0f8fa19fb246",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/concept-prompt.txt",
      "sha256": "6c9914d0db89a006731268e03ce94b65cd2873657604b2aed5a220e98d24a31c",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/concept-validation.json",
      "sha256": "d4a09d3acc9f7c8d5a8a6199b7b7f4214092fa75aa4fe1d15d6fe06173209562",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/dependency-hashes.json",
      "sha256": "f440e920943401d0f28112fdf1da0da2f15357b997200d9b208dc35d2968a543",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/eight-view-sheet.png",
      "sha256": "4b021c35b2057e93a3e761d40ad6216ba00377168d7e02ffbcca414ac32737c0",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/final-stage-times.jsonl",
      "sha256": "1ba3e37ec3734548f438a6b38c3fe79a689c5fbdd30e08c828d5dc54fd721c4b",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/format.log",
      "sha256": "751e83cb0a04ce6f244a89458f9df28c507eb05d87ef526ae23e9813c0737833",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/generator.py",
      "sha256": "7ec20ae9f2106a627a5f2ff7bdc01e393966a2a98bcd23a395e02e16ecbf5161",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/gltf-validator.report.json",
      "sha256": "3c9b83d4bea2bf9d5f2a04deba170222087a043b0e294123ac8feea23c0ea276",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/maker-review.md",
      "sha256": "6175ae9c27e480a31efc9c3098626d22194db11e3c676eb9691559358ef634f9",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/metrics.json",
      "sha256": "12747b6231261f7f3685baddbf76be63d3062d5e92561e493d4570f7ce50234c",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/model.glb",
      "sha256": "a32b30732582580884b7f6de257a22c701df20f2359e9183585a10a8f959834c",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/modeling-freeze.json",
      "sha256": "6bb5acb5bc208d09734c64cc454a299e23e29af6147a5fbdb2b80a24c74a005e",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/preview.png",
      "sha256": "cb89f593ad76a276b62659cca5ea1a3b739582e37fa0dd8d04a89691f9136734",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/profile-contract.json",
      "sha256": "7e3dce37aad451c0a146f8d7b7beaab8d701dc379046ea00421d2a55d75903e6",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final.log",
      "sha256": "4d8b0b9be5daa919d4b2703db8099126016c18fb222d105f994ed7abc4f9e334",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/clay.png",
      "sha256": "e997344f185cb92f61310195baf96b858c93c5de20f172c497d98346d217b818",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/front.png",
      "sha256": "bd4a5be6f749b9857fa2e6cc1f2c1e9b3f7872065037b3c5f42ec0881f5ee3f1",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/hero.png",
      "sha256": "cb89f593ad76a276b62659cca5ea1a3b739582e37fa0dd8d04a89691f9136734",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/rear.png",
      "sha256": "66861720eac2d457fdfff1a643e70a485bec85d1d11601d439d800bd09eee4f5",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/render-config.json",
      "sha256": "24c8afd228c76256ec6a719fbc01c8368e3b8da8017d9484b9e3019b93722397",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/render-manifest.json",
      "sha256": "dd8b9722e97e023169a855f986684a958fa40bbebb858b7c56da3763eb65e53d",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/reversehero.png",
      "sha256": "8774bfd09351cefb4d88dc1d4da996b774119fc0f056a60c9c6c12206e7a4683",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/side.png",
      "sha256": "0b6816904f070c945b53a8c3c9fabf2d637afda192336f98043d644e014de8b1",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/silhouette.png",
      "sha256": "cf23db3d779f9c52db032b13ef65e6ed17ed030940758d33106147068ee7d7c5",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/top.png",
      "sha256": "2e0166e090210aec180cd6b9a80d74bbda752fae9c600bd2a41ab24a48ce90d6",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof-final/turntable.json",
      "sha256": "ed044e106cf65e43d8571670c2868b742752b16e9563741957e8e769d33db675",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8.log",
      "sha256": "f6f35fdd77341c76f542f13d61c6a702775348b7e63451fa21352b8cdd598b9b",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/clay.png",
      "sha256": "9db5d47e961577b2c9f8228c6a94d906964da99dfb66392d11b2e86e82010a0e",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/front.png",
      "sha256": "b132bec91da6f7fa86bfd5dfe039f67afd19ad85a1200689e4443ab11d56d2f5",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/hero.png",
      "sha256": "e1976dbf0603b5db27f37d2198b74d28503f2df930d121aa65a33a60f60f5750",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/rear.png",
      "sha256": "836533ff3778a377c428fbc083c19787f036ef83ff351934cca5c13fd37c2fa4",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/render-config.json",
      "sha256": "0e94691ffc046305870f4ba03c6b6475194f07b025a4b5d8b72269b486e77c41",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/render-manifest.json",
      "sha256": "07475292f599fb313d955bba980d20a8ae59d93443ae4e05825ce8238628defc",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/reversehero.png",
      "sha256": "342ea43959fb2d93ca0748613d8a0fe4033c59e64993bbe65ddcaac26ea9e80a",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/side.png",
      "sha256": "16907d8f0b484e493b82fa4d4a44e96f2776971b9d1b717d28f2b94ccba874f0",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/silhouette.png",
      "sha256": "5485f0850a784167ef80404b50fcbf4f2168d2577135efd5550aeb230131feaf",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/top.png",
      "sha256": "5100018cd163e17b533430ba52296f4439d309588b9bfb7df34461edf4d2aa7a",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/proof8/turntable.json",
      "sha256": "9144223c9d1bd821bd47ec24f8142a47c078fad6582867e008509749b5aa585f",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/qa.json",
      "sha256": "2c7c4f0f3ffba2dcfa9d8dec513e4957b5c563b211df33d53aef960a85a611d1",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/references.json",
      "sha256": "7ef651ed04c394a5f3cddd60763dfbf6f6cdc224c091fb6e69f854f79c419aa1",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/repro-bound-1.log",
      "sha256": "8082006fd99c96df8d462fcc34dfc2492210b8d456b80ee53c18f3a50764b9d1",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/repro-bound-1.report.json",
      "sha256": "8082006fd99c96df8d462fcc34dfc2492210b8d456b80ee53c18f3a50764b9d1",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/repro-bound-2.log",
      "sha256": "0cbaf74d434210c7056f8e606a47d21d9bde0a0e879af0a83483083288d36146",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/repro-bound-2.report.json",
      "sha256": "0cbaf74d434210c7056f8e606a47d21d9bde0a0e879af0a83483083288d36146",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/runtime-parse.report.json",
      "sha256": "0fae8ca354f7f5cb629dbbbca9c1ac0063adb76e01f9c8b0b1417bcc4b3f4e42",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/source-final.report.json",
      "sha256": "40e9d0e86fbc3ce2fd91efefa1c7a59166ae7da0a03c63e2a12f2a15da91708c",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/source-metrics.json",
      "sha256": "ab8f397570b60753f9793830babb900a41dafc6679a49ef6e7a3f042d78b3337",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/source-reopen.log",
      "sha256": "32762b0ba89fd47e60d6896596d46be27f36164167cbc85410b5a3ff1636a7e2",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/source.blend",
      "sha256": "3c9acb026a5bfbf485a802b887cef664b462d9208410e03cec086cd84838cc3f",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/arthrophycus-annulated-burrow/r002/vertex-counts.report.json",
      "sha256": "11f8431204715514530d4316cc3b288455cd5beb87b32cb0dc160d7616e20283",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/brief.json",
      "sha256": "569215636a38b87f8739e06a6ab78db9b8797aa7e8f2f9150d74c28347c2b8dd",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/build-config.json",
      "sha256": "57517e1adae6023099de3973d4de7cd81acf619843f3f4737d46d2f19d22293f",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/build.log",
      "sha256": "d0eb1b67bbd434f3d5a6cd72a0aea907cb2f67740df8f33abd6055cc591041c4",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/concept-generation.json",
      "sha256": "03662507be4e1c578f28294891d85cf582533fdb8de8579ac392c0a202099950",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/concept-original.png",
      "sha256": "7285ce56f8ede05348925a4480669500f32dc7ee9f2c7f53f1cd0f8fa19fb246",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/concept-prompt.txt",
      "sha256": "6c9914d0db89a006731268e03ce94b65cd2873657604b2aed5a220e98d24a31c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/dependency-hashes.json",
      "sha256": "f440e920943401d0f28112fdf1da0da2f15357b997200d9b208dc35d2968a543",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/format.log",
      "sha256": "5988eab26b05caa34c2e5c0e8ba88d838ed3a9d72381323f65612beda26523ef",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/generator.py",
      "sha256": "d496960e7ba16268b8b7e0575d96032726dc3630c53bb0b469af54d20f6ba3e8",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/gltf-validator.report.json",
      "sha256": "774d1efca82e54d48875b9957cbdb39867ee8bb0f7b83fb5c9dc467241fc9f42",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/lifecycle.jsonl",
      "sha256": "38afb9795cfd95caad137acd1e0133cf8928fb77d2bc59e687e06230d0a63c90",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/metrics.json",
      "sha256": "27006ec30d6370c8685c903e67f40633ff2399ce5762a7f916687df10f24d27a",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/model-start.json",
      "sha256": "0b802ddc3cf37c6f50be3c0180d4a6c5d1ad04055d501bc461698736e7162533",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/model.glb",
      "sha256": "78de39e5920c008fc7dd0cef55a27d6b177155e57248f8698830e74d60e7b256",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/modeling-freeze.json",
      "sha256": "1280aee8bb7ed3ea8b7f43f12400777c86f6007a8649211d22654c1f53030391",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof.log",
      "sha256": "25a72d095b0bbd8f8bbfc2054c20a6ea74568d8e93cb83d17f22d5d331641a8c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/clay.png",
      "sha256": "d213140c3a9a0d0d2f2c12cf1b0bdd835b196d287012bde5b92e8dc3d7f15f4c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/front.png",
      "sha256": "f03aff4d07a4f8f19f77c7c150ae8ee684d40b710e4f219954fa2cb4645c7c5c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/hero.png",
      "sha256": "3cd30f6ca46a7831da06ba021903135342658e10382cb0facc12d685abdf6856",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/rear.png",
      "sha256": "f9bbf9e2b23b39f83e47b86aa4606309454755abba9a2e5d2efd298aa7c2ab89",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/render-config.json",
      "sha256": "388f2d29575be6e480f8f71b30207e338146edab8d564682d960805ed131b443",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/render-manifest.json",
      "sha256": "04d2e4fb7ba1791ac30393921e46d40a22e1937df5be2a271a878761969efd21",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/reversehero.png",
      "sha256": "1540d69d9c50b868b21543aaa6c8c7c718f825c9e0f7af46b5c41d392d306b9e",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/side.png",
      "sha256": "73338f65d314180d324ebe06e7602337fbaa891b5f904ce631d4ffaaac41eac9",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/top.png",
      "sha256": "86c329516cd0940c03754260c22cd0a19e84f80d4d3a164976f121be4c4d42be",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/proof/turntable.json",
      "sha256": "1dfdd38ea5a077a1b144647b21351369f9055f236520e6d054db25450cb25446",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/qa.json",
      "sha256": "a1129ed9802148af644959bfaedfc6eeb5707d76a00a4425bfb10d3e9eb70489",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/rebuild-1.log",
      "sha256": "38fe8a35a55bbbcbfd63910a7ca73d5505b51118d19e174c2b39e4be6c2ec970",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/rebuild-2.log",
      "sha256": "0c0b253c8606174319283395fd9a518f6f5131417513fc94df38ecacada2a902",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/references.json",
      "sha256": "458814d5f92eb057f1071eb87439783dca48bcb5c74803364afd4a86525d1eed",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/repro-1.log",
      "sha256": "3af7ff01fdd7ad417126b56e1ad9d0de321bbe2f81236029055d9986e969f3ee",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/repro-1.report.json",
      "sha256": "3af7ff01fdd7ad417126b56e1ad9d0de321bbe2f81236029055d9986e969f3ee",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/repro-2.log",
      "sha256": "a4b84f28c86a8be9956b29cc3c026f73a2a964a972cc04070bff20594015e37b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/repro-2.report.json",
      "sha256": "a4b84f28c86a8be9956b29cc3c026f73a2a964a972cc04070bff20594015e37b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/runtime-parse.report.json",
      "sha256": "c599c8dddc7d5aca12fc1aa6c6b4c82c63710ad28a20b8287b019d5b64f597b0",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/source-export.report.json",
      "sha256": "cabe649427d6e73070d5c0a5a7f383871c0001c03c31aace5a8f0d9062a93058",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/source-metrics.json",
      "sha256": "1b8271d7f20c042a8329805bf824ce87d59881f874c3319d2b7c0d14ed1cf449",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/source-reopen.log",
      "sha256": "c98a2e39ef0e0bf966fed42e56a4acc74211fbc7946f6a92e743fd5d06be0516",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r001/source.blend",
      "sha256": "56c5e7fe1a0c4fbcc038ac7a35c415b10ea2129434a35f90652fba3962c58263",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/brief.json",
      "sha256": "565e599fe3326edcfe53774d1da297c7c44623cbc83db884c068bb0154aa91e4",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/build-config.json",
      "sha256": "9e64f92fdcc7af87d84f2c0418617cd87c6993a6f509d607d1ba527731b0444d",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/candidate-brief-adapter-v001.json",
      "sha256": "e5307ea7009184fa46887b2fec0b221bddd7618ade9130c5d75652165365f62a",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/candidate-brief.json",
      "sha256": "138ff7eef5fa302ff056866b7c403ce78d610aa3f1e1fe84e4c2e38755185f6c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/candidate-initial-invalid.json",
      "sha256": "ca2b7ff081b6cf2c15aff1b01083575a60d4b0d6a26e85580e77aa6421cfdfe3",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/candidate-validation-initial-invalid.json",
      "sha256": "bccad231e86289cea844fb95c7c4bea02fa585f0070a5338fe3441a9f602afa5",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/candidate-validation.json",
      "sha256": "cf1f5d3c31aa4dbc55a2ac8d4210c1769edfae24ac2814c8cb5b14438b47e15a",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/candidate.json",
      "sha256": "326f22bb2b697b1c36fc7349ac5db49298609c1c580ba7f8eb1fb958c355a66b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/concept-evidence.json",
      "sha256": "09faa189ca7c56b7f7e07138422567e4a8190e22ed3067507a6f7a2a438bde9a",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/concept-generation.json",
      "sha256": "03662507be4e1c578f28294891d85cf582533fdb8de8579ac392c0a202099950",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/concept-original.png",
      "sha256": "7285ce56f8ede05348925a4480669500f32dc7ee9f2c7f53f1cd0f8fa19fb246",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/concept-prompt.txt",
      "sha256": "6c9914d0db89a006731268e03ce94b65cd2873657604b2aed5a220e98d24a31c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/concept-validation.json",
      "sha256": "9d4c9e689458975ffa6a752dd6a7d7d3a7ee077ef6611c45c1186708c9183bc7",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/dependency-hashes.json",
      "sha256": "f440e920943401d0f28112fdf1da0da2f15357b997200d9b208dc35d2968a543",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/eight-view-sheet.png",
      "sha256": "b9648a6bc365053e7c0107334d417c2bb263de5f97494bf52a827a0cb75377da",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/final-stage-times.jsonl",
      "sha256": "73f181aaac7e5e80cb0369c44e8ea764ffb28fcd069a243af4738cfc38162272",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/format.log",
      "sha256": "6f3fee031c8cfebd2affb0a8fb4702ea2808158a4f91b2ce971577c1384f6463",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/generator.py",
      "sha256": "7b360b689fb57840f0ddf286ca4d44a39bf2c5a8d82ea2452b8addb667040b76",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/gltf-validator.report.json",
      "sha256": "0db7f622dccf3d4e39b2d288859211c8a85596299bfcf9a302c8b3562361576d",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/maker-review.md",
      "sha256": "bea442cad24b93d65dfa5f0593f807cdb3336db4fe15f503f012aed9d57b2b87",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/metrics.json",
      "sha256": "f8fd370c46223d30cc00b030b8064291eb66ae5bf72cfe4ab3b4bfa7e2265034",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/model.glb",
      "sha256": "9388a918314ca5426c992d9f1702e881d369bc5a15ad43d5dce18afcf80c0fd0",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/modeling-freeze.json",
      "sha256": "7588c32bc50aeccdc3f405c31bda85e53a69c2fbed67b68ab31b537f6d6d45cb",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/preview.png",
      "sha256": "a000622fbe2aaa01b87a82090b0fe0154c8ab62fa0403efd30aaf4ec1fad0402",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/profile-contract.json",
      "sha256": "b1685749af5ed87551682ee3be9cda0aee28ac078559bb6cc96ce2b45080648d",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final.log",
      "sha256": "fce40599b26a94b2f1fc9617b9f7ecd351e9b5f88699e9055d855d3dd93a9142",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/clay.png",
      "sha256": "f4dd1855490896556221bf67837ed807d14a780ec652700c4e1ca9de0be9bb0f",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/front.png",
      "sha256": "9b3b98a6a282dba7cd91e31db65312583709bb8c29a53533977618750d434c2a",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/hero.png",
      "sha256": "a000622fbe2aaa01b87a82090b0fe0154c8ab62fa0403efd30aaf4ec1fad0402",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/rear.png",
      "sha256": "1097f71aa0565cc7fa60b1813fdb52d87be41a71d15f27b15edd838bf7de1aa7",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/render-config.json",
      "sha256": "34804b0387693ac1f505802a6f68826cec0a53672fa6fcc1b60dc5f3738baf00",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/render-manifest.json",
      "sha256": "61d003d17191af428f22c7960ff14968196d896f5593946755af661e7ede7d3e",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/reversehero.png",
      "sha256": "8ada89f230fae0b8ce6c31753cabcaf10be30f049638f9ab3a785125c4df3401",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/side.png",
      "sha256": "110c21f5431d8a50a8050bf127fe091397dfeda9cb1ac0bc5d5919295dd2ddba",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/silhouette.png",
      "sha256": "33c4e4d48ba83997f5479268167ec18ddc33a23822585520008c59398d3a44b1",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/top.png",
      "sha256": "928bed38e4663a3bf6b7f40207e13cfc235162b9c7a3d23d41a948cf65006cce",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof-final/turntable.json",
      "sha256": "8e2ae21cb569388077f4dc7ded2a3870d0b869c709fdd9819cbed0af21db94a0",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8.log",
      "sha256": "2ddbad2cce68ba10e1c36177bcf063d76d6fa3639eb6dae08a290e00bac1bc86",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/clay.png",
      "sha256": "31c2c2b02ffbf100530efabf1d80c357ed3a4d890c35686158d183891fd27429",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/front.png",
      "sha256": "17a205725df53c203a40c2243fde32dfc734a717487bb00904621497561209fc",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/hero.png",
      "sha256": "8331033b4fad2f79af8a2a9231bdd9a4154519ddcac6803e5550df7bf56eaff1",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/rear.png",
      "sha256": "c96c68d06479a76e08e5929b76946b0c7b6d41d833890810cca9cfd0c732b974",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/render-config.json",
      "sha256": "3d187da8e2d577207b6b35fbb755cf65af32d2027b6fccc7d5b207fff023f2e7",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/render-manifest.json",
      "sha256": "a8fea19d3edb5cbdb8d640b51124fd4a5cd9a71b244a6df0cb7effb4a09fa32e",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/reversehero.png",
      "sha256": "53aaccbb197e08f2ace0c3e62753edf8d80e717fd6467bc553e3310c92638043",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/side.png",
      "sha256": "e9e058bd811ac82a73d78ad3ab7569f7c5a246b693a30e630b2b0bf5e8f2db78",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/silhouette.png",
      "sha256": "29e234a5d7008830938e324741b094317bcc2bcfc77db45fc3702a3809b0ad49",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/top.png",
      "sha256": "5deecacf6198c9dfff4f10b9e50e52b93b9622b9443cabcd82ade60ef5f80ef8",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/proof8/turntable.json",
      "sha256": "9770ee46413ba054871f53bd6e8abe53254729f867637d9e3f134775d228fad4",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/qa.json",
      "sha256": "7bed51a8ce35799efe232c80dc47a0529f651e5dbdc711a69f8924e124353960",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/references.json",
      "sha256": "458814d5f92eb057f1071eb87439783dca48bcb5c74803364afd4a86525d1eed",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/repro-bound-1.log",
      "sha256": "b35ab484516b7f977c4df5249c8d50c776b2e292ef0e36566c2108880ccacfc4",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/repro-bound-1.report.json",
      "sha256": "b35ab484516b7f977c4df5249c8d50c776b2e292ef0e36566c2108880ccacfc4",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/repro-bound-2.log",
      "sha256": "455a0d8e21eac6403aa171e614d06e2ace4a52a78da342e291a3e71510ff4119",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/repro-bound-2.report.json",
      "sha256": "455a0d8e21eac6403aa171e614d06e2ace4a52a78da342e291a3e71510ff4119",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/runtime-parse.report.json",
      "sha256": "feceb9a773355522de419d354f73d23c19481b44257ea5c17cb1b75591a44c4e",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/source-final.report.json",
      "sha256": "7c81e266acea426854b9474ec1ea314867a7e644eaa64dd4eb9bf148d3fa3189",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/source-metrics.json",
      "sha256": "2f848863758946f44ad5c8f050f47016430836610dbda3b2260ebc9052470c4b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/source-reopen.log",
      "sha256": "ceb38d3ae4880be7ada583b588c23bcf41ede59401ee73aea1994a676d278d09",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/source.blend",
      "sha256": "b2dd206c55a5436b9af4f58115dd6684e9ed534df4d97945e5f2f18d2f5934e5",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r002/vertex-counts.report.json",
      "sha256": "d94201e3357c2f5969b93ecff9db302d7b0ae6103e84cfbd95b2a24d0c3931b6",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/HANDOFF.md",
      "sha256": "833b5854d3cddb7e8fbd3e88fc8215fb9cd8ba2c73814c3e34950b5d7a6fa37c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/brief.delivery-repair-v001.json",
      "sha256": "d09af7bafa9deff140c78d62c94019f7ec08599487fe180786aac0479d8e1743",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/brief.json",
      "sha256": "565e599fe3326edcfe53774d1da297c7c44623cbc83db884c068bb0154aa91e4",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/build-config.json",
      "sha256": "22820022eaa3157e8aa4cb8f2eb1d71d0311f9bafbbe42018f9ceece6834e517",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/build.log",
      "sha256": "34893189cc021a076e15ddadc609fe5445526016229c4afd0c2b3e917e4d61d4",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/candidate-validation.json",
      "sha256": "3e6f62a014a3c966b1ff427da853deba701bac4122bb1cc819875397ed6367dd",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/candidate.json",
      "sha256": "3cdd60e83969011b064852e05e8ba81053716f77ffcf9f0fb372f58bbcf7afe6",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/check-execution-times.jsonl",
      "sha256": "2f888b611a786fd5f3ea4675e76e34ea395bbd95fd32e52dd59f3dd63dd87f17",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/concept-generation.json",
      "sha256": "03662507be4e1c578f28294891d85cf582533fdb8de8579ac392c0a202099950",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/concept-original.png",
      "sha256": "7285ce56f8ede05348925a4480669500f32dc7ee9f2c7f53f1cd0f8fa19fb246",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/concept-prompt.txt",
      "sha256": "6c9914d0db89a006731268e03ce94b65cd2873657604b2aed5a220e98d24a31c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/count_vertices.py",
      "sha256": "ffa236a6af1d51329ca1c23e04da9a7c1ea4494d63661046ce015aa7c945c0f1",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/delivery-checksums.sha256",
      "sha256": "cc7c280e11fe573baee87d5f4c2e8bb6bc8e25d575ec29fd566e5c9385aa6c90",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/dependency-hashes.json",
      "sha256": "f440e920943401d0f28112fdf1da0da2f15357b997200d9b208dc35d2968a543",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/eight-view-sheet.png",
      "sha256": "62a75acd985bb0e200f93af9c2239dd815c5642504b76487d3c08cd8288f282b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/generator.py",
      "sha256": "0e3f118740e74de404c5c0b854402ede5e0e10d66937da07761bf8ef24da472b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/gltf-validator.report.json",
      "sha256": "ffb8a3ea3f4b4df990fe94a5dcac40a8f44f39bc8e4c345eab0ff6924c900870",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/khronos.log",
      "sha256": "ca25223860772c22e51eee1dfd02b9658bed2c0b011576f757b5cc4e5b9c0a32",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/metrics.json",
      "sha256": "d0b686086b4d2cdb1ae6e37178b757b238ad4e84f0b2cc1bcb8e0b1ee7fcb5f6",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/model.glb",
      "sha256": "d326b3d5f2c3e14256d56afaf444db61b7f14963dc9cb0105aece89c5545cedf",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/modeling-freeze.json",
      "sha256": "59ae2de3a6052d14d0ab4c20ecd9c7646add2c206fa0e095b8b27d5662462af3",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/original-byte-integrity.json",
      "sha256": "29ff203e78bc5ef1533bbd39377f944280f0f8fe5a33a86f3475b97db8506770",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/preview.png",
      "sha256": "6a44a8bfcf167479e8ca903b001b0098bc22823b2b07a0987eae2af27fed447d",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/prior-revision-concept-evidence.json",
      "sha256": "09faa189ca7c56b7f7e07138422567e4a8190e22ed3067507a6f7a2a438bde9a",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/profile-contract.json",
      "sha256": "e3621d9c4ea490a0975e94e66a79f34a5d610ce17014af67c0e29308825a6ea4",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/clay.png",
      "sha256": "63fff18fff6a21b0480837f811c0d9ef94b0a2a676f94708f784e2882aa740c1",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/front.png",
      "sha256": "7bf934139a909f6e0846673e2b6cd8504660bd1c16ec5bbcdabac6ccf1ffd67a",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/hero.png",
      "sha256": "6a44a8bfcf167479e8ca903b001b0098bc22823b2b07a0987eae2af27fed447d",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/rear.png",
      "sha256": "a0638d0045beffcd729adab833d0fbaa4bf2c4fd58d636412bf6716f0623c689",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/render-config.json",
      "sha256": "34804b0387693ac1f505802a6f68826cec0a53672fa6fcc1b60dc5f3738baf00",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/render-manifest.json",
      "sha256": "c4169c245e0b3c95ae8587f48aa8a352da8d06d4e05ccea982943e882e9e5755",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/reversehero.png",
      "sha256": "5d1a0e153e96a7e689f64966335066f863b6033c5e6bd56a7eb6e24df3742e76",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/side.png",
      "sha256": "4f9a79b3a1c1ac7333f9458aff39ac14cf803a14603959442e8d03e94500ded2",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/silhouette.png",
      "sha256": "d7d0a0ddafbfc692eff25e0e5ce83e32e798d5c0a51e7a233acff41e6ed2b615",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/top.png",
      "sha256": "e890e35f408a13beacc9b0517183137210835ec36ed8f88df8f3c0ee2ffb2ab3",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-final/turntable.json",
      "sha256": "981fba7b826445d9600ed9664a9da1212f956667cd830573faf240f89a76fa00",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-interrupted/front.png",
      "sha256": "125a25b043a97ea47bc36a363596898d2c842cb4fe474bcbd99228a1ce11db0d",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-interrupted/hero.png",
      "sha256": "7677046f4849ca12dd613574d55048e4c832605ee994e504074d0916ff7949c5",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-interrupted/rear.png",
      "sha256": "bcf988b99616b9c592d20dd0e1afbd6c88ea8805a8865f2eafaf675140e37fa2",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-interrupted/render-config.json",
      "sha256": "34804b0387693ac1f505802a6f68826cec0a53672fa6fcc1b60dc5f3738baf00",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-interrupted/reversehero.png",
      "sha256": "1679b98b720ac2c0ce0f572064451716173874cac72f914a6feecde21f4c2fff",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/proof-interrupted/side.png",
      "sha256": "07aeb09438f8cda23fba27b5ea6a9d0974345b87dd08879a139332d9af322b02",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/qa.json",
      "sha256": "a8e7eb33aaa066b040dfe5e6246b73b997c181bf31699665923f5de22c2ab233",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuild-queue.json",
      "sha256": "def4bc58ccd6f1641f1ab5d6d201e30ea2a4620a48cfecbf73f6ed0392e55823",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuild-queue.log",
      "sha256": "3a4641709917d7d6ee5ab98a0137a291437a19ff4b1285037fa77b5312d89b62",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-1/c54b90d930153d4f73d61d94a198bdf5b8cfc7a104aa99f9615f576f48d09f90/20261020T023212-e88fade345714660a586ee7987f59b71/outputs/metrics.json",
      "sha256": "df4a8990cd24f1a1fddc1a4c7930a7d77b6d80484f3c6da9e0cacd172df4cb1c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-1/c54b90d930153d4f73d61d94a198bdf5b8cfc7a104aa99f9615f576f48d09f90/20261020T023212-e88fade345714660a586ee7987f59b71/outputs/model.glb",
      "sha256": "d326b3d5f2c3e14256d56afaf444db61b7f14963dc9cb0105aece89c5545cedf",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-1/c54b90d930153d4f73d61d94a198bdf5b8cfc7a104aa99f9615f576f48d09f90/20261020T023212-e88fade345714660a586ee7987f59b71/outputs/source-metrics.json",
      "sha256": "45e2fb8991a17bd6075b5ccfbf76234239b480366a10a36cdba2cd12e7e4b218",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-1/c54b90d930153d4f73d61d94a198bdf5b8cfc7a104aa99f9615f576f48d09f90/20261020T023212-e88fade345714660a586ee7987f59b71/outputs/source.blend",
      "sha256": "cf3d062ca001141f144c8b30afb214132556258ce57f3a349779f3e2867220da",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-1/c54b90d930153d4f73d61d94a198bdf5b8cfc7a104aa99f9615f576f48d09f90/20261020T023212-e88fade345714660a586ee7987f59b71/request.json",
      "sha256": "66b3be71ac8705b30dd87d2532e2fab0b21686d5c37a6c846a48fa0e4db67560",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-1/c54b90d930153d4f73d61d94a198bdf5b8cfc7a104aa99f9615f576f48d09f90/20261020T023212-e88fade345714660a586ee7987f59b71/result.json",
      "sha256": "86cef1f99c83200e07808c52d01a309a0408f852647024557433b52ba4648e94",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-1/c54b90d930153d4f73d61d94a198bdf5b8cfc7a104aa99f9615f576f48d09f90/20261020T023212-e88fade345714660a586ee7987f59b71/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-1/c54b90d930153d4f73d61d94a198bdf5b8cfc7a104aa99f9615f576f48d09f90/20261020T023212-e88fade345714660a586ee7987f59b71/stdout.log",
      "sha256": "d8a35f51ee980bc2c0a8a2509f67e52186195c2edbf935975f2a202e55ed5a7a",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-2/7c2c7542b0f2bf3fe57ec169c53585b6f469429533539236d505ccb15ff11e80/20261020T023215-35d8737945d140f5a93c0dd6d97f28f8/outputs/metrics.json",
      "sha256": "1db3fe72ec5e82f89bca1579e359fc6f60704e6257cf6259c76d2a7e045d504b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-2/7c2c7542b0f2bf3fe57ec169c53585b6f469429533539236d505ccb15ff11e80/20261020T023215-35d8737945d140f5a93c0dd6d97f28f8/outputs/model.glb",
      "sha256": "d326b3d5f2c3e14256d56afaf444db61b7f14963dc9cb0105aece89c5545cedf",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-2/7c2c7542b0f2bf3fe57ec169c53585b6f469429533539236d505ccb15ff11e80/20261020T023215-35d8737945d140f5a93c0dd6d97f28f8/outputs/source-metrics.json",
      "sha256": "45e2fb8991a17bd6075b5ccfbf76234239b480366a10a36cdba2cd12e7e4b218",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-2/7c2c7542b0f2bf3fe57ec169c53585b6f469429533539236d505ccb15ff11e80/20261020T023215-35d8737945d140f5a93c0dd6d97f28f8/outputs/source.blend",
      "sha256": "ec40143ebaeafaec049422915723fff059872dee93a200c2386ac11308187521",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-2/7c2c7542b0f2bf3fe57ec169c53585b6f469429533539236d505ccb15ff11e80/20261020T023215-35d8737945d140f5a93c0dd6d97f28f8/request.json",
      "sha256": "6571e482b769036c5c3205bc5447eff07f502d71b994e46c45bfe704b8019715",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-2/7c2c7542b0f2bf3fe57ec169c53585b6f469429533539236d505ccb15ff11e80/20261020T023215-35d8737945d140f5a93c0dd6d97f28f8/result.json",
      "sha256": "ef7e21c9bbd1803b96b70bbbcb9118f0948075ac01ced36ef4e36b87eba75b0e",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-2/7c2c7542b0f2bf3fe57ec169c53585b6f469429533539236d505ccb15ff11e80/20261020T023215-35d8737945d140f5a93c0dd6d97f28f8/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/build/cycadeoidea/r003/repair-rebuild-2/7c2c7542b0f2bf3fe57ec169c53585b6f469429533539236d505ccb15ff11e80/20261020T023215-35d8737945d140f5a93c0dd6d97f28f8/stdout.log",
      "sha256": "abae1a7961b6a2f0561b3766121c320ea39d6f90621f794a45b6c6f095ae16e8",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/runs/20261020T023212-c9675dd4705c4bc9b8352d5487823f34/manifest.json",
      "sha256": "8d924fa66b07fb548c3e0ec2bd328748afd702a70244fd3eece90634e5d97ca1",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/rebuilds/runs/20261020T023212-c9675dd4705c4bc9b8352d5487823f34/summary.json",
      "sha256": "114764a3f726bc5ba98725aa084976b613b08e63a0ba58b4906663615b189144",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/references.json",
      "sha256": "458814d5f92eb057f1071eb87439783dca48bcb5c74803364afd4a86525d1eed",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/render-complete.log",
      "sha256": "1de7b3866f76af48b7e9c1fee5827fd9c40a0f71de590a73123331fea7e5fcbb",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/render-fixed8.log",
      "sha256": "b6aa26221d02a7f632565d155ed7c3b79768fc0f21898a0dff99d0c4989378f6",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/render.log",
      "sha256": "74cd08148cf6f9e07b37fde6af1993e403c781333ce184768850c1d32225c372",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/render_exact_glb.py",
      "sha256": "33ed7fc4b39a41e67f79e51d41fd4457f2a3087085837e59c8981d87e7bb412d",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/repair-handoff.json",
      "sha256": "248fe23b7134956a12f40f32289b37032c9aa84649210b9b85d3c994c251699f",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/repro-1.log",
      "sha256": "1bc09c7f7a8fe451e6155223017543d6d4b4c2f4641a60df2b9237e37e055821",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/repro-2.log",
      "sha256": "c34f65ef0faaf7ca654e7002da24bf702169e53bd1537b435bd979c8b5428ea9",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/repro-bound-1.report.json",
      "sha256": "1bc09c7f7a8fe451e6155223017543d6d4b4c2f4641a60df2b9237e37e055821",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/repro-bound-2.report.json",
      "sha256": "c34f65ef0faaf7ca654e7002da24bf702169e53bd1537b435bd979c8b5428ea9",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/runtime-parse.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/runtime-parse.mjs",
      "sha256": "9fa56f59dddeff5bf8fe86de0d0ff6627421d263fc59011a2424a03ed229418d",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/runtime-parse.report.json",
      "sha256": "a9021b67c3be20d6f849c17b8ed9059a72c61b1618fc81dd94a96b3b911732a9",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/source-export.report.json",
      "sha256": "5975c78a01387247ba00050c789078f6ab83544b52c52a66acb63066b7a6c396",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/source-metrics.json",
      "sha256": "45e2fb8991a17bd6075b5ccfbf76234239b480366a10a36cdba2cd12e7e4b218",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/source-reopen.log",
      "sha256": "6a981f58251a4bb012a707dfdd39e1248cf32b7414d56c7cea2aff187fba62d6",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/source.blend",
      "sha256": "b0ce63feec724a9b66236bce3429bae08c86ddc1a1c07e55b4d5d233a6a00a63",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/static-glb.report.json",
      "sha256": "9b5e057c938c65fd85999d94ba0cddaca918e02c45f1561d61791a6113fcc436",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/static.log",
      "sha256": "9b5e057c938c65fd85999d94ba0cddaca918e02c45f1561d61791a6113fcc436",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/vertex-counts.log",
      "sha256": "21f1158ec954a432986e1363301b534814180939d84da6a589bb331f3b0bd06a",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/vertex-counts.report.json",
      "sha256": "baf8a187dbe3fc30c48788897ebe1fdb606ec8e3033f85846a1bcf228e3c63ca",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/brief.json",
      "sha256": "b5dca761406ec90f845ab283f9efc55b305acf66a316052439ad54c655da26ac",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/build-config.json",
      "sha256": "2db6a232e08dea1b1b94ad4972b85cb5a2b9c6b4616e18b361b1d9ad01dda414",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/build.log",
      "sha256": "211001d1bf382406e84291fe551e5145aa72e374a7da194be8e5b4ca48daf62a",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/candidate-brief-adapter-v001.json",
      "sha256": "0bf413627f44d04721aba028ddb0781dea25a9a4252e0ebb9be69916c7d3dd02",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/candidate-brief.json",
      "sha256": "d42d8b4ba9ea1cc8d060250da80bf65f66663f909912cbadc76d4919e72ff0b8",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/candidate-validation.json",
      "sha256": "9327f515594c25798d1b05beb4eff667ba1b36c904c8e3ee3eaf1e74ed4a447a",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/candidate.json",
      "sha256": "701168809517d06280bbc7b5b6c12a24d801a32bb2679c00e0d96e32d5ff879c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/concept-evidence.json",
      "sha256": "9882e949b6958def25a7ec2cbabd8c216d73a509d7bcbb1e007156001411bb3d",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/concept-generation.json",
      "sha256": "03662507be4e1c578f28294891d85cf582533fdb8de8579ac392c0a202099950",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/concept-original.png",
      "sha256": "7285ce56f8ede05348925a4480669500f32dc7ee9f2c7f53f1cd0f8fa19fb246",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/concept-prompt.txt",
      "sha256": "6c9914d0db89a006731268e03ce94b65cd2873657604b2aed5a220e98d24a31c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/concept-validation.json",
      "sha256": "114b1f847a9094064463d0c0d350767c4ceb77c32d008f9f21e287994d389d58",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/dependency-hashes.json",
      "sha256": "f440e920943401d0f28112fdf1da0da2f15357b997200d9b208dc35d2968a543",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/eight-view-sheet.png",
      "sha256": "694009e8f86be458ca4d90761c3df0dd1b3fd4cdab56da38b0bb9f3503447783",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/final-stage-times.jsonl",
      "sha256": "ed423f0dec6a54b422c4dc9c59065e98992a5737b4dfc8b456d424c6ef09d109",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/format.log",
      "sha256": "9d4cb25d349c64cab63d4b1391f18f212afc3c9e776821bb20dea883a255c8b6",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/generator.py",
      "sha256": "d496960e7ba16268b8b7e0575d96032726dc3630c53bb0b469af54d20f6ba3e8",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/gltf-validator.report.json",
      "sha256": "9752471839950eed685489c665c5d038938c215c89ee5c0287be5d9d486b0355",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/lifecycle.jsonl",
      "sha256": "bdf6778175265155f626bd7b70520ffdec0b2ddd423843da4296fe613181d9fb",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/maker-review.md",
      "sha256": "6acecf4418ca7e6660b64c4b4b3456e518d68026e6ee4c50e8de5e6250e26834",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/metrics.json",
      "sha256": "9155120f576fd19b6b27590c424a06a84026c52f7a614721a6199abc8fa4cf8d",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/model-start.json",
      "sha256": "86bb60d2ba786049f15061b65b14d0fb5852c5f486ee908775f0c0d254f18746",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/model.glb",
      "sha256": "c679676d46d8e51789a690db2f1590baa89c766cd50eb29700347150b43fd7be",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/modeling-freeze.json",
      "sha256": "ce14936256b618bdce37e55ebfd184ff2053dcbc7662b0785d19f7538a1b76ce",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/preview.png",
      "sha256": "c2d784de2650acb966a12365d073d45c322c90792f8f2d7362dbe22902334506",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/profile-contract.json",
      "sha256": "a4c544829fc5060529c0cbf8be6fa93bd10cfd17d58601e7075ca78c40af577a",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final.log",
      "sha256": "99417e91c5e3491ec8252aa2cd0912998b461242080f72a18c2bc28e656b0449",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/clay.png",
      "sha256": "dd1d17b6a7bb147c6f002f635d5e20c695dcd2c81e56844ceb67fabcd838f3e6",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/front.png",
      "sha256": "133e8acc9db16bea0a5a000afa3c499314f01d82a1d051c304c7a1a2dbb5d36b",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/hero.png",
      "sha256": "c2d784de2650acb966a12365d073d45c322c90792f8f2d7362dbe22902334506",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/rear.png",
      "sha256": "f93a3b1703fe08cc49c507b944d261c478c954f5af374b8d8def6fdc4bc8efd8",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/render-config.json",
      "sha256": "957e9b553ed1ba478eb6ba080fac77e1d75f69d93b934cbde8f01582b6513a9a",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/render-manifest.json",
      "sha256": "ca6ad46122b610219f4a8b91572e013120c61296f39ec88411b417263bea3ddb",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/reversehero.png",
      "sha256": "849101190ecf013c9927d46bd4aa66e6d430f9b48b18715bba06c4f8c4222f4e",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/side.png",
      "sha256": "1d4c26d505dc16c77b23a9f04fc0921eeed022814dddf4c478ec8ee1ecbb409f",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/silhouette.png",
      "sha256": "07ad61fb416772fe6a0f8fa772005713b96a75c8092b132749b5be4911e9e8e4",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/top.png",
      "sha256": "06c9c188a2cd89d2bf4cb5b07cb1de048c4b6b3b42da489f62589b8de3c42036",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof-final/turntable.json",
      "sha256": "060e61effd7ce06e6f24537efa050289f3d1c98576caf37940d985821563625c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof.log",
      "sha256": "74da15ea65270e935213264eb19e00d8ae18fe007b92a714a54b051dc39921f8",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/clay.png",
      "sha256": "0037dc17dbb80d0d45e4d19707a65cff037fe4150c1fbad9f7711f0e7ce4527b",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/front.png",
      "sha256": "cda8eb1038bf9c784ac5d6e229b23f7ea4d3c0dcef7426cc7b3b5fcd7b3e3a33",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/hero.png",
      "sha256": "968872d57ad7ec96648500ef42f9a01702c8010d3065db5e2b4f81bb6d06de56",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/rear.png",
      "sha256": "0a0a358b977c8fa543320fc02ebdfc3a086d52492abbbb0985f9a84a4c01299e",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/render-config.json",
      "sha256": "8141741a0d86ec74886bad28d622abf3a3806a8de61854e652088a8970911937",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/render-manifest.json",
      "sha256": "3e42613a2aabe4306b0cf9273077a5c8f9bf91105e3f7df0002985bf357865c0",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/reversehero.png",
      "sha256": "b8c95748feb99be5752152cde70fd4086d84ca01c0d063edc8479d48ebe838a7",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/side.png",
      "sha256": "40e3587adb2d2eba58aa4c24ee324860ce4ca2c8d4b47123aaba8fffc548f31a",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/top.png",
      "sha256": "aa6f4049ad0fb77345c4abc66f03126ac2f486956210bce55161c8756d5410d8",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof/turntable.json",
      "sha256": "ca79dcf52ae85f471cc2531cafbb7a78898845312bde98068066649949c31d4d",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8.log",
      "sha256": "202ccd237b4bdf772fc9350fad525dd1c10b79390a9739768ccf323c8e49a3c7",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/clay.png",
      "sha256": "d12f531bf5dae3859fb96cec80c5196e20b97f06d912b434da3c27957a61bc6f",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/front.png",
      "sha256": "6ef96db890cfaadec3230ec992afe693cabf668fb527ee9763a7eb67855b83da",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/hero.png",
      "sha256": "582fe58336ed7a14cf72e67e6d9f3b900bd02bb91d7cb9496e30bd4b2112c287",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/rear.png",
      "sha256": "0bd1603e2602cc747f592c8f3444b0559c855947744b99690dce037ee2004677",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/render-config.json",
      "sha256": "22c498f7e9405b78b1b2ad528fc07818ffaf32f9e1f448201dcd81528369103e",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/render-manifest.json",
      "sha256": "b66fdd291e106dcb6b83f1e1cf9136e28d58b43cb788e08a00ed829736b3141b",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/reversehero.png",
      "sha256": "61a5456e33b0ad94f1e407b746a1eb071a6ffca6cbbab786864fec5d43634ab6",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/side.png",
      "sha256": "82a711fc7eabc8657d8a31a305e7420e875e0e7ed90e2c92a7b4f73e53a405db",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/silhouette.png",
      "sha256": "fc8e2c9213c29ce46f7d1296bd07131a828ed9b744e184ffcd91ba669d769679",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/top.png",
      "sha256": "3bcad3f8de573539f31b6bc87e5fd9a8ace0508e717c5911c16d2b6d7e0567b6",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/proof8/turntable.json",
      "sha256": "21912c7852a13293ca0abe4ad4a9a1c2f7944be6911603e059a6a49c756c0e0d",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/qa.json",
      "sha256": "97db8b09b8578eeb7ff5c139370661598c7205fcc77fd1aeff79be6daa5b37d7",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/rebuild-1.log",
      "sha256": "ccf4ff41abd6bc81de5230fd6ad7d21506a4218cefd268adb91a67b66e25e02d",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/rebuild-2.log",
      "sha256": "de4b62fc9afb800106b1ca6ca3ffcc5b79fb91ddeb04b440b273f98a5fe2d317",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/references.json",
      "sha256": "cee7ee3f841c1c1add35fabaa2f542dd4d187645999539b422d9ce0476515fde",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/repro-1.log",
      "sha256": "d15f28676669afdf91a51a54672dacf74a76b1e41a377dfd8ad517a50b8f1020",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/repro-1.report.json",
      "sha256": "d15f28676669afdf91a51a54672dacf74a76b1e41a377dfd8ad517a50b8f1020",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/repro-2.log",
      "sha256": "942f5305d32658b560a70fb3ae517c541bf2822a2fd2f88c5781f77c106ced1c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/repro-2.report.json",
      "sha256": "942f5305d32658b560a70fb3ae517c541bf2822a2fd2f88c5781f77c106ced1c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/repro-bound-1.log",
      "sha256": "54f7e0b53cb0b48f7bbd19a7bb9ccc429eef87b7b3361bfd27cd82548b08e262",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/repro-bound-1.report.json",
      "sha256": "54f7e0b53cb0b48f7bbd19a7bb9ccc429eef87b7b3361bfd27cd82548b08e262",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/repro-bound-2.log",
      "sha256": "8436741a43272cd0dc91707e68b8a15d114d45f74d35ce7ffc68a47fb8d40c44",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/repro-bound-2.report.json",
      "sha256": "8436741a43272cd0dc91707e68b8a15d114d45f74d35ce7ffc68a47fb8d40c44",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/runtime-parse.report.json",
      "sha256": "c67075fb5440c2a3ae53416808c537824cc2caf190ebe4fcdd6fce8b8bc52b7a",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/source-export.report.json",
      "sha256": "819aa6296a18e76ac7f6aa5d58a8efb205ec58d6e0412b29bb10137c5fba8de5",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/source-final.report.json",
      "sha256": "29588cf40597a95b228d42f12e9691aaf02714c145a464b7b4d649de9ac641f9",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/source-metrics.json",
      "sha256": "07b7e359b8db02a593df72c20d84af75ebd2a15a3682ce2ae7ed167fcdc5825c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/source-reopen.log",
      "sha256": "52c9cb70f10ed1e922059f937ed3d8d1019818d67026218c1f170010c421bd08",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/source.blend",
      "sha256": "4cc24271c53a23cc3d65c92a04c0bf0be70726022208d78ef8d51673d4cf1534",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/deflation-hollow/r001/vertex-counts.report.json",
      "sha256": "94950084041f3f5999268fa564ff9eb19dcbe9ba5eac0822dcbdb954c7e187a8",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/brief.json",
      "sha256": "fd7bdad15d08179c3b9ef0993138afd5a4256f127c6f95320cf4865e21d18d86",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/build-config.json",
      "sha256": "f18ab0c7098ba24108a339a1f0bb0e5c7e732cafd0c263e192122f61ffca509c",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/build.log",
      "sha256": "4a36246d5541ba7886d9dfb0fc94f81607a6489cfbb93809fe99696c502b9e9a",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/concept-generation.json",
      "sha256": "03662507be4e1c578f28294891d85cf582533fdb8de8579ac392c0a202099950",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/concept-original.png",
      "sha256": "7285ce56f8ede05348925a4480669500f32dc7ee9f2c7f53f1cd0f8fa19fb246",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/concept-prompt.txt",
      "sha256": "6c9914d0db89a006731268e03ce94b65cd2873657604b2aed5a220e98d24a31c",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/dependency-hashes.json",
      "sha256": "f440e920943401d0f28112fdf1da0da2f15357b997200d9b208dc35d2968a543",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/format.log",
      "sha256": "ee371448fda7d03a80d14cea98d6ead249a2540d10088b57e527544393387a16",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/generator.py",
      "sha256": "d496960e7ba16268b8b7e0575d96032726dc3630c53bb0b469af54d20f6ba3e8",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/gltf-validator.report.json",
      "sha256": "dc0761b5ffbbd01e9b0417ee9cfd6d66f3f5c8b6b34428d1cc6166981523224c",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/lifecycle.jsonl",
      "sha256": "870f93bb2212847429d4323db2084e8f8c6d1cf50b4e7126a858110859fc6b93",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/metrics.json",
      "sha256": "d73aecf4338085eef361a2aace1ed3d9a2db4e31a657ec7e4dc9ae292e22e2fb",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/model-start.json",
      "sha256": "6ede8988275ae3ee4f405edce06c3f3548b312fb60470ba3695eba2ac675cb8e",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/model.glb",
      "sha256": "75796a71ff532addfe21c632c7421f9ddfdb479ceec960a03af5abb216310386",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/modeling-freeze.json",
      "sha256": "9241b2abc3c6f43e985e742ff736bab0f8c488d0788d06cfacc8a4959e6d2652",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof.log",
      "sha256": "cd84eb2f330d39243deeda392974eb47543d54b7e324270bd8a5411943b30a2d",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/clay.png",
      "sha256": "1f2ac720576a1c8ad6e95e205ff15586753016fa8e845903e394e97b4cced4c2",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/front.png",
      "sha256": "592402a8eb5f7b110d53fa6d85dd52d29268b7dfdc1d3b4ef4e400135277ff0c",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/hero.png",
      "sha256": "5560449ad66ae08f196bf214e654be6e8ae6bd71ac7a960fc54d37075ecc14bb",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/rear.png",
      "sha256": "aaa2d8e02542a290eb485c2324af2b84915d2023bbecfd9d7009a6837a4b9210",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/render-config.json",
      "sha256": "b1a24f2a14545fa54a0c6981e44544c617359daf2ad15b121772209b50fb9334",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/render-manifest.json",
      "sha256": "dea80a0b03d5541767c0a39a23e530cb19706a4449f72a89fef1bf1c70943a21",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/reversehero.png",
      "sha256": "787deca9aaf2241843f84f057faad5ebfa6b1f68a5cde2dc49dff2c66c6c38af",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/side.png",
      "sha256": "2c0d79b8cc8fea4070ffc7c81d5129c6a4f2d1574900d41e3096fbbe2b6216a1",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/top.png",
      "sha256": "ca246fa0ee685b544c0796e846d8b1527a157d49f1abe01a84865eda52e60ffd",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/proof/turntable.json",
      "sha256": "6096fcefb5dab80ab0628fe44a17856a9f569fb2fbc690d07fc4708931b9a55b",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/qa.json",
      "sha256": "5f2f38fb96153977d5c6a4f329560744ab292213af8f576c5f74e20120cb938f",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/rebuild-1.log",
      "sha256": "35d83bc9638bca986c9ea55dfd09a9c9f8c68b9bc754dee8106fbfbe3bcfc1bf",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/rebuild-2.log",
      "sha256": "c6846c0d48048e78b0af5c5b00db12321fda0f28c6b97aa68bfc6e7be619d058",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/references.json",
      "sha256": "854287f79299430b8505ef42d98ceb24e6d76244d2ece161a852aedefb23eac6",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/repro-1.log",
      "sha256": "7216037b2ad57c3c2b6851a72d04796f8fcb7c2fcc2032a4255518ba6e12ddfb",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/repro-1.report.json",
      "sha256": "7216037b2ad57c3c2b6851a72d04796f8fcb7c2fcc2032a4255518ba6e12ddfb",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/repro-2.log",
      "sha256": "de815719230e76aa9781d7f8fdbdda4868b8432282efae15a439438624bced65",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/repro-2.report.json",
      "sha256": "de815719230e76aa9781d7f8fdbdda4868b8432282efae15a439438624bced65",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/runtime-parse.report.json",
      "sha256": "631308dc5c46463cf1e76524773849f28640f17d09828b74e114dc5c4affb74d",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/source-export.report.json",
      "sha256": "b297c60d8735fcea05dfbc5af05effffab7fa11fb557463f421fad639ebad438",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/source-metrics.json",
      "sha256": "6905b4246ec06d0b67fe5aca7154214f6d0e64e0ef1f1ef37975c1297795ef18",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/source-reopen.log",
      "sha256": "6e662bcefa5193989d4dddaa9a63bb5efca2d8954450a1cc18702c2d4ff41eff",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r001/source.blend",
      "sha256": "9296d2e3c800fcf34b6d08525689c3a65259c09010bd617aeddd51484678f47f",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/brief.json",
      "sha256": "ca5dcb8fe58a9034b4a7c5ace7d4a04202d05e390b15d71f10f318c58dc88fc3",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/build-config.json",
      "sha256": "4664847bda6302c022be0d16808ede52183072d4c69319aa21592e2ca0793fca",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/candidate-brief-adapter-v001.json",
      "sha256": "c18a9cb6adee247779c3be6fc41d6474d8b5065ab1cf106c9d3cfaf8003468a6",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/candidate-brief.json",
      "sha256": "de0534178a26ffdb04ecf430c357c8f3a24fc0101df6c7e8e0654f684beb600b",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/candidate-validation.json",
      "sha256": "079703de52e404f684c6f8fff4fa7336773606d054da02e7bbd0af3dcf981e79",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/candidate.json",
      "sha256": "4972be24873fcd14501c7e39b02cbe1b6e7b9922dcba10cd3bdf7f527f893341",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/concept-evidence.json",
      "sha256": "0362024872cf52cd24a7ebe23fed601ae612175ef45a259a5ed05e88e9fe2cb6",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/concept-generation.json",
      "sha256": "03662507be4e1c578f28294891d85cf582533fdb8de8579ac392c0a202099950",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/concept-original.png",
      "sha256": "7285ce56f8ede05348925a4480669500f32dc7ee9f2c7f53f1cd0f8fa19fb246",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/concept-prompt.txt",
      "sha256": "6c9914d0db89a006731268e03ce94b65cd2873657604b2aed5a220e98d24a31c",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/concept-validation.json",
      "sha256": "70035f379928729910859daf9bba52c198129a535dfc09efb8861561b4f6ddae",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/dependency-hashes.json",
      "sha256": "f440e920943401d0f28112fdf1da0da2f15357b997200d9b208dc35d2968a543",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/eight-view-sheet.png",
      "sha256": "51580bedd335ef047c0c929d42938f952f8961fedc6a299d7e93521bab933c38",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/final-stage-times.jsonl",
      "sha256": "d6d1a238dcf4e9de0558cb05056428dda44811542a6c46e503ed5feae94a8c23",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/format.log",
      "sha256": "232525d27e4d2ebf7bfa43a56c81e8ca478d667933bd3019de9f0552f944f31c",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/generator.py",
      "sha256": "7b360b689fb57840f0ddf286ca4d44a39bf2c5a8d82ea2452b8addb667040b76",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/gltf-validator.report.json",
      "sha256": "312760a82bc289cbbd438ca27a941880766fc49ed8a2e8f1d4dcafa7c0bc1b50",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/maker-review.md",
      "sha256": "bcd500da9bd1ece4cc531520c0b2be5048b24a5bc5f45de847d792ead451dfe1",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/metrics.json",
      "sha256": "a9814f8f19ce2c5b5662e9ed63ca8a1e3544dd7eb895c54f30cec116d19f02c0",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/model.glb",
      "sha256": "8133ad81f4f3d18b4d0ebd5d29ca2fe540039254b6efc8522fe20d2ec4b4036a",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/modeling-freeze.json",
      "sha256": "7aa348132f0ca2e75f63482192b043b9ad79a22b7cca090d9bfb8659a99f3a39",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/preview.png",
      "sha256": "dfd449fc05a23cb9303b17b77a9e6f13ca35e1d7fb3321a8ed033d0aa641128f",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/profile-contract.json",
      "sha256": "82f87b7fd3c0f291b3adc36b2cad4e7b11ecdb6d0ac3648ca4fd550a0d8e835a",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final.log",
      "sha256": "a78720320dc3359295c5d437e673306d79af3588d52dbf1a14e62177e34b7eb9",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/clay.png",
      "sha256": "9ba0036cb25b092032cb99fd8a57514cea7092b01fb576ff5d85ea13bb1ea5d8",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/front.png",
      "sha256": "1523bed0bdbfc9dd0a6774c642ce6f41352b3eb95052ffd1e828e87ca66ed6da",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/hero.png",
      "sha256": "dfd449fc05a23cb9303b17b77a9e6f13ca35e1d7fb3321a8ed033d0aa641128f",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/rear.png",
      "sha256": "8ab89428d13dbe8e64eac53e7b0060c7495dd83341dd37b85392798aca50350d",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/render-config.json",
      "sha256": "8d9e8608cce03b8f6ac01b1a9d7457808c80bfa21c25fdf23c499424a0edf395",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/render-manifest.json",
      "sha256": "5368ccec266d2fc43942eae6062622bda1642a86037e0a0b38d20cb271a08f84",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/reversehero.png",
      "sha256": "c582a6153434b520058962fb573debf4e39eebace8a33acf17631bf5ab2a6951",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/side.png",
      "sha256": "c58f66914103b08fd42f14106f874f287721c810a904b16abc65087684df1df7",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/silhouette.png",
      "sha256": "40e1050e34ac5bc2ceca8e3428a70fcc9a62a8150a235f3e070485d9e8cfa6b6",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/top.png",
      "sha256": "7280cda586c521128b98161151bdc54e78fb84c502da38180100ab2bae956194",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof-final/turntable.json",
      "sha256": "9b01b22cbf3c6243ac515b2b0c811d27b6ed250a2f4ee12087592a37cd28f3f7",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8.log",
      "sha256": "1d6ea6300ccb7ae7b2e037f2da0d7a6d7e7fdd852c99f38af5c9adb3b884786f",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/clay.png",
      "sha256": "0ed7bff8769a5ac709cd3575461da6279a2d4d56f966fe40c1b4994bf810ea8e",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/front.png",
      "sha256": "2766010600aeb75be23ec47e7f29e2129be3d319c21d3e6cccf166eb82b1687b",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/hero.png",
      "sha256": "8d0b58990437ad373a5adbb0128fa9150579e567fbbd012e3385027930b917d4",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/rear.png",
      "sha256": "54430e12c76c157ca4a07138eccfa7088d82eaab542f8b958f0754303de3ca59",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/render-config.json",
      "sha256": "571bb34f134422222d072428eb974b6ada94766322132db76a46965cde397bf9",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/render-manifest.json",
      "sha256": "80db88157dd3d4e1fdbf1ab89270c86f231b5ac5da9f4c5816addb9318beda0e",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/reversehero.png",
      "sha256": "a5050828645c0a4f29a47dbfa5e419c2efb56d06c66ea2629a2a4a102fd5d1e9",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/side.png",
      "sha256": "c2af7de84ef29a7b90dcc06727fee65b641969ade3ec416df3e1b3ce248a138f",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/silhouette.png",
      "sha256": "b3f5f7da161f39d19cc194ae1ed9afe330882ac5a9bbf2635d908dd78346fb56",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/top.png",
      "sha256": "e144001911be038df64ecd813ccf7134cdbcac29d1af36e09b10348e061e5fd8",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/proof8/turntable.json",
      "sha256": "7f54917c6b6f3153367f4c5d627976e8bec5bfa8dfdb651fc86a0b2ae88ff32c",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/qa.json",
      "sha256": "81c552ae77c8f0b84da6aef50258d9feffe6554ffd21bb9b762d1ad7ee5d76a8",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/references.json",
      "sha256": "854287f79299430b8505ef42d98ceb24e6d76244d2ece161a852aedefb23eac6",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/repro-bound-1.log",
      "sha256": "45e9a727155a87395f091ecdb4eb976201355671636983d19bdb83d6972561c2",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/repro-bound-1.report.json",
      "sha256": "45e9a727155a87395f091ecdb4eb976201355671636983d19bdb83d6972561c2",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/repro-bound-2.log",
      "sha256": "671c1cea80db24ad514c4d5a96aeb500bc2c999d84b09a2cd5758614f655f4d5",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/repro-bound-2.report.json",
      "sha256": "671c1cea80db24ad514c4d5a96aeb500bc2c999d84b09a2cd5758614f655f4d5",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/runtime-parse.report.json",
      "sha256": "38374823d13118fae94db102f795aafe4d71dc1ccf12482e4198c7bcff0b58fe",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/source-final.report.json",
      "sha256": "39b5d91a356c726be6ab9e2c55cde34a168c3baf0091c0efb89540167136a802",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/source-metrics.json",
      "sha256": "f4caa458b36837284bec2412195a8e263d23271832a234d955239b27ff8536b8",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/source-reopen.log",
      "sha256": "5beb18a5658e4c6467522fc8475e751f3d86832e014644c8d310e1e65f9e7525",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/source.blend",
      "sha256": "51c397d4219f9bac1bfafc13790cf65e6adadba9bb6eeb3018a9f1ba80b84816",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-56/gondwanagaricites/r002/vertex-counts.report.json",
      "sha256": "951d4d42c761874a092d37904c6f5a5a4c4c8b25367c1768230464c45a88ca28",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/HANDOFF.md",
      "sha256": "05f554d03a3c4e3a11f810a22db91e48072df5151515cf4e84bc7f613bd9df80",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/arthrophycus-annulated-burrow/r001/rebuild-1/metrics.json",
      "sha256": "28c7212882fdfb43bcfd6e195e4b143e8bef05a0e12b60ff7b22bb7a102270d8",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/arthrophycus-annulated-burrow/r001/rebuild-1/model.glb",
      "sha256": "ce68d66fa8c50817f7eb69b067a340d12fcf875ed5a1e4d0357f0fac33fb2a43",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/arthrophycus-annulated-burrow/r001/rebuild-1/source-metrics.json",
      "sha256": "ab8f397570b60753f9793830babb900a41dafc6679a49ef6e7a3f042d78b3337",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/arthrophycus-annulated-burrow/r001/rebuild-1/source.blend",
      "sha256": "cb16869910e5094e9634dccb70a3d4d3b112113eec3516d71c4065c32dce600c",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/arthrophycus-annulated-burrow/r001/rebuild-2/metrics.json",
      "sha256": "30dff1a90e744cb8af891e375b90d4c744f8d3482ed7500b80531988161cdda2",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/arthrophycus-annulated-burrow/r001/rebuild-2/model.glb",
      "sha256": "ce68d66fa8c50817f7eb69b067a340d12fcf875ed5a1e4d0357f0fac33fb2a43",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/arthrophycus-annulated-burrow/r001/rebuild-2/source-metrics.json",
      "sha256": "ab8f397570b60753f9793830babb900a41dafc6679a49ef6e7a3f042d78b3337",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/arthrophycus-annulated-burrow/r001/rebuild-2/source.blend",
      "sha256": "6105879666a54d82aa2a24ab1e72215a3994744a1267b6cbfec08ddbbae91e6a",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/claim.json",
      "sha256": "731f05298a140634f7fbe564d0dc9bc09ec93190b3155250b8a3844a418d1cae",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/complete-checks.py",
      "sha256": "6a0c9b0c37451280b060048cbde5668acaf29d4a40f103986769b3007feab718",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/concept-generation.json",
      "sha256": "03662507be4e1c578f28294891d85cf582533fdb8de8579ac392c0a202099950",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/concept-original.png",
      "sha256": "7285ce56f8ede05348925a4480669500f32dc7ee9f2c7f53f1cd0f8fa19fb246",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/concept-prompt.txt",
      "sha256": "6c9914d0db89a006731268e03ce94b65cd2873657604b2aed5a220e98d24a31c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/count-vertices.py",
      "sha256": "82d370a6e91dbae032b953d33196b4f3407543f25bb366428986b72c514532a1",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/cycadeoidea/r001/rebuild-1/metrics.json",
      "sha256": "ff867a0025af84676803d68ed60e9775d41e67672af8ac4c7f47c9f1beaca54e",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/cycadeoidea/r001/rebuild-1/model.glb",
      "sha256": "78de39e5920c008fc7dd0cef55a27d6b177155e57248f8698830e74d60e7b256",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/cycadeoidea/r001/rebuild-1/source-metrics.json",
      "sha256": "1b8271d7f20c042a8329805bf824ce87d59881f874c3319d2b7c0d14ed1cf449",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/cycadeoidea/r001/rebuild-1/source.blend",
      "sha256": "3a95a9ed5b8311203f35841db32b9eccda4a99499f45c380ccaa7963e76c49dc",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/cycadeoidea/r001/rebuild-2/metrics.json",
      "sha256": "a2bed823771cc7d86ccca274019f876e7e00389ecb6092f0a634ae7838fce3a9",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/cycadeoidea/r001/rebuild-2/model.glb",
      "sha256": "78de39e5920c008fc7dd0cef55a27d6b177155e57248f8698830e74d60e7b256",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/cycadeoidea/r001/rebuild-2/source-metrics.json",
      "sha256": "1b8271d7f20c042a8329805bf824ce87d59881f874c3319d2b7c0d14ed1cf449",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/cycadeoidea/r001/rebuild-2/source.blend",
      "sha256": "aae9e990e0fd91ff5a6919dd39f2f356fb3460db1fcdf73d368105bb29fe0e57",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/deflation-hollow/r001/rebuild-1/metrics.json",
      "sha256": "d1295ddea72cd62dd020cc19c358d65b3ab55adfb117e4d71d0b9f8a38623f08",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/deflation-hollow/r001/rebuild-1/model.glb",
      "sha256": "c679676d46d8e51789a690db2f1590baa89c766cd50eb29700347150b43fd7be",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/deflation-hollow/r001/rebuild-1/source-metrics.json",
      "sha256": "07b7e359b8db02a593df72c20d84af75ebd2a15a3682ce2ae7ed167fcdc5825c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/deflation-hollow/r001/rebuild-1/source.blend",
      "sha256": "eb0747cfa3a528fc533439ff4c37ad4f08933b4b0959817bb76ad8282accf76b",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/deflation-hollow/r001/rebuild-2/metrics.json",
      "sha256": "2aae3d8fd0eebaebdb9eb5363379536da8c41c008d6f8d9f1778b2cdc737f0a4",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/deflation-hollow/r001/rebuild-2/model.glb",
      "sha256": "c679676d46d8e51789a690db2f1590baa89c766cd50eb29700347150b43fd7be",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/deflation-hollow/r001/rebuild-2/source-metrics.json",
      "sha256": "07b7e359b8db02a593df72c20d84af75ebd2a15a3682ce2ae7ed167fcdc5825c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/deflation-hollow/r001/rebuild-2/source.blend",
      "sha256": "bf0658294805777ed92a07cc2936cf93f4a5bcb71fb70a2ae4ad8ba2d6ee33ec",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/delivery-checksums.sha256",
      "sha256": "616762af00aff1394aa0b81d07a5709565d8ee08f811ce271c35fb3938345c66",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-1/db2a852fb4ef6d6cd2765e02f485eac7d24f654a5684c038de0ed2790b7f6b9a/20261020T020828-2a4bc183529746858a491009ebe04b08/outputs/metrics.json",
      "sha256": "ccc78e8458793e0e3618b8d3e6f080b7d6aede56f818ea226feb5feb70defa81",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-1/db2a852fb4ef6d6cd2765e02f485eac7d24f654a5684c038de0ed2790b7f6b9a/20261020T020828-2a4bc183529746858a491009ebe04b08/outputs/model.glb",
      "sha256": "a32b30732582580884b7f6de257a22c701df20f2359e9183585a10a8f959834c",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-1/db2a852fb4ef6d6cd2765e02f485eac7d24f654a5684c038de0ed2790b7f6b9a/20261020T020828-2a4bc183529746858a491009ebe04b08/outputs/source-metrics.json",
      "sha256": "ab8f397570b60753f9793830babb900a41dafc6679a49ef6e7a3f042d78b3337",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-1/db2a852fb4ef6d6cd2765e02f485eac7d24f654a5684c038de0ed2790b7f6b9a/20261020T020828-2a4bc183529746858a491009ebe04b08/outputs/source.blend",
      "sha256": "49bb0b1d1888dc053f2a5e41d557b34a743a17785f0af91373958722b4d7315f",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-1/db2a852fb4ef6d6cd2765e02f485eac7d24f654a5684c038de0ed2790b7f6b9a/20261020T020828-2a4bc183529746858a491009ebe04b08/request.json",
      "sha256": "ec5c2055346cf32867ee8c289683badaff68b1602dca9f7f979a2da80b86b1c8",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-1/db2a852fb4ef6d6cd2765e02f485eac7d24f654a5684c038de0ed2790b7f6b9a/20261020T020828-2a4bc183529746858a491009ebe04b08/result.json",
      "sha256": "de5a422d88f4f5803fb74f5bf99ca3dcc98ede652db02184d26bd8571b484080",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-1/db2a852fb4ef6d6cd2765e02f485eac7d24f654a5684c038de0ed2790b7f6b9a/20261020T020828-2a4bc183529746858a491009ebe04b08/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-1/db2a852fb4ef6d6cd2765e02f485eac7d24f654a5684c038de0ed2790b7f6b9a/20261020T020828-2a4bc183529746858a491009ebe04b08/stdout.log",
      "sha256": "9d5f3877119b754acfc42dc9cbef7575e5d6562b57f077200f77e53aa48eb8a4",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-2/582f09c9ee6630979e7758f387a43ec865707bd5d1684bdf8d9d1f7d0b352629/20261020T020829-ddcd6de550fe46e3a10da06361fdcbd9/outputs/metrics.json",
      "sha256": "1bb908e7fad19011c27564005e66c147e81dbc0ca6633e6ea1aea959fbeb63fd",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-2/582f09c9ee6630979e7758f387a43ec865707bd5d1684bdf8d9d1f7d0b352629/20261020T020829-ddcd6de550fe46e3a10da06361fdcbd9/outputs/model.glb",
      "sha256": "a32b30732582580884b7f6de257a22c701df20f2359e9183585a10a8f959834c",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-2/582f09c9ee6630979e7758f387a43ec865707bd5d1684bdf8d9d1f7d0b352629/20261020T020829-ddcd6de550fe46e3a10da06361fdcbd9/outputs/source-metrics.json",
      "sha256": "ab8f397570b60753f9793830babb900a41dafc6679a49ef6e7a3f042d78b3337",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-2/582f09c9ee6630979e7758f387a43ec865707bd5d1684bdf8d9d1f7d0b352629/20261020T020829-ddcd6de550fe46e3a10da06361fdcbd9/outputs/source.blend",
      "sha256": "0c7eda57eae6f8c2159516d46dff2e2dbec9a461298744695cdbd9ac632a7fd3",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-2/582f09c9ee6630979e7758f387a43ec865707bd5d1684bdf8d9d1f7d0b352629/20261020T020829-ddcd6de550fe46e3a10da06361fdcbd9/request.json",
      "sha256": "891dc44b95c7b3cb96e21f654ebc1491892cf1fa9523105e43c50b82d5721986",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-2/582f09c9ee6630979e7758f387a43ec865707bd5d1684bdf8d9d1f7d0b352629/20261020T020829-ddcd6de550fe46e3a10da06361fdcbd9/result.json",
      "sha256": "42b1482a92fbbe9a5c7b60abf4a17497a4589388ecf85e0174fba8d50c5d258e",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-2/582f09c9ee6630979e7758f387a43ec865707bd5d1684bdf8d9d1f7d0b352629/20261020T020829-ddcd6de550fe46e3a10da06361fdcbd9/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/arthrophycus-annulated-burrow/r002/semantic-rebuild-2/582f09c9ee6630979e7758f387a43ec865707bd5d1684bdf8d9d1f7d0b352629/20261020T020829-ddcd6de550fe46e3a10da06361fdcbd9/stdout.log",
      "sha256": "6a2c4dae1046788e2fb2e8c4924477181511923fbdf901ff5bc29e145b5853a2",
      "origin": "source",
      "owner": "arthrophycus-annulated-burrow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-1/02279252051a4b675efb166c193b143eaa825f26777ff446105c6fae4ca56b81/20261020T020818-ed4fb4d2f56f4b2ca4d1573f70d8afb2/outputs/metrics.json",
      "sha256": "4da6461b43f99b968e3a938a249c77c8040b4e8ac5dd5e4704dbb27749ef35d1",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-1/02279252051a4b675efb166c193b143eaa825f26777ff446105c6fae4ca56b81/20261020T020818-ed4fb4d2f56f4b2ca4d1573f70d8afb2/outputs/model.glb",
      "sha256": "9388a918314ca5426c992d9f1702e881d369bc5a15ad43d5dce18afcf80c0fd0",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-1/02279252051a4b675efb166c193b143eaa825f26777ff446105c6fae4ca56b81/20261020T020818-ed4fb4d2f56f4b2ca4d1573f70d8afb2/outputs/source-metrics.json",
      "sha256": "2f848863758946f44ad5c8f050f47016430836610dbda3b2260ebc9052470c4b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-1/02279252051a4b675efb166c193b143eaa825f26777ff446105c6fae4ca56b81/20261020T020818-ed4fb4d2f56f4b2ca4d1573f70d8afb2/outputs/source.blend",
      "sha256": "84063408d4ca519b04902d5d4f09896d63dc2d38a26274c716352be14bfb8d70",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-1/02279252051a4b675efb166c193b143eaa825f26777ff446105c6fae4ca56b81/20261020T020818-ed4fb4d2f56f4b2ca4d1573f70d8afb2/request.json",
      "sha256": "736161b53ce3003847c5537bd07db2aac979b96a5b9ee26954b0e214c5c69639",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-1/02279252051a4b675efb166c193b143eaa825f26777ff446105c6fae4ca56b81/20261020T020818-ed4fb4d2f56f4b2ca4d1573f70d8afb2/result.json",
      "sha256": "4598ac5f0266427bac86f7f9857f5842d7c27ac46730561f292059fe7cfa9e39",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-1/02279252051a4b675efb166c193b143eaa825f26777ff446105c6fae4ca56b81/20261020T020818-ed4fb4d2f56f4b2ca4d1573f70d8afb2/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-1/02279252051a4b675efb166c193b143eaa825f26777ff446105c6fae4ca56b81/20261020T020818-ed4fb4d2f56f4b2ca4d1573f70d8afb2/stdout.log",
      "sha256": "655e3351fb79fba47c77c365ae97450819146c87e32315937c44e685ceed3325",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-2/9eb6e96cd529fc72fe640ffbde2d8cdfd912dd29d6d5451eab261cc53a54c512/20261020T020820-ae404598cecb456092f8010239c81051/outputs/metrics.json",
      "sha256": "b023d28bac8dbdbb49ed7a389d8e1ab2476981cb2c279067a3826b99f2409903",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-2/9eb6e96cd529fc72fe640ffbde2d8cdfd912dd29d6d5451eab261cc53a54c512/20261020T020820-ae404598cecb456092f8010239c81051/outputs/model.glb",
      "sha256": "9388a918314ca5426c992d9f1702e881d369bc5a15ad43d5dce18afcf80c0fd0",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-2/9eb6e96cd529fc72fe640ffbde2d8cdfd912dd29d6d5451eab261cc53a54c512/20261020T020820-ae404598cecb456092f8010239c81051/outputs/source-metrics.json",
      "sha256": "2f848863758946f44ad5c8f050f47016430836610dbda3b2260ebc9052470c4b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-2/9eb6e96cd529fc72fe640ffbde2d8cdfd912dd29d6d5451eab261cc53a54c512/20261020T020820-ae404598cecb456092f8010239c81051/outputs/source.blend",
      "sha256": "cbf96124437a34807203b2fbc3840c1a629d67370566b48864aa784a0d9bc6fd",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-2/9eb6e96cd529fc72fe640ffbde2d8cdfd912dd29d6d5451eab261cc53a54c512/20261020T020820-ae404598cecb456092f8010239c81051/request.json",
      "sha256": "3ac04727ed5d0304c34044efb5b032ec189bed138fa47f9f2044ca54c8d6e5e6",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-2/9eb6e96cd529fc72fe640ffbde2d8cdfd912dd29d6d5451eab261cc53a54c512/20261020T020820-ae404598cecb456092f8010239c81051/result.json",
      "sha256": "0218f17362ef40a4a0abf5dec0a03c4aac7022fe8cf8235fdeebf816e1fe1b19",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-2/9eb6e96cd529fc72fe640ffbde2d8cdfd912dd29d6d5451eab261cc53a54c512/20261020T020820-ae404598cecb456092f8010239c81051/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/cycadeoidea/r002/semantic-rebuild-2/9eb6e96cd529fc72fe640ffbde2d8cdfd912dd29d6d5451eab261cc53a54c512/20261020T020820-ae404598cecb456092f8010239c81051/stdout.log",
      "sha256": "bc52ff52f1e92a3360f395185b6fdd782bd95e413824a6038795a7e575c19b2c",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-1/80f80a9368eae3d3b330ef4f1519e69d33c590559e6a0380eeaf117c3d22ed7c/20261020T020825-cf9bcf191ed6418cb4b23adcec0dfe49/outputs/metrics.json",
      "sha256": "32f7eeee0f6e444c7bf03b46c947765bfee76ba72b9cdd6c2abad0a5d97af75d",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-1/80f80a9368eae3d3b330ef4f1519e69d33c590559e6a0380eeaf117c3d22ed7c/20261020T020825-cf9bcf191ed6418cb4b23adcec0dfe49/outputs/model.glb",
      "sha256": "c679676d46d8e51789a690db2f1590baa89c766cd50eb29700347150b43fd7be",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-1/80f80a9368eae3d3b330ef4f1519e69d33c590559e6a0380eeaf117c3d22ed7c/20261020T020825-cf9bcf191ed6418cb4b23adcec0dfe49/outputs/source-metrics.json",
      "sha256": "07b7e359b8db02a593df72c20d84af75ebd2a15a3682ce2ae7ed167fcdc5825c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-1/80f80a9368eae3d3b330ef4f1519e69d33c590559e6a0380eeaf117c3d22ed7c/20261020T020825-cf9bcf191ed6418cb4b23adcec0dfe49/outputs/source.blend",
      "sha256": "6bc1f770c152082170a0e0f848eea22776547bd12419687d04789e46d7300daf",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-1/80f80a9368eae3d3b330ef4f1519e69d33c590559e6a0380eeaf117c3d22ed7c/20261020T020825-cf9bcf191ed6418cb4b23adcec0dfe49/request.json",
      "sha256": "5556f249563dd285fdefd8d7c150a4aa4d0c3cfa89de0dedf343c2ea86b29903",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-1/80f80a9368eae3d3b330ef4f1519e69d33c590559e6a0380eeaf117c3d22ed7c/20261020T020825-cf9bcf191ed6418cb4b23adcec0dfe49/result.json",
      "sha256": "6c68507f6fdd95d381c65279f838da912a223a9d75fdc3310df0bc9e47719560",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-1/80f80a9368eae3d3b330ef4f1519e69d33c590559e6a0380eeaf117c3d22ed7c/20261020T020825-cf9bcf191ed6418cb4b23adcec0dfe49/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-1/80f80a9368eae3d3b330ef4f1519e69d33c590559e6a0380eeaf117c3d22ed7c/20261020T020825-cf9bcf191ed6418cb4b23adcec0dfe49/stdout.log",
      "sha256": "1f76c2cd5481a5770fb047ab2104d6d90b4daa64a91d592f243fc94953d40255",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-2/b944457a462d0c90203d3628969b95b8c9a40afc0a75c6253b29b1363e2c1409/20261020T020826-27d9fb69b88e4e6dafcac75b19cdfe79/outputs/metrics.json",
      "sha256": "7adb659a08aa1c90f7cccac3f89b890c231dae71ea64419571bbce78d4199a11",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-2/b944457a462d0c90203d3628969b95b8c9a40afc0a75c6253b29b1363e2c1409/20261020T020826-27d9fb69b88e4e6dafcac75b19cdfe79/outputs/model.glb",
      "sha256": "c679676d46d8e51789a690db2f1590baa89c766cd50eb29700347150b43fd7be",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-2/b944457a462d0c90203d3628969b95b8c9a40afc0a75c6253b29b1363e2c1409/20261020T020826-27d9fb69b88e4e6dafcac75b19cdfe79/outputs/source-metrics.json",
      "sha256": "07b7e359b8db02a593df72c20d84af75ebd2a15a3682ce2ae7ed167fcdc5825c",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-2/b944457a462d0c90203d3628969b95b8c9a40afc0a75c6253b29b1363e2c1409/20261020T020826-27d9fb69b88e4e6dafcac75b19cdfe79/outputs/source.blend",
      "sha256": "201481eb626000f74fd95d357851f3d11b081d88dc99941b0977d586a96fd392",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-2/b944457a462d0c90203d3628969b95b8c9a40afc0a75c6253b29b1363e2c1409/20261020T020826-27d9fb69b88e4e6dafcac75b19cdfe79/request.json",
      "sha256": "d6061d5400b5f6d029d17f6215354bc51b5a4bc5828faaac5a7745f2db9722b6",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-2/b944457a462d0c90203d3628969b95b8c9a40afc0a75c6253b29b1363e2c1409/20261020T020826-27d9fb69b88e4e6dafcac75b19cdfe79/result.json",
      "sha256": "7cd1c70022c5984072fe1ae26cb62718be373a71bf1550e7d9cc5a8f663ab7eb",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-2/b944457a462d0c90203d3628969b95b8c9a40afc0a75c6253b29b1363e2c1409/20261020T020826-27d9fb69b88e4e6dafcac75b19cdfe79/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/deflation-hollow/r001/semantic-rebuild-2/b944457a462d0c90203d3628969b95b8c9a40afc0a75c6253b29b1363e2c1409/20261020T020826-27d9fb69b88e4e6dafcac75b19cdfe79/stdout.log",
      "sha256": "2c3a0853f3185893fc0298b5117ceb144a32c92a94c4c68e25f856bab6c4b97b",
      "origin": "source",
      "owner": "deflation-hollow"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-1/fb6a74c26a649c8731cab5a146bff5db3452b13bc6e4a8a04bcbe5d064f60b1c/20261020T020822-d3bf4462d94b4dfd9b7aee06f470a071/outputs/metrics.json",
      "sha256": "108a59d9ecc4b553d02ed3e641d0d1b1e2c963e83b164599215aa1af67d95783",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-1/fb6a74c26a649c8731cab5a146bff5db3452b13bc6e4a8a04bcbe5d064f60b1c/20261020T020822-d3bf4462d94b4dfd9b7aee06f470a071/outputs/model.glb",
      "sha256": "8133ad81f4f3d18b4d0ebd5d29ca2fe540039254b6efc8522fe20d2ec4b4036a",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-1/fb6a74c26a649c8731cab5a146bff5db3452b13bc6e4a8a04bcbe5d064f60b1c/20261020T020822-d3bf4462d94b4dfd9b7aee06f470a071/outputs/source-metrics.json",
      "sha256": "f4caa458b36837284bec2412195a8e263d23271832a234d955239b27ff8536b8",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-1/fb6a74c26a649c8731cab5a146bff5db3452b13bc6e4a8a04bcbe5d064f60b1c/20261020T020822-d3bf4462d94b4dfd9b7aee06f470a071/outputs/source.blend",
      "sha256": "088081656b3a6416753cd09955e208c67f8a6e8facbdc8e72b644a88c8f6fb6b",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-1/fb6a74c26a649c8731cab5a146bff5db3452b13bc6e4a8a04bcbe5d064f60b1c/20261020T020822-d3bf4462d94b4dfd9b7aee06f470a071/request.json",
      "sha256": "a866a24499bbbc669f53687efc5272cd5fe2f00fff96e8887243df179fdcadc7",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-1/fb6a74c26a649c8731cab5a146bff5db3452b13bc6e4a8a04bcbe5d064f60b1c/20261020T020822-d3bf4462d94b4dfd9b7aee06f470a071/result.json",
      "sha256": "ac5792a10e5dc4a1e7b6b48b04e6927f24a293a8ca1d283744887f4811c0004e",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-1/fb6a74c26a649c8731cab5a146bff5db3452b13bc6e4a8a04bcbe5d064f60b1c/20261020T020822-d3bf4462d94b4dfd9b7aee06f470a071/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-1/fb6a74c26a649c8731cab5a146bff5db3452b13bc6e4a8a04bcbe5d064f60b1c/20261020T020822-d3bf4462d94b4dfd9b7aee06f470a071/stdout.log",
      "sha256": "2123d5a5db1b9fd1e55d5aa112bae38495d38f41c5e96591cb27b09ded556a4b",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-2/5afc523149fa2cff4b70da1858b90100297bde1507043f9351ea2b5e790ef247/20261020T020823-fd20254bcff24b8abd963670c6f98a83/outputs/metrics.json",
      "sha256": "af2e3951fab15a9262a1aa71f5c532f16d6079eed7dc1643b4f6b859e5fe06ae",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-2/5afc523149fa2cff4b70da1858b90100297bde1507043f9351ea2b5e790ef247/20261020T020823-fd20254bcff24b8abd963670c6f98a83/outputs/model.glb",
      "sha256": "8133ad81f4f3d18b4d0ebd5d29ca2fe540039254b6efc8522fe20d2ec4b4036a",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-2/5afc523149fa2cff4b70da1858b90100297bde1507043f9351ea2b5e790ef247/20261020T020823-fd20254bcff24b8abd963670c6f98a83/outputs/source-metrics.json",
      "sha256": "f4caa458b36837284bec2412195a8e263d23271832a234d955239b27ff8536b8",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-2/5afc523149fa2cff4b70da1858b90100297bde1507043f9351ea2b5e790ef247/20261020T020823-fd20254bcff24b8abd963670c6f98a83/outputs/source.blend",
      "sha256": "fb1c908cf3b47e7f646667823c78b59e9203d4508b1a2bbeb49c8b66990d41a0",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-2/5afc523149fa2cff4b70da1858b90100297bde1507043f9351ea2b5e790ef247/20261020T020823-fd20254bcff24b8abd963670c6f98a83/request.json",
      "sha256": "61ab04ca73398e25c94d32b619fdd113c603cd285d68ec8eebd4f054635ffb25",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-2/5afc523149fa2cff4b70da1858b90100297bde1507043f9351ea2b5e790ef247/20261020T020823-fd20254bcff24b8abd963670c6f98a83/result.json",
      "sha256": "2069ddbd0147b6485c7062a8eb45f7b1a35232bd3f97f29fbb9cafbeb15acdb9",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-2/5afc523149fa2cff4b70da1858b90100297bde1507043f9351ea2b5e790ef247/20261020T020823-fd20254bcff24b8abd963670c6f98a83/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/build/gondwanagaricites/r002/semantic-rebuild-2/5afc523149fa2cff4b70da1858b90100297bde1507043f9351ea2b5e790ef247/20261020T020823-fd20254bcff24b8abd963670c6f98a83/stdout.log",
      "sha256": "fc594a26a9c3f31646c998cc5920506f7a77bca2e42988ffb0b6e5ebc8ff110e",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/runs/20261020T020818-83e5c2d1dfaf48c79ba010987447d224/manifest.json",
      "sha256": "33b933c9a94abdb4f63de2c3829e23335ee6cddef15f3d502bf3510da0087b09",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-rebuild-runs/runs/20261020T020818-83e5c2d1dfaf48c79ba010987447d224/summary.json",
      "sha256": "6f48e3e5c40f3098ecdd4a21b3474e3667d38ecd3ec036b75f7696822d45ac14",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/final-selection.json",
      "sha256": "6100320265aa90f3e24aca169e662e6d5f91778c5fcfc6be22b35ed2e511d602",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/generator.py",
      "sha256": "d496960e7ba16268b8b7e0575d96032726dc3630c53bb0b469af54d20f6ba3e8",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/gondwanagaricites/r001/rebuild-1/metrics.json",
      "sha256": "ebedabb282dc2fa5f4b84f684d9a0b1981550b0e487da75f6dc7b6a706e06587",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/gondwanagaricites/r001/rebuild-1/model.glb",
      "sha256": "75796a71ff532addfe21c632c7421f9ddfdb479ceec960a03af5abb216310386",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/gondwanagaricites/r001/rebuild-1/source-metrics.json",
      "sha256": "6905b4246ec06d0b67fe5aca7154214f6d0e64e0ef1f1ef37975c1297795ef18",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/gondwanagaricites/r001/rebuild-1/source.blend",
      "sha256": "6ad90d6094c38bc6fb3dfc5f3ed45832814ba92fddc7a0149c53f2b95033519b",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/gondwanagaricites/r001/rebuild-2/metrics.json",
      "sha256": "50448dbaf46763d243a1be6632201a760d50235172e7000b42767bddd1a00647",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/gondwanagaricites/r001/rebuild-2/model.glb",
      "sha256": "75796a71ff532addfe21c632c7421f9ddfdb479ceec960a03af5abb216310386",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/gondwanagaricites/r001/rebuild-2/source-metrics.json",
      "sha256": "6905b4246ec06d0b67fe5aca7154214f6d0e64e0ef1f1ef37975c1297795ef18",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/gondwanagaricites/r001/rebuild-2/source.blend",
      "sha256": "7f6f43b0ce200ec9f3cb982643b251fbeec06c76e56bc82a78dfff2b4a73a351",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/handoff.json",
      "sha256": "dffba5f08c8a2aa691bbfc7f3bef6e731dd781cea27e36a888ad549acee4015a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/package-candidates.py",
      "sha256": "783ceff60ae90415a5b9dfd6e5175596c198c13e61f45a1704c0dca4564c1c0c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/planning-integrity.json",
      "sha256": "4c5bab04720b96bca7ad8a7dae30293b49f95413a5c64adeec1a9a6fdbdc4fc3",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/rebuild-jobs.json",
      "sha256": "bf4f3b6f21a182dc8be02718542914290f7068a4de7a7956c947acdfd20979cc",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/render-batch56.py",
      "sha256": "33ed7fc4b39a41e67f79e51d41fd4457f2a3087085837e59c8981d87e7bb412d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/render-canonical.py",
      "sha256": "ab490a7dee7fa41ccd983164072ca6db674d1aea563cb7a59f8086128ef23b02",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-build-jobs.json",
      "sha256": "4fe7a121e208698ee2246a4438a14ad64e2a15d13379934d8b2ffcd5ad8a03b5",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/cycadeoidea/r002/candidate-build/06aa3335be6c7d5f4ca5a4b1ded7ac1ca507a9168a1c1bb555c8e009bd5ce438/20261020T020738-4a67eeab0dbc4862a3ca37b4ded5deb9/outputs/metrics.json",
      "sha256": "f8fd370c46223d30cc00b030b8064291eb66ae5bf72cfe4ab3b4bfa7e2265034",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/cycadeoidea/r002/candidate-build/06aa3335be6c7d5f4ca5a4b1ded7ac1ca507a9168a1c1bb555c8e009bd5ce438/20261020T020738-4a67eeab0dbc4862a3ca37b4ded5deb9/outputs/model.glb",
      "sha256": "9388a918314ca5426c992d9f1702e881d369bc5a15ad43d5dce18afcf80c0fd0",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/cycadeoidea/r002/candidate-build/06aa3335be6c7d5f4ca5a4b1ded7ac1ca507a9168a1c1bb555c8e009bd5ce438/20261020T020738-4a67eeab0dbc4862a3ca37b4ded5deb9/outputs/source-metrics.json",
      "sha256": "2f848863758946f44ad5c8f050f47016430836610dbda3b2260ebc9052470c4b",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/cycadeoidea/r002/candidate-build/06aa3335be6c7d5f4ca5a4b1ded7ac1ca507a9168a1c1bb555c8e009bd5ce438/20261020T020738-4a67eeab0dbc4862a3ca37b4ded5deb9/outputs/source.blend",
      "sha256": "b2dd206c55a5436b9af4f58115dd6684e9ed534df4d97945e5f2f18d2f5934e5",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/cycadeoidea/r002/candidate-build/06aa3335be6c7d5f4ca5a4b1ded7ac1ca507a9168a1c1bb555c8e009bd5ce438/20261020T020738-4a67eeab0dbc4862a3ca37b4ded5deb9/request.json",
      "sha256": "4860c1b5bc2e4e38777851dcb5239de371e672a3b484a7684c20083c68fb64ef",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/cycadeoidea/r002/candidate-build/06aa3335be6c7d5f4ca5a4b1ded7ac1ca507a9168a1c1bb555c8e009bd5ce438/20261020T020738-4a67eeab0dbc4862a3ca37b4ded5deb9/result.json",
      "sha256": "3a2b641a5857b8030054ab8ba2a8d6f9c332265e5c73d5991a501252cac58b47",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/cycadeoidea/r002/candidate-build/06aa3335be6c7d5f4ca5a4b1ded7ac1ca507a9168a1c1bb555c8e009bd5ce438/20261020T020738-4a67eeab0dbc4862a3ca37b4ded5deb9/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/cycadeoidea/r002/candidate-build/06aa3335be6c7d5f4ca5a4b1ded7ac1ca507a9168a1c1bb555c8e009bd5ce438/20261020T020738-4a67eeab0dbc4862a3ca37b4ded5deb9/stdout.log",
      "sha256": "80b42bb339303c1f5f5fd7524f9b5fb979fd73d7ee4700b3858813c382ef8086",
      "origin": "source",
      "owner": "cycadeoidea"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/gondwanagaricites/r002/candidate-build/0a383decb6ffc6b200edded1b0e26859e94a721c2b1e949a4e10bcbdbe1e6aef/20261020T020739-6dc6db96ea2947ddaa88a4b818cb4890/outputs/metrics.json",
      "sha256": "a9814f8f19ce2c5b5662e9ed63ca8a1e3544dd7eb895c54f30cec116d19f02c0",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/gondwanagaricites/r002/candidate-build/0a383decb6ffc6b200edded1b0e26859e94a721c2b1e949a4e10bcbdbe1e6aef/20261020T020739-6dc6db96ea2947ddaa88a4b818cb4890/outputs/model.glb",
      "sha256": "8133ad81f4f3d18b4d0ebd5d29ca2fe540039254b6efc8522fe20d2ec4b4036a",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/gondwanagaricites/r002/candidate-build/0a383decb6ffc6b200edded1b0e26859e94a721c2b1e949a4e10bcbdbe1e6aef/20261020T020739-6dc6db96ea2947ddaa88a4b818cb4890/outputs/source-metrics.json",
      "sha256": "f4caa458b36837284bec2412195a8e263d23271832a234d955239b27ff8536b8",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/gondwanagaricites/r002/candidate-build/0a383decb6ffc6b200edded1b0e26859e94a721c2b1e949a4e10bcbdbe1e6aef/20261020T020739-6dc6db96ea2947ddaa88a4b818cb4890/outputs/source.blend",
      "sha256": "51c397d4219f9bac1bfafc13790cf65e6adadba9bb6eeb3018a9f1ba80b84816",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/gondwanagaricites/r002/candidate-build/0a383decb6ffc6b200edded1b0e26859e94a721c2b1e949a4e10bcbdbe1e6aef/20261020T020739-6dc6db96ea2947ddaa88a4b818cb4890/request.json",
      "sha256": "b77ba4ebe5b63f8da56fb75002b7a5395c771daf8820ab08f6bcb41021483de9",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/gondwanagaricites/r002/candidate-build/0a383decb6ffc6b200edded1b0e26859e94a721c2b1e949a4e10bcbdbe1e6aef/20261020T020739-6dc6db96ea2947ddaa88a4b818cb4890/result.json",
      "sha256": "89fac892bbee67dcf32c7646f4142bb18a7cbce67e50fd1b0fadee5c7de31459",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/gondwanagaricites/r002/candidate-build/0a383decb6ffc6b200edded1b0e26859e94a721c2b1e949a4e10bcbdbe1e6aef/20261020T020739-6dc6db96ea2947ddaa88a4b818cb4890/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/build/gondwanagaricites/r002/candidate-build/0a383decb6ffc6b200edded1b0e26859e94a721c2b1e949a4e10bcbdbe1e6aef/20261020T020739-6dc6db96ea2947ddaa88a4b818cb4890/stdout.log",
      "sha256": "2044f4669cae83d3cb45926e0006a8e6e028343e32bef1dc42c53f8364f7482c",
      "origin": "source",
      "owner": "gondwanagaricites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/runs/20261020T020738-eae45a82571543029364f8044a81f3f4/manifest.json",
      "sha256": "7b226e0c28b0f56589453ff5294cd991992f3740be522dde0899b52a9154cb25",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/repair-runs/runs/20261020T020738-eae45a82571543029364f8044a81f3f4/summary.json",
      "sha256": "7c1e4a4797fe59752a3ebdf99ff1915f9ed5e87767c0dc824771ca9828d6afb3",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/run-lifecycle.py",
      "sha256": "653ce609d1103404b6a1797e7bbf296664ce5abc3ecece0a252ab1ae21c21016",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-56/runtime-parse.mjs",
      "sha256": "fb938eb6db606a51b904de3f58b2557b618fc5963bfcf225ad990b0b1244164c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-independent-20261020/disposition.md",
      "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/assets/card-previews/arthrophycus-annulated-burrow-v2-768-q90.webp",
      "sha256": "c745ef1b5a88a001955c8a108db3b73ee01e63e55e0a156a4383ced233717b89",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/assets/card-previews/cycadeoidea-v2-768-q90.webp",
      "sha256": "e3b40556445e2b95511219ae560904754236902364711c7c33312255f728cc84",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/assets/card-previews/deflation-hollow-v2-768-q90.webp",
      "sha256": "0bd81a398954cdd7629ae9a64c7450ec9e3f4bfa4c843e0401027634971ccf85",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/assets/card-previews/gondwanagaricites-v2-768-q90.webp",
      "sha256": "3df34c9d39cb7f8dbc1af67e7ce0152b2373b65e954ce868cc98c0bf67d937e3",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/assets/turntables/index.json",
      "sha256": "9e680d380178684ed2ee52fb035bc32d0169bfa7c71b754931e468b9f281d90f",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/references/arthrophycus-annulated-burrow.png",
      "sha256": "1c00c7b171083753aba0a485da5806ab7ff5fec574d7813f39698266d591204f",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/references/cycadeoidea.png",
      "sha256": "11de5a9d35f3f1084666f37ad577398687888fa39e8efd6ce4ac1b44fb6f18d8",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/references/deflation-hollow.png",
      "sha256": "2f01afbfb29c8564d5ad353c5bc1c195d4eeea3991c088b5756a4e97efc5e6b2",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/references/gondwanagaricites.png",
      "sha256": "2853d0b7d6909d5aa12bbf25ea0495fa275b6263d01cb2809d35761376f98935",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture/render-report.json",
      "sha256": "c1ed101baab8a80cfef0e2b4c479b411374f23b46bdee79769fad7d279badf44",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture-inputs.json",
      "sha256": "c27a8df2d16f5a06321b49c4eaee36a7fca7f0ec3132745157690d70ea9ded80",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture-provenance.json",
      "sha256": "273923edb8d57c79d2e71bc1eb577fa562fa023421a5bfd0f639a39772bb162c",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/capture-zip-verification.json",
      "sha256": "3079fcf81466fd1aa05a460e4a98eb1ceb9156c43406beb16e379cabc827000c",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/metadata-mapping.json",
      "sha256": "fffbd197a63101ae51109481e91627012c1a18de323cde2f33f31b3013e68a3f",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/preparation.json",
      "sha256": "5ce4472a54c57399d4acbc86d00d7afb0bc0b55881238f120c7d65e0fdc579e5",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/review/lowpoly-batches56-57-independent-audit.md",
      "sha256": "ac85057fd1cc1d83db453441fcdb9b5717cd5019ac568c91b15491a7c76c60c8",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/review/lowpoly-round21-repair56-57-focused-qa.md",
      "sha256": "094a24544eb4045a11cc0c05b0828aac37b3b8ba89855fd36a45f2d9cbffb450",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch56-release-20261020/source-inventory.json",
      "sha256": "a6479d2dbf93321c70ff5bf993ae3901cc47106fadc422853495eab2ba6c890b",
      "origin": "release",
      "owner": "$batch"
    }
  ]
};

/** Exact bounded Batch57 release; unchanged formal gates. */
export const BATCH57_RELEASE = {
  "version": 1,
  "scope": "batch57-20261020",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "provider_generation_timestamp": "unknown",
  "source_commit": "75f08656c73718ad707c0493e9bf8137f3efb45d",
  "review_commit": "adace4d7fd4cd091ab63f60ee4737f77096ba666",
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  },
  "base_descriptor": {
    "path": "assets/releases/concept-landair-20261019.json",
    "sha256": "bb8e0aa3846a0cca9b381e675a988b756c652546efb44405fb4b27927895136b"
  },
  "source_bundle": {
    "path": "qa/batch57-release-20261020/source-bundle.json",
    "sha256": "502372ca0aed56fc4a02576bd53cb22ae3e85c209b230b1a2448915f0f93f8ab"
  },
  "review": {
    "path": "qa/batch57-independent-20261020/disposition.md",
    "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c"
  },
  "capture": {
    "report": {
      "path": "qa/batch57-release-20261020/capture/render-report.json",
      "sha256": "c1ed101baab8a80cfef0e2b4c479b411374f23b46bdee79769fad7d279badf44"
    },
    "index": {
      "path": "qa/batch57-release-20261020/capture/assets/turntables/index.json",
      "sha256": "9e680d380178684ed2ee52fb035bc32d0169bfa7c71b754931e468b9f281d90f"
    },
    "zip_verification": {
      "path": "qa/batch57-release-20261020/capture-zip-verification.json",
      "sha256": "85cef2709e55b14d23dcb9df973fdbb43b178268573f213386a36f839f8c773f"
    }
  },
  "excluded_ids": [
    "nidula-baltica"
  ],
  "additions": [
    {
      "id": "quatsinoporites",
      "revision": "r004",
      "source_commit": "75f08656c73718ad707c0493e9bf8137f3efb45d",
      "review_commit": "adace4d7fd4cd091ab63f60ee4737f77096ba666",
      "metadata": {
        "path": "assets/additions/quatsinoporites/batch57-20261020/release-metadata.json",
        "sha256": "d7e5e32d59d184dcc33e129f6fc31826834d26aef843a5ba31446bc3dfa5a79f"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/candidate.json",
        "sha256": "701fba7892e74e3981c2a8c95cfed718a93999e928430037e4f28710eb7b87d8"
      },
      "review": {
        "path": "qa/batch57-independent-20261020/disposition.md",
        "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/metadata.json",
        "sha256": "74c532514e627e54c6b1126564b0215844c4ad8dc9814adbc8cb2749d35bbd20"
      },
      "original_metadata": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/metadata.json",
        "sha256": "74c532514e627e54c6b1126564b0215844c4ad8dc9814adbc8cb2749d35bbd20"
      },
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/brief.json",
        "sha256": "1d4c516bd4dbb5cd893615f785a35f5b5a7bcc894c8404e174a00cb39813a64f"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/render-manifest.json",
        "sha256": "512629b76843cb7c49139e80e04350c543a1462182044bc33cba799f26ee8c36"
      },
      "capture_reference": {
        "path": "qa/batch57-release-20261020/capture/references/quatsinoporites.png",
        "sha256": "42947b74d001ca8c8022ef6a7eaa71959aa9047efeb1e3ece5c0d0f6f4c8aead"
      }
    },
    {
      "id": "cave-column",
      "revision": "r002",
      "source_commit": "75f08656c73718ad707c0493e9bf8137f3efb45d",
      "review_commit": "adace4d7fd4cd091ab63f60ee4737f77096ba666",
      "metadata": {
        "path": "assets/additions/cave-column/batch57-20261020/release-metadata.json",
        "sha256": "3045fd1d5e93738e16a63b79b97753011812541c0821b0d2730fd21de2ba06ef"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/candidate.json",
        "sha256": "1d6eb031640fa8de2c328fe1a4e8573c14329543c18c12e2cb2920723c905029"
      },
      "review": {
        "path": "qa/batch57-independent-20261020/disposition.md",
        "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/metrics.json",
        "sha256": "5b9db4f2922ab0360a8038a469c7f979a041f3a6efc27169b8601702452d76c5"
      },
      "original_metadata": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/metadata.json",
        "sha256": "e6a3001fe18df66e5b2a41bec92f980ca3076cfe17fe208f018c1f913b8f486a"
      },
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/brief.json",
        "sha256": "717a796450a262f97e204e51926fdc69b0f4c23277d47162977f454030299a36"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/render-manifest.json",
        "sha256": "db3c7429556e72ebfd20d9bea261409553c39be24022776b35fa775b01f76d35"
      },
      "capture_reference": {
        "path": "qa/batch57-release-20261020/capture/references/cave-column.png",
        "sha256": "eb2f80ad46fed8a1031b114c899de6ab5d69e9a5017b7d6aead23de4892dcd70"
      }
    },
    {
      "id": "rusophycus-resting-excavation",
      "revision": "r001",
      "source_commit": "75f08656c73718ad707c0493e9bf8137f3efb45d",
      "review_commit": "adace4d7fd4cd091ab63f60ee4737f77096ba666",
      "metadata": {
        "path": "assets/additions/rusophycus-resting-excavation/batch57-20261020/release-metadata.json",
        "sha256": "cadae30a48833e1122b2a99ae82551636da342eb3db7d4d61748c57965d65510"
      },
      "candidate": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/candidate.json",
        "sha256": "42984064ae87a6653d3055226dc892dbe2aa3058f4c8b28c012bd9248de5f720"
      },
      "review": {
        "path": "qa/batch57-independent-20261020/disposition.md",
        "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c"
      },
      "original_metrics": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/metrics.json",
        "sha256": "69d1febcf204021c13cadd27b42624db4d62b232b0edb10f112e6b8094dce9ca"
      },
      "original_metadata": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/metadata.json",
        "sha256": "bad4d85d8aac7e92aa386bfdaa9b3096c9bda6ab4b92865d94b6e24c321791e9"
      },
      "frozen_brief": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/brief.json",
        "sha256": "ebc8ec5192edaa9749210f8ab36684d1e201d4ba8a2835ff1f13ae282dc4443b"
      },
      "proof": {
        "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/render-manifest.json",
        "sha256": "c1be5c618b16761ae3daf9342f43d667fdfce38cb6fb07c0e0a8035f46aa4cdc"
      },
      "capture_reference": {
        "path": "qa/batch57-release-20261020/capture/references/rusophycus-resting-excavation.png",
        "sha256": "48d14d0033de970b190e31381df9ca60d07db472f671019a66bb94799861ff45"
      }
    }
  ],
  "files": [
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/brief.json",
      "sha256": "c132a3202979454e721623ef3b7820843860062361e57d0fff7163f6f10f5c5e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/brief.md",
      "sha256": "846f2caf3d6c50570203520762c57474748c20d6fdb7572d08f71c1c6351c722",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/build-config.json",
      "sha256": "4adaa4fdcf3a98d1604b71b637d564fdd607d61fcd642d1e9f14917befa3e210",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/cave-column.blend",
      "sha256": "e182bae3a0c21ce7dc460c9b9d43282866cded66fd0a36a7cce3a4ac223f06b3",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/cave-column.glb",
      "sha256": "da454320cf9b4c890efae36418cf6b47600bc00b5cd0e77d89a5e5e85b394d0f",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/eight-views.png",
      "sha256": "799833da7d8964e6678f89c0f5a587ecce9df5b95bde2809ba63bfb7dc4b282d",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/generator.py",
      "sha256": "1cf74e29a99c19b8a258732eca4fe45dcd5911adb5f984ab0bc05042b0009fc6",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/gltf-validator.report.json",
      "sha256": "2447104436cd477f7331bc4781ccb79408a363c7104d08c76afddb81c98dc23e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/metadata.json",
      "sha256": "ea3734b5473c1fe7269e77c7ad03a6121e7542b8b351c5c9efebb0bfe7153924",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/modeling-freeze.json",
      "sha256": "acf41590316cf171cb7c83d4f10c16287d3b16b8bfcf033f0199b4256ad45e5a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/preview.png",
      "sha256": "c5b9c5930bca8157499bb478326afee415e59bdfbe4fe15c2dfbcb86138da159",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/clay.png",
      "sha256": "4b4bf10b3a315b31cebeebd9fac17b4ac5369d93366a7b18ee76faef7d1a0152",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/front.png",
      "sha256": "73522013853e21b4bf99aadff96c6bb076fad6fbd230d8b5a159636202498f4a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/hero.png",
      "sha256": "c5b9c5930bca8157499bb478326afee415e59bdfbe4fe15c2dfbcb86138da159",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/rear.png",
      "sha256": "7055bf49df1bebb69c655fe49a4e85a9cbe99d257a512cdf42f9406edb9a19ea",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/render-config.json",
      "sha256": "65c1502d6d5f95d26ed90f2373328159926c3a4c38417d8d854521421456cde8",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/render-manifest.json",
      "sha256": "75ea9a502217469a5301cb5e74c0c55b55bc946e9aa1d15bacbe4a23b94cb90a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/reversehero.png",
      "sha256": "79b18819a6ab834bb2b2e0ae3ca1b483b277798bbca2db985f1b9e539e0cbb23",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/side.png",
      "sha256": "0af58d1b7056d1831ad2690766a44d48c402f8d2135c67009d3004d9f9729808",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/silhouette.png",
      "sha256": "c9c85a9ae16980fc718c6134560f2d14fc1ca01371af95fd6b6429720243e8bf",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/top.png",
      "sha256": "59d00159cce8590ef73dbe4a03e5fdee8be42444883bbf1645dd9222cddb8d33",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/proof/turntable.json",
      "sha256": "622c7cf9dbbed4f772a98a5d16beba91cd4f64c537957da7c78f36975375f114",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/qa.json",
      "sha256": "589f6cd68b021fb827be9c77c2f0468510f5fe1bca95802ea0c32810b64ea28a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/rebuild-1.report.json",
      "sha256": "58cadf7c0b8a11a1a9fac2f6bc6d5c569b21ed020b3be75f14c231e364d69013",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/rebuild-bound-1.report.json",
      "sha256": "f16546a32929d60953aa69b353b9b94e7908dd57c66a0237443f1c285eab44f8",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/rebuild-bound-2.report.json",
      "sha256": "26133924fe522eac0dd1f7a32b90e002c3ef106d13615d6ec46a8f031a9d1b51",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/references.json",
      "sha256": "a272d86d265d636e6403ff31b6d657fd9392679e13bf2200869369ebc41eb3c5",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/runtime-parse.report.json",
      "sha256": "a97a4aa63c38645fcf19ac0932e72e7f205a58725fb64ea83527c973c3eac24f",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r001/source-export.report.json",
      "sha256": "29e70e991feb932f9fb5cfb5d7f4b1ee7cdf7fb0d39b8c03241884ee00ca6755",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/brief.delivery-v003.json",
      "sha256": "4906ccb2eeb9e2a9a8a5706e43d53b9ad92f20279275702dc020171c8e722c2e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/brief.json",
      "sha256": "717a796450a262f97e204e51926fdc69b0f4c23277d47162977f454030299a36",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/brief.md",
      "sha256": "8c335d3f9c5c32514c2148c57af6ff951648aa60f5b287ce20e4001dd2991678",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/build-config.json",
      "sha256": "8eac8a6d418f51a9c37624aaad023b06c7120d928837b8b560f9523cf1b737e5",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/candidate-validation.json",
      "sha256": "99b3b60c7c6077c1997d7ddca3c3de6809a6ef6a600ad7d39c45238dbe8e5330",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/candidate.json",
      "sha256": "1d6eb031640fa8de2c328fe1a4e8573c14329543c18c12e2cb2920723c905029",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/cave-column.blend",
      "sha256": "d5480f4750afaa5952513bd6ee2444a73685a865891f82aef6c8fd9ebb26d112",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/cave-column.glb",
      "sha256": "2659a158b5c3bf2a50b32057e58e6a28c42ed36827ed27f968918274fc48679a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/concept-evidence.json",
      "sha256": "559b22f4adf8377f0c36ed43e176d16754f3d29aec252876286dfb6d136ec814",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/concept-validation.json",
      "sha256": "394e2954af6e761c5d0b0a700e6eaef1972e6afbefb3debf9d096ca7d2954dab",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/delivery-freeze-v003.json",
      "sha256": "366d1a4e91e7850f64fa51273226f169c41a93259224dcbd4892aa93af7c8d41",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/delivery.json",
      "sha256": "ffa8df5dc6176c83962a96c3cee14fbe3b2c29f449a98a1a2d76ab6af669eeaa",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/eight-views-final.png",
      "sha256": "19974d13bb500adb8522bfb72dd3db04ac551c1bfb7339a18d72eb68a3261604",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/eight-views.png",
      "sha256": "19974d13bb500adb8522bfb72dd3db04ac551c1bfb7339a18d72eb68a3261604",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/generator.py",
      "sha256": "27d3bbfbf84c31a5dc2dd867350cf98a37f45a0cec53386ddf0e23805407562b",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/gltf-validator.report.json",
      "sha256": "193055fea82becb208bea524a51c7d92d5c2d430226c3b8e72f4c306e2dcd6f2",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/hashes.sha256",
      "sha256": "59c72748636dc2363c468a5fa1b1f17a8d0413fd83c5b3ffa1163afa4e1075b5",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/maker-review.md",
      "sha256": "2870bfaf35bd2b5bf5b256a4b1ebca0f2d8a038422f1ca93255f4605f2800869",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/metadata.json",
      "sha256": "e6a3001fe18df66e5b2a41bec92f980ca3076cfe17fe208f018c1f913b8f486a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/metrics.json",
      "sha256": "5b9db4f2922ab0360a8038a469c7f979a041f3a6efc27169b8601702452d76c5",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/modeling-freeze.json",
      "sha256": "f81883b76f7d041725fc5d6486ca4e36b959f9f24102adbb9a48ccc900e6c5cf",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/preview.png",
      "sha256": "7216316a8154ef115842fd8942e39ff4c70e99fdceb99fcd376942275df6e178",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/profile-contract.json",
      "sha256": "6d641e2d6ccc4034128246285fc9790569ff27252c34dcee85de1d9e13042a22",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/clay.png",
      "sha256": "eac987df8a36375478ce39566e2dc137f4537da3b9b425a8c1c3fae22e9483ef",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/front.png",
      "sha256": "d38f7e4af0cb0dde9c7d632bb1b8ef5300d30fc4ef571ea911ea77e74d4b8080",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/hero.png",
      "sha256": "7216316a8154ef115842fd8942e39ff4c70e99fdceb99fcd376942275df6e178",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/rear.png",
      "sha256": "7770901d114bd27a79e55483885f145b6e89557945b53c739f6aebd2693a3f8e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/render-config-static.json",
      "sha256": "912cce77cf22ed66848f4a429c3eeaab5a72a9d25f8e9d2ffd5474c5fc16816b",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/render-config.json",
      "sha256": "36ae5895ecbc0e0df0f57ad1e154edb567fc876c137c8f77ab804be21652f6f1",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/render-manifest-static.json",
      "sha256": "50e09c6dde22bfa0c4f6eb4d962a22530d8e868d2e555936a6c3a1aae0cb30c6",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/render-manifest.json",
      "sha256": "db3c7429556e72ebfd20d9bea261409553c39be24022776b35fa775b01f76d35",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/reversehero.png",
      "sha256": "efddaadd833f3e3b4f14cb31f422a0013fdba08d9adc68a7b7750748bf7979ac",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/side.png",
      "sha256": "f2ca47e9fed79c494641fd3f9f32f1883449ed1b03f289857d50b10b9ec8c81f",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/silhouette.png",
      "sha256": "c253350a21d4e0a99c00da9d5a493531239b9a747ffc8cb00f0a5318694d464b",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/top.png",
      "sha256": "2cf34ff6a74c13803c07630f8847d36eeb8b4e620887e667c72cea0adadf02f3",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/proof-final/turntable.json",
      "sha256": "489c146ac5d18a0ad65219a0a012018f60ae63bdf410cb1f0609505a61e99d3a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/qa.json",
      "sha256": "57c73ad92f85e89043ed645ba42b4fecf5e6518937c0c01799dcd0dc691c3784",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/rebuild-1.report.json",
      "sha256": "3bf6a043f0a40ccbba33e08a49aaf9b3736bd5eecec7ff0b121c5e9311129ee2",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/rebuild-2.report.json",
      "sha256": "f1001a63620c3b05b991a793cee1a8eb3ccdc4c5c627e71956bf753b497a19c2",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/references.json",
      "sha256": "a272d86d265d636e6403ff31b6d657fd9392679e13bf2200869369ebc41eb3c5",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/repair.md",
      "sha256": "1e5a281a90f9e64a75acf3e0fa5f2df626e651004b6be05304995d828acf2377",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/runtime-parse.report.json",
      "sha256": "db195af9f49705a14fbadcdb4d458fd3027e3897e2a56757b8362784f88120e6",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/runtime.report.json",
      "sha256": "62b2125aeaf4029440bb35b7ac717447316e90f421eaf861577150ad570a6086",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/source-export.report.json",
      "sha256": "077fd5bb29ee20be9738b9f920f1aaabecdf20fa90fa2af4d6447a5763a1f284",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/static-glb.report.json",
      "sha256": "125d3fac8b361d2c4f5c18125c65de48de6bd39c4567e6c242b1106ebd09237a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/cave-column/r002/technical.report.json",
      "sha256": "6ce139eeacae95769f55cd7ec909d56e75fddaa314faf270020ebc94db03f0b9",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/brief.json",
      "sha256": "4eede7b6ef47098b91f7f6d0810f06399483b18cbff8609ca05d8f7b18e61dae",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/brief.md",
      "sha256": "fb696f72b803c52ba545e8768d5b2890010ba8365ba17e46a1cecc529eeb12e2",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/build-config.json",
      "sha256": "f255489e12f3fc7bd4e5f4a9f68ae80a8a3edf784faf6917cf9aa79c47187e3d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/eight-views.png",
      "sha256": "e98ade8eec68b5cb3027b2c7f980556e2b7d4bc7d8737bded1d6c9e69af1f366",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/generator.py",
      "sha256": "1cf74e29a99c19b8a258732eca4fe45dcd5911adb5f984ab0bc05042b0009fc6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/gltf-validator.report.json",
      "sha256": "12bd0d2fa2ccb15004e258c777e49c61e8e57a018f70313accb64646c2a5652b",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/metadata.json",
      "sha256": "3ecf559c1afce4970cc25662b6678e37f060a141e3b7e63b4fb73ecfe8feaadb",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/modeling-freeze.json",
      "sha256": "771d73974d281f3b947d4e004548078f527a3013c79fdc74ff502c1cd6a7fc47",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/nidula-baltica.blend",
      "sha256": "928dda4cbf3db0efef09ebd327627c9ab63e9578d556c23c8abd0d9f4518acf7",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/nidula-baltica.glb",
      "sha256": "eb0a0f56b6147f6e222ee4e9fa8d9b19e083739f4718825e50e0d3cfca4908e0",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/preview.png",
      "sha256": "26ede7c69108099d847dd16e65e927012c4cf9c9e243ad94ea26ed8fbf3f8d16",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/clay.png",
      "sha256": "f2ac6cca9bb5ab51546fbd3c390f535d9ecb671abfc113864ca46bf2a262ff17",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/front.png",
      "sha256": "2d84d6e65852f355b36c4d9f2df8b5e2ad043b68a668d160e26d21c8f1a0a329",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/hero.png",
      "sha256": "26ede7c69108099d847dd16e65e927012c4cf9c9e243ad94ea26ed8fbf3f8d16",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/rear.png",
      "sha256": "49d1a9e25da61bbeca6d0235e857e153526225cfd75971cf18775a692126368e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/render-config.json",
      "sha256": "35b9bd9f4b1e17e23dc2ecb8f44beb942463e60e420a9dfe7457b0bde070953d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/render-manifest.json",
      "sha256": "b3faf62b6234df791cc9dc7387b138110a943ae46e296b4e9830422e84661782",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/reversehero.png",
      "sha256": "69c4b72c8f0d228e071819c681b23093d7b2aae829693264e6ddd9c62aacec22",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/side.png",
      "sha256": "6599fc896eac8e84be73e001eba1f19482a246a14a54a1978c3b5e6cddf04695",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/silhouette.png",
      "sha256": "690cfc94173ad0e3d535ce004f1203f00a4da113b8b35a98c34ecf23b64abb51",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/top.png",
      "sha256": "529a3e530980dd0fd0b4d6bc6cd2e1333471ee00e90e207ff40e3cad50f43100",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/proof/turntable.json",
      "sha256": "4c0b47096fbc5a6d502f767cd1a884a20e5c17d7cb3897f8a497cb81d91cf74a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/qa.json",
      "sha256": "5f632eb4a77514dd8143c6f45b1a0d2835729167938d0cc339c5fef4619c7994",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/rebuild-1.report.json",
      "sha256": "b6787c79fa407304646d988b74d0e0dea4ec9e0ed9a030fa38717419b0f0eb3f",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/rebuild-bound-1.report.json",
      "sha256": "a3b5be0e364fd57f34c80526fb5dccc0697694402898a9f574b8830bebed7129",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/rebuild-bound-2.report.json",
      "sha256": "79e6a4ee1598ddd79b8b9c3e2cecda15a00656cfcf1b53e857efb2149dcd8243",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/references.json",
      "sha256": "6a1d9853fc216210fef863389bc343864eaf420007ec88ac1c73fc21bd6c46da",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/runtime-parse.report.json",
      "sha256": "e491f4b92e519f4e6a7066a3972ff4239fa02b341035812117134c18cbe917d0",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r001/source-export.report.json",
      "sha256": "98d6a472a2741fb7d92273e64a4d90a475d018decffa4f4ecad301bf4dcc87dc",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/brief.delivery-v003.json",
      "sha256": "2117182270022f8528295e17a82d9ac170329c123fc44c74d90c0b26f5f39e70",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/brief.json",
      "sha256": "af06c9ca9926af5fca13e1df68f67653f3de963db2ec382203580af39f705eba",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/brief.md",
      "sha256": "fb696f72b803c52ba545e8768d5b2890010ba8365ba17e46a1cecc529eeb12e2",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/build-config.json",
      "sha256": "cc1a28d157a99a22be5fcd6bf4b581cba8ad9646abf63f70c6d133530c1b0b7d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/candidate-validation.json",
      "sha256": "2a2d6e5d259797f3b4a7ec5b03dfe75ab0c2229d61091afa85c7ffb5ba537163",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/candidate.json",
      "sha256": "a1271360b63ff115fbee160a3aff8de61e13dd40e21f4cf5aed721fa03655125",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/concept-evidence.json",
      "sha256": "62f1a72bd79d1c6029847bcddc29f849226091357b8b570dfcae3f05fc1ebdc2",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/concept-validation.json",
      "sha256": "30c87d26b2c33a998d579acce537ed9b7b58482ddeac7d752d8ffdc87ef0f9b2",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/delivery-freeze-v003.json",
      "sha256": "bd64a04921750a89d3c0bdea3e3783652d1803363212c15f98e956f8941c8759",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/delivery.json",
      "sha256": "2ff3a34bf3eaafd7bf6919167c6205e556baec17139720f2821fdfcb0d832016",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/eight-views-final.png",
      "sha256": "86f7b411a6c67a0fde9eb402bb6782e7033c7daab1f3da67c2ef819c33e5423f",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/eight-views.png",
      "sha256": "86f7b411a6c67a0fde9eb402bb6782e7033c7daab1f3da67c2ef819c33e5423f",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/generator.py",
      "sha256": "9e3c5fa21ab52aff134a5c235ae156b8db1b5e12fa50006af6fe3fc61ef424d5",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/gltf-validator.report.json",
      "sha256": "f2914a67ed2f47452435822f537d9a232249c22d3469172733d0e2c6c12bf52b",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/hashes.sha256",
      "sha256": "c1bbde77c72230e172f57d9c3b72ce4fd3cfc1c72c8b9538274ba9a880101552",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/maker-review.md",
      "sha256": "ff99fb4086cf75a110e054f9d6da1c5b23b4287653d0d1863e9ce1960bb059cd",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/metadata.json",
      "sha256": "9ab1fd871f3d205a0bbc3735bf1dba97767319dfc6d3dfdc1babd5af114b9d0d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/metrics.json",
      "sha256": "18d1d2f29fc0953a23a59c58dd245b92fb1d4cfc14806df6faea1a517093ef62",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/modeling-freeze.json",
      "sha256": "2051330545d0ca884c8bd2c753c47852c72b57ee2b5fda8b0b7c0c100ffe7c2a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/nidula-baltica.blend",
      "sha256": "ea67e24dac4adde47c02b2186713cffdcc4235d52b9a788e0615e9274fcaa9fe",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/nidula-baltica.glb",
      "sha256": "2de9c6a6ef69e3aab055add63797055bcd9174da0c7d92554b76ed697c3d2997",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/preview.png",
      "sha256": "061051abf978a8376adfb352db2a93c08c851105835373c87ef3a6ac51683b38",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/profile-contract.json",
      "sha256": "f4bbf879da0c4273914d17fd1270773de7d3f1630ae1f26d6ab0dee51aacad8c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/clay.png",
      "sha256": "b4053266cae28d90b69758583b40eaca239a4695ad9e95b29a018d77e8771395",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/front.png",
      "sha256": "52d7600547b0e1673d234303f5934f62f3028ddc2d11cf37ec05b896e1fd8f2d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/hero.png",
      "sha256": "061051abf978a8376adfb352db2a93c08c851105835373c87ef3a6ac51683b38",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/rear.png",
      "sha256": "388b86c556ccb113f892193c62ed901a4d5166551493ebd7d3509aaee0460590",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/render-config-static.json",
      "sha256": "10722d6ae17671c50149c3bcb2e881d729e4b99068df3f8db3b6168ab8d5e0c5",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/render-config.json",
      "sha256": "35b9bd9f4b1e17e23dc2ecb8f44beb942463e60e420a9dfe7457b0bde070953d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/render-manifest-static.json",
      "sha256": "48c8a687e8f60af54a5b0db71790013cb988e4481b73ae45ef92ff4c604468a6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/render-manifest.json",
      "sha256": "1e0206f27a7dff0426658fce2aa90ec3d6eed7c63809ae1295ea909434d82f70",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/reversehero.png",
      "sha256": "4f2f3d066bcf27c9639ff71db91b06b647e13c280ccb77989682ac58747b6705",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/side.png",
      "sha256": "6b0bb450911daa6ef08d0d731478bc5ccd116cdc19a8fc9bc6dfc19c30056872",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/silhouette.png",
      "sha256": "dabd0e1b0637fbe94035adedb83bae332b3a8eb445e12c01996dea23911aa2c1",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/top.png",
      "sha256": "cda957a2195e1a6a39ce9d025529d1bd11a468bce47d137fe6f19df2e988b86c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/proof-final/turntable.json",
      "sha256": "3d5e55c9e9f72e9527347ca78c5edac263b53792714e31e15aa3fbae4312a435",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/qa.json",
      "sha256": "e6c6368dc9b4709b315acf02132d3ef1e894901ea95b026ed2e927164e934879",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/rebuild-1.report.json",
      "sha256": "aea1d1bcd2afcffe016b4a864b235515788758a1c79524a97ade428bfb182b74",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/rebuild-2.report.json",
      "sha256": "d50ddbe8ca44d6c82e8b17cfb59bb94a7593569f4952191dc8b6586890c030f4",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/references.json",
      "sha256": "6a1d9853fc216210fef863389bc343864eaf420007ec88ac1c73fc21bd6c46da",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/repair.md",
      "sha256": "048a4ccef95f8a58962a44c0f82bc94948fc66efd1a840580d7d53fb6b6379ac",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/runtime-parse.report.json",
      "sha256": "03c7fc0b1a749e6d5a11f8952ae428204bb41ff4813532d555fa4bff96a12118",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/runtime.report.json",
      "sha256": "2429d834d5bf4433bbe5d9e5a349aef56dc037b07b49edf8465b0632b9e61d89",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/source-export.report.json",
      "sha256": "b54740cbe091cb3ce195685fdccc71ab18c2f722d34eaf832064fa3173aa403e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/static-glb.report.json",
      "sha256": "fd856361a1d9f9d570600df6f26fbf5649f65ac1b5363bf26bdf7de8aadcf1af",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/nidula-baltica/r002/technical.report.json",
      "sha256": "cd1cac43b7934d26463646b88de6de07e54d2bd083f11dfa944ca58b8cbd9371",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/brief.delivery-v003.json",
      "sha256": "44b42de0bc06c55a1211d310da0815597ecb338eab7c21de5c9aca041e5c90b8",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/brief.json",
      "sha256": "1d4c516bd4dbb5cd893615f785a35f5b5a7bcc894c8404e174a00cb39813a64f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/brief.md",
      "sha256": "59c7486e801adbb973efbf4cc50a101d184a13fe2f33c7ea339e0ab619a70b60",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/build-config.json",
      "sha256": "63bf35e3714cf14870aef54f97db9c3d644ab087da7a4496c65c86bae206c6e6",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/candidate-validation.json",
      "sha256": "1318751bd6b6f00853f00e125fd111c7e0454f4ae0f21c838d58375be952bcc9",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/candidate.json",
      "sha256": "ed9e058fd7a6736fdb8981cedcc7174de624d4e678aca1c12eb6b1330984b243",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/concept-evidence.json",
      "sha256": "2ad3b5edc6a3051fa79152391f33852a77cea5d2b5f57abf3ebcdb12a59cf646",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/concept-validation.json",
      "sha256": "b3776d6508ecddb76bd4386700b3256ca393bc62f91c44ea60f2a915bd9c1d48",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/delivery-freeze-v003.json",
      "sha256": "aa5b6674adb522a6a6cf5dc570c6e03b629c5e876728d687469f9f6ed54a44f8",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/delivery.json",
      "sha256": "3efce52f836fed94174c56dee20b3db5d159bcf49961f79be8755668a3c67f5a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/eight-views-final.png",
      "sha256": "7227e2ace6ac75baf2b1db130ce5fe8f3d9f64de6524ca62d99f46e19f1f1969",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/eight-views.png",
      "sha256": "7227e2ace6ac75baf2b1db130ce5fe8f3d9f64de6524ca62d99f46e19f1f1969",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/generator.py",
      "sha256": "1cf74e29a99c19b8a258732eca4fe45dcd5911adb5f984ab0bc05042b0009fc6",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/gltf-validator.report.json",
      "sha256": "1bdde68a81983e00a5f2a3c04ba46560c2285433f90b7d9369d9a2e919fd18b7",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/hashes.sha256",
      "sha256": "d8c5c93bee87f59c6f6a0aaf95088026bfc121fff808c2e5b9e972f74193b557",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/maker-review.md",
      "sha256": "d8059f311e88cd12931d9d745dcfc1ed04dddc72ea41e98450992246b9c52cfe",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/metadata.json",
      "sha256": "8bae0ca9793aa4ec006b84f88821498cd713786f85c1e0d748dca2894b62fa2f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/metrics.json",
      "sha256": "d699d1d13728f8273144290687a8bb9d68a7229a45269a72e55ca2983f3539ae",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/modeling-freeze.json",
      "sha256": "5dfc811a1288f1008feccee7510ac63a62b48069c272ceaf9a5f71152b3a165e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/preview-final.png",
      "sha256": "d37d074c19e8c32cd62b33c7d1ef3b431468826d059f6fa54ca7491797be7ee6",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/preview.png",
      "sha256": "4409b49b619284a8078e8a3972b6bc39610b414eff9315748d4b81bbdf293f4d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/profile-contract.json",
      "sha256": "2ef33984b04fee3f42a6c786462d1aa0baed2aa29fd1f3da145bfc3e6548f80d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/clay.png",
      "sha256": "dc353689bb7ffa3a4dd1c919cae76f644a551f55f258adfc29a70c8bfa5f072d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/front.png",
      "sha256": "b31f38914ed0d34e4a81b80ce9e2642fe9c0f4916702f29631981f1d8c6bd9d2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/hero.png",
      "sha256": "d37d074c19e8c32cd62b33c7d1ef3b431468826d059f6fa54ca7491797be7ee6",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/rear.png",
      "sha256": "9af3dbc9d19f91d3090fb860dba04ca86e11f17a3e4df580a9d1e5e6037023c2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/render-config-static.json",
      "sha256": "8fb567936d5b90e07a84fa6d0182b6a443dadfc9f19c8ee0e6a5cafd83f58e23",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/render-config.json",
      "sha256": "ba1a9a6ecc4f518575cd85f0d8324aa930300cb7c13a3f83eac770c7a570f8e4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/render-manifest-static.json",
      "sha256": "dc906c7efc95276d75d8f096fce4b663e33b03bc7eda7414b90cfc51b59d4b22",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/render-manifest.json",
      "sha256": "216a978aa1cd022ba3ae97d2648f306c2e179f996a8d7ca4bd6d6f72b8c56787",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/reversehero.png",
      "sha256": "80f1318c9ce07667b7f8f362531441ea13f7ee029a8bbe5a204d9c1b9649b90a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/side.png",
      "sha256": "536304330aed86be92a93690abdd9686498d18825d289c7dec13331e4f98aac2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/silhouette.png",
      "sha256": "25e21ff6f636e785655b2c507791974c9202f0c88b52f32f7b4f3fe91760217e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/top.png",
      "sha256": "4a16d5a98b07d2a8c97b8f9b8aec716bcf77b76df1d23dbab8821ae232eb6462",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof-final/turntable.json",
      "sha256": "2164ded60a443723f11347ab605f3dd8741c4d33a9a249473f5e518298302473",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/clay.png",
      "sha256": "ae949892322dde9c8747e5411d8d196a199e5cf46964fb87615a0a8e41ca447a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/front.png",
      "sha256": "3e373023c647369e3091c9f8b1eb110d19e2e365967bde625288e868d2d5b92a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/hero.png",
      "sha256": "4409b49b619284a8078e8a3972b6bc39610b414eff9315748d4b81bbdf293f4d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/rear.png",
      "sha256": "aecc649d7cfabbe34cdd2b51c07d8a9f8a13ce203ed8da5b9c5f8e2d11a6589b",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/render-config.json",
      "sha256": "ba1a9a6ecc4f518575cd85f0d8324aa930300cb7c13a3f83eac770c7a570f8e4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/render-manifest.json",
      "sha256": "04442b88c74af7f0b358115d0d16d26cc889da8d6e33d11674e8a5b614986b07",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/reversehero.png",
      "sha256": "287545f763b7570524f7d075049fac5fe1c9a43c0ad6af9ea7a63ba8e6c6e417",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/side.png",
      "sha256": "221dd11bbdffb2c2d8242a3807c7337cf1d18918be81cff9b6b9fdbf8063dd75",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/silhouette.png",
      "sha256": "4e4f2e0958332fa2d215a012252a2f67f54d31e1abea15c7fbaf1a44b04be846",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/top.png",
      "sha256": "d23ae2c71e3f9926746c5193056da9cb22790dcb68a8a1fa6bb63c0a2d117655",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/proof/turntable.json",
      "sha256": "2164ded60a443723f11347ab605f3dd8741c4d33a9a249473f5e518298302473",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/qa.json",
      "sha256": "d0acffd70330d065ad27dfa4d407e3ca371a3c012f1990310759ae4ced685fb6",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/quatsinoporites.blend",
      "sha256": "dfef75134471318068f60359f5ef0c9bb992bc9cdaeac113a3d92166d3927c8f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/quatsinoporites.glb",
      "sha256": "8d1dbd00dab4303b667d48048d5a8df737f07cb54d53a8173bb72fc025d622c2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/rebuild-1.report.json",
      "sha256": "c18120848ad27dc5a50d3d4628a662655413ab1088d527c1aa19870a166f7d97",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/rebuild-bound-1.report.json",
      "sha256": "8925218fc7b16effdf3c61defed2ab909b7f2dfa2476066352a73a3c6a36cb1d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/rebuild-bound-2.report.json",
      "sha256": "c7a561cff3cb3fc06a3423b78b48829ffa380ff9926dc43422aa32042fb0ad39",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/references.json",
      "sha256": "6eff915cec5a096b20fdd01166b710d69d674ab3aeb3cb083b4cff4b540ba63e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/runtime-parse.report.json",
      "sha256": "df0a658d117099ec5ab245c03f4b81806bfc2fa0117487687c4f891b633dfcfd",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/runtime.report.json",
      "sha256": "59ecef441d67407e7ef7aff034161213eeb8191807ffe557839f999370f683dd",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/source-export.report.json",
      "sha256": "57191628e9c421cfcd3edabe7b4e10acfbad6df732f64da63a2c31325f6655a7",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/static-glb.report.json",
      "sha256": "352dc687c24827a0edc21d5d0713c02179f25b41816befbf618c16460a1fe1cd",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r001/technical.report.json",
      "sha256": "90842c67fb04f6aaf323e248d2d69009616b3e3a411ed94c9b1c2144a12b7ecd",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/brief.json",
      "sha256": "87a349033b42cd2165f40ff40ba0e15f5aaf0c9b1e51c2335232dbc26302c2ac",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/brief.md",
      "sha256": "2a13296e8ad41384fe42ac45c5db9d059ffd8efd771f5bbcad536cc2adbcdeab",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/build-config.json",
      "sha256": "b3dfac8168ab5a856d337fbbd6f2c561a5f7945391e168f27361afeaa04eeca6",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/generator.py",
      "sha256": "6ce212e9ff3086ac285ed1a1848d588c6cc843bbcc4c264a4c50828704d0b8d2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/modeling-freeze.json",
      "sha256": "7a2efbfeb4001dda79e7e96204677f75600230bb17a0bb83f113b3c4de9e6ba1",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/references.json",
      "sha256": "6eff915cec5a096b20fdd01166b710d69d674ab3aeb3cb083b4cff4b540ba63e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r002/repair.md",
      "sha256": "4c23dcf4eb380c0c5400d5be12019a3d9a21c0d7cab5a6e422504cedae162d07",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/NOT-SELECTED.md",
      "sha256": "c56ad953bccd067d806344f634eb41ca32a042f0cbb3c77407b251febd3fcd2f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/brief.delivery-repair-v001.json",
      "sha256": "375353eb116df8d9ff84603da7b7b5341988248b5b3ef3bf8bd588265e041b0d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/brief.json",
      "sha256": "1d4c516bd4dbb5cd893615f785a35f5b5a7bcc894c8404e174a00cb39813a64f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/brief.md",
      "sha256": "59c7486e801adbb973efbf4cc50a101d184a13fe2f33c7ea339e0ab619a70b60",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/build-config.json",
      "sha256": "8bc5becf52629f5365fee2771681e1ff7dd5958a67c0f2079de95d50e436a3e9",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/build.log",
      "sha256": "ede8f2393438e2d18937b1c575cfb0f383b409d059ffd8a95100f301c24b534e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/candidate.json",
      "sha256": "82bc3df57dd8f0130e24919a3667661032ee7648bd8eadecc05f0b6b5e74d240",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/generator.py",
      "sha256": "838d615e58c69c5694bf6d4b999149191a270f329c60374e9ccce845100b8ccd",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/metadata.json",
      "sha256": "6a06762c1077dc7a3eede3bc125084b5cd31077ce431d756059fd96f94cfc0e4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/modeling-freeze.json",
      "sha256": "f8b5dec1cb3f55d6c91ed9498e3613c4d02b0a2cff9800c550f80895c2233291",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/prior-revision-concept-evidence.json",
      "sha256": "2ad3b5edc6a3051fa79152391f33852a77cea5d2b5f57abf3ebcdb12a59cf646",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/profile-contract.json",
      "sha256": "2ef33984b04fee3f42a6c786462d1aa0baed2aa29fd1f3da145bfc3e6548f80d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/clay.png",
      "sha256": "8bb357c2a3b2bd7502c3d41480f4e330f694f3c08c9a22606c051e705652cd2e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/front.png",
      "sha256": "c174b50dd54c01af6ee6550a5346a54eaa50b7ed7e3f118f3aff5e4946ed0015",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/hero.png",
      "sha256": "0f38136258e58c28f67f2d32a7f7dce850b9123159821168a36bf71f954f7de1",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/rear.png",
      "sha256": "955f30037a28b8aa8babad34a53aebf7b5e60e5629065630088c52fa22f63c8d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/render-config.json",
      "sha256": "50cbac2302dde9869929df7ce841a0d2be2867cc9f44f7b6b27d95fad68708ff",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/render-manifest.json",
      "sha256": "baf7296ecc922c86cf4ea42351e3c19ac38c29017c7d4f507609f10368d8fef4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/reversehero.png",
      "sha256": "5434c6a5a7b13b9c6dffe504b685d4cf7929b8bbb58cbfd8c9afa3fc7f3254e4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/side.png",
      "sha256": "10d75ffe0f9bae66fc52c793c8e7d77e5f77d90a962e944388302488959bb27a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/silhouette.png",
      "sha256": "253a70c1f733bf2f72eebd0a37204b5b6d98d488ab42352e7b174677ce87a5c4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/top.png",
      "sha256": "65e134746c1fb44147a780960fc6ebf0d1c52124deeb4c44820487256bda2fca",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/proof-final/turntable.json",
      "sha256": "694f649fea02971e184d8129e7b96fa46efdc609d8c4e8e82131d74b336d1417",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/qa.json",
      "sha256": "9b9d97381ffdbee63c770544d0bb5cf7c8d35d47dc326d1ec8ee59f377090bdc",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/quatsinoporites.blend",
      "sha256": "ae2973d73e907018f4840163979224bccd24a1111750b8a80120a489a3303452",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/quatsinoporites.glb",
      "sha256": "e2a3925bf698108c643b5ac3ab0a419d2b33e35576b014c46e06579c561de716",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuild-queue.json",
      "sha256": "bd1a0075dbaffe9c9be3c0b80956a493cf7977f40b630a60fd687c4f22edb0cd",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuild-queue.log",
      "sha256": "faf1398c7eb892334eed934d912cc59e63b1f08f577112a01dee468d62e84433",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-1/cc62ad310106d4d2b35c5aa8a6ce6da6b7a72c8dc08a027759db2b5ca56e887e/20261020T023212-5f224a6803ef40119380200943aefaa3/outputs/metadata.json",
      "sha256": "9637dd01efc2608eb60dc548d5a50298dbe48efef2cf05d1aeb1bcc9b683d885",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-1/cc62ad310106d4d2b35c5aa8a6ce6da6b7a72c8dc08a027759db2b5ca56e887e/20261020T023212-5f224a6803ef40119380200943aefaa3/outputs/qa.json",
      "sha256": "2334e59230d7d686008b839ed9285e091b38bb02a89d67a0bf34dc376c5d52e6",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-1/cc62ad310106d4d2b35c5aa8a6ce6da6b7a72c8dc08a027759db2b5ca56e887e/20261020T023212-5f224a6803ef40119380200943aefaa3/outputs/quatsinoporites.blend",
      "sha256": "7fef9262c81c7e8bf8ced643213b0c834c4a19d461ae0a5b82943913cd4b907f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-1/cc62ad310106d4d2b35c5aa8a6ce6da6b7a72c8dc08a027759db2b5ca56e887e/20261020T023212-5f224a6803ef40119380200943aefaa3/outputs/quatsinoporites.glb",
      "sha256": "e2a3925bf698108c643b5ac3ab0a419d2b33e35576b014c46e06579c561de716",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-1/cc62ad310106d4d2b35c5aa8a6ce6da6b7a72c8dc08a027759db2b5ca56e887e/20261020T023212-5f224a6803ef40119380200943aefaa3/request.json",
      "sha256": "f98e1761e16f0cbc66fdd433fa626e9cb6062495cf9eb0686f0c052de49c876a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-1/cc62ad310106d4d2b35c5aa8a6ce6da6b7a72c8dc08a027759db2b5ca56e887e/20261020T023212-5f224a6803ef40119380200943aefaa3/result.json",
      "sha256": "579b48c70b63d1e573640d09e2b464425183c890988712b56ca67e0e6041ac56",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-1/cc62ad310106d4d2b35c5aa8a6ce6da6b7a72c8dc08a027759db2b5ca56e887e/20261020T023212-5f224a6803ef40119380200943aefaa3/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-1/cc62ad310106d4d2b35c5aa8a6ce6da6b7a72c8dc08a027759db2b5ca56e887e/20261020T023212-5f224a6803ef40119380200943aefaa3/stdout.log",
      "sha256": "a1af41e27cffde993ffc8601187753b1c716a56b7c6fc92f8fdc10c321b52b1c",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-2/3ef305c92c920a3f08de0d5a9804bb966c8d98dd557e0318e476d3d209433ede/20261020T023215-617773a597b0412694ac2dd503eaab4d/outputs/metadata.json",
      "sha256": "530f5a8613e8741d06679cfaca6d0361bf73245734f0c9bae1a441036ea4448c",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-2/3ef305c92c920a3f08de0d5a9804bb966c8d98dd557e0318e476d3d209433ede/20261020T023215-617773a597b0412694ac2dd503eaab4d/outputs/qa.json",
      "sha256": "87d0b8b79c03de49a49103aa7b6df174ed30b6bbb7ca064a099d33b5346d675b",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-2/3ef305c92c920a3f08de0d5a9804bb966c8d98dd557e0318e476d3d209433ede/20261020T023215-617773a597b0412694ac2dd503eaab4d/outputs/quatsinoporites.blend",
      "sha256": "5633a3498f480487549f39d50ccfafef63f6764abbab2d6504397e7178def049",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-2/3ef305c92c920a3f08de0d5a9804bb966c8d98dd557e0318e476d3d209433ede/20261020T023215-617773a597b0412694ac2dd503eaab4d/outputs/quatsinoporites.glb",
      "sha256": "e2a3925bf698108c643b5ac3ab0a419d2b33e35576b014c46e06579c561de716",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-2/3ef305c92c920a3f08de0d5a9804bb966c8d98dd557e0318e476d3d209433ede/20261020T023215-617773a597b0412694ac2dd503eaab4d/request.json",
      "sha256": "6be0d71423bda0a06cbbbb678308b50ff12f57f85185d76cf016527e16f293e4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-2/3ef305c92c920a3f08de0d5a9804bb966c8d98dd557e0318e476d3d209433ede/20261020T023215-617773a597b0412694ac2dd503eaab4d/result.json",
      "sha256": "fc83297fdbf3b98e303aa363eff1b34125377831ab36cd44dbd8c9b1a9ddac21",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-2/3ef305c92c920a3f08de0d5a9804bb966c8d98dd557e0318e476d3d209433ede/20261020T023215-617773a597b0412694ac2dd503eaab4d/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/build/quatsinoporites/r003/repair-rebuild-2/3ef305c92c920a3f08de0d5a9804bb966c8d98dd557e0318e476d3d209433ede/20261020T023215-617773a597b0412694ac2dd503eaab4d/stdout.log",
      "sha256": "f1bc287785b7cfb92c34a5eca3c9cbd31482b011cd25d49a424d0b6789ac83ac",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/runs/20261020T023212-0be64519134f42ceb1d8989c6815c09c/manifest.json",
      "sha256": "7638a980047f6266783ca5208ceafc2c84d2faf3df4907219dd5d3a101b87f43",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/rebuilds/runs/20261020T023212-0be64519134f42ceb1d8989c6815c09c/summary.json",
      "sha256": "bb588e4fb52e6d7e78b43d2853f008d93de6a97ae8dacfda841e57ff417340fc",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/references.json",
      "sha256": "6eff915cec5a096b20fdd01166b710d69d674ab3aeb3cb083b4cff4b540ba63e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/render-fixed8.log",
      "sha256": "bd48a2d013a8de3ae14bc428ef9e43c4c77dfeb3ebc75416af22ba7e14972020",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/render.log",
      "sha256": "74cd08148cf6f9e07b37fde6af1993e403c781333ce184768850c1d32225c372",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r003/render_exact_glb.py",
      "sha256": "33ed7fc4b39a41e67f79e51d41fd4457f2a3087085837e59c8981d87e7bb412d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/HANDOFF.md",
      "sha256": "484c98e9923f41c4cbd5572a0285d071ebe87c8ddd73ac7577326fb99c8114bd",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/brief.delivery-repair-v001.json",
      "sha256": "58fa05006565ad237b76c78ceca72b61a69b2d3d5a955f4f2a7514d3de2485ef",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/brief.json",
      "sha256": "1d4c516bd4dbb5cd893615f785a35f5b5a7bcc894c8404e174a00cb39813a64f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/brief.md",
      "sha256": "59c7486e801adbb973efbf4cc50a101d184a13fe2f33c7ea339e0ab619a70b60",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/build-config.json",
      "sha256": "92d52fb7fcccba06b90bfa4f184d99de65df37f83b2ed42bc087fe6d807a3718",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/build.log",
      "sha256": "41f6126467bc8f92d064112101b0732369186efb30718cbd1dc040452a0b4026",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/candidate-validation.json",
      "sha256": "e6909fc0f7e9290ec2ab4b8dda612de14bd63dae900910fc2b24da94d1bb5989",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/candidate.json",
      "sha256": "701fba7892e74e3981c2a8c95cfed718a93999e928430037e4f28710eb7b87d8",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/check-execution-times.jsonl",
      "sha256": "bc355a0dc90b49e866796a92cff9f72ac99c14a85ebf6deb71c72e89edeb5762",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/count_vertices.py",
      "sha256": "ffa236a6af1d51329ca1c23e04da9a7c1ea4494d63661046ce015aa7c945c0f1",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/delivery-checksums.sha256",
      "sha256": "ab7a099183255b213436ede5e6fa18a3a673db5b2c8906d943819d2a5749a11c",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/eight-view-sheet.png",
      "sha256": "c2d58af2364c802b1618a0e4e6a12c7de9a8926fa7ddb7e5c9a5b6265b5e0fec",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/generator.py",
      "sha256": "aa7ac52a10064f7fea93efad779cebc00aa2431658e591c4023f85e8aa066cd2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/gltf-validator.report.json",
      "sha256": "82ce531e3896e35225d80eb38d3473f23f74a93560905ee6f4b62329c88b3b09",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/khronos.log",
      "sha256": "205e97f45d0cb654dd70132486f4977d22c3e23633bfdf539b2060c8adab15ad",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/metadata.json",
      "sha256": "74c532514e627e54c6b1126564b0215844c4ad8dc9814adbc8cb2749d35bbd20",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/modeling-freeze.json",
      "sha256": "48d69e59c9c91f58ee0b77b82ba63f39a40decc03320f9d427b12ff51d7ef8bf",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/original-byte-integrity.json",
      "sha256": "348cc2081f4359528d75d865669565e545693d210fdd32ea2e1deece75c995d7",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/preview.png",
      "sha256": "24bc44d8a1c321e5b8da268827bf992caaab90f64499de90769c1176e91cbcc7",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/profile-contract.json",
      "sha256": "dee137a3b4f47d41eec29f7a64b7ef76bde03fc0feb415b4d294dacfbd975221",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/clay.png",
      "sha256": "6a0ec26066095f6df3078ac4cde64d02555e6a95decff229728cd56408cd1da4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/front.png",
      "sha256": "0f02cb6835e0a72a0ff96853cc4a8424c915c3195ef4158a6237a3ef16782b0f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/hero.png",
      "sha256": "24bc44d8a1c321e5b8da268827bf992caaab90f64499de90769c1176e91cbcc7",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/rear.png",
      "sha256": "c3a8051c5df3aa99405b957530c03d29347d7a781c25ac72ef1f6eede1d06c73",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/render-config.json",
      "sha256": "50cbac2302dde9869929df7ce841a0d2be2867cc9f44f7b6b27d95fad68708ff",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/render-manifest.json",
      "sha256": "512629b76843cb7c49139e80e04350c543a1462182044bc33cba799f26ee8c36",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/reversehero.png",
      "sha256": "e318d5a134302516b498f78edd07cc3a73b14891e4281f87dcc0b4da5efb995d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/side.png",
      "sha256": "27154b2ca97cc7e4952d1e6f5b90e02a3b8a1318fffa1df1eaaeb3a83090f0a2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/silhouette.png",
      "sha256": "a65b26341d968f6f9912385fe3c364b86aa0fb4617b76e56efda231f441cb277",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/top.png",
      "sha256": "1793737a3df2defa06c43773004374c1c5098fca6a56aa8285003ee26faaca92",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/proof-final/turntable.json",
      "sha256": "d6fc73386750e1c732f87203c5c93479427697b9f8b1fa68f75150a533af9005",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/qa.json",
      "sha256": "dc0740ad860097601659b932cd3b0d1757a4a2b0ae946492aca0962e12dcf292",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/quatsinoporites.blend",
      "sha256": "558150cd76ec6e9ac581a42268d7e88d719676e26056f614a814a59b3a320e9e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/quatsinoporites.glb",
      "sha256": "22e3a5e8c35086c7931b25f9caa5198c5d533f379c8f080311e6bcd1b0b6ec4b",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuild-queue.json",
      "sha256": "e1b307f836795bf68ee01c775aa8d924897c082d2e72d85fd921d07ee2fc3113",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuild-queue.log",
      "sha256": "d187a5d9c4f27f42c137d11ede03c3b1c931a603c78c13f72cd6e282ff789fdb",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-1/8a61ba46d3fd86d019821fd4c1d6dcbc0d9e07e06026cbc3c68554ee5d10c0e6/20261020T023824-3d5f8bd50a0e4c34b34ed0e01ccec9dd/outputs/metadata.json",
      "sha256": "0ffac877f57a9e8f923113c03a3ccd263437d66e34e7676bd25b327b2d9e43a1",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-1/8a61ba46d3fd86d019821fd4c1d6dcbc0d9e07e06026cbc3c68554ee5d10c0e6/20261020T023824-3d5f8bd50a0e4c34b34ed0e01ccec9dd/outputs/qa.json",
      "sha256": "b000934641f448d644f456e10832ee8bd00a731c419110d89872cd0d2c0fe963",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-1/8a61ba46d3fd86d019821fd4c1d6dcbc0d9e07e06026cbc3c68554ee5d10c0e6/20261020T023824-3d5f8bd50a0e4c34b34ed0e01ccec9dd/outputs/quatsinoporites.blend",
      "sha256": "c9c9ff763b52dc173847958f51939756156b197ff08ba9277dcc8c54cbf7f301",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-1/8a61ba46d3fd86d019821fd4c1d6dcbc0d9e07e06026cbc3c68554ee5d10c0e6/20261020T023824-3d5f8bd50a0e4c34b34ed0e01ccec9dd/outputs/quatsinoporites.glb",
      "sha256": "22e3a5e8c35086c7931b25f9caa5198c5d533f379c8f080311e6bcd1b0b6ec4b",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-1/8a61ba46d3fd86d019821fd4c1d6dcbc0d9e07e06026cbc3c68554ee5d10c0e6/20261020T023824-3d5f8bd50a0e4c34b34ed0e01ccec9dd/request.json",
      "sha256": "fdec12cb8845b5bac59df53b4b9cfa7e5ff01da2429e68f22e8c8f6637cd5518",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-1/8a61ba46d3fd86d019821fd4c1d6dcbc0d9e07e06026cbc3c68554ee5d10c0e6/20261020T023824-3d5f8bd50a0e4c34b34ed0e01ccec9dd/result.json",
      "sha256": "0d5908e0f90e096ecc29d2744e5a7ae10e742b047e7d625d24a54b4016f746b5",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-1/8a61ba46d3fd86d019821fd4c1d6dcbc0d9e07e06026cbc3c68554ee5d10c0e6/20261020T023824-3d5f8bd50a0e4c34b34ed0e01ccec9dd/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-1/8a61ba46d3fd86d019821fd4c1d6dcbc0d9e07e06026cbc3c68554ee5d10c0e6/20261020T023824-3d5f8bd50a0e4c34b34ed0e01ccec9dd/stdout.log",
      "sha256": "6948dcbf7b05c6e35ca9798ec7afc3869645212a731131113b1e2431919a4510",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-2/60869732084076e20a6ba9fb7556d2f223c668393036b860ac84e3659577ae51/20261020T023828-98edcad18aa246b1b4f123c1bb2eb176/outputs/metadata.json",
      "sha256": "87964e2c92bf2be130ea3e9ab079c9bbee670e50aa550ded66546a4b78fb34f9",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-2/60869732084076e20a6ba9fb7556d2f223c668393036b860ac84e3659577ae51/20261020T023828-98edcad18aa246b1b4f123c1bb2eb176/outputs/qa.json",
      "sha256": "e99d7711578ac0b4e600fc317e8cb7944f9d6839b5794a4bfa22099053c88d72",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-2/60869732084076e20a6ba9fb7556d2f223c668393036b860ac84e3659577ae51/20261020T023828-98edcad18aa246b1b4f123c1bb2eb176/outputs/quatsinoporites.blend",
      "sha256": "e4914af7106fc0e9ce6acef8dffafd7a130cba2c431ffa2aa298ee840fddffdf",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-2/60869732084076e20a6ba9fb7556d2f223c668393036b860ac84e3659577ae51/20261020T023828-98edcad18aa246b1b4f123c1bb2eb176/outputs/quatsinoporites.glb",
      "sha256": "22e3a5e8c35086c7931b25f9caa5198c5d533f379c8f080311e6bcd1b0b6ec4b",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-2/60869732084076e20a6ba9fb7556d2f223c668393036b860ac84e3659577ae51/20261020T023828-98edcad18aa246b1b4f123c1bb2eb176/request.json",
      "sha256": "8e4e14cfdebfaeed2e977a2e20e3ebb5d43891409561ff2248fc72207bda37d8",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-2/60869732084076e20a6ba9fb7556d2f223c668393036b860ac84e3659577ae51/20261020T023828-98edcad18aa246b1b4f123c1bb2eb176/result.json",
      "sha256": "e5d6fbe049c40944a6bb25f1a23bc030e3b895535e4790b67f89a88067f26fc0",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-2/60869732084076e20a6ba9fb7556d2f223c668393036b860ac84e3659577ae51/20261020T023828-98edcad18aa246b1b4f123c1bb2eb176/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/build/quatsinoporites/r004/repair-rebuild-2/60869732084076e20a6ba9fb7556d2f223c668393036b860ac84e3659577ae51/20261020T023828-98edcad18aa246b1b4f123c1bb2eb176/stdout.log",
      "sha256": "35c6795c99d92ea83b91f5b0e8b7c532ce9f5a8cc31aed3b8fdf23caa5001d06",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/runs/20261020T023824-e148362a4d9c41b68a0273c6d82f6053/manifest.json",
      "sha256": "d56af4327d79678d6272846574de9ef3a421eec18398ed676637a116a41346d3",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/rebuilds/runs/20261020T023824-e148362a4d9c41b68a0273c6d82f6053/summary.json",
      "sha256": "16f7c8b4641c159c84733eec3d262aa9b6891d099ad8a34796b063791ac89833",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/references.json",
      "sha256": "6eff915cec5a096b20fdd01166b710d69d674ab3aeb3cb083b4cff4b540ba63e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/render-complete.log",
      "sha256": "df430573a125336ace24d2d3de3d64700a9086cf018e24c27a82beae76a61370",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/render_exact_glb.py",
      "sha256": "33ed7fc4b39a41e67f79e51d41fd4457f2a3087085837e59c8981d87e7bb412d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/repair-handoff.json",
      "sha256": "09b94e8aa8021ff766fbc1d454583c701dfcd0fe27cf12c2ea2432927783a225",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/repro-1.log",
      "sha256": "2291b5a9b24c5dbd2e096d51a12bcf87b3148c82dfc0d958a2e4fe5810940d1d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/repro-2.log",
      "sha256": "6ad84ab42a39e954201bb738634502f44a27d041af008640e7171d044450e716",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/repro-bound-1.report.json",
      "sha256": "2291b5a9b24c5dbd2e096d51a12bcf87b3148c82dfc0d958a2e4fe5810940d1d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/repro-bound-2.report.json",
      "sha256": "6ad84ab42a39e954201bb738634502f44a27d041af008640e7171d044450e716",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/runtime-parse.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/runtime-parse.mjs",
      "sha256": "9fa56f59dddeff5bf8fe86de0d0ff6627421d263fc59011a2424a03ed229418d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/runtime-parse.report.json",
      "sha256": "dbcaf8780cd8fdd7d4ce01301c72062e8e173ae7fa9fffcbc08f5ee737da7b24",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/source-export.report.json",
      "sha256": "baea00946792bc59bc3396933ba8dde3a03a939fce7134e12a72675e5ed5f0c4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/source-reopen.log",
      "sha256": "fba06d59350700a7a8e27dc81105f25f07f29f84a538984bab28e8999fc554b8",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/static-glb.report.json",
      "sha256": "77482ab20efaf87748bcac9e50048366fc7c86efe38b28cf4d70469f6ec98ce1",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/static.log",
      "sha256": "77482ab20efaf87748bcac9e50048366fc7c86efe38b28cf4d70469f6ec98ce1",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/vertex-counts.log",
      "sha256": "a81048c07b41b2fd86968ee7345eb7a78f18bc38e33510a722a7df7d87a61ea8",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/vertex-counts.report.json",
      "sha256": "47cbe2241a724c4d573bea982c59abedb5d49dbf74ab87acc59f314681420786",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/brief.delivery-v003.json",
      "sha256": "c6b5ff7cb9e8c8628433ba47cb71fcff233b9b6fa48626018f80f620a5a491ce",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/brief.json",
      "sha256": "ebc8ec5192edaa9749210f8ab36684d1e201d4ba8a2835ff1f13ae282dc4443b",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/brief.md",
      "sha256": "5f9ede4e3c1ae1ac9d4d09ad15083da41d6fa941d3b4406357bf4228c539a735",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/build-config.json",
      "sha256": "b6e2161f48cbc52e978c2b44970c68e31b3e727d50bf739c8f17d567c461e46e",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/candidate-validation.json",
      "sha256": "f6ce774496c956472a9e027a4046aea2230bc40143a83d5f6b7a8ca1d697d314",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/candidate.json",
      "sha256": "42984064ae87a6653d3055226dc892dbe2aa3058f4c8b28c012bd9248de5f720",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/concept-evidence.json",
      "sha256": "c14b640bf3896705810a53481f19a5dcd743fd892bc5b4ad989bc50d44a5e994",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/concept-validation.json",
      "sha256": "61ee84e4eeb5d3700f09d26de3ef13550d3771d221df5ec6ea31c5642a2a7686",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/delivery-freeze-v003.json",
      "sha256": "7c448029e1804d7180c94c7b59194b90e0337050e8ca6b2c36ebb594a3265a68",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/delivery.json",
      "sha256": "167ace13ef2db5e7920ed2f2770aa21784c24cdc4b44a294b3cde71fb73cc577",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/eight-views-final.png",
      "sha256": "3b2aa3195a0fce7693f2a080aa9b71fc3936d97afcfa85861269cd29ba6b6584",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/eight-views.png",
      "sha256": "3b2aa3195a0fce7693f2a080aa9b71fc3936d97afcfa85861269cd29ba6b6584",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/generator.py",
      "sha256": "1cf74e29a99c19b8a258732eca4fe45dcd5911adb5f984ab0bc05042b0009fc6",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/gltf-validator.report.json",
      "sha256": "c475121e5c3184cfa8df79276d14e262efbc9af289d8240e521a79440751f3c9",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/hashes.sha256",
      "sha256": "7afe11af8cd25d99cd82747570776b3577768044e384655e570cc0b3a3ebbcda",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/maker-review.md",
      "sha256": "f7b6ef1811532f6477983ba6d7c9a814c3ab2b95a529af3e9fe1e6b4a78056cb",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/metadata.json",
      "sha256": "bad4d85d8aac7e92aa386bfdaa9b3096c9bda6ab4b92865d94b6e24c321791e9",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/metrics.json",
      "sha256": "69d1febcf204021c13cadd27b42624db4d62b232b0edb10f112e6b8094dce9ca",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/modeling-freeze.json",
      "sha256": "df0ef41d7689b3f2b9e85f1a610e4e8d7900e23896bfee0e2bdf3b1d249ff47d",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/preview-final.png",
      "sha256": "9f6b6b5f33d2c383634c68a60337339ea0f9e7f446f0dff68566327bc2773aee",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/preview.png",
      "sha256": "dec503d5805d0d00613ad7201998beadc9ae4099f3a02879c7ef8bfaa1ca262d",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/profile-contract.json",
      "sha256": "64e4afd40530842f75e76699aee9fe24d431ef348af295114820113073d6c078",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/clay.png",
      "sha256": "03be63cd4c711a4092f5968025a0562dd63c6e9f85264481bf633060071fc5e9",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/front.png",
      "sha256": "a55a8acde9388469ee62d38d1d81be2dcd2b60b42850be1aaa5d569e7fc35722",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/hero.png",
      "sha256": "9f6b6b5f33d2c383634c68a60337339ea0f9e7f446f0dff68566327bc2773aee",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/rear.png",
      "sha256": "09e43b8ec368f20d13a6d17697d6f65495c0178b555d0fdea13f38262d914613",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/render-config-static.json",
      "sha256": "9c0a0c66c5bb8e0c604fa32179b2bbfcca1b4ced2b70d51bd2c414b58b6bb2fd",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/render-config.json",
      "sha256": "f24ed0e24c92c173578890af0e9e1b2bdbf0aaa03f69dbee6b58932c3b118a85",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/render-manifest-static.json",
      "sha256": "b30fea8f6714bf65701e56495a5dde09436f0fafd18423879db1e97fca42aca0",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/render-manifest.json",
      "sha256": "c1be5c618b16761ae3daf9342f43d667fdfce38cb6fb07c0e0a8035f46aa4cdc",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/reversehero.png",
      "sha256": "8169b919db682c0963503f028c2a81974f6da97cd3122d1471168b0ca61e633a",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/side.png",
      "sha256": "c79c06206a1a8aa1d579459e55e6395bc194431c075907e04bbfacc240a2d4c5",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/silhouette.png",
      "sha256": "7b96ea6e82ddfae4a7d27695938a3086610910c3967de135f7345557f54cc351",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/top.png",
      "sha256": "b39ff311981030ecde218ac9f95fb89c3527b63d9388472827c1c33d4d349e55",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof-final/turntable.json",
      "sha256": "a4e616ccfc32cc01fc45800d4610c71260373be768589b89cb58a23c914110a1",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/clay.png",
      "sha256": "9f5502fff2b84baff3b6cf34fc1f5c4ef5838036bcb65c47747535200d85cd5e",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/front.png",
      "sha256": "5c4006fb963eb8c2ccfd92a81372e1a82134858041bfde7b6b2d2c712a4b8aa0",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/hero.png",
      "sha256": "dec503d5805d0d00613ad7201998beadc9ae4099f3a02879c7ef8bfaa1ca262d",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/rear.png",
      "sha256": "2e55f76f60787d890d47ec20aa9ebb6acef6d9f566f0bb8679280c5f22d89b9b",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/render-config.json",
      "sha256": "f24ed0e24c92c173578890af0e9e1b2bdbf0aaa03f69dbee6b58932c3b118a85",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/render-manifest.json",
      "sha256": "334cdd50b7236349f72d484bb54c8e53332c4d8f6d7f71e08df3d4b397cc26ff",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/reversehero.png",
      "sha256": "6da7d6fa14fe3c2a67f962889c5d3a64b9728a3a987fdc1b48e6a47660635cf0",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/side.png",
      "sha256": "d48657a9434c9babd2b2ad87c6f95115ff16418185bcec1e37d9b31694996bd2",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/silhouette.png",
      "sha256": "b6fc29f6672b282041c26d7fcbf850327b49c68cd55cfe6d06b2604418ee27fe",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/top.png",
      "sha256": "9bc191fda08f7c523b1982685740247449b5edb4d75684e2a2f5ed065f73f8d9",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/proof/turntable.json",
      "sha256": "a4e616ccfc32cc01fc45800d4610c71260373be768589b89cb58a23c914110a1",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/qa.json",
      "sha256": "62ba6247b38acec16fb842de35fe534e8094f19ad560df60b57969ef886591b3",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/rebuild-1.report.json",
      "sha256": "7b7aced37bd9fda8cb70aefbe15b939bf34bd0840d878c953f3db28db0763c2a",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/rebuild-bound-1.report.json",
      "sha256": "098405e5ff59c31c7e98247aacbbf543b320261e4231c1512c966cc4310d9bf2",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/rebuild-bound-2.report.json",
      "sha256": "904c10e943d203344b620ee2ef2feceb99b5f3939ac2f40c14ff4f653aae4e4a",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/references.json",
      "sha256": "6126d2fb2889fc2944111dcf698d3cf2de6634fe5ad2e0ff3d81dbe9de7b95b3",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/runtime-parse.report.json",
      "sha256": "a9e1aac86a1be455560dbdf787c994f40653421819e0758086acffe0c4796c97",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/runtime.report.json",
      "sha256": "f727cc5242b8f26e86100b8727861415e247d2604bbaa8cfb13c97152fc7eafb",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/rusophycus-resting-excavation.blend",
      "sha256": "38449be768534e005e337bf38fea0a3757ec59a979e321ae7f6a58c67b64ace8",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/rusophycus-resting-excavation.glb",
      "sha256": "7493f6df58164496ae64161395138520787fa2be9a9eb0f2363c56ef4f276751",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/source-export.report.json",
      "sha256": "691e1182958f6072b54a541b68617c1035660a050e0c8fa73f7d568334ce8e92",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/static-glb.report.json",
      "sha256": "a1fe90477a16409f62127c776657ea2ee2726d012172c580f5307ba6c7733599",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r001/technical.report.json",
      "sha256": "d4f004d9ab1c83a43d70171c8d8fb9648b584b11af870054eb4b0f19aa58ca5b",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/brief.json",
      "sha256": "68b465efddf7460ff0016f3e79296c83207b66011e1a7079712d27a98130dbe6",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/brief.md",
      "sha256": "fa26aca2ad1505cb0b64a246515a6bd56f18700c9c8179d42ea575c16bed2b0c",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/build-config.json",
      "sha256": "46ade2d0909405af733e8207d444ef899e384e92212814249a82732028aac0d8",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/generator.py",
      "sha256": "28ea4e8650d82fcadd6094de6eba5254bcf5fab8f408eb297af8839733cba10c",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/modeling-freeze.json",
      "sha256": "8a7697276d76b30ca973246dc286c79864a94311e2096e0944ccab9aed996f89",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/references.json",
      "sha256": "6126d2fb2889fc2944111dcf698d3cf2de6634fe5ad2e0ff3d81dbe9de7b95b3",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "assets/candidates/continuous-small-life-round21-20261020/batch-57/rusophycus-resting-excavation/r002/repair.md",
      "sha256": "f82efce65e4dafbce5133dc7c7d4dada3f5069f1fbd81af650d800e2fc2f75c1",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/HANDOFF.md",
      "sha256": "781b5e096c4510587e9da11c5d1e0641c64bbedae35088311abde26c10295b8d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/baseline-delivery.log",
      "sha256": "941cf7a4bedf84bf0cf15d3565564e5b3e39a499310008f529b3b181c716ebe6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/blocker.json",
      "sha256": "da4adcafad6910724de0657f632d9fc43d43b32484ffd5a4d6a43a86f9d8f1b5",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/build.log",
      "sha256": "01228dfce8e210caa0c75990e92a172f380c47aba351bfdd47c83972a6b51946",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/build.log.json",
      "sha256": "56dcff8a2b9c00126ac6af0f3e385ca0d37008774777796bb54abf0750f8eca7",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/khronos-retry.log",
      "sha256": "8336e2b9c922267a53f33211786b960c14446fa2d50d4d25a0e182b957fd17c8",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/khronos-retry.log.json",
      "sha256": "f8de005147b42687ab097ea07abe3b857dfbad984015bf1e228af12f2782a9c4",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/khronos.log",
      "sha256": "364fe956b845fc977057bc1086492fe45e46e70664b96d1195105336cb82acac",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/khronos.log.json",
      "sha256": "46ad9500960512f3e3a932238da90b814daba87d2db938e546b2c8755f77ae5f",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/modeling-start.json",
      "sha256": "93ce5682b708c87ad95cb493db889c04d49820d9cc0f6ecafdd81baf53580da7",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/rebuild-1.log",
      "sha256": "c1b0581f59efb81ac29a26a560d4aa3d129b6a2e49ee001a3db97aabd5402d06",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/rebuild-1.log.json",
      "sha256": "5679f3439de848d3401be43948989f5fe1ef16575b3703287d0792680fcb73c8",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/rebuild-1/cave-column.blend",
      "sha256": "cd2e8bed8811a92a7f986f8f067113ccc1e526ebea33e155eff8c9273bb0e1a9",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/rebuild-1/cave-column.glb",
      "sha256": "da454320cf9b4c890efae36418cf6b47600bc00b5cd0e77d89a5e5e85b394d0f",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/rebuild-1/metadata.json",
      "sha256": "08fbfd88590258d4884d60e30a5db9b2881015740c5658e50b4a11deaad206c8",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/rebuild-1/qa.json",
      "sha256": "e78f176af6683dc4c8b6e7d4b11eb9067b03fbb143a52ca7c2137984fe66804c",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/rebuild-compare-1.log",
      "sha256": "58cadf7c0b8a11a1a9fac2f6bc6d5c569b21ed020b3be75f14c231e364d69013",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/rebuild-compare-1.log.json",
      "sha256": "c62b21b7e757e68d751ea1e3c96dbd866964118e735aa14c6ec833a4147d9d1e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/render.log",
      "sha256": "dabbe7274304f90265f6cbd97b16bfb89da291f9e992f4b72c3daccbc7cfb2c6",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/render.log.json",
      "sha256": "b63efb53a0c5ebb4852394ccdd1df4678565334dbf8b71c96c39371c81fd8569",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/source-reopen.log",
      "sha256": "40144212ee18e30c6defa3de81cc05b2198dea4010953d9094b67a58155ae9a4",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r001/source-reopen.log.json",
      "sha256": "136e009b3cbecae27087a97dbcbceb305c8299aaf08424b5986a40327ea127de",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/khronos.log",
      "sha256": "a8c868f9c41363b99f230ea29eda954f14ccfa4358d2d315eb99852549c8d09e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/khronos.log.json",
      "sha256": "0e3f968ee3584d483eab82511c519939e28bc155e256a374341e0383e8ca78e9",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/rebuild-1.log",
      "sha256": "3bf6a043f0a40ccbba33e08a49aaf9b3736bd5eecec7ff0b121c5e9311129ee2",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/rebuild-1.log.json",
      "sha256": "7b5ad3ea0f4ccfa10658959e5517de86d6b7618c6d581e19c6991213745ae6b6",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/rebuild-2.log",
      "sha256": "f1001a63620c3b05b991a793cee1a8eb3ccdc4c5c627e71956bf753b497a19c2",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/rebuild-2.log.json",
      "sha256": "0e28e9ef206e2ee7db85ccc9b3430fa86558bf172ba766d7bfd7d83f8e5f2aed",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/render.log",
      "sha256": "58e51b795a35d91ac7bf3de3b01317f42012ac0467d356c7517253b03c470df2",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/render.log.json",
      "sha256": "c9c101b19b8c6830ed05343e3ab68598e6bafebf7842fa72f139bf5bf74b908c",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/runtime-parse.log",
      "sha256": "23552f52e064feff5705bf38f6db1f5022a34c70937c672e62b2263196ef1223",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/runtime-parse.log.json",
      "sha256": "33ae5e41e43cc68619cf73d270d742d3724268c976a8a4d82a4dd9b3daf9b4a0",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/source-reopen.log",
      "sha256": "d97ed834b83e96cba6b39d1de2f22abd84346ba5f6caacb5e3616dcf8da8f1a0",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/cave-column/r002/source-reopen.log.json",
      "sha256": "1b030f2bca8f47667fbebc538c9497dd903914909f3769a4ffc811c59e413118",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/claim.json",
      "sha256": "6fd7ed4afa7545a72ccdad1cdcbd210cbdd3563d3ff2d8a87d41faf89d604a5d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/claim.source.json",
      "sha256": "79d405eda84fd49643a7cac361e2f7a26ee7dee55e887671bc29f288a7616274",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/concepts/generation-record.json",
      "sha256": "6aeb1494ede2100bde02f31e98f1f12ba4918a2b0799e342585337407a858a59",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/concepts/inspection.json",
      "sha256": "10afea004a7acfeedfc2750e355cf5621810cb7a55442b0d5dc013b6a778348e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/concepts/original.png",
      "sha256": "5d6f216cf02b3028d1543365ccedac024410b67e26105544933a42d17f81140a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/concepts/prompt.txt",
      "sha256": "67f773fe3d2eed1fc06b27d45343fb3bc6f80d739301cfeac90950870bc3ee18",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/dependency-install-initial.log",
      "sha256": "f6afb34fe072a530b7e5f84b41ec4ae0a68b069002434de5483f6c9a8f621842",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/dependency-install-tmp-cache.log",
      "sha256": "f1861bbbeeefb2c8142b88c5f32807effe0c627726426d9e2565a726476f0159",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-queue.json",
      "sha256": "b4db608eccfcfe3b248c8024e807bb70c81b190249fc7a1be42ab3851b6bb823",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-queue.log",
      "sha256": "f47899a60f122de84ca28c3e9870b3e298e61a0cdff4c8cab93fd552d70f00f3",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-0/2ddaa2a3bf862be0dbc3a9921f115c87da5607c4db490494d81c6a07c32e9190/20261020T020901-5cf77bd7fb1a4485a411d33db50ba104/outputs/cave-column.blend",
      "sha256": "d5480f4750afaa5952513bd6ee2444a73685a865891f82aef6c8fd9ebb26d112",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-0/2ddaa2a3bf862be0dbc3a9921f115c87da5607c4db490494d81c6a07c32e9190/20261020T020901-5cf77bd7fb1a4485a411d33db50ba104/outputs/cave-column.glb",
      "sha256": "2659a158b5c3bf2a50b32057e58e6a28c42ed36827ed27f968918274fc48679a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-0/2ddaa2a3bf862be0dbc3a9921f115c87da5607c4db490494d81c6a07c32e9190/20261020T020901-5cf77bd7fb1a4485a411d33db50ba104/outputs/metadata.json",
      "sha256": "e6a3001fe18df66e5b2a41bec92f980ca3076cfe17fe208f018c1f913b8f486a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-0/2ddaa2a3bf862be0dbc3a9921f115c87da5607c4db490494d81c6a07c32e9190/20261020T020901-5cf77bd7fb1a4485a411d33db50ba104/outputs/qa.json",
      "sha256": "9f5f69414ccc1fb7057c3f6341f647428055e3889c891d06636479660b98495d",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-0/2ddaa2a3bf862be0dbc3a9921f115c87da5607c4db490494d81c6a07c32e9190/20261020T020901-5cf77bd7fb1a4485a411d33db50ba104/request.json",
      "sha256": "d52a6a22ca324e86ea7771bdb94f046a29c9e3969566e64e6333f3d327f8656a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-0/2ddaa2a3bf862be0dbc3a9921f115c87da5607c4db490494d81c6a07c32e9190/20261020T020901-5cf77bd7fb1a4485a411d33db50ba104/result.json",
      "sha256": "fed87c24155bdcac9a9ee6a7f45f8894f4f70fe0ff74c8a81ff20835d09563c8",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-0/2ddaa2a3bf862be0dbc3a9921f115c87da5607c4db490494d81c6a07c32e9190/20261020T020901-5cf77bd7fb1a4485a411d33db50ba104/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-0/2ddaa2a3bf862be0dbc3a9921f115c87da5607c4db490494d81c6a07c32e9190/20261020T020901-5cf77bd7fb1a4485a411d33db50ba104/stdout.log",
      "sha256": "fb9b47cdbda591a023af53e3e93c521a673b6c43c9bd68ee8bb8337af9c9fe97",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-1/39f94e446c613ebd32ccbcf29b2886cae7bb6d84adb1d5a16d372be43fdb868d/20261020T020902-a48416e0916a4c719b9af4d8c153deef/outputs/cave-column.blend",
      "sha256": "f3b2b81d53fd7502402e38af1553f3bd45a4196cff2f058b858c6fc1e1232c2e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-1/39f94e446c613ebd32ccbcf29b2886cae7bb6d84adb1d5a16d372be43fdb868d/20261020T020902-a48416e0916a4c719b9af4d8c153deef/outputs/cave-column.glb",
      "sha256": "2659a158b5c3bf2a50b32057e58e6a28c42ed36827ed27f968918274fc48679a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-1/39f94e446c613ebd32ccbcf29b2886cae7bb6d84adb1d5a16d372be43fdb868d/20261020T020902-a48416e0916a4c719b9af4d8c153deef/outputs/metadata.json",
      "sha256": "8067471b33bfec9af08bc2d6b2c66dd8c946c4f530c396fd0f0fee90d808e35e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-1/39f94e446c613ebd32ccbcf29b2886cae7bb6d84adb1d5a16d372be43fdb868d/20261020T020902-a48416e0916a4c719b9af4d8c153deef/outputs/qa.json",
      "sha256": "1599f2e6679230f02b461dd50ed3c58940bdbb993e5ffa326b5a3ba7898c171b",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-1/39f94e446c613ebd32ccbcf29b2886cae7bb6d84adb1d5a16d372be43fdb868d/20261020T020902-a48416e0916a4c719b9af4d8c153deef/request.json",
      "sha256": "abd2810fdb57e2f3522868b8e236e632aa979c336f8b3a25a1127d0b1bcfc90e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-1/39f94e446c613ebd32ccbcf29b2886cae7bb6d84adb1d5a16d372be43fdb868d/20261020T020902-a48416e0916a4c719b9af4d8c153deef/result.json",
      "sha256": "23fe955042b7678d9953999d1f23622e0c0804b8b18bf2ff75a54d6e31b9a45b",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-1/39f94e446c613ebd32ccbcf29b2886cae7bb6d84adb1d5a16d372be43fdb868d/20261020T020902-a48416e0916a4c719b9af4d8c153deef/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-1/39f94e446c613ebd32ccbcf29b2886cae7bb6d84adb1d5a16d372be43fdb868d/20261020T020902-a48416e0916a4c719b9af4d8c153deef/stdout.log",
      "sha256": "9182bc0448aa727785acefbf075af0e05493ca7f99b1c4ab591d1c248e1783a9",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-2/1d2676559815b24c629d9a142e2b7153aa978774c4a5fe079d11082f9fe84421/20261020T020904-0090b320a17445ad83376449238109b3/outputs/cave-column.blend",
      "sha256": "2f13dd5e424d3049f351830facbaf837778d3f680db2ec33646886d85f0a06b8",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-2/1d2676559815b24c629d9a142e2b7153aa978774c4a5fe079d11082f9fe84421/20261020T020904-0090b320a17445ad83376449238109b3/outputs/cave-column.glb",
      "sha256": "2659a158b5c3bf2a50b32057e58e6a28c42ed36827ed27f968918274fc48679a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-2/1d2676559815b24c629d9a142e2b7153aa978774c4a5fe079d11082f9fe84421/20261020T020904-0090b320a17445ad83376449238109b3/outputs/metadata.json",
      "sha256": "0d15dea5a45ec5bb14f4ecba9e83afce8f5b62d1da4a5504f5cec26f45b877e2",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-2/1d2676559815b24c629d9a142e2b7153aa978774c4a5fe079d11082f9fe84421/20261020T020904-0090b320a17445ad83376449238109b3/outputs/qa.json",
      "sha256": "fb70a9cf8fad146eee580d3d96d8d204c9e1b5f90ca86fcebb9d9c59f572f4d2",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-2/1d2676559815b24c629d9a142e2b7153aa978774c4a5fe079d11082f9fe84421/20261020T020904-0090b320a17445ad83376449238109b3/request.json",
      "sha256": "8beb79a624e763b332a6b2c0a589c494cb6c9f631260e41d1e5b2bbe3a21d09e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-2/1d2676559815b24c629d9a142e2b7153aa978774c4a5fe079d11082f9fe84421/20261020T020904-0090b320a17445ad83376449238109b3/result.json",
      "sha256": "85332443ee97817a9a6e013aceb5c078195fe519d5934972a4e45258586f87ca",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-2/1d2676559815b24c629d9a142e2b7153aa978774c4a5fe079d11082f9fe84421/20261020T020904-0090b320a17445ad83376449238109b3/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/cave-column/r002/build-2/1d2676559815b24c629d9a142e2b7153aa978774c4a5fe079d11082f9fe84421/20261020T020904-0090b320a17445ad83376449238109b3/stdout.log",
      "sha256": "6a9e55770201c7fbfd1b902e04d411c96fabeb491b9a6e921f6805c439acd219",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-0/aef1df5db27b74d6084df53aca7c33fb24d57386e804b1fc4b6459f9d5a553ca/20261020T020906-80c0007d231d4244864c8b3c1730f210/outputs/metadata.json",
      "sha256": "4f781a178d6370e44061d1df78846c34c34ecb4278f6ecef72e8510055aeb013",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-0/aef1df5db27b74d6084df53aca7c33fb24d57386e804b1fc4b6459f9d5a553ca/20261020T020906-80c0007d231d4244864c8b3c1730f210/outputs/nidula-baltica.blend",
      "sha256": "8a700d31eccc347ea3834f8cfc273827d204f30cf03ee797eb798b5afb02e90d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-0/aef1df5db27b74d6084df53aca7c33fb24d57386e804b1fc4b6459f9d5a553ca/20261020T020906-80c0007d231d4244864c8b3c1730f210/outputs/nidula-baltica.glb",
      "sha256": "2de9c6a6ef69e3aab055add63797055bcd9174da0c7d92554b76ed697c3d2997",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-0/aef1df5db27b74d6084df53aca7c33fb24d57386e804b1fc4b6459f9d5a553ca/20261020T020906-80c0007d231d4244864c8b3c1730f210/outputs/qa.json",
      "sha256": "37b10f9a9a5493fc7e7b3a2d211b5e17db088b2fdbbaf228e62785f0ca9d384a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-0/aef1df5db27b74d6084df53aca7c33fb24d57386e804b1fc4b6459f9d5a553ca/20261020T020906-80c0007d231d4244864c8b3c1730f210/request.json",
      "sha256": "1a692f4034894484a19f4b7c98d15fbccffbdf0b0db8fc66c3f859b31336b360",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-0/aef1df5db27b74d6084df53aca7c33fb24d57386e804b1fc4b6459f9d5a553ca/20261020T020906-80c0007d231d4244864c8b3c1730f210/result.json",
      "sha256": "ab0e626e081b1022e6ee7b02f86203ae63293d4147fa7b898454b670022ffefb",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-0/aef1df5db27b74d6084df53aca7c33fb24d57386e804b1fc4b6459f9d5a553ca/20261020T020906-80c0007d231d4244864c8b3c1730f210/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-0/aef1df5db27b74d6084df53aca7c33fb24d57386e804b1fc4b6459f9d5a553ca/20261020T020906-80c0007d231d4244864c8b3c1730f210/stdout.log",
      "sha256": "c90362fef919b97f828c3647b7d4cdddd9b967fea8c8e6c1a53004b611a176cb",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-1/de454f2c7130de60365f991e6f61953dec62f430a8cd264881c11cabe2f45209/20261020T020908-d5d978a8a516470798eb0d5482a379b4/outputs/metadata.json",
      "sha256": "fae6851ca3f508d5a41f0ff4c8936ffa8ed44ebd7803ada1d281ac1dbe8d6efe",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-1/de454f2c7130de60365f991e6f61953dec62f430a8cd264881c11cabe2f45209/20261020T020908-d5d978a8a516470798eb0d5482a379b4/outputs/nidula-baltica.blend",
      "sha256": "8ea4c1e662b78b4b3921feb8d45a19ece565ca1a9c0ec71c747c8a955f4703a1",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-1/de454f2c7130de60365f991e6f61953dec62f430a8cd264881c11cabe2f45209/20261020T020908-d5d978a8a516470798eb0d5482a379b4/outputs/nidula-baltica.glb",
      "sha256": "2de9c6a6ef69e3aab055add63797055bcd9174da0c7d92554b76ed697c3d2997",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-1/de454f2c7130de60365f991e6f61953dec62f430a8cd264881c11cabe2f45209/20261020T020908-d5d978a8a516470798eb0d5482a379b4/outputs/qa.json",
      "sha256": "091ba2e2612ca80f6ff4762898cc21b83ff7139df6fef992b7218f14ed700737",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-1/de454f2c7130de60365f991e6f61953dec62f430a8cd264881c11cabe2f45209/20261020T020908-d5d978a8a516470798eb0d5482a379b4/request.json",
      "sha256": "cc4cb130e89bac5f54b9018638ed98d32f35de9673c1fce574076301baebe8de",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-1/de454f2c7130de60365f991e6f61953dec62f430a8cd264881c11cabe2f45209/20261020T020908-d5d978a8a516470798eb0d5482a379b4/result.json",
      "sha256": "482eb0ec3e2e95f313800377c460d49d3db39b2dfd16e6297dc8d923eca6eeee",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-1/de454f2c7130de60365f991e6f61953dec62f430a8cd264881c11cabe2f45209/20261020T020908-d5d978a8a516470798eb0d5482a379b4/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-1/de454f2c7130de60365f991e6f61953dec62f430a8cd264881c11cabe2f45209/20261020T020908-d5d978a8a516470798eb0d5482a379b4/stdout.log",
      "sha256": "7f85971f19301030200c1c51d20c946621c654db6eebdc9685cc04bca835f7d2",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-2/ccdb46d9bf8eba5ce959c73567ac482a666938a2f98038adeb0bf8325d1e479e/20261020T020909-dac8df254f124f2ea7e4cf15a7916e58/outputs/metadata.json",
      "sha256": "9b9e44e1d2c1204367b06571947df1e0a15b023e21bf94333aedb1973f70a544",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-2/ccdb46d9bf8eba5ce959c73567ac482a666938a2f98038adeb0bf8325d1e479e/20261020T020909-dac8df254f124f2ea7e4cf15a7916e58/outputs/nidula-baltica.blend",
      "sha256": "3291afc52035e91fcdf6972c21cc304b05d026c1f284c3032e2b192ae256f836",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-2/ccdb46d9bf8eba5ce959c73567ac482a666938a2f98038adeb0bf8325d1e479e/20261020T020909-dac8df254f124f2ea7e4cf15a7916e58/outputs/nidula-baltica.glb",
      "sha256": "2de9c6a6ef69e3aab055add63797055bcd9174da0c7d92554b76ed697c3d2997",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-2/ccdb46d9bf8eba5ce959c73567ac482a666938a2f98038adeb0bf8325d1e479e/20261020T020909-dac8df254f124f2ea7e4cf15a7916e58/outputs/qa.json",
      "sha256": "78b577116eb0ca3ff4ad268db6b8bc19f19eea83e3a7aa884995b1e2255e8353",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-2/ccdb46d9bf8eba5ce959c73567ac482a666938a2f98038adeb0bf8325d1e479e/20261020T020909-dac8df254f124f2ea7e4cf15a7916e58/request.json",
      "sha256": "510447b65c119378294701a5116b79f29de4a8ee7f633fcff12ec01bd7048415",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-2/ccdb46d9bf8eba5ce959c73567ac482a666938a2f98038adeb0bf8325d1e479e/20261020T020909-dac8df254f124f2ea7e4cf15a7916e58/result.json",
      "sha256": "89867bf457811dc8de4c5fb0abad1b0e510d6cee49f94bd91b5acd080dfed04a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-2/ccdb46d9bf8eba5ce959c73567ac482a666938a2f98038adeb0bf8325d1e479e/20261020T020909-dac8df254f124f2ea7e4cf15a7916e58/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/nidula-baltica/r002/build-2/ccdb46d9bf8eba5ce959c73567ac482a666938a2f98038adeb0bf8325d1e479e/20261020T020909-dac8df254f124f2ea7e4cf15a7916e58/stdout.log",
      "sha256": "d5d1caad26f6483bf801f847f422f321f7a337588eb9e77922dd4eb52146be20",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-0/57ae2d34fc19764b13b3c03a78cc29f8c68be426ad947cee864a4afc83847e26/20261020T020856-c2543cb590ec4ca1b98929dfbddb8162/outputs/_export/quatsinoporites/qa.json",
      "sha256": "c96071d069b61a750356fa5f0fb7f34eb7b4099b391bea948a471903f8930061",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-0/57ae2d34fc19764b13b3c03a78cc29f8c68be426ad947cee864a4afc83847e26/20261020T020856-c2543cb590ec4ca1b98929dfbddb8162/request.json",
      "sha256": "ab70ce9cf8633c536cbda9efc36fda750014a16ccafdeb46dab2a7e7fcf0c48f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-0/57ae2d34fc19764b13b3c03a78cc29f8c68be426ad947cee864a4afc83847e26/20261020T020856-c2543cb590ec4ca1b98929dfbddb8162/result.json",
      "sha256": "3b4425eb0ed85e743a54487645bdafab0526b29d914644e9d2958a0f7536f791",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-0/57ae2d34fc19764b13b3c03a78cc29f8c68be426ad947cee864a4afc83847e26/20261020T020856-c2543cb590ec4ca1b98929dfbddb8162/stderr.log",
      "sha256": "96e11a2c27801a373b4dcaba0a25ed9e0332632ae4c734dbdaf24a0e83307bd7",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-0/57ae2d34fc19764b13b3c03a78cc29f8c68be426ad947cee864a4afc83847e26/20261020T020856-c2543cb590ec4ca1b98929dfbddb8162/stdout.log",
      "sha256": "90b9f23d612e25562b057cb9a15b4c7e5304ebbd85d3aae0f5cabe1bfc51ebaa",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-1/735cb8706e8add4505817e6adea5ff46f8e47f71ea70977aa475ff31b9a4f1d2/20261020T020858-8c9a10bb05c04608a16edab46d22de7d/outputs/_export/quatsinoporites/qa.json",
      "sha256": "c96071d069b61a750356fa5f0fb7f34eb7b4099b391bea948a471903f8930061",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-1/735cb8706e8add4505817e6adea5ff46f8e47f71ea70977aa475ff31b9a4f1d2/20261020T020858-8c9a10bb05c04608a16edab46d22de7d/request.json",
      "sha256": "2e612bce153a60b2b99ae2685b301c23734bbd0c76695ae2557d4e13d94719b4",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-1/735cb8706e8add4505817e6adea5ff46f8e47f71ea70977aa475ff31b9a4f1d2/20261020T020858-8c9a10bb05c04608a16edab46d22de7d/result.json",
      "sha256": "76eeecd342df326d0d0c37d706185bd33918447a87d9cc92c3f406039dff2a38",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-1/735cb8706e8add4505817e6adea5ff46f8e47f71ea70977aa475ff31b9a4f1d2/20261020T020858-8c9a10bb05c04608a16edab46d22de7d/stderr.log",
      "sha256": "96e11a2c27801a373b4dcaba0a25ed9e0332632ae4c734dbdaf24a0e83307bd7",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-1/735cb8706e8add4505817e6adea5ff46f8e47f71ea70977aa475ff31b9a4f1d2/20261020T020858-8c9a10bb05c04608a16edab46d22de7d/stdout.log",
      "sha256": "90b9f23d612e25562b057cb9a15b4c7e5304ebbd85d3aae0f5cabe1bfc51ebaa",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-2/275facdd7b248fdccade8b81ee3bc5c13e1a17f3dc3b9ac594f9123197e60ffe/20261020T020859-6e52e8198af14be3a351885654081207/outputs/_export/quatsinoporites/qa.json",
      "sha256": "c96071d069b61a750356fa5f0fb7f34eb7b4099b391bea948a471903f8930061",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-2/275facdd7b248fdccade8b81ee3bc5c13e1a17f3dc3b9ac594f9123197e60ffe/20261020T020859-6e52e8198af14be3a351885654081207/request.json",
      "sha256": "f7ef25843d7520cfb86ff0c70163c73a5033e363e28822d6049535b6daa98ed8",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-2/275facdd7b248fdccade8b81ee3bc5c13e1a17f3dc3b9ac594f9123197e60ffe/20261020T020859-6e52e8198af14be3a351885654081207/result.json",
      "sha256": "779f61ae6e9b0a13a9993b8c3b27a2b2ce7770972a16d032e2341991c8c16593",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-2/275facdd7b248fdccade8b81ee3bc5c13e1a17f3dc3b9ac594f9123197e60ffe/20261020T020859-6e52e8198af14be3a351885654081207/stderr.log",
      "sha256": "96e11a2c27801a373b4dcaba0a25ed9e0332632ae4c734dbdaf24a0e83307bd7",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/quatsinoporites/r002/build-2/275facdd7b248fdccade8b81ee3bc5c13e1a17f3dc3b9ac594f9123197e60ffe/20261020T020859-6e52e8198af14be3a351885654081207/stdout.log",
      "sha256": "90b9f23d612e25562b057cb9a15b4c7e5304ebbd85d3aae0f5cabe1bfc51ebaa",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-0/9193195a6492ffff903a09734386c3bc40cdde77bf0d05024fc45596a719b71a/20261020T020911-a9b2870b69c94595944fb0286a49b706/outputs/_export/rusophycus-resting-excavation/qa.json",
      "sha256": "96c68cba92fcb31a7a32cd341750d075d3cfc0e87f5dc5304255ea0791a27675",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-0/9193195a6492ffff903a09734386c3bc40cdde77bf0d05024fc45596a719b71a/20261020T020911-a9b2870b69c94595944fb0286a49b706/request.json",
      "sha256": "ccfbd663154ff13b3bcaa9078ff004bc36490ccd01910d488236c6777eb84050",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-0/9193195a6492ffff903a09734386c3bc40cdde77bf0d05024fc45596a719b71a/20261020T020911-a9b2870b69c94595944fb0286a49b706/result.json",
      "sha256": "7c110e5604d508482d4a57d9a19f727942daa5113d4e72970c154cbf2371ac0c",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-0/9193195a6492ffff903a09734386c3bc40cdde77bf0d05024fc45596a719b71a/20261020T020911-a9b2870b69c94595944fb0286a49b706/stderr.log",
      "sha256": "23908eaf46dcc3220bd038a1fb1a903d55fa2a349e925dfde20f87b6055979af",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-0/9193195a6492ffff903a09734386c3bc40cdde77bf0d05024fc45596a719b71a/20261020T020911-a9b2870b69c94595944fb0286a49b706/stdout.log",
      "sha256": "90b9f23d612e25562b057cb9a15b4c7e5304ebbd85d3aae0f5cabe1bfc51ebaa",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-1/36f80c499f9f9c45aa6dd2de626c88f6e969ddde4d8629b394bd9db11af5f09f/20261020T020912-947ce9ae7f5244918097b08cd378fc88/outputs/_export/rusophycus-resting-excavation/qa.json",
      "sha256": "96c68cba92fcb31a7a32cd341750d075d3cfc0e87f5dc5304255ea0791a27675",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-1/36f80c499f9f9c45aa6dd2de626c88f6e969ddde4d8629b394bd9db11af5f09f/20261020T020912-947ce9ae7f5244918097b08cd378fc88/request.json",
      "sha256": "60e993b8bf983bb79c7ce22fcc944903b0746569f9f942d312430edcb9d61e00",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-1/36f80c499f9f9c45aa6dd2de626c88f6e969ddde4d8629b394bd9db11af5f09f/20261020T020912-947ce9ae7f5244918097b08cd378fc88/result.json",
      "sha256": "081ff4b793b19e1aa6d35ab4399275434729591aa34619b59bc3c53f4f315a05",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-1/36f80c499f9f9c45aa6dd2de626c88f6e969ddde4d8629b394bd9db11af5f09f/20261020T020912-947ce9ae7f5244918097b08cd378fc88/stderr.log",
      "sha256": "23908eaf46dcc3220bd038a1fb1a903d55fa2a349e925dfde20f87b6055979af",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-1/36f80c499f9f9c45aa6dd2de626c88f6e969ddde4d8629b394bd9db11af5f09f/20261020T020912-947ce9ae7f5244918097b08cd378fc88/stdout.log",
      "sha256": "90b9f23d612e25562b057cb9a15b4c7e5304ebbd85d3aae0f5cabe1bfc51ebaa",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-2/d2eeaef3ddeffa4e0c5b030a2903f69ab618b5889f5475239141a62aef25d268/20261020T020914-3224b51d9e284cd99dfc683433a7223b/outputs/_export/rusophycus-resting-excavation/qa.json",
      "sha256": "96c68cba92fcb31a7a32cd341750d075d3cfc0e87f5dc5304255ea0791a27675",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-2/d2eeaef3ddeffa4e0c5b030a2903f69ab618b5889f5475239141a62aef25d268/20261020T020914-3224b51d9e284cd99dfc683433a7223b/request.json",
      "sha256": "0b95859fc48f923e9e5dc352d90d93d23349c45ac480c3fb3d5e6a4ce6652580",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-2/d2eeaef3ddeffa4e0c5b030a2903f69ab618b5889f5475239141a62aef25d268/20261020T020914-3224b51d9e284cd99dfc683433a7223b/result.json",
      "sha256": "3dc531774ef759df2c80cd17c84a93638970642a262da7eb4afa77ad9ea820c7",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-2/d2eeaef3ddeffa4e0c5b030a2903f69ab618b5889f5475239141a62aef25d268/20261020T020914-3224b51d9e284cd99dfc683433a7223b/stderr.log",
      "sha256": "23908eaf46dcc3220bd038a1fb1a903d55fa2a349e925dfde20f87b6055979af",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/build/rusophycus-resting-excavation/r002/build-2/d2eeaef3ddeffa4e0c5b030a2903f69ab618b5889f5475239141a62aef25d268/20261020T020914-3224b51d9e284cd99dfc683433a7223b/stdout.log",
      "sha256": "90b9f23d612e25562b057cb9a15b4c7e5304ebbd85d3aae0f5cabe1bfc51ebaa",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/runs/20261020T020855-5f88505604464668ad9c27f9cdeb205c/manifest.json",
      "sha256": "39d6afa122e3f65af0bf044858d0966da0ae1111493e52e126a59a754addda64",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-runs/runs/20261020T020855-5f88505604464668ad9c27f9cdeb205c/summary.json",
      "sha256": "3a68802c6fb88aee664c9b18ca2eb4bf85fc1ff0ccbcff6cdce4e2a817113fdf",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-selection.json",
      "sha256": "c1fdbb5a9d8d4ec84bb0fdb792b053f769c8b7b43d53034e64de5f41661d70e3",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/final-validation.log",
      "sha256": "318e72738927b304142664db002fc734ebd367bfdea368b14dcd7dc3df755170",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/handoff.json",
      "sha256": "69cd78d001da485fa4c5c25e1579b8af2ee1353264b2b207bdbc9a99befb48c6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/initial-lifecycle.log",
      "sha256": "fbf0b72b923c50fd49d4f44c6dff02bfd7a845d3a03e01b6239678d0566983d6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/blocker.json",
      "sha256": "a0996af5ea9014a369567eb00bd0babd883340930d321b8a6f705c61019e39a2",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/build.log",
      "sha256": "8db31bb8e5ebfca265ecbfcd41d5f4fbfa8b144cf368b7677d655eadfc787e05",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/build.log.json",
      "sha256": "20e6814cc03eac69fbe8a74653ff84d38b6d42bc7cf2aaa354e9cbec837f2b22",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/khronos-retry.log",
      "sha256": "eebeccc9bbd3b545eb51e60c9eae55203c523b75963d4a75cda5799345f51486",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/khronos-retry.log.json",
      "sha256": "793f14e08f420109f18ef9e8f4a28fcfc73658e021d7a2c308b80200c1b68025",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/khronos.log",
      "sha256": "364fe956b845fc977057bc1086492fe45e46e70664b96d1195105336cb82acac",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/khronos.log.json",
      "sha256": "32c292ab48eed5d1a242909b5566898038905a6875603b3f440126adbb41036f",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/modeling-start.json",
      "sha256": "9e7c4dd16f882cd27be40a1c9171c83e39b3b2be4fb08dcd8cc8b4dd97c82ce1",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/rebuild-1.log",
      "sha256": "d5e3cda140302a92689645ea007a8ae5453b8d3ce403ed6d76e4df80ba498c38",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/rebuild-1.log.json",
      "sha256": "80fb2edddd5ee70169a3ffc6b6d7154ffd7af024d650237eeeae0b59b751a8c5",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/rebuild-1/metadata.json",
      "sha256": "fdfcd972c0a22aca09b3d4c6b3c3ea10649bbc25fd92ae15dabd896c7600d19c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/rebuild-1/nidula-baltica.blend",
      "sha256": "d9a61807a3e296f2165e33c430633390eabcc0a64965ff28f043d0dc65280ace",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/rebuild-1/nidula-baltica.glb",
      "sha256": "50d355021cf444b1ee4dd06f60069db390270c54049c9c41b9cb5c0deab7f3a8",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/rebuild-1/qa.json",
      "sha256": "ac76791e7f3efb2351ff1842479d0775c0a6b002170bb4bd23364e1d9e57680c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/rebuild-compare-1.log",
      "sha256": "b6787c79fa407304646d988b74d0e0dea4ec9e0ed9a030fa38717419b0f0eb3f",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/rebuild-compare-1.log.json",
      "sha256": "b50ba0dea0b48c057174beddeb9c6665fcb74dffc565d76ed0ab74225b7ea89d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/render.log",
      "sha256": "2e12c61947c774d3ea3f84129c4551e6c8344c59ce92253a8af5673bf5e81e5f",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/render.log.json",
      "sha256": "b4ec74e5387369b2d4bbd3e96f77bc04ff1b3768ab44e93671bb84bb94db31c4",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/source-reopen.log",
      "sha256": "c0f628248c728faeae3f7fce52b25e95c1105b46667154256f3980d66b2cd4fb",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r001/source-reopen.log.json",
      "sha256": "f60f03bd4f0b935c15be6b6a928364102b8be5e84ca4912ca763b838785abfdc",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/khronos.log",
      "sha256": "6861d567077ffd3eb55347b78d592294e8e419b649a9f64f3cbf91a58f5560cd",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/khronos.log.json",
      "sha256": "55a94bd9f688451e71109f19fc27ed5b4deebdf565dab6d1be779f9f10503527",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/rebuild-1.log",
      "sha256": "aea1d1bcd2afcffe016b4a864b235515788758a1c79524a97ade428bfb182b74",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/rebuild-1.log.json",
      "sha256": "2aa92bb21301052583233efa5dc9772b8a443d35e1d8ca2992e19c804c33df32",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/rebuild-2.log",
      "sha256": "d50ddbe8ca44d6c82e8b17cfb59bb94a7593569f4952191dc8b6586890c030f4",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/rebuild-2.log.json",
      "sha256": "d5f107dde5ca53dec7a37d467749ee30f3ea2c6ca8d1f4df51e506910d4ae887",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/render.log",
      "sha256": "7b5289e8ce7c7e9f71401c6fed8fae5cafe186de5d53b401452e45dc75711867",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/render.log.json",
      "sha256": "21147730060c79fbbf9da2a25678d699498c5feb65e2b19be684a51364c31165",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/runtime-parse.log",
      "sha256": "6a2aa69bef2832b10cbd37270d78f4b833404dd173c727aa4b79bca3144b8ebc",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/runtime-parse.log.json",
      "sha256": "84ab5131d7a2ddf6af8e93d2b06405bd133a28522f40679bf43b49dc05413d2d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/source-reopen.log",
      "sha256": "50e1eaf7d17db11b016c3e0dee7983bb49d4682f85a18e3d7241916edd3f4487",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-baltica/r002/source-reopen.log.json",
      "sha256": "0649afa948d31b72882768655535edb2454e3e572a9c18b814564349abbc22db",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/nidula-r002-initial-build.log",
      "sha256": "75824d524f774ffa864ff3c07eac4347608df1c2f495d03c5a651fc84fb81716",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/blocker.json",
      "sha256": "ca96ef3bd8cbbee751d12d1557ed7c1ab8e4b5856e7740c04b9c7f60e725767f",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/build.log",
      "sha256": "063eca05623a8170c347ed52459f09a3edb34a4b7ae34489bfabbd2e329bc389",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/build.log.json",
      "sha256": "b0056844f0e972c4f87bca61f6b504e03ff8e4d42967e26e1245cc3b8ce1718d",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/khronos-retry.log",
      "sha256": "9f5012115808bb720bce8136d9be77b04ae9a0ccfebaac49c69a9f9557776927",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/khronos-retry.log.json",
      "sha256": "489034c2a7886ed07e83dae2fc6d8c120dd46108a9a920f57e62e268f4cb75a1",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/khronos.log",
      "sha256": "364fe956b845fc977057bc1086492fe45e46e70664b96d1195105336cb82acac",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/khronos.log.json",
      "sha256": "cb1bb50362df3e4ae5c6789e8ce8b573279a6041d7bead2d3131b9ce368ab82a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/modeling-start.json",
      "sha256": "1ed831bea97b4a8edebaa9d5d9d62cbc14e63d9c3d734e169f51bd44e10dc6de",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/rebuild-1.log",
      "sha256": "d61d78773607f7bd3b168ba40e104f88beaf20f401249b80a4220b9e139d60b6",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/rebuild-1.log.json",
      "sha256": "be7a8652e1f495e45bc5d297518eb40f8ae16ef58a6d50b1642d926337b1eb34",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/rebuild-1/metadata.json",
      "sha256": "e8f57ee61d4b8e579ba8f51acb1116ffe4f50e372a6bf1fe964673b5d2e4354e",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/rebuild-1/qa.json",
      "sha256": "265d7ec9bec9dc2efbf0145c3939d19fcfb12d4c901388562aae1996956fc937",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/rebuild-1/quatsinoporites.blend",
      "sha256": "ec507281afc90e2ae31c7a49d84bd06a0c2dbbcbf1126b2089e8810174f8b61c",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/rebuild-1/quatsinoporites.glb",
      "sha256": "8d1dbd00dab4303b667d48048d5a8df737f07cb54d53a8173bb72fc025d622c2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/rebuild-compare-1.log",
      "sha256": "c18120848ad27dc5a50d3d4628a662655413ab1088d527c1aa19870a166f7d97",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/rebuild-compare-1.log.json",
      "sha256": "b9b1eff956402651c65f4800c933e539c4887f77c2fdb59a18b37f2dae3722ee",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/render-delivery.log",
      "sha256": "059cef8376e314e8143d88fd3f62000a220a00853dd6ef0a990e33c722de12c3",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/render-delivery.log.json",
      "sha256": "cec40964da80c31abe6cca69ff084df65918659b45065e01cd46e23ff78eeb73",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/render.log",
      "sha256": "fd0478845c36c5b1a66d95ee560f140947ada7e4886ff86768462e688422b775",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/render.log.json",
      "sha256": "5f1832ed1b496c110d181379acbb3684060af15e30fe909c12e3855c479a5a82",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/source-reopen.log",
      "sha256": "d9845d9814f56f230eb2156701ef05eac1292387aeca8da072b5277c21f18f14",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/quatsinoporites/r001/source-reopen.log.json",
      "sha256": "ca7867a37be1dbe5f4f875f87b0960ed2b27fb24478453e1127f9a2c6133a652",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rebuild-queue.json",
      "sha256": "c0b01e4e9bb856f885a502a69827c422bacc5b195df08950444512447ae81eac",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/retry-lifecycle.log",
      "sha256": "bca07b604bbe46e50114ff9f3d1128ad1739ea325e341b9cd7297c7aa0a0d6f6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/.queue.lock",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-1/c3318b0aedfad8d3374f11fc751de95604ee6c9be069225a3be0855de7ce54b1/20261020T020703-f9fc4fdfa0014e54931eb6fe6086496d/outputs/cave-column.blend",
      "sha256": "86d8751d71b31e33cae1d1e5ba61daeee29c13d904321bf5d164b9766848157c",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-1/c3318b0aedfad8d3374f11fc751de95604ee6c9be069225a3be0855de7ce54b1/20261020T020703-f9fc4fdfa0014e54931eb6fe6086496d/outputs/cave-column.glb",
      "sha256": "da454320cf9b4c890efae36418cf6b47600bc00b5cd0e77d89a5e5e85b394d0f",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-1/c3318b0aedfad8d3374f11fc751de95604ee6c9be069225a3be0855de7ce54b1/20261020T020703-f9fc4fdfa0014e54931eb6fe6086496d/outputs/metadata.json",
      "sha256": "f07b640897ae853dfe0145589a547d913952eae570e1d1846e705e98e5ee4db0",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-1/c3318b0aedfad8d3374f11fc751de95604ee6c9be069225a3be0855de7ce54b1/20261020T020703-f9fc4fdfa0014e54931eb6fe6086496d/outputs/qa.json",
      "sha256": "1416edac7a234296eacacab2cb7841063a40ade355dee2690ec0e3c965637d7f",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-1/c3318b0aedfad8d3374f11fc751de95604ee6c9be069225a3be0855de7ce54b1/20261020T020703-f9fc4fdfa0014e54931eb6fe6086496d/request.json",
      "sha256": "580718cb5a4218c051084b57a79c71bf7f835b79f58b3ebc54f751d0dfd80d4a",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-1/c3318b0aedfad8d3374f11fc751de95604ee6c9be069225a3be0855de7ce54b1/20261020T020703-f9fc4fdfa0014e54931eb6fe6086496d/result.json",
      "sha256": "1a7f678339f7615fe4ab26999c67936d4b131deab0b2792ce2a4e6eeb5cf891b",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-1/c3318b0aedfad8d3374f11fc751de95604ee6c9be069225a3be0855de7ce54b1/20261020T020703-f9fc4fdfa0014e54931eb6fe6086496d/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-1/c3318b0aedfad8d3374f11fc751de95604ee6c9be069225a3be0855de7ce54b1/20261020T020703-f9fc4fdfa0014e54931eb6fe6086496d/stdout.log",
      "sha256": "af39799de3b87303d209eb3a94a74fcf0b78d96814fa81849127d9262391b0ee",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-2/69d419533f5c7d152b0d5abb2514379a5a2ba687dff5129b14fa3f48090d197c/20261020T020705-cc1627664a5b4adbba75e5545ced29b9/outputs/cave-column.blend",
      "sha256": "452ed2793ac32157eaa1c8d9164f24c360c2fd49763c0363e8e51559a59f3b80",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-2/69d419533f5c7d152b0d5abb2514379a5a2ba687dff5129b14fa3f48090d197c/20261020T020705-cc1627664a5b4adbba75e5545ced29b9/outputs/cave-column.glb",
      "sha256": "da454320cf9b4c890efae36418cf6b47600bc00b5cd0e77d89a5e5e85b394d0f",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-2/69d419533f5c7d152b0d5abb2514379a5a2ba687dff5129b14fa3f48090d197c/20261020T020705-cc1627664a5b4adbba75e5545ced29b9/outputs/metadata.json",
      "sha256": "4b410c679d01024ea6dc12374f4152201513ec4eb3ca88ebb4a729903d0ecb16",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-2/69d419533f5c7d152b0d5abb2514379a5a2ba687dff5129b14fa3f48090d197c/20261020T020705-cc1627664a5b4adbba75e5545ced29b9/outputs/qa.json",
      "sha256": "c2ac9c245b8b19fcb5ccfb495baa991532b048cc6efb379199c71e86995d515b",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-2/69d419533f5c7d152b0d5abb2514379a5a2ba687dff5129b14fa3f48090d197c/20261020T020705-cc1627664a5b4adbba75e5545ced29b9/request.json",
      "sha256": "f06f4a09e757540ee6941e386993a60de27c12b31a632b1443a884862786b58e",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-2/69d419533f5c7d152b0d5abb2514379a5a2ba687dff5129b14fa3f48090d197c/20261020T020705-cc1627664a5b4adbba75e5545ced29b9/result.json",
      "sha256": "02ba5945e6ab00919f71cdd40ad0566dda3de5f955bb29af0aa314e14a90c053",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-2/69d419533f5c7d152b0d5abb2514379a5a2ba687dff5129b14fa3f48090d197c/20261020T020705-cc1627664a5b4adbba75e5545ced29b9/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/cave-column/r001/rebuild-bound-2/69d419533f5c7d152b0d5abb2514379a5a2ba687dff5129b14fa3f48090d197c/20261020T020705-cc1627664a5b4adbba75e5545ced29b9/stdout.log",
      "sha256": "89c9536cce7c4f5a6b4fd1ad6c03837c83996ef95ba82fe7b752e9ed1e566522",
      "origin": "source",
      "owner": "cave-column"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-1/eec5555c603315b2ceb38d5ced96179e73219089387c0142747c1508b91a186d/20261020T020707-62c25907f0e94d2db218b398ddf2d58c/outputs/metadata.json",
      "sha256": "377086e2133e4fd349818e1435a28531a8bcdb7f49a863bb38012080455f760d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-1/eec5555c603315b2ceb38d5ced96179e73219089387c0142747c1508b91a186d/20261020T020707-62c25907f0e94d2db218b398ddf2d58c/outputs/nidula-baltica.blend",
      "sha256": "655e12d05f8d13283f5e19370acb24ecf489c1c92ec728ec39f1798bb1d4437a",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-1/eec5555c603315b2ceb38d5ced96179e73219089387c0142747c1508b91a186d/20261020T020707-62c25907f0e94d2db218b398ddf2d58c/outputs/nidula-baltica.glb",
      "sha256": "50d355021cf444b1ee4dd06f60069db390270c54049c9c41b9cb5c0deab7f3a8",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-1/eec5555c603315b2ceb38d5ced96179e73219089387c0142747c1508b91a186d/20261020T020707-62c25907f0e94d2db218b398ddf2d58c/outputs/qa.json",
      "sha256": "d3dc32e1e2b537034ccc8e886547660f25efa3fabcb768ae6fba417b41b8a6cf",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-1/eec5555c603315b2ceb38d5ced96179e73219089387c0142747c1508b91a186d/20261020T020707-62c25907f0e94d2db218b398ddf2d58c/request.json",
      "sha256": "1b8965ca594d0acea65cd9335a5de7207688a4f5268a562076471dac354c116c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-1/eec5555c603315b2ceb38d5ced96179e73219089387c0142747c1508b91a186d/20261020T020707-62c25907f0e94d2db218b398ddf2d58c/result.json",
      "sha256": "5a4b87c5759f4b3100e68acb46e8bb473715a1e613635cf49c6d8ac72d36623e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-1/eec5555c603315b2ceb38d5ced96179e73219089387c0142747c1508b91a186d/20261020T020707-62c25907f0e94d2db218b398ddf2d58c/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-1/eec5555c603315b2ceb38d5ced96179e73219089387c0142747c1508b91a186d/20261020T020707-62c25907f0e94d2db218b398ddf2d58c/stdout.log",
      "sha256": "59a1ae0c2059fe9612ee4a90cf6160a3d133d92a63d7dfcdf823885e07f3834e",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-2/c7040e7ac6655a60b4febbc6a750c477bcc29610886b056ac0e352a82d6f5248/20261020T020708-9f8776f8af74478a9f87c5e6f21e76ff/outputs/metadata.json",
      "sha256": "c19e2bb8e01f40fc1d8538ff9325698972f86fa99c6d9ea6142565ba1dabad75",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-2/c7040e7ac6655a60b4febbc6a750c477bcc29610886b056ac0e352a82d6f5248/20261020T020708-9f8776f8af74478a9f87c5e6f21e76ff/outputs/nidula-baltica.blend",
      "sha256": "4e07c9eb2b76c4002a5875cbb7a3332372743ea76d623b55fb9e0750b4c11bea",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-2/c7040e7ac6655a60b4febbc6a750c477bcc29610886b056ac0e352a82d6f5248/20261020T020708-9f8776f8af74478a9f87c5e6f21e76ff/outputs/nidula-baltica.glb",
      "sha256": "50d355021cf444b1ee4dd06f60069db390270c54049c9c41b9cb5c0deab7f3a8",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-2/c7040e7ac6655a60b4febbc6a750c477bcc29610886b056ac0e352a82d6f5248/20261020T020708-9f8776f8af74478a9f87c5e6f21e76ff/outputs/qa.json",
      "sha256": "fec0df8cba68ae90807808526ff712ef4a5c45c4ea1d4c39f0fc15c53c5c1529",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-2/c7040e7ac6655a60b4febbc6a750c477bcc29610886b056ac0e352a82d6f5248/20261020T020708-9f8776f8af74478a9f87c5e6f21e76ff/request.json",
      "sha256": "84df47c4a2c5eb5ae4e789d0ca51beac9efa1ce312d34bf74d568354ebdd28ec",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-2/c7040e7ac6655a60b4febbc6a750c477bcc29610886b056ac0e352a82d6f5248/20261020T020708-9f8776f8af74478a9f87c5e6f21e76ff/result.json",
      "sha256": "167f321d8c64dd630ab2b2adf46de886bab5ea6d00ac4dad67c2d3443de87e45",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-2/c7040e7ac6655a60b4febbc6a750c477bcc29610886b056ac0e352a82d6f5248/20261020T020708-9f8776f8af74478a9f87c5e6f21e76ff/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/nidula-baltica/r001/rebuild-bound-2/c7040e7ac6655a60b4febbc6a750c477bcc29610886b056ac0e352a82d6f5248/20261020T020708-9f8776f8af74478a9f87c5e6f21e76ff/stdout.log",
      "sha256": "82d316fe9564f343bdf04ab4740458dab331f45f304242d5442be1238aa7a965",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-1/01f0396068f1d1ea0ea1c36a631f827ebcbad88072f908b00cceb5e5a5d0987c/20261020T020700-8575347c6d104dc1b42c94873d77e5ce/outputs/metadata.json",
      "sha256": "e721870f06c47152fbd83d66693289793e8870f0900355eea75669851ef98396",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-1/01f0396068f1d1ea0ea1c36a631f827ebcbad88072f908b00cceb5e5a5d0987c/20261020T020700-8575347c6d104dc1b42c94873d77e5ce/outputs/qa.json",
      "sha256": "0c3d3ff82b297c8e010696de6a92ff78ca5e196f2c51e9016a423af07ea74d7a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-1/01f0396068f1d1ea0ea1c36a631f827ebcbad88072f908b00cceb5e5a5d0987c/20261020T020700-8575347c6d104dc1b42c94873d77e5ce/outputs/quatsinoporites.blend",
      "sha256": "347274e5ea6cb1c2f25ae1a6349c3f26fc11a5e93e364e440451c091486d0e9a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-1/01f0396068f1d1ea0ea1c36a631f827ebcbad88072f908b00cceb5e5a5d0987c/20261020T020700-8575347c6d104dc1b42c94873d77e5ce/outputs/quatsinoporites.glb",
      "sha256": "8d1dbd00dab4303b667d48048d5a8df737f07cb54d53a8173bb72fc025d622c2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-1/01f0396068f1d1ea0ea1c36a631f827ebcbad88072f908b00cceb5e5a5d0987c/20261020T020700-8575347c6d104dc1b42c94873d77e5ce/request.json",
      "sha256": "9765c7b7b61046641f0199c93d142a099c84682a0c96c651c2907fcefd47ff35",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-1/01f0396068f1d1ea0ea1c36a631f827ebcbad88072f908b00cceb5e5a5d0987c/20261020T020700-8575347c6d104dc1b42c94873d77e5ce/result.json",
      "sha256": "6470c677d740a3713187722097951e21acf98ecd6cb38754d42c58d6d0307809",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-1/01f0396068f1d1ea0ea1c36a631f827ebcbad88072f908b00cceb5e5a5d0987c/20261020T020700-8575347c6d104dc1b42c94873d77e5ce/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-1/01f0396068f1d1ea0ea1c36a631f827ebcbad88072f908b00cceb5e5a5d0987c/20261020T020700-8575347c6d104dc1b42c94873d77e5ce/stdout.log",
      "sha256": "70b752e10b7180582bc05b4e5ccc0a57aa4bb51a2fc2160458048aa42e20cfef",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-2/e14e17f5d51856f8ec2029c18d1e197bbf29ec35853791c452f6bbc3207fb70b/20261020T020702-a127e0c5444c41d08ebc1a15e806627a/outputs/metadata.json",
      "sha256": "b12ffea006c50874f411a01b8f906df69bf7fd2e9055316aca72349fd2b226ac",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-2/e14e17f5d51856f8ec2029c18d1e197bbf29ec35853791c452f6bbc3207fb70b/20261020T020702-a127e0c5444c41d08ebc1a15e806627a/outputs/qa.json",
      "sha256": "3382620b26a4f3d718fbda291fb181a07a10c3612d9c4b2895eb869c77559040",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-2/e14e17f5d51856f8ec2029c18d1e197bbf29ec35853791c452f6bbc3207fb70b/20261020T020702-a127e0c5444c41d08ebc1a15e806627a/outputs/quatsinoporites.blend",
      "sha256": "56570a9a0181fab5bc2f87f649bd95a9e76d395e49be6b1881af94ab0bf8f396",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-2/e14e17f5d51856f8ec2029c18d1e197bbf29ec35853791c452f6bbc3207fb70b/20261020T020702-a127e0c5444c41d08ebc1a15e806627a/outputs/quatsinoporites.glb",
      "sha256": "8d1dbd00dab4303b667d48048d5a8df737f07cb54d53a8173bb72fc025d622c2",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-2/e14e17f5d51856f8ec2029c18d1e197bbf29ec35853791c452f6bbc3207fb70b/20261020T020702-a127e0c5444c41d08ebc1a15e806627a/request.json",
      "sha256": "161a04699beb245e3914e86ec39b9fb0471237909c57dac846fbbb9bdb22cf79",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-2/e14e17f5d51856f8ec2029c18d1e197bbf29ec35853791c452f6bbc3207fb70b/20261020T020702-a127e0c5444c41d08ebc1a15e806627a/result.json",
      "sha256": "1a61a93cd5283e015ebd61c20169e095f84907524323362e5156850a6fdd3f0a",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-2/e14e17f5d51856f8ec2029c18d1e197bbf29ec35853791c452f6bbc3207fb70b/20261020T020702-a127e0c5444c41d08ebc1a15e806627a/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/quatsinoporites/r001/rebuild-bound-2/e14e17f5d51856f8ec2029c18d1e197bbf29ec35853791c452f6bbc3207fb70b/20261020T020702-a127e0c5444c41d08ebc1a15e806627a/stdout.log",
      "sha256": "7d1ab100d4cfafe803123ebac66db6db44ca060a8ecddaa2e5fca971d2e07c63",
      "origin": "source",
      "owner": "quatsinoporites"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-1/cba654475419c58b823dffb90cc9f0ed114ab2e9c5afffea16553212e0637a38/20261020T020710-b306499a3cf3498d8134a12b7791558d/outputs/metadata.json",
      "sha256": "4fd8f66a9353fd8dd96ea69bdc5d4af46960f32f45560ec1ebc6fe6c30e4e9f8",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-1/cba654475419c58b823dffb90cc9f0ed114ab2e9c5afffea16553212e0637a38/20261020T020710-b306499a3cf3498d8134a12b7791558d/outputs/qa.json",
      "sha256": "e6be42ea0613f51984843b351f93f619ba9a1409fb709eeb09259cb90c15050d",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-1/cba654475419c58b823dffb90cc9f0ed114ab2e9c5afffea16553212e0637a38/20261020T020710-b306499a3cf3498d8134a12b7791558d/outputs/rusophycus-resting-excavation.blend",
      "sha256": "a590997cff09ca3ab72f7a9f5a3fa475cd87813b5b0f7dd9dec1692122791b33",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-1/cba654475419c58b823dffb90cc9f0ed114ab2e9c5afffea16553212e0637a38/20261020T020710-b306499a3cf3498d8134a12b7791558d/outputs/rusophycus-resting-excavation.glb",
      "sha256": "7493f6df58164496ae64161395138520787fa2be9a9eb0f2363c56ef4f276751",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-1/cba654475419c58b823dffb90cc9f0ed114ab2e9c5afffea16553212e0637a38/20261020T020710-b306499a3cf3498d8134a12b7791558d/request.json",
      "sha256": "7dcc95ea71e27f32fb877af0fffe7f5d4ad095a488e4f2fc34177b6eb5ea4852",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-1/cba654475419c58b823dffb90cc9f0ed114ab2e9c5afffea16553212e0637a38/20261020T020710-b306499a3cf3498d8134a12b7791558d/result.json",
      "sha256": "4615ca2ef94476e76ebb0e6974b3ba661741f0d0f3224debbf37fe40daf059e8",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-1/cba654475419c58b823dffb90cc9f0ed114ab2e9c5afffea16553212e0637a38/20261020T020710-b306499a3cf3498d8134a12b7791558d/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-1/cba654475419c58b823dffb90cc9f0ed114ab2e9c5afffea16553212e0637a38/20261020T020710-b306499a3cf3498d8134a12b7791558d/stdout.log",
      "sha256": "09beaa107c328a166a4e2e162279438a906bea5b6a6c92ff895f089d57a3ba56",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-2/f7ad1893642131d03f1aeae2f44f508fb19f8bc09be568341102c9f111a96901/20261020T020712-c20d707beae149cfa87463a895d35cac/outputs/metadata.json",
      "sha256": "bb8489e282c9ec665e81966921395c4c7ccf4919f44fd243851333bd529915eb",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-2/f7ad1893642131d03f1aeae2f44f508fb19f8bc09be568341102c9f111a96901/20261020T020712-c20d707beae149cfa87463a895d35cac/outputs/qa.json",
      "sha256": "13b99a70feca31c1bf0d2d2b9440e46bb66a5e285e906c9bea8a72c9d4f95dc8",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-2/f7ad1893642131d03f1aeae2f44f508fb19f8bc09be568341102c9f111a96901/20261020T020712-c20d707beae149cfa87463a895d35cac/outputs/rusophycus-resting-excavation.blend",
      "sha256": "c3536e6ff88c0aa8bad9d6cac635279a9eb9e90622965545be123120dc73ca9e",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-2/f7ad1893642131d03f1aeae2f44f508fb19f8bc09be568341102c9f111a96901/20261020T020712-c20d707beae149cfa87463a895d35cac/outputs/rusophycus-resting-excavation.glb",
      "sha256": "7493f6df58164496ae64161395138520787fa2be9a9eb0f2363c56ef4f276751",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-2/f7ad1893642131d03f1aeae2f44f508fb19f8bc09be568341102c9f111a96901/20261020T020712-c20d707beae149cfa87463a895d35cac/request.json",
      "sha256": "1caceab8bda13a1c622713c91c8a56f9570070bf77efa08d05f6887f607cb657",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-2/f7ad1893642131d03f1aeae2f44f508fb19f8bc09be568341102c9f111a96901/20261020T020712-c20d707beae149cfa87463a895d35cac/result.json",
      "sha256": "4ce677b6793ad3d830be03fb6ad7aa24c6b3558c02f342c6faa09a20c9b0338f",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-2/f7ad1893642131d03f1aeae2f44f508fb19f8bc09be568341102c9f111a96901/20261020T020712-c20d707beae149cfa87463a895d35cac/stderr.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/build/rusophycus-resting-excavation/r001/rebuild-bound-2/f7ad1893642131d03f1aeae2f44f508fb19f8bc09be568341102c9f111a96901/20261020T020712-c20d707beae149cfa87463a895d35cac/stdout.log",
      "sha256": "88be991f7c2175897b2280c23d6215862dc91ef81101aa816759967a696d420c",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/runs/20261020T020659-d24e7e5394fd4d6f93c59668f06d5e1f/manifest.json",
      "sha256": "34be8eb53c8c98a5b727316acae75ab448db1d0f22cf9886358afd6e186a4623",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/runs/runs/20261020T020659-d24e7e5394fd4d6f93c59668f06d5e1f/summary.json",
      "sha256": "fcb071b2a309e43f212573dadb89a651ac7dbe5c2c3789ce9473dd12f0b58c3c",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/blocker.json",
      "sha256": "a921185618f088bf63450e3e81c86730eb3ec98197c7e93bb5ba6210ccc3830f",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/build.log",
      "sha256": "d216e61c6650b851e6589bcc65f2d007860a360148f7bd2ac7eacc6339d55c77",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/build.log.json",
      "sha256": "bf497104cc983676815a990b9ecce6a9ac3807467c023f7c7033c962e44ac6f6",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/khronos-retry.log",
      "sha256": "ade9249b6f7ec22e9b581324e5529ee133a0de153f16e00e7f971bc6496d7400",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/khronos-retry.log.json",
      "sha256": "18a5dbefd069afc0f7ba13c7f45dcc7c1ac1aaac42a720468b0129157f2d4e2e",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/khronos.log",
      "sha256": "364fe956b845fc977057bc1086492fe45e46e70664b96d1195105336cb82acac",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/khronos.log.json",
      "sha256": "27cfa409f731e29dfab40360798921e7bf32f9b31340d8671bfd701765d2132e",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/modeling-start.json",
      "sha256": "01b1ed15205351cab2d55dcf4e66e1b950c14018538cb250007b9e188e1815af",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/rebuild-1.log",
      "sha256": "b35f677daaa86957141388baa0827c0e7133e0b319ed6232c9200b205218b9e6",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/rebuild-1.log.json",
      "sha256": "f6c2e3f9c82eb7437dbe1077dad116cd25c2c23ddc753590ed0a45dd6af35a58",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/rebuild-1/metadata.json",
      "sha256": "760a17e33d3416cf9270ad6242202cba1661cf886cd461918fa66f1109fe088f",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/rebuild-1/qa.json",
      "sha256": "cca398e0b32f2b210d68aafc54f6addd8bb884f57e9c4a630dc3395efe0dfa5b",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/rebuild-1/rusophycus-resting-excavation.blend",
      "sha256": "6291e4c5caa7d1ef5e78845c62dc92f483782b811c333ed4cf58ec5584086f05",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/rebuild-1/rusophycus-resting-excavation.glb",
      "sha256": "7493f6df58164496ae64161395138520787fa2be9a9eb0f2363c56ef4f276751",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/rebuild-compare-1.log",
      "sha256": "7b7aced37bd9fda8cb70aefbe15b939bf34bd0840d878c953f3db28db0763c2a",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/rebuild-compare-1.log.json",
      "sha256": "1a5e844ae901b1bcc34cfa45d2c211377a663dd088cef7c66c58614ebd5ab155",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/render-delivery.log",
      "sha256": "d2d01632b9e2292e4980813170cb909d5ceabbeb5f4bdf4c5b4a0e65135f59ea",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/render-delivery.log.json",
      "sha256": "9491647e4d40597ad9b91556ed6c7576e47f573e9a5d3b85e3223f9fa43102d5",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/render.log",
      "sha256": "4584f0443203a3a8d6000dd6b0cb24842ac8682c3399bbebdd80bcb9e22dd1be",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/render.log.json",
      "sha256": "cd1eac3b518f70c51326c494666a8c2ed81a223a03cc567620ea7040d3294cc2",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/source-reopen.log",
      "sha256": "dc85f66ce45a906c43ba8671b3b93dd047a3a69be722159c8af5505d8ca8962e",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/rusophycus-resting-excavation/r001/source-reopen.log.json",
      "sha256": "b2dcb7e4f2fe70fd576f60f7b4ee92f2b02d9d28f2872930d73e94f441ae7e0b",
      "origin": "source",
      "owner": "rusophycus-resting-excavation"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/source-package-verification.json",
      "sha256": "9cceaac663b7c9cd401aeb45dc0b47776b265ffaf255a6c7af1d302969162251",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/tools/create_handoff.py",
      "sha256": "8834f498abda9ffb68f8f4d6e418d5df3a6eae78a3ffbad444d29344cab11e2d",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/tools/package_evidence.py",
      "sha256": "3003748789b00c789f1266f10d5ed1c41466b9b82fc35397a95716272dcd0303",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/tools/parse_exact_glb.mjs",
      "sha256": "c5ecc00c2720411c8201ce12180c9afca6052d986ee27e2a11b209eb4b5506b6",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "production/continuous-small-life-round21-20261020/work/batch-57/tools/render_exact_glb.py",
      "sha256": "c99e0b7d172d13da64171e5f233b92867907de7e826d5dc8b4b7a6db604b7413",
      "origin": "source",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-independent-20261020/disposition.md",
      "sha256": "2701ca202c08639d59a0fe722d96673a06002669a84b3d9d16e6f09955281b9c",
      "origin": "review",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture/assets/card-previews/cave-column-v2-768-q90.webp",
      "sha256": "5405c124906d649fed1549e7f8e65e58e9a0bbf4e7a8ea506f8c024bc48ee94b",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture/assets/card-previews/quatsinoporites-v2-768-q90.webp",
      "sha256": "24fc8eabc6516115b9b4492ed8f7778f2d88deb4d514134486eac52a39b424a9",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture/assets/card-previews/rusophycus-resting-excavation-v2-768-q90.webp",
      "sha256": "055a68e6234303072397d00d5684c0731441776404ebe4c675fbf5c5f1815051",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture/assets/turntables/index.json",
      "sha256": "9e680d380178684ed2ee52fb035bc32d0169bfa7c71b754931e468b9f281d90f",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture/references/cave-column.png",
      "sha256": "eb2f80ad46fed8a1031b114c899de6ab5d69e9a5017b7d6aead23de4892dcd70",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture/references/quatsinoporites.png",
      "sha256": "42947b74d001ca8c8022ef6a7eaa71959aa9047efeb1e3ece5c0d0f6f4c8aead",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture/references/rusophycus-resting-excavation.png",
      "sha256": "48d14d0033de970b190e31381df9ca60d07db472f671019a66bb94799861ff45",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture/render-report.json",
      "sha256": "c1ed101baab8a80cfef0e2b4c479b411374f23b46bdee79769fad7d279badf44",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture-inputs.json",
      "sha256": "bbb0b3f18d79d34c236b6239dec60e51da1f2c163962ffd5e1a96047aaa035fb",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture-provenance.json",
      "sha256": "0ee288e22e2c0a0b8949be7cbf1acd9435234400e368dc20d2f3bcb4a452a3fa",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/capture-zip-verification.json",
      "sha256": "85cef2709e55b14d23dcb9df973fdbb43b178268573f213386a36f839f8c773f",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/metadata-mapping.json",
      "sha256": "7e52c74c787f26963e65b0741540e8aa159fd3a47e83d6b6bb67ab4415cd2f1d",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/preparation.json",
      "sha256": "720cbdfb37e5fb1806c286ffe2a84b355b20b1148df335b4d3a7413a72d47bf0",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/review/lowpoly-batches56-57-independent-audit.md",
      "sha256": "ac85057fd1cc1d83db453441fcdb9b5717cd5019ac568c91b15491a7c76c60c8",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/review/lowpoly-round21-repair56-57-focused-qa.md",
      "sha256": "094a24544eb4045a11cc0c05b0828aac37b3b8ba89855fd36a45f2d9cbffb450",
      "origin": "release",
      "owner": "$batch"
    },
    {
      "path": "qa/batch57-release-20261020/source-inventory.json",
      "sha256": "14d80cf37301f05cb958e5652f9dfdc985eb9d124f4a42ad8d1ed5fe91077dd8",
      "origin": "release",
      "owner": "$batch"
    }
  ]
};
