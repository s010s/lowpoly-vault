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

def belosaepia(c,m):
 shell=Mesh('original-continuous-pronged-internal-shell-thick-posterior-and-thin-front-deck',m);N=48;v=[];f=[]
 sections=[(-.092,.051,.0012,.0011),(-.087,.049,.0021,.0016),(-.079,.041,.0035,.0027),(-.068,.030,.0050,.0040),(-.055,.021,.0070,.0064),(-.044,.016,.010,.010),(-.032,.015,.015,.014),(-.018,.015,.022,.012),(-.004,.014,.029,.0075),(.012,.014,.034,.0045),(.029,.014,.037,.0028),(.046,.014,.034,.0022),(.060,.014,.027,.0018),(.071,.014,.017,.0015),(.078,.014,.006,.0013)]
 for j,(y,z,rx,rz) in enumerate(sections):
  for k in range(N):
   a=2*pi*k/N;co=math.cos(a);si=math.sin(a);shield=.0015*max(0,si)**5*math.sin(pi*j/(len(sections)-1))
   v.append((rx*co*(1+.012*math.sin(3*a)),y,z+rz*(.8*si+.2*si**3)+shield))
 for j in range(len(sections)-1):
  for k in range(N):f.append((j*N+k,(j+1)*N+k,(j+1)*N+(k+1)%N,j*N+(k+1)%N))
 for j,reverse in [(0,True),(len(sections)-1,False)]:
  center=len(v);y,z,rx,rz=sections[j];v.append((0,y,z))
  for k in range(N):q=(center,j*N+k,j*N+(k+1)%N);f.append(tuple(reversed(q)) if reverse else q)
 shell.add(v,f,0);shell.finish(c)

def tempskya(c,m):
 matrix=Mesh('dense-root-matrix-of-cut-composite-false-trunk-not-ordinary-log-rings',m);N=64;v=[];f=[]
 for j in range(7):
  t=j/6;z=.015+.285*t
  for k in range(N):
   a=2*pi*k/N;r=.155*(1+.045*math.sin(5*a+.8*t)+.03*math.cos(9*a-t))*(.98+.04*t)
   v.append((r*math.cos(a),r*.94*math.sin(a),z))
 for j in range(6):
  for k in range(N):f.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
 for j,rev in [(0,True),(6,False)]:
  center=len(v);v.append((0,0,.015+.285*j/6))
  for k in range(N):q=(center,j*N+k,j*N+(k+1)%N);f.append(tuple(reversed(q)) if rev else q)
 matrix.add(v,f,0);matrix.finish(c)
 roots=Mesh('interwoven-unequal-adventitious-root-cables-around-and-across-cut',m)
 for j in range(19):
  pts=[];n=17;a0=2*pi*j/19+.11*math.sin(j*2.3);twist=.32*(-1 if j%3 else 1);rad=.0031+.0010*(.5+.5*math.sin(j*2.1))
  for i in range(n):
   t=i/(n-1);a=a0+twist*t+.045*math.sin(t*pi*3+j);r=.157*(1+.035*math.sin(5*a+.8*t)+.03*math.cos(9*a-t));pts.append((r*math.cos(a),r*.94*math.sin(a),.016+.284*t))
  roots.tube(pts,[rad*(1-.20*i/(n-1)) for i in range(n)],0,8)
 # Stem islands vary in size and lobing; they are filled tissues embedded in the root mat.
 islands=[(-.073,-.073,.021,.017),(-.020,-.096,.015,.012),(.047,-.071,.023,.018),(.096,-.016,.017,.022),(.046,.023,.025,.019),(-.008,-.026,.026,.021),(-.081,.006,.017,.021),(-.066,.080,.020,.016),(.001,.086,.017,.022),(.077,.078,.019,.014)]
 stems=Mesh('uneven-filled-small-stem-islands-inside-root-mat-cut-face',m)
 for j,(cx,cy,rx,ry) in enumerate(islands):
  vv=[];ff=[];n=24
  for ring,z in [(0,.275),(1,.303),(2,.306)]:
   for k in range(n):a=2*pi*k/n;lob=1+.12*math.sin(3*a+j*.7)+.035*math.cos(5*a-j);fac=.96 if ring==2 else 1;vv.append((cx+rx*lob*math.cos(a)*fac,cy+ry*lob*math.sin(a)*fac,z))
  for ring in range(2):
   for k in range(n):ff.append((ring*n+k,ring*n+(k+1)%n,(ring+1)*n+(k+1)%n,(ring+1)*n+k))
  for ring,rev in [(0,True),(2,False)]:
   ctr=len(vv);vv.append((cx,cy,.275 if ring==0 else .306))
   for k in range(n):q=(ctr,ring*n+k,ring*n+(k+1)%n);ff.append(tuple(reversed(q)) if rev else q)
  stems.add(vv,ff,1)
 for j in range(17):
  pts=[];angle=j*2.399;start=Vector((.145*math.cos(angle),.135*math.sin(angle),.301));end=Vector((.145*math.cos(angle+1.7+.3*math.sin(j)),.135*math.sin(angle+1.7+.3*math.sin(j)),.301))
  for i in range(15):
   t=i/14;p=start.lerp(end,t);p.x+=.012*math.sin(pi*t)*math.cos(j);p.y+=.012*math.sin(pi*t)*math.sin(j)
   # Bend the root band around rather than through the diagnostic larger stem islands.
   for cx,cy,rx,ry in islands:
    d=Vector((p.x-cx,p.y-cy,0));dist=d.length;need=max(rx,ry)+.004
    if .0001<dist<need:d*=((need-dist)/dist)*.85;p+=d
   p.z=.3008+.0014*math.sin(j+i*.5);pts.append(tuple(p))
  roots.tube(pts,[.0018+.0005*math.sin(j*.9)**2]*15,0,8)
 roots.finish(c);stems.finish(c)

