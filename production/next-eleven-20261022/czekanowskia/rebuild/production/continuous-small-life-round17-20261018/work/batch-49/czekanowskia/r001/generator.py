# SPDX-License-Identifier: MIT
"""Original deterministic batch49 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 p=Part('Compact preserved short shoot',m);fol=Part('Solid dichotomous narrow leaf ribbons',m)
 curve_tube(p,[(0,-.020,.003),(0,-.010,.004),(.001,0,.005)],.003,.0018,0,n=10,steps=4)
 # Each closed ribbon has two genuine open fork valleys and four tips, not needles painted on a plane.
 shape=[(-.012,0),(-.013,.34),(-.151,.65),(-.291,1.00),(-.269,1.008),(-.135,.697),(-.109,.995),(-.087,.994),(-.117,.655),(-.024,.404),(.026,.405),(.118,.657),(.090,.982),(.112,.984),(.140,.698),(.265,.972),(.287,.962),(.151,.644),(.013,.34),(.012,0)]
 for j,(angle,length) in enumerate([(-.71,.118),(-.35,.143),(.03,.151),(.40,.138),(.78,.112)]):
  ca=math.cos(angle);sa=math.sin(angle);outline=[]
  for u,v in shape:
   xx=length*(u*ca+v*sa);yy=length*(-u*sa+v*ca);z=.004+.004*math.sin(v*pi)*math.cos(j*.8)+.0008*j*v
   outline.append((xx,yy,z))
  fol.sheet(outline,.00065,1+j%2,axis=(0,0,1))
 for j in range(5):
  a=2*pi*j/5;p.ellipsoid((.0015*math.cos(a),-.001+.0015*math.sin(a),.004),(.0014,.0035,.0012),0,n=8,rings=4)
 p.finish(c,True);fol.finish(c,False)
 xs=[v.co.x for o in c.objects if o.type=='MESH' for v in o.data.vertices];ys=[v.co.y for o in c.objects if o.type=='MESH' for v in o.data.vertices];factor=.18/max(max(xs)-min(xs),max(ys)-min(ys))
 for o in c.objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co*=factor
 return {'nominal_scale':{'meters':.18,'axis':'preserved foliage maximum planar span','kind':'art choice'},'organ_scope':'short shoot and repeatedly dichotomous foliage only; preserved-organ teaching model, no whole tree or reproductive affiliation','geometry_parameters':{'main_leaves':5,'readable_fork_generations':2,'textures':0}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='czekanowskia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='czekanowskia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#82694d', '#a59b68', '#b3a471'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Preserved foliage organ for separate terrestrial natural-history teaching.','habitat_zh':'陆生植物叶器官标本，分区教学展示。','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Only compact short shoot and narrow angular repeatedly forked leaf ribbons; no crown or reproductive organs. Thin thickness, color and spread are original teaching-art choices; no exact species/specimen reconstruction.','zh':'仅紧凑短枝与细带二叉叶；不补树冠或繁殖器官。厚度颜色展开为原创示意，不复制造型标本或指定现代种。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Czekanowskia forked short-shoot specimen','zh':'茨康叶二叉短枝标本'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH49_COMPLETE',s)
if __name__=='__main__':main()
