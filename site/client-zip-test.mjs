import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtemp, rm, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {crc32, buildStoreZip, assembleModelZip} from './client-zip.js';

// 1. IEEE 802.3 CRC-32 standard check vector ("123456789" === 0xCBF43926)
assert.equal(crc32(new TextEncoder().encode('123456789')), 0xcbf43926);
assert.equal(crc32(new Uint8Array(0)), 0x00000000);

// 2. Reject invalid / unsafe entry lists
assert.throws(() => buildStoreZip([]), /at least one entry/);
assert.throws(() => buildStoreZip([{name: '../escape.glb', data: new Uint8Array([1])}]), /Unsafe ZIP entry/);
assert.throws(() => buildStoreZip([{name: '/abs.glb', data: new Uint8Array([1])}]), /Invalid ZIP entry/);
assert.throws(() => buildStoreZip([{name: 'a.txt', data: '1'}, {name: 'a.txt', data: '2'}]), /Duplicate ZIP entry/);

// 3. Assemble a realistic model ZIP (binary GLB + binary blend + UTF-8 bilingual CREDITS.txt)
const glbPayload = new Uint8Array(1024);
for (let i = 0; i < glbPayload.length; i++) glbPayload[i] = (i * 37 + 11) & 0xff;
const blendPayload = new Uint8Array(768);
for (let i = 0; i < blendPayload.length; i++) blendPayload[i] = (i * 53 + 7) & 0xff;
const creditsText = 'Stylolite seam section\n缝合线构造剖面\nCreator: Leon Made This / s010s\nLicense: CC-BY-4.0\n';

const asset = {
  id: 'stylolite-seam-section',
  name: {en: 'Stylolite seam section', zh: '缝合线构造剖面'},
  glb: 'assets/additions/stylolite-seam-section/wave3/model.glb',
  blend: 'assets/additions/stylolite-seam-section/wave3/source.blend',
  downloads: {credits: 'assets/downloads/stylolite-seam-section-CREDITS.txt'},
};
const responses = new Map([
  ['https://example.test/' + asset.glb, glbPayload],
  ['https://example.test/' + asset.blend, blendPayload],
  ['https://example.test/' + asset.downloads.credits, new TextEncoder().encode(creditsText)],
]);
const {filename, bytes} = await assembleModelZip(asset, {
  resolveURL: p => 'https://example.test/' + p,
  fetchImpl: async url => {
    const body = responses.get(url);
    return body ? {ok: true, status: 200, arrayBuffer: async () => body.slice().buffer} : {ok: false, status: 404};
  },
});
assert.equal(filename, 'stylolite-seam-section.zip');
assert.equal(new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength).getUint32(0, true), 0x04034b50);

// 4. Independent Python stdlib zipfile CRC + structure + byte-for-byte extraction proof
const dir = await mkdtemp(join(tmpdir(), 'client-zip-'));
try {
  const zipPath = join(dir, filename);
  await writeFile(zipPath, bytes);
  const py = spawnSync('python3', ['-c', `
import json, sys, zipfile
with zipfile.ZipFile(sys.argv[1], 'r') as z:
    assert z.testzip() is None, 'CRC check failed'
    names = z.namelist()
    assert names == ['model.glb', 'source.blend', 'CREDITS.txt'], names
    for info in z.infolist():
        assert info.compress_type == zipfile.ZIP_STORED
    print(json.dumps({
        'glb_len': len(z.read('model.glb')),
        'blend_len': len(z.read('source.blend')),
        'credits': z.read('CREDITS.txt').decode('utf-8'),
        'glb_head': list(z.read('model.glb')[:8]),
        'blend_head': list(z.read('source.blend')[:8]),
    }))
`, zipPath], {encoding: 'utf8'});
  assert.equal(py.status, 0, py.stderr);
  const parsed = JSON.parse(py.stdout);
  assert.equal(parsed.glb_len, glbPayload.length);
  assert.equal(parsed.blend_len, blendPayload.length);
  assert.equal(parsed.credits, creditsText);
  assert.deepEqual(parsed.glb_head, [...glbPayload.slice(0, 8)]);
  assert.deepEqual(parsed.blend_head, [...blendPayload.slice(0, 8)]);

  // 5. Fallback credits when CREDITS.txt fetch fails (still valid ZIP)
  const fallbackRes = await assembleModelZip({...asset, downloads: {credits: 'assets/downloads/missing.txt'}}, {
    resolveURL: p => 'https://example.test/' + p,
    fetchImpl: async url => {
      const body = responses.get(url);
      return body ? {ok: true, status: 200, arrayBuffer: async () => body.slice().buffer} : {ok: false, status: 404};
    },
  });
  const fbPath = join(dir, 'fallback.zip');
  await writeFile(fbPath, fallbackRes.bytes);
  const py2 = spawnSync('python3', ['-c', `
import sys, zipfile
with zipfile.ZipFile(sys.argv[1], 'r') as z:
    assert z.testzip() is None
    assert 'CC-BY-4.0' in z.read('CREDITS.txt').decode('utf-8')
`, fbPath], {encoding: 'utf8'});
  assert.equal(py2.status, 0, py2.stderr);
} finally {
  await rm(dir, {recursive: true, force: true});
}
console.log('PASS client-zip: IEEE CRC-32 vector, STORE ZIP round-trip verified by Python zipfile.testzip(), UTF-8 credits, fallback credits, path safety');
