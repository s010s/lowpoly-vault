# SPDX-License-Identifier: MIT
"""Original Callichimaera perplexa r001, deterministic editable static reconstruction.
Rebuild: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
Author dimensions use millimeters, converted to meters before saving/exporting.
No acquired meshes, reconstructed source mesh, image pixels, or procedural-only materials.
"""
from pathlib import Path
import sys,json,hashlib,argparse,math
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
P={};C=None;M={};META={}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
class Part:
    def __init__(self,name,material):self.name=name;self.material=material;self.v=[];self.f=[]
    def add(self,v,f):
        offset=len(self.v);self.v.extend(v);self.f.extend(tuple(offset+x for x in face) for face in f)
    def tube(self,points,radii,sides=8,aspect=1):
        points=[Vector(p) for p in points];v=[];f=[]
        for i,p in enumerate(points):
            tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
            ref=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((1,0,0))
            a=tangent.cross(ref).normalized();b=tangent.cross(a).normalized()
            for j in range(sides):
                angle=2*math.pi*j/sides;v.append(tuple(p+radii[i]*(a*math.cos(angle)+b*math.sin(angle)*aspect)))
        f.append(tuple(range(sides-1,-1,-1)))
        for k in range(len(points)-1):
            for j in range(sides):f.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
        f.append(tuple((len(points)-1)*sides+j for j in range(sides)));self.add(v,f)
    def foil(self,outline,center,thickness):
        # Closed convex cambered paddle: thin in Z, outline authored in XY.
        n=len(outline);v=[];f=[]
        for sign in [-1,1]:
            v.append((center[0],center[1],center[2]+sign*thickness))
            for p in outline:v.append((p[0],p[1],p[2]+sign*thickness*.30))
        for k in range(2):
            for j in range(n):f.append((k*(n+1),k*(n+1)+1+j,k*(n+1)+1+(j+1)%n))
        for j in range(n):f.append((1+j,1+(j+1)%n,n+2+(j+1)%n,n+2+j))
        self.add(v,f)
    def make(self):
        o=mesh_object(self.name,self.v,self.f,self.material,C);o['construction']='Original explicit loft/profile geometry';return o

def ellipsoid(name,center,radii,mat,n=16,m=9):
    v=[(center[0],center[1],center[2]-radii[2])];f=[]
    for k in range(1,m):
        a=-math.pi/2+math.pi*k/m
        for j in range(n):
            t=2*math.pi*j/n;v.append((center[0]+radii[0]*math.cos(a)*math.cos(t),center[1]+radii[1]*math.cos(a)*math.sin(t),center[2]+radii[2]*math.sin(a)))
    v.append((center[0],center[1],center[2]+radii[2]));end=len(v)-1
    for j in range(n):f.append((0,1+(j+1)%n,1+j))
    for k in range(m-2):
        for j in range(n):a=1+k*n+j;b=1+k*n+(j+1)%n;f.append((a,b,b+n,a+n))
    for j in range(n):f.append((end,end-n+j,end-n+(j+1)%n))
    return mesh_object(name,v,f,mat,C)

