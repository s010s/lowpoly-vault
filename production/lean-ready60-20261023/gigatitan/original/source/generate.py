# SPDX-License-Identifier: MIT
"""Original Gigatitan vulgaris reconstruction anchored to the selected holotype.
Run: blender -b -t 2 --python source/generate.py -- --output .
Only adjacent params.json and declared source/deps are generation inputs.
Modeling coordinates are millimeters, converted to meters at mesh creation.
"""
from pathlib import Path
import argparse,hashlib,json,math,shutil,sys,tempfile
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene,make_material,mesh_object,export_asset

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
class Parts:
    def __init__(self,name,mat,col):self.name,self.mat,self.col=name,mat,col;self.v=[];self.f=[];self.groups=[]
    def add(self,name,verts,faces):
        n=len(self.v);self.v.extend(tuple(v) for v in verts);self.f.extend(tuple(n+i for i in f) for f in faces);self.groups.append((name,list(range(n,len(self.v)))))
    def finish(self):
        o=mesh_object(self.name,[tuple(x*.001 for x in v) for v in self.v],self.f,self.mat,self.col)
        for name,indices in self.groups:o.vertex_groups.new(name=name).add(indices,1,'REPLACE')
        o['component_names']=[n for n,_ in self.groups];o['construction']='Original profile meshes. Joint overlaps and surface vein attachments intentional.'
        return o

def tube(group,name,points,radii,sides=8):
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
    verts=[];faces=[]
    for y,rx,rz,zc in rows:
        for j in range(n):
            a=2*math.pi*j/n;verts.append((rx*math.cos(a),y,zc+rz*math.sin(a)))
    faces.append(tuple(reversed(range(n))))
    for i in range(len(rows)-1):
        for j in range(n):
            a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
    faces.append(tuple((len(rows)-1)*n+j for j in range(n)));group.add(name,verts,faces)

def interp(t,rows):
    for (a,x),(b,y) in zip(rows,rows[1:]):
        if a<=t<=b:return x+(y-x)*(t-a)/(b-a)
    return rows[-1][1]

# Broad round-tipped planforms, with a modest hindwing anal field rather than a fan.
FORE=[(0,3.0),(.06,9.5),(.18,26),(.33,37),(.50,40),(.66,39),(.81,35),(.91,27),(.97,16),(.985,11.5),(.996,5.6),(1,.50)]
HIND=[(0,3),(.07,15),(.20,34),(.37,40),(.55,40),(.72,36),(.86,29),(.95,19),(.98,12),(.995,5.8),(1,.50)]
def wp(side,kind,t,q):
    hind=kind=='hind';width=interp(t,HIND if hind else FORE)
    x=5.3+(139.7 if hind else 149.7)*t
    # Forewing midline rises anteriorly; hindwing sits posteriorly with clear four-wing separation.
    cy=(-2+20*math.sin(math.pi*t*.78)) if hind else (-20-17*math.sin(math.pi*t*.74))
    y=cy+q*width
    z=15+(2 if hind else 5)*t+.8*math.sin(math.pi*t)*(1-4*q*q)
    return(side*x,y,z)

