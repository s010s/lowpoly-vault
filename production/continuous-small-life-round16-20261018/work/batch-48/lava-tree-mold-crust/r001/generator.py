# SPDX-License-Identifier: MIT
"""Original deterministic batch48 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 host=Part('continuous-lava-crust-enclosing-deep-negative-trunk-mold',m);v=[];f=[];mi=[];N=64;J=8
 def inner(a,t):
  r=(.087*(1-.21*t)+.011*t**4)*(1+.024*math.sin(12*a+.4)+.012*math.sin(19*a+7*t));cx=-.03+.012*t;cy=.015-.005*t;z=.31*(1-t)+.035*t+.008*math.sin(3*a)*(1-t)
  return Vector((cx+r*math.cos(a),cy+.88*r*math.sin(a),z))
 def outer(a,z=None):
  den=(abs(math.cos(a))**4+abs(math.sin(a))**4)**.25;x=.35*math.cos(a)/den*(1+.035*math.sin(5*a));y=.30*math.sin(a)/den*(1+.03*math.cos(7*a));return Vector((x,y,.31+.012*math.sin(3*a)+.008*math.sin(7*a) if z is None else z))
 for j in range(J+1):
  t=j/J
  for k in range(N):
   a=2*pi*k/N;p=inner(a,0).lerp(outer(a),t);p.z+=.006*math.sin(pi*t)+.004*math.sin(17*p.x+8*p.y)*math.sin(pi*t);v.append(tuple(p))
 for j in range(J):
  for k in range(N):a=j*N+k;b=j*N+(k+1)%N;f.append((a,b,b+N,a+N));mi.append(1 if j==0 else 0)
 old=[J*N+k for k in range(N)]
 for z,scale in [(.19,1.012),(.015,.98),(0,.94)]:
  ring=[]
  for k in range(N):p=outer(2*pi*k/N,z);p.x*=scale;p.y*=scale;ring.append(len(v));v.append(tuple(p))
  for k in range(N):q=(k+1)%N;f.append((old[k],ring[k],ring[q],old[q]));mi.append(0)
  old=ring
 bottom=len(v);v.append((0,0,0))
 for k in range(N):f.append((bottom,old[(k+1)%N],old[k]));mi.append(0)
 old=list(range(N))
 for j in range(1,23):
  t=j/22;ring=[]
  for k in range(N):ring.append(len(v));v.append(tuple(inner(2*pi*k/N,t)))
  for k in range(N):q=(k+1)%N;f.append((old[k],old[q],ring[q],ring[k]));mi.append(1)
  old=ring
 floor=len(v);v.append((-.018,.010,.035))
 for k in range(N):f.append((floor,old[k],old[(k+1)%N]));mi.append(1)
 host.add(v,f,mi);o=host.finish(c,False)
 for p in o.data.polygons:p.use_smooth=p.material_index==1
 coords=[p.co for p in o.data.vertices];span=max(max(p[k] for p in coords)-min(p[k] for p in coords) for k in range(3));factor=.7/span
 for p in o.data.vertices:p.co*=factor
 depth=(sum(inner(2*pi*k/N,0).z for k in range(N))/N-.035)*factor
 return {'nominal_crust_and_cavity_span_m':.7,'mold_structure':{'tree_or_wood_assets':0,'continuous_host':True,'deep_negative_cavity':True,'actual_rim_to_floor_depth_m':depth,'integral_chilled_lining':True,'bark_impressions':'restrained real longitudinal wall relief, original nonspecific pattern'},'geological_scope':'original continuous crust surrounding a blind deep negative trunk-shaped cavity, integral lining and low bark-like impressions; not a freestanding hollow column or painted log','process_boundary':'Modern lava-tree-mold process analogy only. No living tree, separate wood/tree asset, tree species, exact locality, dated specimen or Mesozoic field reconstruction. Nominal scale, crust outline and relief are artistic.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='lava-tree-mold-crust');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='lava-tree-mold-crust';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#535752', '#7B7A6B'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original modern-process volcanic-crust teaching analogue','habitat_zh':'原创现代过程熔岩地壳教学类比','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'One continuous crust encloses a deep negative trunk-shaped cavity with integral chilled lining and restrained real bark-like wall relief. No separate tree or wood, exposed hollow column, black-painted log, species or Mesozoic locality inferred.','zh':'一体地壳围住深树干状负形空腔，内壁有一体冷凝衬层与克制真实树皮状起伏；不附第二树木/木材、不做外露空心柱或黑木头，不推断树种或中生代地点。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Lava tree-mold crust','zh':'熔岩树模地壳'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH48_COMPLETE',s)
if __name__=='__main__':main()
