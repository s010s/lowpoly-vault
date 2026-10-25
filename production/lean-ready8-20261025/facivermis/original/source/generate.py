# SPDX-License-Identifier: MIT
"""Original Facivermis yunnanicus animal-only reconstruction, deterministic Blender source.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
No imported model, reference pixels, tube, display stage, rig or animation is incorporated.
"""
from pathlib import Path
import sys,json,hashlib,argparse,math,bisect
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
P={};C=None;M={};GROUND=0;CURVE=[];PARTS=[]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False,default=list)+'\n')
def mesh(name,vs,fs,mat,smooth=False):
    o=mesh_object(name,[tuple(v*.001) for v in map(Vector,vs)],fs,mat,C)
    if smooth:
        for p in o.data.polygons:p.use_smooth=True
    return o

def connect(fs,a,b,n):
    for j in range(n):fs.append((a+j,a+(j+1)%n,b+(j+1)%n,b+j))

def initialize_curve():
    # Unit-speed integration gives exactly 50 mm numerical arc length, not bounding-box length.
    global CURVE
    CURVE=[Vector((0,0,0))];n=2500;step=50/n
    for i in range(n):
        u=(i+.5)/n;theta=-.10+1.18*u*u
        t=Vector((.025*math.cos(math.pi*2*u),-math.sin(theta),math.cos(theta))).normalized()
        CURVE.append(CURVE[-1]+t*step)

def center(s):
    q=max(0,min(50,s))*50;i=min(2499,int(q));f=q-i
    return CURVE[i].lerp(CURVE[i+1],f)

def frame(s):
    t=(center(min(50,s+.015))-center(max(0,s-.015))).normalized()
    x=Vector((1,0,0));x=(x-t*x.dot(t)).normalized();d=t.cross(x).normalized()
    return x,d,t

PROFILE=[(0,.36),(.35,.76),(1.10,1.35),(2.10,1.48),(2.8,1.37),(3.7,1.08),(4.6,.92),(8,.90),(15,.88),(25,.84),(35,.82),(38,.86),(40,.93),(43,1.0),(45,.98),(47,.84),(48.2,.56),(48.6,.66),(49.15,.69),(49.6,.53),(50,.24)]
def radius(s):
    for (s0,r0),(s1,r1) in zip(PROFILE,PROFILE[1:]):
        if s0<=s<=s1:
            u=(s-s0)/(s1-s0);u=u*u*(3-2*u);return r0+(r1-r0)*u
    return PROFILE[0 if s<0 else -1][1]
def bodyring(s,r,n):
    x,d,t=frame(s);c=center(s)
    if s>49.3:c-=d*.12*((s-49.3)/.7)
    return [c+x*math.cos(2*math.pi*j/n)*r+d*math.sin(2*math.pi*j/n)*r*.94 for j in range(n)]

