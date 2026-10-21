# SPDX-License-Identifier: MIT
import bpy,json,sys,math,hashlib,datetime
from pathlib import Path
from mathutils import Vector
src,out=sys.argv[sys.argv.index('--')+1:];bpy.ops.wm.open_mainfile(filepath=src);ct=json.loads(bpy.data.texts['BATCH101_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];v=[o.matrix_world@q.co for q in o.data.vertices];cs={q['tag']:q for q in ct['components']};ids=cs['thallus']['vertices'];N=len(ids)//2;outline=[v[i] for i in ids[:N]];paths={}
for tag,c in cs.items():
 if c['kind']!='costa':continue
 vs=[v[i] for i in c['vertices']];paths[tag]=[sum(vs[i:i+6],Vector())/6 for i in range(0,len(vs)-2,6)]
def width(b,e):
 d=(e-b).normalized();n=Vector((-d.y,d.x,0));mid=(b+e)/2;ss=[]
 for i,x in enumerate(outline):
  y=outline[(i+1)%N];u=x-mid;vv=y-x;den=vv.dot(d)
  if abs(den)<1e-12:continue
  t=-u.dot(d)/den
  if 0<=t<=1:ss.append((u+vv*t).dot(n))
 neg=[x for x in ss if x<=0];pos=[x for x in ss if x>=0];return min(pos)-max(neg) if neg and pos else None
cross=[]
for tag in ['costa_0','costa_1','costa_3','costa_4']:
 pts=paths[tag];w=width(pts[-2],pts[-1]);cross.append({'tag':tag,'section':'Midpoint of distal segment, perpendicular to actual reopened costa centerline. First/last body boundary vertices, not config width.','width_m':w,'range_m':[.0011,.0023],'status':'pass' if w is not None and .0011<=w<=.0023 else 'fail'})
angles=[math.degrees((paths['costa_1'][1]-paths['costa_1'][0]).angle(paths['costa_2'][1]-paths['costa_2'][0])),math.degrees((paths['costa_3'][1]-paths['costa_3'][0]).angle(paths['costa_4'][1]-paths['costa_4'][0]))];lengths={k:sum((b-a).length for a,b in zip(vs,vs[1:])) for k,vs in paths.items()};maxpath=max(lengths['costa_0']+lengths['costa_1'],lengths['costa_0']+lengths['costa_2']+max(lengths['costa_3'],lengths['costa_4']));errors=[x['tag'] for x in cross if x['status']=='fail']+(['angle'] if not all(31<=x<=70 for x in angles) else [])+(['path'] if maxpath>.018 else [])
r={'status':'pass' if not errors else 'fail','source_sha256':hashlib.sha256(Path(src).read_bytes()).hexdigest(),'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ribbon_sections':cross,'actual_branch_angles_deg':angles,'source_branch_angle_range_deg':[31,70],'actual_max_costa_path_m':maxpath,'source_max_length_m':.018,'scope':'Section widths are measured away from junctions/caps, not a false requirement that widened forks equal strap width.','errors':errors};Path(out).open('x').write(json.dumps(r,indent=2));print(json.dumps(r))
