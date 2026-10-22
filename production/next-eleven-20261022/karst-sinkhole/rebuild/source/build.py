# SPDX-License-Identifier: MIT
"""New karst-sinkhole recovery-r001. Blender -b -t 2 --python build.py -- --output DIR.
Original prepared-but-unbuilt geometry is retained separately, never relabeled.
"""
import sys
sys.dont_write_bytecode=True
import bpy,bmesh,math,json,hashlib,argparse
from pathlib import Path
S=Path(__file__).resolve().parent;sys.path.insert(0,str(S/'helpers'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
C=json.loads((S/'config.json').read_text());P=C['geometry_parameters'];N=P['azimuth_segments']
def position(r,z,t):
 # Low-frequency, organized asymmetry, attenuated at the shared cut plane.
 # Outside transitions to a softly squared terrain footprint, not concentric pipes.
 a=P['angular_asymmetry']*(math.sin(3*t)+.35*math.sin(5*t))
 sq=max(0,(r-1.6)/1.4)
 ct=math.cos(t);st=math.sin(t)
 def sp(v):return math.copysign(abs(v)**.72,v)
 x=r*((1-sq)*ct+sq*sp(ct))*(1+a*(1-sq))
 y=r*((1-sq)*st+sq*sp(st))*(1+a*(1-sq))
 dz=P['surface_warp_m']*math.sin(2*t+.3)*math.sin(t)*min(1,max(0,(z-2.04)/1.2))
 # The opening is slightly off-round and the relief has a quiet natural bias.
 return (x,y,z+dz)
def make_geometry(col,mats):
 vertices=[];faces=[];indices=[]
 def add_profile(profile,angles,full,omit_edge=None):
  rows=[]
  for r,z in profile:
   row=[]
   for t in angles:row.append(len(vertices));vertices.append(position(r,z,t))
   rows.append(row)
  for j in range(len(profile)):
   jj=(j+1)%len(profile)
   for k in range(len(angles) if full else len(angles)-1):
    if omit_edge is not None and omit_edge(j,k):continue
    kk=(k+1)%len(angles)
    f=(rows[j][k],rows[j][kk],rows[jj][kk],rows[jj][k])
    faces.append(f)
    indices.append(0 if full and j<2 else 1 if full and j==2 else 2)
  if not full:
   faces.append(tuple(row[0] for row in rows));indices.append(2)
   faces.append(tuple(row[-1] for row in reversed(rows)));indices.append(2)
  return rows
 # k=0..31 is rear +Y. Remove its planar contact band from upper ring.
 add_profile(P['upper_profile'],[2*math.pi*k/N for k in range(N)],True,lambda j,k:j==8 and k<N//2)
 # Lower rear half has no top contact faces. Both contours share exact vertices.
 add_profile(P['lower_profile'],[2*math.pi*k/N for k in range(N//2+1)],False,lambda j,k:j==0)
 mesh=bpy.data.meshes.new('continuous-cutaway-solid-mesh');mesh.from_pydata(vertices,[],faces);mesh.update()
 bm=bmesh.new();bm.from_mesh(mesh)
 for f,i in zip(bm.faces,indices):f.material_index=i
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-9)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
 ob=bpy.data.objects.new('single-solid-enclosed-funnel-throat-and-cavity-cutaway',mesh);col.objects.link(ob);ob.parent=bpy.data.objects['karst-sinkhole']
 for m in mats:mesh.materials.append(m)
 for p in mesh.polygons:p.use_smooth=False
 ob['semantic_role']='Complete surface rim descends through an open throat into enlarged underground cavity; artificial front subsurface section only.'
 ob['solid_design']='One connected watertight rock volume, no interior contact faces and no separate painted void.'
 ob['cutaway']='Front underground half is intentionally omitted; all exposed rock cut faces are closed.'
 return ob

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
 col=setup_scene('karst-sinkhole',C['seed']);mats=[make_material(n,v,roughness=.93) for n,v in C['palette']];make_geometry(col,mats)
 brief=json.loads((S/'brief.json').read_text());refs=json.loads((S/'references.json').read_text())
 md={'revision':'recovery-r001','original_source_commit':'ac3f227a162f4cd413e918ad1f064ba6544a4081','original_geometry_restored':False,'generator':'source/build.py','config_sha256':hashlib.sha256((S/'config.json').read_bytes()).hexdigest(),'description':{'en':'Original stylized karst sinkhole teaching cutaway: an enclosed surface funnel narrows into a real open throat and an enlarged underground cavity. The artificial front subsurface section reveals rock thickness and the connection without opening the surface rim. Nominal 6 m tile, dimensions, low cover, palette and exposed section are artistic choices, not measured site, dated event, collapse sequence or hydrology. No water.','zh':'原创风格化喀斯特落水洞教学剖面：闭合周缘地表真实下凹，经窄喉连接扩大的地下空腔。人工前侧地下剖切展示岩壁厚度和空腔连接，同时保持地表漏斗周缘闭合。名义6米裁片、各部尺寸、低矮覆盖、配色及展示剖面均为美术选择，不代表实测地点、年代事件、塌陷过程或水文。无水。'},'nominal_scale':C['nominal_scale'],'sources':refs['sources'],'reference_visual_access':refs['recovery_visual_access'],'claim_scope':brief['claim_scope'],'provenance':{'geometry':'Original procedural geometry by Leon Made This / s010s, new recovery-r001','third_party_assets_incorporated':False},'representation':'geological-form','reconstruction_type':'artistic-concept','publication_authority':'separate_not_authorized','approved':False,'productionAccepted':'pending_fresh_independent_QA','animation_ready':False,'catalog_facets':brief['catalog_facets'],'topology_design':'Single closed solid rock volume around physical open air cavity. Cutaway is pedagogical, not a natural cave entrance.'}
 export_asset('karst-sinkhole',{'en':'Stylized Karst sinkhole','zh':'风格化喀斯特落水洞'},'terrain',col,metadata=md,output_root=args.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
if __name__=='__main__':main()