def body():
    a=P['anatomy'];n=a['body_radial_segments'];ss0=sorted([s for s,r in PROFILE]+[i*.35 for i in range(1,138)]);ss=[]
    for s in ss0:
        if not ss or s-ss[-1]>.001:ss.append(s)
    vs=[];fs=[]
    for i,s in enumerate(ss):
        # Shallow cuticle folds, not segmented plates or independent stacked rings.
        amp=a['annulation_amplitude_mm'] if 3.7<s<48.2 else .009
        r=radius(s)+amp*math.cos(s*2*math.pi/a['annulation_pitch_mm'])
        vs+=bodyring(s,r,n)
    for i in range(len(ss)-1):connect(fs,i*n,(i+1)*n,n)
    exterior=len(fs)
    # A restrained recessed terminal anus. Closed cavity at inner depth; no visible gut.
    last=0
    for s,r in [(0.04,.15),(.22,.105)]:
        start=len(vs);vs+=bodyring(s,r,n);connect(fs,last,start,n);last=start
    ci=len(vs);vs.append(center(.29))
    for j in range(n):fs.append((last+j,last+(j+1)%n,ci))
    # Slight ventral offset of the terminal lip; no radial teeth or invented jaws.
    last=(len(ss)-1)*n
    for s,r in [(49.96,.14),(49.68,.09)]:
        start=len(vs);vs+=bodyring(s,r,n);connect(fs,last,start,n);last=start
    ci=len(vs);vs.append(center(49.57)-frame(49.57)[1]*.07)
    for j in range(n):fs.append((last+j,last+(j+1)%n,ci))
    o=mesh('continuous-annulated-body-head-and-posterior',vs,fs,[M['cuticle'],M['ventral-cuticle'],M['orifice']],True)
    for i,p in enumerate(o.data.polygons):
        if i>=exterior:p.material_index=2
        elif i%n in [9,10,11,12,13]:p.material_index=1
    o['anatomy']='Continuous 50 mm anatomical centerline; long limbless middle, pear-shaped hook-bearing posterior, 1.8 mm small ovoid head.'
    o['body_centerline_length_m']=.05;o['head_extent_mm']=[48.2,50.0]
    o['annulations']='Shallow cuticle folds; count is representational, not a fixed biological segment count.'
    return o

def append_sweep(vs,fs,path,radii,n=5,cap=True):
    start=len(vs);nr=len(path);lastx=None
    for i,(c,r) in enumerate(zip(path,radii)):
        tangent=(path[min(i+1,nr-1)]-path[max(0,i-1)]).normalized()
        ref=Vector((0,0,1)) if abs(tangent.z)<.85 else Vector((0,1,0))
        x=tangent.cross(ref).normalized() if lastx is None else (lastx-tangent*lastx.dot(tangent)).normalized()
        y=tangent.cross(x).normalized();lastx=x
        vs += [c+x*math.cos(2*math.pi*j/n)*r+y*math.sin(2*math.pi*j/n)*r for j in range(n)]
    for i in range(nr-1):connect(fs,start+i*n,start+(i+1)*n,n)
    if cap:
        fs.append(tuple(start+j for j in range(n-1,-1,-1)))
        end=len(vs);tip=path[-1]+(path[-1]-path[-2]).normalized()*radii[-1]*1.2;vs.append(tip)
        for j in range(n):fs.append((start+(nr-1)*n+j,start+(nr-1)*n+(j+1)%n,end))

def limb(pair,side,s):
    x,d,t=frame(s);base=center(s)+(x*side*.79-d*.44)*radius(s)
    slopes=[.90,.57,.24,-.08,-.36];slope=slopes[pair-1]
    primary=(x*side*.91+t*slope-d*.24).normalized()
    bend=(t*.29-d*.15+x*side*.10)
    path=[];length=P['anatomy']['lobopod_length_mm']
    # Original tapered circular shaft, smoothly bent and not a flat fan.
    raw=[base+(primary*u+bend*(u*u))*length for u in [i/14 for i in range(15)]]
    arc=sum((b-a).length for a,b in zip(raw,raw[1:]));path=[base+(q-base)*(length/arc) for q in raw]
    radii=[(.34*(1-i/14)**.80+.032)*(1+.032*math.cos(i*math.pi)) for i in range(15)]
    vs=[];fs=[];append_sweep(vs,fs,path,radii,8)
    shaft_faces=len(fs)
    def at(u):
        q=u*14;i=min(13,int(q));return path[i].lerp(path[i+1],q-i)
    # Two distinct ventral setal rows per lobopod. Each solid seta starts inside its shaft.
    roots=[]
    for row in [-1,1]:
        for j in range(P['anatomy']['setae_per_ventral_row']):
            u=.17+j*.108;c=at(u);tan=(at(u+.01)-at(u-.01)).normalized()
            vent=(-d-tan*(-d).dot(tan)).normalized();cross=tan.cross(vent).normalized()
            radial=(vent*.77+cross*row*.64).normalized();r=.34*(1-u)**.80+.032
            root=c+radial*(r-.045);h=(.56+.18*math.sin(math.pi*u))*(.96 if side<0 else 1)
            direction=(radial*.85+tan*.34).normalized()
            tip=root+direction*h+tan*.08
            append_sweep(vs,fs,[root,tip],[.050,.020],5)
            roots.append(list(root))
    o=mesh(f'lobopod-pair-{pair}-'+('right' if side>0 else 'left'),vs,fs,[M['cuticle'],M['setae']],True)
    for i,p in enumerate(o.data.polygons):p.material_index=int(i>=shaft_faces)
    o['anterior_pair']=pair;o['side']='right' if side>0 else 'left';o['body_centerline_attachment_mm']=s
    o['shaft_length_m']=length*.001;o['setal_rows']=2;o['setae_each_row']=P['anatomy']['setae_per_ventral_row']
    o['attachment']='Circular ventrolateral shaft base with 0.12 mm embedded overlap; no separate limb joint or pad.'
    o['base_center_mm']=list(base);o['tip_center_mm']=list(path[-1]);o['seta_roots_mm']=roots
    return o

