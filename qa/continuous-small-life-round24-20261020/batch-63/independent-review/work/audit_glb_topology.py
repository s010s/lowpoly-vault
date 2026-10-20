from pathlib import Path
import sys, json, math, hashlib
repo=Path('/tmp/lowpoly-batch63-20261020'); sys.path.insert(0,str(repo/'scripts'))
from qa_glb import read_glb, accessor_values

def mesh_audit(doc,binary,mesh_idx):
    mesh=doc['meshes'][mesh_idx]
    verts=[]; tris=[]; per_prim=[]
    for pi,prim in enumerate(mesh.get('primitives',[])):
        attrs=prim['attributes']; pos=accessor_values(doc,binary,attrs['POSITION'])
        base=len(verts); verts.extend([tuple(map(float,v)) for v in pos])
        inds=accessor_values(doc,binary,prim['indices']) if 'indices' in prim else [(i,) for i in range(len(pos))]
        idx=[int(x[0]) for x in inds]
        mode=prim.get('mode',4)
        if mode!=4: raise ValueError(f'non-triangle primitive mode {mode}')
        if len(idx)%3: raise ValueError('index count not multiple of three')
        ts=[tuple(base+idx[i+j] for j in range(3)) for i in range(0,len(idx),3)]
        tris.extend(ts); per_prim.append({'primitive':pi,'vertices':len(pos),'triangles':len(ts),'material':prim.get('material'),'mode':mode})
    # Float32 positions are grouped by 1e-6 model units for topology closure. This is below the source-export bound tolerance (1e-4 m).
    welded={}; ids=[]
    for v in verts:
        k=tuple(round(c*1_000_000) for c in v)
        if k not in welded: welded[k]=len(welded)
        ids.append(welded[k])
    edge_uses={}; faces=set(); duplicate_faces=0; degenerate=0; min_area=float('inf'); areas=[]
    for t in tris:
        wt=tuple(ids[i] for i in t)
        if len(set(wt))<3: degenerate+=1; continue
        fk=tuple(sorted(wt))
        if fk in faces: duplicate_faces+=1
        faces.add(fk)
        a,b,c=(verts[i] for i in t)
        ab=[b[i]-a[i] for i in range(3)]; ac=[c[i]-a[i] for i in range(3)]
        cross=(ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0])
        area=0.5*math.sqrt(sum(x*x for x in cross)); areas.append(area); min_area=min(min_area,area)
        if area<=1e-14: degenerate+=1
        for u,v in ((wt[0],wt[1]),(wt[1],wt[2]),(wt[2],wt[0])):
            e=tuple(sorted((u,v))); edge_uses[e]=edge_uses.get(e,0)+1
    boundary=sum(n==1 for n in edge_uses.values()); nonmanifold=sum(n>2 for n in edge_uses.values())
    return {'mesh_index':mesh_idx,'name':mesh.get('name',f'mesh{mesh_idx}'),'primitives':len(per_prim),'primitive_stats':per_prim,'triangles':len(tris),'raw_position_vertices':len(verts),'welded_position_vertices':len(welded),'duplicate_position_vertices_removed':len(verts)-len(welded),'boundary_edges_after_weld':boundary,'nonmanifold_edges_after_weld':nonmanifold,'degenerate_triangles':degenerate,'duplicate_triangles':duplicate_faces,'min_nonzero_triangle_area':min_area if min_area!=float('inf') else None}
for path in map(Path,sys.argv[1:]):
    doc,bin,data=read_glb(path)
    summary={'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'asset_version':doc.get('asset',{}).get('version'),'nodes':len(doc.get('nodes',[])),'meshes':[mesh_audit(doc,bin,i) for i in range(len(doc.get('meshes',[])))]}
    dest=path.parent/'independent-topology.json'; dest.write_text(json.dumps(summary,indent=2)+'\n')
    print(path,[(m['name'],m['triangles'],m['boundary_edges_after_weld'],m['nonmanifold_edges_after_weld'],m['degenerate_triangles'],m['duplicate_triangles']) for m in summary['meshes']])
