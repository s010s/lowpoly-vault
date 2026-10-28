/** Compatibility CLI: no historical suite list, sharding or repeated model QA. */
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
const mode=process.argv[2];assert(process.argv.length===3&&['build','publication'].includes(mode),'Use build or publication; obsolete shard plans are not supported');
if(mode==='build'){const {buildSimple}=await import('./ci-build-simple.mjs');await buildSimple();}
else {const result=spawnSync(process.execPath,['site/unified-delivery-contract-test.mjs'],{stdio:'inherit'});assert.equal(result.status,0,'Delivery unit tests failed');}
