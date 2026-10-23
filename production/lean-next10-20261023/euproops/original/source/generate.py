#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original deterministic Euproops danae stage-3 reconstruction. All coordinates below are mm before conversion to SI meters."""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def write(p,d): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=HERE.parent); args=ap.parse_args(argv); out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
P=json.loads((HERE/'params.json').read_text()); C=setup_scene('euproops',P['seed'])
M={k:make_material(k,v,roughness=.84 if k!='eyes' else .48) for k,v in {'carapace':'#6D533B','ridges':'#57412E','limbs':'#9A7953','ventral':'#826647','eyes':'#211C16'}.items()}

class Mesh:
 def __init__(self,name,mat): self.name=name; self.mat=mat; self.v=[]; self.f=[]; self.groups={}
 def add(self,name,v,f):
  start=len(self.v); self.v.extend(v); self.f.extend([tuple(i+start for i in face) for face in f]); self.groups[name]=list(range(start,len(self.v)))
 def emit(self):
  obj=mesh_object(self.name,[tuple(c*.001 for c in v) for v in self.v],self.f,M[self.mat],C)
  for name,inds in self.groups.items(): obj.vertex_groups.new(name=name).add(inds,1,'REPLACE')
  obj['semantic_components']=list(self.groups); obj['construction_units']='millimeters converted to meters'; return obj

def inside(x,y,poly):
 hit=False
 for i,(a,b) in enumerate(poly):
  c,d=poly[(i+1)%len(poly)]
  if (b>y)!=(d>y) and x<(c-a)*(y-b)/(d-b)+a: hit=not hit
 return hit

def shell(mesh,name,poly,ztop,zbottom,spacing=.5):
 points=[Vector(p) for p in poly]; n=len(points)
 for j in range(int(min(p[1] for p in poly)/spacing)-1,int(max(p[1] for p in poly)/spacing)+2):
  y=j*spacing
  for i in range(int(min(p[0] for p in poly)/spacing)-1,int(max(p[0] for p in poly)/spacing)+2):
   x=i*spacing+(j%2)*spacing*.5
   if inside(x,y,poly) and all((x-a)**2+(y-b)**2>.065**2 for a,b in poly): points.append(Vector((x,y)))
 vs,es,fs,_,_,_=delaunay_2d_cdt(points,[(i,(i+1)%n) for i in range(n)],[list(range(n))],1,1e-6)
 # All CDT interior triangles + mirrored bottom skin; boundary edges locate walls.
 top=[(v.x,v.y,ztop(v.x,v.y)) for v in vs]; bot=[(v.x,v.y,zbottom(v.x,v.y)) for v in vs]; N=len(vs)
 faces=[tuple(f) for f in fs]+[tuple(N+i for i in reversed(f)) for f in fs]
 counts={}
 for f in fs:
  for a,b in zip(f,tuple(f[1:])+tuple(f[:1])): counts[tuple(sorted((a,b)))]=counts.get(tuple(sorted((a,b))),0)+1
 for (a,b),c in counts.items():
  if c==1: faces.append((a,b,N+b,N+a))
 mesh.add(name,top+bot,faces)

def tube(mesh,name,path,radii,sides=8,flatten=1.):
 v=[]; f=[]
 for i,p in enumerate(path):
  p=Vector(p); tangent=(Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])).normalized(); ref=Vector((0,0,1))
  if abs(tangent.dot(ref))>.95: ref=Vector((0,1,0))
  a=tangent.cross(ref).normalized(); b=tangent.cross(a).normalized()
  for k in range(sides):
   t=2*math.pi*k/sides; q=p+radii[i]*(math.cos(t)*a+flatten*math.sin(t)*b); v.append(tuple(q))
 for i in range(len(path)-1):
  for j in range(sides): a=i*sides+j; b=i*sides+(j+1)%sides; f.append((a,b,b+sides,a+sides))
 f += [tuple(reversed(range(sides))),tuple((len(path)-1)*sides+j for j in range(sides))]
 mesh.add(name,v,f)

def ellipsoid(mesh,name,center,radii,n=12,rings=5):
 # No duplicated poles; coarse intentional faceting.
 v=[(center[0],center[1],center[2]+radii[2])]
 for j in range(1,rings):
  p=math.pi*j/rings
  for i in range(n):
   t=2*math.pi*i/n; v.append((center[0]+radii[0]*math.sin(p)*math.cos(t),center[1]+radii[1]*math.sin(p)*math.sin(t),center[2]+radii[2]*math.cos(p)))
 south=len(v); v.append((center[0],center[1],center[2]-radii[2])); f=[]
 for i in range(n): f.append((0,1+i,1+(i+1)%n))
 for j in range(rings-2):
  for i in range(n): a=1+j*n+i; b=1+j*n+(i+1)%n; f.append((a,a+n,b+n,b))
 for i in range(n): f.append((south,1+(rings-2)*n+(i+1)%n,1+(rings-2)*n+i))
 mesh.add(name,v,f)

