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

def pentremites(c,m):
 body=Mesh('five-rayed-bud-theca-with-physical-petaloid-longitudinal-food-grooves',m);stem=Mesh('short-stalk-naturally-seated-under-bud',m);arms=Mesh('restrained-fine-brachioles-open-around-food-grooves-not-closed-crown',m);N=100;R=19;v=[];f=[];mi=[]
 for j in range(R):
  t=j/(R-1);z=.047+.070*t;rad=.003+.023*math.sin(pi*t)**.76
  for k in range(N):
   a=2*pi*k/N;d=((a+pi/5)%(2*pi/5))-pi/5;petal=.0017*math.sin(pi*t)**.75*math.exp(-(d/(.09+.10*math.sin(pi*t)))**2);r=rad*(1+.065*math.cos(5*a))-petal;v.append((r*math.cos(a),r*math.sin(a),z))
 f.append(tuple(reversed(range(N))));mi.append(0)
 for j in range(R-1):
  for k in range(N):f.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k));mi.append(1 if k%20 in [0,1,19] else 0)
 top=len(v);v.append((0,0,.118))
 for k in range(N):f.append(((R-1)*N+k,(R-1)*N+(k+1)%N,top));mi.append(0)
 body.add(v,f,mi);body.finish(c,False)
 stem.tube(smooth_path([(-.001,0,0),(-.002,0,.02),(0,0,.049)],18),[.0025+.0009*(i/17)**2 for i in range(18)],0,n=16);stem.finish(c)
 for j in range(5):
  a=j*2*pi/5
  for side in [-1,1]:
   b=a+side*.13;pts=smooth_path([(.018*math.cos(b),.018*math.sin(b),.091),(.030*math.cos(b+side*.10),.030*math.sin(b+side*.10),.111),(.031*math.cos(b+side*.16),.031*math.sin(b+side*.16),.135),(.025*math.cos(b+side*.20),.025*math.sin(b+side*.20),.145)],18);arms.tube(pts,[.00075*(1-.86*i/17) for i in range(18)],2,n=7)
 arms.finish(c)

def slab_mesh(c,m,name,wx,wy,z):
 mesh=Mesh(name,m);N=48;v=[];f=[]
 for h in [0,z]:
  for k in range(N):a=2*pi*k/N;v.append((wx*.5*math.copysign(abs(math.cos(a))**.32,math.cos(a)),wy*.5*math.copysign(abs(math.sin(a))**.32,math.sin(a)),h))
 for k in range(N):f.append((k,(k+1)%N,N+(k+1)%N,N+k))
 v.extend([(0,0,0),(0,0,z)])
 for k in range(N):f.extend([(2*N,(k+1)%N,k),(2*N+1,N+k,N+(k+1)%N)])
 mesh.add(v,f,0);return mesh.finish(c,False)

def schizoneura(c,m):
 slab_mesh(c,m,'original-preserved-shoot-teaching-host-not-whole-plant',.19,.34,.010);axis=Mesh('detached-jointed-axis-with-wide-paired-split-node-sheaths',m)
 pts=smooth_path([(-.008,-.145,.012),(.004,-.045,.014),(-.002,.055,.014),(.008,.145,.013)],28);axis.tube(pts,[.0042*(1-.25*i/27) for i in range(28)],1,n=12)
 for j,y in enumerate([-.115,-.055,.008,.073,.125]):
  x=.003*math.sin(y*22);axis.tube([(x,y-.003,.014),(x,y+.003,.014)],[.0053,.0051],1,n=16)
  for side in [-1,1]:
   path=smooth_path([(x,y,.014),(x+side*.013,y+.012,.015),(x+side*(.043-.003*j),y+.029,.016),(x+side*(.052-.004*j),y+.047,.014)],13)
   widths=[.001+.012*math.sin(pi*i/12)**.65 for i in range(13)];flat_strap(axis,path,widths,.0016,(-.45*side,1,0),1,n=8)
 axis.finish(c)

def tombolo(c,m):
 mesh=Mesh('continuous-mainland-sediment-neck-offshore-island-land-and-bed-no-water',m);nx=72;ny=56;v=[];f=[]
 def height(x,y):
  coast=-4.2+.30*math.sin(y*.62);main=2.0/(1+math.exp(max(-30,min(30,(x-coast)/.45))))
  island=2.55*math.exp(-((x-5.1)/1.80)**2-((y-.60)/2.35)**2)*(1+.07*math.sin(y*1.4))
  t=max(0,min(1,(x+4.8)/9.9));center=-.8+1.4*t+.18*math.sin(t*pi);width=.42+.55*(abs(t-.5)*2)**1.6;neck=.67*math.exp(-((y-center)/width)**2)*math.exp(-((x-.1)/6.3)**6)
  return .10+math.log(math.exp(main*10)+math.exp(island*10)+math.exp(neck*10))/10
 for j in range(ny+1):
  y=-7+14*j/ny
  for i in range(nx+1):x=-9+18*i/nx;v.append((x,y,height(x,y)))
 for j in range(ny):
  for i in range(nx):a=j*(nx+1)+i;f.append((a,a+1,a+nx+2,a+nx+1))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];off=len(v)
 for a in boundary:x,y,z=v[a];v.append((x,y,0))
 for j,a in enumerate(boundary):b=boundary[(j+1)%len(boundary)];f.append((a,off+j,off+(j+1)%len(boundary),b))
 center=len(v);v.append((0,0,0))
 for j in range(len(boundary)):f.append((center,off+(j+1)%len(boundary),off+j))
 mesh.add(v,f);mesh.finish(c)