def posterior_hooks():
    for row,s in enumerate(P['anatomy']['posterior_hook_rings_mm']):
        vs=[];fs=[];x,d,t=frame(s)
        for k in range(P['anatomy']['hooks_per_ring']):
            a=2*math.pi*(k+.25*(row%2))/P['anatomy']['hooks_per_ring'];radial=x*math.cos(a)+d*math.sin(a)
            c=center(s)+radial*(radius(s)-.07)
            path=[c,c+radial*.20+t*.025,c+radial*.31+t*.18,c+radial*.29+t*.30]
            append_sweep(vs,fs,path,[.105,.080,.042,.022],5)
        o=mesh(f'posterior-hook-ring-{row+1}',vs,fs,M['hooks']);o['ring_index']=row+1;o['hooks']=P['anatomy']['hooks_per_ring'];o['interpretation']=P['anatomy']['posterior_hook_count_scope']

def trunk_cuticle():
    vs=[];fs=[]
    # Widely spaced, tiny rooted papillae/curved setae. No armor, limb pairs or uniform noise.
    for row,s in enumerate([6.3,9.8,13.4,17.0,20.6,24.2,27.8,31.4,35.0,37.2]):
        x,d,t=frame(s)
        for k in range(4):
            a=(k+.2+.35*(row%2))*math.pi/2;radial=x*math.cos(a)+d*math.sin(a)
            c=center(s)+radial*(radius(s)-.065);h=.18+.035*math.sin(row)
            append_sweep(vs,fs,[c,c+radial*h-t*.07],[.071,.022],5)
    o=mesh('restrained-middle-trunk-papillae-setae',vs,fs,M['cuticle']);o['anatomy']='Forty simplified short cuticular elements, not appendages or armored segment plates.';o['attachment']='All 40 base centers penetrate the continuous cuticle by 0.065 mm.'

def ocular_spots():
    # Low, shallow paired pigmentation patches; not eyeballs, eyestalks or compound eyes.
    for side in [-1,1]:
        s=49.08;x,d,t=frame(s);radial=(x*side*.70+d*.71).normalized();c=center(s)+radial*(radius(s)*.965)
        u=(t-radial*t.dot(radial)).normalized();v=radial.cross(u).normalized();vs=[];fs=[];n=10
        for depth,scale in [(-.055,1),(.020,.96),(.042,.60)]:
            for j in range(n):
                a=2*math.pi*j/n;vs.append(c+radial*depth+u*math.cos(a)*.155*scale+v*math.sin(a)*.120*scale)
        connect(fs,0,n,n);connect(fs,n,2*n,n);fs.append(tuple(range(n-1,-1,-1)));ci=len(vs);vs.append(c+radial*.050)
        for j in range(n):fs.append((2*n+j,2*n+(j+1)%n,ci))
        o=mesh('simple-ocular-spot-'+('right' if side>0 else 'left'),vs,fs,M['ocular-spots'],True);o['anatomy']='One dorsolateral simple ocellus-like pigmentation spot. Soft shape is interpretive.'

