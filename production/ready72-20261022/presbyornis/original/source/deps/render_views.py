# SPDX-License-Identifier: MIT
"""Bounded four-view render from the caller's clean imported GLB collection."""
import bpy, hashlib, json, math
from pathlib import Path
from mathutils import Vector
from asset_common import _vertices_world,_bounds,_look_at,make_material,srgb_to_linear

def render_views(collection,out,clay=False,glb_sha256=None):
    scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'
    scene.cycles.samples=6 if clay else 32; scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED'; scene.render.threads=2
    scene.render.resolution_x=384 if clay else 900; scene.render.resolution_y=scene.render.resolution_x
    scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'; scene.view_settings.exposure=0; scene.view_settings.gamma=1
    pts=_vertices_world(collection); lo,hi=_bounds(pts); center=Vector([(lo[i]+hi[i])/2 for i in range(3)]); span=max(hi[i]-lo[i] for i in range(3))
    world=bpy.data.worlds.new('review-neutral-world'); world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5; scene.world=world
    stage=bpy.data.collections.new('RENDER_ONLY'); scene.collection.children.link(stage)
    for name,d,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),180,5),('rim',(-2,4,4),200,3)]:
        ld=bpy.data.lights.new(name,'AREA'); ld.energy=energy*span*span/4; ld.shape='DISK'; ld.size=size*span/2
        ob=bpy.data.objects.new(name,ld); stage.objects.link(ob); ob.location=center+Vector(d)*span/2; _look_at(ob,center)
    camd=bpy.data.cameras.new('review-camera'); camd.type='ORTHO'; camd.clip_start=.001; camd.clip_end=30*span
    cam=bpy.data.objects.new('review-camera',camd); stage.objects.link(cam); scene.camera=cam
    if clay:
        gray=make_material('clay','#929292'); bpy.context.view_layer.material_override=gray
    target=out/'private/clay' if clay else out/'views'; target.mkdir(parents=True,exist_ok=True)
    manifest={'source':'source scene, gray diagnostic only' if clay else 'clean import of exact delivered model.glb','glb_sha256':glb_sha256,'blender':bpy.app.version_string,'engine':'Cycles CPU','samples':scene.cycles.samples,'threads':2,'resolution':[scene.render.resolution_x]*2,'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'views':{}}
    for label,d in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        direction=Vector(d).normalized(); cam.location=center+direction*span*4; _look_at(cam,center); bpy.context.view_layer.update()
        inv=cam.matrix_world.inverted(); projected=[inv@p for p in pts]
        width=max(p.x for p in projected)-min(p.x for p in projected); height=max(p.y for p in projected)-min(p.y for p in projected)
        offset=Vector(((max(p.x for p in projected)+min(p.x for p in projected))/2,(max(p.y for p in projected)+min(p.y for p in projected))/2,0))
        cam.location+=cam.matrix_world.to_3x3()@offset; camd.ortho_scale=max(width,height)*1.20
        path=target/(label+'.png'); scene.render.filepath=str(path); bpy.ops.render.render(write_still=True)
        manifest['views'][label]={'path':str(path.relative_to(out)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'direction':list(d),'camera_location_m':list(cam.location),'target_m':list(center),'orthographic_scale_m':camd.ortho_scale}
    if not clay:
        (out/'preview.png').write_bytes((target/'perspective.png').read_bytes())
        manifest['preview_reuses']='views/perspective.png'
    path=out/'private/clay/manifest.json' if clay else out/'qa/evidence/views.json'
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(manifest,indent=2)+'\n')
