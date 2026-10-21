# Independent batch94 audit. Reads fixed maker sources; writes exclusively QA output.
import bpy,bmesh,json,sys,os,pathlib,hashlib,datetime,math,collections
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=pathlib.Path('/workspace/shared/lowpoly-batch94-20261020');O=pathlib.Path('/workspace/shared/lowpoly-batch94-independent-qa-20261020');aid,rev=sys.argv[sys.argv.index('--')+1:];B=S/'production/batch94/assets'/aid/rev;D=O/aid;D.mkdir(exist_ok=True)
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();start=now();bpy.ops.wm.open_mainfile(filepath=str(B/'source.blend'));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();groups={};objects=[];allpts=[]
def bounds(v):
 lo=[min(p[i] for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)];return {'min':lo,'max':hi,'size':[hi[i]-lo[i]for i in range(3)]}
def make_group(v,faces):
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
 return {'v':v,'faces':faces,'tree':tree,'islands':islands}
for ob in bpy.context.scene.objects:
 if ob.type!='MESH':continue
 mesh=ob.data;mesh.calc_loop_triangles();v=[ob.matrix_world@p.co for p in mesh.vertices];allpts+=v;bm=bmesh.new();bm.from_mesh(mesh);bm.normal_update();ev=ob.evaluated_get(deps);em=ev.to_mesh();em.calc_loop_triangles();epts=[ev.matrix_world@x.co for x in em.vertices]
 objects.append({'name':ob.name,'world_matrix':[list(row)for row in ob.matrix_world],'authored_vertices':len(v),'authored_polygons':len(mesh.polygons),'authored_triangles':len(mesh.loop_triangles),'evaluated_vertices':len(em.vertices),'evaluated_triangles':len(em.loop_triangles),'authored_bounds':bounds(v),'evaluated_bounds':bounds(epts),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()==0 for f in bm.faces),'signed_volume':bm.calc_volume(signed=True),'modifiers':[m.type for m in ob.modifiers]});bm.free();ev.to_mesh_clear()
 members=collections.defaultdict(list)
 for vert in mesh.vertices:
  for w in vert.groups:
   if w.weight>0:members[w.group].append(vert.index)
 for group in ob.vertex_groups:
  ix=members[group.index];lookup={old:new for new,old in enumerate(ix)};fs=[tuple(lookup[i]for i in t.vertices)for t in mesh.loop_triangles if all(i in lookup for i in t.vertices)];groups[group.name]=make_group([v[i]for i in ix],fs)
sem=json.load(open(B/'geometry-semantics.json'));brief=json.load(open(B/'brief.json'));tubes=collections.defaultdict(list)
for t in sem['tubes']:tubes[t['group']].append(t)
frames={f['group']:f for f in sem['leaf_frames']}
dirs=[Vector(x).normalized()for x in [(1,.217,.413),(.367,1,.137),(.179,.317,1)]]
def inside(g,p):
 tree=g['tree'];hit,n,idx,dist=tree.find_nearest(p)
 if dist is not None and dist<1e-7:return True,'surface',dist
 votes=[]
 for dr in dirs:
  at=p.copy();n=0
  for _ in range(128):
   hit,normal,idx,d=tree.ray_cast(at,dr)
   if hit is None:break
   n+=1;at=hit+dr*1e-7
  votes.append(n%2==1)
 return sum(votes)>=2,str(votes),dist
