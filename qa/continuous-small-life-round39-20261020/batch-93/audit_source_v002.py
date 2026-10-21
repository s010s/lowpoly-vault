import bpy,sys,os,json,math,hashlib,datetime,collections
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path('/workspace/shared/lowpoly-batch93-20261020');OUT=Path('/workspace/shared/lowpoly-batch93-independent-qa-20261020')
sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
from check_source_export import compare_source_audit
from asset_common import audit_source
A=sys.argv[sys.argv.index('--')+1:];aid,rev=A;dest=OUT/aid;dest.mkdir(exist_ok=True)
base=ROOT/'production/small-life-batch93'/aid/rev;src=base/'artifacts'/f'{aid}.blend';glb=base/'artifacts'/f'{aid}.glb'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
run_started=now();s0=sha(src);g0=sha(glb)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update()
cols=[c for c in bpy.data.collections if c.get('asset_root')];assert len(cols)==1
col=cols[0];dg=bpy.context.evaluated_depsgraph_get();totals=collections.Counter();objrecords=[];comps=[]
for o in col.all_objects:
 if o.type!='MESH':continue
 me=o.data;me.calc_loop_triangles();ev=o.evaluated_get(dg);em=ev.to_mesh();em.calc_loop_triangles()
 row=dict(name=o.name,authored_vertices=len(me.vertices),authored_polygons=len(me.polygons),authored_triangles=len(me.loop_triangles),evaluated_vertices=len(em.vertices),evaluated_polygons=len(em.polygons),evaluated_triangles=len(em.loop_triangles),modifiers=len(o.modifiers))
 totals.update({k:v for k,v in row.items() if isinstance(v,int)});ev.to_mesh_clear();objrecords.append(row)
 verts=[o.matrix_world@v.co for v in me.vertices];adj=[set() for v in verts]
 for e in me.edges:
  x,y=e.vertices;adj[x].add(y);adj[y].add(x)
 unseen=set(range(len(verts)))
 while unseen:
  first=min(unseen);seen={first};stack=[first];unseen.remove(first)
  while stack:
   for j in adj[stack.pop()]:
    if j in unseen:unseen.remove(j);seen.add(j);stack.append(j)
  ids=sorted(seen);im={x:j for j,x in enumerate(ids)};v=[verts[x] for x in ids];polys=[p for p in me.polygons if p.vertices[0] in seen];f=[tuple(im[x] for x in p.vertices) for p in polys];edges=collections.Counter()
  for face in f:
   for x,y in zip(face,face[1:]+face[:1]):edges[tuple(sorted((x,y)))]+=1
  lo=[min(p[k] for p in v) for k in range(3)];hi=[max(p[k] for p in v) for k in range(3)]
  rec=dict(component=len(comps),object=o.name,first_vertex=first,vertices=len(v),polygons=len(f),triangles=sum(len(x)-2 for x in f),edges=len(edges),euler=len(v)-len(edges)+len(f),boundary_edges=sum(n==1 for n in edges.values()),nonmanifold_edges=sum(n!=2 for n in edges.values()),material_indices=sorted(set(p.material_index for p in polys)),bounds_blender_m=dict(min=lo,max=hi,size=[hi[k]-lo[k] for k in range(3)]))
  comps.append(dict(rec=rec,v=v,f=f,bvh=BVHTree.FromPolygons(v,f)))
sourceaudit=audit_source(col,max_triangles=14000);exportaudit=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30)
comparison=compare_source_audit(sourceaudit,exportaudit,s0,g0)
def inside(c,p):
 votes=[]
 for d in [(1,.173,.423),(.319,1,.157),(.131,.297,1)]:
  dr=Vector(d).normalized();q=p.copy();n=0
  for _ in range(30):
   loc,normal,index,dist=c['bvh'].ray_cast(q,dr,100)
   if loc is None:break
   n+=1;q=loc+dr*1e-8
  votes.append(bool(n%2))
 return sum(votes)>=2
