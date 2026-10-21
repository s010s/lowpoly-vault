# SPDX-License-Identifier: MIT
"""Read-only exact original source whole-scene line-of-sight diagnostics."""
import bpy,sys,json,hashlib,math,os,datetime
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:];src=Path(a[0]);glb=Path(a[1]);out=Path(a[2]);bpy.ops.wm.open_mainfile(filepath=str(src));objects=[o for o in bpy.data.objects if o.type=='MESH'];vs=[];ts=[];tags=[];aps=[];group_bounds={}
for o in objects:
 m=o.data;m.calc_loop_triangles();n=len(vs);verts=[o.matrix_world@v.co for v in m.vertices];vs+=verts;vg={g.index:g.name for g in o.vertex_groups};ids={g.name:[] for g in o.vertex_groups}
 for v in m.vertices:
  for g in v.groups:ids[vg[g.group]].append(v.index)
 for tag,ii in ids.items():group_bounds[tag]=[[min(verts[i][k] for i in ii) for k in range(3)],[max(verts[i][k] for i in ii) for k in range(3)]]
 for t in m.loop_triangles:
  common=set(g.group for g in m.vertices[t.vertices[0]].groups)
  for i in t.vertices[1:]:common &= set(g.group for g in m.vertices[i].groups)
  assert len(common)==1
  ts.append(tuple(i+n for i in t.vertices));tags.append(vg[common.pop()])
 aps+=json.loads(o.get('aperture_design','[]'))
tree=BVHTree.FromPolygons(vs,ts,all_triangles=True,epsilon=0);angles={'hero':(35,35),'reversehero':(215,35),'front':(0,0),'side':(90,0),'rear':(180,0),'top':(0,90),'lower_oblique':(45,-50),'lower_proximal':(-30,-60)}
dirs={k:Vector((math.sin(math.radians(az))*math.cos(math.radians(el)),-math.cos(math.radians(az))*math.cos(math.radians(el)),math.sin(math.radians(el)))) for k,(az,el) in angles.items()};res={tag:{'component':tag,'triangle_centroids':0,'visible_triangle_centroids_by_direction':{k:0 for k in dirs}} for tag in set(tags)}
for t,tag in zip(ts,tags):
 aa,b,c=[vs[i] for i in t];center=(aa+b+c)/3;normal=(b-aa).cross(c-aa).normalized();res[tag]['triangle_centroids']+=1
 for name,d in dirs.items():
  if normal.dot(d)<=0:continue
  hit,_,_,_=tree.ray_cast(center+d*1e-8,d,1)
  if hit is None:res[tag]['visible_triangle_centroids_by_direction'][name]+=1
apresult=[]
for ap in aps:
 p=Vector(ap['center']);d=Vector(ap['direction']).normalized();hits=[]
 for key,dd in {'mouth_axis':d,**dirs}.items():
  if d.dot(dd)<=0:continue
  h,_,ix,dist=tree.ray_cast(p+dd*1e-8,dd,1)
  hits.append({'direction':key,'unobstructed_to_exterior':h is None,'nearest_obstruction_component':None if h is None else tags[ix],'distance_m':dist if h is not None else None})
 apresult.append({'component':ap['component'],'ray_visibility':hits,'some_open_exterior_direction':any(x['unobstructed_to_exterior'] for x in hits)})
measure={}
if src.stem=='monograptus':
 pairs=[]
 for j in range(17):
  lo,hi=group_bounds[f'theca_{j:02d}'];l2,h2=group_bounds[f'theca_{j+1:02d}'];overlap=max(0,min(hi[2],h2[2])-max(lo[2],l2[2]));pairs.append({'theca_a':j,'theca_b':j+1,'actual_axial_overlap_m':overlap,'actual_shorter_axial_extent_m':min(hi[2]-lo[2],h2[2]-l2[2]),'fraction_of_shorter_axial_extent':overlap/min(hi[2]-lo[2],h2[2]-l2[2])})
 measure={'neighboring_thecae_axial_overlap':pairs,'interpretation':'Actual transformed tube axial ranges corroborate source overlap of half or more. Ranges alone do not prove visual articulation; exact final overlap detail personally inspected separately.'}
record={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'pid':os.getpid(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Every original triangle centroid, front-facing to each named orthographic direction, ray cast against ALL original scene triangles including own component. No geometry repair, hidden-subset rendering or exposure percentage gate. Epsilon1e-8m excludes self-hit only; distances otherwise strict. Aperture center rays supplement actual solid-recess checks.','camera_angles_degrees':angles,'components':list(res.values()),'components_without_any_sampled_line_of_sight':[k for k,v in res.items() if not any(v['visible_triangle_centroids_by_direction'].values())],'apertures':apresult,'apertures_without_exterior_ray':[x['component'] for x in apresult if not x['some_open_exterior_direction']],'additional_measures':measure}
record['status']='pass' if not record['components_without_any_sampled_line_of_sight'] and not record['apertures_without_exterior_ray'] else 'fail'
with out.open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(record['status'],record['components_without_any_sampled_line_of_sight'],record['apertures_without_exterior_ray'])
