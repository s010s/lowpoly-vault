# SPDX-License-Identifier: MIT
"""Original deterministic batch42 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 def center(u):return Vector((-.12+.24*u,.007*math.sin(pi*u),.036+.010*math.sin(pi*u*1.2)))
 def frame(u):
  d=(center(min(1,u+.001))-center(max(0,u-.001))).normalized();a=Vector((-d.y,d.x,0)).normalized();b=d.cross(a).normalized();return d,a,b
 nr=33;na=28;stride=na+1;v=[];f=[];mi=[]
 for inner in [False,True]:
  for j in range(nr):
   u=j/(nr-1);origin=center(u);d,a,b=frame(u);r=(.019*(1+.025*math.sin(u*5))) if inner else (.027*(1+.04*math.sin(u*5)))
   for k in range(stride):ang=math.radians(200+270*k/na);v.append(tuple(origin+r*(a*math.cos(ang)+b*math.sin(ang))))
 off=nr*stride
 for j in range(nr-1):
  for k in range(na):
   q=(j*stride+k,j*stride+k+1,(j+1)*stride+k+1,(j+1)*stride+k);f.append(q);mi.append(0);f.append(tuple(off+i for i in reversed(q)));mi.append(1)
 for j in [0,nr-1]:
  for k in range(na):q=j*stride+k;f.append((q,q+1,off+q+1,off+q));mi.append(2)
 for j in range(nr-1):
  for k in [0,na]:q=j*stride+k;f.append((q,off+q,off+q+stride,q+stride));mi.append(2)
 p=Part('Continuous sectioned wall and smooth open lumen',m);p.add(v,f,mi);p.finish(c,True)
 p=Part('Bonded unequal exterior construction pellets',m);count=0
 for row in range(11):
  u=.045+.91*row/10;origin=center(u);d,a,b=frame(u);radius=.027*(1+.04*math.sin(u*5))
  for k in range(7):
   ang=math.radians(214+242*k/6+2*math.sin(row*1.7+k*.8));radial=a*math.cos(ang)+b*math.sin(ang);around=radial.cross(d).normalized();pos=origin+radial*(radius+.0011);sx=.0052*(1+.20*math.sin(row*2+k));sy=.0038*(1+.18*math.cos(k*2+row));sz=.0031*(1+.18*math.sin(row+k*1.4));start=len(p.v);p.ellipsoid((0,0,0),(sx,sy,sz),2 if (row+k)%3 else 3,10,5)
   for i in range(start,len(p.v)):
    x,y,z=p.v[i];p.v[i]=tuple(pos+d*x+around*y+radial*z)
   count+=1
 p.finish(c,True)
 obs=[o for o in c.objects if o.type=='MESH'];coords=[v.co for o in obs for v in o.data.vertices];scale=.25/max(max(p[i] for p in coords)-min(p[i] for p in coords) for i in range(3))
 for o in obs:
  for v in o.data.vertices:v.co*=scale
 return {'trace_display':'sectional-structure','wall_structure':{'bonded_exterior_pellets':count,'lumen':'Continuous smooth inner wall, real thickness, two open ends and an original90-degree longitudinal cut window. Exterior pellets do not line or obstruct the lumen.','scope':'Single interpretive gently curved tunnel section; pellet count, sizes, cut and nominal span artistic. No producer, specimen replica or full network claim.'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='ophiomorpha-pellet-lined-burrow');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='ophiomorpha-pellet-lined-burrow';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#ad9f85', '#c1b397', '#aa997a', '#b6a88b'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original interpretive tunnel section','habitat_zh':'原创示意隧道剖面','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original sectional structure with a continuous curved wall, smooth open lumen, real wall thickness and a longitudinal cut exposing the interior. Unequal exterior construction pellets are bonded into the outer wall. Nominal0.25m span, count, palette and cut are artistic; no producer or exact excavated specimen identified.','zh':'原创结构剖面有连续弯曲管壁、平滑开放内腔及实际壁厚，纵剖窗口露出内部；不等大构筑颗粒嵌接外壁。0.25米尺度、数量、配色和剖切属美术选择，不指定造迹物种或精确出土标本。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Ophiomorpha pellet-lined burrow','zh':'Ophiomorpha 粒衬潜穴'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH42_COMPLETE',s)
if __name__=='__main__':main()
