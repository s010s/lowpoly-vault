import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { validateBytes, version } from 'gltf-validator/module.mjs';

const root = process.cwd();
const packageRoot = path.join(root, 'production/concept-small-fish-20261019');
const outputRoot = process.argv[2] ?? path.join(root, 'qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/khronos');
const ids = ['metaspriggina', 'falcatus', 'pteraspis', 'dorypterus'];
await fs.mkdir(outputRoot, { recursive: true });
const assets = [];

for (const id of ids) {
  const file = path.join(packageRoot, id, 'r001', 'output', `${id}.glb`);
  const bytes = await fs.readFile(file);
  const report = await validateBytes(new Uint8Array(bytes), { uri: `${id}.glb`, maxIssues: 0 });
  await fs.writeFile(path.join(outputRoot, `${id}.gltf-validator.json`), JSON.stringify(report, null, 2) + '\n');
  assets.push({
    asset_id: id,
    glb_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
    bytes: bytes.length,
    validator_version: version(),
    issues: report.issues,
  });
}

await fs.writeFile(path.join(outputRoot, 'summary.json'), JSON.stringify({ validator: 'Khronos glTF Validator', assets }, null, 2) + '\n');
console.log(JSON.stringify({ validator_version: version(), assets }, null, 2));
