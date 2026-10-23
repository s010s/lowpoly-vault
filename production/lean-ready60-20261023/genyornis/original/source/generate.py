# SPDX-License-Identifier: MIT
"""Original Genyornis newtoni reconstruction. Blender 4.3.2, deterministic.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output /tmp/genyornis-build
Only this file, params.json and the declared source/deps are needed.
The canonical helper writes an internal build; delivery names are model.blend/model.glb.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
P=json.loads((HERE/'params.json').read_text())
parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
a=parser.parse_args(sys.argv[sys.argv.index('--')+1:]); out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
C=setup_scene('genyornis',P['seed'])
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
M={k:make_material('genyornis-'+k,v,roughness=.87 if k!='eye' else .42) for k,v in P['palette_srgb'].items()}
semantic=[]
def part(name,verts,faces,mat):
    o=mesh_object(name,verts,faces,mat,C); semantic.append(name); return o

def loft_y(name,rings,n,mat):
    # Ring = (y, zcenter, halfwidth, halfheight), closed profile loft.
    v=[]
    for j,(y,z,rx,rz) in enumerate(rings):
        for i in range(n):
            t=2*math.pi*i/n
            v.append((rx*math.cos(t),y,z+rz*math.sin(t)))
    f=[]
    for j in range(len(rings)-1):
        for i in range(n):
            f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    f += [tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+i for i in range(n))]
    return part(name,v,f,mat)

def loft_z(name,rings,n,mat,offset=(0,0,0)):
    v=[]
    for j,(z,y,rx,ry) in enumerate(rings):
        for i in range(n):
            t=2*math.pi*i/n
            v.append((offset[0]+rx*math.cos(t),offset[1]+y+ry*math.sin(t),offset[2]+z))
    f=[]
    for j in range(len(rings)-1):
        for i in range(n): f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    f += [tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+i for i in range(n))]
    return part(name,v,f,mat)

def tube(name,points,radii,mat,n=10):
    v=[]; previous_u=None
    for j,(p,rr) in enumerate(zip(points,radii)):
        p=Vector(p); tangent=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(0,j-1)])
        tangent.normalize(); u=tangent.cross(Vector((0,0,1)))
        if u.length<.001: u=tangent.cross(Vector((0,1,0)))
        u.normalize()
        # Maintain a continuous ring frame through hock direction reversals.
        if previous_u is not None and u.dot(previous_u)<0: u=-u
        previous_u=u.copy(); w=tangent.cross(u).normalized()
        rx,rz=rr if isinstance(rr,tuple) else (rr,rr)
        for i in range(n):
            t=2*math.pi*i/n; v.append(tuple(p+u*math.cos(t)*rx+w*math.sin(t)*rz))
    f=[]
    for j in range(len(points)-1):
        for i in range(n): f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    f += [tuple(range(n-1,-1,-1)),tuple((len(points)-1)*n+i for i in range(n))]
    return part(name,v,f,mat)

def ellipsoid(name,center,scale,mat,n=14,r=7):
    v=[(center[0],center[1],center[2]-scale[2])]
    for j in range(1,r):
        phi=-math.pi/2+math.pi*j/r
        for i in range(n):
            t=2*math.pi*i/n
            v.append((center[0]+scale[0]*math.cos(phi)*math.cos(t),center[1]+scale[1]*math.cos(phi)*math.sin(t),center[2]+scale[2]*math.sin(phi)))
    v.append((center[0],center[1],center[2]+scale[2])); f=[]
    for i in range(n): f.append((0,1+(i+1)%n,1+i))
    for j in range(r-2):
        for i in range(n): f.append((1+j*n+i,1+j*n+(i+1)%n,1+(j+1)*n+(i+1)%n,1+(j+1)*n+i))
    top=len(v)-1; last=1+(r-2)*n
    for i in range(n): f.append((last+i,last+(i+1)%n,top))
    return part(name,v,f,mat)

# Deliberate heavy barrel torso with high rounded back and deep breast.
body=loft_y('body-contoured-feather-mantle',[
(-.59,1.15,.003,.006),(-.57,1.15,.060,.09),(-.51,1.13,.18,.24),(-.39,1.12,.285,.34),(-.20,1.12,.365,.405),
(.02,1.12,.405,.42),(.25,1.13,.40,.405),(.43,1.16,.33,.345),(.57,1.18,.225,.25),(.68,1.18,.10,.13),(.74,1.18,.025,.035)],24,[M['body'],M['under']])
# The lighter belly is a material region on the same closed torso, not a floating shell.
for face in body.data.polygons:
    cen=face.center
    if cen.z<.98 and cen.y<.36: face.material_index=1
# Neck arises within mantle, narrowing into a thick gently swept upper neck.
loft_z('neck-thick-s-curve',[(1.23,-.33,.19,.19),(1.36,-.40,.17,.18),(1.49,-.455,.127,.14),
(1.63,-.455,.095,.112),(1.75,-.435,.078,.092),(1.85,-.425,.072,.078),(1.93,-.44,.067,.061),(1.965,-.453,.043,.036)],18,[M['head']])
# Soft cranium: posterior compression is intentional and is not a generic round duck head.
head=loft_y('head-posterior-cranium',[
(-.548,1.935,.024,.026),(-.522,1.946,.040,.039),(-.494,1.952,.052,.048),(-.461,1.947,.060,.052),(-.431,1.939,.057,.050),(-.410,1.929,.035,.032)],16,M['head'])
# P59521 upper-rostrum nominal span 212.4 x 76.05 x 72.9 mm; keratin contour is inferred.
# Tip is broad and rounded in plan, shallow at its end; dorsal rise is not a hooked raptor beak.
bill_tip=-.7224; bill_base=-.5100
bill=loft_y('bill-upper-broad-rostrum',[
(bill_tip,1.9180,.010,.0045),(-.715,1.919,.021,.006),(-.690,1.926,.0275,.014),
(-.650,1.934,.0325,.023),(-.605,1.944,.0355,.033),(-.560,1.947,.0375,.03645),
(bill_base,1.947,.038025,.03645)],16,M['bill'])
# Mandibular contour sits under the bill with a narrow dark commissure, not an open gape.
loft_y('bill-lower-mandible',[
(-.713,1.907,.009,.003),(-.690,1.901,.022,.009),(-.640,1.898,.029,.014),(-.578,1.901,.034,.017),
(-.518,1.901,.038,.020),(-.469,1.909,.043,.025),(-.431,1.917,.022,.019)],14,M['bill'])
# Low triangular casque: 51.4 mm long and 76.3 mm broad at cranio-rostral base.
casque_v=[(0,-.5614,1.983),( -.03815,-.5100,1.976),(.03815,-.5100,1.976),
(0,-.537,1.993),( -.029,-.510,1.994),(.029,-.510,1.994), (0,-.510,1.999)]
part('casque-low-broad-triangular',casque_v,[(0,1,4,3),(0,3,5,2),(3,4,6),(3,6,5),(1,2,5,6,4),(0,2,1)],M['bill'])
for s,label in [(-1,'left'),(1,'right')]:
    # Eyes are separate editable semantic parts; no anthropomorphic oversized iris.
    ellipsoid('eye-'+label,(s*.052,-.487,1.962),(.0067,.0105,.009),M['eye'],12,6)
    # Inferred subtle naris, flush inset on lateral surface near bill base.
    ellipsoid('nostril-'+label,(s*.0368,-.551,1.955),(.0017,.007,.003),M['eye'],10,5)
    # Two reduced folded wings. Rounded leading shoulder to tapered posterior tip.
    # Explicit shaped contour in Y/Z, convex outer surface, buried inner attachment.
    contour=[(-.16,1.31),(-.04,1.38),(.14,1.36),(.32,1.25),(.40,1.15),(.29,1.11),(.08,1.16),(-.11,1.20)]
    outer_x=[.348,.348,.355,.357,.349,.383,.405,.389]
    inner=[(s*(outer_x[i]-.065),y,z) for i,(y,z) in enumerate(contour)]; outer=[(s*outer_x[i],y,z) for i,(y,z) in enumerate(contour)]
    vv=inner+outer+[(s*.425,.10,1.255)]
    ff=[tuple(range(7,-1,-1))]
    for i in range(8): ff.append((i,(i+1)%8,(i+1)%8+8,i+8)); ff.append((i+8,(i+1)%8+8,16))
    part('wing-reduced-folded-'+label,vv,ff,M['body'])
    # Feathered thigh envelopes merge into torso, below is robust tarsometatarsus.
    dy=-.075 if s<0 else .075
    tube('thigh-feathered-'+label,[(s*.245,.05+dy,.95),(s*.255,-.005+dy,.78),(s*.25,-.025+dy,.61)],[(.13,.15),(.113,.13),(.082,.09)],M['body'],14)
    tube('leg-scaled-'+label,[(s*.25,-.025+dy,.66),(s*.25,.072+dy,.48),(s*.235,.065+dy,.39),(s*.218,.025+dy,.16),(s*.218,.015+dy,.075)],[(.073,.079),(.055,.060),(.045,.049),(.041,.045),(.052,.04)],M['foot'],12)
    # Three toes point forward and fan laterally; no rear digit and no webbed membrane.
    fx=s*.218; fy=.015+dy
    for k,(spread,length) in enumerate([(-.085,.178),(0,.245),(.090,.193)]):
        end=(fx+spread,fy-length,.027)
        start=(fx+spread*.12,fy-.010,.073)
        mid=(fx+spread*.52,fy-length*.55,.037)
        tube('toe-'+label+'-'+str(k+1),[start,mid,end],[(.030,.027),(.025,.023),(.021,.019)],M['foot'],10)
        # Blunt nail ends: no hook, no sharp raptor talon, flat ground contact.
        dx=spread*.17; ddy=-.042
        tip=(end[0]+dx,end[1]+ddy,.020)
        tube('hoof-claw-'+label+'-'+str(k+1),[(end[0]-.004*(k-1),end[1]+.006,.028),tip],[(.022,.020),(.015,.013)],M['bill'],10)
# Small rear feather tail, not a long ostrich or show-bird fan.
tube('tail-short-feather-tip',[(0,.55,1.21),(0,.72,1.20),(0,.84,1.16)],[(.16,.14),(.10,.09),(.035,.035)],M['body'],12)
# Root stays identity at the footprint center. Apply one global vertical grounding offset to mesh data.
min_z=min(v.co.z for ob in C.objects if ob.type=='MESH' for v in ob.data.vertices)
for ob in C.objects:
    if ob.type=='MESH':
        for v in ob.data.vertices: v.co.z-=min_z
bpy.context.view_layer.update()
metadata={'generator':'source/generate.py','reconstruction':'whole-organism living reconstruction; soft tissues and colors inferred',
 'description':{'en':'Original robust flightless Genyornis reconstruction with low broad casque, reduced wings and three blunt-clawed toes.','zh':'完整健壮的不飞鸟复原，保留低宽盔、退化小翼与三前趾钝爪。'},
 'scale_note':P['note'],'original_inventory_ordinal':689,'semantic_parts':semantic,'surface_profile':'palette-only, closed faceted semantic parts'}
b=P['budgets']
rec=export_asset('genyornis',{'en':'Genyornis newtoni','zh':'牛顿巨鸟'},'birds',C,metadata=metadata,output_root=out/'private'/'build-output',render=False,max_triangles=b['max_triangles'],max_materials=b['max_materials'],max_primitives=b['max_primitives'])
stage=out/'private'/'build-output'/'genyornis'
for src,dst in [('genyornis.glb','model.glb'),('genyornis.blend','model.blend')]: shutil.copy2(stage/src,out/dst)
qa=json.loads((stage/'qa.json').read_text()); qa['glb']['file']='model.glb'; qa['delivery_names']={'glb':'model.glb','blend':'model.blend'}
qa['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(); qa['parameters_sha256']=hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()
if (out/'model.glb').stat().st_size>b['max_glb_bytes']: raise RuntimeError('GLB exceeds frozen byte budget')
(out/'qa'/'evidence').mkdir(parents=True,exist_ok=True)
(out/'qa'/'evidence'/'technical.json').write_text(json.dumps(qa,indent=2)+'\n')
rec['glb']='model.glb';rec['blend']='model.blend';rec['preview']='preview.png';rec['mesh_parts']=semantic
(out/'qa'/'evidence'/'build-metadata.json').write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'BUILT','triangles':qa['glb']['scene_triangles'],'glb_sha256':qa['glb']['sha256'],'output':str(out)}))
