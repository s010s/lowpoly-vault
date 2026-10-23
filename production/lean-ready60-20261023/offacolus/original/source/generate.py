# SPDX-License-Identifier: MIT
"""Original Offacolus kingi geometry. Run in Blender 4.3.2:
blender -b -t 2 --python source/generate.py -- --output-dir OUTPUT
Only source/params.json and the hash-pinned sibling deps are required.
"""
import sys, json, math, hashlib, argparse, random
from pathlib import Path
SRC=Path(__file__).resolve().parent
sys.path.insert(0,str(SRC/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
arg=argparse.ArgumentParser(); arg.add_argument('--output-dir',type=Path,default=SRC.parent)
a=arg.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=a.output_dir.resolve(); OUT.mkdir(parents=True,exist_ok=True)
P=json.loads((SRC/'params.json').read_text()); random.seed(P['seed'])
C=setup_scene('offacolus',P['seed'])
root=bpy.data.objects[C['asset_root']]
root['taxon']='Offacolus kingi'; root['reconstruction']='Original, fossil-guided whole living animal; colors and stance inferred'
root['main_reference']='Siveter 2003 Fig.4, accession unspecified, about 7 mm; C.29557 used for anatomy only'
# Coordinates below are millimetres for readability, converted to metres once.
palette=P['palette']; mats={k:make_material(k,v,roughness=.82) for k,v in palette.items()}
B={k:{'v':[],'f':[],'parts':[]} for k in mats}

def add(name,mat,v,f):
 b=B[mat]; off=len(b['v']); face0=len(b['f']); b['v'].extend([list(q) for q in v]); b['f'].extend([tuple(off+i for i in face) for face in f]); b['parts'].append({'name':name,'vertex_start':off,'vertex_count':len(v),'face_start':face0,'face_count':len(f)})

def tube(name,mat,path,radii,n=8):
 pts=[Vector(v) for v in path]; verts=[]; faces=[]
 for i,(p,r) in enumerate(zip(pts,radii)):
  t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized(); ref=Vector((0,0,1)) if abs(t.z)<.92 else Vector((1,0,0)); u=t.cross(ref).normalized(); v=t.cross(u).normalized()
  verts.extend([p+r*(math.cos(2*math.pi*j/n)*u+math.sin(2*math.pi*j/n)*v) for j in range(n)])
 for i in range(len(pts)-1):
  for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 faces.append(tuple(reversed(range(n)))); faces.append(tuple((len(pts)-1)*n+j for j in range(n)))
 add(name,mat,verts,faces)

def cone(name,mat,start,end,r,n=5):
 s=Vector(start); t=Vector(end)-s; z=t.normalized(); ref=Vector((0,0,1)) if abs(z.z)<.9 else Vector((0,1,0)); u=z.cross(ref).normalized(); v=z.cross(u).normalized()
 verts=[s+r*(math.cos(2*math.pi*j/n)*u+math.sin(2*math.pi*j/n)*v) for j in range(n)]+[Vector(end)]
 faces=[tuple(reversed(range(n)))]+[(j,(j+1)%n,n) for j in range(n)]
 add(name,mat,verts,faces)

def ellipsoid(name,mat,c,r,n=10,rings=5):
 v=[(c[0],c[1],c[2]-r[2])]; f=[]
 for k in range(1,rings):
  ph=-math.pi/2+math.pi*k/rings
  for j in range(n):
   th=2*math.pi*j/n; v.append((c[0]+r[0]*math.cos(ph)*math.cos(th),c[1]+r[1]*math.cos(ph)*math.sin(th),c[2]+r[2]*math.sin(ph)))
 top=len(v);v.append((c[0],c[1],c[2]+r[2]))
 for j in range(n): f.append((0,1+(j+1)%n,1+j))
 for k in range(rings-2):
  for j in range(n): f.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
 for j in range(n):f.append((top,1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n))
 add(name,mat,v,f)

# High box-vaulted carapace, a closed thick shell with truly open front and belly.
# Non-ellipsoidal profile preserves vertical flanks and broad, slightly flattened roof.
profile=[(-1.00,.66),(-1.21,.87),(-1.25,1.38),(-1.20,1.99),(-.96,2.43),(-.50,2.64),(0,2.69),(.50,2.64),(.96,2.43),(1.20,1.99),(1.25,1.38),(1.21,.87),(1.00,.66)]
sections=[(-1.40,.88,-.02),(-1.25,.99,0),(-.75,1,0),(-.10,1,.03),(.55,.94,-.02),(.98,.81,-.15),(1.10,.72,-.28)]
v=[];f=[];N=len(profile);K=len(sections)
for inside in (False,True):
 for y,w,dz in sections:
  for x,z in profile: v.append((x*w-(.07 if x>0 else -.07) if inside else x*w,y,z+dz-(.075 if inside else 0)))
for surf in (0,1):
 off=surf*K*N
 for k in range(K-1):
  for j in range(N-1):
   face=(off+k*N+j,off+k*N+j+1,off+(k+1)*N+j+1,off+(k+1)*N+j); f.append(face if surf==0 else face[::-1])
for k in (0,K-1):
 for j in range(N-1):f.append((k*N+j,k*N+j+1,K*N+k*N+j+1,K*N+k*N+j))
for j in (0,N-1):
 for k in range(K-1):f.append((k*N+j,(k+1)*N+j,K*N+(k+1)*N+j,K*N+k*N+j))
add('vaulted_cephalic_shield_open_anterior','carapace',v,f)
# A narrow reinforced rim, not a second colorful shield.
front=[(x*.88,-1.409,z-.02) for x,z in profile]
tube('anterior_shield_margin','rim',front,[.042]*len(front),6)
# Low ventral body-wall plate anchors distinct appendage insertions.
ellipsoid('cephalic_ventral_body_wall','ventral',(0,-.20,.93),(.76,1.16,.24),14,6)
# Reconstructed soft internal volume blocks an anatomically impossible hollow tunnel.
ellipsoid('cephalic_soft_volume_inside_shield','limbs',(0,-.03,1.64),(.99,1.12,.79),16,8)
ellipsoid('rear_ventral_body_core','limbs',(0,1.60,1.12),(.65,.83,.31),12,6)
# Four free tergites; narrow organic arched plates with true interplate gaps.
def tergite(name,y,length,width,top,bottom):
 prof=[(-width,bottom),(-width*.92,top-.27),(-width*.5,top-.035),(0,top),(width*.5,top-.035),(width*.92,top-.27),(width,bottom)]
 vv=[];ff=[]; nn=len(prof)
 for yy,delta in [(y,0),(y+length,-.06)]:
  for x,z in prof:vv.append((x,yy,z+delta))
 for yy,delta in [(y,-.08),(y+length,-.14)]:
  for x,z in prof:vv.append((x*.96,yy,z+delta))
 for j in range(nn-1):ff.extend([(j,j+1,nn+j+1,nn+j),(2*nn+j,3*nn+j,3*nn+j+1,2*nn+j+1),(j,2*nn+j,2*nn+j+1,j+1),(nn+j,nn+j+1,3*nn+j+1,3*nn+j)])
 ff.extend([(0,nn,3*nn,2*nn),(nn-1,2*nn-1,4*nn-1,3*nn-1)])
 add(name,'carapace',vv,ff)
for i in range(4):tergite('free_tergite_%d'%(i+1),.99+i*.25,.229,.93-i*.10,2.25-i*.16,.94-i*.035)
# One compact posterior unit with three constituent segments and shallow seam traces.
# One solid loft, not three free tergites. Separate telson boss is not counted.
vp=[];fp=[];rr=10
rows=[(1.98,.54,1.48,.72),(2.17,.49,1.35,.70),(2.37,.39,1.23,.70),(2.57,.27,1.08,.72)]
for y,w,zt,zb in rows:
 for j in range(rr):
  th=2*math.pi*j/rr;vp.append((w*math.cos(th),y,(zt+zb)/2+(zt-zb)/2*math.sin(th)))
for i in range(len(rows)-1):
 for j in range(rr):fp.append((i*rr+j,i*rr+(j+1)%rr,(i+1)*rr+(j+1)%rr,(i+1)*rr+j))
fp.extend([tuple(reversed(range(rr))),tuple((len(rows)-1)*rr+j for j in range(rr))]);add('three_segment_fused_posterior_unit','carapace',vp,fp)
for i,(y,w,z) in enumerate([(2.18,.475,1.315),(2.38,.37,1.195)]):
 path=[(-w,y,z-.18),(-w*.70,y,z-.035),(0,y,z),(.70*w,y,z-.035),(w,y,z-.18)]
 tube('fused_posterior_shallow_suture_%d'%(i+1),'rim',path,[.025]*5,5)
ellipsoid('telson_articulation_boss_not_trunk_segment','limbs',(0,2.61,.87),(.22,.20,.18),10,5)
tube('narrow_articulated_telson','carapace',[(0,2.66,.88),(0,3.25,.91),(.02,3.95,.84),(.02,4.63,.56)],[.14,.105,.060,.029],7)
cone('telson_fine_tip','carapace',(.02,4.63,.56),(.015,4.86,.40),.03,6)

# Seven paired cephalic appendages. II-V outer and inner stems originate separately.
insertions=[]
for s,side in [(-1,'left'),(1,'right')]:
 def mir(q):return(s*q[0],q[1],q[2])
 # Pair I, a delicate central cheliceral pair with conservative small terminal fingers.
 tube(side+'_I_chelicera','limbs',[mir(q) for q in [(.18,-1.0,.87),(.23,-1.48,.83),(.25,-1.88,.91),(.25,-2.10,.97)]],[.065,.060,.046,.032],7)
 cone(side+'_I_terminal_fixed_finger','rim',mir((.25,-2.08,.97)),mir((.22,-2.25,1.00)),.032,6)
 cone(side+'_I_terminal_movable_finger','rim',mir((.285,-2.05,.97)),mir((.30,-2.20,1.015)),.027,6)
 for k in range(4):
  pair=k+2; y=-.98+.43*k
  # Outer insertion on lateral body wall, never a fork off the walking shaft.
  start=(.69+.015*k,y,1.06)
  tip=(.35+.33*k,-2.48+.13*k,2.28-.25*k)
  path=[start,(1.02+.08*k,y-.20,1.28),(1.12+.12*k,-1.37+.05*k,1.51),(tip[0]+.12,tip[1]+.25,tip[2]-.20),tip]
  tube(side+f'_{pair}_independent_brush_exopod','limbs',[mir(q) for q in path],[.110,.125,.113,.086,.065],8)
  # Pale low-profile joint cuffs reinforce segmented silhouette, not bulbous beads.
  for j in (1,2,3):
   q=Vector(path[j]);d=(Vector(path[j+1])-Vector(path[j-1])).normalized();tube(side+f'_{pair}_exopod_joint_{j}','rim',[mir(q-d*.035),mir(q+d*.035)],[.127 if j<3 else .090]*2,8)
  # Compact distal brush: twelve short tapering setae in a radial, forward/upward fan.
  for j in range(12):
   angle=2*math.pi*j/12;length=.32+.16*(.5+.5*math.cos(angle))
   base=Vector(tip)+Vector((.05*math.cos(angle),.025,.05*math.sin(angle)))
   direction=Vector((.52*math.cos(angle),-.80,.38+.50*math.sin(angle))).normalized()
   cone(side+f'_{pair}_brush_seta_{j+1:02d}','setae',mir(base),mir(base+length*direction),.023,5)
  # Separate inner limb origin, with a visible gap between proximal stems.
  inner=(.31+.065*k,y+.085,.87)
  walk=[inner,(.74+.07*k,y-.055,.69),(1.20+.08*k,y-.18,.42),(1.41+.07*k,y-.40,.16),(1.48+.06*k,y-.61,.10)]
  tube(side+f'_{pair}_independent_endopod','limbs',[mir(q) for q in walk],[.115,.105,.084,.055,.030],8)
  cone(side+f'_{pair}_small_terminal','rim',mir(walk[-1]),mir((walk[-1][0]+.10,walk[-1][1]-.13,.07)),.035,6)
  insertions.append({'side':side,'pair':pair,'exopod_body_wall_mm':mir(start),'endopod_body_wall_mm':mir(inner),'branches_share_proximal_shaft':False})
 # VI: one walking appendage with only a tiny outer tendril.
 path=[(.60,.69,.87),(1.05,.75,.60),(1.42,.61,.28),(1.56,.31,.08)]
 tube(side+'_VI_locomotory_endopod','limbs',[mir(q) for q in path],[.125,.105,.070,.032],8)
 cone(side+'_VI_terminal','rim',mir(path[-1]),mir((1.63,.19,.055)),.033,6)
 tube(side+'_VI_small_outer_tendril','limbs',[mir(q) for q in [(.78,.66,1.03),(1.08,.64,1.08),(1.24,.42,1.15)]],[.047,.036,.025],6)
 # VII: short broad flap, not another large brush.
 ellipsoid(side+'_VII_short_flap','ventral',mir((.55,.99,.69)),(.26,.24,.08),8,4)
 # Six paired opercular groups, first three bear readable reduced lamellar edges.
 for i in range(6):
  y=1.03+.23*i; w=.47-.052*i; length=.27 if i<3 else .18; z=.72-.012*i
  ellipsoid(side+f'_operculum_{i+1}_'+('lamellate' if i<3 else 'reduced'),'ventral',mir((w*.66,y,z)),(w*.64,length*.60,.065),10,4)
  if i<3:
   for j in range(5):
    x=w*.23+j*w*.18
    tube(side+f'_operculum_{i+1}_lamellar_edge_{j+1}','rim',[mir((x,y-.07,z-.044)),mir((x+.02,y+.10,z-.066))],[.026,.025],5)

# Actual pose length is normalized ONCE to the approximate fossil total 7 mm.
# This preserves the whole-body reference scale, not independent part normalization.
allv=[p for b in B.values() for p in b['v']]; miny=min(q[1] for q in allv);maxy=max(q[1] for q in allv);minz=min(q[2] for q in allv)
scale=P['overall_length_approx']/(maxy-miny)
part_records=[]
for mat,b in B.items():
 if not b['v']:continue
 verts=[(q[0]*scale,q[1]*scale,(q[2]-minz)*scale) for q in b['v']]
 obj=mesh_object(mat,verts,b['f'],mats[mat],C)
 for part in b['parts']:
  vg=obj.vertex_groups.new(name=part['name']);vg.add(list(range(part['vertex_start'],part['vertex_start']+part['vertex_count'])),1,'REPLACE')
 obj['semantic_parts']=json.dumps(b['parts'],separators=(',',':'))
 obj['shading']='Deliberate flat low-poly normals; closed manifold component solids'
 part_records.extend([dict(q,object=mat) for q in b['parts']])
bpy.context.view_layer.update()
root['origin']='Floor contact center of the leg footprint; head -Y, dorsal +Z'
root['scale_m_per_design_mm']=scale
# Source audit retains canonical result. Any micro-scale threshold warnings are not hidden.
source=audit_source(C,P['budgets']['max_triangles'])
# Exact topology and area audit independent from the legacy fixed epsilon.
areas=[]; boundary=0;nonmanifold=0; volumes=[]
for obj in C.all_objects:
 if obj.type!='MESH':continue
 me=obj.data;me.calc_loop_triangles();areas.extend(t.area for t in me.loop_triangles)
 bm=bmesh.new();bm.from_mesh(me);boundary+=sum(e.is_boundary for e in bm.edges);nonmanifold+=sum(not e.is_manifold for e in bm.edges);volumes.append({'object':obj.name,'signed_volume_m3':bm.calc_volume(signed=True)});bm.free()
minarea=min(areas)
source['micro_scale_check']={'minimum_triangle_area_m2':minarea,'zero_area_limit_m2':1e-20,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'signed_volumes':volumes,'true_zero_or_nearzero_triangles':sum(v<=1e-20 for v in areas)}
assert minarea>1e-20 and boundary==0 and nonmanifold==0
if source['errors']:raise RuntimeError('Source audit failed: '+repr(source['errors']))
bpy.context.scene['generator']='source/generate.py'; bpy.context.scene['build_blender_version']=bpy.app.version_string
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in C.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(opts)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}; assert not missing,missing
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
save(OUT/'qa/evidence/source-and-glb.json',{'source':source,'glb':glb})
assert not glb['errors'],glb['errors'];assert glb['bytes']<=P['budgets']['max_glb_bytes'];assert glb['scene_triangles']==source['triangles']
sb=source['bounds_blender_m'];expected={'min':[sb['min'][0],sb['min'][2],-sb['max'][1]],'max':[sb['max'][0],sb['max'][2],-sb['min'][1]]}
delta=max(abs(glb['bounds_m'][side][i]-expected[side][i]) for side in ('min','max') for i in range(3));assert delta<1e-8
save(OUT/'qa/evidence/anatomy-map.json',{'glb_sha256':sha(OUT/'model.glb'),'cephalic_appendage_pairs':7,'brush_pairs':[2,3,4,5],'independent_body_wall_insertions_design_mm':insertions,'free_anterior_tergites':4,'fused_posterior_segments':3,'telson_boss_counted_as_trunk':False,'opercular_pairs':6,'lamellate_opercular_pairs':[1,2,3],'reduced_opercular_pairs':[4,5,6],'semantic_parts':part_records,'design_mm_to_m':scale,'total_length_m':glb['bounds_m']['size'][2],'source_export_bounds_max_delta_m':delta,'caveat':'Geometry and object-name evidence does not independently prove paleontological accuracy.'})
save(OUT/'qa/evidence/build.json',{'asset_id':'offacolus','revision':'r001','seed':P['seed'],'generator_sha256':sha(__file__),'params_sha256':sha(SRC/'params.json'),'blender_version':bpy.app.version_string,'gltf_exporter_version':'4.3.47','threejs_target_version':'0.180.0','export_options':{k:v for k,v in opts.items() if k!='filepath'},'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'source_triangle_count':source['triangles'],'source_export_bounds_max_delta_m':delta,'dependencies':[{'name':q.name,'sha256':sha(q)} for q in sorted((SRC/'deps').glob('*.py'))],'units':'meters','palette_srgb':palette,'original_geometry':True,'third_party_geometry_or_texture':False})
print('OFFACOLUS_BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
