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


# ORIGINAL batch65 asset geometry authored after frozen premodel brief.
def burgessochaeta():
 rings=[]
 for i in range(85):
  t=i/84;y=-.023+.047*t;x=.0013*math.sin(t*math.tau);r=(.00065+.00135*math.sin(math.pi*t)**.45)*(1-.055*math.cos(t*math.tau*20));z=.003
  rings.append([(x+r*math.cos(j*math.tau/10),y,z+r*.72*math.sin(j*math.tau/10)) for j in range(10)])
 loft('continuous_shallow_annulated_soft_trunk',rings,'body')
 ellipsoid('differentiated_head',(0,-.0245,.003),(.0012,.002,.001),'body',10,4)
 ellipsoid('small_terminal_mouth',(0,-.0263,.0028),(.00038,.00015,.0003),'mouth',8,3)
 for sign in [-1,1]:tube('exactly_two_smooth_anterior_palps',[(sign*.00065,-.0255,.003),(sign*.0015,-.028,.003),(sign*.0023,-.030,.0027)],[.00022,.00015,.000035],'lobe',6)
 for station in range(20):
  t=(station+.5)/20;y=-.0228+.0455*t;x=.0013*math.sin(t*math.tau);r=.00065+.00135*math.sin(math.pi*t)**.45
  for sign in [-1,1]:
   for ramus in [-1,1]:
    z=.003+ramus*.00055;origin=Vector((x+sign*r*.8,y,z));end=origin+Vector((sign*.00115,-.00015,ramus*.00032))
    tube('uniform_equant_'+('notopodial' if ramus>0 else 'neuropodial')+'_lobes',[tuple(origin),tuple(end)],[.00040,.00030],'lobe',5)
    for k in range(5):
     a=-.55+1.1*k/4;direction=Vector((sign*math.cos(a),math.sin(a),ramus*.20)).normalized();length=.0023+.00045*math.sin(math.pi*k/4);tip=end+direction*length
     tube('lateral_five_simple_chaetae_per_ram us'.replace(' ',''),[tuple(end),tuple(tip)],[.000067,.000025],'bristle',3)
     for fork in [-1,1]:
      fork_tip=tip+direction*.00028+Vector((0,fork*.00010,0));tube('tiny_bifid_chaetal_tips',[tuple(tip),tuple(fork_tip)],[.000024,.000009],'bristle',3)

def stalagmites():
 # Host is shallow irregular crust, not display pedestal.
 rings=[]
 for z,scale in [(0,.88),(.07,1),(.14,.91)]:
  rings.append([(1.15*scale*(1+.06*math.sin(i*2.3))*math.cos(i*math.tau/24),.85*scale*(1+.08*math.sin(i*1.7))*math.sin(i*math.tau/24),z) for i in range(24)])
 loft('low_irregular_floor_mineral_crust',rings,'floor')
 for ci,(x,y,h,r) in enumerate([(0,.27,2.1,.28),(-.61,.04,1.45,.23),(.60,.20,1.15,.24),(-.35,-.44,.83,.21),(.56,-.40,.55,.19)]):
  rings=[]
  for j in range(30):
   t=j/29;cap=math.sqrt(max(.0001,1-((t-.88)/.12)**2)) if t>.88 else 1
   radius=r*(1.4-.64*t+.07*math.cos(t*math.tau*9))*(cap if t>.88 else 1)
   rings.append([(x+.025*math.sin(t*3+ci)+radius*(1+.06*math.cos(i*3+ci))*math.cos(i*math.tau/14),y+radius*(1+.05*math.sin(i*2+ci))*math.sin(i*math.tau/14),.10+h*t) for i in range(14)])
  loft('rounded_solid_floor_stalagmite_'+str(ci+1),rings,'mineral')

