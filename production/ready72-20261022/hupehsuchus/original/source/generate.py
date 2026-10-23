# SPDX-License-Identifier: MIT
"""Deterministic Hupehsuchus reconstruction; run with Blender 4.3.2, --threads 2.
blender -b --factory-startup --python source/generate.py -- --output /empty/output
Only dependencies declared under source/deps and adjacent params.json are used.
"""
from pathlib import Path
import sys, math, json, hashlib, argparse
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
a=argparse.ArgumentParser(); a.add_argument('--output',required=True)
args=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(args.output).resolve(); OUT.mkdir(parents=True,exist_ok=True)
E=OUT/'qa/evidence'; E.mkdir(parents=True,exist_ok=True)
def dump(path,obj): path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
C=setup_scene('hupehsuchus',seed=P['seed'])
M=[make_material(x['name'],x['hex'],roughness=x.get('roughness',.84)) for x in P['materials']]
# All coordinate arrays use actual meters and identity object transforms.
# Ring sections: Y position, half-width, half-height, center Z.
S=P['body_sections']
N=P['body_ring_sides']
v=[]; f=[]; mi=[]
for y,w,h,z in S:
    for j in range(N):
        t=2*math.pi*j/N
        v.append((w*math.cos(t),y,z+h*math.sin(t)))
for i in range(len(S)-1):
    for j in range(N):
        f.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
        q=math.sin(2*math.pi*(j+.5)/N)
        mi.append(0 if q>.30 else 2 if q<-.55 else 1)
# Cap with central vertices to avoid unstable high-order cap triangulation.
for i in (0,len(S)-1):
    end=len(v); v.append((0,S[i][0],S[i][3]))
    for j in range(N):
        f.append((end,i*N+j,i*N+(j+1)%N)); mi.append(1)
body=mesh_object('Body_neck_toothless_snout_and_compressed_tail',v,f,M[:3],C)
for p,k in zip(body.data.polygons,mi): p.material_index=k
body['anatomy']='One continuous profile loft: flattened narrow snout, distinct neck, stiff deep trunk, laterally compressed tapering tail.'
# Four paddle shells: rooted well inside torso; closed edge rings and faceted crown.
def paddles(name,outline,zbase):
    verts=[]; faces=[]; mats=[]
    for sign in (-1,1):
        n=len(outline); base=len(verts)
        cx=sum(p[0] for p in outline)/n; cy=sum(p[1] for p in outline)/n
        # Distal shell thinner than muscular embedded root.
        for layer in (-1,1):
            for x,y in outline:
                t=max(.0028,.0075-.020*x)
                verts.append((sign*x,y,zbase+layer*t))
        verts.extend([(sign*cx,cy,zbase-.008),(sign*cx,cy,zbase+.010)])
        for j in range(n):
            k=(j+1)%n
            faces.append((base+2*n,base+k,base+j)); mats.append(2)
            faces.append((base+2*n+1,base+n+j,base+n+k)); mats.append(0)
            faces.append((base+j,base+k,base+n+k,base+n+j)); mats.append(0)
    obj=mesh_object(name,verts,faces,M[:3],C)
    for p,k in zip(obj.data.polygons,mats): p.material_index=k
    obj['anatomy']='Bilateral closed solid paddles; no independent finger spines; roots overlap body volume.'
    return obj
fore=paddles('Fore_paddles_pair',P['fore_outline'],-.022)
hind=paddles('Hind_paddles_pair',P['hind_outline'],-.020)
# Low layered ossicles hug the convex dorsal midline, never floating above it.
def section(y):
    for a,b in zip(S,S[1:]):
        if a[0]<=y<=b[0]:
            t=(y-a[0])/(b[0]-a[0]); return [a[k]*(1-t)+b[k]*t for k in range(1,4)]
    raise ValueError(y)
def dorsal(x,y):
    w,h,z=section(y); return z+h*math.sqrt(max(0.,1-(x/w)**2))
av=[]; af=[]; armor_records=[]
for i in range(P['armor_count']):
    y=-.228+i*.018
    w,h,zc=section(y)
    width=min(.021,w*.62)
    # Closed pentagonal shield, two ridge levels, rear overlap; 5 mm emergence.
    poly=[(-width,y-.011), (width,y-.011), (width*.90,y+.006), (0,y+.014),(-width*.90,y+.006)]
    start=len(av)
    for x,yy in poly: av.append((x,yy,dorsal(x,yy)-.003))
    for x,yy in poly: av.append((x,yy,dorsal(x,yy)+.0025))
    av.append((0,y-.003,dorsal(0,y-.003)+.008))
    for j in range(5):
        k=(j+1)%5; af.append((start+j,start+k,start+5+k,start+5+j)); af.append((start+10,start+5+j,start+5+k))
    af.append(tuple(start+j for j in reversed(range(5))))
    armor_records.append({'center_y_m':y,'width_m':2*width,'ridge_emergence_m':.008,'root_burial_m':.003})
