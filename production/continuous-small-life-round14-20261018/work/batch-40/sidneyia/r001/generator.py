# SPDX-License-Identifier: MIT
"""Original deterministic batch40 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 def shield(p,cx,cy,w,h,z,dome,mi,square=False):
  n=32;nr=7;v=[(cx,cy,z+dome)];f=[]
  for j in range(1,nr+1):
   r=j/nr
   for k in range(n):
    a=2*pi*k/n;ca=math.cos(a);sa=math.sin(a);xx=math.copysign(abs(ca)**(.70 if square else 1),ca);yy=math.copysign(abs(sa)**(.74 if square else 1),sa);v.append((cx+w*r*xx,cy+h*r*yy,z+dome*(1-r*r)))
  for k in range(n):f.append((0,1+k,1+(k+1)%n))
  for j in range(nr-1):
   for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,a+n,b+n,b))
  bot=len(v);v.append((cx,cy,z-.0015))
  for k in range(n):f.append((bot,1+(nr-1)*n+(k+1)%n,1+(nr-1)*n+k))
  p.add(v,f,mi)
 p=Part('Broad overlapping trunk shields',m)
 widths=[.020,.023,.025,.026,.0255,.024,.022,.019,.016]
 for i,w in enumerate(widths):shield(p,0,-.026+i*.007,w,.0066,.0125+.0005*math.sin(i*.5),.007,0 if i%3 else 1)
 p.finish(c,True);p=Part('Short domed head shield',m);shield(p,0,-.041,.021,.012,.013,.009,1,True);p.finish(c,True)
 p=Part('Connected underside and narrow abdominal rings',m);p.ellipsoid((0,-.001,.0105),(.021,.034,.0065),2,24,10)
 for i in range(3):p.ellipsoid((0,.037+i*.009,.011),(.010-i*.001,.0067,.0055),0,24,8)
 p.finish(c,True)
 p=Part('Telson and paired broad tail paddles',m)
 for sign in [-1,1]:
  outline=[(sign*.004,.057,.011),(sign*.013,.060,.012),(sign*.023,.068,.011),(sign*.025,.075,.010),(sign*.021,.081,.009),(sign*.014,.079,.009),(sign*.006,.068,.010)]
  p.sheet(outline,.002,1,(0,0,1))
 p.sheet([(-.006,.058,.012),(.006,.058,.012),(.007,.067,.012),(0,.084,.009),(-.007,.067,.012)],.002,0,(0,0,1));p.finish(c,True)
 # Simple coherent walking-limb groups; the detailed joint and filament counts are deliberately not reconstructed.
 p=Part('Economical articulated limb groups',m)
 for i in range(8):
  y=-.026+i*.007;w=widths[i]
  for sign in [-1,1]:curve_tube(p,[(sign*w*.65,y,.010),(sign*(w+.006),y-.002,.008),(sign*(w+.011),y+.003,.003),(sign*(w+.010),y+.007,.002)],.0022,.0008,2,7,3)
 p.finish(c,True)
 p=Part('Slender forward antennae and small eye stalks',m)
 for sign in [-1,1]:
  curve_tube(p,[(sign*.014,-.049,.018),(sign*.027,-.059,.018),(sign*.039,-.069,.019),(sign*.045,-.071,.022)],.0012,.00032,2,8,7)
  curve_tube(p,[(sign*.014,-.047,.019),(sign*.018,-.049,.022)],.0014,.0014,2,8,3)
 p.finish(c,True);p=Part('Small rounded lateral eyes',m)
 for sign in [-1,1]:p.ellipsoid((sign*.018,-.049,.023),(.0025,.0023,.002),3,16,7)
 p.finish(c,True)
 scale=.14/(.085-(-.053))
 for o in c.objects:
  if o.type=='MESH':
   for v in o.data.vertices:v.co*=scale
 return {'nominal_body_tail_length_m':.14,'scale_convention':'Nominal body+tail extent0.14m from head-front to tail-tip; antennae extend beyond it. Overall metadata bounds include appendages. Original art dimensions, not a measured specimen.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='sidneyia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='sidneyia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#6c8c82', '#7f9b8b', '#526d67', '#304c49'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Marine benthic teaching animal','habitat_zh':'海生底栖教学动物','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original Sidneyia-inspired animal with short broad head, overlapping wide trunk shields, abruptly narrower ringed abdomen and paired tail paddles. Simple economical limbs, thin antennae and small lateral eyes. Body+tail0.14m is nominal art scale; exact limb/microhair counts, color, movement and predation animation are not claimed.','zh':'原创 Sidneyia 启发教学动物：短宽头甲、宽叠甲躯干、突然收窄的环腹及双尾桨，配经济肢组、细触角与小侧眼。体尾0.14米为名义美术尺度；不声称精确肢节/微毛数量、真实颜色、运动或捕食动画。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Sidneyia broad-bodied hunter','zh':'Sidneyia（宽体节肢动物）'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH40_COMPLETE',s)
if __name__=='__main__':main()
