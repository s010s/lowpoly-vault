# SPDX-License-Identifier: MIT
"""Deterministic original Pleurotomaria shell. Blender 4.3.2, palette only.
A welded helicoidal outer sheet avoids buried overlapping whorl tubes.
The incomplete fossil lip, short slit, and shallow interior are interpretations.
Usage: blender -b -t 2 --python generate.py -- --output /path/output
"""
from pathlib import Path
import sys, json, math, argparse, hashlib, shutil
from collections import defaultdict
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb
A=argparse.ArgumentParser(); A.add_argument('--output',type=Path,required=True); A.add_argument('--clay',action='store_true'); args=A.parse_args(sys.argv[sys.argv.index('--')+1:])
p=json.loads((HERE/'params.json').read_text()); out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
col=ac.setup_scene(p['asset_id'],p['seed']); scene=bpy.context.scene
scene.render.threads_mode='FIXED'; scene.render.threads=2
stone=ac.make_material('weathered limestone shell', '#A9987F',.93)
inside=ac.make_material('conservatively reconstructed shallow interior','#756953',.98)
edge=ac.make_material('subtle shell sculpture','#B1A28D',.94)
M=96; N=5; K=.44; Q=math.exp(K); RF=.0185; C=2.; H=.062
# (normalized vertical interval, radius / R). Distinct broad shoulder ramp,
# restrained shoulder nodes, flat selenizone with two boundaries + median cord.
profile=[(0,.63),(.065,.73),(.13,.83),(.20,.94),(.25,1.005),(.29,1.02),(.34,1.017),(.40,1.015),(.45,1.016),(.49,1.025),(.515,1.028),(.54,1.012),(.565,1.013),(.585,1.024),(.605,1.013),(.62,1.0125),(.63,1.012),(.655,1.028),(.68,1.024),(.73,1.015),(.80,1.00),(.88,.985),(.94,.974),(1,.63*Q)]
P=len(profile); verts=[]; ids={}; faces=[]; mats=[]
def vertex(co): verts.append(tuple(co)); return len(verts)-1
for i in range(N*M+1):
    t=i/M; theta=2*math.pi*(N-t); R=RF*math.exp(K*(t-N))
    for j,(f,r) in enumerate(profile):
        # Exact seam identity stitches the lower edge to the next-turn upper edge.
        if j==P-1 and i+M<=N*M: continue
        nodal=.027*max(0,math.cos(theta*21+.3))**4 * math.exp(-((f-.255)/.065)**2)
        growth=.0022*math.cos(theta*63+f*.9)*math.sin(math.pi*f)**2
        radius=R*(r+nodal+growth)
        z=H-C*R*(1+(Q-1)*f)
        # The last whorl has a nearly level, shallow-convex base. Only its
        # short inner columellar transition rises to the preceding suture.
        if t>N-1 and f>.34:
            u=t-(N-1)
            baseline=H-C*RF*Q
            lowedge=baseline+(H-C*RF-baseline)*max(0.,1-u/.13)**2
            original_low=H-C*R*Q
            w=((f-.34)/.66)**1.5
            z+=(lowedge-original_low)*w
        ids[i,j]=vertex((radius*math.cos(theta),radius*math.sin(theta),z))
for i in range(N*M+1):
    if i+M<=N*M: ids[i,P-1]=ids[i+M,0]
# Slit is a real opening in the outer shell sheet, not a material stripe.
# Last two longitudinal strips, between selenizone boundaries.
slit_start=N*M-2; slit_j0=12; slit_j1=15
for i in range(N*M):
    for j in range(P-1):
        if i>=slit_start and slit_j0<=j<slit_j1: continue
        faces.append((ids[i,j],ids[i+1,j],ids[i+1,j+1],ids[i,j+1])); mats.append(0)
# The closed umbilicus is a shallow convex basal fan, never a basal hole.
# Build a two-ring base between the exposed last-turn lower edge and central plug.
base_indices=[ids[i,P-1] for i in range((N-1)*M,N*M+1)]
base_z=min(verts[x][2] for x in base_indices)-.0009
base_center=vertex((0,0,base_z))
mid=[]
for n,vi in enumerate(base_indices):
    x,y,z=verts[vi]; mid.append(vertex((x*.48,y*.48,base_z+(z-base_z)*.12)))
for n in range(M):
    faces.append((base_indices[n],base_indices[n+1],mid[n+1],mid[n])); mats.append(0)
    faces.append((mid[n],mid[n+1],base_center)); mats.append(0)
