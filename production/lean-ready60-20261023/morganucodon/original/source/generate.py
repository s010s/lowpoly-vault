# SPDX-License-Identifier: MIT
"""Deterministic original Morganucodon living reconstruction.
Run with Blender 4.3.2: blender -b -t 2 --python-exit-code 1 --python source/generate.py
Optional arguments after --: --output-dir destination
Only source/params.json and the declared source/deps Python files are read.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source,ground_asset
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
parser=argparse.ArgumentParser(); parser.add_argument('--output-dir',type=Path,default=HERE.parent)
args=parser.parse_args(argv); OUT=args.output_dir; OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene(P['asset_id'],P['seed'])
MAT=[make_material(k,v,roughness=.24 if k=='eyes_nose_mouth' else .87) for k,v in P['palette'].items()]

class Mesh:
    def __init__(self): self.v=[];self.f=[];self.mi=[]
    def add(self,vertices,faces,mi=0):
        offset=len(self.v); self.v.extend(vertices); self.f.extend([tuple(offset+i for i in face) for face in faces]); self.mi.extend(mi if isinstance(mi,list) else [mi]*len(faces))
    def finish(self,name):
        ob=mesh_object(name,self.v,self.f,MAT,C)
        for p,m in zip(ob.data.polygons,self.mi):p.material_index=m
        # Remove unused slots without changing semantic assignments.
        used=sorted(set(self.mi)); lookup={old:i for i,old in enumerate(used)}
        ob.data.materials.clear()
        for i in used: ob.data.materials.append(MAT[i])
        for p,m in zip(ob.data.polygons,self.mi):p.material_index=lookup[m]
        return ob

def loft_y(mesh,sections,n=16,mi=1,coat=False,fur=0):
    """Closed profile-designed organic loft; section=(y,x,z,width,height)."""
    v=[];f=[];m=[]
    for j,(y,x,z,w,h) in enumerate(sections):
        for i in range(n):
            a=2*math.pi*i/n; k=1+fur*math.cos(i*7+j*2.3)
            v.append((x+math.cos(a)*w*k,y,z+math.sin(a)*h*k))
    for j in range(len(sections)-1):
        for i in range(n):
            a=2*math.pi*(i+.5)/n; c=0 if math.sin(a)>.56 else 2 if math.sin(a)<-.42 else 1
            q=(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i)
            # Alternating diagonals give an intentional triangular low-poly surface.
            f.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])]);m.extend([c if coat else mi]*2)
    f.extend([tuple(reversed(range(n))),tuple((len(sections)-1)*n+i for i in range(n))]);m.extend([mi,mi]);mesh.add(v,f,m)

def tube(mesh,centers,radii,n=10,mi=1):
    v=[];f=[]
    for j,(p,r) in enumerate(zip(centers,radii)):
        p=Vector(p); t=Vector(centers[min(j+1,len(centers)-1)])-Vector(centers[max(j-1,0)])
        t.normalize(); side=t.cross(Vector((0,0,1)))
        if side.length<.01:side=t.cross(Vector((0,1,0)))
        side.normalize();up=side.cross(t).normalized()
        rx,rz=r if isinstance(r,(tuple,list)) else (r,r)
        for i in range(n):
            a=2*math.pi*i/n; v.append(tuple(p+side*(math.cos(a)*rx)+up*(math.sin(a)*rz)))
    for j in range(len(centers)-1):
        for i in range(n):f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    f.extend([tuple(reversed(range(n))),tuple((len(centers)-1)*n+i for i in range(n))]);mesh.add(v,f,mi)

def ellipsoid(mesh,center,scale,mi=4,n=14,rings=7):
    v=[(center[0],center[1],center[2]+scale[2])];f=[]
    for j in range(1,rings):
        a=math.pi*j/rings
        for i in range(n):
            b=2*math.pi*i/n;v.append((center[0]+scale[0]*math.sin(a)*math.cos(b),center[1]+scale[1]*math.sin(a)*math.sin(b),center[2]+scale[2]*math.cos(a)))
    bottom=len(v);v.append((center[0],center[1],center[2]-scale[2]))
    for i in range(n):f.append((0,1+i,1+(i+1)%n));f.append((bottom,1+(rings-2)*n+(i+1)%n,1+(rings-2)*n+i))
    for j in range(rings-2):
        for i in range(n):f.append((1+j*n+i,1+(j+1)*n+i,1+(j+1)*n+(i+1)%n,1+j*n+(i+1)%n))
    mesh.add(v,f,mi)

body=Mesh()
loft_y(body,[(-.039,0,.027,.0038,.005),(-.034,0,.026,.0075,.0085),(-.027,0,.0245,.010,.0115),(-.019,0,.024,.0115,.0124),(-.009,0,.024,.0127,.0134),(.002,0,.024,.0138,.0142),(.013,0,.0235,.014,.0142),(.024,0,.023,.0128,.013),(.033,0,.022,.0098,.0105),(.039,0,.021,.006,.007),(.043,0,.020,.002,.003)],20,coat=True,fur=.016)
body.finish('elongated-low-torso')
neck=Mesh();loft_y(neck,[(-.044,0,.031,.006,.006),(-.039,0,.030,.008,.008),(-.033,0,.028,.0085,.009)],18,coat=True);neck.finish('tapered-neck')
head=Mesh();loft_y(head,[(-.068,0,.0335,.0018,.0025),(-.065,0,.0337,.0031,.0033),(-.060,0,.034,.0039,.004),(-.055,0,.0343,.0046,.0046),(-.050,0,.0345,.0061,.0062),(-.046,0,.034,.0078,.0072),(-.041,0,.0326,.0082,.0077),(-.036,0,.031,.0056,.0064)],20,coat=True);head.finish('long-low-skull-and-muzzle')
nose=Mesh();ellipsoid(nose,(0,-.0682,.034),(.002,.001,.0015),4,n=12,rings=5);nose.finish('small-nasal-pad')
# Near-closed mouth crease only. No incisors or visible teeth are modeled.
mouth=Mesh()
for s in (-1,1):
    tube(mouth,[(s*.0024,-.0658,.0317),(s*.0035,-.060,.0309),(s*.0042,-.055,.0302),(s*.0052,-.0505,.0300)],[.00012,.00013,.00013,.00010],n=6,mi=4)
mouth.finish('closed-mouth-lines')
eyes=Mesh()
for s in (-1,1):ellipsoid(eyes,(s*.0049,-.052,.0372),(.0012,.00145,.00125),4,n=14,rings=7)
eyes.finish('restrained-lateral-eyes')
# Small reconstructed pinnae, concave front, a thick continuous rim and rear.
ears=Mesh()
for s in (-1,1):
    cx=s*.0078;cy=-.039;cz=.0378;n=16;v=[]
    for layer in range(3):
        for i in range(n):
            a=2*math.pi*i/n;scale=(1,.70,.85)[layer]
            x=cx+s*math.cos(a)*.0023*scale;z=cz+math.sin(a)*.0028*scale
            y=cy+(.0004 if layer==0 else .0012 if layer==1 else .0022)+.15*(z-cz)
            v.append((x,y,z))
    v.extend([(cx,cy+.0018,cz),(cx,cy+.0024,cz)])
    f=[];mi=[]
    for i in range(n):
        k=(i+1)%n;f.extend([(i,k,n+k,n+i),(n+i,n+k,3*n),(i,2*n+i,2*n+k,k),(2*n+i,3*n+1,2*n+k)]);mi.extend([1,3,0,0])
    ears.add(v,f,mi)
ears.finish('small-rounded-inferred-ears')
# Four short flexed limbs. Their overlapping roots are intentional, editable joins.
for s in (-1,1):
    limb=Mesh()
    tube(limb,[(s*.0088,-.025,.026),(s*.0128,-.022,.020),(s*.0147,-.018,.0125),(s*.0158,-.024,.006),(s*.016,-.028,.0035)],[(.0040,.0046),(.0035,.0040),(.0028,.0031),(.0021,.0024),(.0019,.0017)],12,1)
    limb.finish(('left' if s<0 else 'right')+'-forelimb')
    limb=Mesh()
    tube(limb,[(s*.0094,.026,.025),(s*.0148,.021,.019),(s*.0173,.018,.013),(s*.018,.027,.006),(s*.018,.028,.0034)],[(.0065,.0070),(.0058,.0062),(.004,.0042),(.0023,.0027),(.0020,.0017)],12,1)
    limb.finish(('left' if s<0 else 'right')+'-hindlimb')
    for label,y,x in [('fore',-.028,.016),('hind',.028,.018)]:
        feet=Mesh();claws=Mesh()
        ellipsoid(feet,(s*x,y-.0012,.0025),(.0031,.004,.0022),3,n=12,rings=5)
        for d in range(5):
            off=(d-2)*.00145;start=(s*(x+off*.75),y-.0022,.0022)
            tip=(s*(x+off*1.18),y-.0068+.0007*abs(d-2),.0010)
            mid=(start[0]*.45+tip[0]*.55,start[1]*.45+tip[1]*.55,.00165)
            tube(feet,[start,mid,tip],[.00078,.00065,.00048],8,3)
            tube(claws,[tip,(tip[0],tip[1]-.0009,.00065),(tip[0],tip[1]-.00165,.00030)],[.00046,.00031,.00009],7,5)
        feet.finish(('left' if s<0 else 'right')+'-'+label+'-five-digits')
        claws.finish(('left' if s<0 else 'right')+'-'+label+'-claws')
tail=Mesh();tube(tail,[(0,.038,.020),(0,.046,.018),(.001,.056,.015),(.003,.066,.012),(.006,.076,.0095),(.009,.086,.0075),(.0105,.096,.0068),(.010,.099,.0069)],[.0041,.0035,.0029,.0024,.0018,.0013,.0007,.00012],12,1);tail.finish('slender-tapering-balancing-tail')
# All visible shapes are hand-authored profiles; no external meshes or textures.
shift=ground_asset(C,center_xy=False)
source=audit_source(C,P['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.scene['scientific_scope']='Genus-level inferred living reconstruction, not a fossil scan.'
bpy.context.scene['soft_tissue_status']='Inferred, including fur, ears, colors, limbs and tail.'
bpy.context.scene['dimensions_caution']=P['scale_caution']
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'/'*1023
                space.params.directory=b'//'
        if area.type=='FILE_BROWSER':area.type='VIEW_3D'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in C.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
props={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
assert not set(opts)-props
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**opts)
glb=audit_glb(OUT/'model.glb',P['max_triangles'],P['max_materials'],P['max_primitives'])
if glb['errors']:raise RuntimeError(glb['errors'])
glb['file']='model.glb'
assert glb['bytes']<=P['max_glb_bytes']
b=source['bounds_blender_m'];lo=[b['min'][0],b['min'][2],-b['max'][1]];hi=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-exp[i]) for side,exp in [('min',lo),('max',hi)] for i in range(3))
assert delta<.0001 and source['triangles']==glb['scene_triangles']
report={'status':'PASS','scope':'Source geometry, standalone static GLB and axis-aware bounds only. Not independent visual QA or GPU rendering.','asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'seed':P['seed'],'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':opts,'ground_shift_m':shift,'authored_dimension_status':P['scale_caution']}
(OUT/'technical.json').write_text(json.dumps(report,indent=2)+'\n')
print('MODEL_BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
