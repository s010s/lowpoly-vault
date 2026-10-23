# SPDX-License-Identifier: MIT
"""Exact-GLB four-view renderer, using the canonical neutral CPU studio recipe.
Canonical helpers supply color conversion, materials, bounds and camera aiming.
The perspective is explicitly (1,-1,1), as frozen in this model's brief.
"""
import argparse, hashlib, json, sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import asset_common as ac

def main(glb,out,res,samples,clay):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1.0
    collection=bpy.data.collections.new('EXACT_GLB');scene.collection.children.link(collection)
    for obj in list(scene.objects):
        for col in list(obj.users_collection):col.objects.unlink(obj)
        collection.objects.link(obj)
    points=ac._vertices_world(collection);low,high=ac._bounds(points)
    center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=res;scene.render.resolution_y=res;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    if clay:
        mat=ac.make_material('temporary-clay','#929292');bpy.context.view_layer.material_override=mat
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        light=bpy.data.objects.new(name,data);scene.collection.objects.link(light);light.location=center+Vector(direction)*span/2;ac._look_at(light,center)
    data=bpy.data.cameras.new('evidence-camera');cam=bpy.data.objects.new('evidence-camera',data);scene.collection.objects.link(cam);scene.camera=cam
    data.type='ORTHO';data.clip_start=.0001;data.clip_end=span*30
    out.mkdir(parents=True,exist_ok=True);records=[]
    for name,vec in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        direction=Vector(vec).normalized();cam.location=center+direction*span*4;ac._look_at(cam,center);bpy.context.view_layer.update()
        inv=cam.matrix_world.inverted();proj=[inv@v for v in points]
        width=max(v.x for v in proj)-min(v.x for v in proj);height=max(v.y for v in proj)-min(v.y for v in proj)
        shift=Vector(((max(v.x for v in proj)+min(v.x for v in proj))/2,(max(v.y for v in proj)+min(v.y for v in proj))/2,0))
        cam.location+=cam.matrix_world.to_3x3()@shift;data.ortho_scale=max(width,height)*1.16
        scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
        records.append({'view':name,'direction_blender':list(vec),'camera_position_m':list(cam.location),'ortho_scale_m':data.ortho_scale,'image_sha256':hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest()})
    record={'status':'RENDERED_EXACT_GLB','glb_sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','resolution':[res,res],'samples':samples,'threads':2,'transparent':True,'material_override':'neutral-clay' if clay else None,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'canonical_neutral_light_recipe':True,'camera_profile':'orthographic canonical axes plus (1,-1,1), per-view full-extents fit with 16 percent margin','renderer_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'views':records,'gpu_claim':False}
    (out/'render-record.json').write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:];p=argparse.ArgumentParser();p.add_argument('--glb',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--resolution',type=int,default=896);p.add_argument('--samples',type=int,default=32);p.add_argument('--clay',action='store_true');a=p.parse_args(args);main(a.glb.resolve(),a.output.resolve(),a.resolution,a.samples,a.clay)
