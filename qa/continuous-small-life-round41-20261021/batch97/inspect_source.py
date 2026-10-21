import bpy,bmesh,json,hashlib,pathlib,sys,math,os,datetime,collections,itertools
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
W=pathlib.Path('/workspace/shared/lowpoly-batch97-20261020');B=W/'production/small-life-batch97';O=pathlib.Path(__file__).parent
sys.path.insert(0,str(W/'scripts'));from qa_glb import audit_glb;from asset_common import audit_source
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
aid=sys.argv[sys.argv.index('--')+1];rev={'ginkgo':'r002','dicranophyllum':'r003','noeggerathia':'r002','bjuvia':'r001'}[aid];d=B/aid/rev;out=O/aid;src=d/'artifacts'/f'{aid}.blend';glb=d/'artifacts'/f'{aid}.glb';brief=json.loads((B/aid/'r001/original-brief.json').read_text())
bpy.context.preferences.filepaths.use_scripts_auto_execute=False;bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();obs=[o for o in bpy.data.objects if o.type=='MESH'];assert len(obs)==1;obj=obs[0];v=[obj.matrix_world@x.co for x in obj.data.vertices];obj.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in obj.data.loop_triangles];groups={vg.name:[] for vg in obj.vertex_groups}
for vertex in obj.data.vertices:
 for gg in vertex.groups:groups[obj.vertex_groups[gg.group].name].append(vertex.index)
lo=[min(x[k] for x in v) for k in range(3)];hi=[max(x[k] for x in v) for k in range(3)];sz=[hi[k]-lo[k] for k in range(3)];extent=max(sz);eps=extent*1e-8
owner={i:tag for tag,ids in groups.items() for i in ids};assert len(owner)==len(v);tby=collections.defaultdict(list)
for i,t in enumerate(tris):
 tags={owner[k] for k in t};assert len(tags)==1;tby[tags.pop()].append(i)
trees={tag:BVHTree.FromPolygons(v,[tris[i] for i in tby[tag]],all_triangles=True,epsilon=0) for tag in groups};whole=BVHTree.FromPolygons(v,tris,all_triangles=True,epsilon=0)
adj={i:set() for i in range(len(v))}
for e in obj.data.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
def islands(ids):
 left=set(ids);parts=[]
 while left:
  first=min(left);left.remove(first);todo=[first];part=[first]
  while todo:
   for q in adj[todo.pop()]:
    if q in left:left.remove(q);todo.append(q);part.append(q)
  parts.append(sorted(part))
 return parts
def signed(p,tree):
 q,n,_,_=tree.find_nearest(p);return float((p-q).dot(n))
def parity(p,tree):
 ds=[Vector((.32731,.47677,.81513)).normalized(),Vector((-.713,.326,.591)).normalized(),Vector((.313,-.823,.471)).normalized()];counts=[]
 for ray in ds:
  q=p.copy();count=0
  for _ in range(100):
   hit,_,idx,_=tree.ray_cast(q,ray,extent*4)
   if idx is None:break
   count+=1;q=hit+ray*max(eps,extent*2e-7)
  counts.append(count%2)
 return sum(counts)>=2,counts
directions=[Vector(q).normalized() for q in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(1,1,1),(-1,-1,1),(1,-1,1),(-1,1,1)]]
def visible(triangle_ids):
 tests=0
 for ti in triangle_ids:
  a,b,c=[v[i] for i in tris[ti]];n=(b-a).cross(c-a).normalized();p=(a+b+c)/3
  for ray in [n,*directions]:
   if ray.dot(n)<=.05:continue
   tests+=1;hit,_,idx,_=whole.ray_cast(p+ray*eps,ray,extent*4)
   if idx is None:return {'triangle':ti,'centroid':list(p),'direction':list(ray),'rays_tested':tests}
 return {'triangle':None,'rays_tested':tests}
