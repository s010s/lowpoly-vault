# SPDX-License-Identifier: MIT
"""Original stylized prehistoric birds. Blender 4.3.2, deterministic, static.

Run: blender -b -t 2 --python-exit-code 1 --python scripts/build_bird_pair.py -- ichthyornis
The editable semantic SOURCE collection is retained; EXPORT has four material batches.
"""
import bpy, bmesh, sys, math, json, hashlib
from pathlib import Path
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
from asset_common import setup_scene, make_material, mesh_object, export_asset, ground_asset

ROOT=Path(__file__).resolve().parents[1]
PARTS=[]
COL=None
MAT=[]

def mesh(name,vs,fs,mi=0):
    obj=mesh_object(name,vs,fs,MAT[mi],COL)
    obj['semantic_part']=name
    PARTS.append(obj)
    return obj

def loft(name,rings,mi=0,n=12,belly=None):
    # Ring records: y, z-center, horizontal radius, vertical radius.
    vs=[]
    for y,z,rx,rz in rings:
        vs += [(rx*math.sin(2*math.pi*j/n),y,z+rz*math.cos(2*math.pi*j/n)) for j in range(n)]
    fs=[tuple(range(n-1,-1,-1))]
    for k in range(len(rings)-1):
        for j in range(n): fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    fs.append(tuple((len(rings)-1)*n+j for j in range(n)))
    ob=mesh(name,vs,fs,mi)
    if belly is not None:
        ob.data.materials.append(MAT[belly])
        for p in ob.data.polygons:
            if p.center.z < 0: pass
        for k in range(len(rings)-1):
            for j in range(n):
                if math.cos(2*math.pi*(j+.5)/n)<-.16: ob.data.polygons[1+k*n+j].material_index=1
    return ob

def oval(name,center,scale,mi=0,n=12,r=6):
    cx,cy,cz=center; sx,sy,sz=scale
    vs=[(cx,cy-sy,cz)]
    for k in range(1,r):
        a=math.pi*k/r
        for j in range(n):
            b=2*math.pi*j/n
            vs.append((cx+sx*math.sin(a)*math.sin(b),cy-sy*math.cos(a),cz+sz*math.sin(a)*math.cos(b)))
    vs.append((cx,cy+sy,cz)); end=len(vs)-1
    fs=[(0,1+j,1+(j+1)%n) for j in range(n)]
    for k in range(r-2):
        for j in range(n): fs.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
    fs += [(end,1+(r-2)*n+(j+1)%n,1+(r-2)*n+j) for j in range(n)]
    return mesh(name,vs,fs,mi)

def tube(name,points,radii,mi=3,n=7):
    ps=[Vector(p) for p in points]; vs=[]
    for i,(p,r) in enumerate(zip(ps,radii)):
        d=(ps[min(i+1,len(ps)-1)]-ps[max(i-1,0)]).normalized()
        axis=Vector((0,0,1)) if abs(d.z)<.9 else Vector((1,0,0))
        u=d.cross(axis).normalized(); v=d.cross(u).normalized()
        vs += [tuple(p+r*(u*math.cos(j*2*math.pi/n)+v*math.sin(j*2*math.pi/n))) for j in range(n)]
    fs=[tuple(range(n-1,-1,-1))]
    for k in range(len(ps)-1):
        for j in range(n): fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    fs.append(tuple((len(ps)-1)*n+j for j in range(n)))
    return mesh(name,vs,fs,mi)

