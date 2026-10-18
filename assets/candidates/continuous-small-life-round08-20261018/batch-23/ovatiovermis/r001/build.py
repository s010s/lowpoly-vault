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

def metasequoia(c,m):
 twig=Mesh('preserved-cut-branch-organ-with-opposite-lateral-attachments',m);foliage=Mesh('paired-and-decussate-small-flat-leaves-with-topological-spaces',m)
 main=smooth_path([(-.085,-.004,.007),(-.025,.001,.009),(.035,.004,.009),(.086,.002,.008)],32);twig.tube(main,[.0025*(1-i/31)+.0008*(i/31) for i in range(32)],0,n=10)
 for node,idx in enumerate([8,16,23]):
  for sign in [-1,1]:
   origin=main[idx];L=[.048,.046,.036][node];d=Vector((.44,sign*.90,0)).normalized();p=smooth_path([origin,origin+d*L*.55+Vector((0,0,.0015)),origin+d*L+Vector((.005,0,0))],17);twig.tube(p,[.0013*(1-i/16)+.00035*(i/16) for i in range(17)],0,n=8)
   lateral=Vector((-d.y,d.x,0))
   for j in range(3,15,2):
    for side in [-1,1]:
     # Opposite attachment pairs, with alternate flattened decussate orientation.
     theta=0 if (j//2)%2==0 else pi/2;vec=(lateral*side*.88*math.cos(theta)+d*.40+Vector((0,0,.88*side*math.sin(theta)))).normalized();leaf_blade(foliage,p[j],vec,.0110*(1-.36*j/16),.00155,.00050,1)
 for idx in [4,12,20,28]:
  for side in [-1,1]:leaf_blade(foliage,main[idx],(.42,side*.90,.12*side),.010,.0016,.0004,1)
 twig.finish(c);foliage.finish(c,False)

def ovatiovermis(c,m):
 trunk=Mesh('unarmoured-continuous-soft-tubular-trunk-and-small-head',m);filters=Mesh('two-long-anterior-paired-filter-limbs-and-four-shorter-middle-pairs',m);setae=Mesh('economical-paired-filter-setae-no-trunk-armour',m);rear=Mesh('three-robust-posterior-lobopod-pairs-supporting-body',m);claws=Mesh('single-strong-claw-on-each-posterior-lobopod',m)
 axis=smooth_path([(.001,.020,.012),(0,.010,.015),(-.001,-.002,.026),(0,-.012,.038),(.001,-.016,.043)],32);trunk.tube(axis,[.0034+.0012*math.sin(pi*i/31)-.0013*(i/31) for i in range(32)],0,n=16);trunk.ellipsoid((.001,-.016,.043),(.0028,.0030,.0028),0,n=12,r=8)
 # Two long anterior pairs and four shorter middle pairs are soft unjointed lobopods.
 for pair in range(6):
  idx=26-pair*3;base=axis[idx]
  for sign in [-1,1]:
   if pair<2:
    end=base+Vector((sign*(.018-.002*pair),-.005-.002*pair,.021-.002*pair));bend=base+Vector((sign*.010,-.004,.009));radius=.0012;count=7
   else:
    end=base+Vector((sign*(.009+.0008*(5-pair)),.002,.008-.0008*(pair-2)));bend=(base+end)*.5+Vector((0,-.001,.001));radius=.0010;count=3
   ps=smooth_path([base,bend,end],17);filters.tube(ps,[radius*(1-j/16)+.00023*(j/16) for j in range(17)],1,n=8)
   for j in range(count):
    k=5+int(j*(10/max(1,count-1)));pos=ps[k];tangent=(ps[min(16,k+1)]-ps[k-1]).normalized();side=tangent.cross(Vector((0,1,0))).normalized()
    for ss in [-1,1]:
     L=(.0043 if pair<2 else .0021)*(1-.25*j/max(1,count-1));tip=pos+side*(ss*L)+tangent*.0012;setae.tube([pos,(pos+tip)*.5,tip],[.00020,.00016,.00007],1,n=5)
 # Posterior feet are stockier, form three stable attachment pairs and bear one curved claw each.
 for pair,idx in enumerate([2,6,10]):
  base=axis[idx]
  for sign in [-1,1]:
   foot=Vector((sign*(.0095+.0007*pair),base.y+.004,.0030));ps=smooth_path([base,base+Vector((sign*.006,.001,-.003)),foot],14);rear.tube(ps,[.0027*(1-j/13)+.00115*(j/13) for j in range(14)],0,n=9)
   ps=smooth_path([foot,foot+Vector((sign*.0025,-.001,-.0010)),foot+Vector((sign*.0022,-.004,-.0015)),foot+Vector((-sign*.001,-.005,-.0006))],10);claws.tube(ps,[.0010*(1-j/9)+.00015*(j/9) for j in range(10)],2,n=7)
 trunk.finish(c);filters.finish(c);setae.finish(c);rear.finish(c);claws.finish(c)

def nordenskioldia(c,m):
 axis=Mesh('preserved-slender-fruiting-axis-only',m);recept=Mesh('persistent-umbrella-like-fruit-receptacles-attached-to-axis',m);fruit=Mesh('radial-wedge-fruitlets-with-distinct-boundaries-no-separate-seeds',m)
 ps=smooth_path([(-.005,0,.003),(-.002,.001,.045),(.004,-.001,.095),(.006,.002,.150)],32);axis.tube(ps,[.0017*(1-i/31)+.00055*(i/31) for i in range(32)],0,n=10)
 for j,k in enumerate([6,13,21,28]):
  sign=-1 if j%2==0 else 1;start=ps[k];center=start+Vector((sign*(.013+.001*j),.002,.006));stem=smooth_path([start,(start+center)*.5+Vector((0,0,-.001)),center],10);axis.tube(stem,[.0009*(1-i/9)+.0005*(i/9) for i in range(10)],0,n=8);recept.ellipsoid(center,(.0062,.0062,.0020),1,n=16,r=6)
  # Ten original simplified fruitlets per fruit: count is not copied as a fossil measurement.
  count=10;rot=j*.38
  for i in range(count):
   a=rot+2*pi*i/count;half=pi/count*.90;outline=[]
   for r,da in [(.0030,-half),(.0087,-half),(.0100,-half*.45),(.0104,0),(.0100,half*.45),(.0087,half),(.0030,half)]:outline.append(Vector((r*math.cos(a+da),r*math.sin(a+da),0)))
   n=len(outline);v=[]
   for upper in [False,True]:
    for q in outline:z=(.0043-.0014*q.length/.0104) if upper else .00015;v.append(tuple(center+q+Vector((0,0,z))))
   f=[tuple(reversed(range(n))),tuple(n+k for k in range(n))]
   for k in range(n):f.append((k,(k+1)%n,n+(k+1)%n,n+k))
   fruit.add(v,f,2 if i%3 else 3)
 axis.finish(c);recept.finish(c);fruit.finish(c,False)

def waterfall_ledge(c,m):
 rock=Mesh('one-continuous-overhanging-resistant-lip-and-recessed-soft-lower-bed',m)
 # Cross section travels clockwise in Y/Z: a single closed rock volume, with a real undercut.
 profile=[(.28,0),(-.30,0),(-.33,.045),(-.07,.12),(.025,.18),(.045,.32),(-.28,.37),(-.32,.43),(-.30,.51),(-.23,.535),(.28,.54)]
 nx=24;n=len(profile);v=[];f=[];mi=[]
 for j in range(nx+1):
  x=-.55+1.10*j/nx
  for k,(y,z) in enumerate(profile):
   wave=(.014*math.sin(x*10+.8)+.008*math.sin(x*23)) if k in range(1,10) else .004*math.sin(x*7);zz=z+(.010*math.sin(x*8+k*.2) if k>3 else 0);v.append((x,y+wave,zz))
 f.append(tuple(range(n)));mi.append(1)
 for j in range(nx):
  for k in range(n):f.append((j*n+k,(j+1)*n+k,(j+1)*n+(k+1)%n,j*n+(k+1)%n));mi.append(0 if 6<=k<=10 else 1)
 f.append(tuple(reversed(tuple(nx*n+k for k in range(n)))));mi.append(1);rock.add(v,f,mi);rock.finish(c,False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'metasequoia': [('preserved-branch-brown', '#8E8067'), ('opposite-decusssate-fossil-leaves', '#9A9173')], 'ovatiovermis': [('soft-bare-trunk-and-anchoring-feet', '#AF9C84'), ('soft-filter-arms-and-setae', '#C0AF90'), ('single-posterior-claws', '#776D5E')], 'nordenskioldia': [('preserved-fruit-axis', '#8C7C61'), ('persistent-receptacle', '#A29474'), ('radial-fruitlets', '#AE9A76'), ('subtle-fruitlet-variation', '#A4916F')], 'waterfall-ledge': [('resistant-overhanging-cap', '#A4A28E'), ('recessed-softer-rock-bed', '#8E9387')]}
 mats=[make_material(name,color,roughness=.82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=(hi[2]-lo[2]) if slug in ['ovatiovermis','nordenskioldia'] else (hi[0]-lo[0]);scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'metasequoia': {'en': 'Metasequoia-inspired preserved leafy branch organ only, with explicit opposite lateral attachments and paired/decussate small flat leaves separated by readable node intervals. Specimen display, no full tree/crown, roots or unsupported associated reproductive organs. Thickness, compression, leaf counts and nominal span are artistic, not measured fossil data.', 'zh': 'Metasequoia启发保存叶枝器官，明确对生侧枝、小扁叶成对并交互排列，节点间隔清楚。仅标本展示，不造完整树冠、根或未关联生殖器官；厚度、压缩程度、叶数和名义展宽属艺术选择，非化石测量。'}, 'ovatiovermis': {'en': 'Marine Ovatiovermis-inspired bare soft tubular lobopodian: two long anterior filter-limb pairs rise from the trunk, four middle pairs are shorter, and three robust posterior pairs terminate in single curved supporting claws. Fine filtering setae are economical original simplifications. Static artistic posture, no armour, humanoid arms or exact feeding mechanics.', 'zh': '海生Ovatiovermis启发裸软管状叶足动物，前两对长滤食足举起，中四对较短，后三对粗足各具单强弯爪支撑；细滤毛经济原创简化。静态艺术姿势，无躯甲、人形手臂或精确取食力学承诺。'}, 'nordenskioldia': {'en': 'Nordenskioldia-inspired preserved fruiting axis organ only: a slender axis carries four separated radial segmented fruits on persistent receptacles, with visible wedge-shaped fruitlet boundaries. Ten fruitlets per teaching fruit are an artistic simplification, not the source specimens counted thirteen/fifteen. No separate seed asset, unknown whole tree, flowers or leafy crown.', 'zh': 'Nordenskioldia启发保存果序轴器官：细轴带四个分隔清楚的放射分段果，接入宿存果托，小楔形果片边界可读。每果十片是教学简化，不冒称原标本十三/十五片计数；不另计种子，不造未知整树、花或叶冠。'}, 'waterfall-ledge': {'en': 'Original waterfall-ledge teaching rock only: one continuous rock volume has a projecting resistant upper lip and a recessed lower soft bed creating real sheltered undercut space. Intentional side presentation cuts and nominal shape, no water mesh, water-flow simulation, exact site/age or loose stacked-block interpretation.', 'zh': '原创瀑布岩阶教学岩体：单一连续岩体，上部抗蚀岩缘突出，下方较软层后退形成真实遮蔽空间。侧面为展示切面、形态尺度属艺术选择，不导出水体、不模拟水流、不指定地点年代，非松散方砖堆。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,('hero',),resolution=512,samples=8,transparent=True)
if __name__=='__main__':main()
