/** Immutable accepted payloads and independent evidence; original candidate failures remain explicit. */
export const ACCEPTED_ROUND07_ASSETS = {
  "cooksonia": {
    "id": "cooksonia",
    "batch": "19",
    "source_commit": "5d137441d8ee2a20fcf5ef96a98e3e1c2ec178dc",
    "review_commit": "69272b5ae67479c021a778adcf471e23d8cd4159",
    "handoff_commit": "5d137441d8ee2a20fcf5ef96a98e3e1c2ec178dc",
    "review": {
      "path": "qa/continuous-small-life-round07-20261018/batch-19/independent-review/review.json",
      "sha256": "a51400253de693e64a0b8c22b7fe41cad2b08b2447a0cb428e87cbcc77ee063c"
    },
    "candidate": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/candidate.json",
      "sha256": "dd0f86d7c38a75e183aeafa0fefae7f51637447c199c3385e865f492ff307106"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/metadata.json",
      "sha256": "8da1aab0f44a6dce9fe79d83b030af47d7080771b621be9e655bad5b7c3fba93"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/cooksonia.glb",
      "sha256": "9f0a98a40646df280257f0f0049dd71a260d0c05056d2e97383f45f974fbb5c0",
      "bytes": 114504
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/cooksonia.blend",
      "sha256": "b296dd083342a3134e933d252a8a77faf900e75a0b8dd57fbe7377be3f03cf18",
      "bytes": 734068
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/view-manifest.json",
      "sha256": "0059c1a0063856b51e824723c922144c7c92ab3e9a58e39bf2ba577312c533d6"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single.json",
      "sha256": "1ba0b0a10a774027fd19bb965524544f09ed49f82289a809a0bdadc5cc478a03"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/scene.json",
      "sha256": "ea4974269479d04e5cced2ded96e4a3af58093529ec010921e4dc421b7b2a271"
    },
    "source_export": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/source-export.json",
      "sha256": "c9546244e038210765dd676594f1e6145f9bcc00ef3e83e093fc2203016d305d"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/gltf-validator.report.json",
      "sha256": "9424dc374bbb215e79089a188853dabf81452d356249ad79f1e974a7472eae71"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/candidate.json",
        "sha256": "dd0f86d7c38a75e183aeafa0fefae7f51637447c199c3385e865f492ff307106"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/cooksonia.glb",
        "sha256": "9f0a98a40646df280257f0f0049dd71a260d0c05056d2e97383f45f974fbb5c0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/cooksonia.blend",
        "sha256": "b296dd083342a3134e933d252a8a77faf900e75a0b8dd57fbe7377be3f03cf18"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/generator.py",
        "sha256": "fa672438446409f95aa8fe80ea1e38524143903308cad4e11454b9662a33c782"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/config.json",
        "sha256": "ad48613bc3ced9a7ccd7a74cf9c551f3974ad6a6f95747273b3ff29391355c15"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/items/cooksonia/brief.json",
        "sha256": "bb61fa06e70907702f3c7f56e762fa78bcbefc125f80446f67c67122319d8bab"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/references.execution.json",
        "sha256": "2a742c06f8e1efa3762a61b897619273666ad89df6487d80a23f7145fc39d8d8"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/items/cooksonia/references.json",
        "sha256": "23883b7c2636ba3fbdd4a2e9d064c9ee6f4dcbbcf80463cdcbc44adf94d40e1d"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/cooksonia/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/cooksonia/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/viewer.html",
        "sha256": "3b97da246abca0281a4931ae53f2538993e3e58c5f4998eda43bc44b0af14d0c"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/browser_qa.mjs",
        "sha256": "6fc8b10594d616bd79e6c732c20220f728178e4a6496ba22ba4e06c7de4f2f6f"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/verify_item.py",
        "sha256": "cabf62a98ccf515f905bff48a96cb5009d287a57beb1cdad160fb4923a1f468a"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/cooksonia/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/reference-access.json",
        "sha256": "2e1875382bfc0145ba75a6e98d9dc6e434c7581f96dcdb14d435e866eb995d9c"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/claim.json",
        "sha256": "243576661c73e1fea9e462635c3ff97902f07f81710237fec1605c58407ab457"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/gltf-validator.report.json",
        "sha256": "9424dc374bbb215e79089a188853dabf81452d356249ad79f1e974a7472eae71"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/source-scene.json",
        "sha256": "012ee7f44d5a55dcdd8a85a884b18e87e4b03fe63f502860194b725087f56430"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/source-export.json",
        "sha256": "c9546244e038210765dd676594f1e6145f9bcc00ef3e83e093fc2203016d305d"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/reproducibility.json",
        "sha256": "7eaf9f4f0f72897042ee9f88c04e4fa5c3f3ca7899085fa03fb96fa1bdbc3a5f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single.json",
        "sha256": "1ba0b0a10a774027fd19bb965524544f09ed49f82289a809a0bdadc5cc478a03"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/scene.json",
        "sha256": "ea4974269479d04e5cced2ded96e4a3af58093529ec010921e4dc421b7b2a271"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/view-manifest.json",
        "sha256": "0059c1a0063856b51e824723c922144c7c92ab3e9a58e39bf2ba577312c533d6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/metadata.json",
        "sha256": "8da1aab0f44a6dce9fe79d83b030af47d7080771b621be9e655bad5b7c3fba93"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/qa.json",
        "sha256": "83230a9422ce19b3bf1fff1d661cc46778a53a4deb554cd5a4645201f1067c86"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/freeze.json",
        "sha256": "bc15801c2d522fe8ad0d55beb7cf23535d306002acd36f5d34c2083eac29069c"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/practical-integrity.json",
        "sha256": "9b52eb8cd16e3871c3d8b900fb119d40b8e57b85b9a502501f348638c6394f98"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/profile-contract.json",
        "sha256": "d67a6d5b248cddbaa16c4033483c7ba88b209083bc50387aa89c4560d3ef34fb"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/profile-gate.json",
        "sha256": "b3fe73be92eb17ef14ae921616277e96e092db8767c33420407f42c906f8bd18"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cooksonia/r001/legacy-gate.json",
        "sha256": "e6038710827c033b6dccbbda3d5b97bc994b2533649d1218277c271508034ac8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/source-contact-sheet.jpg",
        "sha256": "30ef193132011f29158e9fe66e0b9d719ab1b55858fe7e7e746922d10302650c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime-contact-sheet.jpg",
        "sha256": "83f2c7cc8374aae8b710c81b664388289472a50cb7a9afdbe8ff1403d9336eaf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/preview-hero.png",
        "sha256": "56b02182a010a09c8d399b97709a3757f323b8d04e91ed5a23f4e637cb919dc0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/preview-reversehero.png",
        "sha256": "f038398808f6d1c32ae3e1d529c0554e8547f5c4ea30ca9d854788def0d0ed71"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/preview-front.png",
        "sha256": "7304bb50462e310c08a36364bc83e88f39e2ea152bb40dab419657be9cec8cd2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/preview-side.png",
        "sha256": "cf9b0fac2466dcc70e8a0a2b95b6a48e17fd9976163fb54fca721daeab482dee"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/preview-rear.png",
        "sha256": "4d11280b2c129bcbc314581cee6848e9663fa00c640c1d3d56038bb4a21f6c7a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/preview-top.png",
        "sha256": "701ee5e0601529d057108292bddef26e8999c6f415eeff3af092f304522b9ad4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/preview-clay.png",
        "sha256": "83e3a73a9ae3ca5db11928430a34d80a1b60a055cea9175bc9ff986432387b6a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/preview-silhouette.png",
        "sha256": "fdb863380463fd09d11fca884aa000767a338a467a0deae89f76c0f99629e69d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-hero.png",
        "sha256": "97d15ddfe6bef2f1940fd6c91db7637d52426041e4f01d71f18bda69188803a1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-reversehero.png",
        "sha256": "2e7501e79abbef734b4e3a5dedcd4094549430fa517de4a02eb48b67c348b9ea"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-front.png",
        "sha256": "3c07a4c9940b7c27a2ba04685262351560a4b91efa7f2fad2ec6d66f729c3a4d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-side.png",
        "sha256": "89328dc75a0307d5be7d8790eb6abc99409c83b0862ffbe4043b03a5c5fae043"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-rear.png",
        "sha256": "abed734fa273995a11e5714c53a250c0c717d7dd00e183217db3b0ddaf44bf63"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-top.png",
        "sha256": "ddccbf9242b2c8ede515c2a66965208154c48d3769f49ddb2328b555f1507db3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-bottom.png",
        "sha256": "35b1115e1da73048fe6a8d40ca22203f4782ca4dc5c3ea5829ce71c7b711e45b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-80px.png",
        "sha256": "2b8da0de7dfd47992f9e41c68188decbfb010edda108d0417cfad8c874f8b821"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-160px.png",
        "sha256": "ce58e31836354db1b1610bbe4192b0f0c6ae31be30defea6cd6c17e5341c2677"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/single-240px.png",
        "sha256": "9d958d3b7076d19d778244efc8e54f62e6e2d73bfd9e2455072fee8467592c14"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/scene-hero.png",
        "sha256": "2317e148c4a1d6c8c5ebad53baea0367870a22a2323d7ee83ea80d75e0469155"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cooksonia/r001/attempt-01/cooksonia/runtime/scene-top.png",
        "sha256": "29aed07cdf89b34935fa63a42bf440708b764a8681d04c63c33d9b1a5e832362"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/cooksonia/candidate.json",
      "sha256": "6220fa506c7b02fb094d060880d70465bdf817636fed3cf1333837def66b76d0"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/cooksonia-contract.json",
      "sha256": "0e3675fec6980060403026b3bfc1ba678acadcccf14297dff2d3346a28e24644"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/cooksonia-result.json",
      "sha256": "c51d3c4fdcc036eb52c7570a74d377149748ad446bb1ecfbb78b9a9b2d532e4d"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: independent-acceptance-pending",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/cooksonia-original-legacy.json",
      "sha256": "e6038710827c033b6dccbbda3d5b97bc994b2533649d1218277c271508034ac8"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-19.json",
      "sha256": "13b54008b926040873d5ea05ec306fe94f53521b6139c334b18bc5bf7f415a1c"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/HANDOFF.json",
      "sha256": "a92c9f5954edad46d167ed8f967095374266568d15d3d3a9bff429cdabd4b4bf"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/cooksonia.json",
      "sha256": "75173eaaf5d3e9964072e7ccda282e4ae1a510b37fbb57d387e47fb588024828"
    },
    "dependencies": []
  },
  "cambroraster": {
    "id": "cambroraster",
    "batch": "19",
    "source_commit": "5d137441d8ee2a20fcf5ef96a98e3e1c2ec178dc",
    "review_commit": "69272b5ae67479c021a778adcf471e23d8cd4159",
    "handoff_commit": "5d137441d8ee2a20fcf5ef96a98e3e1c2ec178dc",
    "review": {
      "path": "qa/continuous-small-life-round07-20261018/batch-19/independent-review/review.json",
      "sha256": "a51400253de693e64a0b8c22b7fe41cad2b08b2447a0cb428e87cbcc77ee063c"
    },
    "candidate": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/candidate.json",
      "sha256": "8e289be06eb3c68edb299f71ac4394322ff2186cf5cc186e38694f844e8f7965"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/metadata.json",
      "sha256": "325e822fcd6cbc7773a142246fa14f100566c8d5973608102e290d2b849a8fa3"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/cambroraster.glb",
      "sha256": "c8662370a1b676ee7f2b0c12c8b93e8aa8f38a867b375001ac4cb7c5b3f1e86e",
      "bytes": 192668
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/cambroraster.blend",
      "sha256": "921bf7ed3788c150ba90254b408ae5e28f7155f485520b9895b99c800eddf7b9",
      "bytes": 928332
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/view-manifest.json",
      "sha256": "64ff43a0fd272d39cd1b63da5de7167c21072f09d01b793fffcf815f8c6d46a9"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single.json",
      "sha256": "0a735728d4f3492f6eaaeef99a31378ec8c287c15b8cdbacbde956e76c743781"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/scene.json",
      "sha256": "007056d11a4d607d182a8af8bf6fa129c898f3d23e610eaafbbfb5273803e06f"
    },
    "source_export": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/source-export.json",
      "sha256": "5d0244da64bfc1b76dbef94af1fb2eab1f1be89e56d53fe175457e88f229f533"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/gltf-validator.report.json",
      "sha256": "9a83bc3a8fef1f5dfada635dc3fa979d36f0a1a14203f6ae167c3bfe304523d0"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/candidate.json",
        "sha256": "8e289be06eb3c68edb299f71ac4394322ff2186cf5cc186e38694f844e8f7965"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/cambroraster.glb",
        "sha256": "c8662370a1b676ee7f2b0c12c8b93e8aa8f38a867b375001ac4cb7c5b3f1e86e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/cambroraster.blend",
        "sha256": "921bf7ed3788c150ba90254b408ae5e28f7155f485520b9895b99c800eddf7b9"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/generator.py",
        "sha256": "1bddce5fed82965cd7b55ecf2d11dbb7283da8b6fbbc66b2c785049b0b6caf0f"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/config.json",
        "sha256": "527c273e15edc8dd90f8a0108a99701282d0fde3bc7f03b2bd7210bba3fb5fea"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/items/cambroraster/brief.json",
        "sha256": "43abf62a4d7439e6237e19b4bcf8776fbf73a117e02cda9c3e75adb5e4c6ea42"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/references.execution.json",
        "sha256": "41aedab5427087e786a6f8a42d778a9090405f840f5d8cf7d11ff10684881596"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/items/cambroraster/references.json",
        "sha256": "78d4a0f23bc393d8a048dfeefb624bfee71a0d770cbe713ddb02051cfcb361ef"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/cambroraster/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/cambroraster/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/viewer.html",
        "sha256": "fe3bcfd52eb247d2fbb91da0426c870a4bff7d30b7e6bdd6a30538791f4346df"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/browser_qa.mjs",
        "sha256": "c661961636d178d1a38fd5424e12da4df5df8220fc3940d619371dccba8ccda0"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/verify_item.py",
        "sha256": "c2aa4eb35f8f879149b679eee4d1a308fa1b1b3fb9a4338583dda456a74ac5c0"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/cambroraster/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/reference-access.json",
        "sha256": "2e1875382bfc0145ba75a6e98d9dc6e434c7581f96dcdb14d435e866eb995d9c"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/claim.json",
        "sha256": "243576661c73e1fea9e462635c3ff97902f07f81710237fec1605c58407ab457"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/repair.json",
        "sha256": "df091a00eea19d35f61f61ca7c7836e9436dd41157d1a982c6d3bef7f8dc4bd4"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/execution-interruption.json",
        "sha256": "4adccb462d536b8c72a2e3d0698a91b408fd07cbf47070b24c39ed98cd6cde9e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/gltf-validator.report.json",
        "sha256": "9a83bc3a8fef1f5dfada635dc3fa979d36f0a1a14203f6ae167c3bfe304523d0"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/source-scene.json",
        "sha256": "c817f89227292750ec425f8fb4e3e4e49a0363c1d44ea4c2e077d4d399f275fa"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/source-export.json",
        "sha256": "5d0244da64bfc1b76dbef94af1fb2eab1f1be89e56d53fe175457e88f229f533"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/reproducibility.json",
        "sha256": "91e88ccce300b47d1718d759fee62deb77f8b1f97061dfe45bbdeb0507bb8414"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single.json",
        "sha256": "0a735728d4f3492f6eaaeef99a31378ec8c287c15b8cdbacbde956e76c743781"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/scene.json",
        "sha256": "007056d11a4d607d182a8af8bf6fa129c898f3d23e610eaafbbfb5273803e06f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/view-manifest.json",
        "sha256": "64ff43a0fd272d39cd1b63da5de7167c21072f09d01b793fffcf815f8c6d46a9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/metadata.json",
        "sha256": "325e822fcd6cbc7773a142246fa14f100566c8d5973608102e290d2b849a8fa3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/qa.json",
        "sha256": "5629d76b66df60b0db89e3c32b895b6363436350664fb2de887c752aa368b042"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/freeze.json",
        "sha256": "59029f3aae73f23610218a3ebda4195814fae24e7ad36859d656fcc359b6eee9"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/practical-integrity.json",
        "sha256": "7cb571ffdfdb86ae7ffce234c15e9076d4eefc0b6d0232ee404e96fdcaed041e"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/profile-contract.json",
        "sha256": "f166bf7bc3bfb94fec78df192b3b917f783c4184df2308378d00ad1ae91a4945"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/profile-gate.json",
        "sha256": "b006931cd1da37bc8a9b519d76353f04caa12ce67d9ea2a93ba0595470de19e1"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/cambroraster/r002/legacy-gate.json",
        "sha256": "5eb7886b7dcb98733f91fcd3f9debe2bd7dbf459b5bbf8161c98e7f0d60deae7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/source-contact-sheet.jpg",
        "sha256": "1fd7c0bd141ac42763704264694f1bd6333179e71c2f5a375e0ad8788703029c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime-contact-sheet.jpg",
        "sha256": "e5bb0afb4746412e37e9f73f274cbae0c2ec3eecf18f3800a783b7b147e84633"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/preview-hero.png",
        "sha256": "4f878b8aad59fce97ba020ce489964bf9d84921f3756f46200b7c89d1bc95435"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/preview-reversehero.png",
        "sha256": "239f1f3b820f3f0fc09e93adfa43570ee00fce5ac4660ba05fbd2f60050f7598"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/preview-front.png",
        "sha256": "93ba6115f11b2b7be7805ef8fb8d064867f62ca77c3c272cc1d0e86b97ad41b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/preview-side.png",
        "sha256": "38243ac30301e5e18dccdea1471e554a8caade60445ecae53f42a63ba83224c4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/preview-rear.png",
        "sha256": "be7d70f6ab3231dc4fda736934c77f9a421e5460b85de6b4e56e5051636c493a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/preview-top.png",
        "sha256": "4432f80f19c149c58788c52969865123fbdd59e38e71035bff278981ab2306a4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/preview-clay.png",
        "sha256": "9a5bf3c372459562bbfff821eb1369b9daad0621882b4b995d80a1c11bdb5827"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/preview-silhouette.png",
        "sha256": "456f5176c7a7762baba5319ca00f244ef2b638dffa505de44e6acf988b005fe6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-hero.png",
        "sha256": "dae0b22604780dd098ac532a98fb5c87df7d0daf207a321bba5443dc6cf16f80"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-reversehero.png",
        "sha256": "9c3b1a7d73c34fbd5ebe7f2edad92be645ddcad1905e2f7366fd924422b2fe0e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-front.png",
        "sha256": "d1c16043c1e57aadc74654f97b569be207ac0cdbe3d207db3e3fa3e19ca1af00"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-side.png",
        "sha256": "4c2a0f37fe5ba2e78261e0bc1dcfde6df0e866950d5ace507f2af392b56f00d5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-rear.png",
        "sha256": "11e6214b8556e6e1f7b598a85015b14fd80ac7e7418f45138dac94ae78cee803"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-top.png",
        "sha256": "d689f4a339c6cf5c601c8728f3b2286bc757b8bbe2d5da1112895827586a6bba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-bottom.png",
        "sha256": "3e0c6c3836c0a6910db8f91a8245f662b4c64f3ef087c69e85e52d22ff499b98"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-80px.png",
        "sha256": "6a174cbcfbdb49d529f017f89506f6da4e37fee2ceccb92f3fc9276f5d583822"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-160px.png",
        "sha256": "02d32dcf07ce235a761250a505edab0417485e52961f8cc4bfa329cfde31d45b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/single-240px.png",
        "sha256": "f96f4d68d3decbfa7b84e7cdf3f3e212b4afcbbaae7bca52032a96f77dcec466"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/scene-hero.png",
        "sha256": "42d0d606af10c7c2034e25d694a26edd13d2af1c9c2a4977ed950787442df202"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/cambroraster/r002/attempt-01/cambroraster/runtime/scene-top.png",
        "sha256": "0f36db950821b6207ac9dc0279b93d4b483a60d6ff817159cb9ebae7d5e13632"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/cambroraster/candidate.json",
      "sha256": "30707a04283350001f2b0adabf4f7d7e00f3e9ed2f2e119fa23672ef0434974c"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/cambroraster-contract.json",
      "sha256": "b3d5848317d586fef29b7eab26cf98457fb5f47f6ca61a6cfb221770341dbadd"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/cambroraster-result.json",
      "sha256": "c412ae9750025ced43f4d52a99ccb9ccea7d2a7a23b2b05641c88128b3e52a49"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: independent-acceptance-pending",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/cambroraster-original-legacy.json",
      "sha256": "5eb7886b7dcb98733f91fcd3f9debe2bd7dbf459b5bbf8161c98e7f0d60deae7"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-19.json",
      "sha256": "13b54008b926040873d5ea05ec306fe94f53521b6139c334b18bc5bf7f415a1c"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/HANDOFF.json",
      "sha256": "a92c9f5954edad46d167ed8f967095374266568d15d3d3a9bff429cdabd4b4bf"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/cambroraster.json",
      "sha256": "723f0ceee7be78b16db15892ff45ec794dd1b12a13867c1cbaaa201fa124591c"
    },
    "dependencies": []
  },
  "bedrock-pothole": {
    "id": "bedrock-pothole",
    "batch": "19",
    "source_commit": "5d137441d8ee2a20fcf5ef96a98e3e1c2ec178dc",
    "review_commit": "69272b5ae67479c021a778adcf471e23d8cd4159",
    "handoff_commit": "5d137441d8ee2a20fcf5ef96a98e3e1c2ec178dc",
    "review": {
      "path": "qa/continuous-small-life-round07-20261018/batch-19/independent-review/review.json",
      "sha256": "a51400253de693e64a0b8c22b7fe41cad2b08b2447a0cb428e87cbcc77ee063c"
    },
    "candidate": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/candidate.json",
      "sha256": "a7c46b2e4696413325300acc3ca5a434471438a8b19ab845c11224b67631af1a"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/metadata.json",
      "sha256": "9dd47f6fd694bff6b1251c4573a3b9ee15963e20bb41beb743bda90a64b9aeae"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/bedrock-pothole.glb",
      "sha256": "182f30ba029ddf8acb131c82018613178f40f447582baac16d37513600e78420",
      "bytes": 141884
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/bedrock-pothole.blend",
      "sha256": "d33e12bd47d92e3fee7ead0caf9c8d6a3748b5a8ad228eac144c32492b0fda01",
      "bytes": 737408
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/view-manifest.json",
      "sha256": "4b4ab8b598e9396d7d8b8c02ed1911d7c1f74167bc6786dc6a20863253103616"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single.json",
      "sha256": "dc52888b169acf7f6b8a40753ff8da95f074ee10c453511d59f25eef2078a583"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/scene.json",
      "sha256": "4b50058613bdb22e746b73cf8747ced48b8459087cdc39eaef7cd21cc776868c"
    },
    "source_export": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/source-export.json",
      "sha256": "4f93d4c5aa2016deb5591786436b67d955f80e424da93d99a08d975bf94a4c4b"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/gltf-validator.report.json",
      "sha256": "e715cbc8bfa1c1f34a68ff4e5f5e9cb7e6351468467c86c21d6bf1e9821edf97"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/candidate.json",
        "sha256": "a7c46b2e4696413325300acc3ca5a434471438a8b19ab845c11224b67631af1a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/bedrock-pothole.glb",
        "sha256": "182f30ba029ddf8acb131c82018613178f40f447582baac16d37513600e78420"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/bedrock-pothole.blend",
        "sha256": "d33e12bd47d92e3fee7ead0caf9c8d6a3748b5a8ad228eac144c32492b0fda01"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/generator.py",
        "sha256": "441fde42801ca6e82c66d6ef614842ee3a4029096ece74ad81298f6083bec997"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/config.json",
        "sha256": "850c6f8cb6d1dc69a3cead91fa673c2c35c3b09eaacb1ac3686e03010f38bced"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/items/bedrock-pothole/brief.json",
        "sha256": "afbb70eb22394b14f3d271919e740702d7f3abab2d56ee4b7ad711e24ce2c546"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/references.execution.json",
        "sha256": "c03e19874edad493a326c95277e066d7412e9b2b283c84196186b329274b2f48"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/items/bedrock-pothole/references.json",
        "sha256": "fe8de94caf71a6838c6d268b7c1dc5ece2f0ec296a2f6760a3b714a18e3aa5e5"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/bedrock-pothole/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/bedrock-pothole/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/viewer.html",
        "sha256": "3b97da246abca0281a4931ae53f2538993e3e58c5f4998eda43bc44b0af14d0c"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/browser_qa.mjs",
        "sha256": "6fc8b10594d616bd79e6c732c20220f728178e4a6496ba22ba4e06c7de4f2f6f"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/verify_item.py",
        "sha256": "cabf62a98ccf515f905bff48a96cb5009d287a57beb1cdad160fb4923a1f468a"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/bedrock-pothole/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/reference-access.json",
        "sha256": "2e1875382bfc0145ba75a6e98d9dc6e434c7581f96dcdb14d435e866eb995d9c"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/claim.json",
        "sha256": "243576661c73e1fea9e462635c3ff97902f07f81710237fec1605c58407ab457"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/gltf-validator.report.json",
        "sha256": "e715cbc8bfa1c1f34a68ff4e5f5e9cb7e6351468467c86c21d6bf1e9821edf97"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/source-scene.json",
        "sha256": "15da475556858b20f278cae29716d1cde79cc0131a8af0820cda9ee1eb806f44"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/source-export.json",
        "sha256": "4f93d4c5aa2016deb5591786436b67d955f80e424da93d99a08d975bf94a4c4b"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/reproducibility.json",
        "sha256": "0a86326c4cc334a9d6498987fd3031b28731489afb338d80ab5c7f7637713257"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single.json",
        "sha256": "dc52888b169acf7f6b8a40753ff8da95f074ee10c453511d59f25eef2078a583"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/scene.json",
        "sha256": "4b50058613bdb22e746b73cf8747ced48b8459087cdc39eaef7cd21cc776868c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/view-manifest.json",
        "sha256": "4b4ab8b598e9396d7d8b8c02ed1911d7c1f74167bc6786dc6a20863253103616"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/metadata.json",
        "sha256": "9dd47f6fd694bff6b1251c4573a3b9ee15963e20bb41beb743bda90a64b9aeae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/qa.json",
        "sha256": "a5dd48b342ef586e0f46dc29f84755741a261f0cde24078ff4c27f97d0f27ebf"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/freeze.json",
        "sha256": "d60e14a3c1b13bec0d44ddcf323e7ee6fa7a761c563c66c589795e50d9d9fa38"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/practical-integrity.json",
        "sha256": "8782cb2c950bd2480f0d5b3a71610105d545d7f2c682ee05756119d1efbc0aa6"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/profile-contract.json",
        "sha256": "7e1530e7be243ce060e256837da83ad4a9d70a6f022b311e419f9bd6a8a868ea"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/profile-gate.json",
        "sha256": "1642340751c1258635073cd3efdc71a8b0e62c617617fdb0e8765a5c6ce96e01"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/bedrock-pothole/r001/legacy-gate.json",
        "sha256": "26d90cdf3c0e354e8904a4e9265a50b61993b0ae87dd5109ed08bc7ebb95982f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/source-contact-sheet.jpg",
        "sha256": "c35f8218fdae544000c6fa54764834c509bdb1f22896f8578b562428af6985cd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime-contact-sheet.jpg",
        "sha256": "d0b047e9b41e27a605959b3a4ce84e58404880b8b7612b73b627ff77b1c696cb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/preview-hero.png",
        "sha256": "ce52a913820a738d952f7cb81d8bbadddd720e4ae57a6ba21171ef881bf3ebf5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/preview-reversehero.png",
        "sha256": "a07e224c82b8facf166b4f98610ba4a612cde6b9a9f1f792376e9b722316b642"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/preview-front.png",
        "sha256": "feaf3dff7b2a76a3d86fd443428770754087ecbc7f4d4d09442171aab72eb5be"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/preview-side.png",
        "sha256": "559bcab539599c071688f0460db7794df2e784b29454164584ae87489308cd54"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/preview-rear.png",
        "sha256": "bc2adffb5ca755fc6c675767f8073f97be64f83786c74586e7434b71e98e1cb1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/preview-top.png",
        "sha256": "4f7f3751b18a2a66e863cd4bfa9a3be94b2b25e69fcaadd5d02fa8e81183e1be"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/preview-clay.png",
        "sha256": "934158d2ef71bf14156d7e5b62a671debaafbcadcb2cccc6db47328c2159d627"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/preview-silhouette.png",
        "sha256": "6943ea22473bb7eba729d035c66fc466c9e78d43e0cd68c24ef9022dc9d53abb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-hero.png",
        "sha256": "09339e4bdb0d4654d5e42791c0ae3f20e18edc07d846b96e75a237e68f7a3876"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-reversehero.png",
        "sha256": "69b30b47b0d8933251207b361ba5f606b7ee91850be07c5d743a0b710474267c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-front.png",
        "sha256": "50b1d67f62d0ca34408726ee7f8dde2129de9cd8e1330b9cb6a1297f38b78b83"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-side.png",
        "sha256": "6d2d4d48921261c8d34fa9c73d31a6a9e7f853700ad4aaaff5f0a3e4249ae84b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-rear.png",
        "sha256": "83612e5fc8915eec17f5be8a61310cc8b1500d4da2b99750fe0448476fcadbd2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-top.png",
        "sha256": "690a70e3c4b67a4fb02f011fc63f3b18d642b8d02d949b187a5942c6fea7e61f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-bottom.png",
        "sha256": "5ab3f2a2b2c046ceab7d163c9efff2a604a0f49457f87a12e232ad8c8e8a3073"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-80px.png",
        "sha256": "dda7c21ce85db590bf87d61b0d7ac098bb58e6a5f566ffc1575a18f37ad53acc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-160px.png",
        "sha256": "89afd22abba9b654d17c808e1866dcb7d6f594b5ff99816e63661f566dbb6778"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/single-240px.png",
        "sha256": "66a5a22e4c9e34aab83f82d96ab1151f03ede7043b62959f8e3d2d90d55aceab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/scene-hero.png",
        "sha256": "6418d0fb8ff5736267a9c45d8e2470fcdd7ce02458dda8db0481f72dbeb5187f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/bedrock-pothole/r001/attempt-01/bedrock-pothole/runtime/scene-top.png",
        "sha256": "d06469b0607ecf97f3943b34a62bc69d6f6670e9d3cde430a704219c007f6abc"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/bedrock-pothole/candidate.json",
      "sha256": "61df895f8f6119e1299508329749e23c8d66e93712936407ac6467959e99a8a1"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/bedrock-pothole-contract.json",
      "sha256": "6d50feb418ae295aaa23b064c42aec2a6ec3275a7617b31699063ca040336f25"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/bedrock-pothole-result.json",
      "sha256": "f180f9d14e7382b520c7aabe99b001157bc731fcd40d803c4ad998be9fcf126a"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: independent-acceptance-pending",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/bedrock-pothole-original-legacy.json",
      "sha256": "26d90cdf3c0e354e8904a4e9265a50b61993b0ae87dd5109ed08bc7ebb95982f"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-19.json",
      "sha256": "13b54008b926040873d5ea05ec306fe94f53521b6139c334b18bc5bf7f415a1c"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/HANDOFF.json",
      "sha256": "a92c9f5954edad46d167ed8f967095374266568d15d3d3a9bff429cdabd4b4bf"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/bedrock-pothole.json",
      "sha256": "5001cfba927cce887b74e56934499f348810e1246c7457cb70739524abfa3d6f"
    },
    "dependencies": []
  },
  "quartz-prism-cluster": {
    "id": "quartz-prism-cluster",
    "batch": "19",
    "source_commit": "5d137441d8ee2a20fcf5ef96a98e3e1c2ec178dc",
    "review_commit": "69272b5ae67479c021a778adcf471e23d8cd4159",
    "handoff_commit": "5d137441d8ee2a20fcf5ef96a98e3e1c2ec178dc",
    "review": {
      "path": "qa/continuous-small-life-round07-20261018/batch-19/independent-review/review.json",
      "sha256": "a51400253de693e64a0b8c22b7fe41cad2b08b2447a0cb428e87cbcc77ee063c"
    },
    "candidate": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/candidate.json",
      "sha256": "4ac19a0f4baae2be138f6bd59039f7e0871b65a439972b6d12b250aa789563c9"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/metadata.json",
      "sha256": "440cf73c2942f0e9ab9c59e5a39a5d7ede706bbf6b085d630ea072c3448e0588"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/quartz-prism-cluster.glb",
      "sha256": "6efded4938f08ad789a4a3f409a45b6e178c243d998aa6ae50b72bef02b17044",
      "bytes": 58392
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/quartz-prism-cluster.blend",
      "sha256": "aedb083438c72ccea5c8326be631f54d7398de1be79d8745c3679b08f597df75",
      "bytes": 541548
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/view-manifest.json",
      "sha256": "d5ba86a8ff40225d68829c1e3660e33896015588f2c02971263007e0cf574b5c"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single.json",
      "sha256": "167ea2d3295e6b0e993bed938767fb95aaed7a7a4c4c30bb6775ed00086104a1"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/scene.json",
      "sha256": "659a07f00716e164c32d855f177599ae067053f0c1b7b84d17d391286d8187a2"
    },
    "source_export": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/source-export.json",
      "sha256": "44d21c7a47265c1da9859bc280c888163ee64f10255238b140bb04dfe53208fa"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/gltf-validator.report.json",
      "sha256": "aada278006945d059ab696f7583bbddf99532c13ca3cfb04dd4a6ce3cc7d8c29"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/candidate.json",
        "sha256": "4ac19a0f4baae2be138f6bd59039f7e0871b65a439972b6d12b250aa789563c9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/quartz-prism-cluster.glb",
        "sha256": "6efded4938f08ad789a4a3f409a45b6e178c243d998aa6ae50b72bef02b17044"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/quartz-prism-cluster.blend",
        "sha256": "aedb083438c72ccea5c8326be631f54d7398de1be79d8745c3679b08f597df75"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/generator.py",
        "sha256": "c0cffb8eac84b61dd08c01ffa0c33a9a86133e0d7f2d24f4801c84ccdda62a68"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/config.json",
        "sha256": "97a97c9b011f0d849d4d92cc7852be7d2122b9f43b6d20b5c8d598c281d147f0"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/items/quartz-prism-cluster/brief.json",
        "sha256": "f535ad5ab1700f911bd5d4ec1f3aa2e4837bfc258444ee665997ec2bf00fc248"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/references.execution.json",
        "sha256": "691420b9de7ce038045d4cd568b0460aacc501d9488e9694562aa754e43e44bf"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/items/quartz-prism-cluster/references.json",
        "sha256": "aa38b9c0e0dbc3af0b179278e1388b7427bd43e8205dae055030275df003a5bd"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/quartz-prism-cluster/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/quartz-prism-cluster/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/viewer.html",
        "sha256": "3b97da246abca0281a4931ae53f2538993e3e58c5f4998eda43bc44b0af14d0c"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/browser_qa.mjs",
        "sha256": "6fc8b10594d616bd79e6c732c20220f728178e4a6496ba22ba4e06c7de4f2f6f"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/verify_item.py",
        "sha256": "cabf62a98ccf515f905bff48a96cb5009d287a57beb1cdad160fb4923a1f468a"
      },
      {
        "path": "production/continuous-release-round07-20261018/source-snapshots/quartz-prism-cluster/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/reference-access.json",
        "sha256": "2e1875382bfc0145ba75a6e98d9dc6e434c7581f96dcdb14d435e866eb995d9c"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/claim.json",
        "sha256": "243576661c73e1fea9e462635c3ff97902f07f81710237fec1605c58407ab457"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/gltf-validator.report.json",
        "sha256": "aada278006945d059ab696f7583bbddf99532c13ca3cfb04dd4a6ce3cc7d8c29"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/source-scene.json",
        "sha256": "35cf4492eca8a4418b52e0d4f3e162acc8cf3b2cd57e4d69c9fbaaa3b2268b1d"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/source-export.json",
        "sha256": "44d21c7a47265c1da9859bc280c888163ee64f10255238b140bb04dfe53208fa"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/reproducibility.json",
        "sha256": "929be0b6faa343b4b3dbf9106bb52b3657ea7108c6ce9b821f0cbcfa4eb99ae8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single.json",
        "sha256": "167ea2d3295e6b0e993bed938767fb95aaed7a7a4c4c30bb6775ed00086104a1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/scene.json",
        "sha256": "659a07f00716e164c32d855f177599ae067053f0c1b7b84d17d391286d8187a2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/view-manifest.json",
        "sha256": "d5ba86a8ff40225d68829c1e3660e33896015588f2c02971263007e0cf574b5c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/metadata.json",
        "sha256": "440cf73c2942f0e9ab9c59e5a39a5d7ede706bbf6b085d630ea072c3448e0588"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/qa.json",
        "sha256": "6c56187c17d86c17b653a4160da78c6c55e5de855ea24bb5536ed60f97fb23a3"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/freeze.json",
        "sha256": "73f70f61d4948516ebc1cf906b1ba141ba98e927d2000c60d97ef230cbb2f233"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/practical-integrity.json",
        "sha256": "5bce71f53e44f57babc65c769190f422020f5b091caf7b87b0f34614bc49501d"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/profile-contract.json",
        "sha256": "366c094cc0d56812ba74e6880c1a220305c779b4188ce36d6ec5bce797144c3f"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/profile-gate.json",
        "sha256": "290d6247e73672e5bad9a47cbcc025f2a53885cab5d240c506f0551129046b46"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-19/quartz-prism-cluster/r001/legacy-gate.json",
        "sha256": "ad3a57366364ad6715a16cf6bb7915d8b2ca0a4395ea3a5138e810a887f41ac0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/source-contact-sheet.jpg",
        "sha256": "4bc9b771c863f1e91654a0df4ab0e41a42ff52fc6a518ef775444f9648f4502c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime-contact-sheet.jpg",
        "sha256": "70e9be785f49c4ea5b1ef19c7bece897ecb78734c34209402a97976ed59eb9db"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/preview-hero.png",
        "sha256": "9d3ae2973a84bc363fc52360bf33918ac129250d0bc3884be5a93d93c53572f5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/preview-reversehero.png",
        "sha256": "d8369bc54ef4bc9ef5da141691f048ceb18c155f72d2f3eb51d9b922a6fa03c4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/preview-front.png",
        "sha256": "eb3c695a182acad1c22f76d045788b00f200617c1baaebd59422ff2c7ad70c4f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/preview-side.png",
        "sha256": "78d7f635b6f8ea6c476d187e5b4d56c6a5343ed210d09fd6ee38e2b3529a7ee5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/preview-rear.png",
        "sha256": "7d20d07f091bf718bda26e4cff308816ccf1ab0cd90d8cdaae961d71e59b4123"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/preview-top.png",
        "sha256": "91c708521cb7776fd015a0dfb1665a3727ebb398f5fae0ecef488301f1da3942"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/preview-clay.png",
        "sha256": "12c4280667e8622d92dd049590e958396ad03c0cce63ffd86444373ac5cd0477"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/preview-silhouette.png",
        "sha256": "292fcc885ad1600344139a80066d882258bece26d79eee5d4246db5d30fbb9d2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-hero.png",
        "sha256": "052cf1b6a1a14c28cfa56ae7e5701bd3a48240f7a8e0d3f5d8660a38e526b4d3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-reversehero.png",
        "sha256": "9b8307960c50ea09673df7c6542714de36188dd999c8f0e0602c70f696996d25"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-front.png",
        "sha256": "c7aab067f2ed14705e41129160f0d012fd75f80136c9051b1e3f2ad4e203d7d8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-side.png",
        "sha256": "6fef1edf1515e91134ac0b3f79e307f5fb81117d6635984d81695608179cafcc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-rear.png",
        "sha256": "617a8c2a4ba8e308906f3604a7195ab4dcbdfcea3ce70f5cb1a24f5f4836845b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-top.png",
        "sha256": "9765fe63af82838625caaed8e286c974984a39aee93ecbf4d44d412b59479013"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-bottom.png",
        "sha256": "f71f5d4061525a03b770c28b8ec052796994c8aec505bce618a15968cb7c70b2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-80px.png",
        "sha256": "fd3d04aa762085270afad93add60896079f5bb297aa7f801b3756ca24c3f22c4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-160px.png",
        "sha256": "65c2dd797374282b2519c7a9c5d641a8c03a116a37e631f38630071f84da8a9c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/single-240px.png",
        "sha256": "08cb3d0015a4f2a37cb1b02a9a74e1124c70dc775e53b54b258fa8f9c772e504"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/scene-hero.png",
        "sha256": "7beede78aff86c6045ca73c650614feac486c47c45806fc0be37a28701d47490"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-19/quartz-prism-cluster/r001/attempt-01/quartz-prism-cluster/runtime/scene-top.png",
        "sha256": "e6a4b5f06cf3f040f671d77f9c85c63dee16c0bb71ec29d6b77185ab46d394f1"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/quartz-prism-cluster/candidate.json",
      "sha256": "03e062059520ed1d56c266a84c5fa2620b7896f8a2ad9866bb35a425eeb707ad"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/quartz-prism-cluster-contract.json",
      "sha256": "67a5838e0fdd901d242e3d840df846a7b554b2b137405517ee429f65b668ffd7"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/quartz-prism-cluster-result.json",
      "sha256": "e1da71fbf06b7a72d158fcbc2cbc473aacac8438859e150f12b98830bef85bed"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: independent-acceptance-pending",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/quartz-prism-cluster-original-legacy.json",
      "sha256": "ad3a57366364ad6715a16cf6bb7915d8b2ca0a4395ea3a5138e810a887f41ac0"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-19.json",
      "sha256": "13b54008b926040873d5ea05ec306fe94f53521b6139c334b18bc5bf7f415a1c"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-19/HANDOFF.json",
      "sha256": "a92c9f5954edad46d167ed8f967095374266568d15d3d3a9bff429cdabd4b4bf"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/quartz-prism-cluster.json",
      "sha256": "ee4ebd3b5c4924092a7f265fbd0326f6c326c2b17ab9b857c194adfe433eb676"
    },
    "dependencies": []
  },
  "leclercqia": {
    "id": "leclercqia",
    "batch": "20",
    "source_commit": "5194c8cbcacbeb496f79ec6e7cf086adf9cc03b7",
    "review_commit": "b0c61ef1adbb5edc3d484eebb1c2da179de10c10",
    "handoff_commit": "f4090f8bc7130347cabc73dfbcd44f81b5cd5a9f",
    "review": {
      "path": "qa/continuous-small-life-round07-20261018/batch-20/independent-review/report.md",
      "sha256": "633d2322ff5f54c153fe1ecfb4568b07e8f63a6608a80ff0e14b3466141d086f"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/candidate.json",
      "sha256": "8794c586db36e6b4ffa88910ede077b9a496773bdf846d276e15d2d372baf76d"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/metadata.json",
      "sha256": "842118d49b9764cc6574c5694e2d04082865d94daf6f3d4399a5410087cc1c32"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/leclercqia.glb",
      "sha256": "83790eda41c579b89f5abde777f7d6b6a30099df551425b21d0096a5cfc59e2c",
      "bytes": 99412
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/leclercqia.blend",
      "sha256": "5506fbc67c7e63f177df132909c613797607d0d68f9c1da561af008c58388cac",
      "bytes": 647208
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/render-manifest.json",
      "sha256": "bf8c4ed468ce89e5a11366f056fd006d583ff28eee657b841098aaa373ffbdc3"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/runtime-report.json",
      "sha256": "a864269cfb1df41a792f8e510a9662680489384d3e173f3f0abf729255afb04d"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/runtime-report.json",
      "sha256": "a864269cfb1df41a792f8e510a9662680489384d3e173f3f0abf729255afb04d"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/source-export.report.json",
      "sha256": "3973b2f81a1127903131a9beb7ddce13df92e439b26d2720b5290f358bd3b8ed"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/gltf-validator.report.json",
      "sha256": "76dfce4013614a2dfe9eff1815fb5632bd5c6edf83b9a14e3c255af9965e5749"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/candidate.json",
        "sha256": "8794c586db36e6b4ffa88910ede077b9a496773bdf846d276e15d2d372baf76d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/leclercqia.glb",
        "sha256": "83790eda41c579b89f5abde777f7d6b6a30099df551425b21d0096a5cfc59e2c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/brief.json",
        "sha256": "c5588e3ee6960d1c5a7fec39e54a8d83d5648a59dc9e8f73fb77b2a9ddefd48d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/references-profile.json",
        "sha256": "46dccf81ae474464b4b7516b126aa870ef561db239c9c6ddb66e8c6dba1294f3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/leclercqia.blend",
        "sha256": "5506fbc67c7e63f177df132909c613797607d0d68f9c1da561af008c58388cac"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/build.py",
        "sha256": "22f66a2e5f790827722a8eb2c7669f15b2ae83e5be2efc186683e8ec4b2d7969"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/config.json",
        "sha256": "76da180cbd8de0953e8c2fb7c364c8fbea9786ca9869ee042b9c5500b2520317"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/render-manifest.json",
        "sha256": "bf8c4ed468ce89e5a11366f056fd006d583ff28eee657b841098aaa373ffbdc3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/metadata.json",
        "sha256": "842118d49b9764cc6574c5694e2d04082865d94daf6f3d4399a5410087cc1c32"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/references.json",
        "sha256": "46dccf81ae474464b4b7516b126aa870ef561db239c9c6ddb66e8c6dba1294f3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/references-profile-mapping.json",
        "sha256": "acf069bdcf32b090c8e870c58bf6fb39de911bde6c08df2c08138001b6f503fa"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/reference-access.json",
        "sha256": "f2c5e38ca1ff7f5c996f9bd4cdbbfd90e53035e63465caff9c039ae2303b9633"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/profile-contract.json",
        "sha256": "a50d023907d10761239aae8d2586a1cce33a6431c2c2896aa7821515245ac06a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/profile-policy.json",
        "sha256": "7e46864e40eb64411f9ea3296d91948ed833a3422faa503ee4024e9339d388b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/evidence-manifest.json",
        "sha256": "2b974ce9a01082660f28de549645025b1dc9ca8b76735ba9871a76a54a86c340"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/source-export.report.json",
        "sha256": "3973b2f81a1127903131a9beb7ddce13df92e439b26d2720b5290f358bd3b8ed"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/source-mesh-measurements.json",
        "sha256": "d79df392c21549c154f2c91a40b181a581be6c15d0ef8901102f865da875d34e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/profile-checker.report.json",
        "sha256": "12e6f4cf26cdaefcc5e2d6ad220760bd9666ac19ed833a732a8a1056f47f831d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/profile-approved-check.report.json",
        "sha256": "12e6f4cf26cdaefcc5e2d6ad220760bd9666ac19ed833a732a8a1056f47f831d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/project-checker.report.json",
        "sha256": "6e41bced42363f61d582e2f12c6a6274fc1baca7983934972abcbf0fa36d332f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/checksums.sha256",
        "sha256": "d956d708a2c7798a51a0c451728f973d10da6b751e538cd436a2ea079ee4c369"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/HANDOFF.md",
        "sha256": "7cea6956402d52f9345ecc0a85bf4b51b9a9aeb37c042c0268622f7c92e84934"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/serial-execution.report.json",
        "sha256": "7faaecaf373e443815e31a0b42057bdf6b73cc5f69c7868b4725c996344db931"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/upstream-deferred-hashes.json",
        "sha256": "f15e09333774d7a4d392fae301f2e544db6c406bb1f44bb8083700297a78457a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/preview-hero.png",
        "sha256": "a892010c84e219bba05b6e7823066b013b0a2544194ca1daf7d05c4a2e027ebf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/preview-reversehero.png",
        "sha256": "1995b69aebcb5e101cba38ecb02643f87ec3b2af1bb2dbc238d1db889655e0cb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/preview-front.png",
        "sha256": "988154883fd98f17e7ac13aaf0a6f107706621570dca79288ab1afcc034811d8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/preview-side.png",
        "sha256": "3a6464f079e9aa1cf04759878c2ef681a561b5a2ef1635aae884a41161b2de09"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/preview-rear.png",
        "sha256": "f23992bb3885d61d8fb751e578e01f407488f453dc9e095c49fafa7daa92c0f3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/preview-top.png",
        "sha256": "ee8e31263fa03ded70765eba6d7333143d08bd09a330c6f6461b0172de1f21de"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/preview-clay.png",
        "sha256": "9a21df079b4c6e0c8e0e4c375ac6440563e88ce9c468e8216ed65ed6bf9ee87e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/preview-silhouette.png",
        "sha256": "13c119aeca8d9dcb354b003e29f85524ab25151dfaa1a7f005a290189de00a01"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/runtime-report.json",
        "sha256": "a864269cfb1df41a792f8e510a9662680489384d3e173f3f0abf729255afb04d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/front.png",
        "sha256": "ac61d78b122729100a3b68a991f1a24931920bad1dae3a5034e2ddadfeeb182f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/hero.png",
        "sha256": "130bd931501b0f45a7b4f188fb8da3dd7e403eed666f86b4f39cb97f64d28e55"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/near.png",
        "sha256": "0e958d34affdcb066f21c89678160c1a5fc2637d6a34efc18e216574fbc8a90e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/reversehero.png",
        "sha256": "edbed7a3449ad42567050b352aa619193e55de7aad678f18d80dfe969d04dcb8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/scene-9-copies.png",
        "sha256": "dfb58f55422718a0d73ea963c7b2c20dcf926cfee02915bb509b30a44df49518"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/side.png",
        "sha256": "300d69fd0f758553176b8c16e2386fb9d54e11904696c0fbdc8d6ea69d3fc809"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime/top.png",
        "sha256": "5cd14758b4047beac7ad00e05199a7dc5ababf0b54bad1e04f5843700b1f1de2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/view-manifest.json",
        "sha256": "4707cd57a00c789bca6e993fb1471de4ec5fc6f200ddfceeb9ba8083cbb17cba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/views/transparent/preview-hero.png",
        "sha256": "18678f93b5f63ed1167adf974413adbeb809d37263b0244e7e5ca01d1f6ddf74"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/reproducibility-1.report.json",
        "sha256": "9098303962012a295e86b3742a87b04d14993a4094d03b405a925b69209d1f87"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/leclercqia/r001/runs/build/leclercqia/r001/semantic-rebuild-1/d872bd6a36e7b87bb803c2a9946233d027c56b160b456c4861d397063a5e143c/20261018T212831-06f593dbb9f54587a9af660642611d5c/request.json",
        "sha256": "c0a176043d89a2b9c90f7f7d4834303240213e6bb51a9e15e4c35974951689b7"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/leclercqia/r001/runs/build/leclercqia/r001/semantic-rebuild-1/d872bd6a36e7b87bb803c2a9946233d027c56b160b456c4861d397063a5e143c/20261018T212831-06f593dbb9f54587a9af660642611d5c/result.json",
        "sha256": "ad19551079bf0df53c636297f359dfe764a1462c7d3ffc617ffd042062c4e0a9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/reproducibility-2.report.json",
        "sha256": "b6ba9b381ae05b584205852dae2a0ba526515f7e237dadfb7e0023e1251a8bfb"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/leclercqia/r001/runs/build/leclercqia/r001/semantic-rebuild-2/1e2d3dea297b8e81c1bee62ef72b19c7d078e05d3503fbbd7975a9a8511da625/20261018T212833-157e00da5fb9400db4b47b573bb2817f/request.json",
        "sha256": "ccc25b8120169a2eb2cc8a0553c3331a90e74be42616a5453ddc24f9ddb6604c"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/leclercqia/r001/runs/build/leclercqia/r001/semantic-rebuild-2/1e2d3dea297b8e81c1bee62ef72b19c7d078e05d3503fbbd7975a9a8511da625/20261018T212833-157e00da5fb9400db4b47b573bb2817f/result.json",
        "sha256": "4f9f187a0719c7c2a391cff4bbbc5bc7ca4b0cf573004059b31ba3e1c2b65e5b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/maker-self-check.json",
        "sha256": "9c72fe629850b92448d741cf581ec759a5c904f87f1fd33ad4f0360ac499a9d9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/build-config.json",
        "sha256": "ef4b53d42baff86a4401f087448d6f810c27096bc11df36c2b28cab215b4b512"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/dependency-hashes.json",
        "sha256": "885d07a323bd62bfe3753225bb9cc5ab1bd35368cff595c4d7ef23f1d2d723ad"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/freeze.json",
        "sha256": "894db1f3ee85993c0bee7dcb6670624eae0815b7fedaedded6a4ecf753422e59"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/gltf-validator.report.json",
        "sha256": "76dfce4013614a2dfe9eff1815fb5632bd5c6edf83b9a14e3c255af9965e5749"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/inventory-record.json",
        "sha256": "125febc8b8e2cba63a10995ab211d7ec66f5c9a9af7009cc07ff92f8b9bf113d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/maker-visual-inspection.json",
        "sha256": "688a976ad7bbcdf0ca64c06c6d44931beadf1f394b658f3a2963c22ddb77c474"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/preview-hero.png",
        "sha256": "18678f93b5f63ed1167adf974413adbeb809d37263b0244e7e5ca01d1f6ddf74"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/qa-contact-sheet.png",
        "sha256": "aea3698b93799de12ad45c8db5068858d4302e08b31664c50e9dafcf2868cc34"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/qa.json",
        "sha256": "1cbae1c47ddb8f5e8c69abd7ccbbb12f1b34fe5d29b89976961b61e2e0ac88c3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/reference-policy.json",
        "sha256": "6135a2ee5042b82db2ba50413138651b8e9e0c4bb15f0390786650697639f752"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime-contact-sheet.png",
        "sha256": "b9845c71b8759dcdfaa7cd31d2cd93927c09306aeaee26225a7295991157a97c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/upstream-deferred/brief.json",
        "sha256": "0f47e8830ff239368520413d50d6099d2c118a030bb4949b118b0209e8a730e3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/upstream-deferred/build-config.json",
        "sha256": "82bd1b23284e786b650cf406b6b438b355d5d816dd62e16e2d0d915bd002d634"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/upstream-deferred/freeze.json",
        "sha256": "7c2dc5e7234437cb99844ab5f5af1580543fdebbb11c5dfea56fbc9f42d6fe67"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/upstream-deferred/inventory-record.json",
        "sha256": "125febc8b8e2cba63a10995ab211d7ec66f5c9a9af7009cc07ff92f8b9bf113d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/leclercqia/r001/upstream-deferred/references.json",
        "sha256": "4f628dc1e50e10f6cac78611bc285aa8d8dda9ab4fa3c0504735094f9d4c32b4"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/leclercqia/candidate.json",
      "sha256": "11a92985b016d819097819917381751920d8aeaf95d6bdda833b59de70decdb0"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/leclercqia-contract.json",
      "sha256": "43b998373d6db9cc68bc2d498cf559ce373709c840a29cd4711bb8efb57ec3be"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/leclercqia-result.json",
      "sha256": "f117096af7e5ec4afc333e8aa7e5884f90e29703cf0872ef08bf75fbad8c93d5"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: normal-view-craft",
        "open blocker: basic-form-and-scope",
        "open blocker: deliverables-and-label",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/leclercqia-original-legacy.json",
      "sha256": "6e41bced42363f61d582e2f12c6a6274fc1baca7983934972abcbf0fa36d332f"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-20.json",
      "sha256": "21714f468a718f42714a62edffb15891f28b95d1641c075bf50eaa5bf8f02997"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-20/final-handoff.jsonl",
      "sha256": "365c149c01bb494be06761184c044ca0b95b001eb3d333aecf5f0eced41fd418"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/leclercqia.json",
      "sha256": "45ce4d4b38930f897e467b358b4ba339197f008a25434d70200781fda42dfc14"
    },
    "dependencies": []
  },
  "canadia": {
    "id": "canadia",
    "batch": "20",
    "source_commit": "05f4e45f5f65a33ec7ab1738b41275b5dab71bc3",
    "review_commit": "b0c61ef1adbb5edc3d484eebb1c2da179de10c10",
    "handoff_commit": "f4090f8bc7130347cabc73dfbcd44f81b5cd5a9f",
    "review": {
      "path": "qa/continuous-small-life-round07-20261018/batch-20/independent-review/report.md",
      "sha256": "633d2322ff5f54c153fe1ecfb4568b07e8f63a6608a80ff0e14b3466141d086f"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/candidate.json",
      "sha256": "34d8cf277c362fc675f4d99e1a71c52d24b41ed917b3567d823318b018c96cb4"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/metadata.json",
      "sha256": "70e6f473e300981285bc73e2af581c9787e220548b4e9ac708e941f04b8a79e0"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/canadia.glb",
      "sha256": "8fbcd32a40b1a79c02df0e5cc4e91224606cef3482cee88990d73ab26bc02273",
      "bytes": 125040
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/canadia.blend",
      "sha256": "48d72418b220c1ee4f43d4d61110ee25d333234b539ac890ea946dc0b490f529",
      "bytes": 666624
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/render-manifest.json",
      "sha256": "e087ebe905bce45a099f626a57b5385db719ff53e52a11d97c6966830d1398ce"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/runtime-report.json",
      "sha256": "d58c1838affd779fa9fbee09c0505f1dd49360e192530e54fe6216504e7e061a"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/runtime-report.json",
      "sha256": "d58c1838affd779fa9fbee09c0505f1dd49360e192530e54fe6216504e7e061a"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/source-export.report.json",
      "sha256": "7b033ea42d0e49aecf47d8114853c7d986d749cae72d4df74087923a03f723ab"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/gltf-validator.report.json",
      "sha256": "c83695a80bc679d9b748adc27056edcaef33672c8bce4c0b124444101379735d"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/candidate.json",
        "sha256": "34d8cf277c362fc675f4d99e1a71c52d24b41ed917b3567d823318b018c96cb4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/canadia.glb",
        "sha256": "8fbcd32a40b1a79c02df0e5cc4e91224606cef3482cee88990d73ab26bc02273"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/brief.json",
        "sha256": "1849ec6661cf3d10678be8c2ed99a20d9d121f694bf605050c43925ec6aaa5b1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/references-profile.json",
        "sha256": "9448686d4051fa5c6a7d280d4b009da14e49c1ffbb440142d4fc970224aec118"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/canadia.blend",
        "sha256": "48d72418b220c1ee4f43d4d61110ee25d333234b539ac890ea946dc0b490f529"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/build.py",
        "sha256": "22f66a2e5f790827722a8eb2c7669f15b2ae83e5be2efc186683e8ec4b2d7969"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/config.json",
        "sha256": "51a27d535f1902f1a8e851dbefba8199fd89f7215969310a734f665a0ed15494"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/render-manifest.json",
        "sha256": "e087ebe905bce45a099f626a57b5385db719ff53e52a11d97c6966830d1398ce"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/metadata.json",
        "sha256": "70e6f473e300981285bc73e2af581c9787e220548b4e9ac708e941f04b8a79e0"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/references.json",
        "sha256": "9448686d4051fa5c6a7d280d4b009da14e49c1ffbb440142d4fc970224aec118"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/references-profile-mapping.json",
        "sha256": "b0ac4617616c589b892aaf9dbe921691b3d099d32abc59045581c333a8d35a3a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/reference-access.json",
        "sha256": "9c40abd728e664764db79fb0e9cf631059e1fe93277e71b0938c371829be831d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/profile-contract.json",
        "sha256": "9bc2571f6fa378582da47c693bf1c98bc630a0e06c0edbccbd14e937666f75a6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/profile-policy.json",
        "sha256": "7e46864e40eb64411f9ea3296d91948ed833a3422faa503ee4024e9339d388b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/evidence-manifest.json",
        "sha256": "f481c9ab2404f39eb1eb212ab55cee0722108a3a4247634537c7d633079cc5c6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/source-export.report.json",
        "sha256": "7b033ea42d0e49aecf47d8114853c7d986d749cae72d4df74087923a03f723ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/source-mesh-measurements.json",
        "sha256": "df7f4bbf5c77b75a46e486ec696dc2e099fc80eb7b6c3bb3080686057e6bcded"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/profile-checker.report.json",
        "sha256": "2bce71b1ec6a27821267d63c28dfce8384edb8688c75d704a5e7f6dce39d6332"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/profile-approved-check.report.json",
        "sha256": "2bce71b1ec6a27821267d63c28dfce8384edb8688c75d704a5e7f6dce39d6332"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/project-checker.report.json",
        "sha256": "e4f4cdb1ca5bdb9ea16bc57621fa0bf9731ae126d2b9d86e6f5915d51b54dcf6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/checksums.sha256",
        "sha256": "5c1185b0c5161d6916f3d58e22af8fa22a149de1dd4cc83c18e65af635d69d3a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/HANDOFF.md",
        "sha256": "b367c263c38d63f3d86eaa5a94cb29d2a5443212423110947192e7baab5bec35"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/serial-execution.report.json",
        "sha256": "310e46f03b10cd794b64b78d97e1c9b1a7287965319b54fe46f1461a6b155f78"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/preview-hero.png",
        "sha256": "92c3fe6a6127dfa6232f50bac86a1285febffac4244f6a97e9fb1fc3d9db979f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/preview-reversehero.png",
        "sha256": "1377eb6c6126f6ee201d1a4cf34d10ea470d90fb4a6d962304ce9700d5d16e8c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/preview-front.png",
        "sha256": "f89ab1ff2404b2319181f840d57c038af3fda0741e4ffdaa65e20c9e833bcc15"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/preview-side.png",
        "sha256": "069b8d7e89097ed32bd756b5c5affaa34ecbe7818bb5ec5248882c39ad1824b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/preview-rear.png",
        "sha256": "6777ae3accec6f849049bdbea96c6f88cf9a09afc5c0d4e1409d4b189b2dda93"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/preview-top.png",
        "sha256": "bf7648ba674b2bc9c0101022dbcef38a88bc4551df3c13d4e5def217f444d4c6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/preview-clay.png",
        "sha256": "bb86979f095dd9d211dd7a3e7b089a7af017b64b91c8565257167e6072281a89"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/preview-silhouette.png",
        "sha256": "572e605f203c0d6531d7e179b499e8f8b90dd95cf490c8a698037d313647fdaf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/runtime-report.json",
        "sha256": "d58c1838affd779fa9fbee09c0505f1dd49360e192530e54fe6216504e7e061a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/front.png",
        "sha256": "1c5b7824c21df6981619d8c0a37acbdebbb41c7d27ff8839b8894aa13935212e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/hero.png",
        "sha256": "359646680eb41271180cb06903658027f731c3427d83785d423b2587383fbe96"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/near.png",
        "sha256": "be1f41c2803d783bab24df1b18f9c5f30cee5d05bc5c45be2a9f2c64cd8d1832"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/reversehero.png",
        "sha256": "8a4af38b7a1b18291b386403cc06b80a872012b5518cc108b24129ebef3bb3ce"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/scene-9-copies.png",
        "sha256": "2cba03c4a69128c05564bd1974a47306cbffc5f77d85136163c10a5ca9fc3f93"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/side.png",
        "sha256": "83b78347ab9753574edafd846fe959c7f1d4875652aec21fb913eca2eb612f39"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime/top.png",
        "sha256": "a8a6100ee8d94bcf42a520cd36737d5a6efc0bed9fd2bbce42ee1d1111bdc092"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/view-manifest.json",
        "sha256": "c9c39e894356282aac5741a684a55c6eab62261b4934824aa76ec95746f2ce06"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/views/transparent/preview-hero.png",
        "sha256": "e197ca8c37accee13b027cab5412a6616ee36cce833f1cfd53e4de0c743d98f0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/reproducibility-1.report.json",
        "sha256": "61a2fcb0923498ddb8b5300aba06420bf293f7dcf81b52ab07153ff7649840d7"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/canadia/r001/runs/build/canadia/r001/semantic-rebuild-1/07077612b8ed805a7df76bb0fd583508ee870a935a3a52073dea62598ce2b308/20261018T212954-1d7b39d984d84a79858fd16db7e35402/request.json",
        "sha256": "09168aa92f054a8be90a30f8595cca3676589a3b57aaf833675e89bf22bd2a4d"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/canadia/r001/runs/build/canadia/r001/semantic-rebuild-1/07077612b8ed805a7df76bb0fd583508ee870a935a3a52073dea62598ce2b308/20261018T212954-1d7b39d984d84a79858fd16db7e35402/result.json",
        "sha256": "68e0c582e60300903b4904017e9c1df7dc990b1702ef7ad62b776f036698db7f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/reproducibility-2.report.json",
        "sha256": "e25a79a0ba9b4fd5a4796228bcd8d45313c106e293763913a135d4420b7704b2"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/canadia/r001/runs/build/canadia/r001/semantic-rebuild-2/5dff1e7de082ade53d3415bf34d6d827fc60e48277ea0dd49a2d600ef7809f94/20261018T212956-d7546c25d9b54d068bea900965b8cab7/request.json",
        "sha256": "ac0346519690b2e534b2b5ba1bfedfb89e64525641127eb072485eef983cad21"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/canadia/r001/runs/build/canadia/r001/semantic-rebuild-2/5dff1e7de082ade53d3415bf34d6d827fc60e48277ea0dd49a2d600ef7809f94/20261018T212956-d7546c25d9b54d068bea900965b8cab7/result.json",
        "sha256": "cadab8a71df23713f156b65a6d06a59b20b5da32bb8e3c6785980660a3edff00"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/maker-self-check.json",
        "sha256": "b0817247c0daa379d70f5a031a3cdc9ac1fa385d9dbbe1a50264e4e1424c2626"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/build-config.json",
        "sha256": "b825c9165321f7ae1c8cf3b1f7c0f73d9c3ab12e759e88643d3056b527e94939"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/dependency-hashes.json",
        "sha256": "2d9f7526b227e5a1f3663c4a4d8439f3fbb3970215a567c2beed847a92220a4f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/freeze.json",
        "sha256": "e2950c03d6b77eb2a26338be488acbdb3afa35226b54117b2484f022c1fde474"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/gltf-validator.report.json",
        "sha256": "c83695a80bc679d9b748adc27056edcaef33672c8bce4c0b124444101379735d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/inventory-record.json",
        "sha256": "cd608e8b4838f4105c7a418faefb7e58ac4210171468e2f38af42d2ca1e2f843"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/maker-visual-inspection.json",
        "sha256": "034cad45d935c07e425bc109f8bfb6d0f4759c93e2b6a885f2ebe1f0db5db902"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/preview-hero.png",
        "sha256": "e197ca8c37accee13b027cab5412a6616ee36cce833f1cfd53e4de0c743d98f0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/qa-contact-sheet.png",
        "sha256": "9c349a53e95154a2b251b79fd154f72623ae8370458a9217054cecb32c49700c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/qa.json",
        "sha256": "67be8a5ea24b9758e4385c6bea7ff894307d23c2548b0f7729810fa4e8b38e0c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/reference-policy.json",
        "sha256": "6135a2ee5042b82db2ba50413138651b8e9e0c4bb15f0390786650697639f752"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime-contact-sheet.png",
        "sha256": "a0c63289eb5648075ae884ef7107459404633bd2140a180f183dc0a4785fed56"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/canadia/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/canadia/candidate.json",
      "sha256": "f5ecb7e73db6b131b53b98b4353ac97e31ef0e32d2b3322b2a010777b232865a"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/canadia-contract.json",
      "sha256": "51ffa0f0055952687f78c23fc3f95c040ae2d060ade4148182b2812728d7a672"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/canadia-result.json",
      "sha256": "5e28d0f8057002f9878ac271842122912d56a39ceca418fd8307e93ae44dff97"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: normal-view-craft",
        "open blocker: basic-form-and-scope",
        "open blocker: deliverables-and-label",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/canadia-original-legacy.json",
      "sha256": "e4f4cdb1ca5bdb9ea16bc57621fa0bf9731ae126d2b9d86e6f5915d51b54dcf6"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-20.json",
      "sha256": "21714f468a718f42714a62edffb15891f28b95d1641c075bf50eaa5bf8f02997"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-20/final-handoff.jsonl",
      "sha256": "365c149c01bb494be06761184c044ca0b95b001eb3d333aecf5f0eced41fd418"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/canadia.json",
      "sha256": "e3edfb1292945608c5c5c60e829574f6dfab66f28fa948979a9413bedfac6fc5"
    },
    "dependencies": []
  },
  "salvinia": {
    "id": "salvinia",
    "batch": "20",
    "source_commit": "a379c60eb5ace3ffbd7226fab7939e1d2dbd45ce",
    "review_commit": "b0c61ef1adbb5edc3d484eebb1c2da179de10c10",
    "handoff_commit": "f4090f8bc7130347cabc73dfbcd44f81b5cd5a9f",
    "review": {
      "path": "qa/continuous-small-life-round07-20261018/batch-20/independent-review/report.md",
      "sha256": "633d2322ff5f54c153fe1ecfb4568b07e8f63a6608a80ff0e14b3466141d086f"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/candidate.json",
      "sha256": "523d0a28d14d332c8be5cd769948c61d9787540355fe9f2af44e7b3f30c7ad88"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/metadata.json",
      "sha256": "399e2345258bf09e7c9c1c2b1c858c9b7bfff45516df87abd07b4550aec8912b"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/salvinia.glb",
      "sha256": "266e49ba2eecf604aeb27cf0f7c31edfb061d34e21da7bda6657ed04d2cdf321",
      "bytes": 49536
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/salvinia.blend",
      "sha256": "337b2a57188825adbce1c0cd37a0514009334d032ae910233c4620e5e4d992ce",
      "bytes": 603228
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/render-manifest.json",
      "sha256": "4c0aa40497da92a4afb2ff8b74f6fea21d65125acda37c5f3ca75ca3453baceb"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/runtime-report.json",
      "sha256": "e566ea3d0b38d9405df7bce47a1566b2a21a2b26739dc0e761f4c2ed5af57217"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/runtime-report.json",
      "sha256": "e566ea3d0b38d9405df7bce47a1566b2a21a2b26739dc0e761f4c2ed5af57217"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/source-export.report.json",
      "sha256": "2297b48f57cc77de7c77a5681e64d5c772bfbbb1d15bc75da2b9ce2020de7620"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/gltf-validator.report.json",
      "sha256": "44203875db24785dc093ed7f9f810c4264e85561b0117b7875489a8a32302041"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/candidate.json",
        "sha256": "523d0a28d14d332c8be5cd769948c61d9787540355fe9f2af44e7b3f30c7ad88"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/salvinia.glb",
        "sha256": "266e49ba2eecf604aeb27cf0f7c31edfb061d34e21da7bda6657ed04d2cdf321"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/brief.json",
        "sha256": "a1dfba64c9c92ae7fe464b8364c865e733547012ec24bd55728c7885cb496a09"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/references-profile.json",
        "sha256": "832a7cab6dbab8d4e1664e817ff401479934eabab2d467626b9adea96e16ba4f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/salvinia.blend",
        "sha256": "337b2a57188825adbce1c0cd37a0514009334d032ae910233c4620e5e4d992ce"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/build.py",
        "sha256": "22f66a2e5f790827722a8eb2c7669f15b2ae83e5be2efc186683e8ec4b2d7969"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/config.json",
        "sha256": "1294261ac3ee737c87e13091d31def023870db9132e0cc698623d785613ad338"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/render-manifest.json",
        "sha256": "4c0aa40497da92a4afb2ff8b74f6fea21d65125acda37c5f3ca75ca3453baceb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/metadata.json",
        "sha256": "399e2345258bf09e7c9c1c2b1c858c9b7bfff45516df87abd07b4550aec8912b"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/references.json",
        "sha256": "832a7cab6dbab8d4e1664e817ff401479934eabab2d467626b9adea96e16ba4f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/references-profile-mapping.json",
        "sha256": "e8938a4dec05dc897a0276c3520300445e2d5ee88c208a9222120b88125c9b32"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/reference-access.json",
        "sha256": "3e13e38a730e5c9cbc62d596ae794645ebee97baf8fcaa2ce67c835271d52a56"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/profile-contract.json",
        "sha256": "4e079ec31a945c2d6fec056c269f16f4dcb28dc602b7975b26fbbbfeb1fe907a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/profile-policy.json",
        "sha256": "7e46864e40eb64411f9ea3296d91948ed833a3422faa503ee4024e9339d388b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/evidence-manifest.json",
        "sha256": "199875b6f1b36538c472cdc607c7af8f0dc511c961c4642e916891b949411913"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/source-export.report.json",
        "sha256": "2297b48f57cc77de7c77a5681e64d5c772bfbbb1d15bc75da2b9ce2020de7620"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/source-mesh-measurements.json",
        "sha256": "0eda0f2aec31a3cf9f7dde7a7faf5203785616bbdfedb7fb4b35740062182233"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/profile-checker.report.json",
        "sha256": "7ceac323726afbb6dd3aa6a38eba547e75573c2b1d2ace4d8f5e1636cb34bfeb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/profile-approved-check.report.json",
        "sha256": "7ceac323726afbb6dd3aa6a38eba547e75573c2b1d2ace4d8f5e1636cb34bfeb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/project-checker.report.json",
        "sha256": "dde174a42d0394803b45117073fae1ba67dc1908621f7df7e6b80ac06338e619"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/checksums.sha256",
        "sha256": "84448514a8864a1546d3457637e19c8002a5c4a490d5a19d7f15d7a2e3e3d71b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/HANDOFF.md",
        "sha256": "dbd86e7618cd49e65ed3c82e0cee005d0ab10130af9778331059eeedb80b374c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/serial-execution.report.json",
        "sha256": "88ac019161852ad75e6fec59d41bae04bc1a23efb66340dd707a12051e4bc3f4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/upstream-deferred-hashes.json",
        "sha256": "27c2809174b9166e60e2b08b6ccdd3cf9ad4329e9c9402c8adbf446c5fe6977d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/preview-hero.png",
        "sha256": "a97acdea1aa6c57b7042c6f1a07f1e0584a8f82a36ae4180c998d0fec3eb6d85"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/preview-reversehero.png",
        "sha256": "60209866bcf9f5f1e107e7b92b5b33d966efcf84e10b4c04840c2c81fa17c815"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/preview-front.png",
        "sha256": "6eeaa2a0ab4a970b49ef022f4c9739dc3349ebab1c7c7cb8d615cc8703c396a9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/preview-side.png",
        "sha256": "731a0a19321894e4aad4f89474521ed7ca22db7e7b975decd816be60a22261e6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/preview-rear.png",
        "sha256": "f53da73bdd900ec4312a62e67c16e0a2daeaba727b9da4520bda94eb924c560e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/preview-top.png",
        "sha256": "3cf01fa19cc0b184271d374482658ddef5264b6424e2501f463e7bf123815484"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/preview-clay.png",
        "sha256": "c49b8b8884b1634406bb9bfe2fb0ae90e7052568de9e269c8992481dd6d7220a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/preview-silhouette.png",
        "sha256": "6ee2ec418840188990d773c2445cf9559cff0e608d111349e4a889c165ae1192"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/runtime-report.json",
        "sha256": "e566ea3d0b38d9405df7bce47a1566b2a21a2b26739dc0e761f4c2ed5af57217"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/front.png",
        "sha256": "1e56ee71808031f7b4a75b54babe868b067a5ba1abee94a2c414501f21c9f9fc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/hero.png",
        "sha256": "dc289a0a1ebff437bdc41db74e3536ce1d8291e46b4c07d5e9a8983be53c4ebc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/near.png",
        "sha256": "5e00c3646b40747723b45b61751177e398fb05a7b12c860ff7d907f04c9efce1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/reversehero.png",
        "sha256": "45c2b9a6eb7c84c210d7ff133547bdf97b361eab57225dca8e18b1cb3c608d49"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/scene-9-copies.png",
        "sha256": "7d9e8665ce0c74e431c307d74f266d5141b4e2fdfb5e64c20c4c822074f472fc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/side.png",
        "sha256": "555b5c662155f34640596e34d1d50a3d6861c3a0e89152f14374b8bbaa23a5d0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime/top.png",
        "sha256": "3df30f39fd5a1b6bed0b415996bee12fb400ba73a5e7fa9572cf0118a4113f6d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/view-manifest.json",
        "sha256": "4a9c34ef446dde234bc42a9f3a31ce766b5104f45c83661646297b084b99fa28"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/views/transparent/preview-hero.png",
        "sha256": "7ceea4e5919bff121fa5f9bc1d2b1c444f73636606a10cc8f3f060fddca62035"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/reproducibility-1.report.json",
        "sha256": "a84bac064af196378bd3c7ae90481f148244833cd47a9c3a50dcc468a809cf99"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/salvinia/r001/runs/build/salvinia/r001/semantic-rebuild-1/e766c591ae14fa38f1e8ae95d2d0cbda5fdc3f43ab320ec060aa0b01707dd99c/20261018T213111-994bcb98d5ba4c4cb26b25aca76dd422/request.json",
        "sha256": "7d6229277a80196bf31774242348c990f80f78d7c8a958bdf54b0429f2ea3b50"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/salvinia/r001/runs/build/salvinia/r001/semantic-rebuild-1/e766c591ae14fa38f1e8ae95d2d0cbda5fdc3f43ab320ec060aa0b01707dd99c/20261018T213111-994bcb98d5ba4c4cb26b25aca76dd422/result.json",
        "sha256": "8c2895a03c4a11f203dc8d5d4b3aa79cf13f4e9b569f56e630b5d0dde1525f5d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/reproducibility-2.report.json",
        "sha256": "f67e20ad97c70c0e134326a754fb52d21c90df463a7381a29b7c018f8281bb4f"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/salvinia/r001/runs/build/salvinia/r001/semantic-rebuild-2/2e6dfd4f099746924190cd8f41696dbe526b9ed3d7e77f502510ca027fd8762b/20261018T213113-5647dad92b03434da938ac2d8a1e3f5f/request.json",
        "sha256": "c88da3719e7c0fa2ca0b2065ac0dd5f6599640e12c448721080a5fafd8bb0ce3"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/salvinia/r001/runs/build/salvinia/r001/semantic-rebuild-2/2e6dfd4f099746924190cd8f41696dbe526b9ed3d7e77f502510ca027fd8762b/20261018T213113-5647dad92b03434da938ac2d8a1e3f5f/result.json",
        "sha256": "05e36587888d2ac2ec828b4225e8866838a929f53470602d5137ff22e8d8c866"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/maker-self-check.json",
        "sha256": "225f8f026be98578086c73419f6f4c8d58ee6b7fcce481939ef54ab0d195c619"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/build-config.json",
        "sha256": "e6692adac083a5f9be4e53bba0a594d999cbdc58b284dd7c5f32b094ab62b08b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/dependency-hashes.json",
        "sha256": "58a67c1539e8cdaa59ef6439418c6f7661f8af0d17f40e17640ff6e22f7775a3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/freeze.json",
        "sha256": "536ee1f610b978ee1426774b8d8dc85800675c9966dbcaee777c4e36130cde5f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/gltf-validator.report.json",
        "sha256": "44203875db24785dc093ed7f9f810c4264e85561b0117b7875489a8a32302041"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/inventory-record.json",
        "sha256": "a0c165890f0b4ea9519ceff1bf0dc76fa8a1ad1e3af1a243fdf1f35c41b15a6a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/maker-visual-inspection.json",
        "sha256": "bb2bf5300d6eb067354fbaaec0f3a95b7f980fedf03cce0b4c94b186a214088c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/preview-hero.png",
        "sha256": "7ceea4e5919bff121fa5f9bc1d2b1c444f73636606a10cc8f3f060fddca62035"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/qa-contact-sheet.png",
        "sha256": "d0ad58d92c455fe2d1326b105a176715077f662d590464b449c6c4fd07e9535b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/qa.json",
        "sha256": "5c6534d528164eca91fc2839673de21f759f84b2975e471b13a3e96d78ea9640"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/reference-policy.json",
        "sha256": "6135a2ee5042b82db2ba50413138651b8e9e0c4bb15f0390786650697639f752"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime-contact-sheet.png",
        "sha256": "c2600c0f12ca045c0fb5374193bafc451509f79965e1b861f4986185289538a8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/upstream-deferred/brief.json",
        "sha256": "7bf1361422c8e8c2374abce594b8c6cf2fc542bf147979045d4ea08cb3a5c5c7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/upstream-deferred/build-config.json",
        "sha256": "5b7e00c61cbba36563c86e28d8210f56ea0904757007be14cd54c54fe462f69d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/upstream-deferred/freeze.json",
        "sha256": "f44ba62ef6f588c8a979fb03bacff4f06384606dcea31018b5435c5695d0abcf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/upstream-deferred/inventory-record.json",
        "sha256": "a0c165890f0b4ea9519ceff1bf0dc76fa8a1ad1e3af1a243fdf1f35c41b15a6a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/salvinia/r001/upstream-deferred/references.json",
        "sha256": "edaad03386dc98811e027246cadf0b8c11aac97b5e01beaa44065f0efecca855"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/salvinia/candidate.json",
      "sha256": "fb3723aeaae47b618128a9d051eaf874a19cb848853964b328fe764c9f721a74"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/salvinia-contract.json",
      "sha256": "20d4c9450611db89cc85ca9649beb6114dacfe1dcc48482caf11af003ad7e6c5"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/salvinia-result.json",
      "sha256": "330bdd7bad22a636b044474d2a8387053c62000d3fb1d0506fe5dddc3bc3895b"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: normal-view-craft",
        "open blocker: basic-form-and-scope",
        "open blocker: deliverables-and-label",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/salvinia-original-legacy.json",
      "sha256": "dde174a42d0394803b45117073fae1ba67dc1908621f7df7e6b80ac06338e619"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-20.json",
      "sha256": "21714f468a718f42714a62edffb15891f28b95d1641c075bf50eaa5bf8f02997"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-20/final-handoff.jsonl",
      "sha256": "365c149c01bb494be06761184c044ca0b95b001eb3d333aecf5f0eced41fd418"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/salvinia.json",
      "sha256": "67f23cb7625667101f075c2a472bf5c8a732fc2da8a95aecc67c2e11c8422ead"
    },
    "dependencies": []
  },
  "load-cast-bedding": {
    "id": "load-cast-bedding",
    "batch": "20",
    "source_commit": "1d7fdb2e890ff1c79ce341a82c4b8571462716b9",
    "review_commit": "b0c61ef1adbb5edc3d484eebb1c2da179de10c10",
    "handoff_commit": "f4090f8bc7130347cabc73dfbcd44f81b5cd5a9f",
    "review": {
      "path": "qa/continuous-small-life-round07-20261018/batch-20/independent-review/report.md",
      "sha256": "633d2322ff5f54c153fe1ecfb4568b07e8f63a6608a80ff0e14b3466141d086f"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/candidate.json",
      "sha256": "bd7fc4f93a4822d8494feabb43e22e87f1ac86e88e77b921e48354c72584718d"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/metadata.json",
      "sha256": "90e5da5f7d01dd6d550dd2816dcc8614bd29138e272a7a2779ea8f7441e5f8de"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/load-cast-bedding.glb",
      "sha256": "c9c1eb75ec0d81448eb935f38bc86916ae1110617cf315972508cd4c82467e07",
      "bytes": 121996
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/load-cast-bedding.blend",
      "sha256": "855edf00ff5e7893a84b513775357a177d05c9929f75b2c86733ce981075d499",
      "bytes": 670300
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/render-manifest.json",
      "sha256": "ed9cf3277937484e53232489054ca02f7505fb8842fdaaea79137fd0aa450a34"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/runtime-report.json",
      "sha256": "7e153f0c02bfb90db8966bbb57bc5c39b59ca5197c282fbde4238f3d20fc27ee"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/runtime-report.json",
      "sha256": "7e153f0c02bfb90db8966bbb57bc5c39b59ca5197c282fbde4238f3d20fc27ee"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/source-export.report.json",
      "sha256": "a8b4c92096dcfcbb806d8560fe98e37e234638c0f53e7dd1afee70c3587a990b"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/gltf-validator.report.json",
      "sha256": "0d0556502baa0da21982a193884b38c9625aee15d664720d673269297238719d"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/candidate.json",
        "sha256": "bd7fc4f93a4822d8494feabb43e22e87f1ac86e88e77b921e48354c72584718d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/load-cast-bedding.glb",
        "sha256": "c9c1eb75ec0d81448eb935f38bc86916ae1110617cf315972508cd4c82467e07"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/brief.json",
        "sha256": "f14e9687dd1a4338d26ed02bbfd60968a9669d6125d4fa5d7ad0bd8d5cfabd82"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/references-profile.json",
        "sha256": "0cb8c77454fd6f0d69d2b8277690b58678f5254bc5f4df6c08f13c2f29b4b41d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/load-cast-bedding.blend",
        "sha256": "855edf00ff5e7893a84b513775357a177d05c9929f75b2c86733ce981075d499"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/build.py",
        "sha256": "22f66a2e5f790827722a8eb2c7669f15b2ae83e5be2efc186683e8ec4b2d7969"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/config.json",
        "sha256": "5aa3830563d9e9f82b8cc4cead59e4e940d0f6802efec68e8d3fc846208ecf14"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/render-manifest.json",
        "sha256": "ed9cf3277937484e53232489054ca02f7505fb8842fdaaea79137fd0aa450a34"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/metadata.json",
        "sha256": "90e5da5f7d01dd6d550dd2816dcc8614bd29138e272a7a2779ea8f7441e5f8de"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/references.json",
        "sha256": "0cb8c77454fd6f0d69d2b8277690b58678f5254bc5f4df6c08f13c2f29b4b41d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/references-profile-mapping.json",
        "sha256": "b18a861c2c3ecbea0aa88bcd182ad88fd51b06be033bd2f71d6ca3f292693a82"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/reference-access.json",
        "sha256": "0ac3937a56a7be55ea5126dec408886d44a6715bf7e68fb34364d7a46ac784f3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/profile-contract.json",
        "sha256": "a2191a9aa661cd6caf36d478a91a01731f1a8d130424022b507d8fe5856b59c4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/profile-policy.json",
        "sha256": "7e46864e40eb64411f9ea3296d91948ed833a3422faa503ee4024e9339d388b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/evidence-manifest.json",
        "sha256": "368dbc2cdca9caabf38f3495da5adccfc70d1c74bcf58712792c0b254e0465f6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/source-export.report.json",
        "sha256": "a8b4c92096dcfcbb806d8560fe98e37e234638c0f53e7dd1afee70c3587a990b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/source-mesh-measurements.json",
        "sha256": "d34e6f369e780c7ccc5c86b4d060096806e62f7d61a10360503722935c7d9576"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/profile-checker.report.json",
        "sha256": "fb2ac75518a3b693e5a4992205b5afbf2b3bde5fda51ab60619601008f601e87"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/profile-approved-check.report.json",
        "sha256": "fb2ac75518a3b693e5a4992205b5afbf2b3bde5fda51ab60619601008f601e87"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/project-checker.report.json",
        "sha256": "cbfcc67e16228c1e2599286f815dce402230fed8e411062dd72f7145b78c5d50"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/checksums.sha256",
        "sha256": "11dea66798fa3658eeb4764a07bed36c927f08a8ab8696acc54c9e31a56293fd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/HANDOFF.md",
        "sha256": "6ff9ce16abe6454ac43d0146a8607d3fc8778c56bb9570f2d99f5f5760b91d7a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/serial-execution.report.json",
        "sha256": "1c0dd7aa70eaac3fbbd24b018e63d4bbd76f9892274fd61b83892b95cf351fa6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/preview-hero.png",
        "sha256": "8138e492add0fc5a4be0c441da3896b79216653334352b360a2d0909a594a6b0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/preview-reversehero.png",
        "sha256": "338455f98fc0ce996e54dab343d641371e488bfad0c43f6e9529e156c56796fd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/preview-front.png",
        "sha256": "13cf6c0272e9b9be98db5512d6f8395260ddd90fce7bf1873e95cc1b0e785cef"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/preview-side.png",
        "sha256": "744391bd220beae57ccd21f29733fb2277ab769f768b159f0db95f719455c77d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/preview-rear.png",
        "sha256": "8a52e6b28742356d841655163c5e423689d3c0776a7034001e3c1f759cacea2c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/preview-top.png",
        "sha256": "887c2ab77df8ac3a2d828d64585531d2877e248a7f29c9c9fc79362ecb624aa8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/preview-clay.png",
        "sha256": "2d015ac1f67d479100d764204276f925ebb8e68487d3c0caa89d6d3d027e27f1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/preview-silhouette.png",
        "sha256": "453ce95f8c4984087ed570ea8e799cb6f3d54729c3582cb93a0ff91ea941dbcf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/runtime-report.json",
        "sha256": "7e153f0c02bfb90db8966bbb57bc5c39b59ca5197c282fbde4238f3d20fc27ee"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/front.png",
        "sha256": "039382f1a627405b2649b8142ba1b9c0692466fc08587a5aebd292e89b836076"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/hero.png",
        "sha256": "7f69cadb9c3f99a973d6ebc0853566971b0b230b07ed259946808e76cc6dd74e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/near.png",
        "sha256": "8eccf2d56cb1cf181539636eb108f56091d9dc80d57a6999648432455125b5a9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/reversehero.png",
        "sha256": "20dfe4081097f9637729e440a18d6eed89b3ba1e43dc32045659ab15f9d0b553"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/scene-9-copies.png",
        "sha256": "0e48ad14fe104f3267e5914607aeacb941ea5c0ccc03a3acd03aa9e456999910"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/side.png",
        "sha256": "2daaa377909c452fab8f0d3fae68966f198fafbadfab60e40cb64b24d81ca0ff"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime/top.png",
        "sha256": "4ff8004835c74556b7dd72a7b2986036902f4f719708fc9ebdc9e149fc52561d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/view-manifest.json",
        "sha256": "9f60d0bceca605d4f054687a84070877b516461bed5152e3999abcd30755aa6c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/views/transparent/preview-hero.png",
        "sha256": "461221aaa11e07e12c3bddef73742979c2c22fcfda23d49369255f48d7542bba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/reproducibility-1.report.json",
        "sha256": "0f6af3cf8565431b22a4bf126be215c09cf87a50fdb2153d91e4c00eec8f1939"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/load-cast-bedding/r001/runs/build/load-cast-bedding/r001/semantic-rebuild-1/f46b2a3f8b8dbd9cc331bf5af3d1533655cb7ce435bcd0b4a5db5d763fc8fede/20261018T213247-3fefc62d8dea4910a28a6ac55cee0b9b/request.json",
        "sha256": "9ec12da4990aab2586c09accd514b3c969d6471e95b7c6148905ef3d5371d917"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/load-cast-bedding/r001/runs/build/load-cast-bedding/r001/semantic-rebuild-1/f46b2a3f8b8dbd9cc331bf5af3d1533655cb7ce435bcd0b4a5db5d763fc8fede/20261018T213247-3fefc62d8dea4910a28a6ac55cee0b9b/result.json",
        "sha256": "55967dee0333740ecc2e7dd5777c3759200807a5000a9a3ab7b96b963152d5b7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/reproducibility-2.report.json",
        "sha256": "17f3801af53b41544f20460fee16837434d8fe466fe50edb8c570830725f9711"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/load-cast-bedding/r001/runs/build/load-cast-bedding/r001/semantic-rebuild-2/c76efaa4ea7846e89cdb581b4288811c40f30fca98e46a1c4f9cc39e4feadf8b/20261018T213249-c5a08ce087c14b9597686b7b0230853d/request.json",
        "sha256": "99310a5c69850fcd6c8aaea0e3cb3ddc2ab921107d8c32d6252631e9dacb6537"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-20/load-cast-bedding/r001/runs/build/load-cast-bedding/r001/semantic-rebuild-2/c76efaa4ea7846e89cdb581b4288811c40f30fca98e46a1c4f9cc39e4feadf8b/20261018T213249-c5a08ce087c14b9597686b7b0230853d/result.json",
        "sha256": "bdd0770e27c2b7162b0721125d067db4bb477bbc96404aa9fc368c21da11742b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/maker-self-check.json",
        "sha256": "c9e722bbc34314281d360ef9994fe786b365b2c296e25ee12f8590641fd47b32"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/build-config.json",
        "sha256": "9141d9195ece51485d1aa9b3c474c8bef4592ac8c5784ce239d1b9dfdaa30e4d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/dependency-hashes.json",
        "sha256": "bae809303ccc5d9e1412fd42e1b8153ecf812c6adede0bc9cc5b6da2f8d31cf1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/freeze.json",
        "sha256": "bc052ba5de954522389df11166a55c92bd90706ed34ab9a1e8027a7750b9eebf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/gltf-validator.report.json",
        "sha256": "0d0556502baa0da21982a193884b38c9625aee15d664720d673269297238719d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/inventory-record.json",
        "sha256": "991c1a06a30c34e008e83860220c19b369af3b8f09b241d9e80f6eb300b40cad"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/maker-visual-inspection.json",
        "sha256": "495488f715d947cd271175fedec5d938323ab0060e747503ca97603ce0ab7fa4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/preview-hero.png",
        "sha256": "461221aaa11e07e12c3bddef73742979c2c22fcfda23d49369255f48d7542bba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/qa-contact-sheet.png",
        "sha256": "e892317c952064857784e204c2627a9cfa29032323a582dec37a4d92b915cd3f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/qa.json",
        "sha256": "9bae3cc436d0386639e66fea04a7c77fece4937a5debe00234b7c82a02c78e21"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/reference-policy.json",
        "sha256": "6135a2ee5042b82db2ba50413138651b8e9e0c4bb15f0390786650697639f752"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime-contact-sheet.png",
        "sha256": "ed12e116e247cf5668ae7bea93927f641faf21b39399af28c1c5e383cad7c323"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-20/load-cast-bedding/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/load-cast-bedding/candidate.json",
      "sha256": "afd2442cd20d247dcf9b9a9b5fcfbd2741250f0a36eb5ccf0d9da333c390494f"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/load-cast-bedding-contract.json",
      "sha256": "52ad0730b61c0c2c92e292a8672b771ac0cfba49723442d8ad42da1f4044aa58"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/load-cast-bedding-result.json",
      "sha256": "bf48bf43261b569244db9b92ffc0a60d08534f2609e60cf6e92262d3642a7038"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: normal-view-craft",
        "open blocker: basic-form-and-scope",
        "open blocker: deliverables-and-label",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/load-cast-bedding-original-legacy.json",
      "sha256": "cbfcc67e16228c1e2599286f815dce402230fed8e411062dd72f7145b78c5d50"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-20.json",
      "sha256": "21714f468a718f42714a62edffb15891f28b95d1641c075bf50eaa5bf8f02997"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-20/final-handoff.jsonl",
      "sha256": "365c149c01bb494be06761184c044ca0b95b001eb3d333aecf5f0eced41fd418"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/load-cast-bedding.json",
      "sha256": "a3ae3722b479c413b23690e5fbe9c584a94c53f50d609c4ca7676df3a87a50c6"
    },
    "dependencies": []
  },
  "montsechia": {
    "id": "montsechia",
    "batch": "21",
    "source_commit": "86038ef0274924cb2315057500b481fdda8d8ec6",
    "review_commit": "5873b94ed3ed5f3c9a9dabb1e4c4464082c24f4f",
    "handoff_commit": "f78c36446e13cf12e335c152a37096e53859813a",
    "review": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-21/reviews/independent-leon/2026-10-18-independent-qa.md",
      "sha256": "68044acea79d91262dbf9f05107b7eaddffe9603d73258dfcbd4efda4d5338b9"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/candidate.json",
      "sha256": "8a1cb5d945f19d15289007453fed2ff329b317af675ed69ca5504a1689fe5210"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/metadata.json",
      "sha256": "4e90a1f6f4a2345a990d2fc07eca5604c3fea101c4a58af05adc9ac15e531b51"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/montsechia.glb",
      "sha256": "5ce96a830ddd499881f9aac0c5d261a80b1436c79935e85965c7777ffaf28d6b",
      "bytes": 92544
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/montsechia.blend",
      "sha256": "dbd160b8c67d69cc6cab2c5e547e2ea2ad8438c0a20c7de02af79544142a3d4f",
      "bytes": 613980
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/render-manifest.json",
      "sha256": "1b2b5f270ae447558dfe2f2265890cfb3babc7e039e76d09d0adc33a7dab0428"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/runtime-report.json",
      "sha256": "3942db80bba17b35443fa25bd9b73d5f3a3ecfcbabfb7f8ac7551e2315e1cd70"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/runtime-report.json",
      "sha256": "3942db80bba17b35443fa25bd9b73d5f3a3ecfcbabfb7f8ac7551e2315e1cd70"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/source-export.report.json",
      "sha256": "2e59f255f5d0456190d64aaf894c4734404aa9aea3c2d3665cf1ee383530fb34"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/gltf-validator.report.json",
      "sha256": "52c94c206b030048b60609576dfdac5473ed071ef034ad5c25e923fd40b08647"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/candidate.json",
        "sha256": "8a1cb5d945f19d15289007453fed2ff329b317af675ed69ca5504a1689fe5210"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/montsechia.glb",
        "sha256": "5ce96a830ddd499881f9aac0c5d261a80b1436c79935e85965c7777ffaf28d6b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/brief.json",
        "sha256": "0d20d1bc3ae7ee214f02ca9545cf57993d1c8e924671e3326b463c2eb64ada9f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/references-profile.json",
        "sha256": "902d4360e7ef4be2b4bcb579c6b0ccb1c79a093db5111eefc4a4f18f09503c14"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/montsechia.blend",
        "sha256": "dbd160b8c67d69cc6cab2c5e547e2ea2ad8438c0a20c7de02af79544142a3d4f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/build.py",
        "sha256": "236e143e5acf6244431e8064ef40dea863140ce247936f240a13ccb067330732"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/config.json",
        "sha256": "0d61733a40fd97b8ae1590da212310eb4376315c59e909a76b1cfc11a1a81a59"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/render-manifest.json",
        "sha256": "1b2b5f270ae447558dfe2f2265890cfb3babc7e039e76d09d0adc33a7dab0428"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/metadata.json",
        "sha256": "4e90a1f6f4a2345a990d2fc07eca5604c3fea101c4a58af05adc9ac15e531b51"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/references.json",
        "sha256": "902d4360e7ef4be2b4bcb579c6b0ccb1c79a093db5111eefc4a4f18f09503c14"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/references-profile-mapping.json",
        "sha256": "a26ee86674cea370ec946f8589b2c591e48d7842e3dbc629a326db990212d873"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/reference-access.json",
        "sha256": "4bc4164704ec796b4138d09990a18c98171cf8271fb46a736bb6868f5a6efa0a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/profile-contract.json",
        "sha256": "871cbff978f1b53484812273f0c5500f4d8c455a6eb4403a8a7056db9f7ce108"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/profile-policy.json",
        "sha256": "7e46864e40eb64411f9ea3296d91948ed833a3422faa503ee4024e9339d388b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/evidence-manifest.json",
        "sha256": "b377258ef0d691d1b6608b76adf81394dd6eb2409dc64b4a018a11f3df386483"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/source-export.report.json",
        "sha256": "2e59f255f5d0456190d64aaf894c4734404aa9aea3c2d3665cf1ee383530fb34"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/source-mesh-measurements.json",
        "sha256": "2cd8d6d607b0ad718d6d3efbab5fe896f91107eb9f9ed467538922b71114646b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/profile-checker.report.json",
        "sha256": "541d41515d615ae7d3270487b7f1d479cae784b87530f6e9b4a9d55fa70d5272"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/profile-approved-check.report.json",
        "sha256": "541d41515d615ae7d3270487b7f1d479cae784b87530f6e9b4a9d55fa70d5272"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/project-checker.report.json",
        "sha256": "039d949a6a915d97cefa056e0c8032e0853b2850f1104abb297c0c26997fe211"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/checksums.sha256",
        "sha256": "5fb72da8c2280d7b8b64072751647f2425f95abe4a62f1b5ceae2491b46fdf54"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/HANDOFF.md",
        "sha256": "878195c7a94232dca0d92542a9daea6e0f9b4b6959e20b629936b993db71a94a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/serial-execution.report.json",
        "sha256": "c3a33a5eae2228113ee20887f9f14f5ac410213c9005c819f4435750604382ba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/upstream-deferred-hashes.json",
        "sha256": "c92782bee15c9e9a4e72a075dc2c4d1f8cd6c2ba0451a6181132281c57cd8d1c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/preview-hero.png",
        "sha256": "5597ca40387f685a85d0799a9c6f184f2b03702dfc4f0b98deb0948f83ffc7cc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/preview-reversehero.png",
        "sha256": "7d4ab4c5b69fbd4e95a0b9fa2db3c05dd9c3107d66008e3b501dfad820bf5d41"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/preview-front.png",
        "sha256": "2da746336aa553c150d830abab0a4fc128fd877e6255cff06ac0b046d86d9fa5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/preview-side.png",
        "sha256": "e4365bed5265701169c7fb89bd2824d39cc033fbd51693b81066d1792226a53a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/preview-rear.png",
        "sha256": "722aa8bf6334c723dc56def0f9dc78f356c93787ace4dc9be8309086f6953ab4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/preview-top.png",
        "sha256": "f5703722b0695ecb70b02a396e6b519a425d0c43c38cfd22689bcf3898c22f64"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/preview-clay.png",
        "sha256": "9834ea46903321ac7ee2b05c7a09f71305232f68d549044bcee5f72539261fa1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/preview-silhouette.png",
        "sha256": "dbe9ccadd3cf211cf7141d4da036f2adb145b7eed57d4671995de1ff7b358dc6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/runtime-report.json",
        "sha256": "3942db80bba17b35443fa25bd9b73d5f3a3ecfcbabfb7f8ac7551e2315e1cd70"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/front.png",
        "sha256": "15e88813cc24a1fd0ac9b121f6447e3e73d9308acf55710d01a77fe289b95dcb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/hero.png",
        "sha256": "c86747ccdc4f1704fd6101d7cf162dbcf921e2996d33e2e4aaf07ec5b8445b9c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/near.png",
        "sha256": "056e9683055ae7342fe307f78874fbd0def19084e8df41c199e730e696c423de"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/reversehero.png",
        "sha256": "7639adc11238bc16055c5fe85d52145646c5910d7bd3b4eebb785f512253b8d0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/scene-9-copies.png",
        "sha256": "6f840b269b505bdbd2577032b658938abce4f3e4ef8a4817a414320aea1b99c0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/side.png",
        "sha256": "0fca4059f9fe2960814158f279fb53b3dee80e0f7f5b53b02619069ab2cb4080"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime/top.png",
        "sha256": "856708b3ca0ba6c2c52458b7e70066f9e7ea1e5ab4666875d9865f15962d167c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/view-manifest.json",
        "sha256": "289afd2006cd56b9864f51f69c5227ee21f5b452fca1971a4e5ff26e5b969ab8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/views/transparent/preview-hero.png",
        "sha256": "8294e115ff3205fb7e31772770aaa7db72a422e5f82298d15f0e291c734a6f14"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/reproducibility-1.report.json",
        "sha256": "61a926b7c6812c68f7f903155640c665039326c25c864fa13e6086b01184f840"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/montsechia/r001/runs/build/montsechia/r001/semantic-rebuild-1/15e65d2cac54712ebfa9effab2b2c1d65dd2dc7dd86501023ef99f25be0197c3/20261018T214019-2b2d40746e9445b3baddeb5ffcd4d9a7/request.json",
        "sha256": "a68bc50fc04943989837f0ead201dfcb524f11faec5c356df4e961660ca68987"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/montsechia/r001/runs/build/montsechia/r001/semantic-rebuild-1/15e65d2cac54712ebfa9effab2b2c1d65dd2dc7dd86501023ef99f25be0197c3/20261018T214019-2b2d40746e9445b3baddeb5ffcd4d9a7/result.json",
        "sha256": "91fe4f63d915fb82fe83eb55e828b1c90a274f45e21035499020e579d7dbe8ba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/reproducibility-2.report.json",
        "sha256": "17a0d46f96f82304735db5bc8feb0116b81c31a4f47b97c0c0a175e45daa67fe"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/montsechia/r001/runs/build/montsechia/r001/semantic-rebuild-2/20e796ebea249cf8bff80c226a8cb5b5d1a3f239e83eec66c32bf484dbb6d7f4/20261018T214021-11b6bdc3e6e240dcb5cf3c9892cd5fac/request.json",
        "sha256": "ecdc3cb861f741bfb6f9f20385c9298fb93b51a1a33b5c37b9abbf5483929b52"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/montsechia/r001/runs/build/montsechia/r001/semantic-rebuild-2/20e796ebea249cf8bff80c226a8cb5b5d1a3f239e83eec66c32bf484dbb6d7f4/20261018T214021-11b6bdc3e6e240dcb5cf3c9892cd5fac/result.json",
        "sha256": "8a271f400815a860cc0d49aa764f598df04c1c34b08ad387487df29d918aa599"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/maker-self-check.json",
        "sha256": "05bf848529bc1d118ea43d1e0a00447b3b0d89c55479d7e62ca7b199810de257"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/build-config.json",
        "sha256": "6b99833e3ea2fa9883edcf5cfe49177a138b113b3062864f952b13cccfa78877"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/dependency-hashes.json",
        "sha256": "eb7e41577148fd520b20fe799202011d9655fa3b0b868c943ef0715212300860"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/freeze.json",
        "sha256": "b6a681e34b71819f398ff9a6fac239fbd679d1ed2edf0ea552fc75fa67ff1d63"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/gltf-validator.report.json",
        "sha256": "52c94c206b030048b60609576dfdac5473ed071ef034ad5c25e923fd40b08647"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/inventory-record.json",
        "sha256": "0ab9c410ea91bf1153429ebb76997340c6faee92b031268fd10fd740b645d1f8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/maker-visual-inspection.json",
        "sha256": "82ba97dc82ccce4356b288b1010628538ad5e0576a03e62b9a79527a7dd6f60a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/preview-hero.png",
        "sha256": "8294e115ff3205fb7e31772770aaa7db72a422e5f82298d15f0e291c734a6f14"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/qa-contact-sheet.png",
        "sha256": "1a935dc9d10ee9e889595cbae4b51365b7dd9112435fa199461b7952686061b8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/qa.json",
        "sha256": "a6eb949fcadc50f78b8bc1952519d3704cddf248e9322dc91213258ca70d910e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/reference-policy.json",
        "sha256": "6135a2ee5042b82db2ba50413138651b8e9e0c4bb15f0390786650697639f752"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime-contact-sheet.png",
        "sha256": "bb6577e10ab6d24da5973b7ab150b0169c6e0b0a9b850766f5bfec51daa39e23"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/upstream-deferred/brief.json",
        "sha256": "d034ec853a6c9df274f84838cc0673f5cd6a942300ef91a377038a8644924e38"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/upstream-deferred/build-config.json",
        "sha256": "279474584d2160361810b077bda6ce9493bc8b27b85e008eefac209cfb0d35fa"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/upstream-deferred/freeze.json",
        "sha256": "4487b7378e905ea7dc7af17270702a702822a489b7cf1087327fbbfa6a745c8b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/upstream-deferred/inventory-record.json",
        "sha256": "0ab9c410ea91bf1153429ebb76997340c6faee92b031268fd10fd740b645d1f8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001/upstream-deferred/references.json",
        "sha256": "25e3c11d3c547efba88dba4f5528d550d7d934b6b80e1577e2fa6b28b79f95ed"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/montsechia/candidate.json",
      "sha256": "9fa88bd5d3809d43b156a9490b84d96e2adde6653dd71765e414ea64e94d244b"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/montsechia-contract.json",
      "sha256": "ed49c8e0e435249c8f9acffb63b41b57851d54d3fc37c8e4d10d5aa4a342ab86"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/montsechia-result.json",
      "sha256": "5e5a249134a4862da08646af3666e0f31d61c54779fa1ea5eda8ad57b5f66c65"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: normal-view-craft",
        "open blocker: basic-form-and-scope",
        "open blocker: deliverables-and-label",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/montsechia-original-legacy.json",
      "sha256": "039d949a6a915d97cefa056e0c8032e0853b2850f1104abb297c0c26997fe211"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-21.json",
      "sha256": "67271125e8734b376abec4e930d2a10709651d1b374aed9843ebf2ea3bf5e8fa"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-21/final-handoff.jsonl",
      "sha256": "be0d64cf314dab339f3bb9c8435be327cf3c055de4fed04503f181dc6f0cb6a0"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/montsechia.json",
      "sha256": "20094664f3d9ad74302eb72d90392d7b4d997fa8d9db7ee8fde1d97a0dd7da8f"
    },
    "dependencies": []
  },
  "dollocaris": {
    "id": "dollocaris",
    "batch": "21",
    "source_commit": "76872051f73176326d40df9ac4dafbc0dcc9583c",
    "review_commit": "5873b94ed3ed5f3c9a9dabb1e4c4464082c24f4f",
    "handoff_commit": "f78c36446e13cf12e335c152a37096e53859813a",
    "review": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-21/reviews/independent-leon/2026-10-18-independent-qa.md",
      "sha256": "68044acea79d91262dbf9f05107b7eaddffe9603d73258dfcbd4efda4d5338b9"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/candidate.json",
      "sha256": "bde47c9e89c251d63781ad2ef69f41421c512a572e992fc997e37d3d2ddcd193"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/metadata.json",
      "sha256": "966b10ffc7f9d18759707280b4e4efffb002806fbcc895359da91e0f37af9cdb"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/dollocaris.glb",
      "sha256": "5ea5da44c0b7fb0f22110ba5d86686863d67c260802700c9d1dd8a542f58c284",
      "bytes": 124824
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/dollocaris.blend",
      "sha256": "32474bf5cba324bc487e8ba73fdbb2e077211b219a09521dd6b809c584ac40d1",
      "bytes": 759444
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/render-manifest.json",
      "sha256": "003b46b801cf84edd51a3ebc628a346edd03916fa978867f99410dd8143eea1d"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/runtime-report.json",
      "sha256": "018a901ec232d6292cd747a5294ebea3a116c8d0dff6916633bb51e1196868f7"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/runtime-report.json",
      "sha256": "018a901ec232d6292cd747a5294ebea3a116c8d0dff6916633bb51e1196868f7"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/source-export.report.json",
      "sha256": "17f4d390c31bd1ad5834ecd0bcb7e27c02f9837676adb0e057c1f14496f755b1"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/gltf-validator.report.json",
      "sha256": "b0a3f39630c7ec4ec8f79177f518663b2a0a3df668c5b4054538d7272ecd05cf"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/candidate.json",
        "sha256": "bde47c9e89c251d63781ad2ef69f41421c512a572e992fc997e37d3d2ddcd193"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/dollocaris.glb",
        "sha256": "5ea5da44c0b7fb0f22110ba5d86686863d67c260802700c9d1dd8a542f58c284"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/brief.json",
        "sha256": "91a4f496e00cf0bc8ebe37dd7f390cec41e4791e688840294507a8d46014051d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/references-profile.json",
        "sha256": "6741c2234fa5444261194cab47f6276b41d8f4be0b28fbb89f96c1fd0a6fe505"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/dollocaris.blend",
        "sha256": "32474bf5cba324bc487e8ba73fdbb2e077211b219a09521dd6b809c584ac40d1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/build.py",
        "sha256": "236e143e5acf6244431e8064ef40dea863140ce247936f240a13ccb067330732"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/config.json",
        "sha256": "2fc30efcc9878e125afa82847df12a6fc757c6d3d74ed63c50e248afe4c7b765"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/render-manifest.json",
        "sha256": "003b46b801cf84edd51a3ebc628a346edd03916fa978867f99410dd8143eea1d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/metadata.json",
        "sha256": "966b10ffc7f9d18759707280b4e4efffb002806fbcc895359da91e0f37af9cdb"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/references.json",
        "sha256": "6741c2234fa5444261194cab47f6276b41d8f4be0b28fbb89f96c1fd0a6fe505"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/references-profile-mapping.json",
        "sha256": "36a43f809cd7a3ae00de84a796c22fa852c231e9185e3221139993981c0f1b4f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/reference-access.json",
        "sha256": "2240f00ab8c6540b780412ce5713654989557afa845586f688b0a885c483430f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/profile-contract.json",
        "sha256": "8c827fc411c6d6b5741b890b6a604bc6047e513f9a0be7690fd426375031562e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/profile-policy.json",
        "sha256": "7e46864e40eb64411f9ea3296d91948ed833a3422faa503ee4024e9339d388b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/evidence-manifest.json",
        "sha256": "526fcffeb6fd9cdca67722e9a4a3e11d992680447f1f4e11098edf64ea5adf39"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/source-export.report.json",
        "sha256": "17f4d390c31bd1ad5834ecd0bcb7e27c02f9837676adb0e057c1f14496f755b1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/source-mesh-measurements.json",
        "sha256": "1fdd48a1f67210905544993b5c5600241fb0099b220260728f0d0e7fc0e7af9d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/profile-checker.report.json",
        "sha256": "fc083078022838bd2b073f60d61db0b325fe96628305fc40f36e6546f8060dc5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/profile-approved-check.report.json",
        "sha256": "fc083078022838bd2b073f60d61db0b325fe96628305fc40f36e6546f8060dc5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/project-checker.report.json",
        "sha256": "22b1e08b7393bb467961136c29f8fecbe0a3fc30732f49f30fb9255d26e24f6c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/checksums.sha256",
        "sha256": "97d798effedea566e23b30a80df795aafb0218666da839023a0c0738b6ba2aab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/HANDOFF.md",
        "sha256": "844342420288ff9cc6ccb8b5aa680fd43379056093e2567fed12abac89c6c5b7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/serial-execution.report.json",
        "sha256": "84a0f26b092ee6892a57218357f6beaf8be61e37bce5aff38eb78328a52ec759"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/preview-hero.png",
        "sha256": "3c0da8920780eab6c5cfe58bf6c208ab9b953261bab66ae289530ee447dc7cb6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/preview-reversehero.png",
        "sha256": "bd9a6048bc5721bbad4a900a1847e1cfc192545ac4fb2805876f46c400801c5f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/preview-front.png",
        "sha256": "d6bad97336bbe33e09dcd7aebb51766add4835472bb7d1d2f78178cad0967f38"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/preview-side.png",
        "sha256": "9e6d9257b787fecc1ee7158c2b44543032395952bcb584c1a8f69ba7dd923e55"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/preview-rear.png",
        "sha256": "55fbe4ae9d735c42f65b47921ed43ce389fdaa867c9ab0fa9b2490e6c481bb37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/preview-top.png",
        "sha256": "73ad1c8bac8df273b4906e0265710b8ec334fc129fcf0ee6bef1a0ad5dd445fc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/preview-clay.png",
        "sha256": "64d3a9960a8b68bf5600ce6d2e76d13023430f9e7eaf37e8e6f599e92379d49b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/preview-silhouette.png",
        "sha256": "012464fce255548595010c8d2f98ca9d3e609cb5201f54168d954084c2bcff56"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/runtime-report.json",
        "sha256": "018a901ec232d6292cd747a5294ebea3a116c8d0dff6916633bb51e1196868f7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/front.png",
        "sha256": "0925214dd6be85359fc52ce2630ef1e73bd21bff1af8c5c415c6bc8683353f89"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/hero.png",
        "sha256": "c67fd11b315f59dc669e313accf69a1e0ef3e7b1806ad9c0082d8af9dfd1c3b4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/near.png",
        "sha256": "de9aff6a5c9b05adc11fe4a4c10e152b6dd82732132acf990c57c0919238e0f2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/reversehero.png",
        "sha256": "e83324a25716ad3d5597d74cd111b9d854eec01b756c76416d384d2c794b2259"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/scene-9-copies.png",
        "sha256": "de5d5129b21cde55e8c63b81ca75fa69c1fb9b5b9b96435dec81c0d21cf9e840"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/side.png",
        "sha256": "533480d26a5d94d055c1707bdee62f97f12e796e67c92fc4ca4cd9a19ad74155"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime/top.png",
        "sha256": "0c1ca40bd258ac0a09858a31d78024810889039532cac2a91e5d271309766970"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/view-manifest.json",
        "sha256": "719bed003062233b1c2298b0aefebb15481d1df22aef8a6f7a9ba4688dcc4c7d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/views/transparent/preview-hero.png",
        "sha256": "e8c65ec1b29c11083adfff2811a46429af83bd8ed7351b919cb2eab63eedd9ec"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/reproducibility-1.report.json",
        "sha256": "7e876deff79977d1bd53f4567750552ad0565ec44590708027d4a4d3937bc405"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/dollocaris/r001/runs/build/dollocaris/r001/semantic-rebuild-1/8fef53bb66c70f1769a5ba11b18bb487361edc1cc0300d2728a0bb4a2659dc5a/20261018T214155-322b004bef234afeaad66e968b931735/request.json",
        "sha256": "47657429dde18308ef0ab975f63ed431a7f5df37d8e0659c260fa02358eed9c8"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/dollocaris/r001/runs/build/dollocaris/r001/semantic-rebuild-1/8fef53bb66c70f1769a5ba11b18bb487361edc1cc0300d2728a0bb4a2659dc5a/20261018T214155-322b004bef234afeaad66e968b931735/result.json",
        "sha256": "659c3cbdfcefa1a1dd06fbfa2460b800237041bd70adb785ae1516483ccab28d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/reproducibility-2.report.json",
        "sha256": "9bcdf3ab8ac50e2bba1201936338bfd139ccfa0fe4aeff16cbaa4191853aec0b"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/dollocaris/r001/runs/build/dollocaris/r001/semantic-rebuild-2/84ddf8e2795d28ab9d96a3c403fbd54a49c32ff0559a460848e9e26b5ec0709a/20261018T214157-9a6fec3a5be64ac59c22ed64fdd839a4/request.json",
        "sha256": "aae869a056a1000cf9d67d3814ad491d34249258fd4423bc9452656bf51edf20"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/dollocaris/r001/runs/build/dollocaris/r001/semantic-rebuild-2/84ddf8e2795d28ab9d96a3c403fbd54a49c32ff0559a460848e9e26b5ec0709a/20261018T214157-9a6fec3a5be64ac59c22ed64fdd839a4/result.json",
        "sha256": "871add39c4f3220f791042548458d3cb154a2a3d6fe53fcfa5d44521356b7bf1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/maker-self-check.json",
        "sha256": "e3159ebd6f49c16c0f70f437f6473b0624e504e7a72886bd0269b623439df1f3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/build-config.json",
        "sha256": "d69767e42fed84eddd5d6cac9e272bde772d6550b4abc6469db7ff83c1cef9e3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/dependency-hashes.json",
        "sha256": "db2eb6bcfad395633aa547c974c4ad10d8db99c4404c77759232cba873dd9893"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/freeze.json",
        "sha256": "23264b5f292a5b995824e277881b0682db0b260009d1ee569ba189ed167327e6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/gltf-validator.report.json",
        "sha256": "b0a3f39630c7ec4ec8f79177f518663b2a0a3df668c5b4054538d7272ecd05cf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/inventory-record.json",
        "sha256": "e696e0cbea4f1d9c607c36a5419f4ed797ec0301202772bcac77379d5f877a8c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/maker-visual-inspection.json",
        "sha256": "204e9468273ef80e78308b5154ed54167900d389fd59c81fc7b2ff934f4ac2b8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/preview-hero.png",
        "sha256": "e8c65ec1b29c11083adfff2811a46429af83bd8ed7351b919cb2eab63eedd9ec"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/qa-contact-sheet.png",
        "sha256": "c06458ddbc010fe74b665eeb74a0760e9aa50cf4ae523e8ca8b04ea7068bf347"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/qa.json",
        "sha256": "6a24e440bf4864f3f4f5d2e1e4741100c3c254cceceabf1ccd85f2fe5b64b73f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/reference-policy.json",
        "sha256": "6135a2ee5042b82db2ba50413138651b8e9e0c4bb15f0390786650697639f752"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime-contact-sheet.png",
        "sha256": "145c732939637bcac955aaf4be8433b62834abdf9b0c67d5d9eec18235927316"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/dollocaris/candidate.json",
      "sha256": "927dc2d05da924e9d6e1a30cfe8d5923d8c19c9a5f529bed32893f108ca4b237"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/dollocaris-contract.json",
      "sha256": "bd9f81f1bbaf4c8ff89fefbe1fd6b1754c42104c48ff7f29484c47600d2d65fa"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/dollocaris-result.json",
      "sha256": "d0e2b9fa5a7b437ec3126befcbcd2bbf118153937cb99c8ac47c1c6dde32c9a7"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: normal-view-craft",
        "open blocker: basic-form-and-scope",
        "open blocker: deliverables-and-label",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/dollocaris-original-legacy.json",
      "sha256": "22b1e08b7393bb467961136c29f8fecbe0a3fc30732f49f30fb9255d26e24f6c"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-21.json",
      "sha256": "67271125e8734b376abec4e930d2a10709651d1b374aed9843ebf2ea3bf5e8fa"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-21/final-handoff.jsonl",
      "sha256": "be0d64cf314dab339f3bb9c8435be327cf3c055de4fed04503f181dc6f0cb6a0"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/dollocaris.json",
      "sha256": "82299100673d313045e47a1044232aabd3e4215aa9c91fe06efb4d7398def97d"
    },
    "dependencies": []
  },
  "coelurosauravus": {
    "id": "coelurosauravus",
    "batch": "21",
    "source_commit": "8d223a9bd8eb46478bfee41b7c091ca0456b925b",
    "review_commit": "5873b94ed3ed5f3c9a9dabb1e4c4464082c24f4f",
    "handoff_commit": "f78c36446e13cf12e335c152a37096e53859813a",
    "review": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-21/reviews/independent-leon/2026-10-18-independent-qa.md",
      "sha256": "68044acea79d91262dbf9f05107b7eaddffe9603d73258dfcbd4efda4d5338b9"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/candidate.json",
      "sha256": "2f4e6872eaedeafdc4e614fd82e7f77c3e0bdc779ff391ffee668733b76b435d"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/metadata.json",
      "sha256": "80d21af5f717de5626ec72f66c4457ed943fdde586661d90488c84020c7e7f64"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/coelurosauravus.glb",
      "sha256": "7cee9840fa5dc80192df77f9b2486a926aa17f9d9bbf2ae282f0dfa900fb750e",
      "bytes": 126560
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/coelurosauravus.blend",
      "sha256": "c2ede59ba2df6695113ac23416023b5eed2b16c6c95de9390fd46b57e1fb9124",
      "bytes": 759992
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/render-manifest.json",
      "sha256": "a5f035502ef907db7e7d5abca1ae8359a8c713657b14bac9e567ce0e55606643"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/runtime-report.json",
      "sha256": "c192cc03cbcdd4f5874c002489653210f7e163b9c6f744178759345626b65426"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/runtime-report.json",
      "sha256": "c192cc03cbcdd4f5874c002489653210f7e163b9c6f744178759345626b65426"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/source-export.report.json",
      "sha256": "d1e44d63fe68464e6046e21679c2128b099f28c1cdd7a5ab1d1e8dd10c016849"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/gltf-validator.report.json",
      "sha256": "cb980d24759f2adbad47ba6505aea99f547daa07fcf6d1ca1593fcdee62915f5"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/candidate.json",
        "sha256": "2f4e6872eaedeafdc4e614fd82e7f77c3e0bdc779ff391ffee668733b76b435d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/coelurosauravus.glb",
        "sha256": "7cee9840fa5dc80192df77f9b2486a926aa17f9d9bbf2ae282f0dfa900fb750e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/brief.json",
        "sha256": "e755d9d53074740149aaf25163678a8b03dc2a1ab0e04d45f89db4b66863776c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/references-profile.json",
        "sha256": "fbf6fa9f2c20ac1c0da99b9f2fced4be68f98dee9c65678d3c65f3364c53262b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/coelurosauravus.blend",
        "sha256": "c2ede59ba2df6695113ac23416023b5eed2b16c6c95de9390fd46b57e1fb9124"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/build.py",
        "sha256": "236e143e5acf6244431e8064ef40dea863140ce247936f240a13ccb067330732"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/config.json",
        "sha256": "c7899345c9d82717601bf5a88efbda4684f01f07696dbcb7449dec82a8d82f10"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/render-manifest.json",
        "sha256": "a5f035502ef907db7e7d5abca1ae8359a8c713657b14bac9e567ce0e55606643"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/metadata.json",
        "sha256": "80d21af5f717de5626ec72f66c4457ed943fdde586661d90488c84020c7e7f64"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/references.json",
        "sha256": "fbf6fa9f2c20ac1c0da99b9f2fced4be68f98dee9c65678d3c65f3364c53262b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/references-profile-mapping.json",
        "sha256": "499246ef410db129289ad3066406fe2f302b48e97868b73a13388cf23b153402"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/reference-access.json",
        "sha256": "97c37c12ca369c5d161a19f6c9c71d7b061b3ab524edbef856a0656fd49de5e2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/profile-contract.json",
        "sha256": "2fb5680ffe99c339ce4a0864737c52485b04c621d49d64ed7d2dc69c712f5d37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/profile-policy.json",
        "sha256": "7e46864e40eb64411f9ea3296d91948ed833a3422faa503ee4024e9339d388b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/evidence-manifest.json",
        "sha256": "ab76d02fc225c689b1ef0285c0b976575102a8b443ca894837189c30c4d30ad8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/source-export.report.json",
        "sha256": "d1e44d63fe68464e6046e21679c2128b099f28c1cdd7a5ab1d1e8dd10c016849"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/source-mesh-measurements.json",
        "sha256": "7f39a7664fa7aa9a43e9c31cf302584081adf5f4c3c24165e7b4b7cf2cebfd18"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/profile-checker.report.json",
        "sha256": "f0d4e26241a618ec5b8f2362c99c3d9509dbe5e90e75c27cb01db62d3e539cee"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/profile-approved-check.report.json",
        "sha256": "f0d4e26241a618ec5b8f2362c99c3d9509dbe5e90e75c27cb01db62d3e539cee"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/project-checker.report.json",
        "sha256": "d56b94bc4524c9dffeca2dc240c0a0d2deb5a0453258a9748c47d41d63b03b8b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/checksums.sha256",
        "sha256": "c3ae6b85d1dbbf42ed5b060c70d503d67eb3a532dbbf5cdf89b28141dda7e052"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/HANDOFF.md",
        "sha256": "9da16189593d56ca4c0015ec11c856654491b87985495549198f54ebc833744a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/serial-execution.report.json",
        "sha256": "d59f1a9c7c12354f40e4723269920a22cb814e3b03ac46af763ae8edfbf792b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/preview-hero.png",
        "sha256": "b2f9061e13bd5926e930832583e53fa5275662f0f01bf5b8afd312e9dec5a943"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/preview-reversehero.png",
        "sha256": "7340007544764eab4925afd9454a831ade0b80d8b319ca5c322cdc0cbdbeeeaf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/preview-front.png",
        "sha256": "897693621b3db1613eba0f8f3f0270337c897845b8995d29a6fafb620558614a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/preview-side.png",
        "sha256": "c728e100efa246e9c022c0485f104e968574505157f52f8d05a1a8460332dae3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/preview-rear.png",
        "sha256": "740a627cb0c046c3e2f633d45736abe4f97c962deaf29b6a3a0ab3353588eaef"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/preview-top.png",
        "sha256": "de369ce65f959c58a85243fb7d8896f35fe3fdf9e496afc6d54da4f206137b94"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/preview-clay.png",
        "sha256": "a9184adfc932155d37297806cc0b31f352fde56ca367b1e98feeecdd7c4c90d3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/preview-silhouette.png",
        "sha256": "ce4903a6ea00808b1f8fe6031d7a3a8403cda304911ff1fcf8a284dfede19054"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/runtime-report.json",
        "sha256": "c192cc03cbcdd4f5874c002489653210f7e163b9c6f744178759345626b65426"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/front.png",
        "sha256": "441f7491be05498fc67cfbfc809bd31a647346abeff5cf469be9a050076f5196"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/hero.png",
        "sha256": "8b036ffef4db87b65508e31bcc46bd88cb30e5743d1b3f99ac32a59471e9451a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/near.png",
        "sha256": "0fd63480e1c1b8e0765a699e8141475ca83fcb38f7bcd1361488153654acd649"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/reversehero.png",
        "sha256": "6552ae52221cf61bbcddadc00358db57956250bb654531c785559c0b245b6b3b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/scene-9-copies.png",
        "sha256": "dc7bb5a1a9aeb011737dc0ff93a9c1bae90e02b7fb70ab3b2ddfef7ca3b2adc4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/side.png",
        "sha256": "264eb40bad8c0a355f5048c50172a20eb63f66c4f9208c2e65719081b3cc5cba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime/top.png",
        "sha256": "8b956dde9b94625ba6028ce45e73d47380bdbde00e59b2196346743fe62033d1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/view-manifest.json",
        "sha256": "687abf5b487e456d398f031917b2d1de59b2b3728dd16d100edde44668cb7b2b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/views/transparent/preview-hero.png",
        "sha256": "f4d1add2e6706254f75acde29d944e022c60e20196b562e1837c4e0fb35d09be"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/reproducibility-1.report.json",
        "sha256": "0314ce4e76f170d7c68108c66de474b1669c51288ad3b8ba461b0f0b8eb7be95"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/coelurosauravus/r001/runs/build/coelurosauravus/r001/semantic-rebuild-1/a0f94eedd5586e0c754596ea1052e6047174b7d05e1ae88d1b285bd057a54d69/20261018T214344-97ef6c000d2742c591096783d1985335/request.json",
        "sha256": "ec1b83b5684673b3eed8dfd9c49efa1484986ec1b73b58122f4c5a4b2cf01d0a"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/coelurosauravus/r001/runs/build/coelurosauravus/r001/semantic-rebuild-1/a0f94eedd5586e0c754596ea1052e6047174b7d05e1ae88d1b285bd057a54d69/20261018T214344-97ef6c000d2742c591096783d1985335/result.json",
        "sha256": "724daf518e38a31dbe3e5d970d334b0ecc9bc81bf3be24ab8c09e393997c9e3b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/reproducibility-2.report.json",
        "sha256": "d8336a626bc97e5dce942c49d87dc03d2ae6711c310ffbdfa5ec0b9ea1d2dbec"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/coelurosauravus/r001/runs/build/coelurosauravus/r001/semantic-rebuild-2/6c1b4c3152dccbbe1b9bea48db7b42fe568dec6a4f23826df0aacc9bb5723c23/20261018T214346-9dfa1271111249dba3b39da816f2cebe/request.json",
        "sha256": "d92a31e67b48dc2cfede899bd61382b557a49686ba593c2d60e184f8c547abf4"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/coelurosauravus/r001/runs/build/coelurosauravus/r001/semantic-rebuild-2/6c1b4c3152dccbbe1b9bea48db7b42fe568dec6a4f23826df0aacc9bb5723c23/20261018T214346-9dfa1271111249dba3b39da816f2cebe/result.json",
        "sha256": "43e8a5622ec9df03185f55903c506c21bc8bdbbf20e9300b76f24fbf20f3faba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/maker-self-check.json",
        "sha256": "cb17ad125d61092b54ad738ad273cb349ec2b40a6ebd8199c70784d5ca068590"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/build-config.json",
        "sha256": "b3d0ca121e1dbdee507662d763869ef25acc5e127ab4a1bc6bdfd6ce5d23a50e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/dependency-hashes.json",
        "sha256": "72e25c7263810a401c58e2363973231d53ea3079bfde9e6c69fa4952b86044ee"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/freeze.json",
        "sha256": "31e089b2c0bdf6412edda8f38f293b1da02a7073b6e26e345576ba36664b667e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/gltf-validator.report.json",
        "sha256": "cb980d24759f2adbad47ba6505aea99f547daa07fcf6d1ca1593fcdee62915f5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/inventory-record.json",
        "sha256": "ff9f041c8b7a362aea077eb05b800a0dee63b48783bd24cd5f79a6efbb336ce0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/maker-visual-inspection.json",
        "sha256": "dc809fb4d2c36006bfc49e425667af20603911a63d7e67f47571f021da3b8367"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/preview-hero.png",
        "sha256": "f4d1add2e6706254f75acde29d944e022c60e20196b562e1837c4e0fb35d09be"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/qa-contact-sheet.png",
        "sha256": "1e821651586c6aa7d2e27ddfe22c78efff71012c78c324bd13d10994018499ca"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/qa.json",
        "sha256": "541f5bd4d866a5830e9e018f327b960631ce2beac14cdbdf687a7207059b6797"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/reference-policy.json",
        "sha256": "6135a2ee5042b82db2ba50413138651b8e9e0c4bb15f0390786650697639f752"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime-contact-sheet.png",
        "sha256": "c79b628d1acee88b17e76b39c55672d79e6f3e3b10979fbe5921dfdb0953162c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/coelurosauravus/candidate.json",
      "sha256": "01fa5e74e3d77440bc1a9fa65bdac667f6f7530d3fc274dff0793580df4a291b"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/coelurosauravus-contract.json",
      "sha256": "117a8c76a93ddb6bef56f2edb475e51369f2a9a02d6d39dd136465023711249e"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/coelurosauravus-result.json",
      "sha256": "2f8bd92730c9beafbef20eddc7a8a71470266b73ae6bc3ebfe8b0260b4ea6024"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: normal-view-craft",
        "open blocker: basic-form-and-scope",
        "open blocker: deliverables-and-label",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/coelurosauravus-original-legacy.json",
      "sha256": "d56b94bc4524c9dffeca2dc240c0a0d2deb5a0453258a9748c47d41d63b03b8b"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-21.json",
      "sha256": "67271125e8734b376abec4e930d2a10709651d1b374aed9843ebf2ea3bf5e8fa"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-21/final-handoff.jsonl",
      "sha256": "be0d64cf314dab339f3bb9c8435be327cf3c055de4fed04503f181dc6f0cb6a0"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/coelurosauravus.json",
      "sha256": "92a39a1fabaaf1f6f73b744241214c6b3193992c65bcaa45ceb80548480a6c57"
    },
    "dependencies": []
  },
  "columnar-jointed-outcrop": {
    "id": "columnar-jointed-outcrop",
    "batch": "21",
    "source_commit": "49ecdbd68c9f93e8cd9566a837937c5cf588f9f9",
    "review_commit": "5873b94ed3ed5f3c9a9dabb1e4c4464082c24f4f",
    "handoff_commit": "f78c36446e13cf12e335c152a37096e53859813a",
    "review": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-21/reviews/independent-leon/2026-10-18-independent-qa.md",
      "sha256": "68044acea79d91262dbf9f05107b7eaddffe9603d73258dfcbd4efda4d5338b9"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/candidate.json",
      "sha256": "d1ad386278880808404de43b7c51949877c96b7b6f327eca42d2c206482aa43b"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/metadata.json",
      "sha256": "bda334b30ee5c872103ab49c96801a421462e8eb6670e4fff23a07a47bf1a9d3"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/columnar-jointed-outcrop.glb",
      "sha256": "c7fe274488d63ad1df65c0e68362104271c47f9629d95e1abd9c83adfa723f96",
      "bytes": 38692
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/columnar-jointed-outcrop.blend",
      "sha256": "ff91872ca1b1bdb1019d78f909708742c91303656210694138bea0128be16385",
      "bytes": 506676
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/render-manifest.json",
      "sha256": "6c1adb05c7719dd35291a9a830c9e6f5d88ac1c5b18babb61e278926df317970"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/runtime-report.json",
      "sha256": "f23ec6278d00ceb8e4180ad0a56dfac2336235abab1102d45e9de0b0e8dfa5b9"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/runtime-report.json",
      "sha256": "f23ec6278d00ceb8e4180ad0a56dfac2336235abab1102d45e9de0b0e8dfa5b9"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/source-export.report.json",
      "sha256": "fca462615fbc9950e3a504d0ab907b90a111ccc400c9af38604f1daccb7ded4e"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/gltf-validator.report.json",
      "sha256": "5fa21afff0aef4d22690d8a698d4e1692e74a121119a359cefd29ea416441db1"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/candidate.json",
        "sha256": "d1ad386278880808404de43b7c51949877c96b7b6f327eca42d2c206482aa43b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/columnar-jointed-outcrop.glb",
        "sha256": "c7fe274488d63ad1df65c0e68362104271c47f9629d95e1abd9c83adfa723f96"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/brief.json",
        "sha256": "46e3542afb2679374021ac6ec9d163f590f0158957a0e572693a7dc509647206"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/references-profile.json",
        "sha256": "3ee3b91d62e4fc72788364544614f21de33222e68c942bb5192918ab4d896e43"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/columnar-jointed-outcrop.blend",
        "sha256": "ff91872ca1b1bdb1019d78f909708742c91303656210694138bea0128be16385"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/build.py",
        "sha256": "236e143e5acf6244431e8064ef40dea863140ce247936f240a13ccb067330732"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/config.json",
        "sha256": "a8c73189643a6bb05249ef2023c438b2690a53e3376366865e414bc8e9fa3c22"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/render-manifest.json",
        "sha256": "6c1adb05c7719dd35291a9a830c9e6f5d88ac1c5b18babb61e278926df317970"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/metadata.json",
        "sha256": "bda334b30ee5c872103ab49c96801a421462e8eb6670e4fff23a07a47bf1a9d3"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/references.json",
        "sha256": "3ee3b91d62e4fc72788364544614f21de33222e68c942bb5192918ab4d896e43"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/references-profile-mapping.json",
        "sha256": "64d372d3a2290b54e0e78338412ff9a7b31f06ee465baae1310d19da0caa9f3f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/reference-access.json",
        "sha256": "8e747d951fcb3bc327e47830be5557e33bafc4cf0822165ada61aeb751ba5eea"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/profile-contract.json",
        "sha256": "2e98bcd61e5d7de28c96072e3688df5aeaafba12c008754c0c9e8b1e76717887"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/profile-policy.json",
        "sha256": "7e46864e40eb64411f9ea3296d91948ed833a3422faa503ee4024e9339d388b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/evidence-manifest.json",
        "sha256": "0d77c75d802b232aaf4d6d13cf4acb693edc03141b6f49ac9eaacbd3852b52a2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/source-export.report.json",
        "sha256": "fca462615fbc9950e3a504d0ab907b90a111ccc400c9af38604f1daccb7ded4e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/source-mesh-measurements.json",
        "sha256": "70568e8c625c58517d0d339cc9a38283d7496b421bc0eafa2210f76b6c4aa37f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/profile-checker.report.json",
        "sha256": "d7182064ae806ae2cb45893defc72025916de738d7c508a863a6ae983683eb08"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/profile-approved-check.report.json",
        "sha256": "d7182064ae806ae2cb45893defc72025916de738d7c508a863a6ae983683eb08"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/project-checker.report.json",
        "sha256": "6e0fba14e1c9a829afde9b3c906f080d801d30077df890f034e738d1f628a2d9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/checksums.sha256",
        "sha256": "7d8dab34a4511f3823771eac85e0a86a7757c27b40c18b1d2ec8ab001fd6a0b2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/HANDOFF.md",
        "sha256": "9c301d03d97d81aa5f1ed7acdcb2e45138be6a557a9eaa1e88723d16a5536543"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/serial-execution.report.json",
        "sha256": "a606dce43d7facdafb75ed4d627b9c130018273452052e5e16235caecf99c203"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/preview-hero.png",
        "sha256": "b94a2690fb9995b9f2fe3ae7e33010a0427f394adba473976e6e03a74bcba9aa"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/preview-reversehero.png",
        "sha256": "ed63ec6743861d77b2cf1766ad2ec8e9e02d85c0b448a488baa60cae9465b8fb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/preview-front.png",
        "sha256": "e135478158a3d24a0c1edeb01af3a18d0532cd5c13d31dc2e566402a0761286a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/preview-side.png",
        "sha256": "93a10e4204396f4d0948c9c9000d716f8570cb9cb107e35d6de216bfa08b8704"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/preview-rear.png",
        "sha256": "eac1e288a4120e4ee7ce781f6bd5ba0db4ac0845bf1b7e1acfe2e6f090ff77ba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/preview-top.png",
        "sha256": "ff4d70db94e266d303d8d3a9e49884116506aeab93a03d2c8fa7e015f456dce8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/preview-clay.png",
        "sha256": "81ae5297b837282479630a148fea36b2fb5742d19d40fddf68d5fe669184a05e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/preview-silhouette.png",
        "sha256": "0bb3aff972819f55142ae8301f1b193f28070af4e91a441a27922192d1052c9a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/runtime-report.json",
        "sha256": "f23ec6278d00ceb8e4180ad0a56dfac2336235abab1102d45e9de0b0e8dfa5b9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/front.png",
        "sha256": "46959ea14c322f5a61b92ccb41973cc77a0e6908399d34534b21775f866639b1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/hero.png",
        "sha256": "438feec9e5a22040353ed7292255e780272f832325f7526b1cf5eb4f69c52a51"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/near.png",
        "sha256": "919d16abdff81334fb76e9debc051db6521405651128f8dfa345e596a9524b02"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/reversehero.png",
        "sha256": "553dcd12fe099c0695d1d7fa56c147c62c1110fb8a1543d072376e6a7ae25251"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/scene-9-copies.png",
        "sha256": "0cc27eadfd52f32fd11497392668b6fe52271ffe8570c6833a36170fae0ea698"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/side.png",
        "sha256": "103d582f12aafa8e509e268450e2cff9198dfd9f61aeeefe8bfd3b3790419581"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime/top.png",
        "sha256": "f3c41c24196d8b4f9798765b39e5079563d1996c0f576da4a4ed98ce6acd1ae5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/view-manifest.json",
        "sha256": "f8c54d6d727c6c58b4f5c713b8dbba9ad5278dfed21b520f2f796be45144d548"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/views/transparent/preview-hero.png",
        "sha256": "5f08ce4ec2c9988cdb62c75f6b2f7adf7bf04e156da514c9d04c6ab6c819439b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/reproducibility-1.report.json",
        "sha256": "784bd524857bcf3a45afc5054986a47a2fcb7f62e8c727827f4267b84ca01fd2"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/columnar-jointed-outcrop/r001/runs/build/columnar-jointed-outcrop/r001/semantic-rebuild-1/b20eca3c88ac923a1d952b838e5577d01bfca23e6c3d5beb75f527d32e998269/20261018T214527-b40a4e4185e84a69b6399eb698ae6fb1/request.json",
        "sha256": "0d4a56373272b5d05a018ae99aa8d1163dcc888c86a69d08eb8dfef7f39cf688"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/columnar-jointed-outcrop/r001/runs/build/columnar-jointed-outcrop/r001/semantic-rebuild-1/b20eca3c88ac923a1d952b838e5577d01bfca23e6c3d5beb75f527d32e998269/20261018T214527-b40a4e4185e84a69b6399eb698ae6fb1/result.json",
        "sha256": "1cf88b103bb96cd1ba7a53a3afb6ed1f8d5a049a57c84b0acdb8dea8b19e49da"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/reproducibility-2.report.json",
        "sha256": "eaa03de1dec1b02e56090dcdfe5d68c67bc46ef464aa780ee5101d3aae911193"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/columnar-jointed-outcrop/r001/runs/build/columnar-jointed-outcrop/r001/semantic-rebuild-2/6241a43c7742ebb3c71b8c4bc7b85c58a43141006e15d89b0acd154f59a4bf0a/20261018T214528-db0e8618493349a09d87148dc6e02df4/request.json",
        "sha256": "bcdf6fb4ec4dc6fe994ad26360a046b0dafb37cc855731a4831efc1bd4a04030"
      },
      {
        "path": "production/continuous-small-life-round07-20261018/work/batch-21/columnar-jointed-outcrop/r001/runs/build/columnar-jointed-outcrop/r001/semantic-rebuild-2/6241a43c7742ebb3c71b8c4bc7b85c58a43141006e15d89b0acd154f59a4bf0a/20261018T214528-db0e8618493349a09d87148dc6e02df4/result.json",
        "sha256": "f5422879b84dc0157b036193701d780919b7e116f15c4a7f09685dc17f51495a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/maker-self-check.json",
        "sha256": "39cff8f06c9735e030a50b0fd9064ebb824a7aee341845c2d103e03e27a275ae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/build-config.json",
        "sha256": "46af242e0bc31bcc46afda3aace78f6b6f001142b78877dbc4aa226c3183e965"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/dependency-hashes.json",
        "sha256": "903062a3c95cc8228d35a01079b2e69a9cc19837704dfa21dc6d2c8fbe0d6d18"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/freeze.json",
        "sha256": "21a2738d2e0d4a9fa90fa58a3c1483ed6af0835fdff056423c2f7a79ddd08a35"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/gltf-validator.report.json",
        "sha256": "5fa21afff0aef4d22690d8a698d4e1692e74a121119a359cefd29ea416441db1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/inventory-record.json",
        "sha256": "b48a733892c23f5e18fb53efeafd937ecf7140749497e6aa512da8bd6d2fdc16"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/maker-visual-inspection.json",
        "sha256": "9c5a942150693215d29831a6b634c1bf583c4aa7698f723543409a0972ad881e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/preview-hero.png",
        "sha256": "5f08ce4ec2c9988cdb62c75f6b2f7adf7bf04e156da514c9d04c6ab6c819439b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/qa-contact-sheet.png",
        "sha256": "dd4a07eb9d7a09a0adba5cd3c224ccb12198fd8ddfdf7c4f99c007b8a9ca7b90"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/qa.json",
        "sha256": "b5493a05857002b226ccb5c94cdf2aa3691c115a50998dfcfa14ca8372f60b85"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/reference-policy.json",
        "sha256": "6135a2ee5042b82db2ba50413138651b8e9e0c4bb15f0390786650697639f752"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime-contact-sheet.png",
        "sha256": "94d81bfebdebc44e08b0830c4ef7d132b2435e727a72045b26c6a7d3b5d41d72"
      },
      {
        "path": "assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round07-20261018/records/columnar-jointed-outcrop/candidate.json",
      "sha256": "2639c39ded729042a92e5d8e903dc93d4607812cc4c86936bca0997883b0ef89"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/columnar-jointed-outcrop-contract.json",
      "sha256": "1139efb3d63aaf557c8bc5ec730261438c90fb8de4c90d2ed2d1cff883d43047"
    },
    "profile_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/columnar-jointed-outcrop-result.json",
      "sha256": "4f879313008152acc8c5d557e4408450ddf762c6fe38723e22c78d5a8b6e4cbd"
    },
    "profile_outcome": {
      "valid": true,
      "approved_for_brief": false,
      "errors": [],
      "approval_blockers": [
        "technical: unknown",
        "technical-integrity: unknown",
        "visual: unknown",
        "normal-view-craft: unknown",
        "factual: unknown",
        "basic-form-and-scope: unknown",
        "specification: unknown",
        "deliverables-and-label: unknown",
        "runtime_parse: unknown",
        "target-loader: unknown",
        "gpu: unknown",
        "functional-render: unknown",
        "scene: unknown",
        "representative-scene: unknown",
        "open blocker: normal-view-craft",
        "open blocker: basic-form-and-scope",
        "open blocker: deliverables-and-label",
        "approval: pending"
      ],
      "profile_contract_status": "pass"
    },
    "original_legacy_result": {
      "path": "qa/continuous-release-round07-20261018/profile-checks/columnar-jointed-outcrop-original-legacy.json",
      "sha256": "6e0fba14e1c9a829afde9b3c906f080d801d30077df890f034e738d1f628a2d9"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round07-20261018/qa-bindings/batch-21.json",
      "sha256": "67271125e8734b376abec4e930d2a10709651d1b374aed9843ebf2ea3bf5e8fa"
    },
    "handoff": {
      "path": "production/continuous-small-life-round07-20261018/work/batch-21/final-handoff.jsonl",
      "sha256": "be0d64cf314dab339f3bb9c8435be327cf3c055de4fed04503f181dc6f0cb6a0"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round07-20261018/texture-checks/columnar-jointed-outcrop.json",
      "sha256": "6ffd7b7ec36d0bccf8212ed61160b98f36b45c43a353e7b74d678fc7a697282e"
    },
    "dependencies": []
  }
};
