# SPDX-License-Identifier: MIT
"""Placement-only verification: import frozen GLBs, build ephemeral neutral terrain.
blender -b -t 2 --python experiments/geology-calibration-20261019/sandstone-use-validation/render.py
No source model, export, or production file is written.
"""
import bpy,sys,math,json,hashlib
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;E=H.parent;ROOT=E.parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import make_material
SOURCES={'before':ROOT/'assets/additions/cross-bedded-sandstone/small-life-round11-20261018/cross-bedded-sandstone.glb','after':E/'cross-bedded-sandstone/cross-bedded-sandstone.glb'}
EXPECTED={'before':'1a93b06b2a9a3457f0f11bff876328dc50b5d8c2f3a7a730fe411ebc200b3ac1','after':'99864f92d2028c0a802ad8c992b8fa07d12ae7ef6e0e9ff46ef6610e45196e41'}
def mesh(name,v,f,mat):
 m=bpy.data.meshes.new(name);m.from_pydata(v,[],f);m.update();o=bpy.data.objects.new(name,m);bpy.context.scene.collection.objects.link(o);o.data.materials.append(mat);return o
records=[]
if '--bank-only' in sys.argv and (H/'render-manifest.json').exists():
 records=[r for r in json.loads((H/'render-manifest.json').read_text()) if r['scenario']!='embedded-bank']
for scenario in (['embedded-bank'] if '--bank-only' in sys.argv else ['half-buried-slope','embedded-bank']):
 for version,path in SOURCES.items():
  digest=hashlib.sha256(path.read_bytes()).hexdigest();assert digest==EXPECTED[version]
  bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
  bpy.ops.import_scene.gltf(filepath=str(path))
  # Move only imported root nodes, never author or export new geometry.
  imported=list(s.objects);shift=Vector((0,0,-.135)) if scenario=='half-buried-slope' else Vector((0,.06,.04))
  for o in imported:
   if o.parent is None:o.location+=shift
  earth=make_material('temporary-neutral-soil','#8D887B',.97)
  nx=40;ny=36;v=[];f=[]
  if scenario=='half-buried-slope':
   for j in range(ny+1):
    y=-2+4*j/ny
    for i in range(nx+1):
     x=-2.4+4.8*i/nx;z=.015+.14*y+.018*math.sin(2*x+.4)*math.cos(1.5*y)
     v.append((x,y,z))
   camera=(1.15,-2.35,1.15);target=(0,0,.12);placement='Bottom moved down 0.135 m; approximately lower 0.15 m meets rising soil. Top and front/right faces remain exposed.'
  else:
   # A steep, slightly curved bank with a rounded toe: real occlusion and
   # intersections expose whether this prop reads like an inserted slab.
   for j in range(ny+1):
    z=-.30+1.60*j/ny
    for i in range(nx+1):
     x=-1.8+3.6*i/nx;y=.10-.50*math.exp(-z/.12)-.27*(min(abs(x),.9)/.8)**2+.014*math.sin(3*x+z*2)
     v.append((x,y,z))
   camera=(1.05,-2.65,1.25);target=(0,-.02,.35);placement='Rear moved +0.06 m into bank; lower edge meets rounded soil toe, side edges meet curved wall. Main bedding face stays visible.'
  for j in range(ny):
   for i in range(nx):
    a=j*(nx+1)+i;f.append((a,a+1,a+nx+2,a+nx+1))
  terrain=mesh('TEMPORARY-PLACEMENT-ONLY-TERRAIN',v,f,earth)
  for p in terrain.data.polygons:p.use_smooth=True
  s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=False
  s.render.resolution_x=900;s.render.resolution_y=760;s.render.resolution_percentage=100
  s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
  s.world=bpy.data.worlds.new('neutral-daylight');s.world.use_nodes=True
  s.world.node_tree.nodes['Background'].inputs[0].default_value=(.42,.42,.42,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.45
  for name,loc,power,size in [('soft-key',(-3,-4,5),270,4),('soft-fill',(3,-2,3),100,4)]:
   d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
  d=bpy.data.cameras.new('eye-level-perspective');cam=bpy.data.objects.new('eye-level-perspective',d);s.collection.objects.link(cam);s.camera=cam;d.type='PERSP';d.lens=55;cam.location=camera;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
  out=H/(scenario+'-'+version+'.png');s.render.filepath=str(out);bpy.ops.render.render(write_still=True)
  records.append({'scenario':scenario,'version':version,'file':out.name,'source_glb_sha256':digest,'source_glb':str(path.relative_to(ROOT)),'asset_translation_m':list(shift),'asset_rotation':'unchanged','asset_scale':'1:1 frozen original meters','camera_m':list(camera),'target_m':list(target),'lens_mm':55,'projection':'perspective','camera_height_above_asset_ground_origin_m':camera[2],'placement':placement,'resolution':[900,760],'engine':'Cycles CPU','samples':64,'view_transform':'Standard','exposure':0,'terrain':'neutral ephemeral validation carrier, not a formal asset; no model export'})
(H/'render-manifest.json').write_text(json.dumps(records,indent=2))
