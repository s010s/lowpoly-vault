# SPDX-License-Identifier: MIT
"""Original deterministic batch22 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 def prism(name,axis,L,w,d,offset):
  axis=Vector(axis).normalized();u=Vector((axis.z,0,-axis.x));vv=Vector((0,1,0));center=Vector((0,0,.061))+Vector(offset)
  profile=[(-.50,-.18),(-.33,-.50),(.34,-.50),(.50,.04),(.29,.50),(-.41,.50)]
  rings=[(0,.80),(.035,.98),(.31,1.015),(.66,.985),(.965,.95),(1,.72)];v=[];f=[];mi=[]
  for j,(t,sc) in enumerate(rings):
   for k,(xx,yy) in enumerate(profile):
    # Restrained original crystal growth unevenness; no chip scatter or hardware.
    a=center+axis*((t-.5)*L)+u*(xx*w*sc*(1+.018*math.sin(j*1.7+k)))+vv*(yy*d*sc)
    if j in [0,len(rings)-1]:a+=axis*(.0008*xx+.0005*yy)
    v.append(tuple(a))
  f.append(tuple(reversed(range(6))));mi.append(2)
  for j in range(len(rings)-1):
   for k in range(6):f.append((j*6+k,j*6+(k+1)%6,(j+1)*6+(k+1)%6,(j+1)*6+k));mi.append([0,1,0,2,0,1][k])
  f.append(tuple((len(rings)-1)*6+k for k in range(6)));mi.append(1)
  p=Part(name,m);p.add(v,f,mi);o=p.finish(c,False);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();return o
 a=prism('main prismatic crystal',(0,0,1),.120,.024,.019,(0,0,0));bb=prism('penetrating twinned crystal',(.8660254,0,.5),.112,.023,.018,(.0015,.0008,.0015))
 bpy.context.view_layer.objects.active=a;a.select_set(True);bb.select_set(False)
 mod=a.modifiers.new('intentional natural penetration union','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=bb;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(bb,do_unlink=True)
 bm=bmesh.new();bm.from_mesh(a.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000003);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000003);bmesh.ops.dissolve_limit(bm,angle_limit=.025,use_dissolve_boundaries=False,verts=list(bm.verts),edges=list(bm.edges));bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000012);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(a.data);bm.free()
 a.name='one cruciform intergrown mineral solid'

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='staurolite-cross-twin');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='staurolite-cross-twin';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#8E7156', '#9C7C5E', '#80634E'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original mineral teaching/display specimen; no locality assignment','habitat_zh':'原创矿物教学展示标本，不指定产地','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Geological-form artistic concept: two unequal six-sided prismatic crystals interpenetrate around an intentional boolean-unioned growth center. Original broad facets, modest end asymmetry and softened edges; warm brown opaque mineral palette. Nominal 60-degree composition and 0.12 m scale are art choices, not measured crystal faces or a precise twin-law reconstruction. No bolts, central connector, source-media textures or matrix added.','zh':'地质形态艺术概念：两枚不等长六侧柱晶围绕有意布尔合并的交生中心贯穿连生。原创宽晶面、轻微不对称端部与柔化棱边，采用温暖棕色不透明矿物色系。约60度构图及0.12米为艺术设定，不是精确晶面测量或双晶律复原。不添加螺栓、中心连接件、来源图像贴图或围岩。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Staurolite-inspired cruciform penetration twin','zh':'十字石贯穿双晶'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH19_COMPLETE',s)
if __name__=='__main__':main()
