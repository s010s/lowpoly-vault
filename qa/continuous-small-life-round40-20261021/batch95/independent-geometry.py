import bpy,bmesh,json,sys,os,pathlib,hashlib,datetime,math,collections
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np
S=pathlib.Path('/workspace/shared/lowpoly-batch95-20261020');O=pathlib.Path('/workspace/shared/lowpoly-batch95-independent-qa-20261021');aid=sys.argv[sys.argv.index('--')+1];B=S/'production/small-life-batch95'/aid/'r002';D=O/aid;D.mkdir(exist_ok=True)
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();start=now();bpy.ops.wm.open_mainfile(filepath=str(B/'artifacts'/f'{aid}.blend'),load_ui=False,use_scripts=False);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();groups={};objects=[];allpts=[]
def bounds(v):
 lo=[min(p[i]for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)];return {'min':lo,'max':hi,'size':[hi[i]-lo[i]for i in range(3)]}
def group(v,faces):
 tree=BVHTree.FromPolygons(v,faces,all_triangles=True);adj={i:set()for i in range(len(v))}
 for f in faces:
  for i in f:adj[i].update(f)
 left=set(adj);islands=[]
 while left:
  stack=[min(left)];part=set()
  while stack:
   i=stack.pop()
   if i in part:continue
   part.add(i);stack.extend(adj[i]-part)
  left-=part;islands.append(sorted(part))
 arr=np.array(v);_,axes=np.linalg.eigh(np.cov(arr.T));local=(arr-arr.mean(axis=0))@axes
 return {'v':v,'faces':faces,'tree':tree,'islands':islands,'principal_extents':(local.max(axis=0)-local.min(axis=0)).tolist()}
