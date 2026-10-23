#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original Volaticotherium living reconstruction, meters.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Source dependencies are local and pinned in dependencies.json. No network access.
"""
import sys, json, math, hashlib, argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def write(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
argsv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(); p.add_argument('--out',type=Path,required=True); args=p.parse_args(argsv)
out=args.out.resolve(); out.mkdir(parents=True,exist_ok=True)
params=json.loads((ROOT/'params.json').read_text()); seed=params['seed']
C=setup_scene('volaticotherium',seed)
M={k:make_material(k,v,roughness=.92 if k not in ('dark','claw') else .7) for k,v in params['palette_srgb'].items()}
# All coordinates authored in meters. Root is the airborne mount vertically below trunk center.
bpy.context.scene['origin_contract']='airborne mount at world origin, under trunk center; not a floor-contact animal'
bpy.context.scene['representation']='living reconstruction; membrane outline, pose, ear, color and complete tail length inferred'

# Closed longitudinal profile loft with discrete low-poly cross-sections.
def loft(name, rows, material='coat', n=12, palette=False):
    # rows=(x,y,z, lateral_radius, vertical_radius); section planes are XZ.
    vs=[]
    for j,(x,y,z,rx,rz) in enumerate(rows):
        for k in range(n):
            a=2*math.pi*k/n; mod=1+.018*math.sin(k*3.1+j*2.2)
            vs.append((x+rx*math.cos(a)*mod,y,z+rz*math.sin(a)*mod))
    fs=[tuple(reversed(range(n)))]
    for j in range(len(rows)-1):
        for k in range(n): fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    fs.append(tuple((len(rows)-1)*n+k for k in range(n)))
    obj=mesh_object(name,vs,fs,[M[material],M['back'],M['under']] if palette else M[material],C)
    if palette:
        for f in obj.data.polygons:
            # Inferred modest dorsal/ventral coat variation, no preserved pigmentation claim.
            z=sum(obj.data.vertices[i].co.z for i in f.vertices)/len(f.vertices)
            y=sum(obj.data.vertices[i].co.y for i in f.vertices)/len(f.vertices)
            f.material_index=1 if z>.0305 and name=='torso' else 2 if z<.0165 else 0
    return obj

# Closed tube along arbitrary skeleton path. Shape tapers at endpoints, no zero-area tips.
def tube_mesh(path,radii,sides=8,flat=.85):
    vs=[]; fs=[]
    for j,point in enumerate(path):
        pt=Vector(point)
        tangent=Vector(path[min(j+1,len(path)-1)])-Vector(path[max(j-1,0)])
        tangent.normalize(); ref=Vector((0,0,1))
        if abs(tangent.dot(ref))>.94: ref=Vector((0,1,0))
        a=tangent.cross(ref).normalized(); b=tangent.cross(a).normalized()
        for k in range(sides):
            ang=2*math.pi*k/sides
            vs.append(tuple(pt+radii[j]*(math.cos(ang)*a+flat*math.sin(ang)*b)))
    fs.append(tuple(reversed(range(sides))))
    for j in range(len(path)-1):
        for k in range(sides): fs.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    fs.append(tuple((len(path)-1)*sides+k for k in range(sides)))
    return vs,fs

def tube(name,path,radii,mat='coat',sides=8,flat=.85):
    v,f=tube_mesh(path,radii,sides,flat); return mesh_object(name,v,f,M[mat],C)

def ellipsoid(name,center,radii,mat='coat',n=12,rings=7):
    # Non-zero poles capped by n-gons to avoid tiny degenerate fan triangles.
    cx,cy,cz=center; rx,ry,rz=radii; vs=[]; fs=[]
    for j in range(rings):
        t=-math.pi/2+.12+j*(math.pi-.24)/(rings-1)
        for k in range(n):
            a=2*math.pi*k/n
            vs.append((cx+rx*math.cos(t)*math.cos(a),cy+ry*math.cos(t)*math.sin(a),cz+rz*math.sin(t)))
    fs=[tuple(reversed(range(n)))]
    for j in range(rings-1):
        for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    fs.append(tuple((rings-1)*n+k for k in range(n)))
    return mesh_object(name,vs,fs,M[mat],C)

loft('torso',[(0,-.038,.024,.006,.006),(0,-.030,.025,.011,.010),
 (0,-.018,.025,.016,.012),(0,.0,.025,.018,.013),(0,.020,.024,.017,.012),
 (0,.038,.022,.015,.0105),(0,.052,.020,.010,.008),(0,.060,.019,.005,.004)],palette=True,n=16)
# Skull and jaw depth based on the reconstructed original, not a squirrel's pointed cone.
loft('head',[(0,-.070,.0255,.0028,.0038),(0,-.067,.027,.0050,.0055),
 (0,-.060,.029,.0080,.0076),(0,-.052,.030,.0115,.0100),
 (0,-.044,.029,.0120,.0108),(0,-.035,.026,.0088,.0083)],palette=True,n=16)
loft('lower-jaw',[(0,-.068,.0222,.0026,.0018),(0,-.060,.0212,.0065,.0034),
 (0,-.049,.0208,.0091,.0043),(0,-.038,.0223,.0070,.0033)],material='under',n=10)
ellipsoid('nose',(0,-.0702,.0263),(.0033,.0013,.0022),'dark',10,6)
# Eyes are small, slightly forward-facing, without fabricated white sclera.
for s,label in [(1,'right'),(-1,'left')]:
    ellipsoid(label+'-eye',(s*.0100,-.0535,.0334),(.0019,.0023,.0020),'dark',10,6)
    # Modest reconstructed soft pinnae, not oversized mouse ears.
    ellipsoid(label+'-ear',(s*.0105,-.0385,.0383),(.0042,.0036,.0050),'coat',10,7)
    ellipsoid(label+'-ear-inner',(s*.0108,-.0410,.0388),(.0026,.00115,.0030),'membrane',10,6)
    # A fine unobtrusive mouth line; closed tube intersects the jaw surface intentionally.
    tube(label+'-mouth',[(s*.0036,-.068,.0237),(s*.0070,-.060,.0237),(s*.0095,-.051,.0243)], [.00040,.00044,.00032],'dark',6,.9)

# Membrane surfaces span shoulder/forearm through body side to hindlimb.
# The contour is inferred. The preserved hair is represented by opaque material,
# restrained edge irregularity and very shallow microfacets, never transparency.
inner=[(.012,-.026,.024),(.015,-.020,.024),(.017,-.009,.024),(.018,.005,.023),(.017,.021,.022),(.015,.036,.021),(.009,.050,.020)]
outer=[(.045,-.040,.025),(.076,-.036,.024),(.071,-.015,.020),(.062,.006,.017),(.058,.029,.015),(.059,.049,.014),(.060,.063,.014)]
for s,label in [(1,'right'),(-1,'left')]:
    vs=[]; fs=[]; nr=len(inner); nc=9
    for layer in [1,-1]:
        for r,(a,b) in enumerate(zip(inner,outer)):
            for k in range(nc):
                v=k/(nc-1)
                x=a[0]*(1-v)+b[0]*v; y=a[1]*(1-v)+b[1]*v
                z=a[2]*(1-v)+b[2]*v+.0023*math.sin(math.pi*v)*math.sin(math.pi*r/(nr-1))
                fuzz=.00020*math.sin(r*2.8+k*3.8)*math.sin(math.pi*v)
                if k==nc-1 and 1<r<nr-1: x+=.00045*math.sin(r*2.8)
                thick=.00125+.0013*(1-v)
                vs.append((s*x,y,z+layer*(thick/2)+fuzz))
    count=nr*nc
    for layer in range(2):
        off=layer*count
        for r in range(nr-1):
            for k in range(nc-1):
                a=off+r*nc+k;b=a+1;c=a+nc+1;d=a+nc
                fs.extend([(a,b,c),(a,c,d)] if (r+k)%2 else [(a,b,d),(b,c,d)])
    boundary=[k for k in range(nc)]+[r*nc+nc-1 for r in range(1,nr)]+[(nr-1)*nc+k for k in range(nc-2,-1,-1)]+[r*nc for r in range(nr-2,0,-1)]
    for j,a in enumerate(boundary):
        b=boundary[(j+1)%len(boundary)];fs.append((a,b,b+count,a+count))
    obj=mesh_object(label+'-furred-patagium',vs,fs,[M['membrane'],M['under'],M['coat']],C)
    for f in obj.data.polygons:
        f.material_index=1 if f.center.z < .0 else 0
    # set by known face block: lower half lighter; perimeter coat creates fur edge, not stripes.
    topfaces=2*(nr-1)*(nc-1)
    for idx,f in enumerate(obj.data.polygons): f.material_index=0 if idx<topfaces else 1 if idx<2*topfaces else 2
    # Forelimbs and hindlimbs lie against the membrane boundary, no bat wing fingers.
    tube(label+'-forelimb',[(s*.011,-.026,.025),(s*.030,-.034,.026),(s*.045,-.040,.026),(s*.061,-.039,.025),(s*.076,-.036,.024)],[.005,.004,.0033,.0026,.0022],sides=10)
    tube(label+'-hindlimb',[(s*.012,.046,.022),(s*.031,.044,.021),(s*.042,.052,.018),(s*.060,.063,.014),(s*.064,.067,.014)],[.006,.005,.0036,.0026,.0020],sides=10)
    # Combined semantic paw mesh contains independently closed digits and palm.
    for kind,center in [('hand',(s*.079,-.037,.024)),('foot',(s*.064,.067,.014))]:
        palm=ellipsoid(label+'-'+kind,center,(.0045,.0036,.0021),'coat',10,6)
        verts=[];faces=[];clv=[];clf=[]
        cx,cy,cz=center
        for d in range(5):
            spread=(d-2)*.00165
            length=.0048-.00045*abs(d-2)
            start=(cx+s*.0018,cy+spread,cz)
            end=(cx+s*(.003+length),cy+spread*1.65,cz-.00055)
            path=[start,((start[0]+end[0])*.5,(start[1]+end[1])*.5,cz+.00035),end]
            v,f=tube_mesh(path,[.00085,.0007,.00045],6,.8);base=len(verts);verts+=v;faces += [tuple(base+i for i in f0) for f0 in f]
            tip=(end[0]+s*.0012,end[1]-.0002,end[2]-.0009)
            v,f=tube_mesh([end,tip],[.0005,.00017],5,.8);base=len(clv);clv+=v;clf += [tuple(base+i for i in f0) for f0 in f]
        mesh_object(label+'-'+kind+'-five-short-digits',verts,faces,M['coat'],C)
        mesh_object(label+'-'+kind+'-claws',clv,clf,M['claw'],C)
# Long, narrow, gently bent and slightly dorsoventrally flattened caudal profile.
# Chord length is near 140 mm; exact total restored length is a modeling choice.
loft('slender-flattened-tail',[(0,.055,.019,.0052,.0033),(0,.074,.018,.0049,.0029),
 (.002,.094,.017,.0043,.0025),(.005,.116,.017,.0038,.0021),
 (.008,.139,.018,.0030,.0017),(.009,.161,.020,.0023,.0013),
 (.007,.181,.023,.00155,.00095),(.004,.194,.025,.00055,.00040)],material='coat',n=10)
# Restrained short fur tufts on the trunk shoulder/flanks; original geometry,
# deliberately grouped as one mesh to avoid costly per-strand nodes or hair textures.
vs=[];fs=[]
for j in range(18):
    s=1 if j%2 else -1;y=-.023+(j//2)*.0082
    width=.0125+.0032*math.sin((y+.023)/.07*math.pi)
    z=.027+.003*math.sin(j*1.7);x=s*width
    b=len(vs)
    vs += [(x-s*.0015,y-.002,z-.001),(x+s*.001,y-.001,z+.0008),(x+s*.0022,y+.0032,z-.0013),(x-s*.001,y+.002,z-.0016)]
    fs += [(b,b+2,b+1),(b,b+1,b+3),(b+1,b+2,b+3),(b+2,b,b+3)]
mesh_object('short-flank-fur',vs,fs,M['coat'],C)

# Source and export technical checks remain distinct from independent visual QA.
source=audit_source(C,params['budgets']['max_triangles'])
write(out/'source-qa.json',source)
if source['errors']:raise RuntimeError('Source QA: '+repr(source['errors']))
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in C.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,
 export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,
 export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,
 export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
 export_extras=True,export_gpu_instances=False,export_gn_mesh=False,
 export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
avail={a.identifier for a in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-avail: raise RuntimeError('Unsupported exporter flags: '+repr(set(opts)-avail))
bpy.ops.export_scene.gltf(**opts)
q=audit_glb(out/'model.glb',params['budgets']['max_triangles'],params['budgets']['max_materials'],params['budgets']['max_primitives'])
write(out/'glb-qa.json',q)
if q['errors']:raise RuntimeError('GLB QA: '+repr(q['errors']))
if (out/'model.glb').stat().st_size>params['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m'];lo=[b['min'][0],b['min'][2],-b['max'][1]];hi=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(q['bounds_m'][key][i]-expected[i]) for key,expected in [('min',lo),('max',hi)] for i in range(3))
if delta>1e-6:raise RuntimeError('Axis roundtrip failed')
try:
 import io_scene_gltf2
 exporter_version='.'.join(map(str,io_scene_gltf2.bl_info['version']))
except Exception:exporter_version='bundled, version unavailable'
write(out/'build.json',{'asset_id':'volaticotherium','revision':'r001','seed':seed,'blender_version':bpy.app.version_string,
 'exporter_version':exporter_version,'generator_sha256':digest(Path(__file__)),'parameters_sha256':digest(ROOT/'params.json'),
 'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),'semantic_sha256':q['semantic_sha256'],
 'export_options':{k:v for k,v in opts.items() if k!='filepath'},'source_glb_bounds_max_error_m':delta,
 'source_triangles':source['triangles'],'glb_triangles':q['scene_triangles'],'coordinate_contract':{'blender_up':'+Z','blender_forward':'-Y','glb_up':'+Y','glb_forward':'+Z','units':'meters','origin':'airborne mount vertically below trunk center'},
 'source_clean':not any(o.type in ('LIGHT','CAMERA') for o in bpy.context.scene.objects)})
print('BUILD COMPLETE',str(out),q['scene_triangles'],q['sha256'])
