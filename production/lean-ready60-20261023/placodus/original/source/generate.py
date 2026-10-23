# SPDX-License-Identifier: MIT
"""Original Placodus gigas living reconstruction, deterministic Blender 4.3.2.
Run: blender -b -t 2 --python source/generate.py -- --output DIR [--gray | --no-render]
Only packaged source dependencies are read. All authoring dimensions are metres.
"""
from pathlib import Path
import argparse, sys, json, math, hashlib, shutil
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source, render_previews
from qa_glb import audit_glb
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(); p.add_argument('--output',default=str(HERE.parent)); p.add_argument('--gray',action='store_true'); p.add_argument('--no-render',action='store_true'); a=p.parse_args(args)
OUT=Path(a.output).resolve(); OUT.mkdir(parents=True,exist_ok=True)
P=json.loads((HERE/'params.json').read_text()); col=setup_scene('placodus',P['seed']); root=bpy.data.objects['placodus']
root['authoring_forward']='+X'; root['representation']='Living reconstruction, not a fossil scan'; root['mount_origin']=P['mount_origin']
M={k:make_material(k,v,roughness=.85 if k!='eyes' else .28) for k,v in P['palette'].items()}
class Part:
    def __init__(self,name,mats): self.name=name; self.mats=mats; self.v=[]; self.f=[]; self.mi=[]
    def face(self,f,m=0): self.f.append(tuple(f)); self.mi.append(m)
    def loft(self,rings,n=20,mat_fn=None):
        off=len(self.v)
        for x,y,z,w,h in rings:
            for j in range(n):
                t=2*math.pi*j/n; self.v.append((x,y+w*math.cos(t),z+h*math.sin(t)))
        for i in range(len(rings)-1):
            for j in range(n):
                m=mat_fn(i,j,(j+.5)*2*math.pi/n) if mat_fn else 0
                v0=off+i*n+j; v1=off+i*n+(j+1)%n; v2=off+(i+1)*n+(j+1)%n; v3=off+(i+1)*n+j
                if (i+j)%2:self.face((v0,v1,v3),m);self.face((v1,v2,v3),m)
                else:self.face((v0,v1,v2),m);self.face((v0,v2,v3),m)
        self.face(tuple(off+j for j in reversed(range(n))))
        self.face(tuple(off+(len(rings)-1)*n+j for j in range(n)))
    def tube(self,points,radii,n=10):
        off=len(self.v); pts=[Vector(x) for x in points]
        for i,c in enumerate(pts):
            d=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
            reference=Vector((1,0,0)) if abs(d.z)>.95 else Vector((0,0,1))
            u=d.cross(reference).normalized(); v=d.cross(u).normalized()
            for j in range(n):
                t=2*math.pi*j/n;r=radii[i];self.v.append(tuple(c+u*(math.cos(t)*r[0])+v*(math.sin(t)*r[1])))
        for i in range(len(pts)-1):
            for j in range(n):self.face((off+i*n+j,off+i*n+(j+1)%n,off+(i+1)*n+(j+1)%n,off+(i+1)*n+j))
        self.face(tuple(off+j for j in reversed(range(n))))
        self.face(tuple(off+(len(pts)-1)*n+j for j in range(n)))
    def ellipsoid(self,c,r,n=12,rings=6):
        off=len(self.v);self.v.append((c[0],c[1],c[2]-r[2]))
        for i in range(1,rings):
            t=-math.pi/2+math.pi*i/rings
            for j in range(n):
                q=2*math.pi*j/n;self.v.append((c[0]+r[0]*math.cos(t)*math.cos(q),c[1]+r[1]*math.cos(t)*math.sin(q),c[2]+r[2]*math.sin(t)))
        top=len(self.v);self.v.append((c[0],c[1],c[2]+r[2]))
        for j in range(n):self.face((off,off+1+(j+1)%n,off+1+j));self.face((top,off+1+(rings-2)*n+j,off+1+(rings-2)*n+(j+1)%n))
        for i in range(rings-2):
            for j in range(n):self.face((off+1+i*n+j,off+1+i*n+(j+1)%n,off+1+(i+1)*n+(j+1)%n,off+1+(i+1)*n+j))
    def chisel(self,base,tip,width,thickness):
        # Short robust crown with a broad flattened cutting edge, not a cone.
        off=len(self.v);b=Vector(base);t=Vector(tip);d=(t-b).normalized();u=Vector((0,1,0));v=d.cross(u).normalized()
        for c,w,h in [(b,width,thickness),(b+(t-b)*.58,width*.91,thickness*.83),(t,width*.80,thickness*.35)]:
            for j in range(8):
                q=2*math.pi*j/8;self.v.append(tuple(c+u*math.cos(q)*w+v*math.sin(q)*h))
        for i in range(2):
            for j in range(8):self.face((off+i*8+j,off+i*8+(j+1)%8,off+(i+1)*8+(j+1)%8,off+(i+1)*8+j))
        self.face(tuple(off+j for j in reversed(range(8))));self.face(tuple(off+16+j for j in range(8)))
    def finish(self,extra=None):
        obj=mesh_object(self.name,self.v,self.f,[M[k] for k in self.mats],col)
        for f,m in zip(obj.data.polygons,self.mi):f.material_index=m
        if extra:
            for k,v in extra.items():obj[k]=v
        return obj
