import bpy,bmesh,sys,json,hashlib,datetime,math,os
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/shared/lowpoly-batch88-20261020');Q=Path('/workspace/shared/lowpoly-batch88-independent-qa-20261020')
sys.path.insert(0,str(R/'scripts'));from asset_common import audit_source
from qa_glb import audit_glb
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
aid,rev=sys.argv[sys.argv.index('--')+1:];d=R/'production/batch88/assets'/aid/rev;out=Q/aid;out.mkdir(exist_ok=True)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();before={n:H(d/n) for n in ['source.blend','model.glb','generator.py','build-config.json']}
bpy.context.preferences.filepaths.use_scripts_auto_execute=False;bpy.ops.wm.open_mainfile(filepath=str(d/'source.blend'),load_ui=False,use_scripts=False);bpy.context.view_layer.update();col=bpy.data.collections['EXPORT'];counts=[];leaves=[];meshes={}
for o in col.all_objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();em.calc_loop_triangles()
 coords=[o.matrix_world@v.co for v in m.vertices];adj=[[] for _ in coords]
 for e in m.edges:a,b=e.vertices;adj[a].append(b);adj[b].append(a)
 visited=set();components=[]
 for i in range(len(coords)):
  if i in visited:continue
  comp=[];stack=[i];visited.add(i)
  while stack:
   k=stack.pop();comp.append(k)
   for j in adj[k]:
    if j not in visited:visited.add(j);stack.append(j)
  components.append(sorted(comp))
 bm=bmesh.new();bm.from_mesh(m);bad={'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'loose_edges':sum(e.is_wire for e in bm.edges)};bm.free()
 counts.append(dict(name=o.name,authored_vertices=len(m.vertices),authored_polygons=len(m.polygons),authored_triangles=len(m.loop_triangles),evaluated_vertices=len(em.vertices),evaluated_polygons=len(em.polygons),evaluated_triangles=len(em.loop_triangles),connected_components=len(components),component_vertex_counts=sorted(set(map(len,components))),topology=bad))
 meshes[o.name]={'vertices':[list(v) for v in coords],'faces':[list(p.vertices) for p in m.polygons],'material_indices':[p.material_index for p in m.polygons],'materials':[x.name for x in m.materials]}
 if 'leaf' in o.name:
  for c in components:
   vs=[coords[i] for i in c]
   assert len(vs)==10
   c1=sum(vs[1:5],Vector())/4;c2=sum(vs[5:9],Vector())/4
   leaves.append(dict(vertices=10,base_tip_chord_m=(vs[9]-vs[0]).length,centerline_length_m=(c1-vs[0]).length+(c2-c1).length+(vs[9]-c2).length,max_pairwise_m=max((a-b).length for a in vs for b in vs),width_m=max((vs[1]-vs[3]).length,(vs[5]-vs[7]).length),thickness_m=max((vs[2]-vs[4]).length,(vs[6]-vs[8]).length)))
 ev.to_mesh_clear()
source=audit_source(col,14000);exp=audit_glb(d/'model.glb',14000,6,30)
root=bpy.data.objects[col['asset_root']];bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
opts=json.loads((d/'metrics.json').read_text())['export_options'];opts['filepath']=str(out/'source-reexport.glb');bpy.ops.export_scene.gltf(**opts)
reh=H(out/'source-reexport.glb');reaudit=audit_glb(out/'source-reexport.glb',14000,6,30)
report=dict(asset_id=aid,revision=rev,started_at=start,ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),pid=os.getpid(),blender_version=bpy.app.version_string,source_saved=False,source_hashes_unchanged=before=={n:H(d/n) for n in before},source_hashes=before,source_audit=source,export_audit=exp,parts=counts,reexport_sha256=reh,byte_identical=reh==before['model.glb'],semantic_counts_bounds_match=(reaudit['scene_triangles']==exp['scene_triangles'] and reaudit['bounds_m']==exp['bounds_m']),leaf_count=len(leaves),leaf_measurements_summary={k:{'min':min(l[k] for l in leaves),'max':max(l[k] for l in leaves)} for k in leaves[0]} if leaves else {})
(out/'source-inspection.json').write_text(json.dumps(report,indent=2)+'\n');(out/'mesh-measure-input.json').write_text(json.dumps(meshes,separators=(',',':'))+'\n')
print('INDEPENDENT',aid,'identical',report['byte_identical'],'leaves',len(leaves),'errors',source['errors'],exp['errors'])
