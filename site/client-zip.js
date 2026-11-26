/** Zero-dependency browser STORE-mode ZIP builder for on-demand model bundles. */
const encoder = new TextEncoder();

const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    table[i] = c >>> 0;
  }
  return table;
})();

export function crc32(bytes) {
  const data = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes);
  let crc = 0xffffffff;
  for (let i = 0; i < data.length; i++) crc = CRC_TABLE[(crc ^ data[i]) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function safeEntryName(name) {
  if (typeof name !== 'string' || !name || name.startsWith('/') || /[\\\u0000-\u001f]/.test(name)) {
    throw new Error(`Invalid ZIP entry name: ${String(name)}`);
  }
  if (name.split('/').some(part => !part || part === '.' || part === '..')) {
    throw new Error(`Unsafe ZIP entry path: ${name}`);
  }
  return name;
}

// Fixed DOS timestamp: 2026-01-01 00:00:00 (matches server-side reproducible metadata).
const DOS_TIME = 0;
const DOS_DATE = ((2026 - 1980) << 9) | (1 << 5) | 1;
const UTF8_FLAG = 0x0800;

/**
 * Build a standard STORE-mode (uncompressed, method 0) ZIP archive.
 * GLB and compressed .blend files are already compressed, so STORE avoids CPU stalls.
 * @param {Array<{name: string, data: Uint8Array | ArrayBuffer | string}>} entries
 * @returns {Uint8Array}
 */
export function buildStoreZip(entries) {
  if (!Array.isArray(entries) || entries.length === 0) throw new Error('ZIP requires at least one entry.');
  const seen = new Set();
  const prepared = entries.map(entry => {
    const name = safeEntryName(entry?.name);
    if (seen.has(name)) throw new Error(`Duplicate ZIP entry: ${name}`);
    seen.add(name);
    const nameBytes = encoder.encode(name);
    const data = typeof entry.data === 'string'
      ? encoder.encode(entry.data)
      : entry.data instanceof Uint8Array
        ? entry.data
        : new Uint8Array(entry.data);
    return { nameBytes, data, crc: crc32(data) };
  });

  let localTotal = 0;
  let centralTotal = 0;
  for (const item of prepared) {
    localTotal += 30 + item.nameBytes.length + item.data.length;
    centralTotal += 46 + item.nameBytes.length;
  }
  const output = new Uint8Array(localTotal + centralTotal + 22);
  const view = new DataView(output.buffer);

  const offsets = [];
  let offset = 0;
  for (const item of prepared) {
    offsets.push(offset);
    view.setUint32(offset, 0x04034b50, true); // Local file header signature
    view.setUint16(offset + 4, 20, true); // Version needed to extract (2.0)
    view.setUint16(offset + 6, UTF8_FLAG, true); // General purpose bit flag (UTF-8)
    view.setUint16(offset + 8, 0, true); // Compression method: 0 (STORE)
    view.setUint16(offset + 10, DOS_TIME, true);
    view.setUint16(offset + 12, DOS_DATE, true);
    view.setUint32(offset + 14, item.crc, true);
    view.setUint32(offset + 18, item.data.length, true);
    view.setUint32(offset + 22, item.data.length, true);
    view.setUint16(offset + 26, item.nameBytes.length, true);
    view.setUint16(offset + 28, 0, true); // Extra field length
    output.set(item.nameBytes, offset + 30);
    offset += 30 + item.nameBytes.length;
    output.set(item.data, offset);
    offset += item.data.length;
  }

  const centralOffset = offset;
  for (let i = 0; i < prepared.length; i++) {
    const item = prepared[i];
    view.setUint32(offset, 0x02014b50, true); // Central directory file header signature
    view.setUint16(offset + 4, 20, true); // Version made by
    view.setUint16(offset + 6, 20, true); // Version needed
    view.setUint16(offset + 8, UTF8_FLAG, true);
    view.setUint16(offset + 10, 0, true); // STORE
    view.setUint16(offset + 12, DOS_TIME, true);
    view.setUint16(offset + 14, DOS_DATE, true);
    view.setUint32(offset + 16, item.crc, true);
    view.setUint32(offset + 20, item.data.length, true);
    view.setUint32(offset + 24, item.data.length, true);
    view.setUint16(offset + 28, item.nameBytes.length, true);
    view.setUint16(offset + 30, 0, true); // Extra length
    view.setUint16(offset + 32, 0, true); // Comment length
    view.setUint16(offset + 34, 0, true); // Disk number start
    view.setUint16(offset + 36, 0, true); // Internal attrs
    view.setUint32(offset + 38, 0, true); // External attrs
    view.setUint32(offset + 42, offsets[i], true); // Relative offset of local header
    output.set(item.nameBytes, offset + 46);
    offset += 46 + item.nameBytes.length;
  }

  view.setUint32(offset, 0x06054b50, true); // End of central directory signature
  view.setUint16(offset + 4, 0, true); // Disk number
  view.setUint16(offset + 6, 0, true); // Central dir start disk
  view.setUint16(offset + 8, prepared.length, true);
  view.setUint16(offset + 10, prepared.length, true);
  view.setUint32(offset + 12, centralTotal, true);
  view.setUint32(offset + 16, centralOffset, true);
  view.setUint16(offset + 20, 0, true); // Comment length
  return output;
}

function defaultCreditsText(asset) {
  const title = typeof asset?.name === 'string' ? asset.name : asset?.name?.en || asset?.id || 'Model';
  const titleZh = typeof asset?.name === 'object' ? asset?.name?.zh || '' : '';
  const author = asset?.author || 'Leon Made This / s010s';
  const license = asset?.license || 'CC-BY-4.0';
  const source = asset?.source_url || 'https://github.com/s010s/lowpoly-vault';
  const modelLink = asset?.id ? `https://s010s.github.io/lowpoly-vault/models/${asset.id}/` : source;
  return `${title}${titleZh && titleZh !== title ? `\n${titleZh}` : ''}\nCreator: ${author}\nModel: ${modelLink}\nSource: ${source}\nLicense: ${license}\nhttps://creativecommons.org/licenses/by/4.0/\nIndicate changes if modified.\n`;
}

export async function assembleModelZip(asset, { resolveURL, fetchImpl = globalThis.fetch?.bind(globalThis), fallbackCredits, signal } = {}) {
  if (!asset?.id || !asset?.glb || !asset?.blend) throw new Error('Model ZIP requires id, glb, and blend paths.');
  const checkAborted = () => {
    if (signal?.aborted) throw new DOMException('Cancelled', 'AbortError');
  };
  checkAborted();
  const toURL = typeof resolveURL === 'function' ? resolveURL : (p => p);
  const fetchBytes = async (path, label) => {
    checkAborted();
    const url = toURL(path);
    if (!url) throw new Error(`Missing URL for ${label}`);
    const response = signal ? await fetchImpl(url, { signal }) : await fetchImpl(url);
    checkAborted();
    if (!response.ok) throw new Error(`Failed to fetch ${label} (HTTP ${response.status})`);
    const buffer = await response.arrayBuffer();
    checkAborted();
    return new Uint8Array(buffer);
  };
  const glbName = asset.glb.split('/').at(-1) || `${asset.id}.glb`;
  const blendName = asset.blend.split('/').at(-1) || `${asset.id}.blend`;
  const creditsPath = asset.downloads?.credits;
  const [glbBytes, blendBytes, creditsBytes] = await Promise.all([
    fetchBytes(asset.glb, glbName),
    fetchBytes(asset.blend, blendName),
    creditsPath
      ? fetchBytes(creditsPath, 'CREDITS.txt').catch(error => {
          if (error?.name === 'AbortError' || signal?.aborted) throw error;
          return encoder.encode(fallbackCredits || defaultCreditsText(asset));
        })
      : Promise.resolve(encoder.encode(fallbackCredits || defaultCreditsText(asset))),
  ]);
  checkAborted();
  const bytes = buildStoreZip([
    { name: glbName, data: glbBytes },
    { name: blendName, data: blendBytes },
    { name: 'CREDITS.txt', data: creditsBytes },
  ]);
  return { filename: `${asset.id}.zip`, bytes };
}

export async function downloadModelZip(asset, options = {}) {
  const { filename, bytes } = await assembleModelZip(asset, options);
  if (options.signal?.aborted) throw new DOMException('Cancelled', 'AbortError');
  const blob = new Blob([bytes], { type: 'application/zip' });
  const href = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = href;
  link.download = filename;
  link.rel = 'noopener';
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(href), 60_000);
  return { filename, byteLength: bytes.byteLength };
}
