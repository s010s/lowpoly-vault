# SPDX-License-Identifier: MIT
"""Original deterministic batch43 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def center(t):return Vector((.045*(t-.5),.0013*math.sin(2*pi*t),.0035+.00045*math.sin(pi*t)))
def bodyrad(t):return .00048+.00305*math.sin(pi*t)**.67
def generate(c,m):
 body=Part('continuous-soft-segmented-trunk',m);v=[];f=[];nr=105;n=14
 for j in range(nr):
  t=j/(nr-1);p=center(t);r=bodyrad(t)*(1-.045*(.5+.5*math.cos(2*pi*21*t)))
  tangent=(center(min(1,t+.001))-center(max(0,t-.001))).normalized();side=Vector((-tangent.y,tangent.x,0))
  for k in range(n):
   a=2*pi*k/n;v.append(tuple(p+side*r*math.cos(a)+Vector((0,0,.77*r*math.sin(a)))))
 for j in range(nr-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 body.add(v,[tuple(reversed(range(n))),*f,tuple((nr-1)*n+k for k in range(n))],0);body.finish(c,True)
 roots=Part('fleshy-parapodia-including-head',m);hairs=Part('economical-chaetal-fans',m)
 for j in range(20):
  t=.08+j*.043;p=center(t);r=bodyrad(t)
  for sign in [-1,1]:
   q=p+Vector((0,sign*r*.91,-.00015));roots.ellipsoid(q,(.00085,.00082,.0007),1,8,5)
   for k in range(3):
    delta=(k-1)*.0007;reach=.0017+.00035*math.sin(j*1.7+k)
    pts=[q,q+Vector((delta*.3,sign*.0007,.00025)),q+Vector((delta,sign*reach,.00085+(k%2)*.00055))]
    curve_tube(hairs,[tuple(x) for x in pts],.00014,.000075,2,5,2)
 roots.finish(c,True);hairs.finish(c,True)
 head=Part('head-and-long-paired-sensory-palps',m)
 for sign in [-1,1]:
  p=center(.98)+Vector((0,sign*.0006,.00045))
  pts=[tuple(p),tuple(p+Vector((.002,sign*.001,.0006))),tuple(p+Vector((.0053,sign*.0017,.001))),tuple(p+Vector((.007,sign*.0014,.00165)))]
  curve_tube(head,pts,.00045,.00012,1,8,5)
  # A distinct small head chaetal bundle adjacent to the anterior mouth region.
  q=center(.96)+Vector((0,sign*.001,.0002))
  for k in range(3):curve_tube(head,[tuple(q),tuple(q+Vector((.0007+k*.0004,sign*.0015,.0005))),tuple(q+Vector((.0007+k*.0005,sign*.0024,.0009)))],.00013,.000075,2,5,2)
 p=center(1)+Vector((0,0,.00045));curve_tube(head,[tuple(p),tuple(p+Vector((.0012,0,.0006))),tuple(p+Vector((.0023,0,.001)))],.00026,.00012,3,7,4)
 head.finish(c,True)
 return {'nominal_body_length_m':.045,'anatomical_scope':'one stylized whole annelid; continuous tapered segmented trunk, head chaetae, paired long palps and short medial antenna','scale_note':'Frozen nominal body length 0.045 m is an artistic display choice; ROM describes specimens up to about 0.03 m. Palps extend beyond body. Segment and bristle counts simplified.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='kootenayscolex');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='kootenayscolex';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B87577', '#C98C81', '#DFBA8C', '#D5A89A'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Cambrian marine benthos inspiration','habitat_zh':'寒武纪海底环境启发','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original softened segmented annelid with head bristles, paired palps and a short medial antenna. Palette, posture, reduced chaetal counts and frozen nominal 4.5 cm body are artistic; ROM maximum about 3 cm is not overridden as a fossil measurement.','zh':'原创柔和连续分节体，头部具毛、双触须与短中触角；颜色、姿态、简化刚毛数量及冻结4.5厘米体长为美术选择，非ROM约3厘米上限标本的新测量。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Kootenayscolex head-bristled annelid','zh':'Kootenayscolex 头部具毛环节动物'},'fauna',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH43_COMPLETE',s)
if __name__=='__main__':main()
