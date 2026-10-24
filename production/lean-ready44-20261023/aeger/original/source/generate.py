#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic, original Aeger spinipes living reconstruction.
Run with Blender in background: --python source/generate.py -- --output .
Only source/params.json and the declared source/deps modules are required.
No fossil images, reference meshes, procedural textures or network dependencies.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb, read_glb, semantic_digest

def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lerp(a,b,t):return Vector(a).lerp(Vector(b),t)

def main(out):
    p=json.loads((HERE/'params.json').read_text())
    col=ac.setup_scene(p['asset_id'],p['seed']);root=bpy.data.objects[col['asset_root']]
    root['representation']='living-reconstruction'
    root['mounting_origin']='Swimming specimen: sagittal reference origin at (0,0,0); no floor contact claimed.'
    root['scientific_limit']='Flattened fossil; width, hidden counterparts and living colors reconstructed.'
    mats=[ac.make_material(m['name'],m['srgb'],m.get('roughness',.83)) for m in p['palette']]
    parts=[]
    def mesh(name,v,f,idx,face_mats=None):
        ob=ac.mesh_object(name,v,f,mats if face_mats else mats[idx],col)
        if face_mats:
            for poly,mi in zip(ob.data.polygons,face_mats):poly.material_index=mi
        parts.append(ob);return ob
    def tube(name,points,radii,mat=3,sides=8,ellipses=None,paint=False):
        pts=[Vector(a) for a in points];verts=[];faces=[];fm=[]
        for i,c in enumerate(pts):
            tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
            x=Vector((1,0,0));u=(x-tangent*x.dot(tangent)).normalized()
            if u.length<.5:u=tangent.cross(Vector((0,0,1))).normalized()
            v=tangent.cross(u).normalized()
            # For the sagittal body path v points dorsally.
            if v.z<0:v=-v
            ry=ellipses[i] if ellipses else radii[i]
            for j in range(sides):
                a=math.tau*j/sides
                q=c+u*math.cos(a)*radii[i]+v*math.sin(a)*ry
                verts.append(tuple(q))
        faces.append(tuple(reversed(range(sides))));fm.append(mat)
        for k in range(len(pts)-1):
            for j in range(sides):
                faces.append((k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j))
                a=math.tau*(j+.5)/sides
                fm.append((1 if math.sin(a)>.55 else 2 if math.sin(a)<-.5 else 0) if paint else mat)
        faces.append(tuple((len(pts)-1)*sides+j for j in range(sides)));fm.append(mat)
        return mesh(name,verts,faces,mat,fm if paint else None)
    def sphere(name,c,r,mat):
        # Explicit small ellipsoidal loft, not an untouched UV-sphere primitive.
        return tube(name,[(c[0],c[1],c[2]-r*.92),(c[0],c[1],c[2]-r*.5),(c[0],c[1],c[2]),(c[0],c[1],c[2]+r*.5),(c[0],c[1],c[2]+r*.92)],[r*.2,r*.82,r,r*.82,r*.2],mat,10)
    def blade(name,a,b,width,thick,mat=0):
        a=Vector(a);b=Vector(b);d=(b-a).normalized();u=d.cross(Vector((1,0,0))).normalized()
        if u.length<.5:u=Vector((0,1,0))
        v=d.cross(u).normalized()
        cs=[a,a.lerp(b,.25),a.lerp(b,.67),b]
        widths=[width*.2,width,width*.82,width*.12]
        verts=[]
        for c,w in zip(cs,widths):
            verts.extend([tuple(c+v*w),tuple(c+u*thick),tuple(c-v*w),tuple(c-u*thick)])
        faces=[(3,2,1,0)]
        for k in range(3):
            for j in range(4):faces.append((k*4+j,k*4+(j+1)%4,(k+1)*4+(j+1)%4,(k+1)*4+j))
        faces.append((12,13,14,15));return mesh(name,verts,faces,mat)
    # Continuous primary carapace profile: no slab flattening and no copied mesh.
    body=[(0,-.032,.025),(0,-.028,.0255),(0,-.020,.026),(0,-.010,.026),(0,-.001,.0255),(0,.003,.025)]
    tube('carapace',body,[.0025,.0055,.007,.0068,.0062,.0057],0,16,[.004,.0075,.009,.0085,.0072,.0063],True)
    # Narrow rostrum with raised dorsal profile; A. spinipes, not a short hooked rostrum.
    tube('rostrum',[(0,-.027,.033),(0,-.036,.035),(0,-.046,.036),(0,-.057,.0368),(0,-.062,.0365)],[.00135,.00085,.00055,.00028,.00007],1,8,[.0011,.0012,.0008,.00045,.00007])
    tube('subrostral_spine',[(0,-.038,.0344),(0,-.0405,.0321)],[.00045,.00007],4,6)
    # Six curved, overlapping abdominal somites, with inset flexible joints.
    centers=[Vector(q) for q in p['abdominal_centerline_m']]
    widths=[.0062,.0063,.0059,.0054,.0048,.0039,.0028]
    heights=[.0068,.007,.0066,.006,.0052,.0043,.0032]
    for i in range(6):
        a,b=centers[i],centers[i+1]
        c=[a.lerp(b,t) for t in (.012,.20,.58,.86,.975)]
        w=[widths[i]*.94,widths[i],(widths[i]+widths[i+1])*.51,widths[i+1]*1.035,widths[i+1]*.97]
        h=[heights[i]*.94,heights[i],(heights[i]+heights[i+1])*.51,heights[i+1]*1.035,heights[i+1]*.97]
        tube('abdomen_%02d'%(i+1),c,w,0,16,h,True)
        if i<5:tube('articulation_%02d'%(i+1),[a.lerp(b,.91),b.lerp(centers[i+2],.11)],[widths[i+1]*.87,widths[i+1]*.84],3,12,[heights[i+1]*.85]*2)
        # Ventrolateral pleural lobes are short body plates, not extra leg pairs.
        d=(b-a).normalized();down=Vector((0,-d.z,d.y))
        if down.z>0:down=-down
        mid=a.lerp(b,.55)
        for s,label in [(-1,'L'),(1,'R')]:
            platebase=mid+Vector((s*(w[2]*.84),0,0))
            blade('pleuron_%02d_%s'%(i+1,label),platebase,platebase+down*h[2]*.73+d*.001,w[2]*.34,.0004,0)
    end=centers[-1]
    tube('telson',[end,end+Vector((0,-.003,-.006)),end+Vector((0,-.007,-.012))],[.00265,.0021,.0003],1,10,[.0022,.0013,.00023])
    for s,label in [(-1,'L'),(1,'R')]:
        # Two uropod blades on each side plus central telson make the tail fan.
        blade('uropod_inner_'+label,end+Vector((s*.001,0,0)),end+Vector((s*.007,-.0075,-.012)),.0031,.00045,0)
        blade('uropod_outer_'+label,end+Vector((s*.0015,.001,0)),end+Vector((s*.0115,-.0028,-.010)),.0034,.00045,2)
        tube('eye_stalk_'+label,[(s*.0035,-.0305,.029),(s*.0077,-.034,.030)],[.0009,.00072],2,8)
        sphere('eye_'+label,(s*.0084,-.0348,.0305),.00155,5)
        # Long flexible antennae and paired bifurcating antennules, clearly separate.
        antenna=[(s*.003,-.033,.025),(s*.005,-.040,.024),(s*.009,-.055,.021),(s*.016,-.075,.020),(s*.024,-.096,.022),(s*.030,-.119,.026),(s*.031,-.132,.032)]
        tube('antenna_'+label,antenna,[.00063,.00055,.00043,.00034,.00027,.00018,.00009],3,7)
        antennule=[(s*.0023,-.033,.030),(s*.004,-.042,.031),(s*.006,-.050,.032)]
        tube('antennule_peduncle_'+label,antennule,[.00063,.00048,.00035],2,7)
        for j in (0,1):
            tube('antennule_flagellum_%s_%s'%(label,j),[antennule[-1],(s*(.009+j*.004),-.064,.033+j*.002),(s*(.012+j*.008),-.083+j*.007,.035+j*.004)],[.0003,.00021,.00009],3,6)
        # Main diagnostic gate: elongated, jointed and visibly spinose third maxilliped.
        mx=[(s*.005,-.027,.021),(s*.009,-.034,.015),(s*.015,-.050,.004),(s*.021,-.071,-.007),(s*.022,-.084,-.011)]
        for k in range(4):
            a,b=Vector(mx[k]),Vector(mx[k+1]);rad=[.00135,.00115,.0009,.00068][k]
            tube('maxilliped3_%s_segment%d'%(label,k+1),[a,a.lerp(b,.18),a.lerp(b,.85),b],[rad*.75,rad,rad*.82,rad*.55],3,9)
        for k in (1,2,3):
            a,b=Vector(mx[k]),Vector(mx[k+1]);n=[0,5,7,4][k]
            for j in range(n):
                t=(j+.5)/n;c=a.lerp(b,t)
                length=.0025 if k==1 else .0032 if k==2 else .0022
                # Laterally projecting sparse row with an anterior inclination.
                tip=c+Vector((s*length,-.0008,-.0011))
                tube('maxilliped3_%s_spine_%d_%02d'%(label,k,j+1),[c,tip],[.00028,.000055],4,6)
        tube('maxilliped3_terminal_'+label,[mx[-1],(s*.0213,-.087,-.012)],[.00042,.00006],4,7)
        # Five thoracic walking pairs, the first three with small chelate tips.
        for i,y in enumerate([-.022,-.016,-.010,-.004,.002]):
            yoff=[-.022,-.013,-.003,.009,.020][i]
            hip=(s*.0058,y,.021)
            knee=(s*(.0135+i*.001),y+yoff*.50,.006-i*.0005)
            wrist=(s*(.0195+i*.001),y+yoff,-.008-i*.001)
            tip=(s*(.018+i*.001),y+yoff-.007,-.015-i*.0005)
            points=[hip,knee,wrist,tip]
            for k in range(3):
                a,b=Vector(points[k]),Vector(points[k+1]);r=[.0008,.00067,.00044][k]*(1-i*.045)
                tube('pereiopod_%d_%s_segment%d'%(i+1,label,k+1),[a,a.lerp(b,.15),a.lerp(b,.87),b],[r*.7,r,r*.8,r*.48],3,7)
            if i<3:
                base=Vector(tip);d=Vector((s*-.001,-.003,-.0006))
                tube('pereiopod_%d_%s_fixed_finger'%(i+1,label),[base,base+d+Vector((s*.0006,0,0))],[.00034,.000055],2,6)
                tube('pereiopod_%d_%s_movable_finger'%(i+1,label),[base+Vector((s*.0008,0,0)),base+d+Vector((s*-.0003,.0004,.0003))],[.0003,.000055],2,6)
                a,b=Vector(knee),Vector(wrist)
                for j in range(3):
                    c=a.lerp(b,(j+1)/4)
                    tube('pereiopod_%d_%s_spine%d'%(i+1,label,j),[c,c+Vector((s*.0013,-.0005,-.0007))],[.00021,.00005],4,6)
            else:
                tube('pereiopod_%d_%s_simple_tip'%(i+1,label),[tip,Vector(tip)+Vector((s*-.0003,-.002,-.0005))],[.00024,.000055],4,6)
        # Small biramous pleopods beneath the first five abdominal somites.
        for i in range(5):
            c=centers[i].lerp(centers[i+1],.5);c+=Vector((s*.003,0,-heights[i]*.75))
            q=c+Vector((s*.0015,-.001,-.003))
            tube('pleopod_%d_%s_base'%(i+1,label),[c,q],[.00048,.00032],2,6)
            for j in range(2):
                blade('pleopod_%d_%s_branch%d'%(i+1,label,j),q,q+Vector((s*(.0015+j*.001),-.002-j*.001,-.0035)),.0008,.00017,2)
    # Save editable semantic parts before export-only batching and preview changes.
    source=ac.audit_source(col,max_triangles=p['budgets']['max_triangles'])
    if source['errors']:raise RuntimeError('; '.join(source['errors']))
    out.mkdir(parents=True,exist_ok=True);ev=out/'qa/evidence';ev.mkdir(parents=True,exist_ok=True)
    bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s'
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//preview'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
                    space.params.filename=''
    # Remove unused factory image data and external paths before source saving.
    for image in list(bpy.data.images):
        if image.users==0:bpy.data.images.remove(image)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    # Merge mesh data into one export mesh with six shared palette primitives.
    vv=[];ff=[];mi=[]
    for ob in parts:
        offset=len(vv);vv.extend(tuple(ob.matrix_world@v.co) for v in ob.data.vertices)
        for poly in ob.data.polygons:
            ff.append(tuple(offset+i for i in poly.vertices));mi.append(mats.index(ob.data.materials[poly.material_index]))
    bat=ac.mesh_object('aeger-export-mesh',vv,ff,mats,col)
    for poly,i in zip(bat.data.polygons,mi):poly.material_index=i
    for ob in parts:bpy.data.objects.remove(ob,do_unlink=True)
    bpy.ops.object.select_all(action='DESELECT');root.select_set(True);bat.select_set(True);bpy.context.view_layer.objects.active=root
    opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Exporter options unavailable')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**opts)
    glb=audit_glb(out/'model.glb',p['budgets']['max_triangles'],p['budgets']['max_materials'],p['budgets']['max_primitives'])
    glb['file']='model.glb'
    if glb['errors']:raise RuntimeError('; '.join(glb['errors']))
    if glb['bytes']>p['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    bb=source['bounds_blender_m'];expected={'min':[bb['min'][0],bb['min'][2],-bb['max'][1]],'max':[bb['max'][0],bb['max'][2],-bb['min'][1]]}
    delta=max(abs(glb['bounds_m'][side][i]-expected[side][i]) for side in ('min','max') for i in range(3))
    assert delta<1e-6 and glb['scene_triangles']==source['triangles']
    doc,binary,_=read_glb(out/'model.glb')
    write(ev/'source-glb.json',{'status':'PASS','claim_scope':'Source and static uncompressed GLB geometry checks only; not independent visual approval or GPU rendering.','blender_version':bpy.app.version_string,'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':opts,'semantic_digest':semantic_digest(doc,binary),'source_generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'source_parts':len(parts),'export_meshes':1,'warning_review':{'mount':'Swimming animal uses the declared body center mounting origin; no floor-contact claim.','assembly':'Closed semantic shells intentionally overlap at articulations and appendage roots.','renderable_thin_features':'Antenna and spine terminal radii are conservative display thicknesses, not microscopic measurements.'}})
    write(ev/'anatomy.json',{'glb_sha256':sha(out/'model.glb'),'representation':'living-reconstruction','primary_specimen':'MNHN.F.B13441','scale_source':'Charbonnier and Garassino 2012 Fig. 1A, same-panel 20 mm scale bar','measurements_are':'Approximate figure-derived proportions, not published specimen measurements','body_centerline_arclength_m':.035+sum((centers[i+1]-centers[i]).length for i in range(6))+math.sqrt(.007**2+.012**2),'carapace_length_m':.035,'rostrum_length_from_carapace_front_m':.030,'third_maxilliped_root_to_tip_m':(Vector((.0213,-.087,-.012))-Vector((.005,-.027,.021))).length,'abdominal_somites':6,'third_maxilliped_pairs':1,'pereiopod_pairs':5,'small_chelate_pereiopod_pairs':3,'simple_pereiopod_pairs':2,'pleopod_pairs_conservatively_reconstructed':5,'uropod_blades':4,'living_palette':'Artistic subdued ochre/brown; fossil color is not a living-color claim.','uncertain':['Three-dimensional body width from a compressed fossil','Contralateral appendage completion','Fine appendage and spine arrangement','Antenna and antennule endpoints','Living color']})
    print('AEGER_BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
if __name__=='__main__':
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path.cwd());args=parser.parse_args(argv);main(args.output.resolve())
