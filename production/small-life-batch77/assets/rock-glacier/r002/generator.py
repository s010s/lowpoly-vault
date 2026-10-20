# SPDX-License-Identifier: MIT
"""Original batch77 geometry authored after complete15:55:52Z immutable premodel freezes."""
import bpy,sys,json,math,argparse,pathlib,random
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed'])
def multi(name,vs,fs,ms):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,ms):p.material_index=keys.index(k)
 return o

def gridclose(name,vs,fs,ms,nx,ny,mat):
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];b=len(vs);vs.extend([(vs[a][0],vs[a][1],0) for a in boundary])
 for i,a in enumerate(boundary):q=(i+1)%len(boundary);fs.append((a,boundary[q],b+q,b+i));ms.append(mat)
 fs.append(tuple(b+i for i in range(len(boundary)-1,-1,-1)));ms.append(mat);return multi(name,vs,fs,ms)


def ernietta():
 n=180;vs=[];fs=[];ms=[]
 # Cross-section traverses lower outer wall upward, rounded broken lip, then inside down.
 rings=[(.10,.002),(.40,.004),(.68,.009),(.86,.016),(.98,.027),(1,.038),(.96,.047),(.94,.051),(.81,.051),(.78,.046),(.73,.038),(.59,.028),(.35,.022),(.10,.020)]
 for j,(r,z) in enumerate(rings):
  for i in range(n):
   t=math.tau*i/n;rib=(.5+.5*math.cos(30*t))**.8
   # Unequal truncation, not living fan apex.
   lip=.0030*math.sin(3*t+.3)+.0018*math.sin(7*t+1.1)+.0010*math.sin(13*t)
   w=max(0,min(1,(z-.025)/.022));rr=r+(.027 if j<8 else .014)*rib*math.sin(math.pi*min(1,z/.055))
   x=.04*rr*math.cos(t)*(1+.018*math.sin(5*t));y=.025*rr*math.sin(t)*(1+.025*math.cos(3*t))
   # Zigzag relief of the basal joining region, integral with rounded bottom.
   seam=.0008*(1-abs(math.sin(t)))*math.cos(30*t) if j<4 else 0
   zz=z+w*lip+seam;vs.append((x,y,zz))
 for j in range(len(rings)-1):
  for i in range(n):
   q=(i+1)%n;a=j*n+i;b=j*n+q;c=a+n;d=b+n
   mat='infill' if j>11 else 'tube' if (i%6 in [0,1,5] and j<8) else 'fossil'
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 for row,z,mat,reverse in [(0,.001,'fossil',True),(len(rings)-1,.020,'infill',False)]:
  c=len(vs);vs.append((0,0,z))
  for i in range(n):
   f=(c,row*n+(i+1)%n,row*n+i) if reverse else (c,row*n+i,row*n+(i+1)%n);fs.append(f);ms.append(mat)
 o=multi('incomplete_elliptical_ernietta_basal_fossil_sack_integral_palisade_ribs_open_cavity',vs,fs,ms)
 o['scope']='Incomplete preserved basal sack fossil form, not complete organism. Missing trunk and paired fans not reconstructed.'
 o['morphology']='30 integral tubular ribs around central cavity, truncated distal boundary, compressed rounded base and integral basal zigzag relief.'

def loess():
 nx=96;cross=[(-3.5,.15),(-2.8,.22),(-2.15,.65),(-1.65,1.35),(-1.42,2.4),(-1.36,3.7),(-1.32,5.0),(-1.30,6.25),(-1.12,7.35),(-.65,7.65),(.15,7.7),(1.1,7.35),(2.1,6.45),(3.5,4.65)];ny=len(cross)-1;vs=[];fs=[];ms=[]
 joints=[(-6.3,.25,.65),(-3.9,.17,.48),(-1.2,.34,.86),(1.9,.22,.74),(4.15,.38,.9),(6.5,.18,.43)]
 for j,(y,z) in enumerate(cross):
  for i in range(nx+1):
   x=-8+16*i/nx;g=sum(a*math.exp(-((x-c)/w)**2) for c,w,a in joints);edge=math.sin(math.pi*i/nx)**.4
   crest=.35*math.sin(.53*x+1)+.22*math.sin(1.3*x-.4)-.45*g
   front=j<9;yy=y+(g*(.8 if 3<j<9 else .3) if front else .1*math.sin(x*.7+j))
   zz=z+crest*max(0,min(1,z/7))*edge
   if j<4:zz+=.12*math.sin(x*1.2+j*.5)*edge
   if j>8:zz-=g*.27*max(0,1-(j-9)/4)
   xx=x+.035*math.sin(j*1.6+i*.7)*edge
   # Final front/rear silhouettes and ends remain irregular, but one continuous body.
   vs.append((xx,yy+.06*math.sin(x*2.3+j*.6)*edge,max(.08,zz)))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1;mat='soil' if j>=8 else 'face' if j>=3 else 'silt'
   for f in [(a,c,d),(a,d,b)]:fs.append(f);ms.append(mat)
 o=gridclose('continuous_fine_silt_loess_bluff_with_unequal_vertical_joints_crest_gullies_apron',vs,fs,ms,nx,ny,'silt');o['scope']='Generic fine windblown silt wall, no named-site survey, not rock columns.'

