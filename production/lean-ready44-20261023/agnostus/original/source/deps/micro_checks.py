# SPDX-License-Identifier: MIT
"""Scale-aware source and GLB checks for a sub-millimeter arthropod.
Uses the canonical static GLB decoder without its meter-scale absolute area
cutoff, which would reject legitimate microscopic limbs. Physical area tests
are explicit here; delivered geometry is never enlarged for an audit.
"""
import hashlib,json,math
from pathlib import Path
from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform,IDENTITY,semantic_digest

def source_audit(collection,max_triangles=40000):
    import bpy,bmesh
    errors=[];warn=[];parts=[];points=[];tris=0;areas=[]
    for o in collection.objects:
        if o.type not in ['EMPTY','MESH']:errors.append(o.name+': unsupported type');continue
        if o.type!='MESH':continue
        if o.matrix_world.to_3x3().determinant()<=0:errors.append(o.name+': nonpositive determinant')
        if any(abs(s-1)>1e-8 for s in o.scale):errors.append(o.name+': nonidentity scale')
        m=o.data;m.calc_loop_triangles();tris+=len(m.loop_triangles)
        points.extend(tuple(o.matrix_world@v.co) for v in m.vertices)
        aa=[t.area for t in m.loop_triangles];areas.extend(aa)
        bad=sum(not math.isfinite(a) or a<1e-20 for a in aa)
        if bad:errors.append(o.name+': actual near-zero area triangles '+str(bad))
        bm=bmesh.new();bm.from_mesh(m)
        bd=sum(e.is_boundary for e in bm.edges);nm=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
        if bd or nm:errors.append(o.name+': unexpected open/nonmanifold edges')
        if vol<=0:errors.append(o.name+': nonpositive signed volume')
        parts.append({'name':o.name,'triangles':len(m.loop_triangles),'boundary_edges':bd,'nonmanifold_edges':nm,'signed_volume_m3':vol})
    if tris>max_triangles:errors.append('triangle budget exceeded')
    if any(not math.isfinite(x) for p in points for x in p):errors.append('nonfinite vertex')
    lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
    return {'status':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warn,'triangles':tris,'parts':parts,'bounds_blender_m':{'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]},'min_triangle_area_m2':min(areas),'area_threshold_m2':1e-20,'scale_note':'Explicit micron-scale absolute cutoff, not canonical meter-scale 1e-10 m2 cutoff. No geometric enlargement.'}

def glb_audit(path,source):
    doc,blob,raw=read_glb(path);errors=[];warn=[];points=[];prims=0;tris=0;areas=[];vertices=0;geom=[]
    if doc.get('asset',{}).get('version')!='2.0':errors.append('Not glTF2')
    if len(doc.get('buffers',[]))!=1 or any('uri' in b for b in doc.get('buffers',[])):errors.append('Not embedded buffer')
    if doc.get('images') or doc.get('textures') or doc.get('animations') or doc.get('skins'):errors.append('Outside static palette profile')
    if doc.get('extensionsUsed'):errors.append('Unexpected extension')
    for mm in doc.get('meshes',[]):
        gg=[]
        for p in mm['primitives']:
            prims+=1
            if p.get('mode',4)!=4 or p.get('targets'):errors.append('Not static triangles')
            ps=accessor_values(doc,blob,p['attributes']['POSITION']);ns=accessor_values(doc,blob,p['attributes']['NORMAL']);gg.extend(ps);vertices+=len(ps)
            ii=[v[0] for v in accessor_values(doc,blob,p['indices'])]
            if len(ii)%3:errors.append('index length')
            if len(ps)!=len(ns) or any(abs(math.sqrt(sum(c*c for c in n))-1)>.005 for n in ns):errors.append('nonunit normal')
            for i in range(0,len(ii),3):
                a,b,c=[ps[j] for j in ii[i:i+3]];u=[b[j]-a[j] for j in range(3)];v=[c[j]-a[j] for j in range(3)]
                cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
                area=math.sqrt(sum(x*x for x in cross))/2;areas.append(area)
                if area<1e-20:errors.append('near-zero triangle')
            tris+=len(ii)//3
        geom.append(gg)
    seen=set()
    def visit(i,mat,stack):
        if i in seen or i in stack:raise ValueError('Multiple parent or cycle')
        seen.add(i);n=doc['nodes'][i];m=matmul(mat,node_matrix(n))
        if 'mesh' in n:points.extend(transform(m,p) for p in geom[n['mesh']])
        for c in n.get('children',[]):visit(c,m,stack|{i})
    for i in doc['scenes'][doc.get('scene',0)]['nodes']:visit(i,IDENTITY,set())
    lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
    ss=source['bounds_blender_m'];exp_lo=[ss['min'][0],ss['min'][2],-ss['max'][1]];exp_hi=[ss['max'][0],ss['max'][2],-ss['min'][1]]
    delta=max(abs(a-b) for a,b in zip(lo+hi,exp_lo+exp_hi))
    if delta>1e-9:errors.append('source/export bounds differ > 1 nanometer')
    if tris!=source['triangles']:errors.append('source/export triangle mismatch')
    if abs(lo[1])>1e-9:errors.append('minimum not ground aligned')
    for m in doc['materials']:
        if m.get('alphaMode','OPAQUE')!='OPAQUE' or m.get('doubleSided',False):errors.append('nonopaque or double sided')
    if tris>40000 or prims>8 or len(doc['materials'])>6 or len(raw)>8388608:errors.append('frozen budget exceeded')
    return {'status':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warn,'sha256':hashlib.sha256(raw).hexdigest(),'semantic_sha256':semantic_digest(doc,blob),'bounds_glb_m':{'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]},'source_roundtrip_max_error_m':delta,'counts':{'triangles':tris,'primitives':prims,'materials':len(doc['materials']),'vertices':vertices,'bytes':len(raw)},'min_triangle_area_m2':min(areas),'area_threshold_m2':1e-20,'scope':'Static uncompressed embedded palette GLB; not Khronos Validator, GPU rendering, or visual acceptance.'}
