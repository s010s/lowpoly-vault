#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original conifer quality study, without reference-code/model reuse.

blender -b --threads 2 --python-exit-code 1 --python scripts/experiments/build_conifer_quality_v2.py -- [--draft] [--no-render]
This independent experiment never writes the production asset paths.
Code MIT; generated asset CC-BY-4.0, Leon Made This / s010s.
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
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import asset_common as ac

OUT=ROOT/'experiments'/'quality-v2'
SLUG='conifer-v2'
COLORS={'bark_mid':'#79624B','bark_deep':'#4F443D','cut_wood':'#B59B72','fern_deep':'#294C43','fern_mid':'#47745C','fern_light':'#719366'}
TAU=math.tau

class Mesh:
    def __init__(self,name,collection,materials):
        self.name=name;self.c=collection;self.mats=materials;self.v=[];self.f=[];self.materials=[]
    def add(self,vs,fs,mat=0):
        o=len(self.v);self.v.extend(tuple(x) for x in vs);self.f.extend(tuple(o+i for i in f) for f in fs)
        self.materials.extend(mat if isinstance(mat,list) else [mat]*len(fs))
    def create(self):
        ob=ac.mesh_object(self.name,self.v,self.f,self.mats,self.c)
        for p,i in zip(ob.data.polygons,self.materials):p.material_index=i
        return ob

def V(v):return Vector(v)
def direction(deg):return V((math.cos(math.radians(deg)),math.sin(math.radians(deg)),0))
def axes(axis):
    a=V(axis).normalized();r=V((0,0,1)) if abs(a.z)<.91 else V((0,1,0))
    u=a.cross(r).normalized();v=a.cross(u).normalized();return u,v

def loft(mesh,ps,rs,n,mat=0,cap=None):
    points=[V(p) for p in ps];vs=[];fs=[];ms=[]
    for i,p in enumerate(points):
        a=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized();u,v=axes(a)
        for j in range(n):
            angle=TAU*j/n+.19
            vs.append(p+(math.cos(angle)*u+math.sin(angle)*v)*rs[i])
    fs.append(tuple(reversed(range(n))));ms.append(mat)
    for i in range(len(points)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j));ms.append(mat)
    fs.append(tuple((len(points)-1)*n+j for j in range(n)));ms.append(mat if cap is None else cap)
    mesh.add(vs,fs,ms)

def pathpoint(points,t):
    segments=len(points)-1;q=max(0,min(t,.999999))*segments;i=int(q);return V(points[i]).lerp(V(points[i+1]),q-i)

def needle(mesh,base,axis,length,width,roll,mat):
    """A solid narrow triangular needle bundle, not a broad foliage plate.

    Four faces express a stiff needle in a stable, closed 3D representation.
    It is a stylized bundle envelope, not a claim about a fascicle count.
    """
    a=V(axis).normalized();u,v=axes(a);w=u*math.cos(roll)+v*math.sin(roll);h=a.cross(w).normalized()
    p=V(base)
    vs=[p+w*width*.5-h*width*.10,p-w*width*.5-h*width*.10,p+h*width*.26,p+a*length]
    mesh.add(vs,[(0,2,1),(0,1,3),(1,2,3),(2,0,3)],mat)


def leafy_shoot(wood,foliage,base,axis,length,spread,phase,age=0):
    """Short evergreen twig with radial needle bundles along its distal axis."""
    a=V(axis).normalized();u,v=axes(a);p=V(base)
    bend=V((0,0,.07))*spread
    middle=p+a*length*.55+bend*.65;end=p+a*length+bend
    loft(wood,[p,middle,end],[.023*spread,.014*spread,.0045*spread],4,0)
    # Spiral groups occupy several axial positions, rather than one pom-pom tip.
    for i in range(11):
        t=.16+i*.069
        angle=phase+i*2.3999632297
        radial=u*math.cos(angle)+v*math.sin(angle)
        outward=(a*(.38+.12*(i%3))+radial*.92+V((0,0,.11))).normalized()
        site=p.lerp(end,t)+radial*.010*spread
        size=(.30+.045*math.sin(i*1.37+phase))*spread*(1-.12*t)
        m=0 if age==0 and i<5 else 1
        if i>=9 and age>0:m=2
        needle(foliage,site,outward,size,.080*spread,angle*.33,m)
    needle(foliage,end-a*.025,a,.23*spread,.056*spread,phase,2 if age>0 else 1)
    return end


