import sys,json,pathlib,math,hashlib,collections
W=pathlib.Path('/workspace/shared/lowpoly-batch89-20261020');O=pathlib.Path('/workspace/shared/lowpoly-batch89-independent-qa-20261020');sys.path.insert(0,str(W/'scripts'));from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform,IDENTITY
hand=json.loads((W/'production/small-life-batch89/maker-handoff.json').read_text())
for it in hand['items']:
 aid=it['asset_id'];path=W/it['artifacts']['glb']['path'];doc,bin,data=read_glb(path);meshes=[]
 def walk(i,parent):
  n=doc['nodes'][i];m=matmul(parent,node_matrix(n))
  if 'mesh' in n:meshes.append((doc['meshes'][n['mesh']],m))
  for c in n.get('children',[]):walk(c,m)
 for i in doc['scenes'][doc.get('scene',0)]['nodes']:walk(i,IDENTITY)
 # Reconstruct topology by exact POSITION welding within each material, independently of config counts.
 pts=[];faces=[];materials=[];lookup={}
 for mesh,matrix in meshes:
  for pr in mesh['primitives']:
   mat=doc['materials'][pr['material']]['name'];pv=[transform(matrix,v) for v in accessor_values(doc,bin,pr['attributes']['POSITION'])];ix=[x[0] for x in accessor_values(doc,bin,pr['indices'])];local=[]
   for p in pv:
    key=(mat,p)
    if key not in lookup:lookup[key]=len(pts);pts.append(p);materials.append(mat)
    local.append(lookup[key])
   faces += [tuple(local[x] for x in ix[k:k+3]) for k in range(0,len(ix),3)]
 adj=[set() for p in pts]
 for face in faces:
  for a,b in zip(face,face[1:]+face[:1]):adj[a].add(b);adj[b].add(a)
 unseen=set(range(len(pts)));comps=[]
 while unseen:
  st=min(unseen);seen={st};unseen.remove(st);stack=[st]
  while stack:
   for i in adj[stack.pop()]:
    if i in unseen:unseen.remove(i);seen.add(i);stack.append(i)
  pp=[pts[i] for i in seen];lo=[min(p[k] for p in pp) for k in range(3)];hi=[max(p[k] for p in pp) for k in range(3)];center=[(a+b)/2 for a,b in zip(lo,hi)];c={'index':len(comps),'material':materials[st],'vertices_welded':len(pp),'bounds_glb_m':{'min':lo,'max':hi,'size':[b-a for a,b in zip(lo,hi)]}}
  if aid=='skolithos-pipe-field' and c['material'].endswith('-2'):
   rr=[math.hypot(p[0]-center[0],p[2]-center[2]) for p in pp];c.update(circumradius_min_m=min(rr),circumradius_max_m=max(rr),center_xz_m=[center[0],center[2]],bottom_y_m=lo[1],top_y_m=hi[1])
  comps.append(c)
 r={'asset_id':aid,'revision':it['revision'],'glb_sha256':hashlib.sha256(data).hexdigest(),'method':'Decoded exact GLB POSITION and index data, full scene transforms, exact position welding within material, connectivity traversal. No config counts used.','textures':len(doc.get('textures',[])),'images':len(doc.get('images',[])),'materials':doc['materials'],'component_count_by_material':dict(collections.Counter(c['material'] for c in comps)),'components':comps}
 if aid=='skolithos-pipe-field':
  shafts=[c for c in comps if 'circumradius_min_m' in c];r['shaft_count']=len(shafts);r['frozen_range_m']=[.0026,.0048];r['all_shafts_within_frozen_range']=all(c['circumradius_min_m']>=.0026 and c['circumradius_max_m']<=.0048 for c in shafts);r['minimum_circumradius_m']=min(c['circumradius_min_m'] for c in shafts);print(aid,r['shaft_count'],r['minimum_circumradius_m'],r['all_shafts_within_frozen_range'])
 (O/aid/'own-decoded-glb-features.json').write_text(json.dumps(r,indent=2)+'\n')
