# SPDX-License-Identifier: MIT
"""Original Mammut americanum interpretation. Run with Blender and -- --output DIR.
All authored topology is computed here; only the declared bundled helpers are used.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def mesh(name,vertices,faces,material): return mesh_object(name,vertices,faces,material,COL)
def loft_y(name,rows,material,n=24):
    # Rows are y, center-z, half-width, half-height. Custom body sections.
    v=[]; f=[]
    for y,z,rx,rz in rows:
        for j in range(n):
            a=2*math.pi*j/n
            v.append((rx*math.cos(a),y,z+rz*math.sin(a)))
    for k in range(len(rows)-1):
        for j in range(n):
            a=k*n+j;b=k*n+(j+1)%n;f.append((a,b,b+n,a+n))
    f.extend([tuple(reversed(range(n))),tuple((len(rows)-1)*n+j for j in range(n))])
    return mesh(name,v,f,material)
def loft_z(name,rows,material,n=16):
    # Rows z, center-x, center-y, x-radius, y-radius; feet are explicitly planar.
    v=[];f=[]
    for z,x,y,rx,ry in rows:
        for j in range(n):
            a=2*math.pi*j/n;v.append((x+rx*math.cos(a),y+ry*math.sin(a),z))
    for k in range(len(rows)-1):
        for j in range(n):
            a=k*n+j;b=k*n+(j+1)%n;f.append((a,b,b+n,a+n))
    f.extend([tuple(reversed(range(n))),tuple((len(rows)-1)*n+j for j in range(n))])
    return mesh(name,v,f,material)
def catmull(points,sub=3):
    out=[]
    for i in range(len(points)-1):
        a=Vector(points[max(i-1,0)]);b=Vector(points[i]);c=Vector(points[i+1]);d=Vector(points[min(i+2,len(points)-1)])
        for k in range(sub):
            t=k/sub
            out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
    out.append(Vector(points[-1]));return out

def tube(name,points,radii,material,n=12,sub=3):
    path=catmull(points,sub);rs=[]
    for i in range(len(radii)-1):
        for k in range(sub):rs.append(radii[i]+(radii[i+1]-radii[i])*k/sub)
    rs.append(radii[-1]);v=[];f=[]
    for i,(p,r) in enumerate(zip(path,rs)):
        t=(path[min(i+1,len(path)-1)]-path[max(i-1,0)]).normalized()
        u=Vector((1,0,0));u=(u-t*t.dot(u)).normalized();w=t.cross(u).normalized()
        for j in range(n):
            a=2*math.pi*j/n;v.append(tuple(p+r*(u*math.cos(a)+w*math.sin(a))))
    for k in range(len(path)-1):
        for j in range(n):
            a=k*n+j;b=k*n+(j+1)%n;f.append((a,b,b+n,a+n))
    f.extend([tuple(reversed(range(n))),tuple((len(path)-1)*n+j for j in range(n))])
    return mesh(name,v,f,material)
def ellipsoid(name,center,radii,material,n=12,m=8):
    v=[(center[0],center[1],center[2]-radii[2])];f=[]
    for k in range(1,m):
        a=-math.pi/2+math.pi*k/m
        for j in range(n):
            b=2*math.pi*j/n;v.append((center[0]+radii[0]*math.cos(a)*math.cos(b),center[1]+radii[1]*math.cos(a)*math.sin(b),center[2]+radii[2]*math.sin(a)))
    v.append((center[0],center[1],center[2]+radii[2]));last=len(v)-1
    for j in range(n):f.append((0,1+(j+1)%n,1+j))
    for k in range(m-2):
        for j in range(n):
            a=1+k*n+j;b=1+k*n+(j+1)%n;f.append((a,b,b+n,a+n))
    for j in range(n):f.append((last,last-n+j,last-n+(j+1)%n))
    return mesh(name,v,f,material)

def make_ear(sign):
    # Asymmetrical fleshy paddle, with a thick root and scallop-free broad edge.
    outline=[(-1.55,2.48),(-1.35,2.53),(-1.16,2.43),(-1.10,2.22),(-1.12,1.98),(-1.23,1.78),(-1.40,1.72),(-1.55,1.84),(-1.65,2.10),(-1.66,2.32)]
    cy,cz=-1.39,2.14;v=[];f=[];n=len(outline)
    for layer in [0,1]:
        for scale in [.18,.60,1.0]:
            for y,z in outline:
                yy=cy+(y-cy)*scale;zz=cz+(z-cz)*scale
                xx=sign*(.48+.38*scale-.05*(z-cz)+(.045 if layer==0 else -.045)*(1-.55*scale))
                v.append((xx,yy,zz))
    for layer in [0,1]:
        o=layer*3*n
        for k in range(2):
            for j in range(n):f.append((o+k*n+j,o+k*n+(j+1)%n,o+(k+1)*n+(j+1)%n,o+(k+1)*n+j))
        f.append(tuple(o+j for j in range(n)))
    for j in range(n):f.append((2*n+j,2*n+(j+1)%n,5*n+(j+1)%n,5*n+j))
    obj=mesh('ear-'+('right' if sign>0 else 'left'),v,f,[MAT['body'],MAT['inner_ear']])
    for p in obj.data.polygons:
        # Muted inner region, flush with the ear surface rather than a floating patch.
        if p.index<2*n and p.index<10:p.material_index=1
    return obj

def build():
    global COL,MAT
    COL=setup_scene('mammut',P['seed'])
    MAT={k:make_material(k,v,roughness=.88 if k!='ivory' else .76) for k,v in P['surface']['palette_srgb'].items()}
    skin=[]
    skin.append(loft_y('barrel-and-neck',[(1.77,1.84,.12,.29),(1.61,1.84,.49,.60),(1.30,1.87,.70,.73),(.85,1.89,.80,.78),(.25,1.90,.84,.80),(-.35,1.91,.83,.82),(-.80,1.94,.77,.81),(-1.15,1.99,.67,.72),(-1.43,2.03,.60,.59),(-1.67,2.06,.48,.48)],MAT['body']))
    skin.append(loft_y('low-elongated-head',[(-1.43,2.05,.43,.40),(-1.62,2.11,.54,.45),(-1.90,2.12,.56,.47),(-2.14,2.08,.54,.43),(-2.37,1.99,.47,.36),(-2.59,1.91,.34,.29),(-2.71,1.91,.20,.22)],MAT['body']))
    legs=[]
    for sign in [-1,1]:
        for front in [True,False]:
            y=(-.91 if front else 1.14)+(0.10 if sign<0 else -.10)
            x=sign*.57
            rows=[(0,x,y,.30,.34),(.12,x,y,.33,.36),(.32,x,y,.29,.31),(.65,x+sign*.015,y+.015,.24,.25),(.98,x,y+.06,.255,.28),(1.22,x-sign*.015,y+.05,.31,.35),(1.53,x-sign*.06,y,.38,.40),(1.85,x-sign*.15,y-.04,.40,.45),(2.03,x-sign*.24,y-.07,.30,.35)]
            skin.append(loft_z(('fore' if front else 'hind')+'leg-'+str(sign),rows,MAT['body']))
            legs.append((x,y))
    skin.append(tube('trunk-continuous-root',[(0,-2.53,2.10),(0,-2.75,1.93),(0,-2.89,1.60),(0,-2.98,1.20),(0,-3.03,.80),(0,-3.04,.50),(0,-2.94,.32),(0,-2.76,.35),(0,-2.69,.48)],[.27,.255,.21,.17,.135,.105,.082,.064,.033],MAT['body'],n=16,sub=3))
    # Keep original editable loft blocks in the source, never in the export.
    author=bpy.data.collections.new('AUTHORING_LOFTS');bpy.context.scene.collection.children.link(author)
    author.hide_render=True;author.hide_viewport=True
    for obj in skin:
        dup=obj.copy();dup.data=obj.data.copy();dup.name='editable-'+obj.name;dup.parent=None;author.objects.link(dup)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in skin:obj.select_set(True)
    bpy.context.view_layer.objects.active=skin[0];bpy.ops.object.join();body=skin[0];body.name='integrated-skin'
    mod=body.modifiers.new('join-shoulders-hips-and-trunk','REMESH');mod.mode='VOXEL';mod.voxel_size=.045;mod.use_smooth_shade=False
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=body.modifiers.new('soft-tissue-transition','SMOOTH');mod.factor=1.10;mod.iterations=6;bpy.ops.object.modifier_apply(modifier=mod.name)
    # Preserve broad, flat foot contact after smoothing, with a short rounded ankle.
    for v in body.data.vertices:
        if v.co.z<.065:v.co.z=0
    body.data.calc_loop_triangles();initial=len(body.data.loop_triangles)
    mod=body.modifiers.new('deliberate-low-poly-planes','DECIMATE');mod.ratio=min(1,4800/initial);mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
    for v in body.data.vertices:
        if v.co.z<.0005:v.co.z=0
    body.data.materials.clear();body.data.materials.append(MAT['body']);body.data.materials.append(MAT['body_light'])
    for poly in body.data.polygons:
        poly.use_smooth=False
        # Restrained continuous underside tone, not random patchwork.
        poly.material_index=int(poly.center.z<1.30 and abs(poly.center.y)<1.6 and poly.normal.z<-.3)
    for sign in [-1,1]:
        make_ear(sign)
        tube('upper-tusk-'+str(sign),[(sign*.37,-2.43,1.78),(sign*.43,-2.75,1.65),(sign*.51,-3.10,1.58),(sign*.61,-3.46,1.59),(sign*.70,-3.82,1.69),(sign*.77,-4.11,1.88),(sign*.80,-4.33,2.13),(sign*.80,-4.44,2.39)],[.155,.145,.126,.102,.078,.052,.028,.002],MAT['ivory'],n=14,sub=3)
        # Small eye embedded into the head surface; neither a detached sphere nor a stalk.
        body.data.update();bpy.context.view_layer.update()
        hit,loc,normal,index=body.ray_cast(Vector((sign*2,-2.08,2.22)),Vector((-sign,0,0)))
        if not hit:raise RuntimeError('Eye attachment surface not found')
        ellipsoid('eye-'+str(sign),(loc.x-sign*.015,-2.08,2.22),(.028,.065,.038),MAT['eye_and_mouth'],n=12,m=6)
    tube('tail',[(0,1.65,2.03),(.03,1.85,1.83),(.07,1.97,1.53),(.10,2.01,1.25),(.12,1.99,1.02)],[.105,.083,.060,.042,.026],MAT['body'],n=10,sub=2)
    ellipsoid('tail-tuft',(.12,1.99,.98),(.073,.065,.12),MAT['body'],n=9,m=5)
    # Small low-key toenails on the forward edge. Three across each broad foot.
    for i,(x,y) in enumerate(legs):
        for j in [-1,0,1]:
            nx=x+j*.16
            hit,loc,normal,index=body.ray_cast(Vector((nx,y-.6,.12)),Vector((0,1,0)))
            if not hit:raise RuntimeError('Toenail attachment surface not found')
            ellipsoid('nail-'+str(i)+'-'+str(j),(nx,loc.y+.008,.12),(.062,.022,.060),MAT['toenail'],n=8,m=4)
    # Locate the root at the actual broad four-foot contact footprint center.
    feet=[v.co for v in body.data.vertices if v.co.z<.001]
    pivot=Vector(((min(v.x for v in feet)+max(v.x for v in feet))/2,(min(v.y for v in feet)+max(v.y for v in feet))/2,0))
    for obj in list(COL.all_objects)+list(author.objects):
        if obj.type=='MESH':
            for v in obj.data.vertices:v.co-=pivot
    bpy.context.view_layer.update()
    return COL

def main():
    global P
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=args.output.expanduser().resolve();out.mkdir(parents=True,exist_ok=True)
    P=json.loads((HERE/'params.json').read_text());col=build();policy=P['geometry_policy']
    source=audit_source(col,policy['max_triangles'])
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene.render.filepath='//'
    bpy.context.scene['generator']='source/generate.py'
    bpy.context.scene['scientific_scope']='Original living interpretation of adult Mammut americanum; not a measured specimen replica.'
    bpy.context.preferences.filepaths.save_version=0
    # Do not persist factory file-browser history in the editable source.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:
                    space.params.directory=b'//'
                    space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str((out/'model.blend').resolve()),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(flags)-available:raise RuntimeError('Missing required glTF exporter options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    glb=audit_glb(out/'model.glb',policy['max_triangles'],policy['max_materials'],policy['max_primitives'])
    glb['file']='model.glb'
    b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][s][i]-e[i]) for s,e in [('min',emin),('max',emax)] for i in range(3))
    if glb['errors'] or delta>1e-4 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>policy['max_glb_bytes']:raise RuntimeError('Source/export audit failed')
    import io_scene_gltf2
    dump(out/'technical.json',{'asset_id':'mammut','revision':'r001','source':source,'glb':glb,'source_export_bounds_delta_m':delta,'blender_version':bpy.app.version_string,'exporter_version':io_scene_gltf2.bl_info['version'],'consumer_three_version':'0.180.0','consumer_scope':'version pin only; GPU not tested','export_options':flags,'source_sha256':digest(Path(__file__).resolve()),'params_sha256':digest(HERE/'params.json'),'blend_sha256':digest(out/'model.blend'),'semantic_parts':'Integrated torso/head/limbs/trunk; separate ears, eyes, tusks, tail, toenails. Hidden authoring lofts retain original editable cross sections.'})
if __name__=='__main__':main()