def carapace():
    # Broad deliberate fusiform planes. Reduced dorsal height at named grooves is
    # actual geometry, not a painted line. The small frontal rostrum is separate.
    rows=[(-3.55,.53,.54),(-3.3,1.3,.72),(-2.95,1.8,.91),(-2.4,2.13,1.05),(-1.9,2.28,1.13),(-1.4,2.41,1.17),(-.9,2.51,1.20),(-.4,2.58,1.22),(.1,2.6,1.23),(.65,2.56,1.20),(1.25,2.43,1.12),(1.85,2.2,.98),(2.45,1.87,.81),(3.0,1.45,.64),(3.55,.94,.47),(4.0,.52,.29),(4.25,.20,.15)]
    N=24;v=[];f=[]
    for y,w,h in rows:
        for j in range(N):
            t=2*math.pi*j/N;x=w*math.sin(t);c=math.cos(t)
            z=.90+(h if c>=0 else .30*h)*c
            if c>0:
                cervical_y=-1.15+.52*abs(x)
                cervical=.21*math.exp(-((y-cervical_y)/.32)**2)*c
                branch_x=1.35-.22*max(0,y)
                branch=.15*math.exp(-((abs(x)-branch_x)/.24)**2)*math.exp(-((y-1.0)/1.65)**4)*c
                axial=.10*math.exp(-(x/.27)**2)*max(0,1-abs(y)/4.4)
                z+=axial-cervical-branch
            v.append((x,y,z))
    front_center=len(v);v.append((0,rows[0][0],.90))
    for j in range(N):f.append((front_center,(j+1)%N,j))
    for i in range(len(rows)-1):
        for j in range(N):f.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
    back_center=len(v);v.append((0,rows[-1][0],.90))
    for j in range(N):f.append((back_center,(len(rows)-1)*N+j,(len(rows)-1)*N+(j+1)%N))
    o=mesh_object('fusiform-carapace-with-sculpted-grooves',v,f,M['carapace'],C)
    o['anatomy']='Carapace shell 5.2 mm maximum width; shell plus bifid rostrum 8.5 mm total nominal length'
    rostrum=Part('bifid-rostrum',M['carapace'])
    # Two broad short branches join the continuous front shell, leaving a notch.
    for s in [-1,1]:
        rostrum.tube([(s*.26,-3.35,1.45),(s*.30,-3.75,1.46),(s*.29,-4.25,1.50)],[.25,.19,.07],6,.65)
    rostrum.make()
    ridge=Part('subtle-axial-and-postfrontal-ridges',M['ridge'])
    ridge_path=[]
    for y,w,h in rows[:-1]:
        z=.90+h+.10*max(0,1-abs(y)/4.4)-.21*math.exp(-((y+1.15)/.32)**2)+.018
        ridge_path.append((0,y,z))
    ridge.tube(ridge_path,[.055]*len(ridge_path),6,.65)
    ridge.make()

def limb_chain(name,nodes,radii,mat,aspect=.70):
    p=Part(name,mat)
    for i in range(len(nodes)-1):
        a,b=Vector(nodes[i]),Vector(nodes[i+1]);r=radii[i]
        p.tube([a,a.lerp(b,.19),a.lerp(b,.72),b],[r*.72,r,r*.92,r*.72],8,aspect)
    return p

