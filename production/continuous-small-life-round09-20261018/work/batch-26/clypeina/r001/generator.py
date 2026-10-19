# SPDX-License-Identifier: MIT
"""Original deterministic batch26 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 p=Part('two connected shallow fertile whorls only',m);n=88;nr=10
 for disc,(cx,cy,zz,R,tilt) in enumerate([(0,0,.009,.032,-.055),(.0014,.0005,.027,.036,.065)]):
  def radius(a,t):return .0060+(R*(1+.019*math.sin(7*a+.6)+.011*math.cos(13*a))-.0060)*t
  def height(a,t):return zz+.0115*t**.80+tilt*radius(a,t)*math.cos(a)+.00025*math.cos(16*a+.1)*math.sin(pi*t/2)**2
  v=[];f=[]
  for side in [0,1]:
   for j in range(nr):
    t=j/(nr-1)
    for k in range(n):
     a=2*pi*k/n;rr=radius(a,t);v.append((cx+rr*math.cos(a),cy+rr*math.sin(a),height(a,t)-side*.00145))
  layer=nr*n
  for j in range(nr-1):
   for k in range(n):
    a=j*n+k;b=j*n+(k+1)%n;f.extend([(a,a+n,b+n,b),(layer+a,layer+b,layer+b+n,layer+a+n)])
  for j in [0,nr-1]:
   for k in range(n):a=j*n+k;b=j*n+(k+1)%n;f.append((a,b,layer+b,layer+a))
  p.add(v,f,disc%2)
  # Restrained original radial surface organization; no discrete gear teeth.
  for k in range(16):
   a=2*pi*k/16;pts=[]
   for j in range(8):
    t=.12+.84*j/7;rr=radius(a,t);pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a),height(a,t)+.00004))
   p.tube(pts,[.00015+.00008*j/7 for j in range(8)],2,n=6)
 # Short hollow connector joins only the recorded pair; no unknown high axis.
 n=64;v=[];f=[]
 for inner in [False,True]:
  for j in range(5):
   t=j/4;cx=.0014*t;cy=.0005*t;rr=.0071 if not inner else .0051
   for k in range(n):a=2*pi*k/n;v.append((cx+rr*math.cos(a),cy+rr*math.sin(a),.0077+.021*t))
 off=5*n
 for j in range(4):
  for k in range(n):a=j*n+k;b=j*n+(k+1)%n;f.extend([(a,b,b+n,a+n),(off+a,off+a+n,off+b+n,off+b)])
 for j in [0,4]:
  for k in range(n):a=j*n+k;b=j*n+(k+1)%n;f.append((a,off+a,off+b,b))
 p.add(v,f,1);o=p.finish(c,True);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='clypeina');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='clypeina';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B5AD95', '#ADA58D', '#9E9D86'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Preserved marine algal organ-form specimen; no complete parent alga','habitat_zh':'保存的海生藻类轮盘标本；不复原完整母藻','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Fossil-specimen only: one connected pair of shallow funnel-like whorl discs, coarse radial divisions and a hollow short axial connection. Original limited thickness, small rim irregularity, muted fossil palette and nominal 0.075 m span are teaching art choices. No unknown tall stalk, sterile laterals, roots, complete parent thallus or mechanical gear/coin-stack substitution. No copied source models or figures; exact pore counts and microscopic wall anatomy are not claimed.','zh':'仅化石标本：一对相连浅漏斗状轮盘、粗放射分区与短中空轴连接。有限厚度、轻微不规则边缘、柔和化石色和0.075米名义跨度为教学美术设定。不添加未知高茎、不育轮枝、根或完整母藻，不用机械齿轮或硬币堆替代。不复制来源模型或图像；不主张精确孔数及微观壁结构。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Clypeina-inspired connected fertile-whorl specimen','zh':'Clypeina 相连繁殖轮盘标本'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH26_COMPLETE',s)
if __name__=='__main__':main()
