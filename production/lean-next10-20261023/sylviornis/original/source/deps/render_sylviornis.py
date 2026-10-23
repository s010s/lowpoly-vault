#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exact-GLB four-view renderer, using canonical helper lighting/color conventions.
Original wrapper for Sylviornis. No source-scene preview is delivered as GLB proof.
"""
import argparse, hashlib, json, math, sys, time
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
from qa_glb import audit_glb

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    av=sys.argv[sys.argv.index('--')+1:]
    p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=48)
    a=p.parse_args(av);a.out.mkdir(parents=True,exist_ok=True)
    subject=sha(a.glb);audit=audit_glb(a.glb,max_triangles=16000,max_materials=6,max_primitives=48)
    if audit['errors']:raise RuntimeError(audit['errors'])
    c=setup_scene('sylviornis-render');root=bpy.data.objects[c['asset_root']]
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    objs=[x for x in bpy.data.objects if x not in before]
    for o in objs:link_object(o,c,parent=False)
    for o in objs:
        if o.parent not in objs:
            world=o.matrix_world.copy();o.parent=root;o.matrix_world=world
    pts=_vertices_world(c);low,high=_bounds(pts);center=Vector([(low[i]+high[i])/2 for i in range(3)])
    radius=max((v-center).length for v in pts);span=2*radius
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('_preview_world');world.use_nodes=True;n=world.node_tree.nodes;l=world.node_tree.links
    n['Background'].inputs['Color'].default_value=(.75,.75,.75,1);n['Background'].inputs['Strength'].default_value=.3
    camera_bg=n.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(x/255) for x in (232,228,220))+(1,);camera_bg.inputs['Strength'].default_value=1
    rays=n.new('ShaderNodeLightPath');mix=n.new('ShaderNodeMixShader');l.new(rays.outputs['Is Camera Ray'],mix.inputs[0]);l.new(n['Background'].outputs[0],mix.inputs[1]);l.new(camera_bg.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],n['World Output'].inputs['Surface']);scene.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new('_'+name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*radius
        obj=bpy.data.objects.new('_'+name,data);scene.collection.objects.link(obj);obj.location=center+Vector(direction)*radius;_look_at(obj,center)
        lights.append({'name':name,'direction':list(direction),'energy':data.energy,'size':data.size})
    # Deliberately no floor geometry and no baked lighting on the asset.
    data=bpy.data.cameras.new('_camera');camera=bpy.data.objects.new('_camera',data);scene.collection.objects.link(camera);scene.camera=camera
    data.type='ORTHO';data.clip_start=.0001;data.clip_end=span*40
    if a.clay:bpy.context.view_layer.material_override=make_material('_clay','#929292',roughness=.85)
    frames=[]
    for label,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        camera.location=center+Vector(direction).normalized()*span*4;_look_at(camera,center);bpy.context.view_layer.update()
        projected=[camera.matrix_world.inverted()@v for v in pts]
        minx,maxx=min(v.x for v in projected),max(v.x for v in projected);miny,maxy=min(v.y for v in projected),max(v.y for v in projected)
        camera.location+=camera.matrix_world.to_3x3()@Vector(((maxx+minx)/2,(maxy+miny)/2,0));data.ortho_scale=max(maxx-minx,maxy-miny)*1.20
        path=a.out/(label+'.png');scene.render.filepath=str(path);start=time.monotonic();bpy.ops.render.render(write_still=True)
        frames.append({'path':path.name,'sha256':sha(path),'camera_direction_blender':list(direction),'camera_location_m':list(camera.location),'orthographic_scale':data.ortho_scale,'width':a.resolution,'height':a.resolution,'samples':a.samples,'elapsed_seconds':round(time.monotonic()-start,3)})
    if sha(a.glb)!=subject:raise RuntimeError('GLB changed during rendering')
    record={'schema_version':1,'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','artifact':'model.glb','glb_sha256':subject,'kind':'exact-GLB-clay' if a.clay else 'exact-GLB-final',
    'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'threads':2,'engine':'Cycles CPU','resolution':a.resolution,'samples':a.samples,'denoising':False,
    'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'background_srgb':'#E8E4DC','world_strength':.3,'lighting':lights,'floor':False,
    'source_bounds_blender_m':{'min':low,'max':high},'frames':frames,'script_sha256':sha(__file__),'asset_common_sha256':sha(Path(__file__).with_name('asset_common.py')),
    'scope':'A clean GLB import rendered in Blender, not Three.js GPU or populated-scene validation.'}
    (a.out/'render-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':main()
