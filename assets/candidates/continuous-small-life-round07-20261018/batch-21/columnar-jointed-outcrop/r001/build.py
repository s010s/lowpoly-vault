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

def montsechia(c,m):
 stems=Mesh('rootless-flexible-forking-shoots',m);leaves=Mesh('small-simple-opposite-and-spiral-leaf-tabs',m);fruits=Mesh('paired-terminal-ovoid-fruits',m)
 # One gently inclined rootless shoot with a few flexible forks, no inferred holdfast.
 main=smooth_path([(-.032,0,.004),(-.015,.002,.042),(.003,-.001,.078),(.024,.005,.126)],34)
 stems.tube(main,[.00155*(1-i/33)+.0006*(i/33) for i in range(34)],0,n=9)
 branches=[main]
 for idx,sign in [(9,-1),(17,1),(23,-1)]:
  origin=main[idx];path=smooth_path([origin,origin+Vector((sign*.014,.004,.013)),origin+Vector((sign*.030,-.003,.028)),origin+Vector((sign*.038,.003,.046))],18);stems.tube(path,[.00105*(1-i/17)+.00042*(i/17) for i in range(18)],0,n=8);branches.append(path)
 for bi,path in enumerate(branches):
  for idx in range(4,len(path)-2,3):
   pos=path[idx];tangent=(path[idx+1]-path[idx-1]).normalized();a=idx*.93+bi*.60
   for sign in [-1,1]:
    d=Vector((sign*math.cos(a),sign*math.sin(a),.18)).normalized();L=(.0068 if bi==0 else .0050)*(1-.18*idx/len(path));leaf_blade(leaves,pos,d,L,.00165,.0010,1)
  tip=path[-1];tangent=(path[-1]-path[-3]).normalized();side=tangent.cross(Vector((0,1,0))).normalized()
  for sign in [-1,1]:
   center=tip+side*(sign*.0025)+tangent*.0025;stems.tube([tip,center-tangent*.001],[.00045,.00035],0,n=7);fruits.ellipsoid(center,(.0018,.00155,.0032),2,n=10,r=7)
 stems.finish(c);leaves.finish(c,False);fruits.finish(c)

def dollocaris(c,m):
 shell=Mesh('deep-enclosing-bivalved-carapace',m);head=Mesh('ventral-cephalic-body-and-seated-eye-bases',m);eyes=Mesh('two-enlarged-anterior-eyes-seated-at-carapace',m);arms=Mesh('exactly-three-pairs-of-grasping-cephalic-appendages',m);posterior=Mesh('short-posterior-ventral-appendage-fringe',m)
 shell.ellipsoid((0,.003,.045),(.029,.050,.034),0,n=28,r=15)
 # Subtle sagittal valve junction, no fabricated intricate surface ornament.
 p=smooth_path([(0,-.043,.060),(0,-.020,.0775),(0,.013,.078),(0,.043,.061)],22);shell.tube(p,[.00065]*22,1,n=6)
 head.ellipsoid((0,-.024,.023),(.019,.025,.012),1,n=18,r=9)
 for sign in [-1,1]:
  head.ellipsoid((sign*.014,-.038,.049),(.011,.012,.013),0,n=14,r=9)
  eyes.ellipsoid((sign*.015,-.046,.051),(.0105,.0110,.0107),2,n=18,r=11)
  for j in range(3):
   base=Vector((sign*(.010+.001*j),-.030+.010*j,.024));elbow=base+Vector((sign*(.014+.003*j),-.014,-.011));wrist=elbow+Vector((sign*.001,-(.027-.005*j),-.006));tip=wrist+Vector((-sign*.006,-.008,.010))
   ps=smooth_path([base,elbow,wrist,tip],22);arms.tube(ps,[.0031*(1-i/21)+.0006*(i/21) for i in range(22)],3,n=9)
   # Quiet opposed terminal finger establishes a grasping end without an action scene.
   q=smooth_path([ps[14],ps[14]+Vector((-sign*.004,-.004,-.004)),tip+Vector((sign*.001,.003,-.004))],9);arms.tube(q,[.00115*(1-i/8)+.00025*(i/8) for i in range(9)],3,n=7)
  for j in range(5):
   y=.005+j*.008;ps=smooth_path([(sign*.018,y,.024),(sign*.024,y+.003,.014),(sign*.026,y+.008,.013)],8);posterior.tube(ps,[.0014*(1-i/7)+.00035*(i/7) for i in range(8)],1,n=6)
 shell.finish(c);head.finish(c);eyes.finish(c);arms.finish(c);posterior.finish(c)

