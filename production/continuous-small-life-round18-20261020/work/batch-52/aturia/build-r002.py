# SPDX-License-Identifier: MIT
"""Original full-volume Aturia-inspired fossil shell; no incorporated meshes."""
import sys,json,math,argparse,time
from pathlib import Path
from datetime import datetime,timezone
import bpy
R=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,ground_asset,export_asset
p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);c=json.loads(a.config.read_text());t=time.monotonic();col=setup_scene('aturia',c['seed']);N=c['segments'];K=c['radial_rings'];v=[];f=[]
# Two radial shell faces meet at one shared outer rim. Front/back dimple and spiral
# groove are real geometry, with generous quiet whorl area and no concentric ribbing.
def radius(theta):
    return 1+.025*math.cos(theta-.25)-.045*math.exp(-((math.atan2(math.sin(theta+.65),math.cos(theta+.65)))/.24)**2)
def depth(r,theta):
    bulge=math.sqrt(max(0,1-r*r))*(.68+.32*(1-math.exp(-(r/.105)**2)))
    dist=min(abs(r-.10*math.exp(.24*(theta+2*math.pi*k))) for k in range(-2,3))
    groove=.048*math.exp(-(dist/.030)**2)*(1-r)**.35
    return max(.005,bulge-groove)
# normalized radius rows avoid center duplicates; outside rim shared.
centers=[];rows={}
for side in [-1,1]:
    centers.append(len(v));v.append((0,side*.0525*.68,.11))
    for k in range(1,K):
        r=k/K;rows[side,k]=len(v)
        for j in range(N):
            th=2*math.pi*j/N;rr=r*radius(th);v.append((.12*rr*math.cos(th),side*.0525*depth(r,th),.11+.11*rr*math.sin(th)))
rim=len(v)
for j in range(N):
    th=2*math.pi*j/N;rr=radius(th);v.append((.12*rr*math.cos(th),0,.11+.11*rr*math.sin(th)))
for si,side in enumerate([-1,1]):
    for j in range(N):
        face=(centers[si],rows[side,1]+j,rows[side,1]+(j+1)%N);f.append(face if side==-1 else tuple(reversed(face)))
    for k in range(1,K):
        r1=rows[side,k];r2=rows[side,k+1] if k+1<K else rim
        for j in range(N):
            face=(r1+j,r2+j,r2+(j+1)%N,r1+(j+1)%N);f.append(face if side==-1 else tuple(reversed(face)))
mat=[make_material(n,h,roughness=.92) for n,h in zip(['chalk-sandstone','warm-fossil-patch','pale-rim'],c['palette'])]
o=mesh_object('inflated-involute-fossil-shell',v,f,mat[0],col)
for m in mat[1:]:o.data.materials.append(m)
for poly in o.data.polygons:
    # Broad coherent patch fields only; no random face confetti.
    q=poly.center;theta=math.atan2(q.z-.11,q.x);r=math.sqrt((q.x/.12)**2+((q.z-.11)/.11)**2)
    poly.material_index=1 if .4<r<.88 and .2<theta<1.0 else 2 if r>.91 else 0
# Recalculate winding independently of parametrization, preserve deliberate facets.
import bmesh
bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
ground_asset(col)
a.output.mkdir(parents=True,exist_ok=True)
# helper appends slug; temporary staging remains per-run and never references another asset.
out=export_asset('aturia',{'en':'Aturia-inspired fossil shell','zh':'Aturia 灵感化石壳'},'mollusk',col,metadata={'description':'Original smooth involute fossil-form teaching prop. Artistic scale and palette; not a specimen facsimile.','nominal_dimensions_blender_xyz_m':[.24,.105,.22]},output_root=a.output/'stage',render=False,max_triangles=14000,max_materials=6,max_primitives=30)
import shutil
for file in (a.output/'stage/aturia').iterdir():shutil.move(str(file),a.output/file.name)
shutil.rmtree(a.output/'stage')
(a.output/'build-timing.json').write_text(json.dumps({'finished_at':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'threads':2,'note':'Blender generator/export execution only; active authoring time unrecorded.'},indent=2)+'\n')
