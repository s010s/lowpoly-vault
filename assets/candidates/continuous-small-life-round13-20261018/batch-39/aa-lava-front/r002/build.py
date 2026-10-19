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

def clavagella(c,m):
 shell=Mesh('continuous-preserved-adventitious-calcareous-tube-with-incorporated-small-valve-region',m);N=64;R=48;v=[];f=[];mi=[]
 def section(t):
  y=-.075+.160*t;radius=.003+.020*math.exp(-((t-.22)/.22)**2)+.0035*t;z=.021+.014*t**1.4;x=.003*math.sin(t*pi*1.5);return x,y,z,radius
 for j in range(R):
  t=j/(R-1);x,y,z,r=section(t)
  for k in range(N):
   a=2*pi*k/N;d=((a-pi/2+pi)%(2*pi))-pi;valve=math.exp(-((t-.24)/.115)**4-(d/.60)**4);rib=.00055*math.cos((t-.24)*160)*valve;rr=r*(1+.035*math.cos(3*a+.7*t))+.0012*valve+rib;v.append((x+rr*math.cos(a),y,z+rr*.82*math.sin(a)))
 center=len(v);x,y,z,r=section(0);v.append((x,y,z))
 for k in range(N):f.append((center,(k+1)%N,k));mi.append(0)
 for j in range(R-1):
  t=(j+.5)/(R-1)
  for k in range(N):
   a=2*pi*(k+.5)/N;d=((a-pi/2+pi)%(2*pi))-pi;f.append(tuple(reversed((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))));mi.append(1 if ((t-.24)/.115)**2+(d/.60)**2<1 else 0)
 # Real solid rim and a bounded internal neck lumen; no unknown siphon soft parts.
 base=(R-1)*N
 for j in range(17):
  t=1-.38*j/16;x,y,z,r=section(t)
  for k in range(N):a=2*pi*k/N;v.append((x+r*.67*math.cos(a),y,z+r*.82*.67*math.sin(a)))
 for k in range(N):f.append((base+k,base+N+k,base+N+(k+1)%N,base+(k+1)%N));mi.append(0)
 for j in range(16):
  for k in range(N):a=(R*N+1)+j*N+k;b=(R*N+1)+j*N+(k+1)%N;f.append(tuple(reversed((a,b,b+N,a+N))));mi.append(2)
 inner=(R*N+1)+16*N;x,y,z,r=section(.62);cap=len(v);v.append((x,y,z))
 for k in range(N):f.append((cap,inner+k,inner+(k+1)%N));mi.append(2)
 # Rebuild exact rim faces explicitly to avoid any implied contiguous-ring offset at the basal center.
 rim_start=N+(R-1)*N
 for k in range(N):f[rim_start+k]=(base+k,R*N+1+k,R*N+1+(k+1)%N,base+(k+1)%N)
 shell.add(v,f,mi);shell.finish(c)

