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

def selkirkia(c,m):
 sheath=Mesh('continuous-tapered-sheath-with-two-real-openings-and-solid-wall',m);N=32;R=30;v=[];f=[];mi=[]
 def sec(t):return (.00035*math.sin(pi*t),-.010+.035*t,.005-.0015*t,.0047*(1-t)+.0018*t)
 for inside in [False,True]:
  for j in range(R):
   t=j/(R-1);x,y,z,rad=sec(t);rad*=1+.012*math.sin(18*pi*t)
   if inside:rad-=.00053
   for k in range(N):a=2*pi*k/N;v.append((x+rad*math.cos(a),y,z+rad*.91*math.sin(a)))
 off=R*N
 for j in range(R-1):
  for k in range(N):
   a=j*N+k;b=j*N+(k+1)%N;q=(a,b,b+N,a+N);f.append(q);mi.append(0);f.append(tuple(off+i for i in reversed(q)));mi.append(1)
 for j in [0,R-1]:
  for k in range(N):a=j*N+k;b=j*N+(k+1)%N;f.append((a,off+a,off+b,b));mi.append(0)
 sheath.add(v,f,mi);sheath.finish(c)
 worm=Mesh('worm-centred-with-clearance-inside-sheath-no-wall-penetration',m)
 sections=[]
 for j in range(48):
  t=j/47;y=-.025+.052*t;x=.00018*math.sin(pi*t);z=.005-.0015*max(0,(y+.010)/.035);rad=(.00265*(1-t)+.00048*t)*(1+.025*math.sin(30*pi*t));sections.append((x,y,z,rad,rad*.86))
 ellipse_loft(worm,sections,24,2);worm.finish(c)
 rings=Mesh('restrained-blunt-ring-teeth-on-exposed-introvert-only',m)
 for row,y in enumerate([-.0244,-.0227,-.0210]):
  for k in range(10):
   a=2*pi*(k+.5*(row%2))/10;rad=.0024;pos=(rad*math.cos(a),y,.005+rad*.86*math.sin(a));rings.ellipsoid(pos,(.00032,.00034,.00030),3,n=8,r=5)
 rings.finish(c)

def dicroidium(c,m):
 stem=Mesh('preserved-foliage-basal-Y-rachis-only',m);leaf=Mesh('one-consistent-elongate-entire-pinnule-form-on-both-arms',m)
 base=smooth_path([(0,-.25,.002),(0,-.19,.0028),(.003,-.12,.003)],15);stem.tube(base,[.0045-.0014*i/14 for i in range(15)],0,n=10)
 for side in [-1,1]:
  p=smooth_path([(.003,-.125,.003),(side*.050,-.025,.0035),(side*.105,.105,.003),(side*.137,.240,.002)],36);stem.tube(p,[.0034*(1-.85*i/35) for i in range(36)],0,n=10)
  for j in range(13):
   t=.085+.065*j;idx=min(34,round(t*35));q=p[idx];d=(p[min(35,idx+1)]-p[max(0,idx-1)]).normalized();v=Vector((-d.y,d.x,0));L=.057*(math.sin(pi*(.12+.83*t))**.65)*(1-.26*t)
   for flank in [-1,1]:
    # All original blades use one narrow oblong-lanceolate entire margin, slight alternating offset.
    start=q+d*(.0025 if flank==1 else -.0025);direction=(v*flank*.90+d*.38).normalized();leaf_blade(leaf,start,direction,L*(1+.05*side*flank),L*.19,.0008,1)
 stem.finish(c);leaf.finish(c)

