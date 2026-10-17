#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original conifer structure study. Blender 4.3.2, bounded cloud execution.
Uses the repository export/QA helper; never writes original asset directories.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve()
REPO=next(p for p in HERE.parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
import asset_common as ac
TAU=math.tau

def v(p): return Vector(p)
def radial(a): return Vector((math.cos(a),math.sin(a),0))
def frame(d):
    d=v(d).normalized(); q=Vector((0,0,1)) if abs(d.z)<.9 else Vector((0,1,0))
    u=d.cross(q).normalized(); return u,d.cross(u).normalized()

class Mesh:
    def __init__(self,name,collection,mats):
        self.name=name; self.collection=collection; self.mats=mats
        self.verts=[];self.faces=[];self.mi=[]; self.parts=[]
    def add(self,verts,faces,mat=0,label=None):
        n=len(self.verts); self.verts.extend(tuple(p) for p in verts)
        self.faces.extend(tuple(n+i for i in f) for f in faces)
        self.mi.extend([mat]*len(faces) if isinstance(mat,int) else mat)
        if label:self.parts.append((label,n,len(self.verts)))
    def finish(self):
        obj=ac.mesh_object(self.name,self.verts,self.faces,self.mats,self.collection)
        for f,mi in zip(obj.data.polygons,self.mi):f.material_index=mi
        for label,a,b in self.parts:
            obj.vertex_groups.new(name=label).add(list(range(a,b)),1,'REPLACE')
        return obj

def tube(mesh,points,radii,sides=7,mat=0,label=None):
    points=[v(p) for p in points]; verts=[]
    # Transport a stable frame to avoid twist seams near directional changes.
    for k,p in enumerate(points):
        d=(points[min(k+1,len(points)-1)]-points[max(k-1,0)]).normalized();u,w=frame(d)
        for j in range(sides):
            a=TAU*j/sides+.18
            verts.append(p+radii[k]*(u*math.cos(a)+w*math.sin(a)))
    faces=[tuple(reversed(range(sides)))]
    for k in range(len(points)-1):
        for j in range(sides):faces.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
    faces.append(tuple((len(points)-1)*sides+j for j in range(sides)))
    mesh.add(verts,faces,mat,label)

def needle(mesh,p,d,length,width,mat):
    # A narrow solid, curved-looking awl. Four faces and a triangular base;
    # no broad lamina, alpha card or radial clump anchored to one point.
    p=v(p);d=v(d).normalized();u,w=frame(d)
    verts=[p-u*width*.5,p+u*width*.5,p+w*width*.52,p+d*length+w*length*.08]
    mesh.add(verts,[(0,2,1),(0,1,3),(1,2,3),(2,0,3)],mat)

def curved_finger(mesh, points, radii, tip, material):
    """A narrow solid shoot with meaningful bends and a small curved termination."""
    pts=[v(p) for p in points];verts=[];sides=3
    for k,p in enumerate(pts):
        before=pts[max(0,k-1)];after=pts[k+1] if k+1<len(pts) else v(tip)
        axis=(after-before).normalized();u,w=frame(axis)
        for j in range(sides):
            angle=TAU*j/sides+.35
            verts.append(p+radii[k]*(u*math.cos(angle)+w*math.sin(angle)))
    apex=len(verts);verts.append(v(tip));faces=[(2,1,0)]
    for k in range(len(pts)-1):
        for j in range(sides):faces.append((k*3+j,k*3+(j+1)%3,(k+1)*3+(j+1)%3,(k+1)*3+j))
    for j in range(sides):faces.append(((len(pts)-1)*3+j,(len(pts)-1)*3+(j+1)%3,apex))
    mesh.add(verts,faces,material)

def clustered_spray(mesh, sp, width, material, label):
    """Three elongated, unequal curved lobes following a shared branchlet axis.
    A compound is one aggregated needle-bearing shoot, with tapered attachments.
    """
    start=len(mesh.verts);width*=.40
    curved_finger(mesh,[sp(t) for t in [0,.42,.82]],[.007,width,width*.45],sp(1.10),material)
    span=(sp(1)-sp(0)).length
    for k,(t,side_sign,fraction) in enumerate([(.18,-1,.56),(.51,1,.40)]):
        p=sp(t);axis=(sp(t+.04)-sp(t-.04)).normalized();u,w=frame(axis)
        # Side fingers are close to the branchlet axis, with a small upcurved
        # termination. They cannot become isolated vertical sails or spears.
        direction=(axis+u*side_sign*(.65 if k==0 else .46)+v((0,0,.05))).normalized()
        p+=u*side_sign*width*.50
        length=max(.10,span*fraction)
        def fp(x):return p+direction*length*x+v((0,0,.010*x*x))
        rr=width*(.68 if k==0 else .54)
        curved_finger(mesh,[fp(x) for x in [0,.40,.78]],[.006,rr,rr*.58],fp(1),material)
    mesh.parts.append((label,start,len(mesh.verts)))

def axis(z):
    return Vector((.045*math.sin(z*.75),.025*math.sin(z*.51),z))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--config',type=Path,default=HERE.with_name('clustered-config.json'))
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    config=json.loads(args.config.read_text());out=args.output_dir.resolve()
    if out.exists() and any(out.iterdir()):raise RuntimeError('Attempt output must be empty')
    out.mkdir(parents=True,exist_ok=True)
    collection=ac.setup_scene('conifer-tree',config['seed'])
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    mats=[ac.make_material(name,color,roughness=.92) for name,color in config['palette'].items()]
    wood=Mesh('Conifer | editable woody axis boughs and collars',collection,mats[:1])
    bough=wood
    foliage=Mesh('Conifer | clustered narrow needle-bearing shoots',collection,mats[1:])
    zs=[0,.16,.48,1.1,1.9,2.65,3.4,4.2,5,5.8,6.45,6.9,7.03]
    rs=[.34,.28,.235,.205,.178,.155,.133,.112,.088,.061,.036,.016,.004]
    tube(wood,[axis(z) for z in zs],rs,10,0,'main-leader')
    for i,(a,L) in enumerate([(12,.63),(88,.54),(158,.68),(239,.50),(303,.57)]):
        d=radial(math.radians(a)); tube(wood,[axis(.26)-d*.05,d*.24+v((0,0,.13)),d*L+v((0,0,.035))],[.17,.105,.025],7,0,f'root-{i}')
    tiers=config['tiers']; shoot_count=0; needle_count=0; branch_count=0
    for tier,row in enumerate(tiers):
        z,L,angles=row['height'],row['length'],row['angles']
        for j,degrees in enumerate(angles):
            a=math.radians(degrees);d=radial(a);side=radial(a+math.pi/2)
            length=L*[1.02,.91,1.07,.96,1.04][(j+tier)%5]
            if tier==0 and j==1:length=.40
            start=axis(z+.065*math.sin(j*1.9+tier)); thickness=.078-.008*tier
            droop=.20 if tier<2 else .13 if tier<4 else .05
            def bp(t):return start+d*(length*t)+side*(.07*math.sin(t*math.pi)*(1 if j%2 else -1))+v((0,0,-droop*math.sin(t*math.pi)+(.10+.035*tier)*t*t))
            pts=[bp(t) for t in [0,.10,.26,.48,.73,1]]
            tube(bough,pts,[thickness*1.55,thickness*1.25,thickness*.84,thickness*.59,thickness*.33,.009],8,0,f'tier{tier+1}-bough{j+1}')
            branch_count+=1
            # A broken lower branch leaves a causal opening in the crown.
            if tier==0 and j==1:continue
            pairs=3 if tier<2 else 2
            for k in range(pairs*2+1):
                terminal=(k==pairs*2)
                t=.21+k*(.68/(pairs*2)) if not terminal else .90
                sign=-1 if k%2 else 1
                # Alternating attachments spread along the bough, never a starburst.
                attachment=bp(t)
                direction=(d*(.64 if not terminal else 1)+side*(sign*.77 if not terminal else .06)).normalized()
                shoot_len=length*(.28+.10*math.sin(math.pi*t))*(1-.42*t)
                if terminal:shoot_len=length*.33
                shoot_len*=config['shoot_length_multiplier']
                shoot_len=max(shoot_len,.19)
                def sp(s):return attachment+direction*(shoot_len*s)+d*(.035*s*s)+v((0,0,-.08*math.sin(math.pi*s)+(.08+.018*tier)*s*s))
                width=(.072 if tier<4 else .056)*config['spray_width_multiplier']
                clustered_spray(foliage,sp,width,0 if tier<4 else 1,f'tier{tier+1}-bough{j+1}-shoot{k+1}')
                shoot_count+=1
                needle_count+=3
            # Fine needles continue the main bough tips, avoiding bare spear ends.
    # Seven slender leader shoots preserve a continuous tapering top.
    for i,(z,degrees,ll) in enumerate([(6.46,22,.28),(6.52,135,.25),(6.60,255,.23),(6.67,68,.20),(6.73,185,.17),(6.80,300,.14),(6.88,30,.13)]):
        d=(radial(math.radians(degrees))*.34+v((0,0,.93))).normalized()
        p=axis(z)
        def leader_sp(t,p=p,d=d,ll=ll):return p+d*ll*t
        clustered_spray(foliage,leader_sp,.034*(1-i*.06),1,f'leader-shoot-{i}')
        shoot_count+=1;needle_count+=3
    # Two short dead snags; upper one aligns with a missing lower crown bough.
    for i,(z,a,L) in enumerate([(1.31,210,.30),(1.77,52,.37)]):
        d=radial(math.radians(a));tube(bough,[axis(z),axis(z)+d*L*.55+v((0,0,.07)),axis(z)+d*L+v((0,0,.11))],[.065,.040,.016],7,0,f'old-snag-{i}')
    wood.finish();foliage.finish();ac.ground_asset(collection)
    metadata={'description':{'en':'An original seven-meter conifer concept with open crown gaps, curved tapering boughs, alternating narrow, clustered needle-bearing shoots.','zh':'七米针叶乔木概念：开放冠隙、弯曲渐细枝条、错列细枝及沿轴分布的针状叶。'},'generator':str(HERE.relative_to(REPO)),'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'seed':config['seed'],'scientific_status':'evidence-informed stylized conifer architectural concept; not an identified extinct species','artistic_choices':['Seven-meter scale, crown spacing, small asymmetry and color are original design choices.','Each elongated compound spray represents an aggregated needle-bearing branchlet; its three elongated lobes represent groups of needles, not separate measured leaves.','Tubular bough bases flare into and are buried within the parent trunk; intentional closed-component intersections.'],'profile':'static opaque palette-only; no textures','license_components':{'geometry':'CC-BY-4.0','blend':'CC-BY-4.0','generator':'MIT'},'provenance':'Original procedural geometry. References consulted only; no external mesh or image incorporated.','semantic_counts':{'boughs':branch_count,'branchlets':shoot_count,'aggregated_shoot_components':needle_count},'source_vertex_count_convention':'Sum of authored mesh vertices across unique included meshes, before modifiers; no instances or modifiers.','authored_source_vertices':sum(len(o.data.vertices) for o in collection.all_objects if o.type=='MESH'),'target_runtime':'Three.js 0.180.0; runtime evidence pending','topology_notes':'All elements closed and opaque. Deliberate buried intersections at organic branch joins. No broad leaf laminae, flat bough boards or radial starburst clumps. Two green palette groups follow older and younger shoot zones.'}
    result=ac.export_asset('conifer-tree',{'en':'Open-crown conifer concept','zh':'开放冠针叶乔木'},'plants',collection,metadata,output_root=out,render=False,max_triangles=config['budgets']['max_triangles'],max_materials=config['budgets']['max_materials'],max_primitives=config['budgets']['max_primitives'])
    assert (out/'conifer-tree/conifer-tree.glb').stat().st_size <= config['budgets']['max_glb_bytes'], 'GLB byte budget exceeded'
    (out/'build-config.json').write_text(json.dumps(config,indent=2)+'\n')
    (out/'build-summary.json').write_text(json.dumps({'generator_sha256':metadata['generator_sha256'],'counts':metadata['semantic_counts'],'authored_source_vertices':metadata['authored_source_vertices'],'metadata':result},indent=2)+'\n')
if __name__=='__main__':main()
