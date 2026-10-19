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

def ecphora(c,m):
 # One continuous helical shell surface: broad-rooted T crests deform the wall itself.
 shell=Mesh('original-coiled-Ecphora-shell-with-integral-four-costae-and-open-canal',m);N=80;R=66;v=[];f=[];mi=[]
 def section(t,phi,inner=False):
  theta=-1.5*pi+5.4*pi*t;rad=.035*math.exp(2.45*t);rr=.010+.405*t**3.0;z=.92-.73*t
  # Apertural bottom grows into the prolonged open siphonal canal, not a separate rod.
  bottom=max(0,-math.sin(phi))**18;canal=.41*max(0,(t-.83)/.17)**1.4*bottom
  crest=0
  for p in [-.90,-.30,.32,.94]:
   d=abs((phi-p+pi)%(2*pi)-pi)
   # Shoulder below broad crest makes a thick T section rather than a thin disk.
   crest+=.073*math.exp(-(d/.052)**4)+.034*math.exp(-(d/.12)**2)
  crest*=min(1,t/.40)
  if inner:cr=rr*.86;crest*=.12
  else:cr=rr
  out=Vector((math.cos(theta),math.sin(theta),0));ctr=out*rad+Vector((0,0,z))
  return tuple(ctr+out*((cr+crest)*math.cos(phi))+Vector((0,0,(cr+crest)*math.sin(phi)-canal)))
 for j in range(R):
  for k in range(N):v.append(section(j/(R-1),2*pi*k/N))
 f.append(tuple(reversed(range(N))));mi.append(0)
 for j in range(R-1):
  for k in range(N):f.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k));mi.append(0)
 off=len(v);IR=15
 for j in range(IR):
  t=1-.16*j/(IR-1)
  for k in range(N):v.append(section(t,2*pi*k/N,True))
 edge=(R-1)*N
 for k in range(N):f.append((edge+k,edge+(k+1)%N,off+(k+1)%N,off+k));mi.append(1)
 for j in range(IR-1):
  for k in range(N):f.append((off+j*N+k,off+j*N+(k+1)%N,off+(j+1)*N+(k+1)%N,off+(j+1)*N+k));mi.append(1)
 f.append(tuple(off+(IR-1)*N+k for k in reversed(range(N))));mi.append(1)
 shell.add(v,f,mi);shell.finish(c)

def pteleoidea(c,m):
 wing=Mesh('original-two-coplanar-wings-notched-obovate-fruit',m);N=64;J=9;v=[];f=[]
 def edge(a):
  # Two joined lateral wings, rounded broad apex with a small terminal notch.
  width=.36*(1+.23*math.cos(a));x=width*math.sin(a);y=.53*math.cos(a);notch=.075*math.exp(-(math.sin(a)/.16)**2) if math.cos(a)>0 else 0
  return x,y-notch
 for side in [1,-1]:
  for j in range(J):
   t=.10+.90*j/(J-1)
   for k in range(N):
    a=2*pi*k/N;x,y=edge(a);fold=.012*math.sin(6*a+.25)*t*(1-t)+.018*(1-t)
    v.append((x*t,y*t,.045+fold+side*(.003+.004*(1-t))))
 base=J*N
 for side,off in [(1,0),(-1,base)]:
  f.append(tuple(off+k for k in (reversed(range(N)) if side<0 else range(N))))
  for j in range(J-1):
   for k in range(N):
    q=(off+j*N+k,off+j*N+(k+1)%N,off+(j+1)*N+(k+1)%N,off+(j+1)*N+k);f.append(q if side<0 else tuple(reversed(q)))
 for k in range(N):f.append(((J-1)*N+k,(J-1)*N+(k+1)%N,base+(J-1)*N+(k+1)%N,base+(J-1)*N+k))
 wing.add(v,f,0);wing.finish(c)
 organ=Mesh('fusiform-central-locule-and-narrow-attached-pedicel-style',m)
 organ.ellipsoid((0,-.025,.051),(.077,.36,.043),1,n=24,r=17)
 p=smooth_path([(0,-.345,.052),(.012,-.55,.046),(.025,-.76,.043),(.020,-.90,.045)],22);organ.tube(p,[.012*(1-.45*j/21) for j in range(22)],1,10)
 p=smooth_path([(0,.30,.052),(0,.41,.052),(.006,.485,.050)],12);organ.tube(p,[.006*(1-.5*j/11) for j in range(12)],1,8);organ.finish(c)

