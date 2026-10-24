#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original reference-led Megacerops reconstruction, meters, -Y forward.
Run in Blender: --background --factory-startup --threads 2 --python source/generate.py -- --output candidate
Only package-relative helpers are imported. Reference photographs are not textures.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d): Path(p).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args(argv); out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text()); C=setup_scene(p['asset_id'],p['seed'])
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    mats={k:make_material(k,v,roughness=.86 if k!='recess' else .8) for k,v in p['palette_srgb_hex'].items()}
    construction=[]
    def mesh(name,verts,faces,mat='hide',skin=False):
        o=mesh_object(name,verts,faces,mats[mat],C)
        if skin: construction.append(o)
        return o
    def loft_y(name,sections,n=32,mat='hide',skin=False):
        # y, half-width, dorsal Z, ventral Z; the longitudinal silhouette is explicit.
        v=[]; f=[]
        for y,w,top,bot in sections:
            for j in range(n):
                t=2*math.pi*j/n
                v.append((w*math.sin(t),y,(top+bot)/2+(top-bot)/2*math.cos(t)))
        for i in range(len(sections)-1):
            for j in range(n):
                f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        f.append(tuple(reversed(range(n)))); f.append(tuple((len(sections)-1)*n+j for j in range(n)))
        return mesh(name,v,f,mat,skin)
    def tube(name,centers,radii,n=16,mat='hide',skin=False):
        v=[]; f=[]
        for i,c in enumerate(centers):
            tangent=Vector(centers[min(i+1,len(centers)-1)])-Vector(centers[max(i-1,0)])
            tangent.normalize(); ref=Vector((0,1,0)) if abs(tangent.y)<.9 else Vector((1,0,0))
            u=tangent.cross(ref).normalized(); vv=tangent.cross(u).normalized()
            rx,ry=radii[i] if isinstance(radii[i],tuple) else (radii[i],radii[i])
            for j in range(n):
                th=2*math.pi*j/n; v.append(tuple(Vector(c)+u*rx*math.cos(th)+vv*ry*math.sin(th)))
        for i in range(len(centers)-1):
            for j in range(n): f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        f.extend([tuple(reversed(range(n))),tuple((len(centers)-1)*n+j for j in range(n))])
        return mesh(name,v,f,mat,skin)
    # A nonuniform axial loft defines neck, withers, deep thorax, lumbar slope and rump.
    loft_y('axial-hide',[(-1.62,.18,1.98,1.18),(-1.5,.27,2.02,1.05),(-1.32,.34,2.09,.96),(-1.10,.42,2.18,.88),(-.86,.50,2.28,.82),(-.62,.56,2.30,.78),(-.35,.58,2.28,.76),(0,.58,2.22,.76),(.35,.57,2.16,.79),(.65,.54,2.09,.84),(.95,.51,2.04,.92),(1.2,.46,2.04,1.02),(1.42,.39,2.00,1.13),(1.6,.26,1.9,1.26),(1.73,.10,1.73,1.42),(1.76,.035,1.62,1.52)],skin=True)
    # High occiput, central concavity, raised nasal base, blunt lowered muzzle.
    loft_y('saddle-head',[(-2.65,.10,1.39,1.13),(-2.60,.20,1.44,1.07),(-2.51,.235,1.49,1.04),(-2.40,.255,1.67,1.035),(-2.29,.25,1.72,1.045),(-2.17,.25,1.62,1.025),(-2.03,.265,1.55,.99),(-1.89,.30,1.66,.99),(-1.76,.325,1.81,1.01),(-1.65,.32,1.94,1.12),(-1.54,.27,2.02,1.18),(-1.42,.20,1.99,1.27)],skin=True)
    feet=[]
    for s in (-1,1):
        front_y=-.82+(.055 if s<0 else -.055)
        fore=[(s*.14,-.76,2.10),(s*.29,-.77,1.98),(s*.40,-.79,1.81),(s*.49,-.75,1.62),(s*.53,-.62,1.39),(s*.54,-.58,1.18),(s*.54,-.65,.96),(s*.54,-.76,.72),(s*.54,front_y,.48),(s*.54,front_y,.23),(s*.54,front_y-.035,.12)]
        fore_r=[(.18,.23),(.24,.28),(.28,.31),(.27,.285),(.23,.235),(.185,.19),(.148,.16),(.12,.145),(.125,.145),(.145,.17),(.165,.18)]
        tube(('left' if s<0 else 'right')+'-forelimb',fore,fore_r,20,skin=True)
        hind_y=1.20+(-.055 if s<0 else .055)
        hind=[(s*.10,1.10,1.90),(s*.24,1.14,1.80),(s*.34,1.16,1.73),(s*.43,1.17,1.51),(s*.47,1.00,1.27),(s*.48,.94,1.08),(s*.48,1.1,.86),(s*.49,1.30,.64),(s*.49,1.31,.48),(s*.49,hind_y,.24),(s*.49,hind_y-.025,.12)]
        hind_r=[(.12,.18),(.23,.25),(.28,.30),(.265,.27),(.23,.24),(.195,.20),(.15,.18),(.115,.135),(.105,.12),(.135,.15),(.15,.17)]
        tube(('left' if s<0 else 'right')+'-hindlimb',hind,hind_r,20,skin=True)
        feet.extend([(s*.54,front_y-.06,4,'front'),(s*.49,hind_y-.055,3,'hind')])
    # Preserve the original profile parts as editable source controls outside EXPORT.
    archive=bpy.data.collections.new('CONSTRUCTION_PROFILES'); bpy.context.scene.collection.children.link(archive)
    archive.hide_render=True; archive.hide_viewport=True
    for o in construction:
        cp=o.copy(); cp.data=o.data.copy(); cp.name='profile-'+o.name; cp.parent=None; archive.objects.link(cp)
        cp.hide_render=True; cp.hide_viewport=True
    bpy.ops.object.select_all(action='DESELECT')
    for o in construction:o.select_set(True)
    bpy.context.view_layer.objects.active=construction[0]; bpy.ops.object.join()
    skin=construction[0]; skin.name='continuous-hide'
    # Deterministic voxel union resolves the body/neck/limb junctions, then a restrained
    # surface relaxation and decimation preserve the authored silhouettes as broad planes.
    mod=skin.modifiers.new('anatomical-union','REMESH'); mod.mode='VOXEL'; mod.voxel_size=.035; mod.use_smooth_shade=False
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=skin.modifiers.new('relax-transitions','SMOOTH'); mod.factor=.45; mod.iterations=3
    bpy.ops.object.modifier_apply(modifier=mod.name)
    # Local geometric relaxation across embedded upper-limb roots. The weights
    # feather into the shoulder and haunch, leaving head, feet and lower joints alone.
    group=skin.vertex_groups.new(name='upper-limb-transition')
    for v in skin.data.vertices:
        x,y,z=v.co
        lateral=max(0,min(1,(abs(x)-.23)/.22))
        height=max(0,min(1,(z-1.16)/.24))*max(0,min(1,(2.24-z)/.20))
        along=max(max(0,1-abs(y+.74)/.58),max(0,1-abs(y-1.10)/.53))
        weight=lateral*height*along
        if weight>0:group.add([v.index],weight,'REPLACE')
    mod=skin.modifiers.new('resolve-upper-limb-skin','SMOOTH');mod.factor=.7;mod.iterations=10;mod.vertex_group=group.name
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=skin.modifiers.new('deliberate-faceting','DECIMATE'); mod.ratio=.22; mod.use_collapse_triangulate=True
    bpy.ops.object.modifier_apply(modifier=mod.name)
    skin.data.materials.clear()
    for k in ('hide','flank','muzzle'):skin.data.materials.append(mats[k])
    for f in skin.data.polygons:
        co=f.center
        f.material_index=2 if co.y<-2.40 and co.z<1.49 else 1 if -.45<co.y<.85 and co.z<1.16 and abs(co.x)<.48 else 0
        f.use_smooth=False
    # Original short, thick, individually unbranched frontonasal processes.
    for s in (-1,1):
        tube(('left' if s<0 else 'right')+'-nasal-process',[(s*.155,-2.29,1.64),(s*.20,-2.31,1.73),(s*.275,-2.35,1.82),(s*.33,-2.38,1.86),(s*.35,-2.39,1.87)],[(.145,.12),(.13,.115),(.105,.10),(.08,.085),(.052,.06)],16,'process_cover')
        # Small laterally opened leaf-like ears, closed polyhedra rather than flat sheets.
        vv=[(s*.23,-1.47,1.87),(s*.29,-1.46,1.95),(s*.47,-1.43,2.06),(s*.49,-1.38,1.99),(s*.41,-1.35,1.86),(s*.29,-1.39,1.83),(s*.36,-1.45,1.93),(s*.36,-1.37,1.94)]
        ff=[(6,j,(j+1)%6) for j in range(6)]+[(7,(j+1)%6,j) for j in range(6)]
        mesh(('left' if s<0 else 'right')+'-ear',vv,ff)
        # A deliberately modest inset eye and a shallow nostril; geometry is closed.
        def ellipsoid(name,c,r,mat,n=12,k=6):
            verts=[(c[0],c[1],c[2]+r[2])]
            for q in range(1,k):
                t=math.pi*q/k
                for j in range(n):
                    ph=2*math.pi*j/n; verts.append((c[0]+r[0]*math.sin(t)*math.cos(ph),c[1]+r[1]*math.sin(t)*math.sin(ph),c[2]+r[2]*math.cos(t)))
            verts.append((c[0],c[1],c[2]-r[2])); faces=[]
            for j in range(n):faces.append((0,1+j,1+(j+1)%n))
            for q in range(k-2):
                for j in range(n):faces.append((1+q*n+j,1+(q+1)*n+j,1+(q+1)*n+(j+1)%n,1+q*n+(j+1)%n))
            for j in range(n):faces.append((len(verts)-1,1+(k-2)*n+(j+1)%n,1+(k-2)*n+j))
            return mesh(name,verts,faces,mat)
        ellipsoid(('left' if s<0 else 'right')+'-eye',(s*.293,-1.82,1.62),(.027,.049,.033),'recess')
        ellipsoid(('left' if s<0 else 'right')+'-nostril',(s*.204,-2.555,1.345),(.019,.047,.027),'recess')
        # Thin curved closed lip relief follows the muzzle and never leaves a jaw gape.
        tube(('left' if s<0 else 'right')+'-lip',[(s*.11,-2.643,1.176),(s*.176,-2.602,1.17),(s*.205,-2.54,1.16),(s*.225,-2.46,1.155),(s*.232,-2.38,1.155)],[.004,.009,.009,.008,.003],8,'recess')
    # Four forefoot / three hindfoot compact hoof endings in single semantic foot meshes.
    for index,(x,y,count,kind) in enumerate(feet):
        parts=[]
        spacing=.078 if count==4 else .095
        for j in range(count):
            dx=(j-(count-1)/2)*spacing; outer=abs(j-(count-1)/2)
            yy=y-.045+outer*.022
            o=loft_y('toe-part',[(yy-.17,.018,.08,.012),(yy-.15,.033,.115,.002),(yy-.08,.039,.155,.0),(yy+.025,.041,.17,.0),(yy+.10,.03,.16,.025)],n=12,mat='feet')
            for v in o.data.vertices:v.co.x+=x+dx
            parts.append(o)
        bpy.ops.object.select_all(action='DESELECT')
        for o in parts:o.select_set(True)
        bpy.context.view_layer.objects.active=parts[0]; bpy.ops.object.join(); parts[0].name=f'{kind}-foot-{index+1}-{count}-toes'
    tube('drooping-tail',[(0,1.62,1.72),(.025,1.81,1.62),(.04,1.96,1.46),(.05,2.03,1.29),(.055,2.05,1.18)],[.075,.06,.043,.032,.018],12)
    # Export only the semantic production surface, never source controls or the studio.
    contacts=[v.co for o in C.all_objects if o.type=='MESH' for v in o.data.vertices if abs(v.co.z)<1e-6]
    pivot=Vector(((min(v.x for v in contacts)+max(v.x for v in contacts))/2,(min(v.y for v in contacts)+max(v.y for v in contacts))/2,0))
    for o in list(C.all_objects)+list(archive.objects):
        if o.type=='MESH':
            for v in o.data.vertices:v.co-=pivot
    source=audit_source(C,p['budget']['max_triangles'])
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene.render.filepath='//preview'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in C.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=False,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={q.identifier for q in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Missing exporter flags')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    budget=p['budget']; glb=audit_glb(out/'model.glb',budget['max_triangles'],budget['max_materials'],budget['max_primitives'])
    b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ('min','max') for i in range(3))
    if source['triangles']!=glb['scene_triangles'] or delta>1e-4 or glb['errors'] or glb['bytes']>budget['max_glb_bytes']:raise RuntimeError('Export audit failed')
    glb['file']='model.glb'
    report={'asset_id':p['asset_id'],'revision':p['revision'],'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'glb_sha256':sha(out/'model.glb'),'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'blender_version':bpy.app.version_string,'exporter_version':list(__import__('io_scene_gltf2').bl_info['version']),'seed':p['seed'],'export_options':opts,'geometry_policy':budget,'source_contains_studio':False,'editable_construction_profiles_retained':True,'limits':'Technical maker checks only; no independent visual, GPU, scene, user or publication acceptance.'}
    write(out/'technical.json',report)
    print(json.dumps({'complete':True,'triangles':glb['scene_triangles'],'bytes':glb['bytes'],'sha256':glb['sha256']}))
if __name__=='__main__':main()
