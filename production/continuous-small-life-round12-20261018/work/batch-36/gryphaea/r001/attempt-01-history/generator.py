# SPDX-License-Identifier: MIT
"""Original deterministic batch36 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # One continuously expanding curved principal valve, from recurved umbo to broad rim.
 controls=[(-.022,0,.065),(-.034,0,.067),(-.041,0,.055),(-.038,0,.037),(-.027,0,.023),(-.009,0,.022),(.001,0,.031),(.001,0,.046)]
 pts=catmull(controls,7);n=56;p=Part('Deep hooked lower valve',m);v=[];f=[];mi=[]
 rkeys=[.0014,.0045,.007,.012,.019,.025,.029,.034]
 for j,point in enumerate(pts):
  u=j/(len(pts)-1);q=u*7;k=min(6,int(q));t=q-k;r=rkeys[k]*(1-t)+rkeys[k+1]*t
  point=Vector(point);d=Vector(pts[min(j+1,len(pts)-1)])-Vector(pts[max(0,j-1)]);d.normalize();a=Vector((d.z,0,-d.x));a.normalize();b=Vector((0,1,0))
  # Low, slightly unequal growth lamellae form actual relief, not separate stacked bands.
  ridge=1+.027*math.sin(2*pi*u*11)**6
  for h in range(n):
   ang=2*pi*h/n;ir=1+.019*math.sin(3*ang+u*3)+.012*math.cos(7*ang-u*2)
   v.append(tuple(point+r*ridge*ir*(a*math.cos(ang)+b*math.sin(ang)*.77)))
 f.append(tuple(reversed(range(n))));mi.append(0)
 for j in range(len(pts)-1):
  for h in range(n):f.append((j*n+h,j*n+(h+1)%n,(j+1)*n+(h+1)%n,(j+1)*n+h));mi.append(1 if .82<j/(len(pts)-1)<.89 else 0)
 f.append(tuple((len(pts)-1)*n+h for h in range(n)));mi.append(2);p.add(v,f,mi);p.finish(c,True)
 # Small flatter lid seats within the broad mouth. Broad, low convex shell with irregular concentric growth relief.
 p=Part('Flatter upper right lid',m);n=64;nr=22;v=[(.001,0,.0518)];f=[]
 for j in range(1,nr+1):
  r=j/nr
  for k in range(n):
   a=2*pi*k/n;w=1+.012*math.sin(5*a)+.008*math.cos(9*a);x=.001+.0325*r*math.cos(a)*w;y=.025*r*math.sin(a)*w;z=.0472+.0046*(1-r*r)+.00022*math.sin(r*2*pi*7)**5
   v.append((x,y,z))
 for k in range(n):f.append((0,1+k,1+(k+1)%n))
 for j in range(nr-1):
  for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,a+n,b+n,b))
 bottom=len(v);v.append((.001,0,.046))
 for k in range(n):f.append((bottom,1+(nr-1)*n+(k+1)%n,1+(nr-1)*n+k))
 p.add(v,f,2);p.finish(c,True)
 # Exact nominal largest preserved shell span, uniformly applied to original authored points.
 obs=[o for o in c.objects if o.type=='MESH'];coords=[v.co for o in obs for v in o.data.vertices];span=max(max(p[i] for p in coords)-min(p[i] for p in coords) for i in range(3));scale=.09/span
 for o in obs:
  for v in o.data.vertices:v.co*=scale

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='gryphaea');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='gryphaea';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#927e69', '#a18d77', '#bbab91'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Marine shell specimen','habitat_zh':'海生壳体标本','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Preserved shell only. Deep principal valve grows from a hooked umbo into a broad mouth, closed by a flatter smaller lid. Growth relief and nominal0.09m span are original art choices, not an exact specimen or soft-tissue reconstruction.','zh':'仅保存壳体：钩曲壳顶延伸至深厚主壳，小而平的盖壳自然闭合。生长纹和0.09米名义尺寸为原创美术选择，非真实标本或软组织复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Gryphaea curved oyster fossil','zh':'Gryphaea（弯曲牡蛎化石）'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH36_COMPLETE',s)
if __name__=='__main__':main()
