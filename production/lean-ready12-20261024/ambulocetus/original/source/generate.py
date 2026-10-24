#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Ambulocetus loft reconstruction. Run with Blender --background --python.
All geometry is authored here, not derived from third-party meshes or pixels.
The frozen params describe interpretive anatomy, not fossil measurements.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
N=32
V=[]; F=[]; M=[]
def vertex(v):
    V.append(tuple(v)); return len(V)-1
def face(ids,mat=1):
    F.append(tuple(ids)); M.append(mat)
def bridge(a,b,mat=1):
    assert len(a)==len(b)
    for i in range(len(a)): face([a[i],a[(i+1) % len(a)],b[(i+1) % len(b)],b[i]],mat)
def cap(r,mat=1):
    c=vertex(sum((Vector(V[i]) for i in r),Vector())/len(r))
    for i in range(len(r)):face([r[i],r[(i+1) % len(r)],c],mat)
# y, half-width, lower surface, upper surface, lateral center, mouth-level (head only).
PROFILES=[
 (-1.60,.025,.538,.592,0,.560),(-1.58,.102,.485,.664,0,.563),
 (-1.53,.122,.471,.688,0,.566),(-1.45,.127,.465,.707,0,.570),
 (-1.36,.130,.460,.716,0,.574),(-1.26,.134,.453,.734,0,.578),
 (-1.16,.146,.440,.770,0,.584),(-1.08,.164,.429,.813,0,.590),
 (-1.00,.178,.426,.827,0,.596),(-.92,.174,.413,.813,0,None),
 (-.84,.183,.360,.791,0,None),(-.75,.228,.259,.811,0,None),
 (-.66,.286,.170,.848,0,None),(-.56,.323,.123,.872,0,None),
 (-.46,.344,.101,.886,0,None),(-.36,.354,.092,.887,0,None),
 (-.23,.358,.085,.878,0,None),(-.08,.354,.093,.856,0,None),
 (.07,.339,.115,.820,0,None),(.19,.324,.131,.775,0,None),
 (.29,.323,.137,.748,0,None),(.39,.309,.143,.721,0,None),
 (.49,.277,.159,.676,0,None),(.59,.233,.180,.604,0,None),
 (.70,.189,.185,.521,.005,None),(.83,.145,.169,.433,.018,None),
 (.98,.109,.142,.346,.040,None),(1.13,.079,.119,.280,.071,None),
 (1.28,.055,.104,.226,.107,None),(1.41,.037,.096,.190,.132,None),
 (1.53,.023,.092,.161,.143,None),(1.63,.012,.094,.140,.141,None),
 (1.70,.0035,.110,.118,.135,None)]
R=[]
for y,w,lo,hi,cx,mouth in PROFILES:
    ring=[]
    for j in range(N):
        a=2*math.pi*j/N; s=math.sin(a); c=math.cos(a)
        if mouth is not None:
            # Deep lower jaw and upper muzzle with a recessed, almost-closed mouth seam.
            z=mouth+(hi-mouth)*max(s,0)+(mouth-lo)*min(s,0)
            near=min(j % 16,16-j % 16)
            if near==0: z=mouth; xx=c*w*.925
            elif near==1:
                z=mouth+(1 if s>0 else -1)*.009
                xx=c*w*1.015
            else: xx=c*w
        else:
            z=(hi+lo)/2+(hi-lo)/2*s
            xx=c*w
        ring.append(vertex((cx+xx,y,z)))
    R.append(ring)
# Rectangular apertures in the trunk loft form actual limb sockets, not overlaps.
SOCKETS=[]
for side in (1,-1):
    for label,ri,rj in [('fore',12,15),('hind',19,22)]:
        # Five angular segments, straddling the lower lateral flank.
        start=29 if side==1 else 14
        end=start+5
        SOCKETS.append((side,label,ri,rj,start,end))
def excluded(i,j):
    return any(ri<=i<rj and j in {a % N for a in range(st,en)} for _,_,ri,rj,st,en in SOCKETS)
