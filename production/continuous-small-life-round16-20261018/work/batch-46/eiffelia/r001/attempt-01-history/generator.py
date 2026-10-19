# SPDX-License-Identifier: MIT
"""Original deterministic batch46 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def radius(t):return .058*math.sin(pi*(.025+.85*t))**.61*(.16+.84*t**.18)
def surf(t,a,offset=0):
 r=radius(t)*(1+.024*math.sin(3*a+.4)*math.sin(pi*t)+.012*math.sin(5*a+2*t))-offset
 return Vector((r*math.cos(a),r*math.sin(a),.13*t+.0007*math.sin(2*a+.7)*math.sin(pi*t)))
def generate(c,m):
 wall=Part('rounded-thin-sac-wall-with-small-ostia',m);N=40;J=25;v=[];f=[]
 for layer in range(2):
  for j in range(J+1):
   for k in range(N):
    p=surf(j/J,2*pi*k/N,.0016 if layer else 0)
    if layer and j==0:p.z+=.0016
    v.append(tuple(p))
 off=(J+1)*N;holes={(6,2),(8,16),(11,28),(13,7),(15,21),(18,34),(20,13)};edges={}
 for j in range(J):
  for k in range(N):
   if (j,k) in holes:continue
   q=(j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k);f.extend([q,tuple(off+i for i in reversed(q))])
   for a,b in zip(q,q[1:]+q[:1]):key=tuple(sorted((a,b)));edges[key]=edges.get(key,0)+1
 for (a,b),count in edges.items():
  if count==1:f.append((a,b,b+off,a+off))
 f.extend([tuple(reversed(range(N))),tuple(off+k for k in range(N))]);wall.add(v,f,0);wall.finish(c,True)
 lattice=Part('hierarchical-interlocking-star-spicule-framework',m)
 def star(t,a,size,arms,mi):
  p=surf(t,a);d1=(surf(t,a+.001)-surf(t,a-.001)).normalized();d2=(surf(t+.001,a)-surf(t-.001,a)).normalized();normal=d1.cross(d2).normalized();p+=normal*.00065
  lattice.ellipsoid(tuple(p),(.0015,.0015,.0015) if arms==6 else (.001,.001,.001),mi,6,3)
  for k in range(arms):
   ang=2*pi*k/arms+.10*math.sin(5*a+t);vec=d1*math.cos(ang)+d2*math.sin(ang);q=p+vec*size
   # Project rays onto the curved sac rather than letting straight spikes float off its wall.
   tz=max(.025,min(.98,q.z/.13));aa=math.atan2(q.y,q.x);end=surf(tz,aa)+normal*.00055
   mid=(p+end)*.5;mid=surf(max(.025,min(.98,mid.z/.13)),math.atan2(mid.y,mid.x))+normal*.00065
   lattice.tube([tuple(p),tuple(mid),tuple(end)],[.00085 if arms==6 else .00052,.00058 if arms==6 else .00040,.00025],mi,5)
 for j,t in enumerate([.23,.43,.63,.82]):
  for k in range(7):star(t,2*pi*(k+(j%2)*.5)/7,.018*(.88+.12*math.sin(k*2.3+j)),6,1)
 for j,t in enumerate([.33,.53,.73]):
  for k in range(7):star(t,2*pi*(k+.25+(j%2)*.5)/7,.0085,4,2)
 lattice.finish(c,True)
 allv=[p.co for o in c.objects if o.type=='MESH' for p in o.data.vertices];height=max(p.z for p in allv)-min(p.z for p in allv);factor=.13/height
 for o in c.objects:
  if o.type=='MESH':
   for p in o.data.vertices:p.co*=factor
 return {'nominal_sac_height_m':.13,'sponge_scope':'one original rounded thin-wall sac with open osculum, small actual wall openings and hierarchical six-ray/four-ray star framework; no exact microscopic spicule count','scale_note':'Frozen nominal13cm sac height is artistic teaching scale. ROM reports specimens up to6cm; not a measured fossil-size claim. Colors, conservative wall thickness and reduced lattice classes are interpretive.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='eiffelia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='eiffelia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#8AA6A0', '#C1C9AC', '#AEBCA4'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Cambrian marine benthos inspiration','habitat_zh':'寒武纪海底环境启发','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original rounded thin sac with open osculum, small ostia and interlocking large six-ray/smaller four-ray framework. Conservative wall thickness, reduced counts and palette are artistic; frozen13cm teaching height is not the ROM maximum6cm fossil measurement.','zh':'原创圆薄壁囊，具顶开口、小孔及相扣大六射/小四射格架；壁厚、简化格数和配色为美术选择，冻结13厘米教学高度并非ROM最大6厘米化石的新测量。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Eiffelia lattice-sac sponge','zh':'Eiffelia 格架囊海绵'},'fauna',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH46_COMPLETE',s)
if __name__=='__main__':main()
