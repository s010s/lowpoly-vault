# SPDX-License-Identifier: MIT
"""Original Macrauchenia living reconstruction. Blender 4.3.2, no image inputs.
Run: blender -b --threads 2 --python source/generate.py -- --out OUTPUT
Optional --gray / --render imports only the exact exported model.glb.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
class Part:
    def __init__(self,name,mats):self.name=name;self.mats=mats if isinstance(mats,list) else [mats];self.v=[];self.f=[];self.mi=[]
    def add(self,v,f,mat=0):
        n=len(self.v);self.v.extend(v);self.f.extend(tuple(i+n for i in face) for face in f);self.mi.extend([mat]*len(f))
    def emit(self):
        o=ac.mesh_object(self.name,self.v,self.f,self.mats,COL)
        for f,i in zip(o.data.polygons,self.mi):f.material_index=i
        return o

def tube_geometry(rows,sides=12):
    vs=[]
    for i,row in enumerate(rows):
        c=Vector(row[:3]);t=(Vector(rows[min(i+1,len(rows)-1)][:3])-Vector(rows[max(i-1,0)][:3])).normalized()
        ref=Vector((1,0,0)) if abs(t.x)<.9 else Vector((0,1,0));u=(ref-t*ref.dot(t)).normalized();v=t.cross(u)
        for j in range(sides):
            a=2*math.pi*j/sides;vs.append(tuple(c+u*row[3]*math.cos(a)+v*row[4]*math.sin(a)))
    fs=[tuple(reversed(range(sides)))]
    for i in range(len(rows)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;c=b+sides;d=a+sides
            fs.extend([(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)])
    fs.append(tuple((len(rows)-1)*sides+j for j in range(sides)));return vs,fs

def tube(name,rows,sides,mats):
    p=Part(name,mats);p.add(*tube_geometry(rows,sides));return p.emit()

def loft(name,rows,sides,mats,regions=False):
    # Y-station contour lofts. Independently sculpted ventral and dorsal boundaries.
    vs=[]
    for y,w,b,t in rows:
        for j in range(sides):
            a=2*math.pi*j/sides;vs.append((w*math.cos(a),y,(b+t)/2+(t-b)*math.sin(a)/2))
    fs=[tuple(reversed(range(sides)))]
    for i in range(len(rows)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;c=b+sides;d=a+sides
            fs.extend([(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)])
    fs.append(tuple((len(rows)-1)*sides+j for j in range(sides)))
    p=Part(name,mats);p.add(vs,fs);o=p.emit()
    if regions:
        for f in o.data.polygons:
            if len(f.vertices)==3:
                z=sum(o.data.vertices[i].co.z for i in f.vertices)/3
                n=f.normal
                f.material_index=1 if n.z>.8 else 2 if n.z<-.50 else 0
    return o

def oval(name,c,s,mat,rings=7,sides=12):
    vs=[(c[0],c[1],c[2]-s[2])]
    for i in range(1,rings):
        a=-math.pi/2+math.pi*i/rings
        for j in range(sides):
            b=2*math.pi*j/sides;vs.append((c[0]+s[0]*math.cos(a)*math.cos(b),c[1]+s[1]*math.cos(a)*math.sin(b),c[2]+s[2]*math.sin(a)))
    vs.append((c[0],c[1],c[2]+s[2]));end=len(vs)-1
    fs=[(0,1+(j+1)%sides,1+j) for j in range(sides)]
    for i in range(rings-2):
        for j in range(sides):
            a=1+i*sides+j;b=1+i*sides+(j+1)%sides;fs.extend([(a,b,b+sides),(a,b+sides,a+sides)])
    fs.extend((end,1+(rings-2)*sides+j,1+(rings-2)*sides+(j+1)%sides) for j in range(sides));p=Part(name,mat);p.add(vs,fs);return p.emit()

def create():
    global COL
    COL=ac.setup_scene(P['asset_id'],P['seed']);colors=P['palette_srgb']
    coat=ac.make_material('Warm neutral coat',colors['coat'],.91);back=ac.make_material('Dorsal coat',colors['dorsal'],.93)
    under=ac.make_material('Ventral coat',colors['under'],.94);dark=ac.make_material('Eyes and subtle soft-nasal openings',colors['dark'],.55)
    hoof=ac.make_material('Three-toed hoof horn',colors['hoof'],.88);ear=ac.make_material('Pinna inner surface',colors['ear'],.94)
    loft('Deep long torso without hump',[
        [-.91,.115,1.19,1.55],[-.75,.235,1.01,1.65],[-.48,.305,.91,1.69],[-.15,.325,.88,1.68],
        [.18,.320,.90,1.66],[.48,.305,.96,1.65],[.77,.275,1.00,1.63],[1.00,.205,1.08,1.56],[1.18,.045,1.28,1.43]],
        24,[coat,back,under],True)
    neck=tube('Long upright gently curved neck',[(0,-.62,1.42,.180,.210),(0,-.77,1.64,.225,.245),
        (0,-.91,1.83,.175,.19),(0,-1.015,2.02,.145,.155),(0,-1.105,2.20,.128,.14),
        (0,-1.195,2.37,.125,.14),(0,-1.275,2.49,.145,.15)],20,[coat,back,under])
    for f in neck.data.polygons:
        f.material_index=1 if f.normal.y>.7 else 2 if f.normal.y<-.7 else 0
    # Long narrow skull; high/retracted nasal region does not imply a trunk.
    loft('Elongate skull and high retracted nasal profile',[
        [-1.235,.095,2.39,2.59],[-1.31,.145,2.36,2.67],[-1.40,.160,2.35,2.70],
        [-1.49,.149,2.34,2.68],[-1.59,.119,2.32,2.61],[-1.69,.098,2.31,2.55],[-1.79,.078,2.32,2.50],[-1.82,.047,2.35,2.46]],
        20,[coat,back,under],True)
    loft('Long mandibular ramus',[
        [-1.30,.100,2.33,2.48],[-1.43,.128,2.29,2.39],[-1.57,.106,2.27,2.35],[-1.70,.085,2.29,2.35],[-1.81,.050,2.33,2.38]],16,[under])
    # Mouth seam is small and closed, wholly separate from the upper nasal pad.
    seam=Part('Narrow lateral closed mouth seams',[dark])
    for s in [-1,1]:seam.add(*tube_geometry([(s*.060,-1.805,2.377,.004,.004),(s*.091,-1.70,2.350,.004,.004),(s*.105,-1.60,2.354,.0025,.0025)],7))
    seam.emit()
    # A conservative short mobile pad at the elevated dorsal rostrum, never a hanging proboscis.
    loft('Short elevated soft nasal pad',[
        [-1.48,.080,2.571,2.656],[-1.55,.088,2.560,2.655],[-1.61,.079,2.540,2.622],[-1.66,.050,2.525,2.576]],14,[back])
    nose=Part('Inferred restrained nasal openings',[dark])
    for s in [-1,1]:
        # Rounded narrow nostril marks on the upper rear muzzle; position explicitly inferred.
        vs,fs=tube_geometry([(s*.079,-1.565,2.603,.008,.003),(s*.076,-1.600,2.588,.008,.003)],8);nose.add(vs,fs)
        oval('Lateral orbital margin '+str(s),(s*.150,-1.431,2.568),(.017,.045,.039),back)
        oval('Lateral eye '+str(s),(s*.162,-1.439,2.570),(.010,.027,.023),dark)
        pinna=tube('Small inferred pinna '+str(s),[(s*.102,-1.285,2.610,.038,.022),(s*.150,-1.267,2.706,.050,.026),(s*.175,-1.255,2.784,.034,.019),(s*.171,-1.251,2.819,.007,.008)],10,[coat,ear])
        for f in pinna.data.polygons:
            if f.normal.y<-.5:f.material_index=1
    nose.emit()
    for s,lab in [(-1,'L'),(1,'R')]:
        # Subtle stagger avoids coincident projected limbs while all feet remain grounded.
        fore_y=-.68+(-.12 if s>0 else .06);hind_y=.82+(.10 if s>0 else -.11)
        tube('Long forelimb '+lab,[(s*.10,-.57,1.40,.090,.105),(s*.265,-.56,1.23,.120,.13),
            (s*.28,-.45,1.02,.084,.10),(s*.285,fore_y+.05,.72,.055,.065),(s*.29,fore_y,.52,.064,.066),
            (s*.30,fore_y-.015,.30,.043,.048),(s*.305,fore_y-.030,.16,.054,.055),(s*.305,fore_y-.065,.10,.072,.067)],14,[coat])
        tube('Long hindlimb '+lab,[(s*.10,.77,1.39,.105,.140),(s*.26,.65,1.20,.145,.165),
            (s*.285,.49,1.01,.105,.12),(s*.30,.78,.75,.073,.078),(s*.31,hind_y+.08,.56,.063,.085),
            (s*.315,hind_y+.04,.37,.042,.047),(s*.32,hind_y,.18,.050,.056),(s*.32,hind_y-.025,.10,.070,.066)],14,[coat])
        for role,cx,cy in [('Fore',s*.305,fore_y-.075),('Hind',s*.32,hind_y-.035)]:
            skin=Part(role+' three digit soft tissue '+lab,[coat]);horn=Part(role+' three distinct terminal hooves '+lab,[hoof])
            skin.add(*tube_geometry([(cx,cy+.035,.14,.068,.056),(cx,cy,.095,.092,.055),(cx,cy-.035,.062,.093,.044)],12))
            for j in [-1,0,1]:
                ex=cx+j*.068;ey=cy-.080+(.017 if j else -.014)
                skin.add(*tube_geometry([(cx+j*.045,cy-.020,.074,.032,.032),(ex,ey+.027,.050,.031,.030),(ex,ey,.038,.030,.026)],10))
                # Three independent rounded square horn caps; central digit is slightly longer.
                vs,fs=tube_geometry([(ex,ey+.012,.050,.031,.028),(ex,ey-.020,.040,.035,.029),(ex,ey-.044,.031,.031,.027)],10)
                # Flat sole clips to z=0 rather than balancing on an arbitrary triangle tip.
                vs=[(x,y,max(0,z-.006)) for x,y,z in vs];horn.add(vs,fs)
            skin.emit();horn.emit()
    # Short inferred tail centerline, separated from body-length estimate.
    tail=tube('Short tapering tail',[(0,1.12,1.43,.060,.060),(.018,1.23,1.34,.046,.047),(.033,1.28,1.23,.034,.035),(.052,1.30,1.10,.023,.024),(.070,1.30,1.02,.007,.008)],12,[coat,back])
    for f in tail.data.polygons:
        if f.normal.z<-.3:f.material_index=1
    # Keep all anatomical control lofts editable in a source-only collection.
    # A voxel union rounds functional skin joins; a decimated evaluated copy is the asset surface.
    names=['Deep long torso without hump','Long upright gently curved neck','Elongate skull and high retracted nasal profile',
        'Long mandibular ramus','Long forelimb L','Long forelimb R','Long hindlimb L','Long hindlimb R','Short tapering tail']
    source_parts=[bpy.data.objects[n] for n in names]
    controls=bpy.data.collections.new('AUTHORING - semantic skin control lofts');bpy.context.scene.collection.children.link(controls)
    skin=Part('Continuous anatomical skin',[coat,back,under])
    for o in source_parts:
        matmap={i:[coat,back,under].index(m) for i,m in enumerate(o.data.materials)}
        n=len(skin.v);skin.v.extend(tuple(o.matrix_world@v.co) for v in o.data.vertices)
        for f in o.data.polygons:skin.f.append(tuple(n+i for i in f.vertices));skin.mi.append(matmap[f.material_index])
        COL.objects.unlink(o);controls.objects.link(o);o.parent=None;o.hide_render=True;o.hide_set(True)
    surface=skin.emit();bpy.ops.object.select_all(action='DESELECT');surface.select_set(True);bpy.context.view_layer.objects.active=surface
    mod=surface.modifiers.new('Union anatomical overlaps','REMESH');mod.mode='VOXEL';mod.voxel_size=.025;mod.use_smooth_shade=False
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=surface.modifiers.new('Round skin transitions','SMOOTH');mod.factor=.65;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=surface.modifiers.new('Intentional low-poly surface','DECIMATE');mod.ratio=.22;mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
    for f in surface.data.polygons:
        f.use_smooth=False;c=f.center
        # Broad restrained regions follow anatomy, not random per-triangle color noise.
        f.material_index=2 if c.y>-.65 and c.z<1.10 and f.normal.z<-.25 else 0
    surface['source_controls']='AUTHORING - semantic skin control lofts';surface['voxel_union_m']=.025;surface['decimation_ratio']=.22
    footpts=[o.matrix_world@v.co for o in COL.all_objects if o.type=='MESH' and 'terminal hooves' in o.name for v in o.data.vertices]
    c=Vector([(min(p[i] for p in footpts)+max(p[i] for p in footpts))/2 for i in [0,1]]+[0])
    for o in COL.all_objects:
        if o.type=='MESH':
            for v in o.data.vertices:v.co-=c
    shift=ac.ground_asset(COL,False);root=bpy.data.objects[P['asset_id']]
    root['taxon']='Macrauchenia patachonica';root['representation']='whole living reconstruction, not a scanned specimen'
    root['scale_note']='Approximate whole-body dimensions; PIMUZ A/V 5700 atlas measurements are not used as a whole-body measurement.'
    root['soft_tissue_note']='Short elevated nasal pad, ears, skin and color are conservative inferences; no elongated proboscis.'
    root['original_footprint_center_xy']=list(c)[:2];root['ground_shift_m']=list(shift)
    return COL

def build(out):
    out.mkdir(parents=True,exist_ok=True);col=create();source=ac.audit_source(col,P['budgets']['max_triangles'])
    write(out/'qa/evidence/source.json',source)
    if source['errors']:raise RuntimeError(str(source['errors']))
    bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.filepath='//preview.png'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[P['asset_id']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,
        export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,
        export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,
        export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    missing=set(flags)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if missing:raise RuntimeError('Missing exporter flags '+str(missing))
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    a=audit_glb(out/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives']);a['file']='model.glb'
    write(out/'qa/evidence/glb.json',a)
    if a['errors']:raise RuntimeError(str(a['errors']))
    b=source['bounds_blender_m'];low=[b['min'][0],b['min'][2],-b['max'][1]];high=[b['max'][0],b['max'][2],-b['min'][1]]
    err=max(abs(a['bounds_m'][k][i]-v[i]) for k,v in [('min',low),('max',high)] for i in range(3))
    assert err<.0001 and a['scene_triangles']==source['triangles'] and a['bytes']<=P['budgets']['max_glb_bytes']
    write(out/'qa/evidence/build.json',{'blender':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),
        'glb_sha256':sha(out/'model.glb'),'seed':P['seed'],'export_options':flags,'source_to_export_max_bounds_error_m':err,
        'source_to_export_triangles_equal':True,'consumer_threejs_version':'0.180.0','consumer_gpu_status':'UNKNOWN',
        'authoring_axes':{'up':'+Z','forward':'-Y'},'glb_axes':{'up':'+Y','forward':'+Z'},'origin':'intended floor-contact footprint center',
        'profile':'editable semantic control lofts and voxel-unioned decimated skin; separate closed feet, ears and facial details deliberately overlap; not a print-ready union'})

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--render-only',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);P=json.loads((HERE/'params.json').read_text());out=a.out.resolve()
if not a.render_only:build(out)
if a.gray or a.render:
    from model_render import render_glb
    render_glb(out,gray=a.gray)
