# SPDX-License-Identifier: MIT
"""Small-specimen exact-GLB four-view renderer using the project's lighting recipe.
No reference files, external textures, or presentation geometry are exported.
"""
from pathlib import Path
import argparse,hashlib,json,math,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_look_at,_bounds,_vertices_world

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output-dir',required=True,type=Path);p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=48);p.add_argument('--clay',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output_dir.mkdir(parents=True,exist_ok=False)
    before_hash=sha(a.glb);col=setup_scene('exact-export-view');before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    imported=set(bpy.data.objects)-before
    for o in imported:link_object(o,col,parent=False)
    bpy.context.view_layer.update();points=_vertices_world(col);lo,hi=_bounds(points)
    center=Vector([(lo[k]+hi[k])/2 for k in range(3)]);radius=max((v-center).length for v in points)
    ortho=2*radius*1.16;scene=bpy.context.scene
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral_studio');world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35;scene.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*(2*radius)**2/4;data.shape='DISK';data.size=size*radius
        o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=center+Vector(direction)*radius;_look_at(o,center)
        lights.append({'name':name,'direction':list(direction),'energy':data.energy,'size':data.size})
    camera_data=bpy.data.cameras.new('camera');camera=bpy.data.objects.new('camera',camera_data);scene.collection.objects.link(camera);scene.camera=camera
    camera_data.type='ORTHO';camera_data.ortho_scale=ortho;camera_data.clip_start=.00001;camera_data.clip_end=radius*40
    if a.clay:scene.view_layers[0].material_override=make_material('clay','#9B9B9B',roughness=.93)
    dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    config={'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'threads':2,'resolution':a.resolution,'samples':a.samples,'clay_override':a.clay,'transparent':True,'denoising':False,'color_management':'Standard / None / exposure0 / gamma1','world_strength':.35,'lights':lights,'camera':{'type':'ORTHO','scale':ortho,'target':list(center),'fixed_framing':True,'directions':dirs},'source_glb_sha256':before_hash,'render_script_sha256':sha(__file__),'asset_helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'source_bounds_blender_m':{'min':lo,'max':hi},'claim':'Exact GLB clean reimport; images are not GPU-runtime or scientific approval.'}
    (a.output_dir/'render-config.json').write_text(json.dumps(config,indent=2)+'\n')
    records=[]
    for name,direction in dirs.items():
        camera.location=center+Vector(direction).normalized()*radius*6;_look_at(camera,center)
        dest=a.output_dir/(name+'.png');scene.render.filepath=str(dest);start=time.monotonic();bpy.ops.render.render(write_still=True)
        records.append({'path':dest.name,'sha256':sha(dest),'bytes':dest.stat().st_size,'direction_blender':direction,'width':a.resolution,'height':a.resolution,'seconds':round(time.monotonic()-start,3)})
    assert sha(a.glb)==before_hash
    (a.output_dir/'render-manifest.json').write_text(json.dumps({'source_glb_sha256':before_hash,'config_sha256':sha(a.output_dir/'render-config.json'),'source_unchanged':True,'frames':records},indent=2)+'\n')
    print('EXACT_VIEWS_COMPLETE '+before_hash)
if __name__=='__main__':main()
