# SPDX-License-Identifier: MIT
"""Original batch62 full-volume geometry from frozen concepts and primary-source briefs."""
import bpy,sys,json,math,argparse,pathlib,datetime,hashlib
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True)
slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};groups={};gp=cfg['geometry_parameters']
def part(name,vs,fs,mat):
 v,f=groups.setdefault((name,mat),([],[]));n=len(v);v.extend(vs);f.extend([tuple(n+i for i in face) for face in fs])
def loft(name,rings,mat):
 n=len(rings[0]);vs=[p for ring in rings for p in ring];fs=[tuple(range(n-1,-1,-1))]
 for j in range(len(rings)-1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 fs.append(tuple((len(rings)-1)*n+i for i in range(n)));part(name,vs,fs,mat)
def tube(name,points,radii,mat,n=6):
 # Parallel-transport section frame avoids twist discontinuities in helical curves.
 vs=[];rings=[];prev=None
 for i,p in enumerate(points):
  if radii[i]<=0:rings.append([len(vs)]);vs.append(tuple(p));continue
  t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.normalize()
  ref=Vector((0,0,1)) if abs(t.z)<.95 else Vector((1,0,0))
  u=(prev-t*prev.dot(t)).normalized() if prev is not None and (prev-t*prev.dot(t)).length>.1 else t.cross(ref).normalized();w=t.cross(u).normalized();prev=u
  ring=[]
  for j in range(n):ring.append(len(vs));vs.append(tuple(Vector(p)+radii[i]*(u*math.cos(j*math.tau/n)+w*math.sin(j*math.tau/n))))
  rings.append(ring)
 fs=[]
 if len(rings[0])>1:fs.append(tuple(reversed(rings[0])))
 for ra,rb in zip(rings,rings[1:]):
  if len(ra)==1:
   for j in range(n):fs.append((ra[0],rb[j],rb[(j+1)%n]))
  elif len(rb)==1:
   for j in range(n):fs.append((ra[j],rb[0],ra[(j+1)%n]))
  else:
   for j in range(n):fs.append((ra[j],ra[(j+1)%n],rb[(j+1)%n],rb[j]))
 if len(rings[-1])>1:fs.append(tuple(rings[-1]))
 part(name,vs,fs,mat)
def ellipsoid(name,c,r,mat,n=12,k=6):
 # Distinct poles, no collapsed duplicate rings or tiny polar cap slivers.
 vs=[(c[0],c[1],c[2]-r[2])]
 for j in range(1,k):
  t=-math.pi/2+math.pi*j/k
  for i in range(n):vs.append((c[0]+r[0]*math.cos(t)*math.cos(i*math.tau/n),c[1]+r[1]*math.cos(t)*math.sin(i*math.tau/n),c[2]+r[2]*math.sin(t)))
 end=len(vs);vs.append((c[0],c[1],c[2]+r[2]));fs=[]
 for i in range(n):fs.append((0,1+(i+1)%n,1+i))
 for j in range(k-2):
  for i in range(n):aa=1+j*n+i;bb=1+j*n+(i+1)%n;fs.append((aa,bb,bb+n,aa+n))
 for i in range(n):fs.append((1+(k-2)*n+i,1+(k-2)*n+(i+1)%n,end))
 part(name,vs,fs,mat)
def needle(name,start,end,radius,mat='bristle'):
 tube(name,[start,end],[radius,0],mat,4)
def dinomischus():
 n=40
 # Basal bulb, slender rigid tapering stem and chalice as contiguous axial sections.
 prof=[(0,.00025),(.0002,.00075),(.0007,.00105),(.0013,.0009),(.002,.00050),(.003,.00028),(.0158,.00025),(.017,.00045),(.018,.0009),(.019,.0018),(.020,.00265),(.0214,.00315),(.0222,.0033),(.02235,.0031)]
 rings=[[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z+(.0024 if z>=.018 else 0)) for i in range(n)] for z,r in prof];loft('bulb_stem_and_calyx_full_organism',rings,'body')
 # Shallow recessed upper disc, no cavity-through stem.
 rings=[[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z) for i in range(n)] for r,z in [(.0031,.02475),(.0028,.02445),(.0018,.0242),(.0008,.0241)]];loft('shallow_upper_surface',rings,'inner')
 for j in range(gp['bracts']):
  a=j*math.tau/gp['bracts'];u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0));rings=[]
  # Flattened volume with a rounded distal contour, not a petal sphere.
  for t,w in [(0,.00042),(.15,.00047),(.72,.00049),(.91,.00038),(1,.00008)]:
   c=u*(.00320+.0006*t)+Vector((0,0,.0238+gp['bract_length_m']*t));rings.append([tuple(c+v*(w*math.cos(k*math.tau/8))+u*(.00012*math.sin(k*math.tau/8))) for k in range(8)])
  loft('twenty_stiff_flattened_upright_bracts',rings,'bract')
 # Two understated openings on disc are interpretation, not an expressive face.
 for x,y,r in [(-.0007,-.0003,.00018),(.00065,.0002,.00014)]:
  ellipsoid('subtle_interpreted_upper_openings',(x,y,.02424),(r,r,.00005),'opening',12,4)
