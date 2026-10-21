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
frozen=ROOT/'production/small-life-batch97'/aid/'r001/original-brief.json'
brief=json.loads(frozen.read_text());ranges=brief['scale']['hard_world_bbox_size_ranges_xyz_m'];pts=[o.matrix_world@v.co for o in bpy.data.objects if o.type=='MESH' for v in o.data.vertices];lo=[min(v[k] for v in pts) for k in range(3)];hi=[max(v[k] for v in pts) for k in range(3)];size=[hi[k]-lo[k] for k in range(3)];checks=[ranges[k][0]<=size[k]<=ranges[k][1] for k in range(3)];component_ok=all(all(x>0 and x<=max(r[1] for r in ranges) for x in item['world_bounds_blender_m']['size']) for item in measure)
(out.parent/'hard-dimension-check.json').write_text(json.dumps({'status':'pass' if all(checks) and component_ok else 'fail','original_brief_sha256':hashlib.sha256(frozen.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'actual_final_world_bbox_blender_m':{'min':lo,'max':hi,'size':size},'hard_size_ranges_xyz_m':ranges,'per_axis_pass':checks,'all_component_extents_finite_positive_within_hard_global_max':component_ok,'all_component_count':len(measure),'transforms':[{'object':o.name,'scale':list(o.scale),'matrix_world':[list(row) for row in o.matrix_world]} for o in bpy.data.objects if o.type=='MESH']},indent=2)+'\n')

# Counts inferred from reopened geometry and connected mesh islands, not design properties.
features={'asset_id':aid,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'Actual named component groups cross-checked against mesh-island sizes; Dicranophyllum fork graph inferred from actual ribbon ring-center coincidences. No config counts substituted.','counts':{},'details':[]}
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
 if aid=='ginkgo':
  ids=g['six_lobed_lamina'];points=[ob.matrix_world@ob.data.vertices[i].co for i in ids[:len(ids)//2]];base=(points[0]+points[-1])/2;rs=[(v-base).length for v in points];peaks=[i for i in range(1,len(rs)-1) if rs[i]>rs[i-1] and rs[i]>rs[i+1]];veinparts=[islands(ids) for tag,ids in g.items() if tag.startswith('radiating_vein_')];features['counts']={'actual_margin_radial_peaks':len(peaks),'lamina_islands':len(islands(ids)) if False else len(islands(g['six_lobed_lamina'])),'petiole_islands':len(islands(g['petiole'])),'actual_vein_systems':len(veinparts),'actual_vein_segments':sum(len(x) for x in veinparts)};features['details']=[{'radial_peak_indices':peaks,'actual_radial_distances_m':rs}]
 elif aid=='dicranophyllum':
  details=[]
  for tag,ids in g.items():
   if not tag.startswith('leaf_'):continue
   parts=islands(ids);nodes=[];edges=[]
   def node(v):
    for i,p in enumerate(nodes):
     if (p-v).length<1e-6:return i
    nodes.append(v);return len(nodes)-1
   for piece in parts:
    pts=[ob.matrix_world@ob.data.vertices[i].co for i in piece];start=sum(pts[:4],Vector())/4;end=sum(pts[-4:],Vector())/4;edges.append((node(start),node(end)))
   degree=[sum(i in e for e in edges) for i in range(len(nodes))];details.append({'component':tag,'actual_closed_islands':len(parts),'ring_graph_edges':len(edges),'ring_graph_nodes':len(nodes),'binary_junction_nodes':degree.count(3),'free_ends_including_base':degree.count(1),'terminal_tips_excluding_base':degree.count(1)-1,'all_junctions_degree_at_most3':max(degree)<=3})
  features['details']=details;features['counts']={'actual_leaf_groups':len(details),'actual_terminal_tips':sum(x['terminal_tips_excluding_base'] for x in details),'actual_binary_fork_junctions':sum(x['binary_junction_nodes'] for x in details),'actual_leaf_cushions':sum(k.startswith('cushion_') for k in g),'actual_axes':len(islands(g['slender_axis']))};assert all(x['terminal_tips_excluding_base']==4 and x['binary_junction_nodes']==3 and x['actual_closed_islands']==7 for x in details)
 elif aid=='noeggerathia':
  leaves=[k for k in g if k.startswith('pinnule_')];features['counts']={'actual_pinnules':len(leaves),'actual_solid_pinnule_islands':sum(len(islands(g[k])) for k in leaves),'actual_vein_systems':sum(k.startswith('fan_veins_') for k in g),'actual_rachis_islands':len(islands(g['rachis']))};features['details']=[{'component':k,'actual_outline_vertices_per_surface':len(g[k])//2,'closed_solid_islands':len(islands(g[k]))} for k in leaves]
 elif aid=='bjuvia':
  veins=[k for k in g if k.startswith('transverse_vein_')];features['counts']={'actual_lamina_islands':len(islands(g['entire_strap_lamina'])),'actual_midrib_islands':len(islands(g['midrib'])),'actual_lateral_vein_islands':sum(len(islands(g[k])) for k in veins),'actual_paired_rows':len({k.split('_')[2] for k in veins}),'crossvein_tagged_groups':sum(k.startswith('crossvein') for k in g)};features['topology_limit']='Zero crossvein groups is corroborated by actual same-scale neutral pixels and each of192 lateral veins being an independent nonbranching closed3-ring tube. No numerical claim that all veins are completely separate from central rib.';assert all(len(islands(g[k]))==1 and len(g[k])==12 for k in veins)
(out.parent/'actual-feature-counts.json').write_text(json.dumps(features,indent=2)+'\n')

# Every actual closed Ginkgo vein segment and every ring must cross and protrude from actual parent surface.
if aid=='ginkgo':
 ob=next(o for o in bpy.data.objects if o.type=='MESH');records=[]
 for tag,ids in g.items():
  if not tag.startswith('radiating_vein_'):continue
  for j,piece in enumerate(islands(ids)):
   ring=[]
   for k in range(0,len(piece),5):
    pp=[ob.matrix_world@ob.data.vertices[i].co for i in piece[k:k+5]];flags=[inside(v,bvhs['six_lobed_lamina']) for v in pp];ring.append({'ring':k//5,'inside_vertices':sum(flags),'outside_vertices':len(flags)-sum(flags)})
   records.append({'group':tag,'segment':j,'rings':ring,'all_rings_cross_and_expose':all(0<x['inside_vertices']<5 for x in ring)})
 (out.parent/'actual-vein-segment-exposure.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'segments':records,'all_segments_pass':all(r['all_rings_cross_and_expose'] for r in records),'method':'Actual closed-mesh ray parity, each5-vertex ring on each connected vein segment; full-segment surface protrusion and partial embedding, not group-center coincidence.'},indent=2)+'\n')
 assert len(records)==42 and all(r['all_rings_cross_and_expose'] for r in records)
