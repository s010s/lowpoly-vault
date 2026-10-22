# SPDX-License-Identifier: MIT
"""New recovery-r001 geometry. Original prepared build was never run.
Run: blender -b -t 2 --python build.py -- --output /absolute/output-parent
The output parent receives fault-scarp/. No network or repository writes.
"""
import bpy, bmesh, math, json, sys, argparse, hashlib
from pathlib import Path
SRC=Path(__file__).resolve().parent
sys.path.insert(0,str(SRC/'helpers'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
CFG=json.loads((SRC/'config.json').read_text())
P=CFG['geometry_parameters']
S=[0,.035,.09,.18,.32,.50,.70,.86,1.0]
T=[0,.11,.25,.39,.47,.515,.55,.585,.63,.73,.86,1.0]

def plane(z):return P['fault_plane_x0']+P['fault_plane_dx_dz']*z

def xrange(side,s,z):
 f=plane(z)
 return -4+(f+4)*s if side==0 else f+(4-f)*s

def perimeter_y(x,t,inset=0):
 front=-2.84+.105*math.sin(.73*x)+.045*math.cos(1.8*x)
 back=2.84+.12*math.sin(.61*x+.9)-.04*math.cos(1.4*x)
 return front+inset+(back-front-2*inset)*t

def ztop(side,x,y,s):
 channel=.34+.12*math.sin(.8*x)
 z=P['top_low']+side*P['offset']+.065*math.sin(.63*x)+.055*math.cos(.65*y)
 z-=P['channel_depth']*math.exp(-((y-channel)/P['channel_width'])**2)
 if side==1:z-=.13*math.exp(-(s/.09)**2)
 return z

def toppoint(side,s,t):
 z=P['top_low']+side*P['offset']
 for _ in range(18):
  x=xrange(side,s,z);y=perimeter_y(x,t);z=ztop(side,x,y,s)
 x=xrange(side,s,z);y=perimeter_y(x,t)
 return (x,y,z)

def ringpoint(side,s,t,level,inset):
 # Bedding undulation is shared before displacement. Low-amplitude, not noise.
 z=level
 for _ in range(18):
  x=xrange(side,s,z);y=perimeter_y(x,t,inset)
  z=level+(.022*math.sin(.55*x)+.013*math.cos(.8*y) if level>0 else 0)
 return (xrange(side,s,z),perimeter_y(xrange(side,s,z),t,inset),z)

def build_block(side,col,mats):
 n=len(S);m=len(T);verts=[];faces=[];mi=[]
 for t in T:
  for s in S:verts.append(toppoint(side,s,t))
 # Alternating diagonal tracks the channel's broad top planes.
 for j in range(m-1):
  for i in range(n-1):
   a=j*n+i;b=a+1;c=a+n+1;d=a+n
   faces.extend([(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)]);mi.extend([0,0])
 edge=list(range(n))+[j*n+n-1 for j in range(1,m)]+[(m-1)*n+i for i in range(n-2,-1,-1)]+[j*n for j in range(m-2,0,-1)]
 params=[(S[k%n],T[k//n]) for k in edge]
 shift=side*P['offset']
 # Ring depths form two shallow genuine grooves in the artificial cut faces.
 levels=[(0,0),(.43+shift,0),(.60+shift,0),(.64+shift,P['bedding_relief']),(.68+shift,0),(1.02+shift,0),(1.06+shift,P['bedding_relief']),(1.10+shift,0)]
 rows=[]
 for z,ins in levels:
  row=[]
  for s,t in params:
   row.append(len(verts));verts.append(ringpoint(side,s,t,z,ins))
  rows.append(row)
 rows.append(edge)
 for j in range(len(rows)-1):
  lower,upper=rows[j],rows[j+1]
  # Three comparable regions. Colors are subordinate to geometric relief.
  mat=3 if j<2 else 2 if j<6 else 1
  for k in range(len(edge)):
   kk=(k+1)%len(edge);faces.append((lower[k],lower[kk],upper[kk],upper[k]));mi.append(mat)
 # Fan triangulates a flat bottom safely, with one grounded pivot.
 ctr=len(verts);verts.append(tuple(sum(verts[k][i] for k in rows[0])/len(rows[0]) for i in range(3)))
 for k in range(len(edge)):
  faces.append((ctr,rows[0][(k+1)%len(edge)],rows[0][k]));mi.append(3)
 name='hanging-wall-downthrown-continuous-terrain' if side==0 else 'footwall-high-ground-and-weathered-scarp'
 obj=mesh_object(name,verts,faces,mats,col)
 for p,idx in zip(obj.data.polygons,mi):p.material_index=idx;p.use_smooth=False
 obj['semantic_role']='downthrown ground and displaced matching strata' if side==0 else 'high ground, exposed single fault scarp and matching strata'
 obj['contact_plane']='x = -1.1 + 0.5 z; deliberately shared internal contact surface only'
 obj['nominal_displacement_art_direction_m']=P['offset']
 return obj

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);a=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
 col=setup_scene('fault-scarp',CFG['seed'])
 mats=[make_material(n,c,roughness=.9) for n,c in CFG['palette']]
 for side in [0,1]:build_block(side,col,mats)
 refs=json.loads((SRC/'references.json').read_text());brief=json.loads((SRC/'brief.json').read_text())
 md={'revision':'recovery-r001','original_source_commit':'833333e97c9525d61bc06796980d38d18dfe2a92','original_geometry_restored':False,'generator':'source/build.py','build_config_sha256':hashlib.sha256((SRC/'config.json').read_bytes()).hexdigest(),'description':{'en':'Original stylized normal-fault teaching crop: one continuous scarp separates matching high and low ground, corresponding displaced sediment bands and a shallow channel. A rounded shoulder and real cut-face bedding relief remain visible in clay. Nominal 8 m width, 1.1 m model offset, palette, crop and weathering are artistic choices, not measured site or earthquake data.','zh':'原创风格化正断层教学裁片：一处连续断层崖连接高低地面，对应沉积层和浅槽发生错移；灰模可见圆化崖肩与实体层理浅凹。名义8米宽、模型1.1米高差、配色、裁面及风化均为美术选择，不是实测地点或地震数据。'},'nominal_scale':CFG['nominal_scale'],'claim_scope':brief['claim_scope'],'sources':refs['sources'],'reference_visual_access':refs['recovery_visual_access'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s; new recovery revision','third_party_assets_incorporated':False},'representation':'geological-form','reconstruction_type':'artistic-concept','publication_authority':'separate_not_authorized','animation_ready':False,'approved':False,'productionAccepted':'pending_fresh_independent_QA','catalog_facets':brief['catalog_facets'],'contact_design':'Two individually closed terrain volumes meet on one inclined fault plane. Opposite internal contact faces are intentional; no gap and no overlapping interior volumes.'}
 export_asset('fault-scarp',{'en':'Stylized Fault scarp','zh':'风格化断层崖'},'terrain',col,metadata=md,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
if __name__=='__main__':main()
