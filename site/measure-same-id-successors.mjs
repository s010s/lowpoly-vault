/** Read-only geometry parse of the frozen fourteen; emits new local evidence only.
 * No rendering, model mutation, source rebuild, world/GPU or publication acceptance.
 */
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {Box3, REVISION} from 'three';
import {MESH_SUCCESSOR_IDS} from './same-id-successors.mjs';
const [root, inputPath, output] = process.argv.slice(2); assert(root && inputPath && output, 'Usage: node site/measure-same-id-successors.mjs STAGING_ROOT staged-inputs.json NEW_OUTPUT_DIR');
assert.equal(REVISION, '180', 'The parser evidence is pinned to Three.js 0.180.0');
const input = JSON.parse(await readFile(inputPath)), rows = input.items || input.assets;
assert(Array.isArray(rows), 'Staged items array required');
assert.deepEqual(rows.map(row => row.id).sort(), [...MESH_SUCCESSOR_IDS].sort(), 'Exactly the frozen14 staged sources required');
globalThis.ProgressEvent ??= class { constructor(type, options = {}) { this.type = type; Object.assign(this, options); } };
const measurements = [];
await mkdir(output); // Refuse an existing output; do not overwrite evidence.
for (const row of rows) {
  const reference = row.glb || row.model || row.files?.glb || row.staged?.glb;
  assert(reference && typeof reference.path === 'string' && !reference.path.startsWith('/') && reference.path.split('/').every(part => part && part !== '.' && part !== '..'), 'Explicit staged GLB pin required');
  const raw = await readFile(resolve(root, reference.path)), sha = createHash('sha256').update(raw).digest('hex'); assert.equal(sha, reference.sha256);
  const loaded = await new Promise((accept, reject) => new GLTFLoader().parse(raw.buffer.slice(raw.byteOffset, raw.byteOffset + raw.byteLength), '', accept, reject));
  loaded.scene.updateMatrixWorld(true); const box = new Box3().setFromObject(loaded.scene), bounds = {min: box.min.toArray(), max: box.max.toArray(), size: box.max.clone().sub(box.min).toArray()};
  assert(bounds.size.every(value => Number.isFinite(value) && value > 0), 'Invalid parsed bounds');
  let meshes = 0, triangles = 0; const materials = new Set();
  loaded.scene.traverse(object => { if (object.isMesh) { meshes++; triangles += (object.geometry.index?.count || object.geometry.attributes.position.count) / 3; for (const material of Array.isArray(object.material) ? object.material : [object.material]) materials.add(material.uuid); } });
  assert(Number.isSafeInteger(triangles) && triangles > 0 && meshes > 0);
  const parser = {schema_version: 1, kind: 'same-id-current-parser-v1', asset_id: row.id, status: 'PASS', glb_sha256: sha, triangles, meshes, three_version: '0.180.0', errors: []};
  const path = `${row.id}/current-parser.json`, bytes = Buffer.from(JSON.stringify(parser, null, 2) + '\n'); await mkdir(resolve(output, row.id)); await writeFile(resolve(output, path), bytes, {flag: 'wx'});
  measurements.push({id: row.id, parser: {path, sha256: createHash('sha256').update(bytes).digest('hex'), bytes: bytes.length}, asset_patch: {triangles, dimensions: bounds.size, bounds_glb_m: bounds, primitives: meshes, material_count: materials.size}});
}
await writeFile(resolve(output, 'measurements.json'), JSON.stringify({kind: 'same-id-current-measurements-v1', measurements, status: 'CPU_PARSE_ONLY', publication_authorized: false, reviewer_authority: false, world_accepted: false, gpu_accepted: false}, null, 2) + '\n', {flag: 'wx'});
console.log(JSON.stringify({parsed: measurements.length, output, status: 'CPU_PARSE_ONLY'}));
