# SPDX-License-Identifier: MIT
"""Original deterministic Acanthodes lopatini-inspired living reconstruction.
Blender -b -t 2 --factory-startup --python build_acanthodes.py -- --config config.json --output-dir PATH [--gray]
Construction coordinates are mm. Reference-led, not a traced/reused model.
"""
import bpy,bmesh,json,math,sys,argparse,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent))
import asset_common as ac
p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--gray',action='store_true')
A=p.parse_args(sys.argv[sys.argv.index('--')+1:]);C=json.loads(A.config.read_text());OUT=A.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
coll=ac.setup_scene(C['asset_id'],C['seed']);root=bpy.data.objects[coll['asset_root']];S=C['model_space_mm_to_m'];parts={};links=[];spines=[]
mats={k:ac.make_material('acanthodes-'+k,'#929292' if A.gray else col,double_sided=False) for k,col in C['palette'].items()}
def add(name,verts,faces,mat):
 o=ac.mesh_object(name,[[a*S for a in v] for v in verts],faces,[mats[x] for x in mat] if isinstance(mat,list) else mats[mat],coll)
 parts[name]=o;vg=o.vertex_groups.new(name=name);vg.add(list(range(len(o.data.vertices))),1,'REPLACE');return o

def link(a,b,kind):links.append({'child':a.name,'parent':b.name,'kind':kind})
def resample(points,steps=3):
 result=[]
 for i in range(len(points)-1):
  for j in range(steps):
   t=j/steps;result.append([a*(1-t)+b*t for a,b in zip(points[i],points[i+1])])
 result.append(points[-1]);return result

def tube(name,points,radii,mat,n=10,spine=False):
 ps=[Vector(x) for x in points];v=[]
 for i,pt in enumerate(ps):
  t=(ps[min(i+1,len(ps)-1)]-ps[max(i-1,0)]).normalized();axis=Vector((0,0,1)) if abs(t.z)<.9 else Vector((0,1,0));u=t.cross(axis).normalized();w=t.cross(u).normalized()
  for j in range(n):v.append(tuple(pt+radii[i]*(u*math.cos(j*2*math.pi/n)+w*math.sin(j*2*math.pi/n))))
 f=[tuple(reversed(range(n)))]
 for i in range(len(ps)-1):
  for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 f.append(tuple((len(ps)-1)*n+j for j in range(n)));o=add(name,v,f,mat)
 if spine:spines.append({'name':name,'centerline_mm':points,'length_mm':sum((b-a).length for a,b in zip(ps,ps[1:])),'root_radius_mm':radii[0],'tip_radius_mm':radii[-1]})
 return o

def solid_poly(name,poly,thick,axis,mat):
 # Every web is a finite solid with side walls, no alpha sheets/DoubleSide.
 n=len(poly);d=Vector(axis)*thick/2;v=[tuple(Vector(p)-d) for p in poly]+[tuple(Vector(p)+d) for p in poly]
 f=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,n+(j+1)%n,n+j) for j in range(n)]
 return add(name,v,f,mat)

pectoral_shells=[]
def triangulate_projected_pectoral(poly):
 # Canonical +X/Y projection is a simple polygon. Matching triangles on both
 # Z-offset surfaces make this a graph shell, not two unrelated warped n-gons.
 pts=[(abs(p[0]),p[1]) for p in poly]
 cross=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 area=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))/2
 ids=list(range(len(pts))) if area>0 else list(reversed(range(len(pts))))
 def within(p,a,b,c):return min(cross(a,b,p),cross(b,c,p),cross(c,a,p))>=-1e-10
 tris=[]
 while len(ids)>3:
  for j,b in enumerate(ids):
   a,c=ids[j-1],ids[(j+1)%len(ids)]
   if cross(pts[a],pts[b],pts[c])<=1e-9:continue
   if any(within(pts[q],pts[a],pts[b],pts[c]) for q in ids if q not in [a,b,c]):continue
   tris.append((a,b,c));ids.pop(j);break
  else:raise RuntimeError('Pectoral projected polygon cannot be simply triangulated')
 tris.append(tuple(ids))
 assert len(tris)==len(poly)-2
 assert abs(sum(abs(cross(pts[a],pts[b],pts[c]))/2 for a,b,c in tris)-abs(area))<1e-8
 return tris,abs(area)

