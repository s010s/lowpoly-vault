import bpy, sys, json, hashlib
args=sys.argv[sys.argv.index('--')+1:]
out=args[0]
assets=args[1:]

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def material_info(mat):
 p=mat.node_tree.nodes.get('Principled BSDF') if mat and mat.use_nodes and mat.node_tree else None
 if p:
  base=p.inputs['Base Color'].default_value
  rough=p.inputs['Roughness'].default_value
  metal=p.inputs['Metallic'].default_value
 else:
  base=mat.diffuse_color; rough=mat.roughness; metal=mat.metallic
 return {'base_color_linear_rgba':[round(float(x),7) for x in base], 'roughness':round(float(rough),7), 'metallic':round(float(metal),7)}
def stats():
 objs=[o for o in bpy.context.scene.objects if o.type=='MESH']; deps=bpy.context.evaluated_depsgraph_get(); pts=[]; tris=0; verts=0; materials={}; bad=[]
 for o in objs:
  e=o.evaluated_get(deps); m=e.to_mesh(); m.calc_loop_triangles(); tris+=len(m.loop_triangles); verts+=len(m.vertices)
  pts.extend(o.matrix_world @ v.co for v in m.vertices)
  for idx in {poly.material_index for poly in m.polygons}:
   if idx < len(o.data.materials):
    mat=o.data.materials[idx]
    if mat: materials[mat.name]=material_info(mat)
  if o.matrix_world.to_3x3().determinant()<=0: bad.append(o.name)
  e.to_mesh_clear()
 if pts:
  lo=[min(p[i] for p in pts) for i in range(3)]; hi=[max(p[i] for p in pts) for i in range(3)]; dims=[hi[i]-lo[i] for i in range(3)]
 else: lo=hi=dims=None
 return {'mesh_objects':len(objs),'evaluated_vertices_sum':verts,'triangles':tris,'bounds_min_xyz':lo,'bounds_max_xyz':hi,'dimensions_xyz':dims,'materials':materials,'nonpositive_transform_determinants':bad}
rows=[]
for asset,blend,glb in zip(assets[0::3],assets[1::3],assets[2::3]):
 bpy.ops.wm.open_mainfile(filepath=blend); source=stats()
 bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=glb); imported=stats()
 close=all(abs(source['dimensions_xyz'][i]-imported['dimensions_xyz'][i])<1e-8 for i in range(3))
 names_equal=sorted(source['materials'])==sorted(imported['materials'])
 color_max=0.0; pbr_max=0.0
 for n in set(source['materials'])&set(imported['materials']):
  color_max=max(color_max,*[abs(source['materials'][n]['base_color_linear_rgba'][i]-imported['materials'][n]['base_color_linear_rgba'][i]) for i in range(4)])
  pbr_max=max(pbr_max,abs(source['materials'][n]['roughness']-imported['materials'][n]['roughness']),abs(source['materials'][n]['metallic']-imported['materials'][n]['metallic']))
 rows.append({'asset_id':asset,'source_blend_sha256':sha(blend),'glb_sha256':sha(glb),'source_blend':source,'independent_clean_glb_reimport':imported,'comparison':{'triangles_equal':source['triangles']==imported['triangles'],'dimensions_equal_within_1e-8':close,'materials_equal_by_name':names_equal,'max_linear_base_color_delta':round(color_max,8),'max_roughness_or_metallic_delta':round(pbr_max,8),'source_and_glb_have_no_nonpositive_mesh_transforms':not source['nonpositive_transform_determinants'] and not imported['nonpositive_transform_determinants']}})
with open(out,'w') as f: json.dump({'blender_version':bpy.app.version_string,'assets':rows},f,indent=2); f.write('\n')
print('Wrote independent reimport summary')