def aa_lava_front(c,m):
 body=Mesh('irregular-sloping-continuous-lava-core-rounded-rubble-bearing-front-no-plinth',m);clasts=Mesh('unequal-angular-clinker-embedded-in-sloping-core-and-irregular-toe',m);N=56;v=[];f=[]
 def h(x,y):
  rho=(abs(x/.55)**3+abs((y-.04)/.40)**3)**(1/3)
  return (.125+.135*(y+.50)+.019*math.cos(x*5+y*2))*max(0,1-max(0,(rho-.64)/.40))
 def outline(a,t):
  r=1+.085*math.sin(5*a+.4)+.042*math.cos(7*a-.3)
  return (.55*math.copysign(abs(math.cos(a))**.70,math.cos(a))*r*t,.40*math.copysign(abs(math.sin(a))**.70,math.sin(a))*r*t+.04)
 # Grounded irregular footprint and outward rolled toe; no rectangular cut slab or vertical plate sides.
 for row,t in enumerate([.91,.86,.74,.55,.27]):
  for k in range(N):
   a=2*pi*k/N;x,y=outline(a,t)
   if row==0:z=0
   elif row==1:z=max(.024,h(x,y)*(.78+.20*math.sin(3*a+.4)))
   elif row==2:z=h(x,y)
   else:z=h(x,y)
   v.append((x,y,z))
 bot=len(v);v.append((0,0,0));top=len(v);v.append((0,.01,h(0,.01)))
 for k in range(N):f.append((bot,(k+1)%N,k));f.append((4*N+k,4*N+(k+1)%N,top))
 for row in range(4):
  for k in range(N):f.append((row*N+k,row*N+(k+1)%N,(row+1)*N+(k+1)%N,(row+1)*N+k))
 body.add(v,f);body.finish(c,False)
 specs=[(-.40,.25,.19,.15,.16),(-.06,.31,.22,.16,.18),(.32,.26,.20,.18,.17),(-.48,.02,.13,.13,.16),(-.22,.03,.20,.17,.21),(.14,.05,.21,.17,.24),(.45,.02,.15,.15,.16),(-.40,-.22,.20,.14,.18),(-.04,-.22,.20,.15,.16),(.30,-.21,.22,.16,.20),(-.52,-.36,.09,.08,.09),(-.25,-.37,.13,.09,.12),(.10,-.37,.12,.09,.10),(.46,-.35,.10,.09,.11),(-.31,.17,.10,.09,.11),(.15,.25,.09,.10,.13),(-.10,-.05,.10,.08,.12),(.37,-.06,.09,.08,.13),(-.56,.25,.07,.09,.08),(.52,.23,.08,.08,.10),(-.18,-.30,.07,.08,.10),(.23,-.35,.08,.06,.09)]
 specs += [(-.40,-.46,.11,.09,.10),(-.14,-.50,.09,.075,.08),(.17,-.48,.13,.085,.11),(.40,-.43,.085,.07,.085)]
 for j,(x,y,rx,ry,hh) in enumerate(specs):
  n=6+j%3;vv=[];ff=[];a0=.43*j;z0=max(0,h(x,y)-.035)
  for row,(s,z) in enumerate([(1,0),(1.06,.43),(.70,1)]):
   for k in range(n):a=a0+2*pi*k/n;rr=s*(1+.12*math.sin(k*2.3+j));vv.append((x+rx*rr*math.cos(a)+.025*z*math.sin(j),y+ry*rr*math.sin(a)-.035*z,z0+hh*z+.018*math.sin(k*1.7+j)*z))
  b=len(vv);vv.extend([(x,y,z0),(x+.012*math.cos(j),y-.016,z0+hh*1.06)])
  for k in range(n):ff.append((b,(k+1)%n,k));ff.append((b+1,2*n+k,2*n+(k+1)%n))
  for row in range(2):
   for k in range(n):ff.append((row*n+k,row*n+(k+1)%n,(row+1)*n+(k+1)%n,(row+1)*n+k))
  clasts.add(vv,ff,1 if j in [0,4,6,11,18] else 0)
 clasts.finish(c,False)

def native_copper_dendrite(c,m):
 crystal=Mesh('original-planar-coalescent-copper-dendritic-sheets-with-unequal-flat-terminal-growth',m)
 def branch(points,w0,w1,mat=0):
  pts=smooth_path([(x,y,.004+.0009*math.sin(i)) for i,(x,y) in enumerate(points)],14);flat_strap(crystal,pts,[w0*(1-i/13)+w1*i/13 for i in range(14)],.0026,(1,0,0),mat,n=6)
  p=Vector(pts[-1]);d=(p-Vector(pts[-3])).normalized();lat=Vector((-d.y,d.x,0));outline=[p-d*.007-lat*w1*.5,p-d*.003+lat*w1*1.30,p+d*.004+lat*w1*1.14,p+d*.008+lat*w1*.26,p+d*.005-lat*w1*.96,p-d*.002-lat*w1*1.10];vv=[tuple(q+Vector((0,0,z))) for z in [-.0022,.0022] for q in outline];n=len(outline);ff=[tuple(reversed(range(n))),tuple(n+k for k in range(n))]
  for k in range(n):ff.append((k,(k+1)%n,n+(k+1)%n,n+k))
  crystal.add(vv,ff,mat)
 branch([(-.043,-.062),(-.014,-.024),(.005,.014),(.028,.058)],.008,.0035)
 branch([(-.024,-.038),(-.049,-.018),(-.067,.011),(-.063,.035)],.0062,.0038)
 branch([(-.012,-.020),(.019,-.028),(.051,-.017),(.071,.009)],.0065,.0048,1)
 branch([(-.001,.005),(-.027,.020),(-.037,.051),(-.051,.069)],.0055,.0042)
 branch([(.010,.022),(.041,.023),(.061,.049)],.005,.004)
 branch([(-.051,.002),(-.077,-.006),(-.086,.008)],.0042,.0034,1)
 branch([(.039,-.023),(.047,-.046),(.066,-.054)],.0048,.0038)
 branch([(-.030,.036),(-.009,.040),(-.002,.063)],.0044,.0032,1)
 branch([(.030,.032),(.033,.078)],.0039,.003)
 crystal.finish(c,False)

