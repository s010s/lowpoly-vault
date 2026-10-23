# SPDX-License-Identifier: MIT
"""Original Scelidosaurus harrisonii reconstruction. No external image dependency.
blender -b -t 2 --python source/generate.py -- --out ROOT --mode build
Modes gray/final render a clean reimport of OUT/model.glb, never source geometry.
"""
import argparse,hashlib,json,math,shutil,sys
from pathlib import Path
S=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'deps'))
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from asset_common import setup_scene,make_material,mesh_object,export_asset,render_previews
P=json.loads((S/'params.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mode',choices=['build','gray','final'],default='build')
A=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);OUT=Path(A.out).resolve();OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
class Part:
    def __init__(self,name,mats):self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[];self.groups=[]
    def add(self,v,f,mi=0,label=''):
        n=len(self.v);self.v.extend(v);self.f.extend(tuple(n+i for i in face) for face in f);self.mi.extend([mi]*len(f));self.groups.append((label,list(range(n,len(self.v)))))
    def object(self,col):
        o=mesh_object(self.name,self.v,self.f,self.mats,col)
        for poly,m in zip(o.data.polygons,self.mi):poly.material_index=m
        for label,ids in self.groups:
            if label:o.vertex_groups.new(name=label).add(ids,1,'REPLACE')
        return o

def loft(part,rows,n=16,mi=0,label=''):
    # Deliberate cross sections along Y: centerX, Y, centerZ, lateralRadius, verticalRadius.
    v=[];f=[]
    for x,y,z,rx,rz in rows:
        v.extend((x+rx*math.cos(j*math.tau/n),y,z+rz*math.sin(j*math.tau/n)) for j in range(n))
    for k in range(len(rows)-1):
        f.extend((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j) for j in range(n))
    f.extend([tuple(range(n-1,-1,-1)),tuple((len(rows)-1)*n+j for j in range(n))]);part.add(v,f,mi,label)

def tube(part,points,radii,n=10,mi=0,label=''):
    ps=[Vector(p) for p in points];v=[];f=[]
    for i,p in enumerate(ps):
        t=(ps[min(i+1,len(ps)-1)]-ps[max(i-1,0)]).normalized();u=t.cross(Vector((0,1,0)))
        if u.length<.05:u=t.cross(Vector((1,0,0)))
        u.normalize();w=t.cross(u).normalized()
        v.extend(tuple(p+u*math.cos(j*math.tau/n)*radii[i][0]+w*math.sin(j*math.tau/n)*radii[i][1]) for j in range(n))
    for k in range(len(ps)-1):f.extend((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j) for j in range(n))
    f.extend([tuple(range(n-1,-1,-1)),tuple((len(ps)-1)*n+j for j in range(n))]);part.add(v,f,mi,label)

