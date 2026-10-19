# SPDX-License-Identifier: MIT
"""Original deterministic batch43 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 axis=Vector((0,-.78,.626)).normalized();u=Vector((1,0,0));v=axis.cross(u).normalized()
 def point(x,y,z):return tuple(u*x+v*y+axis*z)
 fruit=Part('single-elongated-indehiscent-fruit',m);vs=[];fs=[];n=18
 profile=[(0,.0006),(.002,.0018),(.007,.0032),(.015,.0038),(.023,.0034),(.029,.0026),(.033,.0015),(.034,.00055)]
 for j,(z,r) in enumerate(profile):
  for k in range(n):
   a=2*pi*k/n;rr=r*(1+.035*math.cos(6*a));vs.append(point(rr*math.cos(a),rr*math.sin(a),z))
 for j in range(len(profile)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 fruit.add(vs,[tuple(reversed(range(n))),*fs,tuple((len(profile)-1)*n+k for k in range(n))],0);fruit.finish(c,True)
 calyx=Part('continuous-unlobed-shallow-funnel-calyx',m);vs=[];fs=[];N=80;R=9
 # Closed, thin funnel shell, subtly irregular outline; radial relief is geometry, no petal divisions.
 for layer in range(2):
  for j in range(R):
   t=j/(R-1);r=.0021+(.025-.0021)*t
   for k in range(N):
    a=2*pi*k/N;rr=r*(1+.014*math.sin(3*a)+.009*math.sin(7*a+.4));ridge=(.00029*(.25+.75*t)*(.5+.5*math.cos(20*a))**3)*math.sin(pi*t)**.35
    z=.023+.0065*t**1.1+ridge-(.00075 if layer else 0);vs.append(point(rr*math.cos(a),rr*math.sin(a),z))
 off=R*N
 for layer in range(2):
  for j in range(R-1):
   for k in range(N):
    ids=(layer*off+j*N+k,layer*off+j*N+(k+1)%N,layer*off+(j+1)*N+(k+1)%N,layer*off+(j+1)*N+k)
    fs.append(ids if layer==0 else tuple(reversed(ids)))
 for j in [0,R-1]:
  for k in range(N):a=j*N+k;b=j*N+(k+1)%N;fs.append((a,a+off,b+off,b))
 calyx.add(vs,fs,[1 if i<((R-1)*N) else 2 for i in range(len(fs))]);calyx.finish(c,True)
 return {'nominal_preserved_organ_span_m':.05,'organ_scope':'one stylized preserved indehiscent fruit with attached persistent unlobed funnel calyx; no parent plant or flower','preservation_note':'Original softly three-dimensional teaching presentation of an isolated fossil organ. Brown palette, conservative restored thickness, gentle tilt and reduced radial-ridge count are artistic, not a facsimile or measured specimen.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='dillhoffia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='dillhoffia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#795340', '#B79566', '#91724D'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Paleogene preserved reproductive-organ teaching specimen','habitat_zh':'古近纪孤立繁殖器官教学标本','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'One elongated preserved fruit with attached unlobed shallow funnel calyx and reduced major radial ridges, inspired by UWBM 310839 descriptions. Original thickness, palette and display tilt; no parent plant, family inference or flowering reconstruction.','zh':'参考UWBM 310839描述的一枚长果体与无裂浅漏斗宿存萼，简化主要放射脊；厚度、配色、展示倾角为原创美术选择，不推断母树、科级形态或花。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Dillhoffia funnel-calyx fruit','zh':'Dillhoffia 漏斗萼果化石'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH43_COMPLETE',s)
if __name__=='__main__':main()
