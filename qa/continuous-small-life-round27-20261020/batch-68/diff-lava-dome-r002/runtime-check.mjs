import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import validator from 'gltf-validator';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { Box3, Vector3, REVISION } from 'three';

const glb = '/workspace/shared/lowpoly-batch68-20261020/assets/candidates/continuous-small-life-round27-20261020/batch-68/lava-dome/r002/model.glb';
const out = '/workspace/shared/lowpoly-round27-qa68/diff-lava-dome-r002/independent-runtime.json';
const bytes = fs.readFileSync(glb);
const sha = crypto.createHash('sha256').update(bytes).digest('hex');
const validation = await validator.validateBytes(new Uint8Array(bytes), {uri:path.basename(glb), format:'glb', writeTimestamp:false, maxIssues:0});
const buf = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
const parsed = await new GLTFLoader().parseAsync(buf, '');
parsed.scene.updateMatrixWorld(true);
let triangles = 0, meshes = 0, primitives = 0, materialIds = new Set();
parsed.scene.traverse(o => {
  if (o.isMesh) {
    meshes++;
    primitives++;
    triangles += (o.geometry.index?.count || o.geometry.attributes.position.count) / 3;
    for (const m of (Array.isArray(o.material) ? o.material : [o.material])) if (m) materialIds.add(m.uuid);
  }
});
const size = new Box3().setFromObject(parsed.scene).getSize(new Vector3()).toArray();
const report = {
  status: validation.issues.numErrors === 0 && validation.issues.numWarnings === 0 && REVISION === '180' ? 'pass' : 'review',
  glb_path: glb, glb_sha256: sha, bytes: bytes.length,
  khronos: {validator_version: validator.version(), errors: validation.issues.numErrors, warnings: validation.issues.numWarnings, infos: validation.issues.numInfos, hints: validation.issues.numHints, messages: validation.issues.messages},
  three: {revision: REVISION, parser:'Node GLTFLoader.parseAsync', status:'pass', triangles, mesh_count:meshes, primitive_count:primitives, material_count:materialIds.size, bounds_glb_xyz_m:size},
  gpu: 'not_run', scene: 'not_run',
  limitations: 'CPU parser and Khronos format checks only; no GPU, browser or composed-scene evidence.'
};
fs.writeFileSync(out, JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
