import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
import {readCaptureArchives,assertCaptureEntry} from './detail-capture-provenance.mjs';
const sha=b=>createHash('sha256').update(b).digest('hex'),source='a'.repeat(40),renderer='b'.repeat(64);
const entry={png:{sha256:'same-delivered-png'},capture:{native_frames:[{camera:{near:.005},sha256:'original-native'}],first_frame:{sha256:'original-repeat'}}};
const raw=Buffer.from('export default '+JSON.stringify({source_commit:source,renderer_input_sha256:renderer,presentations:{a:entry}})+';\n');
const receipt={run_id:1,source_commit:source,renderer_input_sha256:renderer,capture_index_sha256:sha(raw),capture_index_path:'qa/detail-presentation-evidence/captures/1/original-capture-index.js'};
const archives=await readCaptureArchives([receipt],async()=>raw);assertCaptureEntry(archives,receipt,'a',structuredClone(entry));
for(const mutate of [e=>e.capture.native_frames[0].camera.near=.01,e=>e.capture.native_frames[0].sha256='forged-native-with-new-png',e=>e.capture.first_frame.sha256='forged-repeat']){const e=structuredClone(entry);mutate(e);assert.throws(()=>assertCaptureEntry(archives,receipt,'a',e),/differs/);}
await assert.rejects(readCaptureArchives([receipt],async()=>Buffer.concat([raw,Buffer.from('\n')])),/index changed/);
await assert.rejects(readCaptureArchives([{...receipt,source_commit:'c'.repeat(40)}],async()=>raw),/source mismatch/);
await assert.rejects(readCaptureArchives([{...receipt,renderer_input_sha256:'d'.repeat(64)}],async()=>raw),/renderer mismatch/);
for(const run_id of [0,-1,1.5,'../../escape',Number.MAX_SAFE_INTEGER+1])await assert.rejects(readCaptureArchives([{...receipt,run_id}],async()=>{throw Error('must not read');}),/Positive/);
console.log('PASS 12 original-entry provenance/mutation cases; no production evidence modified');
