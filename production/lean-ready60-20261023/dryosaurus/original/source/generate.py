# SPDX-License-Identifier: MIT
"""Deterministic original Dryosaurus elderae living reconstruction.
Run: blender -b -t 2 -P source/generate.py -- --out . --mode build
Use --mode gray or final to render a clean import of the exact output GLB.
Only relative source/deps helpers are imported. Reference photos are not embedded.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, _look_at
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
a=argparse.ArgumentParser();a.add_argument('--out',default='.');a.add_argument('--mode',choices=['build','gray','final'],default='build')
A=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(A.out).resolve();OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
class Mesh:
    def __init__(self):self.v=[];self.f=[];self.mi=[];self.groups=[]
    def add(self,vs,fs,mat=0,name=''):
        off=len(self.v);self.v.extend(vs);self.f.extend(tuple(off+i for i in f) for f in fs);self.mi.extend([mat]*len(fs))
        if name:self.groups.append((name,list(range(off,len(self.v)))))
    def object(self,name,mats,col):
        ob=mesh_object(name,self.v,self.f,mats,col)
        for f,mi in zip(ob.data.polygons,self.mi):f.material_index=mi
        for name,ids in self.groups:ob.vertex_groups.new(name=name).add(ids,1,'REPLACE')
        return ob

def loft(mesh,rings,n=16,mat=0,name='',axis='Y',palette=None):
    # Each ring is (longitudinal coordinate, center1, center2, radius1, radius2).
    vs=[];fs=[];mids=[]
    for t,c1,c2,r1,r2 in rings:
        for k in range(n):
            q=2*math.pi*k/n
            vs.append((c1+r1*math.cos(q),t,c2+r2*math.sin(q)) if axis=='Y' else (c1+r1*math.cos(q),c2+r2*math.sin(q),t))
    fs.append(tuple(range(n-1,-1,-1)));mids.append(mat)
    for j in range(len(rings)-1):
        for k in range(n):
            aa=j*n+k;bb=j*n+(k+1)%n;cc=(j+1)*n+(k+1)%n;dd=(j+1)*n+k
            fs.extend([(aa,bb,cc),(aa,cc,dd)])
            m=mat
            if palette:
                s=math.sin(2*math.pi*(k+.5)/n)
                if s<-.50:m=palette[1]
                elif s>.80:m=palette[2]
            mids.extend([m,m])
    fs.append(tuple((len(rings)-1)*n+k for k in range(n)));mids.append(mat)
    start=len(mesh.f);mesh.add(vs,fs,mat,name);mesh.mi[start:]=mids

def tube(mesh,points,radii,n=8,mat=0,name=''):
    # Parallel-transported local frames give deliberate closed tapered sections.
    ps=[Vector(p) for p in points];vs=[];fs=[];last=None
    for j,p in enumerate(ps):
        t=(ps[min(j+1,len(ps)-1)]-ps[max(j-1,0)]).normalized()
        u=(Vector((1,0,0)) if abs(t.x)<.9 else Vector((0,1,0))) if last is None else last
        u=(u-t*u.dot(t)).normalized();v=t.cross(u).normalized();last=u
        r=radii[j];rx,ry=(r,r) if isinstance(r,(float,int)) else r
        for k in range(n):
            q=2*math.pi*k/n;vs.append(tuple(p+u*(rx*math.cos(q))+v*(ry*math.sin(q))))
    fs.append(tuple(range(n-1,-1,-1)))
    for j in range(len(ps)-1):
        for k in range(n):
            a=j*n+k;b=j*n+(k+1)%n;c=(j+1)*n+(k+1)%n;d=(j+1)*n+k;fs.extend([(a,b,c),(a,c,d)])
    fs.append(tuple((len(ps)-1)*n+k for k in range(n)));mesh.add(vs,fs,mat,name)

def ellipsoid(mesh,c,r,mat=0,n=12,lats=6,name=''):
    vs=[(c[0],c[1],c[2]-r[2])];fs=[]
    for j in range(1,lats):
        phi=-math.pi/2+math.pi*j/lats
        for k in range(n):
            q=2*math.pi*k/n;vs.append((c[0]+r[0]*math.cos(phi)*math.cos(q),c[1]+r[1]*math.cos(phi)*math.sin(q),c[2]+r[2]*math.sin(phi)))
    top=len(vs);vs.append((c[0],c[1],c[2]+r[2]))
    for k in range(n):fs.append((0,1+(k+1)%n,1+k))
    for j in range(lats-2):
        for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;cc=b+n;d=a+n;fs.extend([(a,b,cc),(a,cc,d)])
    for k in range(n):fs.append((top,1+(lats-2)*n+k,1+(lats-2)*n+(k+1)%n))
    mesh.add(vs,fs,mat,name)

def build():
    col=setup_scene('dryosaurus',P['seed']);m={k:make_material(k,v) for k,v in P['palette'].items()}
    body=Mesh()
    # One continuous loft joins long narrow neck, moderately deep chest, hips and tail.
    rings=[(-.89,0,1.318,.039,.048),(-.83,0,1.290,.044,.060),(-.76,0,1.232,.047,.065),(-.68,0,1.150,.053,.073),(-.59,0,1.075,.060,.086),(-.49,0,1.032,.073,.109),(-.40,0,1.012,.106,.143),(-.30,0,.996,.145,.192),(-.17,0,.978,.173,.230),(-.02,0,.966,.186,.249),(.13,0,.968,.178,.244),(.27,0,.979,.152,.214),(.40,0,.993,.117,.164),(.55,.003,1.013,.091,.121),(.72,.012,1.040,.072,.090),(.90,.025,1.067,.055,.069),(1.10,.045,1.090,.040,.048),(1.30,.064,1.108,.029,.032),(1.48,.079,1.118,.019,.022),(1.64,.086,1.119,.012,.014),(1.77,.086,1.112,.007,.008),(1.85,.082,1.100,.0018,.0022)]
    loft(body,rings,20,palette=[0,1,2],name='continuous long neck torso tapering tail')
    body.object('Continuous_neck_torso_balancing_tail',[m['skin'],m['ventral'],m['dorsal']],col)
    head=Mesh()
    # Large posterior orbit and tapering toothless rostrum follow adult skull cast,
    # with artist-reconstructed closed cheeks and keratinous beak.
    hr=[(-1.15,0,1.338,.022,.020),(-1.125,0,1.344,.033,.028),(-1.080,0,1.353,.041,.038),(-1.035,0,1.361,.048,.049),(-.985,0,1.368,.058,.066),(-.935,0,1.372,.071,.081),(-.890,0,1.367,.068,.079),(-.850,0,1.351,.048,.066),(-.829,0,1.331,.029,.039)]
    loft(head,hr,16,name='small tapered herbivore skull')
    for i in range(1+2*16*2):head.mi[i]=1
    head.object('Small_tapered_beaked_head',[m['skin'],m['horn']],col)
    limbs=Mesh();arms=Mesh();digits=Mesh();claws=Mesh()
    for s,side,offset in [(-1,'left',-.030),(1,'right',.030)]:
        # Small muscular proximal thigh, long gracile shin, narrow long metatarsus.
        hind=[(1.075,s*.115,.17,.068,.094),(.990,s*.148,.16,.089,.113),(.865,s*.177,.085,.081,.100),(.735,s*.187,-.020,.060,.071),(.655,s*.189,-.038,.045,.054),(.520,s*.192,.054,.036,.042),(.365,s*.192,.169,.028,.032),(.275,s*.190,.208,.026,.029),(.170,s*.187,.179,.024,.027),(.080,s*.185,.120,.027,.036)]
        hind=[(z,x,y+offset,rx,ry) for z,x,y,rx,ry in hind]
        loft(limbs,hind,12,axis='Z',name=side+' hindlimb femur tibia metatarsus')
        # Forelimbs held entirely clear of ground; wrists face inward, no thumb spike.
        tube(arms,[(s*.105,-.340,1.030),(s*.168,-.352,.967),(s*.192,-.305,.855),(s*.200,-.390,.785),(s*.201,-.465,.748)],[(.043,.049),(.040,.044),(.026,.030),(.020,.024),(.019,.021)],10,name=side+' short bent forelimb')
        # Five short unequal manual digits with a clear small fan, not three theropod claws.
        for j in range(5):
            dx=(j-2)*.012;length=[.050,.076,.088,.074,.052][j]
            root=(s*(.202+dx),-.468,.743)
            mid=(s*(.202+dx*1.7),-.492-length*.28,.719)
            tip=(s*(.202+dx*2.25),-.480-length,.696+abs(j-2)*.005)
            tube(digits,[root,mid,tip],[.008,.007,.0035],7,name=side+' manus digit '+str(j+1))
        # Three long splayed pedal digits. Thin keratin tips, no massive hoof pads.
        for j in [-1,0,1]:
            x=s*.185+j*.027;endx=x+j*.032;end_y=(-.135 if j==0 else -.095)+offset
            pts=[(x,.124+offset,.078),(x+j*.012,.065+offset,.043),(endx,end_y+.045,.028),(endx,end_y,.022)]
            tube(digits,pts,[.018,.020,.016,.010],8,name=side+' pes digit '+str(j+3))
            tube(claws,[(endx,end_y+.012,.023),(endx,end_y-.026,.019),(endx,end_y-.045,.015)],[.012,.009,.0018],7,name=side+' pedal claw '+str(j+3))
        # Reduced elevated hallux behind the inner ankle; not a fourth ground-bearing toe.
        tube(digits,[(s*.164,.124+offset,.105),(s*.146,.166+offset,.080),(s*.138,.189+offset,.066)],[.011,.008,.0035],7,name=side+' reduced elevated hallux')
    limbs.object('Long_light_hindlimbs',[m['skin']],col)
    arms.object('Short_free_forelimbs',[m['skin']],col)
    digits.object('Five_manual_and_three_main_pedal_digits',[m['skin']],col)
    claws.object('Small_pedal_keratin_tips',[m['horn']],col)
    eyes=Mesh();iris=Mesh()
    for s in [-1,1]:
        ellipsoid(iris,(s*.064,-.938,1.403),(.009,.026,.024),n=12,lats=6,name='restrained orbit surround')
        ellipsoid(eyes,(s*.071,-.940,1.404),(.006,.018,.018),n=12,lats=6,name='lateral eye')
        ellipsoid(eyes,(s*.036,-1.089,1.367),(.0035,.008,.0045),n=8,lats=4,name='small rostral nostril')
        mouth=[(s*(rx*math.cos(math.pi/8)+.0003),y,cz-rz*math.sin(math.pi/8)) for y,cx,cz,rx,rz in hr[:6]]
        tube(eyes,mouth,[.0011,.0012,.0012,.0013,.0014,.0012],6,name='closed herbivorous mouth seam')
    eyes.object('Eyes_nostrils_and_closed_mouth',[m['eye']],col)
    iris.object('Subtle_orbit_rings',[m['iris']],col)
    # Lower the feet to the ground and center the actual fore-aft footprint.
    # Vertex shifts preserve a single identity root and all positive object transforms.
    allverts=[v for ob in col.all_objects if ob.type=='MESH' for v in ob.data.vertices]
    dz=-min(v.co.z for v in allverts)
    for v in allverts:v.co.z+=dz;v.co.y-=.005
    scene=bpy.context.scene
    scene['generator']='source/generate.py';scene['scale_basis']='3 m approximate museum display length, not a complete fossil measurement'
    scene['root_basis']='Mean left and right pedal contact region; Z zero at lowest toe surface'
    scene['scientific_limits']='D. elderae living reconstruction. CM3392 mount about 35 percent original bone and 25 percent newly sculpted. NPS adult skull cast reference. Soft tissue, pose and colour interpretative.'
    source=audit_source(col,max_triangles=P['geometry_policy']['max_triangles'])
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
    bpy.context.view_layer.objects.active=bpy.data.objects['dryosaurus']
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Required exporter option unavailable')
    bpy.ops.export_scene.gltf(filepath='model.glb',**options)
    g=P['geometry_policy'];glb=audit_glb(Path('model.glb'),g['max_triangles'],g['max_materials'],g['max_primitives'])
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][q][i]-expected[q][i]) for q in ['min','max'] for i in range(3))
    if glb['errors'] or delta>.0001 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source to GLB check failed: '+str(glb['errors']))
    if (OUT/'model.glb').stat().st_size>g['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    write(OUT/'qa/evidence/source-glb.json',{'asset_id':'dryosaurus','glb_sha256':sha(OUT/'model.glb'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':options,'blender_version':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'source_dependencies_sha256':sha(HERE/'dependencies.json'),'profile':'palette-only static uncompressed','warnings_reviewed':'Closed flat-faceted semantic parts. Limb bases overlap torso intentionally, head overlaps neck, eyes and lips are inset surface details. No source audit can establish anatomy or visual join quality.'})

def render():
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.use_denoising=False
    gray=A.mode=='gray';cfg=P['render'];res=cfg['resolution_gray' if gray else 'resolution_final'];samples=cfg['samples_gray' if gray else 'samples_final']
    scene.cycles.samples=samples;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=res;scene.render.resolution_y=res;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
    meshes=[o for o in scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
    low=Vector([min(v[i] for v in points) for i in range(3)]);high=Vector([max(v[i] for v in points) for i in range(3)]);center=(low+high)/2;span=max(high-low)
    if gray:
        clay=make_material('clay','#929292')
        for ob in meshes:
            ob.data.materials.clear();ob.data.materials.append(clay)
            for f in ob.data.polygons:f.material_index=0
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
    data=bpy.data.cameras.new('evidence_camera');cam=bpy.data.objects.new('evidence_camera',data);scene.collection.objects.link(cam);data.type='ORTHO';data.clip_end=span*30;scene.camera=cam
    dest=OUT/('private/gray' if gray else 'views');dest.mkdir(parents=True,exist_ok=True);records=[]
    for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points];xx=[p.x for p in proj];yy=[p.y for p in proj]
        shift=Vector(((max(xx)+min(xx))/2,(max(yy)+min(yy))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift;data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.16
        path=dest/(name+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
        records.append({'view':name,'path':('private/gray/' if gray else 'views/')+path.name,'sha256':sha(path),'direction':direction,'camera_location_m':list(cam.location),'ortho_scale_m':data.ortho_scale,'resolution':[res,res],'samples':samples})
    if not gray:
        (OUT/'preview.png').write_bytes((dest/'perspective.png').read_bytes())
        write(OUT/'qa/evidence/views.json',{'glb_sha256':sha(OUT/'model.glb'),'source':'Clean import of exact model.glb, not source scene','renderer':'Blender '+bpy.app.version_string+' Cycles CPU','generator_sha256':sha(HERE/'generate.py'),'render_config':cfg,'lighting':'Canonical asset_common key/fill recipe, no stage, transparent film','views':records,'preview_reuses':'views/perspective.png','website_contract_equivalence':False})
if A.mode=='build':build()
else:render()
