#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only original embedded-image integrity/budget check; never grants approval."""
import argparse
import hashlib
import json
from pathlib import Path
from qa_glb import read_glb
from validate_candidate import checked_file, relative_file, json_bytes, obj, arr, need, integer, text, image_size


def check_textures(candidate, root):
    root=Path(root).resolve()
    result={'status':'fail','errors':[],'grants_approval':False,'grants_publication':False}
    try:
        record=obj(json_bytes(relative_file(root,str(candidate),'candidate').read_bytes(),'candidate'),'candidate')
        artifacts=obj(record.get('artifacts'),'artifacts')
        glb,_=checked_file(root,artifacts['glb'],'glb')
        _,brief_raw=checked_file(root,artifacts['brief'],'brief');brief=obj(json_bytes(brief_raw,'brief'),'brief')
        _,refs_raw=checked_file(root,artifacts['references'],'references');refs=obj(json_bytes(refs_raw,'references'),'references')
        source_rows=arr(refs.get('sources'),'sources');sources={s['id']:s for s in source_rows};need(len(sources)==len(source_rows),'Duplicate source IDs')
        doc,binary,_=read_glb(glb);images=doc.get('images',[]);rows=arr(record.get('textures'),'textures')
        need(len(images)==len(rows),'Every embedded image needs one original texture record')
        measured={'texture_count':len(images),'texture_max_dimension':0,'texture_bytes':0,'decoded_texture_bytes_estimate':0}
        seen=set()
        for row in rows:
            row=obj(row,'texture');index=integer(row.get('image_index'),'image_index');need(index<len(images)and index not in seen,'Duplicate/invalid image_index');seen.add(index)
            image=images[index];need('uri'not in image and 'bufferView'in image,'Standalone embedded image required')
            view=doc['bufferViews'][image['bufferView']];start=integer(view.get('byteOffset',0),'image offset');size=integer(view.get('byteLength'),'image bytes',1)
            need(view.get('buffer',0)==0 and start+size<=len(binary),'Invalid embedded image range')
            _,raw=checked_file(root,row,'original texture');need(raw==binary[start:start+size],'Original PNG differs from embedded GLB bytes')
            width,height=image_size(raw);need(row.get('width')==width and row.get('height')==height and row.get('byte_length')==len(raw),'Texture dimensions/bytes mismatch')
            provenance=obj(row.get('provenance'),'texture provenance');source=obj(sources.get(provenance.get('source_id')),'original source')
            need(source.get('use')=='original-authored incorporated texture','Consulted sources cannot supply incorporated images')
            need(source.get('creator')==provenance.get('creator')=='Leon Made This / s010s','Original texture creator must match frozen asset owner')
            need(source.get('license')==provenance.get('license')=='CC-BY-4.0','Owner-authored image license must match asset license')
            text(source.get('url'),'original source URL');text(provenance.get('usage'),'texture usage');text(source.get('rights_note'),'original rights note')
            measured['texture_max_dimension']=max(measured['texture_max_dimension'],width,height);measured['texture_bytes']+=len(raw)
            while True:
                measured['decoded_texture_bytes_estimate']+=width*height*4
                if width==height==1:break
                width,height=max(1,width//2),max(1,height//2)
        policy=obj(brief.get('texture_policy'),'texture policy')
        for key,limit in [('texture_count','max_textures'),('texture_max_dimension','max_dimension'),('texture_bytes','max_total_bytes'),('decoded_texture_bytes_estimate','max_decoded_bytes')]:
            maximum=integer(policy.get(limit),limit);need(measured[key]<=maximum,f'{key} exceeds frozen {limit}')
        result.update(status='pass',glb_sha256=hashlib.sha256(glb.read_bytes()).hexdigest(),measurements=measured)
    except (ValueError,OSError,KeyError,TypeError,IndexError) as error:result['errors'].append(str(error))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('candidate');parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args()
    result=check_textures(args.candidate,args.root);print(json.dumps(result,indent=2));return 0 if result['status']=='pass'else 1


if __name__=='__main__':raise SystemExit(main())
