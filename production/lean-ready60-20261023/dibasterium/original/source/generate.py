#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Dibasterium durgae construction, in metres, no external geometry.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output /path/build
The source .blend contains separately editable named anatomical pieces. Export
uses temporary material batches and leaves the saved source unchanged.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=argparse.ArgumentParser(); args.add_argument('--output',type=Path,required=True)
a=args.parse_args(sys.argv[sys.argv.index('--')+1:]); OUT=a.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('dibasterium',P['seed']); root=bpy.data.objects[C['asset_root']]
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
M={k:make_material(k,c,roughness=.82) for k,c in P['palette'].items()}
parts=[]
def mesh(name,v,f,mat,**meta):
    obj=mesh_object(name,[[q*.001 for q in p] for p in v],f,M[mat],C)
    for k,val in meta.items(): obj[k]=val
    parts.append({'name':name,'material':mat,**meta})
    return obj

def tube(name,points,radii,mat='limb-cuticle',n=8,ell=.85,**meta):
    pts=[Vector(p) for p in points]; verts=[]
    for i,p in enumerate(pts):
        d=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
        ref=Vector((0,0,1)) if abs(d.z)<.9 else Vector((0,1,0))
        u=d.cross(ref).normalized(); vv=d.cross(u).normalized()
        for j in range(n):
            t=2*math.pi*j/n; verts.append(tuple(p+radii[i]*(math.cos(t)*u+ell*math.sin(t)*vv)))
    faces=[tuple(range(n-1,-1,-1))]
    for i in range(len(pts)-1):
        for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.append(tuple((len(pts)-1)*n+j for j in range(n)))
    return mesh(name,verts,faces,mat,**meta)

def rod(name,a,b,r1,r2,mat='limb-cuticle',**meta):
    aa,bb=Vector(a),Vector(b); d=bb-aa
    r2=max(r2,.04)  # Display-scale minimum tip radius: preserve finite closed caps at 23.2 mm size.
    return tube(name,[aa,aa+d*.16,aa+d*.82,bb],[r1*.82,r1,r2,r2*.80],mat,**meta)

def cap_shell(name,outline,center,height,zbase,thick,mat,**meta):
    n=len(outline); rs=[.22,.45,.67,.84,.95,1.0]
    verts=[]
    for inside in (False,True):
        for r in rs:
            for x,y in outline:
                z=zbase+height*math.sqrt(max(0,1-r*r))-(thick if inside else 0)
                verts.append((center[0]+(x-center[0])*r,center[1]+(y-center[1])*r,z))
        verts.append((center[0],center[1],zbase+height-(thick if inside else 0)))
    layer=len(rs)*n+1; faces=[]
    for ins in range(2):
        o=ins*layer
        for j in range(n): faces.append((o+len(rs)*n,o+j,o+(j+1)%n))
        for k in range(len(rs)-1):
            for j in range(n): faces.append((o+k*n+j,o+(k+1)*n+j,o+(k+1)*n+(j+1)%n,o+k*n+(j+1)%n))
    for j in range(n): faces.append(((len(rs)-1)*n+j,(len(rs)-1)*n+(j+1)%n,layer+(len(rs)-1)*n+(j+1)%n,layer+(len(rs)-1)*n+j))
    return mesh(name,verts,faces,mat,**meta)

# Broad semi-oval shield, posterior outline gently procurved, no eyes or ridges.
half=[(0,-8),(1.7,-7.72),(3.05,-6.95),(4.0,-5.8),(4.48,-4.4),(4.6,-2.9),(4.54,-1.3),(4.38,.2),(4.15,1.08),(3.4,1.2),(2.3,1.05),(1.15,.94),(0,.9)]
outline=half+[(-x,y) for x,y in half[-2:0:-1]]
cap_shell('01-prosomal-shield',outline,(0,-3.25),3.45,1.55,.16,'dorsal-carapace',anatomy='semioval smooth vaulted shield; no eyes',body_length_component=True)
# Ventral body wall is recessed, distinct from inner and outer limb bases.
ventral=[(.0,-6.85),(1.2,-6.5),(2.5,-5.2),(3.45,-3.3),(3.5,-1.8),(3.1,.2),(1.5,.7),(0,.7)]
ventral+= [(-x,y) for x,y in ventral[-2:0:-1]]
cap_shell('02-ventral-body-wall',ventral,(0,-2.8),.54,1.53,.22,'ventral-cuticle',anatomy='body-wall support; branch insertions independent')
# Raised perioral area; not a proboscis. Inferred simplified ventral tissue.
tube('03-perioral-pad',[(0,-4.5,1.40),(0,-3.7,1.36),(0,-2.6,1.42)],[.5,.65,.46],'ventral-cuticle',n=12,ell=.5)

