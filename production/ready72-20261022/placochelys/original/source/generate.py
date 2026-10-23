# SPDX-License-Identifier: MIT
"""Placochelys placodonta: original deterministic low-poly reconstruction.
Run: blender -b -t 2 --python source/generate.py -- --out /path --mode build
Modes: build, gray, final. All runtime dependencies vendored under source/deps.
No photograph is loaded, embedded, traced, or required for regeneration.
"""
from pathlib import Path
import sys, json, math, hashlib, shutil, argparse
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE/'deps'))
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from asset_common import setup_scene, make_material, mesh_object, export_asset, render_previews
P = json.loads((SOURCE/'params.json').read_text())
args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); ap.add_argument('--mode',choices=['build','gray','final'],default='build')
a=ap.parse_args(args); OUT=Path(a.out).resolve(); OUT.mkdir(parents=True,exist_ok=True)
def write(p,obj): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

# Each semantic object may contain intentional overlapping closed anatomical solids.
class Part:
    def __init__(self,name,mats): self.name=name; self.mats=mats; self.v=[];self.f=[];self.mi=[];self.groups=[]
    def add(self,verts,faces,mi=0,label=None):
        off=len(self.v);self.v.extend(verts);self.f.extend(tuple(off+i for i in f) for f in faces);self.mi.extend([mi]*len(faces))
        if label:self.groups.append((label,list(range(off,len(self.v)))))
    def obj(self,col):
        o=mesh_object(self.name,self.v,self.f,self.mats,col)
        for p,m in zip(o.data.polygons,self.mi):p.material_index=m
        for name,ids in self.groups:o.vertex_groups.new(name=name).add(ids,1,'REPLACE')
        return o

def loft(part,sections,n=12,mi=0,label=None):
    # World-Y cross sections: (y,centerX,centerZ,radiusX,radiusZ), flat-end capped.
    vs=[];fs=[]
    for y,x,z,rx,rz in sections:
        vs += [(x+rx*math.cos(2*math.pi*j/n),y,z+rz*math.sin(2*math.pi*j/n)) for j in range(n)]
    for k in range(len(sections)-1):
        for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    fs += [tuple(range(n-1,-1,-1)),tuple((len(sections)-1)*n+j for j in range(n))]
    part.add(vs,fs,mi,label)

def tube(part,points,radii,n=8,mi=0,label=None):
    # Tangent-frame elliptical loft, explicit perpendicular axes.
    vs=[];fs=[];ps=[Vector(p) for p in points]
    for i,p in enumerate(ps):
        tangent=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized()
        u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u).normalized()
        for j in range(n):
            t=2*math.pi*j/n;vs.append(tuple(p+u*(radii[i][0]*math.cos(t))+v*(radii[i][1]*math.sin(t))))
    for k in range(len(ps)-1):
        for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    fs += [tuple(range(n-1,-1,-1)),tuple((len(ps)-1)*n+j for j in range(n))]
    part.add(vs,fs,mi,label)

