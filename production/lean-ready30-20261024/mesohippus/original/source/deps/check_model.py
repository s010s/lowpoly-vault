#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fresh source reopen and exact GLB correspondence, with anatomical geometry counts.
These checks do not establish scientific truth or visual acceptance.
"""
import argparse, hashlib, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from asset_common import audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True,type=Path);ap.add_argument('--glb',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args(argv)
    sh,gh=sha(a.source),sha(a.glb)
    bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()),load_ui=False,use_scripts=False)
    bpy.context.view_layer.update(); c=bpy.data.collections['EXPORT']; src=audit_source(c,18000); exp=audit_glb(a.glb,18000,8,36);exp['file']='model.glb'
    errors=list(src['errors'])+list(exp['errors']); warnings=list(src['warnings'])+list(exp['warnings'])
    bounds=src['bounds_blender_m']; expected={'min':[bounds['min'][0],bounds['min'][2],-bounds['max'][1]],'max':[bounds['max'][0],bounds['max'][2],-bounds['min'][1]]}
    delta=max(abs(expected[s][i]-exp['bounds_m'][s][i]) for s in ('min','max') for i in range(3))
    if delta>0.0001 or src['triangles']!=exp['scene_triangles']: errors.append('Source/export mismatch')
    unintended=[o.name for o in bpy.data.objects if o.type in ('CAMERA','LIGHT') or o.name.startswith('_PREVIEW')]
    if unintended: errors.append('Presentation objects in source')
    feet=[]
    for o in c.objects:
        if o.type!='MESH' or not o.name.endswith('_three_distinct_toes'): continue
        mesh=o.data; inds=set(); adjacent={}
        for f in mesh.polygons:
            if f.material_index==1:
                for v in f.vertices: inds.add(v); adjacent.setdefault(v,set()).update(f.vertices)
        parts=[]
        while inds:
            todo=[min(inds)]; found=set()
            while todo:
                v=todo.pop()
                if v in found: continue
                found.add(v);todo.extend(adjacent[v]-found)
            inds-=found
            points=[o.matrix_world@mesh.vertices[v].co for v in sorted(found)]
            lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
            parts.append({'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]})
        parts.sort(key=lambda p:p['min'][0]); r={'object':o.name,'disconnected_hoof_components':len(parts),'hooves':parts,'lowest_z_m':min(p['min'][2] for p in parts)}
        if len(parts)!=3: errors.append(o.name+': expected three discrete hoof components')
        else:
            r['central_width_over_lateral']=[parts[1]['size'][0]/parts[i]['size'][0] for i in (0,2)]
            r['tip_x_gaps_m']=[parts[1]['min'][0]-parts[0]['max'][0],parts[2]['min'][0]-parts[1]['max'][0]]
            if min(r['central_width_over_lateral'])<1.4: errors.append(o.name+': middle hoof not clearly enlarged')
            if min(r['tip_x_gaps_m'])<=0: errors.append(o.name+': hoof bounds not laterally separated')
            if abs(r['lowest_z_m'])>0.002: errors.append(o.name+': floor contact mismatch')
        feet.append(r)
    if len(feet)!=4: errors.append('Expected four independently identified three-toed feet')
    root=bpy.data.objects[c['asset_root']]
    if tuple(root.location)!=(0.,0.,0.) or tuple(root.scale)!=(1.,1.,1.) or any(root.rotation_euler): errors.append('Root transform is not identity')
    external_images=[i.name for i in bpy.data.images if i.source=='FILE' and i.filepath]
    libraries=[x.name for x in bpy.data.libraries]
    if external_images or libraries: errors.append('Unexpected external source dependencies')
    if sha(a.source)!=sh or sha(a.glb)!=gh: errors.append('Input artifact changed')
    result={'schema_version':1,'status':'PASS' if not errors else 'FAIL','source_sha256':sh,'glb_sha256':gh,'blender_version':bpy.app.version_string,'source_reopened':True,'source_saved':False,'script_autoexec':False,'source_audit':src,'glb_audit':exp,'bounds_max_error_m':delta,'unintended_presentation_objects':unintended,'external_images':external_images,'libraries':libraries,'feet':feet,'errors':errors,'warnings':warnings,'limitations':'Closed semantic components intentionally overlap at joints. Not a watertight union, scientific proof, independent visual verdict or GPU/scene check.'}
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
    if errors: raise RuntimeError(errors)
if __name__=='__main__':main()
