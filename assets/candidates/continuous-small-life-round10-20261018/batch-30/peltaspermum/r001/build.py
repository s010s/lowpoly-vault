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

def peltaspermum(c,m):
 disc=Mesh('preserved-thin-wavy-peltate-reproductive-disc-only',m);stalk=Mesh('cut-petiole-connected-to-disc-underside',m);bases=Mesh('attached-lower-surface-ring-of-simplified-ovulate-bases',m)
 N=60;R=5;v=[];f=[];mi=[]
 def surface(x,y):return .038-1.25*y
 # Thin shield, no thick mushroom cap. A tilt exposes the lower-surface relationship in ordinary gray views.
 for side in [1,-1]:
  for j in range(1,R+1):
   t=j/R
   for k in range(N):
    a=2*pi*k/N;r=t*(1+.035*math.sin(10*a+.2));x=.026*r*math.cos(a);y=.023*r*math.sin(a);z=surface(x,y)+side*.00038+.00055*(1-t*t)+.00020*t*math.cos(10*a+.2);v.append((x,y,z))
  v.append((0,0,.038+side*.00038+.00055))
 off=N*R+1
 for side in [0,1]:
  o=side*off;ctr=o+N*R
  for k in range(N):f.append((ctr,o+k,o+(k+1)%N) if side==0 else (ctr,o+(k+1)%N,o+k));mi.append(0 if side==0 else 1)
  for j in range(R-1):
   for k in range(N):
    q=(o+j*N+k,o+(j+1)*N+k,o+(j+1)*N+(k+1)%N,o+j*N+(k+1)%N);f.append(q if side==0 else tuple(reversed(q)));mi.append(0 if side==0 else 1)
 for k in range(N):a=(R-1)*N+k;b=(R-1)*N+(k+1)%N;f.append((a,off+a,off+b,b));mi.append(0)
 disc.add(v,f,mi)
 p=smooth_path([(.006,.014,0),(.008,.009,.014),(.003,.003,.027),(0,0,.0382)],19);stalk.tube(p,[.00125*(1-i/18)+.00155*i/18 for i in range(19)],1,n=10)
 # These are attached simplified basal ovulate structures of the same organ, not separate seed assets.
 for k in range(10):
  a=2*pi*k/10+.19;x=.0183*math.cos(a);y=.0158*math.sin(a);z=surface(x,y)-.0002;end=Vector((x*1.03,y*1.03,z-.0030));bases.tube([(x,y,z),tuple(end)],[.0010,.0010],1,n=8);bases.ellipsoid(end,(.0026,.0023,.0016),2,n=12,r=7)
 disc.finish(c,False);stalk.finish(c);bases.finish(c)

def capinatator(c,m):
 body=Mesh('continuous-slender-flexible-body-and-head-no-ring-worm-segmentation',m);banks=Mesh('two-opposed-curving-head-spine-arrays-blunt-friendly-static',m)
 sections=[]
 for j in range(39):
  t=j/38;y=-.039+.080*t;x=.0016*math.sin(t*pi*1.6);rx=.00022+.0030*math.sin(pi*(.12+.86*t))**.8
  rx+=.00135*math.exp(-((t-.09)/.13)**2);rz=rx*.62;sections.append((x,y,.0043+.0006*math.sin(t*pi),rx,rz))
 ellipse_loft(body,sections,20,0)
 for s in [-1,1]:
  for j in range(9):
   b=Vector((s*(.0032+.0003*math.sin(j*.4)),-.0375+j*.00058,.0048+.00014*j));p=smooth_path([b,b+Vector((s*.0013,-.0020,.0022)),b+Vector((-s*.0013,-.0055,.0034)),b+Vector((-s*.0023,-.0062,.0028))],13);banks.tube(p,[.00040*(1-i/12)+.00011*i/12 for i in range(13)],1,n=7)
 body.finish(c);banks.finish(c)