def feather(name,start,end,width,mi,thick=.0014,bend=.002):
    # Closed tapered feather blade, with deliberate central ridge, no alpha planes.
    a,b=Vector(start),Vector(end); d=b-a
    side=Vector((-d.y,d.x,0)).normalized()
    if side.length<.1: side=Vector((1,0,0))
    centers=[a,a+d*.25+Vector((0,0,bend)),a+d*.62+Vector((0,0,bend)),a+d*.88,b]
    widths=[width*.18,width*.85,width,width*.56,width*.025]
    vs=[]
    for c,w in zip(centers,widths):
        vs.extend([tuple(c-side*w/2),tuple(c+Vector((0,0,thick))),tuple(c+side*w/2),tuple(c-Vector((0,0,thick*.42)))])
    fs=[(3,2,1,0)]
    for k in range(4):
        for j in range(4): fs.append((4*k+j,4*k+(j+1)%4,4*(k+1)+(j+1)%4,4*(k+1)+j))
    fs.append((16,17,18,19))
    return mesh(name,vs,fs,mi)

def feet(shin_top,foot_y=-.014,spread=.027):
    for s in (-1,1):
        x=s*spread
        tube(('left' if s<0 else 'right')+'-leg',[(x,foot_y+.018,shin_top),(x,foot_y+.024,.035),(x,foot_y,.009)],[.006,.0038,.0032],3)
        for i,dx in enumerate((-.012,0,.012)):
            tube(f'foot-{s}-forward-toe-{i}',[(x,foot_y,.008),(x+dx*.6,foot_y-.013,.0043),(x+dx,foot_y-.031+(abs(dx)*.35),.0027)],[.003,.0025,.0009],3,6)
        tube(f'foot-{s}-rear-toe',[(x,foot_y+.003,.007),(x+s*.007,foot_y+.020,.003)],[.0025,.0009],3,6)

def eyes(head_y,head_z,head_x,eye_mi=3):
    for s in (-1,1):
        oval(f'eye-{s}',(s*head_x,head_y,head_z),(.0036,.0047,.0052),eye_mi,n=10,r=5)
        oval(f'eye-glint-{s}',(s*(head_x+.0028),head_y-.0012,head_z+.0018),(.0007,.00135,.00135),1,n=7,r=4)

def ichthyornis():
    loft('streamlined-torso',[(-.068,.113,.006,.010),(-.052,.110,.028,.035),(-.020,.105,.041,.045),(.024,.104,.038,.038),(.060,.106,.023,.023),(.083,.111,.005,.007)],0,14,1)
    loft('rising-neck',[(-.080,.151,.012,.014),(-.067,.143,.020,.024),(-.055,.125,.025,.029),(-.042,.112,.024,.026)],1,12)
    loft('slender-head',[(-.121,.161,.008,.010),(-.108,.164,.020,.021),(-.088,.167,.025,.025),(-.067,.166,.020,.021),(-.055,.158,.005,.008)],0,14,1)
    # Broad rear jaws taper to a small toothless tip. Closed mouth, no exposed teeth.
    loft('upper-pointed-jaw',[(-.180,.157,.0007,.0007),(-.161,.159,.004,.0037),(-.135,.160,.009,.007),(-.113,.160,.012,.009)],2,8)
    loft('lower-pointed-jaw',[(-.178,.156,.0007,.0007),(-.150,.1547,.006,.0022),(-.121,.1535,.010,.003)],2,8)
    for s in (-1,1):
        tube(f'quiet-jaw-line-{s}',[(s*.011,-.115,.156),(s*.006,-.148,.1558),(s*.0014,-.171,.1562)],[.0005,.00045,.00025],3,5)
    eyes(-.099,.174,.023)
    feet(.084)
    for i in range(7):
        x=(i-3)*.006
        feather(f'short-tail-{i}',(x*.6,.067,.111),(x*1.65,.120-abs(i-3)*.004,.107),.014,0 if i%3 else 3,thick=.0015)
    for s in (-1,1):
        # Distinct bent arm/forearm cover and overlapping feather layers.
        feather(f'wing-{s}-leading-cover',(s*.030,-.039,.129),(s*.139,.017,.157),.046,0,thick=.004,bend=.006)
        for i in range(8):
            a=(s*(.070+i*.010),-.019+i*.007,.141+i*.001)
            b=(s*(.094+i*.016),.077+i*.0025,.127-i*.0015)
            feather(f'wing-{s}-flight-{i}',a,b,.025-i*.0007,3 if i>=5 else 0,thick=.002)
        for i in range(6):
            feather(f'wing-{s}-covert-{i}',(s*(.055+i*.014),-.025+i*.007,.150+i*.001),(s*(.074+i*.015),.033+i*.006,.148),.018,0 if i<4 else 1,thick=.0018,bend=.004)

