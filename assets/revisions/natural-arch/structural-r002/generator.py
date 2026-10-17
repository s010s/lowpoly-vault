# SPDX-License-Identifier: MIT
"""Original continuous sandstone fin-arch. Blender 4.3.2; deterministic."""
from pathlib import Path
import argparse,sys,json,math,hashlib
import bpy,bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset

def clamp(x):return min(1.,max(0.,x))
def tent(x,a,b,c,d):return min(clamp((x-a)/(b-a)),clamp((d-x)/(d-c)))
def bed(p):return p.z+.045*p.x-.015*p.y

def cut_planes(obj,levels):
    bm=bmesh.new();bm.from_mesh(obj.data)
    for h in levels:
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,h),plane_no=(.045,-.015,1),clear_inner=False,clear_outer=False)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free()

def subtract(obj,polygon,name,y_front,y_back,col):
    n=len(polygon);vs=[(x,y,z) for y in (y_front,y_back) for x,z in polygon]
    fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    cutter=mesh_object(name,vs,fs,None,col)
    bpy.context.view_layer.objects.active=obj;obj.select_set(True)
    mod=obj.modifiers.new(name,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name);obj.select_set(False)
    cutter.hide_render=True;cutter.hide_set(True);cutter['purpose']='Editable construction cutter, excluded from export.'

def build(cfg):
    col=setup_scene('natural-arch',seed=cfg['seed'])
    mats=[make_material('Sandstone_lower_mass','#A89578',.89),make_material('Sandstone_middle_mass','#B3A080',.89),make_material('Sandstone_upper_mass','#B7A482',.89)]
    outer=cfg['outer_profile'];inner=cfg['inner_profile']
    # Narrow, unequal bevels avoid a broad molded border. Front and rear are independent low-frequency planes.
    cross=[(0,.16),(.045,.025),(.43,0),(.94,.035),(1,.19),(1,.72),(.965,.95),(.57,1),(.08,.94),(0,.75)]
    vs=[];fs=[];n=len(cross)
    for i,((ox,oz),(ix,iz)) in enumerate(zip(outer,inner)):
        s=i/(len(outer)-1)
        depth=1.02+.66*math.exp(-((s-.11)/.22)**2)+.20*math.exp(-((s-.95)/.14)**2)
        front=-.60-.18*math.exp(-((s-.19)/.22)**2)+.10*math.exp(-((s-.58)/.19)**2)
        for u,d in cross:
            x=ix+(ox-ix)*u;z=iz+(oz-iz)*u;y=front+depth*d
            if i not in (0,len(outer)-1):
                x+=(d-.5)*(.13*math.sin(math.pi*s)-.055)
                z+=(d-.5)*(.17*math.sin(1.3*math.pi*s))
                # Surface-directed broad, nonconcentric facets.
                y+=.055*math.sin(x*1.45+z*.71)*(1-abs(2*d-1))
            vs.append((x,y,z))
    for i in range(len(outer)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.extend([tuple(range(n-1,-1,-1)),tuple((len(outer)-1)*n+j for j in range(n))])
    obj=mesh_object('Continuous_fin_arch_with_unequal_buttresses',vs,fs,mats,col)
    cut_planes(obj,[.38,.58,.83,1.03,1.30,1.62,2.03,2.72])
    for v in obj.data.vertices:
        p=v.co;q=bed(p)
        # Local exposure lobes follow beds but taper across the rock face.
        # There are no circumferential support grooves or long crest incisions.
        left_patch=tent(q,.38,.58,.83,1.03)*tent(p.x,-2.62,-2.21,-1.78,-1.16)*.105
        right_weathering=tent(q,.38,.83,1.30,1.62)*tent(p.x,1.40,1.73,2.10,2.40)*.13
        f=clamp((.05-p.y)/.60);b=clamp((p.y-.10)/.60)
        p.y+=(left_patch+right_weathering)*f
        # Restrained local outer-edge loss, fading before the grounded feet.
        if p.x>1.4:p.x-=right_weathering*.20*clamp((p.x-1.9)/.45)
        # Rear upper right shoulder loses depth, while broad left buttress keeps its weight.
        rear=.24*tent(p.x,.20,.75,1.75,2.35)*tent(p.z,1.92,2.32,2.90,3.25)
        p.y-=rear*b
    obj.data.update()
    operations=bpy.data.collections.new('SOURCE_OPERATIONS');bpy.context.scene.collection.children.link(operations)
    # One irregular shoulder spall is the dominant ledge; the broad crest stays quiet.
    subtract(obj,[(-3.2,2.03),(-2.28,2.04),(-1.80,2.18),(-1.61,2.32),(-1.98,2.53),(-2.59,2.48),(-3.2,2.56)],'Localized_tapering_left_shoulder_spall',-2.0,-.38,operations)
    # Three restrained sedimentary values. No dark belts painted to mimic shadows.
    for f in obj.data.polygons:
        p=sum((obj.data.vertices[i].co for i in f.vertices),Vector())/len(f.vertices)
        q=bed(p);f.material_index=0 if q<.90 else 1 if q<2.72 else 2
    bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.shade_flat()
    obj['structure']='One continuous volume; thick irregular left fin, thinner right buttress, rear depth loss, physical selective weak-bed recession.'
    # One low fallen slab, not a decorative rubble border.
    v=[(-.47,-.25,0),(.41,-.23,0),(.52,.16,0),(-.33,.29,0),(-.38,-.18,.11),(.36,-.16,.19),(.30,.17,.16),(-.28,.23,.08)]
    v=[(x-2.14,y-.93,z) for x,y,z in v]
    f=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    mesh_object('Localized_low_shoulder_spall',v,f,mats[1],col)
    return col

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());a.output_dir.mkdir(parents=True,exist_ok=True)
    if list(a.output_dir.iterdir()):raise RuntimeError('Attempt outputs must be empty')
    col=build(cfg);scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
    md={'description':{'en':'Evidence-informed stylized sandstone fin-arch with an irregular high left shoulder, offset opening, unequal supports and selective weak-bed undercuts. Not a named site or prehistoric reconstruction.','zh':'有依据的风格化砂岩石拱：左肩高耸、孔洞偏心、不等支脚与局部弱层凹退；非具体地点或史前环境复原。'},'generator':str(Path(__file__).relative_to(ROOT)),'generator_model':'GPT-6 Astra, xhigh','generator_parameters':cfg,'sources':[{'title':'NPS Geodiversity Atlas: Arches, Arch Formation','url':'https://www.nps.gov/articles/nps-geodiversity-atlas-arches-national-park-utah.htm','use':'Consulted for fins, joints and erosion; geometry original.'}],'scientific_scope':'Time-neutral evidence-informed stylized concept. Dimensions and erosion pattern are artistic; no structural engineering claim.','provenance':{'geometry':'Original deterministic design','textures':'None','license':'CC-BY-4.0','author':'Leon Made This / s010s'},'status':'unapproved_structural_candidate'}
    record=export_asset('natural-arch',{'en':'Natural arch · Structural candidate','zh':'天然石拱 · 结构候选'},'geology',col,metadata=md,output_root=a.output_dir,collection_id='structural-refinement',render=False,max_triangles=6000,max_materials=3,max_primitives=6)
    print('BUILD_RESULT='+json.dumps(record),flush=True)
if __name__=='__main__':main()
