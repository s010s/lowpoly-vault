#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original deterministic tree/deadwood assets, authored for lowpoly-vault.

Run: blender --background --threads 2 --python scripts/models/build_trees_deadwood.py -- [all|conifer-tree|lepidodendron|uprooted-log] [--draft|--no-render]
Generator code is MIT. Generated geometry, .blend files and previews are
CC-BY-4.0, attribution Leon Made This / s010s. No external assets are used.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys

import bpy
from mathutils import Vector

HERE=Path(__file__).resolve()
sys.path.insert(0,str(HERE.parents[1]))
import asset_common as ac

PALETTE={
    'fern_deep':'#294C43','fern_mid':'#47745C','fern_light':'#719366',
    'dry_olive':'#A1A276','bark_deep':'#4F443D','bark_mid':'#79624B',
    'cut_wood':'#B59B72','earth':'#8A715B','warm_stone':'#A89578',
    'stone_light':'#C7B798','cool_stone':'#6B7774','ochre':'#BD8B4D',
}
TAU=math.tau

def vec(x): return Vector(x)
def mix(a,b,t): return vec(a).lerp(vec(b),t)
def xy(angle): return Vector((math.cos(angle),math.sin(angle),0))

class MeshBuilder:
    """A semantic editable mesh, with deliberate closed components and colors."""
    def __init__(self,name,collection,materials):
        self.name=name; self.collection=collection; self.materials=materials
        self.vertices=[]; self.faces=[]; self.mi=[]
    def add(self,vertices,faces,material=0):
        offset=len(self.vertices)
        self.vertices.extend(tuple(v) for v in vertices)
        self.faces.extend(tuple(i+offset for i in f) for f in faces)
        self.mi.extend(material if isinstance(material,list) else [material]*len(faces))
    def finish(self):
        if not self.vertices: return None
        obj=ac.mesh_object(self.name,self.vertices,self.faces,self.materials,self.collection)
        for face,index in zip(obj.data.polygons,self.mi): face.material_index=index
        obj['construction']='Original profile-built geometry; intentional faceted surfaces'
        return obj

def frame(axis):
    axis=vec(axis).normalized()
    ref=Vector((0,0,1)) if abs(axis.z)<0.88 else Vector((0,1,0))
    u=axis.cross(ref).normalized(); v=axis.cross(u).normalized()
    return u,v

def tube(builder,points,radii,sides=7,material=0,cap_material=None,roll=0,ellipse=1.0,end_offsets=None):
    """Tapered closed loft. Every ring follows the actual growth direction."""
    ps=[vec(p) for p in points]; verts=[]
    for k,p in enumerate(ps):
        tangent=(ps[min(k+1,len(ps)-1)]-ps[max(k-1,0)]).normalized()
        u,v=frame(tangent)
        for j in range(sides):
            a=TAU*j/sides+roll
            rr=radii[k]*(1+0.035*math.cos(a*3+0.4))
            q=p+rr*(math.cos(a)*u+ellipse*math.sin(a)*v)
            if end_offsets is not None and k==len(ps)-1: q+=tangent*end_offsets[j]
            verts.append(q)
    faces=[tuple(reversed(range(sides)))]; mids=[material]
    for k in range(len(ps)-1):
        for j in range(sides):
            faces.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j)); mids.append(material)
    end_material=cap_material if cap_material is not None else material
    if end_offsets is None:
        faces.append(tuple((len(ps)-1)*sides+j for j in range(sides))); mids.append(end_material)
    else:
        tangent=(ps[-1]-ps[-2]).normalized()
        center_index=len(verts)
        verts.append(ps[-1]+tangent*(sum(end_offsets)/len(end_offsets)-.035))
        start=(len(ps)-1)*sides
        for j in range(sides): faces.append((start+j,start+(j+1)%sides,center_index)); mids.append(end_material)
    builder.add(verts,faces,mids)


