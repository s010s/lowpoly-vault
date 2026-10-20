# SPDX-License-Identifier: MIT
"""Original batch61 full-volume geometry from frozen concepts and primary-source briefs."""
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
def pseudopulex():
 # Anatomical forward-Y convention; all six coxae attach to small thorax.
 n=20;ys=[-.0035,-.0028,-.0014,.0002,.0018,.0034,.005,.0065,.0078,.0092];ws=[.00155,.0020,.00240,.0026,.00262,.00252,.00228,.00185,.00115,.00016];hs=[.00072,.00098,.00114,.00122,.00124,.00117,.00108,.00085,.00053,.00015];rings=[]
 for y,w,h in zip(ys,ws,hs):rings.append([(w*math.cos(i*math.tau/n),y,.0032+h*math.sin(i*math.tau/n)) for i in range(n)])
 loft('broad_not_laterally_compressed_tapering_abdomen',rings,'abdomen')
 # Shallow integrated-looking transverse collars express eight inferred segments.
 for j in range(1,8):
  y=-.0032+j*.00148;idx=min(range(len(ys)),key=lambda k:abs(ys[k]-y));w=ws[idx]*1.007;h=hs[idx]*1.012
  loft('eight_suggested_abdominal_tergal_bands',[[(w*math.cos(i*math.tau/n),yy,.0032+h*math.sin(i*math.tau/n)) for i in range(n)] for yy in [y-.00012,y+.00010]],'ochre')
 ellipsoid('compact_wingless_thorax',(0,-.00465,.0032),(.00125,.0012,.00085),'chitin',16,6)
 # Trapezoid head outline broad posterior, narrower anterior, not flea profile.
 outline=[(-.00068,-.0078),(.00068,-.0078),(.00098,-.0062),(.0008,-.0059),(-.0008,-.0059),(-.00098,-.0062)]
 vs=[(x,y,z) for z in [.00265,.00365] for x,y in outline];fs=[(5,4,3,2,1,0),(6,7,8,9,10,11)]+[(i,(i+1)%6,(i+1)%6+6,i+6) for i in range(6)];part('small_trapezoid_head',vs,fs,'chitin')
 for s in [-1,1]:
  ellipsoid('paired_reduced_lateral_eyes',(s*.00084,-.00685,.00345),(.00018,.00025,.00020),'dark',10,5)
  #16 compact bead sections, antenna only about1.7mm long.
  pts=[]
  for j in range(gp['antennal_beads']):
   t=j/15;p=(s*(.00074+.0010*t),-.00715-.0014*t,.0034+.00036*math.sin(math.pi*t));pts.append(p)
   ellipsoid('sixteen_compact_flagellar_beads',p,(.00011*(1-.25*t),.00010*(1-.2*t),.00010*(1-.2*t)),'ochre',6,4)
  #paired serrated stylets; long enough to exceed twice the head length.
  start=Vector((s*.00015,-.0076,.00285));tip=Vector((s*.00010,-.01115,.00130));tube('paired_elongate_serrated_laciniae',[tuple(start),tuple(start*.50+tip*.50),tuple(tip)],[.00017,.00013,0],'ochre',7)
  for j in range(12):
   t=.08+.072*j;p=start*(1-t)+tip*t;needle('deep_notches_and_stylet_teeth',tuple(p+Vector((s*.00009,0,0))),tuple(p+Vector((s*.00033,.00012,-.000015))),.000045,'chitin')
  #Two short palp systems, echoes preserved visible segments, not total-count proof.
  for q,count in [(0,3),(1,4)]:
   for j in range(count):
    p=(s*(.00045+.00016*j+.00023*q),-.00715-.00028*j,.0028-.00016*j);ellipsoid('short_artistic_maxillary_and_labial_palps',p,(.00013,.00018,.00012),'chitin',6,4)
  for j,(rooty,kneey,footy) in enumerate([(-.00545,-.0062,-.0090),(-.0046,-.0027,-.0027),(-.0037,.0000,.0038)]):
   c=Vector((s*.00085,rooty,.00285));hip=Vector((s*.0020,rooty-.00025,.00295));knee=Vector((s*(.0053+.0004*j),kneey,.0022));ankle=Vector((s*(.0068+.0002*j),footy,.00055))
   tube('six_coxae_and_long_legs',[tuple(c),tuple(hip),tuple(knee),tuple(ankle)],[.00028,.00024,.00020,.000115],'chitin',7)
   #Tibial comb along outer distal section, posterior-leaning stout spurs.
   for k in range(5):
    t=.40+.115*k;p=knee*(1-t)+ankle*t;needle('six_tibial_pseudocombs',tuple(p),tuple(p+Vector((s*.00045,.00020,-.00004))),.000055)
   foot=ankle+Vector((s*.00045,.00040,-.00032))
   for k in range(gp['tarsal_subdivisions']):
    t0=k/5;t1=(k+1)/5;p0=ankle*(1-t0)+foot*t0;p1=ankle*(1-t1)+foot*t1;tube('five_subdivided_tarsi_per_leg',[tuple(p0),tuple(p1)],[.00013-.000008*k,.000115-.000008*k],'ochre',6)
   for q in [-1,1]:
    p=foot+Vector((q*.00011,0,0));tube('paired_scythe_like_claws_on_six_feet',[tuple(p),tuple(p+Vector((q*.00013,.00020,-.00008))),tuple(p+Vector((q*.00011,.00032,-.00002))),tuple(p+Vector((q*.00004,.00034,.00008)))],[.00007,.00006,.00004,0],'dark',5)
 #Original simplified posteriorly-directed setae; radial origins follow actual body envelope.
 for j in range(1,9):
  for k in range(8):
   an=k*math.tau/8+.12*math.sin(j);w=ws[j];h=hs[j];p=Vector((w*math.cos(an),ys[j],.0032+h*math.sin(an)));d=Vector((.00026*math.cos(an),.00065+.00010*math.sin(j),.00023*math.sin(an)));needle('posterior_directed_abdominal_setae',tuple(p),tuple(p+d),.00004)
