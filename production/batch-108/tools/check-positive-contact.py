#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only positive-volume contact witnesses, rejecting boundary-only intersections.
Three oblique ray parities and nonzero nearest-surface distance independently check each point.
Sampling scales with actual local triangle edges, never a new minimum overlap acceptance range.
"""
import argparse,json,hashlib,sys,datetime
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source);before=src.read_bytes();bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);ct=json.loads(bpy.data.texts['BATCH108_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices];tris=[tuple(t.vertices) for t in o.data.loop_triangles];extent=max(max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3));epsilon=extent*1e-9;dirs=[Vector(x).normalized() for x in [(1,.371,.217),(.163,1,.493),(.719,.283,1)]];trees={};faces={};lookup={c['tag']:c for c in ct['components']}
for c in ct['components']:
 ids=set(c['vertices']);faces[c['tag']]=[t for t in tris if all(i in ids for i in t)];trees[c['tag']]=BVHTree.FromPolygons(vs,faces[c['tag']],all_triangles=True)
def inside(tree,q):
 hit,n,f,dist=tree.find_nearest(q)
 if dist is None or dist<=epsilon:return False,dist,[]
 parity=[]
 for d in dirs:
  cursor=q.copy();count=0
  for _ in range(1000):
   hit=tree.ray_cast(cursor,d,extent*4)[0]
   if hit is None:break
   count+=1;cursor=hit+d*epsilon*8
  parity.append(count%2)
 return all(parity),dist,parity
records=[];errors=[]
for c in ct['components']:
 if not c.get('parent'):continue
 own=trees[c['tag']];parent=trees[c['parent']];candidates=[]
 # Actual base-face center, vertex-set center and inward samples of every real surface triangle.
 for ids in [c['base_vertices'],c['vertices']]:candidates.append(sum((vs[i] for i in ids),Vector())/len(ids))
 for tri in faces[c['tag']]:
  x,y,z=[vs[i] for i in tri];n=(y-x).cross(z-x)
  if n.length==0:continue
  n.normalize();cc=(x+y+z)/3;step=min((y-x).length,(z-y).length,(x-z).length)
  for fraction in [.05,.2,.45]:candidates.append(cc-n*step*fraction)
 witness=None
 for q in candidates:
  qp=parent.find_nearest(q)
  if qp[3] is None or qp[3]<=epsilon or (q-qp[0]).dot(qp[1])>=0:continue
  ip,dp,pp=inside(parent,q)
  if not ip:continue
  ic,dc,pc=inside(own,q)
  if ic:witness={'point_world_m':list(q),'distance_to_parent_surface_m':dp,'distance_to_child_surface_m':dc,'parent_three_ray_parities':pp,'child_three_ray_parities':pc};break
 records.append({'child':c['tag'],'parent':c['parent'],'positive_volume_interior_witness':witness,'pass':witness is not None})
 if witness is None:errors.append(c['tag'])
assert src.read_bytes()==before
report={'schema_version':1,'status':'pass' if not errors else 'fail','source_sha256':hashlib.sha256(before).hexdigest(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':records,'errors':errors,'boundary_exclusion_numerical_epsilon_m':epsilon,'policy':'No boundary point counts as inside. Each pass contains a point strictly interior to both original solids in3oblique ray parity tests, with positive distances to both surfaces. No new minimum overlap distance imposed; finite sampling can miss real overlaps and requires diagnosis, not automatic geometry enlargement.','source_modified':False}
Path(a.output).open('x').write(json.dumps(report,indent=2)+'\n');print(report['status'],errors)
