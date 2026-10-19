# SPDX-License-Identifier: MIT
"""Original deterministic batch46 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 shoot=Part('preserved-continuous-tapered-jointed-shoots',m);leaves=Part('reduced-helically-placed-leaf-tips',m)
 def stem(control,r0,r1,nodes,phase):
  points=[Vector(p) for p in catmull(control,12)];lengths=[0]
  for i in range(1,len(points)):lengths.append(lengths[-1]+(points[i]-points[i-1]).length)
  total=lengths[-1]
  def at(t):
   d=t*total;i=next((j for j in range(1,len(points)) if lengths[j]>=d),len(points)-1);u=(d-lengths[i-1])/(lengths[i]-lengths[i-1]);return points[i-1].lerp(points[i],u)
  ts=sorted(set([j/100 for j in range(101)]+[max(0,min(1,(j+.30)/nodes+delta)) for j in range(nodes) for delta in [-.008,0,.008,.018]]));v=[];f=[];mi=[];n=10
  for t in ts:
   p=at(t);d=(at(min(1,t+.001))-at(max(0,t-.001))).normalized();u=Vector((-d.y,d.x,0)).normalized();r=r0*(1-t)+r1*t;near=min(abs(t-(j+.30)/nodes) for j in range(nodes));rim=.00033*math.exp(-(near/.007)**2)*(1-.45*t)
   for k in range(n):a=2*pi*k/n;v.append(tuple(p+u*(r+rim)*math.cos(a)+Vector((0,0,.62*(r+rim)*math.sin(a)))))
  for j in range(len(ts)-1):
   near=min(abs((ts[j]+ts[j+1])*.5-(q+.30)/nodes) for q in range(nodes))
   for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if near<.009 else 0)
  shoot.add(v,[tuple(reversed(range(n))),*f,tuple((len(ts)-1)*n+k for k in range(n))],[0,*mi,0])
  for j in range(nodes):
   t=(j+.30)/nodes;p=at(t);d=(at(min(1,t+.001))-at(max(0,t-.001))).normalized();side=Vector((-d.y,d.x,0)).normalized();a=phase+j*2.39996;u=side*math.cos(a)+Vector((0,0,.62*math.sin(a)));r=r0*(1-t)+r1*t;root=p+u*r*.82;tip=p+d*(.0036*(1-.35*t))+u*(r+.0020*(1-.35*t));cross=d.cross(u).normalized();outline=[tuple(root-cross*.0008),tuple(root+d*.0012-cross*.00065),tuple(tip),tuple(root+cross*.0008)];leaves.sheet(outline,.0003,1,tuple(cross))
 stem([(-.11,0,.007),(-.04,.004,.008),(.04,.003,.008),(.11,.002,.008)],.0049,.0012,10,.3)
 stem([(-.037,.004,.008),(-.006,.025,.009),(.029,.045,.010),(.056,.058,.011)],.0028,.00085,5,1.2)
 stem([(.029,.003,.008),(.046,-.020,.009),(.069,-.033,.010),(.091,-.041,.010)],.00225,.00075,4,2.4)
 shoot.finish(c,True);leaves.finish(c,True)
 allv=[p.co for o in c.objects if o.type=='MESH' for p in o.data.vertices];span=max(max(p[k] for p in allv)-min(p[k] for p in allv) for k in range(3));factor=.22/span
 for o in c.objects:
  if o.type=='MESH':
   for p in o.data.vertices:p.co*=factor
 return {'nominal_preserved_shoot_span_m':.22,'organ_scope':'one original preserved jointed conifer-shoot fragment with two attached short lateral shoots; smooth tapering internodes, integral sheath rims and tiny single helical leaf tips','preservation_note':'Conservative flattened thickness, branch layout, reduced node count and muted brown palette are teaching-art choices. No full crown/trunk/roots, associated cones, modern species, exact parent plant or complete habitat reconstructed.','reference_limit':'Basic morphology supported by actual primary indexed excerpt and separate publisher abstract; original Axsmith2006 publisher full text/abstract fetch blocked. No detailed paper/figure-based restoration claim.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='pseudofrenelopsis');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='pseudofrenelopsis';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#8C7961', '#A59270'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Preserved Cretaceous conifer-shoot teaching specimen','habitat_zh':'白垩纪针叶树枝段教学标本','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'An original preserved tapering jointed shoot fragment with two attached short lateral shoots, integral reduced-leaf sheath rims and tiny helical tips. Brown palette, thickness and branch/node counts are artistic; no whole tree, cones, roots or modern-species inference.','zh':'原创渐细分节枝段，带两枚附着短侧枝、连续缩叶鞘缘与微小螺旋叶尖；褐色、厚度及枝节数量为美术选择，不外推整树、球果、根或现代种。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Pseudofrenelopsis jointed conifer shoots','zh':'Pseudofrenelopsis 拟节柏枝'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH46_COMPLETE',s)
if __name__=='__main__':main()
