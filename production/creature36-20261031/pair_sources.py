"""Blender --background --python pair_sources.py -- [recheck]

Build a clean editable pair by importing each exact transformed delivery GLB.
Original authoring files remain in the private recovery archive.
"""
import bpy,json,pathlib,hashlib,sys
from mathutils import Vector
ROOT=pathlib.Path(__file__).resolve().parents[2]
folder=ROOT/'production/creature36-20261031';ledger=json.loads((folder/'integration-ledger.json').read_text());records=[]
recheck='recheck' in sys.argv
for row in ledger['models']:
    glb=ROOT/row['glb'];target=glb.with_name('source.blend')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if recheck:bpy.ops.wm.open_mainfile(filepath=str(target))
    else:
        assert not target.exists()
        bpy.ops.import_scene.gltf(filepath=str(glb))
        bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
        for im in bpy.data.images:
            if not im.packed_file:im.pack()
        bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    coords=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
    lo=[min(v[k] for v in coords) for k in range(3)];hi=[max(v[k] for v in coords) for k in range(3)]
    # glTF Y up -> Blender Z up. Object boxes may conservatively overbound after
    # a rotation; actual mesh vertices provide the verification coordinates.
    coords=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
    lo=[min(v[k] for v in coords) for k in range(3)];hi=[max(v[k] for v in coords) for k in range(3)]
    dims=[hi[k]-lo[k] for k in range(3)];expected=row['bounds']['dimensions'];actual=[dims[0],dims[2],dims[1]]
    assert max(abs(a-b) for a,b in zip(actual,expected))<2e-5,(row['id'],actual,expected)
    assert abs(lo[2])<2e-5
    triangles=sum(len(p.vertices)-2 for o in meshes for p in o.data.polygons)
    assert triangles==row['bounds']['triangles']
    images=[dict(name=i.name,width=i.size[0],height=i.size[1],packed=bool(i.packed_file)) for i in bpy.data.images]
    assert all(i['packed'] and i['width']>0 and i['height']>0 for i in images)
    b=target.read_bytes();records.append(dict(id=row['id'],glb_sha256=row['glb_sha256'],blend=str(target.relative_to(ROOT)),blend_sha256=hashlib.sha256(b).hexdigest(),blend_bytes=len(b),triangles=triangles,dimensions_glb_axes=actual,images=images,relationship='Clean import of exact delivery GLB; editable source, not original authoring history or byte-identical reexport guarantee.',reopened=recheck))
    print('PAIRED',row['id'],len(b),flush=True)
(folder/'evidence'/('source-reopen.json' if recheck else 'source-pairs.json')).write_text(json.dumps(dict(blender=bpy.app.version_string,models=records),indent=2)+'\n')
