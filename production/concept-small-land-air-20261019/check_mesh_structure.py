# SPDX-License-Identifier: MIT
"""Maker technical mesh audit: direct source counts and position-welded import boundaries.
Does not repair/save any artifact or certify a printable union, anatomy or appearance.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import bpy
import bmesh

def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--glb',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    sha={k:h(v) for k,v in [('source',a.source),('glb',a.glb)]};bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()),load_ui=False,use_scripts=False)
    col=bpy.data.collections['EXPORT'];parts=[];deps=bpy.context.evaluated_depsgraph_get()
    for ob in col.all_objects:
        if ob.type!='MESH':continue
        mesh=ob.evaluated_get(deps).to_mesh();parts.append(dict(name=ob.name,authored_vertices=len(ob.data.vertices),evaluated_vertices=len(mesh.vertices),modifiers=len(ob.modifiers)));ob.evaluated_get(deps).to_mesh_clear()
    source_scene_types=sorted(o.type for o in bpy.context.scene.objects)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()));imported=[]
    coords=[ob.matrix_world@v.co for ob in bpy.context.scene.objects if ob.type=='MESH' for v in ob.data.vertices]
    tolerance=max(max(v[i] for v in coords)-min(v[i] for v in coords) for i in range(3))*1e-6
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        bm=bmesh.new();bm.from_mesh(ob.data);before=sum(e.is_boundary for e in bm.edges)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=tolerance)
        imported.append(dict(name=ob.name,boundary_edges_before_position_weld=before,boundary_edges_after_position_weld=sum(e.is_boundary for e in bm.edges),nonmanifold_edges_after_position_weld=sum(not e.is_manifold for e in bm.edges),vertices_after_position_weld=len(bm.verts)));bm.free()
    result=dict(created_at=datetime.now(timezone.utc).isoformat(),scope='maker technical self-check, not independent QA',source_sha256=sha['source'],glb_sha256=sha['glb'],source_parts=parts,authored_vertices=sum(x['authored_vertices'] for x in parts),evaluated_vertices=sum(x['evaluated_vertices'] for x in parts),source_scene_object_types=source_scene_types,imported_parts=imported,position_weld_tolerance_m=tolerance,position_weld_saved=False,input_hashes_unchanged=sha=={'source':h(a.source),'glb':h(a.glb)},limitations='Weld audit explains split-normal accessor topology only. Separate closed components intentionally overlap; this is not a printable watertight union or an outward-normal proof.')
    a.output.write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
