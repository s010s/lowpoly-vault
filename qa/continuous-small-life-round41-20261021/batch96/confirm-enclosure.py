import bpy,bmesh,json,sys,pathlib,datetime,hashlib,os,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=pathlib.Path(sys.argv[sys.argv.index('--')+1]);D=pathlib.Path(sys.argv[sys.argv.index('--')+2]);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=H(B/'source.blend')
bpy.ops.wm.open_mainfile(filepath=str(B/'source.blend'),load_ui=False,use_scripts=False);bpy.context.view_layer.update();brief=json.load(open(B/'brief.json'));sem=json.load(open(B/'geometry-semantics.json'));groups={};faces={};objs=[]
def bounds(v):
 lo=[min(p[i]for p in v)for i in range(3)];hi=[max(p[i]for p in v)for i in range(3)];return {'min':lo,'max':hi,'size':[hi[i]-lo[i]for i in range(3)]}
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 o.data.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(o.data);bm.normal_update();edit=o.data.vertices[0].co.copy();o.data.vertices[0].co.x+=.001;changed=o.data.vertices[0].co!=edit;o.data.vertices[0].co=edit
 objs.append({'name':o.name,'editable_vertex_roundtrip_in_memory':changed,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'polygons':len(o.data.polygons),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-16 for f in bm.faces),'negative_scale':any(x<0 for x in o.matrix_world.to_scale()),'bounds_m':bounds([o.matrix_world@v.co for v in o.data.vertices])});bm.free()
 for g in o.vertex_groups:
  ix=[v.index for v in o.data.vertices if any(k.group==g.index and k.weight>0 for k in v.groups)];lut={n:i for i,n in enumerate(ix)};assert g.name not in groups
  groups[g.name]=[o.matrix_world@o.data.vertices[i].co for i in ix];faces[g.name]=[tuple(lut[i]for i in t.vertices)for t in o.data.loop_triangles if all(i in lut for i in t.vertices)]
trees={g:BVHTree.FromPolygons(v,faces[g],all_triangles=True)for g,v in groups.items()};dirs=[Vector(x).normalized()for x in [(1,.171,.293),(.233,1,.379),(.257,.319,1)]]
def contains(g,p):
 t=trees[g];near=t.find_nearest(p);dist=near[3]
 if dist is not None and dist<1e-7:return True,dist,[True]*3
 votes=[]
 for d in dirs:
  origin=p.copy();distances=[];traveled=0
  for _ in range(100):
   hit,n,idx,ds=t.ray_cast(origin,d)
   if hit is None:break
   traveled+=ds
   if not distances or abs(traveled-distances[-1])>2e-7:distances.append(traveled)
   origin=hit+d*1e-7;traveled+=1e-7
  votes.append(len(distances)%2==1)
 return sum(votes)>=2,dist,votes
frames={x['group']:x for x in sem['leaf_frames']};tubes={x['group']:x for x in sem['tubes']};contact=[]
for a in sem['attachments']:
 g=a['child'];ids=(frames.get(g)or tubes[g])['base_indices'];ps=[groups[g][i]for i in ids];c=sum(ps,Vector())/len(ps);tests=[contains(a['parent'],x)for x in[c]+ps];ok=any(x[0]for x in tests)
 contact.append({'child':g,'parent':a['parent'],'connected':ok,'center_world_m':list(c),'center_inside_ray_majority':tests[0][0],'inside_base_vertices':sum(x[0]for x in tests[1:]),'center_surface_distance_m':tests[0][1],'center_ray_votes':tests[0][2]})
counts={p:sum(g.startswith(p)if p.endswith('-')else g==p for g in groups)for p in brief['hard_component_counts']}
def centers(g):
 n=tubes[g]['sides'];return[sum(groups[g][i:i+n],Vector())/n for i in range(0,len(groups[g]),n)]
hier={};aid=B.parent.name
for parent,child,n in ({'paralycopodites':[('lateral-','twig-',4),('twig-','cone-',1),('twig-','leaf-',7)],'lyginopteris':[('frond-','fan-',2),('fan-','pinna-',3),('pinna-','leaf-',6)],'medullosa':[('frond-','fan-',2),('fan-','pinna-',4),('pinna-','leaf-',8)],'cordaites':[('limb-','twig-',3),('twig-','leaf-',5)]}[aid]):
 d={g:sum(a['parent']==g and a['child'].startswith(child)for a in sem['attachments'])for g in groups if g.startswith(parent)};hier[parent+child]={'expected':n,'counts':d,'pass':all(x==n for x in d.values())}
leaves={g:{'longitudinal_m':max(v.dot(Vector(f['longitudinal']))for v in groups[g])-min(v.dot(Vector(f['longitudinal']))for v in groups[g]),'transverse_m':max(v.dot(Vector(f['transverse']))for v in groups[g])-min(v.dot(Vector(f['transverse']))for v in groups[g])}for g,f in frames.items()}
extra={}
if aid=='paralycopodites':
 rows=[{'group':a['child'],'direction':list((centers(a['child'])[1]-centers(a['child'])[0]).normalized())}for a in sem['attachments']if a['parent']=='main-axis'and a['child'].startswith('lateral-')];extra['main_lateral_rows']=rows;extra['cone_lengths_m']={g:sum((b-a).length for a,b in zip(centers(g),centers(g)[1:]))for g in tubes if g.startswith('cone-')}
if aid=='lyginopteris':extra['support_station_distance_m']=min((a-b).length for a in centers('main-axis')for b in centers('support-axis'))
if aid=='cordaites':extra['leaf_band_vertex_counts']={g:len(v)for g,v in groups.items()if g.startswith('leaf-')}

checks=[]
for a in sem['attachments']:
 if not (a['child'].startswith('leaf-') or a['child'].startswith('gland-') or a['child'].startswith('cone-')):continue
 tests=[contains(a['parent'],v) for v in groups[a['child']]]
 checks.append({'child':a['child'],'parent':a['parent'],'vertices':len(tests),'vertices_inside_parent':sum(t[0]for t in tests),'all_vertices_inside_parent':all(t[0]for t in tests),'surface_intersection_triangle_pairs':len(trees[a['child']].overlap(trees[a['parent']])),'max_surface_distance_m':max(t[1] for t in tests)})
d={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'source_sha256':before,'glb_sha256':H(B/'model.glb'),'method':'Independent three-ray-majority point-in-volume tests at every actual world vertex of leaves, cones and gland bases against their parent surfaces. All-inside is strong burial evidence for these locally convex parent tubes; no geometry changed.','checks':checks,'fully_inside':[c for c in checks if c['all_vertices_inside_parent'] and c['surface_intersection_triangle_pairs']==0]}
with (D/'enclosure-confirmation.json').open('x') as f:json.dump(d,f,indent=2)
print(aid,'fully inside',[(c['child'],c['parent']) for c in d['fully_inside']])
