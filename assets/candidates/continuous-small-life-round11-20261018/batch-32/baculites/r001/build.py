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

def ctenocystis(c,m):
 body=Mesh('original-low-bilateral-rounded-theca-not-boot-or-crab',m);frame=Mesh('paired-marginal-plate-frame-and-broad-dorsal-fields',m);comb=Mesh('anterior-ctenidium-blade-like-comb-plates',m)
 N=40;v=[];f=[]
 def xy(a,t=1):return Vector((.020*t*math.copysign(abs(math.cos(a))**.68,math.cos(a)),.024*t*math.copysign(abs(math.sin(a))**.68,math.sin(a)),0))
 for t,z in [(1,.0025),(1.01,.0055),(.88,.0095),(.58,.0115)]:
  for k in range(N):q=xy(2*pi*k/N,t);v.append((q.x,q.y,z+.0004*math.cos(2*pi*k/N)**2))
 f.append(tuple(reversed(range(N))))
 for j in range(3):
  for k in range(N):f.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
 top=len(v);v.append((0,.001,.0122))
 for k in range(N):f.append((3*N+k,3*N+(k+1)%N,top))
 body.add(v,f,0)
 # Marginal frame fields follow a bilateral curved perimeter rather than square tiles.
 for j in range(16):
  a=2*pi*j/16;b=2*pi*(j+1)/16;aa=a+.035;bb=b-.035;pts=[xy(aa,.96),xy(bb,.96),xy(bb,.76),xy(aa,.76)];vv=[tuple(q+Vector((0,0,z))) for z in [.0073,.0100] for q in pts];ff=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];frame.add(vv,ff,1 if j%4 in [0,3] else 0)
 # A quiet central longitudinal pair gives a readable bilateral dorsal organization.
 for s in [-1,1]:
  pts=[(s*.001,-.016,.0116),(s*.009,-.014,.0114),(s*.010,.013,.0114),(s*.001,.017,.0120)];vv=[(x,y,z+dz) for dz in [-.0006,.0004] for x,y,z in pts];ff=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
  if s<0:ff=[tuple(reversed(q)) for q in ff]
  frame.add(vv,ff,1)
 # Blade-like front comb, no modern articulated limbs or speculative soft feeding parts.
 for j in range(14):
  x=(j-6.5)*.00205;p=smooth_path([(x,-.0210,.0063),(x*1.05,-.0246,.0051),(x*1.08,-.0285+.0012*(abs(x)/.014)**2,.0053)],8);flat_strap(comb,p,[.00076*(1-.20*i/7) for i in range(8)],.00038,(1,0,0),2,n=8)
 body.finish(c);frame.finish(c,False);comb.finish(c)

def baculites(c,m):
 shell=Mesh('preserved-compressed-nearly-straight-shell-with-real-aperture',m);N=40;R=35;v=[];f=[];mi=[]
 def section(t):
  rx=.0135*(1-t)+.0032*t;rz=.0067*(1-t)+.0019*t;return (.0018*math.sin(t*pi),-.100+.200*t,.008+.0012*math.sin(t*pi),rx,rz)
 for j in range(R):
  t=j/(R-1);x,y,z,rx,rz=section(t);growth=1+.017*math.sin(t*pi*18)*(1-t)
  for k in range(N):a=2*pi*k/N;v.append((x+rx*growth*math.cos(a),y,z+rz*growth*math.sin(a)))
 for j in range(R-1):
  for k in range(N):q=(j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k);f.append(tuple(reversed(q)));mi.append(0)
 f.append(tuple(reversed([(R-1)*N+k for k in range(N)])));mi.append(0)
 off=len(v);IR=17
 for j in range(IR):
  t=.32*j/(IR-1);x,y,z,rx,rz=section(t)
  for k in range(N):a=2*pi*k/N;v.append((x+rx*.78*math.cos(a),y,z+rz*.73*math.sin(a)))
 for k in range(N):f.append((k,(k+1)%N,off+(k+1)%N,off+k));mi.append(1)
 for j in range(IR-1):
  for k in range(N):f.append((off+j*N+k,off+j*N+(k+1)%N,off+(j+1)*N+(k+1)%N,off+(j+1)*N+k));mi.append(2)
 f.append(tuple(off+(IR-1)*N+k for k in range(N)));mi.append(2)
 shell.add(v,f,mi);shell.finish(c)