def waterfall_plunge_pool(c,m):
 terrain=Mesh('connected-deep-plunge-basin-undercut-rockstep-and-upstream-bed-no-water',m);nx=64;ny=38;v=[];f=[]
 def recess(x):return .60*math.exp(-(x/1.85)**4)
 def under_y(x):return 1.20+recess(x)
 def pool_h(x,y):
  r=((x/1.95)**2+((y+.05)/1.75)**2)**.5
  bowl=1.63*math.exp(-(r**3.5));rim=2.08+.075*math.sin(x*.78+y*.3);return rim-bowl
 # Foreground bank/basin sheet joins the physically recessed cliff foot.
 for j in range(ny+1):
  t=j/ny
  for i in range(nx+1):x=-4+8*i/nx;y=-3.2+(under_y(x)+3.2)*t;v.append((x,y,pool_h(x,y)))
 for j in range(ny):
  for i in range(nx):a=j*(nx+1)+i;f.append((a,a+1,a+nx+2,a+nx+1))
 prev=[ny*(nx+1)+i for i in range(nx+1)]
 # Actual receding lower wall, projecting lip, and high upstream platform; no colored water patch.
 for row in range(1,7):
  cur=[]
  for i in range(nx+1):
   x=-4+8*i/nx;u=under_y(x);foot=pool_h(x,u);lip=1.04+.09*math.sin(x*.9)
   if row==1:y=u+.06;z=foot+.40
   elif row==2:y=u+.04;z=2.65+.04*math.sin(x)
   elif row==3:y=lip;z=3.10+.035*math.sin(x)
   elif row==4:y=lip-.025;z=3.30+.035*math.sin(x)-.17*math.exp(-(x/.67)**4)
   elif row==5:y=2.1;z=3.40+.04*math.sin(x)-.17*math.exp(-(x/.67)**4)
   else:y=3.2;z=3.47+.035*math.sin(x)-.17*math.exp(-(x/.67)**4)
   cur.append(len(v));v.append((x,y,z))
  for i in range(nx):f.append((prev[i],prev[i+1],cur[i+1],cur[i]))
  prev=cur
 rows=ny+7;boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,rows)]+[(rows-1)*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(rows-2,0,-1)];off=len(v)
 for i in boundary:x,y,z=v[i];v.append((x,y,0))
 center=len(v);v.append((0,0,0))
 for j,a in enumerate(boundary):b=boundary[(j+1)%len(boundary)];f.append((a,off+j,off+(j+1)%len(boundary),b));f.append((center,off+(j+1)%len(boundary),off+j))
 terrain.add(v,f,0);terrain.finish(c,True)

