# SPDX-License-Identifier: MIT
"""Original deterministic batch29 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 axes=Part('connected creeping freshwater branch units',m);leaves=Part('overlapping small scale fronds in two alternate ranks',m)
 def unit(points,steps,L=.0047):
  pts=catmull(points,5);axes.tube(pts,[.00072*(1-j/(len(pts)-1))+.00030*j/(len(pts)-1) for j in range(len(pts))],0,n=7)
  for j in range(steps*2):
   t=.08+.84*j/max(1,steps*2-1);idx=min(len(pts)-2,int(t*(len(pts)-1)));center=Vector(pts[idx]);direction=(Vector(pts[idx+1])-Vector(pts[max(0,idx-1)])).normalized();side=Vector((-direction.y,direction.x,0)).normalized()
   for sign in [(-1 if j%2==0 else 1)]:
    cen=center+side*sign*.0012+direction*(.0007 if sign>0 else -.0004);outline=[(-.0017,-.0019),(-.0020,-.0003),(-.0016,.0014),(-.0007,.0023),(.0006,.0025),(.0017,.0016),(.0021,.0001),(.0014,-.0018)]
    # Broad overlapping dorsal lobe with shallow closed lower surface, no large Salvinia leaf pair.
    base=[tuple(cen+side*x+direction*y*1.40+Vector((0,0,-.00025))) for x,y in outline];upper=[tuple(cen+side*x*.83+direction*y*1.40*.83+Vector((0,0,.00055))) for x,y in outline];v=base+upper+[tuple(cen+Vector((0,0,.0009)))];f=[tuple(reversed(range(8)))]
    for k in range(8):kk=(k+1)%8;f.extend([(k,kk,8+kk,8+k),(16,8+k,8+kk)])
    leaves.add(v,f,1 if (j+(sign>0))%5 else 2)
 unit([(0,-.050,.020),(.001,0,.020),(-.001,.050,.020)],20)
 for j,yy in enumerate([-.032,-.016,0,.016,.032]):
  for sign in [-1,1]:
   span=.034*(1-.19*abs(j-2)/2);unit([(0,yy,.020),(sign*span*.48,yy+.006,.0205),(sign*span,yy+.016,.020)],7)
 axes.finish(c,True);leaves.finish(c,True)
 roots=Part('restrained submerged root hints',m)
 for j in range(6):
  y=-.037+j*.014;curve_tube(roots,[(0,y,.019),(.0015*math.sin(j),y+.001,.011),(.003*math.sin(j+.5),y+.003,.0035+.001*(j%2))],.00039,.00013,0,6,4)
 roots.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='azolla');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='azolla';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#819276', '#99A785', '#A9B18F'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Freshwater wetland floating fern only; not marine vegetation','habitat_zh':'仅淡水湿地浮生水蕨；不是海生植被','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living whole-organism inspired-by teaching mat: connected creeping branches carry overlapping small scale fronds in two alternate ranks, with restrained submerged root hints. Nominal0.12m patch, muted green palette, shallow lobe thickness and density are art choices; this is one composition, not a density variant count. Basic modern genus architecture and fossil specimen context consulted; original needs-specific-reference status retained. No claim that all ancient species details, exact sporocarps or microanatomy are verified, no marine tolerance or coexistence claim, and no copied Salvinia geometry.','zh':'原创全体inspired-by教学浮垫：连续匍匐分枝具两列互生重叠小叶瓦，辅以克制水下根提示。0.12米名义片区、柔和绿色、浅叶瓣厚度及密度为美术设定；只计一种构图，不靠密度变体增数。已查阅现代属级基本结构与化石标本背景，保留原始needs-specific-reference状态。不主张所有古种细节、精确孢子囊或微观解剖均已验证，不声称海水耐受或共存关系，不复制Salvinia几何。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Azolla-inspired scale-leaved freshwater floating mat','zh':'Azolla 满江红类淡水叶瓦浮垫'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH29_COMPLETE',s)
if __name__=='__main__':main()
