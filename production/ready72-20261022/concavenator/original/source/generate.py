# SPDX-License-Identifier: MIT
"""Deterministic original Concavenator whole-animal reconstruction.
Blender: -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUTPUT
Flesh proportions, pose and colour are artistic, not osteometric claims.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
PARAMS=json.loads((HERE/'params.json').read_text())
COL=setup_scene('concavenator',seed=PARAMS['seed'])
MATS={name:make_material('concavenator-'+name,value,roughness=.9) for name,value in PARAMS['palette'].items()}

class Part:
    def __init__(self,name,materials):
        self.name=name; self.materials=materials; self.verts=[]; self.faces=[]; self.indices=[]; self.groups=[]
    def add(self,name,verts,faces,indices=None):
        start=len(self.verts); self.verts.extend(verts)
        self.faces.extend(tuple(start+i for i in face) for face in faces)
        self.indices.extend(indices if indices is not None else [0]*len(faces))
        self.groups.append((name,start,len(self.verts)))
    def finish(self):
        obj=mesh_object(self.name,self.verts,self.faces,[MATS[x] for x in self.materials],COL)
        for polygon,index in zip(obj.data.polygons,self.indices): polygon.material_index=index
        for name,start,end in self.groups: obj.vertex_groups.new(name=name).add(list(range(start,end)),1,'REPLACE')
        return obj

body=Part('Continuous-head-neck-trunk-local-crest-tail',['body','dorsal','belly','crest'])
legs=Part('Muscular-hindlimbs',['body'])
arms=Part('Inward-facing-grasping-forelimbs',['body'])
digits=Part('Three-pedal-and-three-manual-digits',['body'])
keratin=Part('Terminal-claws',['keratin'])
face=Part('Mouth-creases-nostrils-and-eye-sockets',['keratin'])
irises=Part('Amber-eyes',['iris'])

def tube(part,name,points,radii,sides=8,flatten=1):
    """Closed shaped tube with path-aligned rings, no sphere joints."""
    pts=[Vector(p) for p in points]; verts=[]; faces=[]
    for i,p in enumerate(pts):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
        ref=Vector((1,0,0)) if abs(tangent.x)<.85 else Vector((0,1,0))
        u=(ref-tangent*ref.dot(tangent)).normalized(); v=tangent.cross(u).normalized()
        rr=radii[i] if isinstance(radii,(list,tuple)) else radii
        rx,ry=rr if isinstance(rr,(list,tuple)) else (rr,rr*flatten)
        for j in range(sides):
            a=2*math.pi*j/sides; q=p+rx*math.cos(a)*u+ry*math.sin(a)*v; verts.append(tuple(q))
    faces.append(tuple(reversed(range(sides))))
    for i in range(len(pts)-1):
        for j in range(sides): faces.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    faces.append(tuple((len(pts)-1)*sides+j for j in range(sides)))
    part.add(name,verts,faces)

def ellipsoid(part,name,center,radii,n=12,rings=5):
    verts=[(center[0],center[1],center[2]-radii[2])]; faces=[]
    for i in range(1,rings):
        a=-math.pi/2+math.pi*i/rings
        for j in range(n):
            b=2*math.pi*j/n
            verts.append((center[0]+radii[0]*math.cos(a)*math.cos(b),center[1]+radii[1]*math.cos(a)*math.sin(b),center[2]+radii[2]*math.sin(a)))
    top=len(verts); verts.append((center[0],center[1],center[2]+radii[2]))
    for j in range(n): faces.append((0,1+(j+1)%n,1+j))
    for i in range(rings-2):
        for j in range(n):
            a=1+i*n+j; b=1+i*n+(j+1)%n; faces.append((a,b,b+n,a+n))
    for j in range(n): faces.append((1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n,top))
    part.add(name,verts,faces)

# Y, half-width, center Z, half-height, extra height of LOCAL topmost ridge.
# Modest pre-pelvic crest, not a shoulder-to-tail sail. Shape is artistic.
sections=[
 (-2.65,.105,1.91,.105,0),(-2.52,.167,1.965,.165,0),
 (-2.28,.215,2.015,.215,0),(-2.06,.238,2.04,.245,0),
 (-1.87,.221,2.01,.236,0),(-1.70,.184,1.90,.219,0),
 (-1.51,.189,1.75,.246,0),(-1.30,.238,1.63,.317,0),
 (-1.08,.325,1.57,.390,0),(-.80,.390,1.57,.438,0),
 (-.48,.417,1.595,.456,0),(-.32,.428,1.615,.454,.19),
 (-.10,.429,1.630,.435,.48),(.045,.417,1.645,.407,.31),
 (.22,.390,1.655,.364,.08),(.32,.348,1.665,.321,0),
 (.66,.294,1.67,.269,0),(1.02,.242,1.68,.216,0),
 (1.42,.185,1.68,.163,0),(1.86,.138,1.675,.120,0),
 (2.28,.094,1.69,.088,0),(2.68,.060,1.73,.056,0),
 (3.02,.030,1.79,.029,0),(3.35,.0025,1.845,.0025,0)]
verts=[]; faces=[]; indices=[]; N=16
for y,w,z,h,crest in sections:
    for j in range(N):
        a=2*math.pi*j/N; c=math.cos(a); s=math.sin(a)
        elevation=crest*max(s,0)**16
        verts.append((w*c,y,z+h*s+elevation))
faces.append(tuple(reversed(range(N)))); indices.append(0)
for i in range(len(sections)-1):
    for j in range(N):
        faces.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
        s=math.sin(2*math.pi*(j+.5)/N)
        is_crest=max(sections[i][4],sections[i+1][4])>.05 and s>.90
        indices.append(3 if is_crest else 2 if s<-.69 else 1 if s>.83 else 0)
faces.append(tuple((len(sections)-1)*N+j for j in range(N)));indices.append(0)
body.add('continuous-animal-axis',verts,faces,indices)

for side in (-1,1):
    label='left' if side<0 else 'right'; dx=side
    shift=-.13 if side<0 else .13
    tube(legs,label+'-hip-to-metatarsus',[
        (.27*dx,.28,1.66),(.39*dx,.12,1.46),(.465*dx,-.30+shift,1.13),
        (.47*dx,-.17+shift,.94),(.435*dx,.22+shift,.49),(.43*dx,.13+shift,.29),
        (.43*dx,-.12+shift,.080)],
        [(.21,.235),(.245,.23),(.18,.175),(.135,.14),(.072,.079),(.071,.075),(.085,.07)],sides=10)
    for digit,(spread,length) in enumerate(((-.14,.43),(0,.54),(.14,.405)),1):
        bx=.43*dx+spread*.25; by=-.05+shift
        tipx=.43*dx+spread*1.35; tipy=by-length
        points=[(bx,by,.12),(.43*dx+spread*.65,by-.15,.071),(tipx,tipy+.07,.049),(tipx,tipy,.041)]
        toe_start=len(digits.verts)
        tube(digits,f'{label}-pedal-{digit}',points,[.051,.045,.031,.022],sides=8,flatten=.78)
        # Make the fleshy pad, not just the terminal claw, weight-bearing.
        toe_delta=.002-min(v[2] for v in digits.verts[toe_start:])
        for vi in range(toe_start,len(digits.verts)):
            x,y,z=digits.verts[vi];digits.verts[vi]=(x,y,z+toe_delta)
        tube(keratin,f'{label}-pedal-{digit}-claw',[(tipx,tipy+.015,.050+toe_delta),(tipx,tipy-.058,.022),(tipx,tipy-.10,.012)],[.027,.019,.0025],sides=7,flatten=.72)
    tube(arms,label+'-shoulder-elbow-wrist',[
      (.285*dx,-.94,1.63),(.415*dx,-.88,1.40),(.47*dx,-.92,1.24),
      (.475*dx,-1.11,1.19),(.46*dx,-1.31,1.155)],
      [(.11,.13),(.10,.12),(.077,.079),(.058,.063),(.052,.056)],sides=9)
    for digit,(dz,reach) in enumerate(((.085,.17),(0,.25),(-.08,.20)),1):
        points=[(.46*dx,-1.29,1.155+dz*.55),(.47*dx,-1.42,1.16+dz),
                (.47*dx,-1.42-reach*.65,1.13+dz),(.455*dx,-1.42-reach,1.095+dz)]
        tube(digits,f'{label}-manual-{digit}',points,[.026,.023,.017,.012],sides=7)
        tip=points[-1]
        tube(keratin,f'{label}-manual-{digit}-claw',[tip,(.43*dx,tip[1]-.033,tip[2]-.035),(.412*dx,tip[1]-.035,tip[2]-.060)],[.015,.011,.002],sides=6)
    tube(face,label+'-mouth-crease',[(dx*.101,-2.645,1.877),(dx*.159,-2.52,1.885),(dx*.201,-2.28,1.915),(dx*.224,-2.06,1.938),(dx*.218,-1.94,1.972)],[.009,.011,.011,.012,.006],sides=6)
    ellipsoid(face,label+'-nostril',(dx*.164,-2.48,2.016),(.015,.035,.017),n=8,rings=4)
    ellipsoid(face,label+'-orbital-socket',(dx*.205,-1.982,2.139),(.048,.087,.066),n=12,rings=5)
    ellipsoid(irises,label+'-iris',(dx*.249,-2.003,2.140),(.013,.045,.040),n=12,rings=5)
    ellipsoid(face,label+'-pupil',(dx*.261,-2.013,2.140),(.006,.017,.025),n=8,rings=4)
    tube(legs,label+'-low-brow',[(dx*.190,-2.11,2.20),(dx*.222,-2.00,2.205),(dx*.194,-1.89,2.172)],[.023,.032,.014],sides=7)

for part in (body,legs,arms,digits,keratin,face,irises): part.finish()
meshes=[o for o in COL.objects if o.type=='MESH']
minz=min(v.co.z for o in meshes for v in o.data.vertices)
contacts=[Vector(v) for name,start,end in digits.groups if '-pedal-' in name for v in digits.verts[start:end] if v[2]<.004]
foot_y=(min(v.y for v in contacts)+max(v.y for v in contacts))/2
foot_x=(min(v.x for v in contacts)+max(v.x for v in contacts))/2
for o in meshes:
    for v in o.data.vertices: v.co.x-=foot_x; v.co.y-=foot_y; v.co.z-=minz
bpy.context.scene['anatomical_reconstruction']='Artistic living reconstruction, not specimen replica.'
bpy.context.scene['diagnostic_feature']='Localized pre-pelvic elevation from two high presacral neural spines.'
bpy.context.scene['colour_and_soft_tissue']='Unknown: palette, crest soft tissue, stance and volumes are artistic.'
bpy.context.scene['generator_revision']='concavenator-r001-v4'
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True);args=parser.parse_args(argv)
out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
buildroot=out/'private'/'helper-export'
record=export_asset('concavenator',{'en':'Concavenator','zh':'昆卡猎龙'},'dinosaurs',COL,
    metadata={'generator':'source/generate.py','revision':'r001','representation':'living-reconstruction',
      'description':{'en':'Original low-poly reconstruction of Concavenator corcovatus with a localized pre-pelvic crest.','zh':'昆卡猎龙原创低多边形活体重建，髋前局部隆起。'},
      'uncertainty':'Soft-tissue form, integument, colour and stance are artistic; not a specimen replica.'},
    output_root=buildroot,render=False,max_triangles=6000,max_materials=6,max_primitives=12,diagnostics=False)
art=buildroot/'concavenator';evidence=out/'qa'/'evidence';evidence.mkdir(parents=True,exist_ok=True)
shutil.copy2(art/'concavenator.glb',out/'model.glb');shutil.copy2(art/'concavenator.blend',out/'model.blend')
qa=json.loads((art/'qa.json').read_text());(evidence/'source-and-glb.json').write_text(json.dumps(qa,indent=2)+'\n')
record.update(glb='model.glb',blend='model.blend',preview='preview.png',origin='center of intended two-foot contact footprint; root identity')
record['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
record['params_sha256']=hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()
record['source_dependencies']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((HERE/'deps').glob('*.py'))}
(evidence/'build-metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
assert (out/'model.glb').stat().st_size<=2000000
print('CONCAVENATOR_BUILD_COMPLETE '+json.dumps({'sha256':qa['glb']['sha256'],'triangles':qa['glb']['scene_triangles'],'source_warnings':qa['source']['warnings']}))
