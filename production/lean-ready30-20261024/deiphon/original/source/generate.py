# SPDX-License-Identifier: MIT
"""Original Deiphon barrandei living reconstruction, deterministic Blender 4.3.2.
Run: blender -b -t 2 --python source/generate.py -- --output-dir OUTPUT
Only this source directory and its declared deps are needed to regenerate.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import qa_glb_scale_aware
sys.modules['qa_glb']=qa_glb_scale_aware
from asset_common import setup_scene, make_material, mesh_object, audit_source, ground_asset


def h(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

class Geometry:
    def __init__(self): self.v=[]; self.f=[]
    def add(self,vertices,faces):
        n=len(self.v);self.v+=vertices;self.f += [tuple(i+n for i in face) for face in faces]
    def tube(self,points,widths,heights=None,sides=8):
        pts=[Vector(p) for p in points];heights=heights or widths;v=[];f=[]
        for i,(p,w,ht) in enumerate(zip(pts,widths,heights)):
            t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
            side=t.cross(Vector((0,0,1))).normalized()
            if side.length<0.1: side=Vector((1,0,0))
            up=side.cross(t).normalized()
            for j in range(sides):
                a=2*math.pi*j/sides;v.append(tuple(p+side*w*math.cos(a)+up*ht*math.sin(a)))
        for i in range(len(pts)-1):
            for j in range(sides):
                a=i*sides+j;b=i*sides+(j+1)%sides
                f.append((a,b,b+sides,a+sides))
        f.append(tuple(range(sides-1,-1,-1)));f.append(tuple((len(pts)-1)*sides+j for j in range(sides)))
        self.add(v,f)
    def ovoid(self,center,radii,rings=12,sides=24,phase=0):
        cx,cy,cz=center;rx,ry,rz=radii;v=[(cx,cy,cz-rz)];f=[]
        for i in range(1,rings):
            phi=-math.pi/2+math.pi*i/rings
            for j in range(sides):
                a=2*math.pi*j/sides+phase
                # A full rounded glabella, gently broader forward, not a flat shield.
                xx=rx*math.cos(phi)*math.cos(a);yy=ry*math.cos(phi)*math.sin(a)
                v.append((cx+xx,cy+yy,cz+rz*math.sin(phi)))
        top=len(v);v.append((cx,cy,cz+rz))
        for j in range(sides): f.append((0,1+(j+1)%sides,1+j))
        for i in range(rings-2):
            for j in range(sides):
                a=1+i*sides+j;b=1+i*sides+(j+1)%sides
                f.append((a,b,b+sides,a+sides))
        base=1+(rings-2)*sides
        for j in range(sides):f.append((base+j,base+(j+1)%sides,top))
        self.add(v,f)
    def obj(self,name,material,collection):
        return mesh_object(name,self.v,self.f,material,collection)


def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=HERE.parent);p.add_argument('--gray',action='store_true');a=p.parse_args(args)
    out=a.output_dir;out.mkdir(parents=True,exist_ok=True);cfg=json.loads((HERE/'params.json').read_text())
    col=setup_scene('deiphon',cfg['seed']);m={k:make_material('deiphon-'+k, '#93908B' if a.gray else color,roughness=0.82 if k!='eye' else 0.6) for k,color in cfg['palette'].items()}
    g=Geometry();g.ovoid((0,-0.0093,0.0054),(0.0055,0.0056,0.0047),cfg['glabella_sections'],cfg['glabella_radial_sides']);g.obj('inflated-spherical-glabella',m['shell'],col)
    # Separate cheek foundations remain small, leaving an unmistakable balloon-like glabella.
    cheek=Geometry();genal=Geometry();eyes=Geometry();collar=Geometry()
    for s in (-1,1):
        cheek.tube([(s*.0035,-.007,.0035),(s*.0060,-.0067,.0031),(s*.0074,-.0048,.0026)], [.0014,.00125,.0009],[.001,.0009,.00065],8)
        genal.tube([(s*.0057,-.0067,.0032),(s*.008,-.0048,.0027),(s*.0104,-.0008,.0021),(s*.0118,.0042,.0017),(s*.0117,.0095,.0012)], [.0012,.00105,.00072,.00046,.00011],[.00075,.00065,.00044,.00029,.00009],8)
        eyes.ovoid((s*.0054,-.0082,.0057),(.00078,.0011,.00075),6,10)
    cheek.obj('small-free-cheeks',m['pleura'],col);genal.obj('paired-sweeping-genal-spines',m['shell'],col);eyes.obj('subordinate-lateral-eyes',m['eye'],col)
    collar.tube([(-.0026,-.0039,.0035),(0,-.0037,.0040),(.0026,-.0039,.0035)],[.0006,.00075,.0006],[.0005,.00065,.0005],8);collar.obj('occipital-neck-ring',m['ridge'],col)
    axial=Geometry();pleura=Geometry();sternites=Geometry();legs=Geometry()
    for i in range(cfg['trunk_segments']):
        t=i/10;y=-.0023+i*.00138;w=.00225-.00062*t;z=.0032-.00065*t
        # Individually arched annuli and real spaces between the slender swept pleurae.
        axial.ovoid((0,y,z),(w,.00079,.0008),6,12,math.pi/12)
        for s in (-1,1):
            reach=.0097-.0016*t**2
            pleura.tube([(s*w*.82,y,z-.00012),(s*.0044,y+.00013,z-.00020),(s*(reach*.82),y+.00075,z-.00043),(s*reach,y+.0020,z-.00080)], [.00058,.00061,.00047,.00010],[.00040,.00039,.00029,.00008],8)
            if not a.gray and i<9:
                # Inferred small walking limbs below the exoskeletal spines, never substituted for them.
                ly=y+.0001
                legs.tube([(s*.0012,ly,.0021),(s*.0030,ly+.00020,.0014),(s*.0041,ly+.00060,.00055),(s*.00455,ly+.0009,.00027)],[.00028,.00025,.00019,.00011],[.00023,.00020,.00016,.00010],6)
        if not a.gray:
            sternites.ovoid((0,y,.0019),(w*.85,.00063,.00045),4,10)
    axial.obj('narrow-segmented-axial-trunk',m['ridge'],col);pleura.obj('twenty-two-separated-pleural-spines',m['pleura'],col)
    posterior=Geometry()
    for s in (-1,1):
        posterior.tube([(s*.0010,.0124,.0025),(s*.0034,.0142,.0020),(s*.0056,.0162,.0013),(s*.0061,.0180,.0007)],[.0010,.0010,.00062,.00011],[.00055,.00056,.0004,.00009],8)
    posterior.obj('paired-pygidial-rear-extensions',m['shell'],col)
    if not a.gray:
        sternites.obj('inferred-ventral-sternites',m['ventral'],col);legs.obj('inferred-short-ventral-limbs',m['limb'],col)
        antennae=Geometry()
        for s in (-1,1):
            antennae.tube([(s*.0018,-.0125,.0015),(s*.0027,-.0146,.0011),(s*.0040,-.0164,.0014),(s*.0052,-.0170,.0019)],[.00027,.00022,.00016,.00010],[.00023,.00020,.00014,.00009],6)
        antennae.obj('inferred-paired-antennae',m['antenna'],col)
    shift=ground_asset(col,False);root=bpy.data.objects[col['asset_root']]
    root['taxon']='Deiphon barrandei';root['representation']='living-reconstruction';root['scientific_limits']='Ventral limbs, antennae, color, posture and thickness are inferred. Approximate 3.5 cm caption scale; no feeding or buoyancy claim.'
    source=audit_source(col,max_triangles=18000)
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath='//preview.png'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
                    space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=root
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Missing required export options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    audit=qa_glb_scale_aware.audit_glb(out/'model.glb',max_triangles=18000,max_materials=8,max_primitives=36)
    if audit['errors']:raise RuntimeError(audit['errors'])
    audit['file']='model.glb'
    low=source['bounds_blender_m']['min'];high=source['bounds_blender_m']['max']
    expected={'min':[low[0],low[2],-high[1]],'max':[high[0],high[2],-low[1]]}
    delta=max(abs(audit['bounds_m'][k][i]-expected[k][i]) for k in ('min','max') for i in range(3))
    if delta>1e-6 or audit['scene_triangles']!=source['triangles']:raise RuntimeError('Source/export mismatch')
    if audit['bytes']>2000000:raise RuntimeError('GLB byte budget exceeded')
    write(out/'qa/evidence/source-build.json',{'schema_version':1,'status':'PASS','claim_scope':'Deterministic source build and static export only; no independent visual or runtime acceptance.','asset_id':'deiphon','revision':'r001','blender_version':bpy.app.version_string,'generator_sha256':h(HERE/'generate.py'),'params_sha256':h(HERE/'params.json'),'blend_sha256':h(out/'model.blend'),'glb_sha256':h(out/'model.glb'),'source':source,'export':audit,'source_export_bounds_error_m':delta,'export_options':options,'ground_shift_m':shift,'gray_stage':a.gray})

if __name__=='__main__':main()
