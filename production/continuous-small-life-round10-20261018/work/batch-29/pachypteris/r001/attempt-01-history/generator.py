# SPDX-License-Identifier: MIT
"""Original deterministic batch29 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 stems=Part('original branched rachis of one preserved foliage organ',m);leaves=Part('shallow thick entire-margined blunt pinnules',m)
 curve_tube(stems,[(0,-.105,.004),(.002,-.035,.004),(0,.035,.004),(.001,.106,.004)],.00165,.00065,0,12,8)
 def pinnule(base,direction,L,W,index):
  direction=Vector(direction).normalized();side=Vector((-direction.y,direction.x,0));base=Vector(base);outline=[(0,0),(-.42,.13),(-.58,.42),(-.47,.78),(-.20,.96),(.18,1),(.48,.81),(.59,.43),(.43,.13)];n=len(outline)
  top=[tuple(base+side*x*W+direction*y*L+Vector((0,0,.00025+.00017*math.sin(pi*y)))) for x,y in outline];bottom=[tuple(base+side*x*W+direction*y*L+Vector((0,0,-.00035))) for x,y in outline];v=top+bottom+[tuple(base+direction*L*.49+Vector((0,0,.00105))),tuple(base+direction*L*.49+Vector((0,0,-.00048)))];f=[]
  for k in range(n):kk=(k+1)%n;f.extend([(k,n+k,n+kk,kk),(2*n,k,kk),(2*n+1,n+kk,n+k)])
  leaves.add(v,f,1 if index%7 else 2)
 count=0
 for j,yy in enumerate([-.073,-.038,-.003,.032,.067]):
  for sign in [-1,1]:
   span=.054*(1-.35*j/5);start=Vector((.001*math.sin(yy*30),yy,.004));end=Vector((sign*span,yy+.022,.004));mid=start.lerp(end,.5)+Vector((0,.002,.0004));curve_tube(stems,[tuple(start),tuple(mid),tuple(end)],.0010,.00038,0,9,5);direction=(end-start).normalized();normal=Vector((-direction.y,direction.x,0))
   for k in range(5):
    t=.15+.165*k;base=start.lerp(end,t)+Vector((0,.001*math.sin(pi*t),0));L=(.0107-.0024*k/4)*(1-.12*j/5)
    for side in [-1,1]:
     d=(normal*side*.92+direction*.40).normalized();pinnule(base,d,L,.0054-.0007*k/4,count);count+=1
   pinnule(end-direction*.0015,direction,.0090,.0046,count);count+=1
 # Conservative terminal pinnule at the leaf-axis tip; no root/trunk or extra plant organ.
 pinnule((.001,.102,.004),(0,1,0),.011,.005,1)
 stems.finish(c,True);leaves.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='pachypteris');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='pachypteris';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#8E937F', '#A6A58D', '#B2AF94'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Preserved terrestrial foliage organ; original biome unspecified','habitat_zh':'保存型陆生叶器官；原始biomes未指定','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Fossil-specimen foliage only: original branching rachis and thick entire-margined pinnules with shallow lenticular volume and blunt polygonal tips. Nominal0.22m organ span, conservative thickness, simplified veins and muted fossil palette are art choices, not original leaf color or new fossil measurements. Museum genus/specimen text consulted for basic foliage architecture; no exact named specimen replica, whole mother shrub/tree, roots, reproductive organ or newly associated habitat claimed. Original empty biome array retained; no prior frond mesh copied or simply thickened.','zh':'仅化石保存叶器官：原创分枝叶轴与厚全缘小羽片，具浅透镜状体积及钝多边叶尖。0.22米名义器官跨度、保守厚度、细脉简化及柔和化石色为美术设定，不是原叶色或新化石测量。博物馆属级/标本文本用于基本叶序依据；不复制具名标本，不推断母灌木/母树、根、生殖器官或新关联生境。保留原始biomes空数组，不复制旧蕨叶网格或仅加厚改名。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Pachypteris-inspired preserved thick-pinnule frond','zh':'Pachypteris 厚羽片保存叶器官'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH29_COMPLETE',s)
if __name__=='__main__':main()
