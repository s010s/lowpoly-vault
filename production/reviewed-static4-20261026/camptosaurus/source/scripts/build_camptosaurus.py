# SPDX-License-Identifier: MIT
"""Original reference-led C. dispar reconstruction, explicit closed low-poly lofts.

No existing dinosaur geometry, scan or texture is loaded. All numerical soft
tissue proportions are artistic, not specimen measurements. Run in factory
Blender with -- --config FILE --output-dir DIRECTORY [--greybox].
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_common as ac

P=argparse.ArgumentParser();P.add_argument('--config',type=Path,required=True);P.add_argument('--output-dir',type=Path,required=True);P.add_argument('--greybox',action='store_true')
A=P.parse_args(sys.argv[sys.argv.index('--')+1:]);C=json.loads(A.config.read_text())
E=ac.setup_scene('camptosaurus',C['seed']);scene=bpy.context.scene
scene.render.threads_mode='FIXED';scene.render.threads=2
M=[ac.make_material(k,'#929292' if A.greybox else c,roughness=.88,double_sided=False) for k,c in C['palette']]
YSHIFT=.22
anatomy=[]

def loft(name, nodes, sides=12, material=0, subdivisions=1, color=False, up='auto'):
    """Each node is xyz, ellipse width, ellipse depth; caps are true fans.
    Width axis is projected X except near parallel paths. No negative scale.
    """
    expanded=[]
    for a,b in zip(nodes[:-1],nodes[1:]):
        for j in range(subdivisions):
            t=j/subdivisions;expanded.append([a[k]*(1-t)+b[k]*t for k in range(5)])
    expanded.append(nodes[-1]);nodes=expanded
    V=[];F=[];mids=[]
    for i,n in enumerate(nodes):
        p=Vector(n[:3]);p.y+=YSHIFT
        tangent=Vector(nodes[min(i+1,len(nodes)-1)][:3])-Vector(nodes[max(i-1,0)][:3]);tangent.normalize()
        base=Vector((1,0,0)) if abs(tangent.x)<.88 else Vector((0,1,0))
        u=(base-tangent*base.dot(tangent)).normalized();v=tangent.cross(u).normalized()
        for j in range(sides):
            ang=2*math.pi*j/sides
            q=p+u*math.cos(ang)*n[3]+v*math.sin(ang)*n[4]
            V.append(tuple(q))
    for i in range(len(nodes)-1):
        for j in range(sides):
            F.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
            mids.append((i,j))
    for i,rev in [(0,True),(len(nodes)-1,False)]:
        n=nodes[i];idx=len(V);V.append((n[0],n[1]+YSHIFT,n[2]))
        for j in range(sides):
            f=(idx,i*sides+j,i*sides+(j+1)%sides)
            F.append(f[::-1] if rev else f)
    obj=ac.mesh_object(name,V,F,M if color else M[material],E)
    if color:
        for poly,(i,j) in zip(obj.data.polygons,mids):
            c=sum((Vector(V[k]) for k in poly.vertices),Vector())/len(poly.vertices)
            cz=(nodes[i][2]+nodes[i+1][2])/2
            r=(nodes[i][4]+nodes[i+1][4])/2
            # Broad dorsal and ventral regions; not a claimed fossil pattern.
            poly.material_index=1 if c.z>cz+r*.52 else 2 if c.z<cz-r*.43 else 0
            if c.y-YSHIFT<-1.84:poly.material_index=3
        for poly in obj.data.polygons[len(mids):len(mids)+sides]:poly.material_index=1
        for poly in obj.data.polygons[len(mids)+sides:]:poly.material_index=3
    obj['anatomical_role']=name;obj['construction']='original explicit closed profile loft'
    anatomy.append({'part':name,'path_nodes':nodes,'sides':sides,'closed':True})
    return obj

# Integrated tail, deep torso, compact rising neck and small corrected wedge head.
# Brill & Carpenter Fig3.2 E/F + Fig3.3 only; head 0.49m artist nominal.
loft('continuous_axial_skin',[
 (0,3.00,.99,.006,.007),(0,2.88,1.015,.018,.020),(0,2.64,1.07,.035,.040),
 (0,2.37,1.13,.055,.065),(0,2.08,1.19,.080,.095),(0,1.80,1.25,.112,.127),
 (0,1.53,1.31,.145,.165),(0,1.28,1.37,.18,.205),(0,1.04,1.42,.22,.25),
 (0,.82,1.47,.26,.31),(0,.59,1.51,.305,.37),(0,.35,1.51,.35,.43),
 (0,.10,1.48,.385,.47),(0,-.16,1.44,.395,.49),(0,-.42,1.44,.375,.48),
 (0,-.65,1.49,.335,.43),(0,-.86,1.57,.285,.355),(0,-1.04,1.70,.215,.28),
 (0,-1.18,1.85,.165,.225),(0,-1.32,1.97,.145,.19),
 (0,-1.47,2.065,.165,.17),(0,-1.57,2.075,.164,.165),
 (0,-1.68,2.045,.139,.134),(0,-1.80,2.01,.110,.095),
 (0,-1.90,1.985,.082,.065),(0,-1.97,1.97,.066,.046),
 (0,-2.00,1.97,.044,.032)],sides=20,subdivisions=2,color=True)

for s,label in [(-1,'L'),(1,'R')]:
    # A shaped muscular thigh transitions to calf/ankle, rather than bead joints.
    loft(label+'_hindlimb',[
      (s*.25,.12,1.56,.205,.24),(s*.29,.01,1.38,.22,.245),
      (s*.32,-.14,1.19,.185,.205),(s*.35,-.26,1.00,.14,.15),
      (s*.365,-.20,.84,.112,.12),(s*.375,-.05,.66,.105,.11),
      (s*.38,.09,.48,.083,.09),(s*.38,.13,.30,.066,.067),
      (s*.38,.08,.18,.073,.073),(s*.38,-.02,.10,.10,.065)],
      sides=14,subdivisions=2,material=0)
    loft(label+'_metatarsal_pad',[
      (s*.38,.12,.08,.085,.065),(s*.38,.03,.075,.12,.075),
      (s*.38,-.08,.075,.142,.075),(s*.38,-.18,.07,.13,.065),
      (s*.38,-.24,.065,.095,.055)],sides=14,subdivisions=2,material=0)
    for digit,dx,length,w in [('II',-s*.11,.35,.048),('III',0,.43,.052),('IV',s*.11,.33,.045)]:
        x=s*.38+dx
        toe=loft(label+'_pes_'+digit,[
          (x,-.15,.082,w*1.15,.061),(x+dx*.35,-.26,.063,w,.055),
          (x+dx*.65,-.15-length*.68,.053,w*.88,.047),
          (x+dx*.84,-.15-length*.90,.050,w*.67,.035),
          (x+dx*.92,-.15-length,.047,w*.42,.022)],sides=10,subdivisions=2,material=0)
        # Blunt terminal keratin is a material region, not a detached claw object.
        toe.data.materials.append(M[3])
        nside=10
        for p in toe.data.polygons:
            if p.index>=6*nside:p.material_index=1
    loft(label+'_pes_I_raised_medial',[
       (s*.325,.07,.28,.035,.037),(s*.29,.025,.24,.034,.033),
       (s*.25,-.045,.20,.027,.026),(s*.23,-.085,.19,.015,.016)],sides=8,subdivisions=2,material=3)
    # Forearms and hands stay medial-facing; digits fan along the sagittal plane.
    loft(label+'_forelimb',[
      (s*.235,-.86,1.62,.12,.14),(s*.31,-.78,1.46,.105,.115),
      (s*.385,-.70,1.28,.078,.082),(s*.41,-.78,1.14,.064,.066),
      (s*.43,-.89,1.02,.052,.052),(s*.44,-.965,.94,.046,.045)],sides=12,subdivisions=2,material=0)
    loft(label+'_manus_palm',[
      (s*.44,-.965,.965,.046,.046),(s*.445,-.995,.91,.052,.070),
      (s*.445,-1.005,.85,.049,.084),(s*.445,-1.00,.82,.038,.075)],sides=12,subdivisions=2,material=0)
    # Each finger is independently editable; I and V are visibly shorter.
    fingers=[('I',-1.08,.865,-1.155,.81,.024),('II',-1.065,.84,-1.105,.715,.025),
             ('III',-1.005,.826,-1.01,.675,.026),('IV',-.945,.84,-.919,.72,.022),
             ('V',-.921,.865,-.868,.79,.018)]
    for digit,y,z,ey,ez,r in fingers:
        loft(label+'_manus_'+digit,[(s*.446,y,z,r,r),
           (s*.45,(2*y+ey)/3,(2*z+ez)/3,r*.94,r*.92),
           (s*.447,(y+2*ey)/3,(z+2*ez)/3,r*.78,r*.76),
           (s*.435,ey,ez,r*.46,r*.50)],sides=8,subdivisions=2,material=0)
    # Restrained living eyes and nares embedded in skin, no exposed skull holes.
    loft(label+'_eye',[(s*.149,-1.565,2.115,.018,.021),
         (s*.169,-1.565,2.115,.020,.023),(s*.173,-1.565,2.115,.013,.015)],sides=12,material=4)
    loft(label+'_naris',[(s*.083,-1.868,2.005,.014,.008),
         (s*.09,-1.868,2.005,.014,.008),(s*.093,-1.868,2.005,.009,.005)],sides=10,material=4)
    # Closed thin lip line is supported by the head surface, not an open gape.
    # Sample the actual axial mesh, so thin lips remain embedded rather than
    # assuming an elliptical head surface after its curved-frame transformation.
    lip=[];skin=bpy.data.objects['continuous_axial_skin']
    for y,z in [(-1.975,1.95),(-1.89,1.945),(-1.79,1.947),(-1.68,1.949),(-1.57,1.96)]:
        hit,loc,normal,idx=skin.ray_cast(Vector((s,y+YSHIFT,z)),Vector((-s,0,0)))
        if not hit:raise RuntimeError('Closed lip skin support ray missed')
        lip.append((loc.x+s*.0006,y,z,.003,.003))
    loft(label+'_closed_lip',lip,sides=6,material=4)

# First reproduce r001 exactly; its authored YSHIFT is not contact-centered.
ac.ground_asset(E,center_xy=False)
# r002: measure and fix the actual contact datum, without reshaping the animal.
# All active-scene referenced world vertices are used, not object origins or
# the animal bbox. Every mesh-local vertex then receives the same translation.
origin_cfg=C['origin_repair'];eps=origin_cfg['contact_epsilon_m']
# r001 ground_asset used a common object Z translation. Bake that existing
# world-space datum before the horizontal repair so r002 mesh transforms are
# genuinely identity. This does not add a vertical world-space displacement.
bpy.context.view_layer.update();baseline_ground_transforms={}
for obj in E.all_objects:
    if obj.type!='MESH':continue
    world=obj.matrix_world.copy()
    baseline_ground_transforms[obj.name]=[list(row) for row in world]
    expected_z=origin_cfg['baseline_common_grounding_z_m']
    if any(abs(world[r][c]-((1. if r==c else 0.)+(expected_z if (r,c)==(2,3) else 0.)))>1e-12 for r in range(4) for c in range(4)):
        raise RuntimeError('Unexpected baseline transform; only common known Z grounding may be baked')
    for vertex in obj.data.vertices:vertex.co=world@vertex.co
    obj.matrix_world.identity();obj.data.update()
bpy.context.view_layer.update()
def contact_measurement():
    bpy.context.view_layer.update();points=[];parts={}
    for obj in scene.objects:
        if obj.type!='MESH':continue
        if obj.name not in E.all_objects:raise RuntimeError('Unexpected active-scene mesh outside EXPORT')
        if any(abs(obj.matrix_world[r][c]-(1. if r==c else 0.))>1e-12 for r in range(4) for c in range(4)):
            raise RuntimeError('Origin repair requires identity mesh transforms')
        refs=sorted({i for poly in obj.data.polygons for i in poly.vertices})
        pts=[tuple(obj.matrix_world@obj.data.vertices[i].co) for i in refs]
        points.extend(pts);selected=[p for p in pts if abs(p[2])<=eps]
        if selected:parts[obj.name]=len(set(selected))
    unique=sorted(set(points));lowest=min(p[2] for p in unique)
    if lowest!=0:raise RuntimeError('Expected exact source minimum Z=0')
    contact=[p for p in unique if abs(p[2])<=eps]
    lo=[min(p[i] for p in contact) for i in range(3)];hi=[max(p[i] for p in contact) for i in range(3)]
    return {'epsilon_m':eps,'lowest_z_m':lowest,'referenced_unique_vertices':len(unique),'contact_unique_vertices':len(contact),'contact_min_m':lo,'contact_max_m':hi,'center_xy_m':[(lo[i]+hi[i])/2 for i in range(2)],'contact_parts':parts}
origin_before=contact_measurement()
expected=origin_cfg['expected_pretranslation_center_blender_xy_m']
if any(abs(a-b)>1e-12 for a,b in zip(origin_before['center_xy_m'],expected)):
    raise RuntimeError('Frozen r001 contact center changed; refuse guessed translation')
delta=origin_cfg['uniform_delta_blender_xyz_m']
if any(abs(delta[i]+origin_before['center_xy_m'][i])>1e-12 for i in range(2)) or delta[2]!=0:
    raise RuntimeError('Configured translation does not match selected contact algorithm')
for obj in E.all_objects:
    if obj.type!='MESH':continue
    for vertex in obj.data.vertices:
        vertex.co.x+=delta[0];vertex.co.y+=delta[1];vertex.co.z+=delta[2]
    obj.data.update()
origin_after=contact_measurement()
if any(abs(v)>origin_cfg['posttranslation_center_tolerance_m'] for v in origin_after['center_xy_m']):
    raise RuntimeError('Translated source contact center exceeds frozen tolerance')
root=bpy.data.objects['camptosaurus'];root['representation']='living-reconstruction';root['taxon']='Camptosaurus dispar'
root['size_basis']='5m artistic nominal, not a measured specimen';root['pose_basis']='conservative modern balanced bipedal interpretation'
root['reconstruction_limits']='Skin, colors, exact muscle masses and minor digit articulation are artistic; corrected composite skull rather than one individual.'
source=ac.audit_source(E,12000)
A.output_dir.mkdir(parents=True,exist_ok=True)
meta=ac.export_asset('camptosaurus',{'en':'Camptosaurus dispar — conservative adult','zh':'弯龙（异弯龙启发成年形态）'},'animals',E,
   metadata={'representation':'living-reconstruction','generator_seed':C['seed'],'source_evidence':'Brill/Carpenter Fig3.2 E/F+3.3, Gilmore1912 postcrania only, Carpenter/Wilson2008 Fig23 B-E, Gilmore1909 pes text','greybox':A.greybox},
   output_root=A.output_dir,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
o=A.output_dir/'camptosaurus'
(o/'anatomy-map.json').write_text(json.dumps({'parts':anatomy,'authored_translation_y_m':YSHIFT,'origin_only_uniform_delta_blender_xyz_m':delta,'notes':'Paths are original r001 construction controls before the disclosed r002 uniform origin correction, not fossil measurements; source mesh is editable. Digit names express count not precise reconstructed phalangeal joints.'},indent=2))
(o/'origin-source-report.json').write_text(json.dumps({'revision':'r002','scope':'origin-only','algorithm':'Bake existing common r001 object grounding Z into vertices; active-scene referenced world vertices with abs(BlenderZ)<=epsilon define contact XY extrema. Bake one uniform XY translation in local vertices; identity transforms established.','baseline_ground_transforms_baked':baseline_ground_transforms,'before':origin_before,'uniform_delta_blender_xyz_m':delta,'after':origin_after,'root_and_mesh_transforms':'identity','artistic_geometry_material_pose_scale_changes':False,'float32_note':'World-transform baking and horizontal translation stored in Blender float32 coordinates; exporter may recompute normals with small rounding changes. Decoded final GLB world-space triangle delta audit is authoritative.'},indent=2))
(o/'build-provenance.json').write_text(json.dumps({'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender_version':bpy.app.version_string,'threads':2,'greybox':A.greybox,'from_factory_startup':True,'input_meshes':[],'native_editable':True,'source_audit':source,'exporter_flags_probed':True},indent=2))
print('CAMPTOSAURUS_BUILD_OK',json.dumps({'triangles':meta['triangles'],'bytes':meta['glb_bytes'],'bounds':meta['blender_dimensions_m']}))
