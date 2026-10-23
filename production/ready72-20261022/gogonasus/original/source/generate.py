# SPDX-License-Identifier: MIT
"""Original Gogonasus skull study. Blender 4.3.2; no external scene or images required.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
All construction is parametric millimeters, converted once to meters before export.
"""
import bpy, bmesh, sys, math, json, hashlib, argparse
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,required=True); args=ap.parse_args(argv)
out=args.out.resolve(); out.mkdir(parents=True,exist_ok=True)
coll=setup_scene(P['asset_id'],P['seed']); root=bpy.data.objects[coll['asset_root']]
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
mats=[make_material(n,c,roughness=.87) for n,c in zip(['Dermal bone ivory','Slightly darker jaw and panels','Fine pale dentition','Subtle panel lines'],P['palette_srgb'])]
# y, half-width, lateral lower margin, midline height above lower margin.
PROF=P['cranial_profile_mm']
def interp(y):
    for a,b in zip(PROF,PROF[1:]):
        if y<=b[0]:
            t=max(0,min(1,(y-a[0])/(b[0]-a[0])))
            return tuple(a[i]*(1-t)+b[i]*t for i in (1,2,3))
    return PROF[-1][1:]
def surf(y,t):
    w,z,h=interp(y)
    # Slight deliberate profile irregularity, mirrored, not copied specimen fractures.
    return Vector((w*math.sin(t),y-3.0*math.sin(t)**2*max(0,(y-19)/8.5)**2,z+h*math.cos(t)))
def top_at(x,y):
    w,z,h=interp(y)
    return z+h*math.sqrt(max(0,1-(x/w)**2))
N=P['roof_longitudinal_segments']; M=P['roof_cross_segments']; thick=P['shell_thickness_mm']
verts=[]; faces=[]
for layer in (0,1):
    for j in range(N+1):
        y=-27.5+55*j/N
        for k in range(M+1):
            t=-math.pi/2+math.pi*k/M
            v=surf(y,t)
            if layer:
                v-=Vector((math.sin(t),0,math.cos(t)))*min(thick,interp(y)[0]*.55)
            verts.append(tuple(v))
stride=(N+1)*(M+1)
def ix(l,j,k): return l*stride+j*(M+1)+k
for l in (0,1):
    for j in range(N):
        for k in range(M):
            f=(ix(l,j,k),ix(l,j+1,k),ix(l,j+1,k+1),ix(l,j,k+1)); faces.append(f if l==0 else f[::-1])
for j in range(N):
    for k in (0,M): faces.append((ix(0,j,k),ix(0,j+1,k),ix(1,j+1,k),ix(1,j,k)))
for j in (0,N):
    for k in range(M): faces.append((ix(0,j,k),ix(0,j,k+1),ix(1,j,k+1),ix(1,j,k)))
skull=mesh_object('Dermal cranial vault and cheeks',verts,faces,mats[:2],coll)
# A large cheek plate is mildly distinguished; no high-contrast patchwork.
for f in skull.data.polygons:
    c=f.center
    f.material_index=int(abs(c.x)>10 and c.y>1 and c.z<17)

def prism(name, cx,cy, rx,ry, z0=-4,z1=40,n=32):
    v=[(cx+rx*math.cos(2*math.pi*i/n),cy+ry*math.sin(2*math.pi*i/n),z) for z in (z0,z1) for i in range(n)]
    f=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh_object(name,v,f,mats[0],coll)
def cut(obj,cutter):
    bpy.context.view_layer.objects.active=obj
    m=obj.modifiers.new('Real through aperture','BOOLEAN'); m.operation='DIFFERENCE'; m.solver='EXACT'; m.object=cutter
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
def oblique_prism(name,cx,cy,rx,ry,axis,depth=13,n=32):
    normal=Vector(axis).normalized(); u=Vector((0,1,0));v=normal.cross(u)
    center=Vector((cx,cy,top_at(cx,cy)))
    vv=[tuple(center+normal*d+u*ry*math.cos(math.tau*i/n)+v*rx*math.sin(math.tau*i/n)) for d in (-depth/2,depth/2) for i in range(n)]
    ff=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh_object(name,vv,ff,mats[0],coll)
for side in (-1,1):
    q=P['orbit'];cut(skull,oblique_prism('Orbital cutting tool',side*q['center_x_abs_mm'],q['center_y_mm'],*q['radius_xy_mm'],(side*.80,0,.60),depth=8))
    q=P['spiracle'];cut(skull,oblique_prism('Spiracular cutting tool',side*q['center_x_abs_mm'],q['center_y_mm'],*q['radius_xy_mm'],(side*.62,0,.785),depth=15))
    cut(skull,prism('Anterior narial cutting tool',side*6.4,-23.4,.65,.9,n=16))
