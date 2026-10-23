# SPDX-License-Identifier: MIT
"""Original Sphecoptera brongniarti living interpretation, specimen MNHN.F.R51337.
Run: blender -b -t 2 --python source/generate.py -- --output .
Only adjacent params.json and declared source/deps are generation inputs.
Profile coordinates below are millimeters; mesh coordinates are meters.
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
    def __init__(self,name,mats,col):self.name,self.mats,self.col=name,mats,col;self.v=[];self.f=[];self.mi=[];self.groups=[]
    def add(self,name,verts,faces,material=0):
        n=len(self.v);self.v.extend(tuple(v) for v in verts);self.f.extend(tuple(n+i for i in f) for f in faces);self.mi.extend(material if isinstance(material,list) else [material]*len(faces));self.groups.append((name,list(range(n,len(self.v)))))
    def finish(self):
        o=mesh_object(self.name,[tuple(x*.001 for x in v) for v in self.v],self.f,self.mats,self.col)
        for poly,mi in zip(o.data.polygons,self.mi):poly.material_index=mi
        for name,indices in self.groups:o.vertex_groups.new(name=name).add(indices,1,'REPLACE')
        o['component_names']=[n for n,_ in self.groups];o['construction']='Original profile surfaces. Closed parts; deliberate overlaps at joints, abdominal segments and vein roots.'
        return o

def tube(group,name,points,radii,sides=7):
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

def loft(group,name,rows,n=16,accent=False):
    # y, width radius, depth radius, vertical center. Finite end rings.
    verts=[];faces=[];mi=[]
    for y,rx,rz,zc in rows:
        for j in range(n):
            a=2*math.pi*j/n;verts.append((rx*math.cos(a),y,zc+rz*math.sin(a)))
    faces.append(tuple(reversed(range(n))));mi.append(0)
    for i in range(len(rows)-1):
        for j in range(n):
            a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n));mi.append(1 if accent and i==len(rows)-2 and 0<=j<n//2 else 0)
    faces.append(tuple((len(rows)-1)*n+j for j in range(n)));mi.append(0);group.add(name,verts,faces,mi)

def interp(t,items):
    for (a,x),(b,y) in zip(items,items[1:]):
        if a<=t<=b:return x+(y-x)*(t-a)/(b-a)
    return items[-1][1]
WIDTH=[(0,.65),(.06,.75),(.15,1.1),(.25,1.95),(.34,3.5),(.45,6.0),(.57,8.4),(.70,10.1),(.80,10.9),(.88,9.9),(.94,7.4),(.975,4.3),(.995,1.8),(1,.35)]
def wing_point(side,kind,t,q):
    hind=kind=='hind';angle=math.radians(21 if hind else -4);length=47.3 if hind else 48.4
    w=interp(t,WIDTH)*(.97 if hind else 1);along=length*t;across=q*w
    x=1.6+along*math.cos(angle)-across*math.sin(angle);y=(-1.5 if hind else -6.0)+along*math.sin(angle)+across*math.cos(angle)
    z=5.7+(1.35 if hind else 2.0)*t+.34*math.sin(math.pi*t)*(1-(2*q-.15)**2)
    return(side*x,y,z)

def make_wing(mem,vein,side,kind):
    label=('L' if side<0 else 'R')+'-'+kind
    ts=sorted(set([round(i/40,6) for i in range(41)]+[t for t,_ in WIDTH]));qs=[-.43,-.32,-.20,-.08,.05,.18,.31,.44,.57]
    nr,nc=len(ts),len(qs);top=[wing_point(side,kind,t,q) for t in ts for q in qs];off=len(top);verts=top+[(x,y,z-.075) for x,y,z in top];faces=[];mi=[]
    def pattern(t,q):
        # Broad irregular alternating patches, not a claim of exact vein/cell counts or living hue.
        tt=t+.027*math.sin(11*q+(0.55 if kind=='hind' else 0))+.018*q
        dark=any(a<=tt<=b for a,b in [(.28,.37),(.43,.53),(.60,.70),(.77,.87),(.93,.99)])
        if q<-.29 and t<.73:dark=False
        if q>.28 and .50<t<.61:dark=True
        if q>.13 and .82<t<.87:dark=False
        return int(dark)
    for r in range(nr-1):
        for c in range(nc-1):
            a=r*nc+c;b=a+1;d=a+nc;e=d+1;m=pattern((ts[r]+ts[r+1])/2,(qs[c]+qs[c+1])/2)
            faces.extend([(a,b,e,d),(a+off,d+off,e+off,b+off)]);mi.extend([m,m])
    border=list(range(nc))+[r*nc+nc-1 for r in range(1,nr)]+list(range((nr-1)*nc+nc-2,(nr-1)*nc-1,-1))+[r*nc for r in range(nr-2,0,-1)]
    for j,a in enumerate(border):
        b=border[(j+1)%len(border)];faces.append((a,a+off,b+off,b));mi.append(pattern(ts[a//nc],qs[a%nc]))
    mem.add(label+'-long-petiolate-flight-wing',verts,faces,mi)
    def raised(t,q):
        x,y,z=wing_point(side,kind,t,q);return(x,y,z+.055)
    for q,tag in [(-.43,'leading-margin'),(-.23,'longitudinal-a'),(-.04,'longitudinal-b'),(.20,'longitudinal-c'),(.57,'trailing-margin')]:
        tt=[0,.12,.25,.38,.50,.62,.74,.84,.92,.97,.99]
        tube(vein,label+'-'+tag,[raised(t,q) for t in tt],[.07 if 'margin' in tag else .052]*len(tt),5)
    for i,(start,end) in enumerate([(.33,.63),(.48,.78),(.65,.91)]):
        tube(vein,label+f'-sparse-branch-{i+1}',[raised(start,-.04),raised((start+end)/2,.16),raised(end,.53)],[.055,.047,.040],5)
    for i,t in enumerate([.30,.43,.57,.70,.82,.92]):
        tube(vein,label+f'-sparse-cross-connection-{i+1}',[raised(t,-.23),raised(t+.018,.20),raised(t+.012,.50)],[.041,.041,.041],4)

def build(p):
    col=setup_scene('sphecoptera',p['seed'])
    colors={'cuticle':'#74634C','segment_edges':'#99876A','membrane':'#BDB395','patches':'#77745F','veins':'#8C7C5E','eyes':'#30352E'}
    mats={k:make_material('Sphecoptera-'+k,v,roughness=.82 if k!='eyes' else .42) for k,v in colors.items()}
    groups=[Parts('Head-thorax-and-ten-abdominal-segments',[mats['cuticle'],mats['segment_edges']],col),Parts('Four-patterned-petiolate-wings',[mats['membrane'],mats['patches']],col),Parts('Sparse-interpretive-wing-veins',mats['veins'],col),Parts('Six-walking-legs-and-paired-appendages',mats['cuticle'],col),Parts('Paired-modest-eyes',mats['eyes'],col)]
    B,W,V,A,E=groups
    loft(B,'Small-head',[(-11,.42,.58,4.7),(-10.65,1.18,.88,4.8),(-9.7,1.38,1.05,4.9),(-8.55,.95,.88,4.9),(-8.3,.72,.72,4.8)])
    loft(B,'Prothorax',[(-8.6,.78,.8,4.6),(-8.15,1.2,1.3,4.6),(-7.15,1.38,1.45,4.6),(-6.7,1.15,1.3,4.6)],accent=True)
    loft(B,'Mesothorax',[(-6.8,1.18,1.35,4.55),(-6.35,1.7,1.8,4.5),(-4.6,1.85,2.0,4.5),(-3.8,1.6,1.6,4.5)],accent=True)
    loft(B,'Metathorax',[(-3.9,1.6,1.6,4.45),(-3.25,1.8,1.9,4.45),(-1.1,1.65,1.65,4.4),(.15,1.5,1.45,4.35)],accent=True)
    # Slender continuous segmented abdomen; no wasp waist or thick odonate cylinder.
    for i in range(10):
        a=i*2.7;b=(i+1)*2.7;rx=1.56-.078*i if i<7 else [1.01,.78,.53][i-7];rz=1.30-.075*i;zc=4.3-.055*i
        loft(B,f'Abdominal-segment-{i+1:02d}',[(a-.12 if i else a,rx*.94,rz*.96,zc),(a+.40,rx,rz,zc),(b-.22,rx*.96,rz*.95,zc),(b,rx*.88,rz*.86,zc)],accent=True)
    for side in [-1,1]:
        lab='L' if side<0 else 'R'
        tube(E,lab+'-eye',[(side*1.09,-10.40,5.0),(side*1.48,-10.0,5.17),(side*1.16,-9.56,5.25)],[.35,.47,.32],10)
        make_wing(W,V,side,'fore');make_wing(W,V,side,'hind')
        for i,(rooty,elbowy,footy,footx) in enumerate([(-7.4,-10.0,-13.0,6.7),(-5.1,-3.3,-1.0,9.0),(-1.6,2.6,7.2,8.2)]):
            pts=[(side*.94,rooty,3.55),(side*2.4,rooty-.3,3.0),(side*4.8,elbowy,3.2),(side*footx,footy,1.1)]
            tube(A,lab+f'-walking-leg-{i+1}-coxa-femur-tibia-inferred',pts,[.28,.31,.24,.15],7)
            end=Vector(pts[-1]);dy=-1 if i==0 else 1;start=end
            for j in range(3):
                nxt=start+Vector((side*.27,dy*.52,-.18));tube(A,lab+f'-walking-leg-{i+1}-tarsal-unit-{j+1}-inferred',[start,nxt],[.13-j*.023,.115-j*.023],6);start=nxt
            tube(A,lab+f'-walking-leg-{i+1}-terminal-claw-inferred',[start,start+Vector((side*.15,dy*.28,-.1))],[.07,.043],5)
        tube(A,lab+'-short-antenna-inferred',[(side*.63,-10.55,5.42),(side*.94,-12.25,5.8),(side*1.65,-14.8,6.0)],[.13,.10,.045],7)
        # Each 35 mm length includes inferred missing-end completion, not a measured fossil value.
        points=[];radii=[]
        for j in range(29):
            t=j/28;points.append((side*(.41+3.25*t+.6*math.sin(math.pi*t)),26.8+34.82*t,4.1+.36*t-.28*math.sin(math.pi*t)));radii.append(.21*(1-t)**1.05+.043)
        tube(A,lab+'-long-cercus-inferred-tip-completion',points,radii,7)
    tube(A,'Small-ventral-sucking-rostrum-inferred',[(0,-10.25,4.0),(0,-11.25,3.2),(0,-12.3,2.8)],[.23,.16,.06],7)
    objects=[g.finish() for g in groups]
    # Museum mount: origin at floor below thorax. All numerical geometry remains real scale.
    low=min(v.co.z for o in objects for v in o.data.vertices)
    for o in objects:
        for v in o.data.vertices:v.co.z-=low
    root=bpy.data.objects[col['asset_root']]
    root['taxon']='Sphecoptera brongniarti Meunier, 1908';root['reference_specimen']='MNHN.F.R51337 incomplete lectotype'
    root['body_length_image_estimate_m']=p['body_length_estimate'];root['wingspan_image_estimate_m']=p['wingspan_estimate'];root['cerci_length_inferred_m']=p['cerci_length_inferred']
    root['scientific_scope']='Interpretive living restoration. Body 38 mm and wingspan about 100 mm are centimeter-ruler photographic estimates with about 15 percent uncertainty. Cerci 35 mm include missing-end completion.'
    root['inferred_features']='Depth, three walking-leg pairs, short antennae, small ventral rostrum and endpoint completions. Hues and sex unknown. No third tail, no prothoracic winglets, no species mixing.'
    root['pattern_scope']='Original low-contrast interpretation of alternating fossil wing patches. Sparse veins are not diagnostic vein counts.'
    root['mount']='Floor contact of hanging legs, origin below thorax; head -Y, abdomen +Y, dorsal +Z.'
    return col,objects

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('.'));args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    p=json.loads((SOURCE/'params.json').read_text());out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);col,objects=build(p)
    scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
    with tempfile.TemporaryDirectory(prefix='sphecoptera-export-') as temp:
        record=export_asset('sphecoptera',{'en':'Sphecoptera brongniarti','zh':'柄翅古网翅虫复原'},'invertebrates',col,metadata={'generator':'source/generate.py','surface_profile':'opaque-palette-only','representation':'living-reconstruction'},output_root=temp,render=False,max_triangles=40000,max_materials=6,max_primitives=8,diagnostics=False)
        built=Path(temp)/'sphecoptera';shutil.copyfile(built/'sphecoptera.glb',out/'model.glb');shutil.copyfile(built/'sphecoptera.blend',out/'model.blend');qa=json.loads((built/'qa.json').read_text());qa['glb']['file']='model.glb'
    report={'asset_id':'sphecoptera','revision':'r001','glb_sha256':sha(out/'model.glb'),'source_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','generator_seed':p['seed'],'export_options':record['export_options'],'source':qa['source'],'glb':qa['glb'],'bounds_roundtrip_max_error_m':qa['bounds_roundtrip_max_error_m'],'anatomical_components':{o.name:list(o['component_names']) for o in objects},'units':'meters','authoring_forward':'-Y','glb_forward':'+Z','scope':'Source/export geometry evidence only; not independent review, GPU, scene, user or publication approval.'}
    write(out/'build-report.json',report);print('BUILD_COMPLETE',report['glb_sha256'],report['glb']['scene_triangles'])
if __name__=='__main__':main()
