# SPDX-License-Identifier: MIT
"""Original deterministic interpretation of Struthioptera aff. osiris specimen 268.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUT
No private research images or undeclared local model files are required at runtime.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o): Path(p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,default=HERE.parent); ap.add_argument('--gray',action='store_true'); a=ap.parse_args(argv)
    p=json.loads((HERE/'params.json').read_text()); out=a.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    evidence=out/'qa'/'evidence'; evidence.mkdir(parents=True,exist_ok=True)
    col=setup_scene(p['asset_id'],p['seed']); root=bpy.data.objects[col['asset_root']]
    root['taxon']='Struthioptera aff. osiris'; root['reference_specimen']='Weidemeyer 2009 specimen 268, Plate 14 Figure 9'
    root['reconstruction_limit']='Adapertural exterior documented; depth and shallow reverse recess inferred.'
    root['origin']='Surviving basal shell contact centered on x=0,y=0; no display base.'
    pal=['#A99B83','#A49780','#B0A28B','#6C6355'] if not a.gray else ['#949494']*4
    mats=[make_material(n,c,roughness=.9) for n,c in zip(['Fossil limestone','Weathered recess','Worn high points','Inferred cavity'],pal)]
    # Deliberate closed radial loft, with four retained stepped spire whorls.
    profile=p['body_profile_mm']; n=p['angular_segments']; verts=[]
    for k,(z,r) in enumerate(profile):
        for i in range(n):
            t=math.tau*i/n
            # Shoulder nodules are geometry, not glued-on balls. Coarsest on spire.
            peaks=sum(amp*math.exp(-((z-at)/width)**2) for at,amp,width in [(10,.28,1.1),(17.2,.48,1.1),(26.4,.95,1.1),(32,.70,.8),(36.8,.36,.7),(40.8,.21,.65)])
            nod=peaks*(max(0,math.cos(16*t+.3*z))**3)
            sculpt=.095*math.sin(2.9*z+.75*t)*math.exp(-((z-16)/13)**4)
            rr=r+nod+sculpt
            zoff=.48*math.sin(t)*min(1,z/3,(44-z)/3)
            cx=-5.0*max(0,1-z/15)**1.4 if z<24 else -.35*(z-24)/20
            x=cx+rr*math.cos(t)
            y=rr*.92*math.sin(t)
            # The unseen aperture is NOT restored: only a shallow ovoid back recess.
            if math.sin(t)>.0 and 3<z<23:
                recess=2.1*math.exp(-((z-13)/7)**4)*max(0,math.sin(t))**14
                y-=recess
            verts.append((x,y,z+zoff))
    faces=[]
    for k in range(len(profile)-1):
        for i in range(n): faces.append((k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i))
    # One planar cap at each preserved blunt end, not a fabricated needle.
    faces.append(tuple(reversed(range(n)))); faces.append(tuple((len(profile)-1)*n+i for i in range(n)))
    body_width=max(v[0] for v in verts)-min(v[0] for v in verts)
    verts=[(x*25/body_width,y,z) for x,y,z in verts]
    body=mesh_object('Shell body and four preserved whorls',verts,faces,mats,col)
    # Broad wing: an original hand-shaped concave outline, thickened continuously.
    outline=p['wing_outline_xz_mm']; polygon=[Vector((x,0,z)) for x,z in outline]
    tris=tessellate_polygon([polygon]); index={tuple(v):i for i,v in enumerate(polygon)}
    tv=[tuple(v if isinstance(v,int) else index[tuple(v)] for v in tri) for tri in tris]
    # Subdivide the polygon triangles with shared midpoint vertices before cupping.
    points=[(x,z) for x,z in outline]
    boundary=[(i,(i+1)%len(outline)) for i in range(len(outline))]
    for _ in range(3):
        mids={}
        def mid(i,j):
            key=tuple(sorted((i,j)))
            if key not in mids:
                mids[key]=len(points); points.append(((points[i][0]+points[j][0])/2,(points[i][1]+points[j][1])/2))
            return mids[key]
        nt=[]
        for i,j,k in tv:
            ij=mid(i,j); jk=mid(j,k); ki=mid(k,i)
            nt += [(i,ij,ki),(ij,j,jk),(ki,jk,k),(ij,jk,ki)]
        boundary=[e for i,j in boundary for e in [(i,mid(i,j)),(mid(i,j),j)]]; tv=nt
    wverts=[]
    for back in (False,True):
        for x,z in points:
            inward=max(0,min(1,(x+29.5)/22))
            center=-.3-3.9*inward-1.7*math.exp(-((z-16)/7)**2)
            half=.60+2.0*inward
            # The thick lower sweep continues the strongest body keel into the lip.
            rib=.55*math.exp(-((z-(16.7+.055*(x+10)))/1.0)**2)
            y=center+half if back else center-half-rib
            wverts.append((x,y,z))
    m=len(points); wf=[tuple(reversed(t)) for t in tv]+[tuple(m+i for i in t) for t in tv]
    wf += [(i,j,m+j,m+i) for i,j in boundary]
    wing=mesh_object('Broad attached labral wing and posterior process',wverts,wf,mats,col)
    # Retain semantic construction meshes separately in editable blend; not exported.
    source=bpy.data.collections.new('SOURCE_EDITABLE'); bpy.context.scene.collection.children.link(source)
    for obj in (body,wing):
        cp=obj.copy(); cp.data=obj.data.copy(); cp.name='SOURCE '+obj.name; source.objects.link(cp); cp.parent=None; cp.hide_render=True; cp.hide_set(True)
        for v in cp.data.vertices: v.co*=.001
    source.hide_render=True; source.hide_viewport=True
    # Union via an explicitly bounded 0.16 mm voxel intermediate. This avoids
    # Boolean intersection slivers at this 44 mm fossil scale; original lofts retained.
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True); wing.select_set(True); bpy.context.view_layer.objects.active=body
    bpy.ops.object.join()
    mod=body.modifiers.new('Continuous shell voxel union 0.16 mm','REMESH'); mod.mode='VOXEL'; mod.voxel_size=.16; mod.use_smooth_shade=False
    bpy.ops.object.modifier_apply(modifier=mod.name)
    sm=body.modifiers.new('Restrained voxel surface relaxation','SMOOTH'); sm.factor=.3; sm.iterations=2
    bpy.ops.object.modifier_apply(modifier=sm.name)
    body.data.calc_loop_triangles()
    dec=body.modifiers.new('Low polygon surface reduction','DECIMATE'); dec.ratio=min(1,18000/len(body.data.loop_triangles)); dec.use_collapse_triangulate=True
    bpy.ops.object.modifier_apply(modifier=dec.name)
    body.name='Continuous fossil shell'
    bm=bmesh.new(); bm.from_mesh(body.data)
    for _ in range(12):
        tiny=[f for f in bm.faces if f.calc_area()<.0002]
        if not tiny: break
        edges=list({min(f.edges,key=lambda e:e.calc_length()) for f in tiny})
        bmesh.ops.collapse(bm,edges=edges)
    wires=[e for e in bm.edges if not e.link_faces]
    if wires: bmesh.ops.delete(bm,geom=wires,context='EDGES')
    loose=[v for v in bm.verts if not v.link_faces]
    if loose: bmesh.ops.delete(bm,geom=loose,context='VERTS')
    assert all(len(e.link_faces)==2 for e in bm.edges), 'Union must form a closed connected surface'
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(body.data); bm.free(); body.data.update()
    # Match measured external bounding size. Height 44 / total width 42 / inferred depth 23 mm.
    low=[min(v.co[i] for v in body.data.vertices) for i in range(3)]; high=[max(v.co[i] for v in body.data.vertices) for i in range(3)]
    factors=[42/(high[0]-low[0]),23/(high[1]-low[1]),44/(high[2]-low[2])]
    for v in body.data.vertices:
        v.co.x*=factors[0]*.001; v.co.y=(v.co.y-(low[1]+high[1])/2)*factors[1]*.001; v.co.z=(v.co.z-low[2])*factors[2]*.001
    # Restrained three-tone fossil finish; no photographic texture or procedural export shader.
    for poly in body.data.polygons:
        c=poly.center; phase=math.sin(c.x*1700+c.z*810)*math.cos(c.y*980-c.z*630)
        poly.material_index=2 if phase>.78 else 1 if phase<-.8 else 0
        poly.use_smooth=False
    body['construction']='Profile loft plus concave thick labral wing; 0.16 mm voxel union, restrained relaxation and 18k triangle reduction. Hidden construction parts remain editable.'
    body['surface']='Flat-shaded restrained fossil palette. No copied textures.'
    body['unseen_depth']='23 mm, artist working inference, not a specimen measurement.'
    # Apply explicit triangulation so source, export, and rebuild count the same topology.
    triang=body.modifiers.new('Deterministic final triangulation','TRIANGULATE'); triang.quad_method='FIXED'; triang.ngon_method='CLIP'; bpy.ops.object.modifier_apply(modifier=triang.name)
    bpy.context.view_layer.update()
    bm=bmesh.new(); bm.from_mesh(body.data)
    unseen=set(bm.verts); components=0
    while unseen:
        components+=1; stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                other=e.other_vert(v)
                if other in unseen: unseen.remove(other); stack.append(other)
    geometry={'status':'PASS_TECHNICAL_ONLY','connected_components':components,'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'min_triangle_area_m2':min(f.calc_area() for f in bm.faces),'method':'Final generated mesh BMesh adjacency, signed volume and triangle area; no printable physical-shell claim.'}
    assert components==1 and geometry['boundary_edges']==0 and geometry['nonmanifold_edges']==0 and geometry['signed_volume_m3']>0,geometry
    bm.free()
    sourceqa=audit_source(col,max_triangles=40000)
    if sourceqa['errors']: write(evidence/'source.json',sourceqa); raise RuntimeError(sourceqa['errors'])
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects: obj.select_set(True)
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    supported={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    assert set(options)<=supported, 'Exporter version/options differ'
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    glb=audit_glb(out/'model.glb',max_triangles=40000,max_materials=6,max_primitives=8)
    write(evidence/'source.json',dict(sourceqa,glb_sha256=sha(out/'model.glb')))
    write(evidence/'geometry.json',dict(geometry,glb_sha256=sha(out/'model.glb')))
    write(evidence/'glb.json',glb)
    assert not glb['errors'],glb['errors']
    assert glb['scene_triangles']==sourceqa['triangles']
    assert glb['bytes']<=8000000
    bb=sourceqa['bounds_blender_m']; expected_min=[bb['min'][0],bb['min'][2],-bb['max'][1]]; expected_max=[bb['max'][0],bb['max'][2],-bb['min'][1]]
    err=max(abs(glb['bounds_m'][key][i]-ex[i]) for key,ex in [('min',expected_min),('max',expected_max)] for i in range(3))
    assert err<1e-7
    write(evidence/'build.json',{'asset_id':p['asset_id'],'revision':'r001','status':'PASS_TECHNICAL_ONLY','blender':bpy.app.version_string,'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'semantic_sha256':glb['semantic_sha256'],'export_options':options,'source_to_glb_max_bounds_error_m':err,'source_to_glb_triangles_equal':True,'gray_diagnostic':a.gray,'runtime_dependencies':['Python standard library','Blender 4.3.2 bpy/bmesh/mathutils','source/deps/asset_common.py','source/deps/qa_glb.py'],'independent_review':'NOT_RUN','gpu':'NOT_RUN','populated_scene':'NOT_RUN'})
    print('MODEL_BUILD_COMPLETE',json.dumps({'glb':sha(out/'model.glb'),'triangles':glb['scene_triangles'],'primitives':glb['scene_primitives_estimated_base_draw_calls'],'bytes':glb['bytes']}))
if __name__=='__main__': main()
