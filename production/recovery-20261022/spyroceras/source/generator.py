# SPDX-License-Identifier: MIT
"""Original frozen-source Spyroceras fragment loft. All geometry is generated here."""
import argparse,json,pathlib,sys,math,hashlib,datetime
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent/'helpers'))
import bpy
from asset_common import setup_scene,make_material,mesh_object,export_asset

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=pathlib.Path);p.add_argument('--output-dir',required=True,type=pathlib.Path)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);c=json.loads(a.config.read_text());out=a.output_dir
 if out.exists() and any(out.iterdir()):raise RuntimeError('Output must be new empty attempt directory')
 out.mkdir(parents=True,exist_ok=True)
 col=setup_scene(c['asset_id'],c['seed']);N=c['angular_samples']; L=c['length_m']; count=c['annulations']
 centers=[.0013+(i/(count-1))**1.055*.0834+.00017*math.sin(i*1.31)+.00009*math.sin(i*.47) for i in range(count)]
 levels=[(0.0,0.0)]
 for i,z in enumerate(centers):
  spacing=(centers[min(i+1,count-1)]-centers[max(0,i-1)])/ (2 if 0<i<count-1 else 1)
  levels.extend([(z-spacing*.34,0.0),(z,1.0),(z+spacing*.34,0.0)])
 levels.append((.096,0.0));levels.sort()
 vv=[]
 for z,ridge in levels:
  t=z/L;base=.00260+.00276*t+.00034*t*t
  for k in range(N):
   th=2*math.pi*k/N
   long_rib=(.000145 if k%4==0 else .000075 if k%4==2 else 0.0)*(0.8+0.2*t)
   annulus=(.00015+.00019*t)*ridge*(1+.14*math.cos(th*3+z*70))
   radius=(base+long_rib+annulus)*(1+.007*math.cos(3*th+.4)+.003*math.sin(5*th))
   vv.append((radius*math.cos(th),radius*math.sin(th),z))
 ff=[]
 for j in range(len(levels)-1):
  for k in range(N):ff.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
 # Clip continuous surface to one oblique fracture plane. Cache each shared edge.
 slope=c['upper_break_slope_x'];plane=.0845
 def fracture_relief(v):
  th=math.atan2(v[1],v[0]);return .00036*math.cos(3*th+.2)+.00018*math.sin(7*th-.3)
 def d(v):return v[2]-slope*v[0]-plane-fracture_relief(v)
 verts=list(vv);intersections={};faces=[]
 def intersect(i,j):
  key=tuple(sorted((i,j)))
  if key not in intersections:
   x,y=vv[i],vv[j];t=d(x)/(d(x)-d(y));edge=math.sqrt(sum((x[k]-y[k])**2 for k in range(3)))
   if t*edge<.00002:intersections[key]=i
   elif (1-t)*edge<.00002:intersections[key]=j
   else:intersections[key]=len(verts);verts.append(tuple(x[k]+t*(y[k]-x[k]) for k in range(3)))
  return intersections[key]
 for face in ff:
  clipped=[]
  for q,i in enumerate(face):
   j=face[(q+1)%len(face)];di,dj=d(vv[i]),d(vv[j])
   if di<=0:clipped.append(i)
   if (di<=0)!=(dj<=0):clipped.append(intersect(i,j))
  clipped=list(dict.fromkeys(clipped))
  if len(clipped)>=3:faces.append(tuple(clipped))
 top=sorted(set(intersections.values()),key=lambda i:math.atan2(verts[i][1],verts[i][0]));tc=len(verts);verts.append((0.,0.,plane+.00024));cap_start=len(faces)
 for i,k in enumerate(top):faces.append((k,top[(i+1)%len(top)],tc))
 bc=len(verts);verts.append((0.,0.,0.))
 for k in range(N):faces.append(((k+1)%N,k,bc))
 used=sorted({i for f in faces for i in f});remap={old:new for new,old in enumerate(used)};verts=[verts[i] for i in used];faces=[tuple(remap[i] for i in f) for f in faces]
 maxz=max(v[2] for v in verts);extent_factor=L/maxz;verts=[(x,y,z*extent_factor) for x,y,z in verts]
 mats=[make_material('fossil-mineral',c['palette']['mineral'],.93),make_material('fractured-mineral',c['palette']['fracture'],.96)]
 obj=mesh_object('preserved-phragmocone-fragment',verts,faces,mats,col)
 for i,p in enumerate(obj.data.polygons):p.material_index=1 if i>=cap_start else 0
 obj['claim_scope']='Incomplete fossil fragment only; no apex/aperture/body chamber/soft body';obj['source_specimen']='UMUT PM18493';obj['construction']='single continuous clipped radial loft with closed inferred mineral break faces';obj['geometry_rib_count']=32
 metadata={'revision':c['revision'],'generator':'source/build_spyroceras_v003.py','config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest(),'description':{'en':'Evidence-informed incomplete phragmocone fragment, Spyroceras melolineatum holotype UMUT PM18493. Rear and closed mineral fracture faces inferred. Nominal 89mm preserved length is conditional print-scale estimate (at least ±15% uncertainty), not exact specimen measurement.','zh':'据文献制作的不完整气室壳残片；背面与矿化断面推定，89毫米为至少±15%不确定性的条件印刷比例估计。'},'claim_scope':'Stylized external fossil fragment; no restored aperture, apex or full animal.','sources':[{'id':'Niko1996-Fig5.5','figure':'p354 Fig5.5','url':'https://doi.org/10.14825/prpsj1951.1996.181_347'}],'scale_uncertainty':'at least ±15% conditional print calibration','origin':'narrow preserved cut center; upright museum mount, not life orientation'}
 record=export_asset(c['asset_id'],{'en':'Spyroceras fossil fragment','zh':'Spyroceras 气室壳残片'},'cephalopods',col,metadata=metadata,output_root=out,render=False,max_triangles=c['budgets']['max_triangles'],max_materials=c['budgets']['max_materials'],max_primitives=c['budgets']['max_primitives'])
 assert record['glb_bytes']<=c['budgets']['max_glb_bytes']
 (out/'build-receipt.json').write_text(json.dumps({'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest(),'collection':'EXPORT','root':c['asset_id'],'mesh_objects':['preserved-phragmocone-fragment'],'raw_levels':len(levels),'annulations':count,'angular_samples':N,'clipped_fracture_vertices':len(top),'artifact':record},indent=2)+'\n')
if __name__=='__main__':main()
