#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon Made This / s010s
"""Bounded batch108 repair. Reopen the immutable authored r002 scene, extend only
four lower vertices on each independently proven detached plate toward its core.
No upper vertex, face, material, semantic group, transform or other object changes.
"""
import argparse,datetime,hashlib,json,os,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'scripts'))
from asset_common import export_asset
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(o):
 return dict(vertices=[list(v.co) for v in o.data.vertices],faces=[list(p.vertices) for p in o.data.polygons],material_indices=[p.material_index for p in o.data.polygons],materials=[m.name for m in o.data.materials],matrix=[list(x) for x in o.matrix_world],groups=[(g.name,[(v.index,z.weight) for v in o.data.vertices for z in v.groups if z.group==g.index]) for g in o.vertex_groups])
def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());aid=cfg['asset_id'];out=Path(a.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();source=R/'production/batch-108'/aid/'r002/artifacts'/f'{aid}.blend';assert h(source)==cfg['connection_repair']['original_source_sha256']
 bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False);ctext=bpy.data.texts['BATCH108_COMPONENT_CONTRACT.json'].as_string();ct=json.loads(ctext);o=bpy.data.objects[ct['object_name']];bpy.context.view_layer.update();before=snapshot(o);o.data.calc_loop_triangles();V=[v.co.copy() for v in o.data.vertices];T=[tuple(t.vertices) for t in o.data.loop_triangles];core=set(next(c for c in ct['components'] if c['tag']=='theca')['vertices']);coretree=BVHTree.FromPolygons(V,[t for t in T if all(i in core for i in t)],all_triangles=True);extent=max(max(v[k] for v in V)-min(v[k] for v in V) for k in range(3));margin=extent*2**-17;records=[]
 np.savez_compressed(out/'before.npz',vertices=np.array(before['vertices'],dtype=np.float64),triangles=np.array(T,dtype=np.int32))
 for rec in cfg['connection_repair']['affected_solids']:
  ids=rec['source_vertex_indices'];assert len(ids)==8 and ids==list(range(ids[0],ids[0]+8));low=ids[:4];upper=ids[4:];direction=sum((V[i]-V[j] for i,j in zip(low,upper)),Vector()).normalized();bottom=[t for t in T if all(i in low for i in t)];assert len(bottom)==2;hits=[]
  for t in bottom:
   q=sum((V[i] for i in t),Vector())/3;hit,n,fi,dist=coretree.ray_cast(q,direction,extent)
   if hit is not None:hits.append((dist,t,q,hit))
  assert hits,'Lower face must see actual core';dist,t,q,hit=min(hits,key=lambda x:x[0]);move=direction*(dist+margin)
  for i in low:o.data.vertices[i].co=V[i]+move
  records.append(dict(component=rec['component'],part=rec['connected_part_index'],vertices=ids,lower_vertices=low,upper_vertices=upper,translation=list(move),translation_length_m=move.length,first_core_hit_distance_m=dist,lower_triangle=list(t),old_lower_center=list(q),core_hit=list(hit),planned_witness=list(q+direction*(dist+margin*.5)),numerical_design_margin_m=margin,before=[list(V[i]) for i in low],after=[list(o.data.vertices[i].co) for i in low]))
 o.data.update();bpy.context.view_layer.update();after=snapshot(o);changed=[i for i,(x,y) in enumerate(zip(before['vertices'],after['vertices'])) if x!=y];expected=sorted(i for r in records for i in r['lower_vertices']);assert changed==expected
 for k in before:
  if k!='vertices':assert before[k]==after[k],k
 assert bpy.data.texts['BATCH108_COMPONENT_CONTRACT.json'].as_string()==ctext
 o.data.calc_loop_triangles();np.savez_compressed(out/'after.npz',vertices=np.array(after['vertices'],dtype=np.float64),triangles=np.array([tuple(t.vertices) for t in o.data.loop_triangles],dtype=np.int32))
 col=next(c for c in bpy.data.collections if c.get('asset_root'));export_asset(aid,aid,'animals',col,metadata={'representation':'living-reconstruction','export_texcoords':False,'source_scope':'Immutable batch108 original scope; r003 only lowers proven detached plate undersides.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 def jhash(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 identity={k:{'before':jhash(before[k]),'after':jhash(after[k]),'identical':before[k]==after[k]} for k in before if k!='vertices'};unchanged=[i for i in range(len(V)) if i not in set(changed)];identity['unaffected_vertices']={'count':len(unchanged),'before':jhash([before['vertices'][i] for i in unchanged]),'after':jhash([after['vertices'][i] for i in unchanged]),'identical':True};identity['contract']={'sha256':hashlib.sha256(ctext.encode()).hexdigest(),'identical':True}
 (out/'repair-identity.json').write_text(json.dumps(dict(asset=aid,source_sha256=h(source),records=records,changed_vertex_indices=changed,unchanged_identity=identity,only_lower_vertices_changed=True,precision_note='The modest extent-scaled margin is an implementation choice to keep float32-exported contact numerically resolvable, not an acceptance tolerance or a scientific minimum overlap.'),indent=2)+'\n')
 (out/'execution.json').write_text(json.dumps(dict(pid=os.getpid(),parent_pid=os.getppid(),argv=sys.argv,started_at_executor_clock=start,finished_at_executor_clock=datetime.datetime.now(datetime.timezone.utc).isoformat(),generator_sha256=h(Path(__file__)),config_sha256=h(Path(a.config)),source_sha256=h(source),blender=bpy.app.version_string,clock_note='Executor clock only.'),indent=2)+'\n')
if __name__=='__main__':main()
