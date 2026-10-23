#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Canonical exact-GLB Cycles views, using the pinned project's neutral lighting recipe.
Inspection images are not website-render or target GPU evidence.
"""
from pathlib import Path
import argparse,hashlib,json,sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_look_at,_vertices_world,_bounds

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main(a):
    source=a.glb.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    col=setup_scene('exact-export-view');root=bpy.data.objects[col['asset_root']]
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(source));imported=[o for o in bpy.data.objects if o not in before]
    for o in imported:link_object(o,col,parent=False)
    for o in imported:
        if o.parent not in imported:m=o.matrix_world.copy();o.parent=root;o.matrix_world=m
    bpy.context.view_layer.update();points=_vertices_world(col);low,high=_bounds(points)
    center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
    scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-preview-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    lighting=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new('preview-'+name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        ob=bpy.data.objects.new('preview-'+name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
        lighting.append({'name':name,'direction':list(direction),'energy':data.energy,'size':data.size})
    cd=bpy.data.cameras.new('preview-camera');camera=bpy.data.objects.new('preview-camera',cd);scene.collection.objects.link(camera);scene.camera=camera;cd.type='ORTHO';cd.clip_start=.01;cd.clip_end=span*30
    if a.clay:bpy.context.view_layer.material_override=make_material('gray-form-check','#939393',.85)
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)};frames=[]
    for view in a.views.split(','):
        direction=Vector(directions[view]).normalized();camera.location=center+direction*span*4;_look_at(camera,center);bpy.context.view_layer.update()
        inv=camera.matrix_world.inverted();p=[inv@v for v in points];minx,maxx=min(v.x for v in p),max(v.x for v in p);miny,maxy=min(v.y for v in p),max(v.y for v in p)
        camera.location+=camera.matrix_world.to_3x3()@Vector(((minx+maxx)/2,(miny+maxy)/2,0));cd.ortho_scale=max(maxx-minx,maxy-miny)*1.16
        scene.render.filepath=str(out/(view+'.png'));bpy.ops.render.render(write_still=True)
        frames.append({'path':view+'.png','sha256':digest(out/(view+'.png')),'direction_blender':directions[view],'camera_position_blender_m':list(camera.location),'camera_rotation_xyz_radians':list(camera.rotation_euler),'orthographic_scale':cd.ortho_scale})
    tris=0
    for o in imported:
        if o.type=='MESH':o.data.calc_loop_triangles();tris+=len(o.data.loop_triangles)
    report={'asset_id':'guanlong','revision':'r001','glb_sha256':digest(source),'renderer_sha256':digest(__file__),'helper_sha256':digest(Path(__file__).with_name('asset_common.py')),'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'resolution':[a.resolution,a.resolution],'samples':a.samples,'transparent':True,'clay_override':a.clay,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'lighting':lighting,'world_strength':.3,'camera_framing':'Per-view projection fit, 1.16 margin; unchanged metric geometry.','camera_type':'ORTHO','imported_bounds_blender_m':{'min':low,'max':high},'imported_triangles':tris,'frames':frames,'claim_scope':'Clean import of the exact GLB and view generation only; not independent inspection or WebGL evidence.','website_reuse':False,'website_reuse_reason':'Canonical Cycles inspection recipe differs from the website renderer and camera contract.'}
    (out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--views',default='front,side,top,perspective');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=32);p.add_argument('--clay',action='store_true');main(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