# Eleven separate tergites. First is reduced and largely concealed below shield.
# Axial shallow furrows are a section change, not invented sagittal spines.
segments=[(1,.72,1.35,2.15,2.65),(2,1.28,2.55,3.65,3.05),(3,2.50,3.85,3.58,3.05),(4,3.80,5.03,3.28,2.96),(5,4.98,6.00,2.97,2.80),(6,5.95,6.89,2.66,2.62),(7,6.84,7.62,2.30,2.43),(8,7.57,8.35,1.95,2.25),(9,8.30,9.65,1.59,2.04),(10,9.60,10.98,1.21,1.84),(11,10.93,12.28,.86,1.65)]
section=[-1,-.86,-.65,-.56,-.48,-.28,0,.28,.48,.56,.65,.86,1]
for idx,ya,yb,w,zpeak in segments:
    zrim=1.22 if idx<9 else 1.10
    v=[]; N=len(section)
    for inner in (False,True):
        for row,t in enumerate([0,.18,.76,1]):
            for u in section:
                y=ya+(yb-ya)*t
                # Posterolateral points become clearer posteriorly, not horns.
                if idx>1: y += max(0,(abs(u)-.78)/.22)*(.08 if idx<5 else .17)*t*t
                dome=math.sqrt(max(0,1-u*u))
                furrow=.07*math.exp(-((abs(u)-.55)/.085)**2)
                z=zrim+(zpeak-zrim)*dome + .08*math.sin(t*math.pi)-furrow-(.12 if inner else 0)
                v.append((w*u,y,z))
    layer=4*N; f=[]
    for inside in (0,1):
        o=inside*layer
        for r in range(3):
            for j in range(N-1): f.append((o+r*N+j,o+r*N+j+1,o+(r+1)*N+j+1,o+(r+1)*N+j))
    for r in range(3):
        for j in (0,N-1): f.append((r*N+j,(r+1)*N+j,layer+(r+1)*N+j,layer+r*N+j))
    for r in (0,3):
        for j in range(N-1): f.append((r*N+j,layer+r*N+j,layer+r*N+j+1,r*N+j+1))
    mesh(f'10-tergite-{idx:02}',v,f,'dorsal-carapace',tergite_index=idx,tagma='preabdomen' if idx<=8 else 'postabdomen',reduced_concealed=(idx==1))
    if idx>1:
        tube(f'11-arthrodial-membrane-{idx:02}',[(0,ya-.10,1.53),(0,ya+.13,1.53)],[w*.70,w*.70],'joint-cuticle',n=12,ell=.52)
# Ventral sternites only on enclosed postabdomen; no appendages on tergite 8.
for idx,ya,yb,w,z in segments[7:]:
    tube(f'12-sternite-{idx:02}',[(0,ya+.04,1.25),(0,yb-.04,1.25)],[w*.76,w*.64],'ventral-cuticle',n=10,ell=.25)
# Triangular-section telson; two short terminal projections, not a sting.
tube('13-telson',[(0,12.20,1.32),(0,12.65,1.30),(0,13.5,1.20),(0,14.5,1.04),(0,14.96,.96)],[.66,.58,.40,.22,.12],'dorsal-carapace',n=3,ell=.9)
for side in (-1,1): rod(f'13-telson-terminal-{side}',(side*.065,14.84,.97),(side*.095,15.20,.91),.065,.028,'dorsal-carapace')

# Paired chelicerae: narrow flexible pedestals, no extra antennae.
for s in (-1,1):
    prefix='L' if s<0 else 'R'
    points=[(s*.40,-4.68,1.35),(s*.62,-5.55,1.04),(s*.90,-6.50,.84),(s*1.10,-7.60,.89),(s*1.24,-8.65,1.15),(s*1.33,-9.65,1.62),(s*1.42,-10.55,2.05)]
    tube(f'20-{prefix}-pair1-chelicera-flexible',points,[.13,.12,.12,.11,.105,.09,.075],n=8,prosomal_pair=1,ramus='chelicera')
    rod(f'20-{prefix}-pair1-chela-fixed',points[-1],(s*1.55,-10.94,2.17),.068,.028,prosomal_pair=1)
    rod(f'20-{prefix}-pair1-chela-movable',(s*1.42,-10.52,2.05),(s*1.27,-10.85,2.16),.058,.028,prosomal_pair=1)
