#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original P. walkeri whole-organism reconstruction, Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUT
Only local params/deps and Blender/standard-library imports are required.
"""
import argparse, hashlib, json, math, shutil, sys, tempfile
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
A=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); p.add_argument('--clay',action='store_true'); args=p.parse_args(A)
OUT=args.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
P=json.loads((HERE/'params.json').read_text()); C=setup_scene(P['asset_id'],seed=P['seed'])
M=[make_material(name,'#929292' if args.clay else hex,roughness=.88) for name,hex in P['palette_hex'].items()]
V=[]; F=[]; MI=[]; SEM=[]
def add(name,verts,faces,material=0,indices=None):
    start=len(V); V.extend([tuple(v) for v in verts]); F.extend([tuple(start+i for i in f) for f in faces]); MI.extend(indices if indices is not None else [material]*len(faces)); SEM.append((name,start,len(verts)))
def loft(name,sections,n=16,material=0,band=False,power=1):
    # Profile rings (x, y, center Z, half width, half height). Closed shell.
    vs=[]
    for x,y,z,rx,rz in sections:
        for j in range(n):
            a=2*math.pi*j/n; c=math.cos(a); s=math.sin(a)
            vs.append((x+rx*math.copysign(abs(c)**power,c),y,z+rz*math.copysign(abs(s)**power,s)))
    fs=[tuple(range(n-1,-1,-1))]; ms=[material]
    for i in range(len(sections)-1):
        for j in range(n):
            fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
            a=(j+.5)*2*math.pi/n
            ms.append(2 if band and math.sin(a)<-.55 else 1 if band and math.sin(a)>.73 else material)
    fs.append(tuple((len(sections)-1)*n+j for j in range(n))); ms.append(material)
    add(name,vs,fs,material,ms)
def tube(name,sections,n=12,material=0,band=False):
    vs=[]
    for i,(pt,rx,rv) in enumerate(sections):
        t=(Vector(sections[min(i+1,len(sections)-1)][0])-Vector(sections[max(i-1,0)][0])).normalized()
        u=Vector((1,0,0)); u=(u-t*u.dot(t)).normalized(); v=t.cross(u).normalized()
        for j in range(n):
            a=2*math.pi*j/n; vs.append(Vector(pt)+u*(rx*math.cos(a))+v*(rv*math.sin(a)))
    fs=[tuple(range(n-1,-1,-1))]; ms=[material]
    for i in range(len(sections)-1):
        for j in range(n):
            f=(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j); fs.append(f)
            center=sum((Vector(vs[k]) for k in f),Vector())/4
            baseline=(sections[i][0][2]+sections[i+1][0][2])/2
            ms.append(2 if band and center.z<baseline-.10 else material)
    fs.append(tuple((len(sections)-1)*n+j for j in range(n))); ms.append(material)
    add(name,vs,fs,material,ms)
def oval(name,c,r,n=12,rings=5,material=0):
    vs=[(c[0],c[1],c[2]-r[2])]
    for k in range(1,rings):
        a=-math.pi/2+math.pi*k/rings
        for j in range(n):
            t=2*math.pi*j/n; vs.append((c[0]+r[0]*math.cos(a)*math.cos(t),c[1]+r[1]*math.cos(a)*math.sin(t),c[2]+r[2]*math.sin(a)))
    top=len(vs); vs.append((c[0],c[1],c[2]+r[2])); fs=[]
    for j in range(n): fs.append((0,1+(j+1)%n,1+j))
    for k in range(rings-2):
        for j in range(n): fs.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
    for j in range(n): fs.append((top,1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n))
    add(name,vs,fs,material)

# Full continuous torso and tail: a deep herbivorous ribcage, gently arched back,
# broad sacral region, muscular caudal base, then a long slender lifted tail.
loft('ribcage-hip-and-comparatively-reconstructed-tail',[
 (0,-1.75,2.20,.12,.17),(0,-1.57,2.16,.34,.52),(0,-1.42,2.14,.44,.64),(0,-1.08,2.10,.56,.76),
 (0,-.65,2.09,.65,.82),(0,-.18,2.12,.70,.86),(0,.28,2.19,.68,.84),(0,.70,2.27,.60,.75),
 (0,1.05,2.30,.46,.56),(0,1.33,2.28,.345,.40),(0,1.65,2.24,.29,.33),
 (.025,2.04,2.18,.24,.29),(.06,2.49,2.13,.195,.245),(.10,2.95,2.08,.155,.20),
 (.14,3.40,2.06,.12,.155),(.17,3.85,2.07,.088,.117),(.17,4.25,2.11,.061,.083),
 (.14,4.62,2.17,.039,.052),(.09,4.93,2.24,.022,.031),(.035,5.18,2.30,.010,.016),(0,5.30,2.33,.002,.004)
],n=16,band=True)
# Healthy elevated neck, not the ROM768 taphonomic extreme recurvature.
tube('neck-healthy-living-contour',[
 ((0,-1.20,2.28),.36,.40),((0,-1.57,2.53),.35,.42),((0,-1.89,2.78),.30,.36),
 ((0,-2.10,3.00),.26,.30),((0,-2.30,3.16),.24,.26),((0,-2.47,3.22),.23,.22)
],n=14,band=True)
# Long face with low wide bill. No teeth, horns, neck web, or dorsal sail.
loft('long-sloping-face-and-posterior-skull',[
 (0,-3.58,3.075,.24,.070),(0,-3.38,3.12,.225,.115),(0,-3.15,3.19,.215,.16),
 (0,-2.92,3.25,.23,.205),(0,-2.70,3.29,.265,.23),(0,-2.50,3.30,.245,.225),(0,-2.35,3.285,.19,.17)
],n=14,band=True,power=.85)
loft('broad-keratinous-duckbill',[
 (0,-3.70,3.065,.20,.045),(0,-3.65,3.070,.28,.065),(0,-3.52,3.075,.285,.073),(0,-3.36,3.075,.225,.066)
],n=12,material=4,power=.65)
loft('closed-lower-jaw-and-cheek',[
 (0,-3.63,3.005,.245,.028),(0,-3.43,2.995,.22,.05),(0,-3.15,3.015,.215,.085),
 (0,-2.85,3.055,.24,.115),(0,-2.60,3.115,.25,.12),(0,-2.40,3.22,.165,.11)
],n=12,material=2,power=.8)
# Long gently descending tube with solid lowpoly surface. This is not a claim
# about the invisible airway; no invented open snorkel nostrils at its tip.
tube('diagnostic-backward-tubular-cranial-crest',[
 ((0,-2.60,3.40),.165,.18),((0,-2.45,3.53),.145,.16),((0,-2.22,3.60),.125,.145),
 ((0,-1.96,3.615),.115,.13),((0,-1.70,3.60),.105,.12),((0,-1.45,3.565),.097,.113),
 ((0,-1.23,3.515),.089,.105),((0,-1.07,3.455),.078,.093),((0,-1.00,3.405),.045,.060),((0,-.98,3.39),.013,.023)
],n=12,material=3)
for s,label in [(-1,'left'),(1,'right')]:
    # Eye small and lateral, sunk into a subtle upper eyelid, not a floating ball.
    oval(label+'-eye-socket',(s*.254,-2.70,3.315),(.035,.105,.072),n=10,rings=4,material=1)
    oval(label+'-eye',(s*.282,-2.713,3.318),(.014,.050,.044),n=10,rings=4,material=5)
    tube(label+'-upper-eyelid',[( (s*.276,-2.77,3.34),.016,.018),((s*.282,-2.71,3.363),.018,.018),((s*.267,-2.65,3.34),.014,.016)],n=7,material=0)
    oval(label+'-nostril',(s*.218,-3.335,3.167),(.010,.055,.024),n=8,rings=4,material=5)
    tube(label+'-closed-mouth-seam',[
      ((s*.266,-3.62,3.025),.007,.009),((s*.278,-3.50,3.020),.007,.009),((s*.224,-3.34,3.025),.007,.009),
      ((s*.220,-3.10,3.055),.007,.010),((s*.251,-2.86,3.100),.007,.010),((s*.256,-2.67,3.150),.006,.008)
    ],n=6,material=5)
    # Hindlimbs: fleshy thighs brought into the pelvis; knees forward, hocks back.
    tube(label+'-robust-hindlimb',[
      ((s*.46,.72,2.29),.31,.39),((s*.60,.60,1.99),.33,.40),((s*.67,.39,1.64),.285,.34),
      ((s*.70,.24,1.31),.215,.25),((s*.72,.43,1.02),.155,.19),((s*.73,.69,.68),.112,.145),
      ((s*.73,.73,.40),.107,.126),((s*.73,.65,.20),.16,.16)
    ],n=12)
    # Compact broad foot, three short hoof-bearing toes. Flat contact at Z=0.
    loft(label+'-hind-foot-pad',[(s*.73,.14,.095,.14,.075),(s*.73,.27,.12,.245,.12),(s*.73,.48,.155,.25,.155),(s*.73,.72,.17,.155,.15)],n=12,material=0,power=.55)
    for j in range(3):
        x=s*.73+(j-1)*.155; front=.075+(j!=1)*.045
        loft(label+'-hind-hoof-'+str(j+1),[(x,front,.075,.062,.050),(x,front+.045,.081,.080,.065),(x,front+.16,.10,.078,.078),(x,front+.235,.12,.060,.075)],n=8,material=4,power=.40)
    # Supportive forelimbs substantially slimmer than hindlimbs. Short hand
    # forms a weight-bearing mitten, with no raptorial fingers/claws.
    tube(label+'-supportive-forelimb',[
      ((s*.37,-1.25,2.20),.22,.27),((s*.48,-1.12,1.91),.21,.24),((s*.53,-.94,1.57),.155,.19),
      ((s*.55,-.92,1.35),.128,.15),((s*.55,-1.08,.99),.105,.12),((s*.55,-1.20,.62),.085,.105),
      ((s*.55,-1.26,.30),.092,.11),((s*.55,-1.29,.13),.13,.13)
    ],n=12)
    loft(label+'-fore-hand-mitten',[(s*.55,-1.53,.085,.110,.065),(s*.55,-1.46,.11,.158,.11),(s*.55,-1.29,.13,.15,.13),(s*.55,-1.17,.14,.10,.11)],n=12,material=0,power=.55)
    for j in range(3):
        x=s*.55+(j-1)*.085
        loft(label+'-blunt-manual-hoof-'+str(j+1),[(x,-1.565,.067,.029,.035),(x,-1.525,.075,.042,.052),(x,-1.42,.088,.040,.065)],n=8,material=4,power=.45)
# One coherent editable mesh with semantic groups and six material regions;
# independent closed anatomical volumes overlap intentionally at soft joints.
V=[(x,y+P['footprint_origin_y_translation_m'],z) for x,y,z in V]
obj=mesh_object('Parasaurolophus-editable-anatomy',V,F,M,C)
for poly,mat in zip(obj.data.polygons,MI): poly.material_index=mat
for name,start,num in SEM: obj.vertex_groups.new(name=name).add(list(range(start,start+num)),1,'REPLACE')
obj['construction']='Original anatomical lofts; closed components with intentional soft-tissue overlaps. No image textures or copied meshes.'
policy=P['geometry_policy']
with tempfile.TemporaryDirectory(prefix='parasaurolophus-export-',dir=str(OUT)) as temp:
    meta=export_asset(P['asset_id'],{'en':'Parasaurolophus','zh':'副栉龙'},'dinosaurs',C,output_root=Path(temp),render=False,diagnostics=False,
       max_triangles=policy['max_triangles'],max_materials=policy['max_materials'],max_primitives=policy['max_primitives'],
       metadata={'generator':'source/generate.py','description':{'en':'Original whole living P. walkeri reconstruction with long backward tubular crest, duckbill, neutral four-foot support, and elevated tail.','zh':'副栉龙完整活体原创重建：向后延伸的长管冠、鸭嘴、自然四足支撑及离地长尾。'},'reconstruction_notes':P['reconstruction_notes']})
    built=Path(temp)/P['asset_id']; shutil.copy2(built/(P['asset_id']+'.glb'),OUT/'model.glb'); shutil.copy2(built/(P['asset_id']+'.blend'),OUT/'model.blend')
    qa=json.loads((built/'qa.json').read_text()); qa['glb']['file']='model.glb'; meta.update(glb='model.glb',blend='model.blend',preview='preview.png',semantic_sha256=qa['glb']['semantic_sha256'])
    meta['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(); meta['params_sha256']=hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()
    meta['origin']='Identity root at centroid of four ground-contact pads, Z=0, meters'
    meta['scale_note']='9 m genus-level museum estimate as artistic adult target; not a measurement of incomplete ROM768.'
    meta['source_editing']='Single six-material mesh, named anatomical vertex groups, all source component surfaces closed.'
    meta['glb_exporter_version']='4.3.47'; meta['python_runtime']=sys.version; meta['blender_version']=bpy.app.version_string
    (OUT/'build-metadata.json').write_text(json.dumps(meta,indent=2)+'\n'); (OUT/'build-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
if (OUT/'model.glb').stat().st_size>policy['max_glb_bytes']: raise RuntimeError('GLB byte budget exceeded')
print('PARASAUROLOPHUS_BUILD_COMPLETE '+json.dumps({'triangles':meta['triangles'],'glb_sha256':meta['sha256']['glb'],'semantic_sha256':meta['semantic_sha256']}))
