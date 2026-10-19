import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const root = process.cwd();
const packageRoot = path.join(root, 'production/concept-small-fish-20261019');
const ids = ['metaspriggina', 'falcatus', 'pteraspis', 'dorypterus'];
const loader = new GLTFLoader();
const parse = buffer => new Promise((resolve, reject) => loader.parse(buffer, '', resolve, reject));
const assets = [];

for (const id of ids) {
  const file = path.join(packageRoot, id, 'r001', 'output', `${id}.glb`);
  const bytes = await fs.readFile(file);
  const arrayBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
  const gltf = await parse(arrayBuffer);
  gltf.scene.updateMatrixWorld(true);
  const bounds = new THREE.Box3().setFromObject(gltf.scene);
  const dimensions = new THREE.Vector3();
  bounds.getSize(dimensions);
  let meshCount = 0;
  let primitiveCount = 0;
  let triangles = 0;
  let positionCount = 0;
  const materials = new Map();
  gltf.scene.traverse(object => {
    if (!object.isMesh) return;
    meshCount++;
    primitiveCount += Array.isArray(object.material) ? object.material.length : 1;
    const geometry = object.geometry;
    const vertexCount = geometry.attributes.position?.count ?? 0;
    positionCount += vertexCount;
    triangles += (geometry.index?.count ?? vertexCount) / 3;
    for (const material of (Array.isArray(object.material) ? object.material : [object.material])) {
      if (material) materials.set(material.name, {
        baseColorLinear: material.color.toArray(),
        roughness: material.roughness,
        metallic: material.metalness,
        transparent: material.transparent,
        opacity: material.opacity,
        side: material.side,
      });
    }
  });
  assets.push({
    asset_id: id,
    glb_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
    bytes: bytes.length,
    loader: 'Three.js GLTFLoader',
    parse: 'pass',
    mesh_count: meshCount,
    primitive_count: primitiveCount,
    triangles,
    position_count: positionCount,
    bounds_xyz_m: { min: bounds.min.toArray(), max: bounds.max.toArray(), dimensions: dimensions.toArray() },
    material_count: materials.size,
    materials: Object.fromEntries(materials),
  });
}

console.log(JSON.stringify({ three_revision: THREE.REVISION, assets }, null, 2));
