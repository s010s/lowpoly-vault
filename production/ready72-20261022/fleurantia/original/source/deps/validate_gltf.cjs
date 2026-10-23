#!/usr/bin/env node
// SPDX-License-Identifier: MIT
// Official Khronos validation; no network or external resource loading.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
let validator;
try { validator = require('gltf-validator'); }
catch { console.error('Missing official gltf-validator devDependency. Install the repository dependencies first.'); process.exit(2); }

function filesUnder(target) {
  const stat = fs.statSync(target);
  if (stat.isFile()) return target.toLowerCase().endsWith('.glb') ? [target] : [];
  return fs.readdirSync(target, {withFileTypes: true}).flatMap(entry => {
    const child = path.join(target, entry.name);
    return entry.isDirectory() ? filesUnder(child) : entry.isFile() && entry.name.toLowerCase().endsWith('.glb') ? [child] : [];
  });
}

async function validate(filename) {
  const bytes = fs.readFileSync(filename);
  const sha256 = crypto.createHash('sha256').update(bytes).digest('hex');
  const dir = path.dirname(filename);
  const qaPath = path.join(dir, 'qa.json');
  const reportPath = path.join(dir, 'gltf-validator.report.json');
  const qa = fs.existsSync(qaPath) ? JSON.parse(fs.readFileSync(qaPath, 'utf8')) : {};
  try {
    const report = await validator.validateBytes(new Uint8Array(bytes), {
      uri: path.basename(filename),
      maxIssues: 10000,
      severityOverrides: {ACCESSOR_INDEX_TRIANGLE_DEGENERATE: 0},
      externalResourceFunction: async uri => { throw new Error('Standalone GLB must not request external resource: ' + uri); }
    });
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n');
    const issues = report.issues;
    const messages = issues.messages || [];
    const errors = messages.filter(x => x.severity === 0);
    const warnings = messages.filter(x => x.severity === 1);
    qa.khronos_validator = {
      status: issues.numErrors ? 'fail' : issues.numWarnings ? 'pass_with_warnings' : 'pass',
      validator_version: validator.version(),
      sha256, errors, warnings,
      num_errors: issues.numErrors, num_warnings: issues.numWarnings,
      report: path.basename(reportPath), truncated: Boolean(issues.truncated)
    };
    if (issues.truncated) qa.khronos_validator.warnings.push('Issue report truncated; review full validation before acceptance.');
    fs.writeFileSync(qaPath, JSON.stringify(qa, null, 2) + '\n');
    console.log(`${qa.khronos_validator.status}: ${filename} (${issues.numErrors} errors, ${issues.numWarnings} warnings)`);
    return issues.numErrors === 0;
  } catch (error) {
    qa.khronos_validator = {status: 'fail', sha256, errors: [String(error)], warnings: []};
    fs.writeFileSync(qaPath, JSON.stringify(qa, null, 2) + '\n');
    console.error(`fail: ${filename}: ${error}`);
    return false;
  }
}

(async () => {
  const target = path.resolve(process.argv[2] || path.join(__dirname, '..', 'assets'));
  const files = filesUnder(target).sort();
  if (!files.length) throw new Error('No GLB files found at ' + target);
  let passed = true;
  for (const file of files) if (!await validate(file)) passed = false;
  process.exitCode = passed ? 0 : 1;
})().catch(error => { console.error(error); process.exitCode = 2; });
