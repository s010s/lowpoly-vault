# SPDX-License-Identifier: MIT
"""Original batch60 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
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

# ORIGINAL batch60 functions authored after modeling freeze.
def collinsium():
 # Axis -Y anterior. Radius envelopes widen gradually toward midbody.
 rings=[]
 for i in range(61):
  t=i/60;y=-.036+.075*t;radius=.0028+.0022*math.sin(math.pi*t)**.7
  # Epidermal corrugations are small real radius changes, not arthropod plates.
  radius*=1+.026*math.sin(t*math.tau*45);z=.012+.0015*math.sin(math.pi*t)
  rings.append([(radius*math.cos(j*math.tau/12),y,z+radius*.86*math.sin(j*math.tau/12)) for j in range(12)])
 loft('continuous_tubular_annulated_trunk',rings,'body')
 ellipsoid('ventrally_bent_eyeless_bulbous_head',(0,-.0393,.0105),(.0034,.0050,.0036),'body',12,6)
 ellipsoid('small_terminal_ventral_mouth',(0,-.0435,.0086),(.00115,.00038,.0008),'mouth',10,4)
 for sign in [-1,1]:
  ellipsoid('paired_subrectangular_head_sclerites',(sign*.00125,-.0399,.0136),(.00125,.0026,.00042),'spine',8,3)
  tube('paired_uniramous_antenna_like_appendages',[(sign*.0019,-.0423,.0109),(sign*.0030,-.0463,.010),(sign*.0039,-.048,.0093)],[.00032,.00020,.000035],'underside',5)
 # Positions compressed near both ends; midbody spacing is larger.
 ys=[-.034,-.0308,-.0272,-.0233,-.0190,-.0144,-.0087,-.0025,.0037,.0099,.0161,.0214,.0260,.0300,.0336]
 for j,y in enumerate(ys):
  t=(y+.036)/.075;r=.0028+.0022*math.sin(math.pi*t)**.7;z=.012+.0015*math.sin(math.pi*t)
  if j==0:
   for sign in [-1,1]:tube('station01_two_short_dorsolateral_spines',[(sign*r*.65,y,z+r*.65),(sign*(r*.65+.0004),y-.0002,z+r*.65+.00075)],[.00025,.000018],'spine',5)
  else:
   length=.006+.006*math.sin(math.pi*j/15)
   for q,ang in enumerate([0,-.60,.60,-1.12,1.12]):
    # Angle0 points dorsally. Spines generally incline gently anteriorly.
    sign=1 if ang>=0 else -1;ratio=1 if q==0 else (1/3 if q in [1,2] else 1/8);le=length*ratio
    base=Vector((r*math.sin(ang),y,z+r*.86*math.cos(ang)));direction=Vector((math.sin(ang),-.12,math.cos(ang))).normalized()
    tip=base+direction*le+Vector((0,-.00035*ratio,0));mid=base+direction*le*.65
    tube('stations02to15_medial_spines' if q==0 else 'stations02to15_paired_dorsolateral_spines' if q in [1,2] else 'stations02to15_paired_short_lateral_spines',[tuple(base),tuple(mid),tuple(tip)],[.00065*ratio**.45,.00032*ratio**.45,.000018],'spine',6)
  for sign in [-1,1]:
   origin=Vector((sign*r*.78,y,z-.0014))
   if j<6:
    pts=[origin,Vector((sign*(r+.002),y-.005,.010)),Vector((sign*(r+.005),y-.014,.0055)),Vector((sign*(r+.007),y-.025,.0014))]
    tube('six_pairs_elongated_smooth_filtering_limbs',[tuple(p) for p in pts],[.00085,.00064,.00040,.00010],'underside',6)
    # Twenty paired comb setae, downsampled from source~30, inner/ventral chevrons.
    for k in range(20):
     u=.20+.77*k/19;pos=u*3;idx=min(2,int(pos));f=pos-idx;p=pts[idx]*(1-f)+pts[idx+1]*f
     for side in [-1,1]:
      end=p+Vector((-sign*(.0015+.0005*math.sin(k*.3)),side*.00065,-.0007));tube('filter_setae_20_paired_per_limb',[tuple(p),tuple(end)],[.000095,.000018],'spine',3)
   else:
    pts=[origin,Vector((sign*(r+.0019),y+.0003,.008)),Vector((sign*(r+.0030),y+.0005,.0045)),Vector((sign*(r+.0035),y+.0018,.0022))]
    # Fine actual annular radius modulation along stout rear lobopods.
    ps=[];rs=[]
    for k in range(10):
     u=k/9;pos=u*3;idx=min(2,int(pos));f=pos-idx;p=pts[idx]*(1-f)+pts[idx+1]*f;ps.append(tuple(p));rs.append((.00125*(1-u*.65))*(1+.075*math.cos(k*math.pi)))
    tube('nine_pairs_annulated_posterior_lobopods',ps,rs,'underside',6)
    p=pts[-1];tube('nine_pairs_backward_recurved_terminal_claws',[tuple(p),tuple(p+Vector((0,.0016,-.0010))),tuple(p+Vector((0,.0024,-.0004))),tuple(p+Vector((0,.0027,.0006)))],[.00050,.00038,.00020,.000025],'claw',5)
 tube('posterior_lobopodous_trunk_extension',[(0,.036,.0124),(0,.040,.012),(0,.044,.0112)],[.0028,.0019,.00010],'body',10)
def yardang():
 # Continuous stone core, high compact windward nose to tapered lee tail.
 n=24;rings=[]
 for j in range(37):
  t=j/36;y=-4+8*t
  width=1.40*(.20+.80*min(1,t/.075))*(1-.91*t)**.80
  height=2.5*(.72+.28*min(1,t/.12))*(1-.98*t)**.72
  ring=[]
  for i in range(n):
   a=i*math.tau/n;sin=math.sin(a);groove=1+.065*math.sin(a*7+.25*math.sin(t*4))+.035*math.cos(a*11)
   x=width*math.cos(a)*groove+.07*math.sin(t*5)*(1-t);z=height*(.5+.5*sin)
   # Quiet ledge-like actual profile variation shared along the ridge.
   z+=height*.018*math.cos(a*8+t*2)*max(0,1-sin*sin)
   z=max(0,z);ring.append((x,y,z))
  rings.append(ring)
 loft('single_wind_eroded_longitudinally_fluted_ridge',rings,'sandstone')
def cirque():
 nx=40;ny=44;vs=[];fs=[]
 for j in range(ny+1):
  y=-45+90*j/ny
  for i in range(nx+1):
   x=-40+80*i/nx;dx=x/33;dy=(y-4)/32;r=math.sqrt(dx*dx+dy*dy);angle=math.atan2(dy,dx)
   # Front-Y throat has no enclosing high rim. Rear+Y headwall is steep.
   back=.10+.90*max(0,min(1,(dy+.45)/.85));base=2.2+.55*math.sin(x*.11)*math.sin(y*.09)
   if r<.53:z=base+.8*(r/.53)**2
   elif r<1.0:z=base+((r-.53)/.47)**1.45*(30*back+3)
   else:z=base+(30*back+3)*max(.32,1-(r-1)*.65)
   # Jagged rim rhythm chiefly changes silhouette, not color noise.
   ridge=math.exp(-((r-.99)/.20)**2);z+=ridge*back*(2.2*math.sin(angle*13)+1.4*math.sin(angle*21+.6))
   # A low, finite front rock threshold and valley outlet, lower than bowl shoulders.
   if y<-14 and abs(x)<12:
    mask=max(0,1-abs(x)/12);throat=2.4+1.3*math.exp(-((y+19)/4)**2)
    z=z*(1-mask)+throat*mask
   vs.append((x,y,max(.4,z)))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+nx+1
   if (i+j)%2:fs.extend([(a,b,b+1),(a,b+1,a+1)])
   else:fs.extend([(a,b,a+1),(a+1,b,b+1)])
 perimeter=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 o=len(vs)
 for v in perimeter:x,y,z=vs[v];vs.append((x,y,0))
 for k,a in enumerate(perimeter):q=(k+1)%len(perimeter);fs.append((a,o+k,o+q,perimeter[q]))
 fs.append(tuple(o+k for k in range(len(perimeter)-1,-1,-1)));part('continuous_excavated_cirque_terrain_closed_cutaway',vs,fs,'rock')
def frostwork():
 import random
 rng=random.Random(cfg['seed'])
 # Irregular ellipsoidal host, small rock not display stand.
 n=18;rings=[]
 for j in range(7):
  t=-math.pi/2+.12+(math.pi-.24)*j/6
  ring=[]
  for k in range(n):
   a=k*math.tau/n;v=1+.12*math.sin(k*2.1+j*.8);ring.append((.080*math.cos(t)*math.cos(a)*v,.064*math.cos(t)*math.sin(a)*v,.033+.031*math.sin(t)*v))
  rings.append(ring)
 loft('small_irregular_limestone_host',rings,'host')
 clusters=[(-.047,-.018,.053,(-.6,-.2,.85)),(.043,-.023,.053,(.6,-.2,.9)),(.004,.028,.061,(.03,.2,1)),(-.039,.031,.052,(-.45,.6,.8)),(.045,.030,.050,(.55,.5,.8))]
 for ci,(x,y,z,axis) in enumerate(clusters):
  origin=Vector((x,y,z));ellipsoid('five_small_nodular_growth_origins',tuple(origin),(.010,.009,.008),'ivory',10,4);ax=Vector(axis).normalized();u=ax.cross(Vector((0,1,0))).normalized();v=ax.cross(u).normalized()
  for k in range(17):
   angle=k*2.399963;spread=.20+.62*((k%7)/6);d=(ax+spread*(math.cos(angle)*u+math.sin(angle)*v)).normalized();length=.034+.029*rng.random();tip=origin+d*length;mat='ivory' if k%3 else 'coolneedle'
   tube('five_radiating_bundles_straight_acicular_primary_needles',[tuple(origin),tuple(origin+d*length*.86),tuple(tip)],[.0010,.00055,.000025],mat,5)
   if k%2==0:
    start=origin+d*length*.53
    for q in [-1,1]:
     branch=(d+.50*q*u+.32*v*math.sin(angle)).normalized();end=start+branch*(.012+.010*rng.random())
     tube('finer_straight_secondary_acicular_sprigs',[tuple(start),tuple(start*.18+end*.82),tuple(end)],[.00040,.00021,.000018],mat,4)
{'collinsium':collinsium,'yardang':yardang,'glacial-cirque':cirque,'aragonite-frostwork':frostwork}[slug]()

for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if slug=='yardang':
  obj.data.materials.append(m['lightlayer']);obj.data.materials.append(m['darklayer'])
  for poly in obj.data.polygons:
   z=sum(obj.data.vertices[i].co.z for i in poly.vertices)/len(poly.vertices)
   poly.material_index=1 if .65<z<.84 or 1.46<z<1.64 else 2 if .38<z<.48 or 1.12<z<1.24 else 0
 if slug=='glacial-cirque':
  for key in ['rocklight','rockdark','snow']:obj.data.materials.append(m[key])
  for poly in obj.data.polygons:
   c=poly.center;x,y,z=c;rr=math.sqrt((x/33)**2+((y-4)/32)**2)
   poly.material_index=3 if y>8 and .65<rr<.92 and 10<z<24 and math.sin(x*.6+y*.18)>.55 else 1 if poly.normal.z>.72 else 2 if poly.normal.y<-.3 else 0
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
