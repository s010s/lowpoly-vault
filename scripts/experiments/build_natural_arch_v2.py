"""Original quality-sample arch: erosion changes geometry, not only bands.

Cloud Blender 4.3.2. No reference model or source code is incorporated.
  blender -b -t 3 --python-exit-code 1 --python scripts/experiments/build_natural_arch_v2.py
  ... -- --draft                 # 640px first-look views
  ... -- --no-render             # geometry and measured export
  ... -- --compare               # same-camera old/new 1024px diagnostic pairs
"""
from pathlib import Path
import sys,math,json,argparse,hashlib
import bpy,bmesh
from mathutils import Vector,Euler
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset,audit_source,ground_asset,render_previews
from qa_glb import audit_glb
SLUG='natural-arch-v2'
OUT=ROOT/'experiments'/'quality-v2'/SLUG
OLD=ROOT/'assets'/'prehistoric'/'geology'/'natural-arch'/'natural-arch.blend'


def clamp(x,a=0.,b=1.):return max(a,min(b,x))
def trapezoid(x,a,b,c,d):return min(clamp((x-a)/(b-a)),clamp((d-x)/(d-c)))
def bed_coordinate(p):return p.z-.06*p.x-.02*p.y


def split_planes(obj,levels):
    bm=bmesh.new();bm.from_mesh(obj.data)
    for h in levels:
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,
            plane_co=(0,0,h),plane_no=(-.06,-.02,1),clear_inner=False,clear_outer=False)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(obj.data);bm.free();obj.data.update()


def assign_beds(obj):
    for face in obj.data.polygons:
        p=sum((obj.data.vertices[i].co for i in face.vertices),Vector())/len(face.vertices)
        q=bed_coordinate(p)
        weak_exposure=(.97<q<1.10 and p.x>.85) or (2.13<q<2.20 and p.x<-.8)
        face.material_index=1 if weak_exposure else 2 if q>3.03 else 0


def cutter_mesh(col):
    # One broad planar shoulder joint opens toward the front and outside edge.
    polygon=[(-3.35,1.76),(-2.29,1.83),(-1.45,2.48),(-1.78,2.75),(-3.35,2.80)]
    vertices=[(x,y,z) for y in (-2.3,-.19) for x,z in polygon]
    n=len(polygon);faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    for i in range(n):faces.append((i,(i+1)%n,(i+1)%n+n,i+n))
    return mesh_object('SOURCE_Shoulder_joint_cutting_volume',vertices,faces,None,col)


def apply_bool(obj,cutter,operation):
    bpy.context.view_layer.objects.active=obj;obj.select_set(True)
    mod=obj.modifiers.new('Planar_shoulder_'+operation,'BOOLEAN');mod.operation=operation;mod.solver='EXACT';mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.data.update();obj.select_set(False)


def chip(col,mat):
    v=[(-.31,-.15,0),(.30,-.13,0),(.10,.22,0),(-.22,-.10,.12),(.19,-.09,.19),(.07,.12,.13)]
    v=[(x-1.13,y-1.13,z) for x,y,z in v]
    f=[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)]
    return mesh_object('Small_chip_below_same_shoulder_failure',v,f,mat,col)


