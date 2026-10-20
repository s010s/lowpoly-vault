import bpy,json,math,os
from mathutils import Vector
objs=[o for o in bpy.context.scene.objects if o.type=='MESH']
dg=bpy.context.evaluated_depsgraph_get()
out={'file':bpy.data.filepath,'blender':bpy.app.version_string,'scene':bpy.context.scene.name,'objects':[],'totals':{'authored_vertices':0,'authored_faces':0,'evaluated_vertices':0,'evaluated_triangles':0,'materials':set()}}
for o in objs:
    mesh=o.data
    eval_o=o.evaluated_get(dg)
    em=eval_o.to_mesh()
    em.calc_loop_triangles()
    # bounds of evaluated mesh in world coordinates
    coords=[eval_o.matrix_world @ v.co for v in em.vertices]
    lo=[min(v[i] for v in coords) for i in range(3)] if coords else [0,0,0]
    hi=[max(v[i] for v in coords) for i in range(3)] if coords else [0,0,0]
    edge_use={e.index:0 for e in em.edges}
    for p in em.polygons:
      for ek in p.edge_keys:
        key=tuple(sorted(ek))
        # find edge id from vertices pair
        # build mapping below outside is cheaper but small
    edge_map={tuple(sorted(e.vertices)):e.index for e in em.edges}
    edge_use={i:0 for i in range(len(em.edges))}
    for p in em.polygons:
      for ek in p.edge_keys: edge_use[edge_map[tuple(sorted(ek))]]+=1
    boundary=sum(1 for n in edge_use.values() if n==1)
    nonmanifold=sum(1 for n in edge_use.values() if n>2)
    mats=[m.name if m else None for m in mesh.materials]
    out['objects'].append({'name':o.name,'vertices':len(mesh.vertices),'faces':len(mesh.polygons),'evaluated_vertices':len(em.vertices),'evaluated_triangles':len(em.loop_triangles),'bounds_world_min':lo,'bounds_world_max':hi,'materials':mats,'modifiers':[m.name+':'+m.type for m in o.modifiers],'boundary_edges':boundary,'nonmanifold_edges':nonmanifold})
    out['totals']['authored_vertices']+=len(mesh.vertices);out['totals']['authored_faces']+=len(mesh.polygons);out['totals']['evaluated_vertices']+=len(em.vertices);out['totals']['evaluated_triangles']+=len(em.loop_triangles);out['totals']['materials'].update(mats)
    eval_o.to_mesh_clear()
out['totals']['materials']=sorted(x for x in out['totals']['materials'] if x)
print('QA64_REOPEN_JSON='+json.dumps(out,sort_keys=True))
