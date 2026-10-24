# SPDX-License-Identifier: MIT
"""Original Diprotodon profile-loft reconstruction. Run with Blender --background --python source/generate.py -- --output-dir OUTPUT --params source/params.json.
Only declared package-local helpers, Python standard library and Blender are required.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o): Path(p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')

def loft(name,profiles,mat,col,n=20):
    # Profiles are (longitudinal y, lateral half-width, bottom z, top z).
    verts=[];faces=[]
    for j,(y,w,b,t) in enumerate(profiles):
        mid=(b+t)/2; height=(t-b)/2
        for i in range(n):
            a=2*math.pi*i/n
            verts.append((w*math.cos(a),y,mid+height*math.sin(a)))
    for j in range(len(profiles)-1):
        for i in range(n): faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    faces+=[tuple(range(n-1,-1,-1)),tuple((len(profiles)-1)*n+i for i in range(n))]
    return mesh_object(name,verts,faces,mat,col)

def tube(name,sections,mat,col,n=14):
    # Sections are ((x,y,z), lateral radius, front/back radius), stacked vertically.
    verts=[];faces=[]
    for (x,y,z),rx,ry in sections:
        for i in range(n):
            a=2*math.pi*i/n; verts.append((x+rx*math.cos(a),y+ry*math.sin(a),z))
    for j in range(len(sections)-1):
        for i in range(n): faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    faces+=[tuple(range(n-1,-1,-1)),tuple((len(sections)-1)*n+i for i in range(n))]
    return mesh_object(name,verts,faces,mat,col)

def ellipsoid(name,center,scales,mat,col,segments=16,rings=8,rot=None):
    verts=[];faces=[]
    for j in range(1,rings):
        v=math.pi*j/rings
        for i in range(segments):
            a=2*math.pi*i/segments
            q=Vector((scales[0]*math.sin(v)*math.cos(a),scales[1]*math.sin(v)*math.sin(a),scales[2]*math.cos(v)))
            if rot: q=rot@q
            verts.append(tuple(q+Vector(center)))
    top=len(verts);verts.append((center[0],center[1],center[2]+scales[2]));bottom=len(verts);verts.append((center[0],center[1],center[2]-scales[2]))
    for j in range(rings-2):
        for i in range(segments): faces.append((j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i))
    for i in range(segments): faces.extend([(top,i,(i+1)%segments),(bottom,(rings-2)*segments+(i+1)%segments,(rings-2)*segments+i)])
    return mesh_object(name,verts,faces,mat,col)

def union_surface(parts,col,mat,params):
    # Preserve semantic pre-union lofts for editing separately from the export.
    construction=bpy.data.collections.new('EDITABLE_PROFILE_LOFTS');bpy.context.scene.collection.children.link(construction)
    for ob in parts:
        cp=ob.copy();cp.data=ob.data.copy();cp.parent=None;construction.objects.link(cp)
        cp.name='profile_'+ob.name;cp.hide_render=True;cp.hide_viewport=True
    construction.hide_render=True;construction.hide_viewport=True
    bpy.ops.object.select_all(action='DESELECT')
    for ob in parts: ob.select_set(True)
    bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();body=parts[0];body.name='continuous_coat_surface'
    rem=body.modifiers.new('Loft union','REMESH');rem.mode='VOXEL';rem.voxel_size=params['voxel_size_m'];rem.use_smooth_shade=False
    bpy.ops.object.modifier_apply(modifier=rem.name)
    sm=body.modifiers.new('Soft tissue transitions','SMOOTH');sm.factor=1.0;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)
    dec=body.modifiers.new('Deliberate low-poly surface','DECIMATE');dec.ratio=params['surface_decimate_ratio'];dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name)
    # Foot soles stay exactly on the ground after voxel smoothing.
    for v in body.data.vertices:
        if v.co.z<0.045: v.co.z=0
    bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.00001);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=0.000001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
    body.data.materials.clear();body.data.materials.append(mat);body.data.shade_flat();return body

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--params',type=Path,default=HERE/'params.json');ap.add_argument('--gray',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True);p=json.loads(a.params.read_text());col=setup_scene(p['asset_id'],p['seed']);scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
    mats={k:make_material(k, '#99958D' if a.gray else v) for k,v in p['palette'].items()}
    parts=[loft('deep_bellied_high_shouldered_torso',p['torso_profiles_y_width_bottom_top'],mats['coat'],col),loft('large_blunt_skull_envelope',p['head_profiles_y_width_bottom_top'],mats['coat'],col)]
    # Strong limbs with identifiable elbows/hocks; left/right contacts differ only slightly in y.
    for sign,label in [(-1,'left'),(1,'right')]:
        dy=0.025*sign
        parts.append(tube(label+'_forelimb',[((sign*.32,-.57,1.53),.10,.18),((sign*.40,-.57,1.34),.22,.27),((sign*.42,-.57,1.17),.25,.28),((sign*.47,-.54,.95),.22,.22),((sign*.49,-.48,.65),.16,.18),((sign*.48,-.63,.32),.12,.13),((sign*.46,-.67,.10),.12,.12)],mats['coat'],col))
        parts.append(tube(label+'_hindlimb',[((sign*.30,.77,1.43),.10,.17),((sign*.39,.78,1.24),.24,.29),((sign*.42,.78,1.10),.27,.29),((sign*.49,.85,.91),.23,.24),((sign*.48,.99,.60),.15,.17),((sign*.45,.93,.32),.12,.13),((sign*.43,.85,.10),.12,.12)],mats['coat'],col))
        for kind,cx,cy in [('fore',sign*.45,-.74+dy),('hind',sign*.42,.77+dy)]:
            parts.append(tube(label+'_'+kind+'_inturned_foot',[((cx-sign*.025,cy-.025,0),.145,.22),((cx-sign*.02,cy-.025,.075),.16,.23),((cx,cy+.04,.19),.13,.14)],mats['coat'],col))
        # Small inferred ears, with a broad attachment rather than projecting cones.
        parts.append(ellipsoid(label+'_ear', (sign*.335,-1.065,1.47),(.14,.105,.19),mats['coat'],col))
    parts.append(loft('short_inferred_tail',[(1.08,.11,.91,1.12),(1.28,.10,.85,1.02),(1.40,.07,.78,.91),(1.45,.018,.77,.81)],mats['coat'],col,n=12))
    body=union_surface(parts,col,mats['coat'],p)
    if not a.gray:
        # A shallow broad nasal pad, not a trunk; all soft-tissue extent is explicitly inferred.
        ellipsoid('broad_fleshy_nasal_pad',(0,-1.816,1.055),(.29,.118,.16),mats['muzzle'],col)
        ellipsoid('nose_leather',(0,-1.906,1.065),(.22,.058,.105),mats['nose'],col,segments=16,rings=6)
        for sign,label in [(-1,'left'),(1,'right')]:
            ellipsoid(label+'_nostril',(sign*.122,-1.95,1.075),(.045,.015,.026),mats['eye'],col,segments=12,rings=5)
            ellipsoid(label+'_eye_socket',(sign*.355,-1.425,1.205),(.058,.09,.069),mats['muzzle'],col,segments=12,rings=6)
            ellipsoid(label+'_eye',(sign*.396,-1.447,1.219),(.026,.045,.033),mats['eye'],col,segments=12,rings=6)
            ellipsoid(label+'_ear_inner',(sign*.335,-1.151,1.487),(.083,.02,.112),mats['ear'],col,segments=12,rings=6)
            ellipsoid(label+'_lower_incisor',(sign*.044,-1.807,.786),(.034,.078,.031),mats['incisor'],col,segments=10,rings=5)
        # Thin lip separation follows the broad blunt jaw; teeth remain discreet and non-tusk-like.
        ellipsoid('closed_lip_line',(0,-1.801,.822),(.267,.025,.015),mats['nose'],col,segments=20,rings=4)
        # Small rounded keratin tips, three visible simplified toe tips per foot, not hooves or digging claws.
        for sign,label in [(-1,'left'),(1,'right')]:
            for kind,cx,cy in [('fore',sign*.45,-.74+.025*sign),('hind',sign*.42,.77+.025*sign)]:
                for j,dx in enumerate([-.085,0,.085]):
                    ellipsoid(label+'_'+kind+'_toe_'+str(j),(cx-sign*.025+dx,cy-.223,.047),(.038,.043,.025),mats['keratin'],col,segments=8,rings=4)
    source=audit_source(col,18000)
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0
    scene.render.filepath='//preview.png'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b' '*1023
                    space.params.directory=b'//'
                    space.params.filename=''
    scene['scientific_limits']=p['scientific_note'];scene['generator']='source/generate.py';scene['generator_sha256']=digest(__file__);scene['params_sha256']=digest(a.params)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects: obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available: raise RuntimeError('Required exporter flags unavailable')
    bpy.ops.export_scene.gltf(**options)
    glb=audit_glb(out/'model.glb',18000,8,36)
    # No internal input/output locations in public reports.
    glb.pop('path',None);glb['file']='model.glb'
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][s][i]-expected[s][i]) for s in ('min','max') for i in range(3))
    if glb['errors'] or delta>0.0001 or glb['scene_triangles']!=source['triangles']: raise RuntimeError('Export validation failed '+repr(glb['errors']))
    report={'asset_id':p['asset_id'],'revision':p['revision'],'status':'PASS','scope':'Source and static GLB structure plus axis-aware bounds; not independent visual QA or GPU rendering.','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'generator_sha256':digest(__file__),'params_sha256':digest(a.params),'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'export_options':{k:v for k,v in options.items() if k!='filepath'},'editable_source':'Semantic pre-union profile lofts in hidden EDITABLE_PROFILE_LOFTS; final export surface and facial details in EXPORT.','gray':a.gray}
    write(out/'build-report.json',report);print(json.dumps({'status':'PASS','triangles':glb['scene_triangles'],'bytes':glb['bytes'],'bounds':glb['bounds_m']}))
if __name__=='__main__': main()
