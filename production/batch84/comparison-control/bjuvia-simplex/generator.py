# SPDX-License-Identifier: MIT
"""Original fossil blade/net generator and explicitly non-delivery neutral control, after scope freeze."""
import bpy,sys,json,math,pathlib,argparse,random
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);control=cfg.get('comparison_control',False);slug=cfg['asset_id'];col=setup_scene(slug,84);m={k:make_material(k,v) for k,v in cfg['palette'].items()};vs=[];fs=[];mi=[];keys=list(m)
def addmesh(vertices,faces,mat):
 base=len(vs);vs.extend(vertices)
 for f in faces:fs.append(tuple(base+i for i in f));mi.append(keys.index(mat))
def plate(outline,z0,z1,mat):
 n=len(outline);v=[(x,y,z0) for x,y in outline]+[(x,y,z1) for x,y in outline];v.extend([(0,0,z0),(0,0,z1)]);f=[]
 for i in range(n):
  q=(i+1)%n;f += [(i,q,n+q,n+i),(2*n,q,i),(2*n+1,n+i,n+q)]
 addmesh(v,f,mat)
N=60;outline=[]
for i in range(N):
 t=math.tau*i/N;r=1+.035*math.sin(t*5+.7)+.025*math.cos(t*7);outline.append((.0375*r*math.cos(t),.0975*r*math.sin(t)))
plate(outline,0,.005,'matrix')
def width(t):return .029*max(0,math.sin(math.pi*t))**.55*(.82+.18*t)*min(1,max(.01,t/.15))**.23
outline=[(-width(t),-.08+.16*t) for t in [i/64 for i in range(65)]]+[(width(t),-.08+.16*t) for t in [i/64 for i in range(63,0,-1)]]
# Top/bottom fan centers lie strictly inside this convex outline. Original full-volume slab and blade relief.
plate(outline,.0048,.00545,'leaf')
height=cfg['vein_ridge_height_m'];half=cfg['vein_ridge_halfwidth_m'];top=.00545
# Continuous closed triangular-prism ridges: bases embedded below leaf surface; no coplanar overlays.
def ridge(p,q,w=half,h=height):
 x,y=p;xx,yy=q;dx=xx-x;dy=yy-y;L=math.hypot(dx,dy)
 if L<1e-7:return
 nx=-dy/L*w;ny=dx/L*w
 v=[(x-nx,y-ny,top-.00009),(x+nx,y+ny,top-.00009),(x,y,top+h),(xx-nx,yy-ny,top-.00009),(xx+nx,yy+ny,top-.00009),(xx,yy,top+h)]
 addmesh(v,[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)],'vein')
ridge((0,-.078),(0,.077),w=.00065,h=.00031)
rows=cfg['vein_rows_per_side']
for sign in [-1,1]:
 curves=[]
 for j in range(rows):
  t=.065+j*(.86/(rows-1));y=-.08+.16*t
  if control:
   # Source-supported Bjuvia transverse parallel side veins, with a short basal dichotomy on alternate veins.
   end=sign*width(t)*.975;ridge((sign*.0007,y),(end,y+.0006))
   if j%2==0:ridge((sign*.003,y),(end,y+.0021))
  else:
   pts=[]
   for k,s in enumerate([.02,.26,.53,.76,.96]):
    yy=y+.014*s*(.90-.25*t)+.0007*math.sin(j*1.7+s*3)*s
    tt=(yy+.08)/.16
    pts.append((sign*width(tt)*s,yy))
   for p,q in zip(pts,pts[1:]):ridge(p,q)
   curves.append(pts)
 if not control:
  for j in range(rows-1):
   # Short unequal connecting branches close elongated polygonal meshes in actual geometric relief.
   for k in [1,2,3]:
    p=curves[j][k];q0=curves[j+1][k];q1=curves[j+1][min(4,k+1)];f=.35+.12*math.sin(j*1.4+k)
    q=(q0[0]*(1-f)+q1[0]*f,q0[1]*(1-f)+q1[1]*f);ridge(p,q,w=half*.80,h=height*.88)
o=mesh_object('non_delivery_Bjuvia_simplex_parallel_vein_control' if control else 'single_Glossopteris_browniana_fossil_leaf_polygonal_reticulate_vein_relief',vs,fs,[m[k] for k in keys],col)
for p,i in zip(o.data.polygons,mi):p.material_index=i
o['scope']='Non-delivery same-outline neutral control only, no whole Bjuvia reconstruction' if control else 'Original fossil teaching relief, not living whole organism or source scan'
o['intended_embedded_contacts']='Blade base embedded in slab, ridge bases embedded in blade; vein junction intersections intentional natural network, not floating/copanar overlays.'
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'));bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',comparison_control=control),indent=2)+'\n');print('BUILT',slug,qa['scene_triangles'],qa['bytes'])
