# SPDX-License-Identifier: MIT
"""Extract retained PNG C2PA action declarations without asserting signature trust."""
import hashlib
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parent.parent
raw=(ROOT/'concept-original.png').read_bytes()
label=raw.index(b'c2pa.actions.v2\x00')
kind=raw.index(b'cbor',label)
length=struct.unpack_from('>I',raw,kind-4)[0]
data=raw[kind+4:kind-4+length]
offset=0

def decode():
    global offset
    head=data[offset];offset+=1;major=head>>5;additional=head&31
    if additional<24:n=additional
    elif additional in (24,25,26,27):
        size={24:1,25:2,26:4,27:8}[additional]
        n=int.from_bytes(data[offset:offset+size],'big');offset+=size
    else:raise ValueError('Unsupported CBOR length')
    if major==0:return n
    if major==1:return -1-n
    if major in (2,3):
        value=data[offset:offset+n];offset+=n
        return value.hex() if major==2 else value.decode('utf-8')
    if major==4:return [decode() for _ in range(n)]
    if major==5:
        value={}
        for _ in range(n):key=decode();value[key]=decode()
        return value
    if major==6:return {'cbor_tag':n,'value':decode()}
    if major==7 and n in (20,21,22):return {20:False,21:True,22:None}[n]
    raise ValueError('Unsupported CBOR type')

decoded=decode()
assert offset==len(data)
created=[x for x in decoded['actions'] if x['action']=='c2pa.created']
assert len(created)==1 and created[0]['when']['cbor_tag']==0
report={'source':'concept-original.png','source_sha256':hashlib.sha256(raw).hexdigest(),
        'evidence_type':'embedded C2PA c2pa.actions.v2 declaration',
        'cbor_box_offset':kind-4,'cbor_payload_sha256':hashlib.sha256(data).hexdigest(),
        'decoded_assertion':decoded,'concept_created_at_declaration':created[0]['when']['value'],
        'first_pixel_inspection_at':None,'first_pixel_inspection_status':'unknown',
        'signature_or_trusted_timestamp_validation':'not_run',
        'limitation':'Provider-embedded creation-time attestation only. Does not prove tool completion, first viewing time or a trusted wall clock. No filesystem mtime used.'}
(ROOT/'closure-20261019/concept-time-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
