#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original male Protoceras celer, Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT [--gray]
No external asset, template mesh, network, or undeclared authoring file is read.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, render_previews
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
A=argparse.ArgumentParser(); A.add_argument('--out',type=Path,required=True); A.add_argument('--gray',action='store_true')
a=A.parse_args(sys.argv[sys.argv.index('--')+1:]); out=a.out.resolve(); out.mkdir(parents=True,exist_ok=True)
col=setup_scene('protoceras',P['seed'])
M=[make_material(n,c,roughness=r) for n,c,r in P['palette']]
parts=[]

def obj(name,v,f,mi=0,indices=None):
    o=mesh_object(name,v,f,[M[i] for i in mi] if isinstance(mi,list) else M[mi],col)
    if indices:
        for p,i in zip(o.data.polygons,indices): p.material_index=i
    parts.append(o); return o

def loft(name,sections,n=12,mi=0,paint=None):
    # Rings in the XZ plane; y,longitudinal, z,height, rx,rz.
    v=[];f=[];ids=[]
    for k,(y,z,rx,rz) in enumerate(sections):
        for j in range(n):
            t=2*math.pi*j/n
            v.append((rx*math.cos(t),y,z+rz*math.sin(t)))
    for k in range(len(sections)-1):
        for j in range(n):
            # Alternating diagonals make restrained deliberate facets.
            q=(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j)
            if (j+k)%2: fs=[(q[0],q[1],q[3]),(q[1],q[2],q[3])]
            else: fs=[(q[0],q[1],q[2]),(q[0],q[2],q[3])]
            for face in fs:
                f.append(face); ids.append(paint(k,j) if paint else 0)
    for k in (0,len(sections)-1):
        c=len(v); y,z,rx,rz=sections[k];v.append((0,y,z))
        for j in range(n): f.append((c,k*n+j,k*n+(j+1)%n));ids.append(0)
    return obj(name,v,f,mi,ids)

def tube(name,sections,n=10,mi=0,paint=None):
    # Freely bent centerline with two separately sized local radii.
    v=[];f=[];ids=[]
    for k,(co,r1,r2) in enumerate(sections):
        c=Vector(co)
        prev=Vector(sections[max(0,k-1)][0]);nxt=Vector(sections[min(len(sections)-1,k+1)][0]);t=(nxt-prev).normalized()
        u=Vector((1,0,0));u=(u-t*u.dot(t)).normalized();w=t.cross(u).normalized()
        for j in range(n):
            ang=2*math.pi*j/n;v.append(tuple(c+u*(r1*math.cos(ang))+w*(r2*math.sin(ang))))
    for k in range(len(sections)-1):
        for j in range(n):
            q=(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j)
            f.append(q);ids.append(paint(k,j) if paint else 0)
    for k in (0,len(sections)-1):
        c=len(v);v.append(sections[k][0])
        for j in range(n): f.append((c,k*n+j,k*n+(j+1)%n));ids.append(0)
    return obj(name,v,f,mi,ids)

def ellipsoid(name,c,r,mi=0,n=12,rings=6):
    v=[(c[0],c[1],c[2]+r[2])];f=[]
    for i in range(1,rings):
        th=math.pi*i/rings
        for j in range(n):
            t=2*math.pi*j/n;v.append((c[0]+r[0]*math.sin(th)*math.cos(t),c[1]+r[1]*math.sin(th)*math.sin(t),c[2]+r[2]*math.cos(th)))
    bot=len(v);v.append((c[0],c[1],c[2]-r[2]))
    for j in range(n): f.append((0,1+j,1+(j+1)%n))
    for i in range(rings-2):
        for j in range(n):q=(1+i*n+j,1+i*n+(j+1)%n,1+(i+1)*n+(j+1)%n,1+(i+1)*n+j);f.append(q)
    for j in range(n):f.append((bot,1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n))
    return obj(name,v,f,mi)

def leaf(name,root,mid,tip,width,thick,mi=0,inner=False):
    # Closed flattened convex blade, not an open double-sided card.
    r,m,t=map(Vector,(root,mid,tip));axis=(t-r).normalized();u=Vector((0,1,0));u=(u-axis*u.dot(axis)).normalized();normal=axis.cross(u).normalized()
    outline=[r,m-u*width,t,m+u*width]
    v=[tuple(p+normal*thick) for p in outline]+[tuple(p-normal*thick) for p in outline]
    v.extend([tuple(m+normal*thick*2),tuple(m-normal*thick*2)])
    f=[];idx=[]
    for j in range(4):f.append((8,j,(j+1)%4));idx.append(1 if inner else 0)
    for j in range(4):f.append((9,4+(j+1)%4,4+j));idx.append(0)
    for j in range(4):f.append((j,4+j,4+(j+1)%4,(j+1)%4));idx.append(0)
    return obj(name,v,f,mi,idx)