def skinmat(i,j):
    y,w,lo,hi,cx,mouth=PROFILES[i]
    a=2*math.pi*(j+.5)/N
    if mouth is not None and i<8 and j in (0,15,16,31):return 4
    return 0 if math.sin(a)>.42 else 2 if math.sin(a)<-.60 else 1
# Eye socket patches replace ordinary body faces, so no detached eyeball islands exist.
EYES={(7,3),(7,12)}
NOSTRILS={(1,5),(1,10)}
def inset_patch(outer,kind):
    p=[Vector(V[i]) for i in outer]
    center=sum(p,Vector())/4
    normal=(p[1]-p[0]).cross(p[3]-p[0]).normalized()
    radial=Vector((center.x,0,center.z-.59))
    if normal.dot(radial)<0:normal=-normal
    # Eight-sided oval within a single quad; lip and central dark inset share edges.
    u=(p[1]-p[0]+p[2]-p[3])/2; v=(p[3]-p[0]+p[2]-p[1])/2
    scale=.28 if kind=='eye' else .23
    inside=[]
    for k in range(8):
        angle=math.pi/4*k
        inside.append(vertex(center+u*math.cos(angle)*scale+v*math.sin(angle)*scale+normal*(.002 if kind=='eye' else -.001)))
    # Align outer corners with ring diagonals and fill each quadrant with triangles.
    # Each corner corresponds to one diagonal (5,7,1,3) in this uv convention.
    ix=[5,7,1,3]
    for k in range(4):
        a=ix[k]; b=ix[(k+1) % 4]; mid=(a+1) % 8
        face([outer[k],outer[(k+1) % 4],inside[b]],0)
        face([outer[k],inside[b],inside[mid]],0)
        face([outer[k],inside[mid],inside[a]],0)
    c=vertex(center+normal*(.005 if kind=='eye' else -.002))
    for k in range(8):face([inside[k],inside[(k+1) % 8],c],3)
for i in range(len(R)-1):
    for j in range(N):
        if excluded(i,j):continue
        outer=[R[i][j],R[i+1][j],R[i+1][(j+1) % N],R[i][(j+1) % N]]
        if (i,j) in EYES:inset_patch(outer,'eye')
        elif (i,j) in NOSTRILS:inset_patch(outer,'nostril')
        else:face(outer,skinmat(i,j))
cap(R[0],1); cap(R[-1],0)

def foot_outline(kind):
    # A single continuous fleshy outline. Five hand lobes; four longer hind lobes.
    pts=[]
    if kind=='fore':
        centers=[-.081,-.0405,0,.0405,.081]; lengths=[.166,.211,.234,.218,.176]
        half=.02025; valley=.133
        for c,l in zip(centers,lengths):
            pts.extend([(c-half,-valley),(c-half*.76,-l+.018),(c,-l),(c+half*.76,-l+.018)])
        width=.104
    else:
        centers=[-.102,-.034,.034,.102]; lengths=[.331,.413,.430,.365]
        half=.034; valley=.267
        for c,l in zip(centers,lengths):
            pts.extend([(c-half,-valley),(c-half*.83,-l+.035),(c-half*.32,-l+.006),(c+half*.32,-l),(c+half*.83,-l+.028)])
        width=.138
    pts.extend([(width,-valley*.90),(width*.98,-valley*.60),(width*.87,-valley*.30),
                (width*.72,0),(width*.48,.047),(width*.18,.062),(-width*.18,.062),
                (-width*.48,.047),(-width*.72,0),(-width*.87,-valley*.30),
                (-width*.98,-valley*.60),(-width,-valley*.90)])
    assert len(pts)==32
    return pts

