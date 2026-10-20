# SPDX-License-Identifier: MIT
"""Original batch71 geometry authored after complete immutable14:30:50Z freezes."""
import bpy,sys,json,math,argparse,pathlib,random
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed']);groups={}
def part(name,vs,fs,mat):
 v,f=groups.setdefault((name,mat),([],[]));n=len(v);v.extend(vs);f.extend([tuple(n+i for i in face) for face in fs])
def loft(name,rings,mat):
 n=len(rings[0]);vs=[p for ring in rings for p in ring];fs=[tuple(range(n-1,-1,-1))]
 for j in range(len(rings)-1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 fs.append(tuple((len(rings)-1)*n+i for i in range(n)));part(name,vs,fs,mat)
def tube(name,pts,rs,mat,n=6):
 rings=[]
 for i,p in enumerate(pts):
  d=Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(0,i-1)]);d.normalize();ref=Vector((0,0,1)) if abs(d.z)<.95 else Vector((1,0,0));u=d.cross(ref).normalized();v=d.cross(u).normalized();rings.append([tuple(Vector(p)+rs[i]*(u*math.cos(j*math.tau/n)+v*math.sin(j*math.tau/n))) for j in range(n)])
 loft(name,rings,mat)
def multi(name,vs,fs,mats):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,mats):p.material_index=keys.index(k)
 return o

def eldonia():
 n=128;nr=20;vs=[];fs=[];mats=[]
 # Complete closed lenticular soft body. Two polar surfaces join continuously at margin.
 def upper(x,y):
  r=math.hypot(x,y);ang=math.atan2(y,x);return .024+.0058*math.sqrt(max(0,1-(r/.075)**2))+.00022*math.sin(ang*49+math.sin(ang*7))*(r/.075)**.6
 def lower(x,y):
  r=math.hypot(x,y);return .0235-.0046*math.sqrt(max(0,1-(r/.075)**2))
 for surface in [0,1]:
  vs.append((0,0,upper(0,0) if surface==0 else lower(0,0)))
  for j in range(1,nr+1):
   for i in range(n):
    t=i*math.tau/n;r=.075*j/nr*(1+.007*math.sin(t*5)+.004*math.sin(t*11));x,y=r*math.cos(t),r*math.sin(t);z=upper(x,y) if surface==0 else lower(x,y)
    if surface==1:
     # Actual ventral apertures are shallow pits, no dorsal hole.
     for cx,cy,rad,depth in [(.026,-.012,.004,.0019),(.032,.013,.0023,.0014)]:z+=depth*math.exp(-((x-cx)**2+(y-cy)**2)/(rad*rad*.6))
    vs.append((x,y,z))
 off=1+nr*n
 def projection(x,y):
  # Deliberate flush color-coded internal-anatomy projection. NOT external tube.
  t=math.atan2(y,x);q=(-t)%math.tau;r=math.hypot(x,y)
  if .22<q<5.50:
   center=.034+.0035*math.sin(q*.7);width=.0058 if q<3.9 else .0028
   if abs(r-center)<width:return True
  # Short pharynx leading from off-centre mouth to start of clockwise stomach arc.
  return .022<x<.038 and -.014<y<-.007 and abs(y+.011)<.003
 for surf in [0,1]:
  o=surf*off
  for i in range(n):
   f=(o,o+1+i,o+1+(i+1)%n);fs.append(f);mats.append('body')
  for j in range(nr-1):
   for i in range(n):
    aa=o+1+j*n+i;bb=o+1+j*n+(i+1)%n;cc=aa+n;dd=bb+n
    for f in [(aa,cc,dd),(aa,dd,bb)]:
     x=sum(vs[v][0] for v in f)/3;y=sum(vs[v][1] for v in f)/3;mat='body'
     if surf==0 and projection(x,y):mat='projection'
     elif surf==0 and i%5==0:mat='rays'
     elif surf==1 and (((x-.026)**2+(y+.012)**2)<.0032**2 or ((x-.032)**2+(y-.013)**2)<.002**2):mat='openings'
     fs.append(f);mats.append(mat)
 for i in range(n):q=(i+1)%n;fs.append((1+(nr-1)*n+i,1+(nr-1)*n+q,off+1+(nr-1)*n+q,off+1+(nr-1)*n+i));mats.append('body')
 o=multi('whole_soft_disc_with_flush_internal_anatomy_projection',vs,fs,mats);o['teaching_visualization']='Flush color-coded internal gut projection, NOT natural exposed organ or pigmentation';o['gut_direction']='clockwise in dorsal +Z view';o['scope']='Complete E.ludwigi body; ecology and affinity uncertain'
 # Exactly two oral trunks, branch tips stay in short paired oral fans, no marginal fringe.
 for s in [-1,1]:
  pts=[(.026,-.012,.019),(.026+s*.003,-.017,.014),(.025+s*.009,-.027,.009),(.024+s*.014,-.039,.006)]
  tube('paired_dendritic_oral_tentacles',pts,[.0019,.0018,.0012,.00035],'tentacles',8)
  for j in range(1,5):
   t=j/5;base=Vector(pts[1]).lerp(Vector(pts[3]),t)
   for side in [-1,1]:
    tip=base+Vector((s*.004+side*.0025,-.0035+side*.0015,-.0006));mid=base.lerp(tip,.65)+Vector((0,-.0007,.0003));tube('paired_dendritic_oral_tentacles',[tuple(base),tuple(mid),tuple(tip)],[.0007,.0005,.00012],'tentacles')
    if j in [2,4]:
     twig=mid+Vector((side*.002,-.0015,.0001));tube('paired_dendritic_oral_tentacles',[tuple(mid),tuple(twig)],[.00035,.00008],'tentacles',5)

