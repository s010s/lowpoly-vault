# SPDX-License-Identifier: MIT
"""Deterministic Dalmanites genus-level living reconstruction.
Run with Blender in background mode, then pass -- --output DIR.
Scientific scope and uncertainty are frozen in brief.json and params.json.
All modeled vertices are original. No fossil scan geometry is incorporated.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
sys.path.insert(0, str(Path(__file__).resolve().parent/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads(Path(__file__).with_name('params.json').read_text())
M=.001
C=setup_scene(P['asset_id'],P['seed'])
ROOT=bpy.data.objects[C['asset_root']]
PALETTE=[('dorsal_olive','#71634A',.78),('ridges_ochre','#887454',.78),('flexible_underside','#504F42',.86),('limbs_umber','#796447',.82),('ocular_cuticle','#403E2F',.53),('ocular_lenses','#C4AD7E',.45)]
MAT=[make_material(*x[:2],roughness=x[2]) for x in PALETTE]
PARTS=[]

def add(name,v,f,mat=0,smooth=False):
    ob=mesh_object(name,[(x*M,y*M,z*M) for x,y,z in v],f,MAT[mat],C)
    for p in ob.data.polygons: p.use_smooth=smooth
    ob['anatomical_component']=name
    PARTS.append(ob)
    return ob

def tube(name,pts,radii,mat=0,sides=8,ell=.85):
    # Original closed elliptical tube with endpoint caps; no collapsed rings.
    v=[]
    for i,p in enumerate(pts):
        p=Vector(p); t=Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(0,i-1)])
        t.normalize(); u=t.cross(Vector((0,0,1)))
        if u.length<.1:u=t.cross(Vector((0,1,0)))
        u.normalize();w=t.cross(u).normalized()
        r=radii[i]
        for j in range(sides):
            a=2*math.pi*j/sides;v.append(tuple(p+u*(r*math.cos(a))+w*(r*ell*math.sin(a))))
    f=[tuple(reversed(range(sides)))]
    for i in range(len(pts)-1):
        for j in range(sides):
            k=i*sides+j;l=i*sides+(j+1)%sides; f.append((k,l,l+sides,k+sides))
    f.append(tuple((len(pts)-1)*sides+j for j in range(sides)))
    return add(name,v,f,mat)

def ellipsoid(name,center,scales,mat=0,segments=12,rings=5,smooth=False):
    v=[(center[0],center[1],center[2]-scales[2])]
    for i in range(1,rings):
        lat=-math.pi/2+math.pi*i/rings
        for j in range(segments):
            a=2*math.pi*j/segments
            v.append((center[0]+scales[0]*math.cos(lat)*math.cos(a),center[1]+scales[1]*math.cos(lat)*math.sin(a),center[2]+scales[2]*math.sin(lat)))
    v.append((center[0],center[1],center[2]+scales[2]));top=len(v)-1
    f=[]
    for j in range(segments):f.append((0,1+(j+1)%segments,1+j))
    for i in range(rings-2):
        for j in range(segments):
            a=1+i*segments+j;b=1+i*segments+(j+1)%segments; f.append((a,b,b+segments,a+segments))
    for j in range(segments):f.append((top,1+(rings-2)*segments+j,1+(rings-2)*segments+(j+1)%segments))
    return add(name,v,f,mat,smooth)

def solid_grid(name,nx,nt,fn,mat=0,thickness=.5,material_bands=False):
    # Surface plus a complete lower skin and stitched perimeter: never a paper shell.
    v=[fn(i/nx,j/nt) for j in range(nt+1) for i in range(nx+1)]
    size=len(v);v.extend([(x,y,z-thickness) for x,y,z in v]);f=[]
    for j in range(nt):
        for i in range(nx):
            a=j*(nx+1)+i;f.append((a,a+1,a+nx+2,a+nx+1));f.append((a+size,a+nx+1+size,a+nx+2+size,a+1+size))
    boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,nt+1)]+[nt*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(nt-1,0,-1)]
    for i,a in enumerate(boundary):
        b=boundary[(i+1)%len(boundary)];f.append((a,b,b+size,a+size))
    ob=add(name,v,f,mat)
    if material_bands:
        ob.data.materials.append(MAT[1])
        for p in ob.data.polygons:
            if p.index<2*nx*nt and (p.index//(2*nx)) in [1,2]:p.material_index=1
    return ob

# Crescent head: a rounded anterior outline and posterior cephalic margin.
def head(u,t):
    q=(u*2-1)*.998; x=16.5*q
    yf=-25+12.8*(abs(q)**2.8);yb=-10.6+1.2*(abs(q)**2)
    y=yf+(yb-yf)*t
    z=3.0+2.4*(1-q*q)*(math.sin(math.pi*t)**.62)+.35*(1-q*q)
    return x,y,z
solid_grid('cephalon_crescent_shield',32,12,head,0,.6)
# Rolled anterior border, continuous paired sides with no imported texture.
pts=[head(i/32,.018) for i in range(33)]
tube('cephalic_anterior_border',[(x,y,z+.07) for x,y,z in pts],[.24]*33,1,8,.7)
# Inflated glabella with frontal expansion and posterior contraction.
tube('glabella_expanded_front',[(0,-23.1,4.6),(0,-21.7,5.4),(0,-19,5.9),(0,-16.5,6.0),(0,-13.7,5.7),(0,-11.3,5.45)],[1.1,3.75,4.25,3.6,2.85,2.7],0,16,.66)
# Narrow occipital ring behind the glabella.
tube('occipital_ring',[(-3,-11.5,5.4),(-1.8,-11.25,6.6),(0,-11.2,7.1),(1.8,-11.25,6.6),(3,-11.5,5.4)],[.31]*5,1,8,.7)
for sign,side in [(-1,'left'),(1,'right')]:
    tube('genal_spine_'+side,[(sign*15.7,-11.8,3.1),(sign*16.1,-8.7,2.9),(sign*15.6,-4.4,2.7),(sign*14.4,.3,2.4),(sign*12.8,4.4,2.2)],[1.1,.94,.68,.37,.055],0,10,.75)
    # Ocular platform and individually separated low lens facets.
    ellipsoid('schizochroal_eye_platform_'+side,(sign*6.4,-18.1,6.0),(2.2,3.0,1.45),4,16,7)
    for row in range(4):
        lat=.08+.25*row
        for j in range(9):
            a=-1.28+2.56*j/8
            x=sign*(6.4+2.12*math.cos(a)*math.cos(lat)); y=-18.1+2.88*math.sin(a)*math.cos(lat);z=6.0+1.43*math.sin(lat)
            ellipsoid('eye_'+side+'_lens_%02d_%02d'%(row,j),(x,y,z),(.235,.255,.235),5,6,3)
    # Antennae are inferred, retained within the restored body length envelope.
    tube('inferred_antenna_'+side,[(sign*3.5,-21.4,2.4),(sign*6.9,-23.6,2.0),(sign*10.2,-24.6,2.0),(sign*12.0,-23.8,2.4),(sign*12.5,-22.6,2.8)],[.24,.20,.15,.10,.055],3,7,1)

# Continuous ventral trunk underlap backs every inter-tergite joint.
tube('continuous_ventral_trunk',[(0,-11,2.8),(0,-7,2.8),(0,0,2.7),(0,7,2.5),(0,13,2.4)],[8.4,8.2,7.8,6.9,5.5],2,18,.16)
# Eleven separate, physically overlapping articulated thoracic tergites.
for i in range(11):
    yc=-10.3+i*(23/11); hw=14.1-3.45*(i/10)**1.5; lift=1-i*.025
    def seg(u,t,yc=yc,hw=hw,i=i,lift=lift):
        q=2*u-1;x=q*hw
        y=yc+(t-.5)*2.77+(.25+1.5*i/10)*(abs(q)**3)
        z=2.65+2.0*(1-q*q)+1.9*math.exp(-((abs(x)/3.1)**4))
        z+=(.45*math.sin(math.pi*t)-.16*math.exp(-((t-.75)/.09)**2))*lift
        z-=.38*i/10
        return x,y,z
    ob=solid_grid('thoracic_tergite_%02d'%(i+1),28,6,seg,0,.62,True)
    ob['segment_number']=i+1;ob['fore_aft_overlap_mm']=2.77-23/11
    # A short central transverse ring clarifies the axial lobe without detached beads.
    pts=[seg(.5+x/(2*hw),.36) for x in [-2.8,-2,-1,0,1,2,2.8]]
    tube('thoracic_axial_ring_%02d'%(i+1),[(x,y,z+.07) for x,y,z in pts],[.16]*7,1,6,.7)

# Broad subtriangular pygidium; 13 shallow axial rings and 9 paired furrows.
def tail_width(t):return 10.9*(1-.89*t**1.45)+.08

def tail(u,t):
    q=2*u-1;x=q*tail_width(t);y=11.85+13.15*t
    axis=1.4*(1-.67*t)*math.exp(-((x/(2.8-1.65*t))**4))
    z=2.65+1.7*(1-q*q)*(1-.60*t)+axis
    # Fine ribs exist in the solid shell. Furrows stop short of the outer border.
    coord=t-.075*(abs(q)**1.25)*(1-t)
    ridge=.16*math.cos(2*math.pi*9*coord)*(1-q*q)*min(1,t*14)
    z+=ridge
    return x,y,z
solid_grid('pygidium_broad_ribbed_shield',34,40,tail,0,.62)
for k in range(13):
    t=.045+k*.063;aw=2.7-1.6*t
    pts=[tail(.5+x/(2*tail_width(t)),t) for x in [-aw,-aw*.7,0,aw*.7,aw]]
    tube('pygidial_shallow_axial_ring_%02d'%(k+1),[(x,y,z+.10) for x,y,z in pts],[.145*(1-.4*t)]*5,1,6,.65)
# Nine lateral ribs sweep posteriorly, embedded into the continuous plate.
for side,sign in [('left',-1),('right',1)]:
    for k in range(9):
        t=.06+k*.086; pts=[]
        for n in range(9):
            q=.26+.65*n/8;tt=t+.075*q**1.25*(1-t)
            pt=tail((sign*q+1)/2,tt);pts.append((pt[0],pt[1],pt[2]+.07))
        tube('pygidial_pleural_rib_'+side+'_%02d'%(k+1),pts,[.15*(1-.3*t)]*9,1,6,.65)
tube('single_median_caudal_spine',[(0,24.3,3.08),(0,26.0,2.95),(0,29.0,2.65),(0,33.2,2.30),(0,37.0,1.85)],[1.32,1.05,.72,.37,.055],0,10,.75)

# Comparative ventral limb system. Counts are interpretation, not PRI preservation.
def limb_pair(tag,y,span,scale=1):
    for sign,side in [(-1,'left'),(1,'right')]:
        tube(tag+'_endopod_'+side,[(sign*2.35,y,2.5),(sign*4.1,y+.15,1.7),(sign*span*.71,y+.45,.65),(sign*span,y+.85,.18)],[.43*scale,.34*scale,.25*scale,.16*scale],3,7,.8)
        # A restrained oval exopod paddle below the pleura, solid membrane with ribs.
        cx=sign*(span*.60);cy=y+.10;cz=2.25
        ellipsoid(tag+'_membrane_'+side,(cx,cy,cz),(span*.29,.73*scale,.11*scale),2,12,4)
        for n in range(5):
            dy=(-.48+.24*n)*scale
            tube(tag+'_fan_rib_'+side+'_%02d'%n,[(sign*3.9,cy+dy*.3,cz+.06),(cx,cy+dy,cz+.06),(sign*span*.86,cy+dy*.7,cz+.02)],[.10*scale,.085*scale,.06*scale],3,5,.7)
        tube(tag+'_exopod_stem_'+side,[(sign*2.4,y,2.45),(sign*4,y,2.34),(cx,cy,cz)],[.25*scale,.20*scale,.15*scale],3,7,.8)
for i in range(3):limb_pair('head_postantennal_pair_%02d'%(i+1),-19.3+i*2.4,8.0+i*1.15,.75 if i==0 else .95)
for i in range(11):limb_pair('thoracic_pair_%02d'%(i+1),-9.9+i*23/11,12.9-3.0*i/10,1-.19*i/10)
for i in range(6):limb_pair('inferred_pygidial_pair_%02d'%(i+1),13.0+i*1.7,7.7-i*.70,.77-i*.065)
ellipsoid('hypostome_comparative',(0,-19.3,2.35),(2.5,3.0,.65),2,14,6)

# Retain semantic editable objects in the source; export six material groups only.
EDIT=bpy.data.collections.new('EDITABLE_ANATOMY');bpy.context.scene.collection.children.link(EDIT)
for ob in list(PARTS):
    C.objects.unlink(ob);EDIT.objects.link(ob);ob.parent=None
EDIT.hide_render=True;EDIT.hide_viewport=True
bpy.context.view_layer.update()
for mi,mat in enumerate(MAT):
    vs=[];fs=[];groups=[]
    for ob in PARTS:
        selected=[p for p in ob.data.polygons if ob.data.materials[p.material_index]==mat]
        if not selected:continue
        start=len(vs);vs.extend([tuple(v.co) for v in ob.data.vertices]);fs.extend([tuple(start+vi for vi in p.vertices) for p in selected]);groups.append((ob.name,start,len(vs)))
    if vs:
        # Aggregate preserves original closed components, not a boolean union.
        out=mesh_object(mat.name+'_export',vs,fs,mat,C,recalculate_normals=False)
        for name,start,end in groups:out.vertex_groups.new(name=name).add(list(range(start,end)),1.,'REPLACE')
# Exact lowest foot contact is the documented ground center reference.
all_export=[o for o in C.objects if o.type=='MESH'];low=min(v.co.z for o in all_export for v in o.data.vertices)
for ob in all_export+PARTS:
    for v in ob.data.vertices:v.co.z-=low
ROOT['reconstruction']='Genus-level comparative restoration; missing tips and all appendages inferred.'
ROOT['preserved_PRI_body_length_m']=.05;ROOT['estimated_complete_length_m']=.062
ROOT['pygidial_limb_pairs_inferred']=6
scene=bpy.context.scene;scene['source_notes']='See brief.json and references.json; palette is artistic.'
scene.render.threads_mode='FIXED';scene.render.threads=2
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);args=a.parse_args(argv);out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
source=audit_source(C,max_triangles=40000)
# Material partitioning opens edges between export material groups; semantic originals stay closed.
source['partition_note']='Export material groups share position boundaries. Complete semantic originals are individually closed; export components are not a boolean union.'
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
# Store no external scripts, images, or directory references in the blend.
for tx in list(bpy.data.texts):bpy.data.texts.remove(tx)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
bpy.ops.object.select_all(action='DESELECT')
for ob in C.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=ROOT
options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Missing exporter options: '+repr(missing))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(out/'model.glb',max_triangles=40000,max_materials=6,max_primitives=8)
if glb['errors']:raise RuntimeError(glb['errors'])
glb['file']='model.glb'
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ['min','max'] for i in range(3));assert delta<1e-7
assert glb['scene_triangles']==source['triangles']
result={'source':source,'glb':glb,'source_to_glb_bounds_max_error_m':delta,'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','seed':P['seed'],'semantic_parts':len(PARTS),'palette':PALETTE,'export_options':{k:v for k,v in options.items() if k!='filepath'},'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256(Path(__file__).with_name('params.json').read_bytes()).hexdigest(),'counts':{'thoracic_tergites':11,'head_postantennal_pairs':3,'thoracic_limb_pairs':11,'pygidial_limb_pairs_inferred':6,'pygidial_axial_rings':13,'pygidial_pleural_ribs_per_side':9,'caudal_spines':1},'scope':'Maker technical evidence only; no independent, GPU, scene, user or deployment approval.'}
(out/'technical-build.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print('DALMANITES_BUILD_COMPLETE',glb['scene_triangles'],glb['sha256'])
