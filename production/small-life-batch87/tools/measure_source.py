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
