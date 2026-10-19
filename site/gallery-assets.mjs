/** Validate the explicit gallery resource allowlist without selecting catalog assets. */
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile, readdir, realpath } from 'node:fs/promises';
import { resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const safePath = path => typeof path === 'string' && path.startsWith('gallery/') &&
  !/[\\\u0000-\u001f?#%]/.test(path) && !path.split('/').some(part => !part || part === '.' || part === '..');
const digest = value => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
// Seals the original approved poster pairs, wheel framing and scale companions.
// New deterministic captures extend resources.json without rewriting this baseline.
const REVIEWED_RESOURCES_SHA256 = '3a8a3d69f8c4069dbe1aa3e7a338f314638a1d142c10daf93207dde5c2c997a7';

async function verifiedFile(root, path) {
  assert(safePath(path), `Unsafe gallery resource path: ${path}`);
  const expected = resolve(root, path);
  assert(expected.startsWith(resolve(root) + sep), 'Gallery resource escapes the site root');
  assert.equal(await realpath(expected), expected, `Gallery symlinks are not allowed: ${path}`);
  return readFile(expected);
}

async function fileList(root, directory = 'gallery') {
  const files = [];
  for (const item of await readdir(resolve(root, directory), { withFileTypes: true })) {
    const path = `${directory}/${item.name}`;
    assert(!item.isSymbolicLink(), `Gallery symlinks are not allowed: ${path}`);
    if (item.isDirectory()) files.push(...await fileList(root, path));
    else { assert(item.isFile(), `Unsupported gallery resource: ${path}`); files.push(path); }
  }
  return files;
}

/** outputRoot optionally audits the final Vite-copied public resources too. */
export async function auditGalleryAssets(manifest, { root = process.cwd(), outputRoot, requireComplete = false } = {}) {
  assert(manifest && Array.isArray(manifest.assets) && !manifest.review_only, 'A published manifest is required');
  const publicRoot = resolve(root, 'site/public');
  const reviewedBytes = await verifiedFile(publicRoot, 'gallery/approved-resources.json');
  assert.equal(hash(reviewedBytes), REVIEWED_RESOURCES_SHA256, 'Approved gallery baseline changed');
  const reviewed = JSON.parse(reviewedBytes);
  const resourceRoot = outputRoot ? resolve(outputRoot) : publicRoot;
  const resources = JSON.parse(await verifiedFile(resourceRoot, 'gallery/resources.json'));
  assert.equal(resources.version, 1, 'Unsupported gallery resource version');
  assert(resources.posters && resources.references && Array.isArray(resources.files), 'Invalid gallery resources');
  for (const key of ['approved_site_commit', 'runtime_revision', 'source_renderer_sha256']) assert.equal(resources[key], reviewed[key], `Reviewed gallery provenance changed: ${key}`);
  assert.deepEqual(resources.references, reviewed.references, 'Reviewed scale references changed');
  for (const [id, poster] of Object.entries(reviewed.posters)) assert.deepEqual(resources.posters[id], poster, `Reviewed gallery poster or framing changed: ${id}`);
  const reviewedFiles = new Map(reviewed.files.map(file => [file.path, file]));
  reviewedFiles.set('gallery/approved-resources.json', {path:'gallery/approved-resources.json', sha256:REVIEWED_RESOURCES_SHA256, bytes:reviewedBytes.length});
  const allowedGeneratedFiles = new Set(Object.keys(resources.posters).filter(id => !Object.hasOwn(reviewed.posters, id)).flatMap(id => [`gallery/posters/${id}.png`, `gallery/posters/${id}-wheel.png`]));
  const published = new Map(manifest.assets.map(asset => [asset.id, asset]));
  assert.equal(published.size, manifest.assets.length, 'Duplicate published model IDs');
  const files = new Map();
  for (const file of resources.files) {
    assert(safePath(file.path) && !files.has(file.path), `Invalid or duplicate gallery file: ${file.path}`);
    assert(digest(file.sha256) && Number.isSafeInteger(file.bytes) && file.bytes > 0, 'Invalid gallery file seal');
    if (reviewedFiles.has(file.path)) assert.deepEqual(file, reviewedFiles.get(file.path), `Reviewed gallery file seal changed: ${file.path}`);
    else assert(allowedGeneratedFiles.has(file.path), `Unapproved additional gallery resource: ${file.path}`);
    const bytes = await verifiedFile(resourceRoot, file.path);
    assert.equal(bytes.length, file.bytes, `Gallery file size changed: ${file.path}`);
    assert.equal(hash(bytes), file.sha256, `Gallery file hash changed: ${file.path}`);
    files.set(file.path, file);
  }
  for (const path of reviewedFiles.keys()) assert(files.has(path), `Reviewed gallery resource omitted: ${path}`);
  const expectedFiles = ['gallery/resources.json', ...files.keys()].sort();
  assert.deepEqual((await fileList(resourceRoot)).sort(), expectedFiles, 'Unexpected gallery files must be explicitly reviewed');
  for (const path of Object.values(resources.references)) assert(files.has(path), `Unsealed scale reference: ${path}`);
  for (const [id, poster] of Object.entries(resources.posters)) {
    const asset = published.get(id);
    assert(asset, `Gallery poster must belong to a published model: ${id}`);
    assert(digest(poster.source_glb_sha256), `Invalid gallery source digest: ${id}`);
    assert.equal(poster.source_glb_sha256, asset.sha256?.glb, `Gallery poster source changed: ${id}`);
    assert(typeof asset.glb === 'string' && asset.glb.startsWith('assets/') && !/[\\\u0000-\u001f?#%]/.test(asset.glb) && !asset.glb.split('/').some(part => !part || part === '.' || part === '..'), `Unsafe GLB path: ${id}`);
    const modelPath = resolve(root, asset.glb);
    assert.equal(await realpath(modelPath), modelPath, `GLB symlinks are not allowed: ${id}`);
    assert.equal(hash(await readFile(modelPath)), poster.source_glb_sha256, `Gallery source GLB bytes changed: ${id}`);
    for (const kind of ['detail', 'wheel']) {
      assert.equal(poster[kind], `gallery/posters/${id}${kind === 'wheel' ? '-wheel' : ''}.png`, `Unexpected ${kind} poster path: ${id}`);
      assert(files.has(poster[kind]), `Unsealed ${kind} poster: ${id}`);
      const bytes = await verifiedFile(resourceRoot, poster[kind]);
      assert.equal(bytes.subarray(0, 8).toString('hex'), '89504e470d0a1a0a', `Invalid ${kind} PNG: ${id}`);
      assert.deepEqual([bytes.readUInt32BE(16), bytes.readUInt32BE(20)], kind === 'wheel' ? [768, 432] : [512, 512], `Invalid ${kind} dimensions: ${id}`);
      assert([4, 6].includes(bytes[25]), `Transparent ${kind} PNG required: ${id}`);
    }
    const spec = poster.wheelSpec;
    assert(spec && [spec.azimuth, spec.elevation, spec.zoom, spec.aspect].every(Number.isFinite) && spec.zoom > 0 && Math.abs(spec.aspect - 16 / 9) < 1e-9, `Invalid wheel camera: ${id}`);
    assert(Array.isArray(spec.offset) && spec.offset.length === 2 && spec.offset.every(Number.isFinite), `Invalid wheel offset: ${id}`);
    assert(Array.isArray(spec.floorCenter) && spec.floorCenter.length === 2 && spec.floorCenter.every(Number.isFinite), `Invalid wheel floor center: ${id}`);
    assert(Array.isArray(spec.floorPoints) && spec.floorPoints.length >= 3 && spec.floorPoints.every(point => Array.isArray(point) && point.length === 2 && point.every(Number.isFinite)), `Invalid wheel floor contour: ${id}`);
    assert(spec.projectedBounds && ['left', 'right', 'top', 'bottom'].every(key => Number.isFinite(spec.projectedBounds[key])), `Invalid wheel projected bounds: ${id}`);
  }
  const missing = manifest.assets.filter(asset => !Object.hasOwn(resources.posters, asset.id)).map(asset => asset.id);
  if (requireComplete) assert.equal(missing.length, 0, `Canonical gallery posters missing: ${missing.join(', ')}`);
  return { resources, coverage: { published: manifest.assets.length, matched: Object.keys(resources.posters).length, missing }, files: files.size, bytes: [...files.values()].reduce((sum, file) => sum + file.bytes, 0) };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const manifest = JSON.parse(await readFile('assets/manifest.json', 'utf8'));
  const result = await auditGalleryAssets(manifest, { requireComplete: process.argv.includes('--complete') || process.env.REQUIRE_COMPLETE_GALLERY === '1', outputRoot: process.argv.includes('--dist') ? process.env.GALLERY_OUTPUT_DIR || 'dist' : undefined });
  console.log(JSON.stringify({ files: result.files, bytes: result.bytes, coverage: result.coverage }, null, 2));
}