def cothurnocystis(c,m):
 body=Mesh('original-asymmetric-flattened-boot-shaped-theca',m);plates=Mesh('broad-interlocking-plate-fields-inset-relief-not-ball-pattern',m);arm=Mesh('single-long-curved-segmented-appendage-connected-to-boot-base',m)
 outline=[(-.011,-.022),(.002,-.025),(.013,-.023),(.020,-.017),(.019,-.008),(.008,-.004),(.007,.013),(-.002,.019),(-.012,.016),(-.015,.006),(-.011,-.003),(-.016,-.013)];n=len(outline);ctr=Vector((-.003,-.005,.006));v=[];f=[]
 for side in [-1,1]:
  for x,y in outline:v.append((x,y,.003+side*.0025))
 v += [(-.003,-.005,.0005),tuple(ctr)]
 for k in range(n):
  f.extend([(2*n,(k+1)%n,k),(2*n+1,n+k,n+(k+1)%n),(k,(k+1)%n,n+(k+1)%n,n+k)])
 body.add(v,f,0)
 # Economical distinct broad plates follow the boot surface, with shallow inset seams.
 for j in range(0,n,2):
  raw=[Vector((outline[j][0],outline[j][1],.0055)),Vector((outline[(j+1)%n][0],outline[(j+1)%n][1],.0055)),Vector((outline[(j+2)%n][0],outline[(j+2)%n][1],.0055)),ctr];center=sum(raw,Vector())/len(raw);poly=[center+(q-center)*.91 for q in raw];vv=[tuple(q+Vector((0,0,z))) for z in [-.0004,.0005] for q in poly];nn=len(poly);ff=[tuple(reversed(range(nn))),tuple(nn+k for k in range(nn))]
  for k in range(nn):ff.append((k,(k+1)%nn,nn+(k+1)%nn,nn+k))
  plates.add(vv,ff,1 if j%4==0 else 0)
 ps=smooth_path([(-.003,.014,.0035),(-.005,.028,.0037),(-.002,.049,.004),(.009,.067,.0045),(.008,.085,.0048)],43)
 # Continuous core and shallow periodic annuli communicate segmentation without detached bead pieces.
 rs=[]
 for i in range(43):
  t=i/42;r=(.00245*(1-t)+.00062*t)*(1-.16*(.5+.5*math.cos(2*pi*t*13)));rs.append(r)
 arm.tube(ps,rs,2,n=11)
 body.finish(c,False);plates.finish(c,False);arm.finish(c)