def ellipse_loft(mesh,sections,n=18,mat=0):
 # Axial Y loft. All rings have positive finite radii and outward winding.
 v=[];f=[]
 for x,y,z,rx,rz in sections:
  for k in range(n):a=2*pi*k/n;v.append((x+rx*math.cos(a),y,z+rz*math.sin(a)))
 f.append(tuple(range(n)))
 for j in range(len(sections)-1):
  for k in range(n):f.append(tuple(reversed((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))))
 f.append(tuple(reversed(tuple((len(sections)-1)*n+k for k in range(n)))));mesh.add(v,f,mat)

def coelurosauravus(c,m):
 body=Mesh('continuous-small-reptile-head-trunk-and-long-tapering-tail',m);legs=Mesh('four-limbs-distinct-from-lateral-membrane-rods',m);mem=Mesh('paired-lateral-gliding-membranes-not-hand-wings',m);rods=Mesh('independent-non-rib-lateral-membrane-support-rods',m);eyes=Mesh('small-seated-reptile-eyes',m)
 # A single continuous silhouette from snout through neck, flat torso and long tail.
 controls=[(-.072,.012,.006,.004),(-.060,.014,.011,.007),(-.048,.014,.010,.007),(-.035,.013,.006,.005),(-.015,.013,.013,.007),(.015,.013,.014,.007),(.036,.012,.010,.006),(.053,.011,.006,.004),(.083,.010,.0034,.0026),(.125,.010,.0018,.0014),(.164,.012,.0005,.00055)]
 sections=[]
 for j in range(len(controls)-1):
  for k in range(4):
   t=k/4;u=controls[j];v=controls[j+1];y=u[0]*(1-t)+v[0]*t;z=u[1]*(1-t)+v[1]*t;rx=u[2]*(1-t)+v[2]*t;rz=u[3]*(1-t)+v[3]*t;x=.003*math.sin((y+.07)*14)*(max(0,y)/.16);sections.append((x,y,z,rx,rz))
 y,z,rx,rz=controls[-1];sections.append((.003*math.sin((y+.07)*14),y,z,rx,rz));ellipse_loft(body,sections,20,0)
 for sign in [-1,1]:
  eyes.ellipsoid((sign*.009,-.056,.019),(.0021,.0027,.0018),3,n=10,r=6)
  for fore in [True,False]:
   y=-.027 if fore else .034;base=Vector((sign*.008,y,.012));elbow=Vector((sign*.023,y+(-.016 if fore else .016),.006));wrist=Vector((sign*.032,y+(-.033 if fore else .035),.003));ps=smooth_path([base,elbow,wrist],14);legs.tube(ps,[.0040*(1-i/13)+.0015*(i/13) for i in range(14)],0,n=9)
   for digit in range(3):
    ps=smooth_path([wrist,wrist+Vector((sign*.003,(digit-1)*.002,.0002)),wrist+Vector((sign*.007,(digit-1)*.003,-.0008))],6);legs.tube(ps,[.00075*(1-i/5)+.00022*(i/5) for i in range(6)],0,n=6)
  # Separate fan of rods rooted in the lateral trunk skin, not fingers or extended ribs.
  inners=[];outers=[]
  for j in range(11):
   t=j/10;yi=-.025+.058*t;yo=-.053+.115*t;span=.021+.053*math.sin(pi*t)**.65;inner=Vector((sign*.009,yi,.014));outer=Vector((sign*span,yo,.011+.003*math.sin(pi*t)));inners.append(inner);outers.append(outer)
   ps=smooth_path([inner,(inner+outer)*.5+Vector((0,0,.002)),outer],10);rods.tube(ps,[.0009*(1-i/9)+.00038*(i/9) for i in range(10)],2,n=6)
  # Closed thin curved membrane strip with readable scalloped fan margin.
  v=[]
  for bottom in [False,True]:
   for j in range(11):
    for k in range(5):
     u=k/4;p=inners[j]*(1-u)+outers[j]*u;p.z+=.0018*math.sin(pi*u)-(.0005 if bottom else 0);v.append(tuple(p))
  f=[];off=55
  for j in range(10):
   for k in range(4):a=j*5+k;q=(a,a+1,a+6,a+5);f.append(q if sign>0 else tuple(reversed(q)));f.append(tuple(off+i for i in (tuple(reversed(q)) if sign>0 else q)))
  boundary=list(range(5))+[j*5+4 for j in range(1,11)]+[50+k for k in range(3,-1,-1)]+[j*5 for j in range(9,0,-1)]
  for k,a in enumerate(boundary):b=boundary[(k+1)%len(boundary)];q=(a,off+a,off+b,b);f.append(q if sign>0 else tuple(reversed(q)))
  mem.add(v,f,1)
 body.finish(c);legs.finish(c);mem.finish(c);rods.finish(c);eyes.finish(c)

