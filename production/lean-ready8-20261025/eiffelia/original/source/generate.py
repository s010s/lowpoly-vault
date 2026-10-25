# SPDX-License-Identifier: MIT
"""Original Eiffelia globosa r001. Deterministic original profile and wall relief.
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output rebuilt
No reference pixels, acquired meshes, or network resources are used by the build.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P={}; C=None; M={}; OUTER=None; BVH=None; STAR_RECORDS=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def radius(z):
    rows=P['outer_profile_mm']
    for (za,ra),(zb,rb) in zip(rows,rows[1:]):
        if za<=z<=zb:return ra+(rb-ra)*(z-za)/(zb-za)
    return rows[0][1] if z<0 else rows[-1][1]
def slope(z):
    rows=P['outer_profile_mm']
    for (za,ra),(zb,rb) in zip(rows,rows[1:]):
        if za<=z<=zb:return (rb-ra)/(zb-za)
    return 0
def point(theta,z,r=None):
    if r is None:r=radius(z)
    # Low-frequency, restrained asymmetry. No noise or random face colors.
    t=z/P['outer_profile_mm'][-1][0]
    mod=1+.014*math.sin(3*theta+.55)*math.sin(math.pi*t)**2
    cx=.30*math.sin(math.pi*t)*math.sin(.7+1.5*t)
    cy=.22*math.sin(math.pi*t)*math.sin(2.1*t)
    return Vector((cx+r*math.cos(theta)*mod,cy+.965*r*math.sin(theta)*mod,z+.10*math.sin(theta+.3)*t**5))
def make_shell():
    global OUTER,BVH
    n=P['radial_segments']; outer=P['outer_profile_mm'];v=[];f=[]
    for z,r in outer:
        for j in range(n):v.append(tuple(point(2*math.pi*j/n,z,r)))
    for k in range(len(outer)-1):
        for j in range(n):
            a=k*n+j;b=k*n+(j+1)%n;f.append((a,b,b+n,a+n))
    outerfaces=list(f);outerverts=list(v)
    # A small completed basal contact disk is the lower sac, not an attachment pad.
    f.append(tuple(range(n-1,-1,-1)))
    inner=[(z,max(.55,r-P['wall_thickness_mm'])) for z,r in reversed(outer[2:])]
    inner += [(1.10,2.80),(.90,.80)]
    for z,r in inner:
        for j in range(n):v.append(tuple(point(2*math.pi*j/n,z,r)))
    last=(len(outer)-1)*n
    for k in range(len(inner)):
        nxt=len(outer)*n+k*n
        for j in range(n):f.append((last+j,last+(j+1)%n,nxt+(j+1)%n,nxt+j))
        last=nxt
    f.append(tuple(last+j for j in range(n)))
    OUTER=mesh_object('continuous-hollow-sac-open-osculum',v,f,M['soft_wall'],C)
    OUTER['anatomy']='One connected, closed material wall with genuinely open upper lumen, connected rim and completed lower sac; no cap at osculum.'
    OUTER['source_anchor']='ROM 53567 outline and scale; USNM 66522 aperture; volume and thickness interpretive.'
    OUTER['outer_vertex_count']=len(outerverts)
    OUTER['outer_ring_count']=len(outer)
    BVH=BVHTree.FromPolygons([Vector(x) for x in outerverts],outerfaces,all_triangles=False)
    return OUTER
def mapped(theta,z,dx,dy,height):
    # Coordinates follow the wall in the local circumferential/meridional metric.
    r=radius(z);zz=z+dy/math.sqrt(1+slope(z)**2)
    if not .25<zz<30.08:raise ValueError('Spicule outside supported sac surface')
    approx=point(theta+dx/max(r,1),zz)
    hit,normal,index,dist=BVH.find_nearest(approx)
    if hit is None:raise ValueError('No shell attachment')
    # Face normals must be outward even on the lower and upper shoulder slopes.
    radial=Vector((hit.x,hit.y,0))
    if normal.dot(radial)<0:normal=-normal
    return tuple(hit+normal*height)
class StarGroup:
    def __init__(self,name,material):self.name=name;self.mat=material;self.v=[];self.f=[]
    def star(self,theta,z,n,length,rotation,index,group):
        off=len(self.v);verts=[];faces=[]
        hub=(.30 if n==6 else .18)*(length/(3.8 if n==6 else 1.4))**.55
        relief=(.22 if group=='large' else .17 if group=='medium' else .12)
        def p(x,y,h):return mapped(theta,z,x,y,h)
        # Closed shared hub. Each ray attaches to one complete prism side, sharing
        # all four root vertices, rather than six disconnected ornamental sticks.
        for h in [-.16,relief]:
            for j in range(n):
                a=rotation+2*math.pi*(j-.5)/n
                verts.append(p(hub*math.cos(a),hub*math.sin(a),h))
        faces.append(tuple(range(n-1,-1,-1)));faces.append(tuple(n+j for j in range(n)))
        for j in range(n):
            a=rotation+2*math.pi*j/n;u=Vector((math.cos(a),math.sin(a)));perp=Vector((-u.y,u.x))
            L=length*(1+.12*math.sin(1.7*index+2.3*j))
            mid=u*(L*.54);width=hub*math.sin(math.pi/n)*.59
            k=len(verts)
            # Same corner order as the hub root: lower left, lower right,
            # upper right, upper left. The lower section embeds into the wall.
            for sign,h in [(-1,-.13),(1,-.13),(1,relief*.82),(-1,relief*.82)]:
                xy=mid+perp*(sign*width);verts.append(p(xy.x,xy.y,h))
            root=[j,(j+1)%n,n+(j+1)%n,n+j]
            midids=[k,k+1,k+2,k+3]
            for q in range(4):faces.append((root[q],root[(q+1)%4],midids[(q+1)%4],midids[q]))
            tip=len(verts);xy=u*L;verts.append(p(xy.x,xy.y,0))
            for q in range(4):faces.append((midids[q],midids[(q+1)%4],tip))
        self.v.extend(verts);self.f.extend(tuple(off+i for i in face) for face in faces)
        STAR_RECORDS.append({'group':group,'surface_rays':n,'theta_rad':theta,'z_mm':z,'ray_length_mm':length,'vertices':len(verts),'faces':len(faces),'base_inset_mm':.16,'hub_relief_mm':relief,'shared_hub':True})
    def make(self):
        ob=mesh_object(self.name,self.v,self.f,self.mat,C)
        ob['construction']='Each closed star shares a connected central hub with its rays; lower faces intersect the continuous body wall. Relief follows the exact polygonal shell. No radial spray.'
        return ob
def make_spicules():
    for group,n,param,mat in [('large',6,'large_six_rayed_rows','large_spicules'),('medium',6,'medium_six_rayed_rows','smaller_spicules'),('small',4,'small_four_rayed_rows','smaller_spicules')]:
        G=StarGroup(group+'-wall-following-'+str(n)+'-rayed-spicules',M[mat]);idx=0
        for row,entry in enumerate(P[param]):
            count=entry['count'];offset={'large':.12,'medium':.53,'small':.78}[group]
            for j in range(count):
                theta=2*math.pi*(j+offset+(row%2)*.47)/count+.05*math.sin(1.8*j+.9*row)
                z=entry['z']+.28*math.sin(j*2.2+row*.6)
                L=entry['ray_length']*(1+.10*math.sin(j*1.3+row*1.9))
                rot=(.015 if group=='large' else .22)+.11*math.sin(j*.8+row*.7)
                G.star(theta,z,n,L,rot,idx,group);idx+=1
        G.make()
def main():
    global P,C,M
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    P=json.loads((HERE/'params.json').read_text());C=setup_scene('eiffelia',P['seed'])
    M={k:make_material(k,v,roughness=P['surface']['roughness']) for k,v in P['surface']['palette_srgb'].items()}
    make_shell();make_spicules()
    # Calibrate only uniform scale from maximum transverse body diameter, excluding
    # spicule relief. The profile and all spicules are scaled together, not stretched.
    pts=[v.co.copy() for v in OUTER.data.vertices[:OUTER['outer_vertex_count']]]
    diameter=max(math.hypot(p.x-q.x,p.y-q.y) for i,p in enumerate(pts) for q in pts[:i])
    factor=P['body_diameter_m']/diameter
    for ob in C.all_objects:
        if ob.type=='MESH':
            for v in ob.data.vertices:v.co*=factor
    bpy.context.view_layer.update()
    policy=P['geometry_policy'];source=audit_source(C,policy['max_triangles'])
    source['authored_vertices']=sum(len(o.data.vertices) for o in C.all_objects if o.type=='MESH');source['evaluated_vertices']=source['authored_vertices']
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene.render.filepath='//';bpy.context.scene['generator']='source/generate.py';bpy.context.scene['scientific_scope']=P['interpretation'];bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in C.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(flags)-available:raise RuntimeError('Missing required exporter options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    glb=audit_glb(out/'model.glb',policy['max_triangles'],policy['max_materials'],policy['max_primitives']);glb['file']='model.glb'
    b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][s][i]-e[i]) for s,e in [('min',emin),('max',emax)] for i in range(3))
    if glb['errors'] or delta>1e-5 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>policy['max_glb_bytes']:raise RuntimeError('Source/export audit failed: '+str(glb['errors']))
    import io_scene_gltf2
    anatomy={'nominal_body_diameter_m':P['body_diameter_m'],'measured_transverse_body_diameter_m':diameter*factor,'uniform_author_mm_to_m_factor':factor,'outer_body_height_m':max(v.co.z for v in OUTER.data.vertices),'large_six_rayed_stars':sum(x['group']=='large' for x in STAR_RECORDS),'medium_six_rayed_stars':sum(x['group']=='medium' for x in STAR_RECORDS),'small_four_rayed_stars':sum(x['group']=='small' for x in STAR_RECORDS),'continuous_body_wall':True,'true_upper_cavity':True,'body_material_wall_thickness_nominal_m':P['wall_thickness_mm']*factor,'attachment':'Embedded wall relief; stars are not a printable Boolean union with the body','spicule_count_scope':'Deliberate artistic simplification, not measured species-fixed census','perpendicular_rays':'Not resolved; four wall rays do not assert absence of perpendicular rays','ostia':'Microscopic ostia omitted at this stylization scale','private_reference_pixels_incorporated':False}
    dump(out/'technical.json',{'asset_id':'eiffelia','revision':'r001','source':source,'glb':glb,'source_export_bounds_delta_m':delta,'blender_version':bpy.app.version_string,'exporter_version':io_scene_gltf2.bl_info['version'],'consumer_three_version':'0.180.0','consumer_scope':'CPU parse separate; GPU and populated world untested','export_options':flags,'source_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(out/'model.blend'),'anatomy':anatomy,'scientific_scope':P['interpretation']})
    dump(out/'assembly.json',{'glb_sha256':sha(out/'model.glb'),'spicules':STAR_RECORDS,'anatomy':anatomy})
if __name__=='__main__':main()
