# SPDX-License-Identifier: MIT
"""Original deterministic Arsinoitherium zitteli living reconstruction.

Run in Blender with -- --output OUTPUT --params source/params.json.
Only the relative deps directory and params file are required to rebuild.
Dimensions and all soft-tissue details are artistic estimates, not specimen data.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb


def longitudinal(name, rings, mat, col, sides=20, subdivision=1):
    """Closed anatomical loft: rings are (y, z-center, halfwidth, halfheight)."""
    verts=[]
    for y,z,w,h in rings:
        for i in range(sides):
            a=2*math.pi*i/sides
            # Full rounded upper body with a slightly contracted belly.
            lateral=1.0 if math.sin(a)>0 else 0.91
            verts.append((w*math.cos(a)*lateral,y,z+h*math.sin(a)))
    faces=[]
    for j in range(len(rings)-1):
        for i in range(sides):
            k=j*sides+i; q=j*sides+(i+1)%sides
            faces.append((k,q,q+sides,k+sides))
    faces.append(tuple(reversed(range(sides))))
    faces.append(tuple((len(rings)-1)*sides+i for i in range(sides)))
    obj=mesh_object(name,verts,faces,mat,col)
    if subdivision:
        mod=obj.modifiers.new('gentle anatomical loft refinement','SUBSURF')
        mod.subdivision_type='CATMULL_CLARK'; mod.levels=subdivision; mod.render_levels=subdivision
        bpy.context.view_layer.objects.active=obj
        obj.select_set(True); bpy.ops.object.modifier_apply(modifier=mod.name); obj.select_set(False)
    return obj


def tube(name, centers, radii, mat, col, sides=12):
    """Closed bent loft with local frames; the final vertex is a unique tip."""
    centers=[Vector(c) for c in centers]
    verts=[]
    for j,(c,r) in enumerate(zip(centers[:-1],radii[:-1])):
        tangent=(centers[min(j+1,len(centers)-1)]-centers[max(0,j-1)]).normalized()
        u=tangent.cross(Vector((0,1,0)))
        if u.length<0.01: u=tangent.cross(Vector((1,0,0)))
        u.normalize(); v=tangent.cross(u).normalized()
        rx,ry=(r,r) if isinstance(r,(int,float)) else r
        for i in range(sides):
            a=2*math.pi*i/sides
            verts.append(tuple(c+u*(rx*math.cos(a))+v*(ry*math.sin(a))))
    n=len(centers)-1
    faces=[tuple(reversed(range(sides)))]
    for j in range(n-1):
        for i in range(sides):
            k=j*sides+i; q=j*sides+(i+1)%sides
            faces.append((k,q,q+sides,k+sides))
    tip=len(verts); verts.append(tuple(centers[-1]))
    for i in range(sides): faces.append(((n-1)*sides+i,(n-1)*sides+(i+1)%sides,tip))
    return mesh_object(name,verts,faces,mat,col)


def leg(name, x, y, hind, mat, col):
    # Broad shoulder/haunch taper into an explicitly flexed short lower limb.
    levels=[(1.49,0.135,0.15,0.0),(1.36,0.21,0.23,0.0),(1.15,0.245,0.25,0.015),(0.94,0.22,0.215,0.06 if hind else -0.015),
            (0.73,0.145,0.16,0.10 if hind else 0.02),(0.53,0.13,0.14,0.05 if hind else 0.03),
            (0.31,0.145,0.16,0.00),(0.16,0.205,0.255,-0.045),(0.065,0.22,0.28,-0.07),(0.00,0.20,0.25,-0.07)]
    sides=14; verts=[]
    for z,wx,wy,dy in levels:
        for i in range(sides):
            a=2*math.pi*i/sides
            verts.append((x+wx*math.cos(a),y+dy+wy*math.sin(a),z))
    faces=[tuple(reversed(range(sides)))]
    for j in range(len(levels)-1):
        for i in range(sides):
            k=j*sides+i; q=j*sides+(i+1)%sides
            faces.append((k,q,q+sides,k+sides))
    faces.append(tuple((len(levels)-1)*sides+i for i in range(sides)))
    return mesh_object(name,verts,faces,mat,col)


def ellipsoid(name, center, scale, mat, col, sides=12, rings=6):
    cx,cy,cz=center; sx,sy,sz=scale
    verts=[(cx,cy,cz-sz)]
    for j in range(1,rings):
        p=-math.pi/2+math.pi*j/rings
        for i in range(sides):
            a=2*math.pi*i/sides
            verts.append((cx+sx*math.cos(p)*math.cos(a),cy+sy*math.cos(p)*math.sin(a),cz+sz*math.sin(p)))
    verts.append((cx,cy,cz+sz)); faces=[]
    for i in range(sides): faces.append((0,1+(i+1)%sides,1+i))
    for j in range(rings-2):
        for i in range(sides):
            k=1+j*sides+i; q=1+j*sides+(i+1)%sides
            faces.append((k,q,q+sides,k+sides))
    top=len(verts)-1; start=1+(rings-2)*sides
    for i in range(sides): faces.append((start+i,start+(i+1)%sides,top))
    return mesh_object(name,verts,faces,mat,col)


def ear(name, side, mat, inner, col):
    # Broad oval ears point outward/back, well below the pointed posterior horns.
    c=Vector((side*0.34,-0.51,1.49))
    outline=[(0,-.06,0),(.08,-.10,.03),(.19,-.08,.065),(.25,-.025,.08),(.27,.04,.06),(.23,.10,.02),(.13,.14,-.005),(.03,.10,-.03)]
    verts=[tuple(c+Vector((side*x,y,z))) for x,y,z in outline]
    verts+= [tuple(c+Vector((side*.13,.025,.055))),tuple(c+Vector((side*.12,.025,-.005)))]
    faces=[]
    n=len(outline)
    for i in range(n): faces.append((i,(i+1)%n,n)); faces.append(((i+1)%n,i,n+1))
    obj=mesh_object(name,verts,faces,[mat,inner],col)
    for p in obj.data.polygons: p.material_index=1 if p.index%2==0 else 0
    return obj


def join_parts(parts,name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]; bpy.ops.object.join(); parts[0].name=name
    bpy.ops.object.select_all(action='DESELECT')
    return parts[0]


def build(params, gray=False):
    col=setup_scene(params['asset_id'],params['seed'])
    palette=params['palette']
    skin=make_material('warm gray-brown skin', '#949494' if gray else palette['skin'],0.92)
    horn=make_material('estimated horn surface covering', '#949494' if gray else palette['horn'],0.9)
    dark=make_material('dark anatomical accents', '#949494' if gray else palette['dark'],0.96)
    nails=make_material('dull broad toenails', '#949494' if gray else palette['nails'],0.88)
    inner=make_material('ear interior', '#949494' if gray else palette['ear'],0.95)
    # Continuous snout, cranium, short neck, shoulder, deep barrel and rump.
    rings=[(-1.56,1.015,.10,.07),(-1.53,1.035,.225,.15),(-1.43,1.09,.29,.23),
           (-1.29,1.16,.325,.29),(-1.09,1.225,.365,.31),(-.89,1.26,.36,.32),
           (-.72,1.27,.315,.32),(-.59,1.27,.34,.37),(-.45,1.23,.43,.46),
           (-.27,1.205,.53,.51),(-.02,1.17,.57,.525),(.25,1.155,.58,.52),
           (.52,1.15,.56,.50),(.77,1.15,.51,.46),(1.0,1.155,.425,.385),
           (1.16,1.15,.29,.30),(1.25,1.16,.105,.145),(1.27,1.16,.035,.06)]
    longitudinal('continuous body neck and broad head',rings,skin,col,20,1)
    for side,label in [(-1,'left'),(1,'right')]:
        leg(label+' forelimb and broad foot',side*.385,-.39,False,skin,col)
        leg(label+' hindlimb and broad foot',side*.375,.83,True,skin,col)
        # A huge nasal horn pair, never tandem. Broad bases are sunk into upper face.
        centers=[(side*.205,-1.13,1.405),(side*.245,-1.205,1.53),(side*.295,-1.34,1.71),
                 (side*.345,-1.49,1.9),(side*.39,-1.64,2.075),(side*.43,-1.77,2.20),
                 (side*.46,-1.84,2.245)]
        tube(label+' enormous nasal horn',centers,[(.205,.22),(.195,.21),(.17,.19),(.135,.15),(.085,.1),(.035,.045),0],horn,col,14)
        # Small supraorbital pair at eye region, behind and separated from nasal pair.
        tube(label+' small supraorbital horn',[(side*.255,-.76,1.48),(side*.24,-.74,1.62),
            (side*.18,-.735,1.78),(side*.15,-.76,1.92),(side*.14,-.80,1.99)],
            [.105,.095,.07,.038,0],horn,col,10)
        ear(label+' lateral ear',side,skin,inner,col)
        if not gray:
            ellipsoid(label+' small lateral eye',(side*.342,-.875,1.38),(.025,.045,.036),dark,col)
            ellipsoid(label+' recessed nostril',(side*.223,-1.488,1.13),(.033,.022,.045),dark,col)
            toes=[]
            for tag,y,x in [('fore',-.39,.385),('hind',.83,.375)]:
                parts=[]
                for dx in [-.105,0,.105]:
                    parts.append(ellipsoid(label+tag+' nail', (side*x+dx,y-.294,.065),(.045,.042,.049),nails,col,10,4))
                join_parts(parts,label+' '+tag+' three understated toenails')
    # Very short lip seam, an estimated surface detail rather than separate jawbone.
    if not gray:
        tube('lower lip seam',[(-.205,-1.482,.995),(-.12,-1.55,.987),(0,-1.569,.984),(.12,-1.55,.987),(.205,-1.482,.995)],
             [.006,.008,.008,.006,0],dark,col,6)
    tube('short tapering tail',[(0,1.16,1.25),(0,1.35,1.15),(.02,1.48,.98),(.025,1.54,.81),(.015,1.56,.71)],
         [.09,.064,.045,.025,0],skin,col,10)
    feet=[o for o in col.all_objects if o.type=='MESH' and 'limb and broad foot' in o.name]
    contacts=[v.co.y for o in feet for v in o.data.vertices if v.co.z<=0.07]
    footprint_y=(min(contacts)+max(contacts))/2
    for obj in col.all_objects:
        if obj.type=='MESH':
            for v in obj.data.vertices: v.co.y-=footprint_y
    bpy.context.view_layer.update()
    root=bpy.data.objects[col['asset_root']]
    # Footprint centre, not the longer head silhouette, defines the floor origin.
    root['reconstruction']='A. zitteli; estimated living soft tissues, horn covering and dimensions'
    root['diagnostic']='Two huge nasal horns and two separate small supraorbital horns'
    return col


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--params',type=Path,default=HERE/'params.json');p.add_argument('--gray',action='store_true')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    params=json.loads(args.params.read_text());out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    col=build(params,args.gray);source=audit_source(col,params['budgets']['max_triangles'])
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,
        export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
        export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
        export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Exporter option unavailable')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    exported=audit_glb(out/'model.glb',params['budgets']['max_triangles'],params['budgets']['max_materials'],params['budgets']['max_primitives'])
    if exported['errors']:raise RuntimeError(exported['errors'])
    if exported['bytes']>params['budgets']['max_glb_bytes']:raise RuntimeError('File budget exceeded')
    report={'schema_version':1,'kind':'maker_build_metrics','asset_id':params['asset_id'],'revision':params['revision'],
        'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'params_sha256':hashlib.sha256(args.params.read_bytes()).hexdigest(),'export_options':opts,'source':source,'glb':exported,
        'gray':args.gray,'claim_scope':'Technical construction metrics only; independent review pending'}
    (out/'build-metrics.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__': main()
