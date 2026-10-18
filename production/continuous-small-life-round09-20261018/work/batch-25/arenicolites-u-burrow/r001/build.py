# SPDX-License-Identifier: MIT
"""Original organ-scoped and natural-process teaching forms. Blender -b -t 2 --python build.py -- --config config.json --output /absolute/r001 [--preview]."""
import bpy,sys,math,json,random,hashlib,argparse
from pathlib import Path
from mathutils import Vector
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset,render_previews
pi=math.pi
class Mesh:
 def __init__(self,name,mats):self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  off=len(self.v);self.v+=v;self.f += [tuple(off+i for i in q) for q in f];self.mi += mi if isinstance(mi,list) else [mi]*len(f)
 def finish(self,c,smooth=True):
  o=mesh_object(self.name,self.v,self.f,self.mats,c)
  for p,m in zip(o.data.polygons,self.mi):p.material_index=m;p.use_smooth=smooth
  return o
 def tube(self,pts,rads,mat=0,n=12,hollow=False):
  ps=[Vector(p) for p in pts];vs=[];fs=[];mis=[]
  for j,p in enumerate(ps):
   d=(ps[min(j+1,len(ps)-1)]-ps[max(j-1,0)]).normalized();u=d.cross(Vector((0,1,0)))
   if u.length<.01:u=d.cross(Vector((1,0,0)))
   u.normalize();w=d.cross(u).normalized()
   for k in range(n):a=2*pi*k/n;vs.append(tuple(p+rads[j]*(u*math.cos(a)+w*math.sin(a))))
  fs.append(tuple(reversed(range(n))));mis.append(mat)
  for j in range(len(ps)-1):
   for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mis.append(mat)
  base=(len(ps)-1)*n
  if hollow:
   # A closed wall/rim/interior bowl, with the visible opening modeled in geometry.
   for depth,ratio in [(0,.70),(.38,.64),(2.1,.42)]:
    p=ps[-1]-d*rads[-1]*depth
    for k in range(n):a=2*pi*k/n;vs.append(tuple(p+rads[-1]*ratio*(u*math.cos(a)+w*math.sin(a))))
   for j in range(3):
    for k in range(n):fs.append((base+j*n+k,base+j*n+(k+1)%n,base+(j+1)*n+(k+1)%n,base+(j+1)*n+k));mis.append(mat if j==0 else min(mat+1,len(self.mats)-1))
   fs.append(tuple(base+3*n+k for k in range(n)));mis.append(min(mat+1,len(self.mats)-1))
  else:fs.append(tuple(base+k for k in range(n)));mis.append(mat)
  self.add(vs,fs,mis)
 def ellipsoid(self,p,s,mat=0,n=16,r=9):
  vs=[(p[0],p[1],p[2]+s[2])];fs=[]
  for j in range(1,r):
   a=pi*j/r
   for k in range(n):b=2*pi*k/n;vs.append((p[0]+s[0]*math.sin(a)*math.cos(b),p[1]+s[1]*math.sin(a)*math.sin(b),p[2]+s[2]*math.cos(a)))
  bot=len(vs);vs.append((p[0],p[1],p[2]-s[2]))
  for k in range(n):fs.append((0,1+k,1+(k+1)%n))
  for j in range(r-2):
   for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;fs.append((a,b,b+n,a+n))
  for k in range(n):fs.append((bot,1+(r-2)*n+(k+1)%n,1+(r-2)*n+k))
  self.add(vs,fs,mat)

def smooth_path(points,n=28):
 # Catmull-Rom interpolation preserves named bends and a continuous taper.
 p=[Vector(q) for q in points];out=[]
 for i in range(n):
  t=i/(n-1)*(len(p)-1);k=min(int(t),len(p)-2);t-=k;a=p[max(0,k-1)];b=p[k];c=p[k+1];d=p[min(len(p)-1,k+2)]
  out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
 return out

