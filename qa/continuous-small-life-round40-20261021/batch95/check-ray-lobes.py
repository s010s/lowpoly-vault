import bpy,sys,pathlib,json,hashlib,math,datetime,os
from mathutils import Vector
S=pathlib.Path('/workspace/shared/lowpoly-batch95-20261020/production/small-life-batch95/dictyophyllum/r002/artifacts/dictyophyllum.blend');O=pathlib.Path('/workspace/shared/lowpoly-batch95-independent-qa-20261021/dictyophyllum/ray-lobes-supplement.json');bpy.ops.wm.open_mainfile(filepath=str(S),load_ui=False,use_scripts=False);ob=next(o for o in bpy.context.scene.objects if o.type=='MESH');groups={g.name:[]for g in ob.vertex_groups}
for v in ob.data.vertices:
 for g in v.groups:groups[ob.vertex_groups[g.group].name].append(ob.matrix_world@v.co)
rows=[]
for sign in [-1,1]:
 v=groups['four_ray_web_'+str(sign)];n=len(v)//2
 for r in range(4):
  outline=v[1+r*29:1+(r+1)*29];sides=[outline[:15],[outline[14]]+outline[15:]]
  for sid,points in enumerate(sides):
   convex=[];cross=[]
   for i in range(1,len(points)-1):
    a,b,c=points[i-1:i+2];cr=(b.x-a.x)*(c.z-b.z)-(b.z-a.z)*(c.x-b.x);cross.append(cr)
    if cr*sign<0:convex.append(i)
   rows.append({'arm':sign,'ray':r,'side':sid,'boundary_samples':len(points),'convex_lobe_vertex_indices':convex,'convex_lobe_count':len(convex),'signed_turns_xz':cross})
r={'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'tests':rows,'method':'Actual ordered volume boundary transformed XZ coordinates; outward convex turns between adjacent edge segments independently count marginal lobes; endpoints are basal join and apex, not extra lobes.','pass':all(x['convex_lobe_count']==7 for x in rows)};json.dump(r,O.open('x'),indent=2);print(r['pass'],[x['convex_lobe_count']for x in rows])
