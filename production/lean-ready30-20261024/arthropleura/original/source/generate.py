# SPDX-License-Identifier: MIT
"""Deterministic original genus-level Arthropleura, meters, -Y forward.
Run with Blender background, --factory-startup, --threads 2, and --python-exit-code 1.
Use -- --out OUTPUT --params source/params.json. Optional --gray or --views.
All generator dependencies are copied, hashed, package-relative Python files.
"""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
import bpy
from mathutils import Vector
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE / 'deps'))
from asset_common import setup_scene, make_material, mesh_object, ground_asset, audit_source, render_previews, link_object
from qa_glb import audit_glb


def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

class Part:
    def __init__(self,name,materials,collection):
        self.name,self.materials,self.collection=name,materials,collection
        self.v=[]; self.f=[]; self.mi=[]; self.module=[]
    def add(self,verts,faces,mat=0,module=-1):
        offset=len(self.v); self.v.extend(verts); self.f.extend([tuple(offset+x for x in f) for f in faces]); self.mi.extend([mat]*len(faces)); self.module.extend([module]*len(faces))
    def finish(self):
        o=mesh_object(self.name,self.v,self.f,self.materials,self.collection)
        for p,m in zip(o.data.polygons,self.mi): p.material_index=m
        a=o.data.attributes.new('anatomical_module','INT','FACE')
        for d,m in zip(a.data,self.module): d.value=m
        o['edit_note']='Disconnected closed anatomical components; face attribute anatomical_module identifies repeated modules.'
        return o


def tube(part,points,radii,mat=0,module=-1,sides=6):
    points=[Vector(p) for p in points]; verts=[]
    for i,(p,r) in enumerate(zip(points,radii)):
        tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
        ref=Vector((0,1,0)) if abs(tangent.y)<.9 else Vector((1,0,0))
        a=tangent.cross(ref).normalized(); b=tangent.cross(a).normalized()
        for j in range(sides): verts.append(tuple(p+r*(math.cos(2*math.pi*j/sides)*a+math.sin(2*math.pi*j/sides)*b)))
    faces=[tuple(reversed(range(sides)))]
    for k in range(len(points)-1):
        for j in range(sides): faces.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
    faces.append(tuple((len(points)-1)*sides+j for j in range(sides)))
    part.add(verts,faces,mat,module)


def ellipsoid(part,center,scale,mat=0,module=-1,sides=12):
    # Explicit pole fans avoid duplicate collapsed ring vertices.
    c=Vector(center); sx,sy,sz=scale; verts=[tuple(c+Vector((0,0,-sz)))]; rings=5
    for k in range(1,rings+1):
        t=-math.pi/2+math.pi*k/(rings+1)
        for j in range(sides):
            a=2*math.pi*j/sides; verts.append(tuple(c+Vector((sx*math.cos(t)*math.cos(a),sy*math.cos(t)*math.sin(a),sz*math.sin(t)))))
    top=len(verts); verts.append(tuple(c+Vector((0,0,sz)))); faces=[]
    for j in range(sides): faces.append((0,1+(j+1)%sides,1+j))
    for k in range(rings-1):
        a=1+k*sides;b=a+sides
        for j in range(sides): faces.append((a+j,a+(j+1)%sides,b+(j+1)%sides,b+j))
    for j in range(sides): faces.append((top,1+(rings-1)*sides+j,1+(rings-1)*sides+(j+1)%sides))
    part.add(verts,faces,mat,module)


def plate(part,xc,y,w,side,module):
    # A broad low lateral tergite with an articulated rearward outer corner.
    root=w*.85; extent=w+(.118 if module<18 else .118*(24-module)/6)
    outline=[(root,y-.031,.114),(w+.044,y-.028,.120),(extent-.018,y-.004,.101),(extent,y+.034,.079),(extent-.025,y+.053,.088),(w+.026,y+.027,.113),(root,y+.030,.114)]
    scale=.78+.22*min(1.,w/.12)
    pts=[(xc+side*x,yy,z*scale) for x,yy,z in outline]; n=len(pts)
    center=(xc+side*(w+.042),y+.009,.127*scale)
    verts=pts+[center]+[(x,yy,z-.009) for x,yy,z in pts]+[(center[0],center[1],center[2]-.014)]
    faces=[]
    for j in range(n):
        k=(j+1)%n; faces.extend([(n,j,k),(2*n+1,n+1+k,n+1+j),(j,n+1+j,n+1+k,k)])
    part.add(verts,faces,module%2,module)