# Continuous axial profile: deep barrel, very short neck, muscular tapering tail.
body=[(-2.0,.12,.38,.003,.004),(-1.88,.115,.385,.012,.016),(-1.73,.10,.39,.025,.034),(-1.56,.077,.40,.040,.052),(-1.39,.052,.41,.060,.072),(-1.20,.028,.425,.085,.096),(-1.02,.012,.44,.112,.124),(-.82,0,.455,.144,.155),(-.62,0,.47,.185,.195),(-.47,0,.49,.226,.245),(-.30,0,.50,.25,.278),(-.10,0,.50,.26,.29),(.10,0,.50,.255,.287),(.28,0,.49,.232,.267),(.43,0,.475,.19,.221),(.56,0,.455,.14,.164),(.65,0,.44,.105,.117),(.74,0,.44,.088,.093),(.84,0,.45,.091,.084),(.88,0,.455,.092,.08)]
part=Part('01_Barrel_neck_tail',['dorsal','flank','ventral']);part.loft(body,24,lambda i,j,t:0 if math.sin(t)>.40 else 2 if math.sin(t)<-.54 else 1);part.finish({'anatomy':'Deep unshielded barrel torso; short neck; tail outline inferred','barrel_depth_m':.58,'barrel_width_m':.52,'estimated_tail_length_m':1.38})
# Fleshed skull with narrow rounded snout, broad cheek and high rear cranium.
head=[(.79,0,.465,.068,.064),(.84,0,.474,.103,.083),(.90,0,.478,.115,.092),(.96,0,.472,.111,.086),(1.02,0,.459,.096,.067),(1.08,0,.449,.083,.050),(1.13,0,.445,.074,.041),(1.155,0,.442,.052,.033)]
part=Part('02_Fleshed_upper_head',['dorsal','flank']);part.loft(head,20,lambda i,j,t:0 if math.sin(t)>.45 else 1);part.finish({'anatomy':'Short robust Placodus skull; no exposed temporal fenestrae'})
# Mandible falls approximately twenty degrees from hinge to chin.
jaw=[(.805,0,.398,.067,.038),(.855,0,.384,.099,.037),(.91,0,.362,.105,.032),(.97,0,.343,.095,.027),(1.03,0,.322,.080,.024),(1.09,0,.302,.065,.023),(1.136,0,.289,.045,.020)]
part=Part('03_Lower_jaw',['flank','ventral']);part.loft(jaw,16,lambda i,j,t:1 if math.sin(t)<-.1 else 0);part.finish({'approximate_gape_degrees':20})
# Dark oral lining only on actual palate and floor, leaving the gape unfilled.
part=Part('04_Oral_lining',['mouth']);part.loft([(.86,0,.400,.083,.008),(.93,0,.398,.092,.009),(1.00,0,.398,.078,.009),(1.07,0,.400,.062,.006),(1.13,0,.407,.041,.005)],16)
part.loft([(.865,0,.415,.078,.006),(.93,0,.388,.084,.007),(1.00,0,.362,.074,.006),(1.065,0,.339,.057,.005),(1.11,0,.322,.038,.004)],16);part.finish()
# Low, round osteoderms form ONE midline row. They are not a carapace.
part=Part('05_Single_low_dorsal_row',['dorsal']);osteoderms=[]
for i,(x,z,w,h) in enumerate([(-.76,.611,.027,.018),(-.65,.647,.034,.020),(-.53,.706,.038,.023),(-.41,.756,.043,.025),(-.29,.782,.046,.026),(-.17,.794,.046,.026),(-.05,.794,.045,.025),(.07,.791,.044,.025),(.19,.777,.042,.025),(.31,.748,.039,.023),(.42,.701,.035,.021),(.52,.641,.031,.018),(.61,.578,.025,.015)]):
    part.ellipsoid((x,0,z),(.052,w,h),12,6);osteoderms.append([x,0,z,w,h])
