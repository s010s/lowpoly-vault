#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Guanlong wucaii reconstruction based on adult IVPP V14531.
Run: blender -b -t 2 --python source/generate.py -- --output .
Known crest bone windows are displayed open by artistic choice. Living skin
covering, colour and pose are unknown. The anterior crest margin is restored.
"""
from pathlib import Path
import argparse,hashlib,json,math,sys
import bpy
from mathutils import Vector,geometry
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
class Part:
    def __init__(self):self.v=[];self.f=[];self.mi=[]
    def add(self,v,f,mi=0):
        b=len(self.v);self.v.extend(v);self.f.extend(tuple(b+i for i in face) for face in f);self.mi.extend(mi if isinstance(mi,list) else [mi]*len(f))
    def object(self,name,mats,col):
        ob=mesh_object(name,self.v,self.f,mats,col)
        for p,i in zip(ob.data.polygons,self.mi):p.material_index=i
        return ob

def loft_y(part,rows,n=14,belly=False):
    v=[];f=[];mi=[]
    for y,z,rx,rz in rows:
        for j in range(n):
            a=2*math.pi*j/n;v.append((rx*math.cos(a),y,z+rz*math.sin(a)))
    f.append(tuple(range(n-1,-1,-1)));mi.append(0)
    for k in range(len(rows)-1):
        for j in range(n):
            f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if belly and math.sin(2*math.pi*(j+.5)/n)<-.45 else 0)
    f.append(tuple((len(rows)-1)*n+j for j in range(n)));mi.append(0);part.add(v,f,mi)

def tube(part,rows,n=8,mi=0):
    pts=[Vector(r[:3]) for r in rows];v=[];f=[]
    for k,r in enumerate(rows):
        tangent=(pts[min(k+1,len(pts)-1)]-pts[max(k-1,0)]).normalized();u=Vector((1,0,0))
        if abs(u.dot(tangent))>.92:u=Vector((0,1,0))
        u=(u-tangent*u.dot(tangent)).normalized();w=tangent.cross(u).normalized()
        for j in range(n):
            a=2*math.pi*j/n;v.append(tuple(pts[k]+u*r[3]*math.cos(a)+w*r[4]*math.sin(a)))
    f.append(tuple(range(n-1,-1,-1)))
    for k in range(len(rows)-1):
        for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    f.append(tuple((len(rows)-1)*n+j for j in range(n)));part.add(v,f,mi)

def ellipsoid(part,c,r,n=8,l=4,mi=0):
    v=[(c[0],c[1],c[2]+r[2])];f=[]
    for i in range(1,l):
        a=math.pi*i/l
        for j in range(n):
            b=2*math.pi*j/n;v.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]+r[2]*math.cos(a)))
    bot=len(v);v.append((c[0],c[1],c[2]-r[2]))
    for j in range(n):f.append((0,1+j,1+(j+1)%n))
    for i in range(l-2):
        for j in range(n):f.append((1+i*n+j,1+(i+1)*n+j,1+(i+1)*n+(j+1)%n,1+i*n+(j+1)%n))
    for j in range(n):f.append((bot,1+(l-2)*n+(j+1)%n,1+(l-2)*n+j))
    part.add(v,f,mi)

def point_in(p,poly):
    x,y=p;inside=False
    for i,a in enumerate(poly):
        b=poly[(i+1)%len(poly)]
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
    return inside

def perforated_crest(part):
    # Y/Z outline: high, delicate single median blade. Front-upper segment is restored.
    outer=[(-.983,1.349),(-.942,1.391),(-.898,1.444),(-.842,1.494),(-.783,1.531),(-.723,1.551),(-.666,1.553),(-.622,1.538),(-.602,1.515),(-.608,1.493),(-.647,1.468),(-.682,1.442),(-.710,1.402),(-.738,1.363),(-.820,1.351),(-.900,1.343)]
    # Large posterior pneumatic fenestra plus two smaller anterior/ventral fenestrae.
    windows=[ [(-.771,1.451),(-.751,1.490),(-.713,1.522),(-.669,1.527),(-.638,1.516),(-.630,1.502),(-.657,1.485),(-.702,1.462),(-.744,1.444)],
              [(-.902,1.387),(-.869,1.431),(-.832,1.465),(-.802,1.483),(-.797,1.466),(-.815,1.430),(-.845,1.405),(-.882,1.385)],
              [(-.820,1.379),(-.800,1.404),(-.780,1.418),(-.755,1.421),(-.747,1.408),(-.766,1.389),(-.791,1.378)] ]
    verts=[];edges=[]
    for poly in [outer]+windows:
        o=len(verts);verts.extend(Vector(p) for p in poly);edges.extend((o+i,o+(i+1)%len(poly)) for i in range(len(poly)))
    vv,ee,ff,_,_,_=geometry.delaunay_2d_cdt(verts,edges,[],0,1e-7)
    faces=[]
    for face in ff:
        c=sum((vv[i] for i in face),Vector((0,0)))/len(face)
        if point_in(c,outer) and not any(point_in(c,w) for w in windows):faces.append(face)
    # Extruded single connected plate. Actual through-windows, not painted dark spots.
    def half(p):return .002+max(0,min(1,(p[0]+.785)/.16))*.005
    v=[(s*half(p),p[0],p[1]) for s in [-1,1] for p in vv];n=len(vv);f=[];mi=[];count={}
    for face in faces:
        f.append(tuple(reversed(face)));mi.append(0);f.append(tuple(n+i for i in face));mi.append(0)
        for j,a in enumerate(face):
            b=face[(j+1)%len(face)];key=tuple(sorted((a,b)));count[key]=count.get(key,0)+1
    for (a,b),c in count.items():
        if c==1:f.append((a,b,n+b,n+a));mi.append(1)
    part.add(v,f,mi)
    return {'outline_yz_m':outer,'window_boundaries_yz_m':windows,'lateral_laminae':4,'window_count':3}

def lamina(part,side,anchor,tip,width):
    # Thin oblique triangular buttress extending anteroventrally from median blade.
    ay,az=anchor;ty,tz=tip;t=.002
    center=[(side*.003,ay,az),(side*width,ty,tz),(side*.004,ty-.018,tz+.006)]
    v=[(x+s*t,y,z) for s in [-1,1] for x,y,z in center]
    part.add(v,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],0)

def build(out):
    params=json.loads((HERE/'params.json').read_text());col=setup_scene('guanlong',params['seed']);mats={k:make_material(k,v,.86) for k,v in params['palette'].items()}
    # Continuous S-curved cervical series, shallow trunk and long tapering counterweight.
    body=Part();rows=[(-.645,1.231,.045,.061),(-.613,1.197,.049,.071),(-.566,1.126,.052,.083),(-.513,1.036,.058,.094),
      (-.446,.956,.072,.120),(-.358,.917,.097,.147),(-.244,.902,.129,.169),(-.100,.899,.153,.177),
      (.057,.903,.158,.177),(.199,.910,.144,.155),(.328,.907,.113,.123),(.449,.901,.084,.085),
      (.580,.892,.066,.063),(.740,.879,.049,.048),(.925,.865,.038,.037),(1.119,.850,.030,.029),
      (1.308,.835,.023,.023),(1.495,.826,.018,.018),(1.661,.826,.012,.013),(1.802,.836,.008,.009),(1.901,.850,.004,.005),(1.970,.861,.001,.0015)]
    loft_y(body,rows,16,True);body.object('axial-neck-trunk-balancing-tail',[mats['body'],mats['belly']],col)
    # Long shallow snout and modest orbit. No enlarged adult-Tyrannosaurus skull mass.
    head=Part();loft_y(head,[(-1.030,1.268,.019,.032),(-1.009,1.274,.031,.042),(-.961,1.281,.038,.047),
      (-.898,1.290,.043,.054),(-.830,1.304,.050,.066),(-.770,1.314,.063,.075),(-.714,1.317,.070,.080),
      (-.661,1.303,.064,.074),(-.623,1.279,.048,.059),(-.611,1.260,.033,.043)],14,True)
    head.object('long-shallow-skull',[mats['body'],mats['belly']],col)
    crest=Part();crest_record=perforated_crest(crest)
    for s in [-1,1]:
        lamina(crest,s,(-.814,1.448),(-.898,1.349),.034)
        lamina(crest,s,(-.660,1.473),(-.791,1.370),.050)
    ob=crest.object('single-fenestrated-median-crest-and-four-laminae',[mats['crest'],mats['crest_rim']],col)
    ob['external_windows']='Artistic exposed-framework treatment; living skin across fenestrae unknown.'
    ob['anterior_contour']='Restored missing portion following primary Fig 2.'
    dark=Part();eyes=Part();measurements=[]
    for side,label in [(-1,'left'),(1,'right')]:
        dy=.041 if side<0 else -.041
        hip=(side*.112,.183+dy,.912);knee=(side*.176,-.012+dy,.568);ankle=(side*.169,.180+dy,.252);foot=(side*.170,.117+dy,.064)
        leg=Part();tube(leg,[(*hip,.087,.104),(side*.156,.110+dy,.783,.088,.101),(*knee,.054,.062),
          (side*.172,.066+dy,.431,.037,.043),(*ankle,.026,.030),(*foot,.020,.022)],10)
        ellipsoid(leg,(side*.170,.088+dy,.048),(.037,.060,.037),8,4)
        for j in [-1,0,1]:
            x=side*.170+j*.030;y=-.108+abs(j)*.038+dy
            tube(leg,[(side*.170+j*.018,.074+dy,.039,.013,.014),(x,-.008+dy,.023,.011,.012),(x+j*.011,y,.015,.008,.009)],7)
            tube(dark,[(x+j*.011,y,.016,.009,.008),(x+j*.012,y-.025,.008,.005,.005),(x+j*.013,y-.039,.004,.001,.001)],6)
        tube(leg,[(side*.154,.117+dy,.095,.008,.008),(side*.142,.179+dy,.071,.006,.005)],6)
        tube(dark,[(side*.142,.179+dy,.071,.006,.006),(side*.137,.198+dy,.052,.001,.001)],6)
        leg.object('slender-hindlimb-'+label,mats['body'],col)
        # Anatomical path totals about 58% of hindlimb path; manus includes digits.
        shoulder=(side*.105,-.333,.925);elbow=(side*.170,-.220,.746);wrist=(side*.208,-.334,.630)
        arm=Part();tube(arm,[(*shoulder,.040,.045),(side*.150,-.275,.840,.032,.036),(*elbow,.025,.030),
          (side*.193,-.278,.680,.018,.023),(*wrist,.013,.017),(side*.211,-.370,.605,.013,.026)],10)
        ellipsoid(arm,(side*.211,-.372,.601),(.013,.034,.032),8,4)
        # Palms face inward; fingers are separated in the parasagittal plane.
        finger_claw_start=len(dark.v)
        digits=[(-.405,.615,-.469,.581,-.490,.550,.010),(-.382,.589,-.445,.525,-.459,.485,.0105),(-.355,.584,-.398,.523,-.402,.480,.007)]
        for i,(y0,z0,y1,z1,y2,z2,r) in enumerate(digits):
            xx=side*(.212+.002*(i-1));tube(arm,[(xx,y0,z0,r,r*1.10),(xx,y1,z1,r*.77,r*.83),(xx,y2,z2,r*.58,r*.62)],7)
            tube(dark,[(xx,y2,z2,r*.64,r*.67),(xx,y2-.014,z2-.013,r*.45,r*.44),(xx,y2-.009,z2-.028,.001,.001)],6)
        # A small proportional refinement preserves long arms at approximately 58% of the posed hindlimb.
        arm_scale=.935
        arm.v=[tuple(Vector(shoulder)+(Vector(v)-Vector(shoulder))*arm_scale) for v in arm.v]
        dark.v[finger_claw_start:]=[tuple(Vector(shoulder)+(Vector(v)-Vector(shoulder))*arm_scale) for v in dark.v[finger_claw_start:]]
        arm.object('long-three-fingered-inward-palm-'+label,mats['body'],col)
        # Small eyes, dark inset perimeter and restrained gold iris.
        ellipsoid(dark,(side*.0658,-.699,1.342),(.007,.019,.017),10,5)
        ellipsoid(eyes,(side*.0715,-.701,1.342),(.0035,.013,.0115),10,5)
        ellipsoid(dark,(side*.0745,-.705,1.342),(.0018,.0052,.0076),8,4)
        ellipsoid(dark,(side*.035,-.982,1.290),(.002,.007,.004),8,4)
        tube(dark,[(side*.021,-1.027,1.254,.0015,.0015),(side*.034,-.989,1.249,.0019,.0019),
          (side*.042,-.925,1.249,.0019,.0019),(side*.049,-.854,1.252,.002,.002),(side*.060,-.780,1.257,.002,.002),(side*.063,-.700,1.259,.0015,.0015)],6)
        hind=sum((Vector(b)-Vector(a)).length for a,b in [(hip,knee),(knee,ankle),(ankle,foot)])
        digit2=(side*.214,-.459,.457)
        fore=sum((Vector(b)-Vector(a)).length for a,b in [(shoulder,elbow),(elbow,wrist),(wrist,digit2)])
        measurements.append({'side':label,'hindlimb_centerline_m':hind,'forelimb_centerline_m':fore*arm_scale,'forelimb_hindlimb_ratio':fore*arm_scale/hind,'definition':'Hip-knee-ankle-metatarsal contact versus shoulder-elbow-wrist-digit-II claw tip; approximate posed soft-tissue centreline, not fossil bone measurements.'})
    dark.object('claws-nares-mouth-pupils',mats['keratin'],col);eyes.object('small-irises',mats['iris'],col)
    scene=bpy.context.scene;scene['reconstruction_scope']='Adult IVPP V14531 cranial anatomy and approximately 3 m length. Fig 1 juvenile V14532 is not the adult skeleton. Living covering and colour unknown. Open crest windows display bone architecture by artistic choice. Anterior crest restored.'
    scene['generator']='source/generate.py';scene['asset_license']='CC-BY-4.0'
    low=min((o.matrix_world@v.co).z for o in col.objects if o.type=='MESH' for v in o.data.vertices)
    for o in col.objects:
        if o.type=='MESH':
            for v in o.data.vertices:v.co.z-=low
    bpy.context.view_layer.update();source=audit_source(col,6500)
    if source['errors']:raise RuntimeError(source['errors'])
    out.mkdir(parents=True,exist_ok=True);bpy.context.preferences.filepaths.save_version=0;scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'.'*1023;space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
      export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
      export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
      export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Required exporter properties unavailable')
    bpy.ops.export_scene.gltf(**opts);glb=audit_glb(out/'model.glb',6500,6,12);glb['file']='model.glb'
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][s][i]-expected[s][i]) for s in ['min','max'] for i in range(3))
    if glb['errors'] or delta>1e-4 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source/export audit failed: '+str(glb['errors']))
    if glb['bytes']>2000000:raise RuntimeError('Frozen byte budget exceeded')
    save(out/'build-report.json',{'asset_id':'guanlong','revision':'r001','blender':bpy.app.version_string,'seed':params['seed'],
      'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'source':source,'glb':glb,
      'source_export_bounds_max_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'crest_geometry':crest_record,'limb_measurements':measurements,
      'claim_scope':'Technical source and static GLB checks only. No independent visual, GPU or publication claim.'})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);build(a.output.resolve())
