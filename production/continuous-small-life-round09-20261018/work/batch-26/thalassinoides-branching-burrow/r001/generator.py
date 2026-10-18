# SPDX-License-Identifier: MIT
"""Original deterministic batch26 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 # Gray host block is an interpretive section, not an excavated specimen replica.
 v=[(-.16,-.13,0),(.16,-.13,0),(.16,.13,0),(-.16,.13,0),(-.16,-.13,.075),(.16,-.13,.075),(.16,.13,.075),(-.16,.13,.075)];f=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
 p=Part('continuous gray host-rock teaching section',m);p.add(v,f,0);host=p.finish(c,False);bpy.context.view_layer.objects.active=host;host.select_set(True);mod=host.modifiers.new('restrained section edge rounding','BEVEL');mod.width=.0023;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 paths=[[(0,-.17,.070),(.002,-.09,.070),(.004,-.025,.070),(0,.008,.070)],[(0,-.010,.070),(-.043,.038,.070),(-.080,.084,.070),(-.120,.170,.070)],[(0,-.010,.070),(.047,.035,.070),(.091,.085,.070),(.145,.170,.070)],[(-.047,.040,.070),(-.09,.035,.070),(-.135,.037,.070),(-.19,.045,.070)]]
 cutters=[]
 for j,pts in enumerate(paths):
  p=Part('temporary tunnel volume '+str(j),m);curve_tube(p,pts,.018 if j==0 else .0165,.017 if j==0 else .0155,1,20,5);o=p.finish(c,True);cutters.append(o)
 for j,co in enumerate([(0,-.007,.070),(-.046,.039,.070)]):
  p=Part('temporary open-junction volume '+str(j),m);p.ellipsoid(co,(.020,.020,.018),1,24,12);cutters.append(p.finish(c,True))
 for o in cutters:
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 volume=cutters[0]
 for other in cutters[1:]:
  bpy.context.view_layer.objects.active=volume;volume.select_set(True);other.select_set(False);mod=volume.modifiers.new('open connected Y volume union','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=other;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(other,do_unlink=True)
 bpy.context.view_layer.objects.active=host;host.select_set(True);volume.select_set(False);mod=host.modifiers.new('connected cavities removed from host','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=volume;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(volume,do_unlink=True)
 bm=bmesh.new();bm.from_mesh(host.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000012);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(host.data);bm.free()
 for face in host.data.polygons:face.use_smooth=face.material_index==1
 host.name='gray host with exposed interconnected stout tunnel cavities'

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='thalassinoides-branching-burrow');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='thalassinoides-branching-burrow';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#A3AAA7', '#7F8D88'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Interpretive marine trace-morphology section; no producer or real excavated site','habitat_zh':'海生遗迹形态示意剖面；不指定制造者或真实出土地点','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Trace-concept artistic teaching section: continuous gray host-rock block with a unioned network of stout smooth negative tunnel cavities, two open Y junctions and section-edge outlets. The upper section plane removes the roof to expose the cavity/host relationship; dark inner surfaces are original gray palette, not floating branches, worms or filled casts. Nominal 0.32 m block width, path layout and section convention are art choices. No producer species, exact trace dimensions, behavior, excavated specimen or locality asserted.','zh':'遗迹概念艺术教学剖面：连续灰色围岩块内有经合并的粗平滑负空间隧道、两处开放Y节点与剖面边缘出口。上部剖切平面移去顶壁以显露洞腔与围岩关系；深灰内表面为原创配色，不是悬空枝条、虫体或实体充填铸型。0.32米名义块宽、路径布局与剖切方式为美术设定。不指定制造者物种、精确遗迹尺寸、行为、出土标本或地点。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Thalassinoides-inspired open-Y burrow structural section','zh':'Thalassinoides 开放Y节点潜穴结构剖面'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH26_COMPLETE',s)
if __name__=='__main__':main()
