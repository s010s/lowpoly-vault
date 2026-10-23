# SPDX-License-Identifier: MIT
"""Four exact-GLB views, neutral standard light rig, correct millimetre framing."""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
from asset_common import setup_scene, make_material, link_object, _vertices_world, _bounds, _look_at, srgb_to_linear

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(); p.add_argument('glb',type=Path); p.add_argument('--out',type=Path,required=True)
    p.add_argument('--gray',action='store_true'); p.add_argument('--resolution',type=int,default=768); p.add_argument('--samples',type=int,default=64)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]); a.out.mkdir(parents=True,exist_ok=True)
    source_hash=sha(a.glb); col=setup_scene('exact-glb-preview')
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=str(a.glb))
    imported=[o for o in bpy.data.objects if o not in before]
    for obj in imported: link_object(obj,col,parent=False)
    points=_vertices_world(col); low,high=_bounds(points); center=Vector([(low[i]+high[i])/2 for i in range(3)])
    radius=max((v-center).length for v in points); span=2*radius
    sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=a.samples; sc.cycles.use_denoising=False
    sc.render.threads_mode='FIXED'; sc.render.threads=2
    sc.render.resolution_x=sc.render.resolution_y=a.resolution; sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGBA'; sc.render.film_transparent=False
    sc.view_settings.view_transform='Standard'; sc.view_settings.look='None'; sc.view_settings.exposure=0; sc.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral studio'); world.use_nodes=True
    bg=world.node_tree.nodes['Background']; bg.inputs['Color'].default_value=(.75,.75,.75,1); bg.inputs['Strength'].default_value=.3
    cam_bg=world.node_tree.nodes.new('ShaderNodeBackground'); cam_bg.inputs['Color'].default_value=tuple(srgb_to_linear(c/255) for c in (232,228,220))+(1,)
    lp=world.node_tree.nodes.new('ShaderNodeLightPath'); mix=world.node_tree.nodes.new('ShaderNodeMixShader')
    world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]); world.node_tree.links.new(bg.outputs[0],mix.inputs[1]); world.node_tree.links.new(cam_bg.outputs[0],mix.inputs[2]); world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface']); sc.world=world
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA'); data.energy=energy*span*span/4; data.shape='DISK'; data.size=size*span/2
        ob=bpy.data.objects.new(name,data); sc.collection.objects.link(ob); ob.location=center+Vector(direction)*span/2; _look_at(ob,center)
    data=bpy.data.cameras.new('view'); cam=bpy.data.objects.new('view',data); sc.collection.objects.link(cam); sc.camera=cam
    data.type='ORTHO'; data.ortho_scale=span*1.12; data.clip_start=span/1000; data.clip_end=span*40
    if a.gray: sc.view_layers[0].material_override=make_material('diagnostic clay','#9A9A9A',.9)
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    frames=[]
    for label,direction in views.items():
        direction=Vector(direction).normalized(); cam.location=center+direction*span*4; _look_at(cam,center)
        out=a.out/(label+'.png'); sc.render.filepath=str(out); bpy.ops.render.render(write_still=True)
        frames.append({'view':label,'path':out.name,'sha256':sha(out),'direction_blender':list(direction)})
    assert sha(a.glb)==source_hash
    manifest={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','source_glb_sha256':source_hash,'blender_version':bpy.app.version_string,
              'renderer':'Cycles CPU','threads':2,'samples':a.samples,'resolution':a.resolution,'gray':a.gray,'frames':frames,
              'camera':{'type':'ORTHO','target_blender_m':list(center),'ortho_scale_m':span*1.12},
              'bounds_blender_m':{'min':low,'max':high},'view_transform':'Standard','look':'None','background_srgb':'#E8E4DC',
              'source_unchanged':True,'render_script_sha256':sha(__file__)}
    (a.out/'render-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__': main()