for ob in bpy.context.scene.objects:
 if ob.type!='MESH':continue
 mesh=ob.data;mesh.calc_loop_triangles();v=[ob.matrix_world@p.co for p in mesh.vertices];allpts+=v;bm=bmesh.new();bm.from_mesh(mesh);bm.normal_update();ev=ob.evaluated_get(deps);em=ev.to_mesh();em.calc_loop_triangles();epts=[ev.matrix_world@x.co for x in em.vertices]
 objects.append({'name':ob.name,'world_matrix':[list(row)for row in ob.matrix_world],'authored_vertices':len(v),'authored_polygons':len(mesh.polygons),'authored_triangles':len(mesh.loop_triangles),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':len(em.loop_triangles),'authored_bounds':bounds(v),'evaluated_bounds':bounds(epts),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()==0 for f in bm.faces),'signed_volume':bm.calc_volume(signed=True),'modifiers':[m.type for m in ob.modifiers]});bm.free();ev.to_mesh_clear()
 members=collections.defaultdict(list)
 for vert in mesh.vertices:
  for w in vert.groups:
   if w.weight>0:members[w.group].append(vert.index)
 for vg in ob.vertex_groups:
  ix=members[vg.index];lookup={old:new for new,old in enumerate(ix)};fs=[tuple(lookup[i]for i in t.vertices)for t in mesh.loop_triangles if all(i in lookup for i in t.vertices)];groups[vg.name]=group([v[i]for i in ix],fs)
directions=[Vector(x).normalized()for x in [(1,.217,.413),(.367,1,.137),(.179,.317,1)]]
def inside(g,p):
 tree=g['tree'];hit,n,idx,dist=tree.find_nearest(p)
 if dist is not None and dist<1e-8:return True,'touching_surface',dist
 votes=[]
 for dr in directions:
  at=p.copy();n=0
  for _ in range(128):
   hit,normal,idx,d=tree.ray_cast(at,dr)
   if hit is None:break
   n+=1;at=hit+dr*1e-7
  votes.append(n%2==1)
 return sum(votes)>=2,votes,dist
contacts=[]
for name,g in groups.items():
 par=[]
 if name.startswith(('wedge_leaf_','divided_leaf_')):par=[x for x in groups if x=='main_axis'or x.startswith('lateral_axis_')]
 elif name.startswith('lateral_axis_')or name.startswith('root_')and not name.startswith(('root_bundle_','root_mantle_')):par=['main_axis']
 elif name.startswith('hook_'):par=['divided_leaf_'+name.split('_')[-1]]
 elif name.startswith(('root_bundle_','frond_rachis_')):par=['root_mantle_core']
 elif name.startswith('pinna_'):par=['frond_rachis_'+name.split('_')[1]]
 elif name.startswith('pinnule_'):par=['pinna_'+'_'.join(name.split('_')[1:4])]
 elif name.startswith(('major_','net_cross_')):par=['continuous_fan_lamina']
 elif name.startswith('basal_arm_'):par=['short_petiole']
 elif name.startswith(('ray_midvein_','ray_sidevein_','ray_net_')):par=['four_ray_web_'+name.split('_')[2]]
 if not par:continue
 witness=None;overlaps={};nearest=None
 for parent in par:
  pg=groups[parent]
  # Three-direction majority over actual child surface vertices, never a free centerline.
  for i,p in enumerate(g['v']):
   ok,votes,dist=inside(pg,p);nearest=dist if nearest is None else min(nearest,dist)
   if ok:witness={'parent':parent,'kind':'actual_child_vertex','index':i,'world':list(p),'votes':votes,'nearest_parent_surface_m':dist};break
  if witness:break
  for i,f in enumerate(g['faces']):
   a,b,c=[g['v'][k]for k in f]
   for label,p in [('triangle_centroid',(a+b+c)/3),('edge_mid_ab',(a+b)/2),('edge_mid_bc',(b+c)/2),('edge_mid_ca',(c+a)/2)]:
    ok,votes,dist=inside(pg,p)
    if ok:witness={'parent':parent,'kind':label,'face_index':i,'world':list(p),'votes':votes,'nearest_parent_surface_m':dist};break
   if witness:break
  if witness:break
  overlaps[parent]=len(g['tree'].overlap(pg['tree']))
 contacts.append({'child':name,'tested_parents':par,'witness':witness,'overlap_pairs_if_no_witness':overlaps,'nearest_surface_m':nearest,'physical_contact':bool(witness)or any(overlaps.values())})
counts={p:sum(n.startswith(p)for n in groups)for p in ['main_axis','lateral_axis_','wedge_leaf_','divided_leaf_','hook_','root_','root_bundle_','frond_rachis_','pinna_','pinnule_','continuous_fan_lamina','major_initial_','major_mid_','major_terminal_','net_cross_','short_petiole','basal_arm_','four_ray_web_','ray_midvein_','ray_sidevein_','ray_net_']}
checks={'topology':all(o['nonmanifold_edges']==0 and o['zero_area_faces']==0 for o in objects),'all_parent_interfaces_contact':all(c['physical_contact']for c in contacts),'full_expected_contact_count':len(contacts)==dict(sphenophyllum=108,psaronius=1258,hausmannia=103,dictyophyllum=186)[aid]};hierarchy={}
if aid=='sphenophyllum':
 checks.update(exact_counts=counts['main_axis']==1 and counts['lateral_axis_']==3 and counts['wedge_leaf_']==88 and counts['divided_leaf_']==8 and counts['hook_']==4 and counts['root_']==5,divided_two_islands=all(len(g['islands'])==2 for n,g in groups.items()if n.startswith('divided_leaf_')))
 # Derive whorl clusters from leaf base geometry, not design properties. Bases may move fractionally into axial tube.
 bases=[]
 for n,g in groups.items():
  if n.startswith('wedge_leaf_'):p=(g['v'][0]+g['v'][11]+g['v'][12]+g['v'][23])/4
  elif n.startswith('divided_leaf_'):p=g['v'][0]
  else:continue
  bases.append((n,p))
 clusters=[]
 for n,p in bases:
  match=next((x for x in clusters if(p-x['p']).length<.0003),None)
  if match:match['names'].append(n)
  else:clusters.append({'p':p,'names':[n]})
 hierarchy['base_clusters']=[{'base':list(x['p']),'members':x['names']}for x in clusters];checks['16_six_leaf_whorls']=len(clusters)==16 and all(len(x['names'])==6 for x in clusters)
if aid=='psaronius':
 checks['exact_counts']=counts['root_bundle_']==18 and counts['frond_rachis_']==8 and counts['pinna_']==112 and counts['pinnule_']==1120
 hierarchy['pinnae_per_frond']={n:sum(c['physical_contact'] and c['child'].startswith('pinna_')and c['tested_parents']==[n]for c in contacts)for n in groups if n.startswith('frond_rachis_')};hierarchy['pinnules_per_pinna']={n:sum(c['physical_contact'] and c['child'].startswith('pinnule_')and c['tested_parents']==[n]for c in contacts)for n in groups if n.startswith('pinna_')};checks['14_pinnae_each_frond']=all(v==14 for v in hierarchy['pinnae_per_frond'].values());checks['10_pinnules_each_pinna']=all(v==10 for v in hierarchy['pinnules_per_pinna'].values())
if aid=='hausmannia':
 checks['exact_counts']=counts['continuous_fan_lamina']==1 and counts['major_initial_']==4 and counts['major_mid_']==8 and counts['major_terminal_']==16 and counts['net_cross_']==75
 g=groups['continuous_fan_lamina'];v=g['v'];base=v[0];ring=v[1+4*129:1+5*129];rad=[math.hypot(p.x-base.x,p.z-base.z)for p in ring];peaks=[i for i in range(1,len(rad)-1)if rad[i]>rad[i-1]and rad[i]>rad[i+1]];hierarchy['margin_radial_peaks']=peaks;checks['16_margin_teeth']=len(peaks)==16
if aid=='dictyophyllum':
 checks['exact_counts']=counts['short_petiole']==1 and counts['basal_arm_']==2 and counts['four_ray_web_']==2 and counts['ray_midvein_']==8 and counts['ray_sidevein_']==96 and counts['ray_net_']==80;checks['single_continuous_web_each_side']=all(len(g['islands'])==1 for n,g in groups.items()if n.startswith('four_ray_web_'));hierarchy['rays_per_arm']={str(s):sum(n.startswith('ray_midvein_'+str(s)+'_')for n in groups)for s in [-1,1]};checks['four_rays_each_arm']=all(x==4 for x in hierarchy['rays_per_arm'].values())
# Reexport reopened source, not the generator, with same explicit export policy. No maker writes.
bpy.ops.object.select_all(action='DESELECT')
collection=next(c for c in bpy.data.collections if c.get('asset_root'))
for ob in collection.all_objects:ob.select_set(True)
opt=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(filepath=str(D/'independent-reexport.glb'),**opt)
d={'asset_id':aid,'revision':'r002','started_at':start,'finished_at':now(),'pid':os.getpid(),'argv':sys.argv,'blender':bpy.app.version_string,'source_sha256':H(B/'artifacts'/f'{aid}.blend'),'glb_sha256':H(B/'artifacts'/f'{aid}.glb'),'reexport_sha256':H(D/'independent-reexport.glb'),'reexport_byte_identical':H(B/'artifacts'/f'{aid}.glb')==H(D/'independent-reexport.glb'),'objects':objects,'world_bounds_blender_m':bounds(allpts),'counts':counts,'component_bounds':{n:{'vertices':len(g['v']),'triangles':len(g['faces']),'closed_islands':len(g['islands']),'bounds':bounds(g['v']),'principal_axis_extents_m':g['principal_extents']}for n,g in groups.items()},'contacts':contacts,'hierarchy':hierarchy,'checks':checks,'pass':all(checks.values()),'method_limits':'Read-only actual transformed mesh audit; closed-volume surface samples with three-ray-majority parity or exact BVH triangle overlaps establish physical contact. No free centers count as geometry. Numerical 1e-8 surface and 1e-7 ray advances are computational epsilons, not new artistic size limits. Visual quality separately judged. GPU/composed scene unrun.'}
(D/'independent-geometry.json').write_text(json.dumps(d,indent=2)+'\n');print(aid,checks,'reexport-identical',d['reexport_byte_identical'])
