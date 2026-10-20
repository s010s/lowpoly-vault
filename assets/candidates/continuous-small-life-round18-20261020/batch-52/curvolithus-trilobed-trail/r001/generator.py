# SPDX-License-Identifier: MIT
"""Original deterministic integral height-field Curvolithus-inspired relief."""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy
REPO = next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').is_file())
sys.path.insert(0,str(REPO/'scripts'))
from asset_common import setup_scene, make_material, mesh_object, export_asset

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--config',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    c=json.loads(args.config.read_text())
    col=setup_scene(c['asset_id'],c['seed'])
    mats=[make_material(n,color) for n,color in zip(('sandstone-surface','sediment-upper-layer','sediment-base'),c['palette'])]
    # Three lobes are one continuous surface, including their substrate.
    offsets=[-.05,-.048,-.044,-.039,-.033,-.027,-.024,-.019,-.012,0,.012,.019,.024,.027,.033,.039,.044,.048,.05]
    heights=[0,.003,.006,.0072,.006,.003,.0018,.006,.011,.014,.011,.006,.0018,.003,.006,.0072,.006,.003,0]
    rows=c['longitudinal_samples']; verts=[]; faces=[]; mids=[]
    for i in range(rows):
        t=i/(rows-1); y=-.16+.32*t
        center=c['trail_amplitude_m']*math.sin(2*math.pi*(t-.12))
        # Bevelled angular corners taper only at the slab ends; no uniform noise.
        edge=.12-.023*max(0,(abs(y)-.125)/.035)
        left=-edge+.002*math.sin(3*math.pi*t)
        right=edge+.002*math.sin(4*math.pi*t)
        xvals=[left,left+.005,center-.075]+[center+x for x in offsets]+[center+.075,right-.005,right]
        taper=max(0,min(1,(.145-abs(y))/.023))
        taper=taper*taper*(3-2*taper)
        for j,x in enumerate(xvals):
            relief=heights[j-3]*taper if 3<=j<3+len(offsets) else 0
            z=.033+relief
            if j in (0,len(xvals)-1):z-=.003
            verts.append((x,y,z))
    cols=len(xvals)
    for i in range(rows-1):
        for j in range(cols-1):
            a=i*cols+j
            faces.append((a,a+1,a+1+cols,a+cols));mids.append(0)
    # Perimeter in consistent winding, with thick editable sediment wall rings.
    perimeter=list(range(cols))+[i*cols+cols-1 for i in range(1,rows)]+list(range((rows-1)*cols+cols-2,(rows-1)*cols-1,-1))+[i*cols for i in range(rows-2,0,-1)]
    prev=perimeter
    for z,scale,mi in [(.009,1.002,1),(0,.975,2)]:
        ring=[]
        for ix in perimeter:
            x,y,_=verts[ix];ring.append(len(verts));verts.append((x*scale,y*scale,z))
        for k in range(len(ring)):
            n=(k+1)%len(ring);faces.append((prev[k],prev[n],ring[n],ring[k]));mids.append(mi)
        prev=ring
    faces.append(tuple(reversed(prev)));mids.append(2)
    # Match only this asset's explicitly frozen nominal XYZ target.
    bounds=[(min(v[k] for v in verts),max(v[k] for v in verts)) for k in range(3)]
    dims=c['nominal_blender_xyz_m']
    verts=[tuple((v[k]-(bounds[k][0]+bounds[k][1])/2)*dims[k]/(bounds[k][1]-bounds[k][0]) if k<2 else (v[k]-bounds[k][0])*dims[k]/(bounds[k][1]-bounds[k][0]) for k in range(3)) for v in verts]
    obj=mesh_object('integral-trilobed-relief-and-slab',verts,faces,mats[0],col)
    for mat in mats[1:]:obj.data.materials.append(mat)
    for poly,mi in zip(obj.data.polygons,mids):
        poly.material_index=mi
        poly.use_smooth=mi==0
    obj['construction']='Closed integral positive-relief surface, no copied mesh'
    output=export_asset(c['asset_id'],{'en':'Curvolithus trilobed trail','zh':'Curvolithus 三叶爬迹'},'traces',col,output_root=args.output_dir,render=False,max_triangles=14000,max_materials=6,max_primitives=30,metadata={'revision':c['revision'],'nominal_artistic_blender_xyz_m':dims,'scientific_scope':'Stylized trace morphology, illustrative slab; no producer, species, measured specimen, age or locality asserted.','generator':'generator.py','preview_status':'pending exact-GLB proof'})
    print('BUILD_OUTPUT='+str(output))

if __name__=='__main__':main()
