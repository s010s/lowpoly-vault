from pathlib import Path
w=Path(__file__).parent;old=Path('/workspace/shared/lowpoly-batch74-20261020/production/continuous-small-life-round30-20261020/work/batch-74/generator.py').read_text()
head=old[:old.index('# Geometry authored')]
helpers=old[old.index('import random'):old.index("if slug=='tribrachidium':")]
geom='''# Original geometry authored after four immutable premodel freezes2026-10-20T15:44:14.790616Z.
if slug=='rangea':
 # Single closed six-lobed bilaminar radial spindle. No stacked intersection tubes.
 nz=42;np=108;vs=[]
 for j in range(nz+1):
  t=.018+.964*j/nz;x=.14*(t-.5);width=.0225*math.sin(math.pi*t)**.83
  for i in range(np):
   ph=math.tau*i/np;u=(.5+.5*math.cos(6*ph))**3.5
   core=.00125*math.sin(math.pi*t)**.6
   # Chevron/rangeomorph primary units on both sides of each vane.
   q=((ph+math.pi/6)%(math.pi/3)-math.pi/6)/(math.pi/6)
   phase=t*17*math.tau+abs(q)*4.5
   primary=max(0,math.cos(phase))**5
   secondary=max(0,math.cos(t*51*math.tau+abs(q)*15))**8
   r=core+(width-core)*u
   # Surface relief along full-volume vane flanks, no free tentacles.
   r+=.0007*primary*(.22+.78*u)*math.sin(math.pi*t)
   r+=.00016*secondary*math.sin(math.pi*t)
   vs.append((x,r*math.cos(ph),r*math.sin(ph)))
 fs=[]
 for j in range(nz):
  for i in range(np):
   a=j*np+i;b=j*np+(i+1)%np;c=b+np;d=a+np;fs.extend([(a,b,c),(a,c,d)])
 fs+=[tuple(reversed(range(np))),tuple(nz*np+i for i in range(np))]
 part('six_bilaminar_radial_vanes_integrated_hierarchical_ribbed_fossil',vs,fs,'fossil')
elif slug=='serac':
 nx=57;ny=57;vs=[]
 for i in range(nx):
  for j in range(ny):
   x=-15+30*i/(nx-1);y=-15+30*j/(ny-1)
   u=x+.6*math.sin(y*.27)+.18*math.sin(y*.87)
   v=y+.5*math.sin(x*.31+1)
   dx=min(abs(u-4.1),abs(u+4.4));dy=min(abs(v-4.0),abs(v+4.7));d=min(dx,dy)
   ch=max(0,min(1,(d-.28)/.88));ch=ch*ch*(3-2*ch)
   central=abs(u)<3.6 and abs(v)<3.5
   roof=(16.8+.045*x-.12*y+1.0*math.sin(x*.6)*math.sin(y*.42)) if central else (5.5+.09*y+.6*math.sin(x*.35+y*.18))
   z=.65+(roof-.65)*ch
   if not central:z+=.15*math.sin(i*2.1+j*.7)*ch
   vs.append((x,y,z))
 fs,per=grid_faces(nx,ny);terrain('continuous_glacier_angular_tower_two_crossing_crevasse_systems',vs,fs,per,0,'ice')
elif slug=='moulin-shaft':
 n=64;nr=10;vs=[]
 def boundary(ph,k):
  # Rays connect an asymmetric opening to a square glacier tile.
  c=math.cos(ph);s=math.sin(ph);outer=10/max(abs(c),abs(s));inner=3.2*(1+.13*math.sin(3*ph)+.08*math.cos(5*ph))
  r=inner+(outer-inner)*k/nr;x=r*c;y=r*s
  inlet=math.exp(-(angdist(ph,math.pi/2)/.13)**2)
  z=11.8+.13*math.sin(ph*5+k*.9)-1.15*inlet
  return (x,y,z)
 for k in range(nr+1):
  for i in range(n):vs.append(boundary(math.tau*i/n,k))
 fs=[]
 for k in range(nr):
  for i in range(n):
   a=k*n+i;b=k*n+(i+1)%n;c=b+n;d=a+n;fs.extend([(a,d,c),(a,c,b)])
 # Inner walls are steep and visibly have depth, with a genuine open truncated lower shaft.
 inner_last=list(range(n))
 for level in [8.1,4.1,0]:
  start=len(vs)
  for i in range(n):
   ph=math.tau*i/n;x,y,z=boundary(ph,0);scale=.93 if level>4 else .85
   vs.append((x*scale,y*scale,level))
  new=list(range(start,start+n))
  for i in range(n):fs.append((inner_last[i],inner_last[(i+1)%n],new[(i+1)%n],new[i]))
  inner_last=new
 outerbottom=[]
 for i in range(n):
  x,y,z=vs[nr*n+i];outerbottom.append(len(vs));vs.append((x,y,0))
 for i in range(n):
  a=nr*n+i;b=nr*n+(i+1)%n;c=outerbottom[(i+1)%n];d=outerbottom[i];fs.append((a,b,c,d));fs.append((d,c,inner_last[(i+1)%n],inner_last[i]))
 part('true_open_upper_moulin_annular_ice_volume',vs,fs,'ice')
 # Original ribbon is inside the carved inlet/shaft, not a coplanar decal.
 wv=[]
 for k in range(12):
  y=10-6.9*k/11;z=10.70+.035*math.sin(k*.5)
  wv.extend([(-.29,y,z),(.29,y,z)])
 wf=[(2*k,2*k+1,2*k+3,2*k+2) for k in range(11)]
 part('shallow_surface_meltwater_inlet',wv,wf,'water')
 ph=math.pi/2;x,y,z=boundary(ph,0)
 part('upper_wall_meltwater_descent',[(-.24,y-.17,10.66),(.24,y-.17,10.66),(.19,y*.92-.15,4.35),(-.19,y*.92-.15,4.35)],[(0,3,2,1)],'water')
elif slug=='solifluction-lobe':
 nx=53;ny=65;vs=[]
 def lobe(x,y):
  width=5.3;u=abs(x-.25*math.sin(y*.3))/width
  if u>=1:return 0
  front=5.1+3.0*u*u+.18*math.sin(x*1.2)
  q=max(0,min(1,(y-front)/.45));q=q*q*(3-2*q)
  neck=max(0,min(1,(18.5-y)/4.8));neck=neck*neck*(3-2*neck)
  edge=max(0,min(1,(1-u)/.16));edge=edge*edge*(3-2*edge)
  return .65*q*neck*edge
 for i in range(nx):
  for j in range(ny):
   x=-9+18*i/(nx-1);y=24*j/(ny-1)
   z=1+.115*y+lobe(x,y)+.035*math.sin(x*.7+y*.4)
   # One much subtler offset partial lobe, not regular steps.
   z+=.12*math.exp(-((x+5)/3)**4)*math.exp(-((y-20)/2.2)**4)
   vs.append((x,y-12,z))
 fs,per=grid_faces(nx,ny);terrain('continuous_soil_mantle_shallow_rounded_downslope_tongue',vs,fs,per,0,'turf')

for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if slug in ['serac','moulin-shaft'] and mat=='ice':
  obj.data.materials.append(m['pale']);obj.data.materials.append(m['deepice' if slug=='serac' else 'wall'])
  for poly in obj.data.polygons:poly.material_index=1 if poly.normal.z>.55 else 2 if poly.normal.z<.4 else 0
 if slug=='solifluction-lobe':
  obj.data.materials.append(m['soil']);obj.data.materials.append(m['turfshade'])
  for poly in obj.data.polygons:
   if poly.normal.z<.85:poly.material_index=1
   elif math.sin(poly.center.x*.9+poly.center.y*.7)>.65:poly.material_index=2
'''
tail=old[old.index('ground_asset(col,center_xy=True)'):]
(w/'generator.py').write_text(head+helpers+geom+tail)
