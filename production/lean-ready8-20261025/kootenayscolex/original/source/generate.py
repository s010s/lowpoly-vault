# SPDX-License-Identifier: MIT
"""Original Kootenayscolex static animal. Blender 4.3.2; no external content.
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
All shape coordinates below are designed in millimeters, uniformly converted to meters.
"""
from pathlib import Path
import sys, json, hashlib, argparse, math
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P={};C=None;M={};PARTS={};MEASURE={}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def center(y):return Vector((.55*math.sin(2*math.pi*(y+12.5)/25),y,1.12+.06*math.sin(math.pi*(y+12.5)/25)))
def form(t):
    # Broad middle and independently narrowed anterior and posterior silhouette.
    w=.53+1.00*math.sin(math.pi*(.12+.82*t))**.95
    w*=1-.55*t**3
    return w,.57+.22*math.sin(math.pi*t)
def acc(name,verts,faces,mat,smooth=False):
    a=PARTS.setdefault(name,{'v':[],'f':[],'mat':mat,'smooth':smooth})
    n=len(a['v']);a['v'].extend([tuple(v) for v in verts]);a['f'].extend([tuple(n+i for i in f) for f in faces])
def tube(name,points,radii,mat,sides=6,smooth=False):
    pts=[Vector(x) for x in points];vs=[];fs=[];rings=[]
    for k,(p,r) in enumerate(zip(pts,radii)):
        if r==0:rings.append([len(vs)]);vs.append(tuple(p));continue
        tangent=(pts[min(k+1,len(pts)-1)]-pts[max(k-1,0)]).normalized()
        axis=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((0,1,0))
        u=tangent.cross(axis).normalized();v=tangent.cross(u).normalized();ring=[]
        for j in range(sides):
            theta=2*math.pi*j/sides;ring.append(len(vs));vs.append(tuple(p+r*(u*math.cos(theta)+v*math.sin(theta))))
        rings.append(ring)
    for a,b in zip(rings,rings[1:]):
        for j in range(sides):
            if len(a)==1:fs.append((a[0],b[(j+1)%sides],b[j]))
            elif len(b)==1:fs.append((a[j],a[(j+1)%sides],b[0]))
            else:fs.append((a[j],a[(j+1)%sides],b[(j+1)%sides],b[j]))
    if len(rings[0])>1:fs.append(tuple(reversed(rings[0])))
    if len(rings[-1])>1:fs.append(tuple(rings[-1]))
    acc(name,vs,fs,mat,smooth)
