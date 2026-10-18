# SPDX-License-Identifier: MIT
"""Original stylized Juracimbrophlebia and Asteroxylon static environment props.

Run in cloud Blender 4.3.2: blender -b -t 2 --python-exit-code 1 --python
scripts/models/build_small_insect_plant_pair.py -- --asset juracimbrophlebia
No external meshes, images, textures or palettes are incorporated.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
SCRIPT=Path(__file__).resolve(); REPO=SCRIPT.parents[2]
sys.path.insert(0,str(REPO/'scripts'))
import asset_common as C
SEED=20261017

class Mesh:
    def __init__(self): self.v=[]; self.f=[]; self.mi=[]
    def add(self,vs,fs,mi=0):
        n=len(self.v); self.v.extend(tuple(p) for p in vs); self.f.extend(tuple(n+i for i in f) for f in fs)
        self.mi.extend([mi]*len(fs) if isinstance(mi,int) else mi)
    def finish(self,name,mats,col):
        ob=C.mesh_object(name,self.v,self.f,mats,col)
        for p,i in zip(ob.data.polygons,self.mi):p.material_index=i
        return ob

def tube(mesh,points,radii,sides=6,mat=0,elliptic=1,phase=0):
    pts=list(map(Vector,points)); vs=[]
    for k,(p,r) in enumerate(zip(pts,radii)):
        t=(pts[min(k+1,len(pts)-1)]-pts[max(k-1,0)]).normalized()
        ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((0,1,0))
        u=t.cross(ref).normalized(); v=t.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides+phase; vs.append(p+r*(math.cos(a)*u+elliptic*math.sin(a)*v))
    fs=[tuple(reversed(range(sides)))]; mi=[mat if isinstance(mat,int) else mat[0]]
    for k in range(len(pts)-1):
        for j in range(sides):
            fs.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
            mi.append(mat if isinstance(mat,int) else mat[k])
    fs.append(tuple((len(pts)-1)*sides+j for j in range(sides))); mi.append(mi[-1])
    mesh.add(vs,fs,mi)

def blade(mesh,base,tip,width,fold,mat=0,normal=(0,0,1)):
    b,t=Vector(base),Vector(tip); d=t-b; n=Vector(normal).normalized()
    s=d.cross(n).normalized(); n=s.cross(d).normalized()
    vs=[b,b+d*.32+s*width,t,b+d*.32-s*width,b+d*.39+n*fold,b+d*.39-n*fold*.45]
    fs=[]
    for j in range(4):fs.extend([(j,(j+1)%4,4),((j+1)%4,j,5)])
    mesh.add(vs,fs,mat)

def ellipsoid(mesh,center,radii,mat=0,segments=8):
    c=Vector(center); vs=[]
    for z,w in [(-.88,.36),(-.5,.86),(0,1),(.5,.86),(.88,.36)]:
        for j in range(segments):
            a=2*math.pi*j/segments;vs.append(c+Vector((radii[0]*w*math.cos(a),radii[1]*w*math.sin(a),radii[2]*z)))
    fs=[tuple(reversed(range(segments)))]
    for k in range(4):
        for j in range(segments):fs.append((k*segments+j,k*segments+(j+1)%segments,(k+1)*segments+(j+1)%segments,(k+1)*segments+j))
    fs.append(tuple(4*segments+j for j in range(segments)));mesh.add(vs,fs,mat)

def insect():
    col=C.setup_scene('juracimbrophlebia',SEED)
    bodymat=C.make_material('body-moss','#596C40',.82)
    wingmat=C.make_material('wing-warm-ochre','#B7B578',.88)
    darkmat=C.make_material('veins-and-eyes','#45553C',.78)
    lightmat=C.make_material('wing-light-panels','#D1C58C',.88)
    body=Mesh(); legs=Mesh(); wings=Mesh(); veins=Mesh()
    # Profile-designed elongated abdomen with eight restrained segment boundaries.
    ys=[-.008,-.0065,-.004,-.0035,0,.0005,.004,.0045,.008,.0085,.012,.0125,.016,.0165,.019,.020,.022]
    rs=[.00145,.0018,.0018,.00155,.00175,.0015,.0017,.00148,.00163,.0014,.00155,.0013,.00142,.00115,.00122,.0009,.00048]
    tube(body,[(0,y,-.00025-.0008*max(0,y)/.022) for y in ys],rs,8,0,.78)
    tube(body,[(0,-.015,0),(0,-.0135,.00025),(0,-.011,.0004),(0,-.0085,0)], [.0012,.002,.0019,.0014],8,0,.85)
    ellipsoid(body,(0,-.0172,.00035),(.00135,.0019,.00115),0,8)
    # Eyes and conservative rostrum are distinct without oversized cartoon head.
    for s in (-1,1):ellipsoid(veins,(s*.00113,-.0175,.00065),(.00053,.0008,.00057),0,6)
    tube(veins,[(0,-.0183,.00005),(0,-.021,-.0014),(0,-.0221,-.0023)],[.00058,.00039,.00018],6)
    # Each of four leaf-like lobes is one elongated wing, not a lobed butterfly wing.
    for s in (-1,1):
        for fore in (True,False):
            b=Vector((s*.00145,-.0117 if fore else -.0089,.0010 if fore else .0006))
            axis=Vector((s*(.039 if fore else .021),.017 if fore else .035,.003 if fore else -.0010))
            side=Vector((-axis.y,axis.x,0)).normalized()
            if s<0:side=-side
            widths=[.00055,.0028,.0048,.0053,.0039,.00015]
            fractions=[0,.18,.43,.68,.86,1.]
            centers=[b+axis*t+Vector((0,0,math.sin(math.pi*t)*.00075)) for t in fractions]
            vs=[]
            for i,(c,w) in enumerate(zip(centers,widths)):
                vs.extend([c-side*w,c+Vector((0,0,.0003*math.sin(math.pi*fractions[i])+.00012)),c+side*w])
            fs=[];mi=[]
            # Two narrow planar ribbons meet at a soft longitudinal ridge.
            for k in range(5):
                fs.extend([(k*3,k*3+1,(k+1)*3+1,(k+1)*3),(k*3+1,k*3+2,(k+1)*3+2,(k+1)*3+1)])
                mi.extend([0,1 if k in (1,2,3) else 0])
            # Thin closed underside keeps correct winding and avoids alpha sorting.
            topn=len(vs);vs += [p-Vector((0,0,.00014)) for p in vs]
            fs += [tuple(topn+i for i in reversed(f)) for f in fs];mi += list(mi)
            boundary=[0,3,6,9,12,15,16,17,14,11,8,5,2,1]
            for i,j in zip(boundary,boundary[1:]+boundary[:1]):fs.append((i,j,j+topn,i+topn));mi.append(0)
            wings.add(vs,fs,mi)
            # Sparse original major veins, deliberately larger than fossil microsculpture.
            ridge=[c+Vector((0,0,.00047)) for c in centers]
            tube(veins,ridge,[.00013,.00013,.00012,.00011,.00010,.00008],4)
            for idx in (1,2,3,4):
                for sign in (-1,1):
                    end=centers[idx]+side*widths[idx]*.87*sign+Vector((0,0,.0002))
                    start=ridge[max(0,idx-1)]
                    tube(veins,[start,(start+end)*.5+Vector((0,0,.00008)),end],[.000095,.000085,.00007],4)
    # All six articulated legs attach to thorax; no abdomen-mounted appendages.
    endpoints=[((.005,-.022,-.002),(.011,-.036,-.003),(.009,-.040,-.002)),
               ((.010,-.015,-.003),(.021,-.025,-.007),(.023,-.028,-.006)),
               ((.009,.002,-.004),(.014,.018,-.009),(.012,.024,-.008))]
    for s in (-1,1):
        for i,parts in enumerate(endpoints):
            p=[(s*.0014,-.014+i*.0022,-.0004)]+[(s*x,y,z+(0 if s==1 else .0007)) for x,y,z in parts]
            tube(legs,p,[.00042,.00033,.00023,.00014],6)
            # Grasping distal tarsal curve: quiet, no invented extra joint count claim.
            q=Vector(p[-1]);tube(legs,[q,q+Vector((-s*.0007,.0013,.0005)),q+Vector((-s*.0014,.0010,.0008))],[.00014,.00013,.00010],5)
        tube(legs,[(s*.00065,-.0185,.0010),(s*.0022,-.024,.0018),(s*.0045,-.030,.0011),(s*.0048,-.034,.0003)],[.00020,.00016,.00012,.00008],5)
    body.finish('segmented-body-and-head',[bodymat],col)
    legs.finish('six-legs-and-two-antennae',[darkmat],col)
    wings.finish('four-elongated-wing-membranes',[wingmat,lightmat],col)
    veins.finish('eyes-rostrum-and-sparse-wing-veins',[darkmat],col)
    return col,{'body_length_m':.040,'wing_count':4,'leg_count':6,'antenna_count':2,'mount_origin':'body-center','palette_is_artistic':True,'closed_opaque_wings':True}

def plant():
    col=C.setup_scene('asteroxylon',SEED)
    stemmat=C.make_material('axes-jade','#477557',.9)
    leafmat=C.make_material('enations-sage','#7BA46B',.86)
    tipmat=C.make_material('young-enations-lime','#B1BC7E',.88)
    rootmat=C.make_material('rooting-axes-earth','#8A7156',.94)
    axes=Mesh(); leaves=Mesh(); bearing=Mesh(); roots=Mesh()
    # Plagiotropic leafy axis: one connected basal architecture with clear forks.
    basal=[(-.115,.025,.052),(-.073,.008,.058),(-.025,-.003,.054),(.018,.008,.058),(.063,.019,.051),(.108,.036,.055)]
    tube(axes,basal,[.0034,.0054,.0062,.0055,.0045,.0027],7)
    shoot_defs=[([(-.073,.008,.058),(-.080,.012,.110),(-.084,.025,.164),(-.073,.028,.213),(-.058,.022,.240)],.0042),
        ([(-.025,-.003,.054),(-.028,-.005,.121),(-.017,.002,.185),(-.021,.004,.247),(-.005,.008,.296)],.0050),
        ([(.018,.008,.058),(.039,-.009,.103),(.045,-.018,.150),(.037,-.020,.197),(.048,-.016,.231)],.0042),
        ([(.063,.019,.051),(.076,.025,.100),(.072,.038,.143),(.084,.041,.180)],.0037),
        ([(-.080,.012,.110),(-.111,-.004,.147),(-.124,-.011,.188),(-.116,-.006,.220)],.0028),
        ([(-.017,.002,.185),(.007,.036,.218),(.025,.047,.254)],.0027),
        ([(.045,-.018,.150),(.072,-.049,.177),(.081,-.052,.212)],.0025)]
    def leaf_axis(points,r,idx,step=.0055):
        ps=list(map(Vector,points));lens=[(b-a).length for a,b in zip(ps,ps[1:])];total=sum(lens)
        tube(axes,ps,[r*(1-.76*k/(len(ps)-1)) for k in range(len(ps))],6)
        count=max(5,int(total/step))
        for n in range(count):
            t=(n+.35)/count;dist=t*total; seg=0
            while seg<len(lens)-1 and dist>lens[seg]:dist-=lens[seg];seg+=1
            a,b=ps[seg],ps[seg+1];tangent=(b-a).normalized();p=a+(b-a)*(dist/lens[seg])
            # Small individual enations spiral around axes; no frond or pinna construction.
            angle=n*2.34+idx*.93
            normal=Vector((math.cos(angle),math.sin(angle),0));up=Vector((0,0,1))
            for half in (0,1,2):
                theta=angle+half*math.tau/3
                radial=Vector((math.cos(theta),math.sin(theta),0))
                length=(.016+.003*math.sin(n*1.7+idx))*(.66+.34*math.sin(math.pi*t))
                tip=p+radial*length+up*(length*(.25+.45*t))
                blade(leaves,p,tip,.0027*(1-.35*t),.00065,1 if t>.78 else 0,normal=tuple(radial.cross(up)))
    for i,(pts,r) in enumerate(shoot_defs):leaf_axis(pts,r,i)
    # Sparse basal leaves retain a leafy creeping axis without hiding attachment sites.
    for i in range(14):
        k=min(4,i//3);t=(i%3+.5)/3;p=Vector(basal[k]).lerp(Vector(basal[k+1]),t);sgn=(-1)**i
        blade(leaves,p,p+Vector((.002,sgn*.011,.005)),.0017,.0005,0,normal=(1,0,0))
    # Root-bearing axes descend from the plagiotropic/leafy system and fork anisotomously.
    attachments=[(-.073,.008,.058),(-.025,-.003,.054),(.018,.008,.058),(.063,.019,.051)]
    for i,a in enumerate(map(Vector,attachments)):
        b=a+Vector(((-1)**i*.009,-.012,.0))
        c=a+Vector(((-1)**i*.014,-.021,-.025))
        d=a+Vector(((-1)**i*.021,-.025,-.038))
        tube(bearing,[a,b,c,d],[.0028,.0025,.0018,.0012],6)
        blade(leaves,b,b+Vector(((-1)**i*.006,-.004,.003)),.0012,.00035,0,normal=(0,1,0))
        for j in (-1,1):
            e=d+Vector((j*.016,-.009,-.010))
            f=e+Vector((j*.011,-.010,-.004))
            tube(roots,[d,e,f],[.00105,.00072,.00032],5)
            for q in (-1,1):
                end=e+Vector((j*.006+q*.009,.008*q,-.009))
                tube(roots,[e,end],[.00063,.00027],5)
    axes.finish('connected-leafy-axes',[stemmat],col)
    leaves.finish('individual-simple-enations',[leafmat,tipmat],col)
    bearing.finish('descending-root-bearing-axes',[stemmat],col)
    roots.finish('branching-rooting-axes',[rootmat],col)
    C.ground_asset(col)
    # Frozen nominal whole-cluster height, preserving exact meter-scale coordinates.
    pts=C._vertices_world(col);low,high=C._bounds(pts);factor=.30/(high[2]-low[2])
    for ob in col.objects:
        if ob.type=='MESH':
            for v in ob.data.vertices:v.co*=factor
            ob.location*=factor
    return col,{'cluster_height_m':.30,'shoot_design_count':7,'axis_roles':['leafy shoots','root-bearing axes','rooting axes'],'mount_origin':'root-contact-center','palette_is_artistic':True,'complete_fossil_habit_claimed':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--asset',choices=['juracimbrophlebia','asteroxylon'],required=True);p.add_argument('--output-root',type=Path);p.add_argument('--brief-dir',type=Path);p.add_argument('--config',type=Path)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    col,params=(insect if a.asset=='juracimbrophlebia' else plant)()
    config=json.loads(a.config.read_text()) if a.config else {'asset':a.asset,'revision':'r1','seed':SEED}
    if config.get('asset')!=a.asset:raise ValueError('Config asset mismatch')
    category='animals' if a.asset=='juracimbrophlebia' else 'plants'
    outroot=a.output_root or REPO/'assets'/'prehistoric'/category
    out=outroot/a.asset;out.mkdir(parents=True,exist_ok=True)
    briefdir=a.brief_dir or REPO/'production'/'small-fauna-v1'/'pilot'/a.asset
    refs=json.loads((briefdir/'references.json').read_text()) if (briefdir/'references.json').exists() else {}
    inputs={}
    for name in ('brief.json','references.json','freeze.json'):
        src=briefdir/name
        if src.exists():
            data=src.read_bytes();(out/name).write_bytes(data);inputs[name]=hashlib.sha256(data).hexdigest()
    title={'en':'Juracimbrophlebia · leaf-wing hangingfly','zh':'叶翼悬蝇 · Juracimbrophlebia'} if a.asset=='juracimbrophlebia' else {'en':'Asteroxylon · branching ground plant','zh':'星木 · 分枝地被植物'}
    note='Original artistic interpretation for an imaginative children’s prehistoric world. Basic identifying forms are retained; colors, fine surface details, pose and incomplete parts are creative choices. Static prop, no rig or animation. Cross-period display is fantasy, not a coexistence claim.'
    metadata={'revision':config.get('revision','r1'),'taxon':'Juracimbrophlebia ginkgofolia' if category=='animals' else 'Asteroxylon mackiei','description':{'en':note,'zh':'面向儿童想象史前世界的原创艺术化静态道具。保留基本识别结构；颜色、细节、姿态与缺失部位为创作选择。无骨骼、无动画；跨时代组合不表示真实共存。'},'scientific_scope':'stylized-inspired environment prop; not a strict scientific reconstruction','generator':'scripts/models/'+SCRIPT.name,'generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'design_parameters':params,'config':config,'frozen_inputs_sha256':inputs,'sources':refs,'provenance':{'geometry':'original authored profile/loft meshes','textures':'none','palette':'original artistic colors','incorporated_third_party_content':False},'origin':params['mount_origin'],'tags':['static','environment-prop','small-fauna-v1','artistic-interpretation'],'modeling_runtime':'cloud Blender 4.3.2','intentional_overlaps':'Closed component joins occur inside connected axes/joints; no overlapping alpha surfaces.'}
    record=C.export_asset(a.asset,title,category,col,metadata=metadata,output_root=outroot,render=False,max_triangles=12000,max_materials=4,max_primitives=8)
    # The baseline helper supplies generic origin text; this prop records an explicit pivot.
    record['origin']=params['mount_origin'];(out/'metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    (out/'generator-config.json').write_text(json.dumps(config,indent=2)+'\n')
    (out/'LICENSE.txt').write_text('Assets and previews: CC BY 4.0. Attribution: Leon Made This / s010s.\nGenerator code: MIT.\nScientific sources consulted only; no reference artwork, meshes or textures incorporated.\n')
    print(json.dumps({'asset':a.asset,'triangles':record['triangles'],'bytes':record['glb_bytes'],'dimensions':record['dimensions'],'sha256':record['sha256']['glb']}))
if __name__=='__main__':main()
