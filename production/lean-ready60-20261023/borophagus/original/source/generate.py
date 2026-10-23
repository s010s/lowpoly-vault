#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original genus-level living Borophagus reconstruction. Dimensions are estimates.
Usage: blender -b -t 2 --python source/generate.py -- --output OUTPUT_DIRECTORY
Only params.json, bundled Blender modules and declared relative dependencies are needed.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((SOURCE/'params.json').read_text());col=setup_scene(cfg['asset_id'],cfg['seed']);root=bpy.data.objects[col['asset_root']]
    mats={k:make_material(k,v,roughness=.88 if k!='eye' else .62) for k,v in cfg['palette_srgb'].items()}
    def mesh(name,vs,fs,materials):
        ob=mesh_object(name,vs,fs,[mats[k] for k in materials],col);ob['anatomical_part']=name;return ob
    def join_data(arrays):
        vs=[];fs=[]
        for a,b in arrays:
            off=len(vs);vs.extend(a);fs.extend([tuple(i+off for i in f) for f in b])
        return vs,fs
    def rings_mesh(rings,n=12):
        # Horizontal transverse profiles. Each ring has y, center-z, half-width,
        # upper and lower depth; independent depths shape vault, throat and belly.
        vs=[]
        for y,z,rx,up,down in rings:
            for j in range(n):
                t=math.tau*j/n;ss=math.sin(t)
                vs.append((rx*math.cos(t),y,z+ss*(up if ss>=0 else down)))
        fs=[tuple(reversed(range(n)))]
        for k in range(len(rings)-1):
            for j in range(n):
                a=k*n+j;b=k*n+(j+1)%n;c=(k+1)*n+(j+1)%n;d=(k+1)*n+j
                if (k+j)%2:fs.extend([(a,b,d),(b,c,d)])
                else:fs.extend([(a,b,c),(a,c,d)])
        fs.append(tuple((len(rings)-1)*n+j for j in range(n)))
        return vs,fs
    def loft(name,rings,n,materials):return mesh(name,*rings_mesh(rings,n),materials)
    def tube_data(points,radii,n=10):
        vs=[]
        for i,point in enumerate(points):
            c=Vector(point);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.normalize()
            ref=Vector((1,0,0))
            if abs(t.dot(ref))>.95:ref=Vector((0,1,0))
            u=(ref-t*t.dot(ref)).normalized();v=t.cross(u).normalized();rr=radii[i];a,b=(rr,rr) if isinstance(rr,(int,float)) else rr
            vs.extend([tuple(c+u*a*math.cos(math.tau*j/n)+v*b*math.sin(math.tau*j/n)) for j in range(n)])
        fs=[tuple(reversed(range(n)))]
        for i in range(len(points)-1):
            for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        fs.append(tuple((len(points)-1)*n+j for j in range(n)));return vs,fs
    def tube(name,points,radii,n,materials):return mesh(name,*tube_data(points,radii,n),materials)
    def ellipsoid_data(c,r,n=10,lat=5):
        vs=[(c[0],c[1],c[2]+r[2])]
        for k in range(1,lat):
            q=math.pi*k/lat
            vs.extend([(c[0]+r[0]*math.sin(q)*math.cos(math.tau*j/n),c[1]+r[1]*math.sin(q)*math.sin(math.tau*j/n),c[2]+r[2]*math.cos(q)) for j in range(n)])
        vs.append((c[0],c[1],c[2]-r[2]));b=len(vs)-1
        fs=[(0,1+j,1+(j+1)%n) for j in range(n)]
        for k in range(lat-2):
            for j in range(n):fs.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
        fs.extend([(b,1+(lat-2)*n+(j+1)%n,1+(lat-2)*n+j) for j in range(n)]);return vs,fs
    def ellipsoid(name,c,r,materials,n=10,lat=5):return mesh(name,*ellipsoid_data(c,r,n,lat),materials)
    # Rear pelvis narrows into waist. Ribcage and broad muscular forequarter flow
    # into the rising neck as one continuous loft instead of stacked spheres.
    body=loft('torso_and_powerful_neck',[
        (.430,.480,.023,.048,.060),(.390,.480,.085,.095,.100),
        (.300,.470,.120,.133,.120),(.200,.461,.117,.145,.078),
        (.095,.456,.130,.159,.113),(-.035,.463,.151,.173,.153),
        (-.155,.469,.159,.181,.170),(-.255,.485,.141,.170,.172),
        (-.330,.535,.120,.142,.153),(-.395,.598,.101,.117,.121),
        (-.442,.654,.078,.090,.084)],16,['body','under'])
    for f in body.data.polygons:
        if f.center.z<.375 and -.30<f.center.y<.21:f.material_index=1
    # F:AM61640-informed head: deep cheek and mandibular region, pronounced
    # cranial vault, sharp forehead-to-rostrum step and broad short muzzle.
    head=loft('domed_cranium_short_broad_muzzle',[
        (-.421,.690,.059,.081,.076),(-.449,.698,.084,.110,.096),
        (-.480,.701,.103,.113,.108),(-.511,.694,.099,.095,.098),
        (-.535,.680,.084,.065,.079),(-.554,.670,.069,.043,.059),
        (-.590,.665,.063,.038,.050),(-.625,.662,.058,.031,.040),
        (-.649,.661,.049,.024,.030)],16,['body','under'])
    for f in head.data.polygons:
        if f.center.z<.645 and f.center.y<-.53:f.material_index=1
    jaw=loft('deep_mandibular_body',[
        (-.461,.617,.067,.035,.030),(-.495,.613,.085,.041,.037),
        (-.536,.614,.073,.031,.032),(-.579,.618,.059,.023,.025),
        (-.622,.626,.047,.018,.019)],12,['under'])
    ellipsoid('nose_leather',(0,-.652,.671),(.043,.018,.022),['nose'],12,5)
    for s,label in [(-1,'left'),(1,'right')]:
        # Eyes sit at anterolateral orbit rim, neither front-facing cat orbits nor
        # oversized cartoon eyes. Small sclera-free dark eyes are reconstruction.
        ellipsoid('eye_'+label,(s*.087,-.521,.722),(.011,.015,.009),['eye'],10,5)
        tube('closed_mouth_'+label,[(s*.042,-.646,.641),(s*.059,-.610,.637),(s*.069,-.565,.635),(s*.080,-.529,.634)], [.0019,.0020,.0020,.0015],6,['nose'])
        # Low compact auricles remain distinct above the dome. No copied pattern.
        ear=tube('ear_'+label,[(s*.060,-.444,.771),(s*.076,-.436,.806),(s*.083,-.431,.840),(s*.079,-.437,.858)],[(.031,.022),(.028,.015),(.017,.009),(.0025,.0025)],8,['body','ear'])
        for f in ear.data.polygons:
            if f.normal.y<-.25:f.material_index=1
    feet=[]
    for s,label in [(-1,'left'),(1,'right')]:
        # Subtle contralateral stance offsets expose four legs without a gait
        # claim. Fore upper arm bends back to elbow; carpus/pastern return forward.
        fy=-.257 if s==1 else -.207;fx=s*.126
        tube('foreleg_'+label,[(s*.080,-.199,.553),(s*.116,-.197,.506),(s*.135,-.175,.435),(s*.136,-.125,.316),(s*.131,-.182,.204),(fx,fy+.015,.106),(fx,fy-.003,.053)],[(.037,.042),(.061,.067),(.051,.059),(.036,.043),(.026,.031),(.023,.027),(.031,.034)],12,['body'])
        hy=.290 if s==1 else .339;hx=s*.124
        tube('hindleg_'+label,[(s*.074,.303,.512),(s*.103,.303,.475),(s*.130,.267,.406),(s*.136,.205,.303),(s*.133,.327,.192),(hx,hy+.030,.101),(hx,hy,.054)],[(.039,.044),(.069,.075),(.061,.069),(.043,.050),(.027,.031),(.022,.025),(.028,.032)],12,['body'])
        feet.extend([('fore_'+label,fx,fy-.014),('hind_'+label,hx,hy-.015)])
    claws=[]
    for label,x,y in feet:
        ellipsoid('paw_metapad_'+label,(x,y+.008,.040),(.043,.046,.036),['body'],12,5)
        toes=[]
        for j,dx in enumerate([-.0315,-.0105,.0105,.0315]):
            central=j in (1,2);yy=y-.026 if central else y-.016
            # Closed, flattened toe lobes; discrete rounded lobes are not hooves.
            outline=[(-.6,-1),(.6,-1),(1,-.45),(1,.55),(.5,1),(-.5,1),(-1,.55),(-1,-.45)]
            w=.010;length=.032 if central else .027
            vs=[(x+dx+a*w,yy+b*length,.001) for a,b in outline]
            vs.extend([(x+dx+a*w*.92,yy+b*length*.84,.028 if b<0 else .041) for a,b in outline])
            fs=[tuple(reversed(range(8))),tuple(range(8,16))]+[(k,(k+1)%8,(k+1)%8+8,k+8) for k in range(8)]
            toes.append((vs,fs))
            claws.append(tube_data([(x+dx,yy-length+.005,.017),(x+dx,yy-length-.005,.012),(x+dx,yy-length-.011,.006)], [.0045,.0035,.0008],6))
        toe=mesh('four_toes_'+label,*join_data(toes),['body']);toe['weight_bearing_toe_count']=4
    mesh('restrained_nonretractile_claws',*join_data(claws),['claws'])
    tube('moderate_tapered_tail',[(0,.390,.534),(.010,.468,.513),(.022,.548,.461),(.036,.611,.398),(.044,.667,.333),(.046,.692,.292)],[(.039,.043),(.040,.043),(.034,.038),(.026,.031),(.016,.020),(.003,.004)],12,['body'])
    root['representation']='living-reconstruction';root['taxon']='Borophagus; cranial reference B. secundus F:AM61640'
    root['scientific_limit']='Head/body scale and all soft tissues are original reconstruction estimates, not a fossil scan.'
    root['skull_image_estimate_m']=.21;root['nose_rump_model_m']=1.1;root['shoulder_model_m']=.65;root['tail_model_m']=.36
    root['weight_bearing_toes_per_paw']=4
    bpy.context.view_layer.update();report=audit_source(col,cfg['budgets']['max_triangles'])
    if report['errors']:raise RuntimeError(report['errors'])
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    if set(opts)-set(bpy.ops.export_scene.gltf.get_rna_type().properties.keys()):raise RuntimeError('Missing required exporter options')
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=root;bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'));bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    glb=audit_glb(out/'model.glb',max_triangles=cfg['budgets']['max_triangles'],max_materials=cfg['budgets']['max_materials'],max_primitives=cfg['budgets']['max_primitives'])
    if glb['errors']:raise RuntimeError(glb['errors'])
    if (out/'model.glb').stat().st_size>cfg['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    src=report['bounds_blender_m'];mn=[src['min'][0],src['min'][2],-src['max'][1]];mx=[src['max'][0],src['max'][2],-src['min'][1]]
    err=max(abs(glb['bounds_m'][k][i]-v[i]) for k,v in [('min',mn),('max',mx)] for i in range(3))
    if err>1e-4 or glb['scene_triangles']!=report['triangles']:raise RuntimeError('Source/export mismatch')
    glb['file']='model.glb';write(out/'qa/evidence/glb-audit.json',glb)
    write(out/'qa/evidence/source.json',{'status':'PASS','source':report,'source_export_bounds_deviation_m':err,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'exporter_settings':opts,'generator_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'glb_sha256':sha(out/'model.glb')})
    print('BUILD_COMPLETE',json.dumps({'glb_sha256':sha(out/'model.glb'),'triangles':report['triangles'],'primitives':glb.get('primitives'),'source_status':report['status'],'glb_status':glb['status']}))
if __name__=='__main__':main()
