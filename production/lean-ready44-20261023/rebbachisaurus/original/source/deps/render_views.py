# SPDX-License-Identifier: MIT
"""Four orthographic views from a clean import of the delivered GLB only."""
import argparse, hashlib, json, math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
import asset_common as ac


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('glb',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--resolution',type=int,default=768)
    parser.add_argument('--samples',type=int,default=48)
    parser.add_argument('--clay',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    ac.setup_scene('exact-glb-views')
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(args.glb.resolve()))
    imported=[o for o in bpy.data.objects if o not in before]
    bpy.context.view_layer.update()
    points=[o.matrix_world@v.co for o in imported if o.type=='MESH' for v in o.data.vertices]
    low,high=ac._bounds(points);center=Vector([(a+b)/2 for a,b in zip(low,high)])
    radius=max((v-center).length for v in points)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU'
    scene.cycles.samples=args.samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=args.resolution
    scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
    scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Studio-world');world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    lighting=[]
    for name,vec,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.shape='DISK'
        data.energy=power*radius*radius;data.size=size*radius
        obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj)
        obj.location=center+Vector(vec)*radius;ac._look_at(obj,center)
        lighting.append({'name':name,'direction':vec,'energy':data.energy,'size':data.size})
    if args.clay:
        material=ac.make_material('Diagnostic-clay','#94958F')
        for obj in imported:
            if obj.type=='MESH':
                obj.data.materials.clear();obj.data.materials.append(material)
                for face in obj.data.polygons:face.material_index=0
    camera_data=bpy.data.cameras.new('Camera');camera=bpy.data.objects.new('Camera',camera_data)
    scene.collection.objects.link(camera);scene.camera=camera;camera_data.type='ORTHO'
    camera_data.clip_start=.001;camera_data.clip_end=radius*40
    views={};directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    for label,direction in directions.items():
        camera.location=center+Vector(direction).normalized()*radius*4
        ac._look_at(camera,center);bpy.context.view_layer.update()
        inv=camera.matrix_world.inverted();screen=[inv@v for v in points]
        x0=min(v.x for v in screen);x1=max(v.x for v in screen)
        y0=min(v.y for v in screen);y1=max(v.y for v in screen)
        offset=Vector(((x0+x1)/2,(y0+y1)/2,0))
        camera.location+=camera.matrix_world.to_3x3()@offset
        camera_data.ortho_scale=max(x1-x0,y1-y0)*1.14
        scene.render.filepath=str(out/(label+'.png'));bpy.ops.render.render(write_still=True)
        views[label]={'path':label+'.png','sha256':digest(out/(label+'.png')),'direction_blender':list(direction),
            'camera_location_blender_m':list(camera.location),'orthographic_scale':camera_data.ortho_scale}
    report={'scope':'Exact delivered GLB clean-import Blender CPU render, not browser/GPU or independent visual approval',
        'glb_sha256':digest(args.glb),'renderer_sha256':digest(__file__),'helper_sha256':digest(Path(__file__).with_name('asset_common.py')),
        'blender_version':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'resolution':[args.resolution,args.resolution],
        'samples':args.samples,'denoising':False,'transparent':True,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},
        'lighting':lighting,'world_strength':.3,'clay':args.clay,'views':views,
        'bounds_blender_m':{'min':low,'max':high},'images':len(views)}
    (out/'render-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
