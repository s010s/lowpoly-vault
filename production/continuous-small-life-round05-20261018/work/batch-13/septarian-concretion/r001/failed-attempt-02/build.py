# SPDX-License-Identifier: MIT
"""Original evidence-informed marine teaching forms. Blender -b -t 2 --python build.py -- --config config.json --output /absolute/r001 [--preview]."""
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

def acrocyathus(c,m):
 cups=Mesh('elongated-polygonal-corallites-with-real-calyces',m);septa=Mesh('radial-calyx-septal-blades',m)
 specs=[(-.042,-.025,.072,.018,7),(-.004,-.036,.094,.020,8),(.038,-.025,.084,.019,7),(-.060,.013,.085,.017,7),(-.026,.009,.112,.023,8),(.021,.013,.105,.022,7),(.055,.014,.076,.018,7),(-.041,.047,.086,.018,7),(.001,.047,.097,.021,8),(.038,.046,.082,.018,7)]
 for idx,(x,y,h,r,n) in enumerate(specs):
  ang=.23*idx;vs=[];fs=[];mi=[];profiles=[(.002,.38),(.015,.55),(.035,.74),(h*.65,.90),(h*.89,.98),(h,1),(h-.001,.86),(h-.011,.76),(h-.025,.48),(h-.031,.10)]
  for z,ratio in profiles:
   t=z/h;cx=x*(.62+.38*t);cy=y*(.62+.38*t)
   for k in range(n):a=2*pi*k/n+ang;vs.append((cx+r*ratio*math.cos(a),cy+r*ratio*math.sin(a),z+.0012*math.sin(a*2+idx)*t))
  fs.append(tuple(reversed(range(n))));mi.append(0)
  for j in range(len(profiles)-1):
   for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if j>=6 else 0)
  fs.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(1);cups.add(vs,fs,mi)
  for k in range(n*2):
   a=2*pi*k/(n*2)+ang;u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0));verts=[];faces=[]
   for j,t in enumerate([0,.35,.7,1]):
    p=Vector((x,y,h-.028))+u*r*(.13+.66*t)+Vector((0,0,.023*t));th=.00045;rise=.0018*(1-.5*t)
    verts.extend([tuple(p-v*th),tuple(p+v*th),tuple(p+Vector((0,0,rise)))])
   faces.append((2,1,0))
   for j in range(3):
    for e in range(3):faces.append((j*3+e,j*3+(e+1)%3,(j+1)*3+(e+1)%3,(j+1)*3+e))
   faces.append((9,10,11));septa.add(verts,faces,2)
 cups.finish(c,False);septa.finish(c)

def sawdonia(c,m):
 from asset_common import link_object
 spines=Mesh('sparse-directional-spines-attached-along-shoots',m)
 for idx,(off,sc,ang) in enumerate([((-.021,.008,0),.88,-.5),((.016,.014,0),.77,.65),((0,-.009,0),1,.05)]):
  p=[(0,0,0),(0,0,.025),(.002,0,.060),(-.002,0,.091),(.004,0,.125),(-.025,.002,.118),(.025,.003,.149),(-.009,.002,.158),(-.036,.004,.151),(.032,.003,.173),(.034,.004,.185),(.029,.005,.192),(.021,.005,.191),(.017,.005,.185),(-.010,.002,.178),(-.017,.002,.185),(-.025,.002,.185),(-.030,.002,.179),(-.044,.004,.169),(-.042,.004,.179),(-.035,.004,.183)]
  edges=[(0,1),(1,2),(2,3),(3,4),(3,5),(4,6),(4,7),(5,8),(6,9),(9,10),(10,11),(11,12),(12,13),(7,14),(14,15),(15,16),(16,17),(8,18),(18,19),(19,20)]
  radii=[.0048,.004,.0034,.003,.0026,.0025,.0022,.0022,.0019,.0018,.0015,.0013,.0010,.0006,.0016,.0013,.0010,.0006,.0013,.001,.0006]
  def xf(v):x,y,z=v;return Vector(off)+Vector(((x*math.cos(ang)-y*math.sin(ang))*sc,(x*math.sin(ang)+y*math.cos(ang))*sc,z*sc))
  v=[tuple(xf(q)) for q in p];mesh=bpy.data.meshes.new('editable-branch-network-'+str(idx));mesh.from_pydata(v,edges,[]);mesh.update();o=bpy.data.objects.new('continuous-spiny-shoot-with-circinate-tips-'+str(idx),mesh);link_object(o,c);mesh.materials.append(m[0]);skin=o.modifiers.new('Continuous natural forks','SKIN');skin.use_smooth_shade=True;bpy.context.view_layer.update()
  for d,r in zip(mesh.skin_vertices[0].data,radii):d.radius=(r*sc,r*sc)
  mesh.skin_vertices[0].data[0].use_root=True;sub=o.modifiers.new('Soft tapered forks and hooked tips','SUBSURF');sub.levels=1;sub.render_levels=1
  for e,(ia,ib) in enumerate(edges):
   if e>9:continue
   pa,pb=Vector(v[ia]),Vector(v[ib]);tangent=(pb-pa).normalized()
   for k,t in enumerate([.30,.68]):
    ctr=pa.lerp(pb,t);a=idx*.8+e*2.05+k*pi;side=Vector((math.cos(a),math.sin(a),0));length=(.0045 if e<4 else .0033)*sc;base=radii[ia]*sc*.82
    start=ctr+side*base;tip=start+side*length+tangent*length*.46
    spines.tube([tuple(start),tuple(start.lerp(tip,.55)),tuple(tip)],[.00065*sc,.00040*sc,.00008],1,n=6)
 spines.finish(c)