def star_dune():
 na=gp['angular_steps'];nr=gp['radial_steps'];vs=[(0,0,100)];fs=[];arms=[1,.86,1.04,.8,.94]
 for j in range(1,nr+1):
  t=j/nr
  for i in range(na):
   a=i*math.tau/na;phase=(5*a/math.tau)%1;dist=min(phase,1-phase)*2;ridge=(1-dist)**1.3;arm=int((5*a/math.tau+.5)%5);outer=(.74+.26*ridge)*arms[arm];bend=.14*math.sin(2*a+.5)*t
   x=200*t*outer*math.cos(a+bend);y=160*t*outer*math.sin(a+bend)
   z=100*(1-t)**1.13*(.48+.52*ridge)*(1-.04*math.sin(3*a)*t)
   vs.append((x,y,z))
 for i in range(na):fs.append((0,1+i,1+(i+1)%na))
 for j in range(nr-1):
  for i in range(na):
   a=1+j*na+i;b=1+j*na+(i+1)%na;c=b+na;d=a+na;fs.extend([(a,b,c),(a,c,d)])
 fs.append(tuple(reversed([1+(nr-1)*na+i for i in range(na)])))
 part('five_connected_sand_ridges_and_saddles',vs,fs,'sand')
def slot_canyon():
 ny=gp['longitudinal_steps'];nz=gp['height_steps']
 def inner(y,t,side):
  center=.85*math.sin(y*.28)+.28*math.sin(y*.61)
  half=.92+.18*math.sin(y*.48+1)+.13*math.cos(y*.8+t*5+side)
  # Meandering whole throat plus erosion bulges change with height without crossing.
  return center+side*(half+.23*math.sin(t*math.pi*3+y*.4)+.48*t*t)
 for side,label in [(-1,'west'),(1,'east')]:
  vs=[];fs=[]
  for k in range(nz+1):
   t=k/nz
   for j in range(ny+1):
    y=-14+28*j/ny;x=inner(y,t,side);z=.2+11.8*t*(.96+.04*math.sin(y*.25+side));vs.append((x,y,z))
  for k in range(nz):
   for j in range(ny):
    a=k*(ny+1)+j;b=a+1;c=b+ny+1;d=a+ny+1;fs.extend([(a,b,c),(a,c,d)])
  # Integral exterior shoulders down to flat crop base, close each wall block.
  perimeter=list(range(ny+1))+[k*(ny+1)+ny for k in range(1,nz+1)]+[nz*(ny+1)+j for j in range(ny-1,-1,-1)]+[k*(ny+1) for k in range(nz-1,0,-1)]
  outer=[]
  for idx in perimeter:
   x,y,z=vs[idx];outer.append(len(vs));vs.append((side*7,y,z))
  for i,idx in enumerate(perimeter):fs.append((idx,perimeter[(i+1)%len(perimeter)],outer[(i+1)%len(perimeter)],outer[i]))
  fs.append(tuple(reversed(outer)))
  obj=mesh_object(label+'_solid_fluted_canyon_wall',vs,fs,[m['sandstone'],m['pale'],m['deep']],col)
  # Coherent height bands, not stochastic noise.
  for p in obj.data.polygons:
   z=p.center.z;band=int(z/1.4)%6;p.material_index=1 if band in [1,4] else (2 if band==3 else 0)
 # Thin integral sandy floor substrate with open passage on both ends.
 vs=[(x,y,z) for z in [0,.2] for y in [-14,14] for x in [-7,7]];fs=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)];part('dry_channel_floor_substrate',vs,fs,'floor')