# Enumerate manifold boundary loops. One is the worn apical remnant, one aperture.
def loops_now():
    edges=defaultdict(list)
    for face in faces:
        for a,b in zip(face,face[1:]+face[:1]): edges[tuple(sorted((a,b)))].append((a,b))
    adj=defaultdict(list)
    for (a,b),uses in edges.items():
        if len(uses)==1: adj[a].append(b); adj[b].append(a)
    assert all(len(x)==2 for x in adj.values()), 'Boundary is not an unbranched loop'
    remaining=set(adj); loops=[]
    while remaining:
        start=min(remaining); cur=start; prev=None; loop=[]
        while True:
            loop.append(cur); remaining.discard(cur)
            nxt=adj[cur][0] if adj[cur][0]!=prev else adj[cur][1]
            prev,cur=cur,nxt
            if cur==start: break
        loops.append(loop)
    return loops
loops=loops_now(); assert len(loops)==2,len(loops)
apex=max(loops,key=lambda l:sum(verts[v][2] for v in l)/len(l))
aperture=min(loops,key=lambda l:sum(verts[v][2] for v in l)/len(l))
apex_z=max(verts[v][2] for v in apex)-.00022
apex_center=vertex((0,0,apex_z))
for a,b in zip(apex,apex[1:]+apex[:1]): faces.append((a,b,apex_center)); mats.append(0)
# Cavity follows the aperture and slit outline with a thin inferred lip.
# No detailed internal whorl anatomy is asserted. The recess ends at a simple cap.
center=Vector((RF*.52,0,(min(verts[v][2] for v in aperture)+max(verts[v][2] for v in aperture))*.5))
previous=aperture
for scale,depth in [(.955,.00065),(.89,.002),(.70,.0045)]:
    ring=[]
    for vi in aperture:
        co=Vector(verts[vi]); co=center+(co-center)*scale; co.y+=depth
        ring.append(vertex(co))
    for a in range(len(ring)):
        b=(a+1)%len(ring); faces.append((previous[a],previous[b],ring[b],ring[a])); mats.append(1)
    previous=ring
back=vertex((center.x,.0048,center.z))
for a,b in zip(previous,previous[1:]+previous[:1]): faces.append((a,b,back)); mats.append(1)
obj=ac.mesh_object('shell with stepped whorls and disclosed slit',verts,faces,[stone,inside,edge],col)
for poly,mi in zip(obj.data.polygons,mats): poly.material_index=mi; poly.use_smooth=True
# Apply size in vertex coordinates, keeping the identity root and object transforms.
vs=obj.data.vertices; lo=[min(v.co[i] for v in vs) for i in range(3)]; hi=[max(v.co[i] for v in vs) for i in range(3)]
scale=(p['width']/(hi[0]-lo[0]),p['depth']/(hi[1]-lo[1]),p['height']/(hi[2]-lo[2]))
for v in vs:
    v.co.x*=scale[0]; v.co.y*=scale[1]; v.co.z=(v.co.z-lo[2])*scale[2]
obj.data.update()
# Remove no topology; recalculate consistent exterior normals and verify the signed volume.
bm=bmesh.new(); bm.from_mesh(obj.data); bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context="VERTS"); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
if bm.calc_volume(signed=True)<0: bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
edge_counts={'boundary':sum(e.is_boundary for e in bm.edges),'nonmanifold':sum(not e.is_manifold for e in bm.edges)}
volume=bm.calc_volume(signed=True); bm.to_mesh(obj.data); bm.free()
assert not edge_counts['nonmanifold'],edge_counts
obj['observed']='Five stepped whorls, broad shoulder ramp, nodules, mid-face selenizone, closed umbilicus'
obj['inferred']='Aperture continuation, shallow interior and short open slit; not an exact specimen facsimile'
obj['specimen']='CNP-PIIc0440, Ferrari 2020 Figure 5 A-G; no type-status claim'
if args.clay:
    gray=ac.make_material('authoring gray','#929292',.85)
    for i in range(len(obj.data.materials)): obj.data.materials[i]=gray
source=ac.audit_source(col,max_triangles=40000)
assert not source['errors'],source
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects: o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
actual={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}; assert set(opts)<=actual
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(out/'model.glb',40000,6,8); assert not glb['errors'],glb
slit_a=Vector(verts[ids[N*M,slit_j0]]); slit_b=Vector(verts[ids[slit_start,slit_j0]])
slit_w=abs(verts[ids[N*M,slit_j1]][2]-verts[ids[N*M,slit_j0]][2])*scale[2]
report={'asset_id':p['asset_id'],'revision':p['revision'],'status':'PASS','blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'source':source,'glb':glb,'topology':{**edge_counts,'signed_volume_m3':volume,'method':'Welded source mesh edge incidence and coherent normals; no claim of print-ready exact fossil'},'slit':{'interpretation':True,'approx_length_m':(slit_b-slit_a).length*sum(scale[:2])/2,'approx_vertical_width_m':slit_w,'target_length_m':p['slit_length_inferred'],'target_width_m':p['slit_width_inferred']},'export_options':{k:v for k,v in opts.items() if k!='filepath'},'source_blend_has_no_preview_objects':all(o.type in {'MESH','EMPTY'} for o in bpy.data.objects),'runtime':'Three.js GPU and populated scene not run by maker'}
(out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'])
