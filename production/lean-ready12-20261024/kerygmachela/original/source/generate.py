# SPDX-License-Identifier: MIT
"""Original deterministic Kerygmachela reconstruction. Run in Blender with -- --output DIR.
Only the adjacent params.json and pinned deps are construction dependencies.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,ground_asset,audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

def tube(points,radii,sides=10):
    verts=[];faces=[]
    for i,p in enumerate(points):
        t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        t.normalize(); a=t.cross(Vector((0,0,1))).normalized(); b=t.cross(a).normalized()
        for j in range(sides):
            angle=2*math.pi*j/sides
            v=Vector(p)+radii[i]*(math.cos(angle)*a+math.sin(angle)*b)
            verts.append(tuple(v))
    for i in range(len(points)-1):
        for j in range(sides): faces.append((i*sides+j,i*sides+(j+1) % sides,(i+1)*sides+(j+1) % sides,(i+1)*sides+j))
    faces.extend([tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))])
    return verts,faces

def combine(parts):
    v=[];f=[]
    for vv,ff in parts:
        off=len(v);v.extend(vv);f.extend(tuple(i+off for i in face) for face in ff)
    return v,f

def interp(t, knots):
    for i in range(1,len(knots)):
        if t<=knots[i][0]:
            q=(t-knots[i-1][0])/(knots[i][0]-knots[i-1][0]);return knots[i-1][1]*(1-q)+knots[i][1]*q
    return knots[-1][1]

def body_radius(y):
    t=(y+.0325)/.065
    return interp(t,[(0,.0010),(.045,.0030),(.12,.0043),(.22,.0057),(.40,.0066),(.53,.0064),(.65,.0059),(.78,.0047),(.90,.0034),(1,.00135)])


def make_model():
    c=setup_scene(P['asset_id'],P['seed']); mats={k:make_material(k,v,roughness=.83 if k!='eyes' else .67) for k,v in P['palette'].items()}
    rows=[-.026+i*.00525 for i in range(11)]
    # A single continuous surface carries annulations and all 44 restrained tubercles.
    n=32; nr=111;v=[];f=[]; rowangles=[math.radians(a) for a in [35,70,110,145]]
    for iy in range(nr):
        y=-.0325+.065*iy/(nr-1);r=body_radius(y)
        ann=.026*math.cos((y-rows[0])*2*math.pi/.00175)
        for j in range(n):
            a=2*math.pi*j/n
            bump=0
            for cy in rows:
                gy=math.exp(-((y-cy)/.00095)**2)
                if gy<.0001:continue
                for ia,ca in enumerate(rowangles):
                    da=(a-ca+math.pi) % (2*math.pi)-math.pi
                    bump+=gy*math.exp(-(da/.16)**2)*(.00048 if ia in (0,3) else .00082)
            x=math.cos(a)*(r*(1+ann)+bump)
            z=.0053+math.sin(a)*(.0044*(r/.0066)**.65*(1+ann)+bump)
            v.append((x,y,z))
    for iy in range(nr-1):
        for j in range(n):f.append((iy*n+j,iy*n+(j+1) % n,(iy+1)*n+(j+1) % n,(iy+1)*n+j))
    f += [tuple(range(n-1,-1,-1)),tuple((nr-1)*n+j for j in range(n))]
    body=mesh_object('soft-trunk-integrated-44-tubercles',v,f,[mats['cuticle'],mats['ventral']],c)
    for poly in body.data.polygons:
        poly.material_index=1 if poly.center.z<.003 else 0
        poly.use_smooth=True
    body['tubercle_rows']=11;body['tubercles_per_row']=4;body['surface']='continuous soft annulated cuticle, not armor'
    # Thin closed swept rounded paddle volumes. Distal margins have clear spacing.
    spans=[.0100,.0130,.0152,.0170,.0170,.0160,.0143,.0123,.0101,.0076,.0047]
    parts=[];flap_metrics=[]
    for side in [-1,1]:
        for i,(y0,L) in enumerate(zip(rows,spans)):
            root=body_radius(y0)*.78; centerz=.0047
            stations=[(0,.00180,.00067),(.17,.00265,.00065),(.43,.0029,.00058),(.70,.00265,.00044),(.89,.00185,.00029),(1,.00022,.00015)]
            chordscale=.86+ .14*math.sin(math.pi*i/10)
            vv=[];ff=[];sides=10
            for t,ry,rz in stations:
                cy=y0+.00135*t+.00025*math.sin(i*.8)*t
                cz=centerz+.00065*math.sin(i*.8+.3)*t+.00085*math.sin(math.pi*t)
                for j in range(sides):
                    a=2*math.pi*j/sides
                    vv.append((side*(root+L*t),cy+ry*chordscale*math.cos(a),cz+rz*math.sin(a)))
            for k in range(len(stations)-1):
                for j in range(sides):ff.append((k*sides+j,k*sides+(j+1) % sides,(k+1)*sides+(j+1) % sides,(k+1)*sides+j))
            ff.extend([tuple(range(sides-1,-1,-1)),tuple((len(stations)-1)*sides+j for j in range(sides))])
            parts.append((vv,ff));flap_metrics.append({'side':side,'pair':i+1,'center_y_m':y0,'span_m':L,'closed':True})
    vv,ff=combine(parts);flaps=mesh_object('eleven-bilateral-flap-pairs',vv,ff,[mats['cuticle'],mats['flap_edge'],mats['ventral']],c)
    # Each component has 50 side quads plus two end caps; distal band is a bounded palette choice.
    for k,p in enumerate(flaps.data.polygons):
        local=k % 52;p.material_index=1 if local>=40 else 2 if p.center.z<.0045 else 0
        p.use_smooth=True
    flaps['bilateral_pairs']=11;flaps['largest_pairs']='4,5';flaps['closed_components']=22
    # One median, unsegmented spine, gently elevated, approximately trunk length.
    pts=[];rs=[]
    for k in range(13):
        t=k/12;pts.append((.0008*math.sin(math.pi*t),.0317+.0608*t,.0054+.0043*t+.001*math.sin(math.pi*t)));rs.append(.00150*(1-t)**1.15+.00007)
    vv,ff=tube(pts,rs,10); tail=mesh_object('single-median-tail-spine',vv,ff,mats['cuticle'],c)
    for p in tail.data.polygons:p.use_smooth=True
    tail['count']=1;tail['unsegmented']=True
    # Paired broad-based frontal appendages with forward-curved inward branches.
    for side in [-1,1]:
        pts=[];rs=[]
        for k in range(13):
            t=k/12;pts.append((side*(.0034+.0130*t-.0025*t*t),-.0275-.0400*t,.0057+.0050*t-.0008*math.sin(math.pi*t)));rs.append(.00265*(1-t)**1.4+.00009)
        parts=[tube(pts,rs,10)]
        for j,t in enumerate([.16,.27,.39,.51,.64,.76]):
            x=side*(.0034+.013*t-.0025*t*t);y=-.0275-.040*t;z=.0057+.005*t-.0008*math.sin(math.pi*t)
            length=[.0036,.0048,.0062,.0080,.0100,.0110][j]
            branch=[];rad=[]
            for k in range(6):
                u=k/5;branch.append((x-side*(.0021*math.sin(math.pi*u/2)+.0010*u),y-length*u,z+.0005*math.sin(math.pi*u)))
                rad.append((.00058-.000035*j)*(1-u)+.000055)
            parts.append(tube(branch,rad,8))
        vv,ff=combine(parts);o=mesh_object(('left' if side<0 else 'right')+'-frontal-appendage-six-spines',vv,ff,mats['cuticle'],c)
        for p in o.data.polygons:p.use_smooth=True
    # Sessile kidney-shaped eye lobes under the appendage bases, not spheres.
    outline=[(-.28,-1),(.35,-.90),(.65,-.50),(.72,.0),(.48,.60),(.08,1),(-.40,.90),(-.30,.50),(-.12,.10),(-.27,-.45)]
    for side in [-1,1]:
        vv=[];ff=[]
        for scl,z in [(0.78,.00265),(1,.00315),(.85,.0038)]:
            for x,y in outline:vv.append((side*(.00415+x*.0020*scl),-.0275+y*.0035*scl,z))
        for k in range(2):
            for j in range(10):ff.append((k*10+j,k*10+(j+1) % 10,(k+1)*10+(j+1) % 10,(k+1)*10+j))
        ff.extend([tuple(range(9,-1,-1)),tuple(20+j for j in range(10))]);o=mesh_object(('left' if side<0 else 'right')+'-sessile-kidney-eye',vv,ff,mats['eyes'],c)
        for p in o.data.polygons:p.use_smooth=True
    # Ventral mouth and paired rostral spines, deliberately understated.
    pts=[(0,-.0316,.0030),(0,-.0327,.0032)]; vv,ff=tube(pts,[.00064,.00051],10);mesh_object('ventral-mouth-opening',vv,ff,mats['eyes'],c)
    parts=[]
    for side in [-1,1]:parts.append(tube([(side*.0012,-.0306,.0033),(side*.00145,-.0330,.0030),(side*.0015,-.0346,.00335)],[.00042,.00024,.000065],8))
    vv,ff=combine(parts);mesh_object('paired-rostral-spines',vv,ff,mats['ventral'],c)
    shift=ground_asset(c,center_xy=False)
    return c,flap_metrics,shift


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    c,flaps,shift=make_model(); source=audit_source(c,12000)
    write(out/'source-audit.json',source)
    if source['errors']:raise RuntimeError(str(source['errors']))
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    # Portable presentation defaults; exclude inherited file-browser and output locations.
    bpy.context.scene.render.filepath='//render'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
                    space.params.filename=''
                    space.params.filter_glob=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in c.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[c['asset_root']]
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    supported={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    assert not set(options)-supported, set(options)-supported
    bpy.ops.export_scene.gltf(**options)
    audit=audit_glb(out/'model.glb',12000,6,32);audit['file']='model.glb';write(out/'glb-audit.json',audit)
    assert not audit['errors'],audit['errors'];assert audit['bytes']<=1800000
    bb=source['bounds_blender_m']; expected={'min':[bb['min'][0],bb['min'][2],-bb['max'][1]],'max':[bb['max'][0],bb['max'][2],-bb['min'][1]]}
    delta=max(abs(audit['bounds_m'][edge][i]-expected[edge][i]) for edge in expected for i in range(3))
    assert delta<.0001 and source['triangles']==audit['scene_triangles']
    try:
        import io_scene_gltf2
        exporter=str(io_scene_gltf2.bl_info['version'])
    except Exception:exporter='bundled with Blender '+bpy.app.version_string
    write(out/'build-record.json',{'asset_id':P['asset_id'],'revision':P['revision'],'seed':P['seed'],'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blender_version':bpy.app.version_string,'exporter_version':exporter,'export_options':{k:v for k,v in options.items() if k!='filepath'},'glb_sha256':sha(out/'model.glb'),'semantic_sha256':audit['semantic_sha256'],'bounds_roundtrip_max_error_m':delta,'source_to_export_triangle_match':True,'ground_shift_m':shift,'flap_pairs':flaps,'scientific_scope':'Original external living reconstruction; tissue depth, color and pose are artistic; not a fossil scan or adult maximum.'})
    print('BUILD_COMPLETE',audit['scene_triangles'],audit['bytes'])
if __name__=='__main__':main()
