# SPDX-License-Identifier: MIT
"""Exact-export four-view evidence adapter using the canonical neutral light preset."""
from pathlib import Path
import argparse,sys,json,hashlib,math,time
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,_vertices_world,_bounds,_look_at,srgb_to_linear

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('glb',type=Path);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--gray',action='store_true');ap.add_argument('--resolution',type=int,default=768);ap.add_argument('--samples',type=int,default=64)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
    h=sha(a.glb); c=setup_scene('exact-export-view'); root=bpy.data.objects[c['asset_root']]
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb))
    imported=set(bpy.data.objects)-before
    for o in imported:link_object(o,c,parent=False)
    for o in imported:
        if o.parent not in imported:
            m=o.matrix_world.copy();o.parent=root;o.matrix_world=m
    points=_vertices_world(c);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=a.samples;sc.cycles.use_denoising=False
    sc.render.threads_mode='FIXED';sc.render.threads=2
    sc.render.resolution_x=sc.render.resolution_y=a.resolution;sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
    sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
    w=bpy.data.worlds.new('Neutral_world');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;sc.world=w
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2
        o=bpy.data.objects.new(name,d);sc.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
        lights.append({'name':name,'direction':direction,'energy':d.energy,'size':d.size})
    d=bpy.data.cameras.new('Evidence_camera');o=bpy.data.objects.new('Evidence_camera',d);sc.collection.objects.link(o);sc.camera=o;d.type='ORTHO';d.clip_start=.0001;d.clip_end=span*30
    dirs={'front':(0,-1,0),'side':(1,0,0),'perspective':(1,-1,1)}
    if not a.gray:dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    config={'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'camera_type':'ORTHO','color_management':'Standard / None / exposure 0 / gamma 1','transparent':True,'samples':a.samples,'resolution':[a.resolution,a.resolution],'threads':2,'lights':lights,'world_strength':.3,'renderer_sha256':sha(__file__),'canonical_helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'subject_glb_sha256':h,'camera_directions_blender':dirs,'framing':'Per-view orthographic projected bounds with constant 1.20 padding; no geometry transforms'}
    frames=[]
    for name,direction in dirs.items():
        o.location=center+Vector(direction).normalized()*span*4;_look_at(o,center);bpy.context.view_layer.update();inv=o.matrix_world.inverted();pp=[inv@p for p in points]
        xmin,xmax=min(p.x for p in pp),max(p.x for p in pp);ymin,ymax=min(p.y for p in pp),max(p.y for p in pp)
        o.location+=o.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));d.ortho_scale=max(xmax-xmin,ymax-ymin)*1.20
        f=a.output/(name+'.png');sc.render.filepath=str(f);t=time.monotonic();bpy.ops.render.render(write_still=True)
        frames.append({'view':name,'path':name+'.png','sha256':sha(f),'direction_blender':direction,'camera_location_m':list(o.location),'orthographic_scale_m':d.ortho_scale,'width':a.resolution,'height':a.resolution,'wall_seconds':round(time.monotonic()-t,3)})
    assert sha(a.glb)==h
    (a.output/'render-manifest.json').write_text(json.dumps({'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','claim_scope':'Clean import of exact GLB, CPU rendering only; not browser GPU evidence','config':config,'frames':frames},indent=2)+'\n')
if __name__=='__main__':main()
