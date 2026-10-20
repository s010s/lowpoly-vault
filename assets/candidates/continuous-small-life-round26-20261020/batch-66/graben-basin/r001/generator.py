# SPDX-License-Identifier: MIT
"""Original batch66 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
import bpy,sys,json,math,argparse,pathlib,datetime,hashlib
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True)
slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};groups={}
def part(name,vs,fs,mat):
 v,f=groups.setdefault((name,mat),([],[]));n=len(v);v.extend(vs);f.extend([tuple(n+i for i in face) for face in fs])
def loft(name,rings,mat):
 n=len(rings[0]);vs=[p for ring in rings for p in ring];fs=[tuple(range(n-1,-1,-1))]
 for j in range(len(rings)-1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 fs.append(tuple((len(rings)-1)*n+i for i in range(n)));part(name,vs,fs,mat)
def tube(name,points,radii,mat,n=6):
 rings=[]
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);tangent.normalize();ref=Vector((0,0,1)) if abs(tangent.z)<.95 else Vector((1,0,0));u=tangent.cross(ref).normalized();w=tangent.cross(u).normalized()
  rings.append([tuple(Vector(p)+radii[i]*(u*math.cos(j*math.tau/n)+w*math.sin(j*math.tau/n))) for j in range(n)])
 loft(name,rings,mat)
def ellipsoid(name,c,r,mat,n=12,k=6):
 rings=[]
 for j in range(k+1):
  t=-math.pi/2+.15+(math.pi-.30)*j/k
  rings.append([(c[0]+r[0]*math.cos(t)*math.cos(i*math.tau/n),c[1]+r[1]*math.cos(t)*math.sin(i*math.tau/n),c[2]+r[2]*math.sin(t)) for i in range(n)])
 loft(name,rings,mat)

# Geometry authored after all four immutable freezes 2026-10-20T13:35:44Z.
import random
rng=random.Random(cfg['seed'])
def louisella():
 n=16
 def center(t):return Vector((.014*math.sin(t*math.tau),-.15+.30*t,.016+.003*math.sin(t*math.tau)))
 def radius(t):
  levels=[(0,.0015),(.08,.0024),(.16,.0045),(.24,.0048),(.28,.0105),(.37,.012),(.48,.0122),(.65,.0115),(.83,.009),(.9,.0065),(.97,.0034),(1,.002)]
  for (a,r),(b,s) in zip(levels,levels[1:]):
   if a<=t<=b:return r+(s-r)*(t-a)/(b-a)
  return .002
 def frame(t):
  tangent=(center(min(1,t+.001))-center(max(0,t-.001))).normalized();u=Vector((tangent.y,-tangent.x,0)).normalized();v=u.cross(tangent).normalized();return u,v
 rings=[]
 # Start at closed recessed oral throat, roll out through mouth rim, then whole body to rounded posterior.
 for t,r in [(.009,.00035),(0,.0008),(0,.0015)]+[(i/140,radius(i/140)*(1+.045*math.cos(i*math.pi))) for i in range(1,141)]:
  c=center(t);u,v=frame(t);rings.append([tuple(c+r*(u*math.cos(k*math.tau/n)+v*math.sin(k*math.tau/n))) for k in range(n)])
 loft('whole_body_four_zones_annulated_and_smooth_rear',rings,'body')
 # Short trunk spine rings; posterior zone deliberately unspined.
 for j in range(16):
  t=.29+j*.037;c=center(t);u,v=frame(t);r=radius(t)
  for k in range(10):
   a=k*math.tau/10+(j%2)*.2;d=u*math.cos(a)+v*math.sin(a);length=.0015 if t<.43 else .00085
   tube('short_trunk_spine_rings',[tuple(c+d*(r-.00015)),tuple(c+d*(r+length))],[.00042,.00008],'spines',5)
 # Proboscis smaller scalids, exactly25 long scalids around its midlength.
 for j in range(7):
  t=.025+j*.028;c=center(t);u,v=frame(t)
  for k in range(8):
   a=k*math.tau/8+j*.3;d=u*math.cos(a)+v*math.sin(a);r=radius(t);tube('fine_proboscis_scalids',[tuple(c+d*(r-.0001)),tuple(c+d*(r+.00065))],[.00024,.00006],'spines',5)
 t=.125;c=center(t);u,v=frame(t)
 for k in range(25):
  a=k*math.tau/25;d=u*math.cos(a)+v*math.sin(a);tube('proboscis_exactly_25_long_midlength_scalids',[tuple(c+d*(radius(t)-.0001)),tuple(c+d*(radius(t)+.0042)+Vector((0,-.001,0)))],[.00045,.00008],'spines',5)
 for j in range(23):
  t=.45+j*.0195;c=center(t);u,v=frame(t);r=radius(t)
  for side in [-1,1]:
   d=(v*.82+u*side*.57).normalized();start=c+d*(r-.0002);end=c+d*(r+.0027)
   tube('paired_dorsal_longitudinal_blunt_papilla_rows',[tuple(start),tuple(start.lerp(end,.72)),tuple(end)],[.00105,.00095,.0003],'papilla',7)
 # Small smooth posterior opening inset but no spines/appendages.
 c=center(1);u,v=frame(1)
 # Closed recessed terminal cup is represented in full rear volume rather than adding an appendage.
 ellipsoid('posterior_small_recessed_aperture',tuple(c+Vector((0,.00002,0))),(.0007,.00015,.0007),'mouth',10,4)
def hoodoo():
 n=20;rings=[]
 levels=[(0,1.55),(.4,1.35),(1.0,1.06),(1.4,.92),(1.55,1.12),(1.7,.91),(2.5,.74),(2.9,.89),(3.05,.7),(3.8,.63),(4.25,.74),(4.4,.60),(5.3,.55),(5.8,.66),(5.95,.50),(6.7,.48),(7.3,.51),(7.37,.66),(7.75,.67),(8,.54)]
 for j,(z,r) in enumerate(levels):
  cx=.13*math.sin(z*.4);cy=.11*math.sin(z*.8)
  rings.append([(cx+r*(1+.11*math.sin(i*2.7)+.06*math.sin(i*.7+j*.25))*math.cos(i*math.tau/n),cy+r*.88*(1+.12*math.sin(i*1.8+j*.22))*math.sin(i*math.tau/n),z+.035*math.sin(i*1.6+j*.3) if z else 0) for i in range(n)])
 loft('continuous_irregular_tapered_cap_protected_pillar',rings,'rock')
def graben():
 # Three fully volumetric prisms with real inward-dipping boundaries and physically displaced marker layers.
 # Each cross-section polygon is built in X,Z and extruded alongY. Same layers down9m centrally.
 def prism(name,poly,mat):
  vs=[(x,y,z) for y in [-30,30] for x,z in poly];n=len(poly);fs=[tuple(range(n-1,-1,-1)),tuple(n+i for i in range(n))]
  for i in range(n):fs.append((i,(i+1)%n,(i+1)%n+n,i+n))
  part(name,vs,fs,mat)
 # Fault boundaries slope from x+-11 at base to x+-20 at high shoulder top.
 def left(z):return -11-.60*z
 def right(z):return 11+.60*z
 # Layer edges shifted lower by9m in middle. Truncated bottom retains closed geometry.
 for side in [-1,1]:
  for j,(lo,hi,mat) in enumerate([(0,3,'base'),(3,6,'rust'),(6,9,'ochre'),(9,12,'pale'),(12,15,'surface')]):
   poly=[(-40,lo),(left(lo),lo),(left(hi),hi),(-40,hi)] if side<0 else [(right(lo),lo),(40,lo),(40,hi),(right(hi),hi)]
   prism(('left' if side<0 else 'right')+'_shoulder_layer_'+str(j),poly,mat)
 # Central surface is lower, with same stratigraphic marker colors displaced downward.
 for j,(lo,hi,mat) in enumerate([(0,3,'pale'),(3,6,'surface')]):prism('down_dropped_central_block_layer_'+str(j),[(left(lo),lo),(right(lo),lo),(right(hi),hi),(left(hi),hi)],mat)
 # Tiny integrated angular erosion spurs along outer shoulders, not floating rocks.
 for side in [-1,1]:
  for k in range(10):
   y=-27+k*6;x=side*(25+2*math.sin(k*1.3));ellipsoid('shoulder_subtle_erosion_relief',(x,y,14.9),(4.3,3.8,.65),'surface',7,3)
def river():
 # Cross-channel strip sampling: high floodplain, low inside bar, flat opaque water, steep outside bank.
 ny=90;nc=14;vs=[];fs=[];mats=[]
 for j in range(ny+1):
  y=-45+j;cx=12*math.sin(y*math.tau/60);inside=-1 if cx>0 else 1;strength=abs(math.sin(y*math.tau/60))
  lb=5.0+5*strength if inside<0 else 5.0;rb=5.0+5*strength if inside>0 else 5.0
  xs=[-30,-24,-18,cx-lb-3,cx-lb,cx-4.5,cx-3.4,cx,cx+3.4,cx+4.5,cx+rb,cx+rb+3,18,24,30]
  # Ensure broad outer columns remain ordered at extreme bends.
  xs[:4]=[-30,(-30+cx-lb-3)/2,cx-lb-5,cx-lb-3];xs[11:]=[cx+rb+3,cx+rb+5,(cx+rb+3+30)/2,30]
  heights=[]
  for i,x in enumerate(xs):
   if i in [6,7,8]:z=1.45
   elif i in [5,9]:z=1.65 if (i==5 and inside<0) or (i==9 and inside>0) else 4.6
   elif i in [4,10]:z=2.4 if (i==4 and inside<0) or (i==10 and inside>0) else 4.8
   else:z=4.75+.18*math.sin(x*.23+y*.19)
   vs.append((x,y,z))
 for j in range(ny):
  y=-44.5+j;inside=-1 if math.sin(y*math.tau/60)>0 else 1
  for i in range(nc):
   a=j*15+i;b=a+15;fs.extend([(a,a+1,b+1),(a,b+1,b)])
   mat='water' if i in [6,7] else 'sand' if (inside<0 and i in [4,5]) or (inside>0 and i in [8,9]) else 'cutbank' if i in [5,8] else 'land';mats.extend([mat,mat])
 perimeter=list(range(15))+[j*15+14 for j in range(1,ny+1)]+[ny*15+i for i in range(13,-1,-1)]+[j*15 for j in range(ny-1,0,-1)];offset=len(vs)
 for v in perimeter:x,y,z=vs[v];vs.append((x,y,0))
 for k,a in enumerate(perimeter):q=(k+1)%len(perimeter);fs.append((a,perimeter[q],offset+q,offset+k));mats.append('soil')
 fs.append(tuple(offset+k for k in range(len(perimeter))));mats.append('soil')
 keys=list(cfg['palette']);obj=mesh_object('closed_floodplain_with_inset_channel_and_banks',vs,fs,[m[k] for k in keys],col)
 for poly,mat in zip(obj.data.polygons,mats):poly.material_index=keys.index(mat)
{'louisella':louisella,'hoodoo':hoodoo,'graben-basin':graben,'meandering-river-reach':river}[slug]()
for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if mat=='body':
  for k in ['pale','neck','mouth']:obj.data.materials.append(m[k])
  obj.data.update()
  for p in obj.data.polygons:
   t=(p.center.y+.15)/.30;p.material_index=3 if t<.01 and p.center.y>-.1498 else 2 if .26<t<.41 else 1 if t>.86 or .43<t<.65 else 0
 elif slug=='hoodoo':
  for k in ['pale','rust','cap']:obj.data.materials.append(m[k])
  obj.data.update()
  for p in obj.data.polygons:
   z=p.center.z;p.material_index=3 if z>7.35 else 1 if 1.35<z<1.75 or 2.8<z<3.15 or 4.15<z<4.5 or 5.7<z<6.1 else 2 if 2<z<2.8 or 4.8<z<5.7 else 0
 # Intentional flat-shaded faces, no negative scale or hidden reference meshes.
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
