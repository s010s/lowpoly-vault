# SPDX-License-Identifier: MIT
"""Original deterministic Therizinosaurus reconstruction. Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
All Python imports are bundled alongside this source. No network, random assets or textures.
Semantic source parts remain editable. Only the temporary export is batched by material.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
argsv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args(argsv)
out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
p=json.loads((HERE/'params.json').read_text())
col=setup_scene('therizinosaurus',p['seed'])
root=bpy.data.objects[col['asset_root']]
mats={n:make_material(n,c,roughness=.86) for n,c in p['palette_hex'].items()}
parts=[]

def loft(name,rings,sides=12,mat='Olive plumage',belly=False):
    # Ring is center xyz and cross-section half widths. Transported lateral frame.
    vs=[];fs=[]
    for i,ring in enumerate(rings):
        c=Vector(ring[:3]);prev=Vector(rings[max(0,i-1)][:3]);nxt=Vector(rings[min(len(rings)-1,i+1)][:3])
        tangent=(nxt-prev).normalized();u=Vector((1,0,0));u=(u-tangent*u.dot(tangent)).normalized();v=tangent.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides;vs.append(tuple(c+u*(ring[3]*math.cos(a))+v*(ring[4]*math.sin(a))))
    fs.append(tuple(reversed(range(sides))))
    for i in range(len(rings)-1):
        for j in range(sides):fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    fs.append(tuple((len(rings)-1)*sides+j for j in range(sides)))
    materials=[mats[mat],mats['Warm belly'],mats['Moss back']] if belly else mats[mat]
    ob=mesh_object(name,vs,fs,materials,col)
    if belly:
        for poly in ob.data.polygons:
            zs=[ob.data.vertices[i].co.z for i in poly.vertices];xs=[ob.data.vertices[i].co.x for i in poly.vertices]
            mid=sum(zs)/len(zs)
            if mid<2.65 and abs(sum(xs)/len(xs))<.95:poly.material_index=1
            elif mid>3.5:poly.material_index=2
    ob['anatomical_part']=name;ob['construction']='closed profile loft; original reconstruction';parts.append(ob)
    return ob

def ellipsoid(name,center,radii,mat,sides=10):
    x,y,z=center;rx,ry,rz=radii
    return loft(name,[(x,y-ry*.98,z,rx*.14,rz*.14),(x,y-ry*.72,z,rx*.7,rz*.7),(x,y,z,rx,rz),(x,y+ry*.72,z,rx*.7,rz*.7),(x,y+ry*.98,z,rx*.14,rz*.14)],sides,mat)

# A broad, deep abdomen and raised chest, not a slim predatory theropod trunk.
loft('Abdomen and raised chest',[(0,-1.25,3.22,.36,.55),(0,-1.03,3.00,.72,.91),(0,-.55,2.79,.99,1.12),(0,.13,2.73,1.03,1.17),(0,.75,2.84,.87,1.04),(0,1.21,2.97,.58,.71),(0,1.50,3.06,.24,.37)],16,belly=True)
# S-shaped neck: broad feathered base, narrow upper neck, small head.
loft('Upright S-shaped neck',[(0,-.90,3.40,.46,.49),(0,-1.27,3.77,.40,.43),(0,-1.52,4.20,.32,.35),(0,-1.55,4.69,.25,.29),(0,-1.59,5.17,.22,.25),(0,-1.81,5.61,.22,.24),(0,-2.10,5.87,.23,.22)],12)
loft('Small herbivore head',[(0,-1.94,5.88,.16,.17),(0,-2.11,5.96,.25,.24),(0,-2.35,5.98,.24,.22),(0,-2.55,5.91,.17,.16),(0,-2.64,5.87,.12,.12)],12,'Warm belly')
loft('Narrow keratinous beak',[(0,-2.53,5.89,.15,.12),(0,-2.67,5.86,.145,.095),(0,-2.79,5.83,.075,.052),(0,-2.84,5.81,.018,.018)],10,'Dark keratin')
# Counterbalance tail is stout proximally and relatively short, no raptor whip.
loft('Tapering balance tail',[(0,1.12,3.00,.47,.49),(0,1.65,2.96,.39,.41),(0,2.20,2.89,.32,.34),(0,2.80,2.77,.23,.24),(0,3.36,2.68,.15,.16),(0,3.86,2.63,.08,.10),(0,4.30,2.59,.008,.012)],12)
# Left and right hindlimbs and broad, four-digit weight-bearing feet.
for s,label in [(-1,'Left'),(1,'Right')]:
    loft(label+' muscular thigh',[(s*.69,.47,2.93,.34,.44),(s*.83,.23,2.45,.42,.46),(s*.90,-.04,1.94,.35,.38),(s*.88,-.11,1.64,.24,.27)],12)
    loft(label+' angled shin',[(s*.88,-.10,1.75,.23,.26),(s*.87,.13,1.29,.19,.22),(s*.85,.38,.78,.15,.17),(s*.85,.40,.42,.17,.19)],10,'Warm belly')
    loft(label+' metatarsus',[(s*.85,.40,.54,.17,.19),(s*.86,.25,.28,.21,.20),(s*.86,.05,.17,.24,.13)],10,'Warm belly')
    for j in range(3):
        dx=(j-1)*.22;startx=s*.86+dx;endy=-.69+(abs(j-1)*.11)
        loft(label+f' forward pedal digit {j+1}',[(startx,.10,.18,.105,.095),(startx+dx*.3,-.16,.115,.10,.10),(startx+dx*.5,endy+.10,.095,.075,.075),(startx+dx*.55,endy,.075,.045,.045)],8,'Warm belly')
        loft(label+f' pedal claw {j+1}',[(startx+dx*.5,endy+.03,.09,.057,.051),(startx+dx*.55,endy-.12,.055,.037,.031),(startx+dx*.58,endy-.21,.025,.004,.004)],8,'Dark keratin')
    loft(label+' medial weight-bearing digit IV',[(s*.74,.25,.21,.10,.10),(s*.54,.08,.12,.10,.09),(s*.42,-.15,.08,.07,.06),(s*.40,-.27,.05,.04,.035)],8,'Warm belly')
    loft(label+' pedal claw IV',[(s*.40,-.23,.06,.045,.036),(s*.36,-.40,.02,.004,.004)],8,'Dark keratin')
    # Upper arm descends; forearm reaches forward. Palm plane remains sagittal.
    loft(label+' upper arm',[(s*.72,-.93,3.34,.25,.30),(s*1.02,-1.17,3.09,.22,.25),(s*1.17,-1.37,2.78,.18,.20),(s*1.20,-1.40,2.65,.16,.18)],10)
    loft(label+' forearm',[(s*1.18,-1.36,2.76,.16,.18),(s*1.32,-1.62,2.65,.15,.17),(s*1.39,-1.91,2.66,.12,.16),(s*1.40,-2.09,2.65,.10,.18)],10)
    # Three vertically fanned digital rays on inward-facing palms, never across X.
    loft(label+' inward-facing palm',[(s*1.40,-1.98,2.65,.105,.18),(s*1.40,-2.16,2.65,.09,.28),(s*1.40,-2.24,2.64,.075,.26)],10,'Warm belly')
    for j in range(3):
        z=2.92-j*.28;y=-2.20-(.08 if j==1 else 0)
        loft(label+f' manual digit {j+1}',[(s*1.40,-2.12,2.73-j*.10,.075,.07),(s*1.40,y-.07,z,.062,.068),(s*1.40,y-.23,z-.018,.059,.07)],8,'Warm belly')
        # Long flattened ungual with a gentle ventral curve. Length ~0.67 m.
        claw=loft(label+f' long manual ungual {j+1}',[(s*1.40,y-.20,z-.015,.063,.085),(s*1.40,y-.38,z-.027,.052,.072),(s*1.40,y-.57,z-.080,.039,.052),(s*1.40,y-.73,z-.17,.025,.033),(s*1.40,y-.85,z-.28,.004,.006)],8,'Ivory horn')
        claw['manual_digit_index']=j+1;claw['palm_normal']=[-s,0,0];claw['uncertainty']='visible keratin extension artistic; not a measured fossil'
    # Eyes sit on either side, not forward-facing predator eyes.
    ellipsoid(label+' ochre eye surround',(s*.232,-2.30,6.04),(.045,.092,.086),'Moss back',10)
    ellipsoid(label+' eye',(s*.264,-2.325,6.05),(.023,.047,.046),'Dark keratin',10)
    ellipsoid(label+' nostril',(s*.136,-2.65,5.90),(.012,.019,.013),'Dark keratin',8)
# Floor datum is final foot contact, whole geometry shift does not move the identity root.
lowest=min(v.co.z for ob in parts for v in ob.data.vertices)
for ob in parts:
    for v in ob.data.vertices:v.co.z-=lowest
bpy.context.view_layer.update()
root['reconstruction']='incomplete taxon; body, colour, soft tissue and pose inferred'
root['manual_digits_per_hand']=3
source=audit_source(col,p['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.scene['generator_sha256']=sha(__file__)
bpy.context.scene['params_sha256']=sha(HERE/'params.json')
bpy.context.scene['source_semantic_parts']=len(parts)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
# Batch only transient export geometry into material meshes. Source remains semantically editable.
exportcol=bpy.data.collections.new('GLB_BATCH');bpy.context.scene.collection.children.link(exportcol)
for matname,mat in mats.items():
    verts=[];faces=[]
    for ob in parts:
        for poly in ob.data.polygons:
            if ob.data.materials[poly.material_index]!=mat:continue
            f=[]
            for vi in poly.vertices:f.append(len(verts));verts.append(tuple(ob.matrix_world@ob.data.vertices[vi].co))
            faces.append(tuple(f))
    if faces:
        batch=mesh_object('Surface '+matname,verts,faces,mat,exportcol,recalculate_normals=False);batch.parent=root
bpy.ops.object.select_all(action='DESELECT')
for ob in exportcol.objects:ob.select_set(True)
root.select_set(True);bpy.context.view_layer.objects.active=root
options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Missing exporter options '+str(set(options)-available))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(out/'model.glb',p['budgets']['max_triangles'],p['budgets']['max_materials'],p['budgets']['max_primitives'])
if glb['errors']:raise RuntimeError(glb['errors'])
if glb['bytes']>p['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m'];mins=[b['min'][0],b['min'][2],-b['max'][1]];maxs=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][k][i]-target[i]) for k,target in [('min',mins),('max',maxs)] for i in range(3))
if delta>1e-4 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source-export mismatch')
write(out/'build-report.json',{'asset_id':'therizinosaurus','revision':'r001','blender':bpy.app.version_string,'seed':p['seed'],'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'source_parts_preserved':len(parts),'export_batching':'By material only; source .blend retains semantic closed meshes. Export flat-normal vertex seams are intentional.','manual_claws':{'count':6,'per_hand':3,'palm_normals':{'left':[1,0,0],'right':[-1,0,0]},'each_visible_ungual_path_m':.72},'ground_shift_m':-lowest,'blend_sha256':sha(out/'model.blend')})
print('MODEL_BUILT',json.dumps({'triangles':glb['scene_triangles'],'bytes':glb['bytes'],'glb_sha256':glb['sha256']}))
