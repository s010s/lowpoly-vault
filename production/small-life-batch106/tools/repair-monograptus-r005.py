#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded deterministic repair of original Monograptus r004; no other asset regeneration."""
import sys,json,os,datetime,hashlib,argparse
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import export_asset
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('--config',required=True);a.add_argument('--output',required=True);a=a.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());out=Path(a.output);out.mkdir(parents=True,exist_ok=False);start=datetime.datetime.now(datetime.timezone.utc).isoformat();src=ROOT/cfg['repair']['source_path'];assert h(src)==cfg['repair']['source_sha256'];bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False)
 col=next(c for c in bpy.data.collections if c.get('asset_root'));ob=next(o for o in col.all_objects if o.type=='MESH');me=ob.data;assert ob.name=='monograptus-original-tubarium';vg=ob.vertex_groups['nema'];ids=[v.index for v in me.vertices if any(x.group==vg.index for x in v.groups)];assert len(ids)==18
 verts=[tuple(v.co) for v in me.vertices];faces=[tuple(p.vertices) for p in me.polygons];mats=[p.material_index for p in me.polygons];smooth=[p.use_smooth for p in me.polygons];groupnames=[g.name for g in ob.vertex_groups];groups=[[(x.group,x.weight) for x in v.groups] for v in me.vertices];base=ids[:6];plane=verts[base[0]][2];assert all(verts[i][2]==plane for i in base);cap=[i for i,f in enumerate(faces) if set(f)==set(base)];assert len(cap)==1
 # Keep every original vertex and every exposed side polygon unchanged. Move the
 # hidden cap to a new lower ring and connect it to the old ring inside the stipe.
 new=list(range(len(verts),len(verts)+6));depth=cfg['repair']['hidden_base_extension_m'];verts += [(verts[i][0],verts[i][1],verts[i][2]-depth) for i in base];mapping=dict(zip(base,new));oldcap=faces[cap[0]];faces[cap[0]]=tuple(mapping[i] for i in oldcap)
 # Original lower cap is reverse ring order; side orientation follows source.
 for j in range(6):k=(j+1)%6;faces.append((new[j],new[k],base[k],base[j]));mats.append(mats[cap[0]]);smooth.append(False)
 orig_name=me.name;newmesh=bpy.data.meshes.new(orig_name+'-repair');newmesh.from_pydata(verts,[],faces);newmesh.update()
 for m in me.materials:newmesh.materials.append(m)
 for p,mi,sm in zip(newmesh.polygons,mats,smooth):p.material_index=mi;p.use_smooth=sm
 ob.data=newmesh;bpy.data.meshes.remove(me);newmesh.name=orig_name
 ob.vertex_groups.clear()
 for name in groupnames:ob.vertex_groups.new(name=name)
 for i,gs in enumerate(groups):
  for gi,weight in gs:ob.vertex_groups[gi].add([i],weight,'REPLACE')
 ob.vertex_groups['nema'].add(new,1,'REPLACE');bpy.context.view_layer.update()
 record=export_asset('monograptus','monograptus','fossils',col,metadata={'representation':'living-reconstruction','export_texcoords':False,'source_scope':'Type-centered primary-supported skeletal tubarium; color, selected counts and inferred thickness artistic.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 receipt={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':h(__file__),'config_sha256':h(a.config),'original_source_sha256':h(src),'source_unchanged':h(src)==cfg['repair']['source_sha256'],'original_vertex_count':len(groups),'new_vertex_count':len(new),'modified_original_vertices':0,'modified_original_polygons':[cap[0]],'added_side_polygons':6,'original_base_ring_indices':base,'new_base_ring_indices':new,'original_base_plane_local_m':plane,'hidden_extension_m':depth,'note':'Only the old hidden basal cap is relocated; every original source vertex and all original exposed side faces stay unchanged.'};(out/'execution.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':main()