contacts=[]
for a in sem['attachments']:
 g=groups[a['child']];parent=groups[a['parent']];pts=g['v']
 if a['child']in frames:
  n=frames[a['child']]['outline_vertices'];ids=[0,n]if n==4 else [0,n-1,n,2*n-1]
 elif a['child']in tubes:ids=list(range(tubes[a['child']][0]['sides']))
 else:ids=list(range(len(pts)//2))
 base=sum((pts[i]for i in ids),Vector())/len(ids);tests=[inside(parent,p)for p in [base]+[pts[i]for i in ids]];cross=len(g['tree'].overlap(parent['tree']));contacts.append({'child':a['child'],'parent':a['parent'],'base_world':list(base),'base_center_inside':tests[0][0],'base_vertices_inside':sum(t[0]for t in tests[1:]),'surface_triangle_intersections':cross,'nearest_base_surface_m':tests[0][2],'connected':any(t[0]for t in tests)or cross>0})
# Measure the full forklet hierarchy: three actual closed mesh islands per forklet and both terminal joins.
internal=[]
for name,g in groups.items():
 if not name.startswith('forklet-'):continue
 islands=g['islands'];recs=[]
 for part in islands:
  lut={old:new for new,old in enumerate(part)};recs.append(make_group([g['v'][i]for i in part],[tuple(lut[i]for i in f)for f in g['faces']if all(i in lut for i in f)]))
 joins=[]
 for j in range(1,len(recs)):
  base=sum(recs[j]['v'][:4],Vector())/4;tests=[inside(recs[0],p)[0]for p in [base]+recs[j]['v'][:4]];cross=len(recs[0]['tree'].overlap(recs[j]['tree']));joins.append({'terminal':j,'base':list(base),'overlap_pairs':cross,'contact':any(tests)or cross>0})
 internal.append({'group':name,'islands':len(islands),'island_vertex_counts':[len(x)for x in islands],'terminal_joins':joins,'pass':len(islands)==3 and all(x['contact']for x in joins)})
counts={p:sum(bool(g['v'])and(name.startswith(p)if p.endswith('-')else name==p)for name,g in groups.items())for p in brief['hard_component_counts']};checks={'hard_component_counts':counts==brief['hard_component_counts'],'topology':all(o['nonmanifold_edges']==0 and o['zero_area_faces']==0 for o in objects),'all_parent_interfaces_connected':all(c['connected']for c in contacts),'full_forklet_internal_hierarchy':all(x['pass']for x in internal)};hierarchy={}
def centers(name):
 t=tubes[name][0];v=groups[name]['v'];n=t['sides'];return [sum(v[i:i+n],Vector())/n for i in range(0,t['stations']*n,n)]
if aid=='rhacophyton':
 for parentprefix,childprefix,want in [('frond-','pinna-',8),('pinna-','forklet-',4)]:
  vals={g:sum(c['parent']==g and c['child'].startswith(childprefix)and c['connected']for c in contacts)for g in groups if g.startswith(parentprefix)};hierarchy[childprefix]=vals;checks[childprefix+'per_parent']=all(v==want for v in vals.values())
 # Geometric pinna base stations: four paired attachments per frond.
 paircounts={}
 for frond in [g for g in groups if g.startswith('frond-')]:
  points=[c['base_world']for c in contacts if c['parent']==frond and c['child'].startswith('pinna-')];clusters=[]
  for p in points:
   match=next((c for c in clusters if(Vector(c['base'])-Vector(p)).length<1e-6),None)
   if match:match['count']+=1
   else:clusters.append({'base':p,'count':1})
  paircounts[frond]=clusters
 hierarchy['actual_pinna_pair_stations']=paircounts;checks['four_pairs_per_frond']=all(len(c)==4 and all(x['count']==2 for x in c)for c in paircounts.values())
if aid=='sigillaria':
 v=groups['main-axis']['v'];ring=v[:48];cent=sum(ring,Vector())/48;r=[math.hypot(p.x-cent.x,p.y-cent.y)for p in ring];peaks=[i for i in range(48)if r[i]>r[i-1] and r[i]>r[(i+1)%48]];scarcenters={g:sum(d['v'],Vector())/len(d['v'])for g,d in groups.items()if g.startswith('scar-')};columns=collections.defaultdict(list)
 for g,c in scarcenters.items():columns[round(math.atan2(c.y-cent.y,c.x-cent.x),4)].append(c.z)
 hierarchy['actual_radial_maxima']=len(peaks);hierarchy['scar_columns_by_measured_azimuth']={str(k):sorted(v)for k,v in columns.items()};checks['twelve_physical_ribs']=len(peaks)==12;checks['twelve_columns_sixteen_scars']=len(columns)==12 and all(len(v)==16 for v in columns.values())
if aid in ['pseudobornia','calamites']:
 c=centers('main-axis');n=tubes['main-axis'][0]['sides'];v=groups['main-axis']['v'];r=[sum((p-center).length for p in v[i*n:(i+1)*n])/n for i,center in enumerate(c)];peaks=[i for i in range(1,len(r)-1)if r[i]>r[i-1]and r[i]>r[i+1]];hierarchy['main_axis_stations']=[{'center':list(x),'radius':rad}for x,rad in zip(c,r)];hierarchy['actual_swollen_node_count']=len(peaks);checks['swollen_nodes']=len(peaks)==(4 if aid=='pseudobornia'else 8)
 pref='second-'if aid=='pseudobornia'else'primary-';tiers=collections.defaultdict(list)
 for name in groups:
  if name.startswith(pref):base=centers(name)[0];tiers[round(base.z,5)].append({'group':name,'base':list(base),'azimuth':math.atan2((centers(name)[-1]-base).y,(centers(name)[-1]-base).x)})
 hierarchy['actual_branch_tiers']={str(k):v for k,v in tiers.items()};checks['branch_tiers']=sorted(len(v)for v in tiers.values())==([1,1,2,2]if aid=='pseudobornia'else[5]*4)
 whorls=[]
 for contact in contacts:
  if not contact['child'].startswith('leaf-'):continue
  base=contact['base_world'];match=next((w for w in whorls if w['parent']==contact['parent']and(Vector(w['base'])-Vector(base)).length<1e-6),None)
  if match:match['leaves']+=1
  else:whorls.append({'base':base,'parent':contact['parent'],'leaves':1})
 hierarchy['actual_leaf_whorls']=whorls;checks['leaf_whorls']=len(whorls)==(24 if aid=='pseudobornia'else 80)and all(w['leaves']==(4 if aid=='pseudobornia'else 7)for w in whorls)
# Export source independently without writing source .blend or touching maker reports.
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.data.collections['EXPORT'].all_objects:ob.select_set(True)
opt=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(filepath=str(D/'independent-reexport.glb'),**opt)
d={'asset':aid,'revision':rev,'started_at':start,'finished_at':now(),'pid':os.getpid(),'argv':sys.argv,'blender':bpy.app.version_string,'source_sha256':H(B/'source.blend'),'glb_sha256':H(B/'model.glb'),'reexport_sha256':H(D/'independent-reexport.glb'),'reexport_byte_identical':H(B/'model.glb')==H(D/'independent-reexport.glb'),'objects':objects,'world_bounds':bounds(allpts),'counts':counts,'component_bounds':{n:{'vertices':len(g['v']),'triangles':len(g['faces']),'closed_islands':len(g['islands']),'bounds':bounds(g['v'])}for n,g in groups.items()},'contacts':contacts,'forklet_internal_hierarchy':internal,'hierarchy':hierarchy,'checks':checks,'pass':all(checks.values()),'method_limits':'Geometry measured from actual world vertices and triangulated source. Ray majority and exact triangle overlap establish closed-volume joint contact; 1e-7 m numerical surface epsilon and 1e-6 m coincident-base clustering are not new size/art tolerances. Labels only identify claimed parts; nonempty meshes, topology and actual placement independently checked. GPU and composed scene not tested.'};(D/'independent-geometry.json').write_text(json.dumps(d,indent=2)+'\n');print(aid,checks,'reexport-identical',d['reexport_byte_identical'])
