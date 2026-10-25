# SPDX-License-Identifier: MIT
"""Original deterministic static Dunkleosteus reconstruction. Blender 4.3.2.
Rebuild: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
No external content, textures, randomness, rig, simulation or presentation objects.
"""
from pathlib import Path
import sys, json, hashlib, argparse, math
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P={}; C=None; M={}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def mesh(name,vs,fs,mat):return mesh_object(name,vs,fs,mat,C)

def loft(name,rows,materials,segments=24,head=False):
    # Longitudinal rings carry deliberate changing width, dorsal and ventral profiles.
    vs=[];fs=[]
    for y,w,lo,hi in rows:
        for j in range(segments):
            t=2*math.pi*j/segments
            z=(hi+lo)/2+(hi-lo)/2*math.sin(t)
            # Broad armor crown, not spherical head primitives.
            x=w*math.cos(t)*(1.0 if not head else (1-.08*max(0,math.sin(t))))
            # The head joint sweeps obliquely: dorsally posterior, ventrally anterior.
            # This prevents an artificial transverse collar while preserving the gill cleft.
            joint_weight=0
            if name=='cranial-shield-and-cheeks':joint_weight=max(0,min(1,(y+1.25)/.35))
            elif name=='gill-opening-and-cranio-thoracic-joint':joint_weight=1
            elif name=='continuous-stocky-trunk-and-caudal-peduncle':joint_weight=max(0,1-(y+.86)/.45)
            yy=y+.105*math.sin(t)*joint_weight
            vs.append((x,yy,z))
    fs.append(tuple(range(segments-1,-1,-1)))
    for i in range(len(rows)-1):
        for j in range(segments):fs.append((i*segments+j,i*segments+(j+1)%segments,(i+1)*segments+(j+1)%segments,(i+1)*segments+j))
    fs.append(tuple((len(rows)-1)*segments+j for j in range(segments)))
    o=mesh(name,vs,fs,materials)
    if isinstance(materials,list) and len(materials)>1:
        for p in o.data.polygons:
            # Color region follows ventral anatomy, not random face assignment.
            p.material_index=1 if p.center.z < .64 and p.normal.z<-.25 else 0
    return o

def ellipsoid(name,center,radii,mat,n=14,m=7):
    vs=[(center[0],center[1],center[2]-radii[2])];fs=[]
    for k in range(1,m):
        a=-math.pi/2+math.pi*k/m
        for j in range(n):
            t=2*math.pi*j/n
            vs.append((center[0]+radii[0]*math.cos(a)*math.cos(t),center[1]+radii[1]*math.cos(a)*math.sin(t),center[2]+radii[2]*math.sin(a)))
    vs.append((center[0],center[1],center[2]+radii[2]));end=len(vs)-1
    for j in range(n):fs.append((0,1+(j+1)%n,1+j))
    for k in range(m-2):
        for j in range(n):a=1+k*n+j;b=1+k*n+(j+1)%n;fs.append((a,b,b+n,a+n))
    for j in range(n):fs.append((end,end-n+j,end-n+(j+1)%n))
    return mesh(name,vs,fs,mat)

def fin(name,outline,center,thickness,axis,mat):
    # Closed tapered foil with a subtle internal camber ridge; one semantic editable mesh.
    vs=[];fs=[];n=len(outline)
    for side in [-1,1]:
        p=list(center);p[axis]+=side*thickness;vs.append(tuple(p))
        for pt in outline:
            q=list(pt);q[axis]+=side*.003;vs.append(tuple(q))
    for k in range(2):
        base=k*(n+1)
        for j in range(n):fs.append((base,base+1+j,base+1+(j+1)%n))
    for j in range(n):fs.append((1+j,1+(j+1)%n,n+2+(j+1)%n,n+2+j))
    return mesh(name,vs,fs,mat)