def needle_spray(builder,base,axis,length,width,height,material=0):
    """Closed, pointed branch-tip mass, with three needle-like edge lobes.

    It is a designed outline loft, not a cone or a noisy sphere. A calm center
    ridge gives large readable planes, while the perimeter suggests needles.
    """
    origin=vec(base); d=vec(axis).normalized()
    side=d.cross(Vector((0,0,1)))
    if side.length<0.01: side=Vector((1,0,0))
    side.normalize(); up=side.cross(d).normalized()
    # Faceted, needle-covered shoot volumes. The cross section is a solid
    # diamond, not a flat broad leaf; the three long planes keep the crown calm.
    verts=[]
    for t,w,h,drift in [(0.,.17,.20,0.),(.35,1.,.94,.03),(.72,.73,.76,-.02)]:
        center=origin+d*(t*length)+side*(drift*width)+up*(height*.10*t)
        verts += [center+up*(h*height),center+side*(w*width),center-up*(h*height*.64),center-side*(w*width)]
    verts.append(origin+d*(length*1.09)+up*(height*.08))
    faces=[(3,2,1,0)]
    for k in range(2):
        for j in range(4): faces.append((k*4+j,k*4+(j+1)%4,(k+1)*4+(j+1)%4,(k+1)*4+j))
    for j in range(4): faces.append((8+j,8+(j+1)%4,12))
    builder.add(verts,faces,material)



def blade(builder,base,direction,length,width,bend=0.16,material=0,roll=0):
    """A solid narrow lanceolate microphyll: two sides, raised ridge, sharp tip."""
    p=vec(base); d=vec(direction).normalized(); u,v=frame(d)
    side=u*math.cos(roll)+v*math.sin(roll)
    normal=d.cross(side).normalized()
    m=p+d*(length*.43)+normal*bend
    tip=p+d*length+normal*(bend*.35)
    verts=[p,m-side*width*.5,m+normal*width*.18,m+side*width*.5,tip,m-normal*width*.10]
    faces=[(0,1,2),(0,2,3),(1,4,2),(2,4,3),(0,5,1),(0,3,5),(1,5,4),(5,3,4)]
    builder.add(verts,faces,material)


def leaf_cushion(builder,center,normal,width,height,depth,material=0):
    """Closed low relief diamond; regular helical positioning, no random noise."""
    c=vec(center); n=vec(normal).normalized(); h=Vector((0,0,1)); w=h.cross(n).normalized()
    p=[c+h*height*.5,c+w*width*.5,c-h*height*.5,c-w*width*.5,c+n*depth]
    builder.add(p,[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(3,2,1,0)],material)


def make_mats(keys): return [ac.make_material(key,PALETTE[key]) for key in keys]

def tree_metadata(slug,scientific,description,features,sources,notes):
    return {
        'description':description,
        'generator':'scripts/models/build_trees_deadwood.py',
        'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),
        'generator_license':'MIT','style':'original evidence-informed low-poly',
        'scientific_status':'evidence-informed stylized concept',
        'scientific_context':scientific,'identifying_features':features,
        'sources':sources,'artistic_choices':notes,
        'provenance':'Original geometry and palette-based materials authored procedurally in Blender. No downloaded models, textures, or reference images are included.',
        'license_components':{'geometry':'CC-BY-4.0','blend':'CC-BY-4.0','previews':'CC-BY-4.0','generator':'MIT'},
        'target_runtime':'Three.js 0.180.0; static opaque texture-free GLB',
        'topology_notes':'Closed solid component meshes with purposeful buried intersections at biological branch junctions. No transparent leaf cards. Flat shading; no random per-face colors.',
        'palette_reference':'skills/lowpoly-art-direction/references/first-batch.md',
        'reproducibility':{'deterministic':True,'random_geometry':False,'algorithm_revision':1},
    }


