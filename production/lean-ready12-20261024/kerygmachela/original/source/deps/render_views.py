# SPDX-License-Identifier: MIT
"""Four exact-export inspection views; palette or grayscale. No source scene reuse."""
from pathlib import Path
import argparse,hashlib,json,sys,math
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('glb',type=Path);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--clay',action='store_true');ap.add_argument('--resolution',type=int,default=768);ap.add_argument('--samples',type=int,default=48);ap.add_argument('--views',default='front,side,top,perspective');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    a.output.mkdir(parents=True,exist_ok=True); glbsha=sha(a.glb)
    c=setup_scene('exact-export-inspection');root=bpy.data.objects[c['asset_root']];before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()));imported=[o for o in bpy.data.objects if o not in before]
    for o in imported:link_object(o,c,parent=False)
    for o in imported:
        if o.parent not in imported:
            m=o.matrix_world.copy();o.parent=root;o.matrix_world=m
    bpy.context.view_layer.update();points=_vertices_world(c);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);radius=max((p-center).length for p in points)
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
    s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    w=bpy.data.worlds.new('neutral-studio');w.use_nodes=True;nd=w.node_tree.nodes;li=w.node_tree.links;nd['Background'].inputs['Color'].default_value=(.75,.75,.75,1);nd['Background'].inputs['Strength'].default_value=.3
    cam_bg=nd.new('ShaderNodeBackground');cam_bg.inputs['Color'].default_value=tuple(srgb_to_linear(x/255) for x in (232,228,220))+(1,);cam_bg.inputs['Strength'].default_value=1
    lp=nd.new('ShaderNodeLightPath');mx=nd.new('ShaderNodeMixShader');li.new(lp.outputs['Is Camera Ray'],mx.inputs[0]);li.new(nd['Background'].outputs[0],mx.inputs[1]);li.new(cam_bg.outputs[0],mx.inputs[2]);li.new(mx.outputs[0],nd['World Output'].inputs['Surface']);s.world=w
    for name,d,e,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        ld=bpy.data.lights.new(name,'AREA');ld.energy=e*(2*radius)**2/4;ld.shape='DISK';ld.size=size*radius;o=bpy.data.objects.new(name,ld);s.collection.objects.link(o);o.location=center+Vector(d)*radius;_look_at(o,center)
    cd=bpy.data.cameras.new('inspection-camera');cam=bpy.data.objects.new('inspection-camera',cd);s.collection.objects.link(cam);s.camera=cam;cd.type='ORTHO';cd.clip_start=.00001;cd.clip_end=10
    if a.clay:bpy.context.view_layer.material_override=make_material('inspection-clay','#989898')
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)};frames=[]
    for name in a.views.split(','):
        direction=Vector(directions[name]).normalized();cam.location=center+direction*radius*6;_look_at(cam,center);bpy.context.view_layer.update()
        q=cam.rotation_euler.to_quaternion();right=q@Vector((1,0,0));up=q@Vector((0,1,0));xs=[(p-center).dot(right) for p in points];ys=[(p-center).dot(up) for p in points];wid=max(xs)-min(xs);hei=max(ys)-min(ys)
        projected_center=center+right*(max(xs)+min(xs))/2+up*(max(ys)+min(ys))/2;cam.location=projected_center+direction*radius*6;_look_at(cam,projected_center);cd.ortho_scale=max(wid,hei)*1.18
        target=a.output/(name+'.png');s.render.filepath=str(target);bpy.ops.render.render(write_still=True)
        frames.append({'path':name+'.png','sha256':sha(target),'camera_direction_blender':list(directions[name]),'camera_target_blender_m':list(projected_center),'orthographic_scale_m':cd.ortho_scale,'resolution':[a.resolution,a.resolution]})
    assert sha(a.glb)==glbsha
    record={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','source_glb_sha256':glbsha,'renderer_sha256':sha(__file__),'helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'renderer':'Blender Cycles CPU','version':bpy.app.version_string,'samples':a.samples,'threads':2,'clay_override':a.clay,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'world_strength':.3,'background_srgb':'#E8E4DC','source_bounds_blender_m':{'min':low,'max':high},'frames':frames,'scope':'Fresh clean import of exact delivered GLB. Not a Three.js GPU or populated-scene test.'}
    (a.output/'render-record.json').write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':main()
