# SPDX-License-Identifier: MIT
"""Original batch04 geometry. Blender 4.3.2; one worker, two threads.
blender -b -t 2 --python-exit-code 1 --python THIS -- --config CONFIG --output-dir DIR
Output dir is the immutable attempt bundle itself. No third-party media.
"""
import argparse, hashlib, importlib.util, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene, make_material, mesh_object, export_asset, ground_asset, render_previews
# Reuse this repository's MIT geometry utility, never its subject geometry.
spec=importlib.util.spec_from_file_location('trio_util',ROOT/'production/small-fauna-trio-v2/build_trio.py')
util=importlib.util.module_from_spec(spec);spec.loader.exec_module(util)
Part=util.Part
pi=math.pi

def loft(part, profiles, n=28, mi=0):
    """Y-axis continuous loft with nonzero pole rings, explicit caps."""
    v=[]
    for y,w,z,h in profiles:
        for k in range(n):
            a=2*pi*k/n;v.append((w*math.cos(a),y,z+h*math.sin(a)))
    f=[tuple(reversed(range(n)))]
    for j in range(len(profiles)-1):
        for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    f.append(tuple((len(profiles)-1)*n+k for k in range(n)))
    part.add(v,f,mi)

def calceola(c,m):
    # D-shaped section: a broad flat hinge edge and a curved slipper front.
    outline=[(.026*math.cos(pi*k/32),.004-.044*math.sin(pi*k/32)) for k in range(33)]
    n=len(outline);v=[]
    rings=[(.002,.10),(.006,.22),(.012,.43),(.021,.70),(.030,.91),(.036,1),(.037,1.005),(.0365,.91),(.031,.84),(.020,.56),(.014,.22)]
    for j,(z,r) in enumerate(rings):
        for k,(x,y) in enumerate(outline):
            # Broad coherent growth folds; no random polygon noise.
            a=2*pi*k/n;fold=1+.012*math.sin(11*a)*(1 if j<7 else .25)
            v.append((x*r*fold, -.022+(y+.022)*r, z+.00030*math.sin(2*a)*r))
    f=[tuple(reversed(range(n)))];mi=[0]
    for j in range(len(rings)-1):
        for k in range(n):
            f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if j in (5,6) else 2 if j>7 else 0)
    f.append(tuple((len(rings)-1)*n+k for k in range(n)));mi.append(2)
    p=Part('continuous-slipper-cup-and-recess',m);p.add(v,f,mi);p.finish(c,True)
    # One semicircular operculum, gently ajar; hinge remains physically connected.
    lid=Part('single-semicircular-lid',m)
    hinge=Vector((0,.004,.037));rot=Matrix.Rotation(math.radians(-30),3,'X')
    shape=[Vector((x*.98,(y-.004)*.98,0)) for x,y in outline]
    vv=[]
    for side in (-1,1):
        for q in shape:vv.append(tuple(hinge+rot@(q+Vector((0,0,side*.0009)))))
    center=Vector((0,-.016,.003));vv.extend([tuple(hinge+rot@(center+Vector((0,0,-.0009)))),tuple(hinge+rot@(center+Vector((0,0,.0009))))])
    ff=[];ii=[]
    for k in range(n):
        j=(k+1)%n;ff.extend([(2*n,k,j),(2*n+1,n+j,n+k),(k,n+k,n+j,j)]);ii.extend([2,1,0])
    lid.add(vv,ff,ii);lid.finish(c,True)
    ridges=Part('restrained-growth-ribs-and-hinge',m)
    ridges.tube([(-.022,.004,.0365),(0,.004,.037),(.022,.004,.0365)],[.001,.0011,.001],0,10)
    # Soft septal ribs in the open cup, modestly visible rather than a micro-array.
    for k in range(1,13):
        a=pi*k/14
        x=.026*math.cos(a);y=.004-.044*math.sin(a)
        pts=[(x*r,-.022+(y+.022)*r,z+.00025) for r,z in [(.22,.014),(.56,.020),(.84,.031),(.91,.0365)]]
        ridges.tube(pts,[.00020,.00030,.00030,.00015],1,6)
    ridges.finish(c,True)
    # Frozen nominal span applies to the largest cup/lid extent.
    for o in c.objects:
        if o.type=='MESH':
            for vv in o.data.vertices:vv.co.z*=.62
    points=[v.co for o in c.objects if o.type=='MESH' for v in o.data.vertices]
    span=max(max(v[i] for v in points)-min(v[i] for v in points) for i in range(3))
    for o in c.objects:
        if o.type=='MESH':
            for v in o.data.vertices:v.co*=.07/span
    ground_asset(c)

