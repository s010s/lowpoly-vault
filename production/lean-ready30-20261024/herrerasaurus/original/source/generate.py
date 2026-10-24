# SPDX-License-Identifier: MIT
"""Original Herrerasaurus living reconstruction. Run with Blender background Python.

Usage: blender -b -t 2 --python source/generate.py -- --output . --stage final
All geometry is authored in meters with -Y forward and +Z up.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE / 'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, _bounds, _vertices_world, _look_at
from qa_glb import audit_glb

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p, d): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

class Part:
    def __init__(self,name): self.name=name; self.v=[]; self.f=[]; self.m=[]
    def loft(self, rows, n=12, mat=0, region=False):
        """Parallel transverse frames, non-uniform anatomical sections, closed ends."""
        base=len(self.v); pts=[Vector(r[:3]) for r in rows]
        for i,r in enumerate(rows):
            tangent=(pts[min(i+1,len(rows)-1)]-pts[max(0,i-1)]).normalized()
            axis=Vector((1,0,0)); u=(axis-tangent*axis.dot(tangent)).normalized(); v=tangent.cross(u).normalized()
            # Longitudinal ring seam is at the dorsal side when the path runs forward.
            for j in range(n):
                a=2*math.pi*j/n
                self.v.append(tuple(pts[i]+u*(r[3]*math.cos(a))+v*(r[4]*math.sin(a))))
        for i in range(len(rows)-1):
            for j in range(n):
                self.f.append((base+i*n+j,base+i*n+(j+1)%n,base+(i+1)*n+(j+1)%n,base+(i+1)*n+j))
                if region:
                    z=sum(self.v[k][2] for k in self.f[-1])/4
                    zc=(pts[i].z+pts[i+1].z)/2; rmax=(rows[i][4]+rows[i+1][4])/2
                    self.m.append(0 if z>zc+rmax*.40 else 2 if z<zc-rmax*.38 else 1)
                else: self.m.append(mat)
        self.f.append(tuple(base+j for j in reversed(range(n))));self.m.append(mat)
        self.f.append(tuple(base+(len(rows)-1)*n+j for j in range(n)));self.m.append(mat)
        return self
    def ellipsoid(self,c,s,n=10,rings=6,mat=0):
        # Deliberate polar fan avoids coincident polar-ring vertices.
        base=len(self.v);self.v.append((c[0],c[1],c[2]+s[2]))
        for i in range(1,rings):
            a=math.pi*i/rings
            for j in range(n):
                b=2*math.pi*j/n;self.v.append((c[0]+s[0]*math.sin(a)*math.cos(b),c[1]+s[1]*math.sin(a)*math.sin(b),c[2]+s[2]*math.cos(a)))
        bot=len(self.v);self.v.append((c[0],c[1],c[2]-s[2]))
        for j in range(n): self.f.append((base,base+1+j,base+1+(j+1)%n));self.m.append(mat)
        for i in range(rings-2):
            for j in range(n):
                a=base+1+i*n+j;b=base+1+i*n+(j+1)%n
                self.f.append((a,b,b+n,a+n));self.m.append(mat)
        for j in range(n): self.f.append((bot,base+1+(rings-2)*n+(j+1)%n,base+1+(rings-2)*n+j));self.m.append(mat)
    def finish(self,mats):
        ob=mesh_object(self.name,self.v,self.f,mats,C)
        for p,m in zip(ob.data.polygons,self.m):p.material_index=m
        ob['anatomical_part']=self.name
        return ob

def build(detail):
    global C
    C=setup_scene('herrerasaurus', P['seed'])
    bpy.context.scene['reconstruction_scope']='Original living reconstruction; not specimen-exact. Skin/color inferred.'
    M={k:make_material('herrerasaurus-'+k,v,roughness=.86 if k!='eye' else .62) for k,v in P['palette'].items()}
    skin=[M['dorsal'],M['flank'],M['belly']]
    Part('axial-body-deep-pelvis-compact-neck').loft([
        (0,.40,.89,.125,.145),(0,.25,.885,.190,.240),(0,.06,.875,.209,.265),
        (0,-.14,.89,.201,.225),(0,-.33,.93,.175,.196),(0,-.49,.97,.135,.160),
        (0,-.61,1.035,.102,.130),(0,-.69,1.125,.085,.108),(0,-.78,1.16,.074,.085),
        (0,-.865,1.158,.076,.070)],16,region=True).finish(skin)
    Part('long-counterbalance-tail').loft([
        (0,.32,.90,.148,.160),(0,.51,.91,.127,.135),(.005,.72,.94,.102,.105),
        (.014,.98,.987,.070,.069),(.025,1.24,1.027,.045,.044),(.034,1.47,1.053,.026,.025),
        (.045,1.67,1.068,.012,.013),(.05,1.80,1.075,.003,.004)],12,region=True).finish(skin)
    Part('elongate-skull-upper').loft([
        (0,-.80,1.176,.061,.065),(0,-.855,1.188,.086,.082),(0,-.94,1.189,.090,.081),
        (0,-1.035,1.183,.074,.068),(0,-1.13,1.17,.061,.052),(0,-1.20,1.159,.047,.036)],12,region=True).finish(skin)
    Part('mandible').loft([
        (0,-.825,1.112,.065,.041),(0,-.90,1.079,.073,.036),(0,-1.015,1.075,.062,.026),
        (0,-1.12,1.085,.049,.021),(0,-1.195,1.104,.040,.014)],10,mat=1).finish(skin)
    Part('closed-mouth-cavity').loft([(0,-.85,1.118,.057,.025),(0,-.99,1.114,.06,.026),(0,-1.17,1.126,.037,.013)],10).finish([M['mouth']])
    claws=Part('keratin-hand-and-foot-claws'); digits=Part('grasping-digit-cores'); feet=Part('pedal-digits'); reduced=Part('reduced-outer-manual-digits')
    for sign,label in [(-1,'left'),(1,'right')]:
        s=sign; yoff=.035 if s<0 else -.035
        Part(label+'-hip-to-knee').loft([(s*.142,.095,.88,.113,.16),(s*.198,.015,.76,.115,.142),
            (s*.232,-.12,.61,.086,.10),(s*.236,-.20,.535,.060,.065)],12,mat=1).finish(skin)
        Part(label+'-shin-to-ankle').loft([(s*.235,-.195,.55,.056,.063),(s*.244,-.13,.45,.052,.055),
            (s*.249,-.015,.29,.038,.043),(s*.252,.055+yoff,.16,.030,.033)],10,mat=1).finish(skin)
        Part(label+'-metatarsus').loft([(s*.252,.06+yoff,.17,.030,.032),(s*.25,.02+yoff,.085,.028,.031),
            (s*.25,-.025+yoff,.045,.041,.035)],10,mat=1).finish(skin)
        for k in range(3):
            x=s*(.25+(k-1)*.040);endy=-.27+yoff+(abs(k-1)*.045)
            feet.loft([(s*.25,-.025+yoff,.046,.022,.024),(x,-.10+yoff,.032,.020,.022),
                (x+s*(k-1)*.012,endy+.04,.025,.014,.018)],8)
            claws.loft([(x+s*(k-1)*.012,endy+.045,.025,.015,.019),(x+s*(k-1)*.015,endy,.017,.010,.011),(x+s*(k-1)*.016,endy-.035,.007,.0015,.0015)],8)
        feet.loft([(s*.25,.005+yoff,.068,.015,.018),(s*.216,.105+yoff,.041,.010,.011)],8)
        claws.loft([(s*.216,.105+yoff,.041,.011,.012),(s*.211,.138+yoff,.027,.0015,.002)],8)
        Part(label+'-brachium').loft([(s*.138,-.45,.94,.061,.07),(s*.193,-.435,.845,.053,.058),
            (s*.235,-.39,.735,.040,.044),(s*.246,-.41,.692,.033,.037)],10,mat=1).finish(skin)
        Part(label+'-forearm').loft([(s*.242,-.404,.706,.035,.039),(s*.266,-.513,.69,.033,.034),
            (s*.281,-.634,.684,.025,.028)],10,mat=1).finish(skin)
        Part(label+'-inward-facing-palm').loft([(s*.281,-.62,.681,.026,.034),(s*.286,-.71,.667,.029,.064),
            (s*.288,-.772,.647,.023,.058)],10,mat=1).finish(skin)
        for k,rows in enumerate([
            [(s*.289,-.744,.704,.022,.023),(s*.292,-.825,.702,.019,.020),(s*.286,-.888,.671,.015,.017)],
            [(s*.291,-.774,.654,.022,.024),(s*.299,-.865,.626,.019,.021),(s*.293,-.918,.566,.014,.016)],
            [(s*.288,-.751,.603,.019,.020),(s*.292,-.821,.557,.016,.018),(s*.286,-.857,.502,.012,.014)]
        ]):
            digits.loft(rows,9)
            a=rows[-1]
            claws.loft([a,(a[0]-s*.013,a[1]-.025,a[2]-.032,.011,.012),(a[0]-s*.030,a[1]-.018,a[2]-.057,.0015,.002)],8)
        for k in range(2):
            reduced.loft([(s*.283,-.722+k*.014,.604-k*.028,.013,.014),(s*.279,-.747+k*.014,.575-k*.027,.010,.011),(s*.277,-.752+k*.014,.562-k*.027,.004,.005)],8)
    digits.finish([M['flank']]);feet.finish([M['flank']]);reduced.finish([M['flank']]);claws.finish([M['claw']])
    if detail:
        eyes=Part('paired-amber-eyes');pupils=Part('paired-small-pupils');brows=Part('supraorbital-living-ridges');nostrils=Part('paired-nostrils');teeth=Part('small-theropod-dentition')
        for s in (-1,1):
            eyes.ellipsoid((s*.080,-.904,1.213),(.011,.018,.013),12,6)
            pupils.ellipsoid((s*.090,-.908,1.214),(.003,.008,.009),10,6)
            brows.loft([(s*.063,-.855,1.226,.008,.008),(s*.074,-.895,1.231,.008,.008),(s*.069,-.945,1.225,.007,.007)],8)
            nostrils.ellipsoid((s*.054,-1.145,1.185),(.004,.011,.006),8,4)
            for k in range(8):
                y=-.92-.031*k;x=s*(.071-(k*.004));z=1.119 + k*.001
                teeth.loft([(x,y,z,.005,.007),(x,y-.002,z-.017,.0018,.0018)],6)
        eyes.finish([M['eye']]);pupils.finish([M['pupil']]);brows.finish([M['dorsal']]);nostrils.finish([M['mouth']]);teeth.finish([M['teeth']])
    # Normalize only to the frozen 3 m nose-to-tail estimate, never a unit cube.
    pts=_vertices_world(C);lo,hi=_bounds(pts);scale=P['target_length_m']/(hi[1]-lo[1])
    # Root remains identity at the middle of the pedal support footprint.
    footlo=-.27-.035-.035;foothi=.138+.035;fy=(footlo+foothi)/2
    for ob in C.objects:
        if ob.type=='MESH':
            for v in ob.data.vertices: v.co=Vector((v.co.x*scale,(v.co.y-fy)*scale,(v.co.z-.0055)*scale))
    pts=_vertices_world(C);lo,hi=_bounds(pts)
    for ob in C.objects:
        if ob.type=='MESH':
            for v in ob.data.vertices:v.co.z-=lo[2]
    return C

def render(collection,out,stage):
    points=_vertices_world(collection);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)])
    span=max(hi[i]-lo[i] for i in range(3));scene=bpy.context.scene
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8 if stage=='gray' else 32;scene.cycles.use_denoising=False
    scene.render.resolution_x=scene.render.resolution_y=320 if stage=='gray' else 768
    scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('evidence-studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.72,.72,.72,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45;scene.world=world
    for name,loc,power,size in [('key',(-3,-4,6),600,5),('fill',(4,-2,3),240,4),('rim',(0,4,5),350,3)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power*span*span/4;d.shape='DISK';d.size=size
        ob=bpy.data.objects.new(name,d);scene.collection.objects.link(ob);ob.location=center+Vector(loc);_look_at(ob,center)
    d=bpy.data.cameras.new('evidence-camera');cam=bpy.data.objects.new('evidence-camera',d);scene.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.clip_start=.01;d.clip_end=100
    clay=make_material('gray-model','#8B8E88')
    if stage=='gray':bpy.context.view_layer.material_override=clay
    directions={'front':(0,-1,0),'side':(1,0,0),'perspective':(1,-1,1)}
    if stage!='gray': directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    manifest=[];out.mkdir(parents=True,exist_ok=True)
    for name,vec in directions.items():
        cam.location=center+Vector(vec).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update()
        inv=cam.matrix_world.inverted();pr=[inv@p for p in points];xmin,xmax=min(p.x for p in pr),max(p.x for p in pr);ymin,ymax=min(p.y for p in pr),max(p.y for p in pr)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));d.ortho_scale=max(xmax-xmin,ymax-ymin)*1.18
        scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
        manifest.append({'path':name+'.png','sha256':digest(out/(name+'.png')),'direction':list(vec),'camera_location_m':list(cam.location),'orthographic_scale_m':d.ortho_scale,'resolution':scene.render.resolution_x})
    return {'method':'clean import of exact GLB' if stage!='gray' else 'source gray structural check before fine details','engine':'Cycles CPU','samples':scene.cycles.samples,'view_transform':'Standard','look':'None','background':'neutral world','views':manifest}

argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--stage',choices=['gray','final','rebuild','render'],default='final');args=p.parse_args(argv)
P=json.loads((SOURCE/'params.json').read_text());out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
if args.stage=='render':
    C=setup_scene('herrerasaurus-render');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(out/'model.glb'))
    for ob in set(bpy.data.objects)-before:
        for col in list(ob.users_collection):col.objects.unlink(ob)
        C.objects.link(ob)
    record=render(C,out/'views','final');record['glb_sha256']=digest(out/'model.glb');record['generator_sha256']=digest(__file__);save(out/'qa/evidence/views.json',record)
    (out/'preview.png').write_bytes((out/'views/perspective.png').read_bytes())
else:
    C=build(args.stage!='gray')
    if args.stage=='gray':save(out/'gray-manifest.json',render(C,out,'gray'))
    else:
        source=audit_source(C,max_triangles=18000)
        if source['errors']:raise RuntimeError(str(source['errors']))
        bpy.context.preferences.filepaths.save_version=0
        bpy.context.scene.render.filepath='//'
        for screen in bpy.data.screens:
            for area in screen.areas:
                for space in area.spaces:
                    if space.type=='FILE_BROWSER' and space.params:
                        space.params.directory=b'//'
        bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
        bpy.ops.object.select_all(action='DESELECT')
        for ob in C.objects:ob.select_set(True)
        bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
        options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
        available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
        assert not(set(options)-available),'Exporter option unavailable'
        bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
        glb=audit_glb(out/'model.glb',18000,8,36)
        if glb['errors']:raise RuntimeError(str(glb['errors']))
        if glb['bytes']>2000000:raise RuntimeError('GLB byte budget exceeded')
        # Audit uses a portable asset filename in the public record.
        if 'path' in glb:glb['path']='model.glb'
        if 'file' in glb:glb['file']='model.glb'
        b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
        err=max(abs(glb['bounds_m'][side][i]-expected[side][i]) for side in ('min','max') for i in range(3))
        assert err<.0001 and source['triangles']==glb['scene_triangles']
        save(out/'qa/evidence/build.json',{'check':'source-and-export','status':'PASS','blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),'generator_sha256':digest(__file__),'params_sha256':digest(SOURCE/'params.json'),'source':source,'glb':glb,'source_export_bounds_max_error_m':err,'export_options':options,'scope':'Static geometry and bounds only; independent visuals, GPU and scene are not tested.'})
