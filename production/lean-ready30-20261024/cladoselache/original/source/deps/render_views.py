# SPDX-License-Identifier: MIT
"""Clean-import four-view evidence for the exact delivered GLB."""
from pathlib import Path
import argparse, hashlib, json, sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene, link_object, make_material, srgb_to_linear, _vertices_world, _bounds, _look_at

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('glb',type=Path); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--report',type=Path,required=True); ap.add_argument('--resolution',type=int,default=768); ap.add_argument('--samples',type=int,default=24); ap.add_argument('--clay',action='store_true'); a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    a.output.mkdir(parents=True,exist_ok=True)
    col=setup_scene('cladoselache-view'); root=bpy.data.objects[col['asset_root']]
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=str(a.glb))
    imported=set(bpy.data.objects)-before
    for obj in imported: link_object(obj,col,parent=False)
    for obj in imported:
        if obj.parent not in imported:
            w=obj.matrix_world.copy();obj.parent=root;obj.matrix_world=w
    scene=bpy.context.scene; points=_vertices_world(col); low,high=_bounds(points); center=Vector([(low[i]+high[i])/2 for i in range(3)]); span=max(high[i]-low[i] for i in range(3))
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=a.resolution;scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;nodes=world.node_tree.nodes;links=world.node_tree.links
    bg=nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
    camera_bg=nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(c/255) for c in (232,228,220))+(1,);camera_bg.inputs['Strength'].default_value=1
    lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(bg.outputs[0],mix.inputs[1]);links.new(camera_bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs['Surface']);scene.world=world
    lighting=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        ld=bpy.data.lights.new(name,'AREA');ld.energy=energy*span*span/4;ld.shape='DISK';ld.size=size*span/2;lo=bpy.data.objects.new(name,ld);scene.collection.objects.link(lo);lo.location=center+Vector(direction)*span/2;_look_at(lo,center);lighting.append({'name':name,'direction':direction,'energy':ld.energy,'size':ld.size})
    cd=bpy.data.cameras.new('proof-camera');cam=bpy.data.objects.new('proof-camera',cd);scene.collection.objects.link(cam);cd.type='ORTHO';cd.clip_start=.001;cd.clip_end=span*30;scene.camera=cam
    if a.clay: bpy.context.view_layer.material_override=make_material('clay','#A0A0A0')
    frames=[]
    for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();p=[inv@v for v in points]
        lo=[min(v[i] for v in p) for i in range(2)];hi=[max(v[i] for v in p) for i in range(2)];shift=Vector(((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0));cam.location+=cam.matrix_world.to_3x3()@shift;cd.ortho_scale=max(hi[i]-lo[i] for i in range(2))*1.16
        dest=a.output/(name+'.png');scene.render.filepath=str(dest);bpy.ops.render.render(write_still=True);frames.append({'view':name,'file':name+'.png','sha256':sha(dest),'direction_blender':direction,'camera_location_m':list(cam.location),'camera_rotation_radians':list(cam.rotation_euler),'orthographic_scale':cd.ortho_scale})
    report={'check':'exact-glb-clean-import-four-view-render','status':'COMPLETE_NOT_INDEPENDENT_REVIEW','glb_sha256':sha(a.glb),'renderer_sha256':sha(Path(__file__)),'helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'blender_version':bpy.app.version_string,'engine':'Cycles CPU','gpu_claim':'UNKNOWN','resolution':[a.resolution,a.resolution],'samples':a.samples,'clay_override':a.clay,'background_srgb':'#E8E4DC','world_strength':.3,'lighting':lighting,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'imported_bounds_blender_m':{'min':low,'max':high},'frames':frames}
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