def favosites(c,m):
    # A welded colony surface. Adjacent hexagons share their outer vertices;
    # recessed calices are part of the mound, never stacks of detached tubes.
    radius=.0113;v=[];f=[];mi=[];lookup={};outer_edges={}
    def vert(q,shared=False):
        key=tuple(round(a,8) for a in q)
        if shared and key in lookup:return lookup[key]
        i=len(v);v.append(q)
        if shared:lookup[key]=i
        return i
    def height(x,y):
        r=((x/.09)**2+(y/.077)**2)**.5
        return .018+.038*max(0,1-r*r)**.72+.003*math.sin(x*19+y*13)
    for q in range(-4,5):
        for r in range(-4,5):
            if max(abs(q),abs(r),abs(q+r))>4:continue
            cx=radius*math.sqrt(3)*(q+r/2);cy=radius*1.5*r
            rings=[]
            for rr,dz in [(1,0),(.82,.0005),(.68,-.0010),(.59,-.0060)]:
                ring=[]
                for k in range(6):
                    a=pi/6+2*pi*k/6;x=cx+radius*rr*math.cos(a);y=cy+radius*rr*math.sin(a)
                    ring.append(vert((x,y,height(x,y)+dz),rr==1))
                rings.append(ring)
            for k in range(6):
                a,b=rings[0][k],rings[0][(k+1)%6];key=tuple(sorted((a,b)))
                outer_edges[key]=outer_edges.get(key,0)+1
            for j in range(3):
                for k in range(6):f.append((rings[j][k],rings[j][(k+1)%6],rings[j+1][(k+1)%6],rings[j+1][k]));mi.append(1 if j==0 else 0 if j==1 else 2)
            f.append(tuple(rings[-1]));mi.append(2)
    # Boundary skirt and sealed basal underside, with no internal colony walls.
    boundary=[edge for edge,count in outer_edges.items() if count==1];low={}
    for a,b in boundary:
        for i in (a,b):
            if i not in low:low[i]=vert((v[i][0]*.92,v[i][1]*.92,0))
        f.append((a,b,low[b],low[a]));mi.append(0)
    center=vert((0,0,0))
    for a,b in boundary:f.append((center,low[a],low[b]));mi.append(0)
    p=Part('welded-honeycomb-colony-with-recessed-calices',m);p.add(v,f,mi);o=p.finish(c,False)
    # Hexagonal colony envelope is softened by an ellipse at its extremities.
    for vv in o.data.vertices:
        x,y,z=vv.co
        vv.co.x=x*(1-.06*(y/.077)**2)*(1+.06*math.sin(y*35))+.004*math.sin(y*26)+.001*math.sin(y*80+x*45)
        vv.co.y=y*.98*(1+.07*math.cos(x*27))+.003*math.sin(x*20)
        vv.co.z=z*(1+.10*math.sin(x*23-y*32))
    ground_asset(c)

