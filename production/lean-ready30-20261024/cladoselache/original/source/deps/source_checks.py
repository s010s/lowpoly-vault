# SPDX-License-Identifier: MIT
"""Read the actual editable source and compare with the delivered GLB."""
from pathlib import Path
import hashlib,json,sys
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import audit_source
from qa_glb import audit_glb
from check_source_export import compare_source_audit

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    root=Path(sys.argv[sys.argv.index('--')+1]);source=root/'model.blend';glb=root/'model.glb';before=[sha(source),sha(glb)]
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()),load_ui=False,use_scripts=False)
    col=bpy.data.collections['EXPORT'];bpy.context.view_layer.update();s=audit_source(col,16000);g=audit_glb(glb,16000,8,100);g['file']='model.glb'
    result=compare_source_audit(s,g,before[0],before[1]);result.update({'blender_version':bpy.app.version_string,'source':'model.blend','glb':'model.glb','source_audit':s,'glb_audit':g,'script_autoexec':False,'source_saved':False,'source_bytes_unchanged':before==[sha(source),sha(glb)],'external_dependency_counts':{'linked_libraries':len(bpy.data.libraries),'external_images':sum(bool(x.filepath) and not x.packed_file for x in bpy.data.images),'text_blocks':len(bpy.data.texts)},'warning_disposition':'Both lowest-Z/Y warnings are intentional swimming-center origin, not ground-contact failure. All parts are closed; intentional root/eye/gill/lip overlaps are not a boolean-union claim.','checker_sha256':sha(Path(__file__))})
    p=root/'qa/evidence/source-export.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n')
    assert not result['errors'] and result['source_bytes_unchanged']
    assert not any(result['external_dependency_counts'].values())
if __name__=='__main__':main()
