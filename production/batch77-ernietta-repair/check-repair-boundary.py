# SPDX-License-Identifier: MIT
"""Read-only old/new Blender shape comparison; no visual/factual approval."""
import bpy,sys,json,hashlib,datetime
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:];old,new,out=map(Path,args);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={str(p):H(p) for p in [old,new]}
def read(p):
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
 objects=[o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH'];assert len(objects)==1
 o=objects[0];return {'vertices':[tuple(v.co) for v in o.data.vertices],'translation':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale),'materials':[{'name':m.name,'double_sided':not m.use_backface_culling,'rgba':list(m.diffuse_color),'roughness':m.roughness,'metallic':m.metallic} for m in o.data.materials]}
a=read(old);b=read(new);upper=range(4*180,14*180);same=all(a['vertices'][i]==b['vertices'][i] for i in upper);assert same;assert a['vertices'][-1]==b['vertices'][-1];assert a['materials']==b['materials'];assert a['rotation']==b['rotation'] and a['scale']==b['scale'];assert all(H(Path(p))==h for p,h in before.items())
d={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_source_sha256':H(old),'repaired_source_sha256':H(new),'original_source_path':str(old),'repaired_source_path':str(new),'original_authored_vertices':len(a['vertices']),'repaired_authored_vertices':len(b['vertices']),'unchanged_authored_vertex_indices':[4*180,14*180-1],'unchanged_upper_wall_rim_inner_cavity_vertices':1800,'unchanged_cavity_floor_center':True,'materials_identical':True,'no_rotation_or_scale_change':True,'original_grounding_translation':a['translation'],'repaired_grounding_translation':b['translation'],'source_files_unchanged':True,'note':'Comparison in authored mesh coordinates. Only bottom4 radial levels plus new basal joining strip changed. Grounding translation adjusts to new physical minimum; no pose/rotation/scale trick. This is a shape-boundary and material audit, not independent scientific/visual acceptance.'};out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
