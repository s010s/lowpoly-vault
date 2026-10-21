import bpy, sys, json, pathlib, hashlib, datetime, os, collections
from mathutils.bvhtree import BVHTree
R=pathlib.Path('/workspace/shared/lowpoly-batch77-ernietta-repair-20261020')
A=R/'production/batch77-ernietta-repair/assets/ernietta/r012'
O=pathlib.Path('/workspace/shared/lowpoly-batch77-20261020/production/small-life-batch77/assets/ernietta/r004')
Q=pathlib.Path('/workspace/shared/lowpoly-ernietta-r012-independent-qa-20261020')
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
before={str(p):H(p) for p in [A/'source.blend',A/'model.glb',O/'source.blend',O/'model.glb']}
def inspect(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False)
 col=bpy.data.collections['EXPORT'];objs=[o for o in col.all_objects if o.type=='MESH'];assert len(objs)==1
 o=objs[0];me=o.data;me.calc_loop_triangles();vs=[tuple(v.co) for v in me.vertices];world=[o.matrix_world@v.co for v in me.vertices];tris=[tuple(t.vertices) for t in me.loop_triangles]
 mats=[]
 for m in o.data.materials:
  nodes=[]
  if m.node_tree:
   for n in m.node_tree.nodes:
    vals={}
    for x in n.inputs:
     if hasattr(x,'default_value'):
      v=x.default_value
      try:v=list(v)
      except TypeError:pass
      if isinstance(v,(int,float,str,bool,list)):vals[x.name]=v
    nodes.append({'type':n.type,'inputs':vals})
  mats.append({'name':m.name,'diffuse':list(m.diffuse_color),'metallic':m.metallic,'roughness':m.roughness,'backface_culling':m.use_backface_culling,'nodes':nodes})
 dg=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(dg);em=ev.to_mesh();evcount=len(em.vertices);ev.to_mesh_clear()
 return {'vertices':vs,'world':world,'triangles':tris,'materials':mats,'location':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale),'world_matrix':[list(row) for row in o.matrix_world],'evaluated_vertices':evcount,'collection_objects':[{'name':x.name,'type':x.type,'location':list(x.location),'rotation':list(x.rotation_euler),'scale':list(x.scale)} for x in col.all_objects]},col,o
old,_,_=inspect(O/'source.blend');new,col,obj=inspect(A/'source.blend')
unchanged=[i for i in range(2520) if old['vertices'][i]==new['vertices'][i]]
changed=[i for i in range(2520) if old['vertices'][i]!=new['vertices'][i]]
assert all(i in unchanged for i in range(720,2520));assert old['vertices'][-1]==new['vertices'][-1]
assert old['materials']==new['materials'];assert old['rotation']==new['rotation'] and old['scale']==new['scale']
assert old['triangles'][:4680]==new['triangles'][:4680]
edges=collections.Counter(tuple(sorted((t[i],t[(i+1)%3]))) for t in new['triangles'] for i in range(3))
adj=collections.defaultdict(set)
for a,b in edges:adj[a].add(b);adj[b].add(a)
unvisited=set(range(len(new['vertices'])));components=[]
while unvisited:
 todo=[unvisited.pop()];n=0
 while todo:
  i=todo.pop();n+=1
  for v in adj[i]&unvisited:unvisited.remove(v);todo.append(v)
 components.append(n)
world=new['world'];tris=new['triangles'];tree=BVHTree.FromPolygons(world,tris,all_triangles=True,epsilon=0)
pairs=sorted({tuple(sorted((a,b))) for a,b in tree.overlap(tree) if a!=b and not (set(tris[a])&set(tris[b]))})
areas=[(world[b]-world[a]).cross(world[c]-world[a]).length/2 for a,b,c in tris]
volume=sum(world[a].dot(world[b].cross(world[c]))/6 for a,b,c in tris)
bounds={'min':[min(v[i] for v in world) for i in range(3)],'max':[max(v[i] for v in world) for i in range(3)]};bounds['size']=[b-a for a,b in zip(bounds['min'],bounds['max'])]
seam=[new['vertices'][0]]+new['vertices'][2520:2609]+[new['vertices'][90]]
profile=[{'ring':r,'changed_vertices':sum(r*180<=i<(r+1)*180 for i in changed),'max_displacement_m':max(sum((old['vertices'][i][k]-new['vertices'][i][k])**2 for k in range(3))**.5 for i in range(r*180,(r+1)*180))} for r in range(14)]
mesh_json={'old_vertices':old['vertices'],'new_vertices':new['vertices'],'old_triangles':old['triangles'],'new_triangles':new['triangles']}
(Q/'source-mesh-diff-raw.json').write_text(json.dumps(mesh_json)+'\n')
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=json.loads((A/'metrics.json').read_text())['export_options'];opts['filepath']=str(Q/'reexport.glb')
bpy.ops.export_scene.gltf(**opts)
assert H(Q/'reexport.glb')==H(A/'model.glb');assert all(H(p)==h for p,h in before.items())
report={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'blender':bpy.app.version_string,'source_saved':False,'autoexec':False,'input_hashes_before':before,'input_hashes_unchanged':True,'reexport_sha256':H(Q/'reexport.glb'),'byte_identical_reexport':True,'authored_vertices':len(new['vertices']),'evaluated_vertices':new['evaluated_vertices'],'triangles':len(tris),'bounds_blender_m':bounds,'unchanged_upper_vertices':1800,'unchanged_cavity_floor_center':True,'changed_existing_vertices_count':len(changed),'changed_existing_vertices_minmax':[min(changed),max(changed)],'per_ring_diff':profile,'upper_and_side_connectivity_unchanged_triangles':4680,'old_source_vertex_count':len(old['vertices']),'new_source_vertex_count':len(new['vertices']),'removed_old_bottom_center_index':2520,'added_join_chain_vertices':89,'material_nodes_equal':True,'rotation_and_scale_equal':True,'old_ground_translation':old['location'],'new_ground_translation':new['location'],'mesh_components':components,'boundary_nonmanifold_edges':sum(v!=2 for v in edges.values()),'nonadjacent_bvh_intersections':len(pairs),'intersection_examples':pairs[:30],'min_triangle_area_m2':min(areas),'signed_volume_m3':volume,'seam_chain_bounds_authored_m':{'min':[min(v[i] for v in seam) for i in range(3)],'max':[max(v[i] for v in seam) for i in range(3)]},'seam_center_max_recess_y_m':max(new['vertices'][2520+i-1][1]-(new['vertices'][i][1]+new['vertices'][180-i][1])/2 for i in range(1,90)),'old_objects':old['collection_objects'],'new_objects':new['collection_objects'],'limitations':'BVH excludes shared-vertex adjacency; no universal absence proof at every tolerance. Source coordinates compared before normal grounding. No GPU or scene render.'}
assert not report['boundary_nonmanifold_edges'] and not pairs and len(components)==1 and min(areas)>0
(Q/'reopen-diff.report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
