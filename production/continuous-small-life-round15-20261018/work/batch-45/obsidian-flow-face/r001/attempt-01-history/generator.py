# SPDX-License-Identifier: MIT
"""Original deterministic batch45 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # A substantial exposed flow face, not an isolated polished nodule.
 rock=Part('one-continuous-banded-volcanic-glass-face',m);v=[];f=[];mi=[];nx=55
 levels=[0,.015,.03,.047,.063,.080,.088,.096,.113,.130,.147,.164,.172,.180,.197,.214,.231,.248,.256,.264,.281,.298,.315,.332,.340,.348,.365,.382,.399,.416,.432,.448,.46];ny=len(levels)
 for side in range(2):
  for j,zz in enumerate(levels):
   t=zz/.46
   for i in range(nx):
    u=i/(nx-1);x=(-.35+.70*u)*(1-.11*abs(2*t-1)**3);z=zz+.020*math.sin(7*x+3*t)*math.sin(pi*t)+.009*math.sin(13*x+.7)*t**6
    if side==0:
     y=-.105+.009*math.sin(11*x+2*z)
     for cx,cz,rx,rz,dep in [(-.14,.27,.215,.185,.064),(.16,.205,.205,.177,.055)]:
      rr=((x-cx)/rx)**2+((z-cz)/rz)**2
      if rr<1:y+=dep*(1-rr)**1.42+.0025*math.sin(math.sqrt(rr+.0001)*18)*(1-rr)**.65
     # Flow relief is integral and subordinate to broad curving fracture scars.
     y+=.0016*math.sin(2*pi*zz/.084)
    else:y=.112+.009*math.sin(9*x+5*z)+.007*math.cos(z*14)
    v.append((x,y,z))
 off=nx*ny
 for side in range(2):
  for j in range(ny-1):
   for i in range(nx-1):
    a=side*off+j*nx+i;ids=(a,a+1,a+nx+1,a+nx);f.append(ids if side==0 else tuple(reversed(ids)));mi.append((1 if j in [5,6,11,12,17,18,23,24] else 0) if side==0 else 2)
 per=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+[(ny-1)*nx+i for i in range(nx-2,-1,-1)]+[j*nx for j in range(ny-2,0,-1)]
 for k,a in enumerate(per):b=per[(k+1)%len(per)];f.append((a,a+off,b+off,b));mi.append(2)
 rock.add(v,f,mi);o=rock.finish(c,True);span=max(p.co.x for p in o.data.vertices)-min(p.co.x for p in o.data.vertices)
 for p in o.data.vertices:p.co*=.7/span
 for material in m:
  bs=material.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.52;bs.inputs['Metallic'].default_value=0
 return {'nominal_flow_face_width_m':.7,'geological_scope':'one original substantial volcanic-glass exposure with gently curved flow bands continuing over two broad concave conchoidal fracture surfaces','surface_note':'Muted opaque nonmetallic glass, roughness0.52; no transparency or mirror trick. Flow-band count/layout and fracture curvature are artistic diagnostic geometry, not a sampled site, dated stratum or conchoidal biological shell.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='obsidian-flow-face');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='obsidian-flow-face';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#303A42', '#4B5356', '#3B4145'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original volcanic-glass flow exposure teaching concept','habitat_zh':'原创火山玻璃流露面教学概念','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'A substantial original exposure combines gently sinuous flow bands and broad curving conchoidal break surfaces. Dark nonmetallic opaque palette, moderate roughness and conservative integral relief; no enlarged flint nodule, polished scoria, shell organism or exact locality.','zh':'原创厚实露面结合柔和流带与宽曲面贝壳状断口，采用不透明非金属暗色、适中粗糙度和真实几何浅起伏；不是放大燧石结核、抛光火山渣或贝壳生物，不声称具体地点。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Obsidian flow face','zh':'黑曜岩流面'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH45_COMPLETE',s)
if __name__=='__main__':main()
