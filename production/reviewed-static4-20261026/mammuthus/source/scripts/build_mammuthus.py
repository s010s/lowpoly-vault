# SPDX-License-Identifier: MIT
"""Original Mammuthus loft model. No image, mesh, scan, or other animal geometry is loaded."""
import bpy,sys,json,math,hashlib,argparse
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
import asset_common as ac
p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
col=ac.setup_scene(cfg['asset_id'],seed=cfg['seed']);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=cfg['render_threads']
bpy.context.scene.view_settings.view_transform='Standard';bpy.context.scene.view_settings.look='None';bpy.context.scene.view_settings.exposure=0;bpy.context.scene.view_settings.gamma=1
mats={k:ac.make_material(k,v,roughness=.88 if k!='ivory' else .64,double_sided=False) for k,v in cfg['palette'].items()}
measure={}
def mesh(name,v,f,mat='coat'):
    ob=ac.mesh_object(name,v,f,mats[mat] if isinstance(mat,str) else [mats[x] for x in mat],col)
    ob['anatomical_role']=name;ob['original_geometry']=True
    return ob

def ring_loft(name,rs,n=20,axis='y',mat='coat',coat=False):
    # Each section: primary axis coordinate, first center, second center, radiusA, radiusB.
    vs=[]
    for j,(u,c1,c2,r1,r2) in enumerate(rs):
        for k in range(n):
            t=2*math.pi*k/n
            A=c1+r1*math.cos(t);B=c2+r2*math.sin(t)
            if coat:
                # Broad subtle radial shaping, no random microgeometry.
                A+=.008*math.sin(k*3+j*.65)*math.cos(t)
                B+=.007*math.sin(k*3+j*.65)*math.sin(t)
                if name=='barrel-and-sloping-shoulder' and math.sin(t)<.30:
                    A+=.025*math.sin(j*1.45+k*.6)*math.cos(t)
                    B+=.018*math.sin(j*1.45+k*.6)*math.sin(t)
            vs.append((A,u,B) if axis=='y' else (A,B,u) if axis=='z' else (u,A,B))
    faces=[]
    for j in range(len(rs)-1):
        for k in range(n):faces.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    for end in [0,len(rs)-1]:
        u,c1,c2,_,_=rs[end];ci=len(vs);vs.append((c1,u,c2) if axis=='y' else (c1,c2,u) if axis=='z' else (u,c1,c2))
        for k in range(n): faces.append((ci,end*n+(k+1)%n,end*n+k) if end==0 else (ci,end*n+k,end*n+(k+1)%n))
    ob=mesh(name,vs,faces,mat)
    if coat and isinstance(mat,list):
        for poly in ob.data.polygons:
            j=poly.index//n;k=poly.index%n
            # Tonal planes follow anatomy, not checkerboard triangle noise.
            poly.material_index=1 if 1<=k<=n//2-2 and j<9 else 2 if n//2+2<=k<=n-3 else 0
    return ob

def catmull(points,steps):
    P=[Vector(x) for x in points];res=[]
    for i in range(len(P)-1):
        p0=P[max(0,i-1)];p1=P[i];p2=P[i+1];p3=P[min(len(P)-1,i+2)]
        for j in range(steps):
            t=j/steps
            res.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
    return res+[P[-1]]

def tube(name,points,radii,n=12,steps=3,mat='coat',ellipse=1):
    centers=catmull(points,steps);vs=[];rs=[];prev=None
    for i,c in enumerate(centers):
        t=i/(len(centers)-1);j=min(int(t*(len(radii)-1)),len(radii)-2);f=t*(len(radii)-1)-j;r=radii[j]*(1-f)+radii[j+1]*f;rs.append(r)
        tan=(centers[min(i+1,len(centers)-1)]-centers[max(0,i-1)]).normalized()
        if prev is None: u=tan.cross(Vector((0,0,1)) if abs(tan.z)<.9 else Vector((0,1,0))).normalized()
        else:u=(prev-tan*prev.dot(tan)).normalized()
        v=tan.cross(u).normalized();prev=u
        for k in range(n):vs.append(tuple(c+r*(u*math.cos(2*math.pi*k/n)+ellipse*v*math.sin(2*math.pi*k/n))))
    faces=[]
    for i in range(len(centers)-1):
        for k in range(n):faces.append((i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k))
    for end in [0,len(centers)-1]:
        ci=len(vs);vs.append(tuple(centers[end]))
        for k in range(n):faces.append((ci,end*n+(k+1)%n,end*n+k) if end==0 else (ci,end*n+k,end*n+(k+1)%n))
    ob=mesh(name,vs,faces,mat)
    measure[name]={'centerline_m':sum((centers[i+1]-centers[i]).length for i in range(len(centers)-1)),'centers':[list(c) for c in centers],'radii':rs}
    return ob

