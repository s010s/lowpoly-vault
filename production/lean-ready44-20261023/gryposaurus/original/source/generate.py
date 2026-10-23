#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Gryposaurus living reconstruction, pinned Blender 4.3.2.
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
    col=setup_scene(p['asset_id'],p['seed']);mat={k:make_material('Gryposaurus_'+k,v,roughness=.90) for k,v in p['palette'].items()}
    body=Profiles('Axial_NasalArch_DeepHead_Neck_Trunk_Tail',[mat['skin'],mat['dorsal'],mat['ventral']])
    # Nose to tail: high nasal arch is forward of the orbits and flows directly
    # into the steep anterior snout. No separate crown, tube, helmet or horn.
    sections=[
      (-4.16,3.090,.280,.090,.100),(-4.06,3.190,.350,.290,.230),
      (-3.94,3.320,.390,.560,.370),(-3.78,3.450,.418,.740,.510),
      (-3.66,3.485,.425,.800,.525),(-3.57,3.510,.430,.790,.540),
      (-3.47,3.515,.443,.765,.530),(-3.36,3.520,.458,.655,.520),
      (-3.14,3.520,.492,.535,.490),(-2.94,3.520,.510,.490,.455),
      (-2.73,3.505,.480,.455,.390),(-2.54,3.430,.397,.435,.335),
      (-2.37,3.210,.350,.445,.365),(-2.18,2.950,.420,.560,.510),
      (-1.94,2.690,.590,.730,.610),(-1.63,2.500,.810,.940,.765),
      (-1.25,2.410,1.000,1.120,.980),(-.80,2.400,1.120,1.250,1.180),
      (-.30,2.440,1.180,1.300,1.270),(.20,2.510,1.150,1.290,1.200),
      (.70,2.570,1.020,1.220,1.045),(1.15,2.600,.870,1.110,.900),
      (1.60,2.560,.750,.990,.800),(2.10,2.470,.650,.850,.690),
      (2.65,2.350,.540,.715,.590),(3.25,2.220,.425,.580,.490),
      (3.85,2.120,.325,.455,.390),(4.45,2.060,.247,.345,.305),
      (5.05,2.050,.181,.255,.230),(5.65,2.090,.125,.185,.165),
      (6.20,2.160,.085,.125,.115),(6.72,2.250,.051,.078,.072),
      (7.15,2.340,.027,.045,.042),(7.53,2.410,.013,.022,.020),
      (7.80,2.460,.002,.004,.004)]
    body.axial('ContinuousAnatomicalProfile',sections,n=24,palette=True)
    hind=Profiles('Muscular_Hindlimbs_TridactylFeet',[mat['skin']]);fore=Profiles('Short_Forelimbs_SupportHands',[mat['skin']])
    keratin=Profiles('Beak_And_Unguals',[mat['keratin']]);iris=Profiles('EyeIrises',[mat['iris']]);dark=Profiles('Eyes_Nares_ClosedMouth',[mat['dark']])
    keratin.axial('SteepDownturnedBeak',[
      (-4.20,3.080,.260,.075,.085),(-4.15,3.095,.315,.115,.125),
      (-4.09,3.155,.349,.200,.205),(-4.025,3.213,.359,.238,.220)],n=16)
    def surf(y,z):
      for a,b in zip(sections,sections[1:]):
        if a[0]<=y<=b[0]:
          t=(y-a[0])/(b[0]-a[0]);cz=a[1]*(1-t)+b[1]*t;rx=a[2]*(1-t)+b[2]*t;rz=(a[3]*(1-t)+b[3]*t) if z>=cz else (a[4]*(1-t)+b[4]*t)
          # Polygonal ring surface, rather than a circumscribed ellipse.
          v=max(-.999,min(.999,(z-cz)/rz));ang=math.asin(v);step=2*math.pi/24;k=math.floor(ang/step);z0=math.sin(k*step);z1=math.sin((k+1)*step);u=(v-z0)/(z1-z0)
          return rx*(math.cos(k*step)*(1-u)+math.cos((k+1)*step)*u)
      raise ValueError('Head detail outside profile')
    for sg,label in [(1,'Left'),(-1,'Right')]:
      def mir(a):return [(sg*x,y,z,r1,r2) for x,y,z,r1,r2 in a]
      hind.tube(label+'_Hindlimb',mir([
        (.730,.650,2.700,.420,.500),(.980,.430,2.360,.470,.520),
        (1.115,.090,1.950,.390,.460),(1.155,-.140,1.560,.270,.310),
        (1.170,.040,1.190,.200,.225),(1.140,.390,.760,.135,.145),
        (1.135,.490,.460,.117,.128),(1.140,.330,.250,.160,.145),
        (1.150,.190,.165,.225,.105)]),n=14)
      for digit,dx,ln,spread,rad in [('II',-.145,.400,-.060,.091),('III',0,.510,.012,.108),('IV',.145,.385,.075,.087)]:
        x=1.150+dx;y=.190-ln
        hind.tube(label+'_HindDigit'+digit,mir([
          (1.150+dx*.60,.210,.165,rad*1.20,.095),(x,.020,.110,rad,.078),
          (x+spread*.60,y+.090,.080,rad*.85,.064),(x+spread,y,.065,rad*.65,.045)],),n=10)
        keratin.tube(label+'_HindUngual'+digit,mir([
          (x+spread*.85,y+.025,.071,rad*.70,.051),(x+spread,y-.070,.044,rad*.57,.036),
          (x+spread,y-.112,.029,rad*.23,.018)]),n=8)
      fore.tube(label+'_Forelimb',mir([
        (.590,-1.650,2.640,.235,.290),(.780,-1.700,2.300,.275,.300),
        (.895,-1.510,1.910,.235,.245),(.930,-1.420,1.620,.180,.192),
        (.948,-1.590,1.230,.139,.151),(.963,-1.750,.800,.105,.120),
        (.970,-1.820,.450,.100,.114),(.980,-1.850,.220,.137,.133),
        (.980,-1.920,.110,.158,.090)],),n=14)
      # A compact hadrosaur support mitten, not a grasping hand or thumb spike.
      for digit,dx,ln in [(2,-.085,.170),(3,0,.195),(4,.082,.164)]:
        x=.980+dx;y=-1.920-ln
        fore.tube(label+'_SupportDigit'+str(digit),mir([
          (.980+dx*.70,-1.920,.116,.061,.071),(x,-2.000,.075,.058,.051),(x,y,.055,.052,.038)],),n=8)
        keratin.tube(label+'_ManualUngual'+str(digit),mir([
          (x,y+.010,.059,.053,.040),(x,y-.052,.040,.041,.027),(x,y-.080,.023,.025,.016)]),n=8)
      fore.tube(label+'_ReducedManualDigitV',mir([(.1+1.0,-1.820,.270,.047,.050),(1.174,-1.900,.190,.044,.045),(1.190,-1.985,.145,.032,.032)]),n=8)
      def conform(builder,name,y,z,ry,rz,d,offset=0.003,parent_eye=None,n=16):
        def lift(yy,zz):
          if parent_eye is None:return offset
          py,pz,pry,prz,pd=parent_eye
          return offset+pd*max(0.0,1-((yy-py)/pry)**2-((zz-pz)/prz)**2)**0.5
        vs=[]
        for j in range(n):
          yy=y+ry*math.cos(2*math.pi*j/n);zz=z+rz*math.sin(2*math.pi*j/n)
          vs.append((sg*(surf(yy,zz)+lift(yy,zz)),yy,zz))
        vs.extend([(sg*(surf(y,z)+lift(y,z)+d),y,z),(sg*(surf(y,z)-.010),y,z)])
        fs=[]
        for j in range(n):fs.extend([(j,(j+1)%n,n),((j+1)%n,j,n+1)])
        builder.add(label+name,vs,fs)
      ey=-2.955;ez=3.755
      conform(iris,'_Eye',ey,ez,.080,.073,.026)
      conform(dark,'_Pupil',ey-.010,ez+.003,.035,.042,.003,parent_eye=(ey,ez,.080,.073,.026),n=12)
      conform(dark,'_Naris',-3.865,3.630,.051,.027,.006,n=12)
      line=[]
      for y,z in [(-4.175,3.065),(-4.100,3.100),(-4.030,3.145),(-3.94,3.185),(-3.78,3.230),(-3.57,3.255),(-3.36,3.275),(-3.14,3.295),(-2.94,3.320),(-2.77,3.340)]:
        x=.29 if y<-4.16 else surf(y,z)+.003
        line.append((sg*x,y,z,.004,.004))
      dark.tube(label+'_ClosedMouthLine',line,n=6,frame=(0,0,1))
    for b in (body,hind,fore,keratin,iris,dark):b.finish(col)
    shift=ground_asset(col,center_xy=False)
    pts=[o.matrix_world@v.co for o in col.all_objects if o.type=='MESH' for v in o.data.vertices if (o.matrix_world@v.co).z<.065]
    shift[1]=-(min(v.y for v in pts)+max(v.y for v in pts))/2
    for o in col.all_objects:
      if o.type=='MESH':o.location.y+=shift[1]
    bpy.context.view_layer.update();root=bpy.data.objects[p['asset_id']]
    root['representation']='living-reconstruction';root['scale_basis']='12 m species upper estimate, not a measured fossil specimen'
    root['scientific_limits']='Artistic composite. RAM6797 missing most right skull side; Utah mount identity and original-bone percentage unknown. Tail, soft tissues, colour and pose reconstructed.'
    root['diagnostic']='High nasal arch anterior to orbits; deep robust skull and mandible; no cranial crown or tube'
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
    report={'status':'PASS','scope':'Source geometry and emitted static GLB only, not independent visual or target GPU acceptance','glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'blender_version':bpy.app.version_string,'gltf_exporter_version':'4.3.47','exporter_required_flags_probed':True,'export_options':flags,'source':audit,'glb':glb,'source_export_bounds_error_m':delta,'ground_translation_m':shift,'profile':'Static, uncompressed, texture-free palette-only','source_components':'Six editable mesh objects with semantic vertex groups','scale_note':'12.0 m nose-to-tail horizontal extent, species upper estimate rather than a single specimen measurement'}
    write(out/'qa/evidence/source-export.json',report);print(json.dumps({'status':'BUILT','glb_sha256':report['glb_sha256'],'triangles':glb['scene_triangles'],'bytes':glb['bytes']}))
if __name__=='__main__':main()
