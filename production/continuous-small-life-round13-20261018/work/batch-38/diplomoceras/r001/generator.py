# SPDX-License-Identifier: MIT
"""Original deterministic batch38 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # A single continuous, growing shell sweep. Centerline is planar; no pipe fittings or assembled elbows.
 pts=[]
 def line(a,b,n):
  for j in range(n):
   u=j/n;pts.append(tuple(Vector(a)*(1-u)+Vector(b)*u))
 line((-.16,0,.20),(-.16,0,.72),43)
 for j in range(42):
  t=pi-pi*j/42;pts.append((-.065+.095*math.cos(t),0,.72+.095*math.sin(t)))
 line((.03,0,.72),(.03,0,.15),47)
 for j in range(46):
  t=pi+pi*j/46;pts.append((.145+.115*math.cos(t),0,.15+.115*math.sin(t)))
 line((.26,0,.15),(.26,0,.64),40);pts.append((.26,0,.64))
 lengths=[0.]
 for a,b in zip(pts,pts[1:]):lengths.append(lengths[-1]+(Vector(b)-Vector(a)).length)
 p=Part('Continuous ribbed trombone shell',m);v=[];f=[];n=24;nr=len(pts)
 for j,point in enumerate(pts):
  u=lengths[j]/lengths[-1];r=.013+.021*u**.9;ridge=1+.075*(.5+.5*math.cos(lengths[j]*2*pi/.036))**3
  center=Vector(point);d=(Vector(pts[min(j+1,nr-1)])-Vector(pts[max(0,j-1)])).normalized();axis=Vector((d.z,0,-d.x)).normalized();side=Vector((0,1,0))
  for k in range(n):
   a=2*pi*k/n;v.append(tuple(center+r*ridge*(axis*math.cos(a)+side*.88*math.sin(a))))
 f.append(tuple(reversed(range(n))))
 for j in range(nr-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 # Real dark terminal aperture, with wall thickness and a short closed inner recess.
 center=Vector(pts[-1]);d=(center-Vector(pts[-2])).normalized();axis=Vector((d.z,0,-d.x)).normalized();side=Vector((0,1,0));r=.034*(1+.075*(.5+.5*math.cos(lengths[-1]*2*pi/.036))**3)
 for j in range(2):
  for k in range(n):
   a=2*pi*k/n;v.append(tuple(center-d*(.045*j)+r*.78*(axis*math.cos(a)+side*.88*math.sin(a))))
 off=nr*n
 for k in range(n):
  kk=(k+1)%n;f.append(((nr-1)*n+k,(nr-1)*n+kk,off+kk,off+k));f.append((off+k,off+kk,off+n+kk,off+n+k))
 f.append(tuple(off+n+k for k in reversed(range(n))));p.add(v,f,0);o=p.finish(c,True)
 coords=[v.co for v in o.data.vertices];scale=.9/max(max(p[i] for p in coords)-min(p[i] for p in coords) for i in range(3))
 for v in o.data.vertices:v.co*=scale

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='diplomoceras');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='diplomoceras';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#a99b84'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Preserved marine shell specimen','habitat_zh':'保存的海生壳体标本','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original shell-only concept with parallel growing shafts, two broad hairpin turns, open gaps and integral restrained ribs. The real aperture is recessed; fine sutures and chambers simplified. Nominal0.9m longest span is display art scale, not a species measurement. No soft body or swimming mechanism claimed.','zh':'原创壳体概念：平行渐粗长管、两处宽发夹弯、清楚间隙及克制实体肋纹，末端有真实凹入壳口。细缝合线和腔室简化，0.9米为名义展示尺度，非物种实测；不添加软体或运动机制。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Diplomoceras trombone ammonite','zh':'Diplomoceras（长号形菊石）'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH36_COMPLETE',s)
if __name__=='__main__':main()
