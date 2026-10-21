import sys,pathlib,json,hashlib,collections,datetime,os,math
sys.dont_write_bytecode=True
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=pathlib.Path('/workspace/shared/lowpoly-batch105-20261021');O=pathlib.Path('/workspace/shared/lowpoly-batch105-independent-qa-20261021');sys.path.insert(0,str(R/'scripts'))
from qa_glb import audit_glb
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
aid=sys.argv[sys.argv.index('--')+1];H=json.loads((R/'production/small-life-batch105/maker-handoff.json').read_text());a=next(a for a in H['assets'] if a['asset_id']==aid);D=R/'production/small-life-batch105'/aid/a['revision'];src=R/a['source']['path'];oldsha=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();rootcols=[c for c in bpy.data.collections if c.get('asset_root')];assert len(rootcols)==1;col=rootcols[0];ct=json.loads(bpy.data.texts['BATCH105_COMPONENT_CONTRACT.json'].as_string());ob=bpy.data.objects[ct['object_name']];vs=[ob.matrix_world@v.co for v in ob.data.vertices];ob.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in ob.data.loop_triangles];maxextent=max(max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3));eps=maxextent*1e-8;alltree=BVHTree.FromPolygons(vs,tris,all_triangles=True);components={c['tag']:c for c in ct['components']};frames={};meshes={};records=[];errors=[]
for tag,c in components.items():
 ids=set(c['vertices']);ts=[t for t in tris if set(t)<=ids];mesh=BVHTree.FromPolygons(vs,ts,all_triangles=True);meshes[tag]=mesh;ds=[(ob.matrix_world.to_3x3()@Vector(d)).normalized() for d in c['axes']];frames[tag]=ds;ps=[vs[i] for i in ids];sizes=[max(v.dot(d) for v in ps)-min(v.dot(d) for v in ps) for d in ds];es=collections.defaultdict(list)
 for t in ts:
  for x,y in zip(t,t[1:]+t[:1]):es[tuple(sorted((x,y)))].append(1 if x<y else -1)
 topo={'boundary_edges':sum(len(e)==1 for e in es.values()),'nonmanifold_edges':sum(len(e)>2 for e in es.values()),'same_direction_edges':sum(len(e)==2 and e[0]==e[1] for e in es.values()),'signed_volume_m3':sum(vs[t[0]].dot(vs[t[1]].cross(vs[t[2]]))/6 for t in ts),'euler_characteristic':len(ids)-len(es)+len(ts)};topo['pass']=topo['signed_volume_m3']>0 and all(topo[k]==0 for k in ['boundary_edges','nonmanifold_edges','same_direction_edges'])
 if not topo['pass']:errors.append('source topology '+tag)
 directions=[Vector(d).normalized() for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(.47,-.67,.57),(-.47,.67,.57)]];visible=0
 for t in ts:
  p=sum((vs[i] for i in t),Vector())/3
  if any(alltree.ray_cast(p+d*eps,d,maxextent*3)[0] is None for d in directions):visible+=1
 if not visible:errors.append('no actual global exposure '+tag)
 rec={'tag':tag,'kind':c['kind'],'vertices':len(ids),'triangles':len(ts),'oriented_length_m':sizes[0],'oriented_width_m':sizes[1],'oriented_thickness_m':sizes[2],'original_index_topology':topo,'all_scene_visible_triangle_centroids':visible,'all_scene_sampled_triangles':len(ts),'world_aabb_m':{'min':[min(v[k] for v in ps) for k in range(3)],'max':[max(v[k] for v in ps) for k in range(3)]}}
 if c.get('parent'):
  parent=components[c['parent']];pp=[t for t in tris if set(t)<=set(parent['vertices'])];tree=BVHTree.FromPolygons(vs,pp,all_triangles=True);signed=[]
  for i in c['base_vertices']:
   near,n,fi,dist=tree.find_nearest(vs[i]);signed.append((vs[i]-near).dot(n))
  overlaps=mesh.overlap(tree);rec['root_contact']={'parent':c['parent'],'base_vertices':len(c['base_vertices']),'signed_distance_m_min':min(signed),'signed_distance_m_max':max(signed),'intersecting_surface_triangle_pairs':len(overlaps),'pass':min(signed)<=eps and bool(overlaps)}
  if not rec['root_contact']['pass']:errors.append('root contact '+tag)
 records.append(rec)
# Actual non-parent contacts distinguish genuine free laterals from a fused net.
nonparent=[]
for i,(tag,c) in enumerate(components.items()):
 for tag2,c2 in list(components.items())[i+1:]:
  if c.get('parent')==tag2 or c2.get('parent')==tag:continue
  pair=meshes[tag].overlap(meshes[tag2]);nonparent.append({'a':tag,'b':tag2,'intersections':len(pair)})
  if aid=='penniretepora' and pair:errors.append('fused laterals '+tag+' '+tag2)
