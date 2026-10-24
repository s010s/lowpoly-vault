# SPDX-License-Identifier: MIT
"""Agnostus pisiformis, first holaspid, original deterministic reconstruction.
Run with Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output .
The geometry is authored numerically in millimeters and converted to meters once
at mesh creation. Final output is always meter-scale, never enlarged for viewing.
"""
from pathlib import Path
import argparse, hashlib, json, math, re, shutil, sys
import bpy, bmesh
from mathutils import Vector
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
from asset_common import setup_scene, make_material, mesh_object
from micro_checks import source_audit, glb_audit
from preview import render_exact_glb


def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, v): Path(p).parent.mkdir(parents=True, exist_ok=True); Path(p).write_text(json.dumps(v, indent=2, ensure_ascii=False)+'\n')
args = argparse.ArgumentParser()
args.add_argument('--output', default=str(HERE.parent))
args.add_argument('--renders', choices=['none','gray','final'], default='none')
opts = args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(opts.output).resolve(); OUT.mkdir(parents=True,exist_ok=True)
P=json.loads((HERE/'params.json').read_text())
C=setup_scene('agnostus', P['seed'])
ROOT=bpy.data.objects[C['asset_root']]
ROOT['taxon']='Agnostus pisiformis'
ROOT['life_stage']='first holaspid h1'
ROOT['primary_specimen']='UB822'
ROOT['free_thoracic_tergites']=2
ROOT['appendage_pairs']=9
ROOT['opening_degrees']=P['gap_angle_degrees_inferred']
ROOT['origin']='Lowest surface aligned to Z=0; X=0 sagittal plane, Y=0 cephalic datum; swimming reconstruction without support geometry.'
M=[make_material('shell-warm-gray','#969184',.88),make_material('shell-axis','#817E70',.89),
   make_material('border-pale-gray','#B8B09A',.91),make_material('ventral-soft-body','#736E60',.92),
   make_material('limb-cuticle','#AB9D80',.91),make_material('setae','#C4B798',.94)]
SEM=[]
def mesh(name,vs,fs,mi, extra=None):
    o=mesh_object(name,[(x*.001,y*.001,z*.001) for x,y,z in vs],fs,M[mi],C)
    o['semantic_part']=name
    if extra:
        for k,v in extra.items():o[k]=v
    SEM.append({'name':name,'material':M[mi].name,'vertices':len(vs),'faces':len(fs)})
    return o

