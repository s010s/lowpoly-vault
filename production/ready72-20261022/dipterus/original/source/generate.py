#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic whole-animal Dipterus, meters, anterior -Y.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Only relative source/deps and params.json are used. No network, textures or other model directories.
"""
import argparse, hashlib, json, math, os, shutil, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, export_asset
P=json.loads((HERE/'params.json').read_text())
parser=argparse.ArgumentParser(); parser.add_argument('--out',required=True); parser.add_argument('--gray',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
OUT=Path(args.out).resolve(); OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('dipterus',seed=P['seed'])
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
colors=P['palette']
M=[make_material(n, '#959595' if args.gray else c,roughness=.82 if i!=4 else .5) for i,(n,c) in enumerate(colors.items())]

def obj(name,vs,fs,mids=None,materials=None):
    o=mesh_object(name,vs,fs,materials or M,C)
    if mids is not None:
        for p,mi in zip(o.data.polygons,mids): p.material_index=mi
    o['anatomical_part']=name
    return o

def loft(name,profiles,n=20,default_mat=None):
    vs=[]; fs=[]; mids=[]
    for y,w,lo,hi in profiles:
        for j in range(n):
            a=2*math.pi*j/n; vs.append((w*math.sin(a),y,(lo+hi)/2+(hi-lo)/2*math.cos(a)))
    for k in range(len(profiles)-1):
        for j in range(n):
            fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
            co=math.cos(2*math.pi*(j+.5)/n)
            mids.append(default_mat if default_mat is not None else 0 if co>.42 else 2 if co<-.44 else 1)
    for k in [0,len(profiles)-1]:
        y,w,lo,hi=profiles[k]; q=len(vs); vs.append((0,y,(lo+hi)/2))
        for j in range(n): fs.append((q,k*n+j,k*n+(j+1)%n)); mids.append(default_mat if default_mat is not None else 1)
    return obj(name,vs,fs,mids)

bodyprof=[(-.069,.0155,-.017,.024),(-.057,.0175,-.021,.026),(-.041,.0175,-.021,.025),(-.023,.0163,-.020,.024),(-.004,.0147,-.018,.022),(.014,.0122,-.015,.019),(.030,.0096,-.012,.016),(.045,.0075,-.009,.013),(.059,.0053,-.0065,.0095),(.072,.0031,-.004,.0067),(.085,.0012,-.0015,.004)]
loft('Robust_trunk_to_caudal_peduncle',bodyprof)
loft('Broad_blunt_upper_skull',[(-.100,.0065,-.001,.011),(-.097,.0108,-.0017,.016),(-.090,.0141,-.0030,.022),(-.080,.0161,-.0058,.025),(-.069,.0162,-.009,.025),(-.060,.0165,-.014,.025)],20)
loft('Lower_jaw_and_throat',[(-.100,.0063,-.009,-.0052),(-.096,.0100,-.011,-.0058),(-.088,.0131,-.014,-.0067),(-.077,.0147,-.017,-.0072),(-.065,.0158,-.019,-.006),(-.057,.0162,-.019,-.009)],20,2)
# Dark curved backing behind the true mouth aperture, not a painted mouth seam.
loft('Mouth_interior',[(-.078,.0120,-.0075,-.0055),(-.073,.0135,-.009,-.0070),(-.068,.0145,-.013,-.008)],16,4)

# Solid lenticular fin. Each surface fan carries longitudinal structural facets.
def fin(name,outline,normal,thickness=.0008):
    normal=Vector(normal).normalized(); pts=[Vector(p) for p in outline]; center=sum(pts,Vector())/len(pts)
    vs=[tuple(p+normal*.00012) for p in pts]+[tuple(p-normal*.00012) for p in pts]+[tuple(center+normal*thickness),tuple(center-normal*thickness)]
    n=len(pts); fs=[]; mids=[]
    for i in range(n):
        j=(i+1)%n
        fs.extend([(2*n,i,j),(2*n+1,n+j,n+i),(i,n+i,n+j,j)])
        mids.extend([3 if i%3 else 1,3 if i%3 else 1,3])
    ob=obj(name,vs,fs,mids); ob['fin_thickness_m']=2*thickness; return ob

fins={
'Dorsal_1_separate_smaller':([(0,.008,.017),(0,.017,.026),(0,.027,.029),(0,.034,.028),(0,.040,.025),(0,.036,.019),(0,.026,.015)],(1,0,0)),
'Dorsal_2_separate_larger':([(0,.046,.011),(0,.053,.025),(0,.062,.031),(0,.071,.0315),(0,.081,.028),(0,.077,.020),(0,.072,.008),(0,.061,.007)],(1,0,0)),
'Anal_pointed_leaf':([(0,.047,-.007),(0,.057,-.017),(0,.068,-.022),(0,.079,-.021),(0,.074,-.013),(0,.064,-.004)],(1,0,0)),
'Caudal_asymmetric_unforked':([(0,.078,.003),(0,.085,.008),(0,.097,.014),(0,.100,.012),(0,.097,.004),(0,.095,-.009),(0,.088,-.013),(0,.083,-.008),(0,.078,-.003)],(1,0,0))}
for name,(outline,normal) in fins.items(): fin(name,outline,normal)
for side,sign in [('R',1),('L',-1)]:
    fin('Pectoral_'+side+'_fleshy_leaf',[(sign*.013,-.061,-.009),(sign*.021,-.054,-.015),(sign*.029,-.038,-.024),(sign*.031,-.023,-.027),(sign*.022,-.031,-.024),(sign*.014,-.047,-.015)],(sign*.30,-.1,.95),.0015)
    fin('Pelvic_'+side+'_fleshy_leaf',[(sign*.007,.015,-.010),(sign*.014,.023,-.014),(sign*.020,.040,-.021),(sign*.019,.047,-.022),(sign*.011,.039,-.019),(sign*.006,.025,-.011)],(sign*.35,-.1,.94),.0010)

# Detail builders aggregate small structures into semantic meshes, not thousands of draw calls.
class Builder:
    def __init__(self): self.v=[]; self.f=[]; self.m=[]
    def add(self,vs,fs,mat):
        off=len(self.v); self.v.extend(vs); self.f.extend(tuple(off+i for i in f) for f in fs); self.m.extend([mat]*len(fs))
    def emit(self,name): return obj(name,self.v,self.f,self.m)

def tube(B,points,radii,mat,n=6):
    points=[Vector(p) for p in points]; vs=[]; fs=[]
    for k,(p,r) in enumerate(zip(points,radii)):
        tangent=(points[min(k+1,len(points)-1)]-points[max(0,k-1)]).normalized()
        u=tangent.cross(Vector((0,0,1)))
        if u.length<.01: u=tangent.cross(Vector((0,1,0)))
        u.normalize(); v=tangent.cross(u).normalized()
        vs.extend(tuple(p+r*(u*math.cos(j*2*math.pi/n)+v*math.sin(j*2*math.pi/n))) for j in range(n))
    for k in range(len(points)-1):
        for j in range(n): fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    fs.extend([tuple(range(n-1,-1,-1)),tuple((len(points)-1)*n+j for j in range(n))]); B.add(vs,fs,mat)

# Very low rays reinforce fan growth and never form spikes at the perimeter.
rays=Builder()
for name,(out,normal) in fins.items():
    root=Vector(out[0]); no=Vector(normal)
    for edge in out[1:-2]:
        target=Vector(edge); a=root.lerp(target,.17); b=root.lerp(target,.91)
        for sign in [-1,1]: tube(rays,[a+no*sign*.00055,b+no*sign*.00025],[.00018,.00009],2,5)
rays.emit('Median_fin_radial_ribs')
# Bilateral opercular boundary as restrained dark seams, plus eye sockets and small eyes.
seams=Builder(); eyes=Builder(); rims=Builder()
for s in [-1,1]:
    tube(seams,[(s*.006,-.067,.022),(s*.0125,-.063,.014),(s*.017,-.061,.002),(s*.015,-.061,-.010),(s*.010,-.066,-.017)],[.00033]*5,0,5)
    # Ellipsoid geometry is transformed in vertices, leaving positive identity transforms.
    def ellipsoid(B,center,radii,mat,n=12,lat=6):
        vs=[(center[0],center[1],center[2]+radii[2])]; fs=[]
        for k in range(1,lat):
            a=math.pi*k/lat
            for j in range(n):
                b=2*math.pi*j/n; vs.append((center[0]+radii[0]*math.sin(a)*math.cos(b),center[1]+radii[1]*math.sin(a)*math.sin(b),center[2]+radii[2]*math.cos(a)))
        bot=len(vs); vs.append((center[0],center[1],center[2]-radii[2]))
        for j in range(n): fs.append((0,1+j,1+(j+1)%n)); fs.append((bot,1+(lat-2)*n+(j+1)%n,1+(lat-2)*n+j))
        for k in range(lat-2):
            for j in range(n): a=1+k*n+j; b=1+k*n+(j+1)%n; fs.append((a,b,b+n,a+n))
        B.add(vs,fs,mat)
    ellipsoid(rims,(s*.0130,-.087,.010),(.0028,.0033,.0034),2)
    ellipsoid(eyes,(s*.0147,-.087,.0105),(.0018,.0023,.0023),4)
seams.emit('Paired_opercular_boundaries'); rims.emit('Eye_socket_rims'); eyes.emit('Small_lateral_eyes')

# Paired lower and opposed upper tooth plates. Sloping low ridges, not teeth cones.
plates=Builder(); ridges=Builder()
for s in [-1,1]:
    for upper in [False,True]:
        direction=1 if not upper else -1
        def z_at(y):
            t=max(0,min(1,(y+.098)/.023))
            return (-.0052-.0018*t) if not upper else (-.0012-.0052*t)
        raw=[(s*.0012,-.098),(s*.0070,-.0955),(s*.0100,-.085),(s*.0044,-.0765)]
        polygon=[(x,y,z_at(y)) for x,y in raw]
        vv=polygon+[(x,y,z-.0007*direction) for x,y,z in polygon]
        ff=[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
        plates.add(vv,ff,5)
        pivot=Vector((s*.0041,-.078,z_at(-.078)))
        endpoints=[(s*.0019,-.097),(s*.0036,-.0964),(s*.0054,-.0957),(s*.0071,-.0938),(s*.0087,-.0892)]
        for i,(x,y) in enumerate(endpoints):
            tip=Vector((x,y,z_at(y))); tangent=(tip-pivot).normalized(); lateral=Vector((-tangent.y,tangent.x,0))*.00030
            q0=pivot.lerp(tip,.15); q1=pivot.lerp(tip,.94); crest=(q0+q1)*.5+Vector((0,0,.00065*direction))
            base=[tuple(q0+lateral),tuple(q1+lateral),tuple(q1-lateral),tuple(q0-lateral),tuple(crest)]
            ridges.add(base,[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(3,2,1,0)],5)
plates.emit('Paired_upper_and_lower_tooth_plates'); ridges.emit('Low_radiating_tooth_plate_ridges')

# Slightly raised closed scale shields follow the true body loft, not reference imagery.
if not args.gray:
    scales=Builder()
    def profile(y):
        for a,b in zip(bodyprof,bodyprof[1:]):
            if a[0]<=y<=b[0]:
                t=(y-a[0])/(b[0]-a[0]); return [a[i]*(1-t)+b[i]*t for i in range(1,4)]
        return bodyprof[-1][1:]
    def surface(y,a,raise_m=0):
        w,lo,hi=profile(y); return Vector(((w+raise_m)*math.sin(a),y,(lo+hi)/2+((hi-lo)/2+raise_m)*math.cos(a)))
    for row in range(19):
        y=-.051+row*.0059
        for j in range(14):
            a=(j+.5*(row%2))*2*math.pi/14
            # Flat-rhomboid scale shell, subtly faceted, from y >= gill boundary.
            ring=[surface(y-.0024,a),surface(y,a+.18),surface(y+.0024,a),surface(y,a-.18)]
            top=surface(y,a,.00033)
            bot=surface(y,a,-.00020)
            vs=[tuple(p) for p in ring]+[tuple(top),tuple(bot)]
            fs=[(4,k,(k+1)%4) for k in range(4)]+[(5,(k+1)%4,k) for k in range(4)]
            co=math.cos(a); mi=0 if co>.45 else 2 if co<-.45 else 1
            scales.add(vs,fs,mi)
    scales.emit('Subordinate_rhomboid_scale_field')

# Export using the pinned common pipeline. No source rendering or external mutation.
record=export_asset('dipterus',{'en':'Dipterus','zh':'双翼鱼'},'animals',C,metadata={
    'generator':'source/generate.py','revision':P['revision'],
    'description':{'en':'Whole living Dipterus reconstruction with two discrete dorsal fins and low radiating tooth plates.','zh':'双翼鱼全身活体重建，保留两个分离背鳍及低矮放射状齿板。'},
    'reconstruction_notes':['Approximate 0.20 m specimen-informed length, not species maximum.','Soft tissue thickness, lips and slate-olive palette are artistic inferences.','Mounting origin is body-center; swimming animal, no ground or stand.'],
    'sources':['https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0272246','https://orkneylandscapes.org/orkney/dipterus-valenciennesi/']
},output_root=OUT/'_build',render=False,max_triangles=P['geometry_policy']['max_triangles'],max_materials=P['geometry_policy']['max_materials'],max_primitives=P['geometry_policy']['max_primitives'])
BUILD=OUT/'_build'/'dipterus'
for source,target in [('dipterus.glb','model.glb'),('dipterus.blend','model.blend'),('qa.json','technical.json'),('metadata.json','build-metadata.json')]: shutil.copy2(BUILD/source,OUT/target)
if (OUT/'model.glb').stat().st_size>P['geometry_policy']['max_glb_bytes']: raise RuntimeError('GLB bytes budget exceeded')
print('GENERATED',str(OUT/'model.glb'))
