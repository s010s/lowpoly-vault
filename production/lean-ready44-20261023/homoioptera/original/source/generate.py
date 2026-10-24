# SPDX-License-Identifier: MIT
"""Original same-species Homoioptera vorhallensis reconstruction.
Run: blender -b -t 2 --python source/generate.py -- --output .
Only adjacent params.json and declared source/deps are generation inputs.
Coordinates below are millimeters, converted to meters at mesh creation.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys, tempfile
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene,make_material,mesh_object,export_asset

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

class Parts:
    def __init__(self,name,mat,col):self.name,self.mat,self.col=name,mat,col;self.v=[];self.f=[];self.groups=[]
    def add(self,name,verts,faces):
        n=len(self.v);self.v.extend(tuple(v) for v in verts);self.f.extend(tuple(n+i for i in f) for f in faces);self.groups.append((name,list(range(n,len(self.v)))))
    def finish(self):
        o=mesh_object(self.name,[tuple(a*.001 for a in v) for v in self.v],self.f,self.mat,self.col)
        for name,indices in self.groups:o.vertex_groups.new(name=name).add(indices,1,'REPLACE')
        o['component_names']=[n for n,_ in self.groups];o['construction']='Original profile meshes; intentional overlaps at articulated joints and surface vein roots.'
        return o

def tube(group,name,points,radii,sides=6):
    points=list(map(Vector,points));verts=[];faces=[]
    for i,p in enumerate(points):
        t=(points[min(len(points)-1,i+1)]-points[max(0,i-1)]).normalized();base=Vector((0,0,1))
        if abs(t.dot(base))>.9:base=Vector((0,1,0))
        u=t.cross(base).normalized();v=t.cross(u).normalized()
        verts.extend(p+radii[i]*(math.cos(2*math.pi*j/sides)*u+math.sin(2*math.pi*j/sides)*v) for j in range(sides))
    faces.append(tuple(reversed(range(sides))))
    for i in range(len(points)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
    faces.append(tuple((len(points)-1)*sides+j for j in range(sides)));group.add(name,verts,faces)

def loft(group,name,rows,n=16):
    # rows: y, horizontal radius, vertical radius, z center. No collapsed poles.
    verts=[];faces=[]
    for y,rx,rz,zc in rows:
        for j in range(n):
            a=2*math.pi*j/n;x=rx*math.cos(a);z=zc+rz*math.sin(a)
            if math.sin(a)>0:z-=.25*math.exp(-(x/.5)**2)*math.sin(a)
            verts.append((x,y,z))
    faces.append(tuple(reversed(range(n))))
    for i in range(len(rows)-1):
        for j in range(n):
            a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
    faces.append(tuple((len(rows)-1)*n+j for j in range(n)));group.add(name,verts,faces)

def patch(group,name,outline,center,depth=.10):
    # Closed shallow radial surface; original polygon, not a copied reference texture.
    N=len(outline);verts=[center]+outline+[(x,y,z-depth) for x,y,z in [center]+outline];faces=[];off=N+1
    for j in range(N):
        a=1+j;b=1+(j+1)%N;faces.extend([(0,a,b),(off,b+off,a+off),(a,a+off,b+off,b)])
    group.add(name,verts,faces)

def interp(t,items):
    for (a,x),(b,y) in zip(items,items[1:]):
        if a<=t<=b:return x+(y-x)*(t-a)/(b-a)
    return items[-1][1]

# Flight wings deliberately broad with rounded-pointed distal outlines.
WIDTH=[(0,4.0),(.06,13),(.16,23),(.29,31),(.43,37),(.57,40),(.70,39),(.81,32),(.90,23),(.96,12),(1,.45)]
def wing_point(side,kind,t,q):
    hind=kind=='hind';angle=math.radians(8 if hind else -7);length=91.3 if hind else 95.4
    w=interp(t,WIDTH)*(1.12 if hind else 1);x0=4.5;y0=-2 if hind else -15
    along=length*t;across=q*w;x=x0+along*math.cos(angle)-across*math.sin(angle);y=y0+along*math.sin(angle)+across*math.cos(angle)
    z=(10.2 if hind else 12.6)+(2.2 if hind else 4.0)*t+.60*math.sin(math.pi*t)*(1-(2*q-.2)**2)
    return(side*x,y,z)

def make_wing(mem,vein,side,kind):
    lab=('L' if side<0 else 'R')+'-'+kind;ts=[t for t,_ in WIDTH];qs=[-.38,-.18,.02,.22,.42,.62]
    rows=[[wing_point(side,kind,t,q) for q in qs] for t in ts];nr,nc=len(rows),len(qs)
    top=[v for r in rows for v in r];verts=top+[(x,y,z-.12) for x,y,z in top];off=len(top);faces=[]
    for r in range(nr-1):
        for c in range(nc-1):
            a=r*nc+c;b=a+1;d=a+nc;e=d+1;faces.extend([(a,b,e,d),(a+off,d+off,e+off,b+off)])
    border=list(range(nc))+[r*nc+nc-1 for r in range(1,nr)]+list(range((nr-1)*nc+nc-2,(nr-1)*nc-1,-1))+[r*nc for r in range(nr-2,0,-1)]
    for j,a in enumerate(border):
        b=border[(j+1)%len(border)];faces.append((a,a+off,b+off,b))
    mem.add(lab+'-broad-flight-wing',verts,faces)
    def raised(t,q):
        x,y,z=wing_point(side,kind,t,q);return(x,y,z+.085)
    # Simplified original venation: no claim of a fixed species diagnostic count.
    for q,label in [(-.38,'costa'),(-.26,'subcosta'),(-.11,'radius'),(.08,'media'),(.30,'cubitus'),(.62,'trailing-margin')]:
        end=.68 if label=='subcosta' else .985;tt=[t for t in ts if t<end]+[end]
        tube(vein,lab+'-'+label,[raised(t,q) for t in tt],[.13 if label in('costa','radius') else .095]*len(tt),5)
    for i,end in enumerate([.50,.61,.72,.83,.94]):
        tt=[.12,.25,(end+.25)/2,end];qq=[-.11,-.04,.19,.60]
        tube(vein,lab+f'-radial-sector-{i+1}',[raised(t,q) for t,q in zip(tt,qq)],[.11,.10,.085,.065],5)
    for i,end in enumerate([.16,.23,.30,.38,.46,.54,.62]):
        tube(vein,lab+f'-anal-fan-{i+1}',[raised(.012,.18),raised(end*.56,.43),raised(end,.61)],[.105,.09,.07],5)
    for j in range(1,27):
        t=.02+j*.035
        for k,(q1,q2) in enumerate([(-.38,-.26),(-.26,-.11),(-.11,.08),(.08,.30),(.30,.46),(.46,.62)]):
            t2=min(.975,t+(.010 if (j+k)%2 else -.009))
            tube(vein,lab+f'-crossvein-{j:02d}-{k}',[raised(t,q1),raised(t2,q2)],[.054,.054],4)

def build(p):
    col=setup_scene('homoioptera',p['seed'])
    colors={'cuticle':'#70533F','tergites':'#94704A','wings':'#D6CCA7','veins':'#857655','appendages':'#6D5941','eyes':'#242B29'}
    mats={k:make_material('Homoioptera-'+k,v,roughness=.83 if k!='eyes' else .35) for k,v in colors.items()}
    groups={k:Parts(n,mats[k],col) for k,n in [('cuticle','Head-and-three-thoracic-segments'),('tergites','Abdomen-ten-tergites'),('wings','Broad-flight-wings-and-small-prothoracic-lobes'),('veins','Simplified-wing-venation'),('appendages','Six-walking-legs-and-separate-head-and-tail-appendages'),('eyes','Paired-compound-eyes')]}
    C,A,W,V,P,E=[groups[k] for k in ['cuticle','tergites','wings','veins','appendages','eyes']]
    # Entire unflexed axial envelope is 85 mm, estimated from the 3 cm bar.
    loft(C,'Head-capsule',[(-32,2.4,2.3,9.4),(-31.5,3.4,2.9,9.5),(-29,3.8,3.2,9.6),(-27,3,2.5,9.3)],16)
    loft(C,'Prothorax',[(-27,2.7,2.6,9.2),(-26,3.4,3.4,9.1),(-22,3.6,3.5,9),(-20,3.5,3.1,9)],16)
    loft(C,'Mesothorax',[(-20,3.4,3.1,9),(-18,4.4,4.2,8.8),(-12,4.7,4.4,8.6),(-9,4.3,3.9,8.5)],16)
    loft(C,'Metathorax',[(-9,4.1,3.5,8.4),(-7,4.4,4.1,8.3),(-2,4.3,3.8,8.1),(1,3.8,3.2,8)],16)
    loft(C,'Abdominal-ventral-core',[(0,3.6,2.8,7.5),(10,3.7,2.7,7.2),(26,3.1,2.2,6.7),(40,2.4,1.7,6.2),(53,1.1,1.0,5.8)])
    for side in[-1,1]:
        tube(E,('L' if side<0 else 'R')+'-compound-eye',[(side*3.1,-30.8,9.6),(side*3.5,-29.8,10.2),(side*3.3,-28.8,10.2)],[.85,1.03,.8],12)
    # Tergites meet with a short natural imbrication; no invented external gills.
    widths=[8.2,8.6,8.4,8.0,7.6,7.1,6.4,5.6,4.6,3.4]
    for i,w in enumerate(widths):
        y=1+i*5.1;length=min(6.0,53-y);z=7.9-.20*i
        loft(A,f'Tergite-{i+1:02d}',[(y,w*.43,2.4-.12*i,z),(y+.6,w*.50,2.65-.13*i,z+.10),(y+length-.6,w*.49,2.55-.13*i,z),(y+length,w*.43,2.2-.12*i,z-.12)],16)
    for side in[-1,1]:
        lab='L' if side<0 else 'R';make_wing(W,V,side,'fore');make_wing(W,V,side,'hind')
        outline2=[(3.2,-27),(5.0,-30),(8.4,-30.4),(11.1,-29),(13,-26.7),(12.5,-24.5),(10.5,-22),(6.6,-20.7),(3.4,-21.4)]
        outline=[(side*x,y,11.4+.055*(x-3)) for x,y in outline2];center=(side*7.0,-25.2,12.0)
        patch(W,lab+'-small-prothoracic-lobe',outline,center,.12)
        for j in range(1,8):
            end=outline[j];start=(side*3.5,-23.6,11.7);mid=tuple((a+b)/2 for a,b in zip(start,end))
            tube(V,lab+f'-prothoracic-fan-{j}',[start,(mid[0],mid[1],mid[2]+.25),(end[0],end[1],end[2]+.07)],[.09,.08,.055],5)
        for t in[.42,.70,.88]:
            arc=[(side*3.5+(end[0]-side*3.5)*t,-23.6+(end[1]+23.6)*t,11.85+.17*t) for end in outline[1:8]]
            tube(V,lab+f'-prothoracic-cross-{t}',arc,[.045]*len(arc),4)
        # Walking pairs arise only on thorax, distinct from two maxillary palps.
        for i,(y,fy,fx) in enumerate([(-24,-36,14),(-14,-14,21),(-3,17,19)]):
            pts=[(side*3,y,6.8),(side*6.0,y-.3,5.8),(side*11.5,(y+fy)/2,7.4),(side*fx,fy,1.5)]
            tube(P,lab+f'-walking-leg-{i+1}-coxa-femur-tibia',pts,[.70,.80,.65,.40],8)
            start=Vector(pts[-1]);direction=Vector((side*.27,(-.85 if i<2 else .85),-.30)).normalized()
            for j in range(5):
                a=start+direction*(j*.64);b=start+direction*((j+1)*.64)
                tube(P,lab+f'-walking-leg-{i+1}-tarsus-{j+1}',[a,b],[.32-j*.038,.29-j*.038],6)
            end=start+direction*3.2
            for k in[-1,1]:
                tip=end+Vector((side*k*.40,(-.72 if i<2 else .72),-.25));tip.z=max(.08,tip.z)
                tube(P,lab+f'-walking-leg-{i+1}-claw-{k}',[end,tip],[.15,.045],5)
        ap=[];ar=[]
        for j in range(20):
            t=j/19;ap.append((side*(1.7+32*t+5*math.sin(math.pi*t)), -31-48*t,11+5*math.sin(math.pi*t)+4*t));ar.append(.34*(1-t)**1.2+.045)
        tube(P,lab+'-long-antenna',ap,ar,7)
        pp=[(side*1.8,-31.3,7.7),(side*3.6,-38,6.0),(side*5.1,-46,7.5),(side*4.5,-54,8.9)]
        tube(P,lab+'-head-origin-long-maxillary-palp',pp,[.38,.34,.27,.09],8)
        for j,t in enumerate([.30,.47,.65,.80]):
            a=Vector(pp[1]).lerp(Vector(pp[-1]),t);tube(V,lab+f'-palp-segmentation-{j}',[a,a+Vector((0,-.14,.03))],[.28-.16*t]*2,6)
        # 220 mm is an explicitly inferred completion, NOT a fully measured fossil.
        origin=Vector((side*1.3,52.8,5.9));raw=[]
        for j in range(65):
            t=j/64;raw.append(Vector((side*(20*t+15*math.sin(math.pi*t*.65)),216*t,4*t-1.1*math.sin(math.pi*t))))
        arc=sum((b-a).length for a,b in zip(raw,raw[1:]));factor=p['cerci_length_inferred']*1000/arc
        pts=[origin+v*factor for v in raw];radii=[.70*(1-j/64)**1.20+.055 for j in range(65)]
        tube(P,lab+'-220mm-inferred-cercus',pts,radii,7)
        for j in range(1,62):
            tangent=(pts[j+1]-pts[j-1]).normalized();width=.17*(1-j/65)+.035
            tube(V,lab+f'-cercus-articulation-{j:02d}',[pts[j]-tangent*width,pts[j]+tangent*width],[radii[j]+.025]*2,7)
    tube(P,'Separate-head-origin-long-sucking-beak',[(0,-32,7.3),(0,-38,5.4),(0,-46,4.2),(0,-53,4.5)],[.52,.45,.32,.075],9)
    objects=[g.finish() for g in groups.values()]
    zlow=min(v.co.z for o in objects for v in o.data.vertices)
    for o in objects:
        for v in o.data.vertices:v.co.z-=zlow
    root=bpy.data.objects[col['asset_root']]
    root['taxon']='Homoioptera vorhallensis; same-species living reconstruction'
    root['published_dimensions']='Wingspan approximately 200 mm; a preserved incomplete cercus exceeds 200 mm. Brauckmann et al. 2010, p. 28.'
    root['inferred_dimensions']='Body 85 mm estimated from Figure 2E 30 mm scale bar; each complete cercus chosen as 220 mm arc, not a fossil endpoint measurement.'
    root['artistic_choices']='Living thickness, earth-tone opaque membranes, posture, simplified venation and missing distal completion are interpretive.'
    root['sex']='Not asserted. No ovipositor or male claspers added.'
    root['specimen_identity']='Figure 2D-F catalog identity not verified; no holotype claim.'
    root['mount']='Floor at terminal claws; identity origin below thorax; model in meters.'
    return col,objects

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('.'));args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    p=json.loads((SOURCE/'params.json').read_text());out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    col,objects=build(p);scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
    with tempfile.TemporaryDirectory(prefix='homoioptera-export-') as temp:
        record=export_asset('homoioptera',{'en':'Homoioptera vorhallensis','zh':'沃尔哈勒同翅虫复原'},'invertebrates',col,metadata={'generator':'source/generate.py','surface_profile':'opaque-palette-only','representation':'living-reconstruction'},output_root=temp,render=False,max_triangles=40000,max_materials=6,max_primitives=8,diagnostics=False)
        built=Path(temp)/'homoioptera';shutil.copyfile(built/'homoioptera.glb',out/'model.glb');shutil.copyfile(built/'homoioptera.blend',out/'model.blend');qa=json.loads((built/'qa.json').read_text());qa['glb']['file']='model.glb'
    record['export_options']['filepath']='model.glb'
    report={'asset_id':'homoioptera','revision':'r001','glb_sha256':sha(out/'model.glb'),'source_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','generator_seed':p['seed'],'export_options':record['export_options'],'source':qa['source'],'glb':qa['glb'],'bounds_roundtrip_max_error_m':qa['bounds_roundtrip_max_error_m'],'anatomical_components':{o.name:list(o['component_names']) for o in objects},'units':'meters','authoring_forward':'-Y','glb_forward':'+Z','scope':'Source/export geometry evidence only; not independent review, GPU, scene, user or publication approval.'}
    write(out/'build-report.json',report);print('BUILD_COMPLETE',report['glb_sha256'],report['glb']['scene_triangles'])
if __name__=='__main__':main()