def revolved_profile(mesh,profile,angles,full=True,mat=0):
 v=[];f=[];inds=[];NA=len(angles)
 for r,z in profile:
  if r<1e-8:inds.append([len(v)]*NA);v.append((0,0,z));continue
  row=[]
  for a in angles:
   rr=r*(1+.018*math.sin(3*a)+.012*math.cos(5*a));row.append(len(v));v.append((rr*math.cos(a),rr*math.sin(a),z))
  inds.append(row)
 for j in range(len(profile)):
  jj=(j+1)%len(profile)
  for k in range(NA if full else NA-1):
   kk=(k+1)%NA;q=[inds[j][k],inds[j][kk],inds[jj][kk],inds[jj][k]];clean=[]
   for i in q:
    if i not in clean:clean.append(i)
   if len(clean)>=3:f.append(tuple(clean))
 if not full:
  f.extend([tuple(inds[j][0] for j in reversed(range(len(profile)))),tuple(inds[j][-1] for j in range(len(profile)))])
 mesh.add(v,f,mat)

def karst_sinkhole(c,m):
 roof=Mesh('full-closed-funnel-rim-descending-to-real-throat-in-continuous-rock',m)
 upper=[(3,.65),(2.75,.66),(2.38,.60),(2.03,.43),(1.68,.18),(1.34,-.09),(1.02,-.33),(.73,-.53),(.48,-.70),(.36,-.84),(.36,-.91),(3,-.91)]
 revolved_profile(roof,upper,[2*pi*k/96 for k in range(96)],True,0);roof.finish(c)
 section=Mesh('subsurface-expanded-cavity-connected-to-throat-front-teaching-cutaway',m)
 lower=[(3,-.91),(.36,-.91),(.43,-1.08),(.82,-1.25),(1.16,-1.52),(1.24,-1.93),(.99,-2.30),(.52,-2.55),(0,-2.64),(0,-2.95),(3,-2.95)]
 revolved_profile(section,lower,[pi*k/64 for k in range(65)],False,0);section.finish(c)