def solid_pectoral(name,poly,thick,mat):
 n=len(poly);tris,area=triangulate_projected_pectoral(poly)
 d=Vector((0,0,1))*thick/2
 v=[tuple(Vector(p)-d) for p in poly]+[tuple(Vector(p)+d) for p in poly]
 f=[tuple(reversed(t)) for t in tris]+[tuple(n+i for i in t) for t in tris]
 for j in range(n):
  k=(j+1)%n;f.extend([(j,k,n+k),(j,n+k,n+j)])
 o=add(name,v,f,mat)
 pectoral_shells.append({'mesh':name,'perimeter_vertices':n,'matched_cap_triangle_indices':tris,'projected_area_mm2':area,'constant_z_thickness_mm':thick,'source_faces_all_explicit_triangles':all(len(x)==3 for x in f),'cap_projection':'abs(X), Y canonical mirrored projection','no_ngon_caps':True})
 return o

def eye(name,s):
 n=16;rings=8;cx=s*3.12;cy=-44.0;cz=12.0;rx=.82;ry=2.0;rz=1.9
 v=[(cx,cy,cz+rz)]
 for k in range(1,rings):
  t=math.pi*k/rings
  for j in range(n):
   a=j*2*math.pi/n;v.append((cx+rx*math.sin(t)*math.cos(a),cy+ry*math.sin(t)*math.sin(a),cz+rz*math.cos(t)))
 v.append((cx,cy,cz-rz));f=[]
 for j in range(n):f.append((0,1+j,1+(j+1)%n))
 for k in range(rings-2):
  for j in range(n):f.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
 for j in range(n):f.append((len(v)-1,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
 return add(name,v,f,'eye')
# Species proportions: 100mm nose-to-axial-tip, head/gill region about20mm,
# max trunk depth16.7mm and selected width12mm. Narrow tail axial continuation.
sections=[[-50,.22,8.5,10.4],[-49,1.25,6.8,12.6],[-47,2.7,4.6,15.2],[-44,3.9,2.9,17.0],[-40,5.1,1.9,18.0],[-34,5.8,1.3,18.0],[-28,6.0,1.4,18.1],[-20,5.8,1.7,18.0],[-12,5.25,2.3,17.7],[-4,4.5,3.2,17.2],[4,3.6,4.5,16.5],[12,2.7,6.1,15.8],[20,1.8,7.7,15.1],[27,1.05,8.9,15.0],[32,.65,10.2,15.6],[37,.38,12.7,16.9],[42,.27,15.3,18.4],[47,.17,18.0,19.8],[50,.09,19.4,20.0]]
rings=resample(sections,C['body_subdivisions']);n=C['body_ring_sides'];v=[]
for y,w,lo,hi in rings:
 for j in range(n):
  a=j*2*math.pi/n;v.append((w*math.sin(a),y,(hi+lo)/2+(hi-lo)/2*math.cos(a)))
f=[tuple(reversed(range(n)))]
for k in range(len(rings)-1):
 for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
f.append(tuple((len(rings)-1)*n+j for j in range(n)))
body=add('01-continuous-fusiform-body-and-axial-tail',v,f,['dorsal','flank','ventral'])
for k,face in enumerate(body.data.polygons):
 if k==0 or k==len(body.data.polygons)-1:face.material_index=1
 else:
  a=((k-1)%n+.5)*2*math.pi/n;c=math.cos(a);face.material_index=0 if c>.52 else 2 if c<-.62 else 1
# Tail membrane wraps the axial continuation; asymmetric lower lobe is larger.
tailpoly=[(0,26.5,14.0),(0,30,15.1),(0,34.5,16.7),(0,39,18.5),(0,44,19.7),(0,48.5,20.2),(0,50,20.0),(0,49.4,19.5),(0,47.8,18.8),(0,44,16.5),(0,41.6,14.2),(0,40.5,12.4),(0,40.6,9.0),(0,41.0,6.5),(0,40.0,6.2),(0,37.1,8.0),(0,33.3,9.9),(0,29.5,10.5),(0,26.5,10.3)]
tail=solid_poly('02-asymmetric-caudal-web-small-distal-axial-lobe',tailpoly,.48,(1,0,0),'web');link(tail,body,'continuous overlap around tapered axial caudal continuation')
# Only paired fin-spine set: two sabre-curved pectorals.
for s,side in [(-1,'L'),(1,'R')]:
 points=[(s*4,-30,4.7),(s*4.7,-29,3.5),(s*5.5,-27.6,2.2),(s*6.5,-25.6,.9),(s*7.5,-23.4,.0),(s*8.5,-20,-.4)]
 ps=resample(points,2);r=[.46*(1-i/(len(ps)-1))+.10*i/(len(ps)-1) for i in range(len(ps))]
 spine=tube(f'03-{side}-pectoral-spine',ps,r,'spine',10,True);link(spine,body,'pectoral spine base embedded in ventrolateral gill-region skin')
 poly=[(s*4,-30,4.7),(s*4.8,-28.6,3.1),(s*5.5,-27.6,2.2),(s*6.5,-25.6,.9),(s*7.5,-23.4,.0),(s*8.5,-20,-.4),(s*7.3,-22.0,.8),(s*6.2,-22.4,2.1),(s*5.0,-22.7,3.6),(s*3.6,-24.0,5.2),(s*3.6,-28,5.2)]
 web=solid_pectoral(f'04-{side}-understated-pectoral-web',poly,.34,'web');link(web,body,'pectoral web soft root embedded in flank');link(web,spine,'web follows curved posterior surface of pectoral spine')
 e=eye(f'05-{side}-embedded-anterior-eye',s);link(e,body,'flattened eye solid broadly embeds anterior head; no stalk or bead')
# Single median ventral spine and long shallow web, never a pelvic pair.
spine_defs=[('ventral',[(-6,3.5),(-5.1,1.8),(-3.1,-.3)],.30,.08),('anal',[(11.5,6.5),(13.4,4.1),(15.7,1.2),(18.6,-1.0)],.43,.10),('dorsal',[(13.0,15.3),(15.2,17.3),(17.7,19.7),(20.9,22.1)],.43,.10)]
spine_objects={}
for name,ys,rad,tip in spine_defs:
 ps=resample([(0,y,z) for y,z in ys],3);r=[rad*(1-i/(len(ps)-1))+tip*i/(len(ps)-1) for i in range(len(ps))]
 o=tube('06-single-midline-'+name+'-spine',ps,r,'spine',10,True);spine_objects[name]=o;link(o,body,'unpaired '+name+' spine with deeply embedded base')
web_defs={'ventral':[(-6.3,3.8),(-5.1,1.8),(-3.1,-.3),(-1.4,.8),(1.3,1.8),(4.8,3.2),(8,4.6),(11.5,5.9),(12,6.8),(4,5.3),(-3,4.3)],'anal':[(11.2,6.8),(13.4,4.1),(15.7,1.2),(18.6,-1.0),(18.0,.8),(18.6,2.7),(20.4,4.8),(23.5,6.4),(26,7.5),(23,8.4),(16,8.0)],'dorsal':[(12.6,15.0),(15.2,17.3),(17.7,19.7),(20.9,22.1),(19.8,19.5),(20.0,17.9),(21.1,16.6),(23.4,15.4),(26,14.8),(24,14.2),(17,14.6)]}
for name,poly in web_defs.items():
 o=solid_poly('07-single-midline-'+name+'-web',[(0,y,z) for y,z in poly],.44 if name!='ventral' else .38,(1,0,0),'web');link(o,body,'unpaired '+name+' soft fin root intersects body');link(o,spine_objects[name],name+' web contacts leading spine')
# Tiny closed mouth seam: a flattened attached solid, not an open hole or teeth.
mouth=tube('08-compact-closed-mouth-line',[(-.9,-49.25,8.6),(0,-49.8,8.4),(.9,-49.25,8.6)],[.12,.12,.12],'eye',6);link(mouth,body,'small closed mouth seam embedded across blunt snout')
# Full source geometry intersections/parity containment, not AABB assertions.
bpy.context.view_layer.update()
cache={name:BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],all_triangles=False,epsilon=0) for name,o in parts.items()}
def inside(pt,tree):
 d=Vector((1,.137,.219)).normalized();pos=pt.copy();count=0
 for _ in range(60):
  hit,n,idx,dist=tree.ray_cast(pos,d,1)
  if hit is None:break
  count+=1;pos=hit+d*1e-9
 return count%2==1
