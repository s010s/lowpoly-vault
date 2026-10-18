# SPDX-License-Identifier: MIT
"""Original deterministic batch27 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 ctrl=[(-.026,-.016,.008),(-.022,-.033,.008),(.008,-.035,.0085),(.028,-.017,.008),(.021,.011,.0075),(.006,.024,.007)];raw=[Vector(p) for p in catmull(ctrl,16)];dist=[0]
 for j in range(1,len(raw)):dist.append(dist[-1]+(raw[j]-raw[j-1]).length)
 pts=[];nr=161;n=24
 for j in range(nr):
  d=dist[-1]*j/(nr-1);k=next((k for k in range(1,len(dist)) if dist[k]>=d),len(dist)-1);t=(d-dist[k-1])/(dist[k]-dist[k-1]);pts.append(raw[k-1].lerp(raw[k],t))
 v=[];f=[]
 for j,p in enumerate(pts):
  t=j/(nr-1);direction=pts[min(j+1,nr-1)]-pts[max(0,j-1)];direction.normalize();u=direction.cross(Vector((0,0,1))).normalized();w=direction.cross(u).normalized();rad=(.0046+.0031*math.sin(pi*t)**.65-.0013*t)*(1-.052*math.cos(2*pi*48*t))
  for k in range(n):a=2*pi*k/n;v.append(tuple(p+rad*(u*math.cos(a)+w*.88*math.sin(a))))
 for j in range(nr-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 f.extend([tuple(reversed(range(n))),tuple((nr-1)*n+k for k in range(n))]);body=Part('one gently curved tapered annulated trunk',m);body.add(v,f,0);body.finish(c,True)
 intro=Part('restrained short introvert and inset mouth cup',m);curve_tube(intro,[(-.026,-.019,.008),(-.026,-.010,.0088),(-.023,-.0045,.010)],.0039,.0025,1,18,6)
 center=Vector((-.023,-.0015,.010));n=32;v=[];f=[];mi=[]
 for rr,dy in [(.0025,-.003),(.00265,0),(.0019,-.0005),(.0010,-.0017)]:
  for k in range(n):a=2*pi*k/n;v.append(tuple(center+Vector((rr*math.cos(a),dy,rr*math.sin(a)))))
 for j in range(3):
  for k in range(n):kk=(k+1)%n;f.append((j*n+k,j*n+kk,(j+1)*n+kk,(j+1)*n+k));mi.append(1 if j==0 else 2)
 f.extend([tuple(reversed(range(n))),tuple(3*n+k for k in range(n))]);mi.extend([1,2]);intro.add(v,f,mi);intro.finish(c,True)
 hooks=Part('subtle short posterior hook hints',m);tail=pts[-1]
 for j in range(4):
  a=2*pi*j/4;offset=Vector((math.cos(a)*.0026,0,math.sin(a)*.0022));base=tail+offset;curve_tube(hooks,[tuple(base),tuple(base+Vector((.0006,.0018,.0006))),tuple(base+Vector((.0015,.0020,.0001)))],.00048,.00013,2,7,3)
 hooks.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='ottoia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='ottoia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#A69E88', '#B7AE96', '#8F947F'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Cambrian marine teaching interpretation; no predation or coexistence scene','habitat_zh':'寒武纪海生教学复原；不展示捕食或共存场景','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living whole-organism teaching interpretation: one curved annulated soft trunk with graded thickness, a short conservative introvert and inset mouth cup, plus a few restrained posterior hook hints. Muted colors, nominal0.1m body length and static curvature are artistic choices. No mechanical stacked cylinders, exact microscopic hook/tooth counts, fully exposed tooth array, feeding scene or detailed soft-anatomy/locomotor claim. Closed introvert roots overlap organically within the trunk.','zh':'原创全体教学生活复原：连续柔弯环纹躯体与渐变粗细、短而保守的可缩吻端及内凹口杯，辅以少量克制后钩提示。柔和颜色、0.1米名义体长及静态弯曲为美术设定。不堆叠机械圆筒，不主张精确微钩/齿数，不展示满口尖牙、捕食场景或详细软组织/运动机制。封闭吻根自然嵌接于躯体。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Ottoia-inspired gently curved annulated worm','zh':'Ottoia 柔弯环纹蠕虫'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH27_COMPLETE',s)
if __name__=='__main__':main()