def karst_spring_mouth(c,m):
 # Low continuous roof/wall volume with a bounded hollow gallery, open at its mouth.
 rock=Mesh('continuous-thick-rock-roof-low-spring-cavity-and-wall',m);N=64;R=12;v=[];f=[]
 def outer(j,k):
  a=2*pi*k/N;t=j/(R-1);s=1-.12*t;wav=1+.025*math.sin(5*a+1.5*t)+.018*math.cos(9*a-t)
  return (1.18*s*math.copysign(abs(math.cos(a))**.64,math.cos(a))*wav,.0+1.1*t,.56+.51*s*math.sin(a)*wav)
 def inner(j,k):
  a=2*pi*k/N;t=j/(R-1);s=1-.18*t
  return (.55*s*math.cos(a),.0+.89*t,.39+.245*s*math.sin(a)*(1+.025*math.cos(3*a)))
 for j in range(R):
  for k in range(N):v.append(outer(j,k))
 for j in range(R-1):
  for k in range(N):f.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
 f.append(tuple(reversed([(R-1)*N+k for k in range(N)])))
 off=len(v)
 for j in range(R):
  for k in range(N):v.append(inner(j,k))
 for k in range(N):f.append((k,off+k,off+(k+1)%N,(k+1)%N))
 for j in range(R-1):
  for k in range(N):f.append((off+j*N+k,off+(j+1)*N+k,off+(j+1)*N+(k+1)%N,off+j*N+(k+1)%N))
 f.append(tuple(off+(R-1)*N+k for k in range(N)));rock.add(v,f,0);rock.finish(c)
 bed=Mesh('attached-exposed-rock-bed-and-short-open-spring-channel-no-water',m);nx=52;ny=40;v=[];f=[]
 for j in range(ny+1):
  t=j/ny;y=-1.65+1.90*t
  for i in range(nx+1):
   x=-1.23+2.46*i/nx;ctr=.11*math.sin(2*y);width=.27+.12*(1-t);bank=1-math.exp(-((x-ctr)/width)**4);z=.10+.16*bank+.05*t+.035*math.sin(x*3+y)*bank
   # Blend the full channel cross-section into the gallery floor, not just its center.
   if y>-.45:
    ss=1-.18*max(0,y)/.89;rx=.55*ss
    if abs(x)<rx*.98:
     target=.39-.245*ss*math.sqrt(max(0,1-(x/rx)**2))-.002
     blend=min(1,max(0,(y+.45)/.55));blend=blend*blend*(3-2*blend);z=z*(1-blend)+target*blend
   v.append((x,y,z))
 for j in range(ny):
  for i in range(nx):a=j*(nx+1)+i;f.append((a,a+1,a+nx+2,a+nx+1))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];off=len(v)
 for a in boundary:x,y,z=v[a];v.append((x,y,0))
 center=len(v);v.append((0,-.7,0))
 for j,a in enumerate(boundary):b=boundary[(j+1)%len(boundary)];f.append((a,off+j,off+(j+1)%len(boundary),b));f.append((center,off+(j+1)%len(boundary),off+j))
 bed.add(v,f,0);bed.finish(c)

