# SPDX-License-Identifier: MIT
"""Read both editable sources without saving; compare actual evaluated/source mesh geometry and normals."""
import bpy,json,hashlib,sys
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:];baseline,revision,output=map(Path,args)
def digest(b):return hashlib.sha256(b).hexdigest()
def snapshot(path):
 original_hash=digest(path.read_bytes());bpy.ops.wm.open_mainfile(filepath=str(path.resolve()),load_ui=False,use_scripts=False)
 col=bpy.data.collections['EXPORT'];parts=[]
 for o in sorted(col.all_objects,key=lambda o:o.name):
  p={'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,'matrix_world':[list(r) for r in o.matrix_world],'modifiers':[m.type for m in o.modifiers]}
  if o.type=='MESH':
   m=o.data;m.update();p.update(vertices=[list(v.co) for v in m.vertices],vertex_normals=[list(v.normal) for v in m.vertices],edges=[list(e.vertices) for e in m.edges],polygons=[{'vertices':list(f.vertices),'smooth':f.use_smooth,'normal':list(f.normal),'material_index':f.material_index} for f in m.polygons],corner_normals=[list(n.vector) for n in m.corner_normals])
  parts.append(p)
 assert digest(path.read_bytes())==original_hash
 payload={'unit_scale':bpy.context.scene.unit_settings.scale_length,'parts':parts}
 return {'source_sha256':original_hash,'mesh_transforms_topology_normals_digest':digest(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()),'source_saved':False,'parts':len(parts),'mesh_vertices':sum(len(p.get('vertices',[])) for p in parts),'mesh_faces':sum(len(p.get('polygons',[])) for p in parts)}
a=snapshot(baseline);b=snapshot(revision);ok=a['mesh_transforms_topology_normals_digest']==b['mesh_transforms_topology_normals_digest'];report={'check':'source_geometry_normals_identity','status':'pass' if ok else 'fail','blender_version':bpy.app.version_string,'baseline':a,'revision':b,'geometry_normals_topology_transforms_material_assignment_identical':ok};output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert ok