def build_conifer():
    slug='conifer-tree'; c=ac.setup_scene(slug,3101)
    mats=make_mats(['bark_mid','bark_deep','cut_wood','fern_deep','fern_mid','fern_light'])
    trunk=MeshBuilder('Conifer | tapered main axis',c,mats[:3])
    ps=[(0,0,.10),(.015,.005,.55),(-.025,.02,1.4),(.025,.015,2.4),(.045,.04,3.5),(.09,.02,4.6),(.15,.025,5.7),(.14,.04,6.65),(.13,.04,6.95)]
    tube(trunk,ps,[.31,.25,.216,.187,.159,.13,.095,.045,.009],sides=9,material=0,roll=.16)
    roots=MeshBuilder('Conifer | buttress roots',c,mats[:3])
    for i,(angle,length,height) in enumerate([(20,.72,.31),(103,.63,.25),(187,.79,.37),(262,.52,.23),(315,.56,.26)]):
        d=xy(math.radians(angle)); tube(roots,[(0,0,.23),d*.30+Vector((0,0,height*.55)),d*length+Vector((0,0,.045))],[.16,.12,.025],sides=6,material=0)
    branches=MeshBuilder('Conifer | lateral branch skeleton and old snags',c,mats[:3])
    # Tiers are deliberately uneven. Tier 1 has a missing forward branch,
    # opening a strong negative-space window that survives 128px silhouettes.
    whorls=[(2.45,1.45,[-8,68,158,249],.02),(3.45,1.65,[20,101,184,272],.10),(4.49,1.28,[-25,54,139,231],.02),(5.43,.97,[12,105,203,286],.06),(6.18,.66,[-32,64,166,257],.10)]
    for tier,(z,L,angles,lift) in enumerate(whorls):
        foliage=MeshBuilder(f'Conifer | foliage whorl {tier+1:02d}',c,mats[3:])
        center=Vector((.03+.025*tier,.025,z))
        for j,degrees in enumerate(angles):
            if tier==0 and j==0:
                d=xy(math.radians(degrees)); tube(branches,[center,center+d*.48+Vector((0,0,-.07)),center+d*.67+Vector((0,0,.04))],[.075,.042,.024],6,0,2,end_offsets=[0,.015,.035,.0,-.015,.02]); continue
            angle=math.radians(degrees); d=xy(angle); side=xy(angle+math.pi/2)
            # Fixed design variation favors the left rear silhouette.
            factor=[1.04,.91,1.09,.96][(j+tier)%4]; length=L*factor
            end=center+d*length+side*.06+Vector((0,0,.12+lift))
            pts=[center,center+d*length*.40+Vector((0,0,-.09)),center+d*length*.76+Vector((0,0,-.015)),end]
            tube(branches,pts,[.092-.01*tier,.062-.006*tier,.035,.013],sides=5,material=0)
            # Three different branchlet axes form a flat, deeply notched spray.
            for k,(fraction,yaw,sz) in enumerate([(.35,-.62,.89),(.49,.61,.90),(.69,0,1.13)]):
                attach=mix(pts[1],pts[-1],(fraction-.40)/.60)
                twig=xy(angle+yaw)*(.80 if k!=2 else 1.)+Vector((0,0,.17+.025*tier))
                leafy_length=(.52+.25*length)*sz
                needle_spray(foliage,attach,twig,leafy_length,.24+.055*length,.21+.010*tier,material=(1 if tier<3 else 2) if k==2 else (0 if tier<2 else 1))
        foliage.finish()
    # Fine upright leader maintains a continuous main-axis reading.
    crown=MeshBuilder('Conifer | upright leader shoots',c,mats[3:])
    for j,(a,z,l) in enumerate([(25,6.55,.48),(165,6.62,.43),(278,6.75,.35)]):
        needle_spray(crown,(.14,.035,z),xy(math.radians(a))*.25+Vector((0,0,.88)),l,.14,.12,2)
    # One lower broken branch gives scale without creating a second crown tier.
    tube(branches,[(0,0,1.62),(-.28,-.15,1.71),(-.44,-.18,1.79)],[.075,.04,.022],sides=5,material=1,cap_material=2)
    trunk.finish();roots.finish();branches.finish();crown.finish(); ac.ground_asset(c)
    metadata=tree_metadata(slug,
        {'period':'Jurassic–Cretaceous-inspired concept','themes':['mesozoic-forest','mesozoic-river-valley'],'taxon_scope':'Conifer architectural analogue; not an identified extinct or unchanged modern species'},
        {'en':'A seven-meter conifer concept with an exposed tapering axis, asymmetric lateral branch whorls, deeply notched foliage sprays and one deliberate crown gap.','zh':'约七米高的针叶乔木概念：渐细主干、错落轮生侧枝、分叉叶簇与一处清楚的树冠缺口。'},
        ['dominant tapering trunk','near-whorled lateral branches','open asymmetric crown tiers'],
        [{'url':'https://www.nhm.ac.uk/discover/how-to-grow-a-dinosaur-garden.html','supports':'Conifer context in Jurassic and Cretaceous vegetation; broad living analogue only'},{'url':'https://www.digitalatlasofancientlife.org/learn/embryophytes/tracheophytes/branching/','supports':'Lateral branching distinguished from apical dichotomies'}],
        ['Exact height, tier spacing, foliage clumping, colors and branch damage are original artistic choices, not fossil measurements.','Leaf masses summarize short conifer foliage without pretending to reproduce a named Araucaria species.'])
    return c,metadata,{'en':'Mesozoic conifer concept','zh':'针叶乔木'},'plants',2800