part.finish({'anatomy':'Thirteen low integrated osteoderm domes in a single midline row, artistic soft-tissue covering','row_count':1,'osteoderm_count':13})
# Stout splayed legs with articulated bends, short five-digit hands and feet.
limbs=[]
for fore,s in [(True,-1),(True,1),(False,-1),(False,1)]:
    kind='fore' if fore else 'hind';side='right' if s<0 else 'left';part=Part('06_'+kind+'limb_'+side,['flank']);f=lambda x,y,z:(x,s*y,z)
    if fore:
        pts=[f(.43,.15,.42),f(.45,.25,.37),f(.48,.33,.31),f(.46,.38,.29),f(.42,.43,.275)];r=[(.080,.070),(.072,.060),(.059,.047),(.045,.035),(.050,.026)]
        outward=Vector((.12,s*.99,0));across=Vector((.99,-s*.12,0));span=.90
    else:
        pts=[f(-.47,.16,.43),f(-.54,.25,.38),f(-.62,.31,.32),f(-.63,.36,.29),f(-.69,.40,.275)];r=[(.085,.071),(.078,.063),(.062,.047),(.048,.034),(.050,.026)]
        outward=Vector((-.58,s*.815,0));across=Vector((.815,s*.58,0));span=.86
    part.tube(pts,r,12);wrist=Vector(pts[-1]);end=wrist+outward*.063
    part.tube([tuple(wrist-outward*.02),tuple(wrist+outward*.028),tuple(end)],[ (.053,.025),(.074,.025),(.075,.019)],12)
    endpoints=[]
    for offset,length in zip([-.058,-.03,0,.03,.058],[.068,.095,.112,.102,.074]):
        base=end+across*offset-outward*.018;d=(outward+across*offset*3.0).normalized();tip=base+d*length*span+Vector((0,0,-.006));mid=base+d*length*span*.55
        part.tube([tuple(base),tuple(mid),tuple(tip-d*.009),tuple(tip)],[ (.014,.014),(.014,.012),(.010,.009),(.006,.006)],8);endpoints.append(list(tip))
    limb_scale=.85; pivot=Vector(pts[0])
    part.v=[tuple(pivot+(Vector(v)-pivot)*limb_scale) for v in part.v]
    endpoints=[list(pivot+(Vector(v)-pivot)*limb_scale) for v in endpoints]
    part.finish({'anatomy':'Short stout bent leg with five digits and inferred partial webbing; no imported historical humerus','digit_count':5,'digit_endpoints_json':json.dumps(endpoints),'limb_class':kind})
    limbs.append({'name':part.name,'digit_count':5,'root_to_longest_tip_m':max((Vector(v)-Vector(pts[0])).length for v in endpoints),'digit_endpoints_blender_m':endpoints})
part=Part('07_Eyes_and_nares',['eyes'])
for s in [-1,1]:
    part.ellipsoid((.956,s*.096,.510),(.017,.011,.014),12,6)
    part.ellipsoid((1.100,s*.036,.488),(.008,.005,.003),8,4)
