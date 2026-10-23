# SPDX-License-Identifier: MIT
"""Four canonical exact-GLB evidence views. No website-renderer claim."""
from pathlib import Path
import argparse, hashlib, json, sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--glb',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--clay',action='store_true');ap.add_argument('--resolution',type=int,default=640);ap.add_argument('--samples',type=int,default=48);ap.add_argument('--views',default='front,side,top,perspective')
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
    beforehash=sha(a.glb);col=setup_scene('gigatitan-render')
    prior=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    imported=[o for o in bpy.data.objects if o not in prior]
    for o in imported:link_object(o,col,parent=False)
    points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(l+h)/2 for l,h in zip(lo,hi)]);span=max(h-l for l,h in zip(lo,hi))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Studio-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.30;scene.world=world
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        light=bpy.data.objects.new(name,data);scene.collection.objects.link(light);light.location=center+Vector(direction)*span/2;_look_at(light,center)
    camera_data=bpy.data.cameras.new('Evidence-camera');camera_data.type='ORTHO';camera_data.clip_start=.0001;camera_data.clip_end=10
    camera=bpy.data.objects.new('Evidence-camera',camera_data);scene.collection.objects.link(camera);scene.camera=camera
    if a.clay:bpy.context.view_layer.material_override=make_material('Clay','#929292',roughness=.85)
    dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)};results={}
    assert set(a.views.split(',')) <= set(dirs)
    for name in a.views.split(','):
        d=dirs[name]
        camera.location=center+Vector(d).normalized()*span*4;_look_at(camera,center);bpy.context.view_layer.update();iv=camera.matrix_world.inverted();projected=[iv@p for p in points]
        xmin,xmax=min(p.x for p in projected),max(p.x for p in projected);ymin,ymax=min(p.y for p in projected),max(p.y for p in projected)
        camera.location+=camera.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));camera_data.ortho_scale=max(xmax-xmin,ymax-ymin)*1.17
        scene.render.filepath=str((a.output/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        results[name]={'path':name+'.png','sha256':sha(a.output/(name+'.png')),'direction':list(d),'camera_location_m':list(camera.location),'ortho_scale_m':camera_data.ortho_scale}
    if not a.clay:
        import shutil
        shutil.copyfile(a.output/'perspective.png',a.output/'preview.png')
    assert beforehash==sha(a.glb)
    report={'glb_sha256':beforehash,'source':'Clean import of delivered GLB, not source blend','renderer':'Blender '+bpy.app.version_string+' Cycles CPU','threads':2,'resolution':[a.resolution,a.resolution],'samples':a.samples,'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'clay':a.clay,'lights':{'world':.30,'key':{'direction':[-3,-4,6],'energy_factor':450,'size_factor':4},'fill':{'direction':[4,-1,3],'energy_factor':150,'size_factor':5}},'render_source_sha256':sha(Path(__file__)),'views':results,'website_compatibility':'NOT_CLAIMED: no website renderer/config binding; integration must use its verified renderer contract.'}
    (a.output/'render-report.json').write_text(json.dumps(report,indent=2)+'\n');print('FOUR_VIEWS_COMPLETE',beforehash)
if __name__=='__main__':main()