def build_lepidodendron():
    slug='lepidodendron'; c=ac.setup_scene(slug,3102)
    mats=make_mats(['bark_mid','bark_deep','fern_deep','fern_mid','fern_light'])
    trunk=MeshBuilder('Lepidodendron | columnar trunk',c,mats[:2])
    ps=[(0,0,.12),(0,0,.55),(.025,0,1.5),(.025,.02,2.6),(-.01,.025,3.7),(-.025,.04,4.7),(-.03,.045,5.18)]
    rs=[.43,.375,.34,.312,.284,.257,.244]
    tube(trunk,ps,rs,sides=10,material=1,roll=.08)
    # Shallow lycopsid rooting axes. This is not the seed-tree root plate used
    # by uprooted-log; no annual growth rings are added to this tree.
    root=MeshBuilder('Lepidodendron | shallow bifurcating root seat',c,mats[:2])
    for i,(angle,L) in enumerate([(15,1.10),(112,.93),(203,1.19),(294,1.02)]):
        d=xy(math.radians(angle)); side=xy(math.radians(angle)+math.pi/2)
        stem=[(0,0,.24),d*.43+Vector((0,0,.15)),d*.79+Vector((0,0,.07))]
        tube(root,stem,[.22,.15,.085],sides=6)
        for sign in [-1,1]: tube(root,[stem[-1],d*L+side*(.17*sign)+Vector((0,0,.035)),d*(L+.14)+side*(.30*sign)+Vector((0,0,.026))],[.087,.045,.013],sides=5)
    scars=MeshBuilder('Lepidodendron | helical diamond leaf cushions',c,mats[:2])
    # A controlled low-frequency helical lattice, large enough for a teaching
    # asset. Each diamond represents one leaf cushion, not reptilian scales.
    for row in range(11):
        z=.65+row*.38
        rr=.375-(z-.55)*.0275
        center=Vector((.02-.01*max(0,z-2),.006*z,z))
        for col in range(7):
            angle=TAU*col/7 + row*TAU/14 + .12
            normal=xy(angle)
            leaf_cushion(scars,center+normal*(rr*.965),normal,.18-.004*row,.32-.004*row,.035,0)
    branch=MeshBuilder('Lepidodendron | crown dichotomies',c,mats[:2])
    # Three successive apical forks create a high, wide candelabra crown.
    # Unequal lengths and a shallow depth offset avoid a flat heraldic fork.
    forks=[
      ((-.03,.045,5.05),(-.62,.06,5.86),(-.91,.10,6.39),.238,.14),
      ((-.03,.045,5.05),(.49,.05,5.84),(.76,.16,6.29),.238,.15),
      ((-.91,.10,6.34),(-1.22,-.34,6.78),(-1.40,-.48,7.13),.144,.082),
      ((-.91,.10,6.34),(-.86,.57,6.81),(-.72,.83,7.17),.144,.086),
      ((.76,.16,6.23),(.69,-.39,6.75),(.79,-.65,7.12),.150,.086),
      ((.76,.16,6.23),(1.15,.52,6.65),(1.38,.66,7.02),.150,.079),
    ]
    for index,(p,m,q,r1,r2) in enumerate(forks): tube(branch,[p,m,q],[r1,(r1+r2)*.54,r2],7,1 if index<2 else 0)
    bases=[vec(x[2]) for x in forks[2:]]
    ends=[]
    for i,b in enumerate(bases):
        directions=[Vector((-.42,-.14,.60)),Vector((.18,.31,.68))]
        if i in [1,3]: directions=[Vector((-.27,.20,.61)),Vector((.40,-.05,.58))]
        for j,d in enumerate(directions):
            q=b+d*(1-.06*i+.03*j)
            tube(branch,[b,b+d*.48,q],[.09,.061,.024],6,0)
            ends.append((b,q,i*2+j))
    foliage=MeshBuilder('Lepidodendron | narrow young-branch leaves',c,mats[2:])
    for b,q,index in ends:
        axis=(q-b).normalized(); u,v=frame(axis)
        # Leaves attach along the young shoot, not to a single palm crown.
        for k in range(13):
            t=.18+.062*k; t=min(t,.92)
            a=k*2.399963+index*.4
            radial=u*math.cos(a)+v*math.sin(a)
            direction=(axis*.82+radial*.80).normalized()
            ll=.74+.13*math.sin(k*.9+index*.7)
            if k>9: ll*=.80
            blade(foliage,mix(b,q,t)+radial*.035,direction,ll,.145,.060,0 if k<4 else 1 if k<10 else 2,roll=.3)
        # One growing tip ends each young shoot.
        blade(foliage,q,axis,.37,.065,.018,2)
    trunk.finish(); root.finish(); scars.finish(); branch.finish(); foliage.finish(); ac.ground_asset(c)
    metadata=tree_metadata(slug,
        {'period':'Late Carboniferous-inspired coal-swamp concept','themes':['carboniferous-wetland-forest'],'taxon_scope':'Lepidodendron-like arborescent lycopsid in a branching life stage; not a specimen or species reconstruction'},
        {'en':'A tall Carboniferous lycopsid concept with helical diamond leaf cushions, a high three-level dichotomous crown and narrow leaves on younger shoots.','zh':'石炭纪鳞木类概念：高柱状干保留螺旋菱形叶枕，高处三级二歧分枝，狭长叶着生于年轻枝条。'},
        ['columnar trunk with helical leaf cushions','high repeated apical dichotomies','narrow simple leaves on young crown axes'],
        [{'url':'https://www.digitalatlasofancientlife.org/learn/embryophytes/tracheophytes/leaves/','supports':'Diamond-shaped Lepidodendron leaf cushions and helical arrangement'},{'url':'https://www.digitalatlasofancientlife.org/learn/embryophytes/tracheophytes/branching/','supports':'Fossil Lepidodendron apical dichotomy; differs from lateral seed-plant branches'},{'url':'https://forces.si.edu/atmosphere/02_02_06.html','supports':'Carboniferous wetland context for giant lycopsids'}],
        ['The eight-meter display scale, exact fork angles, simplified leaf-cushion count, crown stage, green palette and root extent are artistic choices.','This asset belongs to a Carboniferous collection; do not present it as coexisting with Mesozoic dinosaur habitats.','Shallow visible root axes are simplified; subsurface stigmarian rootlets are omitted.'])
    return c,metadata,{'en':'Carboniferous lycopsid concept','zh':'石炭纪鳞木'},'plants',2900


