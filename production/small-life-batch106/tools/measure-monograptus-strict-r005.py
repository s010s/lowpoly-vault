#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only actual source, complete solid union exposure, and direct GLB orientation audit."""
import sys,json,hashlib,datetime,os,math,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from check_source_export import main
main()
import bpy,bmesh,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform
args=sys.argv[sys.argv.index('--')+1:];source=Path(args[args.index('--source')+1]);glb=Path(args[args.index('--glb')+1]);out=Path(args[args.index('--output')+1]).parent;aid=source.stem;now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 v.update(source_sha256=h(source),glb_sha256=h(glb),measured_at=now(),pid=os.getpid());(out/n).open('x').write(json.dumps(v,indent=2)+'\n')
class StrictSolid:
 def __init__(self,verts,polys,**kw):
  self.tree=BVHTree.FromPolygons(verts,polys,**kw)
  self.tri=np.array([[list(verts[i]) for i in t] for t in polys],dtype=np.float64)
  self.epsilon=64*np.finfo(np.float64).eps*max(1e-3,float(np.max(np.abs(self.tri))))
 def ray_cast(self,*a):return self.tree.ray_cast(*a)
 def find_nearest(self,*a):return self.tree.find_nearest(*a)
def inside(pt,tree):
 # Source is float32, but stored coordinates are exact inputs to float64 proof.
 # In particular, sample centroids below are computed in float64, not mathutils
 # float32: a rounded centroid must not move a boundary witness into a solid.
 p=np.array(pt,dtype=np.float64);tri=tree.tri;a,b,c=tri[:,0],tri[:,1],tri[:,2];ab=b-a;ac=c-a;n=np.cross(ab,ac);nn=np.einsum('ij,ij->i',n,n);ap=p-a;plane=np.einsum('ij,ij->i',ap,n);proj=ap-n*(plane/nn)[:,None]
 d00=np.einsum('ij,ij->i',ab,ab);d01=np.einsum('ij,ij->i',ab,ac);d11=np.einsum('ij,ij->i',ac,ac);d20=np.einsum('ij,ij->i',proj,ab);d21=np.einsum('ij,ij->i',proj,ac);den=d00*d11-d01*d01;u=(d11*d20-d01*d21)/den;v=(d00*d21-d01*d20)/den
 dd=np.where((u>=0)&(v>=0)&(u+v<=1),plane*plane/nn,np.inf)
 for x,y in [(a,b),(b,c),(c,a)]:
  e=y-x;q=p-x;t=np.clip(np.einsum('ij,ij->i',q,e)/np.einsum('ij,ij->i',e,e),0,1);dist=q-e*t[:,None];dd=np.minimum(dd,np.einsum('ij,ij->i',dist,dist))
 if float(dd.min())<=tree.epsilon**2:return False
 x,y,z=a-p,b-p,c-p;nx=np.linalg.norm(x,axis=1);ny=np.linalg.norm(y,axis=1);nz=np.linalg.norm(z,axis=1);num=np.einsum('ij,ij->i',x,np.cross(y,z));den=nx*ny*nz+np.einsum('ij,ij->i',x,y)*nz+np.einsum('ij,ij->i',y,z)*nx+np.einsum('ij,ij->i',z,x)*ny;w=float(np.arctan2(num,den).sum()/(2*math.pi))
 return abs(abs(w)-1)<1e-7
