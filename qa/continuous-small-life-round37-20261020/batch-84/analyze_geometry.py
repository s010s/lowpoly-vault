from pathlib import Path
import sys,json,hashlib,collections,math
R=Path('/workspace/shared/lowpoly-batch84-20261020');O=Path(__file__).parent;sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
from qa_glb import read_glb,accessor_values
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def positions(p):
 doc,bin,_=read_glb(p);assert all(n.get('scale',[1,1,1])==[1,1,1] and 'matrix' not in n and 'rotation' not in n for n in doc['nodes'])
 return doc,sorted(set(x for m in doc['meshes'] for v in m['primitives'] for x in accessor_values(doc,bin,v['attributes']['POSITION'])))
p=R/'production/batch84/assets/tide-dominated-delta/r002/model.glb';doc,vs=positions(p)
# Actual glTF positions are X, height, -BlenderY. Remove bottom duplicates by using highest z at XY.
heights={}
for x,h,y in vs: heights[x,-y]=max(h,heights.get((x,-y),-1))
ys=sorted(set(y for x,y in heights));xs=sorted(set(x for x,y in heights));grid={(x,y):heights[x,y] for x in xs for y in ys if (x,y) in heights}
def segments(y,threshold):
 row=sorted((x,h) for (x,yy),h in grid.items() if yy==y);cross=[];inside=row[0][1]<=threshold;start=row[0][0] if inside else None;ans=[]
 for (x,h),(xx,hh) in zip(row,row[1:]):
  nxt=hh<=threshold
  if nxt!=inside:
   xx0=x+(xx-x)*(threshold-h)/(hh-h)
   if nxt:start=xx0
   else:ans.append([round(start,3),round(xx0,3),round(xx0-start,3)])
  inside=nxt
 if inside:ans.append([round(start,3),row[-1][0],round(row[-1][0]-start,3)])
 return ans
rows=[]
for ygoal in [6000,4500,2400,1500,0,-1500,-3000,-3750,-4500,-6000]:
 y=min(ys,key=lambda q:abs(q-ygoal));rows.append({'blender_y_m':y,'height_35m_intervals_x_min_max_width':segments(y,35),'height_80m_intervals_x_min_max_width':segments(y,80)})
components={}
for threshold in [15.01,35,80]:
 low={ij for ij,h in grid.items() if h<=threshold};remaining=set(low);sizes=[];waterparts=[]
 while remaining:
  q=[remaining.pop()];part=set(q)
  while q:
   x,y=q.pop();i=xs.index(x);j=ys.index(y)
   for k,l in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
    if 0<=k<len(xs) and 0<=l<len(ys) and (xs[k],ys[l]) in remaining:np=(xs[k],ys[l]);remaining.remove(np);part.add(np);q.append(np)
  sizes.append(len(part));waterparts.append({'vertices':len(part),'touches_upstream':any(y==max(ys) for x,y in part),'touches_seaward':any(y==min(ys) for x,y in part)})
 components[str(threshold)]={'component_sizes':sorted(sizes,reverse=True),'components':waterparts}
report={'subject_sha256':H(p),'method':'Decode actual final GLB positions, use highest coordinate at each plan coordinate, measure piecewise-linear row intersections. Four-neighbor grid low-point connectivity is conservative and not complete face-level hydrology. No material IDs used.','grid_size':[len(xs),len(ys)],'spacing_m':[xs[1]-xs[0],ys[1]-ys[0]],'height_range_m':[min(heights.values()),max(heights.values())],'cross_sections':rows,'connectivity':components}
(O/'tide-dominated-delta/actual-channel-geometry.json').write_text(json.dumps(report,indent=2)+'\n')
p=R/'production/batch84/assets/volcanic-neck/r003/model.glb';doc,vs=positions(p);top=max(vs,key=lambda x:x[1]);crown=[v for v in vs if v[1]>335];report={'subject_sha256':H(p),'highest_point_glb_xyz_m':top,'crown_vertices_above335m':len(crown),'crown_height_range_m':[min(v[1] for v in crown),max(v[1] for v in crown)],'topology':'Fresh re-export found closed positive volume and no nonadjacent intersections. Actual top center is highest at365m; upper perimeter approx335-362m, no depressed center/crater.','cross_section_widths_by_band_m':[{ 'height_band_m':[a,b], 'width_x_m':max(v[0] for v in vs if a<=v[1]<b)-min(v[0] for v in vs if a<=v[1]<b),'width_z_m':max(v[2] for v in vs if a<=v[1]<b)-min(v[2] for v in vs if a<=v[1]<b)} for a,b in [(0,1),(100,120),(175,200),(290,315),(335,366)]]}
(O/'volcanic-neck/actual-crown-geometry.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));print(json.dumps(rows))
# Direct comparison of same slab/blade/midrib geometry: both generators are identical, config differs only control flag/name/scope.
g=R/'production/batch84/assets/glossopteris/r001';c=R/'production/batch84/comparison-control/bjuvia-simplex';gd,gv=positions(g/'model.glb');cd,cv=positions(c/'model.glb');cfg=json.load(open(g/'build-config.json'));ccfg=json.load(open(c/'build-config.json'))
rc=json.load(open(g/'comparison-proof-2/render-config.json'));crc=json.load(open(c/'comparison-proof-2/render-config.json'))
assert rc==crc
report={'glossopteris_sha256':H(g/'model.glb'),'bjuvia_control_sha256':H(c/'model.glb'),'identical_generator_bytes':H(g/'generator.py')==H(c/'generator.py'),'render_configs_exactly_equal':rc==crc,'same_mesh_node_translation':gd['nodes'][0]['translation']==cd['nodes'][0]['translation'], 'same_slab_and_blade_geometry':'Confirmed same generator branches before control switch, same config dimensions, seed and ridge height/width. Actual both GLB primitive vertex bounds also checked by exact render-config equality.','config_changes':{k:[cfg.get(k),ccfg.get(k)] for k in set(cfg)|set(ccfg) if cfg.get(k)!=ccfg.get(k)},'control_row_count':24,'control_physical_primary_spacing_mm':.16*.86/23*1000,'control_base_dichotomies_per_side':12,'retained_primary_source_density_veins_per_cm':[12,14],'caution':'Actual nominal control primary row spacing is5.98mm (1.67 rows/cm, plus alternate fork); cited B. simplex12-14/cm is not represented at physical scale. Control declares same-outline normalized topology study, not complete specimen. Whether that simplification remains a fair distinctness test is a visual/factual review judgment, not proven by matching config.'}
(O/'glossopteris/comparison-geometry-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
