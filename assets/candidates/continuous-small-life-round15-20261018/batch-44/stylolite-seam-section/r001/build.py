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

def yochelcionella(c,m):
 shell=Mesh('single-continuous-compressed-curved-cap-and-subapical-open-tube-wall',m);N=48;R=21;v=[];f=[];mi=[]
 for inside in [False,True]:
  for j in range(R):
   t=j/(R-1)*.965;rx=.0058*(1-t)**.82+.00015;ry=.0106*(1-t)**.64+.00015;yc=.0045*t*t;z=.016*t
   if inside:rx*=.87;ry*=.90;z*=.95
   growth=1+.008*math.cos(12*pi*t)
   for k in range(N):a=2*pi*k/N;v.append((rx*growth*math.cos(a),yc+ry*growth*math.sin(a),z))
 off=R*N
 # Remove corresponding four-by-four wall patches. Their exact boundary loops become the joined tube walls.
 j0,j1,k0,k1=10,14,34,38
 for inside in [False,True]:
  offset=off if inside else 0
  for j in range(R-1):
   for k in range(N):
    if j0<=j<j1 and k0<=k<k1:continue
    q=(offset+j*N+k,offset+j*N+(k+1)%N,offset+(j+1)*N+(k+1)%N,offset+(j+1)*N+k);f.append(tuple(reversed(q)) if inside else q);mi.append(1 if inside else 0)
  top=len(v);v.append((0,.0045,.016*(.95 if inside else 1)))
  for k in range(N):q=(offset+(R-1)*N+k,offset+(R-1)*N+(k+1)%N,top);f.append(tuple(reversed(q)) if inside else q);mi.append(1 if inside else 0)
 for k in range(N):f.append((k,off+k,off+(k+1)%N,(k+1)%N));mi.append(0)
 border=[j0*N+k for k in range(k0,k1+1)]+[j*N+k1 for j in range(j0+1,j1+1)]+[j1*N+k for k in range(k1-1,k0-1,-1)]+[j*N+k0 for j in range(j1-1,j0,-1)];B=len(border);ends=[]
 for inside in [False,True]:
  inds=[i+(off if inside else 0) for i in border];base=[Vector(v[i]) for i in inds];center=sum(base,Vector())/B;prev=inds
  axis=Vector((0,-.94,.34)).normalized();u=Vector((1,0,0));vv=axis.cross(u).normalized()
  for row in range(1,9):
   t=row/8;ctr=center.lerp(Vector((0,-.0105,.0132)),t);rad=(.00155*(1-t)+.00128*t)*(.64 if inside else 1);cur=[]
   for k in range(B):
    a=5*pi/4+2*pi*k/B;circle=ctr+u*(rad*math.cos(a))+vv*(rad*math.sin(a));q=base[k].lerp(circle,min(1,t*3.0));cur.append(len(v));v.append(tuple(q))
   for k in range(B):q=(prev[k],prev[(k+1)%B],cur[(k+1)%B],cur[k]);f.append(tuple(reversed(q)) if inside else q);mi.append(1 if inside else 0)
   prev=cur
  ends.append(prev)
 for k in range(B):f.append((ends[0][k],ends[0][(k+1)%B],ends[1][(k+1)%B],ends[1][k]));mi.append(0)
 used=sorted({i for face in f for i in face});mapping={old:new for new,old in enumerate(used)};v=[v[i] for i in used];f=[tuple(mapping[i] for i in face) for face in f]
 shell.add(v,f,mi);shell.finish(c)