parts=[];measures=[];contact=[];exposure=[];topology=[];features={};allpts=[];groupdata={};degenerate=[];aperture_results=[];dg=bpy.context.evaluated_depsgraph_get()
for ob in bpy.data.objects:
 if ob.type!='MESH':continue
 me=ob.data;me.calc_loop_triangles();ev=ob.evaluated_get(dg);em=ev.to_mesh();em.calc_loop_triangles();parts.append({'name':ob.name,'authored_vertices':len(me.vertices),'authored_polygons':len(me.polygons),'authored_triangles':len(me.loop_triangles),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':len(em.loop_triangles),'modifier_count':len(ob.modifiers)});ev.to_mesh_clear()
 verts=[ob.matrix_world@v.co for v in me.vertices];allpts+=verts;tris=[tuple(t.vertices) for t in me.loop_triangles];groups={vg.name:[] for vg in ob.vertex_groups}
 for v in me.vertices:
  for gg in v.groups:groups[ob.vertex_groups[gg.group].name].append(v.index)
 trees={};bounds={};gtris={};samples={};island_ids={};adj=collections.defaultdict(set)
 for e in me.edges:
  a,b=e.vertices;adj[a].add(b);adj[b].add(a)
 for tag,ids in groups.items():
  ss=set(ids);tt=[t for t in tris if set(t)<=ss];gtris[tag]=tt;trees[tag]=StrictSolid(verts,tt,all_triangles=True,epsilon=0);vv=np.array([verts[i] for i in ids]);lo=vv.min(0);hi=vv.max(0);bounds[tag]=(lo,hi);_,axes=np.linalg.eigh(np.cov(vv.T));loc=(vv-vv.mean(0))@axes;ext=loc.max(0)-loc.min(0);left=set(ids);islands=[]
  while left:
   s=min(left);todo=[s];piece={s};left.remove(s)
   while todo:
    for j in adj[todo.pop()]:
     if j in left:left.remove(j);piece.add(j);todo.append(j)
   islands.append(piece)
  island_ids[tag]=islands
  edges=collections.defaultdict(list);vol=0;zero=[]
  for ti,t in enumerate(tt):
   a,b,c=[verts[i] for i in t];vol+=a.dot(b.cross(c))/6
   if (b-a).cross(c-a).length<1e-18:zero.append(ti)
   for a,b in zip(t,t[1:]+t[:1]):edges[tuple(sorted((a,b)))].append((a,b))
  bad=[k for k,v in edges.items() if len(v)!=2];same=[k for k,v in edges.items() if len(v)==2 and v[0]==v[1]]
  topology.append({'component':tag,'connected_islands':len(islands),'vertices':len(ids),'triangles':len(tt),'nonmanifold_edge_count':len(bad),'same_direction_shared_edge_count':len(same),'signed_volume_m3':vol,'zero_area_triangles':zero,'pass':not bad and not same and not zero and vol>0})
  item={'component':tag,'vertices':len(ids),'triangles':len(tt),'connected_islands':len(islands),'world_bounds_blender_m':{'min':lo.tolist(),'max':hi.tolist(),'size':(hi-lo).tolist()},'principal_axis_extents_m':ext.tolist(),'transform_scale':list(ob.scale)};measures.append(item);groupdata[tag]=(ids,tt,verts)
  samples[tag]=[('vertex',i,verts[i]) for i in ids]+[('triangle_centroid',k,np.mean(np.array([list(verts[i]) for i in t],dtype=np.float64),axis=0)) for k,t in enumerate(tt)]
 for rel in json.loads(ob.get('contact_design','[]')):
  ch,par=rel['child'],rel['parent'];hits=[{'sample_kind':kind,'sample_index':idx,'world':list(pt)} for kind,idx,pt in samples[ch] if inside(pt,trees[par])]
  reverse_hits=[{'sample_kind':kind,'sample_index':idx,'world':list(pt)} for kind,idx,pt in samples[par] if inside(pt,trees[ch])]
  island_contact=[]
  for island in island_ids[ch]:
   forward=any((hit['sample_index'] in island if hit['sample_kind']=='vertex' else gtris[ch][hit['sample_index']][0] in island) for hit in hits)
   island_tree=StrictSolid(verts,[t for t in gtris[ch] if t[0] in island],all_triangles=True,epsilon=0)
   backward=any(inside(Vector(hit['world']),island_tree) for hit in reverse_hits)
   island_contact.append(forward or backward)
  contact.append({'child':ch,'parent':par,'actual_child_geometry_sample_inside_parent':all(island_contact),'sample_count':len(samples[ch])+len(samples[par]),'witnesses':hits[:3],'reverse_parent_inside_child_witnesses':reverse_hits[:3],'each_child_island_inside_witness':island_contact,'method':'Strict positive-volume intersection is symmetric: actual surface sample strictly inside other solid; checked per child island in either direction, no distance tolerance contact.'})
 for tag,sp in samples.items():
  exposed=[];buried=collections.Counter();vertex_flags=[]
  for kind,idx,pt in sp:
   oc=[]
   for other,(lo,hi) in bounds.items():
    if other==tag or any(pt[k]<lo[k]-1e-11 or pt[k]>hi[k]+1e-11 for k in range(3)):continue
    if inside(pt,trees[other]):oc.append(other)
   if not oc:exposed.append((kind,idx,list(pt)))
   else:buried.update(oc)
   if kind=='vertex':vertex_flags.append(not oc)
  zones=[]
  # Every ring of each required pod/arm, not merely one exposed vertex for the whole organ.
  step=6 if tag.startswith('pod_') else 7 if tag.startswith('arm_') else None
  if step:
   zones=[{'ring':j//step,'samples':len(vertex_flags[j:j+step]),'vertices_outside_all_other_solids':sum(vertex_flags[j:j+step])} for j in range(0,len(vertex_flags),step)]
  island_exposure=[any((idx in island if kind=='vertex' else gtris[tag][idx][0] in island) for kind,idx,pt in exposed) for island in island_ids[tag]]
  exposure.append({'each_closed_island_has_global_exposure_sample':island_exposure,'component':tag,'actual_surface_samples':len(sp),'global_exposed_samples':len(exposed),'global_exposed_fraction':len(exposed)/len(sp),'sample_exposed_witnesses':exposed[:3],'buried_by_counts':dict(buried),'not_wholly_buried_by_union':bool(exposed) and all(island_exposure),'ring_diagnostics':zones})
 # Aperture witnesses are actual original-scene ray casts, not dark material labels.
 for ap in json.loads(ob.get('aperture_design','[]')):
  tag=ap['component'];pt=Vector(ap['center']);direction=Vector(ap['direction']).normalized();eps=1e-8
  own=trees[tag];inner=pt-direction*eps;blocked=[other for other,tr in trees.items() if inside(inner,tr)]
  loc,normal,index,depth=own.ray_cast(inner,-direction,1)
  forward=[]
  for other,tr in trees.items():
   pos,n,ix,dist=tr.ray_cast(pt+direction*eps,direction,1)
   if pos is not None:forward.append({'component':other,'distance_m':dist})
  aperture_results.append({'component':tag,'mouth_center_world_m':list(pt),'axis':list(direction),'mouth_in_other_or_own_solid':blocked,'actual_axis_recess_m':depth if loc is not None else None,'inward_hit_component':tag if loc is not None else None,'inward_hit_world_m':list(loc) if loc is not None else None,'outward_ray_hits_sorted':sorted(forward,key=lambda x:x['distance_m'])[:3],'actual_open_recess':not blocked and loc is not None and depth>eps,'limits':'Axis probes demonstrate real recessed geometry; oblique visible pixels determine readable exposure. Infinite outward obstruction is diagnostic, not an arbitrary acceptance percentage.'})
# Exact selected diagnostic feature counts, from reopened original geometry.
prefixes={'didymograptus':['stipe_','theca_','sicula'],'monograptus':['theca_','stipe','sicula','nema'],'diplograptus':['theca_','first_pair_spine_','sicula','virgella','nema'],'dictyonema':['stipe_0_','stipe_1_','stipe_2_','thecal_bridge_','aperture_']}
for pre in prefixes[aid]:features[pre.rstrip('_')]=sum(x['connected_islands'] for x in measures if x['component'].startswith(pre))
checks=[]
def gate(name,actual,lo,hi):checks.append({'measure':name,'actual':actual,'range':[lo,hi],'pass':lo<=actual<=hi})
expected={'didymograptus':{'stipe':2,'theca':52,'sicula':1},'monograptus':{'theca':18,'stipe':1,'sicula':1,'nema':1},'diplograptus':{'theca':20,'first_pair_spine':2,'sicula':1,'virgella':1,'nema':1},'dictyonema':{'stipe_0':16,'stipe_1':32,'stipe_2':64,'thecal_bridge':224,'aperture':48}}
for n,v in expected[aid].items():gate(n,features[n],v,v)
feature_details={'limits':'Counts are physically connected original mesh islands; ropy relief, hooked morphology and overlapping tubular segments are visual structures and not inferred merely from group labels or counts.'}
save('actual-aperture-recesses.json',{'items':aperture_results,'failed':[x['component'] for x in aperture_results if not x['actual_open_recess']],'method':'Mouth center and axis from authored semantic metadata; actual first inward intersections and solid-occupancy computed against reopened untouched source BVHs.'})
lo=[min(p[k] for p in allpts) for k in range(3)];hi=[max(p[k] for p in allpts) for k in range(3)]
save('authored-evaluated-counts.json',{'parts':parts,'totals':{k:sum(p[k] for p in parts) for k in ['authored_vertices','authored_polygons','authored_triangles','evaluated_vertices','evaluated_polygons','evaluated_triangles']},'source_saved':False})
save('actual-mesh-topology.json',{'components':topology,'status':'pass' if all(x['pass'] for x in topology) else 'fail','method':'Original reopened source indexed directed triangle edges and signed volume; no repair or vertex welding.'})
save('world-components-and-contacts.json',{'world_component_measurements':measures,'physical_contact_tests':contact,'contact_witness_counts':{'tested':len(contact),'with_inside_witness':sum(x['actual_child_geometry_sample_inside_parent'] for x in contact),'without_witness':sum(not x['actual_child_geometry_sample_inside_parent'] for x in contact)},'method':'Actual transformed original source groups, each checked as closed connected solid. Contact tests actual vertices and triangle centroids strictly inside the other true solid by float64 generalized winding plus exact triangle-distance boundary rejection, in both directions; triangle-centroid samples computed in float64, per child island.'})
save('global-component-exposure.json',{'items':exposure,'wholly_buried':[x['component'] for x in exposure if not x['not_wholly_buried_by_union']],'method':'Every actual vertex and actual triangle centroid tested against union of ALL OTHER closed solids, AABB pruning. Ring diagnostics added for pods/arms. No arbitrary fraction acceptance gate. Sampling is not exhaustive visibility; exact final pixels must also be viewed.'})
save('hard-dimension-check.json',{'checks':checks,'status':'pass' if all(x['pass'] for x in checks) else 'fail','actual_final_world_bbox_blender_m':{'min':lo,'max':hi,'size':[hi[k]-lo[k] for k in range(3)]},'no_rescaling':True,'interpretation':'Art targets are nominal; only source ranges and explicit diagnostic counts gated.'})
save('actual-feature-counts.json',{'counts':features,'actual_integral_feature_details':feature_details,'limits':'Selected original-source connected solids counted by memberships. Counts do not prove visible morphological identity.'})
# Decode ORIGINAL GLB, keeping all original triangle order/winding. Co-located keys
# only identify shared geometric edges after material/normal vertex splits. No normals
# are recalculated, no triangles modified, no welded diagnostic geometry substituted.
doc,binary,_=read_glb(glb);triangles=[]
identity=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
def walk(i,parent):
 nd=doc['nodes'][i];mat=matmul(parent,node_matrix(nd))
 if 'mesh' in nd:
  for pr in doc['meshes'][nd['mesh']]['primitives']:
   vv=[tuple(transform(mat,p)) for p in accessor_values(doc,binary,pr['attributes']['POSITION'])];ind=[x[0] for x in accessor_values(doc,binary,pr['indices'])] if 'indices' in pr else list(range(len(vv)))
   for j in range(0,len(ind),3):triangles.append(tuple(vv[k] for k in ind[j:j+3]))
 for ch in nd.get('children',[]):walk(ch,mat)
for i in doc['scenes'][doc.get('scene',0)]['nodes']:walk(i,identity)
edges=collections.defaultdict(list);zs=[];signed=0;vkeys={};vlist=[];ts=[]
for ti,tt in enumerate(triangles):
 # Exact IEEE decoded coordinates, not a spatial-tolerance weld.
 for p in tt:
  if p not in vkeys:vkeys[p]=len(vlist);vlist.append(p)
 ids=tuple(vkeys[p] for p in tt);ts.append(ids);a,b,c=map(Vector,tt);signed+=a.dot(b.cross(c))/6
 if (b-a).cross(c-a).length<1e-18:zs.append(ti)
 for a,b in zip(ids,ids[1:]+ids[:1]):edges[tuple(sorted((a,b)))].append((a,b,ti))
bad=[k for k,v in edges.items() if len(v)!=2];same=[k for k,v in edges.items() if len(v)==2 and v[0][:2]==v[1][:2]]
# Connected geometric edge islands expose negative caps even when aggregate volume positive.
adj=collections.defaultdict(set)
for es in edges.values():
 for a in es:
  for b in es:adj[a[2]].add(b[2])
left=set(range(len(ts)));island_vol=[]
while left:
 i=min(left);left.remove(i);todo=[i];seen=[i]
 while todo:
  for j in adj[todo.pop()]:
   if j in left:left.remove(j);todo.append(j);seen.append(j)
 vol=sum(Vector(triangles[j][0]).dot(Vector(triangles[j][1]).cross(Vector(triangles[j][2])))/6 for j in seen);island_vol.append({'triangle_count':len(seen),'signed_volume_m3':vol})
status='pass' if not bad and not same and not zs and all(v['signed_volume_m3']>0 for v in island_vol) else 'fail'
save('original-glb-winding.json',{'status':status,'method':'Direct original GLB triangle decode. Exact coordinate keys only for detecting geometric sharing across normals/material seams; no mesh changes, no normal recalculation. Original winding retained.','triangles':len(triangles),'exact_coordinate_vertices':len(vlist),'nonmanifold_geometric_edges':len(bad),'same_direction_shared_edges':len(same),'zero_area_triangles':zs,'closed_islands':island_vol,'signed_volume_sum_m3':signed})
summary={'status':'pass' if all(x['pass'] for x in topology) and not any(not x['actual_child_geometry_sample_inside_parent'] for x in contact) and not any(not x['not_wholly_buried_by_union'] for x in exposure) and all(x['pass'] for x in checks) and status=='pass' and all(x['actual_open_recess'] for x in aperture_results) else 'fail','bad_apertures':[x['component'] for x in aperture_results if not x['actual_open_recess']],'bad_contacts':[x['child'] for x in contact if not x['actual_child_geometry_sample_inside_parent']],'buried':[x['component'] for x in exposure if not x['not_wholly_buried_by_union']],'bad_topology':[x['component'] for x in topology if not x['pass']]};save('measurement-summary.json',summary);print(json.dumps(summary))
