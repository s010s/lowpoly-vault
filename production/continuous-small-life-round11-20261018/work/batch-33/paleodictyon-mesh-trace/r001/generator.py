# SPDX-License-Identifier: MIT
"""Original deterministic batch33 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 substrate=Part('quiet-sediment-slab-exposed-fossil-relief-face',m)
 outline=[(-.110,-.120,.0065),(.098,-.120,.0065),(.117,-.108,.0065),(.120,-.075,.0065),(.119,.093,.0065),(.103,.119,.0065),(.055,.120,.0065),(-.099,.118,.0065),(-.120,.103,.0065),(-.120,-.092,.0065)]
 substrate.sheet(outline,.013,0,axis=(0,0,1));substrate.finish(c,False)
 graph=Part('thin-connected-hexagonal-positive-tube-relief',m);side=.024;nodes={};edges=set();cells=[]
 def key(x,y):return (round(x,10),round(y,10))
 for q in range(-2,3):
  for r in range(-2,3):
   if max(abs(q),abs(r),abs(q+r))>2:continue
   cx=1.5*side*q;cy=math.sqrt(3)*side*(r+q/2);cell=[]
   for k in range(6):
    a=2*pi*k/6;p=key(cx+side*math.cos(a),cy+side*math.sin(a));nodes[p]=p;cell.append(p)
   cells.append(cell)
   for k,p in enumerate(cell):edges.add(tuple(sorted([p,cell[(k+1)%6]])))
 assert len(cells)==19 and len(nodes)==54 and len(edges)==72
 for a,b in sorted(edges):
  pts=[]
  for k in range(3):
   t=k/2;x=a[0]*(1-t)+b[0]*t;y=a[1]*(1-t)+b[1]*t;z=.0142+.00010*math.sin(22*x+17*y);pts.append((x,y,z))
  graph.tube(pts,[.0015]*3,0,n=8)
 for x,y in sorted(nodes):
  z=.0142+.00010*math.sin(22*x+17*y);graph.ellipsoid((x,y,z),(.00160,.00160,.00150),0,n=8,rings=5)
 graph.finish(c,True)
 return {'trace_display':'raised-fossil-relief','trace_graph':{'original_layout':'axial hexagonal patch, radius2cells; not copied specimen','cells':len(cells),'nodes':len(nodes),'edges':len(edges),'independent_closed_cycles':len(edges)-len(nodes)+1,'geometry_note':'Closed tubes overlap restrained junction patches and substrate for continuous visible positive relief. Graph connectivity does not assert a single boolean-unioned watertight mesh.'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='paleodictyon-mesh-trace');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='paleodictyon-mesh-trace';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#969696'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Marine trace-morphology teaching concept; producer unresolved','habitat_zh':'海生潜迹形态教学概念；制造者未确定','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original raised-fossil-relief teaching slab: a low connected thin tube network forms19 closed hexagonal cells on an exposed substrate. Basic hexagonal tunnel architecture and unresolved producer supported by the accessed primary study Introduction; modern surface openings are not copied into this fossil-relief display. Original nominal0.24m module, tube thickness, grid extent and gray palette are art choices. No exact ichnospecies, excavated specimen replica, coral/honeycomb organism, proven farming/ventilation mechanism or producer assignment; original Paleogene inventory context is not a universal range or coexistence claim.','zh':'原创凸起化石浮雕教学岩板：低矮相连细管网在露面基底上形成19个闭合六角单元。已读原始研究引言支持六角管网基本结构及制造者未确定；不将现代海底表面小孔照搬作本项化石浮雕。原创0.24米名义模块、管厚、网格范围及灰色为美术设定。不指定潜迹种，不复制出土标本，不作珊瑚或蜂巢生物，不主张已证实的耕作、通风机制或制造者；原始古近纪分类背景不代表完整时代范围或共存。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Paleodictyon raised hexagonal mesh teaching relief','zh':'Paleodictyon 六角网格凸起教学浮雕'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH33_COMPLETE',s)
if __name__=='__main__':main()
