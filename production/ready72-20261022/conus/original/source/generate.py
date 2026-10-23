#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original deterministic Conus spurius fossil interpretation.
Usage: blender -b -t 2 --factory-startup --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Only Python source, params.json, deps/ and Blender 4.3.2 are required.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys, tempfile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy, bmesh
from asset_common import setup_scene, make_material, mesh_object, export_asset
P=json.loads((HERE/'params.json').read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True)
args=a.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
col=setup_scene('conus',seed=P['seed'])
ivory=make_material('fossil-ivory',P['palette']['ivory'],roughness=.83)
inside=make_material('aperture-inner-ivory',P['palette']['interior'],roughness=.9)
suture=make_material('subtle-fossil-suture',P['palette']['suture'],roughness=.88)
materials=[ivory,inside,suture]
# A C-section thick wall. Its missing angular sector is actual negative space,
# not a black stripe or double-sided alpha plane. Both ends are physical lips.
N=P['body_segments'];zs=P['body_z_m'];H=P['shoulder_height_m'];R=P['shoulder_radius_m'];th=P['wall_thickness_m']
vs=[]; fs=[]; mis=[]
for surface in (0,1):
    for j,z in enumerate(zs):
        t=z/H
        rr=P['anterior_radius_m']+(R-P['anterior_radius_m'])*t**P['body_profile_exponent']
        # Broad shoulders, gently convex taper. The front slot narrows naturally.
        for i in range(N+1):
            ang=math.radians(P['lip_angle_deg']+(P['body_wrap_deg']*i/N))
            flare=.00005*math.sin(math.pi*t)**.7*math.exp(-i/2.0)
            r=rr+flare-(th if surface else 0)
            x=r*math.cos(ang)-.00012*(1-t)
            y=r*math.sin(ang)
            vs.append((x,y,z))
L=len(zs);S=(N+1)*L
ix=lambda s,j,i:s*S+j*(N+1)+i
for s in (0,1):
    for j in range(L-1):
        for i in range(N):
            f=(ix(s,j,i),ix(s,j,i+1),ix(s,j+1,i+1),ix(s,j+1,i))
            fs.append(f if s==0 else tuple(reversed(f)));mis.append(0 if s==0 else 1)
for j in range(L-1):
    for i in (0,N):
        fs.append((ix(0,j,i),ix(0,j+1,i),ix(1,j+1,i),ix(1,j,i)));mis.append(0)
for j in (0,L-1):
    for i in range(N):
        fs.append((ix(0,j,i),ix(1,j,i),ix(1,j,i+1),ix(0,j,i+1)));mis.append(0)
body=mesh_object('body-whorl-with-open-aperture',vs,fs,materials,col)
for p,mi in zip(body.data.polygons,mis):p.material_index=mi
body['anatomy']='Thick tapered body whorl; genuinely open longitudinal aperture, inner lining, continuous outer lip.'
body['intentional_opening']='Angular sector between outer lip and columellar lip remains absent along entire body.'
# The short spire is a closed cap, with one continuous clockwise-outward
# spiral relief field. Phase depends on theta AND radius, never stacked rings.
A=P['spire_angular_segments'];B=P['spire_radial_rings'];turns=P['spire_turns']
vs=[(0,0,P['height_m'])];fs=[];mis=[]
def boundary_radius(theta):
    # Apertural notch in outermost whorl, aligned with the missing body sector.
    d=((math.degrees(theta)-335+180)%360)-180
    notch=.18*math.cos(d/25*math.pi/2)**2 if abs(d)<25 else 0
    return R*(1-notch)
for j in range(1,B+1):
    u=j/B
    for i in range(A):
        theta=2*math.pi*i/A
        r=boundary_radius(theta)*u
        phase=2*math.pi*turns*u+theta
        wave=P['suture_relief_m']*math.cos(phase)*math.sin(math.pi*u)**.65
        z=H+(P['height_m']-H)*(1-u)**1.07+wave
        vs.append((r*math.cos(theta),r*math.sin(theta),z))
idx=lambda j,i:1+(j-1)*A+(i%A)
for i in range(A):fs.append((0,idx(1,i),idx(1,i+1)));mis.append(0)
for j in range(1,B):
    for i in range(A):
        fs.append((idx(j,i),idx(j+1,i),idx(j+1,i+1),idx(j,i+1)))
        phase=2*math.pi*turns*((j+.5)/B)+2*math.pi*(i+.5)/A
        mis.append(2 if math.cos(phase)<-.95 else 0)
# Thick undersurface closes the cap without extending over aperture notch.
bottom=len(vs);vs.append((0,0,H-.00016))
bstart=len(vs)
for i in range(A):
    x,y,z=vs[idx(B,i)];vs.append((x,y,H-.00016))
for i in range(A):
    q=(i+1)%A
    fs.append((idx(B,i),bstart+i,bstart+q,idx(B,q)));mis.append(0)
    fs.append((bottom,bstart+q,bstart+i));mis.append(1)
