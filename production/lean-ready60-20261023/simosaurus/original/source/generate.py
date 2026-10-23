# SPDX-License-Identifier: MIT
"""Deterministic original Simosaurus living reconstruction. Blender 4.3.2.
Run: blender -b -t 2 --python source/generate.py -- --output DIR [--gray | --no-render]
No source-file dependencies outside this source folder. Scientific references are
interpretive inputs, not runtime reads. All profile coordinates are in metres.
"""
from pathlib import Path
import argparse, sys, json, math, hashlib, shutil
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source, render_previews
from qa_glb import audit_glb
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(); p.add_argument('--output',default=str(HERE.parent)); p.add_argument('--gray',action='store_true'); p.add_argument('--no-render',action='store_true'); a=p.parse_args(args)
OUT=Path(a.output).resolve(); OUT.mkdir(parents=True,exist_ok=True)
P=json.loads((HERE/'params.json').read_text()); col=setup_scene('simosaurus',P['seed'])
root=bpy.data.objects['simosaurus']; root['authoring_forward']='+X'; root['representation']='Living reconstruction; inferred soft tissues'; root['mount_origin']=P['mount_origin']
M={k:make_material(k,v,roughness=.84 if k!='eyes' else .3) for k,v in P['palette'].items()}
# Explicit closed sectional surfaces. Append can combine disconnected small
# features into one editable semantic mesh without multiplying draw primitives.
class Part:
    def __init__(self,name,mats): self.name=name; self.mats=mats; self.v=[]; self.f=[]; self.mi=[]
    def face(self,f,m=0): self.f.append(tuple(f)); self.mi.append(m)
    def loft(self,rings,n=16,mat_fn=None):
        # rings: x, y center, z center, y radius, z radius
        off=len(self.v)
        for x,y,z,w,h in rings:
            for j in range(n):
                t=2*math.pi*j/n; self.v.append((x,y+w*math.cos(t),z+h*math.sin(t)))
        for i in range(len(rings)-1):
            for j in range(n):
                m=mat_fn(i,j,(j+.5)*2*math.pi/n) if mat_fn else 0
                v0=off+i*n+j; v1=off+i*n+(j+1)%n; v2=off+(i+1)*n+(j+1)%n; v3=off+(i+1)*n+j
                # Alternate diagonals give deliberate small polygon planes.
                if (i+j)%2: self.face((v0,v1,v3),m); self.face((v1,v2,v3),m)
                else: self.face((v0,v1,v2),m); self.face((v0,v2,v3),m)
        self.face(tuple(off+j for j in reversed(range(n))),0)
        self.face(tuple(off+(len(rings)-1)*n+j for j in range(n)),0)
    def tube(self,points,radii,n=12):
        off=len(self.v)
        pts=[Vector(x) for x in points]
        for i,c in enumerate(pts):
            d=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
            reference=Vector((1,0,0)) if abs(d.z)>.95 else Vector((0,0,1))
            u=d.cross(reference).normalized(); v=d.cross(u).normalized()
            for j in range(n):
                t=2*math.pi*j/n; r=radii[i]; self.v.append(tuple(c+u*(math.cos(t)*r[0])+v*(math.sin(t)*r[1])))
        for i in range(len(pts)-1):
            for j in range(n):
                self.face((off+i*n+j,off+i*n+(j+1)%n,off+(i+1)*n+(j+1)%n,off+(i+1)*n+j))
        self.face(tuple(off+j for j in reversed(range(n))))
        self.face(tuple(off+(len(pts)-1)*n+j for j in range(n)))
    def ellipsoid(self,c,r,n=12,rings=6):
        # Two unique poles avoid degenerate polar quad triangles.
        off=len(self.v); self.v.append((c[0],c[1],c[2]-r[2]))
        for i in range(1,rings):
            t=-math.pi/2+math.pi*i/rings
            for j in range(n):
                q=2*math.pi*j/n; self.v.append((c[0]+r[0]*math.cos(t)*math.cos(q),c[1]+r[1]*math.cos(t)*math.sin(q),c[2]+r[2]*math.sin(t)))
        top=len(self.v); self.v.append((c[0],c[1],c[2]+r[2]))
        for j in range(n): self.face((off,off+1+(j+1)%n,off+1+j)); self.face((top,off+1+(rings-2)*n+j,off+1+(rings-2)*n+(j+1)%n))
        for i in range(rings-2):
            for j in range(n): self.face((off+1+i*n+j,off+1+i*n+(j+1)%n,off+1+(i+1)*n+(j+1)%n,off+1+(i+1)*n+j))
    def finish(self,extra=None):
        obj=mesh_object(self.name,self.v,self.f,[M[k] for k in self.mats],col)
        for f,m in zip(obj.data.polygons,self.mi): f.material_index=m
        if extra:
            for k,v in extra.items(): obj[k]=v
        return obj
