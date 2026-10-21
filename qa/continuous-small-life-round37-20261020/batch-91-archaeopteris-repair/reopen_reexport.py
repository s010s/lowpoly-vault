import bpy,bmesh,sys,os,json,hashlib,datetime
from pathlib import Path
sys.dont_write_bytecode=True
S=Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-20261020');O=Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-independent-qa-20261021');A=S/'production/batch91-archaeopteris-repair/archaeopteris/r002/artifacts'
sys.path.insert(0,str(S/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb
from check_source_export import compare_source_audit
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
started=now();bpy.context.preferences.filepaths.use_scripts_auto_execute=False

def extract(path):
 h=sha(path);bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);bpy.context.view_layer.update()
 cols=[c for c in bpy.data.collections if c.get('asset_root')];assert len(cols)==1;col=cols[0];parts=[]
 for ob in col.all_objects:
  if ob.type!='MESH':continue
  me=ob.data;me.calc_loop_triangles();ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();em.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(me)
  parts.append({'name':ob.name,'matrix_world':[list(r) for r in ob.matrix_world],'vertices':[list(ob.matrix_world@v.co) for v in me.vertices],'edges':[list(e.vertices) for e in me.edges],'polygons':[list(p.vertices) for p in me.polygons],'material_indices':[p.material_index for p in me.polygons],'authored_vertices':len(me.vertices),'authored_polygons':len(me.polygons),'authored_triangles':len(me.loop_triangles),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':len(em.loop_triangles),'modifiers':len(ob.modifiers),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'boundary_edges':sum(e.is_boundary for e in bm.edges),'wire_edges':sum(e.is_wire for e in bm.edges),'signed_volume':bm.calc_volume(signed=True)})
  bm.free();ev.to_mesh_clear()
 assert sha(path)==h
 return {'source_path':str(path),'sha256':h,'parts':parts,'libraries':[str(x.filepath) for x in bpy.data.libraries],'image_dependencies':[str(x.filepath) for x in bpy.data.images if x.filepath],'audit':audit_source(col,max_triangles=14000)},col
new,col=extract(A/'archaeopteris.blend')
bpy.ops.object.select_all(action='DESELECT')
for ob in col.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(col.get('asset_root',''))
fresh=O/'archaeopteris-reexport.glb'
bpy.ops.export_scene.gltf(filepath=str(fresh),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
a=audit_glb(A/'archaeopteris.glb',14000,6,30);f=audit_glb(fresh,14000,6,30);comparison=compare_source_audit(new['audit'],a,new['sha256'],sha(A/'archaeopteris.glb'))
old,_=extract(Path('/workspace/shared/lowpoly-batch91-20261020/production/small-life-batch91/archaeopteris/r001/artifacts/archaeopteris.blend'))
(O/'source-geometry.json').write_text(json.dumps({'old':old,'new':new},separators=(',',':'))+'\n')
r={'started_at':started,'finished_at':now(),'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'blender':bpy.app.version_string,'source_sha256':new['sha256'],'source_unchanged':sha(A/'archaeopteris.blend')==new['sha256'],'source_saved':False,'autoexec':False,'byte_identical':sha(fresh)==sha(A/'archaeopteris.glb'),'semantic_match':a['semantic_sha256']==f['semantic_sha256'],'totals':{k:sum(p[k] for p in new['parts']) for k in ['authored_vertices','authored_polygons','authored_triangles','evaluated_vertices','evaluated_polygons','evaluated_triangles','modifiers','nonmanifold_edges','boundary_edges','wire_edges']},'source_comparison':comparison,'fresh_glb_audit':f,'original_glb_audit':a,'libraries':new['libraries'],'image_dependencies':new['image_dependencies']}
(O/'reopen-reexport.report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));assert r['source_unchanged'] and r['semantic_match'] and not a['errors'] and not f['errors'] and not comparison['errors']
