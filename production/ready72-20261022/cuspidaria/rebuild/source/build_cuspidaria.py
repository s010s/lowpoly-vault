# SPDX-License-Identifier: MIT
"""Original analytic single-valve surface; reference-informed, not image traced."""
import bpy,sys,json,math,hashlib,argparse,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'deps'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
args=sys.argv[sys.argv.index('--')+1:]
p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--out',required=True);p.add_argument('--clay',action='store_true');a=p.parse_args(args)
C=json.loads(Path(a.config).read_text());S=C['length_m']/8.0
coll=setup_scene('cuspidaria',seed=C['seed'])
# Original shape controls in millimetre-like design units. Not digitized from pixels.
outline=[(-4,2.32),(-3.85,2.62),(-3.05,2.77),(-2.2,2.96),(-1.3,3.26),(-0.50,3.62),(0.10,4.04),(0.57,4.55),(1.02,4.76),(1.69,4.64),(2.57,4.13),(3.43,3.37),(3.96,2.53),(3.92,1.76),(3.35,0.88),(2.45,0.28),(1.42,0.02),(0.49,0.08),(-0.25,0.38),(-0.80,0.93),(-1.10,1.48),(-1.64,1.89),(-2.34,2.05),(-3.18,2.12),(-3.85,2.15)]
def catmull(p0,p1,p2,p3,t):
    return tuple(0.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t) for k in range(2))
bound=[]
for i in range(len(outline)):
    for j in range(C['boundary_samples_per_control']):
        bound.append(catmull(outline[(i-1)%len(outline)],outline[i],outline[(i+1)%len(outline)],outline[(i+2)%len(outline)],j/C['boundary_samples_per_control']))
# Normalize the designed outline only, not the delivered specimen's scientific dimensions.
minx,maxx=min(x for x,z in bound),max(x for x,z in bound); minz,maxz=min(z for x,z in bound),max(z for x,z in bound)
bound=[((x-minx)/(maxx-minx)*8-4,(z-minz)/(maxz-minz)*8*C['height_length_ratio']) for x,z in bound]
cx,cz=0.80,3.25;N=len(bound);verts=[];faces=[];regions=[]
def vtx(x,y,z): verts.append((x*S,y*S,z*S));return len(verts)-1
def surf(r,x,z):
    body=0.28+0.72/(1+math.exp(-2.5*(x+1.25)))
    dome=1.37*max(0,1-r*r)**0.66*body
    body_relief=1/(1+math.exp(-4*(x+0.45)))
    ripple=0.016*math.sin(r*math.pi*14.5+0.4)*math.sin(math.pi*r)**0.8*body_relief
    return -0.065-dome-ripple
center=vtx(cx,surf(0,cx,cz),cz);rings=[]
for r in C['growth_rings']:
    ring=[]
    for bx,bz in bound:
        x=cx+r*(bx-cx);z=cz+r*(bz-cz)
        ring.append(vtx(x,surf(r,x,z),z))
    rings.append(ring)
for i in range(N):faces.append((center,rings[0][i],rings[0][(i+1)%N]));regions.append(0)
for j in range(len(rings)-1):
    for i in range(N):
        ni=(i+1)%N;aa,bb,cc,dd=rings[j][i],rings[j][ni],rings[j+1][ni],rings[j+1][i]
        faces.extend([(aa,bb,cc),(aa,cc,dd)]);regions.extend([0,0])
# Quiet technical rear disk and a thin perimeter lip, not an anatomical inner valve.
back=[]
for x,z in bound: back.append(vtx(x,0.050,z))
backcenter=vtx(cx,0.050,cz)
for i in range(N):
    ni=(i+1)%N
    faces.extend([(rings[-1][i],back[i],back[ni]),(rings[-1][i],back[ni],rings[-1][ni]),(backcenter,back[ni],back[i])]);regions.extend([1,1,1])
materials=[make_material('Exterior fossil clay','#A6A6A6' if a.clay else C['palette']['exterior'],roughness=.90),make_material('Technical back closure','#A6A6A6' if a.clay else C['palette']['back'],roughness=.95)]
obj=mesh_object('Single valve exterior and technical closure',verts,faces,materials,coll)
for poly,r in zip(obj.data.polygons,regions):poly.material_index=r
obj['representation']='single fossil valve exterior study';obj['back_is_artistic_technical_closure']=True
obj['scale_note']=C['scale_evidence'];obj['landmarks']='rounded inflated body; umbonal shoulder; narrow blunt posterior rostrum'
obj.data.calc_loop_triangles()
import bmesh
bm=bmesh.new();bm.from_mesh(obj.data)
volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);bad=sum(not e.is_manifold for e in bm.edges);bm.free()
if volume<=0 or boundary or bad:raise RuntimeError('Closed volume topology failed')
# A shallow concave profile constrains the growth fan to its visibility kernel.
# Fail before export if moving its center would fold the surface or rear cap.
areas=[]
for tri in obj.data.loop_triangles:
    if obj.data.polygons[tri.polygon_index].material_index!=0:continue
    p0,p1,p2=[obj.data.vertices[i].co for i in tri.vertices]
    areas.append((p1.x-p0.x)*(p2.z-p0.z)-(p1.z-p0.z)*(p2.x-p0.x))
if min(areas)<=1e-14:raise RuntimeError('Exterior fan leaves profile kernel: projected fold')
from mathutils.bvhtree import BVHTree
triangles=[tuple(t.vertices) for t in obj.data.loop_triangles]
tree=BVHTree.FromPolygons([v.co for v in obj.data.vertices],triangles,all_triangles=True,epsilon=0.0)
if any(i<j and not(set(triangles[i])&set(triangles[j])) for i,j in tree.overlap(tree)):
    raise RuntimeError('Nonadjacent BVH overlap; revise geometry before export')
record=export_asset('cuspidaria',{'en':'Cuspidaria single fossil valve','zh':'Cuspidaria 单瓣化石外形'},'animals',coll,metadata={'description':{'en':'Evidence-informed exterior study of a Pliocene rostrate bivalve. Technical back and depth are artistic.','zh':'依据上新世长吻双壳化石外观的单瓣研究；背面闭合和厚度为美术补全。'},'generator':'source/build_cuspidaria.py','source_scale_note':C['scale_evidence'],'representation':'fossil-specimen','taxon':'Cuspidaria','reference_specimen':'MNHN.F.J04629','reference_url':'https://science.mnhn.fr/institution/mnhn/collection/f/item/j04629','scientific_scope':'Single-valve exterior, not internal anatomy or full paired reconstruction.'},output_root=Path(a.out),render=False,max_triangles=C['max_triangles'],max_materials=2,max_primitives=2)
dest=Path(a.out)/'cuspidaria'
ext=bpy.ops.export_scene.gltf.get_rna_type()
report={'built_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest(),'blender':bpy.app.version_string,'source_vertices':len(verts),'source_triangles':len(obj.data.loop_triangles),'boundary_edges':boundary,'nonmanifold_edges':bad,'signed_volume_m3':volume,'connected_components':1,'clay_blockout':a.clay,'description':'Single closed star-domain outer height field and planar rear technical closure; continuous rings, no detached parts.'}
(dest/'build-record.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