def shatter_cone_rock(c,m):
 rock=Mesh('original-nested-conical-fracture-face-with-aligned-feathered-relief',m);nx=65;nz=52;v=[];f=[]
 # A cone-fan envelope opens downward from a common apex; nested lips carry feathered ridges.
 for j in range(nz+1):
  t=j/nz;z=.90-.86*t;width=.13+.48*t**.7
  for i in range(nx+1):
   q=-1+2*i/nx;x=width*q;rad=math.hypot(x,z-.98);theta=math.atan2(x,.98-z)
   cone=.11*math.sqrt(max(0,1-q*q))*(.3+.7*t)
   nested=.026*(.5+.5*math.cos(rad*34+1.2*theta))**3
   feather=.012*(.2+.8*t)*(math.cos(theta*43+rad*5)+.35*math.cos(theta*79-rad*3))
   y=-.16-cone-nested-feather;v.append((x,y,z+.012*math.sin(q*3)*t))
 for j in range(nz):
  for i in range(nx):a=j*(nx+1)+i;f.append((a,a+nx+1,a+nx+2,a+1))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,nz+1)]+[nz*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(nz-1,0,-1)];off=len(v)
 for a in boundary:x,y,z=v[a];v.append((x,.075+.035*math.sin(z*4+x),z))
 center=len(v);v.append((0,.11,.48))
 for j,a in enumerate(boundary):b=boundary[(j+1)%len(boundary)];f.append((a,b,off+(j+1)%len(boundary),off+j));f.append((center,off+j,off+(j+1)%len(boundary)))
 rock.add(v,f,0);rock.finish(c)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'ecphora': [('original-fossil-shell-and-integral-costae', '#ADA18A'), ('real-shell-wall-interior', '#B8AC94')], 'pteleoidea': [('two-thin-coplanar-fossil-wings', '#B5AA8F'), ('central-locule-stalk-and-style', '#9D927A')], 'karst-spring-mouth': [('continuous-weathered-spring-bedrock', '#ABA591')], 'shatter-cone-rock': [('original-directional-fractured-rock', '#AAA695')]}
 mats=[make_material(name,color,roughness=.86) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=max(hi[i]-lo[i] for i in range(3)) if slug in ['ecphora','pteleoidea'] else hi[0]-lo[0];scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'ecphora': {'en': 'Original preserved Ecphora shell inspired by the frozen Miocene E. gardnerae gardnerae reference scope: rounded whorls with four projecting T-section spiral costae grown continuously from the shell wall, an open umbilical axis and a prolonged aperture canal. Real shell wall and aperture, no soft body, foot or life-mechanism assertion. Nominal75mm length, color, growth increments and display pose are artistic, not copied specimen measurements.', 'zh': '原创保存Ecphora螺壳，以冻结中新世E.gardnerae gardnerae范围启发：圆壳圈上的四道T形螺肋连续生于壳壁，开放轴向脐部与延长壳口沟，真实壳壁开口。无软体足或生活机制断言；名义75毫米、配色生长起伏与展示姿态属美术，非标本实测复制。'}, 'pteleoidea': {'en': 'Original preserved Pteleoidea fruit organ only: a raised fusiform central locule joins two coplanar broad wings forming an obovate notched outline, a modest apical style and a narrow retained pedicel. Thin folded wing relief, nominal45mm span and quiet color are artistic. No funnel calyx, separate seed, known parent tree, leaves or precise phylogenetic claim.', 'zh': '原创保存Pteleoidea果器官：隆起纺锤中央腔体相接共面两宽翅，组成倒卵环状顶缺口轮廓，克制顶端花柱和细柄。薄翅折面起伏、名义45毫米与配色属美术；不加漏斗萼、独立种子、未知母树叶或精确亲缘推论。'}, 'karst-spring-mouth': {'en': 'Original nominal3m representative karst spring rock-and-bed patch: a low real cavity beneath a thick continuous rock roof opens directly into a short exposed channel in the attached bed. Geometric cavity, wall thickness and bed connection remain visible without water or blue shading; no water, lights or flow simulation exported. Layout, crop and scale are artistic, not a measured spring, hydrological rate, named site or exact age.', 'zh': '原创名义3米岩溶泉口岩床裁片：厚实连续岩顶下低矮真实洞腔直接通向相接床面的短明渠。无水蓝色也可见洞腔壁厚及床面连接，不导出水灯或流动模拟。布局裁片与尺度属美术，非实测泉流地点年代。'}, 'shatter-cone-rock': {'en': 'Original nominal32cm interpretive rock fragment exposing nested curved conical fracture surfaces and aligned radiating ridges with actual relief, not painted straight scratches or an assembly of pointed cones. Shared direction and primary/secondary surface hierarchy are deliberately readable in gray. Generic impact-related teaching form only, no measured event, locality, pressure, stress direction or precise impact age.', 'zh': '原创名义32厘米教学岩块，露出嵌套弯曲锥状断裂面及方向一致放射脊，真实起伏而非直线刻纹或尖锥堆。灰模下主次面层次与共同方向可读；仅通用撞击相关形态，不作实测事件地点压力应力方向或精确撞击年代。'}}
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