def build(params):
    collection=setup_scene('arthropleura',params['seed'])
    mats=[make_material(p['name'],p['hex'],p['roughness']) for p in params['palette']]
    trunk=Part('Dorsal segmented axial shields',mats[:2],collection)
    laterals=[Part('Lateral plates '+s,mats[:2],collection) for s in ('left','right')]
    legs=[Part('Short walking legs '+s,[mats[2]],collection) for s in ('left','right')]
    underside=Part('Ventral segmented body',[mats[3]],collection)
    head=Part('Head and enclosed mouth',[mats[1],mats[3]],collection)
    antenna=Part('Slender antennae and eye peduncles',[mats[2]],collection)
    eyes=Part('Small stalked eyes',[mats[4]],collection)
    count=params['dorsal_modules']; ys=[]
    for i in range(count):
        t=i/(count-1); y=-.79+1.68*t; xc=.012*math.sin(t*math.pi*1.4)
        w=.102+.021*math.sin(min(t/.7,1.)*math.pi*.7)
        if t>.72: w*=1-.70*((t-.72)/.28)**1.3
        if i==0: w*=.91
        ys.append((xc,y,w))
        # Three longitudinal profile rings create bevels around each closed shield.
        profile=[(-1.,.098),(-.92,.128),(-.55,.153),(0,.160),(.55,.153),(.92,.128),(1.,.098),(.7,.078),(-.7,.078)]
        verts=[]; sides=len(profile)
        for off,factor,zfactor in [(-.033,.94,.95),(-.012,1.,1.),(.032,.97,.98)]:
            verts.extend((xc+x*w*factor,y+off,z*(.86+.14*w/.122)*zfactor) for x,z in profile)
        faces=[tuple(reversed(range(sides)))]
        for k in range(2):
            for j in range(sides): faces.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
        faces.append(tuple(2*sides+j for j in range(sides)))
        trunk.add(verts,faces,i%2,i)
        ellipsoid(underside,(xc,y,.083),(w*.89,.041,.031),module=i,sides=8)
        for si,side in enumerate((-1,1)):
            plate(laterals[si],xc,y,w,side,i)
            # Two short leg pairs per trunk module, with conservative reduction at ends.
            offsets=[-.020,.018] if 0<i<count-1 else [0.]
            for j,offset in enumerate(offsets):
                phase=math.sin(i*.65+si*1.1+j*.4); d=.007*phase
                extent=w+.104
                points=[(xc+side*w*.55,y+offset,.078),(xc+side*(w+.020),y+offset+.005,.063),(xc+side*(w+.064),y+offset+d,.029),(xc+side*extent,y+offset+.010+d,.005)]
                tube(legs[si],points,[.010,.009,.006,.0038],module=i,sides=6)
    ellipsoid(head,(0,-.871,.097),(.073,.075,.044),sides=14)
    ellipsoid(head,(0,-.922,.078),(.038,.026,.018),mat=1,sides=10)
    for s in (-1,1):
        tube(antenna,[(s*.038,-.918,.091),(s*.058,-.956,.087),(s*.092,-.989,.101),(s*.120,-1.021,.124),(s*.132,-1.050,.144)],[.007,.0065,.0055,.0042,.0027],sides=7)
        tube(antenna,[(s*.055,-.877,.114),(s*.081,-.895,.128),(s*.094,-.902,.132)],[.005,.0045,.004],sides=7)
        ellipsoid(eyes,(s*.096,-.904,.134),(.008,.007,.007),sides=8)
    # Rounded terminal plate, not a scorpion telson or invented tail sting.
    xc,y,w=ys[-1]; ellipsoid(underside,(xc,y+.027,.083),(.025,.045,.025),module=count,sides=10)
    objects=[p.finish() for p in [trunk,*laterals,*legs,underside,head,antenna,eyes]]
    for o in objects:o['reconstruction']='Original genus-level artistic reconstruction; adult head scaling extrapolated from juvenile evidence.'
    ground_asset(collection,center_xy=False)
    # Pivot is the midpoint of the actual walking-foot contact envelope.
    bpy.context.view_layer.update()
    foot_points=[o.matrix_world@v.co for o in objects if o.name.startswith('Short walking legs') for v in o.data.vertices if (o.matrix_world@v.co).z<.003]
    contact_center=Vector(((min(v.x for v in foot_points)+max(v.x for v in foot_points))/2,(min(v.y for v in foot_points)+max(v.y for v in foot_points))/2,0))
    for o in objects:
        o.location-=contact_center
    bpy.context.view_layer.update()
    root=bpy.data.objects[collection['asset_root']]; root['module_count_artistic']=count; root['walking_leg_pairs_artistic']=46
    return collection


