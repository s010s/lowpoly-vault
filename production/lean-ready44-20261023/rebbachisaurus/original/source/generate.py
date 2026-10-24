# SPDX-License-Identifier: MIT
"""Deterministic Rebbachisaurus living reconstruction, meters, -Y forward.
Run with Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output .
No network, project tree, sibling asset, image or undeclared data dependency.
"""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
import bpy, bmesh
from mathutils import Vector
import asset_common as ac
from qa_glb import audit_glb


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def loft_body(collection, materials, rings):
    """Ring coordinates are x-center, y, z-center, width, height, ridge lift."""
    n = 24
    vertices=[]
    for xc,y,zc,w,h,lift in rings:
        for k in range(n):
            a=2*math.pi*k/n
            vertices.append((xc+w*math.sin(a),y,zc+h*math.cos(a)+lift*max(0,math.cos(a))**12))
    faces=[]; mat_indices=[]
    for r in range(len(rings)-1):
        ym=(rings[r][1]+rings[r+1][1])/2
        for k in range(n):
            j=(k+1)%n
            faces.append((r*n+k,r*n+j,(r+1)*n+j,(r+1)*n+k))
            ca=math.cos(2*math.pi*(k+.5)/n)
            # Continuous underside and narrow dorsal tint are original coloration,
            # not fossil evidence, stripes, plates or exposed neural spines.
            mat_indices.append(1 if ca < -.42 else 2 if ca>.88 and -2.65<ym<3.0 else 0)
    vertices.extend([(0,-8.4,4.52),(rings[-1][0],11.6,rings[-1][2])])
    for k in range(n):
        faces.append((len(vertices)-2,(k+1)%n,k));mat_indices.append(0)
        a=(len(rings)-1)*n
        faces.append((len(vertices)-1,a+k,a+(k+1)%n));mat_indices.append(0)
    obj=ac.mesh_object('Continuous-head-neck-trunk-highback-tail',vertices,faces,materials,collection)
    for f,mi in zip(obj.data.polygons,mat_indices):f.material_index=mi
    obj['anatomy']='Tall dorsal profile is bone-supported; exact covering and missing regions are reconstruction.'
    return obj


def vertical_loft(name, rings, material, collection, n=16):
    vertices=[]
    for x,y,z,rx,ry in rings:
        for k in range(n):
            a=2*math.pi*k/n
            vertices.append((x+rx*math.cos(a),y+ry*math.sin(a),z))
    faces=[]
    for j in range(len(rings)-1):
        for k in range(n):
            l=(k+1)%n
            faces.append((j*n+k,j*n+l,(j+1)*n+l,(j+1)*n+k))
    vertices += [rings[0][:3],rings[-1][:3]]
    for k in range(n):
        faces.append((len(vertices)-2,(k+1)%n,k))
        base=(len(rings)-1)*n
        faces.append((len(vertices)-1,base+k,base+(k+1)%n))
    return ac.mesh_object(name,vertices,faces,material,collection)


