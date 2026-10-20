from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round25-20261020/work/batch-65';B=R/'assets/candidates/continuous-small-life-round25-20261020/batch-65/breccia-outcrop';a=B/'r001';b=B/'r002';b.mkdir(exist_ok=True);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
for n in ['concept-original.png','concept-prompt.txt','concept-generation.json','references.json','brief.md']:shutil.copy(a/n,b/n)
for n in ['brief.json','build-config.json']:
 d=json.load(open(a/n));d['revision']='r002'
 if n=='brief.json':d['brief_version']='r002';d['created_at']=now();d['concept_decisions']+=' r002 repair: cast placement rays against actual irregular host surface, not nominal ellipse, so all angular fragments are embedded shallowly and visible across every exposed face. Increase varied angular fragment coverage; no scope change.'
 else:d['modeling_decisions']+=' r002: actual-host ray projection and denser90side/30crown fragment field, varied size .12-.40m. Visible coverage repair, not a scientific claim change.'
 (b/n).write_text(json.dumps(d,indent=2)+'\n')
(b/'brief.md').write_text((b/'brief.md').read_text()+'\nr002 visible improvement: ray-project shallow embedded angular clasts onto actual host, increase coverage instead of hiding most fragments under matrix.\n')
(b/'modeling-freeze.json').write_text(json.dumps({'asset_id':'breccia-outcrop','revision':'r002','frozen_at':now(),'status':'Pre-repair revised design freeze. r001 preserved; no model authored for r002 yet','files':{n:H(b/n) for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json']}},indent=2)+'\n')
s=(a/'generator.py').read_text();s=s.replace("loft('coherent_angular_matrix_outcrop',rings,'matrix')","""loft('coherent_angular_matrix_outcrop',rings,'matrix')
 from mathutils.bvhtree import BVHTree
 host_vs,host_fs=groups[('coherent_angular_matrix_outcrop','matrix')]
 host_bvh=BVHTree.FromPolygons([Vector(v) for v in host_vs],host_fs,all_triangles=False)""")
s=s.replace('for k in range(60):','for k in range(90):').replace("c=(1.50*rscale*math.cos(a),1.025*rscale*math.sin(a),z);u=(-math.sin(a),math.cos(a),0);v=(0,0,1)\n  clast('embedded_angular_surface_fragments',c,u,v,.15,.10+.23*rng.random()", """outside=Vector((4*math.cos(a),4*math.sin(a),z));direction=Vector((-math.cos(a),-math.sin(a),0));hit,normal,idx,dist=host_bvh.ray_cast(outside,direction)
  if hit is None:continue
  c=hit+normal*.012;u=Vector((0,0,1)).cross(normal).normalized();v=normal.cross(u).normalized()
  clast('embedded_angular_surface_fragments',c,u,v,.18,.12+.28*rng.random()""")
s=s.replace('for k in range(23):','for k in range(30):').replace("clast('embedded_angular_crown_fragments',c,(1,0,0),(0,1,0),.17,.09+.20*rng.random()", """hit,normal,idx,dist=host_bvh.ray_cast(Vector((c[0],c[1],4)),Vector((0,0,-1)))
  if hit is None:continue
  c=hit+normal*.012;u=Vector((0,1,0)).cross(normal).normalized();v=normal.cross(u).normalized()
  clast('embedded_angular_crown_fragments',c,u,v,.18,.10+.20*rng.random()""")
(b/'generator.py').write_text(s);(b/'authoring-start.json').write_text(json.dumps({'observed_at':now(),'note':'Actual r002 revision authoring observed after freeze'})+'\n');final=json.load(open(W/'final-selection.json'))
for x in final:
 if x['asset_id']=='breccia-outcrop':x['revision']='r002';x['path']=str(b.relative_to(R))
(W/'final-selection.json').write_text(json.dumps(final,indent=2)+'\n');print(now())
