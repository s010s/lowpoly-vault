# SPDX-License-Identifier: MIT
"""Original, deterministic genus-level Deinotherium living reconstruction.
Run: blender -b -t 2 --python source/generate.py -- --output-dir build --params source/params.json
The two downturned tusks belong to the mandible, never the upper maxilla.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent / 'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')


def tube(name, stations, mat, collection, sides=12):
    """Closed swept ring mesh: stations are (x,y,z, lateral_radius, in-plane_radius)."""
    verts=[]; faces=[]
    for i,s in enumerate(stations):
        c=Vector(s[:3]); prev=Vector(stations[max(0,i-1)][:3]); nxt=Vector(stations[min(len(stations)-1,i+1)][:3])
        tangent=(nxt-prev).normalized()
        if name.endswith('limb') and i==len(stations)-1: tangent=Vector((0,0,-1))
        a=Vector((1,0,0)); a=(a-a.dot(tangent)*tangent).normalized()
        b=tangent.cross(a).normalized()
        for j in range(sides):
            angle=2*math.pi*j/sides
            verts.append(tuple(c+a*(s[3]*math.cos(angle))+b*(s[4]*math.sin(angle))))
    for i in range(len(stations)-1):
        for j in range(sides):
            a=i*sides+j; b=i*sides+(j+1)%sides; c=(i+1)*sides+(j+1)%sides; d=(i+1)*sides+j
            # Alternating diagonal gives a deliberate faceted surface.
            faces.extend([(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)])
    verts.extend([tuple(stations[0][:3]),tuple(stations[-1][:3])]); start=len(verts)-2; end=len(verts)-1
    for j in range(sides):
        faces.append((start,j,(j+1)%sides)); a=(len(stations)-1)*sides; faces.append((end,a+(j+1)%sides,a+j))
    return mesh_object(name,verts,faces,mat,collection)


def torso(name, rings, materials, collection, sides=20):
    verts=[]; faces=[]
    for y,z,w,h in rings:
        for j in range(sides):
            t=2*math.pi*j/sides
            # Lower barrel slightly flatter than dorsal arc, not a sphere primitive.
            s=math.sin(t); zz=z+h*(s if s>=0 else s*.89)
            verts.append((w*math.cos(t),y,zz))
    for i in range(len(rings)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;c=(i+1)*sides+(j+1)%sides;d=(i+1)*sides+j
            faces.extend([(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)])
    verts.extend([(0,rings[0][0],rings[0][1]),(0,rings[-1][0],rings[-1][1])]); a=len(verts)-2;b=len(verts)-1
    for j in range(sides): faces.extend([(a,j,(j+1)%sides),(b,(len(rings)-1)*sides+(j+1)%sides,(len(rings)-1)*sides+j)])
    obj=mesh_object(name,verts,faces,materials,collection)
    for poly in obj.data.polygons:
        z=sum(obj.data.vertices[n].co.z for n in poly.vertices)/len(poly.vertices)
        poly.material_index=1 if z<1.95 else 2 if z>3.15 and poly.index%7==0 else 0
    return obj


def ellipsoid(name, center, radii, material, collection, n=10, rings=6):
    v=[(center[0],center[1],center[2]+radii[2])]; f=[]
    for k in range(1,rings):
        t=math.pi*k/rings
        for j in range(n):
            a=2*math.pi*j/n
            v.append((center[0]+radii[0]*math.sin(t)*math.cos(a),center[1]+radii[1]*math.sin(t)*math.sin(a),center[2]+radii[2]*math.cos(t)))
    v.append((center[0],center[1],center[2]-radii[2])); bottom=len(v)-1
    for j in range(n): f.extend([(0,1+j,1+(j+1)%n),(bottom,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j)])
    for k in range(rings-2):
        for j in range(n):
            a=1+k*n+j;b=1+k*n+(j+1)%n;c=1+(k+1)*n+(j+1)%n;d=1+(k+1)*n+j
            f.append((a,b,c,d))
    return mesh_object(name,v,f,material,collection)


def ear(side, materials, collection):
    # A thick, modest fan; size and outline are soft-tissue estimates.
    yz=[(-1.88,3.53),(-1.65,3.52),(-1.44,3.36),(-1.38,3.08),(-1.50,2.85),(-1.73,2.72),(-1.94,2.80),(-2.06,3.04),(-2.05,3.30)]
    v=[(side*(.56+(.33 if 1<=i<=5 else .12)),y,z) for i,(y,z) in enumerate(yz)]
    v += [(side*(abs(x)-.075),y+.04,z) for x,y,z in v]
    v.extend([(side*.91,-1.73,3.13),(side*.73,-1.69,3.12)])
    n=len(yz); f=[]
    for i in range(n): f.extend([(2*n,i,(i+1)%n),(2*n+1,n+(i+1)%n,n+i),(i,n+i,n+(i+1)%n,(i+1)%n)])
    o=mesh_object(('left' if side>0 else 'right')+'-ear-estimate',v,f,materials,collection)
    for p in o.data.polygons:p.material_index=1 if p.index%3==0 and p.index<18 else 0
    return o


def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--params',type=Path,default=Path(__file__).with_name('params.json'));a=ap.parse_args(argv)
    params=json.loads(a.params.read_text());out=a.output_dir;out.mkdir(parents=True,exist_ok=True)
    col=setup_scene('deinotherium',params['seed']); bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    skin=make_material('warm-gray-skin','#77766D',.88); under=make_material('shadow-skin','#6A6B63',.92); lit=make_material('dorsal-skin','#7D7C72',.88)
    creases=make_material('soft-folds','#5E605A',.92); ivory=make_material('mandibular-ivory','#D2C4A4',.7); eye=make_material('dark-eyes','#252B29',.4); nail=make_material('muted-toenails','#8B8776',.91)
    torso('continuous-torso-neck-long-skull',params['torso_rings'],[skin,under,lit],col)
    tube('downturned-mandible',[(0,-1.89,2.97,.40,.28),(0,-2.13,2.78,.47,.23),(0,-2.38,2.65,.43,.20),(0,-2.62,2.53,.37,.21),(0,-2.72,2.33,.29,.19),(0,-2.69,2.23,.25,.12)],skin,col,16)
    tube('nasal-trunk-artistic-estimate',params['trunk_stations'],[skin],col,14)
    for side in (-1,1):
        label='left' if side>0 else 'right'
        tube(label+'-mandibular-tusk',[(side*x,y,z,r,r*.92) for x,y,z,r in params['tusk_stations']],ivory,col,12)
        ear(side,[skin,under],col)
        ellipsoid(label+'-orbital-skin',(side*.535,-2.30,3.25),(.062,.145,.103),creases,col)
        ellipsoid(label+'-eye',(side*.579,-2.34,3.255),(.029,.057,.043),eye,col)
        # Broad shoulder-to-ankle transition and padded soles; four distinct contacts.
        for fore in (True,False):
            y=-1.10 if fore else 1.13
            x=side*(.64 if fore else .67)
            stations=[(x,y,2.84,.37,.43),(x+side*.025,y-.02,2.26,.35,.36),(x+side*.04,y+.02,1.69,.26,.29),(x+side*.045,y-.045,1.12,.245,.25),(x+side*.05,y-.085,.53,.26,.25),(x+side*.055,y-.11,.18,.33,.34),(x+side*.055,y-.12,0,.34,.35)]
            tube(label+('-forelimb' if fore else '-hindlimb'),stations,skin,col,14)
            for k in (-1,0,1):
                ellipsoid(label+('-front' if fore else '-rear')+'-nail-'+str(k+2),(x+side*.055+k*.16,y-.426,.118),(.075,.032,.09),nail,col,8,4)
    tube('small-tapered-tail',[(0,1.68,2.72,.14,.13),(.06,1.97,2.45,.11,.10),(.12,2.12,2.11,.075,.075),(.14,2.20,1.76,.045,.052),(.17,2.25,1.50,.055,.065),(.18,2.27,1.36,.02,.025)],under,col,10)
    # Keep the identity root at the center of the four ground-contact soles.
    for obj in col.all_objects:
        if obj.type=='MESH':
            for vertex in obj.data.vertices: vertex.co.y-=params['floor_contact_center_y']
    bpy.context.view_layer.update()
    source=audit_source(col,max_triangles=params['budgets']['max_triangles'])
    if source['errors']:raise RuntimeError(source['errors'])
    root=bpy.data.objects['deinotherium'];root['representation']='living-reconstruction';root['reconstruction_scope']='Deinotherium sp.; genus-level artistic reconstruction';root['soft_tissue']='Trunk, ears, skin, color, pose and dimensions are artistic estimates.'
    bpy.context.preferences.filepaths.save_version=0
    # Clear machine-specific default presentation paths through Blender's API.
    bpy.context.scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'/'*1023
                    space.params.directory=b'//'
                    space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=root
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties};assert set(flags)<=available
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    q=audit_glb(out/'model.glb',max_triangles=params['budgets']['max_triangles'],max_materials=params['budgets']['max_materials'],max_primitives=params['budgets']['max_primitives'])
    if q['errors']:raise RuntimeError(q['errors'])
    q['file']='model.glb'
    assert (out/'model.glb').stat().st_size<=params['budgets']['max_glb_bytes']
    write(out/'build-report.json',{'check':'source-and-static-export','status':'PASS','blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'generator_sha256':sha(__file__),'params_sha256':sha(a.params),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'export_flags':flags,'source':source,'glb':q,'limitations':'Numeric source/export audit only; not independent visual approval, browser GPU, populated-scene or deployment evidence.'})

if __name__=='__main__':main()