def tube(name, pts, widths, mi=4, sides=8, flatten=1, extra=None):
    pts=[Vector(p) for p in pts]; vs=[]; fs=[]; previous_u=None
    for i,p in enumerate(pts):
        t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
        if previous_u is None:
            axis=Vector((0,0,1))
            if abs(t.dot(axis))>.9:axis=Vector((0,1,0))
            u=t.cross(axis).normalized()
        else:
            u=previous_u-t*previous_u.dot(t)
            if u.length<1e-7:raise ValueError('Tube frame cannot be transported')
            u.normalize()
        previous_u=u.copy();v=t.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides
            vs.append(tuple(p+u*math.cos(a)*widths[i]+v*math.sin(a)*widths[i]*flatten))
    for i in range(len(pts)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides
            fs.append((a,b,b+sides,a+sides))
    fs += [tuple(reversed(range(sides))),tuple((len(pts)-1)*sides+j for j in range(sides))]
    return mesh(name,vs,fs,mi,extra)

def ellipsoid(name,center,radii,mi=3,segments=20,rings=10):
    vs=[(center[0],center[1],center[2]+radii[2])];fs=[]
    for i in range(1,rings):
        t=math.pi*i/rings
        for j in range(segments):
            a=math.tau*j/segments
            vs.append((center[0]+radii[0]*math.sin(t)*math.cos(a),center[1]+radii[1]*math.sin(t)*math.sin(a),center[2]+radii[2]*math.cos(t)))
    for j in range(segments):fs.append((0,1+j,1+(j+1)%segments))
    for i in range(rings-2):
        s=1+i*segments
        for j in range(segments):fs.append((s+j,s+segments+j,s+segments+(j+1)%segments,s+(j+1)%segments))
    last=len(vs);vs.append((center[0],center[1],center[2]-radii[2]));s=1+(rings-2)*segments
    for j in range(segments):fs.append((s+j,last,s+(j+1)%segments))
    return mesh(name,vs,fs,mi)

HEAD_L=P['head_length']*1000;HEAD_W=P['head_width']*1000
TAIL_L=P['pygidium_length']*1000
ANGLE=math.radians(P['gap_angle_degrees_inferred'])
HC=(0,-.045,.42); TH=(0,.47,.35)
def headmap(x,y,z):return(x,HC[1]+y,HC[2]+z)
def tailmap(x,y,z):
    s=y+TAIL_L/2
    return(x,TH[1]-math.cos(ANGLE)*s+math.sin(ANGLE)*z,TH[2]-math.sin(ANGLE)*s-math.cos(ANGLE)*z)

def shield(name,L,W,H,mapper,tail=False):
    n=64; ring_r=[.10,.22,.35,.48,.61,.73,.83,.90,.95,1.0]
    vs=[];fs=[]
    # An integrated axial relief, not a detached dorsal cylinder.
    def elevation(x,y,r):
        base=(H-.013)*.78*max(0,1-r*r)**.74
        if tail:
            axis=(H-.013)*.22*math.exp(-(x/.12)**4)*math.exp(-((y+.035)/(.32))**4)
            axis*=1-.12*math.exp(-((y+.16)/.018)**2)-.09*math.exp(-((y+.08)/.015)**2)
        else:
            axis=(H-.013)*.22*math.exp(-(x/.115)**4)*math.exp(-((y-.015)/.32)**4)
            axis*=1-.16*math.exp(-((y+.10)/.021)**2)-.12*math.exp(-((y-.19)/.019)**2)
        return base+axis*(1-r**6)
    # Paired outer and inner surfaces preserve the concave ventral cavity.
    for lower in [False,True]:
        vs.append(mapper(0,0,elevation(0,0,0)-(.016 if lower else 0)))
        for r in ring_r:
            for j in range(n):
                a=math.tau*j/n
                # Near-isopygous rounded shields; posterior subtly flattened.
                x=W/2*r*math.sin(a)
                y=-L/2*r*math.cos(a)
                z=elevation(x,y,r)-(.013 if lower else 0)
                vs.append(mapper(x,y,z))
    ns=1+len(ring_r)*n
    for layer in range(2):
        off=layer*ns
        for j in range(n):fs.append((off,off+1+j,off+1+(j+1)%n))
        for i in range(len(ring_r)-1):
            offi=off+1+i*n
            for j in range(n):fs.append((offi+j,offi+n+j,offi+n+(j+1)%n,offi+(j+1)%n))
    a=1+(len(ring_r)-1)*n
    for j in range(n):fs.append((a+j,a+(j+1)%n,ns+a+(j+1)%n,ns+a+j))
    ob=mesh(name,vs,fs,0,{'length_m':L*.001,'width_m':W*.001,'reference':'UB822 and Fig.2 first holaspid'})
    # Restrained axial material and the actual narrow rim are editable face regions.
    for mat in M[1:3]:ob.data.materials.append(mat)
    for f in ob.data.polygons:
        cent=sum((ob.data.vertices[v].co for v in f.vertices),Vector())/len(f.vertices)
        # Local radius obtained from untransformed construction records.
        ids=list(f.vertices); un=[i%ns for i in ids]; rmax=max((i-1)//n if i else -1 for i in un)
        if rmax>=len(ring_r)-2:f.material_index=2
        elif all(i<ns for i in ids) and abs(cent.x)<.00009:f.material_index=1
    return ob
head=shield('cephalic-shield-840x820um',HEAD_L,HEAD_W,HEAD_L*P['head_height_ratio'],headmap)
tail=shield('pygidial-shield',TAIL_L,.765,.185,tailmap,True)
# Small paired pygidial marginal spines, at the folded anterior-facing tail rim.
for sign in [-1,1]:
    pp=[tailmap(sign*.265,.235,.016),tailmap(sign*.301,.303,.004),tailmap(sign*.312,.36,-.004)]
    tube('pygidial-marginal-spine-'+str(sign),pp,[.018,.012,.0018],0,7)
# Posterolateral cephalic corners remain short, not extended trilobite horns.
for sign in [-1,1]:
    tube('cephalic-posterolateral-point-'+str(sign),[(sign*.255,.284,.46),(sign*.302,.355,.423),(sign*.319,.405,.408)],[.025,.014,.002],0,8)

def tergite(name,start_angle,end_angle,width):
    # A plate-like transverse articulating band follows the posterior sagittal
    # bend. Pleural wings and the axial ring are relief within one closed plate.
    nx=40;nt=6;vs=[];fs=[]
    for inside in [False,True]:
        for j in range(nt+1):
            a=math.radians(start_angle+(end_angle-start_angle)*j/nt)
            for i in range(nx+1):
                x=width*(2*i/nx-1);side=abs(x)/width
                lobe=.012*math.exp(-(x/.105)**4)+.008*math.exp(-((abs(x)-.20)/.055)**2)
                rad=.10+lobe-(.010 if inside else 0)
                vs.append((x,.36+rad*math.sin(a)-.045*side**2,.34+rad*math.cos(a)-.022*side**1.6))
    count=(nx+1)*(nt+1)
    for k in range(2):
        for j in range(nt):
            for i in range(nx):
                a=k*count+j*(nx+1)+i;fs.append((a,a+1,a+nx+2,a+nx+1))
    for j in [0,nt]:
        for i in range(nx):
            a=j*(nx+1)+i;fs.append((a,a+1,a+1+count,a+count))
    for i in [0,nx]:
        for j in range(nt):
            a=j*(nx+1)+i;fs.append((a,a+nx+1,a+nx+1+count,a+count))
    return mesh(name,vs,fs,1,{'free_thoracic_tergite':True,'ordinal':1 if '01' in name else 2})
tergite('thoracic-tergite-01',0,44,.282)
tergite('thoracic-tergite-02',49,95,.301)
# Continuous compact ventral axis follows the bend, not a bivalve lateral hinge.
tube('ventral-body-axis',[(0,-.30,.49),(0,-.12,.555),(0,.08,.55),(0,.27,.48),(0,.37,.37),(0,.32,.23),(0,.245,.10),(0,.17,-.01)], [.06,.092,.089,.075,.065,.053,.038,.017],3,12,flatten=.75)
ellipsoid('hypostome', (0,-.267,.468),(.06,.077,.024),3,20,8)
# Antennules I: curved multisegmented uniramous limbs. No dorsal eyes or eye stalks.
for sign,side in [(-1,'L'),(1,'R')]:
    path=[(sign*.055,-.275,.489),(sign*.10,-.37,.455),(sign*.16,-.47,.406),(sign*.21,-.565,.367),(sign*.235,-.64,.355),(sign*.217,-.695,.342),(sign*.19,-.72,.326)]
    for i in range(len(path)-1):
        a=Vector(path[i]);b=Vector(path[i+1]);d=b-a
        tube(f'appendage-01-antennule-{side}-podomere-{i+1:02}',[a,a+d*.93],[.018*(1-.10*i),.016*(1-.10*i)],4,8)
    for i in [2,3,4,5]:
        p=Vector(path[i]);q=p+Vector((sign*.026,.008,-.036))
        tube(f'antennular-seta-{side}-{i}',[p,q],[.0026,.0007],5,5)

# Homologous pairs II-IV are cephalic; V-IX are the five trunk pairs.
# The final h1 limb is a small developed leg, not the meraspid bud of Fig.6G.
origins=[(-.15,.53,.105,.27),(.015,.545,.105,.24),(.145,.515,.09,.205),(.27,.46,.078,.19),(.355,.35,.070,.17),(.312,.218,.057,.143),(.251,.102,.043,.113),(.185,.002,.031,.082)]
for pair,(y,z,rootx,reach) in enumerate(origins,start=2):
    for sign,side in [(-1,'L'),(1,'R')]:
        root=Vector((sign*rootx,y,z));scale=reach/.27
        tube(f'appendage-{pair:02}-{side}-coxa',[root,root+Vector((sign*.038*scale,-.018*scale,-.038*scale))],[.027*scale,.023*scale],3,9)
        base=root+Vector((sign*.030*scale,-.012*scale,-.024*scale))
        ex=[base,base+Vector((sign*.074*scale,-.035*scale,-.048*scale)),base+Vector((sign*.132*scale,-.072*scale,-.098*scale)),base+Vector((sign*.155*scale,-.111*scale,-.153*scale)),base+Vector((sign*.157*scale,-.133*scale,-.205*scale))]
        # Strong multiarticulate setose exopods on anterior cephalic appendages.
        if pair<=7:
            for j in range(4):
                a=ex[j];b=ex[j+1]
                tube(f'appendage-{pair:02}-{side}-exopod-{j+1:02}',[a,a+(b-a)*.95],[.022*scale*(1-.14*j),.018*scale*(1-.14*j)],4,8,flatten=.78)
            count=6 if pair in [2,3] else 5 if pair<=5 else 3
            for k in range(count):
                t=k/(count-1);start=ex[2].lerp(ex[4],t)
                extension=Vector((sign*(.085-.025*t)*scale,-(.073-.018*t)*scale,-(.074+.012*t)*scale))
                tube(f'appendage-{pair:02}-{side}-exopodal-seta-{k+1:02}',[start,start+extension*.65,start+extension],[.0038*scale,.0028*scale,.0009*scale],5,5)
        # Pair II has absent/reduced endopod, rather than a generic spider leg.
        if pair==2:continue
        en=[base,base+Vector((sign*.030*scale,-.025*scale,-.046*scale)),base+Vector((sign*.044*scale,-.039*scale,-.092*scale)),base+Vector((sign*.040*scale,-.062*scale,-.137*scale)),base+Vector((sign*.016*scale,-.085*scale,-.171*scale)),base+Vector((-sign*.008*scale,-.105*scale,-.188*scale))]
        if pair==4:
            ellipsoid(f'appendage-{pair:02}-{side}-endopodal-club',tuple(en[3]),(.022*scale,.021*scale,.035*scale),4,12,6)
        for j in range(5):
            a=en[j];b=en[j+1]
            tube(f'appendage-{pair:02}-{side}-endopod-{j+1:02}',[a,a+(b-a)*.93],[.018*scale*(1-.13*j),.0155*scale*(1-.13*j)],4,7)
        for k in range(2):
            start=en[-1];end=start+Vector((sign*(.013+.010*k)*scale,-.024*scale,-.023*scale))
            tube(f'appendage-{pair:02}-{side}-terminal-seta-{k+1}',[start,end],[.0028*scale,.0008*scale],5,5)
# Ground numerical minimum without altering physical dimensions.
minimum=min(v.co.z for o in C.objects if o.type=='MESH' for v in o.data.vertices)
for o in C.objects:
    if o.type=='MESH':
        for v in o.data.vertices:v.co.z-=minimum
ROOT['ground_shift_m']=-minimum
bpy.context.view_layer.update()
source=source_audit(C,max_triangles=40000)
source['semantic_parts']=SEM
source['measured_head_m']={'length':max(v.co.y for v in head.data.vertices)-min(v.co.y for v in head.data.vertices),'width':max(v.co.x for v in head.data.vertices)-min(v.co.x for v in head.data.vertices),'height':max(v.co.z for v in head.data.vertices)-min(v.co.z for v in head.data.vertices),'target_height_ratio':P['head_height_ratio']}
source['measured_head_m']['actual_height_ratio']=source['measured_head_m']['height']/source['measured_head_m']['length']
pairs={i:set() for i in range(1,10)}
for part in SEM:
    match=re.match(r'appendage-(\d+)-(?:antennule-)?([LR])-',part['name'])
    if match:pairs[int(match.group(1))].add(match.group(2))
if any(sides!={'L','R'} for sides in pairs.values()):raise RuntimeError('Missing anatomical appendage side')
tergites=[o.name for o in C.objects if o.get('free_thoracic_tergite')]
if len(tergites)!=2:raise RuntimeError('Incorrect free tergite count')
source['anatomical_counts']={'free_thoracic_tergites':len(tergites),'free_tergite_objects':tergites,'cephalic_pairs':len([p for p in pairs if p<=4]),'trunk_pairs':len([p for p in pairs if p>4]),'total_appendage_pairs':len(pairs),'source_objects_confirmed_sides':{str(i):sorted(v) for i,v in pairs.items()}}
write(OUT/'qa/evidence/source-audit.json',source)
if source['errors']:raise RuntimeError('Source check failed: '+str(source['errors']))
bpy.context.preferences.filepaths.save_version=0
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                try:space.params.directory=b'//';space.params.filename=''
                except (AttributeError,TypeError):pass
bpy.context.scene.render.filepath='//'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'),relative_remap=True)
# Coalesce only export copies by material, leaving the saved semantic source intact.
# Six material groups produce six GLB primitives, no draw-call explosion.
combined={i:([],[]) for i in range(len(M))}
for o in list(C.objects):
    if o.type!='MESH':continue
    for p in o.data.polygons:
        global_m=M.index(o.data.materials[p.material_index])
        vv,ff=combined[global_m];k=len(vv)
        vv.extend(tuple(o.matrix_world@o.data.vertices[v].co) for v in p.vertices)
        ff.append(tuple(k+j for j in range(len(p.vertices))))
    bpy.data.objects.remove(o,do_unlink=True)
for i,(vs,fs) in combined.items():
    if vs:mesh_object('export-'+M[i].name,vs,fs,M[i],C,recalculate_normals=False)
bpy.ops.object.select_all(action='DESELECT')
for o in C.objects:o.select_set(True)
bpy.context.view_layer.objects.active=ROOT
export=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
missing=set(export)-available
if missing:raise RuntimeError('Missing exporter options '+str(missing))
bpy.ops.export_scene.gltf(**export)
report=glb_audit(OUT/'model.glb',source)
write(OUT/'qa/evidence/glb-audit.json',report)
if report['errors']:raise RuntimeError('GLB check failed '+str(report['errors']))
write(OUT/'qa/evidence/build.json',{'blender':bpy.app.version_string,'seed':P['seed'],'source_generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'glb_sha256':digest(OUT/'model.glb'),'blend_sha256':digest(OUT/'model.blend'),'export_options':{k:v for k,v in export.items() if k!='filepath'},'geometry_profile':'static-uncompressed-palette-only','units':'meters','origin':ROOT['origin'],'source_semantic_objects':len(SEM),'export_material_groups':len(combined),'counts':report['counts'],'unrun':['target GPU render','populated scene performance','independent visual and factual acceptance','user acceptance','deployment']})
if opts.renders!='none':
    render_exact_glb(OUT/'model.glb',OUT,gray=opts.renders=='gray')
print('AGNOSTUS_BUILD_COMPLETE',report['sha256'])