def entobia_sponge_boring_network(c,m):
 # Actual CSG chambers/galleries cut a carbonate teaching section, not surface dots.
 import bmesh
 host=Mesh('carbonate-section-with-true-interconnected-chamber-and-gallery-voids',m);host.add([(-.12,-.055,0),(.12,-.055,0),(.12,.065,0),(-.12,.065,0),(-.12,-.055,.19),(.12,-.055,.19),(.12,.065,.19),(-.12,.065,.19)],[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);obj=host.finish(c,False)
 sources=bpy.data.collections.new('SOURCE_EDITABLE_VOID_CUTTERS_NOT_EXPORTED');bpy.context.scene.collection.children.link(sources)
 centers=[(-.077,-.046,.045,.022),(-.012,-.046,.035,.025),(.061,-.047,.052,.026),(-.066,-.045,.117,.026),(.004,-.046,.109,.031),(.079,-.045,.132,.023),(-.017,-.044,.164,.018)]
 cutters=[]
 for j,(x,y,z,r) in enumerate(centers):
  cut=Mesh('original-chamber-void-'+str(j),m);cut.ellipsoid((x,y,z),(r,r*.84,r*.90),n=18,r=9);cutters.append(cut)
 for j,(ia,ib) in enumerate([(0,1),(1,2),(0,3),(1,4),(2,5),(3,4),(4,5),(3,6),(4,6)]):
  a=Vector(centers[ia][:3]);b=Vector(centers[ib][:3]);mid=(a+b)*.5;mid.y=-.052;mid.z+=.0025*math.sin(j);pts=smooth_path([a,mid,b],7);cut=Mesh('original-connecting-gallery-void-'+str(j),m);cut.tube(pts,[.0065+.0005*math.sin(j+k*.6) for k in range(7)],n=10);cutters.append(cut)
 for j,cut in enumerate(cutters):
  data=bpy.data.meshes.new(cut.name);data.from_pydata(cut.v,[],cut.f);data.update();operand=bpy.data.objects.new(cut.name,data);sources.objects.link(operand);bpy.context.view_layer.objects.active=obj;obj.select_set(True);mod=obj.modifiers.new('Exact original chamber/gallery difference '+str(j),'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=operand;bpy.ops.object.modifier_apply(modifier=mod.name);operand.hide_render=True;operand.hide_set(True)
 # Submicron intersection cleanup is deliberate, not a lowered QA threshold.
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()
 sources.hide_render=True;sources.hide_viewport=True

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'pentremites': [('bud-theca', '#B3A98C'), ('longitudinal-grooves', '#A5A086'), ('fine-brachioles', '#C2B596')], 'schizoneura': [('illustrative-preserved-organ-host', '#B9AF95'), ('paired-sheaths-and-jointed-shoot', '#8B9479')], 'tombolo': [('continuous-sediment-mainland-neck-island', '#ADA98F')], 'entobia-sponge-boring-network': [('carbonate-chamber-and-gallery-host', '#B8B09A')]}
 mats=[make_material(name,color,roughness=.86) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=(hi[2]-lo[2]) if slug=='pentremites' else (hi[1]-lo[1]) if slug=='schizoneura' else hi[0]-lo[0];scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'pentremites': {'en': 'Original Pentremites-inspired stalked five-rayed bud theca with physical longitudinal petaloid food grooves and restrained fine open brachioles. No closed crinoid crown or spiral-cup rescale; exact fine anatomy, counts, colors and nominal size artistic.', 'zh': '原创Pentremites启发有柄五棱芽体，真实纵花瓣食沟与克制开放细腕丝；非封闭海百合冠或螺旋杯缩放。精细软体、数量、配色与名义尺度属美术选择。'}, 'schizoneura': {'en': 'Preserved Schizoneura-inspired jointed shoot shallow-relief organ only, with broad paired split leaf-sheath clusters seated at nodes on an illustrative host slab. No whole plant, roots, trunk, living stand or ring of independent needle leaves; organ outline generalized from limited textual support.', 'zh': '仅保存Schizoneura启发分节枝段浅浮雕器官，宽大成对裂叶鞘簇自然接节，置示意宿主板。无整株、根、树干、活体群落或独立针叶环；依据有限文字作器官基础概括。'}, 'tombolo': {'en': 'Original nominal18m landscape teaching patch: continuous mainland, low narrow sediment neck with two shorelines and an offshore island, surrounded by lower exposed bed. No elongated free-ended spit, water/lights exported, hydrodynamic simulation or measured real locality. Empty eras unspecified.', 'zh': '原创名义18米landscape教学片：连续大陆、双侧岸线低窄沉积细颈与离岸岛体，周围较低露床。非自由末端长沙嘴；不导出水灯、不模拟水动力、不指实测地点，空时代保持未指定。'}, 'entobia-sponge-boring-network': {'en': 'Original interpretive carbonate section exposing actual three-dimensional intersecting chamber voids and narrow connecting galleries. Section cut is educational; no random surface-hole decoration, wood-boring recolor, exact excavated specimen, species/age/locality or named producer. Hidden editable original void cutters remain source-only, not exported.', 'zh': '原创示意碳酸盐剖面，真实三维腔室空隙由细通道连通。教学剖切，非随机表孔装饰、木质钻孔换色或精确出土标本，不指定种、年代、地点或制造者。原创可编辑负形刀具留源场景不导出。'}}
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