def estuary_basin(c,m):
 terrain=Mesh('continuous-estuary-land-and-bed-with-connected-widening-channel-network-no-water',m);nx=58;ny=48;v=[];f=[];mi=[]
 def h(x,y):
  t=(5-y)/10;center=.45*math.sin(y*.65)*(1-.45*t);width=.27+2.40*t**1.75;dist=abs(x-center);bank=1/(1+math.exp(-max(-25,min(25,(dist-width)/.20))))
  z=.18+.28*(1-t)+.83*bank+.065*math.sin(x*.65+y*.31)*bank
  # Two side channels join the main channel; they are bed depressions, not water geometry.
  for side,y0 in [(-1,1.4),(1,-.6)]:
   along=side*x
   if 0<along<3.8:
    cy=y0+.48*along+.13*math.sin(along*1.8);dip=math.exp(-((y-cy)/(.15+.045*along))**2)*(.50+.14*(1-along/3.8));z-=dip*bank
  # One low elongated shoal splits the broad lower reach while preserving two connected routes.
  shoal=.29*math.exp(-((x+.12)/.45)**2-((y+2.1)/1.15)**2);z+=shoal
  return max(.14,z),bank
 for j in range(ny+1):
  y=-5+10*j/ny
  for i in range(nx+1):x=-6+12*i/nx;z,_=h(x,y);v.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;f.append((a,a+1,a+nx+2,a+nx+1));x=-6+12*(i+.5)/nx;y=-5+10*(j+.5)/ny;z,bank=h(x,y);mi.append(0 if bank>.85 and z>.8 else (1 if bank>.22 or z>.57 else 2))
 boundary=[i for i in range(nx+1)]+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];off=len(v)
 for k in boundary:x,y,z=v[k];v.append((x,y,0))
 for j,a in enumerate(boundary):b=boundary[(j+1)%len(boundary)];f.append((a,off+j,off+(j+1)%len(boundary),b));mi.append(1)
 f.append(tuple(reversed([off+j for j in range(len(boundary))])));mi.append(1);terrain.add(v,f,mi);terrain.finish(c,False)

