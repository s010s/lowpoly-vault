# SPDX-License-Identifier: MIT
"""Normalized static GLB geometry/material identity, not an arbitrary glTF validator."""
import hashlib,json,sys
from pathlib import Path
from qa_glb import read_glb,accessor_values

def normalized(path):
    doc,binary,_=read_glb(path)
    meshes=[]
    for mesh in doc.get('meshes',[]):
        primitives=[]
        for p in mesh['primitives']:
            attributes={k:accessor_values(doc,binary,v) for k,v in sorted(p['attributes'].items())}
            primitives.append({'attributes':attributes,'indices':accessor_values(doc,binary,p['indices']),'material':p.get('material'),'mode':p.get('mode',4)})
        meshes.append({'name':mesh.get('name'),'primitives':primitives})
    nodes=[{k:v for k,v in n.items() if k in ('name','mesh','children','matrix','translation','rotation','scale')} for n in doc.get('nodes',[])]
    record={'meshes':meshes,'materials':doc.get('materials',[]),'nodes':nodes,'scenes':doc.get('scenes'),'scene':doc.get('scene',0)}
    return hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
if __name__=='__main__':
    for f in sys.argv[1:]: print(normalized(f),f)
