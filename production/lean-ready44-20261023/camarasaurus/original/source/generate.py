# SPDX-License-Identifier: MIT
"""Original deterministic adult Camarasaurus reconstruction. Run with Blender -b -P.
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

def loft(mesh,rings,n=16,material=0,name=None,axis='Y',palette=None,power=1.0):
    # rings: (longitudinal position, lateral center, vertical center, width, depth)
    vs=[];fs=[];mids=[]
    for t,c1,c2,r1,r2 in rings:
        for k in range(n):
            a=2*math.pi*k/n;cx=math.copysign(abs(math.cos(a))**power,math.cos(a));sz=math.copysign(abs(math.sin(a))**power,math.sin(a))
            if axis=='Y':vs.append((c1+r1*cx,t,c2+r2*sz))
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
    col=setup_scene('camarasaurus',P['seed']);m={k:make_material(k,v) for k,v in P['palette'].items()}
    body=Mesh()
    # Continuous stout neck, broad barrel torso and slowly tapering complete tail.
    # Shoulder and hip dorsum differ by only 0.1 m, not a brachiosaur shoulder tower.
    rings=[(-5.83,0,4.96,.20,.22),(-5.65,0,4.95,.26,.28),(-5.28,0,4.85,.31,.34),(-4.86,0,4.72,.36,.39),(-4.40,0,4.57,.41,.45),(-3.94,0,4.42,.46,.51),(-3.47,0,4.23,.52,.58),(-3.02,0,4.02,.58,.65),(-2.62,0,3.80,.65,.73),(-2.25,0,3.57,.75,.83),(-1.91,0,3.34,.90,.96),(-1.52,0,3.13,1.03,1.10),(-1.20,0,3.05,1.13,1.15),(-.75,0,3.00,1.25,1.24),(-.25,0,2.97,1.31,1.30),(.25,0,2.99,1.32,1.33),(.75,0,3.03,1.26,1.31),(1.20,0,3.06,1.16,1.26),(1.55,0,3.05,1.02,1.25),(1.91,0,3.03,.82,1.10),(2.25,0,3.00,.65,.87),(2.64,0,2.95,.54,.68),(3.06,0,2.87,.45,.54),(3.51,0,2.76,.37,.43),(4.00,0,2.63,.30,.34),(4.52,0,2.49,.25,.28),(5.06,0,2.35,.205,.22),(5.61,0,2.20,.164,.17),(6.14,0,2.05,.128,.13),(6.66,0,1.91,.095,.10),(7.15,0,1.78,.066,.071),(7.60,0,1.66,.043,.049),(8.00,0,1.56,.023,.027),(8.30,0,1.49,.006,.008)]
    loft(body,rings,20,palette=[0,1,2],name='continuous compact neck barrel body and complete tail')
    body.object('Stout_neck_barrel_torso_tapered_tail',[m['skin'],m['ventral'],m['dorsal']],col)
    head=Mesh()
    # Adult CM12020 informs deep box proportions and domed roof, not bone openings.
    # Superellipse sections make a short rounded-square muzzle rather than a beak.
    hr=[(-6.70,0,5.02,.235,.285),(-6.63,0,5.05,.31,.34),(-6.44,0,5.08,.355,.375),(-6.22,0,5.10,.365,.41),(-6.02,0,5.105,.34,.435),(-5.82,0,5.08,.29,.375),(-5.64,0,5.02,.22,.255)]
    loft(head,hr,16,name='short deep round boxed adult skull',power=.62)
    head.object('Short_boxy_blunt_head',[m['skin']],col)
    legs=Mesh();feet=Mesh();horns=Mesh()
    # Deliberate stance has short, almost columnar forelegs and slightly taller
    # hindlegs. Feet remain close to the body, not a wide reptilian sprawl.
    for s,side in [(-1,'left'),(1,'right')]:
        fore=[(3.33,s*.77,-1.28,.45,.53),(2.95,s*.91,-1.29,.43,.48),(2.51,s*.94,-1.23,.35,.40),(2.10,s*.95,-1.16,.29,.34),(1.72,s*.94,-1.20,.265,.30),(1.22,s*.94,-1.32,.25,.28),(.72,s*.94,-1.40,.25,.29),(.34,s*.94,-1.42,.29,.34),(.16,s*.94,-1.42,.32,.37)]
        hind=[(3.58,s*.75,1.47,.51,.63),(3.16,s*.92,1.51,.51,.59),(2.72,s*1.00,1.46,.43,.50),(2.28,s*1.04,1.33,.35,.41),(1.89,s*1.04,1.31,.30,.35),(1.48,s*1.05,1.46,.28,.32),(1.01,s*1.04,1.59,.27,.31),(.57,s*1.04,1.56,.28,.33),(.24,s*1.04,1.49,.34,.42)]
        loft(legs,fore,14,name=side+' forelimb shoulder elbow wrist',axis='Z')
        loft(legs,hind,14,name=side+' hindlimb hip knee ankle',axis='Z')
        # Fleshy sauropod soles. Flat zero-height rings make four genuine contacts.
        loft(feet,[(0,s*.94,-1.47,.34,.40),(.12,s*.94,-1.47,.37,.43),(.28,s*.94,-1.45,.35,.40),(.48,s*.94,-1.42,.27,.32)],14,name=side+' horseshoe manus',axis='Z')
        loft(feet,[(0,s*1.04,1.40,.41,.54),(.12,s*1.04,1.40,.44,.56),(.30,s*1.04,1.43,.40,.50),(.48,s*1.04,1.48,.29,.36)],14,name=side+' broad weight bearing pes',axis='Z')
        # Three modest inner pes unguals, not a row of horse hooves. The other
        # toes are flesh-covered. A single medial thumb claw per forefoot.
        for i in range(3):
            x=s*(.79+i*.17);y=.98+(.035 if i==2 else 0);z=.13
            ellipsoid(horns,(x,y,z),(.095,.18,.105),n=10,lats=4,name=side+' pes ungual '+str(i+1))
        ellipsoid(horns,(s*.68,-1.66,.17),(.12,.20,.11),n=10,lats=4,name=side+' medial manus claw')
    legs.object('Four_columnar_load_bearing_limbs',[m['skin']],col)
    feet.object('Four_grounded_fleshy_feet',[m['skin']],col)
    horns.object('Restricted_inner_toe_and_thumb_claws',[m['horn']],col)
    details=Mesh()
    for s,side in [(-1,'left'),(1,'right')]:
        ellipsoid(details,(s*.337,-5.995,5.27),(.028,.072,.067),n=12,lats=6,name=side+' lateral eye')
        # Soft tissue nares reconstructed on the snout rather than filling the
        # much larger bony nasal openings. Position is explicitly interpretative.
        ellipsoid(details,(s*.304,-6.54,5.22),(.017,.051,.029),n=10,lats=4,name=side+' inferred rostral nostril')
        path=[(-6.66,.267,4.92),(-6.50,.335,4.92),(-6.30,.354,4.92),(-6.10,.34,4.94),(-5.94,.308,4.96)]
        vs=[];fs=[]
        for y,x,z in path:vs.extend([(s*(x+.007),y,z-.010),(s*(x+.007),y,z+.010),(s*(x-.007),y,z)])
        for k in range(len(path)-1):
            a=k*3;b=(k+1)*3;fs.extend([(a,b,b+1,a+1),(a+1,b+1,b+2,a+2),(a+2,b+2,b,a)])
        fs.extend([(0,1,2),(len(vs)-1,len(vs)-2,len(vs)-3)])
        details.add(vs,fs,name=side+' closed level mouth seam')
    details.object('Eyes_rostral_nares_closed_lips',[m['eye']],col)
    bpy.context.view_layer.update()
    bpy.context.scene['root_basis']='Floor contact center, at the mean manus/pes support region'
    bpy.context.scene['scale_basis']='15 m genus estimate, not a measured museum individual'
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
    bpy.context.view_layer.objects.active=bpy.data.objects['camarasaurus']
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Required exporter option unavailable')
    bpy.ops.export_scene.gltf(filepath='model.glb',**options)
    glb=audit_glb(Path('model.glb'),6500,6,12)
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][q][i]-expected[q][i]) for q in ['min','max'] for i in range(3))
    if glb['errors'] or delta>.0001 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source to GLB check failed')
    write(OUT/'qa/evidence/source-glb.json',{'asset_id':'camarasaurus','glb_sha256':sha(OUT/'model.glb'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':options,'blender_version':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'source_dependencies_sha256':sha(HERE/'dependencies.json'),'profile':'palette-only static uncompressed','warnings_reviewed':'All parts are closed manifold deliberate flat-faceted meshes. Overlap of proximal limbs into trunk, feet into limbs, and head into neck is intentional anatomy; source audit does not establish intersection quality.'})

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
