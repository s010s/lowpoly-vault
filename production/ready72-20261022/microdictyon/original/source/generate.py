#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Microdictyon reconstruction. Run with Blender 4.3.2, factory state.
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir DIR
No downloaded meshes, images, textures, or non-stdlib modeling dependencies.
"""
from pathlib import Path
import sys, math, json, hashlib, argparse
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tube(name, points, radii, sides, mat, col, smooth=True, cap_start=True, cap_end=True):
    v=[]; f=[]; points=[Vector(p) for p in points]
    for i,(p,r) in enumerate(zip(points,radii)):
        tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
        ref=Vector((0,0,1)) if abs(tangent.z)<0.93 else Vector((0,1,0))
        u=tangent.cross(ref).normalized(); w=tangent.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides
            v.append(tuple(p+r*(math.cos(a)*u+math.sin(a)*w)))
    for i in range(len(points)-1):
        for j in range(sides):
            a=i*sides+j; b=i*sides+(j+1)%sides
            f.append((a,b,b+sides,a+sides))
    if cap_start:f.append(tuple(range(sides-1,-1,-1)))
    if cap_end:f.append(tuple((len(points)-1)*sides+j for j in range(sides)))
    ob=mesh_object(name,v,f,mat,col)
    if smooth:
        for poly in ob.data.polygons:poly.use_smooth=len(poly.vertices)==4
    return ob

def lerp_table(y, table):
    if y<=table[0][0]:return table[0][1]
    for (a,av),(b,bv) in zip(table,table[1:]):
        if y<=b:
            t=(y-a)/(b-a); t=t*t*(3-2*t)
            return av*(1-t)+bv*t
    return table[-1][1]

def cx(y): return .00135*math.sin((y+.023)*58)+.00055*math.sin((y+.005)*105)
def cz(y): return lerp_table(y,[(-.0435,.0037),(-.033,.0052),(-.022,.0077),(.005,.0081),(.018,.0072),(.0265,.0052)])
def radial_direction(y,side,angle):
    dy=.07/120
    tangent=(Vector((cx(y+dy),y+dy,cz(y+dy)))-Vector((cx(y-dy),y-dy,cz(y-dy)))).normalized()
    u=tangent.cross(Vector((0,0,1))).normalized();w=tangent.cross(u).normalized()
    return side*math.sin(angle)*u-math.cos(angle)*w

def radius(y): return lerp_table(y,[(-.0435,.00062),(-.038,.0010),(-.029,.0019),(-.022,.00275),(-.012,.0030),(.01,.0030),(.02,.0027),(.0265,.00145)])

def clip_poly(poly,nx,ny,c):
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        dp=nx*p[0]+ny*p[1]-c; dq=nx*q[0]+ny*q[1]-c
        if dp<=1e-10:out.append(p)
        if (dp<0 and dq>0) or (dp>0 and dq<0):
            t=dp/(dp-dq); out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
    cleaned=[]
    for p in out:
        if not cleaned or math.dist(p,cleaned[-1])>1e-7:cleaned.append(p)
    if len(cleaned)>1 and math.dist(cleaned[0],cleaned[-1])<1e-7:cleaned.pop()
    return cleaned

def plate_template():
    # A clipped Voronoi sheet: 13 real apertures, shared top/bottom web edges,
    # explicit bore walls and exterior rim. One connected genus-13 solid.
    seeds=[(0.,0.)]+[(.43*math.cos(a),.43*math.sin(a)) for a in [math.pi/6+i*math.pi/3 for i in range(6)]]+[(.79*math.cos(a),.79*math.sin(a)) for a in [i*math.pi/3 for i in range(6)]]
    boundary=[(math.cos(i*2*math.pi/18),math.sin(i*2*math.pi/18)) for i in range(18)]
    cells=[]
    for sx,sy in seeds:
        poly=boundary[:]
        for tx,ty in seeds:
            if (tx,ty)==(sx,sy):continue
            poly=clip_poly(poly,tx-sx,ty-sy,(tx*tx+ty*ty-sx*sx-sy*sy)/2)
        cells.append(poly)
    verts=[]; index={}; faces=[]; boundary_edges={}; holes=[]
    def add(p,z):
        key=(round(p[0],8),round(p[1],8),z)
        if key not in index:index[key]=len(verts);verts.append(key)
        return index[key]
    for poly in cells:
        # Apertures stay in each cell; a 58% cell scale leaves robust web struts.
        c=(sum(p[0] for p in poly)/len(poly),sum(p[1] for p in poly)/len(poly))
        hole=[(c[0]+.58*(p[0]-c[0]),c[1]+.58*(p[1]-c[1])) for p in poly]
        holes.append(c)
        for k in range(len(poly)):
            p,q=poly[k],poly[(k+1)%len(poly)]; a,b=hole[k],hole[(k+1)%len(poly)]
            p0,q0,a0,b0=[add(v,0) for v in (p,q,a,b)]
            p1,q1,a1,b1=[add(v,1) for v in (p,q,a,b)]
            faces.extend([(p1,q1,b1,a1),(q0,p0,a0,b0),(a0,a1,b1,b0)])
            edge=tuple(sorted((p0,q0)))
            boundary_edges.setdefault(edge,[]).append((p0,q0,p1,q1))
    for edge,items in boundary_edges.items():
        if len(items)==1:
            p0,q0,p1,q1=items[0];faces.append((p0,q0,q1,p1))
        elif len(items)!=2:raise ValueError('Bad cell edge multiplicity')
    return verts,faces,holes

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--gray',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    params=json.loads((HERE/'params.json').read_text())
    col=setup_scene('microdictyon',params['seed'])
    scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
    palette=params['palette_srgb']
    mats={k:make_material(k,'#929292' if args.gray else v,.86) for k,v in palette.items()}
    root=bpy.data.objects['microdictyon']
    root['reconstruction']='Nine pairs follows tentative Chen et al. 2024 interpretation; older ten-pair reconstruction disputed.'
    root['scale_note']='Representative 70 mm anterior-posterior extent; not direct specimen measurement.'
    # Continuous tubular soft trunk. Low-amplitude annulation changes real radius.
    n=121;ys=[-.0435+.07*i/(n-1) for i in range(n)]
    points=[(cx(y),y,cz(y)) for y in ys]
    radii=[radius(y)*(1+.035*math.cos(2*math.pi*i/2)) for i,y in enumerate(ys)]
    body=tube('soft_annulated_trunk_and_limb_free_anterior',points,radii,10,mats['soft_trunk'],col,True,False,True)
    # Small terminal recessed mouth. No invented eyes/head shield.
    start=Vector(points[0]);tangent=(Vector(points[1])-start).normalized()
    lip=tube('terminal_mouth_lining',[tuple(start),tuple(start+tangent*.00004),tuple(start+tangent*.00065)],[radii[0],radii[0]*.94,.00025],10,mats['mouth_recess'],col,False,False,True)
    plate_v,plate_f,hole_centres=plate_template()
    stations=[];claw_geometries=[]
    sizes=[.76,.88,.98,1,1,1,.98,.88,.7]
    leg_lengths=[]
    for i in range(9):
        y=-.0215+i*.0058; r=radius(y); z=cz(y); x=cx(y)
        stations.append({'station':i+1,'y_m':y,'center_x_m':x,'body_z_m':z,'scale':sizes[i]})
        for side in [-1,1]:
            tag=('L' if side<0 else 'R')+f'{i+1:02d}'
            # Plates curve around each dorsolateral shoulder, leaving the midline bare.
            verts=[]
            for u,v,layer in plate_v:
                yy=y+u*.0025*sizes[i]
                angle=.82+v*.65*sizes[i]
                radial=radius(yy)+.00022+layer*.00016
                verts.append(tuple(Vector((cx(yy),yy,cz(yy)))+radial*radial_direction(yy,side,angle)))
            ob=mesh_object('perforated_sclerite_'+tag,verts,plate_f,mats['sclerites'],col)
            ob['station']=i+1;ob['side']='left' if side<0 else 'right';ob['true_apertures']=13
            # Non-jointed tapered lobopods, continuously curved; posterior pair shortest.
            reach=(.0085 if i<8 else .0057)*(1+(.04*math.sin(i*1.5+side)))
            foot_y=y+(.0011*math.sin(i*1.1+side*.8) if i<8 else .0011)
            foot=Vector((x+side*reach,foot_y,.00066))
            base=Vector((x+side*r*.6,y,z-r*.45))
            ctrl=Vector((x+side*(reach*.7),y+.0006*side,z*.63))
            legpts=[];legr=[]
            for j in range(7):
                t=j/6; p=(1-t)**2*base+2*(1-t)*t*ctrl+t*t*foot
                legpts.append(tuple(p));legr.append((.00078*(1-t)+.00023*t)*(1 if i<8 else .82))
            leg=tube('lobopod_'+tag,legpts,legr,7,mats['soft_trunk'],col,True)
            leg['station']=i+1;leg['non_jointed']=True
            length=sum(math.dist(a,b) for a,b in zip(legpts,legpts[1:]));leg_lengths.append({'part':leg.name,'length_m':length})
            for k in [-1,1]:
                p0=foot+Vector((0,k*.00018,0))
                p1=foot+Vector((side*.00025,k*.00035,-.0001))
                p2=foot+Vector((side*.00045,k*.0005,-.00058))
                claw=tube('claw_'+tag+('_a' if k<0 else '_b'),[p0,p1,p2],[.00014,.00011,.000055],5,mats['claw_tips'],col,False)
                claw_geometries.append(claw)
    # One editable named claw mesh keeps source semantic legs and 18 plates separate,
    # while avoiding 36 tiny rendering primitives. No boolean or destructive unions.
    cv=[];cf=[]
    for ob in claw_geometries:
        off=len(cv);cv.extend(tuple(v.co) for v in ob.data.vertices);cf.extend(tuple(off+j for j in p.vertices) for p in ob.data.polygons)
    for ob in claw_geometries:bpy.data.objects.remove(ob,do_unlink=True)
    claws=mesh_object('paired_terminal_claws_36',cv,cf,mats['claw_tips'],col)
    claws['count']=36
    # Root remains identity. Ground and centre the actual claw footprint numerically.
    minz=min(v.co.z for v in claws.data.vertices);minx=min(v.co.x for v in claws.data.vertices);maxx=max(v.co.x for v in claws.data.vertices)
    miny=min(v.co.y for v in claws.data.vertices);maxy=max(v.co.y for v in claws.data.vertices)
    shift=Vector((-(minx+maxx)/2,-(miny+maxy)/2,-minz))
    for ob in col.objects:
        if ob.type=='MESH':
            for v in ob.data.vertices:v.co+=shift
    bpy.context.view_layer.update()
    source=audit_source(col,max_triangles=params['geometry_policy']['max_triangles'])
    write(out/'source-qa.json',source)
    if source['errors']:raise RuntimeError('Source audit failed: '+repr(source['errors']))
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=root
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Required exporter options unavailable')
    bpy.ops.export_scene.gltf(**opts)
    audit=audit_glb(out/'model.glb',params['geometry_policy']['max_triangles'],params['geometry_policy']['max_materials'],params['geometry_policy']['max_primitives'])
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(audit['bounds_m'][s][j]-expected[s][j]) for s in ('min','max') for j in range(3))
    if delta>1e-7:audit['errors'].append('Source/export bounds mismatch')
    if source['triangles']!=audit['scene_triangles']:audit['errors'].append('Source/export triangle mismatch')
    if audit['bytes']>params['geometry_policy']['max_glb_bytes']:audit['errors'].append('GLB size budget exceeded')
    write(out/'glb-qa.json',audit)
    if audit['errors']:raise RuntimeError('GLB audit failed: '+repr(audit['errors']))
    write(out/'build-receipt.json',{'asset_id':'microdictyon','revision':'r001','gray':args.gray,'blender':bpy.app.version_string,'gltf_exporter':'4.3.47','threads':2,'seed':params['seed'],'source_sha256':sha(Path(__file__)),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'semantic_sha256':audit['semantic_sha256'],'blend_sha256':sha(out/'model.blend'),'bounds_delta_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'geometry_policy':params['geometry_policy'],'counts':{'leg_pairs':9,'sclerite_pairs':9,'claws':36,'perforations_per_sclerite':13,'total_real_plate_apertures':234},'station_data':stations,'limb_centerline_lengths':leg_lengths,'ground_shift_m':list(shift),'notes':['70 mm longitudinal extent is representative, not a measured fossil length.','Nine limb pairs follow a tentative 2024 interpretation instead of older ten-pair reconstructions.','Normal intermolt condition; no permanently duplicated molting plates.','Soft body cross-section, resting/walking pose and color reconstructed.','13 apertures per plate simplify the microscopic reticulum, not an exact hole count.','Source meshes intentionally overlap at soft limb attachment; no claim of a printable union.']})
    print('BUILD_COMPLETE',json.dumps({'triangles':audit['scene_triangles'],'bytes':audit['bytes'],'primitives':audit['scene_primitives_estimated_base_draw_calls'],'sha256':audit['sha256']}))
if __name__=='__main__':main()
