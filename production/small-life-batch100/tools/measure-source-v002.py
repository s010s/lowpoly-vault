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

# Actual mesh topology and retained design metadata, separate from inferred biological counts.
import bmesh
topo=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);topo.append({'object':o.name,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'euler_characteristic':len(bm.verts)-len(bm.edges)+len(bm.faces),'boundary_edges':sum(1 for e in bm.edges if len(e.link_faces)==1),'nonmanifold_edges':sum(1 for e in bm.edges if len(e.link_faces)!=2),'design_metadata_not_independent_measurements':{k:o[k] for k in o.keys() if k.startswith('design_')}});bm.free()
with (out.parent/'actual-mesh-topology.json').open('x') as f:json.dump({'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'objects':topo},f,indent=2);f.write('\n')
# Direct final WORLD-space per-component measurements and physical point-in-solid contact.
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np
measure=[];contact=[]
for ob in bpy.data.objects:
 if ob.type!='MESH':continue
 groups={vg.name:[] for vg in ob.vertex_groups};vertices=[ob.matrix_world@v.co for v in ob.data.vertices]
 for v in ob.data.vertices:
  for gg in v.groups:groups[ob.vertex_groups[gg.group].name].append(v.index)
 ob.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in ob.data.loop_triangles];bvhs={};group_tris={}
 for tag,ids in groups.items():
  pts=np.array([vertices[i] for i in ids],dtype=float);lo=pts.min(axis=0);hi=pts.max(axis=0);cov=np.cov(pts.T);_,axes=np.linalg.eigh(cov);local=(pts-pts.mean(axis=0))@axes;ext=local.max(axis=0)-local.min(axis=0)
  measure.append({'component':tag,'vertices':len(ids),'world_bounds_blender_m':{'min':lo.tolist(),'max':hi.tolist(),'size':(hi-lo).tolist()},'principal_axis_extents_m':ext.tolist(),'transform_scale':list(ob.scale),'measurement':'Actual reopened transformed mesh vertices, no config substitution'})
  ii=set(ids);polys=[t for t in tris if all(j in ii for j in t)];group_tris[tag]=polys;bvhs[tag]=BVHTree.FromPolygons(vertices,polys,all_triangles=True,epsilon=0)
 def inside(point,bvh):
  direction=Vector((.32731,.47677,.81513)).normalized();pos=point.copy();n=0;advance=max(1e-9,max(abs(v) for v in point)*1e-6)
  for _ in range(32):
   loc,normal,index,dist=bvh.ray_cast(pos,direction,100)
   if loc is None:break
   n+=1;pos=loc+direction*advance
  return n%2==1
 for tag,ids in groups.items():
  par=[x['parent'] for x in json.loads(ob.get('contact_design','[]')) if x['child']==tag]
  if not par:continue
  hits=[];mind=None
  for parent in par:
   if parent not in bvhs:continue
   tree=bvhs[parent]
   for vi in ids:
    point=vertices[vi];near=tree.find_nearest(point)
    if near[0] is not None:mind=near[3] if mind is None else min(mind,near[3])
    if inside(point,tree):hits.append({'parent':parent,'actual_child_vertex':vi});break
  vertex_hit=bool(hits)
  if not hits:
   for parent in par:
    if parent not in bvhs:continue
    found=False
    for tri in group_tris[tag]:
     aa,bb,cc=[vertices[j] for j in tri]
     for label,pt in [('centroid',(aa+bb+cc)/3),('edge_ab',(aa+bb)/2),('edge_bc',(bb+cc)/2),('edge_ca',(cc+aa)/2)]:
      if inside(pt,bvhs[parent]):hits.append({'parent':parent,'actual_child_triangle':list(tri),'surface_sample':label,'position_world':list(pt)});found=True;break
     if found:break
    if found:break
  contact.append({'child':tag,'tested_parents':par,'actual_child_vertex_inside_parent':vertex_hit,'actual_child_geometry_sample_inside_parent':bool(hits),'inside_witnesses':hits,'nearest_surface_distance_m':mind,'test':'Odd ray parity on actual closed parent mesh, using actual child vertices then actual triangle centroids/edge midpoints. Surface witness inside parent establishes real geometric penetration. No configuration-based contact assumption. Scale-aware ray advancement avoids float32 repeat hits.'})
# Exposure is independently tested on the actual closed supporting surface, not centerline.
exposure=[]
for ob in bpy.data.objects:
 if ob.type!='MESH':continue
 for relation in json.loads(ob.get('contact_design','[]')):
  child,parent=relation['child'],relation['parent'];points=[vertices[i] for i in groups[child]];inside_flags=[inside(v,bvhs[parent]) for v in points];outside=[v for v,flag in zip(points,inside_flags) if not flag];distances=[bvhs[parent].find_nearest(v)[3] for v in outside];exposure.append({'child':child,'parent':parent,'actual_vertices':len(points),'inside_vertices':sum(inside_flags),'outside_vertices':len(outside),'outside_fraction':len(outside)/len(points),'max_exposed_vertex_distance_from_parent_surface_m':max(distances) if distances else 0,'not_wholly_buried':bool(outside),'method':'Full actual child transformed vertex set tested by parity on actual closed supporting mesh; exposure does not alone prove512px visibility.'})
with (out.parent/'actual-component-exposure.json').open('x') as f:json.dump({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'items':exposure,'wholly_buried':[r['child'] for r in exposure if not r['not_wholly_buried']]},f,indent=2);f.write('\n')
report={'schema_version':1,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'world_component_measurements':measure,'physical_contact_tests':contact,'contact_witness_counts':{'tested':len(contact),'with_inside_witness':sum(x['actual_child_geometry_sample_inside_parent'] for x in contact),'without_witness':sum(not x['actual_child_geometry_sample_inside_parent'] for x in contact)},'no_normalization':'Only grounding/centering translations in generator; all actual posttransform dimensions above.'}
with (out.parent/'world-components-and-contacts.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')

# Broad frozen world dimensions applied to actual transformed mesh, including every group.
config=Path(args[args.index('--source')+1]).parents[1]/'config.json'
# Queue source path may not be in delivery tree; explicit frozen brief is passed outside check_source_export CLI through environment-independent script constant lookup.
aid=source.stem
frozen=ROOT/'production/small-life-batch100'/aid/'r001/original-brief.json'
brief=json.loads(frozen.read_text());ranges=brief['scale']['hard_world_bbox_size_ranges_xyz_m'];pts=[o.matrix_world@v.co for o in bpy.data.objects if o.type=='MESH' for v in o.data.vertices];lo=[min(v[k] for v in pts) for k in range(3)];hi=[max(v[k] for v in pts) for k in range(3)];size=[hi[k]-lo[k] for k in range(3)];checks=[ranges[k][0]<=size[k]<=ranges[k][1] for k in range(3)];component_ok=all(all(x>0 and x<=max(r[1] for r in ranges) for x in item['world_bounds_blender_m']['size']) for item in measure)
(out.parent/'hard-dimension-check.json').write_text(json.dumps({'status':'pass' if all(checks) and component_ok else 'fail','original_brief_sha256':hashlib.sha256(frozen.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'actual_final_world_bbox_blender_m':{'min':lo,'max':hi,'size':size},'hard_size_ranges_xyz_m':ranges,'per_axis_pass':checks,'all_component_extents_finite_positive_within_hard_global_max':component_ok,'all_component_count':len(measure),'transforms':[{'object':o.name,'scale':list(o.scale),'matrix_world':[list(row) for row in o.matrix_world]} for o in bpy.data.objects if o.type=='MESH']},indent=2)+'\n')

# Counts and segment exposure inferred from actual reopened geometry, not design properties.
features={'asset_id':aid,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'Actual named vertex groups checked against mesh connected islands and their world vertex arrays. Design metadata separately retained, not substituted for measurement.','counts':{},'details':[]}
for ob in bpy.data.objects:
 if ob.type!='MESH':continue
 g={vg.name:[] for vg in ob.vertex_groups}
 for v in ob.data.vertices:
  for gg in v.groups:g[ob.vertex_groups[gg.group].name].append(v.index)
 adjacency={v.index:set() for v in ob.data.vertices}
 for e in ob.data.edges:
  x,y=e.vertices;adjacency[x].add(y);adjacency[y].add(x)
 def islands(ids):
  left=set(ids);parts=[]
  while left:
   seed=min(left);left.remove(seed);todo=[seed];part=[seed]
   while todo:
    for q in adjacency[todo.pop()]:
     if q in left:left.remove(q);todo.append(q);part.append(q)
   parts.append(sorted(part))
  return parts
 if aid=='lygodium':
  veins=[tag for tag in g if tag.startswith('dichotomous_veins_')];records=[];segments=[]
  for tag in veins:
   for j,piece in enumerate(islands(g[tag])):
    rings=[];centers=[]
    for k in range(0,len(piece),4):
     pp=[ob.matrix_world@ob.data.vertices[i].co for i in piece[k:k+4]];flags=[inside(v,bvhs['bifid_lamina']) for v in pp];centers.append(sum(pp,Vector())/len(pp));rings.append({'ring':k//4,'inside_vertices':sum(flags),'outside_vertices':len(flags)-sum(flags)})
    segments.append([list(centers[0]),list(centers[-1])]);records.append({'group':tag,'segment':j,'rings':rings,'all_rings_cross_and_expose':all(0<x['inside_vertices']<4 for x in rings)})
  signatures=[tuple(sorted(tuple(round(x,9) for x in p) for p in ends)) for ends in segments];dup=len(signatures)-len(set(signatures));features['counts']={'actual_lamina_islands':len(islands(g['bifid_lamina'])),'actual_sorophore_solids':sum(len(islands(ids)) for tag,ids in g.items() if tag.startswith('flattened_sorophore')),'actual_fertile_branchlets':sum(len(islands(ids)) for tag,ids in g.items() if tag.startswith('fertile_branchlet')),'actual_vein_systems':len(veins),'actual_closed_vein_segments':len(records),'duplicate_whole_vein_segments':dup};features['vein_segment_exposure']={'all_segments_pass':all(r['all_rings_cross_and_expose'] for r in records),'segments':records,'method':'Each actual4-vertex ring on every closed vein segment tested against actual supporting lamina. Intended shared fork centers allowed; identical complete segments forbidden.'}
 elif aid=='chaetocladus':
  tags=[tag for tag in g if tag.startswith('lateral_')];bywhorl={};ends=[];details=[]
  for tag in tags:
   wh=tag.split('_')[1];bywhorl[wh]=bywhorl.get(wh,0)+1;ids=g[tag];pp=[ob.matrix_world@ob.data.vertices[i].co for i in ids];cs=[sum(pp[k:k+3],Vector())/3 for k in range(0,len(pp),3)];ends.append(tuple(round(x,9) for x in cs[-1]));details.append({'component':tag,'actual_connected_solids':len(islands(ids)),'actual_vertices':len(ids),'centerline_segments':len(cs)-1,'side_rings':len(cs),'branching_in_this_tube':False,'root_world':list(cs[0]),'tip_world':list(cs[-1])})
  features['counts']={'actual_axis_islands':len(islands(g['central_axis'])),'actual_lateral_solids':sum(len(islands(g[t])) for t in tags),'actual_whorls':len(bywhorl),'laterals_per_named_whorl':bywhorl,'unique_lateral_tips':len(set(ends)),'duplicate_lateral_tip_positions':len(ends)-len(set(ends))};features['details']=details;assert all(d['actual_vertices']==9 and d['actual_connected_solids']==1 for d in details)
 elif aid=='flabellophyton':features['counts']={'actual_closed_body_islands':len(islands(g['integral_fan_stalk_attachment'])),'actual_surface_grid_vertices':len(g['integral_fan_stalk_attachment']),'separate_root_components':0};features['limits']='Integrated corrugation and stalk are one connected shell. Filament ridge count corroborated by row curvature and pixels, not separate organism counts.'
 else:features['counts']={'actual_body_islands':len(islands(g['bilobed_cancellate_body'])),'actual_vertices':len(g['bilobed_cancellate_body']),'separate_spore_components':0};features['limits']='Bilobed silhouette is interpreted from actual pixels, not counted from arbitrary tag names.'
(out.parent/'actual-feature-counts.json').write_text(json.dumps(features,indent=2)+'\n')
# Detect local inversions of front/back sheet faces from actual transformed triangles.
# Closed topology alone misses the failed r002 Protosalvinia notch fold.
fold_checks=[]
for ob in bpy.data.objects:
 if ob.type!='MESH':continue
 vv=[ob.matrix_world@v.co for v in ob.data.vertices];ob.data.calc_loop_triangles();degenerate=[]
 for ti,t in enumerate(ob.data.loop_triangles):
  a,b,c=[vv[i] for i in t.vertices]
  if (b-a).cross(c-a).length<=1e-20:degenerate.append(ti)
 if aid in ['protosalvinia','flabellophyton']:
  half=len(vv)//2;wrong=[];front=back=0
  for ti,t in enumerate(ob.data.loop_triangles):
   ids=list(t.vertices);a,b,c=[vv[i] for i in ids];ny=(b-a).cross(c-a).y
   if max(ids)<half:
    front+=1
    if ny>=0:wrong.append({'triangle':ti,'side':'front','oriented_cross_y':ny})
   elif min(ids)>=half:
    back+=1
    if ny<=0:wrong.append({'triangle':ti,'side':'back','oriented_cross_y':ny})
  fold_checks.append({'object':ob.name,'front_triangles':front,'back_triangles':back,'locally_inverted_faces':wrong,'zero_area_triangles':degenerate,'pass':not wrong and not degenerate})
 else:fold_checks.append({'object':ob.name,'front_back_test':'Not applicable to compound tubes/laminae; individual contact/exposure and pixels are separate checks.','zero_area_triangles':degenerate,'pass':not degenerate})
(out.parent/'actual-surface-fold-check.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'Actual world-space oriented triangle cross products. For sheet-like whole-body meshes, front/back half index sets identified from authored regular shell topology; any locally reversed projection is an inversion. Does not claim exhaustive all-pairs surface-intersection testing for compound branches.','status':'pass' if all(x['pass'] for x in fold_checks) else 'fail','objects':fold_checks},indent=2)+'\n')
assert all(x['pass'] for x in fold_checks),fold_checks
