# SPDX-License-Identifier: MIT
"""Original deterministic batch36 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # Continuous bent solid beds, with substantial cross-section and tiny relief at their exposed margins.
 # The same family of curves passes through an anticline on the left and a syncline on the right.
 section=[(-.136,0),(-.145,.08),(-.147,.23),(-.147,.77),(-.144,.93),(-.136,1),(.134,1),(.143,.92),(.146,.74),(.146,.24),(.142,.07),(.134,0)]
 samples=69
 for bed in range(6):
  p=Part('Continuous folded bed %02d'%(bed+1),m);v=[];f=[];mis=[]
  for j in range(samples):
   u=j/(samples-1);x=-.475+.95*u
   phase=2*pi*(u+.035);z=.17+.104*math.sin(phase)+.020*math.sin(phase*2+.3)
   slope=(.104*2*pi*math.cos(phase)+.04*2*pi*math.cos(phase*2+.3))/.95
   normal=Vector((-slope,0,1)).normalized()
   for k,(y,t) in enumerate(section):
    # Slight thickness taper and irregular exposed edges avoid factory-extruded wave strips.
    h=.0465*(1+.04*math.sin(u*3));level=(bed+t)*h
    q=Vector((x,y*(1+.018*math.sin(u*11+bed)),z))+normal*level
    q.y+=.004*math.sin(u*5+bed*.8)
    if k in (0,5,6,11):q.z+=.0012*math.sin(u*31+bed)
    v.append(tuple(q))
  n=len(section);f.append(tuple(reversed(range(n))));mis.append(bed%4)
  for j in range(samples-1):
   for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mis.append(bed%4)
  f.append(tuple((samples-1)*n+k for k in range(n)));mis.append(bed%4)
  p.add(v,f,mis);p.finish(c,False)
 # Width is a teaching module choice, uniformly normalize the whole original section.
 obs=[o for o in c.objects if o.type=='MESH'];coords=[v.co for o in obs for v in o.data.vertices];scale=.95/(max(p.x for p in coords)-min(p.x for p in coords))
 for o in obs:
  for v in o.data.vertices:v.co*=scale

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='folded-strata-outcrop');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='folded-strata-outcrop';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#9e9b8a', '#b0ac98', '#8b9187', '#c2bca6'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic geological teaching section','habitat_zh':'通用地质教学剖面','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original exposed section of six continuous solid beds bending through an anticline and a syncline. Actual bed thickness, beveled exposed boundaries and bent outline carry the structure in grayscale; no painted stripes. Section count, proportions and0.95m nominal width are illustrative, with no exact strain, site, age or co-occurrence claim.','zh':'六条连续实体岩层经过背斜和向斜，实际厚度、露面边缘和弯曲轮廓在灰色下仍可读，非绘制条纹。层数、比例及0.95米名义宽度属教学选择，不声称精确应变、地点、时代或共存关系。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Folded strata outcrop','zh':'褶皱地层露头'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH36_COMPLETE',s)
if __name__=='__main__':main()