def bezier(points,n):
    p=[Vector(x) for x in points];out=[]
    for k in range(n+1):
        t=k/n;out.append((1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t**3*p[3])
    return out
def length(points):return sum((Vector(b)-Vector(a)).length for a,b in zip(points,points[1:]))
def build():
    global C,M,MEASURE
    C=setup_scene(P['asset_id'],P['seed']);M={k:make_material(k,v,roughness=.83) for k,v in P['palette'].items()}
    # One coherent loft from prostomium through twenty trunk bulges to simple pygidium.
    rows=[(-12.5,.10,.14),(-12.36,.45,.40),(-12.03,.78,.59),(-11.6,.96,.65),(-11.15,1.00,.64),(-10.8,.97,.61)]
    start=-10.8;step=22.1/P['trunk_segments']
    for i in range(P['trunk_segments']):
        for f,b in [(0,.90),(.25,1.0),(.60,1.025),(.86,.97)]:
            t=(i+f)/P['trunk_segments'];w,h=form(t);rows.append((start+(i+f)*step,w*b,h*b))
    rows.extend([(11.3,.54,.45),(11.7,.41,.35),(12.1,.25,.23),(12.4,.12,.13),(12.5,.035,.045)])
    # Remove duplicate seam rings before building; head/trunk connection remains continuous.
    rows=[r for i,r in enumerate(rows) if i==0 or abs(r[0]-rows[i-1][0])>1e-8]
    n=16;vs=[];fs=[]
    for y,w,h in rows:
        p=center(y)
        for j in range(n):
            a=2*math.pi*j/n;vs.append(tuple(p+Vector((w*math.cos(a),0,h*math.sin(a)))))
    fs.append(tuple(range(n-1,-1,-1)))
    for i in range(len(rows)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.append(tuple((len(rows)-1)*n+j for j in range(n)))
    acc('continuous-prostomium-20-trunk-segments-pygidium',vs,fs,[M['dorsal'],M['ventral']],True)
    for i in range(P['trunk_segments']):
        t=(i+.48)/P['trunk_segments'];y=start+(i+.48)*step;p=center(y);w,h=form(t)
        # The appendage length also tapers. The wider ventral fans sit below the dorsal fans.
        extent=2.5*(.62+.38*math.sin(math.pi*t))*(1-.35*t**4)
        for sign,side in [(-1,'left'),(1,'right')]:
            for row,zfactor,spread,count in [('dorsal',.61,.39,P['dorsal_chaetae_per_fan']),('ventral',-.37,.65,P['ventral_chaetae_per_fan'])]:
                root=p+Vector((sign*w*.80,0,zfactor*h))
                outer=p+Vector((sign*(w+.40),.10,zfactor*h+(0.10 if row=='dorsal' else -.13)))
                mid=(root+outer)/2
                tube(f'{side}-{row}-parapodial-lobes',[root,mid,outer],[.21,.24,.125],M['parapodia'],6,True)
                for j in range(count):
                    a=-spread+2*spread*j/(count-1)
                    base=outer+Vector((-sign*.07,(j-(count-1)/2)*.022,0))
                    dx=extent*math.cos(a)*(1.0 if row=='ventral' else .82)
                    dy=extent*math.sin(a)+(.16 if row=='ventral' else .07)
                    zend=(.13+.12*(j/(count-1))) if row=='ventral' else outer.z+1.35+.32*(1-abs(a)/spread)
                    tip=Vector((outer.x+sign*dx,outer.y+dy,zend))
                    m=base+(tip-base)*.60;m.z+=.10
                    tube(f'{side}-{row}-chaetal-fans',[base,m,tip],[.036,.020,0],M['chaetae'],3,False)
    # Pair of long flexible palps, with coherent curved centerlines and gently tapered tips.
    palp_lengths=[]
    for sign,side in [(-1,'left'),(1,'right')]:
        pts=bezier([(sign*.47,-12.0,1.51),(sign*2.6,-14.4,2.3),(sign*5.5,-19.9,.80),(sign*3.7,-21.1,1.08)],18)
        radii=[.245*(1-k/18)**.7+.012 for k in range(19)];radii[-1]=0
        tube(f'{side}-long-sensory-palp',pts,radii,M['palps'],8,True);palp_lengths.append(length(pts))
    antenna=bezier([(0,-12.05,1.65),(.02,-12.45,1.99),(.03,-12.91,2.12),(.0,-13.18,2.14)],8)
    tube('short-median-antenna',antenna,[.11*(1-k/8)+.009 for k in range(8)]+[0],M['palps'],6,True)
    # A separate head pair next to the modest ventral oral area; no eyes or jaws.
    for sign,side in [(-1,'left'),(1,'right')]:
        root=Vector((sign*.64,-12.0,.94));outer=Vector((sign*1.12,-12.24,.91))
        tube(f'{side}-head-parapodium',[root,(root+outer)/2,outer],[.22,.25,.12],M['parapodia'],6,True)
        for j in range(P['head_chaetae_per_side']):
            a=-.62+1.24*j/(P['head_chaetae_per_side']-1)
            tip=Vector((outer.x+sign*(1.90*math.cos(a)),outer.y-1.15+1.9*math.sin(a),.4+.17*j))
            tube(f'{side}-head-chaetae',[outer,(outer+tip)/2,tip],[.034,.019,0],M['chaetae'],3)
    # Small recessed-looking ventral oral field, not an invented jaw apparatus.
    tube('modest-ventral-oral-field',[(0,-12.23,.64),(0,-12.35,.67),(0,-12.40,.72)],[.16,.145,0],M['oral'],8,True)
    centerline=[center(-12.5+25*i/1000) for i in range(1001)]
    factor=P['body_length_m']/length(centerline)
    for name,a in PARTS.items():
        o=mesh_object(name,[tuple(Vector(v)*factor) for v in a['v']],a['f'],a['mat'],C)
        for f in o.data.polygons:f.use_smooth=a['smooth']
        if name.startswith('continuous'):
            for f in o.data.polygons:
                f.material_index=1 if f.normal.z<-.38 else 0
        o['semantic_role']=name;o['original_geometry']=True
    low=min(v.co.z for o in C.all_objects if o.type=='MESH' for v in o.data.vertices)
    for o in C.all_objects:
        if o.type=='MESH':
            for v in o.data.vertices:v.co.z-=low
    bpy.context.view_layer.update()
    MEASURE={'body_centerline_m':length(centerline)*factor,'body_axis_length_m':25*factor,'palp_centerline_lengths_m':[x*factor for x in palp_lengths],'median_antenna_centerline_m':length(antenna)*factor,'trunk_segments':20,'dorsal_strands_per_fan':3,'ventral_strands_per_fan':4,'head_strands_per_side':5,'uniform_mm_to_m_factor':factor,'floor_shift_m':-low,'excluded_from_body_length':['palps','antenna','chaetae'],'body_centerline_measurement':'1000-interval sampling of authored gentle S centerline; projected axial body length recorded separately.'}
    C['body_centerline_m']=P['body_length_m'];C['segment_count']=20
    return C
def main():
    global P
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    P=json.loads((HERE/'params.json').read_text());col=build();policy=P['geometry_policy'];tol=P['technical_tolerances']
    source=audit_source(col,policy['max_triangles'],tol['triangle_area_m2'],tol['contact_m'])
    source['authored_vertices']=sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH');source['evaluated_vertices']=source['authored_vertices']
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene.render.filepath='//';bpy.context.scene['generator']='source/generate.py';bpy.context.scene['reconstruction_scope']=P['interpretation'];bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(flags)-available:raise RuntimeError('Missing exporter options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    glb=audit_glb(out/'model.glb',policy['max_triangles'],policy['max_materials'],policy['max_primitives'],tol['contact_m'],tol['triangle_area_m2']);glb['file']='model.glb'
    b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][s][i]-e[i]) for s,e in [('min',emin),('max',emax)] for i in range(3))
    if glb['errors'] or delta>tol['bounds_delta_m'] or source['triangles']!=glb['scene_triangles'] or glb['bytes']>policy['max_glb_bytes']:raise RuntimeError('Source/export audit failed: '+str(glb['errors']))
    import io_scene_gltf2
    dump(out/'technical.json',{'asset_id':P['asset_id'],'revision':P['revision'],'source':source,'glb':glb,'source_export_bounds_delta_m':delta,'tolerances':tol,'tolerance_rationale':'25 mm body: bounds/contact tolerance 1e-6 of body length; degeneracy threshold 1e-16 m2 resolves narrow finite chaetae while rejecting collapsed faces. No asset enlargement.','blender_version':bpy.app.version_string,'exporter_version':io_scene_gltf2.bl_info['version'],'consumer_three_version':'0.180.0','consumer_scope':'CPU parse separately; GPU and world scene UNKNOWN','export_options':flags,'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(out/'model.blend'),'measurements':MEASURE,'interpretation':P['interpretation'],'warning_review':'Smooth faces on the body, fleshy parapodia, palps and antenna are intentional low-sided soft anatomy. Chaetae are flat closed triangular solids. Embedded anatomical attachments are overlapping closed shells, not a Boolean union; no watertight print claim.'})
if __name__=='__main__':main()
