"""Independent GLB decode, world-transform, welded topology, and exact revision differential.
No maker config, measurement report, or generator is imported.
Welding is exact-coordinate only: no numeric acceptance tolerance.
"""
import json, struct, math, hashlib, collections, datetime
from pathlib import Path
import numpy as np
ROOT=Path('/workspace/shared/lowpoly-batch89-skolithos-repair-20261020')
OUT=Path('/workspace/shared/lowpoly-skolithos-r002-independent-qa-20261020')
BASE=ROOT/'production/small-life-batch89/skolithos-pipe-field'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(p):
    b=p.read_bytes(); magic,ver,total=struct.unpack_from('<4sII',b); assert magic==b'glTF' and ver==2 and total==len(b)
    n,kind=struct.unpack_from('<II',b,12);assert kind==0x4e4f534a
    doc=json.loads(b[20:20+n]);n2,kind2=struct.unpack_from('<II',b,20+n);assert kind2==0x004e4942
    binary=b[28+n:28+n+n2]
    def accessor(ai):
        a=doc['accessors'][ai];assert 'sparse' not in a and not a.get('normalized');v=doc['bufferViews'][a['bufferView']]
        codes={5121:'B',5123:'H',5125:'I',5126:'f'}; dims={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
        fmt='<'+codes[a['componentType']]*dims[a['type']]; width=struct.calcsize(fmt);stride=v.get('byteStride',width);start=v.get('byteOffset',0)+a.get('byteOffset',0)
        return [struct.unpack_from(fmt,binary,start+i*stride) for i in range(a['count'])]
    def transform(node):
        if 'matrix' in node:return np.array(node['matrix'],dtype=float).reshape((4,4),order='F')
        x,y,z,w=node.get('rotation',[0,0,0,1]);r=np.array([[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],[2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],[2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]])
        m=np.eye(4);m[:3,:3]=r@np.diag(node.get('scale',[1,1,1]));m[:3,3]=node.get('translation',[0,0,0]);return m
    components=[];transforms=[];primitives=[]
    def visit(ni,parent):
        node=doc['nodes'][ni];world=parent@transform(node);transforms.append({'node':ni,'name':node.get('name'),'world_matrix_row_major':world.tolist()})
        if 'mesh' in node:
            for pi,pr in enumerate(doc['meshes'][node['mesh']]['primitives']):
                assert pr.get('mode',4)==4
                local=accessor(pr['attributes']['POSITION']);points=[tuple((world@np.array([*v,1.]))[:3]) for v in local]
                ind=[x[0] for x in accessor(pr['indices'])] if 'indices' in pr else list(range(len(points)))
                unique=list(dict.fromkeys(points));lookup={p:i for i,p in enumerate(unique)};vmap=[lookup[p] for p in points];tri=[tuple(vmap[j] for j in ind[i:i+3]) for i in range(0,len(ind),3)]
                adjacency=[set() for p in unique]
                for face in tri:
                    for a,b in zip(face,face[1:]+face[:1]):adjacency[a].add(b);adjacency[b].add(a)
                unseen=set(range(len(unique)))
                while unseen:
                    seed=min(unseen);unseen.remove(seed);ids={seed};stack=[seed]
                    while stack:
                        for v in adjacency[stack.pop()]:
                            if v in unseen: unseen.remove(v);ids.add(v);stack.append(v)
                    coords=[unique[i] for i in sorted(ids)];faces=[f for f in tri if f[0] in ids];edges=collections.Counter(tuple(sorted((a,b))) for f in faces for a,b in zip(f,f[1:]+f[:1]))
                    lo=[min(v[j] for v in coords) for j in range(3)];hi=[max(v[j] for v in coords) for j in range(3)]
                    c={'node':ni,'primitive':pi,'material':pr.get('material'),'vertices':len(coords),'triangles':len(faces),'bounds':{'min':lo,'max':hi},'boundary_edges':sum(v==1 for v in edges.values()),'nonmanifold_edges':sum(v!=2 for v in edges.values()),'world_vertices':sorted(coords)}
                    if len(coords)==24:
                        levels=sorted({v[1] for v in coords});assert len(levels)==2
                        rings=[]
                        for y in levels:
                            ring=[v for v in coords if v[1]==y];assert len(ring)==12
                            cx=(min(v[0] for v in ring)+max(v[0] for v in ring))/2;cz=(min(v[2] for v in ring)+max(v[2] for v in ring))/2
                            radius=[math.hypot(v[0]-cx,v[2]-cz) for v in ring]
                            # Independent least-squares circumcircle corroboration, not acceptance tolerance.
                            xy=np.array([[v[0]-cx,v[2]-cz] for v in ring]);A=np.c_[2*xy,np.ones(12)];sol=np.linalg.lstsq(A,(xy*xy).sum(axis=1),rcond=None)[0]
                            rings.append({'y_m':y,'vertex_count':12,'center_xz_m':[cx,cz],'circumradius_min_m':min(radius),'circumradius_max_m':max(radius),'circumcircle_fit_radius_m':float(math.sqrt(sol[2]+sol[0]**2+sol[1]**2)),'strict_range_pass':all(.0026<=r<=.0048 for r in radius),'radii_m':radius})
                        c['rings']=rings;c['constant_section']=sorted((v[0],v[2]) for v in coords if v[1]==levels[0])==sorted((v[0],v[2]) for v in coords if v[1]==levels[1])
                    components.append(c)
                primitives.append({'node':ni,'primitive':pi,'position_vertices':len(points),'triangles':len(ind)//3,'world_vertices_in_export_order':points,'indices':ind})
        for child in node.get('children',[]):visit(child,world)
    for n in doc['scenes'][doc.get('scene',0)]['nodes']:visit(n,np.eye(4))
    return {'path':str(p),'sha256':sha(p),'bytes':len(b),'transforms':transforms,'materials':doc.get('materials',[]),'textures':len(doc.get('textures',[])),'components':components,'primitives':primitives}
old=decode(BASE/'r001/artifacts/skolithos-pipe-field.glb');new=decode(BASE/'r002/artifacts/skolithos-pipe-field.glb')
diff=[]
for a,b in zip(old['components'],new['components']):
    # Deterministic topology order is independently verified below by primitive indices.
    aa=a['world_vertices'];bb=b['world_vertices'];changed=[(x,y) for x,y in zip(aa,bb) if x!=y]
    diff.append({'component':len(diff),'is_shaft':'rings' in b,'world_vertices_identical':aa==bb,'changed_vertex_count':len(changed),'max_displacement_m':max((math.dist(x,y) for x,y in changed),default=0),'old_ring_radii':[r['circumradius_min_m'] for r in a.get('rings',[])],'new_ring_radii':[r['circumradius_min_m'] for r in b.get('rings',[])]})
assert all(a['indices']==b['indices'] for a,b in zip(old['primitives'],new['primitives']))
assert old['transforms']==new['transforms'] and old['materials']==new['materials']
shafts=[c for c in new['components'] if 'rings' in c];assert len(shafts)==7 and len(new['components'])==8
all_r=[v for c in shafts for r in c['rings'] for v in r['radii_m']]
summary={'schema_version':1,'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Independent binary/accessor decoder; all scene parent/local transforms; exact position weld; face connectivity; each 12-vertex top and bottom ring measured in world XZ; radial extrema and independent fitted circumcircle. No maker config or maker measurement input.','acceptance_tolerance_m':0,'original_frozen_range_m':[.0026,.0048],'new_minimum_radius_m':min(all_r),'new_maximum_radius_m':max(all_r),'all_168_radial_samples_in_range':all(.0026<=v<=.0048 for v in all_r),'shaft_count':len(shafts),'constant_sections':all(c['constant_section'] for c in shafts),'all_components_closed':all(c['nonmanifold_edges']==0 for c in new['components']),'topology_indices_unchanged':True,'transforms_materials_unchanged':True,'differential':diff,'old':old,'new':new}
(OUT/'own-world-geometry-differential.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['old','new']},indent=2))
