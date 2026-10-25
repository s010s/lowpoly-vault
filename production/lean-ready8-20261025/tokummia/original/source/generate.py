# SPDX-License-Identifier: MIT
"""Original deterministic Tokummia katalepsis living reconstruction.
Blender 4.3.2. No external meshes, reference pixels, rig, or presentation objects.
Rebuild: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
Parameters are authoring conventions, not measurements of a fossil individual.
"""
from pathlib import Path
import sys, json, hashlib, argparse, math
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P={}; C=None; M={}; META={}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

class Part:
    """Editable semantic mesh batching explicitly disconnected anatomical elements."""
    def __init__(self,name,material):self.name=name;self.material=material;self.v=[];self.f=[]
    def add(self,v,f):
        off=len(self.v);self.v.extend(v);self.f.extend(tuple(off+j for j in q) for q in f)
    def tube(self,points,radii,sides=6,aspect=1.0):
        pts=[Vector(p) for p in points];v=[];f=[]
        for i,p in enumerate(pts):
            tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
            ref=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((1,0,0))
            a=tangent.cross(ref).normalized();b=tangent.cross(a).normalized()
            for j in range(sides):
                ang=2*math.pi*j/sides;v.append(tuple(p+radii[i]*(a*math.cos(ang)+b*math.sin(ang)*aspect)))
        f.append(tuple(range(sides-1,-1,-1)))
        for i in range(len(pts)-1):
            for j in range(sides):f.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
        f.append(tuple((len(pts)-1)*sides+j for j in range(sides)))
        self.add(v,f)
    def foil(self,outline,center,thickness):
        # Solid cambered paddle, thin in longitudinal Y and rounded in XZ outline.
        n=len(outline);v=[];f=[]
        for s in [-1,1]:
            v.append((center[0],center[1]+s*thickness,center[2]))
            for p in outline:v.append((p[0],p[1]+s*thickness*.32,p[2]))
        for k in range(2):
            for j in range(n):f.append((k*(n+1),k*(n+1)+1+j,k*(n+1)+1+(j+1)%n))
        for j in range(n):f.append((1+j,1+(j+1)%n,n+2+(j+1)%n,n+2+j))
        self.add(v,f)
    def make(self):
        obj=mesh_object(self.name,self.v,self.f,self.material,C)
        obj['construction']='Original explicit lofts and solid foils; no acquired mesh'
        return obj

def ellipsoid(name,center,radii,mat,n=10,m=6):
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

def shell(sign):
    # A paired curved thin-walled valve, not a solid ellipsoid or flat fossil card.
    rows=P['shell']['longitudinal_rows'];N=P['shell']['arc_sections'];v=[];f=[]
    thickness=P['shell']['thickness_units']
    for inside in [False,True]:
        for y,w,h,zc in rows:
            for j in range(N+1):
                t=P['shell']['open_arc_radians']*j/N
                # Folded rounded valves meet dorsally but remain open ventrally.
                x=sign*(.065+w*math.sin(t)-(thickness if inside else 0)*math.sin(t))
                z=zc+h*math.cos(t)-(thickness if inside else 0)*math.cos(t)
                v.append((x,y,z))
    layer=len(rows)*(N+1)
    for k in [0,1]:
        off=k*layer
        for i in range(len(rows)-1):
            for j in range(N):
                a=off+i*(N+1)+j;f.append((a,a+1,a+N+2,a+N+1))
    boundary=list(range(N+1))+[i*(N+1)+N for i in range(1,len(rows))]+[(len(rows)-1)*(N+1)+j for j in range(N-1,-1,-1)]+[i*(N+1) for i in range(len(rows)-2,0,-1)]
    for j,a in enumerate(boundary):b=boundary[(j+1)%len(boundary)];f.append((a,b,b+layer,a+layer))
    o=mesh_object(('left' if sign<0 else 'right')+'-curved-carapace-valve',v,f,[M['shell'],M['rim'],M['underside']],C)
    for face in o.data.polygons:
        idx=face.index
        face.material_index=2 if (len(rows)-1)*N<=idx<2*(len(rows)-1)*N else 1 if idx>=2*(len(rows)-1)*N else 0
    o['anatomy']='One of two broad dorsal-hinged valves; open underside and anterior aperture'
    return o

def trunk_z(t):return 2.02-.07*t-.75*max(0,(t-.62)/.38)**1.5
def trunk_r(t):return .57*(1-.66*t)+.03

