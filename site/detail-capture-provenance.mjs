/** Supplemental receipts bind complete original entries, not only delivered PNG hashes. */
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const sha=b=>createHash('sha256').update(b).digest('hex');
export async function readCaptureArchives(receipts,read=readFile){
 const archives=new Map();for(const receipt of receipts){
  assert(Number.isSafeInteger(receipt.run_id)&&receipt.run_id>0,'Positive capture run ID required');
  assert(/^[a-f0-9]{40}$/.test(receipt.source_commit),'Exact source commit required');
  assert(/^[a-f0-9]{64}$/.test(receipt.renderer_input_sha256)&&/^[a-f0-9]{64}$/.test(receipt.capture_index_sha256),'Exact capture seals required');
  assert.equal(receipt.capture_index_path,`qa/detail-presentation-evidence/captures/${receipt.run_id}/original-capture-index.js`);
  const raw=await read(receipt.capture_index_path);assert.equal(sha(raw),receipt.capture_index_sha256,'Original capture index changed');
  const text=raw.toString();assert(text.startsWith('export default '));const archived=JSON.parse(text.slice('export default '.length).trim().replace(/;$/,''));
  assert.equal(archived.source_commit,receipt.source_commit,'Archive source mismatch');assert.equal(archived.renderer_input_sha256,receipt.renderer_input_sha256,'Archive renderer mismatch');archives.set(receipt,archived);
 }return archives;
}
export function assertCaptureEntry(archives,receipt,id,entry){assert.deepEqual(entry,archives.get(receipt)?.presentations?.[id],'Current entry differs from original authenticated capture '+id);}
