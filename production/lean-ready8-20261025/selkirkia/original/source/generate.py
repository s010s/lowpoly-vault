# SPDX-License-Identifier: MIT
"""Original deterministic Selkirkia columbia, static living animal and its organic tube.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
All geometry is authored here. No reference pixels, external models, textures, rig or stage.
"""
from pathlib import Path
import sys,json,hashlib,argparse,math
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
P={};C=None;M={};GROUND=0;FACTOR=1

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def mm(v):return tuple(c*.001 for c in v)
def mesh(name,vs,fs,mat):return mesh_object(name,[mm(v) for v in vs],fs,mat,C)
def center(y):
    # Gentle intentional curve shared by the trunk and its enclosing tube.
    t=max(0,min(1,(y+11.5)/33))
    x=.48*math.sin(math.pi*t)-.12*math.sin(2*math.pi*t)
    z=3.0-1.0*t+.16*math.sin(math.pi*t)
    if y < -11.5:z+=.018*(-11.5-y)
    return x,z

def ring(y,r,n):
    x,z=center(y)
    return [(x+r*math.cos(2*math.pi*j/n),y,z+r*math.sin(2*math.pi*j/n)) for j in range(n)]

def join_rings(fs,a,b,n):
    for j in range(n):fs.append((a+j,a+(j+1)%n,b+(j+1)%n,b+j))

