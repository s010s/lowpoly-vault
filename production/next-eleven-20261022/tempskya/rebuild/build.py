# Recovery-r001/c003: new local source derived from historical prepared build.py. No old geometry existed.
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
  ps=[Vector(p) for p in pts];vs=[];fs=[];mis=[];previous_u=None
  for j,p in enumerate(ps):
   d=(ps[min(j+1,len(ps)-1)]-ps[max(j-1,0)]).normalized()
   if previous_u is None:
    axes=[Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1))];axis=min(axes,key=lambda q:abs(q.dot(d)));u=d.cross(axis).normalized()
   else:u=(previous_u-d*previous_u.dot(d)).normalized()
   previous_u=u.copy();w=d.cross(u).normalized()
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
 matrix.add(v,f,0);ob=matrix.finish(c)
 for face in ob.data.polygons:
  if abs(face.normal.z)>.98:face.use_smooth=False
 roots=Mesh('interwoven-unequal-adventitious-root-cables-around-and-across-cut',m)
 for j in range(19):
  pts=[];n=13;a0=2*pi*j/19+.11*math.sin(j*2.3);twist=.32*(-1 if j%3 else 1);rad=.0031+.0010*(.5+.5*math.sin(j*2.1))
  for i in range(n):
   t=i/(n-1);a=a0+twist*t+.045*math.sin(t*pi*3+j);r=.155*(1+.045*math.sin(5*a+.8*t)+.03*math.cos(9*a-t))*(.98+.04*t)-rad*.42;pts.append((r*math.cos(a),r*.94*math.sin(a),.020+.276*t))
  roots.tube(pts,[rad*(1-.20*i/(n-1)) for i in range(n)],0,6)
 # Stem islands vary in size and lobing; they are filled tissues embedded in the root mat.
 islands=[(-.073,-.073,.021,.017),(-.020,-.096,.015,.012),(.047,-.071,.023,.018),(.096,-.016,.017,.022),(.046,.023,.025,.019),(-.008,-.026,.026,.021),(-.081,.006,.017,.021),(-.066,.080,.020,.016),(.001,.086,.017,.022),(.077,.078,.019,.014)]
 stems=Mesh('uneven-filled-small-stem-islands-inside-root-mat-cut-face',m)
 for j,(cx,cy,rx,ry) in enumerate(islands):
  vv=[];ff=[];n=24
  for ring,z in [(0,.275),(1,.3010),(2,.3028)]:
   for k in range(n):a=2*pi*k/n;lob=1+.12*math.sin(3*a+j*.7)+.035*math.cos(5*a-j);fac=.96 if ring==2 else 1;vv.append((cx+rx*lob*math.cos(a)*fac,cy+ry*lob*math.sin(a)*fac,z))
  for ring in range(2):
   for k in range(n):ff.append((ring*n+k,ring*n+(k+1)%n,(ring+1)*n+(k+1)%n,(ring+1)*n+k))
  for ring,rev in [(0,True),(2,False)]:
   ctr=len(vv);vv.append((cx,cy,.275 if ring==0 else .3028))
   for k in range(n):q=(ctr,ring*n+k,ring*n+(k+1)%n);ff.append(tuple(reversed(q)) if rev else q)
  stems.add(vv,ff,1)
 for j in range(32):
  pts=[];angle=j*2.399;delta=2.3+1.1*(.5+.5*math.sin(j*1.7));start=Vector((.145*math.cos(angle),.135*math.sin(angle),.299));end=Vector((.145*math.cos(angle+delta),.135*math.sin(angle+delta),.299))
  for i in range(25):
   t=i/24;p=start.lerp(end,t)
   p.x+=.016*math.sin(pi*t)*math.sin(t*pi*3+j*.8)
   p.y+=.013*math.sin(pi*t)*math.cos(t*pi*3+j*1.1)
   # Softly skirt islands; any lower relief beneath a filled stem remains embedded.
   for cx,cy,rx,ry in islands:
    d=Vector((p.x-cx,p.y-cy,0));dist=d.length;need=max(rx,ry)+.003
    if .0001<dist<need:p+=d*((need-dist)/dist)*.25
   p.z=.2991+.0015*math.sin(pi*t)+.0008*math.sin(j*.8+i*.8)*math.sin(pi*t)
   pts.append(tuple(p))
  roots.tube(pts,[.00135+.0004*math.sin(j*.9)**2]*25,0,5)
 roots.finish(c);ob=stems.finish(c)
 for face in ob.data.polygons:
  if abs(face.normal.z)>.98:face.use_smooth=False
 # New revision: recenter XY after source scale below; geometry remains original and fully closed.

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
   for v in o.data.vertices:
    v.co.z-=lo[2]
    v.co.x-=(lo[0]+hi[0])/2
    v.co.y-=(lo[1]+hi[1])/2
 brief=json.loads((a.config.parent/'brief.json').read_text());refs=json.loads((a.config.parent/'references.json').read_text());desc={'en':'Original evidence-informed stylized teaching form; nominal scale, palette and simplified counts are artistic. Static only; no exact species, location, locomotion or shared habitat reconstruction.','zh':'原创依据基础形态的风格化教学造型；名义尺度、配色及简化数量属美术选择。仅静态，不声称精确种、地点、运动机制或共同栖息地复原。'}
 descriptions={'belosaepia': {'en': 'Original Belosaepia-inspired internal-shell specimen only: a thick posterior body joins a long gently curved posterior prong and broad thin anterior shield/deck through one continuous shell volume. Relative thickness and outward flare are readable; microscopic chambers, soft cuttlefish, arms and inferred living body proportions are omitted. Nominal11cm, palette and presentation are artistic, not a copied fossil or exact species measurement.', 'zh': '原创Belosaepia启发内壳标本：厚后体、较长微弯后刺与前扩薄盾板/腹板为单一连续壳体，厚薄层次和外展可读。省微壳室，不补软体乌贼腕或生活比例。名义11厘米、配色与展示属美术，非化石复制或精确种级测量。'}, 'tempskya': {'en': 'Original Tempskya-inspired cut composite false-trunk specimen only: unequal rounded/lobed small stem islands are embedded in a dense root matrix, with interwoven cable-like root bands across the cut and outer side. Filled stem sections are larger than root strands, not concentric ordinary wood rings or punched holes. Nominal38cm, organ counts, cut relief and color are artistic; no living crown, leaves or whole fern inferred.', 'zh': '原创Tempskya启发切面复合假干标本：不等大圆/浅裂小茎岛包埋于密集根基质，切面与外侧有交织绳状根带，实心茎切面大于细根而非普通木纹同心圆孔。名义38厘米、数量裁面起伏与配色属美术，不推全株冠叶。'}, 'karst-sinkhole': {'en': 'Original nominal6m closed sinkhole teaching patch: a full surrounding surface funnels downward into a narrow throat and an enlarged underground cavity. An explicitly artificial front subsurface teaching cutaway reveals the connection while the above-ground funnel rim stays closed all around. Physical void and rock thickness, no painted black hole, water or lights; not a blocked spring mouth, measured site, collapse event, age or hydrological simulation.', 'zh': '原创名义6米封闭落水漏斗教学裁片：完整周缘地表真实下凹汇入窄喉并通向下部扩大的地下腔。明确人工前侧地下展示剖切露出连接，同时地表漏斗周缘保持闭合。真实空腔岩厚，非黑贴孔/泉口堵口，无水灯，不指实测地点塌陷事件年代或水文模拟。'}, 'fault-scarp': {'en': 'Original nominal8m interpretive offset-ground teaching exposure: the same gently shaped ground/channel marker and three comparable physical sediment layers are displaced across one planar scarp. Real high/low ground and cut-face layer relief remain readable in gray, not two detached painted stones. Crop faces and modest weathering are artistic; no actual earthquake, slip measurement, named site, age or stress direction asserted.', 'zh': '原创名义8米错移地面教学露面：同一缓起伏地面/浅槽标志及三层可对照实体沉积层跨一处平面阶坎发生错移，灰模真实高差和剖面层理可读，非两块贴色石。裁面与克制风化属美术，不指实际地震滑移测量地点年代应力方向。'}}
 desc=descriptions[slug]
 export_asset(slug,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata={'approved':False,'production_acceptance':'pending_independent_QA','historical_prepared_not_built':'preserved_original_r001','new_geometry_revision':'c003','revision':'recovery-r001','description':desc,'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s','third_party_assets_incorporated':False},'sources':refs['sources'],'nominal_scale':cfg['nominal_scale'],'representation':brief['subject']['representation'],'reconstruction_type':brief['subject']['reconstruction_type'],'animation_ready':False,'reference_status':'basic-form textual reference support with explicit limits; not strict reconstruction','publication_authority':'separate','candidate_validation_profile':'static-stylized-v1','generator':str(Path(__file__).relative_to(ROOT)),'build_config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()},output_root=a.output.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 generated=a.output.parent/slug
 if generated!=a.output:
  a.output.mkdir(parents=True,exist_ok=True)
  for f in generated.iterdir():f.rename(a.output/f.name)
  generated.rmdir();mp=a.output/'metadata.json';md=json.loads(mp.read_text());rel=str(a.output.relative_to(ROOT)) if a.output.is_relative_to(ROOT) else str(a.output);md.update(glb=rel+'/'+slug+'.glb',blend=rel+'/'+slug+'.blend',preview=rel+'/preview-hero.png');mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 mp=a.output/'metadata.json';md=json.loads(mp.read_text());facets=brief['catalog_facets'];md['catalog_facets']=facets;md['research_packs']=facets['packs'];md['packs']=[];md['pack_membership_status']='research-only; no published pack membership asserted'
 for key in ['worlds','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type']:md[key]=facets[key]
 md['scale_class']=json.loads((a.config.parent/'inventory-record.json').read_text())['scale_class'];md['collection']=facets['worlds'][0] if facets['worlds'] else None;mp.write_text(json.dumps(md,indent=2,ensure_ascii=False)+'\n')
 if a.preview:render_previews(c,a.output,tuple(cfg['required_views']),resolution=cfg['preview']['resolution'],samples=cfg['preview']['samples'],transparent=True)
if __name__=='__main__':main()
