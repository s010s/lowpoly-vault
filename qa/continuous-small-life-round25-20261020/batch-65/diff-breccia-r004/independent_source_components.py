import bpy,bmesh,sys,json,hashlib,math
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
out_path=args[0]; paths=args[1:]
def sha(b): return hashlib.sha256(b).hexdigest()
def qpt(v): return tuple(round(float(x),5) for x in v)
def comp_digest(coords,faces):
    tris=[]
    for f in faces:
        vs=[qpt(coords[i]) for i in f]
        for k in range(1,len(vs)-1): tris.append(tuple(sorted((vs[0],vs[k],vs[k+1]))))
    tris.sort()
    return sha(json.dumps(tris,separators=(',',':')).encode())
def comp_measure(coords,faces):
    signed=0.0
    for f in faces:
        if len(f)<3: continue
        a=Vector(coords[f[0]])
        for k in range(1,len(f)-1):
            b=Vector(coords[f[k]]);c=Vector(coords[f[k+1]])
            signed += a.dot(b.cross(c))/6.0
    return abs(signed)
def inspect(path):
    bpy.ops.wm.open_mainfile(filepath=path)
    dg=bpy.context.evaluated_depsgraph_get()
    meshes=sorted([o for o in bpy.data.objects if o.type=='MESH'],key=lambda o:o.name)
    host=next(o for o in meshes if o.name=='coherent_angular_matrix_outcrop')
    h_inv=host.matrix_world.inverted()
    result={'path':path,'blend_sha256':sha(open(path,'rb').read()),'blender_version':bpy.app.version_string,'scene_objects':len(bpy.data.objects),'material_names':sorted(m.name for m in bpy.data.materials),'parts':[],'components':[],'module_bounds_world':None}
    all_world=[]; total_tri=0
    for ob in meshes:
        eo=ob.evaluated_get(dg); em=eo.to_mesh(); bm=bmesh.new(); bm.from_mesh(em); bm.verts.ensure_lookup_table(); bm.verts.index_update()
        coords_local=[tuple(float(c) for c in v.co) for v in em.vertices]
        coords_rel=[tuple(h_inv @ (ob.matrix_world @ Vector(v))) for v in coords_local]
        faces=[list(p.vertices) for p in em.polygons]
        tri=sum(max(0,len(f)-2) for f in faces); total_tri+=tri
        boundary=sum(e.is_boundary for e in bm.edges); nonman=sum(not e.is_manifold for e in bm.edges)
        obj_world=[ob.matrix_world @ Vector(v) for v in coords_local]
        if obj_world: all_world.extend(obj_world)
        vol=abs(bm.calc_volume(signed=True)) if bm.faces else 0.
        local_geom=sha(json.dumps({'vertices':[[round(float(c),9) for c in v] for v in coords_local],'faces':faces,'material_indices':[int(p.material_index) for p in em.polygons],'slots':[s.material.name if s.material else None for s in ob.material_slots]},sort_keys=True,separators=(',',':')).encode())
        part={'name':ob.name,'local_geometry_sha256':local_geom,'material_slots':[s.material.name if s.material else None for s in ob.material_slots],'vertices':len(em.vertices),'polygons':len(em.polygons),'triangles':tri,'boundary_edges':int(boundary),'nonmanifold_edges':int(nonman),'volume_m3':float(vol),'matrix_world':[[float(ob.matrix_world[r][c]) for c in range(4)] for r in range(4)],'bounds_world':{'min':[min(v[i] for v in obj_world) for i in range(3)],'max':[max(v[i] for v in obj_world) for i in range(3)]} if obj_world else None}
        result['parts'].append(part)
        # Split the indexed evaluated topology into disconnected vertex/edge components.
        adj=[set() for _ in coords_local]
        used=set()
        for f in faces:
            for v in f: used.add(v)
            for i,a in enumerate(f): adj[a].add(f[(i+1)%len(f)]); adj[a].add(f[(i-1)%len(f)])
        unseen=set(used); comp_num=0
        while unseen:
            seed=unseen.pop(); stack=[seed]; vids={seed}
            while stack:
                x=stack.pop()
                for y in adj[x]:
                    if y in unseen: unseen.remove(y);vids.add(y);stack.append(y)
            cfaces=[f for f in faces if f and f[0] in vids]
            # Count all faces entirely belonging to this component (indices form disjoint components).
            cfaces=[f for f in faces if f and all(i in vids for i in f)]
            remap={v:i for i,v in enumerate(sorted(vids))}; ccoords=[coords_rel[v] for v in sorted(vids)]
            lfaces=[[remap[v] for v in f] for f in cfaces]
            cworld=[tuple(coords_rel[v]) for v in vids]
            centroid=[sum(p[i] for p in cworld)/len(cworld) for i in range(3)]
            centered=[[p[i]-centroid[i] for i in range(3)] for p in ccoords]
            cb=[(min(p[i] for p in cworld),max(p[i] for p in cworld)) for i in range(3)]
            comp_tri=sum(max(0,len(f)-2) for f in lfaces)
            # BMesh connected subgraph edge QA.
            bverts=[bm.verts[v] for v in vids]
            be={e for v in bverts for e in v.link_edges if e.verts[0].index in vids and e.verts[1].index in vids}
            boundary_c=sum(e.is_boundary for e in be);nonman_c=sum(not e.is_manifold for e in be)
            result['components'].append({'object':ob.name,'component_local_index':comp_num,'min_vertex_index':min(vids),'vertices':len(vids),'triangles':comp_tri,'volume_m3':comp_measure(ccoords,lfaces),'boundary_edges':int(boundary_c),'nonmanifold_edges':int(nonman_c),'centroid_in_host_local':centroid,'bounds_in_host_local':[[a,b] for a,b in cb],'geometry_sha256':comp_digest(centered,lfaces)})
            comp_num+=1
        bm.free();eo.to_mesh_clear()
    if all_world:
        result['module_bounds_world']={'min':[min(v[i] for v in all_world) for i in range(3)],'max':[max(v[i] for v in all_world) for i in range(3)]}
    result['triangles_total']=total_tri
    result['component_count']=len(result['components'])
    result['status']='pass' if result['components'] and all(c['boundary_edges']==0 and c['nonmanifold_edges']==0 and c['volume_m3']>0 for c in result['components']) else 'fail'
    return result