features=[];rows=collections.defaultdict(list)
for f in ct['integrated_features']:
 pts=[vs[i] for i in f['vertices']];ds=frames[f['component']];normal=ds[2]*f.get('side',1);r={'tag':f['tag'],'kind':f['kind'],'component':f['component'],'side':f.get('side')}
 if f['kind']=='recessed_aperture':
  rim=pts[:8];center=sum(rim,Vector())/8;bottom=pts[-1];w=max(v.dot(ds[1]) for v in rim)-min(v.dot(ds[1]) for v in rim);depth=(center-bottom).dot(normal);hit=alltree.ray_cast(bottom+normal*eps,normal,maxextent*3);lum=hit[0] is None;r.update(width_m=w,mean_rim_to_bottom_depth_m=depth,unobstructed_bottom_to_outside=lum,blocking_distance_m=hit[3] if hit[0] is not None else None,row_coordinate_m=center.dot(ds[1]),station_coordinate_m=center.dot(ds[0]));rows[(f['component'],f.get('side'))].append(r)
  if depth<=0:errors.append('not a cavity '+f['tag'])
  hard={'penniretepora':(.00006,.00008),'cystodictya':(.00010,.00018)}.get(aid)
  if hard and not hard[0]-1e-10<=w<=hard[1]+1e-10:errors.append('aperture range '+f['tag'])
 elif f['kind']=='integrated_stellate_depression':
  center=pts[-1];rim=pts[:-1];rel=[(v-center).dot(normal) for v in rim];hit=alltree.ray_cast(center+normal*eps,normal,maxextent*3);r.update(center_below_surrounding_m_min=min(rel),center_below_surrounding_m_max=max(rel),unobstructed_center_to_outside=hit[0] is None)
  if min(rel)<-1e-10 or max(rel)<=0:errors.append('not depressed '+f['tag'])
  if hit[0] is not None:errors.append('macula center covered '+f['tag'])
 elif f['kind']=='open_fenestrule':
  r.update(actual_vertex_count=len(pts))
 features.append(r)
rowresults=[]
for key,rs in rows.items():
 if aid=='constellaria':continue
 groups=[]
 for r in sorted(rs,key=lambda r:r['row_coordinate_m']):
  if not groups or abs(groups[-1][-1]['row_coordinate_m']-r['row_coordinate_m'])>1e-8:groups.append([r])
  else:groups[-1].append(r)
 rr={'component':key[0],'side':key[1],'actual_geometric_rows':len(groups),'required':2 if aid=='penniretepora' else 5,'row_apertures':[len(g) for g in groups],'row_unobstructed_lumens':[sum(r['unobstructed_bottom_to_outside'] for r in g) for g in groups]};rr['pass']=rr['actual_geometric_rows']==rr['required'] and all(n>0 for n in rr['row_unobstructed_lumens']);rowresults.append(rr)
 if not rr['pass']:errors.append('required visible rows '+str(key))
brief=json.loads((D/'original-brief.json').read_text());ranges=[]
for rule in brief['hard_organ_ranges']:
 vals=[r[rule['measure']] for r in records if r['kind']==rule['kind']];lo,hi=rule['range'];ok=all(lo-1e-10<=v<=hi+1e-10 for v in vals);ranges.append({'rule':rule,'actual':vals,'pass':ok})
 if not ok:errors.append('scientific hard range '+str(rule))
# Re-export every original asset-collection object. No mesh edit/repair/source save.
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(col['asset_root'])
opts=dict(filepath=str(O/'exports'/(aid+'.glb')),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);old=audit_glb(D/'artifacts'/(aid+'.glb'),14000,6,30);new=audit_glb(O/'exports'/(aid+'.glb'),14000,6,30);match=old['semantic_sha256']==new['semantic_sha256'];assert sha(src)==oldsha
if not match:errors.append('full collection reexport semantic mismatch')
result={'asset_id':aid,'revision':a['revision'],'source_sha256':oldsha,'glb_sha256':a['triplet']['glb_sha256'],'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_pid':os.getpid(),'blender_version':bpy.app.version_string,'source_modified':False,'source_repaired':False,'evaluated_full_collection':[(o.name,o.type) for o in col.all_objects],'actual_transform':[list(r) for r in ob.matrix_world],'components':records,'nonparent_intersections':nonparent,'features':features,'rows':rowresults,'hard_range_checks':ranges,'full_collection_reexport':{'path':str(O/'exports'/(aid+'.glb')),'sha256':sha(O/'exports'/(aid+'.glb')),'semantic_sha256':new['semantic_sha256'],'matches_original':match,'original_semantic_sha256':old['semantic_sha256'],'triangles':new['scene_triangles'],'bounds':new['bounds_m']},'errors':errors,'pass':not errors,'limitations':'Finite eight-direction surface and normal-direction cavity ray sampling; no percentage gate. Does not prove GPU or composed scene behavior.'}
(O/'reports'/(aid+'-source-independent.json')).write_text(json.dumps(result,indent=2)+'\n');print('INDEPENDENT_RESULT',aid,'pass' if not errors else 'fail',errors)