def opabinia(c,m):
    body=Part('continuous-low-body-head-and-tapered-trunk',m)
    profiles=[(-.038,.0007,.011,.0015),(-.037,.006,.0115,.005),(-.033,.010,.012,.007),(-.025,.011,.012,.0075)]
    for j in range(23):
        t=j/22;y=-.020+t*.067;w=.0105*(1-.72*t**1.7);z=.011+.002*math.sin(t*pi)
        profiles.append((y,w*(1+.025*math.cos(j*pi)),z,.0065*(1-.65*t)))
    profiles.extend([(.050,.0017,.011,.0018),(.052,.0006,.011,.0007)])
    loft(body,profiles,32,0);body.finish(c,True)
    flaps=Part('paired-soft-overlapping-lateral-lobes-and-tail-fan',m)
    # Closed curved lenses blend broad roots into the continuous trunk.
    def lens(outline,thick,mat):
        n=len(outline);center=sum((Vector(p) for p in outline),Vector())/n
        vv=[tuple(Vector(p)+Vector((0,0,thick/2))) for p in outline]+[tuple(Vector(p)-Vector((0,0,thick/2))) for p in outline]
        vv.extend([tuple(center+Vector((0,0,thick*1.2))),tuple(center-Vector((0,0,thick*.6)))])
        ff=[]
        for k in range(n):
            j=(k+1)%n;ff.extend([(2*n,k,j),(2*n+1,n+j,n+k),(k,n+k,n+j,j)])
        flaps.add(vv,ff,mat)
    for j in range(12):
        t=j/11;y=-.022+j*.0058;w=.0105*(1-.65*t**1.6);spread=.012*(1-.50*t)+.001*math.sin(j*.7)
        for s in (-1,1):
            lens([(s*w*.75,y-.0028,.010),(s*(w+spread*.48),y-.0018,.0105),(s*(w+spread),y+.002,.008),(s*(w+spread*.9),y+.005,.007),(s*(w+spread*.40),y+.007,.0075),(s*w*.75,y+.005,.010)],.00075,1 if j%3 else 2)
    for s in (-1,1):
        for j in range(3):
            y=.039+j*.0038
            lens([(s*.002,y,.011),(s*.009,y+.003,.016+j*.001),(s*.016,y+.013,.020+j*.001),(s*.013,y+.017,.017),(s*.003,y+.007,.011)],.0008,1)
    flaps.finish(c,True)
    face=Part('five-short-eye-stalks-and-five-eyes',m)
    eyes=[(-.0065,-.033,.021),(.0065,-.033,.021),(-.008,-.025,.022),(.008,-.025,.022),(0,-.026,.025)]
    for x,y,z in eyes:
        face.tube([(x*.72,y+.001,.016),(x*.95,y,z-.001)],[.0011,.0010],0,10)
        face.ellipsoid((x,y,z),(.0018,.00165,.0017),3,16,9)
        face.ellipsoid((x-.0004,y-.0010,z+.0010),(.00045,.00035,.00035),4,10,5)
    face.finish(c,True)
    nozzle=Part('single-curving-proboscis-and-opposed-terminal-grasper',m)
    pts=[(0,-.036,.0115),(0,-.045,.011),( .001,-.056,.009),(.003,-.067,.007),(.004,-.076,.009),(.003,-.081,.012)]
    nozzle.tube(pts,[.0023,.0021,.00185,.0016,.00135,.00125],0,14)
    for s in (-1,1):
        nozzle.tube([(.003,-.080,.012),(.003+s*.0029,-.082,.0127),(.003+s*.0038,-.086,.0134),(.003+s*.0019,-.089,.0132)],[.0012,.00095,.00067,.00025],2,10)
    nozzle.finish(c,True)
    # Body length (without proboscis/fan) is an artistic nominal 0.1m.
    factor=.1/.09
    for o in c.objects:
        if o.type=='MESH':
            for vv in o.data.vertices:vv.co*=factor
    # Swimming specimen: root is below body centreline, never ground-normalized.