def joffrea(c,m):
 shoot=Mesh('preserved-longshoot-shortshoot-junction-with-attached-fruit-stalks',m);fruits=Mesh('one-mature-twisted-follicle-bearing-state-no-detached-seeds-or-leaves',m)
 p=smooth_path([(-.014,-.078,.005),(0,-.025,.006),(.005,.025,.006),(.013,.075,.006)],32);shoot.tube(p,[.0037*(1-.5*i/31) for i in range(32)],0,n=12)
 spur=smooth_path([(.003,-.005,.006),(.018,.003,.007),(.027,.018,.009),(.030,.029,.010)],16);shoot.tube(spur,[.0030*(1-.30*i/15) for i in range(16)],0,n=12)
 specs=[((.027,.017,.009),(.058,-.007,.011),.033,.0048),((.029,.023,.010),(.073,.024,.014),.041,.0055),((.030,.028,.010),(.065,.057,.013),.037,.0049),((.026,.014,.008),(.041,-.027,.010),.034,.0045),((.030,.030,.010),(.036,.080,.011),.039,.0051)]
 for j,(attach,tip,L,W) in enumerate(specs):
  start=Vector(attach);end=Vector(tip);d=(end-start).normalized();ped=start+d*.008;shoot.tube(smooth_path([start,ped],6),[.00135*(1-.28*i/5) for i in range(6)],0,n=10)
  u=Vector((-d.y,d.x,0)).normalized();path=smooth_path([tuple(ped),tuple(ped+d*L*.42+u*(.003*(-1 if j%2 else 1))+Vector((0,0,.003))),tuple(ped+d*L+u*.002)],20);verts=[];faces=[];N=16
  for i,p in enumerate(path):
   t=i/19;tangent=(path[min(19,i+1)]-path[max(0,i-1)]).normalized();lat=Vector((-tangent.y,tangent.x,0)).normalized();normal=tangent.cross(lat).normalized();w=.00060+W*(math.sin(pi*t)**.75)*(1-.22*t)
   for k in range(N):
    a=2*pi*k/N;groove=1-.16*math.exp(-(min(a,2*pi-a)/.30)**2);verts.append(tuple(p+lat*(w*math.cos(a)*groove)+normal*(w*.53*math.sin(a))))
  faces.append(tuple(reversed(range(N))));faces.append(tuple(19*N+k for k in range(N)))
  for i in range(19):
   for k in range(N):faces.append((i*N+k,i*N+(k+1)%N,(i+1)*N+(k+1)%N,(i+1)*N+k))
  fruits.add(verts,faces,1)
 shoot.finish(c);fruits.finish(c)

def oxbow_lake_basin(c,m):
 terrain=Mesh('continuous-floodplain-mainriver-and-separate-horseshoe-abandoned-channel-no-water',m);nx=76;ny=66;v=[];f=[]
 R=4.2;theta=.65;cx=-2.4;ends=[Vector((cx+R*math.cos(theta),s*R*math.sin(theta))) for s in [-1,1]]
 def h(x,y):
  plain=1.84+.08*math.sin(.30*x+.17*y)+.05*math.cos(.3*y);river=3.0+.22*math.sin(y*.34);main_depth=1.37*math.exp(-((x-river)/.82)**4)
  ang=math.atan2(y,x-cx);rad=math.hypot(x-cx,y)
  if abs(ang)>=theta:dist=abs(rad-R)
  else:dist=min(math.hypot(x-p.x,y-p.y) for p in ends)
  # Closed sediment necks separate both old-channel ends from the current river.
  old_depth=1.20*math.exp(-(dist/.72)**2);near_end=min(math.hypot(x-p.x,y-p.y) for p in ends);old_depth*=1-.24*math.exp(-(near_end/.80)**2)
  return plain-max(main_depth,old_depth)
 for j in range(ny+1):
  y=-7.5+15*j/ny
  for i in range(nx+1):x=-9+18*i/nx;v.append((x,y,h(x,y)))
 for j in range(ny):
  for i in range(nx):a=j*(nx+1)+i;f.append((a,a+1,a+nx+2,a+nx+1))
 edge=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];off=len(v)
 for i in edge:x,y,z=v[i];v.append((x,y,0))
 center=len(v);v.append((0,0,0))
 for j,i in enumerate(edge):q=edge[(j+1)%len(edge)];f.append((i,off+j,off+(j+1)%len(edge),q));f.append((center,off+(j+1)%len(edge),off+j))
 terrain.add(v,f,0);terrain.finish(c)

