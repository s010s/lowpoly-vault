# SPDX-License-Identifier: MIT
"""Original low-poly Drepanaspis, deterministic Blender 4.3.2 generator.
Run with Blender in background, passing --output-dir and optional --stage gray.
All generation dependencies are the adjacent params.json and deps directory.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, value): Path(p).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
argsv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--output-dir', type=Path, default=HERE.parent)
ap.add_argument('--stage', choices=['gray','final'], default='final')
a = ap.parse_args(argsv)
p = json.loads((HERE / 'params.json').read_text())
out = a.output_dir.resolve(); out.mkdir(parents=True, exist_ok=True)
col = setup_scene(p['asset_id'], p['seed'])
root = bpy.data.objects[col['asset_root']]
root['representation']='living-reconstruction'
root['mounting_origin']='center of broad shield in horizontal swimming posture'
root['scientific_limits']='Thickness, tail outline, eyes, mouth, pose, color and representative size are estimates.'
material = {k: make_material(k, '#999999' if a.stage=='gray' else v, roughness=0.88 if k!='eye' else 0.55) for k,v in p['palette'].items()}
# Radial loft: a continuous, shallow shield with a very broad front half and
# narrowing rear. The edge is finite thickness, never a zero-thickness ray wing.
outline = p['shield_outline_xy_m']
N = len(outline)
center_y = -0.035

def top_at(x,y):
    r2 = (x / 0.120)**2 + ((y-center_y)/0.131)**2
    return 0.0045 + 0.0195*max(0.,1.-r2)

def bottom_at(x,y):
    r2 = (x/0.120)**2 + ((y-center_y)/0.131)**2
    return -0.0045 - 0.011*max(0.,1.-r2)

verts=[]
for factor in [1.,0.70,0.36]:
    verts += [(x*factor,center_y+(y-center_y)*factor,top_at(x*factor,center_y+(y-center_y)*factor)) for x,y in outline]
verts.append((0,center_y,top_at(0,center_y)))
top_center=len(verts)-1
bottom_start=len(verts)
for factor in [1.,0.70,0.36]:
    verts += [(x*factor,center_y+(y-center_y)*factor,bottom_at(x*factor,center_y+(y-center_y)*factor)) for x,y in outline]
verts.append((0,center_y,bottom_at(0,center_y))); bottom_center=len(verts)-1
faces=[]
for base, cent in [(0,top_center),(bottom_start,bottom_center)]:
    for ring in range(2):
        for i in range(N):
            j=(i+1)%N; faces.append((base+ring*N+i,base+ring*N+j,base+(ring+1)*N+j,base+(ring+1)*N+i))
    for i in range(N): faces.append((base+2*N+i,base+2*N+(i+1)%N,cent))
for i in range(N):
    j=(i+1)%N; faces.append((i,j,bottom_start+j,bottom_start+i))
body=mesh_object('continuous-shield-and-ventral-body',verts,faces,[material['armor'],material['underside']],col)
for poly in body.data.polygons:
    if poly.center.z<0: poly.material_index=1

def loft(name, stations, mat, segments=12):
    vs=[]
    for y,rx,rz,zc in stations:
        for i in range(segments):
            theta=2*math.pi*i/segments
            vs.append((rx*math.cos(theta),y,zc+rz*math.sin(theta)))
    fs=[]
    for j in range(len(stations)-1):
        for i in range(segments):
            ni=(i+1)%segments; fs.append((j*segments+i,j*segments+ni,(j+1)*segments+ni,(j+1)*segments+i))
    fs.extend([tuple(reversed(range(segments))),tuple((len(stations)-1)*segments+i for i in range(segments))])
    return mesh_object(name,vs,fs,mat,col)

loft('short-armored-tail-peduncle',p['tail_stations_y_rx_rz_z_m'],material['tail'])
# Conservative finite-thickness median tail edge, not a ray sting or paired fins.
# The lower lobe is subordinate; all detailed outline proportions are inferred.
fin_yz=p['tail_fin_profile_yz_m']; half=0.0016
vs=[(s*half,y,z) for s in [-1,1] for y,z in fin_yz]
n=len(fin_yz); fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]
for i in range(n):j=(i+1)%n;fs.append((i,j,n+j,n+i))
mesh_object('small-median-caudal-fin',vs,fs,material['tail'],col)

if a.stage=='final':
    # Shallow fitted plate relief, stylized from the broad plate organization.
    # Narrow seams distinguish armor plates without copying fossil cracks.
    def plate(name,poly,mat):
        cx=sum(x for x,y in poly)/len(poly);cy=sum(y for x,y in poly)/len(poly)
        shrink=0.986
        pts=[(cx+(x-cx)*shrink,cy+(y-cy)*shrink) for x,y in poly]
        n=len(pts); vs=[]
        for f in [1.,0.70,0.35]:
            for x,y in pts:
                xx=cx+(x-cx)*f; yy=cy+(y-cy)*f
                vs.append((xx,yy,top_at(xx,yy)+0.0011))
        vs.append((cx,cy,top_at(cx,cy)+0.0011)); center=3*n
        vs += [(x,y,top_at(x,y)-0.0020) for x,y in pts]
        base=center+1;fs=[]
        for ring in range(2):
            for i in range(n):
                j=(i+1)%n;fs.append((ring*n+i,ring*n+j,(ring+1)*n+j,(ring+1)*n+i))
        for i in range(n):
            j=(i+1)%n;fs.extend([(2*n+i,2*n+j,center),(i,base+i,base+j,j)])
        fs.append(tuple(reversed(range(base,base+n))))
        return mesh_object(name,vs,fs,mat,col)
    central=[(0,-0.136),(0.040,-0.108),(0.057,-0.050),(0.046,0.018),(0,0.060),(-0.046,0.018),(-0.057,-0.050),(-0.040,-0.108)]
    plate('broad-central-dorsal-plate',central,material['plate'])
    right_panels=[
        [(0,-0.136),(0.040,-0.108),(0.052,-0.127),(0.023,-0.151),(0,-0.157)],
        [(0.040,-0.108),(0.057,-0.050),(0.096,-0.065),(0.089,-0.102),(0.052,-0.127)],
        [(0.057,-0.050),(0.046,0.018),(0.089,0.021),(0.111,-0.023),(0.096,-0.065)],
        [(0.046,0.018),(0,0.060),(0.023,0.082),(0.060,0.062),(0.089,0.021)],
        [(0.052,-0.127),(0.089,-0.102),(0.105,-0.078),(0.097,-0.112),(0.064,-0.142)],
        [(0.096,-0.065),(0.111,-0.023),(0.114,-0.055),(0.105,-0.078),(0.089,-0.102)],
    ]
    for sign,label in [(1,'right'),(-1,'left')]:
        for i,poly in enumerate(right_panels):
            poly=[(x*sign,y) for x,y in poly]
            plate(f'{label}-marginal-armor-{i+1:02d}',poly,material['armor'] if i%2==0 else material['plate'])
    # Low lateral eyes. Their small aperture and orientation are estimates.
    def ellipsoid(name,loc,radii,mat,seg=12,rings=5):
        vs=[(loc[0],loc[1],loc[2]+radii[2])]
        for j in range(1,rings):
            phi=math.pi*j/rings
            for i in range(seg):
                th=2*math.pi*i/seg
                vs.append((loc[0]+radii[0]*math.sin(phi)*math.cos(th),loc[1]+radii[1]*math.sin(phi)*math.sin(th),loc[2]+radii[2]*math.cos(phi)))
        vs.append((loc[0],loc[1],loc[2]-radii[2])); last=len(vs)-1;fs=[]
        for i in range(seg):fs.append((0,1+i,1+(i+1)%seg))
        for j in range(rings-2):
            for i in range(seg):ni=(i+1)%seg;fs.append((1+j*seg+i,1+(j+1)*seg+i,1+(j+1)*seg+ni,1+j*seg+ni))
        for i in range(seg):fs.append((last,1+(rings-2)*seg+(i+1)%seg,1+(rings-2)*seg+i))
        return mesh_object(name,vs,fs,mat,col)
    for sign,label in [(1,'right'),(-1,'left')]:
        x=sign*0.071;y=-0.111;z=top_at(x,y)
        ellipsoid(label+'-subtle-orbit',(x,y,z+0.0009),(0.008,0.0065,0.0031),material['rim'])
        ellipsoid(label+'-small-eye',(x,y-0.0008,z+0.0030),(0.0036,0.0032,0.0019),material['eye'])
    # A small anterior slit, no jaw, teeth or projecting rostrum.
    ellipsoid('small-jawless-anterior-mouth',(0,-0.1594,0.0015),(0.0135,0.0011,0.0015),material['eye'])

# Place the broad shield center at the identity swimming mount, independent of tail length.
for obj in col.all_objects:
    if obj.type=='MESH':
        for v in obj.data.vertices: v.co.y -= center_y
        obj.data.update()
bpy.context.view_layer.update()
source=audit_source(col,p['budgets']['max_triangles'])
if source['errors']: raise RuntimeError(str(source['errors']))
bpy.context.scene['asset_license']='CC-BY-4.0'
bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'//'
# Saving the authoring model precedes all rendering; no lights/cameras are kept.
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),relative_remap=False)
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects: obj.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,
    export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,
    export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
    export_animations=False,export_skins=False,export_morph=False,export_cameras=False,
    export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,
    export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={q.identifier for q in bpy.ops.export_scene.gltf.get_rna_type().properties}
missing=set(options)-available
if missing: raise RuntimeError('Missing exporter options: '+str(sorted(missing)))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(out/'model.glb',p['budgets']['max_triangles'],p['budgets']['max_materials'],p['budgets']['max_primitives'])
if glb['errors']: raise RuntimeError(str(glb['errors']))
if glb['bytes']>p['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
glb['file']='model.glb'
report={'asset_id':p['asset_id'],'revision':p['revision'],'stage':a.stage,'blender_version':bpy.app.version_string,
 'gltf_exporter_version':list(__import__('io_scene_gltf2').bl_info['version']),'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'source':source,'glb':glb,
 'export_options':{k:v for k,v in options.items() if k!='filepath'},'blend_sha256':sha(out/'model.blend'),
 'origin':'shield-centered horizontal swimming specimen','estimated_scale':True,
 'limits':'Body thickness, tail outline, eyes, mouth, colors and dimensions are inferred, not measured.'}
write(out/'build-evidence.json',report)
print('BUILD_COMPLETE', glb['sha256'], glb['scene_triangles'])
