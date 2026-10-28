/** Compatibility CLI. The one generic code-test selector replaces batch-specific suites. */
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
assert(['contracts','publication','pipeline'].includes(process.argv[2]));
const result=spawnSync(process.execPath,['site/ci-code-tests.mjs'],{stdio:'inherit'});assert.equal(result.status,0,'Code tests failed');
