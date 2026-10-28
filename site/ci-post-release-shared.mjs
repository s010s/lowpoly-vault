/** Optional generic gallery diagnostic; automatic live readback uses ci-live-smoke.mjs. */
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
const result=spawnSync(process.execPath,['site/gallery-browser-test.mjs'],{stdio:'inherit'});
assert.equal(result.status,0,'Gallery diagnostic failed');
