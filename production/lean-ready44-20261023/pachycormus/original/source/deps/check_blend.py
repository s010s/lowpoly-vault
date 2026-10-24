# SPDX-License-Identifier: MIT
"""Reopen the editable source; report source-only geometry and closure facts."""
from pathlib import Path
import argparse, hashlib, json, sys
import bpy, bmesh

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--blend',required=True,type=Path);ap.add_argument('--glb',required=True,type=Path);ap.add_argument('--report',required=True,type=Path);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(args.blend.resolve()))
    root=bpy.data.objects.get('pachycormus');parts=[];errors=[]
    for obj in bpy.data.objects:
        if obj.type in {'CAMERA','LIGHT'} or obj.name.startswith('_PREVIEW'):errors.append('Presentation object saved in editable source')
        if obj.type!='MESH':continue
        bm=bmesh.new();bm.from_mesh(obj.data)
        info={'name':obj.name,'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'scale':list(obj.scale),'negative_determinant':obj.matrix_world.to_3x3().determinant()<=0,'modifiers':len(obj.modifiers)}
        if info['boundary_edges'] or info['nonmanifold_edges'] or info['signed_volume_m3']<=0 or info['negative_determinant']:errors.append('Closed outward component test failed: '+obj.name)
        parts.append(info);bm.free()
    external=[]
    for image in bpy.data.images:
        if image.filepath and not image.packed_file:external.append(image.name)
    if bpy.data.libraries:external.extend(lib.name for lib in bpy.data.libraries)
    if external:errors.append('External image or linked-library dependency')
    if bpy.data.texts:errors.append('Unexpected embedded script/text block')
    identity=root is not None and all(abs(root.matrix_world[r][c]-(1 if r==c else 0))<1e-7 for r in range(4) for c in range(4))
    if not identity:errors.append('Nonidentity or missing mount root')
    report={'status':'PASS' if not errors else 'FAIL','blend_sha256':sha(args.blend),'glb_sha256':sha(args.glb),'errors':errors,'root_identity':identity,'root_forward':root.get('authoring_forward') if root else None,'external_datablocks':external,'embedded_text_blocks':len(bpy.data.texts),'parts':parts,'scope':'Reopened source topology, positive signed volumes, identity transforms and external datablocks. Not a proof of Boolean-union topology, absence of all self-intersections, anatomy or GPU rendering.'}
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n')
    if errors:raise RuntimeError('; '.join(errors))
    print('REOPEN_PASS',len(parts))
if __name__=='__main__':main()
