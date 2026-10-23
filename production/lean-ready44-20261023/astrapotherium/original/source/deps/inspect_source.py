# SPDX-License-Identifier: MIT
"""Reopen editable source and clean-import the exact exported GLB for technical checks."""
from pathlib import Path
import argparse,hashlib,json,sys
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import audit_source,_vertices_world,_bounds
ap=argparse.ArgumentParser();ap.add_argument('--blend',type=Path,required=True);ap.add_argument('--glb',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(a.blend.resolve()));col=bpy.data.collections['EXPORT'];before=audit_source(col,16000)
root=bpy.data.objects[col['asset_root']]
root_identity=all(abs(root.matrix_world[i][j]-(1. if i==j else 0.))<1e-7 for i in range(4) for j in range(4))
source_forms=bpy.data.collections['SOURCE_FORMS']
scene_clean=not any(o.type in ['CAMERA','LIGHT'] for o in bpy.context.scene.objects) and '_PREVIEW_ONLY' not in bpy.data.collections
external_files={'libraries':[x.name for x in bpy.data.libraries],'file_images':[x.name for x in bpy.data.images if x.source=='FILE'],'file_fonts':[x.name for x in bpy.data.fonts if x.filepath and x.filepath!='<builtin>']}
meshes={o.name:o for o in col.all_objects if o.type=='MESH'}
canines={n:o for n,o in meshes.items() if '_canine_' in n}
volumes={};bvh={}
for name,ob in meshes.items():
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));volumes[name]=bm.calc_volume(signed=True);bm.free()
    if name in canines:
        ob.data.calc_loop_triangles();bvh[name]=BVHTree.FromPolygons([ob.matrix_world@v.co for v in ob.data.vertices],[list(t.vertices) for t in ob.data.loop_triangles],all_triangles=True)
intersections=[];names=sorted(canines)
for i,n in enumerate(names):
    for other in names[i+1:]:
        overlaps=bvh[n].overlap(bvh[other])
        intersections.append({'first':n,'second':other,'triangle_overlaps':len(overlaps)})
body=meshes['Continuous_original_body_surface'];ground={}
for sign,label in [(-1,'L'),(1,'R')]:
    for leg,ymin,ymax in [('fore',-.75,-.30),('hind',.65,1.20)]:
        points=[v.co for v in body.data.vertices if sign*v.co.x>.12 and ymin<v.co.y<ymax and v.co.z<.2]
        ground[label+'_'+leg]=min(v.z for v in points)
upper_count=sum(n.startswith('Upper_canine_') for n in canines);lower_count=sum(n.startswith('Lower_canine_') for n in canines)
source_info={'report':before,'root_identity':root_identity,'scene_has_no_preview_cameras_lights':scene_clean,'source_forms_count':len(source_forms.objects),'source_forms_excluded_from_export':all(o not in set(col.all_objects) for o in source_forms.objects),'external_files':external_files,'upper_canine_meshes':upper_count,'lower_canine_meshes':lower_count,'four_foot_ground_min_z_m':ground,'pairwise_canine_intersections':intersections,'signed_mesh_volumes_m3':volumes,'volume_scope':'Positive volume plus recalc normals inspected; distinct embedded parts are not a watertight printable union.'}
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()));pts=[];count=0
for ob in bpy.data.objects:
    if ob.type=='MESH':
        ob.data.calc_loop_triangles();count+=len(ob.data.loop_triangles);pts.extend(ob.matrix_world@v.co for v in ob.data.vertices)
low,high=_bounds(pts);source_bounds=before['bounds_blender_m'];delta=max(abs(v-source_bounds[k][i]) for k,arr in [('min',low),('max',high)] for i,v in enumerate(arr))
checks={'source_no_errors':not before['errors'],'four_canines':upper_count==lower_count==2,'no_pairwise_canine_triangle_intersection':all(x['triangle_overlaps']==0 for x in intersections),'positive_part_signed_volumes':all(x>0 for x in volumes.values()),'four_ground_contacts':all(abs(z)<.002 for z in ground.values()),'root_identity':root_identity,'clean_editable_scene':scene_clean,'no_external_source_resources':not any(external_files.values()),'source_forms_excluded':source_info['source_forms_excluded_from_export'],'roundtrip_triangle_match':count==before['triangles'],'roundtrip_bounds_match':delta<1e-5}
out={'asset_id':'astrapotherium','revision':'r001','glb_sha256':sha(a.glb),'blend_sha256':sha(a.blend),'blender':bpy.app.version_string,'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL','source':source_info,'clean_glb_import':{'triangles':count,'bounds_blender_m':{'min':low,'max':high},'max_bound_difference_m':delta},'limits':['Not independent visual acceptance.','Blender CPU import/render does not prove a browser GPU path or populated-scene performance.']}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'checks':checks}));
if not all(checks.values()):raise RuntimeError('Source-roundtrip technical check failed')
