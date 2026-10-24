# SPDX-License-Identifier: MIT
"""Reopen editable source and audit closed components, floor and semantic groups."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy,bmesh
from asset_common import audit_source
args=sys.argv[sys.argv.index('--')+1:];src=Path(args[0]);dest=Path(args[1])
bpy.ops.wm.open_mainfile(filepath=str(src))
c=bpy.data.collections['EXPORT'];report=audit_source(c,6500);components=[]
for obj in c.all_objects:
    if obj.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(obj.data);todo=set(bm.verts);counts=[]
    while todo:
        stack=[next(iter(todo))];verts=set()
        while stack:
            v=stack.pop()
            if v in verts:continue
            verts.add(v);todo.discard(v)
            stack.extend(e.other_vert(v) for e in v.link_edges if e.other_vert(v) not in verts)
        fs={f for v in verts for f in v.link_faces};sub=bmesh.new();mapping={v:sub.verts.new(v.co) for v in verts}
        for face in fs:sub.faces.new([mapping[v] for v in face.verts])
        volume=sub.calc_volume(signed=True);boundary=sum(e.is_boundary for e in sub.edges);nonmanifold=sum(not e.is_manifold for e in sub.edges)
        counts.append({'vertices':len(verts),'faces':len(fs),'signed_volume_m3':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold});sub.free()
    components.append({'name':obj.name,'semantic_vertex_groups':list(obj.vertex_groups.keys()),'components':counts});bm.free()
report.update(source_blend_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),blender_version=bpy.app.version_string,cameras=sum(o.type=='CAMERA' for o in bpy.data.objects),lights=sum(o.type=='LIGHT' for o in bpy.data.objects),unpacked_external_images=[i.name for i in bpy.data.images if i.source=='FILE' and i.filepath and not i.packed_file],preview_collection_exists='_PREVIEW_ONLY' in bpy.data.collections,components=components,component_volume_scope='Closed constituent volumes and outward orientation only; overlapping anatomical solids are not a printable union.')
report['pass']=not report['errors'] and report['cameras']==0 and report['lights']==0 and not report['preview_collection_exists'] and not report['unpacked_external_images'] and all(p['signed_volume_m3']>0 and p['nonmanifold_edges']==0 for o in components for p in o['components'])
dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'pass':report['pass'],'components':sum(len(o['components']) for o in components)}))
if not report['pass']:raise RuntimeError('Source reopen inspection failed')
