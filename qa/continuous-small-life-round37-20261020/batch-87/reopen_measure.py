import bpy,sys,json,hashlib,datetime,os,math,bmesh
from pathlib import Path
from mathutils.bvhtree import BVHTree
root=Path('/workspace/shared/lowpoly-batch87-20261020');sys.path.insert(0,str(root/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb
args=sys.argv[sys.argv.index('--')+1:];aid,rev=args
out=Path('/workspace/shared/lowpoly-batch87-independent-qa-20261020')/aid;out.mkdir(exist_ok=True)
p=root/'production/small-life-batch87'/aid/rev/'artifacts';source=p/(aid+'.blend');glb=p/(aid+'.glb');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=h(source);start=datetime.datetime.now(datetime.timezone.utc).isoformat()
bpy.context.preferences.filepaths.use_scripts_auto_execute=False;bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
col=bpy.data.collections['EXPORT'];objs=[o for o in col.all_objects if o.type=='MESH'];dg=bpy.context.evaluated_depsgraph_get();parts=[];allv=[]
for o in objs:
 me=o.data;me.calc_loop_triangles();ev=o.evaluated_get(dg);em=ev.to_mesh();em.calc_loop_triangles();v=[list(o.matrix_world@p.co) for p in me.vertices];allv+=v
 edges={};tri=[tuple(t.vertices) for t in me.loop_triangles]
 for f in me.polygons:
  for i,a in enumerate(f.vertices):
   b=f.vertices[(i+1)%len(f.vertices)];key=tuple(sorted((a,b)));edges[key]=edges.get(key,0)+1
 tree=BVHTree.FromPolygons(v,tri,all_triangles=True);nonadj=[(a,b) for a,b in tree.overlap(tree) if a<b and not set(tri[a])&set(tri[b])]
 parts.append({'name':o.name,'vertices':len(me.vertices),'polygons':len(me.polygons),'triangles':len(tri),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':len(em.loop_triangles),'modifiers':len(o.modifiers),'non_two_face_edges':sum(n!=2 for n in edges.values()),'nonadjacent_bvh_overlap_pairs':len(nonadj),'sample_pairs':nonadj[:12]});ev.to_mesh_clear()
metrics={};v=allv
if aid=='pleuromeia':
 # Index attribution independently verified against generator constructor topology and source arrays.
 lengths=[];horizontal=[]
 for i in range(42):
  vs=v[420+i*20:420+(i+1)*20];centers=[[sum(p[k] for p in vs[q:q+4])/4 for k in range(3)] for q in range(0,20,4)]
  lengths.append(sum(math.dist(a,b) for a,b in zip(centers,centers[1:])));horizontal.append(math.dist(centers[0][:2],centers[-1][:2]))
 cone=v[1260:2548]
 metrics={'stem_vertex_count':420,'stem_axial_intervals':20,'radial_vertices_per_stem_ring':20,'stem_bounds_z':[min(p[2] for p in v[:420]),max(p[2] for p in v[:420])],'leaf_count':42,'leaf_centerline_lengths_m':lengths,'leaf_horizontal_lengths_m':horizontal,'leaf_length_range_m':[min(lengths),max(lengths)],'leaf_horizontal_range_m':[min(horizontal),max(horizontal)],'cone_bounds_z':[min(p[2] for p in cone),max(p[2] for p in cone)],'cone_max_radius_m':max(math.hypot(p[0],p[1]) for p in cone),'roots_count':24,'root_vertex_count':len(v)-2548}
elif aid=='glacier-crevasse-field':
 rows=[v[i*25:(i+1)*25] for i in range(24)];cr=[4,10,15,20];quiet=[p for i,row in enumerate(rows) if i not in cr+[5] for p in row];floors=[p for i in cr for p in rows[i]];widths=[]
 for a,b in [(3,6),(9,11),(14,16),(19,21)]:widths.append([math.dist(rows[a][j][:2],rows[b][j][:2]) for j in range(25)])
 metrics={'transverse_segments':24,'crack_count':4,'surface_height_range_m':[min(p[2] for p in quiet),max(p[2] for p in quiet)],'crack_floor_range_m':[min(p[2] for p in floors),max(p[2] for p in floors)],'crack_width_ranges_m':[[min(w),max(w)] for w in widths],'surface_vertices_over_13m':sum(p[2]>13+1e-6 for p in quiet),'surface_vertices_under_10m':sum(p[2]<10-1e-6 for p in quiet),'crack_floor_vertices_under_2p4m':sum(p[2]<2.4-1e-6 for p in floors)}
elif aid=='spatter-cone':
 rim=[p for p in v if .6<math.hypot(p[0],p[1])<1.7 and p[2]>1.8];floor=[p for p in v if math.hypot(p[0],p[1])<.4 and p[2]>.02]
 metrics={'height_m':max(p[2] for p in v)-min(p[2] for p in v),'rim_height_range_m':[min(p[2] for p in rim),max(p[2] for p in rim)],'vent_floor_points_range_m':[min(p[2] for p in floor),max(p[2] for p in floor)],'outer_radius_max_m':max(math.hypot(p[0],p[1]) for p in v)}
else:
 # Pool floor material faces split into five disconnected height bands.
 pool={}
 for o in objs:
  for f in o.data.polygons:
   if f.material_index in [3,4]:
    pts=[o.matrix_world@o.data.vertices[i].co for i in f.vertices];z=round(sum(p.z for p in pts)/len(pts),6);pool[z]=pool.get(z,0)+1
 metrics={'pool_floor_levels_and_face_counts':pool,'rise_per_level_m':[round(b-a,6) for a,b in zip(sorted(pool),sorted(pool)[1:])],'cross_segments':28,'pool_rim_relief_center_m':[]}
 rows=[v[i*29:(i+1)*29] for i in range(26)]
 for level in range(5):
  i=0 if level==0 else 6+(level-1)*5;floorrow=i+1 if level==0 else i;rimrow=i+3 if level==0 else i+2
  metrics['pool_rim_relief_center_m'].append(rows[rimrow][14][2]-rows[floorrow][14][2])
sa=audit_source(col,max_triangles=14000);ga=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30)
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(col.get('asset_root',''))
exp=out/'fresh-reexport.glb'
bpy.ops.export_scene.gltf(filepath=str(exp),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
ea=audit_glb(exp,max_triangles=14000,max_materials=6,max_primitives=30)
r={'asset_id':aid,'revision':rev,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'blender':bpy.app.version_string,'source_sha256':before,'source_unchanged':h(source)==before,'glb_sha256':h(glb),'source_saved':False,'parts':parts,'numeric_measurements':metrics,'source_audit':sa,'glb_audit':ga,'fresh_reexport':{'path':str(exp),'sha256':h(exp),'byte_equal':h(exp)==h(glb),'semantic_equal':ea['semantic_sha256']==ga['semantic_sha256'],'semantic_sha256':ea['semantic_sha256']}}
(out/'source-measurements.json').write_text(json.dumps(r,indent=2)+'\n');print('INDEPENDENT',aid,json.dumps(metrics),r['fresh_reexport'])
