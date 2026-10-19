# SPDX-License-Identifier: MIT
"""Original deterministic batch38 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # Clip each inclined older solid bed against the actual horizontal erosional contact.
 def clip(poly,a,b,c):
  out=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   fp=a*p[0]+b*p[1]-c;fq=a*q[0]+b*q[1]-c;pin=fp<=1e-9;qin=fq<=1e-9
   if pin:out.append(p)
   if pin!=qin:
    t=fp/(fp-fq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  return out
 def bed(name,poly,mi,depth):
  if len(poly)<3:return
  p=Part(name,m);p.sheet([(x,0,z) for x,z in poly],depth,mi,(0,1,0));o=p.finish(c,False);bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Weathered cut boundary','BEVEL');mod.width=.0009;mod.segments=1;bpy.ops.object.modifier_apply(modifier=mod.name)
 for j in range(9):
  lo=-.30+.10*j;hi=lo+.10;poly=[(-.425,0),(.425,0),(.425,.27),(-.425,.27)];poly=clip(poly,-.64,1,hi);poly=clip(poly,.64,-1,-lo);bed('Older tilted bed %02d'%j,poly,j%2,.282+.002*math.sin(j))
 for j,(lo,hi) in enumerate([(.27,.323),(.323,.381),(.381,.444)]):
  if j<2:poly=[(-.425,lo),(.425,lo),(.425,hi),(-.425,hi)]
  else:poly=[(-.425,lo),(.425,lo)]+[(.425-.85*k/12,hi+.003*math.sin(k*1.2)+.0015*math.cos(k*2.7)) for k in range(13)]
  bed('Younger near-horizontal cover bed %02d'%j,poly,2+j%2,.286)
 obs=[o for o in c.objects if o.type=='MESH'];coords=[v.co for o in obs for v in o.data.vertices];scale=.85/(max(p.x for p in coords)-min(p.x for p in coords))
 for o in obs:
  for v in o.data.vertices:v.co*=scale
 return {'contact_structure':{'lower_beds':'Original inclined solids clipped at z0.27m before final nominal scaling and grounding; bedding truly terminates at erosional contact.','upper_beds':'Three continuous near-horizontal covering solids; no rotated whole older asset or painted-line layering.','age_scope':'Relative older/younger relation only; no actual ages or GrandCanyon specimen/site replica.'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='angular-unconformity-outcrop');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='angular-unconformity-outcrop';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#959387', '#aaa390', '#b6ad96', '#c4b99f'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic geological teaching section','habitat_zh':'通用地质教学剖面','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original solid section with older inclined beds actually clipped at an erosional contact, covered by three continuous near-horizontal beds. Real boundaries remain legible in gray. Nominal0.85m crop width, layer count and palette are illustrative; no exact site or geological age claim.','zh':'原创实体剖面：下部倾斜老层在侵蚀接触面真实终止，上覆三条连续近平层。灰色下实际层界仍可读。0.85米裁片宽度、层数与配色属示意，不指定实际地点或地层年龄。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Angular unconformity outcrop','zh':'角度不整合露头'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH38_COMPLETE',s)
if __name__=='__main__':main()
