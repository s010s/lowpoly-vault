# SPDX-License-Identifier: MIT
"""Run inside Blender on model.blend; quantitative checks, not species acceptance."""
import bpy,json,sys,hashlib,math
from pathlib import Path
from mathutils import Vector
argv=sys.argv[sys.argv.index('--')+1:];root=Path(argv[0]);out=Path(argv[1]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(root/'model.blend'))
objs=list(bpy.data.collections['EXPORT'].all_objects);meshes=[o for o in objs if o.type=='MESH'];names=[o.name for o in meshes]
checks={};measurements={}
for side in ['R','L']:
    checks['five_manual_digits_'+side]=sum(n.startswith('21_ManualDigit_'+side+'_') for n in names)==5
    checks['four_pedal_digits_'+side]=sum(n.startswith('14_PedalDigit_'+side+'_') for n in names)==3 and '16_MedialDigitI_'+side in names
    for prefix in ['11_Thigh_','12_LongShin_','18_UpperArm_','19_Forearm_']:
        checks[prefix+side]=prefix+side in names
    thigh=bpy.data.objects['11_Thigh_'+side];shin=bpy.data.objects['12_LongShin_'+side]
    height=lambda o:max(v.co.z for v in o.data.vertices)-min(v.co.z for v in o.data.vertices)
    measurements['thigh_vertical_span_'+side]=height(thigh);measurements['shin_vertical_span_'+side]=height(shin)
    checks['shin_taller_than_thigh_'+side]=height(shin)>height(thigh)*1.15
points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
lo=[min(v[i] for v in points) for i in range(3)];hi=[max(v[i] for v in points) for i in range(3)];size=[hi[i]-lo[i] for i in range(3)]
checks['two_metre_display_length']=abs(size[1]-2)<1e-5
checks['ground_height_zero']=abs(lo[2])<1e-6
checks['no_preview_scene_helpers']=not any(o.type in ['CAMERA','LIGHT'] or o.name.startswith('_preview') for o in bpy.data.objects)
checks['positive_mesh_determinants']=all(o.matrix_world.determinant()>0 for o in meshes)
checks['single_identity_root']=sum(o.type=='EMPTY' for o in objs)==1 and all(abs(bpy.data.objects['hypsilophodon'].matrix_world[i][j]-(1 if i==j else 0))<1e-7 for i in range(4) for j in range(4))
checks['no_external_resources']=not bpy.data.libraries and not bpy.data.images and not bpy.data.fonts and not bpy.data.sounds
checks['no_animation_or_rig']=not bpy.data.actions and not bpy.data.armatures
body=bpy.data.objects['01_Continuous_ShortNeck_DeepTrunk_Tail'];tail=[v.co.z for v in body.data.vertices if v.co.y>.50]
measurements['tail_min_surface_height_m']=min(tail);checks['tail_not_ground_support']=min(tail)>.45
measurements.update(bounds_blender_m={'min':lo,'max':hi,'size':size},editable_mesh_parts=len(meshes))
checks['relative_render_path']=bpy.context.scene.render.filepath.startswith('//')
out.write_text(json.dumps({'status':'PASS' if all(checks.values()) else 'FAIL','blend_sha256':sha(root/'model.blend'),'glb_sha256':sha(root/'model.glb'),'checks':checks,'measurements':measurements,'scope':'Counted actual saved semantic meshes and measured actual source bounds. Digit arrangement, clean visual joints, taxonomic identity and scientific accuracy still require image/reference review; disconnected overlapping components are not a printable union.'},indent=2)+'\n')
if not all(checks.values()):raise RuntimeError(checks)
