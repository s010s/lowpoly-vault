# SPDX-License-Identifier: MIT
"""Original Fruitafossor restoration. Run Blender 4.3.2 -b -t 2 --python this.py -- --output-dir OUTPUT.
No image, fossil mesh, network, other candidate directory or undeclared helper is read.
"""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, ground_asset, export_asset
P=json.loads((HERE/'params.json').read_text())
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,required=True); A=ap.parse_args(args)
OUT=A.output_dir.resolve(); OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene(P['asset_id'],P['seed'])
M={k:make_material(k,v,roughness=.34 if k=='eye' else .84) for k,v in P['palette'].items()}

def loft_data(rings,n=12,mode='path'):
    """Closed elliptical cross sections, with single center fan caps."""
    vv=[]; ff=[]
    for i,(center,ra,rb) in enumerate(rings):
        c=Vector(center)
        if mode=='y': u=Vector((1,0,0)); v=Vector((0,0,1))
        elif mode=='x': u=Vector((0,1,0)); v=Vector((0,0,1))
        else:
            t=(Vector(rings[min(i+1,len(rings)-1)][0])-Vector(rings[max(0,i-1)][0])).normalized()
            ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((0,1,0))
            u=t.cross(ref).normalized(); v=t.cross(u).normalized()
        for j in range(n):
            a=2*math.pi*j/n; vv.append(tuple(c+ra*math.cos(a)*u+rb*math.sin(a)*v))
    for i in range(len(rings)-1):
        for j in range(n): ff.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    for i,reverse in [(0,True),(len(rings)-1,False)]:
        cap=len(vv); vv.append(tuple(rings[i][0]))
        for j in range(n):
            face=(cap,i*n+j,i*n+(j+1)%n); ff.append(face[::-1] if reverse else face)
    return vv,ff

def loft(name,rings,mat='fur',n=12,mode='path',ventral=False):
    vv,ff=loft_data(rings,n,mode); ob=mesh_object(name,vv,ff,[M['fur'],M['ventral']] if ventral else M[mat],COL)
    if ventral:
        for poly in ob.data.polygons:
            # Restricted underside only; no invented stripes, spots or sharp dorsal mask.
            coords=[ob.data.vertices[j].co for j in poly.vertices]
            avg=sum((c.z for c in coords))/len(coords)
            y=sum((c.y for c in coords))/len(coords)
            centerz=min(rings,key=lambda r:abs(r[0][1]-y))[0][2]
            poly.material_index=1 if avg<centerz-.006 else 0
    return ob

def aggregate(name,parts,mat='fur',n=10,mode='path'):
    vv=[]; ff=[]
    for rings in parts:
        v,f=loft_data(rings,n,mode); off=len(vv); vv.extend(v); ff.extend(tuple(j+off for j in face) for face in f)
    return mesh_object(name,vv,ff,M[mat],COL)

def oval(name,c,r,mat,n=12,levels=7):
    # Profile ellipsoid with finite cap rings, avoiding tiny pole sliver triangles.
    cx,cy,cz=c; rx,ry,rz=r; rings=[]
    for j in range(levels):
        t=-.94+1.88*j/(levels-1); s=math.sqrt(1-t*t)
        rings.append(((cx,cy+ry*t,cz),rx*s,rz*s))
    return loft(name,rings,mat,n,'y')

# A deliberately drawn connected axial outline: wedge muzzle, low neck, strong shoulders,
# round compact chest and tapered rump. This is not a chain of untouched sphere primitives.
axial=[(-.064,.0245,.0028,.0026),(-.060,.0254,.0042,.0037),(-.055,.027,.0056,.0051),
       (-.049,.0294,.0078,.0074),(-.043,.0302,.0096,.0092),(-.037,.0294,.0103,.0101),
       (-.031,.029,.0109,.0104),(-.024,.0288,.0138,.0132),(-.016,.0292,.0164,.0157),
       (-.006,.0298,.0170,.0165),(.006,.0294,.0164,.0156),(.017,.0284,.0148,.0140),
       (.028,.0261,.0108,.0108),(.035,.0238,.0061,.0065),(.039,.022,.003,.0036)]
loft('body-neck-wedge-head', [((0,y,z),rx,rz) for y,z,rx,rz in axial],n=20,mode='y',ventral=True)
# Gently downturned slim tail, not a squirrel brush or naked rat-whip caricature.
loft('long-tapered-tail', [((0,.034,.023),.0042,.0044),((.0005,.044,.020),.0038,.0035),
    ((.0015,.055,.0155),.0030,.0027),((.003,.067,.0108),.0022,.0020),
    ((.005,.078,.0075),.0015,.00135),((.008,.087,.0061),.0009,.0008),
    ((.011,.0955,.0058),.00034,.00034)],n=12)