# Torso: long, compact ribcage with raised withers, a tucked belly and narrow rump.
loft('Torso_ribcage',[(.385,.510,.012,.030),(.35,.527,.060,.075),(.285,.529,.090,.091),(.20,.518,.101,.093),(.09,.515,.105,.095),(-.02,.519,.103,.094),(-.12,.533,.094,.094),(-.21,.527,.079,.088),(-.275,.506,.045,.063),(-.292,.498,.014,.028)],16,[0,1],lambda k,j:1 if j>=9 and j<=14 else 0)
# Broad insertion and continuously tapered moderate neck, with no separate ball joint.
tube('Neck_moderate', [((0,-.235,.505),.061,.061),((0,-.256,.56),.064,.067),((0,-.30,.622),.056,.060),((0,-.345,.683),.045,.050),((0,-.392,.733),.037,.043),((0,-.419,.752),.031,.034)],14,[0,1],lambda k,j:1 if 3<=j<=5 else 0)
# Anatomical head length is 0.215 m: occiput -0.415 to premaxillary tip -0.630.
loft('Skull_long_rostrum', [(-.415,.752,.029,.034),(-.438,.758,.043,.039),(-.460,.757,.047,.041),(-.485,.749,.038,.034),(-.515,.736,.029,.026),(-.550,.725,.024,.022),(-.589,.714,.023,.020),(-.617,.710,.024,.018),(-.630,.710,.019,.014)],14,[0,1],lambda k,j:1 if 8<=j<=12 else 0)
# Restrained soft tissue jaw contour.
loft('Lower_jaw', [(-.443,.732,.027,.019),(-.472,.723,.032,.018),(-.515,.710,.023,.013),(-.568,.699,.019,.011),(-.614,.697,.018,.010),(-.626,.701,.015,.007)],10,0)
ellipsoid('Nose_soft_rhinarium',(0,-.629,.712),(.020,.008,.013),2,n=12,rings=5)
for s,side in ((-1,'L'),(1,'R')):
    # Eyes are lateral and slightly anterior of the posterior projections.
    ellipsoid('Orbital_rim_'+side,(s*.044,-.462,.765),(.009,.018,.017),3,n=12,rings=5)
    ellipsoid('Lateral_eye_'+side,(s*.050,-.467,.767),(.006,.010,.010),4,n=12,rings=6)
    # Ears separate from horns, rearward and lateral.
    leaf('Ear_'+side,(s*.025,-.414,.769),(s*.065,-.386,.806),(s*.092,-.367,.831),.017,.006,[0,1],True)
    # Paired maxillary PLATES: broad anteroposterior basis, thin X dimension,
    # convex outer face and inward-curved tip with a persistent median gap.
    tube('Maxillary_plate_'+side,[((s*.027,-.558,.733),.008,.034),((s*.037,-.559,.758),.011,.034),((s*.041,-.565,.787),.010,.029),((s*.032,-.566,.818),.008,.017),((s*.025,-.562,.827),.004,.008)],10,3)
    # Supraorbital flares are low, sideways wing-like plates, NOT tall conical horns.
    leaf('Supraorbital_flare_'+side,(s*.030,-.468,.787),(s*.061,-.462,.793),(s*.081,-.458,.788),.025,.005,3)
    # Posterior flattened parietal projections: diverge a little outward and back.
    tube('Parietal_projection_'+side,[((s*.028,-.428,.779),.012,.017),((s*.039,-.423,.802),.012,.014),((s*.045,-.415,.830),.009,.011),((s*.044,-.413,.843),.004,.005)],9,3)
    # Short small canine points; no upturned or gigantic elephant tusks.
    tube('Upper_canine_'+side,[((s*.022,-.591,.706),.0045,.005),((s*.026,-.589,.691),.0035,.004),((s*.029,-.593,.681),.0012,.0015)],8,5)

