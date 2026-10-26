# SPDX-License-Identifier: MIT
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
sys.path.insert(0,str(Path(__file__).parent))
import asset_common as ac
from dorsal_geometry import build_geometry
P=argparse.ArgumentParser();P.add_argument('--config',type=Path,required=True);P.add_argument('--output-dir',type=Path,required=True);P.add_argument('--gray',action='store_true')
A=P.parse_args(sys.argv[sys.argv.index('--')+1:]);C=json.loads(A.config.read_text());OUT=A.output_dir;OUT.mkdir(exist_ok=True,parents=True)
assert bpy.app.version_string==C['blender_version']
COL=ac.setup_scene(C['asset_id'],C['seed']);root=bpy.data.objects[C['asset_id']];scene=bpy.context.scene
scene.render.threads_mode='FIXED';scene.render.threads=2
mats={k:ac.make_material(k,'#929292' if A.gray else v,roughness=.90,double_sided=False) for k,v in C['palette'].items()}
v,f,t,g,construction=build_geometry()
o=ac.mesh_object('continuous-fossil-dorsal-exoskeleton',[(x*.001,y*.001,z*.001) for x,y,z in v],f,list(mats.values()),COL)
keys=list(mats)
for p,tag in zip(o.data.polygons,t):
 c=p.center
 mat='neutral_closure' if tag=='closure' else 'axial' if tag=='axis' else 'shell'
 if tag=='head':
  y=c.y*1000;x=abs(c.x*1000);eye_x=25.5+7.2*__import__('math').sin(__import__('math').pi*max(0,min(1,(y+103)/34)))
  if -102<y<-72 and abs(x-eye_x)<2.4:mat='eye_lobe'
 p.material_index=keys.index(mat);p.use_smooth=False
for name,ids in g.items():o.vertex_groups.new(name=name).add(ids,1,'REPLACE')
o['representation']=C['representation'];o['construction']=construction['construction'];o['thoracic_tergites']=20;o['technical_underside']=construction['underside']
root['taxon']='Paradoxides davidis davidis';root['representation']=C['representation'];root['NOT_COMPLETE_LIVING_ANATOMY']=True;root['no_soft_parts_or_appendages']=True;root['technical_underside_not_anatomy']=True
# Strong single-component closed-shell source verification before the unchanged shared exporter.
bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table();seen=set();components=0
for q in bm.verts:
 if q in seen:continue
 components+=1;stack=[q];seen.add(q)
 while stack:
  a=stack.pop()
  for e in a.link_edges:
   b=e.other_vert(a)
   if b not in seen:seen.add(b);stack.append(b)
checks={'connected_components':components,'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'inconsistent_winding_edges':sum(e.is_manifold and not e.is_contiguous for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'vertices':len(bm.verts),'triangles':len(f)};bm.free()
assert components==1 and checks['nonmanifold_edges']==0 and checks['inconsistent_winding_edges']==0 and checks['signed_volume_m3']>0,checks
(OUT/'anatomical-connections.json').write_text(json.dumps({**construction,'source_topology':checks,'status':'PASS_ACTUAL_CONNECTED_INDEXED_TOPOLOGY','all_parts_in_same_closed_component':True},indent=2))
record=ac.export_asset('paradoxides',{'en':'Paradoxides davidis davidis — fossil dorsal exoskeleton reconstruction','zh':'奇异虫（化石背甲复原）'},'fossils',COL,metadata={'revision':'r001','representation':C['representation'],'description':{'en':'Original reconstructed dorsal exoskeleton;20 thoracic tergites and neutral artistic technical underside. Not a complete living animal.','zh':'原创化石背甲复原；20胸节，浅中性技术艺术封闭底面，不是完整活体。'},'reconstruction_notes':C['notes'],'generator':'scripts/build_paradoxides.py','geometry_generator':'scripts/dorsal_geometry.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'nominal_total_length_m':.24,'origin_note':'Footprint center at neutral technical underside Z0; no base, slab, or feet.','source_reference_images_incorporated':False},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'geometry_generator_sha256':hashlib.sha256((Path(__file__).parent/'dorsal_geometry.py').read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'default_area_epsilon_m2':1e-10,'named_anatomical_vertex_groups':len(g),'export_meshes':1,'glb_sha256':record['sha256']['glb'],'source_topology':checks},indent=2));print('BUILD_COMPLETE',record['sha256']['glb'])
