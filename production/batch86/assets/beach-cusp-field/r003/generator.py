# SPDX-License-Identifier: MIT
"""Original batch86 geometry. Authored after all four immutable premodel freezes."""
import bpy,sys,json,math,argparse,pathlib,random
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed'])
def multi(name,vs,fs,ms):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,ms):p.material_index=keys.index(k)
 return o

def grid_solid(name,nx,ny,coords,matfn):
 vs=[coords(i/nx,j/ny,i,j) for j in range(ny+1) for i in range(nx+1)];fs=[];ms=[]
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in ([(a,b,d),(a,d,c)] if (i+j)%2==0 else [(a,b,c),(b,d,c)]):fs.append(f);ms.append(matfn([vs[k] for k in f],i,j))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];base=len(vs)
 for v in boundary:vs.append((vs[v][0],vs[v][1],0))
 for i,v in enumerate(boundary):q=(i+1)%len(boundary);fs.append((v,base+i,base+q,boundary[q]));ms.append('cut')
 center=len(vs);vs.append((0,0,0))
 for i in range(len(boundary)):fs.append((center,base+(i+1)%len(boundary),base+i));ms.append('cut')
 return multi(name,vs,fs,ms)

def beach():
 # Coordinate rows follow the true scalloped shoreline and shallow ridge/swale geometry.
 def shore(x):
  u=(x+60)/120;phase=math.tau*(4*u+.035*math.sin(math.tau*u));c=(1+math.cos(phase))/2
  return -2-10*(c**1.65)*(1+.10*math.sin(u*8)),c
 rows=[(0,'sea'),(.15,'sea'),(.3,'sea'),(.45,'sea'),(.5,'shore'),(.55,'land'),(.62,'land'),(.72,'land'),(.85,'land'),(1,'land')]
 def p(u,v,i,j):
  x=(u-.5)*120;s,c=shore(x)
  if v<=.5:y=-30+(s+30)*(v/.5);z=.75
  else:
   t=(v-.5)*2;y=s+(30-s)*t
   # Low sediment horn crests fade inland, real relief not a painted boundary alone.
   z=.75+3.65*t+2.8*c*math.sin(math.pi*min(1,t/.5))*math.exp(-t)+.07*math.sin(x*.12)*t
  return (x,y,z)
 o=grid_solid('continuous_swash_beach_five_horns_four_crescent_bays',96,20,p,lambda ps,i,j:'water' if j<10 else 'damp_sand' if j<13 else 'dry_sand');o['scope']='Generic beach cusp field. Scalloped row geometry and low horn/bay relief; not dunes, DEM, tide or named site.'

def cinder():
 n=96;levels=[(0,94),(18,94),(36,98),(55,108),(73,124),(88,143),(100,150),(115,146),(135,136),(165,117),(205,92),(250,62),(290,35),(325,13),(345,5)]
 vs=[];fs=[];ms=[]
 # Interior radial center is a single point, avoiding a zero-area ring.
 vs.append((0,0,94));rings=levels[1:]
 for j,(r,z) in enumerate(rings):
  for i in range(n):
   t=math.tau*i/n;asym=1+.04*math.sin(t*3+.6)+.025*math.cos(t*5)
   relief=(2.5*math.sin(t*3+.3)+1.4*math.cos(t*7))*(r/100 if r<100 else max(0,(345-r)/245))
   groove=-(1.7+.9*math.sin(t*2))*max(0,math.cos(t*13+.8))**10*(1 if 115<r<325 else .3)
   vs.append((r*asym*math.cos(t),r*.955*asym*math.sin(t),z+relief+groove))
 for i in range(n):fs.append((0,1+i,1+(i+1)%n));ms.append('weathered')
 for j in range(len(rings)-1):
  for i in range(n):
   q=(i+1)%n;a=1+j*n+i;b=1+j*n+q;c=a+n;d=b+n
   region='oxidized' if j in (3,4,5,6) and math.sin(i*math.tau/n+1)>.35 else 'weathered' if j<4 else 'scoria'
   for f in [(a,c,d),(a,d,b)]:fs.append(f);ms.append(region)
 # Close the integrated apron and the whole volume underneath.
 base=len(vs)
 for i in range(n):x,y,z=vs[1+(len(rings)-1)*n+i];vs.append((x,y,0))
 bot=len(vs);vs.append((0,0,0))
 for i in range(n):q=(i+1)%n;fs.extend([(1+(len(rings)-1)*n+i,base+i,base+q,1+(len(rings)-1)*n+q),(bot,base+q,base+i)]);ms.extend(['cut','cut'])
 o=multi('compact_scoria_cone_continuous_flank_uneven_rim_and_depressed_bowl',vs,fs,ms);o['scope']='Generic intact cinder-cone form, dry broad crater, no activity/site claim.'

