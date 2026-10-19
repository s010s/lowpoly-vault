# SPDX-License-Identifier: MIT
"""Original deterministic batch49 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 body=Part('Continuous narrow soft trunk',m);legs=Part('Twenty robust lobopods',m);spines=Part('Reduced large soft-cuticle spine rhythm',m)
 pts=[];rr=[]
 for j in range(65):
  t=j/64;x=.056*(t-.5);y=.0011*math.sin(t*2*pi);z=.0093+.0010*math.sin(pi*t)
  pts.append((x,y,z));rr.append(.00024+.00142*math.sin(pi*t)**.45)
 body.tube(pts,rr,0,n=12)
 for j in range(10):
  t=(j+.6)/10.2;x=.052*(t-.5);by=.0011*math.sin(t*2*pi);bz=.0093+.0010*math.sin(pi*t)
  for side in [-1,1]:
   angle=.20*math.sin(j*.8)+.12*side;length=.0115*(.88+.12*math.sin(pi*t))
   points=[];rs=[]
   for k in range(11):
    u=k/10;points.append((x+.0014*math.sin(pi*u)*math.sin(j*.7),by+side*(.0007+length*u),bz-.0067*u+.0006*math.sin(pi*u)));rs.append((.00085+.00155*math.sin(pi*u)**.6)*(1-.38*u))
   legs.tube(points,rs,1 if j%3 else 0,n=10)
   # Narrow bases, inflated mid-lobopods; no ball joints or rigid segmented plates.
   for k in [3,5,7,9]:
    p=Vector(points[k]);u=k/10;r=rs[k]
    for a in [.25*pi,.85*pi,1.4*pi]:
     direction=Vector((math.cos(a),side*.28,math.sin(a))).normalized();start=p+direction*(r*.8);tip=p+direction*(r+.00115*(1-.28*u))
     spines.tube([tuple(start),tuple(start.lerp(tip,.5)),tuple(tip)],[.00034,.00020,.000055],2,n=5)
   p=Vector(points[-1]);spines.tube([tuple(p),tuple(p+Vector((.0003,side*.0011,-.0005)))],[.00038,.000055],2,n=6)
 body.finish(c,True);legs.finish(c,True);spines.finish(c,False)
 for o in c.objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co*=.06/.056
 return {'nominal_scale':{'meters':.06,'axis':'trunk length; appendages remain proportionally smaller','kind':'art choice'},'organism_scope':'whole-organism inspired-by Diania; soft unjointed robust lobopods; no phylogeny assertion','geometry_parameters':{'lobopod_pairs':10,'large_spine_rows_reduced':3,'textures':0}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='diania');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='diania';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#b78c7b', '#c69a86', '#ead7b5'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Cambrian marine-inspired teaching organism; not shared-site reconstruction.','habitat_zh':'寒武纪海生动物形态启发，非共生场景。','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Thin continuous trunk, robust lateral lobopods with narrow bases and sparse spines. Soft annulations and details reduced; palette, scale and posture original art, no rigid joints or settled phylogeny.','zh':'细连续躯干与窄基粗叶足，主要刺节奏；颜色尺度姿态为原创美术，软环纹简化，不宣称硬关节或系统发育结论。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Diania-inspired spiny lobopodian','zh':'Diania 粗刺叶足动物概念'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH49_COMPLETE',s)
if __name__=='__main__':main()
