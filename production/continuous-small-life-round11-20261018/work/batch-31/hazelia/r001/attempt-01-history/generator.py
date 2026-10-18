# SPDX-License-Identifier: MIT
"""Original deterministic batch31 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 shield=Part('thin-cupped-shield-inner-outer-wall',m);nu=64;nt=28;v=[];f=[];mi=[]
 def surface(t,u):
  width=.065*(.085+.915*t**.72)*(1+.09*math.sin(pi*t))
  x=width*math.sin(u*1.29)/math.sin(1.29)
  z=.010+.103*t+t**4*(.0042*math.sin(3.4*u+.4)+.0024*math.sin(8*u-.3))
  # The edges curl forward into an open cupped shield; real volume both sides.
  y=.022*t-.044*t**.72*u*u+.003*math.sin(pi*t)*(u+.3)
  # Restrained diverging radial fibre-tract relief, not holes or a separate wire grid.
  radial=.00056*(.2+.8*t)*(.5+.5*math.cos(14*pi*u+.35*math.sin(3*u)))**5
  return x,y-radial,z
 for side in [0,1]:
  for j in range(nt+1):
   t=j/nt
   for k in range(nu+1):
    u=-1+2*k/nu;x,y,z=surface(t,u);thick=.00155*(1-.30*t)
    v.append((x,y+(-.5 if side==0 else .5)*thick,z))
 N=(nt+1)*(nu+1)
 for j in range(nt):
  for k in range(nu):
   a=j*(nu+1)+k;b=a+1;d=a+nu+1;e=d+1
   f.extend([(a,d,e,b),(N+a,N+b,N+e,N+d)]);mi.extend([0,1])
 # Thickened continuous rim/boundary. The cup remains genuinely open, no closing lid.
 boundary=list(range(nu+1))+[j*(nu+1)+nu for j in range(1,nt+1)]+[nt*(nu+1)+k for k in range(nu-1,-1,-1)]+[j*(nu+1) for j in range(nt-1,0,-1)]
 for i,a in enumerate(boundary):b=boundary[(i+1)%len(boundary)];f.append((a,b,N+b,N+a));mi.append(0)
 shield.add(v,f,mi);shield.finish(c,True)
 base=Part('small-organic-attachment-base',m)
 curve_tube(base,[(0,0,.001),(0,.001,.004),(0,.001,.008),(0,0,.014)],.0048,.0051,1,n=14,steps=3)
 base.ellipsoid((0,0,.0018),(.007,.005,.0018),1,n=20,rings=7)
 base.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='hazelia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='hazelia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#a09579', '#8d876f'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Attached marine sponge inspired teaching concept; not a coral','habitat_zh':'附着海生海绵灵感教学概念；非珊瑚','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living inspired-by broad thin cupped shield based on ROM basic H.palmata morphology, with real inner/outer surfaces, small attachment base and restrained diverging radial relief. No perforated panel, tube-sponge reuse or microspicule/net/canal count claim. Nominal0.13m span, muted ochre palette and irregular rim layout are art choices; genus forms vary and this selected shield is not universal.','zh':'原创活体inspired-by宽薄杯盾，依据ROM H.palmata基本形态，具真实内外表面、小附着基部及克制放射脊。不做漏孔平板，不复用管状海绵，不声称微骨针、网格或水孔计数准确。0.13米名义展幅、柔和赭色及不规则口缘为美术设定；属内形态多样，所选盾形不是全属普遍形态。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Hazelia open-shield sponge inspired teaching model','zh':'Hazelia 开盾形海绵灵感教学模型'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH31_COMPLETE',s)
if __name__=='__main__':main()
