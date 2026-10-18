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

def leclercqia(c,m):
 stem=Mesh('slender-shoot-with-spirally-seated-leaf-bases',m);leaves=Mesh('divided-leaf-units-with-long-recurved-central-segments',m)
 def axis(z):return Vector((.004*math.sin(z*13),.002*math.sin(z*22),z))
 pts=[axis(.002+.163*i/25) for i in range(26)];stem.tube(pts,[.0043*(1-i/25)+.0015*(i/25) for i in range(26)],0,n=12)
 for idx in range(11):
  z=.027+.012*idx;a=idx*2.38+.30;u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0));origin=axis(z);sc=(.78+.24*math.sin(pi*idx/11))*(.78 if idx>8 else 1)
  base=[origin,origin+u*.006*sc+Vector((0,0,.002)),origin+u*.013*sc+Vector((0,0,.006))];flat_strap(leaves,base,[.0025*sc,.0030*sc,.0022*sc],.0005*sc,v,1)
  split=base[-1];ps=smooth_path([split,split+u*.010*sc+Vector((0,0,.006*sc)),split+u*.023*sc+Vector((0,0,.007*sc)),split+u*.029*sc+Vector((0,0,.001*sc)),split+u*.026*sc+Vector((0,0,-.004*sc))],12);flat_strap(leaves,ps,[.0021*sc*(1-j/11)+.0004*sc*(j/11) for j in range(12)],.00042*sc,v,1)
  pairs=2 if idx in [0,1,3,4,6,8] else 1
  for tier in range(pairs):
   for sign in [-1,1]:
    start=split-u*.003*sc+u*.005*tier*sc;d=(u*(.48+.17*tier)+v*sign*(.88-.18*tier)).normalized();L=(.015-.004*tier)*sc;ps=smooth_path([start,start+d*L*.55+Vector((0,0,.002*sc)),start+d*L+Vector((0,0,.001*sc))],7);flat_strap(leaves,ps,[.0017*sc*(1-j/6)+.00025*sc*(j/6) for j in range(7)],.00035*sc,v,1)
 stem.finish(c);leaves.finish(c)

def canadia(c,m):
 body=Mesh('continuous-dorsoventrally-flattened-segmented-worm',m);bristles=Mesh('overlapping-wide-leaflike-dorsal-chaetal-fans',m);bases=Mesh('paired-small-parapodial-chaeta-bases',m);feelers=Mesh('two-smooth-anterior-tentacles',m)
 n=20;vs=[];fs=[]
 for j in range(25):
  t=j/24;y=-.030+.060*t;rx=.0012+.0047*math.sin(pi*t)**.62;rz=.0010+.0021*math.sin(pi*t)**.65;cx=.0007*math.sin(t*pi*1.4)
  for k in range(n):a=2*pi*k/n;vs.append((cx+rx*math.cos(a),y,.0033+rz*math.sin(a)))
 fs.append(tuple(range(n)))
 for j in range(24):
  for k in range(n):fs.append(tuple(reversed((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))))
 fs.append(tuple(reversed(tuple(24*n+k for k in range(n)))));body.add(vs,fs,0)
 for j in range(10):
  y=-.023+j*.0049;t=(y+.030)/.060;w=.0012+.0047*math.sin(pi*t)**.62
  for sign in [-1,1]:
   bases.ellipsoid((sign*w*.87,y,.0025),(.0015,.0018,.0012),0,n=10,r=6)
   for rank in range(3):
    start=Vector((sign*(.0015+.0016*rank),y-.001,.0048-.00045*rank));d=Vector((sign*(.14+.32*rank),.98-.23*rank,0)).normalized();L=[.012,.010,.007][rank]*(.82+.18*math.sin(pi*t));width=[.0018,.00145,.0011][rank];leaf_blade(bristles,start,d,L,width,.0011 if rank==0 else .0006,1 if rank<2 else 2)
 for sign in [-1,1]:
  p=smooth_path([(sign*.0011,-.028,.0040),(sign*.0025,-.036,.0058),(sign*.006,-.046,.005),(sign*.007,-.049,.004)],16);feelers.tube(p,[.00055*(1-i/15)+.00012*(i/15) for i in range(16)],2,n=8)
 body.finish(c);bases.finish(c);bristles.finish(c,False);feelers.finish(c)

def salvinia(c,m):
 floats=Mesh('exactly-two-broad-floating-leaves',m);node=Mesh('short-node-and-floating-leaf-petioles',m);submerged=Mesh('one-dissected-submerged-leaf-NOT-ROOTS',m)
 water_z=.043;node.tube([(-.004,0,water_z),(.004,0,water_z)],[.0012,.0012],0,n=10)
 for sign in [-1,1]:
  center=Vector((sign*.0145,0,water_z));node.tube([(0,0,water_z),tuple(center)],[.0011,.0008],0,n=8);n=36;v=[];f=[]
  for bottom in [False,True]:
   v.append(tuple(center+Vector((0,0,-.0008 if bottom else .0016))))
   for k in range(n):
    a=2*pi*k/n;x=.014*math.cos(a);y=.019*math.sin(a);z=.0020+.0028*abs(math.cos(a))**1.6+.0007*math.sin(a*2)
    v.append(tuple(center+Vector((x,y,z-(.0008 if bottom else 0)))))
  off=n+1
  for k in range(n):q=(k+1)%n;f.extend([(0,k+1,q+1),(off,off+q+1,off+k+1),(k+1,off+k+1,off+q+1,q+1)])
  floats.add(v,f,1 if sign<0 else 2)
 # The descending organ is a single modified dissected leaf, not a true root system.
 axis=smooth_path([(0,0,water_z),(.001,.002,.033),(-.001,.003,.017),(.002,.004,.006)],18);submerged.tube(axis,[.0009*(1-i/17)+.00035*(i/17) for i in range(18)],3,n=8)
 for j in range(5):
  z=.034-j*.0053;start=Vector((.0005,.002,z))
  for sign in [-1,1]:
   L=.013*(1-.085*j);tip=start+Vector((sign*L,.002*math.sin(j),-.010-j*.0007));ps=smooth_path([start,start+Vector((sign*L*.55,.001,-.005)),tip],9);submerged.tube(ps,[.00055*(1-i/8)+.00012*(i/8) for i in range(9)],3,n=6)
   mid=ps[4];ps2=smooth_path([mid,mid+Vector((sign*.004,-.002,-.003)),mid+Vector((sign*.007,-.003,-.009))],7);submerged.tube(ps2,[.00030*(1-i/6)+.00008*(i/6) for i in range(7)],3,n=6)
 floats.finish(c);node.finish(c);submerged.finish(c)

