#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic Eurhinosaurus sp. R5465-inspired living reconstruction.
blender -b -t 2 --python source/generate.py -- --output /absolute/output --stage build
Other stages: gray (source diagnostics), render (clean exact GLB import).
Uses only source/params.json and the declared vendored helpers at run time.
"""
from pathlib import Path
import sys, json, math, shutil, hashlib, argparse
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
a=argparse.ArgumentParser();a.add_argument('--output',required=True);a.add_argument('--stage',choices=['build','gray','render'],default='build');args=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(args.output).resolve();OUT.mkdir(parents=True,exist_ok=True)
def js(path,x): path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(x,indent=2)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def mesh(name,v,f,mats,smooth=False):
    o=ac.mesh_object(name,v,f,mats,C)
    if smooth:
        for poly in o.data.polygons: poly.use_smooth=True
    return o

def loft(name,rows,mats,n=24,colors=False):
    # Closed elliptical section loft: x, y_center, z_center, width_radius, depth_radius.
    v=[];f=[]
    for x,y,z,ry,rz in rows:
        for j in range(n):
            t=2*math.pi*j/n;v.append((x,y+ry*math.cos(t),z+rz*math.sin(t)))
    for i in range(len(rows)-1):
        for j in range(n): f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.extend([tuple(range(n-1,-1,-1)),tuple((len(rows)-1)*n+j for j in range(n))])
    o=mesh(name,v,f,mats,True)
    if colors:
        for p in o.data.polygons:
            j=p.index%n;h=math.sin(2*math.pi*(j+.5)/n)
            p.material_index=0 if h>.30 else 2 if h<-.42 else 1
    return o

def paddle(name,sgn,rows):
    # Spanwise swept oval sections, closed tip. Width here is fore-aft half chord.
    n=12;v=[];f=[]
    for x,y,z,c,t in rows:
        for j in range(n):
            ang=2*math.pi*j/n;v.append((x+c*math.cos(ang),sgn*y,z+t*math.sin(ang)))
    for i in range(len(rows)-1):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.extend([tuple(range(n-1,-1,-1)),tuple((len(rows)-1)*n+j for j in range(n))])
    return mesh(name,v,f,SKIN[0],True)

def vertical_fin(name,outline,center,halfdepth):
    # Organic low-profile closed membrane volume. An inset ring provides a rounded edge.
    cx,cz=center;N=len(outline);v=[];f=[]
    for scale,ysign in [(1,0),(.82,-1),(.82,1)]:
        for x,z in outline:v.append((cx+(x-cx)*scale,ysign*halfdepth,cz+(z-cz)*scale))
    v.extend([(cx,-halfdepth*1.14,cz),(cx,halfdepth*1.14,cz)])
    for i in range(N):
        j=(i+1)%N
        f.extend([(i,j,N+j,N+i),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N),(2*N+j,2*N+i,3*N+1)])
    return mesh(name,v,f,SKIN[0],True)

# Collect many small bilateral features into one editable semantic mesh each.
def ellipsoid(buf,center,radius,nu=16,nv=8):
    v,f=buf;k=len(v);cx,cy,cz=center;rx,ry,rz=radius
    v.append((cx,cy,cz-rz))
    for j in range(1,nv):
        t=-math.pi/2+math.pi*j/nv
        for i in range(nu):
            p=2*math.pi*i/nu;v.append((cx+rx*math.cos(t)*math.cos(p),cy+ry*math.cos(t)*math.sin(p),cz+rz*math.sin(t)))
    top=len(v);v.append((cx,cy,cz+rz))
    for i in range(nu):f.append((k,k+1+(i+1)%nu,k+1+i))
    for j in range(nv-2):
        for i in range(nu):
            aa=k+1+j*nu+i;bb=k+1+j*nu+(i+1)%nu;f.append((aa,bb,bb+nu,aa+nu))
    last=k+1+(nv-2)*nu
    for i in range(nu):f.append((last+i,last+(i+1)%nu,top))

def tube(buf,points,radius=0.003,n=6):
    v,f=buf;k=len(v)
    for idx,pt in enumerate(points):
        tangent=Vector(points[min(idx+1,len(points)-1)])-Vector(points[max(idx-1,0)])
        tangent.normalize();u=tangent.cross(Vector((0,0,1))).normalized();w=tangent.cross(u).normalized()
        for j in range(n):v.append(tuple(Vector(pt)+radius*(math.cos(j*2*math.pi/n)*u+math.sin(j*2*math.pi/n)*w)))
    for i in range(len(points)-1):
        for j in range(n):f.append((k+i*n+j,k+i*n+(j+1)%n,k+(i+1)*n+(j+1)%n,k+(i+1)*n+j))
    f.extend([tuple(k+j for j in range(n-1,-1,-1)),tuple(k+(len(points)-1)*n+j for j in range(n))])

if args.stage in ['build','gray']:
    C=ac.setup_scene('eurhinosaurus',P['seed']);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    root=bpy.data.objects['eurhinosaurus'];root['authoring_forward']='+X';root['selected_specimen']='NHMUK PV R5465';root['taxon']='Eurhinosaurus sp.';root['reconstruction']='Soft contours inferred; species assignment unresolved.'
    SKIN=[ac.make_material('Dorsal blue grey','#4B6269',.70),ac.make_material('Flank grey','#829493',.77),ac.make_material('Ventral warm grey','#BBC1B7',.82)]
    EYE=ac.make_material('Eyes graphite','#16282B',.24)
    LINE=ac.make_material('Mouth and nares','#34484B',.80)
    TOOTH=ac.make_material('Subdued ivory teeth','#B9B4A0',.84)
    rows=[(-2.17,0,.055,.009,.015),(-2.10,0,.18,.014,.020),(-2.02,0,.32,.020,.027),(-1.91,0,.48,.024,.029),(-1.80,0,.52,.034,.045),(-1.64,0,.55,.047,.066),(-1.44,0,.57,.066,.092),(-1.22,0,.585,.092,.131),(-1.03,0,.59,.123,.170),(-.82,0,.59,.155,.215),(-.55,0,.59,.182,.250),(-.25,0,.59,.190,.260),(.02,0,.59,.174,.243),(.24,0,.60,.146,.205),(.40,0,.62,.128,.173),(.53,0,.63,.122,.155),(.65,0,.64,.104,.127),(.77,0,.647,.073,.092),(.91,0,.65,.041,.058),(1.08,0,.653,.027,.035),(1.26,0,.656,.020,.024),(1.44,0,.660,.014,.018),(1.59,0,.664,.0085,.011),(1.65,0,.665,.0035,.005)]
    body=loft('Continuous trunk skull and upper rostrum',rows,SKIN,24,True)
    jaw=loft('Short connected mandible',[(.25,0,.493,.105,.040),(.35,0,.485,.105,.047),(.45,0,.483,.102,.057),(.55,0,.48,.099,.055),(.66,0,.495,.084,.049),(.79,0,.532,.059,.039),(.93,0,.574,.036,.028),(1.05,0,.604,.022,.019),(1.13,0,.622,.009,.009)],SKIN,20,True)
    for s,side in [(-1,'near'),(1,'far')]:
        paddle('Forepaddle '+side,s,[(.24,.098,.470,.120,.038),(.20,.205,.452,.121,.032),(.14,.34,.422,.111,.027),(.08,.49,.385,.091,.023),(.025,.63,.35,.064,.018),(-.005,.74,.325,.030,.010),(-.008,.77,.320,.008,.004)])
        paddle('Hindpaddle '+side,s,[(-1.035,.070,.510,.082,.027),(-1.07,.14,.48,.083,.025),(-1.12,.25,.437,.075,.021),(-1.18,.36,.392,.054,.016),(-1.23,.46,.354,.028,.010),(-1.245,.49,.345,.007,.004)])
    vertical_fin('Modest inferred dorsal fin',[(-.96,.79),(-.87,.93),(-.76,1.075),(-.71,1.09),(-.70,1.045),(-.66,.97),(-.59,.91),(-.44,.855),(-.29,.825)],(-.72,.882),.027)
    vertical_fin('Vertical caudal membrane with lower lobe support',[(-1.74,.50),(-1.81,.68),(-1.92,.83),(-2.075,.940),(-2.105,.925),(-2.075,.78),(-2.025,.65),(-2.035,.49),(-2.11,.28),(-2.20,.025),(-2.185,0),(-2.02,.16),(-1.88,.32)],(-1.945,.51),.026)
    eyes=([],[]);details=([],[]);teeth=([],[])
    for s in [-1,1]:
        ellipsoid(eyes,(.62,s*.106,.674),(.060,.022,.061),20,10)
        ellipsoid(details,(.835,s*.053,.697),(.022,.006,.010),12,6)
        tube(details,[(.48,s*.101,.495),(.60,s*.092,.515),(.73,s*.073,.551),(.86,s*.048,.585),(1.00,s*.029,.619),(1.10,s*.018,.631)],.0029,6)
        # Discreet small conical teeth remain attached to the underside of the upper jaw.
        for i in range(19):
            x=.96+i*.033;z=.65+(x-.91)*.024;ry=max(.006,.036-(x-.96)*.055);rz=max(.010,.047-(x-.96)*.060)
            v,f=teeth;k=len(v);r=.0025;h=.007
            for j in range(6):v.append((x+r*math.cos(j*math.pi/3),s*ry+r*math.sin(j*math.pi/3),z-rz+.002))
            v.append((x+.001,s*ry,z-rz-h))
            f.append(tuple(k+j for j in range(5,-1,-1)))
            for j in range(6):f.append((k+j,k+(j+1)%6,k+6))
    mesh('Bilateral external eyes',*eyes,EYE,True);mesh('Mouth seams and lateral nares',*details,LINE,True);mesh('Fine upper jaw dentition',*teeth,TOOTH,False)
    if args.stage=='gray':
        gray=ac.make_material('Temporary clay','#939393',.85)
        for o in C.objects:
            if o.type=='MESH':
                o.data.materials.clear();o.data.materials.append(gray)
                for p in o.data.polygons:p.material_index=0
        ac.render_previews(C,OUT/'private/gray',views=('front','side','top','hero'),resolution=640,samples=12,transparent=True)
        js(OUT/'private/gray/evidence.json',{'stage':'pre-final source gray diagnostic','generator_sha256':sha(HERE/'generate.py'),'views':['front','side','top','hero'],'resolution':640,'samples':12,'actual_export_final_evidence':False})
    else:
        # Public filenames are declared here from the beginning, not changed during packaging.
        work=OUT/'private/export-work';meta=ac.export_asset('eurhinosaurus',{'en':'Eurhinosaurus','zh':'Eurhinosaurus（海生爬行类）'},'animals',C,metadata={'description':{'en':'R5465-inspired genus-level reconstruction with elongated upper jaw and short mandible.','zh':'以 R5465 为骨架参考的属级复原，突出长上颌和短下颌。'},'generator':'source/generate.py'},output_root=work,render=False,max_triangles=24000,max_materials=6,max_primitives=16)
        generated=work/'eurhinosaurus';shutil.copyfile(generated/'eurhinosaurus.glb',OUT/'model.glb');shutil.copyfile(generated/'eurhinosaurus.blend',OUT/'model.blend')
        qa=json.loads((generated/'qa.json').read_text());js(OUT/'qa/evidence/source-export.json',qa)
        meta.update({'id':'eurhinosaurus','revision':'r001','glb':'model.glb','blend':'model.blend','preview':'preview.png','axes':{'blender_up':'+Z','blender_forward':'+X','glb_up':'+Y','glb_forward':'+X'},'origin':'Swimming mount at X=0,Y=0,Z=0; lowest caudal tip at Z=0','reference_specimen':'NHMUK PV R5465','taxon':'Eurhinosaurus sp.','source_inputs':['source/generate.py','source/params.json','source/deps/asset_common.py','source/deps/qa_glb.py']})
        js(OUT/'qa/evidence/build-metadata.json',meta)
        js(OUT/'qa/evidence/anatomy-measurements.json',{'glb_sha256':sha(OUT/'model.glb'),'total_length_m':3.85,'skull_posterior_landmark_x_m':.55,'upper_rostrum_tip_x_m':1.65,'lower_jaw_tip_x_m':1.13,'skull_length_inferred_m':1.10,'mandible_length_inferred_m':.58,'mandible_skull_ratio':.58/1.10,'body_width_inferred_m':.38,'body_depth_inferred_m':.52,'paired_paddles':4,'caudal_plane':'XZ, vertical','geometry_policy':{'max_triangles':24000,'max_materials':6,'max_primitives':16,'max_glb_bytes':2500000},'measurement_status':'Only total length is specimen-published; other values are authored geometry or conservative inference; humerus 0.097m is skeletal reference, not a modeled skin landmark.'})
        assert (OUT/'model.glb').stat().st_size<2500000
else:
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    C=bpy.data.collections.new('EXACT_GLB');bpy.context.scene.collection.children.link(C)
    for obj in list(bpy.context.scene.objects):
        for old in list(obj.users_collection):old.objects.unlink(obj)
        C.objects.link(obj)
    files=ac.render_previews(C,OUT/'private/final-render',views=('front','side','top','hero'),resolution=1024,samples=48,transparent=True)
    (OUT/'views').mkdir(exist_ok=True)
    for label in ['front','side','top']:shutil.copyfile(OUT/f'private/final-render/preview-{label}.png',OUT/f'views/{label}.png')
    shutil.copyfile(OUT/'private/final-render/preview-hero.png',OUT/'preview.png');shutil.copyfile(OUT/'preview.png',OUT/'views/perspective.png')
    js(OUT/'qa/evidence/exact-glb-views.json',{'status':'rendered_pending_independent_review','glb_sha256':sha(OUT/'model.glb'),'source':'Clean factory scene import of model.glb; no source scene rendering','engine':'Cycles CPU','threads':2,'resolution':[1024,1024],'samples':48,'denoising':False,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'transparent':True,'camera_directions_blender':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},'files':{p:sha(OUT/p) for p in ['preview.png','views/front.png','views/side.png','views/top.png','views/perspective.png']},'perspective_reuses_preview':True,'artifact_scope':'Actual exported GLB, not an ImageGen or source-only image.'})
print('EURHINOSAURUS_STAGE_COMPLETE',args.stage)