def lens(part,center,scales,n=10,rings=5,mi=0,label=None):
    # Pole-aware ellipsoid; no duplicate zero-area pole vertices.
    x,y,z=center;rx,ry,rz=scales;vs=[(x,y,z+rz)];fs=[]
    for k in range(1,rings):
        phi=math.pi*k/rings
        vs += [(x+rx*math.sin(phi)*math.cos(j*2*math.pi/n),y+ry*math.sin(phi)*math.sin(j*2*math.pi/n),z+rz*math.cos(phi)) for j in range(n)]
    vs.append((x,y,z-rz));bottom=len(vs)-1
    for j in range(n):fs.append((0,1+j,1+(j+1)%n))
    for k in range(rings-2):
        for j in range(n):fs.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
    for j in range(n):fs.append((bottom,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
    part.add(vs,fs,mi,label)

def build():
    col=setup_scene('placochelys',seed=P['seed'])
    mats={k:make_material(k,c,roughness=.88) for k,c in P['palette_srgb'].items()}
    shell=Part('Carapace_low_oval',[mats['armour']])
    skin=Part('Body_neck_four_limbs_tail',[mats['skin'],mats['underside']])
    head=Part('Broad_skull_and_pointed_rostrum',[mats['skin'],mats['underside']])
    nodes=Part('Subtle_polygonal_osteoderms',[mats['scute'],mats['armour']])
    trim=Part('Eyes_nostrils_and_closed_mouth',[mats['dark']])
    rims=Part('Orbital_rims',[mats['scute']])
    # Thin low oval cuirass: reconstructed 0.49 x 0.35 m outline, ratio 1.4.
    # Four radial rings with an almost level crown. Never a hemispherical turtle dome.
    n=32;vs=[(0,-.005,.173)];fs=[]
    profiles=[(.27,.172),(.55,.165),(.79,.145),(1,.105),(.98,.088)]
    for r,z in profiles:
        for j in range(n):
            t=2*math.pi*j/n;vs.append((.175*r*math.cos(t),-.005+.245*r*math.sin(t),z+.003*math.cos(2*t)))
    for j in range(n):fs.append((0,1+j,1+(j+1)%n))
    for k in range(len(profiles)-1):
        for j in range(n):fs.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
    fs.append(tuple(1+(len(profiles)-1)*n+j for j in range(n-1,-1,-1)))
    shell.add(vs,fs,label='Low_elliptical_armour')
    loft(skin,[(-.25,0,.085,.032,.022),(-.22,0,.080,.104,.035),(-.12,0,.078,.161,.038),(.06,0,.075,.163,.036),(.19,0,.075,.111,.032),(.235,0,.078,.03,.018)],16,label='Body_below_armour')
    # Slight visible cream-brown belly, flattened rather than a modern turtle plastron.
    lens(skin,(0,-.005,.061),(.145,.220,.017),n=20,rings=4,mi=1,label='Soft_belly')
    loft(skin,[(-.315,0,.097,.039,.025),(-.285,0,.096,.042,.027),(-.254,0,.091,.049,.029),(-.22,0,.083,.064,.03)],12,label='Short_neck')
    # 15 cm skull. The last anterior 4 cm form a narrow, edentulous taper.
    loft(head,[(-.43,0,.087,.006,.009),(-.416,0,.09,.012,.012),(-.39,0,.098,.025,.016),(-.36,0,.106,.045,.024),(-.327,0,.107,.063,.029),(-.296,0,.103,.073,.027),(-.28,0,.100,.048,.023)],12,label='Skull_0p15m')
    loft(head,[(-.427,0,.077,.005,.003),(-.400,0,.077,.017,.006),(-.36,0,.078,.036,.009),(-.323,0,.080,.052,.012),(-.287,0,.082,.042,.012)],10,mi=1,label='Closed_lower_jaw_posterior_teeth_not_exposed')
    # Posterolateral corners of skull are represented by profile widening, not speculative horns.
    for s in (-1,1):
        lens(rims,(s*.043,-.354,.121),(.013,.015,.004),10,4,label='Orbital_rim_'+str(s))
        lens(trim,(s*.047,-.357,.124),(.008,.009,.0038),10,4,label='Eye_'+str(s))
        lens(trim,(s*.010,-.409,.100),(.0031,.0042,.0018),8,4,label='Nostril_'+str(s))
        tube(trim,[(s*.007,-.428,.079),(s*.015,-.404,.079),(s*.030,-.378,.080),(s*.046,-.351,.082),(s*.057,-.322,.084)],[(.0012,.0012)]*5,n=6,label='Closed_mouth_line_'+str(s))
    # Short, bent, laterally splayed limbs. Five shallow terminal scallops on each
    # foot indicate conservative webbing; limb form remains a reconstruction.
    for s in (-1,1):
        for fore in (True,False):
            y0=-.165 if fore else .145; y1=-.19 if fore else .185
            pts=[(s*.125,y0,.078),(s*.172,y0-.01 if fore else y0+.01,.06),(s*.218,y1,.037),(s*.245,y1-.017 if fore else y1+.025,.023)]
            tube(skin,pts,[(.039,.027),(.034,.024),(.026,.018),(.019,.011)],10,label=('Fore' if fore else 'Hind')+'_limb_'+str(s))
            cy=y1-.025 if fore else y1+.035;cx=s*.250
            # Outline is local foot XY; +u is distal (outward), five muted lobes.
            outline=[(-.020,-.018),(-.003,-.032),(.018,-.038),(.034,-.032),(.030,-.024),(.041,-.018),(.037,-.009),(.046,0),(.038,.010),(.042,.020),(.030,.023),(.031,.033),(.015,.034),(-.004,.024),(-.019,.016)]
            vs=[]
            # Beveled soft foot profile, not a flat extruded slab.
            for z,scale in ((.009,.84),(.016,1.0),(.025,.76)):
                vs.extend((cx+s*(.012+(u-.012)*scale),cy+v*scale,z) for u,v in outline)
            nn=len(outline);fs=[tuple(range(nn-1,-1,-1)),tuple(2*nn+j for j in range(nn))]
            for k in (0,1):
                fs += [(k*nn+j,k*nn+(j+1)%nn,(k+1)*nn+(j+1)%nn,(k+1)*nn+j) for j in range(nn)]
            skin.add(vs,fs,label=('Fore' if fore else 'Hind')+'_five_digit_web_'+str(s))
    tube(skin,[(0,.197,.077),(.003,.252,.074),(.011,.312,.067),(.019,.375,.055),(.018,.431,.042),(.012,.470,.035)],[(.047,.028),(.036,.025),(.024,.019),(.015,.012),(.007,.006),(.0018,.0018)],12,label='Tapered_tail')
    # Independent coarse hexagonal nodules follow the cuirass surface; these are
    # original procedural accents, not traced fossil plates or claimed exact rows.
    shell_surface=BVHTree.FromPolygons([Vector(v) for v in shell.v],shell.f,all_triangles=False)
    def surface_z(x,y):
        hit,normal,index,distance=shell_surface.ray_cast(Vector((x,y,.5)),Vector((0,0,-1)))
        if hit is None:raise ValueError('Nodule lies outside the shell surface')
        return hit.z
    idx=0
    for row in range(-6,7):
        row_y=-.005+row*.032
        for c in range(-5,6):
            x=(c+(0.5 if row%2 else 0))*.029+.0025*math.sin(c*4.1+row*1.8)
            y=row_y+.0035*math.cos(c*3.1-row*1.4)
            r=math.sqrt((x/.175)**2+((y+.005)/.245)**2)
            if r>.89:continue
            idx+=1;size=.013*(.87+.12*math.sin(idx*2.31));base=surface_z(x,y)
            vs=[];n=6
            for j in range(n):
                t=2*math.pi*j/n+(.08*math.sin(idx));xx=x+size*math.cos(t);yy=y+size*1.08*math.sin(t)
                vs.append((xx,yy,surface_z(xx,yy)-.001))
            for j in range(n):
                t=2*math.pi*j/n+.08*math.sin(idx);xx=x+size*.68*math.cos(t);yy=y+size*.68*1.08*math.sin(t)
                vs.append((xx,yy,surface_z(xx,yy)+.0038+.0006*math.sin(idx)))
            vs.append((x,y,base+.0055))
            fs=[tuple(range(n-1,-1,-1))]
            for j in range(n):fs.extend([(j,(j+1)%n,n+(j+1)%n,n+j),(n+j,n+(j+1)%n,2*n)])
            nodes.add(vs,fs,mi=0 if idx%4 else 1,label='Dorsal_nodule_%03d'%idx)
    objs=[p.obj(col) for p in (shell,skin,head,nodes,trim,rims)]
    # Ground original foot contact. This is an interpretative benthic pose.
    for o in objs:
        for v in o.data.vertices:v.co.z-=.009
    root=bpy.data.objects['placochelys'];root['anatomical_basis']='Holotype skull; incompletely preserved/lost postcranium. Live reconstruction.'
    root['crushing_teeth']='Posterior teeth present biologically but occluded by closed jaw. Snout tip is toothless.'
    root['inferred']='Colour, skin volume, webbing, carapace outline and pose; not a complete fossil measurement.'
    root['scale']='0.9m length and 0.15m skull: published educator reconstruction estimates.'
    return col

if a.mode in ('build','gray'):
    col=build()
    if a.mode=='gray':
        gray=make_material('Authoring_clay','#929292')
        for o in col.all_objects:
            if o.type=='MESH':
                o.data.materials.clear();o.data.materials.append(gray)
                for p in o.data.polygons:p.material_index=0
        render_previews(col,OUT,views=('front','side','top','hero'),resolution=384,samples=8,transparent=False)
    else:
        record=export_asset('placochelys',{'en':'Placochelys','zh':'Placochelys'},'animals',col,output_root=OUT/'private'/'canonical-export',render=False,max_triangles=6500,max_materials=6,max_primitives=12,
            metadata={'generator':'source/generate.py','description':{'en':'Original living reconstruction of Placochelys placodonta with a pointed toothless rostrum, low oval cuirass, four short webbed limbs and tapering tail.','zh':'Placochelys placodonta 原创活体复原，具窄尖无齿吻端、低椭圆甲、四条短肢及渐细尾。'},'reconstruction_notes':P['uncertainties'],'origin':'Foot-contact centre, identity root; +Z up and -Y head in Blender.'})
        canonical=OUT/'private'/'canonical-export'/'placochelys'
        shutil.copy2(canonical/'placochelys.glb',OUT/'model.glb');shutil.copy2(canonical/'placochelys.blend',OUT/'model.blend')
        for fn,dest in [('qa.json','technical.json'),('metadata.json','build-metadata.json')]:
            data=json.loads((canonical/fn).read_text())
            if fn=='metadata.json':
                data['glb']='model.glb';data['blend']='model.blend';data['preview']='preview.png'
            write(OUT/'qa'/'evidence'/dest,data)
        write(OUT/'qa'/'evidence'/'generation.json',{'blender':bpy.app.version_string,'generator_sha256':sha(SOURCE/'generate.py'),'parameters_sha256':sha(SOURCE/'params.json'),'glb_sha256':sha(OUT/'model.glb'),'seed':P['seed'],'node_count':len(col.all_objects),'python':sys.version,'mode':'build','source_path_policy':'All model-generating imports from own source/deps; bpy/mathutils runtime only'})
else:
    # Fresh scene and actual delivered GLB, never the source scene.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    col=bpy.data.collections.new('ACTUAL_GLB');bpy.context.scene.collection.children.link(col)
    for o in list(bpy.context.scene.objects):
        for old in list(o.users_collection):old.objects.unlink(o)
        col.objects.link(o)
    images=render_previews(col,OUT/'private'/'final-raw',views=('front','side','top','hero'),resolution=896,samples=32,transparent=False)
    view=OUT/'views';view.mkdir(exist_ok=True)
    records=[]
    directions={'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]}
    for name in ('front','side','top','perspective'):
        source=OUT/'private'/'final-raw'/('preview-'+('hero' if name=='perspective' else name)+'.png')
        dest=view/(name+'.png');shutil.copy2(source,dest)
        records.append({'path':'views/'+name+'.png','sha256':sha(dest),'camera_direction_blender':directions[name],'projection':'orthographic'})
    shutil.copy2(view/'perspective.png',OUT/'preview.png')
    write(OUT/'qa'/'evidence'/'actual-glb-views.json',{'status':'rendered_pending_independent_visual_review','glb_sha256':sha(OUT/'model.glb'),'engine':'Cycles CPU','threads':2,'resolution':[896,896],'samples':32,'denoising':False,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'lighting':'Unmodified canonical asset_common.py neutral key/fill preset','background':'#E8E4DC','scene':'Factory-reset Blender scene, clean import of delivered GLB, stage excluded from source and export','views':records,'preview_sha256':sha(OUT/'preview.png'),'perspective_reused_as_preview':True})
print('COMPLETE',a.mode,str(OUT))
