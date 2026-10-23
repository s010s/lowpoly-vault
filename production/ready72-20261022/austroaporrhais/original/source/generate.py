# SPDX-License-Identifier: MIT
"""Original deterministic Austroaporrhais cf. gregaria material-level reconstruction.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
Only local params.json and the declared source/deps files are imported.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector, geometry
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((SOURCE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); args=p.parse_args(argv)
out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
def save(name,value): (out/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
c=setup_scene(P['asset_id'],P['seed'])
root=bpy.data.objects[c['asset_root']]
root['taxon']='Austroaporrhais cf. gregaria'
root['representation']='Material-level interpretive fossil-shell reconstruction; not a specimen scan or facsimile'
root['restoration']='Specimen 272 body; specimen 302 posterior-process direction only. No fragment dimensions transferred.'
mat=make_material('Muted limestone fossil',P['palette']['fossil'],roughness=.91)
dark=make_material('Shallow inferred aperture',P['palette']['aperture'],roughness=.96)
# A low, blunt preserved apex, four stepped helical turns, and expanded final whorl.
profile=[(0,.22),(.025,1.7),(.07,3.5),(.13,5.1),(.20,8.1),(.27,12.3),(.34,16.0),(.41,18.2),(.47,17.6),(.53,14.4),(.59,11.1),(.63,10.0),(.70,8.6),(.77,7.0),(.84,5.7),(.91,4.2),(.97,2.8),(1,1.25)]
def interp(t):
 for (a,x),(b,y) in zip(profile,profile[1:]):
  if a<=t<=b:
   u=(t-a)/(b-a); u=u*u*(3-2*u); return x+(y-x)*u
 return profile[-1][1]
def g(x,s): return math.exp(-.5*(x/s)**2)
N=P['radial_segments']; H=P['height_segments']; verts=[]; faces=[]; regions=[]
for i in range(H+1):
 t=i/H; z=.1*t
 for j in range(N):
  th=2*math.pi*j/N
  r=interp(t)/1000
  # Broad sutural relief only; it is intentionally not a reconstruction of lost shell ornament.
  if t>.57:
   wave=(math.cos(2*math.pi*(t-.59)/.113-th)-.2)
   amp=.00095*min(1,(t-.57)/.05)*min(1,(1.015-t)/.065)
   r+=amp*wave
  r+=.0017*g(z-(.044+.0014*math.sin(th)),.0021)
  r+=.00105*g(z-(.027+.0010*math.sin(th)),.0019)
  # Slightly irregular retained fossil shape, never high-frequency micro-ornament.
  r*=1+.013*math.sin(3*th+1.3)*math.sin(math.pi*t)
  x=r*math.cos(th); y=.86*r*math.sin(th)
  # Opposite (+Y) side has only a conservative shallow oval recess, no deep throat.
  q=((x+.002)/.010)**2+((z-.028)/.017)**2
  inner=math.sin(th)>.45 and q<1
  if math.sin(th)>.45:
   y-=.0082*max(0,1-q)**1.45
   y+=.00045*g(q-1,.17)
  verts.append((x,y,z)); regions.append(1 if inner and q<.75 else 0)
for i in range(H):
 for j in range(N):
  a=i*N+j;b=i*N+(j+1)%N;d=(i+1)*N+j;e=(i+1)*N+(j+1)%N
  faces.extend([(a,b,e),(a,e,d)])
base=len(verts);verts.extend([(0,0,0),(0,0,.1)]);regions.extend([0,0])
for j in range(N):
 faces.append((base,(j+1)%N,j)); faces.append((base+1,H*N+j,H*N+(j+1)%N))
body=mesh_object('Preserved_body_and_stepped_spire',verts,faces,[mat,dark],c)
for poly in body.data.polygons:
 poly.use_smooth=True
 poly.material_index=1 if all(regions[v] for v in poly.vertices) else 0
# Closed, gently convex wing: deep upper sinus; one long, upturned posterior process;
# one much shorter anterior process. The root is embedded into the preserved final whorl.
poly=[(2,55),(-16,51),(-23,48),(-29,48.5),(-34,51),(-37.5,57),(-40,65),(-40.7,70),(-42.1,69),(-43,65),(-43,59),(-41,48),(-38,38),(-34.5,29),(-34,25),(-35.5,22),(-38,20),(-37,17.5),(-31,17),(-24,15),(-17,18),(2,19)]
# Retain the deliberate low-poly contour; interpolate edges before triangulation.
pts=[Vector((x/1000,z/1000,0)) for x,z in poly]
tris0=geometry.tessellate_polygon([pts]); coords=[(v.x,v.y) for v in pts]
idx={tuple(v):i for i,v in enumerate(pts)}
tris=[tuple(v if isinstance(v,int) else idx[tuple(v)] for v in tri) for tri in tris0]
# Uniform triangle subdivision creates an editable solid without an external triangulator.
for level in range(3):
 cache={}; nxt=[]
 def mid(a,b):
  k=tuple(sorted((a,b)))
  if k not in cache:
   cache[k]=len(coords);coords.append(tuple((coords[a][i]+coords[b][i])/2 for i in range(2)))
  return cache[k]
 for a,b,d in tris:
  ab=mid(a,b);bd=mid(b,d);da=mid(d,a)
  nxt.extend([(a,ab,da),(ab,b,bd),(da,bd,d),(ab,bd,da)])
 tris=nxt
# Boundaries are found from topology, not floating point guesses.
edgecount={}
for tri in tris:
 for a,b in zip(tri,tri[1:]+tri[:1]):
  key=tuple(sorted((a,b)));edgecount[key]=edgecount.get(key,0)+1
boundary=[e for e,n in edgecount.items() if n==1]
def dsegment(x,z,a,b):
 ax,az=poly[a]; bx,bz=poly[b]; ax/=1000;az/=1000;bx/=1000;bz/=1000
 dx=bx-ax;dz=bz-az;u=max(0,min(1,((x-ax)*dx+(z-az)*dz)/(dx*dx+dz*dz)))
 return math.hypot(x-(ax+u*dx),z-(az+u*dz))
wv=[]
for side in (-1,1):
 for x,z in coords:
  dist=min(dsegment(x,z,k,(k+1)%len(poly)) for k in range(len(poly)))
  # Longitudinal ridges lead into each process without adding free spikes.
  rel=min(1,max(0,(-x-.014)/.029))
  upper=.043 + .025*rel**2.9
  lower=.026 - .008*rel
  ridge=.0017*g(z-upper,.0022)+.0010*g(z-lower,.0018)
  core=.00065+.0023*min(1,dist/.005)
  front=-.0025-.0060*max(0,1-rel)**1.7-ridge
  back=-.0004
  y=(front-core if side==-1 else back+core)
  # Taper the interior root behind the body, closing the low-root visual slit.
  rootblend=max(0,min(1,(x+.019)/.021))
  if side==-1:y=y*(1-.78*rootblend)
  else:y=y*(1-.45*rootblend)
  wv.append((x,y,z))
K=len(coords); wf=[tuple(reversed(t)) for t in tris]+[tuple(i+K for i in t) for t in tris]
for a,b in boundary:wf.append((a,b,b+K,a+K))
wing=mesh_object('Attached_wing_two_unequal_processes',wv,wf,mat,c)
for face in wing.data.polygons:face.use_smooth=True
wing['evidence']='272 observed wing roots; 302 posterior direction supplemented; tip z70 mm is inferred'
# Match measured envelope, not fragment-derived proportions. No global unit normalization.
allverts=[v for ob in (body,wing) for v in ob.data.vertices]
xmin=min(v.co.x for v in allverts); xmax=max(v.co.x for v in allverts)
ymin=min(v.co.y for v in allverts); ymax=max(v.co.y for v in allverts)
for v in allverts:
 v.co.x*=P['width_m']/(xmax-xmin)
 v.co.y*=P['depth_m']/(ymax-ymin)
# Preserve semantic meshes and identity root. Root is the basal shell-axis mounting point.
bpy.context.scene['origin_note']='Basal shell-axis point at z=0. Upright museum orientation, not a live-life posture.'
bpy.context.scene['surface_note']='Smooth low-poly normals with explicit broad keels; no invented fine shell sculpture.'
source=audit_source(c,max_triangles=40000)
if source['errors']: raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in c.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Exporter missing '+str(missing))
bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
audit=audit_glb(out/'model.glb',40000,6,8)
if audit['errors']:raise RuntimeError(audit['errors'])
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(audit['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
assert delta<1e-6 and audit['scene_triangles']==source['triangles']
assert (out/'model.glb').stat().st_size<=8000000
save('build-report.json',{'asset_id':P['asset_id'],'revision':P['revision'],'generator_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'blender':bpy.app.version_string,'exporter':'4.3.47','seed':P['seed'],'source':source,'glb':audit,'source_export_bounds_error_m':delta,'export_options':options,'reviewed_source_warnings':['Intentional smooth normals retain broad silhouette steps and keels. Both closed meshes are manifold; overlapping wing root is deliberate anatomical attachment, not claimed printable union.'],'bytes':(out/'model.glb').stat().st_size})
