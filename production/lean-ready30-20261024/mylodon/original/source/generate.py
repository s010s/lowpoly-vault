# SPDX-License-Identifier: MIT
"""Deterministic, original Mylodon darwinii life reconstruction.
Run inside Blender: --python source/generate.py -- --output-dir build
Only sibling params.json and deps are generation dependencies. Artistic soft
anatomy is an estimate; no complete articulated specimen was available.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def write(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def loft_y(name, sections, sides, mats, collection, shade=False):
    # Sections: y, z center, horizontal radius, vertical radius. Closed cap fans.
    vertices=[]
    for j,(y,z,rx,rz) in enumerate(sections):
        for k in range(sides):
            a=2*math.pi*k/sides
            vertices.append((rx*math.cos(a),y,z+rz*math.sin(a)))
    vertices += [(0,sections[0][0],sections[0][1]),(0,sections[-1][0],sections[-1][1])]
    faces=[]
    for j in range(len(sections)-1):
        for k in range(sides):
            a=j*sides+k;b=j*sides+(k+1)%sides;c=b+sides;d=a+sides
            # Deliberate diagonals keep broad anatomical facets readable.
            if (j+k)%2: faces += [(a,b,d),(b,c,d)]
            else: faces += [(a,b,c),(a,c,d)]
    for k in range(sides):
        faces.append((len(vertices)-2,(k+1)%sides,k))
        faces.append((len(vertices)-1,(len(sections)-1)*sides+k,(len(sections)-1)*sides+(k+1)%sides))
    obj=mesh_object(name,vertices,faces,mats,collection)
    if shade:
        for face in obj.data.polygons:
            # Restrained light on dorsal coat; no random colored confetti.
            z=sum(obj.data.vertices[v].co.z for v in face.vertices)/len(face.vertices)
            face.material_index=1 if z>1.12 else 2 if z<0.57 else 0
    return obj

def tube_geometry(points,radii,sides=10,aspect=1.,axis_hint=None):
    points=[Vector(p) for p in points];verts=[];faces=[]
    for i,p in enumerate(points):
        tangent=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
        axis=Vector(axis_hint or (1,0,0))
        if abs(tangent.dot(axis))>.9: axis=Vector((0,1,0))
        u=(axis-tangent*tangent.dot(axis)).normalized();v=tangent.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides
            verts.append(tuple(p+u*(math.cos(a)*radii[i])+v*(math.sin(a)*radii[i]*aspect)))
    verts += [tuple(points[0]),tuple(points[-1])]
    for i in range(len(points)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    for j in range(sides):
        faces.append((len(verts)-2,(j+1)%sides,j))
        faces.append((len(verts)-1,(len(points)-1)*sides+j,(len(points)-1)*sides+(j+1)%sides))
    return verts,faces

def tube(name,points,radii,mats,collection,sides=10,aspect=1.):
    v,f=tube_geometry(points,radii,sides,aspect)
    return mesh_object(name,v,f,mats,collection)

def merge_chunks(name,chunks,mats,collection):
    v=[];f=[];indices=[]
    for vv,ff,mi in chunks:
        n=len(v);v.extend(vv);f.extend(tuple(n+x for x in face) for face in ff);indices.extend([mi]*len(ff))
    obj=mesh_object(name,v,f,mats,collection)
    for p,mi in zip(obj.data.polygons,indices): p.material_index=mi
    return obj

def ellipsoid(name,center,radii,mat,collection,sides=12,rings=6):
    cx,cy,cz=center;rx,ry,rz=radii
    sections=[]
    for i in range(rings+1):
        a=-math.pi/2+(i+.1)/(rings+.2)*math.pi
        sections.append((cy+ry*math.sin(a),cz,rx*math.cos(a),rz*math.cos(a)))
    ob=loft_y(name,sections,sides,mat,collection)
    for v in ob.data.vertices:v.co.x+=cx
    return ob

def build(params,gray=False):
    random.seed(params['seed'])
    col=setup_scene('mylodon',params['seed'])
    palette=params['palette']
    mats={k:make_material(k,v,roughness=.91 if k!='eye' else .38) for k,v in palette.items()}
    fur=[mats['coat'],mats['coat-light'],mats['coat-dark']]
    torso=loft_y('deep_low_trunk',[
        (-.81,.94,.12,.17),(-.69,.91,.30,.30),(-.48,.87,.40,.37),
        (-.17,.83,.46,.40),(.16,.84,.47,.43),(.47,.88,.45,.43),
        (.73,.85,.36,.37),(.91,.78,.22,.27),(.99,.73,.07,.11)],16,fur,col,True)
    torso['anatomical_role']='deep low shaggy trunk, not a fossil articulation'
    loft_y('low_neck_and_long_narrow_head',[
        (-1.60,.93,.080,.085),(-1.53,.95,.110,.115),(-1.35,.99,.130,.14),
        (-1.17,1.035,.15,.16),(-1.02,1.055,.185,.20),(-.86,1.04,.19,.215),
        (-.72,1.00,.20,.22),(-.62,.96,.22,.24)],12,fur,col)
    # Long slender muzzle is covered by soft tissue. No speculative nasal horn.
    nose=loft_y('soft_nasal_pad',[
        (-1.634,.943,.055,.060),(-1.610,.949,.083,.075),(-1.577,.950,.087,.077),(-1.551,.947,.077,.062)],10,mats['nose'],col)
    loft_y('lower_jaw_soft_profile',[
        (-1.58,.861,.043,.026),(-1.44,.863,.083,.041),(-1.24,.873,.105,.060),
        (-1.06,.912,.130,.070),(-.96,.94,.11,.08)],10,mats['coat-dark'],col)
    for side,label in [(-1,'left'),(1,'right')]:
        # Small ears and lateral eyes, well behind the narrow muzzle.
        ear=ellipsoid('ear_'+label,(side*.177,-.907,1.182),(.047,.069,.081),mats['coat-dark'],col,10,4)
        ellipsoid('eye_'+label,(side*.143,-1.164,1.113),(.019,.027,.022),mats['eye'],col,10,4)
        # Plantigrade-looking lateral support surfaces; anatomical weight-bearing
        # arrangement and joint posture remain estimates, not fossil facts.
        tube('forelimb_'+label,[(side*.285,-.57,.96),(side*.355,-.61,.75),(side*.39,-.55,.48),(side*.405,-.66,.24),(side*.419,-.71,.14)],
             [.19,.165,.134,.112,.105],fur[0],col,12)
        ellipsoid('forepaw_support_'+label,(side*.425,-.738,.107),(.137,.198,.107),mats['coat-dark'],col,12,6)
        tube('hindlimb_'+label,[(side*.29,.62,.93),(side*.365,.64,.71),(side*.405,.78,.43),(side*.431,.65,.20),(side*.443,.57,.13)],
             [.24,.217,.15,.12,.109],fur[0],col,12)
        ellipsoid('hindfoot_support_'+label,(side*.44,.519,.105),(.15,.23,.105),mats['coat-dark'],col,12,6)
    # Robust curved foreclaws remain distinct from fur and supporting paw pads.
    claws=[]
    for s in [-1,1]:
        for i in range(3):
            x=s*(.335+i*.088); length=[.21,.265,.225][i]
            y=-.85+[.015,-.005,.025][i]
            pts=[(x,y,.148),(x+s*.004,y-length*.34,.159),(x+s*.008,y-length*.71,.116),(x+s*.006,y-length,.050)]
            vv,ff=tube_geometry(pts,[.046,.042,.028,.0045],8,1.05);claws.append((vv,ff,0))
        for i in range(3):
            x=s*(.345+i*.088);y=.35+[.02,0,.025][i]
            pts=[(x,y,.11),(x,y-.075,.105),(x,y-.13,.059),(x,y-.145,.037)]
            vv,ff=tube_geometry(pts,[.034,.03,.018,.0035],8,.9);claws.append((vv,ff,0))
    merge_chunks('stout_curved_claws',claws,mats['claw'],col)
    tube('tapering_subordinate_tail',[(0,.80,.68),(0,1.00,.51),(0,1.18,.30),(0,1.35,.19),(0,1.49,.175),(0,1.61,.205)],
         [.205,.163,.115,.078,.043,.008],fur[0],col,12,.84)
    if not gray:
        # Closed, slender coat locks overlap the underlying skin surface.
        # Fur is a restrained external silhouette, not exposed dermal armor.
        locks=[]
        # Irregular, fine flattened locks: deliberately no repeated scale rows.
        sections=[(-.69,.91,.30,.30),(-.48,.87,.40,.37),(-.17,.83,.46,.40),(.16,.84,.47,.43),(.47,.88,.45,.43),(.73,.85,.36,.37)]
        for side in [-1,1]:
            for i in range(65):
                y=random.uniform(-.62,.69)
                for j in range(len(sections)-1):
                    if sections[j][0]<=y<=sections[j+1][0]:
                        t=(y-sections[j][0])/(sections[j+1][0]-sections[j][0])
                        zc,rx,rz=[sections[j][k]*(1-t)+sections[j+1][k]*t for k in [1,2,3]]
                        break
                a=random.uniform(-1.03,.66)
                x=side*rx*math.cos(a);z=zc+rz*math.sin(a)
                length=random.uniform(.075,.14);width=random.uniform(.018,.032)
                pts=[(x-side*.020,y,z+.025),(x+side*.006,y+.020,z-.012),(x+side*.004,y+.055,z-length)]
                vv,ff=tube_geometry(pts,[width,width*.8,.002],5,.35,(0,1,0))
                mi=2 if a<-.64 else 0
                locks.append((vv,ff,mi))
            for i in range(13):
                y=-.43+i*.083+random.uniform(-.022,.022);x=side*random.uniform(.21,.29)
                length=random.uniform(.065,.115)
                pts=[(x,y,.51),(x+side*.015,y+.025,.465),(x+side*.008,y+.055,.465-length)]
                vv,ff=tube_geometry(pts,[.026,.021,.002],5,.4,(0,1,0));locks.append((vv,ff,2))
            for j in range(9):
                y=-.77+random.uniform(0,.22);z=random.uniform(.90,1.13)
                pts=[(side*.205,y,z),(side*.225,y+.024,z-.03),(side*.227,y+.056,z-.105)]
                vv,ff=tube_geometry(pts,[.022,.018,.002],5,.4,(0,1,0));locks.append((vv,ff,0))
        merge_chunks('coarse_coat_locks',locks,fur,col)
    for o in col.all_objects:
        if o.type=='MESH':o['surface_style']='intentional flat faceted closed semantic part'
    # Center of the four support-paw contacts, not the full tail/head bounding box.
    minimum=min(v.co.z for ob in col.all_objects if ob.type=='MESH' for v in ob.data.vertices)
    for ob in col.all_objects:
        if ob.type=='MESH':
            for v in ob.data.vertices:
                v.co.y += .1095
                v.co.z -= minimum
    return col

def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--params',type=Path,default=HERE/'params.json');ap.add_argument('--gray',action='store_true')
    a=ap.parse_args(args);p=json.loads(a.params.read_text());out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    col=build(p,a.gray)
    if a.gray:
        gray=make_material('gray-study','#8E8A83')
        for ob in col.all_objects:
            if ob.type=='MESH':ob.data.materials.clear();ob.data.materials.append(gray)
    audit=audit_source(col,p['budgets']['max_triangles'])
    if audit['errors']:raise RuntimeError(audit['errors'])
    bpy.context.scene['scientific_limits']='Living reconstruction. Body proportions, stance, color, fur distribution, claw curvature and muzzle are estimates. Jaw/skin observations do not prove a complete articulated skeleton.'
    bpy.context.scene['generator']='source/generate.py'
    bpy.context.preferences.filepaths.save_version=0
    # Avoid saving default host render/file-browser locations in the editable file.
    bpy.context.scene.render.filepath='//render'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:
                    space.params.directory=b'//'
                    space.params.filename='model.blend'
    # The native source contains no camera, lights, stage, scripts or source paths.
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,
        export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
        export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
        export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Missing explicit exporter options: '+str(set(opts)-available))
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    glb=audit_glb(out/'model.glb',p['budgets']['max_triangles'],p['budgets']['max_materials'],p['budgets']['max_primitives'])
    if glb['errors']:raise RuntimeError(glb['errors'])
    if glb['bytes']>p['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    b=audit['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][side][i]-expected[side][i]) for side in ['min','max'] for i in range(3))
    if delta>1e-4 or glb['scene_triangles']!=audit['triangles']:raise RuntimeError('Source/export mismatch')
    # Canonical audit may report input paths; public evidence uses only artifact names.
    glb['file']='model.glb'
    report={'status':'PASS','scope':'SOURCE_STATIC_GLB_METRICS_AND_AXIS_BOUNDS_ONLY','gray_study':a.gray,
        'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],
        'generator_sha256':sha(__file__),'params_sha256':sha(a.params),'glb_sha256':sha(out/'model.glb'),
        'blend_sha256':sha(out/'model.blend'),'source':audit,'glb':glb,'bounds_max_error_m':delta,'export_options':opts}
    write(out/'build-report.json',report)
    print(json.dumps({'status':'built','triangles':audit['triangles'],'glb_sha256':report['glb_sha256']}))
if __name__=='__main__':main()