def build():
    col=setup_scene(SLUG,seed=0)
    mats=[make_material('warm_stone','#A89578'),make_material('earth','#8A715B'),make_material('stone_light','#C7B798')]
    # The opening and crest have separate, deliberately unequal rhythms.
    outer=[(-2.83,0),(-2.88,.41),(-2.67,.88),(-2.62,1.34),(-2.48,1.85),(-2.29,2.22),
           (-2.13,2.56),(-1.91,2.99),(-1.40,3.35),(-.83,3.46),(-.19,3.43),(.35,3.23),
           (.92,3.17),(1.43,2.94),(1.88,2.49),(2.15,2.02),(2.27,1.45),(2.31,.91),(2.46,.43),(2.52,0)]
    inner=[(-.91,0),(-1.01,.26),(-1.19,.62),(-1.23,1.00),(-1.08,1.38),(-.91,1.64),
           (-.68,1.91),(-.39,2.18),(-.11,2.38),(.22,2.45),(.57,2.32),(.89,2.12),
           (1.10,1.83),(1.25,1.63),(1.43,1.46),(1.50,1.18),(1.48,.85),(1.49,.54),(1.57,.25),(1.61,0)]
    # Mid-face vertices are structural folds, not uniform triangular noise.
    cross=[(0,.15),(.09,.035),(.33,-.020),(.70,.015),(.92,.075),(1,.19),
           (1,.71),(.92,.91),(.65,1.0),(.29,.95),(.07,.88),(0,.75)]
    vertices=[];faces=[];count=len(cross)
    for i,((ox,oz),(ix,iz)) in enumerate(zip(outer,inner)):
        s=i/(len(outer)-1)
        thick=1.12+.56*math.exp(-((s-.11)/.22)**2)+.18*math.exp(-((s-.94)/.17)**2)
        front=-.54-.17*math.exp(-((s-.18)/.20)**2)-.11*math.exp(-((s-.63)/.16)**2)
        for u,d in cross:
            x=ix+(ox-ix)*u
            z=iz+(oz-iz)*u
            y=front+thick*d
            # The rear crown leans away; the feet retain broad ground contact.
            if i not in (0,len(outer)-1):
                x+=(d-.5)*(-.13*math.sin(math.pi*s)+.045)
                z+=(d-.5)*.13*math.sin(math.pi*s)
            vertices.append((x,y,z))
    for i in range(len(outer)-1):
        for j in range(count):faces.append((i*count+j,i*count+(j+1)%count,(i+1)*count+(j+1)%count,(i+1)*count+j))
    faces.extend([tuple(range(count-1,-1,-1)),tuple((len(outer)-1)*count+j for j in range(count))])
    arch=mesh_object('Arch_resistant_crown_and_eroded_supports',vertices,faces,mats,col)
    # Cutting at the erosion transitions makes the stepped profile deliberate.
    split_planes(arch,[.79,.91,1.10,1.23,2.04,2.12,2.25,2.34,3.03])
    for v in arch.data.vertices:
        p=v.co;q=bed_coordinate(p)
        low=trapezoid(q,.79,.91,1.10,1.23)
        upper=trapezoid(q,2.04,2.12,2.25,2.34)
        low_strength=.055+.10*clamp((p.x+.8)/2.0)
        upper_strength=.15*(1-.75*clamp((p.x+.6)/2.0))
        recess=low_strength*low+upper_strength*upper
        f=clamp(-p.y/.50);back=clamp(p.y/.55)
        p.y+=recess*(1.18*f-.74*back)
        if p.z<2.25:
            if p.x<-1.0:p.x+=recess*.52*math.tanh((-1.84-p.x)*4.0)
            elif p.x>1.12:p.x+=recess*.77*math.tanh((1.94-p.x)*4.0)
        # One rear shoulder is markedly thinner; this is absent on the front.
        rear_loss=.25*trapezoid(p.x,.55,.95,1.60,2.02)*trapezoid(p.z,1.72,2.03,2.55,2.88)
        p.y-=rear_loss*back
    arch.data.update()
    operations=bpy.data.collections.new('SOURCE_OPERATIONS');bpy.context.scene.collection.children.link(operations)
    cutter=cutter_mesh(operations)
    fragment=arch.copy();fragment.data=arch.data.copy();fragment.name='Fallen_shoulder_flake_original_break_geometry';col.objects.link(fragment)
    apply_bool(fragment,cutter,'INTERSECT')
    apply_bool(arch,cutter,'DIFFERENCE')
    cutter.hide_render=True;cutter.hide_set(True);cutter['purpose']='Editable source construction reference; excluded from GLB.'
    assign_beds(arch);assign_beds(fragment)
    coords=[v.co.copy() for v in fragment.data.vertices]
    middle=sum(coords,Vector())/len(coords)
    # Rest the largest fracture face flat on the ground instead of balancing
    # the flake on a visually floating corner.
    largest_face=max(fragment.data.polygons,key=lambda face:face.area)
    settle=largest_face.normal.rotation_difference(Vector((0,0,-1))).to_matrix()
    rotation=Euler((0,0,math.radians(-20))).to_matrix()@settle
    transformed=[rotation@(p-middle) for p in coords]
    low=min(p.z for p in transformed)
    for v,p in zip(fragment.data.vertices,transformed):v.co=p+Vector((-2.47,-1.14,-low))
    fragment.data.update()
    chip(col,mats[0])
    # Flat normals are recomputed after intentional spatial deformation and cuts.
    for obj in [arch,fragment]:
        bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.shade_flat()
    ground_asset(col)
    arch['structure']='Two weak beds retreat physically; left shoulder has a broad planar break; rear right shoulder loses thickness.'
    fragment['structure']='Geometry removed from that shoulder, rotated into a localized fallen flake.'
    metadata={
      'description':{'en':'Experimental natural arch with physical weak-bed undercuts, an asymmetric load-bearing crown, a broad shoulder fracture, and its localized fallen flake.','zh':'质量样板：具有真实弱层凹退、不等厚承重冠部、宽大肩部剥落及对应落块的天然石拱。'},
      'generator':'scripts/experiments/build_natural_arch_v2.py','generator_model':'GPT-6 Astra, xhigh','status':'experimental_quality_sample_not_approved_replacement',
      'component_and_cause':{'primary':'A thick left crown bridges a shifted, irregular opening to a narrower right support.','secondary':['Two weaker beds recede through depth and support width.','A planar shoulder joint removes a broad front-left corner.','The back-right shoulder is thinner than its front.'],'tertiary':'The removed shoulder fragment lies locally below its source; one smaller chip shares the fall zone.','quiet_region':'The resistant upper crown retains broad unbroken facets.'},
      'budget_profile':{'role':'Single focal geological landmark and close gallery inspection; not a repeated background rock.','renderer':'Three.js 0.180.0 target; Blender 4.3.2 diagnostic renders','screen_coverage_px':[128,512,820],'assumed_simultaneous_instances':{'typical':1,'stress_for_later_runtime_test':8},'lod':'One close/medium mesh in this sample. No distant LOD or performance claim.','provisional_ceilings':{'triangles':3500,'export_position_vertices':8500,'materials':3,'primitives':9,'glb_bytes':250000},'reason':'Geometry is reserved for broad undercuts, the shoulder fracture, depth variation, and the opening; no subdivision is added merely to approach a ceiling.','unverified':'Target-device frame times, 8-instance scene timing and 32px distant suitability remain unmeasured.'},
      'reference_learning':{'study':'qa/reference-quality-study.md','principle':'Middle-scale, cause-based structure remains visible after color removal.','reuse':'No RHS059 model, code, palette, texture, or screenshot is incorporated.'},
      'scientific_scope':{'en':'Original stylized erosion-landform concept; not a reconstructed named arch, fossil locality, or geological measurement.','zh':'原创风格化侵蚀地貌概念，不对应具体石拱、化石地点或地质测量。'},
      'sources':[{'title':'NPS Geodiversity Atlas: Arches','url':'https://www.nps.gov/articles/nps-geodiversity-atlas-arches-national-park-utah.htm','use':'General erosion context only.'}],
      'design_notes':['Bedding shifts both surface position and support thickness; bands alone no longer provide the entire geological story.','The detached flake is the actual cut piece, not an evenly distributed decorative pebble.','All geometry is original and deterministic.']}
    return col,metadata


