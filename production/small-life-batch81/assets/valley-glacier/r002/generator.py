# SPDX-License-Identifier: MIT
"""Original batch81 original geometry, authored after complete immutable16:58:19Z design freezes."""
import bpy,sys,json,math,argparse,pathlib,random
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed'])
def multi(name,vs,fs,ms):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,ms):p.material_index=keys.index(k)
 return o

def grid(name,nx,ny,coords,matfn):
 vs=[];fs=[];ms=[]
 for j in range(ny+1):
  for i in range(nx+1):vs.append(coords(i/nx,j/ny,i,j))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(matfn(sum(vs[k][0] for k in f)/3,sum(vs[k][1] for k in f)/3,sum(vs[k][2] for k in f)/3,i,j))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];base=len(vs)
 for v in boundary:vs.append((vs[v][0],vs[v][1],0))
 for i,v in enumerate(boundary):q=(i+1)%len(boundary);fs.append((v,base+i,base+q,boundary[q]));ms.append(list(m)[-1])
 center=len(vs);vs.append((0,0,0))
 for i in range(len(boundary)):fs.append((center,base+(i+1)%len(boundary),base+i));ms.append(list(m)[-1])
 return multi(name,vs,fs,ms)

def charnia():
 def p(u,v,i,j):
  x=(u-.5)*.12;y=(v-.5)*.26
  x*=1-.16*abs(2*v-1)**5+.02*math.sin(12*v);y*=1-.07*abs(2*u-1)**5
  z=.011+.00012*math.sin(111*x+57*y)
  t=(y+.105)/.21;axis=.0035*math.sin(5*t)*math.sin(math.pi*max(0,min(1,t)))
  if 0<t<1:
   w=.029*(1-t)**.64*min(1,t/.10)**.35
   a=abs(x-axis);xn=a/max(w,1e-8)
   if xn<1:
    side=1 if x>axis else 0
    # Closed flattened body region; staggered sigmoidal primary units, no plant leaflets.
    taper=max(0,1-xn*xn)**.33
    z-=.00095*taper
    phase=t*23-.47*side-.40*xn+.20*xn*xn
    boundary=math.exp(-(math.sin(math.pi*phase)/.24)**2)
    z-=.00066*boundary*taper
    # Nested furled secondary relief inside broad primary units.
    secondary=math.exp(-(math.sin(math.pi*(xn*6.2+.30*math.sin(math.tau*phase)))/.33)**2)
    z-=.00023*secondary*(1-boundary)*taper
    z+=.00023*math.exp(-((x-axis)/.0008)**2)*taper
  return x,y,z
 def mat(x,y,z,i,j):return 'impression' if z<.01045 else 'sandstone'
 o=grid('Charnia_masoni_fossil_impression_BGS_GSM105873_informed_not_facsimile',46,138,p,mat);o['scope']='Shallow fossil impression only. Alternating nested branches. No living underside or holotype equivalence.'

def inselberg():
 def p(u,v,i,j):
  x=(u-.5)*1100*(1-.11*abs(2*v-1)**5);y=(v-.5)*900*(1-.10*abs(2*u-1)**5)
  xx=(x+24)/260;yy=(y-12)/184;r=math.sqrt(xx*xx+yy*yy);theta=math.atan2(yy,xx)
  rim=1+.05*math.sin(3*theta+.7)+.025*math.cos(5*theta)
  q=r/rim;z=4+.5*math.sin(x*.013+y*.017)
  if q<1:
   h=168*max(0,1-q*q)**.38*(1+.08*math.sin(theta)*q)
   h-=3.2*math.sin(13*theta+.6)**12*q*q
   z+=h
  return x,y,z
 def mat(x,y,z,i,j):return 'rock' if z>13 else 'weathered' if z>6 else 'plain'
 o=grid('isolated_rounded_asymmetric_residual_rock_hill_surrounded_low_plain',66,64,p,mat);o['scope']='Generic inselberg not site reconstruction. No separate exfoliation shell, flat mesa cap or volcanic origin assertion.'

