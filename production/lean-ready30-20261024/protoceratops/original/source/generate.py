#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original deterministic Protoceratops reconstruction, authored in meters.
Run with Blender background mode and pass --output-dir DIR after --.
Only package-relative dependencies and params are used. Stage gray is a
low-cost silhouette diagnostic, not the finished asset or factual approval.
"""
import argparse, hashlib, json, math, os, sys
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v): Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

def loft_y(name, sections, materials, collection, n=12, belly=False):
    verts=[]
    for y,x,z,rx,rz in sections:
        verts.extend((x+rx*math.cos(2*math.pi*k/n),y,z+rz*math.sin(2*math.pi*k/n)) for k in range(n))
    faces=[tuple(range(n-1,-1,-1))]
    for i in range(len(sections)-1):
        for k in range(n): faces.append((i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k))
    faces.append(tuple((len(sections)-1)*n+k for k in range(n)))
    obj=mesh_object(name,verts,faces,materials,collection)
    if belly:
        for face in obj.data.polygons:
            mid=sum(obj.data.vertices[i].co.z for i in face.vertices)/len(face.vertices)
            if mid<.29: face.material_index=1
    return obj

def tube_z(name,sections,mat,col,n=10):
    # Each ring is a horizontal anatomical cross section. Bent joints are
    # connected, not a necklace of spheres or scaled primitives.
    verts=[]
    for x,y,z,rx,ry in sections:
        verts.extend((x+rx*math.cos(2*math.pi*k/n),y+ry*math.sin(2*math.pi*k/n),z) for k in range(n))
    faces=[tuple(range(n-1,-1,-1))]
    for i in range(len(sections)-1):
        for k in range(n): faces.append((i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k))
    faces.append(tuple((len(sections)-1)*n+k for k in range(n)))
    return mesh_object(name,verts,faces,mat,col)

def ellipsoid(name,c,r,mat,col,n=12,lat=6):
    verts=[(c[0],c[1],c[2]+r[2])]
    for j in range(1,lat):
        a=math.pi*j/lat
        for k in range(n):
            b=2*math.pi*k/n
            verts.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]+r[2]*math.cos(a)))
    bottom=len(verts);verts.append((c[0],c[1],c[2]-r[2]));faces=[]
    for k in range(n):faces.append((0,1+k,1+(k+1)%n))
    for j in range(lat-2):
        for k in range(n):
            a=1+j*n+k;b=1+j*n+(k+1)%n;faces.append((a,a+n,b+n,b))
    for k in range(n): faces.append((bottom,1+(lat-2)*n+(k+1)%n,1+(lat-2)*n+k))
    return mesh_object(name,verts,faces,mat,col)

def build(p,gray):
    col=setup_scene(p['asset_id'],p['seed'])
    mats={k:make_material(k,'#97938B' if gray else v,.88 if k!='eye' else .53) for k,v in p['palette'].items()}
    loft_y('barrel-torso-and-neck',p['body_sections'],[mats['skin'],mats['underside']],col,16,True)
    loft_y('long-tapering-tail',p['tail_sections'],[mats['skin'],mats['underside']],col,12,True)
    loft_y('deep-hornless-skull',p['head_sections'],[mats['skin'],mats['underside']],col,14,True)
    # Skin-covered cranial frill: bowed closed plate, no literal fenestra holes.
    contour=p['frill_contour']; center=(0,.473);n=len(contour);verts=[]
    for back in (False,True):
        for scale in (.15,.52,.84,1):
            for x,z in contour:
                xx=x*scale;zz=center[1]+(z-center[1])*scale
                yy=-.393+.48*(zz-.43)+(.023 if back else 0)-.028*(1-scale*scale)
                verts.append((xx,yy,zz))
    faces=[];mi=[]
    for layer in range(2):
        o=layer*4*n;faces.append(tuple(o+k for k in range(n)));mi.append(0)
        for j in range(3):
            for k in range(n): faces.append((o+j*n+k,o+j*n+(k+1)%n,o+(j+1)*n+(k+1)%n,o+(j+1)*n+k));mi.append(1 if j==2 else 0)
    for k in range(n): faces.append((3*n+k,3*n+(k+1)%n,7*n+(k+1)%n,7*n+k));mi.append(1)
    frill=mesh_object('broad-solid-cranial-frill',verts,faces,[mats['skin'],mats['frill_edge']],col)
    for face,idx in zip(frill.data.polygons,mi):face.material_index=idx
    loft_y('hooked-upper-keratin-beak',p['beak_upper'],mats['beak'],col,12)
    loft_y('lower-beak-and-jaw',p['beak_lower'],mats['beak'],col,10)
    # Four independent continuous limb chains. Sole rings are at floor Z=0.
    feet=[]
    for s,side in [(1,'right'),(-1,'left')]:
        fore=[[s*.100,-.235,.362,.062,.074],[s*.137,-.210,.285,.057,.060],[s*.160,-.183,.192,.043,.044],[s*.166,-.241,.092,.029,.034],[s*.169,-.268,.040,.044,.065],[s*.169,-.284,.0,.048,.070]]
        hind=[[s*.107,.19,.396,.086,.104],[s*.154,.208,.305,.076,.082],[s*.173,.162,.205,.052,.060],[s*.173,.225,.080,.031,.035],[s*.177,.208,.035,.049,.074],[s*.177,.190,.0,.054,.078]]
        tube_z(side+'-forelimb-with-foot',fore,mats['skin'],col)
        tube_z(side+'-hindlimb-with-foot',hind,mats['skin'],col)
        feet.extend([(s*.169,-.284,.048,.070),(s*.177,.190,.054,.078)])
    if not gray:
        for s,side in [(1,'right'),(-1,'left')]:
            # Laterally directed eyes, small and inset in the cheek profile.
            ellipsoid(side+'-eyelid',(s*.108,-.474,.427),(.023,.029,.024),mats['frill_edge'],col)
            ellipsoid(side+'-eye',(s*.124,-.478,.429),(.009,.017,.016),mats['eye'],col)
            ellipsoid(side+'-pupil',(s*.131,-.481,.429),(.0045,.008,.010),mats['dark'],col,10,5)
            ellipsoid(side+'-nostril',(s*.066,-.581,.373),(.004,.009,.005),mats['dark'],col,10,4)
        # Discreet hooflike nail tips only on the three central toes; the soft
        # foot outline is stylized, not a claim that all digits are preserved.
        v=[];f=[]
        for x,y,rx,ry in feet:
            for toe in (-1,0,1):
                cx=x+toe*.025;cy=y-ry*.72+(abs(toe)*.007);z=.018;w=.010;d=.021;h=.014
                o=len(v);v.extend([(cx-w,cy+d,z-h),(cx+w,cy+d,z-h),(cx+w*.8,cy-d,z-h),(cx-w*.8,cy-d,z-h),(cx-w*.7,cy+d,z+h),(cx+w*.7,cy+d,z+h),(cx+w*.6,cy-d,z),(cx-w*.6,cy-d,z)])
                f.extend(tuple(o+i for i in q) for q in [(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)])
        mesh_object('twelve-small-keratin-nail-tips',v,f,mats['beak'],col)
    for obj in col.all_objects:
        if obj.type=='MESH':
            for vert in obj.data.vertices:vert.co*=p.get('scale',1)
    return col

def main():
    a=argparse.ArgumentParser();a.add_argument('--output-dir',type=Path,required=True);a.add_argument('--params',type=Path,default=BASE/'params.json');a.add_argument('--stage',choices=['gray','final'],default='final')
    args=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    p=json.loads(args.params.read_text());out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    col=build(p,args.stage=='gray');source=audit_source(col,max_triangles=18000)
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene['scientific_scope']='Original estimated Protoceratops andrewsi living reconstruction, guided by CM9185, not a scan.'
    bpy.context.scene['source_generator']='source/generate.py';bpy.context.scene['source_params_sha256']=digest(args.params)
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//renders/'
    # Keep unused startup editor directories portable in the editable file.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None and hasattr(space.params,'directory'):
                    space.params.directory=b'//'
                    if hasattr(space.params,'filename'):space.params.filename='' 
    os.chdir(out)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),relative_remap=False)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    options=dict(filepath='model.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    assert not set(options)-available,'Required exporter flags unavailable'
    bpy.ops.export_scene.gltf(**options)
    glb=audit_glb('model.glb',18000,8,36)
    assert not glb['errors'],glb['errors']
    sb=source['bounds_blender_m'];expected={'min':[sb['min'][0],sb['min'][2],-sb['max'][1]],'max':[sb['max'][0],sb['max'][2],-sb['min'][1]]}
    delta=max(abs(glb['bounds_m'][kind][i]-expected[kind][i]) for kind in ['min','max'] for i in range(3))
    assert delta<.0001 and source['triangles']==glb['scene_triangles']
    evidence=out/'qa/evidence';evidence.mkdir(parents=True,exist_ok=True)
    save(evidence/'source.json',{'status':'PASS','stage':args.stage,'generator_sha256':digest(__file__),'params_sha256':digest(args.params),'blend_sha256':digest('model.blend'),'glb_sha256':digest('model.glb'),'source':source,'source_export_bounds_max_delta_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'scope':'Source evaluated geometry and exact export comparison only; not independent visual or scientific acceptance.'})
    save(evidence/'glb-audit.json',glb)
    print(json.dumps({'status':'GENERATED','stage':args.stage,'glb_sha256':glb['sha256'],'triangles':glb['scene_triangles'],'primitives':glb['scene_primitives_estimated_base_draw_calls'],'bytes':glb['bytes'],'bounds_m':glb['bounds_m']}))
if __name__=='__main__':main()
