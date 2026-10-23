# SPDX-License-Identifier: MIT
"""Original Murchisonia fossil interpretation, Blender 4.3.2, no external inputs.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output DIR
The supplied JSON and copied helpers are the complete build dependency set.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def sweep(name, start, stop, count, section_count, collection, material, cavity=False):
    vertices, faces = [], []
    for i in range(count + 1):
        turn = start + (stop - start) * i / count
        q = 1.5 ** (turn - 6)
        angle = -2 * math.pi * turn
        radial = Vector((math.cos(angle), math.sin(angle), 0))
        qr = q ** 0.83
        center = radial * (2.72 * qr) + Vector((0, 0, 21.3 - 17.5 * q))
        if cavity:
            # A short blind cavity, not a claim about inner-whorl anatomy.
            frac = max(0, min(1, (turn - start) / (6 - start)))
            inner_factor = 0.54 + 0.30 * frac
        else: inner_factor = 1
        for j in range(section_count):
            v = 2 * math.pi * j / section_count
            c, s = math.cos(v), math.sin(v)
            # Low rounded upper shoulder, never an invented sharp/spiny keel.
            shoulder = 0.10 * math.exp(-((v - 0.42) / 0.27) ** 2) if c > 0 else 0
            r = 2.78 * qr * (c + shoulder) * inner_factor
            z = 3.80 * q * s * inner_factor
            p = center + radial * r + Vector((0, 0, z))
            # Conservatively bowed, oblique terminal edge, not a sawn-off plane
            # or an assertion that the damaged fossil preserves a perfect lip.
            lip_weight=max(0,min(1,(turn-5.72)/.28))**2
            p.y+=lip_weight*(-.50*c-.55*s)
            if not cavity:
                # Minute original broad-scale worn calcite relief, no photo texture.
                variation = 0.015 * q * math.sin(13 * angle + 1.6 * s) * math.cos(3 * v)
                p += radial * variation
            vertices.append(tuple(p))
    for i in range(count):
        for j in range(section_count):
            a = i * section_count + j
            b = i * section_count + (j + 1) % section_count
            faces.append((a, b, b + section_count, a + section_count))
    if cavity:
        # Carry the final mouth outward, so the conservative axial envelope
        # cannot accidentally seal or mask the visible aperture from the front.
        old=count*section_count
        vertices.extend((x,y-8,z) for x,y,z in vertices[-section_count:])
        for j in range(section_count):
            a=old+j; b=old+(j+1)%section_count
            faces.append((a,b,b+section_count,a+section_count))
        count+=1
    faces.append(tuple(reversed(range(section_count))))
    faces.append(tuple(count * section_count + j for j in range(section_count)))
    return mesh_object(name, vertices, faces, material, collection)

def apply(obj, modifier):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=modifier.name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    params = json.loads((HERE / 'params.json').read_text())
    collection = setup_scene('murchisonia', seed=params['seed'])
    materials = [make_material('Fossil calcite', '#C6B99C', 0.94),
                 make_material('Pale mineral variation', '#CBBEA2', 0.95),
                 make_material('Soft ochre variation', '#C1B397', 0.96)]
    # Millimetre numerical construction for robust voxel/Boolean operations;
    # final geometry is baked into real-world metre coordinates before export.
    body = sweep('Coiled shell and conservative aperture', 0.10, 6.0, 354, 40, collection, materials[0])
    # A closed conservative inner envelope fills unnaturally deep coil recesses.
    # The outer helical skin remains visible as low continuous worn shoulders.
    profile=[(2.00,.03),(2.45,1.25),(3.0,2.1),(3.8,3.2),(4.8,4.1),(5.5,4.35),
             (7.0,3.95),(9.0,3.39),(11.0,2.82),(13.0,2.27),(15.0,1.68),
             (17.0,1.13),(19.0,.55),(20.2,.20),(20.6,.08)]
    dense=[]
    for i in range(len(profile)-1):
        p0=profile[max(0,i-1)]; p1=profile[i]; p2=profile[i+1]; p3=profile[min(len(profile)-1,i+2)]
        for k in range(8):
            t=k/8
            z=p1[0]+(p2[0]-p1[0])*t
            r=.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t*t+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t*t*t)
            dense.append((z,max(.025,r)))
    profile=dense+[profile[-1]]
    verts=[]; faces=[]; n=96
    for z,r in profile:
        if z>5.5: r*=max(.04,(21.3-z)/17.5)**(-.17)
        for j in range(n):
            t=2*math.pi*j/n; verts.append((r*math.cos(t),r*math.sin(t),z))
    for i in range(len(profile)-1):
        for j in range(n):
            a=i*n+j; b=i*n+(j+1)%n; faces.append((a,b,b+n,a+n))
    faces.append(tuple(reversed(range(n)))); faces.append(tuple((len(profile)-1)*n+j for j in range(n)))
    envelope=mesh_object('temporary conservative whorl envelope',verts,faces,materials[0],collection)
    bpy.ops.object.select_all(action='DESELECT'); body.select_set(True); envelope.select_set(True)
    bpy.context.view_layer.objects.active=body; bpy.ops.object.join()
    remesh = body.modifiers.new('Union intersecting whorl interiors', 'REMESH')
    remesh.mode = 'VOXEL'; remesh.voxel_size = 0.075; remesh.use_smooth_shade = True
    apply(body, remesh)
    smooth = body.modifiers.new('Worn fossil shoulder rounding', 'SMOOTH')
    smooth.factor = 0.34; smooth.iterations = 2; apply(body, smooth)
    cavity = sweep('temporary aperture cavity', 5.78, 6.0, 24, 48, collection, materials[0], cavity=True)
    boolean = body.modifiers.new('Conservative open aperture', 'BOOLEAN')
    boolean.operation = 'DIFFERENCE'; boolean.solver = 'EXACT'; boolean.object = cavity
    apply(body, boolean); bpy.data.objects.remove(cavity, do_unlink=True)
    remesh=body.modifiers.new('Regular manifold aperture topology','REMESH')
    remesh.mode='VOXEL'; remesh.voxel_size=.065; remesh.use_smooth_shade=True; apply(body,remesh)
    smooth=body.modifiers.new('Lightly worn aperture edge','SMOOTH')
    smooth.factor=.22; smooth.iterations=2; apply(body,smooth)
    decimate = body.modifiers.new('Deliberate low-poly surface', 'DECIMATE')
    decimate.ratio = min(1, 11000 / max(1, len(body.data.polygons) * 2))
    decimate.use_collapse_triangulate = True; apply(body, decimate)
    bm = bmesh.new(); bm.from_mesh(body.data)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=0.00001)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(body.data); bm.free()
    bounds = [(min(v.co[k] for v in body.data.vertices), max(v.co[k] for v in body.data.vertices)) for k in range(3)]
    dims = (params['width'], params['depth'], params['height'])
    for vertex in body.data.vertices:
        original = vertex.co.copy()
        for axis in range(3):
            lo, hi = bounds[axis]
            vertex.co[axis] = (original[axis] - (lo if axis == 2 else (lo + hi) / 2)) * dims[axis] / (hi - lo)
    for mat in materials[1:]: body.data.materials.append(mat)
    for polygon in body.data.polygons:
        center = sum((body.data.vertices[i].co for i in polygon.vertices), Vector()) / len(polygon.vertices)
        n = math.sin(center.x * 750 + center.z * 470) + 0.55 * math.sin(center.y * 1460 - center.z * 910)
        polygon.material_index = 1 if n > 0.8 else 2 if n < -0.8 else 0
        polygon.use_smooth = True
    body['construction'] = 'Original logarithmic coiling; buried tube interiors unioned, blind cavity cut into final mouth, low worn shoulder.'
    body['aperture_reconstruction'] = 'Conservative local repair, not exact intact lip, slit, canal or internal anatomy.'
    body['scale_uncertainty_m'] = 0.001
    bpy.context.view_layer.update()
    source = audit_source(collection, max_triangles=40000)
    if source['errors']:
        save(output / 'source-failure.json', source); raise RuntimeError(str(source['errors']))
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(output / 'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.all_objects: obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[collection['asset_root']]
    options = dict(filepath=str(output / 'model.glb'), export_format='GLB', use_selection=True,
        export_yup=True, export_apply=True, export_normals=True, export_texcoords=False,
        export_tangents=False, export_materials='EXPORT', export_vertex_color='NONE',
        export_animations=False, export_skins=False, export_morph=False, export_cameras=False,
        export_lights=False, export_extras=True, export_gpu_instances=False, export_gn_mesh=False,
        export_draco_mesh_compression_enable=False, export_use_gltfpack=False)
    available = {p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if not set(options).issubset(available): raise RuntimeError('Required exporter options missing')
    bpy.ops.export_scene.gltf(**options)
    glb = audit_glb(output / 'model.glb', 40000, 6, 8)
    sb = source['bounds_blender_m']
    expected = {'min': [sb['min'][0], sb['min'][2], -sb['max'][1]], 'max': [sb['max'][0], sb['max'][2], -sb['min'][1]]}
    delta = max(abs(glb['bounds_m'][side][i] - expected[side][i]) for side in ('min', 'max') for i in range(3))
    if glb['errors'] or delta > 1e-7 or glb['scene_triangles'] != source['triangles']:
        raise RuntimeError('Export evidence mismatch: ' + str(glb['errors']))
    report = {'asset_id': 'murchisonia', 'revision': 'r001', 'blender_version': bpy.app.version_string,
              'generator_sha256': sha(__file__), 'params_sha256': sha(HERE / 'params.json'), 'source': source, 'glb': glb,
              'bounds_roundtrip_max_error_m': delta, 'export_options': {k: v for k, v in options.items() if k != 'filepath'},
              'dimensions_m': {'width': params['width'], 'depth': params['depth'], 'height': params['height']},
              'material_profile': 'Original neutral calcite palette, intentional smooth low-poly, no textures or external images.',
              'glb_sha256': sha(output / 'model.glb'), 'blend_sha256': sha(output / 'model.blend')}
    save(output / 'build-report.json', report)
    print(json.dumps({'status': 'BUILT', 'triangles': glb['scene_triangles'], 'glb_bytes': glb['bytes'], 'sha256': glb['sha256']}))
if __name__ == '__main__': main()
