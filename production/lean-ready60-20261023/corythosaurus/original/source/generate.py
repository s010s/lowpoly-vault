#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original deterministic Corythosaurus living reconstruction.
Run in Blender: blender -b -t 2 --python source/generate.py -- --output .
Only the accompanying parameter file and declared relative dependencies are read.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

class Part:
    def __init__(self): self.v=[];self.f=[];self.mi=[]
    def add(self,v,f,mi=0):
        base=len(self.v);self.v.extend(v);self.f.extend(tuple(base+i for i in face) for face in f)
        self.mi.extend(mi if isinstance(mi,list) else [mi]*len(f))
    def object(self,name,mats,col):
        ob=mesh_object(name,self.v,self.f,mats,col)
        for p,i in zip(ob.data.polygons,self.mi):p.material_index=i
        return ob

def loft_y(part,rows,n=14,belly=False):
    # Ring rows: y, central z, lateral halfwidth, vertical halfheight.
    v=[];f=[];mi=[]
    for y,z,rx,rz in rows:
        for j in range(n):
            a=2*math.pi*j/n;v.append((rx*math.cos(a),y,z+rz*math.sin(a)))
    f.append(tuple(range(n-1,-1,-1)));mi.append(0)
    for k in range(len(rows)-1):
        for j in range(n):
            f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
            mi.append(1 if belly and math.sin(2*math.pi*(j+.5)/n)<-.48 else 0)
    f.append(tuple((len(rows)-1)*n+j for j in range(n)));mi.append(0)
    part.add(v,f,mi)

def tube(part,rows,n=10):
    # Along an anatomical joint path, with a transported lateral frame.
    pts=[Vector(r[:3]) for r in rows];v=[];f=[]
    for k,r in enumerate(rows):
        tangent=(pts[min(k+1,len(pts)-1)]-pts[max(k-1,0)]).normalized()
        u=Vector((1,0,0));u=(u-tangent*u.dot(tangent)).normalized();w=tangent.cross(u).normalized()
        for j in range(n):
            a=2*math.pi*j/n;p=pts[k]+u*(r[3]*math.cos(a))+w*(r[4]*math.sin(a));v.append(tuple(p))
    f.append(tuple(range(n-1,-1,-1)))
    for k in range(len(rows)-1):
        for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    f.append(tuple((len(rows)-1)*n+j for j in range(n)));part.add(v,f)

def ellipsoid(part,c,r,n=10,l=6):
    v=[(c[0],c[1],c[2]+r[2])];f=[]
    for i in range(1,l):
        a=math.pi*i/l
        for j in range(n):
            b=2*math.pi*j/n;v.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]+r[2]*math.cos(a)))
    bottom=len(v);v.append((c[0],c[1],c[2]-r[2]))
    for j in range(n):f.append((0,1+j,1+(j+1)%n))
    for i in range(l-2):
        for j in range(n):f.append((1+i*n+j,1+(i+1)*n+j,1+(i+1)*n+(j+1)%n,1+i*n+(j+1)%n))
    for j in range(n):f.append((bottom,1+(l-2)*n+(j+1)%n,1+(l-2)*n+j))
    part.add(v,f)