def ell(part,c,r,n=10,rings=5,mi=0,label=''):
    x,y,z=c;rx,ry,rz=r;v=[(x,y,z+rz)];f=[]
    for k in range(1,rings):
        p=k*math.pi/rings;v.extend((x+rx*math.sin(p)*math.cos(j*math.tau/n),y+ry*math.sin(p)*math.sin(j*math.tau/n),z+rz*math.cos(p)) for j in range(n))
    v.append((x,y,z-rz));b=len(v)-1
    for j in range(n):f.append((0,1+j,1+(j+1)%n))
    for k in range(rings-2):f.extend((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n) for j in range(n))
    for j in range(n):f.append((b,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
    part.add(v,f,mi,label)

def scute(part,c,width,length,height,normal,mi=0,label=''):
    # Closed six-sided base and longitudinal roof ridge, not an upright stegosaur plate.
    n=Vector(normal).normalized();long=Vector((0,1,0));long=(long-n*long.dot(n)).normalized();across=long.cross(n).normalized();c=Vector(c)
    outline=[(-.5,-.27),(-.32,-.5),(.32,-.5),(.5,-.27),(.5,.28),(.28,.5),(-.28,.5),(-.5,.28)]
    v=[tuple(c+across*u*width+long*w*length-n*.012) for u,w in outline]
    v.extend(tuple(c+across*u*width*.87+long*w*length*.90+n*.006) for u,w in outline)
    v += [tuple(c+long*(-length*.27)+n*height),tuple(c+long*(length*.23)+n*height*.88)]
    f=[tuple(range(7,-1,-1))]+[(j,(j+1)%8,8+(j+1)%8,8+j) for j in range(8)]
    f += [(8,9,16),(9,10,16),(10,11,16),(11,12,17,16),(12,13,17),(13,14,17),(14,15,17),(15,8,16,17)]
    part.add(v,f,mi,label)

def build():
    col=setup_scene('scelidosaurus',P['seed']);m={k:make_material(k,c,.88) for k,c in P['palette_srgb'].items()}
    body=Part('Axial_body_neck_tapered_tail',[m['Skin'],m['Belly']]);limbs=Part('Four_weight_bearing_limbs',[m['Skin'],m['Belly']]);head=Part('Wedge_skull_and_lower_jaw',[m['Skin'],m['Belly']]);armour=Part('Longitudinal_low_keeled_osteoderms',[m['Armour'],m['Armour_keel']]);small=Part('Intervening_small_ossicles',[m['Armour'],m['Skin']]);trim=Part('Beak_toes_and_skull_knobs',[m['Beak_claws'],m['Armour']]);orb=Part('Orbital_rims',[m['Orbital_rim']]);dark=Part('Eyes_nostrils_mouth_seam',[m['Eye']])
    # Neck, deep ribcage and hips form one continuous mesh. Tail is similarly a continuous loft.
    axial=[(0,-1.24,.86,.105,.12),(0,-1.12,.86,.13,.145),(0,-.98,.83,.17,.18),(0,-.81,.80,.225,.245),(0,-.62,.78,.295,.30),(0,-.38,.76,.355,.33),(0,-.10,.755,.375,.345),(0,.17,.77,.365,.36),(0,.41,.81,.32,.345),(0,.62,.84,.255,.29),(0,.80,.84,.195,.205),(.015,.99,.81,.155,.165),(.035,1.22,.765,.125,.13),(.06,1.47,.70,.095,.10),(.08,1.70,.62,.067,.076),(.09,1.93,.54,.044,.052),(.08,2.14,.48,.021,.028),(.065,2.35,.45,.003,.004)]
    loft(body,axial,n=16,label='Continuous_axial_outline')
    # Material bands follow ventral half of the original topology; no duplicated belly shell.
    for i in range(len(body.f)-2):
        j=i%16
        if 9<=j<=14:body.mi[i]=1
    # Skull widens behind the narrow, herbivorous rostrum. A short rear-skull knob pair is specimen based.
    loft(head,[(0,-1.65,.87,.038,.048),(0,-1.60,.90,.065,.064),(0,-1.50,.94,.087,.08),(0,-1.39,.96,.125,.105),(0,-1.27,.95,.145,.105),(0,-1.17,.92,.108,.09)],12,label='Small_wedge_skull')
    loft(head,[(0,-1.642,.831,.032,.016),(0,-1.55,.83,.070,.028),(0,-1.42,.831,.102,.040),(0,-1.28,.843,.116,.044),(0,-1.18,.863,.083,.034)],12,mi=1,label='Closed_lower_jaw')
    loft(trim,[(0,-1.655,.868,.038,.045),(0,-1.617,.884,.051,.053)],10,label='Modest_edentulous_beak_cap')
    for s in (-1,1):
        ell(orb,(s*.115,-1.378,1.001),(.018,.049,.030),10,4,label='Raised_orbital_brow_'+str(s))
        ell(dark,(s*.131,-1.387,1.000),(.010,.022,.019),10,5,label='Lateral_eye_'+str(s))
        ell(dark,(s*.063,-1.576,.924),(.005,.010,.006),8,4,label='Small_nostril_'+str(s))
        tube(dark,[(s*.035,-1.652,.843),(s*.067,-1.57,.845),(s*.094,-1.47,.850),(s*.12,-1.36,.866),(s*.126,-1.265,.882)],[(.0025,.0025)]*5,6,label='Fine_closed_mouth_seam_'+str(s))
        tube(trim,[(s*.113,-1.223,1.00),(s*.152,-1.18,1.026),(s*.17,-1.145,1.037)],[(.034,.030),(.021,.020),(.002,.003)],8,mi=1,label='Modest_posterior_skull_knob_'+str(s))
    # Forelimbs shorter/slimmer than the weighty hindlimbs. All four feet exactly at Z=0.
    for s in (-1,1):
        for fore in (True,False):
            off=.035 if s==1 else -.035
            if fore:
                pts=[(s*.225,-.63,.80),(s*.30,-.64,.65),(s*.345,-.53,.43),(s*.335,-.64,.21),(s*.335,-.70+off,.095)];r=[(.145,.15),(.125,.12),(.08,.085),(.055,.061),(.057,.063)]
                fy=-.735+off;fx=s*.335;fw=.10;fl=.14
            else:
                pts=[(s*.20,.43,.87),(s*.32,.39,.66),(s*.365,.27,.44),(s*.37,.55,.235),(s*.37,.57+off,.105)];r=[(.20,.21),(.185,.19),(.12,.13),(.07,.07),(.068,.075)]
                fy=.53+off;fx=s*.37;fw=.125;fl=.17
            label=('Fore' if fore else 'Hind')+('_left' if s<0 else '_right')
            tube(limbs,pts,r,12,label=label+'_continuous_jointed_limb')
            # Closed foot loft with flat ground contacts and gently domed upper shape.
            n=12;v=[];f=[]
            for z,fac in [(0,.88),(.045,1),(.105,.70),(.13,.38)]:
                v.extend((fx+fw*fac*math.cos(j*math.tau/n),fy+fl*fac*math.sin(j*math.tau/n),z) for j in range(n))
            f=[tuple(range(n-1,-1,-1)),tuple(3*n+j for j in range(n))]
            for k in range(3):f.extend((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j) for j in range(n))
            limbs.add(v,f,label=label+'_planted_foot')
            for digit in range(3):
                x=fx+(digit-1)*fw*.55
                tube(trim,[(x,fy-fl*.65,.047),(x,fy-fl*1.0,.036),(x,fy-fl*1.14,.022)],[(.023,.020),(.018,.014),(.003,.003)],8,label=label+'_ungual_'+str(digit+1))
    # Project each organized row to the actual faceted surface. Small overlaps sink scute bases, never float.
    surface=BVHTree.FromPolygons([Vector(v) for v in body.v],body.f,all_triangles=False)
    def section(y):
        for a,b in zip(axial,axial[1:]):
            if a[1]<=y<=b[1]:
                t=(y-a[1])/(b[1]-a[1]);return tuple(a[k]+t*(b[k]-a[k]) for k in range(5))
        raise ValueError(y)
    counts={}
    for sign in (-1,1):
        for row,angle in [('paramedian',65),('dorsolateral',32),('flank',2)]:
            ys=[-1.04+i*.155 for i in range(20)]
            count=0
            for j,y in enumerate(ys):
                cx,_,cz,rx,rz=section(y);a=math.radians(angle);vec=Vector((sign*math.cos(a),0,math.sin(a)))
                h,n,_,_=surface.ray_cast(Vector((cx,y,cz))+vec*1.5,-vec)
                if h is None:raise ValueError('Scute ray missed axial mesh')
                size=min(1,rx/.27)*(.96+.06*math.sin(j*1.7+angle));w=.11*size;ln=.143*min(1,(rx/.18)**.5);height=(.055 if row=='paramedian' else .04)*size
                scute(armour,h,w,ln,height,n,mi=1 if (j%5==2 and row!='flank') else 0,label=f'{row}_{sign}_{j:02d}');count+=1
            counts[row+'_'+str(sign)]=count
        # Small ossicles occupy gaps without forming a continuous armadillo shell.
        for j in range(17):
            y=-.94+j*.137
            cx,_,cz,rx,rz=section(y)
            for angle in (46,18):
                a=math.radians(angle);d=Vector((sign*math.cos(a),0,math.sin(a)));h,n,_,_=surface.ray_cast(Vector((cx,y,cz))+d*1.5,-d)
                fac=min(1,rx/.25)
                scute(small,h,.042*fac,.048*fac,.012*fac,n,mi=j%2,label=f'ossicle_{sign}_{j}_{angle}')
    # Two understated roof scutes on rear skull, not high cranial horns.
    for s in (-1,1):scute(small,(s*.065,-1.29,1.035),.07,.11,.026,(0,0,1),label='Cranial_low_scale_'+str(s))
    parts=[body,limbs,head,armour,small,trim,orb,dark]
    for part in parts:
        part.v=[(x,y+.1025,z) for x,y,z in part.v]
        part.object(col)
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    tmp=OUT/'private/canonical-export'
    record=export_asset('scelidosaurus',{'en':'Scelidosaurus','zh':'腿龙'},'dinosaurs',col,metadata={'generator':'source/generate.py','description':{'en':'Original four-metre approximate Scelidosaurus reconstruction with elongate quadrupedal body, low osteoderm rows, modest posterior skull knobs and a long tapering unclubbed tail.','zh':'约四米体长的腿龙原创复原：四足、低脊甲纵列、后颅小角与无锤长尾。'},'reconstruction_notes':'Cast-based morphology, not fossil scan; no sex inference; colour, flesh, precise scute count and stance are artistic.','profile':'palette-only static low-poly'},output_root=tmp,render=False,diagnostics=False,**{k:P['geometry_policy'][k] for k in ('max_triangles','max_materials','max_primitives')})
    cdir=tmp/'scelidosaurus';shutil.copy2(cdir/'scelidosaurus.glb',OUT/'model.glb');shutil.copy2(cdir/'scelidosaurus.blend',OUT/'model.blend')
    if (OUT/'model.glb').stat().st_size>P['geometry_policy']['max_glb_bytes']:raise ValueError('GLB exceeds frozen byte budget')
    technical=json.loads((cdir/'qa.json').read_text());technical['glb_sha256']=sha(OUT/'model.glb');technical['glb']['file']='model.glb';write(OUT/'qa/evidence/technical.json',technical)
    record.update(glb='model.glb',blend='model.blend',preview='preview.png',origin='Identity root at mean center of four grounded foot soles, Y shift +0.1025 m baked in vertices');write(OUT/'qa/evidence/build-metadata.json',record)
    write(OUT/'qa/evidence/anatomy-and-scale.json',{'glb_sha256':sha(OUT/'model.glb'),'nominal_length_m':4.0,'posed_length_m':record['blender_dimensions_m'][1],'low_armour_rows':counts,'small_ossicles':70,'feet_contact_z':0,'head_forward':'-Y','tail':'continuous taper, no terminal club or thagomizer','conservative_interpretation':'Three small visible unguals per foot are stylized surface indications, not a claim of complete exact digit count.','topology':'Eight semantic mesh objects with named editable vertex groups; intentional intersecting closed anatomical solids at limb/skull connections and rooted osteoderms.'})
    print('BUILD_COMPLETE',record['triangles'],record['glb_bytes'],sha(OUT/'model.glb'))

def render():
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    col=bpy.data.collections.new('ACTUAL_GLB_IMPORTED');bpy.context.scene.collection.children.link(col)
    for o in list(bpy.context.scene.objects):
        for c in list(o.users_collection):c.objects.unlink(o)
        col.objects.link(o)
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    gray=A.mode=='gray';folder=OUT/('private/gray' if gray else 'private/final-render')
    if gray:
        clay=make_material('Gray_self_check','#929292')
        for o in col.objects:
            if o.type=='MESH':
                o.data.materials.clear();o.data.materials.append(clay)
                for p in o.data.polygons:p.material_index=0
    resolution=384 if gray else P['render']['resolution'];samples=6 if gray else P['render']['samples']
    files=render_previews(col,folder,views=('front','side','top','hero'),resolution=resolution,samples=samples)
    if not gray:
        for view in ('front','side','top'):shutil.copy2(folder/f'preview-{view}.png',OUT/f'views/{view}.png')
        shutil.copy2(folder/'preview-hero.png',OUT/'views/perspective.png');shutil.copy2(folder/'preview-hero.png',OUT/'preview.png')
    viewmap={'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]}
    evidence={'glb_sha256':sha(OUT/'model.glb'),'source':'clean imported exact delivered GLB','stage':'gray self check' if gray else 'final exact-export','engine':'Cycles CPU','threads':2,'resolution':[resolution,resolution],'samples':samples,'background_srgb':'#E8E4DC','colour_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'camera':'orthographic; full geometry bounds fit with 25 percent margin using canonical helper','directions':viewmap,'views':{k:{'path':str(Path(f).relative_to(OUT)) if gray else 'views/'+k+'.png','sha256':sha(Path(f))} for k,f in zip(viewmap,files)}}
    write(OUT/('private/gray/evidence.json' if gray else 'qa/evidence/actual-glb-views.json'),evidence)
    print('RENDER_COMPLETE',A.mode)
if A.mode=='build':build()
else:render()