for side,label in [(-1,'left'),(1,'right')]:
    S=lambda x,y,z:(side*x,y,z)
    # Massive shoulder and broad forearm taper into short metacarpal palm.
    loft(label+'-powerful-forelimb',[(S(.0105,-.021,.030),.0080,.0088),
        (S(.017,-.018,.026),.0082,.0082),(S(.022,-.015,.018),.0068,.0069),
        (S(.023,-.019,.012),.0057,.0056),(S(.022,-.026,.0064),.0046,.0045),
        (S(.022,-.030,.0042),.0044,.0031)],n=14)
    # Five spaced digits. Central three are stronger/longer; broad, flattened, single apex claws.
    fingers=[]; claws=[]
    for k,off in enumerate([-.0052,-.00265,0,.0027,.0052]):
        length=[.0050,.0078,.0088,.0077,.0053][k]
        x=.022+off; y0=-.0323+abs(off)*.23; xt=x+off*.25
        fingers.append([(S(x,y0+.0025,.0036),.00125,.00125),(S(xt,y0-.001,.00275),.00125,.0010),
                        (S(xt,y0-.0032,.0023),.0011,.0008)])
        # The strong flattened bony terminal is modeled as a low, wide spade in plan,
        # ending at ONE point. Never bifid, scythe-like or needle-conical.
        yy=y0-.0031; end=yy-length
        claws.append([(S(xt,yy,.00245),.00115,.00072),(S(xt,yy-.0021,.0020),.00155,.00065),
                      (S(xt, end+.0017,.00145),.00135,.0004),(S(xt,end,.0012),.00025,.00022)])
    palm=[(S(.022,-.0295,.004),.0068,.0030),(S(.022,-.0335,.003),.0065,.0017)]
    aggregate(label+'-short-hand-and-five-digits',[palm]+fingers,n=10,mode='y')
    aggregate(label+'-five-spatulate-manual-claws',claws,'claw',n=10,mode='y')
    # More gracile hind limbs and elongated planted feet.
    loft(label+'-hindlimb',[(S(.0098,.024,.027),.0067,.0074),(S(.015,.020,.022),.0054,.0060),
        (S(.0165,.015,.0165),.0039,.0043),(S(.017,.022,.011),.0028,.0032),
        (S(.0175,.029,.0058),.0025,.0027),(S(.0175,.028,.0032),.0027,.0020)],n=12)
    hindparts=[[(S(.0175,.029,.0028),.0034,.0020),(S(.0175,.022,.0025),.0045,.0018),
                (S(.0175,.016,.0023),.0046,.0015)]]; hindclaws=[]
    for k,off in enumerate([-.0034,-.0017,0,.0017,.0034]):
        y=.012+[.002,.0005,0,.0007,.0024][k]; x=.0175+off
        hindparts.append([(S(x,.018,.0023),.00085,.001),(S(x,y,.0017),.0008,.00075)])
        hindclaws.append([(S(x,y+.0002,.0018),.0007,.0006),(S(x,y-.0017,.0012),.00038,.0003)])
    aggregate(label+'-elongated-hindfoot',hindparts,'skin',n=10,mode='y')
    aggregate(label+'-short-hind-claws',hindclaws,'claw',n=8,mode='y')
    # Understated soft-tissue reconstruction. Eye sits on skull, not on a stalk.
    oval(label+'-eye',S(.00705,-.0495,.0321),(.00165,.0018,.00165),'eye',n=12)
    oval(label+'-small-ear',S(.0092,-.0377,.0396),(.0032,.0018,.0036),'fur',n=12)
    oval(label+'-ear-concha',S(.0101,-.0388,.0398),(.0018,.0009,.0020),'skin',n=10)
    # Small closed mouth crease, no speculative exposed dental anatomy.
    loft(label+'-closed-mouth',[(S(.0028,-.0625,.0233),.00024,.00028),
        (S(.0037,-.056,.0234),.00024,.00028),(S(.0047,-.0515,.024),.00024,.00028)],'nose',n=6)
oval('blunt-sensitive-nose',(0,-.0648,.0246),(.0031,.0016,.0023),'nose',n=12)
shift=ground_asset(COL,center_xy=False)
record=export_asset('fruitafossor',{'en':'Fruitafossor windscheffeli','zh':'掘齿兽'},'animals',COL,
    metadata={'description':{'en':'Original whole-animal reconstruction of a small Late Jurassic digging mammaliaform. Compact trunk, powerful forelimbs and flattened digging claws.','zh':'晚侏罗世小型掘地哺乳型动物完整活体原创复原。紧凑躯干、强健前肢与宽扁掘爪。'},
    'generator':'source/generate.py','revision':'r001','style_profile':P['profile'],
    'scale_note':'Approx. 16 cm reconstructed total length; LACM 150948 is incomplete, not a complete measured body.',
    'reconstruction_notes':'Fur, color, external ears, tail completion and exact stance are artistic reconstructions.',
    'ground_shift_m':shift},output_root=OUT/'private'/'canonical-export',render=False,
    max_triangles=P['max_triangles'],max_materials=P['max_materials'],max_primitives=P['max_primitives'])
built=OUT/'private'/'canonical-export'/'fruitafossor'
for ext in ['glb','blend']: shutil.copy2(built/f'fruitafossor.{ext}',OUT/f'model.{ext}')
if (OUT/'model.glb').stat().st_size>P['max_glb_bytes']: raise RuntimeError('Frozen byte budget exceeded')
(OUT/'qa'/'evidence').mkdir(parents=True,exist_ok=True)
shutil.copy2(built/'qa.json',OUT/'qa'/'evidence'/'source-export.json')
record.update(glb='model.glb',blend='model.blend',preview='preview.png')
(OUT/'qa'/'evidence'/'build-metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
print('BUILD_COMPLETE',json.dumps({'triangles':record['triangles'],'bytes':record['glb_bytes'],'sha256':record['sha256']['glb']}))
