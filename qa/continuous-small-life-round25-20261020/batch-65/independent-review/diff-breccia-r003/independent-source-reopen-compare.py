import bpy,bmesh,sys,json,hashlib,struct,os
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]; out_path=args[0]; blend_paths=args[1:]
def digest(b):return hashlib.sha256(b).hexdigest()
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=path)
 scene=bpy.context.scene; deps=bpy.context.evaluated_depsgraph_get(); objects={}; mats={}
 def material_data(m):
  nodes=[]
  if m.use_nodes and m.node_tree:
   for n in m.node_tree.nodes:
    inputs={}
    for s in n.inputs:
     if not s.is_linked and hasattr(s,'default_value'):
      v=s.default_value
      try: inputs[s.name]=list(v) if hasattr(v,'__iter__') and not isinstance(v,str) else float(v) if isinstance(v,(float,int)) else str(v)
      except: inputs[s.name]=str(v)
    nodes.append({'type':n.bl_idname,'name':n.name,'inputs':inputs})
  return {'name':m.name,'diffuse_color':list(m.diffuse_color),'use_nodes':m.use_nodes,'surface_render_method':getattr(m,'surface_render_method',None),'nodes':nodes}
 for m in bpy.data.materials:mats[m.name]=material_data(m)
 total_tri=0; total_volume=0.0;parts=[]
 for ob in sorted([o for o in bpy.data.objects if o.type=='MESH'],key=lambda x:x.name):
  me=ob.data; verts=[tuple(float(c) for c in v.co) for v in me.vertices]; faces=[list(p.vertices) for p in me.polygons]; mids=[int(p.material_index) for p in me.polygons]; slots=[s.material.name if s.material else None for s in ob.material_slots]
  canonical=json.dumps({'verts':verts,'faces':faces,'material_indices':mids,'slots':slots},separators=(',',':'),sort_keys=True).encode()
  eo=ob.evaluated_get(deps); em=eo.to_mesh();bm=bmesh.new();bm.from_mesh(em); tris=sum(max(0,len(p.vertices)-2) for p in em.polygons); vol=abs(bm.calc_volume(signed=True)) if bm.faces else 0.; boundary=sum(e.is_boundary for e in bm.edges);nonman=sum(not e.is_manifold for e in bm.edges)
  world=[tuple(float(x) for x in (ob.matrix_world @ v.co)) for v in em.vertices];lo=[min(v[i] for v in world) for i in range(3)];hi=[max(v[i] for v in world) for i in range(3)]
  parts.append({'name':ob.name,'vertices':len(me.vertices),'polygons':len(me.polygons),'triangles':tris,'local_geom_sha256':digest(canonical),'local_bounds':{'min':[min(v[i] for v in verts) for i in range(3)],'max':[max(v[i] for v in verts) for i in range(3)]},'world_bounds':{'min':lo,'max':hi},'material_slots':slots,'boundary_edges':int(boundary),'nonmanifold_edges':int(nonman),'volume_m3':vol})
  total_tri+=tris;total_volume+=vol;bm.free();eo.to_mesh_clear()
 root=bpy.context.view_layer.layer_collection.collection
 return {'path':path,'blend_sha256':digest(open(path,'rb').read()),'blender_version':bpy.app.version_string,'scene_objects':len(bpy.data.objects),'parts':parts,'triangles':total_tri,'volume_m3':total_volume,'materials':mats,'material_definitions_sha256':digest(json.dumps(mats,sort_keys=True,separators=(',',':')).encode()),'status':'pass' if parts and all(p['boundary_edges']==0 and p['nonmanifold_edges']==0 and p['volume_m3']>0 for p in parts) else 'fail'}
res=[snapshot(p) for p in blend_paths]
by=[{p['name']:p for p in r['parts']} for r in res]
object_names=sorted(set(by[0])|set(by[1]));diff=[n for n in object_names if n not in by[0] or n not in by[1] or by[0][n]['local_geom_sha256']!=by[1][n]['local_geom_sha256']]
result={'read_only':True,'results':res,'comparison':{'object_names_equal':set(by[0])==set(by[1]),'changed_object_geom_hashes':diff,'host_object':'coherent_angular_matrix_outcrop','host_geometry_exactly_equal':by[0].get('coherent_angular_matrix_outcrop',{}).get('local_geom_sha256')==by[1].get('coherent_angular_matrix_outcrop',{}).get('local_geom_sha256'),'material_defs_exactly_equal':res[0]['material_definitions_sha256']==res[1]['material_definitions_sha256'],'materials_by_name_equal':res[0]['materials']==res[1]['materials'],'renderer_not_part_of_source_comparison':True}}
open(out_path,'w').write(json.dumps(result,indent=2)+'\n')
print(json.dumps({'blender':bpy.app.version_string,'results':[{'blend_sha256':r['blend_sha256'],'triangles':r['triangles'],'volume_m3':r['volume_m3'],'bounds':[p['world_bounds'] for p in r['parts'] if p['name']=='coherent_angular_matrix_outcrop'],'status':r['status']} for r in res], 'comparison':result['comparison']},indent=2))
