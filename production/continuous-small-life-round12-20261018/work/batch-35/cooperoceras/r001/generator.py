# SPDX-License-Identifier: MIT
"""Original deterministic batch35 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def hollow_loft(part,points,radii,n=16,cavity=8):
 pts=[Vector(p) for p in points];v=[];f=[];frames=[];u=Vector((0,1,0))
 for j,p in enumerate(pts):
  d=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized();u=u-d*u.dot(d)
  if u.length<.001:u=d.cross(Vector((0,0,1)))
  if u.length<.001:u=d.cross(Vector((1,0,0)))
  u.normalize();w=d.cross(u).normalized();frames.append((u.copy(),w))
  for k in range(n):v.append(tuple(p+radii[j]*(u*math.cos(2*pi*k/n)+w*math.sin(2*pi*k/n))))
 f.append(tuple(reversed(range(n))))
 for j in range(len(pts)-1):
  for k in range(n):a=j*n+k;b=j*n+(k+1)%n;f.append((a,b,b+n,a+n))
 start=len(pts)-cavity;off=len(v)
 for j in range(start,len(pts)):
  u,w=frames[j];r=max(radii[j]*.60,radii[j]-.0011 if n==20 else radii[j]-.00028)
  for k in range(n):v.append(tuple(pts[j]+r*(u*math.cos(2*pi*k/n)+w*math.sin(2*pi*k/n))))
 for j in range(cavity-1):
  for k in range(n):a=off+j*n+k;b=off+j*n+(k+1)%n;f.append((a,a+n,b+n,b))
 f.append(tuple(off+k for k in range(n)))
 for k in range(n):
  a=(len(pts)-1)*n+k;b=(len(pts)-1)*n+(k+1)%n;ia=off+(cavity-1)*n+k;ib=off+(cavity-1)*n+(k+1)%n;f.append((a,b,ib,ia))
 part.add(v,f,0)
def generate(c,m):
 coil=Part('original-expanding-open-coil-and-real-shell-aperture',m);pts=[];radii=[];N=100
 def center(t):
  a=.35+2*pi*1.36*t;r=.007+.046*t**1.05
  return Vector((r*math.cos(a),-.012*max(0,(t-.91)/.09)**2,.065+r*math.sin(a)))
 for j in range(N+1):
  t=j/N;pts.append(tuple(center(t)));radii.append(.0022+.0075*t**.8)
 hollow_loft(coil,pts,radii,20,12);coil.finish(c,True)
 horns=Part('paired-recurved-hollow-shell-spines',m)
 for t in [.54,.69,.83,.95]:
  a=.35+2*pi*1.36*t;rad=Vector((math.cos(a),0,math.sin(a)));tan=Vector((-math.sin(a),0,math.cos(a)));base=center(t);size=.75+.30*t
  for sign in [-1,1]:
   lateral=Vector((0,sign,0));p=[base+rad*.0045+lateral*.005,base+rad*.013*size+lateral*.014*size,base+rad*.022*size+lateral*.029*size-tan*.004,base+rad*.024*size+lateral*.040*size-tan*.014]
   path=catmull([tuple(x) for x in p],4);rs=[.0035*(1-j/(len(path)-1))**1.15+.0008*j/(len(path)-1) for j in range(len(path))]
   hollow_loft(horns,path,rs,10,4)
 horns.finish(c,True)
 # One metric art scale for shell+horns, preserving proportions and physical dimensions.
 objs=[o for o in c.objects if o.type=='MESH'];coords=[p.co for o in objs for p in o.data.vertices];span=max(max(p[k] for p in coords)-min(p[k] for p in coords) for k in range(3));factor=.17/span
 for o in objs:
  for p in o.data.vertices:p.co*=factor

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='cooperoceras');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='cooperoceras';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#b1a28b'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Preserved nautiloid shell only; original biomes remain unspecified','habitat_zh':'仅保存鹦鹉螺类壳体；原biomes未指定保持不扩写','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original fossil-shell specimen: expanding open coil, real terminal aperture with conservative shallow interior, and four simplified pairs of outward recurved hollow shell spines with flared roots. NPS named Cooperoceras paragraph consulted for basic shell/spine form; count, local pose, palette and nominal0.17m shell+horn span are art choices. Hidden chambers and microscopic sutures simplified, no copied shell mesh, attached fruit, living animal, tentacles, foot or behavioral reconstruction.','zh':'原创化石壳体标本：渐扩开放盘卷、具保守浅内腔的真实末端壳口，四组成对外弯中空壳角以宽根自然衔接。NPS具名Cooperoceras段落仅支持基本壳角结构；组数、局部姿态、配色及0.17米名义壳角总展幅为美术设定。简化隐藏气室与微缝合线，不复制壳网格、不粘接果实，不恢复活体、触手、足或行为。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Cooperoceras horned coiled preserved-shell teaching specimen','zh':'Cooperoceras 长角盘卷保存壳体教学标本'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH35_COMPLETE',s)
if __name__=='__main__':main()