def build():
    global C,M,META
    C=setup_scene('callichimaera',P['seed']);M={k:make_material(k,v,roughness=.78 if k=='eye' else .86) for k,v in P['surface']['palette_srgb'].items()}
    carapace()
    # Flattened sternum and folded pleon are separate editable structures.
    stern=Part('ventral-sternal-plates',M['underside'])
    for y,rx,ry in [(-2.1,.65,1.05),(-.45,1.37,.68),(.9,1.46,.66),(2.2,1.06,.57)]:
        stern.foil([(-rx*.65,y-ry,.48),(-rx,y-.15,.46),(-rx*.75,y+ry,.45),(0,y+ry+.1,.43),(rx*.75,y+ry,.45),(rx,y-.15,.46),(rx*.65,y-ry,.48)],(0,y,.44),.23)
    stern.make()
    stalks=Part('short-unprotected-eye-peduncles',M['limb'])
    antennae=[Part('paired-first-antennae',M['limb']),Part('paired-second-antennae',M['limb'])]
    for s in [-1,1]:
        side='left' if s<0 else 'right'
        def pt(x,y,z):return (s*x,y,z)
        stalks.tube([pt(.65,-3.16,1.25),pt(1.03,-3.50,1.38),pt(1.38,-3.63,1.50)],[.27,.28,.32],8)
        eye=ellipsoid(side+'-large-unprotected-compound-eye',pt(1.69,-3.76,1.59),(.89,.86,.91),M['eye'],20,12)
        eye['anatomy']='Subglobular cornea; coarse faceting abstracts compound facets, no enclosing orbit'
        antennae[0].tube([pt(.38,-3.52,1.23),pt(.53,-4.06,1.34),pt(.67,-4.54,1.67),pt(.61,-4.96,1.84)],[.09,.08,.055,.028],6)
        antennae[1].tube([pt(.68,-3.43,1.11),pt(.83,-4.01,1.17),pt(1.0,-4.43,1.44),pt(1.10,-4.78,1.59)],[.075,.065,.045,.027],6)
        # P1: sturdy wrist connected to broad palm, one approximately right-angle
        # fixed finger and one opposed mobile dactyl. Exactly two finger tips.
        # CAL-P1-001 repair: transverse stout manus and a strongly deflected pollex.
        # Wrist position is unchanged; centerline-angle proxy is documented separately.
        arm=limb_chain(side+'-P1-cheliped-arm',[pt(1.80,-.83,.70),pt(2.55,-1.58,.66),pt(3.45,-2.34,.83),pt(3.69,-3.16,1.08)],[.37,.45,.47],M['limb']);arm.make()
        palm=Part(side+'-P1-stout-spanner-manus',M['limb'])
        palm.foil([pt(3.30,-2.99,1.09),pt(3.28,-3.51,1.10),pt(3.67,-3.96,1.14),pt(4.45,-4.15,1.17),pt(5.12,-3.83,1.12),pt(5.35,-3.30,1.08),pt(4.92,-2.87,1.03),pt(4.04,-2.84,1.04)],pt(4.30,-3.22,1.10),.43);palm.make()
        fixed=Part(side+'-P1-single-fixed-deflected-finger',M['claw_tip'])
        fixed.tube([pt(3.70,-3.70,1.18),pt(3.65,-4.20,1.24),pt(3.49,-4.85,1.34),pt(3.35,-5.40,1.43),pt(3.43,-5.76,1.49)],[.43,.36,.25,.14,.04],8,.70);fixed.make()
        moving=Part(side+'-P1-single-mobile-dactyl',M['claw_tip'])
        moving.tube([pt(5.03,-3.54,1.13),pt(5.53,-4.08,1.21),pt(5.62,-4.70,1.33),pt(5.36,-5.28,1.41),pt(4.91,-5.65,1.47)],[.28,.24,.19,.11,.035],8,.75);moving.make()
        # P2/P3 broad propodus and dactylus, not an extra tail or leg pair.
        for n,nodes,radii,prop,pc,dact,dc in [
            (2,[(2.35,.13,.72),(3.90,-.27,.65),(5.63,-.22,.67),(6.30,.13,.64)],[.34,.39,.38],[(6.15,-.20,.65),(6.67,-.35,.65),(7.68,.04,.65),(8.04,.62,.62),(7.70,1.04,.61),(6.77,.86,.63),(6.20,.53,.64)],(7.12,.34,.64),[(7.81,.51,.62),(8.34,.65,.61),(8.94,1.40,.57),(9.18,2.29,.51),(9.12,2.72,.48),(8.45,2.23,.54),(7.87,1.51,.60),(7.61,.96,.62)],(8.39,1.50,.58)),
            (3,[(2.04,2.08,.70),(3.58,2.15,.67),(4.83,2.64,.61),(5.24,3.24,.56)],[.31,.35,.33],[(5.03,3.02,.56),(5.49,2.93,.56),(6.28,3.57,.53),(6.67,4.45,.49),(6.34,4.89,.46),(5.73,4.48,.50),(5.22,3.78,.54)],(5.86,3.93,.52),[(6.34,4.40,.49),(6.92,4.60,.48),(7.15,5.38,.43),(7.06,6.29,.38),(6.63,7.08,.32),(6.30,6.64,.37),(5.98,5.68,.42),(6.01,4.94,.47)],(6.55,5.56,.42))]:
            p=limb_chain(side+f'-P{n}-paddle-leg',[(s*x,y,z) for x,y,z in nodes],radii,M['paddle'],.62)
            p.foil([(s*x,y,z) for x,y,z in prop],(s*pc[0],pc[1],pc[2]),.20)
            p.foil([(s*x,y,z) for x,y,z in dact],(s*dc[0],dc[1],dc[2]),.16)
            o=p.make();o['anatomy']='One paddle leg with flattened propodus and dactylus'
        # P4/P5 narrow, posterior and subdorsal. P5 distinctly smaller.
        for n,nodes,radii in [
            (4,[(.77,3.59,1.13),(1.47,4.23,1.11),(1.72,5.20,.95),(1.79,6.17,.69),(2.10,6.90,.40)],[.18,.18,.15,.115]),
            (5,[(.89,3.48,1.27),(2.07,3.78,1.25),(2.36,4.47,1.10),(2.29,5.24,.79)],[.145,.14,.10])]:
            leg=limb_chain(side+f'-P{n}-reduced-posterior-leg',[(s*x,y,z) for x,y,z in nodes],radii,M['limb'],.90)
            tip=Vector(nodes[-1]);prev=Vector(nodes[-2]);direc=(tip-prev).normalized();end=tip+direc*(.45 if n==4 else .32)
            leg.tube([pt(*tip),pt(*end)],[.09 if n==4 else .075,.026],6,.80);leg.make()
        # Elongate pediform Mxp3 remain below the front carapace, not extra P legs.
        mxp=limb_chain(side+'-pediform-third-maxilliped',[pt(.50,-.30,.32),pt(1.00,-1.18,.28),pt(.97,-2.14,.30),pt(.63,-2.78,.39),pt(.26,-2.88,.46)],[.18,.20,.16,.12],M['underside'],.78);mxp.make()
    stalks.make()
    for a in antennae:a.make()
    # Six symmetric unfused pleonal plates, folded under the posterior body.
    pleon=Part('six-segment-symmetric-folded-pleon',M['underside'])
    coords=[(4.18,.97,.81),(4.56,.83,.86),(4.91,.61,.80),(4.91,.31,.69),(4.52,.12,.59),(4.11,.09,.46)]
    for i,(y,z,w) in enumerate(coords):
        # Interlocking beveled broad plates; no lateral ramus or uropodal fan.
        ry=.23 if i<3 else .27
        pleon.foil([(-w*.72,y-ry,z),(-w,y-.06,z),(-w*.86,y+ry,z),(0,y+ry+.05,z+.04),(w*.86,y+ry,z),(w,y-.06,z),(w*.72,y-ry,z)],(0,y,z+.03),.13)
    pleon.make()
    telson=Part('small-terminal-pleonal-telson',M['underside'])
    telson.foil([(-.38,3.98,.09),(-.37,3.66,.08),(0,3.40,.07),(.37,3.66,.08),(.38,3.98,.09)],(0,3.77,.08),.09);telson.make()
    # Physical dimensions are preserved, never normalized to total limb span.
    vs=[v for o in C.all_objects if o.type=='MESH' for v in o.data.vertices];low=min(v.co.z for v in vs);factor=P['author_unit_m']
    for v in vs:v.co=Vector((v.co.x*factor,v.co.y*factor,(v.co.z-low)*factor))
    META={'nominal_carapace_length_m':.0085,'nominal_carapace_width_m':.0052,'scale_scope':'Shell and rostral forks; excludes limbs, eyes and exposed pleon','P1_pairs':1,'P2_P3_large_paddle_pairs':2,'P4_P5_reduced_pairs':2,'P5_smallest':True,'eye_pairs':1,'antenna_pairs':2,'third_maxilliped_pairs':1,'pleon_segments':6,'telsons':1,'uropods':0,'pose':'Static symmetric spread-swimming, limb joint angles interpretive','origin':'Mid-carapace horizontal coordinate, lowest exported surface at Z=0; not a walking ground contact','color':'Original artistic muted palette, not fossil stains','soft_volume':'Interpretive','anatomy_detail_scope':'Coarse compound-eye facets and simplified nonreproductive ventral anatomy','author_units_to_m':factor,'datum_shift_m':-low*factor}
    bpy.context.view_layer.update();return C