def karst():
 # Four adjacent plain quadrants with integral lofted towers. Shared plane edges touch,
 # never overlap visible surfaces; lower cut faces are internal only at quadrant joins.
 towers=[(-225,155,112,96,224,.4,(-450,0,0,380)),(205,180,87,77,174,1.7,(0,450,0,380)),(215,-190,95,82,128,3.5,(0,450,-380,0)),(-225,-205,70,61,82,5.1,(-450,0,-380,0))]
 for k,(cx,cy,rx,ry,h,phase,box) in enumerate(towers):
  n=48;vs=[];fs=[];ms=[]
  levels=[(None,0),(1.43,.009),(1.16,.045),(.99,.15),(.94,.34),(.96,.37),(.88,.55),(.89,.58),(.81,.76),(.72,.88),(.53,.97),(.26,1.0)]
  for j,(r,zz) in enumerate(levels):
   for i in range(n):
    t=math.tau*i/n;ct=math.cos(t);st=math.sin(t)
    if r is None:
     rays=[]
     if ct>1e-9:rays.append((box[1]-cx)/ct)
     if ct<-1e-9:rays.append((box[0]-cx)/ct)
     if st>1e-9:rays.append((box[3]-cy)/st)
     if st<-1e-9:rays.append((box[2]-cy)/st)
     q=min(rays);x=cx+q*ct;y=cy+q*st;z=12
    else:
     wave=1+.11*math.sin(t*3+phase)+.065*math.cos(t*5-phase)+.028*math.sin(t*11+.2*j)
     # Correlated dissolution flutes and slight offset crowns, not masonry grids.
     x=cx+rx*r*ct*wave+rx*.045*math.sin(j*.5+phase)*zz
     y=cy+ry*r*st*wave+ry*.07*math.cos(j*.36+phase)*zz
     z=12+h*zz+h*(.024*math.sin(t*3+phase)+.016*math.cos(t*5))*zz
    vs.append((x,y,z))
  for j in range(len(levels)-1):
   for i in range(n):
    q=(i+1)%n;a=j*n+i;b=j*n+q;c=a+n;d=b+n
    for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append('plain' if j==0 else 'weathered' if j in [1,4,6,9,10] else 'limestone')
  top=len(vs);vs.append((cx+rx*.025,cy-ry*.04,12+h*1.025))
  for i in range(n):fs.append((top,(len(levels)-1)*n+i,(len(levels)-1)*n+(i+1)%n));ms.append('weathered')
  base=len(vs)
  for i in range(n):x,y,z=vs[i];vs.append((x,y,0))
  bot=len(vs);vs.append((cx,cy,0))
  for i in range(n):q=(i+1)%n;fs.extend([(i,base+i,base+q,q),(bot,base+q,base+i)]);ms.extend(['cut','cut'])
  o=multi('fenglin_tower_'+str(k+1)+'_integrated_plain_quadrant',vs,fs,ms);o['scope']='Generic tower karst, unequal steep dissolved limestone towers with low corridors. Boundary planes meet without visible surface overlap.'

