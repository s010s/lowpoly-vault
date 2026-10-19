# SPDX-License-Identifier: MIT
"""Original deterministic batch49 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 p=Part('Actual almond negative relief in continuous sediment',m);n=96;nr=12;v=[(0,0,.022-.009)];f=[]
 for j in range(1,nr+1):
  r=j/nr
  for k in range(n):
   a=2*pi*k/n;x=.054*r*math.cos(a);y=.021*r*math.sin(a)*abs(math.sin(a));z=.022-.009*(1-r*r)**1.3;v.append((x,y,z))
 for k in range(n):f.append((0,1+k,1+(k+1)%n))
 for j in range(nr-1):
  for k in range(n):a=1+j*n+k;h=1+j*n+(k+1)%n;f.append((a,a+n,h+n,h))
 # Additional outer sediment annulus, with an unrelated irregular oval crop contour.
 for j in range(1,7):
  u=j/6
  for k in range(n):
   a=2*pi*k/n;rx=.100*(1-.035*math.sin(3*a)**2);ry=.073*(1+.028*math.cos(5*a));ix=.054*math.cos(a);iy=.021*math.sin(a)*abs(math.sin(a));x=ix*(1-u)+rx*math.cos(a)*u;y=iy*(1-u)+ry*math.sin(a)*u;z=.022+.0007*u*u*math.sin(3*a+.4)
   v.append((x,y,z))
  start=1+(nr+j-2)*n;new=start+n
  for k in range(n):f.append((start+k,new+k,new+(k+1)%n,start+(k+1)%n))
 top_count=len(f);last=1+(nr+5)*n;nb=len(v)
 for k in range(n):v.append((v[last+k][0],v[last+k][1],0))
 bot=len(v);v.append((0,0,0))
 for k in range(n):h=(k+1)%n;f.append((last+k,nb+k,nb+h,last+h));f.append((bot,nb+h,nb+k))
 p.add(v,f,0);o=p.finish(c,False)
 for poly in o.data.polygons:
  if poly.index<top_count:poly.use_smooth=True
 return {'trace_display':'negative-impression','nominal_scale':{'meters':.2,'axis':'interpretive sediment crop span','kind':'art choice'},'trace_scope':'Single shallow almond negative resting impression with pointed ends; no producer or copied fossil; common positive fossil casts are not reproduced here.','geometry_parameters':{'impression_length_m':.108,'impression_width_m':.042,'maximum_negative_depth_m':.009,'surface_materials':1,'textures':0,'depth_is_actual_geometry':True}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='lockeia-resting-trace');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='lockeia-resting-trace';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#c1ac8c'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Interpretive sediment impression, not a named producer or exact locality.','habitat_zh':'沉积停栖印示意，不指定制造者或产地。','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'True shallow almond-shaped depression with pointed ends and continuous edge transition; single uniform sediment material, no leaf-shaped paint or inserted shell. Explicit original negative-impression convention, not copied positive hyporelief; dimensions and depth artistic.','zh':'真实两端尖收杏仁浅凹，边缘连续过渡，统一沉积材质，不用叶状涂色或压入贝壳。按原负形展示，不复制常见正浮雕标本；尺寸深度为美术。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Lockeia-inspired almond resting impression','zh':'Lockeia 杏仁状停栖凹印'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH49_COMPLETE',s)
if __name__=='__main__':main()