# Connected tail, barrel torso, smoothly narrowing neck. Widths are estimates.
body=[(-2.35,.18,.48,.004,.004),(-2.25,.16,.48,.013,.017),(-2.10,.13,.47,.023,.032),(-1.93,.095,.46,.039,.052),(-1.75,.06,.45,.056,.069),(-1.57,.03,.44,.077,.086),(-1.39,.01,.44,.099,.101),(-1.20,0,.44,.127,.121),(-1.03,0,.44,.157,.146),(-.86,0,.445,.192,.163),(-.66,0,.455,.227,.18),(-.43,0,.465,.251,.196),(-.19,0,.47,.260,.205),(.05,0,.47,.251,.202),(.28,0,.47,.224,.185),(.46,0,.472,.177,.15),(.61,0,.475,.131,.121),(.76,0,.48,.105,.103),(.92,0,.487,.092,.09),(1.08,0,.493,.086,.085),(1.25,0,.495,.087,.082),(1.43,0,.49,.104,.075),(1.47,0,.485,.108,.072)]
part=Part('01_Trunk_neck_tail',['dorsal','flank','ventral'])
part.loft(body,20,lambda i,j,t: 0 if math.sin(t)>.38 else 2 if math.sin(t)<-.50 else 1); part.finish({'anatomy':'Continuous inferred tail, trunk and neck; no fin or fluke','nominal_tail_length_m':1.51,'nominal_neck_length_m':.8})
# Broad blunt triangular skull; no constricted rostrum. Closed fleshed surface.
head=[(1.34,0,.49,.075,.060),(1.41,0,.497,.132,.078),(1.48,0,.50,.155,.085),(1.56,0,.50,.150,.080),(1.64,0,.493,.129,.071),(1.72,0,.481,.108,.059),(1.79,0,.472,.087,.050),(1.835,0,.465,.062,.040),(1.85,0,.463,.035,.029)]
part=Part('02_Broad_blunt_cranium',['dorsal','flank']); part.loft(head,20,lambda i,j,t:0 if math.sin(t)>.35 else 1); part.finish({'anatomy':'Fleshed Fig8 broad skull shape; posterior cheek region; no exposed fenestrae'})
# Jaw slopes gently downward at snout, leaving only a slim functional gape.
jaw=[(1.39,0,.437,.09,.026),(1.49,0,.414,.139,.025),(1.61,0,.391,.125,.025),(1.72,0,.376,.10,.024),(1.81,0,.366,.069,.021),(1.845,0,.366,.032,.017)]
part=Part('03_Lower_jaw',['flank','ventral']); part.loft(jaw,16,lambda i,j,t:1 if math.sin(t)<-.15 else 0); part.finish()
# Recessed palate is behind visible tooth row, not a black stripe pasted outside.
part=Part('04_Mouth_interior',['mouth']); part.loft([(1.46,0,.431,.115,.009),(1.58,0,.426,.101,.017),(1.71,0,.416,.076,.025),(1.81,0,.413,.044,.024)],12); part.finish()
# Bent proximal and distal limb segments remain leg-like; short partly webbed
# digits fan from broad palms. Every digit has one explicit endpoint in metadata.
limb_records=[]
for kind,sgn in [('fore',-1),('fore',1),('hind',-1),('hind',1)]:
    fore=kind=='fore'; side='right' if sgn<0 else 'left'; name=f'05_{kind}limb_{side}'
    part=Part(name,['flank']); f=lambda x,y,z:(x,sgn*y,z)
    if fore:
        pts=[f(.43,.13,.46),f(.43,.24,.425),f(.38,.36,.38),f(.34,.43,.355),f(.25,.49,.34),f(.13,.57,.33),f(.06,.62,.325)]
        radii=[(.10,.085),(.095,.075),(.08,.06),(.07,.05),(.065,.045),(.060,.035),(.065,.025)]
        wrist=Vector(f(.06,.62,.325)); lateral=Vector((-.75,sgn*.66,0)); across=Vector((.66,sgn*.75,0)); scale=1.
    else:
        pts=[f(-.70,.13,.43),f(-.76,.24,.405),f(-.83,.34,.37),f(-.88,.39,.35),f(-1.00,.45,.335),f(-1.07,.49,.32)]
        radii=[(.081,.069),(.074,.059),(.062,.047),(.055,.04),(.048,.033),(.050,.023)]
        wrist=Vector(f(-1.07,.49,.32)); lateral=Vector((-.77,sgn*.64,0)); across=Vector((.64,sgn*.77,0)); scale=.86
    part.tube(pts,radii,12)
    # Palm is a convex closed webbed pad, joined with short individually tapered digits.
    end=wrist+lateral*.105*scale
    part.tube([tuple(wrist-lateral*.035*scale),tuple(wrist+lateral*.05*scale),tuple(end)],[ (.07*scale,.024*scale),(.105*scale,.025*scale),(.107*scale,.019*scale)],16)
    endpoints=[]
    for i,(offset,length) in enumerate(zip([-.084,-.043,0,.043,.083],[.115,.16,.19,.17,.125])):
        base=end+across*(offset*scale)-lateral*.030*scale
        direction=(lateral+across*(offset*2.2)).normalized()
        tip=base+direction*length*scale+Vector((0,0,-.005))
        mid=base+direction*length*scale*.57+Vector((0,0,.002))
        # tips visibly separated beyond the palm, blunt and unclawed.
        part.tube([tuple(base),tuple(mid),tuple(tip-direction*.012*scale),tuple(tip)],[ (.021*scale,.017*scale),(.019*scale,.014*scale),(.013*scale,.011*scale),(.007*scale,.007*scale)],8)
        endpoints.append(list(tip))
    # Bound full shoulder-to-middle-digit length to the frozen body estimate.
    limb_scale=.82; pivot=Vector(pts[0])
    part.v=[tuple(pivot+(Vector(v)-pivot)*limb_scale) for v in part.v]
    endpoints=[list(pivot+(Vector(v)-pivot)*limb_scale) for v in endpoints]
    obj=part.finish({'anatomy':'Five short digits with inferred partial webbing; conservative distal proportions','digit_count':5,'digit_endpoints_json':json.dumps(endpoints),'limb_class':kind})
    limb_records.append({'name':name,'digit_count':5,'digit_endpoints_blender_m':endpoints,'proximal_centerline_length_m':limb_scale*sum((Vector(pts[i+1])-Vector(pts[i])).length for i in range(len(pts)-1)),'estimated_full_centerline_length_m':limb_scale*(sum((Vector(pts[i+1])-Vector(pts[i])).length for i in range(len(pts)-1))+.265*scale),'distal_reconstruction':'inferred partially webbed pentadactyl hand/foot'})
