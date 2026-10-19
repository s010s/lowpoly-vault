/** Immutable accepted payloads and independent evidence; original candidate failures remain explicit. */
export const ACCEPTED_ROUND11_ASSETS = {
  "asaphus": {
    "id": "asaphus",
    "batch": "31",
    "source_commit": "b94453827c90ed71df0087017a48701477944f35",
    "review_commit": "ba33ae2cbd93fc65e423f76ec252f6e66883ce67",
    "handoff_commit": "b94453827c90ed71df0087017a48701477944f35",
    "review": {
      "path": "qa/continuous-small-life-round11-20261018/batch-31/independent-review/results.json",
      "sha256": "07d5804934efd8e213905c3201148782fb5d7a172c235755f2cb370e269dd4d2"
    },
    "candidate": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/candidate.json",
      "sha256": "f88f356abd29a1999a11a43f895995ac488176afe4791c666d82b613ccfb6285"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/metadata.json",
      "sha256": "0e69a4713951d848217b717817b6be75403418556068e8b62c3e07285ec4e3d7"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/asaphus.glb",
      "sha256": "99432ec959c96f6370d9baa1cf416f76f247c414706d9cde57963a4cc14ca156",
      "bytes": 199612
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/asaphus.blend",
      "sha256": "ad62b7efbaa1c22a99078f62bac4f08f435c0341a0c4ec7f3dd36a84d8d5ac8d",
      "bytes": 888288
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/view-manifest.json",
      "sha256": "63b683e2893671f7ba0e4006ee86cf137da30c45028a758875a060c6e2bfb46a"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single.json",
      "sha256": "46dad609ea9b64b6bb1877ec630a19d273edcae805e6a2004a13461e9036d77e"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/scene.json",
      "sha256": "90987087c5e048f02261ee98040754842bfd8655c5053b4fc6c2e693c5187033"
    },
    "source_export": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/source-export.json",
      "sha256": "e0fc1922d897e14c73313f1e089077c9101c5459dca2295fe6fc9ebc6707ba35"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/gltf-validator.report.json",
      "sha256": "00f47b426c43d20a0eb7b579083d97edc2a322dd18151c1af35b5f06c0548d40"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/candidate.json",
        "sha256": "f88f356abd29a1999a11a43f895995ac488176afe4791c666d82b613ccfb6285"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/asaphus.glb",
        "sha256": "99432ec959c96f6370d9baa1cf416f76f247c414706d9cde57963a4cc14ca156"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/asaphus.blend",
        "sha256": "ad62b7efbaa1c22a99078f62bac4f08f435c0341a0c4ec7f3dd36a84d8d5ac8d"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/generator.py",
        "sha256": "7948aae410c0f360bec179c8c249af7efe35ab78c6b8e756bc12b1becdfbc1a1"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/config.json",
        "sha256": "79de0ade112df752a6dc5b1bad0b6d2b0008f7c1de9e2b3fe45145f69d0ff068"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/asaphus/brief.json",
        "sha256": "d8028dad17701113fbe8f93d9ba8059d0f37af9b8bc47001856b40d54f7788c7"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/references.execution.json",
        "sha256": "c7c8bdd83b3ef3f0545f6cc91505bc7e842df17ab60063bbc4694182ed50002e"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/asaphus/references.json",
        "sha256": "6e5e5d1a304f210843f49c3e2f74c9ad157674cbf5a58b5ff3c7b161eb368f7b"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/asaphus/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/asaphus/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/viewer.html",
        "sha256": "5d54ed44faeadae12c3b0f254492f3179012d38a306263453e65c9c406d39d28"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/browser_qa.mjs",
        "sha256": "77e404da289f12b84dfef078fef1e00144422053f666419657e87eb535533cdf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/verify_item.py",
        "sha256": "39bf9985eee1c04287e04022de0d9000926522a7a9259eec9010bb66fb83cb99"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/asaphus/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/reference-access.json",
        "sha256": "ce3599cb436a72bcaa5f5ac8da5509f23b7f65ba5ca72c5591822ea76b641467"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/claim.json",
        "sha256": "cf92c533428f2cab61d83791182b51c876c58fd4fd1b36d467fb38fccf838fac"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/asaphus/inventory-record.json",
        "sha256": "612a68b649bc68d96f8a03687a0851dbcc72046cdf564adfa10f5fb562934afd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/gltf-validator.report.json",
        "sha256": "00f47b426c43d20a0eb7b579083d97edc2a322dd18151c1af35b5f06c0548d40"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/source-scene.json",
        "sha256": "61b567b49427b4fd26f0601c68e8fb603cbd51664022fb8b962ad5755809a6f2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/source-export.json",
        "sha256": "e0fc1922d897e14c73313f1e089077c9101c5459dca2295fe6fc9ebc6707ba35"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/reproducibility.json",
        "sha256": "51a1e9e0fbaa55d02b592a842e0e4e58ea9d87e8f83b14fb8cba8b9510ff8d9a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single.json",
        "sha256": "46dad609ea9b64b6bb1877ec630a19d273edcae805e6a2004a13461e9036d77e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/scene.json",
        "sha256": "90987087c5e048f02261ee98040754842bfd8655c5053b4fc6c2e693c5187033"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/view-manifest.json",
        "sha256": "63b683e2893671f7ba0e4006ee86cf137da30c45028a758875a060c6e2bfb46a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/metadata.json",
        "sha256": "0e69a4713951d848217b717817b6be75403418556068e8b62c3e07285ec4e3d7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/qa.json",
        "sha256": "a6994c9b1d345c319d2ab89834be12ae005e57c93bf25a2a7e1e770ca08a9457"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/source-contact-sheet.jpg",
        "sha256": "49497c3b9928de49f80f1e8a7f09690f334fc923762b22ef3581a160ff487b26"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime-contact-sheet.jpg",
        "sha256": "605e45a6528c40db035baa0f84d45c5c9cd3965da39a4598fcee7473a0bd4937"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/freeze.json",
        "sha256": "d4b32989dccfe90ca21afd3a90d3e0f8ae3829967644d752373a95a0d92f8631"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/practical-integrity.json",
        "sha256": "fcad73651964c636bd629a9720851bcaab03ab602bc8b620a2ecad37fdaf5983"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/profile-contract.json",
        "sha256": "498ad1b9f595136e98e284975626748082186121b4aabee0becf33a2ff2630d0"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/profile-gate.json",
        "sha256": "1603a5c99c90ebc61c72f595160ef849a939dc12d0c5a4714b6d89b9adc3cc58"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/asaphus/r001/legacy-gate.json",
        "sha256": "59fb0461dba40a298e7fcd1b02fe81e3bd67f00652dd823b9c05aba026e4311f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/preview-hero.png",
        "sha256": "566c06f4446fd256c5110dfe6db2228ad936abab1cc2a480bb65ebb851279e8e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/preview-reversehero.png",
        "sha256": "c6c2cb53d87033db210c72dcd3e2cff4693b9f1696af588f760e68136854654d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/preview-front.png",
        "sha256": "744e53bc5bcf8ff17e8051dcbf17aeed0afd66f0b3012f58ba1c983b33e393b2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/preview-side.png",
        "sha256": "7f9ca6c4d4daaaef253f403afc5d392497695c976210d87162a10366025ae33d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/preview-rear.png",
        "sha256": "e81b551061701c3ea0e9fccc7e990015ec29e04e236015e20df7255b3acf393b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/preview-top.png",
        "sha256": "1d59ea9710d8e9450ec52577feb8f5d27338f806d70c1f7bee61d407d0f51c68"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/preview-clay.png",
        "sha256": "472e302c17add522e8ae0c0591aa03b7a45701d03ad570f2426d35903a528fdb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/preview-silhouette.png",
        "sha256": "53d29407ec9d91513d23a6cfa6790412037b802c6c6b987bb6219572ffc2b8f1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-hero.png",
        "sha256": "ddcc0e7ace745665072ccd5719040e1ed575db5507a95f448af836458722aeaf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-reversehero.png",
        "sha256": "dd2d8d10ff46bbafcbf3e188c1f77a23fa73c261c68ceffe83ad9d630f59a06b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-front.png",
        "sha256": "d29b91ee7cffd8a64f94400db6237fa5d3590a2f4beb1c813b73c782ab5b94ae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-side.png",
        "sha256": "34eaeec1fd5a7970d65c7caabb13e1c067b12d71a2248298de53db4c8dd20290"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-rear.png",
        "sha256": "df4094be3d247e329afb0926d5a59e157d6992e54fda773b5380cbf9e5b6a0dd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-top.png",
        "sha256": "672146c98515c757212715113fde6071b02560c96c09797fae43ee152c1106fb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-bottom.png",
        "sha256": "b1f034b7239d481f934d773a0ad78a6aba373869835d72f2d6c7a5f046479fb4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-80px.png",
        "sha256": "8f7e6e06e7469af7db3fbc9dcd4972f30bacbe93d0dc781eb4cded7932873fb4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-160px.png",
        "sha256": "d99ca8444d1402ecf9af01e5373e3c52cea44e77975280960d6b36c548bd3cc3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/single-240px.png",
        "sha256": "e98a65e84f4229c42685575f5a4d8e40625616ea13536ad03dafd5cd4be51f7a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/scene-hero.png",
        "sha256": "c6602d48628d3a65971afcca53916c05cef089164c2dbaef8187e1c41e8ec230"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/asaphus/r001/attempt-02/asaphus/runtime/scene-top.png",
        "sha256": "fd8c6c39b8e53e7d2f031580dc980d426f56b7b0131eedf9fb3934219246641c"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/asaphus/candidate.json",
      "sha256": "d74d0c149144f24d64d6d65fb881a0dd046276f12c499b6869aca49ada8dfa47"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/asaphus-contract.json",
      "sha256": "c6b6b834e5ca9dc50e0d298b404ffda7f73bb76877b535eaaddedabf09fe8cb9"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/asaphus-result.json",
      "sha256": "ca6c27b7b3499b684c1de08ed79f414e20e762d09b23eff38a429f18258cc15c"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/asaphus-original-legacy.json",
      "sha256": "59fb0461dba40a298e7fcd1b02fe81e3bd67f00652dd823b9c05aba026e4311f"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-31.json",
      "sha256": "62f03e3627c02dc22b53a96ecb987aeedfa2387e9ff560509b9bb7c938d37624"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/HANDOFF.json",
      "sha256": "5208b3287332849a0cd92b9a513ae8305c9fa3915d440b6e9f47405c34f6e89e"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/asaphus.json",
      "sha256": "7edb9022c79f53ad72159daf11d235a8e4d153dd215d55448d3058fe890a9fbe"
    },
    "dependencies": []
  },
  "hazelia": {
    "id": "hazelia",
    "batch": "31",
    "source_commit": "b94453827c90ed71df0087017a48701477944f35",
    "review_commit": "ba33ae2cbd93fc65e423f76ec252f6e66883ce67",
    "handoff_commit": "b94453827c90ed71df0087017a48701477944f35",
    "review": {
      "path": "qa/continuous-small-life-round11-20261018/batch-31/independent-review/results.json",
      "sha256": "07d5804934efd8e213905c3201148782fb5d7a172c235755f2cb370e269dd4d2"
    },
    "candidate": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/candidate.json",
      "sha256": "776264a359a658490e4dff5ae516f6d1e2cb067c958f14c57c6c5aee87d0cd3e"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/metadata.json",
      "sha256": "09a4cde04f6c8f02cc24351b9eb7efbb1ab7460579f0a85d8a69d9cd7cbac936"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/hazelia.glb",
      "sha256": "1922a96efff6f35434a4bc29434a22935f9ab44ee06b7f69ddbc2dd286002cf0",
      "bytes": 152600
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/hazelia.blend",
      "sha256": "fd958ad6bd41659114acee19263c2e1123f78184c6248f5a388a5ca83c9ff052",
      "bytes": 753268
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/view-manifest.json",
      "sha256": "9730ebe5b64e5f92b61d6c0df632c1977823f4c60a23b89043b1685dc51c5458"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single.json",
      "sha256": "fb39594d8d19789c9e34b682025c88b56e761ad54e4883822f77fe2e07ba868b"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/scene.json",
      "sha256": "e2186feb575e149d4c6216573c50dc1a32d872abe2633e7a78e99eb944a5f97f"
    },
    "source_export": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/source-export.json",
      "sha256": "d0894eb49df9df2a3fd6540147337a0b06542e2b87c017a4cc26e4f85771aace"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/gltf-validator.report.json",
      "sha256": "8024f288cd35bfa9ef5ed5279e6338b497febaceb1bf33ab34f14ab8746d1777"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/candidate.json",
        "sha256": "776264a359a658490e4dff5ae516f6d1e2cb067c958f14c57c6c5aee87d0cd3e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/hazelia.glb",
        "sha256": "1922a96efff6f35434a4bc29434a22935f9ab44ee06b7f69ddbc2dd286002cf0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/hazelia.blend",
        "sha256": "fd958ad6bd41659114acee19263c2e1123f78184c6248f5a388a5ca83c9ff052"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/generator.py",
        "sha256": "78c55db8cf240e1a55fc6404c05d632d6be42677702c5afe478300cc71e35df2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/config.json",
        "sha256": "4e4f84cc84db3c233abd96b1251bfad4be7bced53d8a60f132746838024b0db3"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/hazelia/brief.json",
        "sha256": "c566a0d62a3e256275ef3eb8cc5d5ec4d1a697f9fbf0d00da18196fd5f702966"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/references.execution.json",
        "sha256": "35deca4bdbe06c628968ca090520514397ab7a791ce0bdb0b28fcf8ad79c1a45"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/hazelia/references.json",
        "sha256": "10979c57fb5d2e9a183c4299fd2a0940d4735f58a9971ac1e2b0792db71f914e"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/hazelia/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/hazelia/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/viewer.html",
        "sha256": "5d54ed44faeadae12c3b0f254492f3179012d38a306263453e65c9c406d39d28"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/browser_qa.mjs",
        "sha256": "77e404da289f12b84dfef078fef1e00144422053f666419657e87eb535533cdf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/verify_item.py",
        "sha256": "39bf9985eee1c04287e04022de0d9000926522a7a9259eec9010bb66fb83cb99"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/hazelia/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/reference-access.json",
        "sha256": "ce3599cb436a72bcaa5f5ac8da5509f23b7f65ba5ca72c5591822ea76b641467"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/claim.json",
        "sha256": "cf92c533428f2cab61d83791182b51c876c58fd4fd1b36d467fb38fccf838fac"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/hazelia/inventory-record.json",
        "sha256": "b9aa45d38796271e44ad3bd4a8f49052c2ca69b8822d7cfe8d53f922f15e5687"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/gltf-validator.report.json",
        "sha256": "8024f288cd35bfa9ef5ed5279e6338b497febaceb1bf33ab34f14ab8746d1777"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/source-scene.json",
        "sha256": "2c72e980fd47c79a293f88c6d6b3484ca5b9ac44936739ea0cc3f49d89aee2bd"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/source-export.json",
        "sha256": "d0894eb49df9df2a3fd6540147337a0b06542e2b87c017a4cc26e4f85771aace"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/reproducibility.json",
        "sha256": "55c93ecd941d0848374be3878b191ef524117e63bf44b62e59055238722746f6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single.json",
        "sha256": "fb39594d8d19789c9e34b682025c88b56e761ad54e4883822f77fe2e07ba868b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/scene.json",
        "sha256": "e2186feb575e149d4c6216573c50dc1a32d872abe2633e7a78e99eb944a5f97f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/view-manifest.json",
        "sha256": "9730ebe5b64e5f92b61d6c0df632c1977823f4c60a23b89043b1685dc51c5458"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/metadata.json",
        "sha256": "09a4cde04f6c8f02cc24351b9eb7efbb1ab7460579f0a85d8a69d9cd7cbac936"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/qa.json",
        "sha256": "27752b4a665afa2f8934012eb4bb07394c924edc6ff2c5948aa01f834844cdca"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/source-contact-sheet.jpg",
        "sha256": "2507534c634ccf0bc56b1329777bcc680601712c4ac3f9c9bde784662fefd6e8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime-contact-sheet.jpg",
        "sha256": "ab639c6417f279cfef7ea140a6a479fabd442e44d4dbb43adb4410a061da4b50"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/freeze.json",
        "sha256": "c6d2ecfd8f23d3ed133e3b65964a222c912ebe39353ad3eabe589dc5aa4037b0"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/practical-integrity.json",
        "sha256": "4b41f3aac2a715174125e167597134a49ce64a2081493a1900853e032f2170f9"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/profile-contract.json",
        "sha256": "08435a31c410bc9f45da9ea7dea85a5c67e08ab2d5ac3d433a8adb88517caf98"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/profile-gate.json",
        "sha256": "f356759d105344d044e817e1650252eceb6fe4226b0e5c7005c5a39e05ed8167"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/hazelia/r001/legacy-gate.json",
        "sha256": "fd6c5addf5b8eab0f802717dc4d83b6dd6f6ef8270ca69ca0316ca915ebd78e5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/preview-hero.png",
        "sha256": "0e2b3234a15527256f93060ee43ea42de9a65e0c8add4dbe81577ead1fdd46fb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/preview-reversehero.png",
        "sha256": "f601ffd73502d9cbb5e35521d0fa5e19a6666795ccc64826591b6478be859309"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/preview-front.png",
        "sha256": "e0e09ce3bbcc0a90caf39717ca1536203f26de11a6dec4acc27ef27445415f35"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/preview-side.png",
        "sha256": "ef37d34e2e8b8ca3f287f1c2d4aa4edeb3d7cff68ccb8b8d46c7d01439baf66b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/preview-rear.png",
        "sha256": "6bbab11e2d1f9a9650594bad8ab296ecb39eb9e031a28fb4d4ad833bad9d9b7c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/preview-top.png",
        "sha256": "c3f69d51ecf472772c5f98bb499d277eafaa043cdd7fbc98159db28e0c1b0d8d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/preview-clay.png",
        "sha256": "20082d4a0b706607eb33c6858069e8fd63a9e425dcecc7b571a023c0c5767b9e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/preview-silhouette.png",
        "sha256": "29516c04fe74c9eb60abf511be4156d8c1479a16d2028842a5d3af067ebb214f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-hero.png",
        "sha256": "40bf345fde412bcde869acef6bb4d5cace1b74ee01824c1ac155ecfd61fdbf8a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-reversehero.png",
        "sha256": "be0e364a46a803c30b22ef05003fee0007dd44cbf9951a556d91a6540740bbda"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-front.png",
        "sha256": "28c67a15306b202d71aa3e66d30b83fdbacf01c2c351ee47a11e6d7542a1b81e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-side.png",
        "sha256": "76c9c1005f0be2ffe4ebc23c857ff3b6b861b8a3ee3363818825057df0b0d3cc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-rear.png",
        "sha256": "037491d2e9f253a83a7f5f4611216a7747ca6ff35a7fe3ae17ae5af5b01a359a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-top.png",
        "sha256": "a7841defdd29dd97b5906b9014328bc0b1b441e1fb14c983870b197b00e3ba33"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-bottom.png",
        "sha256": "4084ecea80c56ed8cf05a8092c34a5cdbc46755f7680754fb29e7c6837a680ae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-80px.png",
        "sha256": "309f7021a327a8a8cdd31bf4874712fc31668feb9a9212ab43fa5d5fa0ccdcd6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-160px.png",
        "sha256": "d1926ef4c053969b1978b7927f98e07df40de5c29fad24aae8a0383b70c4f459"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/single-240px.png",
        "sha256": "98d96b29b66cde17bede209f7d2690d02200dcc47d5f70e3bffd2ced60b08314"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/scene-hero.png",
        "sha256": "75552b0194123bbb955fa12746f358a9f090281a3275ea11074b88e4565d90ba"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/hazelia/r001/attempt-02/hazelia/runtime/scene-top.png",
        "sha256": "e90b26edc8c4b235b2737d27bfb8f8b51b9a72c596d17cf8aef5f34a7bed8b58"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/hazelia/candidate.json",
      "sha256": "acf83d6b73dbc3f88247d904c9621d14e1ecee10fc61576f2cba6b0736f8b1c6"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/hazelia-contract.json",
      "sha256": "ed770122a345b2722db74d28e5849e7073ed4e5da5c1d3ec7d462a74738e03f6"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/hazelia-result.json",
      "sha256": "ae80ac3e2f1c23d7ce3bd147ba52d272f79a2f62fbe188d4569d3d1060879747"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/hazelia-original-legacy.json",
      "sha256": "fd6c5addf5b8eab0f802717dc4d83b6dd6f6ef8270ca69ca0316ca915ebd78e5"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-31.json",
      "sha256": "62f03e3627c02dc22b53a96ecb987aeedfa2387e9ff560509b9bb7c938d37624"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/HANDOFF.json",
      "sha256": "5208b3287332849a0cd92b9a513ae8305c9fa3915d440b6e9f47405c34f6e89e"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/hazelia.json",
      "sha256": "487bb76480f26ef8bc05d2031e1b95fd467958dd04328c12111224841e8b378d"
    },
    "dependencies": []
  },
  "sea-cave": {
    "id": "sea-cave",
    "batch": "31",
    "source_commit": "b94453827c90ed71df0087017a48701477944f35",
    "review_commit": "ba33ae2cbd93fc65e423f76ec252f6e66883ce67",
    "handoff_commit": "b94453827c90ed71df0087017a48701477944f35",
    "review": {
      "path": "qa/continuous-small-life-round11-20261018/batch-31/independent-review/results.json",
      "sha256": "07d5804934efd8e213905c3201148782fb5d7a172c235755f2cb370e269dd4d2"
    },
    "candidate": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/candidate.json",
      "sha256": "84cefe8d00bf9167c70f29bfce4531ea786dc3b53e613b9740d63e698e9eef90"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/metadata.json",
      "sha256": "288dfff4e8360a4543ae2f065c5fbcb9417fb62212596557cad14879621b4371"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/sea-cave.glb",
      "sha256": "31328a5c5075ecd7ad8415850635188d72a2cdf055ff070a5fd0fa5c48b1adad",
      "bytes": 63736
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/sea-cave.blend",
      "sha256": "e251a55acd0fc61f02a27311eea75491ab69b726bb5970e1f85aa22ef975516c",
      "bytes": 582784
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/view-manifest.json",
      "sha256": "3c0b43e4479496502ef2ad1b068c099b1e9a3f11b1dda7c31b0b948ae9e39e31"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single.json",
      "sha256": "051b567ddbbb44fff70702682caeeb799e4a7ad5c98a348e0401439a696d841f"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/scene.json",
      "sha256": "c7d545567a2ee505d4489708e4e2501d3b1ee15617f5e46959714ce9846f2985"
    },
    "source_export": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/source-export.json",
      "sha256": "88c7422ca8da9c843a1ca2e5c028322f679aedb52a6c91013eb3168f18f3f0fe"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/gltf-validator.report.json",
      "sha256": "c26f460d21274397b51b83c703a8d62ff1482d0df30be1a7c36470b0e7a69be9"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/candidate.json",
        "sha256": "84cefe8d00bf9167c70f29bfce4531ea786dc3b53e613b9740d63e698e9eef90"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/sea-cave.glb",
        "sha256": "31328a5c5075ecd7ad8415850635188d72a2cdf055ff070a5fd0fa5c48b1adad"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/sea-cave.blend",
        "sha256": "e251a55acd0fc61f02a27311eea75491ab69b726bb5970e1f85aa22ef975516c"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/generator.py",
        "sha256": "f46947d6864c9cd4158d929a5508e45d2d01dc81f19db73a10e5241775cd13e0"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/config.json",
        "sha256": "9b1d9ba62d3ce67a3845d4ce6187bdfac9da42c04f5965c3324eff4a2492cb11"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/sea-cave/brief.json",
        "sha256": "c337ba1043d17e1b805beca591783887bd7376c0325e2f94a3de806c8da3d8fa"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/references.execution.json",
        "sha256": "70c617a10629d5d38eaf165afa06999e1999807787bc5bb235025c7a61834249"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/sea-cave/references.json",
        "sha256": "200030b1abba8878777f7ba234da66a266cb72a068e4240ee5baa63de8f908fc"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/sea-cave/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/sea-cave/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/viewer.html",
        "sha256": "5d54ed44faeadae12c3b0f254492f3179012d38a306263453e65c9c406d39d28"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/browser_qa.mjs",
        "sha256": "77e404da289f12b84dfef078fef1e00144422053f666419657e87eb535533cdf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/verify_item.py",
        "sha256": "39bf9985eee1c04287e04022de0d9000926522a7a9259eec9010bb66fb83cb99"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/sea-cave/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/reference-access.json",
        "sha256": "ce3599cb436a72bcaa5f5ac8da5509f23b7f65ba5ca72c5591822ea76b641467"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/claim.json",
        "sha256": "cf92c533428f2cab61d83791182b51c876c58fd4fd1b36d467fb38fccf838fac"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/sea-cave/inventory-record.json",
        "sha256": "ea89db80fa32a8a17a6facab045bef1fe1c9ad8c39ecce66171a1a75ab5fc5c7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/gltf-validator.report.json",
        "sha256": "c26f460d21274397b51b83c703a8d62ff1482d0df30be1a7c36470b0e7a69be9"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/source-scene.json",
        "sha256": "79213e7b7ced7a3d9b54e3e4b18cb21ff7a44c795ef260e6c3fafbb73f83d329"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/source-export.json",
        "sha256": "88c7422ca8da9c843a1ca2e5c028322f679aedb52a6c91013eb3168f18f3f0fe"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/reproducibility.json",
        "sha256": "ddebefe64cd6246310712e92642a65e69a1ad18b302fa51ab174f7133997635f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single.json",
        "sha256": "051b567ddbbb44fff70702682caeeb799e4a7ad5c98a348e0401439a696d841f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/scene.json",
        "sha256": "c7d545567a2ee505d4489708e4e2501d3b1ee15617f5e46959714ce9846f2985"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/view-manifest.json",
        "sha256": "3c0b43e4479496502ef2ad1b068c099b1e9a3f11b1dda7c31b0b948ae9e39e31"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/metadata.json",
        "sha256": "288dfff4e8360a4543ae2f065c5fbcb9417fb62212596557cad14879621b4371"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/qa.json",
        "sha256": "4bec69b7b218ed858affa068b9d5cb0e9dca61b91c72a7265f11b9b52c13055e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/source-contact-sheet.jpg",
        "sha256": "7d56941e306f595e7f43ed47be527b4d25f0620fb47020f77f6038dd7cad00bf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime-contact-sheet.jpg",
        "sha256": "f2f91e7c6d859d04c64a45973807d39851137fed3326a0eaa102e64b977728a5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/freeze.json",
        "sha256": "1f5663eafb48946bfa919bd29e52481c50953086ad5dfba27920f6040525f9ae"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/practical-integrity.json",
        "sha256": "42846ae4e193dd93e1302fb6a9de043689112a1ca7b642892538223809fb7d0e"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/profile-contract.json",
        "sha256": "672ccb3f3f117803127e82726e6f6a6665a0b04bf62fbb96b4a9d10cf49bc256"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/profile-gate.json",
        "sha256": "2029de5334431d7d704a6767ea0e8dbdd15984cd9574cd45df19920003a0b139"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/sea-cave/r001/legacy-gate.json",
        "sha256": "fd6c2ad63b1ed96167463310f8acf8efc64a570ec93c154d9af2739d45e39de8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/preview-hero.png",
        "sha256": "8c5eb94db9e92b6ca01c02181f6b0afdf0b3abb69536e9d33fcea8d0355926dc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/preview-reversehero.png",
        "sha256": "bb053b20bf3c4b47c71523dc91ecdd4535e55c0b62b7b67743a4f84fbe0a8317"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/preview-front.png",
        "sha256": "c6952d7c0412a8bcfd5ce9bd77d9311378bbae4694fb7f5c3c1841747a21769d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/preview-side.png",
        "sha256": "2f8b418263bad24be798d493f3e9a98cd77d91f17ec88092948690066d63fca4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/preview-rear.png",
        "sha256": "f6520318126d0cb5837d261e3e32eca9993686415af9cb2f84ffd9a4e892a054"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/preview-top.png",
        "sha256": "2886bd28748dad9353409ab1d62bdad539fce67b35b0b7ef6c3287f5c6aa93a3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/preview-clay.png",
        "sha256": "6bea041ecaa1be122f0a9fd262ec8acfc4b29e79b2802e7d15cc2e17caaea2e0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/preview-silhouette.png",
        "sha256": "1fcada56ef3d430ba87d08337cda14e76ac4bbcf816b93bb4594c9c918d73357"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-hero.png",
        "sha256": "f2a537abcca8cb3cae6aa96f3f2ad51af07530b30be2c7e607af703d71498837"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-reversehero.png",
        "sha256": "532cf279acc6d75d235e4b44f084a121d9fb02445ab06ca1917047e4825951f7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-front.png",
        "sha256": "ecdacecaeed299e2ef8408210101fe5c9776bba3ace63512937d5bfa79f1e1db"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-side.png",
        "sha256": "dd29d7fdfc8179f627b7b88211e104ff32eebb0c8171e6d93de8fa7f27bfeae5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-rear.png",
        "sha256": "51ce6698fc9277c9634999e60eb20a86ae683ebbb5e9e442236dd32970dff3e9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-top.png",
        "sha256": "9b07b7158afa3b62c2277f91b3bd7123b647f2c8107ef90c0694d3c8d17336bc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-bottom.png",
        "sha256": "56bd7069a4af127a9eff0d90cf1fafbffc88c68797b6806d5d6dacc50d23b4dc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-80px.png",
        "sha256": "712431e9907f63f5d778e36cea69a5fce0669fcaccc3606b20da14db56f06ad3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-160px.png",
        "sha256": "0df335cb9939a9d059da1fa8ef52e80cefcc4d02c3b33a7eb2103fe874b97b2b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/single-240px.png",
        "sha256": "b8def178a12a0f7fd777f0bf71e90dcb85a4cbe0d05bcbd0c9864b2b44a51932"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/scene-hero.png",
        "sha256": "87b31fd4fb84e72bf5b1574fcd46da710fa4572f583fa7b188f70c6beca0fb10"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/sea-cave/r001/attempt-03/sea-cave/runtime/scene-top.png",
        "sha256": "a1c59e65526a5d78fce100bd76019a7846867e90443eb52d11a004abd4349e21"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/sea-cave/candidate.json",
      "sha256": "fe27243d156ea9952f2e4c181072677e5b7c054e47551aaea5f41410920cd4c3"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/sea-cave-contract.json",
      "sha256": "abf80c7cb84347152d0226682f2665db9b08edc82c60e628abb44ff57ba30f96"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/sea-cave-result.json",
      "sha256": "0a1322b750e4dd023c37ee77ba08539d1bffa77349fa7dbb709552f8b5540a26"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/sea-cave-original-legacy.json",
      "sha256": "fd6c2ad63b1ed96167463310f8acf8efc64a570ec93c154d9af2739d45e39de8"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-31.json",
      "sha256": "62f03e3627c02dc22b53a96ecb987aeedfa2387e9ff560509b9bb7c938d37624"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/HANDOFF.json",
      "sha256": "5208b3287332849a0cd92b9a513ae8305c9fa3915d440b6e9f47405c34f6e89e"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/sea-cave.json",
      "sha256": "d2bd671a1679592b7ebc9c15cdb2d0cf1f621b1dbac2249a8c49f20e306b885b"
    },
    "dependencies": []
  },
  "cruziana-crawling-furrow": {
    "id": "cruziana-crawling-furrow",
    "batch": "31",
    "source_commit": "b94453827c90ed71df0087017a48701477944f35",
    "review_commit": "ba33ae2cbd93fc65e423f76ec252f6e66883ce67",
    "handoff_commit": "b94453827c90ed71df0087017a48701477944f35",
    "review": {
      "path": "qa/continuous-small-life-round11-20261018/batch-31/independent-review/results.json",
      "sha256": "07d5804934efd8e213905c3201148782fb5d7a172c235755f2cb370e269dd4d2"
    },
    "candidate": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/candidate.json",
      "sha256": "564792072468466a4267cc34823eb272e6e502b96a62b5f2f3f02e0ddc182776"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/metadata.json",
      "sha256": "3d4b0a52de3aa5e6ea2e39c61e2aa774682bea81bf7f260cac0625066fc9b55d"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/cruziana-crawling-furrow.glb",
      "sha256": "280346aa5b63ff3d14d755f47fd809b9eed1fb1b11a2437daf639dc12a4ea019",
      "bytes": 220080
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/cruziana-crawling-furrow.blend",
      "sha256": "925b63886927374d2b42e5aa4100d1ad12f622c9b7bff7e6e8ee971ee5819574",
      "bytes": 1075336
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/view-manifest.json",
      "sha256": "b0c1760c0d958327f69d716a2150a3a5f1289e96790b6aab69bdac113a4bff00"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single.json",
      "sha256": "f890abdb1466b6ef495a604bbcf1edd78fb5d254b5a7188b67fb3cb0513c7f5e"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/scene.json",
      "sha256": "49dc412b2c83b19dd1bf5551ae8a43d5616d7665dc95711dcf3fb421239a937a"
    },
    "source_export": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/source-export.json",
      "sha256": "088543a68f0a6215b82ce4db50d3e10a43fa6f7b930d5a61b293b88f18312419"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/gltf-validator.report.json",
      "sha256": "36ddb3c5ea2e1d86a265bdb30e15059cebc6b811d054fe6c3fbae1af94b64e24"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/candidate.json",
        "sha256": "564792072468466a4267cc34823eb272e6e502b96a62b5f2f3f02e0ddc182776"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/cruziana-crawling-furrow.glb",
        "sha256": "280346aa5b63ff3d14d755f47fd809b9eed1fb1b11a2437daf639dc12a4ea019"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/cruziana-crawling-furrow.blend",
        "sha256": "925b63886927374d2b42e5aa4100d1ad12f622c9b7bff7e6e8ee971ee5819574"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/generator.py",
        "sha256": "b97c82027b488d0125b7b3ac3fc06ffc6809ede51689a202ee1939e2ecccb8c1"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/config.json",
        "sha256": "201ede1500611874ebf687449d99526b9aafc4b6df72d0207dd1842d70d9f64a"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/cruziana-crawling-furrow/brief.json",
        "sha256": "68a9642c7d37f14626d1ad9a2cc89350e908a2a79d4694d0cd44df792b99c1c3"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/references.execution.json",
        "sha256": "97fcc0813df0a6cc985138c11d2c28ca39e8f8dfb90ae77efe81a5aa3ecf5040"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/cruziana-crawling-furrow/references.json",
        "sha256": "1f29a4085d591dc90451192b616c10565432af871ab87e1880eb1562fea8f964"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/cruziana-crawling-furrow/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/cruziana-crawling-furrow/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/viewer.html",
        "sha256": "5d54ed44faeadae12c3b0f254492f3179012d38a306263453e65c9c406d39d28"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/browser_qa.mjs",
        "sha256": "77e404da289f12b84dfef078fef1e00144422053f666419657e87eb535533cdf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/verify_item.py",
        "sha256": "39bf9985eee1c04287e04022de0d9000926522a7a9259eec9010bb66fb83cb99"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/cruziana-crawling-furrow/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/reference-access.json",
        "sha256": "ce3599cb436a72bcaa5f5ac8da5509f23b7f65ba5ca72c5591822ea76b641467"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/claim.json",
        "sha256": "cf92c533428f2cab61d83791182b51c876c58fd4fd1b36d467fb38fccf838fac"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/cruziana-crawling-furrow/inventory-record.json",
        "sha256": "a1c0a97610f8d196b721602cee99c8fd398691c512a2aa4646dc79d080b26dfd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/gltf-validator.report.json",
        "sha256": "36ddb3c5ea2e1d86a265bdb30e15059cebc6b811d054fe6c3fbae1af94b64e24"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/source-scene.json",
        "sha256": "037ebe87221402cc75f025d9f81c30815189b59ca4f7ec4b6a6f5eb32686fbe0"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/source-export.json",
        "sha256": "088543a68f0a6215b82ce4db50d3e10a43fa6f7b930d5a61b293b88f18312419"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/reproducibility.json",
        "sha256": "099c3f0d5ac0b80a6756031d9418fdfa390e320bebfbd18a27d291324457a731"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single.json",
        "sha256": "f890abdb1466b6ef495a604bbcf1edd78fb5d254b5a7188b67fb3cb0513c7f5e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/scene.json",
        "sha256": "49dc412b2c83b19dd1bf5551ae8a43d5616d7665dc95711dcf3fb421239a937a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/view-manifest.json",
        "sha256": "b0c1760c0d958327f69d716a2150a3a5f1289e96790b6aab69bdac113a4bff00"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/metadata.json",
        "sha256": "3d4b0a52de3aa5e6ea2e39c61e2aa774682bea81bf7f260cac0625066fc9b55d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/qa.json",
        "sha256": "dd01c0aa13f97f82e5f7e4df2df12a9e87ac405c29b9ee440a66fba07b15db66"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/source-contact-sheet.jpg",
        "sha256": "c799ac88ad8cd170e63203ac2b5133f9223bc776ba34cf860bcff26f4d8c5a2b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime-contact-sheet.jpg",
        "sha256": "2e801eb2490bd157a1539bad680853a609a711f1d77234984895c1027b7e2e8b"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/freeze.json",
        "sha256": "0d628d12ed019810271bc8004909ee2aa9153b91cc1c10ecd8157dd34b79114f"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/practical-integrity.json",
        "sha256": "9edb81dda056ebecc09a856209e490c249d4780e80af64672159da7676eb88b2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/profile-contract.json",
        "sha256": "704bab98d4c2b5069931ddb055d01544416a99a7aecfddab737d26061e59fe99"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/profile-gate.json",
        "sha256": "26fd55f2ff3ea3f9dff7687f0f1bb02986a65328bc5a1bbc8afdb0c63ac64dde"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-31/cruziana-crawling-furrow/r001/legacy-gate.json",
        "sha256": "8b27932813a12832e78ee5a3612fdcd4a454149779912060439e6852eea3aa92"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/preview-hero.png",
        "sha256": "cb33b34e49e1c93b9c01253cf7ffdc1c26ed886b4ec5d8b790bd8f7438a3eb15"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/preview-reversehero.png",
        "sha256": "75281e93a4b5146478860158e3cc7be777c244c6e17a173d29439740a4d2f7d9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/preview-front.png",
        "sha256": "04744350ccaa4922effea78523413b887c9afbab02ab3aa80dd2bbe95cad3a8c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/preview-side.png",
        "sha256": "93a7f5810afd3a4ba624c197ec3afaf4b3aa8e597f300eeae32bf2fe19de5aeb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/preview-rear.png",
        "sha256": "63b4fc5c459fa2b7272bb2cfeef6bd37882cabb34a296acd274950da461905a7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/preview-top.png",
        "sha256": "2c6d62619fd7776709173ff2a5c0dc659f03004643e9b5fbaca4f3a3a2524fb5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/preview-clay.png",
        "sha256": "5c897e2b0e21c6199f78b9511d620c635af49a63512ab8f4a0b624e2a95c2e7b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/preview-silhouette.png",
        "sha256": "ab779fb440387ceef031c57d960be8bdbdd9b7908a6f35329bae712ab64dc36c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-hero.png",
        "sha256": "6b21609089dde4b0628410a3ae40ecd3c446e643b4fa7855cd269841dffa9b9a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-reversehero.png",
        "sha256": "d8ca1e5d8b1dbf5ce8cbf81e6d3bbf36ba8a00f66e5a1844d2195bb5dd083262"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-front.png",
        "sha256": "b3fdcdf86bd90fd70ca39fcec4cb0002b71ed9b3d2ab1482c9d06389bbe8d560"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-side.png",
        "sha256": "c7bdfb107fabaf45d4f78996dc9de00f3f9196607e9f97a004f1da8d7b0a6b5f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-rear.png",
        "sha256": "4e92e48af2eee81cf423f9dc2ad97015d369e61a1a57d7753c105729117ac442"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-top.png",
        "sha256": "ba5974e248edd58bc984868a3192c528b17164614cd045af179b74dc9e08a5c1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-bottom.png",
        "sha256": "bcf641aef343898e22d0702dd74ebaa9c58392aa49cc8862544c5bbc1f6746dc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-80px.png",
        "sha256": "447be6ef71838add0d49db8ea040ec20d3da68091a1176f319dc7aab5dfcc8f5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-160px.png",
        "sha256": "4e90b8412f1593841c995901c6a24abb1c1bb5873c2a498d5e4f2657aa26ed23"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/single-240px.png",
        "sha256": "87181f9e7f06cc114f9f7a99bdfe835c3639d3a2b24a64eaa0c7cddf1f5224eb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/scene-hero.png",
        "sha256": "5b9332ccba6f014f4e8ffd3e20832be447e02abdbca71492a034e5fd80c8baa9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-31/cruziana-crawling-furrow/r001/attempt-01/cruziana-crawling-furrow/runtime/scene-top.png",
        "sha256": "5b33198f86ded98b426ca251b0c4f0ae2454f8d5b1d2353c9faea6eae061739c"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/cruziana-crawling-furrow/candidate.json",
      "sha256": "b4bd0dfcfb6f8a95fb87b96d95f458b63da2720510531369b6ab70f2d1443a4a"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/cruziana-crawling-furrow-contract.json",
      "sha256": "7c3ea0d1c05cc7fc744c186d055f03828d44376166377544f45093b936d8a3e5"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/cruziana-crawling-furrow-result.json",
      "sha256": "2172a40f8e962fe453cea526e035961889cc5e29b161836519bd77b9106a2d4a"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/cruziana-crawling-furrow-original-legacy.json",
      "sha256": "8b27932813a12832e78ee5a3612fdcd4a454149779912060439e6852eea3aa92"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-31.json",
      "sha256": "62f03e3627c02dc22b53a96ecb987aeedfa2387e9ff560509b9bb7c938d37624"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-31/HANDOFF.json",
      "sha256": "5208b3287332849a0cd92b9a513ae8305c9fa3915d440b6e9f47405c34f6e89e"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/cruziana-crawling-furrow.json",
      "sha256": "9ec513cc222faac6288483fbba36183c13559fe1fe4bf328f2b7d4306a40dfc4"
    },
    "dependencies": []
  },
  "ctenocystis": {
    "id": "ctenocystis",
    "batch": "32",
    "source_commit": "0a138d15e15579b061030675f8139985edb25daf",
    "review_commit": "bf753fe39eb630759ff6596488117fed8f9e1a20",
    "handoff_commit": "5d2cfac309a28b05a1f213d69f79938081c8bbdc",
    "review": {
      "path": "qa/independent/continuous-small-life-round11-20261018/batch-32/results.json",
      "sha256": "ca86d5fa960f9a052dff824dc7053ac2cad6ae5247443990610b7fc3b5bd1bfd"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/candidate.json",
      "sha256": "fd140ad82ee09efaf72553abd8c3d7ee43b7e55398c23d92c2acccc4a094de78"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/metadata.json",
      "sha256": "bd3391446780d39ebfeaa98c18faa8290b3cd3c610ba4eb28ba247cf7c1e87fe"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/ctenocystis.glb",
      "sha256": "5fa8da2d107ecd444ddbbab5f9801807b1c5a970b460713ffe2b12bed82e1ecc",
      "bytes": 53444
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/ctenocystis.blend",
      "sha256": "bd8fe25dc02c6130ca4f1a06103d088983df4485d4f7a218c713665db69b653d",
      "bytes": 568924
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/render-manifest.json",
      "sha256": "2eed5e9d92ba1b16ea8294114014ccdfdc72c2e20690d26faece854586b080f4"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/runtime-report.json",
      "sha256": "223cba66c870cadf24a52bb445ff194bda5d3c8f5f1c4384355e80111c1f9ac4"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/runtime-report.json",
      "sha256": "223cba66c870cadf24a52bb445ff194bda5d3c8f5f1c4384355e80111c1f9ac4"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/source-export.report.json",
      "sha256": "ee9feba102b98c620c85a17c30cf7ba65ff30b0bb154b05324f307a911bc9d95"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/gltf-validator.report.json",
      "sha256": "1abddca582b8338f3c286b2140e89f5f8601a6fe5b44fc5d8518a24efe899cff"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/candidate.json",
        "sha256": "fd140ad82ee09efaf72553abd8c3d7ee43b7e55398c23d92c2acccc4a094de78"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/ctenocystis.glb",
        "sha256": "5fa8da2d107ecd444ddbbab5f9801807b1c5a970b460713ffe2b12bed82e1ecc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/brief.json",
        "sha256": "76511d6d2029d5d1979b4ed9db2f69461b35f22a28c371c67725dffcf250a23d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/references-profile.json",
        "sha256": "db11fe4be7c5d3aa11a290891f723fd3135824882103e327621bd9f32fced02b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/ctenocystis.blend",
        "sha256": "bd8fe25dc02c6130ca4f1a06103d088983df4485d4f7a218c713665db69b653d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/build.py",
        "sha256": "14b1fe88153471b115c074368b85c8bbd1d7e1e2fbee4cdfbbb3438e8ae2d679"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/config.json",
        "sha256": "f66e9f0b319f73cb24de93fa66f55bb6f41dafecb1bcffb8c52651d0d2ae0a29"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/render-manifest.json",
        "sha256": "2eed5e9d92ba1b16ea8294114014ccdfdc72c2e20690d26faece854586b080f4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/metadata.json",
        "sha256": "bd3391446780d39ebfeaa98c18faa8290b3cd3c610ba4eb28ba247cf7c1e87fe"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/references.json",
        "sha256": "db11fe4be7c5d3aa11a290891f723fd3135824882103e327621bd9f32fced02b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/references-profile-mapping.json",
        "sha256": "5e0e04bb09b1b745cbee059587257532a1c37efaa20fd9e09d251a0dc06811df"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/reference-access.json",
        "sha256": "eb45588fa95c7aa3eed69a8b80959640a0af01e4eb1a8d1492e6016578689512"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/profile-contract.json",
        "sha256": "0d4cc9b6d4b953972100e2dccf067cbe72409aeae0a6307328d2b272d90cf979"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/profile-policy.json",
        "sha256": "78acefa33d3355fa75d872a9aff516beb2142043ff9ec1e6f7e34772f26e51b0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/evidence-manifest.json",
        "sha256": "5a450b7425a70181b6490b82c1aa464cc5d9685b77af20c654dddc6aa3fa0ced"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/source-export.report.json",
        "sha256": "ee9feba102b98c620c85a17c30cf7ba65ff30b0bb154b05324f307a911bc9d95"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/source-mesh-measurements.json",
        "sha256": "68ca7a69d4dc347e3c2044bee98a8c95ffd9b74e1c2544480df6d8cda1f6371a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/profile-checker.report.json",
        "sha256": "c1e4d3f96f7c9fcde476e3d4746165fed72f54b237fad3ce6249333e1436cd2b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/profile-approved-check.report.json",
        "sha256": "c1e4d3f96f7c9fcde476e3d4746165fed72f54b237fad3ce6249333e1436cd2b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/project-checker.report.json",
        "sha256": "e1b92afcf0a72244a93cb11956ad1468f06f5c4316bfb7c7e166025199e8571d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/checksums.sha256",
        "sha256": "2ada951848b676fa90648d331ccc4de9654e55815fdadbe1af50dc4f6118065a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/HANDOFF.md",
        "sha256": "94b0db18ca76371ae1021a2c1813a030849f393faca1119336a506e12aacb054"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/serial-execution.report.json",
        "sha256": "b6708dbab96e09b226b1f8a0740be3aa8976585382e0d943bca0d074b1315648"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/batch-32-QA-SCOPE.json",
        "sha256": "bc0ebd8c7869f9816240ea77a3ede7a9e5b6b5e74d624d33392adac50f65e08b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/qa.json",
        "sha256": "877cb2a6b50894e3b4f6976f4abdf3401308ba703e9133837a02db578494a08d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/dependency-hashes.json",
        "sha256": "0035f4a87502a82330129cf56baf716066e17e2520b63df093afc1c2b0ebd84f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/maker-self-check.json",
        "sha256": "ad588996e095185e37d934a168cd3fc25ed1a560ed060b43443625d6503bdb39"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/maker-visual-inspection.json",
        "sha256": "b3a38ac6f0af9abd31bb6c84f999e6ae8d169060d17c151fd001ff1d8c075ca5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/preview-hero.png",
        "sha256": "a1c0d207bd1035a691fb7731c47a25d8ed21bfc787009cf53bdc77e1b83a64d2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/qa-contact-sheet.png",
        "sha256": "1f039b48b5add5a662225d0601e7b4905b7530223a6fe178902b479d8e07cc57"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime-contact-sheet.png",
        "sha256": "3fe72f0b4ed1663f5e637e6f0f2a1c2a46710dd65aef994658f73aa009241f23"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/reproducibility-1.report.json",
        "sha256": "7ca2575777b01b9802aa875e25c2dce2062bf8655af8aef079bdb6f0934d51f0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/reproducibility-2.report.json",
        "sha256": "6e3e2241ce783313eca2643cc927a37f7fb398389cecf177d46bfc1ff36471ca"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/preview-hero.png",
        "sha256": "35cb15b5849727e610c28f83543172993419897a7bc2bef5bc3b4b6437af3454"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/preview-reversehero.png",
        "sha256": "7e7059b3bb2b29594e2d8b12fec4befa6fb7910b8c20de0cd59309d5be497e7c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/preview-front.png",
        "sha256": "2dbe495f5a14170cefeab7b91e332eab91ada7ecab259be10ecefe10004f4fb7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/preview-side.png",
        "sha256": "afd175c20b693aec9e50768cfe81aa3a30e849ce603fd75bdeedcee641f3169a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/preview-rear.png",
        "sha256": "1f0d759375e9657a7752e83c1948c183e10b7c50ba013ee626e9cc93c6c604d6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/preview-top.png",
        "sha256": "cc6e7b2f4b5301323af9f844372f44e03927dc43c8922f82a78f8e9c77c78e30"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/preview-clay.png",
        "sha256": "5ec075f8270985babb3a51b6b41536f53ca19eb290fbdc65d3f6e06b09c61939"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/preview-silhouette.png",
        "sha256": "5a2b8076b9a3aa1bb00bbb7cd75d995c64cd00173a969fe9d1b14a76e216ed73"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/runtime-report.json",
        "sha256": "223cba66c870cadf24a52bb445ff194bda5d3c8f5f1c4384355e80111c1f9ac4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/front.png",
        "sha256": "b9b91d29712f6a4ae2482d222ffc8d7d4ee8d701511b0e57ba86b028d3f26e25"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/hero.png",
        "sha256": "faa783f7a5784e986aeb5ec61820fb700983b791e3fdf1d3f97a3c20336476a4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/near.png",
        "sha256": "a1365a4e855b31e5024e2db77c90b3dcd897a4da526e8df15d7096c183a7edb6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/reversehero.png",
        "sha256": "7e2057b44e3ac981a57db6ab98d214bb4d737b3541d0765f308517aabf468c84"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/scene-9-copies.png",
        "sha256": "0a4febb1c58ccf020bbd965ebcd0455f44cb533e6bac82cfb3502fbf08ea9906"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/side.png",
        "sha256": "827691e6494ef16ebb35a40f37de6d65118a039b9f9b7752c150beea15b62eef"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime/top.png",
        "sha256": "82d0a5a972181c3e8355cec1ba3d10259cfbd4930deaae99ee53e45a63bd207b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/view-manifest.json",
        "sha256": "e8319991fe3402dac1858665aa3646ba10d6b3b99186ad31bfa82654ddda6346"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/views/transparent/preview-hero.png",
        "sha256": "a1c0d207bd1035a691fb7731c47a25d8ed21bfc787009cf53bdc77e1b83a64d2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/ctenocystis/r001/runs/build/ctenocystis/r001/semantic-rebuild-1/7966d83429fc46c8e2f747b3e3b5f800b6341ca2990a87f7d3a0f135de115022/20261018T234518-c715f08de3c644f6830af15b2afc71ca/request.json",
        "sha256": "497d694a6f78a8309fe8cdfca69d185f21ba1c23bb12ffdae47868cebdb66a5f"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/ctenocystis/r001/runs/build/ctenocystis/r001/semantic-rebuild-1/7966d83429fc46c8e2f747b3e3b5f800b6341ca2990a87f7d3a0f135de115022/20261018T234518-c715f08de3c644f6830af15b2afc71ca/result.json",
        "sha256": "2c0340c08b7f70a560d734fdfa00010370b0bb8703b74094d98296613b6c5df5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/ctenocystis/r001/runs/build/ctenocystis/r001/semantic-rebuild-2/10a1a2a9dab6932df1c5451aa722d24456c082c6197ed586b708854718c4173d/20261018T234520-8aab37b07d7341849eb196a45146da62/request.json",
        "sha256": "b9c06af4b66233661e1a4ec84fdf5ad59eded6cbe71c2d2d229d7d50e034e7fd"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/ctenocystis/r001/runs/build/ctenocystis/r001/semantic-rebuild-2/10a1a2a9dab6932df1c5451aa722d24456c082c6197ed586b708854718c4173d/20261018T234520-8aab37b07d7341849eb196a45146da62/result.json",
        "sha256": "4016cedc179988381f7a9ceb5538b5380cb9bb6080d28b8482fdec039d796051"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/build-config.json",
        "sha256": "7b854b3d1383c333ad94c2261e978f0fc1b0815bceb9593fe0475a0c7d95cdaf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/freeze.json",
        "sha256": "90b7da0884b3a0a7dc165256e10a011111c8874f5ea2aee906440a0aea919042"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/gltf-validator.report.json",
        "sha256": "1abddca582b8338f3c286b2140e89f5f8601a6fe5b44fc5d8518a24efe899cff"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/inventory-record.json",
        "sha256": "7d33b07a09e3f1d8c07b1ad8dede477ff77d191735913fb6eacd9ecd8bde8260"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/reference-policy.json",
        "sha256": "f148fd95e73529d76ba53008716e6e72fc32724181a29566e5c28f0e6801b93b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/ctenocystis/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/ctenocystis/candidate.json",
      "sha256": "04336aaf70d93db5d7e3a9c7247ef08e5e5491e1c03cd790ef4d3442b85bba04"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/ctenocystis-contract.json",
      "sha256": "b00eed54a04f7e346484425f82d203019c570c853e3b4641c286de7c53c4729d"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/ctenocystis-result.json",
      "sha256": "0a2dd8b3c43a19af2e73eadf30f2a4b71d1ebb37568450764c02e4cbe2d01458"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/ctenocystis-original-legacy.json",
      "sha256": "e1b92afcf0a72244a93cb11956ad1468f06f5c4316bfb7c7e166025199e8571d"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-32.json",
      "sha256": "97333c8c89a49c94bbe9358649f8e34a7f4460e12a37cd08cb5484af98e66edb"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-32/final-handoff.jsonl",
      "sha256": "045703462fe390bc43200a95dd2f9fc3fae1e4b080f475d9f4c8d0cfa84280f6"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/ctenocystis.json",
      "sha256": "afc7babf494155e086386452b6384aec5fb28f8ce5f27b3ae67e0a00af68facc"
    },
    "dependencies": []
  },
  "baculites": {
    "id": "baculites",
    "batch": "32",
    "source_commit": "cfad590fcd563b0451710b6c42e4c0e1bc6d541f",
    "review_commit": "bf753fe39eb630759ff6596488117fed8f9e1a20",
    "handoff_commit": "5d2cfac309a28b05a1f213d69f79938081c8bbdc",
    "review": {
      "path": "qa/independent/continuous-small-life-round11-20261018/batch-32/results.json",
      "sha256": "ca86d5fa960f9a052dff824dc7053ac2cad6ae5247443990610b7fc3b5bd1bfd"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/candidate.json",
      "sha256": "b36c6d00d43d3238acb74efedf3bd0837d4337539654eca6a84b98699ec39c07"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/metadata.json",
      "sha256": "6c9d12af79b714618149a6c89ba3167bac13de6073242b92a308d3f96d2f33e9"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/baculites.glb",
      "sha256": "89600216159c052b2c667ff55c31a18011f6ac6022738aa1ace5ed1c11742b1b",
      "bytes": 79952
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/baculites.blend",
      "sha256": "0d3cc4b64bf600e7e8c6a11eb8cc7faf6089c66b85ebe119ffd91dc3cab5f920",
      "bytes": 628372
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/render-manifest.json",
      "sha256": "ad68b4285d7f6c7747a31c05d5ecff8644ee42383a559f36d2b0b845004f7d15"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/runtime-report.json",
      "sha256": "3901be8ac45b7ef0abe664efc544d3c7d195723212b6db8ffc9d96fb5dc14573"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/runtime-report.json",
      "sha256": "3901be8ac45b7ef0abe664efc544d3c7d195723212b6db8ffc9d96fb5dc14573"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/source-export.report.json",
      "sha256": "c99f435b8f92a612a73eb06f50d5b4b25947560e4a7601ec4c61df4ea94d1168"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/gltf-validator.report.json",
      "sha256": "b85508e2386ec757d5405e18f0c8624c13bfa683e12b2c990ec2a3e6b8644629"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/candidate.json",
        "sha256": "b36c6d00d43d3238acb74efedf3bd0837d4337539654eca6a84b98699ec39c07"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/baculites.glb",
        "sha256": "89600216159c052b2c667ff55c31a18011f6ac6022738aa1ace5ed1c11742b1b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/brief.json",
        "sha256": "e997505fc41cae71f6125f69706f1cdf5b2f4b8fd250ffb83c8bfdd1e9ba501c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/references-profile.json",
        "sha256": "90e57f576483f89ffcf064ec5226de94d3e5429817bcc2ae03a7fafd11ca09b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/baculites.blend",
        "sha256": "0d3cc4b64bf600e7e8c6a11eb8cc7faf6089c66b85ebe119ffd91dc3cab5f920"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/build.py",
        "sha256": "14b1fe88153471b115c074368b85c8bbd1d7e1e2fbee4cdfbbb3438e8ae2d679"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/config.json",
        "sha256": "83f0713b07fead3a8cdb1a65c0d85f330f27c2e6ad5f783ec91ba7e164b55a2d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/render-manifest.json",
        "sha256": "ad68b4285d7f6c7747a31c05d5ecff8644ee42383a559f36d2b0b845004f7d15"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/metadata.json",
        "sha256": "6c9d12af79b714618149a6c89ba3167bac13de6073242b92a308d3f96d2f33e9"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/references.json",
        "sha256": "90e57f576483f89ffcf064ec5226de94d3e5429817bcc2ae03a7fafd11ca09b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/references-profile-mapping.json",
        "sha256": "6fa9741c11c5c4224b2414dc837794597cc4137eababefafd9294bd1f1e1daa3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/reference-access.json",
        "sha256": "a0b12f23277af9783fcbb86cb5a44a205a0415a9b79dd1060c5c2298f0aed94e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/profile-contract.json",
        "sha256": "7f9e144fd07fb8f93138cb57a73e604305c2a53b19d7cd2a0238046dff7b2a72"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/profile-policy.json",
        "sha256": "78acefa33d3355fa75d872a9aff516beb2142043ff9ec1e6f7e34772f26e51b0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/evidence-manifest.json",
        "sha256": "66bfb8c4b066181e02348f767b45483eca564d3328cad45d547ef0dd5b8b14d1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/source-export.report.json",
        "sha256": "c99f435b8f92a612a73eb06f50d5b4b25947560e4a7601ec4c61df4ea94d1168"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/source-mesh-measurements.json",
        "sha256": "eab0cbff05746a824f9d007f07e4565a37654891aa0ae507445cfc5f5a335468"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/profile-checker.report.json",
        "sha256": "2af5e40ef81821213b3a60e1958053dc87c1d87aa7047db82bdab14c72e69828"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/profile-approved-check.report.json",
        "sha256": "2af5e40ef81821213b3a60e1958053dc87c1d87aa7047db82bdab14c72e69828"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/project-checker.report.json",
        "sha256": "15b8df929c2b2fdf076d0262817cf61ac3312f792bc4e04f35810f70cab2fc13"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/checksums.sha256",
        "sha256": "90881dc83dbdf4bfd1b8167363b0b0bca5ae7d1ff6804017520a271da7a04a9c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/HANDOFF.md",
        "sha256": "7dfa75b9e48bc86522997ca39b5bf06c37d20145d3323023fef3250a3d081748"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/serial-execution.report.json",
        "sha256": "53377bd3eea0e0532c0d50416ea76c00a9e0043601148fa10779131b984e8f8f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/batch-32-QA-SCOPE.json",
        "sha256": "bc0ebd8c7869f9816240ea77a3ede7a9e5b6b5e74d624d33392adac50f65e08b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/qa.json",
        "sha256": "75d7f84f1cd47a6f161536767c673770dade4ce64018b8d2501175e5f9181f17"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/dependency-hashes.json",
        "sha256": "7926c77d22fa2d1abc22be539c9f81b922f25d90b10a56791f4df9cc32c48424"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/maker-self-check.json",
        "sha256": "03bed7582f62d4d8bc305b06e8844a9090a87f1db91d7425b4e6530540f31d0d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/maker-visual-inspection.json",
        "sha256": "7afa21413fc3c83dbc48ad2b4a7a3dd21112bae8ec326b5a47d2d6d5f151a2c0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/preview-hero.png",
        "sha256": "89e0aafdc7ca64c15d49011c8e093e734ff436a50b694d7ee22d157ae7809339"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/qa-contact-sheet.png",
        "sha256": "cecf82f074f6a11c8533336ed44ec6112b5535bf2421b517c40e076ee32e6aab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime-contact-sheet.png",
        "sha256": "c7416f2c39b576ad6cf745d49e3d64232b09c368df76725e4ab580d8f704bb49"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/reproducibility-1.report.json",
        "sha256": "f8dc1ac3764e151e0735ba48c35c28d5327615e7b72722af20fff6fd4be6b527"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/reproducibility-2.report.json",
        "sha256": "f68131d47ee3ec30c2d0a869474409886b876a652973e55d1c3af4c190498322"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/preview-hero.png",
        "sha256": "098bee4244d6f9cedfb7fde2dab59cb4a37f3a96b0842ef3588e5d2a77e28a06"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/preview-reversehero.png",
        "sha256": "06249195c34688de727bdac85261a2d75f39b5a09c08714c830255185d9a97d2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/preview-front.png",
        "sha256": "c568c1dcb8f09526511b47fba250bb42b9cd00f5a5f40bbfacfcfd77c22d9cac"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/preview-side.png",
        "sha256": "2c933b2024a6710a083bf1dce70fa53a40d0662b74e432b7e47c19ee2986706e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/preview-rear.png",
        "sha256": "aa6d251b506b8e26a95feb5e98e9b5c36969f6601433b90502d03375fa2c570b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/preview-top.png",
        "sha256": "b68ef0d4e69565d7b5a7d5be4a70d2c8f321be703276fcb333bd6b99c8763991"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/preview-clay.png",
        "sha256": "7fa63791370e2cacd2af7288a07539f50633a2e9469b54d5a80c5c5f23a1f4d2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/preview-silhouette.png",
        "sha256": "45a607cb38847e85a8c084c32a213f6301f0f04733912e205ae48e1c931426e3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/runtime-report.json",
        "sha256": "3901be8ac45b7ef0abe664efc544d3c7d195723212b6db8ffc9d96fb5dc14573"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/front.png",
        "sha256": "d28da57e4d7ab1e83d41cced779c32113363bf8b5c1d8631a22a760ba51eeaaa"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/hero.png",
        "sha256": "49f954239483de486c1acd8faedb58c00a36b6e2dafdc28365980910715f000a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/near.png",
        "sha256": "3c7df14230243aff1d1c66c29e61b3db20dad0afa8a29d8d1033f5860e9854de"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/reversehero.png",
        "sha256": "f9e457ded038f8ba01c3007b003e3e4e5842772161c2495ea607e8dfa01c7bda"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/scene-9-copies.png",
        "sha256": "1e3b6e7b200ab08e520ec5612044279450f4ddc626d3d724ec83616c4da42581"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/side.png",
        "sha256": "95c64612f44a551310e7bb3862e118befbc43328109f19e4efb7fbf5c887fc60"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime/top.png",
        "sha256": "6de7570818ccfbd7223e4e8fe32c8f2e03c62b6e7b0b5b94af3b9bb0b2ab1ff9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/view-manifest.json",
        "sha256": "077f75b47b81dbac3d400315485262934ae2074562f62b54793211218392ff5c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/views/transparent/preview-hero.png",
        "sha256": "89e0aafdc7ca64c15d49011c8e093e734ff436a50b694d7ee22d157ae7809339"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/baculites/r001/runs/build/baculites/r001/semantic-rebuild-1/a7b1087d04959550d28344ba5b2c33bb2b2872281029c46b6aa67590352c9cfd/20261018T234801-cf1861429723419cb70afd3f32d192c2/request.json",
        "sha256": "9eb5f9640d7872c193dc1a3e27c15d2ac0f86e5c1dfc6f455dccafb80d89c882"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/baculites/r001/runs/build/baculites/r001/semantic-rebuild-1/a7b1087d04959550d28344ba5b2c33bb2b2872281029c46b6aa67590352c9cfd/20261018T234801-cf1861429723419cb70afd3f32d192c2/result.json",
        "sha256": "cfb44dc3dae009fe06b956bf589c5c2f04f282c5a2715142e076a8695e49eeb1"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/baculites/r001/runs/build/baculites/r001/semantic-rebuild-2/d0fab391901af965f795a0496ec5744639106d6f2aa8835f8997c498610df9c2/20261018T234802-07f404035ecb44a28669d7dcbd0f4d6a/request.json",
        "sha256": "d039df2fccb44c90f80b61bf755f1f1c68a624eb007f9a651c48ca0737acdb52"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/baculites/r001/runs/build/baculites/r001/semantic-rebuild-2/d0fab391901af965f795a0496ec5744639106d6f2aa8835f8997c498610df9c2/20261018T234802-07f404035ecb44a28669d7dcbd0f4d6a/result.json",
        "sha256": "cbac203714d997f3e7fc6b3b4d044af6b69aaf4b5b4d42e6c99c1d6a1d67a167"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/build-config.json",
        "sha256": "9d60ef0ad3ac307618cf91e676b1bcd6c64ed7f40872245b1a7ca4ef02ec715c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/freeze.json",
        "sha256": "8012517d151bc9395f2b05232cfeadeb4ae8921d610902af43a8f84753d5f830"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/gltf-validator.report.json",
        "sha256": "b85508e2386ec757d5405e18f0c8624c13bfa683e12b2c990ec2a3e6b8644629"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/inventory-record.json",
        "sha256": "377b42289f9b40f971c96a33c668ef3dc495e3f1e4eba9147e5ac354f4396b15"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/reference-policy.json",
        "sha256": "f148fd95e73529d76ba53008716e6e72fc32724181a29566e5c28f0e6801b93b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/baculites/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/baculites/candidate.json",
      "sha256": "c72c7c6704430908e7fcf1683fa9c052792ef1b239cafdf65eace445462a4acb"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/baculites-contract.json",
      "sha256": "df27b085ef4ef8577b9c8debce37ae0874d0f7ed5d80188b7d1557d114934817"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/baculites-result.json",
      "sha256": "a7eb531c838bf1c3929fdc5b503faffa6ced64fefe49caa8288e300b22efd661"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/baculites-original-legacy.json",
      "sha256": "15b8df929c2b2fdf076d0262817cf61ac3312f792bc4e04f35810f70cab2fc13"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-32.json",
      "sha256": "97333c8c89a49c94bbe9358649f8e34a7f4460e12a37cd08cb5484af98e66edb"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-32/final-handoff.jsonl",
      "sha256": "045703462fe390bc43200a95dd2f9fc3fae1e4b080f475d9f4c8d0cfa84280f6"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/baculites.json",
      "sha256": "4ecf6db18ba01edf1b33f3ef77197e522fc6dc2346f4448e160c774316701c7c"
    },
    "dependencies": []
  },
  "estuary-basin": {
    "id": "estuary-basin",
    "batch": "32",
    "source_commit": "ebdd87bff416b3445b388b70e157a689fa823594",
    "review_commit": "bf753fe39eb630759ff6596488117fed8f9e1a20",
    "handoff_commit": "5d2cfac309a28b05a1f213d69f79938081c8bbdc",
    "review": {
      "path": "qa/independent/continuous-small-life-round11-20261018/batch-32/results.json",
      "sha256": "ca86d5fa960f9a052dff824dc7053ac2cad6ae5247443990610b7fc3b5bd1bfd"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/candidate.json",
      "sha256": "433c7d2abde55be754837dd2bb46d4280ef4e89b218be33cded32a2694fa8691"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/metadata.json",
      "sha256": "e500a62a63deefcf1baeb2ba7e121756a10e5570b2f63bba4d25df911a78383a"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/estuary-basin.glb",
      "sha256": "22d8cbe94157394901e294c39f9d9a0476dd2a89282266696eefc3b6b9681d56",
      "bytes": 320400
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/estuary-basin.blend",
      "sha256": "b7f0e4d0dbda80d3c707137066b5096bbd8cd9d232e0bb1b11ed5628e5bae9a8",
      "bytes": 653616
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/render-manifest.json",
      "sha256": "47fb55d6479a44801d0418b16f246fc5021384f53f5558b3b62b2e621e851fa5"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/runtime-report.json",
      "sha256": "b6e8a1a2f99dcddf2f40b163de20223bddf3ee6ac7ec73ad8a6cb423917e9dee"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/runtime-report.json",
      "sha256": "b6e8a1a2f99dcddf2f40b163de20223bddf3ee6ac7ec73ad8a6cb423917e9dee"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/source-export.report.json",
      "sha256": "2df66a7237aefe591c24f03295b6a2588d3868b57d8a2736aade4b0e346af8b0"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/gltf-validator.report.json",
      "sha256": "d34ff689f75c30b2e4a1bd52a622cf2da954b62938624978dbedf73bba71cbfd"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/candidate.json",
        "sha256": "433c7d2abde55be754837dd2bb46d4280ef4e89b218be33cded32a2694fa8691"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/estuary-basin.glb",
        "sha256": "22d8cbe94157394901e294c39f9d9a0476dd2a89282266696eefc3b6b9681d56"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/brief.json",
        "sha256": "0acace769b747ebd3a4ebb9b9c82cd154b9455c6c3f5c20b6e3892a5d2646f7a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/references-profile.json",
        "sha256": "67634ec5d1fd922ec0e66f84e1cef8a224ce8a9fbe23beda8554273a59b42439"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/estuary-basin.blend",
        "sha256": "b7f0e4d0dbda80d3c707137066b5096bbd8cd9d232e0bb1b11ed5628e5bae9a8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/build.py",
        "sha256": "a5cbe78f5e0e780c0645d35d526627219ae53bee64614136bc687e60055210de"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/config.json",
        "sha256": "655c3e6463465d04bfd3efc98d0ea82de152f023de08dbbcbdad381d9148a1f9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/render-manifest.json",
        "sha256": "47fb55d6479a44801d0418b16f246fc5021384f53f5558b3b62b2e621e851fa5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/metadata.json",
        "sha256": "e500a62a63deefcf1baeb2ba7e121756a10e5570b2f63bba4d25df911a78383a"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/references.json",
        "sha256": "67634ec5d1fd922ec0e66f84e1cef8a224ce8a9fbe23beda8554273a59b42439"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/references-profile-mapping.json",
        "sha256": "bfa1222bd6574e165cb5c5d50d8e1b293d537a105cbbbd1c7360d18fb8de8e56"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/reference-access.json",
        "sha256": "27aa50b1aa89b6649576f3630942875b7c6f758af937a3e4af763fa72fe0340f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/profile-contract.json",
        "sha256": "cfa9e82632ad212fc6a27803ce726f2f0e0b0d1aed711a1fd235e401b09a30e7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/profile-policy.json",
        "sha256": "78acefa33d3355fa75d872a9aff516beb2142043ff9ec1e6f7e34772f26e51b0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/evidence-manifest.json",
        "sha256": "6e7daee373701ec461540313c4099cb32ad1f4418b9ca77baf1bc0f74369faff"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/source-export.report.json",
        "sha256": "2df66a7237aefe591c24f03295b6a2588d3868b57d8a2736aade4b0e346af8b0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/source-mesh-measurements.json",
        "sha256": "42110a74b3d05a51ca5e0acd52258e64c71af18f53d031c46d14cac13789a993"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/profile-checker.report.json",
        "sha256": "7ab7908ed1eecc28ac5c168316bd6b38fa91a1d79459376205188f345bac8b49"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/profile-approved-check.report.json",
        "sha256": "7ab7908ed1eecc28ac5c168316bd6b38fa91a1d79459376205188f345bac8b49"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/project-checker.report.json",
        "sha256": "37991c0616229f95b00fec0cc4fec147559d8355d161713e22f986b913a48987"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/checksums.sha256",
        "sha256": "7e2faa10a6e0a692c5e224e47ecd10238dcd583d778e26a82084f44c33cfb938"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/HANDOFF.md",
        "sha256": "6cc1b17522cda9a2aef123633ac7033b65c0b6c9787f3552f70a1c6055056b94"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/serial-execution.report.json",
        "sha256": "b0f9164534659c5ac83828b8097c57d284057cffa5f14c2c166154051261795a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/batch-32-QA-SCOPE.json",
        "sha256": "bc0ebd8c7869f9816240ea77a3ede7a9e5b6b5e74d624d33392adac50f65e08b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/qa.json",
        "sha256": "bfdcdd4438058fb817cdd5b16172363d2db6c2e668b5efeded544b47b2c64e81"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/dependency-hashes.json",
        "sha256": "dfa4a15c08ae4372074712696a8350afd0153fa60d8e471d77c5da0d2240a65b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/maker-self-check.json",
        "sha256": "a040325ce0a96a46b380c7608baef8da3e02430dfa637f62de4e1321a8f3d935"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/maker-visual-inspection.json",
        "sha256": "23fc1831de1447c5810b382cf0ff2bf9be163a6d0b1b1ecb023e6a47d13c8e9d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/preview-hero.png",
        "sha256": "f3d325721cfd3732df5e004fc31625fc65df3e70b5280cf0cfd470949ecee858"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/qa-contact-sheet.png",
        "sha256": "f4a3e4aba6f8c06ea0676daca533e135a9e04cc4db12371adfffa6f68af46527"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime-contact-sheet.png",
        "sha256": "f5921151aae6c6e4ec826fea2a83a3573f6399cd214bff827ee406c979c80498"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/reproducibility-1.report.json",
        "sha256": "8f97f1986231f5ac9802fa04fafd07f545c15e6a50dbf0423904bfe3dc1dd732"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/reproducibility-2.report.json",
        "sha256": "5ddbccfd91223d8b237462d573a288c172a73e9f8ccea795704353c12037f01b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/preview-hero.png",
        "sha256": "d3cbe77d0cf2623f9069da9533afed50ca3b598af79e96ab55b92c03c8193f54"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/preview-reversehero.png",
        "sha256": "6cbd93cbe8b429c624bedc92db4cde8bfbac94b1582fd5925c220841a6c4b222"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/preview-front.png",
        "sha256": "8ea767dc320afa9f95f52b247815c747a4479377798559bb5892d5ec850a7b85"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/preview-side.png",
        "sha256": "7892e6757e2a07a1991da744ac81da938d68665b001b9c5632361e7db90bfe88"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/preview-rear.png",
        "sha256": "95671a223947e24724930b292deef917d07d42c7319c583fd8089e699d11c96e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/preview-top.png",
        "sha256": "f7d6fb70f32eeb650ee7a37700d0fc935315342c3557775b237d8bf1ae63ea61"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/preview-clay.png",
        "sha256": "26fba419efdfe0e292d84416eb2e5fbf4efc5d3644428dedf8914946229988f2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/preview-silhouette.png",
        "sha256": "2c074e41a97de019bddf98f9949fbc0d987e2e66170b409b48297cc1b0f86ef0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/runtime-report.json",
        "sha256": "b6e8a1a2f99dcddf2f40b163de20223bddf3ee6ac7ec73ad8a6cb423917e9dee"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/front.png",
        "sha256": "dd26ae53484e87c795e239758648b10e6c30a8a00074a52b087058ac226edad5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/hero.png",
        "sha256": "d8e772b62ce0c57e14f502b3fcc120e60af532c7f25474207f9ab4e08d52bb99"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/near.png",
        "sha256": "5bca9c516892e2cb74644a613060c4941c5d0fefbaf70062f39087c5bb5e8cef"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/reversehero.png",
        "sha256": "3e0d006e286b57aa287bebe60e6da2a7922608c7ba1314d73a590c3ea6f2defe"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/scene-9-copies.png",
        "sha256": "4ccbbbc96a24175fe06d0529e8e519124f76f7b0fbd8118f426a173fad6a30d8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/side.png",
        "sha256": "0ad390382db8cd28df03ac53874f16768f6c7dbe5504f29251701806d63b8282"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime/top.png",
        "sha256": "0ffa61b7143a75ddadb4f84497e0cf7ce62015cbc01be2843ad32ee8d9acc9b5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/view-manifest.json",
        "sha256": "ab6d00750f85e6ea6c0a333a296d9ea010e0cdde484bf79871402edda9b03a59"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/views/transparent/preview-hero.png",
        "sha256": "f3d325721cfd3732df5e004fc31625fc65df3e70b5280cf0cfd470949ecee858"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/estuary-basin/r001/runs/build/estuary-basin/r001/semantic-rebuild-1/36e5fa607c9dd3a05a33a62d76b352927674ec516c06b1397d8c1d9b709562b6/20261018T235233-4035aa83442b425c9409ff4ff466db4f/request.json",
        "sha256": "9a6902d682e8c66983aec69d481d57da3332a0273c468218849372d059f2068e"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/estuary-basin/r001/runs/build/estuary-basin/r001/semantic-rebuild-1/36e5fa607c9dd3a05a33a62d76b352927674ec516c06b1397d8c1d9b709562b6/20261018T235233-4035aa83442b425c9409ff4ff466db4f/result.json",
        "sha256": "2454d47225bf5aa92ac4047f9bbf09706444d72155e6254a02648acd77bc185a"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/estuary-basin/r001/runs/build/estuary-basin/r001/semantic-rebuild-2/a04ba7f93c3732714cbd2f9bd80119df62d9d7b9230a7d409db2c83a99ac7850/20261018T235235-2dad230647654be7a942f5bf5a91c3d3/request.json",
        "sha256": "953590edd35f33dc8d67c9f7bbda3df8bc6aa60492688a4a1d9c71402dbf5f08"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/estuary-basin/r001/runs/build/estuary-basin/r001/semantic-rebuild-2/a04ba7f93c3732714cbd2f9bd80119df62d9d7b9230a7d409db2c83a99ac7850/20261018T235235-2dad230647654be7a942f5bf5a91c3d3/result.json",
        "sha256": "35e8d4fe35c5c7fccf3d504b80d20d06236bd2b6e083b343dd3d5e14bc2eb416"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/build-config.json",
        "sha256": "c58c1b2591c5e37a84e61b6624e5a4c8cfd1063b867fc5e0a797bee9c7352124"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/freeze.json",
        "sha256": "acada804acfb69c4755734fc176f01ff8abe701fa6681d7d6f80aac4814bf4e3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/gltf-validator.report.json",
        "sha256": "d34ff689f75c30b2e4a1bd52a622cf2da954b62938624978dbedf73bba71cbfd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/inventory-record.json",
        "sha256": "4d9a80d7e9fadc9cab7bfc85496b043b83315c0ebffdde176e4fbb081d4dfabe"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/reference-policy.json",
        "sha256": "f148fd95e73529d76ba53008716e6e72fc32724181a29566e5c28f0e6801b93b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/estuary-basin/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/estuary-basin/candidate.json",
      "sha256": "51489a9409cc88e7dcbc310304dad6f936c4fb81cecfe66756c27335684aa4cc"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/estuary-basin-contract.json",
      "sha256": "55035e81aa582cc035ad31d71ae86ea5bfd33183224ef9110a53ef5f6118c088"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/estuary-basin-result.json",
      "sha256": "60bf7a9a91a9d7061375f8a70145fe24bf296251c54a3a583d9222587de7f681"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/estuary-basin-original-legacy.json",
      "sha256": "37991c0616229f95b00fec0cc4fec147559d8355d161713e22f986b913a48987"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-32.json",
      "sha256": "97333c8c89a49c94bbe9358649f8e34a7f4460e12a37cd08cb5484af98e66edb"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-32/final-handoff.jsonl",
      "sha256": "045703462fe390bc43200a95dd2f9fc3fae1e4b080f475d9f4c8d0cfa84280f6"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/estuary-basin.json",
      "sha256": "33accfaf51ce2846dc9ff4aef16e44c3939a8834ea3e1b31286887eea33aca17"
    },
    "dependencies": []
  },
  "cross-bedded-sandstone": {
    "id": "cross-bedded-sandstone",
    "batch": "32",
    "source_commit": "e151470dae73839c1d27934b3915bb2da8055623",
    "review_commit": "bf753fe39eb630759ff6596488117fed8f9e1a20",
    "handoff_commit": "5d2cfac309a28b05a1f213d69f79938081c8bbdc",
    "review": {
      "path": "qa/independent/continuous-small-life-round11-20261018/batch-32/results.json",
      "sha256": "ca86d5fa960f9a052dff824dc7053ac2cad6ae5247443990610b7fc3b5bd1bfd"
    },
    "candidate": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/candidate.json",
      "sha256": "4f456c4a9934623b0fcdc28f314317661ac65cdd7d97e4f7ec84f22f92ddc887"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/metadata.json",
      "sha256": "6d7a9af5e25f0111b5a4f289c1731e030cfcb7fcae45d180a9a501ac74e3c989"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/cross-bedded-sandstone.glb",
      "sha256": "1a93b06b2a9a3457f0f11bff876328dc50b5d8c2f3a7a730fe411ebc200b3ac1",
      "bytes": 34128
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/cross-bedded-sandstone.blend",
      "sha256": "03d2271d446ec84c59a20bffcdde931f35d71c2626975aa1a1aba56f642fc0b3",
      "bytes": 477148
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/render-manifest.json",
      "sha256": "dc64e7ac4c5619c9ee0493b8d515749cb7643470b9c1b8eb7026d74a7bf50885"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/runtime-report.json",
      "sha256": "6bde1e3ac767dae7776000824a6a451a6036390678611d382f0050d7b488300c"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/runtime-report.json",
      "sha256": "6bde1e3ac767dae7776000824a6a451a6036390678611d382f0050d7b488300c"
    },
    "source_export": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/source-export.report.json",
      "sha256": "7104185ac3ccf3dadcc2e5477a3e79fd22f9ef7ac805e96288441f915c7a9de2"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/gltf-validator.report.json",
      "sha256": "293057e0acc368a61ff5be8ff6c30bf2266bdbe4c9c381672355e487fadff131"
    },
    "evidence": [
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/candidate.json",
        "sha256": "4f456c4a9934623b0fcdc28f314317661ac65cdd7d97e4f7ec84f22f92ddc887"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/cross-bedded-sandstone.glb",
        "sha256": "1a93b06b2a9a3457f0f11bff876328dc50b5d8c2f3a7a730fe411ebc200b3ac1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/brief.json",
        "sha256": "c67560c07e04b52bc03bc3b0ed678fc25ad519130a11666b898936492e3a6c26"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/references-profile.json",
        "sha256": "0934860fc31ad757a6e19ef190d1df2375ed70c18f96c5624938cc795d338be0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/cross-bedded-sandstone.blend",
        "sha256": "03d2271d446ec84c59a20bffcdde931f35d71c2626975aa1a1aba56f642fc0b3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/build.py",
        "sha256": "14b1fe88153471b115c074368b85c8bbd1d7e1e2fbee4cdfbbb3438e8ae2d679"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/config.json",
        "sha256": "3be45d30a3770a710b1764a538126fbda09ac2f0db96e6ba9033037747f1064f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/render-manifest.json",
        "sha256": "dc64e7ac4c5619c9ee0493b8d515749cb7643470b9c1b8eb7026d74a7bf50885"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/metadata.json",
        "sha256": "6d7a9af5e25f0111b5a4f289c1731e030cfcb7fcae45d180a9a501ac74e3c989"
      },
      {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/references.json",
        "sha256": "0934860fc31ad757a6e19ef190d1df2375ed70c18f96c5624938cc795d338be0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/references-profile-mapping.json",
        "sha256": "cdee1d010867b87fdabe6d90f38303886f89d72bf67622dfbc9f63955e9cc67b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/reference-access.json",
        "sha256": "96fc6c4695c8df37b2a9773544eaf288a91fe479fe9b0c5cc80b7b55d8b3381c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/profile-contract.json",
        "sha256": "ac94446d19cb2717d25a07ccd01068809f8bace297ffe1021804d85d7d20c655"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/profile-policy.json",
        "sha256": "78acefa33d3355fa75d872a9aff516beb2142043ff9ec1e6f7e34772f26e51b0"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/evidence-manifest.json",
        "sha256": "820db9a13d1ba16cb02613fbbe2184d8bb9567092374e9cbbe9dadcd7bc2d3e9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/source-export.report.json",
        "sha256": "7104185ac3ccf3dadcc2e5477a3e79fd22f9ef7ac805e96288441f915c7a9de2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/source-mesh-measurements.json",
        "sha256": "2e33c0d082bed7f1072684f08fee865d61fe88db58ac4623cbfe220599de4ef3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/profile-checker.report.json",
        "sha256": "17dc92875f221dc5f777a04b8ffcc4d9e452e00c5e6915303e716846a46cef40"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/profile-approved-check.report.json",
        "sha256": "17dc92875f221dc5f777a04b8ffcc4d9e452e00c5e6915303e716846a46cef40"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/project-checker.report.json",
        "sha256": "41dd6ca9621d794a1cd16d80a8eb0b28a8c19536e8aaf617ae1757201fecd06e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/checksums.sha256",
        "sha256": "ae984ca90ffa0237fffaba232d92e0784a498041c5fc47f5dd9e71610043119a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/HANDOFF.md",
        "sha256": "c81818a81d4c4b6b4f26e86f387d859e3de2ccab8fe2a48e556aae861380f23d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/serial-execution.report.json",
        "sha256": "00c3bc94d3d6cd1853d149eb7fc73fb431d4846fed857c2933fe4fd488fc181a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/batch-32-QA-SCOPE.json",
        "sha256": "bc0ebd8c7869f9816240ea77a3ede7a9e5b6b5e74d624d33392adac50f65e08b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/qa.json",
        "sha256": "24d6fdb7ce8290979003a958dc6c8b1bfe274dc15c809ab8cadd7fcf2d06a177"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/dependency-hashes.json",
        "sha256": "a4987ce3cb66c244ff51b52aef23ed400359019a69357e559958f750ae30eef6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/maker-self-check.json",
        "sha256": "c71ee5ff8063cb83a304856c7acd001e956525c4feaa20e76af38e3b2e1c6885"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/maker-visual-inspection.json",
        "sha256": "e8f2a80ffe6f735f1d352160cb289bfd5ca02f3a2564a5fb4fc9e5f7ea20388e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/preview-hero.png",
        "sha256": "95679fbf3e95376d6a11e9504887cefef5ee7e49e1c1b971c0cb0f639d99afaf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/qa-contact-sheet.png",
        "sha256": "82342db8279713a3d27e9d502abcf81f68ea2f5053b22fb04ae62c34f72a61dd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime-contact-sheet.png",
        "sha256": "89f19477dd6bd0ab61362692c2d80d843891c7037b49e055a033153ba966eb40"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/reproducibility-1.report.json",
        "sha256": "95c9edb6295ba2c16215ced2c0071020e738ffef82703daeeb555e919550a0a1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/reproducibility-2.report.json",
        "sha256": "2dc14dc4e0111513df3f5ca646307c32b75f694cb60d97e6de8c9812bae505f1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/render-config.json",
        "sha256": "38cfc6c2773e82b8ae356bf4c7812ce1f2b01734dc248cc98135e77703bc60ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/preview-hero.png",
        "sha256": "ff48b7dc1bf51a4cb2f88444c78bb79ce26ca25e746eaac180b4a907a72b9428"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/preview-reversehero.png",
        "sha256": "6cdba6afec747f7054c173662fdaaf074e81c2198745f594e716c9ce314407de"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/preview-front.png",
        "sha256": "d484049125f86247ed317f04d2c42ed8f0a4401979dc4ab34b5511e1ab1d302b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/preview-side.png",
        "sha256": "d1d3771132ba2db315cc1f941cbe11d79bdbf9fa574bea8fd8da431fbfc1cc68"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/preview-rear.png",
        "sha256": "d69f3c2b56ccb450cb4ca803973d9bc2453c04b6079b9c5a900c16d8787a811e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/preview-top.png",
        "sha256": "465cf8fa1a41d93f92c6930192ae1b0db13c342886185bb47c556ff5ed26e592"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/preview-clay.png",
        "sha256": "5837cd74254b8385801fdf2ed8d6150a616f53d4dc6bd60941b48adbfee38296"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/preview-silhouette.png",
        "sha256": "9b79fe507263144f449060ae3b74dce01c0a39632d05114897c3853aa42b4785"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/runtime-report.json",
        "sha256": "6bde1e3ac767dae7776000824a6a451a6036390678611d382f0050d7b488300c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/front.png",
        "sha256": "7aa689baa825a5f70cd3648b279810b450dc84e40189a2bffd54063d45f6a672"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/hero.png",
        "sha256": "173b0162b2b1ac45ebe94df4981348ad61d70dc11ea3d5688286f5983c76856a"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/near.png",
        "sha256": "5dadae51bcab889d906396c12c84585148147cc31ab9704336ed8ff99e15bebb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/reversehero.png",
        "sha256": "0337edf6e1f4bcfb28c21ddb1d1e2f24c95c9bd851a16cbeeb9d8336da9e4d16"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/scene-9-copies.png",
        "sha256": "b9f34fefbde796ea87fffc6e8f4ef052bd52d87396aebf2ced40d5c659746680"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/side.png",
        "sha256": "7a1912ddd5eaa8a3c49fc5dc6a1463fefb879c6e54aad002723e228e59167644"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime/top.png",
        "sha256": "73ac35b4b84ccdc69616aba195845fb250f09f673d5df4fe9bc44ae94aad640c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/view-manifest.json",
        "sha256": "868cad56540b79240cd33c7dc41a47057dd84b59595878731cc50d6fb901e249"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/views/transparent/preview-hero.png",
        "sha256": "95679fbf3e95376d6a11e9504887cefef5ee7e49e1c1b971c0cb0f639d99afaf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/cross-bedded-sandstone/r001/runs/build/cross-bedded-sandstone/r001/semantic-rebuild-1/4956d25bc9c99fafc3543af3219c521643430a927599d63c6d3c2e10ef6e5427/20261018T235505-e8242f0e2c3b4b5fab0c03b556549dd7/request.json",
        "sha256": "4d63e23a76f6a094a75f93ba35a48b2d604a9bba446c1343cf396dc3d4d939f5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/cross-bedded-sandstone/r001/runs/build/cross-bedded-sandstone/r001/semantic-rebuild-1/4956d25bc9c99fafc3543af3219c521643430a927599d63c6d3c2e10ef6e5427/20261018T235505-e8242f0e2c3b4b5fab0c03b556549dd7/result.json",
        "sha256": "77a4893f59e11687d705e458fa8cfee1e76e493eca82d7def49bd1b10e566973"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/cross-bedded-sandstone/r001/runs/build/cross-bedded-sandstone/r001/semantic-rebuild-2/2a7a2491d9dabeea947cbe86a26f4639859221d6f14bbb750ceb8a622b3f004f/20261018T235507-0f6ede6e92e14e1faa37a9f6257b4b97/request.json",
        "sha256": "41bcb706e2bce75a3a714e43461b05c9e9df967f087af9b55d55544f0d7f314a"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-32/cross-bedded-sandstone/r001/runs/build/cross-bedded-sandstone/r001/semantic-rebuild-2/2a7a2491d9dabeea947cbe86a26f4639859221d6f14bbb750ceb8a622b3f004f/20261018T235507-0f6ede6e92e14e1faa37a9f6257b4b97/result.json",
        "sha256": "404aba9515cb46046905a51c671e5ca0bf43a4cbb4e078cacfd1b848b168c489"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/LICENSE.txt",
        "sha256": "db8890e9554fb0b9169d1815dab2dce607891b9af41ad24d8b937f8178045cae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/build-config.json",
        "sha256": "0a9b1878083b971f89cd91cb7f07af8821866993a7ed66b254e90ed5dd9fe697"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/freeze.json",
        "sha256": "cb86c0815c5e2fcbe64e38954906b0ab6dad35fcf786d1648bb18e90adfe73c9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/gltf-validator.report.json",
        "sha256": "293057e0acc368a61ff5be8ff6c30bf2266bdbe4c9c381672355e487fadff131"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/inspect_source.py",
        "sha256": "e609fd2bc5fb1a66e961a9574138e3d7460399939142604fde8be5a727ce9f37"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/inventory-record.json",
        "sha256": "c26d3b9a6dbfcc0a109ce655d37fb221ac90e9051d9dc1c65a9ecc47d36b5fb5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/reference-policy.json",
        "sha256": "f148fd95e73529d76ba53008716e6e72fc32724181a29566e5c28f0e6801b93b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/render.py",
        "sha256": "aa40f86d2048c10ab7e879b1c4104a037d6fa9b4549d592c0754840eec318bfc"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-32/cross-bedded-sandstone/r001/runtime.mjs",
        "sha256": "92626742d84d0c68d5a26b27d1538a1b0715230c84272aa08d969911acabf563"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/cross-bedded-sandstone/candidate.json",
      "sha256": "45546631a739bddc5705b8b5b5fc79734fc15bc867316967057429333127bfe5"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/cross-bedded-sandstone-contract.json",
      "sha256": "28df2da6735ddcdbaaebc3b4577a9966e20e2d10ed7660f7c2a35a164d5cbdbc"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/cross-bedded-sandstone-result.json",
      "sha256": "a6ee7e9934a38e5f4197c2f4dcc7369a703e4fe55457ec3bfed3589aed224a1f"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/cross-bedded-sandstone-original-legacy.json",
      "sha256": "41dd6ca9621d794a1cd16d80a8eb0b28a8c19536e8aaf617ae1757201fecd06e"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-32.json",
      "sha256": "97333c8c89a49c94bbe9358649f8e34a7f4460e12a37cd08cb5484af98e66edb"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-32/final-handoff.jsonl",
      "sha256": "045703462fe390bc43200a95dd2f9fc3fae1e4b080f475d9f4c8d0cfa84280f6"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/cross-bedded-sandstone.json",
      "sha256": "2b29e8c631ed2684397df4f72c6655a439e4c3a5b76a435f281b2138f4a95c29"
    },
    "dependencies": []
  },
  "mucrospirifer": {
    "id": "mucrospirifer",
    "batch": "33",
    "source_commit": "1156d5a59362fbc191f217fdacf0dd051b58f95c",
    "review_commit": "f8559b952c68bcadccdac3a6b4596033a2dd7f07",
    "handoff_commit": "1156d5a59362fbc191f217fdacf0dd051b58f95c",
    "review": {
      "path": "qa/independent/continuous-small-life-round11-20261018/batch-33/results.json",
      "sha256": "140fb10c78eeb096572e96a857309b061679ae3260cfdf74cd5cb88d1af21dd5"
    },
    "candidate": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/candidate.json",
      "sha256": "47f73c36c83c4556643c7b5e6926779d1d6ed2277e5a45b09a2d48d1ab9cb006"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/metadata.json",
      "sha256": "c8fabfe87a862972dcf87f7e99666093a23b4ce40e2e4e60c479340433f1b671"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/mucrospirifer.glb",
      "sha256": "55b0f89e3c36912f5ac34b9300527d969ad1aa53956d373c763ce04b1737d748",
      "bytes": 204948
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/mucrospirifer.blend",
      "sha256": "cb037f9fe10d8af64c614ee385e9db3462f6a3a236f0d8f31606802d8d4c44b8",
      "bytes": 843180
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/view-manifest.json",
      "sha256": "fbe7c1f04660f8d115272007c497cddf94d7fabf89da79cf6d7223e63c50f575"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single.json",
      "sha256": "4b99998251854be753b83946fe24374f39abad076fed1d4c9bea9ce435e4ba42"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/scene.json",
      "sha256": "173066e0bf8f66c0bb02da06c5ccab34376aa6e511b736b0df450f9d73a1fb8d"
    },
    "source_export": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/source-export.json",
      "sha256": "0415592c7652677abf1ee8ba5be73a83c8bc7ade6d68f70aab76b69022abd889"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/gltf-validator.report.json",
      "sha256": "c94461e8d0b7224081a088f5e43a70d967a26459617f8cd2e82ecf7473f1b357"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/candidate.json",
        "sha256": "47f73c36c83c4556643c7b5e6926779d1d6ed2277e5a45b09a2d48d1ab9cb006"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/mucrospirifer.glb",
        "sha256": "55b0f89e3c36912f5ac34b9300527d969ad1aa53956d373c763ce04b1737d748"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/mucrospirifer.blend",
        "sha256": "cb037f9fe10d8af64c614ee385e9db3462f6a3a236f0d8f31606802d8d4c44b8"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/generator.py",
        "sha256": "d3ecd7be8a27ab32baec7f7a76f18654dc21c77b1a4a648f01e1a6368ebc8cdb"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/config.json",
        "sha256": "a23ad71b066cff76539d1303df2063c93dae117414c126b12b02124cff01d9a8"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/mucrospirifer/brief.json",
        "sha256": "1880cde87cf1abc32fb4c596b7502b809186fbfe6e53b3da8f848fc3421c3bf2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/references.execution.json",
        "sha256": "307f5cc64c3045f286acd91bad4e3d93fa75dc0d3712e6306dd14aecf5bb506f"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/mucrospirifer/references.json",
        "sha256": "c6cf7c968768bdf0c84d24defde044779561f5ca68a169356c899abbe8aa6e65"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/mucrospirifer/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/mucrospirifer/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/viewer.html",
        "sha256": "a9fda9ac59483d4ad3ba379b9ff560dce95c1211c27755e5eda4efd742e3dcfe"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/browser_qa.mjs",
        "sha256": "7babdc7385fa316ae8170a8da02df88c4c5cef7aa9984ceff83238f4c1238066"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/verify_item.py",
        "sha256": "e93a82e28ca273fce74b75627647bddd6626828c0f15d685662f892ad58bcedc"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/mucrospirifer/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/reference-access.json",
        "sha256": "300c352aaba98154daa3391000fec87effa78139311ee249ed5639490521cf31"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/claim.json",
        "sha256": "3ae253a0b4967ee0222df4a05f914e6b588eee579c3022f6cee04724cd01afaf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/mucrospirifer/inventory-record.json",
        "sha256": "5c674938733f5598287886e847e40d5c1d7d7bc2fb34b5a9f9acbd790bdb8be3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/gltf-validator.report.json",
        "sha256": "c94461e8d0b7224081a088f5e43a70d967a26459617f8cd2e82ecf7473f1b357"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/source-scene.json",
        "sha256": "9400b5ca6c4542ea0e2f36ff4b2dd27e2360c0274db5c508928c707b4d1839c3"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/source-export.json",
        "sha256": "0415592c7652677abf1ee8ba5be73a83c8bc7ade6d68f70aab76b69022abd889"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/reproducibility.json",
        "sha256": "ec497094c033470646d0696b6c5f1860d4937dc2e820d794b4e843ff0f7619b2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single.json",
        "sha256": "4b99998251854be753b83946fe24374f39abad076fed1d4c9bea9ce435e4ba42"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/scene.json",
        "sha256": "173066e0bf8f66c0bb02da06c5ccab34376aa6e511b736b0df450f9d73a1fb8d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/view-manifest.json",
        "sha256": "fbe7c1f04660f8d115272007c497cddf94d7fabf89da79cf6d7223e63c50f575"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/metadata.json",
        "sha256": "c8fabfe87a862972dcf87f7e99666093a23b4ce40e2e4e60c479340433f1b671"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/qa.json",
        "sha256": "f97cf00768fc4b95765dc75d784e22bf3b7b8c11e16b1ff3710ef27df59089bf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/source-contact-sheet.jpg",
        "sha256": "570eaf42615fe2a0bfdd1745752a4f26ecc519ad77f01217fadb104cf7ac4e13"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime-contact-sheet.jpg",
        "sha256": "cd276ccbac355cbb8554b05c4f4b1d52da9648bcd3c0e729dbd005bdd4fa6bf6"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/freeze.json",
        "sha256": "e459998c98a95838a9559284956a4b85a72ee67b893d16fc61462abb4eec6185"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/practical-integrity.json",
        "sha256": "07ee6f5198fcdc71a91d254a9ba81d6830e4bb805d82f19da412152ce1193189"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/profile-contract.json",
        "sha256": "0cce3d04bdc7bbc186a99eddc99c1121a558eb5134fa95c6bd1f849fa0456500"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/profile-gate.json",
        "sha256": "1bc7d7e58f067f7af0520aa7f07b571b74079a78069b9c2c9c1c9ab480ad5c59"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mucrospirifer/r001/legacy-gate.json",
        "sha256": "3f93a6d698be1a49bd1296a488a4477df03766b1d60abf4487402447f1703c36"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/preview-hero.png",
        "sha256": "a9bc7f4c7b3aa4959227adf7788fa749a219b6498e0807902ed71cb374e66c57"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/preview-reversehero.png",
        "sha256": "5d61dd8010af95399847afa98e4c0f4f42e9363df3a009fad3653956262e104d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/preview-front.png",
        "sha256": "f76865b9d0870f7d0e774208edeff3a351d036804a9bf5db905dc0f3c625a30e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/preview-side.png",
        "sha256": "44f9ed75db02ce1df1583c9fd795b694d28ec7de9b5f08768825a02a3c00e390"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/preview-rear.png",
        "sha256": "578029a8afd5c2f9a953c376a004f66759714e2068142063c16ea9cf6f6f9513"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/preview-top.png",
        "sha256": "925ac24470d46ef4c0b38012d1ca726951f9309138a580da0b5d73b238ba66ea"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/preview-clay.png",
        "sha256": "977138d10c58cbb61ccdca52312ddad36049c36d6b1879394ee1e6c6bef8e836"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/preview-silhouette.png",
        "sha256": "9a588ef2f06add14b832db8177f8416c9facf243296107c0f4860c778d2f9741"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-hero.png",
        "sha256": "d339eadf57fc2a0b9cbb3b8f388dca8abcddbcf9e101376e3ec664afdf782d05"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-reversehero.png",
        "sha256": "00325a0ae52f0b7a124785669957c38fa5146ead5b334940f3a5d649fc602e3b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-front.png",
        "sha256": "868a1f83184600eb1c654131cc01d0dfa4a3a354c7069bc24d1ee5da50c82e9d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-side.png",
        "sha256": "d66f3582ada8b4194eabea29530fc8ed0c7dd46918472a0fea90faea2024afb4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-rear.png",
        "sha256": "54938070762a33b0079724ab0862c04aa8722f96bd62674e5f7ce4b897de2af5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-top.png",
        "sha256": "83992ec77cab30142fd1ee2c6f4b0be15050205946b9a74f5fb6ad11556461de"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-bottom.png",
        "sha256": "e52c196021629273e06181381d73260ade1353c6aff4dc7639286924d1940b80"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-80px.png",
        "sha256": "0b2d84cf94bf8082aa437e5a8b6cc4e8b619c53010a4135b82ad571a4240b5d8"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-160px.png",
        "sha256": "d7f3c8d70c45bb709ff5eb0421035de8041c38fbb8a8f4b9483991ce71160850"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/single-240px.png",
        "sha256": "424c21401dfe37497e50df51639128724d10d8ba2a86e9efa688f71a9ef66fd6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/scene-hero.png",
        "sha256": "8a7ae0aa194b466b85cc310f067e8d2ad32218f275a4227ccaf46df126776029"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/mucrospirifer/r001/attempt-01/mucrospirifer/runtime/scene-top.png",
        "sha256": "e18be9fbe9ff4f640396fe21b13c865a5fe105223981d33e9530000a626e06bf"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/mucrospirifer/candidate.json",
      "sha256": "ade42668d6dc0272708d6f56c2e4a93fdeea36ac54296f94d3e08c4774e7a43e"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/mucrospirifer-contract.json",
      "sha256": "8f80885f9544e0a4b674808b8b1a9faf846753a16584cfc18fe7625ac2d604c6"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/mucrospirifer-result.json",
      "sha256": "929ff9d7094619e1cf0d75f64d76e5e9c3ef2cc38219991bb86f5b30ddb51721"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/mucrospirifer-original-legacy.json",
      "sha256": "3f93a6d698be1a49bd1296a488a4477df03766b1d60abf4487402447f1703c36"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-33.json",
      "sha256": "89dcedfc7da1ecf55b3373799498b4b19209729f5c9ebf10ffc48139d6aea296"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/HANDOFF.json",
      "sha256": "f2d0205326be610effa38837645b2a56268543fc6e532ae48c8f3fd666240b01"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/mucrospirifer.json",
      "sha256": "cfea872cdf0af2ab6f688e32bdedf5f8ac8c1cb7a8b8b41e01c44c7ca6eeac68"
    },
    "dependencies": []
  },
  "wave-cut-platform": {
    "id": "wave-cut-platform",
    "batch": "33",
    "source_commit": "1156d5a59362fbc191f217fdacf0dd051b58f95c",
    "review_commit": "f8559b952c68bcadccdac3a6b4596033a2dd7f07",
    "handoff_commit": "1156d5a59362fbc191f217fdacf0dd051b58f95c",
    "review": {
      "path": "qa/independent/continuous-small-life-round11-20261018/batch-33/results.json",
      "sha256": "140fb10c78eeb096572e96a857309b061679ae3260cfdf74cd5cb88d1af21dd5"
    },
    "candidate": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/candidate.json",
      "sha256": "6694bde33df4e89c9d272036296b824ef9a6995ab7ee1585e7c0607431be21d4"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/metadata.json",
      "sha256": "9f01834dc458740e3588c6960ff32444235339eeb1b9c1a19e8dce3000b753d7"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/wave-cut-platform.glb",
      "sha256": "fbeffd65ef58a40e7276d5c474d0956b2e02203fe8c122f7bf0f48bacda8ecc3",
      "bytes": 124244
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/wave-cut-platform.blend",
      "sha256": "9cacb487fff9a0d0fa8816f90285f69d7691a35fccf99f818545e8f9c800d7c0",
      "bytes": 791112
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/view-manifest.json",
      "sha256": "9c55a0152e1cc9096fa4e9d52eebefa4460c11f7b180a806d3f5ed0a94434a72"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single.json",
      "sha256": "5aacbc6dbc4aa493cf1e7b00db165adf9841c4558512839d6d3cc0323441e740"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/scene.json",
      "sha256": "facd21dd455294e2b0bd6599dad98fda433d6add5af7f73ec4aa697a3b8d9523"
    },
    "source_export": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/source-export.json",
      "sha256": "1a1b33fb70dfb9307844ae3df6558a0a59af29298a74408198e0453eb26a1d6b"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/gltf-validator.report.json",
      "sha256": "8174694e57098d8664a515ff30c1373a536f0e86d635772d65c07013367d3a05"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/candidate.json",
        "sha256": "6694bde33df4e89c9d272036296b824ef9a6995ab7ee1585e7c0607431be21d4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/wave-cut-platform.glb",
        "sha256": "fbeffd65ef58a40e7276d5c474d0956b2e02203fe8c122f7bf0f48bacda8ecc3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/wave-cut-platform.blend",
        "sha256": "9cacb487fff9a0d0fa8816f90285f69d7691a35fccf99f818545e8f9c800d7c0"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/generator.py",
        "sha256": "758f44cf1daf5c8ab132826302b2e098dadc098250272dddd4804d7a1f54f34f"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/config.json",
        "sha256": "27a2acb508f6d62730b15290e71ea386ecaa8ba4be75160cc5c624bf117e9912"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/wave-cut-platform/brief.json",
        "sha256": "9779339c23a43370b73040fbc3c7cbf914bd970b3cd813556490cd3a7c6e1ee0"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/references.execution.json",
        "sha256": "756567ea698754a2ffd340db1a03f4344f7a54ed153c1f0e0005a0b4db625977"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/wave-cut-platform/references.json",
        "sha256": "716a48861e611911f0db8352fdd8593cd7db3642e5d3549b79ca0479e9f8b969"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/wave-cut-platform/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/wave-cut-platform/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/viewer.html",
        "sha256": "a9fda9ac59483d4ad3ba379b9ff560dce95c1211c27755e5eda4efd742e3dcfe"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/browser_qa.mjs",
        "sha256": "7babdc7385fa316ae8170a8da02df88c4c5cef7aa9984ceff83238f4c1238066"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/verify_item.py",
        "sha256": "e93a82e28ca273fce74b75627647bddd6626828c0f15d685662f892ad58bcedc"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/wave-cut-platform/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/reference-access.json",
        "sha256": "300c352aaba98154daa3391000fec87effa78139311ee249ed5639490521cf31"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/claim.json",
        "sha256": "3ae253a0b4967ee0222df4a05f914e6b588eee579c3022f6cee04724cd01afaf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/wave-cut-platform/inventory-record.json",
        "sha256": "41640557ff99a2476c634c0f89aa8261f44462c4a3aff2078778b0a8aa48bc38"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/gltf-validator.report.json",
        "sha256": "8174694e57098d8664a515ff30c1373a536f0e86d635772d65c07013367d3a05"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/source-scene.json",
        "sha256": "bcfa56bc85c39d455def3c9e782a28aa63c376376dc408aa3fedcfdd6431929a"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/source-export.json",
        "sha256": "1a1b33fb70dfb9307844ae3df6558a0a59af29298a74408198e0453eb26a1d6b"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/reproducibility.json",
        "sha256": "38d82df97b226b0a8eb3a1d46c77eb03b16bc0126f940891498315d7ef09f79c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single.json",
        "sha256": "5aacbc6dbc4aa493cf1e7b00db165adf9841c4558512839d6d3cc0323441e740"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/scene.json",
        "sha256": "facd21dd455294e2b0bd6599dad98fda433d6add5af7f73ec4aa697a3b8d9523"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/view-manifest.json",
        "sha256": "9c55a0152e1cc9096fa4e9d52eebefa4460c11f7b180a806d3f5ed0a94434a72"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/metadata.json",
        "sha256": "9f01834dc458740e3588c6960ff32444235339eeb1b9c1a19e8dce3000b753d7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/qa.json",
        "sha256": "e8f803423e8956c39235c98b696af96c4c6f4622d61c4c8d5148ce9a03080eef"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/source-contact-sheet.jpg",
        "sha256": "a30fb8752450b1a52882c6d2c699021d0a8fd8b4505ef2386dc8d6357cb504d7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime-contact-sheet.jpg",
        "sha256": "5cc258e4c634db8dd0305dec68b2a44b56d59f8201002d06cef513ac2d59168e"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/freeze.json",
        "sha256": "4dc8d7ea7a2fe7d80965b9acef9eec967379acfd8e7529d323f0d9a25b11cafa"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/practical-integrity.json",
        "sha256": "abe07919b48a218afb64ab977420eb14e5e6b78a163fb34cd8528e7ae871d3bb"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/profile-contract.json",
        "sha256": "2d37062721532da4202951122d02351ed1fc2072eafe66531a6335930feb3cd5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/profile-gate.json",
        "sha256": "f3c14925f23f1684ec8a685365b99ec2d314a7428837275153358d989ba3d356"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/wave-cut-platform/r001/legacy-gate.json",
        "sha256": "4d53f8d1a4b77ffe083492975792e709a76297ff25a3e99ffb3fd1562113a615"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/preview-hero.png",
        "sha256": "d8ee443397c2a660accddda171c492514b0c17ee3874e832cf962a0f1731c4bd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/preview-reversehero.png",
        "sha256": "af6a49bbc670f1271140479af9c97f7a725f98652f3c48920af95dd20dfcfc58"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/preview-front.png",
        "sha256": "f5d4db808017fe3cf3e631f7a3318bb8a2337f27ecf39353280c52b256c20d09"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/preview-side.png",
        "sha256": "d538e500e096f389d6a26e72592bcd05e477b1c3c1f8ac3603d8822fd97f438e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/preview-rear.png",
        "sha256": "5b57766aa51f72fc909953e4d7da1ba23fc9f9618992998a0b8ed2d13c6c206c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/preview-top.png",
        "sha256": "8058fa0100a25fa2517a2e386b4e758880713b9f9cafff156ba925a34e320eb2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/preview-clay.png",
        "sha256": "88aa27be017fc66fe6db99fd26f0a7d8da3834ba035fbeb0905d5626ed8665de"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/preview-silhouette.png",
        "sha256": "72a95886e6bf891765068de9c8e12446421233b13f5035159c497c2f3d95e204"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-hero.png",
        "sha256": "1ae042e10c211d6613c2df42e53fb8275457310d87e61c2dd79d4cae5f258701"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-reversehero.png",
        "sha256": "0fcd82bf5b1609ed29e0f07b9015bdbc954ccbb1c3b828fd88ec6eebbea799d6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-front.png",
        "sha256": "fcacf7ead3447409cc76ac0e0bf88aae2507d6fdbdba79c0a8e1f772757d2e52"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-side.png",
        "sha256": "3a581eea7591595e2021d593a25d826d0701c01676d61b0cf6daf8acad2456ca"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-rear.png",
        "sha256": "a1e2c9d9461fc90741da640dc7aecdbb2eb128d7a398c6917f866d53abf58583"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-top.png",
        "sha256": "eb5d87a28ac4552f6cc6f7f90b5a7c1e7b821dd9d752ce15bddb029fece5b6e5"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-bottom.png",
        "sha256": "5b4853c57bcf4afaa3642b954638e797cc398a34d1f2081d80dcc9326a34bb33"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-80px.png",
        "sha256": "32ac789c13bb06b0f134bc642d4b83e74dad554f4296245684b68c0bece5925c"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-160px.png",
        "sha256": "9117fce7429bc6909470ed07b58b77952c817613ff2fd44a6afbef6b891822f9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/single-240px.png",
        "sha256": "e9071949497cb8556e9e42817f6089fb3065bd82504cb6e44834ad233fab477e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/scene-hero.png",
        "sha256": "1976e38341d4046c9c8205b1ba11f1eac5a42b5c24b4d46f3acca37d560af129"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/wave-cut-platform/r001/attempt-02/wave-cut-platform/runtime/scene-top.png",
        "sha256": "a135743696a8999cd7fb9c5613bbddf9ae47f929b7027b2b5dfed8bb1fb3440a"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/wave-cut-platform/candidate.json",
      "sha256": "146106d980cc9908a8952a3366585c2758e38cca929b137b80f9d2f65703f3ab"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/wave-cut-platform-contract.json",
      "sha256": "e5804c94fc70bb598ecf2d5dc34b6fb04813a60b78ab114a086daf94414dccf1"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/wave-cut-platform-result.json",
      "sha256": "3a39800d2212ac78e9dc3137ee99da0f67478bd5d65fab95920e1f88b1b323d5"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/wave-cut-platform-original-legacy.json",
      "sha256": "4d53f8d1a4b77ffe083492975792e709a76297ff25a3e99ffb3fd1562113a615"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-33.json",
      "sha256": "89dcedfc7da1ecf55b3373799498b4b19209729f5c9ebf10ffc48139d6aea296"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/HANDOFF.json",
      "sha256": "f2d0205326be610effa38837645b2a56268543fc6e532ae48c8f3fd666240b01"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/wave-cut-platform.json",
      "sha256": "e4e158927a02ed9dddcb374a4664f6628ed1ed3fbbe3560069f5555b7d927920"
    },
    "dependencies": []
  },
  "flute-cast-slab": {
    "id": "flute-cast-slab",
    "batch": "33",
    "source_commit": "1156d5a59362fbc191f217fdacf0dd051b58f95c",
    "review_commit": "f8559b952c68bcadccdac3a6b4596033a2dd7f07",
    "handoff_commit": "1156d5a59362fbc191f217fdacf0dd051b58f95c",
    "review": {
      "path": "qa/independent/continuous-small-life-round11-20261018/batch-33/results.json",
      "sha256": "140fb10c78eeb096572e96a857309b061679ae3260cfdf74cd5cb88d1af21dd5"
    },
    "candidate": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/candidate.json",
      "sha256": "b8a1b631e1a55eba33439008fed32b8b2120e677f9bcb83cb4ab8ac8190ffd2f"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/metadata.json",
      "sha256": "7458c74e26a5505a78882d104ddf6f614c4d6587227df77ee063683fb6b98f8f"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/flute-cast-slab.glb",
      "sha256": "4ebbbc5561e622b2ce2fa777dfc6ec4236b1c6fa736a5caf14d290142f5b2268",
      "bytes": 203036
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/flute-cast-slab.blend",
      "sha256": "3843311eed5ba4b212371558591dca8a42d0531db9490fd6d89512b2a6ca70f6",
      "bytes": 1024884
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/view-manifest.json",
      "sha256": "179762e0395567e10cd680ed77a7192059b92cc9d52e3c3c9f93a5e633d61a87"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single.json",
      "sha256": "9ff6885d14dd4c66292ea09a0ba25b9108f6a6b0c9fd13cb98fecd33af2d054e"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/scene.json",
      "sha256": "6ea77a209de64a13d37064ac2c594a961856272726216b3042889d8f75aa79aa"
    },
    "source_export": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/source-export.json",
      "sha256": "85f8fdd03c803868387855514c5accb5d7fd2ffdbe200c3eef8b3150c3d7c2a7"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/gltf-validator.report.json",
      "sha256": "8dd42ed9c2d0b7f12b70206262de562f0a9de263c0e9edb76885f6ab2c3fe441"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/candidate.json",
        "sha256": "b8a1b631e1a55eba33439008fed32b8b2120e677f9bcb83cb4ab8ac8190ffd2f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/flute-cast-slab.glb",
        "sha256": "4ebbbc5561e622b2ce2fa777dfc6ec4236b1c6fa736a5caf14d290142f5b2268"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/flute-cast-slab.blend",
        "sha256": "3843311eed5ba4b212371558591dca8a42d0531db9490fd6d89512b2a6ca70f6"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/generator.py",
        "sha256": "88f8bd526b6b7007634333e0c30f75ae367d3e6c37113f6f3d39a1cf4f91556f"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/config.json",
        "sha256": "6a80470feb067f289ed279a536975250159b502bd59a5b5862db1bac124506da"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/flute-cast-slab/brief.json",
        "sha256": "481eab4e3d85f5844b07caeb1ffc3036fc3527ea0249b0177bbcfc883f883da9"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/references.execution.json",
        "sha256": "5b918935b63df0c27691d4375d912d04d60c441d13627404ff6627032f19d1c2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/flute-cast-slab/references.json",
        "sha256": "daa9b1e7038df3699febf10d97c88b360db0e48908d25b3d8319f52e01494c73"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/flute-cast-slab/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/flute-cast-slab/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/viewer.html",
        "sha256": "a9fda9ac59483d4ad3ba379b9ff560dce95c1211c27755e5eda4efd742e3dcfe"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/browser_qa.mjs",
        "sha256": "7babdc7385fa316ae8170a8da02df88c4c5cef7aa9984ceff83238f4c1238066"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/verify_item.py",
        "sha256": "e93a82e28ca273fce74b75627647bddd6626828c0f15d685662f892ad58bcedc"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/flute-cast-slab/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/reference-access.json",
        "sha256": "300c352aaba98154daa3391000fec87effa78139311ee249ed5639490521cf31"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/claim.json",
        "sha256": "3ae253a0b4967ee0222df4a05f914e6b588eee579c3022f6cee04724cd01afaf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/flute-cast-slab/inventory-record.json",
        "sha256": "a00557b30b3aef5714a479d96e91689c368463e8fb582b0f0db2cb6eaab6cc5d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/gltf-validator.report.json",
        "sha256": "8dd42ed9c2d0b7f12b70206262de562f0a9de263c0e9edb76885f6ab2c3fe441"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/source-scene.json",
        "sha256": "a29776a54031d0bbcdb97a151fade5917fe43c71aa15151a7ef21cee0c3d9f98"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/source-export.json",
        "sha256": "85f8fdd03c803868387855514c5accb5d7fd2ffdbe200c3eef8b3150c3d7c2a7"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/reproducibility.json",
        "sha256": "6988fdb13d7ba83c496bffd682f5c40b836e98aa338be6fbefea991ab713721f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single.json",
        "sha256": "9ff6885d14dd4c66292ea09a0ba25b9108f6a6b0c9fd13cb98fecd33af2d054e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/scene.json",
        "sha256": "6ea77a209de64a13d37064ac2c594a961856272726216b3042889d8f75aa79aa"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/view-manifest.json",
        "sha256": "179762e0395567e10cd680ed77a7192059b92cc9d52e3c3c9f93a5e633d61a87"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/metadata.json",
        "sha256": "7458c74e26a5505a78882d104ddf6f614c4d6587227df77ee063683fb6b98f8f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/qa.json",
        "sha256": "03838c63e5285a88b98e3ce40bcd0c582715468cf6f410cf936b9f808d260bc4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/source-contact-sheet.jpg",
        "sha256": "3afc48119159a2a4cdc1c15bc569df73583bfcf7c6e869443737ee4ce050e5f2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime-contact-sheet.jpg",
        "sha256": "9ae5955112cef0a18f20442a53c638cc4cce15066328859281db9da250035dd7"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/freeze.json",
        "sha256": "b385887d65bbca938acae74765fd1506045d55211a41afaaeade925877439e29"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/practical-integrity.json",
        "sha256": "427ed8be2028bbaa6f7d1d1f165167336116c7154ef93bbc2e5e20a274f2033c"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/profile-contract.json",
        "sha256": "7e785f7ebbece8f6b3bd10d01fd07b94ec15b8e22b23e234a0f33885c0a4b2e7"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/profile-gate.json",
        "sha256": "b84d3c2c834766d9843cbb9c42a771aa4265b7e9e62ee942e9c87a2a6ebf6347"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/flute-cast-slab/r001/legacy-gate.json",
        "sha256": "d0bc4c0cfb01857c2c3b5ae31772ac5fd3a1229f005fe71d46186765f96f1f28"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/preview-hero.png",
        "sha256": "52fac7e22c0d21c26ea35dc924715cedcde1766ec5c5f4a489897d5ec987cd20"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/preview-reversehero.png",
        "sha256": "e24533fbb0925834deeb49bb313937996b9e0566dc95a6c7f914cf32e98f1e06"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/preview-front.png",
        "sha256": "e6c8b1dfefca00df7fd8e0761f7afd36e189d1c05f1f1081febcb9d8d1d73007"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/preview-side.png",
        "sha256": "ae927b4be5e81898dab9f188cc8e0d119bbbf83146fa55af1622a789ee65660d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/preview-rear.png",
        "sha256": "b6f466912dac8829570840e9c126c2f20b43ec4604bc53289a0de228781264e1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/preview-top.png",
        "sha256": "9407aa71bf59599f68091dcd8efd9db211c8b61f8d522f08576d094d01dd98a6"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/preview-clay.png",
        "sha256": "bf1c4c7935a55ca8cbb68725ff25ca2441e89af6eda294c5f419e6e6089e9cbf"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/preview-silhouette.png",
        "sha256": "51d040c1113f24385531a37acc10e7a777775a2069d245563728001e347d9d98"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-hero.png",
        "sha256": "1380e4ee8febf94d9925183b7ddda61e5dbd1c2ba67f689bb79eddfb019d1841"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-reversehero.png",
        "sha256": "7dae9641745b522ae5cb07edfadc06848834c4b5f71cdbb9bdbf228988d881b2"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-front.png",
        "sha256": "d2f5fe14a3b6d4313403983c5c4a78736c2dabfd292de95d96c7d4f65273ecd9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-side.png",
        "sha256": "4b5d302603d3f9ab5b3488287309aa1eb1f7b6f3f1f5f71d445f86d6dfcb8d48"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-rear.png",
        "sha256": "a4b15281b13868b64dcb09b9eb952eb5f606965e8879f7994b5e1db268625630"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-top.png",
        "sha256": "b92d23c7b483f683075619cac1186612bc4abdfa24079b57115c3b5e1e03405e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-bottom.png",
        "sha256": "47cbf990b5a46eb9475898d4c632f004d85e154c8108645035aeb57620db4389"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-80px.png",
        "sha256": "ee7829537a5fd366031887e12f784ae32d6f1edf7e3d430aad4e8adec609a432"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-160px.png",
        "sha256": "e269f385da6fa462b6965c94b8bed6d5ccf61e330e50667a9e1ef35ee0fedde7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/single-240px.png",
        "sha256": "20085a47c8e45f6e7e87d5d0dc8bad27e986c39e057d8e78f3c86caaaa7e47bb"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/scene-hero.png",
        "sha256": "203ab16b5a5a2180c1920d8004c7a81750db71b0e6be08ba443e0814bee196fd"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/flute-cast-slab/r001/attempt-01/flute-cast-slab/runtime/scene-top.png",
        "sha256": "27c40233205cf22ab640ba8e6f0b13ce5c41b1e9f9431d6a34613fe23d244cc4"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/flute-cast-slab/candidate.json",
      "sha256": "6954cbf74aa573eb7608634b6462f2b858a972ac465f1ce755c3789666d7fc88"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/flute-cast-slab-contract.json",
      "sha256": "03094d961670dfa57c7972ede22f9e431fb210d840f6bd9db732e742d20f9704"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/flute-cast-slab-result.json",
      "sha256": "ca27eb7eed5751bf71db8cb3771d43e04fa18a5ec21d8e606a2723d8e30fa24b"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/flute-cast-slab-original-legacy.json",
      "sha256": "d0bc4c0cfb01857c2c3b5ae31772ac5fd3a1229f005fe71d46186765f96f1f28"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-33.json",
      "sha256": "89dcedfc7da1ecf55b3373799498b4b19209729f5c9ebf10ffc48139d6aea296"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/HANDOFF.json",
      "sha256": "f2d0205326be610effa38837645b2a56268543fc6e532ae48c8f3fd666240b01"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/flute-cast-slab.json",
      "sha256": "2186f1efd91550c5bcaa9d76e724dd6da59216249894801ba33fbaaf341695d0"
    },
    "dependencies": []
  },
  "paleodictyon-mesh-trace": {
    "id": "paleodictyon-mesh-trace",
    "batch": "33",
    "source_commit": "1156d5a59362fbc191f217fdacf0dd051b58f95c",
    "review_commit": "f8559b952c68bcadccdac3a6b4596033a2dd7f07",
    "handoff_commit": "1156d5a59362fbc191f217fdacf0dd051b58f95c",
    "review": {
      "path": "qa/independent/continuous-small-life-round11-20261018/batch-33/results.json",
      "sha256": "140fb10c78eeb096572e96a857309b061679ae3260cfdf74cd5cb88d1af21dd5"
    },
    "candidate": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/candidate.json",
      "sha256": "78ef3256a3ccc4629a278edd1db7692d05b08ddf349fc5c5459fc3c5c44d8b30"
    },
    "source_metadata": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/metadata.json",
      "sha256": "496207ab32c9f0f17845368004ae1bd7c46f7dbd619a60ce207f442cbcec234d"
    },
    "glb": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/paleodictyon-mesh-trace.glb",
      "sha256": "d0a4427dae977a5c12f7f09b541d36316b0a353ef2237ded516099f9885bef4d",
      "bytes": 129216
    },
    "blend": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/paleodictyon-mesh-trace.blend",
      "sha256": "ab4485589b31415bf4919a940c2184d6efc793191ce9259894788f80274624fa",
      "bytes": 687148
    },
    "views": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/view-manifest.json",
      "sha256": "dc2c18ce733ddf6818fe998aa0a3d75d30c18944427390f56d844ce398771434"
    },
    "runtime": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single.json",
      "sha256": "25e7a82799c2054d8ec4fc1e4b4ef3ec6755e49b2d0e3a690cd1f3727f1f3796"
    },
    "scene": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/scene.json",
      "sha256": "fe19f0d5515da87145b3cc626fa51b21e66211df3f4f7465f4b66cc4b62e9614"
    },
    "source_export": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/source-export.json",
      "sha256": "494080ebe10af796b308326b257a22e10d941d04126924b58da9502d80270383"
    },
    "validator": {
      "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/gltf-validator.report.json",
      "sha256": "f178c08be981e2c26b4c82c707d7fa46100e4fdbf9b7dbe02ca0d0456ce1b442"
    },
    "evidence": [
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/candidate.json",
        "sha256": "78ef3256a3ccc4629a278edd1db7692d05b08ddf349fc5c5459fc3c5c44d8b30"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/paleodictyon-mesh-trace.glb",
        "sha256": "d0a4427dae977a5c12f7f09b541d36316b0a353ef2237ded516099f9885bef4d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/paleodictyon-mesh-trace.blend",
        "sha256": "ab4485589b31415bf4919a940c2184d6efc793191ce9259894788f80274624fa"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/generator.py",
        "sha256": "f63dacbc4b52588ce3fd497ffefba41fbb258f2653987eb588df0a2e8d59dcaf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/config.json",
        "sha256": "98d2b74aeed1791a947da93a93e1925202cb832ea513366dda86743336b73f2c"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/paleodictyon-mesh-trace/brief.json",
        "sha256": "6dd04e8a1685cf02456684b3860d884f420e7f3ed6b7d805b28e96a03232b668"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/references.execution.json",
        "sha256": "21caa7c6b185cb34af8ffaad34263ec28a25cdc3651746213be8fd28e3d40c47"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/paleodictyon-mesh-trace/references.json",
        "sha256": "3ed2ef808b41978a4b4ffed56ab7af7f71f8a6763e0c342c96ccb71aba7cb590"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/mesh_utils.py",
        "sha256": "b9c432dd823f71e3ab621923dc15451dbced524bc50038f25f73f26b3a00214b"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/paleodictyon-mesh-trace/scripts/asset_common.py",
        "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/paleodictyon-mesh-trace/scripts/qa_glb.py",
        "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/inspect_source.py",
        "sha256": "c646b1e95c2e6945728624b22d29ad46ab3d29c1030e83e89e433150a159e9f5"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/viewer.html",
        "sha256": "a9fda9ac59483d4ad3ba379b9ff560dce95c1211c27755e5eda4efd742e3dcfe"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/browser_qa.mjs",
        "sha256": "7babdc7385fa316ae8170a8da02df88c4c5cef7aa9984ceff83238f4c1238066"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/verify_item.py",
        "sha256": "e93a82e28ca273fce74b75627647bddd6626828c0f15d685662f892ad58bcedc"
      },
      {
        "path": "production/continuous-release-round11-20261018/source-snapshots/paleodictyon-mesh-trace/package-lock.json",
        "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/reference-access.json",
        "sha256": "300c352aaba98154daa3391000fec87effa78139311ee249ed5639490521cf31"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/claim.json",
        "sha256": "3ae253a0b4967ee0222df4a05f914e6b588eee579c3022f6cee04724cd01afaf"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/items/paleodictyon-mesh-trace/inventory-record.json",
        "sha256": "6b65789f2722cedfaa9fc6ca5b4172e48e74863140351865b09e32931488823d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/gltf-validator.report.json",
        "sha256": "f178c08be981e2c26b4c82c707d7fa46100e4fdbf9b7dbe02ca0d0456ce1b442"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/source-scene.json",
        "sha256": "9c21fb88ee0b5b59dbb3b1de19a6ead5475f818b33f95e0db24dc3b1238fb2f9"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/source-export.json",
        "sha256": "494080ebe10af796b308326b257a22e10d941d04126924b58da9502d80270383"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/reproducibility.json",
        "sha256": "29df714b204ddfbca8479dc3092175f04477dfac2aab01d99736ac32f6dab24e"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single.json",
        "sha256": "25e7a82799c2054d8ec4fc1e4b4ef3ec6755e49b2d0e3a690cd1f3727f1f3796"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/scene.json",
        "sha256": "fe19f0d5515da87145b3cc626fa51b21e66211df3f4f7465f4b66cc4b62e9614"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/view-manifest.json",
        "sha256": "dc2c18ce733ddf6818fe998aa0a3d75d30c18944427390f56d844ce398771434"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/metadata.json",
        "sha256": "496207ab32c9f0f17845368004ae1bd7c46f7dbd619a60ce207f442cbcec234d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/qa.json",
        "sha256": "2c95597b041088802b43c19dc0792e2166061f1e12da61176b5755787d54c4f3"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/source-contact-sheet.jpg",
        "sha256": "221a6c39dab4f53328e45e2d77e4ae6a86c9f5160e359c333984d72527812bad"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime-contact-sheet.jpg",
        "sha256": "ef2faa9ee3d664380f999f27c792b3656b47392d50ab9764b56419488002d732"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/freeze.json",
        "sha256": "5c9d84daaeb2aae7d3846e7178d6dca85703c5814c665ee45976bfa90721364b"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/practical-integrity.json",
        "sha256": "5ac5872c8f792c6ca69922fa9d8bad3c840aa0db8cb0a1d537462b0a092e2a3b"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/profile-contract.json",
        "sha256": "3f843905ae542a0527e191b3b46f3948e748522ca4defb593b812c1f90a92c82"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/profile-gate.json",
        "sha256": "ce85cc893b5e5e2283be101e6e66748450e4cfd8aa1036df5cb694b4ed48e9e8"
      },
      {
        "path": "production/continuous-small-life-round11-20261018/work/batch-33/paleodictyon-mesh-trace/r001/legacy-gate.json",
        "sha256": "f395c487fd498918c7887d110a1aa782a9e2413b23eae61352abfd26eeac664d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/preview-hero.png",
        "sha256": "52d8512b753d2cdb18b59056886c579bbbad9b67a23c0a6642efa88ce03cb590"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/preview-reversehero.png",
        "sha256": "2e770f4a4fdec8cd17e7bd3635ab51b89d6872982815246ef8dcd4936f42b362"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/preview-front.png",
        "sha256": "c52c4cca0dce4818c3b79062ec7ee702324b95caeed042e834c115bea2f761a4"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/preview-side.png",
        "sha256": "3f27f7c506de55a651c0b0616adff096cc84135921b17553d92c3e58a0f5444f"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/preview-rear.png",
        "sha256": "6519477413eb3face9be388d413147136cc1bcbc6e1547de7b2e3d6d7776540b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/preview-top.png",
        "sha256": "921d7b0d5af12e3d9bd06d217cab32f05b29091c016100c89d9f2c54b076b3ff"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/preview-clay.png",
        "sha256": "1a34a0bce7fbbdcdca06a7991c00d1a5d4eea89e6627878dc8814e13c39681de"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/preview-silhouette.png",
        "sha256": "e8ab30c1ed19c50ec4ce1be333a8b0fa13f8be4f51ad492e1f7b779129077e14"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-hero.png",
        "sha256": "cea1b443364b1841ad340474e7f3a5ec610bb5ff6fa895383686f1a536a6f9a7"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-reversehero.png",
        "sha256": "9f9cd2fb95ef4d58200a791e5905ed42b4b1f526d43cab0898502936521bd610"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-front.png",
        "sha256": "4e7e725dff70dbe88c7e35444d9213f8a9fd556ede32ab06fce27457676110ae"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-side.png",
        "sha256": "d6cb0c6674be8dfb775a628dc13a050f6cc0e4f9f269a2efeadce0d959234577"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-rear.png",
        "sha256": "066e36ef405242304eebd664c6ae0f8a39d2a03fc99595a365cb000ea275c9c1"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-top.png",
        "sha256": "5abbbdff821eeea34dc93262c76bcdaf231d03ecb99333bc223a15a858fa469d"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-bottom.png",
        "sha256": "7b458172f8dc5f26ad280bc719c46294136fde996400c51e896fa9d786902f91"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-80px.png",
        "sha256": "961df45355af3c65ea6a2e3243164307437368dd78a356d4cb8873370a0a68ab"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-160px.png",
        "sha256": "30f8c70e4b772c770b1061a2cb36cf30a48829364f15d0e497494468715a0f42"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/single-240px.png",
        "sha256": "6897d080ff97522f7adc409d12f345bb2903dc91422182ab265fb822992c104b"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/scene-hero.png",
        "sha256": "37c97e0927ae3b35f154a6115836def906a11ee9ce47f76985f1b909b13e1ab9"
      },
      {
        "path": "assets/candidates/continuous-small-life-round11-20261018/batch-33/paleodictyon-mesh-trace/r001/attempt-01/paleodictyon-mesh-trace/runtime/scene-top.png",
        "sha256": "bdbe4051945b49f2d9b0ad4dbd2cdd48107367e617ff5b10ba4f680a400cd125"
      }
    ],
    "profile_candidate": {
      "path": "production/continuous-release-round11-20261018/records/paleodictyon-mesh-trace/candidate.json",
      "sha256": "c82e8119bbe1da96a896c0f65f2a855e413a8a34d2d6f14fe53979ca511ce2ca"
    },
    "profile_contract": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/paleodictyon-mesh-trace-contract.json",
      "sha256": "214ffccf2ef34e6ce82d876bc2e5902d8ad74010bc0977b855289f5a693dcd84"
    },
    "profile_result": {
      "path": "qa/continuous-release-round11-20261018/profile-checks/paleodictyon-mesh-trace-result.json",
      "sha256": "d6b07059723373c39a4dc408441404541dd9c6b631526bc1cc7e7f163c4064c5"
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
      "path": "qa/continuous-release-round11-20261018/profile-checks/paleodictyon-mesh-trace-original-legacy.json",
      "sha256": "f395c487fd498918c7887d110a1aa782a9e2413b23eae61352abfd26eeac664d"
    },
    "qa_bundle": {
      "path": "qa/continuous-release-round11-20261018/qa-bindings/batch-33.json",
      "sha256": "89dcedfc7da1ecf55b3373799498b4b19209729f5c9ebf10ffc48139d6aea296"
    },
    "handoff": {
      "path": "production/continuous-small-life-round11-20261018/work/batch-33/HANDOFF.json",
      "sha256": "f2d0205326be610effa38837645b2a56268543fc6e532ae48c8f3fd666240b01"
    },
    "texture_audit": {
      "path": "qa/continuous-release-round11-20261018/texture-checks/paleodictyon-mesh-trace.json",
      "sha256": "b803fb2fd395327eec19892191389df3e7922e6a20d07bb878ee96d85f55bf50"
    },
    "dependencies": []
  }
};