def stylolite_seam_section(c,m):
 profile=[(-.275,.150),(-.245,.150),(-.238,.175),(-.225,.179),(-.215,.173),(-.207,.208),(-.192,.205),(-.185,.135),(-.158,.128),(-.154,.156),(-.143,.156),(-.139,.143),(-.121,.144),(-.115,.095),(-.087,.101),(-.082,.176),(-.065,.184),(-.060,.172),(-.043,.174),(-.034,.216),(-.016,.212),(-.010,.147),(.012,.150),(.016,.162),(.027,.165),(.033,.139),(.053,.141),(.060,.109),(.078,.111),(.085,.178),(.103,.182),(.109,.168),(.125,.168),(.131,.195),(.147,.194),(.154,.128),(.177,.125),(.184,.155),(.198,.150),(.208,.179),(.220,.176),(.229,.147),(.249,.149),(.255,.140),(.275,.142)]
 N=len(profile);NY=7;gap=.00145
 for upper in [False,True]:
  rock=Mesh(('upper' if upper else 'lower')+'-rock-with-real-complementary-unequal-dissolution-teeth-extending-into-depth',m);v=[];f=[]
  for layer in [0,1]:
   for j in range(NY):
    y=(-.075+.165*j/(NY-1)) if upper else (-.09+.18*j/(NY-1))
    for x,z in profile:
     seam=z+.004*math.sin(24*y+9*x)+.003*math.cos(14*y-13*x)
     zz=(seam+(gap if upper else -gap)) if layer==0 else (.315 if upper else 0)
     v.append((x,y,zz))
  off=N*NY
  for layer in [0,1]:
   for j in range(NY-1):
    for i in range(N-1):a=layer*off+j*N+i;f.append((a,a+1,a+N+1,a+N))
  edge=list(range(N))+[j*N+N-1 for j in range(1,NY)]+[(NY-1)*N+i for i in range(N-2,-1,-1)]+[j*N for j in range(NY-2,0,-1)]
  for j,a in enumerate(edge):b=edge[(j+1)%len(edge)];f.append((a,b,off+b,off+a))
  rock.add(v,f,1 if upper else 0);rock.finish(c,False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'yochelcionella': [('original-preserved-cap-shell', '#B5AA91'), ('real-shell-inner-wall', '#9F9884')], 'joffrea': [('preserved-attached-shoot-and-stalk', '#8E8068'), ('mature-follicle-organ', '#A3977F')], 'oxbow-lake-basin': [('continuous-exposed-land-and-abandoned-channel-bed', '#A9A28A')], 'stylolite-seam-section': [('lower-solid-pressure-solution-contact-rock', '#AEA58F'), ('upper-complementary-contact-rock', '#B9AF98')]}
 mats=[make_material(name,color,roughness=.86) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=max(hi[0]-lo[0],hi[1]-lo[1],hi[2]-lo[2]) if slug in ['yochelcionella','joffrea'] else hi[0]-lo[0];scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'yochelcionella': {'en': 'Original Yochelcionella-inspired preserved shell only: a tall laterally compressed curved cap with an obliquely rising subapical tube, modeled as one continuous wall with a real open tube mouth and shell aperture. No borrowed Clavagella/Haplophrentis geometry, soft body, foot or respiratory-mechanism claim. Nominal22mm cap/tube span, quiet color and economical growth relief are artistic; viewer magnification is separate from real source units.', 'zh': '原创Yochelcionella启发保存壳：较高侧扁弯帽体、壳顶下斜上升管口为单一连续实壁，有真实管口和帽壳开口。不借Clavagella/Haplophrentis网格，不加软体足或断言呼吸机制。名义22毫米壳管跨度、配色及简化生长起伏属美术，viewer展示放大与源米制分开。'}, 'joffrea': {'en': 'Original Joffrea-inspired attached reproductive-shoot specimen only: long/short-shoot junction with several naturally stalked elongate follicles, all represented in one mature twisted-infructescence teaching state supported at abstract/caption level. Shallow geometric follicle sutures, nominal18cm span, count, color and relief are artistic. No whole parent/tree crown, unassociated leaves, loose seeds, seedlings or mixed maturity states added; unrelated inherited Onoclea source is not a diagnostic Joffrea fruit proof.', 'zh': '原创Joffrea启发附果枝标本：长短枝交界与数枚自然果柄相接的长蓇葖，统一采用摘要/图注可支持的成熟扭曲果序教学阶段。几何浅缝、名义18厘米、数量配色与起伏属美术；无整株树冠/未关联叶/散落种子/幼苗/混成熟态，继承Onoclea来源不当作Joffrea果形专证。'}, 'oxbow-lake-basin': {'en': 'Original nominal18m representative floodplain land/bed patch: a current through-river is separate from a horseshoe-shaped abandoned depressed channel. Both old-channel ends close into sediment/land necks, with real basin/bank relief and no water or lights exported. Generic cutoff/infill teaching concept, not a bent estuary, elongated plunge pool, measured river event/site/age, complete watershed or hydrodynamic simulation; landscape scale and original river facet preserved.', 'zh': '原创名义18米泛滥平原土地床面裁片：贯通现主河与马蹄废槽相互分离，旧槽两端由沉积陆颈封闭，凹地岸坡真实几何，无水体灯光导出。通用截弯填淤教学概念，非河口改弯/深潭拉长，不作实测河流事件地点年代/完整流域/水动力模拟，保留landscape尺度与原river生境。'}, 'stylolite-seam-section': {'en': 'Original nominal55cm interpretive rock cut-section: opposing solid rock surfaces have complementary irregular primary and secondary dissolution teeth extending into depth along a continuous narrow seam. The actual interlocking interface and deliberately legible display gap remain readable in gray; no black painted zigzag, random fracture pile, measured stress/pressure direction or locality asserted. Cut outer faces are teaching section boundaries, not an added display plinth.', 'zh': '原创名义55厘米教学岩体裁切剖面：两侧实岩沿连续窄缝以不规则主次溶蚀齿互补嵌合，齿面真实入体；真实互锁界面与为可读性适度夸张的展示细缝在灰模可见。非黑色锯齿贴线/随机碎裂堆，不推定实测应力压力方向地点；外裁面为教学剖切边界，不另加展示底座。'}}
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
