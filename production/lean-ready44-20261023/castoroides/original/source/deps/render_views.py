# SPDX-License-Identifier: MIT
"""Model-specific exact-GLB views using the canonical asset helper lighting recipe.
Canonical source: s010s/lowpoly-vault scripts/render_candidate_views.py.
The adapter uses literal canonical axes and a (1,-1,1) perspective. No GPU claim.
"""
from pathlib import Path
import argparse,hashlib,json,math,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
from qa_glb import audit_glb

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    av=sys.argv[sys.argv.index('--')+1:];ap=argparse.ArgumentParser()
    ap.add_argument('glb');ap.add_argument('--output-dir',required=True);ap.add_argument('--clay',action='store_true');ap.add_argument('--resolution',type=int,default=512);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--detail',action='store_true');args=ap.parse_args(av)
    src=Path(args.glb).resolve();out=Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
    glb_hash=sha(src);col=setup_scene('castoroides-render');root=bpy.data.objects[col['asset_root']]
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(src));imported=[o for o in bpy.data.objects if o not in before]
    for ob in imported:link_object(ob,col,parent=False)
    for ob in imported:
        if ob.parent not in imported: m=ob.matrix_world.copy();ob.parent=root;ob.matrix_world=m
    points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3));radius=max((pt-center).length for pt in points)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=args.samples;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=scene.render.resolution_y=args.resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('studio');world.use_nodes=True;n=world.node_tree.nodes;l=world.node_tree.links
    n['Background'].inputs['Color'].default_value=(.75,.75,.75,1);n['Background'].inputs['Strength'].default_value=.3
    bg=n.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
    lp=n.new('ShaderNodeLightPath');mix=n.new('ShaderNodeMixShader');l.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);l.new(n['Background'].outputs[0],mix.inputs[1]);l.new(bg.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],n['World Output'].inputs['Surface']);scene.world=world
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
    camd=bpy.data.cameras.new('camera');cam=bpy.data.objects.new('camera',camd);scene.collection.objects.link(cam);scene.camera=cam;camd.type='ORTHO';camd.clip_start=.001;camd.clip_end=span*40
    if args.clay:bpy.context.view_layer.material_override=make_material('clay','#929292')
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    if args.detail:views={'incisor-detail':(.6,-1,.14)}
    frames=[]
    for name,direction in views.items():
        target=Vector((0,-.985,.315)) if args.detail else center
        cam.location=target+Vector(direction).normalized()*span*4;_look_at(cam,target);bpy.context.view_layer.update()
        projected=[cam.matrix_world.inverted()@p for p in points]
        if args.detail:camd.ortho_scale=.31
        else:
            w=max(v.x for v in projected)-min(v.x for v in projected);h=max(v.y for v in projected)-min(v.y for v in projected)
            shift=Vector(((max(v.x for v in projected)+min(v.x for v in projected))/2,(max(v.y for v in projected)+min(v.y for v in projected))/2,0))
            cam.location+=cam.matrix_world.to_3x3()@shift;camd.ortho_scale=max(w,h)*1.18
        scene.render.filepath=str(out/(name+'.png'));t=time.monotonic();bpy.ops.render.render(write_still=True)
        frames.append({'path':name+'.png','sha256':sha(out/(name+'.png')),'direction_blender':list(direction),'camera_position':list(cam.location),'orthographic_scale':camd.ortho_scale,'width':args.resolution,'height':args.resolution,'wall_seconds':round(time.monotonic()-t,3)})
    report={'source_glb_sha256':glb_hash,'source_unchanged':sha(src)==glb_hash,'blender':bpy.app.version_string,'renderer':'Cycles CPU','GPU':'UNKNOWN','samples':args.samples,'threads':2,'clay':args.clay,'background_srgb':'#E8E4DC','color_management':'Standard / None / exposure0 / gamma1','frames':frames,'render_script_sha256':sha(__file__),'actual_import_bounds_blender_m':{'min':lo,'max':hi},'actual_import_mesh_count':sum(o.type=='MESH' for o in imported),'visual_review':'PENDING'}
    (out/'render-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print('EXACT_GLB_RENDER_OK',glb_hash)
if __name__=='__main__':main()
