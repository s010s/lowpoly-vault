# SPDX-License-Identifier: MIT
"""Original deterministic batch42 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # One continuous rounded-square organic periderm wall, never four separate panel meshes.
 n=40;nr=64;v=[];f=[];mi=[]
 def ring(z,inner=False):
  out=[];t=max(0,min(1,(z-.125)/.025));radius=.0015+.028*(z/.15)**.83
  for k in range(n):
   a=2*pi*k/n;ca=math.cos(a);sa=math.sin(a);fold=max(0,math.cos(4*a))**1.5
   ridge=.00048*(.5+.5*math.cos(z*2*pi/.009))**4*(1-t)
   r=radius+ridge-.010*t*t*fold
   if inner:r-=.0010+.00045*z/.15
   zz=z-.007*t*t*fold
   out.append((r*math.copysign(abs(ca)**.39,ca),r*math.copysign(abs(sa)**.39,sa),zz))
  return out
 for j in range(nr+1):v.extend(ring(.15*j/nr))
 off=len(v)
 for j in range(nr+1):v.extend(ring(.003+.147*j/nr,True))
 for j in range(nr):
  for k in range(n):
   kk=(k+1)%n;face=(j*n+k,j*n+kk,(j+1)*n+kk,(j+1)*n+k);f.append(face);mi.append(0);f.append(tuple(off+i for i in reversed(face)));mi.append(1)
 # Solid apex closure and a real annular folded mouth rim.
 f.append(tuple(reversed(range(n))));mi.append(0);f.append(tuple(off+k for k in range(n)));mi.append(1)
 for k in range(n):kk=(k+1)%n;a=nr*n;f.append((a+k,a+kk,off+a+kk,off+a+k));mi.append(0)
 p=Part('Continuous tapered four-faced ribbed body and infolded aperture',m);p.add(v,f,mi);p.finish(c,True)
 return {'body_structure':{'nominal_height_m':.15,'top':'Four apertural regions partly infold within one continuous hollow wall; opening and wall thickness are real geometry.','scope':'Periderm/body form only. No complex soft body, tentacles, exact attachment anatomy or ecological mount.'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='conularia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='conularia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#af8970', '#9a7b67'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Marine conulariid teaching form','habitat_zh':'海生锥石类教学形态','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original Conularia-inspired four-sided body, continuous taper with restrained transverse rib relief and a partly infolded real open aperture. Nominal0.15m height, palette, rib spacing and folding pose are art choices. No complex soft tissues, tentacles or exact attachment ecology; not a strict specimen reconstruction.','zh':'原创Conularia启发四棱渐细体，连续体壁有克制实体横肋与部分内折的真实开口。0.15米高度、配色、肋距和折合姿态属美术选择；不添加复杂软体、触手或精确附着生态，非严格标本复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Conularia four-sided conulariid','zh':'Conularia（四棱锥石类）'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH42_COMPLETE',s)
if __name__=='__main__':main()
