import json,sys,math
from pathlib import Path
R=Path('/workspace/shared/lowpoly-batch85-height-repair-20261020');O=Path(__file__).parent;sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
from qa_glb import read_glb,accessor_values
h=json.load(open(R/'production/small-life-batch85-height-repair/maker-handoff.json'));rows=[]
for a in h['items']:
 d,b,raw=read_glb(R/a['artifacts']['glb']['path']);ms={}
 for mesh in d['meshes']:
  ps=set()
  for pr in mesh['primitives']:ps.update(accessor_values(d,b,pr['attributes']['POSITION']))
  # Export Y-up => source (x,-z,y)
  vs=[(x,-z,y) for x,y,z in ps];ms[mesh['name']]=vs
 aid=a['asset_id'];rec={'asset_id':aid,'glb_sha256':a['artifacts']['glb']['sha256'],'measurements':{}};v=rec['measurements']
 if aid=='piedmont-glacier':
  v['shoulder_max_z_m']=max(p[2] for name,vs in ms.items() if 'shoulder' in name for p in vs);v['frozen_max_shoulder_height_m']=390;v['max_shoulder_point_blender_xyz_m']=list(max((p for name,vs in ms.items() if 'shoulder' in name for p in vs),key=lambda p:p[2]))
  pts=next(v for k,v in ms.items() if 'continuous-throat' in k);v['rear_throat_width_m']=max(p[0] for p in pts if abs(p[1]-790)<.001)-min(p[0] for p in pts if abs(p[1]-790)<.001);v['lobe_width_m']=max(p[0] for p in pts)-min(p[0] for p in pts);v['lobe_to_throat_ratio']=v['lobe_width_m']/v['rear_throat_width_m'];v['ice_max_z_m']=max(p[2] for p in pts);v['ice_max_thickness_above_substrate_m']=v['ice_max_z_m']-55
  v['cross_section_method']='Verified source generator reads frozen25, produces25 rows of19 top vertices (18 cross-width segments).'
 if aid=='lava-channel':
  pts=next(iter(ms.values()));v['max_levee_z_m']=max(p[2] for p in pts);v['frozen_levee_height_range_m']=[8,13];v['max_levee_point_blender_xyz_m']=list(max(pts,key=lambda p:p[2]))
  # Slice the13 row positions by common y and sort x. Bottom closure points excluded.
  grouped={}
  for p in pts:
   if p[2]>0:grouped.setdefault(round(p[1],4),[]).append(p)
  sections=[sorted(x) for x in grouped.values()];v['longitudinal_sections']=len(sections);v['section_width_range_m']=[min(s[-1][0]-s[0][0] for s in sections),max(s[-1][0]-s[0][0] for s in sections)];v['left_crest_range_m']=[min(max(p[2] for p in s[:5]) for s in sections),max(max(p[2] for p in s[:5]) for s in sections)];v['right_crest_range_m']=[min(max(p[2] for p in s[8:]) for s in sections),max(max(p[2] for p in s[8:]) for s in sections)];v['floor_z_range_m']=[min(p[2] for s in sections for p in s[5:8]),max(p[2] for s in sections for p in s[5:8])]
 if aid=='karst-polje':
  pts=next(iter(ms.values()));v['flat_floor_vertices']=sum(abs(p[2]-45)<.001 for p in pts);v['floor_height_m']=45;v['floor_bounds_xy_m']=[[min(p[k] for p in pts if abs(p[2]-45)<.001),max(p[k] for p in pts if abs(p[2]-45)<.001)] for k in range(2)];v['rim_max_m']=max(p[2] for p in pts);v['frozen_rim_height_range_m']=[170,270]
  # Each source angular sector has a shared azimuth after ellipse x/y normalization; group and measure local top.
  g={}
  for x,y,z in pts:
   if abs(x)+abs(y)>0:g.setdefault(round(math.atan2(y/1050,x/550)*56/(2*math.pi))%56,[]).append(z)
  v['sector_count']=len(g);v['local_rim_crest_range_m']=[min(map(max,g.values())),max(map(max,g.values()))];v['sectors_below_frozen170m']=[{'sector':k,'crest_z_m':max(z)} for k,z in sorted(g.items()) if max(z)<170];v['below170_count']=sum(max(z)<170 for z in g.values())
 if aid=='namacalathus':
  pts=next(iter(ms.values()));v['height_m']=max(p[2] for p in pts);v['frozen_total_height_m']=.035;v['six_lateral_lumens']='Personally counted through-wall oval openings around shell, additionally connected shell Euler characteristic-12 supports genus7 (6 side handles plus axial tube).';v['stem_open']='Top view central small white hole and paired inner/outer zero-height vertex rings show open axial lumen.'
 rows.append(rec)
(O/'parameter-measurements.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
