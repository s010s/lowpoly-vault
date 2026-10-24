# SPDX-License-Identifier: MIT
"""Original Cheirolepis trailli living reconstruction, not a fossil scan.
Run: blender -b -t 2 --python source/generate.py -- --output .
All generation inputs are in this source directory. No images are embedded.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, ground_asset
from qa_glb import audit_glb

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('.'));ap.add_argument('--gray',action='store_true')
 a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);out=a.output;out.mkdir(parents=True,exist_ok=True)
 cfg=json.loads((HERE/'params.json').read_text())
 if bpy.app.version_string!=cfg['blender_version']:raise RuntimeError('Pinned Blender version mismatch')
 col=setup_scene(cfg['asset_id'],cfg['seed']);root=bpy.data.objects[col['asset_root']]
 root['representation']='living-reconstruction';root['taxon']='Cheirolepis trailli';root['scientific_limits']=cfg['scientific_limits']['en'];root['mount']='body-center projected to lowest fin level'
 mats={k:make_material(k,v,roughness=.40 if k=='dark' else cfg['roughness']) for k,v in cfg['palette'].items()}
 def mesh(name,v,f,mat):return mesh_object(name,v,f,mats[mat] if isinstance(mat,str) else [mats[x] for x in mat],col)
 n=cfg['radial_segments']
 def loft(name,rings,materials):
  v=[(rx*math.cos(2*math.pi*j/n),y,zc+rz*math.sin(2*math.pi*j/n)) for y,rx,rz,zc in rings for j in range(n)]
  f=[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(len(rings)-1) for j in range(n)]
  f += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))]
  obj=mesh(name,v,f,materials)
  if isinstance(materials,list):
   for p in obj.data.polygons:
    avg=sum(obj.data.vertices[k].co.z for k in p.vertices)/len(p.vertices);p.material_index=0 if avg>.013 else 2 if avg<-.014 else 1
  return obj
 body=loft('scaled-tapered-trunk-and-upper-tail-axis',cfg['body_sections'],['dorsal','flank','ventral'])
 head=loft('large-gape-upper-head',cfg['head_sections'],['dorsal','flank','ventral'])
 jaw=loft('oblique-lower-jaw',cfg['jaw_sections'],'ventral')
 # Closed thin fin webs with a low ridge, kept as editable semantic parts.
 def fin(name,points,ridge,axis,half=.00075):
  axis=Vector(axis);ridge=Vector(ridge);m=len(points)
  v=[tuple(Vector(p)+axis*half*.18) for p in points]+[tuple(Vector(p)-axis*half*.18) for p in points]+[tuple(ridge+axis*half),tuple(ridge-axis*half)]
  f=[]
  for j in range(m):
   k=(j+1)%m;f.extend([(2*m,j,k),(2*m+1,m+k,m+j),(j,m+j,m+k,k)])
  return mesh(name,v,f,'fin')
 fins=[]
 def add_fin(name,pts,ridge,axis,half):
  fins.append((name,pts,ridge,axis,half));return fin(name,pts,ridge,axis,half)
 for sign,label in [(1,'right'),(-1,'left')]:
  pts=[(.019,-.088,-.016),(.033,-.080,-.025),(.046,-.054,-.040),(.044,-.045,-.043),(.031,-.052,-.036),(.021,-.070,-.023)]
  add_fin('pectoral-'+label,[(sign*x,y,z) for x,y,z in pts],(sign*.030,-.069,-.029),(0,0,1),.0010)
  pts=[(.015,-.035,-.018),(.025,-.025,-.029),(.030,-.009,-.036),(.023,-.014,-.032),(.013,-.023,-.021)]
  add_fin('pelvic-'+label,[(sign*x,y,z) for x,y,z in pts],(sign*.021,-.024,-.026),(0,0,1),.00065)
 add_fin('posterior-dorsal',[(0,.016,.011),(0,.034,.035),(0,.057,.055),(0,.061,.055),(0,.052,.038),(0,.044,.006)],(0,.039,.028),(1,0,0),.0009)
 add_fin('posterior-anal',[(0,.008,-.014),(0,.026,-.030),(0,.050,-.043),(0,.046,-.024),(0,.051,-.004)],(0,.032,-.023),(1,0,0),.0008)
 add_fin('unequal-caudal-web',[(0,.077,.005),(0,.103,.016),(0,.126,.024),(0,.149,.029),(0,.139,.020),(0,.128,.008),(0,.127,-.001),(0,.138,-.025),(0,.127,-.022),(0,.105,-.007),(0,.085,-.002)],(0,.117,.006),(1,0,0),.00065)
 # Exact polygonal loft surface, used to seat eyes/scales without floating discs.
 def surf(rings,y,angle):
  for i in range(len(rings)-1):
   if rings[i][0]<=y<=rings[i+1][0]:
    t=(y-rings[i][0])/(rings[i+1][0]-rings[i][0]);rx,rz,zc=[rings[i][k]*(1-t)+rings[i+1][k]*t for k in (1,2,3)];break
  else:raise ValueError('Surface query out of loft')
  phase=(angle%(2*math.pi))*n/(2*math.pi);j=int(phase);q=phase-j
  aa=2*math.pi*j/n;bb=2*math.pi*(j+1)/n
  return Vector((rx*((1-q)*math.cos(aa)+q*math.cos(bb)),y,zc+rz*((1-q)*math.sin(aa)+q*math.sin(bb))))
 def sx(rings,y,z):
  for i in range(len(rings)-1):
   if rings[i][0]<=y<=rings[i+1][0]:
    t=(y-rings[i][0])/(rings[i+1][0]-rings[i][0]);rx,rz,zc=[rings[i][k]*(1-t)+rings[i+1][k]*t for k in (1,2,3)];break
  else:raise ValueError('Eye query out of loft')
  cross=[(rx*math.cos(2*math.pi*j/n),zc+rz*math.sin(2*math.pi*j/n)) for j in range(n)];xs=[]
  for j in range(n):
   x1,z1=cross[j];x2,z2=cross[(j+1)%n]
   if min(z1,z2)<=z<=max(z1,z2) and abs(z1-z2)>1e-10:xs.append(x1+(x2-x1)*(z-z1)/(z2-z1))
  return max(xs)
 if not a.gray:
  def eye(name,sign,rad,mat,relief):
   y=-.137;z=.023;k=20;v=[(sign*(sx(cfg['head_sections'],y,z)-.001),y,z)]
   for j in range(k):
    yy=y+rad*.88*math.cos(2*math.pi*j/k);zz=z+rad*math.sin(2*math.pi*j/k);v.append((sign*(sx(cfg['head_sections'],yy,zz)+relief*.12),yy,zz))
   v.append((sign*(sx(cfg['head_sections'],y,z)+relief),y,z));f=[]
   for j in range(k):f += [(0,1+(j+1)%k,1+j),(k+1,1+j,1+(j+1)%k)]
   mesh(name,v,f,mat)
  for sign,label in [(1,'right'),(-1,'left')]:
   eye('orbital-rim-'+label,sign,.0057,'eye_rim',.0008);eye('eye-'+label,sign,.0042,'dark',.00115)
  # Small diamond scales: simplified count, low relief, combined into one mesh.
  v=[];f=[];ids=[]
  for row in range(29):
   y=-.082+row*.0051
   for j in range(n):
    angle=2*math.pi*(j+.5*(row%2))/n;span=.00225 if y<.03 else .0018
    normal=Vector((math.cos(angle),0,math.sin(angle)));start=len(v)
    outline=[surf(cfg['body_sections'],y-span,angle),surf(cfg['body_sections'],y,angle+.10),surf(cfg['body_sections'],y+span,angle),surf(cfg['body_sections'],y,angle-.10)]
    v += [tuple(p+normal*.00004) for p in outline]+[tuple(surf(cfg['body_sections'],y,angle)+normal*.00026),tuple(surf(cfg['body_sections'],y,angle)-normal*.00020)]
    for k in range(4):f += [(start+4,start+k,start+(k+1)%4),(start+5,start+(k+1)%4,start+k)];ids += [0 if surf(cfg['body_sections'],y,angle).z>.013 else 2 if surf(cfg['body_sections'],y,angle).z<-.014 else 1]*2
  obj=mesh('small-rhombic-scale-rhythm',v,f,['dorsal','flank','ventral'])
  for p,idx in zip(obj.data.polygons,ids):p.material_index=idx
  # Thin closed rods give fin-ray cues; no unsupported exact count is claimed.
  rv=[];rf=[]
  def rod(p,q,radius=.00023,sides=5):
   p,q=Vector(p),Vector(q);axis=(q-p).normalized();u=axis.cross(Vector((1,0,0)))
   if u.length<.1:u=axis.cross(Vector((0,1,0)))
   u.normalize();w=axis.cross(u);start=len(rv)
   for center,rr in [(p,radius),(q,radius*.45)]:
    rv.extend([tuple(center+(u*math.cos(2*math.pi*k/sides)+w*math.sin(2*math.pi*k/sides))*rr) for k in range(sides)])
   for k in range(sides):rf.append((start+k,start+(k+1)%sides,start+sides+(k+1)%sides,start+sides+k))
   rf.extend([tuple(start+k for k in reversed(range(sides))),tuple(start+sides+k for k in range(sides))])
  # Fan rays sit on the two thin web faces; the membrane remains the silhouette.
  for name,pts,ridge,axis,half in fins:
   pivot=Vector(pts[0])*.65+Vector(ridge)*.35
   targets=[]
   for k in range(1,len(pts)-2):
    a0,b0=Vector(pts[k]),Vector(pts[k+1])
    for t in [.15,.55,.90]:targets.append(a0.lerp(b0,t))
   for sg in (-1,1):
    off=Vector(axis)*half*.60
    for p in targets:rod(pivot+off,pivot.lerp(p,.93)+off)
  mesh('simplified-fin-ray-cues',rv,rf,'finray')
  # Gill-cover trailing seams, not large placoderm head shields.
  gv=[];gf=[]
  for sign in (-1,1):
   for j in range(12):
    z=.023-j*.0036;y=-.091+.006*math.sin(j*math.pi/11)
    x=sx(cfg['body_sections'],y,z);w=.00045;start=len(gv)
    gv += [(sign*(x+.00022),y-w,z+.0017),(sign*(x+.00022),y+w,z+.0017),(sign*(x+.00022),y+w,z-.0017),(sign*(x+.00022),y-w,z-.0017),(sign*(x-.0005),y,z)]
    gf += [(start,start+1,start+2,start+3),(start+4,start+1,start),(start+4,start+2,start+1),(start+4,start+3,start+2),(start+4,start,start+3)]
  mesh('opercular-seams',gv,gf,'finray')
  # A dark posterior throat anchors a genuine geometric gape, without a side decal.
  loft('recessed-mouth-throat',[[-.111,.018,.007,-.013],[-.103,.020,.009,-.012]],'mouth')
  # Discrete modest marginal teeth on both sides; artistic count and proportions.
  tv=[];tf=[]
  for sign in (-1,1):
   for i in range(10):
    y=-.145+i*.0033
    for rings,upper in [(cfg['head_sections'],True),(cfg['jaw_sections'],False)]:
     ang=-.84 if upper else .84
     p=surf(rings,y,ang);p.x*=sign;p.z+=(-.00015 if upper else .00015)
     tip=p+Vector((0,0,-.0014 if upper else .0014));r=.00058;st=len(tv)
     tv += [tuple(p+Vector((r*math.cos(2*math.pi*k/5),r*math.sin(2*math.pi*k/5),0))) for k in range(5)]+[tuple(tip)]
     tf.append(tuple(st+k for k in reversed(range(5))))
     for k in range(5):tf.append((st+k,st+(k+1)%5,st+5))
  mesh('simplified-marginal-teeth',tv,tf,'ventral')
 # One global scale, no independent normalization of semantic parts.
 ys=[v.co.y for obj in col.all_objects if obj.type=='MESH' for v in obj.data.vertices];factor=cfg['length_m']/(max(ys)-min(ys))
 for obj in col.all_objects:
  if obj.type=='MESH':
   for v in obj.data.vertices:v.co*=factor
 offset=ground_asset(col,center_xy=False);source=audit_source(col,cfg['max_triangles'])
 if source['errors']:raise RuntimeError(source['errors'])
 scene=bpy.context.scene;scene.render.filepath='//render';scene['mounting_offset_m']=offset;scene.render.threads_mode='FIXED';scene.render.threads=2
 for screen in bpy.data.screens:
  for area in screen.areas:
   for space in area.spaces:
    if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//';space.params.filename='model.blend'
 bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
 bpy.ops.object.select_all(action='DESELECT')
 for obj in col.all_objects:obj.select_set(True)
 bpy.context.view_layer.objects.active=root
 options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
 available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
 if set(options)-available:raise RuntimeError('Exporter RNA mismatch')
 bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
 glb=audit_glb(out/'model.glb',cfg['max_triangles'],cfg['max_materials'],cfg['max_primitives']);glb['file']='model.glb'
 if glb['errors'] or glb['bytes']>cfg['max_glb_bytes']:raise RuntimeError(glb)
 write(out/'qa/evidence/build.json',{'check':'deterministic-source-build','blender_version':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'gray_only':a.gray,'source':source,'glb':glb,'blend_sha256':sha(out/'model.blend'),'export_options':options,'mounting_offset_m':offset,'scientific_limits':cfg['scientific_limits']})
 print('BUILD_COMPLETE '+glb['sha256'])
if __name__=='__main__':main()
