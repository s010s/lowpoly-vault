import bpy,json,hashlib,pathlib,sys,math,collections,os,datetime
from mathutils import Vector
from mathutils.bvhtree import BVHTree
W=pathlib.Path('/workspace/shared/lowpoly-batch98-20261020');B=W/'production/small-life-batch98';O=pathlib.Path(__file__).parent
sys.path.insert(0,str(W/'scripts'));from qa_glb import audit_glb;from asset_common import audit_source
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
aid=sys.argv[sys.argv.index('--')+1];d=B/aid/'r001';out=O/aid;src=d/'artifacts'/f'{aid}.blend';glb=d/'artifacts'/f'{aid}.glb';brief=json.loads((d/'original-brief.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();contract=json.loads(bpy.data.texts['BATCH98_COMPONENT_CONTRACT.json'].as_string());obj=bpy.data.objects[contract['object_name']];v=[obj.matrix_world@x.co for x in obj.data.vertices];obj.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in obj.data.loop_triangles];comps=contract['components'];vertex_owner={i:c['tag'] for c in comps for i in c['vertices']};tby=collections.defaultdict(list)
for i,t in enumerate(tris):
 tags={vertex_owner.get(k) for k in t}
 if len(tags)!=1:raise RuntimeError('Triangle crosses component boundaries')
 tby[tags.pop()].append(i)
trees={c['tag']:BVHTree.FromPolygons(v,[tris[i] for i in tby[c['tag']]],all_triangles=True) for c in comps};whole=BVHTree.FromPolygons(v,tris,all_triangles=True);extent=max(max(x[k] for x in v)-min(x[k] for x in v) for k in range(3));eps=extent*1e-8;directions=[Vector(q) for q in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(1,1,1),(-1,-1,1),(1,-1,1),(-1,1,1)]];records=[]
for c in comps:
 pts=[v[i] for i in c['vertices']];sizes=[]
 for axis in c['axes']:
  a=(obj.matrix_world.to_3x3()@Vector(axis)).normalized();dots=[float(p.dot(a)) for p in pts];sizes.append(max(dots)-min(dots))
 r={'tag':c['tag'],'kind':c['kind'],'vertices':len(pts),'triangles':len(tby[c['tag']]),'aabb':{'min':[min(x[k] for x in pts) for k in range(3)],'max':[max(x[k] for x in pts) for k in range(3)]},'oriented_length_m':sizes[0],'oriented_width_m':sizes[1],'oriented_thickness_m':sizes[2],'length_width_ratio':sizes[0]/sizes[1] if sizes[1] else None,'parent':c['parent']}
 if c['parent']:
  tree=trees[c['parent']]
  def sd(i):
   q,n,_,_=tree.find_nearest(v[i]);return float((v[i]-q).dot(n))
  base=[sd(i) for i in c['base_vertices']];all_d=[sd(i) for i in c['vertices']];r.update(base_signed_distances_m=base,base_min_signed_distance_m=min(base),parent_exposed_vertices=sum(x>0 for x in all_d),parent_exposure_max_m=max(all_d))
 # Whole-object visibility, not merely parent-relative: test every triangle centroid until one is visible along an outward ray.
 hits=[];tested=0
 for ti in tby[c['tag']]:
  a,b,cc=[v[i] for i in tris[ti]];n=(b-a).cross(cc-a).normalized();p=(a+b+cc)/3
  for direct in [n,*directions]:
   ray=direct.normalized()
   if ray.dot(n)<=.05:continue
   tested+=1;q,_,hit,dist=whole.ray_cast(p+ray*eps,ray,extent*3)
   if hit is None:
    hits.append({'triangle':ti,'centroid':list(p),'direction':list(ray)});break
  if hits:break
 r.update(whole_object_exposed_surface_sample=hits,exposure_rays_tested=tested);records.append(r)
rg=[]
for rule in brief['hard_organ_ranges']:
 vals=[r for r in records if r['kind']==rule['kind']];lo,hi=rule['range'];rg.append({'rule':rule,'count':len(vals),'min':min(r[rule['measure']] for r in vals),'max':max(r[rule['measure']] for r in vals),'exact_failures':[r['tag'] for r in vals if not lo<=r[rule['measure']]<=hi]})
# Coincident leaf/lobe terminal centers expose collapsed branching hidden by group counts.
ends=collections.defaultdict(list)
for c in comps:
 if c['kind'] not in ['ultimate_lobe','leaf','terminal_bud','cladode']:continue
 a=(obj.matrix_world.to_3x3()@Vector(c['axes'][0])).normalized();pts=[v[i] for i in c['vertices']];mx=max(p.dot(a) for p in pts);tips=[p for p in pts if mx-p.dot(a)<extent*1e-7];cent=sum(tips,Vector())/len(tips);ends[tuple(round(float(q),7) for q in cent)].append(c['tag'])
coincident=[{'position_m':list(k),'components':x} for k,x in ends.items() if len(x)>1]
col=[c for c in bpy.data.collections if c.get('asset_root')];assert len(col)==1;col=col[0];sa=audit_source(col,14000)
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
exp=out/'source-reexport.glb';bpy.ops.export_scene.gltf(filepath=str(exp),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
a=audit_glb(glb,14000,6,30);e=audit_glb(exp,14000,6,30)
r={'schema_version':1,'asset_id':aid,'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'blender_version':bpy.app.version_string,'source_sha256':H(src),'glb_sha256':H(glb),'brief_sha256':H(d/'original-brief.json'),'source_reopened':True,'source_saved':False,'object_matrix':[list(x) for x in obj.matrix_world],'components':records,'component_count':len(records),'kind_counts':dict(collections.Counter(c['kind'] for c in comps)),'hard_ranges_exact':rg,'positive_base_signed_distance':[r['tag'] for r in records if r.get('base_min_signed_distance_m',0)>0],'fully_parent_buried':[r['tag'] for r in records if r.get('parent_exposure_max_m',1)<=0],'whole_object_no_visible_surface_sample':[r['tag'] for r in records if not r['whole_object_exposed_surface_sample']],'visibility_method':'Actual transformed triangle-centroid rays, outward normal and ten global directions, entire exact source mesh BVH. Positive result is explicit visible surface sample; negative requires targeted review, not proof of burial. Does not assert projected recognizability or absence of all intersections.','ray_start_epsilon_m':eps,'coincident_tips_1e_7m_quantization':coincident,'source_audit':sa,'reexport':{'path':str(exp),'sha256':H(exp),'semantic_sha256':e['semantic_sha256'],'original_semantic_sha256':a['semantic_sha256'],'semantic_equal':e['semantic_sha256']==a['semantic_sha256'],'byte_equal':H(exp)==H(glb),'errors':e['errors']}}
(out/'source-independent.json').write_text(json.dumps(r,separators=(',',':'))+'\n');print(json.dumps({k:r[k] for k in ['asset_id','component_count','kind_counts','hard_ranges_exact','positive_base_signed_distance','fully_parent_buried','whole_object_no_visible_surface_sample','coincident_tips_1e_7m_quantization','reexport']},indent=2))
