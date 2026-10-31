"""Compare reopened Blend against a separate fresh import of exact delivery GLB."""
import bpy,pathlib,json,hashlib,array
ROOT=pathlib.Path(__file__).resolve().parents[2];folder=ROOT/'production/creature36-20261031';ledger=json.loads((folder/'integration-ledger.json').read_text())
def fingerprint():
    meshes=[]
    for o in bpy.context.scene.objects:
        if o.type!='MESH':continue
        m=o.data;vertices=array.array('f',[0])*(len(m.vertices)*3);m.vertices.foreach_get('co',vertices)
        uv=[]
        for layer in m.uv_layers:
            a=array.array('f',[0])*(len(layer.data)*2);layer.data.foreach_get('uv',a);uv.append(hashlib.sha256(a.tobytes()).hexdigest())
        meshes.append(dict(vertices=hashlib.sha256(vertices.tobytes()).hexdigest(),faces=[list(p.vertices) for p in m.polygons],uv=uv,matrix=[v for row in o.matrix_world for v in row],materials=[s.material.name for s in o.material_slots]))
    images=sorted((i.name,hashlib.sha256(i.packed_file.data).hexdigest(),list(i.size),i.colorspace_settings.name) for i in bpy.data.images)
    return dict(meshes=meshes,images=images)
records=[]
for row in ledger['models']:
    glb=ROOT/row['glb'];source=glb.with_name('source.blend')
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb));a=fingerprint()
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.wm.open_mainfile(filepath=str(source));b=fingerprint()
    assert a==b,row['id']
    records.append(dict(id=row['id'],glb_sha256=row['glb_sha256'],blend_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),vertex_face_uv_material_and_matrix_equality=True,packed_images=[dict(name=i[0],sha256=i[1],dimensions=i[2],colorspace=i[3]) for i in a['images']]))
    print('PAIR_EQUAL',row['id'],flush=True)
(folder/'evidence/source-equality.json').write_text(json.dumps(dict(blender=bpy.app.version_string,models=records),indent=2)+'\n')
