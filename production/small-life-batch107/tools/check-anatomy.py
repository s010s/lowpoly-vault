#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only actual source geometry measurements; no scientific size bounds invented."""
import argparse,collections,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source);bpy.ops.wm.open_mainfile(filepath=str(src));ct=json.loads(bpy.data.texts['BATCH107_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];vs=[o.matrix_world@v.co for v in o.data.vertices];off=Vector(ct['translation']);local=[v-off for v in vs];o.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in o.data.loop_triangles];cs={c['tag']:c for c in ct['components']};features=ct['integrated_features'];checks=[];measure={}
def pts(t):return [local[i] for i in cs[t]['vertices']]
def center(t):q=pts(t);return sum(q,Vector())/len(q)
def bounds(t):q=pts(t);return [max(v[k] for v in q)-min(v[k] for v in q) for k in range(3)]
def tree(t):ids=set(cs[t]['vertices']);return BVHTree.FromPolygons(vs,[tr for tr in tris if all(i in ids for i in tr)],all_triangles=True)
def check(name,ok,evidence):checks.append(dict(name=name,pass_=bool(ok),evidence=evidence))
def plate_centers(t):return [sum((local[i] for i in f['vertices']),Vector())/len(f['vertices']) for f in features if f['component']==t]
for t in cs:measure[t]={'actual_aabb_dimensions_m':bounds(t),'actual_vertex_centroid_m':list(center(t))}
aid=src.stem
if aid=='dendrocystites':
 h=pts('homoiostele');b=pts('brachiole');nr=len(h)//16;nb=len(b)//8;hc=[sum(h[i*16:(i+1)*16],Vector())/16 for i in range(nr)];bc=[sum(b[i*8:(i+1)*8],Vector())/8 for i in range(nb)];hl=sum((x-y).length for x,y in zip(hc,hc[1:]));bl=sum((x-y).length for x,y in zip(bc,bc[1:]));rr=[(v-hc[1]).length for v in h[16:32]]
 check('one_short_brachiole_distinct_from_long_homoiostele',bl<hl,{'actual_brachiole_centerline_m':bl,'actual_homoiostele_centerline_m':hl,'actual_tube_ring_counts':[nb,nr]})
 check('four_real_longitudinal_seams_in_proximal_ring',all(rr[k]<rr[(k+2)%16] for k in [0,4,8,12]),{'actual_proximal_ring_radii_m':rr,'method':'Distances from actual16-vertex ring centroid; four cardinal notches are actual geometry.'})
 check('flattened_theca',bounds('theca')[2]<min(bounds('theca')[:2]),measure['theca'])
 check('single_suranal_actual_solid',len(plate_centers('suranal'))==1,{'actual_closed_plate_count':len(plate_centers('suranal'))})
elif aid=='trochocystites':
 for t in ['groove_left','groove_right']:
  hits=tree(t).overlap(tree('mouth'));check(t+'_physically_meets_mouth',len(hits)>0,{'actual_triangle_intersection_pairs':len(hits)})
 check('separate_right_anterolateral_mouth',center('mouth').x>center('operculum').x and center('mouth').y<0,{'mouth':list(center('mouth')),'operculum':list(center('operculum'))})
 check('short_posterior_stele',bounds('homostele')[1]<bounds('theca')[1] and center('homostele').y>0,measure['homostele'])
 check('genuine_marginal_plates',len(plate_centers('cinctus'))==16,{'actual_closed_plate_count':len(plate_centers('cinctus'))})
elif aid=='helicoplacus':
 slopes=[]
 for f in features:
  if f['component']!='helical_plating':continue
  q=[local[i] for i in f['vertices'][:len(f['vertices'])//2]]
  if len(q)!=4:continue
  for v,w in zip(q,q[1:]+q[:1]):
   d=math.atan2(w.y,w.x)-math.atan2(v.y,v.x)
   if d<-math.pi:d+=2*math.pi
   if d>math.pi:d-=2*math.pi
   # Exclude meridional edges and horizontal clipping boundaries; evaluate actual oblique edges.
   if abs(d)>.01 and abs(w.z-v.z)>1e-8:slopes.append((w.z-v.z)/d)
 check('actual_left_handed_helical_plate_edges',len(slopes)>0 and all(s<0 for s in slopes),{'measured_plate_edge_dz_per_radian_m_min':min(slopes),'max':max(slopes),'tested_edges':len(slopes),'method':'All actual oblique lower polygon edges; meridional edges and horizontal polar clipping boundaries excluded, not generator metadata.'})
 mouth=center('mouth');H=bounds('theca')[2];z=mouth.z/H;paths=[t for t in cs if cs[t]['kind']=='ambulacral_path'];check('three_surface_ambulacra_and_lateral_mouth',len(paths)==3 and 0<z<1 and math.hypot(mouth.x,mouth.y)>0,{'actual_paths':paths,'mouth_height_fraction':z,'mouth_radial_offset_m':math.hypot(mouth.x,mouth.y)})
 for t in paths:
  q=plate_centers(t);zs=[v.z for v in q];check(t+'_ends_before_poles',min(zs)>0 and max(zs)<H,{'actual_plate_z_range_m':[min(zs),max(zs)],'body_height_m':H,'actual_cover_plates':len(q)})
elif aid=='stromatocystites':
 paths=[t for t in cs if cs[t]['kind']=='ambulacral_path'];check('five_narrow_surface_bands',len(paths)==5,{'actual_paths':paths})
 body=bounds('theca');check('low_disc_not_star_arms',body[2]<min(body[:2]),{'actual_disc_dimensions_m':body})
 for t in paths:
  q=pts(t);maxr=max(math.hypot(v.x,v.y) for v in q);rbody=max(math.hypot(v.x,v.y) for v in pts('theca'));check(t+'_inside_continuous_disc_extent',maxr<rbody,{'actual_max_band_radius_m':maxr,'body_max_radius_m':rbody,'actual_cover_plate_count':len(plate_centers(t))})
 check('aboral_pad_below_oral_mouth',center('attachment_pad').z<center('mouth').z,{'pad':list(center('attachment_pad')),'mouth':list(center('mouth'))})
report=dict(schema_version=1,status='pass' if all(c['pass_'] for c in checks) else 'fail',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),asset_id=aid,read_only_original_mesh=True,measurements=measure,checks=checks,limitations='All dimensions and sampling counts are nominal artistic choices unless a frozen source-specific bound says otherwise. These tests establish geometric implementation, not independent scientific or visual acceptance. No mesh repair performed.');Path(a.output).open('x').write(json.dumps(report,indent=2)+'\n');print(json.dumps(report));sys.exit(0 if report['status']=='pass' else 1)
