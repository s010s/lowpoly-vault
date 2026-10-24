# SPDX-License-Identifier: MIT
"""Deterministic original Psittacosaurus sp. living reconstruction.
Run in Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output .
Only source/params.json and the two declared source/deps helpers are imported.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=SOURCE.parent); ap.add_argument('--config',type=Path,default=SOURCE/'params.json'); ap.add_argument('--gray',action='store_true'); args=ap.parse_args(argv)
    p=json.loads(args.config.read_text()); out=args.output; out.mkdir(parents=True,exist_ok=True)
    col=setup_scene('psittacosaurus',p['seed'])
    mats=[make_material(k, '#929292' if args.gray else v) for k,v in p['palette'].items()]
    def obj(name,verts,faces,inds=None):
        o=mesh_object(name,verts,faces,mats,col)
        if inds:
            for face,idx in zip(o.data.polygons,inds): face.material_index=idx
        return o
    def loft(name,sections,n=16,mat=1,belly=True):
        verts=[];faces=[];inds=[]
        for y,z,rx,rz in sections:
            for j in range(n):
                a=2*math.pi*j/n; verts.append((rx*math.cos(a),y,z+rz*math.sin(a)))
        for i in range(len(sections)-1):
            for j in range(n):
                faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
                s=math.sin(2*math.pi*(j+.5)/n)
                inds.append(2 if belly and s<-.55 else 0 if belly and s>.65 else mat)
        faces.extend([tuple(range(n-1,-1,-1)),tuple((len(sections)-1)*n+j for j in range(n))]);inds.extend([mat,mat])
        return obj(name,verts,faces,inds)
    def tubegeo(path,radii,n=8,aspect=1):
        vs=[];fs=[]
        for i,c in enumerate(path):
            c=Vector(c); t=Vector(path[min(i+1,len(path)-1)])-Vector(path[max(i-1,0)])
            t.normalize(); ref=Vector((1,0,0)) if abs(t.x)<.9 else Vector((0,1,0)); u=t.cross(ref).normalized(); v=t.cross(u).normalized()
            for j in range(n):
                a=2*math.pi*j/n;vs.append(tuple(c+u*(radii[i]*math.cos(a))+v*(radii[i]*aspect*math.sin(a))))
        for i in range(len(path)-1):
            for j in range(n): fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        fs.extend([tuple(range(n-1,-1,-1)),tuple((len(path)-1)*n+j for j in range(n))]);return vs,fs
    def tube(name,path,radii,n=8,mat=1,aspect=1):
        v,f=tubegeo(path,radii,n,aspect); return obj(name,v,f,[mat]*len(f))
    def batch(name,items):
        vs=[];fs=[];mi=[]
        for path,radii,n,mat in items:
            v,f=tubegeo(path,radii,n);offset=len(vs);vs+=v;fs += [tuple(k+offset for k in face) for face in f];mi += [mat]*len(f)
        return obj(name,vs,fs,mi)
    # Purpose-shaped axial lofts, not assembled stock spheres.
    loft('torso', [(-.34,.505,.045,.07),(-.29,.51,.09,.12),(-.20,.51,.132,.158),(-.07,.51,.15,.177),(.07,.51,.153,.171),(.18,.51,.137,.145),(.27,.51,.098,.10),(.30,.51,.07,.067)],20)
    loft('neck',[(-.435,.615,.071,.087),(-.385,.575,.083,.103),(-.32,.54,.085,.095),(-.285,.52,.07,.073)],16)
    loft('skull',[(-.612,.625,.053,.064),(-.575,.642,.083,.101),(-.525,.655,.105,.114),(-.465,.651,.110,.113),(-.405,.63,.085,.09),(-.375,.607,.051,.055)],20)
    loft('mandible',[(-.625,.56,.045,.022),(-.575,.548,.071,.038),(-.50,.545,.086,.044),(-.43,.563,.075,.044)],14,1,False)
    # Downturned short rostral beak, with closed angular bite edge.
    loft('upper-beak',[(-.675,.565,.012,.020),(-.669,.598,.022,.047),(-.645,.627,.047,.057),(-.609,.628,.060,.059),(-.592,.623,.059,.050)],12,3,False)
    loft('lower-beak',[(-.664,.55,.016,.012),(-.639,.544,.038,.014),(-.597,.546,.055,.019)],12,3,False)
    loft('tail',[ (.245,.51,.097,.101),(.33,.508,.079,.080),(.43,.507,.059,.060),(.54,.502,.043,.045),(.65,.493,.031,.034),(.76,.479,.021,.024),(.86,.46,.013,.016),(.94,.435,.007,.009),(.98,.42,.0025,.0035)],14)
    for side,label in [(-1,'left'),(1,'right')]:
        tube(label+'-jugal-projection',[(side*.087,-.435,.595),(side*.122,-.429,.582),(side*.164,-.399,.564)],[.036,.025,.0045],8,1)
        tube(label+'-hindleg',[(side*.113,.085,.525),(side*.151,.035,.444),(side*.169,-.035,.345),(side*.159,.055,.205),(side*.143,.046,.116),(side*.14,-.007,.054)],[.086,.083,.064,.038,.026,.024],12,1,1.12)
        tube(label+'-forelimb',[(side*.095,-.245,.488),(side*.122,-.282,.395),(side*.126,-.259,.335),(side*.12,-.316,.296)],[.042,.029,.024,.022],10,1)
        # Three weight-bearing hind toes plus one reduced inner digit.
        parts=[]
        for j in range(3):
            x=side*(.14+(j-1)*.032); endy=-.144+abs(j-1)*.018
            parts.append(([(side*.14,-.005,.042),(x,-.062,.027),(x+side*(j-1)*.009,endy,.021)],[.025,.020,.013],8,1))
            parts.append(([(x+side*(j-1)*.007,endy+.010,.022),(x+side*(j-1)*.009,endy-.022,.010)],[.012,.003],7,4))
        parts.append(([(side*.122,.009,.047),(side*.09,-.025,.036)],[.013,.006],7,1));batch(label+'-hindfoot',parts)
        parts=[]
        for j in range(4):
            x=side*(.12+(j-1.5)*.012); length=.042-abs(j-1.3)*.009
            parts.append(([(x,-.311,.299),(x+side*.002,-.328,.282),(x,-.326,.299-length)],[.010,.009,.0055],7,1))
            if j<3: parts.append(([(x,-.326,.299-length+.005),(x,-.338,.299-length-.008)],[.006,.0018],6,4))
        batch(label+'-hand',parts)
    # Sparse three-row localized dorsal tail bundles. Number and tips are stylized.
    br=[]
    for i in range(p['bristle_groups']):
        y=.45+i*.029
        basez=.568-(y-.45)*.19
        length=.115+.048*math.sin(math.pi*(i+.5)/p['bristle_groups'])
        for j in [-1,0,1]:
            x=j*(.013-(y-.45)*.015); lean=.026+.012*math.sin(i*.8+j)
            br.append(([(x,y,basez-.006),(x+j*.003,y+lean*.45,basez+length*.52),(x+j*.006,y+lean,basez+length)],[.0027,.0023,.0014],6,4))
    batch('localized-tail-bristles',br)
    if not args.gray:
        # Eyes and nares remain unobtrusive, not a decorative species pattern.
        for side,label in [(-1,'left'),(1,'right')]:
            tube(label+'-eye-rim',[(side*.091,-.511,.687),(side*.105,-.511,.687)],[.026,.025],12,0)
            tube(label+'-eye',[(side*.104,-.514,.689),(side*.113,-.514,.689)],[.019,.0155],14,5)
            tube(label+'-nostril',[(side*.051,-.608,.65),(side*.058,-.609,.652)],[.005,.0045],8,5)
    # Exact artistic envelope length, with no claim to measured specimen dimensions.
    ymax=max(v.co.y for o in col.objects if o.type=='MESH' for v in o.data.vertices); ymin=min(v.co.y for o in col.objects if o.type=='MESH' for v in o.data.vertices)
    fac=p['length_m']/(ymax-ymin)
    zmin=min(v.co.z for o in col.objects if o.type=='MESH' for v in o.data.vertices)
    for o in col.objects:
        if o.type=='MESH':
            for v in o.data.vertices: v.co *= fac; v.co.z-=zmin*fac
    source=audit_source(col,p['geometry_policy']['max_triangles'])
    if source['errors']: raise RuntimeError(str(source['errors']))
    bpy.context.scene['taxon']='Psittacosaurus sp.; SMF R4970 reference; no species assertion'
    bpy.context.scene['reconstruction_limits']='Original artistic restoration; crushed skull breadth, complete bristle tips, color, pose and scale are inferred.'
    # Remove factory UI directories and render destination from the portable source.
    bpy.context.scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                params=getattr(space,'params',None)
                if params is not None and hasattr(params,'directory'): params.directory=b'//'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.objects: o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    assert set(options)<=available
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    glb=audit_glb(out/'model.glb',p['geometry_policy']['max_triangles'],p['geometry_policy']['max_materials'],p['geometry_policy']['max_primitives'])
    if glb['errors']: raise RuntimeError(str(glb['errors']))
    report={'asset_id':p['asset_id'],'revision':p['revision'],'blender_version':bpy.app.version_string,'generator_sha256':sha(__file__),'params_sha256':sha(args.config),'gray':args.gray,'source':source,'glb':glb,'export_options':options,'blend_sha256':sha(out/'model.blend'),'glb_sha256':sha(out/'model.glb')}
    write(out/'build-report.json',report)

if __name__=='__main__':main()
