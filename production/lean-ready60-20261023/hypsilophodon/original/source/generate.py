# SPDX-License-Identifier: MIT
"""Original Hypsilophodon living reconstruction, Blender 4.3.2, metres.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Runtime input closure: params.json and the declared sibling deps helpers.
"""
from pathlib import Path
import sys,json,math,hashlib,argparse,shutil
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene,make_material,mesh_object,audit_source,render_previews
from qa_glb import audit_glb
S=Path(__file__).resolve().parent
P=json.loads((S/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=S.parent);p.add_argument('--gray',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--render-only',action='store_true')
a=p.parse_args(argv);O=a.out.resolve();O.mkdir(parents=True,exist_ok=True);(O/'qa/evidence').mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
C=setup_scene('hypsilophodon',seed=P['seed'])
M=[make_material(k,v,roughness=.86) for k,v in P['palette_hex'].items()]
parts=[]
def loft(name,stations,n=12,palette=True,material=0):
    """Authored closed ring loft; station x,y,z,lateral radius,vertical radius."""
    vs=[];fs=[];ids=[]
    for i,s in enumerate(stations):
        c=Vector(s[:3]);d=Vector(stations[min(i+1,len(stations)-1)][:3])-Vector(stations[max(0,i-1)][:3]);d.normalize();u=Vector((1,0,0))
        if abs(d.dot(u))>.92:u=Vector((0,1,0))
        u=(u-d*u.dot(d)).normalized();v=u.cross(d).normalized()
        for k in range(n):
            t=2*math.pi*k/n;q=c+u*(s[3]*math.cos(t))+v*(s[4]*math.sin(t));vs.append(tuple(q))
    fs.append(tuple(reversed(range(n))));ids.append(material)
    for i in range(len(stations)-1):
        for k in range(n):
            j=(k+1)%n;f=(i*n+k,i*n+j,(i+1)*n+j,(i+1)*n+k);theta=2*math.pi*(k+.5)/n
            mi=(2 if math.sin(theta)<-.62 else 1 if math.sin(theta)>.70 else 0) if palette else material
            if (i+k)%2:fs.extend([(f[0],f[1],f[3]),(f[1],f[2],f[3])])
            else:fs.extend([(f[0],f[1],f[2]),(f[0],f[2],f[3])])
            ids.extend([mi,mi])
    fs.append(tuple((len(stations)-1)*n+k for k in range(n)));ids.append(material)
    ob=mesh_object(name,vs,fs,M,C)
    for f,mi in zip(ob.data.polygons,ids):f.material_index=mi
    ob['anatomical_part']=name;parts.append(ob);return ob

def tube(name,points,radii,n=8,mat=0,palette=False):
    return loft(name,[(*p,r,r) for p,r in zip(points,radii)],n,palette,mat)

def lens(name,c,rx,ry,rz,mat,n=10):
    x,y,z=c;vs=[(x-rx,y,z),(x+rx,y,z)]
    vs += [(x,y+ry*math.cos(2*math.pi*k/n),z+rz*math.sin(2*math.pi*k/n)) for k in range(n)]
    fs=[]
    for k in range(n):j=(k+1)%n;fs += [(0,2+j,2+k),(1,2+k,2+j)]
    ob=mesh_object(name,vs,fs,M[mat],C);ob['anatomical_part']=name;parts.append(ob);return ob

if not a.render_only:
    # Short neck, compact deep ribcage, broad pelvis, then one continuously tapered tail.
    body=[(0,-.475,.770,.048,.062),(0,-.420,.732,.055,.073),(0,-.360,.688,.070,.087),
    (0,-.295,.658,.108,.128),(0,-.205,.654,.149,.176),(0,-.100,.666,.164,.194),
    (0,.015,.678,.158,.191),(0,.120,.688,.140,.171),(0,.225,.687,.120,.139),
    (0,.325,.683,.097,.108),(0,.450,.675,.076,.084),(0,.590,.663,.057,.063),
    (.005,.745,.646,.043,.047),(.011,.900,.627,.031,.034),(.018,1.055,.611,.021,.023),
    (.025,1.200,.604,.012,.014),(.032,1.335,.610,.002,.003)]
    loft('01_Continuous_ShortNeck_DeepTrunk_Tail',body,14)
    # Revised museum cast guides a deep orbital rear and tapering beaked snout.
    head=[(0,-.676,.771,.026,.030),(0,-.654,.787,.037,.047),(0,-.623,.802,.046,.058),
    (0,-.583,.822,.058,.074),(0,-.539,.833,.068,.083),(0,-.497,.822,.064,.081),
    (0,-.459,.794,.048,.057)]
    loft('02_Small_DeepOrbital_Skull',head,12)
    loft('03_Compact_LowerJaw',[(0,-.666,.747,.025,.016),(0,-.626,.741,.040,.024),(0,-.580,.745,.053,.033),(0,-.531,.764,.061,.040),(0,-.481,.785,.045,.033)],10,False,0)
    loft('04_Short_Keratinous_Beak',[(0,-.690,.769,.008,.019),(0,-.676,.771,.028,.031),(0,-.655,.778,.034,.035)],10,False,3)
    for s,label in ((1,'R'),(-1,'L')):
        # Eyes are large relative to head, not oversized cartoon globes; seated into cheek.
        lens('05_OrbitalRim_'+label,(s*.064,-.532,.852),.009,.031,.032,1)
        lens('06_Eye_'+label,(s*.072,-.533,.853),.006,.023,.024,4)
        lens('07_Iris_'+label,(s*.077,-.534,.853),.003,.014,.016,5)
        lens('08_Pupil_'+label,(s*.0798,-.535,.853),.002,.007,.009,4)
        lens('09_Naris_'+label,(s*.038,-.643,.800),.002,.006,.004,4,8)
        tube('10_Subtle_Lip_'+label,[(s*.028,-.673,.750),(s*.043,-.632,.754),(s*.055,-.584,.762),(s*.061,-.541,.784)],[.002,.0023,.0023,.0018],6,3)
        # Semantics and landmarks retain the short thigh / long shin relation.
        hip=(s*.105,.191,.680);knee=(s*.150,.021,.477);ankle=(s*.155,.181,.132)
        loft('11_Thigh_'+label,[(*hip,.071,.087),(s*.138,.139,.605,.072,.080),(s*.152,.065,.518,.050,.056),(*knee,.034,.038)],10,True)
        loft('12_LongShin_'+label,[(*knee,.032,.036),(s*.155,.069,.391,.027,.029),(s*.157,.127,.278,.020,.022),(*ankle,.018,.022)],10,True)
        loft('13_ElongateMetatarsus_'+label,[(*ankle,.020,.022),(s*.155,.153,.084,.024,.023),(s*.155,.106,.042,.029,.022)],10,False,0)
        # Three major forward toes plus smaller medial digit I; no opposing climbing toe.
        toe_specs=[(-.029,-.110,.014),(.0,-.151,.016),(.030,-.119,.014)]
        for i,(dx,tip_y,r) in enumerate(toe_specs,2):
            x=s*(.155+dx);root=(s*.155,.109,.043);mid=(x,.006,.027);tip=(x+s*dx*.30,tip_y,.018)
            tube('14_PedalDigit_'+label+'_'+str(i),[root,mid,tip],[r*1.1,r,r*.65],8,0)
            tube('15_PedalClaw_'+label+'_'+str(i),[tip,(tip[0],tip_y-.022,.014),(tip[0],tip_y-.034,.008)],[r*.67,r*.48,.0015],7,3)
        tube('16_MedialDigitI_'+label,[(s*.134,.126,.071),(s*.105,.083,.041),(s*.088,.040,.026)],[.011,.009,.005],7,0)
        tube('17_MedialClawI_'+label,[(s*.088,.040,.026),(s*.083,.024,.020),(s*.083,.017,.015)],[.005,.004,.001],6,3)
        # Short, free forelimbs, elbows bent and inward-facing palms.
        loft('18_UpperArm_'+label,[(s*.109,-.285,.672,.033,.044),(s*.151,-.314,.583,.029,.033),(s*.171,-.347,.513,.022,.024)],9,True)
        loft('19_Forearm_'+label,[(s*.171,-.347,.513,.023,.025),(s*.171,-.404,.521,.020,.023),(s*.160,-.463,.511,.017,.020)],9,False,0)
        loft('20_GraspingPalm_'+label,[(s*.160,-.463,.511,.018,.020),(s*.157,-.486,.485,.024,.022),(s*.155,-.492,.468,.024,.014)],9,False,0)
        # Five countable short digits. Thumb is small and unspiked, fifth reduced.
        specs=[(-.029,.042),(-.014,.065),(0,.074),(.014,.059),(.027,.042)]
        for digit,(dx,length) in enumerate(specs,1):
            x=s*(.155+dx);y=-.489;z=.472-abs(dx)*.15
            pts=[(x,y,z),(x-s*.005,y-length*.62,z-.016),(x-s*.009,y-length,z-.036)]
            tube('21_ManualDigit_'+label+'_'+str(digit),pts,[.0069,.0056,.0038],7,0)
            tube('22_ManualTip_'+label+'_'+str(digit),[pts[-1],(pts[-1][0],pts[-1][1]-.005,pts[-1][2]-.007)],[.0038,.0011],6,3)
    # Display scale is the rounded NHM species estimate, not a measured specimen.
    yvals=[v.co.y for ob in parts for v in ob.data.vertices];scale=P['length_target']/(max(yvals)-min(yvals))
    for ob in parts:
        for v in ob.data.vertices:v.co*=scale
    low=min(v.co.z for ob in parts for v in ob.data.vertices)
    foot=[v.co.y for ob in parts if ob.name.startswith(('14_','15_','16_','17_')) for v in ob.data.vertices];yc=(min(foot)+max(foot))/2
    for ob in parts:
        for v in ob.data.vertices:v.co.z-=low;v.co.y-=yc
    source=audit_source(C,P['budgets']['max_triangles'])
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene['reconstruction_notes']='Original living reconstruction. NHM approximately 2 m is display scale, not a measured individual. Museum mount and revised 2024 bronze cast are composite reconstructions, accession unverified. Skin, palette and pose inferred.'
    bpy.context.scene['asset_author']='Leon Made This / s010s';bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//'
    bpy.ops.wm.save_as_mainfile(filepath=str(O/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in parts:ob.select_set(True)
    bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();joined=bpy.context.view_layer.objects.active;joined.name='Hypsilophodon_Export_PaletteGroups'
    root=bpy.data.objects[C['asset_root']];root.select_set(True)
    options=dict(filepath=str(O/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties};missing=set(options)-available
    if missing:raise RuntimeError('Unsupported exporter flags '+repr(missing))
    bpy.ops.export_scene.gltf(**options)
    g=audit_glb(O/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives']);g['file']='model.glb'
    if g['errors']:raise RuntimeError(g['errors'])
    if g['bytes']>P['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(g['bounds_m'][s][i]-expected[s][i]) for s in ('min','max') for i in range(3))
    if delta>1e-4 or source['triangles']!=g['scene_triangles']:raise RuntimeError('Source/export metric mismatch')
    save('qa/evidence/source-geometry.json',source);save('qa/evidence/glb-audit.json',g)
    save('qa/evidence/build.json',{'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'generator_sha256':sha(__file__),'params_sha256':sha(S/'params.json'),'glb_sha256':sha(O/'model.glb'),'blend_sha256':sha(O/'model.blend'),'seed':P['seed'],'export_options':{k:v for k,v in options.items() if k!='filepath'},'source_to_export_bound_max_error_m':delta,'source_semantic_parts':len(source['parts']),'export_primitives':g['scene_primitives_estimated_base_draw_calls'],'three_version_target':'0.180.0','anatomy':{'manual_digits_each_side':5,'pedal_digits_each_side':4,'thigh_landmark_length_m':(Vector(hip)-Vector(knee)).length*scale,'shin_landmark_length_m':(Vector(knee)-Vector(ankle)).length*scale,'shin_thigh_ratio':(Vector(knee)-Vector(ankle)).length/(Vector(hip)-Vector(knee)).length,'trunk_max_depth_m':.388*scale,'neck_path_landmark_length_m':.190*scale,'approximate_total_length_m':2.0,'uniform_scale_factor':scale,'ground_adjustment_m':-low,'footprint_center_y_adjustment_m':-yc},'limits':'Measured source/export geometry and original landmark parameters only, not independent anatomical acceptance or union watertightness.'})
if a.gray or a.render:
    # Clean import of the delivered GLB is the only source of inspection pixels.
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(O/'model.glb'))
    c=bpy.data.collections.new('EXACT_GLB');bpy.context.scene.collection.children.link(c)
    for ob in list(bpy.context.scene.objects):
        for old in list(ob.users_collection):old.objects.unlink(ob)
        c.objects.link(ob)
    if a.gray:
        clay=make_material('_Gray_Shape_Check','#929292',roughness=.9);bpy.context.view_layer.material_override=clay
        path=O/'private/gray';path.mkdir(parents=True,exist_ok=True)
        rendered=render_previews(c,path,('front','side','top','hero'),resolution=480,samples=8)
        save('private/gray/evidence.json',{'status':'RENDERED_PENDING_MAKER_INSPECTION','glb_sha256':sha(O/'model.glb'),'views':{Path(x).name:sha(x) for x in rendered},'engine':'Cycles CPU','samples':8,'resolution':480,'threads':2})
    if a.render:
        bpy.context.view_layer.material_override=None
        path=O/'private/final-render';path.mkdir(parents=True,exist_ok=True)
        rendered=render_previews(c,path,('front','side','top','hero'),resolution=1024,samples=64,transparent=True)
        (O/'views').mkdir(exist_ok=True);dest={v:('preview.png' if v=='hero' else 'views/'+v+'.png') for v in ('front','side','top','hero')}
        for v,rel in dest.items():shutil.copyfile(path/f'preview-{v}.png',O/rel)
        shutil.copyfile(O/'preview.png',O/'views/perspective.png')
        save('qa/evidence/exact-glb-views.json',{'status':'RENDERED_PENDING_MAKER_INSPECTION','glb_sha256':sha(O/'model.glb'),'source_unchanged':True,'frames':{rel:sha(O/rel) for rel in list(dest.values())+['views/perspective.png']},'engine':'Cycles CPU','resolution':1024,'samples':64,'threads':2,'transparent':True,'view_transform':'Standard','look':'None','camera_directions':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},'camera_note':'Orthographic diagnostic views and oblique front-right hero. Perspective is a layout role, not projection. Hero is reused byte-identically. Not a website-contract render or GPU evidence.'})
print(json.dumps({'status':'MADE_NOT_INDEPENDENTLY_ACCEPTED','glb_sha256':sha(O/'model.glb')}))