def flat_strap(mesh,pts,widths,thickness,lateral,mat=0,n=6):
 ps=[Vector(p) for p in pts];verts=[];faces=[];lat=Vector(lateral)
 for j,p in enumerate(ps):
  d=(ps[min(j+1,len(ps)-1)]-ps[max(j-1,0)]).normalized();v=lat-d*lat.dot(d)
  if v.length<.01:v=d.cross(Vector((0,0,1)))
  v.normalize();normal=d.cross(v).normalized()
  for k in range(n):a=2*pi*k/n;verts.append(tuple(p+v*(widths[j]*math.cos(a))+normal*(thickness*math.sin(a))))
 faces.append(tuple(reversed(range(n))))
 for j in range(len(ps)-1):
  for k in range(n):faces.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 faces.append(tuple((len(ps)-1)*n+k for k in range(n)));mesh.add(verts,faces,mat)

def leaf_blade(mesh,start,direction,length,width,rise,mat):
 p=Vector(start);u=Vector(direction).normalized();v=u.cross(Vector((0,0,1))).normalized();z=Vector((0,0,1));outline=[p,p+u*length*.28+v*width,p+u*length*.72+v*width*.72+z*rise*.6,p+u*length+z*rise,p+u*length*.72-v*width*.72+z*rise*.6,p+u*length*.28-v*width];ctr=p+u*length*.50+z*(rise*.30+width*.22);vs=[tuple(q) for q in outline]+[tuple(ctr),tuple(ctr-z*.00055)];fs=[]
 for k in range(6):fs.extend([(6,k,(k+1)%6),(7,(k+1)%6,k)])
 mesh.add(vs,fs,mat)

def ellipse_loft(mesh,sections,n=18,mat=0):
 # Axial Y loft. All rings have positive finite radii and outward winding.
 v=[];f=[]
 for x,y,z,rx,rz in sections:
  for k in range(n):a=2*pi*k/n;v.append((x+rx*math.cos(a),y,z+rz*math.sin(a)))
 f.append(tuple(range(n)))
 for j in range(len(sections)-1):
  for k in range(n):f.append(tuple(reversed((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))))
 f.append(tuple(reversed(tuple((len(sections)-1)*n+k for k in range(n)))));mesh.add(v,f,mat)

def anomalocaris(c,m):
 body=Mesh('continuous-tapered-flexible-swimming-body-no-broad-head-shield',m);flaps=Mesh('overlapping-lateral-swimming-flaps',m);front=Mesh('paired-curved-frontal-appendages-and-economic-inner-spines',m);eyes=Mesh('naturally-seated-paired-eyestalks-and-eyes',m);tail=Mesh('three-pairs-of-upturned-tail-fan-blades',m);mouth=Mesh('ventral-oral-cone-three-broad-radial-plates',m)
 sections=[]
 for j in range(35):
  t=j/34;y=-.10+.24*t;rx=.004+.031*math.sin(pi*(.12+.84*t))**.75*(1-.52*t);rz=.004+.009*math.sin(pi*t)**.65;x=.003*math.sin(t*pi*1.4);sections.append((x,y,.021,rx,rz))
 ellipse_loft(body,sections,22,0)
 for j in range(10):
  t=(j+3)/14;y=-.080+j*.020;rx=.004+.031*math.sin(pi*(.12+.84*t))**.75*(1-.52*t)
  for sign in [-1,1]:
   start=Vector((sign*rx*.76,y,.019));d=Vector((sign*.88,.48,0));L=.043*(1-.45*j/10);leaf_blade(flaps,start,d,L,.012*(1-.35*j/10),.0025,1)
 for sign in [-1,1]:
  ps=smooth_path([(sign*.020,-.086,.019),(sign*.034,-.116,.010),(sign*.024,-.145,.005),(sign*.012,-.151,.009)],24);front.tube(ps,[.0055*(1-i/23)+.0020*(i/23) for i in range(24)],2,n=10)
  for j in range(6):
   p=ps[5+j*3];tip=p+Vector((-sign*(.006-.0004*j),-.002,-.004));front.tube([p,(p+tip)*.5,tip],[.0017,.0011,.00022],2,n=6)
  p=smooth_path([(sign*.020,-.082,.029),(sign*.035,-.089,.033),(sign*.044,-.093,.038)],10);eyes.tube(p,[.0030*(1-i/9)+.0020*(i/9) for i in range(10)],0,n=9);eyes.ellipsoid(p[-1],(.0085,.0070,.0060),3,n=14,r=9)
  for j in range(3):
   start=Vector((sign*(.007+.001*j),.105+.006*j,.020));end=Vector((sign*(.022+.009*j),.170-.011*j,.051-.006*j));p=smooth_path([start,(start+end)*.5+Vector((sign*.002,-.002,.003)),end],11);flat_strap(tail,p,[.0090*math.sin(pi*(.12+.84*i/10))+.0004 for i in range(11)],.0011,(sign*.9,-.4,0),1,n=8)
 # Three broad plate sectors, no unsupported fourthfold/Peytoia scheme or microteeth.
 center=Vector((0,-.069,.0125))
 for j in range(3):
  a=j*2*pi/3;points=[]
  for rad,angles in [(.012,[a+k*(2*pi/3*.94)/5 for k in range(6)]),(.004,[a+(5-k)*(2*pi/3*.94)/5 for k in range(6)])]:
   for ang in angles:points.append(center+Vector((rad*math.cos(ang),rad*math.sin(ang),0)))
  n=len(points);v=[tuple(q+Vector((0,0,z))) for z in [-.001,.001] for q in points];f=[tuple(reversed(range(n))),tuple(n+k for k in range(n))]
  for k in range(n):f.append((k,(k+1)%n,n+(k+1)%n,n+k))
  mouth.add(v,f,2)
 body.finish(c);flaps.finish(c,False);front.finish(c);eyes.finish(c);tail.finish(c);mouth.finish(c,False)

