#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Tenontosaurus living reconstruction, pinned Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output .
Only adjacent params.json and the vendored helper files are project dependencies.
"""
import argparse,hashlib,json,math,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene,make_material,mesh_object,ground_asset,audit_source
from qa_glb import audit_glb

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

class Profiles:
    """Closed profile components; semantic vertex groups remain editable."""
    def __init__(self,name,mats): self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[];self.groups={}
    def add(self,name,vs,fs,mi=None):
        start=len(self.v);self.v.extend(vs);self.f.extend(tuple(start+i for i in f) for f in fs)
        self.mi.extend(mi if mi is not None else [0]*len(fs));self.groups[name]=list(range(start,len(self.v)))
    def axial(self,name,sections,n=20,palette=False):
        v=[];f=[];mi=[]
        for y,z,rx,ru,rd in sections:
            for j in range(n):
                a=2*math.pi*j/n;s=math.sin(a);v.append((rx*math.cos(a),y,z+(ru if s>=0 else rd)*s))
        for i in range(len(sections)-1):
            for j in range(n):
                f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
                s=math.sin(2*math.pi*(j+.5)/n);mi.append(1 if palette and s>.66 else 2 if palette and s<-.50 else 0)
        for k,rev in [(0,True),(len(sections)-1,False)]:
            c=len(v);v.append((0,sections[k][0],sections[k][1]))
            for j in range(n):f.append((c,k*n+(j+1)%n,k*n+j) if rev else (c,k*n+j,k*n+(j+1)%n));mi.append(0)
        self.add(name,v,f,mi)
    def tube(self,name,nodes,n=12,frame=(1,0,0)):
        p=[Vector(a[:3]) for a in nodes];v=[];f=[];ref=Vector(frame)
        for i,a in enumerate(nodes):
            t=(p[min(i+1,len(p)-1)]-p[max(0,i-1)]).normalized();u=ref-t*ref.dot(t)
            if u.length<.001:u=Vector((0,0,1))-t*t.z
            u.normalize();w=t.cross(u).normalized()
            for j in range(n):
                ang=2*math.pi*j/n;v.append(tuple(p[i]+u*a[3]*math.cos(ang)+w*a[4]*math.sin(ang)))
        for i in range(len(nodes)-1):
            for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        for k,rev in [(0,True),(len(nodes)-1,False)]:
            c=len(v);v.append(tuple(p[k]))
            for j in range(n):f.append((c,k*n+(j+1)%n,k*n+j) if rev else (c,k*n+j,k*n+(j+1)%n))
        self.add(name,v,f)
    def lens(self,name,c,ry,rz,d,sg,n=12):
        x,y,z=c;v=[(x,y+ry*math.cos(2*math.pi*j/n),z+rz*math.sin(2*math.pi*j/n)) for j in range(n)];v.extend([(x+sg*d,y,z),(x-sg*.008,y,z)]);f=[]
        for j in range(n):f.extend([(j,(j+1)%n,n),((j+1)%n,j,n+1)])
        self.add(name,v,f)
    def finish(self,col):
        ob=mesh_object(self.name,self.v,self.f,self.mats,col)
        for poly,idx in zip(ob.data.polygons,self.mi):poly.material_index=idx
        for name,ids in self.groups.items():ob.vertex_groups.new(name=name).add(ids,1,'REPLACE')
        ob['construction']='Closed deliberate polygon profiles; semantic anatomical vertex groups. Soft-tissue joins are intentional overlapping envelopes.'
        return ob

def build(p):
    col=setup_scene(p['asset_id'],p['seed']);mat={k:make_material('Tenontosaurus_'+k,v,roughness=.87) for k,v in p['palette'].items()}
    body=Profiles('Continuous_Head_Neck_DeepTrunk_LongTail',[mat['skin'],mat['dorsal'],mat['ventral']])
    # Continuous axial topology: low elongated skull, modest neck, deep ribs,
    # muscular hips and long high proximal caudal envelope. Exact widths inferred.
    body.axial('WholeAxialProfile',[
        (-2.085,1.740,.047,.038,.037),(-2.020,1.760,.093,.062,.054),
        (-1.900,1.790,.118,.096,.074),(-1.780,1.820,.135,.133,.099),
        (-1.660,1.829,.151,.154,.123),(-1.550,1.800,.131,.129,.111),
        (-1.445,1.725,.112,.142,.137),(-1.345,1.620,.142,.183,.180),
        (-1.230,1.500,.210,.260,.253),(-1.100,1.425,.292,.330,.341),
        (-.900,1.405,.382,.420,.475),(-.650,1.410,.469,.484,.594),
        (-.350,1.420,.531,.522,.681),(-.030,1.435,.550,.530,.713),
        (.260,1.460,.523,.505,.668),(.510,1.465,.468,.471,.577),
        (.740,1.447,.417,.450,.503),(1.010,1.420,.375,.431,.466),
        (1.300,1.382,.337,.401,.427),(1.620,1.330,.292,.359,.380),
        (1.980,1.271,.246,.310,.323),(2.340,1.211,.196,.255,.266),
        (2.710,1.154,.149,.198,.207),(3.080,1.118,.112,.150,.155),
        (3.460,1.108,.078,.108,.111),(3.830,1.130,.052,.074,.076),
        (4.160,1.172,.034,.048,.050),(4.460,1.224,.020,.029,.029),
        (4.730,1.279,.010,.015,.015),(4.900,1.315,.002,.003,.003)
    ],n=20,palette=True)
    hind=Profiles('Powerful_Hindlimbs_FourToedFeet',[mat['skin']]);fore=Profiles('Short_Forelimbs_FiveDigitHands',[mat['skin']])
    keratin=Profiles('Beak_And_BluntDigitTips',[mat['keratin']]);iris=Profiles('EyeIrises',[mat['iris']]);dark=Profiles('Eyes_Nares_ClosedMouth',[mat['dark']])
    keratin.axial('ShortBeak',[
        (-2.100,1.739,.042,.034,.031),(-2.070,1.742,.063,.044,.040),(-2.015,1.757,.092,.059,.052)
    ],n=12)
    for sg,label,step in [(1,'Left',-.050),(-1,'Right',.050)]:
        def mir(a):return [(sg*x,y,z,r1,r2) for x,y,z,r1,r2 in a]
        # Femur aims forward, tibia back; metatarsals descend to robust spread toes.
        hind.tube(label+'_Hindlimb',mir([
            (.360,.280+step,1.460,.232,.270),(.480,.175+step,1.280,.269,.315),
            (.520,-.035+step,1.030,.235,.270),(.530,-.160+step,.800,.169,.180),
            (.525,-.060+step,.610,.126,.136),(.500,.130+step,.390,.090,.100),
            (.488,.190+step,.255,.081,.085),(.490,.105+step,.143,.109,.092),
            (.490,-.015+step,.105,.156,.075)
        ]),n=12)
        for digit,dx,ln,spread,rad in [('II',-.100,.240,-.045,.060),('III',0,.310,.010,.071),('IV',.100,.220,.056,.056)]:
            x=.490+dx;y=-.015+step-ln
            hind.tube(label+'_HindDigit'+digit,mir([
                (.490+dx*.65,.015+step,.105,rad*1.13,.068),(x,-.100+step,.075,rad,.055),
                (x+spread*.65,y+.060,.060,rad*.80,.046),(x+spread,y,.052,rad*.61,.037)
            ]),n=8)
            keratin.tube(label+'_HindTip'+digit,mir([
                (x+spread*.85,y+.020,.057,rad*.65,.040),(x+spread,y-.050,.040,rad*.43,.027),
                (x+spread*1.03,y-.085,.020,.008,.008)
            ]),n=8)
        hind.tube(label+'_ReducedHindDigitI',mir([
            (.405,.070+step,.145,.048,.052),(.347,-.030+step,.100,.044,.044),(.325,-.155+step,.072,.032,.030)
        ]),n=8)
        keratin.tube(label+'_HindTipI',mir([(.327,-.140+step,.073,.033,.031),(.312,-.205+step,.051,.022,.020),(.303,-.233+step,.038,.007,.007)]),n=7)
        # Short forelimbs descend from the lower shoulder, not human pronated arms.
        fore.tube(label+'_Forelimb',mir([
            (.267,-1.062,1.430,.123,.155),(.353,-1.070,1.200,.142,.162),
            (.401,-.955,.960,.119,.133),(.423,-.912,.795,.095,.106),
            (.437,-1.010,.575,.079,.085),(.449,-1.105,.340,.064,.070),
            (.456,-1.155,.170,.069,.074),(.458,-1.198,.100,.096,.065)
        ]),n=12)
        # Five short manual digits, a compact support hand without a thumb spike.
        for digit,dx,ln in [(1,-.090,.095),(2,-.045,.145),(3,0,.165),(4,.043,.140),(5,.081,.100)]:
            x=.458+dx;y=-1.198-ln
            fore.tube(label+'_ManualDigit'+str(digit),mir([
                (.458+dx*.65,-1.200,.103,.034,.043),(x,-1.250,.069,.031,.034),
                (x+dx*.18,y,.051,.024,.025)
            ]),n=8)
            if digit<=3:keratin.tube(label+'_ManualTip'+str(digit),mir([
                (x+dx*.15,y+.012,.054,.025,.025),(x+dx*.20,y-.033,.034,.017,.016),(x+dx*.21,y-.047,.023,.006,.005)
            ]),n=7)
        iris.lens(label+'_Eye',(sg*.142,-1.666,1.877),.042,.038,.015,sg,n=14)
        dark.lens(label+'_Pupil',(sg*.158,-1.671,1.878),.020,.023,.005,sg,n=12)
        dark.lens(label+'_Naris',(sg*.098,-1.986,1.788),.014,.008,.004,sg,n=8)
        dark.tube(label+'_MouthLine',mir([
            (.055,-2.070,1.730,.002,.002),(.089,-2.020,1.740,.002,.002),
            (.107,-1.900,1.755,.002,.002),(.115,-1.780,1.765,.002,.002),(.135,-1.660,1.770,.002,.002)
        ]),n=6,frame=(0,0,1))
    for builder in (body,hind,fore,keratin,iris,dark):builder.finish(col)
    shift=ground_asset(col,center_xy=False)
    contacts=[o.matrix_world@v.co for o in col.all_objects if o.type=='MESH' for v in o.data.vertices if (o.matrix_world@v.co).z<.040]
    shift[1]=-(min(v.y for v in contacts)+max(v.y for v in contacts))/2
    for o in col.all_objects:
        if o.type=='MESH':o.location.y+=shift[1]
    bpy.context.view_layer.update();root=bpy.data.objects[p['asset_id']]
    root['representation']='living-reconstruction';root['scale_basis']='7 m genus-level estimate, not individual fossil measurement'
    root['scientific_limits']='Artistic composite of separate April, MOR partial and OMNH58340 references; width, soft tissue, colour and pose inferred'
    root['diagnostic']='Deep ribcage and prolonged muscular tail base; no crest or thumb spike'
    return col,shift

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE.parent)
    opt=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);out=opt.output.resolve();out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text());assert bpy.app.version_string==p['blender_version']
    col,shift=build(p);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    audit=audit_source(col,p['max_triangles']);assert not audit['errors'],audit['errors']
    bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'_'*1023;space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),check_existing=False)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[p['asset_id']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={a.identifier for a in bpy.ops.export_scene.gltf.get_rna_type().properties};assert not set(flags)-available
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags);os.chdir(out)
    glb=audit_glb(Path('model.glb'),p['max_triangles'],p['max_materials'],p['max_primitives']);assert not glb['errors'],glb['errors'];assert glb['bytes']<=p['max_glb_bytes']
    b=audit['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][a][i]-expected[a][i]) for a in ['min','max'] for i in range(3));assert delta<.0001 and audit['triangles']==glb['scene_triangles']
    report={'status':'PASS','scope':'Source geometry and emitted static GLB only, not independent visual or target GPU acceptance','glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'blender_version':bpy.app.version_string,'gltf_exporter_version':'4.3.47','exporter_required_flags_probed':True,'export_options':flags,'source':audit,'glb':glb,'source_export_bounds_error_m':delta,'ground_translation_m':shift,'profile':'Static, uncompressed, texture-free palette-only','source_components':'Six editable mesh objects with semantic vertex groups','scale_note':'7.0 m nose-to-tail horizontal extent, genus estimate rather than a single specimen measurement'}
    write(out/'qa/evidence/source-export.json',report);print(json.dumps({'status':'BUILT','glb_sha256':report['glb_sha256'],'triangles':glb['scene_triangles'],'bytes':glb['bytes']}))
if __name__=='__main__':main()
