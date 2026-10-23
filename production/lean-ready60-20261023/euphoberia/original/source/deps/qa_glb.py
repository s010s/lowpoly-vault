#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Project audit for static, uncompressed, self-contained GLBs.

This is deliberately not a replacement for Khronos glTF Validator. Unsupported
sparse/compressed/skinned/animated/instanced geometry fails this baseline audit.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct

IDENTITY = [1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1.]


def read_glb(path):
    data = Path(path).read_bytes()
    if len(data) < 20:
        raise ValueError('File too short for GLB')
    magic, version, length = struct.unpack_from('<4sII', data)
    if magic != b'glTF' or version != 2 or length != len(data):
        raise ValueError('Invalid GLB magic/version/declared length')
    chunks, offset = [], 12
    while offset < length:
        if offset + 8 > length:
            raise ValueError('Truncated chunk header')
        size, kind = struct.unpack_from('<II', data, offset)
        offset += 8
        if size % 4 or offset + size > length:
            raise ValueError('Invalid chunk length/alignment')
        chunks.append((kind, data[offset:offset+size]))
        offset += size
    if not chunks or chunks[0][0] != 0x4E4F534A:
        raise ValueError('First chunk is not JSON')
    if len(chunks) != 2 or chunks[1][0] != 0x004E4942:
        raise ValueError('Baseline expects JSON plus one embedded BIN chunk')
    return json.loads(chunks[0][1]), chunks[1][1], data


def accessor_values(doc, binary, index):
    a = doc['accessors'][index]
    if 'sparse' in a:
        raise ValueError('Sparse accessors need a separate validation profile')
    if 'bufferView' not in a:
        raise ValueError('Baseline accessor has no bufferView')
    v = doc['bufferViews'][a['bufferView']]
    if v.get('buffer', 0) != 0:
        raise ValueError('Only embedded buffer 0 is supported')
    formats = {5120:('b',1), 5121:('B',1), 5122:('h',2), 5123:('H',2), 5125:('I',4), 5126:('f',4)}
    sizes = {'SCALAR':1, 'VEC2':2, 'VEC3':3, 'VEC4':4}
    if a['componentType'] not in formats or a['type'] not in sizes:
        raise ValueError('Unsupported accessor component/type')
    code, component_size = formats[a['componentType']]
    count = sizes[a['type']]
    packed = component_size * count
    stride = v.get('byteStride', packed)
    if stride < packed:
        raise ValueError('Accessor stride is smaller than element size')
    view_start = v.get('byteOffset', 0)
    start = view_start + a.get('byteOffset', 0)
    end = start + max(0, a['count'] - 1) * stride + (packed if a['count'] else 0)
    if start < view_start or end > view_start + v['byteLength'] or end > len(binary):
        raise ValueError('Accessor runs outside bufferView/BIN')
    result = [struct.unpack_from('<' + code*count, binary, start+i*stride) for i in range(a['count'])]
    if a.get('normalized'):
        maxima = {5120:127, 5121:255, 5122:32767, 5123:65535}
        if a['componentType'] not in maxima:
            raise ValueError('Invalid normalized component type')
        maximum = maxima[a['componentType']]
        result = [tuple(max(-1., x/maximum) for x in row) for row in result]
    if any(not math.isfinite(x) for row in result for x in row):
        raise ValueError('Non-finite accessor values')
    return result


def matmul(a, b):
    return [sum(a[k*4+r]*b[c*4+k] for k in range(4)) for c in range(4) for r in range(4)]


def node_matrix(node):
    if 'matrix' in node:
        return node['matrix']
    x,y,z,w = node.get('rotation', [0,0,0,1])
    sx,sy,sz = node.get('scale', [1,1,1])
    tx,ty,tz = node.get('translation', [0,0,0])
    return [(1-2*y*y-2*z*z)*sx, (2*x*y+2*w*z)*sx, (2*x*z-2*w*y)*sx, 0,
            (2*x*y-2*w*z)*sy, (1-2*x*x-2*z*z)*sy, (2*y*z+2*w*x)*sy, 0,
            (2*x*z+2*w*y)*sz, (2*y*z-2*w*x)*sz, (1-2*x*x-2*y*y)*sz, 0,
            tx,ty,tz,1]


def transform(m, p):
    return tuple(sum(m[k*4+r]*p[k] for k in range(3)) + m[12+r] for r in range(3))