def build():
    global C,M,META
    C=setup_scene('tokummia',P['seed'])
    M={k:make_material(k,v,roughness=.86) for k,v in P['surface']['palette_srgb'].items()}
    shell(-1);shell(1)
    # The dorsal connection is narrow and does not fill the paired ventral opening.
    hinge=Part('dorsal-valve-connection',M['body'])
    hinge.tube([(0,r[0],r[3]+r[2]-.11) for r in P['shell']['longitudinal_rows']],[.095]*len(P['shell']['longitudinal_rows']),6,.6);hinge.make()
    # Continuous flexible trunk with 50 shallow annular expansions, not 50 floating beads.
    count=P['trunk']['paired_stations'];y0,y1=P['trunk']['extent_units'];stations=[y0+(y1-y0)*i/(count-1) for i in range(count)]
    pts=[];r=[]
    for i,y in enumerate(stations):
        t=i/(count-1);dy=(y1-y0)/(count-1)
        for offset,factor in [(-.40,.88),(.05,1.0)]:
            pts.append((0,y+offset*dy,trunk_z(t)));r.append(trunk_r(t)*factor)
    body=Part('continuous-fifty-station-trunk',M['body']);body.tube(pts,r,10,1.0);body.make()
    ellipsoid('head-under-anterior-aperture',(0,-2.32,1.95),(.67,.43,.38),M['underside'],12,6)
    # A small triangular cover and paired lobed anterior organ, deliberately not eyes.
    coverv=[(-.40,-2.76,2.45),(.40,-2.76,2.45),(0,-3.30,2.48),(-.34,-2.74,2.35),(.34,-2.74,2.35),(0,-3.24,2.38)]
    mesh_object('anterior-triangular-cover',coverv,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],M['rim'],C)
    for s in [-1,1]:
        side='left' if s<0 else 'right'
        ellipsoid(side+'-paired-lobed-anterior-organ',(s*.105,-2.84,2.13),(.12,.15,.22),M['underside'],8,5)
        # Short, stout segmented antennules: ring geometry follows one bent chain.
        ant=Part(side+'-short-segmented-antennule',M['appendage'])
        path=[(s*.44,-2.64,2.13),(s*.68,-2.97,2.18),(s*.77,-3.29,2.36),(s*.75,-3.54,2.59),(s*.67,-3.75,2.79)]
        for k in range(len(path)-1):
            p=Vector(path[k]);q=Vector(path[k+1]);rad=.145-.023*k
            ant.tube([p,p.lerp(q,.52),q],[rad,rad*.92,rad*.70],7)
        ant.make()
        # Articulated maxilliped curves clear of antennule and valve rim.
        arm=Part(side+'-articulated-grasping-maxilliped',M['appendage'])
        nodes=[(s*.54,-2.40,1.63),(s*.95,-2.69,1.38),(s*1.34,-3.09,1.38),(s*1.64,-3.55,1.57),(s*1.80,-4.02,1.86),(s*1.95,-4.39,2.03)]
        for k in range(len(nodes)-1):
            p=Vector(nodes[k]);q=Vector(nodes[k+1]);radius=[.22,.23,.23,.22,.23][k]
            arm.tube([p,p.lerp(q,.5),q],[radius*.78,radius,radius*.82],8)
        arm.make()
        palm=Part(side+'-slender-pincer-palm',M['appendage'])
        palm.tube([(s*1.92,-4.28,2.01),(s*1.98,-4.57,2.06),(s*1.99,-4.77,2.09)],[.22,.29,.24],8,.70);palm.make()
        fingers=Part(side+'-open-pincer-fingers-and-two-terminal-teeth',M['tip'])
        fingers.tube([(s*2.15,-4.66,2.10),(s*2.29,-4.98,2.13),(s*2.28,-5.27,2.16),(s*2.10,-5.52,2.18)],[.13,.13,.10,.026],7,.75)
        fingers.tube([(s*1.84,-4.67,2.10),(s*1.60,-4.98,2.13),(s*1.59,-5.29,2.16),(s*1.75,-5.52,2.18)],[.13,.11,.085,.026],7,.75)
        # The outer finger endpoint is terminal tooth one; this fork is tooth two.
        fingers.tube([(s*2.23,-5.34,2.16),(s*2.01,-5.37,2.18)],[.075,.023],5)
        fingers.make()
        # Simplified superficial mandible and following two small mouthpart pairs.
        mouths=Part(side+'-mandible-and-two-small-mouthpart-pairs',M['underside'])
        mouths.tube([(s*.39,-2.56,1.83),(s*.23,-2.79,1.70),(s*.08,-2.87,1.76)],[.17,.15,.06],7)
        for k in range(2):mouths.tube([(s*.29,-2.31+k*.20,1.63),(s*.48,-2.47+k*.20,1.45),(s*.23,-2.62+k*.20,1.43)],[.10,.085,.045],6)
        mouths.make()
        walks=Part(side+'-eight-anterior-walking-branches',M['appendage'])
        claws=Part(side+'-walking-terminal-claws',M['tip'])
        backlegs=Part(side+'-posterior-slender-inner-branches',M['appendage'])
        paddles=Part(side+'-fifty-serial-outer-flaps',M['paddle'])
        for i,y in enumerate(stations):
            t=i/(count-1);z=trunk_z(t);rr=trunk_r(t)
            if i<P['trunk']['anterior_walking_pairs']:
                # Leg-root order retained; each branch is narrow longitudinally.
                ext=1.66+.18*math.sin(i*.40)
                yp=y-.14+.025*i
                walks.tube([(s*rr*.74,y,z-.24),(s*1.02,y-.04,1.10),(s*ext,yp,.58),(s*(ext+.35),yp-.10,.19)],[.10,.10,.08,.055],6,.70)
                claws.tube([(s*(ext+.35),yp-.10,.19),(s*(ext+.43),yp-.19,.055),(s*(ext+.49),yp-.27,.015)],[.060,.046,.022],5)
                # Retain a secondary small outer branch, not only modern-dec apod legs.
                plen=.48+.04*i
                baseX=rr*.80; tipX=1.10+.025*i;bottom=z-.65-plen*.32
            else:
                taper=1-.66*((i-8)/(count-9))
                ext=1.02*taper+.25
                backlegs.tube([(s*rr*.70,y,z-.20),(s*(rr+.32*taper),y+.015,z-.61*taper),(s*(rr+.57*taper),y+.04,z-1.13*taper)],[.065*taper+.02,.052*taper+.02,.025],5,.70)
                # Lobate paddles begin around pair nine, then diminish along the trunk.
                baseX=rr*.76;tipX=rr+ext;bottom=z-1.34*taper
            bx=baseX;tx=tipX;rootz=z-.16
            # At each station the foil is a closed flattened lobe with its own gap.
            outline=[(s*bx,y,rootz),(s*(bx+(tx-bx)*.68),y-.055,rootz-.17),(s*tx,y-.050,(rootz+bottom)/2),(s*(tx-.07),y+.015,bottom+.10),(s*(tx-.23),y+.056,bottom),(s*(bx+.12),y+.055,rootz-.35)]
            paddles.foil(outline,(s*(bx+(tx-bx)*.65),y+.005,(rootz+bottom)*.5),.020 if i<30 else .018)
        walks.make();claws.make();backlegs.make();paddles.make()
    # Small terminal plate with two separate narrow caudal rami, no fish/lobster fan.
    tail=Part('small-terminal-plate',M['body'])
    tail.tube([(0,6.02,trunk_z(1)),(0,6.26,1.17),(0,6.43,1.13)],[.22,.24,.18],8,.65);tail.make()
    for s in [-1,1]:
        ramus=Part(('left' if s<0 else 'right')+'-narrow-caudal-ramus',M['appendage'])
        ramus.tube([(s*.14,6.31,1.15),(s*.30,6.61,1.05),(s*.53,6.95,.96),(s*.65,7.17,.92)],[.14,.14,.095,.026],7,.50);ramus.make()
    # Preserve selected physical total length. The root is walking-footprint center.
    allvs=[v for o in C.all_objects if o.type=='MESH' for v in o.data.vertices]
    ymin=min(v.co.y for v in allvs);ymax=max(v.co.y for v in allvs);low=min(v.co.z for v in allvs)
    factor=P['nominal_total_length_m']/(ymax-ymin)
    contacts=[v.co.y for o in C.all_objects if o.type=='MESH' and 'walking-terminal-claws' in o.name for v in o.data.vertices if v.co.z<.08]
    footcenter=(min(contacts)+max(contacts))/2
    for v in allvs:v.co=Vector((v.co.x*factor,(v.co.y-footcenter)*factor,(v.co.z-low)*factor))
    C['body_center_above_datum_m']=(2.02-low)*factor
    C['footprint_center_original_y_units']=footcenter
    META={'paired_trunk_limb_stations':count,'count_convention':'50 paired trunk limb stations excludes grasping maxillipeds, antennules, mouthparts and caudal rami. Approximation to about 50 in cited account, not an observed exact individual count.','anterior_walking_pairs':P['trunk']['anterior_walking_pairs'],'posterior_inner_branch_pairs':count-P['trunk']['anterior_walking_pairs'],'outer_flap_pairs':count,'paired_shell_valves':2,'grasping_maxillipeds':2,'antennule_pairs':1,'caudal_rami':2,'nominal_length_m':P['nominal_total_length_m'],'body_center_above_datum_m':C['body_center_above_datum_m'],'scale_factor_from_author_units':factor,'grounding':'Lowest anterior walking terminal claw at Z=0; root at their longitudinal footprint center. Paired graspers do not bear weight.','uncertain':'Living depth, soft tissues, articulation/pose and colors interpreted. No prominent eyes, no claim of proven blindness.'}
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
    dump(out/'technical.json',{'asset_id':'tokummia','revision':'r001','source':source,'glb':glb,'source_export_bounds_delta_m':delta,'blender_version':bpy.app.version_string,'exporter_version':io_scene_gltf2.bl_info['version'],'consumer_three_version':'0.180.0','consumer_scope':'CPU parse to be independently recorded; GPU not tested','export_options':flags,'source_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(out/'model.blend'),'anatomy':META,'scientific_scope':P['interpretation'],'semantic_parts':'Original paired curved shell panels, tubular segmented trunk, articulated pincers, antennules and superficial mouthparts, batched but separately editable limb classes, paired narrow rami.'})
if __name__=='__main__':main()
