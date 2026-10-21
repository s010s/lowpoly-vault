#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Localized r001 source-preserving axial-end taper, not whole-colony regeneration."""
import argparse,datetime,hashlib,json,math,os,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import export_asset
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);c=json.loads(Path(args.config).read_text());r=c['repair'];source=ROOT/r['source_path'];assert sha(source)==r['source_sha256'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);assert not any(out.iterdir());started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False);ct=json.loads(bpy.data.texts['BATCH105_COMPONENT_CONTRACT.json'].as_string());ob=bpy.data.objects[ct['object_name']];old=[tuple(v.co) for v in ob.data.vertices];faces=[tuple(p.vertices) for p in ob.data.polygons];mats=[p.material_index for p in ob.data.polygons];transform=[list(row) for row in ob.matrix_world];ax=next(v for v in ct['components'] if v['tag']=='axial_helix');ids=ax['vertices'];p=c['parameters'];off=Vector(ct['translation']);T=p['turns']*2*math.pi;H=p['axis_height_m'];rad=p['axis_helix_radius_m'];center=lambda i:Vector((rad*math.cos(T*i/120),rad*math.sin(T*i/120),H*i/120))+off
 records=[];changed=set();allowed=set();ringmap={}
 for i in [0,1,2,3,117,118,119,120]:
  ctr=center(i);a=(center(min(i+1,120))-center(max(i-1,0))).normalized();ref=Vector((0,0,1))
  if abs(a.dot(ref))>.95:ref=Vector((0,1,0))
  w=ref.cross(a).normalized();t=a.cross(w);ring=[]
  for j in range(8):
   expected=ctr+p['axis_tube_radius_m']*(w*math.cos(2*math.pi*j/8)+t*math.sin(2*math.pi*j/8));idx=min(ids,key=lambda k:(Vector(old[k])-expected).length);assert (Vector(old[idx])-expected).length<1e-8;ring.append(idx)
  assert len(set(ring))==8;ringmap[i]=ring;allowed.update(ring);actual=sum((Vector(old[k]) for k in ring),Vector())/8;scale=r['terminal_ring_scales'][min(i,120-i)]
  for k in ring:ob.data.vertices[k].co=actual+(Vector(old[k])-actual)*scale
  shift=Vector((0,0,0))
  if i==0 and r['lower_endpoint_preserve_original_min_z']:
   shift.z=min(v[2] for v in old)-min(ob.data.vertices[k].co.z for k in ring)
   for k in ring:ob.data.vertices[k].co+=shift
   cap=min(ids,key=lambda k:(Vector(old[k])-ctr).length);assert (Vector(old[cap])-ctr).length<1e-8;ob.data.vertices[cap].co+=shift;allowed.add(cap)
  aftercenter=actual+shift;records.append({'ring_index':i,'vertices':ring,'scale_artistic_not_threshold':scale,'before_radius_m':[float((Vector(old[k])-actual).length) for k in ring],'after_radius_m':[float((ob.data.vertices[k].co-aftercenter).length) for k in ring],'terminal_translation_m':list(shift)})
 ob.data.update();bpy.context.view_layer.update();changed={i for i,v in enumerate(ob.data.vertices) if tuple(v.co)!=old[i]};assert changed==allowed;assert faces==[tuple(p.vertices) for p in ob.data.polygons];assert mats==[p.material_index for p in ob.data.polygons];assert transform==[list(row) for row in ob.matrix_world]
 frond=next(v for v in ct['components'] if v['kind']=='perforated_frond');assert all(tuple(ob.data.vertices[i].co)==old[i] for i in frond['vertices']);assert len(ct['integrated_features'])==300
 audit={'schema_version':1,'source_sha256':sha(source),'modified_vertices':sorted(changed),'modified_vertex_count':len(changed),'unchanged_vertices':len(old)-len(changed),'all_faces_unchanged':True,'all_material_indices_unchanged':True,'all_transforms_unchanged':True,'frond_vertices_unchanged':True,'frond_vertex_count':len(frond['vertices']),'all_300_feature_records_unchanged':True,'interior_axial_rings_4_through_116_unchanged':True,'endpoint_ring_measurements':records,'method':'Direct per-index exact float comparison against reopened original source. No topology repair, normal recalculation, weld, camera/material concealment, or normalization.','original_requirement':'Keep actual holes and taper incomplete ends; no massive root base.'}
 bpy.data.texts.new('ARCHIMEDES_R002_REPAIR.json').write(json.dumps({'config':c,'identity_audit':audit},sort_keys=True));col=next(x for x in bpy.data.collections if x.get('asset_root'));export_asset('archimedes','archimedes','animals',col,metadata={'representation':'bounded-skeletal-reconstruction','export_texcoords':False,'source_scope':'Original batch105 freeze; endpoint-only r002 repair.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 (out/'geometry-identity.json').write_text(json.dumps(audit,indent=2)+'\n');assert sha(source)==r['source_sha256'];(out/'execution.json').write_text(json.dumps({'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at_executor_clock':started,'finished_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator_sha256':sha(HERE),'config_sha256':sha(args.config),'original_source_sha256':sha(source),'blender_version':bpy.app.version_string,'source_modified':False},indent=2)+'\n')
if __name__=='__main__':main()
