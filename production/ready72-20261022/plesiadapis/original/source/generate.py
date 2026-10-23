# SPDX-License-Identifier: MIT
"""Original Plesiadapis cookei living reconstruction, Blender 4.3.2.
Run: blender -b --threads 2 --python source/generate.py -- --out OUTPUT
Optional --gray or --render imports OUTPUT/model.glb into a clean scene.
No input reference image is embedded or read by this deterministic generator.
"""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb, read_glb, semantic_digest

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class Part:
    def __init__(self,name,mats):self.name=name;self.mats=mats if isinstance(mats,list) else [mats];self.v=[];self.f=[];self.mi=[]
    def add(self,verts,faces,material=0):
        n=len(self.v);self.v.extend(verts);self.f.extend(tuple(n+j for j in f) for f in faces);self.mi.extend([material]*len(faces))
    def emit(self):
        o=ac.mesh_object(self.name,self.v,self.f,self.mats,COL)
        for p,i in zip(o.data.polygons,self.mi):p.material_index=i
        return o

def tube_geom(rows,sides=12,fur=0):
    verts=[]
    for i,r in enumerate(rows):
        c=Vector(r[:3]);t=Vector(rows[min(i+1,len(rows)-1)][:3])-Vector(rows[max(0,i-1)][:3]);t.normalize()
        u=Vector((1,0,0));u=(u-t*u.dot(t)).normalized();v=t.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides
            q=1+fur*math.sin(3*a+i*1.7)
            verts.append(tuple(c+u*r[3]*math.cos(a)*q+v*r[4]*math.sin(a)*q))
    faces=[tuple(reversed(range(sides)))]
    for i in range(len(rows)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;c=b+sides;d=a+sides
            faces.extend([(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)])
    faces.append(tuple((len(rows)-1)*sides+j for j in range(sides)))
    return verts,faces

def tube(name,rows,sides,mats,fur=0):
    p=Part(name,mats);p.add(*tube_geom(rows,sides,fur));return p.emit()

def loft(name,rows,sides,mats,regions=False,shape=2):
    verts=[]
    for i,row in enumerate(rows):
        y,w,b,t=row[:4];cx=row[4] if len(row)>4 else 0
        for j in range(sides):
            a=2*math.pi*j/sides;c=math.cos(a);s=math.sin(a)
            verts.append((cx+w*math.copysign(abs(c)**(2/shape),c),y,(b+t)/2+(t-b)/2*math.copysign(abs(s)**(2/shape),s)))
    faces=[tuple(reversed(range(sides)))]
    for i in range(len(rows)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;c=b+sides;d=a+sides
            faces.extend([(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)])
    faces.append(tuple((len(rows)-1)*sides+j for j in range(sides)))
    p=Part(name,mats);p.add(verts,faces);o=p.emit()
    if regions:
        for poly in o.data.polygons:
            j=((poly.index-1)//2)%sides
            angle=2*math.pi*(j+.5)/sides
            poly.material_index=1 if math.sin(angle)>.78 else 2 if math.sin(angle)<-.53 else 0
    return o

def ellipsoid(name,c,s,mat,rings=6,segs=12):
    verts=[(c[0],c[1],c[2]-s[2])]
    for i in range(1,rings):
        lat=-math.pi/2+math.pi*i/rings
        for j in range(segs):
            a=j*2*math.pi/segs;verts.append((c[0]+s[0]*math.cos(lat)*math.cos(a),c[1]+s[1]*math.cos(lat)*math.sin(a),c[2]+s[2]*math.sin(lat)))
    verts.append((c[0],c[1],c[2]+s[2]));last=len(verts)-1
    faces=[(0,1+(j+1)%segs,1+j) for j in range(segs)]
    for i in range(rings-2):
        for j in range(segs):
            a=1+i*segs+j;b=1+i*segs+(j+1)%segs;faces.extend([(a,b,b+segs),(a,b+segs,a+segs)])
    faces.extend((last,1+(rings-2)*segs+j,1+(rings-2)*segs+(j+1)%segs) for j in range(segs))
    p=Part(name,mat);p.add(verts,faces);return p.emit()

def create():
    global COL
    COL=ac.setup_scene('plesiadapis',P['seed'])
    colors=P['palette_srgb']
    coat=ac.make_material('Coat warm brown',colors['coat'],.91)
    back=ac.make_material('Dorsal dark brown',colors['back'],.93)
    under=ac.make_material('Throat warm taupe',colors['under'],.93)
    dark=ac.make_material('Eyes nose and mouth',colors['dark'],.45)
    tooth=ac.make_material('Incisor ivory',colors['tooth'],.72)
    claw=ac.make_material('Claw horn',colors['claw'],.82)
    # Connected, deliberately profiled robust trunk and neck. No sphere-body construction.
    loft('Trunk and neck',[
        [-.133,.023,.136,.182],[-.115,.036,.118,.196],[-.088,.046,.100,.207],
        [-.050,.055,.087,.215],[-.012,.061,.080,.220],[.030,.064,.081,.223],
        [.065,.061,.088,.220],[.093,.051,.103,.209],[.116,.034,.121,.190],[.128,.017,.139,.167]],
        20,[coat,back,under],True,2.15)
    # Low, broad braincase followed by a narrow elongated rostrum.
    loft('Long low cranium and pointed rostrum',[
        [-.115,.022,.157,.192],[-.132,.031,.151,.203],[-.149,.034,.146,.206],
        [-.165,.031,.142,.199],[-.181,.024,.138,.186],[-.197,.018,.136,.171],
        [-.211,.013,.135,.160],[-.220,.009,.136,.154]],20,[coat,back,under],True,2.1)
    loft('Mandible and chin',[
        [-.135,.018,.154,.180],[-.153,.026,.139,.161],[-.171,.025,.132,.150],[-.189,.020,.127,.144],
        [-.207,.013,.128,.140],[-.220,.007,.133,.143]],14,[under])
    # A narrow ordinary mouth, not a primate grin. Main teeth are at the tip, not lateral canines.
    loft('Compact mouth seam',[
        [-.194,.017,.137,.139],[-.209,.013,.138,.141],[-.224,.007,.139,.143]],10,[dark])
    ellipsoid('Small nasal pad',(0,-.222,.150),(.009,.0042,.0045),dark,6,12)
    for s,label in [(-1,'L'),(1,'R')]:
        ellipsoid('Lateral orbital rim '+label,(s*.0295,-.161,.1805),(.0047,.007,.0058),back,6,12)
        ellipsoid('Lateral eye '+label,(s*.0325,-.162,.181),(.0032,.0052,.0043),dark,7,12)
        # Restrained non-monkey pinna, low rounded leaf profile, not large circular rodent ears.
        rows=[(s*.024,-.131,.190,.007,.0045),(s*.030,-.132,.201,.008,.0045),(s*.034,-.131,.212,.006,.003),(s*.033,-.130,.218,.0017,.0016)]
        tube('Small pinna '+label,rows,10,[coat])
        tube('Pinna inner shade '+label,[(s*.030,-.136,.200,.0043,.0015),(s*.033,-.1348,.208,.0033,.0012),(s*.033,-.1334,.213,.0008,.0007)],8,[back])
        # Paired broad incisors, mildly curved forward/down. Not canine tusks.
        tube('Upper incisor '+label,[(s*.0039,-.220,.144,.0030,.0027),(s*.0040,-.225,.140,.0029,.0025),(s*.0042,-.2265,.135,.0026,.0017),(s*.0042,-.2248,.132,.0021,.0009)],8,[tooth])
        tube('Lower incisor '+label,[(s*.0035,-.215,.133,.0024,.0019),(s*.0035,-.222,.134,.0022,.0017),(s*.0036,-.226,.1365,.0018,.0010)],8,[tooth])
    # Four independently editable limb assemblies with elbow/knee bends and separate rays.
    for s,label in [(-1,'L'),(1,'R')]:
        fore_shift=-.008 if s>0 else .006
        tube('Forelimb '+label,[(s*.018,-.081,.159,.023,.026),(s*.045,-.067,.132,.023,.024),
            (s*.053,-.052,.092,.017,.017),(s*.057,-.071,.061,.012,.013),
            (s*.060,-.103+fore_shift,.030,.009,.010),(s*.061,-.113+fore_shift,.018,.010,.008)],12,[coat])
        hind_shift=-.070 if s<0 else -.008
        tube('Hindlimb '+label,[(s*.018,.084,.160,.028,.034),(s*.053,.070,.134,.030,.032),
            (s*.064,.044,.098,.024,.024),(s*.065,.080,.062,.016,.019),
            (s*(.079 if s<0 else .067),.112+hind_shift,.031,.011,.011),(s*(.080 if s<0 else .068),.097+hind_shift,.018,.011,.008)],14,[coat])
        for role,cx,cy in [('Fore',s*.061,-.118+fore_shift),('Hind',s*(.080 if s<0 else .068),.092+hind_shift)]:
            paw=Part(role+' foot '+label,[coat,under]);claws=Part(role+' curved claws '+label,[claw])
            paw.add(*tube_geom([(cx,cy+.010,.020,.011,.008),(cx,cy,.014,.014,.008),(cx,cy-.012,.012,.013,.006)],10))
            # All five rays run forward and splay; there is no opposed thumb or flat nail.
            for j in range(5):
                dx=(j-2)*.0064;lng=[.018,.024,.028,.025,.019][j]
                bx=cx+dx*.55;ex=cx+dx*1.45
                y0=cy-.008;ye=y0-lng
                paw.add(*tube_geom([(bx,y0,.013,.0031,.0035),((bx+ex)/2,cy-.012-lng*.42,.011,.0032,.0033),(ex,ye,.009,.0026,.0028)],8))
                claws.add(*tube_geom([(ex,ye+.001,.010,.0022,.0023),(ex+s*.001,ye-.004,.0105,.0020,.0018),
                    (ex+s*.0017,ye-.008,.006,.0013,.0012),(ex+s*.002,ye-.009,.002,.00045,.00040)],7))
            paw.emit();claws.emit()
    # Fur envelope on a relaxed, trailing 350 mm centerline. Neither coil nor prehensile tip.
    controls=[Vector((0,.120,.153)),Vector((.014,.156,.132)),Vector((.032,.198,.099)),
        Vector((.049,.244,.075)),Vector((.061,.292,.059)),Vector((.064,.341,.052)),Vector((.057,.389,.056)),Vector((.043,.437,.067))]
    length=sum((b-a).length for a,b in zip(controls,controls[1:]))
    scale=P['tail_length_m']/length
    controls=[controls[0]+(c-controls[0])*scale for c in controls]
    rows=[]
    radii=[.018,.023,.026,.025,.022,.017,.010,.0014]
    for i in range(len(controls)-1):
        for j in range(3):
            t=j/3;c=controls[i].lerp(controls[i+1],t);r=radii[i]*(1-t)+radii[i+1]*t
            rows.append((*c,r,r*.91))
    rows.append((*controls[-1],radii[-1],radii[-1]*.9))
    tail=tube('Long furry tapering tail',rows,14,[coat,back],.035)
    for poly in tail.data.polygons:
        j=((poly.index-1)//2)%14
        if math.sin(2*math.pi*(j+.5)/14)<-.65:poly.material_index=1
    # Floor sits under the down-curving claw tips; footprint origin is not tail-bbox center.
    footpts=[o.matrix_world@v.co for o in COL.all_objects if o.type=='MESH' and 'curved claws' in o.name for v in o.data.vertices]
    footprint_center=Vector([(min(p[i] for p in footpts)+max(p[i] for p in footpts))/2 for i in (0,1)]+[0])
    for o in COL.all_objects:
        if o.type=='MESH':
            for v in o.data.vertices:v.co-=footprint_center
    ground_offset=ac.ground_asset(COL,False)
    root=bpy.data.objects['plesiadapis']
    root['taxon']='Plesiadapis cookei';root['reconstruction']='whole living animal; soft tissues interpreted'
    root['skull_length_estimate_m']=P['skull_length_m'];root['tail_centerline_m']=P['tail_length_m']
    root['head_body_reconstruction_m']=P['head_body_length_m']
    root['scale_provenance']='Cranium 105.83 mm author estimate; body/tail choices not fossil measurements'
    root['ground_offset_z']=ground_offset[2];root['original_footprint_center_xy']=list(footprint_center)[:2]
    return COL

def build(out):
    out.mkdir(parents=True,exist_ok=True);col=create()
    source=ac.audit_source(col,P['budgets']['max_triangles'])
    write(out/'qa/evidence/source.json',source)
    if source['errors']:raise RuntimeError('Source QA: '+str(source['errors']))
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['plesiadapis']
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,
        export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
        export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
        export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(flags)-available:raise RuntimeError('Missing export flags '+str(set(flags)-available))
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    audit=audit_glb(out/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
    write(out/'qa/evidence/glb.json',audit)
    if audit['errors']:raise RuntimeError('Export QA: '+str(audit['errors']))
    if (out/'model.glb').stat().st_size>P['budgets']['max_glb_bytes']:raise RuntimeError('Byte budget exceeded')
    write(out/'qa/evidence/build.json',{'blender':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),
        'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'seed':P['seed'],
        'export_options':flags,'source_triangle_count':source['triangles'],'glb_bytes':(out/'model.glb').stat().st_size,
        'root_origin':'floor contact center in meters; no tail-box recentering','authoring_forward':'-Y','gltf_forward':'+Z',
        'asset_profile':'static palette-only flat-shaded, original closed profile loft meshes; interpretive soft tissues',
        'tail_centerline_m':P['tail_length_m'],'body_length_choice_m':P['head_body_length_m'],
        'consumer_runtime':'Three.js gate not run in maker; do not infer browser or populated-scene pass'})

def render(out,gray=False):
    from model_render import render_glb
    render_glb(out,gray=gray)

args=argparse.ArgumentParser();args.add_argument('--out',type=Path,required=True);args.add_argument('--render',action='store_true');args.add_argument('--gray',action='store_true');args.add_argument('--render-only',action='store_true')
A=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
P=json.loads((HERE/'params.json').read_text())
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
if not A.render_only:build(A.out)
if A.render or A.gray:render(A.out,gray=A.gray)
