# SPDX-License-Identifier: MIT
"""Original whole-body Holmesina reconstruction. No external reference textures.
Model proportions are estimates, not a composite measured individual.
Run in Blender 4.3.2 with -- --output-dir OUTPUT.
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
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);OUT=a.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene('holmesina',P['seed']);ROOT=bpy.data.objects[COL['asset_root']]
M={k:make_material(k,c,roughness=.85 if k!='eye' else .3) for k,c in P['palette_srgb'].items()}
FORMS=[]
def loft(name,sections,mat='skin',axis='Y',n=16):
    vs=[];fs=[]
    for pos,c1,c2,r1,r2 in sections:
        for j in range(n):
            ang=2*math.pi*j/n
            vs.append((c1+r1*math.cos(ang),pos,c2+r2*math.sin(ang)) if axis=='Y' else (c1+r1*math.cos(ang),c2+r2*math.sin(ang),pos))
    for i in range(len(sections)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.extend([tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))])
    return mesh_object(name,vs,fs,M[mat],COL)
def ell(name,c,r,mat,n=12,k=6):
    vs=[(c[0],c[1],c[2]-r[2])];fs=[]
    for i in range(1,k):
        t=-math.pi/2+math.pi*i/k
        for j in range(n):
            u=2*math.pi*j/n;vs.append((c[0]+r[0]*math.cos(t)*math.cos(u),c[1]+r[1]*math.cos(t)*math.sin(u),c[2]+r[2]*math.sin(t)))
    end=len(vs);vs.append((c[0],c[1],c[2]+r[2]))
    for j in range(n):fs.append((0,1+(j+1)%n,1+j))
    for i in range(k-2):
        b=1+i*n
        for j in range(n):fs.append((b+j,b+(j+1)%n,b+n+(j+1)%n,b+n+j))
    b=1+(k-2)*n
    for j in range(n):fs.append((b+j,b+(j+1)%n,end))
    return mesh_object(name,vs,fs,M[mat],COL)
def join(name,objs):
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objs:ob.select_set(True)
    bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();ob=objs[0];ob.name=name;return ob
# The low, barrel-shaped trunk sits under an elongated armored back.
FORMS.append(loft('Trunk_loft',[(y,0,z,w,h) for y,z,w,h in [(-.58,.48,.19,.215),(-.45,.47,.25,.245),(-.22,.45,.29,.21),(.10,.44,.30,.20),(.40,.43,.27,.20),(.59,.42,.18,.15),(.67,.39,.055,.07)]]))
FORMS.append(loft('Neck_loft',[(y,0,z,w,h) for y,z,w,h in [(-.78,.45,.07,.08),(-.69,.46,.095,.105),(-.56,.48,.15,.13),(-.45,.49,.19,.14)]]))
# Long low wedge head: the nose is narrow, but never an anteater tube.
FORMS.append(loft('Long_narrow_head',[(y,0,z,w,h) for y,z,w,h in [(-1.06,.365,.027,.023),(-1.02,.385,.037,.036),(-.94,.42,.050,.055),(-.86,.455,.066,.075),(-.77,.485,.087,.095),(-.70,.485,.081,.083)]],n=20))
FORMS.append(loft('Closed_mandible',[(y,0,z,w,h) for y,z,w,h in [(-1.045,.345,.026,.014),(-.97,.36,.043,.025),(-.87,.385,.058,.037),(-.77,.420,.073,.043),(-.70,.44,.064,.044)]],n=16))
for s,side in [(-1,'L'),(1,'R')]:
    FORMS.append(loft('Forelimb_'+side,[(.055,s*.262,-.405,.055,.075),(.13,s*.263,-.375,.054,.056),(.24,s*.270,-.340,.061,.068),(.35,s*.251,-.395,.083,.097),(.48,s*.225,-.40,.093,.106)],axis='Z'))
    FORMS.append(loft('Hindlimb_'+side,[(.055,s*.258,.455,.060,.079),(.13,s*.261,.495,.053,.059),(.23,s*.268,.475,.063,.074),(.34,s*.264,.385,.090,.105),(.48,s*.22,.385,.112,.119)],axis='Z'))
    for label,y in [('Fore',-.435),('Hind',.435)]:
        FORMS.append(loft(label+'_foot_'+side,[(0,s*.263,y-.02,.058,.090),(.025,s*.263,y-.026,.075,.104),(.070,s*.263,y,.066,.086),(.105,s*.263,y+.026,.049,.057)],axis='Z'))
# Preserve every semantic skin construction form, separate from EXPORT.
SC=bpy.data.collections.new('SOURCE_FORMS');bpy.context.scene.collection.children.link(SC)
for ob in FORMS:
    cp=ob.copy();cp.data=ob.data.copy();cp.name='EDIT_'+ob.name;cp.parent=None;SC.objects.link(cp);cp.hide_render=True;cp.hide_set(True)
SC.hide_viewport=True;SC.hide_render=True
skin=join('Continuous_living_skin',FORMS)
r=skin.modifiers.new('Skin_union','REMESH');r.mode='VOXEL';r.voxel_size=P['body_voxel_m'];r.use_smooth_shade=False;bpy.ops.object.modifier_apply(modifier=r.name)
r=skin.modifiers.new('Surface_relaxation','SMOOTH');r.factor=.42;r.iterations=2;bpy.ops.object.modifier_apply(modifier=r.name)
skin.data.calc_loop_triangles();r=skin.modifiers.new('Lowpoly_skin','DECIMATE');r.ratio=min(1,P['body_target_triangles']/len(skin.data.loop_triangles));r.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=r.name)
# Ground contact at the four feet, with upper morphology unchanged.
minz=min(v.co.z for v in skin.data.vertices)
for v in skin.data.vertices:
    if v.co.z<.09:v.co.z=max(0,v.co.z-minz)
skin.data.materials.clear();skin.data.materials.append(M['skin'])
# Armored surface profile. The shell is open below, with a genuinely modeled rim.
PROFILE=[(-.54,.255,.735),(-.45,.305,.770),(-.25,.343,.792),(-.10,.355,.800),(.18,.360,.795),(.36,.350,.770),(.53,.310,.705),(.66,.205,.570)]
def shape(y):
    for a,b in zip(PROFILE,PROFILE[1:]):
        if a[0]<=y<=b[0]:
            t=(y-a[0])/(b[0]-a[0]);return a[1]*(1-t)+b[1]*t,a[2]*(1-t)+b[2]*t
    return PROFILE[0][1:] if y<PROFILE[0][0] else PROFILE[-1][1:]
def surf(y,theta,offset=0):
    w,z=shape(y);c=max(0,math.cos(theta));return (w*math.sin(theta)+offset*math.sin(theta),y,.31+(z-.31)*c**.72+offset*c)
def base_shell(name,ys,mat,underlap=False):
    n=24;vs=[];fs=[]
    for layer in [0,-.018]:
        for row,y in enumerate(ys):
            for j in range(n+1):vs.append(surf(y,-math.pi/2+math.pi*j/n,layer-(.012 if underlap and row==len(ys)-1 else 0)))
    rows=len(ys);side=rows*(n+1)
    for layer in [0,1]:
        for i in range(rows-1):
            for j in range(n):
                b=layer*side+i*(n+1)+j;fs.append((b,b+1,b+n+2,b+n+1))
    perimeter=list(range(n+1))+[i*(n+1)+n for i in range(1,rows)]+list(range((rows-1)*(n+1)+n-1,(rows-1)*(n+1)-1,-1))+[i*(n+1) for i in range(rows-2,0,-1)]
    for i,j in zip(perimeter,perimeter[1:]+perimeter[:1]):fs.append((i,j,j+side,i+side))
    ob=mesh_object(name,vs,fs,M[mat],COL);return ob
# Thick bases are continuous shoulder and pelvis bucklers, never independent blocks.
base_shell('Shoulder_buckler',[ -.54,-.45,-.34,-.23,-.12],'armor')
base_shell('Pelvic_buckler',[ .18,.29,.40,.51,.60,.66],'armor')
# Each raised tile is a low polygonal central island with sloping, depressed edges.
# Group tile islands by semantic buckler or band, not hundreds of objects.
def tiles(name,intervals,cols,band=False):
    vs=[];fs=[];mats=[]
    for row,(ya,yb) in enumerate(intervals):
        for j in range(cols):
            ta=-math.pi/2+math.pi*j/cols;tb=-math.pi/2+math.pi*(j+1)/cols
            ym=(ya+yb)/2;tm=(ta+tb)/2;dy=(yb-ya)*.45;dt=(tb-ta)*.46
            uv=[(-1,-1),(1,-1),(1,1),(-1,1)] if band else [(-1,-.50),(0,-1),(1,-.50),(1,.50),(0,1),(-1,.50)]
            nv=len(uv)
            b=len(vs)
            for scale,h in [(1,.004),(.76 if band else .69,.022 if band else .011)]:
                for u,v in uv:
                    lift=h+((1-v)*.005 if band else 0)
                    vs.append(surf(ym+v*dy*scale,tm+u*dt*scale,lift))
            for k in range(nv):fs.append((b+k,b+(k+1)%nv,b+nv+(k+1)%nv,b+nv+k));mats.append(0)
            fs.append(tuple(b+nv+k for k in range(nv)));mats.append(1 if band or (j+row)%5 in (0,2) else 0)
            fs.append(tuple(b+k for k in reversed(range(nv))));mats.append(0)
    ob=mesh_object(name,vs,fs,[M['armor'],M['ridges']],COL)
    for p,mi in zip(ob.data.polygons,mats):p.material_index=mi
    return ob
# Polygonal scutes on the bucklers; rectangular-elongate scutes on mobile rows.
tiles('Shoulder_polygonal_scutes',[(-.535,-.445),(-.440,-.342),(-.337,-.235),(-.230,-.125)],16)
tiles('Pelvic_polygonal_scutes',[(.185,.275),(.280,.370),(.375,.465),(.470,.555),(.560,.650)],16)
for i,(ya,yb) in enumerate([(-.116,-.024),(-.019,.073),(.078,.172)],1):
    base_shell('Mobile_band_%d_base'%i,[ya,(ya+yb)/2,yb,yb+.012],'band',True)
    tiles('Mobile_band_%d_elongate_scutes'%i,[(ya+.003,yb-.003)],23,True)
# Long tapering tail. A series of low annular armor ridges, no club or spikes.
TAIL=[(.62,.345,.065,.061),(.69,.335,.062,.056),(.77,.305,.048,.046),(.87,.265,.035,.034),(.98,.230,.022,.024),(1.08,.212,.010,.014),(1.14,.210,.003,.005)]
loft('Tapering_tail',[(y,0,z,w,h) for y,z,w,h in TAIL],mat='armor',n=12)
def tail_shape(y):
    for a,b in zip(TAIL,TAIL[1:]):
        if a[0]<=y<=b[0]:
            t=(y-a[0])/(b[0]-a[0]);return [a[k]*(1-t)+b[k]*t for k in [1,2,3]]
    return TAIL[-1][1:]
rings=[]
for i,y in enumerate([.70,.76,.82,.88,.94,1.00,1.06,1.11]):
    z,w,h=tail_shape(y)
    rings.append(loft('Tail_ring_%02d'%i,[(y-.008,0,z,w+.003,h+.003),(y,0,z,w+.007,h+.007),(y+.011,0,z,w+.002,h+.002)],mat='ridges',n=12))
join('Grouped_tail_armor_ridges',rings)
# Cephalic shield follows the long wedge, not a generic spherical helmet.
vs=[];fs=[]
for i,(y,w,z) in enumerate([(-1.013,.029,.422),(-.94,.046,.480),(-.86,.062,.531),(-.78,.078,.579),(-.715,.063,.568)]):
    for x in [-1,-.5,0,.5,1]:vs.append((x*w,y,z-.045*abs(x)))
for i in range(4):
    for j in range(4):b=i*5+j;fs.append((b,b+1,b+6,b+5))
# Solidify head shield to keep closed, portable geometry.
ob=mesh_object('Cephalic_shield',vs,fs,M['armor'],COL);bpy.context.view_layer.objects.active=ob
s=ob.modifiers.new('Head_shield_thickness','SOLIDIFY');s.thickness=.008;bpy.ops.object.modifier_apply(modifier=s.name)
for s,side in [(-1,'L'),(1,'R')]:
    ell('Eye_'+side,(s*.077,-.805,.510),(.012,.012,.011),'eye')
    ell('Small_ear_'+side,(s*.087,-.706,.566),(.023,.018,.034),'skin')
    ell('Nostril_'+side,(s*.023,-1.053,.376),(.008,.006,.005),'eye',10,5)
    # Conservative functional claw silhouette, not a claim of exact fossil toe count.
    for limb,y in [('Fore',-.43),('Hind',.435)]:
        claws=[]
        for k,dx in enumerate([-.044,0,.044]):
            x=s*.263+dx;front=y-.145-(.012 if k==1 else 0)
            claws.append(loft(limb+'_claw_'+side+str(k),[(front,x,.012,.003,.005),(front+.030,x,.021,.013,.013),(front+.067,x,.030,.017,.018)],mat='claws',n=8))
        join(limb+'_claws_'+side,claws)
# A restrained closed lip crease avoids the museum mount's open restored jaw.
loft('Closed_lip_line',[(y,0,z,w,.0025) for y,z,w in [(-1.052,.351,.025),(-.98,.372,.041),(-.91,.398,.052)]],mat='eye',n=12)
for ob in COL.all_objects:
    if ob.type!='MESH':continue
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    for f in ob.data.polygons:f.use_smooth=False
bpy.context.view_layer.update();source=audit_source(COL,16000)
if source['errors']:raise RuntimeError(source['errors'])
scene=bpy.context.scene;scene['source_generator']='source/generate.py';scene['scale_status']='Original full-body estimate, not same-specimen measured reconstruction'
scene.render.threads_mode='FIXED';scene.render.threads=2;bpy.context.preferences.filepaths.save_version=0
# Retain portable UI and render defaults in the editable source.
scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b' '*1023
                space.params.directory=b'//'
                space.params.filename='model.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in COL.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=ROOT
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
avail={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-avail:raise RuntimeError('Unsupported exporter option')
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(OUT/'model.glb',16000,6,48)
if glb['errors']:raise RuntimeError(glb['errors'])
glb['file']='model.glb'
if glb['bytes']>2200000:raise RuntimeError('Byte budget')
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ['min','max'] for i in range(3))
if delta>1e-4 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source export disagreement')
rec={'asset_id':'holmesina','revision':'r001','blender':bpy.app.version_string,'seed':P['seed'],'glb_sha256':glb['sha256'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'source_forms_excluded':len(SC.objects),'threads':2,'notes':['Closed meshes; separate armor pieces overlap intentionally as layered osteoderms.','Three mobile central bands. Polygonal scutes are grouped geometry.','UF890 skull, species size estimate, comparative cryptae skeleton and original reconstruction dimensions remain distinct.']}
(OUT/'build-report.json').write_text(json.dumps(rec,indent=2)+'\n');print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
