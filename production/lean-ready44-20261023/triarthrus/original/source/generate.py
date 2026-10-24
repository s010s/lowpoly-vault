# SPDX-License-Identifier: MIT
"""Original deterministic complete Triarthrus eatoni reconstruction.
Run Blender with --python source/generate.py -- --output OUTPUT_DIRECTORY.
Planar size derives from a same-species reconstruction, not measured YPM 219.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((ROOT/'params.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT.parent)
A=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=A.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene(P['asset_id'],seed=P['seed'])
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
palette=[('Dorsal matte olive umber','#706C50'),('Raised axial cuticle','#858064'),('Walking limbs and antennae','#82765C'),('Subpleural gill blades','#A49A79'),('Small lateral eyes','#343C32'),('Ventral soft cuticle','#746C57')]
materials=[make_material(n,c,roughness=.83 if i!=4 else .6) for i,(n,c) in enumerate(palette)]
class Part:
    def __init__(self,name,mi):self.name=name;self.mi=mi;self.v=[];self.f=[];self.groups={}
    def add(self,label,vs,fs):
        k=len(self.v);self.v.extend([tuple(v) for v in vs]);self.f.extend([tuple(k+i for i in f) for f in fs]);self.groups.setdefault(label,[]).extend(range(k,k+len(vs)))
    def finish(self):
        o=mesh_object(self.name,self.v,self.f,materials[self.mi],C)
        for label,ids in self.groups.items():o.vertex_groups.new(name=label).add(ids,1,'REPLACE')
        o['editing']='Named semantic vertex groups; closed authored profile pieces, no negative scales'
        return o
shell=Part('Cephalon 14 tergites and pygidium',0)
axis=Part('Glabella axial rings and marginal trim',1)
legs=Part('Paired antennae and jointed walking branches',2)
gills=Part('Upper limb shafts with combs of gill filaments',3)
eyes=Part('Paired lateral eyes',4)
under=Part('Ventral bases hypostome and limb connections',5)
def tube(part,label,points,radii,sides=6,flatten=1):
    ps=[Vector(p) for p in points];vs=[]
    for i,p in enumerate(ps):
        t=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized();ref=Vector((0,0,1))
        if abs(t.dot(ref))>.95:ref=Vector((1,0,0))
        u=t.cross(ref).normalized();v=t.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides;vs.append(p+radii[i]*(math.cos(a)*u+flatten*math.sin(a)*v))
    fs=[tuple(range(sides-1,-1,-1))]
    for i in range(len(ps)-1):
        for j in range(sides):fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    fs.append(tuple((len(ps)-1)*sides+j for j in range(sides)));part.add(label,vs,fs)
def ellipsoid(part,label,c,r,segments=16,rings=6):
    vs=[(c[0],c[1],c[2]+r[2])]
    for i in range(1,rings):
        a=math.pi*i/rings
        for j in range(segments):
            b=2*math.pi*j/segments;vs.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]+r[2]*math.cos(a)))
    end=len(vs);vs.append((c[0],c[1],c[2]-r[2]));fs=[]
    for j in range(segments):fs.append((0,1+j,1+(j+1)%segments))
    for i in range(rings-2):
        for j in range(segments):
            a=1+i*segments;fs.append((a+j,a+segments+j,a+segments+(j+1)%segments,a+(j+1)%segments))
    a=1+(rings-2)*segments
    for j in range(segments):fs.append((a+j,end,a+(j+1)%segments))
    part.add(label,vs,fs)
def plate(part,label,outline,center,edgez,peakz,thick,rings=5):
    """Closed concentric custom dome, not an untouched sphere primitive."""
    vs=[(center[0],center[1],peakz)];n=len(outline)
    for k in range(1,rings+1):
        r=k/rings;z=edgez+(peakz-edgez)*(1-r*r)**.72
        for x,y in outline:vs.append((center[0]+r*(x-center[0]),center[1]+r*(y-center[1]),z))
    bottom=len(vs);vs.append((center[0],center[1],edgez-thick));fs=[]
    for j in range(n):fs.append((0,1+j,1+(j+1)%n))
    for k in range(rings-1):
        a=1+k*n;b=a+n
        for j in range(n):fs.append((a+j,b+j,b+(j+1)%n,a+(j+1)%n))
    a=1+(rings-1)*n
    for j in range(n):fs.append((a+j,bottom,a+(j+1)%n))
    part.add(label,vs,fs)
# Broad rounded cephalon, short rounded genal corners, no long spines.
outline=[]
for j in range(25):
    a=-math.pi/2+math.pi*j/24;outline.append((.007*math.sin(a),-.0045-.009*math.cos(a)))
outline +=[(.0058,-.00425),(.004,-.00435),(.002,-.0045),(0,-.00455),(-.002,-.0045),(-.004,-.00435),(-.0058,-.00425)]
plate(shell,'Cephalon',outline,(0,-.0081),.00345,.00545,.00035)
tube(axis,'Cephalic anterior border',[(x*.97,-.0045+(y+.0045)*.97,.00362) for x,y in outline[:25]],[.00016]*25,6)
ellipsoid(axis,'Elongate glabella',(0,-.0084,.00502),(.00205,.00375,.00095),20,8)
for i,y in enumerate([-.00615,-.0070,-.00785]):
    for s in [-1,1]:tube(shell,'Glabellar furrow '+str(i),[(s*.001,y+.0001,.00568),(s*.00155,y,.00555),(s*.00186,y-.0001,.00530)],[.000085,.000095,.00007],5)
for s in [-1,1]:
    ellipsoid(eyes,'Eye '+str(s),(s*.00365,-.0081,.00506),(.00040,.00103,.00032),12,6)
    tube(axis,'Palpebral ridge '+str(s),[(s*.00342,-.00925,.00492),(s*.00316,-.00845,.00521),(s*.00325,-.00755,.00505)],[.00013,.00018,.00013],6)
ellipsoid(under,'Hypostome',(0,-.01015,.00295),(.0012,.0015,.0003),14,6)
# Fourteen overlapping roof profiles remain distinct at every articulation.
segment_positions=[]
for i in range(14):
    t=i/13;y=-.00385+i*.001055;w=.0069*(1-.48*t**1.6);segment_positions.append((y,w))
    cross=[(-1,.00340),(-.84,.00372),(-.53,.00415),(-.32,.00418),(-.245,.00465),(-.13,.00503),(0,.00514),(.13,.00503),(.245,.00465),(.32,.00418),(.53,.00415),(.84,.00372),(1,.00340)]
    vs=[]
    for row in range(4):
        for x,z in cross:
            sweep=.00055*abs(x)**1.7;dy=[-.00045,-.00012,.00029,.00042][row];zz=z-.00058*t+([-.00013,.00012,.00004,-.00018][row]);vs.append((x*w,y+sweep+dy,zz))
    n=len(cross);fs=[]
    for row in range(3):
        for j in range(n-1):fs.append((row*n+j,row*n+j+1,(row+1)*n+j+1,(row+1)*n+j))
    boundary=list(range(n))+[row*n+n-1 for row in range(1,4)]+list(range(4*n-2,3*n-1,-1))+[row*n for row in [2,1]]
    b=len(vs);vs.extend([(vs[j][0],vs[j][1],vs[j][2]-.00025) for j in boundary])
    for j,k0 in enumerate(boundary):fs.append((k0,b+j,b+(j+1)%len(boundary),boundary[(j+1)%len(boundary)]))
    fs.append(tuple(b+j for j in range(len(boundary)-1,-1,-1)));shell.add('Thoracic tergite %02d'%(i+1),vs,fs)
    tube(axis,'Axial ring %02d'%(i+1),[(-.00145*(1-.2*t),y-.00025,.00477-.00058*t),(0,y-.00025,.00518-.00058*t),(.00145*(1-.2*t),y-.00025,.00477-.00058*t)],[.00014]*3,6)
tail_outline=[(.00335*math.cos(2*math.pi*j/24),.01155+.00195*math.sin(2*math.pi*j/24)) for j in range(24)]
plate(shell,'Small rounded pygidium',tail_outline,(0,.0114),.0029,.00432,.00025,4)
ellipsoid(axis,'Pygidial axial lobe',(0,.01105,.00395),(.00135,.00165,.00052),14,6)
for i in range(3):
    y=.01025+i*.00053;tube(shell,'Pygidial axial furrow '+str(i),[(-.00095,y,.00420),(0,y,.00446),(.00095,y,.00420)],[.000075]*3,5)
# Ventral axial soft trunk joins bases to the roof. Thickness and cross-section
# are explicitly inferred, not a preserved fossil measurement.
tube(under,'Continuous ventral axial body',[(0,-.0116,.0038),(0,-.009,.0038),(0,-.0044,.0038),(0,.002,.0036),(0,.0085,.0033),(0,.0116,.0030),(0,.0127,.0029)],[.0008,.0017,.0017,.0016,.0013,.0009,.0004],10,.72)
# One pair of tapered antennae with articulated rings.
for s in [-1,1]:
    points=[];radii=[]
    for i in range(19):
        t=i/18;points.append((s*(.00195+.00165*t+.00038*math.sin(math.pi*t)),-.0117-.0062*t,.00305+.00028*math.sin(math.pi*t)));radii.append(.00016*(1-.69*t))
    tube(legs,'Antenna '+str(s),points,radii,6)
    for i in range(2,18):
        p=Vector(points[i]);q=Vector(points[i+1]);tangent=(q-p).normalized();tube(axis,'Antennal annulus %s %02d'%(s,i),[p-tangent*.000035,p+tangent*.000035],[radii[i]*1.09]*2,6)
limb_rows=[('Cephalic %02d'%(i+1),y,w,k) for i,(y,w,k) in enumerate([(-.0094,.0054,.92),(-.0075,.0064,1),(-.00565,.0068,1)])]
limb_rows += [('Thoracic %02d'%(i+1),y,w,1-.25*i/13) for i,(y,w) in enumerate(segment_positions)]
limb_rows += [('Pygidial schematic %02d'%(i+1),.01065+i*.00058,.00325-i*.00048,.55-i*.09) for i in range(4)]
for name,y,w,k in limb_rows:
    for s in [-1,1]:
        label=name+(' L' if s<0 else ' R');rootx=.00115*max(.55,k);basez=.0028-.00035*(1-k)
        p=[(s*rootx,y,basez),(s*(rootx+.00105*k),y+.0001,basez-.00018),(s*(w*.70),y+.00025,.00235*k),(s*(w+.00040*k),y+.00048,.00188*k),(s*(w+.00105*k),y+.0008,.00113*k),(s*(w+.00124*k),y+.0010,.00048*k),(s*(w+.00130*k),y+.00110,.00010*k),(s*(w+.00149*k),y+.00113,.000035)]
        rr=[.00032*k,.00031*k,.00026*k,.00022*k,.00017*k,.00013*k,.000085*k,.00004];tube(legs,label+' walking branch',p,[max(.00004,r) for r in rr],6)
        ellipsoid(under,label+' limb base',(s*rootx,y,basez),(.00045*k,.00033*k,.00035*k),8,4)
        for j in range(2):tube(under,label+' feeding spine '+str(j),[(s*(rootx-.00016*k),y+(j-.5)*.00023,basez-.00012),(s*(rootx-.00046*k),y+(j-.5)*.00023,basez-.00052*k)],[max(.000055,.00011*k),.000035],5)
        # Proposed connection after Hou Fig4C, not directly preserved YPM219 fact.
        start=Vector((s*(rootx+.0002*k),y-.00010,basez+.00050));end=Vector((s*(w+.00018*k),y+.00028,basez+.00042))
        tube(gills,label+' upper shaft',[start,(start+end)/2+Vector((0,0,.00010)),end],[max(.00008,.00016*k),max(.00008,.000145*k),.00007],6)
        count=12 if k>.64 else 8
        for j in range(count):
            t=.12+.84*j/(count-1);p0=start.lerp(end,t);length=(.0011+.00055*math.sin(math.pi*t))*max(.55,k);p1=p0+Vector((s*.00008*k,length*.45,-.00029*k));p2=p0+Vector((s*.00035*k,length,-.00078*k))
            tube(gills,label+' gill filament %02d'%(j+1),[p0,p1,p2],[max(.000055,.000085*k),max(.000055,.000078*k),.000045],5,.55)
objects=[p.finish() for p in [shell,axis,legs,gills,eyes,under]]
zmin=min(v.co.z for o in objects for v in o.data.vertices)
for o in objects:
    for v in o.data.vertices:v.co.z-=zmin
    o.data.update()
root=bpy.data.objects[C['asset_root']];root['anatomy']='14 thoracic segments; 3 cephalic, 14 thoracic, 4 schematic pygidial limb pairs; both branches';root['scientific_limits']='27 mm reconstructed planar body estimate, not YPM219 measurement. Proposed upper-branch connection; living color unknown.'
scene['asset_license']='CC-BY-4.0';scene['asset_author']='Leon Made This / s010s'
source=audit_source(C,max_triangles=40000)
if source['errors']:raise RuntimeError('Source audit: '+repr(source['errors']))
# Startup workspaces can retain an absolute File Browser directory. Clear its
# entire fixed string storage before saving, then use a portable relative path.
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'/'*1023
                space.params.directory=b'//'
scene.render.filepath='//';bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Unsupported exporter options')
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(OUT/'model.glb',40000,6,8)
if glb['errors']:raise RuntimeError('GLB audit: '+repr(glb['errors']))
glb['file']='model.glb'
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][q][i]-expected[q][i]) for q in ['min','max'] for i in range(3))
assert delta<1e-7 and source['triangles']==glb['scene_triangles'] and glb['bytes']<8388608
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'status':'PASS','scope':'Source geometry and static exported geometry, not independent visual or GPU acceptance','asset_id':'triarthrus','revision':'r001','blender_version':bpy.app.version_string,'generator_sha256':sha(ROOT/'generate.py'),'params_sha256':sha(ROOT/'params.json'),'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'source':source,'glb':glb,'source_export_bounds_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'anatomy_counts':{'thoracic_tergites':14,'paired_antennae':1,'cephalic_biramous_pairs':3,'thoracic_biramous_pairs':14,'pygidial_biramous_pairs_schematic':4},'palette_srgb':[{'name':n,'color':c} for n,c in palette],'foot_contact_blender_z_m':0,'texture_images':0,'threejs_target':'0.180.0','gpu':'UNKNOWN','scene':'UNKNOWN','user':'UNKNOWN','deployed':'UNKNOWN'}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'result':'BUILT','triangles':glb['scene_triangles'],'glb_sha256':report['glb_sha256'],'semantic_sha256':glb['semantic_sha256']}))
