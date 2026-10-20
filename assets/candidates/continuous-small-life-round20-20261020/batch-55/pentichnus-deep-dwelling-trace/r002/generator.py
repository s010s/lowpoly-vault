# SPDX-License-Identifier: MIT
# Original batch-55 geometry; no reference meshes or third-party textures.
import bpy,sys,json,math,argparse
from pathlib import Path
from mathutils import Vector
from itertools import combinations
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,ground_asset,export_asset
p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed'])
pi=math.pi

def mat(n,h):return make_material(n,h)

def mesh(n,v,f,m):return mesh_object(n,v,f,m,c)

if slug=='vermicularia':
    mats=[mat('Shell cream','#C5AE85'),mat('Growth shoulder','#B49A72'),mat('Inner shell','#A58A60'),mat('Aperture rim','#DAC69F')]
    # Juvenile logarithmic conispire with a continuous centerline and a free adult tube.
    pts=[];rs=[]
    for i in range(97):
        t=i/96;ang=2*pi*2.4*t;r=.0025+.012*t
        pts.append(Vector((-.061+r*math.cos(ang),r*math.sin(ang),.023+.034*t)))
        rs.append(.00075+.0031*t)
    start=pts[-1]; tangent=(pts[-1]-pts[-2]).normalized()
    # Hermite path segments: maintain a smooth initial tangent and broad irregular adult bends.
    controls=[start,start+tangent*.018,Vector((-.004,.020,.074)),Vector((.037,.005,.036)),Vector((.072,-.028,.030)),Vector((.086,-.047,.058))]
    # Catmull-like cubic Bezier chain chosen for irregular release from the juvenile spire.
    def bez(P0,P1,P2,P3,t):return (1-t)**3*P0+3*(1-t)**2*t*P1+3*(1-t)*t*t*P2+t**3*P3
    b0=[controls[0],controls[1],Vector((-.012,.032,.105)),controls[2]]
    b1=[controls[2],Vector((.012,.010,.030)),Vector((.029,.018,.026)),controls[3]]
    b2=[controls[3],Vector((.062,-.006,.020)),Vector((.080,-.031,.025)),controls[5]]
    for seg,ps in enumerate([b0,b1,b2]):
        for i in range(1,33):
            t=i/32;pts.append(bez(*ps,t));rs.append(.00385+.0097*((seg+t)/3)**.7)
    N=12;v=[]
    # Parallel transport cross section avoids hard twists at bends.
    previous=None
    for j,(P,r) in enumerate(zip(pts,rs)):
        T=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized()
        B=T.cross(Vector((0,0,1))) if previous is None else previous-T*previous.dot(T)
        if B.length<1e-6:B=T.cross(Vector((0,1,0)))
        B.normalize();C=T.cross(B).normalized();previous=B
        for radius in [r,r*.74]:
            for k in range(N):v.append(tuple(P+radius*(math.cos(2*pi*k/N)*B+math.sin(2*pi*k/N)*C)))
    f=[];mi=[]
    for j in range(len(pts)-1):
        for layer in range(2):
            for k in range(N):
                q=j*2*N+layer*N+k;nextk=j*2*N+layer*N+(k+1)%N
                f.append((q,nextk,nextk+2*N,q+2*N));mi.append(2 if layer else 1 if j<96 and j%16<2 else 0)
    for j in [0,len(pts)-1]:
        for k in range(N):f.append((j*2*N+k,j*2*N+(k+1)%N,j*2*N+N+(k+1)%N,j*2*N+N+k));mi.append(3)
    o=mesh('Continuous coiled-to-free hollow shell',v,f,mats)
    for poly,m in zip(o.data.polygons,mi):poly.material_index=m
elif slug=='weichselia':
    mats=[mat('Fossil cortex','#584837'),mat('Attachment shoulders','#736047'),mat('Attachment centers','#958063'),mat('Cut cortex','#8B7353'),mat('Plain cut core','#AA9270')]
    N=48;Z=25;v=[];boss=[(.3,.065,.026),(2.0,.12,.022),(4.2,.07,.025),(5.1,.19,.021),(3.3,.235,.024),(1.2,.255,.018),(5.9,.105,.015),(2.8,.035,.017),(3.7,.16,.014)]
    def rad(th,z):
        base=.063*(1-.14*z/.30)+.002*math.cos(3*th+.5)*(1-z/.35)
        for ang,zz,amp in boss:
            da=(th-ang+pi)%(2*pi)-pi
            base+=amp*math.exp(-((da/.24)**4+((z-zz)/.022)**4))
        return base
    for j in range(Z):
        z=.30*j/(Z-1)
        for k in range(N):
            th=2*pi*k/N;r=rad(th,z);v.append((r*math.cos(th),r*math.sin(th),z))
    f=[];mi=[]
    for j in range(Z-1):
        for k in range(N):
            f.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
            th=2*pi*(k+.5)/N;z=.30*(j+.5)/(Z-1); excess=rad(th,z)-(.063*(1-.14*z/.30)+.002*math.cos(3*th+.5)*(1-z/.35))
            mi.append(2 if excess>.017 else 1 if excess>.007 else 0)
    # Thick cortex on the cut face, no complex guessed stem anatomy or wood rings.
    inner=len(v)
    for k in range(N):
        th=2*pi*k/N;v.append((.026*math.cos(th),.026*math.sin(th),.30))
    for k in range(N):f.append(((Z-1)*N+k,(Z-1)*N+(k+1)%N,inner+(k+1)%N,inner+k));mi.append(3)
    f.append(tuple(inner+k for k in range(N)));mi.append(4)
    f.append(tuple(reversed(range(N))));mi.append(0)
    o=mesh('Single stem cortex and integrated attachment bosses',v,f,mats)
    for poly,m in zip(o.data.polygons,mi):poly.material_index=m
