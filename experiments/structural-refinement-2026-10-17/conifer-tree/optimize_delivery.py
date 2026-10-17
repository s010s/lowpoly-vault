#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Controlled, original static GLB material consolidation and 16-bit storage study.
No triangle removal or material change; quantization is separately labeled lossy.
"""
import argparse,copy,hashlib,json,math,struct,sys
from pathlib import Path
HERE=Path(__file__).resolve();REPO=next(p for p in HERE.parents if (p/'scripts/qa_glb.py').exists());sys.path.insert(0,str(REPO/'scripts'))
from qa_glb import read_glb,accessor_values,audit_glb

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(path,doc,binary):
    doc['buffers']=[{'byteLength':len(binary)}]
    js=json.dumps(doc,separators=(',',':'),allow_nan=False).encode();js+=b' '*((-len(js))%4)
    binary+=b'\0'*((-len(binary))%4)
    path.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(js)+len(binary))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(binary),0x004e4942)+binary)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('--output-dir',type=Path,required=True);args=ap.parse_args()
    out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    doc,blob,raw=read_glb(args.source)
    mesh_nodes=[n for n in doc['nodes'] if 'mesh' in n];translations={tuple(n.get('translation',[0,0,0])) for n in mesh_nodes}
    assert len(translations)==1 and not any('rotation' in n or 'scale'in n or 'matrix'in n for n in mesh_nodes)
    translation=list(next(iter(translations)))
    assert not any(x in doc for x in ['skins','animations','textures','images'])
    groups={};triangles=0;source_primitives=0
    for mesh in doc['meshes']:
      for prim in mesh['primitives']:
        assert set(prim['attributes'])=={'POSITION','NORMAL'} and prim.get('mode',4)==4
        pos=accessor_values(doc,blob,prim['attributes']['POSITION']);norm=accessor_values(doc,blob,prim['attributes']['NORMAL']);ind=[x[0] for x in accessor_values(doc,blob,prim['indices'])]
        g=groups.setdefault(prim['material'],{'p':[],'n':[],'i':[]});base=len(g['p']);g['p'].extend(pos);g['n'].extend(norm);g['i'].extend(i+base for i in ind);triangles+=len(ind)//3;source_primitives+=1
    allp=[p for g in groups.values() for p in g['p']];low=[min(p[k] for p in allp) for k in range(3)];high=[max(p[k] for p in allp) for k in range(3)];scale=max(high[k]-low[k] for k in range(3))
    original_digest=hashlib.sha256()
    for mat,g in sorted(groups.items()):
      for i in g['i']:original_digest.update(struct.pack('<I6f',mat,*g['p'][i],*g['n'][i]))
    results=[]
    for mode in ['lossless-compact','quantized-16']:
      binary=bytearray();views=[];accessors=[];prims=[];max_p_error=0;max_n_angle=0;max_n_length_error=0;isq=mode=='quantized-16';retained=hashlib.sha256()
      def stream(rows,component,type_,fmt,target,normalized=False,minimum=None,maximum=None,stride=None):
        nonlocal binary
        while len(binary)%4:binary+=b'\0'
        start=len(binary)
        for row in rows:binary+=struct.pack('<'+fmt,*row)
        view={'buffer':0,'byteOffset':start,'byteLength':len(binary)-start,'target':target}
        if stride:view['byteStride']=stride
        vi=len(views);views.append(view);a={'bufferView':vi,'componentType':component,'count':len(rows),'type':type_}
        if normalized:a['normalized']=True
        if minimum is not None:a['min']=minimum;a['max']=maximum
        ai=len(accessors);accessors.append(a);return ai
      for mat,g in sorted(groups.items()):
        p,n,i=g['p'],g['n'],g['i']
        if isq:
          qp=[tuple(max(0,min(65535,round((x[k]-low[k])/scale*65535))) for k in range(3)) for x in p]
          qn=[tuple(max(-32767,min(32767,round(x[k]*32767))) for k in range(3)) for x in n]
          for p0,q in zip(p,qp):max_p_error=max(max_p_error,math.sqrt(sum((low[k]+q[k]/65535*scale-p0[k])**2 for k in range(3))))
          for n0,q in zip(n,qn):
            nd=[x/32767 for x in q];nl=math.sqrt(sum(x*x for x in nd));ol=math.sqrt(sum(x*x for x in n0));max_n_length_error=max(max_n_length_error,abs(nl-1));dot=sum(a*b for a,b in zip(n0,nd))/(nl*ol);max_n_angle=max(max_n_angle,math.degrees(math.acos(max(-1,min(1,dot)))))
          pa=stream(qp,5123,'VEC3','3H2x',34962,True,[min(x[k] for x in qp) for k in range(3)],[max(x[k] for x in qp) for k in range(3)],8)
          na=stream(qn,5122,'VEC3','3h2x',34962,True,stride=8)
        else:
          pa=stream(p,5126,'VEC3','3f',34962,False,[min(x[k] for x in p) for k in range(3)],[max(x[k] for x in p) for k in range(3)])
          na=stream(n,5126,'VEC3','3f',34962)
          for k in i:retained.update(struct.pack('<I6f',mat,*p[k],*n[k]))
        assert len(p)<65536
        ia=stream([(x,) for x in i],5123,'SCALAR','H',34963)
        prims.append({'attributes':{'POSITION':pa,'NORMAL':na},'indices':ia,'material':mat})
      node={'mesh':0,'name':'conifer-tree consolidated delivery mesh','translation':translation}
      if isq:node.update(translation=[low[k]+translation[k] for k in range(3)],scale=[scale]*3)
      new={'asset':{'version':'2.0','generator':'lowpoly-vault controlled delivery study'},'scene':0,'scenes':[{'nodes':[1]}],'nodes':[node,{'name':'conifer-tree','children':[0],'extras':copy.deepcopy(doc['nodes'][-1].get('extras',{}))}],'meshes':[{'name':'conifer-tree by material','primitives':prims}],'materials':copy.deepcopy(doc['materials']),'bufferViews':views,'accessors':accessors}
      if isq:new.update(extensionsUsed=['KHR_mesh_quantization'],extensionsRequired=['KHR_mesh_quantization'])
      path=out/(mode+'.glb');write(path,new,bytes(binary));audit=audit_glb(path,24000,5,24);(out/(mode+'.audit.json')).write_text(json.dumps(audit,indent=2)+'\n')
      results.append({'variant':mode,'path':path.name,'sha256':sha(path),'raw_bytes':path.stat().st_size,'buffer_bytes':len(binary),'triangles':triangles,'primitives':len(prims),'materials':len(new['materials']),'position_stream_vertices':sum(len(g['p']) for g in groups.values()),'max_position_error_m':max_p_error,'max_normal_angle_error_degrees':max_n_angle,'max_normal_length_error':max_n_length_error,'ordered_material_triangle_digest':retained.hexdigest() if not isq else None,'lossless_render_arrays_identical':retained.hexdigest()==original_digest.hexdigest() if not isq else False,'requires_extension':'KHR_mesh_quantization' if isq else None,'requires_external_decoder':False,'audit_status':audit['status'],'audit_errors':audit['errors']})
    report={'source':str(args.source),'source_sha256':sha(args.source),'source_raw_bytes':len(raw),'source_primitives':source_primitives,'source_attributes':['POSITION','NORMAL'],'unused_uv_or_tangent_attributes':False,'source_ordered_material_triangle_digest':original_digest.hexdigest(),'source_triangles':triangles,'quantization_profile':'Unsigned normalized 16-bit positions with uniform node scale and offset; signed normalized 16-bit normals; 4-byte element alignment. No topology/triangle removal.','references':['https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_mesh_quantization/README.md'],'variants':results,'limitations':'No runtime GPU or visual approval. Lossless grouping changes scene graph only. Quantization changes positions/normals within measured errors and requires new evidence.'}
    (out/'optimization-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
