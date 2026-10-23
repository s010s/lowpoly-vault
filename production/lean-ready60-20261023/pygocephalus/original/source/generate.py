# SPDX-License-Identifier: MIT
"""Deterministic Pygocephalus complete living interpretation, not a fossil facsimile.
Run with Blender 4.3.2: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
All generator dependencies are packaged beside this file. Millimeter design coordinates
are converted to meters at mesh construction; no texture or external data is loaded.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,required=True)
out=ap.parse_args(args).out; out.mkdir(parents=True,exist_ok=True)
col=setup_scene('pygocephalus',P['seed']); root=bpy.data.objects[col['asset_root']]
root['taxon']='Pygocephalus; P. cooperi sensu Laville et al. 2026'
root['scope']='Complete Carboniferous living interpretation; species ornamentation and depth uncertain.'
root['mount']='Identity root at central walking-foot contact plane; animal forward -Y.'
colors={'shield':'#587265','rim':'#80937B','abdomen':'#7C8060','limbs':'#A49A70','underside':'#70765F','eyes':'#202B28'}
mats={k:make_material('Pygocephalus-'+k,v,roughness=.82) for k,v in colors.items()}
semantic=[]
def mesh(name,verts,faces,mat,category=None):
 obj=mesh_object(name,[tuple(c*.001 for c in v) for v in verts],faces,mats[mat],col)
 obj['semantic_part']=category or name; obj['reconstruction']='original regularized living geometry'
 semantic.append({'name':name,'category':category or name,'material':mat,'vertices':len(verts),'polygons':len(faces)})
 return obj

def tube(name,points,radii,mat='limbs',sides=7,category=None):
 vv=[]; ff=[]
 for i,p in enumerate(points):
  t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
  t.normalize(); ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((0,1,0))
  u=t.cross(ref).normalized(); v=t.cross(u).normalized()
  for j in range(sides):
   q=Vector(p)+radii[i]*(u*math.cos(j*math.tau/sides)+v*math.sin(j*math.tau/sides))
   vv.append(tuple(q))
  if i:
   for j in range(sides): ff.append(((i-1)*sides+j,(i-1)*sides+(j+1)%sides,i*sides+(j+1)%sides,i*sides+j))
 ff.extend([tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))])
 return mesh(name,vv,ff,mat,category)

def ellipsoid(name,center,scale,mat='limbs',n=12,rings=7,category=None):
 vv=[(center[0],center[1],center[2]-scale[2])]; ff=[]
 for k in range(1,rings):
  a=math.pi*k/rings
  for j in range(n):
   b=math.tau*j/n; vv.append((center[0]+scale[0]*math.sin(a)*math.cos(b),center[1]+scale[1]*math.sin(a)*math.sin(b),center[2]-scale[2]*math.cos(a)))
 vv.append((center[0],center[1],center[2]+scale[2])); last=len(vv)-1
 for j in range(n): ff.append((0,1+(j+1)%n,1+j))
 for k in range(rings-2):
  for j in range(n):
   a=1+k*n+j; b=1+k*n+(j+1)%n; ff.append((a,b,b+n,a+n))
 for j in range(n): ff.append((last,last-n+j,last-n+(j+1)%n))
 return mesh(name,vv,ff,mat,category)

def shield():
 # Measured total extent Ls=17.788 and Wm=20.310; posterior width Wp=9.993.
 right=[(0,-8.894),(3.6,-8.78),(6.9,-8.4),(8.65,-6.4),(9.85,-3.65),(10.155,-.5),(9.95,2.7),(8.65,5.6),(6.6,7.7),(4.9965,8.894),(2.5,7.95),(0,7.55)]
 outline=right+[(-x,y) for x,y in right[-2:0:-1]]
 # Add one midpoint on each edge for controlled broad panels.
 boundary=[]
 for i,p in enumerate(outline):
  q=outline[(i+1)%len(outline)]; boundary.extend([p,((p[0]+q[0])/2,(p[1]+q[1])/2)])
 n=len(boundary); vv=[(0,-.2,8.7)]; ff=[]
 for scale,z in ((.29,8.5),(.58,7.9),(.82,6.6),(1,4.35)):
  vv.extend((x*scale,y*scale,z+.12*math.cos(y*.35)) for x,y in boundary)
 for j in range(n): ff.append((0,1+j,1+(j+1)%n))
 for k in range(3):
  a=1+k*n; b=a+n
  for j in range(n): ff.append((a+j,b+j,b+(j+1)%n,a+(j+1)%n))
 underside=len(vv); vv.append((0,0,2.7))
 for j in range(n): ff.append((1+3*n+j,underside,1+3*n+(j+1)%n))
 ob=mesh('Shield-measured-GSC12858',vv,ff,'shield','carapace')
 ob['measured_shield_length_m']=P['shield_length']; ob['measured_shield_width_m']=P['shield_width']; ob['measured_posterior_width_m']=P['posterior_shield_width']
 # Rim is a narrow volume inside the same measured perimeter, not added width.
 vv=[]; ff=[]
 for scale,z in ((1,4.35),(.975,4.65),(.967,4.25),(.993,4.1)):
  vv.extend((x*scale,y*scale,z+.12*math.cos(y*.35)) for x,y in boundary)
 for k in range(4):
  for j in range(n): ff.append((k*n+j,k*n+(j+1)%n,((k+1)%4)*n+(j+1)%n,((k+1)%4)*n+j))
 mesh('Shield-subtle-perimeter-rim',vv,ff,'rim','carapace-rim')
 # Short straight rostrum, measured separately from shield.
 tube('Straight-rostrum-4.575mm',[(0,-8.894,4.65),(0,-10.9,4.7),(0,-13.469,4.62)],[.61,.36,.06],'rim',7,'rostrum')
 for s,label in ((-1,'L'),(1,'R')):
  tube('Anterolateral-spine-'+label,[(s*6.9,-8.4,4.4),(s*7.23,-9.15,4.35),(s*7.34,-9.735,4.3)],[.34,.2,.055],'rim',6,'paired-anterolateral-spine')
shield()
# Ventral thorax is broader posteriorly; the anterior two sternites are partly covered.
for i in range(8):
 y=-6.4+i*1.86; w=1.4+i*.43
 ellipsoid(f'Thoracic-sternite-{i+1:02}',(0,y,2.88),(w,.95,.61),'underside',12,6,'thoracic-sternite')
# Two compact feeding-associated limb pairs; do not replace them with long walking legs.
for s,label in ((-1,'L'),(1,'R')):
 for i in range(2):
  y=-7.0+i*1.8
  ellipsoid(f'Thoracopod-{i+1:02}-{label}-enlarged-base',(s*2.5,y,2.7),(1.55,.95,.8),'limbs',12,6,'compact-feeding-base')
  tube(f'Thoracopod-{i+1:02}-{label}-feeding-palp',[(s*3.1,y,2.8),(s*4.1,y-.5,2.5),(s*4.35,y-1.5,2.35),(s*3.0,y-2.0,2.3)],[.5,.4,.28,.12],'limbs',7,'compact-thoracopod')
 # Six walking pairs lengthen posteriorly, sweep outward and then back with clean gaps.
 for i in range(6):
  y=-3.75+i*1.82; reach=12.3+i*.63
  pts=[(s*(3.7+i*.18),y,3.0),(s*(7.7+i*.2),y-.9,3.25),(s*(reach-1.8),y-.65,3.1),(s*reach,y+1.05,1.8),(s*(reach+.7),y+3.15,0.22)]
  tube(f'Thoracopod-{i+3:02}-{label}-walking',pts,[.63,.53,.4,.28,.12],'limbs',8,'walking-thoracopod')
  ellipsoid(f'Thoracopod-{i+3:02}-{label}-joint',pts[2],(.43,.46,.42),'abdomen',10,6,'walking-joint')
# Continuous low ventral abdomen connects articulating shields without false fossil breaks.
ellipsoid('Pleonal-ventral-axis',(0,15.4,2.8),(3.35,9.3,.8),'underside',16,10,'continuous-pleonal-axis')
# Six compact broad pleonal tergites, with a low rounded arch and lateral pleura.
for i in range(6):
 yc=9.3+i*2.48; half=4.92-i*.19; h=1.58-i*.075; z=3.1-i*.07; length=2.65
 vv=[]; ff=[]; n=20
 for k,(offset,scale) in enumerate(((-length/2,.87),(-length*.34,1),(length*.30,.99),(length/2,.9))):
  for j in range(n):
   a=j*math.tau/n; x=half*scale*math.cos(a); zz=z+h*math.sin(a)
   if zz<z-.65: zz=z-.65
   vv.append((x,yc+offset,zz))
 for k in range(3):
  for j in range(n): ff.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 ff.extend([tuple(range(n-1,-1,-1)),tuple(3*n+j for j in range(n))])
 mesh(f'Pleon-tergite-{i+1:02}',vv,ff,'abdomen','pleonal-segment')
 # Trim highlights the trailing lip, with intentional attached overlaps.
 pts=[]
 for j in range(13):
  a=math.pi*j/12; pts.append((half*.91*math.cos(a),yc+length*.43,z+h*math.sin(a)+.05))
 tube(f'Pleon-{i+1:02}-trailing-rim',pts,[.14]*len(pts),'rim',6,'pleonal-rim')
 for s,label in ((-1,'L'),(1,'R')):
  ellipsoid(f'Pleon-{i+1:02}-{label}-pleuron',(s*half*.95,yc+.13,z-.15),(.59,1.0,.42),'abdomen',10,6,'pleural-flange')
# Broad flexible tail articulation avoids false broken-fossil windows at the last tergite.
mesh('Pleon-telson-articulation',[(-3.65,22.7,2.3),(3.65,22.7,2.3),(2.35,24.0,2.3),(-2.35,24.0,2.3),(-3.65,22.7,3.35),(3.65,22.7,3.35),(2.35,24.0,3.2),(-2.35,24.0,3.2)],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'underside','tail-articulation')
# Hexagonal telson body, distinct from the paired uropods and its TWO pairs of lobes.
poly=[(-2.15,23.55),(-2.75,25.25),(-1.9,28.0),(0,29.05),(1.9,28.0),(2.75,25.25),(2.15,23.55)]
vv=[(x,y,2.2) for x,y in poly]+[(x*.94,y,3.35 if y<27 else 2.95) for x,y in poly]; n=len(poly)
ff=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
mesh('Hexagonal-telson',vv,ff,'shield','telson')
for s,label in ((-1,'L'),(1,'R')):
 # Oval exopod/endopod paddles, not decapod pincers.
 for j,(x,y,rx,ry,angle) in enumerate(((4.45,26.1,1.7,3.6,-s*.28),(2.9,26.35,1.15,3.0,-s*.18))):
  ob=ellipsoid(f'Uropod-{label}-'+('exopod' if j==0 else 'endopod'),(s*x,y,2.48),(rx,ry,.39),'rim' if j==0 else 'abdomen',14,7,'uropod-blade')
  # Mesh-local rotation around blade center keeps identity object transforms.
  cx=s*x*.001; cy=y*.001
  for v in ob.data.vertices:
   dx=v.co.x-cx;dy=v.co.y-cy;v.co.x=cx+dx*math.cos(angle)-dy*math.sin(angle);v.co.y=cy+dx*math.sin(angle)+dy*math.cos(angle)
  tube(f'Uropod-{label}-{j+1}-root',[(s*3.45,22.4,2.8),(s*x,24.3,2.6)],[.45,.5],'abdomen',7,'uropod-base')
 for j,(x,y,rx,ry) in enumerate(((1.75,28.7,.55,1.13),(.72,29.3,.39,.96))):
  ellipsoid(f'Telson-lobe-pair-{j+1}-{label}',(s*x,y,2.52),(rx,ry,.35),'limbs',10,6,'telson-lobe-pair-'+str(j+1))
tube('Telson-central-terminal-spine',[(0,28.8,2.6),(0,30.15,2.5),(0,30.55,2.48)],[.25,.14,.045],'rim',6,'central-terminal-spine')
# Antennules + antennae are separate paired systems; eye form is conservative inference.
for s,label in ((-1,'L'),(1,'R')):
 tube('Eyestalk-'+label,[(s*2.3,-7.5,4.7),(s*3.5,-9.45,5.0)],[.46,.38],'rim',7,'eyestalk-inferred')
 ellipsoid('Small-eye-'+label,(s*3.65,-9.65,5.05),(.68,.68,.56),'eyes',12,7,'eye-inferred')
 ellipsoid('Scaphocerite-'+label,(s*5.1,-10.5,3.65),(1.13,2.5,.4),'limbs',14,7,'scaphocerite')
 tube('Antennule-peduncle-'+label,[(s*1.2,-7.8,4.0),(s*1.45,-10.0,4.3),(s*1.8,-11.5,4.65)],[.44,.34,.25],'limbs',7,'antennule-peduncle')
 for j,dx in enumerate((.5,2.0)):
  tube(f'Antennule-{label}-flagellum-{j+1}',[(s*1.8,-11.5,4.65),(s*(2.3+dx*.4),-15.0,5.0),(s*(2.7+dx),-18.2,5.3),(s*(3.0+dx*1.5),-20.0,5.5)],[.18,.14,.1,.055],'limbs',6,'antennule-flagellum')
 tube('Antenna-peduncle-'+label,[(s*4.5,-7.6,3.7),(s*6.7,-10.2,4.0),(s*8.1,-11.0,4.1)],[.48,.36,.26],'limbs',7,'antenna-peduncle')
 tube('Long-curved-antenna-'+label,[(s*8.1,-11,4.1),(s*10.6,-10.7,4.5),(s*12.9,-8.9,4.6),(s*14.6,-5.4,4.2),(s*15.5,-1.1,3.8),(s*15.95,4.1,3.4),(s*16.1,9.7,2.9),(s*15.9,14.7,2.3)],[.26,.24,.22,.2,.18,.15,.115,.06],'limbs',7,'long-antenna-flagellum')
# Ground contact is established by the twelve walking tips; shift all vertices evenly.
lowest=min(v.co.z for o in col.objects if o.type=='MESH' for v in o.data.vertices)
for obj in col.objects:
 if obj.type=='MESH':
  for v in obj.data.vertices: v.co.z-=lowest
bpy.context.view_layer.update()
source=audit_source(col,40000)
if source['errors']: raise RuntimeError(json.dumps(source['errors']))
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
 for area in screen.areas:
  for space in area.spaces:
   if space.type=='FILE_BROWSER' and space.params:
    space.params.directory=b'//' + b' '*1020
    space.params.directory=b'//'
# Public blend retains semantic parts, without path-bearing Text blocks or camera rig.
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),check_existing=False)
# Group only a temporary export copy by material. Source remains fully editable.
exp=bpy.data.collections.new('EXPORT_BATCHED'); bpy.context.scene.collection.children.link(exp)
exp_root=bpy.data.objects.new('pygocephalus-export-root',None);exp.objects.link(exp_root)
for k in mats:
 vv=[];ff=[]
 for obj in col.objects:
  if obj.type!='MESH' or obj.data.materials[0]!=mats[k]: continue
  offset=len(vv);vv.extend(tuple(obj.matrix_world@v.co) for v in obj.data.vertices)
  ff.extend(tuple(offset+v for v in p.vertices) for p in obj.data.polygons)
 m=bpy.data.meshes.new('Pygocephalus-'+k+'-batched');m.from_pydata(vv,[],ff);m.update();m.materials.append(mats[k])
 o=bpy.data.objects.new('Pygocephalus-'+k,m);exp.objects.link(o);o.parent=exp_root
bpy.ops.object.select_all(action='DESELECT')
for o in exp.objects:o.select_set(True)
bpy.context.view_layer.objects.active=exp_root
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
assert not set(options)-available
bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
glb=audit_glb(out/'model.glb',40000,6,8);glb['file']='model.glb'
assert not glb['errors'],glb['errors'];assert glb['materials']<=6;assert glb['scene_primitives_estimated_base_draw_calls']<=8;assert glb['bytes']<=8388608
b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-target[i]) for side,target in [('min',emin),('max',emax)] for i in range(3))
assert delta<1e-7;assert glb['scene_triangles']==source['triangles']
def write(name,data): (out/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
write('build-report.json',{'status':'PASS','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'export_options':options,'palette_srgb':colors,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'seed':P['seed'],'semantic_parts':semantic,'anatomy_counts':{'thoracic_appendage_pairs':8,'compact_feeding_pairs':2,'walking_pairs':6,'pleonal_segments':6,'uropod_blades_per_side':2,'telson_lobe_pairs':2,'anterior_antennal_system_pairs':2},'ground_shift_m':-lowest,'scope':'Source mesh integrity and exact standalone GLB structure; not independent visual, GPU or populated-scene approval.'})
print('BUILD COMPLETE',glb['sha256'],glb['scene_triangles'])
