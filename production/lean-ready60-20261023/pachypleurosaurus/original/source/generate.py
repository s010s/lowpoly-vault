#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original procedural Neusticosaurus edwardsii living reconstruction.
Run with Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output .
All generator dependencies are bundled in source/deps; no reference assets are loaded.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
from render_views import render_views

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path,value):Path(path).parent.mkdir(parents=True,exist_ok=True);Path(path).write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

class MeshBuilder:
    def __init__(self):self.vertices=[];self.faces=[];self.materials=[]
    def loft(self,stations,n=12,materials=None,axis='path'):
        # Stations are (x,y,z,halfwidth,halfdepth). Capped closed section loft.
        offset=len(self.vertices)
        for i,st in enumerate(stations):
            c=Vector(st[:3])
            if axis=='x':u=Vector((0,1,0));v=Vector((0,0,1))
            else:
                tangent=Vector(stations[min(i+1,len(stations)-1)][:3])-Vector(stations[max(i-1,0)][:3]);tangent.normalize()
                u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u).normalized()
            for j in range(n):
                a=2*math.pi*j/n;p=c+u*(st[3]*math.cos(a))+v*(st[4]*math.sin(a));self.vertices.append(tuple(p))
        for i in range(len(stations)-1):
            for j in range(n):
                self.faces.append((offset+i*n+j,offset+i*n+(j+1)%n,offset+(i+1)*n+(j+1)%n,offset+(i+1)*n+j))
                self.materials.append(materials(j,n) if materials else 0)
        for ri in [0,len(stations)-1]:
            ci=len(self.vertices);self.vertices.append(stations[ri][:3])
            for j in range(n):self.faces.append((ci,offset+ri*n+j,offset+ri*n+(j+1)%n));self.materials.append(0)
    def ellipsoid(self,center,scale,n=16,rings=8,mat=0):
        st=[]
        for i in range(rings+1):
            a=-math.pi/2+(i+.14)/(rings+.28)*math.pi
            st.append((center[0]+scale[0]*math.sin(a),center[1],center[2],scale[1]*math.cos(a),scale[2]*math.cos(a)))
        self.loft(st,n,lambda j,n:mat,'x')
    def web(self,points,thickness=.0014):
        off=len(self.vertices); n=len(points)
        for z in [-thickness/2,thickness/2]:self.vertices.extend((p[0],p[1],p[2]+z) for p in points)
        self.faces.append(tuple(off+i for i in range(n)));self.materials.append(0)
        self.faces.append(tuple(off+n+i for i in range(n)));self.materials.append(0)
        for i in range(n):self.faces.append((off+i,off+(i+1)%n,off+n+(i+1)%n,off+n+i));self.materials.append(0)
    def object(self,name,mats,collection,smooth=False):
        ob=mesh_object(name,self.vertices,self.faces,mats,collection)
        for p,m in zip(ob.data.polygons,self.materials):p.material_index=m;p.use_smooth=smooth
        return ob

