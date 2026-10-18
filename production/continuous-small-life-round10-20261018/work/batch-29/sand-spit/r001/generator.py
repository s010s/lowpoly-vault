# SPDX-License-Identifier: MIT
"""Original deterministic batch29 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 # One connected shore-root and sand tongue; no water plane or separate island.
 controls=[(0,2.9,.72),(.15,2.8,.70),(.25,1.7,.46),(.36,.62,.26),(.54,.48,.24),(.73,.41,.22),(.89,.29,.17),(1,.025,.045)]
 def profile(t):
  for j in range(len(controls)-1):
   a,wa,ha=controls[j];b,wb,hb=controls[j+1]
   if a<=t<=b:
    u=(t-a)/(b-a);s=u*u*(3-2*u);return wa*(1-s)+wb*s,ha*(1-s)+hb*s
  return controls[-1][1:]
 nx=96;ny=30;v=[];f=[]
 for j in range(nx+1):
  t=j/nx;width,height=profile(t);hook=max(0,(t-.65)/.35);center=.12*math.sin(5*t)+2.1*hook*hook
  for k in range(ny+1):
   u=-1+2*k/ny;x=-4+12*t+.05*math.cos(pi*u/2)*math.sin(pi*t);y=center+width*u*(1+.06*math.sin(5*t+u));cross=max(0,math.cos(pi*u/2))**.84;z=.018+height*cross*(1+.025*math.sin(4*t+1.3*u));v.append((x,y,z))
 for j in range(nx):
  for k in range(ny):a=j*(ny+1)+k;f.append((a,a+ny+1,a+ny+2,a+1))
 boundary=list(range(ny+1))+[j*(ny+1)+ny for j in range(1,nx+1)]+[nx*(ny+1)+k for k in range(ny-1,-1,-1)]+[j*(ny+1) for j in range(nx-1,0,-1)];bottom=[]
 for a in boundary:bottom.append(len(v));v.append((v[a][0],v[a][1],.003))
 
 for k,a in enumerate(boundary):kk=(k+1)%len(boundary);f.append((a,bottom[k],bottom[kk],boundary[kk]))
 from mathutils.geometry import tessellate_polygon
 poly=[Vector(v[index]) for index in bottom]
 for tri in tessellate_polygon([poly]):
  ids=[t if isinstance(t,int) else next(i for i,p in enumerate(poly) if (p-t).length<1e-8) for t in tri];f.append(tuple(bottom[i] for i in reversed(ids)))
 p=Part('twelve-metre shore-connected root and free-ended curved sand tongue',m);p.add(v,f,0);o=p.finish(c,True);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='sand-spit');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='sand-spit';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#BDB08F'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic coastal depositional landform teaching patch; water scene separate','habitat_zh':'通用海岸沉积地貌教学片区；水体场景另分','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Geological-form artistic concept: twelve-metre representative landscape extent with a broad cropped shore-connected root narrowing into one projecting low sand tongue and a curved free tip. One continuous closed land mesh, no independent island or second shore attachment/tombolo; broad and narrow macro contours carry the identity rather than ripple noise. Original nominal extent, crest heights, curvature and sand palette, not a complete mapped coast, exact ancient place/age or sediment-transport simulation. Water and display scenery are not included. Original landscape/coast facets preserved.','zh':'地质形态艺术概念：十二米代表性landscape范围，以宽阔截取的连岸根部渐收成单条低矮狭长沙舌及弯曲自由端。单一连续封闭陆体网格，不是独立小岛，也没有第二端连岸/连岛沙洲关系；主要识别来自宽窄宏观轮廓而非波纹噪声。范围、脊高、弯曲及沙色为原创名义设定，不是完整海岸测绘、精确古地点/年代或输沙模拟。不混入水体与展示场景。保留原始landscape/coast分类。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Representative twelve-metre shore-connected sand spit','zh':'十二米代表性连岸沙嘴片区'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH29_COMPLETE',s)
if __name__=='__main__':main()
