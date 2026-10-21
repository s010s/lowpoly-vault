import bpy,sys,json,hashlib,datetime,os,math,collections
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
args=sys.argv[sys.argv.index('--')+1:];src=Path(args[0]);out=Path(args[1]);out.mkdir(exist_ok=True)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=h(src);t0=datetime.datetime.now(datetime.timezone.utc).isoformat()
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update()
vs=[];ts=[];tgs=[];groups={};aps=[];relations=[];objects=[]
for ob in bpy.context.scene.objects:
 if ob.type!='MESH':continue
 me=ob.data;me.calc_loop_triangles();n=len(vs);vs.extend(ob.matrix_world@v.co for v in me.vertices);gn={g.index:g.name for g in ob.vertex_groups}
 for g in ob.vertex_groups:groups[g.name]=[]
 for v in me.vertices:
  for g in v.groups:groups[gn[g.group]].append(v.index+n)
 for t in me.loop_triangles:
  common=set(x.group for x in me.vertices[t.vertices[0]].groups)
  for k in t.vertices[1:]:common &= set(x.group for x in me.vertices[k].groups)
  assert len(common)==1
  ts.append(tuple(k+n for k in t.vertices));tgs.append(gn[common.pop()])
 aps.extend(json.loads(ob.get('aperture_design','[]')));relations.extend(json.loads(ob.get('contact_design','[]')))
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();em.calc_loop_triangles();objects.append({'name':ob.name,'vertices':len(me.vertices),'authored_triangles':len(me.loop_triangles),'evaluated_triangles':len(em.loop_triangles),'modifiers':len(ob.modifiers),'matrix_world':[list(r) for r in ob.matrix_world]});ev.to_mesh_clear()
D=[Vector(x).normalized() for x in [(0.613,0.317,0.724),(-0.441,0.817,0.373),(0.192,-0.553,0.811)]]
# Three independent non-axis-aligned parity rays, strict interior (surface samples excluded).
def inside(p,tree):
 q,_,_,distance=tree.find_nearest(p)
 if q is None or distance<1e-10:return False
 votes=[]
 for d in D:
  p0=p.copy();count=0
  for _ in range(256):
   loc,_,_,dist=tree.ray_cast(p0,d,2)
   if loc is None:break
   count+=1;p0=loc+d*1e-9
  votes.append(count%2==1)
 return sum(votes)>=2
faces={g:[] for g in groups};tree={};islands={};metrics={};samples={}
for f,g in zip(ts,tgs):faces[g].append(f)
for g,ids in groups.items():
 ff=faces[g];tree[g]=BVHTree.FromPolygons(vs,ff,all_triangles=True);adj=collections.defaultdict(set);ed=collections.defaultdict(list)
 for f in ff:
  for a,b in zip(f,f[1:]+f[:1]):adj[a].add(b);adj[b].add(a);ed[tuple(sorted((a,b)))].append((a,b))
 left=set(ids);pieces=[]
 while left:
  seed=next(iter(left));left.remove(seed);piece={seed};todo=[seed]
  while todo:
   for j in adj[todo.pop()]:
    if j in left:left.remove(j);piece.add(j);todo.append(j)
  pieces.append(piece)
 islands[g]=pieces;samples[g]=[(i,vs[i]) for i in ids]+[(f[0],sum((vs[i] for i in f),Vector())/3) for f in ff]
 volumes=[]
 for ii in pieces:volumes.append(sum(vs[a].dot(vs[b].cross(vs[c]))/6 for a,b,c in ff if a in ii))
 metrics[g]={'vertices':len(ids),'triangles':len(ff),'islands':len(pieces),'bounds':{'min':[min(vs[i][k] for i in ids) for k in range(3)],'max':[max(vs[i][k] for i in ids) for k in range(3)]},'signed_volumes':volumes,'nonmanifold_edges':sum(len(e)!=2 for e in ed.values()),'same_direction_edges':sum(len(e)==2 and e[0]==e[1] for e in ed.values()),'zero_area_triangles':sum((vs[b]-vs[a]).cross(vs[c]-vs[a]).length==0 for a,b,c in ff)}
 contacts=[]
for rel in relations:
 ch,pa=rel['child'],rel['parent'];w=[]
 for piece in islands[ch]:
  hit=next(({'direction':'child_surface_inside_parent','point':list(p)} for i,p in samples[ch] if i in piece and inside(p,tree[pa])),None)
  if hit is None:
   subtree=BVHTree.FromPolygons(vs,[f for f in faces[ch] if f[0] in piece],all_triangles=True)
   hit=next(({'direction':'parent_surface_inside_child','point':list(p)} for i,p in samples[pa] if inside(p,subtree)),None)
  w.append(hit)
 contacts.append({**rel,'per_child_island_witnesses':w,'pass':all(x is not None for x in w)})
