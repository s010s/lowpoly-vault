# SPDX-License-Identifier: MIT
import bpy,json,sys,pathlib,math,datetime,os,hashlib
from mathutils import Vector
B=pathlib.Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(B/'source.blend'));aid=B.parent.name;groups={}
for o in bpy.context.scene.objects:
 if o.type=='MESH':
  for g in o.vertex_groups:groups[g.name]=[o.matrix_world@v.co for v in o.data.vertices if any(k.group==g.index for k in v.groups)]
sem=json.load(open(B/'geometry-semantics.json'));tubes={}
for t in sem['tubes']:tubes.setdefault(t['group'],t)
centers=lambda g:[sum(groups[g][i:i+tubes[g]['sides']],Vector())/tubes[g]['sides'] for i in range(0,len(groups[g]),tubes[g]['sides'])]
main=groups['main-axis'];checks={};measure={}
if aid=='sigillaria':
 ring=main[:48];c=sum(ring,Vector())/len(ring);r=[math.hypot(v.x-c.x,v.y-c.y)for v in ring];peaks=[i for i in range(48)if r[i]>r[i-1] and r[i]>r[(i+1)%48]];measure['actual_trunk_ring_radial_maxima_count']=len(peaks);measure['actual_trunk_ring_radii_m']=r;checks['twelve_actual_ribs']=len(peaks)==12;measure['scar_columns']={str(i):len([g for g in groups if g.startswith(f'scar-{i:02d}-')])for i in range(12)};checks['sixteen_scars_in_each_column']=set(measure['scar_columns'].values())=={16}
else:
 t=tubes['main-axis'];cs=centers('main-axis');r=[sum((v-c).length for v in main[i*t['sides']:(i+1)*t['sides']])/t['sides']for i,c in enumerate(cs)];measure['main_axis_actual_ring_centers_m']=[list(c)for c in cs];measure['main_axis_actual_ring_mean_radii_m']=r
 if aid in ['calamites','pseudobornia']:
  peaks=[i for i in range(1,len(r)-1)if r[i]>r[i-1] and r[i]>r[i+1]];measure['actual_swollen_node_count']=len(peaks);checks['actual_main_axis_nodes']=len(peaks)==(8 if aid=='calamites'else 4)
  prefix='primary-'if aid=='calamites'else'second-';tier={}
  for g in groups:
   if g.startswith(prefix):z=round(centers(g)[0].z,5);tier[str(z)]=tier.get(str(z),0)+1
  measure['actual_branch_base_tiers']=tier;checks['tier_counts']=sorted(tier.values())==([5,5,5,5]if aid=='calamites'else[1,1,2,2])
  whorls=[]
  for f in sem['leaf_frames']:
   v=groups[f['group']];n=f['outline_vertices'];ix=[0,n]if n==4 else[0,n-1,n,2*n-1];c=sum((v[i]for i in ix),Vector())/len(ix);match=next((w for w in whorls if(Vector(w['base_world_m'])-c).length<1e-6),None)
   if match:match['leaves']+=1
   else:whorls.append({'base_world_m':list(c),'leaves':1})
  measure['actual_leaf_whorls']=whorls;checks['leaf_whorls_and_counts']=len(whorls)==(80 if aid=='calamites'else 24) and all(w['leaves']==(7 if aid=='calamites'else 4)for w in whorls)
 if aid=='rhacophyton':
  attachments=sem['attachments'];measure['pinna_parent_counts']={g:sum(a['parent']==g and a['child'].startswith('pinna-')for a in attachments)for g in groups if g.startswith('frond-')};measure['forklet_parent_counts']={g:sum(a['parent']==g and a['child'].startswith('forklet-')for a in attachments)for g in groups if g.startswith('pinna-')};checks['eight_pinnae_per_frond']=set(measure['pinna_parent_counts'].values())=={8};checks['four_forklets_per_pinna']=set(measure['forklet_parent_counts'].values())=={4}
d={'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'source_sha256':hashlib.sha256((B/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((B/'model.glb').read_bytes()).hexdigest(),'measurements':measure,'checks':checks,'pass':all(checks.values()),'note':'Supplemental exact-source hierarchy measurements. World-space station radii/leaf-base positions are actual vertices. 1micrometre clustering tolerance only groups analytically co-located leaf bases after float32 evaluation, not a loosened physical dimension. Original frozen art dimensions remain nominal; no normalization.'};(B/'hierarchy-measurements.json').write_text(json.dumps(d,indent=2)+'\n');print(aid,checks);assert d['pass']