def cross_bedded_sandstone(c,m):
 beds=Mesh('three-crossbed-sets-with-physically-truncated-inclined-laminae',m)
 def clip(poly,A,B,C):
  out=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   dp=A*p[0]+B*p[1]+C;dq=A*q[0]+B*q[1]+C;inside=dp>=-1e-10
   if inside:out.append(p)
   if inside!=(dq>=-1e-10):t=dp/(dp-dq);out.append((p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t))
  clean=[]
  for q in out:
   if not clean or math.dist(q,clean[-1])>1e-8:clean.append(q)
  if len(clean)>1 and math.dist(clean[0],clean[-1])<1e-8:clean.pop()
  return clean
 for g,(lo,hi,slope,phase) in enumerate([(0,.165,.30,.007),(.165,.335,-.38,.012),(.335,.505,.23,.004)]):
  spacing=.026
  for j in range(-10,27):
   b=j*spacing+phase;p=[(-.4,lo),(.4,lo),(.4,hi),(-.4,hi)];p=clip(p,-slope,1,-b);p=clip(p,slope,-1,b+spacing)
   area=abs(sum(p[k][0]*p[(k+1)%len(p)][1]-p[(k+1)%len(p)][0]*p[k][1] for k in range(len(p)))/2) if len(p)>2 else 0
   if area<1e-8:continue
   n=len(p);front=-.16+.0030*((j+g)%3);back=.145;vv=[(x,y,z) for y in [front,back] for x,z in p];ff=[tuple(range(n)),tuple(reversed([n+k for k in range(n)]))]
   # Front polygon order in XZ has normal -Y. Side order closes each true wedge.
   for k in range(n):ff.append((k,n+k,n+(k+1)%n,(k+1)%n))
   beds.add(vv,ff,0 if (j+g)%3 else 1)
 beds.finish(c,False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'ctenocystis': [('bilateral-low-theca', '#ADA88F'), ('marginal-frame-and-dorsal-fields', '#C0B99D'), ('anterior-ctenidium-blades', '#B9B39C')], 'baculites': [('preserved-compressed-original-shell', '#B5AB8C'), ('aperture-wall-rim', '#CCBFA0'), ('real-inner-shell-chamber', '#8B8B76')], 'estuary-basin': [('low-bank-land', '#9AA184'), ('sandy-muddy-banks-and-shoal', '#B8AA89'), ('connected-exposed-channel-bed-not-water', '#8D9281')], 'cross-bedded-sandstone': [('sandstone-inclined-laminae', '#B2A386'), ('subtle-lamina-color-variation', '#C1B294')]}
 mats=[make_material(name,color,roughness=.86) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=(hi[1]-lo[1]) if slug in ['ctenocystis','baculites'] else hi[0]-lo[0];scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'ctenocystis': {'en': 'Original Ctenocystis-inspired low flattened bilateral plated theca with a curved marginal frame, quiet paired dorsal fields and naturally seated anterior blade-like ctenidium comb. Stemless basic form, no crab legs, Cothurnocystis boot rescale, exact plate counts, Conollia-specific details or feeding/locomotion reconstruction.', 'zh': '原创Ctenocystis启发低扁双侧板甲体，弧形边缘板框、克制成对背板与自然接合的前缘梳状刀片。基础无柄形态，不加蟹肢，不由Cothurnocystis靴体缩放，不承诺精确板数/Conollia细节或取食运动复原。'}, 'baculites': {'en': 'Baculites-inspired preserved shell specimen only: a nearly straight tapering compressed section with a real wall, broad elliptical aperture and a bounded inner chamber. Quiet original shell surface, not an internal-mold suture pattern used as external decoration. No solid round rod, plant stem, unsupported living soft parts or tentacles; no specimen/model copying.', 'zh': 'Baculites启发保存壳标本：近直渐细扁截面、真实壳壁与较宽椭圆壳口和有限内腔；安静原创壳面，不把内模缝合线当外饰。非实心圆棍/植物茎，不加活体软组织触手，不复制标本模型。'}, 'estuary-basin': {'en': 'Original nominal12m representative estuary land/bed patch: narrow upstream river expands toward an open mouth, connected side channels and a low shoal split/rejoin the exposed bed through continuous banks. All exported geometry is land/sediment, no water/lights, no salt/tidal simulation, no whole paleo-coast map or measured locality. Landscape scale retained, empty eras unspecified.', 'zh': '原创名义12米河口土地/床面代表片：上游窄河向开阔口部展宽，连通支水道与低沙洲使露床通路分合，岸坡连续。只导出陆地沉积物，无水体灯光，不模拟潮汐盐度，不作全古岸测图或实测地点；保留landscape尺度与空时代。'}, 'cross-bedded-sandstone': {'en': 'Original0.8m sandstone teaching exposure with three cross-bed sets: physical inclined wedge laminae end against distinct set boundaries, with alternating dip directions and subtle real cut-face relief readable in gray. Not texture-only diagonal stripes, a uniformly rotated older cliff, or a precise paleocurrent/site/age reconstruction. Empty era/biome facets remain unspecified.', 'zh': '原创0.8米砂岩教学露面，三组物理倾斜楔形细层被清楚组界截切，倾向交替且剖面有微小真实阶差，灰模可读。非仅贴斜纹、整体旋转旧崖，不推定精确古水流/地点/年代；空时代生境保持未指定。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'reference_status':'basic-form textual reference support with explicit limits; not strict reconstruction','publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 mp=a.output/'metadata.json';md=json.loads(mp.read_text());facets=brief['catalog_facets'];md['catalog_facets']=facets;md['research_packs']=facets['packs'];md['packs']=[];md['pack_membership_status']='research-only; no published pack membership asserted'
 for key in ['worlds','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type']:md[key]=facets[key]
 md['scale_class']=json.loads((a.config.parent/'inventory-record.json').read_text())['scale_class'];md['collection']=facets['worlds'][0] if facets['worlds'] else None;mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
