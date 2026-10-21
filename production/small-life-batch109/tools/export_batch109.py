# SPDX-License-Identifier: MIT
"""Compact batch export with compressed editable source; optional GLB-only semantic rebuild."""
import bpy,json,hashlib
from pathlib import Path
from asset_common import audit_source,LICENSE,AUTHOR
from qa_glb import audit_glb

def export_asset(slug,title,category,collection,metadata,output_root,render,max_triangles,max_materials,max_primitives,rebuild_only=False):
 out=Path(output_root)/slug;out.mkdir(parents=True,exist_ok=True);source=audit_source(collection,max_triangles)
 if source['errors']:raise RuntimeError(str(source['errors']))
 bpy.context.scene['asset_license']=LICENSE;bpy.context.scene['asset_author']=AUTHOR;bpy.context.preferences.filepaths.save_version=0
 if not rebuild_only:bpy.ops.wm.save_as_mainfile(filepath=str(out/(slug+'.blend')),compress=True)
 bpy.ops.object.select_all(action='DESELECT')
 for ob in collection.all_objects:ob.select_set(True)
 bpy.context.view_layer.objects.active=bpy.data.objects.get(collection.get('asset_root',''))
 options=dict(filepath=str(out/(slug+'.glb')),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
 bpy.ops.export_scene.gltf(**options);glb=audit_glb(out/(slug+'.glb'),max_triangles,max_materials,max_primitives)
 if glb['errors']:raise RuntimeError(str(glb['errors']))
 if source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source/export triangle mismatch')
 q=dict(schema_version=1,source=source,glb=glb,rebuild_only=rebuild_only,export_options={k:v for k,v in options.items() if k!='filepath'},source_reopen='separate test required')
 (out/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