def build():
    global C,M,GROUND
    C=setup_scene('facivermis',P['seed']);initialize_curve()
    M={k:make_material(k,v,roughness=.80 if k!='ocular-spots' else .70) for k,v in P['surface']['palette_srgb'].items()}
    body()
    for pair,s in enumerate(P['anatomy']['anterior_pair_positions_mm'],1):
        for side in [-1,1]:limb(pair,side,s)
    posterior_hooks();trunk_cuticle();ocular_spots()
    vertices=[v for o in C.all_objects if o.type=='MESH' for v in o.data.vertices];GROUND=min(v.co.z for v in vertices)
    for v in vertices:v.co.z-=GROUND
    root=bpy.data.objects[C['asset_root']];root['body_centerline_length_m']=.05;root['posterior_xy_origin']='Terminal rear center';root['scene_prerequisite']='Separately authored tube habitat required; animal-only not a free-standing behavior claim.'
    root['classification']='Evidence-informed luolishaniid lobopodian reconstruction, not annelid';root['period_region']='Early Cambrian Chengjiang, Yunnan';bpy.context.view_layer.update();return C

def main():
    global P
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    P=json.loads((HERE/'params.json').read_text());col=build();policy=P['geometry_policy'];source=audit_source(col,policy['max_triangles'])
    source['authored_vertices']=sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH');source['evaluated_vertices']=source['authored_vertices']
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene.render.filepath='//';bpy.context.scene['generator']='source/generate.py';bpy.context.scene['scientific_scope']=P['interpretation'];bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(flags)-available:raise RuntimeError('Missing glTF exporter options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    glb=audit_glb(out/'model.glb',policy['max_triangles'],policy['max_materials'],policy['max_primitives']);glb['file']='model.glb'
    b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][s][i]-e[i]) for s,e in [('min',emin),('max',emax)] for i in range(3))
    if glb['errors'] or delta>1e-6 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>policy['max_glb_bytes']:raise RuntimeError('Source/export audit failed: '+str(glb['errors']))
    import io_scene_gltf2
    centerline=[list((v*.001)-Vector((0,0,GROUND))) for v in CURVE]
    dump(out/'technical.json',{'asset_id':'facivermis','revision':'r001','source':source,'glb':glb,'source_export_bounds_delta_m':delta,'blender_version':bpy.app.version_string,'exporter_version':io_scene_gltf2.bl_info['version'],'consumer_three_version':'0.180.0','consumer_scope':'Pin only until separate CPU parser test; GPU not tested.','export_options':flags,'source_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(out/'model.blend'),'anatomical_scope':P['interpretation'],'body_centerline_length_m':sum((b-a).length for a,b in zip(CURVE,CURVE[1:]))*.001,'ground_offset_m':GROUND,'semantic_parts':'One continuous annulated body with pear-shaped posterior and small ovoid head; ten anterior lobopods in five bilateral pairs, each with two setal rows; two hook rings; restrained trunk papillae; paired simple dorsolateral ocular spots. No tube, antennae, posterior limbs or stage.','smooth_shading_review':'Intentional smooth cuticle/limbs/pigmentation surfaces retain low-sided designed profiles; hooks and papillae have deliberate broad flat facets.'})
    dump(out/'anatomy-measurements.json',{'body_centerline_m':centerline,'body_centerline_length_m':sum((b-a).length for a,b in zip(CURVE,CURVE[1:]))*.001,'head_centerline_length_m':.0018,'limb_pairs':5,'limb_parts':[{'name':o.name,**dict(o.items())} for o in col.all_objects if o.type=='MESH' and o.name.startswith('lobopod-pair')],'source_units':'meter; explicitly labeled construction properties in mm','original_geometry':True,'tube_included':False})
if __name__=='__main__':main()