for q in links:
 a,b=q['child'],q['parent'];count=len(cache[a].overlap(cache[b]));contained=any(inside(parts[a].matrix_world@v.co,cache[b]) for v in parts[a].data.vertices)
 q.update(boundary_intersection_pairs=count,child_vertex_inside_parent=contained,status='PASS' if count or contained else 'FAIL')
failed=[q for q in links if q['status']!='PASS'];assert len(spines)==5
lengths={q['name']:q['length_mm'] for q in spines};pectoral=lengths['03-L-pectoral-spine'];ratios={k:lengths['06-single-midline-'+k+'-spine']/pectoral for k in ['ventral','anal','dorsal']}
assert .2<=ratios['ventral']<=.45 and all(.65<=ratios[k]<=.85 for k in ['anal','dorsal']),ratios
report={'method':'BVH actual triangle surface intersection or ray-parity contained child vertex, zero BVH epsilon','count':len(links),'failed':failed,'checks':links,'spine_count':len(spines),'spines':spines,'spine_length_ratios_to_pectoral':ratios,'paired_spine_sets':['pectoral'],'unpaired_spines':['ventral','anal','dorsal'],'median_spine_base_y_mm':{'ventral':-6,'anal':11.5,'dorsal':13},'anal_to_dorsal_origin_offset_mm':1.5,'small_distal_axial_lobe':True,'body_source_sections_mm':sections,'fin_thickness_mm':{'pectoral':.34,'ventral':.38,'anal':.44,'dorsal':.44,'caudal':.48},'body_nominal_length_mm':100,'reconstruction_limits':C['reconstruction_notes'],'nonadjacent_self_intersections':'Not exhaustive; intentional skin/fin/spine intersections recorded, no boolean fusion claimed.'}
(OUT/'anatomical-connections.json').write_text(json.dumps(report,indent=2))
(OUT/'pectoral-shell-topology.json').write_text(json.dumps({'repair':'ACAN-01','method':'Explicit matched cap triangulation over simple XY projection; constant0.34mmZ extrusion with explicit closed side triangles. Closed-positive-volume alone is NOT self-intersection clearance.','shells':pectoral_shells},indent=2))
if failed:raise RuntimeError('Anatomical attachment failed: '+repr(failed))
# Identity root unchanged. Unsupported-swim display datum at lowest surface Z0.
offset=ac.ground_asset(coll,center_xy=True)
for o in coll.all_objects:
 if o.type=='MESH':
  bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
