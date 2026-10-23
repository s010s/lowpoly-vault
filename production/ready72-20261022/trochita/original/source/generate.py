#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Trochita fossil-form study. Blender 4.3.2. No source imagery or meshes.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUT
Author: Leon Made This / s010s. Model/renders CC-BY-4.0. See references.json.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb
P=json.loads((ROOT/'params.json').read_text())
N=P['angular_samples']; TAU=2*math.pi

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def clamp(x): return max(0,min(1,x))

def exterior(r,i):
    a=TAU*i/N
    twist=.19*(1-r)**1.5+1.05*math.exp(-r*7)
    t=a+twist
    # Slow irregularity affects outline; no copied damage or photograph tracing.
    oval=1+.025*math.cos(2*a+.4)+.012*math.sin(3*a-.7)
    rib_phase=P['radial_ribs']*a+1.1*math.sin(3*a)*r+.30*math.sin(5*a)*r*r
    rib=(.5+.5*math.cos(rib_phase))**1.4
    emergence=.62+.38*clamp((r-.20)/.40) if int(round(i/4))%2 else 1.0
    R=P['diameter']/2
    radius=R*r*oval+.00068*r**1.75*(rib-.38)
    x=radius*math.cos(t)+.00055*(1-r)**2*math.sin(r*7)
    y=radius*math.sin(t)+P['apex_offset_y']*(1-r)**1.65
    z=(P['height']-.0024)*max(0,1-r**1.4)**.95+.0024*math.exp(-(r/.105)**2)
    z+=.00150*math.sin(math.pi*r)**.7*(rib-.22)*emergence*clamp(r/.55)
    # One shallow spiral shoulder in the small coiled summit, not stacked whorls.
    phase=(a+1.3)%TAU
    spirals=[.12+.48*(phase/TAU)]
    ridge=max(math.exp(-((r-s)/.06)**2) for s in spirals)
    z+=.0027*ridge*(1-r)*min(1,r/.07)*min(1,phase/.4,(TAU-phase)/.4)
    z+=.00028*r**4*(1+math.cos(3*a+.7))
    return (x,y,z)

def interior(r,i):
    a=TAU*i/N; t=a+.19*(1-r)**1.5+1.05*math.exp(-r*7)
    wall=P['shell_wall_thickness']
    oval=1+.025*math.cos(2*a+.4)+.012*math.sin(3*a-.7)
    phase=P['radial_ribs']*a+1.1*math.sin(3*a)*r+.30*math.sin(5*a)*r*r
    rib=(.5+.5*math.cos(phase))**1.4
    radius=P['diameter']/2*r*oval+.00068*r**10*(rib-.38)-wall*r
    x=radius*math.cos(t)+.00055*(1-r)**2*math.sin(r*7)
    y=radius*math.sin(t)+P['apex_offset_y']*(1-r)**1.65
    z=(P['height']-.0024)*max(0,1-r**1.4)**.95+.0024*math.exp(-(r/.105)**2)
    z+=.00028*r**4*(1+math.cos(3*a+.7))
    z-=wall*(1-.75*r)
    return (x,y,z)

def create_shell(col,mats):
    vertices=[(0,P['apex_offset_y'],P['height'])]; faces=[]; material=[]
    def face(f,m): faces.append(tuple(f));material.append(m)
    def surface(rings,fn,apex,inside):
        ids=[]
        for r in rings:
            ring=[]
            for i in range(N):ring.append(len(vertices));vertices.append(fn(r,i))
            ids.append(ring)
        for i in range(N): face((apex,ids[0][i],ids[0][(i+1)%N]),int(inside))
        for l in range(len(ids)-1):
            for i in range(N):face((ids[l][i],ids[l+1][i],ids[l+1][(i+1)%N],ids[l][(i+1)%N]),int(inside))
        return ids
    outer=surface(P['outer_rings'],exterior,0,False)
    inside_apex=len(vertices); vertices.append((0,P['apex_offset_y'],P['height']-P['shell_wall_thickness']))
    inner=surface(P['inner_rings'],interior,inside_apex,True)
    for i in range(N):face((outer[-1][i],inner[-1][i],inner[-1][(i+1)%N],outer[-1][(i+1)%N]),1)
    obj=mesh_object('ribbed_hollow_shell',vertices,faces,mats,col)
    for p,m in zip(obj.data.polygons,material):p.material_index=m;p.use_smooth=True
    # Preserve rim thickness with crisp shading on lip strip.
    for p in list(obj.data.polygons)[-N:]:p.use_smooth=False
    obj['construction']='One closed solid hollow shell, inner and outer surfaces joined around scalloped lip.'
    obj['ribs']=36
    return obj