features={}
if aid=='omphalophloios':
 wood=[c for c in comps if c['rec']['material_indices']==[0] and c['rec']['vertices'] in [24,28,30]];trunk=next(c for c in wood if len(c['v'])==30);branch=[c for c in wood if c is not trunk];rows=[];graph=collections.defaultdict(list)
 for c in branch:
  n=len(c['v'])//4;joint=sum(c['v'][n:2*n],Vector())/n
  cand=[]
  for p in wood:
   if p is c:continue
   pn=10 if len(p['v'])==30 else len(p['v'])//4;tip=sum(p['v'][-pn:],Vector())/pn;cand.append(((tip-joint).length,p))
  dist,p=min(cand,key=lambda x:x[0]);graph[p['rec']['component']].append(c['rec']['component'])
  inc=sum(inside(p,v) for v in c['v'][:n]);overlap=len(c['bvh'].overlap(p['bvh']));minnear=min(p['bvh'].find_nearest(v)[3] for v in c['v'][:n])
  rows.append(dict(child_component=c['rec']['component'],parent_component=p['rec']['component'],joint_center_error_m=dist,base_ring_vertices=n,base_ring_inside_parent=inc,intersecting_triangle_pairs=overlap,base_vertex_nearest_parent_distance_m=minnear,volume_connected_evidence=bool(inc or overlap)))
 levels={trunk['rec']['component']:0};stack=[trunk['rec']['component']]
 while stack:
  q=stack.pop()
  for c in graph[q]:
   assert c not in levels;levels[c]=levels[q]+1;stack.append(c)
 leaves=[c for c in comps if c['rec']['material_indices'] in [[2],[3]]];sp=[c for c in comps if c['rec']['material_indices']==[4]]
 features=dict(woody_components=len(wood),branch_junctions=len(rows),woody_depth_histogram=dict(collections.Counter(levels.values())),children_histogram=dict(collections.Counter(len(graph[c['rec']['component']]) for c in wood)),terminal_axes=sum(len(c['v'])==24 for c in wood),leaf_components=len(leaves),sporangia_components=len(sp),root_components=sum(c['rec']['vertices']==20 for c in comps),all_joint_centers_match=all(r['joint_center_error_m']<1e-6 for r in rows),all_junctions_have_volume_connection=all(r['volume_connected_evidence'] for r in rows),all_base_rings_fully_inside_parent=all(r['base_ring_inside_parent']==r['base_ring_vertices'] for r in rows),junctions=rows)
if aid in ['nathorstiana','chaloneria']:
 stem=next(c for c in comps if c['rec']['vertices']==(288 if aid=='nathorstiana' else 96));leaves=[c for c in comps if c['rec']['material_indices'] in [[2],[3]]];rows=[]
 for c in leaves:
  p=c['v'][0];rows.append(dict(component=c['rec']['component'],base=list(p),base_inside_stem=inside(stem,p),surface_distance_m=stem['bvh'].find_nearest(p)[3]))
 roots=[c for c in comps if c['rec']['vertices']==20]
 features=dict(leaf_components=len(leaves),root_components=len(roots),stem_top_z_m=stem['rec']['bounds_blender_m']['max'][2],leaf_bases_inside_stem=sum(r['base_inside_stem'] for r in rows),all_leaf_bases_inside_stem=all(r['base_inside_stem'] for r in rows),leaf_attachments=rows)
 if aid=='nathorstiana':
  ring=stem['v'][48:96];rad=[math.hypot(v.x,v.y) for v in ring];features.update(actual_basal_radial_peaks=sum(rad[i]>rad[i-1] and rad[i]>rad[(i+1)%48] for i in range(48)),basal_ring_radius_range_m=[min(rad),max(rad)])
 else:
  sp=[c for c in comps if c['rec']['vertices']==6 and c['rec']['material_indices'] in [[1],[4]]];ordered=sorted(sp,key=lambda c:sum(v.z for v in c['v'])/len(c['v']));bands=[]
  for c in ordered:
   material=c['rec']['material_indices'][0]
   if not bands or bands[-1]['material']!=material:bands.append(dict(material=material,count=0))
   bands[-1]['count']+=1
  features.update(fertile_sporangial_components=len(sp),alternate_sporangial_bands=bands,vegetative_leaves_derived=len(leaves)-len(sp))
