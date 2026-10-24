# SPDX-License-Identifier: MIT
"""Four exact-GLB proof views, with the canonical helper's neutral light recipe.
Rendering is CPU evidence only, not a WebGL or GPU acceptance result.
"""
from pathlib import Path
import argparse, hashlib, json, sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import asset_common as common

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--glb',required=True,type=Path);ap.add_argument('--output-dir',required=True,type=Path);ap.add_argument('--report',required=True,type=Path);ap.add_argument('--clay',action='store_true');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    params=json.loads((Path(__file__).resolve().parents[1]/'params.json').read_text());cfg=params['render']
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(args.glb.resolve()))
    scene=bpy.context.scene; imported=list(scene.objects)
    coll=bpy.data.collections.new('EXACT_GLB');scene.collection.children.link(coll)
    for obj in imported:
        for c in list(obj.users_collection):c.objects.unlink(obj)
        coll.objects.link(obj)
    points=common._vertices_world(coll);low,high=common._bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
    tri=sum(len(o.data.polygons) if all(len(p.vertices)==3 for p in o.data.polygons) else sum(len(p.vertices)-2 for p in o.data.polygons) for o in imported if o.type=='MESH')
    resolution=cfg['clay_resolution'] if args.clay else cfg['resolution'];samples=cfg['clay_samples'] if args.clay else cfg['samples']
    world=bpy.data.worlds.new('neutral_light');world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=resolution;scene.render.resolution_y=resolution;scene.render.resolution_percentage=100
    scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=center+Vector(direction)*span/2;common._look_at(obj,center)
    camera_data=bpy.data.cameras.new('proof_camera');camera=bpy.data.objects.new('proof_camera',camera_data);scene.collection.objects.link(camera);scene.camera=camera
    camera_data.type='ORTHO';camera_data.clip_start=max(.001,span/1000);camera_data.clip_end=span*30
    if args.clay:bpy.context.view_layer.material_override=common.make_material('gray_proof','#929292',roughness=.85)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    manifest={'source':'Clean import of delivered GLB','glb_sha256':sha(args.glb),'renderer_sha256':sha(__file__),'blender_version':bpy.app.version_string,'engine':'Cycles CPU','gpu_claim':'UNKNOWN','projection':'orthographic; perspective role is declared three-quarter oblique','samples':samples,'resolution':[resolution,resolution],'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'clay_override':args.clay,'imported_triangles':tri,'imported_bounds_blender_m':{'min':low,'max':high},'views':{}}
    for label,xyz in cfg['camera_directions'].items():
        direction=Vector(xyz).normalized();camera.location=center+direction*span*4;common._look_at(camera,center);bpy.context.view_layer.update()
        inv=camera.matrix_world.inverted();proj=[inv@p for p in points];width=max(v.x for v in proj)-min(v.x for v in proj);height=max(v.y for v in proj)-min(v.y for v in proj)
        shift=Vector(((max(v.x for v in proj)+min(v.x for v in proj))/2,(max(v.y for v in proj)+min(v.y for v in proj))/2,0))
        camera.location+=camera.matrix_world.to_3x3()@shift;camera_data.ortho_scale=max(width,height,.05)*1.25
        out=args.output_dir/(label+'.png');scene.render.filepath=str(out);bpy.ops.render.render(write_still=True)
        manifest['views'][label]={'file':label+'.png','sha256':sha(out),'bytes':out.stat().st_size,'direction_blender':xyz,'camera_location_blender_m':list(camera.location),'camera_rotation_euler_rad':list(camera.rotation_euler),'ortho_scale_m':camera_data.ortho_scale}
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(manifest,indent=2)+'\n')
    print('VIEWS_COMPLETE',manifest['glb_sha256'])
if __name__=='__main__':main()
