#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original Iguanodon bernissartensis living reconstruction.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py
Optional arguments after --: --output DIR. Metres; head -Y; dorsal +Z.
The source is semantic parts. The export is a material-batched static copy.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, sys
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb


def save_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=BASE.parent);args=ap.parse_args(argv)
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);os.chdir(out)
    par=json.loads((BASE/'params.json').read_text());brief=json.loads((BASE.parent/'brief.json').read_text())
    col=setup_scene('iguanodon',seed=par['seed']);root=bpy.data.objects[col['asset_root']]
    root['taxon']='Iguanodon bernissartensis';root['reconstruction']='Complete living adult; interpretation, not fossil scan'
    mats={k:make_material('Iguanodon-'+k,v,roughness=.88) for k,v in par['palette'].items()}
    matlist=list(mats.values());mid={k:i for i,k in enumerate(mats)}
    parts=[]
    def add(name,vs,fs,indices):
        obj=mesh_object(name,vs,fs,matlist,col)
        for poly,mi in zip(obj.data.polygons,indices):poly.material_index=mi
        parts.append(obj);return obj
    def axial(name,rings,n=16,palette=True,material='skin'):
        # Explicit transverse profile rings: longitudinal Y, mid Z, halfwidth X, halfheight Z.
        vs=[(rx*math.cos(2*math.pi*j/n),y,z+rz*math.sin(2*math.pi*j/n)) for y,z,rx,rz in rings for j in range(n)]
        fs=[];ids=[]
        for i in range(len(rings)-1):
            for j in range(n):
                fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
                h=math.sin(2*math.pi*(j+.5)/n)
                ids.append(mid['dorsal' if h>.65 else 'belly' if h<-.5 else 'skin'] if palette else mid[material])
        for i in [0,len(rings)-1]:
            c=len(vs);vs.append((0,rings[i][0],rings[i][1]))
            for j in range(n):fs.append((c,i*n+j,i*n+(j+1)%n));ids.append(mid[material])
        return add(name,vs,fs,ids)
    def tube(name,path,n=10,material='skin',palette=False):
        # Points are x,y,z,transverse radius,secondary radius; closed caps preserve manifold pieces.
        vs=[]
        for i,p in enumerate(path):
            p=Vector(p[:3]);a=Vector(path[max(0,i-1)][:3]);b=Vector(path[min(len(path)-1,i+1)][:3]);t=(b-a).normalized()
            u=Vector((1,0,0));u=(u-t*u.dot(t)).normalized()
            if u.length<.1:u=Vector((0,1,0));u=(u-t*u.dot(t)).normalized()
            v=t.cross(u).normalized();ra,rb=path[i][3:]
            for j in range(n):vs.append(tuple(p+u*ra*math.cos(2*math.pi*j/n)+v*rb*math.sin(2*math.pi*j/n)))
        fs=[];ids=[]
        for i in range(len(path)-1):
            for j in range(n):
                fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j));ids.append(mid[material])
        for i in [0,len(path)-1]:
            c=len(vs);vs.append(tuple(path[i][:3]))
            for j in range(n):fs.append((c,i*n+j,i*n+(j+1)%n));ids.append(mid[material])
        return add(name,vs,fs,ids)
    def ellipsoid(name,c,r,material,n=10,lat=5):
        vs=[(c[0],c[1],c[2]+r[2])]
        for i in range(1,lat):
            a=math.pi*i/lat
            for j in range(n):
                b=2*math.pi*j/n;vs.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]+r[2]*math.cos(a)))
        vs.append((c[0],c[1],c[2]-r[2]));bot=len(vs)-1;fs=[]
        for j in range(n):fs.append((0,1+j,1+(j+1)%n))
        for i in range(lat-2):
            for j in range(n):fs.append((1+i*n+j,1+i*n+(j+1)%n,1+(i+1)*n+(j+1)%n,1+(i+1)*n+j))
        for j in range(n):fs.append((bot,1+(lat-2)*n+j,1+(lat-2)*n+(j+1)%n))
        return add(name,vs,fs,[mid[material]]*len(fs))
    # Deep trunk, strong high pelvis, gently subhorizontal back, no kangaroo tripod.
    axial('torso_deep_ribcage',[(-1.65,2.39,.23,.34),(-1.48,2.35,.48,.64),(-1.15,2.33,.73,.87),(-.65,2.30,.92,1.00),(-.05,2.30,1.00,1.05),(.55,2.35,1.00,1.03),(1.03,2.42,.89,.91),(1.42,2.50,.65,.68),(1.70,2.52,.42,.43)],20)
    axial('neck_low_stout',[(-2.63,2.88,.26,.27),(-2.4,2.83,.28,.31),(-2.15,2.75,.31,.39),(-1.90,2.62,.35,.46),(-1.60,2.50,.44,.56),(-1.30,2.47,.48,.59)],14)
    axial('head_low_elongate_beaked',[(-3.27,2.76,.15,.13),(-3.25,2.79,.22,.17),(-3.06,2.83,.25,.22),(-2.84,2.87,.30,.27),(-2.65,2.90,.34,.30),(-2.46,2.88,.32,.29),(-2.30,2.85,.22,.23)],14)
    axial('beak_cropped_keratin',[(-3.35,2.75,.155,.145),(-3.29,2.76,.21,.16),(-3.17,2.77,.22,.165)],12,False,'horn')
    axial('tail_stiff_elevated',[ (1.36,2.53,.61,.67),(1.75,2.51,.49,.57),(2.15,2.47,.40,.47),(2.65,2.39,.32,.39),(3.2,2.29,.25,.30),(3.8,2.18,.19,.23),(4.4,2.08,.14,.17),(4.95,1.99,.098,.12),(5.45,1.92,.065,.082),(5.9,1.87,.04,.055),(6.3,1.83,.023,.032),(6.65,1.80,.006,.009)],14)
    # Each limb has a broad muscle profile rather than spherical stick joints.
    for s,side in [(1,'right'),(-1,'left')]:
        tube(side+'_hind_thigh',[(s*.65,.88,2.48,.43,.56),(s*.84,.73,2.12,.48,.57),(s*.96,.38,1.65,.35,.40),(s*.98,.30,1.25,.24,.28)],12)
        tube(side+'_hind_shank',[(s*.98,.32,1.43,.255,.28),(s*1.0,.62,1.03,.20,.23),(s*.98,.91,.60,.15,.17),(s*.98,.80,.30,.15,.17)],10)
        tube(side+'_hind_metatarsus',[(s*.98,.85,.52,.16,.17),(s*.98,.64,.26,.22,.20),(s*.98,.43,.13,.29,.13)],10)
        # Three broad blunt hind toes, no five-claw mammalian foot.
        for j in [-1,0,1]:
            x=s*.98+j*.18;front=.04 if j==0 else .11
            tube(side+'_hind_toe_'+str(j+3),[(x,.50,.15,.13,.125),(x,.25,.13,.12,.12),(x,front,.115,.10,.115)],8)
            tube(side+'_hind_hoof_'+str(j+3),[(x,front+.06,.11,.102,.11),(x,front-.10,.105,.09,.105)],8,'horn')
        tube(side+'_fore_upper',[(s*.64,-1.06,2.30,.31,.38),(s*.79,-1.14,1.96,.32,.35),(s*.91,-1.08,1.49,.24,.26),(s*.94,-1.21,1.22,.20,.20)],10)
        tube(side+'_fore_radius_ulna',[(s*.94,-1.17,1.35,.20,.21),(s*.98,-1.43,.95,.16,.18),(s*1.01,-1.64,.60,.145,.16),(s*1.02,-1.71,.38,.17,.19)],10)
        # Digits II-IV compact and hoof-bearing, with a broad shared metacarpal pad.
        ellipsoid(side+'_manus_metacarpal_pad',(s*1.02,-1.71,.36),(.27,.23,.30),'skin',12,6)
        for digit,dx in [(2,-.16),(3,0),(4,.16)]:
            x=s*(1.02+dx)
            tube(side+'_hand_digit_'+str(digit),[(x,-1.73,.35,.108,.13),(x,-1.83,.19,.105,.14),(x,-1.88,.11,.10,.11)],8)
            tube(side+'_hand_hoof_'+str(digit),[(x,-1.87,.13,.104,.13),(x,-2.02,.105,.10,.105)],8,'horn')
        # Digit I is a separate stout spike pointing obliquely anteromedially.
        tube(side+'_digit_I_base',[(s*.82,-1.74,.48,.135,.14),(s*.73,-1.87,.59,.12,.13)],10)
        tube(side+'_digit_I_conical_spike',[(s*.74,-1.86,.58,.12,.13),(s*.65,-1.99,.78,.10,.105),(s*.53,-2.13,1.06,.007,.008)],10,'spike')
        # Digit V is slender, separate and flexed outward/back; not another spike.
        tube(side+'_digit_V_flexible',[(s*1.24,-1.65,.48,.083,.09),(s*1.40,-1.50,.38,.075,.08),(s*1.48,-1.48,.24,.06,.064),(s*1.43,-1.56,.20,.035,.042)],8)
        ellipsoid(side+'_eye',(s*.315,-2.61,3.025),(.047,.084,.065),'eye',10,5)
        ellipsoid(side+'_nostril',(s*.235,-3.05,2.925),(.020,.045,.026),'eye',8,4)
        tube(side+'_mouth_seam',[(s*.221,-3.25,2.70,.009,.010),(s*.263,-3.04,2.675,.009,.010),(s*.302,-2.80,2.675,.009,.010),(s*.320,-2.60,2.71,.006,.007)],6,'eye')
    # Foot-contact centroid, not full body bounding-box center, is the root origin.
    offset_y=.75
    for obj in parts:
        for v in obj.data.vertices:v.co.y+=offset_y
    source=audit_source(col,max_triangles=brief['geometry_policy']['max_triangles'])
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene['representation']='living-reconstruction'
    bpy.context.scene['scale_note']='10 m taxon estimate; not a measured R51 mount'
    bpy.context.scene['generator']='source/generate.py'
    bpy.context.preferences.filepaths.save_version=0
    # Portable scene destinations and fully overwritten inherited UI path buffers.
    bpy.context.scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'.'*1023
                    space.params.directory=b'//'
                    space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    # Batch the exact source triangles into one temporary mesh; do not save this over source.
    verts=[];faces=[];material_indices=[]
    for obj in parts:
        base=len(verts);verts.extend(tuple(v.co) for v in obj.data.vertices);obj.data.calc_loop_triangles()
        for tri in obj.data.loop_triangles:
            faces.append(tuple(base+x for x in tri.vertices));material_indices.append(obj.data.polygons[tri.polygon_index].material_index)
    packed=mesh_object('iguanodon_static_export',verts,faces,matlist,col,recalculate_normals=False)
    for p,i in zip(packed.data.polygons,material_indices):p.material_index=i
    bpy.ops.object.select_all(action='DESELECT');root.select_set(True);packed.select_set(True);bpy.context.view_layer.objects.active=root
    options=dict(filepath='model.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Missing required glTF exporter options')
    bpy.ops.export_scene.gltf(**options)
    policy=brief['geometry_policy'];glb=audit_glb(Path('model.glb'),policy['max_triangles'],policy['max_materials'],policy['max_primitives'])
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][side][i]-expected[side][i]) for side in expected for i in range(3))
    assert not glb['errors'] and delta<1e-4 and glb['scene_triangles']==source['triangles'] and glb['bytes']<=policy['max_glb_bytes']
    assert abs(b['size'][1]-10)<1e-5
    report={'status':'PASS','scope':'Source meshes, static GLB baseline and axis-aware correspondence only','blender_version':bpy.app.version_string,'seed':par['seed'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((BASE/'params.json').read_bytes()).hexdigest(),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'source_part_count':len(parts),'primitive_batching':'Semantic source parts retained in blend; exported source triangles batched by material','palette_srgb':par['palette'],'scale_note':'10 m taxon estimate, not R51 measurement','gpu':'UNKNOWN','scene':'UNKNOWN'}
    save_json(out/'qa/evidence/build.json',report)
    print('BUILD_PASS',json.dumps({'triangles':glb['scene_triangles'],'glb_sha256':glb['sha256'],'semantic_sha256':glb['semantic_sha256'],'bounds':glb['bounds_m']}))
if __name__=='__main__':main()
