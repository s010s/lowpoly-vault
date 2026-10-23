# SPDX-License-Identifier: MIT
"""Original deterministic complete Mantellisaurus living reconstruction.
Run: blender -b -t 2 -P source/generate.py -- --out . --mode build
Modes gray/final render a clean import of model.glb, never the authoring scene.
Anatomical reference images are not embedded. All dependencies are relative.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, _look_at
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('--out',default='.');parser.add_argument('--mode',choices=['build','gray','final'],default='build')
A=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(A.out).resolve();OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
class Mesh:
    def __init__(self):self.v=[];self.f=[];self.m=[];self.groups=[]
    def add(self,v,f,mi=0,name=None,indices=None):
        offset=len(self.v);self.v.extend(v);self.f.extend(tuple(offset+i for i in face) for face in f);self.m.extend(indices if indices is not None else [mi]*len(f))
        if name:self.groups.append((name,list(range(offset,len(self.v)))))
    def obj(self,name,mats,col):
        ob=mesh_object(name,self.v,self.f,mats,col)
        for poly,mi in zip(ob.data.polygons,self.m):poly.material_index=mi
        for gn,idx in self.groups:ob.vertex_groups.new(name=gn).add(idx,1,'REPLACE')
        return ob

def loft(mesh,rings,n=16,mi=0,name=None,axis='Y',palette=None):
    # Each profile: longitudinal position, lateral center, depth center, two radii.
    vs=[];fs=[];mids=[]
    for t,c1,c2,r1,r2 in rings:
        for k in range(n):
            a=2*math.pi*k/n
            vs.append((c1+r1*math.cos(a),t,c2+r2*math.sin(a)) if axis=='Y' else (c1+r1*math.cos(a),c2+r2*math.sin(a),t))
    fs.append(tuple(range(n-1,-1,-1)));mids.append(mi)
    for j in range(len(rings)-1):
        for k in range(n):
            a=j*n+k;b=j*n+(k+1)%n;c=(j+1)*n+(k+1)%n;d=(j+1)*n+k
            fs.extend([(a,b,c),(a,c,d)])
            material=mi
            if palette:
                h=math.sin(2*math.pi*(k+.5)/n)
                if h<-.45:material=palette[1]
                elif h>.76:material=palette[2]
            mids.extend([material,material])
    fs.append(tuple((len(rings)-1)*n+k for k in range(n)));mids.append(mi)
    mesh.add(vs,fs,mi,name,mids)

def tube(mesh,points,radii,n=10,mi=0,name=None):
    # Ring planes follow an explicit centerline: not a stack of untouched primitives.
    vs=[];fs=[]
    for j,p in enumerate(points):
        p=Vector(p);t=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(j-1,0)])
        t.normalize();basis=Vector((1,0,0))
        if abs(t.dot(basis))>.9:basis=Vector((0,1,0))
        u=(basis-t*t.dot(basis)).normalized();v=t.cross(u).normalized()
        rx,ry=radii[j] if isinstance(radii[j],tuple) else (radii[j],radii[j])
        for k in range(n):
            a=2*math.pi*k/n;vs.append(tuple(p+u*(math.cos(a)*rx)+v*(math.sin(a)*ry)))
    fs.append(tuple(range(n-1,-1,-1)))
    for j in range(len(points)-1):
        for k in range(n):
            a=j*n+k;b=j*n+(k+1)%n;c=(j+1)*n+(k+1)%n;d=(j+1)*n+k;fs.extend([(a,b,c),(a,c,d)])
    fs.append(tuple((len(points)-1)*n+k for k in range(n)));mesh.add(vs,fs,mi,name)

def ellipsoid(mesh,c,r,mi=0,n=12,lats=6,name=None):
    vs=[(c[0],c[1],c[2]-r[2])];fs=[]
    for j in range(1,lats):
        phi=-math.pi/2+math.pi*j/lats
        for k in range(n):
            a=2*math.pi*k/n;vs.append((c[0]+r[0]*math.cos(phi)*math.cos(a),c[1]+r[1]*math.cos(phi)*math.sin(a),c[2]+r[2]*math.sin(phi)))
    top=len(vs);vs.append((c[0],c[1],c[2]+r[2]))
    for k in range(n):fs.append((0,1+(k+1)%n,1+k))
    for j in range(lats-2):
        for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;c=b+n;d=a+n;fs.extend([(a,b,c),(a,c,d)])
    for k in range(n):fs.append((top,1+(lats-2)*n+k,1+(lats-2)*n+(k+1)%n))
    mesh.add(vs,fs,mi,name)

def build():
    col=setup_scene('mantellisaurus',P['seed']);m={k:make_material(k,v,roughness=.86) for k,v in P['palette'].items()}
    trunk=Mesh()
    # Continuous sinuous neck, light narrow ribcage, pelvic transition and long tail.
    rings=[(-2.06,0,2.53,.15,.18),(-1.90,0,2.48,.16,.21),(-1.71,0,2.36,.18,.25),(-1.52,0,2.22,.23,.31),(-1.30,0,2.12,.30,.40),(-1.03,0,2.04,.38,.48),(-.70,0,2.02,.43,.55),(-.33,0,2.06,.46,.59),(.04,0,2.12,.44,.58),(.36,0,2.18,.39,.51),(.65,0,2.19,.31,.40),(.95,0,2.17,.26,.32),(1.28,0,2.13,.225,.28),(1.64,0,2.08,.19,.23),(2.02,0,2.02,.154,.18),(2.40,0,1.95,.12,.14),(2.79,0,1.88,.092,.105),(3.15,0,1.82,.066,.077),(3.50,0,1.77,.045,.052),(3.82,0,1.73,.026,.031),(4.08,0,1.70,.014,.018),(4.30,0,1.68,.004,.006)]
    loft(trunk,rings,20,name='continuous light torso neck and tail',palette=[0,1,2]);trunk.obj('Light_torso_neck_and_complete_tail',[m['skin'],m['ventral'],m['dorsal']],col)
    head=Mesh()
    # Low elongated wedge skull, narrow keratin beak, no crest, no hadrosaur bill.
    hr=[(-2.70,0,2.49,.105,.080),(-2.65,0,2.50,.13,.095),(-2.52,0,2.52,.15,.12),(-2.37,0,2.55,.16,.145),(-2.23,0,2.58,.185,.18),(-2.09,0,2.60,.205,.20),(-1.96,0,2.59,.17,.185),(-1.88,0,2.57,.11,.14)]
    loft(head,hr,16,name='low elongated beaked head')
    for i in range(1,1+2*16*2):head.m[i]=1
    head.m[0]=1;head.obj('Low_long_skull_with_narrow_beak',[m['skin'],m['beak']],col)
    limbs=Mesh();feet=Mesh();hands=Mesh();horn=Mesh();details=Mesh()
    for s,side,dy in [(-1,'left',-.065),(1,'right',.065)]:
        # Slender long hindlimbs; enlarged proximal muscle tapers into bent shin.
        hind=[(2.30,s*.31,.31+dy,.21,.25),(2.13,s*.40,.24+dy,.245,.29),(1.88,s*.44,.12+dy,.235,.27),(1.62,s*.45,-.04+dy,.18,.20),(1.40,s*.46,-.10+dy,.125,.145),(1.22,s*.46,.02+dy,.102,.115),(.98,s*.47,.24+dy,.088,.099),(.74,s*.47,.42+dy,.078,.09),(.49,s*.47,.46+dy,.074,.09),(.27,s*.47,.37+dy,.09,.13),(.15,s*.47,.25+dy,.12,.18)]
        loft(limbs,hind,12,name=side+' hind thigh knee shin hock',axis='Z')
        # Humerus plus radius approximately 48% of femur plus tibia, free of ground.
        armpts=[(s*.29,-1.10,2.13),(s*.37,-1.03,1.94),(s*.42,-.84,1.69),(s*.42,-.85,1.59),(s*.42,-1.03,1.48),(s*.42,-1.21,1.37)]
        tube(limbs,armpts,[(.115,.14),(.12,.13),(.085,.095),(.072,.08),(.059,.067),(.052,.06)],12,name=side+' short free humerus and radius')
        # Central three digits form a compact palm, with visible separate outer digit.
        tube(hands,[(s*.42,-1.20,1.38),(s*.43,-1.28,1.30),(s*.43,-1.32,1.19)],[(.064,.055),(.085,.055),(.073,.04)],10,name=side+' compact central manus')
        for digit in [-1,0,1]:
            x=s*.43+digit*.045
            tube(hands,[(x,-1.32,1.23),(x,-1.35,1.17),(x,-1.35,1.135)],[(.025,.035),(.023,.026),(.012,.016)],8,name=side+' central finger '+str(digit+3))
        tube(hands,[(s*.49,-1.25,1.31),(s*.56,-1.24,1.27),(s*.59,-1.28,1.22)],[(.028,.028),(.026,.026),(.012,.014)],8,name=side+' separate grasping outer digit')
        # Small pointed thumb spike projects inward-forward, not a giant defensive horn.
        tube(horn,[(s*.365,-1.26,1.31),(s*.315,-1.34,1.34),(s*.275,-1.43,1.38)],[.037,.026,.003],8,name=side+' modest thumb spike')
        for digit in [-1,0,1]:
            cx=s*.47+digit*.12;end=-.21-(.10 if digit==0 else 0)+dy
            toe=[(.47+dy,cx,.16,.06,.085),(.25+dy,cx,.12,.08,.12),(.03+dy,cx+digit*.025,.085,.077,.085),(end,cx+digit*.05,.062,.063,.062)]
            loft(feet,toe,10,name=side+' three-toed pes digit '+str(digit+3))
            ellipsoid(horn,(cx+digit*.05,end-.035,.058),(.063,.075,.058),n=10,lats=4,name=side+' blunt toe hoof')
        ellipsoid(details,(s*.191,-2.14,2.68),(.023,.047,.038),n=10,lats=5,name=side+' lateral eye')
        ellipsoid(details,(s*.148,-2.52,2.565),(.008,.030,.012),n=8,lats=4,name=side+' nostril')
        tube(details,[(s*.118,-2.68,2.475),(s*.148,-2.53,2.475),(s*.164,-2.36,2.46),(s*.187,-2.23,2.46),(s*.197,-2.09,2.47)],[.006,.007,.008,.008,.006],6,name=side+' closed lip seam')
    limbs.obj('Long_hindlimbs_and_short_forelimbs',[m['skin']],col)
    feet.obj('Paired_three_toed_hind_feet',[m['skin']],col)
    hands.obj('Paired_complete_hands_with_outer_digits',[m['skin']],col)
    horn.obj('Thumb_spikes_and_blunt_toe_caps',[m['horn']],col)
    details.obj('Eyes_nostrils_and_closed_mouth',[m['eye']],col)
    # Root at the midpoint of the two complete hindfoot contact envelopes.
    for ob in col.all_objects:
        if ob.type=='MESH':
            for v in ob.data.vertices:v.co.y-=.08
    scene=bpy.context.scene
    scene['root_basis']='Floor contact center between paired hind feet'
    scene['scale_basis']='7 m approximate species length; not measurement of holotype R5764'
    scene['reconstruction']='Original complete living reconstruction; inferred skin, colour and balanced bipedal pose'
    scene['source_boundary']='NHM holotype mount 80-90 percent real bones; skull displayed as composite cast from separate preserved bones'
    scene['generator']='source/generate.py';bpy.context.view_layer.update()
    source=audit_source(col,max_triangles=6500)
    if source['errors']:raise RuntimeError(str(source['errors']))
    bpy.context.preferences.filepaths.save_version=0
    for sc in bpy.data.scenes:sc.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'.'*1023;space.params.directory=b'//';space.params.filename=''
    os.chdir(OUT);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'),relative_remap=True)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['mantellisaurus']
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Missing required exporter settings')
    bpy.ops.export_scene.gltf(filepath='model.glb',**opts)
    glb=audit_glb(Path('model.glb'),6500,6,12)
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]};delta=max(abs(glb['bounds_m'][q][i]-expected[q][i]) for q in ['min','max'] for i in range(3))
    if glb['errors'] or delta>.0001 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source/export mismatch')
    write(OUT/'qa/evidence/source-glb.json',{'asset_id':'mantellisaurus','glb_sha256':sha(OUT/'model.glb'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':opts,'blender_version':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'source_dependencies_sha256':sha(HERE/'dependencies.json'),'profile':'palette-only static uncompressed','warnings_reviewed':'All semantic mesh components closed. Deliberate overlaps attach limbs to trunk and toes to feet; visual intersections require image inspection.'})

def render():
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.use_denoising=False
    gray=A.mode=='gray';res=P['render']['resolution_gray' if gray else 'resolution_final'];samples=P['render']['samples_gray' if gray else 'samples_final']
    scene.cycles.samples=samples;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=res;scene.render.resolution_y=res;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    meshes=[o for o in scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices];lo=Vector([min(v[i] for v in points) for i in range(3)]);hi=Vector([max(v[i] for v in points) for i in range(3)]);center=(lo+hi)/2;span=max(hi-lo)
    if gray:
        mat=make_material('clay','#929292')
        for o in meshes:
            o.data.materials.clear();o.data.materials.append(mat)
            for f in o.data.polygons:f.material_index=0
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
    d=bpy.data.cameras.new('evidence_camera');cam=bpy.data.objects.new('evidence_camera',d);scene.collection.objects.link(cam);d.type='ORTHO';d.clip_end=span*30;scene.camera=cam
    dest=OUT/('private/gray' if gray else 'views');dest.mkdir(parents=True,exist_ok=True);records=[]
    for label,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();pr=[inv@p for p in points];xs=[p.x for p in pr];ys=[p.y for p in pr];cam.location+=cam.matrix_world.to_3x3()@Vector(((max(xs)+min(xs))/2,(max(ys)+min(ys))/2,0));d.ortho_scale=max(max(xs)-min(xs),max(ys)-min(ys))*1.16
        path=dest/(label+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);records.append({'view':label,'path':('private/gray/' if gray else 'views/')+path.name,'sha256':sha(path),'direction':direction,'camera_location_m':list(cam.location),'ortho_scale_m':d.ortho_scale,'resolution':[res,res],'samples':samples})
    if not gray:
        (OUT/'preview.png').write_bytes((dest/'perspective.png').read_bytes());write(OUT/'qa/evidence/views.json',{'glb_sha256':sha(OUT/'model.glb'),'source':'Clean import of exact model.glb, not authoring scene','renderer':'Blender '+bpy.app.version_string+' Cycles CPU','generator_sha256':sha(HERE/'generate.py'),'render_config':P['render'],'lighting':'Neutral key/fill area lights, no floor, transparent film','views':records,'preview_reuses':'views/perspective.png','website_contract_equivalence':False})
if A.mode=='build':build()
else:render()