# Fig.1C hand-traced outline. The posterior genal points are integral to the closed prosomal shield.
right=[(0,-6.9),(1.56,-6.72),(3.42,-6.18),(5.16,-5.28),(6.60,-4.08),(7.56,-2.52),(8.16,-.54),(8.4,1.92),(8.34,4.50),(7.92,2.22),(7.32,0),(6.84,-1.02),(6.42,-1.20),(4.80,-.72),(2.82,.06),(0,0)]
propoly=right+[(-x,y) for x,y in reversed(right[1:-1])]
def pro_z(x,y):
 dome=max(0,1-(x/8.4)**2)*max(0,1-((y+2.7)/4.9)**2)
 return 1.05+1.84*dome if y<1.2 else max(.87,1.05-.04*(y-1.2))
pro=Mesh('01_prosoma_with_genal_spines','carapace'); shell(pro,'broad_prosoma_and_two_genal_spines',propoly,pro_z,lambda x,y:.82 if y<1.2 else .73,spacing=.45); pro.emit()
# Seven uneven paired radial epimera trace the published juvenile restoration; no adult solid flange.
r=[(613,177),(657,182),(688,193),(735,234),(693,215),(728,254),(692,233),(710,273),(682,248),(692,289),(665,261),(674,299),(647,271),(651,298),(633,273),(627,299),(613,274)]
r=[((x-613)*5.6/122,(y-177)*7.3/122) for x,y in r]; postpoly=r+[(-x,y) for x,y in reversed(r[1:-1])]
def post_z(x,y):
 q=max(0,1-(x/5.6)**2)*max(0,1-((y-2.9)/4.5)**2)
 z=1.08+1.05*q
 # Shallow surface grooves, not gaps separating movable plates.
 for mid in (1.1,2.0,2.9,3.8,4.65,5.35):
  line=mid+.27*(x/4.5)**2; z-=.073*math.exp(-((y-line)/.10)**2)*max(0,1-(abs(x)/5.2)**4)
 return z
post=Mesh('02_fused_thoracetron_with_radial_epimera','carapace'); shell(post,'fused_posterior_shield_7_paired_epimera',postpoly,post_z,lambda x,y:.80,spacing=.34); post.emit()
# Long ocular ridges terminate in fine backward spines, separate from lateral genal spines.
ridges=Mesh('03_ophthalmic_ridges_and_spines','ridges')
for s,side in [(-1,'left'),(1,'right')]:
 path=[(s*2.80,-2.95,pro_z(2.8,-2.95)+.10),(s*2.78,-2,pro_z(2.78,-2)+.13),(s*2.70,-.8,pro_z(2.7,-.8)+.13),(s*2.60,.5,2.53),(s*2.48,2.1,2.35),(s*2.43,3.95,2.02)]
 tube(ridges,side+'_ophthalmic_ridge_spine',path,[.24,.25,.22,.17,.11,.04],8,.55)
# Shallow, low-contrast transverse segment traces stay on one fused shield.
for j,(mid,width) in enumerate([(1.1,3.25),(2.0,4.0),(2.9,4.05),(3.8,3.55),(4.65,2.8),(5.35,1.65)]):
 path=[]
 for k in range(17):
  x=-width+2*width*k/16; y=mid+.27*(x/4.5)**2; path.append((x,y,post_z(x,y)+.045))
 tube(ridges,'thoracetron_shallow_segment_'+str(j+1),path,[.065]*len(path),6,.45)