def confuciusornis():
    loft('upright-compact-torso',[(-.063,.133,.006,.009),(-.054,.125,.028,.035),(-.025,.118,.041,.050),(.016,.117,.044,.046),(.049,.122,.030,.030),(.078,.127,.006,.008)],0,14,1)
    loft('compact-neck',[(-.071,.171,.013,.019),(-.057,.159,.024,.028),(-.042,.139,.027,.034),(-.027,.127,.020,.025)],0,12,1)
    loft('rounded-head',[(-.102,.184,.006,.009),(-.088,.190,.022,.023),(-.066,.193,.029,.028),(-.045,.190,.025,.025),(-.031,.179,.008,.011)],0,14,1)
    loft('toothless-upper-beak',[(-.125,.178,.0008,.0008),(-.115,.187,.006,.007),(-.099,.188,.012,.012),(-.091,.184,.014,.011)],3,8)
    loft('toothless-lower-beak',[(-.123,.178,.0008,.0008),(-.109,.178,.008,.003),(-.093,.179,.013,.005)],3,8)
    eyes(-.081,.198,.027)
    feet(.083,foot_y=-.008,spread=.025)
    for s in (-1,1):
        # Loosely folded wing profiles, 3D volume follows shoulder to wrist.
        feather(f'folded-wing-{s}-shoulder',(s*.032,-.034,.151),(s*.057,.054,.127),.050,0,thick=.007,bend=.005)
        for i in range(6):
            feather(f'folded-wing-{s}-flight-{i}',(s*(.035+i*.0035),-.014+i*.004,.143-i*.002),(s*(.023+i*.007),.111-i*.003,.105+i*.001),.020,2 if i>1 else 0,thick=.0023,bend=.002)
        for i in range(4):
            feather(f'folded-wing-{s}-covert-{i}',(s*(.039+i*.004),-.020+i*.007,.154-i*.001),(s*(.052+i*.004),.035+i*.010,.137-i*.002),.017,0 if i<2 else 1,thick=.0022)
    for i in range(5):
        feather(f'abbreviated-tail-{i}',((i-2)*.005,.061,.126),((i-2)*.009,.125-abs(i-2)*.004,.110),.014,0,thick=.002)
    # One representative paired-streamer form; NOT a statement about every individual.
    for s in (-1,1):
        points=[(s*.010,.091,.120),(s*.016,.148,.103),(s*.022,.212,.074),(s*.033,.270,.053),(s*.042,.320,.048),(s*.047,.353,.054)]
        widths=[.004,.0045,.0048,.012,.014,.0008]
        vs=[]
        for (x,y,z),w in zip(points,widths):
            vs += [(x-w/2,y,z),(x,y,z+.0012),(x+w/2,y,z),(x,y,z-.0006)]
        fs=[(3,2,1,0)]
        for k in range(len(points)-1):
            for j in range(4):fs.append((k*4+j,k*4+(j+1)%4,(k+1)*4+(j+1)%4,(k+1)*4+j))
        fs.append(tuple((len(points)-1)*4+j for j in range(4)))
        mesh(f'paired-tail-streamer-{s}',vs,fs,2)