def fault_scarp(c,m):
 exposure=Mesh('comparable-strata-and-ground-marker-vertically-offset-across-one-fault-plane',m)
 def box(x0,x1,y0,y1,z0,z1,mat):
  vv=[(x,y,z) for z in [z0,z1] for y in [y0,y1] for x in [x0,x1]];ff=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(1,3,7,5),(3,2,6,7),(2,0,4,6)];exposure.add(vv,ff,mat)
 for side in [0,1]:
  x0,x1=(-4,0) if side==0 else (0,4);shift=1.05*side
  box(x0,x1,-3,3,0,.35+shift,0)
  for j in range(2):box(x0,x1,-3+.025*(j%2),3,.35+.40*j+shift,.75+.40*j+shift,j%2)
  # Both surfaces share a pre-offset shallow marker channel and quiet low relief.
  nx=32;ny=32;v=[];f=[]
  for j in range(ny+1):
   y=-3+6*j/ny
   for i in range(nx+1):
    x=x0+(x1-x0)*i/nx;cy=.35+.30*math.sin(x*.47);h=1.72+.10*math.sin(x*.6)+.07*math.cos(y*.5)-.23*math.exp(-((y-cy)/.32)**2);v.append((x,y,h+shift))
  for j in range(ny):
   for i in range(nx):a=j*(nx+1)+i;f.append((a,a+1,a+nx+2,a+nx+1))
  edge=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];off=len(v)
  for k in edge:x,y,z=v[k];v.append((x,y,1.15+shift))
  ctr=len(v);v.append(((x0+x1)/2,0,1.15+shift))
  for j,k in enumerate(edge):q=edge[(j+1)%len(edge)];f.append((k,off+j,off+(j+1)%len(edge),q));f.append((ctr,off+(j+1)%len(edge),off+j))
  exposure.add(v,f,0)
 exposure.finish(c,False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);random.seed(cfg['seed'])
 palettes={'belosaepia': [('original-preserved-internal-shell', '#B8AF97')], 'tempskya': [('dense-fossil-root-matrix', '#9D947E'), ('filled-larger-stem-cut-islands', '#B4AA91')], 'karst-sinkhole': [('continuous-soluble-rock-teaching-section', '#ADA894')], 'fault-scarp': [('original-offset-ground-and-strata', '#AAA38C'), ('comparable-sediment-marker-layer', '#B8AF98')]}
 mats=[make_material(name,color,roughness=.86) for name,color in palettes[slug]];globals()[slug.replace('-','_')](c,mats)
 from asset_common import _vertices_world,_bounds
 lo,hi=_bounds(_vertices_world(c));extent=max(hi[i]-lo[i] for i in range(3)) if slug in ['belosaepia','tempskya'] else hi[0]-lo[0];scale=cfg['nominal_scale']['meters']/extent
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
 descriptions={'belosaepia': {'en': 'Original Belosaepia-inspired internal-shell specimen only: a thick posterior body joins a long gently curved posterior prong and broad thin anterior shield/deck through one continuous shell volume. Relative thickness and outward flare are readable; microscopic chambers, soft cuttlefish, arms and inferred living body proportions are omitted. Nominal11cm, palette and presentation are artistic, not a copied fossil or exact species measurement.', 'zh': '原创Belosaepia启发内壳标本：厚后体、较长微弯后刺与前扩薄盾板/腹板为单一连续壳体，厚薄层次和外展可读。省微壳室，不补软体乌贼腕或生活比例。名义11厘米、配色与展示属美术，非化石复制或精确种级测量。'}, 'tempskya': {'en': 'Original Tempskya-inspired cut composite false-trunk specimen only: unequal rounded/lobed small stem islands are embedded in a dense root matrix, with interwoven cable-like root bands across the cut and outer side. Filled stem sections are larger than root strands, not concentric ordinary wood rings or punched holes. Nominal38cm, organ counts, cut relief and color are artistic; no living crown, leaves or whole fern inferred.', 'zh': '原创Tempskya启发切面复合假干标本：不等大圆/浅裂小茎岛包埋于密集根基质，切面与外侧有交织绳状根带，实心茎切面大于细根而非普通木纹同心圆孔。名义38厘米、数量裁面起伏与配色属美术，不推全株冠叶。'}, 'karst-sinkhole': {'en': 'Original nominal6m closed sinkhole teaching patch: a full surrounding surface funnels downward into a narrow throat and an enlarged underground cavity. An explicitly artificial front subsurface teaching cutaway reveals the connection while the above-ground funnel rim stays closed all around. Physical void and rock thickness, no painted black hole, water or lights; not a blocked spring mouth, measured site, collapse event, age or hydrological simulation.', 'zh': '原创名义6米封闭落水漏斗教学裁片：完整周缘地表真实下凹汇入窄喉并通向下部扩大的地下腔。明确人工前侧地下展示剖切露出连接，同时地表漏斗周缘保持闭合。真实空腔岩厚，非黑贴孔/泉口堵口，无水灯，不指实测地点塌陷事件年代或水文模拟。'}, 'fault-scarp': {'en': 'Original nominal8m interpretive offset-ground teaching exposure: the same gently shaped ground/channel marker and three comparable physical sediment layers are displaced across one planar scarp. Real high/low ground and cut-face layer relief remain readable in gray, not two detached painted stones. Crop faces and modest weathering are artistic; no actual earthquake, slip measurement, named site, age or stress direction asserted.', 'zh': '原创名义8米错移地面教学露面：同一缓起伏地面/浅槽标志及三层可对照实体沉积层跨一处平面阶坎发生错移，灰模真实高差和剖面层理可读，非两块贴色石。裁面与克制风化属美术，不指实际地震滑移测量地点年代应力方向。'}}
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
