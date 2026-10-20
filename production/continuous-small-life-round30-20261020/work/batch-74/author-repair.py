from pathlib import Path
import json,hashlib,datetime
R=Path.cwd();W=R/'production/continuous-small-life-round30-20261020/work/batch-74';s=(W/'generator.py').read_text();s=s.replace('Geometry authored after actual batch74 design freeze2026-10-20T15:20:41Z.','Geometry repair authored after actual r002 freeze2026-10-20T15:26:09Z. Original r001 generator retained.')
s=s.replace('z=.00085+.00155*max(0,1-u*u)','z=.00085+.0011*max(0,1-u*u)')
s=s.replace('width=.19+.045*u','width=.15+.015*u').replace('z+=.00135*','z+=.00175*').replace('z+=.00040*','z+=.00048*').replace('z-=.00052*','z-=.00080*').replace('pitaxis=k*math.tau/3+.55','pitaxis=k*math.tau/3+.74').replace("vs=[(0,0,.0029)]","vs=[(0,0,.00255)]")
s=s.replace("segments=[(p[i],p[i+1]) for p in paths for i in range(len(p)-1)]","paths=[[(x,y,max(1.7,w)) for x,y,w in path] for path in paths]\n segments=[(p[i],p[i+1]) for p in paths for i in range(len(p)-1)]")
start=s.index(" # Full host beds, genuinely recessed coal")
end=s.index("\nfor (name,mat),(vs,fs) in groups.items():",start)
s=s[:start]+''' # Repair true host contacts, inset core and irregular cleated front blocks.
 def host(name,z0,z1,mat,phase):
  nx=20;ny=8;top=[];bottom=[]
  for i in range(nx):
   x=-1.82+3.64*i/(nx-1)
   for j in range(ny):
    t=j/(ny-1);yf=-.70+.045*math.sin(i*1.9+phase);yb=.69+.04*math.sin(i*1.4)
    y=yf*(1-t)+yb*t;xx=x+(.025*math.sin(i*2+j*3) if i not in [0,nx-1] else 0)
    top.append((xx,y,z1+.075*math.sin(i*1.7+j*2.1+phase)+.025*math.cos(i*.6-j)))
    bottom.append((xx*.99,y*.97,z0+.034*math.sin(i*1.3+j+phase)))
  fs,per=grid_faces(nx,ny);n=len(top);faces=fs+[tuple(n+q for q in reversed(f)) for f in fs]
  for i in range(len(per)):
   a=per[i];b=per[(i+1)%len(per)];faces.extend([(a,n+a,n+b),(a,n+b,b)])
  part(name,top+bottom,faces,mat)
 host('uneven_resistant_lower_host_bed',.045,.77,'hostshade',.2)
 host('uneven_resistant_upper_host_bed',1.61,2.48,'host',2.1)
 # Solid coal behind cleats, buried at contacts. No through-sky slots.
 loft('recessed_coal_interior_continuous_core',[[(-1.69,.055,.65),(1.69,.055,.65),(1.69,.60,.65),(-1.69,.60,.65)],[(-1.69,.055,1.76),(1.69,.055,1.76),(1.69,.60,1.76),(-1.69,.60,1.76)]],'coal')
 cuts=[-1.70,-1.39,-1.18,-.84,-.39,-.16,.22,.47,.91,1.17,1.48,1.68]
 for i,(x0,x1) in enumerate(zip(cuts,cuts[1:])):
  # Unequal face cleats down the full height. Staggered depth-plane butt cleats.
  yfront=-.40+.075*math.sin(i*1.9);ys=[yfront,-.07+.07*math.sin(i*2.8),.20+.04*math.cos(i),.61]
  for j,(ya,yb) in enumerate(zip(ys,ys[1:])):
   gap=.006;a=x0+.006;b=x1-.006;c=ya+gap;d=yb-gap;w=min(.035,(b-a)*.16)
   xy=[(a+w,c),(b-w*.7,c+.012*math.sin(i)),(b,c+w),(b,d-w*.8),(b-w,d),(a+w*.8,d),(a,d-w),(a,c+w)]
   rings=[]
   for k,z in enumerate([.65,.86,1.06,1.28,1.49,1.76]):
    ring=[]
    for q,(x,y) in enumerate(xy):
     dx=.009*math.sin(i*4+j*2+k*2.4+q);dy=.026*math.sin(i*3+k*2.3+q*.7)
     if q in [0,1]:dy+=.028*math.sin(i*2+k*3)
     ring.append((x+dx,y+dy,z+.018*math.sin(i+j*3+k+q)))
    rings.append(ring)
   loft('unequal_chipped_face_cleat_front_short_staggered_butt_cleats',rings,'coalbright' if (i+j)%5==0 else 'coal')
''' +s[end:]
s=s.replace("obj=mesh_object(name,vs,fs,m[mat],col)","""obj=mesh_object(name,vs,fs,m[mat],col)
 if slug=='crevasse-splay' and name.startswith('continuous_shallow'):
  import bmesh
  bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001);bm.to_mesh(obj.data);bm.free();obj.data.update()
""")
# Do not mutate original build/helper identity.
(W/'generator-r002.py').write_text(s)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for x in json.load(open(W/'final-selection.json')):
 if x['revision']!='r002':continue
 b=R/x['path'];(b/'generator.py').write_text(s);d={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator_sha256':H(b/'generator.py'),'config_sha256':H(b/'build-config.json'),'files':{n:H(R/n) for n in ['scripts/asset_common.py','scripts/qa_glb.py','package.json','package-lock.json']},'blender':'4.3.2','python':'Blender bundled Python','three':'0.180.0','seed':74,'textures':0,'external_meshes':False};(b/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
