# SPDX-License-Identifier: MIT
"""Megarachne: original profile-built hypothetical eurypterid, in meters.
Run with Blender in any working directory. All data dependencies are relative to
this script; --output selects a resolved output directory. No reference artwork
is embedded or traced. Posterior anatomy and depth are comparative inference.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
from math import sin, cos, pi
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=HERE.parent)
a=ap.parse_args(argv); OUT=a.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('megarachne',P['seed']); root=bpy.data.objects[C['asset_root']]
root['reconstruction']='Hypothetical eurypterid; posterior body and telson inferred; unknown mouth appendages concealed'
M={k:make_material(k,v,roughness=P['material_defaults']['eye_roughness'] if k=='eyes' else P['material_defaults']['roughness']) for k,v in P['palette_srgb'].items()}
# Build buffered closed islands into semantic editable parts, not primitive objects.
class Part:
 def __init__(self,name,mat):self.name=name;self.mat=mat;self.v=[];self.f=[]
 def add(self,v,f):
  o=len(self.v);self.v.extend(v);self.f.extend([tuple(o+i for i in face) for face in f])
 def finish(self):return mesh_object(self.name,self.v,self.f,self.mat,C)

def rings(part,rows):
 n=len(rows[0]);v=[p for row in rows for p in row]; f=[]
 for j in range(len(rows)-1):
  for i in range(n):f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 for rowidx,reverse in ((0,True),(len(rows)-1,False)):
  row=rows[rowidx];c=len(v);v.append(tuple(sum(p[k] for p in row)/n for k in range(3)))
  for i in range(n):
   face=(c,rowidx*n+i,rowidx*n+(i+1)%n);f.append(face[::-1] if reverse else face)
 part.add(v,f)

def loft(name,profile,mat,n=20):
 # Rows: y, half-width, mid-height, dorsal rise, ventral depth.
 p=Part(name,mat);rows=[]
 for y,w,z,h,d in profile:
  rows.append([(w*cos(t),y,z+(h if sin(t)>0 else d)*sin(t)) for t in [2*pi*i/n for i in range(n)]])
 rings(p,rows);return p.finish()

def plate(name,outline,center,zrim,rise,thick,mat,levels=6):
 # Closed star-convex shield. Deliberate concentric profile, faceted slope and rim.
 n=len(outline);cx,cy=center;v=[(cx,cy,zrim+rise)];f=[]
 for j in range(1,levels+1):
  r=j/levels
  for x,y in outline:v.append((cx+(x-cx)*r,cy+(y-cy)*r,zrim+rise*(1-r*r)**0.8))
 for i in range(n):f.append((0,1+i,1+(i+1)%n))
 for j in range(levels-1):
  b=1+j*n;bb=b+n
  for i in range(n):f.append((b+i,bb+i,bb+(i+1)%n,b+(i+1)%n))
 b=1+(levels-1)*n;bottom=len(v)
 v.extend([(x,y,zrim-thick) for x,y in outline]);c=len(v);v.append((cx,cy,zrim-thick))
 for i in range(n):f.extend([(b+i,bottom+i,bottom+(i+1)%n,b+(i+1)%n),(c,bottom+(i+1)%n,bottom+i)])
 return mesh_object(name,v,f,mat,C)

# Broad low prosoma, continuous modest downturned anterior projection.
shieldprof=[(-.270,.015,.029,.006,.005),(-.266,.035,.033,.008,.008),(-.259,.055,.037,.011,.011),(-.251,.065,.040,.015,.014),(-.238,.067,.041,.019,.015),(-.221,.070,.041,.022,.015),(-.202,.073,.041,.024,.015),(-.183,.077,.040,.025,.015),(-.164,.081,.039,.024,.015),(-.145,.085,.038,.022,.014),(-.127,.088,.036,.020,.013),(-.111,.090,.034,.018,.012),(-.100,.088,.033,.016,.011)]
loft('Prosomal bell shield',shieldprof,M['dorsal_armor'],28)
# Thin integrated median ridge and shoulder rim, not independent fangs.
loft('Median shield ridge',[(-.248,.001,.054,.001,.001),(-.227,.002,.062,.0015,.002),(-.205,.0022,.065,.0018,.002),(-.185,.002,.065,.002,.002),(-.160,.0018,.063,.0012,.002),(-.133,.001,.058,.001,.002)],M['ridge_highlight'],8)
# T1 leaf epimera: sutured central length 38 mm, lateral length about 92 mm.
outline=[(-.088,-.101),(-.094,-.085),(-.095,-.064),(-.091,-.040),(-.078,-.009),(-.067,-.031),(-.057,-.048),(-.039,-.060),(0,-.062),(.039,-.060),(.057,-.048),(.067,-.031),(.078,-.009),(.091,-.040),(.095,-.064),(.094,-.085),(.088,-.101),(.044,-.104),(0,-.105),(-.044,-.104)]
plate('T1 sutured leaf epimera',outline,(0,-.080),.030,.021,.004,M['side_armor'],7)
# Enlarged near-circular T2, narrower than T1. Shallow rather than inflated.
cx,cy=0,.009;rx,ry=.0735,.071
outline=[(rx*cos(2*pi*i/64),cy+ry*sin(2*pi*i/64)) for i in range(64)]
plate('T2 circular dorsal plate',outline,(cx,cy),.032,.025,.004,M['dorsal_armor'],8)
def t2z(x,y):
 r2=(x/rx)**2+((y-cy)/ry)**2
 return .032+.025*max(0,1-r2)**.8
# Thirteen low, embedded fan ribs from the anterior portion, not hair or spines.
ribs=Part('T2 thirteen embedded fan ribs',M['ridge_highlight'])
for k in range(13):
 angle=pi*.06+pi*.88*k/12
 ex=rx*.94*cos(angle);ey=cy+ry*.94*sin(angle)
 sx=ex*.13;sy=-.045+abs(ex)*.06
 rows=[]
 for j in range(9):
  t=j/8;x=sx+(ex-sx)*t;y=sy+(ey-sy)*t;w=.0007+.0007*sin(pi*t)
  dx=ex-sx;dy=ey-sy;l=math.hypot(dx,dy);nx=-dy/l;ny=dx/l
  h=.0015*sin(pi*(.1+.8*t));z=t2z(x,y)
  rows.append([(x+nx*w,y+ny*w,z-.0006),(x,y,z+h),(x-nx*w,y-ny*w,z-.0006),(x,y,z-.0012)])
 rings(ribs,rows)
ribs.finish()
# Original low ventral volume; anterior mouth appendages intentionally concealed.
loft('Concealed ventral prosoma',[(-.252,.026,.024,.003,.007),(-.231,.050,.025,.006,.008),(-.192,.065,.025,.006,.008),(-.151,.069,.026,.007,.008),(-.108,.065,.026,.009,.008),(-.071,.047,.026,.009,.008)],M['underside'],16)
# Kidney-shaped lateral eyes: one pair only, made as custom shallow plates.
for side in (-1,1):
 ex=side*.019;ey=-.184
 outline=[]
 for i in range(24):
  t=2*pi*i/24
  x=.0055*cos(t); y=.0115*sin(t)
  if cos(t)*side<0:x*=.65+.20*abs(sin(t))
  outline.append((ex+x,ey+y))
 plate(('Left' if side<0 else 'Right')+' reniform lateral eye',outline,(ex,ey),.0615,.0038,.001,M['eyes'],3)
outline=[(.0075*cos(2*pi*i/16),-.182+.0075*sin(2*pi*i/16)) for i in range(16)]
plate('Median ocular mound',outline,(0,-.182),.064,.006,.002,M['side_armor'],3)
# Subtle paired ocelli on the small median mound, not a spider eye cluster.
for s in (-1,1):
 outline=[(s*.0023+.0012*cos(2*pi*i/8),-.182+.0015*sin(2*pi*i/8)) for i in range(8)]
 plate('Median ocellus '+str(s),outline,(s*.0023,-.182),.0691,.0006,.0006,M['eyes'],2)
# Comparative T3-T12, overlapping and mostly concealed forward by T2.
for i in range(10):
 y=-.016+i*.0196;w=.060-i*.0046;length=.029-i*.0005;z=.030-i*.00135
 outline=[(-w*.80,y-length*.52),(-w,y-length*.23),(-w*.96,y+length*.30),(-w*.68,y+length*.52),(0,y+length*.58),(w*.68,y+length*.52),(w*.96,y+length*.30),(w,y-length*.23),(w*.80,y-length*.52),(0,y-length*.58)]
 plate('Inferred tergite T'+str(i+3),outline,(0,y),z,.013-i*.00065,.004,M['side_armor'] if i%2==0 else M['dorsal_armor'],4)
loft('Inferred straight hastate telson',[(.172,.014,.013,.007,.005),(.184,.019,.013,.008,.005),(.197,.022,.012,.009,.005),(.214,.019,.011,.009,.004),(.233,.0135,.010,.007,.0035),(.250,.007,.009,.005,.003),(.270,.00045,.008,.0007,.0007)],M['dorsal_armor'],16)
loft('Telson restrained central carina',[(.184,.001,.021,.0008,.001),(.203,.0012,.021,.001,.001),(.229,.001,.018,.0008,.001),(.252,.0005,.013,.0006,.0006)],M['ridge_highlight'],8)
# Six articulated podomeres per conspicuous limb III-VI, not smooth tubes.
paths=[[(.055,-.237,.032),(.094,-.248,.038),(.130,-.280,.043),(.166,-.299,.033),(.198,-.300,.022),(.222,-.287,.012),(.240,-.271,.002)],[(.070,-.203,.030),(.107,-.211,.042),(.152,-.212,.050),(.195,-.206,.040),(.229,-.196,.026),(.249,-.184,.012),(.260,-.175,.002)],[(.080,-.165,.031),(.115,-.151,.046),(.154,-.126,.055),(.197,-.108,.040),(.227,-.080,.026),(.242,-.059,.012),(.250,-.048,.002)],[(.083,-.123,.030),(.112,-.093,.044),(.141,-.050,.052),(.173,-.014,.037),(.193,.020,.023),(.198,.048,.010),(.197,.063,.002)]]
contacts=[]
for side in (-1,1):
 for pair,path0 in enumerate(paths):
  path=[Vector((side*x,y,z)) for x,y,z in path0];label=('L' if side<0 else 'R')+str(pair+3)
  shell=Part('Limb '+label+' six podomeres',M['limbs']);joints=Part('Limb '+label+' joint membranes',M['joint_membrane'])
  for k in range(6):
   A,B=path[k],path[k+1];d=B-A;nx=Vector((-d.y,d.x,0)).normalized();rows=[]
   w=[.0115,.0130,.0110,.0080,.0055,.0038][k];h=[.008,.009,.008,.006,.004,.003][k]
   for q,sw,sh in [(0,.62,.65),(.15,1,1),(.49,.98,.96),(.82,.78,.80),(1,.62,.65)]:
    pos=A+d*q
    if k==5:
     ww=w*(1-q)+.0014*q;hh=h*(1-q)+.002*q
    else:ww=w*sw;hh=h*sh
    row=[]
    for j in range(8):
     t=2*pi*j/8;v=pos+nx*(ww*cos(t))+Vector((0,0,hh*sin(t)));row.append(tuple(v))
    rows.append(row)
   rings(shell,rows)
   if k<5:
    axis=d.normalized();up=Vector((0,0,1));jrows=[]
    for t,sr in [(-.004,.68),(0,1),(.004,.68)]:
     pos=B+axis*t
     jrows.append([tuple(pos+nx*(w*.74*sr*cos(2*pi*j/8))+up*(h*.76*sr*sin(2*pi*j/8))) for j in range(8)])
    rings(joints,jrows)
   if pair<2 and k in (1,2):
    p=A+d*.58;v=[tuple(p+nx*w*.5+Vector((0,0,.002))),tuple(p+nx*w*.5+Vector((0,0,-.002))),tuple(p+nx*w*1.05+d*.17+Vector((0,0,.001))),tuple(p+Vector((0,-.011,0))),tuple(p+nx*w*1.05-d*.12+Vector((0,0,-.001)))]
    shell.add(v,[(0,2,3),(0,3,4),(0,4,1),(0,1,2),(1,4,3),(1,3,2)])
  shell.finish();joints.finish();contacts.append({'limb':label,'anatomical_point_m':list(path[-1]),'lowest_support_z_m':0.0})
# Footprint center, not tail-biased whole-animal bounding-box center.
foot_y=(min(p['anatomical_point_m'][1] for p in contacts)+max(p['anatomical_point_m'][1] for p in contacts))/2
for obj in C.all_objects:
 if obj.type=='MESH':
  for v in obj.data.vertices:v.co.y-=foot_y
for c in contacts:c['root_frame_point_m']=[c['anatomical_point_m'][0],c['anatomical_point_m'][1]-foot_y,c['anatomical_point_m'][2]]
bpy.context.view_layer.update()
limits=P['geometry_limits'];source=audit_source(C,limits['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.scene['source_generator']='source/generate.py';bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
bpy.context.preferences.filepaths.save_version=0
# Factory startup UI can retain host directories unrelated to this model.
# Clear them through Blender's data API before saving the source artifact.
bpy.context.scene.render.filepath='//render'
for screen in bpy.data.screens:
 for area in screen.areas:
  for space in area.spaces:
   if space.type=='FILE_BROWSER' and space.params:
    space.params.directory=b'//'
    space.params.filename=''
# Resolve runtime paths before save, even in an unrelated current directory.
bpy.ops.wm.save_as_mainfile(filepath=str((OUT/'model.blend').resolve()))
bpy.ops.object.select_all(action='DESELECT')
for obj in C.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str((OUT/'model.glb').resolve()),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(opts)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Missing exporter settings '+repr(missing))
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(OUT/'model.glb',limits['max_triangles'],limits['max_materials'],limits['max_primitives']);glb['file']='model.glb'
b=source['bounds_blender_m'];expected_min=[b['min'][0],b['min'][2],-b['max'][1]];expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
if glb['errors'] or delta>1e-4 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>limits['max_glb_bytes']:raise RuntimeError('Export failed '+repr(glb['errors']))
for c in contacts:
 obj=bpy.data.objects['Limb '+c['limb']+' six podomeres'];c['actual_mesh_min_z_m']=min(v.co.z for v in obj.data.vertices)
report={'asset_id':'megarachne','revision':'r001','scope':'Source geometry and static exact-GLB technical checks, not independent visual or browser GPU approval','source':source,'glb':glb,'source_export_bounds_max_error_m':delta,'body_landmark_length_m':.54,'support_footprint_y_shift_m':-foot_y,'support_contacts':contacts,'frozen_budget':limits,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'exporter_options':{k:v for k,v in opts.items() if k!='filepath'},'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'inferred_anatomy':'T3-T12, telson, depths, joint completions and pose; unknown chelicerae and palps not exposed','source_scene_no_cameras_or_lights':not any(o.type in {'CAMERA','LIGHT'} for o in bpy.context.scene.objects)}
(OUT/'qa/evidence').mkdir(parents=True,exist_ok=True)
(OUT/'qa/evidence/source-technical.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print('MEGARACHNE_BUILD_OK',source['triangles'],glb['scene_primitives_estimated_base_draw_calls'],glb['bytes'],glb['semantic_sha256'])
