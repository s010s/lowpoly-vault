# SPDX-License-Identifier: MIT
"""Original specimen-guided fossil. Run in Blender with -- --output-dir OUT."""
import argparse, hashlib, json, math, random, sys
from pathlib import Path
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE/'deps'))
import bpy, bmesh
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n')
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    p=json.loads((SOURCE/'params.json').read_text())
    collection=setup_scene(p['asset_id'],p['seed'])
    materials=[make_material(x['name'],x['srgb'],roughness=x['roughness']) for x in p['palette']]
    verts,faces,mids=[],[],[]
    n=p['section_vertices']; rings=p['growth_rings']; max_theta=p['coiling_radians']; growth=p['logarithmic_growth']
    # An expanding coiled loft, not a traced photograph. Broad collabral
    # undulations are original simplifications of observed growth directions.
    def section(theta,phi):
        e=math.exp(-growth*theta); r=p['final_coiling_radius_mm']*e
        a=p['aperture_major_mm']*.5*e; b=p['aperture_minor_mm']*.5*e
        twist=math.radians(p['aperture_major_tilt_degrees'])*math.exp(-theta/1.9)
        radial=Vector((math.cos(theta),math.sin(theta),0)); vertical=Vector((0,0,1))
        u=radial*math.cos(twist)+vertical*math.sin(twist)
        v=-radial*math.sin(twist)+vertical*math.cos(twist)
        center=Vector((r*math.cos(theta),r*math.sin(theta),p['aperture_center_height_mm']+p['apex_rise_mm']*(1-math.exp(-theta/1.2))))
        ridge=1+.018*math.sin(theta*18+.85*math.sin(phi)+.5*math.sin(2*phi))+.010*math.sin(theta*9.4+.35*math.cos(3*phi))
        irregular=1+.045*math.cos(3*phi+.4)*math.exp(-theta/2.5)+.025*math.sin(5*phi-.7)*math.exp(-theta/1.8)
        co=center+(u*(a*math.cos(phi))+v*(b*math.sin(phi)))*ridge*irregular
        end_weight=math.exp(-theta/.22)
        co.y+=end_weight*(.62*math.sin(3*phi+.7)+.28*math.sin(7*phi-.8)+.65*math.exp(-((phi-4.8)/.32)**2))
        return co,center
    for j in range(rings):
        theta=max_theta*(1-j/(rings-1))
        for i in range(n): verts.append(list(section(theta,2*math.pi*i/n)[0]))
    for j in range(rings-1):
        for i in range(n):
            faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i)); mids.append(0)
    tip=sum((Vector(v) for v in verts[:n]),Vector())/n
    tip_index=len(verts); verts.append(list(tip))
    for i in range(n): faces.append((tip_index,(i+1)%n,i)); mids.append(0)
    final_start=(rings-1)*n; _,aperture_center=section(0,0)
    lip_start=len(verts)
    for i in range(n):
        phi=2*math.pi*i/n; co=Vector(verts[final_start+i]); c=aperture_center.copy(); c.y=co.y
        co=c+(co-c)*(.94+.025*math.sin(phi*4+.2)+.010*math.sin(phi*7-.9)); co.y+=.12; verts.append(list(co))
    for i in range(n): faces.append((final_start+i,final_start+(i+1)%n,lip_start+(i+1)%n,lip_start+i)); mids.append(1)
    # Preserved short internal wall. Aperture remains substantially mineral-filled.
    fill_start=len(verts)
    for i in range(n):
        phi=2*math.pi*i/n; co=Vector(verts[lip_start+i]); c=aperture_center.copy(); c.y=co.y
        co=c+(co-c)*.975; co.y+=.30+.05*math.sin(3*phi+.4); verts.append(list(co))
    for i in range(n): faces.append((lip_start+i,lip_start+(i+1)%n,fill_start+(i+1)%n,fill_start+i)); mids.append(1)
    # A jittered Cartesian mineral mesh prevents radial-star triangulation from
    # inventing shell septa or other biological structures on this filled mouth.
    points=[Vector((verts[fill_start+i][0],verts[fill_start+i][2])) for i in range(n)]
    def inside(x,z):
        odd=False
        for i in range(n):
            a=points[i]; b=points[(i+1)%n]
            if (a.y>z)!=(b.y>z) and x<(b.x-a.x)*(z-a.y)/(b.y-a.y)+a.x: odd=not odd
        return odd
    rng=random.Random(p['seed'])
    for ix in range(-10,31):
        for iz in range(-5,26):
            x=ix*.95+rng.uniform(-.26,.26); z=iz*.95+rng.uniform(-.26,.26)
            if inside(x,z) and min((Vector((x,z))-q).length for q in points[:n])>.48: points.append(Vector((x,z)))
    vv,ee,ff,orig_v,orig_e,orig_f=delaunay_2d_cdt(points,[(i,(i+1)%n) for i in range(n)],[list(range(n))],1,1e-6,True)
    mapping=[]
    for j,v in enumerate(vv):
        boundary=[i for i in orig_v[j] if i<n]
        if boundary: mapping.append(fill_start+boundary[0]); continue
        c2=Vector((aperture_center.x,aperture_center.z)); ray=v-c2
        def cross(a,b): return a.x*b.y-a.y*b.x
        candidates=[]
        for i in range(n):
            edge=points[(i+1)%n]-points[i]; q=points[i]-c2; den=cross(ray,edge)
            if abs(den)<1e-9: continue
            t=cross(q,edge)/den; u=cross(q,ray)/den
            if t>0 and 0<=u<=1: candidates.append((t,i,u))
        t,i,u=min(candidates)
        fraction=min(1,1/t); weight=fraction**3
        boundary_y=verts[fill_start+i][1]*(1-u)+verts[fill_start+(i+1)%n][1]*u
        y=boundary_y*weight+.50*(1-weight)
        y+=(.17*math.sin(v.x*1.8+v.y*1.1)+.13*math.cos(v.x*2.2-v.y*2.7)+rng.uniform(-.06,.06))*(1-weight)
        mapping.append(len(verts)); verts.append([v.x,y,v.y])
    for j,face in enumerate(ff):
        centroid=sum((vv[i] for i in face),Vector((0,0)))/len(face)
        if not inside(centroid.x,centroid.y): continue
        faces.append(tuple(mapping[i] for i in face)); mids.append(2+int(j%29==0))
    # Global calibration to the actual ds/ws/hs, never unit-cube scaling.
    low=[min(v[i] for v in verts) for i in range(3)]; high=[max(v[i] for v in verts) for i in range(3)]
    target=p['target_dimensions_m']; factors=[target[i]/(high[i]-low[i]) for i in range(3)]
    for co in verts:
        for i in range(3): co[i]=(co[i]-(low[i] if i==2 else (low[i]+high[i])/2))*factors[i]
    shell=mesh_object('Recurved-shell-with-retained-lip-and-mineral-fill',verts,faces,materials,collection)
    for poly,mi in zip(shell.data.polygons,mids): poly.material_index=mi; poly.use_smooth=False
    shell['morphology']='Irregular recurved cap shell, early coil and shallow mineral-filled aperture'
    shell['specimen_anchor']='PIN 5489/16-4; Platyceras vetustum; Mazaev 2021 Fig. 10 c1-c5'
    shell['preservation']='Original fossil interpretation, not a scan. Lost lip and internal anatomy not reconstructed.'
    root=bpy.data.objects[collection['asset_root']]
    root['era']='carboniferous'; root['age_context']='Lower Carboniferous; Visean-Serpukhovian boundary-bed assemblage'
    root['reference_doi']='10.1134/S0031030121080049'
    root['geometry_profile']='Original palette-only static low-poly fossil; no source media embedded'
    bpy.context.scene['asset_license']='CC-BY-4.0'; bpy.context.scene['asset_author']='Leon Made This / s010s'
    source_report=audit_source(collection,24000)
    if source_report['errors']:
        write(out/'qa/evidence/source.json',source_report); raise RuntimeError(str(source_report['errors']))
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in collection.all_objects: ob.select_set(True)
    bpy.context.view_layer.objects.active=root
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
        export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
        export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
        export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available: raise RuntimeError('Missing export flags: '+str(set(options)-available))
    bpy.ops.export_scene.gltf(**options)
    report=audit_glb(out/'model.glb',max_triangles=24000,max_materials=6,max_primitives=16)
    if report['errors'] or report['bytes']>2500000: raise RuntimeError(str(report['errors']))
    src=source_report['bounds_blender_m']
    expected={'min':[src['min'][0],src['min'][2],-src['max'][1]],'max':[src['max'][0],src['max'][2],-src['min'][1]]}
    delta=max(abs(report['bounds_m'][s][i]-expected[s][i]) for s in ('min','max') for i in range(3))
    assert delta<1e-7 and report['scene_triangles']==source_report['triangles']
    bm=bmesh.new(); bm.from_mesh(shell.data)
    topology={'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),
        'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),
        'euler_characteristic':len(bm.verts)-len(bm.edges)+len(bm.faces)}; bm.free()
    aperture=[Vector(verts[final_start+i]) for i in range(n)]
    diameters=[(aperture[i]-aperture[(i+n//2)%n]).length for i in range(n//2)]
    bind={'glb_sha256':digest(out/'model.glb'),'generator_sha256':digest(__file__),'params_sha256':digest(SOURCE/'params.json')}
    write(out/'qa/evidence/source.json',{**bind,**source_report,'topology':topology})
    write(out/'qa/evidence/glb.json',report)
    write(out/'qa/evidence/build.json',{**bind,'blender_version':bpy.app.version_string,'exporter':'Blender glTF 2.0 exporter 4.3.47',
        'generator_seed':p['seed'],'geometry_profile':'palette-only','canonical_helper_sha256':digest(SOURCE/'deps/asset_common.py'),
        'audit_helper_sha256':digest(SOURCE/'deps/qa_glb.py'),'export_options':{k:v for k,v in options.items() if k!='filepath'},
        'bounds_roundtrip_max_error_m':delta,'source_glb_triangles_equal':True,'measured_dimensions_m':src['size'],
        'calibration_m_per_authored_mm':factors,'aperture_opposite_rim_distance_m':{'min':min(diameters),'max':max(diameters)},
        'artistic_choices':['Original simplified irregular growth undulations and chipped lip.','Shallow mineral-filled opening, no invented lumen.',
        'Matte fossil color is artistic; source photographs are grayscale.'],
        'coordinate_origin':'Centered XY extents and lowest shell contact Z=0; identity root.'})
    print('GENERATED',json.dumps({'triangles':report['scene_triangles'],'bytes':report['bytes'],'sha256':report['sha256']}))
if __name__=='__main__': main()