def cave_boxwork(c,m):
 rock=Mesh('finite-attached-eroded-cave-rock-display-face',m);walls=Mesh('thin-intersecting-residual-mineral-fins-irregular-planar-cells',m)
 N=48;vs=[];fs=[]
 for z,t in [(0,1),(.034,1.01),(.055,.98)]:
  for k in range(N):a=2*pi*k/N;x=.325*math.copysign(abs(math.cos(a))**.48,math.cos(a));y=.235*math.copysign(abs(math.sin(a))**.48,math.sin(a));vs.append((x*t,y*t,z+(.006*math.sin(x*15+y*7) if z else 0)))
 bot=len(vs);vs.append((0,0,0));top=len(vs);vs.append((0,0,.055))
 for k in range(N):fs.extend([(bot,(k+1)%N,k),(2*N+k,2*N+(k+1)%N,top)])
 for j in range(2):
  for k in range(N):fs.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
 rock.add(vs,fs,0);rock.finish(c,False)
 # Original unequal vein-partition plan. Shared boundaries are deduplicated; broad cells open above the same eroded face.
 seeds=[(-.27,-.18),(-.12,-.19),(.045,-.18),(.22,-.16),(-.24,-.045),(-.055,-.055),(.115,-.025),(.265,.005),(-.265,.12),(-.12,.115),(.035,.135),(.21,.17),(-.015,.015)]
 def clip(poly,A,B,C):
  out=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   dp=A*p[0]+B*p[1]+C;dq=A*q[0]+B*q[1]+C
   if dp<=1e-10:out.append(p)
   if (dp<=0)!=(dq<=0):t=dp/(dp-dq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  return out
 edges={}
 for i,(x,y) in enumerate(seeds):
  poly=[(-.295,-.205),(.295,-.205),(.295,.205),(-.295,.205)]
  for j,(xx,yy) in enumerate(seeds):
   if i!=j:poly=clip(poly,xx-x,yy-y,(x*x+y*y-xx*xx-yy*yy)/2)
  for p,q in zip(poly,poly[1:]+poly[:1]):
   if math.dist(p,q)<.006:continue
   key=tuple(sorted([tuple(round(t,6) for t in p),tuple(round(t,6) for t in q)]));edges[key]=(Vector((*p,0)),Vector((*q,0)))
 for ei,(p,q) in enumerate(edges.values()):
  d=(q-p).normalized();lat=Vector((-d.y,d.x,0));n=5;ww=.0023+.0012*(.5+.5*math.sin(ei*2.13));vv=[];ff=[]
  for j in range(n):
   t=j/(n-1);a=p.lerp(q,t);height=.102+.022*math.sin(a.x*13+a.y*7)+.010*math.sin(a.y*25-ei*.3);lean=lat*(.004*math.sin(ei))
   vv.extend([tuple(a-lat*ww+Vector((0,0,.043))),tuple(a+lat*ww+Vector((0,0,.043))),tuple(a+lat*ww*.64+lean+Vector((0,0,height))),tuple(a-lat*ww*.64+lean+Vector((0,0,height)))])
  ff.extend([(3,2,1,0),tuple((n-1)*4+k for k in range(4))])
  for j in range(n-1):
   for k in range(4):ff.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
  walls.add(vv,ff,1)
 walls.finish(c,False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'selkirkia': [('unmineralized-organic-sheath', '#A99A7B'), ('real-inner-sheath-wall', '#8D846B'), ('soft-worm-introvert', '#B6A894'), ('restrained-blunt-radial-spines', '#C5B7A3')], 'dicroidium': [('preserved-foliage-rachis', '#8B816A'), ('single-pinnule-form-fossil-organ', '#9B927B')], 'waterfall-plunge-pool': [('continuous-bedrock-surface', '#A29B86')], 'cave-boxwork': [('residual-eroded-host-rock', '#9B947F'), ('thin-resistant-mineral-fracture-fins', '#B5AA8F')]}
 mats=[make_material(name,color,roughness=.86) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=(hi[1]-lo[1]) if slug=='selkirkia' else (max(hi[0]-lo[0],hi[1]-lo[1]) if slug=='dicroidium' else hi[0]-lo[0]);scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'selkirkia': {'en': 'Original Selkirkia-inspired static teaching animal: a slightly tapering unmineralized sheath has real wall thickness and two open ends. A continuous worm remains inside with radial clearance; only its anterior ring-toothed introvert and a small posterior end project beyond the openings. Sparse blunt ring teeth, color, size and posture are artistic, not exact count, calcium shell or locomotion claims.', 'zh': '原创Selkirkia启发静态教学动物：略渐细非矿化鞘管有真实壁厚及双端开口；连续虫体在管内留径向间隙，前部环齿吻和少量后端从开口伸出。稀疏钝齿、配色尺度姿态属美术概括，非精确计数/钙壳/运动机制。'}, 'dicroidium': {'en': 'Original Dicroidium-inspired preserved foliage-frond organ only, with a basal Y rachis and two coherent pinnule-bearing arms. One consistent entire oblong-lanceolate pinnule form is used throughout; nominal span and shallow three-dimensional relief are artistic. No fertile organ, whole parent plant, roots, mixed taxa, Umkomasia or Pteruchus added. The frozen brief pose contains an inherited fertile-fragment template phrase; it is explicitly inapplicable to this foliage-only model and metadata.', 'zh': '原创Dicroidium启发保存营养叶器官：基部Y叉叶轴连贯双臂带单一类型的全缘长椭圆披针形小羽片；名义尺度和浅三维起伏为美术。无育性器官/整株/根系/混杂分类群/Umkomasia或Pteruchus。冻结brief姿态保留历史fertile-fragment模板，明确不适用于本仅叶器官模型和文案。'}, 'waterfall-plunge-pool': {'en': 'Original nominal8m representative bedrock teaching patch: a deep rounded plunge basin lies directly below a recessed lower rock step and projecting lip, joined to continuous banks and an upstream bed. The undercut and basin have actual geometry and spatial connection; no blue water sheet, enlarged isolated pothole, old ledge recolor, flow simulation or measured locality/event. Only bedrock exported; landscape scale retained.', 'zh': '原创名义8米床岩教学裁片：深圆潭紧位于下部后退掏蚀岩阶与突出缘下方，连续接岸坡与上游床面；掏蚀和深潭为实际相连几何。非蓝片/孤立壶穴放大/旧瀑台换色，无流体模拟或实测地点事件；仅床岩导出，保留landscape尺度。'}, 'cave-boxwork': {'en': 'Original cave-boxwork teaching exposure: thin intersecting mineral fins with real thickness form irregular open cells attached to one finite eroded rock face, with unequal heights and residual-rock thickness hierarchy. The generic speleogen concept represents more resistant fracture filling exposed by host erosion, not ordinary dripping stalagmite growth, an equal grid, detached panels or a three-dimensional reticulite foam. Nominal65cm patch, mineral palette and display face are artistic; no cave locality or microcrystal claim.', 'zh': '原创洞穴箱状构造教学露面：有真实厚度的相交薄矿物片围成不规则开放格室，附着有限蚀退岩面，高度与残岩厚度分层。示意裂隙填充物较抗蚀后外露的speleogen，非滴水石笋/等距格网/漂浮板片/三维reticulite泡沫；名义65厘米、矿物配色及展示面属美术，不指定洞址微晶。'}}
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
