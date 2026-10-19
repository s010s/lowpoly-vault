# SPDX-License-Identifier: MIT
"""Original deterministic batch35 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import random,itertools
 from mathutils import Matrix,Euler
 rng=random.Random(3514);seeds=[]
 while len(seeds)<13:
  p=Vector(tuple(rng.uniform(-.83,.83) for _ in range(3)))
  if p.length>.95 or any((p-q).length<.54 for q in seeds):continue
  seeds.append(p)
 bounds=[(Vector(n),d) for n,d in [((1,0,0),.96),((-1,0,0),.90),((0,1,0),.91),((0,-1,0),.86),((0,0,1),.88),((0,0,-1),.90),((1,1,1),1.66),((-1,1,1),1.52),((1,-1,1),1.55),((-1,-1,1),1.60),((1,1,-1),1.49),((-1,1,-1),1.61),((1,-1,-1),1.56),((-1,-1,-1),1.43)]]
 vertices=[];edges=set()
 def gid(p):
  for i,q in enumerate(vertices):
   if (p-q).length<.0001:return i
  vertices.append(p.copy());return len(vertices)-1
 for cell,seed in enumerate(seeds):
  planes=bounds+[(other-seed,(other.length_squared-seed.length_squared)/2) for j,other in enumerate(seeds) if j!=cell]
  local=[]
  for ids in itertools.combinations(range(len(planes)),3):
   matrix=Matrix([planes[i][0] for i in ids])
   if abs(matrix.determinant())<1e-6:continue
   p=matrix.inverted()@Vector([planes[i][1] for i in ids])
   if any(n.dot(p)>d+.00001 for n,d in planes):continue
   if any((p-q[0]).length<.0001 for q in local):continue
   active={i for i,(n,d) in enumerate(planes) if abs(n.dot(p)-d)<.00003};local.append((p,active))
  for i,j in itertools.combinations(range(len(planes)),2):
   line=[p for p,active in local if i in active and j in active]
   if len(line)<2:continue
   a,b=max(itertools.combinations(line,2),key=lambda pair:(pair[0]-pair[1]).length_squared);ia,ib=gid(a),gid(b)
   if ia!=ib:edges.add(tuple(sorted((ia,ib))))
 used=set(i for e in edges for i in e);adj={i:set() for i in used}
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 reached=set();stack=[min(used)]
 while stack:
  a=stack.pop()
  if a in reached:continue
  reached.add(a);stack.extend(adj[a]-reached)
 assert reached==used
 rotation=Euler((.22,-.17,.31)).to_matrix()
 ps={i:rotation@Vector((vertices[i].x*.080,vertices[i].y*.068,vertices[i].z*.065)) for i in used}
 foam=Part('irregular-three-dimensional-open-cell-glass-strut-foam',m);radii={i:0 for i in used}
 for k,(a,b) in enumerate(sorted(edges)):
  pa,pb=ps[a],ps[b];r=.00095+.00025*(.5+.5*math.sin(k*1.71));direction=(pb-pa).normalized();bend=direction.cross(Vector((0,0,1)))
  if bend.length<.001:bend=direction.cross(Vector((0,1,0)))
  bend.normalize();mid=(pa+pb)/2+bend*.00065*math.sin(k*2.13)
  foam.tube([tuple(pa),tuple(mid),tuple(pb)],[r*1.10,r*.88,r*1.10],0,n=6);radii[a]=max(radii[a],r*1.15);radii[b]=max(radii[b],r*1.15)
 for i in sorted(used):
  p=ps[i];r=radii[i]*1.07;foam.ellipsoid(tuple(p),(r,r,r),0,n=8,rings=4)
 o=foam.finish(c,True);coords=[p.co for p in o.data.vertices];span=max(max(p[k] for p in coords)-min(p[k] for p in coords) for k in range(3));scale=.16/span
 for p in o.data.vertices:p.co*=scale
 return {'foam_structure':{'construction':'original clipped irregular3D Voronoi-edge foam; cell walls intentionally absent','seed_cells':len(seeds),'strut_edges':len(edges),'junction_nodes':len(used),'graph_connected_components':1,'void_scope':'large open cells interconnect through absent faces, including interior; no measured porosity or microscopic count claim','mesh_scope':'closed struts overlap rounded closed junction patches; continuous visible graph, not a single boolean-unioned watertight solid'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='reticulite-clast');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='reticulite-clast';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.54) for i,color in enumerate(['#76634a'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Volcanic glass clast concept; biomes/eras unspecified','habitat_zh':'火山玻璃碎块概念；原生境和时代未指定','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original three-dimensional irregular open-cell glass-strut foam with rounded continuous junctions and through-connected large voids, based on USGS basic reticulite definition. Original coarse13-cell construction is a visible teaching abstraction, not measured bubble count/porosity, exact specimen, deposit or eruption reconstruction. Entire interior is strut network, no opaque rock core or surface-only tafoni. Unequal cell spacing, gently bowed thin struts and restrained opaque brown glass impression; no industrial equal grid, copied model, transparency dependence or texture. Nominal0.16m largest span is art scale.','zh':'原创三维不规则开孔玻璃杆泡沫，圆润连续节点及互相贯通大孔依据USGS网状火山玻璃基本定义。原创粗化13泡单元构造为可见教学抽象，不是泡数/孔隙率测量、精确标本、矿床或喷发复原。内部全部为杆网，不含不透明岩核或仅表面蜂窝风化。泡孔间距不等、细杆微弯，克制不透明棕玻璃感；不是工业等距晶格，不复制模型，不依靠透明或贴图。0.16米最大名义展幅为美术尺度。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Reticulite open-glass-foam teaching clast','zh':'网状火山玻璃开孔泡沫教学碎块'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH35_COMPLETE',s)
if __name__=='__main__':main()
