import bpy, bmesh, json, hashlib, math, os, sys
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
asset_id, expected_sha, out_path=args
src=bpy.data.filepath
with open(src,'rb') as f: source_sha=hashlib.sha256(f.read()).hexdigest()
objects=[]
col=bpy.data.collections.get('EXPORT')
selected=list(col.objects) if col else list(bpy.data.objects)
for ob in selected:
    if ob.type!='MESH': continue
    mesh=ob.data
    # authored topology, computed from loaded source mesh data
    authored_v=len(mesh.vertices); authored_p=len(mesh.polygons); authored_tri=sum(max(0,len(p.vertices)-2) for p in mesh.polygons)
    # Evaluate modifiers without writing/saving the source.
    dg=bpy.context.evaluated_depsgraph_get(); ev=ob.evaluated_get(dg); em=ev.to_mesh(preserve_all_data_layers=False,depsgraph=dg)
    eval_v=len(em.vertices); eval_p=len(em.polygons); eval_tri=sum(max(0,len(p.vertices)-2) for p in em.polygons)
    mins=[min(v.co[i] for v in em.vertices) for i in range(3)] if em.vertices else [0,0,0]
    maxs=[max(v.co[i] for v in em.vertices) for i in range(3)] if em.vertices else [0,0,0]
    # BMesh is built in memory from the evaluated mesh. Weld coincident vertices before topology checks.
    bm=bmesh.new(); bm.from_mesh(em)
    pre_weld=len(bm.verts)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
    welded_v=len(bm.verts)
    boundary=sum(1 for e in bm.edges if e.is_boundary)
    nonmanifold=sum(1 for e in bm.edges if not e.is_manifold and not e.is_boundary)
    wire=sum(1 for e in bm.edges if e.is_wire)
    # A copied in-memory triangulation checks zero-area triangle degeneracy without touching source data.
    tri_bm=bmesh.new(); tri_bm.from_mesh(em); bmesh.ops.triangulate(tri_bm,faces=list(tri_bm.faces))
    degenerate=sum(1 for f in tri_bm.faces if f.calc_area()<=1e-14)
    objects.append({'name':ob.name,'data_name':mesh.name,'authored_vertices':authored_v,'authored_polygons':authored_p,'authored_triangle_equiv':authored_tri,'evaluated_vertices':eval_v,'evaluated_polygons':eval_p,'evaluated_triangle_equiv':eval_tri,'welded_vertices':welded_v,'vertices_welded':pre_weld-welded_v,'boundary_edges_after_weld':boundary,'nonmanifold_edges_after_weld':nonmanifold,'wire_edges_after_weld':wire,'degenerate_triangulated_faces_area_le_1e-14':degenerate,'bounds_local_m':{'min':mins,'max':maxs,'size':[maxs[i]-mins[i] for i in range(3)]},'modifiers':[{'name':m.name,'type':m.type,'show_viewport':m.show_viewport} for m in ob.modifiers]})
    bm.free(); tri_bm.free(); ev.to_mesh_clear()
# Evaluate scene/world bounds for exported objects in the same coordinate basis.
all_world=[]
for ob in selected:
    if ob.type!='MESH': continue
    dg=bpy.context.evaluated_depsgraph_get(); ev=ob.evaluated_get(dg); em=ev.to_mesh()
    for v in em.vertices: all_world.append(ob.matrix_world @ v.co)
    ev.to_mesh_clear()
if all_world:
    lo=[min(v[i] for v in all_world) for i in range(3)]; hi=[max(v[i] for v in all_world) for i in range(3)]
else: lo=hi=[0,0,0]
report={'asset_id':asset_id,'blend_path':src,'blend_sha256':source_sha,'expected_sha256':expected_sha,'hash_match':source_sha==expected_sha,'blender_version':bpy.app.version_string,'read_only':'opened from source; no save operator invoked','export_collection_found':bool(col),'objects':objects,'export_collection_bounds_blender_m':{'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]}}
with open(out_path,'w') as f: json.dump(report,f,indent=2); f.write('\n')
print(json.dumps({'asset_id':asset_id,'hash_match':source_sha==expected_sha,'objects':len(objects),'triangles':sum(x['evaluated_triangle_equiv'] for x in objects),'report':out_path}))