# Fan of walking inner rami with six distinct podomeres and small chela.
# Outer rami originate on the ventrolateral body wall, NOT on these inner rami.
for p in range(2,7):
    y=[-4.55,-3.50,-2.42,-1.30,-.28][p-2]
    dy=[-2.35,-1.35,-.22,1.05,1.85][p-2]
    for s in (-1,1):
        prefix='L' if s<0 else 'R'
        pts=[(s*.82,y,1.48),(s*1.44,y+.04,1.25),(s*3.48,y+dy*.58,1.50),(s*4.25,y+dy*.76,1.16),(s*4.84,y+dy*.90,.79),(s*5.16,y+dy,.43),(s*5.38,y+dy+.06,.12)]
        for j in range(6):
            rod(f'21-{prefix}-pair{p}-endopod-podomere{j+1}',pts[j],pts[j+1],[.27,.25,.22,.19,.16,.12][j],[.22,.23,.19,.16,.12,.075][j],prosomal_pair=p,ramus='endopod',podomere=j+1,insertion_independent=True)
        if p<=5:
            for branch in (-1,1):
                rod(f'21-{prefix}-pair{p}-claw-{branch}',pts[-1],(s*(5.53+branch*.08),y+dy+branch*.22,.027),.075,.028,prosomal_pair=p,ramus='terminal-chela')
        else:
            rod(f'21-{prefix}-pair6-single-terminal',pts[-1],(s*5.71,y+dy+.24,.027),.074,.028,prosomal_pair=6,ramus='nonchelate-terminal')
        if p<=5:
            # Separate peripheral bases. Shorter outer branches turn between inner legs.
            oy=y+{2:-.30,3:.42,4:.42,5:1.10}[p]  # Stagger independent body-wall origins; avoid ramus crossings in the neutral pose.
            op=[(s*3.22,oy,1.54),(s*3.65,oy+.11,1.32),(s*4.72,oy+dy*.28+.22,1.04),(s*5.16,oy+dy*.36+.42,.77),(s*5.43,oy+dy*.43+.66,.55),(s*5.57,oy+dy*.48+.93,.43)]
            for j in range(5):
                rod(f'22-{prefix}-pair{p}-exopod-podomere{j+1}',op[j],op[j+1],[.22,.20,.17,.14,.115][j],[.19,.17,.14,.115,.07][j],prosomal_pair=p,ramus='exopod',podomere=j+1,insertion_independent=True)
            # Small spine at podomere3; five on 4; three terminal spines on 5.
            q=Vector(op[3]); rod(f'22-{prefix}-pair{p}-exopod-lateral-spine',q,q+Vector((s*.25,.02,-.13)),.052,.026)
            for k in range(5):
                q=Vector(op[3]).lerp(Vector(op[4]),(k+.5)/5)
                rod(f'22-{prefix}-pair{p}-exopod-brush4-{k}',q,q+Vector((s*(.19+.018*k),.10+.03*k,-.27)),.045,.025)
            for k in range(3):
                q=Vector(op[-1]); rod(f'22-{prefix}-pair{p}-exopod-brush5-{k}',q,q+Vector((s*(.10+.11*k),.29-.05*k,-.18)),.043,.025)
# Seventh prosomal pair: small flap behind mouth, spine fringe; not a full leg.
for s in (-1,1):
    prefix='L' if s<0 else 'R'
    rod(f'23-{prefix}-pair7-chilarium-shaft',(s*.67,.15,1.39),(s*.87,-.44,.99),.16,.12,prosomal_pair=7)
    tube(f'23-{prefix}-pair7-spine-fringed-flap',[(s*.87,-.44,.99),(s*1.0,-.78,.83),(s*1.04,-1.02,.79)],[.17,.28,.15],n=10,ell=.32,prosomal_pair=7,ramus='small-flap')
    for k in range(5):
        rod(f'23-{prefix}-pair7-flap-fringe-{k}',(s*(.80+k*.12),-.95,.80),(s*(.77+k*.14),-1.28,.68),.044,.025,prosomal_pair=7)

