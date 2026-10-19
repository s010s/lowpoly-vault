/** Geometry/matrix fixtures only: real texture decoding remains browser-parser coverage. */
import { readFile } from 'node:fs/promises';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export const repositoryURL = new URL('../../../', import.meta.url);
export const referencesURL = new URL('../../public/gallery/scale-reference/', import.meta.url);
export const assetURL = path => new URL(path, repositoryURL);
export async function publishedModels() {
  return JSON.parse(await readFile(new URL('assets/manifest.json', repositoryURL), 'utf8')).assets;
}
export function geometryOnlyLoader() {
  return new GLTFLoader().register(() => ({ name:'GeometryOnlyTextureFixture', loadTexture:() => Promise.resolve(new THREE.Texture()) }));
}
export async function parseGeometry(path) {
  const bytes = await readFile(path);
  return geometryOnlyLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength), '');
}
/** Intercept runtime-created loaders only inside this deterministic Node process. */
export function installGeometryOnlyTextureFixture() {
  const original = GLTFLoader.prototype.parse;
  const installed = Symbol('geometry-only-fixture');
  GLTFLoader.prototype.parse = function (...args) {
    if (!this[installed]) {
      this.register(() => ({ name:'GeometryOnlyTextureFixture', loadTexture:() => Promise.resolve(new THREE.Texture()) }));
      this[installed] = true;
    }
    return original.apply(this, args);
  };
  return () => { GLTFLoader.prototype.parse = original; };
}
