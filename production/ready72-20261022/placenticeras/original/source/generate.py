# SPDX-License-Identifier: MIT
"""Deterministic original Placenticeras costatum fossil-form geometry.
Usage: blender --background --factory-startup --threads 2 --python generate.py -- --output PATH
Only source/params.json and bundled source/deps are needed to rebuild.
"""
import sys, json, math, hashlib, shutil, argparse
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
P=json.loads((HERE/'params.json').read_text())
a=argparse.ArgumentParser(); a.add_argument('--output',required=True)
args=a.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(args.output).resolve(); out.mkdir(parents=True,exist_ok=True)
col=setup_scene('placenticeras',P['seed'])
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
mats=[make_material('warm-grey-limestone','#99958B',roughness=.94),make_material('worn-mineral-termination','#878377',roughness=1.0)]
N=P['angular_segments']; fractions=P['radial_fractions']; M=len(fractions)
# A single continuous, filled spiral-disc envelope. The short closure sector is
# the broken terminal face; it is not an independent ring or a hollow aperture.
verts=[]; faces=[]; face_regions=[]
theta0=math.radians(120); sweep=math.radians(358.7)
for sign in (-1,1):
    verts.append((0,sign*.005,0))
    for i in range(N):
        t=i/(N-1); theta=theta0+sweep*t
        R=.074*math.exp(math.log(1.84)*t)
        # Low-amplitude original shape variation, not a traced photograph.
        R*=1+.006*math.sin(5*theta+.4)+.003*math.sin(11*theta)
        for u in fractions:
            r=u*R
            # Stone-filled central depression and gently lenticular broad flank.
            hollow=.005 + .023*(1-math.exp(-(r/.0108)**2))
            swelling=.0046*math.exp(-((u-.36)/.21)**2)
            taper=max(0,1-u**2.5)**.69
            h=(hollow+swelling)*taper + .0016*u**7
            # Faint, irregular falcate folds mainly on the right outer flank.
            phase=16*theta + 2.25*math.sin(theta+.6)+4.6*u**1.7
            gate=max(0,math.cos(theta-.15))**.8
            fold=(.00145+.00045*math.sin(3*theta))*max(0,math.cos(phase))**4
            h+=fold*math.sin(math.pi*u)**1.1*gate*min(1,(u/.4)**2)
            # Uncopied mineral undulation; bilateral low-level inference only.
            h+=.00018*math.sin(31*theta+18*u)*math.sin(43*u-7*theta)*math.sin(math.pi*u)*min(1,(u/.35)**3)
            h+=.00035*math.sin(11*theta+3*u)*math.sin(17*u)*math.sin(math.pi*u)*min(1,(u/.35)**3)
            if sign==1: h*=1+.012*math.sin(3*theta)*math.sin(math.pi*u)
            th=theta-.075*math.exp(-((1-t)/.023)**2)*math.sin(math.pi*u)**2
            verts.append((r*math.cos(th),sign*h,r*math.sin(th)))
layer=1+N*M
def V(side,i,j): return side*layer+1+(i%N)*M+j
for s in (0,1):
    center=s*layer
    for i in range(N):
        k=(i+1)%N; seam=(i==N-1)
        faces.append((center,V(s,i,0),V(s,k,0))); face_regions.append(1 if seam else 0)
        for j in range(M-1):
            # Explicit triangle strips use consistent, deterministic diagonals.
            aa,bb,cc,dd=V(s,i,j),V(s,i,j+1),V(s,k,j+1),V(s,k,j)
            faces.extend([(aa,bb,cc),(aa,cc,dd)])
            region=1 if seam else 0
            face_regions.extend([region,region])
for i in range(N):
    k=(i+1)%N
    faces.append((V(0,i,M-1),V(1,i,M-1),V(1,k,M-1),V(0,k,M-1)))
    face_regions.append(1 if i==N-1 else 0)
# Pin measured silhouette envelope, thickness, ground and placement numerically.
mins=[min(v[k] for v in verts) for k in range(3)]; maxs=[max(v[k] for v in verts) for k in range(3)]
target=[P['in_plane_width'],P['maximum_axial_thickness'],P['maximum_diameter']]
scale=[target[k]/(maxs[k]-mins[k]) for k in range(3)]
verts=[((v[0]-(mins[0]+maxs[0])/2)*scale[0],v[1]*scale[1],(v[2]-mins[2])*scale[2]) for v in verts]
# Ground contact centre is the lowest perimeter point, not a bounding-box guess.
contact=min(verts,key=lambda v:v[2]); shift=contact[0]
verts=[(x-shift,y,z) for x,y,z in verts]
obj=mesh_object('involute-filled-shell',verts,faces,mats,col)
for p,region in zip(obj.data.polygons,face_regions):
    p.material_index=region
    p.use_smooth=(region!=1)
obj['morphology']='One mineral-filled involute shell; closed depression, not through-hole; broken solid terminal face.'
obj['reference']='USNM486615, Cobban/Kennedy2016 Plate17 and Plate18 figs2-3 only'
obj['scale_note']='D=220 mm from caption; W=188 mm and T=63 mm are photo-derived estimates +/-15%.'
record=export_asset('placenticeras',{'en':'Placenticeras compressed disc ammonite','zh':'Placenticeras（扁盘菊石）'},'geology',col,metadata={'generator':'source/generate.py','profile':'static-palette-stone-fossil','description':{'en':'Original low-poly fossil-form interpretation of P. costatum USNM486615; broad involute compressed shell with small closed umbilicus and infilled terminal break.','zh':'P. costatum USNM486615 化石形态原创模型；扁盘内卷、小型闭合脐部与矿物填充的破损终止面。'},'source':'https://doi.org/10.1515/agp-2016-0031'},output_root=out/'private'/'build',render=False,max_triangles=P['geometry_policy']['max_triangles'],max_materials=P['geometry_policy']['max_materials'],max_primitives=P['geometry_policy']['max_primitives'])
built=out/'private/build/placenticeras'
shutil.copy2(built/'placenticeras.glb',out/'model.glb'); shutil.copy2(built/'placenticeras.blend',out/'model.blend')
e=out/'qa/evidence'; e.mkdir(parents=True,exist_ok=True)
qa=json.loads((built/'qa.json').read_text()); qa['glb_sha256']=hashlib.sha256((out/'model.glb').read_bytes()).hexdigest()
(e/'technical.json').write_text(json.dumps(qa,indent=2)+'\n')
record['glb']='model.glb'; record['blend']='model.blend'; record['preview']='preview.png'; record['generator']='source/generate.py'; record['origin']='lowest fossil rim contact center, Blender Z=0'
record['parameters_sha256']=hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()
record['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
record['canonical_helpers_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE/'deps').glob('*.py')}
(e/'build.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('MADE',qa['glb_sha256'],record['triangles'],record['glb_bytes'])
