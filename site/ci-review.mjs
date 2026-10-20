/** Complete original acceptance probes, partitioned so independent browser suites run in parallel. */
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync,rmSync} from 'node:fs';
import {modelPlan,modelReceipt,verifyBuild} from './ci-model-shards.mjs';
import {computeModelInputs,freshModelRecords,assertBuiltRenderInputs} from './ci-model-proof.mjs';
import {freshCardPreviewRecords} from './ci-card-preview-proof.mjs';
const tasks = {
  "round13": {command:"node site/small-life-browser-test.mjs && node site/ci-scene-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round13-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round13-20261018/site"}},
  "round12": {command:"node site/small-life-browser-test.mjs && node site/ci-scene-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round12-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round12-20261018/site"}},
  "round06": {command:"node site/small-life-browser-test.mjs && node site/ci-scene-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round06-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round06-20261018/site"}},
  "round07": {command:"node site/small-life-browser-test.mjs && node site/ci-scene-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round07-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round07-20261018/site"}},
  "round08": {command:"node site/small-life-browser-test.mjs && node site/ci-scene-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round08-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round08-20261018/site"}},
  "round09": {command:"node site/small-life-browser-test.mjs && node site/ci-scene-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round09-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round09-20261018/site"}},
  "round10": {command:"node site/small-life-browser-test.mjs && node site/ci-scene-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round10-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round10-20261018/site"}},
  "round11": {command:"node site/small-life-browser-test.mjs && node site/ci-scene-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round11-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round11-20261018/site"}},
  "round05": {command:"node site/small-life-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round05-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round05-20261018/site"}},
  "round04": {command:"node site/small-life-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round04-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round04-20261018/site"}},
  "round03": {command:"node site/small-life-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round03-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round03-20261018/site"}},
  "hover": {command:"npm run test:hover:browser",env:{GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/release-hover-reveal"}},
  "round02": {command:"node site/small-life-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-round02-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-round02-20261018/site"}},
  "batch": {command:"node site/small-life-browser-test.mjs",env:{QA_ADDITION_PACK:"prehistoric-small-life-20261018",GALLERY_DIR:"dist",QA_OUTPUT_DIR:"qa/continuous-release-20261018/site"}},
  "scroll": {"command":"npm run test:scroll:browser","env":{"GALLERY_DIR":"dist","QA_OUTPUT_DIR":"qa/catalog-scroll"}},
  "fauna": {"command":"node site/small-life-browser-test.mjs","env":{"QA_ADDITION_PACK":"prehistoric-small-fauna","GALLERY_DIR":"dist","QA_OUTPUT_DIR":"qa/small-fauna-release-20261018/site"}},
  "matrix": {"command":"node site/redesign-browser-test.mjs","env":{"GALLERY_DIR":"dist","QA_OUTPUT_DIR":"qa/release-matrix","QA_REVIEW_SCOPE":"matrix"}},
  "previews": {
    "command": "node site/render-web-previews.mjs",
    "env": {
      "GALLERY_DIR": "dist",
      "PREVIEW_OUTPUT": "qa/web-capture-recheck",
      "VERIFY_SHIPPED_PREVIEWS": "1",
      "PREVIEW_POSTERS_ONLY": "1"
    }
  },
  "models": {
    "command": "node site/redesign-browser-test.mjs",
    "env": {
      "GALLERY_DIR": "dist",
      "QA_OUTPUT_DIR": "qa/release-strict-gpu",
      "QA_ALLOW_WEBGL_FALLBACK": "0"
    }
  },
  "small-life": {
    "command": "node site/small-life-browser-test.mjs",
    "env": {
      "GALLERY_DIR": "dist",
      "QA_OUTPUT_DIR": "qa/small-life-browser"
    }
  },
  "list": {
    "command": "npm run test:scrub:browser",
    "env": {
      "GALLERY_DIR": "dist",
      "QA_OUTPUT_DIR": "qa/shared-model-preview/list-browser"
    }
  },
  "shared": {
    "command": "npm run test:preview:browser",
    "env": {
      "GALLERY_DIR": "dist",
      "QA_OUTPUT_DIR": "qa/shared-model-preview/shared-browser"
    }
  },
  "handoff": {
    "command": "npm run test:handoff:browser",
    "env": {
      "GALLERY_DIR": "dist",
      "QA_OUTPUT_DIR": "qa/handoff-continuity"
    }
  },
  "conifer": {
    "command": "node qa/conifer-doc1-integration/conifer-handoff-browser-test.mjs",
    "env": {
      "GALLERY_DIR": "dist",
      "QA_OUTPUT_DIR": "qa/release-conifer-handoff"
    }
  },
  "modal": {
    "command": "npm run test:modal:browser",
    "env": {
      "GALLERY_DIR": "dist",
      "QA_OUTPUT_DIR": "qa/modal-motion"
    }
  },
  "interaction": {
    "command": "npm run test:interaction:browser",
    "env": {
      "GALLERY_DIR": "dist",
      "QA_OUTPUT_DIR": "qa/interaction-motion"
    }
  },
  "fallback": {
    "command": "node site/redesign-browser-test.mjs",
    "env": {
      "GALLERY_DIR": "dist",
      "QA_OUTPUT_DIR": "qa/release-fallback-only",
      "QA_ALLOW_WEBGL_FALLBACK": "1",
      "QA_FORCE_WEBGL_FALLBACK": "1"
    }
  }
};
const task = process.env.CI_REVIEW_TASK;
const modelShard=task?.startsWith('models-');
const cardProof=task==='previews'&&process.env.CI_MODEL_PROOF_ACTIVE==='true';
const manifest=modelShard?JSON.parse(readFileSync('assets/manifest.json')):null;
const plan=modelShard?modelPlan(manifest,{runtime:process.env.CI_MODEL_PROOF_ACTIVE!=='true'&&process.env.CI_RUNTIME==='true',ids:process.env.QA_MODEL_IDS||''}):null;
const shard=plan?.find(entry=>entry.task===task);
assert(modelShard?shard:Object.hasOwn(tasks,task), 'Known CI task required');
const {command,env} = tasks[modelShard?'models':task];
let build;
if(modelShard){
  rmSync(`qa/ci-model-shards/${task}.json`,{force:true});
  build=verifyBuild('dist');
  env.QA_REVIEW_SCOPE='models';
  env.QA_MODEL_IDS=shard.ids.join(',');
  env.QA_OUTPUT_DIR=`qa/release-strict-gpu/${task}`;
}
if(cardProof){
  rmSync('qa/ci-card-preview-proof/receipt.json',{force:true});
  rmSync('qa/web-capture-recheck/render-report.json',{force:true});
  assert(process.env.PREVIEW_ASSET_IDS,'Incremental card task requires a nonempty exact selection');
  build=verifyBuild('dist');
}
// Static/download integrity is always checked by Pages. Runtime changes cover all models.
if (task === 'models' || task === 'fallback') env.QA_REVIEW_SCOPE = task === 'models' ? 'models' : 'matrix';
if (task === 'fallback' && process.env.FULL_REVIEW === 'true') env.QA_REVIEW_SCOPE = 'full';
if (task === 'models' && process.env.CI_RUNTIME === 'true') env.QA_MODEL_IDS = '';
if (task === 'previews' && !cardProof && process.env.CI_RUNTIME === 'true') env.PREVIEW_ASSET_IDS = '';
const result = spawnSync(command, {shell:true,stdio:'inherit',env:{...process.env,...env}});
if (result.error) throw result.error;
if(modelShard&&result.status===0){
  const report=JSON.parse(readFileSync(`${env.QA_OUTPUT_DIR}/report.json`));
  const receipt=modelReceipt(manifest,plan,shard,report,build);
  if(process.env.CI_MODEL_PROOF_ACTIVE==='true')receipt.proof_records=freshModelRecords({inputs:computeModelInputs({built:await assertBuiltRenderInputs({})}),selectedIDs:shard.ids,browser:report,identity:build.identity,payload_sha256:build.payload_sha256});
  mkdirSync('qa/ci-model-shards',{recursive:true});
  writeFileSync(`qa/ci-model-shards/${task}.json`,JSON.stringify(receipt,null,2)+'\n');
}
if(cardProof&&result.status===0){
  const report=JSON.parse(readFileSync(`${env.PREVIEW_OUTPUT}/render-report.json`));
  const records=freshCardPreviewRecords({inputs:computeModelInputs({built:await assertBuiltRenderInputs({})}),selectedIDs:process.env.PREVIEW_ASSET_IDS.split(','),report,identity:build.identity,payload_sha256:build.payload_sha256});
  mkdirSync('qa/ci-card-preview-proof',{recursive:true});
  writeFileSync('qa/ci-card-preview-proof/receipt.json',JSON.stringify({version:1,kind:'card-preview-shard',identity:build.identity,payload_sha256:build.payload_sha256,records},null,2)+'\n');
}
process.exit(result.status ?? 1);
