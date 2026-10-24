# SPDX-License-Identifier: MIT
"""Original complete Dromornis planei reconstruction, Blender 4.3.2.
Canonical command from bundle root:
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output .
Only relative source/deps and params.json are needed; no borrowed skull mesh.
Fossil plates establish form, not a measured complete living individual.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
P=json.loads((HERE/'params.json').read_text())
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
C=setup_scene('dromornis',P['seed']);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
bpy.context.scene.render.filepath='//renders/'
M={k:make_material('dromornis-'+k,c,roughness=.88 if k!='eye' else .45) for k,c in P['palette_srgb'].items()};semantic=[]
def part(name,v,f,m):
    o=mesh_object(name,v,f,m,C);semantic.append(name);return o

def loft_y(name,rings,n,mat):
    # Explicit profile: y, center z, lateral radius, vertical radius.
    v=[(rx*math.cos(2*math.pi*i/n),y,z+rz*math.sin(2*math.pi*i/n)) for y,z,rx,rz in rings for i in range(n)]
    f=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(rings)-1) for i in range(n)]
    f += [tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+i for i in range(n))]
    return part(name,v,f,mat)

def loft_z(name,rings,n,mat):
    v=[(rx*math.cos(2*math.pi*i/n),y+ry*math.sin(2*math.pi*i/n),z) for z,y,rx,ry in rings for i in range(n)]
    f=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(rings)-1) for i in range(n)]
    f += [tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+i for i in range(n))]
    return part(name,v,f,mat)

def tube(name,points,radii,mat,n=12):
    v=[];previous=None
    for j,(p,rr) in enumerate(zip(points,radii)):
        p=Vector(p);t=(Vector(points[min(j+1,len(points)-1)])-Vector(points[max(j-1,0)])).normalized()
        u=t.cross(Vector((0,0,1)))
        if u.length<.001:u=t.cross(Vector((0,1,0)))
        u.normalize()
        if previous is not None and previous.dot(u)<0:u=-u
        previous=u.copy();w=t.cross(u).normalized();rx,rz=rr if isinstance(rr,tuple) else (rr,rr)
        for i in range(n):v.append(tuple(p+rx*math.cos(2*math.pi*i/n)*u+rz*math.sin(2*math.pi*i/n)*w))
    f=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(points)-1) for i in range(n)]
    f += [tuple(range(n-1,-1,-1)),tuple((len(points)-1)*n+i for i in range(n))]
    return part(name,v,f,mat)

def ellipsoid(name,center,radii,mat,n=14,r=8):
    v=[(center[0],center[1],center[2]-radii[2])]
    for j in range(1,r):
        phi=-math.pi/2+math.pi*j/r
        for i in range(n):
            t=2*math.pi*i/n;v.append((center[0]+radii[0]*math.cos(phi)*math.cos(t),center[1]+radii[1]*math.cos(phi)*math.sin(t),center[2]+radii[2]*math.sin(phi)))
    v.append((center[0],center[1],center[2]+radii[2]));f=[(0,1+(i+1)%n,1+i) for i in range(n)]
    for j in range(r-2):
        for i in range(n):f.append((1+j*n+i,1+j*n+(i+1)%n,1+(j+1)*n+(i+1)%n,1+(j+1)*n+i))
    for i in range(n):f.append((1+(r-2)*n+i,1+(r-2)*n+(i+1)%n,len(v)-1))
    return part(name,v,f,mat)

# A deep heavy feathered torso; deliberately not the thin body of a cursorial ostrich.
body=loft_y('body-deep-feather-mantle',[
(-.47,1.37,.015,.025),(-.43,1.35,.13,.20),(-.33,1.31,.23,.33),(-.17,1.27,.30,.43),
(.03,1.28,.325,.47),(.23,1.30,.305,.44),(.41,1.33,.25,.355),(.56,1.35,.16,.22),(.65,1.35,.045,.075)],24,[M['feathers'],M['belly']])
for face in body.data.polygons:
    if face.center.z<1.17 and face.center.y<.36:face.material_index=1
# Long substantial S neck, fully lofted. Lower neck feathers merge into deep breast.
loft_z('neck-long-substantial-s-curve',[
(1.19,-.17,.135,.15),(1.32,-.26,.178,.195),(1.43,-.31,.185,.205),(1.61,-.37,.143,.17),(1.79,-.38,.112,.135),
(1.96,-.365,.101,.12),(2.11,-.385,.101,.115),(2.23,-.43,.112,.106),(2.34,-.475,.104,.085)],20,M['neck'])
# Short tall soft-tissue cranium. Independent original loft, not a Genyornis skull reuse.
loft_y('head-massive-tall-cranium',[
(-.645,2.355,.074,.105),(-.61,2.367,.105,.125),(-.55,2.365,.116,.135),
(-.49,2.35,.111,.13),(-.43,2.325,.080,.105),(-.40,2.31,.026,.044)],20,M['neck'])
# Curved deep upper bill. Hemispherical dorsal profile is fossil-backed; no damage-derived casque.
# Maximum width .21 m is an estimated fleshed reconstruction, not the compressed fossil width.
# The culmen descends to a short blunt tip rather than a long spear or predatory hook.
loft_y('bill-deep-rounded-upper-rostrum',[
(-.88,2.255,.014,.018),(-.862,2.29,.043,.052),(-.83,2.335,.069,.095),
(-.79,2.37,.086,.130),(-.74,2.377,.100,.143),(-.685,2.371,.105,.139),
(-.635,2.356,.103,.124),(-.60,2.34,.095,.105)],20,M['bill'])
# Robust lower jaw follows upper tomial edge; commissure is a small overlap shadow.
loft_y('jaw-strong-lower-mandible',[
(-.869,2.230,.014,.010),(-.843,2.213,.046,.018),(-.79,2.196,.074,.032),
(-.72,2.186,.090,.043),(-.64,2.196,.098,.049),(-.57,2.218,.095,.058),
(-.505,2.246,.078,.058),(-.462,2.277,.045,.042)],18,M['bill'])
for s,label in [(-1,'left'),(1,'right')]:
    ellipsoid('eye-'+label,(s*.108,-.547,2.396),(.012,.018,.018),M['eye'],12,6)
    # Subtle lateral naris, cosmetic inference, not a cranial fenestra left open in the living bird.
    ellipsoid('nostril-'+label,(s*.101,-.660,2.395),(.0035,.012,.006),M['eye'],10,6)
    # Reduced wings barely project from mantle, restrained bird anatomy rather than arms.
    contour=[(-.10,1.49),(.01,1.53),(.16,1.50),(.31,1.39),(.37,1.29),(.27,1.265),(.08,1.31),(-.08,1.39)]
    outer=[.291,.314,.310,.284,.254,.297,.331,.309]
    vv=[(s*(outer[i]-.060),y,z) for i,(y,z) in enumerate(contour)]+[(s*outer[i],y,z) for i,(y,z) in enumerate(contour)]+[(s*.342,.10,1.414)]
    ff=[tuple(range(7,-1,-1))]
    for i in range(8):ff.extend([(i,(i+1)%8,(i+1)%8+8,i+8),(i+8,(i+1)%8+8,16)])
    part('wing-tiny-folded-'+label,vv,ff,M['feathers'])
    # Two long stout load-bearing legs; stagger subtly for anatomical leg separation in side view.
    dy=-.065 if s<0 else .065
    tube('thigh-feathered-'+label,[(s*.21,.06+dy,1.15),(s*.225,-.07+dy,.99),(s*.23,-.070+dy,.86),(s*.23,-.020+dy,.75)],[(.135,.17),(.115,.15),(.094,.115),(.075,.087)],M['feathers'],16)
    tube('leg-stout-scaled-'+label,[(s*.23,-.09+dy,.86),(s*.23,.08+dy,.60),(s*.22,.10+dy,.50),(s*.205,.06+dy,.25),(s*.205,.015+dy,.10)],[(.081,.093),(.063,.077),(.057,.064),(.052,.058),(.061,.054)],M['feet'],14)
    # Broad three forward toes, independently spread and round-sectioned. No webbing or mammal paws.
    fx=s*.205;fy=.015+dy
    for k,(spread,length) in enumerate([(-.105,.225),(0,.305),(.105,.24)]):
        end=(fx+spread,fy-length,.035)
        tube('toe-'+label+'-'+str(k+1),[(fx+spread*.10,fy-.016,.091),(fx+spread*.55,fy-length*.53,.045),end],[(.038,.032),(.031,.028),(.026,.022)],M['feet'],10)
        tube('claw-blunt-'+label+'-'+str(k+1),[(end[0],end[1]+.008,.036),(end[0]+spread*.14,end[1]-.046,.023)],[(.026,.023),(.012,.012)],M['bill'],10)
# Short feathered rump, not a long display fan.
tube('tail-short-feathered',[(0,.49,1.39),(0,.67,1.36),(0,.80,1.29)],[(.15,.14),(.105,.11),(.023,.038)],M['feathers'],14)
# One shared floor/footprint-origin translation. No per-part scaling or negative transforms.
feet=[o for o in C.objects if o.type=='MESH' and (o.name.startswith('toe-') or o.name.startswith('claw-'))]
min_z=min(v.co.z for o in C.objects if o.type=='MESH' for v in o.data.vertices)
footverts=[v.co for o in feet for v in o.data.vertices];centerx=(min(v.x for v in footverts)+max(v.x for v in footverts))/2;centery=(min(v.y for v in footverts)+max(v.y for v in footverts))/2
for o in C.objects:
    if o.type=='MESH':
        for v in o.data.vertices:v.co.x-=centerx;v.co.y-=centery;v.co.z-=min_z
bpy.context.view_layer.update()
meta={'generator':'source/generate.py','original_inventory_ordinal':688,'surface_profile':P['surface_profile'],'semantic_parts':semantic,
 'description':{'en':'Complete massive flightless Dromornis planei, with high deep curved bill, substantial long neck and stout long legs.','zh':'完整不飞鸟D. planei，保留高深弯喙、粗壮长颈和强健长腿。'},
 'scale_note':'Approximately 2.5 m standing is a species restoration estimate; 300 kg is not simulated mass. Cranial references are different specimens, not a measured complete individual. All modeled living proportions and colors are inferred.',
 'factual_limits':'P9464-106 is a 40 mm-bar braincase reference; P932-2 is a separate 50 mm-bar rostrum with distortion and cavitation. Extreme transverse compression and damaged surface are not reconstructed. No D. stirtoni measurements or illustration used.',
 'origin_note':'Identity root at center of the projected toe-and-claw footprint; lowest contact at Z=0.',
 'generator_seed':P['seed']}
# Clear factory UI directory buffers before saving an independently portable source.
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'.'*1023
                space.params.directory=b'//'
                space.params.filename='model.blend'
b=P['budgets'];rec=export_asset('dromornis',{'en':'Dromornis planei','zh':'普莱恩恐鸟'},'birds',C,metadata=meta,output_root=out/'private'/'build-output',render=False,max_triangles=b['max_triangles'],max_materials=b['max_materials'],max_primitives=b['max_primitives'])
stage=out/'private/build-output/dromornis'
for src,dst in [('dromornis.glb','model.glb'),('dromornis.blend','model.blend')]:shutil.copy2(stage/src,out/dst)
qa=json.loads((stage/'qa.json').read_text());qa['glb']['file']='model.glb';qa['delivery_names']={'glb':'model.glb','blend':'model.blend'}
qa['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();qa['parameters_sha256']=hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()
assert (out/'model.glb').stat().st_size<=b['max_glb_bytes']
(out/'qa/evidence').mkdir(parents=True,exist_ok=True);(out/'qa/evidence/technical.json').write_text(json.dumps(qa,indent=2)+'\n')
rec['glb']='model.glb';rec['blend']='model.blend';rec['preview']='preview.png';rec['mesh_parts']=semantic
(out/'qa/evidence/build-metadata.json').write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'BUILT','triangles':qa['glb']['scene_triangles'],'glb_sha256':qa['glb']['sha256']}))
