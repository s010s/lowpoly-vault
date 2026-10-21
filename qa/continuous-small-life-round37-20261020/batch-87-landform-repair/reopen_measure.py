import bpy,sys,json,hashlib,datetime,os,math
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path('/workspace/shared/lowpoly-batch87-landform-repair-20261020');P=R/'production/batch87-landform-repair';O=Path('/workspace/shared/lowpoly-batch87-landform-repair-independent-qa-20261020');sys.path.insert(0,str(R/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb,read_glb,accessor_values,node_matrix,matmul,transform
args=sys.argv[sys.argv.index('--')+1:];aid,rev=args;out=O/aid;out.mkdir(exist_ok=True);p=P/aid/rev/'artifacts';source=p/(aid+'.blend');glb=p/(aid+'.glb');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=h(source);start=datetime.datetime.now(datetime.timezone.utc).isoformat()
bpy.context.preferences.filepaths.use_scripts_auto_execute=False;bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False);bpy.context.view_layer.update();col=bpy.data.collections['EXPORT'];objs=[o for o in col.all_objects if o.type=='MESH'];dg=bpy.context.evaluated_depsgraph_get();parts=[];v=[];evv=[]
for ob in objs:
 me=ob.data;me.calc_loop_triangles();ev=ob.evaluated_get(dg);em=ev.to_mesh();em.calc_loop_triangles();pts=[list(ob.matrix_world@p.co)for p in me.vertices];v+=pts;evv += [list(ev.matrix_world@p.co)for p in em.vertices];edges={};tri=[tuple(t.vertices)for t in me.loop_triangles]
 for f in me.polygons:
  for i,a in enumerate(f.vertices):
   b=f.vertices[(i+1)%len(f.vertices)];key=tuple(sorted((a,b)));edges[key]=edges.get(key,0)+1
 tree=BVHTree.FromPolygons(pts,tri,all_triangles=True);hits=[(a,b)for a,b in tree.overlap(tree)if a<b and not set(tri[a])&set(tri[b])]
 parts.append({'name':ob.name,'authored_vertices':len(me.vertices),'authored_polygons':len(me.polygons),'authored_triangles':len(tri),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':len(em.loop_triangles),'modifiers':len(ob.modifiers),'world_matrix':[list(row)for row in ob.matrix_world],'non_two_face_edges':sum(n!=2 for n in edges.values()),'nonadjacent_bvh_overlaps':len(hits),'sample_overlap_pairs':hits[:12]});ev.to_mesh_clear()
bounds=lambda ps:{'min':[min(p[k]for p in ps)for k in range(3)],'max':[max(p[k]for p in ps)for k in range(3)],'size':[max(p[k]for p in ps)-min(p[k]for p in ps)for k in range(3)]}
stats=lambda x:{'min':min(x),'max':max(x),'mean':sum(x)/len(x),'count':len(x)}
# Full default-scene traversal, honoring every ancestor and mesh node transform.
doc,blob,_=read_glb(glb);allpos=[];nodes=[];I=[1.,0.,0.,0.,0.,1.,0.,0.,0.,0.,1.,0.,0.,0.,0.,1.]
def walk(n,parent):
 nd=doc['nodes'][n];world=matmul(parent,node_matrix(nd));nodes.append({'index':n,'world_matrix':world})
 if 'mesh'in nd:
  for primitive in doc['meshes'][nd['mesh']]['primitives']:
   for pos in accessor_values(doc,blob,primitive['attributes']['POSITION']):
    x,y,z=transform(world,pos);allpos.append([x,-z,y])
 for c in nd.get('children',[]):walk(c,world)
for n in doc['scenes'][doc.get('scene',0)]['nodes']:walk(n,I)
lookup={tuple(p):p for p in allpos};mapped=[];dist=[]
for pt in v:
 q=lookup.get(tuple(pt))
 if q is None:q=min(allpos,key=lambda q:sum((a-b)**2 for a,b in zip(pt,q)))
 mapped.append(q);dist.append(math.dist(pt,q))
measure={}
for label,ps in [('source',v),('glb_world',mapped)]:
 if aid=='spatter-cone':
  N=64;nr=23;crest=ps[384:448];floor=ps[:128];clearance=[crest[j][2]-max(ps[k*N+j][2]for k in range(nr)if k!=6)for j in range(N)]
  ms={'crest_z':stats([x[2]for x in crest]),'crest_radius':stats([math.hypot(x[0],x[1])for x in crest]),'floor_z':stats([x[2]for x in floor]),'crest_clearance_vs_all_other_rings':stats(clearance),'actual_surface_rings':(len(ps)-N)//N,'rays_per_ring':64,'max_final_radius':max(math.hypot(x[0],x[1])for x in ps),'actual_floor_closing_face_indices':list(ob.data.polygons[0].vertices)}
 else:
  regions=[(l,k)for l in range(5)for k in range(6)if l==0 or k!=0];rows=[ps[i*29:(i+1)*29]for i in range(26)];floors=[rows[i][14][2]for i,(l,k)in enumerate(regions)if k==1];lip=[]
  for i,(l,k)in enumerate(regions):
   if k not in(3,4):continue
   for j,pt in enumerate(rows[i]):
    t=-1+j/14;edge=.2*max(0,(abs(t)-.78)/.22);rough=.035*math.sin(j*1.3+l*2+k*.9)if abs(t)>.83 else 0;saddle=.15*math.exp(-((t-(.27 if l%2 else -.22))/.13)**2);observed=pt[2]-floors[l];lip.append({'vertex':i*29+j,'actual_relief':observed,'nominal_after_declared_edge_saddle_terms':observed-edge-rough+saddle})
  ms={'floor_z':floors,'consecutive_rises':[a-b for a,b in zip(floors,floors[1:])],'lip_actual_relief':stats([x['actual_relief']for x in lip]),'recovered_nominal_lip':stats([x['nominal_after_declared_edge_saddle_terms']for x in lip]),'lip_samples':lip,'cross_intervals':28,'top_rows':26,'bottom_vertices_z':stats([pt[2]for pt in ps[26*29:]])}
 measure[label]=ms
sa=audit_source(col,max_triangles=14000);ga=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30)
bpy.ops.object.select_all(action='DESELECT')
for ob in col.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(col.get('asset_root',''));exp=out/'fresh-reexport.glb'
bpy.ops.export_scene.gltf(filepath=str(exp),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
ea=audit_glb(exp,max_triangles=14000,max_materials=6,max_primitives=30);original_difference=None
if aid=='travertine-terrace-pools':
 orig=Path('/workspace/shared/lowpoly-batch87-20261020/production/small-life-batch87/travertine-terrace-pools/r002/artifacts/travertine-terrace-pools.blend');orig_h=h(orig);bpy.ops.wm.open_mainfile(filepath=str(orig),load_ui=False,use_scripts=False);old=[list(o.matrix_world@p.co)for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH'for p in o.data.vertices];original_difference={'original_source_sha256':orig_h,'original_unchanged':h(orig)==orig_h,'old_vertex_count':len(old),'new_vertex_count':len(v),'top_z_translation_m':stats([v[i][2]-old[i][2]for i in range(754)]),'bottom_z_translation_m':stats([v[i][2]-old[i][2]for i in range(754,860)]),'old_world_bounds':bounds(old),'new_world_bounds':bounds(v)}
r={'asset_id':aid,'revision':rev,'started_at_host':start,'finished_at_host':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'blender':bpy.app.version_string,'source_sha256':before,'source_unchanged':h(source)==before,'source_saved':False,'glb_sha256':h(glb),'parts':parts,'source_world_bounds':bounds(v),'evaluated_world_bounds':bounds(evv),'glb_world_bounds_blender_axes':bounds(allpos),'glb_node_transforms':nodes,'max_source_glb_correspondence_error_m':max(dist),'measurements':measure,'original_difference':original_difference,'source_audit':sa,'glb_audit':ga,'fresh_reexport':{'path':str(exp),'sha256':h(exp),'byte_equal':h(exp)==h(glb),'semantic_equal':ea['semantic_sha256']==ga['semantic_sha256'],'semantic_sha256':ea['semantic_sha256']}}
(out/'source-measurements.json').write_text(json.dumps(r,indent=2)+'\n');print('INDEPENDENT',aid,json.dumps({'bounds':r['source_world_bounds'],'correspondence_error':max(dist),'parts':parts,'reexport':r['fresh_reexport']}))
