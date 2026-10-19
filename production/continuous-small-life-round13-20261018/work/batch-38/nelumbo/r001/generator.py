# SPDX-License-Identifier: MIT
"""Original deterministic batch38 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # A closed shallow leaf impression-relief, no support slab or inferred complete plant.
 n=96;nr=22;v=[(-.004,.002,.005)];f=[]
 def shape(r,a):
  edge=1+.035*math.sin(3*a+.4)+.018*math.sin(7*a-1)
  x=.12*r*edge*math.cos(a);y=.111*r*edge*math.sin(a)
  # Broad unequal low folded sectors, never a deep fluted flower or notched lily leaf.
  z=.006+.003*r+.0025*r*r*math.sin(5*a+.7)+.0011*r*math.sin(9*a-.3)-.002*math.exp(-(r/.12)**2)
  return (x-.004*(1-r),y+.002*(1-r),z)
 for j in range(1,nr+1):
  for k in range(n):v.append(shape(j/nr,2*pi*k/n))
 for k in range(n):f.append((0,1+k,1+(k+1)%n))
 for j in range(nr-1):
  for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,a+n,b+n,b))
 bottom=len(v);v.append((0,0,.001));off=len(v)
 for k in range(n):
  q=shape(1,2*pi*k/n);v.append((q[0],q[1],q[2]-.0028))
 for k in range(n):
  kk=(k+1)%n;a=1+(nr-1)*n+k;b=1+(nr-1)*n+kk;f.append((a,b,off+kk,off+k));f.append((bottom,off+k,off+kk))
 p=Part('Shallow peltate leaf relief',m);p.add(v,f,0);p.finish(c,True)
 # Low radial vein relief joins a small central attachment scar; no elongate midrib.
 p=Part('Broad radial venation and attachment scar',m)
 for k in range(13):
  a=2*pi*k/13+.035*math.sin(k*1.7);pts=[]
  for j in range(15):
   r=.07+.87*j/14;ang=a+.035*math.sin(pi*r)*math.sin(k);q=shape(r,ang);pts.append((q[0],q[1],q[2]+.00025))
  p.tube(pts,[.00028+.0006*(1-j/14) for j in range(15)],1,5)
 p.ellipsoid((-.004,.002,.005),(.0032,.003,.0008),1,14,5);p.finish(c,True)
 obs=[o for o in c.objects if o.type=='MESH'];coords=[v.co for o in obs for v in o.data.vertices];scale=.24/max(max(p[i] for p in coords)-min(p[i] for p in coords) for i in range(3))
 for o in obs:
  for v in o.data.vertices:v.co*=scale

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='nelumbo');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='nelumbo';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#9c9475', '#afa385'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Detached freshwater-associated fossil leaf concept','habitat_zh':'独立淡水相关化石叶概念','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original detached peltate fossil-leaf shallow relief, with near-central attachment scar, broad radial sectors and gently uneven circular edge. Rib count, folds, fossil palette and0.24m span are art choices. No flower, seed pod, root, whole plant or exact modern species reconstruction.','zh':'原创独立盾状化石叶浅浮雕，近中央着生痕、宽放射叶区及轻微起伏圆缘可读。叶脉数、浅折、化石配色及0.24米尺寸属美术选择；无花、莲蓬、根、整株或精确现代种复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Nelumbo peltate leaf specimen','zh':'Nelumbo 古莲叶'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH36_COMPLETE',s)
if __name__=='__main__':main()