def tube():
    a=P['anatomy'];n=a['tube_radial_segments'];count=a['tube_transverse_lineations'];vs=[];fs=[];ys=[];rs=[]
    # One continuous hollow shell, not stacked toruses. Outer fine low ridges and quiet inner wall.
    for i in range(count*2+1):
        u=i/(count*2);y=-11.5+33*u
        r=2.75-1.10*u+.09*math.sin(math.pi*u)
        r+=a['tube_annulation_amplitude_mm']*(1 if i%2 else -.5)
        ys.append(y);rs.append(r);vs+=ring(y,r,n)
    nr=len(ys)
    for i in range(nr-1):join_rings(fs,i*n,(i+1)*n,n)
    outerfaces=len(fs)
    # Inner surfaces are present only for the actual wall, with no solid end caps.
    inner_count=a['tube_inner_rings']
    for i in range(inner_count):
        u=i/(inner_count-1);y=-11.5+33*u
        # Sparse smooth inner loft avoids hidden microgeometry. Thickness stays positive.
        r=2.75-1.10*u+.09*math.sin(math.pi*u)-a['tube_wall_mm']-.5*a['tube_annulation_amplitude_mm']
        vs+=ring(y,r,n)
    for i in range(inner_count-1):join_rings(fs,(nr+i)*n,(nr+i+1)*n,n)
    join_rings(fs,0,nr*n,n);join_rings(fs,(nr-1)*n,(nr+inner_count-1)*n,n)
    o=mesh('organic-annulated-tube-open-at-both-ends',vs,fs,[M['organic-tube'],M['tube-lineation']])
    # Fine light/dark flank rhythm tied to the transverse folds, not random noise.
    for i,p in enumerate(o.data.polygons):p.material_index=1 if i<outerfaces and (i//n)%2==0 else 0
    o['anatomy']='Unmineralized hollow tube; continuous inner and outer wall, annular rims at both ends, no cap discs.'
    o['wall_mm']=a['tube_wall_mm'];o['aperture_diameters_mm']=[2*(rs[0]-.12),2*(rs[-1]-.12)]
    return o

BODY_ROWS=[(-23.5,1.12),(-23.25,1.28),(-22.7,1.46),(-21.7,1.63),(-20.5,1.73),(-19.2,1.76),(-17.9,1.67),(-16.6,1.55),(-15.5,1.49),(-14.4,1.48),(-13.1,1.58),(-11.5,1.82),(-9,1.95),(-5,1.94),(0,1.77),(5,1.55),(10,1.34),(15,1.12),(19,.90),(20.9,.69),(21.1,.45)]
def radius_at(y):
    for (y0,r0),(y1,r1) in zip(BODY_ROWS,BODY_ROWS[1:]):
        if y0<=y<=y1:return r0+(r1-r0)*(y-y0)/(y1-y0)
    raise ValueError('Spine outside continuous body')

def body():
    n=P['anatomy']['body_radial_segments'];vs=[];fs=[]
    for y,r in BODY_ROWS:vs+=ring(y,r,n)
    for i in range(len(BODY_ROWS)-1):join_rings(fs,i*n,(i+1)*n,n)
    externalfaces=len(fs)
    # Re-entrant mouth vestibule: lip and sloped oral walls, not a painted circle.
    last=0
    for y,r in [(-23.46,.85),(-23.12,.72),(-22.48,.45),(-21.92,.20)]:
        start=len(vs);vs+=ring(y,r,n);join_rings(fs,last,start,n);last=start
    cen=len(vs);x,z=center(-21.82);vs.append((x,-21.82,z))
    for j in range(n):fs.append((last+j,last+(j+1)%n,cen))
    # Terminal anus retained as a tiny recessed opening. No elaborate hidden intestine.
    last=(len(BODY_ROWS)-1)*n
    for y,r in [(21.08,.20),(20.8,.12)]:
        start=len(vs);vs+=ring(y,r,n);join_rings(fs,last,start,n);last=start
    cen=len(vs);x,z=center(20.65);vs.append((x,20.65,z))
    for j in range(n):fs.append((last+j,last+(j+1)%n,cen))
    o=mesh('continuous-trunk-and-extended-introvert',vs,fs,[M['living-tissue'],M['oral-recess']])
    for i,p in enumerate(o.data.polygons):
        if i>=externalfaces+n:p.material_index=1
    o['anatomy']='Single connected worm mesh from recessed mouth through deployed introvert and hidden trunk to terminal anus.'
    o['internal_geometry']='Only shallow oral and anal recesses; no represented internal gut.'
    return o

def spine_batch(name,rows,mat,papilla=False):
    vs=[];fs=[];n=5
    # Each scalid is rooted inside the same body loft; all kept in a semantic editable group.
    for row,(y,height,base) in enumerate(rows):
        count=P['anatomy']['papillae_per_row' if papilla else 'spines_per_row']
        for k in range(count):
            theta=2*math.pi*(k+.5*(row%2))/count
            radial=Vector((math.cos(theta),0,math.sin(theta)));around=Vector((-math.sin(theta),0,math.cos(theta)));long=Vector((0,1,0))
            x,z=center(y);r=radius_at(y);p=Vector((x,y,z))+radial*(r-.10)
            # Short scalids point out and slightly toward the posterior; never long tentacles.
            drift=.08 if papilla else .25
            mid=p+radial*(height*.65)+long*(height*drift*.35)
            tip=p+radial*height+long*(height*drift)
            start=len(vs)
            for c,br in [(p,base),(mid,base*.46)]:
                for j in range(n):
                    t=2*math.pi*j/n;vs.append(tuple(c+around*math.cos(t)*br+long*math.sin(t)*br))
            ti=len(vs);vs.append(tuple(tip))
            fs.append(tuple(start+j for j in range(n-1,-1,-1)))
            join_rings(fs,start,start+n,n)
            for j in range(n):fs.append((start+n+j,start+n+(j+1)%n,ti))
    o=mesh(name,vs,fs,mat);o['root_penetration_mm']=.10;o['count_interpretation']='Simplified radial counts, not claimed fossil-exact.'
    return o

def build():
    global C,M,GROUND,FACTOR
    C=setup_scene('selkirkia',P['seed']);M={k:make_material(k,v,roughness=.86 if k.startswith('tube') or k.startswith('organic') else .78) for k,v in P['surface']['palette_srgb'].items()}
    tube();body()
    spine_batch('introvert-short-radial-scalids',[(-22.7,.54,.16),(-21.65,.66,.18),(-20.45,.69,.18),(-19.15,.65,.18),(-17.85,.58,.16),(-16.55,.45,.14)],M['scalids'])
    spine_batch('small-anterior-trunk-papillae',[(-14.5,.30,.15),(-13.20,.29,.15)],M['living-tissue'],True)
    vertices=[v for o in C.all_objects if o.type=='MESH' for v in o.data.vertices]
    ymin=min(v.co.y for v in vertices);ymax=max(v.co.y for v in vertices);GROUND=min(v.co.z for v in vertices);FACTOR=P['nominal_total_length_m']/(ymax-ymin)
    # Tube support footprint center (5 mm in construction coordinates) is the root pivot.
    for v in vertices:v.co=Vector((v.co.x*FACTOR,(v.co.y-.005)*FACTOR,(v.co.z-GROUND)*FACTOR))
    bpy.context.view_layer.update();return C

def main():
    global P
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    P=json.loads((HERE/'params.json').read_text());col=build();policy=P['geometry_policy'];source=audit_source(col,policy['max_triangles'])
    source['authored_vertices']=sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH');source['evaluated_vertices']=source['authored_vertices']
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene.render.filepath='//';bpy.context.scene['generator']='source/generate.py';bpy.context.scene['scientific_scope']=P['interpretation'];bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(flags)-available:raise RuntimeError('Missing glTF exporter options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    glb=audit_glb(out/'model.glb',policy['max_triangles'],policy['max_materials'],policy['max_primitives']);glb['file']='model.glb'
    b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][s][i]-e[i]) for s,e in [('min',emin),('max',emax)] for i in range(3))
    if glb['errors'] or delta>1e-6 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>policy['max_glb_bytes']:raise RuntimeError('Source/export audit failed: '+str(glb['errors']))
    import io_scene_gltf2
    dump(out/'technical.json',{'asset_id':'selkirkia','revision':'r001','source':source,'glb':glb,'source_export_bounds_delta_m':delta,'blender_version':bpy.app.version_string,'exporter_version':io_scene_gltf2.bl_info['version'],'consumer_three_version':'0.180.0','consumer_scope':'pin only until separate CPU parser test; GPU not tested','export_options':flags,'source_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(out/'model.blend'),'anatomical_scope':P['interpretation'],'uniform_scale_factor':FACTOR,'ground_offset_m':GROUND,'semantic_parts':'Continuous hollow organic tube with two annular end rims; single continuous trunk and introvert with recessed mouth and terminal anus; short radial scalids; small anterior trunk papillae. No eyes, legs or long tentacles.'})
if __name__=='__main__':main()
