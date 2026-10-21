#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Batch87 geometry-first repair. All frozen geometric controls are consumed.
Continuous watertight terrain surfaces, no voxel remeasurement drift.
"""
import sys,json,math,os,datetime,hashlib,argparse
from pathlib import Path
import bpy
from math import sin,cos,pi,exp
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset

def solid_grid(name,rows,m,col,assign):
 n=len(rows);k=len(rows[0]);v=[tuple(v) for row in rows for v in row];f=[];mi=[]
 for i in range(n-1):
  for j in range(k-1):
   a=i*k+j;b=a+1;c=b+k;d=a+k
   for ff in ([(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)]):f.append(ff);mi.append(assign(i,j))
 loop=list(range(k))+[i*k+k-1 for i in range(1,n)]+list(range((n-1)*k+k-2,(n-1)*k-1,-1))+[i*k for i in range(n-2,0,-1)]
 start=len(v);v += [(v[a][0],v[a][1],0) for a in loop];L=len(loop)
 for j,a in enumerate(loop):f.append((a,loop[(j+1)%L],start+(j+1)%L,start+j));mi.append(0)
 f.append(tuple(range(start,start+L))[::-1]);mi.append(0)
 o=mesh_object(name,v,f,m,col)
 for p,idx in zip(o.data.polygons,mi):p.material_index=idx
 return o

def spatter(c,m,col):
 p=c['parameters'];N=p['angular_segments'];intervals=p['radial_profile_segments'];groups=p['welded_lobe_groups'];R=p['outer_radius_m'];vr=p['vent_radius_m'];h=p['rim_height_m'];floor=p['vent_floor_m'];W,D,H=c['art_target_bounds_blender_xyz_m']
 # 15 immutable construction stations; exterior-only midpoint tessellation resolves fused welts.
 base=[(.12/vr,0),(.38/vr,0),(.44/vr,.16),(.50/vr,.47),(.56/vr,.80),(.60/vr,.94),(1,1),(.90/vr,.975),(1.20/vr,.93),(1.55/vr,.78),(2.0/vr,.53),(2.45/vr,.31),(2.9/vr,.15),(3.3/vr,.06),(R/vr,.012)]
 if intervals!=14:raise ValueError('Frozen profile uses 14 intervals / 15 stations.')
 centers=[2*pi*g/groups+.13*sin(g*1.63+.4) for g in range(groups)]
 q=[sin(3*2*pi*j/N+.5)+.65*cos(5*2*pi*j/N-.3)+.22*sin(11*2*pi*j/N) for j in range(N)];mean=sum(q)/N;q=[x-mean for x in q];q=[x*(H-h)/max(q) for x in q]
 radius=[vr*(1+.085*sin(3*2*pi*j/N+.2)+.045*cos(5*2*pi*j/N-.4)) for j in range(N)];radius=[x*vr/(sum(radius)/N) for x in radius]
 foot=[(R*(1+.085*sin(3*2*pi*j/N+.4)+.04*cos(5*2*pi*j/N-.3))*cos(2*pi*j/N),R*(1+.085*sin(3*2*pi*j/N+.4)+.04*cos(5*2*pi*j/N-.3))*sin(2*pi*j/N)) for j in range(N)]
 lo=[min(x[k] for x in foot) for k in range(2)];hi=[max(x[k] for x in foot) for k in range(2)];foot=[tuple((xy[k]-(lo[k]+hi[k])/2)*[W,D][k]/(hi[k]-lo[k]) for k in range(2)) for xy in foot]
 samples=[];original_indices=[]
 for k,pt in enumerate(base):
  original_indices.append(len(samples));samples.append((float(k),*pt))
  if 6<=k<intervals:samples.append((k+.5,(pt[0]+base[k+1][0])/2,(pt[1]+base[k+1][1])/2))
 v=[];faces=[];mi=[];reliefs=[]
 for sk,rf,zf in samples:
  for j in range(N):
   a=2*pi*j/N;r=rf*vr;crest=h+q[j];relief=0
   if sk<=6:
    rr=radius[j]*rf;zz=floor+zf*(crest-floor);x,y=rr*cos(a),rr*sin(a)
   else:
    t=(r-vr)/(R-vr)
    for g,aa in enumerate(centers):
     for layer in range(2):
      rc=1.13+.32*sin(g*1.31+layer*2.7)+.93*layer
      da=(a-aa-.19*sin(g+layer*2.1)+pi)%(2*pi)-pi
      relief+=(1.3+.5*cos(g*.9)**2)*exp(-(da/(.16+.06*cos(g)**2))**2-((r-rc)/(.30+.15*sin(g+layer)**2))**2)
    # Rounded staggered relief remains below the actual crest without clipping or Z scaling.
    bulge=math.tanh(relief);weight=sin(pi*t)**.7
    rr=r+.39*bulge*weight+.055*sin(17*a+sk*2.9)*weight
    zz=crest*(zf+(1-zf)*.63*bulge*weight)
    zz+=.055*sin(13*a+sk*2.17)*sin(pi*t)**2
    w=t*t;x=rr*cos(a)+w*(foot[j][0]-R*cos(a));y=rr*sin(a)+w*(foot[j][1]-R*sin(a))
   v.append((x,y,zz));reliefs.append(relief)
 faces.append(tuple(range(N))[::-1]);mi.append(3)
 for k in range(len(samples)-1):
  for j in range(N):
   a=k*N+j;b=k*N+(j+1)%N;cc=b+N;d=a+N
   for ff in ([(a,b,cc),(a,cc,d)] if (k+j)%2 else [(a,b,d),(b,cc,d)]):
    faces.append(ff);mi.append(3 if samples[k][0]<4 else 1 if reliefs[a]>.9 else 2 if sin(j*1.63+k*2.17)>.96 else 0)
 bottom=len(v);foot_start=(len(samples)-1)*N;v += [(v[foot_start+j][0],v[foot_start+j][1],0) for j in range(N)]
 for j in range(N):faces.append((foot_start+j,foot_start+(j+1)%N,bottom+(j+1)%N,bottom+j));mi.append(0)
 faces.append(tuple(range(bottom,bottom+N))[::-1]);mi.append(0)
 o=mesh_object('continuous-welded-spatter-floor-crest-foot',v,faces,m,col)
 for f,idx in zip(o.data.polygons,mi):f.material_index=idx
 o['construction_angular_rays']=N;o['construction_radial_intervals']=intervals;o['construction_profile_stations']=len(base);o['construction_welded_lobe_groups']=groups;o['crest_station']=6;o['floor_stations']='0,1';o['measurement_note']='64 crest vertices are the local radial height maxima. Exterior midpoints tessellate original intervals without redefining construction count.'
 return {'ring_size':N,'construction_profile_stations':len(base),'tessellated_surface_rings':len(samples),'original_station_final_ring_indices':original_indices,'crest_vertex_indices':list(range(6*N,7*N)),'floor_vertex_indices':list(range(2*N)),'lobe_group_angles_radians':centers,'lobe_layers_per_group':2,'nominal_construction_radius_m':R}

def travertine(c,m,col):
 p=c['parameters'];N=p['cross_segments'];levels=p['terrace_levels'];rise=p['rise_per_level_m'];lip=p['pool_rim_relief_m'];W=p['width_m'];Ltot=p['length_m'];H=c['art_target_bounds_blender_xyz_m'][2]
 if p['pool_floor_color']!='opaque stylized water-bearing floor region':raise ValueError('Only frozen opaque floor color semantics supported')
 weights=[2.6,3.4,3.1,4.4,4.5]
 if levels!=len(weights):raise ValueError('Five unequal shelf lengths are frozen')
 lengths=[x/sum(weights)*Ltot for x in weights];rows=[];regions=[]
 for level in range(levels):
  L=lengths[level];y0=Ltot/2-sum(lengths[:level]);floor=(levels-1)*rise+.85-level*rise
  specs=[(0,lip),(.20,0),(L-.78,0),(L-.52,lip),(L-.32,lip),(L,lip-rise)]
  for k,(dy,dz) in enumerate(specs):
   if level>0 and k==0:continue
   row=[]
   for j in range(N+1):
    t=-1+2*j/N;side=abs(t);width=W*(.225+.25*(Ltot/2-y0+dy)/Ltot)*(1+.065*sin((y0-dy)*1.2));x=width*t+.038*W*sin((y0-dy)*.36)
    scallop=.33*cos(t*pi*2+.2*level)+.15*sin(t*pi*5+.6*level);y=y0-dy+scallop*(1 if level<levels-1 or k<5 else .35)
    edge=.20*max(0,(side-.78)/.22);z=floor+dz+edge
    if side>.83:z+=.035*sin(j*1.3+level*2+k*.9)
    if k in (3,4):z-=lip*(.15/.18)*exp(-((t-(.27 if level%2 else -.22))/.13)**2)
    row.append((x,y,z))
   rows.append(row);regions.append((level,k))
 shift=H-max(z for row in rows for x,y,z in row);lo=[min(v[k] for row in rows for v in row) for k in range(2)];hi=[max(v[k] for row in rows for v in row) for k in range(2)]
 rows=[[((x-(lo[0]+hi[0])/2)*W/(hi[0]-lo[0]),(y-(lo[1]+hi[1])/2)*Ltot/(hi[1]-lo[1]),z+shift) for x,y,z in row] for row in rows]
 def idx(i,j):
  level,k=regions[i];_,nk=regions[i+1]
  if k==1 and nk==2 and j>=3 and j<N-3:return 3 if level%2 else 4
  if k in (3,4):return 2
  return 0 if j>2 and j<N-3 else 1
 o=solid_grid('continuous-carbonate-shelf-slope',rows,m,col,idx);o['construction_cross_intervals']=N;o['construction_levels']=levels;o['top_surface_translation_z_m']=shift
 return {'rows':regions,'cross_vertices_per_row':N+1,'pool_floor_z_m':[(levels-1)*rise+.85-l*rise+shift for l in range(levels)],'top_surface_translation_z_m':shift,'xy_envelope_factors':[W/(hi[0]-lo[0]),Ltot/(hi[1]-lo[1])],'primary_lip_nominal_m':lip,'primary_lip_formula':'lip - lip*(.15/.18)*exp(-((t-saddle_center)/.13)^2); side-edge=.20*max(0,(abs(t)-.78)/.22) with .035 irregular term where abs(t)>.83','bottom_z_m':0}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());aid=cfg['asset_id'];out=Path(a.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-region-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])]
 semantics={'spatter-cone':spatter,'travertine-terrace-pools':travertine}[aid](cfg,m,col);bpy.context.view_layer.update()
 export_asset(aid,aid,'terrain',col,metadata={'representation':'geological-form','export_texcoords':False,'source_scope':'Original frozen brief plus prospective measurement-clarification-v002; no source pixels incorporated.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 (out/aid/'construction-semantics.json').write_text(json.dumps(semantics,indent=2)+'\n')
 rec={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(rec,indent=2)+'\n')
if __name__=='__main__':main()