def choia(c,m):
    disc=Part('flattened-elliptical-sponge-disc',m);n=64;v=[]
    # Nested radial rings give a thin softly domed disc, no ball shell.
    rings=[(.08,.0034),(.30,.0035),(.62,.0030),(1,.0016),(.98,.0006),(.55,.0002),(.08,.0004)]
    for j,(r,z) in enumerate(rings):
        for k in range(n):
            a=2*pi*k/n;d=1+.018*math.sin(5*a)+.012*math.sin(9*a)
            v.append((.0128*r*math.cos(a)*d,.0103*r*math.sin(a)*d,z+.00018*r*math.sin(3*a)))
    top=len(v);v.append((0,0,rings[0][1]));bot=len(v);v.append((0,0,rings[-1][1]))
    f=[(top,k,(k+1)%n) for k in range(n)];mi=[0]*n
    for j in range(len(rings)-1):
        for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(0 if j<3 else 2)
    f.extend((bot,(len(rings)-1)*n+(k+1)%n,(len(rings)-1)*n+k) for k in range(n));mi.extend([2]*n)
    disc.add(v,f,mi);disc.finish(c,True)
    spokes=Part('ordered-radial-long-spicules-and-fine-disc-rays',m)
    for k in range(46):
        a=2*pi*k/46+.012*math.sin(k*1.7);co=math.cos(a);si=math.sin(a)
        length=.025+.003*math.sin(3*a)+.0014*math.sin(k*2.1)
        p=Vector((.0077*co,.0062*si,.0025));q=Vector((length*co,length*.91*si,.00055+.0003*math.cos(2*a)))
        mid=p.lerp(q,.55)+Vector((-.0004*si,.0004*co,.0003))
        spokes.tube([p,mid,q],[.00034,.00025,.00007],1 if k%4 else 2,7)
    for k in range(82):
        a=2*pi*k/82;co=math.cos(a);si=math.sin(a)
        spokes.tube([(.0023*co,.0018*si,.00348),(.007*co,.0056*si,.0032),(.0125*co,.0101*si,.0017)],[.00013,.00014,.00009],1,5)
    spokes.finish(c,True)
    points=[vv.co for o in c.objects if o.type=='MESH' for vv in o.data.vertices]
    span=max(max(p.x for p in points)-min(p.x for p in points),max(p.y for p in points)-min(p.y for p in points))
    for o in c.objects:
        if o.type=='MESH':
            for vv in o.data.vertices:vv.co*=.06/span
    ground_asset(c)

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    conf=json.loads(a.config.read_text());s=conf['asset_id'];out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    if any(out.glob('*.glb')):raise RuntimeError('Never overwrite a completed attempt')
    c=setup_scene(s,conf['seed'])
    palettes={'calceola':['#B0957B','#D4C1A0','#82786A'],'favosites':['#AA927E','#D3BFA0','#7C7566'],'opabinia':['#819F9E','#ACC1AE','#99AAA0','#344B50','#D6DDD0'],'choia':['#A8AD90','#C8C9A8','#8D977E']}
    mats=[make_material(s+'-'+str(i),color,roughness=.82) for i,color in enumerate(palettes[s])]
    globals()[s](c,mats)
    plan=ROOT/'production/continuous-small-life-round02-20261018/items'/s
    brief=json.loads((plan/'brief.json').read_text());refs=json.loads((plan/'references.json').read_text())
    meta={'revision':'r001','attempt':conf['attempt'],'status':'candidate-awaiting-independent-QA','generator':str(Path(__file__).relative_to(ROOT)),'config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest(),'claim_scope':brief['claim_scope'],'nominal_scale':brief['scale'],'sources':refs['sources'],'description':{'en':brief['distinctness']['en']+' Original stylized teaching art. Palette, nominal size, pose and simplified details are artistic choices; no scientific reconstruction or coexistence claim.','zh':brief['distinctness']['zh']+' 原创风格化教学道具；配色、标称尺寸、姿态及简化细节是美术选择，非严格科学或同域共存复原。'},'mounting_point':'body-centreline mounting pivot at origin; free swimming, lowest surface intentionally above zero' if s=='opabinia' else 'floor contact centre; lowest authored Z=0; identity root','textures':'none; original palette only','warnings_disposition':'Smooth shading is intentional on continuous organic parts. Flat honeycomb calices are deliberate. Parts are closed; semantic parts may overlap at anatomical attachments.'}
    # Shared export helper adds slug; relocate once to keep mandated bundle layout.
    temp=out/'_export';export_asset(s,brief['subject']['inventory_name'],'animals',c,metadata=meta,output_root=temp,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
    for f in (temp/s).iterdir():f.replace(out/f.name)
    (temp/s).rmdir();temp.rmdir()
    data=json.loads((out/'metadata.json').read_text())
    rel=out.relative_to(ROOT).as_posix() if out.is_relative_to(ROOT) else str(out)
    for k,filename in [('glb',s+'.glb'),('blend',s+'.blend'),('preview','preview-hero.png')]:data[k]=rel+'/'+filename
    (out/'metadata.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    if a.preview:render_previews(c,out,views=tuple(conf['required_views']),resolution=512,samples=16,transparent=True)
if __name__=='__main__':main()
