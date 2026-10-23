# SPDX-License-Identifier: MIT
"""Reopen-source structural and anatomical-attachment evidence, not visual review."""
import bpy, sys, argparse, json, hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser(); p.add_argument('--root',required=True); a=p.parse_args(sys.argv[sys.argv.index('--')+1:]); R=Path(a.root)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(R/'model.blend'))
C=bpy.data.collections['EXPORT']; body=bpy.data.objects['Body_neck_toothless_snout_and_compressed_tail']
assert all(o.type in ['MESH','EMPTY'] for o in bpy.context.scene.objects)
assert not bpy.data.images or all(i.source=='GENERATED' for i in bpy.data.images)
assert all(o.name in C.all_objects for o in bpy.context.scene.objects)
checks=[]
for obj in C.all_objects:
    if obj.type!='MESH':continue
    mesh=obj.data; mesh.calc_loop_triangles(); parent=list(range(len(mesh.vertices)))
    def root(i):
        while parent[i]!=i: parent[i]=parent[parent[i]]; i=parent[i]
        return i
    for e in mesh.edges:
        a,b=e.vertices; parent[root(a)]=root(b)
    components={}
    for tri in mesh.loop_triangles:
        a,b,c=[mesh.vertices[i].co for i in tri.vertices]
        k=root(tri.vertices[0]); components[k]=components.get(k,0.)+a.dot(b.cross(c))/6
    assert all(x>0 for x in components.values()),(obj.name,components)
    checks.append({'name':obj.name,'connected_shells':len(components),'signed_volume_m3':list(components.values()),'all_component_winding_outward':True})
mesh=body.data; mesh.calc_loop_triangles(); bvh=BVHTree.FromPolygons([v.co for v in mesh.vertices],[t.vertices for t in mesh.loop_triangles],all_triangles=True)
def inside(point):
    # Ray parity in a non-axis-aligned direction avoids regular loft edges.
    o=Vector(point); d=Vector((.932,.171,.319)).normalized(); hits=0
    for _ in range(500):
        pos,n,idx,dist=bvh.ray_cast(o,d,5)
        if pos is None: break
        hits+=1; o=pos+d*1e-7
    return hits%2==1
p=json.loads((R/'source/params.json').read_text()); sections=p['body_sections']
def dh(y):
    for a,b in zip(sections,sections[1:]):
        if a[0]<=y<=b[0]:
            t=(y-a[0])/(b[0]-a[0]); return (a[2]+a[3])*(1-t)+(b[2]+b[3])*t
samples=[]
for sign in [-1,1]:
    samples.extend([{'part':'fore paddle','point':[sign*.040,-.185,-.022]},{'part':'hind paddle','point':[sign*.028,.095,-.020]},{'part':'eye socket','point':[sign*.0195,-.365,.025]}])
for i in range(p['armor_count']):
    y=-.228+i*.018; samples.append({'part':'ossicle '+str(i),'point':[0,y,dh(y)-.002]})
for s in samples:s['inside_body_shell']=inside(s['point'])
assert all(s['inside_body_shell'] for s in samples),samples
q={'status':'PASS','scope':'Reopened editable-source integrity, component signed winding and representative body attachment point ray-parity checks; not printable union or all intersections audit','blend_sha256':sha(R/'model.blend'),'glb_sha256':sha(R/'model.glb'),'source_scene_has_no_camera_light_or_preview_objects':True,'all_export_object_transforms_positive':all(o.matrix_world.to_3x3().determinant()>0 for o in C.all_objects),'closed_component_winding':checks,'body_attachment_samples':samples}
(R/'qa/evidence/source-integrity.json').write_text(json.dumps(q,indent=2)+'\n');print('SOURCE_INTEGRITY_PASS',len(samples),'attachment samples')
