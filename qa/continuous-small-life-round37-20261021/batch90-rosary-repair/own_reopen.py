import bpy,sys,json,hashlib,os,datetime,math,collections,struct
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/shared/lowpoly-batch90-rosary-repair-20261020');B=R/'production/batch90-rosary-repair/assets/rosary-shaped-chambered-burrow-hormosiroidea-type/r002';O=Path('/workspace/shared/lowpoly-batch90-rosary-repair-independent-qa-20261021');sys.path.insert(0,str(R/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();start=now();src=B/'source.blend';pins={str(p):H(p) for p in [src,B/'model.glb']}
bpy.context.preferences.filepaths.use_scripts_auto_execute=False;bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();col=bpy.data.collections['EXPORT'];dg=bpy.context.evaluated_depsgraph_get();rows=[];parts=[];components=[]
# Independently reconstruct the unchanged original 97point S-path from its inspected construction, not the maker semantic JSON.
path=[Vector((-.04+.08*i/96,.009*math.sin(math.tau*i/96-.4))) for i in range(97)];f32=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
for o in col.all_objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();ev=o.evaluated_get(dg);em=ev.to_mesh();em.calc_loop_triangles();parts.append(dict(name=o.name,authored_vertices=len(m.vertices),evaluated_vertices=len(em.vertices),authored_triangles=len(m.loop_triangles),evaluated_triangles=len(em.loop_triangles),modifiers=len(o.modifiers)));ev.to_mesh_clear()
 adj=[set() for _ in m.vertices];counts=collections.Counter(tuple(sorted(e)) for f in m.polygons for e in f.edge_keys)
 for a,b in counts:adj[a].add(b);adj[b].add(a)
 unseen=set(range(len(adj)))
 while unseen:
  q=unseen.pop();ids={q};todo=[q]
  while todo:
   for k in adj[todo.pop()]:
    if k in unseen:unseen.remove(k);ids.add(k);todo.append(k)
  components.append(dict(vertices=len(ids),boundary_edges=sum(n==1 for (a,b),n in counts.items() if a in ids),nonmanifold_edges=sum(n!=2 for (a,b),n in counts.items() if a in ids)))
 for vert in m.vertices:
  xyz=list(o.matrix_world@vert.co);q=Vector(xyz[:2]);ds=[]
  for a,b in zip(path,path[1:]):
   v=b-a;t=max(0.,min(1.,(q-a).dot(v)/v.length_squared));ds.append((q-a-v*t).length)
  d=min(ds);neck=.0013*math.sqrt(max(0.,1.-(d/.001)**2)) if d<.001 else 0.;baseline=f32(.009+neck) if xyz[2]>=f32(.009) else xyz[2]
  rows.append(dict(xyz=xyz,neck_baseline_z=baseline,chamber_increment=xyz[2]-baseline,neck_distance=d))
sa=audit_source(col,14000);bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
# Explicit independent export options, matched to documented uncompressed static format.
bpy.ops.export_scene.gltf(filepath=str(O/'source-reexport.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
ga=audit_glb(B/'model.glb',14000,6,30);ra=audit_glb(O/'source-reexport.glb',14000,6,30)
r=dict(started_at_host=start,finished_at_host=now(),pid=os.getpid(),blender=bpy.app.version_string,source_sha256=H(src),glb_sha256=H(B/'model.glb'),source_unchanged=all(H(Path(p))==v for p,v in pins.items()),source_saved=False,autoexec=False,parts=parts,components=components,source_audit=sa,glb_audit=ga,reexport_sha256=H(O/'source-reexport.glb'),reexport_semantic_match=ga['semantic_sha256']==ra['semantic_sha256'],reexport_byte_match=H(O/'source-reexport.glb')==H(B/'model.glb'),baseline_method='Original neck kernel evaluated at actual reopened source vertices with Blender Vector arithmetic and float32 output conversion; no maker baseline or contribution labels consumed.')
(O/'own-source-reopen-reexport.json').write_text(json.dumps(r,indent=2)+'\n');(O/'own-source-vertices-baseline.json').write_text(json.dumps(dict(source_sha256=H(src),glb_sha256=H(B/'model.glb'),rows=rows),indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['source_audit','glb_audit']}))
assert r['source_unchanged'] and r['reexport_byte_match'] and r['reexport_semantic_match'];assert all(x['nonmanifold_edges']==0 for x in components);assert len(components)==1