spire=mesh_object('short-dextral-spiral-spire',vs,fs,materials,col)
for p,mi in zip(spire.data.polygons,mis):p.material_index=mi
spire['anatomy']='Short raised spiral spire with five dextral, clockwise-outward suture turns and outer apertural notch.'
spire['reconstruction']='Original parameterized interpretation; not a scanned specimen.'
# Visible internal columellar core: a closed D-section volume behind the
# aperture, not an image plane. It leaves a deep channel beside the outer lip.
# Only the curved front-facing portion can be seen through the mouth.
vs=[];fs=[];C=10;cz=zs[:-1]+[H-.0002]
for z in cz:
    t=z/H;rr=P['anterior_radius_m']+(R-P['anterior_radius_m'])*t**P['body_profile_exponent']
    for i in range(C+1):
        ang=math.pi+math.pi*i/C
        vs.append((rr*(.10+.78*math.cos(ang))-.00012*(1-t),rr*(.05+.78*math.sin(ang)),z))
for j in range(len(cz)-1):
    for i in range(C+1):
        q=(i+1)%(C+1)
        fs.append((j*(C+1)+i,j*(C+1)+q,(j+1)*(C+1)+q,(j+1)*(C+1)+i))
fs.append(tuple(reversed(tuple(range(C+1)))))
fs.append(tuple((len(cz)-1)*(C+1)+i for i in range(C+1)))
core=mesh_object('recessed-columellar-inner-wall',vs,fs,inside,col)
core['anatomy']='Interior columellar wall within body whorl; curved lining behind open slot; deep unfilled channel at outer lip.'
# Source geometric checks are kept separate from image/factual acceptance.
parts=[]
for obj in (body,spire,core):
    bm=bmesh.new();bm.from_mesh(obj.data);bm.normal_update()
    parts.append({'part':obj.name,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True)})
    bm.free()
assert all(x['boundary_edges']==0 and x['nonmanifold_edges']==0 and x['signed_volume_m3']>0 for x in parts)
with tempfile.TemporaryDirectory(prefix='conus-export-',dir=out) as td:
    meta=export_asset('conus',{'en':'Conus fossil cone-snail shell','zh':'Conus 锥形芋螺化石壳'},'geology',col,metadata={'generator':'source/generate.py','description':{'en':'Original low-poly Late Pliocene Conus spurius fossil interpretation after PRI 70343-1.','zh':'参考 PRI 70343-1 的上新世晚期芋螺化石原创低多边形诠释。'},'taxon':'Conus spurius (Gmelin, 1791)','specimen_reference':'PRI 70343-1','measurement_status':'Image-estimated, not specimen-exact; about 10–15% interpretation tolerance.','python_version':sys.version,'threejs_version':'0.180.0','sources':[{'title':'Neogene Atlas of Ancient Life: Conus spurius','url':'https://neogeneatlas.net/species/conus-spurius/'}]},output_root=td,render=False,**{k:P['geometry_budget'][k] for k in ('max_triangles','max_materials','max_primitives')})
    p=Path(td)/'conus'
    shutil.copy2(p/'conus.glb',out/'model.glb');shutil.copy2(p/'conus.blend',out/'model.blend')
    evidence=out/'qa'/'evidence';evidence.mkdir(parents=True,exist_ok=True)
    qa=json.loads((p/'qa.json').read_text());qa['glb']['file']='model.glb';write(evidence/'source-export.json',qa)
    meta.update(glb='model.glb',blend='model.blend',preview='preview.png',params_sha256=sha(HERE/'params.json'),generator_sha256=sha(__file__),dependency_inventory_sha256=sha(HERE/'dependencies.json'))
    write(evidence/'build-metadata.json',meta)
assert (out/'model.glb').stat().st_size<=P['geometry_budget']['max_glb_bytes']
write(out/'qa'/'evidence'/'geometry.json',{'status':'PASS','claim_scope':'Closed shell-wall volumes, real open cavity, profile dimensions and original procedural topology only; not independent visual or factual acceptance.','glb_sha256':sha(out/'model.glb'),'parts':parts,'aperture':{'method':'C-section wall omits 50 degrees; physical inner surface and joined rim. No black material or alpha mask.','outer_lip_angle_deg':P['lip_angle_deg'],'inner_lip_angle_deg':P['lip_angle_deg']+P['body_wrap_deg'],'anterior_open':True,'shoulder_height_m':H,'wall_thickness_m':th},'dextral_spire':{'phase':'2*pi*5*u + theta','constant_phase_direction':'Clockwise outward when viewed from +Z','turns':turns},'intentional_intersection':'Spire cap overlaps upper shell-wall attachment collar by 0.16 mm. Internal columellar core overlaps the hidden inside of body whorl and leaves a recessed open lip channel; not a boolean union or print-ready claim.'})
print('CONUS_BUILD_COMPLETE',sha(out/'model.glb'))
