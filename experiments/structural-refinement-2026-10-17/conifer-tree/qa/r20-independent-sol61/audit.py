"""Independent read-only r19/r20 audit; output only into this new QA directory."""
import hashlib, json, math, struct
from pathlib import Path
from PIL import Image, ImageChops

Q = Path(__file__).resolve().parent
ROOT = Q.parent.parent
OLD, NEW = ROOT / 'candidate-r19', ROOT / 'candidate-r20'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def glb(p):
    d = p.read_bytes()
    assert struct.unpack_from('<III', d) == (0x46546c67, 2, len(d))
    n, kind = struct.unpack_from('<II', d, 12)
    assert kind == 0x4e4f534a
    g = json.loads(d[20:20+n])
    size, kind = struct.unpack_from('<II', d, 20+n)
    assert kind == 0x004e4942
    return g, d[28+n:28+n+size]

def accessor(g, b, i):
    a = g['accessors'][i]; v = g['bufferViews'][a['bufferView']]
    assert not a.get('sparse') and v['buffer'] == 0
    fmt = {5122:'h', 5123:'H', 5126:'f'}[a['componentType']]
    width = {'SCALAR':1, 'VEC3':3}[a['type']]
    step = struct.calcsize('<'+fmt*width)
    stride = v.get('byteStride', step)
    offset = v.get('byteOffset', 0) + a.get('byteOffset', 0)
    raw = [b[offset+k*stride:offset+k*stride+step] for k in range(a['count'])]
    values = [struct.unpack('<'+fmt*width, r) for r in raw]
    return a, v, raw, values

g0,b0 = glb(OLD/'conifer-tree.glb'); g1,b1 = glb(NEW/'conifer-tree.glb')
pr0 = [p for m in g0['meshes'] for p in m['primitives']]
pr1 = [p for m in g1['meshes'] for p in m['primitives']]
assert len(pr0) == len(pr1) == 3
exact = {k:g0.get(k)==g1.get(k) for k in ['asset','materials','nodes','scenes','scene','meshes']}
angles=[]; lengths=[]; component_errors=[]; rows=[]
for index,(p0,p1) in enumerate(zip(pr0,pr1)):
    checks={}
    for name in ['POSITION','indices']:
        i0 = p0['indices'] if name=='indices' else p0['attributes'][name]
        i1 = p1['indices'] if name=='indices' else p1['attributes'][name]
        a0,v0,r0,x0 = accessor(g0,b0,i0); a1,v1,r1,x1 = accessor(g1,b1,i1)
        checks[name+'_bytes_exact'] = r0==r1
        checks[name+'_accessor_exact'] = a0==a1
    a0,v0,r0,x0 = accessor(g0,b0,p0['attributes']['NORMAL'])
    a1,v1,r1,x1 = accessor(g1,b1,p1['attributes']['NORMAL'])
    offset=v1.get('byteOffset',0)+a1.get('byteOffset',0)
    assert a0['componentType']==5126 and a1['componentType']==5122
    assert a1['type']=='VEC3' and a1['normalized'] is True
    assert v1['byteStride']==8 and offset%4==0 and len(x0)==len(x1)
    local=[]
    for old,packed in zip(x0,x1):
        decoded=tuple(max(c/32767.0,-1.0) for c in packed)
        component_errors.extend(abs(a-b) for a,b in zip(old,decoded))
        norm=math.sqrt(sum(x*x for x in decoded)); lengths.append(abs(norm-1))
        dot=sum(a*b for a,b in zip(old,decoded))
        cross=(old[1]*decoded[2]-old[2]*decoded[1],old[2]*decoded[0]-old[0]*decoded[2],old[0]*decoded[1]-old[1]*decoded[0])
        angle=math.degrees(math.atan2(math.sqrt(sum(x*x for x in cross)),dot))
        angles.append(angle);local.append(angle)
    rows.append({'primitive':index,**checks,'normal_count':len(x1),'normal_component_type':5122,'normalized':True,'stride':8,'offset_aligned_4':True,'max_angle_deg':max(local)})

images=[]; pixels=[]
for newdir,olddir in [('detail512','pilot512'),('native128','pilot128')]:
    for p in sorted((NEW/'evidence'/newdir).glob('*.png')):
        old=OLD/'evidence'/olddir/p.name
        aa=Image.open(old).convert('RGB');bb=Image.open(p).convert('RGB')
        assert aa.size==bb.size
        diff=ImageChops.difference(aa,bb);hist=diff.histogram()
        changed=sum(a!=b for a,b in zip(aa.getdata(),bb.getdata()))
        total=aa.width*aa.height*3
        abs_sum=sum((i%256)*n for i,n in enumerate(hist))
        sq_sum=sum((i%256)**2*n for i,n in enumerate(hist))
        pixels.append({'path':str(p.relative_to(NEW)),'source_sha256':H(old),'candidate_sha256':H(p),'changed_pixels':changed,'changed_fraction':changed/(aa.width*aa.height),'max_channel_difference':max(x[1] for x in diff.getextrema()),'mean_abs_channel_difference':abs_sum/total,'rmse':math.sqrt(sq_sum/total),'exact_pixels':aa.tobytes()==bb.tobytes()})
for sub in ['full-angle256','detail512','native128']:
    for p in sorted((NEW/'evidence'/sub).glob('*.png')):
        im=Image.open(p)
        images.append({'path':str(p.relative_to(NEW)),'sha256':H(p),'size':list(im.size),'opened_pixels':True})
assert len(images)==53
freeze=json.loads((NEW/'freeze.json').read_text())
mismatch=[name for name,value in freeze['files'].items() if not (NEW/name).is_file() or H(NEW/name)!=value['sha256']]
rebuild=NEW/'rebuild-runs/local-rebuild-01/outputs/conifer-tree/conifer-tree.glb'
canonical=NEW/'rebuild-runs/local-rebuild-01/outputs/canonical-export/conifer-tree.glb'
result={'reviewed_commit':'265b47eed899307228d609355cc46c6d6992f61d','source_sha256':H(OLD/'conifer-tree.glb'),'candidate_sha256':H(NEW/'conifer-tree.glb'),'source_bytes':(OLD/'conifer-tree.glb').stat().st_size,'candidate_bytes':(NEW/'conifer-tree.glb').stat().st_size,'exact_json_checks':exact,'primitive_checks':rows,'normal_error':{'max_angle_deg':max(angles),'mean_angle_deg':sum(angles)/len(angles),'p99_nearest_rank_deg':sorted(angles)[math.ceil(.99*len(angles))-1],'max_component_abs':max(component_errors),'max_unit_length_abs':max(lengths)},'extensionsUsed':g1.get('extensionsUsed'),'extensionsRequired':g1.get('extensionsRequired'),'freeze_files_checked':len(freeze['files']),'freeze_mismatches':mismatch,'existing_rebuild_bytes_equal':H(rebuild)==H(NEW/'conifer-tree.glb'),'existing_canonical_bytes_equal_r19':H(canonical)==H(OLD/'conifer-tree.glb'),'independent_rebuild_executed':False,'pixel_comparisons':pixels,'opened_raw_images':images,'gpu_scene':'not_run; separate task required'}
(Q/'audit-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['pixel_comparisons','opened_raw_images']},indent=2))
print('Pixel rows:',json.dumps(pixels,indent=2))
