/** Optional generic UI diagnostics. Batch-specific tasks have been retired. */
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
const tasks={gallery:'site/gallery-browser-test.mjs',hover:'site/hover-reveal-browser-test.mjs',scroll:'site/catalog-scroll-browser-test.mjs',modal:'site/modal-motion-browser-test.mjs',interaction:'site/interaction-motion-browser-test.mjs',handoff:'site/handoff-browser-test.mjs',models:'site/redesign-browser-test.mjs'};
const task=process.env.CI_REVIEW_TASK||process.argv[2]||'gallery';
assert(Object.hasOwn(tasks,task),'Use a generic UI task: '+Object.keys(tasks).join(', '));
const result=spawnSync(process.execPath,[tasks[task]],{stdio:'inherit'});assert.equal(result.status,0,'UI diagnostic failed');
