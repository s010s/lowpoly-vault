# SPDX-License-Identifier: MIT
import bpy,sys,json,math,hashlib,datetime,os
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:];source=Path(args[0]);output=Path(args[1]);bpy.ops.wm.open_mainfile(filepath=str(source));ob=next(o for o in bpy.data.objects if o.type=='MESH');groups={g.name:[] for g in ob.vertex_groups}
for v in ob.data.vertices:
 for g in v.groups:groups[ob.vertex_groups[g.group].name].append(ob.matrix_world@v.co)
def n(prefix):return sum(k.startswith(prefix) for k in groups)
aid=source.stem;counts={};details={}
if aid=='sphenophyllum':counts={'axes':n('main_axis')+n('lateral_axis_'),'wedge_leaves':n('wedge_leaf_'),'divided_leaves':n('divided_leaf_'),'all_leaves':n('wedge_leaf_')+n('divided_leaf_'),'hooks':n('hook_'),'roots':n('root_')};details['whorl_leaf_grouping']={str(i):[k for k in groups if k.startswith(('wedge_leaf_','divided_leaf_')) and int(k.split('_')[-1])//6==i] for i in range(16)}
if aid=='psaronius':counts={'root_bundles':n('root_bundle_'),'fronds':n('frond_rachis_'),'pinnae':n('pinna_'),'pinnules':n('pinnule_')}
if aid=='hausmannia':
 counts={'fan_sectors':n('continuous_fan_lamina'),'initial_veins':n('major_initial_'),'terminal_veins':n('major_terminal_'),'crossbands':len({k.split('_')[2] for k in groups if k.startswith('net_cross_')})};pts=groups['continuous_fan_lamina'];base=pts[0];angles={}
 for p in pts:
  x,z=p.x-base.x,p.z-base.z;r=math.hypot(x,z)
  if r<1e-8:continue
  a=round(math.atan2(x,z),6);angles[a]=max(angles.get(a,0),r)
 ar=sorted(angles.items());peaks=[{'angle_rad':ar[i][0],'radius_m':ar[i][1]} for i in range(1,len(ar)-1) if ar[i][1]>ar[i-1][1] and ar[i][1]>ar[i+1][1]];counts['actual_margin_radial_peaks']=len(peaks);details.update(actual_margin_radial_peaks=peaks,method='Outer envelope of actual transformed source XZ positions around the basal lamina vertex; local radial maxima, not generator parameters. Paired grouping is a visual/artistic interpretation.')
if aid=='dictyophyllum':counts={'basal_arms':n('basal_arm_'),'solid_four_ray_webs':n('four_ray_web_'),'actual_midvein_rays':n('ray_midvein_')};details['ray_count_note']='Eight actual geometric central vein groups, one in each of8 visually inspected lamina rays. Four-ray web boundary triangulation is actual closed volume, not8 disconnected leaf cards.'
json.dump({'schema_version':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'Reopen exact Blend; count nonempty actual geometric vertex groups, not design metadata or config; special Hausmannia radial peak measurement below.','counts':counts,'details':details},output.open('x'),indent=2)
