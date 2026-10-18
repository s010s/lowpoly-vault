// Independent QA helper: run official gltf-validator on frozen exact GLBs.
// Usage: node validate-khronos-batch01.cjs <report.json> <asset.glb>...
const fs = require('node:fs');
const crypto = require('node:crypto');
const validator = require('gltf-validator');

async function main() {
  const [reportPath, ...files] = process.argv.slice(2);
  if (!reportPath || files.length !== 4) throw new Error('Pass report path and four GLB files');
  const assets = [];
  for (const file of files) {
    const bytes = fs.readFileSync(file);
    const sha256 = crypto.createHash('sha256').update(bytes).digest('hex');
    const report = await validator.validateBytes(new Uint8Array(bytes), {
      uri: file.split('/').pop(),
      maxIssues: 10000,
      externalResourceFunction: async uri => { throw new Error(`Unexpected external resource: ${uri}`); },
    });
    const issues = report.issues;
    assets.push({
      file,
      bytes: bytes.length,
      sha256,
      validator_version: validator.version(),
      status: issues.numErrors ? 'FAIL' : issues.numWarnings ? 'PASS_WITH_WARNINGS' : 'PASS',
      numErrors: issues.numErrors,
      numWarnings: issues.numWarnings,
      messages: issues.messages,
    });
  }
  const result = { status: assets.every(x => x.status === 'PASS') ? 'PASS' : 'FAIL', assets };
  fs.writeFileSync(reportPath, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify(result, null, 2));
  if (result.status !== 'PASS') process.exitCode = 1;
}

main().catch(error => { console.error(error); process.exitCode = 2; });