def jimaodanus(c,m):
 axis=Mesh('preserved-narrow-algal-axis-fragment-only',m);brush=Mesh('lower-branched-hairlike-whorls-with-secondary-filament-tier',m);clubs=Mesh('upper-subapical-unbranched-clavate-lateral-crown',m)
 ps=smooth_path([(0,0,.002),(.001,0,.045),(-.001,.002,.085),(.001,.001,.125)],25);axis.tube(ps,[.0020*(1-i/24)+.0009*(i/24) for i in range(25)],0,n=10)
 for j,z in enumerate([.021,.043,.064]):
  for k in range(8):
   a=2*pi*k/8+j*.34;u=Vector((math.cos(a),math.sin(a),0));v=Vector((-u.y,u.x,0));start=Vector((0,0,z));p=smooth_path([start,start+u*.012+Vector((0,0,.001)),start+u*.027+Vector((0,0,.006))],9);brush.tube(p,[.00070*(1-i/8)+.00015*(i/8) for i in range(9)],1,n=6)
   for sign in [-1,1]:
    b=p[4];q=smooth_path([b,b+u*.006+v*sign*.005+Vector((0,0,.001)),b+u*.014+v*sign*.008+Vector((0,0,.005))],7);brush.tube(q,[.00039*(1-i/6)+.00009*(i/6) for i in range(7)],1,n=5)
 # Different topology and size tier: simple club-shaped laterals have no forks.
 for k in range(8):
  a=2*pi*k/8+.22;u=Vector((math.cos(a),math.sin(a),0));p=smooth_path([(0,0,.096),tuple(u*.012+Vector((0,0,.104))),tuple(u*.024+Vector((0,0,.118))),tuple(u*.0245+Vector((0,0,.125)))],14);r=[.0009,.0011,.0014,.0018,.0024,.0032,.0040,.0045,.0048,.0048,.0044,.0035,.0023,.0005];clubs.tube(p,r,2,n=10)
 axis.finish(c);brush.finish(c);clubs.finish(c)

def hydrothermal_chimney(c,m):
 rock=Mesh('continuous-layered-mineral-tower-with-true-narrow-open-conduit',m);N=36;R=28;v=[]
 def center(t):return Vector((.028*math.sin(t*4),.016*math.sin(t*7),.85*t))
 for inner in [False,True]:
  for j in range(R):
   t=j/(R-1);cen=center(t)
   for k in range(N):
    a=2*pi*k/N;profile=.105+.130*(1-t)**1.7+.018*math.sin(t*pi*4+.6)*(1-.4*t);growth=.055*math.sin(3*a+t*3)+.032*math.sin(7*a-t*5)+.040*math.sin(a*4+.8)*math.exp(-((t-.35)/.23)**2);rad=(.026+.006*math.sin(t*5+a*2)) if inner else profile*(1+growth)+.010*math.sin(t*27+a*1.2)**3
    z=cen.z+((.014*math.sin(3*a+.4)+.007*math.sin(7*a))*(t**9));v.append((cen.x+rad*math.cos(a),cen.y+rad*math.sin(a),z))
 f=[];mi=[];off=N*R
 for inner in [False,True]:
  for j in range(R-1):
   for k in range(N):a=j*N+k;q=(a,j*N+(k+1)%N,(j+1)*N+(k+1)%N,a+N);f.append(tuple(off+i for i in reversed(q)) if inner else q);mi.append(2 if inner else (1 if (j+int(2*math.sin(k*.5)))%7 in [0,1] else 0))
 for k in range(N):
  q=(R-1)*N+k;b=(R-1)*N+(k+1)%N;f.append((q,b,off+b,off+q));mi.append(1)
  f.append((k,off+k,off+(k+1)%N,(k+1)%N));mi.append(0)
 rock.add(v,f,mi);o=rock.finish(c,False)
 # The continuous inner wall is smoothly shaded, exterior growth facets remain low-poly.
 for p in o.data.polygons[(R-1)*N:2*(R-1)*N]:p.use_smooth=True

