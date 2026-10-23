# SPDX-License-Identifier: MIT
"""Four bounded exact-export views with canonical color and lighting conventions."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('glb');ap.add_argument('--output',required=True);ap.add_argument('--gray',action='store_true');ap.add_argument('--resolution',type=int,default=512);ap.add_argument('--samples',type=int,default=48)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);glb=Path(a.glb).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
    c=setup_scene('exact-export-view');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(glb))
    for ob in [o for o in bpy.data.objects if o not in before]:link_object(ob,c,parent=False)
    points=_vertices_world(c);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
    s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=not a.gray
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;s.world=world
    for name,direction,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=power*span*span/4;data.shape='DISK';data.size=size*span/2;obj=bpy.data.objects.new(name,data);s.collection.objects.link(obj);obj.location=center+Vector(direction)*span/2;_look_at(obj,center)
    camd=bpy.data.cameras.new('review-camera');cam=bpy.data.objects.new('review-camera',camd);s.collection.objects.link(cam);camd.type='ORTHO';camd.clip_start=.001;camd.clip_end=100;s.camera=cam
    if a.gray:bpy.context.view_layer.material_override=make_material('gray-clay','#929292')
    dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if a.gray:dirs={k:dirs[k] for k in ('side','front','perspective')}
    config={'renderer':'Blender Cycles CPU','blender':bpy.app.version_string,'threads':2,'samples':a.samples,'resolution':a.resolution,'gray_override':a.gray,'transparent':not a.gray,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'directions':dirs,'bounds_blender_m':{'min':lo,'max':hi},'renderer_sha256':sha(__file__),'helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'glb_sha256':sha(glb),'views':{}}
    for name,direction in dirs.items():
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();ps=[inv@p for p in points]
        xmin,xmax=min(p.x for p in ps),max(p.x for p in ps);ymin,ymax=min(p.y for p in ps),max(p.y for p in ps)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((xmax+xmin)/2,(ymax+ymin)/2,0));camd.ortho_scale=max(xmax-xmin,ymax-ymin)*1.20
        path=out/(name+'.png');s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
        config['views'][name]={'path':name+'.png','sha256':sha(path),'camera_direction':direction,'orthographic_scale':camd.ortho_scale,'camera_location':list(cam.location),'framing_margin_factor':1.20}
    (out/'render-receipt.json').write_text(json.dumps(config,indent=2)+'\n')
if __name__=='__main__':main()