res=[inspect(p) for p in paths]
# Match source mesh disconnected prisms by their preserved vertex-order blocks within each aggregate mesh object.
pairs=[]
for obj in sorted(set(c['object'] for c in res[0]['components'])|set(c['object'] for c in res[1]['components'])):
 a=sorted([c for c in res[0]['components'] if c['object']==obj],key=lambda c:c['min_vertex_index']);b=sorted([c for c in res[1]['components'] if c['object']==obj],key=lambda c:c['min_vertex_index'])
 if len(a)!=len(b): continue
 for ca,cb in zip(a,b):
  dist=sum((x-y)**2 for x,y in zip(ca['centroid_in_host_local'],cb['centroid_in_host_local']))**.5
  pairs.append({'object':obj,'old_min_vertex_index':ca['min_vertex_index'],'new_min_vertex_index':cb['min_vertex_index'],'old_centroid':ca['centroid_in_host_local'],'new_centroid':cb['centroid_in_host_local'],'centroid_distance_m':dist,'old_sha256':ca['geometry_sha256'],'new_sha256':cb['geometry_sha256'],'unchanged_component_geometry':ca['geometry_sha256']==cb['geometry_sha256'],'old_volume_m3':ca['volume_m3'],'new_volume_m3':cb['volume_m3'],'old_triangles':ca['triangles'],'new_triangles':cb['triangles'],'old_closed':ca['boundary_edges']==0 and ca['nonmanifold_edges']==0,'new_closed':cb['boundary_edges']==0 and cb['nonmanifold_edges']==0})
open(out_path,'w').write(json.dumps({'method':'Independent Blender 4.3.2 read-only file reopen. Evaluated meshes; BMesh edge-manifold checks; connected-component flood fill over evaluated mesh indices; per-component volume from signed triangle tetrahedra; normalized component geometry hash from sorted rounded triangle coordinates in host-local frame. Stable component matching by minimum source vertex index within each aggregate mesh object; component shape signatures are translation-invariant and rounded to 10 microns. No source saved.','results':res,'component_pairs':pairs,'comparison':{'counts_match':len(res[0]['components'])==len(res[1]['components']),'old_count':len(res[0]['components']),'new_count':len(res[1]['components']),'changed_geometry_components':sum(not x['unchanged_component_geometry'] for x in pairs),'unchanged_geometry_components':sum(x['unchanged_component_geometry'] for x in pairs),'max_centroid_match_distance_m':max((x['centroid_distance_m'] for x in pairs),default=0),'all_components_closed_nonzero_both':all(x['old_closed'] and x['new_closed'] and x['old_volume_m3']>0 and x['new_volume_m3']>0 for x in pairs)}},indent=2)+'\n')
print(json.dumps({'blender':bpy.app.version_string,'results':[{'path':r['path'],'triangles_total':r['triangles_total'],'component_count':r['component_count'],'status':r['status'],'module_bounds_world':r['module_bounds_world'],'parts':[{k:p[k] for k in ('name','vertices','triangles','boundary_edges','nonmanifold_edges','volume_m3','matrix_world','bounds_world')} for p in r['parts']]} for r in res],'comparison':{'counts_match':len(res[0]['components'])==len(res[1]['components']),'old_count':len(res[0]['components']),'new_count':len(res[1]['components']),'changed_geometry_components':sum(not x['unchanged_component_geometry'] for x in pairs),'unchanged_geometry_components':sum(x['unchanged_component_geometry'] for x in pairs),'max_centroid_match_distance_m':max((x['centroid_distance_m'] for x in pairs),default=0),'all_components_closed_nonzero_both':all(x['old_closed'] and x['new_closed'] and x['old_volume_m3']>0 and x['new_volume_m3']>0 for x in pairs)}},indent=2))