def pyrite_cube_cluster(c,m):
 from mathutils import Euler
 matrix=Mesh('irregular-natural-host-matrix-part-of-crystal-cluster',m);n=15;v=[];f=[]
 for j,(r,z) in enumerate([(1,0),(1.04,.012),(.88,.029),(.40,.038)]):
  for k in range(n):a=2*pi*k/n;rad=1+.11*math.sin(3*a+.4)+.07*math.sin(5*a);v.append((.078*r*rad*math.cos(a),.054*r*rad*math.sin(a),z+(.003*math.sin(3*a)*j/3)))
 f.append(tuple(reversed(range(n))))
 for j in range(3):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 f.append(tuple(3*n+k for k in range(n)));matrix.add(v,f,2);matrix.finish(c,False)
 crystals=Mesh('hierarchical-sharp-cubic-intergrowths-and-faced-growth-steps',m)
 def crystal(center,size,rot,mat=0):
  s=size/2;R=Euler(rot).to_matrix();cen=Vector(center);vv=[tuple(cen+R@Vector((x,y,z))) for x,y,z in [(-s,-s,-s),(s,-s,-s),(s,s,-s),(-s,s,-s),(-s,-s,s),(s,-s,s),(s,s,s),(-s,s,s)]];ff=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];crystals.add(vv,ff,[mat,1,mat,0,mat,0])
 mainR=(.13,-.18,-.16);cen=Vector((.003,.003,.064));crystal(cen,.082,mainR)
 crystal((-.048,.018,.042),.051,(.10,.30,.38));crystal((.042,-.035,.035),.040,(-.15,.14,-.40))
 R=Euler(mainR).to_matrix()
 for p,size in [((-.022,-.037,.026),.029),((.027,-.031,.036),.021),((.035,.028,-.021),.018)]:crystal(cen+R@Vector(p),size,mainR)
 o=crystals.finish(c,False)
 # Submillimetre original bevels provide edge highlights; cube faces and natural intergrowth stay sharp.
 bpy.context.view_layer.objects.active=o;bev=o.modifiers.new('submillimetre-crystal-edge-highlights','BEVEL');bev.width=.00028;bev.segments=1;bpy.ops.object.modifier_apply(modifier=bev.name)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'peltaspermum': [('thin-preserved-peltate-disc', '#A29E7C'), ('petiole-and-disc-underside', '#8D9072'), ('attached-ovulate-bases', '#B2A58A')], 'capinatator': [('slender-soft-body', '#9FAF9E'), ('opposed-curved-head-spines', '#B9B59C')], 'cothurnocystis': [('boot-theca-main-plates', '#B1AC96'), ('raised-broad-plate-fields', '#C0BAA3'), ('single-segmented-appendage', '#A5A48B')], 'pyrite-cube-cluster': [('restrained-brassy-pyrite-cube-faces', '#B6A16C'), ('pale-brass-crystal-growth-faces', '#C4B580'), ('natural-host-matrix', '#77796F')]}
 mats=[make_material(name,color,roughness=.42 if slug=='pyrite-cube-cluster' and name!='natural-host-matrix' else .82,metallic=.68 if slug=='pyrite-cube-cluster' and name!='natural-host-matrix' else 0) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=.080 if slug=='capinatator' else ((hi[1]-lo[1]) if slug=='cothurnocystis' else max(hi[0]-lo[0],hi[1]-lo[1],hi[2]-lo[2]));scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'peltaspermum': {'en': 'Peltaspermum-inspired preserved reproductive organ only: thin shallow-wavy peltate disc on a cut curved stalk, with attached simplified basal ovulate structures in a ring on its lower surface. Tilt deliberately reveals the underside relationship. No thick fungal cap, gills, flower, parent plant or separately counted/extracted seed asset; exact count, color and nominal span artistic.', 'zh': 'Peltaspermum启发保存生殖器官：薄浅波缘盾盘与弯曲断柄自然衔接，下表面环列简化着生基部。倾角为展示下侧关系，不作厚蘑菇帽/菌褶、花、母体或另计/取出种子资产；数量颜色名义跨度属美术选择。'}, 'capinatator': {'en': 'Original Capinatator-inspired slender continuous flexible marine body with two opposed arrays of modest curved head spines. Calm static pose and rounded economical spine tips, no enlarged fangs or predation action. Source microscopic counts simplified, no Yale artwork or external model copied; no precise locomotion claim.', 'zh': '原创Capinatator启发细长连续柔躯海生形态，头端两侧相对克制弧棘阵列。友善静态姿势与省简钝尖，无夸张獠牙或捕食动作；微棘数量省简，不复制Yale艺术图或外部模型，不承诺精确运动机制。'}, 'cothurnocystis': {'en': 'Original basic Cothurnocystis-inspired flattened asymmetric boot-shaped plated theca, with broad connected plate fields and one long curved segmented appendage naturally seated at its base. General group text and named captions do not establish species-exact plate seams or feeding mechanism; no starfish or stretched plated sphere.', 'zh': '原创基础Cothurnocystis启发扁平不对称靴形板甲体，宽板域连贯，单根长弯分节附肢自然接基。类群正文与具名图注不等种级板缝或取食机制实证；非海星或拉伸板甲球。'}, 'pyrite-cube-cluster': {'en': 'Original cubic pyrite habit teaching cluster: dominant and subordinate sharp cubes, intentional natural intergrowth, shallow faced growth steps and irregular host matrix. Restrained metallic brass palette, no industrial regular grid or accidental collision claim; no copied specimen locality/measurement or microscopic striation obligation. Empty era/biome facets remain unspecified.', 'zh': '原创立方黄铁矿晶形教学簇：主次锐立方晶、有意天然交生、浅台阶晶面与不规则基体。克制黄铜金属色，非工业规则网格；交生非意外穿插，不复制具体矿点/实测标本、不要求微晶纹。空时代生境保持未指定。'}}
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
