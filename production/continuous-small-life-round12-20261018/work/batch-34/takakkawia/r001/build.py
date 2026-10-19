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

def takakkawia(c,m):
 cup=Mesh('continuous-conical-cup-eight-longitudinal-blade-fins-and-real-osculum',m);N=128;R=19;v=[];f=[];mi=[]
 for j in range(R):
  t=j/(R-1);z=.003+.147*t;body=.006+.025*t**.72+.004*t**5;wing=.001+.022*math.sin(t*pi*.5)**1.5
  for k in range(N):
   a=2*pi*k/N;d=((a+pi/8)%(pi/4))-pi/8;blade=math.exp(-(d/.055)**2);r=body+wing*blade;v.append((r*math.cos(a)+.003*t*t,r*math.sin(a),z+.0012*t*math.cos(a)))
 f.append(tuple(reversed(range(N))));mi.append(0)
 for j in range(R-1):
  for k in range(N):f.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k));mi.append(0)
 # Top rim connects to an actual inner cavity; wall/fin thickness is solid, not double-sided planes.
 for j in range(12):
  t=j/11;z=.149-.113*t;r=.028*(1-t)**.75+.003
  for k in range(N):a=2*pi*k/N;v.append((r*math.cos(a)+.003*(1-t)**2,r*math.sin(a),z+.0012*(1-t)*math.cos(a)))
 base=(R-1)*N
 for j in range(12):
  for k in range(N):f.append((base+j*N+k,base+j*N+(k+1)%N,base+(j+1)*N+(k+1)%N,base+(j+1)*N+k));mi.append(1)
 f.append(tuple(base+12*N+k for k in range(N)));mi.append(1);cup.add(v,f,mi);cup.finish(c)

def sabalites(c,m):
 leaf=Mesh('preserved-continuous-costapalmate-accordion-folded-lamina',m);costa=Mesh('unarmed-petiole-continuing-as-tapered-projecting-costa',m);N=104;R=14;v=[];f=[]
 # A connected lamina, with radial folds and marginal splits confined to distal sectors.
 for layer in [0,1]:
  for j in range(R):
   t=.055+.945*j/(R-1)
   for k in range(N+1):
    a=-1.95+3.9*k/N;u=k/N;edge=.315*(.88+.12*math.cos(a))*(1-.16*math.sin(pi*(k%4)/4)**2);radius=.018*(1-t)+edge*t;x=radius*math.sin(a);y=radius*math.cos(a)+.033*t*math.cos(a*.55);fold=.0085*math.cos(2*pi*k/4)*math.sin(t*pi*.70);z=.025+.021*t+.027*t*t*math.cos(a)+fold-.0018*layer;v.append((x,y,z))
 off=R*(N+1)
 for j in range(R-1):
  for k in range(N):
   q=(j*(N+1)+k,j*(N+1)+k+1,(j+1)*(N+1)+k+1,(j+1)*(N+1)+k);f.append(q);f.append(tuple(off+x for x in reversed(q)))
 boundary=list(range(N+1))+[j*(N+1)+N for j in range(1,R)]+[(R-1)*(N+1)+k for k in range(N-1,-1,-1)]+[j*(N+1) for j in range(R-2,0,-1)]
 for i,a in enumerate(boundary):b=boundary[(i+1)%len(boundary)];f.append((a,off+a,off+b,b))
 # Parametric angular/radial ordering has negative Z normal, reverse shell consistently.
 leaf.add(v,[tuple(reversed(q)) for q in f]);leaf.finish(c,False)
 pts=smooth_path([(0,-.155,.015),(0,-.045,.022),(0,.070,.046),(.003,.175,.061),(.007,.28,.071)],26);costa.tube(pts,[.0058*(1-i/28)**.78+.0005 for i in range(26)],1,n=12);costa.finish(c)

def river_dominated_delta(c,m):
 terrain=Mesh('continuous-land-and-bed-birdfoot-delta-with-projecting-distributary-lobes-no-water',m);nx=72;ny=62;v=[];f=[]
 paths=[[(0,9),(.2,6),(-.15,3.5),(0,2.2)],[(0,2.8),(-1.5,1.2),(-3.2,-1),(-5.8,-4.4),(-6.4,-5.1)],[(0,2.8),(.3,.2),(-.6,-2.7),(-.3,-5.8),(.2,-7.4)],[(0,2.2),(2,.5),(3.4,-1.5),(5.3,-3.8),(6.1,-4.6)],[(3.2,-1.3),(4.4,-.5),(6.5,-1.1),(7.5,-2.1)]]
 def nearest(x,y,path):
  best=(1e9,0)
  for j,(a,b) in enumerate(zip(path,path[1:])):
   dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));d=math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
   if d<best[0]:best=(d,(j+t)/(len(path)-1))
  return best
 def height(x,y):
  h=.19+1.05/(1+math.exp(-max(-30,min(30,(y-2.8)/.5))))
  ds=[]
  for p,path in enumerate(paths):
   d,t=nearest(x,y,path);width=(1.25-.48*t) if p else 1.5;ridge=(.94-.26*t)*math.exp(-(d/width)**4);h=max(h,.19+ridge);ds.append((d,t,p))
  cut=0
  for d,t,p in ds:cut=max(cut,(.43 if p else .61)*math.exp(-(d/(.30+.10*t if p else .48))**4))
  return max(.12,h-cut)
 for j in range(ny+1):
  y=-9+18*j/ny
  for i in range(nx+1):x=-10+20*i/nx;v.append((x,y,height(x,y)))
 for j in range(ny):
  for i in range(nx):a=j*(nx+1)+i;f.append((a,a+1,a+nx+2,a+nx+1))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];off=len(v)
 for a in boundary:x,y,z=v[a];v.append((x,y,0))
 for j,a in enumerate(boundary):b=boundary[(j+1)%len(boundary)];f.append((a,off+j,off+(j+1)%len(boundary),b))
 f.append(tuple(reversed([off+j for j in range(len(boundary))])));terrain.add(v,f);terrain.finish(c,False)

