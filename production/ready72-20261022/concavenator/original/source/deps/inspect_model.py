# SPDX-License-Identifier: MIT
"""Cheap source topology, contact and semantic-part checks; not visual acceptance.
blender -b model.blend -t 2 --python inspect_model.py -- report.json
"""
import bpy, json, sys, hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
report=Path(sys.argv[sys.argv.index('--')+1])
col=bpy.data.collections['EXPORT']; root=bpy.data.objects[col['asset_root']]
parts=[]; toe_minima={}; groups=[]; errors=[]; group_geometry={}
for o in col.objects:
    if o.type!='MESH': continue
    mesh=o.data;mesh.calc_loop_triangles();adj=[set() for v in mesh.vertices]
    for e in mesh.edges:
        a,b=e.vertices;adj[a].add(b);adj[b].add(a)
    seen=set();components=[]
    for v in range(len(mesh.vertices)):
        if v in seen:continue
        component=set();todo=[v]
        while todo:
            n=todo.pop()
            if n in component:continue
            component.add(n);todo.extend(adj[n]-component)
        seen.update(component)
        signed=sum(mesh.vertices[t.vertices[0]].co.dot(mesh.vertices[t.vertices[1]].co.cross(mesh.vertices[t.vertices[2]].co))/6 for t in mesh.loop_triangles if t.vertices[0] in component)
        components.append({'vertices':len(component),'signed_volume_m3':signed})
        if signed<=0:errors.append(o.name+': nonpositive closed component volume')
    for group in o.vertex_groups:
        ids=[v.index for v in mesh.vertices if any(g.group==group.index for g in v.groups)]
        idx=set(ids)
        group_geometry[group.name]=(o,ids,[tuple(t.vertices) for t in mesh.loop_triangles if set(t.vertices)<=idx])
        if '-pedal-' in group.name and '-claw' not in group.name:
            toe_minima[group.name]=min(mesh.vertices[i].co.z for i in ids)
        groups.append(group.name)
    parts.append({'object':o.name,'components':components})
if len(toe_minima)!=6 or any(abs(z)>.002 for z in toe_minima.values()):errors.append('Six fleshy pedal pads must each reach ground within 2mm')
for side in ('left','right'):
    for digit in (1,2,3):
        if f'{side}-manual-{digit}' not in groups:errors.append('Missing manual digit')
if any(o.type in {'CAMERA','LIGHT'} for o in bpy.data.objects):errors.append('Presentation objects leaked into editable model')
if any(abs(root.matrix_world[i][j]-(1 if i==j else 0))>1e-7 for i in range(4) for j in range(4)):errors.append('Nonidentity root')
def inside_group(point,name):
    ob,ids,faces=group_geometry[name]
    bvh=BVHTree.FromPolygons([v.co for v in ob.data.vertices],faces,all_triangles=True)
    direction=Vector((1,.173,.091)).normalized();origin=point.copy();hits=0
    for _ in range(40):
        hit,normal,index,distance=bvh.ray_cast(origin,direction,100)
        if hit is None:break
        hits+=1;origin=hit+direction*.000001
    return hits%2==1
attachments=[]
for side in ('left','right'):
    for kind,parent,n in [('pedal',side+'-hip-to-metatarsus',8),('manual',side+'-shoulder-elbow-wrist',7)]:
        for digit in (1,2,3):
            name=f'{side}-{kind}-{digit}';ob,ids,_=group_geometry[name]
            point=sum((ob.data.vertices[i].co for i in ids[:n]),Vector())/n
            attached=inside_group(point,parent)
            attachments.append({'child':name,'parent':parent,'root_center_inside_parent':attached})
            if not attached:errors.append(name+': root center not inside parent; inspect connection')
record={'status':'PASS' if not errors else 'FAIL','errors':errors,'source_blend_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'parts':parts,'pedal_pad_minimum_z_m':toe_minima,'manual_digits_per_side':3,'digit_root_attachment_ray_tests':attachments,'root_identity':True,'source_presentation_objects':False,'limits':'Closed-component signed volumes and attachment ray tests do not establish anatomical fidelity, absence of all self-intersections, or a single printable union. Limb roots, claws and facial details deliberately overlap at attachment interfaces.'}
report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':record['status'],'errors':errors,'pedal_pad_minimum_z_m':toe_minima}))
if errors:raise RuntimeError(errors)
