# SPDX-License-Identifier: MIT
"""Original NM L7852-informed Ribeiria internal mould. No reference pixels or mesh input.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUTPUT
Only the sibling params.json and deps Python files are required at runtime.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from asset_common import setup_scene, mesh_object, make_material, audit_source, srgb_to_linear
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v): Path(p).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def catmull(points,sub=24):
    out=[]
    for i,p1 in enumerate(points):
        p0,p2,p3=points[i-1],points[(i+1)%len(points)],points[(i+2)%len(points)]
        for j in range(sub):
            t=j/sub
            out.append(tuple(.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t) for k in range(2)))
    return out

def resample(poly,n):
    edges=[math.dist(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))]
    total=sum(edges);out=[];i=0;elapsed=0
    for j in range(n):
        d=j*total/n
        while elapsed+edges[i]<d:
            elapsed+=edges[i];i+=1
        a,b=poly[i],poly[(i+1)%len(poly)];t=(d-elapsed)/edges[i]
        out.append(tuple((1-t)*a[k]+t*b[k] for k in range(2)))
    return out

def build(params):
    col=setup_scene('ribeiria',params['seed'])
    mat=make_material('Fossil limestone - matte warm grey',params['base_srgb'],params['roughness'])
    N=params['perimeter_samples'];R=params['hemisphere_rings']
    profile=resample(catmull(params['profile_control_mm']),N)
    cx,cz=params['side_center_mm'];h=params['maximum_halfwidth_mm']
    verts=[];faces=[]
    # A continuously closed solid: hemispherical lofts meet at a single irregular rim.
    # The pegma cleft is an inset in this contour, not a detached exterior protrusion.
    for sign in (-1,1):
        base=len(verts);verts.append((cx,sign*h,cz))
        for k in range(1,R+1):
            t=(math.pi/2)*k/R;r=math.sin(t)
            for j,(px,pz) in enumerate(profile):
                x=cx+(px-cx)*r;z=cz+(pz-cz)*r
                # Thicker anterior-middle and thinner posterior; the lateral profile is not extruded.
                asym=1-0.14*max(x,0)/11
                y=sign*h*math.cos(t)*asym
                # Small original stone relief, suppressed at the shared rim and side poles.
                envelope=math.sin(t)**.5*math.cos(t)**.65
                noise=(math.sin(2.9*x+1.7*z+sign*.45)*.44+math.sin(5.3*x-4.7*z)*.24+math.cos(1.65*x+2.65*z)*.32)
                y+=sign*params['surface_relief_mm']*noise*envelope
                # Gentle curved growth remnants, not invented major cracks or drilled pores.
                rr=math.sqrt(((x+7.8)*.64)**2+((z-11.65)*.9)**2)
                trace=.012*math.sin(rr*8.2+.11*math.sin(x))*envelope*max(0,min(1,(10.5-z)/4))
                y+=sign*trace
                # Modest unevenness separates the photographed lateral sides while preserving dimensions.
                y+=sign*.018*math.sin(x*.77+z*.48+sign)*envelope
                verts.append((x,y,z))
        for j in range(N): faces.append((base,base+1+j,base+1+(j+1)%N))
        for k in range(R-1):
            a=base+1+k*N;b=a+N
            for j in range(N):
                nj=(j+1)%N
                # Alternate diagonals avoid an obvious one-direction spiral grid.
                if (j+k)%2: faces.extend([(a+j,b+j,a+nj),(a+nj,b+j,b+nj)])
                else: faces.extend([(a+j,b+j,b+nj),(a+j,b+nj,a+nj)])
    # Merge matching rim vertices by index, then retain one watertight manifold.
    first_rim=1+(R-1)*N;second=1+R*N;second_rim=second+1+(R-1)*N
    remap={second_rim+j:first_rim+j for j in range(N)}
    faces=[tuple(remap.get(v,v) for v in f) for f in faces]
    used=sorted({v for f in faces for v in f});lookup={old:new for new,old in enumerate(used)}
    verts=[verts[v] for v in used];faces=[tuple(lookup[v] for v in f) for f in faces]
    lo=[min(v[k] for v in verts) for k in range(3)];hi=[max(v[k] for v in verts) for k in range(3)]
    size=[params['length'],params['width'],params['height']]
    verts=[tuple(((v[k]-lo[k])/(hi[k]-lo[k])-(.5 if k<2 else 0))*size[k] for k in range(3)) for v in verts]
    obj=mesh_object('Whole mineral internal mould - integrated pegma cleft',verts,faces,mat,col)
    for p in obj.data.polygons:p.use_smooth=True
    # COLOR_0 is original low-amplitude mineral mottling; no photographed texture is embedded.
    color=obj.data.color_attributes.new(name='stone_tint',type='FLOAT_COLOR',domain='POINT')
    rgb=[int(params['base_srgb'][i:i+2],16)/255 for i in (1,3,5)]
    for v,d in zip(obj.data.vertices,color.data):
        x,y,z=(a*1000 for a in v.co)
        m=1+.022*math.sin(x*.83+z*1.35)+.012*math.cos(x*4.7-z*2.2+y*3)
        d.color=tuple(srgb_to_linear(min(1,max(0,c*m))) for c in rgb)+(1,)
    node=mat.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='stone_tint'
    shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    mat.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color'])
    obj['representation']='solid internal mould of conjoined shell; no empty shell cavity'
    obj['reference_anchor']='Polechova 2015 Fig 1 D1-D3, NM L7852, Ribeiria apusoides'
    obj['surface_style']='intentionally smooth coarse sculpture with subtle original mineral relief'
    obj['pegma_note']='localized anterior dorsal notch in the same watertight body, never an external horn'
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    return col,obj

def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    params=json.loads((HERE/'params.json').read_text());col,obj=build(params)
    source=audit_source(col,24000)
    bm=bmesh.new();bm.from_mesh(obj.data)
    volume=bm.calc_volume(signed=True)
    bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table()
    unseen=set(bm.verts);components=0
    while unseen:
        components+=1; todo=[unseen.pop()]
        while todo:
            v=todo.pop()
            for e in v.link_edges:
                n=e.other_vert(v)
                if n in unseen:unseen.remove(n);todo.append(n)
    tree=BVHTree.FromBMesh(bm,epsilon=0)
    intersections=[]
    for a,b in tree.overlap(tree):
        if a>=b or set(bm.faces[a].verts)&set(bm.faces[b].verts):continue
        intersections.append([a,b])
    detail={'signed_volume_m3':volume,'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'connected_components':components,'component_method':'bmesh vertex-edge breadth-first connected components','nonadjacent_triangle_intersections':len(intersections),'intersection_method':'BVHTree triangle overlap; pairs sharing any vertex excluded','source_vertices':len(obj.data.vertices),'source_faces':len(obj.data.polygons)}
    bm.free()
    if source['errors'] or detail['nonmanifold_edges'] or components!=1 or intersections or volume<=0:raise RuntimeError(json.dumps({'source':source,'geometry':detail}))
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='ACTIVE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Exporter options unavailable')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    glb=audit_glb(out/'model.glb',24000,6,16)
    if glb['errors'] or glb['bytes']>2500000:raise RuntimeError(json.dumps(glb))
    glb['file']='model.glb'
    b=source['bounds_blender_m'];expected_min=[b['min'][0],b['min'][2],-b['max'][1]];expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][side][i]-e[i]) for side,e in [('min',expected_min),('max',expected_max)] for i in range(3))
    assert delta<1e-8 and source['triangles']==glb['scene_triangles']
    record={'asset_id':'ribeiria','revision':'r001','blender_version':bpy.app.version_string,'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'seed':params['seed'],'source':source,'geometry':detail,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':options,'normal_style_review':'Smooth surfaces deliberate for small mineral internal mould; geometry preserves irregular fossil contour. Not pristine shell or flat cardboard extrusion.','runtime_target':{'threejs':'0.180.0','parse':'not_run','gpu':'not_run','populated_scene':'not_run'}}
    save(out/'build-evidence.json',record)
    print('BUILD_COMPLETE '+json.dumps({'glb_sha256':glb['sha256'],'triangles':glb['scene_triangles'],'bytes':glb['bytes']}))
if __name__=='__main__':main()
