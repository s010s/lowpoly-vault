#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original parametric articulated Paraspirifer fossil-form; no borrowed mesh."""
from pathlib import Path
import sys, json, math, hashlib, argparse
import bpy
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(Path(__file__).parent/'helpers'))
from asset_common import setup_scene, mesh_object, make_material, export_asset
p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=ROOT/'build'); p.add_argument('--parameters',type=Path,default=ROOT/'source/parameters.json')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
c=json.loads(a.parameters.read_text()); N=c['angular_segments']; R=c['radial_rings']; tau=2*math.pi
collection=setup_scene('paraspirifer',seed=c['seed'])
materials=[make_material(s['name'],s['srgb'],roughness=s['roughness'],metallic=0) for s in c['palette']]
verts=[]; faces=[]; mids=[]; groups={'dorsal_fold':[], 'ventral_sulcus':[], 'continuous_commissure':[]}

def boundary(j):
    th=tau*j/N
    x=.020*math.sin(th)
    y=-.015*math.cos(th)
    if y>.007:
        y=.007+(y-.007)*.45+.004*math.exp(-(x/.005)**2)
    # Anterior central indentation is modest in plan, strong in vertical profile.
    front=max(0,math.cos(th))
    y += .00115*math.exp(-(x/.005)**2)*front**3
    z=.0046*math.exp(-(x/.0058)**2)*front**2
    z += .0010*math.exp(-(x/.005)**2)*max(0,-math.cos(th))**2
    # Broad shoulder outline; simplified continuous radial rib scalloping.
    r=.00020*(1+math.cos(tau*j/4))/2
    x += r*math.sin(th); y -= r*math.cos(th)
    return x,y,z

def vertex(sign,t,j):
    xb,yb,zb=boundary(j); focus_y=.0106
    x=t*xb; y=focus_y+t*(yb-focus_y)
    hump=math.sin(math.pi*t)**.78
    front=max(0,min(1,(focus_y-yb)/.018))
    ray_length=math.hypot(xb,yb-focus_y)
    inflation_weight=min(1.0,ray_length/.023)
    center=math.exp(-(x/(.0013+.0043*t))**2)*front
    # Opposite exterior domes share one closed rim. Lower positive displacement
    # is the ventral sulcus; upper positive displacement is the dorsal fold.
    if sign==1:
        z=.0135*math.sqrt(max(0,1-t**1.5)) + t*zb + .0016*center*math.sin(math.pi*t)
    else:
        z=(1-t)*.0025 + t*zb - .0105*hump*inflation_weight + .0048*center*math.sin(math.pi*t)
    # Moderately spaced original costae, not noisy facets or scan damage.
    rib=(1+math.cos(tau*j/4))/2
    amp=.00048*(math.sin(math.pi*t/2)**.7)*(1-.65*center)
    z += sign*amp*rib*(1-t)**.35
    # Converge relief into matching seam rather than opening a gap.
    z += sign*.000045*t**12
    return x,y,z

rings={}
for sign,name in ((1,'dorsal_fold'),(-1,'ventral_sulcus')):
    center_id=len(verts); verts.append((0,.0106,.0135 if sign==1 else .0025)); groups[name].append(center_id)
    rs=[]
    for ri in range(1,R+1):
        t=ri/R
        ids=[]
        for j in range(N):
            ids.append(len(verts)); groups[name].append(len(verts)); verts.append(vertex(sign,t,j))
        rs.append(ids)
    for j in range(N):
        faces.append((center_id,rs[0][j],rs[0][(j+1)%N])); mids.append(0)
    for ri in range(R-1):
        for j in range(N):
            # Consistent quads preserve editable radial flow. Actual triangulation
            # is fixed by Blender and inspected from the exact GLB.
            faces.append((rs[ri][j],rs[ri+1][j],rs[ri+1][(j+1)%N],rs[ri][(j+1)%N]))
            # Low-contrast limestone zones; no randomly scattered color chips.
            mids.append(1 if ri in (4,8) else 2 if j%4==2 and ri>2 else 0)
    rings[sign]=rs