# Forequarter hump highest, broad ribcage, lower rump, underbelly ascends at hindquarters.
body=[(-1.31,0,1.90,.30,.39),(-1.18,0,1.91,.52,.61),(-1.00,0,1.91,.65,.76),(-.80,0,1.89,.72,.81),(-.58,0,1.84,.77,.80),(-.34,0,1.79,.80,.79),(-.08,0,1.75,.81,.78),(.19,0,1.73,.80,.77),(.46,0,1.72,.79,.74),(.72,0,1.70,.76,.70),(.96,0,1.69,.72,.65),(1.17,0,1.68,.65,.59),(1.36,0,1.66,.53,.50),(1.50,0,1.64,.35,.37),(1.57,0,1.64,.12,.18)]
ring_loft('barrel-and-sloping-shoulder',body,28,mat=['coat','mantle','shadow'],coat=True)
# Deliberate peaked domed cranium, full cheek, narrowed premaxillary face; thick neck is embedded.
head=[(-2.03,0,1.98,.18,.24),(-1.97,0,2.04,.28,.36),(-1.86,0,2.19,.36,.49),(-1.72,0,2.30,.42,.57),(-1.57,0,2.36,.46,.62),(-1.42,0,2.37,.47,.63),(-1.26,0,2.34,.47,.60),(-1.11,0,2.26,.48,.55),(-.96,0,2.17,.50,.49),(-.81,0,2.08,.49,.43)]
ring_loft('domed-head-and-neck',head,24,mat=['coat','mantle','shadow'],coat=True)
# Four single continuous columnar legs: broad high haunch to rounded grounded foot, no bead joints.
for sign,side in [(1,'right'),(-1,'left')]:
    for fore,y0 in [(True,-.83),(False,1.00)]:
        x=sign*.54;name=('fore' if fore else 'hind')+'leg-'+side
        profile=[(0,x,y0,.255,.29),(.06,x,y0,.282,.31),(.20,x,y0,.285,.305),(.39,x,y0+.01,.25,.265),(.65,x,y0+.015,.225,.24),(.91,x,y0+.015,.235,.25),(1.18,x,y0-.015,.265,.30),(1.43,x,y0-.03,.32,.36),(1.68,x*.92,y0-.03,.385,.40),(1.89,x*.85,y0-.02,.35,.37)]
        if not fore:profile=[(z,cx,cy,rx*.97,ry) for z,cx,cy,rx,ry in profile]
        ring_loft(name,profile,18,axis='z',mat=['coat','mantle','shadow'],coat=True)
        # Subdued broad nail ridge, embedded in the toe surface; no separate sharp claws.
        for j in [-1,0,1]:
            xx=x+j*.12;yy=y0-.272
            ring_loft(name+'-toenail-'+str(j),[(.035,xx,yy,.043,.022),(.09,xx,yy-.009,.048,.025),(.16,xx,yy+.008,.041,.022),(.20,xx,yy+.035,.018,.015)],8,axis='z',mat='shadow')
