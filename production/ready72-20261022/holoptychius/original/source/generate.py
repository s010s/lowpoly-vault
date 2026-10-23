#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Holoptychius whole-animal reconstruction, deterministic Blender 4.3.2.
Usage: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output .
All geometry is authored in meters: -Y anterior, +Z dorsal. No external pixels.
"""
from pathlib import Path
import sys, json, math, shutil, hashlib, argparse
sys.path.insert(0, str(Path(__file__).resolve().parent/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, export_asset

HERE=Path(__file__).resolve().parent
P=json.loads((HERE/'params.json').read_text())
A=argparse.ArgumentParser(); A.add_argument('--output',type=Path,default=HERE.parent); A.add_argument('--gray',action='store_true')
a=A.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=a.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene(P['asset_id'], P['seed'])
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
bpy.context.scene['reconstruction']='Genus artistic living reconstruction; H. jarviki-informed squamation. 0.9 m is illustrative, not specimen measurement.'
M={k:make_material(k,('#959595' if a.gray else v),roughness=(.68 if k=='mouth-eye' else .84)) for k,v in P['palette'].items()}
V=Vector; PI=math.pi
objects=[]
def obj(name,verts,faces,mats,indices=None):
    o=mesh_object(name,verts,faces,mats,COL)
    if indices:
        for p,i in zip(o.data.polygons,indices):p.material_index=i
    objects.append(o); return o
class Mesh:
    def __init__(self):self.v=[];self.f=[]
    def add(self,v,f):
        n=len(self.v);self.v.extend([tuple(x) for x in v]);self.f.extend([tuple(n+i for i in t) for t in f])
    def finish(self,n,m):return obj(n,self.v,self.f,m)

def profile(t,rows):
    # Piecewise linear deliberate cross-section loft; extra profile rings preserve silhouette.
    if t<=rows[0][0]:return rows[0][1:]
    if t>=rows[-1][0]:return rows[-1][1:]
    for q,r in zip(rows,rows[1:]):
        if q[0]<=t<=r[0]:
            f=(t-q[0])/(r[0]-q[0]);return tuple(x+(y-x)*f for x,y in zip(q[1:],r[1:]))
BODY=P['body_profile']
def body(t,theta,offset=0):
    rx,rz,cx,cz=profile(t,BODY)
    n=V((math.cos(theta)/rx,0,math.sin(theta)/rz)).normalized()
    return V((cx+rx*math.cos(theta),t,cz+rz*math.sin(theta)))+n*offset

def loft_body():
    sides=32; v=[];f=[];mi=[]
    for y,*_ in BODY:
        for j in range(sides):v.append(tuple(body(y,2*PI*j/sides)))
    for k in range(len(BODY)-1):
        for j in range(sides):
            f.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
            s=math.sin(2*PI*(j+.5)/sides); mi.append(2 if s<-.58 else 1 if s>.58 else 0)
    f+=[tuple(reversed(range(sides))),tuple((len(BODY)-1)*sides+j for j in range(sides))]; mi +=[0,0]
    obj('Torso_and_axial_tail',v,f,[M['slate-olive'],M['dorsal-ridges'],M['pale-belly']],mi)

def head_loft(name,rows,lower=False):
    n=24;v=[];f=[];mi=[]
    for y,rx,top,bot in rows:
        for j in range(n):
            th=2*PI*j/n
            # Broad, low rostrum and rounded squared-off cheek.
            x=rx*math.copysign(abs(math.cos(th))**.82,math.cos(th))
            z=(top+bot)/2+(top-bot)/2*math.sin(th)
            v.append((x,y,z))
    for k in range(len(rows)-1):
        for j in range(n):
            f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
            mi.append(1 if lower or math.sin(2*PI*(j+.5)/n)<-.8 else 0)
    f.extend([tuple(reversed(range(n))),tuple((len(rows)-1)*n+j for j in range(n))]);mi +=[0,0]
    obj(name,v,f,[M['slate-olive'],M['pale-belly']],mi)

def ellipsoid(name,center,radii,material,n=16,k=8,normal=None):
    c=V(center); vs=[];fs=[]
    # Nondegenerate poles, ring topology only between actual latitudes.
    zaxis=V(normal or (0,0,1)).normalized(); xaxis=zaxis.cross(V((0,1,0))).normalized(); yaxis=zaxis.cross(xaxis)
    vs.append(c-zaxis*radii[2])
    for r in range(1,k):
        ph=-PI/2+PI*r/k
        for j in range(n):
            th=2*PI*j/n;vs.append(c+xaxis*(radii[0]*math.cos(ph)*math.cos(th))+yaxis*(radii[1]*math.cos(ph)*math.sin(th))+zaxis*(radii[2]*math.sin(ph)))
    end=len(vs);vs.append(c+zaxis*radii[2])
    for j in range(n):fs.append((0,1+(j+1)%n,1+j))
    for r in range(k-2):
        s=1+r*n;t=s+n
        for j in range(n):fs.append((s+j,s+(j+1)%n,t+(j+1)%n,t+j))
    for j in range(n):fs.append((end,end-n+j,end-n+(j+1)%n))
    return obj(name,vs,fs,material)

def tube(name,points,radii,material,n=8):
    v=[];f=[]
    for i,p in enumerate(points):
        p=V(p); tangent=V(points[min(i+1,len(points)-1)])-V(points[max(0,i-1)])
        tangent.normalize(); ref=V((0,0,1)) if abs(tangent.z)<.95 else V((0,1,0));u=tangent.cross(ref).normalized(); w=tangent.cross(u)
        for j in range(n):v.append(p+(u*math.cos(2*PI*j/n)+w*math.sin(2*PI*j/n))*radii[i])
    for i in range(len(points)-1):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f +=[tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]
    return obj(name,v,f,material)

RAYS=Mesh()
def ridge(mesh,start,end,width,height,normal):
    s=V(start);e=V(end);n=V(normal).normalized();mid=(s+e)*.5
    axis=(e-s).normalized();w=n.cross(axis).normalized()*width
    verts=[s,e,mid-w,mid+w,mid+n*height]
    # Closed six-triangle tapered relief, not an infinitely thin floating line.
    faces=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(0,3,2),(3,1,2)]
    mesh.add(verts,faces)

def fin(name,outline,center,normal,thick=.004,rays=True):
    n=V(normal).normalized();c=V(center);N=len(outline)
    vs=[c+n*thick]+[V(p)+n*.00055 for p in outline]+[c-n*thick]+[V(p)-n*.00055 for p in outline]
    fs=[];mi=[]
    for j in range(N):
        k=(j+1)%N
        fs.extend([(0,1+j,1+k),(N+1,N+2+k,N+2+j),(1+j,N+2+j,N+2+k,1+k)])
        mi.extend([0,0,1])
    obj(name,vs,fs,[M['fin-membrane'],M['slate-olive']],mi)
    if rays:
        for j in range(1,N-1):
            tip=V(outline[j]);start=c*.72+tip*.28;end=c*.12+tip*.88
            # Intersect fin surface slightly so no detached decorative filaments.
            for side in [-1,1]:
                ridge(RAYS,start+n*(side*.0028),end+n*(side*.0008),.0006,.00045,side*n)

loft_body()
head_loft('Broad_flattened_cranium',P['upper_head_profile'])
head_loft('Robust_lower_jaw',P['lower_jaw_profile'],True)
# A recessed opaque mouth interior makes the restrained opening legible from front.
ellipsoid('Recessed_mouth_cavity',(0,-.382,-.017),(.067,.061,.004),M['mouth-eye'],n=20,k=4)
for side in [-1,1]:
    normal=V((side*.82,-.10,.57)).normalized()
    center=V((side*.074,-.388,.026))
    ellipsoid(('Left' if side<0 else 'Right')+'_orbital_rim',center,(.010,.009,.0032),M['pale-belly'],n=12,k=6,normal=normal)
    ellipsoid(('Left' if side<0 else 'Right')+'_lateral_eye',center+normal*.002,(.0071,.0064,.0025),M['mouth-eye'],n=12,k=6,normal=normal)
    # Gill seam, a purposeful short arch around the posterior cheek, not a neck ring.
    pts=[]
    for j in range(7):
        t=j/6;pts.append((side*(.067-.014*abs(2*t-1)), -.288-.013*math.sin(PI*t), .049-.10*t))
    tube(('Left' if side<0 else 'Right')+'_opercular_seam',pts,[.0013]*7,M['dorsal-ridges'],6)
# Tiny inward teeth are illustrative, not a tooth count reconstruction.
TEETH=Mesh()
for side in [-1,1]:
    for y,x in [(-.427,.032),(-.411,.051),(-.392,.063),(-.37,.07)]:
        p=V((side*x,y,-.0135));r=.0015
        v=[p+V((-r,-r,0)),p+V((r,-r,0)),p+V((r,r,0)),p+V((-r,r,0)),p+V((0,0,-.0044))]
        TEETH.add(v,[(0,3,2,1),(0,1,4),(1,2,4),(2,3,4),(3,0,4)])
TEETH.finish('Small_recessed_pointed_teeth',M['ivory-details'])
# Paired fleshy fins. Broad pectorals are intentionally unlike slender lungfish filaments.
for side in [-1,1]:
    label='Left' if side<0 else 'Right'
    def S(p):return (side*p[0],p[1],p[2])
    tube(label+'_pectoral_fleshy_lobe',[S((.051,-.248,-.028)),S((.083,-.22,-.04)),S((.112,-.181,-.075))],[.018,.016,.007],M['slate-olive'],10)
    outline=[(.064,-.25,-.035),(.092,-.253,-.063),(.121,-.231,-.102),(.15,-.19,-.137),(.165,-.118,-.154),(.139,-.14,-.117),(.112,-.163,-.087),(.083,-.19,-.06),(.064,-.22,-.043)]
    fin(label+'_pectoral_lobed_fin',[S(p) for p in outline],S((.108,-.20,-.091)),(side*.78,-.36,.51),.0037)
    tube(label+'_pelvic_fleshy_lobe',[S((.035,.061,-.042)),S((.058,.086,-.058)),S((.074,.111,-.079))],[.011,.011,.005],M['slate-olive'],8)
    outline=[(.04,.064,-.044),(.058,.058,-.066),(.085,.079,-.104),(.099,.12,-.133),(.095,.153,-.135),(.078,.169,-.119),(.06,.147,-.085),(.044,.1,-.055)]
    fin(label+'_pelvic_lobed_fin',[S(p) for p in outline],S((.069,.108,-.09)),(side*.78,-.32,.53),.0027)

def X(y,z):
    rx,rz,cx,cz=profile(y,BODY);return (cx,y,z)
fin('First_separate_posterior_dorsal',[X(y,z) for y,z in [(.055,.055),(.073,.085),(.101,.113),(.123,.115),(.133,.102),(.126,.086),(.109,.063),(.094,.049)]],X(.092,.075),(1,0,0),.0034)
fin('Larger_second_posterior_dorsal',[X(y,z) for y,z in [(.164,.037),(.192,.078),(.226,.112),(.261,.13),(.282,.124),(.282,.108),(.261,.08),(.225,.052),(.204,.034)]],X(.22,.073),(1,0,0),.004)
fin('Discrete_posterior_anal',[X(y,z) for y,z in [(.174,-.028),(.191,-.057),(.221,-.086),(.26,-.099),(.279,-.09),(.274,-.075),(.251,-.05),(.222,-.029)]],X(.221,-.058),(1,0,0),.003)
fin('Asymmetric_tapering_caudal',[X(y,z) for y,z in [(.237,.015),(.29,.05),(.35,.08),(.407,.093),(.45,.092),(.426,.071),(.409,.045),(.392,.01),(.374,-.043),(.347,-.055),(.313,-.046),(.275,-.024),(.245,-.013)]],X(.327,.014),(1,0,0),.0046)
RAYS.finish('Subtle_fin_ray_relief',M['dorsal-ridges'])
# Rounded imbricated scale lenses mapped directly to curved torso, in offset rows.
# Individual plates are disconnected closed solids in three joined semantic fields.
fields={'dorsal':Mesh(),'flank':Mesh(),'ventral':Mesh()};ridges={'dorsal':Mesh(),'flank':Mesh(),'ventral':Mesh()};counts={k:0 for k in fields}
rows=[]
y=-.255;row=0
while y<.278:
    rx,rz,_,_=profile(y,BODY)
    circumference=PI*(3*(rx+rz)-math.sqrt((3*rx+rz)*(rx+3*rz)))
    count=max(6,round(circumference/P['scale_circumferential_spacing_m']))
    for j in range(count):
        th=2*PI*(j+.5*(row%2))/count
        sn=math.sin(th);group='ventral' if sn<-.65 else 'dorsal' if sn>.65 else 'flank'
        # Marginally smaller scales where the peduncle tapers, not spikes at tail.
        length=P['scale_length_m']*min(1.,.78+rx*4)
        span=P['scale_width_m']*min(1.,.8+rx*3)
        tangent_speed=math.sqrt((rx*math.sin(th))**2+(rz*math.cos(th))**2)
        angular=span/2/tangent_speed
        ry=length/2;n=10
        verts=[body(y+.0015,th,.00195)]
        for k in range(n):
            angle=2*PI*k/n;dy=ry*math.cos(angle);dt=angular*math.sin(angle)
            raise_m=.0003+.0011*(dy/ry) # anterior edge buried, posterior edge exposed
            verts.append(body(y+dy,th+dt,raise_m))
        verts.append(body(y,th,-.0015));faces=[]
        for k in range(n):
            faces.extend([(0,1+k,1+(k+1)%n),(n+1,1+(k+1)%n,1+k)])
        fields[group].add(verts,faces);counts[group]+=1
        # Flank/dorsal scales bear two shallow, posteriorly aligned ridges.
        # Ventral scales receive one low broad boss rather than spiny grain clouds.
        offsets=[-.30,.30] if group!='ventral' else [0]
        for q in offsets:
            start=body(y-.002,th+angular*q,.0017)
            end=body(y+ry*.78,th+angular*q,.0011)
            normal=V((math.cos(th)/rx,0,math.sin(th)/rz)).normalized()
            ridge(ridges[group],start,end,.0008 if group!='ventral' else .0014,.00055 if group!='ventral' else .00065,normal)
    rows.append({'y_m':y,'plate_count':count});row+=1;y=-.255+row*P['scale_row_spacing_m']
for group in fields:
    mat={'dorsal':'slate-olive','flank':'slate-olive','ventral':'pale-belly'}[group]
    fields[group].finish('Rounded_overlapping_'+group+'_scales',M[mat])
    ridges[group].finish(('Posterior_ridges_' if group!='ventral' else 'Low_ventral_bosses_')+group,M['dorsal-ridges'] if group!='ventral' else M['pale-belly'])
root=bpy.data.objects[COL['asset_root']]
root['mounting_origin']='Whole swimming animal center at (0,0,0), no ground contact. Model axes: -Y anterior, +Z dorsal.'
root['scale_count']=sum(counts.values());root['scale_shape']='Rounded overlapping low closed lens plates with restrained relief.'
# Canonical export performs source QA, explicit static exporter flags and axis comparison.
record=export_asset(P['asset_id'],{'en':'Holoptychius','zh':'全褶鱼'},'fish',COL,
    metadata={'generator':'source/generate.py','description':{'en':'Whole living Holoptychius genus reconstruction with broad predatory head and rounded imbricated scales. 0.90 m illustrative size.','zh':'全褶鱼属完整活体复原，宽扁捕食头部与圆形叠覆鳞片；0.90米为示意美术尺度。'},
              'reconstruction_notes':P['reconstruction_notes'],'source_references':['mondejar2020 Figure 1A-B','miller2007 NBMG13038']},
    output_root=OUT/'private'/'canonical-export',render=False,max_triangles=P['geometry_policy']['max_triangles'],max_materials=P['geometry_policy']['max_materials'],max_primitives=P['geometry_policy']['max_primitives'])
temp=OUT/'private'/'canonical-export'/P['asset_id']
for ext in ['blend','glb']:shutil.copy2(temp/(P['asset_id']+'.'+ext),OUT/('model.'+ext))
qa=json.loads((temp/'qa.json').read_text());(OUT/'qa'/'evidence').mkdir(parents=True,exist_ok=True)
qa['glb']['file']='model.glb'; qa['custom_geometry']={'scale_count':sum(counts.values()),'scales_per_field':counts,'scale_rows':rows,'dorsal_fin_count':2,'paired_pectoral_fins':2,'paired_pelvic_fins':2,'anal_fin_count':1,'caudal_fin_count':1,'toothplate_count':0,'separate_closed_anatomical_components':True,'interpretation':'Closed scale lenses overlap each other and skin by design; this is not a printable union.'}
qa['artifact_sha256']=hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest()
qa['reviewed_warnings']=[{'warning':w,'resolution':'Swimming specimen uses documented central mounting point. Negative Z is intentional, no ground plane.'} for w in qa['source']['warnings']+qa['glb']['warnings'] if 'Lowest' in w]
(OUT/'qa'/'evidence'/'geometry.json').write_text(json.dumps(qa,indent=2)+'\n')
record['glb']='model.glb';record['blend']='model.blend';record['preview']='preview.png';record['origin']='Whole swimming animal center at identity root; no ground contact';record['gray_diagnostic']=a.gray
record['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();record['params_sha256']=hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()
(OUT/'qa'/'evidence'/'build.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
assert (OUT/'model.glb').stat().st_size<=P['geometry_policy']['max_glb_bytes']
print('HOL_COMPLETE',json.dumps({'output':str(OUT),'triangles':qa['glb']['scene_triangles'],'scales':sum(counts.values()),'sha256':qa['glb']['sha256']}))
