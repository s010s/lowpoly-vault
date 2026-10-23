# SPDX-License-Identifier: MIT
"""Original Atopodentatus whole-organism reconstruction. Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Only this directory's params.json and vendored deps are read; no network or asset imports.
"""
import argparse, json, math, sys, shutil, hashlib
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
P=json.loads((HERE/'params.json').read_text())
parser=argparse.ArgumentParser(); parser.add_argument('--out',type=Path,default=HERE.parent)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.out.resolve(); OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene('atopodentatus',seed=P['seed'])
M=[make_material(n,c,roughness=.85 if n!='eye' else .4) for n,c in P['materials']]
class Shape:
    def __init__(self): self.v=[]; self.f=[]; self.mi=[]
    def add(self,v,f,mi=0):
        offset=len(self.v); self.v.extend(v); self.f.extend([tuple(offset+i for i in face) for face in f]); self.mi.extend([mi]*len(f))
    def loft(self,rings,n=16,matfunc=None,power=1.0):
        # Rings: x,y,z, horizontal radius, vertical radius; axis along Y.
        v=[]; f=[]; idx=[]
        for x,y,z,w,h in rings:
            for j in range(n):
                a=2*math.pi*j/n; ca,sa=math.cos(a),math.sin(a); v.append((x+w*math.copysign(abs(ca)**power,ca),y,z+h*math.copysign(abs(sa)**power,sa)))
        f.append(tuple(range(n-1,-1,-1))); idx.append(0)
        for k in range(len(rings)-1):
            for j in range(n):
                f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j)); idx.append(matfunc(k,j,n) if matfunc else 0)
        f.append(tuple((len(rings)-1)*n+j for j in range(n))); idx.append(0)
        off=len(self.v); self.v.extend(v);self.f.extend([tuple(off+i for i in face) for face in f]);self.mi.extend(idx)
    def ellipsoid(self,center,scale,mat=0,n=12,lats=6):
        v=[(center[0],center[1],center[2]+scale[2])];f=[]
        for k in range(1,lats):
            phi=math.pi*k/lats
            for j in range(n):
                a=2*math.pi*j/n;v.append((center[0]+scale[0]*math.sin(phi)*math.cos(a),center[1]+scale[1]*math.sin(phi)*math.sin(a),center[2]+scale[2]*math.cos(phi)))
        v.append((center[0],center[1],center[2]-scale[2]));end=len(v)-1
        for j in range(n): f.append((0,1+j,1+(j+1)%n))
        for k in range(lats-2):
            for j in range(n): f.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
        for j in range(n):f.append((end,1+(lats-2)*n+(j+1)%n,1+(lats-2)*n+j))
        self.add(v,f,mat)
    def tooth(self,x,y,z,wx,wy,height,mat=0,taper=.15):
        v=[(x+sx*wx,y+sy*wy,z) for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        v += [(x+sx*wx*taper,y+sy*wy*taper,z+height) for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        self.add(v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
    def object(self,name,materials):
        obj=mesh_object(name,self.v,self.f,materials,COL)
        for polygon,idx in zip(obj.data.polygons,self.mi): polygon.material_index=idx
        obj['semantic_part']=name;return obj
# One custom loft extends continuously from skull through neck, trunk and tapered tail.
body=Shape()
rings=[(0,-1.215,.320,.058,.020),(0,-1.195,.323,.063,.025),(0,-1.16,.328,.063,.031),(0,-1.12,.328,.074,.038),(0,-1.08,.323,.080,.039),(0,-1.04,.315,.070,.043),(0,-1.00,.303,.060,.050),(0,-.94,.291,.061,.057),(0,-.86,.279,.070,.067),(0,-.77,.267,.096,.085),(0,-.67,.250,.141,.119),(0,-.56,.238,.180,.153),(0,-.43,.235,.207,.181),(0,-.25,.235,.220,.193),(0,-.05,.232,.216,.185),(0,.14,.225,.203,.165),(0,.30,.218,.178,.142),(0,.43,.210,.138,.112),(0,.53,.207,.111,.091),(.004,.64,.208,.091,.078),(.012,.77,.212,.071,.066),(.024,.91,.218,.052,.054),(.042,1.06,.223,.036,.044),(.063,1.20,.225,.024,.034),(.081,1.33,.224,.014,.024),(.090,1.43,.221,.007,.014),(.094,1.51,.219,.0015,.002)]
def region(k,j,n):
    a=2*math.pi*(j+.5)/n
    if math.sin(a)<-.40:return 2
    if math.sin(a)>.55:return 1
    return 0
body.loft(rings,n=20,matfunc=region)
body.object('continuous-skull-neck-trunk-tail',M[:3])
# Broad, straight transverse hammer jaws, deliberately no downturned rostrum.
upper=Shape();upper.loft([(0,-1.240,.312,.130,.011),(0,-1.233,.314,.148,.014),(0,-1.213,.315,.151,.016),(0,-1.199,.319,.144,.015),(0,-1.191,.321,.078,.014)],n=16,power=.4)
for side in [-1,1]:
    upper.loft([(side*(.062+.010*t),-1.194+.111*t,.310+.004*t,.008,.009) for t in [-.04,.25,.5,.75,1.04]],n=12)
upper.object('upper-hammerjaw',M[0])
lower=Shape();lower.loft([(0,-1.236,.273,.129,.007),(0,-1.228,.273,.146,.009),(0,-1.208,.274,.147,.011),(0,-1.195,.275,.071,.010),(0,-1.16,.278,.064,.009),(0,-1.12,.281,.071,.009),(0,-1.075,.284,.073,.009),(0,-1.050,.290,.052,.011)],n=16,power=.4)
for side in [-1,1]:
    lower.loft([(side*(.062+.010*t),-1.194+.111*t,.278+.005*t,.007,.008) for t in [-.04,.25,.5,.75,1.04]],n=12)
lower.object('lower-hammerjaw-and-rami',M[2])
# Four limbs with deliberately shaped elbows, broad webbed hands/feet and five rounded digits.
# Ring paths are baked in vertices: no mirrored negative-scale objects.
def limb(side,front):
    y=-.54 if front else .35
    paths=[(.13,y,.22,.084,.075),(.22,y+.01,.20,.082,.061),(.31,y+.07,.17,.060,.045),(.35,y+.15,.147,.042,.034),(.42,y+.19,.132,.069,.024),(.48,y+.22,.122,.081,.018),(.53,y+.23,.119,.057,.012)]
    if not front: paths=[(x*.88,yy+.12*(x/.53),zz-.01,w*.88,h*.9) for x,yy,zz,w,h in paths]
    # local oval cross sections normal to X-ish limb axis; y extent supplies paddle width.
    v=[];f=[];n=12
    for x,yy,z,w,h in paths:
        for j in range(n):
            a=2*math.pi*j/n;v.append((side*x,yy+w*math.cos(a),z+h*math.sin(a)))
    f.append(tuple(range(n-1,-1,-1)))
    for k in range(len(paths)-1):
        for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    f.append(tuple((len(paths)-1)*n+j for j in range(n)))
    part=Shape();part.add(v,f)
    # Five stubby terminal digits, webbing represented by the broad final paddle loft.
    xx,yy,z,w,h=paths[-1]
    for i in range(5):
        dy=(i-2)*w*.40
        length=.031*(1-abs(i-2)*.12)
        part.ellipsoid((side*(xx+.006),yy+dy,z-.002),(.023+length*.25,w*.215,.010),n=8,lats=4)
    part.object(('left' if side<0 else 'right')+('-forelimb' if front else '-hindlimb'),M[0])
for s in [-1,1]:
    limb(s,True);limb(s,False)
# Front robust short chisels; posterior thin close-spaced filtering teeth.
teeth=Shape()
for i in range(P['front_teeth_per_jaw']):
    x=-.126+.252*i/(P['front_teeth_per_jaw']-1)
    teeth.tooth(x,-1.234,.303,.0043,.0034,-.013,taper=.76)
    teeth.tooth(x+.001,-1.231,.279,.0039,.0030,.012,taper=.76)
for s in [-1,1]:
    for i in range(P['filter_teeth_per_side_per_jaw']):
        t=i/(P['filter_teeth_per_side_per_jaw']-1); y=-1.194+.111*t
        x=s*(.062+.010*t)
        upperz=.304+.004*t; lowerz=.283+.005*t
        teeth.tooth(x,y,upperz,.0010,.0010,-.014,taper=.06)
        teeth.tooth(x,y+.0016,lowerz,.0009,.0009,.014,taper=.06)
teeth.object('front-chisels-and-posterior-filter-mesh',M[3])
# Eyes are on the skull posterior to the hammer, never at the hammer ends.
eyes=Shape()
for s in [-1,1]:
    eyes.ellipsoid((s*.065,-1.094,.349),(.012,.014,.010),0,n=12,lats=6)
    eyes.ellipsoid((s*.071,-1.096,.354),(.007,.009,.006),1,n=10,lats=5)
    eyes.ellipsoid((s*.073,-1.099,.358),(.0038,.0045,.0028),0,n=8,lats=4)
# Thin dark recessed buccal cavity: fully buried margins, not a floating mouth outline.
eyes.loft([(0,-1.225,.291,.124,.001),(0,-1.207,.292,.131,.001),(0,-1.193,.294,.060,.001),(0,-1.15,.296,.059,.001),(0,-1.095,.298,.066,.001),(0,-1.066,.298,.055,.001)],n=12)
eyes.object('eyes-and-recessed-mouth',M[4:])
root=bpy.data.objects[COL['asset_root']];root['mounting_point']='World origin below trunk center; neutral suspended swimming pose, not ground-contact claim.'
root['anatomical_limbs']=4;root['scale_basis']='2.75 m approximate artistic total target; not specimen measurement'
for o in COL.all_objects:
    if o.type=='MESH':o['construction']='Original deterministic custom meshes; reconstruction, no imported model'
META={'description':{'en':'Original low-poly reconstruction of Atopodentatus unicus, with transverse hammer jaws, front scraping teeth and posterior fine filtering dentition.','zh':'滤齿龙完整动物原创低多边形复原，横宽锤颌、前部短刮齿与后部细密滤齿分区。'},'generator':'source/generate.py','reconstruction_notes':['Colour, living soft tissues, limb webbing and pose are artistic inference.','Dentition count reduced for readability; skull length about 18 percent of trunk, not total length.','Neutral swimming pose; origin is mounting point below trunk center.'],'sources':['https://doi.org/10.1126/sciadv.1501659'],'consuming_threejs_version':'0.180.0','render_profile':'Palette-only static original mesh'}
stage=OUT/'private'/'build-stage'
record=export_asset('atopodentatus',{'en':'Atopodentatus','zh':'滤齿龙'},'animals',COL,metadata=META,output_root=stage,render=False,max_triangles=6500,max_materials=6,max_primitives=12,diagnostics=False)
build=stage/'atopodentatus'
shutil.copy2(build/'atopodentatus.glb',OUT/'model.glb');shutil.copy2(build/'atopodentatus.blend',OUT/'model.blend')
(OUT/'qa'/'evidence').mkdir(parents=True,exist_ok=True)
shutil.copy2(build/'qa.json',OUT/'qa'/'evidence'/'geometry.json')
metadata=json.loads((build/'metadata.json').read_text());metadata.update({'glb':'model.glb','blend':'model.blend','preview':'preview.png'})
(OUT/'qa'/'evidence'/'build.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
print('BUILD_COMPLETE',record['triangles'],record['glb_bytes'])
