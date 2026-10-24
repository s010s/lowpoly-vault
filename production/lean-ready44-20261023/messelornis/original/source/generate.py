# SPDX-License-Identifier: MIT
"""Original long-legged Messelornis cristata living reconstruction.
Run with Blender 4.3.2, then -- --output-dir OUTPUT. All dependencies are bundled.
Bone centerlines follow SMF ME3550 measurements; plumage and color are inferred.
"""
from pathlib import Path
import argparse,hashlib,json,math,os,sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def loft_geometry(rows,sides=12):
    verts=[];faces=[];centers=[Vector(r[0]) for r in rows]
    for i,(c,rx,rz) in enumerate(rows):
        c=Vector(c);t=(centers[min(i+1,len(rows)-1)]-centers[max(i-1,0)]).normalized();ref=Vector((1,0,0))
        if abs(t.dot(ref))>.95:ref=Vector((0,1,0))
        u=(ref-t*ref.dot(t)).normalized();v=t.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides;verts.append(tuple(c+u*rx*math.cos(a)+v*rz*math.sin(a)))
    for i in range(len(rows)-1):
        for j in range(sides):faces.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    verts.extend([tuple(centers[0]),tuple(centers[-1])]);a=len(verts)-2;b=len(verts)-1
    for j in range(sides):faces.extend([(a,(j+1)%sides,j),(b,(len(rows)-1)*sides+j,(len(rows)-1)*sides+(j+1)%sides)])
    return verts,faces

def loft(name,rows,mat,sides=12):
    v,f=loft_geometry(rows,sides);return mesh_object(name,v,f,mat,C)
def multi(name,parts,mat):
    vv=[];ff=[]
    for v,f in parts:
        n=len(vv);vv.extend(v);ff.extend(tuple(n+x for x in q) for q in f)
    return mesh_object(name,vv,ff,mat,C)
def feather(a,b,width,thickness,sides=8):
    a,b=Vector(a),Vector(b)
    return loft_geometry([(tuple(a.lerp(b,t)),width*w,thickness*w) for t,w in [(0,.22),(.16,.64),(.37,.97),(.65,1),(.86,.78),(.97,.37),(1,.06)]],sides)
def eye(name,center,radii):
    c=Vector(center);rows=[]
    for t in [-.99,-.8,-.4,0,.4,.8,.99]:
        rows.append((tuple(c+Vector((t*radii[0],0,0))),radii[1]*math.sqrt(1-t*t),radii[2]*math.sqrt(1-t*t)))
    return loft(name,rows,M['eye_claw'],10)