part.finish()
# Differentiated dentition: 3 upper anterior pairs, 4 marginal pairs and
# 3 paired broad flattened palatine teeth. Only the front group is chisel-like.
part=Part('08_Differentiated_teeth',['teeth']);teeth=[]
for s in [-1,1]:
    for pair,(x,y,z,projection) in enumerate([(1.155,.017,.416,.045),(1.146,.046,.414,.044),(1.128,.072,.412,.040)]):
        base=(x,s*y,z);tip=(x+projection,s*(y+.002),z-.011);part.chisel(base,tip,.0115,.010);teeth.append({'group':'upper_premaxillary','pair':pair+1,'base':list(base),'tip':list(tip)})
    for pair,(x,y) in enumerate([(.905,.098),(.969,.088),(1.028,.075),(1.081,.063)]):
        part.ellipsoid((x,s*y,.397),(.021,.016,.010),12,6);teeth.append({'group':'upper_maxillary','pair':pair+1,'center':[x,s*y,.397]})
    for pair,(x,y,rx,ry) in enumerate([(.915,.036,.032,.029),(.982,.034,.030,.027),(1.045,.029,.027,.023)]):
        part.ellipsoid((x,s*y,.388),(rx,ry,.010),12,6);teeth.append({'group':'palatine','pair':pair+1,'center':[x,s*y,.388],'flat_crown_radii':[rx,ry,.010]})
    # Lower anterior arrangement and lower pavement are conservative reconstructions.
    for x,y,z in [(1.128,.020,.311),(1.112,.048,.314)]:part.chisel((x,s*y,z),(x+.028,s*y,z+.012),.011,.009);teeth.append({'group':'lower_anterior_inferred','base':[x,s*y,z]})
    for x,y,z,rx in [(.925,.060,.395,.028),(.984,.053,.374,.027),(1.040,.041,.354,.024)]:
        part.ellipsoid((x,s*y,z),(rx,.024,.010),12,6);teeth.append({'group':'lower_crushing_inferred','center':[x,s*y,z]})
part.finish({'anatomy':'Short forward chisel crowns before flat posterior crushing pavement; no pointed posterior fangs','upper_premaxillary_count':6,'upper_maxillary_count':8,'palatine_count':6,'lower_anterior_count_inferred':4})
bpy.context.view_layer.update()
if a.gray:
    gray=make_material('gray_diagnostic','#929292',roughness=.86)
    for o in col.objects:
        if o.type=='MESH':
            for i in range(len(o.data.materials)):o.data.materials[i]=gray
    render_previews(col,OUT,views=('front','side','top','hero'),resolution=512,samples=8,transparent=True)
    print('GRAY_READY');raise SystemExit(0)
source=audit_source(col,max_triangles=P['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
source['reviewed_warnings']={'mount':'Swimming reconstruction: lowest Z above zero is intentional; root is torso projection mounting point.'}
source['limbs']=limbs;source['teeth']=teeth;source['osteoderms']=osteoderms;source['nominal_inferred_total_length_m']=3.2
bpy.context.scene['source_generator']='source/generate.py';bpy.context.scene['asset_author']='Leon Made This / s010s';bpy.context.preferences.filepaths.save_version=0
# Keep saved authoring UI paths package-relative, including factory File Browser state.
bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'.'*1023
                space.params.directory=b'//'
                space.params.filename='model.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Unsupported export flags '+str(missing))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
if glb['errors']:raise RuntimeError(glb['errors'])
if glb['bytes']>P['budgets']['max_glb_bytes']:raise RuntimeError('Byte budget exceeded')
b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',emin),('max',emax)] for i in range(3))
if delta>1e-4 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Roundtrip geometry mismatch')
qa=OUT/'qa'/'evidence';qa.mkdir(parents=True,exist_ok=True);glb['file']='model.glb'
record={'asset_id':'placodus','revision':'r001','blender_version':bpy.app.version_string,'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'threejs_gpu':'NOT_RUN','populated_scene':'NOT_RUN'}
(qa/'technical.json').write_text(json.dumps(record,indent=2)+'\n')
if not a.no_render:
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    imported=bpy.data.collections.new('EXACT_GLB');bpy.context.scene.collection.children.link(imported)
    for obj in list(bpy.context.scene.objects):
        for old in list(obj.users_collection):old.objects.unlink(obj)
        imported.objects.link(obj)
    vdir=OUT/'views';render_previews(imported,vdir,views=('front','side','top','hero'),resolution=P['preview']['resolution'],samples=P['preview']['samples'],transparent=True)
    for name in ['front','side','top']:(vdir/f'preview-{name}.png').rename(vdir/f'{name}.png')
    (vdir/'preview-hero.png').rename(vdir/'perspective.png');shutil.copyfile(vdir/'perspective.png',OUT/'preview.png')
    (qa/'preview-provenance.json').write_text(json.dumps({'status':'RENDERED_FROM_CLEAN_IMPORT','glb_sha256':glb['sha256'],'renderer':'Blender Cycles CPU','settings':P['preview'],'cameras':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},'preview_equals_perspective':True,'views':{x:hashlib.sha256((vdir/f'{x}.png').read_bytes()).hexdigest() for x in ['front','side','top','perspective']}},indent=2)+'\n')
print('BUILD_READY '+glb['sha256'])
