# SPDX-License-Identifier: MIT
"""Measured anatomy assembly checks on the reopened editable source. Not independent factual QA."""
import sys,json,hashlib,math
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));import generate as g
out=Path(sys.argv[sys.argv.index('--')+1]);root=out.parents[2];g.P=json.loads((HERE/'params.json').read_text());g.initialize_curve()
tech=json.loads((root/'technical.json').read_text());ground=tech['ground_offset_m'];col=bpy.data.collections['EXPORT'];meshes=[o for o in col.all_objects if o.type=='MESH']
limbs=sorted([o for o in meshes if o.name.startswith('lobopod-pair')],key=lambda o:o.name);assert len(limbs)==10

def components(obj):
 adj=[[] for _ in obj.data.vertices]
 for e in obj.data.edges:a,b=e.vertices;adj[a].append(b);adj[b].append(a)
 unseen=set(range(len(adj)));sizes=[]
 while unseen:
  todo=[unseen.pop()];size=0
  while todo:
   a=todo.pop();size+=1
   for b in adj[a]:
    if b in unseen:unseen.remove(b);todo.append(b)
  sizes.append(size)
 return sorted(sizes,reverse=True)
rows=[]
for o in limbs:
 pts=[v.co*1000+Vector((0,0,ground*1000)) for v in o.data.vertices]
 shaft_centers=[sum(pts[i*8:(i+1)*8],Vector())/8 for i in range(15)]
 s=o['body_centerline_attachment_mm'];x,d,t=g.frame(s);root_center=shaft_centers[0];delta=root_center-g.center(s)
 normalized_root_radius=math.sqrt((delta.dot(x)/g.radius(s))**2+(delta.dot(d)/(g.radius(s)*.94))**2)
 assert normalized_root_radius<1
 assert components(o)==[121]+[11]*14
 measured=sum((b-a).length for a,b in zip(shaft_centers,shaft_centers[1:]))
 assert abs(measured-4.5)<1e-4
 setaroots=[]
 for k in range(14):
  b=121+k*11;c=sum(pts[b:b+5],Vector())/5;u=.17+(k%7)*.108;q=u*14;i=min(13,int(q));axis=shaft_centers[i].lerp(shaft_centers[i+1],q-i)
  rad=.34*(1-u)**.80+.032;dist=(c-axis).length
  assert dist<rad
  setaroots.append({'index':k,'row':1 if k<7 else 2,'distance_to_shaft_axis_mm':dist,'shaft_radius_mm':rad,'root_center_inside_shaft':True})
 rows.append({'part':o.name,'anterior_pair':o['anterior_pair'],'side':o['side'],'shaft_length_mm':measured,'body_attachment_centerline_mm':s,'attachment_root_elliptical_radius_fraction':normalized_root_radius,'root_center_inside_body':True,'connected_component_vertex_counts':components(o),'two_ventral_rows':setaroots})
assert sorted(o['anterior_pair'] for o in limbs)==[1,1,2,2,3,3,4,4,5,5]
body=bpy.data.objects['continuous-annulated-body-head-and-posterior'];assert len(components(body))==1
hooks=[o for o in meshes if o.name.startswith('posterior-hook-ring')];eyes=[o for o in meshes if o.name.startswith('simple-ocular-spot')]
assert len(hooks)==2 and all(len(components(o))==10 for o in hooks);assert len(eyes)==2
assert not [o for o in meshes if any(k in o.name for k in ['tube','antenna','stand','seabed','stage'])]
record={'status':'PASS_SCOPED_GEOMETRY','blend_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'glb_sha256':tech['glb']['sha256'],'method':'Reopened source measured shaft ring centers and connected components; verified root centers inside relevant soft-tissue profiles. Does not prove Boolean union or all surface intersections.','body_centerline_length_m':tech['body_centerline_length_m'],'head_centerline_length_m':.0018,'limb_pairs':5,'limb_count':10,'limb_measurements':rows,'long_limb_free_region_mm':[4.6,39.6],'body_connected_components':len(components(body)),'posterior_hook_ring_count':2,'posterior_hook_components_per_ring':[len(components(o)) for o in hooks],'ocular_spot_count':2,'tube_included':False,'posterior_limbs':0,'head_antennae':0,'scope':'Maker technical anatomy correspondence only; independent visual/factual/specification review is PENDING.'}
out.write_text(json.dumps(record,indent=2)+'\n')