def rockglacier():
 from mathutils.geometry import delaunay_2d_cdt
 from mathutils import Vector
 points=[];n=100
 for i in range(n):
  t=math.tau*i/n;rad=1+.025*math.sin(5*t+.4)+.018*math.cos(9*t)
  points.append(Vector((rad*math.cos(t),rad*math.sin(t))))
 for i in range(2300):
  t=rng.random()*math.tau;r=math.sqrt(rng.random())*.98;points.append(Vector((r*math.cos(t),r*math.sin(t))))
 edges=[(i,(i+1)%n) for i in range(n)];verts,edges,faces,*_=delaunay_2d_cdt(points,edges,[],0,1e-6)
 vs=[];ms=[]
 def surface(u,v):
  # The wide rounded toe is negativeY; the uphill neck positiveY.
  width=.82-.14*v+.08*math.sin(v*2);x=12*u*width;y=23*v
  shore=max(0,1-u*u-v*v);z=1.0+1.45*shore**.24+.75*(v+1)/2*shore**.2
  # Unequal curved transverse compression ridges, broad and locally interrupted.
  line=y+4.5*u*u
  for c,w,a,phase in [(-13,2.2,2.05,.2),(-4,1.9,2.65,1.4),(6,2.1,1.80,2.1),(14,1.7,1.25,.8)]:
   asym=.75+.25*math.sin(2.3*u+phase);z+=a*math.exp(-((line-c)/w)**2)*asym*shore**.35
  z+=(rng.random()-.45)*.44*shore**.20
  return (x+.23*math.sin(v*3)*shore,y,z)
 for p in verts:vs.append(surface(p.x,p.y))
 fs=[tuple(f) for f in faces]
 for f in fs:
  z=sum(vs[k][2] for k in f)/len(f);ms.append('clast' if rng.random()<.25 else 'shadow' if rng.random()<.18 else 'rock')
 # Determine boundary from triangle incidences, not assumed returned order.
 counts={}
 for f in fs:
  for i,a in enumerate(f):
   b=f[(i+1)%len(f)];e=tuple(sorted((a,b)));counts[e]=counts.get(e,0)+1
 boundary=[e for e,c in counts.items() if c==1];ids=sorted(set(i for e in boundary for i in e));bottom={}
 for i in ids:bottom[i]=len(vs);vs.append((vs[i][0],vs[i][1],0))
 for a,b in boundary:fs.append((a,b,bottom[b],bottom[a]));ms.append('shadow')
 c=len(vs);vs.append((0,0,0))
 for a,b in boundary:fs.append((c,bottom[a],bottom[b]));ms.append('shadow')
 o=multi('lobate_angular_rubble_rock_glacier_unequal_arcuate_transverse_ridges',vs,fs,ms);o['scope']='Generic rock-glacier surface, uncertain internal ice; no exposed ice, named site, speed or age claim.'
 o['surface']='Continuous unstructured random angular rubble facets; unequal broad locally varying curved ridges; no separate intersecting clasts.'

def slump():
 # Perimeter follows irregular full-depth front and rear plus broken ends.
 outline=[]
 for i in range(49):outline.append((-4+8*i/48,-1.3))
 for i in range(1,13):outline.append((4,-1.3+2.6*i/12))
 for i in range(1,49):outline.append((4-8*i/48,1.3))
 for i in range(1,12):outline.append((-4,1.3-2.6*i/12))
 n=len(outline);levels=[0,.22,.46,.72,.98,1.20,1.43,1.69,1.91,2.15,2.41,2.7,3.02,3.38,3.72,4];vs=[];fs=[];ms=[];records=[]
 for band in range(len(levels)-1):
  for sub in [0,.5]:records.append((band,sub,levels[band]+(levels[band+1]-levels[band])*sub))
 records.append((14,1,4))
 for j,(band,sub,h) in enumerate(records):
  # Middle interval is deformed; top/bottom orderly strata remain flat.
  amp=math.sin(math.pi*(h-.72)/(3.02-.72)) if .72<h<3.02 else 0
  for i,(x,y) in enumerate(outline):
   phase=1.15*x+.20*y+.40
   fold=.58*math.sin(phase)+.15*math.sin(2.1*x-.4)
   xx=x+.12*amp*math.sin(phase+.6)+.04*math.sin(i*.91+h)*abs(x/4)**6
   erosion=.022*math.sin(j*1.13)+.015*math.sin(i*1.7+j*.7)
   yy=y+math.copysign(erosion,y)+.035*math.sin(x*2.7+j*.5)
   z=h+amp*fold+.035*math.sin(x*.9+y)*max(0,(h-3.3)/.7)
   vs.append((xx,yy,z))
 for j in range(len(records)-1):
  band=records[j][0];mat='marl' if band%2==0 else 'silt'
  for i in range(n):
   q=(i+1)%n;a=j*n+i;b=j*n+q;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 fs.append(tuple(range(n-1,-1,-1)));ms.append('earth');o=(len(records)-1)*n;fs.append(tuple(o+i for i in range(n)));ms.append('earth')
 ob=multi('bounded_soft_sediment_slump_folded_middle_interval_orderly_upper_lower_beds',vs,fs,ms);ob['scope']='Generic bounded soft-sediment slump; not tectonic folding, gneiss or exact locality.'
 ob['structure']='Continuous full-depth laminated outcrop; middle asymmetric folded interval bounded by flatter strata; no floating ribbons or duplicate faces.'
{'ernietta':ernietta,'loess-bluff':loess,'rock-glacier':rockglacier,'slump-folded-bed':slump}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