def create_shelf(col,mat):
    boundary=[]
    # Attach to +Y half at actual inner wall ring; embed 0.3 mm into wall.
    r=P['shelf_attachment_r']; samples=72
    for j in range(samples+1):
        i=N*j/(2*samples)
        x,y,z=interior(r,i); a=TAU*i/N
        boundary.append((x+.00030*math.cos(a),y+.00030*math.sin(a),z+.00012))
    end=boundary[-1]; start=boundary[0]
    for j in range(1,36):
        u=j/36
        x=end[0]*(1-u)+start[0]*u
        y=end[1]*(1-u)+start[1]*u-.00155*math.sin(math.pi*u)
        z=end[2]*(1-u)+start[2]*u+.0020*math.sin(math.pi*u)
        boundary.append((x,y,z))
    # Original broad shelf is a shallow solid sheet, not a central cup.
    L=len(boundary); center=(0,.0093,.00365); thick=P['shelf_thickness']
    bottom_boundary=[]
    for j in range(samples+1):
        i=N*j/(2*samples); a=TAU*i/N; target_z=boundary[j][2]-thick
        lo,hi=r,1.0
        for _ in range(36):
            mid=(lo+hi)/2
            if interior(mid,i)[2]+.00012>target_z:lo=mid
            else:hi=mid
        x,y,z=interior((lo+hi)/2,i)
        bottom_boundary.append((x+.00030*math.cos(a),y+.00030*math.sin(a),target_z))
    ds=Vector(bottom_boundary[0])-Vector((boundary[0][0],boundary[0][1],boundary[0][2]-thick))
    de=Vector(bottom_boundary[-1])-Vector((boundary[samples][0],boundary[samples][1],boundary[samples][2]-thick))
    for j in range(1,36):
        u=j/36; x,y,z=boundary[samples+j]
        shift=de*(1-u)+ds*u
        bottom_boundary.append((x+shift.x,y+shift.y,z-thick))
    vertices=boundary+[center]+bottom_boundary+[(center[0],center[1],center[2]-thick)]
    top=L; offset=L+1; bottom=2*L+1; faces=[]
    for i in range(L):
        j=(i+1)%L
        faces.extend([(top,i,j),(bottom,offset+j,offset+i),(i,offset+i,offset+j,j)])
    obj=mesh_object('broad_internal_shelf',vertices,faces,mat,col)
    for p in obj.data.polygons:p.use_smooth=(len(p.vertices)==3)
    obj['construction']='Closed broad shelf slab. Both top and bottom attachment arcs follow the actual inner-wall slope and embed 0.30 mm into shell wall; contact is internal, not a print-ready Boolean union.'
    obj['free_edge']='Near straight with shallow bow, spanning opening. Not a cup.'
    return obj

def geometry_report(col):
    parts=[]
    for ob in col.all_objects:
        if ob.type!='MESH':continue
        bm=bmesh.new();bm.from_mesh(ob.data)
        parts.append({'name':ob.name,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True)})
        bm.free()
    return {'method':'BMesh boundary, edge-manifoldness and signed-volume per semantic solid; source and export face counts/bounds additionally checked. This is not an arbitrary self-intersection or printable-union proof.','parts':parts,'intentional_overlap':'Shelf arc embeds 0.30 mm into shell wall; no floating ribs and no detached visible shelf.','internal_shelf':'Open remaining half aperture; thick slab not central cup. Exact underside view is required.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
    col=setup_scene('trochita',P['seed'])
    mats=[make_material('fossil_exterior',P['palette']['exterior'],.88),make_material('shell_interior',P['palette']['interior'],.9)]
    create_shell(col,mats);create_shelf(col,make_material('internal_shelf',P['palette']['shelf'],.90))
    # Normalize the designed form to the explicit approximate diameter and inferred height.
    meshes=[o for o in col.all_objects if o.type=='MESH'];vs=[v for o in meshes for v in o.data.vertices]
    xmin=min(v.co.x for v in vs);xmax=max(v.co.x for v in vs);ymin=min(v.co.y for v in vs);ymax=max(v.co.y for v in vs);zmin=min(v.co.z for v in vs);zmax=max(v.co.z for v in vs)
    xy=P['diameter']/max(xmax-xmin,ymax-ymin);zz=P['height']/(zmax-zmin)
    for v in vs:v.co.x*=xy;v.co.y*=xy;v.co.z=(v.co.z-zmin)*zz
    bpy.context.view_layer.update(); source=audit_source(col,P['geometry_policy']['max_triangles']); geom=geometry_report(col)
    write(out/'source-audit.json',source);write(out/'geometry.json',geom)
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene['scope']='Original genus-level Trochita fossil-form study; UF146378 plan and underside; PRI70705 lateral comparison; height is inferred, not measured UF morphology.'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    props={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-props:raise RuntimeError('Unsupported exporter options')
    bpy.ops.export_scene.gltf(**options)
    gp=P['geometry_policy'];g=audit_glb(out/'model.glb',gp['max_triangles'],gp['max_materials'],gp['max_primitives']);write(out/'glb-audit.json',g)
    b=source['bounds_blender_m'];d=max(abs(g['bounds_m'][s][i]-x[i]) for s,x in [('min',[b['min'][0],b['min'][2],-b['max'][1]]),('max',[b['max'][0],b['max'][2],-b['min'][1]])] for i in range(3))
    if g['errors'] or g['bytes']>gp['max_glb_bytes'] or g['scene_triangles']!=source['triangles'] or d>1e-6:raise RuntimeError('Export roundtrip failed')
    from io_scene_gltf2 import bl_info
    write(out/'build.json',{'asset_id':'trochita','revision':'r001','blender':bpy.app.version_string,'exporter_version':bl_info['version'],'seed':P['seed'],'generator_sha256':sha(__file__),'params_sha256':sha(ROOT/'params.json'),'options':{k:v for k,v in options.items() if k!='filepath'},'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'semantic_sha256':g['semantic_sha256'],'source_export_bounds_max_error_m':d,'geometry_policy':gp,'method':'Canonical helper source audit and static GLB audit; not full Khronos or independent visual approval','scope':'Original specimen-informed genus study; 48 mm approximate diameter; 22 mm inferred height, range 19–27 mm.'})
    print('BUILT',g['scene_triangles'],g['bytes'],g['sha256'])
if __name__=='__main__':main()