def nereites_lobed_meander(c,m):
 # One raised fossil relief, not a living organism or a painted path.
 N=56;host=Mesh('illustrative-sediment-host-for-positive-fossil-relief',m);v=[];f=[]
 for z in [0,.012]:
  for k in range(N):a=2*pi*k/N;v.append((.15*math.copysign(abs(math.cos(a))**.30,math.cos(a)),.115*math.copysign(abs(math.sin(a))**.30,math.sin(a)),z))
 v.extend([(0,0,0),(0,0,.012)])
 for k in range(N):f.extend([(2*N,(k+1)%N,k),(2*N+1,N+k,N+(k+1)%N),(k,(k+1)%N,N+(k+1)%N,N+k)])
 host.add(v,f);host.finish(c,False);trace=Mesh('raised-meandering-backfilled-axis-with-alternating-overlapping-lateral-lobes',m)
 def p(t):return Vector((-.122+.244*t,.054*math.sin(t*pi*2.25-.35),.014))
 pts=[p(i/95) for i in range(96)];trace.tube(pts,[.0023]*96,n=10)
 for j in range(54):
  t=.025+.95*j/53;q=p(t);d=(p(min(1,t+.005))-p(max(0,t-.005))).normalized();side=1 if j%2 else -1;normal=Vector((-d.y,d.x,0))*side;length=.012+.002*math.sin(j*.47);path=[q-d*.001,q+normal*length*.50-d*.002,q+normal*length-d*.005,q+normal*length*.92-d*.011];path=[Vector((v.x,v.y,.0135)) for v in smooth_path(path,8)];flat_strap(trace,path,[.0015+.0045*math.sin(pi*i/7)**.62 for i in range(8)],.0019,d,0,n=8)
 trace.finish(c)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'clavagella': [('preserved-adventitious-calcium-tube', '#B9AE96'), ('continuously-incorporated-valve-region', '#C7BDA5'), ('bounded-inner-neck-wall', '#948F7B')], 'aa-lava-front': [('coherent-lava-and-most-clinker', '#605F59'), ('quiet-cool-clinker-faces', '#74716A')], 'native-copper-dendrite': [('original-muted-native-copper', '#9C6651'), ('restrained-terminal-copper', '#AE775B')], 'nereites-lobed-meander': [('sediment-and-raised-fossil-relief', '#B3AA94')]}
 mats=[make_material(name,color,roughness=(.43 if slug=='native-copper-dendrite' else .86),metallic=(.65 if slug=='native-copper-dendrite' else 0)) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=(hi[1]-lo[1]) if slug=='clavagella' else hi[0]-lo[0];scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'clavagella': {'en': 'Preserved Clavagella-inspired shell/adventitious calcareous tube specimen only: irregular bulbous enclosure incorporates a small valve region continuously into its wall, narrowing naturally into a long neck with actual solid rim and bounded lumen. No ordinary bottle plus stuck-on shell, living posture, unknown siphon soft tissues or exact species/count/size restoration.', 'zh': '仅保存Clavagella启发壳/附加钙质管标本：不规则膨大包被管壁连续融入小壳瓣区，自然收窄为有真实实壁口缘和有限管腔的长颈。非瓶子贴贝壳，不补生活姿态、未知虹吸软体或精确种/数量/尺度复原。'}, 'aa-lava-front': {'en': 'Original nominal1.2m Aa lava-front representative landscape patch: a coherent solid flow body carries unequal angular clinker masses embedded and piled with visible weight across its front. Quiet structural palette, no equal loose stone scatter, noisy ropy-lava conversion, sharp pillow variant, flame/smoke/flow simulation or named eruption/site.', 'zh': '原创名义1.2米Aa熔岩前缘landscape片：连续实质流体基体承托不等大棱角渣块，前缘嵌入堆覆有重量关系。克制结构配色，非等大散石、绳熔岩加噪声或枕状锐化变体，无火烟流动模拟或具名喷发地点。'}, 'native-copper-dendrite': {'en': 'Original native-copper-inspired dendritic crystal aggregate with unequal continuous flattened branching sheets and blunt irregular flared terminal growth, deliberate coalescent junctions and restrained metal response. Gray shape carries identity; not an old sponge/tree recolor or industrial wire. Nominal15cm span, palette and flat display contact at lower crystal surface are artistic, no measured mineral locality/specimen.', 'zh': '原创自然铜启发枝晶：不等粗连续扁平分枝片、钝不规则外展端部与有意共生融合接点，金属响应克制；灰色结构可识别，非旧海绵树枝换色或工业导线。名义15厘米、配色及下表面平放接触属美术选择，不作实测矿点标本。'}, 'nereites-lobed-meander': {'en': 'Original interpretive raised-fossil-relief Nereites-inspired trace: meandering median backfilled axis with genuinely raised, alternating/slightly offset, partially overlapping ovate lateral lobes on one sediment host. Gray top and oblique carry internal relief; no painted black curve, dense Cruziana variant, known producer species or extra asset counts for synonym names.', 'zh': '原创示意Nereites启发凸浮雕化石迹：曲行中轴回填管及真实隆起、交替略错列且部分重叠的卵形侧叶瓣，置连续沉积宿主。灰顶斜视读内部起伏，非黑曲线、Cruziana加密变体，不指定制造物种或将同义名另计资产。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r002','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'reference_status':'basic-form textual reference support with explicit limits; not strict reconstruction','publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
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
