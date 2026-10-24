# SPDX-License-Identifier: MIT
"""Original articulated Pentecopterus reconstruction. Run in Blender with -- --output DIRECTORY."""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, ground_asset
from qa_glb import audit_glb

class Builder:
    def __init__(self,name,collection,materials):
        self.name=name;self.collection=collection;self.materials=materials
        self.v=[];self.f=[];self.mi=[];self.groups={}
    def add(self,verts,faces,material=0,group='shape'):
        start=len(self.v);self.v.extend([tuple(v) for v in verts]);self.f.extend([tuple(start+i for i in f) for f in faces]);self.mi.extend(material if isinstance(material,list) else [material]*len(faces));self.groups.setdefault(group,[]).extend(range(start,len(self.v)))
    def tube(self,points,radii,material=0,group='segment',sides=12,flatten=1.0):
        points=[Vector(p) for p in points];v=[];f=[]
        for i,p in enumerate(points):
            t=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
            u=t.cross(Vector((0,0,1)))
            if u.length<.01:u=t.cross(Vector((0,1,0)))
            u.normalize();w=t.cross(u).normalized()
            for k in range(sides):
                a=2*math.pi*k/sides;v.append(p+u*(math.cos(a)*radii[i])+w*(math.sin(a)*radii[i]*flatten))
        for i in range(len(points)-1):
            for k in range(sides):a=i*sides+k;b=i*sides+(k+1)%sides;c=b+sides;d=a+sides;f.append((a,b,c,d))
        f.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+k for k in range(sides))])
        self.add(v,f,material,group)
    def pod(self,a,b,r1,r2,number,flatten=.72):
        a,b=Vector(a),Vector(b);d=b-a
        points=[a-d*.045,a+d*.12,a+d*.48,a+d*.91,b+d*.045]
        self.tube(points,[r1*.78,r1,r1*.64+r2*.39,r2,r2*.81],0,number,12,flatten)
        self.tube([a-d*.06,a+d*.05],[r1*.68,r1*.73],2,number+'-joint',8,flatten)
    def spike(self,a,b,r,group):
        a,b=Vector(a),Vector(b);d=b-a
        self.tube([a,a+d*.25,a+d*.65,b],[r,r*.8,r*.40,.0003],1,group,8,.85)
    def finish(self):
        o=mesh_object(self.name,self.v,self.f,self.materials,self.collection)
        for poly,mi in zip(o.data.polygons,self.mi):poly.material_index=mi
        for name,inds in self.groups.items():o.vertex_groups.new(name=name).add(inds,1,'REPLACE')
        o['semantic_parts']=json.dumps(list(self.groups),separators=(',',':'))
        return o

def armor(name,profiles,collection,mats,n=24):
    # Longitudinal sculpted oval sections; the dorsal roof is broader than the belly.
    v=[];f=[];mi=[]
    for y,width,z,depth in profiles:
        for j in range(n):
            a=2*math.pi*j/n;c=math.cos(a);s=math.sin(a)
            v.append((width*c,y,z+depth*s*(1 if s>=0 else .58)))
    for i in range(len(profiles)-1):
        for j in range(n):
            f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
            mi.append(1 if i==len(profiles)-2 else 2 if math.sin(2*math.pi*(j+.5)/n)<-.1 else 0)
    f.extend([tuple(reversed(range(n))),tuple((len(profiles)-1)*n+j for j in range(n))]);mi.extend([2,2])
    o=mesh_object(name,v,f,mats,collection)
    for p,m in zip(o.data.polygons,mi):p.material_index=m
    return o