def roche():
 # Smooth upglacier long stoss then abrupt irregular lee, ONE continuous bedrock volume.
 xs=[-18,-16,-13,-10,-7,-4,-1,2,5,7.5,8.5,9.1,9.8,11,14,18];heights=[.6,1,1.8,2.8,3.9,4.9,5.8,6.6,7.3,7.7,7.5,6.3,3.4,1.1,.7,.5];ny=20;vs=[];fs=[];mats=[]
 for j,(x,h) in enumerate(zip(xs,heights)):
  for i in range(ny+1):
   v=-1+2*i/ny;y=v*12*(.97+.03*math.sin(j*.8));xx=x+.21*math.sin(i*1.7+j*.4)*(math.sin(i*math.pi/ny));cross=max(0,1-v*v)**.55;z=.4+h*cross
   if x<8 and abs(v)<.8:
    for g in [-7.2,-4.3,-1.1,2.2,5.8]:z-=.10*math.exp(-((y-g-.1*math.sin(x*.4))/.22)**2)*math.sin((x+18)*math.pi/29)**2
   if 8<x<12:z+=.3*math.sin(i*1.9+j*.7)*cross
   vs.append((xx,y,z))
 for j in range(len(xs)-1):
  for i in range(ny):
   a=j*(ny+1)+i;b=a+1;c=a+ny+1;d=c+1
   for f in ([(a,c,b),(b,c,d)] if (j+i)%2 else [(a,c,d),(a,d,b)]):fs.append(f);mats.append('fracture' if xs[j]>=8 else 'bedrock')
 boundary=list(range(ny+1))+[j*(ny+1)+ny for j in range(1,len(xs))]+[(len(xs)-1)*(ny+1)+i for i in range(ny-1,-1,-1)]+[j*(ny+1) for j in range(len(xs)-2,0,-1)];bottom=len(vs)
 vs.extend([(vs[a][0],vs[a][1],0) for a in boundary])
 for i,a in enumerate(boundary):q=(i+1)%len(boundary);fs.append((a,boundary[q],bottom+q,bottom+i));mats.append('ground')
 fs.append(tuple(bottom+i for i in range(len(boundary)-1,-1,-1)));mats.append('ground');multi('coherent_bedrock_stoss_and_plucked_lee',vs,fs,mats)

