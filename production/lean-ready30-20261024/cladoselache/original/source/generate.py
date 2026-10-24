# SPDX-License-Identifier: MIT
"""Original Cladoselache living reconstruction. Run with Blender 4.3.2.
blender -b -t 2 --python source/generate.py -- --output .
No reference image or third-party geometry is embedded.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def write(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=Path('.'))
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output; out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((HERE/'params.json').read_text())
    if bpy.app.version_string!=cfg['blender_version']: raise RuntimeError('Pinned Blender version mismatch')
    col=setup_scene(cfg['asset_id'],cfg['seed'])
    root=bpy.data.objects[col['asset_root']]
    root['representation']='living-reconstruction'
    root['mount']='swimming-body-center'
    root['scientific_limits']='Size, soft-tissue depth, pose and color are artistic estimates.'
    mats={k:make_material(k,v,roughness=.46 if k=='dark' else cfg['roughness']) for k,v in cfg['palette'].items()}
    def mesh(name,v,f,mat='fin'):
        return mesh_object(name,v,f,mats[mat] if isinstance(mat,str) else [mats[x] for x in mat],col)
    rings=cfg['cross_sections']; n=cfg['radial_segments']; verts=[]
    for y,rx,rz,zc in rings:
        for j in range(n):
            a=2*math.pi*j/n; verts.append((rx*math.cos(a),y,zc+rz*math.sin(a)))
    faces=[]
    for i in range(len(rings)-1):
        for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))])
    body=mesh('torpedo-body-short-blunt-head',verts,faces,['dorsal','flank','ventral'])
    for p in body.data.polygons:
        avg=sum(body.data.vertices[k].co.z for k in p.vertices)/len(p.vertices)
        p.material_index=0 if avg>.024 else 2 if avg<-.022 else 1
    # Closed sculpted fins: perimeter and two offset ridges, not open planes.
    def fin(name,points,ridge,axis,half=.0035):
        axis=Vector(axis); ridge=Vector(ridge)
        v=[tuple(Vector(p)+axis*half*.18) for p in points]+[tuple(Vector(p)-axis*half*.18) for p in points]
        m=len(points); v += [tuple(ridge+axis*half),tuple(ridge-axis*half)]
        f=[]
        for j in range(m):
            k=(j+1)%m; f.extend([(2*m,j,k),(2*m+1,m+k,m+j),(j,m+j,m+k,k)])
        return mesh(name,v,f)
    for sign,label in [(1,'right'),(-1,'left')]:
        pts=[(.055,-.315,-.020),(.132,-.235,-.052),(.214,-.080,-.087),(.242,.018,-.105),(.176,-.005,-.083),(.061,-.105,-.040)]
        fin('broad-based-pectoral-'+label,[(sign*x,y,z) for x,y,z in pts],(sign*.119,-.156,-.055),(0,0,1),.006)
        pts=[(.032,.095,-.025),(.073,.142,-.042),(.108,.226,-.069),(.068,.211,-.053),(.026,.185,-.030)]
        fin('paired-pelvic-'+label,[(sign*x,y,z) for x,y,z in pts],(sign*.052,.157,-.038),(0,0,1),.0038)
    fin('first-dorsal',[(0,-.225,.052),(0,-.183,.138),(0,-.152,.177),(0,-.121,.167),(0,-.079,.071),(0,-.052,.049)],(0,-.146,.094),(1,0,0),.009)
    fin('second-dorsal',[(0,.070,.037),(0,.103,.094),(0,.129,.114),(0,.151,.101),(0,.188,.029)],(0,.126,.062),(1,0,0),.006)
    # A separate closed upper and lower caudal lobe share a short peduncle.
    fin('forked-caudal-upper',[(0,.302,.010),(0,.355,.051),(0,.463,.158),(0,.493,.177),(0,.480,.119),(0,.407,.016),(0,.355,-.006)],(0,.383,.055),(1,0,0),.007)
    fin('forked-caudal-lower',[(0,.315,-.008),(0,.365,-.042),(0,.467,-.150),(0,.500,-.177),(0,.482,-.099),(0,.408,.016),(0,.350,.014)],(0,.387,-.048),(1,0,0),.007)
    # Broad terminal mouth line tracks the curved blunt snout surface.
    mouth=[(-.058,-.474,-.012),(-.050,-.492,-.010),(-.036,-.501,-.008),(0,-.501,-.008),(.036,-.501,-.008),(.050,-.492,-.010),(.058,-.474,-.012)]
    def ribbon(name,points,width,depth):
        v=[]
        for x,y,z in points: v.extend([(x,y-depth,z+width),(x,y-depth,z-width),(x,y+depth,z+width),(x,y+depth,z-width)])
        f=[]
        for i in range(len(points)-1):
            a=i*4;b=a+4;f.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
        f.extend([(0,1,3,2),(len(v)-4,len(v)-2,len(v)-1,len(v)-3)])
        return mesh(name,v,f,'dark')
    ribbon('wide-terminal-mouth',mouth,.0018,.0009)
    # Intersect the actual loft's polygonal cross section for seated details.
    def surface_x(y,z):
        for i in range(len(rings)-1):
            if rings[i][0]<=y<=rings[i+1][0]:
                t=(y-rings[i][0])/(rings[i+1][0]-rings[i][0])
                rx,rz,zc=[rings[i][k]*(1-t)+rings[i+1][k]*t for k in (1,2,3)]
                break
        else: raise ValueError('Detail outside body loft')
        cross=[(rx*math.cos(2*math.pi*j/n),zc+rz*math.sin(2*math.pi*j/n)) for j in range(n)]
        xs=[]
        for j in range(n):
            x1,z1=cross[j];x2,z2=cross[(j+1)%n]
            if min(z1,z2)<=z<=max(z1,z2) and abs(z2-z1)>1e-10:
                xs.append(x1+(x2-x1)*(z-z1)/(z2-z1))
        return max(xs)
    # Closed, body-conforming eye lenses, without detached circular discs.
    def seated_eye(name,sign,y,z,radius,material,relief):
        k=20; v=[(sign*(surface_x(y,z)-.0015),y,z)]
        for j in range(k):
            yy=y+radius*.85*math.cos(2*math.pi*j/k);zz=z+radius*math.sin(2*math.pi*j/k)
            v.append((sign*(surface_x(yy,zz)+relief*.24),yy,zz))
        v.append((sign*(surface_x(y,z)+relief),y,z));f=[]
        for j in range(k):f.extend([(0,1+(j+1)%k,1+j),(k+1,1+j,1+(j+1)%k)])
        return mesh(name,v,f,material)
    for sign,label in [(1,'right'),(-1,'left')]:
        seated_eye('orbital-rim-'+label,sign,-.443,.027,.0125,'eye_rim',.0018)
        seated_eye('eye-'+label,sign,-.443,.027,.009,'dark',.0030)
        # Five continuous shallow closed gill marks follow the faceted body skin.
        for g in range(5):
            y=-.365+g*.016; v=[];count=9
            for j in range(count):
                z=.016-j*.0066;yy=y+.004*math.sin(j*math.pi/(count-1));w=.00125
                for depth,dy in [(.00065,-w),(.00065,w),(-.0015,-w),(-.0015,w)]:
                    v.append((sign*(surface_x(yy+dy,z)+depth),yy+dy,z))
            f=[]
            for j in range(count-1):
                a=j*4;b=a+4;f.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
            e=(count-1)*4;f.extend([(0,1,3,2),(e,e+2,e+3,e+1)])
            mesh('gill-'+label+'-'+str(g+1),v,f,'dark')
    # Scale the complete living reconstruction once, preserving all proportions.
    all_y=[v.co.y for o in col.all_objects if o.type=='MESH' for v in o.data.vertices]
    factor=cfg['length_m']/(max(all_y)-min(all_y))
    for obj in col.all_objects:
        if obj.type=='MESH':
            for v in obj.data.vertices: v.co *= factor
    source=audit_source(col,cfg['max_triangles'])
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.scene.render.filepath='//render'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
                    space.params.filename='model.blend'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects: obj.select_set(True)
    bpy.context.view_layer.objects.active=root
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available: raise RuntimeError('Exporter RNA options unavailable')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    glb=audit_glb(out/'model.glb',cfg['max_triangles'],cfg['max_materials'],cfg['max_primitives']); glb['file']='model.glb'
    if glb['errors'] or glb['bytes']>cfg['max_glb_bytes']: raise RuntimeError(glb)
    write(out/'qa/evidence/build.json',{'check':'deterministic-source-build','blender_version':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'source':source,'glb':glb,'blend_sha256':sha(out/'model.blend'),'export_options':options,'scientific_limits':cfg['thickness_basis'],'warning_disposition':'Negative lowest Z/Y is intentional for a swimming-body-center mount. No floor contact is claimed.'})
    print('BUILD_COMPLETE '+glb['sha256'])
if __name__=='__main__': main()
