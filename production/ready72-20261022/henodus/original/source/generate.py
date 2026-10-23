#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic Henodus living reconstruction. Blender 4.3.2, standard library only.
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUT [--gray]
No external files are consulted except sibling params.json and declared deps/.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse, random
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source,render_previews
from qa_glb import audit_glb
A=argparse.ArgumentParser(); A.add_argument('--output-dir',type=Path,required=True); A.add_argument('--gray',action='store_true')
a=A.parse_args(sys.argv[sys.argv.index('--')+1:]); out=a.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
p=json.loads((HERE/'params.json').read_text()); rng=random.Random(p['seed'])
col=setup_scene('henodus',p['seed']); root=bpy.data.objects[col['asset_root']]
root['taxon']='Henodus chelyops'; root['revision']='r001'; root['reconstruction']='Living placodont; closed mouth obscures four posterior crushing teeth; soft tissues inferred'
M=[make_material(k,v,roughness=.87) for k,v in p['palette'].items()]
# Mesh buckets retain semantic vertex groups and separate editable named anatomy.
buckets={}
def add(group,verts,faces,mat=0,part=None):
    if group not in buckets: buckets[group]={'v':[],'f':[],'m':[],'parts':[]}
    b=buckets[group]; n=len(b['v']); b['v']+=verts; b['f'] += [tuple(n+i for i in f) for f in faces]; b['m'] += [mat]*len(faces)
    if part:b['parts'].append((part,list(range(n,n+len(verts)))))
def rings(group,name,rows,mat):
    n=len(rows[0]); verts=sum(rows,[]); faces=[]
    for j in range(len(rows)-1):
        for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    faces += [tuple(reversed(range(n))),tuple((len(rows)-1)*n+i for i in range(n))]
    add(group,verts,faces,mat,name)
def superellipse(rx,ry,cy=0,n=32,power=4):
    return [(rx*math.copysign(abs(math.cos(2*math.pi*i/n))**(2/power),math.cos(2*math.pi*i/n)),cy+ry*math.copysign(abs(math.sin(2*math.pi*i/n))**(2/power),math.sin(2*math.pi*i/n))) for i in range(n)]
def carz(x,y):
    r=min(1,(abs(x/.43)**4+abs((y-.045)/.30)**4)**.25)
    return .139+.065*(1-r*r)
outline=superellipse(.43,.30,.045)
# Continuous low carapace foundation: not disconnected armour piled on a tortoise dome.
rows=[]
for scale,z in [(.88,.082),(1,.116),(1,.137),(.80,None),(.48,None),(.12,None)]:
    rows.append([(x*scale,.045+(y-.045)*scale,z if z is not None else carz(x*scale,.045+(y-.045)*scale)-.002) for x,y in outline])
rings('Carapace foundation','continuous-dermal-shield',rows,0)
# Closely tessellated small osteoderms, deterministic Voronoi clipping.
seeds=[]
for j in range(-4,5):
    for i in range(-6,7):
        x=i*.073+(j%2)*.0365+rng.uniform(-.011,.011); y=.045+j*.066+rng.uniform(-.009,.009)
        if (abs(x/.44)**4+abs((y-.045)/.31)**4)<1.05:seeds.append((x,y))
def clip(poly,nx,ny,c):
    q=[]
    for i,b in enumerate(poly):
        aa=poly[i-1]; da=nx*aa[0]+ny*aa[1]-c; db=nx*b[0]+ny*b[1]-c
        if (da<=1e-10)!=(db<=1e-10):
            t=da/(da-db); q.append((aa[0]+t*(b[0]-aa[0]),aa[1]+t*(b[1]-aa[1])))
        if db<=1e-10:q.append(b)
    return q
for k,(sx,sy) in enumerate(seeds):
    poly=outline[:]
    for tx,ty in seeds:
        if tx==sx and ty==sy:continue
        poly=clip(poly,tx-sx,ty-sy,(tx*tx+ty*ty-sx*sx-sy*sy)/2)
        if len(poly)<3:break
    if len(poly)<3:continue
    cx=sum(x for x,y in poly)/len(poly);cy=sum(y for x,y in poly)/len(poly)
    # Narrow, dark sutures remain in underlying continuous shield; bevels are tiny.
    outer=[(cx+(x-cx)*.965,cy+(y-cy)*.965) for x,y in poly]
    inner=[(cx+(x-cx)*.85,cy+(y-cy)*.85) for x,y in poly]
    row0=[(x,y,carz(x,y)-.003) for x,y in outer]
    row1=[(x,y,carz(x,y)+.0016) for x,y in outer]
    row2=[(x,y,carz(x,y)+.0034) for x,y in inner]
    rings('Osteoderm mosaic',f'osteoderm-{k:03}',[row0,row1,row2],1 if rng.random()<.68 else 2)
# Flattened plastral/ventral body beneath broad armour; closed manifold.
rings('Ventral body','ventral-armour',[[ (x*s,.045+(y-.045)*s,z) for x,y in outline] for s,z in [(.60,.044),(.85,.054),(.92,.085),(.84,.111)]] ,4)
# Organic longitudinal loft uses explicit octagonal sections, not default sphere primitives.
def longitudinal(name,sections,mat=3,group='Soft anatomy'):
    rows=[]
    for y,rx,cz,rz in sections:
        # The front skull's two straight cross-edges are rectangular, gently bevelled.
        rows.append([(rx*x,y,cz+rz*z) for x,z in [(-.80,-1),(.80,-1),(1,-.55),(1,.55),(.80,1),(-.80,1),(-1,.55),(-1,-.55)]])
    rings(group,name,rows,mat)