def maar():
 n=96;nr=25;vs=[(0,0,6)];fs=[];mats=[]
 def shape(t,r):
  # broad below-grade floor, steep walls, only2m rim over country20m
  if r<.32:z=6+.35*(r/.32)**2
  elif r<.62:z=6.35+15.0*((r-.32)/.30)**1.15
  elif r<.73:z=21.35+.55*math.sin((r-.62)/.11*math.pi)
  elif r<.91:z=21.35-1.35*((r-.73)/.18)
  else:z=20
  z+=(.38*math.sin(t*5+.5)+.21*math.sin(t*13))*math.sin(r*math.pi)**2
  if .35<r<.68:z+=.38*math.sin(t*19+r*8)*math.sin((r-.35)/.33*math.pi)
  return z
 for j in range(1,nr+1):
  r=j/nr
  for i in range(n):
   t=i*math.tau/n;v=r*(1+.022*math.sin(t*5)+.012*math.sin(t*9));vs.append((60*v*math.cos(t),55*v*math.sin(t),shape(t,r)))
 for i in range(n):fs.append((0,1+i,1+(i+1)%n));mats.append('floor')
 for j in range(nr-1):
  for i in range(n):
   a=1+j*n+i;b=1+j*n+(i+1)%n;c=a+n;d=b+n;r=(j+1.5)/nr;t=(i+.5)*math.tau/n
   for f in [(a,c,d),(a,d,b)]:
    fs.append(f)
    mats.append('floor' if r<.34 else ('wallshade' if math.sin(t*7+r*9)>.3 else 'wall') if r<.62 else 'ejecta' if r<.87+.03*math.sin(t*4) else 'country')
 end=1+(nr-1)*n;bot=len(vs);vs.extend([(vs[end+i][0],vs[end+i][1],0) for i in range(n)])
 for i in range(n):q=(i+1)%n;fs.append((end+i,bot+i,bot+q,end+q));mats.append('country')
 fs.append(tuple(bot+i for i in range(n-1,-1,-1)));mats.append('country');o=multi('below_country_grade_maar_and_low_ejecta_apron',vs,fs,mats);o['country_surface_z_m']=20.;o['crater_floor_z_m']=6.;o['rim_nominal_z_m']=22.

def terrace():
 # Across-valley profile includes broad benches, risers, lower active floodplain, riverbed.
 n=28;profile=[(-40,11),(-31,11),(-23,11),(-16,11),(-14.8,10.8),(-12.8,3.2),(-10.5,3),(-5,3),(-3.9,2.3),(-2.8,1.9),(2.8,1.9),(3.9,2.3),(5,3),(10.5,3),(12.8,3.2),(14.8,10.8),(16,11),(23,11),(31,11),(40,11)];w=len(profile);vs=[];fs=[];mats=[]
 for j in range(n+1):
  y=-35+70*j/n;c=2.1*math.sin(y/16)
  for i,(x,z) in enumerate(profile):
   f=math.sin(math.pi*(x+40)/80);xx=x+c*f+.38*math.sin(y*.31+i*.7)*f;zz=z+(.12*math.sin(y*.33+x*.18) if z>3 else .025*math.sin(y*.31));vs.append((xx,y,zz))
 for j in range(n):
  for i in range(w-1):
   a=j*w+i;b=a+1;c=a+w;d=c+1;z=(profile[i][1]+profile[i+1][1])/2;mat='bench' if z>10.9 else 'sediment' if z>4 else 'floodplain'
   for f in [(a,c,d),(a,d,b)]:fs.append(f);mats.append(mat)
 boundary=list(range(w))+[j*w+w-1 for j in range(1,n+1)]+[n*w+i for i in range(w-2,-1,-1)]+[j*w for j in range(n-1,0,-1)];bot=len(vs);vs.extend([(vs[a][0],vs[a][1],0) for a in boundary])
 for i,a in enumerate(boundary):q=(i+1)%len(boundary);fs.append((a,boundary[q],bot+q,bot+i));mats.append('shade' if i%9<3 else 'sediment')
 fs.append(tuple(bot+i for i in range(len(boundary)-1,-1,-1)));mats.append('sediment');o=multi('abandoned_floodplain_benches_clear_risers_and_lower_active_floodplain',vs,fs,mats);o['terrace_top_z_m']=11.;o['active_floodplain_z_m']=3.;o['riser_height_m']=8.
 rings=[]
 for j in range(n+1):
  y=-35+70*j/n;c=2.1*math.sin(y/16);width=3.65+.14*math.sin(y*.24);rings.append([(c-width,y,2),(c+width,y,2),(c+width,y,2.6),(c-width,y,2.6)])
 loft('opaque_active_river_water_volume',rings,'water')
{'eldonia':eldonia,'roche-moutonnee':roche,'maar-crater':maar,'river-terrace':terrace}[slug]()
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
