#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Cucullaea fossil-form, concentric growth surface over an asymmetric rounded quadrangular margin."""
import argparse,hashlib,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy
from asset_common import setup_scene,make_material,mesh_object,ground_asset,export_asset

def bezier(a,b,c,d,t):
 s=1-t;return (s*s*s*a[0]+3*s*s*t*b[0]+3*s*t*t*c[0]+t*t*t*d[0],s*s*s*a[1]+3*s*s*t*b[1]+3*s*t*t*c[1]+t*t*t*d[1])
def main():
 argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
 ap=argparse.ArgumentParser();ap.add_argument('--config',type=Path,required=True);ap.add_argument('--output-root',type=Path,required=True);a=ap.parse_args(argv)
 p=json.loads(a.config.read_text());assert bpy.app.version_string==p['blender_version']
 col=setup_scene('cucullaea',p['seed'])
 mats=[make_material(n,c,roughness=.94) for n,c in zip(['Neutral fossil shell','Quiet growth faces','Worn shell planes','Closed commissural recess'],p['palette_srgb'])]
 boundary=[]
 for seg in p['outline_beziers_mm']:
  for j in range(seg[4]):boundary.append(bezier(*seg[:4],j/seg[4]))
 n=len(boundary);rings=p['radial_rings'];verts=[];faces=[];face_mats=[];groups={}
 cx,cz=p['umbo_planar_center_mm'];surf_index={}
 for label,sign in [('right_valve',-1),('left_valve',1)]:
  groups[label]=[];surf_index[label]=[]
  for r in rings:
   row=[]
   for j,(bx,bz) in enumerate(boundary):
    dorsal=max(0,min(1,(bz-22)/8.8))**3*math.exp(-((bx-5)/9.8)**2)
    outer_z=bz+p['umbo_rise_mm']*dorsal
    x=cx+r*(bx-cx);z=cz+r*(outer_z-cz)
    edge_y=p['rim_half_gap_mm']+p['umbo_half_separation_mm']*dorsal
    y=p['inflation_mm']*max(0,1-r*r)**.63+edge_y*r**3
    wave=math.sin(2*math.pi*(r-.12)/.085)
    relief=p['growth_relief_mm']*wave*math.sin(math.pi*r)**.7
    y+=relief
    if sign>0:y*=p['left_inflation_ratio']
    row.append(len(verts));groups[label].append(len(verts));verts.append((x*.001,sign*y*.001,z*.001))
   surf_index[label].append(row)
  pole=len(verts);groups[label].append(pole);verts.append((cx*.001,sign*p['inflation_mm']*.001,cz*.001))
  for j in range(n):faces.append((pole,surf_index[label][0][j],surf_index[label][0][(j+1)%n]));face_mats.append(0)
  for k in range(len(rings)-1):
   for j in range(n):
    faces.append((surf_index[label][k][j],surf_index[label][k+1][j],surf_index[label][k+1][(j+1)%n],surf_index[label][k][(j+1)%n]))
    # Adjacent, muted mineral-tonal planes are deliberate; no random biological spotting.
    mi=0
    face_mats.append(mi)
  groups[label+'_umbo']=[i for row in surf_index[label] for i in row if verts[i][2]>.0285 and -.005<verts[i][0]<.016]
 # A rounded dorsal bridge returns the two umbo shoulders to one long near-straight hinge.
 bridge_rows={}
 for label,sign in [('right_valve',-1),('left_valve',1)]:
  bridge_rows[label]=[surf_index[label][-1]]
  for t in (.33,.67):
   row=[]
   for bx,bz in boundary:
    dorsal=max(0,min(1,(bz-22)/8.8))**3*math.exp(-((bx-5)/9.8)**2)
    y=(p['rim_half_gap_mm']+p['umbo_half_separation_mm']*dorsal)*(1-t)
    if sign>0:y*=p['left_inflation_ratio']
    z=bz+p['umbo_rise_mm']*dorsal*math.cos(t*math.pi/2)
    row.append(len(verts));groups[label].append(len(verts));verts.append((bx*.001,sign*y*.001,z*.001))
   bridge_rows[label].append(row)
 groove=[]
 for bx,bz in boundary:
  dx,dz=bx-cx,bz-cz;length=math.hypot(dx,dz)
  groove.append(len(verts));verts.append(((bx-.09*dx/length)*.001,0,(bz-.09*dz/length)*.001))
 groups['continuous_closed_commissure']=groove
 for label,rows in bridge_rows.items():
  rows.append(groove)
  for k in range(len(rows)-1):
   for j in range(n):
    faces.append((rows[k][j],rows[k+1][j],rows[k+1][(j+1)%n],rows[k][(j+1)%n]));face_mats.append(3 if k==2 else 0)
 # Scale X to the sole nominal source-anchored dimension. Other axes remain explicitly inferred.
 xmin=min(v[0] for v in verts);xmax=max(v[0] for v in verts);scale=p['nominal_side_length_m']/(xmax-xmin)
 verts=[(x*scale,y,z) for x,y,z in verts]
 obj=mesh_object('Articulated deep valves and closed commissure',verts,faces,mats,col)
 for f,mi in zip(obj.data.polygons,face_mats):f.material_index=mi
 for name,ids in groups.items():
  if ids:obj.vertex_groups.new(name=name).add(ids,1,'REPLACE')
 obj['construction']='One manifold exterior with two deep semantic valve surfaces and paired umbones, connected by a narrow recessed closed seam. Not mechanically separable hollow valves.'
 obj['claim_scope']=p['claim_scope'];obj['teeth']='No unseen hinge teeth or internal anatomy reconstructed.'
 ground_asset(col,center_xy=True)
 # Keep generator/config as editable text blocks as well as portable external sources.
 for name,body in [('generate.py',Path(__file__).read_text()),('params.json',a.config.read_text())]:bpy.data.texts.new(name).write(body)
 rec=export_asset('cucullaea',{'en':'Cucullaea fossil bivalve','zh':'Cucullaea 双壳类化石'},'animals',col,metadata={'description':{'en':'Original deep, rounded quadrangular closed fossil shell informed by photographed Cucullaea (Idonearca) vulgaris.','zh':'依据 Cucullaea（Idonearca）vulgaris 实物照片制作的深鼓、圆角四边形闭合双壳原创模型。'},'generator':'source/generate.py','revision':p['revision'],'scientific_scope':p['claim_scope'],'scale_note':'Maximum side length 0.049 m is an artistic anchor to S1. Height, depth and cross-view interpolation are inferred. S2 is a different 0.032 m-wide photographed specimen; its dimension is not model depth.','orientation_note':'Blender X anterior-posterior long axis, +X anterior; Y valve depth, -Y shows right valve exterior; +Z dorsal. Ground origin is a presentation pose, not life position.','reconstruction_notes':['Historical Cucullaea (Idonearca) vulgaris photo identification preserved; not taxonomic adjudication.','Continuous manifold closed exterior is not two separable hollow shells.','Hidden ventral closure, inflation, beak transition and palette are artistic interpolation.','No original color claim or photographic texture. No unseen teeth or interior anatomy.'],'sources':[{'id':'S1','title':'James St. John, right-valve specimen, 4.9 cm wide','url':'https://www.flickr.com/photos/jsjgeology/31971664065/'},{'id':'S2','title':'James St. John, articulated hinge-view specimen, 3.2 cm across','url':'https://www.flickr.com/photos/jsjgeology/31971646985/'}]},output_root=a.output_root,render=False,max_triangles=p['budget']['max_triangles'],max_materials=4,max_primitives=4)
 metrics={'boundary_vertices':n,'radial_rings':len(rings),'dimensions_blender_m':rec['blender_dimensions_m'],'triangles':rec['triangles'],'glb_bytes':rec['glb_bytes'],'glb_sha256':rec['sha256']['glb'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()}
 (a.output_root/'build-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics))
if __name__=='__main__':main()