def plate(name,outline,sign,width,mat):
    # A solid, curved cutting plate extruded laterally; not individual conical teeth.
    vs=[];fs=[];n=len(outline)
    for d in [-width/2,width/2]:
        for x,y,z in outline:vs.append((sign*(x+d),y,z))
    fs += [tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    for j in range(n):fs.append((j,(j+1)%n,(j+1)%n+n,j+n))
    return mesh(name,vs,fs,mat)

def build():
    global C,M
    C=setup_scene('dunkleosteus',P['seed'])
    M={k:make_material(k,v,roughness=.82 if k not in ['gnathal','eye'] else .62) for k,v in P['surface']['palette_srgb'].items()}
    bodyrows=[(-.86,.34,.55,1.33),(-.77,.42,.49,1.43),(-.61,.49,.44,1.49),(-.41,.52,.43,1.51),(-.18,.515,.44,1.50),(.04,.49,.47,1.45),(.25,.44,.53,1.37),(.46,.37,.61,1.27),(.66,.29,.69,1.17),(.84,.22,.76,1.08),(1.02,.16,.80,1.02),(1.18,.11,.81,.99),(1.30,.085,.82,.99)]
    body=loft('continuous-stocky-trunk-and-caudal-peduncle',bodyrows,[M['body'],M['underside']])
    body.data.materials.append(M['armor'])
    for f in body.data.polygons:
        if f.center.y<(-.22+.20*f.normal.z) and f.material_index==0:f.material_index=2
    # Head is its own moving-anatomy volume, with deep posterior cheeks and low snout.
    head=loft('cranial-shield-and-cheeks',[(-1.65,.16,.985,1.07),(-1.60,.24,.97,1.16),(-1.48,.315,.92,1.26),(-1.32,.37,.81,1.34),(-1.13,.395,.65,1.38),(-.96,.37,.56,1.32),(-.90,.33,.59,1.30)],M['armor'],24,True)
    # Separate soft tissue at the head/trunk articulation. Narrow visible gill cleft.
    joint=loft('gill-opening-and-cranio-thoracic-joint',[(-.915,.315,.60,1.29),(-.875,.335,.56,1.32),(-.835,.34,.55,1.31)],[M['armor'],M['cavity']],24)
    for face in joint.data.polygons:
        face.material_index=1 if abs(face.normal.x)>.40 and face.center.z<1.23 else 0
    # Anatomical plate regions, with restrained contrast and no raised decorative trim.
    head.data.materials.append(M['armor_ridge'])
    for face in head.data.polygons:
        if face.normal.z>.72 and face.center.y> -1.45:face.material_index=1
    # Lower jaw curves back into the cheek, leaving a real mouth opening at the snout.
    loft('lower-jaw-skin',[(-1.64,.135,.60,.67),(-1.59,.225,.57,.70),(-1.46,.29,.55,.71),(-1.28,.32,.54,.69),(-1.10,.30,.55,.70),(-.98,.24,.58,.73)], [M['underside'],M['underside']],20)
    ellipsoid('mouth-recess',(0,-1.35,.755),(.245,.28,.095),M['cavity'],20,8)
    # Two upper gnathals with a prominent anterior cusp and one continuous cutting margin.
    upper=[(.15,-1.64,1.025),(.215,-1.57,1.00),(.268,-1.45,.94),(.29,-1.31,.85),(.26,-1.28,.80),(.23,-1.42,.865),(.18,-1.56,.89),(.15,-1.615,.805)]
    lower=[(.16,-1.645,.69),(.17,-1.625,.79),(.205,-1.56,.73),(.258,-1.44,.715),(.285,-1.30,.735),(.277,-1.25,.69),(.245,-1.45,.645),(.16,-1.62,.63)]
    for s in [-1,1]:
        plate('upper-gnathal-'+str(s),upper,s,.035,M['gnathal'])
        plate('lower-gnathal-'+str(s),lower,s,.035,M['gnathal'])
        # Eye sockets embedded in cranial surface; small exposed eye and pupil, no stalk.
        yy=-1.43;zz=1.157
        hit,loc,n,idx=head.ray_cast(Vector((s*1,yy,zz)),Vector((-s,0,0)))
        if not hit:raise RuntimeError('Eye surface not found')
        ellipsoid('orbital-rim-'+str(s),(loc.x-s*.012,yy,zz),(.030,.079,.066),M['cavity'],16,8)
        ellipsoid('eye-'+str(s),(loc.x+s*.010,yy-.007,zz),(.022,.050,.045),M['eye'],16,8)
        ellipsoid('pupil-'+str(s),(loc.x+s*.027,yy-.014,zz),(.009,.025,.030),M['cavity'],12,6)
        # Large paired anterior pectorals, swept gently backward from ventrolateral armor.
        fin('pectoral-fin-'+str(s),[(s*.16,-.80,.78),(s*.53,-.68,.56),(s*.84,-.31,.36),(s*.93,-.02,.23),(s*.90,.10,.22),(s*.70,.02,.33),(s*.49,-.23,.45),(s*.20,-.45,.65)],(s*.62,-.37,.44),.035,2,M['fin'])
        fin('pelvic-fin-'+str(s),[(s*.15,.41,.78),(s*.39,.51,.56),(s*.46,.76,.49),(s*.38,.80,.55),(s*.09,.67,.83)],(s*.34,.64,.60),.018,2,M['fin'])
    # Posterior fin outlines are explicit reconstruction choices rather than preserved anatomy.
    fin('dorsal-fin',[(0,-.03,1.45),(0,.15,1.66),(0,.24,1.98),(0,.31,2.00),(0,.42,1.91),(0,.60,1.57),(0,.80,1.18),(0,.93,1.07),(0,.56,1.24)],(0,.38,1.54),.035,0,M['fin'])
    fin('anal-fin',[(0,.62,.71),(0,.83,.60),(0,1.00,.55),(0,.95,.72),(0,1.09,.82)],(0,.86,.72),.020,0,M['fin'])
    fin('caudal-fin',[(0,1.19,.96),(0,1.31,1.14),(0,1.49,1.43),(0,1.73,1.66),(0,1.75,1.65),(0,1.61,1.36),(0,1.50,1.07),(0,1.47,.87),(0,1.58,.53),(0,1.69,.27),(0,1.67,.24),(0,1.45,.46),(0,1.24,.75),(0,1.19,.83)],(0,1.36,.94),.045,0,M['fin'])
    # Normalize only to the explicitly selected metric total length, not a gallery box.
    allvs=[v for o in C.all_objects if o.type=='MESH' for v in o.data.vertices]
    low=min(v.co.z for v in allvs); ymin=min(v.co.y for v in allvs); ymax=max(v.co.y for v in allvs)
    factor=P['nominal_total_length_m']/(ymax-ymin)
    for v in allvs:v.co=Vector((v.co.x*factor,v.co.y*factor,(v.co.z-low)*factor))
    C['centerline_m']=(.94-low)*factor
    bpy.context.view_layer.update()
    return C

def main():
    global P
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    P=json.loads((HERE/'params.json').read_text());col=build();policy=P['geometry_policy']
    source=audit_source(col,policy['max_triangles'])
    source['authored_vertices']=sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH')
    source['evaluated_vertices']=source['authored_vertices']
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene.render.filepath='//';bpy.context.scene['generator']='source/generate.py'
    bpy.context.scene['scientific_scope']=P['interpretation']
    bpy.context.preferences.filepaths.save_version=0
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
    if set(flags)-available:raise RuntimeError('Missing glTF exporter options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    glb=audit_glb(out/'model.glb',policy['max_triangles'],policy['max_materials'],policy['max_primitives']);glb['file']='model.glb'
    b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][s][i]-e[i]) for s,e in [('min',emin),('max',emax)] for i in range(3))
    if glb['errors'] or delta>1e-4 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>policy['max_glb_bytes']:raise RuntimeError('Source/export audit failed: '+str(glb['errors']))
    import io_scene_gltf2
    dump(out/'technical.json',{'asset_id':'dunkleosteus','revision':'r001','source':source,'glb':glb,'source_export_bounds_delta_m':delta,'blender_version':bpy.app.version_string,'exporter_version':io_scene_gltf2.bl_info['version'],'consumer_three_version':'0.180.0','consumer_scope':'version pin only until separate parser test; GPU not tested','export_options':flags,'source_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(out/'model.blend'),'water_placement_centerline_m':col['centerline_m'],'anatomical_scope':P['interpretation'],'semantic_parts':'Continuous original trunk/peduncle, cranial shield/cheeks, separate joint, lower jaw, paired solid gnathals, embedded eyes and closed cambered fins. Static, no rig or swim behavior.'})
if __name__=='__main__':main()