def wing(mem,veins,side,kind):
    lab=('L' if side<0 else 'R')+'-'+kind;ts=[t for t,_ in (HIND if kind=='hind' else FORE)];qs=[-.50,-.30,-.10,.10,.30,.50]
    top=[wp(side,kind,t,q) for t in ts for q in qs];off=len(top);verts=top+[(x,y,z-.12) for x,y,z in top];nr=len(ts);nc=len(qs);faces=[]
    for r in range(nr-1):
        for j in range(nc-1):
            a=r*nc+j;b=a+1;d=a+nc;e=d+1;faces.extend([(a,b,e,d),(a+off,d+off,e+off,b+off)])
    border=list(range(nc))+[r*nc+nc-1 for r in range(1,nr)]+list(range((nr-1)*nc+nc-2,(nr-1)*nc-1,-1))+[r*nc for r in range(nr-2,0,-1)]
    for j,a in enumerate(border):
        b=border[(j+1)%len(border)];faces.append((a,a+off,b+off,b))
    mem.add(lab+'-wing-membrane',verts,faces)
    def raised(t,q):
        x,y,z=wp(side,kind,t,q);return(x,y,z+.105)
    for q,name in [(-.5,'costa'),(-.35,'subcosta'),(-.21,'radius'),(-.04,'media'),(.15,'cubitus'),(.34,'anal'),(.5,'trailing-margin')]:
        end=.74 if name=='subcosta' else .99;tt=[t for t in ts if t<end]+[end]
        tube(veins,lab+'-'+name,[raised(t,q) for t in tt],[.19 if name in ('costa','radius') else .115]*len(tt),6)
    for i,end in enumerate([.45,.57,.69,.81,.95]):
        tt=[.12,.28,(end+.28)/2,end];qq=[-.21,-.12,.10,.46]
        tube(veins,lab+f'-radius-sector-branch-{i+1}',[raised(t,q) for t,q in zip(tt,qq)],[.16,.14,.12,.09],5)
    # Reduced hindwing anal sector is bounded within the same narrow wing envelope.
    for i,end in enumerate([.13,.20,.29,.38]):
        tube(veins,lab+f'-small-anal-field-vein-{i+1}',[raised(.02,.12),raised(end*.55,.34),raised(end,.49)],[.14,.11,.08],5)
    # Irregular net-like cross veins, not a fabricated sound-file organ.
    cols=[-.50,-.35,-.21,-.04,.15,.34,.50];count=28 if kind=='fore' else 23
    for j in range(1,count+1):
        t=.035+j*.91/(count+1)
        for k,(q1,q2) in enumerate(zip(cols,cols[1:])):
            shift=.009*math.sin(j*2.1+k*1.7);t2=max(.035,min(.977,t+shift))
            tube(veins,lab+f'-net-crossvein-{j:02d}-{k}',[raised(t,q1),raised((t+t2)/2+.003,(q1+q2)/2),raised(t2,q2)],[.063,.063,.063],4)