def asteriacites_resting_impression(c,m):
 slab=Mesh('single-continuous-sediment-slab-negative-central-body-and-five-spreading-arm-impressions',m);N=180;v=[(0,0,.011)];f=[]
 arms=[(-pi/2,.097),(-.21,.089),(1.00,.095),(2.18,.083),(3.42,.091)]
 def outline(a):
  vals=[]
  for b,length in arms:
   d=abs((a-b+pi)%(2*pi)-pi);vals.append(.023+(length-.023)*math.exp(-(d/.165)**2))
  return max(vals)
 rings=[(.32,.0105),(.68,.0108),(.90,.0124),(1.,.0160),(1.12,.0230),(1.38,.0240)]
 for t,z in rings:
  for k in range(N):a=2*pi*k/N;r=outline(a)*t;v.append((r*math.cos(a),r*math.sin(a),z))
 for k in range(N):f.append((0,1+k,1+(k+1)%N))
 for j in range(len(rings)-1):
  for k in range(N):a=1+j*N+k;b=1+j*N+(k+1)%N;f.append((a,b,b+N,a+N))
 off=len(v)
 for k in range(N):a=2*pi*k/N;r=.14/(abs(math.cos(a))**8+abs(math.sin(a))**8)**.125;v.append((r*math.cos(a),r*math.sin(a),.024))
 for k in range(N):a=1+(len(rings)-1)*N+k;b=1+(len(rings)-1)*N+(k+1)%N;f.append((a,b,off+(k+1)%N,off+k))
 bot=len(v)
 for k in range(N):x,y,z=v[off+k];v.append((x,y,0))
 for k in range(N):f.append((off+k,bot+k,bot+(k+1)%N,off+(k+1)%N))
 f.append(tuple(reversed([bot+k for k in range(N)])));slab.add(v,f);slab.finish(c,False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'takakkawia': [('quiet-continuous-cup-and-eight-fins', '#B9A387'), ('actual-oscular-cavity-wall', '#968B76')], 'sabalites': [('preserved-folded-leaf-lamina', '#9A9C76'), ('petiole-to-extended-costa', '#ACAA85')], 'river-dominated-delta': [('continuous-delta-sediment-land-and-bed', '#AAA68B')], 'asteriacites-resting-impression': [('single-sediment-negative-trace', '#B2AA94')]}
 mats=[make_material(name,color,roughness=.86) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=(hi[2]-lo[2]) if slug=='takakkawia' else hi[0]-lo[0];scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'takakkawia': {'en': 'Original Takakkawia-inspired elongate conical cup with eight continuous longitudinal radial blade-like fins, an externally flared oscular rim and a real central cavity. Original integrated wall construction, no random inserted plates; basic form only, not microscopic spicules, exact soft tissue or feeding reconstruction.', 'zh': '原创Takakkawia启发长锥杯，八条连续纵向放射翼与外张口缘及真实中央腔；杯壁与纵翼整体连续，非随机插板。仅基础形态，不承诺微骨针、精确软体或取食复原。'}, 'sabalites': {'en': 'Preserved Sabalites-inspired costapalmate leaf organ only: unarmed petiole continues as a tapering costa into a continuous folded fan lamina, with conservative thickness and limited distal splitting. No trunk, whole palm crown, associated flowers/fruits or modern shoreline species reconstruction. Primary search-result text supports basic form; inaccessible full text and unseen source pixels remain explicit.', 'zh': '仅保存Sabalites启发具中肋掌状叶器官：无刺叶柄延续为渐细叶内中肋、连续折褶扇叶与克制末端分裂。无树干、整冠、未关联花果或现代岸边物种复原；基础形态依原始搜索摘要，全文访问限制与源图未阅明确保留。'}, 'river-dominated-delta': {'en': 'Original nominal20m landscape teaching patch with a river trunk splitting into connected distributary channels and raised sediment lobes projecting beyond a coast into lower exposed bed. Original bird-foot architecture, not an enlarged estuary or random ditch layout. Only land/sediment exported, no water/lights, tide/flow simulation or precise mapped paleosite; empty eras remain unspecified.', 'zh': '原创名义20米landscape教学片：主河分为连通分流道，隆起沉积叶瓣伸出岸线进入较低露床。独立鸟足状构造，不放大旧河口或随机加沟。只导出土地沉积物，无水灯、潮汐水流模拟或精确古地点测图；空时代保持未指定。'}, 'asteriacites-resting-impression': {'en': 'Original interpretive negative Asteriacites-inspired resting impression in one continuous sediment slab: shallow central body recess and five spreading tapering arm traces with real gray-readable depth. No black star decal, living sea-star mesh, exact excavated specimen or identified producer species. Negative-impression polarity deliberately retained from the frozen brief.', 'zh': '原创示意Asteriacites启发凹陷停栖迹：连续沉积板中浅中央体区与五条展开渐细腕迹，灰模有真实深度。非黑星贴图、活海星网格或精确出土标本，不指定制造者；保持冻结brief的原凹印极性。'}}
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
