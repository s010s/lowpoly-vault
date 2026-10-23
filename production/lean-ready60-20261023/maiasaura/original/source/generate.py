# SPDX-License-Identifier: MIT
"""Original deterministic adult Maiasaura reconstruction. Run with Blender -b -P.
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

def loft(mesh,rings,n=16,material=0,name=None,axis='Y',palette=None):
    # rings: (longitudinal position, lateral center, vertical center, width, depth)
    vs=[];fs=[];mids=[]
    for t,c1,c2,r1,r2 in rings:
        for k in range(n):
            a=2*math.pi*k/n
            if axis=='Y':vs.append((c1+r1*math.cos(a),t,c2+r2*math.sin(a)))
            else:vs.append((c1+r1*math.cos(a),c2+r2*math.sin(a),t))
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
    col=setup_scene('maiasaura',P['seed']);m={k:make_material(k,v) for k,v in P['palette'].items()}
    body=Mesh()
    rings=[(-2.35,0,2.23,.19,.24),(-2.15,0,2.23,.26,.31),(-1.94,0,2.23,.32,.37),(-1.70,0,2.22,.43,.48),(-1.42,0,2.17,.55,.62),(-1.05,0,2.12,.66,.76),(-.62,0,2.08,.72,.87),(-.15,0,2.08,.77,.91),(.33,0,2.13,.77,.92),(.72,0,2.18,.70,.85),(1.08,0,2.19,.57,.72),(1.4,0,2.19,.43,.57),(1.75,0,2.18,.34,.44),(2.15,0,2.14,.29,.35),(2.6,0,2.08,.245,.29),(3.05,0,1.99,.20,.235),(3.48,0,1.88,.16,.18),(3.9,0,1.77,.118,.13),(4.3,0,1.67,.084,.095),(4.67,0,1.57,.055,.065),(5.0,0,1.49,.032,.04),(5.3,0,1.43,.017,.021),(5.55,0,1.39,.004,.005)]
    loft(body,rings,20,palette=[0,1,2],name='continuous torso neck and tail');body.object('Torso_neck_and_balancing_tail',[m['skin'],m['ventral'],m['dorsal']],col)
    head=Mesh()
    # Deep cheek and elongated nasal profile, with expanded blunt terminal bill.
    hr=[(-3.45,0,1.97,.17,.105),(-3.39,0,1.98,.27,.13),(-3.25,0,2.02,.31,.16),(-3.10,0,2.05,.275,.185),(-2.92,0,2.10,.23,.23),(-2.73,0,2.15,.225,.28),(-2.55,0,2.21,.27,.34),(-2.36,0,2.25,.30,.355),(-2.20,0,2.26,.25,.31),(-2.07,0,2.25,.14,.20)]
    loft(head,hr,20,name='elongated deep skull');
    for i in range(len(head.mi)):
        if i<1+3*20*2:head.mi[i]=1
    head.object('Long_face_deep_jaw_broad_bill',[m['skin'],m['crest_bill']],col)
    crest=Mesh();vs=[];fs=[]
    # Anterior-facing dish: central surface lies posterior to its low broad rim.
    # A closed semicircular plate grows directly out of the skull roof.
    contour=[(-.36,2.52),(-.34,2.60),(-.28,2.68),(-.18,2.735),(0,2.76),(.18,2.735),(.28,2.68),(.34,2.60),(.36,2.52),(.22,2.515),(0,2.52),(-.22,2.515)]
    vs=[(0,-2.30,2.59)]+[(x,-2.39+.035*abs(x)/.36,z) for x,z in contour]+[(0,-2.23,2.59)]+[(x,-2.29+.035*abs(x)/.36,z) for x,z in contour]
    n=len(contour)
    for k in range(n):
        a=1+k;b=1+(k+1)%n;c=1+n+1+k;d=1+n+1+(k+1)%n
        fs.extend([(0,a,b),(n+1,d,c),(a,c,d,b)])
    crest.add(vs,fs,0,'single broad low concave crest');crest.object('Adult_transverse_concave_crest',[m['crest_bill']],col)
    legs=Mesh();feet=Mesh();horns=Mesh()
    for s,side in [(-1,'left'),(1,'right')]:
        hind=[(2.50,s*.52,.75,.28,.34),(2.22,s*.65,.73,.34,.38),(1.9,s*.69,.48,.32,.35),(1.58,s*.71,.25,.24,.27),(1.35,s*.72,.28,.19,.23),(1.09,s*.73,.55,.15,.17),(.79,s*.74,.80,.13,.14),(.52,s*.74,.92,.115,.13),(.25,s*.74,.84,.13,.18),(.12,s*.74,.74,.17,.27)]
        loft(legs,hind,12,name=side+' hindlimb thigh knee hock',axis='Z')
        front=[(2.30,s*.45,-1.33,.18,.24),(2.04,s*.50,-1.36,.19,.22),(1.75,s*.52,-1.23,.16,.19),(1.48,s*.53,-1.09,.13,.15),(1.25,s*.54,-1.11,.105,.12),(.95,s*.54,-1.24,.095,.115),(.60,s*.54,-1.35,.088,.10),(.30,s*.54,-1.36,.095,.12),(.12,s*.54,-1.37,.12,.15)]
        loft(legs,front,12,name=side+' smaller forelimb elbow wrist',axis='Z')
        # Three short, blunt hind toes; a low sole reaches the floor.
        for digit in [-1,0,1]:
            cx=s*.74+digit*.16;length=.50 if digit==0 else .40
            toe=[(.98, cx, .17,.075,.11),(.76,cx,.13,.095,.13),(.57-length*.45,cx+digit*.035,.10,.095,.10),(.48-length*.5,cx+digit*.06,.075,.075,.075)]
            loft(feet,toe,10,name=side+' pes toe '+str(digit+3))
            ellipsoid(horns,(cx+digit*.06,.45-length*.5,.069),(.075,.09,.069),n=10,lats=4,name=side+' pes hoof '+str(digit+3))
        # The central weight-bearing manus digits form one bound mitten, not claws.
        loft(feet,[(.03,s*.54,-1.39,.135,.16),(.12,s*.54,-1.39,.14,.16),(.24,s*.54,-1.36,.10,.12)],12,axis='Z',name=side+' bound manus')
        ellipsoid(horns,(s*.54,-1.45,.055),(.12,.12,.055),n=10,lats=4,name=side+' manus hoof')
        ellipsoid(feet,(s*.67,-1.31,.17),(.06,.11,.10),n=8,lats=4,name=side+' modest lateral manus digit')
    legs.object('Four_limbs_with_anatomical_joints',[m['skin']],col)
    feet.object('Hind_toes_and_bound_forefeet',[m['skin']],col)
    horns.object('Blunt_hoof_caps',[m['horn']],col)
    details=Mesh()
    for s in [-1,1]:
        ellipsoid(details,(s*.278,-2.49,2.40),(.034,.073,.060),n=12,lats=6,name='lateral orbit')
        ellipsoid(details,(s*.242,-3.12,2.13),(.013,.058,.026),n=10,lats=4,name='reconstructed nostril')
        # A closed, thin lip line defines the deep jaw without an open gape.
        vs=[];fs=[];path=[(-3.42,.19,1.955),(-3.26,.297,1.97),(-3.10,.27,1.99),(-2.92,.225,2.01),(-2.73,.218,2.03),(-2.57,.25,2.05)]
        for y,x,z in path:vs.extend([(s*(x+.008),y,z-.009),(s*(x+.008),y,z+.009),(s*(x-.005),y,z)])
        for k in range(len(path)-1):
            a=k*3;b=(k+1)*3;fs.extend([(a,b,b+1,a+1),(a+1,b+1,b+2,a+2),(a+2,b+2,b,a)])
        fs.extend([(0,1,2),(len(vs)-1,len(vs)-2,len(vs)-3)]);details.add(vs,fs,name='closed mouth seam')
    details.object('Eyes_nostrils_and_closed_mouth',[m['eye']],col)
    # Translate vertex positions, preserving an identity root and positive transforms.
    # Front and hind load contacts center on the origin to within two centimetres.
    for ob in col.all_objects:
        if ob.type=='MESH':
            for vertex in ob.data.vertices:vertex.co.y+=.60
    bpy.context.scene['root_basis']='Floor contact center, at the mean manus/pes support region'
    bpy.context.scene['scale_basis']='9 m taxon estimate, not a measured museum individual'
    bpy.context.scene['reconstruction']='Original adult living reconstruction; soft tissue, colour and posture interpretative'
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
    bpy.context.view_layer.objects.active=bpy.data.objects['maiasaura']
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Required exporter option unavailable')
    bpy.ops.export_scene.gltf(filepath='model.glb',**options)
    glb=audit_glb(Path('model.glb'),6500,6,12)
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][q][i]-expected[q][i]) for q in ['min','max'] for i in range(3))
    if glb['errors'] or delta>.0001 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source to GLB check failed')
    write(OUT/'qa/evidence/source-glb.json',{'asset_id':'maiasaura','glb_sha256':sha(OUT/'model.glb'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':options,'blender_version':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'source_dependencies_sha256':sha(HERE/'dependencies.json'),'profile':'palette-only static uncompressed','warnings_reviewed':'All parts are closed manifold deliberate flat-faceted meshes. Overlap of limbs into trunk and crest into skull is intentional anatomy; source audit does not establish intersection quality.'})

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
