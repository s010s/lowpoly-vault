# SPDX-License-Identifier: MIT
"""Original deterministic batch43 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 slab=Part('original-irregular-fine-sandstone-host',m)
 outline=[(-.105,-.15,.012),(.075,-.154,.012),(.121,-.125,.012),(.14,-.03,.012),(.135,.105,.012),(.087,.152,.012),(-.07,.15,.012),(-.132,.112,.012),(-.145,-.012,.012),(-.136,-.114,.012)]
 slab.sheet(outline,.014,0,axis=(0,0,1));host=slab.finish(c,False)
 bevel=host.modifiers.new('softly-worn-host-edge','BEVEL');bevel.width=.0022;bevel.segments=2;bpy.context.view_layer.objects.active=host;bpy.ops.object.modifier_apply(modifier=bevel.name)
 cast=Part('single-continuous-main-tunnel-and-palmate-terminal-broom',m)
 main=[(-.013,-.12,.018),(-.012,-.08,.0185),(-.002,-.033,.019),(.005,.015,.019)]
 curve_tube(cast,main,.0075,.0086,1,12,8)
 # Few terminal fingers share one short distal region; no recursive network.
 branches=[(-.057,.094,.0050),(-.031,.125,.0047),(.003,.131,.0045),(.036,.115,.0047),(.068,.081,.0046)]
 for j,(x,y,endr) in enumerate(branches):
  root=Vector((.003,.003+(j%2)*.004,.0189));mid=Vector((x*.43,.045+(j%2)*.003,.0191))
  pts=[tuple(root),tuple(mid),(x*.86,y-.024,.0188),(x,y,.0181)]
  curve_tube(cast,pts,.0076,endr,1,12,7)
  cast.ellipsoid((x,y,.0181),(endr,endr,endr),1,12,6)
 o=cast.finish(c,True);bpy.context.view_layer.objects.active=o
 # Actual geometric union rounds all tunnel junctions; no disconnected branch roots.
 mod=o.modifiers.new('union-continuous-fossil-relief','REMESH');mod.mode='VOXEL';mod.voxel_size=.0015;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=o.modifiers.new('gentle-sedimentary-rounding','SMOOTH');mod.factor=.55;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=o.modifiers.new('silhouette-conscious-reduction','DECIMATE');mod.ratio=.42;bpy.ops.object.modifier_apply(modifier=mod.name)
 # Keep exact nominal trace span separate from the larger presentation host.
 xs=[v.co.x for v in o.data.vertices];ys=[v.co.y for v in o.data.vertices];span=max(max(xs)-min(xs),max(ys)-min(ys));factor=.26/span
 for p in o.data.vertices:p.co.x*=factor;p.co.y*=factor;p.co.z=.018+(p.co.z-.018)*factor
 for poly in o.data.polygons:poly.material_index=1;poly.use_smooth=True
 return {'trace_display':'raised-fossil-relief','nominal_trace_span_m':.26,'presentation_host_span_m':.306,'trace_scope':'one proximal tunnel with a compact distal fan of five tapering terminal branches, displayed as original positive relief in a host slab; not an excavated specimen or named producer','junction_geometry':'Voxel-unioned closed relief mesh; roots are geometrically connected, with gently rounded junctions. Host and relief overlap as solid semantic parts.','artistic_note':'Host outline, five-finger simplification, exposure depth, nominal size and muted palette are interpretive choices; no facsimile or precise ichnospecies restoration.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='phycodes-palmate-burrow');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='phycodes-palmate-burrow';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#737B7A', '#A8AAA0'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Interpretive sedimentary trace relief; no producer or locality attribution','habitat_zh':'沉积遗迹浮雕示意，不指定制造者或地点','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original raised fossil relief: one proximal tunnel terminates in a compact five-finger broom, with actual unioned branch junctions. Muted sandstone host, nominal26 cm trace and conservative relief are artistic; no copied specimen or producer claim.','zh':'原创凸起化石浮雕：一根主管末端接紧凑五指状末枝，交汇处实际融合。灰调砂岩基底、26厘米名义遗迹跨度和起伏为美术选择，不复制标本、不指定制造者。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Phycodes palmate burrow','zh':'Phycodes 掌状潜穴'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH43_COMPLETE',s)
if __name__=='__main__':main()
