# SPDX-License-Identifier: MIT
"""Checks welded surface topology, face orientation, grounding and semantic parts.
It is not a species, intersection, beauty or browser-GPU validator.
"""
import bpy,sys,json,math,hashlib
from pathlib import Path
from collections import defaultdict
from mathutils import Vector
argv=sys.argv[sys.argv.index('--')+1:]; source=Path(argv[0]); out=Path(argv[1]); bpy.ops.wm.open_mainfile(filepath=str(source))
meshobjs=[o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH']
verts=[]; index={}; tris=[]; sem={}; normals=[]
for obj in meshobjs:
 m=obj.data; m.calc_loop_triangles(); ids=[]
 for v in m.vertices:
  p=obj.matrix_world@v.co; key=tuple(round(x,7) for x in p)
  if key not in index: index[key]=len(verts); verts.append(Vector(key))
  ids.append(index[key])
 for t in m.loop_triangles: tris.append(tuple(ids[v] for v in t.vertices))
 for g in obj.vertex_groups:
  inds=[v.index for v in m.vertices if any(q.group==g.index and q.weight>0 for q in v.groups)]
  if inds:
   ps=[obj.matrix_world@m.vertices[i].co for i in inds]
   sem.setdefault(g.name,[]).extend([tuple(p) for p in ps])
edges=defaultdict(list); adj=defaultdict(set)
for ti,t in enumerate(tris):
 for a,b in zip(t,t[1:]+t[:1]):
  edges[tuple(sorted((a,b)))].append(1 if a<b else -1); adj[a].add(b);adj[b].add(a)
seen=set(); comps=[]
for v in range(len(verts)):
 if v in seen:continue
 stack=[v]; group=set()
 while stack:
  a=stack.pop()
  if a in seen:continue
  seen.add(a);group.add(a);stack.extend(adj[a]-seen)
 ts=[t for t in tris if t[0] in group]
 vol=sum(verts[a].dot(verts[b].cross(verts[c]))/6 for a,b,c in ts)
 comps.append({'vertices':len(group),'triangles':len(ts),'signed_volume_m3':vol,'min_z':min(verts[i].z for i in group)})
boundary=sum(len(q)==1 for q in edges.values()); nonmanifold=sum(len(q)>2 for q in edges.values()); inconsistent=sum(len(q)==2 and sum(q)!=0 for q in edges.values())
checks={'all_coordinates_finite':all(math.isfinite(x) for v in verts for x in v),'boundary_edges_after_material_seam_weld':boundary,'nonmanifold_edges_after_material_seam_weld':nonmanifold,'inconsistent_oriented_edges':inconsistent,'nonpositive_signed_volume_components':sum(c['signed_volume_m3']<=0 for c in comps),'ground_min_z_m':min(v.z for v in verts),'y_length_m':max(v.y for v in verts)-min(v.y for v in verts),'both_fourth_manual_nubs_present':all(label+'-reduced-manual-fourth-nub' in sem for label in ['left','right']),'six_main_manual_digits_present':all(label+'-manual-main-digit-'+str(k) in sem for label in ['left','right'] for k in [1,2,3]),'six_major_forward_toes_present':all(label+'-pedal-digit-'+str(k) in sem for label in ['left','right'] for k in [2,3,4]),'nasal_horn_and_paired_brows_present':all(n in sem for n in ['single-compressed-nasal-horn','left-lacrimal-brow','right-lacrimal-brow']),'preview_stage_absent':all(o.type in ['MESH','EMPTY'] for o in bpy.data.objects)}
errors=[]
for k in ['boundary_edges_after_material_seam_weld','nonmanifold_edges_after_material_seam_weld','inconsistent_oriented_edges','nonpositive_signed_volume_components']:
 if checks[k]: errors.append(k)
for k in ['all_coordinates_finite','both_fourth_manual_nubs_present','six_main_manual_digits_present','six_major_forward_toes_present','nasal_horn_and_paired_brows_present','preview_stage_absent']:
 if not checks[k]: errors.append(k)
if abs(checks['ground_min_z_m'])>1e-5:errors.append('ground_min_z_m')
result={'status':'PASS' if not errors else 'FAIL','source_blend_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'checks':checks,'errors':errors,'component_count':len(comps),'components':comps,'semantic_part_names':sorted(sem),'limitations':['Exact coincident material seams are welded only for auditing; source remains editable per palette.','Separately closed intersecting anatomical volumes are intentional. This is not a Boolean union or printability check.','Positive signed volume and edge orientation establish coherent outward surface components, not absence of all anatomical intersections.','No browser GPU or scientific acceptance is inferred.']}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({'status':result['status'],'checks':checks,'components':len(comps)}))
if errors:sys.exit(1)