def build(params):
    collection=setup_scene(params['asset_id'],params['seed']);root=bpy.data.objects[collection['asset_root']]
    root['authoring_forward']='+X';root['mount']='swimming trunk centerline';root['taxon']='Neusticosaurus edwardsii';root['scale_basis']='Published 1.25 m IPZ3935 estimate; reference photographs are not calibrated measurements'
    mats=[make_material(k,c,.82 if k!='eye' else .35) for k,c in params['materials_srgb'].items()]
    # Tail, pelvis, ribcage, narrow neck, low skull and extended rounded snout.
    profile=[
     (-.625,.021,-.007,.00065,.00065),(-.613,.022,-.006,.0015,.0018),(-.59,.023,-.004,.0030,.0034),(-.55,.024,-.002,.0049,.0055),(-.50,.022,0,.0071,.0080),(-.45,.018,.002,.010,.011),(-.40,.012,.003,.013,.014),(-.35,.006,.004,.016,.017),(-.30,.001,.003,.020,.019),(-.25,-.002,.002,.025,.022),(-.20,-.002,.001,.030,.024),(-.15,-.001,0,.035,.027),(-.105,0,0,.040,.030),
     (-.07,0,0,.045,.032),(-.025,0,0,.048,.034),(.025,0,.001,.050,.034),(.075,0,.002,.049,.033),(.125,0,.003,.046,.032),(.17,0,.004,.042,.030),(.21,0,.005,.037,.027),(.245,0,.006,.031,.023),(.27,0,.007,.024,.019),(.295,0,.008,.018,.016),
     (.325,0,.009,.0158,.0147),(.36,0,.010,.0145,.0137),(.395,0,.011,.0135,.013),(.43,0,.012,.013,.0126),(.465,0,.013,.0135,.0127),(.50,0,.014,.0142,.0130),(.525,0,.015,.0175,.0140),
     (.537,0,.016,.0215,.0155),(.548,0,.017,.0240,.017),(.560,0,.017,.0245,.0165),(.574,0,.016,.0228,.0142),(.590,0,.015,.0198,.012),(.606,0,.014,.0162,.010),(.617,0,.013,.012,.008),(.623,0,.013,.0068,.0058),(.625,0,.013,.0025,.0035)]
    def colors(j,n):
        z=math.sin(2*math.pi*(j+.5)/n)
        return 0 if z>.27 else 2 if z<-.48 else 1
    main=MeshBuilder();main.loft(profile,params['ring_sides'],colors,'x');main.object('axial-body-neck-head-tail',mats[:3],collection)
    limb_records=[]
    for sign in [-1,1]:
        for fore in [True,False]:
            label=('fore' if fore else 'hind')+('-left' if sign==1 else '-right')
            if fore:
                path=[(.239,.027,.003,.014,.014),(.229,.047,.001,.0135,.013),(.211,.082,-.007,.012,.010),(.203,.101,-.012,.011,.0085),(.214,.125,-.015,.009,.0065),(.224,.145,-.017,.0078,.0052),(.217,.158,-.018,.012,.0045)]
                tips=[(.252,.169),(.239,.188),(.218,.196),(.196,.189),(.180,.174)]
                bases=[(.235,.156),(.227,.161),(.216,.163),(.205,.159),(.197,.153)]
                palm=(.216,.155,-.018);ps=(.022,.015,.0048);rad=.0027
            else:
                path=[(-.069,.028,-.002,.011,.011),(-.082,.049,-.009,.010,.009),(-.105,.077,-.017,.009,.008),(-.111,.093,-.020,.0085,.007),(-.100,.114,-.023,.007,.0055),(-.103,.133,-.025,.0065,.0045),(-.112,.145,-.026,.010,.0039)]
                tips=[(-.081,.155),(-.093,.173),(-.114,.181),(-.134,.174),(-.148,.158)]
                bases=[(-.095,.142),(-.103,.147),(-.114,.149),(-.125,.146),(-.132,.14)]
                palm=(-.113,.142,-.026);ps=(.019,.013,.0041);rad=.00235
            mb=MeshBuilder();mb.loft([(x,sign*y,z,w,d) for x,y,z,w,d in path],12)
            mb.ellipsoid((palm[0],sign*palm[1],palm[2]),ps,16,8)
            for i,((bx,by),(tx,ty)) in enumerate(zip(bases,tips)):
                z=palm[2];dx=tx-bx;dy=ty-by
                mb.loft([(bx,sign*by,z,rad*1.3,rad*.85),(bx+dx*.36,sign*(by+dy*.36),z-.0007,rad,rad*.75),(bx+dx*.73,sign*(by+dy*.73),z-.0015,rad*.82,rad*.63),(tx,sign*ty,z-.0018,rad*.32,rad*.3)],8)
            # Thin, closed, shallow webs end proximal to each distinct digit tip.
            for i in range(4):
                a=bases[i];b=bases[i+1];ta=tips[i];tb=tips[i+1];z=palm[2]
                pts=[(a[0],sign*a[1],z),(b[0],sign*b[1],z),(b[0]+.27*(tb[0]-b[0]),sign*(b[1]+.27*(tb[1]-b[1])),z),(a[0]+.27*(ta[0]-a[0]),sign*(a[1]+.27*(ta[1]-a[1])),z)]
                mb.web(pts)
            ob=mb.object(label,[mats[1]],collection)
            ob['digit_count']=5;ob['partial_webbing']='inferred, shallow proximal only';ob['anatomical_pair']='forelimbs' if fore else 'hindlimbs'
            limb_records.append({'name':label,'digits':5,'upper_lower_path_m':[list(p[:3]) for p in path],'tips_blender_m':[[tx,sign*ty,palm[2]-.0018] for tx,ty in tips],'path_length_m':sum((Vector(path[i][:3])-Vector(path[i-1][:3])).length for i in range(1,len(path)))+max(math.dist(b,t) for b,t in zip(bases,tips))})
    eyes=MeshBuilder();iris=MeshBuilder();details=MeshBuilder()
    for s in [-1,1]:
        eyes.ellipsoid((.550,s*.0223,.024),(.0054,.0030,.0050),16,8)
        iris.ellipsoid((.551,s*.0249,.0244),(.0027,.00075,.0030),12,6)
        # Small external nares and a restrained closed jaw commissure.
        details.ellipsoid((.609,s*.0128,.0210),(.0017,.00095,.00115),10,5)
        stations=[(.544,s*.0207,.0085,.0007,.00055),(.559,s*.0231,.0078,.0007,.00055),(.579,s*.0214,.0065,.00065,.0005),(.598,s*.0176,.0054,.00055,.00045),(.616,s*.0108,.0067,.00035,.00035)]
        details.loft(stations,6)
    eyes.object('paired-eyes',[mats[3]],collection,True);iris.object('paired-iris',[mats[4]],collection,True);details.object('closed-jaws-and-nares',[mats[3]],collection)
    return collection,{'axial_stations':len(profile),'estimated_partition_lengths_m':params['partitions_m'],'limbs':limb_records,'anatomical_limb_count':4,'digit_count_each':5,'tail':'continuous tapered cone without fin or fluke','widths_m':{'maximum_trunk':.10,'mid_neck':.026,'maximum_skull':.049},'mount':'swimming origin, not ground contact','surface_assembly':'Closed anatomical solids. Limb/palm/digit/web solids overlap intentionally; not a printable Boolean union.'}

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=SOURCE.parent);ap.add_argument('--grey',action='store_true');ap.add_argument('--render-glb',action='store_true');args=ap.parse_args(argv)
    params=json.loads((SOURCE/'params.json').read_text());out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if args.render_glb:
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(out/'model.glb'))
        col=bpy.data.collections.new('IMPORTED_GLB');bpy.context.scene.collection.children.link(col)
        for ob in list(bpy.context.scene.objects):
            for old in list(ob.users_collection):old.objects.unlink(ob)
            col.objects.link(ob)
        record=render_views(col,out/'views',resolution=params['render']['resolution'],samples=params['render']['samples'])
        record['glb_sha256']=sha(out/'model.glb');record['source']='Clean import of delivered model.glb, not source scene';record['preview_reuse']='preview.png is byte-identical to views/perspective.png'
        (out/'preview.png').write_bytes((out/'views/perspective.png').read_bytes());save(out/'qa/evidence/exact-glb-views.json',record);return
    col,morph=build(params)
    if args.grey:
        record=render_views(col,out,grey=True,resolution=512,samples=12,views=['front','top','perspective']);save(out/'grey-record.json',record);return
    source=audit_source(col,24000)
    if source['errors']:raise RuntimeError(str(source['errors']))
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene['generator']='source/generate.py';bpy.context.scene['generator_seed']=params['seed'];bpy.context.scene['asset_license']='CC-BY-4.0'
    # Embed source text using relative names; no machine path inside the editable file.
    for f in [SOURCE/'generate.py',SOURCE/'params.json']:
        t=bpy.data.texts.new(f.name);t.write(f.read_text())
    bpy.context.scene.render.filepath='//preview.png'
    # Serialize only the editable scene and source texts, not machine-specific UI state.
    bpy.data.libraries.write(str(out/'model.blend'),{bpy.context.scene,*bpy.data.texts},path_remap='RELATIVE',fake_user=True,compress=False)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if missing:raise RuntimeError('Missing exporter flags: '+str(missing))
    bpy.ops.export_scene.gltf(**options)
    glb=audit_glb(out/'model.glb',24000,6,16);glb['file']='model.glb'
    b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
    err=max(abs(glb['bounds_m'][k][i]-e[i]) for k,e in [('min',emin),('max',emax)] for i in range(3))
    assert not glb['errors'],glb['errors'];assert err<.0001;assert source['triangles']==glb['scene_triangles'];assert glb['bytes']<=2500000
    save(out/'qa/evidence/technical.json',{'status':'PASS','scope':'Source/static GLB/source-to-export checks only','blender':bpy.app.version_string,'generator_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':err,'export_options':{k:v for k,v in options.items() if k!='filepath'},'reviewed_warnings':['Smooth eye surfaces are intentional.','Specimen uses an explicit swimming centerline mount, not floor contact.'],'gpu':'UNKNOWN','scene':'UNKNOWN'})
    save(out/'qa/evidence/morphology.json',{'glb_sha256':sha(out/'model.glb'),'measurements_and_construction':morph,'scientific_limits':'1.25 m is an author estimate for IPZ3935, not a photo measurement. Soft tissue, webbing and color inferred.'})
if __name__=='__main__':main()
