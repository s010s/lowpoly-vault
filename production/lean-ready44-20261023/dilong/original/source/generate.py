#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Dilong genus-level living reconstruction, not a specimen scan.
Run: blender -b -t 2 --python source/generate.py -- --output .
All local dependencies are relative and declared in dependencies.json.
"""
from pathlib import Path
import argparse,hashlib,json,math,random,sys
import bpy
from mathutils import Vector
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

def loft_y(part,rows,n=12,belly=False):
    v=[];f=[];mi=[]
    for y,z,rx,rz in rows:
        for j in range(n):
            a=2*math.pi*j/n;v.append((rx*math.cos(a),y,z+rz*math.sin(a)))
    f.append(tuple(range(n-1,-1,-1)));mi.append(0)
    for k in range(len(rows)-1):
        for j in range(n):
            f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if belly and math.sin(2*math.pi*(j+.5)/n)<-.5 else 0)
    f.append(tuple((len(rows)-1)*n+j for j in range(n)));mi.append(0);part.add(v,f,mi)

def tube(part,rows,n=8):
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
    f.append(tuple((len(rows)-1)*n+j for j in range(n)));part.add(v,f)

def ellipsoid(part,c,r,n=8,l=5):
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
    part.add(v,f)

def strand(part,a,b,r=.0015):
    a,b=Vector(a),Vector(b);t=(b-a).normalized();u=t.cross(Vector((1,0,0)))
    if u.length<.01:u=t.cross(Vector((0,1,0)))
    u.normalize();w=t.cross(u).normalized()
    v=[tuple(a+u*r),tuple(a+w*r),tuple(a-u*r),tuple(a-w*r),tuple(b)]
    part.add(v,[(0,3,2,1),(0,1,4),(1,2,4),(2,3,4),(3,0,4)])

def tuft(part,p,delta,width=.0017,branch=True):
    p=Vector(p);d=Vector(delta);strand(part,p,p+d,width)
    if branch:
        j=p+d*.45
        for s in [-1,1]:strand(part,j,p+d*random.uniform(.82,1.06)+Vector((s*.008,random.uniform(-.003,.004),random.uniform(-.003,.002))),width*.68)

def build(out):
    params=json.loads((HERE/'params.json').read_text());col=setup_scene('dilong',params['seed']);mats={k:make_material(k,v,.86) for k,v in params['palette'].items()}
    # Continuous axial loft: gently flexed neck, narrow trunk and tapering balancing tail.
    body=Part();rows=[(-.474,.804,.037,.053),(-.444,.785,.039,.055),(-.410,.738,.040,.058),(-.370,.689,.044,.067),
      (-.320,.643,.056,.085),(-.260,.614,.074,.111),(-.180,.602,.092,.126),(-.085,.607,.104,.132),
      (.015,.611,.102,.129),(.105,.611,.088,.108),(.185,.603,.066,.083),(.260,.593,.048,.057),
      (.350,.582,.036,.039),(.460,.568,.027,.029),(.575,.553,.021,.022),(.690,.546,.015,.016),
      (.790,.550,.009,.010),(.875,.558,.004,.005),(.920,.565,.001,.0015)]
    loft_y(body,rows,14,True);body.object('axial-neck-trunk-tail',[mats['body'],mats['belly']],col)
    # Low, lightly constructed skull and tapered snout, not the deep skull of a derived tyrannosaur.
    head=Part();loft_y(head,[(-.680,.829,.019,.027),(-.653,.837,.030,.037),(-.610,.848,.037,.046),
      (-.560,.861,.045,.055),(-.515,.866,.050,.059),(-.473,.859,.046,.057),(-.446,.843,.032,.043)],12,True)
    # A modest Y-like nasal/lacrimal ridge, branching at the posterior nasal region.
    tube(head,[(0,-.634,.873,.0035,.003),(0,-.593,.895,.004,.004),(0,-.552,.915,.005,.004)],6)
    for s in [-1,1]:tube(head,[(0,-.552,.915,.005,.004),(s*.020,-.522,.925,.004,.004),(s*.034,-.492,.917,.003,.003)],6)
    head.object('low-skull-and-modest-y-ridge',[mats['body'],mats['belly']],col)
    dark=Part();iris=Part()
    for side,label in [(-1,'left'),(1,'right')]:
        dy=.014 if side<0 else -.014
        # Flexed hindlimb: forward femur, backward tibia, long distal metatarsal region.
        leg=Part();tube(leg,[(side*.076,.080+dy,.610,.052,.065),(side*.104,.034+dy,.530,.052,.064),
          (side*.111,-.025+dy,.405,.037,.043),(side*.107,.030+dy,.315,.026,.030),
          (side*.103,.133+dy,.209,.018,.021),(side*.103,.107+dy,.057,.014,.016)],10)
        ellipsoid(leg,(side*.103,.085+dy,.041),(.025,.045,.031),8,4)
        for j in [-1,0,1]:
            x=side*.103+j*.019;end_y=-.051+abs(j)*.026+dy
            tube(leg,[(side*.103+j*.013,.073+dy,.032,.009,.011),(x,.017+dy,.020,.008,.009),(x+j*.008,end_y,.012,.006,.007)],6)
            tube(dark,[(x+j*.008,end_y,.013,.0064,.006),(x+j*.009,end_y-.018,.008,.004,.0038),(x+j*.010,end_y-.026,.006,.001,.001)],5)
        # Small elevated hallux, separate from the load-bearing three toes.
        tube(leg,[(side*.091,.096+dy,.075,.006,.007),(side*.087,.137+dy,.058,.004,.004)],6)
        tube(dark,[(side*.087,.137+dy,.058,.0045,.004),(side*.084,.151+dy,.047,.001,.001)],5)
        leg.object('hindlimb-'+label,mats['body'],col)
        # Humerus remains more than half femur length; arms hang free of chest.
        arm=Part();tube(arm,[(side*.065,-.251,.635,.026,.029),(side*.101,-.231,.575,.021,.025),
          (side*.136,-.206,.502,.017,.021),(side*.145,-.270,.458,.012,.014),
          (side*.143,-.329,.412,.009,.012),(side*.144,-.354,.386,.009,.018)],9)
        # Palm lies parasagittally: fingers fan in Y/Z, never a pronated palm-down rake.
        ellipsoid(arm,(side*.144,-.352,.390),(.009,.026,.022),8,4)
        digits=[(-.374,.391,-.414,.371,-.426,.350,.007),
                (-.358,.378,-.398,.337,-.409,.311,.0075),
                (-.341,.374,-.369,.330,-.372,.300,.0048)]
        for i,(y0,z0,y1,z1,y2,z2,r) in enumerate(digits):
            xx=side*(.145+.0015*(i-1));tube(arm,[(xx,y0,z0,r,r*1.1),(xx,y1,z1,r*.78,r*.85),(xx,y2,z2,r*.58,r*.65)],6)
            tube(dark,[(xx,y2,z2,r*.68,r*.70),(xx,y2-.010,z2-.010,r*.46,r*.45),(xx,y2-.006,z2-.021,.001,.001)],5)
        arm.object('long-three-fingered-forelimb-'+label,mats['body'],col)
        ellipsoid(dark,(side*.0472,-.505,.885),(.0046,.016,.016),10,5)
        ellipsoid(iris,(side*.0510,-.507,.886),(.0027,.0105,.0105),10,5)
        ellipsoid(dark,(side*.0532,-.510,.886),(.0015,.004,.006),8,4)
        ellipsoid(dark,(side*.029,-.647,.851),(.002,.005,.003),8,4)
        # Closed mouth seam, not an oversized tooth display.
        tube(dark,[(side*.020,-.677,.815,.001,.001),(side*.033,-.637,.813,.0013,.0013),
          (side*.041,-.590,.817,.0014,.0014),(side*.046,-.540,.820,.0014,.0014),(side*.046,-.495,.826,.001,.001)],5)
    dark.object('claws-pupils-nares-mouth',mats['keratin'],col);iris.object('irises',mats['iris'],col)
    fil=Part()
    # Branching filament geometry represents integument, never broad aerodynamic feathers.
    # Distribution over body/neck is inferred; primary direct preservation is tail and jaw.
    for k in range(1,len(rows)-1):
        y,z,rx,rz=rows[k]
        for j in [-1,0,1]:
            phi=math.pi/2+j*.48;px=rx*math.cos(phi);pz=z+rz*math.sin(phi)
            length=.025 if y<.3 else .025+.008*math.sin(k*.9)
            tuft(fil,(px,y,pz-.002),(j*.004,length*.85,length*.80),.0016 if y<.3 else .00125)
    # Interleaved smaller tufts interrupt the long dorsal gaps without becoming a crest.
    for k in range(2,16):
        a,b=rows[k],rows[k+1];y,z,rx,rz=[(a[i]+b[i])/2 for i in range(4)]
        for j in [-1,0,1]:
            phi=math.pi/2+j*.53
            tuft(fil,(rx*math.cos(phi),y,z+rz*math.sin(phi)-.002),(j*.005,.018,.017),.0013)
    # Side and nape tufts follow the surface, retaining a fine shaggy silhouette.
    for side in [-1,1]:
        for k in range(3,11):
            y,z,rx,rz=rows[k]
            for sign in [-1,1]:
                tuft(fil,(side*rx*.91,y-.008,z+sign*rz*.40),(side*.013,.024,sign*.009),.0015)
        for k in range(4):
            y=-.507+k*.012;tuft(fil,(side*.037,y,.823),(side*.008,.018,-.020),.0012)
        # Distal-tail traces illustrated in Fig3 make an oblique 30–45-degree fringe.
        for k in range(7):
            y=.55+k*.043;rz=.023-(y-.55)*.058
            tuft(fil,(side*max(.004,rz*.80),y,.551+(.007 if y>.72 else 0)),(side*.012,.026,.021),.0012)
    fil.object('branched-filament-covering-inferred-distribution',mats['filaments'],col)
    bpy.context.scene['reconstruction_scope']='V14243 skeletal anchor; integument V11579 provisionally referred and potentially another close Dilong species. Full-body filament coverage, colour and pose inferred.'
    bpy.context.scene['scale_basis']='1.6 m estimated total length for V14243; not a measured complete adult.'
    bpy.context.scene['generator']='source/generate.py';bpy.context.scene['asset_license']='CC-BY-4.0'
    # Foot-contact plane is the origin; metric length is never normalized for display.
    low=min((o.matrix_world@v.co).z for o in col.objects if o.type=='MESH' for v in o.data.vertices)
    for o in col.objects:
        if o.type=='MESH':
            for v in o.data.vertices:v.co.z-=low
    bpy.context.view_layer.update();source=audit_source(col,6500)
    if source['errors']:raise RuntimeError(source['errors'])
    out.mkdir(parents=True,exist_ok=True);bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.filepath='//renders/'
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
    save(out/'build-report.json',{'asset_id':'dilong','revision':'r001','blender':bpy.app.version_string,'seed':params['seed'],
      'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'source':source,'glb':glb,
      'source_export_bounds_max_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},
      'claim_scope':'Technical source and static GLB checks only. No independent visual, GPU or publication claim.'})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);build(a.output.resolve())
