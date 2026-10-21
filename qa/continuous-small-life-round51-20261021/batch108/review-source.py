import bpy,json,sys,pathlib,hashlib,datetime,os,collections,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=pathlib.Path('/workspace/shared/lowpoly-batch108-20261021');O=pathlib.Path(__file__).parent
sys.path.insert(0,str(R/'scripts'));from qa_glb import audit_glb
asset=sys.argv[-1];rev='r003' if asset=='placocystites' else 'r002';d=R/'production/batch-108'/asset/rev;src=d/'artifacts'/f'{asset}.blend';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=sha(src)
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ct=json.loads(bpy.data.texts['BATCH108_COMPONENT_CONTRACT.json'].as_string());obj=bpy.data.objects[ct['object_name']];obj.data.calc_loop_triangles();V=[obj.matrix_world@v.co for v in obj.data.vertices];T=[tuple(t.vertices) for t in obj.data.loop_triangles];extent=max(max(v[i] for v in V)-min(v[i] for v in V) for i in range(3));eps=extent*2**-21
meshobjs=[o for o in bpy.data.objects if o.type=='MESH'];objects=[dict(name=o.name,type=o.type,collections=[c.name for c in o.users_collection],hide_render=o.hide_render,selected=o.select_get(),matrix=[list(x) for x in o.matrix_world],vertices=len(o.data.vertices) if o.type=='MESH' else None) for o in bpy.data.objects];C=ct['components'];lookup={c['tag']:c for c in C};faces={c['tag']:[t for t in T if all(i in set(c['vertices']) for i in t)] for c in C};trees={k:BVHTree.FromPolygons(V,fs,all_triangles=True) for k,fs in faces.items()};dirs=[Vector(x).normalized() for x in [(1,.371,.217),(.163,1,.493),(.719,.283,1)]]
def inside(tree,p):
 q,n,f,dist=tree.find_nearest(p)
 if dist is None or dist<=eps:return False,dist,[]
 parity=[]
 for direction in dirs:
  cursor=p.copy();hits=0
  for _ in range(256):
   q=tree.ray_cast(cursor,direction,extent*4)[0]
   if q is None:break
   hits+=1;cursor=q+direction*eps*8
  parity.append(hits%2)
 return all(parity),dist,parity
checks=[];errors=[];component_data=[]
for c in C:
 ids=set(c['vertices']);fs=faces[c['tag']];ed=collections.defaultdict(list);adj=collections.defaultdict(set)
 for j,t in enumerate(fs):
  for x,y in zip(t,t[1:]+t[:1]):ed[tuple(sorted((x,y)))].append((j,1 if x<y else -1))
 for refs in ed.values():
  for j,_ in refs:adj[j].update(k for k,_ in refs)
 groups=[];seen=set()
 for j in range(len(fs)):
  if j in seen:continue
  stack=[j];seen.add(j);ii=[]
  while stack:
   k=stack.pop();ii.append(k)
   for n in adj[k]:
    if n not in seen:seen.add(n);stack.append(n)
  groups.append(ii)
 partdata=[]
 for gi,g in enumerate(groups):
  tris=[fs[j] for j in g];verts=set(i for t in tris for i in t);subset=set(g);edge_refs=[refs for refs in ed.values() if refs[0][0] in subset];bad=sum(len(rr)!=2 or rr[0][1]==rr[1][1] for rr in edge_refs);volume=sum(V[t[0]].dot(V[t[1]].cross(V[t[2]]))/6 for t in tris);own=BVHTree.FromPolygons(V,tris,all_triangles=True);witness=None
  if c.get('parent'):
   parent=trees[c['parent']];candidates=[sum((V[i] for i in verts),Vector())/len(verts)]
   for t in tris:
    x,y,z=[V[i] for i in t];n=(y-x).cross(z-x)
    if not n.length:continue
    n.normalize();step=min((x-y).length,(y-z).length,(x-z).length)
    for frac in [.01,.05,.2,.45]:candidates.append((x+y+z)/3-n*step*frac)
   for q in candidates:
    near,n,_,dist=parent.find_nearest(q)
    if dist is None or dist<=eps or (q-near).dot(n)>=0:continue
    ip,dp,pp=inside(parent,q)
    if not ip:continue
    ic,dc,pc=inside(own,q)
    if ic:witness=dict(point=list(q),child_surface_distance=dc,parent_surface_distance=dp,child_parity=pc,parent_parity=pp);break
  rest=BVHTree.FromPolygons(V,[t for t in T if not all(i in verts for i in t)],all_triangles=True);visible=0
  # Per real disconnected solid, not one pass for the whole named aggregate.
  for t in tris:
   q=sum((V[i] for i in t),Vector())/3
   for direction in [Vector(v).normalized() for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(1,-1,1),(-1,1,1)]]:
    if rest.ray_cast(q+direction*eps,direction,extent*4)[0] is None:visible+=1;break
  rec=dict(part=gi,triangles=len(tris),vertices=len(verts),bad_edges=bad,signed_volume=volume,contact_witness=witness,exposed_triangle_centers=visible)
  if bad or volume<=0:errors.append(f'topology:{c["tag"]}:{gi}')
  if c.get('parent') and witness is None:errors.append(f'no_strict_contact_sample:{c["tag"]}:{gi}')
  if not visible:errors.append(f'no_exposure_sample:{c["tag"]}:{gi}')
  partdata.append(rec)
 pts=[V[i] for i in ids];bounds={'min':[min(v[k] for v in pts) for k in range(3)],'max':[max(v[k] for v in pts) for k in range(3)]};component_data.append(dict(tag=c['tag'],kind=c['kind'],bounds=bounds,parts=partdata))
