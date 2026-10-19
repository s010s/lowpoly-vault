# SPDX-License-Identifier: MIT
"""Original deterministic batch26 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common_color import export_asset

def generate(c,m):
 import bmesh
 def mx(y):return .16*math.sin(1.3*y)+.075*math.cos(2.1*y)
 paths=[]
 paths.append(([(mx(2.2-4.4*j/40),2.2-4.4*j/40) for j in range(41)],.12,.19,.026,.048))
 for pts in [[(-2.72,1.52,0),(-1.85,1.18,0),(-1.0,.62,0),(mx(.1),.1,0)],[(2.75,1.22,0),(1.8,.72,0),(1.1,.18,0),(mx(-.7),-.7,0)],[(-2.4,-.38,0),(-1.7,-.55,0),(-.75,-1.1,0),(mx(-1.42),-1.42,0)]]:
  arr=catmull(pts,7);paths.append(([(p[0],p[1]) for p in arr],.060,.115,.008,.035))
 segments=[]
 for pts,w0,w1,d0,d1 in paths:
  seg=[]
  for j in range(len(pts)-1):
   a=pts[j];bb=pts[j+1];dx=bb[0]-a[0];dy=bb[1]-a[1];seg.append((a[0],a[1],dx,dy,dx*dx+dy*dy,j/(len(pts)-1),1/(len(pts)-1)))
  segments.append((seg,w0,w1,d0,d1))
 def depression(x,y):
  result=0
  for seg,w0,w1,d0,d1 in segments:
   best=1e9;prog=0
   for ax,ay,dx,dy,ll,base,step in seg:
    t=max(0,min(1,((x-ax)*dx+(y-ay)*dy)/ll));dd=(x-ax-t*dx)**2+(y-ay-t*dy)**2
    if dd<best:best=dd;prog=base+step*t
   width=w0+(w1-w0)*prog;dep=(d0+(d1-d0)*prog)*math.exp(-best/(width*width));result=max(result,dep)
  return result
 n=80;ny=62;v=[];faces=[];mi=[];depths=[]
 for j in range(ny+1):
  y0=-2+4*j/ny
  for i in range(n+1):
   x=-3+6*i/n;y=y0+.025*math.sin(2*x+.4)*abs(y0/2)**4;dep=depression(x,y);z=.130+.008*(y+2)+.0012*math.sin(1.8*x+.7*y)-dep;v.append((x,y,z));depths.append(dep)
 for j in range(ny):
  for i in range(n):a=j*(n+1)+i;ids=[a,a+1,a+n+2,a+n+1];faces.append(tuple(ids));mi.append(1 if sum(depths[x] for x in ids)/4>.012 else 0)
 boundary=list(range(n+1))+[j*(n+1)+n for j in range(1,ny+1)]+[ny*(n+1)+i for i in range(n-1,-1,-1)]+[j*(n+1) for j in range(ny-1,0,-1)]
 bottom=[]
 for a in boundary:bottom.append(len(v));v.append((v[a][0],v[a][1],.003))
 center=len(v);v.append((0,0,.003))
 for k,a in enumerate(boundary):kk=(k+1)%len(boundary);faces.extend([(a,bottom[k],bottom[kk],boundary[kk]),(center,bottom[kk],bottom[k])]);mi.extend([2,2])
 p=Part('six-metre continuous low-gradient tidal-flat patch with connected runnels',m);p.add(v,faces,mi);o=p.finish(c,True)
 # Original smooth palette tint in mesh vertices, no image or UV map.
 for poly in o.data.polygons:poly.material_index=0
 o.data.materials.clear();o.data.materials.append(m[0]);m[0].diffuse_color=(1,1,1,1);m[0]['palette_srgb']='#FFFFFF';bsdf=m[0].node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(1,1,1,1);node=m[0].node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='ChannelTint';m[0].node_tree.links.new(node.outputs['Color'],bsdf.inputs['Base Color'])
 tint=o.data.color_attributes.new(name='ChannelTint',type='FLOAT_COLOR',domain='POINT')
 def lin(x):return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
 bank=[lin(x/255) for x in (174,163,140)];mud=[lin(x/255) for x in (140,153,140)];cut=[lin(x/255) for x in (148,139,119)]
 for i,data in enumerate(tint.data):
  f=min(1,depths[i]/.043) if i<len(depths) else 0;col=[bank[k]*(1-f)+mud[k]*f for k in range(3)] if i<len(depths) else cut;data.color=(*col,1)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='tidal-flat');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='tidal-flat';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#AEA38C', '#8C998C', '#948B77'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic coastal tidal flat process analogue; no ancient site or co-occurrence claim','habitat_zh':'通用海岸潮坪过程类比；不指定古地点或共存生态','claim_scope':brief['claim_scope'],'surface_profile':'original smoothly interpolated vertex palette; zero image textures','export_helper':'private asset_common_color.py enables ACTIVE vertex colors; shared pipeline unchanged','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Geological-form artistic concept: six-metre-wide low-gradient landscape teaching patch. One continuous surface carries a shallow winding main runnel and three connected tributaries merging downhill toward the front outlet; channel depth is actual geometry, and the muted darker mud palette is not a water simulation. Original nominal spacing, slope, crop thickness and colors; not a complete shoreline survey, a measured prehistoric terrain, or a hand-scale rock. Original scale_class landscape and coast biome preserved.','zh':'地质形态艺术概念：六米宽低坡 landscape 教学片区。连续表面包含一条浅弯主沟及三条向前出口汇流的支沟；沟深来自实际几何，柔和深色泥面不是水体模拟。沟间距、坡度、截取厚度及色彩为原创名义设定，不是完整海岸测绘、实测史前地形或手掌小石。保留原始scale_class landscape及coast生境。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Representative six-metre tidal-flat teaching patch','zh':'六米代表性潮坪教学片区'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH26_COMPLETE',s)
if __name__=='__main__':main()