def zoster():
 groups={k:[[],[]] for k in m}
 def tube(pts,radii,mat,sides=6):
  vs,fs=groups[mat];off=len(vs);ps=[Vector(p) for p in pts]
  for j,p in enumerate(ps):
   t=(ps[min(j+1,len(ps)-1)]-ps[max(0,j-1)]).normalized();u=t.cross(Vector((0,1,0)))
   if u.length<.1:u=t.cross(Vector((1,0,0)))
   u.normalize();v=t.cross(u).normalized()
   for k in range(sides):q=p+radii[j]*(math.cos(math.tau*k/sides)*u+math.sin(math.tau*k/sides)*v);vs.append(tuple(q))
  fs.append(tuple(off+k for k in reversed(range(sides))))
  for j in range(len(ps)-1):
   for k in range(sides):q=(k+1)%sides;a=off+j*sides+k;b=off+j*sides+q;fs.append((a,b,b+sides,a+sides))
  fs.append(tuple(off+(len(ps)-1)*sides+k for k in range(sides)))
 def capsule(center,azimuth,width=.0025,height=.00165,thick=.00065):
  vs,fs=groups['capsule'];off=len(vs);p=Vector(center);u=Vector((math.cos(azimuth),math.sin(azimuth),0));v=Vector((0,0,1));w=u.cross(v);n=10
  # A flattened two-valve lens with a modest basal reniform notch, not a berry sphere.
  for sign in [-1,1]:
   for i in range(n):
    t=math.tau*i/n;x=width*.5*math.cos(t);z=height*.5*math.sin(t)
    if z<0:z+=height*.22*math.exp(-(x/(width*.21))**2)
    q=p+u*x+v*z+w*thick*.22*sign;vs.append(tuple(q))
  front=len(vs);vs.append(tuple(p+w*thick*.5));back=len(vs);vs.append(tuple(p-w*thick*.5))
  for i in range(n):q=(i+1)%n;fs.extend([(back,off+q,off+i),(front,off+n+i,off+n+q),(off+i,off+q,off+n+q,off+n+i)])
 # Six short radial rhizome runners create connected horizontal branch geometry.
 roots_z=.019
 for k in range(6):
  t=math.tau*k/6+.15;d=Vector((math.cos(t),math.sin(t),0));pts=[(0,0,roots_z),tuple(d*.003+Vector((0,0,.0195))),tuple(d*.008+Vector((0,0,.020))),tuple(d*.015+Vector((0,0,.022)))]
  tube(pts,[.0008,.00075,.00055,.00035],'rhizome')
 # Twenty-four branching systems yield forty-eight naked fertile upper axes.
 for k in range(24):
  t=math.tau*k/24+.22*math.sin(k*2.7);d=Vector((math.cos(t),math.sin(t),0));side=Vector((-math.sin(t),math.cos(t),0));rad=.025+.027*((k%5)/4);ht=.082+.009*math.sin(k*.8)+.008*(1-rad/.052)
  p0=d*.004+Vector((0,0,roots_z));p1=d*(rad*.47)+Vector((0,0,.022+.004*(k%3)));p2=d*(rad*.78)+Vector((0,0,.040));fork=d*(rad*.90)+Vector((0,0,.058+.006*math.sin(k)))
  tube([p0,p1,(p1+p2)*.5+Vector((0,0,-.002)),p2,fork],[.00058,.00056,.00054,.00052,.00049],'axis')
  # Clearly visible low H/K-like offshoot joining upward stems, not a fern rosette.
  if k%4==0:
   v0=p1;v1=p1+side*.008;v2=v1+Vector((0,0,.014));tube([v0,v1,v2],[.00042,.00037,.00028],'axis')
  for sign in [-1,1]:
   top=d*(rad+(.002 if sign==1 else -.003))+side*(.0035*sign)+Vector((0,0,ht+.020+.003*sign))
   mid=fork*.43+top*.57+side*.001*sign
   tube([fork,mid,top],[.00048,.00046,.00034],'axis')
   # Two irregular lateral capsule stalks, both with the main axis continuing beyond.
   for q,f in enumerate([.61+.05*math.sin(k+sign),.92+.025*math.cos(k*1.4)]):
    p=fork.lerp(top,f);a0=t+sign*(1.0+q*.55)+.7*math.sin(k*2.1);v=Vector((math.cos(a0),math.sin(a0),0));tip=p+v*.00072+Vector((0,0,.0013));tube([p,tip],[.00028,.00026],'axis',5);capsule(tip+Vector((0,0,.0006)),a0,width=.00275+.00015*math.sin(k+q),height=.0018,thick=.0008)
 for k in range(28):
  t=k*2.399963;rr=.0043*math.sqrt((k+.5)/28);x=rr*math.cos(t);y=rr*math.sin(t);z0=.0197;end=.0010+.002*(.5+.5*math.sin(k))
  tube([(x,y,z0),(x+.0008*math.sin(k),y+.0007*math.cos(k),.012),(x+.0013*math.sin(k+.7),y+.001*math.cos(k+.2),.006),(x+.0015*math.sin(k),y+.0014*math.cos(k),end)],[.00027,.00023,.00016,.000025],'rhizome',5)
 for key,(vs,fs) in groups.items():mesh_object('zosterophyllum_'+key+'_editable_component',vs,fs,m[key],col)

{'zosterophyllum':zoster,'beach-cusp-field':beach,'cinder-cone':cinder,'tower-karst':karst}[slug]()
ground_asset(col,center_xy=True)
root=bpy.data.objects[col['asset_root']]
for obj in col.all_objects:
 if obj.type=='MESH':
  world=obj.matrix_world.copy();obj.data.transform(world);obj.matrix_world.identity();obj.parent=None
root.location=(0,0,0);bpy.context.view_layer.update()
source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