# Modest dark dorsolateral eyes; no cartoon eyelid bulges.
part=Part('06_Eyes_and_nares',['eyes'])
for s in [-1,1]:
    part.ellipsoid((1.625,s*.108,.535),(.027,.018,.022),12,6)
    part.ellipsoid((1.775,s*.043,.515),(.010,.006,.003),8,4)
part.finish()
# Broad sub-conical crowns taper to rounded blunt tips, not needle fangs.
part=Part('07_Short_stout_crowns',['teeth']); teeth=[]
for s in [-1,1]:
    for i,(x,w,z) in enumerate([(1.56,.126,.429),(1.61,.117,.425),(1.66,.106,.419),(1.71,.094,.414),(1.755,.081,.411),(1.795,.064,.410)]):
        base=Vector((x,s*w,z)); tip=base+Vector((.004,0,-.027 if i<4 else -.024)); mid=(base+tip)/2
        part.tube([tuple(base),tuple(mid),tuple(tip)],[ (.0125,.0105),(.011,.009),(.0065,.006)],10); teeth.append(list(tip))
    for x,w,z in [(1.585,.118,.412),(1.69,.095,.395),(1.77,.073,.385)]:
        base=Vector((x,s*w,z)); tip=base+Vector((0,0,.018)); part.tube([tuple(base),tuple((base+tip)/2),tuple(tip)],[ (.010,.009),(.009,.008),(.005,.0045)],10); teeth.append(list(tip))