def snapshot(col):
    deps=bpy.context.evaluated_depsgraph_get();data=[]
    for o in col.all_objects:
        if o.type!='MESH':continue
        ev=o.evaluated_get(deps);me=ev.to_mesh()
        try:
            me.calc_loop_triangles();data.append({'name':o.name,'vertices':[tuple(ev.matrix_world@v.co) for v in me.vertices],
                'faces':[tuple(p.vertices) for p in me.polygons],'material_indices':[p.material_index for p in me.polygons],
                'materials':[{'name':m.name,'color':m.get('palette_srgb','#A89578')} for m in me.materials]})
        finally:ev.to_mesh_clear()
    return data


def compare():
    """Old/new scenes get exactly the same camera transform, ortho span and rig."""
    bpy.ops.wm.open_mainfile(filepath=str(OLD));old=snapshot(bpy.data.collections['EXPORT'])
    bpy.ops.wm.open_mainfile(filepath=str(OUT/(SLUG+'.blend')));new=snapshot(bpy.data.collections['EXPORT'])
    all_points=[Vector(p) for group in [old,new] for part in group for p in part['vertices']]
    lo=Vector([min(p[k] for p in all_points) for k in range(3)]);hi=Vector([max(p[k] for p in all_points) for k in range(3)])
    center=(lo+hi)/2;span=max(hi-lo)
    folder=OUT/'comparison';folder.mkdir(exist_ok=True)
    views={'hero':Vector((.574,-.819,.466)),'reverse':Vector((-.574,.819,.466)),'side':Vector((1,0,.18))}
    camera_specs={}
    for name,direction in views.items():
        direction.normalize();rotation=(-direction).to_track_quat('-Z','Y');inverse=rotation.to_matrix().transposed()
        pp=[inverse@(p-center) for p in all_points]
        width=max(p.x for p in pp)-min(p.x for p in pp);height=max(p.y for p in pp)-min(p.y for p in pp)
        shift=rotation@Vector(((max(p.x for p in pp)+min(p.x for p in pp))/2,(max(p.y for p in pp)+min(p.y for p in pp))/2,0))
        camera_specs[name]=(center+direction*span*4+shift,rotation,max(width,height)*1.25)
    rendered=[]
    for version,parts in [('old',old),('new',new)]:
        col=setup_scene('comparison-'+version)
        cache={}
        for part in parts:
            material_list=[]
            for mat in part['materials']:
                key=(mat['name'],mat['color'])
                if key not in cache:cache[key]=make_material(*key)
                material_list.append(cache[key])
            obj=mesh_object(part['name'],part['vertices'],part['faces'],material_list,col)
            for polygon,mi in zip(obj.data.polygons,part['material_indices']):polygon.material_index=mi
        scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False;scene.cycles.device='CPU'
        scene.render.threads_mode='FIXED';scene.render.threads=3
        scene.render.resolution_x=scene.render.resolution_y=1024;scene.render.resolution_percentage=100
        scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
        world=bpy.data.worlds.new('Fixed_comparison_world');world.use_nodes=True
        world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
        for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
            light=bpy.data.lights.new(name,'AREA');light.energy=energy*span*span/4;light.shape='DISK';light.size=size*span/2
            obj=bpy.data.objects.new(name,light);scene.collection.objects.link(obj);obj.location=center+Vector(direction)*span/2;obj.rotation_euler=(center-obj.location).to_track_quat('-Z','Y').to_euler()
        floor=mesh_object('Comparison_floor',[(-60,-60,-.002),(60,-60,-.002),(60,60,-.002),(-60,60,-.002)],[(0,1,2,3)],make_material('floor','#E8E4DC'),col)
        cam_data=bpy.data.cameras.new('Fixed_comparison_camera');cam_data.type='ORTHO';cam_data.clip_end=100
        cam=bpy.data.objects.new('Fixed_comparison_camera',cam_data);scene.collection.objects.link(cam);scene.camera=cam
        clay=make_material('Neutral_clay','#929292')
        for name in ['hero','reverse','side']:
            cam.rotation_mode='QUATERNION';cam.location,cam.rotation_quaternion,cam_data.ortho_scale=camera_specs[name]
            for material_mode in (['color','clay'] if name=='hero' else ['clay']):
                scene.view_layers[0].material_override=clay if material_mode=='clay' else None
                path=folder/f'{version}-{name}-{material_mode}.png';scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);rendered.append(path.name)
    provenance={'status':'rendered_not_visually_reviewed','old_source':str(OLD.relative_to(ROOT)),'new_source':str((OUT/(SLUG+'.blend')).relative_to(ROOT)),
        'same_rig':True,'same_camera_per_view':True,'independent_normalization':False,'resolution':1024,'samples':32,'view_transform':'Standard','key_to_fill_power_ratio':3,
        'common_bounds_m':{'min':list(lo),'max':list(hi)},'files':rendered}
    (folder/'comparison-settings.json').write_text(json.dumps(provenance,indent=2)+'\n')
    rows=''.join(f'<h2>{label}</h2><div class="pair"><figure><img src="old-{view}-{mode}.png"><figcaption>v1</figcaption></figure><figure><img src="new-{view}-{mode}.png"><figcaption>v2</figcaption></figure></div>' for label,view,mode in [('同角度彩色 / Color','hero','color'),('同角度灰模 / Clay','hero','clay'),('反侧灰模 / Reverse clay','reverse','clay'),('侧面灰模 / Side clay','side','clay')])
    (folder/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Natural arch v1 / v2</title><style>body{font:16px system-ui;background:#e8e4dc;color:#352e26;max-width:1400px;margin:30px auto}.pair{display:flex;gap:12px}figure{margin:0;width:50%}img{width:100%;display:block}figcaption{text-align:center;padding:8px}h2{font-size:19px}</style><h1>天然石拱：结构质量样板</h1><p>每一对使用完全相同的相机、正交画幅、灯光和曝光；未分别归一化尺寸。Same camera, framing, rig and exposure within each pair.</p>'+rows,encoding='utf-8')


def main():
    p=argparse.ArgumentParser();p.add_argument('--draft',action='store_true');p.add_argument('--no-render',action='store_true');p.add_argument('--compare',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if a.compare:compare();return
    col,metadata=build();bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=3
    record=export_asset(SLUG,{'en':'Natural Arch · Quality v2','zh':'天然石拱 · 质量样板 v2'},'geology',col,metadata=metadata,output_root=OUT.parent,collection_id='quality-v2',render=not a.no_render,
        views=('hero','reversehero','clay','clay-alt') if a.draft else ('hero','reversehero','clay','clay-alt','side'),resolution=640 if a.draft else 1024,samples=24 if a.draft else 32,diagnostics=False,max_triangles=3500,max_materials=3,max_primitives=9)
    qa=json.loads((OUT/'qa.json').read_text());source=qa['source'];exported=qa['glb']
    counts={'source_authored_vertices':sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH'),
        'source_evaluated_vertices':sum(p['vertices'] for p in source['parts']),'source_triangles':source['triangles'],
        'export_position_stream_vertices':exported['unique_position_accessor_vertices'],'export_triangles':exported['scene_triangles'],
        'export_primitives':exported['scene_primitives_estimated_base_draw_calls'],'materials':exported['materials'],'glb_bytes':exported['bytes'],
        'note':'No shared POSITION accessors across primitives in this GLB; the unique-accessor sum equals the per-primitive stream sum.'}
    (OUT/'measured-budget.json').write_text(json.dumps(counts,indent=2)+'\n')
    print('ARCH_V2_RESULT='+json.dumps(counts),flush=True)

if __name__=='__main__':main()
