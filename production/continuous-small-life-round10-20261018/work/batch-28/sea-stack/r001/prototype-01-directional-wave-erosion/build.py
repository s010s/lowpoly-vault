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

def fan_leaf(mesh,center,angle,length,tilt,mat):
 p=Vector(center);u=Vector((math.cos(angle),math.sin(angle),0));v=Vector((-u.y,u.x,0));z=Vector((0,0,1));outline=[p]
 for k in range(9):
  a=-.70+1.40*k/8;q=p+(u*math.cos(a)+v*math.sin(a))*length*(1-.10*abs(a))
  q.z+=tilt*length*math.cos(a)+length*.025*math.cos(3*a);outline.append(q)
 n=len(outline);ctr=p+u*length*.64+z*(tilt*length*.64+.0011);verts=[tuple(q+z*.00024) for q in outline]+[tuple(q-z*.00024) for q in outline]+[tuple(ctr),tuple(ctr-z*.0013)];f=[]
 for k in range(n):f.extend([(2*n,k,(k+1)%n),(2*n+1,n+(k+1)%n,n+k),(k,n+k,n+(k+1)%n,(k+1)%n)])
 mesh.add(verts,f,mat)

def marsilea(c,m):
 base=Mesh('creeping-branched-rhizome-modern-genus-analogy',m);pet=Mesh('slender-bent-petioles-connected-to-creeping-axis',m);leaves=Mesh('four-separate-fan-leaflets-per-frond-no-flowers',m)
 points=[(-.068,.010,.003),(-.037,-.005,.003),(-.006,.002,.004),(.031,-.009,.003),(.067,.003,.004)];ps=smooth_path(points,25);base.tube(ps,[.0017*(1-.2*i/24) for i in range(25)],0,n=9)
 for j,(idx,dx,dy,h,L,az) in enumerate([(1,-.009,-.009,.039,.021,.15),(6,-.006,.006,.066,.024,.43),(12,.008,-.002,.080,.025,.18),(18,-.002,.008,.054,.023,.65),(23,.005,-.004,.070,.022,.25)]):
  start=ps[idx];top=start+Vector((dx,dy,h));p=smooth_path([start,start+Vector((dx*.3,dy*.4,h*.45)),top],16);pet.tube(p,[.00105*(1-i/15)+.00060*i/15 for i in range(16)],0,n=8)
  for k in range(4):fan_leaf(leaves,top,az+k*pi/2,L*(1+.035*math.sin(j+k)),(.05+.08*math.sin(j*.8+k*.7)),1+(j+k)%2)
 # Small branch ties the creeping base to a secondary growth direction, not a rosette.
 p=smooth_path([ps[10],ps[10]+Vector((-.004,.016,.001)),ps[10]+Vector((.006,.030,.001))],10);base.tube(p,[.0013*(1-i/9)+.00045*i/9 for i in range(10)],0,n=8)
 base.finish(c);pet.finish(c);leaves.finish(c,False)

def hurdia(c,m):
 shell=Mesh('projecting-triangular-central-H-carapace',m);side=Mesh('paired-lateral-paddle-P-carapace-elements',m);body=Mesh('short-soft-posterior-trunk',m);flap=Mesh('short-trunk-triangular-swimming-flaps',m);front=Mesh('ventral-curved-rake-appendages-with-economic-teeth',m);eyes=Mesh('short-stalked-eyes-at-rear-carapace-notches',m);tail=Mesh('two-rounded-terminal-tail-lobes',m)
 ellipse_loft(body,[(0,-.030,.023,.023,.011),(0,-.010,.025,.032,.014),(.002,.015,.026,.030,.013),(.003,.043,.027,.024,.011),(.002,.066,.027,.015,.008),(0,.081,.027,.004,.003)],20,0)
 # Original shield profile: narrow forward projection expands into a broad roof, not a horseshoe.
 ellipse_loft(shell,[(0,-.143,.049,.0018,.0012),(0,-.119,.051,.010,.003),(0,-.088,.054,.026,.007),(0,-.053,.054,.039,.009),(0,-.019,.050,.034,.008),(0,.001,.044,.022,.004)],18,1)
 for s in [-1,1]:
  p=smooth_path([(s*.017,-.106,.043),(s*.034,-.064,.041),(s*.037,-.023,.035),(s*.024,.012,.031)],18);flat_strap(side,p,[.001+.009*math.sin(pi*i/17)**.7 for i in range(18)],.002,(s,0,.2),2,n=8)
  # Eyes emerge at the posterior shield notch and remain seated on a short fleshy stalk.
  p=smooth_path([(s*.025,-.007,.033),(s*.039,-.005,.040),(s*.047,-.009,.042)],9);eyes.tube(p,[.0024*(1-i/8)+.0019*i/8 for i in range(9)],0,n=8);eyes.ellipsoid(p[-1],(.0055,.0058,.0052),4,n=14,r=8)
  p=smooth_path([(s*.017,-.024,.020),(s*.027,-.054,.010),(s*.028,-.087,.007),(s*.018,-.111,.017)],19);front.tube(p,[.0042*(1-i/18)+.0015*i/18 for i in range(19)],3,n=10)
  for j in range(6):
   b=p[4+j*2];tip=b+Vector((-s*(.006-.0004*j),-.003,-.002));front.tube([b,(b+tip)*.5,tip],[.00125,.00075,.00018],3,n=6)
  for j in range(7):leaf_blade(flap,(s*(.024-.002*j),.000+j*.010,.023),(s*.85,.5,0),.025*(1-.07*j),.008*(1-.05*j),.0015,2)
  # A restrained rounded terminal pair, no Anomalocaris-style upturned three-pair fan.
  p=smooth_path([(s*.002,.074,.026),(s*.010,.088,.027),(s*.013,.102,.028)],11);flat_strap(tail,p,[.0007+.0068*math.sin(pi*i/10)**.6 for i in range(11)],.001,(s*.9,-.25,0),2,n=8)
 shell.finish(c,False);side.finish(c,False);body.finish(c);flap.finish(c,False);front.finish(c);eyes.finish(c);tail.finish(c)

