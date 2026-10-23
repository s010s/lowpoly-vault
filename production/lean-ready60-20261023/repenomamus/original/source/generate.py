#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original deterministic Repenomamus giganticus living reconstruction.
Blender 4.3.2, meters, +Z up and -Y forward. Local relative dependencies only.
Run Blender background with 2 threads, this script, and -- --out OUTPUT.
"""
import sys, json, math, hashlib, argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source, ground_asset
from qa_glb import audit_glb

def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
params=json.loads((ROOT/'params.json').read_text());seed=params['seed']
C=setup_scene('repenomamus',seed)
M={k:make_material(k,v,roughness=.91 if k not in ('dark','claw') else .73) for k,v in params['palette_srgb'].items()}
bpy.context.scene['representation']='living reconstruction; fur, soft tissue, complete tail and pose inferred'
bpy.context.scene['foot_basis']='Congeneric R. robustus V13605; not preserved in R. giganticus V14155'

# Profile-shaped low-poly solids; no untouched organic primitives.
def loft(name,rows,mat='coat',n=16,belly=False):
    v=[];f=[]
    for j,(x,y,z,rx,rz) in enumerate(rows):
        for k in range(n):
            t=2*math.pi*k/n
            v.append((x+rx*math.cos(t),y,z+rz*math.sin(t)))
    f=[tuple(reversed(range(n)))]
    for j in range(len(rows)-1):
        for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    f.append(tuple((len(rows)-1)*n+k for k in range(n)))
    o=mesh_object(name,v,f,[M[mat],M['under']] if belly else M[mat],C)
    if belly:
        for face in o.data.polygons:
            z=sum(o.data.vertices[i].co.z for i in face.vertices)/len(face.vertices)
            # Restrained ventral tonal distinction, no asserted fossil pigmentation.
            if z<.12:face.material_index=1
    return o

def tube_data(path,radii,n=10,flat=1.0):
    v=[];f=[]
    for j,point in enumerate(path):
        pt=Vector(point);t=Vector(path[min(j+1,len(path)-1)])-Vector(path[max(0,j-1)])
        t.normalize();ref=Vector((0,0,1))
        if abs(t.dot(ref))>.94:ref=Vector((0,1,0))
        u=t.cross(ref).normalized();w=t.cross(u).normalized()
        for k in range(n):
            q=2*math.pi*k/n;v.append(tuple(pt+radii[j]*(math.cos(q)*u+flat*math.sin(q)*w)))
    f=[tuple(reversed(range(n)))]
    for j in range(len(path)-1):
        for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    f.append(tuple((len(path)-1)*n+k for k in range(n)))
    return v,f

def tube(name,path,radii,mat='coat',n=10,flat=1.0):
    v,f=tube_data(path,radii,n,flat);return mesh_object(name,v,f,M[mat],C)

def oval(name,center,radii,mat='coat',n=12,rings=7):
    x,y,z=center;rx,ry,rz=radii;v=[];f=[]
    for j in range(rings):
        t=-math.pi/2+.12+j*(math.pi-.24)/(rings-1)
        for k in range(n):
            q=2*math.pi*k/n;v.append((x+rx*math.cos(t)*math.cos(q),y+ry*math.cos(t)*math.sin(q),z+rz*math.sin(t)))
    f=[tuple(reversed(range(n)))]
    for j in range(rings-1):
        for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    f.append(tuple((rings-1)*n+k for k in range(n)))
    return mesh_object(name,v,f,M[mat],C)

# Trunk nominal longitudinal extent 522 mm, the measured skeletal trunk value.
# Fleshed widths/heights are inferred, with a long robust, low body.
loft('long-robust-trunk',[(0,-.240,.160,.060,.050),(0,-.204,.163,.088,.068),
 (0,-.145,.161,.108,.072),(0,-.060,.155,.114,.073),(0,.045,.153,.110,.071),
 (0,.135,.151,.105,.069),(0,.205,.148,.095,.068),(0,.255,.146,.070,.056),
 (0,.282,.144,.043,.036)],n=20,belly=True)
# A short powerful neck flows into broad posterior cheeks without a doglike narrow neck.
loft('strong-neck',[(0,-.292,.176,.051,.048),(0,-.266,.172,.068,.061),
 (0,-.238,.166,.077,.065),(0,-.204,.160,.079,.061)],n=16,belly=True)
# Large head: 175 mm fleshed axial length; heavy posterior cranial/temporal volume.
loft('elongate-heavy-head',[(0,-.415,.167,.029,.023),(0,-.398,.173,.037,.030),
 (0,-.368,.181,.043,.040),(0,-.340,.191,.049,.049),(0,-.312,.193,.062,.054),
 (0,-.280,.186,.067,.056),(0,-.252,.177,.055,.049),(0,-.240,.169,.042,.034)],n=18)
# Thick mandible remains a separate readable lower profile, closed mouth.
loft('deep-powerful-mandible',[(0,-.410,.148,.025,.012),(0,-.392,.143,.033,.018),
 (0,-.360,.139,.042,.024),(0,-.322,.139,.052,.030),(0,-.287,.143,.059,.034),
 (0,-.264,.151,.047,.027)],mat='coat',n=14)
oval('nose',(0,-.4155,.169),(.030,.008,.020),'dark',12,7)
for s,label in [(1,'right'),(-1,'left')]:
    oval(label+'-eye',(s*.0513,-.333,.2095),(.0063,.0080,.0062),'dark',12,7)
    # Small rounded soft-tissue ears are reconstructed, not fossil dimensions.
    oval(label+'-ear',(s*.057,-.267,.227),(.0165,.013,.0215),'coat',12,7)
    oval(label+'-ear-inner',(s*.059,-.277,.230),(.0105,.0045,.0135),'ear',12,7)
    tube(label+'-closed-mouth-line',[(s*.027,-.409,.151),(s*.037,-.383,.153),
      (s*.046,-.352,.158),(s*.055,-.321,.160),(s*.058,-.299,.161)],
      [.0018,.0019,.0019,.0017,.0012],'dark',6,.85)
    # Scapular and thigh masses made as shaped limb sections, not spherical joints.
    tube(label+'-stout-forelimb',[(s*.072,-.187,.177),(s*.091,-.174,.140),
      (s*.116,-.137,.089),(s*.123,-.159,.053),(s*.130,-.192,.024)],
      [.043,.038,.029,.023,.018],n=12)
    tube(label+'-stout-hindlimb',[(s*.071,.204,.159),(s*.096,.183,.132),
      (s*.126,.130,.084),(s*.136,.181,.051),(s*.139,.224,.029),(s*.143,.201,.020)],
      [.049,.044,.033,.024,.019,.018],n=12)
    for kind,cx,cy in [('hand',s*.131,-.195),('foot',s*.143,.194)]:
        # Broad low plantigrade paw and five short digits, based on congener.
        oval(label+'-'+kind+'-palm',(cx,cy,.0185),(.030,.036,.016),'coat',14,7)
        vs=[];fs=[];cv=[];cf=[]
        for d in range(5):
            spread=(d-2)*.011
            length=.022-.0035*abs(d-2)
            start=(cx+spread,cy-.016,.012)
            mid=(cx+spread*1.13,cy-.032,.011)
            end=(cx+spread*1.30,cy-.033-length,.008)
            v,f=tube_data([start,mid,end],[.007,.006,.0048],8,.80)
            b=len(vs);vs+=v;fs += [tuple(b+i for i in face) for face in f]
            tip=(end[0]+spread*.025,end[1]-.008,end[2]-.0037)
            v,f=tube_data([end,tip],[.0048,.0013],7,.70)
            b=len(cv);cv+=v;cf += [tuple(b+i for i in face) for face in f]
        mesh_object(label+'-'+kind+'-five-short-digits',vs,fs,M['coat'],C)
        mesh_object(label+'-'+kind+'-modest-claws',cv,cf,M['claw'],C)
# Long, tapered, near-circular tail. Centerline length is about390 mm, inferred
# beyond the published 364 mm PRESERVED caudal length, not a Castorocauda paddle.
tail=[(0,.262,.144),(.006,.315,.131),(.015,.370,.112),(.030,.425,.090),
 (.050,.482,.073),(.068,.537,.065),(.075,.591,.067),(.071,.643,.076)]
base=Vector(tail[0]); length=sum((Vector(a)-Vector(b)).length for a,b in zip(tail,tail[1:])); tail=[tuple(base+(Vector(p)-base)*(params['tail_model_m']/length)) for p in tail]
tube('long-round-tapering-tail',tail,[.037,.033,.027,.022,.017,.012,.007,.0023],n=14)
# Small restrained angular fur breaks, grouped into one closed editable mesh.
vs=[];fs=[]
for j in range(16):
    s=1 if j%2 else -1;y=-.150+(j//2)*.050
    x=s*(.105 if y<.12 else .094);z=.173
    b=len(vs);vs += [(x-s*.007,y-.010,z-.008),(x+s*.003,y-.006,z+.006),
                     (x+s*.007,y+.016,z-.006),(x-s*.008,y+.009,z-.014)]
    fs += [(b,b+2,b+1),(b,b+1,b+3),(b+1,b+2,b+3),(b+2,b,b+3)]
mesh_object('restrained-short-fur-contour',vs,fs,M['coat'],C)
shift=ground_asset(C,center_xy=False)
# Root stays identity; grounding shifts top-level part object translations only.
source=audit_source(C,params['budgets']['max_triangles']);write(out/'source-qa.json',source)
if source['errors']:raise RuntimeError('Source QA failed: '+repr(source['errors']))
bpy.context.preferences.filepaths.save_version=0
# Replace factory UI filesystem defaults before source freeze. These are not asset dependencies.
bpy.context.scene.render.filepath='//preview'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'//' + b' '*1000
                space.params.directory=b'//'
                space.params.filename=''
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,
 export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,
 export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,
 export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
 export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
avail={v.identifier for v in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-avail:raise RuntimeError('Required exporter option unavailable')
bpy.ops.export_scene.gltf(**opts)
q=audit_glb(out/'model.glb',params['budgets']['max_triangles'],params['budgets']['max_materials'],params['budgets']['max_primitives']);q['file']='model.glb';write(out/'glb-qa.json',q)
if q['errors']:raise RuntimeError('Export audit failed: '+repr(q['errors']))
if (out/'model.glb').stat().st_size>params['budgets']['max_glb_bytes']:raise RuntimeError('Byte budget exceeded')
b=source['bounds_blender_m'];lo=[b['min'][0],b['min'][2],-b['max'][1]];hi=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(q['bounds_m'][key][i]-v[i]) for key,v in [('min',lo),('max',hi)] for i in range(3))
if delta>1e-6:raise RuntimeError('Source/export bounds mismatch')
import io_scene_gltf2
write(out/'build.json',{'asset_id':'repenomamus','revision':'r001','seed':seed,
 'blender_version':bpy.app.version_string,'exporter_version':'.'.join(map(str,io_scene_gltf2.bl_info['version'])),
 'generator_sha256':digest(Path(__file__)),'parameters_sha256':digest(ROOT/'params.json'),
 'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),
 'semantic_sha256':q['semantic_sha256'],'export_options':{k:v for k,v in opts.items() if k!='filepath'},
 'source_glb_bounds_max_error_m':delta,'source_triangles':source['triangles'],'glb_triangles':q['scene_triangles'],
 'tail_centerline_m':sum((Vector(a)-Vector(b)).length for a,b in zip(tail,tail[1:])),
 'coordinate_contract':{'blender_up':'+Z','blender_forward':'-Y','glb_up':'+Y','glb_forward':'+Z','units':'meters','origin':'floor-contact center between four planted paws'},
 'source_clean':not any(o.type in ('CAMERA','LIGHT') for o in bpy.context.scene.objects),
 'ground_shift_m':list(shift)})
print('BUILD COMPLETE',q['scene_triangles'],q['sha256'])
