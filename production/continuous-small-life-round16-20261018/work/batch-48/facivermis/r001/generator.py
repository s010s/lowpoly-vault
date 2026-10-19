# SPDX-License-Identifier: MIT
"""Original deterministic batch48 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def center(t):return Vector((-.038+.069*t,.0016*math.sin(2*pi*t),.006+.0012*math.sin(pi*t)))
def radius(t):
 profile=[(0,.0009),(.07,.0042),(.16,.0045),(.27,.0020),(.69,.0019),(.82,.0026),(.94,.0027),(1,.0012)]
 for j in range(len(profile)-1):
  a,ra=profile[j];b,rb=profile[j+1]
  if a<=t<=b:return ra+(rb-ra)*(t-a)/(b-a)
 return .0012

def generate(c,m):
 body=Part('continuous-bare-trunk-and-swollen-posterior',m);v=[];f=[];n=14;nr=97
 for j in range(nr):
  t=j/(nr-1);p=center(t);r=radius(t)*(1+.018*math.sin(2*pi*16*t));tangent=(center(min(1,t+.001))-center(max(0,t-.001))).normalized();side=Vector((-tangent.y,tangent.x,0)).normalized()
  for k in range(n):a=2*pi*k/n;v.append(tuple(p+side*r*math.cos(a)+Vector((0,0,r*.87*math.sin(a)))))
 for j in range(nr-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 body.add(v,[tuple(reversed(range(n))),*f,tuple((nr-1)*n+k for k in range(n))],0);body.finish(c,True)
 arms=Part('exactly-five-anterior-arm-pairs',m);fringe=Part('restrained-paired-arm-spines',m)
 for j in range(5):
  t=.72+j*.053;p=center(t);r=radius(t)
  for sign in [-1,1]:
   root=p+Vector((0,sign*r*.8,.0002));points=[tuple(root),tuple(root+Vector((.0008,sign*.004,.0013))),tuple(root+Vector((.0032,sign*.009,.0025))),tuple(root+Vector((.0065,sign*(.014+.0003*math.sin(j)),.004+.0005*j)))]
   curve_tube(arms,points,.00115,.00032,1,8,5);arms.ellipsoid(tuple(root),(.0013,.0012,.00115),1,10,5)
   ps=[Vector(q) for q in catmull(points,5)]
   for fraction in [.31,.48,.65,.81]:
    q=ps[round(fraction*(len(ps)-1))]
    for side in [-1,1]:
     end=q+Vector((side*.00115,sign*.0002,.00075));fringe.tube([tuple(q),tuple((q+end)*.5+Vector((0,0,.0001))),tuple(end)],[.00013,.00009,.000055],2,5)
 arms.finish(c,True);fringe.finish(c,True)
 detail=Part('subtle-head-eyes-and-posterior-attachment-hooks',m)
 for sign in [-1,1]:detail.ellipsoid((.028,sign*.0017,.0082),(.00042,.00028,.00038),3,8,5)
 for j in range(6):
  a=2*pi*j/6;p=center(.12)+Vector((0,.0040*math.cos(a),.0035*math.sin(a)));curve_tube(detail,[tuple(p),tuple(p+Vector((-.0011,.0004*math.cos(a),.0004*math.sin(a)))),tuple(p+Vector((-.0015,0,0)))],.00026,.00010,2,5,3)
 detail.finish(c,True)
 allv=[p.co for o in c.objects if o.type=='MESH' for p in o.data.vertices];span=max(max(p[k] for p in allv)-min(p[k] for p in allv) for k in range(3));factor=.075/span
 for o in c.objects:
  if o.type=='MESH':
   for p in o.data.vertices:p.co*=factor
 return {'nominal_body_and_arm_span_m':.075,'anatomical_scope':'one whole Facivermis-inspired lobopodian with exactly five paired anterior arms bearing economical marginal spines, long bare trunk and integrated swollen posterior attachment','arm_pairs':5,'dwelling_tube_included':False,'artistic_note':'Static gently spread arms, restrained hooks/eyes, soft tissue thickness, nominal scale and original muted palette are interpretive teaching choices. No full unsupported dwelling tube, complex internal soft anatomy, feeding animation or exact specimen restoration.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='facivermis');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='facivermis';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B08C83', '#BD9F8B', '#D0B995', '#57514A'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Early Cambrian benthic-organism inspiration','habitat_zh':'早寒武纪底栖生物启发','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Five spiny anterior arm pairs attach softly to a long bare body ending in an integrated swollen posterior. Original static posture and restrained detail; no unsupported full tube, walking limbs along the trunk, feeding animation or strict specimen reconstruction.','zh':'五对带刺前臂柔和连接长裸躯干，后端一体膨大；姿态与微细节为原创克制示意，不补整管、不沿全身布行走足、不承诺取食动画或严格标本复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Facivermis tube-dwelling lobopodian','zh':'Facivermis 管栖叶足动物'},'fauna',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH48_COMPLETE',s)
if __name__=='__main__':main()