# Connected gracile limbs, with different fore and hind joint articulation.
for s,side in ((-1,'L'),(1,'R')):
    stagger=.018 if s<0 else -.018
    x=s*.076;fy=-.215+stagger
    tube('Forelimb_'+side,[((s*.048,-.185,.558),.032,.034),((s*.068,-.19,.474),.025,.029),((x,-.17,.388),.022,.022),((x,fy+.005,.272),.013,.015),((x,fy,.222),.016,.016),((x,fy-.002,.125),.010,.012),((x,fy-.007,.064),.017,.017),((x,fy-.013,.033),.022,.018)],10,[0,3],lambda k,j:1 if k>=5 else 0)
    hy=.265-stagger
    tube('Hindlimb_'+side,[((s*.050,.28,.555),.036,.040),((s*.068,.246,.462),.030,.037),((x,.207,.393),.023,.027),((x,.271,.301),.016,.019),((x,.304,.232),.017,.019),((x,.285,.150),.010,.012),((x,hy,.064),.014,.016),((x,hy-.01,.032),.018,.019)],10,[0,3],lambda k,j:1 if k>=5 else 0)
    # Four functional fore digits. Separate geometry preserves the grooves.
    vs=[];fs=[]
    for idx,offset in enumerate((-.026,-.009,.009,.026)):
        outer=idx in (0,3);w=.0075 if outer else .0085; y0=fy+(.006 if outer else .0);length=.037 if outer else .049;bottom=.003 if outer else 0
        rings=[(bottom,w*.98,y0-length*.54,length*.46),(.014,w,y0-length*.52,length*.48),(.034 if outer else .039,w*.80,y0-length*.29,length*.30)]
        start=len(vs);n=8
        for z,rx,cy,ry in rings:
            for j in range(n):
                th=2*math.pi*j/n;vs.append((x+offset+rx*math.cos(th),cy+ry*math.sin(th),z))
        for k in range(2):
            for j in range(n):fs.append((start+k*n+j,start+k*n+(j+1)%n,start+(k+1)*n+(j+1)%n,start+(k+1)*n+j))
        fs += [tuple(start+j for j in reversed(range(n))),tuple(start+2*n+j for j in range(n))]
    obj('Forefoot_four_digits_'+side,vs,fs,2)
    vs=[];fs=[]
    for offset in (-.011,.011):
        start=len(vs);n=8
        for z,rx,cy,ry in [(0,.010,hy-.026,.028),(.015,.0105,hy-.025,.027),(.039,.009,hy-.012,.018)]:
            for j in range(n):th=2*math.pi*j/n;vs.append((x+offset+rx*math.cos(th),cy+ry*math.sin(th),z))
        for k in range(2):
            for j in range(n):fs.append((start+k*n+j,start+k*n+(j+1)%n,start+(k+1)*n+(j+1)%n,start+(k+1)*n+j))
        fs += [tuple(start+j for j in reversed(range(n))),tuple(start+2*n+j for j in range(n))]
    # Two short non-grounding rudimentary hind side digits, in the same editable foot.
    for offset in (-.016,.016):
        start=len(vs)
        vs.extend([(x+offset-.005,hy-.005,.040),(x+offset+.005,hy-.005,.040),(x+offset+.005,hy+.007,.055),(x+offset-.005,hy+.007,.055),(x+offset,hy,.063)])
        fs.extend([tuple(start+i for i in face) for face in [(0,1,2,3),(0,4,1),(1,4,2),(2,4,3),(3,4,0)]])
    obj('Hindfoot_two_main_two_rudimentary_'+side,vs,fs,2)

tube('Tail_short', [((0,.36,.551),.020,.021),((0,.402,.548),.016,.016),((.008,.443,.523),.011,.012),((.013,.468,.493),.006,.008),((.016,.476,.479),.002,.003)],10,0)
# Footprint-root Y centered on the contact interval midpoint. Keep source/anatomy definition explicit.
contact_min=min(v.co.y for o in parts if 'foot_' in o.name for v in o.data.vertices if v.co.z<.004)
contact_max=max(v.co.y for o in parts if 'foot_' in o.name for v in o.data.vertices if v.co.z<.004)
origin_y=(contact_min+contact_max)/2
for o in parts:
    for v in o.data.vertices:v.co.y-=origin_y
bpy.context.view_layer.update()
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
scene['reconstruction_notes']='Male Protoceras celer; original surface reconstruction. Skull 215 mm. Whole body proportions, coat, ears and tail illustrative, not fossil measurements.'
scene['model_revision']=P['revision'];scene['original_inventory_ordinal']=654
root=bpy.data.objects[col['asset_root']];root['definition']='Whole living male, 2 maxillary plates + 2 low supraorbital flares + 2 parietal projections; forefoot four functional digits, hind two main and two rudimentary.'
source=audit_source(col,max_triangles=16000)
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Exporter flags missing: '+repr(missing))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(out/'model.glb',max_triangles=16000,max_materials=6,max_primitives=48)
if glb['errors']:raise RuntimeError(glb['errors'])
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][s][i]-expected[s][i]) for s in ('min','max') for i in range(3))
assert delta<.0001 and glb['scene_triangles']==source['triangles']
assert glb['bytes']<=2000000
report={'asset_id':'protoceras','revision':P['revision'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'origin_y_shift_m':origin_y,'blender':bpy.app.version_string,'exporter_version':'4.3.47','export_options':{k:v for k,v in options.items() if k!='filepath'},'scale_notes':{'skull_length_m':.215,'skull_length_definition':'occiput to premaxillary tip along original Y; soft-tissue nose projects an extra 7 mm','body_length_m':1.0,'shoulder_height_m':.61,'body_scale_status':'illustrative'},'semantic_parts':[o.name for o in parts]}
(out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
if a.gray:
    gray=make_material('_Gray_selfcheck','#929292',roughness=.85)
    bpy.context.view_layer.material_override=gray
    render_previews(col,out/'gray',views=('front','side','top','hero'),resolution=480,samples=8)
print('BUILD_COMPLETE '+glb['sha256'])
