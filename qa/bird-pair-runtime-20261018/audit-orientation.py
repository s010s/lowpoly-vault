"""Read-only exact-coordinate edge orientation audit; does not modify the GLB."""
import argparse, hashlib, json, struct
from collections import defaultdict, Counter
from pathlib import Path

def audit(path):
    data = path.read_bytes()
    length = struct.unpack_from('<I', data, 12)[0]
    doc = json.loads(data[20:20+length])
    binary = data[28+length:]
    def accessor(index):
        acc = doc['accessors'][index]
        view = doc['bufferViews'][acc['bufferView']]
        count = {'SCALAR':1, 'VEC3':3}[acc['type']]
        code = {5123:'H', 5125:'I', 5126:'f'}[acc['componentType']]
        fmt = '<' + code * count
        stride = view.get('byteStride', struct.calcsize(fmt))
        offset = view.get('byteOffset', 0) + acc.get('byteOffset', 0)
        return [struct.unpack_from(fmt, binary, offset + n * stride) for n in range(acc['count'])]
    edges = defaultdict(list)
    triangle_index = 0
    for mesh in doc['meshes']:
        for primitive in mesh['primitives']:
            positions = accessor(primitive['attributes']['POSITION'])
            indices = [x[0] for x in accessor(primitive['indices'])]
            material = doc['materials'][primitive['material']]['name']
            for offset in range(0, len(indices), 3):
                a, b, c = [positions[i] for i in indices[offset:offset+3]]
                for x, y in ((a,b),(b,c),(c,a)):
                    key = tuple(sorted((x,y)))
                    edges[key].append((1 if x == key[0] else -1, triangle_index, material))
                triangle_index += 1
    conflicts = [v for v in edges.values() if len(v) == 2 and v[0][0] == v[1][0]]
    counts = Counter()
    for values in conflicts:
        for material in {v[2] for v in values}:
            counts[material] += 1
    return {'asset':path.stem, 'sha256':hashlib.sha256(data).hexdigest(),
            'method':'Read-only decode of GLB triangle indices/positions; join identical exact float-coordinate edges and compare adjacent triangle traversal.',
            'triangles':triangle_index, 'geometric_edges':len(edges),
            'boundary_edges':sum(len(v)==1 for v in edges.values()),
            'edges_more_than_two_faces':sum(len(v)>2 for v in edges.values()),
            'shared_edges_with_same_direction':len(conflicts),
            'triangles_touching_orientation_conflicts':len({v[1] for values in conflicts for v in values}),
            'orientation_conflicts_touching_materials':dict(counts),
            'materials_double_sided':[m.get('doubleSided',False) for m in doc['materials']],
            'orientation_result':'FAIL' if conflicts else 'PASS',
            'limit':'Consistent edge traversal does not itself establish outward orientation, actual browser appearance, or absence of self-intersection.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('glbs', nargs='+', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    reports = [audit(p) for p in args.glbs]
    encoded = json.dumps(reports, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded)
