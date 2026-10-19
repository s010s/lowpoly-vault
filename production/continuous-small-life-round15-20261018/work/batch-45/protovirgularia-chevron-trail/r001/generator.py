# SPDX-License-Identifier: MIT
"""Original deterministic batch45 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 slab=Part('original-fine-grained-relief-host',m)
 outline=[(-.070,-.16,.009),(.056,-.165,.009),(.080,-.13,.009),(.079,.11,.009),(.060,.164,.009),(-.057,.166,.009),(-.083,.125,.009),(-.085,-.11,.009)]
 slab.sheet(outline,.012,0,axis=(0,0,1));o=slab.finish(c,False);bpy.context.view_layer.objects.active=o;b=o.modifiers.new('worn-slab-margins','BEVEL');b.width=.002;b.segments=2;bpy.ops.object.modifier_apply(modifier=b.name)
 trail=Part('connected-axial-trail-and-serial-chevron-relief',m)
 def axis(t):return Vector((.011*math.sin(1.35*pi*t),-.14+.28*t,.0162))
 pts=[tuple(axis(j/90)) for j in range(91)];trail.tube(pts,[.0021]*len(pts),1,8)
 for j in range(17):
  t=.055+j*.055;p=axis(t);d=(axis(min(1,t+.001))-axis(max(0,t-.001))).normalized();u=Vector((d.y,-d.x,0));reach=.022*(.90+.10*math.sin(pi*t))
  points=[p-u*reach+d*.007,p-u*.009-d*.002,p-d*.007,p+u*.009-d*.002,p+u*reach+d*.007]
  points=[tuple(q+Vector((0,0,.0003))) for q in points];curve_tube(trail,points,.0018,.0018,1,8,3)
 o=trail.finish(c,True);bpy.context.view_layer.objects.active=o
 mod=o.modifiers.new('continuous-chevron-axis-attachments','REMESH');mod.mode='VOXEL';mod.voxel_size=.0008;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=o.modifiers.new('soft-sediment-relief-rounding','SMOOTH');mod.factor=.40;mod.iterations=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=o.modifiers.new('economical-trace-silhouette','DECIMATE');mod.ratio=.20;bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in o.data.polygons:p.material_index=1;p.use_smooth=True
 span=max(max(p.co[k] for p in o.data.vertices)-min(p.co[k] for p in o.data.vertices) for k in range(3));factor=.28/span
 for obj in c.objects:
  if obj.type=='MESH':
   for p in obj.data.vertices:p.co*=factor
 return {'trace_display':'raised-fossil-relief','nominal_trail_span_m':.28,'chevron_count':17,'trace_scope':'one narrow continuous gently curved median trail with seventeen bilateral V-shaped relief ribs; each apex joined geometrically to the axis, consistent V orientation along the axis','presentation_note':'Original host fragment, positive-relief exposure, spacing, shallow height, branch count and muted palette are artistic. No copied slab, producer identity, speed or precise behavior inference.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='protovirgularia-chevron-trail');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='protovirgularia-chevron-trail';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#777E7B', '#B2B2A3'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Interpretive raised sedimentary trail relief','habitat_zh':'沉积爬迹凸起浮雕示意','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original raised-relief trail with a narrow median axis and a continuous rhythm of bilateral V-shaped ribs. All rib apices are joined to the axis; muted host and nominal28 cm trail are artistic. No named producer, speed or copied fossil slab.','zh':'原创窄中轴与连续双侧V纹节奏的凸起遗迹浮雕，所有V尖均与轴线实际相接；灰调基底和28厘米名义爬迹跨度为美术选择，不指定制造者、速度或复制化石板。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Protovirgularia chevron trail','zh':'Protovirgularia 人字形爬迹'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH45_COMPLETE',s)
if __name__=='__main__':main()
