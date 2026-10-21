"""Read-only before/after source material settings, including actual shader nodes."""
import bpy,json,sys,pathlib,hashlib,os
W=pathlib.Path(__file__).resolve().parents[3];B=W/'production/small-life-batch99';O=pathlib.Path('/workspace/shared/lowpoly-batch99-20261021/production/small-life-batch99')
def value(v):
 if isinstance(v,(str,int,float,bool)) or v is None:return v
 try:return list(v)
 except TypeError:return str(v)
def read(p):
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
 result={}
 for m in bpy.data.materials:
  result[m.name]={'diffuse_color':list(m.diffuse_color),'roughness':m.roughness,'metallic':m.metallic,'use_nodes':m.use_nodes,'use_backface_culling':m.use_backface_culling,'surface_render_method':m.surface_render_method,'nodes':[{'name':n.name,'type':n.bl_idname,'inputs':{s.identifier:value(s.default_value) for s in n.inputs if hasattr(s,'default_value')}} for n in m.node_tree.nodes] if m.use_nodes else [],'links':sorted((l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in m.node_tree.links) if m.use_nodes else []}
 return result
for a,old,new in [('monetianthus','r001','r002'),('proterocladus','r002','r003')]:
 p=O/a/old/'artifacts'/(a+'.blend');q=B/a/new/'artifacts'/(a+'.blend');before=read(p);after=read(q);r={'asset_id':a,'pid':os.getpid(),'source_mutated':False,'before_source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'after_source_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'all_source_materials_exact':before==after,'before_materials':before,'after_materials':after};(B/a/new/'qa/source-material-differential.report.json').write_text(json.dumps(r,indent=2)+'\n');assert before==after;print(a,'all source shader nodes/material settings identical')
