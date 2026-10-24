# SPDX-License-Identifier: MIT
"""Original Glyptodon clavipes reconstruction. Run in Blender with -- --output DIR.
All geometry is authored here, not copied from scans or reference imagery.
The shell dual-cell relief is an artistic low-poly osteoderm abstraction.
"""
from pathlib import Path
import argparse, json, math, sys, hashlib
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,obj): Path(path).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser(); a.add_argument('--output',type=Path,required=True); a.add_argument('--params',type=Path,default=HERE/'params.json'); a.add_argument('--gray',action='store_true'); args=a.parse_args(argv)
P=json.loads(args.params.read_text()); OUT=args.output; OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('glyptodon',P['seed']); mats={k:make_material(k,'#939393' if args.gray else v) for k,v in P['palette'].items()}
root=bpy.data.objects[C['asset_root']]; root['taxon']='Glyptodon clavipes'; root['representation']='living-reconstruction'; root['scientific_limit']='Soft anatomy, color, posture, size and osteoderm simplification are artistic estimates.'

def obj(name,vs,fs,mat): return mesh_object(name,vs,fs,mats[mat],C)
def loft(name,sections,n,mat):
    # Sections are center x/y/z with lateral x and vertical z radii, along Y.
    v=[]; f=[]
    for x,y,z,rx,rz in sections:
        v += [(x+rx*math.cos(2*math.pi*j/n),y,z+rz*math.sin(2*math.pi*j/n)) for j in range(n)]
    f.append(tuple(range(n-1,-1,-1)))
    for k in range(len(sections)-1):
        for j in range(n): f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    f.append(tuple((len(sections)-1)*n+j for j in range(n)))
    return obj(name,v,f,mat)
def ellipsoid_data(center,scale,seg=12,rings=6):
    v=[(center[0],center[1],center[2]+scale[2])]; f=[]
    for k in range(1,rings):
        ph=math.pi*k/rings
        for j in range(seg):
            th=2*math.pi*j/seg
            v.append((center[0]+scale[0]*math.sin(ph)*math.cos(th),center[1]+scale[1]*math.sin(ph)*math.sin(th),center[2]+scale[2]*math.cos(ph)))
    bot=len(v);v.append((center[0],center[1],center[2]-scale[2]))
    for j in range(seg): f.append((0,1+j,1+(j+1)%seg))
    for k in range(rings-2):
        for j in range(seg):
            q=1+k*seg; f.append((q+j,q+seg+j,q+seg+(j+1)%seg,q+(j+1)%seg))
    for j in range(seg): f.append((bot,1+(rings-2)*seg+(j+1)%seg,1+(rings-2)*seg+j))
    return v,f

def ellipsoid(name,c,s,mat,seg=12,rings=6): return obj(name,*ellipsoid_data(c,s,seg,rings),mat)
def combine(parts):
    vs=[];fs=[]
    for v,f in parts:
        n=len(vs);vs+=v;fs += [tuple(n+i for i in face) for face in f]
    return vs,fs

def shell_point(u,offset=0):
    rx,ry,rz=P['shell_radii']; x,y,z=u
    arch=.13*max(0,-y)**8*max(0,1-z)**5
    q=Vector((rx*x,ry*y+P['shell_y_offset'],P['shell_base_z']+rz*z+arch))
    normal=Vector((x/rx,y/ry,z/rz)).normalized()
    return q+normal*offset
# Continuous closed dome, with a gentle raised front rim for the neck exit.
v=[tuple(shell_point((0,0,1)))];f=[];seg=64;rows=16
for k in range(1,rows+1):
    ph=math.pi*.5*k/rows
    for j in range(seg):
        th=2*math.pi*j/seg;v.append(tuple(shell_point((math.sin(ph)*math.cos(th),math.sin(ph)*math.sin(th),math.cos(ph)))))
for j in range(seg): f.append((0,1+j,1+(j+1)%seg))
for k in range(rows-1):
    for j in range(seg):
        q=1+k*seg;f.append((q+j,q+seg+j,q+seg+(j+1)%seg,q+(j+1)%seg))