whole=BVHTree.FromPolygons(vs,ts,all_triangles=True)
angles={'hero':(35,35),'reversehero':(215,35),'front':(0,0),'side':(90,0),'rear':(180,0),'top':(0,90),'lower_oblique':(45,-50),'lower_proximal':(-30,-60)}
dirs={k:Vector((math.sin(math.radians(a))*math.cos(math.radians(e)),-math.cos(math.radians(a))*math.cos(math.radians(e)),math.sin(math.radians(e)))) for k,(a,e) in angles.items()}
exposure=[]
for g,ff in faces.items():
 witnesses=[];counts={k:0 for k in dirs};perisland=[]
 for piece in islands[g]:
  witnesses_here=[]
  for a,b,c in ff:
   if a not in piece:continue
   pt=(vs[a]+vs[b]+vs[c])/3;norm=(vs[b]-vs[a]).cross(vs[c]-vs[a]).normalized()
   for name,d in dirs.items():
    if norm.dot(d)<=0:continue
    loc,_,idx,dist=whole.ray_cast(pt+d*1e-8,d,2)
    if loc is None:
     counts[name]+=1
     if len(witnesses_here)<2:witnesses_here.append({'point':list(pt),'direction':name})
  perisland.append(bool(witnesses_here));witnesses.extend(witnesses_here)
 exposure.append({'component':g,'visible_centroids_by_direction':counts,'each_island_visible':perisland,'witnesses':witnesses,'pass':all(perisland)})
apertures=[]
for ap in aps:
 g=ap['component'];p=Vector(ap['center']);axis=Vector(ap['direction']).normalized();idx=ap['terminal_ring_local_indices'];ring=[vs[groups[g][i]] for i in idx];derived=sum(ring,Vector())/len(ring);center_error=(derived-p).length
 loc,_,ti,depth=whole.ray_cast(p-axis*1e-8,-axis,2);occ=[k for k in tree if inside(p-axis*1e-8,tree[k])];visibility=[]
 for name,d in {'axis':axis,**dirs}.items():
  if d.dot(axis)<=0:continue
  hit,_,fi,dist=whole.ray_cast(p+d*1e-8,d,2)
  visibility.append({'direction':name,'open':hit is None,'first_component':None if hit is None else tgs[fi]})
 # Probe off-axis positions inside actual octagonal/hexagonal radius, excluding any dark-paint interpretation.
 _,u,v=(axis,axis.cross(Vector((.313,.723,.615))).normalized(),None);v=axis.cross(u).normalized();probe=[]
 for d in [u,-u,v,-v]:
  q=p+d*ap['inner_radius_m']*.5-axis*1e-8
  hit,_,fi,dist=whole.ray_cast(q,-axis,2);probe.append({'occupied':any(inside(q,tr) for tr in tree.values()),'recess_depth':dist if hit is not None else None})
 apertures.append({'component':g,'metadata_center_error_m':center_error,'actual_center':list(derived),'axis':list(axis),'rim_radius_min_m':min((x-p).length for x in ring),'whole_scene_axis_floor_depth_m':depth if loc is not None else None,'first_floor_component':None if loc is None else tgs[ti],'occupied_by':occ,'exterior_rays':visibility,'off_axis_cavity_probes':probe,'pass':center_error<1e-8 and not occ and loc is not None and depth>1e-8 and any(v['open'] for v in visibility) and all(not v['occupied'] and v['recess_depth'] is not None and v['recess_depth']>1e-8 for v in probe)})
# Full editable source re-export, with no mesh or material edits and no source save.
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.context.scene.objects:
 if ob.type=='MESH':ob.select_set(True)
reexport=out/(src.stem+'-source-reexport.glb')
bpy.ops.export_scene.gltf(filepath=str(reexport),export_format='GLB',use_selection=True,export_yup=True,export_texcoords=False,export_cameras=False,export_lights=False)
result={'source':str(src),'source_sha256':before,'source_unchanged':h(src)==before,'source_saved':False,'pid':os.getpid(),'started_at':t0,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender':bpy.app.version_string,'objects':objects,'geometry_bounds':{'min':[min(v[k] for v in vs) for k in range(3)],'max':[max(v[k] for v in vs) for k in range(3)]},'components':metrics,'contacts':contacts,'exposure':exposure,'apertures':apertures,'reexport':{'path':str(reexport),'sha256':h(reexport)},'method':'Fresh independent reopened source measurement. Per-component directed topology, transformed bounds, both-direction strict-interior 3-ray majority contact per child island. Every actual triangle centroid tested against the full scene for outward line-of-sight. Mouth center checked from actual terminal-ring vertices and lumen probed at center and four off-axis points. Numerical ray offsets are self-hit handling, not anatomical size gates. No percentage acceptance gate.'}
result['failures']={'topology':[g for g,m in metrics.items() if m['nonmanifold_edges'] or m['same_direction_edges'] or m['zero_area_triangles'] or min(m['signed_volumes'])<=0],'contacts':[x for x in contacts if not x['pass']],'exposure':[x['component'] for x in exposure if not x['pass']],'apertures':[x['component'] for x in apertures if not x['pass']]}
(out/'source-inspection.json').write_text(json.dumps(result,indent=2));print('INDEPENDENT_RESULT',json.dumps(result['failures']))