armor=mesh_object('Dorsal_low_overlapping_ossicles',av,af,M[3],C)
armor['anatomy']='Restrained overlapping ossicle ridge. Color and flesh cover are reconstruction choices, not an exposed bone claim.'
# Small eye domes and a closed mouth seam. No teeth, baleen, pouch or flukes.
ev=[]; ef=[]; em=[]
def ellipsoid(center,radii,material,segments=12,rings=6):
    base=len(ev)
    ev.append((center[0],center[1],center[2]+radii[2]))
    for k in range(1,rings):
        a=math.pi*k/rings
        for j in range(segments):
            t=2*math.pi*j/segments
            ev.append((center[0]+radii[0]*math.sin(a)*math.cos(t),center[1]+radii[1]*math.sin(a)*math.sin(t),center[2]+radii[2]*math.cos(a)))
    bottom=len(ev); ev.append((center[0],center[1],center[2]-radii[2]))
    for j in range(segments): ef.append((base,base+1+j,base+1+(j+1)%segments)); em.append(material)
    for k in range(rings-2):
        for j in range(segments):
            a=base+1+k*segments+j; b=base+1+k*segments+(j+1)%segments
            ef.append((a,b,b+segments,a+segments)); em.append(material)
    for j in range(segments): ef.append((bottom,base+1+(rings-2)*segments+(j+1)%segments,base+1+(rings-2)*segments+j)); em.append(material)
for sign in (-1,1):
    ellipsoid((sign*.0221,-.365,.025),(.0040,.0060,.0052),0)
    ellipsoid((sign*.0254,-.3655,.0255),(.0014,.0032,.0032),1)
eyes=mesh_object('Small_lateral_eyes',ev,ef,[M[4],M[5]],C)
for p,k in zip(eyes.data.polygons,em): p.material_index=k
# Narrow closed mouthline as tiny sealed tapered ribbons attached to skull sides.
mv=[]; mf=[]
ys=[-.494,-.482,-.465,-.440,-.414,-.392,-.378]
for sign in (-1,1):
    base=len(mv)
    for y in ys:
        w,h,z=section(y); zz=z-.0013
        xx=w*math.sqrt(1-((zz-z)/h)**2)
        for dx,dz in ((-.00055,-.0005),(.00040,-.0005),(.00040,.0005),(-.00055,.0005)):
            mv.append((sign*(xx+dx),y,zz+dz))
    for k in range(len(ys)-1):
        for j in range(4): mf.append((base+4*k+j,base+4*k+(j+1)%4,base+4*(k+1)+(j+1)%4,base+4*(k+1)+j))
    mf.append(tuple(base+j for j in reversed(range(4))))
    mf.append(tuple(base+4*(len(ys)-1)+j for j in range(4)))
mouth=mesh_object('Closed_toothless_mouthline',mv,mf,M[5],C)
root=bpy.data.objects['hupehsuchus']; root['mount']='Suspended swim mount at (0,0,0), within trunk core; no floor-contact requirement.'
root['interpretation']='Whole organism, neutral closed mouth, disputed feeding ecology not enacted.'
bpy.context.view_layer.update()
source=audit_source(C,max_triangles=P['budget']['max_triangles'])
if source['errors']: raise RuntimeError(source['errors'])
bpy.context.scene['asset_license']='CC-BY-4.0'; bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in C.all_objects: obj.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing: raise RuntimeError('Missing exporter flags: '+str(missing))
bpy.ops.export_scene.gltf(**options)
g=audit_glb(OUT/'model.glb',P['budget']['max_triangles'],P['budget']['max_materials'],P['budget']['max_primitives'])
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(g['bounds_m'][s][i]-expected[s][i]) for s in expected for i in range(3))
assert delta<1e-4 and g['scene_triangles']==source['triangles']
assert not g['errors'] and g['bytes']<=P['budget']['max_glb_bytes'],g
assert g['materials']<=P['budget']['max_materials'] and g['scene_primitives_estimated_base_draw_calls']<=P['budget']['max_primitives'],g
build={'status':'PASS','scope':'Source/export technical checks; not independent visual or target-runtime approval','asset_id':'hupehsuchus','revision':'r001','glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'generator_sha256':sha(Path(__file__)),'params_sha256':sha(HERE/'params.json'),'blender':bpy.app.version_string,'seed':P['seed'],'units':'meters','mount':'Suspended at trunk core (0,0,0)','source':source,'export_options':{k:v for k,v in options.items() if k!='filepath'},'bounds_roundtrip_max_error_m':delta,'blender_glTF_exporter_version':'4.3.47','target_threejs_version':'0.180.0','target_threejs_status':'NOT_RUN'}
dump(E/'build.json',build); dump(E/'geometry.json',g)
dump(E/'anatomy-design.json',{'glb_sha256':sha(OUT/'model.glb'),'scope':'Generator design parameters, not independent factual validation','body_sections':S,'paddles':{'count':4,'fore_outline':P['fore_outline'],'hind_outline':P['hind_outline'],'root_overlap':'Roots embedded 10-20 mm inside the body shell, visually inspected in exact-GLB images'},'armor':armor_records,'mouth':'Closed toothless seam only; no feeding-specific tissue','eye_centers':[[s*.0221,-.365,.025] for s in [-1,1]],'body_shading':'Flat profile facets with three countershading material bands','reference_note':'Distal tail and living soft tissue inferred, fossil A tail exits frame.'})
print('BUILD_COMPLETE',json.dumps({'triangles':g['scene_triangles'],'primitives':g['scene_primitives_estimated_base_draw_calls'],'materials':g['materials'],'glb_sha256':g['sha256']}))