root['scientific_limits']=C['reconstruction_notes'];root['representation']='living-reconstruction';root['spine_count']=5;root['only_paired_spines']='pectoral';root['source']='Beznosov2009 Acanthodes lopatini Fig2/3/4/7'
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
record=ac.export_asset(C['asset_id'],{'en':'Acanthodes lopatini','zh':'棘鱼 Acanthodes lopatini'},'fish',coll,metadata={'representation':'living-reconstruction','revision':C['revision'],'description':{'en':'Original100mm Acanthodes lopatini-inspired living fish: five spines, one median shallow ventral fin and small asymmetric caudal axial lobe.','zh':'原创100毫米活体复原：五根鳍棘、单个中线浅腹鳍及不对称尾部的小轴叶。'},'reconstruction_notes':C['reconstruction_notes'],'origin_note':'Lowest exported surfaceZ0 and XYbounds center display datum; unsupported neutral swim, not habitat/ground assertion.','generator':'scripts/build_acanthodes.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'total_length_m':.1},output_root=OUT,render=False,diagnostics=False,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'anatomical_components':len(parts),'anatomical_links':len(links),'spine_count':len(spines),'datum_offset_m':offset,'glb_sha256':record['sha256']['glb']},indent=2))
print('BUILD_COMPLETE',record['sha256']['glb'])
