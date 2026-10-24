#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Canonical four-view camera wrapper: clean import of the exact delivered GLB.
Uses the adjacent pinned material, scene and look-at helpers. No source geometry
is rebuilt here, and Cycles CPU rendering does not establish a target GPU gate.
"""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=40)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True);gh=sha(a.glb)
    col=setup_scene('exact-glb-inspection');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    for o in [o for o in bpy.data.objects if o not in before]:link_object(o,col,parent=False)
    points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
    s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    world=bpy.data.worlds.new('NeutralInspection');world.use_nodes=True;s.world=world;ns=world.node_tree.nodes;ls=world.node_tree.links
    env=ns.get('Background');env.inputs['Color'].default_value=(.75,.75,.75,1);env.inputs['Strength'].default_value=.3
    bg=ns.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
    lp=ns.new('ShaderNodeLightPath');mix=ns.new('ShaderNodeMixShader');ls.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);ls.new(env.outputs[0],mix.inputs[1]);ls.new(bg.outputs[0],mix.inputs[2]);ls.new(mix.outputs[0],ns['World Output'].inputs['Surface'])
    lighting=[]
    for name,d,energy,size in [('Key',(-3,-4,6),450,4),('Fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;o=bpy.data.objects.new(name,data);s.collection.objects.link(o);o.location=center+Vector(d)*span/2;_look_at(o,center);lighting.append({'name':name,'direction':d,'energy':data.energy,'size':data.size})
    cam=bpy.data.objects.new('InspectionCamera',bpy.data.cameras.new('InspectionCamera'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO';cam.data.clip_start=.001;cam.data.clip_end=span*30
    if a.gray:bpy.context.view_layer.material_override=make_material('GrayDiagnostic','#939393')
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    rec={'status':'RENDERED_PENDING_VISUAL_INSPECTION','actual_imported_glb_sha256':gh,'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'threads':2,'resolution':a.resolution,'samples':a.samples,'denoising':False,'gray_override':a.gray,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'camera_type':'ORTHO','background_srgb':'#E8E4DC','renderer_sha256':sha(Path(__file__)),'canonical_helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'imported_bounds_blender_m':{'min':lo,'max':hi},'lighting':lighting,'frames':[],'gpu_runtime_status':'UNKNOWN','website_renderer_equivalence':'NOT_CLAIMED'}
    for name,direction in directions.items():
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();cp=[inv@v for v in points];xl,xh=min(v.x for v in cp),max(v.x for v in cp);yl,yh=min(v.y for v in cp),max(v.y for v in cp)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((xl+xh)/2,(yl+yh)/2,0));cam.data.ortho_scale=max(xh-xl,yh-yl)*1.19
        s.render.filepath=str((a.output/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        rec['frames'].append({'view':name,'path':name+'.png','sha256':sha(a.output/(name+'.png')),'camera_direction_blender':direction,'camera_location_blender_m':list(cam.location),'orthographic_scale_m':cam.data.ortho_scale})
    assert sha(a.glb)==gh;(a.output/'render-evidence.json').write_text(json.dumps(rec,indent=2)+'\n')
if __name__=='__main__':main()
