# SPDX-License-Identifier: MIT
"""Original BAR 3877-11 preserved-skull interpretation, not a scan or restoration.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output DIR
Only relative source/params.json and source/deps dependencies are consumed.
"""
import argparse, hashlib, json, math, pathlib, random, shutil, sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, mesh_object, make_material, export_asset
P=json.loads((HERE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output',type=pathlib.Path,required=True); ap.add_argument('--clay',action='store_true'); args=ap.parse_args(argv)
OUT=args.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('kelenken',P['seed']); rng=random.Random(P['seed'])
M=[make_material('Fossil bone · '+str(i), '#999999' if args.clay else c,roughness=.91) for i,c in enumerate(P['palette'])]

def xyz(x,t,z): return (x,t-P['length_m']/2,z)
def triangles(quads):
    out=[]
    for i,q in enumerate(quads):
        if len(q)==4:
            a,b,c,d=q
            out.extend([(a,b,c),(a,c,d)] if i%2 else [(a,b,d),(b,c,d)])
        else: out.append(q)
    return out

def finish(name,v,f,colors=True):
    ob=mesh_object(name,v,triangles(f),M if colors else M[0],C)
    if colors:
        for face in ob.data.polygons:
            # Broad modest tone patches, not simulated engraved sutures.
            q=face.center
            phase=math.sin(q.x*83+q.y*32+q.z*55)+.28*math.sin(q.y*135-q.z*73)
            face.material_index=1 if phase>1.0 else 2 if phase<-.92 else 0
    ob['anatomy_scope']='Preserved upper skull only; simplified, no lower jaw'
    return ob

def shell(name,v,f,thickness,axis=(0,0,1),reference_faces=None):
    # Closed thin bone plate, preserving all explicitly omitted windows.
    n=len(v); u=Vector(axis); verts=list(v)+[tuple(Vector(p)-u*thickness) for p in v]
    faces=list(f)+[tuple(n+i for i in reversed(q)) for q in f]
    edges={}
    for q in f:
        for a,b in zip(q,q[1:]+q[:1]):
            key=tuple(sorted((a,b)))
            if key in edges: edges[key]=None
            else: edges[key]=(a,b)
    for e in edges.values():
        if e: a,b=e; faces.append((a,b,n+b,n+a))
    if reference_faces is not None:
        # Keep every unaffected diagonal from the prior mesh. Removing one local
        # quad must not flip the alternating triangulation across the entire roof.
        rf=list(reference_faces)+[tuple(n+i for i in reversed(q)) for q in reference_faces]
        re={}
        for q in reference_faces:
            for a,b in zip(q,q[1:]+q[:1]):
                key=tuple(sorted((a,b)))
                if key in re: re[key]=None
                else: re[key]=(a,b)
        for e in re.values():
            if e:a,b=e;rf.append((a,b,n+b,n+a))
        old_parity={tuple(sorted(q)):i%2 for i,q in enumerate(rf)}
        stable=[]
        for i,q in enumerate(faces):
            if len(q)!=4: stable.append(q);continue
            a,b,c,d=q;parity=old_parity.get(tuple(sorted(q)),i%2)
            stable.extend([(a,b,c),(a,c,d)] if parity else [(a,b,d),(b,c,d)])
        faces=stable
    return finish(name,verts,faces)

# Main rostrum and anterior palate. Longitudinal coordinates in meters from
# terminal hook; the sole measured dimensions are identified in params.json.
# Hollow shell has four real apertures, not dark decals.
# KEL-01: t is measured from the PREMAXILLARY TIP, never the rear end.
# The cited Table 1 distance directly drives this interval's center.
naris_center=P['nares_tip_distance_m']
naris_min=naris_center-P['naris_length_m']/2
naris_max=naris_center+P['naris_length_m']/2
ant_min,ant_max=P['antorbital_interval_m']
base_stations=P['working_rostrum_sections']
def section_at(t):
    for a,b in zip(base_stations,base_stations[1:]):
        if a[0]-1e-10<=t<=b[0]+1e-10:
            q=(t-a[0])/(b[0]-a[0]);return [t]+[a[k]+q*(b[k]-a[k]) for k in range(1,4)]
    raise ValueError('Landmark outside modeled rostrum')
station_t=sorted(set([q[0] for q in base_stations]+[naris_min,naris_center,naris_max,ant_min,ant_max]))
stations=[section_at(t) for t in station_t]
# cross section: lateral x factor and vertical fraction, clockwise from roof
ring=[(0,1),(.50,.98),(.84,.91),(.97,.84),(1,.73),(1,.59),(.98,.43),(.89,.21),(.65,.06),(0,0),(-.65,.06),(-.89,.21),(-.98,.43),(-1,.59),(-1,.73),(-.97,.84),(-.84,.91),(-.50,.98)]
nr=len(ring); outer=[]; inner=[]
for i,(t,w,lo,hi) in enumerate(stations):
    for j,(xf,zf) in enumerate(ring):
        wav=(math.sin(t*153+j*1.3)*.0013+math.sin(t*74-j*.9)*.0009)*min(1,w/.025)
        # Pointed, low caudodorsal nostrils instead of rectangular cutouts.
        if (abs(t-naris_min)<1e-8 or abs(t-naris_max)<1e-8) and j in [3,4,14,15]:
            zf=.79+(.012 if j in [3,15] else -.012)
        x=w*xf*(1+.025*math.sin(t*21+j))
        z=lo+(hi-lo)*zf+wav
        # Deliberate left/right taphonomic variation, strongest at caudal end.
        z+=(-.0028 if xf<0 else .0008)*min(1,t/.35)
        outer.append(xyz(x,t,z))
        inner.append(xyz(x*.82,t+.003 if i==0 else t,z+(hi+lo-2*z)*.12))
v=outer+inner; n=len(outer); surf=[]
for i in range(len(stations)-1):
    ta,tb=stations[i][0],stations[i+1][0]
    for j in range(nr):
        # Paired nares: exactly centered 0.404 m from the tip. Antorbital
        # windows lie immediately caudoventral, separated by the nasal/maxillary
        # bony row j=4 (right) / j=13 (left), then the short lacrimal wall.
        naris=(ta>=naris_min-1e-8 and tb<=naris_max+1e-8 and j in [3,14])
        antorbital=(ta>=ant_min-1e-8 and tb<=ant_max+1e-8 and j in [5,6,11,12])
        if naris or antorbital: continue
        a=i*nr+j;b=i*nr+(j+1)%nr;c=(i+1)*nr+(j+1)%nr;d=(i+1)*nr+j
        surf.append((a,b,c,d))
f=list(surf)+[tuple(n+k for k in reversed(q)) for q in surf]
edges={}
for q in surf:
    for a,b in zip(q,q[1:]+q[:1]):
        key=tuple(sorted((a,b)))
        if key in edges: edges[key]=None
        else: edges[key]=(a,b)
for e in edges.values():
    if e:
        a,b=e
        if not (a<nr and b<nr): f.append((a,b,n+b,n+a))
# Solid terminal tip, not an exposed hollow pipe.
f.append(tuple(reversed(range(nr))))
f.append(tuple(n+j for j in range(nr)))
rostrum=finish('01 elongated rostrum · true naris and antorbital windows',v,f)
for label,js in [('R',[3,4]),('L',[14,15])]:
    indices=[i*nr+j for i,(t,*_) in enumerate(stations) if naris_min-1e-8<=t<=naris_max+1e-8 for j in js]
    group=rostrum.vertex_groups.new(name='Naris margin '+label)
    group.add(indices,1.0,'REPLACE')
rostrum['nares_center_from_premaxillary_tip_m']=naris_center
rostrum['naris_interval_from_tip_m']=[naris_min,naris_max]
rostrum['antorbital_interval_from_tip_m']=[ant_min,ant_max]

# Broad, low, crushed posterior roof. Each transverse edge is irregular;
# it is not a mirrored pristine living-skull reconstruction.
roof_sections=[(.422,.057,.198),(.454,.066,.204),(.487,.076,.203),(.520,.088,.208),(.550,.107,.201),(.580,.1125,.202),(.610,.103,.193),(.640,.129,.202),(.667,.147,.207),(.692,.156,.208),(.716,.148,.194)]
v=[];nx=9
for i,(t,w,z) in enumerate(roof_sections):
    for j in range(nx):
        s=-1+2*j/(nx-1)
        shift=.004*math.sin(i*2.9+j*.72)*(abs(s)**3)
        xx=w*s+(.002*math.sin(i*2+j)*abs(s) if i not in [9] else 0)
        zz=z-.010*abs(s)**1.4+.005*math.sin(i*1.7+j*1.3)
        # Massive temporal attachment surfaces, subtly depressed, no incision.
        zz-=.008*math.exp(-((t-.645)/.045)**2)*math.exp(-((abs(s)-.55)/.23)**2)
        v.append(xyz(xx,min(.716,max(.422,t+shift)),zz))
f=[];roof_reference_faces=[]
for i in range(len(roof_sections)-1):
    for j in range(nx-1):
        # Discrete broken anterior left margin.
        if i==0 and j==0:continue
        a=i*nx+j;q=(a,a+1,a+nx+1,a+nx);roof_reference_faces.append(q)
        if not (i==0 and j==7): f.append(q)  # only the local right naris-clearance corner
shell('02 broad crushed frontal-parietal table',v,f,.023,reference_faces=roof_reference_faces)

# Low rectangular orbit is real empty space between roof, lacrimal, jugal,
# and broken postorbital projections. Jugal height is the measured 40 mm.
def bone_path(vectors,sides=8):
    verts=[]
    for i,(x,t,z,rx,rz) in enumerate(vectors):
        for j in range(sides):
            a=2*math.pi*j/sides
            verts.append(xyz(x+rx*math.cos(a),t,z+rz*math.sin(a)))
    f=[]
    for i in range(len(vectors)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;c=(i+1)*sides+(j+1)%sides;d=(i+1)*sides+j;f.append((a,b,c,d))
    f.append(tuple(reversed(range(sides))));f.append(tuple((len(vectors)-1)*sides+j for j in range(sides)))
    return verts,f

def combine(groups):
    verts=[];faces=[]
    for v,f in groups:
        n=len(verts);verts+=v;faces += [tuple(n+k for k in q) for q in f]
    return verts,faces
for s,label in [(1,'right'),(-1,'left')]:
    off=0 if s==1 else -.005
    jugal=[(s*.033,.393,.120+off,.012,.015),(s*.053,.431,.119+off,.011,.020),(s*.070,.470,.127+off,.008,.020),(s*.084,.505,.135+off,.008,.018),(s*.098,.540,.139+off,.008,.016),(s*.106,.566,.136+off,.010,.015),(s*.109,.579,.133+off,.007,.012)]
    # Preserved postorbital process does not bridge the entire orbit.
    post=[(s*.107,.559,.195+off,.012,.015),(s*.114,.570,.181+off,.012,.012),(s*.109,.582,.165+off,.009,.011),(s*.102,.587,.157+off,.005,.007)]
    # A short caudal zygomatic remnant, not a reconstructed quadrate.
    rem=[(s*.127,.659,.165+off,.016,.016),(s*.114,.636,.151+off,.013,.014),(s*.110,.620,.141+off,.008,.011)]
    # Bulky damaged posterior temporal walls retain the broad rear cranium;
    # the central posterior palate below remains absent.
    temporal=[(s*.106,.606,.172+off,.012,.022),(s*.118,.632,.155+off,.020,.043),(s*.128,.657,.152+off,.026,.049),(s*.128,.684,.151+off,.027,.053),(s*.123,.707,.160+off,.025,.037)]
    v,f=combine([bone_path(jugal),bone_path(post),bone_path(rem),bone_path(temporal,9)])
    finish('03 '+label+' jugal and broken orbital processes',v,f)

# Occipital table: the outer broken edge is asymmetric, and its genuine small
# triangular foramen magnum is framed by a ring of original low-poly geometry.
outline=[(0,.207),(.050,.205),(.098,.214),(.154,.191),(.148,.166),(.111,.145),(.081,.119),(.044,.078),(.010,.070),(-.028,.074),(-.069,.083),(-.092,.113),(-.120,.154),(-.156,.182),(-.132,.205),(-.071,.210)]
# Corresponding angular ring around a subtly blunted triangle.
hole=[(0,.151),(.005,.150),(.010,.142),(.013,.134),(.012,.129),(.008,.127),(.004,.126),(0,.126),(-.004,.126),(-.008,.127),(-.012,.129),(-.013,.133),(-.010,.141),(-.006,.148),(-.003,.151),(-.001,.152)]
v=[]
for j,(x,z) in enumerate(outline):v.append(xyz(x,.706+.006*math.sin(j*2.1),z))
for j,(x,z) in enumerate(hole):v.append(xyz(x,.710+.002*math.sin(j),z))
f=[(j,(j+1)%16,16+(j+1)%16,16+j) for j in range(16)]
shell('04 broken occipital table with foramen magnum',v,f,.020,axis=(0,1,0))

# Preserved left palatal and pterygoid remnants only. The wide posterior
# underside is deliberately not filled or mirrored.
v,f=bone_path([(-.020,.447,.100,.021,.009),(-.026,.477,.094,.018,.009),(-.035,.503,.088,.012,.007),(-.045,.530,.083,.007,.006),(-.041,.545,.079,.004,.004)],6)
finish('05 left palatal-pterygoid fragment only',v,f)
# Partial interorbital septum seen in the preserved fossil. Keep low and local
# so that the two main lateral orbits remain truly open and readable.
v=[xyz(-.005,.424,.113),xyz(.005,.426,.113),xyz(.006,.449,.145),xyz(.001,.475,.154),xyz(-.006,.497,.141),xyz(-.003,.477,.121)]
f=[(0,1,2),(0,2,3),(0,3,4),(0,4,5)]
shell('06 partial interorbital septum',v,f,.006,axis=(1,0,0))

# Preserve metrically cited length/width without claiming other estimated
# working dimensions as anatomical measurements. Scale each axis only once
# for the 716 mm long / 312 mm caudal-wide fossil envelope.
allv=[v for ob in C.objects if ob.type=='MESH' for v in ob.data.vertices]
minx=min(v.co.x for v in allv);maxx=max(v.co.x for v in allv);miny=min(v.co.y for v in allv);maxy=max(v.co.y for v in allv);minz=min(v.co.z for v in allv)
for v in allv:
    v.co.x=(v.co.x-(minx+maxx)/2)*P['caudal_width_m']/(maxx-minx)
    v.co.y=(v.co.y-(miny+maxy)/2)*P['length_m']/(maxy-miny)
    v.co.z-=minz
root=bpy.data.objects[C['asset_root']];root['specimen']='BAR 3877-11';root['scope']='Preserved upper skull only; no mandible; posterior palate absent except left fragment'
record=export_asset('kelenken',{'en':'Kelenken — preserved skull study','zh':'Kelenken（保存头骨化石研究）'},'fossils',C,metadata={'generator':'source/generate.py','specimen':'BAR 3877-11','reconstruction_type':'specimen','measurement_note':P['working_dimensions_note'],'estimated_dimensions':True},output_root=OUT/'private'/'build-stage',render=False,max_triangles=6500,max_materials=5,max_primitives=24,diagnostics=False)
stage=OUT/'private'/'build-stage'/'kelenken'
for old,new in [('kelenken.glb','model.glb'),('kelenken.blend','model.blend')]:shutil.copy2(stage/old,OUT/new)
evidence=OUT/'qa'/'evidence';evidence.mkdir(parents=True,exist_ok=True)
qa=json.loads((stage/'qa.json').read_text());(evidence/'geometry.json').write_text(json.dumps(qa,indent=2)+'\n')
record.update({'glb':'model.glb','blend':'model.blend','preview':'preview.png','generator_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'exporter_version':'4.3.47','consuming_threejs_version':'0.180.0','threejs_runtime':'NOT_RUN','model_origin':'Floor contact of terminal hook; no support exported','clay_diagnostic':args.clay})
(evidence/'build.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
print('BUILD_OK '+json.dumps({'glb_sha256':record['sha256']['glb'],'triangles':record['triangles'],'bytes':record['glb_bytes']}))