def build_uprooted_log():
    slug='uprooted-log'; c=ac.setup_scene(slug,3103)
    mats=make_mats(['bark_mid','bark_deep','cut_wood','earth','dry_olive'])
    log=MeshBuilder('Deadwood | bent tapered trunk and ragged fracture',c,mats[:3])
    pts=[(-1.32,.02,.61),(-.89,-.015,.52),(-.28,.01,.42),(.46,.07,.34),(1.10,.15,.30),(1.68,.21,.34)]
    radii=[.40,.345,.30,.255,.221,.185]
    offsets=[.09,.18,.04,-.12,-.08,.03,.16,.25,.08]
    tube(log,pts,radii,9,0,2,roll=.16,ellipse=1.0,end_offsets=offsets)
    # Furrows are long, quiet facets, not a noise displacement on every vertex.
    bark=MeshBuilder('Deadwood | split bark ridges and peeled edge',c,mats[:3])
    for j,(a,scale) in enumerate([(2.0,1.),(3.5,.8),(5.3,.9)]):
        vs=[]; faces=[]
        for k in range(1,5):
            tangent=(vec(pts[min(k+1,5)])-vec(pts[k-1])).normalized(); u,v=frame(tangent)
            r=radii[k]*1.015; center=vec(pts[k])
            for aa,rr in [(a-.065,r),(a,r+.022*scale),(a+.065,r)]: vs.append(center+(math.cos(aa)*u+math.sin(aa)*v)*rr)
        for k in range(3): faces += [(k*3,k*3+1,(k+1)*3+1,(k+1)*3),(k*3+1,k*3+2,(k+1)*3+2,(k+1)*3+1)]
        # Closed underside hides inside the original trunk.
        faces += [(0,2,1),(9,10,11),(0,3,6,9,11,8,5,2)]
        bark.add(vs,faces,1)
    # Long irregular exposed wood strip on upper/near side.
    exposed=MeshBuilder('Deadwood | exposed inner wood strip',c,mats[:3])
    # Seat a narrow peeled patch directly on the actual circular loft surface.
    ring_info=[(1,4.80,4.98),(2,4.47,5.30),(3,4.45,5.27),(4,4.79,4.94)]
    vs=[]
    for k,a0,a1 in ring_info:
        tangent=(vec(pts[k+1])-vec(pts[k-1])).normalized(); u,v=frame(tangent)
        for a in [a0,(a0+a1)*.5,a1]:
            r=radii[k]*(1+.035*math.cos(a*3+.4))+.007
            vs.append(vec(pts[k])+(math.cos(a)*u+math.sin(a)*v)*r)
    faces=[]
    for k in range(3):
        faces.extend([(k*3,k*3+1,(k+1)*3+1,(k+1)*3),(k*3+1,k*3+2,(k+1)*3+2,(k+1)*3+1)])
    # Add buried underside and end caps so every component remains closed.
    faces.extend([(0,2,1),(9,10,11),(0,3,6,9,11,8,5,2)])
    exposed.add(vs,faces,2)
    # A few torn wood tongues extend the break and make the end non-sawn.
    tip=vec(pts[-1]); axis=(vec(pts[-1])-vec(pts[-2])).normalized(); u,v=frame(axis)
    for a,extra,ww in [(1.9,.32,.055),(4.5,.23,.040),(5.65,.38,.046)]:
        p=tip+(math.cos(a)*u+math.sin(a)*v)*.148
        blade(exposed,p,axis,.20+extra,ww,.006,2)
    branches=MeshBuilder('Deadwood | three naturally broken lateral branches',c,mats[:3])
    branch_specs=[([(-.65,0,.63),(-.76,-.12,.94),(-.69,-.20,1.13)],[.105,.075,.046],[-.015,.025,.01,.08,-.03,.035]),
                  ([(.10,-.10,.40),(.28,-.40,.49),(.46,-.61,.42)],[.101,.065,.038],[.02,.03,-.01,.025,.06,-.02]),
                  ([(.91,.18,.40),(1.04,.45,.60),(1.21,.57,.65)],[.078,.055,.031],[0,.03,.05,-.02,.01,.02])]
    for ps,rs,eo in branch_specs: tube(branches,ps,rs,6,0,2,end_offsets=eo)
    # A split on the largest stub retains branching history.
    tube(branches,[(-.76,-.12,.94),(-.94,-.09,1.02),(-1.01,-.11,1.09)],[.056,.035,.017],5,0,2,end_offsets=[0,.02,.01,.03,-.01])
    roots=MeshBuilder('Deadwood | asymmetric buttress and torn roots',c,mats[:3])
    root_paths=[
      ([(-1.13,.02,.58),(-1.49,-.16,.83),(-1.69,-.31,1.26),(-1.78,-.35,1.42)],[.23,.17,.097,.035]),
      ([(-1.25,.02,.62),(-1.58,.30,.97),(-1.75,.58,1.19),(-1.87,.63,1.34)],[.20,.145,.068,.024]),
      ([(-1.30,.015,.56),(-1.64,-.40,.50),(-1.83,-.77,.44),(-1.94,-.88,.27)],[.21,.135,.067,.025]),
      ([(-1.24,.035,.50),(-1.48,.43,.34),(-1.72,.77,.18),(-1.82,.92,.07)],[.18,.115,.062,.022]),
      ([(-1.28,.00,.50),(-1.48,-.16,.27),(-1.69,-.28,.10),(-1.92,-.23,.05)],[.18,.12,.055,.018]),
      ([(-1.31,.02,.67),(-1.66,.02,.87),(-1.92,.06,1.03)],[.19,.11,.04]),
    ]
    for i,(ps,rs) in enumerate(root_paths):
        tube(roots,ps,rs,6,0,2,roll=i*.2)
        p=vec(ps[-2]); q=vec(ps[-1]); d=(q-p).normalized()
        off=Vector((-.12,.20 if i%2==0 else -.17,.05 if i<3 else .03))
        tube(roots,[p,p+(q-p)*.35+off*.5,q+off],[rs[-2]*.75,.039,.012],5,0,2)
    # Adhering soil is a physical root plate, with a broken irregular outline.
    soil=MeshBuilder('Deadwood | attached fractured soil root plate',c,[mats[3],mats[1]])
    # Three adjoining but offset clods replace a uniform shield. The roots
    # cross in front; soil has a lower-frequency fractured outline behind.
    clods=[
        ([(-.47,.20),(-.73,.42),(-.61,.78),(-.26,.80),(-.04,.53),(-.15,.22)],-.17),
        ([(-.38,.73),(-.42,1.08),(-.16,1.28),(.18,1.16),(.31,.85),(.10,.66)],-.24),
        ([(.02,.22),(.43,.23),(.66,.49),(.53,.89),(.24,1.00),(.05,.67)],-.18),
    ]
    for yz,depth in clods:
        yy=sum(y for y,z in yz)/len(yz);zz=sum(z for y,z in yz)/len(yz)
        front=[(-1.59-.20*(z-.6)+depth,yy+(y-yy)*.69,zz+(z-zz)*.70) for y,z in yz]
        middle=[(-1.72-.20*(z-.6)+depth,y,z) for y,z in yz]
        back=[(-1.86-.20*(z-.6)+depth,yy+(y-yy)*.73,zz+(z-zz)*.72) for y,z in yz]
        n=len(yz); vs=front+middle+back
        faces=[tuple(range(n)),tuple(reversed(range(2*n,3*n)))]
        for row in range(2):
            for i in range(n): faces.append((row*n+i,(row+1)*n+i,(row+1)*n+(i+1)%n,row*n+(i+1)%n))
        soil.add(vs,faces,0)
    # Two small attached crumbs remain nested in the root plate, no display pad.
    for center,rx,ry,rz in [((-1.61,-.52,.42),.16,.17,.13),((-1.64,.44,.88),.12,.13,.16)]:
        p=vec(center); vs=[p+Vector((0,0,rz)),p-Vector((0,0,rz))]+[p+Vector((rx*math.cos(i*TAU/5),ry*math.sin(i*TAU/5),0)) for i in range(5)]
        faces=[]
        for i in range(5): faces.extend([(0,2+i,2+(i+1)%5),(1,2+(i+1)%5,2+i)])
        soil.add(vs,faces,0)
    for b in [log,bark,exposed,branches,roots,soil]: b.finish()
    ac.ground_asset(c,center_xy=True)
    metadata=tree_metadata(slug,
        {'period':'Mesozoic-inspired seed-plant deadwood concept','themes':['mesozoic-forest','mesozoic-river-valley'],'taxon_scope':'Seed plant/conifer structural concept; explicitly not a lycopsid uprooting reconstruction'},
        {'en':'A low fallen seed-tree trunk with a bent taper, ragged wood break, three snapped branches, an uneven root plate and adhering soil.','zh':'横向倒伏的种子植物枯木：主干弯曲收细、断口参差、三处折枝，偏心根盘附着土块。'},
        ['horizontal tapered bent trunk','hierarchical torn seed-tree roots and attached soil plate','ragged fracture and peeled bark'],
        [{'url':'https://www.nhm.ac.uk/discover/how-to-grow-a-dinosaur-garden.html','supports':'Fossil conifer wood and natural decay; broad prehistoric deadwood context'},{'url':'https://repository.si.edu/bitstreams/27b279ae-6030-4d71-93ba-1b0a713e7399/download','supports':'Referenced boundary against treating lycopsid uprooting as modern seed-tree root-plate behavior'}],
        ['Exact fall angle, diameter, root spread, soil fragments, snapped branches and colors are original prop design.','Exposed pale wood is a ragged break, not a modern saw cut.','No claim is made about a specific tree species, death event, fossil site or fungus.'])
    return c,metadata,{'en':'Uprooted seed-tree log','zh':'连根倒木'},'wood',1600