f.append(tuple(1+(rows-1)*seg+j for j in range(seg-1,-1,-1)))
obj('rigid-domed-carapace',v,f,'shell-seams')
# Dual of an icosphere gives irregularly oriented pentagonal and hexagonal cells,
# not transverse flexible bands. All cells stay in one semantic editable mesh.
if not args.gray:
    bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=P['plate_subdivisions'],radius=1)
    bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table();vs=[];fs=[];mi=[]
    for i,bv in enumerate(bm.verts):
        u=bv.co.normalized()
        if u.z<.035: continue
        t=u.cross(Vector((0,0,1)))
        if t.length<.1:t=u.cross(Vector((1,0,0)))
        t.normalize();b=u.cross(t).normalized()
        centers=[fa.calc_center_median().normalized() for fa in bv.link_faces]
        centers.sort(key=lambda q:math.atan2((q-u).dot(b),(q-u).dot(t)))
        n=len(centers);start=len(vs)
        # Reduced perimeter creates fine recessed mortar lines without open shell.
        lower=[(u+(q-u)*.965).normalized() for q in centers]
        upper=[(u+(q-u)*.82).normalized() for q in centers]
        vs += [tuple(shell_point(q,.002)) for q in lower]
        vs += [tuple(shell_point(q,.011)) for q in upper]
        vs.append(tuple(shell_point(u,.014)))
        fs.append(tuple(start+j for j in range(n-1,-1,-1)));mi.append(0)
        for j in range(n):
            fs.append((start+j,start+(j+1)%n,start+n+(j+1)%n,start+n+j));mi.append(0)
            fs.append((start+n+j,start+n+(j+1)%n,start+2*n));mi.append(1+(i%3))
    bm.free()
    shell=mesh_object('osteoderm-mosaic',vs,fs,[mats[x] for x in ['shell-seams','shell-ochre','shell-warm','shell-muted']],C)
    for face,idx in zip(shell.data.polygons,mi): face.material_index=idx
# Full living body visible only at openings and under-rim.
ellipsoid('living-body',(0,.01,.55),(.51,.71,.29),'skin',20,10)
loft('short-muscular-neck',[(0,-.55,.57,.20,.21),(0,-.77,.57,.18,.19),(0,-.91,.54,.16,.17)],12,'skin')
loft('deep-blunt-head',[(0,-.84,.56,.145,.17),(0,-.98,.54,.182,.205),(0,-1.11,.49,.165,.18),(0,-1.23,.435,.115,.105),(0,-1.27,.43,.09,.075)],12,'skin')
# A brow shield follows the forehead, not an exposed fossil skull.
loft('forehead-shield',[(0,-.86,.694,.10,.034),(0,-.98,.741,.14,.025),(0,-1.10,.657,.13,.025),(0,-1.20,.555,.08,.018)],10,'shell-ochre')
eyes=[];nostrils=[];ears=[]
for side in [-1,1]:
    eyes.append(ellipsoid_data((side*.168,-1.034,.594),(.022,.026,.022),10,6))
    nostrils.append(ellipsoid_data((side*.075,-1.258,.466),(.018,.013,.012),8,4))
    ears.append(ellipsoid_data((side*.18,-.876,.682),(.034,.03,.055),10,6))
obj('small-dark-eyes',*combine(eyes),'dark-features');obj('paired-nostrils',*combine(nostrils),'dark-features');obj('small-ears',*combine(ears),'skin')
# Legs are authored as tapered, bent profiles with planted broad, separated feet.
claws=[]
for side in [-1,1]:
    for front in [True,False]:
        tag=('left' if side<0 else 'right')+('-fore' if front else '-hind')
        y=-.48 if front else .47
        x=side*.405
        # Elliptical cross-sections in horizontal planes for a weight-bearing limb.
        sections=[(side*.33,y,.65,.12,.13),(side*.43,y+.025,.43,.145,.14),(side*.47,y+(.045 if front else .09),.24,.105,.11),(side*.47,y-(.015 if front else .005),.105,.12,.13)]
        lv=[];lf=[];n=12
        for cx,cy,z,rx,ry in sections:
            lv += [(cx+rx*math.cos(2*math.pi*j/n),cy+ry*math.sin(2*math.pi*j/n),z) for j in range(n)]
        lf.append(tuple(range(n-1,-1,-1)))
        for k in range(len(sections)-1):
            for j in range(n):lf.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
        lf.append(tuple((len(sections)-1)*n+j for j in range(n)))
        obj(tag+'-leg',lv,lf,'skin')
        footy=y-.065
        fv,ff=ellipsoid_data((side*.47,footy,.102),(.17,.23,.102),12,6)
        # The low pole is the foot contact, leaving no hidden support or plinth.
        obj(tag+'-foot',fv,ff,'skin')
        for toe in range(4):
            tx=side*.47+(toe-1.5)*.075;ty=footy-.17+abs(toe-1.5)*.025
            claws.append(ellipsoid_data((tx,ty,.054),(.043,.09,.047),8,4))
