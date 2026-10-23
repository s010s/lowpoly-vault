# SPDX-License-Identifier: MIT
"""Clean exact-GLB four-view renderer using the canonical palette/light helpers."""
import argparse, hashlib, json, math, sys, time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene, link_object, make_material, srgb_to_linear, _vertices_world, _bounds, _look_at
from qa_glb import audit_glb
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('glb',type=Path); ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--resolution',type=int,default=768); ap.add_argument('--samples',type=int,default=48); ap.add_argument('--gray',action='store_true')
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]); a.output.mkdir(parents=True,exist_ok=True)
    report=audit_glb(a.glb,max_triangles=24000,max_materials=6,max_primitives=16)
    assert not report['errors']
    collection=setup_scene('platyceras-exact-export-preview')
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
    imported=[ob for ob in bpy.data.objects if ob not in before]
    for ob in imported: link_object(ob,collection,parent=False)
    points=_vertices_world(collection); lo,hi=_bounds(points)
    center=Vector([(lo[i]+hi[i])/2 for i in range(3)])
    radius=max((point-center).length for point in points)
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'
    scene.cycles.samples=a.samples; scene.cycles.use_denoising=False
    scene.render.resolution_x=scene.render.resolution_y=a.resolution; scene.render.resolution_percentage=100
    scene.render.threads_mode='FIXED'; scene.render.threads=2
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'; scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'; scene.view_settings.exposure=0; scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Exact-export-neutral-world'); world.use_nodes=True; nodes=world.node_tree.nodes
    nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1); nodes['Background'].inputs['Strength'].default_value=.3
    bg=nodes.new('ShaderNodeBackground'); bg.inputs['Color'].default_value=tuple(srgb_to_linear(c/255) for c in (232,228,220))+(1,)
    bg.inputs['Strength'].default_value=1
    ray=nodes.new('ShaderNodeLightPath'); mix=nodes.new('ShaderNodeMixShader')
    world.node_tree.links.new(ray.outputs['Is Camera Ray'],mix.inputs[0]); world.node_tree.links.new(nodes['Background'].outputs[0],mix.inputs[1])
    world.node_tree.links.new(bg.outputs[0],mix.inputs[2]); world.node_tree.links.new(mix.outputs[0],nodes['World Output'].inputs['Surface']); scene.world=world
    lights=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA'); data.energy=energy*(2*radius)**2/4; data.shape='DISK'; data.size=size*radius
        ob=bpy.data.objects.new(name,data); scene.collection.objects.link(ob); ob.location=center+Vector(direction)*radius; _look_at(ob,center)
        lights.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
    data=bpy.data.cameras.new('Exact-GLB-camera'); camera=bpy.data.objects.new('Exact-GLB-camera',data); scene.collection.objects.link(camera)
    data.type='ORTHO'; data.clip_start=.00001; data.clip_end=2; scene.camera=camera
    # Same target and scale in all four views, sized against projected geometry.
    extent=0
    for direction in directions.values():
        camera.location=center+Vector(direction).normalized()*radius*6; _look_at(camera,center)
        matrix=camera.rotation_euler.to_matrix().transposed()
        projected=[matrix@(pt-center) for pt in points]
        extent=max(extent,max(v.x for v in projected)-min(v.x for v in projected),max(v.y for v in projected)-min(v.y for v in projected))
    data.ortho_scale=extent*1.17
    if a.gray: bpy.context.view_layer.material_override=make_material('Diagnostic-gray','#969696',roughness=.9)
    records=[]
    for name,direction in directions.items():
        camera.location=center+Vector(direction).normalized()*radius*6; _look_at(camera,center)
        target=a.output/(name+'.png'); scene.render.filepath=str(target); started=time.monotonic(); bpy.ops.render.render(write_still=True)
        records.append({'view':name,'file':name+'.png','sha256':digest(target),'bytes':target.stat().st_size,'camera_direction_blender':direction,
            'camera_location_blender_m':list(camera.location),'render_seconds':time.monotonic()-started})
    evidence={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','glb_sha256':digest(a.glb),'renderer_sha256':digest(__file__),
        'engine':'Blender Cycles CPU','blender_version':bpy.app.version_string,'resolution':a.resolution,'samples':a.samples,'threads':2,
        'gray_override':a.gray,'denoising':False,'camera_type':'ORTHO','ortho_scale_m':data.ortho_scale,'target_blender_m':list(center),
        'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'background':'#E8E4DC','lights':lights,
        'imported_bounds_blender_m':{'min':lo,'max':hi},'frames':records}
    (a.output/'render-manifest.json').write_text(json.dumps(evidence,indent=2)+'\n')
if __name__=='__main__': main()
