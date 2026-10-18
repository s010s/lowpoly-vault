# SPDX-License-Identifier: MIT
"""Read-only exact-float edge winding and shape/palette preservation checks."""
import sys,json,hashlib,math
from pathlib import Path
from collections import defaultdict,Counter
sys.path.insert(0,str(Path(__file__).parent))
from qa_glb import read_glb,accessor_values

def decode(path):
    d,b,raw=read_glb(path);faces=[];edges=defaultdict(list)
    for m in d['meshes']:
        for p in m['primitives']:
            points=accessor_values(d,b,p['attributes']['POSITION']);indices=[x[0] for x in accessor_values(d,b,p['indices'])]
            for k in range(0,len(indices),3):
                tri=tuple(tuple(points[i]) for i in indices[k:k+3]);fi=len(faces);faces.append(tri)
                for a,z in zip(tri,tri[1:]+tri[:1]):edges[tuple(sorted((a,z)))].append((fi,1 if a<z else -1))
    adjacency=defaultdict(set)
    for es in edges.values():
        if len(es)==2:adjacency[es[0][0]].add(es[1][0]);adjacency[es[1][0]].add(es[0][0])
    unvisited=set(range(len(faces)));vols=[]
    while unvisited:
        todo=[unvisited.pop()];part=[]
        while todo:
            f=todo.pop();part.append(f)
            for n in adjacency[f]:
                if n in unvisited:unvisited.remove(n);todo.append(n)
        vol=0
        for f in part:
            a,z,c=faces[f]
            vol+=(a[0]*(z[1]*c[2]-z[2]*c[1])+a[1]*(z[2]*c[0]-z[0]*c[2])+a[2]*(z[0]*c[1]-z[1]*c[0]))/6
        vols.append(vol)
    return d,faces,edges,vols,hashlib.sha256(raw).hexdigest()

def audit(new,old):
    d,fs,es,vs,sha=decode(new);od,ofs,_,_,oldsha=decode(old)
    bad=sum(len(e)==2 and e[0][1]==e[1][1] for e in es.values())
    bounds=lambda f:[[min(p[i] for t in f for p in t) for i in range(3)],[max(p[i] for t in f for p in t) for i in range(3)]]
    # Triangulation diagonals may change because reversed source ngon order is repaired;
    # preserve the exact vertex positions, bounds, counts, and material PBR values.
    result={'sha256':sha,'previous_sha256':oldsha,'triangles':len(fs),'geometric_edges':len(es),
      'boundary_edges':sum(len(e)==1 for e in es.values()),'edges_more_than_two_faces':sum(len(e)>2 for e in es.values()),
      'shared_edges_with_same_direction':bad,'closed_components':len(vs),'negative_volume_components':sum(v<0 for v in vs),
      'component_signed_volumes_m3':vs,'exact_vertex_position_set_unchanged':set(p for t in fs for p in t)==set(p for t in ofs for p in t),
      'bounds_unchanged':bounds(fs)==bounds(ofs),'triangles_unchanged':len(fs)==len(ofs),
      'materials_unchanged':d['materials']==od['materials'],'materials_double_sided':[m.get('doubleSided',False) for m in d['materials']],
      'scope':'Geometric edge orientation and repair preservation; independent graphics/visual acceptance separate.'}
    result['status']='pass' if not bad and not result['boundary_edges'] and not result['edges_more_than_two_faces'] and not result['negative_volume_components'] and all(result[k] for k in ('exact_vertex_position_set_unchanged','bounds_unchanged','triangles_unchanged','materials_unchanged')) else 'fail'
    return result

if __name__=='__main__':
    new,old=map(Path,sys.argv[1:3]);r=audit(new,old);print(json.dumps(r,indent=2));sys.exit(0 if r['status']=='pass' else 1)
