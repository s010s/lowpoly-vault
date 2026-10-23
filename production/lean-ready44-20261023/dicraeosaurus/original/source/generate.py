# SPDX-License-Identifier: MIT
"""Original deterministic complete Dicraeosaurus reconstruction. Run with Blender -b -P.
Examples: blender -b -t 2 -P source/generate.py -- --out . --mode build
Modes: build exports source and GLB; gray/final render a clean import of model.glb.
All model dependencies are contained in source/deps. No source image is embedded.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, _look_at, srgb_to_linear
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=argparse.ArgumentParser();args.add_argument('--out',default='.');args.add_argument('--mode',choices=['build','gray','final'],default='build')
A=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(A.out).resolve();OUT.mkdir(parents=True,exist_ok=True)
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
class Mesh:
    def __init__(self):self.v=[];self.f=[];self.mi=[];self.groups=[]
    def add(self,vs,fs,material=0,name=None):
        n=len(self.v);self.v.extend(vs);self.f.extend(tuple(n+i for i in f) for f in fs);self.mi.extend([material]*len(fs))
        if name:self.groups.append((name,list(range(n,len(self.v)))))
    def object(self,name,mats,col):
        o=mesh_object(name,self.v,self.f,mats,col)
        for f,m in zip(o.data.polygons,self.mi):f.material_index=m
        for gn,indices in self.groups:o.vertex_groups.new(name=gn).add(indices,1,'REPLACE')
        return o

def loft(mesh,rings,n=16,material=0,name=None,axis='Y',palette=None,power=1.0,ridge=None):
    # rings: (longitudinal position, lateral center, vertical center, width, depth)
    vs=[];fs=[];mids=[]
    for ring_index,(t,c1,c2,r1,r2) in enumerate(rings):
        for k in range(n):
            a=2*math.pi*k/n;cx=math.copysign(abs(math.cos(a))**power,math.cos(a));sz=math.copysign(abs(math.sin(a))**power,math.sin(a))
            if axis=='Y':
                relief=0.0
                if ridge and sz>0:
                    relief=ridge[ring_index]*(math.exp(-((a-math.pi/3)/.22)**2)+math.exp(-((a-2*math.pi/3)/.22)**2))
                vs.append((c1+r1*cx,t,c2+r2*sz+relief))
            else:vs.append((c1+r1*cx,c2+r2*sz,t))
    fs.append(tuple(range(n-1,-1,-1)));mids.append(material)
    for j in range(len(rings)-1):
        for k in range(n):
            aa=j*n+k;bb=j*n+(k+1)%n;cc=(j+1)*n+(k+1)%n;dd=(j+1)*n+k
            # deliberate triangulated facets, independent from Blender tessellation
            fs.extend([(aa,bb,cc),(aa,cc,dd)])
            mi=material
            if palette:
                s=math.sin(2*math.pi*(k+.5)/n)
                if s<-.42:mi=palette[1]
                elif s>.72:mi=palette[2]
            mids.extend([mi,mi])
    fs.append(tuple((len(rings)-1)*n+k for k in range(n)));mids.append(material)
    offset=len(mesh.f);mesh.add(vs,fs,material,name);mesh.mi[offset:]=mids

def ellipsoid(mesh,center,radii,material=0,n=12,lats=6,name=None):
    vs=[(center[0],center[1],center[2]-radii[2])];fs=[]
    for j in range(1,lats):
        phi=-math.pi/2+math.pi*j/lats
        for k in range(n):
            a=2*math.pi*k/n;vs.append((center[0]+radii[0]*math.cos(phi)*math.cos(a),center[1]+radii[1]*math.cos(phi)*math.sin(a),center[2]+radii[2]*math.sin(phi)))
    top=len(vs);vs.append((center[0],center[1],center[2]+radii[2]))
    for k in range(n):fs.append((0,1+(k+1)%n,1+k))
    for j in range(lats-2):
        for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;c=b+n;d=a+n;fs.extend([(a,b,c),(a,c,d)])
    for k in range(n):fs.append((top,1+(lats-2)*n+k,1+(lats-2)*n+(k+1)%n))
    mesh.add(vs,fs,material,name)

def build():
    col=setup_scene('dicraeosaurus',P['seed']);m={k:make_material(k,v) for k,v in P['palette'].items()}
    body=Mesh()
    # A single continuous loft supplies the short neck, deep trunk and complete
    # long tail. The survey showcase gap is deliberately not modeled as anatomy.
    rings=[(-3.82,0,2.04,.16,.19),(-3.58,0,2.10,.185,.21),(-3.30,0,2.15,.21,.23),(-3.00,0,2.18,.24,.26),(-2.70,0,2.19,.28,.29),(-2.40,0,2.18,.33,.33),(-2.12,0,2.17,.40,.38),(-1.86,0,2.14,.49,.47),(-1.62,0,2.07,.61,.60),(-1.38,0,2.01,.73,.71),(-1.08,0,1.98,.83,.80),(-.72,0,2.00,.93,.87),(-.34,0,2.05,.99,.92),(.08,0,2.10,1.01,.94),(.50,0,2.16,.99,.95),(.89,0,2.21,.94,.92),(1.22,0,2.24,.84,.86),(1.52,0,2.25,.70,.75),(1.82,0,2.23,.57,.61),(2.15,0,2.18,.47,.49),(2.52,0,2.10,.385,.39),(2.92,0,2.00,.32,.32),(3.34,0,1.89,.267,.266),(3.79,0,1.78,.22,.22),(4.26,0,1.66,.179,.18),(4.73,0,1.54,.145,.145),(5.19,0,1.42,.116,.116),(5.65,.01,1.31,.091,.093),(6.10,.03,1.20,.070,.073),(6.54,.06,1.10,.053,.057),(6.96,.10,1.01,.039,.043),(7.36,.15,.94,.028,.032),(7.73,.22,.89,.019,.023),(8.06,.30,.86,.012,.016),(8.34,.39,.85,.007,.009),(8.60,.48,.85,.0025,.0035)]
    # These paired rounded ridges are inferred flesh over bifid neural spines.
    # They are integrated into the skin, not exposed bone or tall horn sheaths.
    relief=[0,.03,.09,.16,.23,.29,.33,.36,.38,.40,.39,.36,.32,.27,.21,.16,.11,.06,.02]+[0]*17
    loft(body,rings,24,palette=[0,1,2],name='continuous short neck deep torso and full long tail',ridge=relief)
    body.object('Short_neck_paired_flesh_ridges_trunk_complete_tail',[m['skin'],m['ventral'],m['dorsal']],col)
    head=Mesh()
    # A modest elongate blunt head; its tilt is interpretative, and the mounted
    # head is a cast. No empty eye or nasal bone windows on the living skin.
    hr=[(-4.40,0,1.68,.125,.145),(-4.34,0,1.70,.17,.175),(-4.17,0,1.77,.19,.19),(-3.99,0,1.86,.20,.21),(-3.82,0,1.98,.19,.225),(-3.67,0,2.04,.155,.20),(-3.56,0,2.06,.12,.145)]
    loft(head,hr,16,name='small elongated blunt head cast informed',power=.80)
    head.object('Small_elongate_blunt_head',[m['skin']],col)
    legs=Mesh();feet=Mesh();horns=Mesh()
    # Forelimbs are distinctly shorter than hindlimbs; the shoulder is lower
    # than the hip. The stance is weight-bearing, not splayed or brachiosaur-like.
    for s,side in [(-1,'left'),(1,'right')]:
        fore=[(2.27,s*.55,-1.22,.35,.39),(1.98,s*.68,-1.21,.33,.35),(1.65,s*.72,-1.14,.27,.29),(1.35,s*.73,-1.10,.22,.24),(1.05,s*.73,-1.16,.20,.22),(.72,s*.73,-1.25,.19,.22),(.39,s*.73,-1.29,.22,.25),(.16,s*.73,-1.29,.26,.29)]
        hind=[(2.82,s*.55,1.12,.43,.52),(2.44,s*.71,1.17,.41,.47),(2.08,s*.79,1.11,.34,.39),(1.75,s*.83,.99,.28,.32),(1.42,s*.84,.98,.23,.27),(1.08,s*.84,1.11,.22,.25),(.73,s*.84,1.23,.21,.25),(.39,s*.84,1.22,.24,.29),(.17,s*.84,1.18,.29,.36)]
        loft(legs,fore,14,name=side+' shorter forelimb shoulder elbow wrist',axis='Z')
        loft(legs,hind,14,name=side+' longer hindlimb hip knee ankle',axis='Z')
        loft(feet,[(0,s*.73,-1.32,.28,.33),(.11,s*.73,-1.32,.30,.35),(.25,s*.73,-1.31,.28,.32),(.40,s*.73,-1.28,.21,.25)],14,name=side+' grounded manus',axis='Z')
        loft(feet,[(0,s*.84,1.10,.33,.43),(.11,s*.84,1.10,.36,.46),(.27,s*.84,1.13,.33,.41),(.42,s*.84,1.18,.24,.30)],14,name=side+' grounded pes',axis='Z')
        for i in range(3):
            ellipsoid(horns,(s*(.64+i*.145),.75+(.02 if i==2 else 0),.115),(.078,.145,.09),n=10,lats=4,name=side+' pes ungual '+str(i+1))
        ellipsoid(horns,(s*.52,-1.49,.14),(.09,.155,.085),n=10,lats=4,name=side+' medial manus claw')
    legs.object('Four_pillar_limbs_hind_pair_longer',[m['skin']],col)
    feet.object('Four_grounded_fleshy_feet',[m['skin']],col)
    horns.object('Restricted_inner_toe_and_thumb_claws',[m['horn']],col)
    details=Mesh()
    for s,side in [(-1,'left'),(1,'right')]:
        ellipsoid(details,(s*.183,-3.82,2.065),(.022,.052,.047),n=12,lats=6,name=side+' lateral eye')
        ellipsoid(details,(s*.170,-4.28,1.785),(.014,.032,.022),n=10,lats=4,name=side+' inferred rostral naris')
        path=[(-4.36,.154,1.64),(-4.20,.183,1.68),(-4.03,.193,1.75),(-3.88,.184,1.82),(-3.77,.169,1.88)]
        vs=[];fs=[]
        for y,x,z in path:vs.extend([(s*(x+.004),y,z-.007),(s*(x+.004),y,z+.007),(s*(x-.005),y,z)])
        for k in range(len(path)-1):
            a=k*3;b=(k+1)*3;fs.extend([(a,b,b+1,a+1),(a+1,b+1,b+2,a+2),(a+2,b+2,b,a)])
        fs.extend([(0,1,2),(len(vs)-1,len(vs)-2,len(vs)-3)])
        details.add(vs,fs,name=side+' closed mouth seam')
    details.object('Eyes_rostral_nares_and_closed_lips',[m['eye']],col)
    bpy.context.view_layer.update()
    bpy.context.scene['root_basis']='Floor contact center, at the mean manus/pes support region'
    bpy.context.scene['scale_basis']='13 m historical mounted horizontal length reference, not curved live axial length'
    bpy.context.scene['reconstruction']='Original complete living reconstruction; cast head, restored mount, paired ridge soft tissue, colour and posture interpretative'
    bpy.context.scene['generator']='source/generate.py'
    bpy.context.view_layer.update()
    source=audit_source(col,max_triangles=6500)
    if source['errors']:raise RuntimeError(str(source['errors']))
    bpy.context.preferences.filepaths.save_version=0
    # Replace inherited authoring UI destinations before serialization.
    for sc in bpy.data.scenes:sc.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'.'*1023
                    space.params.directory=b'//'
                    space.params.filename=''
    os.chdir(OUT)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'),relative_remap=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['dicraeosaurus']
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Required exporter option unavailable')
    bpy.ops.export_scene.gltf(filepath='model.glb',**options)
    glb=audit_glb(Path('model.glb'),6500,6,12)
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][q][i]-expected[q][i]) for q in ['min','max'] for i in range(3))
    if glb['errors'] or delta>.0001 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source to GLB check failed')
    write(OUT/'qa/evidence/source-glb.json',{'asset_id':'dicraeosaurus','glb_sha256':sha(OUT/'model.glb'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':options,'blender_version':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'source_dependencies_sha256':sha(HERE/'dependencies.json'),'profile':'palette-only static uncompressed','warnings_reviewed':'All parts are closed manifold deliberate flat-faceted meshes. Overlap of proximal limbs into trunk, feet into limbs, and head into neck is intentional anatomy; source audit does not establish intersection quality.'})

def render():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.use_denoising=False
    gray=A.mode=='gray';res=P['render']['resolution_gray' if gray else 'resolution_final'];samples=P['render']['samples_gray' if gray else 'samples_final']
    scene.cycles.samples=samples;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=res;scene.render.resolution_y=res;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    meshes=[o for o in scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
    lo=Vector([min(v[i] for v in points) for i in range(3)]);hi=Vector([max(v[i] for v in points) for i in range(3)]);center=(lo+hi)/2;span=max(hi-lo)
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
        vec=Vector(direction).normalized();cam.location=center+vec*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points]
        x=[p.x for p in proj];y=[p.y for p in proj];shift=Vector(((max(x)+min(x))/2,(max(y)+min(y))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift;d.ortho_scale=max(max(x)-min(x),max(y)-min(y))*1.16
        path=dest/(label+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
        records.append({'view':label,'path':('private/gray/' if gray else 'views/')+path.name,'sha256':sha(path),'direction':direction,'camera_location_m':list(cam.location),'ortho_scale_m':d.ortho_scale,'resolution':[res,res],'samples':samples})
    if not gray:
        (OUT/'preview.png').write_bytes((dest/'perspective.png').read_bytes())
        write(OUT/'qa/evidence/views.json',{'glb_sha256':sha(OUT/'model.glb'),'source':'clean import of exact model.glb, not authoring scene','renderer':'Blender '+bpy.app.version_string+' Cycles CPU','generator_sha256':sha(HERE/'generate.py'),'render_config':P['render'],'lighting':'Canonical asset_common key/fill recipe, no floor and transparent film','views':records,'preview_reuses':'views/perspective.png','website_contract_equivalence':False})
if A.mode=='build':build()
else:render()
