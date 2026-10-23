# SPDX-License-Identifier: MIT
"""Original Fleurantia r001 reconstruction. Run Blender with -- --output DIR.
Standalone: only params.json and bundled deps are loaded. No reference images are imported.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
P=json.loads((BASE/'params.json').read_text())

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path,obj): Path(path).parent.mkdir(parents=True,exist_ok=True); Path(path).write_text(json.dumps(obj,indent=2)+'\n')
class Mesh:
    def __init__(self): self.v=[]; self.f=[]; self.tags=[]
    def add(self,v,f,tag=''):
        k=len(self.v); self.v.extend([tuple(p) for p in v]); self.f.extend([tuple(k+i for i in face) for face in f]); self.tags.append((tag,k,len(self.v)))
    def object(self,name,mat,collection):
        obj=mesh_object(name,self.v,self.f,mat,collection)
        for tag,a,b in self.tags:
            if tag:
                group=obj.vertex_groups.get(tag) or obj.vertex_groups.new(name=tag); group.add(list(range(a,b)),1,'REPLACE')
        return obj

def tube(mesh, points, radii, tag, sides=6):
    pts=[Vector(p) for p in points]; v=[]; f=[]
    for i,p in enumerate(pts):
        tangent=(pts[min(len(pts)-1,i+1)]-pts[max(0,i-1)]).normalized()
        ref=Vector((0,0,1)) if abs(tangent.z)<.88 else Vector((0,1,0))
        u=tangent.cross(ref).normalized(); w=tangent.cross(u).normalized()
        for j in range(sides):
            t=2*math.pi*j/sides; v.append(p+radii[i]*(u*math.cos(t)+w*math.sin(t)))
    for i in range(len(pts)-1):
        for j in range(sides): f.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    f.append(tuple(reversed(range(sides)))); f.append(tuple((len(pts)-1)*sides+j for j in range(sides)))
    mesh.add(v,f,tag)

def sphere(mesh, center, radii, tag, rows=8, columns=16):
    c=Vector(center); v=[c+Vector((0,0,radii[2]))]; f=[]
    for i in range(1,rows):
        t=math.pi*i/rows
        for j in range(columns):
            a=2*math.pi*j/columns
            v.append(c+Vector((radii[0]*math.sin(t)*math.cos(a),radii[1]*math.sin(t)*math.sin(a),radii[2]*math.cos(t))))
    bottom=len(v); v.append(c-Vector((0,0,radii[2])))
    for j in range(columns): f.append((0,1+j,1+(j+1)%columns))
    for i in range(rows-2):
        a=1+i*columns; b=a+columns
        for j in range(columns): f.append((a+j,b+j,b+(j+1)%columns,a+(j+1)%columns))
    a=1+(rows-2)*columns
    for j in range(columns): f.append((a+j,bottom,a+(j+1)%columns))
    mesh.add(v,f,tag)

# s, half-width, upper profile, lower profile. X axis nose=-L/2.
PROFILE=[(0,.0006,-.0090,-.0110),(.025,.0020,-.0070,-.0125),(.07,.0043,-.0030,-.014),(.12,.0072,.0030,-.015),(.18,.0105,.0100,-.016),(.25,.0134,.0165,-.0175),(.34,.0148,.0207,-.0190),(.44,.015,.023,-.019),(.54,.0143,.0225,-.0183),(.63,.0125,.0197,-.0168),(.72,.0093,.0160,-.0138),(.80,.0059,.0127,-.0090),(.86,.0037,.0120,-.0030),(.90,.0024,.0145,.003),(.945,.0015,.021,.012),(.985,.00045,.0265,.0240),(1,.00025,.029,.028)]
L=P['length']
def profile(s):
    for i in range(len(PROFILE)-1):
        a,b=PROFILE[i:i+2]
        if a[0]<=s<=b[0]:
            t=(s-a[0])/(b[0]-a[0]); return tuple(a[j]*(1-t)+b[j]*t for j in (1,2,3))
    return PROFILE[-1][1:]
def surface(s,theta,offset=0):
    width,top,bottom=profile(s); c=(top+bottom)/2; h=(top-bottom)/2
    return Vector(((s-.5)*L,(width+offset)*math.cos(theta),c+(h+offset)*math.sin(theta)))
def median(mesh,tag,outline,thickness=.00065):
    # Outline lives in X/Z; closed two-sided thin volume. Convex fan centre is interior.
    n=len(outline); coords=[((s-.5)*L,z) for s,z in outline]
    cx=sum(p[0] for p in coords)/n; cz=sum(p[1] for p in coords)/n
    v=[(cx,-thickness,cz),(cx,thickness,cz)]
    for y in (-thickness,thickness): v.extend((x,y,z) for x,z in coords)
    f=[]
    for i in range(n):
        j=(i+1)%n; f.extend([(0,2+i,2+j),(1,2+n+j,2+n+i),(2+i,2+n+i,2+n+j,2+j)])
    mesh.add(v,f,tag)
def paired(mesh,tag,side,sections):
    # Loft with fleshy base, lanceolate flattened ray-supported blade; not a filament.
    # station tuple: body s, outward Y distance, Z, lateral width, thickness
    pts=[Vector(((s-.5)*L,side*y,z)) for s,y,z,w,h in sections]
    v=[]; f=[]; sides=10
    for i,(s,y,z,width,height) in enumerate(sections):
        tang=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized(); u=Vector((-tang.y,tang.x,0)).normalized(); w=tang.cross(u).normalized()
        for j in range(sides):
            theta=2*math.pi*j/sides; v.append(pts[i]+u*width*math.cos(theta)+w*height*math.sin(theta))
    for i in range(len(sections)-1):
        for j in range(sides): f.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    f.extend([tuple(reversed(range(sides))),tuple((len(sections)-1)*sides+j for j in range(sides))]); mesh.add(v,f,tag)

def build(out):
    col=setup_scene('fleurantia',seed=P['seed']); root=bpy.data.objects[col['asset_root']]
    root['authoring_forward']='-X'; root['origin']='Swimming midbody mounting point, not ground contact'
    root['reconstruction']='Conservative whole living Fleurantia; color, thickness and fin pose inferred'
    colors=P['palette_srgb']; mats=[make_material(name,value,roughness=.78 if name!='Eye' else .26) for name,value in colors.items()]
    dorsal,flank,belly,fin,detail,eye=mats
    body=Mesh(); rings=49; sides=32
    for i in range(rings):
        s=i/(rings-1)
        for j in range(sides): body.v.append(tuple(surface(s,2*math.pi*j/sides)))
    for i in range(rings-1):
        for j in range(sides): body.f.append((i*sides+j,(i+1)*sides+j,(i+1)*sides+(j+1)%sides,i*sides+(j+1)%sides))
    body.f.extend([tuple(reversed(range(sides))),tuple((rings-1)*sides+j for j in range(sides))])
    obj=body.object('Body_head_and_ascending_caudal_axis',[dorsal,flank,belly],col)
    for poly in obj.data.polygons:
        p=poly.center; s=p.x/L+.5; w,t,b=profile(min(1,max(0,s))); ratio=(p.z-(t+b)/2)/max(.00001,(t-b)/2)
        poly.material_index=0 if ratio>.48 else 2 if ratio<-.52 else 1
    obj['anatomy']='elongate tapered snout; moderately deep trunk; thin ascending heterocercal axial lobe'
    fins=Mesh(); detail_mesh=Mesh(); scales=Mesh(); eye_rings=Mesh(); eyes=Mesh()
    d1=[(.455,.021),(.475,.030),(.505,.033),(.535,.032),(.55,.028),(.536,.024),(.510,.0215)]
    d2=[(.594,.019),(.622,.029),(.660,.038),(.703,.043),(.742,.0435),(.781,.039),(.815,.032),(.839,.022),(.825,.013),(.785,.0125),(.735,.0145),(.68,.0175),(.63,.019)]
    anal=[(.713,-.012),(.747,-.022),(.789,-.026),(.829,-.025),(.850,-.021),(.814,-.019),(.775,-.014)]
    tail=[(.870,.007),(.903,.014),(.949,.021),(.999,.0283),(.971,.016),(.951,.005),(.930,-.007),(.907,-.013),(.880,-.011),(.851,-.007)]
    for tag,outline in [('First_dorsal_separate',d1),('Second_dorsal_enlarged_separate',d2),('Anal_small_separate',anal),('Heterocercal_caudal_separate',tail)]: median(fins,tag,outline)
    # Ray ridges are original surface cues; never internal bones on a living fish.
    rays=[('D1',(.484,.023),d1[1:6]),('D2',(.664,.020),d2[1:9]),('Anal',(.749,-.014),anal[1:6]),('Caudal',(.878,.006),tail[2:9])]
    for tag,(s0,z0),ends in rays:
        for i,(s1,z1) in enumerate(ends):
            for side in (-1,1):
                a=Vector(((s0-.5)*L,side*.00084,z0)); b=Vector(((s1-.5)*L,side*.00084,z1)); b=a+(b-a)*.93
                tube(detail_mesh,[a,a.lerp(b,.5),b],[.00012,.00013,.00010],tag+'_ray_'+str(i),sides=5)
    for side,name in [(-1,'near'),(1,'far')]:
        pec=[(.255,.010,-.011,.0035,.0028),(.29,.015,-.016,.0054,.0020),(.345,.023,-.022,.0054,.00125),(.405,.027,-.028,.0039,.00075),(.46,.030,-.0308,.0004,.00035)]
        pel=[(.55,.010,-.0145,.003,.0020),(.585,.014,-.020,.0043,.0015),(.635,.019,-.026,.0038,.0008),(.69,.022,-.0305,.0022,.0005),(.735,.021,-.031,.0004,.0003)]
        paired(fins,'Pectoral_'+name,side,pec); paired(fins,'Pelvic_'+name,side,pel)
        for tag,sects in [('Pectoral',pec),('Pelvic',pel)]:
            for off in (-.0015,0,.0015):
                pts=[((s-.5)*L+off,side*y,z-.001) for s,y,z,w,h in sects[1:-1]]
                tube(detail_mesh,pts,[.00011]*len(pts),tag+'_rays_'+name,sides=5)
        # Closed-mouth seam and curved opercular surface boundary.
        mouth=[]
        for s in (.014,.045,.08,.115,.15):
            w,t,b=profile(s); mouth.append(((s-.5)*L,side*w*.95,b+(t-b)*.27))
        tube(detail_mesh,mouth,[.00015]*len(mouth),'Closed_mouth_'+name,sides=6)
        operc=[]
        for s,theta in [(.214,.95),(.239,.57),(.252,.15),(.253,-.28),(.242,-.62),(.223,-.84)]:
            p=surface(s,theta if side==1 else math.pi-theta,.00018); operc.append(p)
        tube(detail_mesh,operc,[.00016]*len(operc),'Operculum_'+name,sides=6)
        # Modest eyes; the ring is subdued and the iris/pupil nearly black.
        s=.137; w,t,b=profile(s); z=-.0016; y=side*(w*.98)
        sphere(eye_rings,((s-.5)*L,y,z),(.0028,.0010,.0027),'Orbital_margin_'+name)
        sphere(eyes,((s-.5)*L,y+side*.0007,z),(.00195,.0009,.0019),'Eye_'+name)
        # Rhomboidal original scale cues on trunk, not a photo texture or anatomical bones.
        for k in range(24):
            s=.285+k*.022
            for j in range(9):
                theta=-.47+j*.135+(k%2)*.0675
                if side<0: theta=math.pi-theta
                ds=.0100; dt=.068
                if s>.77: ds=.008
                corners=[surface(s-ds,theta,.00010),surface(s,theta-dt,.00010),surface(s+ds,theta,.00010),surface(s,theta+dt,.00010)]
                center=surface(s,theta,.00036)
                # Thin closed diamond cap, bottom lies just inside the body.
                bottom=surface(s,theta,-.00011)
                scales.add(corners+[center,bottom],[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(1,0,5),(2,1,5),(3,2,5),(0,3,5)],'Scale_cues_'+name)
    fins.object('Separated_median_and_paired_fins',fin,col)
    scales.object('Modest_original_flank_scale_cues',flank,col)
    detail_mesh.object('External_fin_rays_and_closed_face_seams',detail,col)
    eye_rings.object('Subdued_orbital_margins',belly,col)
    eyes.object('Small_closed_surface_eyes',eye,col)
    bpy.context.view_layer.update()
    out.mkdir(parents=True,exist_ok=True)
    # Canonical helper exports into a private construction folder. Final names are declared from the beginning.
    stage=out/'_build'; stage.mkdir(exist_ok=True)
    record=export_asset('fleurantia',{'en':'Fleurantia','zh':'Fleurantia 古肺鱼'},'animals',col,
        metadata={'description':{'en':'Conservative whole living reconstruction of Late Devonian Fleurantia, with a small first dorsal, enlarged separate second dorsal, separate small anal and heterocercal tail.','zh':'晚泥盆世 Fleurantia 完整活体保守复原，保留独立小第一背鳍、大第二背鳍、小臀鳍与异尾。'},'generator':'source/generate.py','profile':'palette-only static','scientific_notes':'215 mm reference length; living thickness, fin pose and color inferred. Original geometry only.'},
        output_root=stage,render=False,max_triangles=40000,max_materials=6,max_primitives=8)
    built=stage/'fleurantia'
    (out/'model.glb').write_bytes((built/'fleurantia.glb').read_bytes())
    # Save directly to declared source name too so loaded .blend filepath matches delivery.
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    report=json.loads((built/'qa.json').read_text())
    report['construction_scope']='Maker source and static export tests, not independent acceptance'
    report['mounting_point']='Identity origin at midbody in swimming pose; below-zero Z is intentional, no ground contract'
    report['build']={'blender':bpy.app.version_string,'python':sys.version,'seed':P['seed'],'generator_sha256':digest(BASE/'generate.py'),'params_sha256':digest(BASE/'params.json'),'export_options':record['export_options'],'runtime_dependencies':['Blender 4.3.2 Python standard library','source/deps/asset_common.py','source/deps/qa_glb.py']}
    report['final_files']={'model.glb':digest(out/'model.glb'),'model.blend':digest(out/'model.blend')}
    save(out/'build-report.json',report)
    save(out/'anatomy-record.json',{'profile':PROFILE,'median_fin_polygons_normalized_s_and_z_m':{'first_dorsal':d1,'second_dorsal':d2,'anal':anal,'caudal':tail},'paired_fins':{'count':4,'structure':'closed 10-sided lofts with fleshy bases and tapering supported blades'},'closed_mouth':True,'original_procedural_geometry':True,'inferred':['living width','color','fin pose','scale cue layout'],'measurement_basis':'Total axial length 0.215 m from Fig9E reported length; remainder conservative reconstruction.'})
    print('FLEURANTIA_BUILD_COMPLETE '+report['glb']['sha256'])

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]); build(args.output.resolve())
