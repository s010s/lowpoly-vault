# SPDX-License-Identifier: MIT
"""Original deterministic batch27 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 def left(y):return -.72+.20*math.sin(2.7*y+.4)+.025*math.sin(8*y)
 def right(y):return .56+.16*math.sin(2.3*y+.7)+.025*math.sin(7*y+.4)
 paths=[]
 for func in [left,right]:paths.append([(func(-1.22+2.44*j/40),-1.22+2.44*j/40) for j in range(41)])
 controls=[[(0,1.22,0),(-.10,.64,0),(-.12,.12,0),(left(-.50),-.50,0)],[(-1.65,.55,0),(left(.30),.30,0),(-.10,.02,0),(right(-.05),-.05,0),(1.65,.40,0)],[(-1.65,-.55,0),(left(-.30),-.30,0),(-.02,-.72,0),(right(-.62),-.62,0),(1.65,-.88,0)],[(right(.78),.78,0),(1.05,.80,0),(1.65,.90,0)]]
 for points in controls:paths.append([(a[0],a[1]) for a in catmull(points,7)])
 segments=[]
 for idx,pts in enumerate(paths):
  seg=[]
  for j in range(len(pts)-1):
   a=pts[j];bb=pts[j+1];dx=bb[0]-a[0];dy=bb[1]-a[1];seg.append((a[0],a[1],dx,dy,dx*dx+dy*dy,j/(len(pts)-1)))
  segments.append((seg,idx))
 def depth(x,y):
  bestdep=0
  for seg,idx in segments:
   best=1e9;prog=0
   for ax,ay,dx,dy,ll,t0 in seg:
    t=max(0,min(1,((x-ax)*dx+(y-ay)*dy)/ll));dd=(x-ax-t*dx)**2+(y-ay-t*dy)**2
    if dd<best:best=dd;prog=t0
   width=.067+.022*math.sin(8*prog+idx)+.009*math.cos(15*prog-idx);dep=(.295+.030*math.sin(4*prog+idx))*math.exp(-(best/(width*width))**2);bestdep=max(bestdep,dep)
  return bestdep
 nx=88;ny=62;v=[];faces=[]
 for j in range(ny+1):
  y0=-1.10+2.2*j/ny
  for i in range(nx+1):
   x0=-1.5+3*i/nx;x=x0*(.98+.02*math.cos(4*y0+.2));y=y0+.045*math.sin(3*x+.4)*abs(y0/1.10)**4
   top=.480+.020*math.sin(3.3*x+1.1*y)*math.sin(2.1*y)+.009*math.sin(11*x+2*y)*math.sin(9*y-x)+.006*x
   # Subordinate shallow dissolution pans; main drainage remains explicit fissure geometry.
   for xx,yy,rr in [(-1.18,.80,.13),(-.34,.52,.16),(.93,.54,.12),(.11,-.94,.15)]:top-=.018*math.exp(-((x-xx)**2+(y-yy)**2)/(rr*rr))
   z=top-depth(x,y);v.append((x,y,z))
 for j in range(ny):
  for i in range(nx):a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];bottom=[]
 for a in boundary:bottom.append(len(v));v.append((v[a][0],v[a][1],.004))
 center=len(v);v.append((0,0,.004))
 for k,a in enumerate(boundary):kk=(k+1)%len(boundary);faces.extend([(a,bottom[k],bottom[kk],boundary[kk]),(center,bottom[kk],bottom[k])])
 p=Part('three-metre gently worn limestone clints and connected deep grikes',m);p.add(v,faces,0);o=p.finish(c,True);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 extent=max(v.co.x for v in o.data.vertices)-min(v.co.x for v in o.data.vertices)
 for v in o.data.vertices:v.co.x*=3.0/extent

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='limestone-pavement');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='limestone-pavement';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#ABAD9B'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic karst teaching outcrop; original cave biome facet retained without a coastal-origin claim','habitat_zh':'通用喀斯特教学露头；保留原始cave分类，不主张海岸成因','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Geological-form artistic concept: representative three-metre-wide landscape outcrop with broad gently inclined limestone surfaces separated by deep continuous dissolution fissures. Unequal curved joint paths, softened shoulders and common lower rock express clints/grikes rather than industrial tiles, polygon columns or enlarged mud cracks. Nominal depth, spacing, crop thickness and gray palette are art choices, not a measured ancient site. Original biomes cave and scale_class landscape retained; no seawater erosion, mapped coastline, exact age or coexisting habitat claim.','zh':'地质形态艺术概念：三米宽代表性landscape露头，平缓宽岩面之间具有深而连通的溶蚀裂隙。不等宽曲折节理、柔化沟肩与共同下部岩体表达岩块/溶沟，区别于工业地砖、多边岩柱或放大泥裂。沟深、间距、截取厚度及灰色配色为美术设定，不是实测古地点。保留原始biomes cave及scale_class landscape，不主张海水侵蚀、海岸测绘、精确年代或共存生境。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Representative three-metre limestone pavement patch','zh':'三米代表性石灰岩溶沟石面'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH27_COMPLETE',s)
if __name__=='__main__':main()
