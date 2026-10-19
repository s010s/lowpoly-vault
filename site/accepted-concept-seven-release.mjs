/** Exact seven reviewed source/QA bindings; grants no formal production acceptance. */
export const CONCEPT_SEVEN_RELEASE = {
  "version": 1,
  "scope": "concept-seven-20261019",
  "authorization": "owner_authorized_publish_independent_qa_passed_batches",
  "acceptance_scope": "independent_qa_accepted_stylized_prop",
  "formal_profile_acceptance": "BLOCKED",
  "hardware_gpu_verified": false,
  "target_scene_verified": false,
  "base_descriptor": {
    "path": "assets/releases/small-life-round13-twelve-20261018.json",
    "sha256": "ad05a2c3816f7db9f986beeab84ca7a97ef19cd733134e341e8256f888326204"
  },
  "publication_policy": {
    "path": "production/policies/qa-passed-batch-publication-20261018.json",
    "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
  },
  "source_bundle": {
    "path": "qa/concept-seven-release-20261019/source-bundle.json",
    "sha256": "4bcc37ced0a46693e86b27a31f5e75604d6173e7ec7e9487c672d2fe1cdb982a"
  },
  "excluded_ids": [
    "ctenoimbricata"
  ],
  "additions": [
    {
      "id": "metaspriggina",
      "group": "fish",
      "revision": "r001",
      "source_commit": "d8c59d6e778f235fccd1e5d451cbfc52b12cb62d",
      "review_commit": "f4406976378c132e5ec50c51e839a717ed4418fa",
      "review": {
        "path": "qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/REPORT.md",
        "sha256": "1b69ff52ee484dd7367d25b867a497db143805e3c5cd398a1f1346aa7e9da337"
      },
      "handoff": {
        "path": "production/concept-small-fish-20261019/handoff.json",
        "sha256": "9adc8988c7cf0605f44db4d7258e26f29a8bc70deaf5b3e7453f71b5a9dd52d9"
      },
      "source_metadata": {
        "path": "production/concept-small-fish-20261019/metaspriggina/r001/output/metadata.json",
        "sha256": "1cb2baade37260c073feff90adae19eb4fa8eab60298f53723836a00b2f89c04"
      },
      "metadata": {
        "path": "assets/additions/metaspriggina/concept-seven-20261019/release-metadata.json",
        "sha256": "c0938af0296db9684218b00c0dce9b1a6ad43d4a7544abfeaf5d2bc28f2fbd07"
      },
      "artifacts": {
        "glb": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/output/metaspriggina.glb",
          "sha256": "f81fd7312d73ee25ebf03b6d2984ccb0b87cc64e30136d57693358d925396950"
        },
        "blend": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/output/metaspriggina.blend",
          "sha256": "5799ef37289782744d4f7b35cca8d2771182e1590698b4fac9ba56438a46ce80"
        },
        "brief": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/brief.json",
          "sha256": "e098801aaa5afb1edf81ede028b6713f57f1407dca24c54a82d031e78f9a17a9"
        },
        "references": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/references.json",
          "sha256": "56d5ef85f43d46c58dc075a60f940becf94b9149f8f690b4f1583ba020d03f79"
        },
        "generator": {
          "path": "production/concept-small-fish-20261019/generator.py",
          "sha256": "8836e09eddfc35efcc8d5d1e893cd6b5c999133b0fd78494bce4ae1e4530d66d"
        },
        "config": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/build-config.json",
          "sha256": "9ffae0337e8eec9c35e0e83e15bdc6f60f72206f77b6ff0bb168b52b5f828a86"
        }
      },
      "technical": {
        "source_export": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/source-export.report.json",
          "sha256": "94507cced0c00f65d90329eca591eaf6b0d1088597f854def0084355ebd0d192"
        },
        "rebuild_1": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/rebuild-1.report.json",
          "sha256": "012804dfe3f28a7c62b7ab83fecf2350b4ca0202fa2a3a33b094facd4fccf7f1"
        },
        "rebuild_2": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/rebuild-2.report.json",
          "sha256": "af122079e45c5049041bd9e76252825f9045faa63801ad77d705884fbc2aa6cc"
        },
        "khronos": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/output/gltf-validator.report.json",
          "sha256": "eabf3138dc351e785d442198edc32cc0fec3beb4c2d8aea305c999642c52fc66"
        },
        "runtime_parse": {
          "path": "production/concept-small-fish-20261019/metaspriggina/r001/threejs-parse.report.json",
          "sha256": "bc93784408848cd988317f3fdce7fcc1345ac66ab6f59a68abfba76ceca629fb"
        }
      },
      "proof": {
        "path": "production/concept-small-fish-20261019/metaspriggina/r001/proof/render-manifest.json",
        "sha256": "1bad846ddee666afa9bc3b92144f3e4a84c310b2f4748e13279ab6997325f414"
      },
      "sha256": {
        "glb": "f81fd7312d73ee25ebf03b6d2984ccb0b87cc64e30136d57693358d925396950",
        "blend": "5799ef37289782744d4f7b35cca8d2771182e1590698b4fac9ba56438a46ce80",
        "preview": "c1c91cfab59d31cf507abe237111eff1b038a312aa6a85d5de2454909a43736b"
      },
      "limits": {
        "asset_id": "metaspriggina",
        "revision": "r001",
        "length_m": 0.07,
        "seed": 19,
        "max_triangles": 16000,
        "max_materials": 7,
        "max_primitives": 90,
        "soft_glb_bytes": 1000000,
        "surface_profile": "palette-only",
        "mount_origin": "swimming body midline at (0,0,0), not floor contact",
        "role": "supporting scene life, typical 128px; inspectable at 512px",
        "normal_visible_copies": 8,
        "stress_visible_copies": 32,
        "runtime_target": "repository pinned Three.js; parent independent runtime/GPU/scene QA pending"
      }
    },
    {
      "id": "falcatus",
      "group": "fish",
      "revision": "r001",
      "source_commit": "d8c59d6e778f235fccd1e5d451cbfc52b12cb62d",
      "review_commit": "f4406976378c132e5ec50c51e839a717ed4418fa",
      "review": {
        "path": "qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/REPORT.md",
        "sha256": "1b69ff52ee484dd7367d25b867a497db143805e3c5cd398a1f1346aa7e9da337"
      },
      "handoff": {
        "path": "production/concept-small-fish-20261019/handoff.json",
        "sha256": "9adc8988c7cf0605f44db4d7258e26f29a8bc70deaf5b3e7453f71b5a9dd52d9"
      },
      "source_metadata": {
        "path": "production/concept-small-fish-20261019/falcatus/r001/output/metadata.json",
        "sha256": "7a47e5ddd81cd7358c6a16249c798e307112703c8a43850fe6d42c5d85d58637"
      },
      "metadata": {
        "path": "assets/additions/falcatus/concept-seven-20261019/release-metadata.json",
        "sha256": "7706909cfbe0c6089c650e963e1c87add42a792222c8c711f4a9550647e4dfcc"
      },
      "artifacts": {
        "glb": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/output/falcatus.glb",
          "sha256": "6af92b103b6c43ff50cdc400254ac6640985e7a70ee0c2a7981d073c9fea0063"
        },
        "blend": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/output/falcatus.blend",
          "sha256": "eb285c675f7796ca4f0a86d33059649e163a46ff8f9541d20978579ec6e90176"
        },
        "brief": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/brief.json",
          "sha256": "2a7834180610f6e6b852ac81cadca0a06a62f35fe40335685a9ad053a26915c4"
        },
        "references": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/references.json",
          "sha256": "36dba9afa46bfc3df35c65ec3e3f0d7fc6a2a64fcb03b98e03ec46523367619d"
        },
        "generator": {
          "path": "production/concept-small-fish-20261019/generator.py",
          "sha256": "8836e09eddfc35efcc8d5d1e893cd6b5c999133b0fd78494bce4ae1e4530d66d"
        },
        "config": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/build-config.json",
          "sha256": "7c46ed3f87d372fade2d3731dd9ab72fdc7655b9ec84fe691db8388e04472997"
        }
      },
      "technical": {
        "source_export": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/source-export.report.json",
          "sha256": "36703355e871154c9022b10f78a0addf4daab77d9c4f2ccc2f50eda2d97e64eb"
        },
        "rebuild_1": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/rebuild-1.report.json",
          "sha256": "2f327f78740f8fc690bc84f1e63e87193adbd38f8ae64211ed29b6cea9d4d8d0"
        },
        "rebuild_2": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/rebuild-2.report.json",
          "sha256": "8cf3a7ae15aa8dab2e5b100b5320a136ab67579a4ef701ccd3e613192322d5cc"
        },
        "khronos": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/output/gltf-validator.report.json",
          "sha256": "3a5bcbf2d2a5df67e3bfd5a0c8900a36c3d7cda745946dc06991b86eb1dbf7fe"
        },
        "runtime_parse": {
          "path": "production/concept-small-fish-20261019/falcatus/r001/threejs-parse.report.json",
          "sha256": "626f3cdb6586d29b539ceed46051002cd00057b1ca2f1a18d6b1cad87bf2008d"
        }
      },
      "proof": {
        "path": "production/concept-small-fish-20261019/falcatus/r001/proof/render-manifest.json",
        "sha256": "ee1b2858b59a0f983f4f0974a265fce84e31c35789e5b0a900d632703c748ad4"
      },
      "sha256": {
        "glb": "6af92b103b6c43ff50cdc400254ac6640985e7a70ee0c2a7981d073c9fea0063",
        "blend": "eb285c675f7796ca4f0a86d33059649e163a46ff8f9541d20978579ec6e90176",
        "preview": "1461e9b6448dffc0880ffddbb4e50cf4fd6f7dd2debed52eaa9ac9dc80d3db84"
      },
      "limits": {
        "asset_id": "falcatus",
        "revision": "r001",
        "length_m": 0.28,
        "seed": 19,
        "max_triangles": 16000,
        "max_materials": 7,
        "max_primitives": 90,
        "soft_glb_bytes": 1000000,
        "surface_profile": "palette-only",
        "mount_origin": "swimming body midline at (0,0,0), not floor contact",
        "role": "supporting scene life, typical 128px; inspectable at 512px",
        "normal_visible_copies": 8,
        "stress_visible_copies": 32,
        "runtime_target": "repository pinned Three.js; parent independent runtime/GPU/scene QA pending"
      }
    },
    {
      "id": "pteraspis",
      "group": "fish",
      "revision": "r001",
      "source_commit": "d8c59d6e778f235fccd1e5d451cbfc52b12cb62d",
      "review_commit": "f4406976378c132e5ec50c51e839a717ed4418fa",
      "review": {
        "path": "qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/REPORT.md",
        "sha256": "1b69ff52ee484dd7367d25b867a497db143805e3c5cd398a1f1346aa7e9da337"
      },
      "handoff": {
        "path": "production/concept-small-fish-20261019/handoff.json",
        "sha256": "9adc8988c7cf0605f44db4d7258e26f29a8bc70deaf5b3e7453f71b5a9dd52d9"
      },
      "source_metadata": {
        "path": "production/concept-small-fish-20261019/pteraspis/r001/output/metadata.json",
        "sha256": "1e89b93404ffce5cbf3931b4a4ca388f6d26b2250fe99a8801c11b32f335fa9c"
      },
      "metadata": {
        "path": "assets/additions/pteraspis/concept-seven-20261019/release-metadata.json",
        "sha256": "18cb1f19428bb721d5b00db43462fd25ba2e482775156d94f3d2447f452bab54"
      },
      "artifacts": {
        "glb": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/output/pteraspis.glb",
          "sha256": "3e2672cdef0f412d29a3c6de23b204ca966e65d827e99503850e314fb74b0674"
        },
        "blend": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/output/pteraspis.blend",
          "sha256": "73cc00ccf544182481ce56664574ce3b99e55a128f3245263096f1a5654cbc08"
        },
        "brief": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/brief.json",
          "sha256": "d2bf788c9e1ba25930538deea12d0412868af16d5a6a21b80def4fbed105cb07"
        },
        "references": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/references.json",
          "sha256": "1b3f3ceb0f3275440c02d013939123fdc5c8352b2c4f4218ef1573cec4096c8f"
        },
        "generator": {
          "path": "production/concept-small-fish-20261019/generator.py",
          "sha256": "8836e09eddfc35efcc8d5d1e893cd6b5c999133b0fd78494bce4ae1e4530d66d"
        },
        "config": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/build-config.json",
          "sha256": "89a76794a6545cd92c3c867db444aac800e3c048245baed81113df511ee32667"
        }
      },
      "technical": {
        "source_export": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/source-export.report.json",
          "sha256": "adbb20fd57a9ab79bf387c85c7e29bd6cf3ed1c65f2b6a5432723a324287d794"
        },
        "rebuild_1": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/rebuild-1.report.json",
          "sha256": "475836b795325844899b00b049635fdad7fb2660e44a44b3e10cae84c06ea2cd"
        },
        "rebuild_2": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/rebuild-2.report.json",
          "sha256": "29d6842bf1920d82e8c921ed0495170089eb69f605f9f4a67280801b7b53d574"
        },
        "khronos": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/output/gltf-validator.report.json",
          "sha256": "cde1b168aaaf7ff1752a17189c8636d8a9652f810f343f2fb686e045bd3bfb8c"
        },
        "runtime_parse": {
          "path": "production/concept-small-fish-20261019/pteraspis/r001/threejs-parse.report.json",
          "sha256": "ab7b8a5f984c1a858ed4bc659ad2514bfc58c765177770eb269c995575e7e1cc"
        }
      },
      "proof": {
        "path": "production/concept-small-fish-20261019/pteraspis/r001/proof/render-manifest.json",
        "sha256": "ca898d613c86b261e59bf89946b7d39bea4b01740924ca89cd13e5cd65763c87"
      },
      "sha256": {
        "glb": "3e2672cdef0f412d29a3c6de23b204ca966e65d827e99503850e314fb74b0674",
        "blend": "73cc00ccf544182481ce56664574ce3b99e55a128f3245263096f1a5654cbc08",
        "preview": "304123568a834f03f1e4c2d4620fb35c8f8f7ec31dd1f41ff3d9af29540553f4"
      },
      "limits": {
        "asset_id": "pteraspis",
        "revision": "r001",
        "length_m": 0.23,
        "seed": 19,
        "max_triangles": 16000,
        "max_materials": 7,
        "max_primitives": 90,
        "soft_glb_bytes": 1000000,
        "surface_profile": "palette-only",
        "mount_origin": "swimming body midline at (0,0,0), not floor contact",
        "role": "supporting scene life, typical 128px; inspectable at 512px",
        "normal_visible_copies": 8,
        "stress_visible_copies": 32,
        "runtime_target": "repository pinned Three.js; parent independent runtime/GPU/scene QA pending"
      }
    },
    {
      "id": "dorypterus",
      "group": "fish",
      "revision": "r001",
      "source_commit": "d8c59d6e778f235fccd1e5d451cbfc52b12cb62d",
      "review_commit": "f4406976378c132e5ec50c51e839a717ed4418fa",
      "review": {
        "path": "qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/REPORT.md",
        "sha256": "1b69ff52ee484dd7367d25b867a497db143805e3c5cd398a1f1346aa7e9da337"
      },
      "handoff": {
        "path": "production/concept-small-fish-20261019/handoff.json",
        "sha256": "9adc8988c7cf0605f44db4d7258e26f29a8bc70deaf5b3e7453f71b5a9dd52d9"
      },
      "source_metadata": {
        "path": "production/concept-small-fish-20261019/dorypterus/r001/output/metadata.json",
        "sha256": "645cd4fb20ba3de9a0794d83bf501789495ce05a090ffaaaa47b923211dbc1f4"
      },
      "metadata": {
        "path": "assets/additions/dorypterus/concept-seven-20261019/release-metadata.json",
        "sha256": "d6553c0e45fbb45f2f0561237245f7d89e9fcd10c807e8822c732bcfa78b962b"
      },
      "artifacts": {
        "glb": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/output/dorypterus.glb",
          "sha256": "33955b1156a50104edbbab7f00bd244c6b17c650ec07bf6d1416ab2d3f7ef06e"
        },
        "blend": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/output/dorypterus.blend",
          "sha256": "7a67801423711974d3d82f69ed86a5be8b2260dde7cd54122009392d93833df4"
        },
        "brief": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/brief.json",
          "sha256": "3991ed0d6f649c75ba63ce0d6fdefe392b7d16f0d2708e9015036e06570a1c1b"
        },
        "references": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/references.json",
          "sha256": "43ee1a2f7cf12bfe0173ac80873a67378ead0dc2929f7927fde0110f6154166a"
        },
        "generator": {
          "path": "production/concept-small-fish-20261019/generator.py",
          "sha256": "8836e09eddfc35efcc8d5d1e893cd6b5c999133b0fd78494bce4ae1e4530d66d"
        },
        "config": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/build-config.json",
          "sha256": "e7df015f8693e05a2b261b121ecf46483ec3cd62f818216ce067f6da3be94c87"
        }
      },
      "technical": {
        "source_export": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/source-export.report.json",
          "sha256": "0e4a314e0e041fd58fefed093dcc916de7dc4293e8a55903ee9a0906391455f8"
        },
        "rebuild_1": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/rebuild-1.report.json",
          "sha256": "628c50448b90c89d6e5a66117386044931d81d93384fdce14420cd39f28f87b2"
        },
        "rebuild_2": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/rebuild-2.report.json",
          "sha256": "7404400aeea0490e3709eb69ebc39dc8ad3239047d64a65b832f73f3f4810697"
        },
        "khronos": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/output/gltf-validator.report.json",
          "sha256": "08b53c0c8865140d059af49877a21c2c6783760c34fcf6f3bc1768dcdd3a4cb4"
        },
        "runtime_parse": {
          "path": "production/concept-small-fish-20261019/dorypterus/r001/threejs-parse.report.json",
          "sha256": "65a61e94189fe9241d02924b876c560c97e0864b22517e7e203d664153fc4108"
        }
      },
      "proof": {
        "path": "production/concept-small-fish-20261019/dorypterus/r001/proof/render-manifest.json",
        "sha256": "bc3ee73c77e55f3ff1072b9bf0883b8598ea0b6308d01c7ca100921a472dc0de"
      },
      "sha256": {
        "glb": "33955b1156a50104edbbab7f00bd244c6b17c650ec07bf6d1416ab2d3f7ef06e",
        "blend": "7a67801423711974d3d82f69ed86a5be8b2260dde7cd54122009392d93833df4",
        "preview": "0119362261809f929fb55d9077a5a6d6ebf4391ad268a1823a552c54c5dfea95"
      },
      "limits": {
        "asset_id": "dorypterus",
        "revision": "r001",
        "length_m": 0.12,
        "seed": 19,
        "max_triangles": 16000,
        "max_materials": 7,
        "max_primitives": 90,
        "soft_glb_bytes": 1000000,
        "surface_profile": "palette-only",
        "mount_origin": "swimming body midline at (0,0,0), not floor contact",
        "role": "supporting scene life, typical 128px; inspectable at 512px",
        "normal_visible_copies": 8,
        "stress_visible_copies": 32,
        "runtime_target": "repository pinned Three.js; parent independent runtime/GPU/scene QA pending"
      }
    },
    {
      "id": "mackenzia",
      "group": "marine",
      "revision": "r001",
      "source_commit": "fc2f6db4133b62e48b9764e4a33b0fd518e806df",
      "review_commit": "33dbb7c2d3deef2b0c17d2bb87daa9da2fea14cc",
      "review": {
        "path": "qa/undersea-invertebrates-concept-20261019/review.json",
        "sha256": "a83ddf9706a8b5f644fea124bc77006c0bf19cd43168d2c0ce21a2d9c9857597"
      },
      "handoff": {
        "path": "production/undersea-invertebrates-concept-20261019/handoff.json",
        "sha256": "aaceacde4cfddd0c3b19429529b8e1271b117db50e35ca252201e44f1ae39294"
      },
      "source_metadata": {
        "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/metadata.json",
        "sha256": "da965e04a2dcf29efdd2907caff09139f2347a40a6a17e30b7df7d98fbe5ac19"
      },
      "metadata": {
        "path": "assets/additions/mackenzia/concept-seven-20261019/release-metadata.json",
        "sha256": "820bbc29bccedadf74aed0cd0510191d0d8a062698e3f1ea96df0561f3fa6597"
      },
      "artifacts": {
        "glb": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/mackenzia.glb",
          "sha256": "6558b3cce6b208ff5e27d0fe56b4ff703ba205f187a51d9d3d178b318ac6bd5d"
        },
        "blend": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/mackenzia.blend",
          "sha256": "68cc73013eae89fb96fdb9b9feeec7d2743fc5d32943498c64145921858fbdbe"
        },
        "brief": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/brief.json",
          "sha256": "0cfe2cc989352aacc5ea6e77d1b5fe2c04a0fd758b2966264c118b3a3ffa7d61"
        },
        "references": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/references.json",
          "sha256": "feaf4d3eabcfbe10cb9665372ac8440a300c1366f5a409b49385944f8a4d7dfb"
        },
        "generator": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/generator.py",
          "sha256": "427f9b4597ed086e496c59459a98b5527d4a293f31ba41bab15dd5790cfa7193"
        },
        "config": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/build-config.json",
          "sha256": "466d69098d99c6fdd4b6c414e86c7eac960a526cc30f2a823a51010f0656457d"
        }
      },
      "technical": {
        "source_export": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/evidence/source-export.report.json",
          "sha256": "4d4cb3cf55d008bbbbd26e79f72dd5e01b49aabdad33914d55b189f71fbd94de"
        },
        "rebuild_1": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/evidence/reproducibility-1.report.json",
          "sha256": "aa9b11bdfd49f614330bad6c5f890dd87cfd7b161748fb16190681b62f2b751d"
        },
        "rebuild_2": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/evidence/reproducibility-2.report.json",
          "sha256": "ce92133ddc62ed3646c427f673d50db0184d575f2e0f1c4db7060a00d4185a0f"
        },
        "khronos": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/gltf-validator.report.json",
          "sha256": "fb0dd6cdad18fb7a1828424141501e6101ed1299b08f4f3686979a19b742d2ab"
        },
        "runtime_parse": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/evidence/runtime-parse.report.json",
          "sha256": "51b5c055fbccc1bfe50bf9a0b4358d9d42aedaa3580f6da7e602c254756dc45e"
        }
      },
      "proof": {
        "path": "assets/candidates/undersea-invertebrates-concept-20261019/mackenzia/r001/proof/render-manifest.json",
        "sha256": "69924b7a396dd25c2e3383ad98f3e0642e0b31c9627144eb38ee6f72a5c4ca30"
      },
      "sha256": {
        "glb": "6558b3cce6b208ff5e27d0fe56b4ff703ba205f187a51d9d3d178b318ac6bd5d",
        "blend": "68cc73013eae89fb96fdb9b9feeec7d2743fc5d32943498c64145921858fbdbe",
        "preview": "d34f1982867a521d5249fd04ddc0564620781bcec82af02fc3dc9246546dd5eb"
      },
      "limits": {
        "max_triangles": 12000,
        "max_materials": 8,
        "max_primitives": 48,
        "max_glb_bytes": 2000000
      }
    },
    {
      "id": "prasopora",
      "group": "marine",
      "revision": "r003",
      "source_commit": "fc2f6db4133b62e48b9764e4a33b0fd518e806df",
      "review_commit": "33dbb7c2d3deef2b0c17d2bb87daa9da2fea14cc",
      "review": {
        "path": "qa/undersea-invertebrates-concept-20261019/review.json",
        "sha256": "a83ddf9706a8b5f644fea124bc77006c0bf19cd43168d2c0ce21a2d9c9857597"
      },
      "handoff": {
        "path": "production/undersea-invertebrates-concept-20261019/handoff.json",
        "sha256": "aaceacde4cfddd0c3b19429529b8e1271b117db50e35ca252201e44f1ae39294"
      },
      "source_metadata": {
        "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/metadata.json",
        "sha256": "6976ee3b7a4980da5e3b1a4e9a1aac9daae3ac9e6ac316518fc5349a34e544c9"
      },
      "metadata": {
        "path": "assets/additions/prasopora/concept-seven-20261019/release-metadata.json",
        "sha256": "668cddbbcba727e09dc64739bd8e5242341e8fe39bf55f1c36c43c6a6de86e52"
      },
      "artifacts": {
        "glb": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/prasopora.glb",
          "sha256": "851e07d6c7b66e4e60a14cec6e153d46fbdc11a6f4f4da4480d733dddd075840"
        },
        "blend": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/prasopora.blend",
          "sha256": "3aaf9fbec27c1be0d7c02a41a21c1fb9baa1fc3b6b821c87870928e4b65cff25"
        },
        "brief": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/brief.json",
          "sha256": "526130d05b1345ec6f64b791367c537d6d71fb29b547a42325ec92e2b0a0e554"
        },
        "references": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/references.json",
          "sha256": "a8cc44a7f1bce1d7d3ab3ec0f68ea5b4645693dfdc33d5ed4eb14a7392aefe8c"
        },
        "generator": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/generator.py",
          "sha256": "2415e4b99985f644fcef9cdb64cc2d6e6e6ac6c31e8dbf6df74dea47a86372dd"
        },
        "config": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/build-config.json",
          "sha256": "a832ef1f969415233bfc1ec1f6d45cfc6c599b935683e9c53fff5638aaeaa57e"
        }
      },
      "technical": {
        "source_export": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/evidence/source-export.report.json",
          "sha256": "ff546b4243df9fc46f6efa54d89deda84b93be538a96847f34f73c199c7f792e"
        },
        "rebuild_1": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/evidence/reproducibility-1.report.json",
          "sha256": "6ed29dfc4d8765e111bbad6fa745c523364c043375fa520acba0242be8fd99ba"
        },
        "rebuild_2": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/evidence/reproducibility-2.report.json",
          "sha256": "0d11f473bc2fc603e9d7200af3bc2f12e1b4bc5568842d0d2348fc5dfe6a2d86"
        },
        "khronos": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/gltf-validator.report.json",
          "sha256": "da3f4b8bdaaafd695842936420a3f884c086019b215475691188df0cfd650d91"
        },
        "runtime_parse": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/evidence/runtime-parse.report.json",
          "sha256": "713d8c6ebb594324035a05ae550a494f35d2515eca50d2496078416dd87ba3c2"
        }
      },
      "proof": {
        "path": "assets/candidates/undersea-invertebrates-concept-20261019/prasopora/r003/proof/render-manifest.json",
        "sha256": "d893b374cc8e1915f5e1376409ed02ab675ee0c0dae4daa5eb749b4bcc8ee929"
      },
      "sha256": {
        "glb": "851e07d6c7b66e4e60a14cec6e153d46fbdc11a6f4f4da4480d733dddd075840",
        "blend": "3aaf9fbec27c1be0d7c02a41a21c1fb9baa1fc3b6b821c87870928e4b65cff25",
        "preview": "7332a560f70f6e63778c57c0ce4fb958875c599ffb85d0432eaf3cb9a2b61b58"
      },
      "limits": {
        "max_triangles": 12000,
        "max_materials": 8,
        "max_primitives": 48,
        "max_glb_bytes": 2000000
      }
    },
    {
      "id": "strophomena",
      "group": "marine",
      "revision": "r003",
      "source_commit": "fc2f6db4133b62e48b9764e4a33b0fd518e806df",
      "review_commit": "33dbb7c2d3deef2b0c17d2bb87daa9da2fea14cc",
      "review": {
        "path": "qa/undersea-invertebrates-concept-20261019/review.json",
        "sha256": "a83ddf9706a8b5f644fea124bc77006c0bf19cd43168d2c0ce21a2d9c9857597"
      },
      "handoff": {
        "path": "production/undersea-invertebrates-concept-20261019/handoff.json",
        "sha256": "aaceacde4cfddd0c3b19429529b8e1271b117db50e35ca252201e44f1ae39294"
      },
      "source_metadata": {
        "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/metadata.json",
        "sha256": "1297ab8878e18f5b93d846a6532a29166ba20e6725116cf2c5c1ce8d6da2a80d"
      },
      "metadata": {
        "path": "assets/additions/strophomena/concept-seven-20261019/release-metadata.json",
        "sha256": "bd3f32f8c104c3a437bb1515cc0978a643c4273620ca7c657fe9b0a2c2eaf02d"
      },
      "artifacts": {
        "glb": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/strophomena.glb",
          "sha256": "2880d555e1ff87e7b191a62f4b27557ab10ca5ee5c0f059701dce4e4430813ca"
        },
        "blend": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/strophomena.blend",
          "sha256": "cc40230a5c9d4f5d36846212815ec0cb334d04168307d2928a00e578b5b5a171"
        },
        "brief": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/brief.json",
          "sha256": "f053825b802d0888e55fdbce12b282ab14abbe8b93ab239481e1ae2fdf2b40d3"
        },
        "references": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/references.json",
          "sha256": "0f7be10de9be917ed9b1f540bba55d6a8f4bbc6232d22bc9e9db24dbcbfcf4c5"
        },
        "generator": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/generator.py",
          "sha256": "8a443adcfbf70670c7e9a0303e19661a130297f3265ecf251202521b4a198d07"
        },
        "config": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/build-config.json",
          "sha256": "c06c635ab9eef135ada99ca27de8977c3d6e1a0e5fca13e993287bc417d1fe32"
        }
      },
      "technical": {
        "source_export": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/evidence/source-export.report.json",
          "sha256": "2d9ce26664f6903406e926e2bdb23104987dd76db1b63859ffd16760e5ee2fc8"
        },
        "rebuild_1": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/evidence/reproducibility-1.report.json",
          "sha256": "fc24b43ea68743fc38976d1a641116f189a88a9539f8ecf06159e322affa221b"
        },
        "rebuild_2": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/evidence/reproducibility-2.report.json",
          "sha256": "b1c965c96ba839ef787eef70cb3dbeeaa25ccc6fe3fcdb9716e29e8651df4ab5"
        },
        "khronos": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/gltf-validator.report.json",
          "sha256": "02de7c9738bf1d3501fd6d3f9cf3481d32a9fbaa487d0375b7298a2c53c01f7b"
        },
        "runtime_parse": {
          "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/evidence/runtime-parse.report.json",
          "sha256": "5e729c22d0fd539e4badd3f22e1d5bf4aa4e5cbc0561adfd67567de79d7f727d"
        }
      },
      "proof": {
        "path": "assets/candidates/undersea-invertebrates-concept-20261019/strophomena/r003/proof/render-manifest.json",
        "sha256": "8e624ac98e4bd716aa0b4b5f5161be8666da618045e2c625209c070a8f13bbaf"
      },
      "sha256": {
        "glb": "2880d555e1ff87e7b191a62f4b27557ab10ca5ee5c0f059701dce4e4430813ca",
        "blend": "cc40230a5c9d4f5d36846212815ec0cb334d04168307d2928a00e578b5b5a171",
        "preview": "23a81a4d6e9b62ff35a96323dc2c45600a40541508b7f93618b50d0f75e24579"
      },
      "limits": {
        "max_triangles": 12000,
        "max_materials": 8,
        "max_primitives": 48,
        "max_glb_bytes": 2000000
      }
    }
  ]
};
