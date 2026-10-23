#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Four canonical CPU evidence views from a clean import of the exact GLB.
Optional cheap clay mode emits three private authoring diagnostics, not acceptance.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import make_material,_look_at,_bounds

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=512);p.add_argument('--samples',type=int,default=32)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    scene=bpy.context.scene;meshes=[o for o in scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
    lo,hi=_bounds(points);target=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
    if a.gray:
        clay=make_material('authoring_gray','#969696',roughness=.9)
        for ob in meshes:
            ob.data.materials.clear();ob.data.materials.append(clay)
            for f in ob.data.polygons:f.material_index=0
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
    scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('evidence_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2
        o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=target+Vector(direction)*span/2;_look_at(o,target)
        lights.append({'name':name,'direction':direction,'energy':d.energy,'size':d.size})
    d=bpy.data.cameras.new('orthographic_evidence');cam=bpy.data.objects.new('orthographic_evidence',d);scene.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.clip_start=.001;d.clip_end=span*30
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if a.gray:directions.pop('top')
    extents=[]
    for direction in directions.values():
        cam.location=target+Vector(direction).normalized()*span*4;_look_at(cam,target);inv=cam.rotation_euler.to_matrix().transposed();view=[inv@(v-target) for v in points]
        extents.append(max(max(v[i] for v in view)-min(v[i] for v in view) for i in (0,1)))
    d.ortho_scale=max(extents)*1.15
    evidence={'glb_sha256':sha(a.glb),'renderer_sha256':sha(__file__),'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'gpu_render':False,'resolution':[a.resolution,a.resolution],'samples':a.samples,'transparent':True,'gray_override':a.gray,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'orthographic_scale_m':d.ortho_scale,'target_blender_m':list(target),'lights':lights,'views':[]}
    for label,direction in directions.items():
        cam.location=target+Vector(direction).normalized()*span*4;_look_at(cam,target);scene.render.filepath=str((a.output/(label+'.png')).resolve());bpy.ops.render.render(write_still=True)
        evidence['views'].append({'path':label+'.png','sha256':sha(a.output/(label+'.png')),'camera_direction_blender':list(direction),'camera_location_blender_m':list(cam.location)})
    (a.output/'render.json').write_text(json.dumps(evidence,indent=2)+'\n')
if __name__=='__main__':main()
