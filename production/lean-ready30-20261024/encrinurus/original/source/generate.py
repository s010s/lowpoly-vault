# SPDX-License-Identifier: MIT
"""Deterministic Encrinurus egani living stylization, Blender 4.3.2.
Run with -- --output OUTPUT_DIRECTORY. --gray creates the private shape study.
The package contains every non-runtime import. Dimensions are authored in mm.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, ground_asset, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser(); a.add_argument('--output',type=Path,required=True); a.add_argument('--gray',action='store_true'); args=a.parse_args(argv)
args.output=args.output.resolve()
args.output.mkdir(parents=True,exist_ok=True)
COL=setup_scene(P['asset_id'],P['seed'])
M={k:make_material(k,'#8B8B87' if args.gray else v,roughness=.78 if k!='eyes' else .62) for k,v in P['palette'].items()}
class Part:
 def __init__(self,name,material): self.name=name; self.material=material; self.v=[]; self.f=[]
 def add(self,v,f):
  off=len(self.v); self.v.extend(v); self.f.extend(tuple(off+i for i in face) for face in f)
 def emit(self):
  ob=mesh_object(self.name,[(x*.001,y*.001,z*.001) for x,y,z in self.v],self.f,M[self.material],COL); return ob

def ellipsoid(p,c,r,n=12,l=6):
 v=[(c[0],c[1],c[2]+r[2])]
 for j in range(1,l):
  phi=math.pi*j/l
  for i in range(n):
   t=2*math.pi*i/n; v.append((c[0]+r[0]*math.sin(phi)*math.cos(t),c[1]+r[1]*math.sin(phi)*math.sin(t),c[2]+r[2]*math.cos(phi)))
 v.append((c[0],c[1],c[2]-r[2])); f=[]
 for i in range(n): f.append((0,1+i,1+(i+1)%n))
 for j in range(l-2):
  for i in range(n):
   a=1+j*n+i; b=1+j*n+(i+1)%n; f.append((a,a+n,b+n,b))
 end=len(v)-1; st=1+(l-2)*n
 for i in range(n): f.append((end,st+(i+1)%n,st+i))
 p.add(v,f)

def tube(p,points,radii,n=8):
 v=[]
 for j,(co,r) in enumerate(zip(points,radii)):
  co=Vector(co); tangent=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(0,j-1)]); tangent.normalize()
  ref=Vector((0,0,1)) if abs(tangent.z)<.85 else Vector((0,1,0)); u=tangent.cross(ref).normalized(); w=tangent.cross(u).normalized()
  for i in range(n):
   t=2*math.pi*i/n; v.append(tuple(co+r*(math.cos(t)*u+math.sin(t)*w)))
 f=[tuple(reversed(range(n)))]
 for j in range(len(points)-1):
  for i in range(n): f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 f.append(tuple((len(points)-1)*n+i for i in range(n))); p.add(v,f)

def solid_grid(p,rows,cols,fun,bottom):
 v=[fun(r,u) for r in rows for u in cols]; count=len(v); nc=len(cols); nr=len(rows)
 v.extend((x,y,bottom(r,u,x,y,z)) for r in rows for u in cols for x,y,z in [fun(r,u)])
 f=[]
 for j in range(nr-1):
  for i in range(nc-1):
   k=j*nc+i; f.append((k,k+1,k+1+nc,k+nc)); f.append((count+k+nc,count+k+1+nc,count+k+1,count+k))
 perimeter=list(range(nc))+[j*nc+nc-1 for j in range(1,nr)]+list(range((nr-1)*nc+nc-2,(nr-1)*nc-1,-1))+[j*nc for j in range(nr-2,0,-1)]
 for k,i in enumerate(perimeter):
  j=perimeter[(k+1)%len(perimeter)]; f.append((i,count+i,count+j,j))
 p.add(v,f)

head=Part('vaulted-cephalon','shell'); v=[(0,-12.3,6.2)]; n=36
for r in [.2,.42,.65,.84,1.0]:
 for i in range(n):
  t=2*math.pi*i/n; perimeter_y=-7.0-12.8*max(math.cos(t),0); y=-12.3+r*(perimeter_y+12.3); x=11.7*r*math.sin(t)
  z=2.65+3.55*(1-r*r)+.15*math.cos(t); v.append((x,y,z))
f=[(0,1+i,1+(i+1)%n) for i in range(n)]
for j in range(4):
 for i in range(n):
  k=1+j*n+i; q=1+j*n+(i+1)%n; f.append((k,k+n,q+n,q))
st=len(v); v.extend((v[1+4*n+i][0],v[1+4*n+i][1],1.65) for i in range(n)); c=len(v); v.append((0,-12.8,1.65))
for i in range(n):
 a0=1+4*n+i; a1=1+4*n+(i+1)%n; f.extend([(a0,st+i,st+(i+1)%n,a1),(c,st+(i+1)%n,st+i)])
head.add(v,f)
# A raised, elongated glabella instead of the spherical expansion of Deiphon.
glab=Part('vaulted-lobate-glabella','glabella'); ellipsoid(glab,(0,-13.35,5.3),(4.55,5.95,3.1),n=20,l=8)
bumps=Part('low-cephalic-tubercles','tubercles')
if not args.gray:
 for yy,xs in [(-17.3,[-1.6,0,1.6]),(-15.7,[-2.8,-.9,.9,2.8]),(-14.1,[-3.1,-1.15,1.15,3.1]),(-12.3,[-2.75,-.9,.9,2.75]),(-10.7,[-1.8,0,1.8]),(-9.6,[-.8,.8])]:
  for xx in xs:
   term=max(.05,1-(xx/4.55)**2-((yy+13.35)/5.95)**2); zz=5.3+3.1*math.sqrt(term)
   ellipsoid(bumps,(xx,yy,zz-.08),(.44,.48,.35),n=8,l=4)
 for side in [-1,1]:
  for xx,yy,zz in [(5.25,-15.7,4.7),(7,-14.4,4.5),(8.3,-12.8,4.1),(6.8,-10.6,4.7),(9.3,-11.2,3.4),(4.8,-9.2,4.8)]:
   ellipsoid(bumps,(side*xx,yy,zz),(.4,.44,.27),n=8,l=4)
# Paired elevated eyes have stout tapering stalks, not thin decorative horns.
stalk=Part('paired-eye-peduncles','glabella'); eyes=Part('paired-visual-surfaces','eyes')
for side in [-1,1]:
 tube(stalk,[(side*6.5,-13,4.45),(side*7.15,-13.25,6.1),(side*7.6,-13.7,8.35)],[1.1,.83,.63],10)
 ellipsoid(eyes,(side*7.6,-13.7,8.6),(.88,.88,.85),n=12,l=6)
 # Subdued genal corners are attached to the cephalic edge.
 tube(head,[(side*11.1,-7.4,2.7),(side*11.4,-6.0,2.3),(side*10.9,-4.8,1.85)],[.95,.65,.18],8)
# Ten overlapping articulated tergites, connected ventrally but visibly separated dorsally.
thorax=Part('articulated-thoracic-tergites','rib'); cols=[-1,-.88,-.68,-.46,-.29,-.2,0,.2,.29,.46,.68,.88,1]
for seg in range(P['thoracic_segments_artistic']):
 y0=-7.1+seg*1.46; w=10.0-.17*seg
 def fun(r,u,y0=y0,w=w):
  x=w*u; y=y0+r+1.05*abs(u)**1.6
  crest=.40*math.sin(math.pi*r/1.35); z=2.35+2.0*(1-u*u)+1.62*math.exp(-(u/.25)**6)+crest
  return (x,y,z)
 solid_grid(thorax,[0,.35,.78,1.35],cols,fun,lambda r,u,x,y,z: 2.0+.25*(1-u*u))
# A single fused triangular pygidial plate with integral transverse rib relief.
tail=Part('fused-densely-ribbed-pygidium','shell'); ribs=P['pygidial_ribs_artistic']
rows=[i/(ribs*4) for i in range(ribs*4+1)]
cols2=[-1,-.92,-.77,-.6,-.43,-.3,-.22,-.15,0,.15,.22,.3,.43,.6,.77,.92,1]
def tail_fun(s,u):
 w=8.12*(1-s)**.86+.20; x=w*u; y=7.3+12.7*s+.7*math.sin(math.pi*s)*abs(u)**1.3
 axial=1.4*math.exp(-(u/.27)**6)*(1-s)**.55
 rib=.34*(.5+.5*math.cos(2*math.pi*ribs*s))*(.65+.35*(1-u*u))*(1-.5*s)
 return (x,y,1.85+.65*(1-s)+1.35*(1-u*u)*(1-.55*s)+axial+rib)
solid_grid(tail,rows,cols2,tail_fun,lambda s,u,x,y,z:1.55+.25*(1-s))
under=Part('inferred-ventral-body','ventral'); ellipsoid(under,(0,-1,2.0),(4.4,13,.95),n=16,l=6)
limbs=Part('inferred-subordinate-appendages','ventral')
if not args.gray:
 for side in [-1,1]:
  for i in range(9):
   yy=-6.7+i*1.75; ww=7.0-.12*i
   tube(limbs,[(side*2.6,yy,1.65),(side*4.8,yy+.1,1.25),(side*ww,yy-.6,.42),(side*(ww+.6),yy-.95,.25)],[.29,.25,.21,.12],6)
  tube(limbs,[(side*3.0,-16.2,1.75),(side*5.2,-18.4,1.3),(side*6.4,-20.3,1.0),(side*6.3,-22.0,.85)],[.24,.2,.15,.09],6)
for p in [head,glab,bumps,stalk,eyes,thorax,tail,under,limbs]:
 if p.v:p.emit()
ground_asset(COL,center_xy=False)
bpy.context.scene['reconstruction_scope']='Living stylization; ventral anatomy, colors and posture inferred; repetition simplified.'
bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.scene['asset_license']='CC-BY-4.0'
# Use portable output and UI directories before serializing the editable scene.
bpy.context.scene.render.filepath='//'
for screen in bpy.data.screens:
 for area in screen.areas:
  for space in area.spaces:
   if space.type=='FILE_BROWSER' and space.params:
    space.params.directory=b'/'*1023
    space.params.directory=b'//'
bpy.context.preferences.filepaths.save_version=0
source=audit_source(COL,max_triangles=18000)
if source['errors']: raise RuntimeError(str(source['errors']))
bpy.ops.wm.save_as_mainfile(filepath=str(args.output/'model.blend'),relative_remap=True)
bpy.ops.object.select_all(action='DESELECT')
for obj in COL.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[COL['asset_root']]
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
assert not (set(options)-available)
bpy.ops.export_scene.gltf(filepath=str(args.output/'model.glb'),**options)
exported=audit_glb(args.output/'model.glb',18000,8,36); exported['file']='model.glb'
report={'status':'PASS' if not exported['errors'] else 'FAIL','source':source,'exported':exported,'export_options':options,'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'gray_study':args.gray}
(args.output/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
if exported['errors']:raise RuntimeError(str(exported['errors']))
print('BUILD_OK',exported['scene_triangles'],exported['bytes'])