def build():
    c=ac.setup_scene(SLUG,261016)
    mats={k:ac.make_material(k,v) for k,v in COLORS.items()}
    bark=[mats['bark_mid'],mats['bark_deep'],mats['cut_wood']]
    greens=[mats['fern_deep'],mats['fern_mid'],mats['fern_light']]
    trunk=Mesh('Conifer v2 | tapering dominant axis',c,bark)
    trunk_ps=[(0,0,.04),(.015,.015,.35),(-.02,.035,1.0),(-.05,.04,1.9),(.02,.055,2.85),(.09,.02,3.8),(.13,.055,4.7),(.17,.085,5.65),(.12,.10,6.45),(.16,.11,7.0)]
    loft(trunk,trunk_ps,[.33,.28,.232,.202,.174,.145,.12,.084,.043,.009],9)
    roots=Mesh('Conifer v2 | unequal buttress roots',c,bark)
    for a,L,w in [(12,.63,.17),(104,.55,.15),(193,.74,.19),(266,.49,.14),(318,.60,.15)]:
        d=direction(a)
        loft(roots,[(0,0,.23),d*.26+V((0,0,.12)),d*L+V((0,0,.028))],[w,w*.58,.018],6)
    main=Mesh('Conifer v2 | primary structural boughs',c,bark)
    secondary=Mesh('Conifer v2 | secondary branchlet fans',c,bark)
    twigs=Mesh('Conifer v2 | fine terminal woody shoots',c,[mats['bark_mid']])
    foliage_groups=[Mesh('Conifer v2 | lower crown needle shoots',c,greens),Mesh('Conifer v2 | middle crown needle shoots',c,greens),Mesh('Conifer v2 | upper crown and leader needles',c,greens)]
    # Authored crown directions and reaches. Three overlapping height groups
    # have different density and bough sweep; one forward opening is deliberate.
    boughs=[
      (1.91,-151,1.62,.34,1.00),(2.07,-44,1.26,.24,.88),(2.17,43,1.73,.61,1.04),(2.01,138,1.51,.45,.96),
      (2.91,-107,1.96,.66,1.07),(3.03,-9,1.77,.50,1.04),(2.78,82,1.88,.70,1.08),(3.12,176,1.78,.64,.99),
      (3.88,-151,1.71,.69,1.04),(3.66,-56,1.81,.63,1.06),(4.02,31,1.62,.74,1.00),(4.13,119,1.48,.56,.94),
      (4.89,-108,1.37,.65,.94),(4.69,-12,1.30,.61,.94),(4.94,80,1.23,.68,.88),(4.81,171,1.41,.66,.96),
      (5.62,-49,.91,.65,.80),(5.73,64,1.02,.56,.83),(5.80,185,.89,.58,.79),
      (6.32,-151,.53,.42,.64),(6.27,-19,.61,.46,.68),(6.36,103,.54,.43,.63),
    ]
    shoot_count=0
    for b,(z,a,L,lift,size) in enumerate(boughs):
        g=0 if z<3.3 else 1 if z<5.35 else 2
        foliage=foliage_groups[g]
        d=direction(a);side=direction(a+90)
        center=V((.03+.023*z,.025+.009*z,z))
        # Upturned outer boughs and staggered starts prevent horizontal shelves.
        points=[center,center+d*L*.28+V((0,0,-.085)),center+d*L*.62+side*.05+V((0,0,lift*.30)),center+d*L+side*.09+V((0,0,lift))]
        base_r=.078 if z<3.4 else .064 if z<5.35 else .045
        loft(main,points,[base_r,base_r*.75,base_r*.43,.012],6 if z<5.35 else 5)
        # All lower fans are asymmetric. The gap bough has only one side fan.
        slots=[(.30,-1,.69),(.48,1,.83),(.67,-1,.68),(.82,1,.50)] if z<5.35 else [(.38,-1,.57),(.66,1,.47)]
        if b==1:slots=[(.53,1,.60),(.80,-1,.40)]
        for k,(t,sign,reach) in enumerate(slots):
            root=pathpoint(points,t)
            angle=a+sign*(46-9*t)+(-3 if b%3==0 else 3)
            sd=direction(angle)
            sl=reach*size
            endpoint=root+sd*sl+V((0,0,.17+.09*size))+side*(.035*sign)
            bend=root.lerp(endpoint,.52)+V((0,0,-.04))
            loft(secondary,[root,bend,endpoint],[.032*size,.021*size,.0085*size],4)
            # The tip shoot plus an unequal lateral offshoot give each branchlet
            # a recognizable fan. Long bare branchlets are avoided deliberately.
            endaxis=(endpoint-bend).normalized()
            leafy_shoot(twigs,foliage,endpoint-endaxis*.14*size,endaxis,.35*size,.92*size,b*.47+k*.81,age=1 if g==2 else 0)
            shoot_count+=1
            if not (g==2 and k==0):
                attach=root.lerp(endpoint,.57)
                sda=direction(angle-sign*39)+V((0,0,.43))
                leafy_shoot(twigs,foliage,attach,sda,.32*size,.78*size,b*.63+k*.32+1.1,age=1 if (g==2 or (b%4==0 and k==2)) else 0)
                shoot_count+=1
        tipaxis=(V(points[-1])-V(points[-2])).normalized()
        leafy_shoot(twigs,foliage,V(points[-1])-tipaxis*.13*size,tipaxis,.38*size,size,b*.71,age=1 if g>0 else 0)
        shoot_count+=1
    # A small cluster around the continuing trunk tip gives a live leader,
    # with subordinate shoots rather than a separate conical crown primitive.
    for j,(a,h) in enumerate([(14,6.72),(141,6.79),(257,6.86)]):
        leafy_shoot(twigs,foliage_groups[2],(.15,.10,h),direction(a)*.30+V((0,0,.95)),.26,.62,j*.81,age=1)
        shoot_count+=1
    loft(main,[(.01,0,1.27),(-.30,-.13,1.36),(-.46,-.18,1.39)],[.055,.032,.015],5,1,2)
    for part in [trunk,roots,main,secondary,twigs]+foliage_groups:part.create()
    ac.ground_asset(c)
    meta={
      'description':{'en':'Original conifer quality sample with structural boughs, asymmetric secondary fans, fine terminal shoots and short solid needle bundles.','zh':'原创针叶树质量样板：主枝、错落侧枝扇、细末梢与短窄立体针叶簇形成连续且有疏密的树冠。'},
      'generator':'scripts/experiments/build_conifer_quality_v2.py','generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'generator_license':'MIT',
      'scientific_status':'evidence-informed stylized concept; no species-level reconstruction',
      'scientific_context':'Conifer architectural concept; geological period and taxon not established by this style experiment.',
      'artistic_choices':['Crown lean, exact near-whorl spacing, branchlet angles, needle grouping, palette and seven-meter display size are original art direction.','Solid narrow tetrahedral needle units summarize several fine needles at medium range; no anatomical fascicle count is claimed.'],
      'originality':'All geometry and code were independently authored. RHS059/low_poly_items was studied only for visual hierarchy; no reference meshes, materials, code or images are included.',
      'design_revision':2,'primary_bough_count':len(boughs),'terminal_shoot_count':shoot_count,
      'usage_profile':{
        'role':'Single focal tree / sparse close-to-midground grove quality sample; not a mass-forest LOD',
        'renderer':'Three.js 0.180.0, opaque rough materials, no texture dependency',
        'screen_coverage_px':[128,512,900],'preferred_coverage_px':[350,650],
        'supported_inspection':'Branch-to-fan and fan-to-needle grouping at medium range; not macro needle anatomy',
        'provisional_visible_instance_count':[1,20],'stress_instance_count':50,
        'frame_time_target':'Not yet benchmarked; no FPS claim',
        'lod':'One authored quality sample only. A lower-detail far variant is a separate future decision.',
        'geometry_budget_decision':'Spend geometry on growth hierarchy and actual short narrow foliage, then measure. Old 2600-triangle cap does not apply. No subdivision is used to fill a ceiling.'
      },
      'sources':[{'url':'https://www.nhm.ac.uk/discover/how-to-grow-a-dinosaur-garden.html','supports':'Broad conifer context; not proof of a particular extinct needle arrangement'},{'url':'https://github.com/RHS059/low_poly_items/tree/2c3cf681cce1cdbcb8f0c7297120422ab178ab90','supports':'Visual study of primary/secondary/tertiary form hierarchy only; no licensed content reused'}],
      'topology_notes':'Every needle bundle is a closed four-face solid. Woody components are closed tapering lofts with purposeful buried growth junctions. No transparency, billboard cards, normals tricks or per-face random color.',
    }
    return c,meta

