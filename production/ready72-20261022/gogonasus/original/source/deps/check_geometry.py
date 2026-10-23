# SPDX-License-Identifier: MIT
"""Hash-bound semantic geometry diagnostics; not independent visual/scientific QA."""
import bpy,bmesh,sys,json,math,hashlib,argparse
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('blend',type=Path);p.add_argument('--glb',type=Path,required=True);p.add_argument('--build-report',type=Path,required=True);p.add_argument('--params',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(a.blend));r=json.loads(a.build_report.read_text());P=json.loads(a.params.read_text());shift=r['ground_shift_m']
PROF=P['cranial_profile_mm']
def top_at(x,y):
    for aa,bb in zip(PROF,PROF[1:]):
        if y<=bb[0]:
            t=max(0,min(1,(y-aa[0])/(bb[0]-aa[0])));w,z,h=[aa[i]*(1-t)+bb[i]*t for i in (1,2,3)];return z+h*math.sqrt(max(0,1-(x/w)**2))
parts=[]
for o in bpy.data.collections['EXPORT'].all_objects:
    if o.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(o.data)
    pending=set(bm.verts);components=0
    while pending:
        components+=1;todo=[pending.pop()]
        while todo:
            v=todo.pop()
            for e in v.link_edges:
                w=e.other_vert(v)
                if w in pending:pending.remove(w);todo.append(w)
    parts.append({'name':o.name,'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'connected_components':components});bm.free()
print('PART_METRICS',json.dumps(parts),flush=True)
assert all(x['nonmanifold_edges']==0 and x['signed_volume_m3']>0 for x in parts)
assert next(x for x in parts if x['name'].startswith('Continuous mandibular'))['connected_components']==1
skull=bpy.data.objects['Dermal cranial vault and cheeks'];holes=[]
for kind in ('orbit','spiracle'):
    q=P[kind]
    for side in (-1,1):
        n=Vector((side*.80,0,.60) if kind=='orbit' else (side*.62,0,.785)).normalized()
        c=Vector((side*q['center_x_abs_mm']*.001,q['center_y_mm']*.001,top_at(q['center_x_abs_mm'],q['center_y_mm'])*.001+shift))
        u=Vector((0,1,0));v=n.cross(u);rx,ry=q['radius_xy_mm']
        tests=[]
        for label,offset in [('center',Vector()),('near_front_rim',-u*(ry+1.2)*.001),('near_rear_rim',u*(ry+1.2)*.001),('near_medial_rim',v*(rx+1.2)*.001)]:
            hit,loc,normal,face=skull.ray_cast(c+offset+n*.006,-n,distance=.012)
            tests.append({'sample':label,'hit_cranial_bone':bool(hit),'ray_origin_blender_m':list(c+offset+n*.006),'direction':list(-n),'distance_m':.012})
        assert not tests[0]['hit_cranial_bone'],(kind,side,tests)
        assert sum(t['hit_cranial_bone'] for t in tests[1:])>=2,(kind,side,tests)
        holes.append({'kind':kind,'side':side,'center_blender_m':list(c),'tests':tests,'status':'PASS real center opening with adjacent bone hits'})
bridge_hit=bpy.data.objects['Premaxillary anterior symphysis'].ray_cast(Vector((0,-.040,.014+shift)),Vector((0,1,0)),distance=.025)[0]
assert bridge_hit, 'Anterior symphysis must close the false median opening'
assert all(m.use_backface_culling for m in bpy.data.materials if m.users)
report={'status':'PASS','claim_scope':'Maker geometric diagnostics only: closed individual solids, positive signed volumes, continuous one-component lower jaw, actual ray-open bilateral orbit and spiracle centers with adjacent bone hits. No printable union or factual accuracy claim.','glb_sha256':sha(a.glb),'blend_sha256':sha(a.blend),'parts':parts,'apertures':holes,'anterior_bridge':{'median_front_ray_hits_bone':bool(bridge_hit),'origin_blender_m':[0,-.040,.014+shift],'direction':[0,1,0]},'materials':{'all_used_opaque':all(m.diffuse_color[3]==1 for m in bpy.data.materials if m.users),'all_used_backface_culling':True},'stated_overlap_policy':'Cheek plates and downfolded laminae intentionally meet or overlap cranial shell; fine teeth enter jaw margin. No boolean union claimed.','code_sha256':sha(Path(__file__))}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print('GOGONASUS_GEOMETRY_PASS')