# One tapering proboscis, reconstructed healthy distal end (not the damaged cut fossil end).
tube('proboscis',cfg['trunk_control_points'],[.235,.225,.18,.145,.11,.088,.075,.058],n=16,steps=4,mat='coat')
# Paired upper tusks: buried proximal starts, 3D out/down/forward/up/in, no lower tusks.
for sign,side in [(1,'right'),(-1,'left')]:
    controls=[(sign*x,y,z) for x,y,z in cfg['tusk_control_points_right']]
    tube('upper-tusk-'+side,controls,[.075,.12,.105,.080,.059,.035,.009],n=14,steps=5,mat='ivory')
    # Small thick droplet ear close to head; solid, fur-colored, not elephant fan.
    ear=[(1.83,sign*.47,-1.17,.065,.07),(1.94,sign*.54,-1.17,.105,.13),(2.10,sign*.57,-1.20,.12,.17),(2.28,sign*.54,-1.22,.105,.16),(2.42,sign*.48,-1.24,.07,.11),(2.48,sign*.44,-1.23,.035,.05)]
    ring_loft('small-ear-'+side,ear,14,axis='z',mat='shadow')
    # tiny embedded ellipsoid eye on lateral front cheek.
    ring_loft('eye-'+side,[(sign*.393,-1.71,2.40,.045,.04),(sign*.426,-1.71,2.40,.053,.047),(sign*.447,-1.71,2.40,.035,.033)],12,axis='x',mat='eye')
# Tail avoids long elephant whip. Root embedded in rump; slender shaft with discreet fur tuft.
tube('short-tail',[(0,1.45,1.94),(.03,1.64,1.73),(.07,1.70,1.46),(.10,1.73,1.23),(.10,1.72,1.09)],[.075,.065,.05,.035,.024],10,3,'shadow')
tube('tail-terminal-hair',[(.10,1.73,1.22),(.11,1.74,1.10),(.10,1.72,.99)],[.06,.07,.022],10,2,'coat')
# Coat locks: broad solid six-sided shingled forms with overlapping roots, not floating hair cones.
# Consolidate by side into editable semantic mesh; each strand starts inside barrel skin.
for sign,side in [(1,'right'),(-1,'left')]:
    vs=[];fs=[]
    for j,y in enumerate([-.95,-.74,-.51,-.26,0,.26,.52,.77,1.00,1.20]):
        seg=next(i for i in range(len(body)-1) if body[i][0]<=y<=body[i+1][0])
        q=(y-body[seg][0])/(body[seg+1][0]-body[seg][0])
        _,_,cz,rx,rz=[body[seg][i]*(1-q)+body[seg+1][i]*q for i in range(5)]
        def surf(z):return rx*math.sqrt(max(.02,1-((z-cz)/rz)**2))
        z0=cz+.12;z1=cz-.22;z2=cz-rz*.78;z3=cz-rz-.07-(.04 if j%3==0 else 0)
        width=.17 if j%2 else .19
        controls=[(sign*(surf(z0)-.09),y,z0),(sign*(surf(z1)-.025),y+.025,z1),(sign*(surf(z2)-.01),y+.065,z2),(sign*.18,y+.085,z3)]
        radii=[(width,.075),(width*.94,.07),(width*.70,.065),(width*.28,.035)]
        off=len(vs)
        for (x,cy,z),(ry,rx) in zip(controls,radii):
            for k in range(6):
                t=math.tau*k/6;vs.append((x+rx*math.cos(t),cy+ry*math.sin(t),z))
        for k in range(6):
            fs.extend([(off+seg*6+k,off+seg*6+(k+1)%6,off+(seg+1)*6+(k+1)%6,off+(seg+1)*6+k) for seg in range(3)])
        fs.append(tuple(off+k for k in reversed(range(6))));fs.append(tuple(off+18+k for k in range(6)))
    mesh('shaggy-flank-locks-'+side,vs,fs,'coat')
# Short throat fringe overlaps neck and chest rather than detached beard plates.
for sign,side in [(1,'right'),(-1,'left')]:
    tube('cheek-coat-'+side,[(sign*.28,-1.64,1.90),(sign*.31,-1.55,1.73),(sign*.25,-1.47,1.61)],[.15,.14,.075],10,3,'shadow',ellipse=.65)