def flowstone():
 nx=gp['cross_steps'];ny=gp['flow_steps'];vs=[];fs=[]
 def profile(t):
  # Three flowing ledge transitions with broad shoulders and rounded risers.
  return .08+sum(h/(1+math.exp(-s*(t-c))) for h,s,c in [(1.0,28,.22),(1.0,30,.50),(1.05,32,.78)])+.34*t
 def point(u,t):
  width=2*(1-.28*t)*(.97+.03*math.cos(5*t));x=u*width;y=-1.5+3*t+.28*u*u*(1-t)
  lobes=(.09*math.cos(u*math.pi*7+.8*t)+.035*math.cos(u*math.pi*15))*max(0,1-u*u)
  z=profile(t)+.12*(1-u*u)+lobes*(.4+.6*math.sin(t*math.pi)**2);return(x,y,z)
 for j in range(ny+1):
  for i in range(nx+1):vs.append(point(-1+2*i/nx,j/ny))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=b+nx+1;d=a+nx+1;fs.extend([(a,b,c),(a,c,d)])
 perimeter=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];bottom=[]
 for idx in perimeter:
  x,y,z=vs[idx];bottom.append(len(vs));vs.append((x,y,0))
 for i,idx in enumerate(perimeter):fs.append((idx,perimeter[(i+1)%len(perimeter)],bottom[(i+1)%len(perimeter)],bottom[i]))
 fs.append(tuple(reversed(bottom)))
 obj=mesh_object('connected_calcite_sheet_over_host_volume',vs,fs,[m['calcite'],m['cream'],m['ochre'],m['host']],col)
 for p in obj.data.polygons:
  if any(v>=((nx+1)*(ny+1)) for v in p.vertices):p.material_index=3
  else:p.material_index=1 if int(p.center.y*5+10)%6==0 else (2 if int(p.center.y*5+10)%6==3 else 0)
 for row,t in enumerate([.32,.60]):
  for j in range(9):
   u=-.88+j*.22;x,y,z=point(u,t);length=.18+.12*(.5+.5*math.sin(j*1.7+row));r=.09+.025*math.cos(j)
   tube('eighteen_rounded_lip_tongues',[(x,y+.04,z+.05),(x,y-.10,z+.01),(x,y-.23,z-length*.60),(x,y-.32,z-length)],[r,r*.95,r*.65,0],'cream',8)
{'dinomischus':dinomischus,'star-dune':star_dune,'slot-canyon':slot_canyon,'flowstone-cascade':flowstone}[slug]()
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset(col,center_xy=True)
ground_asset(col,center_xy=False);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.context.scene['asset_author']='Leon Made This / s010s';bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['reconstruction_scope']=cfg['modeling_decisions'];bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties};assert not set(opts)-available,set(opts)-available
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT','config_sha256':hashlib.sha256(pathlib.Path(a.config).read_bytes()).hexdigest()},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
