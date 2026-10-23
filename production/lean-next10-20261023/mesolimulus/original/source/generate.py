# SPDX-License-Identifier: MIT
"""Deterministic whole-living Mesolimulus walchi reconstruction, SMNS 65410.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUT
Only Blender and the declared sibling deps are required. No reference pixels embedded.
"""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, export_asset
P=json.loads((ROOT/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser(); a.add_argument('--output',type=Path,default=ROOT.parent); args=a.parse_args(argv)
OUT=args.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('mesolimulus',seed=P['seed'])
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
shell=make_material('Carapace muted umber','#77694E',roughness=.76)
rim=make_material('Marginal warm cuticle','#918166',roughness=.8)
limb=make_material('Jointed ventral limbs','#71604A',roughness=.85)
ventral=make_material('Ventral opercular cuticle','#A19475',roughness=.9)
eye=make_material('Small compound eyes','#272A22',roughness=.5)

class Part:
    def __init__(self,name,mats): self.name=name; self.mats=mats; self.v=[]; self.f=[]; self.mi=[]; self.groups={}
    def add(self,label,vs,fs,mat=0):
        k=len(self.v); self.v.extend([tuple(v) for v in vs]); self.f.extend([tuple(k+i for i in f) for f in fs]); self.mi.extend([mat]*len(fs)); self.groups.setdefault(label,[]).extend(range(k,k+len(vs)))
    def finish(self):
        ob=mesh_object(self.name,self.v,self.f,self.mats,C)
        for p,m in zip(ob.data.polygons,self.mi): p.material_index=m
        for label,ids in self.groups.items(): ob.vertex_groups.new(name=label).add(ids,1,'REPLACE')
        ob['construction']='Authored closed profile meshes; editable semantic vertex groups'; return ob

def tube(part,label,points,radii,mat=0,sides=8):
    ps=[Vector(p) for p in points]; vs=[]
    for i,p in enumerate(ps):
        tangent=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized(); ref=Vector((0,0,1))
        if abs(tangent.dot(ref))>.95: ref=Vector((1,0,0))
        u=tangent.cross(ref).normalized(); v=tangent.cross(u).normalized()
        for j in range(sides): vs.append(p+radii[i]*(math.cos(2*math.pi*j/sides)*u+math.sin(2*math.pi*j/sides)*v))
    fs=[tuple(range(sides-1,-1,-1))]
    for i in range(len(ps)-1):
        for j in range(sides): fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    fs.append(tuple((len(ps)-1)*sides+j for j in range(sides)))
    part.add(label,vs,fs,mat)

def ellipsoid(part,label,center,axes,mat=0,segments=12,rings=6):
    vs=[(center[0],center[1],center[2]+axes[2])]
    for i in range(1,rings):
        ph=math.pi*i/rings
        for j in range(segments):
            t=2*math.pi*j/segments; vs.append((center[0]+axes[0]*math.sin(ph)*math.cos(t),center[1]+axes[1]*math.sin(ph)*math.sin(t),center[2]+axes[2]*math.cos(ph)))
    bottom=len(vs); vs.append((center[0],center[1],center[2]-axes[2])); fs=[]
    for j in range(segments): fs.append((0,1+j,1+(j+1)%segments))
    for i in range(rings-2):
        for j in range(segments):
            k=1+i*segments; fs.append((k+j,k+segments+j,k+segments+(j+1)%segments,k+(j+1)%segments))
    k=1+(rings-2)*segments
    for j in range(segments): fs.append((k+j,bottom,k+(j+1)%segments))
    part.add(label,vs,fs,mat)

# Broad 104 mm shield, rounded anterior and sharply posterior genal corners.
prosoma=Part('Prosoma with marginal rim and ophthalmic ridges',[shell,rim])
outline=[]
for i in range(33):
    t=-math.pi/2+math.pi*i/32; outline.append((.052*math.sin(t),-.007-.048*math.cos(t)))
outline +=[(.0515,.002),(.050,.009),(.047,.018),(.043,.025),(.040,.016),(.036,.007),(.031,.002),(.023,.0005),(.012,0),(0,0),(-.012,0),(-.023,.0005),(-.031,.002),(-.036,.007),(-.040,.016),(-.043,.025),(-.047,.018),(-.050,.009),(-.0515,.002)]
# A constrained planar triangulation avoids radial-fan folding at the concave
# posterior shield boundary. Genal corners remain part of the single closed shell.
from mathutils.geometry import delaunay_2d_cdt
N=len(outline)
def inside(x,y):
    result=False
    for i,(ax,ay) in enumerate(outline):
        bx,by=outline[(i+1)%N]
        if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax: result=not result
    return result

def distance_border(x,y):
    p=Vector((x,y)); ds=[]
    for i,aa in enumerate(outline):
        av=Vector(aa); bv=Vector(outline[(i+1)%N]); d=bv-av
        t=max(0,min(1,(p-av).dot(d)/d.length_squared));ds.append((p-(av+t*d)).length)
    return min(ds)

coords=[Vector(p) for p in outline]
for j in range(24):
    y=-.052+j*.0033
    for i in range(31):
        x=-.0495+i*.0033
        if inside(x,y) and distance_border(x,y)>.001:coords.append(Vector((x,y)))
cv,ce,cf,co,_,_=delaunay_2d_cdt(coords,[],[list(range(N))],1,1e-8,True)
def cap_z(x,y):
    back_scale=1 if y<=-.020 else max(.25,1-(y+.020)*18)
    axial=.048 if y<-.007 else .040
    rad=(x/.052)**2+((y+.007)/axial)**2
    return .0065+.0225*(max(0,(1-rad-.08)/.92)**.75)*back_scale
vs=[(v.x,v.y,cap_z(v.x,v.y)) for v in cv]
fs=[tuple(f) for f in cf]; mids=[]
for f in fs:
    x=sum(vs[i][0] for i in f)/3;y=sum(vs[i][1] for i in f)/3
    mids.append(0)
# Matched lower skin, with closed sidewall and no artificial cavity or hole.
bot=len(vs); vs +=[(v.x,v.y,.0047) for v in cv]
fs +=[tuple(bot+i for i in reversed(f)) for f in cf];mids +=[0]*len(cf)
# Close exactly the returned triangulation boundary: CDT may subdivide or
# reorder constraint edges, so original point IDs must not be used as sidewalls.
from collections import Counter
edge_counts=Counter(tuple(sorted((f[j],f[(j+1)%len(f)]))) for f in cf for j in range(len(f)))
assert all(v in (1,2) for v in edge_counts.values()), 'Invalid constrained top surface'
for (q,r),count in edge_counts.items():
    if count==1: fs.append((q,bot+q,bot+r,r));mids.append(1)
prosoma.add('104mm horseshoe shield',vs,fs)
prosoma.mi=mids
# A continuous narrow cuticle band, rather than centroid-colored jagged triangles.
# Its bottom is shallowly embedded in the closed shell to avoid coplanar flicker.
ringv=[]
for i,(x,y) in enumerate(outline):
    a=Vector(outline[(i-1)%N]);b=Vector((x,y));c=Vector(outline[(i+1)%N])
    e1=(b-a).normalized();e2=(c-b).normalized()
    n1=Vector((-e1.y,e1.x));n2=Vector((-e2.y,e2.x));nn=(n1+n2).normalized()
    dist=min(.002,.0012/max(.2,nn.dot(n1)));inner=b+nn*dist
    z=cap_z(x,y)+.00022;zi=cap_z(inner.x,inner.y)+.00022
    ringv.extend([(x,y,z),(inner.x,inner.y,zi),(x,y,z-.0005),(inner.x,inner.y,zi-.0005)])
ringf=[]
for i in range(N):
    a=4*i;b=4*((i+1)%N)
    ringf += [(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)]
prosoma.add('continuous narrow marginal band',ringv,ringf,1)
# Ophthalmic ridges sit on the existing shell, small and subdued. No long eye spines.
# Surface height is interpolated from the authored radial triangulation at eye locations.
def shell_z(x,y):
    from mathutils.geometry import intersect_ray_tri
    origin=Vector((x,y,.06)); direction=Vector((0,0,-1)); highest=None
    for f in fs:
        for k in range(1,len(f)-1):
            hit=intersect_ray_tri(Vector(vs[f[0]]),Vector(vs[f[k]]),Vector(vs[f[k+1]]),direction,origin,True)
            if hit is not None: highest=max(highest or -1,hit.z)
    return highest if highest is not None else .02
for s in [-1,1]:
    ridge_xy=[(s*.016,-.032),(s*.020,-.025),(s*.022,-.017),(s*.023,-.009),(s*.021,-.003)]
    tube(prosoma,('left' if s<0 else 'right')+' ophthalmic ridge',[(x,y,shell_z(x,y)+.0002) for x,y in ridge_xy],[.0004,.00075,.00085,.0007,.0002],0,6)
pro=prosoma.finish()
# Mixed normals: smoothly shaded broad dorsal shell, faceted rim/ridges/limbs.
for polygon in pro.data.polygons:
    if polygon.index < len(cf) and polygon.material_index==0: polygon.use_smooth=True

# One fused compact rear shield, not a stack of independent abdomen plates.
rear=Part('Fused thoracetron with articulated marginal spines',[shell])
ro=[(-.029,-.0005),(.029,-.0005),(.035,.010),(.033,.020),(.027,.030),(.018,.040),(.007,.044),(-.007,.044),(-.018,.040),(-.027,.030),(-.033,.020),(-.035,.010)]
n=len(ro); rv=[(0,.017,.022)]
for r in [.3,.6,.85,1]:
    for x,y in ro:
        yy=.017+r*(y-.017)
        hinge=.006*max(0,1-(yy/.014)**2) if yy<.014 else 0
        rv.append((r*x,yy,.009+.013*(1-r*r)+hinge))
rf=[]
for j in range(n): rf.append((0,1+j,1+(j+1)%n))
for k in range(3):
    for j in range(n): rf.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
b=len(rv)
for x,y in ro: rv.append((x,y,.0068))
for j in range(n): rf.append((1+3*n+j,b+j,b+(j+1)%n,1+3*n+(j+1)%n))
c=len(rv); rv.append((0,.017,.0075))
for j in range(n): rf.append((c,b+(j+1)%n,b+j))
rear.add('single fused thoracetron',rv,rf)
spines=[(.034,.009,.010),(.034,.015,.010),(.032,.022,.010),(.029,.028,.010),(.0245,.034,.0085),(.018,.040,.0065)]
for s in [-1,1]:
    for i,(x,y,l) in enumerate(spines):
        # Gently swept rather than radial fan; separate short articulated shafts.
        tube(rear,f'{s:+d} articulated thoracetronic spine {i+1}',[(s*x,y,.009),(s*(x+l*.35),y+.001,.0084),(s*(x+l),y+.004,.0069)],[.0012,.0010,.00012],sides=6)
        ellipsoid(rear,f'{s:+d} spine socket {i+1}',(s*x,y,.009),(.0016,.0018,.0015),segments=8,rings=4)
rear.finish()

# All six main prosomal pairs are independently named and retained as vertex groups.
legs=Part('Six paired prosomal appendages',[limb])
for s in [-1,1]:
    side='L' if s<0 else 'R'
    chel=[(s*.004,-.025,.007),(s*.006,-.031,.0045),(s*.007,-.038,.0027)]
    tube(legs,side+' chelicera',chel,[.0015,.0011,.0008])
    for d in [-1,1]: tube(legs,side+' chelicera small pincer',[(s*.007,-.0375,.0027),(s*(.007+d*.0012),-.040,.002),(s*.007,-.041,.0018)],[.00065,.0004,.00018],sides=6)
    for i in range(4):
        y=-.020+i*.0085
        # Walking limbs radiate under the shield, with two distal segments returning to floor.
        ys=[-.042,-.025,-.006,.015][i]
        xs=[.035,.045,.048,.044][i]
        ps=[(s*.006,y,.008),(s*.017,y-.003,.0059),(s*.029,y+(-.009+i*.004),.006),(s*xs,ys,.0022)]
        tube(legs,f'{side} walking pair {i+1}',ps,[.0021,.0019,.00145,.00085])
        for k,p in enumerate(ps[1:-1]): ellipsoid(legs,f'{side} walking {i+1} joint {k+1}',p,(.0021,.0021,.002),segments=8,rings=4)
        for d in [-1,1]:
            # Conservative small pincers, not lobster-sized claws.
            tube(legs,f'{side} walking {i+1} pincer',[(s*xs,ys,.0022),(s*(xs+d*.0015),ys-.002,.001),(s*xs,ys-.0034,.00065)],[.0008,.00048,.00018],sides=6)
    ps=[(s*.008,.008,.008),(s*.018,.012,.0068),(s*.029,.019,.005),(s*.037,.029,.0019)]
    tube(legs,side+' pushing leg',ps,[.0025,.0022,.0018,.0011])
    for k,p in enumerate(ps[1:-1]): ellipsoid(legs,side+f' pushing joint {k+1}',p,(.0024,.0024,.0021),segments=8,rings=4)
    for d in [-1,0,1]:
        tube(legs,side+' pushing foot conservative terminal',[(s*.037,.028,.0019),(s*(.038+d*.002),.033,.0014),(s*(.0385+d*.0023),.035,.001)],[.0009,.0010,.0004],sides=6)
legs.finish()

covers=Part('Shallow ventral opercular and book-gill covers',[ventral])
# The six broad overlapping shallow covers are generic limulid inference only.
for i in range(6):
    ellipsoid(covers,('genital opercular cover' if i==0 else f'book-gill cover {i}'),(0,.008+i*.0054,.0052-i*.00012),(.024-i*.0021,.0054,.00125),segments=20,rings=4)
covers.finish()
eyes=Part('Paired small lateral eyes',[eye])
for s in [-1,1]:
    x,y=s*.022,-.017
    ellipsoid(eyes,('L' if s<0 else 'R')+' lateral compound eye',(x,y,shell_z(x,y)+.0008),(.0017,.0025,.0011),segments=12,rings=6)
eyes.finish()
# Straight triangular-section telson. It is a balancing tail spine, never a stinger.
tail=Part('Straight tapering articulated telson',[shell])
tube(tail,'80mm straight telson',[(0,.043,.0092),(0,.050,.010),(0,.095,.006),(0,.123,.0032)],[.0030,.0029,.00135,.00018],sides=3)
ellipsoid(tail,'telson hinge',(0,.0435,.0092),(.0035,.003,.0025),segments=10,rings=4)
tail.finish()
# Lift is preserved. Place the lowest intended walking tip precisely at floor.
meshes=[o for o in C.all_objects if o.type=='MESH']
low=min(v.co.z for ob in meshes for v in ob.data.vertices)
for ob in meshes:
    for v in ob.data.vertices: v.co.z-=low
root=bpy.data.objects[C['asset_root']]; root['published_prosomal_width_m']=.104
root['reconstruction']='Whole living reconstruction; ventral details, height and muted colors inferred.'
meta={'generator':'source/generate.py','generator_seed':P['seed'],
      'reconstruction_notes':['Only prosomal width 0.104 m directly published for SMNS 65410; other dimensions are estimates or inferences.','No exposed muscles or death-track geometry.','One cheliceral pair, four walking pairs, one pushing pair. Six inferred opercular/book-gill covers are not microscopic anatomy.'],
      'description':{'en':'Complete living reconstruction of Jurassic Mesolimulus walchi anchored to SMNS 65410.','zh':'以 SMNS 65410 为锚点的侏罗纪 Mesolimulus walchi 完整活体复原。'}}
record=export_asset('mesolimulus',{'en':'Mesolimulus walchi','zh':'中鲎'},'arthropods',C,metadata=meta,output_root=OUT/'private'/'helper-export',render=False,max_triangles=40000,max_materials=6,max_primitives=8)
raw=OUT/'private'/'helper-export'/'mesolimulus'
shutil.copy2(raw/'mesolimulus.glb',OUT/'model.glb'); shutil.copy2(raw/'mesolimulus.blend',OUT/'model.blend')
(OUT/'qa'/'evidence').mkdir(parents=True,exist_ok=True)
shutil.copy2(raw/'qa.json',OUT/'qa'/'evidence'/'source-export.json')
record['glb']='model.glb'; record['blend']='model.blend'; record['preview']='preview.png'
(OUT/'qa'/'evidence'/'build-metadata.json').write_text(json.dumps(record,indent=2)+'\n')
semantic={'main_appendage_pairs':6,'chelicera_pairs':1,'walking_pairs':4,'pushing_pairs':1,'opercular_and_bookgill_covers':6,'thoracetronic_lateral_spine_pairs':6,
          'prosomal_width_m':.104,'telson_length_m':.08,'source_groups':{o.name:list(o.vertex_groups.keys()) for o in meshes},'minimum_floor_z_before_shift':low,
          'notes':'Appendage groups describe actual authored components. Pair types and cover details are conservative limulid reconstruction, not every structure observed on SMNS 65410.'}
(OUT/'qa'/'evidence'/'anatomy-build.json').write_text(json.dumps(semantic,indent=2)+'\n')
print('MODEL_COMPLETE',OUT/'model.glb')