def daemonelix():
 points=[];radii=[];turns=gp['helix_turns'];radius=gp['helix_center_radius_m'];pitch=gp['helix_pitch_m'];tr=gp['helix_tube_radius_m'];N=144
 #Bottom to top, helix has continuous tangent into bottom lateral tunnel.
 for j in range(N+1):
  t=j/N;th=-math.pi/2+turns*math.tau*t;r=radius*(1+.035*math.sin(th*1.4));z=.25+pitch*turns*t;points.append((r*math.cos(th),r*math.sin(th),z));radii.append(tr*(1+.04*math.sin(th*2.1)))
 p=Vector(points[-1]);tangent=(p-Vector(points[-2])).normalized()
 for k in range(1,7):
  t=k/6;points.append(tuple(p+tangent*.10*t+Vector((0,0,.20*t*t))));radii.append(tr*(1-.12*t))
 tube('solid_continuous_four_and_half_turn_burrow_cast',points,radii,'cast',12)
 #Start tangent at -pi/2 points +X. Chamber extension projects away from coils.
 lower=[(-1.02,-.33,.25),(-.91,-.33,.24),(-.73,-.33,.23),(-.55,-.33,.23),(-.35,-.33,.23),(-.16,-.33,.24),(0,-.33,.25)]
 tube('continuous_lower_tunnel_and_expanded_terminal_chamber',lower,[0,.14,.17,.155,.10,.10,.10],'cast-light',14)
 #Low irregular footing, not a tall slab obscuring the trace geometry.
 rings=[]
 for z,rx,ry in [(0,.86,.50),(.04,.91,.53),(.10,.85,.49)]:
  rings.append([(-.23+rx*(1+.08*math.sin(i*1.9))*math.cos(i*math.tau/20),-.08+ry*(1+.07*math.cos(i*2.1))*math.sin(i*math.tau/20),z+.01*math.sin(i*1.2) if z else 0) for i in range(20)])
 loft('irregular_low_sediment_footing',rings,'sediment')