def leanchoilia(c,m):
 body=Mesh('overlapping-articulated-trunk-tergites',m);head=Mesh('single-rounded-head-shield-and-small-eyes',m);limbs=Mesh('paired-simplified-walking-and-swimming-limbs',m);arms=Mesh('great-appendages-with-three-flagellate-fingers',m);tail=Mesh('lanceolate-terminal-telson',m)
 # -Y anterior; nominal body length excludes the long anterior flagella.
 head.ellipsoid((0,-.021,.010),(.010,.010,.0055),0,n=24,r=10)
 for i in range(10):
  t=i/9;y=-.010+i*.0041;w=.0095*(1-.53*t**1.6);z=.010-.003*t;body.ellipsoid((.0005*math.sin(i*.35),y,z),(w,.0032,.0039*(1-.45*t)),0 if i%3 else 1,n=16,r=7)
  for sign in [-1,1]:
   x=sign*w*.78;pts=[(x,y,.008-.002*t),(sign*(w+.003),y+.001,.004),(sign*(w+.005),y+.003,.0025),(sign*(w+.0055),y+.004,.002)]
   limbs.tube(pts,[.0011,.0009,.00055,.00018],2,n=7)
   limbs.ellipsoid((sign*(w+.0025),y+.001,.006),(.0025,.0026,.00065),1,n=10,r=5)
 for sign in [-1,1]:
  head.ellipsoid((sign*.007,-.027,.012),(.0015,.0018,.0014),3,n=12,r=7)
  base=[(sign*.006,-.026,.009),(sign*.010,-.033,.0095),(sign*.009,-.039,.012),(sign*.006,-.044,.015)];arms.tube(base,[.0017,.0016,.00135,.0012],1,n=10)
  for k in range(3):
   start=Vector(base[-1]);out=sign*(k-1)*.003
   pts=[start+Vector((out*t,-.009*t,.004*math.sin(t*pi*.8))) for t in [j/5 for j in range(6)]];arms.tube(pts,[.00085*(1-.62*j/5) for j in range(6)],1,n=8)
   end=pts[-1];ps=[end+Vector((sign*(.003+k*.001)*t+.002*math.sin(t*pi),-(.024+.004*k)*t,-.006*t+.003*math.sin(t*pi))) for t in [j/13 for j in range(14)]];arms.tube(ps,[.00035*(1-.85*j/13) for j in range(14)],2,n=6)
 # A closed pointed leaflike telson, a broad middle with narrowing terminal spear.
 vs=[(0,.026,.007),(-.0036,.033,.006),(-.0029,.038,.005),(0,.047,.004),(.0029,.038,.005),(.0036,.033,.006),(0,.034,.009),(0,.034,.003)];faces=[]
 for i in range(6):faces.extend([(6,i,(i+1)%6),(7,(i+1)%6,i)])
 tail.add(vs,faces,1)
 body.finish(c);head.finish(c);limbs.finish(c);arms.finish(c);tail.finish(c,False)

