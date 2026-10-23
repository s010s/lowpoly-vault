# SPDX-License-Identifier: MIT
"""CPU views from a clean import of the exact GLB. No geometry or source edits."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,make_material,_look_at,_vertices_world,_bounds,link_object

def main():
    p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=640);p.add_argument('--samples',type=int,default=64);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
    col=setup_scene('cyamodus');bpy.data.objects.remove(bpy.data.objects['cyamodus'],do_unlink=True);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    for o in list(bpy.context.scene.objects):link_object(o,col,parent=False)
    points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35;scene.world=world
    for name,vec,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),190,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.size=size*span/2;obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=center+Vector(vec)*span/2;_look_at(obj,center)
    if a.gray:
        gray=make_material('gray_diagnostic','#919191',.85)
        for o in col.all_objects:
            if o.type=='MESH':
                o.data.materials.clear();o.data.materials.append(gray)
                for f in o.data.polygons:f.material_index=0
    cd=bpy.data.cameras.new('review_camera');cam=bpy.data.objects.new('review_camera',cd);scene.collection.objects.link(cam);cd.type='ORTHO';cd.clip_start=.001;cd.clip_end=30;scene.camera=cam
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if a.gray:views={k:v for k,v in views.items() if k!='side'}
    record={'scope':'ACTUAL_GLB_CPU_RENDER_ONLY','glb_sha256':hashlib.sha256(a.glb.read_bytes()).hexdigest(),'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','resolution':[a.resolution,a.resolution],'samples':a.samples,'gray_override':a.gray,'transparent':True,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'views':{}}
    for name,vec in views.items():
        cam.location=center+Vector(vec).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@x for x in points];w=max(x.x for x in proj)-min(x.x for x in proj);h=max(x.y for x in proj)-min(x.y for x in proj);shift=Vector(((max(x.x for x in proj)+min(x.x for x in proj))/2,(max(x.y for x in proj)+min(x.y for x in proj))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift;cd.ortho_scale=max(w,h)*1.16
        target=a.output/(name+'.png');scene.render.filepath=str(target);bpy.ops.render.render(write_still=True);record['views'][name]={'direction':list(vec),'camera_position':list(cam.location),'ortho_scale':cd.ortho_scale,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    (a.output/'render-record.json').write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':main()
