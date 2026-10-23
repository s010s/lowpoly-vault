# SPDX-License-Identifier: MIT
"""Original Rhizodus P3317 left-ramus study. Not a scan or exact replica.
Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output-dir OUTPUT
Only this source folder and its declared deps are required. Export has no textures.
"""
from pathlib import Path
import sys, json, math, random, hashlib, argparse, shutil
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from asset_common import setup_scene, make_material, mesh_object, export_asset
from mathutils import Vector

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--gray',action='store_true'); a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    p=json.loads((HERE/'params.json').read_text()); out=a.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    random.seed(p['seed']); col=setup_scene('rhizodus',p['seed']); root=bpy.data.objects[col['asset_root']]
    root['representation']='Single preserved left mandibular ramus, NHM P3317 plate-guided study'
    root['scale_status']='Approximate plate estimate, not a direct specimen measurement'
    root['uncertainty']='Thickness and unseen medial surfaces are artistic interpretation; no missing third coronoid fang restored'
    root['anterior']='-Y'; root['lingual']='+X'; root['labial']='-X'
    palette=p['palette']
    mats=[make_material(n,'#929292' if a.gray else c,roughness=r) for n,c,r in palette]
    cortex,worn,tooth,deep=mats
    # Main ventral infradentary shell: closed material shell with a genuinely
    # open medial recess, not a solid box or a filled Meckelian region.
    # All positions are in metres. Longitudinal stations are not a pixel trace.
    N=44; verts=[]; faces=[]
    def lerp_profile(y,points):
        for (ya,va),(yb,vb) in zip(points,points[1:]):
            if ya<=y<=yb: return va+(vb-va)*(y-ya)/(yb-ya)
        return points[0][1] if y<points[0][0] else points[-1][1]
    bottom=[(-.135,.006),(-.129,.001),(-.100,0),(-.071,.0022),(-.050,.001),(-.010,.0017),(.030,.0035),(.063,.0015),(.100,.003),(.130,.004),(.135,.008)]
    height=[(-.135,.021),(-.122,.027),(-.080,.028),(-.038,.031),(.010,.035),(.050,.040),(.082,.043),(.110,.038),(.135,.024)]
    top_d=[(-.133,.038),(-.114,.041),(-.070,.042),(-.030,.043),(.010,.045),(.040,.044),(.063,.050),(.085,.049),(.100,.046)]
    wall_rings=[]
    for i in range(N+1):
        y=-.135+.270*i/N; z0=lerp_profile(y,bottom); h=lerp_profile(y,height)
        x=-.009+ .0015*math.cos((y+.11)*19)
        # The posterior broken outline is uneven, but no fantasy missing bone added.
        z0+=0.00045*math.sin(i*2.3); h+=0.00065*math.sin(i*1.9)
        inner=-.0020+0.0007*math.sin(i*.65); med=.0035+.007*math.sin(math.pi*i/N)**.65
        ring=[(x+.002,y,z0),(x-.0003,y,z0+.004),(x-.0012,y,z0+(h-z0)*.26),
              (x-.0019,y,z0+(h-z0)*.52),(x-.0006,y,z0+(h-z0)*.77),(x+.001,y,h),
              (inner+.0005,y,h+.0002),(inner,y,h-.004),(inner-.0014-.0011*math.sin(i*.42),y,z0+(h-z0)*.55),
              (inner+.0008,y,z0+.008),(med,y,z0+.006),(med+.0005,y,z0+.0025)]
        # Restrained irregular weathering and shallow diagonal bone divisions.
        for k in (2,3,4):
            xx,yy,zz=ring[k]
            frac=(zz-z0)/(h-z0)
            seam=min(abs(y-(base+.05*(1-frac))) for base in (-.077,-.012,.053))
            groove=.00085*math.exp(-(seam/.005)**2)
            ring[k]=(xx+.0004*math.sin(i*1.8+k*3.1)+groove,yy,zz)
        # Broken anterior/posterior edges are beveled, not a perfect saw-cut.
        if i in (0,N):
            sign=1 if i==0 else -1
            ring=[(xx,yy+sign*(.0015+.0014*math.sin(k*1.7)**2),zz) if k not in (2,3) else (xx,yy,zz) for k,(xx,yy,zz) in enumerate(ring)]
        wall_rings.append(ring); verts.extend(ring)
    nr=len(wall_rings[0])
    for i in range(N):
        for k in range(nr):
            v0=i*nr+k; v1=i*nr+(k+1)%nr; v2=(i+1)*nr+(k+1)%nr; v3=(i+1)*nr+k
            if k in (1,2,3,4,7,8) and i%2: faces.extend([(v0,v1,v3),(v1,v2,v3)])
            else: faces.append((v0,v1,v2,v3))
    faces.append(tuple(reversed(range(nr)))); faces.append(tuple(N*nr+k for k in range(nr)))
    wall=mesh_object('infradentary_wall_and_ventral_flange',verts,faces,[cortex,worn,deep],col)
    # Worn broken terminal surfaces and restrained natural cortical variation.
    for face in wall.data.polygons:
        c=face.center
        face.material_index=1 if abs(c.y)>.132 else (2 if c.x>-.003 and c.z>.009 else 0)
    wall['interpretation']='Open lingual recess; no ossified Meckelian fill; thickness inferred'
    # Tooth-bearing dentary, slender posterior continuation retained in silhouette.
    dv=[]; df=[]; drings=29; sides=10
    for i in range(drings):
        t=i/(drings-1); y=-.133+.233*t; top=lerp_profile(y,top_d)
        depth=lerp_profile(y,[(-.133,.016),(-.09,.018),(-.025,.014),(.03,.013),(.07,.011),(.10,.006)])
        width=lerp_profile(y,[(-.133,.012),(-.11,.018),(-.05,.016),(.035,.015),(.075,.012),(.1,.006)])
        cx=-.0020+.0007*math.sin(t*math.pi)
        for j in range(sides):
            ang=2*math.pi*j/sides
            # a little asymmetry produces a preserved bony ledge, not a cylinder
            xx=cx+math.cos(ang)*width*.5
            zz=top-depth*.5+math.sin(ang)*depth*.5
            xx+=.0004*math.sin(i*2.4+j*.8); zz+=.00045*math.sin(i*1.4+j*1.7)
            dv.append((xx,y,zz))
    for i in range(drings-1):
        for j in range(sides):
            df.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    df += [tuple(reversed(range(sides))),tuple((drings-1)*sides+j for j in range(sides))]
    dent=mesh_object('dentary_tooth_bearing_bar',dv,df,[cortex,worn],col)
    for f in dent.data.polygons: f.material_index=1 if abs(f.center.y+.133)<.001 or f.center.y>.097 else 0
    # A modest lingual coronoid ledge supports only the two visible fangs.
    # It does not recreate the missing third coronoid of a complete jaw.
    cv=[]; cf=[]; cs=8
    for i in range(21):
        t=i/20; y=-.093+.133*t; top=lerp_profile(y,top_d)-.0008
        fade=math.sin(math.pi*t)**.45
        rx=.0016+.0062*fade; rz=.0015+.0018*fade; cx=.0012+.0008*fade
        for j in range(cs):
            ang=2*math.pi*j/cs
            cv.append((cx+rx*math.cos(ang),y,top-rz+rz*math.sin(ang)))
    for i in range(20):
        for j in range(cs): cf.append((i*cs+j,i*cs+(j+1)%cs,(i+1)*cs+(j+1)%cs,(i+1)*cs+j))
    cf+=[tuple(reversed(range(cs))),tuple(20*cs+j for j in range(cs))]
    shelf=mesh_object('preserved_lingual_coronoid_shelf',cv,cf,cortex,col)
    shelf['reconstruction']='Interpretive medial support shelf; exact interior not preserved in the plate view'
    # Conical, slightly posterior-recurved teeth with broad bases, not triangular blades.
    def tooth_geometry(x,y,z,height,radius,bend,sides=10):
        vv=[]; ff=[]; levels=[(0,1),(.18,.98),(.46,.76),(.72,.46),(.92,.18)]
        for li,(t,r) in enumerate(levels):
            for j in range(sides):
                angle=j*2*math.pi/sides
                rr=radius*r*(1+(.06 if j%2 else -.03))
                vv.append((x+math.cos(angle)*rr*(1-.08*t),y+bend*t*t+math.sin(angle)*rr,z+height*t))
        for i in range(len(levels)-1):
            for j in range(sides): ff.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
        tip=len(vv); vv.append((x-.0004,y+bend,z+height))
        for j in range(sides): ff.append(((len(levels)-1)*sides+j,(len(levels)-1)*sides+(j+1)%sides,tip))
        ff.append(tuple(reversed(range(sides))))
        return vv,ff
    large=[('anterior_mesial_tusk',-.001,-.116,.039,.0049,.0022),
           ('coronoid_fang_1',.0064,-.048,.0255,.0036,.0021),
           ('coronoid_fang_2',.0062,.002,.0238,.0035,.0020)]
    for name,x,y,h,r,b in large:
        z=lerp_profile(y,top_d)-.0016
        v,f=tooth_geometry(x,y,z,h,r,b,12); obj=mesh_object(name,v,f,tooth,col)
        obj['role']='Mesial/anterior tusk' if 'anterior' in name else 'Plate-supported lingual coronoid fang'
    # Uneven preservation of the marginal row. Missing gaps are intentional.
    small=[(-.102,.0090,.0018,.005),(-.091,.0102,.0017,.004),(-.078,.0062,.0019,.0035),
           (-.068,.0120,.0020,.0016),(-.061,.0098,.0015,.0003),(-.055,.0082,.0015,.0006),
           (-.039,.0090,.0017,.0010),(-.031,.0084,.0018,.0025),(-.023,.0102,.0017,.0010),
           (-.016,.0083,.0014,.0015),(-.008,.0093,.0015,.0011),(.010,.0065,.0018,-.0042),
           (.022,.0041,.0019,-.0035),(.034,.0081,.0018,.0020),(.049,.0073,.0017,.0018),
           (.064,.0052,.0016,.0012)]
    sv=[]; sf=[]
    for i,(y,h,r,b) in enumerate(small):
        x=-.0051+.0005*math.sin(i*1.4); z=lerp_profile(y,top_d)-.0012
        v,f=tooth_geometry(x,y,z,h,r,b,8); n=len(sv); sv.extend(v); sf.extend(tuple(j+n for j in q) for q in f)
    row=mesh_object('irregular_labial_marginal_teeth',sv,sf,tooth,col)
    row['count']=len(small); row['position']='Labial marginal row, distinct from lingual coronoid fangs'
    # Ground the lowest preserved edge, with root at footprint centre.
    low=min((o.matrix_world@v.co).z for o in col.all_objects if o.type=='MESH' for v in o.data.vertices)
    for o in col.all_objects:
        if o.type=='MESH':
            for v in o.data.vertices: v.co.z-=low
    bpy.context.view_layer.update()
    record=export_asset('rhizodus',{'en':'Rhizodus — fossil jaw study','zh':'根齿鱼（颌骨化石研究）'},'fossils',col,
        metadata={'generator':'source/generate.py','generator_sha256':sha(__file__), 'params_sha256':sha(HERE/'params.json'),
                  'revision':'r001','representation':'fossil-specimen','specimen':'P3317 left mandibular ramus',
                  'reconstruction_notes':['Only plate-supported preserved single left ramus; no mirrored mate or third large fang.','Approximate 0.27 m plate-derived length, not a specimen measurement.','Width, internal recess and material palette are restrained artistic interpretation.'],
                  'description':{'en':'Original low-poly plate-guided study of the preserved left jaw of Rhizodus hibberti. Approximate scale; not a scan or exact replica.','zh':'根据历史图版制作的根齿鱼左颌支化石原创低多边形研究；尺寸为图版估算，不是扫描或精确复刻。'},
                  'sources':['https://archive.org/details/catalogueoffossi02brit','https://doi.org/10.1017/S0263593300000432']},
        output_root=out/'raw',render=False,max_triangles=5000,max_materials=5,max_primitives=28)
    built=out/'raw'/'rhizodus'
    shutil.copy2(built/'rhizodus.glb',out/'model.glb'); shutil.copy2(built/'rhizodus.blend',out/'model.blend')
    shutil.copy2(built/'qa.json',out/'technical.json')
    record['glb']='model.glb'; record['blend']='model.blend'; record['preview']='preview.png'
    record['origin']='Lowest preserved edge at Z=0; longitudinal footprint centered at origin'
    record['scale_confidence']='PLATE_ESTIMATE_NOT_DIRECT_SPECIMEN_MEASUREMENT'
    record['no_external_runtime_dependencies']=True
    (out/'metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'MADE_NOT_INDEPENDENTLY_REVIEWED','triangles':record['triangles'],'bytes':record['glb_bytes'],'glb_sha256':record['sha256']['glb']}))
if __name__=='__main__': main()
