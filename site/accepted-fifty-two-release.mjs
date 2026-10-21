// Exact52 independently reviewed bounded delivery. All other publication gates remain mandatory.
export const FIFTY_TWO_RELEASES = [
  {
    "descriptor": {
      "path": "assets/releases/next52-g01-20261021.json",
      "sha256": "7e117cd4aa1ed539e62c3307a6ac664b17a00c188dd96013da8a32afa96ece21"
    },
    "release": {
      "version": 1,
      "scope": "next52-g01-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "06af65fa6e7206f186ab49856d40da5498b35395",
      "review_commit": "06af65fa6e7206f186ab49856d40da5498b35395",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g01-release-20261021/source-bundle.json",
        "sha256": "807e67bad69e15ccee2a38bbcb22456cfa4f66cbe4a2983edfe6049386442ee9"
      },
      "protected_source_inputs": [
        {
          "path": "package-lock.json",
          "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
        },
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
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
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        },
        {
          "path": "scripts/validate_candidate.py",
          "sha256": "fe679a8be19d16b9d9b86ee3419a73d2dd16b77dfa371bf1186ce0120d120ff9"
        },
        {
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/OWN_QA_MANIFEST.json",
          "sha256": "4383fe5b50675164ea203a926cd13a1a407d8ebc88cd3ee2778e9b889a16a0b2"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/handoff.json",
          "sha256": "13aebbb3793f4ae6fa189bc301a614e81500ce5f8ade813b6c24afd602875e94"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/independent-review.json",
          "sha256": "69632c1385e86f9797158ed4845ebdf6d3625faefcf55ee9cd07eb29498fb7f4"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "diplopora",
          "batch": 93,
          "revision": "r002",
          "candidate_root": "production/small-life-batch93/diplopora/r002",
          "source_commit": "06af65fa6e7206f186ab49856d40da5498b35395",
          "reviewed_source_commit": "2cbc3cbb206d81c2383eada3a3f142c2b2c5cd82",
          "original_source_snapshot": "06af65fa6e7206f186ab49856d40da5498b35395",
          "review_commit": "06af65fa6e7206f186ab49856d40da5498b35395",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/diplopora/batch93-20261021/release-metadata.json",
            "sha256": "56cda151ce540c7234624c508477cdaed2cb0224d7673bd3a8fcf91004d177a0"
          },
          "candidate": {
            "path": "production/small-life-batch93/diplopora/r002/candidate.json",
            "sha256": "02d44cbca6f044ad02fe5bc4d62f15639ba51760f67382e6817dba0ae8af4f98"
          },
          "active_candidate": {
            "path": "production/small-life-batch93/diplopora/r002/candidate.json",
            "sha256": "02d44cbca6f044ad02fe5bc4d62f15639ba51760f67382e6817dba0ae8af4f98"
          },
          "original_profile": {
            "path": "production/small-life-batch93/diplopora/r002/profile-contract.json",
            "sha256": "679a6de55187bf2f2b0b5467de99866172ff32c348e333bfb3cf177a2caa1d97"
          },
          "active_profile": {
            "path": "production/small-life-batch93/diplopora/r002/profile-contract.json",
            "sha256": "679a6de55187bf2f2b0b5467de99866172ff32c348e333bfb3cf177a2caa1d97"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-93/independent-review.json",
            "sha256": "69632c1385e86f9797158ed4845ebdf6d3625faefcf55ee9cd07eb29498fb7f4"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-93/independent-review.json",
            "sha256": "69632c1385e86f9797158ed4845ebdf6d3625faefcf55ee9cd07eb29498fb7f4"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-93/independent-review.json",
              "sha256": "69632c1385e86f9797158ed4845ebdf6d3625faefcf55ee9cd07eb29498fb7f4"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-93/OWN_QA_MANIFEST.json",
              "sha256": "4383fe5b50675164ea203a926cd13a1a407d8ebc88cd3ee2778e9b889a16a0b2"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-93/handoff.json",
              "sha256": "13aebbb3793f4ae6fa189bc301a614e81500ce5f8ade813b6c24afd602875e94"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch93/diplopora/r002/artifacts/metadata.json",
            "sha256": "2ab87226e5657cc0c45d48dc88fef073c09cdb71c3a877021dbd480fe13bd373"
          },
          "source_counts": {
            "path": "production/small-life-batch93/diplopora/r002/qa/authored-evaluated-counts.json",
            "sha256": "35d5868d89d5558c522c6b4140c5b3f31b7bc97f153f0b0d85e49ca2128a4304"
          },
          "proof": {
            "path": "production/small-life-batch93/diplopora/r002/views/render-manifest.json",
            "sha256": "118b3a2d4e8fb277d273ff82802799f2d6c59ff1fd663ca1c74323ee80723067"
          },
          "source_preview": {
            "path": "production/small-life-batch93/diplopora/r002/views/hero.png",
            "sha256": "72b096f69b76917d40119ac32637fe4a5aec64a1a4d5a3fd19c71f35c3924ef7"
          },
          "capture_reference": {
            "path": "assets/additions/diplopora/batch93-20261021/diplopora.png",
            "sha256": "9ecbd314d839d2a59ca16cef809713e22e0fd778cf8d84907f3e6049af8cbc71"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/diplopora.json",
            "sha256": "b0ab9220ab2774e92b00e557cc018e04fc78b0acca8e65fa252ec9829b0dcb8b"
          }
        },
        {
          "id": "nathorstiana",
          "batch": 93,
          "revision": "r002",
          "candidate_root": "production/small-life-batch93/nathorstiana/r002",
          "source_commit": "06af65fa6e7206f186ab49856d40da5498b35395",
          "reviewed_source_commit": "2cbc3cbb206d81c2383eada3a3f142c2b2c5cd82",
          "original_source_snapshot": "06af65fa6e7206f186ab49856d40da5498b35395",
          "review_commit": "06af65fa6e7206f186ab49856d40da5498b35395",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/nathorstiana/batch93-20261021/release-metadata.json",
            "sha256": "d3f8e3d5d1a4364eac3fa76b4c8468ff05db8b527e1a7e23c6824e265850cfb2"
          },
          "candidate": {
            "path": "production/small-life-batch93/nathorstiana/r002/candidate.json",
            "sha256": "b06e02392203057ff3d0008f6096f992fe57ab4ca5d4e6379ba522fef8a0a538"
          },
          "active_candidate": {
            "path": "production/small-life-batch93/nathorstiana/r002/candidate.json",
            "sha256": "b06e02392203057ff3d0008f6096f992fe57ab4ca5d4e6379ba522fef8a0a538"
          },
          "original_profile": {
            "path": "production/small-life-batch93/nathorstiana/r002/profile-contract.json",
            "sha256": "2aed2ebf91963f334f24ee38ba538905aa01cd227c30a7bcba74f1bc203602e2"
          },
          "active_profile": {
            "path": "production/small-life-batch93/nathorstiana/r002/profile-contract.json",
            "sha256": "2aed2ebf91963f334f24ee38ba538905aa01cd227c30a7bcba74f1bc203602e2"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-93/independent-review.json",
            "sha256": "69632c1385e86f9797158ed4845ebdf6d3625faefcf55ee9cd07eb29498fb7f4"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-93/independent-review.json",
            "sha256": "69632c1385e86f9797158ed4845ebdf6d3625faefcf55ee9cd07eb29498fb7f4"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-93/independent-review.json",
              "sha256": "69632c1385e86f9797158ed4845ebdf6d3625faefcf55ee9cd07eb29498fb7f4"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-93/OWN_QA_MANIFEST.json",
              "sha256": "4383fe5b50675164ea203a926cd13a1a407d8ebc88cd3ee2778e9b889a16a0b2"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-93/handoff.json",
              "sha256": "13aebbb3793f4ae6fa189bc301a614e81500ce5f8ade813b6c24afd602875e94"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch93/nathorstiana/r002/artifacts/metadata.json",
            "sha256": "c58a4a25e76555c187c3bab9b051e97d91dc4ffe444edce807a43483a7291327"
          },
          "source_counts": {
            "path": "production/small-life-batch93/nathorstiana/r002/qa/authored-evaluated-counts.json",
            "sha256": "7ab199b171ccd2b6ec03576e9c981d5dd0e291acf09464e691c61e8db6969194"
          },
          "proof": {
            "path": "production/small-life-batch93/nathorstiana/r002/views/render-manifest.json",
            "sha256": "48bca22de0a37a3b1cf17d473bee5d7008cebb0a31a6342e6fb45471be9fab43"
          },
          "source_preview": {
            "path": "production/small-life-batch93/nathorstiana/r002/views/hero.png",
            "sha256": "81d324979ad3355dc21e8db2eac5d767c684881942f7860192cb67320f20e5fe"
          },
          "capture_reference": {
            "path": "assets/additions/nathorstiana/batch93-20261021/nathorstiana.png",
            "sha256": "b7b66d78aa37a846a2181ac8a9b272c3cf404a2d740ef44e69ea8f9307525b06"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/nathorstiana.json",
            "sha256": "fb033c15cc874cc4c03f509360dba8fbc5d2efedc669e4665e9a600d556d4aaa"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch93/concepts/diplopora-concept.png",
          "sha256": "5f202471ed9a084d79d6f4f66e233fced1701af45494110a278a89469c008a2b",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/concepts/diplopora-prompt.txt",
          "sha256": "4384ca0ab7dbde96448ce40e6b59952fdc7647adc01a0ad996a6ad5e48d50236",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/concepts/nathorstiana-concept.png",
          "sha256": "02a9c9f8ca9f8b97d56dd89c7db1c4a51a5ce06686ce4d31b45d437649f001de",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/concepts/nathorstiana-prompt.txt",
          "sha256": "e13ff1603f0347c4f3aeedd94620924ceb41f526a781641a6b911721efbaf0f3",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/dependencies-r004-nath-r002.json",
          "sha256": "4916191f23acba3a53f005be1d7c5481af80c4252282fd64d771b9421da49639",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/dependencies.json",
          "sha256": "4d82bbae50d1fa0448ef24d2ee1085f0cbb53a38da029e0e85035c24d28203b8",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r001/references.json",
          "sha256": "74f024c23f75c7d8b1f3c081fbc26f5001ec2937c22cd22cd11762995d6edd1b",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/artifacts/diplopora.blend",
          "sha256": "f557f510fd6f0b917354f13e1ce3be079c55dd8162329ac14fa934598fa2a382",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/artifacts/diplopora.glb",
          "sha256": "b662bfd6068dc7458b2b120d21ae82e7fc3de793e6dc764b192fe99dc9544429",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/artifacts/metadata.json",
          "sha256": "2ab87226e5657cc0c45d48dc88fef073c09cdb71c3a877021dbd480fe13bd373",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/candidate.json",
          "sha256": "02d44cbca6f044ad02fe5bc4d62f15639ba51760f67382e6817dba0ae8af4f98",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/config.json",
          "sha256": "f56cc54f0c14145589a02a6ec714d1e2db15faae2ccfa95b373c3a50d4cc2431",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/delivery-brief.json",
          "sha256": "62705b4c7d45bc5245152ca98b92029936083cddbe00330b57007685c2718bbf",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/profile-contract.json",
          "sha256": "679a6de55187bf2f2b0b5467de99866172ff32c348e333bfb3cf177a2caa1d97",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/qa/authored-evaluated-counts.json",
          "sha256": "35d5868d89d5558c522c6b4140c5b3f31b7bc97f153f0b0d85e49ca2128a4304",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/qa/runtime-parse.report.json",
          "sha256": "ecf94b3b1e7a33b37b060d41516b69a7ce0f8ddd86e190c8f49ea4e1b34e7cfa",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/qa/technical.report.json",
          "sha256": "f00aabca8f3881a541d19b2d1dbc37b01c1491ac01b5e76653ee6e760c8338e2",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/views/clay.png",
          "sha256": "66e3d358a4f3ff3088de6b2e336d86cf3f47f52b5531a55a13ad84678ae4ae51",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/views/front.png",
          "sha256": "8113e6c65eb61ef14febb562c6a1b976a5b03294c8835e0db60d27378a12d154",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/views/hero.png",
          "sha256": "72b096f69b76917d40119ac32637fe4a5aec64a1a4d5a3fd19c71f35c3924ef7",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/views/rear.png",
          "sha256": "22b815cca91d9f04a1961a96e397c44c8d1707524b7a479050d1a328e890886e",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/views/render-manifest.json",
          "sha256": "118b3a2d4e8fb277d273ff82802799f2d6c59ff1fd663ca1c74323ee80723067",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/views/reversehero.png",
          "sha256": "b1d056795476a569b8fbf6a31f96ff085895a0f12b5033d9727f291321cc8f66",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/views/side.png",
          "sha256": "7c4437354e2e6389894ab9392f70aad8d5f1999a3ffd8f68a8a84a18d6f2e922",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/views/silhouette.png",
          "sha256": "1d59bfe0395ec9189eb680044ce4464b3c2aec79dfacfcda31e9f951cd5b4da7",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/diplopora/r002/views/top.png",
          "sha256": "202910235bca1624b25e11a325b0f15b89f259e57c1d309b67206fd4247036de",
          "origin": "source",
          "owner": "diplopora"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r001/references.json",
          "sha256": "2c07b8a649bae0df8d97e61cfb457aeb753b3323cda448a905da1b55d160812d",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/artifacts/metadata.json",
          "sha256": "c58a4a25e76555c187c3bab9b051e97d91dc4ffe444edce807a43483a7291327",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/artifacts/nathorstiana.blend",
          "sha256": "8471058002a975c1caa61dfc2a2fb040558f89fe8a58d24a5f3d76f8de7fab2c",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/artifacts/nathorstiana.glb",
          "sha256": "8f676c164eaf7e82c5a372d533f115f757e1682e8c90af4f16cb78dc1df9f3dc",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/candidate.json",
          "sha256": "b06e02392203057ff3d0008f6096f992fe57ab4ca5d4e6379ba522fef8a0a538",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/config.json",
          "sha256": "c1bd101333583218c65ba2af333756c5474e96a0fc936e5862c86494d4488e79",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/delivery-brief.json",
          "sha256": "26e3319f5635e3717537447ebb4661aab0b34a74bad499bbb33c276695f576e9",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/profile-contract.json",
          "sha256": "2aed2ebf91963f334f24ee38ba538905aa01cd227c30a7bcba74f1bc203602e2",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/qa/authored-evaluated-counts.json",
          "sha256": "7ab199b171ccd2b6ec03576e9c981d5dd0e291acf09464e691c61e8db6969194",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/qa/runtime-parse.report.json",
          "sha256": "020320c24d8a484ed329e4a5728baf1c6a901bf05915d0b72199aa7739b4130f",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/qa/technical.report.json",
          "sha256": "5fdea09aa954e9e7ec59131f5aa38bec9104e387db15032f6306298d631021a4",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/views/clay.png",
          "sha256": "43113ba507ff76fb958785af67469e9b5bcee9f84347fddcd13e98f5ea6a0902",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/views/front.png",
          "sha256": "165353f89404413ce8256d6f59825f45113a45ded4e1de95ee3b6b9713b6a2b3",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/views/hero.png",
          "sha256": "81d324979ad3355dc21e8db2eac5d767c684881942f7860192cb67320f20e5fe",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/views/rear.png",
          "sha256": "5fe388058b310a2b24da309c7d9f0361ea3237e1b7289424f9b1a0f7834de026",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/views/render-manifest.json",
          "sha256": "48bca22de0a37a3b1cf17d473bee5d7008cebb0a31a6342e6fb45471be9fab43",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/views/reversehero.png",
          "sha256": "b254da35165b3e9eb66c95b2f2724f6740c6bb7474a0b60a28333d6e1bf9e3d3",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/views/side.png",
          "sha256": "ddaec03d498c0f60364a51f5ea74d2f029c39c3279a5ea164d46452a8eff169a",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/views/silhouette.png",
          "sha256": "28f5fed24f3deb14c76ccdb5e06b2a45f787ca37bd07b1c7a537765e002d43a9",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/nathorstiana/r002/views/top.png",
          "sha256": "6bd16b1adf75f874cf0a4a50f014f2200ee7cda701fa89c21d0c61c02cfcb512",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/tools/generate-nath-r002.py",
          "sha256": "6c37224ce6343d52d1d1357766f1f8aa9365029fb773f405929d9301ba6951b1",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/tools/generate-r002.py",
          "sha256": "881ff2638624624bebcf43917924be3422bf897078901c4eb0adafc7a4b81e0f",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch93/tools/generate-r003.py",
          "sha256": "e8ab2ed820ee1da1e7a3373fbbc5440e708b7222cb5e4e536443fe1d10f55fdb",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch93/tools/generate-r004.py",
          "sha256": "62d0ac27f0e569c7a8ad2491dde063eca469148349a5a1f80dd637cbba5e50d6",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/tools/generate.py",
          "sha256": "624946b52cb1e7a5f8a3c5bd80d32819d0503f3f82cf64ca8eca852ed67be5c7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch93/tools/measure_source-resume.py",
          "sha256": "e8c66c2c2955b860582170966f952614f058ab8e069294dabc0f06272da338fd",
          "origin": "source",
          "owner": "nathorstiana"
        },
        {
          "path": "production/small-life-batch93/tools/measure_source.py",
          "sha256": "abeae539f8bfa9f25bc7ef510cae9b57fd8f47db1c224717991f31f5c1b40b37",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch93/tools/parse.cjs",
          "sha256": "813bbe4ebbfc1cd80b2d45075f34a43bab68989991e3f81a0858a76c88a790d5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch93/tools/render.py",
          "sha256": "dce6084f0ec6663a5ca5acd3f5815f128314c4e2c94c04748be153ed75c6879e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/OWN_QA_MANIFEST.json",
          "sha256": "4383fe5b50675164ea203a926cd13a1a407d8ebc88cd3ee2778e9b889a16a0b2",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/audit_leaf_features.py",
          "sha256": "0254e0c58969fa5313fee7af9e7e9e100b59a1f5bdbe97769df38619634ad2c3",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/audit_source.py",
          "sha256": "6f1b0140c144a8e9d3ca52e350853fdc84971ae33669896ea7edd5471840b891",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/audit_source_v002.py",
          "sha256": "405da2102f954a7bccbd0cf52d071a04dc183af60add7ed0e634bff64df4a7f1",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/diplopora/queued-at.txt",
          "sha256": "3ac6fbaf0675c0dc6f56ace67a5492025b73ac485b0ff7311330202652399ba1",
          "origin": "review",
          "owner": "diplopora"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/handoff.json",
          "sha256": "13aebbb3793f4ae6fa189bc301a614e81500ce5f8ade813b6c24afd602875e94",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/independent-review.json",
          "sha256": "69632c1385e86f9797158ed4845ebdf6d3625faefcf55ee9cd07eb29498fb7f4",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/nathorstiana/queued-at.txt",
          "sha256": "2c09192125de8cb53a7e8ff2e610a117c90bff378be017332546dbdd7cb0831a",
          "origin": "review",
          "owner": "nathorstiana"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/report.md",
          "sha256": "a429ab0c7724e71bdf4525d27c47658e28b2a736b4dda495e5e72f9cd9218748",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/run-source.sh",
          "sha256": "0c63e21e60b9dd178d85ec45fd5382fa0cffd748e56c8e431deccacb2f875825",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/runtime.mjs",
          "sha256": "7cf070e85813c34feb85faa956e1efcc3a7403b6d947c9c4b6e3d5b96bd4990a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/seal_review.py",
          "sha256": "65d4b755f433b9030606bf0e90376127dd5c87fd244370015858fa112f186fc5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-93/seal_review_v002.py",
          "sha256": "464cf8f29ab375f2be0537ccb1720ba0e5f4e8b4cc6da6f3849d42f52ca49304",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g01-release-20261021/process-archive-index.json",
          "sha256": "a2607e8e6cf03f97672e8f1c5ac896188242c4a0e19f5f960929c4b1331f2de9",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g02-20261021.json",
      "sha256": "5795a0f0541a7b39e405de7b67576c74621c4fba3300781cce59ab63ae0b0474"
    },
    "release": {
      "version": 1,
      "scope": "next52-g02-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "074d56440818359bad76494599209e3f40a155cc",
      "review_commit": "074d56440818359bad76494599209e3f40a155cc",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g02-release-20261021/source-bundle.json",
        "sha256": "29357015d27b2dcac1114c9373d8c53244547276501e041f2a64aef6374c42ac"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
        },
        {
          "path": "scripts/qa_glb.py",
          "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/raw-manifest.json",
          "sha256": "d93eae93fe41d02f6046d020c49e304383c573238c720ff0dc9bfdb9ad3b21a1"
        },
        {
          "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/report.json",
          "sha256": "c08ea64d8ec925d82ed00fa22eeab7039c11d26d551ea052d56c3fb81b1ce5fe"
        },
        {
          "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/report.md",
          "sha256": "6fedb5a3ed3269f712b413a7c10f4793fd4978ffdec184376038e5444daba5ce"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "banded-gneiss-outcrop",
          "batch": 75,
          "revision": "r005",
          "candidate_root": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005",
          "source_commit": "074d56440818359bad76494599209e3f40a155cc",
          "reviewed_source_commit": "843e9b80d4aca535c5fe27ebc4c2e264fa9d77b3",
          "original_source_snapshot": "074d56440818359bad76494599209e3f40a155cc",
          "review_commit": "074d56440818359bad76494599209e3f40a155cc",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/banded-gneiss-outcrop/batch75-20261021/release-metadata.json",
            "sha256": "7400d93a1eaa4be0b1d41796afdfd0e3b553ad69b909a35b0dfcc6a83bae61c3"
          },
          "candidate": {
            "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/candidate.json",
            "sha256": "b3bc63971426ba5b5e1b0ce0401bda654e213f8ab28f7a347ee0c4a35b7644bf"
          },
          "active_candidate": {
            "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/candidate.json",
            "sha256": "b3bc63971426ba5b5e1b0ce0401bda654e213f8ab28f7a347ee0c4a35b7644bf"
          },
          "original_profile": {
            "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/profile-contract.json",
            "sha256": "25b3038f056573f9184170f8e97f1731b7c29952d8a4a0453f902c2838dc5700"
          },
          "active_profile": {
            "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/profile-contract.json",
            "sha256": "25b3038f056573f9184170f8e97f1731b7c29952d8a4a0453f902c2838dc5700"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/report.json",
            "sha256": "c08ea64d8ec925d82ed00fa22eeab7039c11d26d551ea052d56c3fb81b1ce5fe"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/report.json",
            "sha256": "c08ea64d8ec925d82ed00fa22eeab7039c11d26d551ea052d56c3fb81b1ce5fe"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/report.json",
              "sha256": "c08ea64d8ec925d82ed00fa22eeab7039c11d26d551ea052d56c3fb81b1ce5fe"
            },
            {
              "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/report.md",
              "sha256": "6fedb5a3ed3269f712b413a7c10f4793fd4978ffdec184376038e5444daba5ce"
            },
            {
              "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/raw-manifest.json",
              "sha256": "d93eae93fe41d02f6046d020c49e304383c573238c720ff0dc9bfdb9ad3b21a1"
            }
          ],
          "original_metrics": {
            "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/metrics.json",
            "sha256": "ff9bc44822cb3476dcfe813e1b56798f4ff0ef139861e5590be3355e8d638074"
          },
          "source_counts": {
            "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/source-vertex-counts.json",
            "sha256": "6ea9379955358a1582e512dd55d1146b5d6da47d44d80f0401560fd1f79d6c8c"
          },
          "proof": {
            "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/render-manifest.json",
            "sha256": "bdb8db50a21b6e06951cc287b13651f9ef940a2847b719b2b2c7888e37b84e38"
          },
          "source_preview": {
            "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/preview.png",
            "sha256": "92e7dd3a30f1c5260e06861b7b1f965ec860c1de555681b0f6097e79597a6a46"
          },
          "capture_reference": {
            "path": "assets/additions/banded-gneiss-outcrop/batch75-20261021/banded-gneiss-outcrop.png",
            "sha256": "e018282dc92452241057f37600bba13daf8e358ce5c237d840b2e8f6e062e318"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/banded-gneiss-outcrop.json",
            "sha256": "b4bba42cf37881a32f4636cf188b978f2eba51a5a5b0de3d61892ee4fddcefa9"
          }
        }
      ],
      "files": [
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/brief.md",
          "sha256": "f341f59433894a8751ea8ae82eb519247aeac28ab3fd2fa0abef3cf76ba860f3",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/build-config.json",
          "sha256": "085dcda659368124c22773bf015943e736d6176fc8e4f0fb8057c795b38f956b",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/build-dependencies.json",
          "sha256": "ee8634f08f8b17960f7802ee48fde966f58af7e7e93aafa58b6dc353d46f5cb4",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/candidate-brief.json",
          "sha256": "9fd4154834caab11f9275a4f55ec44aff0a61f0aba5857db8a7f006a0c8af63a",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/candidate.json",
          "sha256": "b3bc63971426ba5b5e1b0ce0401bda654e213f8ab28f7a347ee0c4a35b7644bf",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/concept-original.png",
          "sha256": "538d6d10f8adf6bb08abf436f8748e1c9b9be7b3228fb9c1bcd9c60ee1d17fd2",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/concept-prompt.txt",
          "sha256": "084da6769f354ac7ce54dc0cf1b2dff7311719995fe97375570b871da38bb304",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/contact-sheet.png",
          "sha256": "c27450192500354c995623b206ab514f53a0106513b3a1c53772a93ba1b40469",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/final-rebuild-binding.json",
          "sha256": "b7b08ea1ec8eccdf3eba6ebaf391a628251014b18eb43da0abf301bdcdb0c1cb",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/generator.py",
          "sha256": "f52c5c8ae017e6a3bca1d2cb1e1987742a4ca1a08b073b02127f595a97bea015",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/gltf-validator.report.json",
          "sha256": "9285602d593f3b4a80e64f8a390cc82e42948203bd3bfb0b2273492a12a428e7",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/lifecycle.jsonl",
          "sha256": "4f2c33cf1dc54e5c3daa37fed39a3290a2bbec98749903f692d1cc28a167abe0",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/maker-review.md",
          "sha256": "70844ff6b27824b3adc7bac2a60bc883a24c07061451b2f7b28dfb0dec291642",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/metrics.json",
          "sha256": "ff9bc44822cb3476dcfe813e1b56798f4ff0ef139861e5590be3355e8d638074",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/model.glb",
          "sha256": "c86d8b9ef0bda9b0cbd0bc9820fc7f11d561b619608e8a7e3dc676adf6524fad",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/modeling-freeze.json",
          "sha256": "e85f0a8a2728c85eb0815c3b32faa1336e8bbd92f37d125ed74a91e56baf7a33",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/physical-surfaces.report.json",
          "sha256": "2aeb085b82d88c14362b68eaf54828f1e172727a899ed961882df9fc8ba79a74",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/pixel-inspection.json",
          "sha256": "ca2836275d831edb877749daed2357911b29b03fbe944779672df9789bb7176e",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/preview.png",
          "sha256": "92e7dd3a30f1c5260e06861b7b1f965ec860c1de555681b0f6097e79597a6a46",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/profile-contract.json",
          "sha256": "25b3038f056573f9184170f8e97f1731b7c29952d8a4a0453f902c2838dc5700",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/clay.png",
          "sha256": "a431b0e65c35978d5afe7689294450b7966a378a72fe633044fe43f9ee08d7ba",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/front.png",
          "sha256": "f7ce770158f62be23fbacf0f02e6c15b301f9787e786385d3b87acd5bc5e7fc4",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/hero.png",
          "sha256": "92e7dd3a30f1c5260e06861b7b1f965ec860c1de555681b0f6097e79597a6a46",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/rear.png",
          "sha256": "140e15fc5375c8a15d66fee9a972f58ead1963d36526d284cb68828b164ef609",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/render-manifest.json",
          "sha256": "bdb8db50a21b6e06951cc287b13651f9ef940a2847b719b2b2c7888e37b84e38",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/reversehero.png",
          "sha256": "b84e5aa89887b72fb01979f138a1fc5be600e5319411ca9ce9685d29f75dc953",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/side.png",
          "sha256": "813bd21ad94257ad154fb2dd41862453697d8a08a1c91ea6501bc6d58d93ee48",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/silhouette.png",
          "sha256": "0c1912c47c5c3f679e9a8973d99415526d19363c1269e28cc36e327c509e25e5",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/proof-final/top.png",
          "sha256": "b776473766ff7ff938d41ca8c9acd23ccb740c63beaf9b8ed83163485dbba7b6",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/references.json",
          "sha256": "78f10b3b6b804298a0b2b70ba1543ce6e3f053867672f784f4789df077da9a16",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/repair-freeze.json",
          "sha256": "e85f0a8a2728c85eb0815c3b32faa1336e8bbd92f37d125ed74a91e56baf7a33",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/repro-final-1.report.json",
          "sha256": "64036c837d974805042d51216114bd2636b003a7f562d51aa529805eaee2d391",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/repro-final-2.report.json",
          "sha256": "b2cf5488826d1501bde66e532cd2448e78d992b8651d7feb204ec243b1ff1b82",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/runtime-parse.report.json",
          "sha256": "eb32bcc0d3512b4175b26f8e348c909f833db57c5f4601c9280883c8bae84684",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/source-final.report.json",
          "sha256": "93a7cdfa8e4817a0f6e990941e55147bec49dab1aceeb60bce86344e095b7312",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/source-metrics.json",
          "sha256": "05641523e757f495145763b9c0dcd0f9b9ef1cefc913fca8fbc88e6f4201a42f",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/source-vertex-counts.json",
          "sha256": "6ea9379955358a1582e512dd55d1146b5d6da47d44d80f0401560fd1f79d6c8c",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/assets/banded-gneiss-outcrop/r005/source.blend",
          "sha256": "ceaa997a9bc93ff9120f4183e8a83f39da1cceb303847f78e151cdad9023a740",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "production/continuous-small-life-round30-20261020/work/batch-75/repair-gneiss-r005/publication-policy-reference.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256",
          "origin": "source",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/raw-manifest.json",
          "sha256": "d93eae93fe41d02f6046d020c49e304383c573238c720ff0dc9bfdb9ad3b21a1",
          "origin": "review",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/report.json",
          "sha256": "c08ea64d8ec925d82ed00fa22eeab7039c11d26d551ea052d56c3fb81b1ce5fe",
          "origin": "review",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "qa/continuous-small-life-round30-20261020/batch-75/diff-gneiss-r005/report.md",
          "sha256": "6fedb5a3ed3269f712b413a7c10f4793fd4978ffdec184376038e5444daba5ce",
          "origin": "review",
          "owner": "banded-gneiss-outcrop"
        },
        {
          "path": "qa/next52-g02-release-20261021/process-archive-index.json",
          "sha256": "881bef2fd3e77de00cb3d4d69aef854f85692076cecf670976ab51121da111e7",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g03-20261021.json",
      "sha256": "baa57525a28084cf6b9bd2a0fb31dca91e77c039ac4d29a2d60d4db640c8d2d7"
    },
    "release": {
      "version": 1,
      "scope": "next52-g03-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "284d9a257a4d4a866d272d2b490cfab01c61d8f0",
      "review_commit": "bc53aa6cda153da6ca84b7949753291ecf10febf",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g03-release-20261021/source-bundle.json",
        "sha256": "01f7ea23cad1abad4ee2ba1f9f504db3ab924bd833091aa620725c1f77687f5c"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
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
          "path": "scripts/rebuild_frozen_blender.py",
          "sha256": "c5971fab63b69fa3720d52b9884789eb56f6c2b1d2db4d6c9d3fa2bc77a59db6"
        },
        {
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/handoff.json",
          "sha256": "f0e7f320d505d89fc3b0059a2cedeaf39c121574b6758749de731476e71a9562"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
          "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/own-evidence-manifest.json",
          "sha256": "069eefa60e830d1bc5c3b01f5dd7f5cd5f6783c80a3e89dfb442f9c7f8f3ea74"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "cloudina",
          "batch": 83,
          "revision": "r002",
          "candidate_root": "production/small-life-batch83/assets/cloudina/r002",
          "source_commit": "284d9a257a4d4a866d272d2b490cfab01c61d8f0",
          "reviewed_source_commit": "1e0664988dfd77ec163bee527f11fc482668fddd",
          "original_source_snapshot": "bc53aa6cda153da6ca84b7949753291ecf10febf",
          "review_commit": "bc53aa6cda153da6ca84b7949753291ecf10febf",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/cloudina/batch83-20261021/release-metadata.json",
            "sha256": "5c4734932277b82333a92b678ad1b7e3822d15659deebfb41a302f9c7bb0138b"
          },
          "candidate": {
            "path": "production/small-life-batch83/assets/cloudina/r002/candidate.json",
            "sha256": "add0bfee0576c9c3429356e8c4e8c3c6471a6f7fa11e1d43953740fbe6870ed9"
          },
          "active_candidate": {
            "path": "production/small-life-batch83/assets/cloudina/r002/candidate.json",
            "sha256": "add0bfee0576c9c3429356e8c4e8c3c6471a6f7fa11e1d43953740fbe6870ed9"
          },
          "original_profile": {
            "path": "production/small-life-batch83/assets/cloudina/r002/profile-contract.json",
            "sha256": "5dda21fbe3c8b9117ff1da38e1e2459d76ffccdb024a41d196738ef601db1e52"
          },
          "active_profile": {
            "path": "production/small-life-batch83/assets/cloudina/r002/profile-contract.json",
            "sha256": "5dda21fbe3c8b9117ff1da38e1e2459d76ffccdb024a41d196738ef601db1e52"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
            "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
            "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
              "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-83/own-evidence-manifest.json",
              "sha256": "069eefa60e830d1bc5c3b01f5dd7f5cd5f6783c80a3e89dfb442f9c7f8f3ea74"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-83/handoff.json",
              "sha256": "f0e7f320d505d89fc3b0059a2cedeaf39c121574b6758749de731476e71a9562"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch83/assets/cloudina/r002/metrics.json",
            "sha256": "61d52b3f821cbddf7404aad9025d1e084837e385c0ccc0dc10d25e0da497b028"
          },
          "source_counts": {
            "path": "production/small-life-batch83/assets/cloudina/r002/source-vertex-counts.json",
            "sha256": "603b9af1e75e76a729fdfb038d9ce29553d9f487deb164d08c2451ba189b907f"
          },
          "proof": {
            "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/render-manifest.json",
            "sha256": "be5dda5330ba02ac2e73b5515afc85c93bcfc00ce21811eb63bb0f96cca6b3a1"
          },
          "source_preview": {
            "path": "production/small-life-batch83/assets/cloudina/r002/preview.png",
            "sha256": "cf83d3a0918c9a595b2512056cfefb558c10a9a2fca1304f90d2c0132bbe0670"
          },
          "capture_reference": {
            "path": "assets/additions/cloudina/batch83-20261021/cloudina.png",
            "sha256": "7705da6b481167823161d0bc02955cd2b1c358a37dcf336ea2055910cf6788ff"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/cloudina.json",
            "sha256": "734a649761fb29c4212f66ed7774c6ca690e881833d4ec3160e774f9de08257d"
          }
        },
        {
          "id": "impact-crater",
          "batch": 83,
          "revision": "r002",
          "candidate_root": "production/small-life-batch83/assets/impact-crater/r002",
          "source_commit": "284d9a257a4d4a866d272d2b490cfab01c61d8f0",
          "reviewed_source_commit": "1e0664988dfd77ec163bee527f11fc482668fddd",
          "original_source_snapshot": "bc53aa6cda153da6ca84b7949753291ecf10febf",
          "review_commit": "bc53aa6cda153da6ca84b7949753291ecf10febf",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/impact-crater/batch83-20261021/release-metadata.json",
            "sha256": "b25f6e6c91fece4c23437475f5a293515d38ea5c6a2dbe1ea9c0ed62bd267c0b"
          },
          "candidate": {
            "path": "production/small-life-batch83/assets/impact-crater/r002/candidate.json",
            "sha256": "7acd6245a8c850b089ea5c366eec02c93d14a0f79ee709d83a1c45bf0322e2ab"
          },
          "active_candidate": {
            "path": "production/small-life-batch83/assets/impact-crater/r002/candidate.json",
            "sha256": "7acd6245a8c850b089ea5c366eec02c93d14a0f79ee709d83a1c45bf0322e2ab"
          },
          "original_profile": {
            "path": "production/small-life-batch83/assets/impact-crater/r002/profile-contract.json",
            "sha256": "d356962e4a25d440e7256df30b44dd008c18266b02d00286dfb14b17146a0e6b"
          },
          "active_profile": {
            "path": "production/small-life-batch83/assets/impact-crater/r002/profile-contract.json",
            "sha256": "d356962e4a25d440e7256df30b44dd008c18266b02d00286dfb14b17146a0e6b"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
            "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
            "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
              "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-83/own-evidence-manifest.json",
              "sha256": "069eefa60e830d1bc5c3b01f5dd7f5cd5f6783c80a3e89dfb442f9c7f8f3ea74"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-83/handoff.json",
              "sha256": "f0e7f320d505d89fc3b0059a2cedeaf39c121574b6758749de731476e71a9562"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch83/assets/impact-crater/r002/metrics.json",
            "sha256": "3b199ba7793a631a6abb9caddf80974ef56e709f7179ae572466127362a093ab"
          },
          "source_counts": {
            "path": "production/small-life-batch83/assets/impact-crater/r002/source-vertex-counts.json",
            "sha256": "a7863ac74c3cdb39fce3de84d3cfe6637adec286157b1f32ff26dab2c519ae0a"
          },
          "proof": {
            "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/render-manifest.json",
            "sha256": "e8c4dade98c5d0158cf21702063aa54090c4229ef91635e4161fd36f04f55457"
          },
          "source_preview": {
            "path": "production/small-life-batch83/assets/impact-crater/r002/preview.png",
            "sha256": "7652fe19effd074a7295a3d9568417f7400b52d64049f6aca2951070eda7e50e"
          },
          "capture_reference": {
            "path": "assets/additions/impact-crater/batch83-20261021/impact-crater.png",
            "sha256": "e9d050748eed27a066a022a2cd2b72b4b9e6e23cca309c11517ccf243c95cf26"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/impact-crater.json",
            "sha256": "7c31c281499686394d0a368b1fff990228b5e322d38902a9c9a6dfafbb0f9075"
          }
        },
        {
          "id": "lava-tube-entrance",
          "batch": 83,
          "revision": "r003",
          "candidate_root": "production/small-life-batch83/assets/lava-tube-entrance/r003",
          "source_commit": "284d9a257a4d4a866d272d2b490cfab01c61d8f0",
          "reviewed_source_commit": "1e0664988dfd77ec163bee527f11fc482668fddd",
          "original_source_snapshot": "bc53aa6cda153da6ca84b7949753291ecf10febf",
          "review_commit": "bc53aa6cda153da6ca84b7949753291ecf10febf",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/lava-tube-entrance/batch83-20261021/release-metadata.json",
            "sha256": "87668fdb613b78bc15b2d5183cbc731fc5fef44cd4e52b227bf4a10ef9423c14"
          },
          "candidate": {
            "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/candidate.json",
            "sha256": "9d408a49d59f9a5e4eeea7c817fc5fb10c8e8973d9a57d35b2ad96652a3f208e"
          },
          "active_candidate": {
            "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/candidate.json",
            "sha256": "9d408a49d59f9a5e4eeea7c817fc5fb10c8e8973d9a57d35b2ad96652a3f208e"
          },
          "original_profile": {
            "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/profile-contract.json",
            "sha256": "54b4c8024cae88e204e366628abff943b9ccdda2ab7e69da414fac0a855c842e"
          },
          "active_profile": {
            "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/profile-contract.json",
            "sha256": "54b4c8024cae88e204e366628abff943b9ccdda2ab7e69da414fac0a855c842e"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
            "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
            "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
              "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-83/own-evidence-manifest.json",
              "sha256": "069eefa60e830d1bc5c3b01f5dd7f5cd5f6783c80a3e89dfb442f9c7f8f3ea74"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-83/handoff.json",
              "sha256": "f0e7f320d505d89fc3b0059a2cedeaf39c121574b6758749de731476e71a9562"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/metrics.json",
            "sha256": "4de5987efa6d890371fb92257bbeb6c86617e146f412996a98405615483fc320"
          },
          "source_counts": {
            "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/source-vertex-counts.json",
            "sha256": "c5b108c09ea64442246b091c56f5ca13332edfbcf7064c047d5a94d2f78c3240"
          },
          "proof": {
            "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/render-manifest.json",
            "sha256": "a466eb5d4271a7e535c268db3bc4096b17b60cb176d468e404cc791d05870b16"
          },
          "source_preview": {
            "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/preview.png",
            "sha256": "ada2caeb754c82b8deed5b806b9e6acd78461373f66f7cc8982a8cbe72b28223"
          },
          "capture_reference": {
            "path": "assets/additions/lava-tube-entrance/batch83-20261021/lava-tube-entrance.png",
            "sha256": "922b8319958b18043db4f64f139e02a71b53a6f83edf68d8648b716a29236c8f"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/lava-tube-entrance.json",
            "sha256": "b3b4c20108160ff1f3c553ae9e3d0bf097503475b3a5b7389e60de056813a656"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/brief.md",
          "sha256": "f8bad3b15e23c3573285b6c7921fc115c2aef9cdf65f0b8bba1561b651bf0b95",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/build-config.json",
          "sha256": "03cef2c473276aef649139642bb5b32e12b8c1c317e8efbcb0a5e92507098f3a",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/build-dependencies.json",
          "sha256": "be9acd048ca43d856513c88610ab6684c26106b472600c0812076cd5d7e1e01d",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/candidate-brief.json",
          "sha256": "d14a6aac4c61e59aa064ab25f79a18028f9041e6fd2c509ce9fdb8f74eaec701",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/candidate.json",
          "sha256": "add0bfee0576c9c3429356e8c4e8c3c6471a6f7fa11e1d43953740fbe6870ed9",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/concept-original.png",
          "sha256": "512135561cecd01d6e13d07861a969d0661d8a1b25c2b18596a89b3a6af4548f",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/concept-prompt.txt",
          "sha256": "62e19fceb7125edc0a4370b34385ce257088c28c35f23bc9fc43d09a0f6d3d94",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/contact-sheet.png",
          "sha256": "c2e631b68a469da15720f3b2e67d3e826c5bdb35c9eade53fe5236e2656bacc4",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/final-rebuild-binding.json",
          "sha256": "59f209d26e96160de249fac09c5b93a407cd5dbba4c7ae7accff08c27ede1677",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/generator.py",
          "sha256": "e4fb6c38ddb9499cb23070dfac0583eda37188daf37b7cc98a032cf9de92a4f4",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/gltf-validator.report.json",
          "sha256": "c1b350747b208ca586b7d67da27249ae5c64b672448e4f7f6f082b33a6d8dadd",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/lifecycle.jsonl",
          "sha256": "2a8a036e3b5fb83a020945dc90dab690ab7dbbe8f87be8d4c0b59b862ce86d1b",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/maker-review.md",
          "sha256": "65900962951c93697667bfe8f1684b9a38ecfe3c30c8df9eac0678e067d2e3af",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/metrics.json",
          "sha256": "61d52b3f821cbddf7404aad9025d1e084837e385c0ccc0dc10d25e0da497b028",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/model.glb",
          "sha256": "eae46d63f9c74f3a53bd2862ad94a57d7302e5806c06432be9d996107dd7c805",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/modeling-freeze.json",
          "sha256": "f2d7b820e7383e365bcb0bd27afe839f17080ce6a383d6cbf6973d338857912a",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/physical-surfaces.report.json",
          "sha256": "5e6a90c6fd0391ae142cf1a4b97608f0d8ce0a9b6750731459ba46023d807903",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/pixel-inspection.json",
          "sha256": "68dd63bc3d1698d2bd6b602f24c93c5b383b67c0936b85859b2f22aaa42bf907",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/preview.png",
          "sha256": "cf83d3a0918c9a595b2512056cfefb558c10a9a2fca1304f90d2c0132bbe0670",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/profile-contract.json",
          "sha256": "5dda21fbe3c8b9117ff1da38e1e2459d76ffccdb024a41d196738ef601db1e52",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/clay.png",
          "sha256": "2e0a3d78e1009de6483f209a0a92e1bb4e0df002a5fd32e08de8603227dadfb4",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/front.png",
          "sha256": "d90d16740b3a0d470f3cd7532cfd355b2180e15afdca85d057c541c5be07f4d8",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/hero.png",
          "sha256": "cf83d3a0918c9a595b2512056cfefb558c10a9a2fca1304f90d2c0132bbe0670",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/rear.png",
          "sha256": "9ce8d0adf1534f56f352f5f3e2adde7def75b5f3a10a2e40e97dfc666979018f",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/render-manifest.json",
          "sha256": "be5dda5330ba02ac2e73b5515afc85c93bcfc00ce21811eb63bb0f96cca6b3a1",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/reversehero.png",
          "sha256": "3b28fa50e1dcca72d44dca49b8cf9152e169ccdb16fca0dd16e763297459d8a0",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/side.png",
          "sha256": "5afd9697c75b461cfe567c22cc9cc336212799a605b913303a0b5d690a3da1ce",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/silhouette.png",
          "sha256": "25ebb48247416a56d9d87e16f7c853869a13d5f5574ee42adb3d1f23fb60417a",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/proof-final/top.png",
          "sha256": "734a0a0d865c773ffe5a45d6c591fe7a194d93a15e0ef8ab5212680498428a12",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/references.json",
          "sha256": "1b85b9166da4d9b543764af9c00d70bf915080c6e0d54d522ee9192d37b6f7b7",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/repair-freeze.json",
          "sha256": "ca9a0e2fd5c63672acf02c05e290ae8b504f8074cdbbf291e499f4d09e23e4ac",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/repro-final-1.report.json",
          "sha256": "2ad51ba15bf7a04eb773f371398a49db0aeb318652fa3523a765040241d40c77",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/repro-final-2.report.json",
          "sha256": "33854538e906d082c2d4c942a7628cedffcebeeee1a0230ee7a5428c4e53c55f",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/runtime-parse.report.json",
          "sha256": "51b82aed6e156c2c9df6d5faf535a555aa4ac3ac10ef903b0c633dbe3d6b95c1",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/source-final.report.json",
          "sha256": "18d840c8f6c705fd20c4ceaa79c9389ebc9aa5d3e05ac9cc3c6d520d503f2722",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/source-metrics.json",
          "sha256": "0d18ba8513afdb4ee434d35c07efff774612941142f814072588c43c54870f50",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/source-vertex-counts.json",
          "sha256": "603b9af1e75e76a729fdfb038d9ce29553d9f487deb164d08c2451ba189b907f",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/cloudina/r002/source.blend",
          "sha256": "3517d02ce1b0d9e63825300e25f8cf13154add51d042055411beab7c87ea1d60",
          "origin": "source",
          "owner": "cloudina"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/brief.md",
          "sha256": "fbfe8b1574c0320d6ac1198fc4032946032d147aa2233a1f89ea54cfd0492d2b",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/build-config.json",
          "sha256": "ddd64c66f5964a14e25b4c235514ddc39199beb4fb96fa3d361023452e80ffb7",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/build-dependencies.json",
          "sha256": "b7b43289ac05d4d95247bab8c8ccbf3c63e373e27dc0bcc7d022aa8226c17871",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/candidate-brief.json",
          "sha256": "d206de0e81efb51f06985e16a15858ff79661be283626337ba7da97ad6c7e1ac",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/candidate.json",
          "sha256": "7acd6245a8c850b089ea5c366eec02c93d14a0f79ee709d83a1c45bf0322e2ab",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/concept-original.png",
          "sha256": "3289c02bdfdf26cbb71f92ef38386ca0a133c4c4032496e028a484b3c17d2883",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/concept-prompt.txt",
          "sha256": "b183af5a2856514435ab35f3867e5d0fd07e1d0a9ec06ab9268e5916519dbfdf",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/contact-sheet.png",
          "sha256": "5dbcc3e20bc4f3553ab94f4a2780f03e67986c3921825cb1817a1bd47f2d2112",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/final-rebuild-binding.json",
          "sha256": "7d81f345de07419186e1708c5ef02a64570422ca5cb707fe460bc6d0f6b34087",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/generator.py",
          "sha256": "e4fb6c38ddb9499cb23070dfac0583eda37188daf37b7cc98a032cf9de92a4f4",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/gltf-validator.report.json",
          "sha256": "de60fd91f84a7b89c04e3da499dc001fc19ebb999f222b5f4cd40806d3464de0",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/lifecycle.jsonl",
          "sha256": "44fb8c96fc5ee63d8836f934a37a220627e7bff47a713aa9b530f248702987ab",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/maker-review.md",
          "sha256": "ab4880e3d071eaef3b4f3cec771bb254a58625d2e45ee9f2e5c66df3483a00e9",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/metrics.json",
          "sha256": "3b199ba7793a631a6abb9caddf80974ef56e709f7179ae572466127362a093ab",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/model.glb",
          "sha256": "cfd50732977a30859163cfee30ce7190324830c07500a26ce63aeaa47a67cd43",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/modeling-freeze.json",
          "sha256": "9ded3f985a4681c21b63a857b2be032fc1f799dbddf58526b7bd8ef493a19994",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/physical-surfaces.report.json",
          "sha256": "793a74db692f49e1d5f40ab13070d6778c2d690d4f342347d886e45bf5cbcf99",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/pixel-inspection.json",
          "sha256": "3afeecd8188dcd1421ba9ece31a6442ef3ba5e4be289e4ec978c2531adc94f00",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/preview.png",
          "sha256": "7652fe19effd074a7295a3d9568417f7400b52d64049f6aca2951070eda7e50e",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/profile-contract.json",
          "sha256": "d356962e4a25d440e7256df30b44dd008c18266b02d00286dfb14b17146a0e6b",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/clay.png",
          "sha256": "bb5e4966ee0fc8b2dcdbdcd3308d7a123107960c9e80e51dc1501ad71e1ad0e4",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/front.png",
          "sha256": "03e59d822e875c9f2c243bb241b883d57d6c8c93647b0fe1b1b8c40e3eb862dc",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/hero.png",
          "sha256": "7652fe19effd074a7295a3d9568417f7400b52d64049f6aca2951070eda7e50e",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/rear.png",
          "sha256": "3b326af425ee9420aa121c40cc9b4132bb5dc3ad36d30346ffe9e720a0f69e44",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/render-manifest.json",
          "sha256": "e8c4dade98c5d0158cf21702063aa54090c4229ef91635e4161fd36f04f55457",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/reversehero.png",
          "sha256": "013436959041f9a1422cdc10f9fabe165e98e5f1306391b0893ff7dcb90bc10e",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/side.png",
          "sha256": "31479a09e71f6c17d2720da8e6497f804d3241cadc9f380fbc4ffb258da3e44d",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/silhouette.png",
          "sha256": "b732aebf320dd8ccd02f18f7aa94bae82ac044b7e766a5f22aa6197143226bee",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/proof-final/top.png",
          "sha256": "8618fad29df927cda2d03d0f65c5548e69b9b2f11a7b0b0ac290298f7c9d0346",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/references.json",
          "sha256": "207e60ddde923d2b4701e0dbfe988769a286311129922d1c6ca3d2668d70ba64",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/repair-freeze.json",
          "sha256": "733f35436e20a67d00343743e62181f57c5ce22759160360e1d76b13eb396849",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/repro-final-1.report.json",
          "sha256": "07c668693c31f002e54941313c2aa7be660fb26f2477d10d762600102d571423",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/repro-final-2.report.json",
          "sha256": "67f76fc13ff5966e31993144149bc902b24811d6a0a182410a108ae4190fbf52",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/runtime-parse.report.json",
          "sha256": "b8261e0ac9d47034803893798d4cd423ec9a455e7687a5f30eac361deab7d4b4",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/source-final.report.json",
          "sha256": "e0fd5f999c93ff91bc8f83d27c0fa08fbf5cc036b6507b81a0269f348ab28423",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/source-metrics.json",
          "sha256": "017b72ac24fde59e7c1c94c03852ce6758a4353a3380db1d8c9ccb37bb30b6d7",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/source-vertex-counts.json",
          "sha256": "a7863ac74c3cdb39fce3de84d3cfe6637adec286157b1f32ff26dab2c519ae0a",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/impact-crater/r002/source.blend",
          "sha256": "eea31ceef4f9fc84b0cfd79b5b5927e3b321c469d52495f726a1e3236db07c25",
          "origin": "source",
          "owner": "impact-crater"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/brief.md",
          "sha256": "5578326bfb042b7f01400bf5109ba5fa41441a4cf328738c2da80ede0f330935",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/build-config.json",
          "sha256": "005c66b7f57787d856fc25480a664fde79850e9e35e246fc7c5c077047c2df51",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/build-dependencies.json",
          "sha256": "7f8864279e0f4612ee8cf382793c70eba7271561c611a7da89ad2507230d444a",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/candidate-brief.json",
          "sha256": "e69bebb5da55886b1fe3225f0b19c91d9fa68da9b9356dd1b8e46c0b2845198d",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/candidate.json",
          "sha256": "9d408a49d59f9a5e4eeea7c817fc5fb10c8e8973d9a57d35b2ad96652a3f208e",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/concept-original.png",
          "sha256": "7ddc1866e71c3e56bc4a8093615c29d953d6cfa235d7c801127c8c7de7d320bb",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/concept-prompt.txt",
          "sha256": "61f0adf3e35d44c518dde840e7f0426db9a245e38af0e7528089750483273e04",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/contact-sheet.png",
          "sha256": "8514445d0a017a8dbfad8203dc0dc50b5cf3341036fcc577a31923d60244bc37",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/final-rebuild-binding.json",
          "sha256": "981df8903f9d91cbe8abae2c448032ebf79bb0aa3be8f5c4721996e816e7976b",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/generator.py",
          "sha256": "556a3d7cf2d564085874f021de56c299be923255bb4a15baa046a2bc87023c69",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/gltf-validator.report.json",
          "sha256": "8db4da4de43172cb58b47e0e4976d3709308bf9a7247c7fba76e485db7752a5c",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/lifecycle.jsonl",
          "sha256": "3e751b6209cf60e7d307ba15c73967ff730443ec98890d5a5e148c8f525df76c",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/maker-review.md",
          "sha256": "68b9ca0a8ba23c3c2c58c77474c49a0fd28c2f2bba2711b42a198e9476fda0aa",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/metrics.json",
          "sha256": "4de5987efa6d890371fb92257bbeb6c86617e146f412996a98405615483fc320",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/model.glb",
          "sha256": "b7022acdc470a85c3ff76fa13025e3a95e75ac6fe7a5b9b6a3ee2d98c3789f00",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/modeling-freeze.json",
          "sha256": "5bc7f52fa211273e831e2c862e800f471c2706c8457aebdd6903e7abd4c3ad2e",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/physical-surfaces.report.json",
          "sha256": "2511a090e695044dc10c32ba88591ed88a10da8284f233a89c4cd057491a371a",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/pixel-inspection.json",
          "sha256": "8d284dfc1061b93bd838d4c24e657e517aa6b34172cf29cad99db737387d76b4",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/preview.png",
          "sha256": "ada2caeb754c82b8deed5b806b9e6acd78461373f66f7cc8982a8cbe72b28223",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/profile-contract.json",
          "sha256": "54b4c8024cae88e204e366628abff943b9ccdda2ab7e69da414fac0a855c842e",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/clay.png",
          "sha256": "9c6b9733162d9d1437ffdb855b9d5f546b9619eaeeccde24f30083f06612cd2e",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/front.png",
          "sha256": "17e0de6eeedec3debb080e0d96a53167a27ec5f0523dfa3cafb58420dbe32ad7",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/hero.png",
          "sha256": "ada2caeb754c82b8deed5b806b9e6acd78461373f66f7cc8982a8cbe72b28223",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/rear.png",
          "sha256": "0325b1e4e43cf0fbb7b18eddbf1ce0274fa95b137af582e524ef147c5844c694",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/render-manifest.json",
          "sha256": "a466eb5d4271a7e535c268db3bc4096b17b60cb176d468e404cc791d05870b16",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/reversehero.png",
          "sha256": "aa217a4e15b206eabb97921eb83da1aa1ec505b22e26d36e1e3c21ee99f17dc2",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/side.png",
          "sha256": "ec83f608e474a9beb6d49e996f355e92af59d5d3f59aff51ae4d25685f21fde9",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/silhouette.png",
          "sha256": "c3f34842e35fb4bf7f7111e34664ede5d3e18a2501d271e0af0b57110bf1f36a",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/proof-final/top.png",
          "sha256": "04c534a6e2117e710d45cd3b57d44361a272df1be19a8fce65263f529be6cc1c",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/references.json",
          "sha256": "4387992e9081824da43f6c2674925ccddb1a52f2df9b99a74a7ddadfbf018470",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/repair-freeze.json",
          "sha256": "1d580453e29b3967997ade1aa2c54afe2f4f8df0db4085492880190b3e2147c8",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/repro-final-1.report.json",
          "sha256": "26e4b61a717fe6c40bd4f0891f10c25f130832a099d7aa821a2c9595fef57491",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/repro-final-2.report.json",
          "sha256": "79ff404a7ea3805fdd2c530b1f2a918d52beea6ec291137a8aa1294ed6afc996",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/runtime-parse.report.json",
          "sha256": "ec1fb6350864eca6c8a75f03830086a44c079aafaebcdd121fc962d3cdd20337",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/source-final.report.json",
          "sha256": "b49523b5cc538c19bb29965723ce1a4c4039e6ccb68f79235fa1d51170d9d4f8",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/source-metrics.json",
          "sha256": "18203554c593d62e1c57cbac0303ddd0e0fb8db91b2161c0c9d119d8e1940639",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/source-vertex-counts.json",
          "sha256": "c5b108c09ea64442246b091c56f5ca13332edfbcf7064c047d5a94d2f78c3240",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/assets/lava-tube-entrance/r003/source.blend",
          "sha256": "784c0805c89ad662a2b620fcb7350bf917801ed44cf7b5609d548228395d2410",
          "origin": "source",
          "owner": "lava-tube-entrance"
        },
        {
          "path": "production/small-life-batch83/check-physical-surfaces.py",
          "sha256": "fa7f23300e880099e604a52509cbbf86e1aab6d12460cd058f28282f2de1991b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch83/publication-policy-reference.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch83/render-fixed8.py",
          "sha256": "d598261c79abf7ac7f2f8d1c1813b689ebc831f3e7c7b373442272a028c77858",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch83/runtime-parse.mjs",
          "sha256": "fb938eb6db606a51b904de3f58b2557b618fc5963bfcf225ad990b0b1244164c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/REPORT.md",
          "sha256": "152ac68c22aed8a324adfaf9d753eac474df07b3931f4147b70e5a8182b92771",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/analyze_delta_channel.py",
          "sha256": "abc8fd16d8f93a7b5585d2b750a904579b08f7a2eda12a2c5a27d7100b74009b",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/audit_inputs.py",
          "sha256": "8502715c937205c7bd39b6946b469a23a6b5d2d7020e9fc4c1994b778258c585",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/finalize_report.py",
          "sha256": "a999878f5654ad0d339929897587c5e1cc794c24081e1e80e42f1f5c613d9db7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/handoff.json",
          "sha256": "f0e7f320d505d89fc3b0059a2cedeaf39c121574b6758749de731476e71a9562",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/independent-qa.report.json",
          "sha256": "430f33b1f5be66a9c7a5bab0713ce341b149ccc655806a9a530b4976fbc2092b",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/own-evidence-manifest.json",
          "sha256": "069eefa60e830d1bc5c3b01f5dd7f5cd5f6783c80a3e89dfb442f9c7f8f3ea74",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/render_delta_diagnostic.py",
          "sha256": "0988d24746a3e760554504afe9c193ba9e87f0efc7535ca6cb127052e9e7fb8b",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/run_fresh_checks.py",
          "sha256": "2103fb4e3b8689684905c381ce82dc08fa6dc5489d008ef33e58abda74aef3c0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/runtime_checks.mjs",
          "sha256": "16b66a1a6d19c8fa773278fdf784a2837e6d3ff42af2d13b425dd6532f100059",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-83/source_reexport.py",
          "sha256": "7b05a23975f06492ea121238555f820fe2c31f3a0c75636c57d3f926b0750f2f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g03-release-20261021/process-archive-index.json",
          "sha256": "38c852feae60c6f547e2ee695b80c0801270a8afbc857bb88c6517e7bd62d1b9",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g04-20261021.json",
      "sha256": "eea6494f3f012b4c160362a17ead37302eb4384a3a43f3530dc3be5aebbfcb11"
    },
    "release": {
      "version": 1,
      "scope": "next52-g04-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "44da0b1831c97ea45f2f68b46c3a119dc168befd",
      "review_commit": "44da0b1831c97ea45f2f68b46c3a119dc168befd",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g04-release-20261021/source-bundle.json",
        "sha256": "599842187b40fe4ace201c3b2aebfe0be1b66a0cf5186bc9b38b3dcd328ffc20"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
        },
        {
          "path": "scripts/qa_glb.py",
          "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/handoff.json",
          "sha256": "21aa5cfe573a7b1b2287cfb55c8da88017c624bb07eceb7cf1be1ed31dd704a8"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/ownmanifest.json",
          "sha256": "3c4ecfb9714d8aa8327d2f02e1c93941f04f6848bb7acc4d09e10ea32778bfce"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/report.json",
          "sha256": "3eeaaa1ab379fd8765ca6cce973f061b77ff72be6b4bbef0f6b5958bab530be0"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "chondrites-branching-trace",
          "batch": 88,
          "revision": "r002",
          "candidate_root": "production/batch88/assets/chondrites-branching-trace/r002",
          "source_commit": "44da0b1831c97ea45f2f68b46c3a119dc168befd",
          "reviewed_source_commit": "b7c7f1c9ec495ad528568770a789b5d15a2de3a4",
          "original_source_snapshot": "44da0b1831c97ea45f2f68b46c3a119dc168befd",
          "review_commit": "44da0b1831c97ea45f2f68b46c3a119dc168befd",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/chondrites-branching-trace/batch88-20261021/release-metadata.json",
            "sha256": "e1fe1825afba1ab1c69ffdd2f213ad619aee6bf994483047c39c33359ae91c17"
          },
          "candidate": {
            "path": "production/batch88/assets/chondrites-branching-trace/r002/candidate.json",
            "sha256": "e4ebe9a5866bcd0ecf0c29fa7b510366ac5c18590cfd845dceaf297cd518adb7"
          },
          "active_candidate": {
            "path": "production/batch88/assets/chondrites-branching-trace/r002/candidate.json",
            "sha256": "e4ebe9a5866bcd0ecf0c29fa7b510366ac5c18590cfd845dceaf297cd518adb7"
          },
          "original_profile": {
            "path": "production/batch88/assets/chondrites-branching-trace/r002/profile-contract.json",
            "sha256": "9b0ba5804e961148b4c848b07fa4b12d82fa988f31832bf4a815d704b239278f"
          },
          "active_profile": {
            "path": "production/batch88/assets/chondrites-branching-trace/r002/profile-contract.json",
            "sha256": "9b0ba5804e961148b4c848b07fa4b12d82fa988f31832bf4a815d704b239278f"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-88/report.json",
            "sha256": "3eeaaa1ab379fd8765ca6cce973f061b77ff72be6b4bbef0f6b5958bab530be0"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-88/report.json",
            "sha256": "3eeaaa1ab379fd8765ca6cce973f061b77ff72be6b4bbef0f6b5958bab530be0"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-88/report.json",
              "sha256": "3eeaaa1ab379fd8765ca6cce973f061b77ff72be6b4bbef0f6b5958bab530be0"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-88/ownmanifest.json",
              "sha256": "3c4ecfb9714d8aa8327d2f02e1c93941f04f6848bb7acc4d09e10ea32778bfce"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-88/handoff.json",
              "sha256": "21aa5cfe573a7b1b2287cfb55c8da88017c624bb07eceb7cf1be1ed31dd704a8"
            }
          ],
          "original_metrics": {
            "path": "production/batch88/assets/chondrites-branching-trace/r002/metrics.json",
            "sha256": "9b28fcd56257e62298a90dbcf887030e9696f15a00e8cb242e7c4cb1138daf0e"
          },
          "source_counts": {
            "path": "production/batch88/assets/chondrites-branching-trace/r002/source-vertex-counts.json",
            "sha256": "b425d7eb799aa5a94320400a7e8da43a7c20dbd8ce48e68e0a30a844adb5a8eb"
          },
          "proof": {
            "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/render-manifest.json",
            "sha256": "dfbf0e99d420dc07c63be0deb0d01c29a36320f8657ae8edbd90e98bc0757536"
          },
          "source_preview": {
            "path": "production/batch88/assets/chondrites-branching-trace/r002/preview.png",
            "sha256": "fcd6c676cf5e4ef25cff5ac0880fb6ae19eae6997d39a175da0fb3954bf22543"
          },
          "capture_reference": {
            "path": "assets/additions/chondrites-branching-trace/batch88-20261021/chondrites-branching-trace.png",
            "sha256": "e8631c44787054bc259c04d4ca6f68840ead3f8f8c0e8fa0c0422497f397cfd5"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/chondrites-branching-trace.json",
            "sha256": "57037ef23d2b0ab17c817e8c08e9569bda9d274b497591f490a8a04303e93ab5"
          }
        },
        {
          "id": "planolites-smooth-burrow",
          "batch": 88,
          "revision": "r003",
          "candidate_root": "production/batch88/assets/planolites-smooth-burrow/r003",
          "source_commit": "44da0b1831c97ea45f2f68b46c3a119dc168befd",
          "reviewed_source_commit": "b7c7f1c9ec495ad528568770a789b5d15a2de3a4",
          "original_source_snapshot": "44da0b1831c97ea45f2f68b46c3a119dc168befd",
          "review_commit": "44da0b1831c97ea45f2f68b46c3a119dc168befd",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/planolites-smooth-burrow/batch88-20261021/release-metadata.json",
            "sha256": "63e9bd235dd7eb9e0ac96587ef374aaae9f0747b814861d7a54aafe316d6237d"
          },
          "candidate": {
            "path": "production/batch88/assets/planolites-smooth-burrow/r003/candidate.json",
            "sha256": "6b5612d4b296cca7cd4d8d0bf5d17e006fde83b63f4d53ebe6febbcb2b492f5f"
          },
          "active_candidate": {
            "path": "production/batch88/assets/planolites-smooth-burrow/r003/candidate.json",
            "sha256": "6b5612d4b296cca7cd4d8d0bf5d17e006fde83b63f4d53ebe6febbcb2b492f5f"
          },
          "original_profile": {
            "path": "production/batch88/assets/planolites-smooth-burrow/r003/profile-contract.json",
            "sha256": "1a6224ae8b30be0bc8fcc1612f0171b2ee8fcf9331a6e2c513c8f7a9b4c0df5b"
          },
          "active_profile": {
            "path": "production/batch88/assets/planolites-smooth-burrow/r003/profile-contract.json",
            "sha256": "1a6224ae8b30be0bc8fcc1612f0171b2ee8fcf9331a6e2c513c8f7a9b4c0df5b"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-88/report.json",
            "sha256": "3eeaaa1ab379fd8765ca6cce973f061b77ff72be6b4bbef0f6b5958bab530be0"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-88/report.json",
            "sha256": "3eeaaa1ab379fd8765ca6cce973f061b77ff72be6b4bbef0f6b5958bab530be0"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-88/report.json",
              "sha256": "3eeaaa1ab379fd8765ca6cce973f061b77ff72be6b4bbef0f6b5958bab530be0"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-88/ownmanifest.json",
              "sha256": "3c4ecfb9714d8aa8327d2f02e1c93941f04f6848bb7acc4d09e10ea32778bfce"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-88/handoff.json",
              "sha256": "21aa5cfe573a7b1b2287cfb55c8da88017c624bb07eceb7cf1be1ed31dd704a8"
            }
          ],
          "original_metrics": {
            "path": "production/batch88/assets/planolites-smooth-burrow/r003/metrics.json",
            "sha256": "88e932720b2f2d3be1d88a5ec5f68793593d420710b3a7a886fc92bda1573b9e"
          },
          "source_counts": {
            "path": "production/batch88/assets/planolites-smooth-burrow/r003/source-vertex-counts.json",
            "sha256": "6644db7793f69f2060af8cfd91741cf7ff4e87d62e6abc48d72837688f625c39"
          },
          "proof": {
            "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/render-manifest.json",
            "sha256": "88198b77fdd1ac8a620af01e8a232cf8f4bb33813aa5642c164a6c5c71f82aaf"
          },
          "source_preview": {
            "path": "production/batch88/assets/planolites-smooth-burrow/r003/preview.png",
            "sha256": "bbffa9e82e52d4876a9925bc2553388d7d76aa59837821b209a427273f1c2534"
          },
          "capture_reference": {
            "path": "assets/additions/planolites-smooth-burrow/batch88-20261021/planolites-smooth-burrow.png",
            "sha256": "3cdcbed19a7858c311dee882fd8e66d724686d9a7d5108024470f87b36f33e6d"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/planolites-smooth-burrow.json",
            "sha256": "ff4e807af8e073dfec9fc054549cd4416428e075c4613826c1cd09cb0b4a3652"
          }
        }
      ],
      "files": [
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/brief.md",
          "sha256": "ea01b85eb9e994c29de213557616064b9abd199f46ee6c685bce7cf119099ec1",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/build-config.json",
          "sha256": "9ab36efef921acbf278f162e6bb61a649dd14a23c375980cf7cab965c2639690",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/build-dependencies.json",
          "sha256": "fb784108093e6477608bc711b4180f9963a587eb89782b7c4ab11ae970d9fd6c",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/candidate-brief.json",
          "sha256": "f69c69adf836da58e7f1d5260887f4f7abb58272970422d1fc38b78ca85605c2",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/candidate.json",
          "sha256": "e4ebe9a5866bcd0ecf0c29fa7b510366ac5c18590cfd845dceaf297cd518adb7",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/concept-original.png",
          "sha256": "74675f4a00a80f9278656281c58fc38e1e9a730b99fb1e23bd997903fa1cc40d",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/concept-prompt.txt",
          "sha256": "e0d58ebbcee0da4fda72cfa3693c16446afeef0e024bdc20dbee50ca7fe22654",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/contact-sheet.png",
          "sha256": "8b1039c000e5c1661b4301a5ade5234574e2ff68118abae88582dcf672f9c309",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/final-rebuild-binding.json",
          "sha256": "61195c206907cc6a15e631bc9f213e1dfe8c1a12e21e50e75be548b44eddeac1",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/generator.py",
          "sha256": "4acd7af382207a61502363db87015d73a93d5825b2ce6c0e436361f3fc18a28b",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/gltf-validator.report.json",
          "sha256": "dc99b71afd9b0f7d8ef9e7f1da94d8d74cc72c1ffa6cf1efc7bfcc721a6cd85f",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/lifecycle.jsonl",
          "sha256": "577eaf19a03cf67c718dd2365919d54408ab30b716e60c0ffa0ed4ce8632ecd3",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/maker-review.md",
          "sha256": "2e8b5e9704ad4669a70892693f898c618bd775939d194a9cce853ee48f59e743",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/metrics.json",
          "sha256": "9b28fcd56257e62298a90dbcf887030e9696f15a00e8cb242e7c4cb1138daf0e",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/model.glb",
          "sha256": "72a9922ede8d80e1c7c15795c66bf37fffd5dd066cdfaa5f419683f947f05cfe",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/physical-surfaces.report.json",
          "sha256": "5dfb0f7671c8014a9d45ae8b6ab3822cc0b82c76f6132b2abb31b1016849cf61",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/pixel-inspection.json",
          "sha256": "6ad758dc7831cc19049a4cfb635b55110bf70de24e5e5595d758b1a0e10fe31f",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/preview.png",
          "sha256": "fcd6c676cf5e4ef25cff5ac0880fb6ae19eae6997d39a175da0fb3954bf22543",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/profile-contract.json",
          "sha256": "9b0ba5804e961148b4c848b07fa4b12d82fa988f31832bf4a815d704b239278f",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/clay.png",
          "sha256": "2063dd5206fcb045a69b8b35c481fe95ac13527c2321e4f0aece6c3d92789d19",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/front.png",
          "sha256": "895d8e6891d9b09efb80bfe6874d965c38e23ed5b9ad2950cdbe9332e15ed400",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/hero.png",
          "sha256": "fcd6c676cf5e4ef25cff5ac0880fb6ae19eae6997d39a175da0fb3954bf22543",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/rear.png",
          "sha256": "01dbbe2dfd3a6b2d11d917f9cef7df0d765e7d45ba50d74e90016beae95479ee",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/render-manifest.json",
          "sha256": "dfbf0e99d420dc07c63be0deb0d01c29a36320f8657ae8edbd90e98bc0757536",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/reversehero.png",
          "sha256": "08d09d161d9aec9c15c768c36d76baf6f844763dac7a4ffa0b8ee6d080be4f39",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/side.png",
          "sha256": "af0717172b371c4fcd78d74d53d4f94d1956ded1d2f02d762754bcd2a19f2152",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/silhouette.png",
          "sha256": "c40df50222f41796c5bd0737a803a518d4b95175f88de92d835c50e02438d8d5",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/proof-final/top.png",
          "sha256": "3c6f5f09006757ff2e6ed821563abde3cb6ab2e6fddab4f7199e4a219906acc6",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/references.json",
          "sha256": "bd4b74f7dbeabe0a9e1e86cd37f2b2a56919e0ddfaaa9391485f6a075783c934",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/repair-freeze.json",
          "sha256": "2262c2b7ce7c1fe90a6cad200335661059f54fdc75f9299eb3fa96c1da4165ee",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/repro-final-1.report.json",
          "sha256": "78cd714ece54bd2d872469cb89ba2e00837b44a2df7ea0208ca66d1c6339aef3",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/repro-final-2.report.json",
          "sha256": "73fa0591926a800d7fbfba363bd2191c6528c496c1a4dc7678003105b225b146",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/runtime-parse.report.json",
          "sha256": "6eefc6aa0a15156f95685d2ded14ef4d95856293abb777ffcde36b2e413057e9",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/source-final.report.json",
          "sha256": "90b3adc02c26a3ff17e7b47023acac9ecf1ca61dfd33d1a648653d67caf9a9ae",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/source-metrics.json",
          "sha256": "90aa206accc3fa35c59e0a8851ddf64d17581730416c9d1582068cd3917d2ace",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/source-vertex-counts.json",
          "sha256": "b425d7eb799aa5a94320400a7e8da43a7c20dbd8ce48e68e0a30a844adb5a8eb",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/chondrites-branching-trace/r002/source.blend",
          "sha256": "481f62bc1705a31a517cfee69b24088c655a909f685b9592634e52c25174241a",
          "origin": "source",
          "owner": "chondrites-branching-trace"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/brief.md",
          "sha256": "23873422ed0a0d1bd9a742b3adf977d614871f9816d3b0e480d265260ecd8376",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/build-config.json",
          "sha256": "bfc34752a96782939580c247ba6b465e9074160697ae03f2b7220e59b805e1d7",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/build-dependencies.json",
          "sha256": "f4524cc75021bb9d49f0d91671cd45b07673db863a1e78b8cfddb5b380dcc928",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/candidate-brief.json",
          "sha256": "ca78b73c027c6bc9fa96ff35bcc3479d71a3911ff1df4074688d354aafb6fab4",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/candidate.json",
          "sha256": "6b5612d4b296cca7cd4d8d0bf5d17e006fde83b63f4d53ebe6febbcb2b492f5f",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/concept-original.png",
          "sha256": "0e1c627a26d7b552779b71f1a5d5cfb0328fc8fdfbfcbb8573f399062b66fa12",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/concept-prompt.txt",
          "sha256": "282ba10179d31d85ea0524855595ca408218a0c95e4f80523f17705eb032722e",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/contact-sheet.png",
          "sha256": "eb6398f81db43c6f42633a072893480caa60d8ce84214e420fc03dd3c3ac1591",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/final-rebuild-binding.json",
          "sha256": "0b445f2bd5b12eeefba2f20d8c29824813a371510fa1689fab3d2d4f7b16fb88",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/generator.py",
          "sha256": "c0c73707b463502f43711c05344ea254f4c33f519dbd9d6ed2ad61a58a26dab0",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/gltf-validator.report.json",
          "sha256": "6fce4d3e252b9104c157168d73108f3cefc5084ccbb15de2925ac68fc02d4a47",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/lifecycle.jsonl",
          "sha256": "fd78508d86b13faebc96314475f7fb35e1eeae2a8934c29f1e807360457d495a",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/maker-review.md",
          "sha256": "e97771575fcef3b72a858892cac246d8c42f21f9a1757e6fa039e326b17372f3",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/metrics.json",
          "sha256": "88e932720b2f2d3be1d88a5ec5f68793593d420710b3a7a886fc92bda1573b9e",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/model.glb",
          "sha256": "84ef7cdf4286e84cf1ec5473678c3bcbf7dd01258b9e95468339236761a3e694",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/physical-surfaces.report.json",
          "sha256": "2657ae4a7d0886548bd4b621a197e6c3d19497a7d98f59ec22e22c200b36162a",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/pixel-inspection.json",
          "sha256": "c41fe24c53f56a7c35c0274507a5fac555bf3294ea31d933314f565dc22e293f",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/preview.png",
          "sha256": "bbffa9e82e52d4876a9925bc2553388d7d76aa59837821b209a427273f1c2534",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/profile-contract.json",
          "sha256": "1a6224ae8b30be0bc8fcc1612f0171b2ee8fcf9331a6e2c513c8f7a9b4c0df5b",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/clay.png",
          "sha256": "95e9e332dd711ce8bd9177d5488a19fd576d670a202d871d2055062c1ed39e80",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/front.png",
          "sha256": "c2bca6d8ca9ea714b1a3c1da76029b8e21464318db0fa38dff74a910f9533824",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/hero.png",
          "sha256": "bbffa9e82e52d4876a9925bc2553388d7d76aa59837821b209a427273f1c2534",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/rear.png",
          "sha256": "0f4a1803a8f7bc12850ce2cf1bb3ece83123a623b4919546f2f560222f716516",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/render-manifest.json",
          "sha256": "88198b77fdd1ac8a620af01e8a232cf8f4bb33813aa5642c164a6c5c71f82aaf",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/reversehero.png",
          "sha256": "736f647a4b5e5bbe1ed5ecf8aa838201ebcc81d97cff5fa487d41632cb5847b5",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/side.png",
          "sha256": "c729347e9312abb05427724f5c7756cd6d78e32781ab749cd39b5aab9848fb9d",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/silhouette.png",
          "sha256": "1bddd6d8dfa22d59d902b3a87c6931b7edf69160cdebef73147f4146ea6e7b31",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/proof-final/top.png",
          "sha256": "c04b53dbdcf897fe709133d8b9c67494d210ef910af49c2d484a5f3da9cca386",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/references.json",
          "sha256": "782e2a72d0c1a982e042089ff6b6e419c464a2423c4355ff8d16e5940be09954",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/repair-freeze.json",
          "sha256": "442f3b4b798e7324652e83607d07464faa02388bafee92e3e7a027588c653971",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/repro-final-1.report.json",
          "sha256": "a08a6af2158bbe7608867c84b82d6ae660523f3ec6858ee4d7199cee269f2ea1",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/repro-final-2.report.json",
          "sha256": "659b9eae5eca47197d0f6a9d5c4714c5c02f073a99c60e358469fed3db95decf",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/runtime-parse.report.json",
          "sha256": "ec5a58e12b1b088fef6236a17bfa32b676b621f3167d8fc25a38789aaec8569b",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/source-final.report.json",
          "sha256": "e2bd494f8ac9cf1a234b65a09078fe8bc6700e87ffb00468e74c6ecd20040906",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/source-metrics.json",
          "sha256": "10e3ff07832c75bc45d7d94f325138634dbd0c1f969f5f6938b046ee8f20a019",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/source-vertex-counts.json",
          "sha256": "6644db7793f69f2060af8cfd91741cf7ff4e87d62e6abc48d72837688f625c39",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "production/batch88/assets/planolites-smooth-burrow/r003/source.blend",
          "sha256": "210570d890c85a2b4f8bb397ecb0c6100d87acee66c0ba11da911213391a0053",
          "origin": "source",
          "owner": "planolites-smooth-burrow"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/REPORT.md",
          "sha256": "9d6889ad731244723354ceab2feb524add7b902ee8697429241a42d40daf7680",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/check-provenance.py",
          "sha256": "d9753269b25ed8d2dab79bab9708149d775b58a3f87bad0f9f10baff8faeef87",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/handoff.json",
          "sha256": "21aa5cfe573a7b1b2287cfb55c8da88017c624bb07eceb7cf1be1ed31dd704a8",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/inspect-source.py",
          "sha256": "113ae2c0d4104cd44a6b78c435c580e05d3d013ffa8231442690b52c7174fae1",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/measure-caps.py",
          "sha256": "16677886aa6e4f024ce4d4af67100410e511a428f4f304e54eaa4777346d4827",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/measure-geometric-core-50um.py",
          "sha256": "083dcfea68c87e58ab809301289fcf1ac4cd5ff104fcdd77a59a1ec9dab68504",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/measure-geometric-core.py",
          "sha256": "d5cac13ce7216f1e26da2e4ab4fc76854bfaf970b7e9152361362e0373706080",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/measure-plant-connectivity.py",
          "sha256": "34770400f6eae62b21be847081197d204ec6c7faf8e150c6b60b92db49f884b5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/measure-traces.py",
          "sha256": "59d8933a486c68e30b65b3ec571bf15719d8d5c077d7513eaec083acc859d87a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/ownmanifest.json",
          "sha256": "3c4ecfb9714d8aa8327d2f02e1c93941f04f6848bb7acc4d09e10ea32778bfce",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/report.json",
          "sha256": "3eeaaa1ab379fd8765ca6cce973f061b77ff72be6b4bbef0f6b5958bab530be0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/reproduce-core-overhang.py",
          "sha256": "8d1bbb76ff8af285b4d8e2f2fd9ef6ec4c37cad7643f92825cc90b956a9bf9f3",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/run-source.py",
          "sha256": "dd0d36bf47cb22618907077d127f72996cc1563e1ff55ff84b5284e2ef6114d4",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/runtime-check.mjs",
          "sha256": "349c4467c92e71a7f60a3d3ed585f7f0a55ec7d77f9459c328fc15d1a9cdf46a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-88/write-report.py",
          "sha256": "9a17eb9bba192b721b7f69a898a643d1d8cf7f0eac585153bff65367d07a3de9",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g04-release-20261021/process-archive-index.json",
          "sha256": "39ed4881280181b46d137c0a87a944836e663a7d52330da0e72bc87fe0549c81",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g05-20261021.json",
      "sha256": "d1af9871eade30e50ad812c2a577d243d68ca2d29de84d69eb4b958e1fdceec8"
    },
    "release": {
      "version": 1,
      "scope": "next52-g05-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
      "review_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g05-release-20261021/source-bundle.json",
        "sha256": "e3e0e54d14ffe71b624315b8c4cca7733b5adda37e90109f2af01b15f19b7b7a"
      },
      "protected_source_inputs": [
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
          "path": "production/small-life-batch89/tools/measure_source.py",
          "sha256": "280b0e35f4595ab933a46f79b52484a429ed0ded391783580965908bca95dbb9"
        },
        {
          "path": "production/small-life-batch89/tools/parse.cjs",
          "sha256": "813bbe4ebbfc1cd80b2d45075f34a43bab68989991e3f81a0858a76c88a790d5"
        },
        {
          "path": "production/small-life-batch89/tools/render.py",
          "sha256": "dce6084f0ec6663a5ca5acd3f5815f128314c4e2c94c04748be153ed75c6879e"
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
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        },
        {
          "path": "scripts/validate_candidate.py",
          "sha256": "fe679a8be19d16b9d9b86ee3419a73d2dd16b77dfa371bf1186ce0120d120ff9"
        },
        {
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/OWN_QA_MANIFEST.json",
          "sha256": "a9a4bc40be3bd8a80c8c15ddab608393c9130b87235c1a4d3393804bcb1792d0"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/handoff.json",
          "sha256": "52ad2e2df3749d9662008c11e2517b00564a4ae16dddd4f819964a5d6431de0b"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/independent-review.json",
          "sha256": "5bd44e4996ac3c1bdf39e377f214830a1449b088b429d7a2e1fa1609ba77fc52"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "skolithos-pipe-field",
          "batch": 89,
          "revision": "r002",
          "candidate_root": "production/small-life-batch89/skolithos-pipe-field/r002",
          "source_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
          "reviewed_source_commit": "4264dbafd0cc3142175c890644f2990dfaa0acf6",
          "original_source_snapshot": "4888640f243df6aa50e6057f7465cc2d32147829",
          "review_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/skolithos-pipe-field/batch89-20261021/release-metadata.json",
            "sha256": "fce12068ca5653844713023514530a0181f7b317622ab138ca4c28a8aeafa627"
          },
          "candidate": {
            "path": "production/small-life-batch89/skolithos-pipe-field/r002/candidate.json",
            "sha256": "d01f23bf85e4bdf3c93961ee5ff626ac768c2531a4d769300615aaa6c9cec05a"
          },
          "active_candidate": {
            "path": "production/small-life-batch89/skolithos-pipe-field/r002/candidate.json",
            "sha256": "d01f23bf85e4bdf3c93961ee5ff626ac768c2531a4d769300615aaa6c9cec05a"
          },
          "original_profile": {
            "path": "production/small-life-batch89/skolithos-pipe-field/r002/profile-contract.json",
            "sha256": "ffea99e3eea99a9e640aa6d2d3e2f7fa569cd677ff43370d7be666028bc61c1d"
          },
          "active_profile": {
            "path": "production/small-life-batch89/skolithos-pipe-field/r002/profile-contract.json",
            "sha256": "ffea99e3eea99a9e640aa6d2d3e2f7fa569cd677ff43370d7be666028bc61c1d"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/independent-review.json",
            "sha256": "5bd44e4996ac3c1bdf39e377f214830a1449b088b429d7a2e1fa1609ba77fc52"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/independent-review.json",
            "sha256": "5bd44e4996ac3c1bdf39e377f214830a1449b088b429d7a2e1fa1609ba77fc52"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/independent-review.json",
              "sha256": "5bd44e4996ac3c1bdf39e377f214830a1449b088b429d7a2e1fa1609ba77fc52"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/OWN_QA_MANIFEST.json",
              "sha256": "a9a4bc40be3bd8a80c8c15ddab608393c9130b87235c1a4d3393804bcb1792d0"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/handoff.json",
              "sha256": "52ad2e2df3749d9662008c11e2517b00564a4ae16dddd4f819964a5d6431de0b"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch89/skolithos-pipe-field/r002/artifacts/metadata.json",
            "sha256": "8ee45c15727d9c1e566e91e2c636fffcc35414449338b42cc5db862274263dbe"
          },
          "source_counts": {
            "path": "production/small-life-batch89/skolithos-pipe-field/r002/qa/authored-evaluated-counts.json",
            "sha256": "1bc3cf1a830db970a12f04bf4b48990fe76f3180dc457938b568ebc7d18f86ab"
          },
          "proof": {
            "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/render-manifest.json",
            "sha256": "eaffc696465d5ee15c61314a54343aa5ed224e6b3b20cbe9da775db7e6251a86"
          },
          "source_preview": {
            "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/hero.png",
            "sha256": "9a4140317823323ec4b4b23fdd8a123a6d541a333a1c13fa2cd344b9f5a5973a"
          },
          "capture_reference": {
            "path": "assets/additions/skolithos-pipe-field/batch89-20261021/skolithos-pipe-field.png",
            "sha256": "85e9a50609451c76a4bdcb362091be53c68b8832109775ce42a82675f40970d7"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/skolithos-pipe-field.json",
            "sha256": "3076cf01a895aa1e82a55c5db91d18db8d08051e298027b7110f245a83ad01d0"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch89/concepts/skolithos-pipe-field-concept.png",
          "sha256": "2f654b69b2166cc7b35400bf33b32a23f541cee2b7e76e4f90219b5488b22903",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/concepts/skolithos-pipe-field-prompt.txt",
          "sha256": "4a0f548d4074088867c0c2d6cb3e1d184a75e0ff024ce3a3edc97624999af9c8",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r001/candidate.json",
          "sha256": "c7e06189a89ca8b1b39a3556c8aa7970d691f3de77cdd4054bc36c89b7e1fa97",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/artifacts/metadata.json",
          "sha256": "8ee45c15727d9c1e566e91e2c636fffcc35414449338b42cc5db862274263dbe",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/artifacts/skolithos-pipe-field.blend",
          "sha256": "645f1344973768ecf8f145a6038928218b37ff85520b30b4fef64e2e4c2b3667",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/artifacts/skolithos-pipe-field.glb",
          "sha256": "6e729192850db1f29bd886d2d5d07518ae4e8ff2b4d373d245cb8493eef3fbd3",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/candidate.json",
          "sha256": "d01f23bf85e4bdf3c93961ee5ff626ac768c2531a4d769300615aaa6c9cec05a",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/config.json",
          "sha256": "db3eb20deed11a7a6030e6fba5acb93706df40c12f1d3598a2632b17830cc5c2",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/delivery-brief.json",
          "sha256": "96210f9dc574d69b2506c74d433149859370bfe5840b8c7942b74d3afde7a610",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/dependencies.json",
          "sha256": "21cebc24981bfc09d59a25a73434342ece1ccf9993e4d3e01f4928e12c463a5a",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/profile-contract.json",
          "sha256": "ffea99e3eea99a9e640aa6d2d3e2f7fa569cd677ff43370d7be666028bc61c1d",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/qa/authored-evaluated-counts.json",
          "sha256": "1bc3cf1a830db970a12f04bf4b48990fe76f3180dc457938b568ebc7d18f86ab",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/qa/runtime-parse.report.json",
          "sha256": "d7958e53790e6bd96d575acdb9bab800a014eec438a272b136397fbf303c08a9",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/qa/technical.report.json",
          "sha256": "6195fa34ac01dd0a8db0fd8cc6e89dc5046879d97d0807b3b229219af894ab98",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/references.json",
          "sha256": "462acade525357722fbc24fd3391970e666b7550fc3baf026c4bf6d7159a60be",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/clay.png",
          "sha256": "224aa95e11d599c375a34439b98403ea1e2705c8dd9ff598ca8938fe6a570c82",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/front.png",
          "sha256": "9e95a2b11a896f9c4acd8c3be775f8458a4af9d718ff30f9f6bee81be5967079",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/hero.png",
          "sha256": "9a4140317823323ec4b4b23fdd8a123a6d541a333a1c13fa2cd344b9f5a5973a",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/rear.png",
          "sha256": "365416067aa7c88850855648b39df97e9c46057c7111d4af0aec65db65315563",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/render-manifest.json",
          "sha256": "eaffc696465d5ee15c61314a54343aa5ed224e6b3b20cbe9da775db7e6251a86",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/reversehero.png",
          "sha256": "719645ae9fdc3080c85b9e2240217222abae684fa3cbf3d3374497ebd4727f50",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/side.png",
          "sha256": "d6688ba17c66efc5749f96a9decac1352966578024e3cdc6465e5f18781fb1d0",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/silhouette.png",
          "sha256": "e69c37c370b1092172637d049eebce459624e53d94dcd613c8470ac8f57a38c5",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/skolithos-pipe-field/r002/views/top.png",
          "sha256": "ca0acb8a443a6ccf912ce0d1eeb6c1f77230b81b5eab0207a1334979aaf47bac",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/tools/generate-skolithos-r002.py",
          "sha256": "ca2f793abf8b1903ae45190cdc5b141e8b34cc920582eaae524d5fdf906be8d2",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/tools/measure-skolithos-radius-r002.py",
          "sha256": "c6dc97c20e1478613609f18fe9288d32e34f6c3b380774853be7132bea161f10",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "production/small-life-batch89/tools/reopen-skolithos-r002.py",
          "sha256": "c516bef1088a78ee1e9542bc57350d3e54576e1bd95a3b14ba698476be01621e",
          "origin": "source",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/OWN_QA_MANIFEST.json",
          "sha256": "a9a4bc40be3bd8a80c8c15ddab608393c9130b87235c1a4d3393804bcb1792d0",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/audit_provenance_resume2.py",
          "sha256": "9805cac65e8ff067b4c2d9b0cf2ddc5a20d8cf2b7b9937a2bc5f1212fc9bd9fc",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/finalize_review_resume2.py",
          "sha256": "39b72818870f023b1310cac76ee2462849e957f6e84ec4f681c85b8563d40f4e",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/handoff.json",
          "sha256": "52ad2e2df3749d9662008c11e2517b00564a4ae16dddd4f819964a5d6431de0b",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/independent-review.json",
          "sha256": "5bd44e4996ac3c1bdf39e377f214830a1449b088b429d7a2e1fa1609ba77fc52",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/measure_world.py",
          "sha256": "a2cd7a2959328aed8b96b99669c83a0a25ad7845fe87d850f87b7c23be5deecf",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/recheck_geometry_resume2.py",
          "sha256": "e532bfc8c305f45e98481680d1ce178c322d30674bab8341b4865624609140ce",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/reopen_measure_reexport.py",
          "sha256": "e938809ad21693d5eab87deace1e4b5aa1e4acf2d0df57b59949e0a304c0fcd7",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/report.md",
          "sha256": "0cbb39eb92087405f8a9380d978348813d6ee0175c61eeb71390b604dbcd10bf",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch89-skolithos-r002/runtime_checks.cjs",
          "sha256": "c25a855b0693c47c8ebc62f35862e7eed3c47308fdc6636972a44eee8d42dc49",
          "origin": "review",
          "owner": "skolithos-pipe-field"
        },
        {
          "path": "qa/next52-g05-release-20261021/process-archive-index.json",
          "sha256": "59113a1e656c697f6eb17bf56539befd07bd191268aed251ba06c1b10c17dfe6",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g06-20261021.json",
      "sha256": "5a112bf6dce3afbf1b3325037b468c1c6f9c4b751e5c1183790b71414ec489ac"
    },
    "release": {
      "version": 1,
      "scope": "next52-g06-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
      "review_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g06-release-20261021/source-bundle.json",
        "sha256": "679835c462aacc6b8042a9c4e0683ba8757c56a8f93718fd205b0a4f59910611"
      },
      "protected_source_inputs": [
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
          "path": "production/small-life-batch89/dependencies.json",
          "sha256": "18fa560aa2a92b74fffed67cb7f4d2fb9a5c8646fc26634f06ec023c6edf1774"
        },
        {
          "path": "production/small-life-batch89/tools/measure_source.py",
          "sha256": "280b0e35f4595ab933a46f79b52484a429ed0ded391783580965908bca95dbb9"
        },
        {
          "path": "production/small-life-batch89/tools/parse.cjs",
          "sha256": "813bbe4ebbfc1cd80b2d45075f34a43bab68989991e3f81a0858a76c88a790d5"
        },
        {
          "path": "production/small-life-batch89/tools/render.py",
          "sha256": "dce6084f0ec6663a5ca5acd3f5815f128314c4e2c94c04748be153ed75c6879e"
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
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        },
        {
          "path": "scripts/validate_candidate.py",
          "sha256": "fe679a8be19d16b9d9b86ee3419a73d2dd16b77dfa371bf1186ce0120d120ff9"
        },
        {
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-handoff.json",
          "sha256": "72ab6f9b989c4d415d154695cf970a677923eccfd77a6ee7b171c9daf0aa0a74"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
          "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/own-manifest.json",
          "sha256": "8afe6efd7fc3e9f61051b05f1dbf415433aa22f15b13b060b6b90ec29057ecdc"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "psilophyton",
          "batch": 89,
          "revision": "r001",
          "candidate_root": "production/small-life-batch89/psilophyton/r001",
          "source_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
          "reviewed_source_commit": "7ae917c10db80d59fca39a507f91de865cf69b10",
          "original_source_snapshot": "4888640f243df6aa50e6057f7465cc2d32147829",
          "review_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/psilophyton/batch89-20261021/release-metadata.json",
            "sha256": "2062363982ca3bb9e918e2c1c9e31a47d9a39d11cf1678ad84accbef9eb092d5"
          },
          "candidate": {
            "path": "production/small-life-batch89/psilophyton/r001/candidate.json",
            "sha256": "b87de9a53f9246a270229ce9fe5032ecc8f9060643a59cf1b8280f20b60c89f0"
          },
          "active_candidate": {
            "path": "production/small-life-batch89/psilophyton/r001/candidate.json",
            "sha256": "b87de9a53f9246a270229ce9fe5032ecc8f9060643a59cf1b8280f20b60c89f0"
          },
          "original_profile": {
            "path": "production/small-life-batch89/psilophyton/r001/profile-contract.json",
            "sha256": "8a668a4f4c413e34c9247fcf3e98133a67f71f4ba7c826c67648f53e85db4249"
          },
          "active_profile": {
            "path": "production/small-life-batch89/psilophyton/r001/profile-contract.json",
            "sha256": "8a668a4f4c413e34c9247fcf3e98133a67f71f4ba7c826c67648f53e85db4249"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
            "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
            "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
              "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-89/own-manifest.json",
              "sha256": "8afe6efd7fc3e9f61051b05f1dbf415433aa22f15b13b060b6b90ec29057ecdc"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-handoff.json",
              "sha256": "72ab6f9b989c4d415d154695cf970a677923eccfd77a6ee7b171c9daf0aa0a74"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch89/psilophyton/r001/artifacts/metadata.json",
            "sha256": "bd3cd519895a3981f2f1d932359cf613e14c81d70abeb522199c88708fdb6737"
          },
          "source_counts": {
            "path": "production/small-life-batch89/psilophyton/r001/qa/authored-evaluated-counts.json",
            "sha256": "4053a502e8064957fceb91d10720e65b23962b8502c47fe73e42f825ad9da43c"
          },
          "proof": {
            "path": "production/small-life-batch89/psilophyton/r001/views/render-manifest.json",
            "sha256": "e2fe23bcd5d06ec25801cbc7421c7986872ee83066f24a2d7ea027c0012104e4"
          },
          "source_preview": {
            "path": "production/small-life-batch89/psilophyton/r001/views/hero.png",
            "sha256": "f0997d5602c2f908e15db3c5365c85f59f3d6c2ac1631dc7c6223b1e00093ae7"
          },
          "capture_reference": {
            "path": "assets/additions/psilophyton/batch89-20261021/psilophyton.png",
            "sha256": "556ada761f23344fa50b65550d737f94e9b381ea18b77cb6f30aed3b051faa89"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/psilophyton.json",
            "sha256": "29c7d8f563d65874cd662890c14d759e4b0cf5dca21db4782813d5bcd39b0f8f"
          }
        },
        {
          "id": "rosselia-concentrically-filled-burrow",
          "batch": 89,
          "revision": "r002",
          "candidate_root": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002",
          "source_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
          "reviewed_source_commit": "7ae917c10db80d59fca39a507f91de865cf69b10",
          "original_source_snapshot": "4888640f243df6aa50e6057f7465cc2d32147829",
          "review_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/rosselia-concentrically-filled-burrow/batch89-20261021/release-metadata.json",
            "sha256": "790263ba5cbfab08bfeb5167aee89e36557c8283c34e6b2ce6b7a146a5637d1a"
          },
          "candidate": {
            "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/candidate.json",
            "sha256": "c9e9b504138c15dffe9ae8a837a14641f8c35644f882085604066c9f00149278"
          },
          "active_candidate": {
            "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/candidate.json",
            "sha256": "c9e9b504138c15dffe9ae8a837a14641f8c35644f882085604066c9f00149278"
          },
          "original_profile": {
            "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/profile-contract.json",
            "sha256": "8d38fecca72637815b7009ced784cf0bfcb0b28e6a242e964ad7fe76735f884f"
          },
          "active_profile": {
            "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/profile-contract.json",
            "sha256": "8d38fecca72637815b7009ced784cf0bfcb0b28e6a242e964ad7fe76735f884f"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
            "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
            "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
              "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-89/own-manifest.json",
              "sha256": "8afe6efd7fc3e9f61051b05f1dbf415433aa22f15b13b060b6b90ec29057ecdc"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-handoff.json",
              "sha256": "72ab6f9b989c4d415d154695cf970a677923eccfd77a6ee7b171c9daf0aa0a74"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/artifacts/metadata.json",
            "sha256": "0179b5a43203c6f77c3b518c77b751d54ef8db04f8a361211f2a95d060294710"
          },
          "source_counts": {
            "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/qa/authored-evaluated-counts.json",
            "sha256": "6e04602ce1a84752f283ba02e743cb4d3dfc940a35967c9ebaa99105eb81d46d"
          },
          "proof": {
            "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/render-manifest.json",
            "sha256": "a7c042b1812d4538b657fcf33408e50e0e5259a6840ea63bbff201f85b2eb90d"
          },
          "source_preview": {
            "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/hero.png",
            "sha256": "9579d325cb49ddf6a86beecf78518674d44c1edabeb1c8cfa9b8960152b83d30"
          },
          "capture_reference": {
            "path": "assets/additions/rosselia-concentrically-filled-burrow/batch89-20261021/rosselia-concentrically-filled-burrow.png",
            "sha256": "ddf53349536e0c8126254813896e56b1d8527c15382ca94ec8c8737738c94b22"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/rosselia-concentrically-filled-burrow.json",
            "sha256": "df541c3ed29f1d1e1ef6954331c06b116dd5424ac78741f77b99c945b4c7b7c0"
          }
        },
        {
          "id": "teichichnus-spreite-wall",
          "batch": 89,
          "revision": "r003",
          "candidate_root": "production/small-life-batch89/teichichnus-spreite-wall/r003",
          "source_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
          "reviewed_source_commit": "7ae917c10db80d59fca39a507f91de865cf69b10",
          "original_source_snapshot": "4888640f243df6aa50e6057f7465cc2d32147829",
          "review_commit": "4888640f243df6aa50e6057f7465cc2d32147829",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/teichichnus-spreite-wall/batch89-20261021/release-metadata.json",
            "sha256": "be6e36a5a49b5e09c749ba3b22bfddc4e22f5877aba93dff00412b6059b89b44"
          },
          "candidate": {
            "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/candidate.json",
            "sha256": "efbcc490eeed3d9c337765e5d192fd9eb75fea7cfd83151038fae0969291cc0d"
          },
          "active_candidate": {
            "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/candidate.json",
            "sha256": "efbcc490eeed3d9c337765e5d192fd9eb75fea7cfd83151038fae0969291cc0d"
          },
          "original_profile": {
            "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/profile-contract.json",
            "sha256": "8ae7669ed3c3f1b1d5a0f774a68e8caf9946c0f033517495f9be0105bd5064f0"
          },
          "active_profile": {
            "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/profile-contract.json",
            "sha256": "8ae7669ed3c3f1b1d5a0f774a68e8caf9946c0f033517495f9be0105bd5064f0"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
            "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
            "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
              "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-89/own-manifest.json",
              "sha256": "8afe6efd7fc3e9f61051b05f1dbf415433aa22f15b13b060b6b90ec29057ecdc"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-handoff.json",
              "sha256": "72ab6f9b989c4d415d154695cf970a677923eccfd77a6ee7b171c9daf0aa0a74"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/artifacts/metadata.json",
            "sha256": "eb5780796142f52ace776aab74aa2c026ab47d8dbc090e2ac717e82bcefed58e"
          },
          "source_counts": {
            "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/qa/authored-evaluated-counts.json",
            "sha256": "f1c7736e71fdb049ff8d1503f7244eabc6819674516067919474fc81ba3cd637"
          },
          "proof": {
            "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/render-manifest.json",
            "sha256": "d8e39b91df42190e88283e3a3d3be3afc20c23ea6c4a8730a48d5b2150dfa825"
          },
          "source_preview": {
            "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/hero.png",
            "sha256": "19de070eba638b066f2e6866d076bccd1ae75147075863f0ffa177b4419dbbcc"
          },
          "capture_reference": {
            "path": "assets/additions/teichichnus-spreite-wall/batch89-20261021/teichichnus-spreite-wall.png",
            "sha256": "bf3c73b66f80a9335786a044d6e0fa3f9ea7406e2d357958f644de3c0f012711"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/teichichnus-spreite-wall.json",
            "sha256": "3b5587c69bf3e186487b20bc0202bb052f87330a5cbe359ac82900c86f63be57"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch89/concepts/psilophyton-concept.png",
          "sha256": "e871d273f737baa84ada9887b2f34f62febf3ee8f4ef87c7a87a0af267d82602",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/concepts/psilophyton-prompt.txt",
          "sha256": "dea78d3559b5527070f651e91919af08000d3084ebee69d7e7b0d6f0aad17829",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/concepts/rosselia-concentrically-filled-burrow-concept.png",
          "sha256": "a07202b66127f610aaf3705ab00c266bf45642f9347f13e4633968a73598ce7e",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/concepts/rosselia-concentrically-filled-burrow-prompt.txt",
          "sha256": "7fb07d9401165814062781470cfdfecc26ac25b1612267f820f741d7dbf8f446",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/concepts/teichichnus-spreite-wall-concept.png",
          "sha256": "9ae60cc18e7db200ed07834ff40d5207bb44d4d2302b6e2166e1197fc3f31f84",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/concepts/teichichnus-spreite-wall-prompt.txt",
          "sha256": "e33c59b84647a7f759a3b24d5eb82b6aae674ec8fd40faae8e299ae9ca7c26a3",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/dependencies-r003.json",
          "sha256": "ee94bac110e4a00634794d78ea48141ce003814f02b24ee139acdc0db45170f6",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/artifacts/metadata.json",
          "sha256": "bd3cd519895a3981f2f1d932359cf613e14c81d70abeb522199c88708fdb6737",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/artifacts/psilophyton.blend",
          "sha256": "0cadeabdf002fbee67fdff971b0bc7054a44a1938ff88ad10d34461ad2d3d692",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/artifacts/psilophyton.glb",
          "sha256": "d729d9210e9a1df61a4ccde757e144fc5113914d92b2ea017b74c8ccfc975118",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/candidate.json",
          "sha256": "b87de9a53f9246a270229ce9fe5032ecc8f9060643a59cf1b8280f20b60c89f0",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/config.json",
          "sha256": "0f1ff42a88f75be2b7c781c83d688f30f49239b18c9925019ecc55c357bf3070",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/delivery-brief.json",
          "sha256": "22800d4734df5dab26ef968596a6a9f0b5c144f33ca5bae1e61f1202087c8744",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/profile-contract.json",
          "sha256": "8a668a4f4c413e34c9247fcf3e98133a67f71f4ba7c826c67648f53e85db4249",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/qa/authored-evaluated-counts.json",
          "sha256": "4053a502e8064957fceb91d10720e65b23962b8502c47fe73e42f825ad9da43c",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/qa/runtime-parse.report.json",
          "sha256": "3dc06af37a8c9c6c92abc174e1b4af97d0f893a4de1711144acb36a7464f1472",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/qa/technical.report.json",
          "sha256": "04117dd88890dae1e66162719b4a046da1b953562c27c82d91b56abce2764f77",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/references.json",
          "sha256": "fd0994d8f1f42c01c523af8345605dc2884dbea0c4076e680af1201483b5ad54",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/views/clay.png",
          "sha256": "85a5861e184fb7528f69d489db88fba1433f3486897681341354160d77256c2d",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/views/front.png",
          "sha256": "14401c44ee756b7d3eb4122449e83ab574a4217253ffa0fa10cae0452ae6b19f",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/views/hero.png",
          "sha256": "f0997d5602c2f908e15db3c5365c85f59f3d6c2ac1631dc7c6223b1e00093ae7",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/views/rear.png",
          "sha256": "2d81e1687d9aab5b99fd847df45cba9d0b3dcf5b142d69c71acb23352fe04e90",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/views/render-manifest.json",
          "sha256": "e2fe23bcd5d06ec25801cbc7421c7986872ee83066f24a2d7ea027c0012104e4",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/views/reversehero.png",
          "sha256": "cd2c280c30012f5bb1397d5a70820744e28f4cc46571225ed1aeb54ead7d6d80",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/views/side.png",
          "sha256": "80640ab0c4d7114047b584d4a4f196bcdfd48339e1afb3cd9ebdc1ffe9e0ac95",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/views/silhouette.png",
          "sha256": "9585aedd8ca98de9b4763929ff40ac686388669918226ece460fb9bea2f49d00",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/psilophyton/r001/views/top.png",
          "sha256": "3a92aa340992849e6c0165a4aea11c5f237d4dac151c1dccebc9cf24cd0d5b6e",
          "origin": "source",
          "owner": "psilophyton"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r001/references.json",
          "sha256": "761d4872d3b98a3c51c24bb8c1a4f7429fc6dfe3226ccdde0b634c29228b8162",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/artifacts/metadata.json",
          "sha256": "0179b5a43203c6f77c3b518c77b751d54ef8db04f8a361211f2a95d060294710",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/artifacts/rosselia-concentrically-filled-burrow.blend",
          "sha256": "e240bce9476c5e846d3d8118abc83c3f6e338ca374438713196a8a5fbc2ee57e",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/artifacts/rosselia-concentrically-filled-burrow.glb",
          "sha256": "0f839c90ab884478b9a57062107ce84d42f51d1fdd6e153a30c9de8a90d8ca07",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/candidate.json",
          "sha256": "c9e9b504138c15dffe9ae8a837a14641f8c35644f882085604066c9f00149278",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/config.json",
          "sha256": "26e2ae3a359544512c4df7f8fccf69c5fabbde23ee55c6e59b0165d3fcb55d8d",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/delivery-brief.json",
          "sha256": "110584bb28ab87cf77ee4605c254ba356e2a248e9b8baf87d058f63a19df41a4",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/profile-contract.json",
          "sha256": "8d38fecca72637815b7009ced784cf0bfcb0b28e6a242e964ad7fe76735f884f",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/qa/authored-evaluated-counts.json",
          "sha256": "6e04602ce1a84752f283ba02e743cb4d3dfc940a35967c9ebaa99105eb81d46d",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/qa/runtime-parse.report.json",
          "sha256": "6f54928d26d247322548dc783ed66cb2c1a9c4cd2fee20fc6367ed5fc316b994",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/qa/technical.report.json",
          "sha256": "ff7bec6667e7b443468c01df0c9b17a0756a1b7348988132f570ced9604fea40",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/clay.png",
          "sha256": "a14f5b6e84e072df4281431763feb4bef88432d671c5b54e402522a4fb6b4efc",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/front.png",
          "sha256": "0bc396822081ae7d4fe3cb6cbffb3953f637a33c0d2e2f0a32c6add5c25caf22",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/hero.png",
          "sha256": "9579d325cb49ddf6a86beecf78518674d44c1edabeb1c8cfa9b8960152b83d30",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/rear.png",
          "sha256": "0b6149a42a59685978130398ab59faa094489d4ee743daeace923a172f04986c",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/render-manifest.json",
          "sha256": "a7c042b1812d4538b657fcf33408e50e0e5259a6840ea63bbff201f85b2eb90d",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/reversehero.png",
          "sha256": "c3ab0ce1b0ea957076b10bd598db76474831711759d783bf153068b5577e42a7",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/side.png",
          "sha256": "2f87e478f8f366469849dc5a26a29675c1435253323618615b71e37877879258",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/silhouette.png",
          "sha256": "bff84c0ff376f11576d61e2bd91693d62682af71181ef61a0a05955e86a9148e",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/rosselia-concentrically-filled-burrow/r002/views/top.png",
          "sha256": "96240cda22c5759f35be5e1d0e6ec16268f6140ed6bc3e1b68db8ec6d23cd6c3",
          "origin": "source",
          "owner": "rosselia-concentrically-filled-burrow"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r001/references.json",
          "sha256": "40cef2e432e0ee1a257aa4c35aba8d7dfe288bc75c1a9fb56364b578b7e42e72",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/artifacts/metadata.json",
          "sha256": "eb5780796142f52ace776aab74aa2c026ab47d8dbc090e2ac717e82bcefed58e",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/artifacts/teichichnus-spreite-wall.blend",
          "sha256": "1535aa1977d1f3a39da0aa710f84073732d4bcec282a9a0e093c1dbbe0e937ca",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/artifacts/teichichnus-spreite-wall.glb",
          "sha256": "dc663edc45eeeca4d316101f4115a7d22d5d3431ac96df32c6bda5eefcdb1c3e",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/candidate.json",
          "sha256": "efbcc490eeed3d9c337765e5d192fd9eb75fea7cfd83151038fae0969291cc0d",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/config.json",
          "sha256": "86a925dd0061d33d1280095844cdf8af753bb117512e27deb5397afd653f49d5",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/delivery-brief.json",
          "sha256": "e9420013ce73a387d02dc5d193d993cf4c436a02b442049ed3d2a0aaf663055c",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/profile-contract.json",
          "sha256": "8ae7669ed3c3f1b1d5a0f774a68e8caf9946c0f033517495f9be0105bd5064f0",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/qa/authored-evaluated-counts.json",
          "sha256": "f1c7736e71fdb049ff8d1503f7244eabc6819674516067919474fc81ba3cd637",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/qa/runtime-parse.report.json",
          "sha256": "d6cd4e4614902514739637277b4319cb082ac05b0144a6b1e6f5cde4a6633cc7",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/qa/technical.report.json",
          "sha256": "0d3bddda86732454098ca0fc9705fc4532580c7e8184c15ece66845d1f4d146c",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/clay.png",
          "sha256": "2afdb1e9fe9dad948d560967883ae30a694be403615035d3f5de0934ba66be19",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/front.png",
          "sha256": "9dce4f7864bf24e8b1ac04545b35ada893277e9287d71443639f172c52ea395b",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/hero.png",
          "sha256": "19de070eba638b066f2e6866d076bccd1ae75147075863f0ffa177b4419dbbcc",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/rear.png",
          "sha256": "4b2ea8f9f319f1861362e4a5cffc1ab6d07d521ddfb6897faec272aab678782e",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/render-manifest.json",
          "sha256": "d8e39b91df42190e88283e3a3d3be3afc20c23ea6c4a8730a48d5b2150dfa825",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/reversehero.png",
          "sha256": "f2c2c225bae7d5e88dd3be383b43f66dc6662b779c5d7c294ccbc84d7a4d2f5e",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/side.png",
          "sha256": "94e8cae20601846778c8525b54c51abe7edd4dc553d15d40b9fd9123786d9069",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/silhouette.png",
          "sha256": "8e8e6d31054ba496a1c5523d6070a64c900ee58548a551d9e9db3b1c33202668",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/teichichnus-spreite-wall/r003/views/top.png",
          "sha256": "ddd89db97c09ac9a8ec76b6005b25c08419a796d233d6c4b1d8ad623f5017d13",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/tools/generate-relief-r002.py",
          "sha256": "9b1dda782ae0bf5385a2552b5ee026b44e36ee6caacfb157aab82545dcfda249",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch89/tools/generate-teich-r003.py",
          "sha256": "c54f076672f53c1b4ff461da9d9bb7b483c487b519b8df6165614adb35c19fe2",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "production/small-life-batch89/tools/generate.py",
          "sha256": "25871a90c636c8d710285073858c17b91cbfb752d6fb79cb7da83509f379417b",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch89/tools/measure_source-r003.py",
          "sha256": "e17239b6723aed65e9086c5a6236bf970c2614b0f720e8d91a722c81c4a1ac2f",
          "origin": "source",
          "owner": "teichichnus-spreite-wall"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/audit_provenance-attempt1.py",
          "sha256": "459199e56ea70a3a41ea34ad0a91a38be7470ee38d6fc6bfb4d417e5cb5f3ef0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/audit_provenance.py",
          "sha256": "711b0fc92739e193734de8cd83db4ac2cd844bcc96457e91485c03780f0c3dc9",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-handoff.json",
          "sha256": "72ab6f9b989c4d415d154695cf970a677923eccfd77a6ee7b171c9daf0aa0a74",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.json",
          "sha256": "2d412491a835c8eff4999da07692ec7bb532d7159103ba1e645e390aa46a3485",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/independent-review.md",
          "sha256": "9074553508a763fde3904caf3d727ec8daa32a6985e67a08ac2fedb0382ab5a3",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/measure_glb_features.py",
          "sha256": "105bda294738a5476b0a6b1274258bc348f48fc33e5e59c29a67f1f08b7cbc2d",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/own-manifest.json",
          "sha256": "8afe6efd7fc3e9f61051b05f1dbf415433aa22f15b13b060b6b90ec29057ecdc",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/reopen_measure_reexport-attempt1.py",
          "sha256": "1fae86b7680b473375a4a79ce6a3209ba98a75f97d4a7e36a8b21bdfdf21e90c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/reopen_measure_reexport.py",
          "sha256": "0b827fa6897d1ef9d5501b24ca54806e44a19fd7081fa3c1e053cf15dccc8312",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/run_own_sources.sh",
          "sha256": "5a15dee25b6d240cad356b1052db2dae3bf1430852673a7ed7d2c9047c79848f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/runtime_checks.cjs",
          "sha256": "0a035c7d0922cc209d6d864b1f73f6f6885bb945ddc980ef7f807038727d5a7c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-89/write_review.py",
          "sha256": "c2f44461c9db3ff82ca29f1a70bb2dd176c5bb6037eb1798316f3a49fd642f43",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g06-release-20261021/process-archive-index.json",
          "sha256": "fe653882c223d0e5505ce12dbbdc017f936e34babc79eb46a76f732d0effb3d0",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g07-20261021.json",
      "sha256": "0538d0da06fa58989949c7eeca79aa31827bb3ac3c81a9790be1db8133694c9f"
    },
    "release": {
      "version": 1,
      "scope": "next52-g07-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
      "review_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g07-release-20261021/source-bundle.json",
        "sha256": "21411872acac2f5636d6affe4aa765ec9da46bd81a4e6da83a93fb091a550ae0"
      },
      "protected_source_inputs": [
        {
          "path": "package-lock.json",
          "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
        },
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
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
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        },
        {
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/handoff.json",
          "sha256": "443b9b7ca75df66f7b9ac3ce210d85ba9a76a1e18b02c1c4c7a714e6f6f7f69a"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/independent-qa.report.json",
          "sha256": "7ddbcf2f7f1ad97ade71917ef4072d409ec8807fd3b1f00edb2fa1e1612ade5b"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/own-evidence-manifest.json",
          "sha256": "ebb3b5834629e1878659ae8f8a67f7e52ef5485062c407f55063f7c7a9cc036d"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "namacalathus",
          "batch": 85,
          "revision": "r002",
          "candidate_root": "production/small-life-batch85/namacalathus/r002",
          "source_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "reviewed_source_commit": "b727e577737d5108f5316ab898e8d7cbc4948f9f",
          "original_source_snapshot": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "review_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/namacalathus/batch85-20261021/release-metadata.json",
            "sha256": "261ec0a38573195dcc78266175d8ff910e908fdbc36e54546674cc0b8ce8c23b"
          },
          "candidate": {
            "path": "production/small-life-batch85/namacalathus/r002/candidate.json",
            "sha256": "565fb5087818c7703d6f611f8c64ec8e9cc8765d39ed3fde3aa9d3b2f73e3450"
          },
          "active_candidate": {
            "path": "production/small-life-batch85/namacalathus/r002/candidate.json",
            "sha256": "565fb5087818c7703d6f611f8c64ec8e9cc8765d39ed3fde3aa9d3b2f73e3450"
          },
          "original_profile": {
            "path": "production/small-life-batch85/namacalathus/r002/profile-contract.json",
            "sha256": "209cd7b1d124f82491613a629fa17a8fd37b8a791130fcf29fe2e4d6ce4701a2"
          },
          "active_profile": {
            "path": "production/small-life-batch85/namacalathus/r002/profile-contract.json",
            "sha256": "209cd7b1d124f82491613a629fa17a8fd37b8a791130fcf29fe2e4d6ce4701a2"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-85/independent-qa.report.json",
            "sha256": "7ddbcf2f7f1ad97ade71917ef4072d409ec8807fd3b1f00edb2fa1e1612ade5b"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-85/independent-qa.report.json",
            "sha256": "7ddbcf2f7f1ad97ade71917ef4072d409ec8807fd3b1f00edb2fa1e1612ade5b"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-85/independent-qa.report.json",
              "sha256": "7ddbcf2f7f1ad97ade71917ef4072d409ec8807fd3b1f00edb2fa1e1612ade5b"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-85/own-evidence-manifest.json",
              "sha256": "ebb3b5834629e1878659ae8f8a67f7e52ef5485062c407f55063f7c7a9cc036d"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-85/handoff.json",
              "sha256": "443b9b7ca75df66f7b9ac3ce210d85ba9a76a1e18b02c1c4c7a714e6f6f7f69a"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch85/namacalathus/r002/artifacts/metadata.json",
            "sha256": "f16675631238c233a477bde03527ad656522728bdf9835a7b60d957013e00978"
          },
          "source_counts": {
            "path": "production/small-life-batch85/namacalathus/r002/qa/authored-evaluated-counts.json",
            "sha256": "35a19366f6e919b75690481dacaa30a3e94f6c9deba5cdf1fb6091723da286e6"
          },
          "proof": {
            "path": "production/small-life-batch85/namacalathus/r002/views/render-manifest.json",
            "sha256": "694f2ae600b3eeb9f34c5186a682d22e0726df85443ffbc9b1c2cfa7e41034c7"
          },
          "source_preview": {
            "path": "production/small-life-batch85/namacalathus/r002/views/hero.png",
            "sha256": "e90a68fb7299f84ff04ae8eec34b45c025530db85291494f9257b281ee32fe4a"
          },
          "capture_reference": {
            "path": "assets/additions/namacalathus/batch85-20261021/namacalathus.png",
            "sha256": "88c49d78bb2efb89a08ebfe9cf12838d3ae04c28ddb4248eabad0ea1a59b3276"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/namacalathus.json",
            "sha256": "a9845861759601ad6a933f737081c5676b3037851732c663a6fadefcdbd47410"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch85/concepts/namacalathus-concept.png",
          "sha256": "574055750cd4d76c4446eeab3d3a1d0fe355c3b46b195b773a4e573264190c27",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/concepts/namacalathus-prompt.txt",
          "sha256": "4a8ab63ab6c247f72da47ec1275ad5e5e5856dbc4231c2671ac41842b2baa9ad",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/dependencies.json",
          "sha256": "e002694c4e45102aacd4ee2ef6d67f55eb81cef078a74da3af1eb7ef6b5e87c4",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r001/references.json",
          "sha256": "eb17d51c14565902230ffa07249019382116663ec7c62982e2394ca71becffbf",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/artifacts/metadata.json",
          "sha256": "f16675631238c233a477bde03527ad656522728bdf9835a7b60d957013e00978",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/artifacts/namacalathus.blend",
          "sha256": "2ccf174a94f5dc736ef7c7d06b8dd091ce75b3f4fba22b7ce60b3107b6507374",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/artifacts/namacalathus.glb",
          "sha256": "451b4bbb7006fb7f207466590d0fe01165a185fe91f0cb28af129776de600169",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/candidate.json",
          "sha256": "565fb5087818c7703d6f611f8c64ec8e9cc8765d39ed3fde3aa9d3b2f73e3450",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/config.json",
          "sha256": "b1936973a5a870fa2c18d78e1c46a71917ea1684685b41571c576b69da438512",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/delivery-brief.json",
          "sha256": "04d5dbee592cb08c7567fd10a787394bcb9da341eea15946163642e00551c1d9",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/profile-contract.json",
          "sha256": "209cd7b1d124f82491613a629fa17a8fd37b8a791130fcf29fe2e4d6ce4701a2",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/qa/authored-evaluated-counts.json",
          "sha256": "35a19366f6e919b75690481dacaa30a3e94f6c9deba5cdf1fb6091723da286e6",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/qa/runtime-parse.report.json",
          "sha256": "a9180f8f8e0c02fb836f04d9cf3d371b5bad76390351a7f4a6dec580b0f85878",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/qa/technical.report.json",
          "sha256": "d6c6f876e80e661a11a862002792ac2cc8a4743324ab0eff43d3aae25aa61597",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/views/clay.png",
          "sha256": "1ccb7860f43a4f59c74ac3561456165f8bf04da18989165212c6af6362fe59e8",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/views/front.png",
          "sha256": "a42b9fd5d6163c6d522e9edec5655133c7db543b7e5fc058ce456a969dae7817",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/views/hero.png",
          "sha256": "e90a68fb7299f84ff04ae8eec34b45c025530db85291494f9257b281ee32fe4a",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/views/rear.png",
          "sha256": "73358f2c77145acbc6471d18ab29faf82cb9c33efa2981da6a26d86793c2be57",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/views/render-manifest.json",
          "sha256": "694f2ae600b3eeb9f34c5186a682d22e0726df85443ffbc9b1c2cfa7e41034c7",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/views/reversehero.png",
          "sha256": "09f6b933a5b37d82c8f0f7d25fb7893005828d7bc0a5255c141c7d3d17f1b0de",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/views/side.png",
          "sha256": "9b60387d9f54f649d8fd1f8b382c67f977006dfd4c7b9f7fa4d11153a7af63f0",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/views/silhouette.png",
          "sha256": "d613e56fea6156db1f0d80e415698a101e2a20e40dc1d1a7c932b6648d2ff4a2",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/namacalathus/r002/views/top.png",
          "sha256": "24e5d802bf0801121d7bb8f409338d03308722806bf8cd953359eb03fb644c19",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/tools/generate.py",
          "sha256": "5284f9b71635197b870cc0262020d6c2bdcabe3002589b92f8e4829a6dfc5112",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/tools/parse.cjs",
          "sha256": "813bbe4ebbfc1cd80b2d45075f34a43bab68989991e3f81a0858a76c88a790d5",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "production/small-life-batch85/tools/render.py",
          "sha256": "dce6084f0ec6663a5ca5acd3f5815f128314c4e2c94c04748be153ed75c6879e",
          "origin": "source",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/REPORT.md",
          "sha256": "9e643a7b30aca1ad36e78e85ed1066a1a9b0f00c2dcd9dfdb3c3725f66d6d6d4",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/audit_inputs.py",
          "sha256": "0444dbb14d703080c07026d10ddbe7dc92d57a8f83f6bbf4ebcf4bc9dce6e651",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/finalize_report.py",
          "sha256": "47515d493c37c607b3eb7edc7f9cb7cc0443e5315848bd24f39728c524bdb390",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/handoff.json",
          "sha256": "443b9b7ca75df66f7b9ac3ce210d85ba9a76a1e18b02c1c4c7a714e6f6f7f69a",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/independent-qa.report.json",
          "sha256": "7ddbcf2f7f1ad97ade71917ef4072d409ec8807fd3b1f00edb2fa1e1612ade5b",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/measure_parameters.py",
          "sha256": "52c1ab37bc295503fc1adb2ae02c8a8d900a59804a726e114474097b7189361b",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/own-evidence-manifest.json",
          "sha256": "ebb3b5834629e1878659ae8f8a67f7e52ef5485062c407f55063f7c7a9cc036d",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/run_fresh_checks.py",
          "sha256": "11d979966aad747dc641642a526c42047c470628b43337879df33092c4cc6884",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/runtime_checks.mjs",
          "sha256": "371ae17ff73ce9bc222da8d7a6adc2ce4dc42ca0b45742ec6ee50dd73f8df5f4",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-85/source_reexport.py",
          "sha256": "f49bf8c6e5e352210516de82fee98d86fd32c91a39e264cf0bfb38fb458e8b98",
          "origin": "review",
          "owner": "namacalathus"
        },
        {
          "path": "qa/next52-g07-release-20261021/process-archive-index.json",
          "sha256": "90eaa5be32b3f8e2ec08a6b42f952dc00e4ead191632fa6113757ac1a96d08b2",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g08-20261021.json",
      "sha256": "c59b7109b0aae560fd9e5e5d0f80cc2b62e8c45de60a200ccc91e5b315488380"
    },
    "release": {
      "version": 1,
      "scope": "next52-g08-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
      "review_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g08-release-20261021/source-bundle.json",
        "sha256": "e9018767ef55009a974f218b4c1bd93c332599c4f0927a3e172dd223f8b77017"
      },
      "protected_source_inputs": [
        {
          "path": "package-lock.json",
          "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
        },
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "production/small-life-batch85/concepts/karst-polje-concept.png",
          "sha256": "dc5f7557e08105790c683ef8541c251213de37203e9197707f787a851ce67892"
        },
        {
          "path": "production/small-life-batch85/concepts/karst-polje-prompt.txt",
          "sha256": "44029cfb5bf96c667dc564337df06b3aecc4a3da200d2cde9d6df30bc753bde8"
        },
        {
          "path": "production/small-life-batch85/concepts/karst-polje-receipt.json",
          "sha256": "829bd7f4e60bbe7edf32b2708c2853cf019034525ac91cc7a33456edf323590c"
        },
        {
          "path": "production/small-life-batch85/concepts/lava-channel-concept.png",
          "sha256": "c3aadee240fe9a6c5680cb517076ba2a95e1fd521b097609042ff6bc3e60f899"
        },
        {
          "path": "production/small-life-batch85/concepts/lava-channel-prompt.txt",
          "sha256": "27dd3673e58cb046d8d3d8831cea2ad44d2814c706d1ca47fb2e4a22dcaa9e83"
        },
        {
          "path": "production/small-life-batch85/concepts/lava-channel-receipt.json",
          "sha256": "37456c009816b5b9a745b04177c40409e8cc8c54e8472fb6b594de36d47e7c5f"
        },
        {
          "path": "production/small-life-batch85/concepts/piedmont-glacier-concept.png",
          "sha256": "8edaf6049be5bcd875ed429a68481670d7259374c34833a6e5941d290d254f4a"
        },
        {
          "path": "production/small-life-batch85/concepts/piedmont-glacier-prompt.txt",
          "sha256": "2e4551433c7a945d182d15afb299b2bd3227ec0ec17b6989badb51e079e34be9"
        },
        {
          "path": "production/small-life-batch85/concepts/piedmont-glacier-receipt.json",
          "sha256": "ce1760e7d7769454dda8f04cf419723b3a14c19ed579c888ab7b6b07b7ae70b4"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
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
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        },
        {
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/handoff.json",
          "sha256": "13d8564c0e9a5c414aa0f7839501de084eafbde3631fa8142b8119360cd46b34"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
          "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/own-evidence-manifest.json",
          "sha256": "6857f24490d8911c71aa3940b351a2469428f851b03907a3aa02652117aa0b2c"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "karst-polje",
          "batch": 85,
          "revision": "r003",
          "candidate_root": "production/small-life-batch85-height-repair/karst-polje/r003",
          "source_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "reviewed_source_commit": "459054688a9d501f8e024b6ebbd1179cbda57c26",
          "original_source_snapshot": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "review_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/karst-polje/batch85-20261021/release-metadata.json",
            "sha256": "6c75fcfd8962c32fdd4a405dec9c9089bc036a01fef9121e50dea3da412a2ba0"
          },
          "candidate": {
            "path": "production/small-life-batch85-height-repair/karst-polje/r003/candidate.json",
            "sha256": "a2223b3b8e1af523ea5ded7ca711ce8bd806f58fc47dac23a1d5b00a326abecd"
          },
          "active_candidate": {
            "path": "production/small-life-batch85-height-repair/karst-polje/r003/candidate.json",
            "sha256": "a2223b3b8e1af523ea5ded7ca711ce8bd806f58fc47dac23a1d5b00a326abecd"
          },
          "original_profile": {
            "path": "production/small-life-batch85-height-repair/karst-polje/r003/profile-contract.json",
            "sha256": "bc8d48fbfe28987755c9c9ab9d4ff35a3322d77eb0df64fa3c6afc7cde4708af"
          },
          "active_profile": {
            "path": "production/small-life-batch85-height-repair/karst-polje/r003/profile-contract.json",
            "sha256": "bc8d48fbfe28987755c9c9ab9d4ff35a3322d77eb0df64fa3c6afc7cde4708af"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
            "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
            "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
              "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/own-evidence-manifest.json",
              "sha256": "6857f24490d8911c71aa3940b351a2469428f851b03907a3aa02652117aa0b2c"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/handoff.json",
              "sha256": "13d8564c0e9a5c414aa0f7839501de084eafbde3631fa8142b8119360cd46b34"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch85-height-repair/karst-polje/r003/artifacts/metadata.json",
            "sha256": "3b0ca121d7bcc5c5d34f3b6c2ab5bd4bd223368360fa0e104e7687b9fa955685"
          },
          "source_counts": {
            "path": "production/small-life-batch85-height-repair/karst-polje/r003/qa/authored-evaluated-counts.json",
            "sha256": "373c4140b660584d5ee92730c1c48d7af875b53c93cf6bb1cb9b5c292e5fccb7"
          },
          "proof": {
            "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/render-manifest.json",
            "sha256": "2a0cd6b9c299d6e7ee00629f6eb5090585b4cdd02ec4518fc3e31dfd7a1102d5"
          },
          "source_preview": {
            "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/hero.png",
            "sha256": "f2d04651be42c4305dd033fd3ee396425f71c36b0099dcca7e88e93c8564ea13"
          },
          "capture_reference": {
            "path": "assets/additions/karst-polje/batch85-20261021/karst-polje.png",
            "sha256": "3164062b26f7b01dc5a4e17c589e63748f51faf863a42b461c7251e8f0d86131"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/karst-polje.json",
            "sha256": "c3032d552109d9bf4fcbd05e28fec38a3afb082ca03ecf81c9b21fef9b47100f"
          }
        },
        {
          "id": "lava-channel",
          "batch": 85,
          "revision": "r003",
          "candidate_root": "production/small-life-batch85-height-repair/lava-channel/r003",
          "source_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "reviewed_source_commit": "459054688a9d501f8e024b6ebbd1179cbda57c26",
          "original_source_snapshot": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "review_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/lava-channel/batch85-20261021/release-metadata.json",
            "sha256": "8581f399734af398cb83ac0de28d3aea4139c212ece2ed97244cbd9df28da433"
          },
          "candidate": {
            "path": "production/small-life-batch85-height-repair/lava-channel/r003/candidate.json",
            "sha256": "3d6284987649eaaf1cf801dec30084899d48547be5386d9736756120e9a01359"
          },
          "active_candidate": {
            "path": "production/small-life-batch85-height-repair/lava-channel/r003/candidate.json",
            "sha256": "3d6284987649eaaf1cf801dec30084899d48547be5386d9736756120e9a01359"
          },
          "original_profile": {
            "path": "production/small-life-batch85-height-repair/lava-channel/r003/profile-contract.json",
            "sha256": "e67c47f79af8e8a68f5dc41052a75602cb16599110b55ddf5af5a49a489c055f"
          },
          "active_profile": {
            "path": "production/small-life-batch85-height-repair/lava-channel/r003/profile-contract.json",
            "sha256": "e67c47f79af8e8a68f5dc41052a75602cb16599110b55ddf5af5a49a489c055f"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
            "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
            "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
              "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/own-evidence-manifest.json",
              "sha256": "6857f24490d8911c71aa3940b351a2469428f851b03907a3aa02652117aa0b2c"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/handoff.json",
              "sha256": "13d8564c0e9a5c414aa0f7839501de084eafbde3631fa8142b8119360cd46b34"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch85-height-repair/lava-channel/r003/artifacts/metadata.json",
            "sha256": "1f9b48208a80770acf5c33ad869d148a09c1a53bc980023a0585bd03c179f8b5"
          },
          "source_counts": {
            "path": "production/small-life-batch85-height-repair/lava-channel/r003/qa/authored-evaluated-counts.json",
            "sha256": "a4c824b3177740e11270ee64e78f0990d9526f2a2712f46cc31b8bcccaacc22b"
          },
          "proof": {
            "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/render-manifest.json",
            "sha256": "39859fda8174d183de4f4a35cedb9e296eaa93d8d7ab0bf696cc74eacb1fcd76"
          },
          "source_preview": {
            "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/hero.png",
            "sha256": "e713887307dacc19c03b0c30092495471567f1fcfe71f004ecc12520d0bbc73a"
          },
          "capture_reference": {
            "path": "assets/additions/lava-channel/batch85-20261021/lava-channel.png",
            "sha256": "a0e4592e3e4db0bd465bbe8ceb81a38a40f06751617d8a0456329fe0271368ec"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/lava-channel.json",
            "sha256": "264f888538b0c43159c23f59f90401ac465e55160c4f30c1860a6879ffc939c8"
          }
        },
        {
          "id": "piedmont-glacier",
          "batch": 85,
          "revision": "r005",
          "candidate_root": "production/small-life-batch85-height-repair/piedmont-glacier/r005",
          "source_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "reviewed_source_commit": "459054688a9d501f8e024b6ebbd1179cbda57c26",
          "original_source_snapshot": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "review_commit": "4eeb65eb2796a5543067e3df18c52467512dfdc5",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/piedmont-glacier/batch85-20261021/release-metadata.json",
            "sha256": "ffb7d2186aba725cccb19170200530e67391cd079a002c56e86abfd17ace8adf"
          },
          "candidate": {
            "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/candidate.json",
            "sha256": "7ca983d477945ebafdcd439e4162314eb0f41d05f9ad91ca76d36f26abedc87c"
          },
          "active_candidate": {
            "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/candidate.json",
            "sha256": "7ca983d477945ebafdcd439e4162314eb0f41d05f9ad91ca76d36f26abedc87c"
          },
          "original_profile": {
            "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/profile-contract.json",
            "sha256": "6c5dc93f84e920a17e9537b71669f038d4c6fb5eb3b033c9dc018d15f9b8ccec"
          },
          "active_profile": {
            "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/profile-contract.json",
            "sha256": "6c5dc93f84e920a17e9537b71669f038d4c6fb5eb3b033c9dc018d15f9b8ccec"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
            "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
            "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
              "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/own-evidence-manifest.json",
              "sha256": "6857f24490d8911c71aa3940b351a2469428f851b03907a3aa02652117aa0b2c"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/handoff.json",
              "sha256": "13d8564c0e9a5c414aa0f7839501de084eafbde3631fa8142b8119360cd46b34"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/artifacts/metadata.json",
            "sha256": "0b95ff654962f39822b739d922fedce816b396a4224fb167ee5e953ebf74a5dc"
          },
          "source_counts": {
            "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/qa/authored-evaluated-counts.json",
            "sha256": "bdc175407dc3399c0d835761c9a2a58560482f7d03e9a0096cd67c83bda3716e"
          },
          "proof": {
            "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/render-manifest.json",
            "sha256": "1b0bdbf827efb096013c498fd589ddaca05e3eaf8358e6c4086a1ff7551bb696"
          },
          "source_preview": {
            "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/hero.png",
            "sha256": "005038d306d2a8b5bcc65bf91de197c935254c8013f0e7204b89896ca4045179"
          },
          "capture_reference": {
            "path": "assets/additions/piedmont-glacier/batch85-20261021/piedmont-glacier.png",
            "sha256": "fb873390044bb4f4f43ee931b8a7bbec6de727470026149a0656f1a80879bb15"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/piedmont-glacier.json",
            "sha256": "3b75a7e691e531d5af97532c4137863eaab1ffbaf6badff30e96504175fdd731"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch85-height-repair/dependencies.json",
          "sha256": "3d17758576d75a5dc11da7f51b3912741d3872b60d7071ebde349147f7e71d69",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/artifacts/karst-polje.blend",
          "sha256": "3fa38d62fe1665955bdfe12078be0aa29a6926955039afe4411ff5b350fc2db9",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/artifacts/karst-polje.glb",
          "sha256": "40ec03951b3bc0a390344c5577f8dc81beebff352933cea63c81b6c64b49a2c7",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/artifacts/metadata.json",
          "sha256": "3b0ca121d7bcc5c5d34f3b6c2ab5bd4bd223368360fa0e104e7687b9fa955685",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/candidate.json",
          "sha256": "a2223b3b8e1af523ea5ded7ca711ce8bd806f58fc47dac23a1d5b00a326abecd",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/config.json",
          "sha256": "64df56738e64813338002ad3fa3e61e4b585d15651ee71a44c37e28daf6993b3",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/delivery-brief.json",
          "sha256": "18c5a9e5681a88576ea1207565682ec8ee5dea728cb5e9b2334225ea578fa891",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/profile-contract.json",
          "sha256": "bc8d48fbfe28987755c9c9ab9d4ff35a3322d77eb0df64fa3c6afc7cde4708af",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/qa/authored-evaluated-counts.json",
          "sha256": "373c4140b660584d5ee92730c1c48d7af875b53c93cf6bb1cb9b5c292e5fccb7",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/qa/runtime-parse.report.json",
          "sha256": "533fc4da522a8834c0109ab9ba451e9028fd4f5a2943420fbd59d05b20e74509",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/qa/technical.report.json",
          "sha256": "515038b7ef1c4e6847360dde469f290e1b27cd549985025cda5ffc907e5c9457",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/references.json",
          "sha256": "fd90a8906886e838c424ecad410699ecbeeebb1035f038ec9b1dca4858d1a214",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/clay.png",
          "sha256": "fde3e781c46ae241fd550e67e10fe6fb0778f359b9f1fe9dea157e2c7b291553",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/front.png",
          "sha256": "2281f5ae3c73ffe4177e65c1442a47e6d8d10ef58625fddaa0a59cfba4b024d8",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/hero.png",
          "sha256": "f2d04651be42c4305dd033fd3ee396425f71c36b0099dcca7e88e93c8564ea13",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/rear.png",
          "sha256": "ab5876031874c4d13daff594179959f1d194a2827f272e16ba01e6ea6384b4d5",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/render-manifest.json",
          "sha256": "2a0cd6b9c299d6e7ee00629f6eb5090585b4cdd02ec4518fc3e31dfd7a1102d5",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/reversehero.png",
          "sha256": "83f8dca08aae1811da4272fe6f227e7d81ec415af63b0323d5063a3531f55a56",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/side.png",
          "sha256": "0be9e9c98ebc8efc341a0d77e22446dd4b7886d727d1840856f88e83343e54f4",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/silhouette.png",
          "sha256": "27af3782ea8638c574a7fdf9e5eaab07d741c33f5a390b31a0b9ca038e64393e",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/karst-polje/r003/views/top.png",
          "sha256": "47e28766f57586009dc9426440c9ef22b4013fdddf8622186e201777f98838d8",
          "origin": "source",
          "owner": "karst-polje"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/artifacts/lava-channel.blend",
          "sha256": "788edf508e8569c662a9e04512920180333720942d97feba76d465ac919c6e09",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/artifacts/lava-channel.glb",
          "sha256": "552dca8452372f2512e9eec4aa43e25111318a01187f04ad33d4146e19705eba",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/artifacts/metadata.json",
          "sha256": "1f9b48208a80770acf5c33ad869d148a09c1a53bc980023a0585bd03c179f8b5",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/candidate.json",
          "sha256": "3d6284987649eaaf1cf801dec30084899d48547be5386d9736756120e9a01359",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/config.json",
          "sha256": "c98368491f068dc61715ce2b499fa7dc45c7dedb7e7e21f071447d53e119f327",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/delivery-brief.json",
          "sha256": "b190a0eb74fb44d5e76f03698ce044f7066dd39683adbd6c8cf11dee853ce4d4",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/profile-contract.json",
          "sha256": "e67c47f79af8e8a68f5dc41052a75602cb16599110b55ddf5af5a49a489c055f",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/qa/authored-evaluated-counts.json",
          "sha256": "a4c824b3177740e11270ee64e78f0990d9526f2a2712f46cc31b8bcccaacc22b",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/qa/runtime-parse.report.json",
          "sha256": "05731562236cefb0b186ee70260b5f1cc330766d699ed76e415138573e16c4ee",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/qa/technical.report.json",
          "sha256": "5321706856786fd4309e252ba8fabd33920c172570aaa16a79368494500c6739",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/references.json",
          "sha256": "6b049e21e098df0f7f205345e5431073bc6ce42e1f8eae6afd59554316fd166f",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/clay.png",
          "sha256": "cfc3d9286a3457f56ea3b576351ee147c862486fb88f14fd90f65472444a1263",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/front.png",
          "sha256": "675bff46495d99755c438333ebb4fa643d11cc2f030980105ae7d63259ed4f11",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/hero.png",
          "sha256": "e713887307dacc19c03b0c30092495471567f1fcfe71f004ecc12520d0bbc73a",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/rear.png",
          "sha256": "8703dcb896e24c7d1d7af34ddbe2fc3e953d9bd5108f8f4101fefc00f7104996",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/render-manifest.json",
          "sha256": "39859fda8174d183de4f4a35cedb9e296eaa93d8d7ab0bf696cc74eacb1fcd76",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/reversehero.png",
          "sha256": "04d72c665fadedc2dd1963013c61436670d62310d80358e6839bd8abbb566217",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/side.png",
          "sha256": "a606a3670378863f168d2d61942695d96de8365f40c53fdbc2689bd8fa236628",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/silhouette.png",
          "sha256": "b843605455f32078e6f6909ec6881f213ce391558f1e3c6e2bc5f1573f5e38ca",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/lava-channel/r003/views/top.png",
          "sha256": "c43670fb5806ad7234c295db6f3b040e5b58bc115cf874f81955f8ae2b0733f5",
          "origin": "source",
          "owner": "lava-channel"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/artifacts/metadata.json",
          "sha256": "0b95ff654962f39822b739d922fedce816b396a4224fb167ee5e953ebf74a5dc",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/artifacts/piedmont-glacier.blend",
          "sha256": "03272197d50122e7c9ef178db753ec90159b416e2fcec98a05fc46f102fb9b8c",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/artifacts/piedmont-glacier.glb",
          "sha256": "454b7ae3b459daec6fc74fbb096c357e28dd59b0ab32f066789ac7dcc5242279",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/candidate.json",
          "sha256": "7ca983d477945ebafdcd439e4162314eb0f41d05f9ad91ca76d36f26abedc87c",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/config.json",
          "sha256": "1302dcccdd2230f4dbb561ca4476ad97dc75b046dcf722f289d3c954466a9de6",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/delivery-brief.json",
          "sha256": "de3242b3b08630b979ea9bebd23fd6d3e41a679944b5d67712701f4e954ca16e",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/profile-contract.json",
          "sha256": "6c5dc93f84e920a17e9537b71669f038d4c6fb5eb3b033c9dc018d15f9b8ccec",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/qa/authored-evaluated-counts.json",
          "sha256": "bdc175407dc3399c0d835761c9a2a58560482f7d03e9a0096cd67c83bda3716e",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/qa/runtime-parse.report.json",
          "sha256": "239b9874297dfa2727869e5208c1aa06e9226b1e456bff88aa3e98e1a28cee18",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/qa/technical.report.json",
          "sha256": "d7ea905fa77646d8760d012b6b39a64a9476072531f76276549aaebf0b79b92f",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/references.json",
          "sha256": "0ddff5668e94f79d74ac9b96b17c556551471a4aa87d397dde3a82df3151707f",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/clay.png",
          "sha256": "8966850aa69f284f5965b190f36f3a4957d8b1abc38887be7446a6dcc7d7d222",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/front.png",
          "sha256": "4733bb32fbb817b1f40752e56f03b811b45b1448f32976ad53c20a7c70bec551",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/hero.png",
          "sha256": "005038d306d2a8b5bcc65bf91de197c935254c8013f0e7204b89896ca4045179",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/rear.png",
          "sha256": "fe5a5b5a1c8c0f7fac876e51306cb5fbef38cfb7e5b1ba4dbbca4fc8ffe3ae90",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/render-manifest.json",
          "sha256": "1b0bdbf827efb096013c498fd589ddaca05e3eaf8358e6c4086a1ff7551bb696",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/reversehero.png",
          "sha256": "2a48ffff1b2be5e797eaa11c3de8fb716aca91747476b3a34e3f1719b5577f45",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/side.png",
          "sha256": "54255d938d76060bd6dc683cfadfa279e524f4339342e31d5262a592218b24e5",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/silhouette.png",
          "sha256": "d735e858db8d8f7be84dbc242b9f5b45a1e74a2a5f6acca9bd4edb15ee844f9d",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/piedmont-glacier/r005/views/top.png",
          "sha256": "49318eee90c8fa57eea0b22d98897cbe94ae1a8b19a89f2e5ecc9da0a71044cc",
          "origin": "source",
          "owner": "piedmont-glacier"
        },
        {
          "path": "production/small-life-batch85-height-repair/tools/generate.py",
          "sha256": "26751bae0a598103e71cfa6ea8a5ba5570949223ad99dd5dffb0ecefecb61e28",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch85-height-repair/tools/parse.cjs",
          "sha256": "813bbe4ebbfc1cd80b2d45075f34a43bab68989991e3f81a0858a76c88a790d5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch85-height-repair/tools/render.py",
          "sha256": "dce6084f0ec6663a5ca5acd3f5815f128314c4e2c94c04748be153ed75c6879e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch85-height-repair/tools/source_reexport.py",
          "sha256": "80cdd4c293e307c3181d1907f0994611042449860a95bc7e6a4c4a9c0e103bf7",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/REPORT.md",
          "sha256": "6148b9824429cc38b7cd55df0c912511e5d49533ed0952e7bfeebd4d0647e85a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/audit_inputs.py",
          "sha256": "a8670f427c07a7ce20a13ae54267e5b283d4779ec2c5492c2e497b968b1531b6",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/finalize_report.py",
          "sha256": "bf9542002f1e84f4f2b9ab95e36c0c90e20c2bf06220b64e22e7013d3b75be26",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/glb_difference.py",
          "sha256": "c29b8c1f501683d149395409434bffd7985b375913e876455cafdb0b08fcccb6",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/glb_logical_difference.py",
          "sha256": "e1a2d2d37e00a0b8f20a064338df5f1e9efe66aab953225dda3e72843ff0cf0e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/handoff.json",
          "sha256": "13d8564c0e9a5c414aa0f7839501de084eafbde3631fa8142b8119360cd46b34",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/independent-qa.report.json",
          "sha256": "de575cac4a6e81f5b9b1e1c5825410b40710d8f3b53ea79ecfc5fbe2e72f361e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/measure_parameters.py",
          "sha256": "3acc9aed98fc256a2cda60010e0d07850880cf75c7902419a74cad9459dd57c6",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/own-evidence-manifest.json",
          "sha256": "6857f24490d8911c71aa3940b351a2469428f851b03907a3aa02652117aa0b2c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/run_diffs.py",
          "sha256": "55432224aa409af263f8a56756609adf5a75ad4fbff9ee2d29dbfa1d9d9d4f36",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/run_fresh_checks.py",
          "sha256": "8bb97a4163e3e8e9bada2332fc22d287ddd008a2fab01d4590a243ebfa42c5df",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/runtime_checks.mjs",
          "sha256": "6cbbc7ade144ccffb57d9a696348958ab38d96f7296d5f735c2b0873ff898cff",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/source_diff.py",
          "sha256": "486fdc78500f8c1ade93f857675ac70cdc4ced76ba46207b84be0bfa74b273df",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-85-height-repair/source_reexport.py",
          "sha256": "f49bf8c6e5e352210516de82fee98d86fd32c91a39e264cf0bfb38fb458e8b98",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g08-release-20261021/process-archive-index.json",
          "sha256": "1f4b6cb5f484d5146c66c0196205e390a261ee02be8daa7286c966057c9a6752",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g09-20261021.json",
      "sha256": "1dd448167b5e249d95385b074a1d392ede987f3cbca25e19ea07629cfaf8ab93"
    },
    "release": {
      "version": 1,
      "scope": "next52-g09-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "52da64de4c4609b69bd4df22d634aa79fdfc4262",
      "review_commit": "52da64de4c4609b69bd4df22d634aa79fdfc4262",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g09-release-20261021/source-bundle.json",
        "sha256": "438bf65688d813ff2f721a6a42d2f1397f7f1a05822a48e2f852234ca5b05c1a"
      },
      "protected_source_inputs": [
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
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/OWN_QA_MANIFEST.json",
          "sha256": "7df099fc636f2fa71057d81aea6085e51bb08976473341d811c49cd1c3851786"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/handoff.json",
          "sha256": "342bba0fc3f4280a610b37f1145ff27d25352029bec9419a81ec0b65ec375d4e"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/report.md",
          "sha256": "b7be1c80bb41b02f7c8fd2a0e503b083b83626ea76c7165a0cd60fb8ccae8d40"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "ernietta",
          "batch": 77,
          "revision": "r012",
          "candidate_root": "production/batch77-ernietta-repair/assets/ernietta/r012",
          "source_commit": "52da64de4c4609b69bd4df22d634aa79fdfc4262",
          "reviewed_source_commit": "d1a3aa6a277908cd3aee66aa38e4d6dca818879b",
          "original_source_snapshot": "52da64de4c4609b69bd4df22d634aa79fdfc4262",
          "review_commit": "52da64de4c4609b69bd4df22d634aa79fdfc4262",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/ernietta/batch77-20261021/release-metadata.json",
            "sha256": "9ab46c533d9cdaf2265bfae38c5ba8986f3c1a4c57604e440c5a16e3c793b7c3"
          },
          "candidate": {
            "path": "production/batch77-ernietta-repair/assets/ernietta/r012/candidate.json",
            "sha256": "8a35e5654b9699793b71df4f4c77ced3f7a7481def419a96f35090c9b2ed88a7"
          },
          "active_candidate": {
            "path": "production/batch77-ernietta-repair/assets/ernietta/r012/candidate.json",
            "sha256": "8a35e5654b9699793b71df4f4c77ced3f7a7481def419a96f35090c9b2ed88a7"
          },
          "original_profile": {
            "path": "production/batch77-ernietta-repair/assets/ernietta/r012/profile-contract.json",
            "sha256": "e18158c20e62edaeda3c7546968b4986ce7abd8c22d970fcbe825e5d8ce251f1"
          },
          "active_profile": {
            "path": "production/batch77-ernietta-repair/assets/ernietta/r012/profile-contract.json",
            "sha256": "e18158c20e62edaeda3c7546968b4986ce7abd8c22d970fcbe825e5d8ce251f1"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/report.md",
            "sha256": "b7be1c80bb41b02f7c8fd2a0e503b083b83626ea76c7165a0cd60fb8ccae8d40"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/report.md",
            "sha256": "b7be1c80bb41b02f7c8fd2a0e503b083b83626ea76c7165a0cd60fb8ccae8d40"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/report.md",
              "sha256": "b7be1c80bb41b02f7c8fd2a0e503b083b83626ea76c7165a0cd60fb8ccae8d40"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/OWN_QA_MANIFEST.json",
              "sha256": "7df099fc636f2fa71057d81aea6085e51bb08976473341d811c49cd1c3851786"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/handoff.json",
              "sha256": "342bba0fc3f4280a610b37f1145ff27d25352029bec9419a81ec0b65ec375d4e"
            }
          ],
          "original_metrics": {
            "path": "production/batch77-ernietta-repair/assets/ernietta/r012/metrics.json",
            "sha256": "02bbc37b2d75c07707e0f2668e5ef241687aebef5b64bba4db39e2a80d76f7dd"
          },
          "source_counts": {
            "path": "production/batch77-ernietta-repair/assets/ernietta/r012/source-vertex-counts.json",
            "sha256": "e36250d7528296f19cf4a839ea24d3f1d456cedbbc8c78ca515ba234e12b3930"
          },
          "proof": {
            "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/render-manifest.json",
            "sha256": "4e61091e798ed8066b5462c6c9daf3d92ee37ba1f6919da6214783fbe3d1ddea"
          },
          "source_preview": {
            "path": "production/batch77-ernietta-repair/assets/ernietta/r012/preview.png",
            "sha256": "3fbfcb79f7d56ab51404fb52c3f085cbb3d83ec1f91d4b8fcf84f52d0680b074"
          },
          "capture_reference": {
            "path": "assets/additions/ernietta/batch77-20261021/ernietta.png",
            "sha256": "11c4d519cad399e7929b285e37aa39093861aeede45bd5b858530b0d90f0083a"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/ernietta.json",
            "sha256": "31099871b42daa99ecb47b0d760c29312d6f00405392b7e55b9c39301118139c"
          }
        }
      ],
      "files": [
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/LICENSES.md",
          "sha256": "3c85f1aad5eceac3b60086d91acb397df96d069ea57c39ea6805f6beea21aa1c",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/build-config.json",
          "sha256": "468955e0e3287c2b8bc0049c33e6b9400c70d3021bf01b21fded5cac703b6268",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/build-dependencies.json",
          "sha256": "5a814378cc976e50edb82c6623651cc5bb14d772ae591b3488c049da6a997deb",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/candidate-brief.json",
          "sha256": "75f0845911f1a92479081f7911f1714090df64779545623ddaa6cb5ecf80844b",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/candidate.json",
          "sha256": "8a35e5654b9699793b71df4f4c77ced3f7a7481def419a96f35090c9b2ed88a7",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/contact-sheet.png",
          "sha256": "c206df212ff373a56a62b068e4528dd5cdb3b2217b33b7b1c8df95526c416187",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/final-rebuild-binding.json",
          "sha256": "c3223c6f74eafbcb1c4445f3ad45551c81d41fd78f85c7a1e1af866a215122a5",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/generator.py",
          "sha256": "d9c1c204512632e44c35bd2ae1336b90307f1e96b8d374c7e43889f8469e1c18",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/gltf-validator.report.json",
          "sha256": "bf8cb1368a618c2e7e613cca325e587944e36bb467bac76bc80101691a491ae3",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/lifecycle.jsonl",
          "sha256": "3b57fca9c85893c63f677a5a04ac56dea9f4fd71447befa867dc4628b841eea4",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/maker-review.md",
          "sha256": "c102d63f1ab2c09469e5a944eef7cbbe06fddba9583de32ab09741cd78932f07",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/metrics.json",
          "sha256": "02bbc37b2d75c07707e0f2668e5ef241687aebef5b64bba4db39e2a80d76f7dd",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/model.glb",
          "sha256": "72b30dfed8b7786a357e63102bd36ff26007cfb45af28923c6393b7314018e6b",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/physical-surfaces.report.json",
          "sha256": "43e653b5c1a7ca2a31528acb47af8e9bb85679d0d1de8e3eb2817985c96c4b98",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/pixel-inspection.json",
          "sha256": "8a842091330b4a58f432b6c9149281072e2c58ddc63aa8fd73ec856cfc680053",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/preproof-binding.json",
          "sha256": "88c97eaa43bb52f38f4d04d0d31a8ea7108632520d60f34db5e68cecf8adb3b0",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/preview.png",
          "sha256": "3fbfcb79f7d56ab51404fb52c3f085cbb3d83ec1f91d4b8fcf84f52d0680b074",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/profile-contract.json",
          "sha256": "e18158c20e62edaeda3c7546968b4986ce7abd8c22d970fcbe825e5d8ce251f1",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/clay.png",
          "sha256": "0990951a3feffcf2f2782d384aff93e7da5e4f90901527bb7ee10161aa09040e",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/front.png",
          "sha256": "123e7243445278402d8301cdc0a6f3000f4d500d691290b3822b8456f1305dae",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/hero.png",
          "sha256": "3fbfcb79f7d56ab51404fb52c3f085cbb3d83ec1f91d4b8fcf84f52d0680b074",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/rear.png",
          "sha256": "c1d187b4deb953bb6d8419f6785d65d8deee1a0931f342aa9cde5fc5e739965f",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/render-manifest.json",
          "sha256": "4e61091e798ed8066b5462c6c9daf3d92ee37ba1f6919da6214783fbe3d1ddea",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/reversehero.png",
          "sha256": "b3a73c4977b8709265b32d31866fa5ee67b73469bdc8671de0cd7d9f3f97d47c",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/side.png",
          "sha256": "9fa1e8b1cd1e1090aa9e62d3c3de9a5e6446f8332af546a9f00fadad790d8aab",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/silhouette.png",
          "sha256": "09356d41975c7c891334e2ce53722431ba3dcefe4b2fed6a362f8fde531de080",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/proof-final/top.png",
          "sha256": "d6f65bba118f9b5ef1d29b084ddc4f73894ac257e5fafb8f2d75a9aea2621bcf",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/references.json",
          "sha256": "1d9e1f03ee1c23190ff5c533f5494ec1250331a3c1162444dc23467b278f6f3b",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/repair-revision-intent.json",
          "sha256": "03bbd76e1cc477b284ff90606b8c4cd78d4bdd6f0148765d9f2a8c2fc7f29eb9",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/repro-final-1.report.json",
          "sha256": "240767dc66b10adca6a0a06dc609fe2edf8fc5bcd9621b642916c9dbe2ffc941",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/repro-final-2.report.json",
          "sha256": "e7c72da0c6fafb13525c6e895db93206c14a2e71a47d2938304278d39c914b9d",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/runtime-parse.report.json",
          "sha256": "64a0cab7135c192d50a826e4c3d2d06c85eaa66da87eb1a21449267012bb32fe",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/source-final.report.json",
          "sha256": "92eec30072841d67f24b68fa336971146e11ccd01e554cc44a342a9de158306a",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/source-metrics.json",
          "sha256": "0efcc0eace0cd08e138d0f3e006db90300e446fbe43b9d72f8567f53d25ca89d",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/source-vertex-counts.json",
          "sha256": "e36250d7528296f19cf4a839ea24d3f1d456cedbbc8c78ca515ba234e12b3930",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/assets/ernietta/r012/source.blend",
          "sha256": "41851d81db91af4808dad70bd26bc21dedf88fe4378df69f038ca4c91d8225e3",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/check-physical-surfaces.py",
          "sha256": "397b55d50000b5556c37aa502659b2c045a80ba0c5204342bf6f10eb2f02b8ad",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/complete-final.py",
          "sha256": "3c5da8b7785b399145e9991333a202eb02f9354a180b555f98d3f17cc77c6f3d",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/count-source-vertices.py",
          "sha256": "9211091a8a90fdac820ae374478c7f4b28fe1e799a03b764f69aff7aba23c21f",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/original-freeze/concept-original.png",
          "sha256": "83e71efc37cd370eb76008b75220a56c48c4f2a0ac0a927abcc44c58d3352a5c",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/original-freeze/concept-prompt.txt",
          "sha256": "e73aa5153313bd125c39810f07575308e83b96c22a8d65ce1425ac47437f13d7",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/package-final.py",
          "sha256": "54df2bb3c4c1ab6ac34bc257aa359cba6eb9c493e30d4d2c44249a99b3919fe7",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/publication-policy-reference.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/rebuild-final.sh",
          "sha256": "c0a8fbe30c6fd601f19173f0abd1defbf5b9a2a1e890d8ae93fe316cef189fe2",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/render-fixed8.py",
          "sha256": "e3654a0abb9bc8848e52fdf0c37c53ff34396aa876ab5a7ae0bc004607083058",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "production/batch77-ernietta-repair/runtime-parse.mjs",
          "sha256": "fb938eb6db606a51b904de3f58b2557b618fc5963bfcf225ad990b0b1244164c",
          "origin": "source",
          "owner": "ernietta"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/OWN_QA_MANIFEST.json",
          "sha256": "7df099fc636f2fa71057d81aea6085e51bb08976473341d811c49cd1c3851786",
          "origin": "review",
          "owner": "ernietta"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/fresh-validate.mjs",
          "sha256": "5b1a7ffe37fc479972b1d01b7eb3b1fd6b24e8e0f3636e4dc271f0084f263b2f",
          "origin": "review",
          "owner": "ernietta"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/handoff.json",
          "sha256": "342bba0fc3f4280a610b37f1145ff27d25352029bec9419a81ec0b65ec375d4e",
          "origin": "review",
          "owner": "ernietta"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/integrity.py",
          "sha256": "68d42d01e36cc45d2498dd9f88d3156ed6af96494fcaad9ff46106943e04e091",
          "origin": "review",
          "owner": "ernietta"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/reopen-diff.py",
          "sha256": "6b85e2aa9d812a61b45603e761433259b658374eefa86fdc49062863306cebe3",
          "origin": "review",
          "owner": "ernietta"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch77-ernietta-r012/report.md",
          "sha256": "b7be1c80bb41b02f7c8fd2a0e503b083b83626ea76c7165a0cd60fb8ccae8d40",
          "origin": "review",
          "owner": "ernietta"
        },
        {
          "path": "qa/next52-g09-release-20261021/process-archive-index.json",
          "sha256": "a0a97ab32b1b69dfcbc9ecda7adcff5eeb74895304b3509d769061f1e3a08417",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g10-20261021.json",
      "sha256": "9ec780fc43b1fcf5e44e167ad6ef37534be5aa3b62c6ffbac30a782baaed694d"
    },
    "release": {
      "version": 1,
      "scope": "next52-g10-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
      "review_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g10-release-20261021/source-bundle.json",
        "sha256": "a26b6ad8d1b3ccacae29a5b129a2a787d0b4f329a895e37ba93a93c148b7eb3d"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
        },
        {
          "path": "scripts/qa_glb.py",
          "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/HANDOFF.md",
          "sha256": "332ff82af9f71577a4e0e3944b3cc75ca211eadac4193ff8b37a3a56e8e4e79a"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
          "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/ownmanifest.json",
          "sha256": "b1f7c81210a40d6ebcd15e720e25fc722c100b4f5c7ac6e400665636af3713cd"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "caytonia",
          "batch": 92,
          "revision": "r002",
          "candidate_root": "production/batch92/assets/caytonia/r002",
          "source_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "reviewed_source_commit": "37ddf403430e4859d077163855ecdf6e1aa2b0ba",
          "original_source_snapshot": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "review_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/caytonia/batch92-20261021/release-metadata.json",
            "sha256": "f8446eb273241ddd6d1741fce689abef4b44363263b8494750cc0a41b503d1d4"
          },
          "candidate": {
            "path": "production/batch92/assets/caytonia/r002/candidate.json",
            "sha256": "8a8135e40a6a4906ee066d7f67ca4b79b3a9bdd783449c796142850013c6b98d"
          },
          "active_candidate": {
            "path": "production/batch92/assets/caytonia/r002/candidate.json",
            "sha256": "8a8135e40a6a4906ee066d7f67ca4b79b3a9bdd783449c796142850013c6b98d"
          },
          "original_profile": {
            "path": "production/batch92/assets/caytonia/r002/profile-contract.json",
            "sha256": "f2e60080daa3ba7e2afe68124a6c052027abf1500ab5952275fa2803297ec1d9"
          },
          "active_profile": {
            "path": "production/batch92/assets/caytonia/r002/profile-contract.json",
            "sha256": "f2e60080daa3ba7e2afe68124a6c052027abf1500ab5952275fa2803297ec1d9"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
            "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
            "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
              "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/ownmanifest.json",
              "sha256": "b1f7c81210a40d6ebcd15e720e25fc722c100b4f5c7ac6e400665636af3713cd"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/HANDOFF.md",
              "sha256": "332ff82af9f71577a4e0e3944b3cc75ca211eadac4193ff8b37a3a56e8e4e79a"
            }
          ],
          "original_metrics": {
            "path": "production/batch92/assets/caytonia/r002/metrics.json",
            "sha256": "742bdae3780475c05d355e40660e60237f207a618e3b9b3af40324248a20a085"
          },
          "source_counts": {
            "path": "production/batch92/assets/caytonia/r002/source-vertex-counts.json",
            "sha256": "13b173471077fe0eca1d88ae8f65c3b64f2c152ef314ebe6a37e39a2ee948c3c"
          },
          "proof": {
            "path": "production/batch92/assets/caytonia/r002/proof-final/render-manifest.json",
            "sha256": "cf31d5da8698f3344617af0739e48536ed6cbe9d765ddd379bff07994089769f"
          },
          "source_preview": {
            "path": "production/batch92/assets/caytonia/r002/preview.png",
            "sha256": "279aa5326eb67b7a36804f2411cfde55c8f5b5f4bc5e61b930594c23fa663403"
          },
          "capture_reference": {
            "path": "assets/additions/caytonia/batch92-20261021/caytonia.png",
            "sha256": "c478e9fed9e0e5faa9e13ebbc3c5807b86ad4b975fe0c1f516379eaac52b2f83"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/caytonia.json",
            "sha256": "34c593a7eec90acebabbd869e00a7eadd8d6c86e1bdcf838a54520d8cac1d2c5"
          }
        },
        {
          "id": "eophyllophyton",
          "batch": 92,
          "revision": "r004",
          "candidate_root": "production/batch92/assets/eophyllophyton/r004",
          "source_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "reviewed_source_commit": "37ddf403430e4859d077163855ecdf6e1aa2b0ba",
          "original_source_snapshot": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "review_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/eophyllophyton/batch92-20261021/release-metadata.json",
            "sha256": "e2053b94688ffa6caa39fafbb605ff57ec02fa73a1563d090be609d8502c64a0"
          },
          "candidate": {
            "path": "production/batch92/assets/eophyllophyton/r004/candidate.json",
            "sha256": "40e2cb3c7ae88b6758b93746d9106a9e7a73150c02ef41db4af0f68f4fb1e7c5"
          },
          "active_candidate": {
            "path": "production/batch92/assets/eophyllophyton/r004/candidate.json",
            "sha256": "40e2cb3c7ae88b6758b93746d9106a9e7a73150c02ef41db4af0f68f4fb1e7c5"
          },
          "original_profile": {
            "path": "production/batch92/assets/eophyllophyton/r004/profile-contract.json",
            "sha256": "55e774611a17f8d91ecdcfb386808f081c3d013023a4fe4653c0d7fc273dcef1"
          },
          "active_profile": {
            "path": "production/batch92/assets/eophyllophyton/r004/profile-contract.json",
            "sha256": "55e774611a17f8d91ecdcfb386808f081c3d013023a4fe4653c0d7fc273dcef1"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
            "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
            "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
              "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/ownmanifest.json",
              "sha256": "b1f7c81210a40d6ebcd15e720e25fc722c100b4f5c7ac6e400665636af3713cd"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/HANDOFF.md",
              "sha256": "332ff82af9f71577a4e0e3944b3cc75ca211eadac4193ff8b37a3a56e8e4e79a"
            }
          ],
          "original_metrics": {
            "path": "production/batch92/assets/eophyllophyton/r004/metrics.json",
            "sha256": "6a663bf68d8504a11e4c293581984510af7ed78fe9c632c6ea7156264d361ef1"
          },
          "source_counts": {
            "path": "production/batch92/assets/eophyllophyton/r004/source-vertex-counts.json",
            "sha256": "13b515bfe242f4b5bca300c63a9241770bde061b4da3e0560cf0ca7965c023dd"
          },
          "proof": {
            "path": "production/batch92/assets/eophyllophyton/r004/proof-final/render-manifest.json",
            "sha256": "eda3ac817d2937d90e83b29963e760d8d0e99cc7bbb543acdf00716fba7296e3"
          },
          "source_preview": {
            "path": "production/batch92/assets/eophyllophyton/r004/preview.png",
            "sha256": "657aeb3937ea8b9221a434f74965b08eea2a6c746e5b061ec5685e7b866a93a2"
          },
          "capture_reference": {
            "path": "assets/additions/eophyllophyton/batch92-20261021/eophyllophyton.png",
            "sha256": "578777e5ff31970326e5dc42c9734517312aee4914a5dcb6e6d9b3e253dc0b60"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/eophyllophyton.json",
            "sha256": "be94f27b7b9b1941245f510be3499ef32e9a5ca59f7d2eef9bd02a2cd8be4b53"
          }
        },
        {
          "id": "oncoid-bed",
          "batch": 92,
          "revision": "r001",
          "candidate_root": "production/batch92/assets/oncoid-bed/r001",
          "source_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "reviewed_source_commit": "37ddf403430e4859d077163855ecdf6e1aa2b0ba",
          "original_source_snapshot": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "review_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/oncoid-bed/batch92-20261021/release-metadata.json",
            "sha256": "b0b9a1a5f79e05dc62deea24f67b6c9b254b0eeca44bc7231fa47a9c43a440a3"
          },
          "candidate": {
            "path": "production/batch92/assets/oncoid-bed/r001/candidate.json",
            "sha256": "9a16b871ddfbd32c140c9db8d0c0c3c249db6f1847996aac5dd53fcedb07b313"
          },
          "active_candidate": {
            "path": "production/batch92/assets/oncoid-bed/r001/candidate.json",
            "sha256": "9a16b871ddfbd32c140c9db8d0c0c3c249db6f1847996aac5dd53fcedb07b313"
          },
          "original_profile": {
            "path": "production/batch92/assets/oncoid-bed/r001/profile-contract.json",
            "sha256": "cca03e9a0c479e0e90786785ba31c09ce81fec390a0a0eea5fbad3c0da2b212b"
          },
          "active_profile": {
            "path": "production/batch92/assets/oncoid-bed/r001/profile-contract.json",
            "sha256": "cca03e9a0c479e0e90786785ba31c09ce81fec390a0a0eea5fbad3c0da2b212b"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
            "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
            "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
              "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/ownmanifest.json",
              "sha256": "b1f7c81210a40d6ebcd15e720e25fc722c100b4f5c7ac6e400665636af3713cd"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/HANDOFF.md",
              "sha256": "332ff82af9f71577a4e0e3944b3cc75ca211eadac4193ff8b37a3a56e8e4e79a"
            }
          ],
          "original_metrics": {
            "path": "production/batch92/assets/oncoid-bed/r001/metrics.json",
            "sha256": "76d4bc1e33eaf7f32c1aabaa5e1a08356a36b13b947a3a7654eabb9ecaf9021d"
          },
          "source_counts": {
            "path": "production/batch92/assets/oncoid-bed/r001/source-vertex-counts.json",
            "sha256": "4242e102252f172e9da2d805638cc8da594b59c7981e206c9817c520641c4ac7"
          },
          "proof": {
            "path": "production/batch92/assets/oncoid-bed/r001/proof-final/render-manifest.json",
            "sha256": "1944b98c5dad7d7f9c697e4675e9bd8d0560d15083b13304756807e32d1d1587"
          },
          "source_preview": {
            "path": "production/batch92/assets/oncoid-bed/r001/preview.png",
            "sha256": "24429a0e235972fc6271f91ce361d45afb810cefadd366dbb3edda6a0478f030"
          },
          "capture_reference": {
            "path": "assets/additions/oncoid-bed/batch92-20261021/oncoid-bed.png",
            "sha256": "00eb6f5700469f71234adb61bcf48ab07c07ccd23c0339ba359afb8127057f06"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/oncoid-bed.json",
            "sha256": "e8a4063cb893953ff9d0f3906d7860ffde9092736917995b79591d90392520f0"
          }
        },
        {
          "id": "thrombolite-mound",
          "batch": 92,
          "revision": "r003",
          "candidate_root": "production/batch92/assets/thrombolite-mound/r003",
          "source_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "reviewed_source_commit": "37ddf403430e4859d077163855ecdf6e1aa2b0ba",
          "original_source_snapshot": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "review_commit": "6ac756468136cc76625b3c94778f17417c0cf88a",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/thrombolite-mound/batch92-20261021/release-metadata.json",
            "sha256": "b98d1fed644cee762ab4cd1161bde909de52bbe9e2d8063d0dfa698bdf3caf14"
          },
          "candidate": {
            "path": "production/batch92/assets/thrombolite-mound/r003/candidate.json",
            "sha256": "e94dc567bcdbeec0d529a8d6343ec8ae796d2ab21747a11f4f88ce4985ca0b51"
          },
          "active_candidate": {
            "path": "production/batch92/assets/thrombolite-mound/r003/candidate.json",
            "sha256": "e94dc567bcdbeec0d529a8d6343ec8ae796d2ab21747a11f4f88ce4985ca0b51"
          },
          "original_profile": {
            "path": "production/batch92/assets/thrombolite-mound/r003/profile-contract.json",
            "sha256": "377c4813a1a66d27cffd985cffee2aedb0dbb370f5b2d27a0976874297b5b732"
          },
          "active_profile": {
            "path": "production/batch92/assets/thrombolite-mound/r003/profile-contract.json",
            "sha256": "377c4813a1a66d27cffd985cffee2aedb0dbb370f5b2d27a0976874297b5b732"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
            "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
            "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
              "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/ownmanifest.json",
              "sha256": "b1f7c81210a40d6ebcd15e720e25fc722c100b4f5c7ac6e400665636af3713cd"
            },
            {
              "path": "qa/continuous-small-life-round39-20261020/batch-92/HANDOFF.md",
              "sha256": "332ff82af9f71577a4e0e3944b3cc75ca211eadac4193ff8b37a3a56e8e4e79a"
            }
          ],
          "original_metrics": {
            "path": "production/batch92/assets/thrombolite-mound/r003/metrics.json",
            "sha256": "e3dc354bd0a53ca1488cf99519b92e9fff7bb8141fd96320e467def7fea0fc8b"
          },
          "source_counts": {
            "path": "production/batch92/assets/thrombolite-mound/r003/source-vertex-counts.json",
            "sha256": "789b7f44eea0b26093e9071a82f7d126b4192228fd521dba9cf00092fe4d6b21"
          },
          "proof": {
            "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/render-manifest.json",
            "sha256": "905d246f0f3c8b0a09e29ce71d5e1996010629faa3ee35581bbc7c47a341d2e8"
          },
          "source_preview": {
            "path": "production/batch92/assets/thrombolite-mound/r003/preview.png",
            "sha256": "1489133debf4313a5ebb476c0caafab0ba1376cde148afbc9f8996f71fd27626"
          },
          "capture_reference": {
            "path": "assets/additions/thrombolite-mound/batch92-20261021/thrombolite-mound.png",
            "sha256": "baf19180f42d7ad1b34be64032cd7264b7b484e9adfaaedcdec3eab8f2251576"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/thrombolite-mound.json",
            "sha256": "274944ec873d5e55b573c83f4be2efa1f70dd76f134fe4b3418c164a32a6c057"
          }
        }
      ],
      "files": [
        {
          "path": "production/batch92/assets/caytonia/r002/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/build-config.json",
          "sha256": "2b275494362c65fa8e75cd0e6754a611abcd422cb0203d547eef4a41391d72e0",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/build-dependencies.json",
          "sha256": "c535be589ce250497c49619d5c51d6e215554ea2c1961b8123b0b1fd2f6b2762",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/candidate-brief.json",
          "sha256": "4e497d1506553f1ce2b2ee1fb353e90e34e9671737ee37c7d1a730d0f315d397",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/candidate.json",
          "sha256": "8a8135e40a6a4906ee066d7f67ca4b79b3a9bdd783449c796142850013c6b98d",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/concept-original.png",
          "sha256": "e7bdef491f6d9becdb42e4857483372a9cd1446c03b295a7b4b4c7b5c8d2a7e9",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/concept-prompt.txt",
          "sha256": "d2330ccf7a854ad3f80b96bd98bc9ef5d452556fa2fdeb012821a87e19f43858",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/contact-sheet.png",
          "sha256": "7c7f804ea83d1d473b22e2cd80aabd2ee5b4b998873e3a78b70004f88a5031f8",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/generator.py",
          "sha256": "a14c48a3bed1edbcbf76da43c81ea12823cabbefba55d2c88265814b2c9feb87",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/gltf-validator.report.json",
          "sha256": "57db68e225b6a29408854744d65f334d08e5a740a1d6438929812877b769d62a",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/lifecycle.jsonl",
          "sha256": "2affdb6770fd5a1b514b7b06e8fc7b337c5368a7dc71fbc2e978fd3d96ee623f",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/maker-review.md",
          "sha256": "acebe10964c9a612c63c9cb7090851406ec9fc374ac77e56ba530259d481afad",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/metrics.json",
          "sha256": "742bdae3780475c05d355e40660e60237f207a618e3b9b3af40324248a20a085",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/model.glb",
          "sha256": "bfc40984e83cf7d181ad6ac0ec9e7912f7e2a091a77dbebfed4d18c8d5a990a9",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/pixel-inspection.json",
          "sha256": "de91c22b1159f76f039ae0d65f8d47da656ff4bf3f6f6c17932a062f659d5bc7",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/preproof-binding.json",
          "sha256": "184faa651566a80850c7330d07ecb90b8ad46352df114904a0a4fa5307a7fffc",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/preview.png",
          "sha256": "279aa5326eb67b7a36804f2411cfde55c8f5b5f4bc5e61b930594c23fa663403",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/profile-contract.json",
          "sha256": "f2e60080daa3ba7e2afe68124a6c052027abf1500ab5952275fa2803297ec1d9",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/project-audit.json",
          "sha256": "a81e4597441300f822b88d60a4337b5185b9d770965ddfbbfb7a63bf946c861f",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/proof-final/clay.png",
          "sha256": "21ce253b58b503f8de35e31052f0b8006c950b9314212799982b5c39eddd10fa",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/proof-final/front.png",
          "sha256": "b56a2c67433b0ab23310df602bb2c34d2b4a4ed8036f99a04f6a88839ea28ae9",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/proof-final/hero.png",
          "sha256": "279aa5326eb67b7a36804f2411cfde55c8f5b5f4bc5e61b930594c23fa663403",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/proof-final/rear.png",
          "sha256": "e8f1a44af627c03a1f1cd420783eac4de149c4cd79daf3514d2aebf3b9d9c8cf",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/proof-final/render-manifest.json",
          "sha256": "cf31d5da8698f3344617af0739e48536ed6cbe9d765ddd379bff07994089769f",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/proof-final/reversehero.png",
          "sha256": "22d8500202b8936db221ec2a0d95c2e1a2288265295c0794d88836e5998c92cb",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/proof-final/side.png",
          "sha256": "9c9335992e649a786d2ff8276760c987061aba0f1500b2ffddb5c6337e6231ac",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/proof-final/silhouette.png",
          "sha256": "c87f75ee3d241dd9e88670bdfc54774b6da421e3f3241b76169371a168707404",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/proof-final/top.png",
          "sha256": "954cfa82d318f1ec44ee4eb9ab832aa1bb0c4ccf327794766d03ee9c56cf2d25",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/references.json",
          "sha256": "f061a962db3c6a1a2c0b81e30334f87fa72c3f176a335dd6562fe8a20e8a5335",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/repro-final-1.report.json",
          "sha256": "b9260a76f1907516a09c9a4cdd8a75fda24fd44d77663b2ef3f82b9c29c16723",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/repro-final-2.report.json",
          "sha256": "2b8430cc6ed32d77c2aab52342c633c613d719e17c0836ee0ab4ebaca4650005",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/runtime-parse.report.json",
          "sha256": "f017fcefc25fd89716d3771135864c320e33cf2abe67f6af1a0409b396d92e42",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/source-final.report.json",
          "sha256": "6fc863eb240ffea04d21daacee25323a674715dc837609e708e0ac6912ac2884",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/source-metrics.json",
          "sha256": "d06923da230c94ffe1082797c437f837e2f13343e96009e9f5d0e25613cb1696",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/source-vertex-counts.json",
          "sha256": "13b173471077fe0eca1d88ae8f65c3b64f2c152ef314ebe6a37e39a2ee948c3c",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/caytonia/r002/source.blend",
          "sha256": "37879bbdff32ce81c63b2a0d3f7b78a39d6fc6003e1cfc3bd20dceb1f57d8150",
          "origin": "source",
          "owner": "caytonia"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/build-config.json",
          "sha256": "c64e7c853c6561235ef3955419e78557a37262f43959b5a8f1bf3517cc76d296",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/build-dependencies.json",
          "sha256": "0eae3f710172e16099f49bbd609fc4ee1a80c597024dc5f176b07f842f4466e7",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/candidate-brief.json",
          "sha256": "c2d79aaa25601855f7c4cd6d0af32b66cbf71f8a926e98893004f7218057a818",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/candidate.json",
          "sha256": "40e2cb3c7ae88b6758b93746d9106a9e7a73150c02ef41db4af0f68f4fb1e7c5",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/concept-original.png",
          "sha256": "3d502cae3f83891cbbe8ec00749b99b28640f3c89586af55998c6cb4e3990ef8",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/concept-prompt.txt",
          "sha256": "66a8d59047c7e52783ac4505b1fe4faa699f72b37f7fbf7ecdb0e505e912588a",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/contact-sheet.png",
          "sha256": "c69e2ef97a3145e18456d105e7ee97b56b1bb666a0d1599a3d328e1d65115aaa",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/generator.py",
          "sha256": "36e3fed93e7e10b9094dc28cc4ef6162ffc239d8dced51ace044c0bc8a3b11a0",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/gltf-validator.report.json",
          "sha256": "51952ab103801aec6c26d7fe90c0d703c8f9ecbbab82d4c7c8d8df57151503c0",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/lifecycle.jsonl",
          "sha256": "9b3768e006bc66a74fca4bd066f7364cc67179ea74a7607e6cc5c5cebcc86d30",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/maker-review.md",
          "sha256": "3da83a9466f85ed7d79d7123b7e88eed8256930644f7d2c1f9e1e9a4381b41a8",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/metrics.json",
          "sha256": "6a663bf68d8504a11e4c293581984510af7ed78fe9c632c6ea7156264d361ef1",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/model.glb",
          "sha256": "5c810c56560ed16f53cd7a12255d2e63ede479f5c66d786d886c97dd302cac2f",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/pixel-inspection.json",
          "sha256": "d41d0543520b4252abc4f138ede1cbf6df763536af958aeff0020b7acf165e57",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/preproof-binding.json",
          "sha256": "6492bdd769e6b3bf7e591798892c7d71e55cef8736f8deb8e2b925adbe07a7d4",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/preview.png",
          "sha256": "657aeb3937ea8b9221a434f74965b08eea2a6c746e5b061ec5685e7b866a93a2",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/profile-contract.json",
          "sha256": "55e774611a17f8d91ecdcfb386808f081c3d013023a4fe4653c0d7fc273dcef1",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/project-audit.json",
          "sha256": "93ca5fb5bd5ace0ad74053bf161f232e94a63dd81918d1afbf818427f9361c02",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/proof-final/clay.png",
          "sha256": "5bed700c9a319535fd64808d5bf3accf656096d07aeb6f3df4ca45f3b1797c58",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/proof-final/front.png",
          "sha256": "9e7adacc02ac07c51d453f86b10e3470feb1ecc63bd52c1d2b6722a9003042cc",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/proof-final/hero.png",
          "sha256": "657aeb3937ea8b9221a434f74965b08eea2a6c746e5b061ec5685e7b866a93a2",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/proof-final/rear.png",
          "sha256": "7797cedbf3a84b91330c9b4b7eeb5310796dfabb35cad1588f70314a700b324b",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/proof-final/render-manifest.json",
          "sha256": "eda3ac817d2937d90e83b29963e760d8d0e99cc7bbb543acdf00716fba7296e3",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/proof-final/reversehero.png",
          "sha256": "3491ac8adb9b7905261900bcacd10f283cc413f9e7f7a49e8f2720a32f84e33c",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/proof-final/side.png",
          "sha256": "2b289f560109b3938b5d2685004caf0995a324cb4a599c655b1f7c9db9ec9860",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/proof-final/silhouette.png",
          "sha256": "7fcb3d1a9bbab5d5f4a75b5746acc7b44c77efe27ae871a101b570d5934c0d65",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/proof-final/top.png",
          "sha256": "ee070613b37ab6028f4540ed599bc3887cff3fb80e244c92057833767828c8b6",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/references.json",
          "sha256": "9e8e3e939a78699c480838a1688dfc7cf3ac07358fc68690e4d104403707a8ca",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/repro-final-1.report.json",
          "sha256": "fa5e333728efbfc89bb9171fa63f8ca6e735ff8d07b4877b6af49cd026b9115d",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/repro-final-2.report.json",
          "sha256": "6d2e72c9d28a2da1cbea50e821bda5cfb5d71a7c42c4e67a5c18e1eb3e38fec7",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/runtime-parse.report.json",
          "sha256": "c98cc62bce60f9aa48e0c44f8946b7801987b12fd6ae55fe53f64d55722e70c7",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/source-final.report.json",
          "sha256": "1c41a2d36ca1484dbb5b4bf6e5b54e5b423eedcb8c3a861d4807b0fb27ca4efe",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/source-metrics.json",
          "sha256": "fbb89ca545b55080ef769c7a5d3dab51a1e66ff2f24d2e37cb9d8d8c76f1973f",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/source-vertex-counts.json",
          "sha256": "13b515bfe242f4b5bca300c63a9241770bde061b4da3e0560cf0ca7965c023dd",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/eophyllophyton/r004/source.blend",
          "sha256": "062e038c168b8abf6d265c9d53a3b7199dea8962a85b23d296e5026c8ee4bd5b",
          "origin": "source",
          "owner": "eophyllophyton"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/build-config.json",
          "sha256": "5f01f8cd530f18ec5a6728098ad62bb4bbe7c0c020e09b790c1120e9259ce5c7",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/build-dependencies.json",
          "sha256": "268e61f1a4cf5471b60572acab2781ec6544cb5dabbc8f690a6d79c2327cbb6e",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/candidate-brief.json",
          "sha256": "689fc8ce72b60e78c49677e8e190563eb64e84181293bc890a16d49ca4d4f9d0",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/candidate.json",
          "sha256": "9a16b871ddfbd32c140c9db8d0c0c3c249db6f1847996aac5dd53fcedb07b313",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/concept-original.png",
          "sha256": "56dabf0d2222031b0e58b9daf47409af2773ccb7a6e76131ee007b396dac4ebf",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/concept-prompt.txt",
          "sha256": "243f99baef2fce8c5cf66804539dd6c738fb165897760e164db912306ac23bdb",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/contact-sheet.png",
          "sha256": "0afdf2cbf1fd4a09459acd04fc635ff63fab877ba96119d2920c979783ef2554",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/generator.py",
          "sha256": "5d4c6cbe1e60a6880150229b78967d712bea9e6cb58137b24171172ca1132548",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/gltf-validator.report.json",
          "sha256": "9b2c71f953dbb5aec30a59e9d16da5d5fad6e56b289c8b635b61e42a85fd0450",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/lifecycle.jsonl",
          "sha256": "da46e4bb9a6108206e739495c63bc40c7efa97bcd916eafb2c16e86b34ad58e9",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/maker-review.md",
          "sha256": "58b337cffcb54a5ccda098ef045cd8c1dd0a03b4003ef6c0ac4896067b883b1d",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/metrics.json",
          "sha256": "76d4bc1e33eaf7f32c1aabaa5e1a08356a36b13b947a3a7654eabb9ecaf9021d",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/model.glb",
          "sha256": "e18d0eb0817ad70bc1dbc5c4106d8ec536a11e20d5e090794094d119ac9f9da8",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/pixel-inspection.json",
          "sha256": "6656c1eddb74ab0196263a6941eed00d1cb0d8e8de13d8de2eb184092f6bb890",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/preproof-binding.json",
          "sha256": "4eba4f2589e4b66cddfa5e2c61fdd5efc99f45815fadf19bb30b7c861e9bf3f6",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/preview.png",
          "sha256": "24429a0e235972fc6271f91ce361d45afb810cefadd366dbb3edda6a0478f030",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/profile-contract.json",
          "sha256": "cca03e9a0c479e0e90786785ba31c09ce81fec390a0a0eea5fbad3c0da2b212b",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/project-audit.json",
          "sha256": "451cb783f203a8c2ede02a707aed0514c499065a982009257e7b05cd44a0d7bf",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/proof-final/clay.png",
          "sha256": "43d9828a97fb5bb164bc8a17ab6109abbf2014f846253fbf12889faffd86aa62",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/proof-final/front.png",
          "sha256": "72d6597a90c18a18b587504a358f8c9dc43501d6a93710595e773dfb2f28d7c3",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/proof-final/hero.png",
          "sha256": "24429a0e235972fc6271f91ce361d45afb810cefadd366dbb3edda6a0478f030",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/proof-final/rear.png",
          "sha256": "4351b66adf4a333840bc0f33ccf5e627e0b73eccbfb5c08a5858883909671a75",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/proof-final/render-manifest.json",
          "sha256": "1944b98c5dad7d7f9c697e4675e9bd8d0560d15083b13304756807e32d1d1587",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/proof-final/reversehero.png",
          "sha256": "0290330c23ab4ba210c84b2e74a66c762eb0f63a1ff069c05071679315ef3914",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/proof-final/side.png",
          "sha256": "55bd2987f7d0fe8bb0afbce27b67f7e822bcbae6ccac1375f17f68e38366891d",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/proof-final/silhouette.png",
          "sha256": "d3e9c486ec1d0e9729a2e5878bf50d67e585f8ac2a1a893a165909e71cfb64fc",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/proof-final/top.png",
          "sha256": "16c810975504f6aaa286d548be4ca17f8cd8a67557016d09611ea4ff7ca5487e",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/references.json",
          "sha256": "1a555af4d3bf250bdfae3a0910f27851da9d1c65489ca06d7d957af1d86c3c2f",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/repro-final-1.report.json",
          "sha256": "92125c873e77eb955e72b47a8f6e3b4e6b1022a13bc30b3dd9b1408675aedcaa",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/repro-final-2.report.json",
          "sha256": "48291699d001e572886c293a9a4aa620ddeb6c56460b9c5eaefb30e39bff3b15",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/runtime-parse.report.json",
          "sha256": "048f2b1f27467c9ffc9554aa32c27e6afcaf4d127387be1c431a3705a24138d4",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/source-final.report.json",
          "sha256": "93daf30d5e25afe8dde543c1dd5d94ee57c359e2881719797521de84e1422875",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/source-metrics.json",
          "sha256": "1ea6da2379670bef89d36a41f9ee124beac1f74779d7034715079a992704a6cf",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/source-vertex-counts.json",
          "sha256": "4242e102252f172e9da2d805638cc8da594b59c7981e206c9817c520641c4ac7",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/oncoid-bed/r001/source.blend",
          "sha256": "115e5fa3532355bdaa000ceeee7725652abbf63174de434c6cd37f50ecb27c1a",
          "origin": "source",
          "owner": "oncoid-bed"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/build-config.json",
          "sha256": "58ef496bc48e71bf3234c833e7ca6ff8b8bcab3890c0ef9cf8341a2bc9f547b6",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/build-dependencies.json",
          "sha256": "3c9e669c6e9faaadde07d7713fddddde98a37c8c4cec595beab7632947f7896e",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/candidate-brief.json",
          "sha256": "b2b684a64f5fc5d8605f38115d9e22243abc1d8cc2a0cb8650f9844d7b1be512",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/candidate.json",
          "sha256": "e94dc567bcdbeec0d529a8d6343ec8ae796d2ab21747a11f4f88ce4985ca0b51",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/concept-original.png",
          "sha256": "5a1a6392378848ac40bd847f1a6d2259f9f91b13896ed16339f48ce09b2a0ca4",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/concept-prompt.txt",
          "sha256": "161e3365fd1bf128b427e1f55db9971382c29ef2697c979f24489b58ee3f5f64",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/contact-sheet.png",
          "sha256": "c53e6585f8b5935b1af33885583c802d14ff08c045a4c6b272f7863ecba572a7",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/generator.py",
          "sha256": "c7a762de59a47fec252c5bb2fd79b1ad129bda7e1c9a6678c5cbd894712fe321",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/gltf-validator.report.json",
          "sha256": "123097eca75eec5380931ce6a8e6c910efbfc357e7c2d3dcceb791bc13e09950",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/lifecycle.jsonl",
          "sha256": "91c871443996dc2b9de792b8e18c1a54ada3a7b38d2b498d83a8c8259c8fd93c",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/maker-review.md",
          "sha256": "fb3360e494e82311602c5b448dc938cf09e08c750a4bcc8643c297f680bc84eb",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/metrics.json",
          "sha256": "e3dc354bd0a53ca1488cf99519b92e9fff7bb8141fd96320e467def7fea0fc8b",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/model.glb",
          "sha256": "8e303602455cc235dff744df8faad4870282c124b1a2257b8c73831c816d8a3f",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/pixel-inspection.json",
          "sha256": "8ff9f358fe2245af666383295ac80a6a3f88c7dbce3f3f8cacbaf76292e28981",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/preproof-binding.json",
          "sha256": "881e566c09f554612088f45457fbe89089cb80a0d109bdddb039bb47fc588f70",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/preview.png",
          "sha256": "1489133debf4313a5ebb476c0caafab0ba1376cde148afbc9f8996f71fd27626",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/profile-contract.json",
          "sha256": "377c4813a1a66d27cffd985cffee2aedb0dbb370f5b2d27a0976874297b5b732",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/project-audit.json",
          "sha256": "3c0470114d2644d80205d90050798e17ba635c54d0e093b7fff7c9c56f911599",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/clay.png",
          "sha256": "06e31d59cdd1ce55906d7d06968e7def1d0e0211dbd72a5465eb116e60101848",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/front.png",
          "sha256": "6dc1530df548928d6a6b688a6a30a1fbbc6b5d13637de603f4cc316cea060609",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/hero.png",
          "sha256": "1489133debf4313a5ebb476c0caafab0ba1376cde148afbc9f8996f71fd27626",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/rear.png",
          "sha256": "c6eedd5c435a9f2a8458807f138f57222574e6158e1bd2e976d654fa05214598",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/render-manifest.json",
          "sha256": "905d246f0f3c8b0a09e29ce71d5e1996010629faa3ee35581bbc7c47a341d2e8",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/reversehero.png",
          "sha256": "d4693f9adb16dbd1e29d648d93356d930202ca2700ca9874ae9710708384a392",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/side.png",
          "sha256": "f66a4547f36552a3e70b1d35f55a85111a04a1cfda8688b8753418a6e9ec90a3",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/silhouette.png",
          "sha256": "6e6f0cc360ee816822408c55b1c0cab018775a5b10a795155f0ff790c9d4da33",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/proof-final/top.png",
          "sha256": "df4b2af91e511af6a8b7c08a26aaa66091b485e54b0663208581e9b362cc47fb",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/references.json",
          "sha256": "10e563c448bb82e4cc797caa4714357609dc92a1854641a20a9aa7c346bccc81",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/repro-final-1.report.json",
          "sha256": "39e39ecd79a181a1b89d2f1801c95350de14a817d4d4bdae1ead2586e752a868",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/repro-final-2.report.json",
          "sha256": "f5170afe1dfe4bbf5ed89c3734c663d54fda46523478c7f828b4b97a3bcc9092",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/runtime-parse.report.json",
          "sha256": "390361ce88266d9a3a2fa3576a76adbfbd6e6bbb9ac6e657452f5bf8c88a0159",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/source-final.report.json",
          "sha256": "0a4ad6e1ff8434a69cba56d1870142edd0b370bd06591806eb55876fe812f7ff",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/source-metrics.json",
          "sha256": "9cb485becd65f7611f90a39f933809db294ebe98e6f7d521e928d1848ee7be2f",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/source-vertex-counts.json",
          "sha256": "789b7f44eea0b26093e9071a82f7d126b4192228fd521dba9cf00092fe4d6b21",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "production/batch92/assets/thrombolite-mound/r003/source.blend",
          "sha256": "fe5ab1790703e84165c8e75f1677664bbfdb962df57e8f81555191b75d729d6c",
          "origin": "source",
          "owner": "thrombolite-mound"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/HANDOFF.md",
          "sha256": "332ff82af9f71577a4e0e3944b3cc75ca211eadac4193ff8b37a3a56e8e4e79a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.machine.json",
          "sha256": "89104c75b6886b635220eb43c5e8daaefdb9e83da3437d83be15faba1b02326b",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/REPORT.md",
          "sha256": "99170770b37e5486a397547dca97c4bdb406e3a079c6fb41b551b20a2ce639f0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/audit-chain.py",
          "sha256": "827aafe5cb688cf80516454319892b3ecce8a45fe8b95ace31f90952cf3a966f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/finalize-report.py",
          "sha256": "3cc920a386594be9a6a6784e380cd7cf4127cc4b9d4467bd2d82bcf00d2a71f9",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/inspect-runtime.mjs",
          "sha256": "a36560f60cd2e6e1bd497f0b1f5f9302c41e4f5ea78b8d071cfb93ee56a6b267",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/inspect-source.py",
          "sha256": "c7f26099b48e9c7f830146526be055e6c29ab6c4467b7a61fcd51470cebfc159",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/ownmanifest.json",
          "sha256": "b1f7c81210a40d6ebcd15e720e25fc722c100b4f5c7ac6e400665636af3713cd",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round39-20261020/batch-92/run-inspection.py",
          "sha256": "6e78e2fe87596a6975f14abdf706c231eb6a66af775f9dca2008723d8a9de5fe",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g10-release-20261021/process-archive-index.json",
          "sha256": "c9cc7461065c15ff4386885a76247ef05f512cd93ba1edc196b602b38d44296f",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g11-20261021.json",
      "sha256": "9b9be88ae38cd90f30985c7ce2ec7e4813f9c54ba55589218e25b509b8c78281"
    },
    "release": {
      "version": 1,
      "scope": "next52-g11-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "6f8cab54bd17583d3f8a5791713f9eb500459b48",
      "review_commit": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g11-release-20261021/source-bundle.json",
        "sha256": "99e0d5245ed90ad77da0216a1d18519745a48c208b79fe30ccc60df59214ff05"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
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
          "path": "scripts/rebuild_frozen_blender.py",
          "sha256": "c5971fab63b69fa3720d52b9884789eb56f6c2b1d2db4d6c9d3fa2bc77a59db6"
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
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/handoff.json",
          "sha256": "d4bd9ec9e95e400cfafd64d3b87d63015c8c24de8852e9734de2302d7f3a8372"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
          "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/own-evidence-manifest.json",
          "sha256": "4d95737bc4527be4422cdb9faf722118b31deaa10087bb8d658918d0a8e9d07a"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "badlands-ridge-network",
          "batch": 82,
          "revision": "r002",
          "candidate_root": "production/small-life-batch82/assets/badlands-ridge-network/r002",
          "source_commit": "6f8cab54bd17583d3f8a5791713f9eb500459b48",
          "reviewed_source_commit": "13556c314fbf5ee1a4469fb92fc4a3fa84f1771d",
          "original_source_snapshot": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
          "review_commit": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/badlands-ridge-network/batch82-20261021/release-metadata.json",
            "sha256": "d14af916ef6ffbdce1e73c084f8c8cd1167daa8cc5f185b9d50cb7287cff1910"
          },
          "candidate": {
            "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/candidate.json",
            "sha256": "f102637dffb0ec632a6d7f92b64877c87f7c811ba690968743106bf6d948696a"
          },
          "active_candidate": {
            "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/candidate.json",
            "sha256": "f102637dffb0ec632a6d7f92b64877c87f7c811ba690968743106bf6d948696a"
          },
          "original_profile": {
            "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/profile-contract.json",
            "sha256": "8c38a3c62049e01652848b5370bb515025fe279a0aca3275bab6f6d84fe4d8b7"
          },
          "active_profile": {
            "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/profile-contract.json",
            "sha256": "8c38a3c62049e01652848b5370bb515025fe279a0aca3275bab6f6d84fe4d8b7"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
            "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
            "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
              "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82/own-evidence-manifest.json",
              "sha256": "4d95737bc4527be4422cdb9faf722118b31deaa10087bb8d658918d0a8e9d07a"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82/handoff.json",
              "sha256": "d4bd9ec9e95e400cfafd64d3b87d63015c8c24de8852e9734de2302d7f3a8372"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/metrics.json",
            "sha256": "555cdab454951198e4f5584ae8791860994e7eb787d5099f2aa1afa808d7baa3"
          },
          "source_counts": {
            "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/source-vertex-counts.json",
            "sha256": "03c1b841a1ca79a0120a25690b66ea31012f100b63bd68f5a1279426c6c8bff9"
          },
          "proof": {
            "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/render-manifest.json",
            "sha256": "9c0c5acec238e9fc6ae5957d789ab602903f5f64a4172db085f3ea4eae8ee3e7"
          },
          "source_preview": {
            "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/preview.png",
            "sha256": "8c492848d8cc33caa77ebe9eed51a7ebbbb6cf2589a2f3a00b2464f18b7bbeb0"
          },
          "capture_reference": {
            "path": "assets/additions/badlands-ridge-network/batch82-20261021/badlands-ridge-network.png",
            "sha256": "fa58694075ffa464b7057bf2bdf2c04a8668a9c0a12cf21580d2ea8e14a70667"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/badlands-ridge-network.json",
            "sha256": "3ef3ebad4cc4cc013ec3f26a8410068d5ff46abd7f0aed6e18c97188e560ef23"
          }
        },
        {
          "id": "kimberella",
          "batch": 82,
          "revision": "r002",
          "candidate_root": "production/small-life-batch82/assets/kimberella/r002",
          "source_commit": "6f8cab54bd17583d3f8a5791713f9eb500459b48",
          "reviewed_source_commit": "13556c314fbf5ee1a4469fb92fc4a3fa84f1771d",
          "original_source_snapshot": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
          "review_commit": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/kimberella/batch82-20261021/release-metadata.json",
            "sha256": "58d9c53f9b370f46d30b15e99fd6cecb51310c2b1c9751aa300675ea2e8e6671"
          },
          "candidate": {
            "path": "production/small-life-batch82/assets/kimberella/r002/candidate.json",
            "sha256": "8f8c59ed582078287301e110a76ac0752241bc97c239a0ea748817fdb944079f"
          },
          "active_candidate": {
            "path": "production/small-life-batch82/assets/kimberella/r002/candidate.json",
            "sha256": "8f8c59ed582078287301e110a76ac0752241bc97c239a0ea748817fdb944079f"
          },
          "original_profile": {
            "path": "production/small-life-batch82/assets/kimberella/r002/profile-contract.json",
            "sha256": "3c714c79f6c78ac480db461581186c5ca1108606a0321ab073fff992f6c4a150"
          },
          "active_profile": {
            "path": "production/small-life-batch82/assets/kimberella/r002/profile-contract.json",
            "sha256": "3c714c79f6c78ac480db461581186c5ca1108606a0321ab073fff992f6c4a150"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
            "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
            "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
              "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82/own-evidence-manifest.json",
              "sha256": "4d95737bc4527be4422cdb9faf722118b31deaa10087bb8d658918d0a8e9d07a"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82/handoff.json",
              "sha256": "d4bd9ec9e95e400cfafd64d3b87d63015c8c24de8852e9734de2302d7f3a8372"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch82/assets/kimberella/r002/metrics.json",
            "sha256": "a43adab3d1e946894933d95426296feb75c58b030086bb5bfe2cd470e69e9d37"
          },
          "source_counts": {
            "path": "production/small-life-batch82/assets/kimberella/r002/source-vertex-counts.json",
            "sha256": "9eb41c789fa893b1b1a56852766c0f386ec8764e4e6b45359c9b32718fe28f61"
          },
          "proof": {
            "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/render-manifest.json",
            "sha256": "8c0a26da737878036c800e2b5f6900d237b84d7795b6a602acabac0dde292f18"
          },
          "source_preview": {
            "path": "production/small-life-batch82/assets/kimberella/r002/preview.png",
            "sha256": "8538a9a57f21992d3549d1b982a993ec5371e09a2681cdf4483459bed33e26cc"
          },
          "capture_reference": {
            "path": "assets/additions/kimberella/batch82-20261021/kimberella.png",
            "sha256": "fd3cbf2eb879d8bfca9e8895a715d133a70adfa75e8e658fe0ee9d671c4d5c10"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/kimberella.json",
            "sha256": "1ffdb87769d2f66d0b6581f8aa428a7416eb986c8b885bc414820b4a11d34d8d"
          }
        },
        {
          "id": "playa-basin",
          "batch": 82,
          "revision": "r003",
          "candidate_root": "production/small-life-batch82/assets/playa-basin/r003",
          "source_commit": "6f8cab54bd17583d3f8a5791713f9eb500459b48",
          "reviewed_source_commit": "13556c314fbf5ee1a4469fb92fc4a3fa84f1771d",
          "original_source_snapshot": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
          "review_commit": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/playa-basin/batch82-20261021/release-metadata.json",
            "sha256": "83ea0949be8017b5448c52e3520f9557a6834f1a622da9328ac9acab13b7194f"
          },
          "candidate": {
            "path": "production/small-life-batch82/assets/playa-basin/r003/candidate.json",
            "sha256": "2bdd44c63b9c57cd5c1c20dfa44a8248e575efc9791f48b9060dc8134806d222"
          },
          "active_candidate": {
            "path": "production/small-life-batch82/assets/playa-basin/r003/candidate.json",
            "sha256": "2bdd44c63b9c57cd5c1c20dfa44a8248e575efc9791f48b9060dc8134806d222"
          },
          "original_profile": {
            "path": "production/small-life-batch82/assets/playa-basin/r003/profile-contract.json",
            "sha256": "fa9931d476bcc0437eefefc72cd3a604ac3f2754705e26b85f7557c31485e041"
          },
          "active_profile": {
            "path": "production/small-life-batch82/assets/playa-basin/r003/profile-contract.json",
            "sha256": "fa9931d476bcc0437eefefc72cd3a604ac3f2754705e26b85f7557c31485e041"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
            "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
            "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
              "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82/own-evidence-manifest.json",
              "sha256": "4d95737bc4527be4422cdb9faf722118b31deaa10087bb8d658918d0a8e9d07a"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82/handoff.json",
              "sha256": "d4bd9ec9e95e400cfafd64d3b87d63015c8c24de8852e9734de2302d7f3a8372"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch82/assets/playa-basin/r003/metrics.json",
            "sha256": "3b21b212637e74d8a39d9d99c53254f8cc67dd6010aa0a8cf6965d32620aae3c"
          },
          "source_counts": {
            "path": "production/small-life-batch82/assets/playa-basin/r003/source-vertex-counts.json",
            "sha256": "aa80798621b7a4ea9a6a6e826522ba4ef8a42dc6c0664462f448cbb5d13cfc4c"
          },
          "proof": {
            "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/render-manifest.json",
            "sha256": "c90b77a2f665d2451292f7423ddc52bb4bdf32609febee983e4bd83f49c74bfa"
          },
          "source_preview": {
            "path": "production/small-life-batch82/assets/playa-basin/r003/preview.png",
            "sha256": "d119a5e9ff664ac2f3ed12377ea976c5a6526550c878be04fa96ac8e520cbbb7"
          },
          "capture_reference": {
            "path": "assets/additions/playa-basin/batch82-20261021/playa-basin.png",
            "sha256": "e1b35cc0d585b6b4bc2f1bd88c48972a57f307777a71e396122fc853979c8af6"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/playa-basin.json",
            "sha256": "68d03c24321762bf983015a3b74f4fc704400a8cffa984cf9a0c49d079a2cc0a"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/brief.md",
          "sha256": "1f92367b31831799bf4ac7c9e9ab55e40466857dff57e181ab0f9900a9a6fac2",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/build-config.json",
          "sha256": "567c6dd131fc8453bbe106aa60118a83a06acb7faed1a54687b55c5b8da21b7b",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/build-dependencies.json",
          "sha256": "ccd49f364c6058a053eb36d85085105c8ae0cc7274c733eff0c2f7f16bbdea2a",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/candidate-brief.json",
          "sha256": "87004e4067128e641e7865825d513de4c496866a2f7f6d61a1c1b6a4d89d36a3",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/candidate.json",
          "sha256": "f102637dffb0ec632a6d7f92b64877c87f7c811ba690968743106bf6d948696a",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/concept-original.png",
          "sha256": "0060bcb028f42d61e05627fc997c99a165d311c60f7c1384d964e5e18e30286f",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/concept-prompt.txt",
          "sha256": "ded7393034bad979238e05d6c90507d7d9496b519a2c9d65197b9f0910d71fff",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/contact-sheet.png",
          "sha256": "9dac02d1b6a64c2e49c2034c5ee591e589aef0a3181c740043b1748bff4cb492",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/generator.py",
          "sha256": "fab7a41126efa19c93d2591da16627e2709bec57f8bf057ca4ad7b3bf5f9c0f9",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/gltf-validator.report.json",
          "sha256": "be25ac20e305550fe02cfb4771641721642cbb70af84d0684f671d2a5fca1f7d",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/lifecycle.jsonl",
          "sha256": "e213f567021fe677af965a513ab92b4b067905d14d3b95d4356e2b44398e8f13",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/maker-review.md",
          "sha256": "52611bf524caf09fa1de6019f0e9e6153b25fc5c0ede71354fbef89290efeb06",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/metrics.json",
          "sha256": "555cdab454951198e4f5584ae8791860994e7eb787d5099f2aa1afa808d7baa3",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/model.glb",
          "sha256": "b0127ad07c326e85373ff207610051646349205b18b46524c4ce13cc47c87091",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/modeling-freeze.json",
          "sha256": "a9bc55c910164fe03a970dd692a08f1c4602ff819e7b536fbef4a5ed752c9655",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/physical-surfaces.report.json",
          "sha256": "cc7b3d50d64d902f82d8dff9b4207f1e1d9a3857fa9c5c522441664862197e55",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/pixel-inspection.json",
          "sha256": "f85bea74efe41d6a1fd70eabfc775984cd1750c4c43208121ede08c160cf68a6",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/preview.png",
          "sha256": "8c492848d8cc33caa77ebe9eed51a7ebbbb6cf2589a2f3a00b2464f18b7bbeb0",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/profile-contract.json",
          "sha256": "8c38a3c62049e01652848b5370bb515025fe279a0aca3275bab6f6d84fe4d8b7",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/clay.png",
          "sha256": "9b2e876518b722cf76914691a9df79248b65c0a687b8ca93ed86563c3294d397",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/front.png",
          "sha256": "74f904a5338f6021a77d6814d6fe3b020dfd2380d8ffeb887f7308ebef7efe02",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/hero.png",
          "sha256": "8c492848d8cc33caa77ebe9eed51a7ebbbb6cf2589a2f3a00b2464f18b7bbeb0",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/rear.png",
          "sha256": "a9f1fc5c0e9482063668140122803c2db80ea7c1c07f26056cc5691052259a0a",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/render-manifest.json",
          "sha256": "9c0c5acec238e9fc6ae5957d789ab602903f5f64a4172db085f3ea4eae8ee3e7",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/reversehero.png",
          "sha256": "04b02d8b4697ae3228eb556fb862dc61cd4e662c25d069356e0230fcb96bc565",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/side.png",
          "sha256": "4d3ee2931983549797425113e0e3078accc8b2b12f125172a083ec5521ec8e08",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/silhouette.png",
          "sha256": "2b3dc5260ee4a06439f403251c78dc3425a626c30019d067e690c311b7dfef61",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/proof-final/top.png",
          "sha256": "b8c8ecacf72bd35adb9401d673f6e2cbb23ef8cfe923d245cd96ed1361d4dd8d",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/references.json",
          "sha256": "51c956eecbe809d1f9ffc719d8929739b59f36e3068c476ef583a8f9bf4bd460",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/repair-freeze.json",
          "sha256": "7e7cdcae3d9b629696dc29eb69215db64cd9cbf495550c160076bb095bc95afe",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/repro-final-1.report.json",
          "sha256": "6a2aa2dea303bf5b7e638341c2daafd955822553ec2478e1c6dc702196a3f495",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/repro-final-2.report.json",
          "sha256": "265b14195721aa031ac7dbb2c4c073c2a222327fa7d6842d2cfe34ee482cdb15",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/runtime-parse.report.json",
          "sha256": "b1fa18c76eeff2dd62c0ad29fc72361c1d79e2b0679dbacb0f037cdf6c1d3524",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/source-final.report.json",
          "sha256": "6956265ad3718eb5bec5aa4157becee46bbbc2a6b58320146e1d5f6a0c997370",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/source-metrics.json",
          "sha256": "7bfbb5a50b47e86998be7df098c22dc56ce032711c3f925e37d4b5a3a4df2f26",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/source-vertex-counts.json",
          "sha256": "03c1b841a1ca79a0120a25690b66ea31012f100b63bd68f5a1279426c6c8bff9",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/badlands-ridge-network/r002/source.blend",
          "sha256": "fbd3503e0d7f1655f6c454b3a4513e465461e5a760877f86a07be6bc4df1c307",
          "origin": "source",
          "owner": "badlands-ridge-network"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/brief.md",
          "sha256": "8afd1cc1dbada7fe921cb5a3f07559f47eed8edbc27483399dfff47d3447dbd3",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/build-config.json",
          "sha256": "067ac86aa70240cde2c5e7cc46bdd223ce6546cd9ed6ff77e7e8184b7fd9fb68",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/build-dependencies.json",
          "sha256": "b6cc8fd7f8d59cd20461865183c704b5c2214b0619b54c9c59c2b62b5cbae159",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/candidate-brief.json",
          "sha256": "aef0fff8afa9d019b19199b746ed8d6e1162801f112a924a5f177ef266d83a25",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/candidate.json",
          "sha256": "8f8c59ed582078287301e110a76ac0752241bc97c239a0ea748817fdb944079f",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/concept-original.png",
          "sha256": "0060bcb028f42d61e05627fc997c99a165d311c60f7c1384d964e5e18e30286f",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/concept-prompt.txt",
          "sha256": "ded7393034bad979238e05d6c90507d7d9496b519a2c9d65197b9f0910d71fff",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/contact-sheet.png",
          "sha256": "cb80e26439832c9e2f48fef1a436c071516ad233b99b059c087edd519864fec7",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/generator.py",
          "sha256": "c86fae4184d22fbd32cda2a554c3b18a2921601fe0cf728bc72e54777bc41b83",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/gltf-validator.report.json",
          "sha256": "d600a2921a2f1a46c4df2b0d7bebc819bc84d49c8097a784b0af45f246b0f962",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/lifecycle.jsonl",
          "sha256": "72ec842d824bb8fcb1e55334a3d0f6f60436a0ab349bdfe93a72994db7d1dcb1",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/maker-review.md",
          "sha256": "db929f9ff30d8b5c339a4a70fa9c1ff9754585b76509e7b87b9be18327c410cc",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/metrics.json",
          "sha256": "a43adab3d1e946894933d95426296feb75c58b030086bb5bfe2cd470e69e9d37",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/model.glb",
          "sha256": "6437dec0dada749eba5bdf2a7be12b03bc634da4d651b571bf92c6d99aba1947",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/modeling-freeze.json",
          "sha256": "2898c2e7bd375159318cabba7937fa03be87f90fb154b8a7a489a906baa6b312",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/physical-surfaces.report.json",
          "sha256": "1bda14a1dfd0462ff3ee9bb6fdc2cd98bbec727f405ee84744495620ef072c4a",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/pixel-inspection.json",
          "sha256": "6f59d98c603e4b6c9e8d1749042d2300fe8cd135100cb1c45243851916841a30",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/preview.png",
          "sha256": "8538a9a57f21992d3549d1b982a993ec5371e09a2681cdf4483459bed33e26cc",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/profile-contract.json",
          "sha256": "3c714c79f6c78ac480db461581186c5ca1108606a0321ab073fff992f6c4a150",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/clay.png",
          "sha256": "9db0ba40e7bd1fdae16b4f2d66f4492f54786ba658793ff965d7ed543b392bde",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/front.png",
          "sha256": "a49598b6d6d2109f2361081c30e0cc0febf762110687442ba284e8deb9e5e228",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/hero.png",
          "sha256": "8538a9a57f21992d3549d1b982a993ec5371e09a2681cdf4483459bed33e26cc",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/rear.png",
          "sha256": "ff28c6a3772eb10f39ef3bd232f17d3954ea5476ab63511afa54919ac10a67f0",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/render-manifest.json",
          "sha256": "8c0a26da737878036c800e2b5f6900d237b84d7795b6a602acabac0dde292f18",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/reversehero.png",
          "sha256": "3bf2b7fd18c43a08bdf35541a5b1d5d5b1265598127fa99725203eddd8ce41b6",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/side.png",
          "sha256": "3eb1d75e076412f1c0a6f407575939ce968385dd7605d3dadaa5372e0aecfa9d",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/silhouette.png",
          "sha256": "a8260df46d7209262f6f7fd88e0aba0a32a34fddf000b6da521fb121dd04bbdd",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/proof-final/top.png",
          "sha256": "80101733084d77ad8dcb4a0f570630b53abbcd7b67060a5df551712e0329bcfa",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/references.json",
          "sha256": "7483ec11718e6e200f98166c6d7fb74df430c4ea6e929ab42b91c19d6aeb20a5",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/repair-freeze.json",
          "sha256": "3a1b56fb0e4b13e17f8ae8e7ee34f1cafbf710d0681793e4c3a9503eaac02093",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/repro-final-1.report.json",
          "sha256": "0ab494e3b5736b843cd204642cec6ec973340b4e554bdbaa8e591b440e9784e5",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/repro-final-2.report.json",
          "sha256": "7c6c58640026351faf12d261c7fd94785dc35939123ae16b61591d424109d965",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/runtime-parse.report.json",
          "sha256": "6b125efc61764f14d0db198003ebd0feff79743ccd410f3535a15be58bd1e754",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/source-final.report.json",
          "sha256": "c96b4b170601c284506f1df9a7a438eeac31b986766d701f755bba8643991c93",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/source-metrics.json",
          "sha256": "e8435d8d27dc8c43253a96bc4b8f27a3bb8ca8eacab771655fecd89ed4c32f17",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/source-vertex-counts.json",
          "sha256": "9eb41c789fa893b1b1a56852766c0f386ec8764e4e6b45359c9b32718fe28f61",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/kimberella/r002/source.blend",
          "sha256": "299a07e78d489bc22d1d3567ff2149744a7b3852d55620e9f872517d457ad5ef",
          "origin": "source",
          "owner": "kimberella"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/brief.md",
          "sha256": "3fc579fce1bf2bad9519de88655691e9ebde6244b29c098ac2d6eb7cf8700690",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/build-config.json",
          "sha256": "a23995cca4a9a54d2d66af5e81ac0c40dfd7f2bd81516c39f27949fcc5cfea51",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/build-dependencies.json",
          "sha256": "5d2ee614216ac02b6fba1039d1bcb56b37bdb4981a987da8b39fcceb48aa822c",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/candidate-brief.json",
          "sha256": "a2abff226f3601c8e4384fb56278e06b10cd577b44ef35aeb7a9f7f69c2a7354",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/candidate.json",
          "sha256": "2bdd44c63b9c57cd5c1c20dfa44a8248e575efc9791f48b9060dc8134806d222",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/concept-original.png",
          "sha256": "0060bcb028f42d61e05627fc997c99a165d311c60f7c1384d964e5e18e30286f",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/concept-prompt.txt",
          "sha256": "ded7393034bad979238e05d6c90507d7d9496b519a2c9d65197b9f0910d71fff",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/contact-sheet.png",
          "sha256": "cf88415c1b41a3dde66bbe6d65a14425092f74245d8777617b734a3b4a996bd3",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/generator.py",
          "sha256": "54f0327fb0bd90337838e63368311a57cc281073cb9b6aaff38ecc326c415ee7",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/gltf-validator.report.json",
          "sha256": "7d85cd154cedcaf06810a0320613d06851907e480da77ebcaefde69a9abb4a42",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/lifecycle.jsonl",
          "sha256": "8e572747a8b80a44c097cf63e119264bca42d5443151e66b09e42f6466bfa386",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/maker-review.md",
          "sha256": "ef19916c244380e12616fbd0657d861252085cfdeb43f6d742fb6e1a4908213c",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/metrics.json",
          "sha256": "3b21b212637e74d8a39d9d99c53254f8cc67dd6010aa0a8cf6965d32620aae3c",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/model.glb",
          "sha256": "9b6bdef5c02948e1cb0941b531449bf44825bd3c4b7d9f5a858e3ff29183127e",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/modeling-freeze.json",
          "sha256": "61f8d1d64d75c6338eb2ee276788e89fc655843cdd5122b6dcacca4f24963c31",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/physical-surfaces.report.json",
          "sha256": "c23fcd63f23783eb5323b5cb0fa95afbd65ab3ccd5787e7766bb02a64d4d28a8",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/pixel-inspection.json",
          "sha256": "64b5fbf4938aaaaea10740800acc160d99b01b7b71d10d2c9e23f41146f1fca5",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/preview.png",
          "sha256": "d119a5e9ff664ac2f3ed12377ea976c5a6526550c878be04fa96ac8e520cbbb7",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/profile-contract.json",
          "sha256": "fa9931d476bcc0437eefefc72cd3a604ac3f2754705e26b85f7557c31485e041",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/clay.png",
          "sha256": "9a7ca0ce3fcd8c8ce4522aabdf7f9d06147f8c21beae4758caa4e8c53a6c5f49",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/front.png",
          "sha256": "c520f8217d2a717b74ae8fc9d40e4b4875de687f397214a10aa5abc798802d2f",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/hero.png",
          "sha256": "d119a5e9ff664ac2f3ed12377ea976c5a6526550c878be04fa96ac8e520cbbb7",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/rear.png",
          "sha256": "4c7b7070af25210b51421aa1d5b3fb621e0252d67aaf3adaa272799c9bd57995",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/render-manifest.json",
          "sha256": "c90b77a2f665d2451292f7423ddc52bb4bdf32609febee983e4bd83f49c74bfa",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/reversehero.png",
          "sha256": "e35c7e7190235b42227e29429568c9bc2edc94ab0322fa53c42ddb171c8e01eb",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/side.png",
          "sha256": "910cb5f0a8f97af3d656ebf4391bb6bc88a12cf08636af8e9c6e46e8633ccafe",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/silhouette.png",
          "sha256": "15ad901f59a12dfb85a66a0a8d46b0864da6f3cfcb3577af1370b7a86324829d",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/proof-final/top.png",
          "sha256": "8b90898c05cb5b9d33d39d7d3bfbda2a10a1fbb6044bad8d0f75d5f552bc3d55",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/references.json",
          "sha256": "95ba781b6d57af2a7ad0687215368403f3e72ac56f6842e46e73900683c471bf",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/repair-freeze.json",
          "sha256": "ed19e7b7292e4447590f2cc72caa70284bbf068da77f543ebbb6ba53a13ddd2e",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/repro-final-1.report.json",
          "sha256": "b8e0185294a133760b946c39a6e32b35fe04eced5bd3a24603a17bd3d0240b43",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/repro-final-2.report.json",
          "sha256": "2ea806ec0bd63582009529435eeccbf3bc4d107f24b0c169dd676c4edb530684",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/runtime-parse.report.json",
          "sha256": "2f378ac54f9ec4553efa7be1b788ce9cb0416325ce9e6462cf979a4eb1ae333c",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/source-final.report.json",
          "sha256": "4e70cec61ffa678fbeeb8cb40931841fa4ba6c5fc4867cd06af6c6a9e8a0c394",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/source-metrics.json",
          "sha256": "ff5bedf03e95cb17aa0d0f3c97c0f9df80a056a9cef561644d7e1fe4cc1464bd",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/source-vertex-counts.json",
          "sha256": "aa80798621b7a4ea9a6a6e826522ba4ef8a42dc6c0664462f448cbb5d13cfc4c",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/assets/playa-basin/r003/source.blend",
          "sha256": "316df62d699e2ebe609355d9f006ba972ef36833b2540ac96b03ededc323a959",
          "origin": "source",
          "owner": "playa-basin"
        },
        {
          "path": "production/small-life-batch82/check-physical-surfaces.py",
          "sha256": "470f371dabe34231ee0a3e4c6856e5ae57751300aa563eb2c53570f7bed11d42",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch82/publication-policy-reference.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch82/render-fixed8.py",
          "sha256": "02ac03daefa4ac6bf70b89bd85db2983724c7a05c3e2fcd9fe142f7a72b81ce0",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch82/runtime-parse.mjs",
          "sha256": "fb938eb6db606a51b904de3f58b2557b618fc5963bfcf225ad990b0b1244164c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/REPORT.md",
          "sha256": "0335e3346e5bb4e23e844b7569b4be3750d7fb0cb36b2fc485da2948ab23f11d",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/audit_inputs.py",
          "sha256": "2c57110a1b911eae0cd60a5f745521fed0e8fcd4bbdffa86aa2e081e6b174327",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/finalize_report.py",
          "sha256": "ab7528a18ae68173ff876d81a67cb4a26e7019770b816bbfc96e6d1bb9c5a546",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/handoff.json",
          "sha256": "d4bd9ec9e95e400cfafd64d3b87d63015c8c24de8852e9734de2302d7f3a8372",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/independent-qa.report.json",
          "sha256": "9a70e16bba928fe3ffb9fec5317ec0304a38e5ab60e7f86d3e194fe189ace753",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/own-evidence-manifest.json",
          "sha256": "4d95737bc4527be4422cdb9faf722118b31deaa10087bb8d658918d0a8e9d07a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/render_supplemental.py",
          "sha256": "7dee4ba7262de2ab4d43366ac4936f46fc5e5c802f2af6661c4168da86c48dcb",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/run_fresh_checks.py",
          "sha256": "16053ebcc1f2f2aeb8514af4ecea91eb62192681a022e90e3eb717d0f3338f88",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/runtime_checks.mjs",
          "sha256": "24410b47549728958e2de1e85f3912086229e25e899f0b3abd0d050020b16043",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82/source_reexport.py",
          "sha256": "7b05a23975f06492ea121238555f820fe2c31f3a0c75636c57d3f926b0750f2f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g11-release-20261021/process-archive-index.json",
          "sha256": "e92be56e6f4a358963cd0cdf4a878109f1f3b63e3eaeb300fd1a5b58f27e2b16",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g12-20261021.json",
      "sha256": "cafcf6533eae4da31c432e71f689f97b2648d4be10aae76f35452867f3ddf508"
    },
    "release": {
      "version": 1,
      "scope": "next52-g12-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "6f8cab54bd17583d3f8a5791713f9eb500459b48",
      "review_commit": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g12-release-20261021/source-bundle.json",
        "sha256": "087736d42d35dbf010aa35e90a5f55bbf1a0b51909401b4ddc7e29f046636a39"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
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
          "path": "scripts/rebuild_frozen_blender.py",
          "sha256": "c5971fab63b69fa3720d52b9884789eb56f6c2b1d2db4d6c9d3fa2bc77a59db6"
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
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/handoff.json",
          "sha256": "7b09be4995a5dadfaef6dd939b9ccf486a1b41ff66013c06223d4bacb89e9734"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/independent-qa.report.json",
          "sha256": "44e0100d76f808bee5ecf7f393bd3ebd40e0566492a656f7ef15113ba13ea7a9"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/own-evidence-manifest.json",
          "sha256": "3f1612bd7a70795a14df2104626b520e43639b6936a200e90a6b016233c0a016"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "stratovolcano",
          "batch": 82,
          "revision": "r009",
          "candidate_root": "production/batch82-stratovolcano-repair/stratovolcano/r009",
          "source_commit": "6f8cab54bd17583d3f8a5791713f9eb500459b48",
          "reviewed_source_commit": "1b8673e257f7376e4dd7b5967a35ec8bf0a9d0f0",
          "original_source_snapshot": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
          "review_commit": "667f54fc09d57c03c4bc1a62d19133bc069b4f95",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/stratovolcano/batch82-20261021/release-metadata.json",
            "sha256": "3019be5a57335fe2cd85ffda5c6541297f8cba447f4191c1f9f84589a9956576"
          },
          "candidate": {
            "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/candidate.json",
            "sha256": "e9c1b9573b0a4e059ae32d4b0dd478c7a94c3b045177c0ea76320ecf20e92f8f"
          },
          "active_candidate": {
            "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/candidate.json",
            "sha256": "e9c1b9573b0a4e059ae32d4b0dd478c7a94c3b045177c0ea76320ecf20e92f8f"
          },
          "original_profile": {
            "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/profile-contract.json",
            "sha256": "80898b53f4237b119eacf9647eefe0f0922825426286ea921e5f5f48f2c8a66d"
          },
          "active_profile": {
            "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/profile-contract.json",
            "sha256": "80898b53f4237b119eacf9647eefe0f0922825426286ea921e5f5f48f2c8a66d"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/independent-qa.report.json",
            "sha256": "44e0100d76f808bee5ecf7f393bd3ebd40e0566492a656f7ef15113ba13ea7a9"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/independent-qa.report.json",
            "sha256": "44e0100d76f808bee5ecf7f393bd3ebd40e0566492a656f7ef15113ba13ea7a9"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/independent-qa.report.json",
              "sha256": "44e0100d76f808bee5ecf7f393bd3ebd40e0566492a656f7ef15113ba13ea7a9"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/own-evidence-manifest.json",
              "sha256": "3f1612bd7a70795a14df2104626b520e43639b6936a200e90a6b016233c0a016"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/handoff.json",
              "sha256": "7b09be4995a5dadfaef6dd939b9ccf486a1b41ff66013c06223d4bacb89e9734"
            }
          ],
          "original_metrics": {
            "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/metrics.json",
            "sha256": "c91b87c53c0eed9f5fa93c5f7c9564f4bfd958d4a1bb11ee5aec5123b9513543"
          },
          "source_counts": {
            "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/source-vertex-counts.json",
            "sha256": "9ebeb756e232462b298ec48506f1efab409da62b9862262227c4508a84ac54c4"
          },
          "proof": {
            "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/render-manifest.json",
            "sha256": "2cb1dbf07496b31221d0d6d85d9a75c020d215f48491d0112c3302aee84f50c6"
          },
          "source_preview": {
            "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/preview.png",
            "sha256": "b7adc822be2f75b762cca9a7ba8f4ace359294c6f23ab50bff84a2e7dc317b51"
          },
          "capture_reference": {
            "path": "assets/additions/stratovolcano/batch82-20261021/stratovolcano.png",
            "sha256": "7f64371687c11807ed01451736e2c4bbcafe6ae9564e8d699a0746e58d7717b7"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/stratovolcano.json",
            "sha256": "ded6d17e6329c85b91cddcc5e80136e5fe5c8e983014c08ed6c961d6bb26a317"
          }
        }
      ],
      "files": [
        {
          "path": "production/batch82-stratovolcano-repair/check-physical-surfaces.py",
          "sha256": "470f371dabe34231ee0a3e4c6856e5ae57751300aa563eb2c53570f7bed11d42",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/count-source-vertices.py",
          "sha256": "9211091a8a90fdac820ae374478c7f4b28fe1e799a03b764f69aff7aba23c21f",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/legacy-profile-policy-reference.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/render-fixed8.py",
          "sha256": "02ac03daefa4ac6bf70b89bd85db2983724c7a05c3e2fcd9fe142f7a72b81ce0",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/runtime-parse.mjs",
          "sha256": "fb938eb6db606a51b904de3f58b2557b618fc5963bfcf225ad990b0b1244164c",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/source-reexport.py",
          "sha256": "b3d1df248cd30bcdd2e5941ddace47e63e750251a081b349a72c91b037679ad8",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/brief.md",
          "sha256": "7c5a9752cff91977732ad2de6d687259912de1b27fdc6dd6bb621830836769e8",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/build-config.json",
          "sha256": "afc1d3a74dd0ebbac3ffa6d806257c3f34ec26626100b8a879d1c26c3f26db88",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/build-dependencies.json",
          "sha256": "df67f9ef5e1a3a87169db20644a9549e14231c2998c8ace3fa7cc8204b3eacdb",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/candidate-brief.json",
          "sha256": "bd690d4909d9ae333bc3d16e04ac1bb9ab02a8a696dcf474e422f955c43eff45",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/candidate.json",
          "sha256": "e9c1b9573b0a4e059ae32d4b0dd478c7a94c3b045177c0ea76320ecf20e92f8f",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/concept-generation.json",
          "sha256": "ebe1fd448aee852e1c476375eed0dac65eae9b0563dfb0692ab2a5dfa9ff6ebf",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/concept-original.png",
          "sha256": "0060bcb028f42d61e05627fc997c99a165d311c60f7c1384d964e5e18e30286f",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/concept-prompt.txt",
          "sha256": "ded7393034bad979238e05d6c90507d7d9496b519a2c9d65197b9f0910d71fff",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/diagnostic-disposition.json",
          "sha256": "fb5a8326313e45f10b984ee2aebd3889466f4c6b301a311697470fa2a104ffb2",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/executed-rebuilds.json",
          "sha256": "24c6a00255db0926c4876171b7e124e094a4014e90fad514b2e35cd88ddd64cf",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/flank-network.json",
          "sha256": "98517565fdd8dae48da6979d8c47b86fc6b9beb1fd803d835b2c38aaedec8ecc",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/generator.py",
          "sha256": "62c9d749212993251225f358c6aa99277f4b58baeace9473b18ce938be517abe",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/gltf-validator.report.json",
          "sha256": "ad3fb54332bc710c6d35ce1c845ae613485893ed7d70f38a8b41fe208098d04d",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/lossless-sheet-check.json",
          "sha256": "f387b85477703a03c6b927a965bccd01e22047fd30a6ff1a2200b0e3e5860225",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/maker-review.md",
          "sha256": "3b44cfe40bf1357d539b27abac029dbc18ba46189a67dc7377467c7c8c0b40ad",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/metrics.json",
          "sha256": "c91b87c53c0eed9f5fa93c5f7c9564f4bfd958d4a1bb11ee5aec5123b9513543",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/model.glb",
          "sha256": "c49a55663c95bad0c4b537f51b611490897e1f3bfde8b839892d5a9573874998",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/original-modeling-freeze.json",
          "sha256": "b9801da9631035ec87f6ffd1a891297b179e4e6a4ba46e382365fc44926d4379",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/physical-surfaces.report.json",
          "sha256": "fc3cfbbf823b499f85a94b7489aa88912d1e8c57ccb17abb8f8686653e51176d",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/pixel-inspection.json",
          "sha256": "54b7f1abf355ee180b066cf41b945fa76f6a6e707deda8952c131e919c8c8115",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/premodel-schema-check.json",
          "sha256": "477306324306510f9ddbcf0b13e5637fe40b084c667ec66bcd74deeaabb0564a",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/preproof-binding.json",
          "sha256": "d9516c2d8181026aa101a2e004fd33bcbc491508a4d6cadf5b6c100ea8d1aadc",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/preview.png",
          "sha256": "b7adc822be2f75b762cca9a7ba8f4ace359294c6f23ab50bff84a2e7dc317b51",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/profile-contract.json",
          "sha256": "80898b53f4237b119eacf9647eefe0f0922825426286ea921e5f5f48f2c8a66d",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/clay.png",
          "sha256": "8a4d403d690b063463ef4aebedfbdedc2267183aa6c7975d6d80cfb9ea1b0aa0",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/front.png",
          "sha256": "d602cf167e8297e028d5a84b7b23c4692fc7bde9c6d3ede3ff239b778c13f6f7",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/hero.png",
          "sha256": "b7adc822be2f75b762cca9a7ba8f4ace359294c6f23ab50bff84a2e7dc317b51",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/rear.png",
          "sha256": "7d2f7197ab13e9f578cfa687093baaa9166aa1ab542c5fa2655c9a5576fef8a2",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/render-manifest.json",
          "sha256": "2cb1dbf07496b31221d0d6d85d9a75c020d215f48491d0112c3302aee84f50c6",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/reversehero.png",
          "sha256": "d022bde986094838bb41c57713281b36a84211f9af2c7194a64dc2c43ed0a52a",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/side.png",
          "sha256": "083c42159e069c507edfb9eb41e2ec713d55c48450d59987e17dfcd462ca32c1",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/silhouette.png",
          "sha256": "1e6ea2c445ed255220ccba546fc3175f03288c357b71eb8a3dc358ee3a693804",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/proof-final/top.png",
          "sha256": "54bf372ef62ce8a320fd647147f60a3e6325c9ffa5dd34e3b346bf960f030e23",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/qa.json",
          "sha256": "429ff8192af87e1ac859053b0ab865cc6afe72d9ea0df5e129c94b2e7a3b986e",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/references.json",
          "sha256": "ebce3fb83c8205a547fff0fd2e3fa6938f1a9c41552c7d39d66655955fd40d90",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/repair-freeze.json",
          "sha256": "52edbf8caa784497ff7e29f3c07468634d6b726884ab4839a291934cd1a4670d",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/repro-final-1.report.json",
          "sha256": "1da5e1677edbf7fa3a2105019d651aaa605ab6241c446f90bb85a78ff3cfd0ed",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/repro-final-2.report.json",
          "sha256": "6265e8cda10ee36a5249e2ad7f70e9ba26f36fcbccd17f80e888116be9c07329",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/runtime-parse.report.json",
          "sha256": "c9fbe2efd9ba6a774d944977bdbc416a4a4c0d330591dcfdfbfcbd412f9930a5",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/scope-and-regression.json",
          "sha256": "971619c306538b996bd8dfbd884b3bde8c31bac6461067597fbc58ef2d9b2db1",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/source-final.report.json",
          "sha256": "07be8bd1992b776830534ea1b7e77fe595aa69d9e4bc083933c134fc603026f9",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/source-metrics.json",
          "sha256": "ce3582232ef9b90e05de8821d13abe28b7d0ab763a286962f8a68672fb45ab7e",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/source-reexport.report.json",
          "sha256": "ec780f66e28e8e9557547fcbd62bd7b113c7f01b81f833c898859fbe57f6885a",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/source-vertex-counts.json",
          "sha256": "9ebeb756e232462b298ec48506f1efab409da62b9862262227c4508a84ac54c4",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "production/batch82-stratovolcano-repair/stratovolcano/r009/source.blend",
          "sha256": "7d4e1e0785dc35dea73119d004674f5d91f62cd516e26e90095abf3aebc5eedd",
          "origin": "source",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/REPORT.md",
          "sha256": "8701bc11e76bf92d0d695ed6b8b7417f61507b96dfb5bf9396eeaee6cb86a5e0",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/audit_inputs.py",
          "sha256": "a54492ee1f4e9484b87296a2d78ba57cd800e306db44b6a43ace5ae6ec222a52",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/finalize_report.py",
          "sha256": "c5dad96f8638c3944979010914c56fd88b4fe7ccd5f064e8c3b62f047b486131",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/handoff.json",
          "sha256": "7b09be4995a5dadfaef6dd939b9ccf486a1b41ff66013c06223d4bacb89e9734",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/independent-qa.report.json",
          "sha256": "44e0100d76f808bee5ecf7f393bd3ebd40e0566492a656f7ef15113ba13ea7a9",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/measure_difference.py",
          "sha256": "ebf59585e9d85f18af431726fe51ce03674c81a9e30667b5b2738716ea9e51c1",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/own-evidence-manifest.json",
          "sha256": "3f1612bd7a70795a14df2104626b520e43639b6936a200e90a6b016233c0a016",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/render_supplemental.py",
          "sha256": "7dee4ba7262de2ab4d43366ac4936f46fc5e5c802f2af6661c4168da86c48dcb",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/run_fresh.py",
          "sha256": "1b30595c9cbd31cd037f66e39d867db677f0fbdac0a8dc7c2065b3546688d27a",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/run_supplemental.py",
          "sha256": "f45a8553d3226d868d8e808231f1e76eafeac81ad5df9bb733d943c502538827",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/runtime_checks.mjs",
          "sha256": "bb838c8136734a7fa1e19df7a7b8e89e10dd23e5b5a82db1112487a697369931",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-82-stratovolcano-r009/source_reexport.py",
          "sha256": "7b05a23975f06492ea121238555f820fe2c31f3a0c75636c57d3f926b0750f2f",
          "origin": "review",
          "owner": "stratovolcano"
        },
        {
          "path": "qa/next52-g12-release-20261021/process-archive-index.json",
          "sha256": "6c6f9d362496f1b2369ea1bae2ee3bccad45e16a47598a65107087cb4f80be88",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g13-20261021.json",
      "sha256": "a08ea4edf6a7e0b0b572d436aea1cb0f19a4bb734d2df57e7108b7698f69f504"
    },
    "release": {
      "version": 1,
      "scope": "next52-g13-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
      "review_commit": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g13-release-20261021/source-bundle.json",
        "sha256": "665b4c9613908ebb4d5298c67fca0ee9115c048c1ae0fb7282f04fca89c9b56e"
      },
      "protected_source_inputs": [
        {
          "path": "package-lock.json",
          "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
        },
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
        },
        {
          "path": "scripts/qa_glb.py",
          "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round32-20261020/batch-79/OWNED_MANIFEST.json",
          "sha256": "e29cf588a1d807b02c9920db8ff7b1e896120b980c05d70a5163d3f9dc08dff3"
        },
        {
          "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
          "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "arroyo-wash",
          "batch": 79,
          "revision": "r005",
          "candidate_root": "production/small-life-batch79/assets/arroyo-wash/r005",
          "source_commit": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
          "reviewed_source_commit": "a545dcfd9af59623cd3e9265a7cb3b61ae0d6c9c",
          "original_source_snapshot": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
          "review_commit": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/arroyo-wash/batch79-20261021/release-metadata.json",
            "sha256": "fe61a70aba322741b82cd58ce967014eaa5a254f870764432a0b4faf199d358a"
          },
          "candidate": {
            "path": "production/small-life-batch79/assets/arroyo-wash/r005/candidate.json",
            "sha256": "32f1499c19b49ff84f70150cc25410e0ce9ebcc3febe642ec64c30696ca374a2"
          },
          "active_candidate": {
            "path": "production/small-life-batch79/assets/arroyo-wash/r005/candidate.json",
            "sha256": "32f1499c19b49ff84f70150cc25410e0ce9ebcc3febe642ec64c30696ca374a2"
          },
          "original_profile": {
            "path": "production/small-life-batch79/assets/arroyo-wash/r005/profile-contract.json",
            "sha256": "ccb0d337878ec9af02f4384783619b9b24124d7eb1a932f5a6baa25c72aa7e14"
          },
          "active_profile": {
            "path": "production/small-life-batch79/assets/arroyo-wash/r005/profile-contract.json",
            "sha256": "ccb0d337878ec9af02f4384783619b9b24124d7eb1a932f5a6baa25c72aa7e14"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
            "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
            "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
              "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
            },
            {
              "path": "qa/continuous-small-life-round32-20261020/batch-79/OWNED_MANIFEST.json",
              "sha256": "e29cf588a1d807b02c9920db8ff7b1e896120b980c05d70a5163d3f9dc08dff3"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch79/assets/arroyo-wash/r005/metrics.json",
            "sha256": "1ea1844ee0daf1be49c990c4f140ca2eef96457ff641303106bf396ac6ef4a7d"
          },
          "source_counts": {
            "path": "production/small-life-batch79/assets/arroyo-wash/r005/source-vertex-counts.json",
            "sha256": "13151b2ca87475388bb8645d960a2d0144ccc5fcf16e44d05a1b9ddddeadb908"
          },
          "proof": {
            "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/render-manifest.json",
            "sha256": "df79cc9267c6efbf0eb002e425f0c96bb714f307520ebaf6a96e92bb06507ed0"
          },
          "source_preview": {
            "path": "production/small-life-batch79/assets/arroyo-wash/r005/preview.png",
            "sha256": "5fbcd14f18ba71c02097436ec47fde66a39eb580837861cee0a9afc8028406a7"
          },
          "capture_reference": {
            "path": "assets/additions/arroyo-wash/batch79-20261021/arroyo-wash.png",
            "sha256": "facc20fd402cfe044addb9c17c343ec3897ff2c851e9a175f3103f42b9a8fdc0"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/arroyo-wash.json",
            "sha256": "2584d821bc03b3249f436dde425baf3a15ab1aa0f611ea26f6a9252fd56ae49b"
          }
        },
        {
          "id": "dickinsonia",
          "batch": 79,
          "revision": "r006",
          "candidate_root": "production/small-life-batch79/assets/dickinsonia/r006",
          "source_commit": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
          "reviewed_source_commit": "a545dcfd9af59623cd3e9265a7cb3b61ae0d6c9c",
          "original_source_snapshot": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
          "review_commit": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/dickinsonia/batch79-20261021/release-metadata.json",
            "sha256": "ed4d2535fda66874afb074f3f4dbbc670bc936426659f44489b4431ea8758b7a"
          },
          "candidate": {
            "path": "production/small-life-batch79/assets/dickinsonia/r006/candidate.json",
            "sha256": "cede2985caaff8da8539bb519b7d40e98b4b4731b430c62d89fa7739d1cb201a"
          },
          "active_candidate": {
            "path": "production/small-life-batch79/assets/dickinsonia/r006/candidate.json",
            "sha256": "cede2985caaff8da8539bb519b7d40e98b4b4731b430c62d89fa7739d1cb201a"
          },
          "original_profile": {
            "path": "production/small-life-batch79/assets/dickinsonia/r006/profile-contract.json",
            "sha256": "145cd1d9e7e7423d5c01271a70d2937e3f5cd6ac53f57d837b644e1da67c9673"
          },
          "active_profile": {
            "path": "production/small-life-batch79/assets/dickinsonia/r006/profile-contract.json",
            "sha256": "145cd1d9e7e7423d5c01271a70d2937e3f5cd6ac53f57d837b644e1da67c9673"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
            "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
            "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
              "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
            },
            {
              "path": "qa/continuous-small-life-round32-20261020/batch-79/OWNED_MANIFEST.json",
              "sha256": "e29cf588a1d807b02c9920db8ff7b1e896120b980c05d70a5163d3f9dc08dff3"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch79/assets/dickinsonia/r006/metrics.json",
            "sha256": "b62f095186e87110cb50f29e77ca8af5a5f2aedc54dd9441dfbe4b8cdada377b"
          },
          "source_counts": {
            "path": "production/small-life-batch79/assets/dickinsonia/r006/source-vertex-counts.json",
            "sha256": "2f93f14d7368ea623fc5c0e444d2b28c36f59f62ee1b7cf922c6b23b57d722ac"
          },
          "proof": {
            "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/render-manifest.json",
            "sha256": "34b14b3cf8b42d418e2a407b4754eecad5d9deeaa9b1190322f2e1ed53489375"
          },
          "source_preview": {
            "path": "production/small-life-batch79/assets/dickinsonia/r006/preview.png",
            "sha256": "0d4e63f8eb52bc27c847a62235165aea57297cdcf2239fe9ec33948851e6baf5"
          },
          "capture_reference": {
            "path": "assets/additions/dickinsonia/batch79-20261021/dickinsonia.png",
            "sha256": "b1ed21f25250bba552c39abdad37a687b599d40943efbe3a7e9820ffe396ed86"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/dickinsonia.json",
            "sha256": "f34e0534cf0f9c1f06a6c4d308c5a889900b65b9b55d4f29f802967410d4e4db"
          }
        },
        {
          "id": "shield-volcano",
          "batch": 79,
          "revision": "r003",
          "candidate_root": "production/small-life-batch79/assets/shield-volcano/r003",
          "source_commit": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
          "reviewed_source_commit": "a545dcfd9af59623cd3e9265a7cb3b61ae0d6c9c",
          "original_source_snapshot": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
          "review_commit": "7b223cb128101d2ffd4c5bdaf1725205b53aa1ef",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/shield-volcano/batch79-20261021/release-metadata.json",
            "sha256": "c94ec897b29c5ac134f6e82b2ffad6ee69a2e1ee0a57277dbdfb96206ef8febf"
          },
          "candidate": {
            "path": "production/small-life-batch79/assets/shield-volcano/r003/candidate.json",
            "sha256": "1ac1de544d948db51d3ef09e463566d35a65d4e22d80b8c1b62861d147de9f47"
          },
          "active_candidate": {
            "path": "production/small-life-batch79/assets/shield-volcano/r003/candidate.json",
            "sha256": "1ac1de544d948db51d3ef09e463566d35a65d4e22d80b8c1b62861d147de9f47"
          },
          "original_profile": {
            "path": "production/small-life-batch79/assets/shield-volcano/r003/profile-contract.json",
            "sha256": "cc78e7f2720a26d9d50994f3d1364e8bc69777c4d95a5c73f6babc98670aeea5"
          },
          "active_profile": {
            "path": "production/small-life-batch79/assets/shield-volcano/r003/profile-contract.json",
            "sha256": "cc78e7f2720a26d9d50994f3d1364e8bc69777c4d95a5c73f6babc98670aeea5"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
            "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
            "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
              "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac"
            },
            {
              "path": "qa/continuous-small-life-round32-20261020/batch-79/OWNED_MANIFEST.json",
              "sha256": "e29cf588a1d807b02c9920db8ff7b1e896120b980c05d70a5163d3f9dc08dff3"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch79/assets/shield-volcano/r003/metrics.json",
            "sha256": "75da472dc9756c739ea2332aa703fd203abb51f16bb1e81968b62de93a71c5e5"
          },
          "source_counts": {
            "path": "production/small-life-batch79/assets/shield-volcano/r003/source-vertex-counts.json",
            "sha256": "4eaee12db911a71a6e18cc53f07f01d07012ade2ca77e6482abb2c7a2e36c3e3"
          },
          "proof": {
            "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/render-manifest.json",
            "sha256": "8eb59f93c186a2e390c19dd42ab521ac99c84bb5490583f5df6e3b24b4224f36"
          },
          "source_preview": {
            "path": "production/small-life-batch79/assets/shield-volcano/r003/preview.png",
            "sha256": "dc2ca777df6c8a4e135035ee548645156d795d2fb868e82fe450b480e32746a3"
          },
          "capture_reference": {
            "path": "assets/additions/shield-volcano/batch79-20261021/shield-volcano.png",
            "sha256": "6760aef7eaf6b4330c3799f6708f3b7b6d86121342eec4b2078bc46a26cae6b5"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/shield-volcano.json",
            "sha256": "bf8d5b1089db74bac9d618c8481a33e3b626b763677ae034894c4021abd7fa4c"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/brief.md",
          "sha256": "0c39abf0274dbd1d769356674208802f76a38e4681333b129520d744d2f5071b",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/build-config.json",
          "sha256": "b6d540f6d2fbb999125cee4b45bb94542e92b38a465306ede91172f4a5d3b49b",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/build-dependencies.json",
          "sha256": "1ca1e670135547311dd8fc184f454e5314da278fe7318d913d0569b67db07ff6",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/candidate-brief.json",
          "sha256": "49dcb0eff166b0d57341b01029fe7df92d98a48e632bd40774f23335530746dd",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/candidate.json",
          "sha256": "32f1499c19b49ff84f70150cc25410e0ce9ebcc3febe642ec64c30696ca374a2",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/concept-original.png",
          "sha256": "775cfa6a8c191d8865b5c503f95f7b3795240e12b82fde1abe1ec235ee50e10a",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/concept-prompt.txt",
          "sha256": "caa57de3b8a91c7bf1c135f55f4d0e0e65592de541486128f10571cf1489b619",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/contact-sheet.png",
          "sha256": "9f11739e47d941814f9747dae27a4b8af06bf6b6c1985e972571d0f04224d4ee",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/final-rebuild-binding.json",
          "sha256": "554e316e67f3d3ee46ae218581c5cba7ccc6b020ba409f1933bfbeb42dbbe2d8",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/generator.py",
          "sha256": "452163d1b62c3bc174c9cd6caf94e7cb1adfe21fbd35a2a17aa2ade2055bdf72",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/gltf-validator.report.json",
          "sha256": "1549d5dc0492b7ea073a9674d86b14e938bf64779ecc90baf13df35f50ebc013",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/lifecycle.jsonl",
          "sha256": "61d9a5d139463f5ecbbfe2a627b36f2499a9cd160a1fb436f71e0d9741229721",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/maker-review.md",
          "sha256": "a7a843daced74c6565e9e4906b52a7727a6b5aa48f5b2ad75edfacbe33d922f3",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/metrics.json",
          "sha256": "1ea1844ee0daf1be49c990c4f140ca2eef96457ff641303106bf396ac6ef4a7d",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/model.glb",
          "sha256": "92dddf56297b9def8870405ac53b6d31ddddd18bc466ab3af827e92b2b82c3c1",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/modeling-freeze.json",
          "sha256": "d7940409879316d118bc002db232d977d863946d0f8866c7c813fd7e85398f94",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/physical-surfaces.report.json",
          "sha256": "6973900f7a3ceeabc0cd148ee33c9f1931d5cf8f7caad36806799932221d037b",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/pixel-inspection.json",
          "sha256": "f41950c6e5dfb92dd945da653d746a46386a84b7611ee938d8b4b9fb09caaf12",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/preview.png",
          "sha256": "5fbcd14f18ba71c02097436ec47fde66a39eb580837861cee0a9afc8028406a7",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/profile-contract.json",
          "sha256": "ccb0d337878ec9af02f4384783619b9b24124d7eb1a932f5a6baa25c72aa7e14",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/clay.png",
          "sha256": "ad92ebf0ef717756af49b983aeeb5ff4749fd37b8258aa0dda3604b3b3fb70e7",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/front.png",
          "sha256": "544aeceb67d946c94bb097735774bed247a00524921ede23e64f001fa5d00440",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/hero.png",
          "sha256": "5fbcd14f18ba71c02097436ec47fde66a39eb580837861cee0a9afc8028406a7",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/rear.png",
          "sha256": "1e7412b72c9c9cca980997941c94ebeae7a19c126ee20307064e5ac24406fe99",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/render-manifest.json",
          "sha256": "df79cc9267c6efbf0eb002e425f0c96bb714f307520ebaf6a96e92bb06507ed0",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/reversehero.png",
          "sha256": "8a979622eb5ea600ae73cf09f33126d19a58fbfdd27fcda3929e59c7f3f6482b",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/side.png",
          "sha256": "b9c4add8216a4a6c6dbca3556569c2507225a181fe70d315df5951a6f79dafb1",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/silhouette.png",
          "sha256": "1a7ea5ae66e93ff31dc6ae6ed24a4a69fc260365e79aa9db72666d8e4f1f4581",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/proof-final/top.png",
          "sha256": "47b9d89f38f9d0421512c86669383d29f91b1cb983a1a7db4fceeea59bd1b470",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/references.json",
          "sha256": "42ec36a413b8372be11ca62d418d446142dc0244fc589ecf81ff8f72c4b2c243",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/repair-freeze.json",
          "sha256": "8523d9ead187160a86981a056d93c0d613f9d070835c3ab0b9f842e60945240b",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/repro-final-1.report.json",
          "sha256": "40c4c1fe292809d442d0947a014e04d736b4cc3fe39e7090682c0bb678f22dd0",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/repro-final-2.report.json",
          "sha256": "46bbb1ed8388f51e3cdc7fa34ad79cf60de2e107255403406b4e6ca22c72e99d",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/runtime-parse.report.json",
          "sha256": "72df7f52bb9ceaa303a67333a626591e05383f69b8dd95af2b3e530558537e94",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/source-final.report.json",
          "sha256": "978189bad5732c2ca0f9c8d1b598888216bd0ceefb130179a44f248a66d467b8",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/source-metrics.json",
          "sha256": "447fea4d72a6e650518b5e3fcb1be5f38f50edd655e12ff53d709e2ebbe23a0a",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/source-vertex-counts.json",
          "sha256": "13151b2ca87475388bb8645d960a2d0144ccc5fcf16e44d05a1b9ddddeadb908",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/arroyo-wash/r005/source.blend",
          "sha256": "d0fbf329907868da8386567e08be15e4784867aef2b692f3fee030af5be8ce8d",
          "origin": "source",
          "owner": "arroyo-wash"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/brief.md",
          "sha256": "efff6762fa2380116db2a79392c98f4078b52bdf07e98e968ce64eb73f715307",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/build-config.json",
          "sha256": "32d046cdc662e2994bc1e63b2042fb7734b1197f054a23af52b956e6339de84f",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/build-dependencies.json",
          "sha256": "84fd9ac71ffee6a0ddf83752aad5c6f849262a418f0225dc420683c17b68fd53",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/candidate-brief.json",
          "sha256": "eb9be8f5f2cbf5ee585b351235dde411d7b298345ea4cd1c07207c11a4083320",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/candidate.json",
          "sha256": "cede2985caaff8da8539bb519b7d40e98b4b4731b430c62d89fa7739d1cb201a",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/concept-original.png",
          "sha256": "874700b8e9fd23420007e88d0b829e9ca2c92dd353d0491d8f60969f1547b63c",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/concept-prompt.txt",
          "sha256": "fc2ac2088f1e3432911cfb5bc4c75fd86397c9f72ffb88c30755d86589ae2518",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/contact-sheet.png",
          "sha256": "9f57e14ac31c33d2d9ff73cfc83da74849224c29955958031a084c31d500225b",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/final-rebuild-binding.json",
          "sha256": "e3af9bd536023a348022de6880e53f569aa52e3e831fa4c6cf0801fac7fa946d",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/generator.py",
          "sha256": "d03bc8fdf5e6be037d76208e887b66a032b107def60c7139072fbc52bb9ad8ec",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/gltf-validator.report.json",
          "sha256": "4cd451e07d1400f0dbca2267dd9441a5ee5196403a6ed0ebc884cc1b5aac37ea",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/lifecycle.jsonl",
          "sha256": "39849e71253948bd0db43cc78583cc94628fef6a6fcfad8c18dc2d96c3e498ad",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/maker-review.md",
          "sha256": "6f775d1cb2181d2615d17d67db4dd98674ceb5e0f3cf72fe4549a38afaa5c9dd",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/metrics.json",
          "sha256": "b62f095186e87110cb50f29e77ca8af5a5f2aedc54dd9441dfbe4b8cdada377b",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/model.glb",
          "sha256": "6a480a166adc2447f5541fe0b74ebba713498eadddc300f3bcf9ba351ad07728",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/modeling-freeze.json",
          "sha256": "ee8cf0e7854f2fac0f68ddeeddb7700a544a33b6078e6786613c8d870a608fb5",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/physical-surfaces.report.json",
          "sha256": "79d7bc43fdb1cab9622cc115c6115b0dea5517d2eec4ca9bda3d98fa188cad7a",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/pixel-inspection.json",
          "sha256": "4193250a26ee47d22eb8408e7f9b65a9f30694bf45532f1375fa8dd240758f36",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/preview.png",
          "sha256": "0d4e63f8eb52bc27c847a62235165aea57297cdcf2239fe9ec33948851e6baf5",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/profile-contract.json",
          "sha256": "145cd1d9e7e7423d5c01271a70d2937e3f5cd6ac53f57d837b644e1da67c9673",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/clay.png",
          "sha256": "586d29b1daa5872d4dfa17739c26ea5a0e94b1cfa4f0bb2332c3b539f29a94ea",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/front.png",
          "sha256": "375db4b5fd2806e0a1edb42d12f302e4d669efb37229016a96dfc898d8643860",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/hero.png",
          "sha256": "0d4e63f8eb52bc27c847a62235165aea57297cdcf2239fe9ec33948851e6baf5",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/rear.png",
          "sha256": "aacfd8f2d78c6b198728bb1a6c1cfd6157ed920a3c5d970bd4a2ad990e988ae2",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/render-manifest.json",
          "sha256": "34b14b3cf8b42d418e2a407b4754eecad5d9deeaa9b1190322f2e1ed53489375",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/reversehero.png",
          "sha256": "3a7dc74ddb31fbc2cf97b95662736da4c35a966f8cd1bb609956ee3d39aeb0d6",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/side.png",
          "sha256": "b505fff0606a7a7866464d3ac4dea854801a6846c0f49155278fd7311b625c3a",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/silhouette.png",
          "sha256": "f9d50cea7d5ef60382f19ca5f83876849ca3f552d50a53b4ccd5cc06ecf7537c",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/proof-final/top.png",
          "sha256": "b4cf8dacc9e558f8457bc36ae2f06a2ad329baa557bf6af32c1c203903688d3d",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/references.json",
          "sha256": "cd3cf4276d34d1191a228b906790a47d1d8cdca54d4bbd82dd47fb578ed5e597",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/repair-freeze.json",
          "sha256": "7b01728f5cfca039538cb6018f439bb0f6cfd0a165f2b65795bf12cee88aca55",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/repro-final-1.report.json",
          "sha256": "19f25719da158bcab98e62f66eb8db9214a07f8bb25a60e34d07ded11736414b",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/repro-final-2.report.json",
          "sha256": "0be2b789155e256f2f6981a44629836502dffebd0f291bebb73cf26d67c53a8b",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/runtime-parse.report.json",
          "sha256": "b7736d792769eb600223026a1781f7d3ae20369f5ac96f054c712661f0b60ba3",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/source-final.report.json",
          "sha256": "2da071ed2b199420125b8d107fa2dbcf4f0811117c0cb785276567c04a8d5ae7",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/source-metrics.json",
          "sha256": "037e815e8ee8d6507d43f38d8abf2f525ed95a45764da7315245753ae2b60d13",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/source-vertex-counts.json",
          "sha256": "2f93f14d7368ea623fc5c0e444d2b28c36f59f62ee1b7cf922c6b23b57d722ac",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/dickinsonia/r006/source.blend",
          "sha256": "2e760677533369f45fb97a2f275bd6a4abf05d4b1cc7cd6a7fe350f91180ce26",
          "origin": "source",
          "owner": "dickinsonia"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/brief.md",
          "sha256": "72d28314da4b0b1e9bfe3b96cede70322a517cfdf0dd58ba3882f196451291e4",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/build-config.json",
          "sha256": "5db3e63c6ffca9d2eeca5b9d9a69e5e4b157567e3cbcb44d792515e137440f63",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/build-dependencies.json",
          "sha256": "9d1feb43e7a952c5e661eda16a916a974f50e7111c56fddbf586fc6352770312",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/candidate-brief.json",
          "sha256": "3ceb0e0b76b9624fd442df423c9dbb9c1306f172126b9370fa52fb648bb5c3c4",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/candidate.json",
          "sha256": "1ac1de544d948db51d3ef09e463566d35a65d4e22d80b8c1b62861d147de9f47",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/concept-original.png",
          "sha256": "9aaf919d2c9a4f485fbdc079658009929e1a7f1f2eeb6c32a1d0ae1fa2bc6d41",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/concept-prompt.txt",
          "sha256": "1e26211e2562f9aa11000472f0916ad3aa7a9991e549257092aa8d25424b24ad",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/contact-sheet.png",
          "sha256": "f1049bbf98c97383b36898491c11db3ea221802336458f44a9b8e98cc57aa29f",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/final-rebuild-binding.json",
          "sha256": "64c32bc51d968d7e5c6c980e3f250a54794db7f57c90e5249a7d34eeabe86cba",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/generator.py",
          "sha256": "6bd4b6cd4caaff071b6cb948dc5f951a1d0048c98faf3774b0a8a02455c2a80a",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/gltf-validator.report.json",
          "sha256": "971685839e0b8530c81ff6c068c26f911492397b469f5529e81cba9d38408153",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/lifecycle.jsonl",
          "sha256": "daa3e0b8dcd1d84e4b225f86238c738426ee6496c5b4e4c0c10269cba3c335f7",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/maker-review.md",
          "sha256": "10f440321c5a11890b9ad004808cba7c725827d93d8d2133e56258c1fdbbf457",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/metrics.json",
          "sha256": "75da472dc9756c739ea2332aa703fd203abb51f16bb1e81968b62de93a71c5e5",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/model.glb",
          "sha256": "6d1b61ad7e87c8cd5ed8c8b3045ec2004332283f4d7a0d0017b06e9f5675567d",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/modeling-freeze.json",
          "sha256": "98b07e453bf2ebf046471a37fb89bc939878ffd7a6a56e39e97c7b361bd8f92a",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/physical-surfaces.report.json",
          "sha256": "156f4b68f3a1e7b86abbe9223c553810436e46fd8ffecaa1ac225fbf6de86c6b",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/pixel-inspection.json",
          "sha256": "abd18591299f6988eb7917f7187f1005510e2c017a0726cda29e9736ea8ff499",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/preview.png",
          "sha256": "dc2ca777df6c8a4e135035ee548645156d795d2fb868e82fe450b480e32746a3",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/profile-contract.json",
          "sha256": "cc78e7f2720a26d9d50994f3d1364e8bc69777c4d95a5c73f6babc98670aeea5",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/clay.png",
          "sha256": "ebd06b86527b2d0cf749c8d19c978acecba921a973d487dd94d203a549046326",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/front.png",
          "sha256": "e014d8d0c381fbe47b3394ea894d2d492f8994b05fd6bdb6f6068073dcc320fc",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/hero.png",
          "sha256": "dc2ca777df6c8a4e135035ee548645156d795d2fb868e82fe450b480e32746a3",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/rear.png",
          "sha256": "33b7c552e254359706d0006ff00dc73e95ca0138b34558284a2173232f11a124",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/render-manifest.json",
          "sha256": "8eb59f93c186a2e390c19dd42ab521ac99c84bb5490583f5df6e3b24b4224f36",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/reversehero.png",
          "sha256": "8ff04eff2bca5d064df50cccda41ae1fee779e423e5e748cc558dbf41e324711",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/side.png",
          "sha256": "2af0d9b62c1128ce25dbae56774f885508175418c5ebf836ef3844bd942ad783",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/silhouette.png",
          "sha256": "e4b8d716cf82d447ef1725d6bb5f1a8d042993c449efe1094a7f7a96438ceb6c",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/proof-final/top.png",
          "sha256": "ea08d5ef0397f93ae51345bfb5538c82f11d1c78fb2a2815a085e29ff19dfdc0",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/references.json",
          "sha256": "4d60591e1958c812418efa5dd11cf06d7680e1010c451fb84bd30e768bce0838",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/repair-freeze.json",
          "sha256": "0c51433ec0975277ba249b0c85b7488e023d864a5b16be16ccccdb8f341a9573",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/repro-final-1.report.json",
          "sha256": "cc3f5acda5ecdc1133a53050826b5344e546c38363f1168d51c6f61fe2f61b8b",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/repro-final-2.report.json",
          "sha256": "3be9208a1a07f943715b4a6f72b3af79b6e9afa5733c7fa5ced3c073d3e19f6a",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/runtime-parse.report.json",
          "sha256": "6bd15289bada77220f22a249f9710d1ebe394721d3c51ddc735d60b713be5ff3",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/source-final.report.json",
          "sha256": "6e93b5044942267f7debe2253794ddcf591db36c278790f4d38abb0f47868d18",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/source-metrics.json",
          "sha256": "c3fa857b43e0fc2b1158c6273f962ce50944b0c892e2e5c6e8262977c358cd1b",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/source-vertex-counts.json",
          "sha256": "4eaee12db911a71a6e18cc53f07f01d07012ade2ca77e6482abb2c7a2e36c3e3",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/assets/shield-volcano/r003/source.blend",
          "sha256": "9a22a04ac3a2af606bc426b03e1e458bafedbcc92a821f3fc213c080ffb61e90",
          "origin": "source",
          "owner": "shield-volcano"
        },
        {
          "path": "production/small-life-batch79/publication-policy-reference.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round32-20261020/batch-79/OWNED_MANIFEST.json",
          "sha256": "e29cf588a1d807b02c9920db8ff7b1e896120b980c05d70a5163d3f9dc08dff3",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round32-20261020/batch-79/SUMMARY.md",
          "sha256": "6d40daec6184a84649e9f275548c92b2212202692eff7536c78bfdb4bef61aab",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round32-20261020/batch-79/independent-report.json",
          "sha256": "dffc6eb73cafb23f92ced50954e2e270331af4e9ebd4d80424e9645f09c1e6ac",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g13-release-20261021/process-archive-index.json",
          "sha256": "d5008b26a6aa4a336d8d5783c3425c6491b57a77246dc2274a90063a504720cd",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g14-20261021.json",
      "sha256": "b17cd369af8907a7f2aab5f458d3d489b0a4465d1f608e402df36141ac1a7670"
    },
    "release": {
      "version": 1,
      "scope": "next52-g14-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
      "review_commit": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g14-release-20261021/source-bundle.json",
        "sha256": "632ff631e33abe06da352481177db5a479ea096eb56e14ed463f3c5ce29086d4"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
        },
        {
          "path": "scripts/qa_glb.py",
          "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/handoff.json",
          "sha256": "c3f2af4fcbe9441a8bbdc0274b4e7cdd37f76cda9958d650ded7b7aac6083b72"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
          "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/own-evidence-manifest.json",
          "sha256": "b280ca57f742f67ebce68629fd08929a12829b1ced4ff0d184a674b946484260"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "beach-cusp-field",
          "batch": 86,
          "revision": "r003",
          "candidate_root": "production/batch86/assets/beach-cusp-field/r003",
          "source_commit": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
          "reviewed_source_commit": "671bd5145dedae9ec7802a35069f81ab9eefcbf5",
          "original_source_snapshot": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
          "review_commit": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/beach-cusp-field/batch86-20261021/release-metadata.json",
            "sha256": "c96c2c34dffd46d2a9551e22fcb07ef828d3c2661d8bda574d68932113dca321"
          },
          "candidate": {
            "path": "production/batch86/assets/beach-cusp-field/r003/candidate.json",
            "sha256": "5d17de85fe97eb0b7e6d4c2332f89685263809da63317bc59ad86ebcbb441343"
          },
          "active_candidate": {
            "path": "production/batch86/assets/beach-cusp-field/r003/candidate.json",
            "sha256": "5d17de85fe97eb0b7e6d4c2332f89685263809da63317bc59ad86ebcbb441343"
          },
          "original_profile": {
            "path": "production/batch86/assets/beach-cusp-field/r003/profile-contract.json",
            "sha256": "6196ee4d26239f88f25dc9a3728e6199811206080338d8394d08a57ba35b524e"
          },
          "active_profile": {
            "path": "production/batch86/assets/beach-cusp-field/r003/profile-contract.json",
            "sha256": "6196ee4d26239f88f25dc9a3728e6199811206080338d8394d08a57ba35b524e"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
            "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
            "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
              "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-86/own-evidence-manifest.json",
              "sha256": "b280ca57f742f67ebce68629fd08929a12829b1ced4ff0d184a674b946484260"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-86/handoff.json",
              "sha256": "c3f2af4fcbe9441a8bbdc0274b4e7cdd37f76cda9958d650ded7b7aac6083b72"
            }
          ],
          "original_metrics": {
            "path": "production/batch86/assets/beach-cusp-field/r003/metrics.json",
            "sha256": "3e08e0c36704ff26863f5f1eef54c989ab1478ad6d764ea8d892c9c86e01ced7"
          },
          "source_counts": {
            "path": "production/batch86/assets/beach-cusp-field/r003/source-vertex-counts.json",
            "sha256": "60f23905f0e9b30bce49f70d7a354654622152413334751d64dcaff48e7c35ce"
          },
          "proof": {
            "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/render-manifest.json",
            "sha256": "faaf7c5c7e676921cacf1f216197e441f4e407a4cc83436ead75bc397b572762"
          },
          "source_preview": {
            "path": "production/batch86/assets/beach-cusp-field/r003/preview.png",
            "sha256": "8432fca568dc01582a615404d65f7d3587f67f81f99760ca4546aa7feb234878"
          },
          "capture_reference": {
            "path": "assets/additions/beach-cusp-field/batch86-20261021/beach-cusp-field.png",
            "sha256": "82db37819ee25baf7ccd677f6c5013aaefd1d35453afb9bb78692e16f3e86184"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/beach-cusp-field.json",
            "sha256": "551cf4faee00edeec4c16b79eacf17466187edee2a598dc2a203c7d29c9af5bc"
          }
        },
        {
          "id": "cinder-cone",
          "batch": 86,
          "revision": "r001",
          "candidate_root": "production/batch86/assets/cinder-cone/r001",
          "source_commit": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
          "reviewed_source_commit": "671bd5145dedae9ec7802a35069f81ab9eefcbf5",
          "original_source_snapshot": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
          "review_commit": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/cinder-cone/batch86-20261021/release-metadata.json",
            "sha256": "5d2e15404583a666ab7065e05bd9609220521861d67af8bd759c8842b2824a57"
          },
          "candidate": {
            "path": "production/batch86/assets/cinder-cone/r001/candidate.json",
            "sha256": "86e9207e25d2c4b54735e32b8d0b023725d04b143ef7a9fc6e1fef6c498e115b"
          },
          "active_candidate": {
            "path": "production/batch86/assets/cinder-cone/r001/candidate.json",
            "sha256": "86e9207e25d2c4b54735e32b8d0b023725d04b143ef7a9fc6e1fef6c498e115b"
          },
          "original_profile": {
            "path": "production/batch86/assets/cinder-cone/r001/profile-contract.json",
            "sha256": "8b5b3b083825eb91e9e6a278147c163ff41aa73dff5331a00b5baa2d81d164f3"
          },
          "active_profile": {
            "path": "production/batch86/assets/cinder-cone/r001/profile-contract.json",
            "sha256": "8b5b3b083825eb91e9e6a278147c163ff41aa73dff5331a00b5baa2d81d164f3"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
            "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
            "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
              "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-86/own-evidence-manifest.json",
              "sha256": "b280ca57f742f67ebce68629fd08929a12829b1ced4ff0d184a674b946484260"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-86/handoff.json",
              "sha256": "c3f2af4fcbe9441a8bbdc0274b4e7cdd37f76cda9958d650ded7b7aac6083b72"
            }
          ],
          "original_metrics": {
            "path": "production/batch86/assets/cinder-cone/r001/metrics.json",
            "sha256": "ba30decbdc843042df73c343aaa46eaec9c0fd1c94d5762aa8c7c491140f8df0"
          },
          "source_counts": {
            "path": "production/batch86/assets/cinder-cone/r001/source-vertex-counts.json",
            "sha256": "d6dd0332651b805d94c3d43e5c7297dbfb0d2e7425242dd33221e5a4bb44c922"
          },
          "proof": {
            "path": "production/batch86/assets/cinder-cone/r001/proof-final/render-manifest.json",
            "sha256": "1642913d7dac49828e0b1211a2fc361d941d500be736b91694ad59a68347e700"
          },
          "source_preview": {
            "path": "production/batch86/assets/cinder-cone/r001/preview.png",
            "sha256": "653a32a23d3106f74cdc024189fe8704e94047d62fb86d74b85c3058cec32c73"
          },
          "capture_reference": {
            "path": "assets/additions/cinder-cone/batch86-20261021/cinder-cone.png",
            "sha256": "8fca0ecb9809051431d155f2ed33faa72b72822e97c005d198bdd58adf1a626b"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/cinder-cone.json",
            "sha256": "f14a4abc3ad876942a91ad5bd61827b6d46ef9a42eb04d60b586f46f0abaf918"
          }
        },
        {
          "id": "tower-karst",
          "batch": 86,
          "revision": "r003",
          "candidate_root": "production/batch86/assets/tower-karst/r003",
          "source_commit": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
          "reviewed_source_commit": "671bd5145dedae9ec7802a35069f81ab9eefcbf5",
          "original_source_snapshot": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
          "review_commit": "7d2243195a1fc19f216140eae2f8eca6916f68ff",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/tower-karst/batch86-20261021/release-metadata.json",
            "sha256": "67e6219b6823a114a3100e8505adfba53a51a886f5557db2d9fcd4df3b6b0ba2"
          },
          "candidate": {
            "path": "production/batch86/assets/tower-karst/r003/candidate.json",
            "sha256": "0440010c1216f9bfa4872eea52f91aa5e85c5eb558a28468afc8d932aa056d51"
          },
          "active_candidate": {
            "path": "production/batch86/assets/tower-karst/r003/candidate.json",
            "sha256": "0440010c1216f9bfa4872eea52f91aa5e85c5eb558a28468afc8d932aa056d51"
          },
          "original_profile": {
            "path": "production/batch86/assets/tower-karst/r003/profile-contract.json",
            "sha256": "7bb6177e34c458c4a934f079181192f1424611045f5a6796575d684e9d5eaab2"
          },
          "active_profile": {
            "path": "production/batch86/assets/tower-karst/r003/profile-contract.json",
            "sha256": "7bb6177e34c458c4a934f079181192f1424611045f5a6796575d684e9d5eaab2"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
            "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
            "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
              "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-86/own-evidence-manifest.json",
              "sha256": "b280ca57f742f67ebce68629fd08929a12829b1ced4ff0d184a674b946484260"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-86/handoff.json",
              "sha256": "c3f2af4fcbe9441a8bbdc0274b4e7cdd37f76cda9958d650ded7b7aac6083b72"
            }
          ],
          "original_metrics": {
            "path": "production/batch86/assets/tower-karst/r003/metrics.json",
            "sha256": "3ecb18b454ec67ff1b83850d2f4dabb7d1efd6310d9c08f10946d4df244e5660"
          },
          "source_counts": {
            "path": "production/batch86/assets/tower-karst/r003/source-vertex-counts.json",
            "sha256": "d8befe07ad565f58ba322744bc441a91dd8a6945a411bca9d25fb14fe41e6199"
          },
          "proof": {
            "path": "production/batch86/assets/tower-karst/r003/proof-final/render-manifest.json",
            "sha256": "b6f1bf38ac26050a40d18aa468673412db25c9710c53e31d419a04e1bca53bca"
          },
          "source_preview": {
            "path": "production/batch86/assets/tower-karst/r003/preview.png",
            "sha256": "a65ca0ab07b1302283b43cb6641acf9f9e3f0296d54797f144c2a02b8f104cfb"
          },
          "capture_reference": {
            "path": "assets/additions/tower-karst/batch86-20261021/tower-karst.png",
            "sha256": "0ee611cd44447d5561e49b96824fc657d909e2cbc64e5176ed8bbaf815fc8942"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/tower-karst.json",
            "sha256": "0d1fe058c90438c34a31f5f1c46a3c56285caa83fc5f6d67609cbff274604786"
          }
        }
      ],
      "files": [
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/brief.md",
          "sha256": "b838efc2e199fc6ac7410f5f6bf0b86f0e32abc4b36f425ee348b76cd0183162",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/build-config.json",
          "sha256": "652b1428e9de7e9644f431a07597ce4ffaa70a10a056d712fb3b1686adefd4dd",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/build-dependencies.json",
          "sha256": "7b691e12c04c9f7c581a0449e8ff210493d1b97661d7d2e4adb571804dd5f3e6",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/candidate-brief.json",
          "sha256": "dcfe3bf28b14ce21ecdf2a59fdb5d74b05fcb2dde1abed2a1cbad5e846972e65",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/candidate.json",
          "sha256": "5d17de85fe97eb0b7e6d4c2332f89685263809da63317bc59ad86ebcbb441343",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/concept-original.png",
          "sha256": "a7c60e49314c1873cae62425d948993a922bb4ab9f2ab6a6d24e72424d74d8cc",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/concept-prompt.txt",
          "sha256": "4d4ee046bed7d9d79a5791f9da70d855ab33722033e13bef95a1e7ef7d4931cb",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/contact-sheet.png",
          "sha256": "5a6c0676c3ff294f542446774dacbf6038d63db5ae254d4efe8fbfc023791404",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/final-rebuild-binding.json",
          "sha256": "be4c5865a67fc5b4e196d32fdccc293992225b75e7193fd54f6b92d655c1b216",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/generator.py",
          "sha256": "c3ec985e94745541b0b7d84c9979d985ec0f53add94b8df61e5dd66739632b92",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/gltf-validator.report.json",
          "sha256": "28065c7f1e10bfd9512e488d67d018fb6dd5a8e8c10bb2677b8cf35b29c39047",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/lifecycle.jsonl",
          "sha256": "414863168eb4f41bff7464e3a4e3c5f69d4a897a0bc25dba10332cdbc2039858",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/maker-review.md",
          "sha256": "3ef20719c3f416cc28c78756a42fb2f24b21f0f792ccd918d3d25cd34863f6c7",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/metrics.json",
          "sha256": "3e08e0c36704ff26863f5f1eef54c989ab1478ad6d764ea8d892c9c86e01ced7",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/model.glb",
          "sha256": "8ca4797452265d9c6ab889c0ef4af75505b3e8544e4a78d68ee19d9d9b04e07f",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/physical-surfaces.report.json",
          "sha256": "71df9a64636683f06747457e9d93abb3b6c3b56b982e47a544258d0965ea375c",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/pixel-inspection.json",
          "sha256": "765e4d8736cf398168f6ca6ebcd85b7387f0d303940e1209e9635888366a7fb0",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/preview.png",
          "sha256": "8432fca568dc01582a615404d65f7d3587f67f81f99760ca4546aa7feb234878",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/profile-contract.json",
          "sha256": "6196ee4d26239f88f25dc9a3728e6199811206080338d8394d08a57ba35b524e",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/clay.png",
          "sha256": "62456897fdb173559b1f00a798da77d3e1756bdc4c8b1851f381f44ae91763e4",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/front.png",
          "sha256": "203d5fe985293e71689265acf138aa3ec055dd96d4b591e36547dd0bf8983233",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/hero.png",
          "sha256": "8432fca568dc01582a615404d65f7d3587f67f81f99760ca4546aa7feb234878",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/rear.png",
          "sha256": "af8a342b39c4c83d2534e5ed2e48deea5f934ed9f63d727be44186227a6d8d6a",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/render-manifest.json",
          "sha256": "faaf7c5c7e676921cacf1f216197e441f4e407a4cc83436ead75bc397b572762",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/reversehero.png",
          "sha256": "c58fe4a1dca59fc54d46b5fc9676c17dcde11565f0d9921a10a2b062eab15d17",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/side.png",
          "sha256": "cd989de8ce0b731d3a89ff6d895363d3898e446e514417d85ced711f1c24d1ab",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/silhouette.png",
          "sha256": "84778c7523530ab03e9fb99e919280c37967a70743c1e5422f8ebd65c83f26b2",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/proof-final/top.png",
          "sha256": "65de3f091c6afdeff9440f96ada31a97d58ffa2b8915dc2470f0f6c5f10ea1c5",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/references.json",
          "sha256": "97df9e97d67ed6022f8a2758c84a0295b65b50fd24bb1c2423a50254353e01f0",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/repair-freeze.json",
          "sha256": "6fdb84d0e4873cda218b3916468bf32bae71b25c2d4dfd4291cc62f4091f5415",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/repro-final-1.report.json",
          "sha256": "bf7f7c560e43f78bb03f4aeb05c2275834f6145c03201deadc43dfc20c8faef8",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/repro-final-2.report.json",
          "sha256": "481eea4af45ecd9daa38ecc5c047402b2344914c16beb8e5e06c7a5cfd05607f",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/runtime-parse.report.json",
          "sha256": "40b81581adfceb63c648c3f98f2402952469e7c8f70384717bd56ffd04829f04",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/source-final.report.json",
          "sha256": "e84f032f9765d6fdb5a4c5ee24739db58f8a1f0100b1cf5fb186dc9ae86a9688",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/source-metrics.json",
          "sha256": "8b8afebb6e8a1e086666189f13f9c000455f3ba128e0e6dd064dc9b9d91c4cb3",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/source-vertex-counts.json",
          "sha256": "60f23905f0e9b30bce49f70d7a354654622152413334751d64dcaff48e7c35ce",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/beach-cusp-field/r003/source.blend",
          "sha256": "ace2aeb00208cbd262e89606efa892385d11a1e765a426ae3534cb89faf65b69",
          "origin": "source",
          "owner": "beach-cusp-field"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/brief.md",
          "sha256": "b035b0c269d01cb8f7c138dfe4b6790ac652be38325a14a0b3d182432e033aee",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/build-config.json",
          "sha256": "d71d4925fa45300ee303a18d9e8d8721fe324f278e91d1078c2dfecaf81aec4c",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/build-dependencies.json",
          "sha256": "09df87f2d9c4626a431c59f2398b493e5d425cf807a6053484371a2bffc96ab5",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/candidate-brief.json",
          "sha256": "6b6d8858dc7cbcd5e55a5318f99927015abf97abcb74f57571f714a22816fc4c",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/candidate.json",
          "sha256": "86e9207e25d2c4b54735e32b8d0b023725d04b143ef7a9fc6e1fef6c498e115b",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/concept-original.png",
          "sha256": "87284ee5ecdc28bbe5384e12afe868a01814f15dda4a00905fea4494ae86e930",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/concept-prompt.txt",
          "sha256": "057d5646ca9e149603a64f54472a2a55eda010d05b6254dc09dd3363548e9330",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/contact-sheet.png",
          "sha256": "b477ff36846cda11e8f231deed52912f4d3567877559a0958c6459ebe4448789",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/final-rebuild-binding.json",
          "sha256": "049cb134d628be3f55e89159464a44a85850842731242be45db53a2466fb0287",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/generator.py",
          "sha256": "fdb7df59b628d91df24eb0fa9273f737e085add163005eedbe1322d1e4e476af",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/gltf-validator.report.json",
          "sha256": "f4fdd8fa442146a7990d80458980b44658a7824896d4c9f768db3f0b60ea0c48",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/lifecycle.jsonl",
          "sha256": "44d04eb296e790c74b40f2025d35ef3f443722a788b1638eb83344db8c8b1e5e",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/maker-review.md",
          "sha256": "843f63ad50a98c4b1aae235d4a34e7ef77bbb314750e9c5124ddcddd6ec17b26",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/metrics.json",
          "sha256": "ba30decbdc843042df73c343aaa46eaec9c0fd1c94d5762aa8c7c491140f8df0",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/model.glb",
          "sha256": "ecdadbb29a60ac31b7bf729cadf487026f4126bc3983c35ce9754fe0fca37883",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/modeling-freeze.json",
          "sha256": "cecd14161fbac0dddbb3479c1911f9368689e52e13235cfea35c8e01217a00f0",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/physical-surfaces.report.json",
          "sha256": "f2f529955c7967fdd17f8e00246ca09105411ab603e1a2da7138be3fa40da5b8",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/pixel-inspection.json",
          "sha256": "fcefc53ee0f99b76af23e350b38eb1e48761f6fc70b83b5e1de776a8835fcf83",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/preview.png",
          "sha256": "653a32a23d3106f74cdc024189fe8704e94047d62fb86d74b85c3058cec32c73",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/profile-contract.json",
          "sha256": "8b5b3b083825eb91e9e6a278147c163ff41aa73dff5331a00b5baa2d81d164f3",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/proof-final/clay.png",
          "sha256": "b865ef80cb809937f225de8206d590def313453a2ead5df8d18f322b0588f35c",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/proof-final/front.png",
          "sha256": "ec69e9f8e81c7ee84311c1f2482ecc496fe50512fd2d996a8011340fbf9c7a53",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/proof-final/hero.png",
          "sha256": "653a32a23d3106f74cdc024189fe8704e94047d62fb86d74b85c3058cec32c73",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/proof-final/rear.png",
          "sha256": "bb46f12a86e2beab0a8b516aa6bb295415deeb569cf8ecf479f92ac19ab4cabe",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/proof-final/render-manifest.json",
          "sha256": "1642913d7dac49828e0b1211a2fc361d941d500be736b91694ad59a68347e700",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/proof-final/reversehero.png",
          "sha256": "0661e1c839b85b5d0b8a248262af60fe30c53c2e131fdeb4f0f782a277a2fa94",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/proof-final/side.png",
          "sha256": "88f60c7c7515cb8fdc31c440ecf401ebbe541060976cc5787e6d81c20ee410e5",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/proof-final/silhouette.png",
          "sha256": "7a9995dbfbcdb75b9e17aa9fd6b6edbf809209e769eba67d074e8e36f1085266",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/proof-final/top.png",
          "sha256": "76cad2a7c579fcd1df7ca933fe9fee4e6e5ece13d552a88065f04a1bd2798b09",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/references.json",
          "sha256": "ce08e1fe1c2c3516ec10129ae2232542ea6b27027efdd282bb3711e17c870799",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/repro-final-1.report.json",
          "sha256": "d10e3cb948169c355d341235cb38b440dc028d459b2f609ba4ca4a6e9a8d69d1",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/repro-final-2.report.json",
          "sha256": "a8c38a690c9548f72bb7fbe1268f93b5e8def96535d82b0de440e322716dec4d",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/runtime-parse.report.json",
          "sha256": "3750e880e58fa2318399549dae0ed9c3419e0c2f0540539290a90428034cca2e",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/source-final.report.json",
          "sha256": "b2de942f3bc21fc8ab29282c3ad502ffe4100bdc8e0e0af41d87640c15f839e0",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/source-metrics.json",
          "sha256": "5ede66b4f793dbca1dbe57dc3c36cfc7c643ac97f420c1d16a60dd24ba5a2e63",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/source-vertex-counts.json",
          "sha256": "d6dd0332651b805d94c3d43e5c7297dbfb0d2e7425242dd33221e5a4bb44c922",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/cinder-cone/r001/source.blend",
          "sha256": "1fb42d5efaa3531aa1e6b1019ca5e5551af391d186f8078f3f80573e57f29eb6",
          "origin": "source",
          "owner": "cinder-cone"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/brief.md",
          "sha256": "434d52f6b050f4d61c5d1021e793e45358f4d8810bdd544910df26401156812a",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/build-config.json",
          "sha256": "bb97e56594ca58f2874fbe82bc65b4ee5c31c5e9bab853140433accf7c2857be",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/build-dependencies.json",
          "sha256": "c2af4da9dd4bceefef672c44855b6d06c470115f3cee0a820b97d41c5af52017",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/candidate-brief.json",
          "sha256": "3b8fc10a2ed9a3d93d7c43909c13887b0768d3cedcd03432adc93d156326bc22",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/candidate.json",
          "sha256": "0440010c1216f9bfa4872eea52f91aa5e85c5eb558a28468afc8d932aa056d51",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/concept-original.png",
          "sha256": "5252d37d0c2e4cd53ac73e23f87496d4a9136882cd0b5c7ca8b2859405e36203",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/concept-prompt.txt",
          "sha256": "614f2a2c5904c949a887bbc8e30cdd44064a9ba2a14a280247e89f9fd3fb0d10",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/contact-sheet.png",
          "sha256": "271339059cb331bede46582d75d92cf92411a80355244c04b06928b69da12bfb",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/final-rebuild-binding.json",
          "sha256": "c3fc172c7bb3c682de7f0a0bf55a08d21211a4a7a3e0cd243cc339834ac902a4",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/generator.py",
          "sha256": "b2c50312dee4ee55c88e54ed182dee6163f5c1a480fd13fadffd76a03d2add51",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/gltf-validator.report.json",
          "sha256": "89738f03015d2ec36af4d86424ad4d84e7534828dedf25ad2d57a7fd40068a22",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/lifecycle.jsonl",
          "sha256": "90dfab8ca3f87185943acb03c5d67abd3e1101eb593c38b210399c0b018d1c7f",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/maker-review.md",
          "sha256": "94875c864ce16f28d22bfc81c5fa9bc58488acd0c2ac485078c16f1d069e22b3",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/metrics.json",
          "sha256": "3ecb18b454ec67ff1b83850d2f4dabb7d1efd6310d9c08f10946d4df244e5660",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/model.glb",
          "sha256": "897aea54745d39fe910db3e9543988ddda2445b81120a9ee4e49fc1268a73083",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/physical-surfaces.report.json",
          "sha256": "37894031aa4c1eeeddeea4736a8f934733cca113c66c453346c9262b79addea4",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/pixel-inspection.json",
          "sha256": "0b717569a099eb1fb59b86e037fa0da7f9fac2f2ef2ff5a93365d2e2512ed0a6",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/preview.png",
          "sha256": "a65ca0ab07b1302283b43cb6641acf9f9e3f0296d54797f144c2a02b8f104cfb",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/profile-contract.json",
          "sha256": "7bb6177e34c458c4a934f079181192f1424611045f5a6796575d684e9d5eaab2",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/proof-final/clay.png",
          "sha256": "20db6be6fd2f5eb2fdd2506f80e729a177364749b4d38402ebde6cad5cb43142",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/proof-final/front.png",
          "sha256": "60348de5a3b1d794466f49e9ec1bc618f8638c4f5435d79374d3067cb25b0a53",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/proof-final/hero.png",
          "sha256": "a65ca0ab07b1302283b43cb6641acf9f9e3f0296d54797f144c2a02b8f104cfb",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/proof-final/rear.png",
          "sha256": "55d6c729de3095a66a2e6531b0fcac44747f7204d451bfff995e8270c107b165",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/proof-final/render-manifest.json",
          "sha256": "b6f1bf38ac26050a40d18aa468673412db25c9710c53e31d419a04e1bca53bca",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/proof-final/reversehero.png",
          "sha256": "9c2884c5876ae97a086b78070c06a8b48ea572864d7b5c13010f5ae23c57e41b",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/proof-final/side.png",
          "sha256": "2516d442b2e4ca992c69e5b39dff45542e1cbd1ad2d63dfdfa707ecc97d6e029",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/proof-final/silhouette.png",
          "sha256": "ca362128d947f9b09ad00782b434e2e3b18cc456978fa3d9effd8e019aee03d0",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/proof-final/top.png",
          "sha256": "37a99ba8cb47d08124ba2f4cea480830c093550b987467354a6168bc577685b6",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/references.json",
          "sha256": "19b3694904210b0e9622162fec779edb388c38ec0eee1cb96d64fc8487ea062e",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/repair-freeze.json",
          "sha256": "73fd14ac35c35ac32ff27e62ff3079cb60089d1cd3761a405a451f93b2908290",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/repro-final-1.report.json",
          "sha256": "dae7cd451b029c50e1ba5fce5745cefc0f48768b9d96c46413f474bea823a77b",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/repro-final-2.report.json",
          "sha256": "f32d46ac153c1ccc1530efd52e6637447b4a13ec78982cb37d4f88ba0cfc6bbf",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/runtime-parse.report.json",
          "sha256": "95db401c0da08361094e1a0a49717d2dc0ee4c5cb9dac874c9f5cd2ed3fd7458",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/source-final.report.json",
          "sha256": "779b50d4dc55742ba09699fe8ce36e82f37bbdf61ae5479874920dcc0f4d84bb",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/source-metrics.json",
          "sha256": "b0129591f8fcd0d8953ff9aca237ecc99e23661c3cfeac0b9eaa5e5fb5a47be0",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/source-vertex-counts.json",
          "sha256": "d8befe07ad565f58ba322744bc441a91dd8a6945a411bca9d25fb14fe41e6199",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "production/batch86/assets/tower-karst/r003/source.blend",
          "sha256": "f4dcace9d23dca638cc93e3a482414e6d857e2479037fdff422b02d795271723",
          "origin": "source",
          "owner": "tower-karst"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/REPORT.md",
          "sha256": "704db6478a9ea8a670877fcc2b7a62e90efc5148e7c8b1fd9a1c296e03119f2a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/audit_inputs.py",
          "sha256": "c4d2775dd13cc395cc66277695ca6f712da6ca4450a6d8395b259bddaf507c29",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/finalize_report.py",
          "sha256": "166d6208cad3a41bb3382151d91a1cb9c0c25da93ae1eecb141f63c050d29b67",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/handoff.json",
          "sha256": "c3f2af4fcbe9441a8bbdc0274b4e7cdd37f76cda9958d650ded7b7aac6083b72",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/independent-qa.report.json",
          "sha256": "83e66bc83fdae0046cd5568eb363e67427fdabfc3e1b88a1603ee66f010a9685",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/measure_parameters.py",
          "sha256": "2f6fd3d6138b61bfb5c4644eb1a149b6666f8656c526dd3902147ddbdce3894f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/own-evidence-manifest.json",
          "sha256": "b280ca57f742f67ebce68629fd08929a12829b1ced4ff0d184a674b946484260",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/run_fresh_checks.py",
          "sha256": "27bebc5c1762e6a51f43532c27bca486501c691f29befd2afb1cf146c87f8a12",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/runtime_checks.mjs",
          "sha256": "af2f6b7fb835a76d9883b0edf8c2c7036032b5c7bfad7ff213ca6e84cbef1b24",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-86/source_reexport.py",
          "sha256": "3953bca4c0f38c341c8873fed94365e7fd9f19ff79c7fe7c71c76f153aed0677",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g14-release-20261021/process-archive-index.json",
          "sha256": "a391319bf3a8f37538f39210db2f3659f7d627841833ab286bd97fbd28481e9a",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g15-20261021.json",
      "sha256": "841d8f1152a97d2b7f370d56500bc7301961b432ec8dabc0c4a7f2d377112fa8"
    },
    "release": {
      "version": 1,
      "scope": "next52-g15-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
      "review_commit": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g15-release-20261021/source-bundle.json",
        "sha256": "f5b83a5668e182568ffb2d6dd75e83d88f1be42dc88b4ecfcd54069e30486dce"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
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
          "path": "scripts/rebuild_frozen_blender.py",
          "sha256": "c5971fab63b69fa3720d52b9884789eb56f6c2b1d2db4d6c9d3fa2bc77a59db6"
        },
        {
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round33-20261020/batch-80/ingestion-manifest.json",
          "sha256": "1fd679f47cfb973f305181f8fa477ac0b49a3799e658f13469629efb3a0dafcd"
        },
        {
          "path": "qa/continuous-small-life-round33-20261020/batch-80/owned_outputs.json",
          "sha256": "ec710fb9c03aa4f8dd28230693652cf92aededf23fc691de3fe2dd8630c51e74"
        },
        {
          "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
          "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
        },
        {
          "path": "qa/continuous-small-life-round33-20261020/batch-80/report.md",
          "sha256": "e93b4517546455eaea99824d4258c8adf62659fc178c9e083f283ed73a063a20"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "kame-mound",
          "batch": 80,
          "revision": "r002",
          "candidate_root": "production/small-life-batch80/assets/kame-mound/r002",
          "source_commit": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
          "reviewed_source_commit": "42610ec62eeeddfb79ff24866b5840b012a9d729",
          "original_source_snapshot": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
          "review_commit": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/kame-mound/batch80-20261021/release-metadata.json",
            "sha256": "bc0171b97aa103ee3d98a1bf823ff897583bd6b398ed57fa549b5d8af173b4b1"
          },
          "candidate": {
            "path": "production/small-life-batch80/assets/kame-mound/r002/candidate.json",
            "sha256": "4c07dcc462147d95d8017f895c4cc19555a38697ce6388d5a9aec431e068fa1e"
          },
          "active_candidate": {
            "path": "production/small-life-batch80/assets/kame-mound/r002/candidate.json",
            "sha256": "4c07dcc462147d95d8017f895c4cc19555a38697ce6388d5a9aec431e068fa1e"
          },
          "original_profile": {
            "path": "production/small-life-batch80/assets/kame-mound/r002/profile-contract.json",
            "sha256": "d77fab8a03d32a94f744d7cef8127e73bbea6c3245980bba79b4c552a9d048ba"
          },
          "active_profile": {
            "path": "production/small-life-batch80/assets/kame-mound/r002/profile-contract.json",
            "sha256": "d77fab8a03d32a94f744d7cef8127e73bbea6c3245980bba79b4c552a9d048ba"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
            "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
            "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
              "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
            },
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/report.md",
              "sha256": "e93b4517546455eaea99824d4258c8adf62659fc178c9e083f283ed73a063a20"
            },
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/owned_outputs.json",
              "sha256": "ec710fb9c03aa4f8dd28230693652cf92aededf23fc691de3fe2dd8630c51e74"
            },
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/ingestion-manifest.json",
              "sha256": "1fd679f47cfb973f305181f8fa477ac0b49a3799e658f13469629efb3a0dafcd"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch80/assets/kame-mound/r002/metrics.json",
            "sha256": "f31e592cd753070f2de1bbcb89eb41e4c2b84c66b4f1dbd2cb65ca337941c9eb"
          },
          "source_counts": {
            "path": "production/small-life-batch80/assets/kame-mound/r002/source-vertex-counts.json",
            "sha256": "24e67f22ba28ba2b6212668764f7854d80b11089f07cd4073b04ca6897500069"
          },
          "proof": {
            "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/render-manifest.json",
            "sha256": "29c327850f8a95a1581363fe76c726637df9b2e2289e44cd62c5fe2ac87c40b6"
          },
          "source_preview": {
            "path": "production/small-life-batch80/assets/kame-mound/r002/preview.png",
            "sha256": "03448af8b4548356ec98cb312fbbdd4993403b42ab76a5f508e87fb291597aa9"
          },
          "capture_reference": {
            "path": "assets/additions/kame-mound/batch80-20261021/kame-mound.png",
            "sha256": "0ae0dc4ce1f2ec462bd47dc65eb126f958aa4f67bc7f42af49f354de2f327d36"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/kame-mound.json",
            "sha256": "2e2b5f73fe844a5cf6518da2eae52768386a07bc1b462bab8c2182b71472a7ec"
          }
        },
        {
          "id": "pediment",
          "batch": 80,
          "revision": "r002",
          "candidate_root": "production/small-life-batch80/assets/pediment/r002",
          "source_commit": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
          "reviewed_source_commit": "42610ec62eeeddfb79ff24866b5840b012a9d729",
          "original_source_snapshot": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
          "review_commit": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/pediment/batch80-20261021/release-metadata.json",
            "sha256": "28b5a5470734eea3844ecc05988c9a8c401e6b5cb6e6c55d05fae382b5eb8450"
          },
          "candidate": {
            "path": "production/small-life-batch80/assets/pediment/r002/candidate.json",
            "sha256": "dadb435b88514d4694d6251b9ec393a6d0636889ef6d07e4499d577cfadc88e2"
          },
          "active_candidate": {
            "path": "production/small-life-batch80/assets/pediment/r002/candidate.json",
            "sha256": "dadb435b88514d4694d6251b9ec393a6d0636889ef6d07e4499d577cfadc88e2"
          },
          "original_profile": {
            "path": "production/small-life-batch80/assets/pediment/r002/profile-contract.json",
            "sha256": "93c1652bee87bf370a3b090c967cdc29511507420d5982d1730a765e840335b5"
          },
          "active_profile": {
            "path": "production/small-life-batch80/assets/pediment/r002/profile-contract.json",
            "sha256": "93c1652bee87bf370a3b090c967cdc29511507420d5982d1730a765e840335b5"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
            "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
            "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
              "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
            },
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/report.md",
              "sha256": "e93b4517546455eaea99824d4258c8adf62659fc178c9e083f283ed73a063a20"
            },
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/owned_outputs.json",
              "sha256": "ec710fb9c03aa4f8dd28230693652cf92aededf23fc691de3fe2dd8630c51e74"
            },
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/ingestion-manifest.json",
              "sha256": "1fd679f47cfb973f305181f8fa477ac0b49a3799e658f13469629efb3a0dafcd"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch80/assets/pediment/r002/metrics.json",
            "sha256": "ad4d0176ffb501ba1cc6a314d2186e8f70c217741339845fddfc47f9df14e140"
          },
          "source_counts": {
            "path": "production/small-life-batch80/assets/pediment/r002/source-vertex-counts.json",
            "sha256": "0f996a527e93f6dec5e5a09c6742da46bf9f3ec48f02e9109512b51897a3e7ec"
          },
          "proof": {
            "path": "production/small-life-batch80/assets/pediment/r002/proof-final/render-manifest.json",
            "sha256": "c51237c4553ad694b2310153a02743ab2810261ad83c1691e9a61b829cb6db43"
          },
          "source_preview": {
            "path": "production/small-life-batch80/assets/pediment/r002/preview.png",
            "sha256": "8b371886d18a7f0dd21a39236539905befdb78dc8dd77336d1c9e4d29e20927c"
          },
          "capture_reference": {
            "path": "assets/additions/pediment/batch80-20261021/pediment.png",
            "sha256": "2325e445964b759b83719ddccf22e05ea0be3e7e683fed239cdd64bd2dd0a748"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/pediment.json",
            "sha256": "621a4dce8e0d4317ff08084230f3845735bdd05deb729c6f8403b7151eb0d7cd"
          }
        },
        {
          "id": "spriggina",
          "batch": 80,
          "revision": "r003",
          "candidate_root": "production/small-life-batch80/assets/spriggina/r003",
          "source_commit": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
          "reviewed_source_commit": "42610ec62eeeddfb79ff24866b5840b012a9d729",
          "original_source_snapshot": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
          "review_commit": "a7cb42265e06ca7573b7554ae5ae3d924766215c",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/spriggina/batch80-20261021/release-metadata.json",
            "sha256": "ff5593ff5ae234068c8e5bc15b3a9622cf4b59e0a69c0d8924f822394a65abb1"
          },
          "candidate": {
            "path": "production/small-life-batch80/assets/spriggina/r003/candidate.json",
            "sha256": "d47f7fa75884b1e942b20dfda04fbcfd80c7eb30a8e97501c95fa90d9049ebe7"
          },
          "active_candidate": {
            "path": "production/small-life-batch80/assets/spriggina/r003/candidate.json",
            "sha256": "d47f7fa75884b1e942b20dfda04fbcfd80c7eb30a8e97501c95fa90d9049ebe7"
          },
          "original_profile": {
            "path": "production/small-life-batch80/assets/spriggina/r003/profile-contract.json",
            "sha256": "b8d3979e51bcaffb50f37fa99478492f9126587d46c3b629f36dc2e248ba480b"
          },
          "active_profile": {
            "path": "production/small-life-batch80/assets/spriggina/r003/profile-contract.json",
            "sha256": "b8d3979e51bcaffb50f37fa99478492f9126587d46c3b629f36dc2e248ba480b"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
            "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
            "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
              "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c"
            },
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/report.md",
              "sha256": "e93b4517546455eaea99824d4258c8adf62659fc178c9e083f283ed73a063a20"
            },
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/owned_outputs.json",
              "sha256": "ec710fb9c03aa4f8dd28230693652cf92aededf23fc691de3fe2dd8630c51e74"
            },
            {
              "path": "qa/continuous-small-life-round33-20261020/batch-80/ingestion-manifest.json",
              "sha256": "1fd679f47cfb973f305181f8fa477ac0b49a3799e658f13469629efb3a0dafcd"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch80/assets/spriggina/r003/metrics.json",
            "sha256": "8a55ecf3fdb9878438cbb4c435d45039e9c9644cc77b7bf7e9ac4ee6966f5eef"
          },
          "source_counts": {
            "path": "production/small-life-batch80/assets/spriggina/r003/source-vertex-counts.json",
            "sha256": "91d1230e7770ea3830454acc3cb2f0f05b953bac63f9db21f45279705d7d67bb"
          },
          "proof": {
            "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/render-manifest.json",
            "sha256": "991c32cb3bfc11c6a18c3fc1abc2af4d11619e0cb70a8af6bf9da7d12594d36a"
          },
          "source_preview": {
            "path": "production/small-life-batch80/assets/spriggina/r003/preview.png",
            "sha256": "8bacb70be2afd65bb4e4f572967d01678f5789c0b499c5d5c7f86977adca5e1c"
          },
          "capture_reference": {
            "path": "assets/additions/spriggina/batch80-20261021/spriggina.png",
            "sha256": "d0430fae353f7aef7ebc44a45d532c39fa8966fda51235e97bce802e93f21c7d"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/spriggina.json",
            "sha256": "8c3a1b55bb37bb9938d75c47d1dbaed9b40536e96b4d0b9e4720bbc7f9f554e8"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/brief.md",
          "sha256": "da98e88cae463877de3fa1a8ce56bd45f935c93415cf6e228ab8d15576ab7d6f",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/build-config.json",
          "sha256": "05b09bbd56d2a51c496eff8885a168e1bbbf47ba5406c88b3ee5b1360e620a2b",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/build-dependencies.json",
          "sha256": "32841a07c54469df3fb55eaaeb5c8d7043e02731a8b3d28b6a16243a5fa12aad",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/candidate-brief.json",
          "sha256": "be189242d0dedcb87043556624e5caeb362a2f7dabf37f241aab43d1ff4a432e",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/candidate.json",
          "sha256": "4c07dcc462147d95d8017f895c4cc19555a38697ce6388d5a9aec431e068fa1e",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/concept-original.png",
          "sha256": "fc488b1200155010eb607828faa7c647563eedce3e5570f837e35e7fc6d7bca8",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/concept-prompt.txt",
          "sha256": "f5764ad1892bd0f229c3bcaf13e476a9f65dcfac46d9726401c1d2029080531b",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/contact-sheet.png",
          "sha256": "2c6e8bbb96724ea551376b1dd979805b89a5cd232dd000bf977b28b4cf0442b4",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/final-rebuild-binding.json",
          "sha256": "85806092bd778d232461ab9de4ed0e4521fe362049646f697ea2e689ab7ae7c8",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/generator.py",
          "sha256": "4518f29a208439857ccea328b956d12f25aaf6d180c0921192c5982fbc81039f",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/gltf-validator.report.json",
          "sha256": "c4d17a9b9112c901d60ece6a56bfb1e7f08c6eef55d5bfb932e89068bc256ebf",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/lifecycle.jsonl",
          "sha256": "f27019101eaa34a1a2917fb5bb0b92222e231a97abf9568b5f356305c9db6b12",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/maker-review.md",
          "sha256": "7e158ac31b3fd87aa2e381e808a574632d76353066d673d43578d38bb0865b26",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/metrics.json",
          "sha256": "f31e592cd753070f2de1bbcb89eb41e4c2b84c66b4f1dbd2cb65ca337941c9eb",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/model.glb",
          "sha256": "f3877ca2efcca03a31e5b904c55c00675f64d9e58f0bc7736bcda93ac96dccf2",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/modeling-freeze.json",
          "sha256": "ba7a8e035b708c7466933790fc35e05c18f5e9cba259ab99fcfa2dc8878dccf9",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/physical-surfaces.report.json",
          "sha256": "f849c9ef7b170464a7e32a6a8023b48b6b47d1f4c37bc15c77c36e95d1daae64",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/pixel-inspection.json",
          "sha256": "ea0705e73dbebe6f71e7e17d7b689ff76586d6f21b37cdc66c113f1bd5cebb3c",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/preview.png",
          "sha256": "03448af8b4548356ec98cb312fbbdd4993403b42ab76a5f508e87fb291597aa9",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/profile-contract.json",
          "sha256": "d77fab8a03d32a94f744d7cef8127e73bbea6c3245980bba79b4c552a9d048ba",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/clay.png",
          "sha256": "1591851c1274841506263495b1856ff69128a3c099f94a7090c8d27d77a5918b",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/front.png",
          "sha256": "bf121062821a3689320fceee1eab5e2b0a76b31841d6a739e4ce1647cc7e76e7",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/hero.png",
          "sha256": "03448af8b4548356ec98cb312fbbdd4993403b42ab76a5f508e87fb291597aa9",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/rear.png",
          "sha256": "f82467d5e84a23a0d9328ae0cfdf0a1c9348731ac9b3c440a8c5080e8bad9521",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/render-manifest.json",
          "sha256": "29c327850f8a95a1581363fe76c726637df9b2e2289e44cd62c5fe2ac87c40b6",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/reversehero.png",
          "sha256": "4489797681699f579e33a62edaa787f6465d084b8c0f552bdf7c6c6f8f55a7e7",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/side.png",
          "sha256": "9030f57e0655cbcde814ce778aea709dcd60377e0d2bc55d496a4fb9e810415c",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/silhouette.png",
          "sha256": "ef94681da41a9e0ab83533406bb35ff3c3fcafbc367cdd634f02785a8ba9ed7e",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/proof-final/top.png",
          "sha256": "db92919201c7eb2f8f9f67a6f23b9a96f6fe3ae6ac27d2ed7db95fac708fda32",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/references.json",
          "sha256": "74e3627a6d3e94c4ded4c0fc307a1d6f7c7ea29f6af493abbac53feb23e90447",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/repair-freeze.json",
          "sha256": "ace3387ee49b3acd18ad88e9a7ddd3f354a01fa1b04df92942b95c941b474c28",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/repro-final-1.report.json",
          "sha256": "a9dd56419605d12dcaddd6f0bf81646f148f11dd73647e939c22a8bf5db17f74",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/repro-final-2.report.json",
          "sha256": "84346dbafedadd32d4e408603242719ca4ec68d34438a7652aef87148ea248bf",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/runtime-parse.report.json",
          "sha256": "e769add66dfa55157644f061f3d4efc9a96fc453e2d6cc1183e98d2ccc568c4e",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/source-final.report.json",
          "sha256": "a29e9fd4c26bed338092f459d60888ad8ed58a9a33026ef5ea0cef10bfd75251",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/source-metrics.json",
          "sha256": "b5e6f80cd748df031890337a96096f84e3b481bc4ff36f654b908b2f4285872e",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/source-vertex-counts.json",
          "sha256": "24e67f22ba28ba2b6212668764f7854d80b11089f07cd4073b04ca6897500069",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/kame-mound/r002/source.blend",
          "sha256": "82d3ff51f93680c958cd32e2a686e6f8c1f59cbdaa5918c3f657e1a374f078c9",
          "origin": "source",
          "owner": "kame-mound"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/brief.md",
          "sha256": "f545958d7af0ac64ee9110b3578a0e4c490e9e44dc050d17473a3de72abdaef8",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/build-config.json",
          "sha256": "7f80bdb72ec41ceb9a1b9fa3d5e5ee67c0b7b3ee588083986a3064257c8fe484",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/build-dependencies.json",
          "sha256": "3469393db98e3f52365c33b247051d01d79dc266e98a87362795f531ec17d37a",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/candidate-brief.json",
          "sha256": "cf095b05a3c862153a4b3467653e0452c53e41d0b5feee6af7c0c806c7e2091d",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/candidate.json",
          "sha256": "dadb435b88514d4694d6251b9ec393a6d0636889ef6d07e4499d577cfadc88e2",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/concept-original.png",
          "sha256": "ea666ca99294c8f28f0bdbf8a9a61329e1e3cea9416c33b7d4ede52d8d4cca83",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/concept-prompt.txt",
          "sha256": "f7c82c45aa9dafba204a7781ceeb84569c432b7ad29998446387f95f7556d5aa",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/contact-sheet.png",
          "sha256": "9fca1df8fc8988fd57cb0f1272c8ae874b26b2bdca54f8f76e6258b306b2e657",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/final-rebuild-binding.json",
          "sha256": "a939c679b8de79094945f6101de729210d1dffae63df48d1c46bdf7f46994b7b",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/generator.py",
          "sha256": "2289f51e5714ebfa6a5793f2b15d4da136651e9d8439ef1d0dce1f9561b6fb3e",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/gltf-validator.report.json",
          "sha256": "ee60beb66c863f2dca4dc603ed46e9b2e030674ac2a0ebe007a1e5922b6d7382",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/lifecycle.jsonl",
          "sha256": "aec7b5b6d403a11bc6eb316f0cc6d616d7e3ba9e7f40d592f58b83162b004ed2",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/maker-review.md",
          "sha256": "e7bf402310496998f8f610d0b0f1ae319faaa3196785a000f820a08323d9be1b",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/metrics.json",
          "sha256": "ad4d0176ffb501ba1cc6a314d2186e8f70c217741339845fddfc47f9df14e140",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/model.glb",
          "sha256": "5acccae174dabafb01b6f253d09684821d467726d796f251f831ead2f8dad24a",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/modeling-freeze.json",
          "sha256": "cb50eba42f718b71aa536261ea660b5fc08d113db1f16668399fbd24074411e4",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/physical-surfaces.report.json",
          "sha256": "0059de2282aa730c0bc23b88dba52fc990a24392de900b6f3fb07ae33f9cd571",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/pixel-inspection.json",
          "sha256": "7a6752e595f8da2f36374952b86f545b4d7ba7d034ff0f11602f1b7fe4731f2c",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/preview.png",
          "sha256": "8b371886d18a7f0dd21a39236539905befdb78dc8dd77336d1c9e4d29e20927c",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/profile-contract.json",
          "sha256": "93c1652bee87bf370a3b090c967cdc29511507420d5982d1730a765e840335b5",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/proof-final/clay.png",
          "sha256": "291b5ca9498f1013db1f64d777fd5ea0f0d1bcedafa6789345cd27d133721f62",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/proof-final/front.png",
          "sha256": "ae4b3d72d98f8cdc8e32bac2fec6f377b168ed072e626c8a582f489f7dce463e",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/proof-final/hero.png",
          "sha256": "8b371886d18a7f0dd21a39236539905befdb78dc8dd77336d1c9e4d29e20927c",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/proof-final/rear.png",
          "sha256": "f83dcddfb3fba3fca7b2d92049dc22eaf94794c9dd015196b2b3ea7ca219c6dd",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/proof-final/render-manifest.json",
          "sha256": "c51237c4553ad694b2310153a02743ab2810261ad83c1691e9a61b829cb6db43",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/proof-final/reversehero.png",
          "sha256": "6bc97e5fa5e5f2d95d5e50e2f117459f43b50f07169e5a015aef633a24fc4bcc",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/proof-final/side.png",
          "sha256": "eaab1821bc3a06e42c0e5b4435b3daf36893b848f327156c104821437b3eccd4",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/proof-final/silhouette.png",
          "sha256": "49ff81d7f35f2ed5a314f93be0c8dad7ba9ee4fb0a5e26177e72d664d625b5ec",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/proof-final/top.png",
          "sha256": "7357ce55db7d16348bb01cda06023532aaae66e11d2b2139a0f996f9c9e6da9b",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/references.json",
          "sha256": "f8eaea8f48c49900e89d495074aac8cab8e046bed4ae59c9b7d1e1a769617636",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/repair-freeze.json",
          "sha256": "c8c2dd28560c264423fd2331cceca501c31be9caee3605f3d3a1665142cf5bbf",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/repro-final-1.report.json",
          "sha256": "fbc6b0a3861354d981d28a14415f1592a2a65c1baf64952264a25ed1723f1441",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/repro-final-2.report.json",
          "sha256": "f926a5bdb43caac668137e546064c4448d59afc5a6b7e2fd424446c5dc9cebba",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/runtime-parse.report.json",
          "sha256": "a01f5055a25aa161d9607fae559667564c17ce6ff56399b420e752df25872754",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/source-final.report.json",
          "sha256": "196023c32c36bae4c512ebe82c5c2ab9fc14bc7a9d07ee32c3cc5afcc58bfeea",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/source-metrics.json",
          "sha256": "d2857ef4b864fd2408f5520b2bb58c630f6a3b434c68fee9abb4b9ac6dbb1ab6",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/source-vertex-counts.json",
          "sha256": "0f996a527e93f6dec5e5a09c6742da46bf9f3ec48f02e9109512b51897a3e7ec",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/pediment/r002/source.blend",
          "sha256": "3c586522bed75362f6088c26d034f4412ea4f11b6ac19b3423a19e07c4699d81",
          "origin": "source",
          "owner": "pediment"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/brief.md",
          "sha256": "73b029b957701ecf93f801f47c6fcf181e3476101242de3ca4f92e98d6ace0d4",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/build-config.json",
          "sha256": "ea2e775d44c0584128f39c6107faad51ac12458d9976815a031343dce0de4751",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/build-dependencies.json",
          "sha256": "1b4d83d549d9c6c8815e6eca68008565abd1acb6c51b1eb178720278616f6fb0",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/candidate-brief.json",
          "sha256": "4fd11283b4222ad5d9cf254246c72ffda9b57ab2aada958eb65361c6481feff0",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/candidate.json",
          "sha256": "d47f7fa75884b1e942b20dfda04fbcfd80c7eb30a8e97501c95fa90d9049ebe7",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/concept-original.png",
          "sha256": "beee6da3cd3f8998c515d21a46b11a76482e5d9aa00d5213542c32f64979a623",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/concept-prompt.txt",
          "sha256": "94a42124c0b9af75f837b536fb0f7bcc0232c82c5291702bbc30470fc9b629f2",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/contact-sheet.png",
          "sha256": "892c969eedfce0cc5699c06c4fd5514e3adafbb9412a9c778276bf91d5ae6547",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/final-rebuild-binding.json",
          "sha256": "0d2224fc3371be550fafe893ed95b251d969e251b48dc20b698b24a7a53a4881",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/generator.py",
          "sha256": "f14474031824d338a62c9f3c3ba8f22bf2212f5357c905e979d61b703e8fb343",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/gltf-validator.report.json",
          "sha256": "613a59be7711137c9847d1c1e58405af3ab24c57aca56ad2e7405ff61ccf310e",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/lifecycle.jsonl",
          "sha256": "677cc9904421cc0ec25dcbb4a1464b49d116de827fe2822f23517eeefea287c6",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/maker-review.md",
          "sha256": "3d0abe64f382f72bdaa482ef9750e7fa7716729c81c04964bb680cf2a07dfacd",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/metrics.json",
          "sha256": "8a55ecf3fdb9878438cbb4c435d45039e9c9644cc77b7bf7e9ac4ee6966f5eef",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/model.glb",
          "sha256": "c5f189656f3558c352c9413fadc7049a398e7ccf4bab1277e91722b1347cd5e2",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/modeling-freeze.json",
          "sha256": "15e45bd00e6eaa6ac3e45455471925e5e96c7d606d347cc28c2144a8c1d5444c",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/physical-surfaces.report.json",
          "sha256": "8db21d5c49df42e7b4be7993bb6562b784e56ae6e1854418c12ce7b46d00a3a1",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/pixel-inspection.json",
          "sha256": "d92f9801e3560e9b1b63396ea5a4dacebc9a52fa1d6e8fc65622bb176debadf8",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/preview.png",
          "sha256": "8bacb70be2afd65bb4e4f572967d01678f5789c0b499c5d5c7f86977adca5e1c",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/profile-contract.json",
          "sha256": "b8d3979e51bcaffb50f37fa99478492f9126587d46c3b629f36dc2e248ba480b",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/clay.png",
          "sha256": "d643f3718e6d6fc3ec0c5496a6a90f71ced46a10238efc4c3a61f5db5cb55177",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/front.png",
          "sha256": "55ab0aae4fdd4d095fb6326e06c97139fd6ae786b7b292e7d0b566b1472cdd79",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/hero.png",
          "sha256": "8bacb70be2afd65bb4e4f572967d01678f5789c0b499c5d5c7f86977adca5e1c",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/rear.png",
          "sha256": "4a673e1369a93743e89ee5cd0a610f210f11f292be7fdb8c3fb3736e83d107f6",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/render-manifest.json",
          "sha256": "991c32cb3bfc11c6a18c3fc1abc2af4d11619e0cb70a8af6bf9da7d12594d36a",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/reversehero.png",
          "sha256": "aae526530227304ca61a6faceddd0ac9891fd893e26b040ed8cb934e71fe6193",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/side.png",
          "sha256": "17813d545fb85e02a463ed5771f08d489610784187a33a01b5d289acf396ae3d",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/silhouette.png",
          "sha256": "bf2d0ced786a9eb355738754ec099cd44fb7a8e96300f5693479a4f481b5881d",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/proof-final/top.png",
          "sha256": "0eafbfa6627228a3ec55a63a7c33ba132ca9465b0a550b8282e31a82ae421a94",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/references.json",
          "sha256": "f0c3c7aa5209f70ecc2bacf90ba158fc3abc48cd427402fcf989da0a5ee60fcf",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/repair-freeze.json",
          "sha256": "404a5ea0b78269a89c9f233413e217371bf62006a8f4dfeb22906429831152aa",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/repro-final-1.report.json",
          "sha256": "6a287094519f9b21cda9d00900821ab1c3e5e15c734c69136ba18f578b72f79e",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/repro-final-2.report.json",
          "sha256": "5b99df5c0f5531960921c7892efbaa51cb67c36d427f8c5948242ce1bb100ec1",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/runtime-parse.report.json",
          "sha256": "8bf827d23a15a70c6715a5d1f09aafebff8a5a074f09e552c74f353c7e8c8916",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/source-final.report.json",
          "sha256": "259b1145f2421814d7fd94d05bef5bed5bc97b79b7f1594e2772210cbf6e35a0",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/source-metrics.json",
          "sha256": "ecdaa5c634c134723d98f6d76f00e10ddf44114465e15f907a8e0ec1939ede6e",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/source-vertex-counts.json",
          "sha256": "91d1230e7770ea3830454acc3cb2f0f05b953bac63f9db21f45279705d7d67bb",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/assets/spriggina/r003/source.blend",
          "sha256": "001eafb5806a5677bb8d7ef3c519bfa9849cb8d04ed8830eb94b0c1b9e44a88c",
          "origin": "source",
          "owner": "spriggina"
        },
        {
          "path": "production/small-life-batch80/check-physical-surfaces.py",
          "sha256": "470f371dabe34231ee0a3e4c6856e5ae57751300aa563eb2c53570f7bed11d42",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch80/publication-policy-reference.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch80/render-fixed8.py",
          "sha256": "e3654a0abb9bc8848e52fdf0c37c53ff34396aa876ab5a7ae0bc004607083058",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch80/runtime-parse.mjs",
          "sha256": "fb938eb6db606a51b904de3f58b2557b618fc5963bfcf225ad990b0b1244164c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round33-20261020/batch-80/ingestion-manifest.json",
          "sha256": "1fd679f47cfb973f305181f8fa477ac0b49a3799e658f13469629efb3a0dafcd",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round33-20261020/batch-80/owned_outputs.json",
          "sha256": "ec710fb9c03aa4f8dd28230693652cf92aededf23fc691de3fe2dd8630c51e74",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round33-20261020/batch-80/report.json",
          "sha256": "0680e9b660a25890ec2c92a952020a028baf82b2ed3c58e98d24271d8d22e67c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round33-20261020/batch-80/report.md",
          "sha256": "e93b4517546455eaea99824d4258c8adf62659fc178c9e083f283ed73a063a20",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g15-release-20261021/process-archive-index.json",
          "sha256": "699702bb31eb4bd5602cf525ef4d51b5fe5c86487738405442aba5bff82b2629",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g16-20261021.json",
      "sha256": "7ffb4b7aa9c71e411b4e68cdf99ae92a67a4401a44741efb762fcda4f2b74c95"
    },
    "release": {
      "version": 1,
      "scope": "next52-g16-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "bf13b45a810871434efd525b5d99c329869223d8",
      "review_commit": "bf13b45a810871434efd525b5d99c329869223d8",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g16-release-20261021/source-bundle.json",
        "sha256": "0bf4593e5fa09aecd53867a99f45b554086ecbffbda86689f902a908b7620361"
      },
      "protected_source_inputs": [
        {
          "path": "package-lock.json",
          "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
        },
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "production/small-life-batch87/concepts/spatter-cone-concept.png",
          "sha256": "256b9a99b20b51d6416ae4c0e3814300fe82aa449e36b829ad9818d929658efa"
        },
        {
          "path": "production/small-life-batch87/concepts/spatter-cone-prompt.txt",
          "sha256": "c89afcab6c44478532e38e86dda5cd275f5f85d935234197a47a0c7de879de21"
        },
        {
          "path": "production/small-life-batch87/concepts/spatter-cone-receipt.json",
          "sha256": "6438ce47c874cf0e4fa4a0f436ca485df7391b3457676b616a56a7133e699c14"
        },
        {
          "path": "production/small-life-batch87/concepts/travertine-terrace-pools-concept.png",
          "sha256": "5439d910821d5abb12a244daaee5c5a392c03104cf4c99293dc56bcce1a5d04f"
        },
        {
          "path": "production/small-life-batch87/concepts/travertine-terrace-pools-prompt.txt",
          "sha256": "42815251481c31d633a28bb61f2249a892d67b12e57ed132641809a4d01ac487"
        },
        {
          "path": "production/small-life-batch87/concepts/travertine-terrace-pools-receipt.json",
          "sha256": "39931dc2637c936e6e50ed7eb2916c91e6a7177751562c8dee628e3a72ad91b2"
        },
        {
          "path": "production/small-life-batch87/tools/parse.cjs",
          "sha256": "813bbe4ebbfc1cd80b2d45075f34a43bab68989991e3f81a0858a76c88a790d5"
        },
        {
          "path": "production/small-life-batch87/tools/render.py",
          "sha256": "dce6084f0ec6663a5ca5acd3f5815f128314c4e2c94c04748be153ed75c6879e"
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
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        },
        {
          "path": "scripts/validate_candidate.py",
          "sha256": "fe679a8be19d16b9d9b86ee3419a73d2dd16b77dfa371bf1186ce0120d120ff9"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/handoff.json",
          "sha256": "dee1c8fbe67a845a9ae8bc92b8452bcb7e011475bff5cd3227672e951b74304b"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/independent-qa.report.json",
          "sha256": "0b281b8b61e7d0c0b2e3f213bc7d11c0d189cb525cd6de255c2d67eed587a7ac"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/own-manifest.json",
          "sha256": "4dac9fa742663664d9177ba88f56afa055a202e63f55cfa5dabd21514a78c394"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "spatter-cone",
          "batch": 87,
          "revision": "r006",
          "candidate_root": "production/batch87-landform-repair/spatter-cone/r006",
          "source_commit": "bf13b45a810871434efd525b5d99c329869223d8",
          "reviewed_source_commit": "178664a29c9bf5a751ccb3833e749e539d1b3745",
          "original_source_snapshot": "bf13b45a810871434efd525b5d99c329869223d8",
          "review_commit": "bf13b45a810871434efd525b5d99c329869223d8",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/spatter-cone/batch87-20261021/release-metadata.json",
            "sha256": "eb8124106fe8b9ceb63f44d40b0f3600b09733f5d7748f075524843d8917a37e"
          },
          "candidate": {
            "path": "production/batch87-landform-repair/spatter-cone/r006/candidate.json",
            "sha256": "3f6b3531dd6b17dbf569ce4f562f64804d32ef49d540e9dc958366f6a2ea73f9"
          },
          "active_candidate": {
            "path": "production/batch87-landform-repair/spatter-cone/r006/candidate.json",
            "sha256": "3f6b3531dd6b17dbf569ce4f562f64804d32ef49d540e9dc958366f6a2ea73f9"
          },
          "original_profile": {
            "path": "production/batch87-landform-repair/spatter-cone/r006/profile-contract.json",
            "sha256": "b2fb663878a9ac6e4924d9991d6822d9918af6b0d23c3b849de9e5fa579c2b40"
          },
          "active_profile": {
            "path": "production/batch87-landform-repair/spatter-cone/r006/profile-contract.json",
            "sha256": "b2fb663878a9ac6e4924d9991d6822d9918af6b0d23c3b849de9e5fa579c2b40"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/independent-qa.report.json",
            "sha256": "0b281b8b61e7d0c0b2e3f213bc7d11c0d189cb525cd6de255c2d67eed587a7ac"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/independent-qa.report.json",
            "sha256": "0b281b8b61e7d0c0b2e3f213bc7d11c0d189cb525cd6de255c2d67eed587a7ac"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/independent-qa.report.json",
              "sha256": "0b281b8b61e7d0c0b2e3f213bc7d11c0d189cb525cd6de255c2d67eed587a7ac"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/own-manifest.json",
              "sha256": "4dac9fa742663664d9177ba88f56afa055a202e63f55cfa5dabd21514a78c394"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/handoff.json",
              "sha256": "dee1c8fbe67a845a9ae8bc92b8452bcb7e011475bff5cd3227672e951b74304b"
            }
          ],
          "original_metrics": {
            "path": "production/batch87-landform-repair/spatter-cone/r006/artifacts/metadata.json",
            "sha256": "af6cae7ecc941ccee69b165a62b93c5963b0634bf8b558a697e20a9e00987538"
          },
          "source_counts": {
            "path": "production/batch87-landform-repair/spatter-cone/r006/qa/authored-evaluated-counts.json",
            "sha256": "bd0ccb6aac4b467bbfd2f9815d3f4bccb9ce68bdd43c699a79efae1d4279c57d"
          },
          "proof": {
            "path": "production/batch87-landform-repair/spatter-cone/r006/views/render-manifest.json",
            "sha256": "ad92c8435c5a8c30aeb9a6e8c9139d8c0668b0083605bb33731ebd0061f5ecf2"
          },
          "source_preview": {
            "path": "production/batch87-landform-repair/spatter-cone/r006/views/hero.png",
            "sha256": "9b12ba9c80d8a1f6817cdfdb830d66b19e6ea7e6ccfb636598c1c9578eec9627"
          },
          "capture_reference": {
            "path": "assets/additions/spatter-cone/batch87-20261021/spatter-cone.png",
            "sha256": "3928899e7cecd550dea1d696633a8708986fb15a2696cd6080810ecadf23264c"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/spatter-cone.json",
            "sha256": "6c2a5333b534abdf5bdef2e5e59c156a65b98a2e8ee1f44e3089f8ac3231a297"
          }
        },
        {
          "id": "travertine-terrace-pools",
          "batch": 87,
          "revision": "r003",
          "candidate_root": "production/batch87-landform-repair/travertine-terrace-pools/r003",
          "source_commit": "bf13b45a810871434efd525b5d99c329869223d8",
          "reviewed_source_commit": "178664a29c9bf5a751ccb3833e749e539d1b3745",
          "original_source_snapshot": "bf13b45a810871434efd525b5d99c329869223d8",
          "review_commit": "bf13b45a810871434efd525b5d99c329869223d8",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/travertine-terrace-pools/batch87-20261021/release-metadata.json",
            "sha256": "985212100adef6255ded77f0f5b9d69b151b350b5a964e1097a9ae0e88af45e3"
          },
          "candidate": {
            "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/candidate.json",
            "sha256": "53e94c1007fb1f4cd36dd81ec68f65ecb4a138b4654618a64e1eb638bc17d04f"
          },
          "active_candidate": {
            "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/candidate.json",
            "sha256": "53e94c1007fb1f4cd36dd81ec68f65ecb4a138b4654618a64e1eb638bc17d04f"
          },
          "original_profile": {
            "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/profile-contract.json",
            "sha256": "4275910b75b8289862443d8e1fd2af786003964f6d15dac50767c15270d21b64"
          },
          "active_profile": {
            "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/profile-contract.json",
            "sha256": "4275910b75b8289862443d8e1fd2af786003964f6d15dac50767c15270d21b64"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/independent-qa.report.json",
            "sha256": "0b281b8b61e7d0c0b2e3f213bc7d11c0d189cb525cd6de255c2d67eed587a7ac"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/independent-qa.report.json",
            "sha256": "0b281b8b61e7d0c0b2e3f213bc7d11c0d189cb525cd6de255c2d67eed587a7ac"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/independent-qa.report.json",
              "sha256": "0b281b8b61e7d0c0b2e3f213bc7d11c0d189cb525cd6de255c2d67eed587a7ac"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/own-manifest.json",
              "sha256": "4dac9fa742663664d9177ba88f56afa055a202e63f55cfa5dabd21514a78c394"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/handoff.json",
              "sha256": "dee1c8fbe67a845a9ae8bc92b8452bcb7e011475bff5cd3227672e951b74304b"
            }
          ],
          "original_metrics": {
            "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/artifacts/metadata.json",
            "sha256": "d6321deac27902ea615d7da7251a0a53181af084584b95cb8320cf68c98a4f99"
          },
          "source_counts": {
            "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/qa/authored-evaluated-counts.json",
            "sha256": "a29e96c1204f06fdbcc9c9d3c38f3ae595dd37c9d127b8c908965fac2d7ed142"
          },
          "proof": {
            "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/render-manifest.json",
            "sha256": "7b460b76d6d1a24c67bc7b7b6f1797935f269d8a0c0175e8231c1c60db42c25a"
          },
          "source_preview": {
            "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/hero.png",
            "sha256": "5a0130fe3ef020ff96323df391243dfa242d42e72ec09c65bcca8bb5957d6450"
          },
          "capture_reference": {
            "path": "assets/additions/travertine-terrace-pools/batch87-20261021/travertine-terrace-pools.png",
            "sha256": "fe39dac483f43e0492b46f92d33f34e212605a8c2bcae5886ff049bc61dbf27c"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/travertine-terrace-pools.json",
            "sha256": "5c3f67e2c56edbaaf9e2a9444f1169fc5c23c4c2e7e61480a5ebe11d099ed48e"
          }
        }
      ],
      "files": [
        {
          "path": "production/batch87-landform-repair/dependencies.json",
          "sha256": "8cb97ca290e8de6b86bc8237cc66ec1c29c8f380a081117dbc0050ae9930b09a",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/artifacts/metadata.json",
          "sha256": "af6cae7ecc941ccee69b165a62b93c5963b0634bf8b558a697e20a9e00987538",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/artifacts/spatter-cone.blend",
          "sha256": "764db2ea957a5acc1bb342a95916958a6976a63146ba7107ce022617f444a086",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/artifacts/spatter-cone.glb",
          "sha256": "51b4daefbebba036ba57c76b932f2d18b265349c84d047261dbfbd1c223936a7",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/candidate.json",
          "sha256": "3f6b3531dd6b17dbf569ce4f562f64804d32ef49d540e9dc958366f6a2ea73f9",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/config.json",
          "sha256": "0461fb35a332241a03988b820882e106d1d4fb1bcd0e09f3428f785dd1cca38b",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/delivery-brief.json",
          "sha256": "a6488cc54e12c5e76c68403781075464d39d74abfe325f71b432f10bbb700b5a",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/profile-contract.json",
          "sha256": "b2fb663878a9ac6e4924d9991d6822d9918af6b0d23c3b849de9e5fa579c2b40",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/qa/authored-evaluated-counts.json",
          "sha256": "bd0ccb6aac4b467bbfd2f9815d3f4bccb9ce68bdd43c699a79efae1d4279c57d",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/qa/runtime-parse.report.json",
          "sha256": "169546e21c0eafdf206979973b13a1687de1e7b464096ad90a4480a9f75135e9",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/qa/technical.report.v002.json",
          "sha256": "d435409b2149d8bf25d2961944bfe1d377dd08009dbac6ccd967a588446b1c59",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/references.json",
          "sha256": "427cee9955bcb668e22d1544c5509a22bb3e2c3194c4d940cd67457fc2180ce0",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/views/clay.png",
          "sha256": "dc04e8d52da6271c36a5bd42907ff9511b8f680ae40b29df8fa05f66fd801739",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/views/front.png",
          "sha256": "d5637de53e5273c83e1f74bda671a75463b05c85907028a66dbef5dab26c80d8",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/views/hero.png",
          "sha256": "9b12ba9c80d8a1f6817cdfdb830d66b19e6ea7e6ccfb636598c1c9578eec9627",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/views/rear.png",
          "sha256": "8797836b096d6d36aaf97065968bcb8f3c054f2aab13a254a81c1c104f5e2c7e",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/views/render-manifest.json",
          "sha256": "ad92c8435c5a8c30aeb9a6e8c9139d8c0668b0083605bb33731ebd0061f5ecf2",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/views/reversehero.png",
          "sha256": "07db073c2708470a2d4aced9ca34c67111d792dd7c8f6f31e123b5260c13fe10",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/views/side.png",
          "sha256": "d766538d1f350a2736f7f8d07d1d7b1affb0100301cb543a41e92e6d390bdbb2",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/views/silhouette.png",
          "sha256": "6d517f1a22b9b91638097a19099c2d32200dba4241cc5c36ca1896e25549a6f8",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/spatter-cone/r006/views/top.png",
          "sha256": "214c78457154c8ddfa6d9335921c2b892cb3fbdf39b6c6f68527d27493ff6814",
          "origin": "source",
          "owner": "spatter-cone"
        },
        {
          "path": "production/batch87-landform-repair/tools/generate-spatter-r006.py",
          "sha256": "63c37474f4c422d69a591e113af755e1ff3400e16691c0d63b6a762d653d7889",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/batch87-landform-repair/tools/generate.py",
          "sha256": "03195c099638be91ea0d58a0ceaacb19ee2a155922de11520bfc9601abe5c553",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/batch87-landform-repair/tools/measure-local.py",
          "sha256": "76c7ef30bc2f223e4efe48ddca62558b005fd1f1fb1de417e30d2cee13cea231",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/artifacts/metadata.json",
          "sha256": "d6321deac27902ea615d7da7251a0a53181af084584b95cb8320cf68c98a4f99",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/artifacts/travertine-terrace-pools.blend",
          "sha256": "19c44e5f37c85599857478084e659cd60dbf73b57b2d9389be2715fe8d435a4a",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/artifacts/travertine-terrace-pools.glb",
          "sha256": "f0b8e2558e44250555c7205858f602e1bcab8ba33f2b2f1a8fb0934b3227c432",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/candidate.json",
          "sha256": "53e94c1007fb1f4cd36dd81ec68f65ecb4a138b4654618a64e1eb638bc17d04f",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/config.json",
          "sha256": "46ace1bb0436a3c82254fc337adea53461369e9cd2e6443f7cfd6fe291b67516",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/delivery-brief.json",
          "sha256": "f69b79b772bfbeb236f908c9fa64f46b4aaac77f385f83f2c8a92c81a1974c1c",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/profile-contract.json",
          "sha256": "4275910b75b8289862443d8e1fd2af786003964f6d15dac50767c15270d21b64",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/qa/authored-evaluated-counts.json",
          "sha256": "a29e96c1204f06fdbcc9c9d3c38f3ae595dd37c9d127b8c908965fac2d7ed142",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/qa/runtime-parse.report.json",
          "sha256": "7ffdedfe73b5f6fdcc09b9eeb8cb3ab10c756d295bc192466db89ba78a2ba741",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/qa/technical.report.v002.json",
          "sha256": "e246e452d9e5a6b896a15e05f1c91d8ecd2563eae67c35d780c4d97176c9276f",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/references.json",
          "sha256": "efa7af1cc375054c9c7afa276ebeb4ddd5aadfa19bb293e424711044431bdfcd",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/clay.png",
          "sha256": "8ba6847b968f3b365ea1b16cc5b826addfcca601cc95734b6fc8ba78569b2808",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/front.png",
          "sha256": "00c36963eec5ef7b848f4bf8755fb9b3f710c7bbe8b93c22331c123a34672b6e",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/hero.png",
          "sha256": "5a0130fe3ef020ff96323df391243dfa242d42e72ec09c65bcca8bb5957d6450",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/rear.png",
          "sha256": "88421767163a87152ab748fdeeff4074186c29a10730ab8fa13442b6321ea25b",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/render-manifest.json",
          "sha256": "7b460b76d6d1a24c67bc7b7b6f1797935f269d8a0c0175e8231c1c60db42c25a",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/reversehero.png",
          "sha256": "338d1fabb6112f5c0284cef2da0bacd5bd70455f2c5bcd2eb15dff4fd506b9b4",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/side.png",
          "sha256": "754fd19d90bc20e2f7a967571a101d646cff7130582e08da815a5a6dc4e30464",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/silhouette.png",
          "sha256": "19fd5e80863467504799b828a3671f2b836787ea70f6e7dac423637a609c8913",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "production/batch87-landform-repair/travertine-terrace-pools/r003/views/top.png",
          "sha256": "4f70571345320e869497a74810e5e5c189f242e3704c8b23d9cb516e9c9e612b",
          "origin": "source",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/audit_evidence.py",
          "sha256": "b24c7cc82a189f4f1ee7c33d2c9ac8e5205bc52e8d3d66fe98a8d951ed51de5c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/handoff.json",
          "sha256": "dee1c8fbe67a845a9ae8bc92b8452bcb7e011475bff5cd3227672e951b74304b",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/independent-qa.report.json",
          "sha256": "0b281b8b61e7d0c0b2e3f213bc7d11c0d189cb525cd6de255c2d67eed587a7ac",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/independent-qa.report.md",
          "sha256": "447f710e5fcf4ef8949568e81307a98842326f408b690d5d8309b0c24f67109c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/own-manifest.json",
          "sha256": "4dac9fa742663664d9177ba88f56afa055a202e63f55cfa5dabd21514a78c394",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/reopen_measure.py",
          "sha256": "ceab3f98c0c5d6f8dfdb6b7697d71cd2479b18d0e6342afe4c1b23f8a9da410d",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/runtime_validate.mjs",
          "sha256": "342b069a95aa58e9d7eb7fdcd39a5cb8b4f0d11824e3b1baea9b58a8f69ff9ff",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/spatter-cone/candidate-validation.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "spatter-cone"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/travertine-terrace-pools/candidate-validation.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "travertine-terrace-pools"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-87-landform-repair/write_report.py",
          "sha256": "7bcfcb029f23f6b2d9acf8584b855988261a9f0a3de045710b5b487e02be94b9",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g16-release-20261021/process-archive-index.json",
          "sha256": "00c7bd6a166bcb5773083579a092ff549628a97217574c637b5d223ca13d22b5",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g17-20261021.json",
      "sha256": "a207dc7ebde50c89fa416e733b2dba793172d29fa3f6aaa7caa937384aee6a61"
    },
    "release": {
      "version": 1,
      "scope": "next52-g17-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "c3bc13e41e387061f951d9598c67e8f4b8f13ed9",
      "review_commit": "c3bc13e41e387061f951d9598c67e8f4b8f13ed9",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g17-release-20261021/source-bundle.json",
        "sha256": "c7344800be87647d7953ceeca38ca45f7d1796de40d6e9a9590694c5efc7a0d8"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
        },
        {
          "path": "scripts/qa_glb.py",
          "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/handoff.json",
          "sha256": "44a96d0ec071a83eefcd50a8b27a5948bf75dadc194e9fe29a8ae41ad2516137"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/independent-qa.report.json",
          "sha256": "e04ef105d0b72c5201007bbc1d600bc076ac57b3ae349357958671c6ac8ce88c"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/own-evidence-manifest.json",
          "sha256": "ba1e9801739e5f1ccb352bd6ca171687782ec7aa96aa8180d566af1fe80d94d6"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "glossopteris",
          "batch": 84,
          "revision": "r001",
          "candidate_root": "production/batch84/assets/glossopteris/r001",
          "source_commit": "c3bc13e41e387061f951d9598c67e8f4b8f13ed9",
          "reviewed_source_commit": "d7e1fed195c2c9fcb9690cdd52353b06b9edb261",
          "original_source_snapshot": "c3bc13e41e387061f951d9598c67e8f4b8f13ed9",
          "review_commit": "c3bc13e41e387061f951d9598c67e8f4b8f13ed9",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/glossopteris/batch84-20261021/release-metadata.json",
            "sha256": "9a835805da8cf1933b977f774fc1ea6587af7321355e7287e47dcb58039d2dae"
          },
          "candidate": {
            "path": "production/batch84/assets/glossopteris/r001/candidate.json",
            "sha256": "3d0e392f8ba51ee55e2a602106ee3de1a94deae86dae435b7165c606af36d6d4"
          },
          "active_candidate": {
            "path": "production/batch84/assets/glossopteris/r001/candidate.json",
            "sha256": "3d0e392f8ba51ee55e2a602106ee3de1a94deae86dae435b7165c606af36d6d4"
          },
          "original_profile": {
            "path": "production/batch84/assets/glossopteris/r001/profile-contract.json",
            "sha256": "8c90ee4413561b703ff225b04620135d5025ea60806f32f5b0f5deec57cad109"
          },
          "active_profile": {
            "path": "qa/fifty-two-website-release-20261021/release-coordination-profiles/glossopteris.json",
            "sha256": "9e1cf108cf2ad2163efbc6489df013ed724a7f46360982da896c42a3bcd38d7c"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-84/independent-qa.report.json",
            "sha256": "e04ef105d0b72c5201007bbc1d600bc076ac57b3ae349357958671c6ac8ce88c"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-84/independent-qa.report.json",
            "sha256": "e04ef105d0b72c5201007bbc1d600bc076ac57b3ae349357958671c6ac8ce88c"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-84/independent-qa.report.json",
              "sha256": "e04ef105d0b72c5201007bbc1d600bc076ac57b3ae349357958671c6ac8ce88c"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-84/own-evidence-manifest.json",
              "sha256": "ba1e9801739e5f1ccb352bd6ca171687782ec7aa96aa8180d566af1fe80d94d6"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-84/handoff.json",
              "sha256": "44a96d0ec071a83eefcd50a8b27a5948bf75dadc194e9fe29a8ae41ad2516137"
            }
          ],
          "original_metrics": {
            "path": "production/batch84/assets/glossopteris/r001/metrics.json",
            "sha256": "a1e7008f95b6f79145c84fb6264cc70e2d56b015a4977232f824b4d57f8b830e"
          },
          "source_counts": {
            "path": "production/batch84/assets/glossopteris/r001/source-vertex-counts.json",
            "sha256": "7f9a27715776f74c82aa548205dd863f0760c0d16355e6dcbf9d37e3b84ee898"
          },
          "proof": {
            "path": "production/batch84/assets/glossopteris/r001/proof-final3/render-manifest.json",
            "sha256": "516ad0c6c39fbe30647d15ac7e5235bf24dfb72362247a71e0ac08ecd2c5e6ca"
          },
          "source_preview": {
            "path": "production/batch84/assets/glossopteris/r001/preview.png",
            "sha256": "7d2904ca70bfc423a35ecd0d7b1d84c3bb472682b46838636e6a15780b79a125"
          },
          "capture_reference": {
            "path": "assets/additions/glossopteris/batch84-20261021/glossopteris.png",
            "sha256": "4b030af5bb6600eee8661de221f9bfd5a718e8b7e615e03a59eb88d5bf214c3a"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/glossopteris.json",
            "sha256": "b4df3b2cc0da2791e1078b134f94621799b5be864ec0ca4b1aa7d7b54732f9ea"
          }
        },
        {
          "id": "volcanic-neck",
          "batch": 84,
          "revision": "r003",
          "candidate_root": "production/batch84/assets/volcanic-neck/r003",
          "source_commit": "c3bc13e41e387061f951d9598c67e8f4b8f13ed9",
          "reviewed_source_commit": "d7e1fed195c2c9fcb9690cdd52353b06b9edb261",
          "original_source_snapshot": "c3bc13e41e387061f951d9598c67e8f4b8f13ed9",
          "review_commit": "c3bc13e41e387061f951d9598c67e8f4b8f13ed9",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/volcanic-neck/batch84-20261021/release-metadata.json",
            "sha256": "fb32ff8a0e4e4bbdaa39117dd077140fa7fa244b217328651f4af1ef779c67c7"
          },
          "candidate": {
            "path": "production/batch84/assets/volcanic-neck/r003/candidate.json",
            "sha256": "ae37e093b08eb0fe229bea3b69b9b54c058be026c09049e6b4d9a6046c6d1c46"
          },
          "active_candidate": {
            "path": "production/batch84/assets/volcanic-neck/r003/candidate.json",
            "sha256": "ae37e093b08eb0fe229bea3b69b9b54c058be026c09049e6b4d9a6046c6d1c46"
          },
          "original_profile": {
            "path": "production/batch84/assets/volcanic-neck/r003/profile-contract.json",
            "sha256": "934a7917423d88d481829712380e6ee05b9404461989e55ee26a5ff1080927bf"
          },
          "active_profile": {
            "path": "qa/fifty-two-website-release-20261021/release-coordination-profiles/volcanic-neck.json",
            "sha256": "051168a8eb9a571b9082b8ac1402c53ac984fc28fbc609b5e97f3a1bdaf23c4e"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-84/independent-qa.report.json",
            "sha256": "e04ef105d0b72c5201007bbc1d600bc076ac57b3ae349357958671c6ac8ce88c"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-84/independent-qa.report.json",
            "sha256": "e04ef105d0b72c5201007bbc1d600bc076ac57b3ae349357958671c6ac8ce88c"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-84/independent-qa.report.json",
              "sha256": "e04ef105d0b72c5201007bbc1d600bc076ac57b3ae349357958671c6ac8ce88c"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-84/own-evidence-manifest.json",
              "sha256": "ba1e9801739e5f1ccb352bd6ca171687782ec7aa96aa8180d566af1fe80d94d6"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-84/handoff.json",
              "sha256": "44a96d0ec071a83eefcd50a8b27a5948bf75dadc194e9fe29a8ae41ad2516137"
            }
          ],
          "original_metrics": {
            "path": "production/batch84/assets/volcanic-neck/r003/metrics.json",
            "sha256": "60e9d2e1eb6c433c767c1d4e437a7b289e1ea63661ff48e341f9e95e9970ed9d"
          },
          "source_counts": {
            "path": "production/batch84/assets/volcanic-neck/r003/source-vertex-counts.json",
            "sha256": "49e8c0e8f5bab86b0835723762e409fdc533daea1ea66406d685fc359e7bf304"
          },
          "proof": {
            "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/render-manifest.json",
            "sha256": "a2e05ffaccb7cc96598bb0c87b040246e81f462fa7391d8999175eb2ee589d29"
          },
          "source_preview": {
            "path": "production/batch84/assets/volcanic-neck/r003/preview.png",
            "sha256": "f52ef04f6784efd222f52140efaa41a20ab25c530689df7c9db61df986fe90b0"
          },
          "capture_reference": {
            "path": "assets/additions/volcanic-neck/batch84-20261021/volcanic-neck.png",
            "sha256": "87edf25ca3ce532476c850276e11f860907dc5708544496e33430e888da2cf0b"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/volcanic-neck.json",
            "sha256": "fc90535f0f9176b451bede1e51b04b6aaaabff22b3e748a717fece2e11bf8007"
          }
        }
      ],
      "files": [
        {
          "path": "production/batch84/assets/glossopteris/r001/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/brief.md",
          "sha256": "c4b95a040d1d766ac9c024f5928101de48933892801fb76514b83dc2dd73316c",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/build-config.json",
          "sha256": "667037cbafc65bcdf627bb8734c531971dc9598c769a90469d9da2eabad0b7a8",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/build-dependencies.json",
          "sha256": "27a3d4765b1c78b8cd2bee750b6a4cc80daa94dabf488b19d4f77b6f44bfd20e",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/candidate-brief.json",
          "sha256": "dd9544e216587bc42eb84a08e28dcf3705a1ac8707c3783893f32b4cfeb22952",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/candidate.json",
          "sha256": "3d0e392f8ba51ee55e2a602106ee3de1a94deae86dae435b7165c606af36d6d4",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/concept-original.png",
          "sha256": "19740f6b7e549ae3cf9515301b5f16911a6ade2cd06929e256a8e1bd61ca2ad5",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/concept-prompt.txt",
          "sha256": "9ede0f5fe886338c2f076bc9200ba13e29ac3f290454d062666c7186bb3cb3d6",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/contact-sheet.png",
          "sha256": "e38e13e77efccb3db0ca441001efa0bb71a4cf68d9243b720cd9d1c90e8fb37c",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/generator.py",
          "sha256": "cdf80eb26c462bde241f73a699182d808be80ac70e52fba1078497b1f0b98b26",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/gltf-validator.report.json",
          "sha256": "e60b3c5f56e6361f3e92dc6a045e97c0094215a4f130c346daa4bd0bcc0938dc",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/lifecycle.jsonl",
          "sha256": "ea5799d18279978c7981105ee0270f14105f5dc2d8df1e4a711f1756a4bbd92a",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/maker-review.md",
          "sha256": "e537f881e136f77f342d316e0ac096c15a5b417294dd78bc2973df8ded30a80a",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/metrics.json",
          "sha256": "a1e7008f95b6f79145c84fb6264cc70e2d56b015a4977232f824b4d57f8b830e",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/model.glb",
          "sha256": "825d60ab47580bb5edad23c15575f24febda482a3be5a2b57adabbc96e12672d",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/modeling-freeze.json",
          "sha256": "a6cbc99f218f64d708f9e75a069e8a8f20bbb55cc911db47949d54dc1d7417c7",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/pixel-inspection.json",
          "sha256": "8dc7cbacd3b81b55bdf3e83d51fd0e61d8f80d91c4843b3b92d1bb5e96f673cf",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/preview.png",
          "sha256": "7d2904ca70bfc423a35ecd0d7b1d84c3bb472682b46838636e6a15780b79a125",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/profile-contract.json",
          "sha256": "8c90ee4413561b703ff225b04620135d5025ea60806f32f5b0f5deec57cad109",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/proof-final3/clay.png",
          "sha256": "9428cec57d99487197f1c39b55e696aa77b011e0e2eeb4a125950963629aab6a",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/proof-final3/front.png",
          "sha256": "66117c236b541e9df01fdfe188721ed83558049b99dbedd018a5e43ee69048e2",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/proof-final3/hero.png",
          "sha256": "7d2904ca70bfc423a35ecd0d7b1d84c3bb472682b46838636e6a15780b79a125",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/proof-final3/rear.png",
          "sha256": "713a915dfd7871c88a36f4e5365933abc70459aebe8a8ca2c7c8a12c55a11a67",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/proof-final3/render-manifest.json",
          "sha256": "516ad0c6c39fbe30647d15ac7e5235bf24dfb72362247a71e0ac08ecd2c5e6ca",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/proof-final3/reversehero.png",
          "sha256": "2579ccc749a813d4e3377858f4e0727fab1457598c3a47b6a1ce7022e955fd91",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/proof-final3/side.png",
          "sha256": "9e89847b215cdd8a66f4df5f153bbd17c0035045f9630c7680d3ddc83fe317c7",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/proof-final3/silhouette.png",
          "sha256": "f62e5f34cf52257a28d5844fa7a50a75563a9d9fb5fd0b401b410ac2fa6c60d5",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/proof-final3/top.png",
          "sha256": "50f19ed758b92faaf8b55b607f8a07310eb32978529c1dd5fa98fc8916e9ef71",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/references.json",
          "sha256": "810366eca1bd65f8ecd15ff24a64fc97dee870c0fc0025897de2bc629266c2ec",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/repro-final-1.report.json",
          "sha256": "8b6974ad701319a370aefcdc14fe2095986c2d60ab8f466fc4137fa5a20a71ce",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/repro-final-2.report.json",
          "sha256": "a78bd86324242724f13ecfa3e3ebb4b7c7d1106ef7debc2f361d1e43048061ca",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/runtime-parse.report.json",
          "sha256": "0ff6ec6bdacfffe74a22593f57e091b012751144df71d4d14120d8b00a76dee0",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/source-final.report.json",
          "sha256": "3ad3a25e1831d7f57299ac9674a2e97529f4e7a02c1c5f4a27596487768f68cd",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/source-metrics.json",
          "sha256": "2237400b33239321f346193e2545aa4d8009f5d7111ecd0fd10a171f2285ead3",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/source-vertex-counts.json",
          "sha256": "7f9a27715776f74c82aa548205dd863f0760c0d16355e6dcbf9d37e3b84ee898",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/glossopteris/r001/source.blend",
          "sha256": "5175c4f6e1dabb2fc03626c5cbf4703646370ea30e89db4db9589077a6041764",
          "origin": "source",
          "owner": "glossopteris"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/brief.md",
          "sha256": "018ad103bd783786c6de12c70dc03a4176fcbaa9467ce47600aa15f522b659f5",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/build-config.json",
          "sha256": "59150bd7363e4887e05a670be5cf0877eb14f19d85fac2c50fbf3449b6c998e6",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/build-dependencies.json",
          "sha256": "d4f534281be18600f5ad938b1f19b695029c16c9d048cbd4b676277f7d5a141e",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/candidate-brief.json",
          "sha256": "05835435c89f1570f7e90b5b73c338ef7236ec156e8cf42109473360f9f7ff5d",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/candidate.json",
          "sha256": "ae37e093b08eb0fe229bea3b69b9b54c058be026c09049e6b4d9a6046c6d1c46",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/concept-original.png",
          "sha256": "9b2c018103a6a1cd2eaf763f60cc76e623c2f219b992528d9045803e8f075550",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/concept-prompt.txt",
          "sha256": "be7177849cbd3e8a298b6d8d931ca4724c72f340031ae212232574ee634d03e7",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/contact-sheet.png",
          "sha256": "e2e0d2864b2a410f63717ac3c80c6246a87c07312a914bf345f1c47ed4a48a67",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/generator.py",
          "sha256": "53648bbccbc0b27f28e9585d5bdd5911019cb41d3b6b33bb42a17d378a09b68b",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/gltf-validator.report.json",
          "sha256": "0a675ae63396cc4aa0d3ae7771f463076c8024442d877d5c6ee9b4868c8a2bbe",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/lifecycle.jsonl",
          "sha256": "cc0dfb58edd4f2a09459de877ab475f8685d9bf9063c502161747a2d50fca631",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/maker-review.md",
          "sha256": "4084b1f3ed8a3d32a8f1072d0fdf95e6be62a8e524080279c7e3127a48fafef6",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/metrics.json",
          "sha256": "60e9d2e1eb6c433c767c1d4e437a7b289e1ea63661ff48e341f9e95e9970ed9d",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/model.glb",
          "sha256": "a1e302c4c4b1042274828a1287a0a28598bd652681a5efa546b291b13d4a1c74",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/modeling-freeze.json",
          "sha256": "39a1b8cccb4e498142bc0576bbe7def650d53ce46d7437051aa38ce638c468c5",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/physical-surfaces.report.json",
          "sha256": "ac3ae8a8076204b5180af0a8c153f991c77beea13660143972aad3029cd7ab1b",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/pixel-inspection.json",
          "sha256": "eefbab3e75e4f8407db4f6537dc67327ef2bfd594316b3ac3e32a1ee99d869ee",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/preview.png",
          "sha256": "f52ef04f6784efd222f52140efaa41a20ab25c530689df7c9db61df986fe90b0",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/profile-contract.json",
          "sha256": "934a7917423d88d481829712380e6ee05b9404461989e55ee26a5ff1080927bf",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/clay.png",
          "sha256": "664747e00d254a41f8a653eb1d006e1b49e1ff3d5bd3b2fbf4104bf5449c3cee",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/front.png",
          "sha256": "dac981486e152283ed717863cab07a052d2738f9f4847ea3dde83d4f8190f981",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/hero.png",
          "sha256": "f52ef04f6784efd222f52140efaa41a20ab25c530689df7c9db61df986fe90b0",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/rear.png",
          "sha256": "c1207907938d3dcf6a8fe280f8942a29cfe0bb5504a1090719ba45640e313dde",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/render-manifest.json",
          "sha256": "a2e05ffaccb7cc96598bb0c87b040246e81f462fa7391d8999175eb2ee589d29",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/reversehero.png",
          "sha256": "e5e7de4ee62ca0c4fa11e6e7da38959d5631cf74009701708001a13153cb00cc",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/side.png",
          "sha256": "f49065c7df9b7b43171d70ed60fa3423bdf0cc05f1683aee75b524b88485229a",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/silhouette.png",
          "sha256": "7dac77e375f4da9ddf3f60f2a1047d350e2aa08a7715ec101cbfcd4dd07ed85c",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/proof-final3/top.png",
          "sha256": "7a28e1ef927823e969096bc55263ce8be925f8c252937ab9a5dc3179d3378198",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/references.json",
          "sha256": "cfcdfcf85c0b483baf3bd6b31100e0494dfedca2c3fe8409baa4498843c9c104",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/repair-freeze.json",
          "sha256": "0bfe158dbd092d1ec993ffdce8a181978ee4cfb5323e8e1a2a9798a7328e3100",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/repro-final-1.report.json",
          "sha256": "45fe52736afa67857b476eb5ab3a8a2845a17623be1ad5dcd1a6b64f8bdec0bf",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/repro-final-2.report.json",
          "sha256": "b18a697fde72c535fc55d456ae1a76cabd08b6e796ebf82d8c0f4c2b958081f9",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/runtime-parse.report.json",
          "sha256": "9f06fb759cb3b195d131ac973bb453d01873f6a17432ee19746dec962b68978a",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/source-final.report.json",
          "sha256": "6d4d01ef289dc606274fe7bbe10ff2cd571e1cd748d9413151faa3193631bff1",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/source-metrics.json",
          "sha256": "fbd2adab13ca250afca261eced1e0f55713d28e6f96705d5d64f7c8036d5cae1",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/source-vertex-counts.json",
          "sha256": "49e8c0e8f5bab86b0835723762e409fdc533daea1ea66406d685fc359e7bf304",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/assets/volcanic-neck/r003/source.blend",
          "sha256": "843820189078606d0afd6a4b6a62bc3e26dce40460aec06e6db2270a9182df43",
          "origin": "source",
          "owner": "volcanic-neck"
        },
        {
          "path": "production/batch84/publication-policy-reference.json",
          "sha256": "e1b5ca2a1a5a06415ffb8c0dcf04e1a9a17dc868edef170c01d74bce09362a93",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/REPORT.md",
          "sha256": "be36e6d8cdcb3cb1d60cb63a02e64dc4e057e6f751ed5858d13d231c4632f639",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/analyze_geometry.py",
          "sha256": "629f4585200b6570d004edd07b0781323594ccc518915c9d5979a91f1cbbe6ae",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/audit_inputs.py",
          "sha256": "1d4344a076bd8abbc646e79a0f3826bcdf05a51f58917ea2e53a8f6dec352b25",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/finalize_report.py",
          "sha256": "78b786df91e773b5152b811b558908187033cd4b2a8fad9bf89bada3398c48f5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/handoff.json",
          "sha256": "44a96d0ec071a83eefcd50a8b27a5948bf75dadc194e9fe29a8ae41ad2516137",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/independent-qa.report.json",
          "sha256": "e04ef105d0b72c5201007bbc1d600bc076ac57b3ae349357958671c6ac8ce88c",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/own-evidence-manifest.json",
          "sha256": "ba1e9801739e5f1ccb352bd6ca171687782ec7aa96aa8180d566af1fe80d94d6",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/prepare_checks.py",
          "sha256": "ebc5300b3e2e736ec59d68d2496c2561ab467dfea89d5ab2e6e3a795c17a366e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/render_focused_diagnostics.py",
          "sha256": "5063368c24c559a1d5461be79a60f8a6fdc9aff88be4a3d65c820c1c69dbb5b8",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/render_focused_diagnostics_v2.py",
          "sha256": "46512298746d12c9faf0edd19e4a0e12ad8e41c90da8305df03021664602a24f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/run_diagnostics.py",
          "sha256": "14224f135acac27a6041d9bf2342961be38b9d8480ad0b80aa9887446684e73e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/run_diagnostics_v2.py",
          "sha256": "1fb620e01c51f30395f515770b4f1459a3a3f74eccf1fbbd5e61e650168605cf",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/run_fresh_checks.py",
          "sha256": "b8dcc980ecaef93759d9032f643ee9480811aa2a2b6ba00845fdd7e7bc2ce1cb",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/runtime_checks.mjs",
          "sha256": "4f1e4f3c8e90281fa2b7ba4719fac8c7ee6cad63df93a681535dd3c2eeb673fe",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-84/source_reexport.py",
          "sha256": "76d8d351c95c4b62d1d8081088a1a42e24c2af3e540490684805d7c91c606426",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g17-release-20261021/process-archive-index.json",
          "sha256": "2badf51c83c7ea62b553e964388b19874883cfc84b8a80a23e4c80d66226969a",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g18-20261021.json",
      "sha256": "5f7c91e7a2c270bb866132b89121845cabfd0a9d5f898ba22d3d2c5562fd66be"
    },
    "release": {
      "version": 1,
      "scope": "next52-g18-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
      "review_commit": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g18-release-20261021/source-bundle.json",
        "sha256": "5337feb5d67979773ec5c1e3abbacf22ac1b293c24bbd853529ba15c1a0d94c0"
      },
      "protected_source_inputs": [
        {
          "path": "package-lock.json",
          "sha256": "4b89f2140f1d25a363df7e4afa505df747c06dfbc3833c2df40158fc1c63bfb2"
        },
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
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
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        },
        {
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/fixed-handoff.json",
          "sha256": "260a2db7f302d105f169c95f6110d04396a6559174661c728b360a333fd00e02"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
          "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/own-manifest.json",
          "sha256": "a0ea726fd18f46250eaf41667d5962b4befda77546877b653b5eb38eb0124ba7"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "pterosaur-manus-pes-trackway",
          "batch": 91,
          "revision": "r002",
          "candidate_root": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002",
          "source_commit": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
          "reviewed_source_commit": "7a47ea6412457767bdc9abdf662b3cb92c6965df",
          "original_source_snapshot": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
          "review_commit": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/pterosaur-manus-pes-trackway/batch91-20261021/release-metadata.json",
            "sha256": "c3653945a3159a4402f943728c57101459a55632917ad63c3ebcd2e8d6e5129a"
          },
          "candidate": {
            "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/candidate.json",
            "sha256": "f0a52fbfa90543ed45743d9ff6f1a0e3a4757d3bf16c62f4f3901e427e6629e9"
          },
          "active_candidate": {
            "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/candidate.json",
            "sha256": "f0a52fbfa90543ed45743d9ff6f1a0e3a4757d3bf16c62f4f3901e427e6629e9"
          },
          "original_profile": {
            "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/profile-contract.json",
            "sha256": "cb33e810a64b72c1aab722b99ad70487fc2591e8705568fb114044b5af2d9540"
          },
          "active_profile": {
            "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/profile-contract.json",
            "sha256": "cb33e810a64b72c1aab722b99ad70487fc2591e8705568fb114044b5af2d9540"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
            "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
            "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
              "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-91/own-manifest.json",
              "sha256": "a0ea726fd18f46250eaf41667d5962b4befda77546877b653b5eb38eb0124ba7"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-91/fixed-handoff.json",
              "sha256": "260a2db7f302d105f169c95f6110d04396a6559174661c728b360a333fd00e02"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/artifacts/metadata.json",
            "sha256": "da6828538ee9a6671a231d4465f66b887a2afc9d3ea88d96eda00c66607f7002"
          },
          "source_counts": {
            "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/qa/authored-evaluated-counts.json",
            "sha256": "50307b0dc9038510eb62df1ffae794763e3c1de488ad419c2d0f484ac8e96746"
          },
          "proof": {
            "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/render-manifest.json",
            "sha256": "5dc086480cabe3641c4902a9a8c0928bab2963c7d10e229cf80da4489327685f"
          },
          "source_preview": {
            "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/hero.png",
            "sha256": "3a0b6b14516ad28ff350fa576908e9d02ceccab880c7c9247d7ef5485735c518"
          },
          "capture_reference": {
            "path": "assets/additions/pterosaur-manus-pes-trackway/batch91-20261021/pterosaur-manus-pes-trackway.png",
            "sha256": "c0c4da82c3efc0b07ec5b60ccce07d84c3abf9de7f2afc7e5033f36b602ef905"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/pterosaur-manus-pes-trackway.json",
            "sha256": "58e4d5edb7a08c29d232844dde375764a8c4dc7365bcbdb36e82dee917cde7a4"
          }
        },
        {
          "id": "sauropod-manus-pes-trackway",
          "batch": 91,
          "revision": "r001",
          "candidate_root": "production/small-life-batch91/sauropod-manus-pes-trackway/r001",
          "source_commit": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
          "reviewed_source_commit": "7a47ea6412457767bdc9abdf662b3cb92c6965df",
          "original_source_snapshot": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
          "review_commit": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/sauropod-manus-pes-trackway/batch91-20261021/release-metadata.json",
            "sha256": "93c9f75a23e2f0940b6eb6d3bac08212fc812c81b582df7dcd0b2a8b118dd131"
          },
          "candidate": {
            "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/candidate.json",
            "sha256": "404f06e865780e7df8da5c5b8a4612449e818a55ab783145cc27aea86d1a2db2"
          },
          "active_candidate": {
            "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/candidate.json",
            "sha256": "404f06e865780e7df8da5c5b8a4612449e818a55ab783145cc27aea86d1a2db2"
          },
          "original_profile": {
            "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/profile-contract.json",
            "sha256": "aa099e7afda060e51e39cb76c1cc44ee0df8e987d0f6028ab469880095c82adf"
          },
          "active_profile": {
            "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/profile-contract.json",
            "sha256": "aa099e7afda060e51e39cb76c1cc44ee0df8e987d0f6028ab469880095c82adf"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
            "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
            "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
              "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-91/own-manifest.json",
              "sha256": "a0ea726fd18f46250eaf41667d5962b4befda77546877b653b5eb38eb0124ba7"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-91/fixed-handoff.json",
              "sha256": "260a2db7f302d105f169c95f6110d04396a6559174661c728b360a333fd00e02"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/artifacts/metadata.json",
            "sha256": "7f29e665c874f2d38f280fe13abcf9f760f0e8a332550d7e0d8cc9626014017a"
          },
          "source_counts": {
            "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/qa/authored-evaluated-counts.json",
            "sha256": "99323454ced4618186b6c1681a21c3c7bfe2e7348c15f53f8ddafa677ce976ea"
          },
          "proof": {
            "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/render-manifest.json",
            "sha256": "a020b82770cff5bade45690f2160cb77866311ee3764ed45e8a6982b0d0f2e35"
          },
          "source_preview": {
            "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/hero.png",
            "sha256": "3afbb057c5e13bbe177f66fa4050301b404473bb3f5f16cec00063461336c415"
          },
          "capture_reference": {
            "path": "assets/additions/sauropod-manus-pes-trackway/batch91-20261021/sauropod-manus-pes-trackway.png",
            "sha256": "577efc6afcba966d30d983327eea89aab7cc0e6ab6a304c7c70a5d47bfb64d34"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/sauropod-manus-pes-trackway.json",
            "sha256": "de0252f9e38deb1d3171656c2084864eefa87430efeba1248c8e750e48f9b270"
          }
        },
        {
          "id": "spiral-coprolite",
          "batch": 91,
          "revision": "r003",
          "candidate_root": "production/small-life-batch91/spiral-coprolite/r003",
          "source_commit": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
          "reviewed_source_commit": "7a47ea6412457767bdc9abdf662b3cb92c6965df",
          "original_source_snapshot": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
          "review_commit": "c6a511b6996055e9ce3803faa2517ab27ea36bbc",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/spiral-coprolite/batch91-20261021/release-metadata.json",
            "sha256": "19e2982dc81b8b97c598d8fe2af6808ee7556e86f70e77b7040f55c15d272b42"
          },
          "candidate": {
            "path": "production/small-life-batch91/spiral-coprolite/r003/candidate.json",
            "sha256": "4cd04d066891afadc4539752ce7245510ea0870d0a8781c1c7b00bce1a5dd559"
          },
          "active_candidate": {
            "path": "production/small-life-batch91/spiral-coprolite/r003/candidate.json",
            "sha256": "4cd04d066891afadc4539752ce7245510ea0870d0a8781c1c7b00bce1a5dd559"
          },
          "original_profile": {
            "path": "production/small-life-batch91/spiral-coprolite/r003/profile-contract.json",
            "sha256": "aa51c2076c7eaef59f029c58685f7077143be2977ad841b5ce556b0752d56521"
          },
          "active_profile": {
            "path": "production/small-life-batch91/spiral-coprolite/r003/profile-contract.json",
            "sha256": "aa51c2076c7eaef59f029c58685f7077143be2977ad841b5ce556b0752d56521"
          },
          "original_stage_statuses": {
            "technical": "pass",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "pass",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
            "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
            "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
              "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-91/own-manifest.json",
              "sha256": "a0ea726fd18f46250eaf41667d5962b4befda77546877b653b5eb38eb0124ba7"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-91/fixed-handoff.json",
              "sha256": "260a2db7f302d105f169c95f6110d04396a6559174661c728b360a333fd00e02"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch91/spiral-coprolite/r003/artifacts/metadata.json",
            "sha256": "bb598e64c9fff97fee27eb1ca3313f93dcbe4fbbd40c4b4c440c9b55da26ce82"
          },
          "source_counts": {
            "path": "production/small-life-batch91/spiral-coprolite/r003/qa/authored-evaluated-counts.json",
            "sha256": "8582f2f10ee899109c299790c2f3d1b40b3f397f6e140618ce0a60464acddfdc"
          },
          "proof": {
            "path": "production/small-life-batch91/spiral-coprolite/r003/views/render-manifest.json",
            "sha256": "070b314f2dd4315b762c73e2f269481b8ed563537a509e8d984d37222716abb1"
          },
          "source_preview": {
            "path": "production/small-life-batch91/spiral-coprolite/r003/views/hero.png",
            "sha256": "e057205aa4285d90a3d6bea68ce4f8935c95f5fb2ba82fb53ff98b0c12d0b37c"
          },
          "capture_reference": {
            "path": "assets/additions/spiral-coprolite/batch91-20261021/spiral-coprolite.png",
            "sha256": "594982e1ee1cf743d9581859e9253438dae848ab40d3b209587926edac717b71"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/spiral-coprolite.json",
            "sha256": "8eee9d32a6c6d1782f933d11de2a8050bedccbd1c1b856b04975198f0c31267b"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch91/concepts/pterosaur-manus-pes-trackway-concept.png",
          "sha256": "c1e2221957f682e3c85be669dfe60b14e618eb33e75fc2d50eb2c25c9645ade4",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/concepts/pterosaur-manus-pes-trackway-prompt.txt",
          "sha256": "7b433a294a6404ef25aa7e6957c393f4289597b93f33f2ac8deef4f0693aba19",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/concepts/sauropod-manus-pes-trackway-concept.png",
          "sha256": "b8971f8e64614f1e2ee91ea0db3d8a55460dccb16ba39c5a60b92f43ef715257",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/concepts/sauropod-manus-pes-trackway-prompt.txt",
          "sha256": "93e44d32d21f5d2152324fd0f3be8a72073616b82bc980afa3486ed2557356b0",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/concepts/spiral-coprolite-concept.png",
          "sha256": "17bb005791f93e153663eedcdb23c2db95541f7fe7f6a2002ea33feceaa8f908",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/concepts/spiral-coprolite-prompt.txt",
          "sha256": "5a029b78ef17be216e00c38a1b0122a10ab88bfc80115c9e71fd9b838329ea11",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/dependencies.json",
          "sha256": "3c604b537213402f1778a14aab989b38b7da0ea0e94a996ed14a3c8392fd19a3",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r001/references.json",
          "sha256": "48d6310aaea0a7f97bfa53e02eeb464154ea771c949637bcd0f024e833688edf",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/artifacts/metadata.json",
          "sha256": "da6828538ee9a6671a231d4465f66b887a2afc9d3ea88d96eda00c66607f7002",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/artifacts/pterosaur-manus-pes-trackway.blend",
          "sha256": "ef98012a7901191f812516b379885417bc1c631b97abd8256c918ed64d33eb77",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/artifacts/pterosaur-manus-pes-trackway.glb",
          "sha256": "be8849cc5425c8e65776b24e9db3157958387afd1f0b3291d728d32b3093377a",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/candidate.json",
          "sha256": "f0a52fbfa90543ed45743d9ff6f1a0e3a4757d3bf16c62f4f3901e427e6629e9",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/config.json",
          "sha256": "bfcc78ea782b4ecfb4c032f15ecd5416b5ca043ea972e909488c79ac781216d6",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/delivery-brief.json",
          "sha256": "584ce300d75f4a6f4d90687620f7d4007f7110314ca6f0fdf39cb1dff63ce109",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/profile-contract.json",
          "sha256": "cb33e810a64b72c1aab722b99ad70487fc2591e8705568fb114044b5af2d9540",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/qa/authored-evaluated-counts.json",
          "sha256": "50307b0dc9038510eb62df1ffae794763e3c1de488ad419c2d0f484ac8e96746",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/qa/runtime-parse.report.json",
          "sha256": "72333204ef6e7ff97511309e9c623edc66e07b4d814644c457e989346e7b6927",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/qa/technical.report.json",
          "sha256": "10484443dac54ccb109e84245a49a471d122f2d6d795cbb463ade13d49f29d49",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/clay.png",
          "sha256": "3e2635dac61700c8decfaed9ac50627c9fd1cd896fd50cab48a83add1e8d5837",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/front.png",
          "sha256": "22f4068a6d5cf87a44826bbe5a56bc0cc65bc652ac3d5204f12ab1010a8ec5f0",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/hero.png",
          "sha256": "3a0b6b14516ad28ff350fa576908e9d02ceccab880c7c9247d7ef5485735c518",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/rear.png",
          "sha256": "fc31eb8b5ee4e4ccfba70d9ab9e463490239bcd1e32767a58d813442fa1d13e0",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/render-manifest.json",
          "sha256": "5dc086480cabe3641c4902a9a8c0928bab2963c7d10e229cf80da4489327685f",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/reversehero.png",
          "sha256": "c32f2fe7c6c9ba6669dcc9c9d2995c5c68747f7e959e60892ac53ec7a99db221",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/side.png",
          "sha256": "c1889b60fea69272f9bf5f1864ba61c369ce3e9e3fcfeb5da120dd36c8e879bd",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/silhouette.png",
          "sha256": "97fd2604d9a0164175c0b9d79d75c48006f856f7669c5dad668c71c5cf9843b4",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/pterosaur-manus-pes-trackway/r002/views/top.png",
          "sha256": "e1618563bcc2f81384d3a0119212c5345b0891a3d931c73860e58c408609e32c",
          "origin": "source",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/artifacts/metadata.json",
          "sha256": "7f29e665c874f2d38f280fe13abcf9f760f0e8a332550d7e0d8cc9626014017a",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/artifacts/sauropod-manus-pes-trackway.blend",
          "sha256": "ad3c837966a5b21ec4b1cbd89c4144ebceb62eb6f2600fabd00ff79d80ef1563",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/artifacts/sauropod-manus-pes-trackway.glb",
          "sha256": "ccd0b3fa682a43e50384414b98aac04faa78414e8ef92e51427e7025a8b86952",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/candidate.json",
          "sha256": "404f06e865780e7df8da5c5b8a4612449e818a55ab783145cc27aea86d1a2db2",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/config.json",
          "sha256": "105bbe450ea322b9a1ac0c68bd9c09734461faa32a4fecd7aa377e69b0dac6ba",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/delivery-brief.json",
          "sha256": "d9d9e02fc64c829dbe17e391d53a0cef17afe8d284f9a71214b1c1581025893a",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/profile-contract.json",
          "sha256": "aa099e7afda060e51e39cb76c1cc44ee0df8e987d0f6028ab469880095c82adf",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/qa/authored-evaluated-counts.json",
          "sha256": "99323454ced4618186b6c1681a21c3c7bfe2e7348c15f53f8ddafa677ce976ea",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/qa/runtime-parse.report.json",
          "sha256": "19180f2ac7cc78e4b1dc8d320192ecdd3962d0e2cdf83c88c1871bc26c0a1248",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/qa/technical.report.json",
          "sha256": "b125f94e576cfdfaf66d23f8204ef1b1b06657a52c83639cc2f557f5b023553d",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/references.json",
          "sha256": "9545393cf1cb168b270fe3854c941c0c885a3652999d3eeae03867b10d7ecb61",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/clay.png",
          "sha256": "198f8f397eae2b832677bfd40a7a2e39d054055743060d278b2ce1d55452997c",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/front.png",
          "sha256": "4d1426060081a35cf526850c43778380a80537b799781e91d79761ed716eab96",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/hero.png",
          "sha256": "3afbb057c5e13bbe177f66fa4050301b404473bb3f5f16cec00063461336c415",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/rear.png",
          "sha256": "8a1ee33fbb75a768ed8d20ab077b4f1341c89572ec3dd41a7025ae55f1a9f707",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/render-manifest.json",
          "sha256": "a020b82770cff5bade45690f2160cb77866311ee3764ed45e8a6982b0d0f2e35",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/reversehero.png",
          "sha256": "dfea8f55d84ef564f4ae9a2eab34fdc8507f628036dd86c581da7e7e75a97583",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/side.png",
          "sha256": "edc17d29654c451abe252a6ff86f0985f68f60c4d529e820586949b79436cded",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/silhouette.png",
          "sha256": "60a19c25a440740d52658d456f3a51c4c47b95b7971d73aa11f983997038b29a",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/sauropod-manus-pes-trackway/r001/views/top.png",
          "sha256": "a4f5bace5bbac70e309b225aae61a05214a2c849efcf77156e134546ee585c38",
          "origin": "source",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r001/references.json",
          "sha256": "ac2f23f4b59593825d2d56701f9aacee628dcdf79e1c63d3ee3eb22d77ca3d3a",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/artifacts/metadata.json",
          "sha256": "bb598e64c9fff97fee27eb1ca3313f93dcbe4fbbd40c4b4c440c9b55da26ce82",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/artifacts/spiral-coprolite.blend",
          "sha256": "fafb419066fa2429edb9d2ff86a555ff1d006de8154148679c9ec1d5be433d5e",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/artifacts/spiral-coprolite.glb",
          "sha256": "b7646d7a4cad0baf299e6087b7517766272c08d26441b94396e652f6c6e59f86",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/candidate.json",
          "sha256": "4cd04d066891afadc4539752ce7245510ea0870d0a8781c1c7b00bce1a5dd559",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/config.json",
          "sha256": "54091d78122b9d3be16bcca181f7ede5fd3ffdea7a356b3ce766640e8633862f",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/delivery-brief.json",
          "sha256": "477dd4a46201e27dd78d5b87fbc5a2ac1329f80186eebe2db968a67369e68bd5",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/profile-contract.json",
          "sha256": "aa51c2076c7eaef59f029c58685f7077143be2977ad841b5ce556b0752d56521",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/qa/authored-evaluated-counts.json",
          "sha256": "8582f2f10ee899109c299790c2f3d1b40b3f397f6e140618ce0a60464acddfdc",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/qa/runtime-parse.report.json",
          "sha256": "48fffa3736ab96b53c4cd6d0edd24de4b09991a39654d3e8f62e12f13d085bc3",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/qa/technical.report.json",
          "sha256": "dccbb6b2cc0125405c8cccc5a08064eaf57a437f8dbe4b80a3a152483fbf38b5",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/views/clay.png",
          "sha256": "ad55a81e5174471d9e17c9d978db62ed317df0ba846d66c270a85c5f60187a96",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/views/front.png",
          "sha256": "f25ddf6a7323135d85aeb35f5d7e3a00c1c457a1824ac82a421b9969314ae086",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/views/hero.png",
          "sha256": "e057205aa4285d90a3d6bea68ce4f8935c95f5fb2ba82fb53ff98b0c12d0b37c",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/views/rear.png",
          "sha256": "6c80a806611f2ed261d56b408f664b1bf44b93181613f845d35b16443b439978",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/views/render-manifest.json",
          "sha256": "070b314f2dd4315b762c73e2f269481b8ed563537a509e8d984d37222716abb1",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/views/reversehero.png",
          "sha256": "932ccce6fb322c7e0008fc38257c2159d175cc4baaaf59c188bdb3b3521526e4",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/views/side.png",
          "sha256": "9386255abdabeeaea05c4bfd7d50d5236c6e2637ef1e0a3961f8c986df9c988a",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/views/silhouette.png",
          "sha256": "260cd74e3d3e4196029ecb791cae4ca89a98ae14c6bc69de541643058f665861",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/spiral-coprolite/r003/views/top.png",
          "sha256": "702691962880da7a8551f44a60d8a09b49aeccc6f68bc456e412ebaa7d53a0c7",
          "origin": "source",
          "owner": "spiral-coprolite"
        },
        {
          "path": "production/small-life-batch91/tools/generate-r002.py",
          "sha256": "c1f90ad81bfb51e6f795ead795f74ce0537ead640ac2a9dd714ad018a75e67f2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch91/tools/generate-r003.py",
          "sha256": "c55c54432c03f8efacafa9e6f3f46b031e9439ded81e9119d3a3e50d403cb204",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch91/tools/generate.py",
          "sha256": "1ff06b4be2a30fe7817bb2ef4ec17ada62e8f3e1cd8dbb2df88e0c4d932f82b2",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch91/tools/measure_source.py",
          "sha256": "280b0e35f4595ab933a46f79b52484a429ed0ded391783580965908bca95dbb9",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch91/tools/parse.cjs",
          "sha256": "813bbe4ebbfc1cd80b2d45075f34a43bab68989991e3f81a0858a76c88a790d5",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch91/tools/render.py",
          "sha256": "dce6084f0ec6663a5ca5acd3f5815f128314c4e2c94c04748be153ed75c6879e",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/audit_bundle.py",
          "sha256": "e15d9d56a21cce16be5d398f7e8e5bbe47346741e70d7d934a77b05b07acf9d8",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/audit_geometry.py",
          "sha256": "ae4a2684a8f8d97b9c9b8c3ac5bfdc45384630d3c8742d7c73daf61dc57cbcba",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/fixed-handoff.json",
          "sha256": "260a2db7f302d105f169c95f6110d04396a6559174661c728b360a333fd00e02",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.json",
          "sha256": "aca6479a52bd9c3924e5fbd7549fa4a108eabbf147b77fac369f77b52574755f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/independent-report.md",
          "sha256": "ee59c95f521b94ba1767116856249909b4659a788c5f750ab320fb2881fb17ff",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/own-manifest.json",
          "sha256": "a0ea726fd18f46250eaf41667d5962b4befda77546877b653b5eb38eb0124ba7",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/pterosaur-manus-pes-trackway/candidate-schema.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "pterosaur-manus-pes-trackway"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/reopen_reexport.py",
          "sha256": "f7ea91be4fff8c04a33def11bae85ee99461e16bc952ff6487f86babfb2fe353",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/run_reopens.py",
          "sha256": "e167f43e8c1dc42e2767a722c9c4951e9551864744b73a3ba51f9d9317c9dc5a",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/sauropod-manus-pes-trackway/candidate-schema.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "sauropod-manus-pes-trackway"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/seal_report.py",
          "sha256": "6c0444e3516ed04e9ad121c1aca3f177408423dbdab17d275d00c1dab9fca049",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/spiral-coprolite/candidate-schema.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "spiral-coprolite"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-91/validate-runtime.cjs",
          "sha256": "96b08bebd9a77b923b95f4e5fa4c9dd981f7336f47f0c5dc50e6026a08b8932f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g18-release-20261021/process-archive-index.json",
          "sha256": "6431bab24f3d560289db2f29e1acb60c6f52b50d1960220b56c57fc0ad091835",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g19-20261021.json",
      "sha256": "d7d4c19c71ae1abb24556e3fc73e363f9ab6d66e4cfda1977a9ac124f8265f5e"
    },
    "release": {
      "version": 1,
      "scope": "next52-g19-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "d5ce0e66b1b3d5f3e83a43fe43d8fc58ffd52dbe",
      "review_commit": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g19-release-20261021/source-bundle.json",
        "sha256": "2a922ce0b08cd529848129b15751736b72fe7087ae5444ddd4a4c717d4c7e15d"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "production/small-life-batch81/publication-policy-reference.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
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
          "path": "scripts/rebuild_frozen_blender.py",
          "sha256": "c5971fab63b69fa3720d52b9884789eb56f6c2b1d2db4d6c9d3fa2bc77a59db6"
        },
        {
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        },
        {
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/handoff.json",
          "sha256": "5aef021e61b539525ef9a93d3a9bbe2798da968d8d61fcb0f0d0abe617335aa5"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
          "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/own-evidence-manifest.json",
          "sha256": "e3544ad288627002b76b60c503f53898a10d181481021a172cc12ef9b621f0a0"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "inselberg",
          "batch": 81,
          "revision": "r002",
          "candidate_root": "production/small-life-batch81/assets/inselberg/r002",
          "source_commit": "d5ce0e66b1b3d5f3e83a43fe43d8fc58ffd52dbe",
          "reviewed_source_commit": "51368e6e458a531b362babd3f1d8f940faaa05ec",
          "original_source_snapshot": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
          "review_commit": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/inselberg/batch81-20261021/release-metadata.json",
            "sha256": "8dfe6b8efae82b81a37abcb1e31ae8423be818b53e27c6f544bd858a69936d4f"
          },
          "candidate": {
            "path": "production/small-life-batch81/assets/inselberg/r002/candidate.json",
            "sha256": "748ec79d3d9ecb4acd863413cce5ef454a9cecf9d6cad1ec93554ea2fe6463f1"
          },
          "active_candidate": {
            "path": "production/small-life-batch81/assets/inselberg/r002/candidate.json",
            "sha256": "748ec79d3d9ecb4acd863413cce5ef454a9cecf9d6cad1ec93554ea2fe6463f1"
          },
          "original_profile": {
            "path": "production/small-life-batch81/assets/inselberg/r002/profile-contract.json",
            "sha256": "5ca4d3236f4df2c77a94ccbcadd5c95622624dc486a1f50d91dc93651fd7a922"
          },
          "active_profile": {
            "path": "production/small-life-batch81/assets/inselberg/r002/profile-contract.json",
            "sha256": "5ca4d3236f4df2c77a94ccbcadd5c95622624dc486a1f50d91dc93651fd7a922"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
            "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
            "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
              "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81/own-evidence-manifest.json",
              "sha256": "e3544ad288627002b76b60c503f53898a10d181481021a172cc12ef9b621f0a0"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81/handoff.json",
              "sha256": "5aef021e61b539525ef9a93d3a9bbe2798da968d8d61fcb0f0d0abe617335aa5"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch81/assets/inselberg/r002/metrics.json",
            "sha256": "b55a34d932ffb7c4f33e6bc39570782a3da3000d5f6f5f81a529a97ccf8cd68e"
          },
          "source_counts": {
            "path": "production/small-life-batch81/assets/inselberg/r002/source-vertex-counts.json",
            "sha256": "51fc163f13284a8f3054a18e2366a012dd409e1cc32a7a745fdad7759336513a"
          },
          "proof": {
            "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/render-manifest.json",
            "sha256": "0d4cabe053cb38376f40605773c24c07547ade82d070db17e5b7849c164ec240"
          },
          "source_preview": {
            "path": "production/small-life-batch81/assets/inselberg/r002/preview.png",
            "sha256": "f44d4bc4dc090e2f3b6db43e8ca7c151ac3a0f7cbca44ac8a1e273e4e603e9af"
          },
          "capture_reference": {
            "path": "assets/additions/inselberg/batch81-20261021/inselberg.png",
            "sha256": "87d4662f67de413df0bbcabd8c5271eb7634a3ef7e45d77dad54d62d614fc304"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/inselberg.json",
            "sha256": "cf93a0d08c066856b099b9c7c3b0ed682013288bb7ec1573d3d95ca699b43485"
          }
        },
        {
          "id": "patterned-stone-circles",
          "batch": 81,
          "revision": "r004",
          "candidate_root": "production/small-life-batch81/assets/patterned-stone-circles/r004",
          "source_commit": "d5ce0e66b1b3d5f3e83a43fe43d8fc58ffd52dbe",
          "reviewed_source_commit": "51368e6e458a531b362babd3f1d8f940faaa05ec",
          "original_source_snapshot": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
          "review_commit": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/patterned-stone-circles/batch81-20261021/release-metadata.json",
            "sha256": "068724ef86b7a592fa9f3f81ff865b3efe66236c5985531f1da816a12b38e4d9"
          },
          "candidate": {
            "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/candidate.json",
            "sha256": "29a5d6724c06ffefddb4767498809f488a57b7b0b8563d2509b069c9d38612ee"
          },
          "active_candidate": {
            "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/candidate.json",
            "sha256": "29a5d6724c06ffefddb4767498809f488a57b7b0b8563d2509b069c9d38612ee"
          },
          "original_profile": {
            "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/profile-contract.json",
            "sha256": "86ad28520893b72b9a8c7292644001e0d8462f647393f5bce36b144acb582b79"
          },
          "active_profile": {
            "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/profile-contract.json",
            "sha256": "86ad28520893b72b9a8c7292644001e0d8462f647393f5bce36b144acb582b79"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
            "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
            "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
              "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81/own-evidence-manifest.json",
              "sha256": "e3544ad288627002b76b60c503f53898a10d181481021a172cc12ef9b621f0a0"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81/handoff.json",
              "sha256": "5aef021e61b539525ef9a93d3a9bbe2798da968d8d61fcb0f0d0abe617335aa5"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/metrics.json",
            "sha256": "82007959843e98280de10bc70f374e4a8234f48fa39ee13d5f3a3381ce06199f"
          },
          "source_counts": {
            "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/source-vertex-counts.json",
            "sha256": "719e76bf18dc80cacc979026a209355d74e29549f3c7de6e01e614fd537d6abd"
          },
          "proof": {
            "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/render-manifest.json",
            "sha256": "cb1545828a6e3306eec1ebc4f661f2b8634b126eed0bafa4795981f8da811571"
          },
          "source_preview": {
            "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/preview.png",
            "sha256": "e1daf5bcf5aa052cc7118bcca68e7d044cd1d58397376448dacbc3507ed4f996"
          },
          "capture_reference": {
            "path": "assets/additions/patterned-stone-circles/batch81-20261021/patterned-stone-circles.png",
            "sha256": "02c4f98857c304e28bcc16ae7ba51914795d63cce086d3e781d0c1090714f9aa"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/patterned-stone-circles.json",
            "sha256": "f676e7d10d2912450d9dbe0d6e7b5ab4ea7d700ad0500c1d6cd1189f427f2d8d"
          }
        },
        {
          "id": "valley-glacier",
          "batch": 81,
          "revision": "r002",
          "candidate_root": "production/small-life-batch81/assets/valley-glacier/r002",
          "source_commit": "d5ce0e66b1b3d5f3e83a43fe43d8fc58ffd52dbe",
          "reviewed_source_commit": "51368e6e458a531b362babd3f1d8f940faaa05ec",
          "original_source_snapshot": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
          "review_commit": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/valley-glacier/batch81-20261021/release-metadata.json",
            "sha256": "c7da08ca8708ace6ce3a44fc0a7f5b54918394f8589e975e0e061ac7bb4708ef"
          },
          "candidate": {
            "path": "production/small-life-batch81/assets/valley-glacier/r002/candidate.json",
            "sha256": "5e8867b0961e426d64be54f591a15e6b0f5fbe40b99d7279b65e64ac0e461d16"
          },
          "active_candidate": {
            "path": "production/small-life-batch81/assets/valley-glacier/r002/candidate.json",
            "sha256": "5e8867b0961e426d64be54f591a15e6b0f5fbe40b99d7279b65e64ac0e461d16"
          },
          "original_profile": {
            "path": "production/small-life-batch81/assets/valley-glacier/r002/profile-contract.json",
            "sha256": "6cca6218d39bd700fd4b860552a966b2da7daf6ef8a9851b3b08153a1378ece9"
          },
          "active_profile": {
            "path": "production/small-life-batch81/assets/valley-glacier/r002/profile-contract.json",
            "sha256": "6cca6218d39bd700fd4b860552a966b2da7daf6ef8a9851b3b08153a1378ece9"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
            "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
            "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
              "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81/own-evidence-manifest.json",
              "sha256": "e3544ad288627002b76b60c503f53898a10d181481021a172cc12ef9b621f0a0"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81/handoff.json",
              "sha256": "5aef021e61b539525ef9a93d3a9bbe2798da968d8d61fcb0f0d0abe617335aa5"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch81/assets/valley-glacier/r002/metrics.json",
            "sha256": "9f40b8242511b29c875a88d3c0a23e6bc121c0cf743d10fc68a70eb45a8e1b23"
          },
          "source_counts": {
            "path": "production/small-life-batch81/assets/valley-glacier/r002/source-vertex-counts.json",
            "sha256": "1acfa7f5274b77be751f651ce640baf34302d6928e510ceff7b4f7ec014c1c6c"
          },
          "proof": {
            "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/render-manifest.json",
            "sha256": "3fa69c058c62f5288a9a724ccf140baed9805dbda292c151081a3b510b296ba7"
          },
          "source_preview": {
            "path": "production/small-life-batch81/assets/valley-glacier/r002/preview.png",
            "sha256": "95f23a1293e45607fec09fc2bec48731925ab26aa9898bfda29cea7ed39c1b6e"
          },
          "capture_reference": {
            "path": "assets/additions/valley-glacier/batch81-20261021/valley-glacier.png",
            "sha256": "3e3b213e2016c490e01938a3c0503d5aaa7b5ec38ea7a9d1c16e0d1a87c8fbff"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/valley-glacier.json",
            "sha256": "89b3297104b5cc0cb2a1bda23f561260b45e728d17f582a818bcbf772c3da434"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/brief.md",
          "sha256": "b708bf9e7b2cad6937f09f7273d195a38da31aba9e8cccb3e3393efd47411e9a",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/build-config.json",
          "sha256": "46528041f27954ddcf7f80b5bf9ffc8e6f09dc17d47c8c92e0d2a33c47fa97d4",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/build-dependencies.json",
          "sha256": "33140f9b345e1a31180141bdff153641cd16c557d82e430c188232c3fbfa7463",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/candidate-brief.json",
          "sha256": "be9f49152c84c90e383332ca3f343c61b04cf2f0d254d3a904238e59e0181493",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/candidate.json",
          "sha256": "748ec79d3d9ecb4acd863413cce5ef454a9cecf9d6cad1ec93554ea2fe6463f1",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/concept-original.png",
          "sha256": "52eec0dc9d21e5fe6516edd2c1e68c2351e16687f048d5af08b1cf11c2c58a19",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/concept-prompt.txt",
          "sha256": "2993ebdbe8081970f8de4f939d115967fe3a1b0feef9ca7480dc37942331d867",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/contact-sheet.png",
          "sha256": "ff7200c76989e6ec857862a2ffaab3a21316f23ab9bdc3622dbee2e33509ffde",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/final-rebuild-binding.json",
          "sha256": "38aa3c8f842db134dbfba95851917c86d06a09ada8968507559570e05212e3c7",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/generator.py",
          "sha256": "8eb3deb47688c0b005ff4e0ec0a86fa7f71f6244af525ead7b6e9ca9f0a4bac4",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/gltf-validator.report.json",
          "sha256": "b6ca3d3c48335e10dd1a172dc43e849ea5ab3d5671661da8b64c094c081e0485",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/lifecycle.jsonl",
          "sha256": "1484166bbede442a1af48729290796e872503b2bf5b2c6ced808df2e1eed9f9b",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/maker-review.md",
          "sha256": "8bec4afac70f456978a23d4495ced24e1fa410976a92497e879754d7d6b79002",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/metrics.json",
          "sha256": "b55a34d932ffb7c4f33e6bc39570782a3da3000d5f6f5f81a529a97ccf8cd68e",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/model.glb",
          "sha256": "ea11ad794fa02469190c6dc911b0fffeeca0d1b3287a479274ed3c024505f2ad",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/modeling-freeze.json",
          "sha256": "4e499db4e2011dd9963a5a19844ab358edc16a832b4a635fd5413c69f84d11dc",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/physical-surfaces.report.json",
          "sha256": "bb117b8e73b009c11f98e9d1fa1509ecf111d9012c1ee3326fb8ead63601b1d0",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/pixel-inspection.json",
          "sha256": "19e83954a21e5f4c0d6eeee11626b06a1162939ee7f637f5b5862588b57d86f7",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/preview.png",
          "sha256": "f44d4bc4dc090e2f3b6db43e8ca7c151ac3a0f7cbca44ac8a1e273e4e603e9af",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/profile-contract.json",
          "sha256": "5ca4d3236f4df2c77a94ccbcadd5c95622624dc486a1f50d91dc93651fd7a922",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/clay.png",
          "sha256": "509bd688baa1b31b38284a451afe528e332ae50c0697e251434b03f9fa5a8ce4",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/front.png",
          "sha256": "a8536aeb2bbb67a0f5eeca1e1e90431394f1bbe49fdbff22f65d7ae5aaba43c8",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/hero.png",
          "sha256": "f44d4bc4dc090e2f3b6db43e8ca7c151ac3a0f7cbca44ac8a1e273e4e603e9af",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/rear.png",
          "sha256": "ec542becb29aa7329f7ea2dcbd12bdd8c597a5a687ebe7045d4b558b72a2d88a",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/render-manifest.json",
          "sha256": "0d4cabe053cb38376f40605773c24c07547ade82d070db17e5b7849c164ec240",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/reversehero.png",
          "sha256": "509fdc8fd5e343c6db903ee702c861332330e51ea246c90d979081ae14f9561d",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/side.png",
          "sha256": "ffcce58e5f03b601a7b7c47447235e1ea70813ceba0829edfd4397eccddb9e35",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/silhouette.png",
          "sha256": "36a07a1965d51e8dba7523bbfc001127dbc0460555de18c35811ea403d73710c",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/proof-final/top.png",
          "sha256": "27d1aa2b651ef1a8d25698ffc5d9ca0e122a41aeb696224ff035143d2a6e634a",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/references.json",
          "sha256": "3322002b5968de8fdc8c9c53654639e71fcf3de210bae454046a841f5732d2ae",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/repair-freeze.json",
          "sha256": "5ff4d6d3fcf4a821ce611e31687d7c1867bb3277e7c49c597273a0b99500dcf0",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/repro-final-1.report.json",
          "sha256": "9098ab4f4dad5c98246f54ef47e76f09f0564d7539ae9be45d826932182b826a",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/repro-final-2.report.json",
          "sha256": "7e8be8c71c27b074b839d220a9179a373f31a7ecfebb41a52f698b98131f75ae",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/runtime-parse.report.json",
          "sha256": "5a018ebf9b899422c77639d292d8ccaf52eb0c8c1e71562cdf8da7af5323ee8e",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/source-final.report.json",
          "sha256": "27b24cbfe35eef211de5ab8f9f83c4922fd251c37add32220be94e8f5d00aa9c",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/source-metrics.json",
          "sha256": "ad21dcdee712aa669446112b0d3444d2eb32c4e8be4543a11720b5b60b107e16",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/source-vertex-counts.json",
          "sha256": "51fc163f13284a8f3054a18e2366a012dd409e1cc32a7a745fdad7759336513a",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/inselberg/r002/source.blend",
          "sha256": "31e65324cb6cbe4393baeb655a063950c2d986816fe28932b1ac8f8ea4d826d7",
          "origin": "source",
          "owner": "inselberg"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/brief.md",
          "sha256": "ff5e23d80ab59a4904c4765d4a270bf631b05e1d0c88f105ff39e25d099cf011",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/build-config.json",
          "sha256": "34b135648ec98e17b5f14ced7813f2ce946a39959a774a23c677987f79082818",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/build-dependencies.json",
          "sha256": "79edf9d7a20a15a50c74a67f9285784c531a394a04035c2946a6d082a8189042",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/candidate-brief.json",
          "sha256": "91b7fb0d6572af3091b97b980d43709f0d0b7a78312bf4053ac6d4dd7d372bac",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/candidate.json",
          "sha256": "29a5d6724c06ffefddb4767498809f488a57b7b0b8563d2509b069c9d38612ee",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/concept-original.png",
          "sha256": "3b76117cbf12312162e47d783c3177517f6c3cc96652554a5e56aa8e16073ece",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/concept-prompt.txt",
          "sha256": "42e44eacb1f6886f280979cfddd5253c277249608adbca1a034f6e34b125dce2",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/contact-sheet.png",
          "sha256": "221aeb6e335d02706db95e7a11c459d34dc2e956738e14970fff782aeffd8b0a",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/final-rebuild-binding.json",
          "sha256": "825bf7da31bd034794ca8ba3e3d7d63bea4a8c36e68a16c85407c455ee6199f7",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/generator.py",
          "sha256": "9ce69665e961506f01dbf6020429e1b39cc2f7f2982d6a54a8922380f41688d9",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/gltf-validator.report.json",
          "sha256": "90069fa98e855ad6b1699e3f0f3f52cb7b35f7644c0735cacfa1b009034538ef",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/lifecycle.jsonl",
          "sha256": "cd87d694fda0aed623345cd2ad9d0e6e71f4803cf341136db9bc2b5265508ecb",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/maker-review.md",
          "sha256": "847c5a3cc245ddf3d959c517a2b966c0755fbfe7e09f06d39203762643240a04",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/metrics.json",
          "sha256": "82007959843e98280de10bc70f374e4a8234f48fa39ee13d5f3a3381ce06199f",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/model.glb",
          "sha256": "703a9aabf6e3a57b3dd80999a71948a9e51e6a837c79169d148f540c46caa727",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/modeling-freeze.json",
          "sha256": "752d0ba11fa66d25acec34e9600fe26fcd3e9da4c6ace2b04a9aa55c717ed538",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/physical-surfaces.report.json",
          "sha256": "f39bc4a249c553af82c998b58fad8f78016f286df0ef07a5e2f3a637e7df17c7",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/pixel-inspection.json",
          "sha256": "4ccbc5c5199b437cb8867b74c4a30e4895c8f27bde05651033940f2303b4808f",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/preview.png",
          "sha256": "e1daf5bcf5aa052cc7118bcca68e7d044cd1d58397376448dacbc3507ed4f996",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/profile-contract.json",
          "sha256": "86ad28520893b72b9a8c7292644001e0d8462f647393f5bce36b144acb582b79",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/clay.png",
          "sha256": "afffb98479c20d281f3d8e6b3045034e0970a598cacce4741605227728800e59",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/front.png",
          "sha256": "21819cc956da0ec66db572771b44c16cc5f836f931789a87027a4a2f1889aabe",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/hero.png",
          "sha256": "e1daf5bcf5aa052cc7118bcca68e7d044cd1d58397376448dacbc3507ed4f996",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/rear.png",
          "sha256": "179650fe16551901a8892e009f48b635b65656cd22398468d9d5a67871eda22c",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/render-manifest.json",
          "sha256": "cb1545828a6e3306eec1ebc4f661f2b8634b126eed0bafa4795981f8da811571",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/reversehero.png",
          "sha256": "7de8a3fd8a66f4dbbb9bdec60d8483681da52d3c6a14be4c20830595392b25d3",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/side.png",
          "sha256": "94deb0c510de109dafc43031ff4f3ebcbe27b63b0bb31c8b2d5ee9d5b49ba288",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/silhouette.png",
          "sha256": "025ebf79bc698b4d30a42f6d665b32f3d1f9fa6b24c7b84873140447aa29a158",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/proof-final/top.png",
          "sha256": "87c8f5e542bda75b04b41ad2c80c4721a371b72d9eccf0bc0fad44f7e4fb7b30",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/references.json",
          "sha256": "6fe89a434260b4cf7df3272e72186a6770457c0c4ae96f304fbfd5f4a48ca8e2",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/repair-freeze.json",
          "sha256": "1d4c70baa01e575830ad8cc4b9b774379a799cad37e90a954e7f892f9a392491",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/repro-final-1.report.json",
          "sha256": "c80cc0218ab4013faa2510f1646b367b7a39c5ddfcaca9214ad0cc4153aa9f5a",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/repro-final-2.report.json",
          "sha256": "7edd26bc4b4e3b538702711300a79b94e0b61bb33290d41664fbbb2a514e9f62",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/runtime-parse.report.json",
          "sha256": "bebc1608a8822b251b14c4680f74bd3c2f76ea47e5e55259cf63715531f96bda",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/source-final.report.json",
          "sha256": "81f5f5b89d7876ca5e7b9d27004cf881c80250869b05fd0b78b7c9b6c9dd7d82",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/source-metrics.json",
          "sha256": "b2f36502abae5694ed320741ee95ecdcc7875ccdde799ddc5260780c411c0bfd",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/source-vertex-counts.json",
          "sha256": "719e76bf18dc80cacc979026a209355d74e29549f3c7de6e01e614fd537d6abd",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/patterned-stone-circles/r004/source.blend",
          "sha256": "6d5471641b91c2479ca44d2b5f654457ce1b0b8eedbca7379c56a3a6d2614f76",
          "origin": "source",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/brief.md",
          "sha256": "6e5fc8d6043bbd883a288425dc252a911033e063e753151b06ffb1b24d272974",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/build-config.json",
          "sha256": "ef89d0df3d65460705cd9b80dadf5959542f9264d81498ba7cf8b1448fbe37dc",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/build-dependencies.json",
          "sha256": "250c5ccbefe57fb5632bf93383486218c742ef9b4d0bb5d14a44ebdf6caf5758",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/candidate-brief.json",
          "sha256": "6a1db550f28d213aa830b8ca3dbc271d2a33f736b9df7d238f7997408b25faf0",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/candidate.json",
          "sha256": "5e8867b0961e426d64be54f591a15e6b0f5fbe40b99d7279b65e64ac0e461d16",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/concept-original.png",
          "sha256": "1f3a479ae0b4671590c8bbbb36e57aa6f04bb397bc2c25e8faedea30d01172f7",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/concept-prompt.txt",
          "sha256": "df7649c712530d3111a00a86c30e8dab4fa2f23f983fb9360a7fdf19cfb35813",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/contact-sheet.png",
          "sha256": "630cb20cdb888625df7c7345ebe7d6ec30ec8d8fbec4f73c177cf66afa10d80c",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/final-rebuild-binding.json",
          "sha256": "2ff2477f8fbf69b55bb14b9b6318d3db3afd92d6b5fbdd4b3d7585ec13bedcc5",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/generator.py",
          "sha256": "50dc619a61f4e8569619e5f0ac93279320ad99834196952c8f90d8936db210bd",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/gltf-validator.report.json",
          "sha256": "6165b58610e68577be8776b7002e6ca1ceb9359d30c1d12b5939d5d0a5be1457",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/lifecycle.jsonl",
          "sha256": "dea3b1578252a6ceb249f9cd1590a7f1fe758e1e93ff55378fc4f567bcc2bafa",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/maker-review.md",
          "sha256": "fc83d6434438ac2ac10d940164d063476c8a90fbd572e0269ea8d2363b8464ab",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/metrics.json",
          "sha256": "9f40b8242511b29c875a88d3c0a23e6bc121c0cf743d10fc68a70eb45a8e1b23",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/model.glb",
          "sha256": "32ed50dddd1611d06d0ddcaa9d96a9b1af6b58e904a932879ba26f812b3f036d",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/modeling-freeze.json",
          "sha256": "fd64c141775265b46eb6909df6293119741f639c84908310704afb3c9e41b318",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/physical-surfaces.report.json",
          "sha256": "3b5fc158af725a2bcfc44579bde48957fd3ff6a7c35906798a2cab7ba47431f7",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/pixel-inspection.json",
          "sha256": "4747670a73e54240294bfa785163d2431e472b45b9f4b3238fc5abf495ee338f",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/preview.png",
          "sha256": "95f23a1293e45607fec09fc2bec48731925ab26aa9898bfda29cea7ed39c1b6e",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/profile-contract.json",
          "sha256": "6cca6218d39bd700fd4b860552a966b2da7daf6ef8a9851b3b08153a1378ece9",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/clay.png",
          "sha256": "3a3a133118d108bc67b2e1e7978df43dc19b32b3308ced454763dfbd72050454",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/front.png",
          "sha256": "e6c97236bc84d3b0c4ad173ca068d9fd1e0e7f9d546950101689e94ae05a07d2",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/hero.png",
          "sha256": "95f23a1293e45607fec09fc2bec48731925ab26aa9898bfda29cea7ed39c1b6e",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/rear.png",
          "sha256": "23a5741772b184b607dc73021b0d99e7735d96781c0162327d6019ac0057eb67",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/render-manifest.json",
          "sha256": "3fa69c058c62f5288a9a724ccf140baed9805dbda292c151081a3b510b296ba7",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/reversehero.png",
          "sha256": "fb4598bf6b36e1ea8d52a098601e672155b087642f47ff4deec780dd243c4aee",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/side.png",
          "sha256": "37275c65a155794baf35da779879de359ff9c1d962b0d6aa286ecdd64da6b098",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/silhouette.png",
          "sha256": "c46b3609b8888501b055b9bb261d99fbfdb78471dd62d6d3cdf35b9ec924d4d2",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/proof-final/top.png",
          "sha256": "c57606db3472396ed3aea197ddb6bd7cb38c9b7179dcdae0f666e6caf18c75be",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/references.json",
          "sha256": "ec5884a0bd139d84813437a1bdb8a895a1d566396e9a957ed39535453a940f23",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/repair-freeze.json",
          "sha256": "33ac71a80f993cf759d1cf52afe2f908fc9f2807df56df16bcb26e41b8b186db",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/repro-final-1.report.json",
          "sha256": "c1534fb8e36dc4ff60daf27b6a3a9a7875dabf30f513851c1335350b5b0bade7",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/repro-final-2.report.json",
          "sha256": "78771bc5f9ff614c138bae8c4d472ad63ba15f6ee89bd0b4996cddca46c6a77f",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/runtime-parse.report.json",
          "sha256": "586c61bc7d2d5ad5e0652f27a201abbaef0a5cbb5f3bec6259cdc433fe876129",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/source-final.report.json",
          "sha256": "e0c2f09c2783483fade1918b84fee7863fb25de32cd6309faac31bacd0aa4e90",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/source-metrics.json",
          "sha256": "74cef4b8f684ab53343ade0efc8f1f9865aa41ea7b5c78013b36292f92511e57",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/source-vertex-counts.json",
          "sha256": "1acfa7f5274b77be751f651ce640baf34302d6928e510ceff7b4f7ec014c1c6c",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/assets/valley-glacier/r002/source.blend",
          "sha256": "57549c6b090fef0ae135a146411c1f22cc5e45efb337b8d3de37e99eb0925459",
          "origin": "source",
          "owner": "valley-glacier"
        },
        {
          "path": "production/small-life-batch81/check-physical-surfaces.py",
          "sha256": "470f371dabe34231ee0a3e4c6856e5ae57751300aa563eb2c53570f7bed11d42",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch81/render-fixed8.py",
          "sha256": "e3654a0abb9bc8848e52fdf0c37c53ff34396aa876ab5a7ae0bc004607083058",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "production/small-life-batch81/runtime-parse.mjs",
          "sha256": "fb938eb6db606a51b904de3f58b2557b618fc5963bfcf225ad990b0b1244164c",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/REPORT.md",
          "sha256": "24182b20a2803087d1f3ee75c46fb06f3f990f61a1a7ea9a35292ce63d849ad2",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/audit_provenance.py",
          "sha256": "3623d8012cfefee013cec3b97fa0d123af9c1cc635f496329d40c5ce85fce150",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/finalize_report.py",
          "sha256": "df44f7f5a56ccc031cb29b40bea1d6c2bc5e375c4714d5c4d7242d1234ef9920",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/handoff.json",
          "sha256": "5aef021e61b539525ef9a93d3a9bbe2798da968d8d61fcb0f0d0abe617335aa5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/independent-qa.report.json",
          "sha256": "dc4306ca243388a7dee077231b50b976e7a2c318d2e37cf811e03f12ed3e62a5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/inselberg/candidate-fresh.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "inselberg"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/inselberg/concept-fresh.stderr.txt",
          "sha256": "464a21ff0652852f496612585db0a35542dcc2143611d31badaf9b1fe873c8ea",
          "origin": "review",
          "owner": "inselberg"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/own-evidence-manifest.json",
          "sha256": "e3544ad288627002b76b60c503f53898a10d181481021a172cc12ef9b621f0a0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/patterned-stone-circles/candidate-fresh.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/patterned-stone-circles/concept-fresh.stderr.txt",
          "sha256": "464a21ff0652852f496612585db0a35542dcc2143611d31badaf9b1fe873c8ea",
          "origin": "review",
          "owner": "patterned-stone-circles"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/render_supplemental_topclay.py",
          "sha256": "8940a365e40ac5c09ada6e3faa2ae50ffa6884915e7d76cded7af77b18cbf954",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/run_fresh_checks.py",
          "sha256": "f0d00e6f4b0ce25e782a1d0f474b6a6839124d17dfaf315a46c79f94087b978d",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/runtime_checks.mjs",
          "sha256": "00cce4240def2c2ac67d8f327987b65054dfe136cfc27e5436b7cdbebbd18e27",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/source_reexport.py",
          "sha256": "7b05a23975f06492ea121238555f820fe2c31f3a0c75636c57d3f926b0750f2f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/valley-glacier/candidate-fresh.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "valley-glacier"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81/valley-glacier/concept-fresh.stderr.txt",
          "sha256": "464a21ff0652852f496612585db0a35542dcc2143611d31badaf9b1fe873c8ea",
          "origin": "review",
          "owner": "valley-glacier"
        },
        {
          "path": "qa/next52-g19-release-20261021/process-archive-index.json",
          "sha256": "7e083cdc27779ddc6b0083af1f314a20479ae22246de2b1b0606bd9a7e933108",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g20-20261021.json",
      "sha256": "469ef19682db7fb3fa24f376d45b17d810aee2ee453da34d11243410fd7cdaed"
    },
    "release": {
      "version": 1,
      "scope": "next52-g20-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "d5ce0e66b1b3d5f3e83a43fe43d8fc58ffd52dbe",
      "review_commit": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g20-release-20261021/source-bundle.json",
        "sha256": "950ace88f12b08b42b716f153ef202f9ce474451773ddb6686673e1e3c6f6df7"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "production/small-life-batch81/publication-policy-reference.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
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
          "path": "scripts/rebuild_frozen_blender.py",
          "sha256": "c5971fab63b69fa3720d52b9884789eb56f6c2b1d2db4d6c9d3fa2bc77a59db6"
        },
        {
          "path": "scripts/run_asset_queue.py",
          "sha256": "c39174028b94513487f6936d0641b7fb4aa5a6da340526e3da49a724ecd5fd7e"
        },
        {
          "path": "scripts/validate_gltf.cjs",
          "sha256": "c8569d9226692071cbcfb7fa09d1f49710bba09cafda11be34e50f03c1e93ed7"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/handoff.json",
          "sha256": "e206f2b049791f7f091ad365aee7b10858539344f33440274629fc370633f4b4"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/independent-qa.report.json",
          "sha256": "fd933c0eef0e22dcf25b17416f1e3ee74fa0820666a36aa7ccfbcd18229220e4"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/own-evidence-manifest.json",
          "sha256": "8db267aa5cc5e4763adc837479e3638c2c5cf963e7e07f9cf5ea3681a18345f4"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "charnia",
          "batch": 81,
          "revision": "r006",
          "candidate_root": "production/small-life-batch81/assets/charnia/r006",
          "source_commit": "d5ce0e66b1b3d5f3e83a43fe43d8fc58ffd52dbe",
          "reviewed_source_commit": "47e3b51172f44176cd0bb2ad52bc01d7de32fddc",
          "original_source_snapshot": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
          "review_commit": "c1e3061c4dfdda6c5a0efaa112baaca9de983347",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/charnia/batch81-20261021/release-metadata.json",
            "sha256": "9804513cf1b3eb428a0e27f685f6bc152d92ae09cbee312db16f2fb9a379b18f"
          },
          "candidate": {
            "path": "production/small-life-batch81/assets/charnia/r006/candidate.json",
            "sha256": "689ae9ce9997551c60d01bc24fd9d17546c5fcc1efcee8a60960405053ab6e79"
          },
          "active_candidate": {
            "path": "production/small-life-batch81/assets/charnia/r006/candidate.json",
            "sha256": "689ae9ce9997551c60d01bc24fd9d17546c5fcc1efcee8a60960405053ab6e79"
          },
          "original_profile": {
            "path": "production/small-life-batch81/assets/charnia/r006/profile-contract.json",
            "sha256": "4cd807bf398870f5c66978ff74b72390d107c515191b3c0ba6b8c6e499a6aa16"
          },
          "active_profile": {
            "path": "production/small-life-batch81/assets/charnia/r006/profile-contract.json",
            "sha256": "4cd807bf398870f5c66978ff74b72390d107c515191b3c0ba6b8c6e499a6aa16"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/independent-qa.report.json",
            "sha256": "fd933c0eef0e22dcf25b17416f1e3ee74fa0820666a36aa7ccfbcd18229220e4"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/independent-qa.report.json",
            "sha256": "fd933c0eef0e22dcf25b17416f1e3ee74fa0820666a36aa7ccfbcd18229220e4"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/independent-qa.report.json",
              "sha256": "fd933c0eef0e22dcf25b17416f1e3ee74fa0820666a36aa7ccfbcd18229220e4"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/own-evidence-manifest.json",
              "sha256": "8db267aa5cc5e4763adc837479e3638c2c5cf963e7e07f9cf5ea3681a18345f4"
            },
            {
              "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/handoff.json",
              "sha256": "e206f2b049791f7f091ad365aee7b10858539344f33440274629fc370633f4b4"
            }
          ],
          "original_metrics": {
            "path": "production/small-life-batch81/assets/charnia/r006/metrics.json",
            "sha256": "ea44fae29a46dabf4d0b53e1a4447bd56c48915e88aee278736e8d1d7098f56d"
          },
          "source_counts": {
            "path": "production/small-life-batch81/assets/charnia/r006/source-vertex-counts.json",
            "sha256": "be3124233a4f7cd8d04f3acdf9cb898baa06c11a0ab47796f075f2422266af21"
          },
          "proof": {
            "path": "production/small-life-batch81/assets/charnia/r006/proof-final/render-manifest.json",
            "sha256": "1680ea8808e11f671934d8ed4d5e054489a8634c5c892e742343b61d170e5abc"
          },
          "source_preview": {
            "path": "production/small-life-batch81/assets/charnia/r006/preview.png",
            "sha256": "94e9bb8b422eb4c83d2ca9f9537318a5b03964eb319e3fa0730f3433c755e1ad"
          },
          "capture_reference": {
            "path": "assets/additions/charnia/batch81-20261021/charnia.png",
            "sha256": "ff3d6627e074c691e4b9cc64334910de00c5cb22f55ac4748223fd8afc043a99"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/charnia.json",
            "sha256": "0735ac9b5d631647cebed401c88b5534ec30252e26c9dbffc1ef2c1c32611719"
          }
        }
      ],
      "files": [
        {
          "path": "production/small-life-batch81/assets/charnia/r003/candidate.json",
          "sha256": "84ba5240448b8bd6e81c0046eb162313f1163ef6c88db9eea36ed4dfc81d383c",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r003/concept-original.png",
          "sha256": "8534ff98f9908fdc8d66494e2428e25ba17797fdfa985b7a84002d4dcbce1317",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r003/concept-prompt.txt",
          "sha256": "fa109b8386877e657df145621d0fe36f06866341e6a0e5b3ae9396983d7b3046",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r003/generator.py",
          "sha256": "a207d5107cb7330880fdcdea4ccb32ad87d547f6f9bbb8fdf7b236493e98bb03",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r003/maker-review.md",
          "sha256": "37a892b70ab4fee47771e299c2ecba33bfb264ddc24fb3aa0545beda8d587c7d",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/LICENSES.md",
          "sha256": "6e175466ea5cf2519c0242493819b9324f1cd4bfbb9e93771588d9f27d6bc752",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/brief.md",
          "sha256": "35a2436d5e645e63760e54f1ff719e8a7768409ed204cd7db62916fc5b5f1334",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/build-config.json",
          "sha256": "d2b30c9dcc745432de47b46da0b0ce8d68f6767994931bb9b7ef2b24af02361c",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/build-dependencies.json",
          "sha256": "4dd76c30255b62bfd2ceeb72ef808e3fb37d8c9fc0fbaaf4dc9f1f9ac53c01c8",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/candidate-brief.json",
          "sha256": "fa9c75c31fe42b8d8b608c4bdf397e96c20ff2b13ee389e7f1ed052cd4ee12eb",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/candidate.json",
          "sha256": "689ae9ce9997551c60d01bc24fd9d17546c5fcc1efcee8a60960405053ab6e79",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/concept-original.png",
          "sha256": "8534ff98f9908fdc8d66494e2428e25ba17797fdfa985b7a84002d4dcbce1317",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/concept-prompt.txt",
          "sha256": "fa109b8386877e657df145621d0fe36f06866341e6a0e5b3ae9396983d7b3046",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/contact-sheet.png",
          "sha256": "d88de2cd84af909907f54827702b5143645d345cb6fcbbd9c2d142348a8be8d2",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/final-rebuild-binding.json",
          "sha256": "ccf8595846f7225c981438055af476f77a16fce364a9253bbbd86df42b4b2a51",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/generator.py",
          "sha256": "b2d3e56c887c504cfb4e42070558d377fdb97ef37ca8e2cbc09300903180a024",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/gltf-validator.report.json",
          "sha256": "20033af33262bb1d24517cb9674656104a6487f4b77a2b62e46ad8d0d1ee46b7",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/lifecycle.jsonl",
          "sha256": "dd163ccc8bf81267459f7b4a6ed5098e1ff50d1cca8f8e0508b18579e15ae468",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/maker-review.md",
          "sha256": "c4b7afdca4a621cf64d9d197acebeaebf58b60f76be8a54489ca971a8400bcc3",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/metrics.json",
          "sha256": "ea44fae29a46dabf4d0b53e1a4447bd56c48915e88aee278736e8d1d7098f56d",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/model.glb",
          "sha256": "127650cc0c7dc1c00faf6606097dada8500846b2ec13401aba4966c12881a934",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/original-modeling-freeze.json",
          "sha256": "0c41b1df42fd16cae3a4bb1bef4c98886d36ed2c29dba58f948f3e85dd4ee691",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/original-scope-continuity.json",
          "sha256": "413ed18523928123a35b7ed19accf91a88f1a0f9f529413aace2372f192d75c2",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/physical-surfaces.report.json",
          "sha256": "85c7638062d387355b7256c41592e746c9090a6cf65a0ea81f5296775cb7d788",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/pixel-inspection.json",
          "sha256": "e7b58406e3ee1db802491e7757a5a3a686487564725db53060e77fa0b4158dac",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/preview.png",
          "sha256": "94e9bb8b422eb4c83d2ca9f9537318a5b03964eb319e3fa0730f3433c755e1ad",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/profile-contract.json",
          "sha256": "4cd807bf398870f5c66978ff74b72390d107c515191b3c0ba6b8c6e499a6aa16",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/proof-final/clay.png",
          "sha256": "00127551a5b541e22fc55b2b0e84b26b323d3a9869478d9835e6e3dca13a7edd",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/proof-final/front.png",
          "sha256": "cc1ff3bf687ff79ba1f945dcfc8b686a8a41bc0fcbbe08d1a15314ee7686c69e",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/proof-final/hero.png",
          "sha256": "94e9bb8b422eb4c83d2ca9f9537318a5b03964eb319e3fa0730f3433c755e1ad",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/proof-final/rear.png",
          "sha256": "4ba772d45403d4af92d36dbf932270628cfedf899ea11e2b537ac1b67c9e1b2a",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/proof-final/render-manifest.json",
          "sha256": "1680ea8808e11f671934d8ed4d5e054489a8634c5c892e742343b61d170e5abc",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/proof-final/reversehero.png",
          "sha256": "c167ebf00b646c43df4bc3d6f111fd0d8d99af9401d5f3a3f68dd49f6c4f3b93",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/proof-final/side.png",
          "sha256": "d5d4f4480705f998638d840f067926705860e11589ea59b390668e28697387f6",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/proof-final/silhouette.png",
          "sha256": "ab63bc1904196cd4319e7f8240fc0c43d6ac514bf40453cdd9c3c2b6b4b945ff",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/proof-final/top.png",
          "sha256": "acf2248ce5d8389ee49b2b1f33f9ce626cec067f09de96f828d27e904035674a",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/references.json",
          "sha256": "79013203822a7e4d7599545b1b4d0edbfcf5169c7e55f4b05228394fdca4a88d",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/repair-freeze.json",
          "sha256": "2f495257182c0532427c455173e47dc5b3ccacf508c8b328b9cba2ebcf83c462",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/repro-final-1.report.json",
          "sha256": "789133adc36357e1f886823d09e471131b06eb32458f863cc73a3db362985244",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/repro-final-2.report.json",
          "sha256": "d39c4026772078259ed79be1dd5abf7ee17de6a4a4db6ecc34304753f850fb31",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/runtime-parse.report.json",
          "sha256": "a611fd17b8b9980664770013b747ef586c401a4e5bc256ad2001402e603b8713",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/saved-source-reexport/source-reexport.report.json",
          "sha256": "be17dfb8e212a7a61b5f5c3693b6818ab64bd9a8e8503fe96bc2db4e79d14eeb",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/source-final.report.json",
          "sha256": "83059227ce12ee9b21473a9a5d818de0e0f9170ef41a9578c2ac6da232efc4aa",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/source-metrics.json",
          "sha256": "c18e62b0e548ff66bcf4f96f766fe9dde20d2054a52908c567977a2ddaa9a131",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/source-vertex-counts.json",
          "sha256": "be3124233a4f7cd8d04f3acdf9cb898baa06c11a0ab47796f075f2422266af21",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/assets/charnia/r006/source.blend",
          "sha256": "041801bb23c5bfca3d9bf9aa0e0f2a04714f0cc295713029cf692a17cdcdc96b",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/charnia-repair-tools/check-physical-surfaces.py",
          "sha256": "470f371dabe34231ee0a3e4c6856e5ae57751300aa563eb2c53570f7bed11d42",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/charnia-repair-tools/count-source-vertices.py",
          "sha256": "9211091a8a90fdac820ae374478c7f4b28fe1e799a03b764f69aff7aba23c21f",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/charnia-repair-tools/render-fixed8.py",
          "sha256": "e3654a0abb9bc8848e52fdf0c37c53ff34396aa876ab5a7ae0bc004607083058",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/charnia-repair-tools/runtime-parse.mjs",
          "sha256": "fb938eb6db606a51b904de3f58b2557b618fc5963bfcf225ad990b0b1244164c",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "production/small-life-batch81/charnia-repair-tools/source-reexport.py",
          "sha256": "b3d1df248cd30bcdd2e5941ddace47e63e750251a081b349a72c91b037679ad8",
          "origin": "source",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/REPORT.md",
          "sha256": "402004b9dfc58cef13185d4751669d8d81e0d833ffc4613f764f047b40d3708d",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/audit_inputs.py",
          "sha256": "50ff867597fd30a49682cf6bacea33977bde3240c4373faa86f347f3b71bed2a",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/audit_inputs_initial.py",
          "sha256": "26c3bbeaba1b85f34b0da56249f51cd9ce8e4326d03d43b8faefb88a70e94ddd",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/candidate-profile-fresh.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/concept-fresh.stderr.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/finalize_report.py",
          "sha256": "fa562a3499b73c051e0f5667b42ec573c68bd0a72aca32f9d6a33b0997c68847",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/handoff.json",
          "sha256": "e206f2b049791f7f091ad365aee7b10858539344f33440274629fc370633f4b4",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/independent-qa.report.json",
          "sha256": "fd933c0eef0e22dcf25b17416f1e3ee74fa0820666a36aa7ccfbcd18229220e4",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/own-evidence-manifest.json",
          "sha256": "8db267aa5cc5e4763adc837479e3638c2c5cf963e7e07f9cf5ea3681a18345f4",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/render_supplemental_topclay.py",
          "sha256": "8940a365e40ac5c09ada6e3faa2ae50ffa6884915e7d76cded7af77b18cbf954",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/run_fresh.py",
          "sha256": "649abd1eeb536e0e2b8a295ac39d1bfdc5b3b4f6ae5b32208b06750d1ae15095",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/runtime_checks.mjs",
          "sha256": "c15178e2a508f73cedd5fd760bae2942eb818730c1ff54ddb8a17addaf7448cf",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/continuous-small-life-round37-20261020/batch-81-charnia-r006/source_reexport.py",
          "sha256": "7b05a23975f06492ea121238555f820fe2c31f3a0c75636c57d3f926b0750f2f",
          "origin": "review",
          "owner": "charnia"
        },
        {
          "path": "qa/next52-g20-release-20261021/process-archive-index.json",
          "sha256": "5996f7e64c870831f87869d1652f5844f5e49f7a5000000f14d34c42291925a4",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g21-20261021.json",
      "sha256": "6faa1ab6de793950ef0b9d78e055ad22767446dc6eebb42b9fd735b59e6f38ad"
    },
    "release": {
      "version": 1,
      "scope": "next52-g21-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
      "review_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g21-release-20261021/source-bundle.json",
        "sha256": "8ee089b7bba36fe36aabb926e81f04b60b3c99c6319f28742be401277501c856"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
        },
        {
          "path": "scripts/qa_glb.py",
          "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
          "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/HANDOFF.json",
          "sha256": "aee1aaf8c42f21b884684c741bba25ffd176a1a4d6ac1681e301dd45cf246281"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/QA-MANIFEST.json",
          "sha256": "262106559a5f4c42a9c7e3a058518ee4c0d2599a26b38dbd0337c69b527d57c0"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "calamites",
          "batch": 94,
          "revision": "r001",
          "candidate_root": "production/batch94/assets/calamites/r001",
          "source_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "reviewed_source_commit": "b744a404a2d2d648adb44f633221d144f88f18ad",
          "original_source_snapshot": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "review_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/calamites/batch94-20261021/release-metadata.json",
            "sha256": "69889cbb5982e5aad0ef9211a3cc0acd0e93e045c94e9ca595babb3aa4814290"
          },
          "candidate": {
            "path": "production/batch94/assets/calamites/r001/candidate.json",
            "sha256": "b778145f5664350f1dd7f1a0862f298c6cb9200261ffb5db17b879534c707973"
          },
          "active_candidate": {
            "path": "production/batch94/assets/calamites/r001/candidate.json",
            "sha256": "b778145f5664350f1dd7f1a0862f298c6cb9200261ffb5db17b879534c707973"
          },
          "original_profile": {
            "path": "production/batch94/assets/calamites/r001/profile-contract.json",
            "sha256": "3951eaa7d91dc8627e6635df7ef15be59cdcd7e17fde155e3942d9e577e3c715"
          },
          "active_profile": {
            "path": "production/batch94/assets/calamites/r001/profile-contract.json",
            "sha256": "3951eaa7d91dc8627e6635df7ef15be59cdcd7e17fde155e3942d9e577e3c715"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
            "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
            "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
              "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
            },
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/QA-MANIFEST.json",
              "sha256": "262106559a5f4c42a9c7e3a058518ee4c0d2599a26b38dbd0337c69b527d57c0"
            },
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/HANDOFF.json",
              "sha256": "aee1aaf8c42f21b884684c741bba25ffd176a1a4d6ac1681e301dd45cf246281"
            }
          ],
          "original_metrics": {
            "path": "production/batch94/assets/calamites/r001/metrics.json",
            "sha256": "1b92989d14627e634340c8f32584d6fe88cad7dfa0dd39b1a9cb44a33332bff3"
          },
          "source_counts": {
            "path": "production/batch94/assets/calamites/r001/final-measurement.json",
            "sha256": "8d403919f71a8d47be81c57d214c3e52d712c967aab2374b6b15aeb0eb392a69"
          },
          "proof": {
            "path": "production/batch94/assets/calamites/r001/proof-final/render-manifest.json",
            "sha256": "5f7c8fcfc43bf9e6ae10e57afd180e32e46d5cbc85d3f0becd869eeb30189740"
          },
          "source_preview": {
            "path": "production/batch94/assets/calamites/r001/preview.png",
            "sha256": "de791cd18414a5392ccb5a20cc4803a7ee356ebc2939321234e381ee6aa95a3e"
          },
          "capture_reference": {
            "path": "assets/additions/calamites/batch94-20261021/calamites.png",
            "sha256": "b8c824beb79ed33fc6de7a8756ba0147cbda9907f7ca6525052e94b8cc626620"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/calamites.json",
            "sha256": "81567d37ddaef590552d2e40d80ed558e60db34bfb3a9bad53139bb7202aeac1"
          }
        },
        {
          "id": "pseudobornia",
          "batch": 94,
          "revision": "r001",
          "candidate_root": "production/batch94/assets/pseudobornia/r001",
          "source_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "reviewed_source_commit": "b744a404a2d2d648adb44f633221d144f88f18ad",
          "original_source_snapshot": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "review_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/pseudobornia/batch94-20261021/release-metadata.json",
            "sha256": "900298c56b511b70f7158cda6bceb2b5439bc59947265d49c2b37ddb2924bd9d"
          },
          "candidate": {
            "path": "production/batch94/assets/pseudobornia/r001/candidate.json",
            "sha256": "8d6e18c62b42c283a62839fbb95c2423aa019983e674be1a344034e8960aa608"
          },
          "active_candidate": {
            "path": "production/batch94/assets/pseudobornia/r001/candidate.json",
            "sha256": "8d6e18c62b42c283a62839fbb95c2423aa019983e674be1a344034e8960aa608"
          },
          "original_profile": {
            "path": "production/batch94/assets/pseudobornia/r001/profile-contract.json",
            "sha256": "98a6dfa52ab99eb4b9e5e98bf391a22fa725c68e314ca818e24027f4d94f3df4"
          },
          "active_profile": {
            "path": "production/batch94/assets/pseudobornia/r001/profile-contract.json",
            "sha256": "98a6dfa52ab99eb4b9e5e98bf391a22fa725c68e314ca818e24027f4d94f3df4"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
            "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
            "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
              "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
            },
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/QA-MANIFEST.json",
              "sha256": "262106559a5f4c42a9c7e3a058518ee4c0d2599a26b38dbd0337c69b527d57c0"
            },
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/HANDOFF.json",
              "sha256": "aee1aaf8c42f21b884684c741bba25ffd176a1a4d6ac1681e301dd45cf246281"
            }
          ],
          "original_metrics": {
            "path": "production/batch94/assets/pseudobornia/r001/metrics.json",
            "sha256": "360724f0ee3db1ec3ba917355536b3dd3d94b6d84e4cdd4b7858f4bef680656c"
          },
          "source_counts": {
            "path": "production/batch94/assets/pseudobornia/r001/final-measurement.json",
            "sha256": "78b527b60980b136ebef513a2c1832aee09558c875028b525614bffd811feaee"
          },
          "proof": {
            "path": "production/batch94/assets/pseudobornia/r001/proof-final/render-manifest.json",
            "sha256": "2e8b6bdec131ff367a095771321a76e9c8cc77876f875b78b040091e9ecac6ae"
          },
          "source_preview": {
            "path": "production/batch94/assets/pseudobornia/r001/preview.png",
            "sha256": "196a507bd1aca18d4a5fc742f9bd1f4d97003e7de136ce9714576473d292a905"
          },
          "capture_reference": {
            "path": "assets/additions/pseudobornia/batch94-20261021/pseudobornia.png",
            "sha256": "4ff8d60b2edb4022540d0b7491650b64317539a9eff6261f119d01f56a913af1"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/pseudobornia.json",
            "sha256": "8977ac63fa04ce2c030c7c57741f5d925f55380effcc92326716a81b8f2aaa51"
          }
        },
        {
          "id": "rhacophyton",
          "batch": 94,
          "revision": "r002",
          "candidate_root": "production/batch94/assets/rhacophyton/r002",
          "source_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "reviewed_source_commit": "b744a404a2d2d648adb44f633221d144f88f18ad",
          "original_source_snapshot": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "review_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/rhacophyton/batch94-20261021/release-metadata.json",
            "sha256": "9364e8227f7ac0eb9d9ee8ec10c099404b29146d2317760f7092da093c9fa006"
          },
          "candidate": {
            "path": "production/batch94/assets/rhacophyton/r002/candidate.json",
            "sha256": "65ccbaf69254c41dbe41de3b4c7855172a30d780214de7b503953413bc317699"
          },
          "active_candidate": {
            "path": "production/batch94/assets/rhacophyton/r002/candidate.json",
            "sha256": "65ccbaf69254c41dbe41de3b4c7855172a30d780214de7b503953413bc317699"
          },
          "original_profile": {
            "path": "production/batch94/assets/rhacophyton/r002/profile-contract.json",
            "sha256": "dfc897035d6376f153ec5ce44a970be3a69ad8b5ab1750a0d7818dd64e0ef4a6"
          },
          "active_profile": {
            "path": "production/batch94/assets/rhacophyton/r002/profile-contract.json",
            "sha256": "dfc897035d6376f153ec5ce44a970be3a69ad8b5ab1750a0d7818dd64e0ef4a6"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
            "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
            "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
              "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
            },
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/QA-MANIFEST.json",
              "sha256": "262106559a5f4c42a9c7e3a058518ee4c0d2599a26b38dbd0337c69b527d57c0"
            },
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/HANDOFF.json",
              "sha256": "aee1aaf8c42f21b884684c741bba25ffd176a1a4d6ac1681e301dd45cf246281"
            }
          ],
          "original_metrics": {
            "path": "production/batch94/assets/rhacophyton/r002/metrics.json",
            "sha256": "b1b5216386b327e38a09e990e4108d99803829f5bbc2354c55897e01f2270614"
          },
          "source_counts": {
            "path": "production/batch94/assets/rhacophyton/r002/final-measurement.json",
            "sha256": "26c325a039fa4d56a8981a05386f66645efc53ce1a65d5f964365d82553427ec"
          },
          "proof": {
            "path": "production/batch94/assets/rhacophyton/r002/proof-final/render-manifest.json",
            "sha256": "ba644ff758fe9fcffa496b1167dc223d10aa9a5d4301d0604a73723868b561cf"
          },
          "source_preview": {
            "path": "production/batch94/assets/rhacophyton/r002/preview.png",
            "sha256": "ac6b2ddb0c393164656f5195ec6f0aa048456d4f4b73122ef16face5d05c2ef0"
          },
          "capture_reference": {
            "path": "assets/additions/rhacophyton/batch94-20261021/rhacophyton.png",
            "sha256": "03e4e66e9ea285c5b3b0ab9e86adff4cc59bec7c389140f723843f1dd6bae4ca"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/rhacophyton.json",
            "sha256": "9a553d91845b351bf75688d1b9cebcfde65c13d4748b8d5b4567170051588c0b"
          }
        },
        {
          "id": "sigillaria",
          "batch": 94,
          "revision": "r001",
          "candidate_root": "production/batch94/assets/sigillaria/r001",
          "source_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "reviewed_source_commit": "b744a404a2d2d648adb44f633221d144f88f18ad",
          "original_source_snapshot": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "review_commit": "ddc3ea7f58313e95f426b46f648dfd99b52927ab",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/sigillaria/batch94-20261021/release-metadata.json",
            "sha256": "c0d99a61dad78d68e38a1fb15403dc83bab9f2b65055dbfe5219e8c83d4229ec"
          },
          "candidate": {
            "path": "production/batch94/assets/sigillaria/r001/candidate.json",
            "sha256": "991913d279decd63840298c15655f548979f0cca5127d37c0203d32cb79e6291"
          },
          "active_candidate": {
            "path": "production/batch94/assets/sigillaria/r001/candidate.json",
            "sha256": "991913d279decd63840298c15655f548979f0cca5127d37c0203d32cb79e6291"
          },
          "original_profile": {
            "path": "production/batch94/assets/sigillaria/r001/profile-contract.json",
            "sha256": "547ec67a9077f6d40be8be9aafc1518c874f7b48e99e82faacfcadc125048495"
          },
          "active_profile": {
            "path": "production/batch94/assets/sigillaria/r001/profile-contract.json",
            "sha256": "547ec67a9077f6d40be8be9aafc1518c874f7b48e99e82faacfcadc125048495"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
            "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
            "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
              "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f"
            },
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/QA-MANIFEST.json",
              "sha256": "262106559a5f4c42a9c7e3a058518ee4c0d2599a26b38dbd0337c69b527d57c0"
            },
            {
              "path": "qa/continuous-small-life-round40-20261020/batch-94/HANDOFF.json",
              "sha256": "aee1aaf8c42f21b884684c741bba25ffd176a1a4d6ac1681e301dd45cf246281"
            }
          ],
          "original_metrics": {
            "path": "production/batch94/assets/sigillaria/r001/metrics.json",
            "sha256": "5deff7a4d7a9aab094e7e4c4b62b72c9672660ecf311e4c5a290e4f74dc058fd"
          },
          "source_counts": {
            "path": "production/batch94/assets/sigillaria/r001/final-measurement.json",
            "sha256": "f6c3f3e3a04ae4186a0d580f7e923a52405db6c8d6c36d4f36a34c089aac44d4"
          },
          "proof": {
            "path": "production/batch94/assets/sigillaria/r001/proof-final/render-manifest.json",
            "sha256": "a639b6d084660f767882ad200f0ce9306d9593b9ec2d724ab1952034210cf558"
          },
          "source_preview": {
            "path": "production/batch94/assets/sigillaria/r001/preview.png",
            "sha256": "875d6847ecacdd8b16105654e53d9fc0869e244e0fcbdf24bfb564b7807f0d68"
          },
          "capture_reference": {
            "path": "assets/additions/sigillaria/batch94-20261021/sigillaria.png",
            "sha256": "371b0d482a1e07febe18330133e4605d028ee22123cb5185961b004cc765dfc9"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/sigillaria.json",
            "sha256": "2b5175a4ba6fb223a28665e5e35c83f2f0f2bac597c90f215f2e811bca5e2061"
          }
        }
      ],
      "files": [
        {
          "path": "production/batch94/assets/calamites/r001/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/build-config.json",
          "sha256": "e94fe2617a11591fa5135c5e9cbfc91277d9d2d2069e84021ed5709a38fa00cd",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/build-dependencies.json",
          "sha256": "b116ae7a6a68d4baeebba0644a1ed4ac69c0412c5b3258f024b6118f1915cdb2",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/candidate-brief.json",
          "sha256": "4977a5d058a827eb6f2f45909d26a583cebc4bcd5f3965df97e3e907dbc8f740",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/candidate.json",
          "sha256": "b778145f5664350f1dd7f1a0862f298c6cb9200261ffb5db17b879534c707973",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/concept-original.png",
          "sha256": "c016f38b4e647e27c81e2237ce8bd3e4084483ba3aa91f4939b8a93114f91e25",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/concept-prompt.txt",
          "sha256": "fde0bb4fd87b21dbe4f042d3eaa346064fb8af62a7b710d30339cd2d384c4526",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/contact-sheet.png",
          "sha256": "677994709060cd53c0c2d4def18a353fe99183b796884a85f829e27694afa5db",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/diagnostic-lifecycle.jsonl",
          "sha256": "0f17915afdf773f642a07b41019bcfc459ef61b433f40d0a10cc7d26b1ed88c4",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/final-measurement.json",
          "sha256": "8d403919f71a8d47be81c57d214c3e52d712c967aab2374b6b15aeb0eb392a69",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/generator.py",
          "sha256": "1d9028140b1e906692318438ef825b9455d6755f17cb19a49695bed78fb82d91",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/gltf-validator.report.json",
          "sha256": "682394875b48b10081a3c864bd8a0fe87581f12e52387b319000c73b7889a95a",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/lifecycle.jsonl",
          "sha256": "5014ad56c6852440e7b5cf39b705f1952c8a98294ba327337808231d3961197f",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/maker-review.md",
          "sha256": "2d55da45ad7253af21dd7d8180c5bc98d3e85197a5b8563a3cded5daaddee988",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/metrics.json",
          "sha256": "1b92989d14627e634340c8f32584d6fe88cad7dfa0dd39b1a9cb44a33332bff3",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/model.glb",
          "sha256": "44fec258d990ba04a28211ecd8f0c6bfc25071e2a8fdadf7fc864507c9168238",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/pixel-inspection.json",
          "sha256": "ce1d57ead610e66387d78d81e34c25cf526395805401c05e96cb6b0f0e40ddcf",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/preproof-binding.json",
          "sha256": "dacda9daa77c07d68b70b33e9f2db425f617e3c8e33cbc5b0b55484c4f3eb46c",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/preview.png",
          "sha256": "de791cd18414a5392ccb5a20cc4803a7ee356ebc2939321234e381ee6aa95a3e",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/profile-contract.json",
          "sha256": "3951eaa7d91dc8627e6635df7ef15be59cdcd7e17fde155e3942d9e577e3c715",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/project-audit.json",
          "sha256": "dfcb847079a806fefb17d2fa0aeb45f27efcd04a86c6276a37dfe85782356361",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/proof-final/clay.png",
          "sha256": "23982d6df009d09f4d29417ed819d5d23fe13d476159a9a4725b27f983a901b9",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/proof-final/front.png",
          "sha256": "7904570586563caf6f474938d6a648f9668436f302129d7dcc097c3f6c0e39ca",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/proof-final/hero.png",
          "sha256": "de791cd18414a5392ccb5a20cc4803a7ee356ebc2939321234e381ee6aa95a3e",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/proof-final/rear.png",
          "sha256": "fa471bff59ccca18850fa966a78e0ba9968bed6478b2afeee5a96772fa79005c",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/proof-final/render-manifest.json",
          "sha256": "5f7c8fcfc43bf9e6ae10e57afd180e32e46d5cbc85d3f0becd869eeb30189740",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/proof-final/reversehero.png",
          "sha256": "d10ab5552191218daf9fb748ce811e09ee2878ceb49b6ed9f3aa935efbdecf69",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/proof-final/side.png",
          "sha256": "64fcb0cb40ecc3b63a5fa8cb08cf6d7ae065b8245c4be3d8191416bf41af93a8",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/proof-final/silhouette.png",
          "sha256": "ccce43256b82339783c81efdd18e3862728f40c88e722fea6140bc691fe8393c",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/proof-final/top.png",
          "sha256": "1a35397066b5128f4643b63e1cf7c954d23c74ca7a391738d94d702364ba1787",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/references.json",
          "sha256": "9d09bf4cfa5eed82c9c6e28576cd2b5b131b4766aeef2650d23a55f8037f14e5",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/repro-final-1.report.json",
          "sha256": "f506c43d6690bbade5b3356ad0f0009ec4930738b87c419a8a4909c2ee2371cd",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/repro-final-2.report.json",
          "sha256": "c3b82633e8fd8e8e1643b9001446ce08afeeb7db283efd552a580b98d33a1a69",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/runtime-parse.report.json",
          "sha256": "3b6960ca156cee58b2eb2f76b0c3e7de8ca21133112091c1dc9a5b56894701e7",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/source-final.report.json",
          "sha256": "51e24400f45302fbfbdc68b17d6ab1e4e70969430fe3535e9c8c58b42d36822b",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/source-metrics.json",
          "sha256": "8ed4d5ffe7830ed4b019b2cb05dd0d1571c2a09079a61ddbf3443226a466891f",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/calamites/r001/source.blend",
          "sha256": "b3e099291afb1f181bac0f4d712471e297686175e9a9f78aa9086adfb16f79b5",
          "origin": "source",
          "owner": "calamites"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/build-config.json",
          "sha256": "17e2b060bfa4a4d7e74e74b25cef97ed9d740d0956b1f903709f590efe19b374",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/build-dependencies.json",
          "sha256": "adae15157476fddde2bfcc667d68ffa394bb6bb469b19c45c4175f04dd46fe15",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/candidate-brief.json",
          "sha256": "a99d18d8c41932ddcfbf51246fe17f2a420b9051e527131a40c28c3ab56ad329",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/candidate.json",
          "sha256": "8d6e18c62b42c283a62839fbb95c2423aa019983e674be1a344034e8960aa608",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/concept-original.png",
          "sha256": "3a79b517b81507cb826397efdf6e44ea1423ac96d0bf789818a6fa1493c48753",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/concept-prompt.txt",
          "sha256": "9ffbbe2fd011f620c513927b6f7f94cae00e88cd0d43cd5c28b224142f09619b",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/contact-sheet.png",
          "sha256": "4e95c8924e44da7473d48bc6c11b5b97ef8a680972917ae1eba9a3affbb36adb",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/diagnostic-lifecycle.jsonl",
          "sha256": "4afa7d0f22587146a353112809c6b86bc2cf52d98fc6b8af5c0ce684d7c2cab3",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/final-measurement.json",
          "sha256": "78b527b60980b136ebef513a2c1832aee09558c875028b525614bffd811feaee",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/generator.py",
          "sha256": "1d9028140b1e906692318438ef825b9455d6755f17cb19a49695bed78fb82d91",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/gltf-validator.report.json",
          "sha256": "df85a8418af3960ab9ccc69f3867306f1f9777965428c9fea5a5199bade8e08a",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/lifecycle.jsonl",
          "sha256": "ec7ab4ea8f98ac3c96a2e70ce977dc33d6bd8df66b2af4edb974563f403b1f2a",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/maker-review.md",
          "sha256": "7b42631a21b145762cf73232f806d5b9bcca01372c5e63815bbc64426b3a7083",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/metrics.json",
          "sha256": "360724f0ee3db1ec3ba917355536b3dd3d94b6d84e4cdd4b7858f4bef680656c",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/model.glb",
          "sha256": "54c683a7e9a8efdcab16c49dc61a577a67e200122a043b00b357243fe5cb77e2",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/pixel-inspection.json",
          "sha256": "6ad8d3b5033b95f4108c742b3831758f8a1820297a570e1bda654068a44804ff",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/preproof-binding.json",
          "sha256": "67566a0bd1cb1f5a125defb108f0decf3f2cda36a8304b6b24b9ef472ac752ba",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/preview.png",
          "sha256": "196a507bd1aca18d4a5fc742f9bd1f4d97003e7de136ce9714576473d292a905",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/profile-contract.json",
          "sha256": "98a6dfa52ab99eb4b9e5e98bf391a22fa725c68e314ca818e24027f4d94f3df4",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/project-audit.json",
          "sha256": "c89fffcd5e241ef10efb14427e9f7518f98502cd55dc193180907d4b8f137851",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/proof-final/clay.png",
          "sha256": "b11a6045cb01a1e94856487590ade299e610bd03bad536189cc94ae9c73431a1",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/proof-final/front.png",
          "sha256": "9b246cf95745bd0a637b955fca84951f0faded61b9fb934f5a6b9510e90e16ef",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/proof-final/hero.png",
          "sha256": "196a507bd1aca18d4a5fc742f9bd1f4d97003e7de136ce9714576473d292a905",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/proof-final/rear.png",
          "sha256": "f7a123d08aa04fc0f89ef60d85924fbd63795aae9e03e4157c1069322521adee",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/proof-final/render-manifest.json",
          "sha256": "2e8b6bdec131ff367a095771321a76e9c8cc77876f875b78b040091e9ecac6ae",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/proof-final/reversehero.png",
          "sha256": "fc8b55d5c62e36e1fdf19a24621118d18ad088764ed402b9388ada9f23bdc296",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/proof-final/side.png",
          "sha256": "4bf463805d40c89de9a9f5dd7ede6a8c253ab28274b77054bceb6d289a9041dc",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/proof-final/silhouette.png",
          "sha256": "2b9b572930e969a13281df61b321c0ad6f14be425f682d6edcedd543dfe970dc",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/proof-final/top.png",
          "sha256": "d81aa3a53d1b129f4f630eb4cf4c0d913b87cbf6de9228ba949a32eaae0c82dd",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/references.json",
          "sha256": "b72255c11959f5fce5f8fd5887cc078e1b74f0b192694de5be67cf550eac6ee1",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/repro-final-1.report.json",
          "sha256": "33f2a725208ce46f432638fe1b554644af9f379bc277adb7ca3f8ca927648268",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/repro-final-2.report.json",
          "sha256": "b1f267f2c775e97eb0b8d378d7f4272df9d64df286ca241242d4a5516f7cf287",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/runtime-parse.report.json",
          "sha256": "5e0c7489a04487837c0c5d9db6882cd1b368e33d1324a9b33406d3ad52bc9559",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/source-final.report.json",
          "sha256": "5452867fb3001586e1bb57548c022d80537582e312c4ac96a383d5f96e98eebd",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/source-metrics.json",
          "sha256": "605d9cd943d2da0eb02f0be09ad6255f7b0321e8f92f7552c8f6e92c29952f89",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/pseudobornia/r001/source.blend",
          "sha256": "656c25cf6066dcb15d5e42263aae229db47d18549c5197c6579d41b4b8f50894",
          "origin": "source",
          "owner": "pseudobornia"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/build-config.json",
          "sha256": "184ed97b4d4f8389b31fb289405fe83077c064591368b9b9b1e4486b5b0df1b0",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/build-dependencies.json",
          "sha256": "0191324197bfe87e6553d3520549ff15f0efc2c6fa557efcd6659558e453fd60",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/candidate-brief.json",
          "sha256": "9d0f04d9aaf8fda3f17c8cb079d691d15d2168677cce98f52db3f074191e52fa",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/candidate.json",
          "sha256": "65ccbaf69254c41dbe41de3b4c7855172a30d780214de7b503953413bc317699",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/concept-original.png",
          "sha256": "0fb7f586aed08bcf2805a8b08a12676c60531ba0d2da7567ce60982203a78db0",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/concept-prompt.txt",
          "sha256": "07d8097fc16373cfb18ec509fbae59ec6c5028c510826d531e6746db6cf8089a",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/contact-sheet.png",
          "sha256": "911c09121ab996f45e44ff006a8782aec8e2b80e0262e8a959ac72f55c0f5b74",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/final-measurement.json",
          "sha256": "26c325a039fa4d56a8981a05386f66645efc53ce1a65d5f964365d82553427ec",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/generator.py",
          "sha256": "d2b2978ed6d30a342cb727bfae33c004863caa562da4ac492e8e24fd83bbfc91",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/gltf-validator.report.json",
          "sha256": "7d5244f99c9e6970bdd44df4962c3ea1b8d2d7de8425e3aaf2abb07322244787",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/lifecycle.jsonl",
          "sha256": "f192312d5b12d9a336ebf31d6aa08dec1c621675434fa4d5cdc874b2f99de904",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/maker-review.md",
          "sha256": "6c719ba8b4cd6d5c6b412118e011ff284af408de71a52afcf576e4b48b324834",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/metrics.json",
          "sha256": "b1b5216386b327e38a09e990e4108d99803829f5bbc2354c55897e01f2270614",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/model.glb",
          "sha256": "2ab7364eca2c8905a5f99e3344a6ef3c3f1956618a00ed9606dd3b4948c71273",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/pixel-inspection.json",
          "sha256": "7bfb106cc27c88cbb3dced62875416b65f1889346bae28b59e2cc2283a3ae1d9",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/preproof-binding.json",
          "sha256": "6253fc84b2d64167bbfdab2bf3317c4042895c022e7307187b89182165a8b1f1",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/preview.png",
          "sha256": "ac6b2ddb0c393164656f5195ec6f0aa048456d4f4b73122ef16face5d05c2ef0",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/profile-contract.json",
          "sha256": "dfc897035d6376f153ec5ce44a970be3a69ad8b5ab1750a0d7818dd64e0ef4a6",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/project-audit.json",
          "sha256": "4ce0d3cc18a2045d4d271408f51f904355c4d7cc5cd951438c7341a11c332bdd",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/proof-final/clay.png",
          "sha256": "969f549d778af5b0a47be69dfb14129b4981d65bce79929eae832be9e7f1f0c5",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/proof-final/front.png",
          "sha256": "3ecf26e6629733070403a1bea8c45bf453534de934a8417a39d83b0cb709d394",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/proof-final/hero.png",
          "sha256": "ac6b2ddb0c393164656f5195ec6f0aa048456d4f4b73122ef16face5d05c2ef0",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/proof-final/rear.png",
          "sha256": "97194ef23fdb53e96d7883de0052099237ca2c5a4ba679e631224ea4c0c21c7d",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/proof-final/render-manifest.json",
          "sha256": "ba644ff758fe9fcffa496b1167dc223d10aa9a5d4301d0604a73723868b561cf",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/proof-final/reversehero.png",
          "sha256": "ae30fc014db406bd4e5820eccffc663b7e63962961376b68d13732c87ca0a201",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/proof-final/side.png",
          "sha256": "bb9b1653d53425dbb2cdc052709114996742b78f7701de9e8ada3de4fb9024a8",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/proof-final/silhouette.png",
          "sha256": "ab6d91fda5111c1e405592b4837f15b3ea037d1e0a9948d3024c566e20b81141",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/proof-final/top.png",
          "sha256": "c079ecaca0783fbdacbeccf93d6849fe927c46c999d7356df83133bb45f65564",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/references.json",
          "sha256": "2afb566d16d363a29aed36bc826f087233faeaa6be1484148e0ec07d2c8e0be1",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/repro-final-1.report.json",
          "sha256": "7350ec905ea3190d8051ab3299b09b4dbe77911c96ea3ec2c40f351e847cb5d7",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/repro-final-2.report.json",
          "sha256": "7656357d3f0b82f43e8bb61e92b0ce662d6693612508a2f07d7b201c0077bd96",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/runtime-parse.report.json",
          "sha256": "76dcf71eae2a1ece71a01a2825fe6cc3c202954568cdc665506dcb9863c95842",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/source-final.report.json",
          "sha256": "414bfc6f079ccca9b953805abfc7389bf590af37156474174457996a023e8d1b",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/source-metrics.json",
          "sha256": "3c0d653f2594b962134a900861567ed411db3d9e9cdeb1a47cf4c729ef9c561b",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/rhacophyton/r002/source.blend",
          "sha256": "c7d1596e393c6946a53bded32d66be437f01012edd58aa96e121c950ca50687f",
          "origin": "source",
          "owner": "rhacophyton"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/build-config.json",
          "sha256": "6334878ad7750881f17a00c0941b17fad0beef4660dffa97d28787587950b3fb",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/build-dependencies.json",
          "sha256": "832a0832825161afba94c4e4199e94e621f8ff19ce96898974c2b2c8949db48d",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/candidate-brief.json",
          "sha256": "154bd16ac69627421209d227bd4745baa25ac4d4db6f5c50cd0ce0c65bc4d0df",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/candidate.json",
          "sha256": "991913d279decd63840298c15655f548979f0cca5127d37c0203d32cb79e6291",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/concept-original.png",
          "sha256": "80a5724ee76c6cd3aff1b4fd306a9f13a177c835c13f89fc247b15875957f67c",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/concept-prompt.txt",
          "sha256": "9fc0477d34848baeb9caef4c82009a7af00eb9c66a5e1c20af8d9baa5d749da0",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/contact-sheet.png",
          "sha256": "49092b2c0929fed071883e380783b9e6660eacc4384f4b2d65707de6227b4ee6",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/diagnostic-lifecycle.jsonl",
          "sha256": "8b88f274650df4ba4541bf0da43b6f163c6fb268d5edf8813ab460d3c4ee3459",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/final-measurement.json",
          "sha256": "f6c3f3e3a04ae4186a0d580f7e923a52405db6c8d6c36d4f36a34c089aac44d4",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/generator.py",
          "sha256": "1d9028140b1e906692318438ef825b9455d6755f17cb19a49695bed78fb82d91",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/gltf-validator.report.json",
          "sha256": "1a33a0589f759c62bcece246c366dac15c3d37a7459b9dafc2d5095d33fa9d3e",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/lifecycle.jsonl",
          "sha256": "88fcbc37eddc4f5f7e09eac5db2ec52cc645315b3c7c78029627cbb1e14b053f",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/maker-review.md",
          "sha256": "c5dc71fbbf10c45b2b148bd937aaac8d8f3f8ceb443a51dbab4954728b96b9fa",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/metrics.json",
          "sha256": "5deff7a4d7a9aab094e7e4c4b62b72c9672660ecf311e4c5a290e4f74dc058fd",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/model.glb",
          "sha256": "c0b7a2040741e5583d957efdd5b0244314a1611bf840965b5b84673e32847b20",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/pixel-inspection.json",
          "sha256": "b713741c5444b7494cd9b9c63dee4f5bf87d5ca9259f7fa5bf01448c1a3c1fe5",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/preproof-binding.json",
          "sha256": "59d9735dd7f025c73eb75ad4271d58e25d1e8177520b6d198383e259dd5b163c",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/preview.png",
          "sha256": "875d6847ecacdd8b16105654e53d9fc0869e244e0fcbdf24bfb564b7807f0d68",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/profile-contract.json",
          "sha256": "547ec67a9077f6d40be8be9aafc1518c874f7b48e99e82faacfcadc125048495",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/project-audit.json",
          "sha256": "f9612569c60238a92c0d997a14d76a2166772096490651c2d3d08b39ce9123d3",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/proof-final/clay.png",
          "sha256": "d17c4bf78bbfa8338ff22963e8b83f7c7fcd41f2114263356fb22655fab53209",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/proof-final/front.png",
          "sha256": "6e09586c8b5347e9c37fe1d3852e0e7ccf275d8022e2fdc1d611704aef12a5b3",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/proof-final/hero.png",
          "sha256": "875d6847ecacdd8b16105654e53d9fc0869e244e0fcbdf24bfb564b7807f0d68",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/proof-final/rear.png",
          "sha256": "cac2bf26f4c04df8e068b6f2c5dbaa827e3807605062d760cd7001c40df3b4f5",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/proof-final/render-manifest.json",
          "sha256": "a639b6d084660f767882ad200f0ce9306d9593b9ec2d724ab1952034210cf558",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/proof-final/reversehero.png",
          "sha256": "f4536ea51b8d0a9ddfe9be7a1eb871ae85fd55c6be4eabb727b0c68aff038eca",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/proof-final/side.png",
          "sha256": "9bc3502c16f45f827a45575d0d88e44e52b6930e19c6a4b40e629e4c350deb45",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/proof-final/silhouette.png",
          "sha256": "ba0427bdad2924fd835278f88999d1a10c44c30d9c94454a167445f7ab4a9b8a",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/proof-final/top.png",
          "sha256": "a6b012635db0afbf03322a63add2e49e08bbb22531e39b641fcb2522e061de94",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/references.json",
          "sha256": "919d890a19c0591520b929fe85ea4d2cc7f5fa7a5603e2ef1b88560c507785c1",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/repro-final-1.report.json",
          "sha256": "f8376252041a2c18d098b920d899ac248332a14edfcbc5f257ac8859711e70de",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/repro-final-2.report.json",
          "sha256": "efb536a79db01b973ba6635bddd1a2cf8959754682b19117685549aa177a8f35",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/runtime-parse.report.json",
          "sha256": "cfc3511da1d676cfbf28b6abe60a1f1c03d57eec9f83bde0430cb2f0ccaf2707",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/source-final.report.json",
          "sha256": "56c9700f2b304971f58c97d49679810a3134d5d7f5ca3fb706ce0698cba7824c",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/source-metrics.json",
          "sha256": "4336324583aafb843f723ff884fbb70cbfeb0dcb2b519d10ef01daf601c3c416",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/assets/sigillaria/r001/source.blend",
          "sha256": "16856d66a867728250045bf3f1e84684972db5dfda0b423644b83c1efa1e2e9c",
          "origin": "source",
          "owner": "sigillaria"
        },
        {
          "path": "production/batch94/publication-policy.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256",
          "origin": "source",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.json",
          "sha256": "7124261e1a665047493a69a1d06b539a4b2d07cb17537ea3091961229774b33f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/FINAL-REPORT.md",
          "sha256": "8b439001164c229c61b482eb965de21c7aef2962fff5b86c1f1b79af98ff76e5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/HANDOFF.json",
          "sha256": "aee1aaf8c42f21b884684c741bba25ffd176a1a4d6ac1681e301dd45cf246281",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/HANDOFF.md",
          "sha256": "422c41795c81565e66c95d4cddd67f669156141e11709949611612f521346849",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/QA-MANIFEST.json",
          "sha256": "262106559a5f4c42a9c7e3a058518ee4c0d2599a26b38dbd0337c69b527d57c0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/check-provenance.py",
          "sha256": "1408a52072396016bd879ee09dd7b11d8f348a7b7d832025cae2d4d12bbd8dad",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/independent-geometry-initial-syntax-failure.py",
          "sha256": "af8ded4c2328dc256ef013b7342495868fe3b789b90837206e841db94f310e9e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/independent-geometry.py",
          "sha256": "f1187e86392bc7b1bee9f3c3322499c7b7b8a7840b37e20e2202025939e264f0",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/independent-runtime-initial-package-export-failure.mjs",
          "sha256": "00f21a29eb9bf55a79a366763d9772d081fbae8aadc04a7dd24bdf1fe55ee7b2",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/independent-runtime.mjs",
          "sha256": "c9233ab7411ed08e75437659e5eab451300d31edd2b8e0fd7f3a9e5d4c6ae561",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/inspect-preserved-r001.py",
          "sha256": "ebb17166652aea9e88a490115f310aed758cdf0c942039649a46bb28dc36b744",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/run-details.py",
          "sha256": "1d4f4d793e4b2c1b88cf70d643b618c4dc03f00b3c01e26debaf2bc33bb3aa7e",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/run-independent.py",
          "sha256": "299f3262685e1dfb2a74535307ffee80abc5ee4d3c1e553f3f75c7817e0bb3f1",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round40-20261020/batch-94/write-report.py",
          "sha256": "03135476f6ed556e1012be86134b8caba3c57296c56d7c37f4c64e892308f6b6",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g21-release-20261021/process-archive-index.json",
          "sha256": "a70d8e303af87c3a28eeeb96978fb7e0faa08c0d33601778ed9e64d756cf132f",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  },
  {
    "descriptor": {
      "path": "assets/releases/next52-g22-20261021.json",
      "sha256": "20cc0915005d1fa0d10e1e8417f6f96726777bc73043d7ac95c9df535d0fcb3e"
    },
    "release": {
      "version": 1,
      "scope": "next52-g22-release-20261021",
      "authorization": "owner_authorized_fixed52_after_required_checks",
      "acceptance_scope": "independent_qa_accepted_stylized_prop",
      "formal_profile_acceptance": "BLOCKED",
      "hardware_gpu_verified": false,
      "target_scene_verified": false,
      "provider_generation_timestamp": "unknown",
      "source_commit": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
      "review_commit": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
      "publication_policy": {
        "path": "production/policies/qa-passed-batch-publication-20261018.json",
        "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
      },
      "source_bundle": {
        "path": "qa/next52-g22-release-20261021/source-bundle.json",
        "sha256": "f726159730218c917131f903abc531bfb8608b7f2283ecba8b28783150df8594"
      },
      "protected_source_inputs": [
        {
          "path": "production/policies/qa-passed-batch-publication-20261018.json",
          "sha256": "be9d5685f41b6737525aa149c105836b5071ae3502a8f80a758a91387c325256"
        },
        {
          "path": "scripts/asset_common.py",
          "sha256": "a2eecc54fc9b21cf9a9387916541af5e681e0eea03169ac77e924aa4e0f5a519"
        },
        {
          "path": "scripts/qa_glb.py",
          "sha256": "88a278ddd2d2c7c7fded439db85dc4ad046893a146f6b622838364bae7d1e098"
        }
      ],
      "independent_reviews": [
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-handoff.json",
          "sha256": "6cd21dcf979be98dd470260f33109c771c03143f37a477d5d3b9c7b7be553a49"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
          "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/own-manifest.json",
          "sha256": "429423de3dcee2fc6d69bc72536aa108fe47063e2e3189361d6e7368dbb53948"
        }
      ],
      "capture": {
        "report": {
          "path": "qa/fifty-two-website-release-20261021/capture/render-report.json",
          "sha256": "7a4dd79a333cde8c85247d766cbece0283368ed58538e087fd2745788acff6f7"
        },
        "index": {
          "path": "qa/fifty-two-website-release-20261021/capture/card-index.json",
          "sha256": "428e02f49a3e1f7a365e36a2df1e8303be5db86446b8fc5c3a9aa4dae76c104f"
        },
        "artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/artifact-verification.json",
          "sha256": "2331174af34d46228f10f64a97c21fc5c9bd60c0b9d9ea8f18a4c4e932bdcc73"
        },
        "independent_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/independent-card-review.json",
          "sha256": "44df62beec02610e4b2f919d10fd0230e1296e484fbb4890242c536dfb7acd86"
        },
        "reviewer_evidence": {
          "path": "qa/fifty-two-website-release-20261021/capture/reviewer-evidence-pin.json",
          "sha256": "12f9578268cdcb28a714536319849cbc041ccfd7a9c44c9f1641289699bef0e0"
        },
        "review_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/review-inputs.json",
          "sha256": "ac8680fc2c5348ebda8079c4d53e24b5d7ac4d2e2cb7c187461ca5cc611f2e3b"
        },
        "original_inputs": {
          "path": "qa/fifty-two-website-release-20261021/capture/original-inputs.json",
          "sha256": "69c2a0fe8c38615fd049e29b07b3fe6f07112f1809e5db3cd1b256e4e5837fce"
        },
        "original_fixed52": {
          "path": "qa/fifty-two-website-release-20261021/source/original-fixed52-input.json",
          "sha256": "01ed697e60c782b6c8c2d2b25e9d659f640ebe57b33c5713b5aec5a974a3d8ac"
        },
        "source_identity_mapping": {
          "path": "qa/fifty-two-website-release-20261021/source/identity-successors.json",
          "sha256": "7da24de353fe152f5773b3f901fecf1e6d231505415b63460360f2e268098f51"
        },
        "profile_policy_aliases": {
          "path": "qa/fifty-two-website-release-20261021/source/profile-policy-aliases.json",
          "sha256": "c49cddd67aeb0d18b44b8eba4e1d3fd47c98078c565c7311c8f745c0a301eeae"
        },
        "historical_concepts": {
          "path": "qa/fifty-two-website-release-20261021/source/historical-concept-identities.json",
          "sha256": "d11a9537388b2abe339774f3e26b546437b8ef58d6416f9710c7df2158db9cd8"
        },
        "release_coordination_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/release-coordination-profile-audit.json",
          "sha256": "61fd160ab90dab58b7fb1c55086d9cd4c2b432654363b2a488616505cea8fabd"
        },
        "native_current_profiles": {
          "path": "qa/fifty-two-website-release-20261021/source/native-current-profile-validation.json",
          "sha256": "48977c10ddc5636c7ac782843617e7847af512523415c7fc1e0475764b18f5c1"
        },
        "final_gallery_status": "ACTUAL_FINAL_SUBJECT_CAPTURE_AND_INDEPENDENT104_PNG_REVIEW_PASSED_BOUNDED_ONLY",
        "final_gallery_receipt": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-receipt.json",
          "sha256": "dca5c912d683210e3f4be085e53e9047f6c1fe0b939d0af0724aaf06b6b28b44"
        },
        "final_gallery_review": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-independent-review.json",
          "sha256": "956d17934f6678ae7ed9a105485da663ceb0bd2ae8d9b9a315f5f1bf25f00128"
        },
        "final_gallery_artifact_verification": {
          "path": "qa/fifty-two-website-release-20261021/capture/final-gallery-artifact-verification.json",
          "sha256": "b63ce5cb928dc7a7f38d0adedfb9d06de7402c41ff7d92d833fb8345c0bc3f41"
        }
      },
      "excluded_ids": [
        "braided-river-reach",
        "crevasse-splay",
        "kettle-basin"
      ],
      "additions": [
        {
          "id": "lumbricaria-thread-like-coprolite",
          "batch": 90,
          "revision": "r001",
          "candidate_root": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001",
          "source_commit": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
          "reviewed_source_commit": "625b5f2cdd97623e216874fd981958852a3a910d",
          "original_source_snapshot": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
          "review_commit": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/lumbricaria-thread-like-coprolite/batch90-20261021/release-metadata.json",
            "sha256": "d1acc6737c70eb2e3f85e594d97618e9899cd2ffbbfa2f7a674fdac5f0f90120"
          },
          "candidate": {
            "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/candidate.json",
            "sha256": "00f5caec92444216c033c4504b867eebf1c79e1f6fff5e265505fb2758087353"
          },
          "active_candidate": {
            "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/candidate.json",
            "sha256": "00f5caec92444216c033c4504b867eebf1c79e1f6fff5e265505fb2758087353"
          },
          "original_profile": {
            "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/profile-contract.json",
            "sha256": "fb7c30b9507642a45b95a904548120f219a8e978df9f305368ff43c5fb647e8d"
          },
          "active_profile": {
            "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/profile-contract.json",
            "sha256": "fb7c30b9507642a45b95a904548120f219a8e978df9f305368ff43c5fb647e8d"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
            "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
            "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
              "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-90/own-manifest.json",
              "sha256": "429423de3dcee2fc6d69bc72536aa108fe47063e2e3189361d6e7368dbb53948"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-handoff.json",
              "sha256": "6cd21dcf979be98dd470260f33109c771c03143f37a477d5d3b9c7b7be553a49"
            }
          ],
          "original_metrics": {
            "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/metrics.json",
            "sha256": "8541792c1265875a0f05d0bec91afc5b10857ab982653d3da14c2a271d25e36b"
          },
          "source_counts": {
            "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/source-vertex-counts.json",
            "sha256": "1a84ee862f6a8b66243f30d230648977b54a58be4bbf5db46830dc294de70d16"
          },
          "proof": {
            "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/render-manifest.json",
            "sha256": "b14bb952842f3aecabe9c95592886322e1f7c97ad7f22c1ae692fe88a16983cf"
          },
          "source_preview": {
            "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/preview.png",
            "sha256": "fc735ee235b655976f400afc40c66575e03b0c51683cacaf7e2ee7c5e4f0fda0"
          },
          "capture_reference": {
            "path": "assets/additions/lumbricaria-thread-like-coprolite/batch90-20261021/lumbricaria-thread-like-coprolite.png",
            "sha256": "35010df230360290074b0969efc80b01dbd5ace6d6bb7621d414e64e8269b193"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/lumbricaria-thread-like-coprolite.json",
            "sha256": "8f49c6dc1114f71fdcb557f7986904b08e89e71f66cd781db890e16815144bd8"
          }
        },
        {
          "id": "pertica",
          "batch": 90,
          "revision": "r003",
          "candidate_root": "production/batch90/assets/pertica/r003",
          "source_commit": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
          "reviewed_source_commit": "625b5f2cdd97623e216874fd981958852a3a910d",
          "original_source_snapshot": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
          "review_commit": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/pertica/batch90-20261021/release-metadata.json",
            "sha256": "5cc002d580d9af40e7baac39fa7040feeb51ffdcb88ed667a2af29cb96becb19"
          },
          "candidate": {
            "path": "production/batch90/assets/pertica/r003/candidate.json",
            "sha256": "3931a65f3961e851dafd276eabad50af80424095996a0d005c95e4a19f2fe36f"
          },
          "active_candidate": {
            "path": "production/batch90/assets/pertica/r003/candidate.json",
            "sha256": "3931a65f3961e851dafd276eabad50af80424095996a0d005c95e4a19f2fe36f"
          },
          "original_profile": {
            "path": "production/batch90/assets/pertica/r003/profile-contract.json",
            "sha256": "83e05098c669390ff61b56de00f42faa2f2898ef7b3bdcef9a9cc04ec6a9467f"
          },
          "active_profile": {
            "path": "production/batch90/assets/pertica/r003/profile-contract.json",
            "sha256": "83e05098c669390ff61b56de00f42faa2f2898ef7b3bdcef9a9cc04ec6a9467f"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
            "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
            "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
              "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-90/own-manifest.json",
              "sha256": "429423de3dcee2fc6d69bc72536aa108fe47063e2e3189361d6e7368dbb53948"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-handoff.json",
              "sha256": "6cd21dcf979be98dd470260f33109c771c03143f37a477d5d3b9c7b7be553a49"
            }
          ],
          "original_metrics": {
            "path": "production/batch90/assets/pertica/r003/metrics.json",
            "sha256": "10e40b1276896bf754a86327ed32200fb71365949159445fb8408f2b4e5b9e91"
          },
          "source_counts": {
            "path": "production/batch90/assets/pertica/r003/source-vertex-counts.json",
            "sha256": "bd826c6fa8a188d6bd294da7bddd3f3a7dd7939ab560458452f8af8a2607b6b6"
          },
          "proof": {
            "path": "production/batch90/assets/pertica/r003/proof-final/render-manifest.json",
            "sha256": "b33af49ea961b81d025806182e56fe6ae99d19ed6032f17ef56e198598e6d71c"
          },
          "source_preview": {
            "path": "production/batch90/assets/pertica/r003/preview.png",
            "sha256": "c3582b3da1a6bf04752d05ebc7ee6ff1418ef019a1d2a13f05d7580e976cf086"
          },
          "capture_reference": {
            "path": "assets/additions/pertica/batch90-20261021/pertica.png",
            "sha256": "7305492d88ea83511a893b1473588fd14d5ba6a8766233dc7e05df30d1c7b0c4"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/pertica.json",
            "sha256": "26c24c056258191acbf7664b98b0176f26e434073c9973604037ef8959ebde0d"
          }
        },
        {
          "id": "zoophycos-spiral-spreite",
          "batch": 90,
          "revision": "r002",
          "candidate_root": "production/batch90/assets/zoophycos-spiral-spreite/r002",
          "source_commit": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
          "reviewed_source_commit": "625b5f2cdd97623e216874fd981958852a3a910d",
          "original_source_snapshot": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
          "review_commit": "ee1eaa334f5e56a2716f30edb125e01cf193da6f",
          "accepted_disposition": "ACCEPT BOUNDED",
          "metadata": {
            "path": "assets/additions/zoophycos-spiral-spreite/batch90-20261021/release-metadata.json",
            "sha256": "e350630b7a2fa4a2bf0f5c3c32d8fc26fbd0d5f2c63fe0e32507a47f2be6eb37"
          },
          "candidate": {
            "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/candidate.json",
            "sha256": "294765bc7890cae0571ccf23ff3e71943fe421ead8857d8d5e34f8a062c41980"
          },
          "active_candidate": {
            "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/candidate.json",
            "sha256": "294765bc7890cae0571ccf23ff3e71943fe421ead8857d8d5e34f8a062c41980"
          },
          "original_profile": {
            "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/profile-contract.json",
            "sha256": "de9f53304e0a2e81597cd1d5476093dd34efe7ee0bb8efee44517b3cc8c3d725"
          },
          "active_profile": {
            "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/profile-contract.json",
            "sha256": "de9f53304e0a2e81597cd1d5476093dd34efe7ee0bb8efee44517b3cc8c3d725"
          },
          "original_stage_statuses": {
            "technical": "unknown",
            "visual": "unknown",
            "factual": "unknown",
            "specification": "unknown",
            "runtime_parse": "unknown",
            "gpu": "unknown",
            "scene": "unknown"
          },
          "review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
            "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
          },
          "active_review": {
            "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
            "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
          },
          "required_qa_documents": [
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
              "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-90/own-manifest.json",
              "sha256": "429423de3dcee2fc6d69bc72536aa108fe47063e2e3189361d6e7368dbb53948"
            },
            {
              "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-handoff.json",
              "sha256": "6cd21dcf979be98dd470260f33109c771c03143f37a477d5d3b9c7b7be553a49"
            }
          ],
          "original_metrics": {
            "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/metrics.json",
            "sha256": "212016db94a46aca7f330b7ae3029a1207387a514b057e84a301c92c3fb01cf3"
          },
          "source_counts": {
            "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/source-vertex-counts.json",
            "sha256": "2377070026a25b1e84c78581d173d404c011bf42aa98cc10e10a7919c18565b3"
          },
          "proof": {
            "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/render-manifest.json",
            "sha256": "ba1378c19b3bbe063fd8d263d61a99514ae76c61293a8792ac2925439fcb6a34"
          },
          "source_preview": {
            "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/preview.png",
            "sha256": "6a375316829b7033d6bd2596ba5ba14f07ff5ec6fdc6efc06d7657575d1b2d88"
          },
          "capture_reference": {
            "path": "assets/additions/zoophycos-spiral-spreite/batch90-20261021/zoophycos-spiral-spreite.png",
            "sha256": "bbd43ad9494ef819294b77efa59b7851c24d1340aaef91b5483cd916595f6005"
          },
          "capture_input_metadata": {
            "path": "qa/fifty-two-website-release-20261021/capture/input-metadata/zoophycos-spiral-spreite.json",
            "sha256": "3c41c3d4c68e68dc8b1fc8cd9f097de5c3f006f4aa55b6d5eee9d9285e0b2a04"
          }
        }
      ],
      "files": [
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/build-config.json",
          "sha256": "6a242bb2c128b202549d4423f387f9f4d897894af33952e7f03e62d5a2925f2c",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/build-dependencies.json",
          "sha256": "844319cee39706cfc67a25811340492f164925572b97759974bc399402ffecda",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/candidate-brief.json",
          "sha256": "dc63489ccfe424b8813a43a676de091c19db9ca2304baced93f3f85edfc589f8",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/candidate.json",
          "sha256": "00f5caec92444216c033c4504b867eebf1c79e1f6fff5e265505fb2758087353",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/concept-original.png",
          "sha256": "3c6bae77db06a1cb75f91c62f84022683f6f96e5267533d685a5ced8f88c678b",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/concept-prompt.txt",
          "sha256": "6cc060a36aa5d35dc2eebed46b160c1889757c46412d9c1fa8f2f0a03eb6d7ff",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/contact-sheet.png",
          "sha256": "2e176447710adee9aedc6eb7d4e4e31c1a7413ff5e59a7252886c3c525414baa",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/generator.py",
          "sha256": "841b81b7f02da587e5293ab9ad38255fdd277875c0bf8d704cd28685d178f43c",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/gltf-validator.report.json",
          "sha256": "6b9bce0aa0c760504eb4d768bc81d067bd48468abf7d531baa340cd98c6157e9",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/lifecycle.jsonl",
          "sha256": "bb1494ae7a5927f2c6d34cea1279fca64230a0d2ce6ec31b8cc4cbc60f697802",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/maker-review.md",
          "sha256": "fe658eda41adc1c55a6327ce6cbeb5d73ef05768d1c35d3d16ab517497d85239",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/metrics.json",
          "sha256": "8541792c1265875a0f05d0bec91afc5b10857ab982653d3da14c2a271d25e36b",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/model.glb",
          "sha256": "5c473c15091b75f6c1bd82d10d9cd478e1877369e4fc5d101dcea5653144a76e",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/pixel-inspection.json",
          "sha256": "89bbc2448da0e6f1fd4e97c2c78c11b5f88006dbc79095d43ae15092f3472c14",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/preproof-binding.json",
          "sha256": "35bc91519eac0aed59afa8b4f31870ec497c7b5cfebfe85acf4ba49f554ad47a",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/preview.png",
          "sha256": "fc735ee235b655976f400afc40c66575e03b0c51683cacaf7e2ee7c5e4f0fda0",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/profile-contract.json",
          "sha256": "fb7c30b9507642a45b95a904548120f219a8e978df9f305368ff43c5fb647e8d",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/project-audit.json",
          "sha256": "a13d00805699b7c598ae3c2514b8ebdef9c35f611cf671687fd61828fe07dbe1",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/clay.png",
          "sha256": "ddd1ad843b389a54df7387941e0926314abbd7a12e81ebb121e5956cc1ba1f2c",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/front.png",
          "sha256": "1de5b036de11b912783c8228ff8980709a78541297f7fb14b1396306d7178a5f",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/hero.png",
          "sha256": "fc735ee235b655976f400afc40c66575e03b0c51683cacaf7e2ee7c5e4f0fda0",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/rear.png",
          "sha256": "c0993d88cdd21e775a51c99e049bcd58fc39343a563d093764b7efeffa4d590d",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/render-manifest.json",
          "sha256": "b14bb952842f3aecabe9c95592886322e1f7c97ad7f22c1ae692fe88a16983cf",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/reversehero.png",
          "sha256": "ad061592b4f4fdf47c4d3a3615c8a2f8e53dbb36e9199c6edfb4f524a9b349ff",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/side.png",
          "sha256": "76cefcd1b7703853153dd995c0d485177fce375463edeecaa18d42d25108846b",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/silhouette.png",
          "sha256": "4e82e99c918fe77b397661f8fb3c0acb8ebcf70cc74030b29fb4b81aeb1590d9",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/proof-final/top.png",
          "sha256": "aefeff0809c654f7f1c778eb9f88f434d25dd97e907d0a7076e4ca9eef835e61",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/qa.json",
          "sha256": "8bccfdb9d9638644baaaf7a14309e071f090c1a91042f91478c86401783b8883",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/references.json",
          "sha256": "6f083d71ab8b13e40a4a5163337cf295f63aab9314b85c2c5d7ca05c9e2d931d",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/repro-final-1.report.json",
          "sha256": "b6042189bb2cf400fe6ab1761bd496395eafcd9034ea27f847f9fad5f556aa3c",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/repro-final-2.report.json",
          "sha256": "0287c132953992a71b8fde05d140b12ed782da3d1c1aa0a7a0e32acd633d050c",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/runtime-parse.report.json",
          "sha256": "80e3a065d815e382667223be91ef04d2ae7a6b8339e4a946272c2ef4c06c95a4",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/source-final.report.json",
          "sha256": "8ed325ff275f0e29e2dfd9132040103ad6f646965e8ba75680f7e85f3339e302",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/source-metrics.json",
          "sha256": "768241377776a9b1a36ce56df11539e9e4207938e7c97a628cb578ef31ddbfad",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/source-vertex-counts.json",
          "sha256": "1a84ee862f6a8b66243f30d230648977b54a58be4bbf5db46830dc294de70d16",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/lumbricaria-thread-like-coprolite/r001/source.blend",
          "sha256": "ca3ffd846f58d6d91df19dd5b707ebfec79f9e61a7dd1cb3264ab6f58068df5a",
          "origin": "source",
          "owner": "lumbricaria-thread-like-coprolite"
        },
        {
          "path": "production/batch90/assets/pertica/r003/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/build-config.json",
          "sha256": "50d86874a524943bf92c7e80b2f3ad4086e23918d167642bbb9d5281d2f22973",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/build-dependencies.json",
          "sha256": "d1e3fc68cb0f2539911726dea513234bb0addc3a2f0b048b996e3545a39da7c8",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/candidate-brief.json",
          "sha256": "fb1522a02979fdd2b9c3f4169d1ab451d1465dbc86bb4b70ead69f2a9cdd51d8",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/candidate.json",
          "sha256": "3931a65f3961e851dafd276eabad50af80424095996a0d005c95e4a19f2fe36f",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/concept-original.png",
          "sha256": "4417d1b49d6020c1c85711d2162efafcaeb1dac94ebf2d036bb74df26e6d8a12",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/concept-prompt.txt",
          "sha256": "2c14f6ae87009634cd03a7049accefd01d88979c980fe7257cd4e5b8ea22c09e",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/contact-sheet.png",
          "sha256": "428849a5924b8ae41eedc9e2d93d565f50de8f7687287d742b34e4d3b6588090",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/generator.py",
          "sha256": "4e009c2cceefe71ba8469617a6e45d76306278931bad66514783e93da6de901e",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/gltf-validator.report.json",
          "sha256": "82b05da3b08f705ec13bf2939efbcd7a9d24dbdfba96b281859eb208fbe4b923",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/lifecycle.jsonl",
          "sha256": "e48467435e11203b08292545b8ad94191b86ae476990bfaad4201c3d924eaeb0",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/maker-review.md",
          "sha256": "25db2a5ff8788cbbf922fe4406a85641b07d7d147a36a044cff7ebee006c8f0c",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/metrics.json",
          "sha256": "10e40b1276896bf754a86327ed32200fb71365949159445fb8408f2b4e5b9e91",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/model.glb",
          "sha256": "70f0dbec0a276763480e7ceff2c28092f3e69e204fd9c02ca3bd3f02ad62b196",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/pixel-inspection.json",
          "sha256": "a4bc0cddf39b30710c3c6b3766ec1b26d4de47957582fbc5d4a406594dcb2e76",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/preproof-binding.json",
          "sha256": "679829169349c96497f9866d8b7fe763b6bba6074b6e8fea548d299c537d726d",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/preview.png",
          "sha256": "c3582b3da1a6bf04752d05ebc7ee6ff1418ef019a1d2a13f05d7580e976cf086",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/profile-contract.json",
          "sha256": "83e05098c669390ff61b56de00f42faa2f2898ef7b3bdcef9a9cc04ec6a9467f",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/project-audit.json",
          "sha256": "9a2e3669908075ab47a0bf1bbdde7a051e0aadad97f9957164e12fc5a3deb099",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/proof-final/clay.png",
          "sha256": "e9901088bf0cc1bd89f85b908ef97e77d4331a79e089d4d6244c04addbf4e91c",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/proof-final/front.png",
          "sha256": "1ab984ba6e245ff123725ce0b51ff80741bef0cb4d8eee5c856236c1e594f030",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/proof-final/hero.png",
          "sha256": "c3582b3da1a6bf04752d05ebc7ee6ff1418ef019a1d2a13f05d7580e976cf086",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/proof-final/rear.png",
          "sha256": "70c83ca1f4af540236991b473e54f7667d18c1a279e33b62f431b76a23df5a4a",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/proof-final/render-manifest.json",
          "sha256": "b33af49ea961b81d025806182e56fe6ae99d19ed6032f17ef56e198598e6d71c",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/proof-final/reversehero.png",
          "sha256": "1b8204080da762dfdd2cce00ed309f11b09e9de9e62223de26b12a0136c0fc3d",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/proof-final/side.png",
          "sha256": "4aa250ae1b6c9704d3c775004a4d4d85bb83cbcb4098cbb8b31804dfa0cb5f14",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/proof-final/silhouette.png",
          "sha256": "4cf2e601486abd5800819d05e09c9bc97c981484d5bea5191d12ae5807b4dd76",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/proof-final/top.png",
          "sha256": "4c930fff4015e50bc2d1d0cedab102cd90c64fa8d3aa28a52c2cafff3f9cbd1a",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/qa.json",
          "sha256": "d2aa68534020fd4c1e68da76937bed6ad61840e4c0034caa544616334c5c6cf6",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/references.json",
          "sha256": "6dc47a6e463af37d336d07ede5678f7007af13c25f33677dbb6beb1e1f0ce467",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/repro-final-1.report.json",
          "sha256": "f93dc88e66cb9a7339c3840cdfb2971a301f228053adf86f7dddbc18431e9792",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/repro-final-2.report.json",
          "sha256": "7709b12774b278a2bf320abbea2b4b057bd050046ffabb78ded57df075e8f958",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/runtime-parse.report.json",
          "sha256": "a89880f80ba1961d7ca493fb07ba85d0f566827f2f5466a290287e786dee0f84",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/source-final.report.json",
          "sha256": "16086be315bf6615acbd57e32377363179d669402ce0800852981da7b863507a",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/source-metrics.json",
          "sha256": "f5ddc97cdc49a9b358fc4157acdff934edd1e793b6ccdf98be76a8d40171a0a8",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/source-vertex-counts.json",
          "sha256": "bd826c6fa8a188d6bd294da7bddd3f3a7dd7939ab560458452f8af8a2607b6b6",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/pertica/r003/source.blend",
          "sha256": "2b9ca6771ea88fe8df2715915431526ccb8fdbc7f8b2004d115d117e33fae1c4",
          "origin": "source",
          "owner": "pertica"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/LICENSES.md",
          "sha256": "e6d8d260cf0dcf2a18450391fb9c451c521bc2a7eb9dea8e3c863317ea595fec",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/build-config.json",
          "sha256": "4cb36bda1c652dc9abafd0b9da1bf7cba2f7a1453b264fc5ddd6db609f4b6cd7",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/build-dependencies.json",
          "sha256": "d0ba85709f2beff982b3be964049ee6b4641eabe0561036ac91050dc45c27b2e",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/candidate-brief.json",
          "sha256": "aba8bd233586037abb8d8cbf3f68580ae26f192a0902f4bad7a2f39e149bad89",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/candidate.json",
          "sha256": "294765bc7890cae0571ccf23ff3e71943fe421ead8857d8d5e34f8a062c41980",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/concept-original.png",
          "sha256": "efba03db91ba25d64666d4cb2173af30bcbae9007b39c1ce70ab7c2bd34195f1",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/concept-prompt.txt",
          "sha256": "2dbf4516fe9a05f10387ab63e8e0e505c7534afbee07322f213e6e8da2f3f5c0",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/contact-sheet.png",
          "sha256": "4df756d0bbd25122062983e01aa6dabed013392454037c65d7f6613c4818d521",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/generator.py",
          "sha256": "3da45e42f0a84d7a066f246cd8ef0658c04c873466d66b7248822fc5bf9b9b1c",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/gltf-validator.report.json",
          "sha256": "459ff9917eaea81e53db711c01d0e9a420b07f8160e6569613804e75a5d20388",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/lifecycle.jsonl",
          "sha256": "bb06ada7f198b5eeadb075c94eb942d7059f64e06e8b39fdb0ab2e524a954c12",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/maker-review.md",
          "sha256": "7eb205e313b3af2cf60226ec7fc222a7bdf1cff30397e4674b526d071bb219cb",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/metrics.json",
          "sha256": "212016db94a46aca7f330b7ae3029a1207387a514b057e84a301c92c3fb01cf3",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/model.glb",
          "sha256": "c3819e278beb43ba6651a38bd6bcfe509ec7218d13b5bfd51c8d0f4090030e56",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/pixel-inspection.json",
          "sha256": "e6f21f9aee7dfb62f61dbf151f8ea6199528b118cc7cd9eee3e7d9b915bad555",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/preproof-binding.json",
          "sha256": "7e44277ea49b3485e33431322870aa347f549a87a46efee6708c210c10f17204",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/preview.png",
          "sha256": "6a375316829b7033d6bd2596ba5ba14f07ff5ec6fdc6efc06d7657575d1b2d88",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/profile-contract.json",
          "sha256": "de9f53304e0a2e81597cd1d5476093dd34efe7ee0bb8efee44517b3cc8c3d725",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/project-audit.json",
          "sha256": "73d167e789151f71da28ebe8948d3a46943d6611878d219c906c46940d548c1f",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/clay.png",
          "sha256": "fdaa6956efe7b30743359bd39495040a6765150148cdf886c021c887f7f01c53",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/front.png",
          "sha256": "54b47721e1da4fc5b9c1a9abc8f9df5ad3297c12882ded7031f93ad610ad9519",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/hero.png",
          "sha256": "6a375316829b7033d6bd2596ba5ba14f07ff5ec6fdc6efc06d7657575d1b2d88",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/rear.png",
          "sha256": "6e8c8eccd2d9928c0bb2f3b6da23f37766bdf1495e4513b908f0d8302a5ed006",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/render-manifest.json",
          "sha256": "ba1378c19b3bbe063fd8d263d61a99514ae76c61293a8792ac2925439fcb6a34",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/reversehero.png",
          "sha256": "235cd93f461c5a966e974d7baf0e03d3b5245a5f3b2a433130e0bb6ab3a63649",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/side.png",
          "sha256": "37d5a1e0972f9f07fbfbe784b3c15321e38fab471f13c8f823882d5236317afc",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/silhouette.png",
          "sha256": "cb6be6bd6f21f240ced6831efc3f57a8c66e12b5bc67527b4e7626b15c1c79a8",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/proof-final/top.png",
          "sha256": "b1dc1b6008e6e825c2c89afac0b63cf711c663f19effbb1a13919e02772cfff4",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/qa.json",
          "sha256": "80ba98d6a70380cb7e0c2accaa1a4d4d3d1bc2164234cadfcbf6b8c19eacb604",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/references.json",
          "sha256": "e452737ab50846bee3a03ca72c86fe3351508459d70540cb7bbb3721f672e358",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/repro-final-1.report.json",
          "sha256": "ee445bbad7841ea641fdfc0c3655b96b6073dd99d6565fe2f1fd8c129f142856",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/repro-final-2.report.json",
          "sha256": "a78233543b9bf740e4a442bfab7c69085eb69346496d8de14d3845c7cf5ee9b0",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/runtime-parse.report.json",
          "sha256": "89604c8b625526fd21b0f763387600e0256344ba040c6cbe6d580e13c533eaf5",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/source-final.report.json",
          "sha256": "88bd8453d69bad0a87905f9ff47a7525ac5c38a0fb58c334f01ac4a9674ad312",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/source-metrics.json",
          "sha256": "e4f31f1a9c3aebd537ded34e27b839aa590c10c25dfba7d925ded12ce3b50e8b",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/source-vertex-counts.json",
          "sha256": "2377070026a25b1e84c78581d173d404c011bf42aa98cc10e10a7919c18565b3",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "production/batch90/assets/zoophycos-spiral-spreite/r002/source.blend",
          "sha256": "277f7e959c3a5a40b54eab3719eef54cfd982969f925f1c97ea28529fc2c2dab",
          "origin": "source",
          "owner": "zoophycos-spiral-spreite"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/audit_provenance.py",
          "sha256": "0c79f80a6cb25d1e36256a214d3f07ebea7e8d922df47dfc031dfcb038e93880",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/diagnose_chamber_radius.py",
          "sha256": "9986ecc6bbc2f63e28bacba042a9bcdb26e1aa456acc212c585aa049628955d5",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/diagnose_cord_width.py",
          "sha256": "78ca26d0087129e0635bf150bb03f2dac3b0bc12a7e87c9aa2fe07e755b1c789",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-handoff.json",
          "sha256": "6cd21dcf979be98dd470260f33109c771c03143f37a477d5d3b9c7b7be553a49",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.json",
          "sha256": "da755e89f339e45cd88b0098da74e0bfaec326df6924825b8a6cea7494faa4cd",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/independent-review.md",
          "sha256": "83ca2c9dde4e0997698748156dabe237892b7c993fc4bd96b8a72100e911dee4",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/measure_glb_relief-attempt1.py",
          "sha256": "22cf42d9ad42c2c50f0f2b639c018c3a8621d4a8f0114e00154cf5def161b4d3",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/measure_glb_relief.py",
          "sha256": "970b1ed92d1447a0ce136710c166bac7763d83421782ac34371849d7751de3ae",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/own-manifest.json",
          "sha256": "429423de3dcee2fc6d69bc72536aa108fe47063e2e3189361d6e7368dbb53948",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/pin_chamber_tail.py",
          "sha256": "634eef36726d76a87e8e0e503bf5f0f484fb0dc2e71c69d9b4067021717623ea",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/reopen_measure.py",
          "sha256": "4a97784504a4578cd51a257c2cdc2105f450a12b7a713c613bb4ea0fc44d3682",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/run_sources.sh",
          "sha256": "912a05bd249c7534d053d8dd0963130ca93347cf0b7180cbb5a2d43fb238341f",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/runtime_checks.cjs",
          "sha256": "303897059e05a36a0e47dc9508d13c27d8ba0abc2d207ddc606fce35db56650d",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/continuous-small-life-round38-20261020/batch-90/write_review.py",
          "sha256": "7886f34588bb25e57cc2e4d6dc3baae8e646b02bc5cbb173e629997a46705904",
          "origin": "review",
          "owner": "$batch"
        },
        {
          "path": "qa/next52-g22-release-20261021/process-archive-index.json",
          "sha256": "d206223bbe6e3889a632df20512973049912fe103d8f875c9faa2497328661a7",
          "origin": "release",
          "owner": "$batch"
        }
      ]
    }
  }
];
