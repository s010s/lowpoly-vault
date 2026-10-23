#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Hyracodon reconstruction, meters; no reference image is incorporated.
Run using Blender background with two threads, followed by -- --output DIR.
Only params.json and the declared local deps are needed for mesh generation.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((SOURCE/'params.json').read_text())
    col=setup_scene(cfg['asset_id'],cfg['seed']); root=bpy.data.objects[col['asset_root']]
    mats={name:make_material(name,spec['hex'],roughness=spec['roughness']) for name,spec in cfg['palette'].items()}
    def mesh(name,verts,faces,materials):
        ob=mesh_object(name,verts,faces,[mats[k] for k in materials],col)
        ob['anatomical_part']=name
        return ob
    def loft(name,rings,n,materials,shade=False):
        # rings: center X,Y,Z; transverse X radius and sagittal radius in XY or XZ.
        verts=[]
        for center,rx,rz in rings:
            verts.extend([(center[0]+rx*math.cos(2*math.pi*j/n),center[1],center[2]+rz*math.sin(2*math.pi*j/n)) for j in range(n)])
        faces=[tuple(reversed(range(n)))]
        for k in range(len(rings)-1):
            for j in range(n): faces.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
        faces.append(tuple((len(rings)-1)*n+j for j in range(n)))
        ob=mesh(name,verts,faces,materials)
        if shade and len(materials)>1:
            for poly in ob.data.polygons:
                if poly.center.z < .57: poly.material_index=1
        return ob
    def tube(name,points,radii,n,materials):
        vs=[]
        for i,p in enumerate(points):
            p=Vector(p); tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
            tangent.normalize(); ref=Vector((1,0,0))
            if abs(tangent.dot(ref))>.94: ref=Vector((0,1,0))
            u=(ref-tangent*tangent.dot(ref)).normalized(); v=tangent.cross(u).normalized()
            r=radii[i]; rx,ry=(r,r) if isinstance(r,(int,float)) else r
            vs.extend([tuple(p+u*(rx*math.cos(j*2*math.pi/n))+v*(ry*math.sin(j*2*math.pi/n))) for j in range(n)])
        fs=[tuple(reversed(range(n)))]
        for i in range(len(points)-1):
            for j in range(n): fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        fs.append(tuple((len(points)-1)*n+j for j in range(n)))
        return mesh(name,vs,fs,materials)
    def ellipsoid(name,c,r,materials,n=8,lat=4):
        vs=[(c[0],c[1],c[2]+r[2])]
        for k in range(1,lat):
            phi=math.pi*k/lat
            vs.extend([(c[0]+r[0]*math.sin(phi)*math.cos(j*math.tau/n),c[1]+r[1]*math.sin(phi)*math.sin(j*math.tau/n),c[2]+r[2]*math.cos(phi)) for j in range(n)])
        vs.append((c[0],c[1],c[2]-r[2])); bottom=len(vs)-1
        fs=[(0,1+j,1+(j+1)%n) for j in range(n)]
        for k in range(lat-2):
            for j in range(n): fs.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
        fs.extend([(bottom,1+(lat-2)*n+(j+1)%n,1+(lat-2)*n+j) for j in range(n)])
        return mesh(name,vs,fs,materials)
    # Compact lightly built ribcage, uphill shoulder and muscular moderate neck.
    body=loft('torso_neck',[
        ((0,.525,.655),.035,.060),((0,.46,.655),.110,.125),
        ((0,.34,.650),.152,.147),((0,.17,.635),.164,.167),
        ((0,-.01,.636),.168,.178),((0,-.17,.654),.154,.166),
        ((0,-.295,.670),.128,.148),((0,-.39,.730),.099,.128),
        ((0,-.47,.785),.078,.092),((0,-.56,.808),.063,.070)],12,['coat','undercoat'],True)
    # Broad/deep cheek becomes a short constricted muzzle; dorsal surface has no horn.
    head=loft('deep_cheek_and_muzzle',[
        ((0,-.535,.809),.050,.079),((0,-.575,.797),.079,.109),
        ((0,-.63,.792),.085,.112),((0,-.682,.787),.075,.091),
        ((0,-.738,.785),.056,.066),((0,-.79,.780),.052,.050),
        ((0,-.825,.779),.046,.044)],12,['coat','muzzle'])
    for p in head.data.polygons:
        if p.center.y < -.757: p.material_index=1
    # Jaw is integrated through overlap, with a restrained mouth line on both sides.
    for s,label in [(-1,'left'),(1,'right')]:
        ellipsoid('eye_'+label,(s*.079,-.628,.842),(.012,.016,.012),['dark'],10,5)
        ellipsoid('nostril_'+label,(s*.046,-.793,.802),(.006,.014,.007),['dark'],8,4)
        tube('mouth_'+label,[(s*.044,-.818,.762),(s*.050,-.778,.750),(s*.059,-.728,.746)], [.0024,.0025,.0018],5,['dark'])
        # Sculpted leaf-shaped auricle, deliberately short, not rabbit/deer ears.
        tube('ear_'+label,[(s*.058,-.567,.888),(s*.078,-.557,.927),(s*.090,-.549,.961),(s*.087,-.550,.979)],[(.026,.018),(.029,.012),(.020,.009),(.003,.003)],8,['coat','ear'])
        ear=bpy.data.objects['ear_'+label]
        for p in ear.data.polygons:
            if p.normal.y<-.35: p.material_index=1
    # Four whole limbs with long slender zeugopods/metapods and restrained joints.
    feet=[]
    for s,label in [(-1,'left'),(1,'right')]:
        fy=-.305 if s==1 else -.245
        fx=s*.137
        tube('forelimb_'+label,[(s*.107,-.267,.690),(s*.127,-.246,.560),(s*.132,-.212,.454),(s*.131,-.260,.300),(fx,fy,.150),(fx,fy-.008,.073)],[(.063,.072),(.045,.054),(.034,.040),(.026,.030),(.022,.025),(.029,.036)],10,['coat'])
        hy=.330 if s==1 else .413
        hx=s*.151
        tube('hindlimb_'+label,[(s*.109,.355,.669),(s*.137,.335,.550),(s*.146,.262,.428),(s*.150,.412,.272),(hx,hy+.016,.139),(hx,hy,.070)],[(.079,.088),(.064,.070),(.042,.046),(.028,.032),(.021,.024),(.027,.034)],10,['coat'])
        feet.extend([('fore_'+label,fx,fy-.020),('hind_'+label,hx,hy-.015)])
    for label,x,y in feet:
        # A low skin pad feeds three distinct hoof lobes, with visible inter-toe gaps.
        ellipsoid('foot_pad_'+label,(x,y+.006,.061),(.043,.045,.032),['coat'],10,4)
        for j,dx in enumerate([-.033,0,.033]):
            central=j==1; width=.016 if central else .013
            yc=y-.022 if central else y-.011
            length=.048 if central else .037
            # Rounded polygon footprint extruded with a beveled sloped upper surface.
            outline=[(-.65,-1),(.65,-1),(1,-.5),(1,.55),(.6,1),(-.6,1),(-1,.55),(-1,-.5)]
            vs=[(x+dx+a*width,yc+b*length,.001) for a,b in outline]
            vs += [(x+dx+a*width*.88,yc+b*length*.85,.041 if b<0 else .056) for a,b in outline]
            fs=[tuple(reversed(range(8))),tuple(range(8,16))]
            fs += [(k,(k+1)%8,(k+1)%8+8,k+8) for k in range(8)]
            ob=mesh('toe_'+label+'_'+str(j+1),vs,fs,['hoof']); ob['toe_index']=j+1; ob['foot']=label
    tube('tapering_tail',[(0,.475,.710),(.009,.572,.696),(.018,.659,.646),(.020,.735,.558),(.016,.790,.469),(.011,.808,.426)],[(.027,.030),.023,.017,.012,.008,.003],8,['coat'])
    root['representation']='living-reconstruction'; root['scientific_scale']='inferred body dimensions; image-estimated skull length'
    root['nose_rump_m']=1.35; root['shoulder_height_m']=.80; root['toe_count_per_foot']=3
    bpy.context.view_layer.update()
    report=audit_source(col,cfg['budgets']['max_triangles'])
    if report['errors']: raise RuntimeError(report['errors'])
    export_opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available=set(bpy.ops.export_scene.gltf.get_rna_type().properties.keys())
    if set(export_opts)-available: raise RuntimeError('Missing required exporter settings')
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects: ob.select_set(True)
    bpy.context.view_layer.objects.active=root
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:
                    space.params.directory=b'//'
                    space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**export_opts)
    glb=audit_glb(out/'model.glb',max_triangles=cfg['budgets']['max_triangles'],max_materials=cfg['budgets']['max_materials'],max_primitives=cfg['budgets']['max_primitives'])
    if glb['errors']: raise RuntimeError(glb['errors'])
    if (out/'model.glb').stat().st_size>cfg['budgets']['max_glb_bytes']: raise RuntimeError('GLB byte budget exceeded')
    src=report['bounds_blender_m']; expected_min=[src['min'][0],src['min'][2],-src['max'][1]]; expected_max=[src['max'][0],src['max'][2],-src['min'][1]]
    deviation=max(abs(glb['bounds_m'][k][i]-v[i]) for k,v in [('min',expected_min),('max',expected_max)] for i in range(3))
    if deviation>1e-4 or glb['scene_triangles']!=report['triangles']: raise RuntimeError('Source/export mismatch')
    glb['file']='model.glb'
    report['source_export_bounds_deviation_m']=deviation
    write(out/'qa/evidence/source.json',{'status':'PASS','source':report,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'exporter_settings':export_opts,'generator_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'glb_sha256':sha(out/'model.glb'),'bounds_expected_gltf_m':{'min':expected_min,'max':expected_max}})
    write(out/'qa/evidence/glb-audit.json',glb)
    print('BUILD_COMPLETE',json.dumps({'glb_sha256':sha(out/'model.glb'),'triangles':report['triangles'],'source_status':report['status'],'glb_status':glb['status']}))
if __name__=='__main__': main()
