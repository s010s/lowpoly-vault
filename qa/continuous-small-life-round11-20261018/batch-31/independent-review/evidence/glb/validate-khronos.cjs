// SPDX-License-Identifier: MIT
// Re-run the repository-pinned Khronos validator without mutating candidate files.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const validator = require('gltf-validator');

async function main() {
  const [glbPath, outputPath] = process.argv.slice(2);
  if (!glbPath || !outputPath) throw new Error('Usage: node validate-khronos.cjs <glb> <output.json>');
  const bytes = fs.readFileSync(glbPath);
  const glbSha256 = crypto.createHash('sha256').update(bytes).digest('hex');
  const raw = await validator.validateBytes(new Uint8Array(bytes), {
    uri: path.basename(glbPath),
    maxIssues: 10000,
    severityOverrides: { ACCESSOR_INDEX_TRIANGLE_DEGENERATE: 0 },
    externalResourceFunction: async uri => {
      throw new Error(`Standalone GLB requested external resource: ${uri}`);
    },
  });
  const messages = raw.issues.messages || [];
  const report = {
    schema_version: 1,
    check: 'official-khronos-gltf-validator',
    status: raw.issues.numErrors === 0 && !raw.issues.truncated ? 'pass' : 'fail',
    glb_path: glbPath,
    glb_sha256: glbSha256,
    glb_bytes: bytes.length,
    validator_version: validator.version(),
    issues: {
      numErrors: raw.issues.numErrors,
      numWarnings: raw.issues.numWarnings,
      numInfos: raw.issues.numInfos,
      numHints: raw.issues.numHints,
      truncated: Boolean(raw.issues.truncated),
      messages,
    },
    method: 'Pinned gltf-validator validateBytes; external resource requests throw; 10000 issue cap.',
  };
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2) + '\n', { flag: 'wx' });
  process.stdout.write(`${report.status}: ${path.basename(glbPath)} ${glbSha256} errors=${raw.issues.numErrors} warnings=${raw.issues.numWarnings}\n`);
  if (report.status !== 'pass') process.exitCode = 1;
}

main().catch(error => { console.error(error); process.exitCode = 2; });
