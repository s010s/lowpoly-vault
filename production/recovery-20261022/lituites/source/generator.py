# SPDX-License-Identifier: MIT
"""New Lituites maker build, not recovered historical code or exact museum replica.
Observed source-side silhouette; explicit inferred volumetric depth. No source image
is embedded. One closed mineral fossil surface, no terminal aperture or coil tunnel.
"""
import argparse,json,pathlib,sys,math,hashlib,datetime,collections,bisect
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent/'helpers'))
import bpy
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from asset_common import setup_scene,make_material,mesh_object,export_asset

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=pathlib.Path);p.add_argument('--output-dir',required=True,type=pathlib.Path)
 args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);c=json.loads(args.config.read_text());R=pathlib.Path(__file__).resolve().parent.parent;out=args.output_dir
 if out.exists() and any(out.iterdir()):raise RuntimeError('Output must be new empty attempt directory')
 out.mkdir(parents=True,exist_ok=True);q=json.loads((R/c['outline_source']).read_text());poly=q['outline_xz_mm'];N=len(poly)
 def inside(x,z):
  yes=False
  for (ax,az),(bx,bz) in zip(poly,poly[1:]+poly[:1]):
   if (az>z)!=(bz>z) and x<(bx-ax)*(z-az)/(bz-az)+ax:yes=not yes
  return yes
 def border_distance(x,z):
  best=1e6
  for (ax,az),(bx,bz) in zip(poly,poly[1:]+poly[:1]):
   vx,vz=bx-ax,bz-az;d=vx*vx+vz*vz;t=max(0,min(1,((x-ax)*vx+(z-az)*vz)/d)) if d else 0
   best=min(best,math.hypot(x-ax-t*vx,z-az-t*vz))
  return best
 # Exact polygon intersections replace raster-row jumps in depth parameterization.
 def cross_intervals(z):
  xs=[]
  for (ax,az),(bx,bz) in zip(poly,poly[1:]+poly[:1]):
   if (az>z)!=(bz>z):xs.append(ax+(bx-ax)*(z-az)/(bz-az))
  xs.sort();return [(xs[i],xs[i+1]) for i in range(0,len(xs)-1,2)]
 def span(z,x=None):
  ints=cross_intervals(z)
  if not ints:return -10.5-.0001,-10.5+.0001
  if x is not None:
   for lo,hi in ints:
    if lo-1e-5<=x<=hi+1e-5:return lo,hi
  return max(ints,key=lambda p:p[1]-p[0])
 points=[Vector(v) for v in poly];constraints=[(i,(i+1)%N) for i in range(N)]
 def addp(x,z,minimum=.12):
  # Boundary section endpoints are permitted. Other points must stay inside.
  if not inside(x,z) and border_distance(x,z)>1e-6:return None
  v=Vector((x,z))
  for i,p in enumerate(points):
   if (v-p).length<minimum:return i
  points.append(v);return len(points)-1
 def edge(a,b):
  if a is not None and b is not None and a!=b:constraints.append((a,b))
 # Match every observed source-border station with an inward angular support station.
 # This removes long unmatched triangles between a high-resolution silhouette edge and coarse rings.
 supports={}
 for i,(x,zz) in enumerate(poly):
  if zz<24:continue
  candidates=[]
  for ztest in [zz,zz+1e-5,zz-1e-5]:
   for lo,hi in cross_intervals(ztest):
    candidates.extend([(abs(x-lo),lo,hi,1),(abs(x-hi),lo,hi,-1)])
  if not candidates:continue
  error,lo,hi,side=min(candidates)
  if error>.002:continue
  inward=(hi-lo)*.5*(1-math.cos(math.pi/c['section_half_segments']))
  ix=addp(x+side*inward,zz,.025)
  if ix is not None and ix!=i:supports[i]=(ix,side)
 for i in range(N):
  j=(i+1)%N
  if i in supports and j in supports and supports[i][1]==supports[j][1]:edge(supports[i][0],supports[j][0])
 # Coherent section rings and angular lanes; boundary still follows every frozen source vertex.
 prev=None;z=c['section_start_z_mm'];section_count=0
 while z<283.8:
  lo,hi=span(z,c['coil_center_xz_mm'][0]-c['coil_ridge_radii_mm'][-1] if z<30 else None);mid=(lo+hi)/2;rad=(hi-lo)/2;ring=[]
  for j in range(c['section_half_segments']+1):
   if j in (1,c['section_half_segments']-1):ring.append(None);continue
   x=mid-rad*math.cos(math.pi*j/c['section_half_segments']);ring.append(addp(x,z,.03))
  valid_ring=[v for v in ring if v is not None]
  for u,v in zip(valid_ring,valid_ring[1:]):edge(u,v)
  if prev:
   for j in range(1,len(ring)-1):edge(prev[j],ring[j])
  prev=ring;section_count+=1;z+=c['section_spacing_mm']*(1+.10*math.sin(section_count*1.37))
 # One expanding clockwise whorl centerline and its continuous emerging-shaft bridge.
 # All transverse width/depth choices are explicitly inferred; no external tube is unioned.
 xc,zc=c['coil_center_xz_mm'];turn=c['coil_ridge_turns']*2*math.pi;r0,r1=c['coil_ridge_radii_mm'];k=math.log(r1/r0)/turn
 whorl=[]
 for j in range(433):
  t=turn*j/432;rad=r0*math.exp(k*t);ang=-t
  whorl.append((xc+rad*math.cos(ang),zc+rad*math.sin(ang),.18+c['coil_ridge_width_factor']*rad))
 start=whorl[-1];lo,hi=span(36);end=((lo+hi)/2,36,(hi-lo)/2)
 p0=start[:2];p1=(p0[0]-1.0,p0[1]+6);p2=(end[0]-2.0,29);p3=end[:2]
 for j in range(1,81):
  t=j/80;s=1-t;x=s*s*s*p0[0]+3*s*s*t*p1[0]+3*s*t*t*p2[0]+t*t*t*p3[0];zz=s*s*s*p0[1]+3*s*s*t*p1[1]+3*s*t*t*p2[1]+t*t*t*p3[1]
  whorl.append((x,zz,start[2]*(1-t)+end[2]*t))
 # Curved lanes follow the rounded whorl body rather than a narrow subtractive groove.
 previous=[None]*5
 for j in range(0,len(whorl),3):
  x,zz,w=whorl[j]
  if zz>24:break
  pa=whorl[max(0,j-1)];pb=whorl[min(len(whorl)-1,j+1)];dx,dz=pb[0]-pa[0],pb[1]-pa[1];ln=math.hypot(dx,dz);nx,nz=-dz/ln,dx/ln
  current=[]
  for lane,factor in enumerate([-.82,-.46,0,.46,.82]):
   ix=addp(x+factor*w*nx,zz+factor*w*nz,.24);current.append(ix);edge(previous[lane],ix)
  for u,v in zip(current,current[1:]):edge(u,v)
  previous=current
 # Sparse polar support fills the mineral valleys and maintains low-poly readable broad planes.
 r=.45
 while r<21:
  count=max(16,round(c['coil_polar_angles']*min(1,r/8)))
  for j in range(count):
   a=2*math.pi*j/count+.06*math.sin(r);x=xc+r*math.cos(a);zz=zc+r*math.sin(a)
   if zz<24 and inside(x,zz) and border_distance(x,zz)>.18:addp(x,zz,.36)
  r+=c['coil_polar_step_mm']
 verts2,ed,tri,origv,orige,origf=delaunay_2d_cdt(points,constraints,[list(range(N))],1,c['cdt_construction_epsilon_mm'],True)
 verts2=[tuple(v) for v in verts2];raw_cdt_faces=len(tri)
 tri=[tuple(f) for f in tri if inside(sum(verts2[v][0] for v in f)/len(f),sum(verts2[v][1] for v in f)/len(f))]
 excluded_outside_cdt_faces=raw_cdt_faces-len(tri)
 polygon_area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2
 triangle_area=sum(abs((verts2[t[1]][0]-verts2[t[0]][0])*(verts2[t[2]][1]-verts2[t[0]][1])-(verts2[t[1]][1]-verts2[t[0]][1])*(verts2[t[2]][0]-verts2[t[0]][0]))/2 for t in tri)
 if abs(polygon_area-triangle_area)>.05:raise RuntimeError('Source polygon and emitted interior triangle area differ')
 if any(len(t)!=3 for t in tri):raise RuntimeError('CDT did not return triangles')
 edge_use=collections.Counter(tuple(sorted((a,b))) for f in tri for a,b in zip(f,f[1:]+f[:1]));boundary={v for e,n in edge_use.items() if n==1 for v in e}
 # Prevent zero-thickness internal chords connecting two boundary vertices.
 # Split such interior edges and rebuild affected triangles with an interior centroid.
 split={}
 for e,n in edge_use.items():
  if n==2 and all(v in boundary for v in e):
   split[e]=len(verts2);verts2.append(tuple((verts2[e[0]][i]+verts2[e[1]][i])/2 for i in range(2)))
 newtri=[]
 for f in tri:
  ring=[]
  for u,v in zip(f,f[1:]+f[:1]):
   ring.append(u)
   if tuple(sorted((u,v))) in split:ring.append(split[tuple(sorted((u,v)))])
  if len(ring)>3:
   mid=len(verts2);verts2.append(tuple(sum(verts2[v][i] for v in f)/3 for i in range(2)))
   newtri.extend((u,v,mid) for u,v in zip(ring,ring[1:]+ring[:1]))
  else:newtri.append(f)
 tri=newtri
 def smoothstep(t):
  t=max(0,min(1,t));return t*t*(3-2*t)
 def height(x,z):
  lo,hi=span(z,x);mid=(lo+hi)/2;rad=(hi-lo)/2;u=max(-1,min(1,(x-mid)/max(.0001,rad)));fade=math.sqrt(max(0,1-u*u));ratio=.895+min(1,max(0,(z-28)/170))*.105
  shaft=min(16,rad*ratio)*fade
  if z>30:return max(.12,shaft)
  # Actual rounded volume envelope, not a material/normal illusion or a flat disk with cut marks.
  peak=0.0
  for a,b in zip(whorl,whorl[1:]):
   dx,dz=b[0]-a[0],b[1]-a[1];ll=dx*dx+dz*dz;t=max(0,min(1,((x-a[0])*dx+(z-a[1])*dz)/max(ll,1e-12)))
   px,pz=a[0]+t*dx,a[1]+t*dz;w=a[2]*(1-t)+b[2]*t;d2=(x-px)**2+(z-pz)**2
   if d2<w*w:peak=max(peak,c['coil_ridge_depth_ratio']*math.sqrt(w*w-d2))
  r=math.hypot(x-xc,z-zc);core=1.05*math.sqrt(max(0,1-(r/1.65)**2))
  floor=c['coil_mineral_floor_mm']
  # Smooth convex combination avoids a sharp mineral-fill ledge; center remains solid.
  coil=(floor+math.sqrt(peak*peak+core*core)) * math.sqrt(smoothstep(border_distance(x,z)/1.4))
  blend=smoothstep((z-22)/8);v=coil*(1-blend)+shaft*blend
  return max(.12,v)
 vv=[];front={};back={}
 for i,(x,z) in enumerate(verts2):
  if i in boundary:
   front[i]=back[i]=len(vv);vv.append((x*.001,0,z*.001))
  else:
   y=height(x,z);cap=max(0,min(1,(z+2*x-243)/19));front_y=y*(1-.48*cap)
   front[i]=len(vv);vv.append((x*.001,-front_y*.001,z*.001));back[i]=len(vv);vv.append((x*.001,y*.001,z*.001))
 ff=[];mat_ids=[]
 for f in tri:
  x=sum(verts2[v][0] for v in f)/3;z=sum(verts2[v][1] for v in f)/3;cap=z+2*x>248 and z>210
  ff.append(tuple(front[v] for v in f));mat_ids.append(1 if cap else 0)
  ff.append(tuple(back[v] for v in reversed(f)));mat_ids.append(0)
 col=setup_scene(c['asset_id'],c['seed']);mats=[make_material('weathered-limestone',c['palette']['mineral'],.91),make_material('oblique-mineral-fracture',c['palette']['fracture'],.97)]
 obj=mesh_object('preserved-coil-and-curved-shaft',vv,ff,mats,col)
 for i,p in enumerate(obj.data.polygons):p.material_index=mat_ids[i]
 obj['source_specimen']='Lituites lituus MB.C.30527';obj['claim_scope']='Incomplete fossil only. Preserved side silhouette observed; reverse/depth/relief inferred. No terminal aperture or central tunnel.';obj['construction']='One closed source-outline solid with constrained elliptical section facets and continuous rounded whorl envelope; no separate overlapping tube meshes or smooth-shading concealment';obj['scale_warning']='Photo-calibrated conditional geometry;284.167mm is not verified actual specimen total length.'
 meta={'revision':c['revision'],'generator':'source/build_lituites_v008.py','config_sha256':hashlib.sha256(args.config.read_bytes()).hexdigest(),'brief':'freeze/brief-v009.json','description':{'en':'Stylized incomplete external fossil Lituites lituus neotype MB.C.30527, late Darriwilian. Only preserved coil, curved shaft and oblique break. Reverse/depth inferred; photo-scale size conditional and not an exact replica. Terminal aperture absent.','zh':'晚达瑞威尔期 Lituites lituus MB.C.30527 不完整化石标本；仅保存卷部、弯曲展开段和斜断端，反面与厚度推定，图尺尺寸为条件估计，未补终末壳口。'},'claim_scope':'Incomplete specimen, no animal/full aperture. New build, not historical recovery.','sources':[{'id':'LIT2022-Fig33A','url':'https://doi.org/10.5852/ejt.2022.799.1681','location':'Fig33A, p48, Tables9/10'}],'scale_uncertainty':'±5% engineering sensitivity assumption only, not statistical error; source length definitions unresolved; actual total length UNKNOWN','inferences':c['depth_policy']}
 record=export_asset(c['asset_id'],{'en':'Lituites preserved fossil','zh':'Lituites 保存化石标本'},'cephalopods',col,metadata=meta,output_root=out,render=False,max_triangles=c['budgets']['max_triangles'],max_materials=c['budgets']['max_materials'],max_primitives=c['budgets']['max_primitives'])
 assert record['glb_bytes']<=c['budgets']['max_glb_bytes']
 (out/'build-receipt.json').open('x').write(json.dumps({'new_build':True,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(args.config.read_bytes()).hexdigest(),'outline_sha256':hashlib.sha256((R/c['outline_source']).read_bytes()).hexdigest(),'excluded_outside_cdt_faces':excluded_outside_cdt_faces,'polygon_area_mm2':polygon_area,'emitted_planar_area_mm2':triangle_area,'sampling':'elliptical angular lanes and continuous rounded whorl envelope; flat shading unchanged','boundary_support_stations':len(supports),'section_count':section_count,'constraint_edges':len(constraints),'whorl_curve_segments':len(whorl)-1,'input_planar_points':len(points),'cdt_points':len(verts2),'boundary_vertices':len(boundary),'split_internal_boundary_chords':len(split),'collection':'EXPORT','root':c['asset_id'],'mesh_objects':['preserved-coil-and-curved-shaft'],'artifact':record},indent=2)+'\n')
if __name__=='__main__':main()
