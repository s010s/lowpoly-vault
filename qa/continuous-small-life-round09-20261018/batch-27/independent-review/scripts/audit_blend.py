import bpy, bmesh, sys, json, math, hashlib
from pathlib import Path

blend_path=Path(sys.argv[sys.argv.index('--')+1]).resolve()
glb_path=Path(sys.argv[sys.argv.index('--')+2]).resolve()
asset_id=sys.argv[sys.argv.index('--')+3]
output_path=Path(sys.argv[sys.argv.index('--')+4]).resolve()

def scan(objects):
    rows=[]; points=[]; triangles=0; evaluated_vertices=0
    deps=bpy.context.evaluated_depsgraph_get()
    for obj in objects:
        if obj.type!='MESH': continue
        ev=obj.evaluated_get(deps); mesh=ev.to_mesh()
        try:
            mesh.calc_loop_triangles()
            triangles+=len(mesh.loop_triangles); evaluated_vertices+=len(mesh.vertices)
            bm=bmesh.new(); bm.from_mesh(mesh)
            boundary=sum(e.is_boundary for e in bm.edges)
            nonmanifold=sum(not e.is_manifold and not e.is_boundary for e in bm.edges)
            area_bad=sum(not math.isfinite(f.calc_area()) or f.calc_area()<=1e-15 for f in bm.faces)
            signed_volume=bm.calc_volume(signed=True) if bm.faces else 0.0
            bm.free()
            bad_normals=sum(not all(math.isfinite(float(v.normal[i])) for i in range(3)) for v in mesh.vertices)
            world=ev.matrix_world
            coords=[world @ v.co for v in mesh.vertices]
            points.extend(coords)
            rows.append({'name':obj.name,'authored_vertices':len(obj.data.vertices),'evaluated_vertices':len(mesh.vertices),'triangles':len(mesh.loop_triangles),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'zero_or_nonfinite_area_faces':area_bad,'nonfinite_vertex_normals':bad_normals,'signed_volume_m3':signed_volume,'world_dimensions_m':list(obj.dimensions)})
        finally: ev.to_mesh_clear()
    if not points: return rows,triangles,evaluated_vertices,None
    bounds={'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)]}
    bounds['size']=[bounds['max'][i]-bounds['min'][i] for i in range(3)]
    return rows,triangles,evaluated_vertices,bounds

blend_sha=hashlib.sha256(blend_path.read_bytes()).hexdigest()
glb_sha=hashlib.sha256(glb_path.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(blend_path),load_ui=False,use_scripts=False)
export=bpy.data.collections.get('EXPORT')
if export is None: raise RuntimeError('missing EXPORT collection')
root=bpy.data.objects.get(asset_id)
root_identity=bool(root and all(abs(root.matrix_world[r][c]-(1.0 if r==c else 0.0))<1e-6 for r in range(4) for c in range(4)))
source_parts,source_triangles,source_evaluated_vertices,source_bounds=scan(list(export.all_objects))
source_camera_light_count=sum(o.type in {'CAMERA','LIGHT'} for o in bpy.data.objects)
source_unit_scale=bpy.context.scene.unit_settings.scale_length
source_unit_system=bpy.context.scene.unit_settings.system
source_version=bpy.app.version_string

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb_path))
glb_meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
glb_parts,glb_triangles,glb_evaluated_vertices,glb_bounds=scan(glb_meshes)
bounds_match=bool(source_bounds and glb_bounds and all(abs(source_bounds[k][i]-glb_bounds[k][i])<=1e-4 for k in ('min','max') for i in range(3)))
report={'asset_id':asset_id,'blend_sha256':blend_sha,'glb_sha256':glb_sha,'blender_version':source_version,'source_unit_system':source_unit_system,'source_unit_scale_length':source_unit_scale,'root_found':bool(root),'root_identity':root_identity,'source_cameras_lights':source_camera_light_count,'source_triangles':source_triangles,'source_authored_vertices':sum(x['authored_vertices'] for x in source_parts),'source_evaluated_vertices':source_evaluated_vertices,'glb_triangles_after_reimport':glb_triangles,'glb_evaluated_vertices_after_reimport':glb_evaluated_vertices,'triangles_match':source_triangles==glb_triangles,'bounds_match_within_1e-4_m':bounds_match,'source_bounds_blender_m':source_bounds,'glb_bounds_after_blender_import_m':glb_bounds,'source_parts':source_parts,'glb_parts':glb_parts,'source_parts_all_closed_no_degenerate_finite_normals':all(x['boundary_edges']==0 and x['nonmanifold_edges']==0 and x['zero_or_nonfinite_area_faces']==0 and x['nonfinite_vertex_normals']==0 for x in source_parts)}
output_path.parent.mkdir(parents=True,exist_ok=True)
output_path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