def load_cast_bedding(c,m):
 nx=80;ny=14;points=[]
 def interface(x,y):
  centers=[(-.26+.014*math.sin(y*8),.090,.087),(-.015+.018*math.sin(y*6+.5),.097,.111),(.235+.012*math.sin(y*9+1),.080,.078)]
  depth=sum(d*math.exp(-((x-pos)/width)**2) for pos,width,d in centers);return .202+.007*math.sin(y*9+x*2)-depth
 for j in range(ny+1):
  y=-.16+.32*j/ny
  for i in range(nx+1):x=-.4+.8*i/nx;points.append((x,y,interface(x,y)))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 for upper in [False,True]:
  layer=Mesh('continuous-upper-sand-layer-with-downward-load-lobes' if upper else 'continuous-lower-soft-layer-around-load-lobes',m);v=list(points);f=[];mis=[];mat=0 if upper else 1
  for j in range(ny):
   for i in range(nx):a=j*(nx+1)+i;q=(a,a+1,a+nx+2,a+nx+1);f.append(tuple(reversed(q)) if upper else q);mis.append(mat)
  outer=[];height=.318 if upper else 0
  for idx in boundary:x,y,_=v[idx];outer.append(len(v));v.append((x,y,height))
  for k,a in enumerate(boundary):q=(k+1)%len(boundary);b=boundary[q];face=(a,b,outer[q],outer[k]);f.append(face if upper else tuple(reversed(face)));mis.append(mat)
  center=len(v);v.append((0,0,height))
  for k,a in enumerate(outer):q=outer[(k+1)%len(outer)];f.append((center,a,q) if upper else (center,q,a));mis.append(mat)
  layer.add(v,f,mis);o=layer.finish(c,False)
  # Buried interface normals are intentionally smooth; exposed teaching cuts remain flat.
  for p in o.data.polygons[:nx*ny]:p.use_smooth=True
def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'leclercqia':[('slender-lycopsid-shoot','#87916A'),('divided-microphylls','#789263')],'canadia':[('soft-worm-and-parapodia','#AA957B'),('wide-inner-chaetae','#C7AF86'),('outer-chaetae-and-tentacles','#BDA17E')],'salvinia':[('short-floating-node','#8E9B6D'),('first-floating-leaf','#789665'),('second-floating-leaf','#8BA371'),('dissected-SUBMERGED-LEAF','#8D9469')],'load-cast-bedding':[('continuous-upper-sand-layer','#BEA783'),('continuous-lower-soft-mud-layer','#9C9A8C')]}
 mats=[make_material(name,color,roughness=.82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=hi[2]-lo[2] if slug=='leclercqia' else (.060 if slug=='canadia' else hi[0]-lo[0]);scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'leclercqia':{'en':'Leclercqia-inspired divided-leaf shoot, naturally seated leaf bases and a few prominent split leaves with elongated recurved central tips; far leaves simplified. Terrestrial teaching plant, same recovered deferred ID, no species-level leaf-count or microvein restoration.','zh':'Leclercqia启发裂叶枝，叶基自然接茎，主要裂叶具较长回曲中央部，远侧叶简化。陆生教学植物，同一延后ID恢复，不作种级叶数或微细叶脉复原。'},'canadia':{'en':'Canadia-inspired flattened elongate annelid with grouped overlapping broad dorsal chaetae, widest/longest near the midline, and two smooth anterior tentacles. Fine chaetal teeth, gills and segment counts simplified, no fine-spike noise coat.','zh':'Canadia启发扁长环节动物，成组叠覆宽叶状背刚毛靠中线较长较宽，具两根光滑头须。微细锯齿、鳃和体节数量简化，不以细刺噪声覆盖。'},'salvinia':{'en':'Freshwater Salvinia-inspired node with exactly two broad floating leaves and one dissected descending submerged leaf. The lower root-like organ is a LEAF, not true roots. No marine label, microscopic leaf-hair or exact species claim.','zh':'淡水Salvinia启发叶节，具有两片宽浮叶和一片下垂分叉沉水叶。下方根状器官是叶，不是真根。不作海水植物、微观叶毛或精确种复原。'},'load-cast-bedding':{'en':'Load-cast teaching section: two continuous sediment layers, with rounded upper-layer lobes extending downward into the lower soft layer. Intentional cut face, original process geometry, no separate balls, exact strata, earthquake trigger or real-time deformation claim.','zh':'负载构造教学切面：两层连续沉积岩体，上层圆鼓叶瓣向下伸入较软下层。有意教学露面和原创过程几何，不堆离散球，不指定古地层、地震触发或实时变形。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