def comparison_frame(collection):
    """Temporary invisible bounds fixture gives old/new the exact same camera.
    It is added only after export, and is never saved into either source file.
    """
    paths=[ROOT/'assets'/'prehistoric'/'plants'/'conifer-tree'/'qa.json',OUT/SLUG/'qa.json']
    boxes=[json.loads(p.read_text())['source']['bounds_blender_m'] for p in paths]
    low=[min(b['min'][i] for b in boxes) for i in range(3)]
    high=[max(b['max'][i] for b in boxes) for i in range(3)]
    data=bpy.data.meshes.new('_comparison_frame_mesh')
    data.from_pydata([(x,y,z) for x in [low[0],high[0]] for y in [low[1],high[1]] for z in [low[2],high[2]]],[],[])
    obj=bpy.data.objects.new('_comparison_frame',data);collection.objects.link(obj);obj.hide_render=True
    return {'blender_min_m':low,'blender_max_m':high,'description':'Shared invisible union-bounds framing fixture. Exact same camera framing, light rig, stage and render settings for both versions. Never exported or saved.'}


def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument('--draft',action='store_true');p.add_argument('--no-render',action='store_true');p.add_argument('--output-root',type=Path,default=OUT);p.add_argument('--compare-v1',action='store_true')
    a=p.parse_args(argv)
    if a.compare_v1:
        bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets'/'prehistoric'/'plants'/'conifer-tree'/'conifer-tree.blend'))
        c=bpy.data.collections['EXPORT'];frame=comparison_frame(c)
        out=OUT/SLUG/'comparison-v1';out.mkdir(parents=True,exist_ok=True)
        files=ac.render_previews(c,out,views=('hero','reversehero','clay'),resolution=1024,samples=32)
        (out/'render-settings.json').write_text(json.dumps({'frame':frame,'resolution':1024,'samples':32,'view_transform':'Standard','source':'assets/prehistoric/plants/conifer-tree/conifer-tree.blend','source_modified':False,'files':[Path(f).name for f in files]},indent=2)+'\n')
        return
    c,meta=build()
    record=ac.export_asset(SLUG,{'en':'Conifer quality v2','zh':'针叶树质量样板 v2'},'plants',c,meta,output_root=a.output_root,render=False,max_triangles=20000,max_materials=8,max_primitives=24,diagnostics=False)
    out=a.output_root/SLUG
    qa=json.loads((out/'qa.json').read_text())
    counts={'source_vertices':sum(p['vertices'] for p in qa['source']['parts']),'export_position_vertices':qa['glb']['unique_position_accessor_vertices'],'export_triangles':qa['glb']['scene_triangles'],'primitives':qa['glb']['scene_primitives_estimated_base_draw_calls'],'materials':qa['glb']['materials'],'bytes':qa['glb']['bytes']}
    record['geometry_metrics']=counts;(out/'metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    (out/'parameters.json').write_text(json.dumps({'recipe':'build_conifer_quality_v2.py','seed':261016,'primary_boughs':meta['primary_bough_count'],'terminal_shoots':meta['terminal_shoot_count'],'needle_bundles_per_terminal_shoot':12,'geometry_metrics':counts,'usage_profile':meta['usage_profile']},indent=2,ensure_ascii=False)+'\n')
    if not a.no_render:
        frame=comparison_frame(c)
        files=ac.render_previews(c,out,views=('hero','reversehero') if a.draft else ('hero','reversehero','side','clay','clay-alt','silhouette'),resolution=640 if a.draft else 1024,samples=16 if a.draft else 32)
        qa['previews']={'status':'pending_visual_review','files':[Path(f).name for f in files],'resolution':640 if a.draft else 1024,'samples':16 if a.draft else 32,'renderer':'Cycles CPU','rig':'shared asset_common Standard neutral rig','comparison_frame':frame}
        (out/'qa.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
    print('GEOMETRY_METRICS',json.dumps(counts),flush=True)

if __name__=='__main__':main()