def build(p):
    col=setup_scene('gigatitan',p['seed'])
    colors={'cuticle':'#716746','tergites':'#96825A','membrane':'#D1C49C','veins':'#776747','appendages':'#655A3D','eyes':'#272E2A'}
    mats={k:make_material('Gigatitan-'+k,v,roughness=.85 if k!='eyes' else .30) for k,v in colors.items()}
    groups={k:Parts(n,mats[k],col) for k,n in [('cuticle','Head-and-three-thoracic-segments'),('tergites','Segmented-abdominal-tergites'),('membrane','Four-rounded-wing-membranes'),('veins','Simplified-longitudinal-and-net-veins'),('appendages','Six-legs-antennae-mouthparts-and-cerci'),('eyes','Paired-compound-eyes')]}
    C,A,W,V,P,E=[groups[k] for k in ['cuticle','tergites','membrane','veins','appendages','eyes']]
    # Body extent exactly 97.62 mm, independent of antennae and paired terminal cerci.
    loft(C,'Head-capsule',[(-42.62,2.0,2.2,14),(-41.0,4.4,3.9,14),(-37.8,5.2,4.8,14),(-34.8,4.2,4.0,14),(-33.5,3.3,3.2,14)])
    loft(C,'Prothorax',[(-33.5,3.3,3.2,13.5),(-32.5,4.5,4.3,13.5),(-29.0,4.8,4.4,13.5),(-25.2,4.2,3.9,13.4)])
    loft(C,'Mesothorax',[(-25.2,4.2,3.8,13),(-23,5.5,4.7,13),(-18,6.165,5,13),(-12.5,5.7,4.5,12.8)])
    loft(C,'Metathorax',[(-12.5,5.7,4.4,12.8),(-10.5,6.0,4.8,12.8),(-5.0,5.8,4.5,12.5),(0,5.0,3.7,12)])
    loft(C,'Abdomen-ventral-core',[(0,4.9,3.2,11.5),(12,5.9,3.5,11),(27,5.2,3.2,10.4),(42,3.8,2.3,10),(52,1.9,1.5,9.8),(55,.6,.65,9.5)])
    # Ten original overlapping shallow segment shells, tapering distinctly behind the wing roots.
    widths=[10.4,11.5,12.0,11.8,11.4,10.5,9.3,7.8,5.8,3.6]
    for i,w in enumerate(widths):
        y=i*5.1;end=min(55,y+6.2);rx=w/2;zc=11.8-.23*i;rz=3.7-.20*i
        loft(A,f'Abdominal-tergite-{i+1:02d}',[(y,rx*.90,rz*.87,zc),(y+.9,rx,rz,zc),(end-.7,rx*.96,rz*.95,zc-.15),(end,rx*.84,rz*.84,zc-.3)],16)
    for s in [-1,1]:
        lab='L' if s<0 else 'R'
        tube(E,lab+'-compound-eye',[(s*4.4,-39.6,14.2),(s*5.45,-38.2,14.9),(s*4.8,-36.6,15)],[1.0,1.35,.9],12)
        wing(W,V,s,'fore');wing(W,V,s,'hind')
        # Strongly developed femur and opposing slender tibia; pose follows Fig. 6c, not a long mantis neck.
        tube(P,lab+'-foreleg-coxa',[(s*3.8,-30,11),(s*8.7,-31.2,11.5)],[1.4,1.75],10)
        f0=Vector((s*8.7,-31.2,11.5));f1=Vector((s*34,-44.5,17.5))
        tube(P,lab+'-foreleg-enlarged-femur',[f0,f0.lerp(f1,.18),f0.lerp(f1,.65),f1],[1.45,2.45,2.1,1.15],10)
        t0=f1;t1=Vector((s*34.7,-69,20))
        tube(P,lab+'-foreleg-folded-tibia',[t0,t0.lerp(t1,.50),t1],[1.12,.89,.50],8)
        for j in range(10):
            t=.15+j*.074;a=f0.lerp(f1,t);a.y-=1.2;a.z+=.55;b=a+Vector((-s*.45,-(2.4+1.3*math.sin(j)),.35))
            tube(P,lab+f'-fore-femur-grasping-spine-{j+1:02d}',[a,b],[.40,.045],6)
        for j in range(9):
            t=.12+j*.086;a=t0.lerp(t1,t);a.x-=s*.64;b=a+Vector((-s*1.50,.45,-.10))
            tube(P,lab+f'-fore-tibia-tooth-{j+1:02d}',[a,b],[.23,.04],5)
        leg_ends=[(1,t1,Vector((s*.62,-.78,-.03)))]
        for n,y,knee,ankle in [(2,-18,(s*33,-21,10),(s*48,-48,2.4)),(3,-4,(s*34,15,10),(s*35,45,2.4))]:
            c=(s*4.8,y,10);tr=(s*8.2,y+1.4,10.4)
            tube(P,lab+f'-walking-leg-{n}-coxa',[c,tr],[1.0,1.05],8)
            tube(P,lab+f'-walking-leg-{n}-femur',[tr,tuple(Vector(tr).lerp(Vector(knee),.45)),knee],[.95,1.25,.80],8)
            tube(P,lab+f'-walking-leg-{n}-tibia',[knee,ankle],[.72,.40],8)
            for j in range(7):
                a=Vector(knee).lerp(Vector(ankle),.18+j*.10);b=a+Vector((s*.8,0,.15));tube(P,lab+f'-walking-leg-{n}-small-seta-{j}',[a,b],[.14,.025],5)
            leg_ends.append((n,Vector(ankle),Vector((s*.32,-.85 if n==2 else .85,-.36)).normalized()))
        for n,start,direction in leg_ends:
            direction=direction.normalized()
            for j in range(5):
                a=start+direction*j*1.15;b=start+direction*(j+1)*1.15
                tube(P,lab+f'-leg-{n}-tarsus-{j+1}',[a,b],[.39-j*.045,.36-j*.045],6)
            end=start+direction*5.75
            for k in [-1,1]:
                tip=end+Vector((s*k*.60,-.85 if n!=3 else .85,-.24));tip.z=max(.06,tip.z)
                tube(P,lab+f'-leg-{n}-claw-{k}',[end,tip],[.18,.035],5)
        # Long fine antennae completed conservatively; thickness and exact length are inferred.
        ap=[(s*2.7,-41,17.2),(s*7,-48,19.2),(s*18,-56,21),(s*38,-62,22),(s*65,-65,23),(s*94,-66,23.5),(s*117,-66.5,24)]
        tube(P,lab+'-antenna-inferred',ap,[.42,.36,.29,.22,.16,.11,.045],7)
        tube(P,lab+'-mandible-inferred',[(s*2.6,-41.5,11.8),(s*3.5,-45,11.2),(s*1.1,-46,11.8)],[.90,.70,.09],8)
        tube(P,lab+'-short-maxillary-palp-inferred',[(s*3.5,-41.5,11),(s*5.5,-44,10.5),(s*4.8,-48,10.4)],[.30,.23,.065],7)
        tube(P,lab+'-short-terminal-cercus-inferred',[(s*.8,54,9.3),(s*3.5,59,9),(s*4.4,63,8.8)],[.38,.22,.055],7)
    objects=[g.finish() for g in groups.values()]
    zlow=min(v.co.z for o in objects for v in o.data.vertices)
    for o in objects:
        for v in o.data.vertices:v.co.z-=zlow
    root=bpy.data.objects[col['asset_root']]
    root['taxon']='Gigatitan vulgaris';root['body_length_m']=p['body_length'];root['thorax_width_m']=p['thorax_width']
    root['scale_evidence']='Body 97.62 mm and thorax 12.33 mm directly annotated on selected holotype in Schubnel et al. 2021 Fig. 6a; approx. 310 mm spread inferred from Fig. 6c scale bar.'
    root['uncertainty']='Antennae, appendage endings, body thickness, colors and pose are reconstructed. No assertion of proven active flight or stridulation.'
    root['anatomy']='Three leg pairs including spined grasping forelegs; two pairs of broad rounded wings with small hindwing anal field; short paired cerci.'
    root['mount']='Floor at walking-leg claws; root at projected thoracic center. Identity transform.'
    return col,objects

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('.'));a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    p=json.loads((SOURCE/'params.json').read_text());out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    col,objects=build(p);scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
    with tempfile.TemporaryDirectory(prefix='gigatitan-export-') as tmp:
        record=export_asset('gigatitan',{'en':'Gigatitan vulgaris','zh':'巨翅虫'},'invertebrates',col,metadata={'generator':'source/generate.py','surface_profile':'opaque-palette-only','representation':'living-reconstruction'},output_root=tmp,render=False,max_triangles=40000,max_materials=6,max_primitives=8,diagnostics=False)
        built=Path(tmp)/'gigatitan';shutil.copyfile(built/'gigatitan.glb',out/'model.glb');shutil.copyfile(built/'gigatitan.blend',out/'model.blend');qa=json.loads((built/'qa.json').read_text());qa['glb']['file']='model.glb'
    report={'asset_id':'gigatitan','revision':'r001','glb_sha256':sha(out/'model.glb'),'source_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','generator_seed':p['seed'],'export_options':record['export_options'],'source':qa['source'],'glb':qa['glb'],'bounds_roundtrip_max_error_m':qa['bounds_roundtrip_max_error_m'],'anatomical_components':{o.name:list(o['component_names']) for o in objects},'units':'meters','authoring_forward':'-Y','glb_forward':'+Z','scope':'Source/export geometry evidence only; not independent review, GPU, scene, user or publication approval.'}
    write(out/'build-report.json',report);print('BUILD_COMPLETE',report['glb_sha256'],report['glb']['scene_triangles'])
if __name__=='__main__':main()