# r002/D01: bury only coat top-cap loops against the actual faceted barrel, not an ideal ellipse.
# Every other vertex, part, material and contact datum remains as r001.
body_obj=bpy.data.objects['barrel-and-sloping-shoulder'];body_obj.data.calc_loop_triangles()
body_tree=BVHTree.FromPolygons([v.co.copy() for v in body_obj.data.vertices],[tuple(t.vertices) for t in body_obj.data.loop_triangles],all_triangles=True)
coat_root_changes=[]
for sign,side in [(1,'right'),(-1,'left')]:
    ob=bpy.data.objects['shaggy-flank-locks-'+side]
    for lock in range(10):
        # Translate the intact six-point cap, never independently clip vertices.
        # Independent clipping can collapse opposite hexagon points onto the same facet.
        loop=[ob.data.vertices[lock*24+k] for k in range(6)];hits=[];required=0.0
        for vertex in loop:
            p=vertex.co;hit,normal,face,distance=body_tree.ray_cast(Vector((sign*3,p.y,p.z)),Vector((-sign,0,0)),6)
            if hit is None:raise RuntimeError('Coat root missed actual faceted body surface')
            hits.append(tuple(hit));required=max(required,sign*p.x-sign*hit.x+cfg['coat_root_min_inset_m'])
        for vertex,hit in zip(loop,hits):
            p=vertex.co;before=tuple(p);p.x-=sign*required
            if tuple(p)!=before:coat_root_changes.append({'part':ob.name,'vertex':vertex.index,'before':before,'after':tuple(p),'surface_hit':hit,'intact_loop_inward_translation_m':required})
    ob.data.update()
    # New local surface normals, same closed topology, no culling tricks.
    import bmesh
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
# Center the actual four-foot contact rectangle on the identity root; preserve meter scale.
datum_shift=cfg['footprint_datum_shift_y_m']
for ob in col.all_objects:
    if ob.type=='MESH':
        for vertex in ob.data.vertices:vertex.co.y+=datum_shift
        ob.data.update()
for row in measure.values():
    for center in row['centers']:center[1]+=datum_shift
# Built-in helper is intentionally unmodified, including default area threshold.
meta={'description':{'en':'Original adult woolly mammoth-inspired reconstruction, with domed head, sloping high shoulders, small ears and paired three-dimensional recurved upper tusks.','zh':'原创成年真猛犸象启发重建：穹顶头、高肩斜背、小耳及双侧立体弯曲上门齿。'},'generator':'scripts/build_mammuthus.py','variant':'Mammuthus primigenius-inspired adult; artistic composite','source_claim':'Consulted-only museum photograph and carcass paper; no incorporated reference pixels or geometry.','scientific_limits':json.loads((Path(__file__).resolve().parents[1]/'brief.json').read_text())['scientific_limits'],'origin_detail':'Center of four-foot footprint, Z=0 contact plane','config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
rec=ac.export_asset('mammuthus',{'en':'Woolly mammoth','zh':'猛犸象'},'animals',col,metadata=meta,output_root=out,render=False,max_triangles=12000,max_materials=8,max_primitives=48,diagnostics=False)
root=out/'mammuthus'
(root/'coat-root-changes.json').write_text(json.dumps({'defect':'MAM-R001-D01','minimum_inset_m':cfg['coat_root_min_inset_m'],'changes':coat_root_changes,'only_top_cap_loop_vertices_modified':True},indent=2))
(root/'centerline-measurements.json').write_text(json.dumps(measure,indent=2))
(root/'build-observation.json').write_text(json.dumps({'factory_startup':True,'complete_procedural_build':True,'generator_sha256':meta['generator_sha256'],'config_sha256':meta['config_sha256'],'blender_version':bpy.app.version_string,'exporter_version':bpy.context.preferences.addons.get('io_scene_gltf2').module if bpy.context.preferences.addons.get('io_scene_gltf2') else 'builtin glTF RNA probed by helper','render_threads':2,'export_root':{'name':bpy.data.objects[col['asset_root']].name,'identity':True},'no_external_mesh_loaded':True},indent=2))
print('MAMMUTHUS_BUILD_COMPLETE',root,rec['triangles'],rec['sha256']['glb'],flush=True)
