# SPDX-License-Identifier: MIT
"""Deterministic Vegavis genus-level composite reconstruction.
Run with Blender 4.3.2 in background mode, then pass -- --output-dir OUTPUT.
All code dependencies are bundled beside this generator. No reference image is embedded.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def tube_geometry(rows,sides=12):
    """Oriented elliptical profile loft: rows are center, halfwidth, halfdepth."""
    verts=[]; faces=[]
    centers=[Vector(r[0]) for r in rows]
    for i,(c,rx,rz) in enumerate(rows):
        c=Vector(c); tangent=(centers[min(i+1,len(rows)-1)]-centers[max(i-1,0)]).normalized()
        ref=Vector((1,0,0))
        if abs(tangent.dot(ref))>.95: ref=Vector((0,1,0))
        u=(ref-tangent*ref.dot(tangent)).normalized(); v=tangent.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides
            verts.append(tuple(c+u*(rx*math.cos(a))+v*(rz*math.sin(a))))
    for i in range(len(rows)-1):
        for j in range(sides): faces.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    verts.extend([tuple(centers[0]),tuple(centers[-1])]); a=len(verts)-2;b=len(verts)-1
    for j in range(sides): faces.extend([(a,(j+1)%sides,j),(b,(len(rows)-1)*sides+j,(len(rows)-1)*sides+(j+1)%sides)])
    return verts,faces

def tube(name,rows,mat,sides=12):
    v,f=tube_geometry(rows,sides); return mesh_object(name,v,f,mat,C)

def multi(name,parts,mat):
    verts=[];faces=[]
    for v,f in parts:
        n=len(verts);verts.extend(v);faces.extend(tuple(n+x for x in q) for q in f)
    return mesh_object(name,verts,faces,mat,C)

def ellipsoid(name,center,radii,mat,n=12,rings=7):
    c=Vector(center); v=[tuple(c+Vector((0,0,-radii[2])))];f=[]
    for k in range(1,rings):
        a=-math.pi/2+math.pi*k/rings
        for j in range(n):
            t=2*math.pi*j/n;v.append(tuple(c+Vector((radii[0]*math.cos(a)*math.cos(t),radii[1]*math.cos(a)*math.sin(t),radii[2]*math.sin(a)))))
    v.append(tuple(c+Vector((0,0,radii[2]))));top=len(v)-1
    for j in range(n):f.extend([(0,1+(j+1)%n,1+j),(top,1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n)])
    for k in range(rings-2):
        for j in range(n):f.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
    return mesh_object(name,v,f,mat,C)

def feather_geometry(a,b,width,thickness,sides=8):
    a,b=Vector(a),Vector(b);rows=[]
    for t,w in [(0,.25),(.18,.82),(.45,1),(.72,.74),(.94,.25),(1,.035)]:rows.append((tuple(a.lerp(b,t)),width*w,thickness*w))
    return tube_geometry(rows,sides)

def web_geometry(side,yshift):
    # Closed three-lobed web with recessed margins; skin and webbing are inferred.
    x=side*.030
    outline=[(x-.009,.019+yshift),(x-.019,-.033+yshift),(x-.009,-.026+yshift),(x,-.048+yshift),(x+.010,-.027+yshift),(x+.020,-.034+yshift),(x+.011,.019+yshift)]
    zlo=.002;zhi=.005
    verts=[(a,b,zlo) for a,b in outline]+[(a,b,zhi) for a,b in outline]
    # Convex fan from the ankle-side center avoids filling the concave toe notches incorrectly.
    n=len(outline); center=(x,.008+yshift)
    verts.extend([(center[0],center[1],zlo),(center[0],center[1],zhi)])
    faces=[]
    for j in range(n):
        k=(j+1)%n;faces.extend([(2*n,k,j),(2*n+1,n+j,n+k),(j,k,n+k,n+j)])
    return verts,faces

def build():
    global C,M
    C=setup_scene(P['asset_id'],P['seed']);M={k:make_material(k,v,roughness=.84 if k!='eye' else .36) for k,v in P['palette_srgb'].items()}
    # One continuous body and S-neck avoids a stacked-sphere neck silhouette.
    rows=[((0,.102,.183),.005,.006),((0,.088,.199),.021,.023),((0,.066,.219),.032,.039),((0,.036,.243),.043,.050),((0,.005,.270),.037,.045),((0,-.022,.294),.025,.030),((0,-.039,.318),.018,.021),((0,-.033,.339),.015,.018),((0,-.028,.358),.014,.017),((0,-.036,.379),.015,.017),((0,-.054,.399),.018,.020),((0,-.064,.410),.015,.014)]
    rows=[((c[0],c[1],c[2]-(.030 if i<6 else .020 if i==6 else .010 if i==7 else .004 if i==8 else 0)),rx,rz) for i,(c,rx,rz) in enumerate(rows)]
    body=tube('body-and-curved-neck',rows,[M['body'],M['under']],16)
    for f in body.data.polygons:
        c=f.center
        # Countershading on forward-facing neck and underside of torso, with faceted boundary.
        if (c.z<.295 and f.normal.z<-.25) or (c.z>.285 and f.normal.y<-.35):f.material_index=1
    head=tube('small-rounded-braincase',[((0,-.035,.408),.003,.004),((0,-.044,.410),.016,.017),((0,-.059,.408),.023,.022),((0,-.076,.407),.022,.020),((0,-.094,.405),.015,.013),((0,-.108,.402),.009,.007)],[M['body'],M['under']],16)
    for f in head.data.polygons:
        if f.normal.z<-.35:f.material_index=1
    tube('long-narrow-pointed-bill',[((0,-.102,.402),.010,.0075),((0,-.118,.400),.009,.0068),((0,-.139,.398),.0068,.0050),((0,-.160,.395),.0043,.0032),((0,-.180,.392),.0018,.0018),((0,-.186,.391),.00045,.0005)],M['bill'],12)
    for s,label in [(1,'right'),(-1,'left')]:
        ellipsoid(label+'-eye',(s*.0218,-.074,.4135),(.0028,.0033,.0033),M['eye'],n=10,rings=6)
        # Subtle closed jaw seam, no teeth and no spoon-shaped enlargement.
        tube(label+'-jaw-line',[((s*.0085,-.115,.399),.0005,.00045),((s*.0066,-.138,.3972),.00042,.00035),((s*.0038,-.161,.3944),.00028,.00024),((s*.0012,-.180,.3919),.00014,.00013)],M['wing'],6)
        # Folded flight wing, layered coverts over tapered remiges. No flipper.
        wingparts=[]
        for j in range(5):
            a=(s*(.035+.003*j),-.002+.007*j,.264-.004*j)
            b=(s*(.020+.005*j),.106-.003*j,.174+.004*j)
            wingparts.append(feather_geometry(a,b,.0065,.0030,8))
        multi(label+'-folded-flight-feathers',wingparts,M['wing'])
        tube(label+'-wing-coverts',[((s*.029,-.017,.269),.004,.004),((s*.039,.001,.263),.008,.025),((s*.042,.025,.244),.008,.029),((s*.037,.051,.223),.007,.023),((s*.027,.078,.201),.005,.012),((s*.020,.091,.187),.001,.002)],M['body'],12)
        # Strong posterior limbs follow the published flexed profile; thigh is feathered.
        shift=-.004 if s==1 else .004
        tube(label+'-feathered-thigh',[((s*.022,.051+shift,.218),.013,.017),((s*.027,.065+shift,.186),.013,.017),((s*.030,.077+shift,.155),.010,.012),((s*.031,.085+shift,.137),.006,.007)],M['body'],12)
        tube(label+'-lower-leg',[((s*.030,.078+shift,.155),.0068,.0074),((s*.031,.088+shift,.119),.0058,.0066),((s*.031,.100+shift,.077),.0048,.0056),((s*.031,.096+shift,.066),.0058,.0056)],M['foot'],10)
        tube(label+'-tarsometatarsus',[((s*.031,.097+shift,.069),.0052,.0053),((s*.030,.076+shift,.044),.0042,.0046),((s*.030,.049+shift,.019),.0037,.0042),((s*.030,.025+shift,.007),.0045,.0036)],M['foot'],10)
        toes=[]
        for dx,end_y in [(-.018,-.035),(0,-.050),(.020,-.036)]:
            toes.append(tube_geometry([((s*.030,.026+shift,.006),.003,.0025),((s*.030+dx*.45,-.003+shift,.004),.0024,.0020),((s*.030+dx,end_y+shift,.0025),.0018,.0017)],8))
        toes.append(tube_geometry([((s*.030,.024+shift,.005),.0021,.0017),((s*.030-s*.008,.042+shift,.0025),.0018,.0015)],8))
        multi(label+'-swimming-toes',toes,M['foot'])
        v,f=web_geometry(s,shift);mesh_object(label+'-inferred-webbing',v,f,M['foot'],C)
    tail=[]
    for j in range(5):
        x=(j-2)*.006
        tail.append(feather_geometry((x*.65,.083,.204),(x,.129-abs(j-2)*.005,.150+abs(j-2)*.004),.0055,.0028,8))
    multi('short-feathered-tail',tail,M['wing'])
    # Lower the body/flight feathers together; extend the S-neck rather than elongating the naked legs.
    for o in C.objects:
        if o.type=='MESH' and any(tag in o.name for tag in ['folded-flight-feathers','wing-coverts','feathered-thigh','short-feathered-tail']):
            for v in o.data.vertices:v.co.z-=.030
        if o.type=='MESH' and 'lower-leg' in o.name:
            for v in o.data.vertices:v.co.z-=.030*max(0,min(1,(v.co.z-.07)/.085))
    # Set a literal 43 cm artistic standing extent, preserving all proportions.
    zs=[v.co.z for o in C.objects if o.type=='MESH' for v in o.data.vertices]
    z0=min(zs); scale=P['standing_height_model_m']/(max(zs)-z0)
    # Root at center of toe contact envelope, not the visual bounding box.
    foot_y=-.003
    for o in C.objects:
        if o.type=='MESH':
            for v in o.data.vertices:v.co=Vector((v.co.x*scale,(v.co.y-foot_y)*scale,(v.co.z-z0)*scale))
    bpy.context.view_layer.update()
    return C

def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE.parent);a=ap.parse_args(args)
    output=a.output_dir.resolve();output.mkdir(parents=True,exist_ok=True);build()
    src=audit_source(C,max_triangles=16000)
    if src['errors']:raise RuntimeError(src['errors'])
    bpy.context.scene['representation']='genus-level composite living reconstruction'
    bpy.context.scene['scientific_limits']='AMNH FARB 30899 skull reassigned V. notopothousa in 2026; body is comparative composite; feathers, webbing, colors inferred.'
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//render.png'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//' + b' '*1020
                    space.params.directory=b'//'
    # Keep saved source free of authoring text blocks, external images and render scenes.
    os.chdir(output);bpy.ops.wm.save_as_mainfile(filepath=str(output/'model.blend'),relative_remap=False)
    bpy.ops.object.select_all(action='DESELECT')
    for o in C.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Exporter option unavailable')
    bpy.ops.export_scene.gltf(filepath='model.glb',**options)
    glb=audit_glb(Path('model.glb'),max_triangles=16000,max_materials=6,max_primitives=48)
    if glb['errors']:raise RuntimeError(glb['errors'])
    b=src['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ['min','max'] for i in range(3))
    assert delta<.00001 and src['triangles']==glb['scene_triangles'] and glb['bytes']<=2200000
    write(output/'qa/evidence/geometry.json',{'source':src,'glb':glb,'bounds_roundtrip_max_error_m':delta,'scope':'Source mesh and emitted static GLB numeric checks only; no independent appearance or GPU claim.'})
    import io_scene_gltf2
    write(output/'qa/evidence/build-metadata.json',{'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'gltf_exporter_version':io_scene_gltf2.bl_info['version'],'seed':P['seed'],'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(output/'model.glb'),'blend_sha256':sha(output/'model.blend'),'export_options':options,'threejs_target_version':P['threejs_target_version'],'profile':P['profile'],'origin':'Center of paired toe contact envelope at floor; not body-bounds center.','axes':{'blender_up':'+Z','blender_forward':'-Y','glb_up':'+Y','glb_forward':'+Z'},'scale_status':P['scale_status'],'semantic_parts':[p['name'] for p in src['parts']],'materials':[{'name':k,'srgb':v} for k,v in P['palette_srgb'].items()]})
    print('VEGAVIS_BUILD_OK',glb['sha256'],glb['scene_triangles'],glb['bytes'])
if __name__=='__main__':main()
