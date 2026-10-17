# SPDX-License-Identifier: MIT
"""Repack identity-transform static source geometry into one mesh / material primitives.
No quantization, compression extension, normal/position rounding or triangle deletion.
"""
import json, struct
from pathlib import Path

def pack(path):
    from qa_glb import read_glb, accessor_values
    doc,binary,raw=read_glb(path)
    # This generated source uses identity mesh nodes; fail rather than bake unknown transforms.
    mesh_nodes=[n for n in doc['nodes'] if 'mesh' in n]
    common_transform={k:mesh_nodes[0][k] for k in ('matrix','translation','rotation','scale') if k in mesh_nodes[0]}
    for node in mesh_nodes:
        assert {k:node[k] for k in ('matrix','translation','rotation','scale') if k in node}==common_transform, node
    groups={}
    for mesh in doc['meshes']:
        for primitive in mesh['primitives']:
            assert set(primitive['attributes'])=={'POSITION','NORMAL'} and primitive.get('mode',4)==4
            material=primitive.get('material');g=groups.setdefault(material,{'verts':[],'norms':[],'indices':[],'lookup':{}})
            pos=accessor_values(doc,binary,primitive['attributes']['POSITION']);nor=accessor_values(doc,binary,primitive['attributes']['NORMAL'])
            indexes=accessor_values(doc,binary,primitive['indices'])
            for (i,) in indexes:
                key=(pos[i],nor[i]);lookup=g['lookup']
                if key not in lookup:
                    lookup[key]=len(g['verts']);g['verts'].append(pos[i]);g['norms'].append(nor[i])
                g['indices'].append(lookup[key])
    new={'asset':doc['asset'],'scene':0,'scenes':[{'nodes':[0]}], 'nodes':[{'name':'fern-cluster','children':[1]},{'name':'Fern material-batched export','mesh':0}], 'materials':doc['materials'],'meshes':[{'name':'Fern material-batched export','primitives':[]}], 'accessors':[],'bufferViews':[],'buffers':[]}
    new['nodes'][1].update(common_transform)
    blob=bytearray()
    def acc(values,fmt,component,kind,target):
        while len(blob)%4:blob.append(0)
        offset=len(blob)
        for value in values:blob.extend(struct.pack('<'+fmt,*value))
        view=len(new['bufferViews']);new['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(blob)-offset,'target':target})
        a={'bufferView':view,'componentType':component,'count':len(values),'type':kind}
        if kind=='VEC3':a.update(min=[min(v[k] for v in values) for k in range(3)],max=[max(v[k] for v in values) for k in range(3)])
        index=len(new['accessors']);new['accessors'].append(a);return index
    for material,g in sorted(groups.items()):
        pos=acc(g['verts'],'fff',5126,'VEC3',34962);normal=acc(g['norms'],'fff',5126,'VEC3',34962)
        assert len(g['verts'])<65536
        idx=acc([(x,) for x in g['indices']],'H',5123,'SCALAR',34963)
        new['meshes'][0]['primitives'].append({'attributes':{'POSITION':pos,'NORMAL':normal},'indices':idx,'material':material,'mode':4})
    new['buffers']=[{'byteLength':len(blob)}]
    while len(blob)%4:blob.append(0)
    encoded=json.dumps(new,separators=(',',':')).encode();encoded+=b' '*((-len(encoded))%4)
    result=struct.pack('<4sII',b'glTF',2,12+8+len(encoded)+8+len(blob))+struct.pack('<II',len(encoded),0x4e4f534a)+encoded+struct.pack('<II',len(blob),0x004e4942)+blob
    Path(path).write_bytes(result)
    return {'before_bytes':len(raw),'after_bytes':len(result),'before_meshes':len(doc['meshes']),'after_primitives':len(groups),'quantized':False,'extensions_added':[]}