elif slug=='ventifact':
    mats=[mat('Wind polished stone','#A49379'),mat('Basal fracture','#817360')]
    # Exact half-space intersection creates three uninterrupted abrasion planes,
    # not a noisy sphere. Basal planes trim the supporting broken shoulder.
    planes=[(Vector((0,0,-1)),0)]
    for k in range(6):
        th=2*pi*k/6;planes.append((Vector((math.cos(th),math.sin(th),-.08)),.40 if k%2==0 else .36))
    for k in range(3):
        th=2*pi*k/3+.2;planes.append((Vector((.93*math.cos(th),.93*math.sin(th),1)),.60))
    from mathutils import Matrix
    v=[]
    for combo in combinations(range(len(planes)),3):
        M=Matrix([planes[i][0] for i in combo])
        if abs(M.determinant())<1e-7:continue
        x=M.inverted()@Vector([planes[i][1] for i in combo])
        if all(n.dot(x)<=d+1e-6 for n,d in planes) and not any((x-Vector(y)).length<1e-5 for y in v):v.append(tuple(x))
    f=[];mi=[]
    for idx,(n,d) in enumerate(planes):
        face=[i for i,x in enumerate(v) if abs(n.dot(Vector(x))-d)<1e-5]
        if len(face)<3:continue
        center=sum((Vector(v[i]) for i in face),Vector())/len(face);u=(Vector(v[face[0]])-center).normalized();w=n.normalized().cross(u)
        face.sort(key=lambda i:math.atan2((Vector(v[i])-center).dot(w),(Vector(v[i])-center).dot(u)))
        f.append(tuple(face));mi.append(0 if idx>=7 else 1)
    o=mesh('Three dominant wind abrasion planes',v,f,mats)
    for poly,m in zip(o.data.polygons,mi):poly.material_index=m
elif slug=='pentichnus-deep-dwelling-trace':
    mats=[mat('Sediment upper','#B9A17D'),mat('Sediment middle','#AA906B'),mat('Sediment lower','#957D5D'),mat('Cavity walls','#9C8262')]
    # Solid sectional annulus: five-sided cavity is deep, not surface embossing.
    # Remove one complete front sector; cut caps show sediment thickness to floor.
    N=5;zs=[0,.018,.052,.09,.13];ris=[.004,.012,.022,.037]
    v=[]
    for z in zs:
        for k in range(N):
            th=2*pi*k/N-pi/2;v.append((.07*math.cos(th),.07*math.sin(th),z))
    for z,ri in zip(zs[1:],ris):
        for k in range(N):
            th=2*pi*k/N-pi/2;v.append((ri*math.cos(th),ri*math.sin(th),z))
    cb=len(v);v.append((0,0,0));cf=len(v);v.append((0,0,.018));f=[];mi=[]
    for j in range(4):
        for k in range(1,5):
            kk=(k+1)%5;f.append((j*5+k,j*5+kk,(j+1)*5+kk,(j+1)*5+k));mi.append(min(j//2,2))
    for j in range(3):
        for k in range(1,5):
            kk=(k+1)%5;f.append((25+j*5+k,25+(j+1)*5+k,25+(j+1)*5+kk,25+j*5+kk));mi.append(3)
    for k in range(1,5):
        kk=(k+1)%5
        f.append((20+k,20+kk,40+kk,40+k));mi.append(0)
        f.append((cb,kk,k));mi.append(2)
        f.append((cf,25+k,25+kk));mi.append(3)
    for k in [0,1]:
        f.append(tuple([j*5+k for j in range(5)]+[25+j*5+k for j in reversed(range(4))]+[cf,cb]));mi.append(1)
    o=mesh('Pentameral deep cavity sectional sediment',v,f,mats)
    for poly,m in zip(o.data.polygons,mi):poly.material_index=m
else:raise ValueError(slug)
ground_asset(c,center_xy=True)
metadata={'generator':str(Path(__file__).name),'description':cfg['design'],'nominal_design_dimensions_blender_xyz_m':cfg['nominal_design_dimensions_blender_xyz_m'],'scale_uncertainty':'Artistic dimensions; no exact measured specimen claim.','surface_profile':'palette-only','reconstruction_type':'artistic-concept','references':'references.json'}
export_asset(slug,slug,'specimen',c,metadata,output_root=a.out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