records=[];relations={x['child']:x['parent'] for x in json.loads(obj.get('contact_design','[]'))};all_islands={tag:islands(ids) for tag,ids in groups.items()}
for tag,ids in groups.items():
 pts=np.array([v[i] for i in ids],dtype=float);c=pts-pts.mean(axis=0);_,axes=np.linalg.eigh(np.cov(c.T));proj=c@axes;mins=pts.min(axis=0);maxs=pts.max(axis=0);sizes=maxs-mins
 r={'tag':tag,'vertices':len(ids),'triangles':len(tby[tag]),'islands':len(all_islands[tag]),'world_bounds':{'min':mins.tolist(),'max':maxs.tolist(),'size':sizes.tolist()},'pca_extents_m':(proj.max(axis=0)-proj.min(axis=0)).tolist(),'finite_positive_extents':bool(np.isfinite(sizes).all() and (sizes>0).all()),'within_global_bounds':all(mins[k]>=lo[k] and maxs[k]<=hi[k] for k in range(3)),'max_extent_within_global_hard_max':max(sizes)<=max(x[1] for x in brief['scale']['hard_world_bbox_size_ranges_xyz_m']),'whole_surface_witness':visible(tby[tag])}
 if tag in relations:
  parent=relations[tag];tree=trees[parent];distances=[signed(v[i],tree) for i in ids];witness=None
  for i,ds in zip(ids,distances):
   if ds < -eps:
    inside,counts=parity(v[i],tree)
    if inside:witness={'child_vertex':i,'point':list(v[i]),'signed_distance_m':ds,'three_ray_parity':counts};break
  if witness is None:
   for ti in tby[tag]:
    p=sum([v[i] for i in tris[ti]],Vector())/3;ds=signed(p,tree)
    if ds < -eps:
     inside,counts=parity(p,tree)
     if inside:witness={'child_triangle_centroid':ti,'point':list(p),'signed_distance_m':ds,'three_ray_parity':counts};break
  r.update(parent=parent,contact_inside_witness=witness,parent_signed_distance_range_m=[min(distances),max(distances)],parent_exposed_vertices=sum(x>eps for x in distances))
 records.append(r)
