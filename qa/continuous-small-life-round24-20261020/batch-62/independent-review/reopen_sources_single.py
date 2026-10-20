import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path('/tmp/lowpoly-batch62-20261020');OUT=Path('/workspace/shared/lowpoly-round24-qa62')
B='assets/candidates/continuous-small-life-round24-20261020/batch-62'
args=sys.argv[sys.argv.index('--')+1:];asset=args[0];rev=args[1]
d=ROOT/B/asset/rev;path=d/'source.blend'
def obj_bounds(o):
 pts=[o.matrix_world @ Vector(v) for v in o.bound_box]
 return [[min(p[k] for p in pts) for k in range(3)],[max(p[k] for p in pts) for k in range(3)]]
dg=bpy.context.evaluated_depsgraph_get();dg.update();meshes=[];types={}
for o in bpy.data.objects:
 types[o.type]=types.get(o.type,0)+1
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();eo=o.evaluated_get(dg);ev=eo.to_mesh(preserve_all_data_layers=False,depsgraph=dg);ev.calc_loop_triangles()
 meshes.append({'name':o.name,'data_name':m.name,'authored_vertices':len(m.vertices),'authored_polygons':len(m.polygons),'authored_triangles':len(m.loop_triangles),'evaluated_vertices':len(ev.vertices),'evaluated_polygons':len(ev.polygons),'evaluated_triangles':len(ev.loop_triangles),'materials':list(dict.fromkeys([s.material.name if s.material else None for s in o.material_slots])),'modifiers':[{'name':md.name,'type':md.type,'show_render':md.show_render,'show_viewport':md.show_viewport} for md in o.modifiers],'bounds_world_m':obj_bounds(o)})
 eo.to_mesh_clear()
counts=json.load(open(d/'source-vertex-counts.json'));srcmetrics=json.load(open(d/'source-metrics.json'));exp={p['name']:p for p in counts.get('parts',[])};comps=[]
for m in meshes:
 e=exp.get(m['name']);comps.append({'name':m['name'],'count_record_found':bool(e),'record':e,'authored_vertex_match':bool(e and m['authored_vertices']==e['authored_vertices']),'evaluated_vertex_match':bool(e and m['evaluated_vertices']==e['evaluated_vertices']),'authored_polygon_match':bool(e and m['authored_polygons']==e['authored_polygons']),'evaluated_polygon_match':bool(e and m['evaluated_polygons']==e['evaluated_polygons'])})
totals={k:sum(m[k] for m in meshes) for k in ['authored_vertices','authored_polygons','authored_triangles','evaluated_vertices','evaluated_polygons','evaluated_triangles']};raw=path.read_bytes()
rep={'asset_id':asset,'revision':rev,'source_path':str(path),'source_sha256':hashlib.sha256(raw).hexdigest(),'source_matches_dedicated_counts_hash':hashlib.sha256(raw).hexdigest()==counts.get('source_sha256'),'blender_version':bpy.app.version_string,'objects_by_type':types,'mesh_objects':meshes,'totals':totals,'recorded_totals':{k:counts.get(k) for k in ['authored_vertices','evaluated_vertices','authored_polygons','evaluated_polygons']},'record_totals_match':{k:totals[k]==counts.get(k) for k in ['authored_vertices','evaluated_vertices','authored_polygons','evaluated_polygons']},'part_reconciliation':comps,'part_count_matches':len(comps)==len(exp) and all(c['count_record_found'] for c in comps),'source_metric_triangles':srcmetrics.get('triangles'),'source_metric_bounds_blender_m':srcmetrics.get('bounds_blender_m'),'diagnostic_objects':{t:n for t,n in types.items() if t in ('CAMERA','LIGHT')}}
(OUT/f'source-reopen-{asset}.json').write_text(json.dumps(rep,indent=2)+'\n');print(asset, 'opened',len(meshes),'meshes', totals)
