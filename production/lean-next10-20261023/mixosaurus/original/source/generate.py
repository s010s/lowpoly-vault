#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic Mixosaurus cornalianus r001; Blender 4.3.2.
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Only bundled deps and params are read. No reference imagery is embedded.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, ground_asset, export_asset

P=json.loads((HERE/'params.json').read_text())
args=argparse.ArgumentParser(); args.add_argument('--out',type=Path,default=HERE.parent)
A=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=A.out.resolve(); OUT.mkdir(parents=True,exist_ok=True); (OUT/'qa/evidence').mkdir(parents=True,exist_ok=True)
C=setup_scene('mixosaurus',P['seed']); bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
root=bpy.data.objects[C['asset_root']]; root['authoring_forward']='+X'; root['glTF_forward']='+X'; root['reconstruction']='Mixosaurus cornalianus; BES SC 1000 primarily; life volume and colour inferred'
M={k:make_material(k,v,roughness=.78 if k!='eye' else .48) for k,v in P['palette'].items()}
# Axial loft tuples: x, centre z, half width y, half depth z. Exact end tips define nominal total length.
R=P['body_stations']; N=P['body_sides']
v=[]; f=[]; mi=[]
for x,z,wy,hz in R:
    for j in range(N):
        t=2*math.pi*j/N; v.append((x,wy*math.cos(t),z+hz*math.sin(t)))
for i in range(len(R)-1):
    for j in range(N):
        f.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
        mi.append(1 if math.sin((j+.5)*2*math.pi/N)<-.40 else 0)
f.append(tuple(reversed(range(N)))); mi.append(0)
f.append(tuple((len(R)-1)*N+j for j in range(N))); mi.append(0)
body=mesh_object('continuous_head_trunk_bent_tail',v,f,[M['skin'],M['ventral']],C)
for p,m in zip(body.data.polygons,mi): p.material_index=m
body['anatomy']='Continuous original loft; 190 mm head envelope, long substantial bent tail, not thunniform'
# Paddle lofts use a root-to-tip centreline, chord across x, thickness along local normal.
def paddle(name,stations,side):
    verts=[]; faces=[]; n=10
    for x,y,z,chord,thick in stations:
        for j in range(n):
            t=2*math.pi*j/n; verts.append((x+chord*math.cos(t),side*y,z+thick*math.sin(t)))
    for i in range(len(stations)-1):
        for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces += [tuple(reversed(range(n))),tuple((len(stations)-1)*n+j for j in range(n))]
    obj=mesh_object(name,verts,faces,M['skin'],C); obj['anatomy']='Closed fleshy paddle with root buried in trunk; no free digits'; return obj
for side,label in [(-1,'right'),(1,'left')]:
    paddle('forepaddle_'+label,P['fore_paddle'],side)
    paddle('hindpaddle_'+label,P['hind_paddle'],side)
# Median fin, solid profile. Intermediate ring provides curved lenticular thickness, not a flat billboard.
def median(name,outline,thick):
    cx=sum(x for x,z in outline)/len(outline); cz=sum(z for x,z in outline)/len(outline)
    verts=[(x,0,z) for x,z in outline]; n=len(outline)
    for s in [-1,1]:
        for x,z in outline: verts.append((cx+(x-cx)*.62,s*thick,cz+(z-cz)*.62))
    faces=[]
    for j in range(n):
        k=(j+1)%n; faces.extend([(j,k,n+k,n+j),(j,2*n+j,2*n+k,k)])
    verts += [(cx,-thick*1.08,cz),(cx,thick*1.08,cz)]
    for j in range(n):
        k=(j+1)%n; faces.extend([(3*n,n+j,n+k),(3*n+1,2*n+k,2*n+j)])
    return mesh_object(name,verts,faces,M['skin'],C)
median('small_anterior_dorsal_fin',P['dorsal_outline'],.0032)
median('modest_upper_caudal_lobe',P['upper_caudal_outline'],.0020)
# Slightly proud, modest soft-tissue eyes, not bony-orbit-sized eyeballs.
def ellipsoid(name,c,r,material):
    verts=[(c[0],c[1],c[2]+r[2])]; faces=[]; n=16; nr=6
    for i in range(1,nr):
        lat=math.pi*i/nr
        for j in range(n):
            t=2*math.pi*j/n; verts.append((c[0]+r[0]*math.sin(lat)*math.cos(t),c[1]+r[1]*math.sin(lat)*math.sin(t),c[2]+r[2]*math.cos(lat)))
    bot=len(verts); verts.append((c[0],c[1],c[2]-r[2]))
    for j in range(n): faces.append((0,1+j,1+(j+1)%n))
    for i in range(nr-2):
        for j in range(n): faces.append((1+i*n+j,1+(i+1)*n+j,1+(i+1)*n+(j+1)%n,1+i*n+(j+1)%n))
    for j in range(n): faces.append((bot,1+(nr-2)*n+(j+1)%n,1+(nr-2)*n+j))
    return mesh_object(name,verts,faces,material,C)
bpy.context.view_layer.update()
def surface_y(x,z):
    hit,point,normal,index=body.ray_cast(Vector((x,1.0,z)),Vector((0,-1,0)),distance=2.0)
    if not hit: raise ValueError('Facial mark does not intersect the actual triangulated skin')
    return point.y
