#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Ceratosaurus reconstruction. Run with Blender 4.3.2, -t 2.
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
The params and all Python imports are local to this delivered source tree.
"""
import sys, json, math, hashlib, argparse, tempfile, shutil
from pathlib import Path
from mathutils import Vector
import bpy
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
from qa_glb import audit_glb

ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); p.add_argument('--clay',action='store_true'); args=p.parse_args(ARGS)
OUT=args.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
P=json.loads((HERE/'params.json').read_text())
C=setup_scene(P['asset_id'],seed=P['seed'])
# One mesh per palette slot, with editable semantic vertex groups per component.
# This retains anatomical editing while keeping the export to six primitives.
palette=P['palette_hex']; mats=[make_material(n,'#929292' if args.clay else c,roughness=.88) for n,c in palette.items()]
V=[[] for _ in mats]; F=[[] for _ in mats]; SEM=[[] for _ in mats]

def add(name,verts,faces,mat):
    k=len(V[mat]); V[mat].extend([tuple(v) for v in verts]); F[mat].extend([tuple(k+i for i in f) for f in faces]); SEM[mat].append((name,k,len(verts)))

def loft_y(name,sections,n=12,mat=0,belly=False,power=1):
    # sections = x center, y, z center, lateral radius, vertical radius
    verts=[]
    for x,y,z,rx,rz in sections:
        for j in range(n):
            t=2*math.pi*j/n; a=math.cos(t); b=math.sin(t)
            verts.append((x+rx*math.copysign(abs(a)**power,a),y,z+rz*math.copysign(abs(b)**power,b)))
    faces=[]
    # Deliberate strips provide angular, even-scale faceting; caps are closed.
    faces.append(tuple(range(n-1,-1,-1)))
    for r in range(len(sections)-1):
        for j in range(n): faces.append((r*n+j,r*n+(j+1)%n,(r+1)*n+(j+1)%n,(r+1)*n+j))
    faces.append(tuple((len(sections)-1)*n+j for j in range(n)))
    if not belly: add(name,verts,faces,mat); return
    # Continuous shell, material split along lower flanks; no extra offset skin.
    groups={mat:[],1:[],2:[]}
    for i,face in enumerate(faces):
        if i in (0,len(faces)-1): mi=mat
        else:
            j=(i-1)%n; a=(j+.5)*2*math.pi/n
            mi=1 if math.sin(a)<-.58 else 2 if math.sin(a)>.72 else mat
        groups[mi].append(face)
    for mi,fs in groups.items():
        if fs: add(name,verts,fs,mi)

def tube(name,sections,n=10,mat=0):
    # Cross sections perpendicular to the anatomical centerline.
    verts=[]
    for i,(point,ra,rb) in enumerate(sections):
        tangent=Vector(sections[min(i+1,len(sections)-1)][0])-Vector(sections[max(i-1,0)][0]); tangent.normalize()
        axis=Vector((1,0,0))
        if abs(tangent.dot(axis))>.94: axis=Vector((0,1,0))
        u=(axis-tangent*axis.dot(tangent)).normalized(); v=tangent.cross(u).normalized()
        for j in range(n):
            t=2*math.pi*j/n; verts.append(Vector(point)+u*(math.cos(t)*ra)+v*(math.sin(t)*rb))
    faces=[tuple(range(n-1,-1,-1))]
    for k in range(len(sections)-1):
        for j in range(n): faces.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    faces.append(tuple((len(sections)-1)*n+j for j in range(n)))
    add(name,verts,faces,mat)

def ellipsoid(name,c,r,n=10,rings=5,mat=0):
    verts=[(c[0],c[1],c[2]-r[2])]
    for i in range(1,rings):
        a=-math.pi/2+math.pi*i/rings
        for j in range(n):
            t=2*math.pi*j/n; verts.append((c[0]+r[0]*math.cos(a)*math.cos(t),c[1]+r[1]*math.cos(a)*math.sin(t),c[2]+r[2]*math.sin(a)))
    top=len(verts); verts.append((c[0],c[1],c[2]+r[2])); faces=[]
    for j in range(n): faces.append((0,1+(j+1)%n,1+j))
    for k in range(rings-2):
        for j in range(n): faces.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
    for j in range(n): faces.append((top,1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n))
    add(name,verts,faces,mat)

def wedge(name,y,z,length,width,height,mat=3):
    # Nasal/scute ridge: laterally compressed, rounded low profile, never sail.
    loft_y(name,[(0,y-length*.50,z,width*.72,.018),(0,y-length*.24,z+height*.34-.018,width,height*.40+.018),(0,y+length*.08,z+height*.40-.018,width*.68,height*.48+.018),(0,y+length*.50,z,width*.30,.012)],n=8,mat=mat)

# Continuous ribcage, hips and long muscular tail, not an assembly of spheres.
loft_y('trunk-and-balancing-tail',[
 (0,-1.03,1.88,.25,.35),(0,-.78,1.78,.36,.47),(0,-.40,1.68,.47,.56),(0,.00,1.67,.50,.58),(0,.40,1.70,.43,.52),
 (0,.70,1.73,.32,.36),(.01,1.03,1.70,.245,.275),(.03,1.43,1.63,.19,.22),(.07,1.85,1.53,.145,.175),(.12,2.27,1.43,.109,.134),
 (.18,2.68,1.36,.077,.098),(.22,3.04,1.35,.050,.065),(.22,3.35,1.39,.027,.038),(.18,3.60,1.44,.010,.016),(.15,3.70,1.47,.002,.003)],n=12,belly=True)
# Strong but short S neck merges into the chest and occiput.
tube('cervical-column-and-musculature',[((0,-.90,1.83),.30,.36),((0,-1.16,2.02),.27,.31),((0,-1.36,2.24),.235,.30),((0,-1.48,2.36),.23,.25)],n=12)
# Deep muzzle, rear skull and lower jaw, broad constraints from MWC 1 Plate 1.
loft_y('deep-skull',[(0,-2.30,2.325,.135,.190),(0,-2.20,2.35,.19,.225),(0,-1.98,2.36,.235,.245),(0,-1.76,2.365,.277,.255),(0,-1.52,2.385,.285,.245),(0,-1.36,2.38,.215,.19)],n=12,power=.78)
loft_y('lower-jaw',[(0,-2.28,2.065,.125,.035),(0,-2.14,2.045,.18,.058),(0,-1.90,2.035,.23,.075),(0,-1.65,2.065,.255,.095),(0,-1.39,2.19,.19,.12)],n=10,mat=1,power=.8)
# Narrow oral seam remains embedded and connected, no floating teeth.
for s,label in [(-1,'left'),(1,'right')]:
    tube(label+'-mouth-line',[((s*.140,-2.27,2.125),.009,.012),((s*.199,-2.12,2.102),.010,.014),((s*.246,-1.91,2.105),.011,.016),((s*.273,-1.70,2.135),.010,.014),((s*.238,-1.44,2.21),.008,.010)],n=6,mat=4)
    # Small restrained lip-visible ivory teeth rooted in the maxillary margin.
    for i,y in enumerate([-2.12,-2.01,-1.90,-1.79]):
        x=s*(.205+.022*i); z=2.118+.007*i
        tube(label+'-tooth-'+str(i),[((x,y,z),.012,.018),((x,y-.004,z-.034),.003,.004)],n=5,mat=5)
    # Eye sockets and eyeballs are sunk into the cheek, with a narrow gold iris.
    ellipsoid(label+'-orbital-surround',(s*.276,-1.585,2.455),(.023,.085,.072),n=10,rings=5,mat=4)
    ellipsoid(label+'-eye',(s*.291,-1.592,2.462),(.015,.041,.038),n=10,rings=5,mat=5)
    ellipsoid(label+'-pupil',(s*.304,-1.601,2.465),(.007,.016,.026),n=8,rings=4,mat=4)
    ellipsoid(label+'-nostril',(s*.185,-2.165,2.440),(.009,.035,.020),n=8,rings=4,mat=4)
    # Paired low lacrimal brows, physically separated from central nasal horn.
    tube(label+'-lacrimal-brow',[((s*.248,-1.73,2.55),.050,.055),((s*.262,-1.66,2.635),.044,.050),((s*.251,-1.56,2.60),.028,.036)],n=8,mat=3)
wedge('single-compressed-nasal-horn',-2.02,2.585,.32,.060,.185,mat=3)
# Conservative low midline osteoderms, not a sail or plate armor.
for i,(y,z,length,height,width) in enumerate([(-1.08,2.33,.13,.052,.040),(-.82,2.255,.15,.063,.046),(-.55,2.245,.16,.064,.048),(-.25,2.25,.17,.065,.050),(.06,2.26,.17,.066,.050),(.36,2.22,.16,.064,.047),(.67,2.095,.15,.057,.043),(1.00,1.965,.14,.051,.038),(1.34,1.885,.12,.045,.033),(1.68,1.77,.11,.040,.027),(2.02,1.645,.10,.035,.024)]):
    wedge('dorsal-ossicle-%02d'%i,y,z,length,width,height,mat=2)
# Weight-bearing hind limbs. Slight stagger, knees forward and hocks rearward.
for s,label,dy in [(-1,'left',.075),(1,'right',-.075)]:
    tube(label+'-hindlimb',[((s*.34,.25+dy,1.70),.285,.31),((s*.48,.10+dy,1.37),.265,.29),((s*.53,-.14+dy,1.00),.185,.205),((s*.52,-.06+dy,.85),.14,.15),((s*.49,.28+dy,.48),.095,.11),((s*.48,.32+dy,.30),.078,.090),((s*.48,.15+dy,.115),.078,.082)],n=12)
    ellipsoid(label+'-ankle-pad',(s*.48,.10+dy,.105),(.12,.16,.105),n=10,rings=5,mat=0)
    for k,spread in enumerate([-.145,0,.145]):
        endy=(-.43 if k==1 else -.35)+dy
        tube(label+'-pedal-digit-'+str(k+2),[((s*.48+spread*.28,.09+dy,.12),.057,.055),((s*.48+spread*.72,-.12+dy,.075),.045,.05),((s*.48+spread,endy+.065,.055),.032,.035)],n=8)
        tube(label+'-pedal-claw-'+str(k+2),[((s*.48+spread,endy+.08,.058),.034,.038),((s*.48+spread,endy-.02,.035),.018,.020),((s*.48+spread,endy-.065,.018),.002,.003)],n=7,mat=3)
    # Small raised hallux, distinct from three primary forward ground toes.
    tube(label+'-hallux',[((s*.41,.13+dy,.16),.024,.028),((s*.37,.24+dy,.10),.014,.017),((s*.36,.27+dy,.075),.003,.004)],n=6,mat=3)
    # Arms held adducted; palms face inward, fingers flex down rather than pronate.
    tube(label+'-short-forelimb',[((s*.34,-.80,1.85),.14,.17),((s*.47,-.72,1.58),.11,.12),((s*.50,-.67,1.42),.075,.085),((s*.49,-.91,1.28),.061,.07),((s*.49,-.98,1.24),.065,.082)],n=10)
    ellipsoid(label+'-inward-facing-palm',(s*.49,-.97,1.245),(.058,.11,.070),n=8,rings=4,mat=0)
    for k in range(3):
        # Digit axes distributed along the palm's fore-aft plane.
        y=-1.035+.066*k; z=1.22-.012*k
        tube(label+'-manual-main-digit-'+str(k+1),[((s*.492,y,z),.028,.030),((s*.485,y-.035,z-.11+(k==2)*.025),.020,.022),((s*.445,y-.07,z-.15+(k==2)*.03),.012,.014)],n=7)
        tube(label+'-manual-claw-'+str(k+1),[((s*.445,y-.07,z-.14+(k==2)*.03),.016,.018),((s*.412,y-.10,z-.16+(k==2)*.03),.002,.003)],n=6,mat=3)
    tube(label+'-reduced-manual-fourth-nub',[((s*.49,-.89,1.265),.022,.025),((s*.485,-.86,1.220),.014,.015),((s*.475,-.865,1.205),.004,.005)],n=7)

# Origin at intended footprint center; the lowest soft plantar pads touch Z=0.
for mi in range(len(mats)):
    if not F[mi]: continue
    # Remove unused vertices from split-color shell components before export.
    used=sorted(set(v for f in F[mi] for v in f)); remap={v:i for i,v in enumerate(used)}
    obj=mesh_object(list(palette)[mi],[V[mi][v] for v in used],[tuple(remap[v] for v in f) for f in F[mi]],mats[mi],C)
    for name,start,num in SEM[mi]:
        ids=[remap[i] for i in range(start,start+num) if i in remap]
        if ids: obj.vertex_groups.new(name=name).add(ids,1,'REPLACE')
    obj['semantic_parts']=[q[0] for q in SEM[mi]]
# Recalculate normals on joined palette surfaces; split strips are intentionally
# open boundaries only at material seams and together form a continuous shell.
policy=P['geometry_policy']
with tempfile.TemporaryDirectory(prefix='ceratosaurus-export-',dir=str(OUT)) as temp:
    record=export_asset('ceratosaurus',{'en':'Ceratosaurus','zh':'角鼻龙'},'dinosaurs',C,output_root=Path(temp),render=False,max_triangles=policy['max_triangles'],max_materials=policy['max_materials'],max_primitives=policy['max_primitives'],metadata={'generator':'source/generate.py','description':{'en':'Original whole-animal Ceratosaurus reconstruction with a low nasal horn, paired brow relief, small midline ossicles, and reduced fourth manual digits.','zh':'原创角鼻龙全身重建：低鼻角、双眉隆起、细小背中线骨饰及退化第四手指。'},'reconstruction_notes':P['reconstruction_notes']})
    build=Path(temp)/'ceratosaurus'
    shutil.copy2(build/'ceratosaurus.glb',OUT/'model.glb'); shutil.copy2(build/'ceratosaurus.blend',OUT/'model.blend')
    qa=json.loads((build/'qa.json').read_text())
    record.update(glb='model.glb',blend='model.blend',preview='preview.png')
    record['semantic_sha256']=qa['glb']['semantic_sha256']
    record['params_sha256']=hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()
    record['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    record['scale_note']='Six-metre genus-level artistic scale, NOT measured MWC 1 specimen length.'
    record['source_editing']='Six material meshes with named anatomical vertex groups; contiguous material seams and overlapping separately closed anatomical components.'
    record['glb_exporter_version']='4.3.47'
    (OUT/'build-metadata.json').write_text(json.dumps(record,indent=2)+'\n')
    (OUT/'build-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
if (OUT/'model.glb').stat().st_size>policy['max_glb_bytes']: raise RuntimeError('GLB byte budget exceeded')
print('CERATOSAURUS_BUILD_COMPLETE '+json.dumps({'triangles':record['triangles'],'glb_sha256':record['sha256']['glb'],'semantic_sha256':record['semantic_sha256']}))
