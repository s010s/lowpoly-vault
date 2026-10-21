#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Actual world-space full-scene visibility diagnostics, not photographic approval."""
import argparse,hashlib,json,datetime,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=a.source);contract=json.loads(bpy.data.texts['BATCH99_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[contract['object_name']];bpy.context.view_layer.update();verts=[o.matrix_world@v.co for v in o.data.vertices];o.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in o.data.loop_triangles];directions={'front':(0,-1,0),'rear':(0,1,0),'left':(-1,0,0),'right':(1,0,0),'top':(0,0,1),'bottom':(0,0,-1),'hero':(.47,-.67,.57),'reversehero':(-.47,.67,.57)};dirs={k:Vector(v).normalized() for k,v in directions.items()};extent=max(max(v[k] for v in verts)-min(v[k] for v in verts) for k in range(3));eps=extent*1e-7;records=[];errors=[]
for c in contract['components']:
 ids=set(c['vertices']);rest=[t for t in tris if not all(v in ids for v in t)];tree=BVHTree.FromPolygons(verts,rest,all_triangles=True);counts={k:0 for k in dirs};seen=set()
 for i in c['vertices']:
  for key,d in dirs.items():
   pos,_,_,distance=tree.ray_cast(verts[i]+d*eps,d,extent*3)
   if pos is None:counts[key]+=1;seen.add(i)
 rec={'tag':c['tag'],'kind':c['kind'],'component_vertices':len(ids),'visible_vertices_any_direction':len(seen),'visible_fraction':len(seen)/len(ids),'visible_vertices_by_direction':counts,'has_actual_exposed_vertices':bool(seen)};records.append(rec)
 if not seen:errors.append('no ray-exposed actual component vertex:'+c['tag'])
r={'schema_version':1,'status':'pass' if not errors else 'fail','source_sha256':hashlib.sha256(Path(a.source).read_bytes()).hexdigest(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Reopened transformed Blend mesh. For each component, exclude only its own triangles and ray-cast every actual vertex in8 fixed directions against ALL other component triangles. No camera/material adjustments. Positive visibility is necessary, not sufficient, for meaningful pixel readability.','numerical_ray_origin_epsilon_m':eps,'directions':directions,'components':records,'errors':errors,'limitations':'Sparse-direction geometric exposure, not complete screen-space occlusion nor independent visual/factual acceptance. Tiny visible fractions are disclosed, not converted to arbitrary pass thresholds.'};Path(a.output).open('x').write(json.dumps(r,indent=2)+'\n');print(r['status'],r['errors'])