def circles():
 centers=[(-3.5,-2.2,1.42,1.24,.1),(-.25,-2.05,1.55,1.15,.7),(3.0,-1.55,1.36,1.42,1.8),(-2.0,1.25,1.35,1.6,2.3),(1.15,1.65,1.57,1.35,3.4)]
 # Fixed irregular clast relief sampled on one integral surface, not overlapping separate rocks.
 clasts=[]
 for cx,cy,rx,ry,ph in centers:
  for k in range(115):
   a=rng.random()*math.tau;spread=rng.gauss(0,.16);rr=1+spread+.05*math.sin(3*a+ph)
   clasts.append((cx+rx*rr*math.cos(a),cy+ry*rr*math.sin(a),rng.uniform(.055,.14),rng.uniform(.035,.13)))
 def density(x,y):
  ds=[]
  for cx,cy,rx,ry,ph in centers:
   a=math.atan2((y-cy)/ry,(x-cx)/rx);r=math.sqrt(((x-cx)/rx)**2+((y-cy)/ry)**2);ds.append(abs(r-(1+.055*math.sin(3*a+ph)+.035*math.cos(5*a+ph))))
  return math.exp(-(min(ds)/.19)**2)
 def p(u,v,i,j):
  x=(u-.5)*12*(1-.13*abs(2*v-1)**6);y=(v-.5)*10*(1-.12*abs(2*u-1)**5)
  # Unequal jitter retains cell orientation and avoids regular triangular clast grids.
  if 0<i<76:x+=.035*math.sin(i*73+j*93)
  if 0<j<70:y+=.035*math.cos(i*53+j*67)
  d=density(x,y);z=.19+.010*math.sin(3*x+2*y)+.035*d
  for cx,cy,r,h in clasts:
   q=((x-cx)/r)**2+((y-cy)/(r*.78))**2
   if q<1:z+=h*(1-q)**.6
  return x,y,z
 def mat(x,y,z,i,j):
  d=density(x,y)
  return 'stone' if d>.4 and z>.245 else 'gravel' if d>.25 else 'soil'
 o=grid('five_natural_frost_sorted_fine_centers_diffuse_coarse_clast_margins',76,70,p,mat);o['scope']='Frost sorted ground not mechanical rings. Clast relief integral in closed low terrain patch.'

def glacier():
 def p(u,v,i,j):
  y=(v-.5)*1600;center=65*math.sin((v-.1)*4.8);width=110+40*v+70*max(0,(v-.78)/.22)
  x=(u-.5)*900*(1-.07*abs(2*v-1)**5)
  # Lateral sample distribution allocates enough ice crevasse detail without excessive terrain density.
  x=x
  d=abs(x-center)/width;base=10+v*130
  rock=base+math.sin(math.pi*min(1,max(0,(d-1)/2.65)))**.65*(170+70*math.sin(v*9+(0 if x<center else 1.8))**2)
  if d<1 and v>.065:
   rise=min(1,(v-.065)/.03);z=base+36*rise+8*(1-d*d)
   # Irregular shallow transverse cracks remain inside one continuous ice tongue.
   if .10<v<.50:
    phase=v*14+.12*math.cos((x-center)/80)+.03*math.sin(v*24)
    groove=math.exp(-(math.sin(math.pi*phase)/.38)**2)
    z-=min(10,6+4*d)*groove*(1-d*d)
  else:z=rock
  # Side slopes higher than tongue, not an empty valley. Avoid all coplanar skins.
  if d>=1:z=rock+36*max(0,1-(d-1)/.36)*min(1,max(0,(v-.065)/.03))
  z+=7.0*math.sin(x*.033+y*.019)*(min(1,max(0,d-1)))
  return x,y,max(1,z)
 def mat(x,y,z,i,j):
  v=(y+800)/1600;center=65*math.sin((v-.1)*4.8);width=110+40*v+70*max(0,(v-.78)/.22);d=abs(x-center)/width
  if d<.97 and v>.076:
   if v>.87+.020*math.cos(x*.025):return 'snow'
   return 'crevasse' if .10<v<.50 and z<10+v*130+36+8*(1-d*d)-3 else 'ice'
  return 'bedrock'
 o=grid('continuous_confined_valley_glacier_solid_tongue_and_higher_bedrock_walls',64,84,p,mat);o['scope']='Generic valley glacier not piedmont, no exact site. Ice never severed by shallow cracks.'

{'charnia':charnia,'inselberg':inselberg,'patterned-stone-circles':circles,'valley-glacier':glacier}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
