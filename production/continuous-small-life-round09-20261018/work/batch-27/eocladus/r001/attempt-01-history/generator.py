# SPDX-License-Identifier: MIT
"""Original deterministic batch27 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 stem=Part('preserved narrow main axis segment without holdfast',m);curve_tube(stem,[(0,-.073,.002),(.001,-.025,.002),(0,.023,.002),(.0013,.074,.002)],.00145,.00143,0,12,10);stem.finish(c,True)
 p=Part('flattened multi-order cylindrical branchwork',m)
 lengths=[.012,.0090,.0059,.0036];radii=[.0010,.00072,.00049,.00032]
 def branch(start,angle,order,scale,phase):
  vec=Vector((math.cos(angle),math.sin(angle),0));tan=Vector((-math.sin(angle),math.cos(angle),0));L=lengths[order]*scale;end=start+vec*L;mid=start+vec*L*.5+tan*(.0006*math.sin(phase));pts=catmull([tuple(start),tuple(mid),tuple(end)],2);rr0=radii[order];rr1=rr0*.74;p.tube(pts,[rr0*(1-j/(len(pts)-1))+rr1*j/(len(pts)-1) for j in range(len(pts))],1 if order<2 else 2,n=7)
  if order<3:
   spread=.34 if order==0 else .42
   branch(end,angle-spread,order+1,scale*.96,phase+.8);branch(end,angle+spread,order+1,scale*.95,phase+1.6)
 for j,yy in enumerate([-.056,-.038,-.020,-.002,.016,.034,.051]):
  for sign in [-1,1]:
   x=.0006*math.sin(yy*40);angle=(.48 if sign>0 else pi-.48)+.055*math.sin(j*1.3);scale=.87+.10*math.sin((j+1)*.6);branch(Vector((x,yy,.002)),angle,0,scale,j*.7+(1 if sign>0 else 0))
 o=p.finish(c,True)
 # Preserved flat layout: limited conservative relief, no reconstructed out-of-plane growth.
 for obj in c.objects:
  if obj.type=='MESH':
   for v in obj.data.vertices:v.co.z=.002+(v.co.z-.002)*.45
   bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='eocladus');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='eocladus';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#8B927F', '#969E88', '#A7AD94'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Preserved marine algal branchwork specimen only; no complete living growth','habitat_zh':'仅保存型海生藻轴枝序标本；不复原完整生活藻体','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Fossil-specimen only: original flattened narrow axis segment carrying coarse-to-fine branched laterals through several orders. Limited teaching thickness, nominal0.16m span, muted gray-green fossil palette and simplified terminal counts are art choices. Primary genus description consulted for basic architecture; original inventory needs-specific-reference status retained. No named figure/specimen replica, unknown complete thallus, high extra stalk, holdfast, roots, reproductive bodies or out-of-plane growth asserted. Cylindrical segment character is expressed with softened limited relief.','zh':'仅化石标本：原创扁平窄轴片段，侧枝以粗细阶差表达数级分枝。有限教学厚度、0.16米名义跨度、柔和灰绿化石色及末枝数量简化为美术设定。已查阅属级原始描述支持基本枝序；保留原始needs-specific-reference状态。不宣称具名图/标本复制，不添加未知完整藻体、额外高茎、固着器、根、生殖体或离面生长。圆柱形分枝节段用柔和有限浮雕厚度表达。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Eocladus-inspired preserved multilevel algal branchwork','zh':'Eocladus 保存型复枝藻轴片段'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH27_COMPLETE',s)
if __name__=='__main__':main()