obj('weight-bearing-toe-claws',*combine(claws),'claws')
# Short tapering tail with complete overlapping annular armor, never a mace.
tail_sections=[(0,.72,.39,.14,.13),(0,.88,.30,.13,.12),(0,1.03,.23,.105,.10),(0,1.17,.175,.077,.075),(0,1.30,.14,.045,.045),(0,1.36,.132,.009,.012)]
loft('short-tail-core',tail_sections,14,'skin')
rv=[];rf=[];rmi=[]
for k in range(8):
    y=.82+k*.067
    for left,right in zip(tail_sections,tail_sections[1:]):
        if left[1]<=y<=right[1]:
            t=(y-left[1])/(right[1]-left[1]);z=left[2]*(1-t)+right[2]*t;rx=(left[3]*(1-t)+right[3]*t)*1.08;rz=(left[4]*(1-t)+right[4]*t)*1.08;break
    start=len(rv);n=14
    for yy,fac in [(y-.032,.90),(y-.022,1.10),(y+.018,1.06),(y+.032,.87)]:
        for j in range(n):
            th=2*math.pi*j/n; scallop=1+.055*(j%2)
            rv.append((rx*fac*math.cos(th)*scallop,yy,z+rz*fac*math.sin(th)*scallop))
    rf.append(tuple(start+j for j in range(n-1,-1,-1)));rmi.append(0)
    for layer in range(3):
        for j in range(n):rf.append((start+layer*n+j,start+layer*n+(j+1)%n,start+(layer+1)*n+(j+1)%n,start+(layer+1)*n+j));rmi.append(1 if layer==1 else 0)
    rf.append(tuple(start+3*n+j for j in range(n)));rmi.append(0)
ring=mesh_object('eight-short-tail-armor-rings',rv,rf,[mats['shell-muted'],mats['shell-ochre']],C)
for face,idx in zip(ring.data.polygons,rmi):face.material_index=idx
# Center the actual four planted foot contacts without moving the identity root.
for part in C.all_objects:
    if part.type=='MESH':
        for vertex in part.data.vertices:vertex.co.y+=P['footprint_translation_y_m']
# No stage, cameras, lights, textures, linked assets, or hidden geometry in source.
bpy.context.view_layer.update(); policy=P['geometry_policy'];source=audit_source(C,policy['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
bpy.context.preferences.filepaths.save_version=0
# Remove factory-session file-browser and render destinations from the saved source.
bpy.context.scene.render.filepath='//preview.png'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'//'
                space.params.filename=''

bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
assert not set(options)-available
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**options)
exported=audit_glb(OUT/'model.glb',policy['max_triangles'],policy['max_materials'],policy['max_primitives']);exported['file']='model.glb'
if exported['errors']:raise RuntimeError(exported['errors'])
assert exported['bytes']<=policy['max_glb_bytes']
write(OUT/'build-audit.json',{'status':'pass','blender_version':bpy.app.version_string,'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'generator_sha256':sha(Path(__file__)),'params_sha256':sha(args.params),'gray_model':args.gray,'export_options':options,'source':source,'glb':exported,'limits':policy,'representation':'living-reconstruction','gpu':'UNKNOWN','scene':'UNKNOWN'})
print('BUILD COMPLETE',exported['scene_triangles'],exported['bytes'])
