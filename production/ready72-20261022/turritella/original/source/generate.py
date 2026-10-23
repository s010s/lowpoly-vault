# SPDX-License-Identifier: MIT
"""Deterministic original Turritella fossil-form shell. Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output DIR
No network, photo textures, copied meshes, or other model directory dependencies.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
TAU=2*math.pi

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def smooth(x):return x*x*(3-2*x)
def lerp_profile(z,profile):
    for (za,ra),(zb,rb) in zip(profile,profile[1:]):
        if z<=zb:return ra+(rb-ra)*smooth(max(0,min(1,(z-za)/(zb-za))))
    return profile[-1][1]

def make_shell(collection):
    H=P['target_height']; N=P['angular_segments']; W=P['visible_whorls_target']
    base=P['spire_base_z']; tipbase=P['spire_top_ring_z']
    # Spire is a single exterior envelope: radius is modulated by a continuous
    # dextral screw phase. No overlapping/disconnected tori are used.
    def z_from_w(w):return H-(H-base)*(w/W)**1.35
    def w_from_z(z):return W*max(0,(H-z)/(H-base))**(1/1.35)
    zs=P['base_ring_z'][:]
    ws=[0.28,0.50,0.72,0.94]+[1.125+i/8 for i in range(96)]
    zs += sorted(z_from_w(w) for w in ws if base+1e-7<z_from_w(w)<tipbase-1e-7)
    zs += [tipbase]
    zs=sorted(set(zs)); M=len(zs)
    i0=zs.index(P['opening_z_bounds'][0]);i1=zs.index(P['opening_z_bounds'][1])
    j0,j1=P['opening_angular_bounds'];jmid=(j0+j1)/2; jhalf=(j1-j0)/2
    zmid=(zs[i0]+zs[i1])/2;zhalf=(zs[i1]-zs[i0])/2
    centre_angle=-math.pi+TAU*jmid/N
    n=Vector((math.cos(centre_angle),math.sin(centre_angle),0))
    tangent=Vector((-n.y,n.x,0)); up=Vector((0,0,1))
    verts=[]; faces=[]; material_indices=[]
    def radius(z,theta):
        if z<=base:
            r=lerp_profile(z,P['base_radius_profile'])
            return r*(1+0.009*math.cos(7*theta+0.8)*max(0,z/base))
        w=w_from_z(z); f=(w/W)
        r=P['spire_base_radius']*f**0.98
        phase=(w+theta/TAU)%1
        # Narrow shallow suture; rounded shoulder + only a modest low keel.
        shoulder=0.967+0.028*math.cos(TAU*(phase-0.53))
        suture=0.028*math.exp(-((min(phase,1-phase))/0.105)**2)
        keel=0.015*math.exp(-((phase-0.71)/0.115)**2)
        axial=0.012*max(0,math.sin(math.pi*phase))*math.sin(8*theta+0.35*w)
        return r*(shoulder-suture+keel+axial)
    for i,z in enumerate(zs):
        for j in range(N):
            theta=-math.pi+TAU*j/N; zz=z
            s=(j-jmid)/jhalf;t=(z-zmid)/zhalf;m=max(abs(s),abs(t))
            if 0<m<2.0:
                # Rectangular grid transitions continuously to a rounded-
                # subquadrate aperture, with a subtly flattened basal edge.
                factor=m/(abs(s)**P['opening_superellipse_power']+abs(t)**P['opening_superellipse_power'])**(1/P['opening_superellipse_power'])
                weight=1 if m<=1 else 1-smooth(m-1)
                factor=1+(factor-1)*weight
                theta=-math.pi+TAU*(jmid+s*factor*jhalf)/N
                zz=zmid+t*factor*zhalf
            r=radius(zz,theta)
            verts.append((r*math.cos(theta),r*math.sin(theta),zz))
    vid=lambda i,j:i*N+(j%N)
    def face(v,mat=0):faces.append(tuple(v));material_indices.append(mat)
    for i in range(M-1):
        for j in range(N):
            if i0<=i<i1 and j0<=j<j1:continue
            face((vid(i,j),vid(i,j+1),vid(i+1,j+1),vid(i+1,j)))
    # Both poles close the exterior. The top is a visible simplified pointed
    # end, not an invented protoconch reconstruction.
    bottom=len(verts);verts.append((0,0,0))
    apex=len(verts);verts.append((0,0,H))
    for j in range(N):
        face((bottom,vid(0,j+1),vid(0,j)))
        face((apex,vid(M-1,j),vid(M-1,j+1)))
    # Boundary traverses clockwise viewed from outside; bridge to real inner
    # wall, then a blind vestibule ending well inside the body whorl.
    boundary=[vid(i0,j) for j in range(j0,j1)]
    boundary += [vid(i,j1) for i in range(i0,i1)]
    boundary += [vid(i1,j) for j in range(j1,j0,-1)]
    boundary += [vid(i,j0) for i in range(i1,i0,-1)]
    original=[Vector(verts[v]) for v in boundary]
    centre=n*P['opening_reference_radius']+up*zmid
    previous=boundary
    for level,(depth,scale) in enumerate(P['vestibule_depth_scale']):
        ring=[]
        for v in original:
            delta=v-centre
            p=v-n*depth+(scale-1)*(tangent*delta.dot(tangent)+up*delta.z)
            ring.append(len(verts));verts.append(tuple(p))
        for k in range(len(ring)):
            face((previous[k],previous[(k+1)%len(ring)],ring[(k+1)%len(ring)],ring[k]),1 if level==0 else 2)
        previous=ring
    c=sum((Vector(verts[v]) for v in previous),Vector())/len(previous)
    c-=n*0.00015;cap=len(verts);verts.append(tuple(c))
    for k in range(len(previous)):face((previous[k],previous[(k+1)%len(previous)],cap),2)
    # Drop unused aperture-grid vertices. All remaining vertices form one
    # closed, connected shell with an intentional geometric recess.
    used=sorted({x for f in faces for x in f}); remap={old:new for new,old in enumerate(used)}
    verts=[verts[v] for v in used];faces=[tuple(remap[v] for v in f) for f in faces]
    # Exact frozen size estimate, preserving relative anatomy rather than a
    # unit cube. X/Y isotropic scale sets greatest horizontal span to 7.5 mm.
    width=max(max(v[k] for v in verts)-min(v[k] for v in verts) for k in (0,1))
    scale=P['target_width']/width
    verts=[(x*scale,y*scale,z) for x,y,z in verts]
    mats=[make_material('Fossil_bone_beige',P['palette_hex']['shell'],0.84),
          make_material('Thin_fossil_aperture_rim',P['palette_hex']['rim'],0.81),
          make_material('Recessed_fossil_inner_wall',P['palette_hex']['interior'],0.94)]
    ob=mesh_object('Continuous_dextral_shell_with_recess',verts,faces,mats,collection)
    for poly,mi in zip(ob.data.polygons,material_indices):poly.material_index=mi;poly.use_smooth=True
    ob['construction']='single continuous screw-modulated exterior envelope, integrated aperture rim and short recessed vestibule'
    ob['handedness']='dextral; from apex downward the whorl crest winds clockwise'
    ob['visible_whorl_target']=W
    ob['model_scope']='original fossil-form study, not a specimen scan'
    bm=bmesh.new();bm.from_mesh(ob.data)
    edge_data={'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True)}
    # Connected component count independent of Blender object count.
    pending=set(bm.verts);components=0
    while pending:
        components+=1;stack=[pending.pop()]
        while stack:
            v=stack.pop()
            for edge in v.link_edges:
                q=edge.other_vert(v)
                if q in pending:pending.remove(q);stack.append(q)
    edge_data['connected_components']=components;bm.free()
    edge_data.update({'construction_whorl_coordinate_max':W,'opening_boundary_vertices':len(boundary),'short_vestibule_depth_m':P['vestibule_depth_scale'][-1][0],'self_intersection_method':'Exterior is single-valued polar radius. Inner vestibule is bounded beneath opening; no general triangle intersection solver run. Independent visual review remains required.'})
    return edge_data

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    args=parser.parse_args(argv);out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    collection=setup_scene(P['asset_id'],P['seed']);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    topology=make_shell(collection)
    source=audit_source(collection,P['geometry_policy']['max_triangles'])
    save(out/'source-audit.json',source);save(out/'geometry.json',topology)
    if source['errors']:
        ob=next(o for o in collection.objects if o.type=='MESH');ob.data.calc_loop_triangles()
        save(out/'small-triangles.json',[{'area':t.area,'xyz':[list(ob.data.vertices[i].co) for i in t.vertices]} for t in ob.data.loop_triangles if t.area<1e-10])
        raise RuntimeError(str(source['errors']))
    bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[collection['asset_root']]
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Missing required exporter flags: '+str(set(options)-available))
    bpy.ops.export_scene.gltf(**options)
    audit=audit_glb(out/'model.glb',P['geometry_policy']['max_triangles'],P['geometry_policy']['max_materials'],P['geometry_policy']['max_primitives'])
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(audit['bounds_m'][k][i]-expected[k][i]) for k in ('min','max') for i in range(3))
    audit['source_bounds_max_delta_m']=delta
    save(out/'glb-audit.json',audit)
    if audit['errors'] or delta>1e-7 or audit['scene_triangles']!=source['triangles']:raise RuntimeError('Export audit failed')
    if audit['bytes']>P['geometry_policy']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    metadata={'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'python_version':sys.version,'gltf_exporter_version':getattr(__import__('io_scene_gltf2'),'bl_info',{}).get('version'),'source_sha256':sha(Path(__file__)),'params_sha256':sha(HERE/'params.json'),'export_options':{k:v for k,v in options.items() if k!='filepath'},'seed':P['seed'],'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'semantic_sha256':audit['semantic_sha256'],'dimensions_blender_m':b['size'],'triangles':audit['scene_triangles'],'materials':audit.get('materials'),'geometry':topology,'style':'refined low-poly silhouette with deliberate smooth shell normals; palette-only PBR','axis':'Blender +Z apex, aperture front-right (+X,-Y); glTF +Y up/+Z front','size_claim':'26 x 7.5 mm approximate atlas image inference; not a direct specimen measurement','taxonomy_claim':'Traditional Turritella genus-level fossil-form study. subannulata is synonym of extant perexilis; no extinction or exact UF181437 layer/locality claim.'}
    save(out/'build-metadata.json',metadata)
    print(json.dumps({'status':'BUILT_NOT_INDEPENDENTLY_REVIEWED','sha256':audit['sha256'],'triangles':audit['scene_triangles'],'bytes':audit['bytes'],'topology':topology}))
if __name__=='__main__':main()