LIMB_INFO=[]; JOINT_VERTICES=set()
for side,kind,ri,rj,st,en in SOCKETS:
    boundary=[R[i][st % N] for i in range(ri,rj)]
    boundary +=[R[rj][j % N] for j in range(st,en)]
    boundary +=[R[i][en % N] for i in range(rj,ri,-1)]
    boundary +=[R[ri][j % N] for j in range(en,st,-1)]
    assert len(boundary)==16
    JOINT_VERTICES.update(boundary)
    center=sum((Vector(V[i]) for i in boundary),Vector())/len(boundary)
    if kind=='fore':
        paths=[((side*.352,-.485,.401),.122,.122),((side*.405,-.374,.294),.109,.103),
               ((side*.448,-.330,.220),.093,.085),((side*.481,-.416,.152),.075,.071),
               ((side*.498,-.552,.105),.059,.057),((side*.503,-.616,.081),.052,.050)]
        ankle=Vector((side*.503,-.616,.081)); angle=side*math.radians(12)
    else:
        paths=[((side*.360,.279,.376),.143,.137),((side*.423,.188,.288),.130,.116),
               ((side*.489,.160,.210),.102,.087),((side*.520,.275,.146),.081,.073),
               ((side*.543,.427,.105),.062,.061),((side*.549,.481,.081),.057,.055)]
        ankle=Vector((side*.549,.481,.081)); angle=side*math.radians(19)
    centers=[Vector(c) for c,_,_ in paths]
    tangent=(centers[0]-center).normalized()
    axis1=Vector((0,1,0)); axis1=(axis1-tangent*axis1.dot(tangent)).normalized()
    axis2=tangent.cross(axis1).normalized()
    offset=Vector(V[boundary[0]])-center
    phase=math.atan2(offset.dot(axis2),offset.dot(axis1))
    b1=Vector(V[boundary[1]])-center
    direction=1 if offset.cross(b1).dot(tangent)>0 else -1
    previous=boundary
    for k,(c,rx,ry) in enumerate(paths):
        current=centers[k]
        tangent=((centers[k+1]-centers[max(0,k-1)]) if k<len(paths)-1 else Vector((0,0,-1))).normalized()
        axis1=(axis1-tangent*axis1.dot(tangent)).normalized(); axis2=tangent.cross(axis1).normalized()
        ring=[vertex(current+axis1*(math.cos(phase+direction*2*math.pi*j/N)*rx)+axis2*(math.sin(phase+direction*2*math.pi*j/N)*ry)) for j in range(N)]
        if k<2:JOINT_VERTICES.update(ring)
        if len(previous)==16:
            for j in range(16):
                a=previous[j]; b=previous[(j+1) % 16]; q=2*j
                face([a,b,ring[(q+2) % N],ring[(q+1) % N]],1)
                face([a,ring[(q+1) % N],ring[q]],1)
        else:bridge(previous,ring,1)
        previous=ring
    outline=[]
    for x,y in foot_outline(kind):
        outline.append(Vector((ankle.x+math.cos(angle)*side*x-math.sin(angle)*y,
                               ankle.y+math.sin(angle)*side*x+math.cos(angle)*y,0)))
    # Choose a cyclic ordering matching the ankle ring, without changing topology.
    prevdirs=[(Vector(V[i])-ankle).normalized() for i in previous]
    best=None
    for rev in (1,-1):
        for shift in range(N):
            inds=[(shift+rev*j) % N for j in range(N)]
            cost=sum((prevdirs[j]-Vector((outline[inds[j]].x-ankle.x,outline[inds[j]].y-ankle.y,0)).normalized()).length_squared for j in range(N))
            if best is None or cost<best[0]:best=(cost,inds)
    outline=[outline[i] for i in best[1]]
    for scale,z in ((.49,.072),(.83,.050),(1,.024),(1,0)):
        ring=[vertex((ankle.x+(p.x-ankle.x)*scale,ankle.y+(p.y-ankle.y)*scale,z)) for p in outline]
        bridge(previous,ring,1 if z>.024 else 2); previous=ring
    # A common sole center is inside this star-shaped outline; no separate toe capsules.
    cap(previous,2)
    LIMB_INFO.append({'name':('right-' if side==1 else 'left-')+kind,'digits':5 if kind=='fore' else 4,'connected_socket_edges':16,'foot_outline_vertices':32})


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def json_write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def build(out):
    out.mkdir(parents=True,exist_ok=True)
    coll=setup_scene('ambulocetus',seed=P['seed'])
    mats=[make_material(name,color,P['surface']['roughness']) for name,color in list(P['surface']['palette_srgb_hex'].items())[:5]]
    used=sorted({i for f in F for i in f}); remap={old:i for i,old in enumerate(used)}
    animal=mesh_object('Integrated-animal-skin',[V[i] for i in used],[[remap[i] for i in f] for f in F],mats,coll)
    for p,idx in zip(animal.data.polygons,M):p.material_index=idx
    # Relax only anatomical socket neighborhoods; the deliberately authored profiles remain intact.
    bm=bmesh.new();bm.from_mesh(animal.data);bm.verts.ensure_lookup_table()
    selection=[bm.verts[remap[i]] for i in JOINT_VERTICES if i in remap]
    for _ in range(5):bmesh.ops.smooth_vert(bm,verts=selection,factor=.38,use_axis_x=True,use_axis_y=True,use_axis_z=True)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(animal.data);bm.free();animal.data.update()
    animal['construction']='Single connected loft skin: muzzle, jaw seam, neck, trunk, tail, four socket-bridged limbs and lobed soles.'
    animal['interpretation']='Soft tissue, skin coloration and stance are artistic reconstruction.'
    animal['hind_toes_per_foot']=4;animal['fingers_per_hand']=5
    scene=bpy.context.scene
    scene.render.threads_mode='FIXED';scene.render.threads=2
    source=audit_source(coll,P['geometry_budget']['max_triangles'])
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0
    scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:
                    space.params.directory=b'//'
                    space.params.filename=''
    for text in list(bpy.data.texts):bpy.data.texts.remove(text)
    # Disable the user-environment filename from the saved startup preferences.
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in coll.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=animal
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
      export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',
      export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,
      export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,
      export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Missing explicit exporter options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    glb=audit_glb(out/'model.glb',12000,8,48)
    glb['file']='model.glb'
    if glb['errors']:raise RuntimeError(glb['errors'])
    src=source['bounds_blender_m']; expected={'min':[src['min'][0],src['min'][2],-src['max'][1]],'max':[src['max'][0],src['max'][2],-src['min'][1]]}
    delta=max(abs(expected[s][i]-glb['bounds_m'][s][i]) for s in ['min','max'] for i in range(3))
    if delta>1e-4 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source-to-export mismatch')
    bm=bmesh.new();bm.from_mesh(animal.data)
    seen=set();components=[]
    for v in bm.verts:
        if v.index in seen:continue
        stack=[v];count=0
        while stack:
            cur=stack.pop()
            if cur.index in seen:continue
            seen.add(cur.index);count+=1;stack += [e.other_vert(cur) for e in cur.link_edges]
        components.append(count)
    signed_volume=bm.calc_volume(signed=True);bm.free()
    if len(components)!=1:raise RuntimeError('Unexpected disconnected skin components')
    semantic={'vertices':[[round(x,7) for x in v.co] for v in animal.data.vertices],
              'polygons':[list(f.vertices) for f in animal.data.polygons],
              'materials':[f.material_index for f in animal.data.polygons],
              'palette':P['surface']['palette_srgb_hex']}
    normalized=hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    import io_scene_gltf2
    data={'asset_id':'ambulocetus','revision':'r001','status':'PASS_SCOPED_TECHNICAL_ONLY',
          'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'exporter_version':list(io_scene_gltf2.bl_info['version']),
          'source_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),
          'seed':P['seed'],'export_options':opts,'source':source,'glb':glb,
          'bounds_roundtrip_max_error_m':delta,'normalized_geometry_material_sha256':normalized,
          'connected_components':components,'closed_skin_signed_volume_m3':signed_volume,
          'limb_topology':LIMB_INFO,'limitations':['Numeric checks do not establish anatomy, beauty, independent review, browser GPU, scene performance, user approval or publication.']}
    json_write(out/'qa/evidence/source-export.json',data)
    return coll

if __name__=='__main__':
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=HERE.parent)
    args=parser.parse_args(argv);build(args.out.resolve())
