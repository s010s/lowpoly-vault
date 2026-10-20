import pathlib,datetime,json,hashlib
r=pathlib.Path.cwd();w=r/'production/continuous-small-life-round32-20261020/work/batch-78'
old=pathlib.Path('/workspace/shared/lowpoly-batch76-20261020/production/continuous-small-life-round31-20261020/work/batch-76/generator-final.py').read_text();prefix=old[:old.index('# Original geometry authored')];suffix=old[old.index('ground_asset(col,center_xy=True)'):]
body=r'''
# Original batch78 geometry authored only after complete immutable four-asset freezes.
if slug=='pteridinium':
 # One continuous closed Y-section fossil body, quilted outer and inner surfaces.
 N=100;vs=[];cross=[]
 # Trace cross-section counterclockwise around three joined thin vanes.
 for side in [-1,1]:
  pts=[]
  for j in range(9):
   u=j/8;pts.append((side*.035*u,.005+.021*u*u-.0011,u,side))
  for j in reversed(range(9)):
   u=j/8;pts.append((side*.035*u,.005+.021*u*u+.0011,u,side))
  if side==-1:cross.extend(pts)
 # Central vane with two faces from common seam.
 for j in range(1,10):cross.append((-.0012,.005+.037*j/9,j/9,-2))
 for j in reversed(range(1,10)):cross.append((.0012,.005+.037*j/9,j/9,2))
 # Right wing trace reverse relative to left, no self crossing.
 for j in range(9):
  u=j/8;cross.append((.035*u,.005+.021*u*u+.0011,u,1))
 for j in reversed(range(9)):
  u=j/8;cross.append((.035*u,.005+.021*u*u-.0011,u,1))
 nc=len(cross)
 for j in range(N+1):
  t=.009+.982*j/N;en=math.sin(math.pi*t)**.72
  for y,z,u,side in cross:
   phase=t*22*math.tau+u*1.1+(math.pi if side>0 else 0)
   rib=max(0,math.cos(phase))**3*.0011*en*math.sin(math.pi*min(1,u))**.4
   # Relief displaces away from each vane midplane, not disconnected tubes.
   if abs(side)==2:yy=y*en+math.copysign(rib,y);zz=z*en
   else:yy=y*en;zz=(z+rib)*en
   vs.append((.20*(t-.5),yy,zz))
 fs=[]
 for j in range(N):
  for i in range(nc):a=j*nc+i;b=j*nc+(i+1)%nc;fs.extend([(a,b,b+nc),(a,b+nc,a+nc)])
 lo=len(vs);vs.append((-.10,0,.001));hi=len(vs);vs.append((.10,0,.001))
 fs.extend((lo,(i+1)%nc,i) for i in range(nc));fs.extend((hi,N*nc+i,N*nc+(i+1)%nc) for i in range(nc))
 part('integrated_three_quilted_vanes_canoe_fossil_interpreted_posture',vs,fs,'fossil')
 # Supporting small irregular sandstone matrix is below, no reference scan.
 ellipsoid('small_original_supporting_fossil_matrix',(0,0,-.002),(.082,.022,.003),'matrix',16,4)
elif slug=='pingo':
 # Partial radial domain removes one sector as an explicitly schematic teaching cutaway.
 nr=26;na=80;ph0=-.18;ph1=math.tau-1.0;vs=[];fs=[];tags=[]
 def height(r,ph):
  rho=r/18;z=.55+11.8*max(0,1-rho*rho)**2.1
  # Unequal narrow summit tension fissures, not circular crater.
  if r<6.8:
   d=min(abs(r*math.sin(ph-.25)),abs(r*math.sin(ph-2.1)),abs(r*math.sin(ph-4.25)))
   z-=1.05*math.exp(-(d/.18)**2)*math.exp(-(r/5.5)**4)
  return z+.12*math.sin(ph*3+r*.35)*min(1,r/2)
 for k in range(nr+1):
  r=.12+(18-.12)*k/nr
  for i in range(na+1):
   ph=ph0+(ph1-ph0)*i/na;vs.append((r*math.cos(ph),r*.89*math.sin(ph),height(r,ph)))
 for k in range(nr):
  for i in range(na):
   a=k*(na+1)+i;b=a+na+1;fs.extend([(a,b,b+1),(a,b+1,a+1)]);tags.extend(['turf','turf'])
 # Inner tiny perimeter capped, outer boundary and two radial schematic cut surfaces.
 perimeter=[i for i in reversed(range(na+1))]+[k*(na+1) for k in range(1,nr+1)]+[nr*(na+1)+i for i in range(1,na+1)]+[k*(na+1)+na for k in reversed(range(1,nr))]
 # Domain perimeter cycle follows top mesh; use soil upper side strip and ice below on cuts.
 lower=[];bottom=[]
 for idx in perimeter:
  x,y,z=vs[idx];is_cut=(idx%(na+1) in [0,na]) and idx//(na+1)<nr
  lower.append(len(vs));vs.append((x,y,max(.05,z-.7)))
  bottom.append(len(vs));vs.append((x,y,0))
 for j,idx in enumerate(perimeter):
  q=(j+1)%len(perimeter);nxt=perimeter[q];is_cut=abs(math.atan2(vs[idx][1]/.89,vs[idx][0])-ph0)<.001 or (idx%(na+1)==na and nxt%(na+1)==na)
  fs.append((idx,nxt,lower[q],lower[j]));tags.append('soil')
  fs.append((lower[j],lower[q],bottom[q],bottom[j]));tags.append('ice' if is_cut and max(vs[idx][2],vs[nxt][2])>1.4 else 'soil')
 fs.append(tuple(reversed(bottom)));tags.append('soil')
 # Material split preserves a single full-volume mesh, no overlapping core under skin.
 for mat in ['turf','soil','ice']:
  chosen=[f for f,t in zip(fs,tags) if t==mat];part('continuous_pingo_cutaway_'+mat,vs,chosen,mat)
elif slug=='sill-ledge':
 n=96;vs=[];fs=[];tags=[]
 levels=[(0,1.02,'host'),(.12,1,'host'),(.75,.94,'host'),(.81,.91,'hostshade'),(.91,.94,'host'),(1.5,.91,'host'),(1.57,.88,'hostshade'),(1.68,.92,'host'),(2.25,.88,'host'),(2.5,.88,'baked'),(2.67,1.08,'baked'),(2.76,1.12,'sill'),(4.26,1.12,'sill'),(4.36,.94,'baked'),(4.54,.91,'baked'),(5.0,.91,'host'),(5.08,.88,'hostshade'),(5.2,.90,'host'),(5.85,.87,'host'),(5.93,.85,'hostshade'),(6.05,.88,'host'),(6.65,.84,'host')]
 for k,(z,scale,mat) in enumerate(levels):
  for i in range(n):
   ph=math.tau*i/n;c=math.cos(ph);s=math.sin(ph);rad=min(6/max(abs(c),1e-8),3.5/max(abs(s),1e-8));irreg=1+.035*math.sin(7*ph)+.018*math.cos(13*ph)
   # Sparse blocky vertical joints physically recess the sill face, not drawn stripes.
   joint=(max(0,math.cos(ph*12+.7))**22)*(.13 if mat=='sill' else .025)
   x=rad*c*scale*irreg*(1-joint);y=rad*s*scale*irreg*(1-joint);zz=z+.12*x+.04*math.sin(ph*5)
   vs.append((x,y,zz))
 for k in range(len(levels)-1):
  for i in range(n):a=k*n+i;b=k*n+(i+1)%n;fs.append((a,b,b+n,a+n));tags.append(levels[k+1][2])
 fs.append(tuple(reversed(range(n))));tags.append('host');fs.append(tuple((len(levels)-1)*n+i for i in range(n)));tags.append('host')
 for mat in ['host','hostshade','sill','baked']:part('integrated_dipping_sill_ledge_'+mat,vs,[f for f,t in zip(fs,tags) if t==mat],mat)
elif slug=='exfoliation-dome':
 # Coherent massive body, no horizontal stacked tiers.
 n=56;kmax=22;vs=[]
 def dome(th,ph,r=1):return (7*r*math.sin(th)*math.cos(ph),6*r*math.sin(th)*math.sin(ph),7.8*r*math.cos(th))
 for k in range(kmax+1):
  th=.025+(math.pi/2-.025)*k/kmax
  for i in range(n):
   ph=math.tau*i/n;v=dome(th,ph);vs.append((v[0]*(1+.015*math.sin(ph*5)),v[1],v[2]+.07*math.sin(ph*3)*math.sin(th)))
 fs=[]
 for k in range(kmax):
  for i in range(n):a=k*n+i;b=k*n+(i+1)%n;fs.extend([(a,b,b+n),(a,b+n,a+n)])
 fs.append(tuple(reversed(range(n))));fs.append(tuple(kmax*n+i for i in range(n)));part('coherent_rounded_massive_granite_body',vs,fs,'granite')
 # Broad locally lifted curved slabs, conformal to core and well separated, closed thin volumes.
 for patch,(pc,span,ts,te) in enumerate([(.55,.66,.53,1.45),(3.45,.58,.78,1.48)]):
  nu=14;nv=18;v=[]
  for layer in [0,1]:
   for i in range(nu+1):
    u=i/nu;ph=pc+span*(2*u-1)
    for j in range(nv+1):
     t=j/nv;th=ts+(te-ts)*t+.035*math.sin(u*8+patch)*math.sin(math.pi*t)
     # Upper edge rises slightly, underside remains outside entire core envelope.
     lift=.045+.030*(1-t)**2+.008*math.sin(u*6)**2
     r=1+lift+(.018 if layer else 0)
     v.append(dome(th,ph,r))
  nn=(nu+1)*(nv+1);f=[]
  for i in range(nu):
   for j in range(nv):
    a=i*(nv+1)+j;b=a+nv+1;f.append((a,a+1,b+1,b));f.append((a+nn,b+nn,b+1+nn,a+1+nn))
  per=[i*(nv+1) for i in range(nu+1)]+[nu*(nv+1)+j for j in range(1,nv+1)]+[i*(nv+1)+nv for i in reversed(range(nu))]+[j for j in reversed(range(1,nv))]
  for i,a in enumerate(per):b=per[(i+1)%len(per)];f.append((a,b,b+nn,a+nn))
  part('broad_curved_local_exfoliation_sheet_'+str(patch),v,f,'sheet')
# Weld material boundaries so intentionally shared physical contacts do not become open source seams.
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
if slug in ['pingo','sill-ledge']:
 objects=[o for o in col.all_objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();o=bpy.context.object
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=.000001);bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT')
'''
s=prefix+body+'\n'+suffix;s=s.replace('Original batch74 geometry','Original batch78 geometry');(w/'generator.py').write_text(s)
for x in json.loads((w/'final-selection.json').read_text()):
 b=r/x['path'];(b/'generator.py').write_text(s)
 deps={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender':'4.3.2','seed':78,'generator_sha256':hashlib.sha256(s.encode()).hexdigest(),'files':{n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ['scripts/asset_common.py','scripts/qa_glb.py']},'three_version':'0.180.0','no_reference_mesh_or_texture':True};(b/'build-dependencies.json').write_text(json.dumps(deps,indent=2)+'\n')
