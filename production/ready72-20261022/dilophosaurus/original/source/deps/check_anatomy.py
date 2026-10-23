# SPDX-License-Identifier: MIT
"""Hash-bound source geometry and actual exported position-soup audit. Not visual acceptance."""
import sys,json,hashlib,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy,bmesh
from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform
args=sys.argv[sys.argv.index('--')+1:]; root=Path(args[0]); output=Path(args[1]);
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(root/'model.blend'))
objects=[o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH']
checks={}; details=[]; source_triangles=[]
def tri_key(tri): return tuple(sorted(tuple(round(float(x),5) for x in p) for p in tri))
for ob in objects:
    bm=bmesh.new();bm.from_mesh(ob.data)
    details.append({'name':ob.name,'signed_volume_m3':bm.calc_volume(signed=True),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)})
    bm.free();ob.data.calc_loop_triangles()
    for t in ob.data.loop_triangles:
        tri=[]
        for i in t.vertices:
            v=ob.matrix_world@ob.data.vertices[i].co;tri.append((v.x,v.z,-v.y))
        source_triangles.append(tri_key(tri))
checks['closed_positive_semantic_parts']=all(d['boundary_edges']==0 and d['nonmanifold_edges']==0 and d['signed_volume_m3']>0 for d in details)
checks['no_preview_stage_in_source']=not any(o.type in ('LIGHT','CAMERA') or o.name.startswith('_preview') for o in bpy.context.scene.objects)
checks['manual_digits_each_hand']=all(len([o for o in objects if o.name.startswith('14_Manus_'+side+'_Major_Digit_')])==3 for side in ('L','R'))
checks['fourth_digit_is_reduced']=True
manual={}
for side in ('L','R'):
    main=[o for o in objects if o.name.startswith('14_Manus_'+side+'_Major_Digit_')]
    nub=[o for o in objects if o.name=='16_Manus_'+side+'_Reduced_Digit_IV_Nub']
    def span(ob): return max(v.co.y for v in ob.data.vertices)-min(v.co.y for v in ob.data.vertices)
    manual[side]={'main_digit_count':len(main),'reduced_IV_count':len(nub),'main_digit_lengths_y_m':[span(o) for o in main],'reduced_IV_length_y_m':span(nub[0]) if len(nub)==1 else None}
    checks['fourth_digit_is_reduced'] &= len(nub)==1 and span(nub[0])<.4*min(span(o) for o in main)
checks['three_major_forward_toes_each_foot']=all(len([o for o in objects if o.name.startswith('10_Pes_'+side+'_Digit_')])==3 for side in ('L','R'))
feet={side:min(v.co.z for o in objects if o.name.startswith(('10_Pes_'+side,'11_Pes_'+side)) for v in o.data.vertices) for side in ('L','R')}
checks['both_feet_at_floor']=all(abs(z)<1e-6 for z in feet.values())
crests=[o for o in objects if o.name.startswith('05_Separate_Nasolacrimal_Crest_')]
left=next(o for o in crests if o.name.endswith('L'));right=next(o for o in crests if o.name.endswith('R'))
gap=min(v.co.x for v in right.data.vertices)-max(v.co.x for v in left.data.vertices)
checks['two_separate_longitudinal_crests']=len(crests)==2 and gap>.15
# Decode the delivered GLB and compare triangle positions to the editable source.
doc,binary,_=read_glb(root/'model.glb');exported=[];I=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
def visit(i,parent):
    node=doc['nodes'][i];world=matmul(parent,node_matrix(node))
    if 'mesh' in node:
        for primitive in doc['meshes'][node['mesh']]['primitives']:
            vertices=accessor_values(doc,binary,primitive['attributes']['POSITION']);indices=accessor_values(doc,binary,primitive['indices'])
            flat=[int(x[0] if isinstance(x,(list,tuple)) else x) for x in indices]
            for j in range(0,len(flat),3): exported.append(tri_key([transform(world,vertices[k]) for k in flat[j:j+3]]))
    for child in node.get('children',[]): visit(child,world)
for i in doc['scenes'][doc.get('scene',0)]['nodes']:visit(i,I)
checks['source_export_full_triangle_position_soup_match_1e_5_m']=sorted(source_triangles)==sorted(exported)
result={'status':'PASS' if all(checks.values()) else 'FAIL','claim_scope':'Maker executed measurable geometric obligations only, not scientific or visual independent acceptance. Overlapping anatomical solids are intentional; this does not claim a boolean watertight union.','glb_sha256':sha(root/'model.glb'),'blend_sha256':sha(root/'model.blend'),'checker_sha256':sha(__file__),'checks':checks,'crest_gap_m':gap,'feet_min_z_m':feet,'manual_digits':manual,'source_triangles':len(source_triangles),'export_triangles':len(exported),'semantic_parts':details}
output.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({'status':result['status'],'checks':checks}));
if not all(checks.values()):raise RuntimeError('Geometry obligation failed')
