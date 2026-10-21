#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read original editable geometry; test actual profiles and locally curved cavity exposure.
No imported generator logic, labels-only approvals, edits, welding or new microscopic tolerances.
"""
import argparse,datetime,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source);before=src.read_bytes();bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);ct=json.loads(bpy.data.texts['BATCH108_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices];tris=[tuple(t.vertices) for t in o.data.loop_triangles];cs={c['tag']:c for c in ct['components']};off=Vector(ct['translation']);aid=o.name.split('-original')[0];errors=[];checks=[];extent=max(max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3));eps=extent*1e-8
cent=lambda ids:sum((vs[i] for i in ids),Vector())/len(ids)
def pts(tag):return [vs[i] for i in cs[tag]['vertices']]
def check(name,ok,observed):
 checks.append(dict(check=name,pass_result=bool(ok),observed=observed))
 if not ok:errors.append(name)
def tree_except(ids):return BVHTree.FromPolygons(vs,[t for t in tris if not all(i in ids for i in t)],all_triangles=True)
def tube_profile(c,sides):
 ids=c['vertices'];rings=[ids[i:i+sides] for i in range(0,len(ids),sides)];centers=[cent(r) for r in rings];rs=[sum((vs[k]-cc).length for k in rr)/len(rr) for rr,cc in zip(rings,centers)];articles=(len(rs)-1)//3;delta=[rs[3*j+1]-rs[3*j] for j in range(articles)];return dict(rings=len(rings),geometric_articles=articles,waist_to_next_shoulder_deltas_m=delta,all_actual_waists=all(x>0 for x in delta),ring_centers=[list(x) for x in centers],ring_mean_radii_m=rs)
# Cavity checks derive all directions from the actual rings and curved local host.
for c in cs.values():
 if c['kind'] not in ('spiracle','anispiracle','anal_opening'):continue
 ids=c['vertices'];rings=[ids[j:j+12] for j in range(0,48,12)];base,rim,inner,floor=[cent(r) for r in rings];normal=(rim-base).normalized();depth=(rim-floor).dot(normal);hostids=set(cs['theca']['vertices']);host=BVHTree.FromPolygons(vs,[t for t in tris if all(i in hostids for i in t)],all_triangles=True);q,nn,fi,dist=host.find_nearest(floor);relative=(floor-q).dot(nn);others=tree_except(set(ids));samples=[floor]+[(floor+vs[i])/2 for i in rings[3]];visible=[others.ray_cast(x+normal*eps,normal,extent*3)[0] is None for x in samples];check(c['tag']+'_real_local_depression',depth>0 and relative>0 and any(visible),{'local_rim_to_floor_depth_m':depth,'floor_signed_to_nearest_curved_host_m':relative,'floor_samples_outward_visible':sum(visible),'floor_sample_count':len(samples),'actual_axis':list(normal),'method':'Floor lies below its own physical rim, above actual nearest curved host; outward rays against every other component. Center/floor vertices derive from original mesh, not a flat global-Z assumption.'})
for c in cs.values():
 if c['kind'] not in ('brachiole','stem','aulacophore'):continue
 sides=6 if c['kind']=='brachiole' else 8 if c['kind']=='stem' else 12;r=tube_profile(c,sides);check(c['tag']+'_actual_article_waists',r['all_actual_waists'],r)
if aid=='isorophus':
 curves=[]
 for tag in [x for x in cs if x.startswith('ambulacrum_')]:
  ff=[x for x in ct['integrated_features'] if x['component']==tag];groups=[ff[i:i+4] for i in range(0,len(ff),4)];cc=[cent([v for f in g for v in f['vertices']])-off for g in groups];aa=[math.atan2(v.y,v.x) for v in cc];total=sum(math.atan2(math.sin(b-a),math.cos(b-a)) for a,b in zip(aa,aa[1:]));curves.append({'ray':tag,'actual_angular_sweep_radians':total,'actual_radial_start_end_m':[cc[0].xy.length,cc[-1].xy.length]})
 check('four_contrasolar_one_solar_actual_paths',sum(x['actual_angular_sweep_radians']>0 for x in curves)==4 and sum(x['actual_angular_sweep_radians']<0 for x in curves)==1,curves)
if aid=='eleutherocrinus':
 spans={tag:max(v.y for v in pts(tag))-min(v.y for v in pts(tag)) for tag in cs if tag.startswith('ambulacrum_')};short=min(spans,key=spans.get);check('four_long_one_short_D_actual_extent',short=='ambulacrum_0' and all(spans[k]>spans[short] for k in spans if k!=short),spans)
 shortZ=sum(v.z for v in pts(short))/len(pts(short));bodycenter=sum(v.z for v in pts('theca'))/len(pts('theca'));check('short_D_on_lower_surface',shortZ<bodycenter,{'short_mean_z':shortZ,'body_mean_z':bodycenter})
if aid=='nucleocrinus':
 pp=pts('theca');b=[max(v[k] for v in pp)-min(v[k] for v in pp) for k in range(3)];check('subglobular_not_elongate_theca',b[2]<max(b[:2]),{'actual_theca_xyz_m':b})
 ids=cs['theca']['vertices'];bottom=vs[ids[0]];top=vs[ids[-1]];lower=[vs[x] for x in ids[1:33]];upper=[vs[x] for x in ids[-33:-1]];check('actual_basal_concavity',bottom.z>min(v.z for v in lower),{'axial_bottom_z':bottom.z,'first_ring_min_z':min(v.z for v in lower)});check('actual_summit_concavity',top.z<max(v.z for v in upper),{'axial_summit_z':top.z,'last_ring_max_z':max(v.z for v in upper)})
 for j in range(5):
  pp=pts('oral_'+str(j));upper=pp[len(pp)//2:];rr=[(v-off).xy.length for v in upper];check('oral_'+str(j)+'_actual_arrow_outline',len(upper)==6 and rr[3]>rr[2] and rr[3]>rr[4] and rr[0]<rr[1] and rr[0]<rr[5],{'outline_vertex_count':len(upper),'actual_radial_outline_m':rr})
if aid=='placocystites':
 for tag in ['spine_-1','spine_1']:
  pp=pts(tag);rings=[pp[i:i+8] for i in range(0,len(pp),8)];rr=[]
  for ring in rings:
   cc=sum(ring,Vector())/8;rr.append(sum((v-cc).length for v in ring)/8)
  check(tag+'_unjointed_taper',all(a>b for a,b in zip(rr,rr[1:])),{'actual_section_radii_m':rr})
 c=cs['aulacophore'];ring=[vs[i] for i in c['vertices'][12:24]];cc=sum(ring,Vector())/12;rr=[(v-cc).length for v in ring];check('proximal_multirow_longitudinal_sculpture',max(rr)>min(rr),{'actual_cross_section_radii_m':rr,'note':'Fourfold longitudinal indentations in addition to transverse article waists; final detail pixels separately required.'})
 assert all(x in cs for x in ['ventral_V2','ventral_V3','ventral_V4','ventral_V17'])
assert src.read_bytes()==before
report=dict(schema_version=1,status='pass' if not errors else 'fail',asset_id=aid,source_sha256=hashlib.sha256(before).hexdigest(),created_at_executor_clock=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,errors=errors,source_modified=False,limitations='Maker geometry diagnostics, not independent acceptance. Actual contact/topology/global feature visibility reported separately. No pixel-readability conclusion from numbers alone; original artistic sizes are not additional scientific ranges.')
Path(a.output).open('x').write(json.dumps(report,indent=2)+'\n');print(aid,report['status'],errors)