def ellipsoid_data(center, radii, vertices, faces, segments=12, latitude=6):
    base=len(vertices)
    cx,cy,cz=center; rx,ry,rz=radii
    for j in range(1,latitude):
        theta=math.pi*j/latitude
        for k in range(segments):
            a=2*math.pi*k/segments
            vertices.append((cx+rx*math.sin(theta)*math.cos(a),cy+ry*math.sin(theta)*math.sin(a),cz+rz*math.cos(theta)))
    north=len(vertices);vertices.append((cx,cy,cz+rz))
    south=len(vertices);vertices.append((cx,cy,cz-rz))
    for j in range(latitude-2):
        for k in range(segments):
            a=base+j*segments+k;b=base+j*segments+(k+1)%segments
            faces.append((a,b,b+segments,a+segments))
    for k in range(segments):
        faces.append((north,base+k,base+(k+1)%segments))
        a=base+(latitude-2)*segments
        faces.append((south,a+(k+1)%segments,a+k))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=HERE.parent)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    params=json.loads((HERE/'params.json').read_text())
    collection=ac.setup_scene('rebbachisaurus',seed=params['seed'])
    mats=[ac.make_material(name,color,roughness=.9) for name,color in params['palette'].items()]
    body=loft_body(collection,mats[:3],params['body_rings'])
    for name,rings in params['legs'].items():
        obj=vertical_loft(name,rings,mats[0],collection)
        obj['reconstruction']='Conservative pillar-legged sauropod support; not a complete preserved limb series.'
    # Shared face accents keep small eye/nostril/mouth cues editable without
    # multiplying draw primitives. No broad Nigersaurus-style muzzle is claimed.
    vertices=[];faces=[]
    for s in (-1,1):
        ellipsoid_data((s*.315,-7.89,4.68),(.052,.092,.078),vertices,faces)
        ellipsoid_data((s*.247,-8.19,4.62),(.031,.050,.031),vertices,faces,8,4)
        ellipsoid_data((s*.270,-8.06,4.365),(.017,.215,.018),vertices,faces,12,4)
    ac.mesh_object('Eyes-nostrils-mouth-accents',vertices,faces,mats[3],collection)
    # Small, subdued rear pedal unguals, not giant front-hand claws.
    vertices=[];faces=[]
    for name,rings in params['legs'].items():
        if not name.startswith('Hind'):continue
        x,y,z,rx,ry=rings[0]
        for off in (-.18,0,.18):
            ellipsoid_data((x+off,y-.385,.115),(.083,.125,.085),vertices,faces,8,4)
    ac.mesh_object('Small-hind-pedal-unguals',vertices,faces,mats[4],collection)
    root=bpy.data.objects['rebbachisaurus']
    root['scientific_scope']='Living reconstruction. Holotype tall dorsal spine anchors high back; missing head, neck, limbs, tail and all coloration are inferred.'
    root['scale_basis']='20 m NHM genus estimate, not measured complete fossil.'
    root['revision']=params['revision']
    # Save portable scene/UI paths rather than machine-specific factory defaults.
    bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:
                    space.params.directory=b'//'
    # Canonical helper owns source checks, explicit exporter flags and GLB audit.
    stage=out/'private'/'build-output'
    record=ac.export_asset('rebbachisaurus',{'en':'Rebbachisaurus','zh':'雷巴齐斯龙'},'dinosaurs',collection,
      metadata={'generator':'source/generate.py','description':{'en':'Complete high-backed sauropod reconstruction with explicit uncertainty.','zh':'明确标注不确定性的完整高背蜥脚类复原。'}},
      output_root=stage,render=False,max_triangles=6500,max_materials=6,max_primitives=12,diagnostics=False)
    built=stage/'rebbachisaurus'
    shutil.copy2(built/'rebbachisaurus.glb',out/'model.glb')
    shutil.copy2(built/'rebbachisaurus.blend',out/'model.blend')
    qa=json.loads((built/'qa.json').read_text())
    # Public report uses the delivered logical name; raw helper output stays in private build output.
    qa['glb']['file']='model.glb'
    save_json(out/'qa/evidence/source-export.json',qa)
    parts=[]
    for obj in collection.all_objects:
        if obj.type!='MESH':continue
        bm=bmesh.new();bm.from_mesh(obj.data)
        parts.append({'name':obj.name,'signed_volume_m3':bm.calc_volume(signed=True),
          'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)})
        bm.free()
    save_json(out/'qa/evidence/geometry.json',{'glb_sha256':digest(out/'model.glb'),
      'method':'Source mesh manifold edges and signed volumes after consistent normal recalculation; exact source-export counts and bounds audited separately.',
      'parts':parts,'all_component_volumes_positive':all(p['signed_volume_m3']>0 for p in parts),
      'union_claim':False,'overlap_notes':'Separate closed limb roots intentionally overlap the continuous trunk; eyes, nostrils, mouth marks and pedal horn are shallow attached details. Not a boolean-unified print model.',
      'crest_height_m':max(r[2]+r[4]+r[5] for r in params['body_rings']),
      'shoulder_dorsum_height_m':sum(params['body_rings'][15][k] for k in (2,4,5)),
      'pelvic_dorsum_height_m':sum(params['body_rings'][22][k] for k in (2,4,5)),
      'foot_contact_min_z_m':{name:min(r[2] for r in rings) for name,rings in params['legs'].items()},
      'source_has_cameras_lights_or_preview_collection':any(o.type in {'CAMERA','LIGHT'} for o in bpy.context.scene.objects) or '_PREVIEW_ONLY' in bpy.data.collections})
    save_json(out/'qa/evidence/build-metadata.json',{
      'asset_id':'rebbachisaurus','revision':params['revision'],'blender_version':bpy.app.version_string,
      'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),
      'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),
      'dependencies_sha256':digest(HERE/'dependencies.json'),'units':'meters','source_up':'+Z','source_forward':'-Y',
      'glb_up':'+Y','glb_forward':'+Z','origin':'Floor contact center between support feet, root identity',
      'export_options':record['export_options'],'generator_seed':params['seed'],'palette':params['palette'],
      'triangle_count':record['triangles'],'glb_bytes':record['glb_bytes'],
      'height_m':record['blender_dimensions_m'][2],'length_m':record['blender_dimensions_m'][1],
      'geometry_digest':qa['glb'].get('semantic_sha256'),'three_target_version':'0.180.0',
      'anatomical_claims':'Tall holotype dorsal neural spine supports a high-backed trunk. Exact soft tissue, absent regions and coloration are artistic inference.',
      'scale_basis':'20 m is the NHM genus estimate, not measured fossil length.'})
    if (out/'model.glb').stat().st_size>2000000:raise RuntimeError('Frozen GLB byte budget exceeded')
    print(json.dumps({'status':'BUILT_NOT_INDEPENDENTLY_REVIEWED','triangles':record['triangles'],'glb_sha256':digest(out/'model.glb')}))
if __name__=='__main__':main()
