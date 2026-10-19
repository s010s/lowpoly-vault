# SPDX-License-Identifier: MIT
"""Original deterministic batch40 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 p=Part('Single attached fertile branch system in shallow relief',m);curve_tube(p,[(0,-.080,.002),(-.001,-.036,.0025),(.003,.014,.0028),(0,.072,.0025)],.0018,.0007,0,9,7)
 sacs=Part('Attached compressed rounded sporangia clusters',m)
 for i in range(4):
  for sign in [-1,1]:
   y=-.005+i*.019+(0 if sign<0 else .005);length=.035-i*.005;start=Vector((.002,y,.0025));end=Vector((sign*length,y+.026-i*.002,.0025));curve_tube(p,[tuple(start),tuple(start.lerp(end,.5)+Vector((0,-.001,0))),tuple(end)],.0012,.00055,0,7,5)
   tangent=(end-start).normalized();perp=Vector((-tangent.y,tangent.x,0))
   for k in range(6):
    u=.22+.14*k;pos=start.lerp(end,u);offset=perp*((-1 if k%2 else 1)*.0032);center=pos+offset;curve_tube(p,[tuple(pos),tuple(center)],.0006,.00055,0,6,2)
    radius=.00265*(1-.20*u);sacs.ellipsoid((center.x,center.y,.003),(radius,radius*.94,.00145),1,12,6)
 # Small terminal fertile continuation belongs to the same axis, not a detached vegetative leaf.
 for k in range(4):
  y=.065+k*.004;sign=-1 if k%2 else 1;center=(sign*.0025,y,.003);curve_tube(p,[(0,y,.0025),center],.00055,.0005,0,6,2);sacs.ellipsoid(center,(.002,.0019,.0012),1,12,6)
 p.finish(c,True);sacs.finish(c,True)
 obs=[o for o in c.objects if o.type=='MESH'];coords=[v.co for o in obs for v in o.data.vertices];scale=.16/max(max(p[i] for p in coords)-min(p[i] for p in coords) for i in range(3))
 for o in obs:
  for v in o.data.vertices:v.co*=scale

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='botrychium');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='botrychium';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#756e5d', '#a09172'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Detached terrestrial fossil fertile fragment','habitat_zh':'独立陆生化石育性残片','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'One original fertile branch fragment in shallow compression relief: elongated basal axis, acute fertile branches and attached alternating rounded sporangia. Counts, pose, fossil palette and0.16m span are art choices. No unattached sterile frond, root, whole fern or exact modern species reconstruction; no microscopic spores inferred.','zh':'一件原创浅压型育性残片：长基轴、锐角育性分枝及连续着生的交替圆孢子囊。数量、姿态、化石配色及0.16米跨度属美术选择，不拼未相连营养叶、根或整株，不作精确现代种或显微孢子复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Botrychium fertile-frond specimen','zh':'Botrychium 阴地蕨类化石'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH40_COMPLETE',s)
if __name__=='__main__':main()