# Clean exact-Boolean triangulation without changing aperture geometry.
bm=bmesh.new();bm.from_mesh(skull.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.025)
bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.015)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bmesh.ops.triangulate(bm,faces=list(bm.faces))
# Exact-Boolean intersections can leave sub-0.000101 mm2 sliver triangles.
# Collapse only their shortest edges, bounded below 0.15 mm, then recheck.
sliver_collapses=0
for _ in range(24):
    tiny=[f for f in bm.faces if f.calc_area()<.000101]
    if not tiny:break
    edge=min(tiny[0].edges,key=lambda e:e.calc_length())
    if edge.calc_length()>.15:raise RuntimeError('Unexpected non-local Boolean sliver')
    bmesh.ops.collapse(bm,edges=[edge],uvs=False);sliver_collapses+=1
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.00001)
assert not [f for f in bm.faces if f.calc_area()<.000101]
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(skull.data);bm.free();skull.data.update()
skull['anatomical_scope']='External dermal skull; both orbital openings and posterodorsal spiracular notches are actual missing surface.'
# The anterior upper arcade is bridged by a substantial premaxillary symphysis,
# rather than leaving the open underside of the loft as a false median notch.
pre_v=[];pre_f=[];ns=16
for y in (-27.52,-26.0):
    w,z,h=interp(max(-27.5,y))
    for k in range(ns+1):
        t=-math.pi/2+math.pi*k/ns;pre_v.append((w*math.sin(t),y,z+h*math.cos(t)))
pre_f.append(tuple(range(ns,-1,-1)));pre_f.append(tuple(ns+1+k for k in range(ns+1)))
for k in range(ns+1):
    j=(k+1)%(ns+1);pre_f.append((k,j,ns+1+j,ns+1+k))
mesh_object('Premaxillary anterior symphysis',pre_v,pre_f,mats[0],coll)
# Spiracular lamina: each surviving medial/fore rim turns inward/down ~3 mm.
# Partial U, not a ring pasted over a filled black disk; open lateral/posterior notch remains.
for side in (-1,1):
    vv=[];ff=[];q=P['spiracle'];cx=q['center_x_abs_mm'];cy=q['center_y_mm'];rx,ry=q['radius_xy_mm']
    normal=Vector((.62,0,.785)).normalized(); u=Vector((0,1,0));v=normal.cross(u);center=Vector((cx,cy,top_at(cx,cy)))
    # Medial half of the real aperture: curved rim intersects the skull surface.
    angles=[math.radians(i*180/24) for i in range(25)]
    for a in angles:
        p0=center+u*ry*math.cos(a)+v*rx*math.sin(a)
        w,zb,h=interp(p0.y)
        A=(normal.x/w)**2+(normal.z/h)**2
        B=2*(p0.x*normal.x/w**2+(p0.z-zb)*normal.z/h**2)
        C=(p0.x/w)**2+((p0.z-zb)/h)**2-1
        disc=max(0,B*B-4*A*C);lam=(-B+math.sqrt(disc))/(2*A);p=p0+normal*lam
        radial=(u*math.cos(a)+v*math.sin(a)).normalized()
        for off in (radial*.30, -normal*2.6, -normal*2.6+radial*.65,radial*.65):
            pp=p+off;vv.append((side*pp.x,pp.y,pp.z))
    for j in range(len(angles)-1):
        for k in range(4):ff.append((j*4+k,(j+1)*4+k,(j+1)*4+(k+1)%4,j*4+(k+1)%4))
    ff.extend([(3,2,1,0),tuple((len(angles)-1)*4+k for k in range(4))])
    o=mesh_object(('Left' if side<0 else 'Right')+' downturned spiracular lamina',vv,ff,mats[1],coll)
    o['reconstruction']='Simplified folded medial bony margin; CT-specific architecture not reproduced.'
# Broad posterior dermal cheek plates, bulged profile, attached to the vault.
# These overlap the shell at the upper edge as anatomical solid components.
for side in (-1,1):
    outline=[(13.0,-1,16.0),(14.6,4,17.3),(14.9,11,17.5),(13.7,18,17.0),(11.2,23.5,13.0),(9.0,22.5,8.3),(10.1,18,6.6),(12.4,9,6.7),(13.9,2,9.6)]
    outline=[(interp(y)[0]*math.sqrt(max(0,1-((z-interp(y)[1])/interp(y)[2])**2))+.08,y,z) for _,y,z in outline]
    cy=11.0;cz=12.0;w,zb,h=interp(cy);center=Vector((w*math.sqrt(1-((cz-zb)/h)**2)+.30,cy,cz)); vv=[(side*x,y,z) for x,y,z in outline]
    vv.append((side*center.x,center.y,center.z)); n=len(outline)
    vv.extend([(side*(x-1.2),y,z) for x,y,z in outline]);vv.append((side*(center.x-1.2),center.y,center.z))
    ff=[]
    for i in range(n):
        k=(i+1)%n;ff.extend([(i,k,n),(n+1+k,n+1+i,2*n+1),(i,n+1+i,n+1+k,k)])
    mesh_object(('Left' if side<0 else 'Right')+' broad posterior cheek plate',vv,ff,mats[1],coll)
