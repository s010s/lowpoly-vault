# SPDX-License-Identifier: MIT
"""Original Cartorhynchus living reconstruction. Blender 4.3.2, deterministic.
Usage: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir DIR
All imported project dependencies are vendored in this source directory.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, ground_asset, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,default=HERE.parent); ap.add_argument('--clay',action='store_true')
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text()); C=setup_scene('cartorhynchus',seed=p['seed'])
    root=bpy.data.objects['cartorhynchus']; root['taxon']='Cartorhynchus lenticarpus'; root['specimen_basis']='AGB6257'; root['reconstruction']='Original living reconstruction; inferred missing distal tail and soft tissues'; root['teeth']='Closed mouth; hidden rounded posterior crushing teeth not visible'; root['origin']='Ventral tangent plane under trunk center; neutral swimming display pose'
    pal=p['palette_hex']; mats={n:make_material(n,'#929292' if args.clay else c,roughness=.78 if n=='eye-black' else .88) for n,c in pal.items()}
    n=24
    profiles=p['body_profiles']
    verts=[]; faces=[]; band=[]
    # y, lateral radius, center height, vertical radius, lateral center.
    for y,rx,z,rz,xc in profiles:
        for j in range(n):
            a=2*math.pi*j/n
            verts.append((xc+rx*math.cos(a),y,z+rz*math.sin(a)))
    for i in range(len(profiles)-1):
        for j in range(n):
            faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
            s=math.sin(2*math.pi*(j+.5)/n)
            band.append(0 if s>.28 else 2 if s<-.43 else 1)
    faces += [tuple(range(n-1,-1,-1)),tuple((len(profiles)-1)*n+j for j in range(n))]; band += [1,0]
    body=mesh_object('axial-body-short-skull-trunk-tapered-tail',verts,faces,[mats['dorsal-sage'],mats['flank-grey'],mats['ventral-sand']],C)
    for poly,mi in zip(body.data.polygons,band): poly.material_index=mi
    for name,(lo,hi) in {'short-rounded-skull':(-.126,-.065),'short-neck-trunk':(-.065,.065),'inferred-distal-tail':(.065,.276)}.items():
        g=body.vertex_groups.new(name=name); g.add([v.index for v in body.data.vertices if lo<=v.co.y<=hi],1.0,'REPLACE')
    body['topology']='24-sided deliberate elliptical profile loft; continuous skull, trunk and laterally flattened tapered tail'
    # The paddle lofts are broad and blunt, without projecting digits or claws.
    # Single material each keeps the draw-call budget independent of anatomy count.
    paddle_metrics={}
    for kind in ('fore','hind'):
        profiles=p[kind+'_paddle_profiles']
        for side in (-1,1):
            vv=[]; ff=[]; N=16
            for x,y,z,w,h in profiles:
                for j in range(N):
                    a=2*math.pi*j/N
                    vv.append((side*x,y+w*math.cos(a),z+h*math.sin(a)))
            for i in range(len(profiles)-1):
                for j in range(N): ff.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
            ff += [tuple(range(N-1,-1,-1)),tuple((len(profiles)-1)*N+j for j in range(N))]
            name=kind+'paddle-'+('left' if side<0 else 'right')
            obj=mesh_object(name,vv,ff,mats['flank-grey'],C)
            obj['anatomy']='Broad flexible-wrist forepaddle' if kind=='fore' else 'Smaller rounded hindpaddle'
            for label,ixs in [('proximal-attachment',range(0,N*2)),('flexible-wrist',range(N*2,N*4)),('rounded-distal-paddle',range(N*4,len(vv)))]:
                g=obj.vertex_groups.new(name=label);g.add(list(ixs),1.,'REPLACE')
            paddle_metrics[name]={'max_chord_m':2*max(x[3] for x in profiles),'reach_m':max(x[0] for x in profiles)-min(x[0] for x in profiles),'sections':len(profiles)}
    # All small facial features are one editable mesh with two material groups.
    fv=[];ff=[];fm=[];groups=[]
    def ellipsoid(name,center,radii,material,axis=None,segments=16,rings=8):
        start=len(fv); center=Vector(center); rot=axis.to_track_quat('Z','Y') if axis is not None else None
        def tr(v):
            q=Vector(v); return tuple(center+(rot@q if rot else q))
        fv.append(tr((0,0,radii[2])))
        for i in range(1,rings):
            t=math.pi*i/rings
            for j in range(segments):
                a=2*math.pi*j/segments; fv.append(tr((radii[0]*math.sin(t)*math.cos(a),radii[1]*math.sin(t)*math.sin(a),radii[2]*math.cos(t))))
        bottom=len(fv);fv.append(tr((0,0,-radii[2])))
        for j in range(segments): ff.append((start,start+1+j,start+1+(j+1)%segments));fm.append(material)
        for i in range(rings-2):
            for j in range(segments):
                a=start+1+i*segments+j;b=start+1+i*segments+(j+1)%segments
                ff.append((a,a+segments,b+segments,b));fm.append(material)
        for j in range(segments):ff.append((bottom,bottom-segments+(j+1)%segments,bottom-segments+j));fm.append(material)
        groups.append((name,list(range(start,len(fv)))))
    def tube(name,points,radius):
        start=len(fv);N=6
        for i,pos in enumerate(points):
            tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)]); tangent.normalize()
            u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u).normalized()
            for j in range(N):fv.append(tuple(Vector(pos)+radius*(u*math.cos(2*math.pi*j/N)+v*math.sin(2*math.pi*j/N))))
        for i in range(len(points)-1):
            for j in range(N):ff.append((start+i*N+j,start+i*N+(j+1)%N,start+(i+1)*N+(j+1)%N,start+(i+1)*N+j));fm.append(0)
        ff.extend([tuple(start+j for j in reversed(range(N))),tuple(start+(len(points)-1)*N+j for j in range(N))]);fm.extend([0,0]);groups.append((name,list(range(start,len(fv)))))
    for s in (-1,1):
        ax=Vector((s*.96,-.12,.24)).normalized()
        c=Vector((s*.0241,-.106,.0439))
        ellipsoid('eye-rim-'+str(s),c,(.0055,.0055,.0022),1,ax)
        ellipsoid('eye-black-'+str(s),c+ax*.0015,(.0045,.0045,.0015),0,ax)
        ellipsoid('nostril-'+str(s),(s*.0106,-.1215,.0371),(.00115,.0016,.0007),0,Vector((s*.3,-.4,1)).normalized(),12,6)
        points=[]
        anchors=[(-.1225,.0276),(-.1165,.0272),(-.107,.0267),(-.096,.0265),(-.085,.0267),(-.077,.0277)]
        for k in range(25):
            y=anchors[0][0]+(anchors[-1][0]-anchors[0][0])*k/24
            for aa,bb in zip(anchors,anchors[1:]):
                if aa[0]-1e-8<=y<=bb[0]+1e-8:
                    u=(y-aa[0])/(bb[0]-aa[0]);z=aa[1]*(1-u)+bb[1]*u;break
            for a,b in zip(p['body_profiles'],p['body_profiles'][1:]):
                if a[0]<=y<=b[0]:
                    t=(y-a[0])/(b[0]-a[0]);rx=a[1]*(1-t)+b[1]*t;zc=a[2]*(1-t)+b[2]*t;rz=a[3]*(1-t)+b[3]*t
                    step=2*math.pi/n;angle=math.asin((z-zc)/rz);low=math.floor(angle/step)*step;high=low+step
                    za=zc+rz*math.sin(low);zb=zc+rz*math.sin(high)
                    u=(z-za)/(zb-za);x=rx*((1-u)*math.cos(low)+u*math.cos(high))+.00004
                    points.append((s*x,y,z));break
        tube('closed-mouth-seam-'+str(s),points,.00032)
    face=mesh_object('eyes-nostrils-closed-mouth',fv,ff,[mats['eye-black'],mats['iris-bronze']],C)
    for poly,mi in zip(face.data.polygons,fm):poly.material_index=mi
    for name,indices in groups:g=face.vertex_groups.new(name=name);g.add(indices,1.,'REPLACE')
    offset=ground_asset(C,center_xy=False)
    source=audit_source(C,max_triangles=p['geometry_policy']['max_triangles'])
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in C.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=root
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={prop.identifier for prop in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Required exporter flags unavailable')
    bpy.ops.export_scene.gltf(**options)
    audit=audit_glb(out/'model.glb',p['geometry_policy']['max_triangles'],p['geometry_policy']['max_materials'],p['geometry_policy']['max_primitives'])
    if audit['errors']:raise RuntimeError(audit['errors'])
    if audit['bytes']>p['geometry_policy']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(expected[k][i]-audit['bounds_m'][k][i]) for k in expected for i in range(3))
    if delta>.0001 or source['triangles']!=audit['scene_triangles']:raise RuntimeError('Source/export mismatch')
    exporter=__import__('io_scene_gltf2');
    write(out/'qa/evidence/build.json',{'asset_id':'cartorhynchus','revision':'r001','maker_task':'maker','blender':bpy.app.version_string,'seed':p['seed'],'exporter_version':list(exporter.bl_info['version']),'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'clay':args.clay,'source':source,'glb':audit,'source_export_bounds_delta_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'origin':'Ventral tangent plane under trunk center; neutral swimming display pose','ground_translation_m':offset,'paddles':paddle_metrics,'palette_hex':pal,'source_scene_has_preview_objects':False,'gpu':'NOT_RUN','populated_scene':'NOT_RUN'})
    print(json.dumps({'status':'BUILD_TECHNICAL_PASS','glb_sha256':sha(out/'model.glb'),'triangles':audit['scene_triangles'],'semantic_sha256':audit['semantic_sha256']}))
if __name__=='__main__':main()
