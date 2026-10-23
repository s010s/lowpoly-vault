# SPDX-License-Identifier: MIT
"""Original genus-level female Stenodictya, anchored to published S. lobata.
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

WIDTH=[(0,3.2),(.07,9.5),(.17,15.4),(.28,17.5),(.43,17.4),(.60,15.8),(.70,12.7),(.82,8.5),(.91,5.4),(.97,3.0),(1,.35)]
def wing_point(side,kind,t,q):
    # q goes from leading -0.40 to trailing +0.60; nominal axis is 66 mm.
    hind=kind=='hind';angle=math.radians(20 if hind else -2);length=65 if hind else 66
    w=interp(t,WIDTH)*(1.10 if hind else 1);x0=4.3;y0=-3.1 if hind else -10.5
    along=length*t;across=q*w; x=x0+along*math.cos(angle)-across*math.sin(angle);y=y0+along*math.sin(angle)+across*math.cos(angle)
    z=10.0+(2.2 if hind else 5.0)*t+.65*math.sin(math.pi*t)*(1-(2*q-.2)**2)
    return (side*x,y,z)

def make_wing(mem,vein,side,kind):
    lab=('L' if side<0 else 'R')+'-'+kind
    ts=[t for t,_ in WIDTH];qs=[-.4,-.2,0,.2,.4,.6];rows=[[wing_point(side,kind,t,q) for q in qs] for t in ts]
    # Closed upper/lower grid, with finite cap at tip to avoid invalid triangles.
    nr,nc=len(rows),len(qs);top=[v for r in rows for v in r];verts=top+[(x,y,z-.09) for x,y,z in top];off=len(top);faces=[]
    for r in range(nr-1):
        for c in range(nc-1):
            a=r*nc+c;b=a+1;d=a+nc;e=d+1;faces.extend([(a,b,e,d),(a+off,d+off,e+off,b+off)])
    border=list(range(nc))+[r*nc+nc-1 for r in range(1,nr)]+list(range((nr-1)*nc+nc-2,(nr-1)*nc-1,-1))+[r*nc for r in range(nr-2,0,-1)]
    for j,a in enumerate(border):
        b=border[(j+1)%len(border)];faces.append((a,a+off,b+off,b))
    mem.add(lab+'-flight-wing',verts,faces)
    def raised(t,q):
        x,y,z=wing_point(side,kind,t,q);return(x,y,z+.09)
    for q,label in [(-.4,'costa'),(-.27,'subcosta'),(-.13,'radius'),(.04,'media-anterior'),(.23,'media-posterior'),(.40,'cubitus'),(.6,'trailing-margin')]:
        end=.64 if label=='subcosta' else .98
        tt=[t for t in ts if t<end]+[end]
        tube(vein,lab+'-'+label,[raised(t,q) for t in tt],[.12 if label in ('costa','radius') else .085]*len(tt),5)
    # Radius sector with five terminal branches, six simple anal veins.
    for i,end in enumerate([.48,.59,.70,.81,.94]):
        ts2=[.14,.27,(end+.27)/2,end];qq=[-.13,-.03,.15,.55]
        tube(vein,lab+f'-radial-branch-{i+1}',[raised(t,q) for t,q in zip(ts2,qq)],[.10,.095,.08,.065],5)
    for i,end in enumerate([.13,.18,.24,.31,.39,.47]):
        tube(vein,lab+f'-anal-vein-{i+1}',[raised(.015,.20),raised(end*.55,.40),raised(end,.59)],[.09,.08,.065],5)
    # Regular cross veins in leading areas, staggered reticulum posteriorly.
    for j in range(1,33):
        t=.035+j*.028
        for k,(q1,q2) in enumerate([(-.4,-.27),(-.27,-.13),(-.13,.04),(.04,.23),(.23,.40),(.40,.60)]):
            t2=min(.977,t+(.012 if (j+k)%2 else -.010))
            tube(vein,lab+f'-crossvein-{j:02d}-{k}',[raised(t,q1),raised(t2,q2)],[.047,.047],4)

def build(p):
    col=setup_scene('stenodictya',p['seed'])
    colors={'cuticle':'#8A5738','tergites':'#A26B40','wings':'#CEBF91','veins':'#71563A','appendages':'#725039','eyes':'#292C28'}
    mats={k:make_material('Stenodictya-'+k,v,roughness=.80 if k!='eyes' else .35) for k,v in colors.items()}
    groups={k:Parts(n,mats[k],col) for k,n in [('cuticle','Head-and-three-thoracic-segments'),('tergites','Abdomen-ten-overlapping-tergites'),('wings','Four-flight-wings-and-two-prothoracic-lobes'),('veins','Simplified-wing-venation-and-body-ridges'),('appendages','Six-legs-mouthparts-antennae-and-female-tail'),('eyes','Paired-eyes')]}
    C,A,W,V,P,E=[groups[k] for k in ['cuticle','tergites','wings','veins','appendages','eyes']]
    # Meso/metathorax have the published 7.8/7.2 mm lengths. Prothorax is estimated.
    loft(C,'Prothorax',[(-22.3,2.7,2.3,7.4),(-21.5,3.5,3.0,7.5),(-18.5,3.8,3.4,7.4),(-15.0,3.6,2.8,7.3)])
    loft(C,'Mesothorax',[(-15.0,3.6,2.7,7.3),(-14.3,4.5,3.8,7.2),(-10.4,4.8,4.0,7.0),(-7.2,4.6,3.6,7.0)])
    loft(C,'Metathorax',[(-7.2,4.4,3.5,7.0),(-6.5,4.7,3.8,7.0),(-2.0,4.8,3.7,6.8),(0,4.2,3.0,6.7)])
    loft(C,'Head-broad-clypeus',[(-23.8,2.7,1.9,7.6),(-23.4,3.5,2.1,7.6),(-22.7,3.5,2.3,7.7),(-22.3,2.6,1.8,7.6)],16)
    for side in [-1,1]:
        tube(E,('L' if side<0 else 'R')+'-eye',[(side*3.1,-23.3,7.5),(side*3.65,-23.1,7.8),(side*3.25,-22.8,8.1)],[.6,.85,.6],10)
    # Entire 39 mm abdominal envelope, with overlapping curved rear edges and
    # modest pointed posterolateral corners, not free gill plates.
    widths=[9.5,10.5,10.4,10.1,9.7,9.1,8.4,7.6,6.7,5.3]
    loft(C,'Abdominal-ventral-core',[(0,4.2,2.1,6.3),(8,4.6,2.4,6.0),(20,3.9,2.0,5.3),(31,2.8,1.5,4.7),(39,1.7,1.0,4.2)])
    for i,w in enumerate(widths):
        y=i*3.65;length=6.15 if i==9 else 4.65;length=min(length,39-y)
        nr=4;nc=13;rows=[]
        for t in [0,.28,.68,1]:
            row=[]
            for j in range(nc):
                u=-1+2*j/(nc-1);xx=u*w/2*(.94+.06*t)
                yy=y+t*length+(.50*abs(u)**8-.40*u*u)*t
                if i==9:yy=min(39,yy)
                z=6.2-.18*i+(2.4-.12*i)*(1-u*u)+.20*math.sin(math.pi*t)
                row.append((xx,yy,z))
            rows.append(row)
        top=[v for r in rows for v in r];off=len(top);verts=top+[(x,y,z-.65) for x,y,z in top];faces=[]
        for r in range(nr-1):
            for j in range(nc-1):
                a=r*nc+j;b=a+1;d=a+nc;e=d+1;faces.extend([(a,b,e,d),(a+off,d+off,e+off,b+off)])
        border=list(range(nc))+[r*nc+nc-1 for r in range(1,nr)]+list(range((nr-1)*nc+nc-2,(nr-1)*nc-1,-1))+[r*nc for r in range(nr-2,0,-1)]
        for j,a in enumerate(border):
            b=border[(j+1)%len(border)];faces.append((a,a+off,b+off,b))
        A.add(f'Tergite-{i+1:02d}',verts,faces)
        for s in [-1,1]:
            tube(V,f'Tergite-{i+1:02d}-oblique-ridge-{s}',[(s*w*.42,y+length*.89,6.2-.18*i+.55),(s*w*.28,y+length*.48,6.2-.18*i+1.75),(s*w*.14,y+length*.35,6.2-.18*i+2.18)],[.10,.13,.08],5)
    for side in [-1,1]:
        lab='L' if side<0 else 'R'
        make_wing(W,V,side,'fore');make_wing(W,V,side,'hind')
        outline2=[(4,-16.5),(4.7,-20.5),(6.2,-24.6),(9,-26.0),(12,-25.4),(14.8,-23.5),(15.1,-21.8),(14.2,-21.0),(15.0,-19.8),(13.8,-17.5),(10.5,-15.4),(7,-14.4),(4.5,-15.2)]
        outline=[(side*x,y,10.1+.045*(x-4)) for x,y in outline2];center=(side*8.1,-20.0,10.7)
        patch(W,lab+'-cordate-prothoracic-lobe',outline,center,.10)
        for j in range(7):
            end=outline[j+2];start=(side*4.2,-17.1,10.3);mid=tuple((a+b)/2 for a,b in zip(start,end))
            tube(V,lab+f'-lobe-fan-vein-{j+1}',[start,(mid[0],mid[1],mid[2]+.4),(end[0],end[1],end[2]+.10)],[.11,.10,.07],5)
        for t in [.28,.48,.68,.84]:
            arc=[]
            for end in outline[2:10]:arc.append((side*4.2+(end[0]-side*4.2)*t,-17.1+(end[1]+17.1)*t,10.6+.2*t))
            tube(V,lab+f'-lobe-cross-arc-{t}',arc,[.055]*len(arc),4)
        # Three articulated pairs, discrete five-part tarsi and paired claws.
        for i,(y,fy,fx) in enumerate([(-18.3,-29,12.4),(-10.5,-10.0,17),(-3.8,10,15.5)]):
            pts=[(side*3,y,5.2),(side*5.8,y-.3,4.6),(side*10.0,(y+fy)/2,5.6),(side*fx,fy,1.5)]
            tube(P,lab+f'-leg-{i+1}-coxa-femur-tibia',pts,[.68,.75,.60,.38],8)
            start=Vector(pts[-1]);direction=Vector((side*.27,(-.85 if i<2 else .85),-.32)).normalized()
            for j in range(5):
                a=start+direction*(j*.63);b=start+direction*((j+1)*.63)
                tube(P,lab+f'-leg-{i+1}-tarsus-{j+1}',[a,b],[.31-j*.035,.28-j*.035],6)
            end=start+direction*3.15
            for k in [-1,1]:
                tip=end+Vector((side*k*.40,(-.75 if i<2 else .75),-.30));tip.z=max(.08,tip.z)
                tube(P,lab+f'-leg-{i+1}-claw-{k}',[end,tip],[.16,.055],5)
        # Segmented antennae and long paired palps; no chewing mandibles.
        ap=[(side*1.8,-23.3,9),(side*2.2,-28,10),(side*4.5,-35,11),(side*7.0,-42,12)]
        tube(P,lab+'-antenna',ap,[.25,.22,.15,.055],7)
        pp=[(side*1.8,-23.6,6.7),(side*2.3,-28,5.6),(side*2.6,-33,5.7),(side*2.1,-37.2,6.0)]
        tube(P,lab+'-maxillary-palp-inferred-length',pp,[.29,.25,.19,.075],7)
        # Robust basal cerci taper progressively, long but never male pincers.
        pts=[];radii=[]
        for j in range(29):
            t=j/28;pts.append((side*(1.7+18*t+1.3*math.sin(math.pi*t)),38.8+67.3*t,4.7+1.2*t-.45*math.sin(math.pi*t)));radii.append(.65*(1-t)**1.15+.065)
        tube(P,lab+'-long-tapering-cercus-inferred-length',pts,radii,7)
        for j in range(1,21):
            t=j/28;pp=Vector(pts[j]);tangent=(Vector(pts[j+1])-Vector(pts[j-1])).normalized();r=radii[j]+.028
            tube(V,lab+f'-cercus-segment-ring-{j}',[pp-tangent*.075,pp+tangent*.075],[r,r],7)
    tube(P,'Separate-forward-downward-sucking-beak',[(0,-23.6,6.6),(0,-27.5,5.2),(0,-32.5,4.4),(0,-35,4.6)],[.48,.43,.32,.11],8)
    tube(P,'Female-curved-ovipositor-inferred-distal-completion',[(0,37.8,3.8),(0,41,3.4),(0,44.4,2.7),(0,47,2.9)],[.68,.61,.39,.11],8)
    objects=[g.finish() for g in groups.values()]
    # Preserve actual dimensions; floor mounting centered below thorax.
    zlow=min(v.co.z for o in objects for v in o.data.vertices)
    for o in objects:
        for v in o.data.vertices:v.co.z-=zlow
    root=bpy.data.objects[col['asset_root']]
    root['taxon']='Stenodictya sp.; genus-level female reconstruction anchored to S. lobata'
    root['published_dimensions']='Forewing 66 x 17.5 mm; abdomen 39 mm; mesothorax 7.8 mm; metathorax 7.2 mm; head 7 x 1.5 mm.'
    root['reconstruction_scope']='Kukalova 1970 genus composite; winglet outline, legs and beak use separately attributed congeners. Palps and ovipositor distal completion comparative, not measured lobata.'
    root['artistic_choices']='Depth, earth-tone opaque membranes, posture, vein simplification and full cercus length inferred.'
    root['sex']='Female, separate ovipositor, paired cerci, no male claspers.'
    root['mount']='Floor at terminal claws; origin below thorax, identity transform.'
    return col,objects

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('.'));args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    p=json.loads((SOURCE/'params.json').read_text());out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    col,objects=build(p);scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
    with tempfile.TemporaryDirectory(prefix='stenodictya-export-') as temp:
        record=export_asset('stenodictya',{'en':'Stenodictya, female genus reconstruction','zh':'狭网翅虫属雌性复原'},'invertebrates',col,metadata={'generator':'source/generate.py','surface_profile':'opaque-palette-only','representation':'living-reconstruction'},output_root=temp,render=False,max_triangles=40000,max_materials=6,max_primitives=8,diagnostics=False)
        built=Path(temp)/'stenodictya';shutil.copyfile(built/'stenodictya.glb',out/'model.glb');shutil.copyfile(built/'stenodictya.blend',out/'model.blend');qa=json.loads((built/'qa.json').read_text());qa['glb']['file']='model.glb'
    report={'asset_id':'stenodictya','revision':'r001','glb_sha256':sha(out/'model.glb'),'source_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','generator_seed':p['seed'],'export_options':record['export_options'],'source':qa['source'],'glb':qa['glb'],'bounds_roundtrip_max_error_m':qa['bounds_roundtrip_max_error_m'],'anatomical_components':{o.name:[n for n in o['component_names']] for o in objects},'units':'meters','authoring_forward':'-Y','glb_forward':'+Z','scope':'Source/export geometry evidence only; not independent review, GPU, scene, user or publication approval.'}
    write(out/'build-report.json',report);print('BUILD_COMPLETE',report['glb_sha256'],report['glb']['scene_triangles'])
if __name__=='__main__':main()