# Read local cavity geometry in original source, compare genuine depths with the curved solid and all rest-of-scene solids.
cavities=[]
for c in C:
 if c['kind'] not in ['spiracle','anispiracle','anal_opening']:continue
 ids=c['vertices'];rings=[ids[i:i+12] for i in range(0,48,12)];centers=[sum((V[i] for i in ring),Vector())/len(ring) for ring in rings];base,rim,inner,floor=centers;normal=(rim-base).normalized();host=trees['theca'];q,n,_,distance=host.find_nearest(rim);qf,nf,_,df=host.find_nearest(floor);rest=BVHTree.FromPolygons(V,[t for t in T if not all(i in ids for i in t)],all_triangles=True);samples=[floor]+[(floor+V[i])/2 for i in rings[3]];vis=[rest.ray_cast(p+normal*eps,normal,extent*4)[0] is None for p in samples];cavities.append(dict(tag=c['tag'],rim_to_floor_depth=(rim-floor).dot(normal),rim_above_nearest_core=(rim-q).dot(n),floor_above_nearest_core=(floor-qf).dot(nf),outer_diameter=max((V[i]-rim).length for i in rings[1])*2,floor_clear_samples=sum(vis),floor_samples=len(vis),normal=list(normal),rim_world=list(rim)))
# Export ALL authored objects, not selection state. Scene has one mesh; record anything outside root as a blocker.
roots=[c for c in bpy.data.collections if c.get('asset_root')];included=set(o.name for c in roots for o in c.all_objects);outside=[o.name for o in meshobjs if o.name not in included]
if outside:errors.append('authored_meshes_outside_asset_root')
export=O/asset/'full-source-reexport.glb';bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=False,export_apply=True,export_yup=True,export_texcoords=False,export_normals=True,export_materials='EXPORT',export_animations=False,export_cameras=False,export_lights=False)
audit=audit_glb(export,max_triangles=14000,max_materials=6,max_primitives=30);orig=audit_glb(d/'artifacts'/f'{asset}.glb',max_triangles=14000,max_materials=6,max_primitives=30);match=audit['semantic_sha256']==orig['semantic_sha256'];
if not match:errors.append('full_source_reexport_semantics_differ')
report=dict(asset_id=asset,revision=rev,source_sha256=h,glb_sha256=sha(d/'artifacts'/f'{asset}.glb'),created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),pid=os.getpid(),objects=objects,all_authored_meshes=[o.name for o in meshobjs],outside_root=outside,contract_vertices_cover_all=sorted(set(i for c in C for i in c['vertices']))==list(range(len(V))),components=component_data,cavities=cavities,errors=errors,reexport=dict(path=str(export),sha256=sha(export),semantic_match=match,semantic_sha256=audit['semantic_sha256'],source_semantic_sha256=orig['semantic_sha256'],triangles=audit['scene_triangles']),source_unchanged=sha(src)==h,epsilon=eps,method='Fresh reviewer script. Split every named aggregate into actual connected source solids, preserve original world triangles/winding; require positive signed volume/opposed two-use edges, strict interior contact witnesses and sampled exposure to rest of scene. Finite sampling misses require diagnosis, not invented anatomical thresholds. Full source re-export with use_selection=False includes every mesh regardless of saved selection.')
(O/asset/'fresh-source-inspection.json').write_text(json.dumps(report,indent=2)+'\n');print(asset,'done',len(component_data),'groups',sum(len(x['parts']) for x in component_data),'actual solids; errors',errors)