# The two valve exteriors form one manifold surface, with a closed dark rim band.
for j in range(N):
    ids=(rings[1][-1][j],rings[-1][-1][j],rings[-1][-1][(j+1)%N],rings[1][-1][(j+1)%N])
    faces.append(ids); mids.append(3); groups['continuous_commissure'].extend(ids)
# Exact metric width and floor-contact origin are baked into vertices.
width=max(v[0] for v in verts)-min(v[0] for v in verts); scale=c['width_m']/width
verts=[tuple(q*scale for q in v) for v in verts]
lowz=min(v[2] for v in verts)
contact=[v for v in verts if abs(v[2]-lowz)<1e-9]
ycontact=sum(v[1] for v in contact)/len(contact)
verts=[(x,y-ycontact,z-lowz) for x,y,z in verts]
obj=mesh_object('Articulated shell · dorsal fold + ventral sulcus',verts,faces,materials,collection)
for poly,mi in zip(obj.data.polygons,mids): poly.material_index=mi
for name,ids in groups.items():
    vg=obj.vertex_groups.new(name=name); vg.add(sorted(set(ids)),1.0,'REPLACE')
obj['construction']='One watertight exterior with separately editable dorsal, ventral and commissure vertex groups; no hidden internal faces.'
obj['uncertainty']='40 mm approximate width from PRI 76796; length, depth and hidden rear form are artistic estimates.'
obj['source_specimen']='PRI 76796, corroboration PRI 76880; references consulted, no source mesh copied.'
# Preserve source and parameters directly in the blend for editing and rebuild.
for f in (Path(__file__),a.parameters):
    text=bpy.data.texts.new(f.name); text.write(f.read_text())
metadata={'description':{'en':'Original low-poly fossil-form interpretation of Paraspirifer, with a deep biconvex shell, median dorsal fold and opposing ventral sulcus. Approximately 40 mm wide; hidden depth is an artistic estimate.','zh':'Paraspirifer 原创低多边形化石形态：深厚双凸壳、中央背褶与相对腹沟。宽约 40 毫米，隐藏厚度为艺术估计。'},'generator':'source/build_paraspirifer.py','revision':c['revision'],'scientific_scope':'Genus-level stylized fossil-form informed by named P. bownockeri specimens, not an exact specimen replica.','references':'references.json','sources':[{'id':'PRI-76796','url':'https://sketchfab.com/3d-models/brachiopod-paraspirifer-bownockeri-pri-76796-1cf9f4fbf7a745c2a1ec15e2b76195b4'},{'id':'PRI-76880','url':'https://sketchfab.com/3d-models/brachiopod-paraspirifer-bownockeri-pri-76880-091de1e5940144d9a5222ea29a37a303'}],'reconstruction_notes':['Conservative closed commissure; no invented internal organs or large aperture.','Width follows PRI approximate 4 cm; other dimensions, palette, rib simplification and hidden posterior geometry are artistic.','No scan-derived meshes, photographs or textures are incorporated.','Ventral sulcus and dorsal fold are semantic mesh regions sharing a manifold closed exterior.'],'runtime_profile':{'three':'0.180.0','gltf_validator':'2.0.0-dev.3.10','surface':'palette-only opaque single-sided'},'parameters_sha256':hashlib.sha256(a.parameters.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'reviewed_warnings':[]}
record=export_asset('paraspirifer',{'en':'Paraspirifer barrel-wing brachiopod','zh':'Paraspirifer 桶翼腕足动物'},'animals',collection,metadata=metadata,output_root=a.output,render=False,max_triangles=c['max_triangles'],max_materials=4,max_primitives=4)
print('BUILD_RESULT '+json.dumps({'glb_sha256':record['sha256']['glb'],'triangles':record['triangles'],'glb_bytes':record['glb_bytes'],'dimensions':record['dimensions']}))