def columnar_jointed_outcrop(c,m):
 columns=Mesh('tightly-interlocking-polygonal-columns-with-stepped-broken-ends',m);base=Mesh('continuous-low-rock-mass-under-column-joints',m)
 # Deterministic original irregular polygonal cells, tightly adjoining rather than a crystal array.
 rng=random.Random(2026101818);seeds=[]
 for r in range(-2,3):
  for q in range(-2,3):
   if abs(q+r)<=2:seeds.append(Vector((.155*(q+r*.5)+rng.uniform(-.012,.012),.137*r+rng.uniform(-.010,.010))))
 boundary=[(-.42,-.22),(-.31,-.32),(.29,-.32),(.42,-.22),(.42,.22),(.30,.32),(-.30,.32),(-.42,.22)]
 def clip(poly,n,d):
  out=[]
  for j,a in enumerate(poly):
   b=poly[(j+1)%len(poly)];da=a.dot(n)-d;db=b.dot(n)-d
   if da<=0:out.append(a)
   if (da<=0)!=(db<=0):out.append(a+(b-a)*(da/(da-db)))
  return out
 for idx,p in enumerate(seeds):
  poly=[Vector(v) for v in boundary]
  for j,b in enumerate(seeds):
   if j!=idx:poly=clip(poly,b-p,(b.dot(b)-p.dot(p))*.5)
  if len(poly)<3:continue
  center=sum(poly,Vector((0,0)))/len(poly);poly=[center+(v-center)*.994 for v in poly];h=.17+.20*math.exp(-((p.x-.07)**2/.075+(p.y-.02)**2/.055))+rng.uniform(-.045,.038);h=max(.13,h);n=len(poly);v=[]
  for level in range(3):
   for k,x in enumerate(poly):
    pt=x if level<2 else center+(x-center)*.955;z=.025 if level==0 else h-.008 if level==1 else h+.007*(x.x-center.x)/.10+.004*math.sin(idx*.8+k)
    v.append((pt.x,pt.y,z))
  f=[tuple(reversed(range(n)))]
  for level in range(2):
   for k in range(n):f.append((level*n+k,level*n+(k+1)%n,(level+1)*n+(k+1)%n,(level+1)*n+k))
  ctr=len(v);v.append((center.x,center.y,h+.001))
  for k in range(n):f.append((ctr,2*n+k,2*n+(k+1)%n))
  columns.add(v,f,idx%3)
 n=len(boundary);v=[(x,y,z) for z in [0,.045] for x,y in boundary];f=[tuple(reversed(range(n))),tuple(n+k for k in range(n))]
 for k in range(n):f.append((k,(k+1)%n,n+(k+1)%n,n+k))
 base.add(v,f,1);columns.finish(c,False);base.finish(c,False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'montsechia': [('fine-flexible-shoots', '#7F926A'), ('small-simple-leaves', '#8A9D72'), ('paired-terminal-fruits', '#9A9B70')], 'dollocaris': [('deep-hood-carapace', '#8A9A91'), ('ventral-body-and-short-appendages', '#738073'), ('large-seated-eyes', '#394A43'), ('grasping-appendages', '#A5AE91')], 'coelurosauravus': [('soft-reptile-body', '#8E9C7B'), ('lateral-gliding-membrane', '#B3AB87'), ('separate-support-rods', '#A29770'), ('small-seated-eyes', '#3D4B3B')], 'columnar-jointed-outcrop': [('stone-grey', '#8B9188'), ('stone-mid', '#858B83'), ('stone-light', '#95998E')]}
 mats=[make_material(name,color,roughness=.82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=max(hi[i]-lo[i] for i in range(3)) if slug=='montsechia' else (.100 if slug=='dollocaris' else .236 if slug=='coelurosauravus' else hi[0]-lo[0]);scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'montsechia': {'en': 'Freshwater Montsechia-inspired rootless flexible branching shoots with small simple leaves and paired terminal ovoid fruits. Restores the same deferred ID once; no unsupported roots, large flowers, microscopic fruit veins or exact branch counts.', 'zh': '淡水Montsechia启发无根柔韧分叉枝，具小简单叶与成对末端卵形果；仅恢复同一延后ID，不添无依据根、大花、微细果脉或精确枝数。'}, 'dollocaris': {'en': 'Dollocaris-inspired deep enclosing bivalved carapace, two enlarged anterior eyes seated into cephalic bases and exactly three paired grasping cephalic limbs, with a restrained short posterior appendage fringe. Static teaching form, no predation demonstration or microscopic compound-eye claim.', 'zh': 'Dollocaris启发深罩双瓣甲，两枚大前眼嵌入头部眼基，三对捕捉头足自然接入整体头部，壳后腹缘短肢省简。静态教学造型，无捕食演示或微观复眼复原。'}, 'coelurosauravus': {'en': 'Coelurosauravus-inspired small flat reptile with continuous long tail, four distinct limbs and paired lateral membranes supported by separate non-rib rods. Support origin, exact rod count, color and static pose are artistic/uncertain; not bird wings, bat hand-wings or an animated gliding-mechanism reconstruction. Nominal nose-to-tail length excludes membrane span.', 'zh': 'Coelurosauravus启发小型扁伏爬行动物，身体长尾自然连续，四肢与侧方独立骨杆支撑膜可区分；支撑来源、精确杆数、配色及静态姿势属艺术或不确定范围，非鸟翼/蝙蝠手翼，不复原滑翔动画机制。名义吻尾长不计膜展宽。'}, 'columnar-jointed-outcrop': {'en': 'Original columnar-jointing teaching outcrop: tightly adjoining irregular polygonal rock columns rooted in a continuous low rock mass, with uneven stepped broken ends. Cooling-contraction form concept, not a large-gap crystal cluster, precise locality, basalt-only claim or measured column diameter.', 'zh': '原创柱状节理教学岩体：紧接的不规则多边岩柱接入连续低岩体，不齐断端形成台阶。冷却收缩形态概念，非大空隙晶簇，不指定地点、只限玄武岩或实测柱径。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
