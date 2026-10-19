# SPDX-License-Identifier: MIT
"""Original deterministic batch45 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 host=Part('declared-original-limestone-attachment-fragment',m)
 outline=[(-.084,0,.008),(-.078,0,.084),(-.066,0,.105),(-.043,0,.09),(-.039,0,.052),(-.046,0,.010)]
 host.sheet(outline,.033,0,axis=(0,1,0));o=host.finish(c,False);bpy.context.view_layer.objects.active=o
 b=o.modifiers.new('soft-mineral-mount-edges','BEVEL');b.width=.004;b.segments=2;bpy.ops.object.modifier_apply(modifier=b.name)
 growth=Part('one-continuous-contorted-mineral-tube-cluster',m)
 curves=[([(-.057,0,.050),(-.031,-.004,.065),(-.012,.003,.089),(.010,.007,.092),(.030,.001,.075),(.045,-.004,.082),(.049,-.002,.108),(.039,.004,.13)],.0037,.0019),([(-.013,.003,.088),(-.005,.009,.12),(-.020,.012,.14),(-.031,.009,.133)],.0028,.0016),([(.027,.001,.077),(.045,.009,.059),(.065,.015,.064),(.079,.014,.082)],.0027,.0015),([(-.031,-.004,.065),(-.029,-.020,.089),(-.013,-.034,.098),(.002,-.035,.089)],.0026,.0015)]
 for points,r0,r1 in curves:
  curve_tube(growth,points,r0,r1,1,10,7);growth.ellipsoid(points[-1],(r1,r1,r1),1,10,5)
 o=growth.finish(c,True);bpy.context.view_layer.objects.active=o
 mod=o.modifiers.new('continuous-natural-mineral-junctions','REMESH');mod.mode='VOXEL';mod.voxel_size=.0008;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=o.modifiers.new('gentle-growing-surface','SMOOTH');mod.factor=.42;mod.iterations=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=o.modifiers.new('economical-rounded-silhouette','DECIMATE');mod.ratio=.34;bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in o.data.polygons:p.material_index=1;p.use_smooth=True
 span=max(max(p.co[k] for p in o.data.vertices)-min(p.co[k] for p in o.data.vertices) for k in range(3));factor=.2/span
 for obj in c.objects:
  if obj.type=='MESH':
   for p in obj.data.vertices:p.co*=factor
 return {'nominal_mineral_growth_span_m':.2,'attachment_scope':'small original limestone wall/coating fragment included as declared display/support context; mineral cluster grows from an embedded root on its side, not an unsupported floating wire','growth_scope':'one continuously joined main curved fine tube and three subordinate branches, changing horizontal/vertical direction; simplified solid macroscopic teaching geometry','microscopic_boundary':'No central capillary bore, precise growth mechanism, chemical assay, age, locality or copied specimen claim. Ivory palette, branch layout and nominal size are artistic.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='helictite');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='helictite';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#9C9788', '#D7D5C1'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original cave-wall mineral-growth teaching concept','habitat_zh':'原创洞壁矿物生长教学概念','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'A continuous fine mineral-tube cluster bends away from vertical and forms a few subordinate curled branches. The included limestone attachment fragment is declared context. Microscopic channels and exact growth mechanisms are outside the macroscopic teaching scope.','zh':'连续细矿物管偏离竖直方向弯折，形成少量次级卷曲分枝；附带石灰岩附着碎片为明确展示支撑。微观通道及精确生长机制不在宏观教学范围内。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Helictite','zh':'卷曲石'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH45_COMPLETE',s)
if __name__=='__main__':main()
