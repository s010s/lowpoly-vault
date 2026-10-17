#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only budget inventory for research GLBs; not a conformance validator.

Usage: python inspect_glb_samples.py inputs.json output.json
inputs.json is an array of {id, path, optional visual_status}. Embedded
PNG/JPEG/WebP GLBs are supported; meshopt/quantized counts are declarations
only and geometry is never decoded or validated here. Unknown extensions,
external buffers, sparse data, and non-triangle primitives fail explicitly.
GPU texture numbers are allocation estimates, not browser measurements.
"""
import hashlib
import io
import json
from pathlib import Path
import struct
import sys
from PIL import Image


def mip_bytes(width, height, bytes_per_pixel=4):
    total = 0
    while True:
        total += width * height * bytes_per_pixel
        if width == height == 1:
            return total
        width, height = max(1, width // 2), max(1, height // 2)


def inspect(record):
    path = Path(record['path'])
    data = path.read_bytes()
    magic, version, length = struct.unpack_from('<4sII', data)
    if (magic, version, length) != (b'glTF', 2, len(data)):
        raise ValueError('Invalid GLB header')
    chunks, offset = [], 12
    while offset < len(data):
        size, kind = struct.unpack_from('<II', data, offset)
        offset += 8
        if size % 4 or offset + size > length:
            raise ValueError('Invalid chunk size')
        chunks.append((kind, data[offset:offset + size]))
        offset += size
    if [c[0] for c in chunks] != [0x4e4f534a, 0x004e4942]:
        raise ValueError('Requires JSON and embedded BIN chunks')
    doc, binary = json.loads(chunks[0][1]), chunks[1][1]
    supported = {'EXT_texture_webp', 'KHR_materials_unlit', 'EXT_meshopt_compression', 'KHR_mesh_quantization'}
    if set(doc.get('extensionsUsed', [])) - supported:
        raise ValueError('Unsupported extension; use a decoder-aware inventory')
    if not doc.get('buffers') or any('uri' in b for b in doc['buffers']):
        raise ValueError('External buffers unsupported')
    if len(doc['buffers']) != 1 and 'EXT_meshopt_compression' not in doc.get('extensionsUsed', []):
        raise ValueError('Multiple buffers only supported as meshopt declarations')
    if any('sparse' in a for a in doc.get('accessors', [])):
        raise ValueError('Sparse data needs a separate inventory profile')
    primitives = [p for m in doc.get('meshes', []) for p in m['primitives']]
    if any(p.get('mode', 4) != 4 for p in primitives):
        raise ValueError('Requires TRIANGLES primitives')
    accessors = doc.get('accessors', [])
    pos_ids = {p['attributes']['POSITION'] for p in primitives}
    triangles = sum(accessors[p['indices']]['count'] // 3 if 'indices' in p
                    else accessors[p['attributes']['POSITION']]['count'] // 3
                    for p in primitives)
    mesh_triangles = [sum(accessors[p['indices']]['count'] // 3 if 'indices' in p
                         else accessors[p['attributes']['POSITION']]['count'] // 3
                         for p in m['primitives']) for m in doc.get('meshes', [])]
    scene_nodes = []
    def walk(index, ancestors):
        if index in ancestors:
            raise ValueError('Cyclic nodes')
        scene_nodes.append(index)
        for child in doc.get('nodes', [])[index].get('children', []):
            walk(child, ancestors | {index})
    for root in doc.get('scenes', [])[doc.get('scene', 0)].get('nodes', []):
        walk(root, set())
    mesh_refs = [doc['nodes'][i]['mesh'] for i in scene_nodes if 'mesh' in doc['nodes'][i]]
    images = []
    for image in doc.get('images', []):
        if 'bufferView' not in image or image.get('mimeType') not in {'image/png', 'image/jpeg', 'image/webp'}:
            raise ValueError('Requires embedded PNG/JPEG/WebP')
        view = doc['bufferViews'][image['bufferView']]
        if view.get('buffer', 0) != 0:
            raise ValueError('Image must be in the embedded GLB buffer')
        start = view.get('byteOffset', 0)
        encoded = binary[start:start + view['byteLength']]
        im = Image.open(io.BytesIO(encoded))
        images.append({'name': image.get('name'), 'mime': image['mimeType'],
                       'encoded_bytes': len(encoded), 'sha256': hashlib.sha256(encoded).hexdigest(),
                       'width': im.width, 'height': im.height, 'image_mode': im.mode,
                       'rgba8_base_bytes_estimate': im.width * im.height * 4,
                       'rgba8_full_mips_bytes_estimate': mip_bytes(im.width, im.height)})
    geometry_views = {accessors[i]['bufferView'] for p in primitives
                      for i in list(p['attributes'].values()) + ([p['indices']] if 'indices' in p else [])}
    materials = doc.get('materials', [])
    return {'id': record['id'], 'input_filename': path.name,
            'input_sha256': hashlib.sha256(data).hexdigest(), 'glb_bytes': len(data),
            'unique_mesh_triangles': triangles,
            'scene_triangles_all_nodes': sum(mesh_triangles[i] for i in mesh_refs),
            'unique_position_accessor_vertices': sum(accessors[i]['count'] for i in pos_ids),
            'declared_unique_geometry_buffer_view_bytes': sum(doc['bufferViews'][i]['byteLength'] for i in geometry_views),
            'mesh_count': len(doc.get('meshes', [])), 'mesh_instances': len(mesh_refs),
            'primitive_count': len(primitives), 'material_count': len(materials),
            'base_primitive_submissions_estimate': sum(len(doc['meshes'][i]['primitives']) for i in mesh_refs),
            'transparent_material_count': sum(m.get('alphaMode', 'OPAQUE') == 'BLEND' for m in materials),
            'masked_material_count': sum(m.get('alphaMode') == 'MASK' for m in materials),
            'double_sided_material_count': sum(bool(m.get('doubleSided')) for m in materials),
            'attribute_semantics': sorted({s for p in primitives for s in p['attributes']}),
            'animations': len(doc.get('animations', [])), 'skins': len(doc.get('skins', [])),
            'extensions_used': doc.get('extensionsUsed', []),
            'extensions_required': doc.get('extensionsRequired', []), 'images': images,
            'embedded_image_bytes': sum(i['encoded_bytes'] for i in images),
            'texture_rgba8_full_mips_bytes_estimate': sum(i['rgba8_full_mips_bytes_estimate'] for i in images),
            'visual_status': record.get('visual_status', 'not_assessed_by_inventory'),
            'runtime_gpu_status': 'not_measured',
            'notes': ['Geometry counts are declarations from accessors; geometry is not decoded or validated.',
                      'Counts include all default-scene mesh nodes, not actual visible/cull results.',
                      'Primitive submissions are a structural base-pass estimate; real draw calls may differ.',
                      'Texture estimate assumes one RGBA8/SRGB8_ALPHA8 allocation per embedded image with a full mip pyramid. Shared/duplicate sampler uploads, alignment, CPU copies, driver overhead, render targets and environment maps are excluded.',
                      'No FPS, decode time, GPU memory measurement, visual approval or format validity is established.']}


if __name__ == '__main__':
    records = json.loads(Path(sys.argv[1]).read_text())
    result = {'measurement_date_utc': '2026-10-17', 'method': __doc__, 'records': [inspect(r) for r in records]}
    Path(sys.argv[2]).write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
