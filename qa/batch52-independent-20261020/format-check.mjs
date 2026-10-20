import {createHash} from 'node:crypto';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import validator from 'gltf-validator';

const root = resolve('.');
const output = resolve(root, process.env.QA_RUN_DIR || 'qa/batch52-independent-20261020/technical', 'technical');
await mkdir(output, {recursive: true});
const specs = [
  ['aturia', 'r002', '65f2c625334872f5e849d3bee11ff6085cc3245c93cb2cd86ba4baf13a74287b'],
  ['phoenicopsis', 'r001', '7e7fa939eeca8d1d0571ae1724faa7fa2387f03441bf0794fe4b269d666182d0'],
  ['cave-popcorn', 'r003', '36439f98c26784601b24ba4ac18c709f51c3ef9b071e0225438aaec42b7ba85b'],
  ['curvolithus-trilobed-trail', 'r001', 'c07529a8856b679af1a1d3e816c37046076488ee926f7e38e70241f0cbefed22'],
];
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const results = [];
for (const [id, revision, expectedHash] of specs) {
  const rel = 'assets/candidates/continuous-small-life-round18-20261020/batch-52/' + id + '/' + revision + '/' + id + '.glb';
  const bytes = await readFile(resolve(root, rel));
  const sha256 = digest(bytes);
  if (sha256 !== expectedHash) throw new Error(id + ': frozen GLB SHA mismatch');
  const report = await validator.validateBytes(new Uint8Array(bytes), {
    uri: rel,
    format: 'glb',
    maxIssues: 0,
    writeTimestamp: false,
  });
  const asset = {
    asset_id: id,
    revision,
    path: rel,
    sha256,
    bytes: bytes.length,
    validator_version: validator.version(),
    issues: report.issues,
    status: report.issues.numErrors === 0 && report.issues.numWarnings === 0 ? 'pass' : 'fail',
  };
  await writeFile(resolve(output, id + '-khronos.json'), JSON.stringify(asset, null, 2) + '\n');
  results.push(asset);
  console.log(JSON.stringify({asset_id: id, sha256, bytes: bytes.length, validator: asset.validator_version, errors: report.issues.numErrors, warnings: report.issues.numWarnings, status: asset.status}));
}
await writeFile(resolve(output, 'khronos-summary.json'), JSON.stringify({
  schema_version: 1,
  kind: 'independent_khronos_validation_summary',
  validator_version: validator.version(),
  results,
}, null, 2) + '\n');
if (results.some(item => item.status !== 'pass')) process.exitCode = 1;
