import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
root=Path('/workspace/scratch/f9208c421601/lowpoly-conifer-final-qa');src=root/'study-r11/conifer-tree.blend'
bpy.ops.wm.open_mainfile(filepath=str(src))
report={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'blender':bpy.app.version_string,'unit_scale':bpy.context.scene.unit_settings.scale_length,'objects':[]}
for o in bpy.context.scene.objects:
 d={'name':o.name,'type':o.type,'matrix_world':[list(v) for v in o.matrix_world],'parent':o.parent.name if o.parent else None,'collections':[c.name for c in o.users_collection]}
 if o.type=='MESH':
  o.data.calc_loop_triangles();d.update(vertices=len(o.data.vertices),triangles=len(o.data.loop_triangles),polygons=len(o.data.polygons),modifiers=[m.type for m in o.modifiers],smooth_polygons=sum(p.use_smooth for p in o.data.polygons),groups=[g.name for g in o.vertex_groups])
 report['objects'].append(d)
 if o.type=='MESH' and 'clustered' in o.name:
  finger_metrics=[]
  for g in o.vertex_groups:
   ids=[vert.index for vert in o.data.vertices if any(x.group==g.index for x in vert.groups)]
   if len(ids)!=48:raise Exception((g.name,len(ids)))
   for finger in range(4):
    verts=[o.data.vertices[i].co.copy() for i in ids[finger*12:(finger+1)*12]]
    centers=[sum(verts[k:k+3],Vector())/3 for k in range(0,12,3)]
    radii=[sum((x-centers[k]).length for x in verts[k*3:k*3+3])/3 for k in range(4)]
    length=sum((centers[k+1]-centers[k]).length for k in range(3));end=(centers[-1]-centers[-2]).length
    finger_metrics.append({'group':g.name,'finger':finger,'path_length_m':length,'cross_section_radii_m':radii,'terminal_segment_length_m':end,'terminal_segment_fraction':end/length,'cap_to_max_radius_ratio':radii[-1]/max(radii),'terminal_approx_half_angle_deg':math.degrees(math.atan((radii[-2]-radii[-1])/end))})
  report['fingers']=finger_metrics
out=root/'independent-source-inspection.json';out.write_text(json.dumps(report,indent=2))
print('WROTE',out)
