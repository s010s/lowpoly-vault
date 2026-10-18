/** Complete original acceptance probes, partitioned so independent browser suites run in parallel. */
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
const tasks = {
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
assert(Object.hasOwn(tasks,task), 'Known CI task required');
const {command,env} = tasks[task];
// Static/download integrity is always checked by Pages. Runtime changes cover all models.
if (task === 'models' || task === 'fallback') env.QA_REVIEW_SCOPE = task === 'models' ? 'models' : 'matrix';
if (task === 'fallback' && process.env.FULL_REVIEW === 'true') env.QA_REVIEW_SCOPE = 'full';
if (task === 'models' && process.env.CI_RUNTIME === 'true') env.QA_MODEL_IDS = '';
if (task === 'previews' && process.env.CI_RUNTIME === 'true') env.PREVIEW_ASSET_IDS = '';
const result = spawnSync(command, {shell:true,stdio:'inherit',env:{...process.env,...env}});
if (result.error) throw result.error;
process.exit(result.status ?? 1);