if aid=='diplopora':
 assert len(comps)==1;c=comps[0];v=c['v'];f=c['f'];r=[math.hypot(p.x,p.y) for p in v]
 # Outer wall is separated by radius from inner wall and traversing canal/rim faces.
 outer=[face for face in f if all(r[i]>.012 for i in face)];ec=collections.Counter()
 for face in outer:
  for i,j in zip(face,face[1:]+face[:1]):ec[tuple(sorted((i,j)))]+=1
 edges=[e for e,n in ec.items() if n==1];adj=collections.defaultdict(set)
 for x,y in edges:adj[x].add(y);adj[y].add(x)
 unseen=set(adj);loops=[]
 while unseen:
  a=min(unseen);seen={a};stack=[a];unseen.remove(a)
  while stack:
   for j in adj[stack.pop()]:
    if j in unseen:unseen.remove(j);seen.add(j);stack.append(j)
  loops.append(sorted(seen))
 holes=[lp for lp in loops if len(lp)==8];rims=[lp for lp in loops if len(lp)!=8];samples=[]
 for lp in holes:
  center=sum((v[i] for i in lp),Vector())/len(lp);a=math.atan2(center.y,center.x);start=Vector((.022*math.cos(a),.022*math.sin(a),center.z));dr=Vector((-math.cos(a),-math.sin(a),0));hit=c['bvh'].ray_cast(start,dr,.020)[0]
  # Adjacent angular cell-edge control at same elevation must encounter solid wall.
  ac=a+math.pi/16;control=Vector((.022*math.cos(ac),.022*math.sin(ac),center.z));ctrl=c['bvh'].ray_cast(control,Vector((-math.cos(ac),-math.sin(ac),0)),.020)[0]
  samples.append(dict(angle_rad=a,z_m=center.z,outer_boundary_vertices=len(lp),clear_through_near_wall=hit is None,solid_between_pores=ctrl is not None))
 zs=sorted(s['z_m'] for s in samples);groups=[]
 for z in zs:
  if not groups or z-groups[-1][-1]>.003:groups.append([])
  groups[-1].append(z)
 axisclear=c['bvh'].ray_cast(Vector((0,0,-.01)),Vector((0,0,1)),1)[0] is None
 features=dict(outer_surface_boundary_loops=len(loops),pore_loops=len(holes),rim_loops=[len(lp) for lp in rims],boundary_loop_degree_two=all(len(x)==2 for x in adj.values()),pore_whorl_counts=[len(x) for x in groups],pore_whorl_z_ranges_m=[[min(x),max(x)] for x in groups],all96_real_through_channels=len(samples)==96 and all(s['clear_through_near_wall'] for s in samples),all_wall_controls_solid=all(s['solid_between_pores'] for s in samples),axial_lumen_ray_clear=axisclear,samples=samples)
# Actual fresh source reexport, local QA copy only. Never save source.
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(col['asset_root']);fresh=dest/'fresh-reexport-attempt2.glb'
assert not fresh.exists()
bpy.ops.export_scene.gltf(filepath=str(fresh),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
fa=audit_glb(fresh,max_triangles=14000,max_materials=6,max_primitives=30)
report=dict(schema_version=1,asset_id=aid,revision=rev,started_at=run_started,finished_at=now(),pid=os.getpid(),parent_pid=os.getppid(),blender_version=bpy.app.version_string,source_sha256=s0,glb_sha256=g0,script_sha256=sha(Path(__file__)),source_saved=False,source_unchanged=sha(src)==s0,glb_unchanged=sha(glb)==g0,source_counts=dict(totals),objects=objrecords,components=[c['rec'] for c in comps],features=features,source_audit=sourceaudit,project_glb_audit=exportaudit,source_export_comparison=comparison,fresh_reexport=dict(path=str(fresh),sha256=sha(fresh),byte_identical=sha(fresh)==g0,audit=fa),gpu='unknown/unrun',scene='unknown/unrun')
with (dest/'source-geometry-reexport-attempt2.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print('INDEPENDENT',aid,'source',comparison['status'],'fresh_identical',report['fresh_reexport']['byte_identical'],'features', {k:x for k,x in features.items() if k not in ['junctions','samples','leaf_attachments']})
