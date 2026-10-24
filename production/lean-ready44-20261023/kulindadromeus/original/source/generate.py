#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original deterministic Kulindadromeus reconstruction, not a specimen scan.
Run with Blender: --background --threads 2 --python source/generate.py -- --out OUTPUT [--clay]
The adjacent params.json and pinned deps/ are the complete project dependency closure.
"""
from pathlib import Path
import argparse, hashlib, json, math, random, shutil, sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, mesh_object, make_material, export_asset, render_previews
P=json.loads(Path(__file__).with_name('params.json').read_text())
B={};COL=None;M={};SEMS=[]

def append(group,name,vs,fs,mats):
    b=B.setdefault(group,{'v':[],'f':[],'m':[],'semantic':[]});o=len(b['v'])
    b['v']+=list(map(tuple,vs));b['f'] += [tuple(o+i for i in f) for f in fs]
    b['m'] += [mats]*len(fs) if isinstance(mats,str) else mats
    b['semantic'].append((name,o,len(vs)))

def loft(group,name,sections,mat='cover',n=12,regions=False):
    v=[];f=[];mi=[]
    for y,z,rx,rz in sections:
        v += [(rx*math.cos(2*math.pi*j/n),y,z+rz*math.sin(2*math.pi*j/n)) for j in range(n)]
    f.append(tuple(reversed(range(n))));mi.append(mat)
    for i in range(len(sections)-1):
        for j in range(n):
            f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
            a=math.sin(2*math.pi*(j+.5)/n);mi.append('dorsal' if regions and a>.45 else 'belly' if regions and a<-.4 else mat)
    f.append(tuple((len(sections)-1)*n+j for j in range(n)));mi.append(mat)
    append(group,name,v,f,mi)

def tube(group,name,points,radii,mat='cover',n=8,aspect=1):
    ps=list(map(Vector,points));v=[];f=[]
    for i,p in enumerate(ps):
        t=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized();ref=Vector((1,0,0)) if abs(t.x)<.85 else Vector((0,1,0))
        u=(ref-t*ref.dot(t)).normalized();w=t.cross(u)
        for j in range(n):
            a=2*math.pi*j/n;v.append(p+u*(radii[i]*math.cos(a))+w*(aspect*radii[i]*math.sin(a)))
    f.append(tuple(reversed(range(n))))
    for i in range(len(ps)-1):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.append(tuple((len(ps)-1)*n+j for j in range(n)))
    append(group,name,v,f,mat)

def oval(group,name,c,r,mat,n=10,rings=4):
    v=[(c[0],c[1],c[2]+r[2])];f=[]
    for k in range(1,rings):
        a=math.pi*k/rings
        v += [(c[0]+r[0]*math.sin(a)*math.cos(2*math.pi*j/n),c[1]+r[1]*math.sin(a)*math.sin(2*math.pi*j/n),c[2]+r[2]*math.cos(a)) for j in range(n)]
    e=len(v);v.append((c[0],c[1],c[2]-r[2]))
    for j in range(n):f.append((0,1+j,1+(j+1)%n))
    for k in range(rings-2):
        for j in range(n):a=1+k*n+j;b=1+k*n+(j+1)%n;f.append((a,b,b+n,a+n))
    for j in range(n):f.append((e,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
    append(group,name,v,f,mat)

def hair(base,normal,length,mat,name,bundle=3):
    n=Vector(normal).normalized();ref=Vector((0,1,0)) if abs(n.y)<.85 else Vector((1,0,0));u=n.cross(ref).normalized();w=n.cross(u)
    for j in range(bundle):
        drift=u*((j-(bundle-1)/2)*.24)+w*random.uniform(-.10,.10)+Vector((0,.28,0))
        direct=(n*.6+drift).normalized();p=Vector(base)+u*((j-(bundle-1)/2)*.0012)-n*.001
        radius=.00085 if length>.017 else .00062
        v=[p+u*(radius*math.cos(2*math.pi*k/3))+w*(radius*math.sin(2*math.pi*k/3)) for k in range(3)]
        v.append(p+direct*length*random.uniform(.86,1.10));append('Short_filament_cover',name+'_'+str(j),v,[(0,2,1),(0,1,3),(1,2,3),(2,0,3)],mat)

def interpolate(secs,y):
    for i in range(len(secs)-1):
        if secs[i][0]<=y<=secs[i+1][0]:
            t=(y-secs[i][0])/(secs[i+1][0]-secs[i][0]);return [secs[i][k]*(1-t)+secs[i+1][k]*t for k in range(1,4)]
    return secs[-1][1:]

def build():
    global COL,M
    COL=setup_scene(P['asset_id'],P['seed']);random.seed(P['seed']);M={k:make_material(k,v,roughness=.88 if k!='eye' else .45) for k,v in P['palette'].items()}
    trunk=[(-.200,.435,.039,.057),(-.158,.463,.063,.083),(-.084,.474,.083,.105),(.010,.479,.096,.119),(.098,.487,.094,.118),(.168,.484,.070,.086),(.215,.481,.043,.058)]
    loft('Core_profiles','Torso_profile',trunk,regions=True,n=14)
    neck=[(-.190,.470,.047,.055),(-.237,.480,.040,.045),(-.282,.514,.032,.038),(-.316,.550,.031,.041),(-.351,.573,.036,.040)]
    loft('Core_profiles','Short_curving_neck',neck,regions=True,n=12)
    skull=[(-.330,.590,.027,.036),(-.354,.607,.043,.051),(-.393,.610,.049,.052),(-.428,.601,.043,.043),(-.459,.585,.031,.029),(-.481,.577,.023,.021)]
    loft('Core_profiles','Short_deep_skull',skull,regions=True,n=12)
    loft('Core_profiles','Compact_lower_jaw',[(-.344,.565,.028,.017),(-.388,.555,.038,.020),(-.434,.555,.029,.016),(-.477,.561,.020,.010)],mat='belly',n=10)
    loft('Keratin_details','Small_upper_beak',[(-.474,.577,.023,.020),(-.495,.574,.020,.015),(-.509,.566,.010,.007)],mat='keratin',n=10)
    loft('Keratin_details','Small_lower_beak',[(-.473,.559,.019,.009),(-.497,.559,.013,.007),(-.506,.562,.008,.004)],mat='keratin',n=8)
    tail=[(.175,.486,.053,.064),(.245,.483,.047,.055),(.335,.479,.039,.044),(.450,.473,.030,.032),(.575,.470,.021,.023),(.710,.468,.014,.016),(.845,.468,.008,.010),(1.000,.470,.0013,.0018)]
    loft('Scaly_tail','Long_tapered_tail',tail,mat='tail',n=12)
    # Five longitudinal rows of very shallow epidermal scale plates over dorsal/lateral tail.
    # They are not osteoderms: no keels, spikes, knob armor, or deep plate margins.
    for row,a in enumerate([.08,.65,math.pi/2,math.pi-.65,math.pi-.08]):
        for k in range(28):
            y=.238+k*.025+(row%2)*.007
            if y>.94:continue
            z,rx,rz=interpolate(tail,y);length=.026 if y<.65 else .022
            halfangle=.23;vs=[]
            for yy,aa in [(y-length*.51,a-halfangle),(y-length*.51,a+halfangle),(y+length*.46,a+halfangle),(y+length*.60,a),(y+length*.46,a-halfangle)]:
                zz,rrx,rrz=interpolate(tail,yy);normal=Vector((math.cos(aa),0,math.sin(aa)))
                vs.append(Vector((rrx*math.cos(aa),yy,zz+rrz*math.sin(aa)))+normal*.0005)
            # Single-sided epidermal sheets sit 0.5 mm above the opaque tail.
            # Intentional open boundaries express thin scales, not solid osteoderms.
            fs=[(4,3,2,1,0)]
            append('Scaly_tail','Epidermal_row%d_%02d'%(row+1,k),vs,fs,'dorsal' if (k+row)%5==0 else 'tail')
    for s,label in [(1,'R'),(-1,'L')]:
        oval('Core_profiles',label+'_Cheek',(s*.034,-.391,.578),(.016,.032,.027),'cover',n=10,rings=4)
        oval('Dark_details',label+'_Eye',(s*.047,-.382,.625),(.005,.010,.010),'eye',n=12,rings=5)
        oval('Dark_details',label+'_Nostril',(s*.024,-.474,.587),(.0018,.0038,.0023),'eye',n=8,rings=4)
        tube('Dark_details',label+'_Closed_mouth_seam',[(s*.023,-.489,.561),(s*.032,-.439,.563),(s*.036,-.401,.566)],[.0012,.0011,.0008],mat='eye',n=5,aspect=.7)
        tube('Limbs',label+'_Muscular_thigh',[(s*.062,.120,.479),(s*.095,.058,.403),(s*.101,-.010,.310)],[.061,.055,.031],n=10,aspect=1.18)
        tube('Limbs',label+'_Long_shin',[(s*.101,-.010,.314),(s*.104,.062,.219),(s*.098,.116,.131)],[.029,.020,.013],mat='tail',n=9,aspect=.85)
        tube('Limbs',label+'_Long_metatarsus',[(s*.098,.116,.137),(s*.095,.082,.071),(s*.093,.042,.026)],[.014,.012,.014],mat='tail',n=8,aspect=.83)
        for j in range(3):
            x=s*(.093+(j-1)*.023);y=-.068-(.022 if j==1 else 0)
            tube('Limbs',label+'_Foot_digit_'+str(j+2),[(s*.093,.042,.026),(x,-.012,.016),(x+s*(j-1)*.008,y,.011)],[.010,.007,.0045],mat='tail',n=7,aspect=.78)
            tube('Keratin_details',label+'_Foot_claw_'+str(j+2),[(x+s*(j-1)*.008,y,.011),(x+s*(j-1)*.009,y-.017,.006),(x+s*(j-1)*.009,y-.024,.0025)],[.0047,.003,.00075],mat='keratin',n=6,aspect=.8)
        tube('Limbs',label+'_Small_hallux',[(s*.083,.061,.041),(s*.068,.080,.026),(s*.061,.095,.022)],[.0055,.0035,.0015],mat='tail',n=6)
        tube('Limbs',label+'_Short_upper_arm',[(s*.055,-.145,.443),(s*.073,-.169,.388),(s*.079,-.180,.355)],[.024,.020,.014],n=8)
        tube('Limbs',label+'_Short_forearm',[(s*.079,-.180,.355),(s*.086,-.224,.332),(s*.087,-.248,.322)],[.014,.011,.009],mat='tail',n=8)
        tube('Limbs',label+'_Inward_palm',[(s*.087,-.246,.324),(s*.088,-.260,.308)],[.012,.011],mat='tail',n=8,aspect=.65)
        for j in range(3):
            y=-.266+j*.010;z=.309-j*.004;ln=[.024,.033,.028][j]
            tube('Limbs',label+'_Manual_digit_'+str(j+1),[(s*.089,y,z),(s*.091,y-.012,z-ln*.65),(s*.086,y-.016,z-ln)],[.0047,.0035,.0018],mat='tail',n=6)
        for j in range(2):tube('Limbs',label+'_Reduced_manual_digit_'+str(j+4),[(s*.089,-.240+j*.008,.307),(s*.088,-.247+j*.008,.292)],[.0032,.001],mat='tail',n=5)
    # Short irregular filament bundles. Distribution and density are inferred, not fossil counts.
    for i in range(150):
        y=random.uniform(-.17,.19);a=random.uniform(-.40,math.pi+.40);z,rx,rz=interpolate(trunk,y)
        hair((rx*math.cos(a),y,z+rz*math.sin(a)),(math.cos(a),0,math.sin(a)),random.uniform(.020,.030),'dorsal' if math.sin(a)>.5 else 'cover','Trunk_tuft_%03d'%i)
    for i in range(30):
        y=random.uniform(-.31,-.205);ns=sorted(neck);z,rx,rz=interpolate(ns,y);a=random.uniform(0,math.pi)
        hair((rx*math.cos(a),y,z+rz*math.sin(a)),(math.cos(a),0,math.sin(a)),random.uniform(.013,.019),'cover','Neck_filament_%02d'%i,bundle=2)
    for i in range(45):
        y=random.uniform(-.420,-.345);ss=sorted(skull);z,rx,rz=interpolate(ss,y);a=random.uniform(.15,math.pi-.15)
        hair((rx*math.cos(a),y,z+rz*math.sin(a)),(math.cos(a),0,math.sin(a)),random.uniform(.010,.015),'dorsal','Head_filament_%02d'%i,bundle=2)
    for s,label in [(1,'R'),(-1,'L')]:
        for i in range(22):
            t=random.uniform(.10,.77);c=Vector((s*(.062+.039*t),.120-.130*t,.479-.169*t));a=random.uniform(-.5,2.7)
            n=Vector((s*math.cos(a),math.sin(a),.2));rad=.061*(1-t)+.031*t
            hair(c+n.normalized()*rad,n,random.uniform(.020,.030),'cover',label+'_Femoral_bundle_%02d'%i)
        for i in range(8):
            t=random.uniform(.05,.70);c=Vector((s*(.055+.024*t),-.145-.035*t,.443-.088*t));n=Vector((s,random.uniform(-.4,.5),.3))
            hair(c+n.normalized()*(.024-.010*t),n,.019,'cover',label+'_Humeral_bundle_%02d'%i)
    # All source components remain selectable as named vertex groups in six semantic meshes.
    # Merge by semantic family rather than hundreds of draw calls; no source-only modifiers.
    pts=[Vector(v) for b in B.values() for v in b['v']];scale=P['total_length_target_m']/(max(v.y for v in pts)-min(v.y for v in pts));minz=min(v.z for v in pts)
    for group,b in B.items():
        mats=list(dict.fromkeys(b['m']));vs=[(v[0]*scale,(v[1]-.001)*scale,(v[2]-minz)*scale) for v in b['v']]
        obj=mesh_object(group,vs,b['f'],[M[m] for m in mats],COL)
        for p,mi in zip(obj.data.polygons,b['m']):p.material_index=mats.index(mi)
        for name,start,count in b['semantic']:obj.vertex_groups.new(name=name).add(list(range(start,start+count)),1,'REPLACE')
        obj['semantic_component_count']=len(b['semantic']);obj['original_geometry']=True
    return COL

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--out',type=Path,required=True);pa.add_argument('--clay',action='store_true');args=pa.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True);col=build();bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    bpy.context.scene.render.filepath='//'
    # Clear factory-startup browser locations from the editable public source.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'';space.params.filename=''
    bpy.context.preferences.filepaths.temporary_directory='' 
    meta={'generator':'source/generate.py','revision':P['revision'],'representation':'living-reconstruction','scale_basis':'Approximate 1.5 m descriptive length, composite anatomy rather than complete individual measurement','surface_profile':'Opaque palette-only PBR; original inferred colours','scientific_notes':'Thin epidermal tail scales, not osteoderms. Short filamentous integument, not flight feathers. Original source Fig.1 is composite.','export_texcoords':False}
    stage=out/'private'/'export-stage'
    export_asset(P['asset_id'],{'en':'Kulindadromeus','zh':'库林达奔龙'},'dinosaurs',col,meta,output_root=stage,render=False,max_triangles=6500,max_materials=6,max_primitives=12)
    gen=stage/P['asset_id'];shutil.copyfile(gen/(P['asset_id']+'.glb'),out/'model.glb');shutil.copyfile(gen/(P['asset_id']+'.blend'),out/'model.blend')
    ev=out/'qa/evidence';ev.mkdir(parents=True,exist_ok=True);q=json.loads((gen/'qa.json').read_text());q['glb']['file']='model.glb';q['subject_glb_sha256']=hashlib.sha256((out/'model.glb').read_bytes()).hexdigest();(ev/'source-and-glb.json').write_text(json.dumps(q,indent=2)+'\n')
    m=json.loads((gen/'metadata.json').read_text());m.update(glb='model.glb',blend='model.blend',preview='preview.png');(ev/'build-metadata.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
    if args.clay:
        bpy.context.view_layer.material_override=make_material('Authoring_clay','#939393',roughness=.85)
        render_previews(col,out/'private/clay',views=('front','side','top','hero'),resolution=480,samples=8)
    print('BUILD_COMPLETE')
if __name__=='__main__':main()
