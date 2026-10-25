# SPDX-License-Identifier: MIT
"""Bounded source-island attachment inspection, not independent visual acceptance."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[sys.argv.index('--')+1]);col=bpy.data.collections['EXPORT']
meshes={o.name:o for o in col.all_objects if o.type=='MESH'}
def tree(o,faces=None):
    return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],faces or [list(p.vertices) for p in o.data.polygons],all_triangles=False,epsilon=0)
def islands(o):
    m=o.data;adj=[set() for v in m.vertices]
    for e in m.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
    seen=set();groups=[]
    for i in range(len(m.vertices)):
        if i in seen:continue
        stack=[i];g=set();seen.add(i)
        while stack:
            v=stack.pop();g.add(v)
            for w in adj[v]-seen:seen.add(w);stack.append(w)
        groups.append([list(p.vertices) for p in m.polygons if p.vertices[0] in g])
    return groups
body=meshes['continuous-prostomium-20-trunk-segments-pygidium'];bodytree=tree(body);rows=[]
for name,o in meshes.items():
    if o==body:continue
    parent=body
    for side in ['left','right']:
        for row in ['dorsal','ventral']:
            if name==f'{side}-{row}-chaetal-fans':parent=meshes[f'{side}-{row}-parapodial-lobes']
        if name==f'{side}-head-chaetae':parent=meshes[f'{side}-head-parapodium']
    pt=bodytree if parent==body else tree(parent)
    counts=[len(tree(o,fs).overlap(pt)) for fs in islands(o)]
    rows.append({'part':name,'attachment_target':parent.name,'connected_islands':len(counts),'surface_intersection_pairs_per_island':counts,'all_islands_intersect_target':all(n>0 for n in counts)})
report={'status':'PASS' if all(r['all_islands_intersect_target'] for r in rows) else 'FAIL','blend_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'method':'Fresh .blend read. Exact vertex-connected source islands, zero-epsilon BVH triangle intersections with semantic attachment target. Positive pair count confirms intersecting surfaces; not a Boolean union, skin-quality or scientific-accuracy verdict.','parts':rows,'independent_qa':'PENDING'}
out.write_text(json.dumps(report,indent=2)+'\n')
if report['status']!='PASS':raise RuntimeError('An anatomical attachment lacks source surface intersection')
