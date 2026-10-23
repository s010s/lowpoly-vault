# SPDX-License-Identifier: MIT
"""Exact-GLB canonical views; source helpers are locally vendored, no scene dependency."""
from pathlib import Path
import argparse,hashlib,json,math,sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=40)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);glb=a.glb.resolve();original=sha(glb)
    col=setup_scene('exact-export-view');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(glb));objects=[o for o in bpy.data.objects if o not in before]
    for o in objects:link_object(o,col,parent=False)
    points=_vertices_world(col);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);radius=max((p-center).length for p in points);scale=2*radius*1.10
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
    s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    world=bpy.data.worlds.new('Neutral studio');world.use_nodes=True;ns=world.node_tree.nodes;lk=world.node_tree.links
    ns['Background'].inputs['Color'].default_value=(.75,.75,.75,1);ns['Background'].inputs['Strength'].default_value=.3
    bg=ns.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in(232,228,220))+(1,);bg.inputs['Strength'].default_value=1
    lightpath=ns.new('ShaderNodeLightPath');mix=ns.new('ShaderNodeMixShader');lk.new(lightpath.outputs['Is Camera Ray'],mix.inputs[0]);lk.new(ns['Background'].outputs[0],mix.inputs[1]);lk.new(bg.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],ns['World Output'].inputs[0]);s.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*radius*radius;d.shape='DISK';d.size=size*radius;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=center+Vector(direction)*radius;_look_at(o,center);lights.append({'direction':direction,'energy':d.energy,'size':d.size})
    cd=bpy.data.cameras.new('Canonical camera');cam=bpy.data.objects.new('Canonical camera',cd);s.collection.objects.link(cam);cd.type='ORTHO';cd.ortho_scale=scale;cd.clip_start=.00001;cd.clip_end=radius*40;s.camera=cam
    if a.gray:bpy.context.view_layer.material_override=make_material('Gray shape check','#929292',roughness=.9)
    dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1),'basal':(0,0,-1)}
    if a.gray:dirs={k:dirs[k] for k in ('front','top','perspective','basal')}
    frames=[]
    for name,d in dirs.items():
        # For the basal diagnostic put both lights below, preserving physical view visibility.
        for o,l in zip([bpy.data.objects['key'],bpy.data.objects['fill']],lights):
            v=Vector(l['direction']);v.z=-abs(v.z) if name=='basal' else abs(v.z);o.location=center+v*radius;_look_at(o,center)
        cam.location=center+Vector(d).normalized()*radius*6;_look_at(cam,center)
        s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
        frames.append({'view':name,'path':name+'.png','sha256':sha(out/(name+'.png')),'camera_direction_blender':list(d),'camera_location_m':list(cam.location),'basal_light_flip':name=='basal'})
    assert sha(glb)==original
    (out/'render-manifest.json').write_text(json.dumps({'subject_glb_sha256':original,'source_unchanged':True,'renderer':'Blender Cycles CPU','blender':bpy.app.version_string,'source':'clean import of exact delivered GLB','mode':'gray diagnostic' if a.gray else 'final actual GLB','resolution':a.resolution,'samples':a.samples,'threads':2,'denoising':False,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'camera':{'projection':'orthographic','scale_m':scale,'center_m':list(center),'fixed_framing':True},'lights':lights,'frames':frames,'visual_acceptance':'pending maker inspection; no independent acceptance'},indent=2)+'\n')
if __name__=='__main__':main()