# Continuous substantial U-shaped lower jaw, tapered anterior symphysis.
ys=[24,21,17,12,7,2,-3,-8,-13,-18,-22,-25,-26.6]
path=[]
for y in ys:
    w,z,h=interp(y);path.append(Vector((-max(.6,w-.55),y,0)))
path.append(Vector((0,-27.15,0)))
for y in reversed(ys):
    w,z,h=interp(y);path.append(Vector((max(.6,w-.55),y,0)))
def jaw_z(y):
    if y<-18:
        t=(-18-y)/9.15;return (7.1+2.2*t,1.5+5.8*t)
    if y>8:
        t=(y-8)/16;return (7.1+3.5*t,1.1+4.4*t)
    return (7.1, .10+1.4*((y+4)/22)**2)
v=[];f=[]
for i,p in enumerate(path):
    tan=(path[min(i+1,len(path)-1)]-path[max(0,i-1)]).normalized()
    inward=Vector((-tan.y,tan.x,0))
    if inward.dot(Vector((-p.x,-p.y,0)))<0: inward=-inward
    top,bottom=jaw_z(p.y)
    for d,z in ((-.15,top-.45),(.65,top),(2.0,top-.5),(2.15,bottom+1.0),(.8,bottom),(-.25,bottom+.6),(-.90,(top+bottom)/2),(-.65,top-1.5)):
        q=p+inward*d;v.append((q.x,q.y,z))
for i in range(len(path)-1):
    for k in range(8):f.append((i*8+k,(i+1)*8+k,(i+1)*8+(k+1)%8,i*8+(k+1)%8))
f.extend([tuple(range(7,-1,-1)),tuple((len(path)-1)*8+k for k in range(8))])
jaw=mesh_object('Continuous mandibular rami and anterior symphysis',v,f,mats[1],coll)
# Small original tapered teeth, integrated into upper and lower jaw margins.
def teeth_mesh(upper):
    V=[];F=[]
    for s in (-1,1):
        for j,y in enumerate([-27.2,-26.7,-26.1,-25.4]+[-24.6+k*35.5/29 for k in range(30)]):
            w,base,h=interp(y)
            if upper: p=Vector((s*max(.12,w-.40),y,base+.10));direction=Vector((-s*.10,-.12,-1)).normalized();length=.95+.24*math.sin(j*1.7)**2
            else: p=Vector((s*max(.12,w-1.20),y,jaw_z(y)[0]-.18));direction=Vector((-s*.06,-.08,1)).normalized();length=.78+.24*math.sin(j*1.3)**2
            radius=.19+(.045 if j%4==0 else 0)
            # Slightly oval bases avoid a beaded gum-line.
            a=direction.cross(Vector((0,1,0))).normalized(); b=direction.cross(a)
            q=len(V)
            for r in range(6): V.append(tuple(p+radius*(a*math.cos(r*math.tau/6)+b*math.sin(r*math.tau/6))))
            V.append(tuple(p+direction*length));F.append(tuple(q+i for i in range(5,-1,-1)))
            for r in range(6):F.append((q+r,q+(r+1)%6,q+6))
    return mesh_object(('Upper' if upper else 'Lower')+' fine tooth fringe',V,F,mats[2],coll)
teeth_mesh(True);teeth_mesh(False)
# Restrained low-relief seams. These are simplified study panel divisions, not a
# claim that every fracture in the specimen is a named suture.
seam_paths=[ [(-22,0),(-18,4),(-13,0),(-9,3),(-4,0),(1,0)],
             [(-5,0),(-5,16),(-3,28),(-2,42),(-4,55),(-3,70)],
             [(6,0),(7,17),(5,29),(7,40),(5,57),(9,70),(10,88)],
             [(18,0),(16,18),(17,30)],
             [(-24,60),(-20,62),(-18,70),(-12,72),(-7,69),(-4,71),(0,82)],
             [(0,82),(3,67),(6,62),(10,62),(12,73),(17,77),(21,82)] ]
VV=[];FF=[]
def seam_point(y,deg):
    t=math.radians(deg);p=surf(y,t);return p+Vector((math.sin(t),0,math.cos(t)))*.045