def semantic_digest(doc,binary):
    """Hash decoded data and scene structure, ignoring layout, generator and extras.

    Node/mesh order and topology order remain meaningful. This is a deterministic
    rebuild digest, not a topology-isomorphism or perceptual-equivalence test.
    """
    def clean(value):
        if isinstance(value,dict): return {k:clean(v) for k,v in value.items() if k not in {'name','extras'}}
        if isinstance(value,(list,tuple)): return [clean(v) for v in value]
        if isinstance(value,float): return round(value,8)
        return value
    payload={'meshes':[], 'nodes':clean(doc.get('nodes',[])),
             'scenes':clean(doc.get('scenes',[])), 'scene':doc.get('scene',0),
             'materials':clean(doc.get('materials',[])), 'textures':clean(doc.get('textures',[])),
             'samplers':clean(doc.get('samplers',[])), 'images':[]}
    for mesh in doc.get('meshes',[]):
        parts=[]
        for part in mesh.get('primitives',[]):
            attrs={name:accessor_values(doc,binary,index) for name,index in sorted(part['attributes'].items())}
            indices=accessor_values(doc,binary,part['indices']) if 'indices' in part else None
            parts.append({'mode':part.get('mode',4),'attributes':attrs,'indices':indices,'material':part.get('material')})
        payload['meshes'].append(parts)
    for image in doc.get('images',[]):
        if 'bufferView' not in image: raise ValueError('Digest requires embedded image bufferViews')
        view=doc['bufferViews'][image['bufferView']]
        start=view.get('byteOffset',0)
        payload['images'].append({'mimeType':image.get('mimeType'),'sha256':hashlib.sha256(binary[start:start+view['byteLength']]).hexdigest()})
    encoded=json.dumps(clean(payload),sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def audit_glb(path, max_triangles=12000, max_materials=8, max_primitives=24, ground_tolerance=0.002):
    errors, warnings = [], []
    report = {'profile':'static-uncompressed-v1', 'file':str(path), 'errors':errors, 'warnings':warnings,
              'khronos_validator':'not_run_by_this_script'}
    try:
        doc, binary, raw = read_glb(path)
        report.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), generator=doc.get('asset',{}).get('generator'))
        if doc.get('asset',{}).get('version') != '2.0': errors.append('Asset version is not 2.0')
        if len(doc.get('buffers',[])) != 1 or any('uri' in b for b in doc.get('buffers',[])):
            errors.append('Expected one embedded buffer with no URI')
        if any('uri' in image for image in doc.get('images',[])):
            errors.append('External or data-URI images violate standalone GLB baseline')
        if doc.get('animations') or doc.get('skins'):
            errors.append('Animations/skins require another profile')
        extensions = doc.get('extensionsUsed',[])
        report['extensions_used'] = extensions
        forbidden = {'KHR_draco_mesh_compression','EXT_meshopt_compression','KHR_meshopt_compression','EXT_mesh_gpu_instancing'}
        if forbidden.intersection(extensions):
            raise ValueError('Compressed/instanced asset needs another audit profile')
        materials = doc.get('materials',[])
        report['materials'] = len(materials)
        if not materials: errors.append('No exported materials')
        if len(materials) > max_materials: warnings.append(f'Material budget exceeded: {len(materials)} > {max_materials}')
        for i,m in enumerate(materials):
            if m.get('alphaMode','OPAQUE') != 'OPAQUE': warnings.append(f'Material {i} is not opaque')
            if m.get('doubleSided',False): warnings.append(f'Material {i} is double-sided; review intentional thin surfaces')
        geom, unique_triangles, unique_primitives = [], 0, 0
        position_accessors = set()
        for mi,mesh in enumerate(doc.get('meshes',[])):
            parts = []
            for pi,p in enumerate(mesh.get('primitives',[])):
                label = f'mesh {mi} primitive {pi}'
                if p.get('mode',4) != 4: raise ValueError(label+' is not TRIANGLES')
                if p.get('targets'): raise ValueError(label+' has morph targets')
                attrs = p.get('attributes',{})
                if 'POSITION' not in attrs: raise ValueError(label+' lacks POSITION')
                positions = accessor_values(doc,binary,attrs['POSITION'])
                position_accessors.add(attrs['POSITION'])
                if not positions: errors.append(label+' is empty')
                normals = accessor_values(doc,binary,attrs['NORMAL']) if 'NORMAL' in attrs else []
                if len(normals) != len(positions): errors.append(label+' lacks matching normals')
                elif any(abs(math.sqrt(sum(x*x for x in n))-1)>0.005 for n in normals): errors.append(label+' contains non-unit normals')
                indices = [v[0] for v in accessor_values(doc,binary,p['indices'])] if 'indices' in p else list(range(len(positions)))
                if len(indices)%3: errors.append(label+' index/vertex count is not divisible by three')
                if any(not isinstance(i,int) or i<0 or i>=len(positions) for i in indices): raise ValueError(label+' invalid index')
                degenerates = 0
                for offset in range(0,len(indices)-2,3):
                    a,b,c = [positions[i] for i in indices[offset:offset+3]]
                    u,v = [b[j]-a[j] for j in range(3)], [c[j]-a[j] for j in range(3)]
                    cross = [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
                    if sum(x*x for x in cross)<1e-20: degenerates += 1
                if degenerates: errors.append(f'{label} has {degenerates} degenerate triangles')
                triangles = len(indices)//3
                parts.append((positions,triangles))
                unique_triangles += triangles
                unique_primitives += 1
            geom.append(parts)
        report['unique_mesh_triangles'] = unique_triangles
        report['unique_mesh_primitives'] = unique_primitives
        report['unique_position_accessor_vertices'] = sum(doc['accessors'][i]['count'] for i in position_accessors)
        nodes = doc.get('nodes',[])
        scene_index = doc.get('scene',0)
        scenes = doc.get('scenes',[])
        if not scenes: raise ValueError('No scene')
        if scene_index >= len(scenes): raise ValueError('Invalid default scene index')
        points, rendered_triangles, rendered_primitives, seen = [], 0, 0, set()
        def walk(index,parent,stack):
            nonlocal rendered_triangles,rendered_primitives
            if index in stack: raise ValueError('Cycle in node hierarchy')
            if index in seen: raise ValueError('Node has multiple parents in active scene')
            seen.add(index)
            node = nodes[index]
            world = matmul(parent,node_matrix(node))
            if any(not math.isfinite(x) for x in world): raise ValueError('Non-finite node transform')
            if 'mesh' in node:
                for vertices,triangles in geom[node['mesh']]:
                    points.extend(transform(world,p) for p in vertices)
                    rendered_triangles += triangles
                    rendered_primitives += 1
            for child in node.get('children',[]): walk(child,world,stack|{index})
        for index in scenes[scene_index].get('nodes',[]): walk(index,IDENTITY,set())
        if not points: errors.append('No visible geometry in default scene')
        else:
            lower = [min(p[i] for p in points) for i in range(3)]
            upper = [max(p[i] for p in points) for i in range(3)]
            report['bounds_m'] = {'min':lower,'max':upper,'size':[upper[i]-lower[i] for i in range(3)]}
            if abs(lower[1]) > ground_tolerance: warnings.append(f'Lowest glTF Y is {lower[1]:.6f} m; verify mounting/ground contract')
        report['semantic_sha256'] = semantic_digest(doc,binary)
        report['semantic_digest_profile'] = 'decoded-static-content-v1'
        report['scene_triangles'] = rendered_triangles
        report['scene_primitives_estimated_base_draw_calls'] = rendered_primitives
        if rendered_triangles > max_triangles: errors.append(f'Triangle budget exceeded: {rendered_triangles} > {max_triangles}')
        if rendered_primitives > max_primitives: warnings.append(f'Primitive budget exceeded: {rendered_primitives} > {max_primitives}')
    except (ValueError,IndexError,KeyError,TypeError,struct.error,OverflowError) as exc:
        errors.append(str(exc))
    report['status'] = 'fail' if errors else 'pass_with_warnings' if warnings else 'pass'
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('glb'); p.add_argument('--report'); p.add_argument('--max-triangles',type=int,default=12000)
    p.add_argument('--max-materials',type=int,default=8); p.add_argument('--max-primitives',type=int,default=24)
    a=p.parse_args()
    result=audit_glb(a.glb,a.max_triangles,a.max_materials,a.max_primitives)
    encoded=json.dumps(result,indent=2,ensure_ascii=False)
    if a.report: Path(a.report).write_text(encoded+'\n')
    print(encoded)
    return 1 if result['errors'] else 0

if __name__=='__main__': raise SystemExit(main())
