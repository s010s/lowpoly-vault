#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Batch99 label-only repair; immutable original anatomy builders are reused.
Collapse only exact coordinate duplicates in the actual converted FONT mesh
before assembly. The unchanged emitter then consistently orients connected,
closed glyph shells. No tolerance, smoothing, shape change or diagnostic copy.
"""
import importlib.util,json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve()
args=sys.argv[sys.argv.index('--')+1:]
cfg=json.loads(Path(args[args.index('--config')+1]).read_text())
base_name={'monetianthus':'generate-r004.py','proterocladus':'generate-r006.py'}[cfg['asset_id']]
spec=importlib.util.spec_from_file_location('immutable_batch99_generator',HERE.with_name(base_name))
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
def text_label(M,b,size,mat,parent):
    curve=bpy.data.curves.new('enlarged-label','FONT');curve.body='ENLARGED';curve.size=size;curve.align_x='CENTER';curve.extrude=.00010;curve.resolution_u=1;curve.bevel_depth=0
    o=bpy.data.objects.new('label-conversion',curve);bpy.context.collection.objects.link(o);o.rotation_euler.x=base.pi/2;o.location=b;bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o=bpy.context.object
    vertices=[];lookup={};old_to_new={}
    for vertex in o.data.vertices:
        coordinate=tuple(o.matrix_world@vertex.co)
        if coordinate not in lookup:lookup[coordinate]=len(vertices);vertices.append(coordinate)
        old_to_new[vertex.index]=lookup[coordinate]
    faces=[tuple(old_to_new[i] for i in polygon.vertices) for polygon in o.data.polygons]
    assert all(len(set(face))==len(face) for face in faces),'Exact merge collapsed a face'
    M.add(vertices,faces,mat,'enlarged_label','display_label')
    bpy.data.objects.remove(o,do_unlink=True)
base.text_label=text_label
base.HERE=HERE
base.main()