for side in (-1,1):
    for path_index,coords in enumerate(seam_paths):
        if path_index==0 and side<0:continue
        points=[]
        for (ya,ta),(yb,tb) in zip(coords,coords[1:]):
            length=(surf(ya,math.radians(ta))-surf(yb,math.radians(tb))).length
            nn=max(2,math.ceil(length/.9))
            for j in range(nn):
                t=j/nn;points.append(seam_point(ya*(1-t)+yb*t,side*(ta*(1-t)+tb*t)))
        points.append(seam_point(coords[-1][0],side*coords[-1][1]))
        for a,b in zip(points,points[1:]):
            mid=(a+b)/2
            avoid=False
            for hole in [P['orbit'],P['spiracle']]:
                rx,ry=hole['radius_xy_mm'];nx,nz=(.80,.60) if hole is P['orbit'] else (.62,.785)
                c=Vector((hole['center_x_abs_mm'],hole['center_y_mm'],top_at(hole['center_x_abs_mm'],hole['center_y_mm'])))
                d=Vector((abs(mid.x),mid.y,mid.z))-c
                if ((-nz*d.x+nx*d.z)/(rx+.25))**2+(d.y/(ry+.25))**2<1.0:avoid=True
            if avoid:continue
            axis=(b-a).normalized();u=axis.cross(Vector((0,0,1)))
            if u.length<.01:u=Vector((1,0,0))
            u.normalize();v=axis.cross(u).normalized();q=len(VV)
            for p in (a,b):
                for k in range(4):VV.append(tuple(p+(u*math.cos(k*math.tau/4)+v*math.sin(k*math.tau/4))*.065))
            FF.extend([(q+k,q+(k+1)%4,q+4+(k+1)%4,q+4+k) for k in range(4)])
            FF.extend([(q+3,q+2,q+1,q),(q+4,q+5,q+6,q+7)])
seams=mesh_object('Simplified dermal panel relief',VV,FF,mats[3],coll)
seams['limits']='Subdued artistic simplification of panel pattern; not scan-exact sutural tracing.'
# Orient each closed connected solid outward, including the concave U-shaped jaw.
# Consistent edge winding alone does not prove outward normals.
for obj in coll.all_objects:
    if obj.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(obj.data);remaining=set(bm.faces)
    while remaining:
        first=remaining.pop();group=[first];todo=[first]
        while todo:
            face=todo.pop()
            for edge in face.edges:
                for other in edge.link_faces:
                    if other in remaining:remaining.remove(other);todo.append(other);group.append(other)
        vol=0
        for f in group:
            vv=[v.co.copy() for v in f.verts]
            for i in range(1,len(vv)-1):vol+=vv[0].dot(vv[i].cross(vv[i+1]))/6
        if vol<0:bmesh.ops.reverse_faces(bm,faces=group)
    bm.to_mesh(obj.data);bm.free();obj.data.update()
# Scale every vertex once, preserving identity transforms and original meter size.
for obj in coll.all_objects:
    if obj.type=='MESH':
        for v in obj.data.vertices:v.co*=.001
        obj.data.update()
# Ground center on minimum jaw point; center length envelope on origin.
bpy.context.view_layer.update()
low=min((o.matrix_world@v.co).z for o in coll.all_objects if o.type=='MESH' for v in o.data.vertices)
for o in coll.all_objects:
    if o.type=='MESH':
        for v in o.data.vertices:v.co.z-=low
root['scale_note']=P['scale_note']; root['species']='Gogonasus andrewsae';root['reconstruction']='Original skull study, bilateral inference, simplified seams; not a scan.'
source=audit_source(coll,P['max_triangles'])
if source['errors']:
    (out/'source-qa-failed.json').write_text(json.dumps(source,indent=2));raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in coll.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties};assert not(set(options)-available)
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(out/'model.glb',P['max_triangles'],P['max_materials'],P['max_primitives'])
assert not glb['errors'],glb['errors'];assert glb['bytes']<=P['max_glb_bytes']
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][s][i]-expected[s][i]) for s in ('min','max') for i in range(3));assert delta<1e-7
assert source['triangles']==glb['scene_triangles']
report={'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'seed':P['seed'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'source':source,'glb':glb,'boolean_sliver_cleanup':{'collapsed_short_edges':sliver_collapses,'max_allowed_edge_mm':.15,'area_threshold_mm2':.000101},'ground_shift_m':-low,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'limits':'Static source/export audit only, not independent factual/visual, GPU or populated-scene acceptance.'}
(out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('GOGONASUS_BUILD',json.dumps({'sha256':glb['sha256'],'triangles':glb['scene_triangles'],'bytes':glb['bytes'],'bounds':glb['bounds_m']}))