BUILDERS={'conifer-tree':build_conifer,'lepidodendron':build_lepidodendron,'uprooted-log':build_uprooted_log}

def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser()
    parser.add_argument('asset',nargs='?',default='all',choices=['all']+list(BUILDERS))
    parser.add_argument('--draft',action='store_true')
    parser.add_argument('--review',action='store_true',help='Full diagnostic set at 640px before shared final hero rendering')
    parser.add_argument('--preview-only',action='store_true',help='Open delivered blend and render without changing model files or official QA')
    parser.add_argument('--no-render',action='store_true')
    parser.add_argument('--output-root',type=Path,help='Alternate parent for deterministic verification builds')
    a=parser.parse_args(args)
    for slug in (BUILDERS if a.asset=='all' else [a.asset]):
        if a.preview_only:
            category='wood' if slug=='uprooted-log' else 'plants'
            output_dir=(a.output_root or ac.REPO_ROOT/'assets'/'prehistoric'/category)/slug
            bpy.ops.wm.open_mainfile(filepath=str(output_dir/f'{slug}.blend'))
            collection=bpy.data.collections['EXPORT']
            resolution=640 if a.review else 1024
            samples=16 if a.review else 32
            files=ac.render_previews(collection,output_dir,views=('hero','reversehero','front','side','rear','top'),resolution=resolution,samples=samples)
            files+=ac.render_diagnostics(collection,output_dir,resolution=resolution,samples=samples)
            qa_path=output_dir/'qa.json'; qa=json.loads(qa_path.read_text())
            qa['previews']={'status':'rendered_not_visually_reviewed','files':[Path(f).name for f in files],'engine':'Cycles CPU','resolution':resolution,'samples':samples,'view_transform':'Standard','look':'None','background_srgb':'#E8E4DC','stage':'diagnostic pass; final hero quality is recorded separately'}
            qa_path.write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
            print('PREVIEWS_COMPLETE',slug,flush=True)
            continue
        collection,metadata,title,category,budget=BUILDERS[slug]()
        record=ac.export_asset(slug,title,category,collection,metadata=metadata,
            output_root=a.output_root,
            views=('hero','reversehero') if a.draft else ('hero','reversehero','front','side','rear','top'),
            max_triangles=budget,max_materials=8,max_primitives=24,
            resolution=640 if (a.draft or a.review) else 1024,samples=16 if (a.draft or a.review) else 32,
            render=not a.no_render,diagnostics=not a.draft)
        output_dir=(a.output_root or ac.REPO_ROOT/'assets'/'prehistoric'/category)/slug
        parameters={
            'schema_version':1,'asset_id':slug,'recipe_revision':1,
            'generator':'scripts/models/build_trees_deadwood.py',
            'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),
            'generator_seed':bpy.context.scene.get('generator_seed'),
            'units':'meters','palette_srgb':{m['name']:m['srgb'] for m in record['materials']},
            'geometry_recipe':'All profile points, branch angles, radii, leaf placements and structural material groups are fixed in the named build function in the generator.',
            'design':{
                'conifer-tree':{'whorl_heights_m':[2.45,3.45,4.49,5.43,6.18],'whorl_branch_reaches_m':[1.45,1.65,1.28,.97,.66],'lower_crown_gap':'First low forward limb is broken; asymmetrical crown preserved','leaf_representation':'Solid elongated needle-bearing shoot volumes, never billboard cards'},
                'lepidodendron':{'trunk_first_fork_height_m':5.05,'apical_fork_levels':3,'young_terminal_axes':8,'leaf_cushion_helical_rows':11,'leaf_cushions_per_row':7,'leaves_per_young_axis':14},
                'uprooted-log':{'trunk_radii_m':[.40,.345,.30,.255,.221,.185],'large_root_axes':6,'secondary_root_branches':6,'snapped_lateral_branches':3,'attached_soil_clods':3,'construction':'Independent seed-plant deadwood recipe; not a rotated living-tree mesh'},
            }[slug],
            'actual_glb_bounds_size_m':record['dimensions'],
            'triangle_budget':budget,'actual_glb_triangles':record['triangles'],
            'license':'CC-BY-4.0','author':'Leon Made This / s010s',
        }
        (output_dir/'parameters.json').write_text(json.dumps(parameters,indent=2,ensure_ascii=False)+'\n')
        print('ASSET_COMPLETE',slug,flush=True)

if __name__=='__main__': main()
