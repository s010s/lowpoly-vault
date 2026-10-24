#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Isolated exact-GLB CPU renders. Does not modify or render the authoring scene."""
from pathlib import Path
import argparse,hashlib,json,sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import make_material,_bounds,_look_at

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    a=argparse.ArgumentParser();a.add_argument('glb',type=Path);a.add_argument('--output',type=Path,required=True);a.add_argument('--gray',action='store_true');a.add_argument('--resolution',type=int,default=512);a.add_argument('--samples',type=int,default=48)
    args=a.parse_args(sys.argv[sys.argv.index('--')+1:]);args.output.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(args.glb.resolve()))
    scene=bpy.context.scene;meshes=[o for o in scene.objects if o.type=='MESH'];pts=[o.matrix_world@v.co for o in meshes for v in o.data.vertices];lo,hi=_bounds(pts);target=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
    if args.gray:
        mat=make_material('clay_diagnostic','#999999',roughness=.85)
        for ob in meshes:
            ob.data.materials.clear();ob.data.materials.append(mat)
            for f in ob.data.polygons:f.material_index=0
    world=bpy.data.worlds.new('neutral_studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=args.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=args.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    for label,direction,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(label,'AREA');d.energy=power*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(label,d);scene.collection.objects.link(o);o.location=target+Vector(direction)*span/2;_look_at(o,target)
    d=bpy.data.cameras.new('evidence_camera');cam=bpy.data.objects.new('evidence_camera',d);scene.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.clip_start=.001;d.clip_end=span*30
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if args.gray:directions.pop('top')
    ext=[]
    for direction in directions.values():
        cam.location=target+Vector(direction).normalized()*span*4;_look_at(cam,target);inv=cam.rotation_euler.to_matrix().transposed();view=[inv@(Vector(v)-target) for v in pts];ext.append(max(max(v[a] for v in view)-min(v[a] for v in view) for a in (0,1)))
    d.ortho_scale=max(ext)*1.15
    receipt={'glb_sha256':sha(args.glb),'renderer_script_sha256':sha(Path(__file__)),'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'gpu_render':False,'resolution':[args.resolution,args.resolution],'samples':args.samples,'transparent':True,'gray_override':args.gray,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'orthographic_scale_m':d.ortho_scale,'target_blender_m':list(target),'views':[]}
    for name,vec in directions.items():
        cam.location=target+Vector(vec).normalized()*span*4;_look_at(cam,target);scene.render.filepath=str((args.output/(name+'.png')).resolve());bpy.ops.render.render(write_still=True);receipt['views'].append({'path':name+'.png','sha256':sha(args.output/(name+'.png')),'camera_direction_blender':list(vec),'camera_location_blender_m':list(cam.location)})
    (args.output/'render.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':main()
