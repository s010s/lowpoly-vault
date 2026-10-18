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

def flabellum(c,m):
 cup=Mesh('laterally-compressed-fan-wedge-with-blade-opening',m);septa=Mesh('restrained-interior-septal-blades',m);n=64;vs=[];fs=[];mi=[];profiles=[]
 for j in range(19):
  t=j/18;profiles.append((t,.0018+.046*t**.68,.0015+.0088*math.sin(t*pi/2)**.72,.003+.087*t,0))
 for rx,ry,z in [(.046,.0094,.089),(.043,.0084,.085),(.035,.0069,.076),(.025,.0049,.065),(.012,.0027,.055),(.0035,.0016,.052)]:profiles.append((1,rx,ry,z,1))
 for t,rx,ry,z,inside in profiles:
  for k in range(n):
   a=2*pi*k/n;rib=.00032*math.cos(a*20)*t if not inside else 0;vs.append(((rx+rib)*math.cos(a)+.002*math.sin(t*pi),(ry+rib*.25)*math.sin(a),z-.010*abs(math.cos(a))**1.8*t))
 cap=len(vs);vs.append((0,0,.003))
 for k in range(n):fs.append((cap,(k+1)%n,k));mi.append(0)
 for j in range(len(profiles)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(profiles[j+1][4])
 fs.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(1);cup.add(vs,fs,mi)
 for k in range(24):
  a=2*pi*k/24;u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0));sv=[];sf=[]
  for j,t in enumerate([0,.20,.45,.70,.90,1]):
   rx=.0035+.040*t;ry=.0016+.0067*t;z=.042+.043*t-.008*abs(math.cos(a))**1.8;ctr=Vector((rx*math.cos(a),ry*math.sin(a),z));w=.00025+.00013*t;h=.00055+.0018*math.sin(pi*t)
   sv.extend([tuple(ctr-v*w),tuple(ctr+v*w),tuple(ctr+Vector((0,0,h)))])
  sf.append((2,1,0))
  for j in range(5):
   for e in range(3):sf.append((j*3+e,j*3+(e+1)%3,(j+1)*3+(e+1)%3,(j+1)*3+e))
  sf.append((15,16,17));septa.add(sv,sf,2)
 cup.finish(c);septa.finish(c)

def horneophyton(c,m):
 from asset_common import link_object
 corms=Mesh('readable-swollen-corm-like-bases',m)
 specs=[((0,0,0),1.0,.10),((-.025,.012,0),.80,-.65),((.025,.014,0),.72,.75)]
 for idx,(offset,scale,angle) in enumerate(specs):
  off=Vector(offset);corms.ellipsoid(tuple(off+Vector((0,0,.010*scale))),(.012*scale,.0095*scale,.010*scale),1,n=20,r=10)
  vertices=[(0,0,.010),(0,0,.028),(.002,.001,.064),(-.010,.001,.086),(.014,.003,.091),(-.017,.001,.109),(.021,.004,.112),(-.025,.005,.126),(-.009,-.003,.129),(.015,.011,.132),(.030,-.001,.130),(-.026,.006,.139),(-.008,-.003,.140),(.015,.012,.143),(.031,-.001,.142)]
  edges=[(0,1),(1,2),(2,3),(2,4),(3,5),(4,6),(5,7),(5,8),(6,9),(6,10),(7,11),(8,12),(9,13),(10,14)]
  radii=[.0065,.0030,.0027,.0025,.0024,.0036,.0035,.0044,.0041,.0042,.0039,.0015,.0014,.0015,.0014]
  v=[]
  for p in vertices:
   x,y,z=p;v.append(tuple(off+Vector(((x*math.cos(angle)-y*math.sin(angle))*scale,(x*math.sin(angle)+y*math.cos(angle))*scale,z*scale))))
  mesh=bpy.data.meshes.new('continuous-forked-sporangial-axis-'+str(idx));mesh.from_pydata(v,edges,[]);mesh.update();o=bpy.data.objects.new('continuous-forked-sporangial-axis-'+str(idx),mesh);link_object(o,c);mesh.materials.append(m[0]);skin=o.modifiers.new('Editable continuous shoot skin','SKIN');skin.use_smooth_shade=True
  bpy.context.view_layer.update()
  for j,r in enumerate(radii):mesh.skin_vertices[0].data[j].radius=(r*scale,r*scale*.88)
  mesh.skin_vertices[0].data[0].use_root=True
  sub=o.modifiers.new('Soft continuous corm-to-axis and sporangial forks','SUBSURF');sub.levels=1;sub.render_levels=1
 corms.finish(c)