def mesa():
 n=gp['mesa_perimeter_steps'];levels=gp['mesa_levels_m'];scale=[1,.97,.89,.85,.83,.79,.76,.755];rings=[]
 #Angular erosion bays are consistent through rock faces, quiet resistant top.
 for k,(z,sc) in enumerate(zip(levels,scale)):
  ring=[]
  for j in range(n):
   th=j*math.tau/n;base=1+.048*math.sin(th*3+.4)+.033*math.sin(th*7+.2)+.021*math.cos(th*11);bay=.035*math.cos(th*17+.3)*(1 if k>1 else .4);r=base+bay
   ring.append((300*sc*r*math.cos(th),225*sc*r*math.sin(th),z if k in [0,7] else z+2.0*math.sin(th*5+.8)))
  rings.append(ring)
 #One contiguous body; material bands by shell levels, no floating layer stacks.
 vs=[p for row in rings for p in row];fs=[tuple(range(n-1,-1,-1))];mats=['talus']
 for k in range(len(rings)-1):
  mat=['talus','talus','sandstone','pale','sandstone','upper','cap'][k]
  for j in range(n):
   aa=k*n+j;bb=k*n+(j+1)%n;fs.append((aa,bb,bb+n,aa+n));mats.append(mat)
 #Flat triangulated summit radial patches, subtle color not rough geometry.
 center=len(vs);vs.append((-15,8,180))
 for j in range(n):fs.append(((len(rings)-1)*n+j,(len(rings)-1)*n+(j+1)%n,center));mats.append('cap')
 #Split semantic material regions but share identical ring coordinates to avoid seams.
 matnames=list(dict.fromkeys(mats));obj=mesh_object('continuous_flat_capped_mesa_with_coherent_layers',vs,fs,[m[mat] for mat in matnames],col)
 for poly,mat in zip(obj.data.polygons,mats):poly.material_index=matnames.index(mat)
 #Sparse integral-looking buttresses at lower scarps, deliberately nonuniform.
 for j in [2,7,15,21,29,36,43,51,58]:
  th=j*math.tau/n;rad=.81;xx=300*rad*math.cos(th);yy=225*rad*math.sin(th);c=(xx,yy)
  outdir=Vector((math.cos(th),math.sin(th),0));side=Vector((-math.sin(th),math.cos(th),0));base=Vector((xx,yy,20));v=[tuple(base+outdir*55+side*18),tuple(base+outdir*55-side*18),tuple(base+outdir*10-side*12+Vector((0,0,67))),tuple(base+outdir*6+side*12+Vector((0,0,67))),tuple(base-outdir*15-side*15),tuple(base-outdir*15+side*15)]
  part('asymmetric_lower_talus_buttresses',v,[(0,1,2,3),(0,5,4,1),(1,4,2),(4,5,3,2),(5,0,3)],'talus')
def drumlin():
 #Longitudinal sections with distinct start/end points, continuous rounded transverse arch.
 ny=gp['drumlin_longitudinal_steps'];nx=gp['drumlin_cross_steps'];vs=[(0,-225,0)];rows=[]
 for j in range(1,ny):
  t=j/ny;y=-225+450*t
  #Blunt nose swells fast, high point anterior, elongated gently decaying tail.
  width=75*(math.sin(math.pi*t)**.58)*(1.18-.60*t);h=35*((t/.24)**.72 if t<.24 else ((1-t)/.76)**1.55);row=[]
  for i in range(nx+1):
   u=-1+2*i/nx;x=width*u;z=h*(max(0,1-u*u)**.78)*(1+.018*math.sin(6*t+1.3*u));row.append(len(vs));vs.append((x,y,z))
  rows.append(row)
 end=len(vs);vs.append((0,225,0));fs=[]
 for i in range(nx):fs.append((0,rows[0][i+1],rows[0][i]))
 for j in range(len(rows)-1):
  for i in range(nx):
   a,b=rows[j][i],rows[j+1][i];c,d=rows[j+1][i+1],rows[j][i+1]
   #Broad quiet facets, deliberate alternating diagonal to avoid a needle crest.
   fs.extend([(a,b,d),(b,c,d)] if (i+j)%2 else [(a,b,c),(a,c,d)])
 for i in range(nx):fs.append((rows[-1][i],rows[-1][i+1],end))
 perimeter=[0]+[row[0] for row in rows]+[end]+[row[-1] for row in reversed(rows)];fs.append(tuple(reversed(perimeter)))
 #Single full closed mound with sparse restrained material variation.
 part('rounded_low_asymmetric_till_mound',vs,fs,'till')
{'pseudopulex':pseudopulex,'daemonelix-helical-burrow':daemonelix,'mesa':mesa,'drumlin':drumlin}[slug]()
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
#Footprint center is the authored origin. Pseudopulex approximate six-foot contact center.
if slug=='pseudopulex':
 for obj in col.all_objects:
  if obj.type=='MESH':
   for ve in obj.data.vertices:ve.co.y+=.00245
else:
 #Center geological footprint in XY, without independently normalizing its scale.
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