def build(p):
    col=setup_scene(p['asset_id'],p['seed']);root=bpy.data.objects[col['asset_root']]
    pal=p['palette_srgb_hex'];dorsal=make_material('cuticle-umber',pal['dorsal'],.8);edge=make_material('cuticle-worn-edge',pal['edge'],.85);ventral=make_material('cuticle-ventral',pal['ventral'],.9);joint=make_material('joint-membrane',pal['joint'],.95);eye=make_material('hypothetical-dark-eye',pal['eye_hypothetical'],.48)
    mats=[dorsal,edge,ventral];limbmat=[dorsal,edge,joint]
    # Headshield: a long rostrate trapezoid, not a semicircular horseshoe shield.
    shield=armor('prosomal-shield-hypothetical',[
        (-.425,.050,.064,.005),(-.419,.060,.064,.010),(-.401,.065,.063,.019),(-.369,.073,.061,.027),(-.329,.084,.060,.029),(-.284,.094,.058,.026),(-.252,.095,.055,.023),(-.245,.086,.053,.018)],col,mats,32)
    # A shallow median rostral notch formed in the front vertices, not an added horn.
    for ve in shield.data.vertices:
        x,y,z=ve.co
        if y<-.418 and abs(x)<.017:ve.co.y+=.006*(1-abs(x)/.017)
    shield['inference']='Dorsal shell not preserved; hypothetical low dome informed by ventral outline.'
    # Twelve sealed overlapping armor units, including a reduced first tergite.
    lengths=[.022,.042,.043,.044,.045,.046,.044,.039,.035,.033,.039,.058]
    widths=[.089,.091,.092,.092,.089,.083,.074,.065,.056,.046,.035,.025]
    y=-.245
    trunk=[]
    for i,(length,width) in enumerate(zip(lengths,widths)):
        zw=.050-i*.0013;dep=.024-i*.0011
        wn=widths[min(i+1,11)] if i<11 else .020
        prof=[(y-.001,width*.96,zw,dep*.79),(y+length*.14,width,zw,dep),(y+length*.55,width*.99,zw,dep*.98),(y+length*.91,(width*.5+wn*.5),zw-.001,dep*.92),(y+length+.001,wn*.98,zw-.001,dep*.76)]
        o=armor(f'opisthosoma-{i+1:02d}',prof,col,mats,28);o['segment_number']=i+1
        # Restrained shallow scale relief, built into the segment mesh as attached solids.
        if 1<=i<=8:
            b=Builder('temporary-scale',col,[edge])
            for k in [-1,0,1]:
                x=k*.004;y0=y+length*.55+(abs(k)*.005);top=zw+dep*math.sqrt(max(0,1-(x/width)**2))
                b.tube([(x,y0-.003,top-.0007),(x,y0,top+.0005),(x,y0+.003,top-.0007)],[.0012,.0018,.0004],0,'scale',8,.48)
            start=len(o.data.vertices);sv=[tuple(v.co) for v in o.data.vertices]+b.v;sf=[tuple(f.vertices) for f in o.data.polygons]+[tuple(start+j for j in f) for f in b.f];oldmi=[f.material_index for f in o.data.polygons]
            new=bpy.data.meshes.new(o.name+'-relief');new.from_pydata(sv,[],sf);new.update();
            for m in mats:new.materials.append(m)
            for poly,mi in zip(new.polygons,oldmi+[1]*len(b.f)):poly.material_index=mi
            bm=bmesh.new();bm.from_mesh(new);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(new);bm.free();old=o.data;o.data=new;bpy.data.meshes.remove(old)
        trunk.append(o);y+=length
    # Telson: a single broad xiphous blade with softly rounded lateral shoulders.
    telson=armor('telson-single-xiphous',[(.245,.0195,.035,.009),(.265,.027,.034,.010),(.292,.0325,.032,.009),(.325,.030,.030,.008),(.365,.022,.027,.006),(.398,.011,.025,.0038),(.425,.0007,.023,.001)],col,mats,24)
    # Small eyes sit directly in the inferred dorsal shield surface.
    for side in [-1,1]:
        b=Builder(('L' if side<0 else 'R')+'-hypothetical-eye',col,[eye,edge])
        pts=[(side*.050,-.365,.079),(side*.056,-.359,.081),(side*.061,-.349,.081),(side*.061,-.340,.079)]
        b.tube(pts,[.0035,.0044,.0042,.0029],0,'reniform-eye',12,.54);ob=b.finish();ob['inference']='Hypothetical small reniform lateral eye; not preserved.'
    # Paired appendages: one mesh per functional limb, editable podomere groups.
    for s in [-1,1]:
        side='L' if s<0 else 'R'
        def P(x,y,z):return (s*x,y,z)
        # I: modest three-part chelicerae, almost entirely below the rostrum.
        b=Builder(side+'-I-chelicera',col,limbmat)
        pts=[P(.014,-.292,.041),P(.020,-.338,.034),P(.025,-.390,.036),P(.019,-.428,.039)]
        for k in range(3):b.pod(pts[k],pts[k+1],[.007,.005,.0035][k],[.005,.0035,.0011][k],f'I-{k+1}')
        b.spike(P(.025,-.400,.037),P(.032,-.427,.039),.0018,'I-small-fixed-finger');b.finish()
        # II: short stout arm, fourth-podomere paired long spine is conspicuous.
        pts=[P(.032,-.299,.044),P(.049,-.321,.040),P(.062,-.350,.041),P(.074,-.378,.047),P(.080,-.408,.055),P(.081,-.438,.063),P(.079,-.464,.069),P(.073,-.481,.074)]
        radii=[.015,.015,.014,.012,.010,.007,.0042,.0010]
        b=Builder(side+'-II-short-raptorial',col,limbmat)
        for k in range(7):b.pod(pts[k],pts[k+1],radii[k],radii[k+1],f'II-{k+1}')
        for k in [2,3,4]:
            a=Vector(pts[k+1]);length={2:.020,3:.056,4:.023}[k]
            for q in [-1,1]:b.spike(a+Vector((s*q*radii[k]*.60,.002,-.004)),a+Vector((s*q*(.013 if k==3 else .009),-length,-.002)),.0028 if k==3 else .0021,f'II-{k+1}-spine-{q}')
        b.finish()
        # III: eight podomeres; pairs on 3,4,5,6 progressively increase in length.
        pts=[P(.055,-.282,.046),P(.096,-.300,.042),P(.131,-.334,.044),P(.151,-.382,.049),P(.161,-.425,.055),P(.164,-.467,.059),P(.161,-.513,.064),P(.155,-.579,.069),P(.145,-.605,.071)]
        radii=[.021,.022,.021,.017,.014,.012,.010,.0046,.0008]
        b=Builder(side+'-III-long-raptorial',col,limbmat)
        for k in range(8):b.pod(pts[k],pts[k+1],radii[k],radii[k+1],f'III-{k+1}')
        for k,L in [(3,.022),(4,.034),(5,.049),(6,.072)]:
            a=Vector(pts[k]);r=radii[k]
            for q in [-1,1]:
                start=a+Vector((s*q*r*.70,.004,-.003))
                end=a+Vector((s*q*(.019+L*.11),-L,-.011 if q==-1 else .001))
                b.spike(start,end,.0031 if k<6 else .0035,f'III-{k}-fixed-spine-{q}')
        b.finish()
        # IV: shorter, ventrolateral spinose walking/capture limb.
        pts=[P(.053,-.274,.039),P(.087,-.275,.031),P(.118,-.282,.022),P(.146,-.292,.016),P(.171,-.306,.014),P(.191,-.324,.020),P(.205,-.344,.031),P(.207,-.365,.042)]
        radii=[.012,.012,.011,.010,.009,.007,.0045,.0010]
        b=Builder(side+'-IV-ventral-spinose',col,limbmat)
        for k in range(7):b.pod(pts[k],pts[k+1],radii[k],radii[k+1],f'IV-{k+1}',.83)
        for k,L in [(3,.014),(4,.022),(5,.028),(6,.034)]:
            a=Vector(pts[k])
            for q in [-1,1]:b.spike(a+Vector((s*q*radii[k]*.65,.002,0)),a+Vector((s*q*.012,-L,.012)),.0025,f'IV-{k}-spine-{q}')
        b.finish()
        # V: reduced slender armature and a small three-point terminal outline.
        pts=[P(.057,-.261,.041),P(.085,-.251,.032),P(.112,-.242,.023),P(.138,-.232,.016),P(.162,-.226,.012),P(.184,-.222,.011),P(.201,-.221,.011),P(.211,-.224,.012)]
        radii=[.010,.009,.008,.007,.006,.0048,.0028,.0008]
        b=Builder(side+'-V-slender-walking',col,limbmat)
        for k in range(7):b.pod(pts[k],pts[k+1],radii[k],radii[k+1],f'V-{k+1}')
        # Restrained denticles embedded in the distal rims, distinct from the terminal fingers.
        for k in [4,5,6]:
            a=Vector(pts[k]);r=radii[k]
            for q in [-1,1]:
                base=a+Vector((-s*.0008,q*r*.55,.0003))
                tip=a+Vector((s*.0014,q*(r+.0031),.0010))
                b.spike(base,tip,.0013,f'V-{k}-rim-denticle-{q}')
        for q in [-1,1]:b.spike(P(.198,-.221,.011),P(.208,-.221+q*.006,.012),.0014,f'V-terminal-{q}')
        b.finish()
        # VI: articulated compound paddle, tilted out of the explanatory fossil plane.
        b=Builder(side+'-VI-compound-paddle',col,limbmat)
        pts=[P(.060,-.252,.045),P(.086,-.225,.036),P(.110,-.199,.027),P(.132,-.173,.024),P(.149,-.146,.024),P(.159,-.120,.025)]
        radii=[.015,.016,.013,.012,.010,.009]
        for k in range(5):b.pod(pts[k],pts[k+1],radii[k],radii[k+1],f'VI-{k+1}',.60)
        # Each leaf is a closed shaped lens with edge rings, not an oval primitive.
        def leaf(name,outline,z,thickness,material=0):
            # outline is local in XY with moderate anteroposterior tilt.
            n=len(outline);cx=sum(x for x,y in outline)/n;cy=sum(y for x,y in outline)/n;v=[];faces=[];mi=[]
            for t,dz in [(1,0),(.80,thickness),(.32,thickness*1.24),(.80,-thickness*.52)]:
                for x,y in outline:
                    xx=cx+(x-cx)*t;yy=cy+(y-cy)*t;v.append((s*xx,yy,z+dz+(yy-cy)*.12))
            for r0,r1,m in [(0,1,1),(1,2,material),(0,3,material)]:
                for j in range(n):faces.append((r0*n+j,r0*n+(j+1)%n,r1*n+(j+1)%n,r1*n+j));mi.append(m)
            faces.extend([tuple(2*n+j for j in range(n)),tuple(reversed([3*n+j for j in range(n)]))]);mi.extend([material,2]);b.add(v,faces,mi,name)
        leaf('VI-6-expanded-leaf',[(.150,-.143),(.163,-.157),(.183,-.155),(.202,-.144),(.214,-.129),(.194,-.115),(.173,-.108),(.158,-.113)],.028,.0055)
        leaf('VI-7-elongate-blade',[(.155,-.116),(.172,-.123),(.193,-.112),(.211,-.090),(.213,-.072),(.202,-.057),(.185,-.063),(.169,-.082),(.156,-.099)],.023,.0054)
        leaf('VI-7a-overlap',[(.193,-.077),(.203,-.076),(.211,-.066),(.209,-.053),(.202,-.049),(.195,-.060)],.0238,.0025,1)
        leaf('VI-8-oval-distal',[(.198,-.068),(.211,-.065),(.215,-.051),(.210,-.037),(.201,-.032),(.194,-.044),(.193,-.057)],.020,.004)
        b.pod(P(.205,-.035,.020),P(.201,-.020,.017),.004,.0012,'VI-9-terminal',.5)
        b.finish()
    # Discreet inferred ventral oral plate, never a genital-type claim.
    armor('hypothetical-metastoma',[(-.315,.009,.033,.003),(-.303,.014,.033,.004),(-.281,.012,.034,.004),(-.271,.004,.034,.002)],col,[ventral,ventral,ventral],16)['inference']='Metastoma not preserved. Shape hypothetical; sex and genital type not assigned.'
    shift=ground_asset(col,False)
    root['taxon']=p['target_taxon'];root['representation']=p['representation'];root['body_length_m']=.85;root['scientific_limits']='Dorsal shield, eyes, metastoma, depth, pose and colors are reconstruction choices. No cercal blades.'
    return col,shift

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True);(out/'qa/evidence').mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text());col,shift=build(p);budget=p['geometry_policy'];source=audit_source(col,budget['max_triangles'])
    if source['errors']:raise RuntimeError(json.dumps(source['errors']))
    source['mount_shift_m']=shift
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s'
    # Runtime-resolved absolute save path is necessary; no source-machine locator is hard coded.
    bpy.ops.wm.save_as_mainfile(filepath=str((out/'model.blend').resolve()),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    flags=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(flags)-available:raise RuntimeError('Missing required glTF export options')
    bpy.ops.export_scene.gltf(**flags)
    glb=audit_glb(out/'model.glb',budget['max_triangles'],budget['max_materials'],budget['max_primitives'])
    glb['file']='model.glb'
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][s][i]-expected[s][i]) for s in ['min','max'] for i in range(3))
    if glb['errors'] or delta>.0001 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Export audit failed '+str(glb))
    if (out/'model.glb').stat().st_size>budget['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    doc={'status':'PASS','scope':'Source topology and static GLB technical audit only. Not visual, GPU, scene, user or deployment approval.','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'runtime':{'blender':bpy.app.version_string,'exporter':'4.3.47','target_three':'0.180.0'},'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'export_flags':{k:v for k,v in flags.items() if k!='filepath'},'glb_sha256':hashlib.sha256((out/'model.glb').read_bytes()).hexdigest()}
    (out/'qa/evidence/technical.json').write_text(json.dumps(doc,indent=2)+'\n')
    print('MODEL_COMPLETE',json.dumps({'triangles':source['triangles'],'bytes':(out/'model.glb').stat().st_size,'primitives':glb.get('scene_primitives'),'sha256':doc['glb_sha256']}))
if __name__=='__main__':main()