ridges.emit()
eyes=Mesh('04_paired_lateral_eyes','eyes')
for s,side in [(-1,'left'),(1,'right')]: ellipsoid(eyes,side+'_small_lateral_eye',(s*2.85,-2.96,pro_z(2.85,-2.96)+.16),(.19,.24,.13),10,4)
eyes.emit()
tel=Mesh('05_straight_styliform_telson','carapace'); origin=7.3*(274-177)/122
# A long continuous taper, neither tucked abdomen nor raised sting.
tube(tel,'telson_7_9_mm',[(0,origin,1.11),(0,origin+1.20,1.00),(0,origin+4.2,.73),(0,origin+7.90,.32)],[.34,.28,.16,.04],8,.62); tel.emit()
legs=Mesh('06_six_pairs_prosomal_appendages','limbs'); limb_records=[]
for s,side in [(-1,'left'),(1,'right')]:
 # Small pre-oral chelicera, not an additional walking leg.
 pts=[(s*.43,-3.15,.98),(s*.68,-3.70,.72),(s*.68,-4.12,.60)]
 tube(legs,side+'_pair1_chelicera',pts,[.18,.16,.10],7)
 for finger in (-1,1): tube(legs,side+'_chelicera_finger_'+str(finger),[(s*.68+finger*.07,-4.08,.60),(s*.68+finger*.12,-4.36,.53),(s*.68+finger*.025,-4.46,.51)],[.07,.055,.025],6)
 limb_records.append({'side':side,'pair':1,'kind':'chelicera'})
 configurations=[(-2.55,-3.6,-4.6,4.45),(-1.65,-1.9,-2.6,5.65),(-.75,-.30,.1,6.15),(.15,1.3,2.5,5.85)]
 for i,(rooty,kneey,endy,width) in enumerate(configurations,2):
  pts=[(s*.83,rooty,1.01),(s*2.1,rooty+.08,.86),(s*(width*.74),kneey,.64),(s*width,endy,.22),(s*(width-.25),endy+.25,.10)]
  tube(legs,side+'_pair'+str(i)+'_walking',pts,[.25,.28,.22,.15,.10],8)
  # Modest small terminal chela, with clearly separated fingers.
  for finger in(-1,1): tube(legs,side+'_walking'+str(i)+'_finger'+str(finger),[(s*(width-.25)+finger*.07,endy+.23,.11),(s*(width-.42)+finger*.12,endy+.48,.07),(s*(width-.48)+finger*.035,endy+.61,.04)],[.075,.06,.025],6)
  limb_records.append({'side':side,'pair':i,'kind':'walking'})
 pts=[(s*.92,1.0,1.0),(s*2.5,1.55,.9),(s*4.35,3.20,.52),(s*4.85,4.55,.19)]
 tube(legs,side+'_pair6_pusher',pts,[.30,.32,.26,.16],8)
 # Conservative distal expanded pusher lobes, not speculative detailed leaf anatomy.
 for j in (-1,0,1): tube(legs,side+'_pusher_lobe'+str(j),[(s*4.85,4.48,.20),(s*(4.95+j*.18),4.86,.14),(s*(4.94+j*.22),5.15,.07)],[.11,.14,.045],7,.50)
 limb_records.append({'side':side,'pair':6,'kind':'pushing'})
legs.emit()
belly=Mesh('07_understated_ventral_body','ventral'); ellipsoid(belly,'prosomal_sternum',(0,-1.35,.94),(1.3,2.45,.34),16,6); ellipsoid(belly,'posterior_ventral_body',(0,3.0,.85),(2.7,2.55,.20),20,5); belly.emit()
# Floor contact is determined by the lowest walking fingertip, not by shell centering.
meshes=[o for o in C.objects if o.type=='MESH']; low=min(v.co.z for o in meshes for v in o.data.vertices)
for o in meshes:
 for v in o.data.vertices: v.co.z-=low
source=audit_source(C,max_triangles=40000)
write(out/'qa/evidence/source.json',source)
if source['errors']: raise RuntimeError('Source audit failed: '+repr(source['errors']))
bpy.context.scene['asset_author']='Leon Made This / s010s'; bpy.context.scene['asset_license']='CC-BY-4.0'; bpy.context.scene['reconstruction_scope']='YPM IP168040 likely stage 3; text dimensions, not conflicting printed scale bar; appendage detail inferred.'
bpy.context.preferences.filepaths.save_version=0; bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.objects: o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(opts)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing: raise RuntimeError('Missing exporter flags: '+repr(missing))
bpy.ops.export_scene.gltf(**opts)
qa=audit_glb(out/'model.glb',max_triangles=40000,max_materials=6,max_primitives=8)
write(out/'qa/evidence/glb-audit.json',qa)
if qa['errors']: raise RuntimeError('GLB audit failed: '+repr(qa['errors']))
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}; delta=max(abs(qa['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
assert delta<1e-7 and qa['scene_triangles']==source['triangles']
write(out/'qa/evidence/build.json',{'asset_id':'euproops','revision':'r001','generator_seed':P['seed'],'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','threejs_target':'0.180.0','glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'source_sha256':sha(Path(__file__)),'params_sha256':sha(HERE/'params.json'),'source_bounds_to_glb_max_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'origin':'floor contact at Z=0; XY shell center, not tail-tip bbox center','ground_shift_m':-low,'semantic_appendages':limb_records,'major_appendage_pair_count':6,'walking_pair_count':4,'epimera_per_side':7,'measurements_m':{'prosoma_width':.0168,'prosoma_anterior_to_attachment':.0069,'opisthosoma_width':.0112,'opisthosoma_anterior_to_longest_epimeron':.0073,'telson_centerline_y_span':.0079,'shell_max_height_inferred':.003},'scale_caveat':'Text dimensions govern. Figure scale bar discrepancy disclosed; nominal 22.1 mm sum is not separately measured total length. Telson originates within posterior marginal spine span. Color and height inferred.'})
print('BUILD_OK',qa['sha256'],qa['scene_triangles'])