bm=bmesh.new();bm.from_mesh(obj.data);topo={'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'boundary_edges':sum(len(e.link_faces)==1 for e in bm.edges),'nonmanifold_edges':sum(len(e.link_faces)!=2 for e in bm.edges),'zero_area_faces':sum(f.calc_area()<=1e-15 for f in bm.faces)};bm.free()
features={};extra={}
if aid=='ginkgo':
 ids=groups['six_lobed_lamina'];pts=[v[i] for i in ids[:len(ids)//2]];base=(pts[0]+pts[-1])/2;radius=[(p-base).length for p in pts];peaks=[i for i in range(1,len(pts)-1) if radius[i]>radius[i-1] and radius[i]>radius[i+1]];valleys=[i for i in range(1,len(pts)-1) if radius[i]<radius[i-1] and radius[i]<radius[i+1]]
 features={'radial_margin_peaks':len(peaks),'peak_indices':peaks,'radial_sinus_indices':valleys,'sinus_radii_m':[radius[i] for i in valleys],'lamina_closed_islands':len(all_islands['six_lobed_lamina']),'petiole_closed_islands':len(all_islands['petiole'])};segments=[]
 for tag,parts in all_islands.items():
  if not tag.startswith('radiating_vein_'):continue
  for n,ids in enumerate(parts):
   ring=[]
   for j in range(0,len(ids),5):
    ds=[signed(v[i],trees['six_lobed_lamina']) for i in ids[j:j+5]];ring.append({'ring':j//5,'minimum_signed_distance_m':min(ds),'maximum_signed_distance_m':max(ds),'crosses':min(ds)<-eps and max(ds)>eps})
   ids_set=set(ids);ti=[i for i in tby[tag] if all(q in ids_set for q in tris[i])];segments.append({'group':tag,'segment':n,'ring_count':len(ring),'rings':ring,'all_rings_cross':all(x['crosses'] for x in ring),'whole_surface_witness':visible(ti)})
 extra['ginkgo_segments']=segments;features['vein_segments']=len(segments);features['all_378_rings_cross']=all(s['all_rings_cross'] for s in segments)
elif aid=='dicranophyllum':
 leaves=[]
 for tag,parts in all_islands.items():
  if not tag.startswith('leaf_'):continue
  nodes=[];edges=[]
  def node(p):
   for i,q in enumerate(nodes):
    if (p-q).length<extent*1e-7:return i
   nodes.append(p);return len(nodes)-1
  for part in parts:edges.append((node(sum([v[i] for i in part[:4]],Vector())/4),node(sum([v[i] for i in part[-4:]],Vector())/4)))
  deg=[sum(i in e for e in edges) for i in range(len(nodes))];roots=[i for i in range(len(nodes)) if deg[i]==1];root=min(roots,key=lambda i:nodes[i].z);tips=[nodes[i] for i in roots if i!=root];dist=[(p-q).length for p,q in itertools.combinations(tips,2)];leaves.append({'tag':tag,'islands':len(parts),'edges':edges,'node_positions':[list(p) for p in nodes],'degree':deg,'tips':len(tips),'forks':deg.count(3),'tip_pair_distance_min_m':min(dist),'tip_positions':[list(p) for p in tips]})
 features={'leaves':len(leaves),'terminal_tips':sum(x['tips'] for x in leaves),'forks':sum(x['forks'] for x in leaves),'all_have_four_tips_three_forks':all(x['tips']==4 and x['forks']==3 and len(x['edges'])==7 for x in leaves),'minimum_tip_separation_m':min(x['tip_pair_distance_min_m'] for x in leaves),'leaf_cushions':sum(k.startswith('cushion_') for k in groups),'axes':len(all_islands['slender_axis'])};extra['leaf_graphs']=leaves
elif aid=='noeggerathia':
 leaves=[k for k in groups if k.startswith('pinnule_')];features={'pinnules':len(leaves),'pinnule_solid_islands':sum(len(all_islands[k]) for k in leaves),'vein_systems':sum(k.startswith('fan_veins_') for k in groups),'rachis_islands':len(all_islands['rachis'])};extra['pinnule_outlines']=[{'tag':k,'front_outline_world':[list(v[i]) for i in groups[k][:len(groups[k])//2]]} for k in leaves]
elif aid=='bjuvia':
 veins=[k for k in groups if k.startswith('transverse_vein_')];features={'lamina_islands':len(all_islands['entire_strap_lamina']),'midrib_islands':len(all_islands['midrib']),'lateral_islands':sum(len(all_islands[k]) for k in veins),'rows':len({k.split('_')[2] for k in veins}),'all_laterals_single_three_ring_tubes':all(len(groups[k])==12 and len(all_islands[k])==1 for k in veins)}
 # Verify no physical intersections between different lateral rows, rather than trust absence of a crossvein tag.
 intersections=[]
 for a,b in itertools.combinations(veins,2):
  if a.split('_')[2]==b.split('_')[2]:continue
  if trees[a].overlap(trees[b]):intersections.append([a,b])
 extra['different_lateral_row_surface_intersections']=intersections
collections_=[c for c in bpy.data.collections if c.get('asset_root')];assert len(collections_)==1;col=collections_[0];sa=audit_source(col,14000);dg=bpy.context.evaluated_depsgraph_get();ev=obj.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();counts={'authored_vertices':len(obj.data.vertices),'authored_polygons':len(obj.data.polygons),'authored_triangles':len(obj.data.loop_triangles),'evaluated_vertices':len(me.vertices),'evaluated_polygons':len(me.polygons),'evaluated_triangles':len(me.loop_triangles)};ev.to_mesh_clear()
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']];exp=out/'source-reexport.glb'
bpy.ops.export_scene.gltf(filepath=str(exp),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
a=audit_glb(glb,14000,6,30);e=audit_glb(exp,14000,6,30);ranges=brief['scale']['hard_world_bbox_size_ranges_xyz_m'];hard=[{'axis':k,'actual_size_m':sz[k],'range':ranges[k],'passes_exact':ranges[k][0]<=sz[k]<=ranges[k][1],'distance_to_lower_m':sz[k]-ranges[k][0],'distance_to_upper_m':ranges[k][1]-sz[k]} for k in range(3)]
r={'asset_id':aid,'revision':rev,'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'blender_version':bpy.app.version_string,'source_sha256':H(src),'glb_sha256':H(glb),'original_brief_sha256':H(B/aid/'r001/original-brief.json'),'source_reopened':True,'source_saved':False,'object_matrix':[list(x) for x in obj.matrix_world],'world_bounds':{'min':lo,'max':hi,'size':sz},'hard_envelope_exact':hard,'float_policy':'Source vertices are binary32. Each world coordinate converted to Python float before min/max subtraction. Constraints are tested exactly against frozen bounds, with no blanket tolerance or altered freeze; all margin deltas reported. Ray-start epsilon is geometric query robustness only, never dimension allowance.','ray_start_epsilon_m':eps,'source_counts':counts,'topology':topo,'components':records,'component_count':len(records),'features':features,**extra,'source_audit':sa,'missing_contact_witnesses':[r['tag'] for r in records if 'parent' in r and r['contact_inside_witness'] is None],'wholly_parent_buried':[r['tag'] for r in records if r.get('parent_exposed_vertices',1)==0],'no_whole_surface_witness':[r['tag'] for r in records if r['whole_surface_witness']['triangle'] is None],'visibility_limit':'Every component is tested against the complete transformed mesh with actual triangle-centroid outward rays; positive samples establish geometric exposure, not pixel-scale recognizability. Pixel review is separate.','reexport':{'path':str(exp),'sha256':H(exp),'semantic_sha256':e['semantic_sha256'],'original_semantic_sha256':a['semantic_sha256'],'semantic_equal':e['semantic_sha256']==a['semantic_sha256'],'byte_equal':H(exp)==H(glb),'errors':e['errors']}}
(out/'source-independent.json').write_text(json.dumps(r,indent=2,default=lambda x:x.item() if hasattr(x,"item") else str(x))+'\n');print(json.dumps({k:r[k] for k in ['asset_id','component_count','features','hard_envelope_exact','missing_contact_witnesses','wholly_parent_buried','no_whole_surface_witness','reexport']},indent=2))
