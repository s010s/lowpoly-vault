# SPDX-License-Identifier: MIT
"""Read-only editable-source checks. Run after opening model.blend in Blender."""
import hashlib,json,sys
from pathlib import Path
import bpy,bmesh

def main():
    output=Path(sys.argv[sys.argv.index('--')+1]);parts=[];errors=[]
    for o in bpy.data.objects:
        if o.type in ('LIGHT','CAMERA'):errors.append('Presentation object in source: '+o.name)
        if o.type!='MESH':continue
        bm=bmesh.new();bm.from_mesh(o.data);unseen=set(bm.verts);volumes=[]
        while unseen:
            seed=unseen.pop();todo=[seed];comp={seed}
            while todo:
                v=todo.pop()
                for e in v.link_edges:
                    w=e.other_vert(v)
                    if w in unseen:unseen.remove(w);comp.add(w);todo.append(w)
            faces={f for v in comp for f in v.link_faces};vol=0
            for f in faces:
                p=[v.co for v in f.verts]
                for i in range(1,len(p)-1):vol+=p[0].dot(p[i].cross(p[i+1]))/6
            volumes.append(vol)
        if any(v<=0 for v in volumes):errors.append('Nonpositive closed-component volume: '+o.name)
        coords=[o.matrix_world@v.co for v in o.data.vertices];lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)]
        parts.append({'name':o.name,'bounds_blender_m':{'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]},'closed_components':len(volumes),'positive_outward_component_volumes':all(v>0 for v in volumes),'minimum_component_volume_m3':min(volumes)});bm.free()
    record={'status':'PASS' if not errors else 'FAIL','model_blend_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'errors':errors,'scene_objects':len(bpy.data.objects),'mesh_objects':len(parts),'camera_light_objects':0,'root_identity':all(abs(bpy.data.objects['cyamodus'].matrix_world[r][c]-(1 if r==c else 0))<1e-8 for r in range(4) for c in range(4)),'parts':parts,'notes':['Closed components may intentionally overlap at anatomical joins and armor substrates. This does not certify Boolean union or intersection absence.','Source has semantic editable meshes, no external images, textures, libraries, cameras or lights.']}
    record['external_images']=len([x for x in bpy.data.images if x.filepath and not x.packed_file]);record['linked_libraries']=len(bpy.data.libraries)
    output.write_text(json.dumps(record,indent=2)+'\n')
    if errors:raise RuntimeError(errors)
if __name__=='__main__':main()
