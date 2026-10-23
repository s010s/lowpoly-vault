#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Four diagnostic views from a clean import of the delivered GLB."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at,srgb_to_linear

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    pa=argparse.ArgumentParser();pa.add_argument('glb',type=Path);pa.add_argument('--out',type=Path,required=True);pa.add_argument('--gray',action='store_true');pa.add_argument('--resolution',type=int,default=768);pa.add_argument('--samples',type=int,default=40)
    a=pa.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True);gh=sha(a.glb)
    col=setup_scene('exact-export-inspection');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    for ob in [o for o in bpy.data.objects if o not in before]:link_object(ob,col,parent=False)
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
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=center+Vector(d)*span/2;_look_at(ob,center)
        lighting.append({'name':name,'direction':d,'energy':data.energy,'size':data.size})
    cam=bpy.data.objects.new('InspectionCamera',bpy.data.cameras.new('InspectionCamera'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO';cam.data.clip_start=.001;cam.data.clip_end=span*30
    if a.gray:bpy.context.view_layer.material_override=make_material('GrayDiagnostic','#939393')
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)};chosen=['front','side','perspective'] if a.gray else list(directions)
    rec={'status':'RENDERED_PENDING_VISUAL_INSPECTION','actual_imported_glb_sha256':gh,'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'threads':2,'resolution':a.resolution,'samples':a.samples,'denoising':False,'gray_override':a.gray,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'camera_type':'ORTHO','background_srgb':'#E8E4DC','renderer_sha256':sha(Path(__file__)),'canonical_helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'imported_bounds_blender_m':{'min':lo,'max':hi},'lighting':lighting,'frames':[],'gpu_runtime_status':'UNKNOWN','website_renderer_equivalence':'NOT_CLAIMED'}
    for name in chosen:
        d=Vector(directions[name]).normalized();cam.location=center+d*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();cp=[inv@p for p in points]
        xl,xh=min(p.x for p in cp),max(p.x for p in cp);yl,yh=min(p.y for p in cp),max(p.y for p in cp)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((xl+xh)/2,(yl+yh)/2,0));cam.data.ortho_scale=max(xh-xl,yh-yl)*1.19
        s.render.filepath=str((a.out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        rec['frames'].append({'view':name,'path':name+'.png','sha256':sha(a.out/(name+'.png')),'camera_direction_blender':directions[name],'camera_location_blender_m':list(cam.location),'orthographic_scale_m':cam.data.ortho_scale})
    assert sha(a.glb)==gh;(a.out/'render-evidence.json').write_text(json.dumps(rec,indent=2)+'\n')
if __name__=='__main__':main()
