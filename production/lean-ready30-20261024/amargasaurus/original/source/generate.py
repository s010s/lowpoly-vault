# SPDX-License-Identifier: MIT
"""Deterministic original living Amargasaurus reconstruction. Run with Blender.
The cervical soft-tissue outline is an interpretation, not a specimen measurement.
Example: blender -b -t 2 --python source/generate.py -- --output output
"""
import argparse, hashlib, json, math, os, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb


def loft(name, rings, mats, collection, n=14, palette=True):
    """Y-axis profile rings: center x,y,z and lateral/vertical radii."""
    vertices=[]; faces=[]; indices=[]
    for x,y,z,rx,rz in rings:
        vertices += [(x+rx*math.cos(2*math.pi*k/n),y,z+rz*math.sin(2*math.pi*k/n)) for k in range(n)]
    for j in range(len(rings)-1):
        for k in range(n):
            faces.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
            indices.append(1 if len(mats)>1 and palette and math.sin(2*math.pi*(k+.5)/n)<-.35 else 0)
    faces += [tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+k for k in range(n))];indices += [0,0]
    obj=mesh_object(name,vertices,faces,mats,collection)
    for p,i in zip(obj.data.polygons,indices):p.material_index=i
    return obj


def tube(name, nodes, mat, collection, n=10):
    """Closed tapered tube following an explicit 3-D axis, no scaled primitives."""
    vertices=[]; faces=[]
    for i,(p,rx,ry) in enumerate(nodes):
        p=Vector(p); before=Vector(nodes[max(0,i-1)][0]); after=Vector(nodes[min(len(nodes)-1,i+1)][0]);t=(after-before).normalized()
        ref=Vector((1,0,0)) if abs(t.x)<.85 else Vector((0,1,0));u=(ref-t*ref.dot(t)).normalized();v=t.cross(u).normalized()
        for k in range(n):
            a=2*math.pi*k/n;vertices.append(tuple(p+u*rx*math.cos(a)+v*ry*math.sin(a)))
    for j in range(len(nodes)-1):
        for k in range(n):faces.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    faces += [tuple(range(n-1,-1,-1)),tuple((len(nodes)-1)*n+k for k in range(n))]
    return mesh_object(name,vertices,faces,mat,collection)


def ellipsoid_component(vertices,faces,center,scale,n=10,r=5):
    offset=len(vertices);cx,cy,cz=center;sx,sy,sz=scale
    vertices.append((cx,cy,cz-sz))
    for j in range(1,r):
        ph=-math.pi/2+math.pi*j/r
        for k in range(n):
            a=2*math.pi*k/n;vertices.append((cx+sx*math.cos(ph)*math.cos(a),cy+sy*math.cos(ph)*math.sin(a),cz+sz*math.sin(ph)))
    top=len(vertices);vertices.append((cx,cy,cz+sz))
    for k in range(n):faces.append((offset,offset+1+(k+1)%n,offset+1+k))
    for j in range(r-2):
        for k in range(n):faces.append((offset+1+j*n+k,offset+1+j*n+(k+1)%n,offset+1+(j+1)*n+(k+1)%n,offset+1+(j+1)*n+k))
    for k in range(n):faces.append((top,offset+1+(r-2)*n+k,offset+1+(r-2)*n+(k+1)%n))


