#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original Plateosaurus, Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output .
All model-building dependencies are vendored beside this script.
"""
import argparse, hashlib, json, math, os, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene,make_material,mesh_object,ground_asset,audit_source
from qa_glb import audit_glb

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,data):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

class Builder:
    """Closed explicit profile components with semantic vertex groups."""
    def __init__(self,name,materials):
        self.name=name; self.materials=materials; self.v=[]; self.f=[]; self.mi=[]; self.groups={}
    def component(self,label,vertices,faces,material_indices=None):
        base=len(self.v); self.v.extend(vertices)
        self.f.extend(tuple(base+i for i in f) for f in faces)
        self.mi.extend(material_indices or [0]*len(faces))
        self.groups[label]=list(range(base,len(self.v)))
    def axial(self,label,sections,sides=16,palette=False):
        # Sections: longitudinal Y, center Z, X radius, upper/lower Z radius.
        v=[]; f=[]; ids=[]
        for y,z,rx,ru,rd in sections:
            for j in range(sides):
                a=2*math.pi*j/sides; sn=math.sin(a)
                v.append((rx*math.cos(a),y,z+(ru if sn>=0 else rd)*sn))
        for i in range(len(sections)-1):
            for j in range(sides):
                f.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
                a=2*math.pi*(j+.5)/sides
                ids.append(1 if palette and math.sin(a)>.66 else 2 if palette and math.sin(a)<-.50 else 0)
        for ring,reverse in [(0,True),(len(sections)-1,False)]:
            y,z,*_=sections[ring]; cap=len(v); v.append((0,y,z))
            for j in range(sides):
                f.append((cap,ring*sides+(j+1)%sides,ring*sides+j) if reverse else (cap,ring*sides+j,ring*sides+(j+1)%sides)); ids.append(0)
        self.component(label,v,f,ids)
    def tube(self,label,nodes,sides=10,frame=(1,0,0)):
        # Each node is x,y,z,radius-u,radius-v. Project reference to avoid twist.
        v=[];f=[];centers=[Vector(n[:3]) for n in nodes];ref=Vector(frame)
        for i,node in enumerate(nodes):
            t=(centers[min(i+1,len(nodes)-1)]-centers[max(i-1,0)]).normalized()
            u=ref-t*ref.dot(t)
            if u.length<.001:
                alt=Vector((0,0,1));u=alt-t*alt.dot(t)
            u.normalize();w=t.cross(u).normalized()
            for j in range(sides):
                a=2*math.pi*j/sides;v.append(tuple(centers[i]+u*node[3]*math.cos(a)+w*node[4]*math.sin(a)))
        for i in range(len(nodes)-1):
            for j in range(sides): f.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
        for ring,reverse in [(0,True),(len(nodes)-1,False)]:
            cap=len(v);v.append(tuple(centers[ring]))
            for j in range(sides):
                f.append((cap,ring*sides+(j+1)%sides,ring*sides+j) if reverse else (cap,ring*sides+j,ring*sides+(j+1)%sides))
        self.component(label,v,f)
    def lens(self,label,center,ry,rz,depth,sign,sides=12):
        x,y,z=center
        v=[(x,y+ry*math.cos(2*math.pi*j/sides),z+rz*math.sin(2*math.pi*j/sides)) for j in range(sides)]
        v += [(x+sign*depth,y,z),(x-sign*.008,y,z)]
        f=[]
        for j in range(sides): f += [(j,(j+1)%sides,sides),((j+1)%sides,j,sides+1)]
        self.component(label,v,f)
    def finish(self,collection):
        obj=mesh_object(self.name,self.v,self.f,self.materials,collection)
        for poly,index in zip(obj.data.polygons,self.mi): poly.material_index=index
        for label,indices in self.groups.items(): obj.vertex_groups.new(name=label).add(indices,1,'REPLACE')
        obj['construction']='Original closed polygon profiles; disconnected anatomical components intentional.'
        return obj

def build(config):
    collection=setup_scene('plateosaurus',config['seed'])
    palette={k:make_material('Plateosaurus_'+k,v,roughness=.88) for k,v in config['palette'].items()}
    core=Builder('AxialBody_HeadNeckTrunkTail',[palette['skin'],palette['dorsal'],palette['ventral']])
    # One uninterrupted profile, small elongate skull, long neck, posteriorly
    # deeper/wider pear abdomen and tail. Soft tissues are interpretative.
    core.axial('AxialProfile',[
        (-3.20,2.60,.025,.040,.040),(-3.15,2.61,.085,.080,.075),
        (-2.99,2.63,.105,.105,.090),(-2.84,2.66,.119,.150,.120),
        (-2.70,2.67,.125,.165,.130),(-2.57,2.64,.100,.105,.100),
        (-2.43,2.58,.096,.130,.125),(-2.22,2.52,.106,.152,.150),
        (-2.00,2.43,.122,.177,.180),(-1.79,2.28,.148,.210,.215),
        (-1.58,2.07,.188,.252,.250),(-1.35,1.91,.240,.302,.315),
        (-1.11,1.82,.302,.360,.390),(-.83,1.76,.365,.410,.480),
        (-.48,1.72,.450,.455,.610),(-.10,1.70,.530,.500,.710),
        (.27,1.72,.570,.510,.710),(.58,1.77,.530,.450,.610),
        (.85,1.82,.400,.365,.430),(1.12,1.86,.295,.285,.280),
        (1.48,1.85,.231,.225,.225),(1.91,1.80,.174,.177,.177),
        (2.34,1.75,.122,.134,.134),(2.76,1.73,.078,.087,.087),
        (3.13,1.76,.047,.054,.054),(3.46,1.81,.026,.031,.031),
        (3.78,1.88,.006,.007,.007),(3.80,1.885,.0018,.002,.002)
    ],sides=16,palette=True)
    legs=Builder('Hindlimbs_DigitigradeFeet',[palette['skin']])
    arms=Builder('Forelimbs_InwardGraspingHands',[palette['skin']])
    horns=Builder('ManualAndPedalClaws',[palette['keratin']])
    iris=Builder('EyeIrises',[palette['iris']])
    details=Builder('Pupils_Nostrils_MouthLine',[palette['dark']])
    for sign,side,step in [(1,'Left',-.08),(-1,'Right',.08)]:
        def mirrored(nodes): return [(sign*x,y,z,a,b) for x,y,z,a,b in nodes]
        legs.tube(side+'_Hindlimb',mirrored([
            (.40,.48+step,1.79,.235,.295),(.47,.33+step,1.55,.270,.325),
            (.50,.06+step,1.22,.230,.280),(.51,-.06+step,1.00,.155,.185),
            (.51,.04+step,.82,.125,.145),(.50,.25+step,.54,.092,.110),
            (.49,.27+step,.36,.090,.100),(.49,.13+step,.20,.115,.115),
            (.49,-.02+step,.115,.170,.090)
        ]),sides=12)
        # Three strong forward toes and a smaller medial digit I.
        for digit,dx,length,spread,width in [('II',-.12,.34,-.055,.065),('III',0,.44,.008,.073),('IV',.12,.31,.075,.060)]:
            x=.49+dx;end_y=-.02+step-length
            legs.tube(side+'_Pedal'+digit,mirrored([
                (x*.65+.49*.35,.00+step,.11,width*1.2,.075),
                (x,-.12+step,.080,width,.065),
                (x+spread*.65,end_y+.095,.067,width*.80,.055),
                (x+spread,end_y,.058,width*.58,.044)
            ]),sides=8)
            horns.tube(side+'_PedalClaw'+digit,mirrored([
                (x+spread*.85,end_y+.035,.064,width*.60,.045),
                (x+spread,end_y-.045,.055,width*.44,.031),
                (x+spread*1.03,end_y-.105,.025,.004,.005)
            ]),sides=8)
        legs.tube(side+'_PedalI',mirrored([
            (.37,.075+step,.18,.055,.060),(.30,-.015+step,.13,.050,.050),(.285,-.14+step,.087,.035,.035)
        ]),sides=8)
        horns.tube(side+'_PedalClawI',mirrored([
            (.285,-.12+step,.087,.036,.034),(.272,-.20+step,.075,.023,.022),(.265,-.25+step,.055,.003,.004)
        ]),sides=8)
        # Free arm with sagittal Y-Z palm, normal facing opposite hand.
        arms.tube(side+'_UpperAndLowerArm',mirrored([
            (.30,-.80,1.86,.135,.155),(.41,-.65,1.67,.145,.155),
            (.55,-.43,1.39,.110,.115),(.59,-.44,1.28,.090,.100),
            (.61,-.65,1.21,.075,.080),(.62,-.86,1.17,.060,.067)
        ]),sides=10)
        arms.tube(side+'_SagittalPalm',mirrored([
            (.62,-.87,1.18,.052,.067),(.62,-.96,1.09,.056,.125),(.62,-1.00,1.01,.050,.133)
        ]),sides=10)
        # Five differentiated fingers; robust digit I has the biggest claw.
        arms.tube(side+'_ManualI_Thumb',mirrored([
            (.615,-1.105,1.090,.048,.054),(.595,-1.180,1.005,.052,.054),(.565,-1.218,.953,.047,.045)
        ]),sides=8)
        horns.tube(side+'_EnlargedCurvedThumbClaw',mirrored([
            (.565,-1.213,.960,.049,.048),(.528,-1.255,.902,.044,.041),
            (.475,-1.258,.856,.029,.029),(.435,-1.221,.848,.004,.005)
        ]),sides=9)
        for digit,y,length,radius,bend in [('II',-1.078,.235,.037,.055),('III',-.989,.285,.035,.075),('IV',-.908,.205,.030,.045),('V',-.839,.133,.025,.025)]:
            endz=1.015-length
            arms.tube(side+'_Manual'+digit,mirrored([
                (.624,y,1.035,radius,radius),(.625,y-.015,1.015-length*.45,radius*.92,radius*.92),
                (.595,y-.022,endz+.035,radius*.76,radius*.76),(.625-bend,y-.028,endz,radius*.50,radius*.50)
            ]),sides=8)
            if digit in ('II','III'):
                horns.tube(side+'_ManualClaw'+digit,mirrored([
                    (.625-bend+.008,y-.026,endz+.018,radius*.60,radius*.57),
                    (.625-bend-.019,y-.034,endz-.015,radius*.35,radius*.32),
                    (.625-bend-.042,y-.042,endz-.005,.003,.003)
                ]),sides=7)
        iris.lens(side+'_Iris',(sign*.116,-2.745,2.727),.043,.040,.015,sign)
        details.lens(side+'_Pupil',(sign*.132,-2.752,2.728),.018,.025,.006,sign)
        details.lens(side+'_Nostril',(sign*.091,-3.048,2.651),.014,.009,.004,sign,sides=8)
        details.tube(side+'_MouthSeam',mirrored([
            (.074,-3.155,2.580,.003,.003),(.099,-3.017,2.591,.004,.004),
            (.108,-2.859,2.606,.004,.004),(.108,-2.730,2.610,.0025,.003)
        ]),sides=6,frame=(0,0,1))
    for part in (core,legs,arms,horns,iris,details): part.finish(collection)
    shift=ground_asset(collection,center_xy=False)
    # Place the identity root at the center of the low hindfoot support envelope.
    contacts=[o.matrix_world@v.co for o in collection.all_objects if o.type=='MESH'
              for v in o.data.vertices if (o.matrix_world@v.co).z<.035]
    shift[1]=-(min(v.y for v in contacts)+max(v.y for v in contacts))/2
    for o in collection.all_objects:
        if o.type=='MESH': o.location.y+=shift[1]
    bpy.context.view_layer.update()
    root=bpy.data.objects['plateosaurus']
    root['representation']='living-reconstruction'
    root['scope']='Original adult bipedal reconstruction; not a replica of one fossil mount.'
    root['scale_basis']='7 m taxon estimate, not a measurement of GPIT/RE/7288.'
    root['scientific_limits']='Soft tissues and palette interpretative; named hand composite; no juvenile proportions transferred.'
    return collection,shift

def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE.parent)
    options=parser.parse_args(args);output=options.output.resolve();output.mkdir(parents=True,exist_ok=True)
    config=json.loads((HERE/'params.json').read_text())
    if bpy.app.version_string!=config['blender_version']: raise RuntimeError('Pinned Blender runtime differs')
    collection,shift=build(config)
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    source=audit_source(collection,config['max_triangles'])
    if source['errors']: raise RuntimeError('Source audit failed: '+str(source['errors']))
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//renders/'
    # Portable source UI: remove machine-specific file-browser directories.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'_'*1023
                    space.params.directory=b'//'
                    space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'model.blend'),check_existing=False)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.all_objects: obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['plateosaurus']
    export=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
        export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',
        export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,
        export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,
        export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(export)-available: raise RuntimeError('Missing exporter flags')
    bpy.ops.export_scene.gltf(filepath=str(output/'model.glb'),**export)
    os.chdir(output)
    glb=audit_glb(Path('model.glb'),config['max_triangles'],config['max_materials'],config['max_primitives'])
    if glb['errors']: raise RuntimeError('GLB audit failed: '+str(glb['errors']))
    if glb['bytes']>config['max_glb_bytes']: raise RuntimeError('GLB bytes exceed budget')
    b=source['bounds_blender_m']
    expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][a][i]-expected[a][i]) for a in ['min','max'] for i in range(3))
    assert delta<.0001 and source['triangles']==glb['scene_triangles']
    report={'status':'PASS','scope':'Source meshes and static GLB audit only; no independent visual or GPU acceptance',
        'glb_sha256':sha(output/'model.glb'),'blend_sha256':sha(output/'model.blend'),
        'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),
        'blender_version':bpy.app.version_string,'gltf_exporter_version':'4.3.47',
        'exporter_required_flags_probed':True,'export_options':export,'source':source,'glb':glb,
        'source_export_bounds_error_m':delta,'ground_translation_m':shift,
        'profile':'Static uncompressed embedded-buffer palette-only',
        'source_components':'Six editable semantic mesh objects with named vertex groups.',
        'scale_note':'7.0 m nose-to-tail horizontal envelope, taxon estimate; pose is interpretative.'}
    write(output/'qa/evidence/source-export.json',report)
    print(json.dumps({'status':'BUILT','glb_sha256':report['glb_sha256'],'triangles':glb['scene_triangles'],'bytes':glb['bytes']}))
if __name__=='__main__': main()
