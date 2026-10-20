import sys,os,json,hashlib,datetime,math,collections
sys.dont_write_bytecode=True
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
from asset_common import audit_source
from check_source_export import compare_source_audit
p=Path(sys.argv[sys.argv.index('--')+1]);out=Path(sys.argv[sys.argv.index('--')+2]);out.mkdir(exist_ok=True,parents=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
t=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
started=t();h=sha(p);bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
bpy.context.view_layer.update();cols=[c for c in bpy.data.collections if c.get('asset_root')];assert len(cols)==1
col=cols[0];parts=[];comps=[]
for o in col.all_objects:
 if o.type!='MESH':continue
 me=o.data;me.calc_loop_triangles();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();em.calc_loop_triangles()
 bm=bmesh.new();bm.from_mesh(me)
 parts.append({'object':o.name,'authored_vertices':len(me.vertices),'authored_polygons':len(me.polygons),'authored_triangles':len(me.loop_triangles),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':len(em.loop_triangles),'modifiers':len(o.modifiers),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'wire_edges':sum(e.is_wire for e in bm.edges),'signed_volume':bm.calc_volume(signed=True),'properties':{k:o[k] for k in o.keys() if k in ['negative_relief_depth_m','design_trace_pairs_json']}});bm.free();ev.to_mesh_clear()
 adj=[set() for _ in me.vertices]
 for e in me.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
 unseen=set(range(len(adj)))
 while unseen:
  i=min(unseen);todo=[i];seen={i};unseen.remove(i)
  while todo:
   for q in adj[todo.pop()]:
    if q in unseen:unseen.remove(q);seen.add(q);todo.append(q)
  inds=sorted(seen);pts=[o.matrix_world@me.vertices[x].co for x in inds];polys=[f for f in me.polygons if f.vertices[0] in seen];lo=[min(v[k] for v in pts) for k in range(3)];hi=[max(v[k] for v in pts) for k in range(3)];mats=sorted({me.materials[f.material_index].name for f in polys});co={'object':o.name,'first_vertex':i,'vertices':len(pts),'faces':len(polys),'bounds':{'min':lo,'max':hi,'size':[hi[k]-lo[k] for k in range(3)]},'materials':mats}
  if len(pts)==8 and len(polys)==12:
   co['leaf_base_tip_length_m']=(pts[3]-pts[0]).length;co['leaf_max_chord_m']=max((a-b).length for a in pts for b in pts);co['leaf_width_m']=(pts[2]-pts[4]).length;co['leaf_thickness_m']=(pts[6]-pts[7]).length
  comps.append(co)
actual=audit_source(col,max_triangles=14000)
glb=p.with_suffix('.glb');a=audit_glb(glb,14000,6,30)
compare=compare_source_audit(actual,a,h,sha(glb))
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(col.get('asset_root',''))
fresh=out/(p.stem+'-reexport.glb')
bpy.ops.export_scene.gltf(filepath=str(fresh),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
f=audit_glb(fresh,14000,6,30)
r={'schema_version':1,'started_at':started,'finished_at':t(),'pid':os.getpid(),'parent_pid':os.getppid(),'blender':bpy.app.version_string,'argv':sys.argv,'source_path':str(p),'source_sha256':h,'source_unchanged':h==sha(p),'source_saved':False,'script_autoexec':False,'source_comparison':compare,'parts':parts,'components':comps,'totals':{k:sum(x[k] for x in parts) for k in ['authored_vertices','authored_polygons','authored_triangles','evaluated_vertices','evaluated_polygons','evaluated_triangles']},'original_glb_audit':a,'fresh_glb_audit':f,'byte_identical':sha(glb)==sha(fresh),'semantic_match':a['semantic_sha256']==f['semantic_sha256']}
leaves=[c for c in comps if 'leaf_base_tip_length_m' in c]
if leaves:r['leaf_measurements']={'count':len(leaves),'base_tip_length_range_m':[min(c['leaf_base_tip_length_m'] for c in leaves),max(c['leaf_base_tip_length_m'] for c in leaves)],'max_chord_range_m':[min(c['leaf_max_chord_m'] for c in leaves),max(c['leaf_max_chord_m'] for c in leaves)],'thickness_range_m':[min(c['leaf_thickness_m'] for c in leaves),max(c['leaf_thickness_m'] for c in leaves)],'over_frozen_max_0_23':sum(c['leaf_base_tip_length_m']>.230001 for c in leaves),'under_frozen_min_0_15':sum(c['leaf_base_tip_length_m']<.149999 for c in leaves)}
# Additional actual world-space measurements and immutable r001 differential.
r['normalization']=json.loads(bpy.context.scene['repair_normalization'])
leafcomps=[c for c in comps if c.get('leaf_base_tip_length_m')]
verts=[o.matrix_world@v.co for o in col.all_objects if o.type=='MESH' for v in o.data.vertices]
connections=[]
for c in leafcomps:
 first=c['first_vertex'];spray=max(x['first_vertex'] for x in comps if x['vertices']==15 and x['first_vertex']<first)
 centers=[sum((verts[spray+5*k+j] for j in range(5)),Vector())/5 for k in range(3)]
 axis=centers[2]-centers[0];base=verts[first];tt=(base-centers[0]).dot(axis)/axis.length_squared;distance=(base-(centers[0]+axis*tt)).length
 connections.append({'first_vertex':first,'spray_first_vertex':spray,'axis_fraction':tt,'base_axis_distance_m':distance,'length_m':c['leaf_base_tip_length_m'],'width_m':c['leaf_width_m'],'width_to_length':c['leaf_width_m']/c['leaf_base_tip_length_m'],'thickness_m':c['leaf_thickness_m']})
r['leaf_connections']=connections
r['leaf_measurements']['width_to_length_range']=[min(x['width_to_length'] for x in connections),max(x['width_to_length'] for x in connections)]
r['leaf_measurements']['maximum_base_axis_distance_m']=max(x['base_axis_distance_m'] for x in connections)
r['leaf_measurements']['float_tolerance_m']=1e-6
r['leaf_measurements']['strict_outside_nominal_float_count']=sum(x['length_m']<.15 or x['length_m']>.23 for x in connections)
r['measured_component_counts']={str(k):v for k,v in collections.Counter((c['vertices'],c['faces']) for c in comps).items()}
r['measured_parameter_interpretations']={'leaf_length_range_m':'Hard final meter range, measured above; tolerance only 1e-6m float precision.','leaf_width_to_length':'Actual side vertex separation divided by actual base-tip length.','leaf_thickness_m':'Actual peak-to-peak local normal separation; preserves 0.009m.','normalized_total_height_m':'Hard final 3.8m height.','trunk_base_diameter_m':'Original construction section before basal flare x1.33 and skeleton normalization. Actual basal ring maximum chord is measured.','trunk_top_height_m':'Original centerline input before skeleton normalization; not total tree height.','root_radius_m':'Original radial envelope input times per-root .84+.14*sin(j*2.2), then skeleton normalization; actual tips are measured.'}
r['actual_skeleton_dimensions']={'trunk_base_flared_max_chord_m':max((a-b).length for a in verts[:10] for b in verts[:10]),'trunk_centerline_height_m':(sum(v.z for v in verts[110:120])-sum(v.z for v in verts[:10]))/10,'root_tip_center_xy_radii_m':[]}
for c in comps:
 if c['vertices']==24:
  first=c['first_vertex'];center=sum((verts[first+18+j] for j in range(6)),Vector())/6;r['actual_skeleton_dimensions']['root_tip_center_xy_radii_m'].append(math.hypot(center.x,center.y))
old=Path('/workspace/shared/lowpoly-batch91-20261020/production/small-life-batch91/archaeopteris/r001/artifacts/archaeopteris.blend');oldsha=sha(old)
bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ov=[o.matrix_world@v.co for o in bpy.data.objects if o.type=='MESH' for v in o.data.vertices];assert len(ov)==len(verts)
li={c['first_vertex']+j for c in leafcomps for j in range(8)};scale_ratio=r['normalization']['skeleton_scale']/r['normalization']['old_scale']
r['r001_difference']={'source_sha256':oldsha,'source_unchanged':sha(old)==oldsha,'same_vertex_count':True,'max_vertex_displacement_m':max((a-b).length for a,b in zip(verts,ov)),'max_nonleaf_displacement_m':max((verts[i]-ov[i]).length for i in range(len(verts)) if i not in li),'max_skeleton_expected_uniform_scale_error_m':max((verts[i]-ov[i]*scale_ratio).length for i in range(len(verts)) if i not in li),'max_leaf_base_expected_uniform_scale_error_m':max((verts[c['first_vertex']]-ov[c['first_vertex']]*scale_ratio).length for c in leafcomps),'max_leaf_axis_direction_change_rad':max((verts[c['first_vertex']+3]-verts[c['first_vertex']]).angle(ov[c['first_vertex']+3]-ov[c['first_vertex']]) for c in leafcomps),'note':'Only blade dimensions and the analytically necessary common skeleton scale change. No topology, component counts, palette or orientation design change.'}
assert len(leafcomps)==576 and r['leaf_measurements']['over_frozen_max_0_23']==0 and r['leaf_measurements']['under_frozen_min_0_15']==0
assert all(abs(x['thickness_m']-.009)<1e-6 and abs(x['width_to_length']-.62)<1e-5 for x in connections)
assert r['leaf_measurements']['maximum_base_axis_distance_m']<1e-6
(out/'reopen-reexport.report.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:r[k] for k in ['pid','source_unchanged','semantic_match','byte_identical','totals']}));print(json.dumps(r.get('leaf_measurements')))
assert not a['errors'] and not f['errors'] and not compare['errors'] and r['semantic_match'] and r['source_unchanged']
