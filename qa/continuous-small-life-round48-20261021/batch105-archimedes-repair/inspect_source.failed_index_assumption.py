import bpy,sys,pathlib,json,hashlib,math,collections,os,datetime
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode=True
R=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-repair-20261021');Q=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-independent-qa-20261021');D=R/'production/small-life-batch105-archimedes-repair/r002';O=R/'production/small-life-batch105/archimedes/r001';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pins=[sha(O/'artifacts/archimedes.blend'),sha(D/'artifacts/archimedes.blend')]
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ct=json.loads(bpy.data.texts['BATCH105_COMPONENT_CONTRACT.json'].as_string());ob=bpy.data.objects[ct['object_name']];ob.data.calc_loop_triangles()
 mats=[]
 for m in ob.data.materials:
  mats.append({'name':m.name,'diffuse_color':list(m.diffuse_color),'use_nodes':m.use_nodes,'surface_render_method':m.surface_render_method,'nodes':[(n.name,n.bl_idname,[(i.name,list(i.default_value) if hasattr(i.default_value,'__len__') and not isinstance(i.default_value,str) else i.default_value) for i in n.inputs if hasattr(i,'default_value')]) for n in m.node_tree.nodes],'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links]})
 return {'vertices':[tuple(v.co) for v in ob.data.vertices],'world_vertices':[tuple(ob.matrix_world@v.co) for v in ob.data.vertices],'faces':[tuple(p.vertices) for p in ob.data.polygons],'triangles':[tuple(t.vertices) for t in ob.data.loop_triangles],'material_indices':[p.material_index for p in ob.data.polygons],'matrix':list(map(list,ob.matrix_world)),'materials':mats,'contract':ct,'objects':[(o.name,o.type, bool(o.hide_render)) for o in bpy.data.objects],'modifiers':[(m.name,m.type) for m in ob.modifiers]}
a=snapshot(O/'artifacts/archimedes.blend');b=snapshot(D/'artifacts/archimedes.blend');diff=[i for i,(v,w) in enumerate(zip(a['vertices'],b['vertices'])) if v!=w];assert len(diff)==65
for k in ['faces','triangles','material_indices','matrix','materials','contract','objects','modifiers']:assert a[k]==b[k],k
axis=next(c for c in b['contract']['components'] if c['kind']=='axial_helix');frond=next(c for c in b['contract']['components'] if c['kind']=='perforated_frond');assert not set(diff)&set(frond['vertices']);assert len(b['contract']['integrated_features'])==300
assert all(a['vertices'][i]==b['vertices'][i] for i in range(32,936));assert set(diff)==set(range(32))|set(range(936,969))
vs=[Vector(v) for v in b['world_vertices']];top=[]
def topology(c):
 ids=set(c['vertices']);ts=[t for t in b['triangles'] if set(t)<=ids];ed=collections.defaultdict(list);adj={i:set() for i in ids}
 for t in ts:
  for x,y in zip(t,t[1:]+t[:1]):ed[tuple(sorted((x,y)))].append((x,y));adj[x].add(y);adj[y].add(x)
 todo=set(ids);components=0
 while todo:
  components+=1;st=[todo.pop()]
  while st:
   i=st.pop();ns=adj[i]&todo;todo-=ns;st+=list(ns)
 volume=sum(vs[t[0]].dot(vs[t[1]].cross(vs[t[2]]))/6 for t in ts);chi=len(ids)-len(ed)+len(ts);bad=[e for e,u in ed.items() if len(u)!=2 or u[0]!=u[1][::-1]]
 assert not bad and volume>0 and components==1
 return {'tag':c['tag'],'vertices':len(ids),'triangles':len(ts),'edges':len(ed),'boundary_nonmanifold_or_direction_errors':len(bad),'signed_volume_m3':volume,'connected_components':components,'euler_characteristic':chi,'closed_orientable_genus':(2-chi)//2},ts
at,ats=topology(axis);ft,fts=topology(frond);assert at['euler_characteristic']==2 and ft['closed_orientable_genus']==300
rings=[]
for i in [0,1,2,3,4,116,117,118,119,120]:
 ix=list(range(8*i,8*i+8));rs={}
 for name,s in [('original',a),('repaired',b)]:
  points=[Vector(s['vertices'][j]) for j in ix];ctr=sum(points,Vector())/8;rr=[(v-ctr).length for v in points];rs[name]={'center_m':list(ctr),'min_radius_m':min(rr),'max_radius_m':max(rr)}
 rings.append({'ring':i,**rs})
assert all(rings[j]['repaired']['max_radius_m']<rings[j+1]['repaired']['min_radius_m'] for j in range(4));assert all(rings[j]['repaired']['min_radius_m']>rings[j+1]['repaired']['max_radius_m'] for j in range(5,9))
# Complete closed axis BVH, actual source frond triangles. Boundary points never count as inside.
axis_tree=BVHTree.FromPolygons(vs,ats,all_triangles=True);frond_tree=BVHTree.FromPolygons(vs,fts,all_triangles=True);pairs=frond_tree.overlap(axis_tree)
def wn(p):
 total=0.
 for t in ats:
  x,y,z=(vs[i]-p for i in t);den=x.length*y.length*z.length+x.dot(y)*z.length+y.dot(z)*x.length+z.dot(x)*y.length;total+=2*math.atan2(x.dot(y.cross(z)),den)
 return total/(4*math.pi)
contacts=[];off=b['contract']['translation'][2];H=.035
for name,lo,hi in [('lower',min(v.z for v in vs),off+H*4/120),('upper',off+H*116/120,off+H)]:
 strict=[];negative=0
 for j,t in enumerate(fts):
  p=sum((vs[i] for i in t),Vector())/3
  if not lo<=p.z<=hi:continue
  closest,normal,k,dist=axis_tree.find_nearest(p);sgn=(p-closest).dot(normal)
  if sgn>=0 or dist==0:continue
  negative+=1;w=wn(p)
  if abs(w-1)<1e-5:strict.append({'triangle':j,'source_indices':t,'centroid_m':list(p),'distance_m':dist,'signed_distance_m':sgn,'winding':w})
 local=[p for p in pairs if lo<=sum(vs[i].z for i in fts[p[0]])/3<=hi];assert strict and local
 contacts.append({'endpoint':name,'z_window_m':[lo,hi],'strict_interior_surface_centroids':len(strict),'negative_candidates':negative,'local_surface_intersections':len(local),'examples':sorted(strict,key=lambda x:x['signed_distance_m'])[:6]})
# Check entire authored collection and export every object, not a chosen mesh subset.
cols=[c for c in bpy.data.collections if c.get('asset_root')];assert len(cols)==1;col=cols[0];allobjects=list(col.all_objects);assert set(o.name for o in bpy.context.scene.objects if o.type=='MESH')==set(o.name for o in allobjects if o.type=='MESH');assert len([o for o in allobjects if o.type=='MESH'])==1
bpy.ops.object.select_all(action='DESELECT')
for ob in allobjects:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(col['asset_root']);export=Q/'full-collection-reexport.glb';assert not export.exists()
bpy.ops.export_scene.gltf(filepath=str(export),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
assert export.read_bytes()==(D/'artifacts/archimedes.glb').read_bytes();assert pins==[sha(O/'artifacts/archimedes.blend'),sha(D/'artifacts/archimedes.blend')]
report={'status':'pass','source_original_sha256':pins[0],'source_repaired_sha256':pins[1],'blender_version':bpy.app.version_string,'pid':os.getpid(),'changed_vertices':diff,'changed_vertex_count':len(diff),'unchanged_vertices':len(a['vertices'])-len(diff),'all_faces_original_indices_materials_nodes_transforms_contracts_equal':True,'middle_113_rings_unchanged':True,'all_3132_frond_vertices_and_7460_triangles_unchanged':True,'all_300_feature_records_unchanged':True,'original_topology':[at,ft],'taper_ring_profiles':rings,'endpoint_contacts':contacts,'actual_scene_objects':b['objects'],'full_collection_objects':[(o.name,o.type) for o in allobjects],'full_collection_reexport_sha256':sha(export),'full_collection_reexport_byte_identical':True,'source_modified':False,'original_geometry_repaired_or_welded':False,'numeric_note':'Radius values describe actual geometric taper, not an added acceptance threshold. Interior test uses real frond surface centroids with nonzero distance, negative outward-normal signed distance, winding near+1, and actual local surface intersections. No new penetration-depth requirement.'}
(Q/'source-independent.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: independent source difference, original topology, strict contacts, full collection export')
