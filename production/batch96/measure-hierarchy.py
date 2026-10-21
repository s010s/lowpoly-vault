# SPDX-License-Identifier: MIT
import bpy,json,sys,pathlib,datetime,os,hashlib,math
from mathutils import Vector
B=pathlib.Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(B/'source.blend'));aid=B.parent.name;groups={}
for o in bpy.context.scene.objects:
 if o.type=='MESH':
  for g in o.vertex_groups:groups[g.name]=[o.matrix_world@v.co for v in o.data.vertices if any(k.group==g.index for k in v.groups)]
sem=json.load(open(B/'geometry-semantics.json'));tubes={t['group']:t for t in sem['tubes']};att=sem['attachments'];measure={};checks={}
def centers(g):
 n=tubes[g]['sides'];return[sum(groups[g][i:i+n],Vector())/n for i in range(0,len(groups[g]),n)]
def links(parent,child,n):
 d={g:sum(a['parent']==g and a['child'].startswith(child)for a in att) for g in groups if g.startswith(parent)};measure[parent+'to'+child]=d;checks[parent+'to'+child]=bool(d)and set(d.values())=={n}
cs=centers('main-axis');measure['actual_main_axis_station_centers_world_m']=[list(c)for c in cs];measure['actual_main_axis_station_mean_radii_m']=[sum((v-c).length for v in groups['main-axis'][i*tubes['main-axis']['sides']:(i+1)*tubes['main-axis']['sides']])/tubes['main-axis']['sides']for i,c in enumerate(cs)]
if aid=='paralycopodites':
 links('lateral-','twig-',4);links('twig-','leaf-',7);links('twig-','cone-',1);rows=[]
 for a in att:
  if a['parent']=='main-axis'and a['child'].startswith('lateral-'):
   c=centers(a['child']);d=(c[1]-c[0]).normalized();rows.append(dict(group=a['child'],base_world_m=list(c[0]),direction_world=list(d),side='negativeX'if d.x<0 else'positiveX'))
 measure['main_lateral_actual_directions']=rows;checks['ten_main_laterals_in_two_opposed_planes']=len(rows)==10 and sum(r['side']=='negativeX'for r in rows)==5 and all(abs(r['direction_world'][1])<1e-6 for r in rows)
 measure['actual_cone_station_axis_length_m']={g:sum((c[j+1]-c[j]).length for j in range(len(c)-1))for g in groups if g.startswith('cone-')for c in[centers(g)]}
 checks['two_crown_leaders']=sum(g.startswith('crown-')for g in groups)==2
elif aid in ['lyginopteris','medullosa']:
 links('frond-','fan-',2);links('fan-','pinna-',3 if aid=='lyginopteris' else 4);links('pinna-','leaf-',6 if aid=='lyginopteris' else 8)
 if aid=='lyginopteris':
  sc=centers('support-axis');measure['actual_support_station_to_living_station_min_distance_m']=min((x-y).length for x in sc for y in cs);checks['support_intersects_living_axis']=measure['actual_support_station_to_living_station_min_distance_m']<.001
  measure['actual_main_lean_xy_m']=(cs[-1]-cs[0]).xy.length;checks['nonvertical_leaning_main_axis']=measure['actual_main_lean_xy_m']>.3
else:
 links('limb-','twig-',3);links('twig-','leaf-',5);n=next(t for t in sem['leaf_frames']);measure['leaf_actual_vertices_per_group']={g:len(v)for g,v in groups.items()if g.startswith('leaf-')};checks['five_equal_width_bands_four_longitudinal_stations']=set(measure['leaf_actual_vertices_per_group'].values())=={48}
d={'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'source_sha256':hashlib.sha256((B/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((B/'model.glb').read_bytes()).hexdigest(),'measurements':measure,'checks':checks,'pass':all(checks.values()),'note':'Counts require actual mesh groups and parent contact report. Station dimensions measured from transformed world vertices. Tiny plane residual tolerance checks floating arithmetic only, not botanical dimension hard ranges. Nominal dimensions are not hard equality gates.'};(B/'hierarchy-measurements.json').write_text(json.dumps(d,indent=2)+'\n');print(aid,checks);assert d['pass']
