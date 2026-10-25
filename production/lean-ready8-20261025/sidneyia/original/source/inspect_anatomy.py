# SPDX-License-Identifier: MIT
"""Focused source counts and attachment graph; maker evidence, not factual approval."""
import bpy,json,sys,hashlib,re
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[sys.argv.index('--')+1]);src=Path(bpy.data.filepath)
objs=sorted([o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH'],key=lambda o:o.name)
records=[]
for o in objs:
 vs=[o.matrix_world@v.co for v in o.data.vertices];fs=[list(f.vertices) for f in o.data.polygons]
 records.append({'name':o.name,'vs':vs,'tree':BVHTree.FromPolygons(vs,fs),'lo':[min(p[i] for p in vs) for i in range(3)],'hi':[max(p[i] for p in vs) for i in range(3)]})
parent=list(range(len(records)))
def root(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
edges=[]
for i,a in enumerate(records):
 for j in range(i+1,len(records)):
  b=records[j]
  if any(a['lo'][k]>b['hi'][k]+1e-8 or b['lo'][k]>a['hi'][k]+1e-8 for k in range(3)):continue
  pairs=a['tree'].overlap(b['tree']);method='triangle-surface-overlap'
  connected=bool(pairs)
  if not connected:
   for inner,outer in [(a,b),(b,a)]:
    for p in inner['vs'][::max(1,len(inner['vs'])//12)]:
     if all(outer['lo'][k]-1e-8<=p[k]<=outer['hi'][k]+1e-8 for k in range(3)):
      near,n,idx,dist=outer['tree'].find_nearest(p)
      if near is not None and (dist<1e-7 or (p-near).dot(n)<-1e-8):connected=True;method='contained-vertex-nearest-oriented-surface';break
    if connected:break
  if connected:
   parent[root(j)]=root(i);edges.append({'a':a['name'],'b':b['name'],'method':method,'surface_overlap_triangle_pairs':len(pairs)})
components={}
for i,r in enumerate(records):components.setdefault(str(root(i)),[]).append(r['name'])
names=[o.name for o in objs]
counts={'tergites':len([n for n in names if re.fullmatch(r'tergite-\d\d',n)]),'cephalic_limbs':len([n for n in names if re.fullmatch(r'cephalic-\d\d-[LR]-walking-branch',n)]),'trunk_limbs':len([n for n in names if re.fullmatch(r'trunk-\d\d-[LR]-walking-branch',n)]),'abdominal_rings':len([n for n in names if n.startswith('abdominal-ring-')]),'tail_flaps':len([n for n in names if n.startswith('tail-flap-')]),'telson':names.count('central-telson'),'eyes':len([n for n in names if re.fullmatch(r'eye--?1',n)]),'gill_blades':len([n for n in names if '-gill-blade-' in n]),'antenna_segments':len([n for n in names if n.startswith('antenna-')])}
expected={'tergites':9,'cephalic_limbs':6,'trunk_limbs':18,'abdominal_rings':2,'tail_flaps':2,'telson':1,'eyes':2,'gill_blades':54,'antenna_segments':26}
assert counts==expected,(counts,expected)
bodyparts=[o for o in objs if o.name=='cephalic-shield' or o.name.startswith('tergite-') or o.name.startswith('abdominal-ring-') or o.name=='central-telson' or o.name.startswith('tail-flap-')]
pts=[o.matrix_world@v.co for o in bodyparts for v in o.data.vertices]
bounds={'min':[min(v[i] for v in pts) for i in range(3)],'max':[max(v[i] for v in pts) for i in range(3)]};bounds['size']=[bounds['max'][i]-bounds['min'][i] for i in range(3)]
report={'status':'PASS' if len(components)==1 else 'REVIEW_REQUIRED','blend_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'counts':counts,'source_mesh_count':len(objs),'exoskeleton_bounds_blender_m':bounds,'attachment_graph_components':list(components.values()),'attachment_edges':edges,'methods':['Broadphase AABB, exact source triangle overlap','If no surface overlap, sampled vertex containment using nearest oriented closed surface'],'limitations':'Maker geometric attachment screen, not independent factual or visual approval. Containment is an oriented-nearest-surface screen, not a general watertight Boolean proof. Counts are source mesh identities, not a fossil-exact joint or lamella claim.'}
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'counts':counts,'components':list(components.values()) if len(components)>1 else 1,'edges':len(edges)}))