def septarian_concretion(c,m):
 rind=Mesh('rounded-concretion-rind-and-lower-body',m);host=Mesh('sectioned-host-rock-blocks-between-internal-veins',m);mineral=Mesh('volumetric-radial-and-concentric-mineral-cement',m)
 # Rounded nodule with a deliberately horizontal teaching section. The fill is real 3D volume.
 n=64;vs=[];fs=[];mi=[]
 # Exterior rises from a floor contact to the section lip; inner closed floor supports the section blocks.
 profiles=[(0,.009),(.005,.034),(.018,.059),(.040,.077),(.063,.085),(.084,.080),(.102,.070),(.102,.063),(.070,.062),(.065,.050)]
 for z,r in profiles:
  for k in range(n):a=2*pi*k/n;rr=r*(1+.023*math.cos(3*a+.4));vs.append((rr*math.cos(a),rr*.92*math.sin(a),z+.0008*math.sin(a*3)*(r/.085)))
 fs.append(tuple(reversed(range(n))));mi.append(0)
 for j in range(len(profiles)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(0 if j<7 else 1)
 fs.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(1);rind.add(vs,fs,mi)
 # Planar polygon tessellation: every cell and the connected veins extend 27mm below the exposed face.
 angles=[0,.68,1.51,2.39,3.21,4.12,5.17,2*pi];radii=[0,.024,.046,.0678]
 def wedge(a,b,r0,r1,target,mat):
  steps=max(2,int((b-a)*22))
  def polar(r,t):
   q=r/.0678;rr=r*(1+.09*(1-q*.4)*math.sin(3*t+.7)+.047*math.cos(5*t-1));aa=t+.11*math.sin(q*pi)*math.sin(2*t+.3);return Vector((rr*math.cos(aa)+.002*(1-q),rr*.92*math.sin(aa)-.0015*(1-q),.102))
  outer=[polar(r1,a+(b-a)*k/steps) for k in range(steps+1)]
  inner=[polar(r0,b-(b-a)*k/steps) for k in range(steps+1)] if r0>.00001 else [polar(0,0)]
  poly=outer+inner;N=len(poly);verts=[tuple(p) for p in poly]+[tuple(Vector((p.x*.87,p.y*.87,.073))) for p in poly];faces=[tuple(range(N)),tuple(reversed(range(N,N*2)))]
  for j in range(N):faces.append((j,N+j,N+(j+1)%N,(j+1)%N))
  target.add(verts,faces,mat)
 # Continuous radial mineral strips get wider inward. Segmented ring bands cross them.
 for ring in range(3):
  r0,r1=radii[ring],radii[ring+1];ringw=.0014 if ring else 0
  if ring:
   for q in range(8):wedge(q*pi/4,(q+1)*pi/4,r0-ringw,r0+ringw,mineral,2)
  for i in range(len(angles)-1):
   a,b=angles[i],angles[i+1];width=.085 if ring==0 else (.040 if ring==1 else .014)
   wedge(a+width,b-width,r0+ringw if ring else .0026,r1-(.0014 if ring<2 else 0),host,1)
   wedge(a-width,a+width,r0+ringw if ring else 0,r1,mineral,2)
 mineral.tube([(0,0,.073),(0,0,.102)],[.0027,.0027],2,n=16)
 rind.finish(c,False);host.finish(c,False);mineral.finish(c,False)
def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'acrocyathus':[('corallite-wall','#B79E89'),('calyx-interior','#99816F'),('septal-crests','#D5BDA1')],'sawdonia':[('leafless-branching-axis','#77956A'),('directional-spines','#9AA679')],'leanchoilia':[('dorsal-cuticle','#9C876F'),('articulated-plates','#B19A7F'),('limbs-and-flagella','#BAA487'),('eyes','#49483D')],'septarian-concretion':[('weathered-concretion-rind','#958774'),('fine-host-rock','#AD9D83'),('internal-mineral-cement','#DCC493')]}
 mats=[make_material(name,color,roughness=.82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=hi[0]-lo[0] if slug in ['acrocyathus','septarian-concretion'] else (.078 if slug=='leanchoilia' else hi[2]-lo[2]);scale=cfg['nominal_scale']['meters']/extent
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
 if slug=='sawdonia':desc={'en':'Terrestrial or moist-shore Sawdonia-inspired teaching shoots: continuous natural forks, sparse directional spines and circinate hooked tips. Counts, color, scale and pose are artistic; not seawater vegetation.','zh':'陆生或湿润岸边Sawdonia启发教学刺轴：自然连续分叉、稀疏有方向的刺及钩曲顶端。数量、配色、尺度与姿态属美术选择，不作海水植被。'}
 if slug=='septarian-concretion':desc={'en':'Rounded concretion teaching section with volumetric radial and crossing concentric mineral-filled fractures extending into the host rock. Cut surface is an intentional display choice, not an in-situ fracture or named paleolocality.','zh':'圆状结核教学切面，放射及环向交叉矿物充填裂隙具有进入围岩的真实厚度。切面是展示选择，不声称原地自然断裂或具体古地点。'}
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
