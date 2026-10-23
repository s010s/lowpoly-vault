# SPDX-License-Identifier: MIT
"""Inspect actual .blend topology and exact triangle intersections (not quality approval)."""
import bpy,bmesh,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
args=sys.argv[sys.argv.index('--')+1:]; src=Path(args[0]); out=Path(args[1])
bpy.ops.wm.open_mainfile(filepath=str(src))
objs=[o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH']
reports=[]
def hit(p,q,a,b,c):
    # Moller-Trumbore finite segment test. Coplanar contacts are separately
    # bounded by the orientable manifold check; this test is not a solid-union proof.
    d=q-p;e1=b-a;e2=c-a;h=d.cross(e2);det=e1.dot(h)
    if abs(det)<1e-17: return False
    f=1/det;s=p-a;u=f*s.dot(h)
    if not 1e-7<u<1-1e-7: return False
    vv=d.dot(s.cross(e1))*f
    if not 1e-7<vv or not u+vv<1-1e-7: return False
    t=e2.dot(s.cross(e1))*f
    return 1e-7<t<1-1e-7
for o in objs:
    m=o.data;m.calc_loop_triangles();v=[o.matrix_world@x.co for x in m.vertices];tris=[tuple(t.vertices) for t in m.loop_triangles]
    tree=BVHTree.FromPolygons(v,tris,all_triangles=True,epsilon=0)
    candidates={(min(a,b),max(a,b)) for a,b in tree.overlap(tree) if a!=b and not set(tris[a])&set(tris[b])}
    intersections=[]
    for a,b in candidates:
        aa=[v[i] for i in tris[a]];bb=[v[i] for i in tris[b]]
        if any(hit(aa[i],aa[(i+1)%3],*bb) for i in range(3)) or any(hit(bb[i],bb[(i+1)%3],*aa) for i in range(3)): intersections.append([a,b])
    bm=bmesh.new();bm.from_mesh(m);bm.normal_update()
    volume=bm.calc_volume(signed=True); boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges)
    inconsistent=sum(not e.is_contiguous for e in bm.edges)
    seen=set();components=0
    for vv in bm.verts:
        if vv in seen: continue
        components+=1; stack=[vv];seen.add(vv)
        while stack:
            p=stack.pop()
            for e in p.link_edges:
                w=e.other_vert(p)
                if w not in seen:seen.add(w);stack.append(w)
    report={'name':o.name,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'euler_characteristic':len(bm.verts)-len(bm.edges)+len(bm.faces),'connected_components':components,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'inconsistent_oriented_edges':inconsistent,'signed_volume_m3':volume,'bvh_nonadjacent_candidates':len(candidates),'proper_triangle_crossings':len(intersections),'crossing_examples':intersections[:20]}
    bm.free();reports.append(report)
status='pass' if all(r['connected_components']==1 and r['boundary_edges']==0 and r['nonmanifold_edges']==0 and r['inconsistent_oriented_edges']==0 and r['signed_volume_m3']>0 and r['proper_triangle_crossings']==0 for r in reports) else 'fail'
result={'status':status,'blend_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(src.with_suffix('.glb').read_bytes()).hexdigest(),'parts':reports,'method':'Actual source mesh manifold/orientation/connectivity/volume and BVH candidate + finite segment triangle cross test','limits':'Not independent visual or factual acceptance. Adjacent triangles and coplanar contact are not counted as proper crossings.'}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if status!='pass': raise RuntimeError('Geometry check failed')
