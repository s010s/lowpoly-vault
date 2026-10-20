import fs from 'node:fs';
import crypto from 'node:crypto';
import validator from '/workspace/shared/lowpoly-landair-web-integration/node_modules/gltf-validator/index.js';
for (const file of process.argv.slice(2)) {
  const bytes = fs.readFileSync(file);
  const sha256 = crypto.createHash('sha256').update(bytes).digest('hex');
  const r = await validator.validateBytes(new Uint8Array(bytes), {
    uri: file.split('/').at(-1), maxIssues: 10000,
    externalResourceFunction: async uri => { throw new Error('Unexpected external resource: '+uri); }
  });
  const messages = r.issues.messages ?? [];
  const out = {
    file, sha256, validator_version: validator.version(),
    num_errors: r.issues.numErrors, num_warnings: r.issues.numWarnings,
    messages, truncated: !!r.issues.truncated,
    status: r.issues.numErrors ? 'fail' : r.issues.numWarnings ? 'pass_with_warnings' : 'pass'
  };
  fs.writeFileSync('/workspace/shared/lowpoly-round25-qa65/technical/khronos-'+file.split('/').at(-3)+'.json',JSON.stringify(out,null,2)+'\n');
  console.log(JSON.stringify({file,sha256,status:out.status,num_errors:out.num_errors,num_warnings:out.num_warnings}));
}
