# SPDX-License-Identifier: MIT
"""Original static Dapedium/Callichimaera props, frozen small-life batch A.

Run with Blender 4.3.2 -b -t 2 --python-exit-code 1 --python this.py --
  --asset dapedium --output-root /path/to/category
All coordinates are authored in meters, Z up and -Y forward. No reference
artwork or meshes are incorporated. Source parts retain named vertex groups.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from asset_common import setup_scene, make_material, mesh_object, export_asset


class Geometry:
    def __init__(self, name, mat):
        self.name, self.mat = name, mat
        self.vertices, self.faces, self.parts = [], [], []

    def add(self, name, vertices, faces):
        offset = len(self.vertices)
        self.vertices.extend(tuple(p) for p in vertices)
        self.faces.extend(tuple(offset+i for i in face) for face in faces)
        self.parts.append((name, list(range(offset, len(self.vertices)))))

    def object(self, collection):
        obj = mesh_object(self.name, self.vertices, self.faces, self.mat, collection)
        for name, indices in self.parts:
            obj.vertex_groups.new(name=name).add(indices, 1.0, 'REPLACE')
        obj['semantic_parts'] = json.dumps([p[0] for p in self.parts])
        return obj


def loft(group, name, sections, sides=16):
    """Designed y-axis cross sections: (y, xcenter, zcenter, halfwidth, halfheight)."""
    vertices, faces = [], []
    for y, x, z, rx, rz in sections:
        for k in range(sides):
            a = 2*math.pi*k/sides
            vertices.append((x+rx*math.cos(a), y, z+rz*math.sin(a)))
    for j in range(len(sections)-1):
        for k in range(sides):
            faces.append((j*sides+k, j*sides+(k+1)%sides,
                          (j+1)*sides+(k+1)%sides, (j+1)*sides+k))
    faces += [tuple(reversed(range(sides))),
              tuple((len(sections)-1)*sides+k for k in range(sides))]
    group.add(name, vertices, faces)


def oval(group, name, center, radius, rings=6, sides=12):
    cx, cy, cz = center
    rx, ry, rz = radius
    vertices = [(cx, cy, cz+rz)]
    for j in range(1, rings):
        a = math.pi*j/rings
        for k in range(sides):
            b = 2*math.pi*k/sides
            vertices.append((cx+rx*math.sin(a)*math.cos(b),
                             cy+ry*math.sin(a)*math.sin(b), cz+rz*math.cos(a)))
    bottom = len(vertices)
    vertices.append((cx, cy, cz-rz))
    faces = [(0,1+k,1+(k+1)%sides) for k in range(sides)]
    for j in range(rings-2):
        for k in range(sides):
            a = 1+j*sides+k
            b = 1+j*sides+(k+1)%sides
            faces.append((a,a+sides,b+sides,b))
    last = 1+(rings-2)*sides
    faces += [(last+k,bottom,last+(k+1)%sides) for k in range(sides)]
    group.add(name,vertices,faces)


def tube(group, name, path, radii, sides=7):
    vertices, faces = [], []
    for i, point in enumerate(path):
        p = Vector(point)
        tangent = Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])
        tangent.normalize()
        ref = Vector((0,0,1)) if abs(tangent.z)<0.9 else Vector((0,1,0))
        u = tangent.cross(ref).normalized()
        v = tangent.cross(u).normalized()
        for k in range(sides):
            a = 2*math.pi*k/sides
            vertices.append(p+radii[i]*(u*math.cos(a)+v*math.sin(a)))
    for j in range(len(path)-1):
        for k in range(sides):
            faces.append((j*sides+k,j*sides+(k+1)%sides,
                          (j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    faces += [tuple(reversed(range(sides))),tuple((len(path)-1)*sides+k for k in range(sides))]
    group.add(name,vertices,faces)


def plate(group, name, outline, normal, thickness):
    """Closed bevel-free thin plate with a slightly crowned, faceted surface."""
    n = Vector(normal).normalized()
    points = [Vector(p) for p in outline]
    center = sum(points,Vector())/len(points)
    count = len(points)
    vertices = [p-n*thickness/2 for p in points]+[p+n*thickness/2 for p in points]
    vertices += [center-n*thickness/2, center+n*thickness*0.9]
    faces = []
    for k in range(count):
        q=(k+1)%count
        faces += [(k,q,count+q,count+k),(2*count,k,q),
                  (2*count+1,count+q,count+k)]
    group.add(name,vertices,faces)


def dapedium(groups):
    body, scales, fins, eyes = groups
    sections=[(-.120,0,0,.006,.007),(-.112,0,.001,.013,.018),
              (-.099,0,.004,.020,.034),(-.078,0,.003,.024,.050),
              (-.050,0,.001,.026,.059),(-.019,.001,0,.025,.062),
              (.012,.003,0,.022,.057),(.039,.005,0,.017,.044),
              (.062,.006,0,.010,.027),(.080,.006,0,.005,.012),
              (.091,.007,0,.004,.010)]
    loft(body,'deep-oval-armored-body',sections,20)

    def skin(y, phi, side, lift=0):
        for a,b in zip(sections,sections[1:]):
            if a[0] <= y <= b[0]:
                t=(y-a[0])/(b[0]-a[0])
                vals=[a[i]*(1-t)+b[i]*t for i in range(1,5)]
                x,z,rx,rz=vals
                return (x+side*(rx*math.cos(phi)+lift),y,z+rz*math.sin(phi))
        raise ValueError(y)

    # Broad rhomboid scales follow the body surface, arranged in diagonal rows.
    for side in (-1,1):
        for row,phi in enumerate([-.91,-.59,-.29,0,.29,.59,.91]):
            for col in range(7):
                y=-.064+col*.017+(row%2)*.007
                if y>.058: continue
                dy=.0076
                dphi=.145
                points=[skin(y-dy,phi,side,.0006),skin(y,phi+dphi,side,.0006),
                        skin(y+dy,phi,side,.0006),skin(y,phi-dphi,side,.0006)]
                normal=(side*math.cos(phi),0,math.sin(phi))
                plate(scales,f'ordered-scale-{side}-{row}-{col}',points,normal,.0007)
        # A quiet opercular shield and short curved gill seam make the head legible.
        points=[skin(y,p,side,.0004) for y,p in [(-.086,.58),(-.068,.61),
                 (-.062,.12),(-.070,-.42),(-.088,-.44)]]
        plate(body,f'operculum-{side}',points,(side,0,0),.0011)
        seam=[skin(y,p,side,.0012) for y,p in [(-.066,.55),(-.062,.27),(-.063,-.04),(-.069,-.39)]]
        tube(fins,f'gill-seam-{side}',seam,[.0007]*4,5)
        oval(scales,f'eye-rim-{side}',(side*.0194,-.099,.018),(.0035,.0068,.0068),6,12)
        oval(eyes,f'eye-{side}',(side*.0217,-.100,.018),(.0023,.0048,.0048),6,12)
        oval(scales,f'eye-glint-{side}',(side*.02355,-.1013,.0197),(.0006,.00115,.00115),4,8)
        outline=[(side*.022,-.068,-.005),(side*.041,-.047,-.014),
                 (side*.054,-.008,-.025),(side*.034,-.014,-.030),
                 (side*.022,-.048,-.016)]
        plate(fins,f'pectoral-fin-{side}',outline,(0,0,1),.0015)
        tube(scales,f'pectoral-leading-ray-{side}',[outline[0],outline[1],outline[2]],[.0008,.00065,.00025],5)
        plate(fins,f'pelvic-fin-{side}',[(side*.011,.004,-.049),(side*.026,.022,-.070),
             (side*.016,.046,-.061),(side*.008,.032,-.040)],(0,0,1),.0012)
    # Dorsal, anal and caudal membranes are original closed low-poly fans.
    plate(fins,'dorsal-fin',[(.001,-.040,.056),(.001,-.023,.078),(.003,.006,.082),
          (.005,.034,.065),(.006,.061,.034),(.006,.071,.020),(.005,.040,.041),(.003,.008,.054)],(1,0,0),.0017)
    plate(fins,'anal-fin',[(.002,-.005,-.059),(.003,.014,-.077),(.005,.038,-.065),
          (.006,.068,-.026),(.005,.041,-.041)],(1,0,0),.0016)
    tail=[(.007,.081,.010),(.007,.103,.027),(.005,.128,.047),(.005,.130,.025),
          (.006,.118,.002),(.007,.130,-.034),(.007,.125,-.042),(.009,.100,-.020),(.007,.082,-.010)]
    plate(fins,'slightly-forked-tail',tail,(1,0,0),.0020)
    for i,(y,z) in enumerate([(.127,.041),(.128,.025),(.118,.002),(.128,-.032)]):
        tube(scales,f'caudal-ray-{i}',[(.009,.087,0),(.009,(.087+y)/2,z*.42),(.008,y,z)],
             [.00065,.0006,.0002],5)
    for i,(y,z) in enumerate([(-.022,.075),(.005,.078),(.031,.062),(.057,.035)]):
        tube(scales,f'dorsal-ray-{i}',[(.003,y-.010,max(.026,z-.024)),(.004,y,z)], [.00065,.00025],5)
    tube(eyes,'compact-mouth',[(-.005,-.1193,-.002),(0,-.1202,-.003),(.005,-.1193,-.002)],
         [.00075,.00075,.00075],6)


def callichimaera(groups):
    shell, cream, paddles, eyes=groups
    loft(shell,'elongate-fusiform-carapace',[
        (-.010,0,.0005,.0017,.0015),(-.008,0,.0005,.0038,.0026),
        (-.004,0,.0005,.0051,.0032),(.001,0,.0004,.0050,.0031),
        (.005,0,.0002,.0041,.0025),(.008,0,0,.0028,.0018),
        (.010,0,-.0001,.0013,.0009)],16)
    loft(cream,'ventral-sternal-crown',[
        (-.008,0,-.0017,.0015,.0005),(-.003,0,-.0020,.0038,.0006),
        (.003,0,-.0019,.0035,.0006),(.008,0,-.0012,.0016,.0005)],12)
    # Discrete shallow carapace ridges and exposed rear pleon, not a lobster tail.
    tube(cream,'dorsal-midline-ridge',[(0,-.008,.003),(0,-.003,.0038),(0,.003,.0034),(0,.007,.0023)],
         [.0002,.00028,.00024,.00012],6)
    for j in range(3):
        oval(shell,f'posterior-pleon-segment-{j}',(0,.009+j*.0009,-.0005-j*.0003),
             (.0021-j*.0003,.0007,.0007),4,10)
    for side in (-1,1):
        s=lambda x,y,z:(side*x,y,z)
        tube(shell,f'short-eye-peduncle-{side}',[s(.0023,-.008,.001),s(.0041,-.0105,.0016)],
             [.0008,.0008],8)
        oval(eyes,f'large-exposed-compound-eye-{side}',s(.0052,-.0112,.0020),(.00275,.0031,.00275),7,14)
        oval(cream,f'eye-light-facet-{side}',s(.0057,-.0123,.0041),(.0007,.00085,.0004),4,8)
        # Two short antennal pairs stay between the eyes.
        for j in range(2):
            tube(cream,f'short-antenna-{side}-{j}',[s(.00065+j*.0006,-.0095,.0009),
                 s(.0012+j*.0007,-.0125-j*.0008,.0012)], [.00018,.00010],5)
        # P1 is a paired compact claw below the eyes, with bent spanner fingers.
        tube(shell,f'P1-arm-{side}',[s(.0026,-.005,-.0017),s(.0062,-.007,-.0030),
             s(.0050,-.0100,-.0036)], [.00075,.0009,.00065],8)
        oval(shell,f'P1-manus-{side}',s(.0051,-.0113,-.0037),(.0011,.0016,.00075),5,10)
        tube(cream,f'P1-fixed-finger-{side}',[s(.0060,-.0120,-.0037),s(.0061,-.0135,-.0038),
             s(.0048,-.0139,-.0038)], [.00045,.00035,.00013],6)
        tube(shell,f'P1-moving-finger-{side}',[s(.0044,-.0118,-.0037),s(.0038,-.0130,-.0038),
             s(.0044,-.0135,-.0038)], [.00038,.00028,.00010],6)
        # P2 and P3 carry flattened oars, clearly different from posterior legs.
        for index,rooty,elbowy,tipy in [(2,-.003,-.0045,-.0060),(3,.0025,.0045,.0085)]:
            tube(shell,f'P{index}-proximal-leg-{side}',[s(.0037,rooty,-.0006),s(.0074,elbowy,-.0010),
                 s(.0100,elbowy+.0005,-.0009)], [.0007,.0009,.00085],8)
            outline=[s(.0090,elbowy-.0005,-.0008),s(.0115,tipy-.0018,-.0007),
                s(.0154,tipy-.0023,-.0006),s(.0170,tipy,-.0007),
                s(.0150,tipy+.0022,-.0009),s(.0114,elbowy+.0015,-.0010)]
            plate(paddles,f'P{index}-broad-oar-{side}',outline,(0,0,1),.0008)
            tube(cream,f'P{index}-oar-ridge-{side}',[s(.0098,elbowy,-.00025),s(.0133,tipy,-.0002),
                 s(.0162,tipy,-.00025)], [.00028,.00022,.00012],6)
        for index,rooty,elbowx,elbowy,tipx,tipy in [
             (4,.0055,.0088,.0095,.0108,.014),
             (5,.0076,.0058,.0120,.0067,.016)]:
            tube(shell,f'P{index}-reduced-slender-leg-{side}',[
                s(.0032,rooty,.0005),s(elbowx,elbowy,.0012),s(tipx,tipy,.0002)],
                [.00038,.00030,.00012],7)
        # Mouthparts are restrained small pediform appendages, without setae.
        tube(cream,f'pediform-mouthpart-{side}',[s(.0012,-.004,-.0025),s(.0014,-.008,-.0031),
             s(.0010,-.010,-.0025)], [.00035,.0003,.00016],6)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--asset',choices=['dapedium','callichimaera'],required=True)
    parser.add_argument('--output-root',type=Path)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    plan=ROOT/'production/small-fauna-v1/remaining-20'/args.asset
    config=json.loads((plan/'build-config.json').read_text())
    brief=json.loads((plan/'brief.json').read_text())
    collection=setup_scene(args.asset,config['seed'])
    bpy.context.scene.render.threads_mode='FIXED'
    bpy.context.scene.render.threads=2
    if args.asset=='dapedium':
        palette=[('bronze-body','#8D7961'),('armored-scale','#B5A184'),
                 ('blue-gray-fin','#68858B'),('dark-eye','#263D43')]
    else:
        palette=[('coral-shell','#BF8067'),('ochre-ridges','#D8B28A'),
                 ('muted-oar','#768E92'),('dark-compound-eye','#344B55')]
    groups=[Geometry(name,make_material(name,color,roughness=.72 if 'eye' in name else .88))
            for name,color in palette]
    globals()[args.asset](groups)
    for group in groups: group.object(collection)
    root=bpy.data.objects[collection['asset_root']]
    root['mounting_origin']='Body center for free-swimming static prop; not ground contact.'
    root['anatomical_forward']='-Y'
    category=brief['subject']['category']
    out=args.output_root or ROOT/'assets/small-fauna-v1'/category
    record=export_asset(args.asset,brief['display_name'],category,collection,
        output_root=out,collection_id='small-fauna-v1',render=False,
        max_triangles=brief['geometry_policy']['max_triangles'],max_materials=4,max_primitives=8,
        metadata={'quality_tier':'environment-prop','revision':'r1','static_only':True,
          'claim_scope':brief['claim_scope'],'description':brief['purpose'],
          'maker':{'model':'GPT-6 Astra','reasoning_effort':'xhigh','environment':'dot cloud Blender'},
          'source_plan_commit':'51a583295fcba6109117e01441ecf39354221b1b',
          'origin_detail':'Identity root at body center; suspended aquatic prop, no floor contact.',
          'surface_profile':'original palette-only; closed faceted geometry; no texture images',
          'generator':'scripts/models/build_small_fish_crab.py',
          'config':str(plan.relative_to(ROOT)/'build-config.json'),
          'sources':json.loads((plan/'references.json').read_text())['sources'],
          'artistic_choices':brief['artistic_choices'],
          'review_status':'candidate; independent visual/factual/specification/runtime review pending'})
    print(json.dumps({'asset':args.asset,'bytes':record['glb_bytes'],'triangles':record['triangles'],
                      'sha256':record['sha256']},indent=2))


if __name__=='__main__': main()
