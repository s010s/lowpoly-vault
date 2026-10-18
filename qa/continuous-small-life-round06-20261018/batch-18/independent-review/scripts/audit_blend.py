import bpy, bmesh, sys, json, math, hashlib
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]
blend=Path(args[0]); glb=Path(args[1]); asset=args[2]

def scan_mesh_objects(objects):
    out=[]; bounds=[]; tri_count=0
    deps=bpy.context.evaluated_depsgraph_get()
    for obj in objects:
        if obj.type!='MESH': continue
        ev=obj.evaluated_get(deps); mesh=ev.to_mesh()
        try:
            mesh.calc_loop_triangles()
            tri_count += len(mesh.loop_triangles)
            bm=bmesh.new(); bm.from_mesh(mesh)
            boundary=sum(e.is_boundary for e in bm.edges)
            nonmanifold=sum(not e.is_manifold for e in bm.edges)
            bad_area=sum(not math.isfinite(f.calc_area()) or f.calc_area()<=1e-15 for f in bm.faces)
            nonfinite_normals=sum(not all(math.isfinite(v.normal[i]) for i in range(3)) for v in bm.verts)
            volume=bm.calc_volume(signed=True) if bm.faces else 0
            bm.free()
            mat=ev.matrix_world
            coords=[mat @ v.co for v in mesh.vertices]
            if coords:
                mins=[min(p[i] for p in coords) for i in range(3)]; maxs=[max(p[i] for p in coords) for i in range(3)]
                bounds.append((mins,maxs))
            out.append({'name':obj.name,'vertices':len(mesh.vertices),'triangles':len(mesh.loop_triangles),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'bad_area_faces':bad_area,'nonfinite_vertex_normals':nonfinite_normals,'signed_volume_m3':volume,'matrix_scale':list(ev.matrix_world.to_scale()),'local_dimensions':list(obj.dimensions)})
        finally:
            ev.to_mesh_clear()
    if not bounds: return out,tri_count,None
    return out,tri_count,{'min':[min(b[0][i] for b in bounds) for i in range(3)],'max':[max(b[1][i] for b in bounds) for i in range(3)]}

bpy.ops.wm.open_mainfile(filepath=str(blend), load_ui=False)
export=bpy.data.collections.get('EXPORT')
if export is None: raise RuntimeError('missing EXPORT collection')
source_objects=list(export.all_objects)
source_parts,source_tris,source_bounds=scan_mesh_objects(source_objects)
root=bpy.data.objects.get(asset)
source={'blend_sha256':hashlib.sha256(blend.read_bytes()).hexdigest(),'unit_scale_length':bpy.context.scene.unit_settings.scale_length,'root_found':root is not None,'root_world_matrix':[list(r) for r in root.matrix_world] if root else None,'part_count':len(source_parts),'parts':source_parts,'triangles':source_tris,'bounds_blender_m':source_bounds}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb))
glb_meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
glb_parts,glb_tris,glb_bounds=scan_mesh_objects(glb_meshes)
# glTF uses +Y up, while Blender source is Z-up with forward -Y.
converted=None
if source_bounds:
    mn=source_bounds['min']; mx=source_bounds['max']
    converted={'min':[mn[0],mn[2],mn[1]],'max':[mx[0],mx[2],mx[1]]}
# The Blender source Y axis is forward and GLB Z axis is forward, so axis conversion also reflects Y sign.
if source_bounds:
    mn=source_bounds['min'];mx=source_bounds['max']
    converted={'min':[mn[0],mn[2],-mx[1]],'max':[mx[0],mx[2],-mn[1]]}
reimport_bounds_match=all(abs(source_bounds[k][i]-glb_bounds[k][i])<=1e-4 for k in ('min','max') for i in range(3)) if source_bounds and glb_bounds else False
report={'asset_id':asset,'source':source,'glb':{'glb_sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'mesh_count':len(glb_meshes),'parts':glb_parts,'triangles':glb_tris,'bounds_blender_after_import_m':glb_bounds},'source_expected_glb_bounds_m':converted,'triangles_match':source_tris==glb_tris,'bounds_reimport_match_1e-4':reimport_bounds_match,'source_parts_all_closed_finite_positive':all(p['boundary_edges']==0 and p['nonmanifold_edges']==0 and p['bad_area_faces']==0 and p['nonfinite_vertex_normals']==0 and p['signed_volume_m3']>0 for p in source_parts)}
print(json.dumps(report,indent=2))