def build(params,gray=False):
    c=setup_scene(params['asset_id'],params['seed'])
    m={key:make_material('amargasaurus-'+key,'#96968F' if gray else value) for key,value in params['palette'].items()}
    skin=[m['skin'],m['underside']]
    # Torso/shoulder/hip form is intentionally compact, with no platform/supports.
    loft('torso',[(0,-1.48,2.12,.25,.35),(0,-1.25,2.12,.52,.61),(0,-.88,2.13,.7,.72),(0,-.35,2.12,.8,.78),(0,.25,2.12,.81,.78),(0,.78,2.1,.72,.72),(0,1.17,2.08,.54,.56),(0,1.47,2.02,.29,.36)],skin,c,n=18)
    # Neck rises forward from shoulders; continuously shaped cross sections.
    neck=[(0,-1.12,2.26,.49,.55),(0,-1.4,2.42,.42,.46),(0,-1.67,2.61,.35,.38),(0,-1.94,2.83,.31,.32),(0,-2.2,3.04,.27,.28),(0,-2.45,3.2,.235,.245),(0,-2.69,3.31,.205,.215),(0,-2.91,3.38,.18,.195),(0,-3.1,3.4,.17,.18),(0,-3.25,3.4,.17,.17)]
    loft('neck',neck,skin,c,n=14)
    loft('head',[(0,-3.89,3.28,.11,.095),(0,-3.82,3.3,.18,.13),(0,-3.64,3.34,.205,.18),(0,-3.46,3.4,.21,.23),(0,-3.27,3.43,.18,.2),(0,-3.14,3.4,.13,.15)],skin,c,n=12)
    tail=[]
    for j in range(24):
        t=j/23; y=1.11+3.95*t; x=.05+.33*math.sin(t*math.pi*.85)*t; z=2.06-.82*t-.27*math.sin(t*math.pi)
        rad=.375*(1-t)**1.55+.016
        tail.append((x,y,z,rad,rad*.93))
    loft('tapered-tail',tail,skin,c,n=12)
    # Distinct bent forelimbs and strong hindlimbs. Their feet define floor origin.
    for side,s in [('left',-1),('right',1)]:
        for kind,y,offset in [('fore',-.93,-.09 if s==1 else .09),('hind',.92,.08 if s==1 else -.08)]:
            if kind=='fore':
                nodes=[((s*.52,y,2.12),.30,.34),((s*.61,y-.01,1.72),.24,.27),((s*.65,y+.11,1.17),.185,.19),((s*.65,y-.04,.63),.15,.17),((s*.65,y+offset-.10,.18),.20,.24)]
            else:
                nodes=[((s*.50,y,2.17),.38,.42),((s*.64,y-.04,1.75),.31,.34),((s*.68,y-.25,1.25),.23,.26),((s*.68,y-.06,.68),.16,.18),((s*.68,y+offset-.07,.18),.22,.27)]
            tube(kind+'-limb-'+side,nodes,m['skin'],c,n=12)
            x=s*(.65 if kind=='fore' else .68); fy=y+offset-.1
            # Axial Z rings, flat sole at Z=0 and rounded toe spread.
            vertices=[];faces=[];n=12
            for z,rx,ry,shift in [(0,.22,.29,-.04),(.07,.25,.31,-.04),(.23,.23,.27,0),(.38,.17,.19,.035)]:
                for k in range(n):
                    a=2*math.pi*k/n;vertices.append((x+rx*math.cos(a),fy+shift+ry*math.sin(a),z))
            for j in range(3):
                for k in range(n):faces.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
            faces += [tuple(range(n-1,-1,-1)),tuple(3*n+k for k in range(n))]
            mesh_object(kind+'-foot-'+side,vertices,faces,m['skin'],c)
    # Pair of closed skin-covered ridges. Each toothed outline is a deliberately
    # modest sail between cervical supports, not exposed keratin horn sheaths.
    # (y,base z,base x,tip z,backward y lean). Height is artistic, not a measurement.
    stations=[(-3.03,3.49,.075,3.93,.18),(-2.81,3.51,.09,4.35,.37),(-2.56,3.44,.10,4.68,.49),(-2.28,3.29,.12,4.73,.51),(-1.98,3.09,.14,4.59,.48),(-1.67,2.91,.16,4.35,.42),(-1.33,2.73,.19,4.06,.35),(-.96,2.74,.24,3.77,.27),(-.57,2.78,.30,3.55,.19),(-.16,2.80,.32,3.40,.12),(.25,2.78,.31,3.27,.09),(.67,2.71,.28,3.13,.06),(1.08,2.53,.21,2.92,.04),(1.43,2.23,.14,2.58,.02)]
    for side,s in [('left',-1),('right',1)]:
        samples=[]
        for j,(y,bz,bx,tz,lean) in enumerate(stations):
            samples.append((y,bz,bx,y+lean,tz,bx+.17 if j<8 else bx+.03,True))
            if j<len(stations)-1:
                ny,nbz,nbx,ntz,nlean=stations[j+1]
                # Soft concave upper margin joins adjacent high supports.
                samples.append(((y+ny)/2,(bz+nbz)/2,(bx+nbx)/2,(y+lean+ny+nlean)/2,(bz+nbz)/2+.58*(min(tz,ntz)-(bz+nbz)/2) if j<7 else min(tz,ntz)-.09,(bx+nbx)/2+(.09 if j<8 else .025),False))
        verts=[];faces=[];mi=[];rows=5
        for thickness_side in [-1,1]:
            for y,bz,bx,ty,tz,tx,is_peak in samples:
                for k in range(rows):
                    t=k/(rows-1);half=.028*(1-t)+.013
                    xx=s*(bx+(tx-bx)*t)+thickness_side*half
                    verts.append((xx,y+(ty-y)*t,bz+(tz-bz)*t))
        N=len(samples)*rows
        for q in [0,1]:
            for j in range(len(samples)-1):
                for k in range(rows-1):
                    a=q*N+j*rows+k;faces.append((a,a+1,a+1+rows,a+rows));mi.append(1 if k==rows-2 else 0)
        for j in range(len(samples)-1):
            for k in [0,rows-1]:
                a=j*rows+k;b=(j+1)*rows+k;faces.append((a,b,b+N,a+N));mi.append(1 if k==rows-1 else 0)
        for j in [0,len(samples)-1]:
            for k in range(rows-1):
                a=j*rows+k;faces.append((a,a+N,a+N+1,a+1));mi.append(0)
        ob=mesh_object('paired-soft-crest-'+side,verts,faces,[m['crest'],m['crest_edge']],c)
        for poly,i in zip(ob.data.polygons,mi):poly.material_index=i
    if not gray:
        # Restrained eyes/naris and toe nails, not large decorative patterning.
        vertices=[];faces=[]
        for s in [-1,1]:
            ellipsoid_component(vertices,faces,(s*.198,-3.47,3.48),(.024,.046,.039),10,5)
            ellipsoid_component(vertices,faces,(s*.144,-3.77,3.375),(.016,.028,.018),8,4)
        mesh_object('eyes-and-nares',vertices,faces,m['eye'],c)
        vertices=[];faces=[]
        for s in [-1,1]:
            for kind,y,offset in [('fore',-.93,-.09 if s==1 else .09),('hind',.92,.08 if s==1 else -.08)]:
                for toe in [-1,0,1]:
                    x=s*(.65 if kind=='fore' else .68)+toe*.11;fy=y+offset-.38
                    ellipsoid_component(vertices,faces,(x,fy,.075),(.055,.085,.049),8,4)
        mesh_object('small-toe-nails',vertices,faces,m['claw'],c)
        # Short bilateral mouth creases are closed tubes, inset nearly flush.
        for s in [-1,1]:
            tube('mouth-crease-'+str(s),[((s*.15,-3.83,3.275),.008,.008),((s*.194,-3.66,3.265),.009,.009),((s*.199,-3.51,3.27),.007,.007)],m['eye'],c,n=6)
    return c


