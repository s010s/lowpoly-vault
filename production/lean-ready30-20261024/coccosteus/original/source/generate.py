# SPDX-License-Identifier: MIT
"""Deterministic original Coccosteus living reconstruction. Run with Blender 4.3.2.
blender -b -t 2 --python source/generate.py -- --output .
Geometry is original; the reference ledger distinguishes fossil evidence from inference.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb_scale_aware import audit_glb
P=json.loads((HERE/'params.json').read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def build(gray=False):
    c=setup_scene(P['asset_id'],P['seed'])
    mats=[make_material(n, '#858A83' if gray else h,roughness=.84) for n,h in P['palette'].items()]
    def mesh(name,v,f,mi=0,slots=None):
        o=mesh_object(name,v,f,[mats[i] for i in slots] if slots else mats[mi],c)
        return o
    def loft(name,rings,n=16,slots=(0,),choose=None):
        v=[]
        for y,w,bot,top in rings:
            z=(bot+top)/2; h=(top-bot)/2
            for j in range(n):
                a=2*math.pi*j/n
                v.append((w*math.sin(a),y,z+h*math.cos(a)))
        f=[tuple(reversed(range(n)))]
        ids=[0]
        for i in range(len(rings)-1):
            for j in range(n):
                f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
                ids.append(choose(i,j,n) if choose else 0)
        f.append(tuple((len(rings)-1)*n+j for j in range(n))); ids.append(0)
        o=mesh(name,v,f,slots=slots)
        for p,k in zip(o.data.polygons,ids): p.material_index=k
        return o
    # Flexible posterior body: deliberately much longer than the compact armor.
    loft('Flexible_trunk_and_caudal_peduncle',P['body_rings'],16,(2,3),lambda i,j,n: 1 if 5<=j<=10 else 0)
    # Dark narrow articulation lies under, not outside, the head and trunk shields.
    loft('Cranio_thoracic_articulation',P['joint_rings'],16,(5,))
    loft('Compact_head_shield',P['head_rings'],16,(0,1,3),lambda i,j,n: 2 if 6<=j<=9 else 1 if j in (0,1,14,15) else 0)
    loft('Short_thoracic_shield',P['thorax_rings'],16,(0,1,3),lambda i,j,n: 2 if 6<=j<=9 else 1 if j in (0,1,14,15) else 0)
    # The small lower jaw does not introduce Dunkleosteus-like cutting blades.
    loft('Moderate_lower_jaw',P['jaw_rings'],12,(3,0),lambda i,j,n: 1 if j in (0,1,10,11) else 0)
    # A closed flattened ribbon is a shallow mouth crease, not an open black void.
    def tube(name,points,radius,mat=5,n=6):
        v=[]
        for i,p in enumerate(points):
            tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
            tangent.normalize(); u=tangent.cross(Vector((0,0,1)))
            if u.length<.001: u=tangent.cross(Vector((1,0,0)))
            u.normalize(); v2=tangent.cross(u).normalized()
            for j in range(n):
                a=2*math.pi*j/n; v.append(tuple(Vector(p)+radius*(u*math.cos(a)+v2*math.sin(a))))
        f=[tuple(reversed(range(n)))]
        for i in range(len(points)-1):
            for j in range(n): f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        f.append(tuple((len(points)-1)*n+j for j in range(n)))
        return mesh(name,v,f,mat)
    # Thin modeled surface boundaries: a few selected plate divisions, not fossil cracks.
    for sign,label in [(-1,'L'),(1,'R')]:
        tube('Mouth_crease_'+label,[(0,-.151,.073),(sign*.011,-.148,.0715),(sign*.020,-.139,.0685),(sign*.025,-.125,.066)],.00035)
        tube('Shield_boundary_'+label,[(sign*.004,-.100,.1045),(sign*.018,-.106,.100),(sign*.028,-.114,.087),(sign*.029,-.108,.074)],.00048)
    # Fin webs are closed thin sculpted volumes, conservative original outlines.
    def fin(name,outline,center,thick,axis,mat=4):
        n=len(outline); a=Vector(axis).normalized(); v=[]
        for sign in (1,-1):
            v.extend([tuple(Vector(q)+a*thick*.25*sign) for q in outline])
            v.append(tuple(Vector(center)+a*thick*.5*sign))
        f=[]
        for j in range(n):
            k=(j+1)%n
            f.extend([(n,j,k),(2*n+1,n+1+k,n+1+j),(j,n+1+j,n+1+k,k)])
        return mesh(name,v,f,mat)
    for s,label in [(-1,'L'),(1,'R')]:
        fin('Pectoral_fin_'+label,[(s*.024,-.046,.059),(s*.038,-.036,.052),(s*.055,-.011,.042),(s*.052,.009,.041),(s*.040,.018,.045),(s*.026,.003,.054),(s*.021,-.023,.059)],(s*.035,-.015,.052),.0025,(0,0,1))
        fin('Lateral_pelvic_fin_'+label,[(s*.014,.030,.061),(s*.029,.038,.057),(s*.043,.061,.048),(s*.038,.078,.047),(s*.025,.080,.051),(s*.013,.058,.058)],(s*.026,.055,.055),.0020,(0,0,1))
    fin('Dorsal_fin',[(0,.029,.101),(0,.045,.131),(0,.057,.133),(0,.078,.120),(0,.099,.099),(0,.111,.087),(0,.074,.091)],(0,.065,.108),.003,(1,0,0))
    fin('Unequal_caudal_fin',[(0,.131,.083),(0,.147,.097),(0,.174,.114),(0,.200,.124),(0,.193,.108),(0,.176,.090),(0,.163,.079),(0,.175,.069),(0,.185,.045),(0,.171,.047),(0,.152,.058),(0,.137,.068)],(0,.151,.079),.003,(1,0,0))
    # Explicit faceted lens meshes, scaled in vertex data, give distinct modest eyes.
    def lens(name,center,scale,mi):
        cx,cy,cz=center; sx,sy,sz=scale; n=12; rings=6; v=[(cx,cy,cz+sz)]
        for i in range(1,rings):
            t=math.pi*i/rings
            for j in range(n):
                a=math.tau*j/n; v.append((cx+sx*math.sin(t)*math.cos(a),cy+sy*math.sin(t)*math.sin(a),cz+sz*math.cos(t)))
        v.append((cx,cy,cz-sz)); f=[]
        for j in range(n): f.append((0,1+j,1+(j+1)%n))
        for i in range(rings-2):
            a=1+i*n;b=a+n
            for j in range(n): f.append((a+j,b+j,b+(j+1)%n,a+(j+1)%n))
        end=len(v)-1; start=1+(rings-2)*n
        for j in range(n): f.append((start+j,end,start+(j+1)%n))
        return mesh(name,v,f,mi)
    for s,label in [(-1,'L'),(1,'R')]:
        lens('Eye_iris_'+label,(s*.0258,-.134,.088),(.0020,.0053,.0053),6)
        lens('Eye_pupil_'+label,(s*.0273,-.1342,.088),(.0011,.0034,.0034),7)
    bpy.context.scene['reconstruction_scope']='Original living reconstruction; soft tissues, color and 0.35 m length are inferred.'
    bpy.context.scene['mounting_origin']='Body center projected to Z=0; swimming specimen above the ground.'
    return c

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE.parent);ap.add_argument('--gray',action='store_true');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True); c=build(args.gray)
    source=audit_source(c,P['geometry_policy']['max_triangles'])
    if source['errors']: raise RuntimeError(source['errors'])
    source['warning_review']={'Lowest Blender Z':'Intentional swimming mounting point above Z=0; no ground-contact claim.'}
    bpy.context.preferences.filepaths.save_version=0
    # Keep the editable source free of machine-local UI and output locations.
    bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'.'*1023
                    space.params.directory=b'//'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in c.all_objects: o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[c['asset_root']]
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Required exporter options missing')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    glb=audit_glb(out/'model.glb',P['geometry_policy']['max_triangles'],P['geometry_policy']['max_materials'],P['geometry_policy']['max_primitives'])
    if glb['errors']:raise RuntimeError(glb['errors'])
    glb['file']='model.glb'
    glb['warning_review']={'Lowest glTF Y':'Intentional swimming mounting point, consistent with the frozen brief.'}
    b=source['bounds_blender_m']; em=[b['min'][0],b['min'][2],-b['max'][1]]; ex=[b['max'][0],b['max'][2],-b['min'][1]]
    err=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',em),('max',ex)] for i in range(3))
    assert err<1e-6 and glb['scene_triangles']==source['triangles']
    assert (out/'model.glb').stat().st_size<=P['geometry_policy']['max_glb_bytes']
    write(out/'qa/evidence/source-export.json',{'status':'PASS','claim_scope':'Source geometry, baseline static GLB audit and coordinate-bound comparison only','blender_version':bpy.app.version_string,'export_options':options,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':err,'gray':args.gray})
if __name__=='__main__':main()