longitudinal('short-neck',[(-.215,.083,.105,.040),(-.285,.082,.105,.043),(-.335,.091,.110,.044)])
longitudinal('broad-rectangular-skull',[(-.310,.100,.111,.046),(-.365,.124,.116,.050),(-.435,.128,.111,.044),(-.510,.132,.099,.034),(-.525,.126,.097,.028)])
longitudinal('lower-jaw',[(-.340,.081,.071,.023),(-.425,.121,.066,.027),(-.510,.131,.067,.022),(-.524,.125,.071,.018)],4,'Ventral body')
# Mouth is closed, square across front. Posterior crushing teeth are not exposed.
def tube(name,points,widths,depths,mat=3,group='Soft anatomy',sides=8):
    rows=[]
    for i,point in enumerate(points):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)]); tangent.normalize()
        axis=tangent.cross(Vector((0,0,1))).normalized(); other=tangent.cross(axis).normalized()
        rows.append([tuple(Vector(point)+axis*(widths[i]*math.cos(2*math.pi*j/sides))+other*(depths[i]*math.sin(2*math.pi*j/sides))) for j in range(sides)])
    rings(group,name,rows,mat)
# Recessed narrow mouth seam: minimal embedded dark surface, never exposed baleen.
tube('closed-mouth-line',[(-.126,-.516,.085),(-.105,-.527,.085),(0,-.529,.085),(.105,-.527,.085),(.126,-.516,.085)],[.0016]*5,[.0016]*5,5,'Eye and mouth detail',6)
for sign in (-1,1):
    # Small dorsolateral eyes at the rear half of the square skull.
    tube('eye-rim',[(sign*.105,-.411,.140),(sign*.119,-.416,.145),(sign*.125,-.416,.142)],[.015,.015,.007],[.009,.010,.006],0,'Carapace foundation',10)
    tube('eye',[(sign*.116,-.418,.146),(sign*.127,-.418,.145)],[.008,.0075],[.008,.006],5,'Eye and mouth detail',10)
    for hind in (False,True):
        ys=[.198,.274,.312] if hind else [-.148,-.242,-.281]
        points=[(sign*.277,ys[0],.093),(sign*.377,ys[1],.052),(sign*.456,ys[2],.027)]
        tube(('hind' if hind else 'fore')+'-limb-'+str(sign),points,[.045,.031,.023],[.035,.022,.015])
        # Four modest webbed digits form a compact lobed paddle, not a turtle flipper.
        base=Vector(points[-1]); fx=sign*.515; fy=ys[2]+(.025 if hind else -.012)
        contour=[(sign*.439,ys[2]-.023),(sign*.483,fy-.039),(sign*.520,fy-.037),(sign*.536,fy-.023),(sign*.523,fy-.009),(sign*.542,fy+.004),(sign*.526,fy+.017),(sign*.530,fy+.030),(sign*.510,fy+.040),(sign*.474,fy+.036),(sign*.443,ys[2]+.021)]
        if sign<0:contour.reverse()
        cx=sum(x for x,y in contour)/len(contour); cy=sum(y for x,y in contour)/len(contour)
        rings('Soft anatomy',('hind' if hind else 'fore')+'-webbed-foot-'+str(sign),[[(x,y,.001) for x,y in contour],[(x,y,.018) for x,y in contour],[(cx+(x-cx)*.70,cy+(y-cy)*.70,.030) for x,y in contour]],3)
longitudinal('short-tapering-tail',[(.270,.050,.086,.033),(.345,.037,.072,.026),(.405,.023,.047,.018),(.452,.010,.025,.009),(.475,.0025,.014,.003)])
for name,b in buckets.items():
    used=sorted(set(b['m'])); mats=[M[i] for i in used];obj=mesh_object(name,b['v'],b['f'],mats,col)
    for poly,idx in zip(obj.data.polygons,b['m']):poly.material_index=used.index(idx)
    for part,ids in b['parts']:
        vg=obj.vertex_groups.new(name=part);vg.add(ids,1,'REPLACE')
    obj['topology']='Closed low-poly lofts; deliberate embedded anatomical joins; flat normals'
bpy.context.view_layer.update()
source=audit_source(col,p['geometry_policy']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={v.identifier for v in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Required exporter options missing')
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(out/'model.glb',p['geometry_policy']['max_triangles'],p['geometry_policy']['max_materials'],p['geometry_policy']['max_primitives'])
b=source['bounds_blender_m'];want={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-want[k][i]) for k in want for i in range(3))
if glb['errors'] or delta>1e-4 or glb['scene_triangles']!=source['triangles'] or glb['bytes']>p['geometry_policy']['max_glb_bytes']:raise RuntimeError('Export QA failed '+str(glb['errors']))
report={'asset_id':'henodus','revision':'r001','blender_version':bpy.app.version_string,'seed':p['seed'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'threejs_version_target':'0.180.0','origin':'floor footprint center, lowest foot z=.001m','source_clean':{'cameras':sum(o.type=='CAMERA' for o in bpy.data.objects),'lights':sum(o.type=='LIGHT' for o in bpy.data.objects),'collections':[c.name for c in bpy.data.collections]},'diagnostic_measurements':{'carapace_width_m':.86,'carapace_length_m':.60,'carapace_width_length_ratio':.86/.60,'total_length_m':1.,'carapace_height_m':.125,'limb_count':4,'jaw_anterior_width_m':.252,'closed_mouth':True}}
(out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
if a.gray:
    gray=make_material('Gray authoring diagnostic','#929292',roughness=.9)
    bpy.context.view_layer.material_override=gray
    render_previews(col,out/'gray',views=('front','side','top','hero'),resolution=384,samples=8)
print('HENODUS_BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'])
