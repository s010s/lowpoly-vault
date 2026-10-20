import bpy,sys,pathlib,json,hashlib,datetime
src,out=map(pathlib.Path,sys.argv[sys.argv.index('--')+1:]); source_hash=hashlib.sha256(src.read_bytes()).hexdigest()
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();col=bpy.data.collections.get('EXPORT')
if col is None: raise RuntimeError('No EXPORT collection')
dg=bpy.context.evaluated_depsgraph_get(); rows=[]; total={'authored_vertices':0,'authored_polygons':0,'evaluated_vertices':0,'evaluated_polygons':0}
for o in sorted(col.all_objects,key=lambda x:x.name):
 if o.type!='MESH': rows.append({'name':o.name,'type':o.type});continue
 m=o.data; e=o.evaluated_get(dg); em=e.to_mesh()
 row={'name':o.name,'type':'MESH','authored_vertices':len(m.vertices),'authored_polygons':len(m.polygons),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'bounds_local_min':[float(x) for x in o.bound_box[0]],'bounds_local_max':[float(x) for x in o.bound_box[6]],'materials':[x.name if x else None for x in m.materials]}
 for k in total:total[k]+=row[k]
 rows.append(row); e.to_mesh_clear()
imgs=[{'name':i.name,'source':i.source,'filepath':i.filepath,'packed':bool(i.packed_file)} for i in bpy.data.images]
r={'kind':'read_only_blender_source_counts','status':'pass','source_sha256':source_hash,'blender_version':bpy.app.version_string,'collection':'EXPORT','objects':rows,'totals':total,'bpy_data_images':imgs,'source_saved':False,'autoexec_disabled':True,'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','source_sha256','totals','bpy_data_images']}))
