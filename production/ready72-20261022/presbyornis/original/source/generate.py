# SPDX-License-Identifier: MIT
"""Presbyornis pervetus, original whole-animal low-poly reconstruction.
Blender 4.3.2; meters, +Z up, -Y forward. No reference textures.
Usage: blender -b -t 2 --python source/generate.py -- --out OUTPUT [--clay | --render-only]
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, _bounds, _vertices_world, _look_at
from qa_glb import audit_glb
from render_views import render_views
P=json.loads((HERE/'params.json').read_text())

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(x,indent=2)+'\n')

def loft(name, sections, mat, n=16, axis='Y', phase=0):
    # Sections (center x,y,z; transverse radius x; transverse radius z or y).
    # End caps are triangle fans, avoiding pinched zero-radius rings.
    verts=[]; faces=[]
    for x,y,z,a,b in sections:
        for j in range(n):
            t=2*math.pi*j/n+phase
            verts.append((x+a*math.cos(t), y+(b*math.sin(t) if axis=='Z' else 0), z+(b*math.sin(t) if axis=='Y' else 0)))
    for i in range(len(sections)-1):
        for j in range(n):
            k=i*n+j; kn=i*n+(j+1)%n
            faces.append((k,kn,kn+n,k+n))
    for i,rev in ((0,True),(len(sections)-1,False)):
        p=sections[i]; c=len(verts); verts.append(p[:3])
        for j in range(n):
            f=(c,i*n+j,i*n+(j+1)%n); faces.append(tuple(reversed(f)) if rev else f)
    return mesh_object(name,verts,faces,mat,C)

def tube(name, points, radii, mat, n=10):
    verts=[]; faces=[]
    for i,(p,r) in enumerate(zip(points,radii)):
        p=Vector(p)
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        tangent.normalize(); u=tangent.cross(Vector((0,1,0)))
        if u.length<0.1: u=tangent.cross(Vector((1,0,0)))
        u.normalize(); v=tangent.cross(u).normalized()
        for j in range(n):
            t=j*2*math.pi/n; verts.append(tuple(p+r*(u*math.cos(t)+v*math.sin(t))))
    for i in range(len(points)-1):
        for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    for i in (0,len(points)-1):
        c=len(verts); verts.append(points[i])
        for j in range(n): faces.append((c,i*n+j,i*n+(j+1)%n))
    return mesh_object(name,verts,faces,mat,C)

def ellipsoid(name,center,radii,mat,n=12,rings=6):
    x,y,z=center; rx,ry,rz=radii
    ss=[]
    for i in range(rings+1):
        theta=math.pi*(.025+.95*i/rings)
        ss.append((x,y-ry*math.cos(theta),z,rx*math.sin(theta),rz*math.sin(theta)))
    return loft(name,ss,mat,n)

def feather(name,s,x,y,z,length,width,mat):
    return loft(name,[(s*x,y,z,.003,.005),(s*(x+.006),y+.025,z-.005,width,.009),(s*(x+.006),y+length*.65,z-.016,width*.68,.006),(s*x,y+length,z-.025,.002,.002)],mat,8)

def foot(name,x,y):
    # Closed thick web, scalloped leading edge between three forward toes.
    outline=[(-.010,.010),(-.025,-.025),(-.038,-.064),(-.027,-.060),(-.017,-.048),(-.009,-.059),(0,-.082),(.009,-.061),(.020,-.049),(.029,-.058),(.039,-.062),(.024,-.027),(.010,.010)]
    verts=[(x+dx,y+dy,z) for z in (.001,.007) for dx,dy in outline]
    N=len(outline); faces=[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]
    faces += [(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
    mesh_object(name+'-web',verts,faces,M['leg'],C)
    for k,(dx,dy) in enumerate([(-.038,-.064),(0,-.082),(.039,-.062)]):
        tube(name+f'-toe-{k+1}',[(x,y,.014),(x+dx*.52,y+dy*.52,.009),(x+dx,y+dy,.0045)],[.005,.0036,.0025],M['leg'],8)
    tube(name+'-elevated-hallux',[(x,y+.004,.026),(x,y+.026,.021),(x+.004,y+.038,.014)],[.004,.003,.0018],M['leg'],8)

def build(out):
    global C,M
    C=setup_scene(P['asset_id'],P['seed'])
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    M={k:make_material('presbyornis-'+k,c) for k,c in P['palette_srgb'].items()}
    # Feathered trunk: cream lower breast and abdomen, original muted brown mantle.
    body=loft('feathered-trunk',[(0,-.152,.667,.020,.033),(0,-.132,.653,.055,.077),(0,-.09,.646,.084,.098),(0,-.025,.646,.101,.105),(0,.045,.653,.099,.098),(0,.108,.661,.078,.077),(0,.16,.663,.049,.047),(0,.195,.661,.018,.018)],[M['back'],M['under']],20)
    for f in body.data.polygons:
        if f.center.z < .653: f.material_index=1
    # Narrow neck in gently bent upright pose; no swan loop or bulky cylindrical collar.
    neck=loft('long-gently-curved-neck',[(0,-.113,.681,.039,.042),(0,-.137,.713,.030,.034),(0,-.163,.753,.023,.027),(0,-.181,.798,.019,.022),(0,-.183,.840,.0165,.020),(0,-.177,.881,.016,.018),(0,-.183,.918,.017,.019),(0,-.200,.953,.018,.019),(0,-.210,.976,.018,.018)],[M['under'],M['back']],16,axis='Z')
    for f in neck.data.polygons:
        if f.center.y > -.17 and f.center.z>.75: f.material_index=1
    # Cranium + bill span exactly 100 mm along Y, as a reconstruction parameter, not a specimen measurement.
    head=loft('small-duck-like-head',[(0,-.194,.974,.004,.008),(0,-.201,.976,.014,.018),(0,-.213,.977,.021,.023),(0,-.226,.976,.020,.022),(0,-.237,.973,.015,.016),(0,-.246,.970,.011,.010)],[M['under'],M['back']],16)
    for f in head.data.polygons:
        if f.center.z>.985: f.material_index=1
    bill=loft('broad-flattened-spatulate-bill',[(0,-.236,.971,.010,.008),(0,-.249,.969,.013,.0063),(0,-.266,.967,.015,.0048),(0,-.282,.966,.0165,.0042),(0,-.290,.966,.014,.0038),(0,-.294,.966,.008,.003)],[M['bill'],M['eye']],16)
    # Thin underside edge is closed and matte, not a floating open sheet.
    for f in bill.data.polygons:
        if f.center.z < .963 and f.center.y < -.25: f.material_index=1
    for s,label in [(-1,'left'),(1,'right')]:
        ellipsoid(label+'-eye',(s*.0200,-.226,.982),(.0032,.0034,.0031),M['eye'],12,6)
        ellipsoid(label+'-nostril',(s*.0122,-.253,.972),(.0014,.0032,.0012),M['eye'],8,4)
        # Broad folded wing coverage plus three tapered primary ridges, no floating repeated plates.
        wing=loft(label+'-folded-wing',[(s*.064,-.102,.695,.011,.026),(s*.086,-.065,.694,.017,.052),(s*.100,-.005,.683,.017,.066),(s*.094,.06,.671,.020,.066),(s*.075,.12,.653,.019,.047),(s*.051,.184,.634,.009,.017),(s*.045,.206,.630,.002,.003)],[M['wing'],M['back']],16)
        for f in wing.data.polygons:
            if f.center.z>.70: f.material_index=1
        for j in range(3): feather(label+f'-primary-{j+1}',s,.074-j*.013,.065+j*.019,.627-j*.006,.135,.011-j*.001,M['wing'])
        # Upper feather pant joins to tibiotarsus. Hock bends slightly back; two-grounded standing pose.
        x=s*.043; off=(-.009 if s<0 else .009)
        tube(label+'-feathered-thigh',[(x,.005+off,.59),(x,.020+off,.54),(x,.029+off,.495)],[.025,.020,.010],M['under'],12)
        tube(label+'-exposed-stilt-leg',[(x,.029+off,.510),(x,.039+off,.405),(x,.057+off,.298),(x,.054+off,.282),(x,.031+off,.145),(x,.006+off,.014)],[.0075,.0065,.0085,.008,.0058,.0065],M['leg'],10)
        foot(label,x,.006+off)
    # Short feathered tail is a coherent modest fan, not a long crane/fantail extension.
    for j in range(5):
        x=(j-2)*.012
        loft(f'tail-feather-{j+1}',[(x,.148,.654,.012,.011),(x*1.08,.205,.637,.014,.010),(x*1.1,.264-abs(j-2)*.008,.607,.006,.004)],M['wing'],8)
    # All sole contacts use lowest Z=0; preserve identity root and footprint center.
    from asset_common import ground_asset
    shift=ground_asset(C,center_xy=False)
    # Translate footprint midpoint, not trunk bbox, to root origin.
    shift_y=.006-(.082-.038)/2
    for obj in C.objects:
        if obj.type=='MESH':
            for v in obj.data.vertices: v.co.y-=shift_y
    source=audit_source(C,P['budgets']['max_triangles'])
    write(out/'qa/evidence/source.json',source)
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.scene['reconstruction_notes']='AMNH standing height approximately 1m; 100mm head/bill model choice; 90mm genus-level skull is a different specimen; plumage speculative.'
    bpy.context.scene['asset_license']='CC-BY-4.0'; bpy.context.scene['asset_author']='Leon Made This / s010s'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in C.all_objects: obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['presbyornis']
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available: raise RuntimeError('Missing exporter flags '+str(set(opts)-available))
    bpy.ops.export_scene.gltf(**opts)
    qa=audit_glb(out/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
    b=source['bounds_blender_m']; emin=[b['min'][0],b['min'][2],-b['max'][1]]; emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(qa['bounds_m'][key][i]-p[i]) for key,p in [('min',emin),('max',emax)] for i in range(3))
    qa['source_bounds_max_error_m']=delta
    assert delta<1e-5 and qa['scene_triangles']==source['triangles']
    assert qa['bytes']<=P['budgets']['max_glb_bytes'] and not qa['errors'],qa
    write(out/'qa/evidence/glb.json',qa)
    write(out/'qa/evidence/build.json',{'asset_id':'presbyornis','revision':'r001','blender':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'seed':P['seed'],'threads':2,'palette_profile':'opaque palette-only PBR','export_options':{k:v for k,v in opts.items() if k!='filepath'},'head_bill_working_length_m':.1,'approximately_1m_height_is_estimate':True,'ground_shift':shift,'footprint_y_shift':shift_y})
    return C

args=argparse.ArgumentParser(); args.add_argument('--out',required=True); args.add_argument('--clay',action='store_true'); args.add_argument('--render-only',action='store_true'); a=args.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True)
if a.render_only:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(out/'model.glb'))
    C=bpy.data.collections.new('IMPORTED_GLB'); bpy.context.scene.collection.children.link(C)
    for obj in list(bpy.context.scene.objects):
        for old in list(obj.users_collection): old.objects.unlink(obj)
        C.objects.link(obj)
    render_views(C,out,clay=False,glb_sha256=sha(out/'model.glb'))
else:
    C=build(out)
    if a.clay: render_views(C,out,clay=True,glb_sha256=sha(out/'model.glb'))
print('PRESBYORNIS_DONE',sha(out/'model.glb'))
