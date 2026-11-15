import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,rm,open,mkdir,symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {checkGlbSizes} from './glb-size-gate.mjs';
async function fixture(t,bytes){const root=await mkdtemp(join(tmpdir(),'glb-gate-'));t.after(()=>rm(root,{recursive:true,force:true}));const f=await open(join(root,'model.glb'),'w');await f.truncate(bytes);await f.close();return root;}
const manifest=(glb='model.glb')=>({assets:[{id:'test-model',glb,bytes:1}]});
for(const bytes of [1,4_999_999,5_000_000])test(`accept ${bytes} actual bytes`,async t=>{const root=await fixture(t,bytes);assert.equal((await checkGlbSizes(manifest(),{root})).models[0].bytes,bytes);});
test('reject 5,000,001 actual bytes despite metadata',async t=>{const root=await fixture(t,5_000_001);await assert.rejects(checkGlbSizes(manifest(),{root}),/test-model.*5000001 bytes exceeds 5000000 bytes by 1 bytes/);});
test('reject empty',async t=>{const root=await fixture(t,0);await assert.rejects(checkGlbSizes(manifest(),{root}),/nonempty regular file/);});
test('reject missing',async t=>{const root=await fixture(t,1);await assert.rejects(checkGlbSizes(manifest('absent.glb'),{root}),/absent.glb.*ENOENT/);});
test('reject directory',async t=>{const root=await fixture(t,1);await mkdir(join(root,'dir.glb'));await assert.rejects(checkGlbSizes(manifest('dir.glb'),{root}),/nonempty regular file/);});
test('reject unsafe paths',async t=>{const root=await fixture(t,1);for(const path of ['../model.glb','/model.glb','a\\model.glb','model.glb?x','model.blend'])await assert.rejects(checkGlbSizes(manifest(path),{root}),/unsafe or non-GLB/);});
test('reject symlink',async t=>{const root=await fixture(t,1);await symlink('model.glb',join(root,'link.glb'));await assert.rejects(checkGlbSizes(manifest('link.glb'),{root}),/symlink/);});
test('reject empty manifest and duplicate IDs',async t=>{const root=await fixture(t,1);await assert.rejects(checkGlbSizes({assets:[]},{root}),/nonempty assets/);await assert.rejects(checkGlbSizes({assets:[...manifest().assets,...manifest().assets]},{root}),/duplicate asset ID/);});