def cube_mesh(name,lo,hi,c,m):
 x0,y0,z0=lo;x1,y1,z1=hi;v=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)];f=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];mesh=Mesh(name,m);mesh.add(v,f);return mesh.finish(c,False)

def arenicolites_u_burrow(c,m):
 rock=cube_mesh('teaching-host-sediment-with-real-internal-U-cavity-no-spreite',(-.40,-.12,0),(.40,.18,.65),c,m)
 bpy.context.view_layer.objects.active=rock;rock.select_set(True);bev=rock.modifiers.new('soft-display-block-edges','BEVEL');bev.width=.005;bev.segments=2;bpy.ops.object.modifier_apply(modifier=bev.name)
 window=cube_mesh('_construction-front-section-cut',(-.50,-.40,-.04),(.50,0,.565),c,m)
 def difference(cutter,label):
  bpy.context.view_layer.objects.active=rock;mod=rock.modifiers.new(label,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 difference(window,'illustrative-open-front-section-not-excavated-specimen')
 cut_offset=.00037
 ps=[Vector((-.20,cut_offset,.72-(.72-.25)*j/18)) for j in range(19)]
 ps += [Vector((.20*math.cos(pi+pi*j/28),cut_offset,.25+.20*math.sin(pi+pi*j/28))) for j in range(1,29)]
 ps += [Vector((.20,cut_offset,.25+(.72-.25)*j/18)) for j in range(1,19)]
 cutter=Mesh('_construction-negative-two-shafts-and-basal-U-link',m);cutter.tube(ps,[.028]*len(ps),0,n=20);negative=cutter.finish(c,False);difference(negative,'true-U-conduit-through-host-rock')
 import bmesh
 bm=bmesh.new();bm.from_mesh(rock.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='EAR_CLIP');bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(rock.data);bm.free();rock.data.update()
 # Assign only actual tunnel-wall polygons a restrained neutral lining colour/shading.
 def distance(q):
  if q.z>=.25:return min(math.hypot(q.x+.20,q.y-cut_offset),math.hypot(q.x-.20,q.y-cut_offset))
  return math.hypot(math.hypot(q.x,q.z-.25)-.20,q.y-cut_offset)
 for p in rock.data.polygons:
  q=p.center
  if abs(distance(q)-.028)<.0025:p.material_index=1;p.use_smooth=True

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'anomalocaris': [('flexible-radiodont-body', '#A7977E'), ('swimming-flaps-and-raised-tail', '#B8A98B'), ('curved-frontal-limbs-and-three-oral-plates', '#94856F'), ('stalked-eyes', '#424C42')], 'jimaodanus': [('preserved-narrow-algal-axis', '#8C8D72'), ('fine-branched-lower-whorls', '#9A9C7E'), ('unbranched-clavate-upper-crown', '#A4A085')], 'hydrothermal-chimney': [('continuous-mineral-growth-body', '#878A7B'), ('growth-rims-and-broad-depositional-steps', '#A3A088'), ('narrow-conduit-wall', '#6F7569')], 'arenicolites-u-burrow': [('neutral-host-sediment-cut-section', '#A5A69C'), ('neutral-real-tunnel-wall', '#8A8D83')]}
 mats=[make_material(name,color,roughness=.82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=.24 if slug=='anomalocaris' else ((hi[2]-lo[2]) if slug in ['jimaodanus','hydrothermal-chimney'] else hi[0]-lo[0]);scale=cfg['nominal_scale']['meters']/extent
 # Scale authored edge skeletons and skin radii together; evaluated source remains editable and physically scaled.
 for o in c.all_objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co*=scale
   if o.data.skin_vertices:
    for d in o.data.skin_vertices[0].data:d.radius=(d.radius[0]*scale,d.radius[1]*scale)
 lo,hi=_bounds(_vertices_world(c))
 for o in c.all_objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co.z-=lo[2]
 brief=json.loads((a.config.parent/'brief.json').read_text());refs=json.loads((a.config.parent/'references.json').read_text());desc={'en':'Original evidence-informed stylized teaching form; nominal scale, palette and simplified counts are artistic. Static only; no exact species, location, locomotion or shared habitat reconstruction.','zh':'原创依据基础形态的风格化教学造型；名义尺度、配色及简化数量属美术选择。仅静态，不声称精确种、地点、运动机制或共同栖息地复原。'}
 descriptions={'anomalocaris': {'en': 'Original Anomalocaris-inspired tapered flexible marine swimmer with overlapping lateral flaps, paired curved frontal appendages and stalked eyes, three pairs of upturned tail blades and a simplified three-plate ventral oral cone. No broad horseshoe head shield or recolored earlier radiodont mesh. Spine/teeth counts and static pose artistic; no predation animation. Nominal length refers to the tapered body, excluding appendage/fan display extremes.', 'zh': '原创Anomalocaris启发海生渐细柔躯游泳体，侧叶叠接、成对弯前附肢与柄眼、三对上扬尾叶及简化三大板腹口；无宽马蹄头盾，不为旧奇虾类改色网格。刺齿数量和静态姿势属艺术选择，不作捕食动画；名义体长指渐细躯体，不计附肢/尾扇展示极值。'}, 'jimaodanus': {'en': 'Jimaodanus-inspired preserved algal axis fragment only, with lower branched hairlike whorls in a fine secondary branching tier and an upper subapical crown of thicker simple unbranched clavate laterals. Two distinct branch types, not duplicated branches with changed density. Historical Heterocladus name retained as nomenclatural context only; no roots, unknown mother thallus or complete living plant claim.', 'zh': 'Jimaodanus启发保存藻轴片段，下部细刷轮枝具次级分叉，上部近顶冠为较粗未分叉棒瓣，两区枝型与粗细阶次不同，非同枝改密度。历史Heterocladus名仅作命名背景，不添根、未知母藻或完整活体植物。'}, 'hydrothermal-chimney': {'en': 'Original hydrothermal-chimney process analog: one irregular continuous mineral-growth tower surrounds a true narrow open conduit. Broad changing growth shoulders/rims are part of the same wall geometry, not sleeves or inserted stones. No plume, water mesh, eruption simulation, exact mineral site or paleoecological coexistence claim. Empty eras/biomes facets remain unspecified.', 'zh': '原创热液烟囱过程类比：连续不规则矿物生长塔包围真实狭窄开口通道，变化的生长肩部和层缘属于同一塔壁几何，非套筒或插石。不导出烟羽水体、不模拟喷发、不指定矿点或古生态共存；空时代/生境facet保持未指定。'}, 'arenicolites-u-burrow': {'en': 'Arenicolites interpretive section only: a real narrow U-shaped negative channel cuts the neutral host sediment, two vertical shafts connect in a simple basal bend without intervening spreiten. Top cap retains two openings; exposed gray front/clay sections reveal internal geometry. No suspended tube, identified maker, feeding assignment or copied excavated specimen. Teaching block width is nominal.', 'zh': 'Arenicolites潜穴示意剖面：真实窄U形负空间切入中性灰围岩，两竖井以简单底弯相连，中间无蹼状叠层；顶盖保留双开口，灰色前剖面/灰模可见内部结构。非悬空圆管，不指定制造者、取食方式或复制出土标本；教学块宽度属名义尺度。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 mp=a.output/'metadata.json';md=json.loads(mp.read_text());facets=brief['catalog_facets'];md['catalog_facets']=facets;md['research_packs']=facets['packs'];md['packs']=[];md['pack_membership_status']='research-only; no published pack membership asserted'
 for key in ['worlds','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type']:md[key]=facets[key]
 md['collection']=facets['worlds'][0] if facets['worlds'] else None;mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
