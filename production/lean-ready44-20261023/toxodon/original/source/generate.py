#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Toxodon whole-animal reconstruction, seed 632, in meters.
No fossil imagery is included in the meshes. Body size and soft tissues are
artistic estimates; named fossil measurements belong to distinct specimens.
Run Blender in background with two threads, then -- --output DIRECTORY.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((SOURCE/'params.json').read_text());col=setup_scene('toxodon',cfg['seed']);root=bpy.data.objects[col['asset_root']]
    mats={n:make_material(n,s['hex'],roughness=s['roughness']) for n,s in cfg['palette'].items()}
    def mesh(name,vs,fs,ma):
        ob=mesh_object(name,vs,fs,[mats[x] for x in ma],col);ob['anatomical_part']=name;return ob
    def loft(name,rings,n,ma):
        # Y-directed shaped sections: center y,z, horizontal radius, vertical radius.
        vs=[]
        for y,z,rx,rz in rings:
            for j in range(n):
                a=math.tau*j/n;vs.append((rx*math.cos(a),y,z+rz*math.sin(a)))
        fs=[tuple(reversed(range(n)))]
        for k in range(len(rings)-1):
            for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
        fs.append(tuple((len(rings)-1)*n+j for j in range(n)))
        return mesh(name,vs,fs,ma)
    def tube(name,pts,radii,n,ma):
        vs=[]
        for i,p in enumerate(pts):
            p=Vector(p);t=(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(i-1,0)])).normalized();u=Vector((1,0,0))
            if abs(t.dot(u))>.94:u=Vector((0,1,0))
            u=(u-t*t.dot(u)).normalized();v=t.cross(u).normalized();r=radii[i];a,b=(r,r) if isinstance(r,(float,int)) else r
            vs.extend([tuple(p+u*a*math.cos(j*math.tau/n)+v*b*math.sin(j*math.tau/n)) for j in range(n)])
        fs=[tuple(reversed(range(n)))]
        for k in range(len(pts)-1):
            for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
        fs.append(tuple((len(pts)-1)*n+j for j in range(n)))
        return mesh(name,vs,fs,ma)
    def oval(name,c,r,ma,n=10,lat=5):
        vs=[(c[0],c[1],c[2]+r[2])]
        for k in range(1,lat):
            p=math.pi*k/lat
            for j in range(n):
                a=math.tau*j/n;vs.append((c[0]+r[0]*math.sin(p)*math.cos(a),c[1]+r[1]*math.sin(p)*math.sin(a),c[2]+r[2]*math.cos(p)))
        vs.append((c[0],c[1],c[2]-r[2]));end=len(vs)-1
        fs=[(0,1+j,1+(j+1)%n) for j in range(n)]
        for k in range(lat-2):
            for j in range(n):fs.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
        fs.extend([(end,1+(lat-2)*n+(j+1)%n,1+(lat-2)*n+j) for j in range(n)])
        return mesh(name,vs,fs,ma)
    # Deep elongated barrel, mildly higher hindquarter, and a short low neck.
    body=loft('barrel_torso_and_short_neck',[
        (1.10,1.00,.055,.10),(1.04,1.01,.19,.25),(.91,1.00,.32,.36),
        (.70,.975,.41,.425),(.40,.94,.465,.44),(.10,.92,.475,.435),
        (-.20,.92,.46,.43),(-.45,.94,.405,.41),(-.61,.94,.32,.37),
        (-.74,.93,.255,.29),(-.87,.92,.23,.245),(-.97,.89,.21,.22)],16,['coat','belly'])
    for p in body.data.polygons:
        if p.center.z<.64:p.material_index=1
    # The short head descends toward a broad, restrained muzzle, not a hippo gape.
    head=loft('low_cranium_and_upper_muzzle',[
        (-.91,.88,.16,.21),(-.99,.84,.235,.245),(-1.10,.81,.25,.24),
        (-1.22,.785,.225,.215),(-1.34,.76,.205,.18),(-1.46,.725,.215,.135),
        (-1.55,.695,.205,.10),(-1.60,.68,.165,.065)],12,['coat','muzzle'])
    for p in head.data.polygons:
        if p.center.y< -1.43:p.material_index=1
    jaw=loft('deep_mandible',[
        (-.97,.69,.17,.16),(-1.09,.59,.215,.17),(-1.22,.505,.20,.12),
        (-1.37,.46,.175,.07),(-1.49,.465,.19,.06),(-1.58,.48,.155,.045)],12,['muzzle'])
    # Recessed continuous oral cavity prevents light-through gaps; front teeth are separate.
    cavity=loft('recessed_oral_cavity',[(-1.17,.62,.18,.045),(-1.34,.59,.175,.07),(-1.49,.565,.172,.052),(-1.575,.55,.145,.025)],12,['dark'])
    for s,side in [(-1,'left'),(1,'right')]:
        oval('eye_'+side,(s*.228,-1.09,.937),(.023,.033,.021),['dark'])
        oval('nostril_'+side,(s*.147,-1.567,.729),(.023,.019,.015),['dark'],8,4)
        ear=tube('ear_'+side,[(s*.181,-.976,1.045),(s*.245,-.94,1.105),(s*.286,-.915,1.139),(s*.309,-.909,1.133)],[(.047,.027),(.060,.027),(.041,.018),(.008,.007)],8,['coat','muzzle'])
        for f in ear.data.polygons:
            if f.normal.y<-.15:f.material_index=1
        # Enlarged upper lateral I2: broad curved chisels, not canine/elephant tusks.
        tooth=tube('upper_I2_'+side,[(s*.153,-1.51,.645),(s*.160,-1.565,.615),(s*.164,-1.602,.569),(s*.164,-1.611,.529),(s*.159,-1.593,.502)],[(.048,.039),(.044,.034),(.039,.028),(.033,.021),(.027,.009)],8,['enamel'])
        tooth['evidence']='Enlarged I2 supported; exposed curve and missing tip conservatively reconstructed.'
        # Three lower incisors per side, with wider outer i3 and restrained exposed crowns.
        for idx,(x,w) in enumerate([(.027,.023),(.079,.025),(.137,.035)],1):
            ys=-1.555+(.012 if idx==3 else 0)
            tooth=tube('lower_i%d_%s'%(idx,side),[(s*x,ys+.026,.485),(s*x,ys-.008,.505),(s*x,ys-.032,.537),(s*x,ys-.029,.556)],[(w,.027),(w,.024),(w*.95,.018),(w*.91,.008)],6,['enamel'])
            tooth['evidence']='Partial lower incisors; i3 base wider than i1/i2. Exposed tip restored.'
    # Four robust whole limbs; knees and hocks defined by tapered section changes.
    feet=[]
    for s,side in [(-1,'left'),(1,'right')]:
        fy=-.70 if s==1 else -.57;hy=.57 if s==1 else .70;fx=s*.315;hx=s*.32
        tube('forelimb_'+side,[(s*.27,-.49,1.01),(s*.31,-.48,.79),(s*.315,-.43,.59),(s*.32,-.53,.40),(fx,fy+.02,.21),(fx,fy,.105)],[(.145,.17),(.13,.135),(.10,.115),(.078,.09),(.074,.078),(.095,.10)],12,['coat'])
        tube('hindlimb_'+side,[(s*.27,.73,1.07),(s*.31,.64,.84),(s*.335,.48,.63),(s*.34,.72,.38),(hx,hy+.03,.20),(hx,hy,.105)],[(.165,.20),(.145,.17),(.105,.12),(.078,.09),(.076,.082),(.095,.10)],12,['coat'])
        feet.extend([('fore_'+side,fx,fy),('hind_'+side,hx,hy)])
    for label,x,y in feet:
        oval('foot_pad_'+label,(x,y,.098),(.135,.126,.075),['coat'],10,4)
        for j,dx in enumerate([-.088,0,.088],1):
            central=j==2;w=.048 if central else .037;length=.13 if central else .103;yc=y-.006 if central else y+.012
            outline=[(-.63,-1),(.63,-1),(1,-.55),(1,.5),(.60,1),(-.60,1),(-1,.5),(-1,-.55)]
            vs=[(x+dx+a*w,yc+b*length,0) for a,b in outline]
            vs.extend([(x+dx+a*w*.85,yc+b*length*.82,.080 if b<0 else .115) for a,b in outline])
            fs=[tuple(reversed(range(8))),tuple(range(8,16))]+[(k,(k+1)%8,(k+1)%8+8,k+8) for k in range(8)]
            ob=mesh('toe_'+label+'_'+str(j),vs,fs,['hoof']);ob['toe_index']=j;ob['foot']=label
    tube('short_tapering_tail',[(0,1.025,1.12),(.015,1.15,1.105),(.027,1.25,1.04),(.033,1.32,.95),(.036,1.35,.85),(.034,1.349,.78)],[(.055,.06),.043,.032,.024,.015,.004],8,['coat'])
    root['representation']='living-reconstruction';root['reconstruction']='Composite T. platensis-oriented reconstruction; references explicitly include cf. T. platensis.'
    root['incisor_tips']='Conservative restored tips; complete curvature not preserved by cited fossils.'
    root['scale']='Whole-body estimates, not directly measured from a single associated individual.'
    root['head_body_m']=2.7;root['shoulder_m']=1.35;root['toe_count_per_foot']=3
    # Floor-contact bounding center defines the identity root, including all four toe pads.
    contacts=[v.co.copy() for o in col.all_objects if o.type=='MESH' and o.name.startswith('toe_') for v in o.data.vertices if abs(v.co.z)<1e-9]
    shift=Vector(((min(v.x for v in contacts)+max(v.x for v in contacts))/2,(min(v.y for v in contacts)+max(v.y for v in contacts))/2,0))
    for o in col.all_objects:
        if o.type=='MESH':
            for v in o.data.vertices:v.co-=shift
    root['contact_center_shift_m']=list(shift);bpy.context.view_layer.update()
    report=audit_source(col,cfg['budgets']['max_triangles'])
    if report['errors']:raise RuntimeError(report['errors'])
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available=set(bpy.ops.export_scene.gltf.get_rna_type().properties.keys())
    if set(opts)-available:raise RuntimeError('Required exporter options unavailable')
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=root;bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    qa=audit_glb(out/'model.glb',max_triangles=cfg['budgets']['max_triangles'],max_materials=cfg['budgets']['max_materials'],max_primitives=cfg['budgets']['max_primitives'])
    if qa['errors']:raise RuntimeError(qa['errors'])
    if (out/'model.glb').stat().st_size>cfg['budgets']['max_glb_bytes']:raise RuntimeError('GLB bytes exceed brief')
    b=report['bounds_blender_m'];mn=[b['min'][0],b['min'][2],-b['max'][1]];mx=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(qa['bounds_m'][k][i]-v[i]) for k,v in [('min',mn),('max',mx)] for i in range(3))
    if delta>1e-4 or qa['scene_triangles']!=report['triangles']:raise RuntimeError('Source/export mismatch')
    qa['file']='model.glb'
    write(out/'qa/evidence/source.json',{'status':'PASS','source':report,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'exporter_settings':opts,'generator_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'glb_sha256':sha(out/'model.glb'),'bounds_expected_gltf_m':{'min':mn,'max':mx},'bounds_deviation_m':delta})
    write(out/'qa/evidence/glb-audit.json',qa)
    print('BUILD_COMPLETE',json.dumps({'glb_sha256':sha(out/'model.glb'),'triangles':report['triangles'],'primitives':qa['scene_primitives_estimated_base_draw_calls'],'status':qa['status']}))
if __name__=='__main__':main()
