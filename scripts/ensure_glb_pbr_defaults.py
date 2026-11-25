#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Losslessly normalize GLB PBR metallicFactor/roughnessFactor defaults.

glTF 2.0 defaults omitted pbrMetallicRoughness.metallicFactor to 1.0 (pure metal),
which renders dark/metallic in engines without an IBL environment map. This helper
rewrites only the JSON chunk (4-byte space-padded) while preserving the BIN chunk
byte-for-byte, ensuring non-whitelisted materials without metallicRoughnessTexture
explicitly set metallicFactor=0.0 and a sensible default roughnessFactor (0.85-1.0).
"""
import argparse
import json
from pathlib import Path
import struct

GLB_MAGIC = b'glTF'
CHUNK_JSON = 0x4E4F534A
CHUNK_BIN = 0x004E4942
TRUE_METAL_WHITELIST = frozenset({'pyrite-cube-cluster', 'native-copper-dendrite'})
DEFAULT_ROUGHNESS = 0.9


def read_glb_chunks(data: bytes):
    if len(data) < 20:
        raise ValueError(f'File too short for GLB ({len(data)} bytes)')
    magic, version, declared_len = struct.unpack_from('<4sII', data, 0)
    if magic != GLB_MAGIC or version != 2 or declared_len != len(data):
        raise ValueError('Invalid GLB v2 header or declared length mismatch')
    chunks = []
    offset = 12
    while offset < declared_len:
        if offset + 8 > declared_len:
            raise ValueError('Truncated GLB chunk header')
        chunk_len, chunk_type = struct.unpack_from('<II', data, offset)
        offset += 8
        if chunk_len % 4 != 0 or offset + chunk_len > declared_len:
            raise ValueError('Invalid GLB chunk alignment or length')
        chunks.append((chunk_type, data[offset:offset + chunk_len]))
        offset += chunk_len
    if not chunks or chunks[0][0] != CHUNK_JSON:
        raise ValueError('First GLB chunk must be JSON')
    doc = json.loads(chunks[0][1].decode('utf-8'))
    return doc, chunks[1:]


def pack_glb(doc: dict, trailing_chunks) -> bytes:
    json_bytes = json.dumps(doc, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    pad = (-len(json_bytes)) % 4
    if pad:
        json_bytes += b' ' * pad
    body = [struct.pack('<II', len(json_bytes), CHUNK_JSON), json_bytes]
    for chunk_type, payload in trailing_chunks:
        cpad = (-len(payload)) % 4
        if cpad:
            payload = payload + (b'\x00' * cpad)
        body.append(struct.pack('<II', len(payload), chunk_type))
        body.append(payload)
    total_len = 12 + sum(len(part) for part in body)
    header = struct.pack('<4sII', GLB_MAGIC, 2, total_len)
    return header + b''.join(body)


def normalize_glb_materials_bytes(
    data: bytes,
    *,
    asset_id: str | None = None,
    metallic_factor: float = 0.0,
    default_roughness: float = DEFAULT_ROUGHNESS,
    roughness_override: float | None = None,
    max_allowed_metallic: float = 0.1,
    force_metallic: bool = False,
    whitelist=TRUE_METAL_WHITELIST,
):
    doc, trailing = read_glb_chunks(data)
    exempt = bool(asset_id and asset_id in whitelist)
    changes = []
    if not exempt:
        for idx, mat in enumerate(doc.get('materials') or []):
            pbr = mat.setdefault('pbrMetallicRoughness', {})
            has_mr_tex = isinstance(pbr.get('metallicRoughnessTexture'), dict) and isinstance(
                pbr['metallicRoughnessTexture'].get('index'), int
            )
            if has_mr_tex:
                continue
            old_mf = pbr.get('metallicFactor', None)
            if force_metallic or old_mf is None or not isinstance(old_mf, (int, float)) or old_mf > max_allowed_metallic:
                pbr['metallicFactor'] = float(metallic_factor)
                changes.append({'material': idx, 'field': 'metallicFactor', 'before': old_mf, 'after': float(metallic_factor)})
            old_rf = pbr.get('roughnessFactor', None)
            if roughness_override is not None:
                if old_rf != float(roughness_override):
                    pbr['roughnessFactor'] = float(roughness_override)
                    changes.append({'material': idx, 'field': 'roughnessFactor', 'before': old_rf, 'after': float(roughness_override)})
            elif old_rf is None:
                pbr['roughnessFactor'] = float(default_roughness)
                changes.append({'material': idx, 'field': 'roughnessFactor', 'before': None, 'after': float(default_roughness)})
    out_bytes = pack_glb(doc, trailing) if changes else data
    return out_bytes, {'changed': bool(changes), 'exempt': exempt, 'changes': changes, 'before_bytes': len(data), 'after_bytes': len(out_bytes)}


def ensure_glb_pbr_defaults(
    glb_path,
    *,
    output_path=None,
    asset_id: str | None = None,
    default_roughness: float = DEFAULT_ROUGHNESS,
    roughness_override: float | None = None,
    force_metallic: bool = False,
):
    src = Path(glb_path)
    dst = Path(output_path) if output_path else src
    raw = src.read_bytes()
    patched, report = normalize_glb_materials_bytes(
        raw,
        asset_id=asset_id,
        default_roughness=default_roughness,
        roughness_override=roughness_override,
        force_metallic=force_metallic,
    )
    if dst != src or report['changed']:
        dst.write_bytes(patched)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('glb', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--id', dest='asset_id')
    parser.add_argument('--default-roughness', type=float, default=DEFAULT_ROUGHNESS)
    parser.add_argument('--roughness', type=float, default=None, help='Explicitly override roughnessFactor (e.g. 0.25 for crystal/glass)')
    parser.add_argument('--force-metallic-zero', action='store_true')
    args = parser.parse_args()
    report = ensure_glb_pbr_defaults(
        args.glb,
        output_path=args.output,
        asset_id=args.asset_id,
        default_roughness=args.default_roughness,
        roughness_override=args.roughness,
        force_metallic=args.force_metallic_zero,
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