def surface_spot(name,x,z,rx,rz,side,mat,bump):
    verts=[];faces=[];n=20
    for depth in [.0005,-.00045]:
        for j in range(n):
            t=2*math.pi*j/n;xx=x+rx*math.cos(t);zz=z+rz*math.sin(t);verts.append((xx,side*(surface_y(xx,zz)+depth),zz))
    verts.extend([(x,side*(surface_y(x,z)+bump),z),(x,side*(surface_y(x,z)-.0007),z)])
    for j in range(n):
        k=(j+1)%n;faces.extend([(2*n,j,k),(2*n+1,n+k,n+j),(j,n+j,n+k,k)])
    return mesh_object(name,verts,faces,mat,C)
for s,label in [(-1,'right'),(1,'left')]:
    surface_spot('eye_'+label,.321,.139,.0115,.0108,s,M['eye'],.0017)
# Closed jaw seam is a narrow mesh ribbon conforming to each lateral jaw; all dark facial marks consolidated per side.
def details(side,label):
    vv=[]; ff=[]
    path=[]
    for a,b in zip(P['mouth_path'],P['mouth_path'][1:]):
        for k in range(5):
            t=k/5;path.append([a[j]*(1-t)+b[j]*t for j in range(3)])
    path.append(P['mouth_path'][-1])
    for x,y,z in path: vv.extend([(x,side*(surface_y(x,z-.0007)+.0003),z-.0007),(x,side*(surface_y(x,z+.0007)+.0003),z+.0007)])
    for i in range(len(path)-1): ff.append((2*i,2*i+1,2*i+3,2*i+2))
    # Duplicate back face offset slightly inward: closed thin strip, not double-sided material.
    n=len(vv); vv += [(x,y-side*.00065,z) for x,y,z in vv]
    for i in range(len(path)-1): ff.append((n+2*i+2,n+2*i+3,n+2*i+1,n+2*i))
    for i in range(len(path)-1):
        ff += [(2*i,n+2*i,n+2*i+2,2*i+2),(2*i+1,2*i+3,n+2*i+3,n+2*i+1)]
    ff += [(0,1,n+1,n),(n-2,2*n-2,2*n-1,n-1)]
    # tiny slit-like nostril near snout base, fully modeled flattened closed ellipsoid merged by data
    obj=mesh_object('jaw_seam_'+label,vv,ff,M['mark'],C)
    nostril=surface_spot('nostril_'+label,.358,.122,.0045,.0013,side,M['mark'],.00035)
    # Join same-side details without modifier or destructive changes to anatomical main parts.
    verts=[tuple(v.co) for v in obj.data.vertices]; faces=[tuple(p.vertices) for p in obj.data.polygons]
    k=len(verts); verts += [tuple(v.co) for v in nostril.data.vertices]; faces += [tuple(k+i for i in p.vertices) for p in nostril.data.polygons]
    bpy.data.objects.remove(obj,do_unlink=True); bpy.data.objects.remove(nostril,do_unlink=True)
    return mesh_object('closed_jaw_and_naris_'+label,verts,faces,M['mark'],C)
for s,l in [(-1,'right'),(1,'left')]: details(s,l)
# Lowest geometry is at Z=0, identity root at swim mounting plane. Preserve exact +X/-X length.
shift=ground_asset(C,center_xy=False)
root['origin_description']='Identity swim mount under axial midpoint; lowest posed geometry Z=0, no support'
record=export_asset('mixosaurus',{'en':'Mixosaurus','zh':'混鱼龙'},'marine-reptiles',C,
    metadata={'generator':'source/generate.py','description':{'en':'Original refined low-poly Mixosaurus cornalianus, constrained by BES SC 1000 preserved fins and skeleton.','zh':'依据 BES SC 1000 化石与鳍软组织约束制作的原创混鱼龙模型。'},'source_basis':'Renesto et al. 2020 doi:10.4202/app.00731.2020; life thickness and palette inferred'},
    output_root=OUT/'private/build',render=False,diagnostics=False,max_triangles=24000,max_materials=6,max_primitives=16)
raw=OUT/'private/build/mixosaurus'
shutil.copy2(raw/'mixosaurus.glb',OUT/'model.glb'); shutil.copy2(raw/'mixosaurus.blend',OUT/'model.blend')
qa=json.loads((raw/'qa.json').read_text()); qa['artifact_sha256']=hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest()
(OUT/'qa/evidence/source-export.json').write_text(json.dumps(qa,indent=2)+'\n')
record.update({'glb':'model.glb','blend':'model.blend','preview':'preview.png','axes':{'blender_up':'+Z','blender_forward':'+X','glb_up':'+Y','glb_forward':'+X'},'origin':root['origin_description'],'ground_shift':shift,'exporter_version':'4.3.47','generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'nominal_total_length_m':.985,'runtime_threejs_version':'0.180.0','runtime_threejs_status':'NOT_RUN'})
(OUT/'qa/evidence/build-metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'BUILT','triangles':record['triangles'],'bytes':record['glb_bytes'],'glb_sha256':record['sha256']['glb']}))