def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--params',type=Path,default=HERE/'params.json');ap.add_argument('--gray',action='store_true');args=ap.parse_args(argv)
    args.params=args.params.resolve();params=json.loads(args.params.read_text());out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    c=build(params,args.gray);policy=params['geometry_policy'];source=audit_source(c,policy['max_triangles'])
    if source['errors']:raise RuntimeError(source['errors'])
    scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2;scene['source_profile']='original palette-only living reconstruction';scene['scientific_limits']='Exact soft tissue, sail margins, colors and pose are artistic; not a specimen scan.'
    bpy.context.preferences.filepaths.save_version=0
    scene.render.filepath='//preview.png'
    # Reset startup file-browser locations before saving a portable source.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'/'*1023
                    space.params.directory=b'//'
                    space.params.filename=''
    os.chdir(out);bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in c.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[c['asset_root']]
    opts=dict(filepath='model.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties};assert set(opts)<=available
    bpy.ops.export_scene.gltf(**opts)
    glb=audit_glb(Path('model.glb'),policy['max_triangles'],policy['max_materials'],policy['max_primitives']);assert not glb['errors'],glb['errors'];assert glb['bytes']<=policy['max_glb_bytes']
    b=source['bounds_blender_m'];g=glb['bounds_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]};delta=max(abs(g[k][i]-expected[k][i]) for k in expected for i in range(3));assert delta<.0001;assert glb['scene_triangles']==source['triangles']
    report={'asset_id':params['asset_id'],'revision':params['revision'],'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256(args.params.resolve().read_bytes()).hexdigest(),'export_options':{k:v for k,v in opts.items() if k!='filepath'},'scope':'Static source and exact GLB technical audit only. No GPU, scene, scientific or independent visual acceptance.'}
    (out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'])
if __name__=='__main__':main()