def export_model(collection,out,params):
    audit=audit_source(collection,params['budgets']['max_triangles'])
    if audit['errors']: raise RuntimeError(repr(audit['errors']))
    bpy.context.preferences.filepaths.save_version=0
    # Clear default UI and render-path buffers before saving an editable deliverable.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b' '*1000; space.params.directory=b'//'
                    space.params.filename=' '*200; space.params.filename=''
    bpy.context.scene.render.filepath=' '*1000
    bpy.context.scene.render.filepath='//renders/'
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[collection['asset_root']]
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Missing required exporter flags')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    g=audit_glb(out/'model.glb',params['budgets']['max_triangles'],params['budgets']['max_materials'],params['budgets']['max_primitives'])
    if g['errors']:raise RuntimeError(repr(g['errors']))
    g['file']='model.glb'  # Package-relative evidence label, never an execution path.
    assert g['bytes']<=params['budgets']['max_glb_bytes']
    b=audit['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    error=max(abs(g['bounds_m'][side][i]-expected[side][i]) for side in ('min','max') for i in range(3))
    assert error<.0001 and g['scene_triangles']==audit['triangles']
    write(out/'qa/evidence/build.json',{'status':'PASS','scope':'Source topology, static GLB audit, source/export counts and bounds; not independent visual or runtime approval.','blender_version':bpy.app.version_string,'generator_sha256':digest(SOURCE/'generate.py'),'params_sha256':digest(SOURCE/'params.json'),'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),'source_audit':audit,'glb_audit':g,'bounds_max_error_m':error,'export_options':options,'dorsal_modules_artistic':24,'walking_leg_pairs_artistic':46})


def render_exact(out,gray=False):
    before=digest(out/'model.glb');collection=setup_scene('arthropleura-view')
    existing=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(out/'model.glb'));imported=[o for o in bpy.data.objects if o not in existing]
    for o in imported:link_object(o,collection,parent=False)
    if gray:
        mat=make_material('Gray blockout','#929292',.85)
        for o in imported:
            if o.type=='MESH':
                o.data.materials.clear();o.data.materials.append(mat)
                for p in o.data.polygons:p.material_index=0
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    folder=out/'private/gray' if gray else out/'views'
    views=('front','side','hero') if gray else ('front','side','top','hero')
    rendered=render_previews(collection,folder,views=views,resolution=384 if gray else 768,samples=8 if gray else 48,transparent=not gray)
    for v in views:
        source=folder/('preview-'+v+'.png');target=folder/(('perspective' if v=='hero' else v)+'.png');source.replace(target)
    if not gray:shutil.copyfile(folder/'perspective.png',out/'preview.png')
    assert digest(out/'model.glb')==before
    evidence={'scope':'Fresh import of exact GLB into Blender Cycles CPU, not source-scene proof or browser GPU validation.','glb_sha256':before,'generator_sha256':digest(SOURCE/'generate.py'),'renderer_helper_sha256':digest(SOURCE/'deps/asset_common.py'),'blender_version':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'samples':8 if gray else 48,'resolution':[384,384] if gray else [768,768],'transparent':not gray,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'camera_type':'ORTHO','directions':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},'images':{p.name:digest(p) for p in folder.glob('*.png')}}
    write(out/('private/gray-evidence.json' if gray else 'qa/evidence/exact-glb-views.json'),evidence)


def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--params',type=Path,default=SOURCE/'params.json');p.add_argument('--gray',action='store_true');p.add_argument('--views',action='store_true');p.add_argument('--render-only',action='store_true');a=p.parse_args(argv)
    a.out.mkdir(parents=True,exist_ok=True);params=json.loads(a.params.read_text())
    if not a.render_only:export_model(build(params),a.out,params)
    if a.gray or a.views:render_exact(a.out,a.gray)
if __name__=='__main__': main()
