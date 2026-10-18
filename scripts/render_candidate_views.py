#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fresh exact-GLB turntable and diagnostic renders in an isolated directory.

blender -b -t 2 --python-exit-code 1 --python scripts/render_candidate_views.py -- \
    candidate.glb --output-dir /tmp/candidate-preview --revision r1
Rendering is evidence generation, never visual approval or Three.js runtime QA.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene, link_object, make_material, srgb_to_linear, _vertices_world, _bounds, _look_at
from qa_glb import audit_glb


BACKGROUND = '#E8E4DC'
DIRECTIONS = {'hero':(35,20), 'reversehero':(215,20), 'front':(0,0), 'rear':(180,0),
              'left':(270,0), 'right':(90,0), 'side':(90,0), 'top':(0,90), 'bottom':(0,-90),
              'clay':(35,20), 'clayalt':(35,20), 'clay-alt':(35,20), 'wire':(35,20), 'wireframe':(35,20), 'detail':(35,20)}


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            value.update(chunk)
    return value.hexdigest()


def save_json(path, value):
    with Path(path).open('x') as stream:
        json.dump(value,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')


def main():
    argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('glb',type=Path)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--revision',required=True)
    parser.add_argument('--brief',type=Path)
    parser.add_argument('--references',type=Path)
    parser.add_argument('--transparent',action='store_true')
    parser.add_argument('--resolution',type=int,default=256)
    parser.add_argument('--samples',type=int,default=8)
    parser.add_argument('--turntable-frames',type=int,default=24)
    parser.add_argument('--elevation',type=float,default=20)
    parser.add_argument('--base-pose-deg',type=float,default=0)
    parser.add_argument('--views',default='hero,reversehero,front,rear,left,right,top,bottom,clay,wire')
    parser.add_argument('--detail-target',help='Normalized bbox x,y,z; required when requesting detail')
    parser.add_argument('--detail-scale',type=float,default=0.45)
    parser.add_argument('--format',choices=('PNG','WEBP'),default='PNG')
    parser.add_argument('--webp-quality',type=int,default=90)
    parser.add_argument('--webp-python',default=shutil.which('python3'),help='Python with Pillow WebP support; no installation performed')
    args = parser.parse_args(argv)
    if not 32 <= args.resolution <= 4096 or not 1 <= args.samples <= 4096:
        parser.error('resolution must be 32..4096 and samples 1..4096')
    if not 0 <= args.turntable_frames <= 360:
        parser.error('turntable-frames must be 0..360; production baseline is 24–36, not a universal hard gate')
    if not math.isfinite(args.elevation) or not -89 <= args.elevation <= 89 or not math.isfinite(args.base_pose_deg):
        parser.error('Invalid camera elevation or base pose')
    if not math.isfinite(args.detail_scale) or not 0 < args.detail_scale <= 1:
        parser.error('detail-scale must be >0 and <=1')
    views = [value.strip() for value in args.views.split(',') if value.strip()]
    if len(views)!=len(set(views)) or any(view not in DIRECTIONS for view in views):
        parser.error('Duplicate or unknown diagnostic views')
    if not views and not args.turntable_frames:
        parser.error('At least one frame is required')
    detail = None
    if args.detail_target:
        try:
            detail = [float(value) for value in args.detail_target.split(',')]
        except ValueError:
            parser.error('detail-target must be three normalized numbers')
        if len(detail)!=3 or not all(math.isfinite(x) and 0<=x<=1 for x in detail):
            parser.error('detail-target must be three numbers in [0,1]')
    if 'detail' in views and detail is None:
        parser.error('A detail view requires --detail-target x,y,z chosen for this asset')
    if not 1 <= args.webp_quality <= 100:
        parser.error('webp-quality must be 1..100')
    if args.format=='WEBP':
        if not args.webp_python:
            parser.error('WEBP requires --webp-python with Pillow; PNG needs no external converter')
        subprocess.run([args.webp_python,'-c',"from PIL import features; assert features.check('webp')"],check=True)
    source = args.glb.resolve()
    output = args.output_dir.resolve()
    if output == source.parent or output in source.parents:
        parser.error('Use an isolated output directory, never the source directory or its parent')
    output.mkdir(parents=True,exist_ok=True)
    if any(output.iterdir()):
        parser.error('Output directory must be empty; previous evidence is never overwritten')
    source_hash = digest(source)
    subject = {'revision':args.revision, 'glb_sha256':source_hash,
               'brief_sha256':digest(args.brief) if args.brief else None,
               'references_sha256':digest(args.references) if args.references else None}
    exported = audit_glb(source,max_triangles=10**9,max_materials=10**6,max_primitives=10**6)
    if exported['errors']:
        raise RuntimeError('Static GLB audit failed: '+repr(exported['errors']))
    collection = setup_scene('candidate-render')
    root = bpy.data.objects[collection['asset_root']]
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(source))
    imported = [obj for obj in bpy.data.objects if obj not in before]
    for obj in imported:
        link_object(obj,collection,parent=False)
    for obj in imported:
        if obj.parent not in imported:
            matrix = obj.matrix_world.copy()
            obj.parent = root
            obj.matrix_world = matrix
    root.rotation_euler.z = math.radians(args.base_pose_deg)
    bpy.context.view_layer.update()
    points = _vertices_world(collection)
    if not points:
        raise RuntimeError('No renderable mesh vertices')
    low, high = _bounds(points)
    center = Vector([(low[i]+high[i])/2 for i in range(3)])
    radius = max((point-center).length for point in points)
    radius = max(radius,0.025)
    # One enclosing-sphere scale and target for every orbit angle avoids frame
    # pumping; diagnostics use the same scale except explicitly requested detail.
    ortho_scale = 2*radius*1.12
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = False
    scene.render.resolution_x = scene.render.resolution_y = args.resolution
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = args.transparent
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    world = bpy.data.worlds.new('_candidate_world'); world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.75,0.75,0.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.3
    camera_background=world.node_tree.nodes.new('ShaderNodeBackground')
    camera_background.inputs['Color'].default_value=tuple(srgb_to_linear(value/255) for value in (232,228,220))+(1,)
    camera_background.inputs['Strength'].default_value=1
    light_path=world.node_tree.nodes.new('ShaderNodeLightPath')
    mix=world.node_tree.nodes.new('ShaderNodeMixShader')
    world.node_tree.links.new(light_path.outputs['Is Camera Ray'],mix.inputs[0])
    world.node_tree.links.new(world.node_tree.nodes['Background'].outputs[0],mix.inputs[1])
    world.node_tree.links.new(camera_background.outputs[0],mix.inputs[2])
    world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface'])
    scene.world=world
    lighting=[]
    light_objects={}
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new('_candidate_'+name,'AREA')
        data.energy=energy*(2*radius)**2/4; data.shape='DISK'; data.size=size*radius
        obj=bpy.data.objects.new('_candidate_'+name,data); scene.collection.objects.link(obj)
        obj.location=center+Vector(direction)*radius; _look_at(obj,center)
        light_objects[name]=obj
        lighting.append({'name':name,'direction':list(direction),'energy':data.energy,'size':data.size})
    camera_data=bpy.data.cameras.new('_candidate_camera')
    camera=bpy.data.objects.new('_candidate_camera',camera_data); scene.collection.objects.link(camera)
    camera_data.type='ORTHO'; camera_data.ortho_scale=ortho_scale
    camera_data.clip_start=max(0.0001,radius/1000); camera_data.clip_end=radius*40
    scene.camera=camera
    clay=make_material('_candidate_clay','#929292',roughness=0.85)
    wire=make_material('_candidate_wire','#B5B5B5',roughness=0.85)
    wire_node=wire.node_tree.nodes.new('ShaderNodeWireframe'); wire_node.use_pixel_size=True
    wire_node.inputs['Size'].default_value=0.8
    wire_mix=wire.node_tree.nodes.new('ShaderNodeMixRGB')
    wire_mix.inputs[1].default_value=(0.47,0.47,0.47,1); wire_mix.inputs[2].default_value=(0.015,0.015,0.015,1)
    wire.node_tree.links.new(wire_node.outputs['Fac'],wire_mix.inputs[0])
    bsdf=next(node for node in wire.node_tree.nodes if node.type=='BSDF_PRINCIPLED')
    wire.node_tree.links.new(wire_mix.outputs[0],bsdf.inputs['Base Color'])
    frames=[{'id':f'turntable-{i:03d}','view':'turntable','angle_degrees':[360*i/args.turntable_frames,args.elevation]}
            for i in range(args.turntable_frames)]
    for view in views:
        semantic={'side':'right','wireframe':'wire','clay-alt':'clayalt'}.get(view,view)
        frames.append({'id':view,'view':semantic,'angle_degrees':list(DIRECTIONS[view])})
    config={'schema_version':1,'target_renderer':'blender-cycles-cpu','renderer':'Blender Cycles CPU','version':bpy.app.version_string,
            'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},
            'lighting':{'lights':lighting,'world_strength':0.3,'camera_background':BACKGROUND,
                        'clayalt_key_direction':[3,4,6]},
            'camera':{'type':'ORTHO','orthographic_scale':ortho_scale,'target_blender_m':list(center),
                      'fixed_orbit_framing':True,'elevation_deg':args.elevation,'base_pose_deg':args.base_pose_deg},
            'renderer_sha256':digest(Path(__file__)),
            'helper_sha256':digest(Path(__file__).with_name('asset_common.py')),
            'audit_helper_sha256':digest(Path(__file__).with_name('qa_glb.py')),
            'blender_version':bpy.app.version_string,'engine':'Cycles CPU','resolution':args.resolution,
            'samples':args.samples,'denoising':False,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,
            'background':'transparent' if args.transparent else BACKGROUND,'lights':lighting,'camera_type':'ORTHO','orthographic_scale':ortho_scale,
            'target_blender_m':list(center),'source_bounds_blender_m':{'min':list(low),'max':list(high)},
            'fixed_orbit_framing':True,'turntable_frames':args.turntable_frames,'elevation_deg':args.elevation,
            'base_pose_deg':args.base_pose_deg,'detail_target_normalized':detail,'detail_scale':args.detail_scale,
            'format':args.format,'webp_quality':args.webp_quality if args.format=='WEBP' else None,
            'render_threads':scene.render.threads,'render_threads_mode':scene.render.threads_mode,
            'frames':[dict(frame) for frame in frames]}
    save_json(output/'render-config.json',config)
    config_hash=digest(output/'render-config.json')
    started=time.monotonic()
    for frame in frames:
        azimuth,elevation=map(math.radians,frame['angle_degrees'])
        direction=Vector((math.sin(azimuth)*math.cos(elevation),-math.cos(azimuth)*math.cos(elevation),math.sin(elevation)))
        target=Vector([low[i]+detail[i]*(high[i]-low[i]) for i in range(3)]) if frame['view']=='detail' else center
        camera.location=target+direction*radius*6; _look_at(camera,target)
        camera_data.ortho_scale=ortho_scale*(args.detail_scale if frame['view']=='detail' else 1)
        bpy.context.view_layer.material_override=clay if frame['view'] in {'clay','clayalt'} else wire if frame['view']=='wire' else None
        light_objects['key'].location=center+Vector((3,4,6) if frame['view']=='clayalt' else (-3,-4,6))*radius
        _look_at(light_objects['key'],center)
        png=output/(frame['id']+'.png'); scene.render.filepath=str(png)
        frame_start=time.monotonic(); bpy.ops.render.render(write_still=True)
        final=png
        if args.format=='WEBP':
            final=png.with_suffix('.webp')
            subprocess.run([args.webp_python,'-c',
                "from PIL import Image; import sys; Image.open(sys.argv[1]).save(sys.argv[2],format='WEBP',quality=int(sys.argv[3]),method=6)",
                str(png),str(final),str(args.webp_quality)],check=True)
            png.unlink()
        frame.update({'path':final.name,'sha256':digest(final),'width':args.resolution,'height':args.resolution,
                      'byte_length':final.stat().st_size,'bytes':final.stat().st_size,
                      'azimuth_deg':frame['angle_degrees'][0],'elevation_deg':frame['angle_degrees'][1],
                      'wall_seconds':round(time.monotonic()-frame_start,4)})
    if digest(source)!=source_hash:
        raise RuntimeError('Source GLB changed while rendering; no completed render manifest emitted')
    if (args.brief and digest(args.brief)!=subject['brief_sha256']) or (args.references and digest(args.references)!=subject['references_sha256']):
        raise RuntimeError('Brief/references changed while rendering')
    manifest={'schema_version':1,'target_renderer':'blender-cycles-cpu','kind':'render_manifest','stage':'visual','subject':subject,
              'render_config':{'path':'render-config.json','sha256':config_hash},'frames':frames,
              'frame_count':len(frames),'source_glb_sha256':source_hash,'config_sha256':config_hash,
              'width':args.resolution,'height':args.resolution,'total_encoded_bytes':sum(x['byte_length'] for x in frames),
              'decoded_rgba_bytes_estimate':len(frames)*args.resolution**2*4,'background':'transparent' if args.transparent else BACKGROUND,
              'source_unchanged':True,'visual_review':'pending','runtime_qa':'not_run',
              'coverage_note':'Rendered coverage is described by frames; no automatic visual approval.',
              'wall_seconds':round(time.monotonic()-started,4),'created_at':datetime.now(timezone.utc).isoformat()}
    save_json(output/'render-manifest.json',manifest)
    orbit=[frame for frame in frames if frame['view']=='turntable']
    web={'version':1,'target_renderer':'blender-cycles-cpu','source_glb_sha256':source_hash,'config_sha256':config_hash,'frame_count':len(orbit),
         'width':args.resolution,'height':args.resolution,'frames':orbit,'poster_index':0 if orbit else None,
         'background':'transparent' if args.transparent else BACKGROUND,'elevation_deg':args.elevation,'base_pose_deg':args.base_pose_deg,
         'format':args.format,'total_encoded_bytes':sum(frame['byte_length'] for frame in orbit),
         'decoded_rgba_bytes_estimate':len(orbit)*args.resolution**2*4}
    save_json(output/'turntable.json',web)
    print(json.dumps({'status':'rendered_pending_review','render_manifest':str(output/'render-manifest.json'),
                      'frames':len(frames),'turntable_frames':len(orbit),'source_glb_sha256':source_hash,
                      'wall_seconds':manifest['wall_seconds']}))


if __name__=='__main__':
    main()