def build():
    global C,M
    C=setup_scene(P['asset_id'],P['seed']);M={k:make_material(k,v,roughness=.86 if k!='eye_claw' else .42) for k,v in P['palette_srgb'].items()}
    # Compact continuous back, chest and moderately curved neck. Cross-sections are designed, not stacked primitives.
    rows=[((0,.082,.139),.004,.005),((0,.070,.146),.016,.015),((0,.048,.148),.028,.024),((0,.021,.147),.032,.029),((0,-.004,.151),.028,.027),((0,-.024,.161),.019,.021),((0,-.030,.176),.0125,.0145),((0,-.031,.188),.0105,.012),((0,-.042,.199),.012,.013),((0,-.056,.203),.012,.012)]
    body=loft('trunk-and-curved-neck',rows,[M['feathers'],M['underside']],18)
    for p in body.data.polygons:
        if (p.center.z<.165 and p.normal.z<-.27) or (p.center.z>.16 and p.normal.y<-.38):p.material_index=1
    head=loft('small-rounded-head',[((0,-.046,.203),.004,.006),((0,-.054,.205),.012,.014),((0,-.065,.205),.015,.015),((0,-.076,.203),.013,.012),((0,-.087,.201),.008,.007)],[M['feathers'],M['underside']],16)
    for p in head.data.polygons:
        if p.normal.z<-.4:p.material_index=1
    # Narrow short bill with a modest hook confined to its last 3 mm, not a raptor beak.
    loft('short-pointed-lightly-hooked-bill',[((0,-.085,.201),.007,.006),((0,-.093,.201),.0056,.0045),((0,-.103,.2005),.0034,.0029),((0,-.109,.200),.0014,.0016),((0,-.112,.1987),.00028,.00065)],M['bill_legs'],12)
    for s,label in [(1,'right'),(-1,'left')]:
        eye(label+'-eye',(s*.0143,-.068,.207),(.0013,.0021,.0021))
        loft(label+'-closed-jaw-seam',[((s*.0065,-.089,.1996),.0003,.00025),((s*.0048,-.097,.1994),.00025,.0002),((s*.0024,-.106,.1993),.00017,.00015),((s*.0006,-.110,.1988),.0001,.0001)],M['wing'],6)
        # Feather coverts and five broad overlapping folded remiges form a true feathered wing.
        parts=[]
        for j in range(5):
            a=(s*(.022+.002*j),-.007+.005*j,.165-.002*j);b=(s*(.016+.003*j),.083-.004*j,.132+.001*j)
            parts.append(feather(a,b,.0055,.0022))
        multi(label+'-folded-wing-remiges',parts,M['wing'])
        loft(label+'-wing-coverts',[((s*.022,-.006,.156),.002,.004),((s*.030,.008,.156),.0058,.014),((s*.032,.028,.153),.005,.015),((s*.028,.048,.146),.0045,.012),((s*.020,.067,.138),.002,.006),((s*.016,.075,.134),.0007,.0015)],M['feathers'],12)
        # Actual measured tibia/tarsometatarsus centerline lengths. Hidden femur is inferred.
        shift=-.004 if s==1 else .004;x=s*.021
        ankle=Vector((x,-.009+shift,.0042));hock=ankle+Vector((0,.015,math.sqrt(P['tarsometatarsus_reference_m']**2-.015**2)))
        knee=hock+Vector((0,-.020,math.sqrt(P['tibiotarsus_reference_m']**2-.020**2)))
        hip=Vector((x*.8,.026+shift,.140))
        loft(label+'-feathered-thigh',[(tuple(hip),.010,.013),(tuple(hip.lerp(knee,.55)),.010,.012),(tuple(knee),.006,.007),(tuple(knee.lerp(hock,.15)),.004,.005)],M['feathers'],12)
        loft(label+'-tibiotarsal-leg',[(tuple(knee),.0036,.0039),(tuple(knee.lerp(hock,.55)),.0029,.0032),(tuple(hock),.0033,.0036)],M['bill_legs'],10)
        loft(label+'-tarsometatarsal-leg',[(tuple(hock),.0031,.0033),(tuple(hock.lerp(ankle,.5)),.0023,.0025),(tuple(ankle),.0030,.0024)],M['bill_legs'],10)
        toes=[];claws=[]
        for dx,dy in [(-.012,-.032),(0,-.040),(.012,-.031),(-s*.002,.0085)]:
            end=Vector((x+dx,ankle.y+dy,.0016));mid=ankle.lerp(end,.55);mid.z=.0025
            toes.append(loft_geometry([(tuple(ankle),.0019,.0016),(tuple(mid),.0015,.0014),(tuple(end),.0011,.0012)],8))
            ext=(end-mid).normalized()*.0035;claws.append(loft_geometry([(tuple(end),.0011,.0010),(tuple(end+ext*.60+Vector((0,0,.0003))),.0007,.0006),(tuple(end+ext+Vector((0,0,-.0006))),.00015,.00015)],6))
        multi(label+'-three-forward-toes-and-hallux',toes,M['bill_legs']);multi(label+'-moderate-claws',claws,M['eye_claw'])
    # Seven overlapping long rectrices, fan width an explicitly artistic reconstruction.
    parts=[]
    for j in range(-3,4):
        a=(j*.003,.071,.148-abs(j)*.0008);b=(j*.0068,.188-abs(j)*.007,.127+abs(j)*.0015)
        parts.append(feather(a,b,.0055,.00165,10))
    multi('broad-long-feather-tail',parts,M['wing'])
    # Root centered on paired toe contact extent. Ground all contact geometry without scale normalization.
    meshes=[o for o in C.objects if o.type=='MESH'];foot=[v.co for o in meshes if 'toes' in o.name or 'claws' in o.name for v in o.data.vertices]
    origin_y=(min(v.y for v in foot)+max(v.y for v in foot))/2;floor=min(v.co.z for o in meshes for v in o.data.vertices)
    for o in meshes:
        for v in o.data.vertices:v.co.y-=origin_y;v.co.z-=floor
    bpy.context.view_layer.update();return C

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE.parent);args=ap.parse_args(argv)
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True);build();src=audit_source(C,16000)
    if src['errors']:raise RuntimeError(src['errors'])
    scene=bpy.context.scene;scene['representation']='living-reconstruction';scene['scientific_limits']='Whole body and plumage inferred; measured SMF ME3550 tibia 63.4 mm, tarsometatarsus 55.7 mm; museum species size about 30 cm, not individual measurement.'
    scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.filepath='//render.png';bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'+b' '*1020;space.params.directory=b'//'
    os.chdir(out);bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),relative_remap=False)
    bpy.ops.object.select_all(action='DESELECT')
    for o in C.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Exporter option missing')
    bpy.ops.export_scene.gltf(filepath='model.glb',**options);glb=audit_glb(Path('model.glb'),16000,6,48)
    if glb['errors']:raise RuntimeError(glb['errors'])
    b=src['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]};delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ['min','max'] for i in range(3))
    assert delta<1e-5 and src['triangles']==glb['scene_triangles'] and glb['bytes']<=2200000
    write(out/'qa/evidence/geometry.json',{'source':src,'glb':glb,'bounds_roundtrip_max_error_m':delta,'scope':'Source and static GLB technical geometry audit, not visual or factual acceptance.'})
    import io_scene_gltf2
    write(out/'qa/evidence/build-metadata.json',{'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'gltf_exporter_version':io_scene_gltf2.bl_info['version'],'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'seed':P['seed'],'export_options':options,'threejs_target_version':P['threejs_target_version'],'profile':P['profile'],'origin':'Center of paired toe contact envelope at ground','axes':{'blender_up':'+Z','blender_forward':'-Y','glb_up':'+Y','glb_forward':'+Z'},'scale_status':P['scale_status'],'measured_bone_centerline_m':{'tibiotarsus':P['tibiotarsus_reference_m'],'tarsometatarsus':P['tarsometatarsus_reference_m'],'ratio':P['tarsometatarsus_reference_m']/P['tibiotarsus_reference_m']},'semantic_parts':[p['name'] for p in src['parts']],'materials':[{'name':k,'srgb':v} for k,v in P['palette_srgb'].items()]})
    print('MESSELORNIS_BUILD_OK',glb['sha256'],glb['scene_triangles'],glb['bytes'])
if __name__=='__main__':main()
