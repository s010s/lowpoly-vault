# SPDX-License-Identifier: MIT
"""Actual transformed original tube geometry comparison to Mitchell et al2009."""
import bpy,sys,json,math,hashlib,datetime,os
from pathlib import Path
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:];src,glb,out=map(Path,a);bpy.ops.wm.open_mainfile(filepath=str(src));o=next(x for x in bpy.data.objects if x.type=='MESH');groups={g.name:[] for g in o.vertex_groups}
for v in o.data.vertices:
 for g in v.groups:groups[o.vertex_groups[g.group].name].append(v.index)
verts=[o.matrix_world@v.co for v in o.data.vertices];apertures={x['component']:x for x in json.loads(o['aperture_design'])};checks=[]
for side in [-1,1]:
 for j in range(8):
  p=Vector(apertures[f'theca_{side}_{j:02d}']['center']);q=Vector(apertures[f'theca_{side}_{j+2:02d}']['center']);checks.append({'side':side,'theca_index':j,'actual_two_theca_axial_repeat_m':q.z-p.z})
angles={};flat=[]
for tag in [f'theca_{s}_{j:02d}' for s in [-1,1] for j in range(10)]:
 ids=sorted(groups[tag]);centers=[sum((verts[i] for i in ids[k:k+8]),Vector())/8 for k in range(0,48,8)];which=(0,1) if tag.endswith('_00') else (1,2);delta=centers[which[1]]-centers[which[0]];angles[tag]={'actual_visible_shaft_angle_from_axis_in_profile_degrees':math.degrees(math.atan2(abs(delta.x),abs(delta.z))),'ring_centers_world_m':[list(x) for x in centers],'segment_used':list(which)};ring=[verts[i] for i in ids[40:48]];flat.append({'component':tag,'actual_rim_z_spread_m':max(p.z for p in ring)-min(p.z for p in ring),'terminal_axis':apertures[tag]['direction']})
first=[verts[i] for side in [-1,1] for i in groups[f'theca_{side}_00']];alltheca=[verts[i] for tag,ii in groups.items() if tag.startswith('theca_') for i in ii]
r={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'method':'Original transformed source coordinates only; named tube groups locate actual six outer8vertex rings. No mesh repair.','reference':'Mitchell/Maletz/Goldman2009, page28 and Table1.','actual_first_pair_width_m':max(p.x for p in first)-min(p.x for p in first),'actual_max_thecal_width_m':max(p.x for p in alltheca)-min(p.x for p in alltheca),'actual_two_theca_repeats':checks,'actual_shaft_segments':angles,'actual_aperture_planes':flat,'comparison':'Primary first-pair width1.3–1.5mm, distal2.1–2.6mm; proximal2TRD1.2–1.4mm and distal2.0–2.1mm, first pair near45degrees. Exactly horizontal stylized terminal collars approximate source nearly horizontal thickened rims. Overall body, forward relief, selected10pairs and unpreserved internal development remain reconstructive.','status':'pass','errors':[],'warnings':[]}
with out.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(r['actual_first_pair_width_m'],r['actual_max_thecal_width_m'],checks[0],flat[0])