part.finish({'anatomy':'Simplified short stout blunt crowns, not complete tooth count','visible_crown_count':len(teeth)})
bpy.context.view_layer.update()
if a.gray:
    gray=make_material('gray_diagnostic','#929292',roughness=.86)
    for o in col.objects:
        if o.type=='MESH':
            for i in range(len(o.data.materials)): o.data.materials[i]=gray
    render_previews(col,OUT,views=('front','side','top','hero'),resolution=512,samples=8,transparent=True)
    print('GRAY_READY'); raise SystemExit(0)
# Source QA and semantic measurements, before any presentation scene exists.
source=audit_source(col,max_triangles=24000)
if source['errors']: raise RuntimeError(source['errors'])
source['reviewed_warnings']={'mount':'Swimming asset. Lowest Z above zero is intentional; root is torso projection mounting point.'}
source['limbs']=limb_records
source['head_length_m']=.51 # fleshy cranial envelope includes neck insertion; nominal skull is .44 m
source['head_max_width_m']=.31
source['nominal_reconstruction_length_m']=4.2
bpy.context.scene['source_generator']='source/generate.py'; bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Unsupported export flags '+str(missing))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(OUT/'model.glb',24000,6,16)
if glb['errors']:raise RuntimeError(glb['errors'])
if glb['bytes']>2500000:raise RuntimeError('Byte budget exceeded')
b=source['bounds_blender_m']; emin=[b['min'][0],b['min'][2],-b['max'][1]]; emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',emin),('max',emax)] for i in range(3))
if delta>1e-4 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Roundtrip geometry mismatch')
qa=OUT/'qa'/'evidence'; qa.mkdir(parents=True,exist_ok=True)
glb['file']='model.glb'
record={'asset_id':'simosaurus','revision':'r001','blender_version':bpy.app.version_string,'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'threejs_gpu':'NOT_RUN','populated_scene':'NOT_RUN'}
(qa/'technical.json').write_text(json.dumps(record,indent=2)+'\n')
if not a.no_render:
    # New factory scene, import exact shipped bytes. Never source-scene final views.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    imported=bpy.data.collections.new('EXACT_GLB'); bpy.context.scene.collection.children.link(imported)
    for obj in list(bpy.context.scene.objects):
        for old in list(obj.users_collection):old.objects.unlink(obj)
        imported.objects.link(obj)
    vdir=OUT/'views'; render_previews(imported,vdir,views=('front','side','top','hero'),resolution=P['preview']['resolution'],samples=P['preview']['samples'],transparent=True)
    for name in ['front','side','top']:(vdir/f'preview-{name}.png').rename(vdir/f'{name}.png')
    (vdir/'preview-hero.png').rename(vdir/'perspective.png'); shutil.copyfile(vdir/'perspective.png',OUT/'preview.png')
    (qa/'preview-provenance.json').write_text(json.dumps({'status':'RENDERED_FROM_CLEAN_IMPORT','glb_sha256':glb['sha256'],'renderer':'Blender Cycles CPU','settings':P['preview'],'cameras':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},'preview_equals_perspective':True,'views':{x:hashlib.sha256((vdir/f'{x}.png').read_bytes()).hexdigest() for x in ['front','side','top','perspective']}},indent=2)+'\n')
print('BUILD_READY '+glb['sha256'])