def main():
    global P
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    P=json.loads((HERE/'params.json').read_text());col=build();policy=P['geometry_policy']
    source=audit_source(col,policy['max_triangles']);source['authored_vertices']=sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH');source['evaluated_vertices']=source['authored_vertices']
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene.render.filepath='//';bpy.context.scene['generator']='source/generate.py';bpy.context.scene['scientific_scope']=P['interpretation'];bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(flags)-available:raise RuntimeError('Missing glTF exporter options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    glb=audit_glb(out/'model.glb',policy['max_triangles'],policy['max_materials'],policy['max_primitives']);glb['file']='model.glb'
    b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][s][i]-e[i]) for s,e in [('min',emin),('max',emax)] for i in range(3))
    if glb['errors'] or delta>1e-5 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>policy['max_glb_bytes']:raise RuntimeError('Source/export audit failed: '+str(glb['errors']))
    import io_scene_gltf2
    dump(out/'technical.json',{'asset_id':'callichimaera','revision':'r001','source':source,'glb':glb,'source_export_bounds_delta_m':delta,'blender_version':bpy.app.version_string,'exporter_version':io_scene_gltf2.bl_info['version'],'consumer_three_version':'0.180.0','consumer_scope':'CPU parse to be independently recorded; GPU not tested','export_options':flags,'source_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(out/'model.blend'),'anatomy':META,'scientific_scope':P['interpretation'],'semantic_parts':'Original fusiform shell, integrated rostral forks, large unprotected eyes, two antenna pairs, spanner claws P1, paddle legs P2/P3, reduced legs P4/P5, pediform mouthparts and symmetric folded pleon.'})
if __name__=='__main__':main()