def build(out):
    params=json.loads((HERE/'params.json').read_text());col=setup_scene('corythosaurus',params['seed'])
    mats={k:make_material(k,v,.87) for k,v in params['palette'].items()}
    body=Part();loft_y(body,[
      (-2.83,2.92,.22,.29),(-2.62,2.88,.27,.34),(-2.40,2.75,.31,.39),(-2.15,2.56,.36,.43),
      (-1.87,2.39,.46,.55),(-1.52,2.26,.60,.69),(-1.10,2.24,.76,.82),(-.55,2.27,.88,.90),
      (.05,2.30,.91,.91),(.60,2.31,.82,.83),(1.12,2.25,.65,.68),(1.54,2.21,.48,.51),
      (1.90,2.18,.38,.40),(2.35,2.14,.32,.34),(2.90,2.08,.26,.28),(3.50,2.00,.21,.23),
      (4.10,1.89,.165,.18),(4.65,1.77,.12,.14),(5.13,1.65,.08,.10),(5.55,1.55,.045,.063),
      (5.87,1.49,.022,.035),(6.10,1.46,.006,.011)],n=16,belly=True)
    body.object('axial-torso-neck-tail',[mats['body'],mats['belly']],col)
    head=Part();loft_y(head,[(-3.90,2.92,.30,.105),(-3.74,2.96,.34,.14),(-3.53,3.00,.31,.18),
      (-3.30,3.08,.26,.245),(-3.08,3.12,.285,.285),(-2.87,3.11,.27,.28),(-2.69,3.05,.22,.23),(-2.57,3.00,.12,.13)],n=14)
    # Broad keratinous bill is the anterior portion of the head, not a toothy beak.
    for i in range(len(head.mi)):
        ys=[head.v[j][1] for j in head.f[i]]
        if sum(ys)/len(ys)<-3.56:head.mi[i]=1
    head.object('head-and-broad-bill',[mats['body'],mats['bill']],col)
    # A solid, laterally compressed high helmet with a broad continuous skull base.
    profile=[(-3.34,3.20),(-3.39,3.43),(-3.34,3.67),(-3.23,3.87),(-3.05,4.00),
      (-2.83,4.04),(-2.62,3.99),(-2.46,3.85),(-2.39,3.66),(-2.43,3.45),(-2.58,3.22),(-2.84,3.17)]
    crest=Part();n=len(profile);v=[];f=[]
    for side in [-1,1]:
        for y,z in profile:v.append((side*(.065+.055*max(0,1-(z-3.2)/.84)),y,z))
        cy,cz=-2.88,3.57
        for y,z in profile:v.append((side*.185,cy+(y-cy)*.52,cz+(z-cz)*.52))
        v.append((side*.20,cy,cz))
    stride=2*n+1
    for s in [0,1]:
        b=s*stride
        for j in range(n):
            q=(j+1)%n;f.append((b+j,b+q,b+n+q,b+n+j));f.append((b+n+j,b+n+q,b+2*n))
    for j in range(n):q=(j+1)%n;f.append((j,q,stride+q,stride+j))
    crest.add(v,f);crest.object('rounded-helmet-crest',mats['crest'],col)
    claws=Part();detail=Part()
    for side,label in [(-1,'left'),(1,'right')]:
        dy=.10 if side<0 else -.10
        leg=Part();tube(leg,[(side*.60,.52+dy,2.38,.39,.48),(side*.76,.22+dy,1.98,.38,.46),
          (side*.80,-.21+dy,1.40,.29,.33),(side*.77,-.08+dy,1.05,.20,.23),
          (side*.72,.26+dy,.55,.135,.16),(side*.72,.27+dy,.23,.14,.14)],12)
        # Broad plantigrade three-toed foot with blunt, hoof-like digit ends.
        ellipsoid(leg,(side*.72,.05+dy,.18),(.27,.37,.18),12,6)
        for j in [-1,0,1]:
            x=side*.72+j*.18;yend=-.48+dy+abs(j)*.085
            tube(leg,[(x*.95+.036*side,.02+dy,.17,.12,.12),(x,yend+.12,.12,.115,.10),(x,yend,.10,.10,.085)],8)
            ellipsoid(claws,(x,yend-.035,.098),(.092,.112,.07),8,4)
        leg.object('hindlimb-'+label,mats['body'],col)
        arm=Part();tube(arm,[(side*.55,-1.35,2.36,.23,.28),(side*.65,-1.50,1.98,.19,.22),
          (side*.65,-1.32,1.62,.15,.16),(side*.62,-1.55,1.29,.10,.12),(side*.61,-1.72,1.13,.105,.13)],10)
        ellipsoid(arm,(side*.61,-1.75,1.09),(.13,.15,.17),8,5)
        for j in [-1,0,1]:tube(arm,[(side*.61+j*.065,-1.79,1.03,.045,.055),(side*.61+j*.065,-1.84,.90,.038,.044)],6)
        arm.object('forelimb-'+label,mats['body'],col)
        ellipsoid(detail,(side*.269,-3.13,3.19),(.039,.071,.061),10,6)
        ellipsoid(detail,(side*.291,-3.61,3.058),(.021,.047,.027),8,4)
        # A shallow closed mouth seam: visual soft-tissue choice, not exposed teeth.
        tube(detail,[(side*.286,-3.81,2.924,.009,.011),(side*.311,-3.65,2.925,.009,.011),
          (side*.285,-3.46,2.95,.008,.009)],6)
    claws.object('blunt-toe-nails',mats['nails'],col);detail.object('eyes-nares-mouth',mats['detail'],col)
    # Explicit footprint pivot, metric size and unobscured asset-only scene.
    bpy.context.scene['reconstruction_scope']='Living reconstruction; artistic soft tissue, colour and pose.'
    bpy.context.scene['scale_basis']='10 m genus estimate, not a measured museum specimen.'
    bpy.context.scene['generator']='source/generate.py';bpy.context.scene['asset_license']='CC-BY-4.0'
    bpy.context.view_layer.update();source=audit_source(col,6500)
    if source['errors']:raise RuntimeError(source['errors'])
    out.mkdir(parents=True,exist_ok=True);bpy.context.preferences.filepaths.save_version=0
    # Replace inherited UI directories and render destinations before saving source.
    # Saturate fixed-size directory buffers before assigning the portable value.
    bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'.'*1023
                    space.params.directory=b'//'
                    space.params.filename=''

    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
      export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
      export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
      export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Required exporter properties unavailable')
    bpy.ops.export_scene.gltf(**opts)
    glb=audit_glb(out/'model.glb',6500,6,12);glb['file']='model.glb'
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][s][i]-expected[s][i]) for s in ['min','max'] for i in range(3))
    if glb['errors'] or delta>1e-4 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source/export audit failed')
    if glb['bytes']>2000000 or glb['materials']>6 or glb['scene_primitives_estimated_base_draw_calls']>12:raise RuntimeError('Frozen budget exceeded')
    save(out/'build-report.json',{'asset_id':'corythosaurus','revision':'r001','blender':bpy.app.version_string,'seed':params['seed'],
      'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'source':source,'glb':glb,
      'source_export_bounds_max_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},
      'claim_scope':'Technical source and static GLB checks only. No independent visual, GPU or publication claim.'})

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);build(a.output.resolve())
