# SPDX-License-Identifier: MIT
"""Original batch63 full-volume geometry from frozen concepts and primary-source briefs."""
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
def siphusauctum():
 n=gp['calyx_segments'];rs=[.006,.012,.020,.027,.032,.035,.035,.033,.029,.022,.013,.0032];zs=[.11,.118,.126,.136,.148,.16,.173,.186,.198,.209,.217,.22];vs=[]
 #Paired shell surfaces; the same openings connect external and internal surfaces.
 for inner in [False,True]:
  for j,(z,r) in enumerate(zip(zs,rs)):
   for i in range(n):
    a=i*math.tau/n;rr=(r-(.0012 if inner else 0))*(1+.035*math.cos(6*a));vs.append((rr*math.cos(a),rr*math.sin(a),z))
 outer=[];L=len(rs)*n
 for j in range(len(rs)-1):
  for i in range(n):
   #Six inset ports, each spanning two angular cells and one vertical band.
   if j==2 and i%8 in [3,4]:continue
   outer.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 fs=outer+[tuple(L+i for i in reversed(f)) for f in outer]
 #Every boundary edge gets a connecting wall, including top anus and basal neck.
 counts={}
 for f in outer:
  for a,b in zip(f,f[1:]+f[:1]):
   k=tuple(sorted((a,b)));counts.setdefault(k,[]).append((a,b))
 for e,oriented in counts.items():
  if len(oriented)==1:
   a,b=oriented[0];fs.append((b,a,a+L,b+L))
 #Sheath mesh has face materials by lobed longitudinal sectors, inner muted.
 obj=mesh_object('complete_ovoid_sheath_six_basal_ports_terminal_anus',vs,fs,[m['sheath'],m['lobe'],m['inner']],col)
 for p in obj.data.polygons:
  p.material_index=2 if p.index>=len(outer) else (1 if (p.index%n)//4%2 else 0)
 #Inner neck continues to basal flattened holdfast; sleeve ends above holdfast.
 tube('continuous_inner_stem',[(0,0,.007),(0,0,.045),(.001,0,.082),(0,0,.113)],[.0033,.0032,.0036,.0057],'stem',14)
 tube('outer_stem_sleeve_ending_above_holdfast',[(0,0,.018),(0,0,.050),(.001,0,.082),(0,0,.114)],[.0047,.0043,.0047,.0065],'stem',18)
 ellipsoid('small_flattened_bulbous_holdfast',(0,0,.004),(.011,.009,.004),'stem',18,6)
def esker():
 ny=gp['longitudinal_steps'];nx=gp['cross_steps'];vs=[(0,-350,0)];rows=[]
 for j in range(1,ny):
  t=j/ny;y=-350+700*t;cx=80*math.sin(math.tau*t);dx=80*math.tau/700*math.cos(math.tau*t);norm=math.sqrt(1+dx*dx);width=35*(math.sin(math.pi*t)**.35)*(1+.08*math.sin(11*t));h=35*math.sin(math.pi*t)**.35*(.93+.07*math.sin(t*18));row=[]
  for i in range(nx+1):
   u=-1+2*i/nx;z=h*max(0,1-u*u)**1.8;z*=1+.045*math.sin(13*t+3*u)*abs(u);row.append(len(vs));vs.append((cx+u*width/norm,y-u*width*dx/norm,z))
  rows.append(row)
 end=len(vs);vs.append((0,350,0));fs=[];mi=[]
 for i in range(nx):fs.append((0,rows[0][i+1],rows[0][i]));mi.append(0)
 for j in range(len(rows)-1):
  for i in range(nx):
   a,b,c,d=rows[j][i],rows[j+1][i],rows[j+1][i+1],rows[j][i+1];fs.extend([(a,b,c),(a,c,d)]);mi.extend([1 if abs(i-nx/2)<2 else 2]*2)
 for i in range(nx):fs.append((rows[-1][i],rows[-1][i+1],end));mi.append(0)
 perimeter=[0]+[r[0] for r in rows]+[end]+[r[-1] for r in reversed(rows)];fs.append(tuple(reversed(perimeter)));mi.append(0)
 obj=mesh_object('closed_sinuous_glaciofluvial_sand_gravel_ridge',vs,fs,[m['gravel'],m['crest'],m['flank']],col)
 for p,i in zip(obj.data.polygons,mi):p.material_index=i
def caldera():
 n=gp['radial_segments'];scales=gp['radial_ring_scales'];heights=gp['ring_heights_m'];vs=[(0,0,85)];rings=[]
 for k,(r,z) in enumerate(zip(scales,heights)):
  row=[]
  for i in range(n):
   a=i*math.tau/n;edge=1+.07*math.sin(3*a+.4)+.04*math.cos(7*a)+(.045*math.sin(17*a+.3) if k>=4 else .012*math.sin(9*a));breach=math.exp(-((math.atan2(math.sin(a+math.pi/2),math.cos(a+math.pi/2)))/.26)**2);variation=(math.sin(5*a)+.50*math.sin(11*a+.7))*72*(r**1.3);zz=z+variation if k<len(scales)-1 else 0
   if 3<=k<=6:zz-=breach*225*math.sin((k-2)*math.pi/5)
   #Gullies strongest on scarps, quiet interior floor.
   if k in [4,5,6]:zz-=48*(.5+.5*math.cos(18*a+.4))**4
   row.append(len(vs));vs.append((gp['radius_x_m']*r*edge*math.cos(a),gp['radius_y_m']*r*edge*math.sin(a),zz))
  rings.append(row)
 fs=[];ms=[]
 for i in range(n):fs.append((0,rings[0][i],rings[0][(i+1)%n]));ms.append(3)
 for k in range(len(rings)-1):
  for i in range(n):
   a,b,c,d=rings[k][i],rings[k+1][i],rings[k+1][(i+1)%n],rings[k][(i+1)%n];fs.extend([(a,b,c),(a,c,d)]);ms.extend([3 if k<2 else 2 if k<4 else 1 if k<5 else 0]*2)
 fs.append(tuple(reversed(rings[-1])));ms.append(0);obj=mesh_object('continuous_closed_volcanic_collapse_basin',vs,fs,[m['outer'],m['rim'],m['scarp'],m['floor']],col)
 for p,i in zip(obj.data.polygons,ms):p.material_index=i
def dogtooth():
 n=gp['host_segments'];vs=[];rings=[]
 #Cross-sectional path from back exterior over thick front rim into recessed back.
 profiles=[(.48,.15),(.86,.115),(1,.025),(.94,-.115),(.66,-.135),(.58,-.09),(.43,.015),(.16,.07)]
 for j,(r,y) in enumerate(profiles):
  row=[]
  for i in range(n):
   a=i*math.tau/n;irr=1+.10*math.sin(3*a+.5)+.075*math.sin(7*a)+.035*math.sin(13*a+1.2);row.append(len(vs));vs.append((.225*r*irr*math.cos(a),y+.008*math.sin(5*a)*r,.19+.19*r*irr*math.sin(a)))
  rings.append(row)
 fs=[tuple(reversed(rings[0]))];ms=[0]
 for j in range(len(rings)-1):
  for i in range(n):
   a,b,c,d=rings[j][i],rings[j][(i+1)%n],rings[j+1][(i+1)%n],rings[j+1][i];fs.extend([(a,b,c),(a,c,d)]);ms.extend([2 if j>=4 else 1 if j==3 else 0]*2)
 fs.append(tuple(rings[-1]));ms.append(2);o=mesh_object('thick_closed_back_limestone_vug',vs,fs,[m['limestone'],m['host-light'],m['inner']],col)
 for p,i in zip(o.data.polygons,ms):p.material_index=i
 #Scalenohedron is12 inequilateral triangular faces around a zig-zag equatorial hexagon.
 for tier,count in enumerate(gp['crystal_tiers']):
  for j in range(count):
   a=math.tau*(j+.31*tier)/count+.075*math.sin(j*2.17+1.6*tier);rad=[.63,.51,.34][tier]*(1+.085*math.sin(j*1.89+tier));yy=[-.10,-.025,.05][tier]+.018*math.sin(j*2.8+tier);base=Vector((.225*rad*math.cos(a),yy,.19+.19*rad*math.sin(a)));length=.017+.052*(.5+.5*math.sin(j*2.39+tier))
   if tier==0 and j in [2,7,16]:length=.08
   d=Vector((-math.cos(a),-.18-.12*tier,-math.sin(a))).normalized();u=d.cross(Vector((0,1,0))).normalized();w=d.cross(u).normalized();width=length*(.20+.05*math.sin(j+1));center=base+d*length*.2
   v=[tuple(base-d*length*.28)]
   for k in range(6):
    th=k*math.tau/6+.12*j;zoffset=length*(.11 if k%2 else -.11);v.append(tuple(center+u*width*math.cos(th)+w*width*math.sin(th)+d*zoffset))
   v.append(tuple(base+d*length));f=[]
   for k in range(6):f.extend([(0,1+(k+1)%6,1+k),(7,1+k,1+(k+1)%6)])
   part('mixed_inward_scalenohedral_calcite_crystals',v,f,'calcite-light' if j%4==0 else 'calcite')
{'siphusauctum':siphusauctum,'esker':esker,'caldera':caldera,'dogtooth-spar-cavity':dogtooth}[slug]()
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.context.scene['asset_author']='Leon Made This / s010s';bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['reconstruction_scope']=cfg['modeling_decisions'];bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties};assert not set(opts)-available,set(opts)-available
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT',config_sha256=hashlib.sha256(pathlib.Path(a.config).read_bytes()).hexdigest()),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