def wave_ripple_surface(c,m):
 surface=Mesh('bounded-shallow-block-with-symmetric-wave-ripples',m);nx=96;ny=24;vs=[];fs=[];mi=[]
 for j in range(ny+1):
  v=-1+2*j/ny
  for i in range(nx+1):
   u=-1+2*i/nx;x=.75*u*(1-.035*v**8);y=.58*v*(1-.025*u**8);phase=2*pi*(x/.205+.075*math.sin(x*2*pi/.83)+.09*math.sin(y*2*pi/1.25+.4*x));amp=.018*(.96+.04*math.cos(y*5));z=.043+amp*(.5+.5*math.cos(phase));vs.append((x,y,z))
 for j in range(ny):
  for i in range(nx):a=j*(nx+1)+i;fs.append((a,a+1,a+nx+2,a+nx+1));mi.append(0)
 top_faces=len(fs);boundary=[i for i in range(nx+1)]+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];bottom=[]
 for idx in boundary:bottom.append(len(vs));x,y,_=vs[idx];vs.append((x,y,0))
 for k,b in enumerate(boundary):q=(k+1)%len(boundary);fs.append((b,bottom[k],bottom[q],boundary[q]));mi.append(1)
 center=len(vs);vs.append((0,0,0))
 for k in range(len(bottom)):fs.append((center,bottom[(k+1)%len(bottom)],bottom[k]));mi.append(1)
 surface.add(vs,fs,mi);o=surface.finish(c,False)
 for p in o.data.polygons[:top_faces]:p.use_smooth=True

def gogia(c,m):
 base=Mesh('short-attachment-base-and-stalk',m);theca=Mesh('pear-shaped-continuous-plated-theca',m);crown=Mesh('thin-branching-feeding-brachioles',m)
 base.tube([(0,0,.001),(0,0,.004),(.001,0,.011),(.001,.001,.017)],[.0055,.0039,.0030,.0040],0,n=12)
 prof=[(.012,.0032),(.018,.0085),(.026,.0135),(.035,.0142),(.044,.0106),(.051,.0063),(.054,.0048)];n=12;vs=[];fs=[];mis=[]
 for j,(z,r) in enumerate(prof):
  for k in range(n):a=2*pi*k/n+.04*math.sin(j*1.4);vs.append((.001+r*math.cos(a),.001+r*.90*math.sin(a),z))
 cap=len(vs);vs.append((.001,.001,.012))
 for k in range(n):fs.append((cap,(k+1)%n,k));mis.append(0)
 for j in range(len(prof)-1):
  for k in range(n):
   ids=[j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k];points=[Vector(vs[i]) for i in ids];ctr=sum(points,Vector())/4;normal=Vector((ctr.x-.001,(ctr.y-.001)/.9,0)).normalized();inner=[]
   for p in points:inner.append(len(vs));vs.append(tuple(ctr+(p-ctr)*.88+normal*.00043))
   for e in range(4):fs.append((ids[e],ids[(e+1)%4],inner[(e+1)%4],inner[e]));mis.append(1)
   fs.append(tuple(inner));mis.append(0 if j<4 else 1)
 top=len(vs);vs.append((.001,.001,.054))
 for k in range(n):fs.append((top,(len(prof)-1)*n+k,(len(prof)-1)*n+(k+1)%n));mis.append(1)
 theca.add(vs,fs,mis)
 for k in range(7):
  a=2*pi*k/7+.10*math.sin(k*2);u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0));pts=[]
  length=.041+.008*math.sin(k*1.7)
  for j in range(12):
   t=j/11;p=Vector((.001,.001,.052))+u*(.003+.019*t**1.3)+v*(.003*math.sin(pi*t+k)*t)+Vector((0,0,length*(t-.13*t*t)));pts.append(p)
  crown.tube(pts,[.00085*(1-.64*j/11) for j in range(12)],2,n=8)
  if k%2==0:
   start=pts[7]
   for sign in [-1,1]:
    ps=[start+u*(.007*t)+v*(sign*.007*t**1.2)+Vector((0,0,.016*t-.002*t*t)) for t in [j/7 for j in range(8)]];crown.tube(ps,[.00052*(1-.55*j/7) for j in range(8)],2,n=8)
 base.finish(c);theca.finish(c,False);crown.finish(c)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'flabellum':[('fan-corallum','#C5AA9A'),('calyx-wall','#AD9284'),('septal-blades','#D4BAA6')],'horneophyton':[('leafless-axes-and-forked-sporangia','#71956B'),('swollen-corm-base','#918565')],'wave-ripple-surface':[('rippled-sediment','#BBA78C'),('bounded-cut-edge','#9F8C72')],'gogia':[('plated-theca','#BC9676'),('plate-junctions','#AE8769'),('feeding-brachioles','#C7AA88')]}
 mats=[make_material(name,color,roughness=.82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=hi[0]-lo[0] if slug=='wave-ripple-surface' else hi[2]-lo[2];scale=cfg['nominal_scale']['meters']/extent
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
 if slug=='horneophyton':desc={'en':'Terrestrial/wet-shore early-plant teaching concept with enlarged corm-like bases, leafless branching axes and continuous forked sporangia. Not marine vegetation; scale and palette are artistic.','zh':'陆生或湿润岸边早期植物教学概念，具膨大基体、无叶分叉轴及连续分枝孢子囊。不标为海水植被；尺度与配色属美术选择。'}
 if slug=='wave-ripple-surface':desc={'en':'Original bounded shallow surface patch with rounded symmetric wave-ripple relief and gently varying spacing. Sedimentary-process teaching concept, no named prehistoric locality or seamless-tiling claim.','zh':'原创浅厚度地表块，具圆钝对称波痕起伏及柔和变化的间距。沉积过程教学概念，不指定史前地点，不承诺任意无缝拼接。'}
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