def preserve_and_batch(slug):
    # Keep original named parts with exact mesh/material data in an editable hidden source collection.
    src=bpy.data.collections.new('SOURCE-editable-semantic-parts');bpy.context.scene.collection.children.link(src)
    for ob in PARTS:
        cp=ob.copy(); cp.data=ob.data.copy();cp.name='SOURCE-'+ob.name;cp.parent=None;src.objects.link(cp)
    src.hide_render=True;src.hide_viewport=True
    # Batch only exported faces by material; no destructive edit of the semantic source.
    batches=[([],[]) for _ in MAT]
    for ob in list(PARTS):
        for p in ob.data.polygons:
            mi=MAT.index(ob.data.materials[p.material_index]);vs,fs=batches[mi]
            off=len(vs);vs.extend(tuple(ob.matrix_world@ob.data.vertices[i].co) for i in p.vertices)
            fs.append(tuple(range(off,off+len(p.vertices))))
        bpy.data.objects.remove(ob,do_unlink=True)
    for i,(vs,fs) in enumerate(batches):
        ob=mesh_object(slug+'-'+MAT[i].name,vs,fs,MAT[i],COL)
        # Weld same-material neighboring vertices; components remain intentionally closed overlaps.
        bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.to_mesh(ob.data);bm.free();ob.data.update()
    return src

def main():
    global COL,MAT
    args=sys.argv[sys.argv.index('--')+1:];slug=args[0]
    if slug not in ('ichthyornis','confuciusornis'):raise ValueError(slug)
    config=ROOT/'production/small-fauna-v1/remaining-20'/slug/'build-config.json'
    settings=json.loads(config.read_text());COL=setup_scene(slug,settings['seed'])
    colors=['#6C8994','#E5DCC7','#BB945C','#334650'] if slug=='ichthyornis' else ['#A56C50','#E8D6B5','#4D7977','#493F39']
    names=['plumage','warm-breast','accent','quiet-dark']
    MAT=[make_material(n,c,.8) for n,c in zip(names,colors)]
    (ichthyornis if slug=='ichthyornis' else confuciusornis)()
    ground_asset(COL)
    count=len(PARTS);src=preserve_and_batch(slug)
    metadata={
      'description':{'en':f'Original static stylized {slug.capitalize()}-inspired scene prop for an imaginative children’s world.','zh':'原创静态史前鸟类灵感场景配角，面向儿童想象世界。'},
      'quality_tier':'environment-prop','claim_scope':'stylized-inspired; not a strict scientific reconstruction',
      'static_only':True,'animation_ready':False,'surface_profile':'four original opaque palette materials; no textures',
      'source_parts':count,'editable_source_collection':src.name,
      'origin_note':'Identity root at paired-foot contact center; Blender Z up, -Y forward; meters.',
      'scale_note':settings['nominal_scale'],
      'reconstruction_notes':['Color, pose, nominal size and soft-tissue proportions are artistic.','Quiet closed mouth; no frightening teeth.','Semantic closed components overlap invisibly at shoulder, torso, feathers and leg roots to remain easy to edit.','Paired streamers represent one artistic Confuciusornis individual, not every specimen.'] if slug=='confuciusornis' else ['Color, pose, nominal size and soft-tissue proportions are artistic.','Slender jaw tapers to a small toothless tip; closed mouth intentionally does not expose rear teeth.','Semantic closed components overlap invisibly at shoulder, torso, feathers and leg roots to remain easy to edit.'],
      'generator':{'path':'scripts/build_bird_pair.py','sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(config.read_bytes()).hexdigest(),'model':'GPT-6 Astra','reasoning_effort':'xhigh'},
      'acceptance':'candidate; independent review pending','publication':'not authorized by asset generation'}
    record=export_asset(slug,{'en':'Stylized '+slug.capitalize(),'zh':'风格化 '+slug.capitalize()},'birds',COL,metadata,
      output_root=ROOT/'assets/prehistoric/birds',render=False,max_triangles=12000,max_materials=4,max_primitives=8)
    folder=ROOT/'assets/prehistoric/birds'/slug
    bpy.ops.wm.save_as_mainfile(filepath=str(folder/(slug+'.blend')),compress=True)
    record['sha256']['blend']=hashlib.sha256((folder/(slug+'.blend')).read_bytes()).hexdigest()
    (folder/'metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    print('BIRD_RESULT '+json.dumps(record))

if __name__=='__main__':main()
