# SPDX-License-Identifier: MIT
"""Original deterministic batch40 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # Original backing sediment section, a presentation host rather than a copied excavated specimen.
 p=Part('Original cut sediment host',m);outline=[(-.125,.025,-.012),(-.123,.025,.204),(-.111,.025,.223),(-.035,.025,.226),(.035,.025,.224),(.112,.025,.219),(.125,.025,.203),(.124,.025,-.012),(.105,.025,-.020),(-.107,.025,-.020)];p.sheet(outline,.036,0,(0,1,0));p.finish(c,False)
 # Each lamina is a real continuous solid sheet spanning the two arms, with curved successive occupation fronts.
 for layer in range(8):
  outline=[];n=33
  for j in range(n):
   x=-.058+.116*j/(n-1);z=.012+.019*layer+.025*(x/.058)**2;outline.append((x,-.001+.0008*math.sin(layer*.7),z))
  for j in reversed(range(n)):
   x=-.058+.116*j/(n-1);z=.012+.019*layer+.025*(x/.058)**2+.016;outline.append((x,-.001+.0008*math.sin(layer*.7),z))
  p=Part('Continuous intervening spreite lamina %02d'%layer,m);p.sheet(outline,.024,1+layer%2,(0,1,0));p.finish(c,False)
 # True hollow U-burrow wall with two open annular mouths; stable planar frames avoid twist at vertical bends.
 pts=[]
 for j in range(22):pts.append((-.066,-.002,.210-(.144*j/22)))
 for j in range(43):
  a=pi+pi*j/42;pts.append((.066*math.cos(a),-.002,.066+.066*math.sin(a)))
 for j in range(1,23):pts.append((.066,-.002,.066+.144*j/22))
 n=20;nr=len(pts);v=[];f=[]
 for inner in [False,True]:
  for j,point in enumerate(pts):
   center=Vector(point);d=(Vector(pts[min(j+1,nr-1)])-Vector(pts[max(0,j-1)])).normalized();axis=Vector((d.z,0,-d.x));side=Vector((0,1,0));radius=.0072 if inner else .011
   for k in range(n):a=2*pi*k/n;v.append(tuple(center+radius*(axis*math.cos(a)+side*math.sin(a))))
 off=nr*n
 for j in range(nr-1):
  for k in range(n):
   kk=(k+1)%n;face=(j*n+k,j*n+kk,(j+1)*n+kk,(j+1)*n+k);f.append(face);f.append(tuple(off+i for i in reversed(face)))
 for k in range(n):
  kk=(k+1)%n;f.append((k,off+k,off+kk,kk));a=(nr-1)*n;f.append((a+k,a+kk,off+a+kk,off+a+k))
 p=Part('Hollow U wall and open paired mouths',m);p.add(v,f,3);p.finish(c,True)
 obs=[o for o in c.objects if o.type=='MESH'];coords=[v.co for o in obs for v in o.data.vertices];scale=.25/max(max(p[i] for p in coords)-min(p[i] for p in coords) for i in range(3))
 for o in obs:
  for v in o.data.vertices:v.co*=scale
 return {'trace_display':'sectional-structure','spreite_structure':{'continuous_solid_sheets':8,'interpretation':'Each full-width curved sheet spans the actual gap between U arms and overlaps their inner margins. Layer count and teaching cut are artistic; not a set of separate U pipes or surface-only lines.','tube':'Continuous hollow wall, two real open mouths. No producer or dated behavior event identified.'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='diplocraterion-spreite-burrow');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='diplocraterion-spreite-burrow';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#958d7b', '#b3a48b', '#a99b83', '#c7b79a'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original interpretive sediment section','habitat_zh':'原创示意沉积物剖面','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original sectional structure: a hollow U-burrow with two open mouths and eight true continuous curved spreite sheets spanning the arms, exposed against a cut sediment host. Count, palette, section and0.25m span are teaching choices, not an excavated specimen, named producer, event duration or exact behavior claim.','zh':'原创结构剖面：带两处真开口的中空U潜穴，两臂之间有八条真实连续弯曲spreite叠层片，结合剖切沉积物宿主展示。层数、配色、剖切及0.25米尺度属教学选择，不复制出土标本，不指定造迹物种、事件时长或精确行为。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Diplocraterion spreite burrow','zh':'Diplocraterion 蹼状U形潜穴'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH40_COMPLETE',s)
if __name__=='__main__':main()