# Six PAIRS of lamellate gills. Six thick display lamellae per group are an
# explicit LOD simplification of the published approximately20-30 anteriorly.
# These are reconstructed near-axis insertions, not known articulated bases.
for g in range(1,7):
    gy=[2.15,3.32,4.47,5.48,6.35,7.11][g-1]
    gw=[2.92,2.83,2.64,2.39,2.12,1.82][g-1]
    for s in (-1,1):
        prefix='L' if s<0 else 'R'
        for lam in range(6):
            # Posterior/ventral nested fan of lamellae, separate left/right groups.
            shrink=1-lam*.045; x0=.19 if g==1 else .055
            yy=gy+(lam-2.5)*.105; z=.99-(lam*.071)
            leaf=[(s*x0,yy-.28,z+.10),(s*(gw*.45*shrink),yy-.43,z+.13),(s*(gw*.88*shrink),yy-.34,z+.12),(s*(gw*shrink),yy-.03,z+.07),(s*(gw*.92*shrink),yy+.26,z),(s*(gw*.52*shrink),yy+.40,z-.03),(s*x0,yy+.24,z+.02)]
            vv=leaf+[(x,y,z-.055) for x,y,z in leaf]; nn=len(leaf)
            ff=[tuple(range(nn)),tuple(range(2*nn-1,nn-1,-1))]+[(j,(j+1)%nn,(j+1)%nn+nn,j+nn) for j in range(nn)]
            mesh(f'30-{prefix}-gill{g}-lamella{lam+1}',vv,ff,'gill-lamellae',gill_pair=g,lamella_display_index=lam+1,attachment='conservative inferred near-axis')

# Place intended claw contacts at the common Z=0 floor; do not normalize length.
bpy.context.view_layer.update()
low=min((o.matrix_world@v.co).z for o in C.objects if o.type=='MESH' for v in o.data.vertices)
contact_y=[v.co.y for o in C.objects if o.type=='MESH' and ('-claw-' in o.name or '-single-terminal' in o.name) for v in o.data.vertices]
footprint_y=(min(contact_y)+max(contact_y))/2
for o in C.objects:
    if o.type=='MESH':
        for v in o.data.vertices:
            v.co.z-=low
            v.co.y-=footprint_y
root['taxon']='Dibasterium durgae'; root['prosomal_appendage_pairs']=7; root['separate_biramous_pairs']='2,3,4,5'; root['tergites']=11; root['gill_pairs']=6
root['units']='metres'; root['mounting_origin']='floor contact center'; root['biological_colour']='unknown; muted artistic palette'
source=audit_source(C,max_triangles=40000)
# At millimetre specimen scale, test actual nonzero geometry as well as report
# the canonical absolute-area checker. It must never be mistaken for a repair.
if source['errors']: raise RuntimeError(source['errors'])
(OUT/'source-audit.json').write_text(json.dumps(source,indent=2)+'\n')
(OUT/'anatomy.json').write_text(json.dumps({'parts':parts,'counts':{'tergites':11,'preabdomen':8,'postabdomen':3,'prosomal_pairs':7,'biramous_pairs':[2,3,4,5],'gill_pairs':6,'display_lamellae_per_gill':6},'scale_landmarks_mm':{'anterior_shield_y':-8-footprint_y*1000,'posterior_terminal_y':15.2-footprint_y*1000,'body_length':23.2,'shield_width':9.2},'ground_shift_m':-low,'footprint_center_shift_y_m':-footprint_y,'origin':'intended floor contact center','note':'Minor posture, cuticle thickness, palette and gill attachment are conservative reconstructions.'},indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
# Temporary batching preserves saved editability and source semantic audit.
groups={}
for o in list(C.objects):
    if o.type!='MESH': continue
    mat=o.data.materials[0]; key=mat.name
    g=groups.setdefault(key,{'v':[],'f':[],'parts':[]}); offset=len(g['v'])
    g['v'] += [tuple(o.matrix_world@v.co) for v in o.data.vertices]
    g['f'] += [tuple(offset+i for i in p.vertices) for p in o.data.polygons]
    g['parts'].append(o.name); bpy.data.objects.remove(o,do_unlink=True)
for k,g in groups.items():
    o=mesh_object('batch-'+k,g['v'],g['f'],M[k],C); o['semantic_parts']=';'.join(g['parts'])
bpy.ops.object.select_all(action='DESELECT')
for o in C.objects:o.select_set(True)
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
assert set(opts)<=available,set(opts)-available
bpy.ops.export_scene.gltf(**opts)
qa=audit_glb(OUT/'model.glb',max_triangles=40000,max_materials=6,max_primitives=8)
assert not qa['errors'],qa['errors']
assert source['triangles']==qa['scene_triangles'],(source['triangles'],qa['scene_triangles'])
(OUT/'glb-audit.json').write_text(json.dumps(qa,indent=2)+'\n')
(OUT/'build.json').write_text(json.dumps({'blender':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'seed':P['seed'],'export_options':{k:v for k,v in opts.items() if k!='filepath'},'original_geometry':True,'source_preview_scene_saved':False,'threejs_version_target':'0.180.0'},indent=2)+'\n')
print('DIBASTERIUM_BUILD_COMPLETE',qa['semantic_sha256'])