def sea_stack(c,m):
 rock=Mesh('single-isolated-steep-coastal-stack-with-coherent-wave-cut-base',m);n=23;zs=[0,.12,.29,.48,.69,.91,1.25,1.63,2.03,2.40,2.78,3.15,3.46,3.72,3.90];rs=[.76,.78,.69,.59,.58,.69,.82,.85,.82,.79,.75,.72,.66,.59,.42];vs=[];f=[];mi=[]
 for j,(z,r) in enumerate(zip(zs,rs)):
  for k in range(n):
   a=2*pi*k/n;shape=1+.105*math.sin(3*a+.6)+.055*math.sin(5*a-1)+.028*math.sin(8*a+j*.15);erosion=.10*math.cos(a+.2)*math.exp(-((z-.52)/.28)**2);rad=r*shape-erosion;cx=.055*math.sin(z*.8);cy=.035*math.sin(z*1.3)
   vs.append((cx+rad*math.cos(a),cy+rad*.77*math.sin(a),z+(.045*math.sin(a*3)+.020*math.sin(a*5+.3))*(j/(len(zs)-1))))
 f.append(tuple(reversed(range(n))));mi.append(2)
 for j in range(len(zs)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(2 if j<3 else (1 if j in [6,10,12] else 0))
 top=len(vs);vs.append((.035,-.02,3.91))
 for k in range(n):f.append(((len(zs)-1)*n+k,(len(zs)-1)*n+(k+1)%n,top));mi.append(1)
 rock.add(vs,f,mi);rock.finish(c,False)

def raw_tube(name,pts,rads,c,m,inner=False):
 mesh=Mesh(name,m);n=18;ps=[Vector(p) for p in pts];v=[];f=[]
 for j,p in enumerate(ps):
  d=(ps[min(j+1,len(ps)-1)]-ps[max(j-1,0)]).normalized();u=d.cross(Vector((0,1,0)))
  if u.length<.01:u=d.cross(Vector((1,0,0)))
  u.normalize();w=d.cross(u).normalized()
  for k in range(n):
   a=2*pi*k/n;r=rads[j]*(1 if inner else 1+.065*math.sin(5*a+j*.7)+.035*math.sin(3*a-j*.9));v.append(tuple(p+r*(u*math.cos(a)+w*math.sin(a))))
 f.append(tuple(reversed(range(n))))
 for j in range(len(ps)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 f.append(tuple((len(ps)-1)*n+k for k in range(n)));mesh.add(v,f,2 if inner else 0);return mesh.finish(c,False)

def fulgurite_tube(c,m):
 # Build original outer junctions and subtract connected extended lumens: a real continuous hollow tree.
 main=smooth_path([(0,0,.008),(.008,.004,.062),(-.006,.003,.115),(.003,-.003,.168),(.017,0,.214)],24)
 branch=smooth_path([main[10],(.030,.009,.126),(.066,.010,.145),(.092,.004,.160)],15)
 branch2=smooth_path([main[15],(-.022,-.005,.171),(-.042,-.013,.196)],12)
 paths=[main,branch,branch2];rads=[[.0125*(1-i/23)+.0095*i/23 for i in range(24)],[.0100*(1-i/14)+.0060*i/14 for i in range(15)],[.0075*(1-i/11)+.0047*i/11 for i in range(12)]]
 def boolean(target,cutter,op,label):
  bpy.context.view_layer.objects.active=target;mod=target.modifiers.new(label,'BOOLEAN');mod.operation=op;mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 rock=raw_tube('continuous-fused-sand-glass-branching-shell',paths[0],rads[0],c,m)
 for j in [1,2]:boolean(rock,raw_tube('_outer-branch-'+str(j),paths[j],rads[j],c,m),'UNION','fused-continuous-outer-junction-'+str(j))
 cutters=[]
 for j,(ps,rs) in enumerate(zip(paths,rads)):
  q=list(ps);q[0]=q[0]-(q[1]-q[0]).normalized()*.018;q[-1]=q[-1]+(q[-1]-q[-2]).normalized()*.018
  cutters.append(raw_tube('_true-lumen-'+str(j),q,[r*.58 for r in rs],c,m,True))
 bore=cutters[0]
 for j in [1,2]:boolean(bore,cutters[j],'UNION','connected-lumen-junction-'+str(j))
 boolean(rock,bore,'DIFFERENCE','real-hollow-core-through-all-branch-mouths')
 import bmesh
 bm=bmesh.new();bm.from_mesh(rock.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(rock.data);bm.free();rock.data.update()
 for p in rock.data.polygons:
  if p.material_index==2:p.use_smooth=True
  elif p.center.z<.04 or (p.center.z>.10 and p.center.z<.13):p.material_index=1

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'marsilea': [('creeping-axis-and-petioles', '#718766'), ('fan-leaf-upper-green', '#91A980'), ('fan-leaf-warm-green', '#A2B48B')], 'hurdia': [('short-soft-body', '#9C9B85'), ('projecting-triangular-shield', '#B8AD87'), ('lateral-paddles-and-flaps', '#9FA58D'), ('ventral-rakes', '#918B74'), ('short-stalk-eyes', '#424F48')], 'sea-stack': [('weathered-cliff-body', '#949587'), ('resistant-bedding-edges', '#A6A393'), ('wave-cut-base', '#7C8278')], 'fulgurite-tube': [('fused-sand-glass-outer-wall', '#A59A7F'), ('sandy-fused-growth-bands', '#BAB098'), ('real-glass-lined-lumen', '#72796B')]}
 mats=[make_material(name,color,roughness=.72 if slug=='fulgurite-tube' else .82) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=(hi[2]-lo[2]) if slug=='sea-stack' else ((hi[1]-lo[1]) if slug=='hurdia' else max(hi[0]-lo[0],hi[1]-lo[1],hi[2]-lo[2]));scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'marsilea': {'en': 'Marsilea-inspired freshwater margin water-fern patch with creeping branched rhizome, naturally curved upright petioles and four separate fan leaflets on each frond. Modern genus basic architecture is an analogy only; original needs-specific-reference status retained, not a precise fossil species, spore structure or flowering clover reconstruction. No marine habitat or water mesh.', 'zh': 'Marsilea启发淡水岸边水蕨，以匍匐分枝根茎连接自然弯叶柄，每柄四枚独立扇形小叶。仅借现代属级基础架构，保留needs-specific-reference，不作精确化石种、孢子结构或有花三叶草复原。不作海生或导出水体。'}, 'hurdia': {'en': 'Original Hurdia-inspired marine radiodont: large projecting triangular central shield with paired lateral paddle elements, short soft trunk and triangular lateral flaps, ventral curved rake appendages, short-stalked eyes at rear shield notches and two rounded tail lobes. Microteeth and soft-tissue counts simplified, no predation or movement mechanism claim.', 'zh': '原创Hurdia启发海生奇虾类：前伸三角中央大甲与成对侧桨甲、短软躯及三角侧叶、腹侧弯耙肢、后甲角短柄眼和两圆尾叶。微耙齿和软组织数量省简，不承诺捕食或运动机制。'}, 'sea-stack': {'en': 'One independent steep coastal remnant with a continuous irregular cliff mass and a coherent wave-eroded lower notch, supported by a broad stable foot. Landscape scale retained: nominal 4 m height is a teaching art choice, not an exact locality, measured stack or unit-normalized stone. No water exported.', 'zh': '单一独立陡立海岸残余岩体，连续不规则峭壁和连贯浪蚀下凹，宽稳岩脚支撑。保留landscape尺度，名义4米高属教学美术，不指定地点、实测岩柱或单位化小石。不导出水体。'}, 'fulgurite-tube': {'en': 'Original small branching fused-sand glass tube with a continuous outer shell and connected true hollow core opening at the base and all tips. Irregular fused wall, unequal branch hierarchy and restrained opaque glass-lined lumen; not a smooth plastic pipe, plant root, copied specimen or complex transparent material. Empty eras/biomes remain unspecified.', 'zh': '原创小型分叉熔砂玻璃管，连续外壁与相连真实空芯贯通基部和各尖端；不规则熔结壁、主次分枝，克制不透明玻璃内衬，非光滑塑料管、植物根、标本复制或复杂透明材质。空时代生境保持未指定。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'revision':'r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'reference_status':'needs-specific-reference' if slug=='marsilea' else 'basic-form textual reference support; not strict reconstruction','publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
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
