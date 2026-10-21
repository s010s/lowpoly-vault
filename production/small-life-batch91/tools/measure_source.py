#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only source reopen plus authored/evaluated counts; no source mutation."""
import sys,json,hashlib,datetime,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from check_source_export import main
main()
import bpy
args=sys.argv[sys.argv.index('--')+1:];source=Path(args[args.index('--source')+1]);out=Path(args[args.index('--output')+1]);parts=[];dg=bpy.context.evaluated_depsgraph_get()
for o in bpy.data.objects:
 if o.type!='MESH':continue
 o.data.calc_loop_triangles();ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'authored_polygons':len(o.data.polygons),'authored_triangles':len(o.data.loop_triangles),'evaluated_vertices':len(me.vertices),'evaluated_polygons':len(me.polygons),'evaluated_triangles':len(me.loop_triangles),'modifier_count':len(o.modifiers)});ev.to_mesh_clear()
r={'schema_version':1,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'blender':bpy.app.version_string,'parts':parts,'totals':{k:sum(x[k] for x in parts) for k in ['authored_vertices','authored_polygons','authored_triangles','evaluated_vertices','evaluated_polygons','evaluated_triangles']},'source_saved':False}
with (out.parent/'authored-evaluated-counts.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
# Mesh-connected-component measurements derive directly from freshly reopened vertex/face data.
components=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 adj=[set() for _ in o.data.vertices]
 for e in o.data.edges:
  a,b=e.vertices;adj[a].add(b);adj[b].add(a)
 unseen=set(range(len(adj)));count=0
 while unseen:
  start=next(iter(unseen));stack=[start];seen={start};unseen.remove(start)
  while stack:
   for q in adj[stack.pop()]:
    if q in unseen:unseen.remove(q);seen.add(q);stack.append(q)
  points=[o.matrix_world@o.data.vertices[i].co for i in seen];lo=[min(v[k] for v in points) for k in range(3)];hi=[max(v[k] for v in points) for k in range(3)];polys=[p for p in o.data.polygons if p.vertices[0] in seen];mats=sorted({o.data.materials[p.material_index].name for p in polys});components.append({'object':o.name,'component':count,'vertices':len(seen),'polygons':len(polys),'materials':mats,'bounds_blender_m':{'min':lo,'max':hi,'size':[hi[k]-lo[k] for k in range(3)]}});count+=1
rr={'schema_version':1,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'method':'Actual freshly reopened source connected vertex-edge components, not config counts; intersecting branch junction components intentionally remain separate.','components':components}
with (out.parent/'frozen-feature-measurements.json').open('x') as f:json.dump(rr,f,indent=2);f.write('\n')
