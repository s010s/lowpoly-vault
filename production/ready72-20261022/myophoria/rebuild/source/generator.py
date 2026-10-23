# SPDX-License-Identifier: MIT
"""Original Myophoria fossil form. Rebuild: blender -b -t 2 --python generator.py -- --params params.json --output-root OUT
Artwork: CC-BY-4.0, Leon Made This / s010s. Reference DOI10.1007/s41513-025-00309-6 Fig5g-i.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
S=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'deps'))
import bpy, bmesh
from asset_common import setup_scene, make_material, mesh_object, export_asset
from qa_glb import audit_glb

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def delta(a,b):return (a-b+math.pi)%(2*math.pi)-math.pi
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--params',type=Path,required=True);ap.add_argument('--output-root',type=Path,required=True)
 a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);p=json.loads(a.params.read_text());out=a.output_root.resolve();out.mkdir(parents=True,exist_ok=True)
 c=setup_scene(p['asset_id'],p['seed']);scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
 scene['revision']=p['revision'];scene['claim_scope']='Original Myophoria fossil form; not a scanned or catalog-exact replica'
 mats=[make_material(k,v,roughness=.91) for k,v in p['palette'].items()]
 outline=p['outline_xz_mm'];center=p['umbo_center_mm'];mainangle=math.atan2(p['main_carina_endpoint_mm'][1]-center[1],p['main_carina_endpoint_mm'][0]-center[0]);second=math.atan2(p['secondary_ridge_endpoint_mm'][1]-center[1],p['secondary_ridge_endpoint_mm'][0]-center[0])
 special=[math.atan2(z-center[1],x-center[0]) for x,z in outline]
 special += [mainangle+x for x in (-.23,-.10,0,.10,.23)] + [second+x for x in (-.16,0,.16)]
 angles=[]
 for v in sorted((x+math.pi)%(2*math.pi)-math.pi for x in special):
  if not angles or abs(v-angles[-1])>.018:angles.append(v)
 for i in range(p['base_angular_samples']):
  v=-math.pi+2*math.pi*i/p['base_angular_samples']
  if min(abs(delta(v,u)) for u in angles)>.045:angles.append(v)
 angles.sort();N=len(angles)
 def boundary(th):
  d=(math.cos(th),math.sin(th));ts=[]
  for i,A in enumerate(outline):
   B=outline[(i+1)%len(outline)];E=(B[0]-A[0],B[1]-A[1]);Q=(A[0]-center[0],A[1]-center[1]);den=cross(d,E)
   if abs(den)<1e-12:continue
   t=cross(Q,E)/den;u=cross(Q,d)/den
   if t>0 and -1e-8<=u<=1+1e-8:ts.append(t)
  assert ts,(th,d)
  t=min(ts);return (center[0]+t*d[0],center[1]+t*d[1])
 edge=[boundary(th) for th in angles]
 vs=[];faces=[];mids=[];valve_groups={};carina_vertices=[];secondary_vertices=[]
 # The perimeter is shared by the two valve surfaces, yielding a single watertight exterior.
 perimeter=[]
 for x,z in edge:perimeter.append(len(vs));vs.append((x,0,z))
 for sign,name in [(-1,'Left_valve_negativeY'),(1,'Right_valve_positiveY')]:
  center_depth=6.5*(p['inferior_depth_taper']['floor']+(1-p['inferior_depth_taper']['floor'])*(center[1]/31)**p['inferior_depth_taper']['power'])
  centeridx=len(vs);vs.append((center[0],sign*center_depth,center[1]));rings=[];group=[centeridx]
  for r in p['radial_rings'][:-1]:
   ring=[]
   for j,(x,z) in enumerate(edge):
    th=angles[j];peak=max(0,1-abs(delta(th,mainangle))/p['main_ridge_width_radians']);weak=max(0,1-abs(delta(th,second))/p['secondary_ridge_width_radians'])
    envelope=max(0,1-r*r)**.55
    relief=(p['primary_relief_mm']*peak+p['secondary_relief_mm']*weak)*r*math.sqrt(1-r)
    # A broad, quieter posterior field is lower than the continuous main carina.
    posterior=.55*math.exp(-(delta(th,mainangle+.36)/.23)**2)*r*math.sqrt(1-r)
    depth=6.5*envelope+relief-posterior
    # Very faint concentric undulation: artistic internal-cast simplification, not ornate ribs.
    depth+=.07*math.sin(6*math.pi*r)*r*(1-r)
    projected_z=center[1]+r*(z-center[1])
    depth*=p['inferior_depth_taper']['floor']+(1-p['inferior_depth_taper']['floor'])*(max(0,projected_z)/31)**p['inferior_depth_taper']['power']
    idx=len(vs);vs.append((center[0]+r*(x-center[0]),sign*depth,center[1]+r*(z-center[1])));ring.append(idx);group.append(idx)
    if abs(delta(th,mainangle))<.025:carina_vertices.append(idx)
    if abs(delta(th,second))<.025:secondary_vertices.append(idx)
   rings.append(ring)
  rings.append(perimeter);group+=perimeter;valve_groups[name]=group
  def mat_for(j,r):
   th=angles[j]
   if r>.999:return 3
   if mainangle+.13<th<.35:return 2
   if .23<r<.82 and th<mainangle-.2:return 1
   return 0
  for j in range(N):faces.append((centeridx,rings[0][j],rings[0][(j+1)%N]));mids.append(mat_for(j,.07))
  for k in range(len(rings)-1):
   rmean=(p['radial_rings'][k]+p['radial_rings'][k+1])/2
   for j in range(N):
    q=(j+1)%N;faces.append((rings[k][j],rings[k+1][j],rings[k+1][q],rings[k][q]));mids.append(mat_for(j,rmean))
 lo=[min(v[k] for v in vs) for k in range(3)];hi=[max(v[k] for v in vs) for k in range(3)];dims=p['dimensions_mm']
 # Preserve measured projection ratios, with the explicitly inferred full inflation.
 vs=[((v[0]-(lo[0]+hi[0])/2)*dims[0]/(hi[0]-lo[0])/1000,(v[1]-(lo[1]+hi[1])/2)*dims[1]/(hi[1]-lo[1])/1000,(v[2]-lo[2])*dims[2]/(hi[2]-lo[2])/1000) for v in vs]
 obj=mesh_object('Myophoria_closed_cast_envelope',vs,faces,mats,c)
 for f,mi in zip(obj.data.polygons,mids):f.material_index=mi
 for name,ids in {**valve_groups,'Primary_oblique_carina':carina_vertices,'Secondary_weak_ridge':secondary_vertices,'Closed_commissure':perimeter}.items():obj.vertex_groups.new(name=name).add(ids,1,'REPLACE')
 obj['anatomy']='two valve exterior surfaces joined at shared closed perimeter; no hidden internal shell faces'
 obj['relief']='one primary continuous oblique carina and one weaker secondary direction'
 obj['surface_scope']='internal-cast-inspired muted ornament; palette is artistic'
 # Embed editable generator and parameter text without executable auto-run.
 for path in [Path(__file__),a.params]:bpy.data.texts.load(str(path))
 bm=bmesh.new();bm.from_mesh(obj.data);volume=bm.calc_volume(signed=True);boundary_count=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free()
 if volume<=0 or boundary_count or nonmanifold:raise RuntimeError('Closed exterior topology invalid')
 metadata={'revision':p['revision'],'generator':'source/generator.py','generator_sha256':sha(__file__),'params_sha256':sha(a.params),'description':{'en':'Original compact triangular Myophoria fossil form with a continuous oblique carina and subdued secondary ridge.','zh':'原创 Myophoria 紧凑三角双壳化石形态，保留连续强斜脊及较弱次脊。'},'sources':[{'doi':'10.1007/s41513-025-00309-6','figure':'5g-i','license':'CC-BY-4.0'}],'reconstruction_notes':json.loads((S.parent/'brief.json').read_text()),'threejs_target_version':'0.180.0','measured_scale_evidence':'evidence/scale-measurement.json'}
 record=export_asset(p['asset_id'],{'en':'Myophoria triangular ridged bivalve','zh':'Myophoria（三角脊双壳类）'},'animals',c,metadata=metadata,output_root=out,render=False,max_triangles=p['max_triangles'],max_materials=p['max_materials'],max_primitives=p['max_primitives'])
 target=out/p['asset_id'];audit=audit_glb(target/'myophoria.glb',p['max_triangles'],p['max_materials'],p['max_primitives'])
 receipt={'status':'succeeded','blender_version':bpy.app.version_string,'generator_sha256':sha(__file__),'params_sha256':sha(a.params),'helper_sha256':sha(S/'deps/asset_common.py'),'audit_helper_sha256':sha(S/'deps/qa_glb.py'),'glb_sha256':sha(target/'myophoria.glb'),'blend_sha256':sha(target/'myophoria.blend'),'semantic_sha256':audit['semantic_sha256'],'geometry':{'vertices':len(vs),'source_polygons':len(faces),'triangles':audit['scene_triangles'],'angular_samples':N,'radial_rings':len(p['radial_rings']),'source_boundary_edges':boundary_count,'source_nonmanifold_edges':nonmanifold,'signed_volume_m3':volume,'surface_components':1},'gpu_status':'unknown; Cycles CPU only','preview_helpers_saved':False}
 (target/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
