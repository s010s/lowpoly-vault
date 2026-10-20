# SPDX-License-Identifier: MIT
"""Original batch60 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
import bpy,sys,json,math,argparse,pathlib,datetime,hashlib
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True)
slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};groups={}
def part(name,vs,fs,mat):
 v,f=groups.setdefault((name,mat),([],[]));n=len(v);v.extend(vs);f.extend([tuple(n+i for i in face) for face in fs])
def loft(name,rings,mat):
 n=len(rings[0]);vs=[p for ring in rings for p in ring];fs=[tuple(range(n-1,-1,-1))]
 for j in range(len(rings)-1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 fs.append(tuple((len(rings)-1)*n+i for i in range(n)));part(name,vs,fs,mat)
def tube(name,points,radii,mat,n=6):
 rings=[]
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);tangent.normalize();ref=Vector((0,0,1)) if abs(tangent.z)<.95 else Vector((1,0,0));u=tangent.cross(ref).normalized();w=tangent.cross(u).normalized()
  rings.append([tuple(Vector(p)+radii[i]*(u*math.cos(j*math.tau/n)+w*math.sin(j*math.tau/n))) for j in range(n)])
 loft(name,rings,mat)
def ellipsoid(name,c,r,mat,n=12,k=6):
 rings=[]
 for j in range(k+1):
  t=-math.pi/2+.15+(math.pi-.30)*j/k
  rings.append([(c[0]+r[0]*math.cos(t)*math.cos(i*math.tau/n),c[1]+r[1]*math.cos(t)*math.sin(i*math.tau/n),c[2]+r[2]*math.sin(t)) for i in range(n)])
 loft(name,rings,mat)


# Original targeted corrective geometry, after r002 repair freeze.
# The original brief and composition are preserved verbatim.
rings=[]
for z,scale in [(0,.88),(.07,1),(.14,.91)]:
 rings.append([(1.15*scale*(1+.06*math.sin(i*2.3))*math.cos(i*math.tau/24),.85*scale*(1+.08*math.sin(i*1.7))*math.sin(i*math.tau/24),z) for i in range(24)])
loft('low_irregular_floor_mineral_crust',rings,'floor')
columns=[(0,.27,2.1,.28),(-.61,.04,1.45,.23),(.60,.20,1.15,.24),(-.35,-.44,.83,.21),(.56,-.40,.55,.19)]
for ci,(x,y,h,r) in enumerate(columns):
 rings=[];n=32;ns=36;phase=ci*1.319
 # Unequal height locations and weak amplitudes, not a periodic stacked-ring profile.
 terrace_positions=[.17+.025*math.sin(ci*1.2),.36+.04*math.cos(ci),.58+.027*math.sin(ci+1),.76+.025*math.cos(ci*2)]
 for j in range(ns):
  t=j/(ns-1)*.9999;cap=math.sqrt(max(.0001,1-((t-.86)/.14)**2)) if t>.86 else 1
  envelope=1.38-.54*t-.10*math.sin(math.pi*t)
  cx=x+.035*math.sin(t*2.5+phase)*t;cy=y+.025*math.sin(t*3.1+phase*.7)*t
  ring=[]
  for i in range(n):
   ang=i*math.tau/n
   # Five continuous asymmetric drip buttresses, slow twist avoids vertical machine grooves.
   ridge=0
   for q in range(5):
    center=q*math.tau/5+.16*math.sin(q*2.1+phase)+.10*math.sin(t*2.8+q)
    delta=math.atan2(math.sin(ang-center),math.cos(ang-center))
    amplitude=.24+.13*math.sin(q*1.6+phase)**2
    ridge+=amplitude*math.exp(-(delta/.30)**2)*(.52+.48*math.sin(math.pi*t)**.5)
   fine=.018*math.cos(ang*9+.32*math.sin(t*4+phase))
   # Weak irregular deposition terraces, warped by angular drip pattern and differing heights.
   terrace=0
   for q,pos in enumerate(terrace_positions):
    warped=pos+.025*math.sin(ang*2+q+phase)+.014*math.cos(ang*3+phase)
    terrace+=(.012+.007*math.sin(q+ci)**2)*math.exp(-((t-warped)/(.032+.01*(q%2)))**2)
   radial=r*envelope*cap*(1+ridge+fine+terrace)
   ring.append((cx+radial*math.cos(ang),cy+radial*(.95+.025*math.sin(ang+phase))*math.sin(ang),.10+h*t))
  rings.append(ring)
 loft('solid_rounded_stalagmite_'+str(ci+1)+'_irregular_longitudinal_drips',rings,'mineral')
for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if mat=='mineral':
  obj.data.materials.append(m['light']);obj.data.materials.append(m['ochre'])
  # No regular height-band colors. Restrained long mineral variations follow vertical drips.
  ci=int(name.split('_')[3])-1;x,y,h,r=columns[ci]
  for poly in obj.data.polygons:
   c=poly.center;ang=math.atan2(c.y-y,c.x-x);t=(c.z-.10)/h
   poly.material_index=1 if poly.normal.z>.60 and t>.88 else 0

ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