def breccia():
 import random
 rng=random.Random(65)
 # Angular stepped coherent host, elliptical horizontal rings, closed base.
 n=18;rings=[]
 for j,(z,sx,sy) in enumerate([(0,1.45,1.0),(.35,1.64,1.10),(.95,1.50,1.02),(1.55,1.34,.93),(1.78,1.03,.69)]):
  rings.append([(sx*(1+.12*math.sin(i*2.6+j*.4))*math.cos(i*math.tau/n),sy*(1+.13*math.cos(i*1.8+j*.3))*math.sin(i*math.tau/n),z+.06*math.sin(i*2.4+j) if j else 0) for i in range(n)])
 loft('coherent_angular_matrix_outcrop',rings,'matrix')
 def clast(name,c,u,v,depth,size,mat):
  c=Vector(c);u=Vector(u);v=Vector(v);normal=u.cross(v).normalized();count=rng.choice([4,5,6]);angles=[i*math.tau/count+.10*rng.random() for i in range(count)];shape=[(math.cos(a)*size*(.7+.3*rng.random()),math.sin(a)*size*(.6+.4*rng.random())) for a in angles]
  vs=[tuple(c+u*x+v*y+normal*d) for d in [-depth*.65,depth*.35] for x,y in shape];fs=[tuple(range(count-1,-1,-1)),tuple(count+i for i in range(count))]+[(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)];part(name,vs,fs,mat)
 for k in range(60):
  a=k*2.399963;z=.22+1.28*((k%11)/10);rscale=1-.12*z
  c=(1.50*rscale*math.cos(a),1.025*rscale*math.sin(a),z);u=(-math.sin(a),math.cos(a),0);v=(0,0,1)
  clast('embedded_angular_surface_fragments',c,u,v,.15,.10+.23*rng.random(),['paleclast','ochreclast','darkclast'][k%3])
 for k in range(23):
  a=k*2.399963;r=.2+.7*((k%7)/6);c=(1.00*r*math.cos(a),.68*r*math.sin(a),1.73+.03*math.sin(k))
  clast('embedded_angular_crown_fragments',c,(1,0,0),(0,1,0),.17,.09+.20*rng.random(),['paleclast','ochreclast','darkclast'][k%3])

def landslide():
 # Cross section extruded with crescent scar rear edge. +Y is uphill.
 ys=[-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,4.8,5.2,6,8]
 curve=lambda y:.55+.034*(y+6)**2
 def solid_profile(name,ys,top,bottom,width,mat,curve_scar=False):
  vs=[];nx=16
  for j,y in enumerate(ys):
   for i in range(nx+1):
    x=-width+2*width*i/nx;yy=y
    if curve_scar and y>3:yy=y+.65*(1-(x/width)**2)*max(0,1-abs(y-4.8)/2)
    z=top(y,x);vs.append((x,yy,z))
  fs=[];topfaces=[]
  for j in range(len(ys)-1):
   for i in range(nx):
    a=j*(nx+1)+i;b=a+nx+1;fs.extend([(a,a+1,b+1),(a,b+1,b)]);topfaces.extend([len(fs)-2,len(fs)-1])
  perimeter=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,len(ys))]+[(len(ys)-1)*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(len(ys)-2,0,-1)]
  o=len(vs)
  for a in perimeter:x,y,z=vs[a];vs.append((x,y,bottom(y,x)))
  for k,a in enumerate(perimeter):q=(k+1)%len(perimeter);fs.append((a,o+k,o+q,perimeter[q]))
  fs.append(tuple(o+k for k in range(len(perimeter)-1,-1,-1)));part(name,vs,fs,mat)
 def base_top(y,x):
  if y<=4:return curve(y)
  if y<5.2:return curve(4)+(6.8-curve(4))*(y-4)/1.2
  return 6.8+.07*math.sin(x*.4)
 solid_profile('continuous_substrate_curved_listric_scarp',ys,base_top,lambda y,x:0,6,'earth',True)
 # Coherent displaced block with lower forward toe and a bench back-tilted toward uphill.
 by=[-7.5,-6.5,-5.5,-4.5,-3.5,-2.5,-1.5,0,1.5,3,3.8]
 def block_top(y,x):
  if y<-2.5:return 1.0+(y+7.5)/5*3.85+.06*math.cos(x*.5)
  return 4.85-.115*(y+2.5)+.04*math.cos(x*.6)
 solid_profile('coherent_displaced_backtilted_block_and_toe',by,block_top,lambda y,x:curve(y)+.075,4.9,'earthlight')
 # Curved thin band exposed at the two side cutaways, original educational abstraction.
 for sign in [-1,1]:
  path=[(sign*4.92,y,curve(y)+.06) for y in by]
  tube('exposed_curved_slip_interface_band',path,[.055]*len(path),'slipsurface',5)

{'burgessochaeta':burgessochaeta,'stalagmite-group':stalagmites,'breccia-outcrop':breccia,'rotational-landslide':landslide}[slug]()
for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if slug=='stalagmite-group' and mat=='mineral':
  obj.data.materials.append(m['light']);obj.data.materials.append(m['ochre'])
  for p in obj.data.polygons:p.material_index=1 if p.center.z>1.6 else 2 if int(p.center.z*16)%7==0 else 0
 if slug=='breccia-outcrop' and mat=='matrix':
  obj.data.materials.append(m['matrixlight'])
  for p in obj.data.polygons:p.material_index=1 if p.normal.z>.7 else 0
 if slug=='rotational-landslide':
  obj.data.materials.append(m['grass']);obj.data.materials.append(m['darkearth'])
  for p in obj.data.polygons:
   if 'displaced' in name:p.material_index=1 if p.normal.z>.7 else 0
   elif 'substrate' in name:p.material_index=1 if p.center.y>5.3 and p.normal.z>.7 else 2 if abs(p.normal.x)>.8 else 0

ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
